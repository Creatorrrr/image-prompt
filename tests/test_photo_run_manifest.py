"""Independent manifests must represent both reference and text-only attempts."""

import hashlib
import json
import subprocess
import sys
import tempfile
import copy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDER = ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"


class PhotoRunManifestTests(unittest.TestCase):
    def run_recorder(self, directory, version="v10", status="success", extra=(), omit=()):
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
        values["--authorial-core-sha256"] = "b" * 64
        values["--intent-lock-sha256"] = "c" * 64
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
        for version in ("v10",):
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


    def test_current_emitted_versions_and_enums_match_the_public_schema(self):
        schema = json.loads((RECORDER.parent.parent / "assets/run_ledger.schema.json").read_bytes())
        for status in ("success", "safety_block", "error"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                result = self.run_recorder(directory, status=status)
                self.assertEqual(result.returncode, 0, result.stderr)
                row = json.loads((Path(directory) / "ledger.ndjson").read_text())
                manifest = json.loads((Path(directory) / "manifest.json").read_text())
                self.assertEqual(row["candidate_pack_version"], "v10")
                self.assertEqual(manifest["candidate_pack_version"], row["candidate_pack_version"])
                self.assertEqual(manifest["contract_version"], "photo-independent-run-manifest/v2")
                self.assertFalse(set(row) - set(schema["properties"]))
                for key, value in row.items():
                    choices = schema["properties"][key].get("enum")
                    if choices is not None:
                        self.assertIn(value, choices, key)

    def test_old_or_unknown_versions_cannot_create_new_records(self):
        for version in ("v2", "v6", "v9", "v11"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                result = self.run_recorder(directory, version=version, status="safety_block")
                self.assertEqual(result.returncode, 2)
                self.assertFalse((Path(directory) / "ledger.ndjson").exists())
                self.assertFalse((Path(directory) / "manifest.json").exists())

    def test_appending_current_record_preserves_historical_row_bytes(self):
        schema = json.loads((RECORDER.parent.parent / "assets/run_ledger.schema.json").read_bytes())
        for version in ("v2", "v3", "v4", "v5", "v6", "v9"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                old = (json.dumps({"ts": "2026-09-01T00:00:00Z", "run_id": "a" * 16,
                                  "prompt_id": "b" * 16, "prompt_en": "An older preserved photograph.",
                                  "attempt": 1, "status": "safety_block", "candidate_pack_version": version},
                                  separators=(",", ":")) + "\n").encode()
                ledger = Path(directory) / "ledger.ndjson"
                ledger.write_bytes(old)
                result = self.run_recorder(directory, status="safety_block")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(ledger.read_bytes().startswith(old))
                rows = ledger.read_bytes().splitlines()
                self.assertEqual(len(rows), 2)
                self.assertEqual(json.loads(rows[1])["candidate_pack_version"], "v10")
                self.assertIn(version, schema["properties"]["candidate_pack_version"]["enum"])

    def test_direct_builders_reject_obsolete_or_conflicting_versions(self):
        import sys
        sys.path.insert(0, str(RECORDER.parent))
        import record_image_run as recorder
        args = recorder.parse_args(["--ts", "2026-10-20T00:00:00Z", "--prompt-en", "A copper bell.",
                                    "--attempt", "1", "--status", "safety_block",
                                    "--candidate-pack-version", "v10", "--arm-id", "one",
                                    "--worktree-id", "isolated", "--skill-sha256", "a" * 64,
                                    "--source-ref", "frozen", "--image-call-count", "1",
                                    "--authorial-core-sha256", "b" * 64, "--intent-lock-sha256", "c" * 64,
                                    "--independent-no-cross-arm-inputs"])
        entry = recorder.build_entry(args)
        obsolete = copy.copy(args)
        obsolete.candidate_pack_version = "v9"
        with self.assertRaisesRegex(ValueError, "new records require"):
            recorder.build_entry(obsolete)
        with self.assertRaisesRegex(ValueError, "independent manifests require"):
            recorder.build_independent_manifest(entry, obsolete)
        changed = dict(entry, candidate_pack_version="v9")
        with self.assertRaisesRegex(ValueError, "differs from its ledger entry"):
            recorder.build_independent_manifest(changed, args)


if __name__ == "__main__":
    unittest.main()
