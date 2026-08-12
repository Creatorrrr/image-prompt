# Research-backed scene expression and rendered-image quality qualification

- Recorded: 2026-08-07 22:55 KST
- Status: active
- Qualification: resolved-material-failure
- Goal/problem signature: Preserve the source-backed research taxonomy and routing contracts while preventing research, subculture, worldbuilding, and CJK routes from converging on clerks, inspections, records, counters, and documentary administration in final images.
- Search terms: scene expression, administrative convergence, atomic render blueprint, sparse evidence budget, metadata-free visual review, worldbuilding render quality
- Affected scope: `skills/photo-prompt-image-generator` research-backed extensions, scene selection, candidate-pack composition/audit, semantic index, frozen routing, and rendered-image qualification
- Excluded scope: commit, push, PR, deployment, exact protected-world reproduction, living ritual instructions, exhaustive image-model quality, and automatic promotion of optional soft concept readiness
- Related paths: `GOAL_PLAN.md`, `tests/fixtures/photo_prompt/render_scene_expression_baseline_v1.json`, `tests/fixtures/photo_prompt/render_scene_quality_holdout_v1.jsonl`, `tests/fixtures/photo_prompt/render_scene_quality_visual_review_v1.json`, `skills/photo-prompt-image-generator/scripts/audit_scene_expression.py`
- Related failed report: `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`

## Reproduction context

- Repository/ref: `/Users/chasoik/Projects/image-prompt`, local `main`
- Baseline: clean `main@7daff7a`; qualified changes remain uncommitted because the goal explicitly excluded commit/push
- Runtime: Python 3.14.3, repository `.venv`, Gemini `gemini-embedding-2`, 768 dimensions, semantic text recipe `semantic-text-v2`
- Current dictionary/index: `ad0496bbb45e0db76c786cdf5b8d4e88e7c1853686daad63cc978f7e004fd6ff`, 6,379 entries, 16 JSON shards
- External boundary: Final quality evaluation used approved sanitized taxonomy and retrieval-query text with real Gemini embeddings. Index rematerialization reused 6,379/6,379 vectors and sent no taxonomy text during those rebuilds. Native image generation produced only the frozen local test sample.

## Successful approach

- Freeze first: Record the three visibly bad CJK images, inventory all 88 existing routes, and select 12 rendered holdout cases—three per extension—before implementation.
- Separate knowledge from rendering: Keep mechanisms, evidence, source provenance, typed domains, and ordinary sampler candidates intact. Resolve one scene blueprint into mandatory subject/action/location/prop labels outside the candidate pool, so the renderer receives one coherent event without falsifying sampler provenance.
- Make scene choice explicit but normally automatic: Deterministically cycle eligible blueprints by seed. Offer `--scene-function` only for a direct preset; it is a control rather than visible intent and fails closed when unavailable. Explicit no-people requests admit only blueprints declared non-human.
- Reduce evidence density: Carry one core event, one physical prop, at most one additional world clue, a stake or consequence, and one genre anchor instead of listing every institution and mechanism.
- Repair the data, not the rubric: Add compact non-operational confrontation, revelation, threshold, intimate-decision, community-performance, controlled-action, aftermath, and environmental-spectacle scenes across all prior research layers. Preserve one diegetic provenance per scene and keep market origin nonvisual.
- Qualify pixels separately: Audit prompt contracts first, then inspect the actual images without prompt metadata. Preserve two unsuccessful first renders and use one bounded image edit for each; never count prompt-audit PASS as pixel PASS.

## Material repair history

1. Injecting resolved scene atoms as synthetic candidates broke 17 frozen generalization cases with `candidate_pool_not_sampler_exact`. The implementation moved those atoms outside ordinary slots and retained exact sampler pools.
2. The first closed full suite passed the real acceptance and contradiction gates but finished 397/399. Removing redundant pilot subject multipliers restored the existing CJK seed-diversity contract; the generic exact-key test now requires the additive render fields to be present and disabled. The repaired full suite passes 399/399.
3. The rendered sample was generated under dictionary hash `97259…`. The final `ad0496…` change only removed ordinary subject reweighting; selected blueprints, composed prompt bytes, saved images, and visual findings did not change. The versioned visual artifact records both hashes and this boundary.

