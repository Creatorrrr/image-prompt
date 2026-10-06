#!/usr/bin/env python3
"""Resume remaining independent test modules with an explicit per-test ledger."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

OUT = Path(__file__).resolve().parent
PLAN = json.loads((OUT / "FULL-SUITE-RESUME-PLAN.json").read_text())
sys.path.insert(0, PLAN["checkout"])


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def worker(number):
    selected = set(PLAN["parts"][number])
    discovered = list(flatten(unittest.TestLoader().discover("tests")))
    ids = [test.id() for test in discovered]
    if ids != PLAN["discovery_ids"]:
        save(OUT / f"full-suite-discovery-mismatch-{number}.json",
             {"expected_ids": PLAN["discovery_ids"], "observed_ids": ids})
        raise RuntimeError("Test discovery changed after the resume checkpoint")
    suite = unittest.TestSuite(test for test in discovered if test.id() in selected)
    result_path = OUT / f"full-suite-part-{number}.json"
    statuses = {}
    details = []

    class LedgerResult(unittest.TextTestResult):
        def startTest(self, test):
            statuses[test.id()] = "RUNNING"
            super().startTest(test)

        def addSuccess(self, test):
            statuses[test.id()] = "PASS"
            super().addSuccess(test)

        def addFailure(self, test, err):
            statuses[test.id()] = "FAIL"
            details.append({"test_id": test.id(), "kind": "FAIL", "traceback": self._exc_info_to_string(err, test)})
            super().addFailure(test, err)

        def addError(self, test, err):
            statuses[test.id()] = "ERROR"
            details.append({"test_id": test.id(), "kind": "ERROR", "traceback": self._exc_info_to_string(err, test)})
            super().addError(test, err)

        def addSubTest(self, test, subtest, err):
            if err is not None:
                kind = "FAIL" if issubclass(err[0], test.failureException) else "ERROR"
                statuses[test.id()] = kind
                details.append({"test_id": test.id(), "subtest": str(subtest), "kind": kind,
                                "traceback": self._exc_info_to_string(err, test)})
            super().addSubTest(test, subtest, err)

        def addSkip(self, test, reason):
            statuses[test.id()] = "SKIP"
            super().addSkip(test, reason)

        def addExpectedFailure(self, test, err):
            statuses[test.id()] = "EXPECTED_FAILURE"
            super().addExpectedFailure(test, err)

        def addUnexpectedSuccess(self, test):
            statuses[test.id()] = "UNEXPECTED_SUCCESS"
            super().addUnexpectedSuccess(test)

        def stopTest(self, test):
            super().stopTest(test)
            save(result_path, {"worker": number, "status": "RUNNING", "planned": len(selected),
                               "outcomes": statuses, "details": details, "completed": self.testsRun})

    with (OUT / f"full-suite-part-{number}.log").open("w") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=1, resultclass=LedgerResult).run(suite)
    payload = {"worker": number, "status": "COMPLETE", "planned": len(selected), "outcomes": statuses,
               "details": details, "completed": result.testsRun, "failures": len(result.failures),
               "errors": len(result.errors), "skipped": len(result.skipped),
               "coverage_complete": set(statuses) == selected and all(v != "RUNNING" for v in statuses.values()),
               "successful": result.wasSuccessful()}
    save(result_path, payload)
    print(f"Worker {number}: {result.testsRun}/{len(selected)} tests, {len(result.failures)} failures, {len(result.errors)} errors", flush=True)
    return 0 if result.wasSuccessful() and payload["coverage_complete"] else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int)
    args = parser.parse_args()
    if args.worker is not None:
        sys.exit(worker(args.worker))
    jobs = [subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--worker", str(number)],
                             cwd=PLAN["checkout"]) for number in range(len(PLAN["parts"]))]
    remaining = set(range(len(jobs)))
    while remaining:
        for number in list(remaining):
            if jobs[number].poll() is not None:
                remaining.remove(number)
                print(f"Worker {number} ended with {jobs[number].returncode}", flush=True)
        if remaining:
            time.sleep(0.5)
    outcomes = dict(PLAN["prefix_statuses"])
    details = []
    for number in range(len(jobs)):
        result = json.loads((OUT / f"full-suite-part-{number}.json").read_text())
        outcomes.update(result["outcomes"])
        details.extend(result["details"])
    complete = set(outcomes) == set(PLAN["discovery_ids"]) and all(v != "RUNNING" for v in outcomes.values())
    summary = {"status": "COMPLETE" if complete else "INCOMPLETE", "test_total": PLAN["test_total"],
               "unique_tests_covered": len(outcomes), "all_discovered_tests_covered": complete,
               "outcomes": outcomes, "worker_failure_details": details,
               "original_sequential_failures": [k for k, v in PLAN["prefix_statuses"].items() if v == "FAIL"],
               "restored_dependency_initial_errors": [k for k, v in PLAN["prefix_statuses"].items() if v.startswith("ERROR_INITIAL")],
               "original_log": "full-suite.initial-sequential.log",
               "checkpoint_safety_repeated_test": PLAN["last_completed_test_repeated_for_checkpoint_safety"],
               "expectations_or_holdouts_rewritten": False}
    save(OUT / "FULL-SUITE-COVERAGE.json", summary)
    print(f"Full suite coverage: {len(outcomes)}/{PLAN['test_total']} unique tests; complete={complete}", flush=True)
    sys.exit(0 if complete and not details and not summary["original_sequential_failures"] else 1)


if __name__ == "__main__":
    main()
