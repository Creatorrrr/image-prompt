"""Independent manifests must represent both reference and text-only attempts."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDER = ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"


class PhotoRunManifestTests(unittest.TestCase):
    def run_recorder(self, directory, version="v6", status="success", extra=(), omit=()):
        directory = Path(directory)
        values = {
            "--ts": "2026-09-05T12:00:00+09:00",
            "--prompt-en": "A copper bell on a wooden table in window light.",
            "--attempt": "1",
            "--status": status,
            "--tool": "image_gen",
            "--arm-id": "text-only-arm",
            "--worktree-id": "isolated-text-only-environment",
            "--skill-sha256": "a" * 64,
            "--source-ref": "frozen-test-snapshot",
            "--candidate-pack-version": version,
            "--image-call-count": "1",
            "--manifest": str(directory / "manifest.json"),
            "--ledger": str(directory / "ledger.ndjson"),
        }
        if version in {"v5", "v6"}:
            values["--authorial-core-sha256"] = "b" * 64
            values["--intent-lock-sha256"] = "c" * 64
        else:
            values["--authorial-request-sha256"] = "d" * 64
        if status == "success":
            image = directory / "returned-image.png"
            image.write_bytes(b"delivered image fixture")
            values["--image-path"] = str(image)
        else:
            values["--failure-reason"] = "tool reported a blocked output"
        argv = [sys.executable, str(RECORDER)]
        for flag, value in values.items():
            if flag not in omit:
                argv.extend([flag, value])
        argv.append("--independent-no-cross-arm-inputs")
        argv.extend(extra)
        return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)

    def test_text_only_success_and_blocked_attempts_write_one_manifest_and_ledger_row(self):
        for version in ("v4", "v5", "v6"):
            for status in ("success", "safety_block"):
                with self.subTest(version=version, status=status), tempfile.TemporaryDirectory() as tmp:
                    result = self.run_recorder(tmp, version=version, status=status)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    manifest = json.loads((Path(tmp) / "manifest.json").read_text())
                    rows = (Path(tmp) / "ledger.ndjson").read_text().splitlines()
                    self.assertEqual(len(rows), 1)
                    row = json.loads(rows[0])
                    self.assertEqual(manifest["ledger_run_id"], row["run_id"])
                    self.assertEqual(manifest["reference_sha256"], [])
                    self.assertEqual(manifest["status"], status)
                    self.assertEqual(manifest["image_call_count"], 1)
                    self.assertFalse(manifest["cross_arm_inputs_used"])
                    if status == "success":
                        self.assertEqual(len(manifest["image_hashes"]), 1)
                        self.assertEqual(manifest["image_hashes"][0]["sha256"], hashlib.sha256(b"delivered image fixture").hexdigest())
                    else:
                        self.assertEqual(manifest["image_paths"], [])
                        self.assertEqual(manifest["image_hashes"], [])

    def test_attached_reference_hashes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_recorder(tmp, extra=("--reference-sha256", "e" * 64))
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((Path(tmp) / "manifest.json").read_text())
            self.assertEqual(manifest["reference_sha256"], ["e" * 64])

    def test_invalid_attached_reference_is_rejected_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_recorder(tmp, extra=("--reference-sha256", "invalid"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("--reference-sha256 must be", result.stderr)
            self.assertFalse((Path(tmp) / "ledger.ndjson").exists())
            self.assertFalse((Path(tmp) / "manifest.json").exists())

    def test_text_only_attempt_still_requires_core_and_source_provenance(self):
        for flag in ("--authorial-core-sha256", "--intent-lock-sha256", "--source-ref"):
            with self.subTest(flag=flag), tempfile.TemporaryDirectory() as tmp:
                result = self.run_recorder(tmp, omit=(flag,))
                self.assertEqual(result.returncode, 2)
                self.assertIn(flag.removeprefix("--").replace("-", "_"), result.stderr)
                self.assertFalse((Path(tmp) / "ledger.ndjson").exists())
                self.assertFalse((Path(tmp) / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
