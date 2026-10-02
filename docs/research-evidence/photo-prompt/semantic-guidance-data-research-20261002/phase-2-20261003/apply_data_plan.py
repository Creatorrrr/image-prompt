"""Apply the authorized data plan using a private assets copy and guarded install."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from build_plan import OUT, ROOT, draft_after, read, sha

SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
STAGE = ROOT / "tmp/semantic-guidance-apply-20261003"
EVIDENCE = OUT / "implementation"

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name, value):
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def prepare():
    if STAGE.exists(): raise SystemExit("Private stage already exists; inspect it before resuming.")
    snapshot = read("current-snapshot.json")
    drift = [name for name, expected in snapshot["protected_file_sha256"].items() if digest(ROOT / name) != expected]
    if drift: raise SystemExit("Research baseline drift: " + ", ".join(drift))
    stage_assets = STAGE / "assets"
    stage_assets.mkdir(parents=True)
    copied = []
    for path in sorted(ASSETS.glob("*.json")):
        shutil.copy2(path, stage_assets / path.name); copied.append(path)
    manifest = json.loads((ASSETS / "photo_prompt_semantic_index.json").read_text())
    for row in manifest["shards"]:
        source = ASSETS / row["path"]
        target = stage_assets / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target); copied.append(source)
    target_files = {}
    plans = read("profile-change-plan.json")["plans"]
    for plan in plans:
        path = ROOT / plan["source_file"]
        assert digest(path) == plan["source_file_sha256"]
        data = target_files.setdefault(path.name, json.loads(path.read_text()))
        index = next(i for i, row in enumerate(data["profiles"]) if row["id"] == plan["profile_id"])
        raw = data["profiles"][index]
        assert sha(raw) == plan["before_raw_profile_sha256"]
        updated = draft_after(raw, plan["operations"])
        assert sha(updated) == plan["after_raw_profile_sha256"]
        data["profiles"][index] = updated
    graph_plan = read("character-scope-plan.json")
    graph_source = ROOT / graph_plan["source_file"]
    assert digest(graph_source) == graph_plan["source_file_sha256"]
    graph = json.loads(graph_source.read_text())
    rows = graph["character_mechanism_graph"]["concept_profiles"]
    index = next(i for i, row in enumerate(rows) if row["id"] == "kuudere")
    assert sha(rows[index]) == graph_plan["before_sha256"]
    rows[index] = draft_after(rows[index], graph_plan["operations"])
    assert sha(rows[index]) == graph_plan["after_sha256"]
    target_files[graph_source.name] = graph
    install_names = sorted([*target_files, "photo_prompt_visual_profile_index.json", "photo_prompt_semantic_index.json"])
    for name in install_names:
        target = STAGE / "before/assets" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ASSETS / name, target)
    for name, data in target_files.items():
        (stage_assets / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    save("baseline.json", {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "protected_file_sha256": snapshot["protected_file_sha256"],
        "copied_asset_sha256": {str(p.relative_to(ROOT)): digest(p) for p in copied},
        "install_names": install_names, "profile_ids": [p["profile_id"] for p in plans],
        "graph_record_id": "kuudere", "stage": str(STAGE.relative_to(ROOT)),
        "status": "PRIVATE_DATA_STAGE_PREPARED",
    })
    print(json.dumps({"copied_assets": len(copied), "data_files_changed_in_private_stage": len(target_files), "profile_records": len(plans), "graph_records": 1}))

def install():
    baseline = json.loads((EVIDENCE / "baseline.json").read_text())
    # Refuse to overwrite any source that changed while indexes were building.
    for relative, expected in baseline["protected_file_sha256"].items():
        if digest(ROOT / relative) != expected: raise SystemExit("Source changed during staged build: " + relative)
    stage_assets = STAGE / "assets"
    sys.path.insert(0, str(SKILL / "scripts"))
    import prompt_generator as pg
    reg = pg.load_visual_obligation_registry(stage_assets / "photo_prompt_visual_obligations.json")
    pg.load_visual_profile_index(stage_assets / "photo_prompt_visual_profile_index.json", reg)
    data = pg.load_json(stage_assets / "photo_prompt_tags.json")
    semantic = pg.load_semantic_index_payload(stage_assets / "photo_prompt_semantic_index.json")
    pg.validate_semantic_index_metadata(semantic, data)
    manifest = json.loads((stage_assets / "photo_prompt_semantic_index.json").read_text())
    added = []
    for row in manifest["shards"]:
        source = stage_assets / row["path"]
        assert digest(source) == row["sha256"]
        target = ASSETS / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if digest(target) != row["sha256"]: raise SystemExit("Existing shard conflict: " + row["path"])
        else:
            shutil.copy2(source, target); added.append(str(target.relative_to(ROOT)))
    # New immutable shards precede manifest publication; original generations stay intact.
    installed = []
    for name in baseline["install_names"]:
        source, target = stage_assets / name, ASSETS / name
        temp = target.with_name(target.name + ".semantic-guidance.tmp")
        if temp.exists(): raise SystemExit("Unexpected install temporary file: " + name)
        shutil.copy2(source, temp); temp.replace(target)
        installed.append({"path": str(target.relative_to(ROOT)), "before_sha256": digest(STAGE / "before/assets" / name), "after_sha256": digest(target)})
    save("install-receipt.json", {"installed_at": datetime.now(timezone.utc).isoformat(), "status": "APPLIED_PENDING_RUNTIME_CHECKS", "files": installed, "new_shards": added, "profile_count": len(reg["profiles"]), "semantic_entries": manifest["entry_count"], "old_shards_deleted": 0, "skill_logic_changed": False})
    print(json.dumps({"installed_files": len(installed), "new_shards": len(added), "loaded_profiles": len(reg["profiles"]), "semantic_entries": manifest["entry_count"]}))

def install_repair():
    baseline = json.loads((EVIDENCE / "baseline.json").read_text())
    receipt = json.loads((EVIDENCE / "install-receipt.json").read_text())
    repair = json.loads((EVIDENCE / "repair-plan.json").read_text())
    expected = dict(baseline["protected_file_sha256"])
    expected.update({row["path"]: row["after_sha256"] for row in receipt["files"]})
    test_change = repair["test_adjustment"]
    expected[test_change["path"]] = test_change["after_sha256"]
    for relative, value in expected.items():
        if digest(ROOT / relative) != value: raise SystemExit("Source changed during staged repair: " + relative)
    stage_assets = STAGE / "assets"
    graph_source = ROOT / repair["source_file"]
    assert digest(graph_source) == repair["before_file_sha256"]
    graph = json.loads((stage_assets / graph_source.name).read_text())
    row = next(r for r in graph["character_mechanism_graph"]["concept_profiles"] if r["id"] == "kuudere")
    assert sha(row) == repair["after_record_sha256"]
    sys.path.insert(0, str(SKILL / "scripts"))
    import prompt_generator as pg
    pg.validate_character_mechanism_graph(graph)
    semantic = pg.load_semantic_index_payload(stage_assets / "photo_prompt_semantic_index.json")
    pg.validate_semantic_index_metadata(semantic, pg.load_json(stage_assets / "photo_prompt_tags.json"))
    old_semantic = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
    assert sorted(k for k, v in semantic["entries"].items() if v != old_semantic["entries"][k]) == ["character_response_concept:kuudere"]
    added = []
    for descriptor in semantic["shards"]:
        source, target = stage_assets / descriptor["path"], ASSETS / descriptor["path"]
        assert digest(source) == descriptor["sha256"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if digest(target) != descriptor["sha256"]: raise SystemExit("Existing repair shard conflict")
        else:
            shutil.copy2(source, target); added.append(str(target.relative_to(ROOT)))
    save("initial-install-receipt.json", receipt)
    changes = []
    for name in (graph_source.name, "photo_prompt_semantic_index.json"):
        source, target = stage_assets / name, ASSETS / name
        before = digest(target)
        temp = target.with_name(target.name + ".semantic-guidance.tmp")
        if temp.exists(): raise SystemExit("Unexpected repair temporary file")
        shutil.copy2(source, temp); temp.replace(target)
        relative = str(target.relative_to(ROOT))
        changes.append({"path": relative, "before_sha256": before, "after_sha256": digest(target)})
        next(r for r in receipt["files"] if r["path"] == relative)["after_sha256"] = digest(target)
    receipt["new_shards"].extend(added)
    receipt["test_changes"] = [test_change]
    receipt["repair"] = {"installed_at": datetime.now(timezone.utc).isoformat(), "reason": repair["reason"],
        "files": changes, "new_shards": added, "successful_embedding_items": 1}
    save("install-receipt.json", receipt)
    print(json.dumps({"repaired_data_files": len(changes), "new_shards": len(added), "fixture_files_changed": 0}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "install", "install-repair"])
    args = parser.parse_args()
    {"prepare": prepare, "install": install, "install-repair": install_repair}[args.action]()
