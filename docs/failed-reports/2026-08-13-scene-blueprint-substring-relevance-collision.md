# Scene blueprint relevance treated control prose and substrings as scene evidence

- Recorded: 2026-08-13 14:35 KST
- Status: resolved
- Resolved: 2026-08-13 14:45 KST
- Goal/checkpoint: Independent Japanese-subculture moe generation, Stage 1 fixed reproduction
- Affected scope: `photo-prompt-image-generator` v3/v4 character scene blueprint selection
- Search terms: `candidate_pack_select_scene_blueprint`, `candidate_pack_scene_blueprint_request_text`, `mist`, `unmistakably`, plant watering convergence, unique request relevance
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_scene_expression_character_moe.json`, `tests/test_photo_prompt_contract_v2.py`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`
- Related failed reports: `docs/failed-reports/2026-08-12-natural-moe-default-scene-repair-convergence.md`

## Failure

- Conditions or trigger: Generate v3 and v4 rule-mode candidate packs with seeds `1301`, `2603`, `3907`, `5209`, and `6503` from the frozen concept `Photorealistic Japanese-subculture-style, explicitly nonsexual, behavior-led moe scene of the same unmistakably adult woman, mid-twenties or older, preserving fixed reference identity, with pretty-and-cute bishoujo-inspired appeal through expression, grooming, role styling, pose, light, and one concrete character-revealing event.`
- Expected: Because the request contains no plant, watering, spray, windowsill, or domestic-care event, none of those scene concepts should receive request-relevance priority. The five seeds may vary independently through the bounded everyday scene pool.
- Observed: All five v3 packs select `moe_attribute_composition_graph_natural_03`, whose atomic scene is a houseplant at a windowsill, careful misting, a rebounding droplet, and a plant mister. V4 hides the blueprint ID and atomic prose from the public pack, but retains the same internal selector and therefore does not prove that selection was corrected.
- Impact on the goal: Five genuinely separate agents can independently receive the same unintended plant event before authoring begins. Isolation cannot recover variety or user intent once the shared skill has falsely promoted one scene as the unique relevance winner.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Ten fixed packs under `/tmp/image-prompt-selector-baseline.t2QCkk/`, produced from current commit `795691ed4f84`; source inspection at `candidate_pack_scene_blueprint_request_text` and `candidate_pack_select_scene_blueprint`.
- Result: v3 pack IDs `77201f128cef2b00`, `126f703c8629fb0c`, `cc8b716812f2f3ac`, `ef64d78799f40f7f`, and `3061bfa127820e6d` all expose `moe_attribute_composition_graph_natural_03`. Its relevance corpus scores nine matches against the request: generic controls `adult`, `behavior`, `character`, `explicitly`, `scene`, `through`, `with`, the requested craft word `light`, and the false substring `mist` inside `unmistakably`. The next natural defaults score only five or six, so the plant blueprint becomes the unique winner before the seed cycle can vary it.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed. `candidate_pack_scene_blueprint_request_text` merges concept locks, mandatory intents, and additional requirements without typed scene/control separation. `candidate_pack_select_scene_blueprint` then derives every length-four token from the entire blueprint prose and uses raw `term in request_text` substring membership. Generic control vocabulary boosts authored scenes, and `mist` matches within `unmistakably`.
- Confidence: confirmed
- Remaining unknowns: The smallest cue vocabulary that preserves explicit user-requested scene routing across English, Korean, and Japanese without exposing private blueprint prose in v4.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Run five isolated agents on v3 with different seeds | All five independently selected the same plant scene | Seed variation is bypassed when one blueprint has a unique positive relevance score |
| Make v4 hide blueprint ID and atomic prose and require a newly authored final scene | Public pack no longer leaks the literal plant instructions | Privacy and final authorship do not repair the internal relevance decision or prove pre-pack agent provenance |
| Repair generic natural-moe defaults after earlier work/repair convergence | Removed technician/repair/coworker leakage | The relevance matcher can still promote an unrelated everyday default through generic words and partial substrings |

## Resolution or next safe step

- Resolution/workaround: Blueprint relevance now scores only explicit internal `selection_cues` with the existing boundary-aware alias matcher. It no longer derives terms from full subject/action/location/prop prose. The strongly themed plant-misting default declares `requires_selection_cue=true`, so it is absent from a no-evidence seed fallback but remains selectable from explicit houseplant/watering/mister cues. `--explain-scene-routing` emits a diagnostic-only private trace with request-channel counts, candidate cue scores, matched cues, and the selected ID; ordinary v4 packs remain private.
- Verification: The exact frozen generic request produces zero cue matches, does not select the plant blueprint for seeds `1301`, `2603`, `3907`, `5209`, or `6503`, and the private trace selects the book scene for seed `1301` by deterministic cycle. An explicit `watering a small houseplant with a plant mister` request selects the plant blueprint from boundary-aware cues and does not match `mist` inside `unmistakably`. Five focused tests covering the collision, v4/v3/v2 projection, v4 scene privacy, multilingual no-preset natural routes, and all 112 research-route scene contracts pass in 13.958 seconds.

## Reuse guidance

- Avoid: Treating different seeds or isolated agents as protection against a deterministic relevance winner, and treating v4 public privacy as proof of correct private selection.
- Prefer: Typed scene evidence, boundary-aware cue matching, no-evidence fallback, and separate independence versus diversity reporting.
- Applicable when: A candidate system scores free-form request text against long authored scene or preset prose before an agent composes the final prompt.
- Re-check when: Request provenance channels, scene blueprint fields, alias matching, natural-moe defaults, or candidate-pack privacy versions change.
