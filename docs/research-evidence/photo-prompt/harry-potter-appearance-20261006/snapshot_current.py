#!/usr/bin/env python3
"""Freeze current read-only contracts and source identity for this research."""
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()
if __name__ == "__main__":
    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    paths = sorted(p for p in ASSETS.glob("*.json") if not p.name.startswith(("photo_prompt_semantic_index", "photo_prompt_visual_profile_index")))
    paths += [SKILL / "scripts" / name for name in ("prompt_generator.py", "photo_contracts.py", "photo_candidate_semantics.py", "visual_profile_contracts.py", "build_semantic_index.py", "build_visual_profile_index.py")]
    entries = []
    for path in [ASSETS / "photo_prompt_tags.json", *sorted(ASSETS.glob("photo_prompt*extension*.json"))]:
        data = json.loads(path.read_text())
        for slot, rows in data.get("slots", {}).items():
            for row in rows:
                entries.append({"id": row["id"], "slot": slot, "file": str(path.relative_to(ROOT)), "en": row.get("en", ""), "ko": row.get("ko", "")})
    profile_files = {}
    for path in ASSETS.glob("photo_prompt_visual_obligations*.json"):
        for p in json.loads(path.read_text()).get("profiles", []):
            profile_files[p["id"]] = str(path.relative_to(ROOT))
    profiles = [{"id": p["id"], "file": profile_files.get(p["id"]), "definition": p.get("semantics", {}).get("definition", ""), "activation": p.get("activation", {}), "candidate": p.get("concept_candidate", {})} for p in registry["profiles"]]
    snapshot = {"schema_version": "harry-potter-checkout-snapshot/v1", "date_kst": "2026-10-06", "head": run("git", "rev-parse", "HEAD"), "branch": run("git", "branch", "--show-current"), "status_porcelain": run("git", "status", "--porcelain"), "preservation": "Read only. Existing dirty/untracked work is outside this research. No reset, stash, index rebuild, commit or push.", "current_authored_registry_load": {"status": "PASS", "profiles": len(profiles), "scope": "Current source registry load only; generated indexes, retrieval, candidate packs and renders were not qualified."}, "source_hashes": {str(p.relative_to(ROOT)): sha(p) for p in paths}, "generated_index_hashes": {str(p.relative_to(ROOT)): sha(p) for p in (ASSETS / "photo_prompt_semantic_index.json", ASSETS / "photo_prompt_visual_profile_index.json")}, "candidate_entries": len(entries)}
    (OUT / "CHECKOUT-SNAPSHOT.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    (OUT / "EXISTING-DATA-CATALOG.json").write_text(json.dumps({"status": "READ_ONLY_CURRENT_SOURCE_CATALOG", "profiles": profiles, "candidates": entries}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"head": snapshot["head"], "profiles": len(profiles), "candidate_entries": len(entries), "hashed_source_files": len(paths)}))

