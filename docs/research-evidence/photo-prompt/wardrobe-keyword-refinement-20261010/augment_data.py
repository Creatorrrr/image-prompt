"""Preserve complete old gates; strengthen discovery/contrast and retained identities."""
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path[:0] = [str(SKILL / "scripts"), str(SKILL / "precore")]
from photo_candidate_semantics import digest
from photo_runtime_sources import source_update


def load(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def unique(values):
    return list(dict.fromkeys(values))


extension_path = ASSETS / "photo_prompt_wardrobe_owner_relations_extension.json"
profiles_path = ASSETS / "photo_prompt_visual_obligations_wardrobe_owner_relations.json"
clothing_path = ASSETS / "photo_prompt_clothing_structure_extension.json"
clothing_profiles_path = ASSETS / "photo_prompt_visual_obligations_clothing_structure.json"
extension, profiles = load(extension_path), load(profiles_path)
clothing, clothing_profiles = load(clothing_path), load(clothing_profiles_path)
before_extension, before_profiles = copy.deepcopy(extension), copy.deepcopy(profiles)
before_clothing, before_clothing_profiles = copy.deepcopy(clothing), copy.deepcopy(clothing_profiles)
assert len(profiles["profiles"]) == 146, "Refuse repeated augmentation."
research = ROOT / "docs/research-evidence/photo-prompt/wardrobe-keyword-semantics-20261010"
cards = {card["id"]: card for card in load(research / "SEMANTIC-CARDS.json")["cards"]}
decisions = load(HERE.parent / "wardrobe-keyword-integration-20261010/INTEGRATION-DECISIONS.json")
entries = {row["id"]: row for rows in extension["slots"].values() for row in rows}

observations = {
    "008": ("The side edge of the same long outer garment and the torso are separately visible with open space between them.",
            "an opening between front panels without a visible torso-side gap"),
    "025": ("Scalloped lace follows the inner edge of the same garment neckline with its attachment boundary visible.",
            "a separate necklace or nearby lace that does not follow the same neckline"),
    "047": ("Fine yarn crossings and a distinct stitched edge remain readable on one continuous area of cloth.",
            "surface grain, blur or another object's weave without resolved yarn crossings beside the stitched edge"),
    "074": ("The opaque body panel and translucent sleeve of one garment meet at the same visible joining boundary.",
            "global transparency that removes the opaque-body versus sheer-sleeve distinction"),
    "080": ("Two distinct strap-end fittings visibly connect to and support the body of the same bag.",
            "one local fitting standing in for two complete attachments or the whole strap route"),
    "095": ("The same worn skirt forms short compressed folds at its visible contact with the seat surface.",
            "long hanging pleats or ordinary wrinkles away from the visible seat contact"),
}
changed = []
for profile in profiles["profiles"]:
    number = profile["id"].split("_")[1][2:]
    if number not in observations:
        continue
    paraphrase, contrast = observations[number]
    profile["semantics"]["paraphrase_examples"] = unique(profile["semantics"]["paraphrase_examples"] + [paraphrase])
    profile["semantics"]["contrast_examples"] = unique(profile["semantics"]["contrast_examples"] + [contrast])
    profile["reject_substitutes"] = unique(profile["reject_substitutes"] + [contrast])
    candidate = entries[profile["id"] + "_candidate"]
    candidate["paraphrases"] = unique(candidate.get("paraphrases", []) + [paraphrase])
    candidate["keywords"] = unique(candidate.get("keywords", []) + [paraphrase])
    candidate["embedding_text"] += " | " + paraphrase
    usage = candidate.setdefault("contextual_usage", {"contexts": []})
    usage["contexts"].append({
        "id": profile["id"] + "_visible_endpoints",
        "definition": "Use the complete visible relation on the existing permitted owner.",
        "observable_interpretation": paraphrase,
        "claim_limits": ["A local impression does not establish missing endpoints, continuity, quantity or hidden material identity."],
        "activation_authority": "interpretation_only_not_a_required_visual_recipe",
    })
    bundle = next(row for row in extension["visual_semantics"] if candidate["id"] in row["candidate_ids"])
    bundle["confusion_boundaries"] = unique(bundle["confusion_boundaries"] + [contrast])
    changed.append(profile["id"])

retained = [("WK024", "clt_ct037_v1", "양쪽 부착 경계 사이에 드리워진 같은 목선의 주름", ["cowl neckline", "loose neck folds"]),
            ("WK029", "clt_ct047_v1", "같은 손목 커프에 모인 풍성한 소매", ["bishop sleeve", "gathered wrist cuff"])]
retained_rows = []
for card_id, candidate_id, label, cues in retained:
    card = cards[card_id]
    pid = "wkr_" + card_id.lower() + "_retained_relation"
    text = card["observable_proposition_en"]
    profile = {
        "id": pid, "category": "wardrobe_owner_selected_relation",
        "activation": {"exact_terms": [text], "requires_adult_character": False,
                       "semantic_discovery_requires_component_evidence": True,
                       "hard_activation": {"contract_version": "photo-visual-hard-activation/v1",
                                           "required_any_groups": [{"id": "complete_selected_relation", "any_terms": [text]}]}},
        "semantics": {"definition": text, "paraphrase_examples": [label], "visual_components": [text],
                      "contrast_examples": card["confusion_boundaries_ko"],
                      "claim_limits": ["This is a complete selected relation, not a universal construction definition for the family label.",
                                       "Only visible ownership, boundaries and attachment can be assessed; hidden construction and fiber identity are not established."]},
        "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": [{
            "id": "component_1", "match_terms": [text, *cues], "evidence_field": "component_1_phrase",
            "evidence_terms": [text], "min_content_words": 3,
            "instruction": "Keep the selected owner and complete visible relation together: " + text,
            "render_gate": {"id": "vo_" + pid + "_1", "review_scale": "native",
                            "description": text + " Inspect the declared owner, attachment endpoints and distinguishing shape in this same image. Hidden or partial evidence fails."}}]},
        "concept_candidate": {"concept_terms": [label, text], "core_assertion_discovery": True,
                              "affected_dimensions": card["affected_dimensions"], "affected_properties": card["affected_properties"]},
        "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                               "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
        "reject_substitutes": card["confusion_boundaries_ko"],
    }
    profiles["profiles"].append(profile)
    relations = [{"id": pid + "_relation", "type": card["relations"][0]["type"],
                  "subject": card["owner"], "object": card["counterpart"]}]
    bundle = {"id": pid + "_bundle", "primary_visual_proposition": text, "hard_profile_ids": [pid],
              "component_groups": [{"id": "component_1", "visible_evidence": [text]}],
              "candidate_ids": [candidate_id], "candidate_slots": {candidate_id: "garment_detail"},
              "confusion_boundaries": card["confusion_boundaries_ko"], "source_keywords": [label, text],
              "candidate_only": True, "activation_mode": "component_complete_exact_only", "relations": relations}
    extension["visual_semantics"].append(bundle)
    entry = next(row for row in clothing["slots"]["garment_detail"] if row["id"] == candidate_id)
    old_profile = next(row for row in clothing_profiles["profiles"] if row["id"] == "clothing_" + candidate_id[4:])
    properties = entry["affected_properties"] + card["affected_properties"]
    entry["affected_properties"] = list({(p["dimension"], p["target"], p["property"]): p for p in properties}.values())
    entry["affected_dimensions"] = unique(entry["affected_dimensions"] + card["affected_dimensions"])
    old_profile["concept_candidate"]["affected_dimensions"] = copy.deepcopy(entry["affected_dimensions"])
    old_profile["concept_candidate"]["affected_properties"] = copy.deepcopy(entry["affected_properties"])
    retained_rows.append({"card_id": card_id, "candidate_id": candidate_id, "profile_id": pid, "bundle_id": bundle["id"],
                          "identity_reused": True, "complete_relation": text,
                          "reason": "Retained family identity lacked a separate bounded endpoint contract for this research relation; preserve its broader old profile."})

