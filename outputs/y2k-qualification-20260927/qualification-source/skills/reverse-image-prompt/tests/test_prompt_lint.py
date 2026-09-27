#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from prompt_lint import audit_standalone_prompt_text
from salience_plan import audit_standalone_prompt_text as salience_prompt_audit


class PromptLintTests(unittest.TestCase):
    def run_cli(self, prompt_path: Path) -> tuple[int, dict]:
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                str(TOOLS / "prompt_lint.py"),
                str(prompt_path),
            ],
            cwd=prompt_path.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=10,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_salience_plan_reexports_shared_audit(self) -> None:
        self.assertIs(salience_prompt_audit, audit_standalone_prompt_text)

    def test_non_string_input_preserves_existing_error(self) -> None:
        self.assertEqual(
            audit_standalone_prompt_text(None),
            ["authored prompt text must be a string"],
        )

    def test_overlapping_references_report_one_error_per_span(self) -> None:
        errors = audit_standalone_prompt_text("Preserve the original composition.")
        self.assertEqual(len(errors), 1)
        self.assertIn("unresolved comparison target", errors[0])

    def test_cli_accepts_self_contained_scene_without_plan_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "prompt text.txt"
            prompt_path.write_text(
                "PROMPT:\nA matte vessel rests on a rough café table. A large soft "
                "light source above viewer-left creates a broad highlight. "
                "Keep the vessel tilted toward viewer-right, preserve the oval "
                "rim, and let its lower half remain outside the frame.\n"
                "NEGATIVE PROMPT:\nCrisp background lettering, polished reflections.",
                encoding="utf-8",
            )
            returncode, payload = self.run_cli(prompt_path)
        self.assertEqual(returncode, 0)
        self.assertEqual(payload, {"status": "ok", "errors": []})

    def test_cli_preserves_narrow_boundary_check_for_empty_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "prompt.txt"
            prompt_path.write_text("", encoding="utf-8")
            returncode, payload = self.run_cli(prompt_path)
        self.assertEqual(returncode, 0)
        self.assertEqual(payload, {"status": "ok", "errors": []})

    def test_cli_rejects_unavailable_evidence_and_provenance(self) -> None:
        cases = (
            ("SOURCE-supported lighting", "internal provenance label"),
            ("Use the attached image.", "unavailable image artifact"),
            ("Match the reference.", "unresolved comparison target"),
            ("The source placement is low.", "unresolved source placeholder"),
            ("The original composition.", "unresolved original-state placeholder"),
            ("Position it as shown in the image.", "deictic image instruction"),
        )
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "prompt.txt"
            for phrase, category in cases:
                with self.subTest(phrase=phrase):
                    prompt_path.write_text(f"PROMPT:\n{phrase}", encoding="utf-8")
                    returncode, payload = self.run_cli(prompt_path)
                    self.assertEqual(returncode, 1)
                    self.assertEqual(payload["status"], "failed")
                    self.assertEqual(len(payload["errors"]), 1)
                    self.assertIn(category, payload["errors"][0])
                    self.assertIn("literal visible target state or relation", payload["errors"][0])

    def test_cli_reports_missing_file_as_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "missing-prompt.txt"
            returncode, payload = self.run_cli(prompt_path)
        self.assertEqual(returncode, 1)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(len(payload["errors"]), 1)
        self.assertIn("cannot read prompt file", payload["errors"][0])
        self.assertIn("missing-prompt.txt", payload["errors"][0])

    def test_cli_reports_non_utf8_file_as_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "invalid-prompt.txt"
            prompt_path.write_bytes(b"PROMPT:\n\xff\xfe")
            returncode, payload = self.run_cli(prompt_path)
        self.assertEqual(returncode, 1)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(len(payload["errors"]), 1)
        self.assertIn("cannot read prompt file", payload["errors"][0])
        self.assertIn("utf-8", payload["errors"][0])


if __name__ == "__main__":
    unittest.main()
