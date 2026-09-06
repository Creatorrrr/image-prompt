#!/usr/bin/env python3
"""Run the discovered suite in process-isolated batches and retain every result."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item.id()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--worker-ids", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    os.chdir(root)
    sys.path.insert(0, str(root))
    if args.worker_ids:
        ids = json.loads(args.worker_ids.read_text())
        suite = unittest.defaultTestLoader.loadTestsFromNames(ids)
        start = time.monotonic()
        with (output / "unittest.log").open("w") as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        record = {
            "tests": result.testsRun, "seconds": time.monotonic() - start,
            "failures": [{"id": t.id(), "traceback": trace} for t, trace in result.failures],
            "errors": [{"id": t.id(), "traceback": trace} for t, trace in result.errors],
            "skipped": [{"id": t.id(), "reason": reason} for t, reason in result.skipped],
            "expected_failures": [t.id() for t, _ in result.expectedFailures],
            "unexpected_successes": [t.id() for t in result.unexpectedSuccesses],
            "status": "pass" if result.wasSuccessful() else "fail",
        }
        (output / "result.json").write_text(json.dumps(record, indent=2) + "\n")
        return 0

    ids = list(flatten(unittest.defaultTestLoader.discover(str(root / "tests"), top_level_dir=str(root))))
    (output / "discovered-test-ids.json").write_text(json.dumps(ids, indent=2) + "\n")
    batches = [ids[i:i + args.batch_size] for i in range(0, len(ids), args.batch_size)]
    script = str(Path(__file__).resolve())
    started = time.monotonic()

    def run_batch(item):
        index, test_ids = item
        batch = output / f"batch-{index:03d}"
        batch.mkdir(exist_ok=True)
        path = batch / "test-ids.json"
        path.write_text(json.dumps(test_ids) + "\n")
        with (batch / "process.log").open("w") as stream:
            completed = subprocess.run(
                [sys.executable, script, "--root", str(root), "--output", str(batch), "--worker-ids", str(path)],
                stdout=stream, stderr=subprocess.STDOUT,
            )
        result_path = batch / "result.json"
        return index, json.loads(result_path.read_text()) if result_path.exists() else {
            "status": "process_error", "exit_code": completed.returncode, "ids": test_ids,
        }

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for future in concurrent.futures.as_completed([executor.submit(run_batch, row) for row in enumerate(batches)]):
            index, result = future.result()
            results.append({"batch": index, **result})
            print(f"completed {len(results)}/{len(batches)} batches; batch {index}: {result['status']}", flush=True)
            (output / "progress.json").write_text(json.dumps(results, indent=2) + "\n")
    summary = {
        "root": str(root), "discovered": len(ids), "executed": sum(r.get("tests", 0) for r in results),
        "seconds": time.monotonic() - started,
        "failures": [f for r in results for f in r.get("failures", [])],
        "errors": [f for r in results for f in r.get("errors", [])],
        "skipped": [f for r in results for f in r.get("skipped", [])],
        "process_errors": [r for r in results if r["status"] == "process_error"],
        "unexpected_successes": [f for r in results for f in r.get("unexpected_successes", [])],
    }
    summary["status"] = "pass" if not any(summary[k] for k in ("failures", "errors", "process_errors", "unexpected_successes")) and summary["executed"] == len(ids) else "fail"
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in summary.items()}), flush=True)
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
