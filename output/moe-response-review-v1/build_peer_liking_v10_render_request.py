#!/usr/bin/env python3
"""Freeze and audit the exact v10 native image-tool input; do not render."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
PACK_PATH = CASE_DIR / "candidate_pack_peer_liking_v10.json"
COMPOSED_PATH = CASE_DIR / "composed_prompt_peer_liking_v10.json"
REQUEST_PATH = CASE_DIR / "render_request_peer_liking_v10.json"
IDENTITY_PATH = CASE_DIR.parent / "reference_identity" / "fictional_adult_reference.jpeg"
SCENE_PATH = CASE_DIR / "render_identity_control.png"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    payload = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    pack = payload[0] if isinstance(payload, list) else payload
    composed = json.loads(COMPOSED_PATH.read_text(encoding="utf-8"))
    positive = composed["prompt_en"]
    negative = pack["negative_en"]

    runtime_prompt = (
        "Use case: identity-preserving edit. Create exactly one photorealistic result.\n\n"
        "Reference roles:\n"
        "- Image 1 is the sole identity and adult-age source for the primary woman. Preserve her exact adult "
        "face geometry; it does not supply the secondary recipient landmark.\n"
        "- Image 2 supplies only the maid costume, body, hands, mid-bandaging action, warm cafe light, camera "
        "distance, framing, and restrained adult sensual level. It is not an additional identity source.\n\n"
        "Audited scene brief (preserve this block exactly):\n"
        f"{positive}\n\n"
        "Spatial disambiguation:\n"
        "- The primary woman's head and nose turn toward image-right in a natural three-quarter pose.\n"
        "- At the upper-left edge, show only a tiny, blurred sliver of the same adult recipient whose bandaged "
        "hand is below: one outer eye plus temple/profile edge, cropped and subordinate, never a full second face.\n"
        "- Only the primary woman's irises return upper-left toward that visible eye. Do not rotate her head left "
        "with her gaze, do not look into the lens, and do not make the recipient a second subject.\n"
        "- Keep her active pursed-lip protest. At second glance only, slightly soften the lower lids and let one "
        "mouth corner begin to rise before she suppresses it. The result is concealed peer liking, not an open "
        "smile, suspicious side-eye, or maternal benevolence.\n"
        "- Preserve Image 1 eye aperture/shape/spacing, face length, lower-face/jaw width, adult age, and natural "
        "asymmetry. Achieve pretty-and-cute appeal through micro-expression, grooming, light, and styling.\n"
        "- Preserve Image 2's covered costume, bandaging contact, human hands, small asymmetric living cat ears, "
        "framing, and appropriate low sensual support. Keep the background unlettered.\n\n"
        f"Avoid: {negative}"
    )

    request = {
        "schema_version": "photo-image-render-request/v2",
        "case_id": "ko_tsundere_nekomimi_maid",
        "pack_id": pack["pack_id"],
        "qualification": "v10_visible_recipient_landmark_preflight_only",
        "generator": "image_gen",
        "render_count": 0,
        "retry_count": 0,
        "runtime_prompt_en": runtime_prompt,
        "runtime_negative_en": negative,
        "references": [
            {
                "path": "../reference_identity/fictional_adult_reference.jpeg",
                "sha256": sha256_path(IDENTITY_PATH),
                "role": "sole_identity_and_adult_age_reference",
            },
            {
                "path": SCENE_PATH.name,
                "sha256": sha256_path(SCENE_PATH),
                "role": "scene_costume_pose_and_action_reference_only",
            },
        ],
        "audit_boundary": {
            "composed_prompt_audit_status": "pass",
            "runtime_prompt_audit_status": "not_run",
            "inherits_composed_prompt_pass": False,
            "explanation": (
                "The exact runtime prompt, negative bytes, and reference bytes require their own pre-render audit."
            ),
        },
        "status": "preflight_only_not_rendered",
    }
    REQUEST_PATH.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(REQUEST_PATH)


if __name__ == "__main__":
    main()
