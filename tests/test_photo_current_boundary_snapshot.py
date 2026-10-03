"""A changed candidate allocation cannot rebaseline the frozen scene."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / "skills/subculture-illustration-image-generator"
sys.path.insert(0, str(ILLUSTRATION / "scripts"))
import validate_illustration_assets as validator

OBSERVATION = ROOT / "docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/photo-boundary-after-pack.json"


class PhotoCurrentBoundarySnapshotTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.assets = Path(self.directory.name)
        for path in (ILLUSTRATION / "assets").glob("photo_regression_baseline_v*.json"):
            shutil.copyfile(path, self.assets / path.name)
        shutil.copyfile(ILLUSTRATION / "assets/universal_scene_baseline_v1.json",
                        self.assets / "universal_scene_baseline_v1.json")
        self.current = self.assets / "photo_regression_baseline_v6.json"
        self.output = OBSERVATION.read_bytes()

    def change(self, apply):
        row = json.loads(self.current.read_text())
        apply(row)
        self.current.write_text(json.dumps(row, indent=2) + "\n")

    def validate(self):
        def generate(command, **kwargs):
            Path(command[command.index("--output-file") + 1]).write_bytes(self.output)
            return SimpleNamespace(returncode=0, stderr="", stdout="")
        with mock.patch.object(validator.subprocess, "run", side_effect=generate):
            # Preserve the upstream V6 observation independently of live V7.
            return validator.validate_photo_regression_baseline(self.assets, baseline_version=6)

    def test_successor_preserves_history_and_the_observed_scene_contract(self):
        self.assertEqual(self.validate()["status"], "pass")
        previous = self.assets / "photo_regression_baseline_v5.json"
        current = json.loads(self.current.read_text())
        self.assertEqual(current["historical_baseline"]["sha256"], hashlib.sha256(previous.read_bytes()).hexdigest())

    def test_modified_predecessor_cannot_be_hidden_by_a_new_output_hash(self):
        previous = self.assets / "photo_regression_baseline_v5.json"
        previous.write_text(previous.read_text() + "\n")
        with self.assertRaisesRegex(validator.ValidationFailure, "current photo baseline lineage"):
            self.validate()

    def test_changed_seed_or_scene_command_is_rejected(self):
        def change(row):
            row["command"][row["command"].index("--seed") + 1] = "910001"
        self.change(change)
        with self.assertRaisesRegex(validator.ValidationFailure, "frozen generation command"):
            self.validate()

    def test_changed_input_bytes_are_rejected(self):
        self.change(lambda row: row["frozen_inputs"].update({next(iter(row["frozen_inputs"])): "0" * 64}))
        with self.assertRaisesRegex(validator.ValidationFailure, "frozen input bytes"):
            self.validate()

    def test_changed_negative_contract_is_rejected(self):
        self.change(lambda row: row.update(negative_en="discard the original negative contract"))
        with self.assertRaisesRegex(validator.ValidationFailure, "preserved public boundary"):
            self.validate()

    def test_recomputed_output_hash_cannot_accept_a_changed_frozen_scene(self):
        pack = json.loads(self.output)
        pack[0]["authorial_core"]["subject"] = "an unrelated replacement subject"
        pack[0]["pack_id"] = validator._canonical_photo_pack_id(pack[0])
        self.output = (json.dumps(pack, indent=2, ensure_ascii=False) + "\n").encode()
        self.change(lambda row: row.update(sha256=hashlib.sha256(self.output).hexdigest(), pack_id=pack[0]["pack_id"]))
        with self.assertRaisesRegex(validator.ValidationFailure, "frozen scene or composition contract"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
