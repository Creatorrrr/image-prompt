import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.test_photo_workflow_precore import freeze_fixture, files, ROOT
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import photo_workflow as workflow
import record_image_run as recorder


class PhotoWorkflowStateTests(unittest.TestCase):
    def test_status_does_not_import_candidate_modules(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = freeze_fixture(Path(temp))
            code = 'import sys; sys.path.insert(0,sys.argv[1]); import photo_workflow; photo_workflow.main(["status","--run",sys.argv[2]]); assert "prompt_generator" not in sys.modules; assert "photo_runtime_sources" not in sys.modules'
            result = subprocess.run([sys.executable, "-c", code, str(SCRIPTS), str(run)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["phase"], "core_frozen")

    def test_cold_scripts_worker_can_verify_neutral_freeze_without_precore_path(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = freeze_fixture(Path(temp))
            code = 'import sys;sys.path.insert(0,sys.argv[1]);from photo_workflow_state import load_state,verify_freeze;verify_freeze(load_state(sys.argv[2]));assert "prompt_generator" not in sys.modules'
            result = subprocess.run([sys.executable, "-c", code, str(SCRIPTS), str(run)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_ledger_preserves_history_and_deduplicates_conflicts(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "ledger"; historical = b'{"run_id":"old","legacy":true}\n'; ledger.write_bytes(historical)
            row = {"run_id": "new", "workflow_operation_id": "a" * 32 + ":1", "attempt": 1}
            recorder.append_entry(ledger, row); once = ledger.read_bytes(); recorder.append_entry(ledger, row)
            self.assertEqual(once, ledger.read_bytes()); self.assertTrue(once.startswith(historical))
            with self.assertRaisesRegex(ValueError, "identity conflict"): recorder.append_entry(ledger, {**row, "attempt": 2})
            with self.assertRaisesRegex(ValueError, "identity conflict"): recorder.append_entry(ledger, {**row, "run_id": "other"})

    def test_concurrent_same_ledger_operation_has_one_row(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "ledger"
            code = 'import sys,pathlib;sys.path.insert(0,sys.argv[1]);from record_image_run import append_entry;append_entry(pathlib.Path(sys.argv[2]),{"run_id":"a","workflow_operation_id":"b"*32+":1"})'
            children = [subprocess.Popen([sys.executable, "-c", code, str(SCRIPTS), str(ledger)]) for _ in range(4)]
            self.assertEqual([p.wait() for p in children], [0] * 4)
            self.assertEqual(len(ledger.read_bytes().splitlines()), 1)

    def test_incomplete_pair_does_not_regenerate_or_change_seed(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = freeze_fixture(Path(temp))
            staging = run / ".staging/retrieve"; staging.mkdir(parents=True)
            files.atomic_write(staging / "transaction.json", files.encode({"seed": 9, "started": True}))
            args = argparse.Namespace(run=run, seed=None)
            with patch("subprocess.run", side_effect=AssertionError("must not regenerate")):
                with self.assertRaisesRegex(ValueError, "incomplete_retrieve_pair"): workflow.retrieve(args)
            args.seed = 10
            with self.assertRaisesRegex(ValueError, "retrieval_seed_conflict"): workflow.retrieve(args)

    def test_revision_admission_and_stale_status(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = freeze_fixture(Path(temp)); before = files.load_state(run)
            original_core = before["artifacts"]["authorial_core_input"]
            with files.locked_state(run) as state:
                files.commit_stage(run, state, "test_phase", {"composed": b'{}'})
            self.assertEqual(files.load_state(run)["artifacts"]["authorial_core_input"], original_core)
            files.bound_path(files.load_state(run), "composed").write_bytes(b'{"changed":true}')
            result = files.status(files.load_state(run)); self.assertEqual(result["phase"], "stale"); self.assertEqual(result["stale_roles"], ["composed"])


if __name__ == "__main__": unittest.main()