# Existing opt-in duties stay byte-identical for valid repair lineage.
old_by_id = {row["id"]: row for row in before_profiles["profiles"]}
for row in profiles["profiles"]:
    if row["id"] in old_by_id:
        assert row["authored_components"] == old_by_id[row["id"]]["authored_components"]
        assert row["activation"] == old_by_id[row["id"]]["activation"]
old_clothing_profiles = {row["id"]: row for row in before_clothing_profiles["profiles"]}
for row in clothing_profiles["profiles"]:
    old = old_clothing_profiles[row["id"]]
    assert row["authored_components"] == old["authored_components"]
    assert row["activation"] == old["activation"]

change_record = {"schema": "wardrobe-failure-refinement/v1", "existing_profile_discovery_contrast_updates": changed,
                 "complete_old_gate_and_activation_bytes_preserved": True,
                 "retained_candidate_endpoint_contracts": retained_rows,
                 "new_candidate_ids": [], "new_profiles": 2, "new_bundles": 2,
                 "previous_research_decisions_unchanged": True,
                 "annotation_ids_retained_externally": [r["card_id"] for r in decisions["annotations"]],
                 "runtime_global_negatives_or_case_routing_added": False}
write(HERE / "DATA-CHANGES.json", change_record)

maintenance_dir = HERE.parent / "extension-maintenance"
prior_ref = extension.pop("maintenance_ref")
record = load(maintenance_dir / (prior_ref["record_id"] + ".json"))
record.update(record_id="wardrobe-owner-relations-20261010-v7", authored_source_sha256=digest(extension),
              profile_source_sha256=digest(profiles), decisions_sha256=digest(change_record), prior_maintenance_ref=prior_ref,
              reason="Preserve existing duties; improve endpoint contrasts and complete retained cowl/bishop relation contracts.")
