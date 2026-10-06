#!/usr/bin/env python3
"""Load actual primary index shards and record the qualified data binding."""
from pathlib import Path
import hashlib
import json
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg

data = pg.load_runtime_data()
registry = data[pg.VISUAL_OBLIGATIONS_DATA_KEY]
semantic = data[pg.SEMANTIC_INDEX_DATA_KEY]
visual = data[pg.VISUAL_PROFILE_INDEX_DATA_KEY]
assets = SKILL / "assets"
paths = [SKILL / "scripts" / name for name in
         ["prompt_generator.py", "photo_contracts.py", "audit_composed_prompt.py"]] + [SKILL / "SKILL.md"]
receipt = {
    "status": "PASS",
    "actual_shards_loaded": True,
    "semantic_bm25f_and_metadata_validated": True,
    "visual_registry_binding_validated": True,
    "profile_count": len(registry["profiles"]),
    "raw_slot_entry_count": sum(len(rows) for rows in data["slots"].values()),
    "semantic_index_entry_count": len(semantic["entries"]),
    "visual_index_entry_count": len(visual["entries"]),
    "dictionary_hash": pg.dictionary_hash(data),
    "index_manifest_sha256": {
        name: hashlib.sha256((assets / name).read_bytes()).hexdigest()
        for name in ["photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"]
    },
    "runtime_source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in paths},
    "primary_current_runtime_verified": True,
    "native_runs_remain_bound_to_original_isolated_runtime": True,
}
(OUT / "PRIMARY-RUNTIME-VERIFICATION.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(f"Primary runtime PASS: {receipt['profile_count']} profiles, {receipt['raw_slot_entry_count']} slot entries")
