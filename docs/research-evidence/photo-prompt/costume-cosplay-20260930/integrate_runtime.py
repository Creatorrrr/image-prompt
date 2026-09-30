#!/usr/bin/env python3
"""Compile reviewed research into runtime data; retain provenance in maintenance evidence."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_semantics as semantics
from visual_profile_contracts import compile_visual_profile

ASSETS = SKILL / "assets"
EXTENSION = "photo_prompt_costume_cosplay_extension.json"
OBLIGATIONS = "photo_prompt_visual_obligations_costume_cosplay.json"
RECORD_ID = "photo_prompt_costume_cosplay_extension"

# Alternative ordinary-language discovery phrases. Exact activation and hard
# evidence still use the full authored component clauses, never these examples.
PARAPHRASE_TEMPLATES = {
    "connected_to": "visible connection between {subject} and {object}",
    "layered_over": "{subject} layered over {object}",
    "distinct_from": "{subject} clearly separate from {object}",
    "directional_length": "{subject} with a short front and longer rear tails",
    "layered_inside": "{subject} visible inside {object}",
    "connected_across": "{subject} continuing across {object}",
    "positioned_below": "{subject} positioned below {object}",
    "surrounds": "{subject} surrounding {object}",
    "aligned_along": "{subject} arranged along {object}",
    "anchored_to": "{subject} visibly anchored to {object}",
    "attached_at_both_ends": "both ends of the {subject} attached to {object}",
    "continuous_across": "{subject} forming one continuous garment across {object}",
    "attached_to": "{subject} visibly attached to {object}",
    "border": "{subject} bordering {object}",
    "rests_on": "{subject} resting on {object}",
    "joins": "{subject} joined to {object}",
    "separated_from": "{subject} separated by a visible gap from {object}",
    "repeats_across": "{subject} repeated at matching positions across {object}",
    "owned_separately_by": "{subject} attached separately to {object}",
    "asymmetric_between": "different {subject} on the {object}",
    "asymmetric_length": "{subject} ending at unequal heights on the {object}",
    "frames": "{subject} framing a separately visible {object}",
    "suspended_from": "{subject} hanging from visible {object}",
    "visible_between": "{subject} visible in the gaps between {object}",
    "stop_around": "{subject} ending around the {object}",
    "localized_on": "{subject} confined to the surface of {object}",
    "overlap": "{subject} visibly overlapping {object}",
    "bounded_by": "{subject} enclosed by a visible border of {object}",
    "contained_by": "{subject} contained inside {object}",
    "overlap_with_distinct_edges": "{subject} overlapping {object} with separately readable edges",
    "distinct_from_each_other": "{subject} with separate tips and outlines above the {object}",
    "extend_to_opposite_sides": "{subject} spreading on opposite sides of the {object}",
    "encloses": "{subject} enclosing {object}",
    "join": "{subject} joined at distinct cuffs to {object}",
    "has_visible_boundary": "{subject} retaining a visible {object}",
    "continue_beneath": "{subject} extending continuously under the {object}",
    "wraps_around": "{subject} wrapping as a separate band around {object}",
    "ends_above": "{subject} ending above the separate {object}",
    "run_along": "{subject} continuing lengthwise along {object}",
    "closes": "{subject} closing the {object}",
    "extend_from": "{subject} starting at the {object}",
    "spreads_around": "{subject} flaring outward around the {object}",
    "repeat_across": "{subject} repeated across the {object}",
    "project_from": "{subject} projecting from the {object}",
    "varies_across": "brightness of {subject} varying across {object}",
    "continuous_with": "{subject} continuing into the {object}",
    "continue_toward": "{subject} continuing toward the {object}",
    "raised_above": "{subject} standing in relief above the {object}",
    "flat_against": "{subject} lying flat against the {object}",
    "in_contact_with": "{subject} making visible contact with the {object}",
    "encircles": "{subject} encircling the {object}",
    "positioned_beyond": "{subject} positioned beyond the separate {object}",
    "visible_inside": "{subject} separately visible inside the {object}",
    "continue_between": "{subject} continuing between the {object}",
    "gathers": "{subject} gathering the {object} into folds",
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    research = read(HERE / "visual-semantics.proposed.json")
    candidates = read(HERE / "candidate-data.proposed.json")
    bundles = read(HERE / "candidate-bundles.proposed.json")
    profile_map = {}
    component_map = {}
    scope = {}
    runtime_profiles = []
    # A single relation is the activation unit. Family rows remain a maintenance grouping.
    # This avoids imposing every researched relation when only one was requested.
    for family in research["profiles"]:
        family_profiles = []
        for component in family["components"]:
            cid = component["id"]
            pid = "costume_" + cid
            exact = [component["en"], component["ko"]]
            row = {
                "id": pid, "category": "costume_cosplay_visible_relation",
                "activation": {
                    "exact_terms": exact, "requires_adult_character": False,
                    "semantic_discovery_requires_component_evidence": True,
                    "hard_activation": {
                        "contract_version": "photo-visual-hard-activation/v1",
                        "required_any_groups": [{"id": "selected_relation", "any_terms": exact}],
                    },
                },
                "semantics": {
                    "definition": component["en"],
                    "paraphrase_examples": [PARAPHRASE_TEMPLATES[component["assertion"]["type"]].format(
                        subject=component["assertion"]["subject"], object=component["assertion"]["object"])],
                    "contrast_examples": family["confusion_boundaries"],
                    "claim_limits": [
                        "One request-supported visible relation, not a universal costume or character definition.",
                        "The selected garment or appendage does not establish wearer identity, age, occupation or anatomy.",
                        "Occluded required relations fail pixel review; hidden construction or physical function is not inferred.",
                    ],
                },
                "concept_candidate": {
                    "concept_terms": list(dict.fromkeys([component["ko"], family["label_ko"]])),
                },
                "runtime_expression": {
                    "default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                    "forbidden_prompt_terms": [], "runtime_forbidden_labels": [],
                },
                "reject_substitutes": family["confusion_boundaries"],
                "authored_components": {
                    "contract_version": "photo-authored-visual-components/v1",
                    "components": [{
                        "id": "component_1", "match_terms": exact,
                        "evidence_field": "component_1_phrase",
                        "evidence_terms": [component["en"]], "min_content_words": 3,
                        "instruction": "Preserve this selected visible owner relation: " + component["en"],
                        "render_gate": {k: component["render_gate"][k]
                                        for k in ("id", "review_scale", "description")},
                    }],
                },
            }
            compile_visual_profile(row)
            runtime_profiles.append(row)
            profile_map[cid] = pid
            component_map[cid] = component
            family_profiles.append(pid)
        scope[family["id"]] = {
            "runtime_profile_ids": family_profiles,
            "source_refs": family["source_refs"],
            "source_record_bindings": family["source_record_bindings"],
            "evidence_basis": family["evidence_basis"],
            "minimum_view": family["minimum_view"],
            "broad_terms_not_sufficient": family["broad_terms_not_sufficient"],
            "confusion_boundaries": family["confusion_boundaries"],
        }
    runtime_registry = {
        "schema_version": "photo-visual-obligation-registry-extension/v1",
        "relation_contract_version": "photo-visual-relation/v1",
        "description": "Independently requested visible costume, attachment, surface and prop relations.",
        "profiles": runtime_profiles,
    }
    write(ASSETS / OBLIGATIONS, runtime_registry)

    allowed_fields = {
        "id", "ko", "en", "weight", "for_any", "aliases", "keywords", "embedding_text",
        "concept_units", "relations",
    }
    slot_scopes = {
        "costume_style": ["appearance"], "garment_detail": ["appearance"],
        "wearable_accessory": ["appearance"], "surface_material": ["material"],
        "hair_style": ["appearance"], "action": ["action", "appearance"],
        "location": ["setting"],
    }
    individual_scopes = {
        "ccx_cc36_01": ["action", "pose"],
        "ccx_cc36_02": ["appearance"],
        "ccx_cc12_02": ["appearance"],
        "ccx_loose_ear_tail_components": ["appearance", "setting"],
        "ccx_convention_floor_portrait": ["framing", "setting"],
        "ccx_studio_costume_catalog": ["style", "framing", "setting"],
        "ccx_two_wearer_stage_scene": ["count", "subject", "setting"],
        "ccx_cc09_01": ["appearance", "count"],
        "ccx_cc09_02": ["appearance", "count"],
    }
    slots = {}
    by_id = {}
    for slot, entries in candidates["slots"].items():
        for entry in entries:
            out = {k: copy.deepcopy(v) for k, v in entry.items() if k in allowed_fields}
            out["tags"] = ["human", "costume", "cosplay"]
            out["aliases"] = list(dict.fromkeys([entry["ko"], *entry.get("aliases", [])]))
            out["keywords"] = list(dict.fromkeys([entry["ko"], *entry.get("keywords", [])]))
            out["embedding_text"] = entry["en"] + " | " + " | ".join(out["keywords"])
            out["affected_dimensions"] = individual_scopes.get(entry["id"], slot_scopes.get(slot))
            assert out["affected_dimensions"], (slot, entry["id"])
            slots.setdefault(slot, []).append(out)
            by_id[out["id"]] = (slot, out)

    visual_semantics = []
    for bundle in bundles["bundles"]:
        ids = bundle["component_ids"]
        visual_semantics.append({
            "id": "costume_" + bundle["id"].lower(),
            "primary_visual_proposition": bundle["same_frame_relation"],
            "component_groups": [
                {"id": f"component_{i}", "visible_evidence": by_id[cid][1]["concept_units"]}
                for i, cid in enumerate(ids, 1)
            ],
            "candidate_ids": ids,
            "candidate_slots": {cid: by_id[cid][0] for cid in ids},
            "hard_profile_ids": [profile_map[cid] for cid in ids],
            "relations": [{
                "id": "same_frame_owner_relation", "type": "same_frame_owner_relation",
                "subject": "the request-supported costume wearer",
                "object": bundle["same_frame_relation"],
            }],
            "confusion_boundaries": list(dict.fromkeys(
                note for fid in bundle["proposed_profile_refs"]
                for note in scope[fid]["confusion_boundaries"])),
            "candidate_only": True,
            "activation_mode": "independent_component_request_evidence_only",
            "source_keywords": [bundle["label_ko"]],
        })
    extension = {
        "schema_version": "photo-prompt-research-extension/v1",
        "slots": slots, "visual_semantics": visual_semantics,
    }
    maintenance = {
        "contract_version": "photo-extension-maintenance/v1",
        "record_id": RECORD_ID, "source_filename": EXTENSION,
        "authored_source_sha256": semantics.digest(extension),
        "runtime_keys": ["slots", "visual_semantics"],
        "maintenance_only": {
            "research_path": str(HERE.relative_to(ROOT)),
            "source_ledger_sha256": semantics.digest(read(HERE / "sources.json")),
            "candidate_drafts_sha256": semantics.digest(candidates),
            "visual_research_sha256": semantics.digest(research),
            "runtime_registry_sha256": semantics.digest(runtime_registry),
            "profile_scope": scope,
            "research_to_runtime_profile_ids": profile_map,
            "reused_profiles_and_scope_exclusions": research["reuse_and_scope_exclusions"],
            "adoption_scope": "42 family groups, 87 independent component profiles, 94 candidates and 27 optional recipes.",
            "materialization_policy": "No character-version, wearer-body or population-frequency inference.",
            "qualification_status": "runtime_integrated_pixels_pending",
        },
    }
    write(ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (RECORD_ID + ".json"), maintenance)
    extension["maintenance_ref"] = {
        "contract_version": "photo-extension-maintenance-ref/v1",
        "record_id": RECORD_ID, "sha256": semantics.digest(maintenance),
    }
    write(ASSETS / EXTENSION, extension)
    tags_path = ASSETS / "photo_prompt_tags.json"
    tags = read(tags_path)
    required = tags["candidate_semantic_policy"]["required_extensions"]
    if EXTENSION not in required:
        text = tags_path.read_text()
        previous_last = required[-1]
        needle = '      "' + previous_last + '"\n'
        assert text.count(needle) == 1, "Required-extension list needs a unique insertion point."
        required.append(EXTENSION)
        updated = text.replace(needle, needle.rstrip('\n') + ',\n      "' + EXTENSION + '"\n')
        assert json.loads(updated) == tags
        tags_path.write_text(updated)
    write(HERE / "runtime-integration-map.json", {
        "status": "runtime_integrated_indexes_and_validation_pending",
        "family_count": len(scope), "profile_count": len(runtime_profiles),
        "candidate_count": len(by_id), "bundle_count": len(visual_semantics),
        "family_scope": scope, "component_profile_ids": profile_map,
        "runtime_files": [str((ASSETS / name).relative_to(ROOT)) for name in (EXTENSION, OBLIGATIONS)],
        "maintenance_record": str((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (RECORD_ID + ".json")).relative_to(ROOT)),
    })
    print(f"compiled {len(runtime_profiles)} component profiles, {len(by_id)} candidates, {len(visual_semantics)} optional bundles")


if __name__ == "__main__":
    main()
