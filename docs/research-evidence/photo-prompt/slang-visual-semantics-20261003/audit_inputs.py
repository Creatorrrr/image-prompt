"""Read live corpus without changing authored assets or generated indexes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import unicodedata

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg

def write(name, payload):
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())

corpus = pg.load_runtime_data(ASSETS / "photo_prompt_tags.json")
registry = corpus[pg.VISUAL_OBLIGATIONS_DATA_KEY]
index = corpus[pg.VISUAL_PROFILE_INDEX_DATA_KEY]
profile_paths = [ASSETS / "photo_prompt_visual_obligations.json"] + [
    ASSETS / name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES
]
candidate_paths = [ASSETS / "photo_prompt_tags.json"] + [
    ASSETS / name for name in pg.RESEARCH_EXTENSION_FILENAMES
]
profile_owners = {}
candidate_owners = {}
for path in profile_paths:
    if path.exists():
        for profile in json.loads(path.read_text()).get("profiles", []):
            profile_owners[profile["id"]] = str(path.relative_to(ROOT))
for path in candidate_paths:
    if path.exists():
        payload = json.loads(path.read_text())
        for slot, entries in payload.get("slots", {}).items():
            for entry in entries:
                candidate_owners[(slot, entry["id"])] = str(path.relative_to(ROOT))
profiles = {p["id"]: p for p in registry["profiles"]}
selected_profile_ids = {
    "composite_overwhelmed_expression", "pv_profile_double_v", "pv_profile_v_sign",
    "pv_profile_chair_straddle", "pv_profile_supine", "pv_profile_prone",
    "soft_full_figure_volume", "bust_prominence_relation",
    "bm_abdominal_projection", "bm_gluteal_projection", "bm_breast_asymmetry",
    "bm_breast_root_width", "bm_breast_fullness", "bm_breast_spacing",
    "bm_eye_aperture", "ne_regional_soft_volume", "ne_regional_contour_transition",
    "ne_current_lip_protrusion",
}
selected_candidate_ids = {
    "pv_double_v", "pv_v_sign", "pv_half_lidded", "pv_parted_lips",
    "ae_slack_jaw", "ae_deadpan_form", "pv_wide_stance", "pv_chair_straddle",
    "bm_abdominal_projection", "bm_gluteal_projection", "bm_breast_asymmetry",
    "bm_breast_root_width", "bm_breast_fullness", "bm_breast_spacing",
    "ne_regional_soft_volume", "ne_regional_contour_transition",
    "ctx_c151",
}
selected_candidates = []
all_candidates = {}
for slot, entries in corpus["slots"].items():
    for entry in entries:
        all_candidates[entry["id"]] = {"slot": slot, "owner_file": candidate_owners.get((slot, entry["id"])), **entry}
        if entry["id"] in selected_candidate_ids:
            selected_candidates.append(all_candidates[entry["id"]])
literal_aliases = {}
for profile in profiles.values():
    activation = profile.get("activation", {})
    for term in activation.get("exact_terms", []) + activation.get("project_glossary_aliases", []):
        literal_aliases.setdefault(norm(term), []).append(profile["id"])
inventory = json.loads((OUT / "TERM-INVENTORY.json").read_text())
literal_probes = [{"term_id": item["id"], "term": item["term"],
    "literal_exact_alias_owners": literal_aliases.get(norm(item["term"]), []),
    "not_a_contextual_activation_test": True} for item in inventory["spellings"]]
requests = [
    "성인 배우의 아헤가오 표정", "an adult actor with an ahegao expression",
    "성인 배우의 우스운 멍한 표정", "성인 배우의 토로가오 표정",
    "성인 배우의 아헤가오 더블피스", "성인 배우의 하트동공",
    "성인 모델의 M자개각 자세", "성인 모델이 대자로 누운 자세",
    "성인 모델의 육덕진 체형", "성인 모델의 보테배",
    "성인 모델의 슴부격차", "성인 모델의 인몬",
    "an adult model in a chair-straddle pose",
    "an adult actor holding a double V-sign",
    "an adult model with a soft full figure",
    "an adult model with half-lidded eyes",
    "fresh melons and bread buns on a table", "an Arsenal gooner in a football scarf",
    "a bubble-tea drink called booba", "a doable assignment and a dong currency note",
    "a bazooka weapon on a display stand", "성인 배우, 아헤가오 표정 제외",
]
context_probes = []
for request in requests:
    polarity = "excluded" if request.endswith("표정 제외") else "included"
    result = pg.resolve_visual_profile_hits(
        registry, [{"source": "user_requirement", "polarity": polarity, "text": request}],
        visual_profile_index=index, adult_context=True)
    context_probes.append({"request": request, "supplied_polarity": polarity,
        "hits": [{key: hit.get(key) for key in (
            "profile_id", "match_basis", "applicability_status", "hard_eligible", "optional_eligible"
        )} for hit in result["hits"]]})
paths = set(profile_paths + candidate_paths + [
    ASSETS / "photo_prompt_visual_profile_index.json",
    ASSETS / "photo_prompt_semantic_index.json",
    SKILL / "scripts/prompt_generator.py",
    SKILL / "scripts/photo_candidate_semantics.py",
    SKILL / "scripts/photo_contracts.py",
])
paths.update(ASSETS.rglob("*.json"))
paths.update((SKILL / "scripts").glob("*.py"))
files = [{"path": str(path.relative_to(ROOT)),
    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
    for path in sorted(paths) if path.exists()]
write("INPUT-RECEIPT.json", {
    "schema_version": "slang-research-input-receipt/v1", "checked_on": "2026-10-03",
    "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
    "git_status_at_audit": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
    "files": files, "writes_outside_this_research_directory": False,
})
write("CURRENT-DATA-AUDIT.json", {
    "schema_version": "slang-current-data-audit/v1", "checked_on": "2026-10-03",
    "loader_status": "PASS", "profile_count": len(profiles), "slot_count": len(corpus["slots"]),
    "candidate_count": sum(len(entries) for entries in corpus["slots"].values()),
    "registry_sha256": index.get("registry_sha256"),
    "slot_dimensions": corpus["candidate_semantic_policy"]["slot_dimensions"],
    "candidate_limits": {"core_per_slot": pg.CANDIDATE_PACK_CORE_SLOT_LIMIT,
        "support_per_slot": pg.CANDIDATE_PACK_SUPPORT_SLOT_LIMIT,
        "pack_total": pg.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT},
    "selected_profiles": [{"owner_file": profile_owners[p["id"]], **p}
        for p in registry["profiles"] if p["id"] in selected_profile_ids],
    "selected_candidates": selected_candidates,
    "all_profile_ids": list(profiles),
    "all_candidate_scopes": [{"id": entry["id"], "slot": entry["slot"],
        "owner_file": entry["owner_file"], "affected_dimensions": entry.get("affected_dimensions"),
        "affected_properties": entry.get("affected_properties")}
        for entry in all_candidates.values()],
    "literal_alias_probes": literal_probes, "contextual_probes": context_probes,
    "probe_boundary": "Current exact-only resolver diagnostics with synthetic source rows. No new implementation, normalized frozen core, v6 pack adoption, image generation, or pixel qualification.",
    "unresolved_selected_profile_ids": sorted(selected_profile_ids - set(profiles)),
    "unresolved_selected_candidate_ids": sorted(selected_candidate_ids - set(all_candidates)),
})
print(json.dumps({"profile_count": len(profiles), "slot_count": len(corpus["slots"]),
    "candidate_count": sum(len(entries) for entries in corpus["slots"].values()),
    "input_files": len(files), "contextual_probes": len(context_probes),
    "missing_profile_ids": sorted(selected_profile_ids - set(profiles)),
    "missing_candidate_ids": sorted(selected_candidate_ids - set(all_candidates))}))
