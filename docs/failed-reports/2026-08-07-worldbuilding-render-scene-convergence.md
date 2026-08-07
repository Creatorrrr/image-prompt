# Research-backed routes converge on administrative documentary scenes

- Recorded: 2026-08-07 18:26 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Scene Diversity and Render Quality Goal / Stage 1
- Affected scope: `skills/photo-prompt-image-generator` research-backed extensions, direct candidate packs, prompt composition, and rendered-image qualification
- Search terms: administrative documentary convergence, genre recognizability, atomic scene contract, sparse evidence budget, market origin, visual provenance
- Related paths: `GOAL_PLAN.md`, `skills/photo-prompt-image-generator/assets/photo_prompt_cjk_worldbuilding_extension.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `generated_images/cjk-rofan-status-academy-3-agent-test-20260807_174120`
- Related passed reports: `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`, `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`

## Failure

- Conditions or trigger: Generate one direct candidate pack and actual image for Korean-market romantasy, status-system world, and ability-academy world from the completed CJK taxonomy. Inspect the pixels for topic recognition and scene distinctiveness instead of relying on prompt-contract status.
- Expected: Each image should show a recognizable, original genre event with a clear stake and should not share the same administrative scene skeleton.
- Observed: The romantasy image reads primarily as a Chinese-style historical bookkeeping meeting; the status-system image as a modern public-service counter; the academy image as an administrative resource-allocation workshop. All three use staff/administrators, indoor counters or tables, document/token checking or handoff, and documentary capture.
- Impact on the goal: The previous routing and evidence criteria passed but did not establish useful creative image generation. Treating those results as product success would optimize the generator for taxonomy visibility rather than recognizable, interesting images.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `generated_images/cjk-rofan-status-academy-3-agent-test-20260807_174120/{01-rofan,02-status-system,03-ability-academy}/final.png` and each directory's `candidate_pack.json`, `composed_prompt.json`, and `result.json`.
- Result: Prompt audits report contract PASS, yet the root pixel review gives 0/3 unqualified topic-and-scene passes. The romantasy sub-review already records genre/provenance failure. The other two sub-reviews accepted institutional legibility but did not test whether a viewer would identify the requested genre without the prompt.
- Structural result: In the CJK extension, 31 of 46 English actions begin with checking/cross-checking/comparing/coordinating; 43 of 46 subjects contain staff, clerk, inspector, assessor, coordinator, operator, auditor, administrator, worker, or related operational roles. The three selected packs all chose `documentary_photo` plus `documentary`.
- Frozen inventory result: `render_scene_expression_baseline_v1.json` includes all 88 research-backed presets (research 17, subculture 33, worldbuilding 18, CJK 20). The pre-change baseline marks 88/88 for improvement because none has the new explicit render contract and the narrative-world routes do not yet meet the frozen scene/function thresholds. `render_scene_quality_holdout_v1.jsonl` fixes 12 later pixel-review cases, exactly three per extension.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed structural convergence. The completed goal required many world mechanisms and six material evidence slots, the authored scenes overwhelmingly encode inspection/records/administration, and documentary medium/genre have higher global selection weights. Direct CJK presets do not carry a non-empty mandatory topic intent or enabled fail-closed scene contract. Capture-context anti-overfit wording also removes recognizable genre anchors, while `market_origin` can be mistaken for visible cultural provenance.
- Confidence: confirmed
- Remaining unknowns: No unresolved blocker for this goal. Image-model behavior can still drift, so the 12-case pixel review must be repeated when render contracts, the image model, or visual acceptance rubric materially changes.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Source-backed taxonomy, two atomic scenes per CJK route, six world-evidence slots, 100/100 retrieval and full structural regression | Routing/evidence qualified, render quality not qualified | The goal explicitly excluded rendering and optimized evidence density rather than scene interest or genre recognition. |
| Three independent prompt audits and image renders | Contract audits passed; product-level visual result failed | Audit rubrics rewarded institutional evidence, text/IP safety, and photographic coherence but lacked metadata-free topic recognition and cross-route scene-diversity gates. |
| One bounded image edit or prompt repair per route | Romantasy remained culturally/genre ambiguous; status and academy remained administrative | Local edits could not repair a candidate pool whose subjects, actions, locations, capture style, and evidence budget already converged on administration. |
| Stage 4 virtual scene atoms injected into ordinary slot candidates | 88/88 scene contracts and the frozen retrieval suite passed, but frozen generalization failed 17 research cases with `candidate_pool_not_sampler_exact` | A resolved render instruction was represented as a synthetic candidate after sampling. That mixed the render-expression layer back into the knowledge/sampler pool and broke the existing exact-candidate provenance contract. |
| Stage 6 first full unit suite after visual acceptance | Real acceptance and contradiction gates passed, but full unit finished 397/399 with two failures | Pilot subject weight multipliers unnecessarily changed the ordinary CJK sampler and collapsed `cjk_ability_academy_lineage_system` seed 1..3 subject coverage from at least two to one. Separately, one exact candidate-pack key-set regression had not yet admitted the intentional disabled `render_contract` and `evidence_budget` fields. |

## Resolution or next safe step

- Resolution/workaround: Resolved. The research/evidence layer remains intact while every one of the 88 routes now has a separate scene-expression contract. One deterministic render blueprint contributes mandatory subject/action/location/prop atoms outside the ordinary sampler pool; operational documentary is no longer the only scene function, clues are limited to 1–2, and market origin is distinct from diegetic visual provenance. Redundant pilot subject weights were removed so existing sampler diversity remains unchanged.
- Verification: Current structural audit passes 88/88 routes. The frozen 12-case rendered sample passes 12/12 cases and 36/36 metadata-free review focuses, including romantasy, status-system, and adult ability-academy repairs. Current real acceptance passes generalization 79/79, holdout 24/24, domain v2 6/6, retrieval v4 22/22, all bleed/diversity/candidate hard checks, and visual review; contradiction generates 1,929 prompts with 0 violations; full unit passes 399/399.
- Next safe step if unresolved: Not applicable while current qualification remains valid. Reopen this report rather than weakening expectations if a later image-model, render-contract, candidate-pool, or routing change restores administrative convergence.

## Reuse guidance

- Avoid: Inferring image quality from routing accuracy, candidate count, prompt-contract PASS, or the presence of many world-system clues. Do not repair this by adding more documentary evidence or by weakening genre-specific expectations.
- Prefer: Separate knowledge from render expression, select one atomic scene function, use one event plus sparse clues and stakes, and inspect actual pixels without prompt metadata.
- Applicable when: A richly researched taxonomy repeatedly yields clerks, inspectors, counters, records, tokens, audits, or handoffs across otherwise different fictional genres.
- Re-check when: Scene-contract composition, selection weights, direct-preset mandatory intents, visual provenance, or actual image model behavior changes.

## Supersession

- Supersedes:
- Superseded by: `docs/passed-reports/2026-08-07-research-scene-expression-render-quality.md`
- Reason: The linked report records the product delta, current closed regression results, and actual rendered-image qualification that resolve this failure.
