"""Run the complete unittest discovery set in independent module processes."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "full-suite"
sys.path.insert(0, str(ROOT))


def ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from ids(item)
        else:
            yield item.id()


def worker(pattern):
    OUT.mkdir(exist_ok=True)
    name = Path(pattern).stem
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern=pattern)
    discovered = list(ids(suite))
    started = time.time()
    with (OUT / f"{name}.log").open("w") as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    record = {
        "pattern": pattern,
        "discovered_ids": discovered,
        "tests_run": result.testsRun,
        "success": result.wasSuccessful(),
        "failures": [{"id": test.id(), "traceback": trace} for test, trace in result.failures],
        "errors": [{"id": test.id(), "traceback": trace} for test, trace in result.errors],
        "skipped": [{"id": test.id(), "reason": reason} for test, reason in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
        "elapsed_seconds": round(time.time() - started, 3),
    }
    (OUT / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n")
    return 0 if record["success"] else 1


def launch(pattern):
    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--worker", pattern],
        cwd=ROOT, capture_output=True, text=True,
    )
    path = OUT / f"{Path(pattern).stem}.json"
    if not path.exists():
        raise RuntimeError(f"Worker {pattern} returned {completed.returncode}: {completed.stderr[-2000:]}")
    record = json.loads(path.read_text())
    record["process_exit_code"] = completed.returncode
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.worker:
        return worker(args.worker)
    OUT.mkdir(exist_ok=True)
    started = time.time()
    loader = unittest.TestLoader()
    expected = sorted(ids(loader.discover(str(ROOT / "tests"))))
    patterns = sorted(path.name for path in (ROOT / "tests").glob("test*.py"))
    records = []
    reused = 0
    pending = []
    for pattern in patterns:
        path = OUT / f"{Path(pattern).stem}.json"
        expected_module = sorted(ids(loader.discover(str(ROOT / "tests"), pattern=pattern)))
        cached = json.loads(path.read_text()) if args.resume and path.exists() else None
        if cached and cached["success"] and sorted(cached["discovered_ids"]) == expected_module:
            cached["reused_successful_module_evidence"] = True
            records.append(cached)
            reused += 1
        else:
            pending.append(pattern)
    print(f"Discovered {len(expected)} tests in {len(patterns)} modules; workers={args.workers}", flush=True)
    print(f"Reused {reused} valid successful modules; running {len(pending)} modules", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(launch, pattern): pattern for pattern in pending}
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            print(f"{len(records)}/{len(patterns)} {record['pattern']}: "
                  f"{'PASS' if record['success'] else 'FAIL'} "
                  f"{record['tests_run']} tests in {record['elapsed_seconds']} s", flush=True)
    actual = sorted(test_id for record in records for test_id in record["discovered_ids"])
    same_discovery = actual == expected
    summary = {
        "contract_version": "module-parallel-unittest-evidence/v1",
        "invocation": ".venv/bin/python run_full_suite.py --workers 6",
        "equivalent_serial_scope": ".venv/bin/python -m unittest discover -s tests",
        "discovery_multiset_equal": same_discovery,
        "discovery_ids_sha256": hashlib.sha256("\n".join(expected).encode()).hexdigest(),
        "module_count": len(records),
        "reused_successful_module_count": reused,
        "tests_discovered": len(expected),
        "tests_run": sum(record["tests_run"] for record in records),
        "success": same_discovery and all(record["success"] for record in records),
        "failures": [failure for record in records for failure in record["failures"]],
        "errors": [error for record in records for error in record["errors"]],
        "skipped": [skip for record in records for skip in record["skipped"]],
        "expected_failures": [test for record in records for test in record["expected_failures"]],
        "unexpected_successes": [test for record in records for test in record["unexpected_successes"]],
        "elapsed_seconds": round(time.time() - started, 3),
        "modules": sorted(records, key=lambda record: record["pattern"]),
    }
    (HERE / "FULL-SUITE-RESULT.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "modules"}), flush=True)
    return 0 if summary["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
