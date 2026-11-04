"""Progress reporting is observational and cannot change audit results.

Set PHOTO_H_F2_TEST_NATIVE to a sealed native generation directory to load its
dependencies while testing the reviewed workflow overlay. No runtime is needed
for ordinary test discovery; these checks skip without the environment value.
"""
import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]
OVERLAY = SKILL / "runtime-overlays/h-f2/scripts/photo_workflow.py"
NATIVE = os.environ.get("PHOTO_H_F2_TEST_NATIVE")


@unittest.skipUnless(NATIVE, "set PHOTO_H_F2_TEST_NATIVE to a sealed native generation")
class AuditProgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scripts = Path(NATIVE).resolve() / "scripts"
        if not scripts.is_dir():
            raise AssertionError("PHOTO_H_F2_TEST_NATIVE must name a native generation directory")
        sys.path.insert(0, str(scripts))
        cls.addClassCleanup(lambda: sys.path.remove(str(scripts)))
        spec = importlib.util.spec_from_file_location("_photo_workflow_audit_progress_test", OVERLAY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.workflow = module

    def setUp(self):
        self.events = []
        events = self.events

        class Progress:
            def __init__(self, run):
                events.append(("init", run))

            def update(self, stage, status="running"):
                events.append((stage, status))

        self.progress = Progress
        self.state = {"h_f2_binding": {"generation_id": "fixed"}}

    def call(self, state, action, start="composition_audit", finish="composition_audited"):
        with patch.dict(sys.modules, {"photo_h_f2_workflow": types.SimpleNamespace(Progress=self.progress)}):
            return self.workflow._with_h_f2_audit_progress(state, "/isolated/run", start, finish, action)

    def test_success_keeps_exact_result(self):
        result = {"status": "pass", "failures": [], "evidence": {"unchanged": True}}
        self.assertIs(self.call(self.state, lambda: result), result)
        self.assertEqual(self.events, [("init", "/isolated/run"), ("composition_audit", "running"),
                                       ("composition_audited", "complete")])

    def test_failed_result_is_not_promoted(self):
        result = {"status": "fail", "failures": ["existing_audit_failure"]}
        self.assertIs(self.call(self.state, lambda: result, "delivery_audit", "delivery_complete"), result)
        self.assertEqual(self.events[-2:], [("delivery_audit", "running"), ("failed", "failed")])

    def test_audit_exception_propagates_unchanged(self):
        error = ValueError("audit failed")
        def operation():
            raise error
        with self.assertRaises(ValueError) as actual:
            self.call(self.state, operation)
        self.assertIs(actual.exception, error)
        self.assertEqual(self.events[-1], ("failed", "failed"))

    def test_non_h_f2_does_not_instantiate_progress(self):
        result = {"status": "pass"}
        self.assertIs(self.call({}, lambda: result), result)
        self.assertEqual(self.events, [])

    def test_progress_write_failure_does_not_change_success_or_exception(self):
        class BrokenProgress:
            def __init__(self, run):
                pass
            def update(self, *args, **kwargs):
                raise OSError("progress file unavailable")
        self.progress = BrokenProgress
        result = {"status": "pass", "failures": []}
        self.assertIs(self.call(self.state, lambda: result), result)
        error = RuntimeError("real audit failure")
        def operation():
            raise error
        with self.assertRaises(RuntimeError) as actual:
            self.call(self.state, operation)
        self.assertIs(actual.exception, error)


if __name__ == "__main__":
    unittest.main()
