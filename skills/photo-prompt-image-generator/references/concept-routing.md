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

## Route Explicit Viewer Outcomes

At the agent layer, add `--viewer-experience` when the user explicitly asks for an audience reaction, emotion, empathy, immersion, attachment, reinspection, sharing or purchase behavior, a commercial communication objective, or a subculture character relationship. Korean cues include `독자`, `관객`, `감동`, `공감`, `몰입`, `애착`, `다시 보고 싶은`, `기억에 남는`, and `광고`; use semantic intent rather than keyword matching. Do not raise `--creativity` unless the request also asks for creative or authorial work.

Every high creative-direction run receives the viewer contract automatically. A generic product record, ordinary cute portrait, factual documentary, or subculture taxonomy request without an explicit viewer-response goal keeps the ordinary path. The control exposes a composition procedure, not a new preset, candidate, audience stereotype, or predicted performance score.

## Route Natural Character-Moe Requests

Natural KO/JA/EN phrases that explicitly request `모에`, `萌え`, `moe`, `갭모에`, `ギャップ萌え`, or a supported character-specific mechanism route to `character_moe_grammar` when the request describes an adult or otherwise valid character/photo context. They do not require a research alias or implementation phrase. The route adds both `moe_response` and `viewer_experience` because the requested outcome is a character response hypothesis.

Keep routing scoped. A merely cute portrait, animal photo, dictionary discussion such as “what does moe mean,” negated phrase such as “not moe,” unrelated word fragment, or generic streamer request must not activate the route. Parse multiword negative tone phrases such as `야하지 않은`, `性的ではない`, and `not sexual` as constraints; do not split their control words into positive `mandatory_intents`.

Treat adult age and sexual tone independently. Explicit nonsexual wording routes to `sexual_tone: nonsexual` and suppresses configured sensual/fetish defaults. A plain adult-moe request routes to `sexual_tone: sensual_optional` and keeps the eligible-human low-intensity `sensual_editorial=1`, `fetish_fashion=0` default as supporting appeal. Explicit adult sensual wording routes to `sexual_tone: sensual`. Sexual appeal may support adult moe, but it never substitutes for the pretty-and-cute character-design gate or the character-specific response.

Treat a pretty-and-cute adult character-design read as a required moe entry condition, not an optional embellishment. Explicit feminine presentation routes to adult bishoujo, explicit masculine presentation routes to adult bishonen, and explicit androgynous/nonbinary presentation is preserved as a beautiful-and-cute adult equivalent. Gender-unspecified explicit moe defaults locally to adult bishoujo; this default must not affect ordinary non-moe requests. Resolve this route before generic rule-mode preset and subject sampling, while preserving an explicit preset or a narrower role/mixin recipe. `Bishoujo` and `bishonen` name adult design categories here, never literal minor age.

Preserve requested roles and species layers. `네코미미`, `猫耳`, and `cat-eared` mean an otherwise human adult with compact living ears and ordinary human limbs. Explicit `수인`, `獣人`, `beastkin`, or broader kemonomimi wording may route to the full species-family contract. Do not let natural descriptive text become a named-person likeness reference.

## Route Request-Scoped Visual Obligations

Use `photo-visual-obligations/v1` for exact meanings whose success depends on pixels rather than a label: pose geometry, support/contact mechanics, multiple facial components that must coexist, intentional body-region salience, a transformation embodied on the character, or an archetype proven by behavior. Automatic hard activation uses only boundary-aware, non-negated direct terms or profile-local project glossary aliases from positive request sources and requires explicit adult context. A glossary alias activates only its owning profile and is expanded into that profile's composition instruction, evidence fields, substitute rejections, runtime-expression mode, and pixel gates. A direct `photo-visual-intent/v1` row may bind a requesting-user definition that the registry aliases cannot safely infer.

Use `photo-visual-concepts/v1` for indirect recognition. Each profile declares component groups and weak concept cues in data. Meeting the declared component threshold or one weak cue may expose one optional candidate, but can never create a hard duty. Candidate order and `concept_terms` are seed-shuffled and non-preferential; the pack omits matched cues, match kind, score, rank, and recommendation. The composer must explicitly provide `chosen_visual_concept_ids`, including `[]`. Selecting a candidate promotes its pre-baked opt-in obligation; leaving it unselected has no effect. This gives an indirect phrase a scoped influence without converting similarity into an automatic answer.

