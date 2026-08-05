# Concept and Selection Routing

## Choose the Narrowest Input

- Exact preset requested: `--preset`.
- Free visual description: `--intent` in semantic mode.
- Literal meaning that must dominate: repeatable `--concept-lock`.
- Known short Korean role or mixin: repeatable `--concept`.
- Concrete unmatched visible detail: repeatable `--additional-requirement`.
- Exact dictionary choice: repeatable `--set slot=id`.

Do not use `--intent` with rule mode. Rule mode is deterministic weighted selection; semantic mode uses the local semantic index and API-backed query embedding.

## Preserve Negative Intent

Korean and English absence phrases are constraints, not positive nouns. `사람 없는`, `인물 없이`, `no people`, and `without people` must exclude human subject candidates and the `person_presence` quality axis. Keep the whole phrase as mandatory intent.

Named-person references are provenance for likeness handling, not visual content to force into the prompt. Public/idol routes use an original fictional adult with `--likeness-mode inspired`.

## Avoid Theme Overfitting

The selection balance layer reduces K-style and fantasy weights when the request does not mention those themes. Do not compensate by manually preferring idol, K-beauty, cosplay, fairy, vampire, princess, or beastkin candidates for a generic portrait.

Presets and slot entries must have moderate positive weights. The validator rejects values above 5 and presets without a non-empty `required_slots` contract.

## Recipe Structure

Prefer this structure for reusable roles:

```json
{
  "identity_core": {
    "subject": "role_subject",
    "wardrobe_style": "role_wardrobe"
  },
  "scene_variants": [
    {"id": "task_a", "weight": 1, "set": {"location": "place_a", "action": "action_a"}},
    {"id": "task_b", "weight": 1, "set": {"location": "place_b", "action": "action_b"}}
  ]
}
```

Keep role-defining identity in `identity_core`. Put place, action, prop, light, composition, and time-specific examples in two or more weighted `scene_variants`. Selection is deterministic for a concept and seed. Do not hardwire nationality or one mood unless it is part of the requested identity.

Use `anchor_pool` to keep all valid variant values reachable in soft mode. Use `critical_anchor_slots` only for meaning-bearing identity or role-scene evidence, not decorative defaults.

## Slot Mapping

- Subject identity: `subject`, `appearance_type`, `person_origin` only when requested.
- Clothes: `wardrobe_style`, `costume_style`, `footwear`, `silhouette_proportion`, `garment_detail`.
- Makeup: `skin_finish`, `brow_style`, `lip_finish`, `eye_makeup_line`, `eye_detail`; use `makeup_style` for full-look shorthand.
- Hair: `hair_style`, `hair_color`; preserve unsupported length, part, texture, finish, and cultural grammar as explicit requirements.
- Pose: `body_pose`, `hand_pose`, `gaze_engagement`, `shot_scale`, `camera_direction`, `composition`, `platform_framing`.
- Scene: `location`, `space_condition`, `crowd_density`, `situation_context`, `occasion_context`.
- Still life: `prop`, `surface_material`, `texture`, `light_shape`, `composition`, `aesthetic_trend`.

Do not force posters, UI, typography, webtoons, stickers, or other non-photographic output through this skill.
