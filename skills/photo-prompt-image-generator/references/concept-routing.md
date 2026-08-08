# Concept and Selection Routing

## Choose the Narrowest Input

- Exact preset requested: `--preset`.
- Free visual description: `--intent` in semantic mode.
- Literal meaning that must dominate: repeatable `--concept-lock`.
- Known short Korean role or mixin: repeatable `--concept`.
- Concrete unmatched visible detail: repeatable `--additional-requirement`.
- Exact dictionary choice: repeatable `--set slot=id`.

Do not use `--intent` with rule mode. Rule mode is deterministic weighted selection; semantic mode uses the local semantic index and API-backed query embedding.

## Route Explicit Creative Intent

At the agent layer, explicit requests for a creative, original, ingenious, inventive, surprising, or authorially distinctive result automatically set `--creativity 0.85` or higher. Korean triggers include `창의적`, `독창적`, `기발한`, `참신한`, `작가적`, and `작가의 터치`; interpret clear equivalents by meaning rather than requiring an exact keyword. This activates the generic `creative_direction` composition contract. Do not ask the user to repeat the request or add topic-specific candidates.

Requests for several safe variations or wider candidate exploration without an explicit originality/authorial goal may use a lower creativity value and remain outside creative direction. Ordinary prompt and image requests keep the default path.

## Preserve Negative Intent

Korean and English absence phrases are constraints, not positive nouns. `사람 없는`, `인물 없이`, `no people`, and `without people` must exclude human subject candidates and the `person_presence` quality axis. Keep the whole phrase as mandatory intent.

Named-person references are provenance for likeness handling, not visual content to force into the prompt. Public/idol routes use an original fictional adult with `--likeness-mode inspired`.

## Typed Request Routing

Subject intent is resolved to `human`, `animal`, `food`, `object`, `plant`, or `environment`; domain intent is resolved independently. Keep aliases in `photo_prompt_quality_layers.json` so Korean and English routes share one data contract. Negated aliases such as `not a portrait` must not activate the human category.

Literal secondary-subject inference uses entry IDs and labels but ignores the configured `literal_subject_stop_terms`. This prevents generated phrases such as `role`, `subject`, or `context` from turning a human request into an unrelated food or object scene.

In rule mode, an entry with a uniquely stronger explicit request-term match may win deterministically. This affects the sampled choice but does not narrow the candidate pack: the remaining alternatives must still come from the exact eligible sampler pool.

## Avoid Theme Overfitting

The selection balance layer reduces K-style, fantasy, robot, underwater, cosplay, and horror weights when the request does not mention those themes. Theme-specific supporting elements are also gated by primary scene context; robot, glitch, cosplay, beastkin, underwater, holographic, horror, surveillance, and field-only modifiers must not leak into unrelated candidates. Do not compensate by manually preferring any of these themes for a generic request.

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

Keep role-defining identity in `identity_core`. Put place, action, prop, light, composition, and time-specific examples in two or more weighted `scene_variants`. Selection is deterministic for a concept and seed. A selected variant is atomic: its scene slots use only that variant's local pools and may not borrow values from a sibling variant. Do not hardwire nationality or one mood unless it is part of the requested identity.

Use `anchor_pool` to keep all valid variant values reachable in soft mode. Use `critical_anchor_slots` only for meaning-bearing identity or role-scene evidence, not decorative defaults.

A standalone mixin may use only a role-free generic bundle. If every bundle is authored for a role, keep the mixin core and return no bundle rather than borrowing an unrelated role scene.

## Slot Mapping

- Subject identity: `subject`, `appearance_type`, `person_origin` only when requested.
- Clothes: `wardrobe_style`, `costume_style`, `footwear`, `silhouette_proportion`, `garment_detail`.
- Makeup: `skin_finish`, `brow_style`, `lip_finish`, `eye_makeup_line`, `eye_detail`; use `makeup_style` for full-look shorthand.
- Hair: `hair_style`, `hair_color`; preserve unsupported length, part, texture, finish, and cultural grammar as explicit requirements.
- Pose: `body_pose`, `hand_pose`, `gaze_engagement`, `shot_scale`, `camera_direction`, `composition`, `platform_framing`.
- Scene: `location`, `space_condition`, `crowd_density`, `situation_context`, `occasion_context`.
- Still life: `prop`, `surface_material`, `texture`, `light_shape`, `composition`, `aesthetic_trend`.

Do not force posters, UI, typography, webtoons, stickers, or other non-photographic output through this skill.
