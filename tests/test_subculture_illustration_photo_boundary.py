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
HISTORICAL_BASELINE_PATH = ILLUSTRATION_ROOT / "assets" / "photo_regression_baseline_v1.json"
BASELINE_PATH = ILLUSTRATION_ROOT / "assets" / "photo_regression_baseline_v2.json"
BASELINE_REF = "f86abef678c99ee8aad7a98a5ea44a685197d371"
ILLUSTRATION_INTRODUCTION_REF = "66e0cbabe55d33575d9e3384176815af515c76ac"


def _canonical_photo_pack_id(pack: dict[str, object]) -> str:
    hashable = dict(pack)
    hashable["pack_id"] = None
    encoded = json.dumps(
        hashable,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def _selected_photo_ids(pack: dict[str, object]) -> list[str]:
    presets = pack["presets"]
    slots = pack["slots"]
    assert isinstance(presets, list)
    assert isinstance(slots, dict)
    selected = [str(item["id"]) for item in presets if item.get("selected_by_sampler") is True]
    selected.extend(str(slot["selected"]) for slot in slots.values())
    return selected


class SubcultureIllustrationPhotoBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        historical = self.baseline["historical_baseline"]
        self.assertEqual(HISTORICAL_BASELINE_PATH.name, historical["path"])
        self.assertEqual(
            historical["sha256"],
            hashlib.sha256(HISTORICAL_BASELINE_PATH.read_bytes()).hexdigest(),
        )

    def test_frozen_photo_command_matches_byte_and_pack_contract(self) -> None:
        frozen_command = list(self.baseline["command"])
        output_flag = frozen_command.index("--output-file")
        frozen_output_path = frozen_command[output_flag + 1]

        with tempfile.TemporaryDirectory(prefix="illustration-photo-boundary-") as temp_dir:
            temporary_output = Path(temp_dir) / "photo-candidate-pack.json"
            command = list(frozen_command)
            command[output_flag + 1] = str(temporary_output)
            environment = os.environ.copy()
            environment["GEMINI_API_KEY"] = ""
            environment["GOOGLE_API_KEY"] = ""
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)
            raw = temporary_output.read_bytes()

        payload = json.loads(raw)
        self.assertIsInstance(payload, list)
        self.assertEqual(1, len(payload))
        pack = payload[0]

        # output-file is intentionally part of photo provenance and therefore of
        # pack_id.  Restore the exact frozen argv value before comparing frozen
        # command bytes; all other subprocess output remains untouched.
        provenance_argv = pack["provenance"]["argv"]
        emitted_output_flag = provenance_argv.index("--output-file")
        self.assertEqual(str(temporary_output), provenance_argv[emitted_output_flag + 1])
        provenance_argv[emitted_output_flag + 1] = frozen_output_path
        pack["pack_id"] = _canonical_photo_pack_id(pack)
        normalized_bytes = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

        self.assertEqual(self.baseline["sha256"], hashlib.sha256(normalized_bytes).hexdigest())
        self.assertEqual(self.baseline["pack_id"], pack["pack_id"])
        self.assertEqual(
            self.baseline["sample_prompt_id"],
            pack["provenance"]["sample_prompt_id"],
        )
        self.assertEqual(self.baseline["selected_ids"], _selected_photo_ids(pack))
        self.assertEqual(self.baseline["negative_en"], pack["negative_en"])

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
