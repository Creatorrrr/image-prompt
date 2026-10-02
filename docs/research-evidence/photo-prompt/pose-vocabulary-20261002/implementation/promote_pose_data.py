#!/usr/bin/env python3
"""Adapt reviewed research atoms to the current, optional runtime contracts.

Research/source/variant status stays in the maintenance ledger. This script
does not invent requester assertions, change existing candidate meanings, or
qualify pixels. It also never resolves an unrelated working-tree conflict.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RESEARCH = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as generator

ACCEPTED = {"definition_ready", "project_operational_definition", "reuse_existing_profile"}
EXTENSION = "photo_prompt_pose_vocabulary_extension.json"
PROFILE_EXTENSION = "photo_prompt_visual_obligations_pose_vocabulary.json"
RECORD_ID = "photo_prompt_pose_vocabulary_reviewed_20261002"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def baseline_data() -> tuple[dict, list[str]]:
    """Read a maintenance comparison without changing concurrent merge work.

    The incoming maintenance-reference alternative is used only in this
    in-memory comparison if a concurrent merge leaves conflict markers.
    Live validation and final indices still require the actual resolved file.
    """
    data = json.loads((ASSETS / "photo_prompt_tags.json").read_text())
    conflicts = []
    for filename in generator.RESEARCH_EXTENSION_FILENAMES:
        if filename == EXTENSION:
            continue
        path = ASSETS / filename
        if not path.exists():
            continue
        raw = path.read_text()
        if "<<<<<<< " in raw:
            conflicts.append(str(path.relative_to(ROOT)))
            raw = re.sub(r"^<<<<<<< [^\n]*\n.*?^=======\n(.*?)^>>>>>>> [^\n]*\n", r"\1", raw, flags=re.M | re.S)
        data = generator.merge_research_extension(data, json.loads(raw))
    return data, conflicts


def scope(row: dict) -> tuple[list[str], list[dict]]:
    slot, name = row["target_slot"], row["id"]
    if slot == "body_pose":
        dimensions, property_path = ["pose"], "body.support_and_configuration"
    elif slot == "body_orientation":
        dimensions, property_path = ["pose"], "body.segment_orientation"
    elif slot == "hand_pose":
        dimensions, property_path = ["pose"], "body.hand_configuration"
    elif slot == "gaze_engagement":
        dimensions, property_path = ["expression"], "eyes.gaze_direction"
    elif slot == "expression":
        dimensions, property_path = ["expression"], "face.expression"
    elif slot == "contact_point":
        dimensions, property_path = ["pose", "relationship"], "body.contact_configuration"
    else:
        dimensions, property_path = ["action", "pose"], "body.action_configuration"
        if slot == "relational_action":
            dimensions.append("relationship")
    effects = [{"dimension": dimensions[0], "target": "main_subject", "property": property_path}]
    if name in {"pv_arms_behind_head", "pv_wrists_cross_overhead", "pv_arm_heart", "pv_flower_chin", "pv_finger_frame", "pv_ballet_fifth_arms_overhead"}:
        effects.append({"dimension": "pose", "target": "main_subject", "property": "body.arm_configuration"})
    for dimension in dimensions[1:]:
        effects.append({"dimension": dimension, "target": "main_subject", "property":
                        "body.support_and_configuration" if dimension == "pose" else "body.contact_configuration"})
    paired = name in {"pv_handholding_pair", "pv_linked_arms", "pv_forehead_pair", "pv_nose_pair", "pv_head_shoulder_pair"} or slot == "relational_action"
    if paired:
        effects += [{**effect, "target": "partner_subject"} for effect in effects]
    return dimensions, effects


def runtime_terms(row: dict) -> list[str]:
    conditional = {term.casefold() for rule in row.get("conditional_alias_constraints", []) for term in rule["terms"]}
    conditional.update({"밤비 포즈", "bambi pose", "bambi", "self-covering", "셀프 커버링"})
    return list(dict.fromkeys(term for term in [row["ko"], *row["aliases"]]
                              if term.casefold() not in conditional and len(term.strip()) > 2))


def natural_units(row: dict) -> list[str]:
    return [text.replace("actor_1", "the first actor").replace("actor_2", "the second actor") for text in row["concept_units"]]


def main() -> None:
    proposed = json.loads((RESEARCH / "candidate-data.proposed.json").read_text())["candidates"]
    proposals = json.loads((RESEARCH / "visual-profiles.proposed.json").read_text())["profiles"]
    refined = json.loads((OUT / "refined-variants.json").read_text())["candidates"]
    for row in refined:
        proposals.append({"id": "pv_profile_" + row["id"][3:], "candidate_id": row["id"],
                          "qualification": row["qualification"], "operation": "propose_new_profile"})
    current, conflicts = baseline_data()
    current_entries = {slot: {entry["id"]: entry for entry in entries} for slot, entries in current["slots"].items()}
    registry = generator.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    known_profiles = {profile["id"] for profile in registry["profiles"]}
    existing_extension = ASSETS / PROFILE_EXTENSION
    if existing_extension.exists():
        known_profiles -= {profile["id"] for profile in json.loads(existing_extension.read_text())["profiles"]}
    sources = [RESEARCH / name for name in ("candidate-data.proposed.json", "visual-profiles.proposed.json", "candidate-atoms.tsv", "row-decompositions.tsv", "sources.json", "keyword-catalog.json")]
    sources += [OUT / "refined-variants.json", OUT / "supplemental-sources.json"]
    if not (OUT / "baseline.json").exists():
        tracked_sources = [ASSETS / "photo_prompt_tags.json", ASSETS / "photo_prompt_visual_obligations.json", SKILL / "scripts/prompt_generator.py"]
        write(OUT / "baseline.json", {
            "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "slot_count": len(current["slots"]), "candidate_count": sum(map(len, current["slots"].values())),
            "profile_count": len(registry["profiles"]),
            "files": {str(path.relative_to(ROOT)): digest(path) for path in tracked_sources},
            "concurrent_unresolved_paths": conflicts,
            "comparison_only_conflict_policy": "incoming metadata reference in memory; working files untouched",
            "existing_work": "preserved; no reset, checkout, commit or push",
        })

    extension = {"schema_version": generator.RESEARCH_EXTENSION_SCHEMA, "slots": {}, "existing_slot_context_extensions": {}, "visual_semantics": []}
    slots, contexts = defaultdict(list), defaultdict(dict)
    promoted, dispositions = {}, []
    for row in proposed + refined:
        accepted = row["qualification"] in ACCEPTED
        disposition = {"research_id": row["id"], "research_qualification": row["qualification"], "source_ids": row["source_ids"],
                       "conditional_alias_constraints": row.get("conditional_alias_constraints", []),
                       "confusion_boundaries": row["confusion_boundaries"], "entity_bindings": row["required_entity_bindings"],
                       "observability": row["observability"], "pixel_status": "not_run", "user_acceptance": "pending"}
        if not accepted:
            disposition.update(status="deferred_variant_or_source_review", runtime_candidate=None,
                               reason="Research explicitly requires a variant, individual source, phase or reference calibration; no global alias or hard meaning is invented.")
            dispositions.append(disposition)
            continue
        reused = row.get("existing_reuse_or_extension_target")
        if reused:
            slot, entry_id = reused["slot"], reused["id"]
            if entry_id not in current_entries.get(slot, {}):
                raise ValueError(f"Missing reuse target {slot}.{entry_id}")
            target = current_entries[slot][entry_id]
            # Equivalent paraphrases only; retain original labels, units, effects and guards.
            contexts[slot][entry_id] = {"paraphrases": list(dict.fromkeys(runtime_terms(row) + natural_units(row))), "contexts": [{
                "id": "pose_vocabulary_" + row["id"],
                "meaning_scope": row["en"], "ordinary_readings": row["confusion_boundaries"],
                "claim_limits": ["Equivalent observable pose only; attire, tone, framing and actor count are independent.",
                                 "Apparent support is visible configuration, not a force measurement."],
            }]}
            disposition.update(status="reused_with_equivalent_context", runtime_candidate={"slot": slot, "id": entry_id},
                               original_candidate_sha256=generator.photo_candidate_semantics.digest(target))
            promoted[row["id"]] = (row, slot, entry_id, *scope(row))
        else:
            slot, entry_id = row["target_slot"], row["id"]
            if entry_id in current_entries.get(slot, {}):
                raise ValueError(f"Duplicate runtime target {slot}.{entry_id}")
            dimensions, effects = scope(row)
            units, terms = natural_units(row), runtime_terms(row)
            candidate = {
                "id": entry_id, "ko": row["ko"], "en": "; ".join(units), "weight": 0.5,
                "tags": ["human", "pose_vocabulary", slot], "for_any": ["human"],
                "aliases": terms, "keywords": terms, "embedding_text": "; ".join(terms + units),
                "concept_units": units,
                "relations": [{"id": "owner_scope", "type": "declared_owner_scope", "subject": "main_subject",
                               "object": "the body parts, support surfaces and contact targets stated in this configuration"}],
                "affected_dimensions": dimensions, "affected_properties": effects, "core_assertion_discovery": True,
            }
            if slot == "relational_action" or any("partner_subject" == effect["target"] for effect in effects):
                candidate["requires_primary_any_tags"] = ["pair", "couple", "partners", "group", "two_people", "multiple_people", "relationship"]
            slots[slot].append(candidate)
            disposition.update(status="new_optional_candidate", runtime_candidate={"slot": slot, "id": entry_id})
            promoted[row["id"]] = (row, slot, entry_id, dimensions, effects)
        dispositions.append(disposition)

    profiles, profile_dispositions = [], []
    for proposal in proposals:
        if proposal["qualification"] not in ACCEPTED:
            profile_dispositions.append({"profile_id": proposal["id"], "status": "deferred", "reason": proposal["qualification"]})
            continue
        if proposal["operation"] == "review_existing_profile_do_not_duplicate":
            if proposal["id"] not in known_profiles:
                raise ValueError("Existing visual profile missing")
            profile_dispositions.append({"profile_id": proposal["id"], "status": "reused_unchanged", "pixel_status": "not_run"})
            continue
        row, slot, entry_id, dimensions, effects = promoted[proposal["candidate_id"]]
        units, terms = natural_units(row), runtime_terms(row)
        if proposal["id"] in known_profiles:
            raise ValueError("Duplicate visual profile")
        # Bare nickname/domain words remain optional retrieval leads. Exact
        # activation uses a pose-qualified label, or the explicit Korean
        # configuration, so an ornament/object homonym does not set geometry.
        exact_terms = [row["ko"]] + [term if term.casefold().endswith(" pose") else
                                    term + (" 자세" if re.search(r"[가-힣]", term) else " pose")
                                    for term in terms if term != row["ko"]]
        profile = {
            "id": proposal["id"], "category": "observable_pose_configuration",
            "activation": {"exact_terms": list(dict.fromkeys(exact_terms)), "requires_adult_character": False,
                           "semantic_discovery_requires_component_evidence": True,
                           "hard_activation": {"contract_version": "photo-visual-hard-activation/v1", "required_any_groups": [{
                               "id": "body_pose_context", "any_terms": ["pose", "posing", "posture", "person", "woman", "man", "human", "subject", "actor", "dancer", "ballet", "sitting", "seated", "kneeling", "hand", "finger", "foot", "인물", "자세", "포즈", "사람", "무릎", "손", "발레", "앉기", "앉은"]
                           }]}},
            "semantics": {"definition": "; ".join(units), "paraphrase_examples": units,
                          "visual_components": units, "contrast_examples": row["confusion_boundaries"],
                          "claim_limits": ["Bind every limb and contact target to its declared actor; laterality is actor-relative.",
                                           "Support means an observable support configuration, not measured force or motion history.",
                                           "Each required component must be visible and pass; partial evidence fails and occlusion is unobservable.",
                                           "A locked crop is preserved; an invisible prerequisite cannot be reported as satisfied.",
                                           "This geometry creates no identity, body-shape, wardrobe, tone, camera or actor-count requirement."]},
            "concept_candidate": {"concept_terms": terms + units, "core_assertion_discovery": True,
                                  "affected_dimensions": dimensions, "affected_properties": effects},
            "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                                   "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "reject_substitutes": row["confusion_boundaries"],
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": [{
                "id": f"component_{index}", "match_terms": [unit], "evidence_field": f"component_{index}_phrase",
                "evidence_terms": [unit], "min_content_words": 3,
                "instruction": "Bind this visible configuration to the declared actor and target: " + unit + ".",
                "render_gate": {"id": f"vo_{proposal['id']}_{index}", "review_scale": "both",
                                "description": unit + ". Inspect the complete relation in the original pixels; partial evidence fails and a hidden prerequisite is unobservable."},
            } for index, unit in enumerate(units, 1)]},
        }
        generator.compile_visual_profile(profile)
        profiles.append(profile)
        profile_dispositions.append({"profile_id": proposal["id"], "status": "new_request_scoped_or_explicit_opt_in_profile",
                                     "candidate_id": entry_id, "source_ids": row["source_ids"],
                                     "definition_basis": row["qualification"], "gate_basis": "project_operationalization_not_a_source_standard",
                                     "pixel_status": "not_run"})
        extension["visual_semantics"].append({
            "id": "pv_bundle_" + row["id"][3:], "candidate_only": True, "primary_visual_proposition": "; ".join(units),
            "candidate_ids": [entry_id], "candidate_slots": {entry_id: slot}, "hard_profile_ids": [proposal["id"]],
            "component_groups": [{"id": f"component_{index}", "visible_evidence": [unit]} for index, unit in enumerate(units, 1)],
            "source_keywords": terms, "confusion_boundaries": row["confusion_boundaries"],
            "relations": [{"id": "owner_scope", "type": "declared_owner_scope", "subject": "main_subject",
                           "object": "the expressly declared support and contact configuration"}],
        })

    extension["slots"] = dict(slots)
    extension["existing_slot_context_extensions"] = dict(contexts)
    record = {
        "contract_version": "photo-extension-maintenance-record/v1", "record_id": RECORD_ID,
        "maintenance_only": True,
        "source_hashes": {str(path.relative_to(ROOT)): digest(path) for path in sources},
        "source_catalog": "docs/research-evidence/photo-prompt/pose-vocabulary-20261002/keyword-catalog.json",
        "dispositions": [row for row in dispositions if row["research_id"] in {entry["id"] for entry in proposed}],
        "refinement_dispositions": [row for row in dispositions if row["research_id"] in {entry["id"] for entry in refined}],
        "profile_dispositions": profile_dispositions,
        "counts": dict(Counter(row["status"] for row in dispositions)),
        "runtime_policy": "Reviewed equivalent definitions only; conditional nicknames and unresolved phases remain deferred.",
        "evidence_policy": "Runtime binding and pixel qualification are separate; pack exposure never creates a requester obligation.",
    }
    extension["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": RECORD_ID,
                                    "sha256": generator.photo_candidate_semantics.digest(record)}
    write(ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (RECORD_ID + ".json"), record)
    write(OUT / "implementation-disposition-ledger.json", record)
    write(ASSETS / EXTENSION, extension)
    write(ASSETS / PROFILE_EXTENSION, {"schema_version": generator.VISUAL_OBLIGATION_EXTENSION_SCHEMA_VERSION,
                                      "relation_contract_version": generator.VISUAL_RELATION_CONTRACT_VERSION, "profiles": profiles})
    write(OUT / "promotion-summary.json", {"source_atom_count": len(proposed), "resolved_variant_count": len(refined), "dispositions": record["counts"],
                                           "new_profiles": len(profiles), "new_bundles": len(extension["visual_semantics"]),
                                           "new_candidates_by_slot": {slot: len(rows) for slot, rows in slots.items()},
                                           "deferred_profiles": sum(row["status"] == "deferred" for row in profile_dispositions)})
    print(json.dumps(json.loads((OUT / "promotion-summary.json").read_text()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
