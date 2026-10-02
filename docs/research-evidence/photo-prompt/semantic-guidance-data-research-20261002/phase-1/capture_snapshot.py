"""Capture the current research baseline without changing skill data or indexes."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
PROFILE_IDS = [
    "aircraft_pilot_operation", "one_piece_dress_construction",
    "embodied_corruption_transition", "kuudere_composed_warmth_relation",
    "pfe_cowl", "clothing_ct037_v1", "pfe_one_shoulder", "pfe_ruching",
    "sheer_garment_optical_layering", "clothing_ct090_v2", "clothing_ct023_v2",
    "split_diopter_dual_focus_planes", "film_halation_highlight_edge_relation",
    "broad_face_light_orientation_relation", "short_face_light_orientation_relation",
]


def main():
    assert Path.cwd().resolve() == ROOT
    skill = ROOT / "skills/photo-prompt-image-generator"
    sys.path.insert(0, str(skill / "scripts"))
    import prompt_generator as pg
    loaded = pg.load_visual_obligation_registry(skill / "assets/photo_prompt_visual_obligations.json")["profiles"]
    by_id = {p["id"]: p for p in loaded}
    owners = {}
    for path in sorted((skill / "assets").glob("photo_prompt_visual_obligations*.json")):
        for profile in json.loads(path.read_text()).get("profiles", []):
            if profile["id"] in PROFILE_IDS:
                assert profile["id"] not in owners
                owners[profile["id"]] = path.relative_to(ROOT).as_posix()
    assert set(PROFILE_IDS) == set(owners)
    tracked = subprocess.check_output(["git", "ls-files", "-z", "--", "skills"], cwd=ROOT).decode().split("\0")
    files = []
    for name in sorted(x for x in tracked if x):
        data = (ROOT / name).read_bytes()
        files.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    snapshot = {
        "schema_version": 1,
        "captured_at_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "loaded_profile_count": len(loaded),
        "grain": "one loaded visual-obligation profile",
        "profiles": [{"source_file": owners[ident], "profile": by_id[ident]} for ident in PROFILE_IDS],
        "protected_skill_files": files,
        "limitations": [
            "This is a source snapshot, not a retrieval, model-knowledge, moderation, or image evaluation.",
            "The selected 15 profiles are the agreed research targets rather than a representative quality sample.",
        ],
    }
    (OUT / "source-snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"head": snapshot["head"], "loaded_profiles": len(loaded), "selected_profiles": len(PROFILE_IDS), "protected_skill_files": len(files)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
