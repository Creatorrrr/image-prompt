"""Run every discovered unittest once, in four isolated module groups."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def leaves(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from leaves(item)
        else:
            yield item


def worker(number):
    manifest = json.loads((HERE / "full-suite-coverage.json").read_text())
    group = manifest["groups"][number]
    suite = unittest.defaultTestLoader.loadTestsFromNames(group["modules"])
    actual = sorted(test.id() for test in leaves(suite))
    if actual != sorted(group["test_ids"]):
        raise RuntimeError("Discovered coverage changed before worker execution")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    save(HERE / f"full-suite-worker-{number}.json", {
        "modules": group["modules"], "test_ids": actual,
        "tests_run": result.testsRun, "successful": result.wasSuccessful(),
        "failures": [{"test_id": case.id(), "traceback": tb} for case, tb in result.failures],
        "errors": [{"test_id": case.id(), "traceback": tb} for case, tb in result.errors],
        "skipped": [{"test_id": case.id(), "reason": reason} for case, reason in result.skipped],
        "expected_failures": [case.id() for case, _ in result.expectedFailures],
        "unexpected_successes": [case.id() for case in result.unexpectedSuccesses],
    })
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int)
    args = parser.parse_args()
    if args.worker is not None:
        return worker(args.worker)
    tests = list(leaves(unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))))
    by_module = {}
    for test in tests:
        by_module.setdefault(type(test).__module__, []).append(test.id())
    groups = [{"modules": [], "test_ids": []} for _ in range(4)]
    for module, ids in sorted(by_module.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        target = min(groups, key=lambda group: len(group["test_ids"]))
        target["modules"].append(module)
        target["test_ids"].extend(ids)
    save(HERE / "full-suite-coverage.json", {
        "test_count": len(tests), "module_count": len(by_module), "groups": groups,
        "test_module_sha256": {module: hashlib.sha256((ROOT / (module.replace(".", "/") + ".py")).read_bytes()).hexdigest()
                               for module in by_module},
        "coverage_rule": "Every discovered test ID appears in exactly one worker; no filters or exclusions.",
    })
    handles, processes = [], []
    for number in range(4):
        handle = (HERE / f"full-suite-worker-{number}.log").open("w")
        handles.append(handle)
        processes.append(subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--worker", str(number)],
                                          cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT))
    codes = [process.wait() for process in processes]
    for handle in handles:
        handle.close()
    results = [json.loads((HERE / f"full-suite-worker-{number}.json").read_text()) for number in range(4)]
    delivered = [test_id for result in results for test_id in result["test_ids"]]
    exact = len(set(delivered)) == len(tests) and sorted(delivered) == sorted(test.id() for test in tests)
    summary = {
        "coverage_complete": exact,
        "test_count": len(tests), "module_count": len(by_module),
        "tests_run": sum(result["tests_run"] for result in results),
        "successful": exact and all(result["successful"] for result in results) and all(code == 0 for code in codes),
        "worker_exit_codes": codes,
        **{key: [item for result in results for item in result[key]] for key in
           ("failures", "errors", "skipped", "expected_failures", "unexpected_successes")},
    }
    save(HERE / "full-suite-summary.json", summary)
    print(json.dumps({key: value for key, value in summary.items() if key not in ("failures", "errors")}, ensure_ascii=False))
    return 0 if summary["successful"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