Keep the negative boundary stronger than resemblance. The user-established project glossary is an explicit, narrow exception: exact Korean `절대공역`, `사이갭`, and `사이 갭` own the `inner_thigh_negative_space` profile and therefore expand to close/adducted or crossed legs plus a real background opening bounded by upper inner-thigh contours. They must not remain unexplained fashion labels. Indirect geometry such as close knees plus a small inverted-triangle opening, or a weak cue such as attractive-thigh emphasis, produces only the optional candidate. This local mapping does not silently reinterpret conventional English/Japanese zettai-ryouiki fashion wording. An ordinary drink does not imply a balancing challenge; political/data/file corruption does not imply a character transition; an underarm garment seam does not imply body-region emphasis; black wardrobe or crystals do not imply embodied corruption; a hairstyle or compact face does not imply a haughty behavioral archetype; incidental visibility does not imply intentional body-region emphasis. Reference images provide identity and age-control evidence only, never personality activation. Do not copy an active profile to a later unrelated request.

Profiles expose composition fields and pixel gates, not a sampled answer or finished scene. The agent still authors the scene, but every active or selected duty and listed substitute rejection remains hard. `definition_only` profiles suppress sensitive shorthand and require component prose; `label_plus_definition` profiles require a safe English label plus full geometry; `definition_with_optional_label` profiles accept the component definition alone. Add or broaden a direct alias, component group, or soft cue only with development positives, adjacent hard negatives, and the separately frozen routing holdout.

## Route Hybrid Detail and Adult Fashion Appeal

The default skill workflow uses `--hybrid-augmentation` so the candidate pack can strengthen an agent-authored core instead of acting only as a validator. Direct CLI callers may opt in explicitly; high creative direction activates it automatically. Treat exposed routes as proposals, not instructions: select one or reject all, and use the marginal-value test before accepting a detail.

Eligible human candidate packs normally default `--sensual-editorial-intensity` to `1` and `--fetish-fashion-intensity` to `0`, with sensual-led emphasis. The axes remain independent; fetish fashion requires an explicit positive intensity, and passing `--sensual-editorial-intensity 0` disables the remaining default. Suppress the configured defaults for explicit nonsexual moe, no-people, and non-human requests. Do not map either axis from inferred gender, body, ethnicity, occupation, market, or predicted popularity.

Adult-appeal controls require candidate-pack composition. They expose a curated adult-fashion inventory derived from the adult editorial preset while keeping ordinary sampler provenance distinct. Preserve the user's larger concept as the governing idea; use sensual editorial for gaze, pose, lighting, framing, or silhouette, and fetish fashion for material, garment layering, accessories, or footwear.

## Preserve Negative Intent

Korean and English absence phrases are constraints, not positive nouns. `사람 없는`, `인물 없이`, `no people`, and `without people` must exclude human subject candidates and the `person_presence` quality axis. Preserve the full request in the mixed/excluded `intent_contract` row, but do not copy the absence phrase into positive `mandatory_intents`.

Named-person references are provenance for likeness handling, not visual content to force into the prompt. Public/idol routes use an original fictional adult with `--likeness-mode inspired`.

## Typed Request Routing

Subject intent is resolved to `human`, `animal`, `food`, `object`, `plant`, or `environment`; domain intent is resolved independently. Keep aliases in `photo_prompt_quality_layers.json` so Korean and English routes share one data contract. Negated aliases such as `not a portrait` must not activate the human category.

When a small curated `subject_routes` entry matches an explicit literal subject such as `cat` or `고양이`, narrow the rule-mode subject pool to that entry before category steering. Do not infer exact entries from role, soft, or negative recipe guidance, and remove human routes when `no_people` is active.

Literal secondary-subject inference uses entry IDs and labels but ignores the configured `literal_subject_stop_terms`. This prevents generated phrases such as `role`, `subject`, or `context` from turning a human request into an unrelated food or object scene.

Outside an exact curated subject route, an entry with a uniquely stronger explicit request-term match may win deterministically in rule mode without narrowing the candidate pack. The remaining alternatives must still come from the exact eligible sampler pool.

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

Do not force posters, UI, typography, webtoons, stickers, covers, card art, key visuals, or other non-photographic output through this skill. Route subculture illustration and artwork requests to `$subculture-illustration-image-generator` before adding photographic defaults.
