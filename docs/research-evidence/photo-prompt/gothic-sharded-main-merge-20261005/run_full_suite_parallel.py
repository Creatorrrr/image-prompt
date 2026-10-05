"""Run every discovered test on the reviewed V22 successor, retaining each assertion and traceback.

Modules use independent processes and their normal unittest order. Only Python's
regex compilation cache capacity is enlarged in these test processes; regex
patterns, matching behavior, repository source and tests remain unchanged.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

EVIDENCE = Path(__file__).resolve().parent
ROOT = Path.cwd()
WORKERS = 6
CACHE_CAPACITY = 200_000


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def drift():
    frozen = json.loads((EVIDENCE / "SOURCES-FROZEN.json").read_text())
    return [name for name, sha in frozen.items()
            if not (ROOT / name).is_file()
            or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != sha]


def worker(index):
    shard = json.loads((EVIDENCE / "FULL-SUITE-PARALLEL-PLAN.json").read_text())["shards"][index]
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "tests"))
    re._MAXCACHE = CACHE_CAPACITY
    if hasattr(re, "_MAXCACHE2"):
        re._MAXCACHE2 = CACHE_CAPACITY
    suite = unittest.defaultTestLoader.loadTestsFromNames(shard["modules"])
    ids = [test.id() for test in flatten(suite)]
    if ids != shard["test_ids"]:
        raise RuntimeError(f"Assigned test IDs differ from loaded tests in worker {index}")
    started = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    record = dict(worker=index, expected_test_ids=shard["test_ids"], actual_test_ids=ids,
                  exact_assigned_test_ids=ids == shard["test_ids"], tests_run=result.testsRun,
                  wall_seconds=time.monotonic()-started,
                  failures=[dict(test=str(test), traceback=tb) for test, tb in result.failures],
                  errors=[dict(test=str(test), traceback=tb) for test, tb in result.errors],
                  skipped=[dict(test=str(test), reason=reason) for test, reason in result.skipped],
                  expected_failures=[str(test) for test, _ in result.expectedFailures],
                  unexpected_successes=[str(test) for test in result.unexpectedSuccesses],
                  was_successful=result.wasSuccessful(), regex_cache_capacity=CACHE_CAPACITY)
    save(EVIDENCE / f"parallel-worker-{index}.result.json", record)
    return 0 if result.wasSuccessful() and record["exact_assigned_test_ids"] else 1


def main():
    ids = json.loads((EVIDENCE / "FULL-SUITE-ORDER.json").read_text())
    modules = {}
    for tid in ids:
        modules.setdefault(tid.split(".")[0], []).append(tid)
    shards = [dict(worker=i, modules=[], test_ids=[], assigned_count=0) for i in range(WORKERS)]
    for module, tids in sorted(modules.items(), key=lambda item: (-len(item[1]), item[0])):
        target = min(shards, key=lambda item: item["assigned_count"])
        target["modules"].append(module)
        target["assigned_count"] += len(tids)
    for shard in shards:
        shard["modules"].sort()
        shard["test_ids"] = [tid for m in shard["modules"] for tid in modules[m]]
    assigned = [tid for shard in shards for tid in shard["test_ids"]]
    if sorted(assigned) != sorted(ids) or len(assigned) != len(set(assigned)) or any(not s["modules"] for s in shards):
        raise RuntimeError("Full-suite plan must assign all tests exactly once across nonempty workers")
    before = drift()
    if before:
        raise RuntimeError(f"Frozen source drift before suite: {before}")
    save(EVIDENCE / "FULL-SUITE-PARALLEL-PLAN.json", dict(
        runtime_root=str(ROOT), expected_count=len(ids), module_count=len(modules),
        source_state="V22 source and tests frozen; exact historical dependencies restored",
        assertion_or_repository_changes=False, regex_cache_capacity=CACHE_CAPACITY,
        cache_note="Compilation reuse only; original regex patterns and matches are unchanged.",
        shards=shards))
    started = time.monotonic()
    jobs = []
    for shard in shards:
        log = (EVIDENCE / f"parallel-worker-{shard['worker']}.log").open("w")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                                    "--worker", str(shard["worker"])],
                                   cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=env)
        jobs.append((process, log))
    exits = []
    for process, log in jobs:
        exits.append(process.wait())
        log.close()
    results = [json.loads((EVIDENCE / f"parallel-worker-{i}.result.json").read_text())
               for i in range(WORKERS)]
    actual = [tid for result in results for tid in result["actual_test_ids"]]
    after = drift()
    aggregate = dict(expected_tests=len(ids), tests_run=sum(r["tests_run"] for r in results),
                     modules=len(modules), workers=WORKERS, worker_exit_codes=exits,
                     all_test_ids_exactly_once=sorted(ids)==sorted(actual) and len(actual)==len(set(actual)),
                     failure_count=sum(len(r["failures"]) for r in results),
                     error_count=sum(len(r["errors"]) for r in results),
                     skipped_count=sum(len(r["skipped"]) for r in results),
                     failures=[f for r in results for f in r["failures"]],
                     errors=[e for r in results for e in r["errors"]],
                     wall_seconds=time.monotonic()-started,
                     regex_cache_capacity=CACHE_CAPACITY,
                     source_drift_before=before, source_drift_after=after,
                     user_judgment="pending")
    aggregate["status"] = "PASS" if all(code == 0 for code in exits) and not after else "FAIL"
    save(EVIDENCE / "FULL-SUITE-PARALLEL-RESULT.json", aggregate)
    print(json.dumps({k:v for k,v in aggregate.items() if k not in {"failures","errors"}}, indent=2))
    return 0 if aggregate["status"]=="PASS" else 1


if __name__ == "__main__":
    raise SystemExit(worker(int(sys.argv[2])) if len(sys.argv)>1 and sys.argv[1]=="--worker" else main())
