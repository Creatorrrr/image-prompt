#!/usr/bin/env python3
"""Build the unrendered v10 fixed-identity tsundere preflight and mutations."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_peer_liking_v10.json"
BASE_PATH = CASE_DIR / "composed_prompt_peer_liking_v9.json"
OUTPUT_PATH = CASE_DIR / "composed_prompt_peer_liking_v10.json"
AUDIT_PATH = CASE_DIR / "composed_prompt_peer_liking_v10.audit.json"
MUTATION_PATH = CASE_DIR / "peer_liking_v10_mutation_audit.json"

PROMPT_EN = (
    "Pretty, cute adult woman: refined face, lively eyes. Preserve uploaded portrait: eye "
    "aperture/shape/spacing; nose, lips; face length, lower-face/jaw width; adult age. No enlarging, "
    "rounding, shortening, narrowing. Customer's bandaged hand fills lower foreground; same adult customer's "
    "blurred outer eye and temple sliver stays upper-left. Cheek puffed, lips pursed mid-protest. Three-quarter head "
    "turns right; nose points right; only irises make small oblique return upper-left. Private liking barely "
    "shows: lower lids soften; one mouth corner starts lifting, then flattens. Mid-bandaging, she holds "
    "knuckle; wing open. Human-ear-scale near ear turns toward hand; far ear keeps different angle. Pad "
    "covers scrape; wing unfastened. Face, hands, maid apron, bandage share one focal plane under shared light from cafe lamps. Restrained allure. "
    "Unlettered bokeh."
)


def load_audit_module():
    module_path = (
        ROOT
        / "skills"
        / "photo-prompt-image-generator"
        / "scripts"
        / "audit_composed_prompt.py"
    )
    spec = importlib.util.spec_from_file_location("photo_prompt_audit_v10", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load audit module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mutation_result(audit_module, pack, composed, field, replacement):
    mutated = copy.deepcopy(composed)
    original = str(composed["moe_response"]["prompt_evidence"][field])
    mutated["prompt_en"] = mutated["prompt_en"].replace(original, replacement)
    mutated["moe_response"]["prompt_evidence"][field] = replacement
    return audit_module.audit_composed_prompt(pack, mutated)


def main() -> None:
    payload = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    pack = payload[0] if isinstance(payload, list) else payload
    composed = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    composed["pack_id"] = pack["pack_id"]
    composed["prompt_en"] = PROMPT_EN
    composed["negative_en"] = pack["negative_en"]

    evidence = {
        "actor_phrase": "Adult woman",
        "aesthetic_baseline_phrase": (
            "Pretty, cute adult woman: refined face, lively eyes"
        ),
        "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
        "care_action_anchor_phrase": "Customer's bandaged hand fills lower foreground",
        "relationship_gaze_anchor_phrase": (
            "same adult customer's blurred outer eye and temple sliver stays upper-left"
        ),
        "concealed_affection_phrase": (
            "Three-quarter head turns right; nose points right; only irises make small oblique return "
            "upper-left. Private liking barely shows: lower lids soften; one mouth corner starts lifting, "
            "then flattens"
        ),
        "affective_leak_phrase": (
            "Private liking barely shows: lower lids soften; one mouth corner starts lifting, then flattens"
        ),
        "background_control_phrase": "Unlettered bokeh",
        "baseline_phrase": "Cheek puffed, lips pursed mid-protest",
        "event_phase_phrase": "Mid-bandaging",
        "trigger_phrase": "Customer's bandaged hand",
        "target_phrase": "wing open",
        "visible_response_phrase": (
            "Human-ear-scale near ear turns toward hand; far ear keeps different angle"
        ),
        "immediate_consequence_phrase": "Pad covers scrape; wing unfastened",
        "continuity_phrase": "Face, hands, maid apron, bandage",
        "focal_plane_phrase": (
            "Face, hands, maid apron, bandage share one focal plane under shared light from cafe lamps"
        ),
        "reference_identity_phrase": (
            "Preserve uploaded portrait: eye aperture/shape/spacing; nose, lips; face length, lower-face/jaw "
            "width; adult age. No enlarging, rounding, shortening, narrowing"
        ),
    }

    response = copy.deepcopy(composed["moe_response"])
    response["relationship_register"] = "peer_liking_under_denial"
    response["baseline"] = "puffed-cheek, pursed-lip guarded service"
    response["event_phase"] = "mid-bandaging before completion"
    response["trigger"] = "the customer's lower-foreground bandaged hand"
    response["target"] = "the visible customer hand and open bandage wing"
    response["visible_response"] = (
        "active protest, a head-away versus iris-return vector to a visible partial recipient landmark, "
        "two suppressed warm microcues, and a trigger-directed compact ear"
    )
    response["immediate_consequence"] = (
        "the pad covers the scrape while one bandage wing remains unfastened"
    )
    response["continuity"] = (
        "the uploaded adult identity, facial proportions, human hands, maid role, and living ears remain stable"
    )
    response["prompt_evidence"] = evidence
    composed["moe_response"] = response

    augmentation = copy.deepcopy(composed["augmentation_brief"])
    augmentation["concept_core"] = (
        "Keep the fixed-identity v3 costume, bandaging event, and approved low adult allure while making "
        "concealed peer liking verifiable through a subordinate partial-recipient landmark."
    )
    augmentation["adult_appeal"]["adult_subject_phrase"] = "Adult woman"
    augmentation["adult_appeal"]["agency_phrase"] = "she holds knuckle"
    for decision in augmentation["decisions"]:
        if decision.get("candidate_id") == (
            "augmentation:adult_appeal:sensual_editorial:action:posing_editorial"
        ):
            decision["prompt_evidence"] = "Restrained allure"
    composed["augmentation_brief"] = augmentation

    composed["manual_gate_evidence"] = {
        "nekomimi_living_ear_test": {
            "review_stage": "pixel_review_required",
            "evidence_phrases": [
                evidence["visible_response_phrase"],
                evidence["continuity_phrase"],
            ],
        },
        "contradiction_in_frame": {
            "review_stage": "pixel_review_required",
            "evidence_phrases": [
                evidence["active_denial_phrase"],
                evidence["care_action_anchor_phrase"],
                evidence["relationship_gaze_anchor_phrase"],
                evidence["concealed_affection_phrase"],
                "she holds knuckle",
                evidence["immediate_consequence_phrase"],
            ],
        },
    }

    viewer = copy.deepcopy(composed["viewer_experience"])
    viewer["viewer_promise"] = (
        "the preserved adult woman's hands tend the injury while an opposite-vector glance almost gives away peer liking"
    )
    viewer["first_glance_hook"] = (
        "a pretty and cute adult maid protests while two tiny warm cues nearly escape"
    )
    viewer["interpretive_question"] = (
        "Why do her head and nose turn right while only her irises return to the recipient's partial face at upper-left?"
    )
    viewer["affect_evidence"] = {
        "actor": "the preserved adult nekomimi maid",
        "action": "bandages the knuckle while flattening a starting smile",
        "target": "the adult recipient whose hand and blurred partial face occupy separate anchors",
        "consequence": "one tab stays open while the opposite iris return leaks private liking",
    }
    viewer["reinspection_reward"]["description"] = (
        "the head and nose turn away from the visible partial recipient landmark while only the irises return"
    )
    viewer["prompt_evidence"] = {
        "first_glance_hook_phrase": evidence["active_denial_phrase"],
        "affect_actor_phrase": "Adult woman",
        "affect_action_phrase": evidence["event_phase_phrase"],
        "affect_target_phrase": evidence["care_action_anchor_phrase"],
        "affect_consequence_phrase": evidence["immediate_consequence_phrase"],
        "attachment_phrase": evidence["concealed_affection_phrase"],
        "reinspection_reward_phrase": evidence["relationship_gaze_anchor_phrase"],
    }
    composed["viewer_experience"] = viewer

    audit_module = load_audit_module()
    word_count = audit_module.english_prompt_word_count(PROMPT_EN)
    if word_count != 120:
        raise RuntimeError(f"v10 fixed-identity prompt must be 120 words, got {word_count}")
    audit = audit_module.audit_composed_prompt(pack, composed)
    if audit.get("status") != "pass":
        raise RuntimeError(f"v10 preflight failed: {audit.get('failures')}")

    OUTPUT_PATH.write_text(
        json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    AUDIT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mutation_specs = [
        (
            "imagined_off_axis_eye_line_without_visible_recipient_landmark",
            "relationship_gaze_anchor_phrase",
            "same adult customer's off-axis face-level eye line stays upper-left",
            "moe_response_partial_recipient_landmark",
        ),
        (
            "second_full_recipient_face",
            "relationship_gaze_anchor_phrase",
            "same adult customer's blurred second full recipient face stays upper-left",
            "moe_response_partial_recipient_landmark",
        ),
        (
            "head_and_irises_turn_together_left",
            "concealed_affection_phrase",
            "Three-quarter head turns left; nose points left; only irises make a small oblique return upper-left. "
            "Private liking barely shows: lower lids soften; one mouth corner starts lifting, then flattens",
            "moe_response_opposed_head_iris_vector",
        ),
        (
            "iris_return_misses_visible_recipient_landmark",
            "concealed_affection_phrase",
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-right. "
            "Private liking barely shows: lower lids soften; one mouth corner starts lifting, then flattens",
            "moe_response_opposed_head_iris_vector",
        ),
    ]
    mutations = []
    for mutation_id, field, replacement, required_check in mutation_specs:
        result = mutation_result(audit_module, pack, composed, field, replacement)
        checks = sorted(
            {
                str(row.get("check") or "")
                for row in result.get("failures") or []
                if isinstance(row, dict)
            }
        )
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
                "prompt_word_count": word_count,
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
