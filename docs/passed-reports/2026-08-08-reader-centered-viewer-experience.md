# Reader-Centered Viewer Experience, Attachment, and Commercial Intent

- Date: 2026-08-08
- Status: current
- Scope: `skills/photo-prompt-image-generator`
- Goal: `GOAL_PLAN.md` Reader-Centered Viewer Experience, Attachment, and Commercial Intent
- Resolves: none
- Supersedes: none

## Outcome

The skill now treats creative or authorial images as experiences interpreted by a viewer, not merely as unusual subjects or decorated prompts. High creative-direction runs automatically include a topic-neutral `photo-viewer-experience/v1` composition contract. Explicit audience-response, affect, attachment, commercial, and relation-centered subculture requests use the same contract through the agent-layer `--viewer-experience` control without raising creativity or changing ordinary candidate pools.

The composed-prompt audit requires one audience/context, one primary viewer need, one coherent intended experience, and visible actor/action/target/consequence evidence. Attachment, causal reinspection, and commercial comprehension/memory/action add conditional literal evidence. The audit rejects stacked needs, missing or nonliteral causes, response claims, genre/style labels used as proof, youth morphology used as attachment, and commercial objectives that lack product legibility.

## Direct Product Evidence

Three implementation-before requests used fixed rule-mode seeds `900101`–`900103`, one audited prompt each, one built-in image render each, no edits, no rerenders, and no batch selection.

| Case | Viewer contract | Metadata-free pixel result |
|---|---|---|
| Unlabeled insulated bottle | `product_detail`, `trust`, `remember` | The whole bottle reads first; a separated lid and plausible hand visibly reseat its silicone gasket, making maintenance and construction inspectable without a logo or claim. |
| Adult worker and nonhuman companion | `full_screen`, `relatedness`, `reciprocity` | The companion points at a sparking fault while holding a brush; the adult looks to the signal and extends pliers across their shared used repair kit. |
| Final morning in a long-lived home | `full_screen`, `meaning`, `self_relevance`, causal second reading | The adult removes the last key beside an open door; pale furniture absences and a worn floor route turn apparent emptiness into accumulated domestic contact on reinspection. |

`assets/render_viewer_experience_visual_review_v1.json` records 3/3 cases and all 18 frozen focus dimensions as PASS. The images and exact candidate/composed/audit/result files are under `generated_images/viewer-experience-holdout-v1-20260808_220600/`. The PNG SHA-256 values are `25c1c1c48c5980c2b4561016626fb9fa973ab232dfc647b61a1c76aea9ce0b2b`, `ec0b6fa6dab542904b5d423bdb4f6bf35819f82cebf162612504ffbac1acf1d9`, and `92a88152fdde6efbae5cdfc17eb611d4bd8b3eb7b9f0aa74625c9e0a1dfe9b58`.

## Verification

- Focused viewer/creative/visual-review contract tests: 4/4 PASS.
- Candidate composed audits: 3/3 `status=pass`, `quality_status=pass`, failures/warnings empty, negative bytes exact.
- Visual review: 3/3 cases, 18/18 focus results, no contract or declared focus failure.
- Dictionary validator: PASS.
- Current merged scene-expression audit: 112/112 routes PASS.
- Semantic-index integrity: PASS, dictionary hash `930f5f4359ed51f5784cc0b75923f2702495590c48811dd359c776660d07d6d2`, 6,513 entries, no index diff.
- Full unit suite: `Ran 404 tests in 1673.594s` — `OK`.
- `git diff --check`: PASS.

The delta adds no topic taxonomy, preset, embedding text, or semantic-index entry. Ordinary requests retain their previous candidate packs; explicit viewer control changes only the additive composition contract.

## Reuse Conditions and Limits

- Keep exactly one primary viewer need and one coherent experience. Emotional word stacking is not depth.
- Bind the reason to care to an observable event: actor, directed action, target, and consequence. A face or genre label can support but cannot replace that chain.
- For commercial work, distinguish stop, comprehension, memory, action, sharing, and return. Never obscure the product or invent a claim for an attention device.
- For subculture attachment, use agency, reciprocity, continuity, or self-relevance; do not rely on youth-coded human morphology, costume, market terminology, or protected designs.
- For authorial work, preserve a familiar anchor, one changed rule, a causal reveal, and concrete vantage/timing/omission/material decisions. The viewer contract explains why the discovery matters.
- The local review is not independent or population-level evidence. It cannot prove actual emotion, memory, virality, purchase, or long-term attachment; those claims require blinded human or market evaluation.
- In the departure image, the clean patch behind the hook is rectangular rather than distinctly key-shaped. The accepted second reading rests on the multiple furniture absences and worn path to the exit, which remain visible at thumbnail and native resolution.