record["affected_candidate_ids"] = unique(record["affected_candidate_ids"] + [r[1] for r in retained])
extension["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": record["record_id"], "sha256": digest(record)}

clothing_ref = clothing.pop("maintenance_ref")
clothing_record = load(maintenance_dir / (clothing_ref["record_id"] + ".json"))
clothing_record.update(record_id="clothing-retained-wardrobe-effects-20261010", authored_source_sha256=digest(clothing),
                       prior_maintenance_ref=clothing_ref, profile_filename=clothing_profiles_path.name,
                       profile_source_sha256=digest(clothing_profiles),
                       reason="Declare same-owner cowl drape and bishop cuff/sleeve effects while preserving all candidate identities and prior profile duties.")
clothing["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": clothing_record["record_id"], "sha256": digest(clothing_record)}

unchanged_entries = 0
new_clothing = {row["id"]: row for rows in clothing["slots"].values() for row in rows}
for rows in before_clothing["slots"].values():
    for row in rows:
        if row["id"] not in {r[1] for r in retained}:
            assert new_clothing[row["id"]] == row
            unchanged_entries += 1
write(HERE / "ROW-PRESERVATION.json", {"status": "PASS", "existing_wardrobe_profile_duties_preserved": 146,
                                      "existing_clothing_profile_duties_preserved": len(old_clothing_profiles),
                                      "other_clothing_candidates_unchanged": unchanged_entries,
                                      "only_clothing_effect_rows_changed": [r[1] for r in retained]})

with source_update(SKILL):
    write(maintenance_dir / (record["record_id"] + ".json"), record)
    write(maintenance_dir / (clothing_record["record_id"] + ".json"), clothing_record)
    write(extension_path, extension)
    write(profiles_path, profiles)
    write(clothing_path, clothing)
    write(clothing_profiles_path, clothing_profiles)
print(json.dumps({"updated_existing_profiles": len(changed), "new_profiles": 2, "new_bundles": 2,
                  "new_candidates": 0, "retained_candidate_effects_completed": 2, "old_gates_preserved": 146}, ensure_ascii=False))
