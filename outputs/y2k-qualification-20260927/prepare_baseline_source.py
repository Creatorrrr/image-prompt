"""Prepare a source-isolated pre-Y2K comparison, including subprocesses."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "qualification-source"
DEST = HERE / "baseline-source"
shutil.copytree(SOURCE, DEST, symlinks=True, dirs_exist_ok=True,
                ignore=lambda _path, names: [name for name in names if name in {"__pycache__", "photo_prompt_semantic_index_shards"}])
for relative in ["skills/photo-prompt-image-generator/assets/photo_prompt_tags.json", "skills/photo-prompt-image-generator/scripts/prompt_generator.py"]:
    original = subprocess.run(["git", "show", f"HEAD:{relative}"], cwd=ROOT, check=True, capture_output=True).stdout
    (DEST / relative).write_bytes(original)
relative_assets = Path("skills/photo-prompt-image-generator/assets")
assets = DEST / relative_assets
for name in ["photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"]:
    shutil.copy2(HERE / "index-baseline" / name, assets / name)
index = json.loads((assets / "photo_prompt_semantic_index.json").read_text())
for row in index["shards"]:
    src = ROOT / relative_assets / row["path"]
    assert hashlib.sha256(src.read_bytes()).hexdigest() == row["sha256"]
    target = assets / row["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
manifest = {"source_root": str(DEST), "generator_and_tags": "unchanged clean HEAD bytes", "indexes": "saved pre-Y2K bytes and verified immutable shards", "subprocesses_use_baseline_code": True}
(HERE / "baseline-source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(manifest))
