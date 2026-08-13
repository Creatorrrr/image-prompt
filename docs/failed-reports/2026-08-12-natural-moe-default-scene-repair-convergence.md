# Natural moe default scene still converged on repair and coworker work

- Recorded: 2026-08-12 22:26 KST
- Status: resolved
- Resolved: 2026-08-13 07:00 KST
- Goal/checkpoint: explicit adult-bishonen branch pixel qualification
- Affected scope: `photo-prompt-image-generator` natural-language moe scene selection for `character_attribute_composition_scene`
- Search terms: natural moe default, adult bishonen, repair convergence, coworker scene, selected render blueprint
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_scene_expression_character_moe.json`, `tests/fixtures/photo_prompt/natural_moe_response_contract_v1.jsonl`, `output/moe-response-review-v1/ko_explicit_male_bishonen/candidate_pack_aesthetic_contract.json`
- Related passed reports: `docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`

## Failure

- Conditions or trigger: Generate one rule-mode v3 candidate pack with seed `20260816` for the frozen natural request `야하지 않은 성인 남자 캐릭터를 미소년 계열로 모에하게`.
- Expected: Preserve `adult_bishonen`, nonsexual tone, and one character-specific causal event without inventing a profession, repair task, or coworker relationship.
- Observed: Pack `78114253e06888c3` correctly routed to `adult_bishonen`, but its selected subject was an adult night repairer and coworker; its action, location, and prop were a strap repair, maintenance bench, and stitched tool strap.
- Impact on the goal: The male aesthetic branch cannot be honestly rendered as evidence of generic natural-language moe because the scene still depends on the exact work/repair/coworker pattern the user asked the skill to avoid.

### Regression found during v10 completion audit (2026-08-13)

- Conditions or trigger: Generate a candidate pack without `--preset` from natural paraphrases that route to `character_gap_contrast_scene` or `character_nonhuman_expression_scene`, including Japanese adult-bishonen gap moe and English/Korean adult nekomimi moe.
- Expected: The resolved natural route should select a compatible scene and emit a pack without requiring the caller to know or pass an internal preset.
- Observed: The wrapper exits with `Preset '<route>' has no everyday render scene for its natural moe route`. The generic `character_attribute_composition_scene` route works because it owns `natural_moe_default_only` scenes, but the same default-only restriction is applied to other natural moe routes that do not own those markers.
- Impact on the goal: Current frozen intent-resolution tests overstate multilingual natural-language support; actual end-to-end wrapper generation fails for valid gap and nekomimi paraphrases.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: deterministic candidate pack at `output/moe-response-review-v1/ko_explicit_male_bishonen/candidate_pack_aesthetic_contract.json`.
- Result: `moe_response.aesthetic_baseline=adult_bishonen` and `sexual_tone=nonsexual`, while `render_contract.selected_scene.blueprint_id=moe_attribute_composition_graph_atomic_01` and all four scene atoms encode maintenance work with a coworker.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed. The generic natural moe route reuses a research preset whose four authored blueprints contain three night-repair/coworker scenes and one private everyday scene. With no role-specific request relevance, deterministic seed cycling still exposes the repair majority.
- Confidence: confirmed
- Remaining unknowns: Whether a bounded default-only everyday scene pool will remain visually legible after composition and rendering.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Pre-sample natural moe preset routing | Correctly prevented the earlier elderly-commuter subject leak and produced `adult_bishonen` | It constrained the preset but did not distinguish generic natural requests from the preset's research-specific repair exemplars |
| Apply the generic route's `natural_moe_default_only` filter to every natural moe route | Generic adult moe avoids repair convergence | Valid gap-moe and nekomimi routes have no scenes carrying that marker and fail before pack creation |

## Resolution or next safe step

- Resolution/workaround: The original generic-route repair remains valid: `character_attribute_composition_scene` is restricted to its explicitly marked everyday scenes while direct preset replay retains the original authored research scenes. Natural-route scene selection now first prefers a default whose declared relationship register matches the resolved response, then an unscoped natural default. Gap and nonhuman routes own bounded everyday defaults, including a default-only peer-liking-under-denial scene. Roleless natural moe bypasses legacy mixin preset affinity so a `츤데레` styling recipe cannot replace the mechanism route with `candid_iphone_portrait`; explicit roles such as maid still retain their role preset.
- Verification: Four end-to-end, no-`--preset` KO/JA/EN paraphrases now materialize the expected gap or nonhuman scene, adult-bishoujo/bishonen/androgynous baseline, relationship register, and sexual tone, with no technician/repair/coworker/maintenance/shift leakage. Focused surrounding regressions pass 8/8. A later completion sweep promoted all 32 frozen natural-language cases to public-wrapper materialization and passes 32/32, including 25 positive contracts and seven hard-negative exclusions. The complete affected suites pass 335/335 (`test_photo_prompt_contract_v2` 59/59 and `test_prompt_generator` 276/276); direct research-preset replay still cycles only its four frozen scenes. Dictionary metadata, scene-expression 112/112, contradiction 2,001/0, generalization 79/79, holdout 24/24, domain holdout 6/6, and retrieval holdout 22/22 pass.

## Reuse guidance

- Avoid: Treating a correct aesthetic contract as proof that the scene respects a generic request, or hiding convergence by cherry-picking a seed.
- Prefer: Separate role-specific research exemplars from a small default-only natural-language scene pool and apply it only when request relevance does not justify a narrower role scene.
- Applicable when: A broad natural-language route shares a preset with strongly authored profession or relationship exemplars.
- Re-check when: Natural moe routing, blueprint scoring, default-scene markers, or the character scene corpus changes. Include end-to-end no-`--preset` KO/JA/EN gap and nonhuman paraphrases, not only intent-resolution fixtures.
