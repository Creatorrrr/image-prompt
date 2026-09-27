"""Read-only replay of early full-suite failures against the pre-change data.

Original authored tags come from clean HEAD; saved original indexes retain
their original shards. Only the two Y2K loader registrations are omitted.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
HERE = Path(__file__).resolve().parent
BASE = HERE / "baseline-comparison"
BASE.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as generator

for path in ASSETS.iterdir():
    dest = BASE / path.name
    if path.name not in {"photo_prompt_tags.json", "photo_prompt_visual_profile_index.json", "photo_prompt_semantic_index.json"} and not dest.exists():
        dest.symlink_to(path, target_is_directory=path.is_dir())
original = subprocess.run(["git", "show", "HEAD:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json"], cwd=ROOT, check=True, capture_output=True).stdout
(BASE / "photo_prompt_tags.json").write_bytes(original)
for name in ("photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"):
    (BASE / name).write_bytes((HERE / "index-baseline" / name).read_bytes())

generator.RESEARCH_EXTENSION_FILENAMES = tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES if name != "photo_prompt_y2k_extension.json")
generator.VISUAL_OBLIGATION_EXTENSION_FILENAMES = tuple(name for name in generator.VISUAL_OBLIGATION_EXTENSION_FILENAMES if name != "photo_prompt_visual_obligations_y2k.json")
load_json = generator.load_json
load_semantic = generator.load_semantic_index_payload
load_visual = generator.load_visual_profile_index


def original_path(path):
    path = Path(path)
    if path.name in {"photo_prompt_tags.json", "photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"} and path.resolve().parent == ASSETS.resolve():
        return BASE / path.name
    return path


generator.load_json = lambda path: load_json(original_path(path))
generator.load_semantic_index_payload = lambda path, *args, **kwargs: load_semantic(original_path(path), *args, **kwargs)
generator.load_visual_profile_index = lambda path, *args, **kwargs: load_visual(original_path(path), *args, **kwargs)
suite = unittest.TestLoader().loadTestsFromNames([
    "tests.test_beastkin_improvements",
    "tests.test_golden_snapshots",
    "tests.test_makeup_layer_dictionary",
])
result = unittest.TextTestRunner(verbosity=2).run(suite)
(HERE / "baseline-test-comparison.json").write_text(json.dumps({"tests_run": result.testsRun, "failures": [case.id() for case, _ in result.failures], "errors": [case.id() for case, _ in result.errors], "new_y2k_extensions_loaded": False, "original_tags_source": "clean HEAD", "original_indexes_source": "saved pre-change bytes"}, indent=2) + "\n")
raise SystemExit(not result.wasSuccessful())
