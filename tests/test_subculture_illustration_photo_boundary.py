"""Photo-runtime non-regression boundary for the sibling illustration skill."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION_ROOT = REPO_ROOT / "skills" / "subculture-illustration-image-generator"
HISTORICAL_BASELINE_PATH = ILLUSTRATION_ROOT / "assets" / "photo_regression_baseline_v3.json"
BASELINE_PATH = ILLUSTRATION_ROOT / "assets" / "photo_regression_baseline_v4.json"
BASELINE_REF = "f86abef678c99ee8aad7a98a5ea44a685197d371"
ILLUSTRATION_INTRODUCTION_REF = "66e0cbabe55d33575d9e3384176815af515c76ac"






class SubcultureIllustrationPhotoBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        historical = self.baseline["historical_baseline"]
        self.assertEqual(HISTORICAL_BASELINE_PATH.name, historical["path"])
        self.assertEqual(
            historical["sha256"],
            hashlib.sha256(HISTORICAL_BASELINE_PATH.read_bytes()).hexdigest(),
        )

    def test_frozen_photo_baseline_is_historical_and_not_a_current_adapter(self) -> None:
        self.assertEqual(self.baseline["contract_version"], "photo-candidate-pack/v6")
        self.assertTrue(self.baseline["sha256"])
        self.assertTrue(self.baseline["pack_id"])
        photo_entrypoint = REPO_ROOT / "skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py"
        source = photo_entrypoint.read_text(encoding="utf-8")
        self.assertNotIn("photo_regression_baseline", source)
        self.assertNotIn("resolve_concepts", source)

    def test_illustration_modules_do_not_import_photo_runtime(self) -> None:
        banned_modules = {
            "prompt_generator",
            "generate_photo_prompt",
            "photo_prompt_image_generator",
        }
        script_root = ILLUSTRATION_ROOT / "scripts"
        for path in sorted(script_root.glob("*.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(path))
                imported: set[str] = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported.update(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported.add(node.module)
                roots = {name.split(".")[0].replace("-", "_") for name in imported}
                self.assertTrue(banned_modules.isdisjoint(roots), imported)
                self.assertNotIn("importlib", roots, imported)
                self.assertNotIn("photo-prompt-image-generator", source)
                self.assertNotIn("generate_photo_prompt", source)

    def test_illustration_introduction_did_not_modify_photo_runtime(self) -> None:
        for ref in (BASELINE_REF, ILLUSTRATION_INTRODUCTION_REF):
            object_check = subprocess.run(
                ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            if object_check.returncode != 0:
                self.skipTest(f"boundary git object is unavailable: {ref}")

        protected_paths = [
            "skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json",
            "skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index_shards",
            "skills/photo-prompt-image-generator/scripts",
            "skills/photo-prompt-image-generator/assets/photo_prompt_tags.json",
            "skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json",
        ]
        diff = subprocess.run(
            [
                "git",
                "diff",
                "--exit-code",
                BASELINE_REF,
                ILLUSTRATION_INTRODUCTION_REF,
                "--",
                *protected_paths,
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, diff.returncode, diff.stdout or diff.stderr)


if __name__ == "__main__":
    unittest.main()
