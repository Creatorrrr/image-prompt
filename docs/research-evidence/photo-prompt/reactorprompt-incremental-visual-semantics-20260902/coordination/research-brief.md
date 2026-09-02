# ReactorPrompt incremental corpus visual-semantics research brief

## Authority and status

- Request: analyze the newly collected images and prompts to research stronger visual-semantics data and candidate-pack content across at least ten independently delegated topics.
- Mode: research/design only. Do not edit runtime assets, generated indexes, tests, or the target skill in this study.
- Target skill baseline: `skills/photo-prompt-image-generator` at Git revision `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab` with unrelated pre-existing working-tree changes preserved.
- Evidence layers must remain separate: prompt text inspection, delivered corpus-pixel observation, repository/package inspection, external research, and user judgment.
- No image generation is authorized or required. Corpus images are already delivered source artifacts, so direct inspection of them is pixel evidence about this corpus only.

## Frozen corpus

- Incremental manifest: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- Manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- Gallery snapshot SHA-256: `35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f`
- Translation snapshot SHA-256: `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586`
- Scope: 1,182 posts, 4,908 images, 924 non-empty prompts, 904 unique prompt bodies, 258 missing prompts; post IDs 1565 through 2746.
- Existing visual-obligation source SHA-256: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
- Existing tag/candidate source SHA-256: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
- Existing quality-layer source SHA-256: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`
- Existing generated visual-profile index SHA-256: `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626`

## Shared method for every topic

1. Scan all 924 non-empty prompt records programmatically for the assigned topic. Record the query/heuristic and match counts; counts are prompt-side evidence only.
2. Inspect current runtime sources relevant to the topic to identify overlap, gaps, and the correct owning layer. Do not treat the generated index as an authored source.
3. Inspect at least 24 actual corpus images spanning at least 12 posts, using a deterministic or explicitly documented sample that includes positive examples and nearby controls. Prefer coverage across early, middle, and late incremental IDs. If fewer than 12 topic-positive posts exist, inspect every positive plus enough controls to reach 24 images.
4. Keep prompt claims and pixel claims separate. State the pixel sample denominator and never generalize a sampled pixel frequency to all 4,908 images.
5. Do not infer identity, same-person status, protected traits, actual relationships, health, attractiveness, personality, occupation, ethnicity, nationality, or allegiance from pixels. Limit people-related observations to visible adult presentation, pose, expression, styling, action, and spatial relations.
6. Use authoritative or primary external sources only where they materially define a stable photographic mechanism or terminology; cite direct URLs. Corpus-derived findings do not need unrelated web research.
7. Express proposals as `observable components -> confusion negatives -> candidate data or owning layer -> thumbnail/native render gates -> positive and hard-negative regression cases`.
8. Separate broad advisory candidates from narrow exact hard profiles. BM25F/embedding-only retrieval remains advisory; corpus frequency is not permission for a global default.
9. End with a bounded decision: `proposed`, `revise`, or `reject`. Everything remains unimplemented and render-qualification/user judgment remain unscored.

## Required report sections

- Scope and sampling method
- Prompt-side findings and counts
- Pixel-side observations and sample IDs
- Prompt/pixel alignment and divergences
- Existing-data overlap and ownership
- Proposed semantic components and confusion boundaries
- Candidate-pack/data proposals with exact suggested fields or layer
- Regression and held-out tests
- Limitations and bounded decision
- Evidence appendix with post IDs, image paths, commands, and external sources

## Independently delegated topics

1. Composition, framing, crop, negative space, and attention hierarchy
2. Pose, body mechanics, weight distribution, gesture, and support/contact
3. Camera viewpoint, lens/perspective, distance, depth of field, and focus plane
4. Lighting geometry, exposure, shadow ownership, fill, rim, and material response
5. Color palette, white balance, tonal contrast, grading, and color separation
6. Environment, background structure, depth layers, atmosphere, and weather
7. Subject-prop action, hand/object contact, tool legibility, and state topology
8. Multi-subject staging, eyelines, proxemics, occlusion, and relationship topology
9. Facial expression, gaze, head orientation, micro-tension, and readability
10. Wardrobe silhouette, garment construction, material, texture, drape, and styling
11. Hair, makeup, skin rendering, beauty-capture detail, and anti-plasticity cues
12. Capture medium, smartphone/compact/studio signatures, flash, grain, compression, and processing
13. Narrative event timing, causal beat, unfinished transition, and visible consequence
14. Negative constraints, false substitutes, anatomy/object artifacts, and failure prevention
15. Prompt language architecture, clause ownership, redundancy, translation drift, and evidence budgeting
16. Non-portrait coverage: product, food, architecture, nature, systems, and documentary evidence scenes

