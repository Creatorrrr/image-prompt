"""Complete unittest discovery, with a fresh offline process per module."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--module")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(args.repo))
    for name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
        os.environ.pop(name, None)
    if args.module:
        executed = []
        runtime_sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (args.repo / "skills/photo-prompt-image-generator/scripts").glob("*.py")}
        data_sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (args.repo / "skills/photo-prompt-image-generator/assets").glob("*.json")}

        class RecordedResult(unittest.TextTestResult):
            def startTest(self, test):
                executed.append(test.id())
                super().startTest(test)

        suite = unittest.defaultTestLoader.loadTestsFromName(args.module)
        result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(suite)
        payload = {"module": args.module, "tests_run": result.testsRun, "executed_ids": executed,
            "runtime_sources": runtime_sources, "data_sources": data_sources,
            "failures": [{"id": t.id(), "traceback": trace} for t, trace in result.failures],
            "errors": [{"id": t.id(), "traceback": trace} for t, trace in result.errors],
            "skipped": [{"id": t.id(), "reason": reason} for t, reason in result.skipped],
            "expected_failures": [t.id() for t, _ in result.expectedFailures],
            "unexpected_successes": [t.id() for t in result.unexpectedSuccesses]}
        (args.output / f"{args.module}.json").write_text(json.dumps(payload, indent=2) + "\n")
        return 0 if result.wasSuccessful() else 1
    loader = unittest.TestLoader()
    suite = loader.discover(str(args.repo / "tests"), top_level_dir=str(args.repo))
    if loader.errors:
        raise RuntimeError("\n".join(loader.errors))
    ids = [t.id() for t in flatten(suite)]
    assert len(set(ids)) == len(ids), "duplicate discovery IDs"
    modules = sorted({t.rsplit(".", 2)[0] for t in ids})
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo, text=True).strip()
    discovery = {"commit": commit, "discovered_ids": ids, "modules": modules,
        "method": "complete unittest discovery, isolated offline module processes", "workers": args.workers}
    (args.output / "discovery.json").write_text(json.dumps(discovery, indent=2) + "\n")
    environment = os.environ.copy()
    for name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(name, None)

    def run(module):
        started = time.monotonic()
        log = args.output / f"{module}.log"
        with log.open("w") as stream:
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--repo", str(args.repo),
                "--output", str(args.output), "--module", module], cwd=args.repo, env=environment,
                stdout=stream, stderr=subprocess.STDOUT)
        return {"module": module, "returncode": proc.returncode,
            "seconds": round(time.monotonic() - started, 3), "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}

    started = time.monotonic()
    results = []
    print(f"Discovered {len(ids)} tests in {len(modules)} modules at {commit}.", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, module) for module in modules]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Completed {len(results)}/{len(modules)}: {result['module']} rc={result['returncode']}", flush=True)
            (args.output / "progress.json").write_text(json.dumps(results, indent=2) + "\n")
    records = [json.loads((args.output / f"{r['module']}.json").read_text())
               for r in results if (args.output / f"{r['module']}.json").exists()]
    executed = [i for r in records for i in r["executed_ids"]]
    summary = {"commit": commit, "method": discovery["method"], "workers": args.workers,
        "discovered_tests": len(ids), "executed_tests": sum(r["tests_run"] for r in records),
        "module_count": len(modules), "missing_execution_ids": sorted(set(ids) - set(executed)),
        "unexpected_execution_ids": sorted(set(executed) - set(ids)),
        "duplicate_execution_ids": sorted({i for i in executed if executed.count(i) > 1}),
        "failures": [f for r in records for f in r["failures"]],
        "errors": [f for r in records for f in r["errors"]],
        "skipped": [f for r in records for f in r["skipped"]],
        "module_results": sorted(results, key=lambda r: r["module"]),
        "wall_seconds": round(time.monotonic() - started, 3)}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "module_results"}), flush=True)
    return 0 if all(r["returncode"] == 0 for r in results) and not summary["missing_execution_ids"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
