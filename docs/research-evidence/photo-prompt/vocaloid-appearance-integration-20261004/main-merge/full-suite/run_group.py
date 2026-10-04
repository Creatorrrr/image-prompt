"""Complete the remaining discovered tests and retain per-case outcomes."""
from __future__ import annotations

import hashlib
import json
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tests").is_dir() and (p / ".git").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
group = int(sys.argv[1])
plan = json.loads((HERE / "PLAN.json").read_text())
ids = plan["groups"][group]
events_path = HERE / f"group-{group}-events.ndjson"
assert not events_path.exists(), "Use a unique run prefix; do not replace prior outcomes."
test_paths = sorted({ROOT / "tests" / (test_id.split(".")[0] + ".py") for test_id in ids})
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = {str(p): digest(p) for p in test_paths}


class RetainedResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        self.started = time.monotonic()
        self.subtest_details = []
        self.retained = False

    def retain(self, test, outcome, detail=None):
        self.retained = True
        row = {"id": test.id(), "outcome": outcome,
               "elapsed_seconds": round(time.monotonic() - getattr(self, "started", time.monotonic()), 3)}
        if detail is not None:
            row["detail"] = detail
        with events_path.open("a") as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.subtest_details.append(self._exc_info_to_string(err, subtest))

    def stopTest(self, test):
        if self.subtest_details and not self.retained:
            self.retain(test, "fail", "\n".join(self.subtest_details))
        super().stopTest(test)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.retain(test, "pass")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.retain(test, "fail", self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.retain(test, "error", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.retain(test, "skip", reason)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.retain(test, "expected_failure", self._exc_info_to_string(err, test))

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.retain(test, "unexpected_success")


loader = unittest.TestLoader()
suite = loader.loadTestsFromNames(ids)
started_at = time.time()
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=1, resultclass=RetainedResult).run(suite)
events = [json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
observed = {event["id"] for event in events}
after = {str(p): digest(p) for p in test_paths}
complete = observed == set(ids) and result.testsRun == len(ids) and not loader.errors
receipt = {
    "schema_version": "photo-unittest-completion-group/v1", "group": group,
    "expected_count": len(ids), "tests_run": result.testsRun,
    "elapsed_seconds": round(time.time() - started_at, 3),
    "coverage_complete": complete, "missing_ids": sorted(set(ids) - observed),
    "unexpected_ids": sorted(observed - set(ids)), "loader_errors": loader.errors,
    "test_files_unchanged": before == after, "test_file_sha256": after,
    "status": "pass" if result.wasSuccessful() and complete and before == after else "fail",
    "events": events,
}
(HERE / f"group-{group}-results.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
raise SystemExit(0 if receipt["status"] == "pass" else 1)
