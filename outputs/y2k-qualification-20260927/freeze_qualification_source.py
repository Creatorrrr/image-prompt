"""Reconstruct the ready Y2K-only source without altering shared edits."""
import hashlib
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = HERE / "qualification-source"
READY = json.loads((HERE / "data_ready.json").read_text())
DEST.mkdir(exist_ok=True)
process = subprocess.Popen(["git", "archive", "HEAD", "skills", "tests"], cwd=ROOT, stdout=subprocess.PIPE)
with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
    for member in archive:
        if "/photo_prompt_semantic_index_shards/" in member.name:
            continue
        archive.extract(member, DEST, filter="data")
assert process.wait() == 0
assets_relative = Path("skills/photo-prompt-image-generator/assets")
assets = DEST / assets_relative
live_assets = ROOT / assets_relative
tags_path = assets / "photo_prompt_tags.json"
tags_text = tags_path.read_text()
tags_old = '      "photo_prompt_everyday_scene_extension.json"\n'
assert tags_text.count(tags_old) == 1
tags_text = tags_text.replace(tags_old, '      "photo_prompt_everyday_scene_extension.json",\n      "photo_prompt_y2k_extension.json"\n')
tags_path.write_text(tags_text)
script_path = DEST / "skills/photo-prompt-image-generator/scripts/prompt_generator.py"
code = script_path.read_text()
for last, addition in [
    ('    "photo_prompt_visual_obligations_everyday_scene.json",\n)', '    "photo_prompt_visual_obligations_y2k.json",\n'),
    ('    "photo_prompt_scene_expression_character_moe.json",\n)', '    "photo_prompt_y2k_extension.json",\n'),
]:
    assert code.count(last) == 1
    code = code.replace(last, last[:-1] + addition + ")")
script_path.write_text(code)
for name, expected in READY["source_sha256"].items():
    target = assets / name
    if name != "photo_prompt_tags.json":
        cached = HERE / "ready-source-assets" / name
        source = cached if cached.exists() else live_assets / name
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected, name
        shutil.copy2(source, target)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == expected, name
index = json.loads((assets / "photo_prompt_semantic_index.json").read_text())
for shard in index["shards"]:
    source = live_assets / shard["path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == shard["sha256"]
    target = assets / shard["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
shutil.copy2(ROOT / "tests/test_photo_y2k_visual_semantics.py", DEST / "tests/test_photo_y2k_visual_semantics.py")
for name in ["docs", "artifacts", "outputs", "output", ".venv", ".agents"]:
    target = DEST / name
    if not target.exists():
        target.symlink_to(ROOT / name, target_is_directory=True)
manifest = {
    "purpose": "Isolated qualification source corresponding exactly to the pre-render ready source; shared unrelated edits preserved.",
    "git_base": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(),
    "source_root": str(DEST),
    "ready_source_sha256": READY["source_sha256"],
    "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
    "runtime_sources_are_independent_copies": True,
    "linked_nonruntime_evidence": ["docs", "artifacts", "outputs", "output"],
    "excluded_concurrent_registration": "portrait_composition",
}
(HERE / "qualification-source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"source_root": str(DEST), "source_hashes": "all match ready", "semantic_shards": len(index["shards"])}))
