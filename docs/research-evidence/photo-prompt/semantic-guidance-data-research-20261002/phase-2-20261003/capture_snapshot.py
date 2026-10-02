"""Freeze the current authored data and protect unrelated work; no runtime writes."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PHASE1 = OUT.parent / "phase-1"
SKILL = ROOT / "skills/photo-prompt-image-generator"
IDS = [
    "aircraft_pilot_operation", "one_piece_dress_construction",
    "embodied_corruption_transition", "kuudere_composed_warmth_relation",
    "pfe_cowl", "clothing_ct037_v1", "pfe_one_shoulder", "pfe_ruching",
    "sheer_garment_optical_layering", "clothing_ct090_v2", "clothing_ct023_v2",
    "split_diopter_dual_focus_planes", "film_halation_highlight_edge_relation",
    "broad_face_light_orientation_relation", "short_face_light_orientation_relation",
]

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    target = OUT / "current-snapshot.json"
    if target.exists():
        raise SystemExit("Snapshot already exists; never overwrite historical evidence.")
    sys.path.insert(0, str(SKILL / "scripts"))
    import prompt_generator as pg
    profiles = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")["profiles"]
    selected = {row["id"]: row for row in profiles if row["id"] in IDS}
    owners = {}
    for path in sorted((SKILL / "assets").glob("photo_prompt_visual_obligations*.json")):
        data = json.loads(path.read_text())
        for row in data.get("profiles", []):
            if row.get("id") in IDS:
                owners[row["id"]] = {"path": str(path.relative_to(ROOT)), "raw_profile": row}
    paths = set()
    for base in [ROOT / "skills", ROOT / "tests", PHASE1]:
        paths.update(p for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for path in ROOT.glob("**/AGENTS.md"):
        if path.is_file(): paths.add(path)
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}
    snapshot = {
        "schema_version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
        "loaded_profile_count": len(profiles),
        "selected_profile_count": len(selected),
        "selected_profiles": selected,
        "raw_owners": owners,
        "protected_file_sha256": hashes,
        "scope": "Research and unapplied data plan only. Existing dirty and untracked files are protected.",
    }
    assert len(selected) == len(IDS) == len(owners)
    target.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"loaded_profiles": len(profiles), "selected": len(selected), "protected_files": len(hashes)}))

if __name__ == "__main__":
    main()
