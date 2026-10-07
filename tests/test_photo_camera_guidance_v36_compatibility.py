"""Focused public-entry compatibility using unchanged legacy fixture tests.

These controls replay preserved observations through the actual validator. They
do not generate packs, qualify the current runtime, or claim historical Python
equivalence. The legacy tests retain their original subprocess/source-hash
fixtures and assertions. Four missing observations/proof files are delivered
from authenticated, local-only 8c Git objects into a temporary fixture root.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tests import photo_camera_guidance_history_v36 as history
from tests import test_photo_current_boundary_snapshot as v6_tests
from tests import test_photo_latest_metadata_boundary_history as v11_tests
from tests import test_photo_nape_metadata_boundary_history as metadata_tests
from tests import test_photo_religion_iconography_boundary_history as religion_tests
from tests import test_photo_slang_boundary_history as slang_tests
from tests import test_photo_subculture_appearance_boundary_history as appearance_tests
from tests import test_photo_uniform_metadata_boundary_history as v13_tests
from tests import test_photo_vocaloid_metadata_boundary_history as v12_tests


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/subculture-illustration-image-generator")
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts/validate_illustration_assets.py"
EVIDENCE = "docs/research-evidence/photo-prompt/"
LIVE_VALIDATOR = v6_tests.validator

# Exact original containers and member files, not reconstructed archives.
# Total payload: 492,146 bytes. GitSnapshot also authenticates commit/tree/blob
# identity and regular-file mode, with replacement and network fetch disabled.
ARCHIVAL_FIXTURES = {
    EVIDENCE + "retrieval-runtime-improvement-20261003/photo-boundary-after-pack.json": (
        "63d85d810cbdbec91aa7bfab800bbf97474d3ad3", 202126,
        "dd334295c9d95d2f9693ef41aa88b287e7fdc0e01fe0cf92bf22ef59adf9b026"),
    EVIDENCE + "camera-evidence-structure-20261003/independent-v9-boundary-diagnostics.tar.gz": (
        "88d7624b3fea39954ad556365757f826ae6543cd", 86361,
        "a6a5ea23eab5965292cff5b83ae499794a3cbe12eaa442096f8921308f24cc32"),
    EVIDENCE + "camera-evidence-structure-20261003/independent-v9-boundary-verification.json": (
        "7603af56b47c01eb227316b81617156f8a6d1b33", 1533,
        "e33f840476ea7fc4e04c12b104619303697a26aa1610e8f2929f379ebb359db3"),
    EVIDENCE + "camera-evidence-structure-20261003/pr-review-followup/latest-qualified-boundary-pack.json": (
        "14df2f4060dac35b91b6fa4063b2c251ed4c41c6", 202126,
        "6c097471705589a4db45daf5aa164017f2c7b512dcaab880e9e58bb3882f5589"),
}


def setUpModule():
    global FIXTURE_TEMPORARY, FIXTURE_ROOT, COPIED_VALIDATOR
    snapshot = history.GitSnapshot(ROOT, history.PIN, history.TREE)
    authenticated = {}
    for name, (blob, size, sha256) in ARCHIVAL_FIXTURES.items():
        entry = snapshot.entry(name)
        if entry["git_blob"] != blob or entry["mode"] != "100644":
            raise AssertionError("Compatibility fixture identity/mode drift: " + name)
        raw = snapshot.payload(name, sha256=sha256)
        if len(raw) != size:
            raise AssertionError("Compatibility fixture size drift: " + name)
        authenticated[name] = raw
    if sum(map(len, authenticated.values())) != 492146:
        raise AssertionError("Compatibility fixture closure size drift")

    FIXTURE_TEMPORARY = tempfile.TemporaryDirectory(prefix="photo-v36-compatibility-")
    unittest.addModuleCleanup(FIXTURE_TEMPORARY.cleanup)
    FIXTURE_ROOT = Path(FIXTURE_TEMPORARY.name)

    def copy_current(name):
        source, target = ROOT / name, FIXTURE_ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if target.read_bytes() != source.read_bytes():
            raise AssertionError("Compatibility fixture copy drift: " + str(name))

    # Copy only the fixture closure consumed by the original tests. No photo
    # runtime, source DATA, or environment gate is altered or materialized.
    for path in (ROOT / ASSETS).glob("photo_regression_baseline_v*.json"):
        copy_current(path.relative_to(ROOT))
    copy_current(ASSETS / "universal_scene_baseline_v1.json")
    baseline = json.loads((ROOT / ASSETS / "photo_regression_baseline_v6.json").read_bytes())
    for name in baseline["frozen_inputs"]:
        copy_current(name)
    for name in (
        EVIDENCE + "camera-evidence-structure-20261003/pr-review-followup/V11-four-leaf-proof.json",
        EVIDENCE + "vocaloid-appearance-integration-20261004/main-merge/V12-FOUR-LEAF-PROOF.json",
        EVIDENCE + "uniform-costume-integration-20261004/main-merge/V13-FOUR-LEAF-PROOF.json",
    ):
        copy_current(name)
    for name, raw in authenticated.items():
        target = FIXTURE_ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(0o644)
    observation = authenticated[EVIDENCE + "retrieval-runtime-improvement-20261003/photo-boundary-after-pack.json"]
    if hashlib.sha256(observation).hexdigest() != baseline["sha256"]:
        raise AssertionError("Compatibility V6 observation does not match its descriptor")

    # The copied script is byte-identical to the amended implementation. Its
    # real __file__ gives legacy checks the temporary fixture root naturally.
    copy_current(VALIDATOR)
    spec = importlib.util.spec_from_file_location("photo_v36_compatibility_validator", FIXTURE_ROOT / VALIDATOR)
    COPIED_VALIDATOR = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = COPIED_VALIDATOR
    unittest.addModuleCleanup(sys.modules.pop, spec.name, None)
    spec.loader.exec_module(COPIED_VALIDATOR)


class _CopiedLegacyFixtures:
    """Change fixture delivery only; inherit the original test bodies intact."""

    def setUp(self):
        module = self.fixture_module
        self.enterContext(mock.patch.object(module, "validator", COPIED_VALIDATOR))
        self.enterContext(mock.patch.object(module, "ROOT", FIXTURE_ROOT))
        for name in ("SKILL", "ILLUSTRATION"):
            if hasattr(module, name):
                self.enterContext(mock.patch.object(module, name, FIXTURE_ROOT / SKILL))
        if hasattr(module, "OBSERVATION"):
            name = EVIDENCE + "retrieval-runtime-improvement-20261003/photo-boundary-after-pack.json"
            self.enterContext(mock.patch.object(module, "OBSERVATION", FIXTURE_ROOT / name))
        loader = self.enterContext(mock.patch.object(
            COPIED_VALIDATOR, "_camera_v36_support",
            side_effect=AssertionError("Copied legacy fixtures must not load V36 support"),
        ))
        self.addCleanup(loader.assert_not_called)
        super().setUp()
        if hasattr(self, "assets"):
            # The original glob copies V36 too: this is the reported regression.
            self.assertTrue((self.assets / "photo_regression_baseline_v36.json").is_file())
            self.assertNotEqual(self.assets.resolve(), (FIXTURE_ROOT / ASSETS).resolve())


class CopiedV6Tests(_CopiedLegacyFixtures, v6_tests.PhotoCurrentBoundarySnapshotTests):
    fixture_module = v6_tests


class CopiedV10Tests(_CopiedLegacyFixtures, metadata_tests.NapeMetadataBoundaryHistoryTests):
    fixture_module = metadata_tests


class CopiedV11Tests(_CopiedLegacyFixtures, v11_tests.LatestMetadataBoundaryHistoryTests):
    fixture_module = metadata_tests


class CopiedV12Tests(_CopiedLegacyFixtures, v12_tests.VocaloidMetadataBoundaryHistoryTests):
    fixture_module = metadata_tests


class CopiedV13Tests(_CopiedLegacyFixtures, v13_tests.UniformMetadataBoundaryHistoryTests):
    fixture_module = metadata_tests


class CopiedReligionTests(_CopiedLegacyFixtures, religion_tests.ReligionIconographyBoundaryHistoryTests):
    fixture_module = religion_tests


class CopiedSlangTests(_CopiedLegacyFixtures, slang_tests.SlangBoundaryHistoryTests):
    fixture_module = slang_tests


class CopiedAppearanceTests(_CopiedLegacyFixtures, appearance_tests.AppearanceBoundaryHistoryTests):
    fixture_module = appearance_tests


class PublicEntryCompatibilityTests(unittest.TestCase):
    def test_explicit_v36_wrong_root_fails_before_loading_support(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            shutil.copyfile(ROOT / ASSETS / "photo_regression_baseline_v36.json",
                            assets / "photo_regression_baseline_v36.json")
            with mock.patch.object(LIVE_VALIDATOR, "_camera_v36_support") as loader:
                with self.assertRaisesRegex(LIVE_VALIDATOR.ValidationFailure, "asset directory mismatch"):
                    LIVE_VALIDATOR.validate_photo_regression_baseline(assets, baseline_version=36)
                loader.assert_not_called()

    def test_canonical_current_and_historical_calls_keep_successor_dispatch(self):
        # A routing sentinel is not a qualification or a fabricated PASS result.
        for version in (None, 36, 6, 10, 11, 12, 13, 35):
            with self.subTest(version=version):
                sentinel = object()
                support = SimpleNamespace(dispatch=mock.Mock(return_value=sentinel))
                with mock.patch.object(LIVE_VALIDATOR, "_camera_v36_support", return_value=support) as loader:
                    result = LIVE_VALIDATOR.validate_photo_regression_baseline(
                        ROOT / ASSETS, baseline_version=version)
                self.assertIs(result, sentinel)
                loader.assert_called_once_with(ROOT)
                support.dispatch.assert_called_once_with(
                    ROOT / ASSETS, source_root=ROOT, baseline_version=version)

    def controlled_failures(self):
        return (
            (None, "loader", AssertionError("controlled V36 source/proof rejection")),
            (36, "dispatch", AssertionError("V36 exact runtime environment unavailable")),
            (36, "dispatch", ValueError("controlled V36 malformed proof")),
            (6, "dispatch", history.HistoricalReplayUnavailable(
                "Exact V35 Python/Unicode environment unavailable: controlled fixture")),
        )

    @contextlib.contextmanager
    def failing_support(self, stage, failure):
        support = SimpleNamespace(dispatch=mock.Mock(side_effect=failure))
        options = {"side_effect": failure} if stage == "loader" else {"return_value": support}
        with mock.patch.object(LIVE_VALIDATOR, "_camera_v36_support", **options):
            yield

    def test_successor_failures_use_public_validation_failure_and_preserve_cause(self):
        for version, stage, failure in self.controlled_failures():
            with self.subTest(version=version, stage=stage, failure=type(failure).__name__):
                with self.failing_support(stage, failure):
                    with self.assertRaises(LIVE_VALIDATOR.ValidationFailure) as caught:
                        LIVE_VALIDATOR.validate_photo_regression_baseline(
                            ROOT / ASSETS, baseline_version=version)
                self.assertEqual(str(caught.exception), str(failure))
                self.assertIs(caught.exception.__cause__, failure)

    def test_actual_cli_main_reports_successor_failures_as_normal_failure_json(self):
        # Exercise real parse_args/main and the real public photo entry, while
        # isolating unrelated illustration validation and expensive replay.
        for version, stage, failure in self.controlled_failures():
            with self.subTest(version=version, stage=stage, failure=type(failure).__name__):
                def photo_only(asset_dir, *, verify_local_images):
                    self.assertIsNone(asset_dir)
                    self.assertFalse(verify_local_images)
                    return LIVE_VALIDATOR.validate_photo_regression_baseline(
                        ROOT / ASSETS, baseline_version=version)

                stdout, stderr = io.StringIO(), io.StringIO()
                with self.failing_support(stage, failure), \
                     mock.patch.object(LIVE_VALIDATOR, "validate_all", side_effect=photo_only) as validate_all, \
                     mock.patch.object(sys, "argv", [str(ROOT / VALIDATOR)]), \
                     contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    returncode = LIVE_VALIDATOR.main()
                validate_all.assert_called_once_with(None, verify_local_images=False)
                self.assertEqual(returncode, 1)
                self.assertEqual(json.loads(stdout.getvalue()), {"status": "fail", "error": str(failure)})
                self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