## Evidence and eight completion criteria

| Criterion | Direct evidence | Result |
|---|---|---|
| 1. All prior research routes are audited and repaired | Frozen inventory covers research 17, subculture 33, worldbuilding 18, and CJK 20; current audit reports 88 routes, 88 pass, 0 fail | pass |
| 2. Scene/function diversity meets the frozen thresholds | Narrative routes have at least 4 scenes, at least 3 functions, and no operational majority; specialty/evidence routes have at least 2 functions or their documented evidence exception; seed cycles reach every blueprint | pass |
| 3. Direct packs are sparse and fail closed without corrupting candidates | Every route exposes a selected-render-blueprint group, non-empty topic intent, one provenance, and clue budget 1–2; literal atom omission/cross-scene candidate selection fails audit; ordinary pools remain sampler-exact and capped at 64 | pass |
| 4. Market and visible cultural provenance remain distinct | `market_origin` is routing metadata; every selected scene carries exactly one `diegetic_visual_provenance`; culture-sensitive CJK scenes do not combine KR/CN/JP provenance | pass |
| 5. Romantasy, status-system, and academy failures are visibly repaired | Final pixels show a pseudo-European betrothal refusal, a rescue with observable ability cost, and an adult arena rival rescue; none uses the former ledger meeting, public-service counter, or allocation workshop skeleton | pass |
| 6. The frozen stratified rendered sample passes | 12/12 cases, 36/36 review focuses, contract failures 0; all composed prompts are 88–120 words with contract and quality audit PASS and no warnings | pass |
| 7. Routing, isolation, deterministic, safety, and IP/culture contracts remain green | Real acceptance: generalization 79/79, holdout 24/24, domain v2 6/6, retrieval v4 22/22, bleed 4/4, diversity 3/3, candidate coverage 6/6; automatic safety shape unchanged; protected-reference scan clear | pass |
| 8. Closed technical qualification passes on current state | Dictionary validator pass; index check pass; contradiction 643 presets × 3 = 1,929 with 0 violations; full unit 399/399; real acceptance `passed=true`, mock=false; final `git diff --check` pass | pass |

## Rendered sample and retained limitations

- Actual files: `generated_images/scene-expression-holdout-v1-20260807_211500/`; 12 final PNGs are 1536×1024. Original pre-edit solarpunk and academy attempts are retained beside their final files.
- Solarpunk required one edit because the first image read as generic eco-delivery. The final frame makes shared batteries, refrigeration, water pumping, greenhouse light, and medicine-priority visible in one community microgrid.
- Academy required one edit because the first energy burst could read as an attack on the fallen rival. The final arc visibly bends over the intact rival into an empty impact surface while the mentor advances.
- Status-system remains intentionally adjacent to original superpower survival fiction because the genre rule is expressed through bodily cause and cost, not a literal UI. Lowrider hydraulic motion is implied by stance and threshold action rather than frozen mid-lift.
- `soft_promotion_ready=false` remains an optional concept-benchmark signal. The final gate used `soft_required=false`; all hard legacy, golden, routing, isolation, and visual criteria pass.

## Verification commands

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
.venv/bin/python -m unittest discover -s tests
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py \
  --acceptance-gate --quality-runs 2 \
  --visual-review tests/fixtures/photo_prompt/render_scene_quality_visual_review_v1.json \
  --summary-only
git diff --check
```

## Reuse guidance

- Prefer: Preserve sourced knowledge and ordinary candidates, then add a small render-expression layer that selects one sparse event. Validate candidate provenance, prompt composition, and pixels as separate gates.
- Avoid: Increasing documentary evidence density, injecting resolved instructions as candidates, using a market label as costume provenance, or accepting a route because its prompt audit or retrieval score passed.
- Re-check when: The image model, scene blueprint resolver, candidate-pack schema, evidence budget, cultural provenance logic, semantic model/recipe, or frozen visual rubric changes.
- Reopen the related failure when: Different genres again converge on staff, counters, records, inspection, handoff, or committee scenes, even if structural and prompt audits still pass.
