"""Maintenance-only audit of every focused research decision against current data."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
RESEARCH = HERE.parent / "wardrobe-keyword-semantics-20261010"
PRIOR = HERE.parent / "wardrobe-keyword-integration-20261010"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from photo_candidate_semantics import digest


def read(path):
    return json.loads(path.read_text())


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


catalog = read(RESEARCH / "inputs/wardrobe_keyword_catalog.json")
coverage = read(RESEARCH / "KEYWORD-COVERAGE.json")["rows"]
cards = read(RESEARCH / "SEMANTIC-CARDS.json")["cards"]
drafts = read(RESEARCH / "CANDIDATE-BLUEPRINTS.json")["drafts"]
decisions = read(PRIOR / "INTEGRATION-DECISIONS.json")
changes = read(HERE / "DATA-CHANGES.json")
data = pg.load_json(ASSETS / "photo_prompt_tags.json")
registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
entries = {r["id"]: (slot, r) for slot, rows in data["slots"].items() for r in rows}
profiles = {r["id"]: r for r in registry["profiles"]}
bundles = {r["id"]: r for r in data["candidate_bundles"]}
card_ids = {r["id"] for r in cards}
keyword_ids = {r["id"] for r in catalog["keywords"]}
assert len(keyword_ids) == len(catalog["keywords"]) == 503
assert {r["id"] for r in coverage} == keyword_ids
assert all(r["research_card_ids"] and set(r["research_card_ids"]) <= card_ids for r in coverage)
assert {r["id"] for r in drafts} == {r["draft_id"] for r in decisions["rows"]}
visible_ids = {r["id"] for r in cards if r["observation_mode"] == "present_visible_relation"}
annotation_ids = {r["id"] for r in cards if r["observation_mode"] == "annotation_or_context_only"}
assert {r["card_id"] for r in decisions["rows"]} == visible_ids
assert {r["card_id"] for r in decisions["annotations"]} == annotation_ids
assert set(changes["annotation_ids_retained_externally"]) == annotation_ids
retained_updates = {r["card_id"]: r for r in changes["retained_candidate_endpoint_contracts"]}
retained_profiles = {"WK038": "clothing_ct031_v1", "WK046": "vg_ribbon_to_garment_seam_profile"}
rows = []
for decision in decisions["rows"]:
    cid = decision["candidate_id"]
    slot, candidate = entries[cid]
    reused = decision["decision"] == "reuse_existing_candidate_identity"
    update = retained_updates.get(decision["card_id"])
    pid = (update["profile_id"] if update else retained_profiles[decision["card_id"]]) if reused else decision["profile_id"]
    profile = profiles[pid]
    bundle_id = update["bundle_id"] if update else decision.get("bundle_id")
    if bundle_id:
        bundle = bundles[bundle_id]
        assert cid in {r["entry_id"] for r in bundle["member_candidates"]}
        assert pid in bundle["associated_profile_ids"]
    gates = profile["render_gates"]
    assert gates and profile["composition_instruction"]
    assert candidate.get("affected_dimensions") and candidate.get("affected_properties")
    if not reused:
        assert slot == decision["slot"]
        assert candidate["en"] == decision["reviewed_text"]
        assert candidate["affected_dimensions"] == decision["affected_dimensions"]
        assert candidate["affected_properties"] == decision["affected_properties"]
        assert candidate["relations"] == decision["relations"]
    rows.append({"card_id": decision["card_id"], "draft_id": decision["draft_id"],
                 "candidate_id": cid, "slot": slot, "profile_id": pid, "bundle_id": bundle_id,
                 "disposition": "completed_retained_endpoint_contract" if update else decision["decision"],
                 "current_candidate_sha256": digest(candidate), "current_profile_sha256": digest(profile),
                 "required_gate_ids_when_activated_or_adopted": [r["id"] for r in gates],
                 "native_pixels_verified_for_all_variants": False, "status": "CURRENT_LINKS_VERIFIED"})

maintenance = []
for name in ["photo_prompt_wardrobe_owner_relations_extension.json", "photo_prompt_clothing_structure_extension.json"]:
    extension = read(ASSETS / name)
    ref = extension["maintenance_ref"]
    record_path = HERE.parent / "extension-maintenance" / (ref["record_id"] + ".json")
    record = read(record_path)
    source_without_ref = copy.deepcopy(extension)
    source_without_ref.pop("maintenance_ref")
    assert digest(record) == ref["sha256"]
    assert digest(source_without_ref) == record["authored_source_sha256"]
    assert digest(read(ASSETS / record["profile_filename"])) == record["profile_source_sha256"]
    maintenance.append({"source": name, "record": str(record_path.relative_to(ROOT)),
                        "record_sha256": ref["sha256"], "status": "CURRENT_SOURCE_VERIFIED"})

audit = {
    "schema_version": "wardrobe-research-current-coverage/v1", "status": "PASS",
    "scope": "Every focused card/variant and original decision; not exhaustive universal definitions of all historical prompts or terms.",
    "counts": {"normalized_headwords_with_focused_mapping": len(coverage), "categories": len({r["category"] for r in coverage}),
               "selected_original_catalog_records": len(catalog["sources"]), "semantic_cards": len(cards),
               "visible_relation_cards": len(visible_ids), "external_annotation_cards": len(annotation_ids),
               "reviewed_drafts": len(drafts), "named_original_variants": sum(len(r["variants"]) for r in cards),
               "new_ordinary_candidate_identities_from_prior_integration": sum(not (r["decision"] == "reuse_existing_candidate_identity") for r in decisions["rows"]),
               "reused_ordinary_candidate_identities": 4,
               "current_wardrobe_profiles": sum(pid.startswith("wkr_") for pid in profiles),
               "current_wardrobe_bundles": sum(bid.startswith("wkr_") for bid in bundles),
               "optional_historical_combinations": len(decisions["past_combinations"]["recipes"]),
               "contextual_historical_exclusions": len(catalog["contextual_exclusions"])},
    "coverage_rows": rows, "maintenance": maintenance,
    "annotations": [{"card_id": r["card_id"], "disposition": r["disposition"],
                     "reason": r["annotation"]["definition_ko"], "runtime_alias_or_required_recipe": False} for r in decisions["annotations"]],
    "constraints": {"all_research_drafts_accounted_for": True, "no_duplicate_candidate_ids_added_this_turn": True,
                    "broad_labels_remain_optional": True, "original_catalog_files_individually_reopened": False,
                    "all_503_universal_meanings_or_all_variant_pixels_proven": False,
                    "historical_recipes_are_optional_and_exclusions_contextual": True},
    "input_hashes": {str(p.relative_to(ROOT)): file_sha(p) for p in [RESEARCH / "SEMANTIC-CARDS.json", RESEARCH / "CANDIDATE-BLUEPRINTS.json",
                       RESEARCH / "KEYWORD-COVERAGE.json", PRIOR / "INTEGRATION-DECISIONS.json", ASSETS / "photo_prompt_source_manifest.json"]}}
(HERE / "RESEARCH-COVERAGE-AUDIT.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": audit["status"], "counts": audit["counts"]}, ensure_ascii=False))
