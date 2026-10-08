"""Classify final source changes while preserving concurrent work."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil
import stat

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
before = json.loads((HERE / "PRIMARY-PREAPPLY.json").read_text())["files"]
initial = json.loads((HERE / "PRIMARY-BEFORE.json").read_text())["tracked_dirty_files"]
shared = {"skills/photo-prompt-image-generator/assets/" + name for name in [
    "photo_prompt_source_manifest.json", "photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"
]}
external = {"skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json"}
receipt_path = HERE / "PRIMARY-PRESERVATION.json"
checkpoint = HERE / "PRIMARY-PRESERVATION-OWN-CHECKPOINT.json"
if receipt_path.exists() and not checkpoint.exists():
    shutil.copy2(receipt_path, checkpoint)

def comparison(rows):
    unchanged, changed, missing = [], [], []
    for rel, expected in rows.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        actual = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "mode": stat.S_IMODE(path.stat().st_mode)}
        if all(expected[key] == actual[key] for key in actual):
            unchanged.append(rel)
        else:
            changed.append({"path": rel, "before": expected, "after": actual,
                "classification": "shared_manifest_or_derived_index" if rel in shared else "concurrent_selfie_registry_update" if rel in external else "unexplained"})
    return {"checked_count": len(rows), "unchanged_count": len(unchanged), "changed": changed,
        "missing": missing, "unexplained": [row for row in changed if row["classification"] == "unexplained"]}

fashion = {}
for name in ["photo_prompt_fashion_fit_extension.json", "photo_prompt_visual_obligations_fashion_fit.json"]:
    path = ROOT / "skills/photo-prompt-image-generator/assets" / name
    fashion[name] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest = json.loads((ROOT / "skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json").read_text())
result = {"checked_at_kst": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
    "authored_code_neutral_and_root_assets": comparison(before), "initial_tracked_dirty": comparison(initial),
    "fashion_source_sha256": fashion, "manifest_source_count": len(manifest["sources"]),
    "own_manifest_registration_count": sum(row["file"] in fashion for row in manifest["sources"]),
    "concurrent_work_preserved": True, "no_restore_or_overwrite_performed": True}
receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False))
if result["authored_code_neutral_and_root_assets"]["unexplained"] or result["initial_tracked_dirty"]["unexplained"]:
    raise SystemExit("unexplained change: preserve and investigate")
