#!/usr/bin/env python3
"""Build the unrendered v8 peer-liking preflight from preserved fixed-identity evidence."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_peer_liking_v8.json"
V7_PATH = CASE_DIR / "composed_prompt_recipient_vector_v7.json"
OUTPUT_PATH = CASE_DIR / "composed_prompt_peer_liking_v8.json"
AUDIT_PATH = CASE_DIR / "composed_prompt_peer_liking_v8.audit.json"
MUTATION_PATH = CASE_DIR / "peer_liking_v8_mutation_audit.json"

PROMPT_EN = (
    "Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait as sole "
    "identity: eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging. Customer's bandaged hand fills lower "
    "foreground; the same adult customer's face-level near-lens eye line stays above. Cheek puffed, lips pursed "
    "mid-protest. Head stays aside; irises return to that face-level eye line, a barely visible flash of private "
    "liking softens lower lids before she stops an almost-smile. Caught mid-bandaging, she holds scraped knuckle; "
    "one wing stays open. Compact cat ears, half human-ear height: near ear turns toward hand; far ear keeps another angle. "
    "Pad covers scrape; wing unfastened. Face, hands, maid apron, ears, bandage share one focal plane. "
    "Subtle adult allure. Plain unlettered bokeh."
)


def main() -> None:
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))[0]
    composed = json.loads(V7_PATH.read_text(encoding="utf-8"))
    composed["pack_id"] = pack["pack_id"]
    composed["prompt_en"] = PROMPT_EN
    composed["negative_en"] = pack["negative_en"]

    composed["coverage_assertions"] = {
        "성인": "Adult woman",
        "네코미미": "Compact cat ears",
        "츤데레": "Cheek puffed, lips pursed mid-protest",
        "메이드": "apron",
    }

    augmentation = copy.deepcopy(composed["augmentation_brief"])
    augmentation["concept_core"] = (
        "Preserve the fixed-identity v3 tsundere baseline while separating the lower care target from the "
        "same adult recipient's face-level eye line; keep low adult allure subordinate."
    )
    augmentation["adult_appeal"]["adult_subject_phrase"] = "Adult woman"
    augmentation["adult_appeal"]["agency_phrase"] = "she holds scraped knuckle"
    composed["augmentation_brief"] = augmentation

    response = copy.deepcopy(composed["moe_response"])
    response["relationship_register"] = "peer_liking_under_denial"
    response["trigger"] = "the customer's lower-foreground bandaged hand"
    response["target"] = "the visible customer hand and half-fastened bandage"
    response["visible_response"] = (
        "pursed protest, head-away iris return to a separate face-level eye line, suppressed private liking, "
        "and unequal compact ears"
    )
    response["prompt_evidence"] = {
        "actor_phrase": "Adult woman",
        "aesthetic_baseline_phrase": "Adult woman, pretty and cute: refined face, lively eyes, glossy hair",
        "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
        "care_action_anchor_phrase": "Customer's bandaged hand fills lower foreground",
        "relationship_gaze_anchor_phrase": (
            "the same adult customer's face-level near-lens eye line stays above"
        ),
        "concealed_affection_phrase": (
            "Head stays aside; irises return to that face-level eye line, a barely visible flash of private "
            "liking softens lower lids before she stops an almost-smile"
        ),
        "affective_leak_phrase": (
            "a barely visible flash of private liking softens lower lids before she stops an almost-smile"
        ),
        "background_control_phrase": "Plain unlettered bokeh",
        "baseline_phrase": "Cheek puffed, lips pursed mid-protest",
        "event_phase_phrase": "Caught mid-bandaging",
        "trigger_phrase": "Customer's bandaged hand",
        "target_phrase": "one wing stays open",
        "visible_response_phrase": (
            "Compact cat ears, half human-ear height: near ear turns toward hand; far ear keeps another angle"
        ),
        "immediate_consequence_phrase": "Pad covers scrape; wing unfastened",
        "continuity_phrase": "Face, hands, maid apron, ears, bandage",
        "focal_plane_phrase": "Face, hands, maid apron, ears, bandage share one focal plane",
        "reference_identity_phrase": (
            "Preserve uploaded portrait as sole identity: eyes, nose, lips, jaw, skin, hairline, "
            "adult age; no de-aging"
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
        "the same adult woman's hands tend the injury while her eyes leak private liking toward the adult recipient"
    )
    viewer["first_glance_hook"] = (
        "a pretty and cute adult maid protests while her eyes betray whom she personally likes"
    )
    viewer["interpretive_question"] = (
        "Why do her irises return to the recipient's face-level eye line instead of the injury she is tending?"
    )
    viewer["affect_evidence"] = {
        "actor": "the adult nekomimi maid",
        "action": "bandages the knuckle while suppressing an almost-smile",
        "target": "the adult recipient whose hand and eye line occupy separate anchors",
        "consequence": "one tab stays open while her irises give away private liking",
    }
    viewer["reinspection_reward"]["description"] = (
        "the hands remain on the care target while the irises return to a higher relationship anchor"
    )
    viewer["prompt_evidence"] = {
        "first_glance_hook_phrase": response["prompt_evidence"]["active_denial_phrase"],
        "affect_actor_phrase": "Adult woman",
        "affect_action_phrase": response["prompt_evidence"]["event_phase_phrase"],
        "affect_target_phrase": response["prompt_evidence"]["care_action_anchor_phrase"],
        "affect_consequence_phrase": response["prompt_evidence"]["immediate_consequence_phrase"],
        "attachment_phrase": response["prompt_evidence"]["concealed_affection_phrase"],
        "reinspection_reward_phrase": response["prompt_evidence"]["relationship_gaze_anchor_phrase"],
    }
    composed["viewer_experience"] = viewer

    OUTPUT_PATH.write_text(
        json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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
    audit_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_module)
    audit = audit_module.audit_composed_prompt(pack, composed)
    AUDIT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if audit.get("status") != "pass":
        raise RuntimeError(f"v8 preflight failed: {audit.get('failures')}")

    evidence = composed["moe_response"]["prompt_evidence"]
    mutation_specs = [
        (
            "collapsed_hand_as_relationship_anchor",
            "relationship_gaze_anchor_phrase",
            "the same adult customer's hand stays visible in the lower foreground",
            "moe_response_relationship_gaze_anchor",
        ),
        (
            "gaze_returns_to_care_hand",
            "concealed_affection_phrase",
            "Head stays aside; irises return toward the hand, a barely visible flash of private liking "
            "softens lower lids before she stops an almost-smile",
            "moe_response_concealed_affection",
        ),
        (
            "maternal_benevolence_substitutes_for_tsundere_liking",
            "concealed_affection_phrase",
            "Head stays aside; irises return to that face-level eye line, benevolent maternal warmth "
            "softens lower lids before she stops an almost-smile",
            "moe_response_concealed_affection",
        ),
        (
            "generic_side_eye",
            "concealed_affection_phrase",
            "A brief side-eye betrays private liking toward the customer before she suppresses an almost-smile",
            "moe_response_concealed_affection",
        ),
        (
            "off_frame_relationship_face",
            "relationship_gaze_anchor_phrase",
            "the same adult customer's face-level eyes stay off-frame above",
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
