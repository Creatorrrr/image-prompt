#!/usr/bin/env python3
"""Build the unrendered v8 mamang-benevolence fixed-identity preflight."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_mamang_benevolence_v8.json"
BASE_PATH = CASE_DIR / "composed_prompt_peer_liking_v8.json"
OUTPUT_PATH = CASE_DIR / "composed_prompt_mamang_benevolence_v8.json"
AUDIT_PATH = CASE_DIR / "composed_prompt_mamang_benevolence_v8.audit.json"
MUTATION_PATH = CASE_DIR / "mamang_benevolence_v8_mutation_audit.json"

PROMPT_EN = (
    "Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait as sole "
    "identity: eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging. A benevolent mamang-like maid with "
    "relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention watches the adult customer's "
    "scraped knuckle. Caught mid-bandaging, she steadies the hand; pad covers the scrape while one wing stays "
    "open and unfastened. Her soft eyes and reassuring mouth show warm concern. Compact living cat ears, half human-ear "
    "height: near ear turns toward the hand; far ear keeps another angle. Face, hands, frilled apron, ears, bandage "
    "share one focal plane. Subtle adult allure. Room-light bounce casts contact shadow; one loose hair remains. "
    "Plain unlettered bokeh."
)


def load_audit_module():
    audit_module_path = (
        ROOT
        / "skills"
        / "photo-prompt-image-generator"
        / "scripts"
        / "audit_composed_prompt.py"
    )
    spec = importlib.util.spec_from_file_location("photo_prompt_audit", audit_module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load audit module: {audit_module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))[0]
    composed = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    composed["pack_id"] = pack["pack_id"]
    composed["prompt_en"] = PROMPT_EN
    composed["negative_en"] = pack["negative_en"]
    composed["chosen_candidate_ids"] = [
        "preset:maid_cafe_cosplay_portrait",
        "slot:subject:maid_cafe_performer",
        "slot:costume_style:frill_apron_maid_costume",
        "slot:location:maid_cafe_interior",
        "slot:focus:face_detection_focus",
        "slot:anatomical_connection:ear_root_in_hairline",
        "slot:species_marker:feline_reflective_eye_whisker_shadow",
        "augmentation:adult_appeal:sensual_editorial:action:posing_editorial",
    ]
    composed["coverage_assertions"] = {
        "인자한": "benevolent",
        "마망": "mamang-like",
        "예쁘고": "pretty",
        "귀여운": "cute",
        "성인": "Adult woman",
        "네코미미": "living cat ears",
        "메이드": "maid",
    }

    composed["augmentation_brief"] = {
        "concept_core": (
            "Hold the uploaded adult identity, maid costume, and approved low sensual intensity constant while "
            "testing whether explicit mature benevolence reads independently of tsundere denial."
        ),
        "routes_considered": [
            {
                "route_id": "material_world",
                "decision": "selected",
                "reason": (
                    "The maid apron preserves the accepted costume while a minimal adult editorial cue retains "
                    "the user's approved sensual calibration."
                ),
            },
            {
                "route_id": "action_camera",
                "decision": "rejected",
                "reason": "A larger pose or camera consequence would compete with the quiet care action.",
            },
            {
                "route_id": "light_second_reading",
                "decision": "rejected",
                "reason": "Patterned or split light would obscure the four-part benevolent expression test.",
            },
        ],
        "selected_route_id": "material_world",
        "decisions": [
            {
                "candidate_id": "augmentation:adult_appeal:sensual_editorial:action:posing_editorial",
                "decision": "modified",
                "function": "pose_camera",
                "rationale": (
                    "The user judged low-intensity adult appeal appropriate for this maid costume and clarified "
                    "that sensuality can help without defining moe."
                ),
                "marginal_contribution": (
                    "It retains the accepted adult calibration while the face and care action remain primary."
                ),
                "modification": (
                    "Reduce the editorial attitude to calm agency and subtle adult allure; remove sultry gaze and "
                    "body-first posing."
                ),
                "prompt_evidence": "Subtle adult allure",
            },
            {
                "candidate_id": "slot:costume_style:frill_apron_maid_costume",
                "decision": "modified",
                "function": "material_detail",
                "rationale": "The apron preserves the exact role and costume family used in the controlled comparison.",
                "marginal_contribution": "Removing it would change the accepted maid-costume baseline.",
                "modification": "Keep a compact frilled-apron anchor without fetish escalation.",
                "prompt_evidence": "frilled apron",
            },
            {
                "candidate_id": "slot:texture:fine_grain",
                "decision": "rejected",
                "function": "concept_bridge",
                "rationale": "Grain does not strengthen benevolent facial legibility.",
                "marginal_contribution": "None; rejection protects the facial evidence budget.",
            },
            {
                "candidate_id": "slot:color:pastel",
                "decision": "rejected",
                "function": "material_detail",
                "rationale": "A palette change would not test the requested relational affect.",
                "marginal_contribution": "None; rejection keeps the comparison focused on expression.",
            },
        ],
        "adult_appeal": {
            "adult_subject_phrase": "Adult woman",
            "agency_phrase": "she steadies the hand",
            "axes": {
                "sensual_editorial": {"intensity": 1},
                "fetish_fashion": {"intensity": 0},
            },
            "blend": {"emphasis": "sensual_led"},
        },
    }

    evidence = {
        "actor_phrase": "Adult woman",
        "aesthetic_baseline_phrase": (
            "Adult woman, pretty and cute: refined face, lively eyes, glossy hair"
        ),
        "benevolent_affect_phrase": (
            "A benevolent mamang-like maid with relaxed brow, patient soft eyes, reassuring mouth, and calm "
            "protective attention watches the adult customer's scraped knuckle"
        ),
        "affective_leak_phrase": "Her soft eyes and reassuring mouth show warm concern",
        "background_control_phrase": "Plain unlettered bokeh",
        "baseline_phrase": "calm protective attention",
        "event_phase_phrase": "Caught mid-bandaging",
        "trigger_phrase": "the adult customer's scraped knuckle",
        "target_phrase": "one wing stays open and unfastened",
        "visible_response_phrase": (
            "Compact living cat ears, half human-ear height: near ear turns toward the hand; far ear keeps "
            "another angle"
        ),
        "immediate_consequence_phrase": "pad covers the scrape while one wing stays open and unfastened",
        "continuity_phrase": "Face, hands, frilled apron, ears, bandage",
        "focal_plane_phrase": "Face, hands, frilled apron, ears, bandage share one focal plane",
        "reference_identity_phrase": (
            "Preserve uploaded portrait as sole identity: eyes, nose, lips, jaw, skin, hairline, adult age; "
            "no de-aging"
        ),
    }
    composed["moe_response"] = {
        "aesthetic_baseline": "adult_bishoujo",
        "mechanism": "quiet_care_trace",
        "relationship_register": "nurturant_benevolence",
        "baseline": "calm, mature protective attention",
        "event_phase": "mid-bandaging before completion",
        "trigger": "the adult customer's visible scraped knuckle",
        "target": "the recipient's hand and unfinished bandage wing",
        "visible_response": "four-part benevolent expression plus an asymmetric compact-ear reflex",
        "immediate_consequence": "the pad is seated while one adhesive wing remains unfastened",
        "continuity": "the uploaded adult identity, human hands, maid role, and living ears remain stable",
        "support_mechanisms": ["nonhuman_reflex_leak"],
        "prompt_evidence": evidence,
    }
    composed["manual_gate_evidence"] = {
        "nekomimi_living_ear_test": {
            "review_stage": "pixel_review_required",
            "evidence_phrases": [
                evidence["visible_response_phrase"],
                evidence["continuity_phrase"],
            ],
        }
    }

    composed["viewer_experience"] = {
        "target_audience": {
            "literacy": "subculture_literate",
            "required_prior_knowledge": "none; mature protective warmth must be legible from the face and action",
        },
        "viewing_context": "feed_thumbnail",
        "primary_viewer_need": "care",
        "intended_experience": "notice mature benevolence in a specific unfinished act of care",
        "viewer_promise": "the same adult woman calmly protects the recipient while finishing the bandage",
        "first_glance_hook": "a pretty and cute adult maid shows a four-part benevolent expression",
        "interpretive_question": "What makes her care read as patient and protective rather than generic kindness?",
        "affect_evidence": {
            "actor": "the adult nekomimi maid",
            "action": "steadies the customer's hand mid-bandaging",
            "target": "the adult customer's scraped knuckle",
            "consequence": "the pad is seated while one wing remains unfastened",
        },
        "attachment_channel": "continuity",
        "reinspection_reward": {
            "mode": "causal_second_reading",
            "description": "the unfinished bandage proves that her expression belongs to a continuing care action",
        },
        "commercial_objective": "none",
        "prompt_evidence": {
            "first_glance_hook_phrase": evidence["benevolent_affect_phrase"],
            "affect_actor_phrase": "Adult woman",
            "affect_action_phrase": "Caught mid-bandaging",
            "affect_target_phrase": evidence["trigger_phrase"],
            "affect_consequence_phrase": evidence["immediate_consequence_phrase"],
            "attachment_phrase": evidence["reference_identity_phrase"],
            "reinspection_reward_phrase": evidence["target_phrase"],
        },
    }

    OUTPUT_PATH.write_text(
        json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    audit_module = load_audit_module()
    audit = audit_module.audit_composed_prompt(pack, composed)
    AUDIT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if audit.get("status") != "pass":
        raise RuntimeError(f"mamang v8 preflight failed: {audit.get('failures')}")

    original = evidence["benevolent_affect_phrase"]
    mutation_specs = [
        (
            "generic_kindness_only",
            "A kind mamang-like maid watches the adult customer's scraped knuckle",
        ),
        (
            "missing_relaxed_brow",
            "A benevolent mamang-like maid with patient soft eyes, reassuring mouth, and calm protective "
            "attention watches the adult customer's scraped knuckle",
        ),
        (
            "missing_patient_soft_eyes",
            "A benevolent mamang-like maid with relaxed brow, reassuring mouth, and calm protective attention "
            "watches the adult customer's scraped knuckle",
        ),
        (
            "missing_reassuring_mouth",
            "A benevolent mamang-like maid with relaxed brow, patient soft eyes, and calm protective attention "
            "watches the adult customer's scraped knuckle",
        ),
        (
            "missing_protective_attention",
            "A benevolent mamang-like maid with relaxed brow, patient soft eyes, and reassuring mouth watches "
            "the adult customer's scraped knuckle",
        ),
        (
            "tsundere_romantic_leak_substitution",
            "A benevolent mamang-like maid with relaxed brow, patient soft eyes, reassuring mouth, and private "
            "liking lets her irises return mid-protest toward the adult customer's face",
        ),
    ]
    mutations = []
    for mutation_id, replacement in mutation_specs:
        mutated = copy.deepcopy(composed)
        mutated["prompt_en"] = mutated["prompt_en"].replace(original, replacement)
        mutated["moe_response"]["prompt_evidence"]["benevolent_affect_phrase"] = replacement
        result = audit_module.audit_composed_prompt(pack, mutated)
        checks = sorted(
            {
                str(row.get("check") or "")
                for row in result.get("failures") or []
                if isinstance(row, dict)
            }
        )
        required_check = "moe_response_benevolent_affect"
        if result.get("status") != "fail" or required_check not in checks:
            raise RuntimeError(
                f"mutation {mutation_id} did not fail through {required_check}: {checks}"
            )
        mutations.append(
            {
                "id": mutation_id,
                "status": result["status"],
                "required_check": required_check,
                "failure_checks": checks,
            }
        )
    MUTATION_PATH.write_text(
        json.dumps(
            {
                "contract_version": pack["moe_response"]["contract_version"],
                "pack_id": pack["pack_id"],
                "baseline_status": audit["status"],
                "mutations": mutations,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUTPUT_PATH)
    print(AUDIT_PATH)
    print(MUTATION_PATH)


if __name__ == "__main__":
    main()
