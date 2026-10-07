"""Current V37 caller behavior plus unchanged copied-legacy fixture assertions."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tests import photo_workflow_boundary_v37 as v

ROOT = Path(__file__).resolve().parents[1]
legacy = v._load_module(ROOT / v.retained_name("tests/test_photo_camera_guidance_v36_compatibility.py"),
                        "_v37_copied_legacy_controls")
legacy.ROOT = ROOT
validator = legacy.LIVE_VALIDATOR


def setUpModule():
    legacy.setUpModule()


class CopiedV6Tests(legacy.CopiedV6Tests): pass
class CopiedV10Tests(legacy.CopiedV10Tests): pass
class CopiedV11Tests(legacy.CopiedV11Tests): pass
class CopiedV12Tests(legacy.CopiedV12Tests): pass
class CopiedV13Tests(legacy.CopiedV13Tests): pass
class CopiedReligionTests(legacy.CopiedReligionTests): pass
class CopiedSlangTests(legacy.CopiedSlangTests): pass
class CopiedAppearanceTests(legacy.CopiedAppearanceTests): pass


class CurrentCallerTests(unittest.TestCase):
    def test_default_current_and_explicit_history_use_v37_dispatch(self):
        self.assertTrue((ROOT / v.CURRENT_BASELINE).is_file())
        for version in (None, 37, 36, 35, 13, 6):
            sentinel = object(); support = SimpleNamespace(dispatch=mock.Mock(return_value=sentinel))
            with self.subTest(version=version), mock.patch.object(validator, "_workflow_v37_support", return_value=support) as loader, \
                    mock.patch.object(validator, "_camera_v36_support") as old_loader:
                result = validator.validate_photo_regression_baseline(ROOT / v.ASSETS, baseline_version=version)
                self.assertIs(result, sentinel)
                loader.assert_called_once_with(ROOT)
                support.dispatch.assert_called_once_with(ROOT / v.ASSETS, source_root=ROOT, baseline_version=version)
                old_loader.assert_not_called()

    def test_explicit_37_wrong_root_rejects_before_support_import(self):
        with tempfile.TemporaryDirectory() as temporary, mock.patch.object(validator, "_workflow_v37_support") as loader:
            with self.assertRaisesRegex(validator.ValidationFailure, "asset directory mismatch"):
                validator.validate_photo_regression_baseline(Path(temporary), baseline_version=37)
            loader.assert_not_called()

    def test_failures_preserve_public_type_message_and_cause(self):
        for failure in (AssertionError("source rejected"), RuntimeError("exact original unavailable"), ValueError("bad JSON")):
            support = SimpleNamespace(dispatch=mock.Mock(side_effect=failure))
            with self.subTest(failure=type(failure).__name__), mock.patch.object(validator, "_workflow_v37_support", return_value=support):
                with self.assertRaises(validator.ValidationFailure) as caught:
                    validator.validate_photo_regression_baseline(ROOT / v.ASSETS)
                self.assertIs(caught.exception.__cause__, failure)
                self.assertEqual(str(caught.exception), str(failure))

    def test_real_cli_main_emits_normal_failure_json(self):
        failure = AssertionError("controlled V37 source rejection")
        support = SimpleNamespace(dispatch=mock.Mock(side_effect=failure))
        def photo_only(asset_dir, *, verify_local_images):
            self.assertIsNone(asset_dir); self.assertFalse(verify_local_images)
            return validator.validate_photo_regression_baseline(ROOT / v.ASSETS)
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(validator, "_workflow_v37_support", return_value=support), \
                mock.patch.object(validator, "validate_all", side_effect=photo_only), \
                mock.patch.object(sys, "argv", [str(ROOT / v.VALIDATOR)]), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = validator.main()
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(stdout.getvalue()), {"status": "fail", "error": str(failure)})
        self.assertEqual(stderr.getvalue(), "")

    def test_new_baseline_is_present_in_copied_legacy_fixture_delivery(self):
        self.assertTrue((legacy.FIXTURE_ROOT / v.CURRENT_BASELINE).is_file())


if __name__ == "__main__":
    unittest.main()
