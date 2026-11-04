"""Live progress must not affect authoritative run status or leak text."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import tempfile
import unittest

PRECORE = Path(__file__).resolve().parents[1] / "precore"
sys.path.insert(0, str(PRECORE))
import photo_run_files as files


class ProgressStatusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name)
        raw = self.run / "revisions" / "revision" / "request_raw.json"
        raw.parent.mkdir(parents=True)
        raw.write_bytes(b"request")
        self.state = {"run_id": "run", "schema_version": files.VERSION, "mode": "prompt_only",
                      "phase": "slot_intents_authored", "artifacts": {"request_raw": {
                          "path": str(raw), "sha256": files.digest(raw.read_bytes())}}, "operations": []}
        self.path = self.run / ".staging" / "h-f2" / "progress.json"
        self.path.parent.mkdir(parents=True)

    def progress(self, **overrides):
        now = datetime.now(timezone.utc)
        row = {"schema": "photo-h-f2-progress/v1", "stage": "receipt_audit",
               "start_at": (now - timedelta(minutes=3)).isoformat(), "updated_at": now.isoformat(),
               "completed_queries": 3, "total_queries": 3, "pid": 123, "status": "running"}
        row.update(overrides)
        self.path.write_text(json.dumps(row))
        return files.status(self.state)

    def test_unavailable_and_observed_are_not_completion(self):
        self.assertEqual(files.status(self.state)["progress"], {"state": "unavailable"})
        result = self.progress()
        self.assertEqual(result["progress"]["state"], "observed")
        self.assertEqual(result["progress"]["stage"], "receipt_audit")
        self.assertEqual(result["phase"], "slot_intents_authored")
        self.assertIsNone(result["technical_qualification"])

    def test_stale_heartbeat_does_not_assert_failure(self):
        past = (datetime.now(timezone.utc) - timedelta(minutes=3)).isoformat()
        result = self.progress(start_at=past, updated_at=past)
        self.assertEqual(result["progress"]["state"], "stale")
        self.assertEqual(result["progress"]["status"], "running")
        self.assertEqual(result["phase"], "slot_intents_authored")

    def test_composition_and_delivery_are_observational_stages(self):
        for stage in ("composition_audit", "composition_audited", "delivery_audit", "delivery_complete"):
            with self.subTest(stage=stage):
                result = self.progress(stage=stage)
                self.assertEqual(result["progress"]["stage"], stage)
                self.assertEqual(result["phase"], "slot_intents_authored")
                self.assertIsNone(result["technical_qualification"])

    def test_corrupt_and_unexpected_content_cannot_be_reflected(self):
        self.path.write_text('{"prompt":"sensitive"')
        self.assertEqual(files.status(self.state)["progress"], {"state": "invalid"})
        result = self.progress(stage="sensitive prompt text")
        self.assertEqual(result["progress"], {"state": "invalid"})
        self.assertNotIn("sensitive", json.dumps(result))
        self.assertEqual(result["phase"], "slot_intents_authored")

    def test_wrong_counts_and_timestamp_are_invalid(self):
        self.assertEqual(self.progress(completed_queries=4)["progress"], {"state": "invalid"})
        self.assertEqual(self.progress(updated_at="not-a-date")["progress"], {"state": "invalid"})


if __name__ == "__main__":
    unittest.main()
