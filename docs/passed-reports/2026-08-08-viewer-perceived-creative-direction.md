# Viewer-Perceived Creative Direction and Authorial Voice

- Date: 2026-08-08
- Status: current
- Scope: `skills/photo-prompt-image-generator`
- Goal: `GOAL_PLAN.md` Viewer-Perceived Creative Direction and Authorial Voice
- Resolves: `../failed-reports/2026-08-08-creative-direction-pixel-premise-legibility.md`
- Supersedes: none

## Outcome

Explicit creative/original/ingenious/authorial requests now activate a generic creative-direction workflow rather than relying only on candidate diversity. A high-creativity candidate pack exposes no new topic data; it exposes a binding development contract. The agent must name ordinary first answers, develop at least four proposals using distinct concept operators, choose exactly one, and carry one rule change, multiple physical consequences, a reveal path, and concrete vantage/timing/omission/material decisions into the final prompt.

The composed-prompt audit rejects missing or shallow briefs, duplicate moves, stacked rule changes, mismatch between the selected proposal and selected concept, unselected signature mixing, non-literal evidence, and attempts to use fixed `artistic_final_touch` wording as authorial proof. Ordinary packs below the activation floor do not gain the field and retain the previous contract.

## Direct Product Evidence

The implementation-before baseline and final comparison use three frozen requests, rule-mode seeds `890101`–`890103`, the same built-in image tool, one initial image per prompt, no image edits, and preserved failures.

| Case | Baseline pixel result | Accepted concept move | Final pixel result |
|---|---|---|---|
| Potter | distressed-luxury cup flatlay; no discoverable premise | `absence_as_evidence` | rimless displaced-dust footprint and off-center held cup create an absence→comparison reveal |
| Urban solitude | familiar rainy back-view outside a convenience store | `functional_recontextualization` | transparent tote contains a warm room and extends a dry amber corridor through cold wet pavement |
| Adult transformation/recovery | ordinary bicycle-light repair | `temporal_fold` | current bare-hand repair and previous-duty gloved hands coexist in the closed case reflection |

`assets/render_creative_direction_visual_review_v1.json` records 3/3 cases passing all eight frozen focus items. Every case improves originality, ingenuity, and intentionality over its baseline without topic-fidelity or photographic-coherence regression. Failed first/repair attempts remain under `generated_images/creative-direction-holdout-v1-20260808_163100/`; acceptance did not select from a batch.

## Material Failure and Recovery

Prompt audit alone initially overpredicted two relations. The potter's empty trace became a solid circular base, and the urban traveler kept a normal pavement reflection through one repair. The durable recovery was not more adjectives or more anomalies:

- define negative space through positive material evidence and explicitly exclude a physical rim/base;
- stop fighting a repeated image-model absence prior after one failed repair;
- select an already-developed alternative operator whose two consequences are spatially concrete;
- preserve one causal rule and the same aboutness while changing its visual realization.

This boundary is reusable: literal prompt binding qualifies the product contract, while original pixels—not the brief—qualify relation following.

## Verification

- Focused creative contract tests: 2/2 PASS, including normal brief plus seven fail-closed mutations.
- Dictionary validator: PASS.
- Current merged scene-expression audit: 112/112 routes PASS.
- Final candidate/composed integrity: 3/3 audit PASS, negative content byte-identical, prompts 118/120/120 words.
- Final PNG hashes and versioned visual review: PASS, 3/3 × 8 focus items.
- Full unit suite: `Ran 401 tests in 1551.172s` — `OK`.
- `git diff --check`: PASS.

The creative-direction delta adds no topic taxonomy, embedding text, or semantic-index entries. The full suite also validated the pre-existing character-moe dictionary/index state in the same working tree.

## Reuse Conditions and Limits

- Activate this workflow only for explicit viewer-side creativity/originality/authorial intent; ordinary requests keep the conservative path.
- Treat `creative_exploration` feature distance as search diversity, never as a creativity score.
- Keep a familiar anchor and one rule change. More anomalies are not a repair for weak meaning.
- Use frame, time, omission, and material relations to express voice; never substitute a named artist or the fixed final-touch sentence.
- Preserve first renders and stop after the bounded repair budget. A successful prompt audit is not permission to hide a failed image.
- The three-case result is direct product evidence, not a blinded population study or a guarantee of historical novelty across all models and subjects.
