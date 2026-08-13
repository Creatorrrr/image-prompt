#!/usr/bin/env python3
"""Build the unrendered v7 recipient-vector preflight from the preserved v6 evidence."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_recipient_vector_v7.json"
V6_PATH = CASE_DIR / "composed_prompt_concealed_affection_v6.json"
OUTPUT_PATH = CASE_DIR / "composed_prompt_recipient_vector_v7.json"

PROMPT_EN = (
    "Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait as sole "
    "identity: eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging. Customer's bandaged hand fills lower "
    "foreground, fixing near-lens POV. Cheek puffed, lips pursed mid-protest. Head stays aside; irises return toward "
    "the near-lens hand in a fond slip, lower lids soften, one mouth corner almost lifts before she stops it. Caught "
    "mid-bandaging, she holds the scraped knuckle; one wing stays lifted across an open gap. Compact cat ears, half "
    "human-ear height: near ear angles toward the hand; far ear keeps a different angle. Pad covers scrape; wing "
    "unfastened. Face, hands, maid apron, ears, bandage share one focal plane. Subtle adult allure. Plain unlettered bokeh."
)


def main() -> None:
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))[0]
    composed = json.loads(V6_PATH.read_text(encoding="utf-8"))
    composed["pack_id"] = pack["pack_id"]
    composed["prompt_en"] = PROMPT_EN
    composed["negative_en"] = pack["negative_en"]

    composed["coverage_assertions"] = {
        "성인": "Adult woman",
        "네코미미": "Compact cat ears",
        "츤데레": "Cheek puffed, lips pursed mid-protest",
        "메이드": "maid apron",
    }

    augmentation = copy.deepcopy(composed["augmentation_brief"])
    augmentation["concept_core"] = (
        "Preserve the fixed-identity v3 tsundere baseline while the customer's visible lower-foreground hand "
        "anchors a verifiable head-away, irises-returning affection vector; keep low adult allure subordinate."
    )
    augmentation["adult_appeal"]["adult_subject_phrase"] = "Adult woman"
    composed["augmentation_brief"] = augmentation

    response = copy.deepcopy(composed["moe_response"])
    response["trigger"] = "the customer's lower-foreground bandaged hand"
    response["target"] = "the visible near-lens customer hand and half-fastened bandage"
    response["visible_response"] = (
        "pursed protest, head-away iris return, softened lower lids, stopped mouth-corner lift, and unequal compact ears"
    )
    response["prompt_evidence"] = {
        "actor_phrase": "Adult woman",
        "aesthetic_baseline_phrase": "Adult woman, pretty and cute: refined face, lively eyes, glossy hair",
        "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
        "recipient_anchor_phrase": "Customer's bandaged hand fills lower foreground, fixing near-lens POV",
        "concealed_affection_phrase": (
            "Head stays aside; irises return toward the near-lens hand in a fond slip, lower lids soften, "
            "one mouth corner almost lifts before she stops it"
        ),
        "affective_leak_phrase": (
            "in a fond slip, lower lids soften, one mouth corner almost lifts before she stops it"
        ),
        "background_control_phrase": "Plain unlettered bokeh",
        "baseline_phrase": "Cheek puffed, lips pursed mid-protest",
        "event_phase_phrase": "Caught mid-bandaging",
        "trigger_phrase": "Customer's bandaged hand",
        "target_phrase": "one wing stays lifted across an open gap",
        "visible_response_phrase": (
            "Compact cat ears, half human-ear height: near ear angles toward the hand; "
            "far ear keeps a different angle"
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
                response["prompt_evidence"]["recipient_anchor_phrase"],
                response["prompt_evidence"]["concealed_affection_phrase"],
                "she holds the scraped knuckle",
                response["prompt_evidence"]["immediate_consequence_phrase"],
            ],
        },
    }

    viewer = copy.deepcopy(composed["viewer_experience"])
    viewer["viewer_promise"] = (
        "the same adult woman's head stays aside while her irises return to the customer's visible hand"
    )
    viewer["first_glance_hook"] = (
        "a pretty and cute adult maid protests while her irises return to the customer's visible hand"
    )
    viewer["interpretive_question"] = (
        "Why do her irises return to the customer's hand while her head keeps turning away?"
    )
    viewer["affect_evidence"] = {
        "actor": "the adult nekomimi maid",
        "action": "bandages the knuckle while stopping a mouth-corner lift",
        "target": "the visible lower-foreground customer hand",
        "consequence": "one tab stays open while her irises give away fondness",
    }
    viewer["reinspection_reward"]["description"] = (
        "head direction and iris direction separate around the same visible recipient anchor"
    )
    viewer["prompt_evidence"] = {
        "first_glance_hook_phrase": response["prompt_evidence"]["active_denial_phrase"],
        "affect_actor_phrase": "Adult woman",
        "affect_action_phrase": response["prompt_evidence"]["event_phase_phrase"],
        "affect_target_phrase": response["prompt_evidence"]["recipient_anchor_phrase"],
        "affect_consequence_phrase": response["prompt_evidence"]["immediate_consequence_phrase"],
        "attachment_phrase": response["prompt_evidence"]["concealed_affection_phrase"],
        "reinspection_reward_phrase": response["prompt_evidence"]["visible_response_phrase"],
    }
    composed["viewer_experience"] = viewer

    OUTPUT_PATH.write_text(
        json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
