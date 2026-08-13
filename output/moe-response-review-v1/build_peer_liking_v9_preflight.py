#!/usr/bin/env python3
"""Build the unrendered v9 fixed-identity tsundere preflight and mutations."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_peer_liking_v9.json"
BASE_PATH = CASE_DIR / "composed_prompt_peer_liking_v8.json"
OUTPUT_PATH = CASE_DIR / "composed_prompt_peer_liking_v9.json"
AUDIT_PATH = CASE_DIR / "composed_prompt_peer_liking_v9.audit.json"
MUTATION_PATH = CASE_DIR / "peer_liking_v9_mutation_audit.json"

PROMPT_EN = (
    "Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait: eye "
    "aperture/shape/spacing; nose, lips; face length, lower-face/jaw width; hairline, adult age. No enlarging, "
    "rounding, shortening, narrowing. Customer's bandaged hand fills lower foreground; same adult customer's "
    "off-axis face-level eye line stays upper-left. Cheek puffed, lips pursed mid-protest. Three-quarter head "
    "turns right; nose points right; only irises make a small oblique return upper-left. Private liking barely "
    "shows: lower lids soften; one mouth corner starts to lift, then flattens. Mid-bandaging, she holds scraped "
    "knuckle; one wing open. Human-ear-scale near ear turns toward hand; far ear keeps different angle. Pad "
    "covers scrape; wing unfastened. Face, hands, maid apron, bandage share one focal plane. Restrained allure. "
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
    spec = importlib.util.spec_from_file_location("photo_prompt_audit_v9", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load audit module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    payload = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    pack = payload[0] if isinstance(payload, list) else payload
    composed = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    composed["pack_id"] = pack["pack_id"]
    composed["prompt_en"] = PROMPT_EN
    composed["negative_en"] = pack["negative_en"]
    composed["coverage_assertions"] = {
        "성인": "Adult woman",
        "네코미미": "Human-ear-scale near ear",
        "츤데레": "Cheek puffed, lips pursed mid-protest",
        "메이드": "maid apron",
    }

    augmentation = copy.deepcopy(composed["augmentation_brief"])
    augmentation["concept_core"] = (
        "Keep the fixed-identity v3 costume, event, and approved low adult allure while making concealed peer "
        "liking off-axis and preserving the source face proportions as hard gates."
    )
    augmentation["adult_appeal"]["adult_subject_phrase"] = "Adult woman"
    augmentation["adult_appeal"]["agency_phrase"] = "she holds scraped knuckle"
    for decision in augmentation["decisions"]:
        if decision.get("candidate_id") == (
            "augmentation:adult_appeal:sensual_editorial:action:posing_editorial"
        ):
            decision["prompt_evidence"] = "Restrained allure"
    composed["augmentation_brief"] = augmentation

    response = copy.deepcopy(composed["moe_response"])
    response["relationship_register"] = "peer_liking_under_denial"
    response["baseline"] = "puffed-cheek, pursed-lip guarded service"
    response["event_phase"] = "mid-bandaging before completion"
    response["trigger"] = "the customer's lower-foreground bandaged hand"
    response["target"] = "the visible customer hand and open bandage wing"
    response["visible_response"] = (
        "active protest, three-quarter head-away geometry, a small oblique iris return, two suppressed warm "
        "microcues, and a trigger-directed compact ear"
    )
    response["immediate_consequence"] = (
        "the pad covers the scrape while one bandage wing remains unfastened"
    )
    response["continuity"] = (
        "the uploaded adult identity, facial proportions, human hands, maid role, and living ears remain stable"
    )
    response["prompt_evidence"] = {
        "actor_phrase": "Adult woman",
        "aesthetic_baseline_phrase": (
            "Adult woman, pretty and cute: refined face, lively eyes, glossy hair"
        ),
        "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
        "care_action_anchor_phrase": "Customer's bandaged hand fills lower foreground",
        "relationship_gaze_anchor_phrase": (
            "same adult customer's off-axis face-level eye line stays upper-left"
        ),
        "concealed_affection_phrase": (
            "Three-quarter head turns right; nose points right; only irises make a small oblique return "
            "upper-left. Private liking barely shows: lower lids soften; one mouth corner starts to lift, "
            "then flattens"
        ),
        "affective_leak_phrase": (
            "Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens"
        ),
        "background_control_phrase": "Unlettered bokeh",
        "baseline_phrase": "Cheek puffed, lips pursed mid-protest",
        "event_phase_phrase": "Mid-bandaging",
        "trigger_phrase": "Customer's bandaged hand",
        "target_phrase": "one wing open",
        "visible_response_phrase": (
            "Human-ear-scale near ear turns toward hand; far ear keeps different angle"
        ),
        "immediate_consequence_phrase": "Pad covers scrape; wing unfastened",
        "continuity_phrase": "Face, hands, maid apron, bandage",
        "focal_plane_phrase": "Face, hands, maid apron, bandage share one focal plane",
        "reference_identity_phrase": (
            "Preserve uploaded portrait: eye aperture/shape/spacing; nose, lips; face length, lower-face/jaw "
            "width; hairline, adult age. No enlarging, rounding, shortening, narrowing"
        ),
    }
    composed["moe_response"] = response

    composed["manual_gate_evidence"] = {
        "nekomimi_living_ear_test": {
            "review_stage": "pixel_review_required",
            "evidence_phrases": [
                response["prompt_evidence"]["visible_response_phrase"],
                response["prompt_evidence"]["continuity_phrase"],
            ],
        },
        "contradiction_in_frame": {
            "review_stage": "pixel_review_required",
            "evidence_phrases": [
                response["prompt_evidence"]["active_denial_phrase"],
                response["prompt_evidence"]["care_action_anchor_phrase"],
                response["prompt_evidence"]["relationship_gaze_anchor_phrase"],
                response["prompt_evidence"]["concealed_affection_phrase"],
                "she holds scraped knuckle",
                response["prompt_evidence"]["immediate_consequence_phrase"],
            ],
        },
    }

    viewer = copy.deepcopy(composed["viewer_experience"])
    viewer["viewer_promise"] = (
        "the preserved adult woman's hands tend the injury while an oblique glance almost gives away peer liking"
    )
    viewer["first_glance_hook"] = (
        "a pretty and cute adult maid actively protests while two tiny warm cues nearly escape"
    )
    viewer["interpretive_question"] = (
        "Why do only her irises return upper-left while her nose and head remain turned away?"
    )
    viewer["affect_evidence"] = {
        "actor": "the preserved adult nekomimi maid",
        "action": "bandages the knuckle while flattening a starting smile",
        "target": "the adult recipient whose hand and face-level eye line are separate",
        "consequence": "one tab stays open while the oblique iris return leaks private liking",
    }
    viewer["reinspection_reward"]["description"] = (
        "the head and nose remain off-lens while only the irises return to the recipient"
    )
    viewer["prompt_evidence"] = {
        "first_glance_hook_phrase": response["prompt_evidence"]["active_denial_phrase"],
        "affect_actor_phrase": "Adult woman",
        "affect_action_phrase": response["prompt_evidence"]["event_phase_phrase"],
        "affect_target_phrase": response["prompt_evidence"]["care_action_anchor_phrase"],
        "affect_consequence_phrase": response["prompt_evidence"]["immediate_consequence_phrase"],
        "attachment_phrase": response["prompt_evidence"]["concealed_affection_phrase"],
        "reinspection_reward_phrase": response["prompt_evidence"][
            "relationship_gaze_anchor_phrase"
        ],
    }
    composed["viewer_experience"] = viewer

    audit_module = load_audit_module()
    if audit_module.english_prompt_word_count(PROMPT_EN) != 120:
        raise RuntimeError("v9 fixed-identity prompt must remain exactly at its verified 120-word boundary")
    audit = audit_module.audit_composed_prompt(pack, composed)
    if audit.get("status") != "pass":
        raise RuntimeError(f"v9 preflight failed: {audit.get('failures')}")
    OUTPUT_PATH.write_text(
        json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    AUDIT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    evidence = composed["moe_response"]["prompt_evidence"]
    mutation_specs = [
        (
            "direct_frontal_eye_contact",
            "concealed_affection_phrase",
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left "
            "with direct frontal eye contact. Private liking barely shows: lower lids soften; one mouth corner "
            "starts to lift, then flattens",
            "moe_response_concealed_affection",
        ),
        (
            "generic_head_aside_without_three_quarter_geometry",
            "concealed_affection_phrase",
            "Head stays aside; irises return upper-left. Private liking barely shows: lower lids soften; one "
            "mouth corner starts to lift, then flattens",
            "moe_response_concealed_affection",
        ),
        (
            "lower_lid_only_without_mouth_leak",
            "concealed_affection_phrase",
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left. "
            "Private liking barely shows as lower lids soften before suppression",
            "moe_response_concealed_affection",
        ),
        (
            "mouth_leak_only_without_lower_lids",
            "concealed_affection_phrase",
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left. "
            "Private liking barely shows as one mouth corner starts to lift, then flattens",
            "moe_response_concealed_affection",
        ),
        (
            "weak_identity_anchors",
            "reference_identity_phrase",
            "Preserve uploaded portrait identity: eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging",
            "moe_response_reference_identity",
        ),
        (
            "collapsed_hand_as_relationship_anchor",
            "relationship_gaze_anchor_phrase",
            "same adult customer's hand stays visible in the lower foreground",
            "moe_response_relationship_gaze_anchor",
        ),
    ]
    mutations = []
    for mutation_id, field, replacement, required_check in mutation_specs:
        mutated = copy.deepcopy(composed)
        original = str(evidence[field])
        mutated["prompt_en"] = mutated["prompt_en"].replace(original, replacement)
        mutated["moe_response"]["prompt_evidence"][field] = replacement
        result = audit_module.audit_composed_prompt(pack, mutated)
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
                "prompt_word_count": audit_module.english_prompt_word_count(PROMPT_EN),
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
