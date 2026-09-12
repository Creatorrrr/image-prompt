"""Read-only authored inventory and exact-match diagnostic; no network or generation."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as g

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assets = SKILL / "assets"
registry = g.load_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json")
targets = {
    "fashion_editorial", "lookbook", "campaign_photo", "posing_editorial",
    "professional_poised", "editorial_quality", "contact_sheet_grid",
    "adult_beauty_model", "fierce_editorial_stare", "poised_standing",
    "contrapposto_weight_shift", "contact_sheet_selection_context",
    "clamshell_dual_source_portrait_light", "sheer_complexion_texture_preservation",
}
selected = []
all_labels = []
files = [assets / "photo_prompt_tags.json", assets / "photo_prompt_visual_obligations.json"]
files += [assets / name for name in g.RESEARCH_EXTENSION_FILENAMES]
files += [assets / name for name in g.VISUAL_OBLIGATION_EXTENSION_FILENAMES]

def walk(x, path, source):
    if isinstance(x, dict):
        if "id" in x:
            all_labels.append((source, path, str(x["id"])))
            if x["id"] in targets:
                selected.append({"file": source, "json_pointer": path,
                    "id": x["id"], "record_sha256": hashlib.sha256(
                    json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
                    ).hexdigest(),
                    "record_excerpt": {k: x[k] for k in ("ko", "en", "tags", "activation", "semantics")
                                       if k in x}})
        for k, v in x.items():
            walk(v, path + "/" + str(k), source)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, path + "/" + str(i), source)

for path in files:
    walk(json.loads(path.read_text()), "", str(path.relative_to(ROOT)))
queries = ["professional model", "agency model", "fashion editorial", "lookbook",
    "campaign", "model digitals", "model test", "print-ready", "contrapposto",
    "콘트라포스토", "contact-sheet selection photograph", "clamshell dual-source portrait light",
    "피팅 모델", "garment-aware posing", "double-page spread", "micro-expression"]
diagnostic = []
for q in queries:
    # Supplying no vector index intentionally limits this to deterministic local profile resolution.
    resolution = g.resolve_visual_profile_hits(registry,
        [{"source": "concept_lock", "text": q, "polarity": "required",
          "priority": "critical", "mandatory": True}], adult_context=True)
    diagnostic.append({"query": q, "exact_hard_profile_ids":
        [x["profile_id"] for x in resolution.get("hits", [])
         if x.get("match_basis") == "exact" and x.get("hard_eligible")]})
payload = {
    "schema_version": "photo-research-repo-audit/v1",
    "captured_at": "2026-09-12",
    "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "main_file_profile_count": len(json.loads((assets / "photo_prompt_visual_obligations.json").read_text())["profiles"]),
    "loaded_profile_count": len(registry["profiles"]),
    "source_files": [{"path":str(f.relative_to(ROOT)), "sha256":sha(f)} for f in files],
    "selected_existing_records": selected,
    "exact_match_diagnostic": diagnostic,
    "limitations": [
        "Exact profile lookup only; this is not candidate-pack exposure or semantic retrieval evaluation.",
        "Absence of an ID or exact match does not prove absence of all semantically similar content.",
        "Generated indexes and runtime files are not changed."
    ]
}
(HERE / "repo-audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"loaded_profiles":len(registry["profiles"]), "selected_records":len(selected),
                  "exact_match_diagnostic":diagnostic}, ensure_ascii=False, indent=2))

