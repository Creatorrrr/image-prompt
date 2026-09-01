# Arm-03 qualification report

Technical verdict: **FAIL** under the strict all-gates protocol. The generated image passes all 5 old-growth target gates and 4 of 5 shared gates, but `shared_reference_appearance_continuity` fails. User aesthetic judgment is **pending**.

## Test case and pack activation

- Assigned term: `old-growth forest structure`
- Deterministic seed: `1148298314`
- Independently selected concept: a wide, deep-focus post-rain temperate-rainforest transect in which a small adult field observer kneels by a seedling-bearing nurse log and photographs it; live-tree cohorts, canopy tiers, a standing snag, and fallen deadwood remain the primary scene structure.
- Active hard profile: `old_growth_forest_multilayer_deadwood_structure` (exactly one)
- Applied post-core mixin route: `노령림 구조`
- Candidate IDs selected in the final v6 pack/composition:
  - `old_growth_forest_structure_aesthetic`
  - `old_growth_forest_structural_subject`
  - `old_growth_gap_deadwood_regeneration`
  - `old_growth_forest_gap_location`
  - `old_growth_deadwood_decay_surface`
  - `layered_vertical_forest_depth_frame`

The assigned English term is not an exact span in the immutable user envelope. The mixin claim is therefore limited to the coordinator's post-core recipe-route diagnostic and canonical data existence; no requester-owned concept lock was invented and no pack JSON was hand-injected. Earlier setup experiments are preserved as preflight failures and consumed zero image calls.

## Prompt and render provenance

- Candidate pack: `photo-candidate-pack/v6`, pack ID `83f7796e7c777440`
- Composed prompt audit: PASS; advisory quality WARN only for the 238-word evidence-heavy prompt and manual pixel-review boundaries
- Runtime request audit: PASS, runtime prompt ID `2b60b6b6d7c50d15`
- Reference: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`, SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`, role `appearance_reference_not_edit_target`
- Tool: built-in `image_gen.imagegen`
- Actual image-tool calls: exactly 1
- Semantic/pixel retries: 0
- Saved output: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/render.png`
- Output: 1536 x 1024 PNG, SHA-256 `20d4c269617b06545aeb837fec50a488ccfa87634791766fbefd239dcb60d0b2`

## Direct pixel review

The same saved render was inspected at a 384 x 256 thumbnail and at native 1536 x 1024 resolution. The thumbnail is a deterministic size-only derivative, not another generation.

| Gate | Scale | Result | Observable evidence |
| --- | --- | --- | --- |
| `vo_natural_old_growth_cohorts` | thumbnail | PASS | Massive edge trunks, medium conifers, and slender saplings have visibly different girths and heights. |
| `vo_natural_old_growth_canopy_layers` | both | PASS | Fern/broadleaf understory, middle saplings and conifer boughs, and high crowns remain spatially separate around the bright gap. |
| `vo_natural_old_growth_standing_snag` | native | PASS | The central upright dead trunk has exposed weathered wood and a jagged broken crown distinct from green live conifers. |
| `vo_natural_old_growth_fallen_log` | both | PASS | A huge moss-covered decaying log spans the foreground with person-readable scale and convincing floor contact; additional downed trunks remain visible. |
| `vo_natural_old_growth_non_inference` | thumbnail | PASS | Multiple live cohorts, separated tiers, a snag, and several fallen logs read together; the image is not a plantation row, generic green wall, or single-tree substitute. |
| `shared_single_saved_image` | both | PASS | Both inspections derive from the one saved render; no cross-attempt averaging occurred. |
| `shared_environment_primary_legibility` | thumbnail | PASS | The forest fills the composition while the observer remains small and subordinate near the lower center-right. |
| `shared_reference_appearance_continuity` | both | **FAIL** | Adult presentation and long dark softly waved hair are visible, but the face is absent as comparable detail at thumbnail scale and remains small, downward-looking, and three-quarter/profile at native scale. General facial-appearance continuity with the frontal reference is therefore ambiguous; hair alone is partial evidence. |
| `shared_reference_non_occlusion` | both | PASS | The small observer does not hide the snag, main log, live cohorts, or foreground-to-crown layering. |
| `shared_photographic_coherence` | native | PASS | Wide-angle perspective, wet materials, mist-softened light, scale, anatomy, camera grip, and ground contact read as one plausible photograph. |

Partial or ambiguous evidence is a failure, so the single failed shared gate makes the overall technical verdict FAIL. The first render is preserved unchanged, with no repair or rerender. `audit_image_render_review.py` is not applicable because the pack has no generic `render_repair` contract; the coordinator's 10 qualification gates are recorded directly in `pixel_review.json`.

## Evidence files

- Pixel review: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/pixel_review.json`
- Independent run manifest: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/run_manifest.json`
- Run ledger: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/image_runs.ndjson`
- Composed prompt: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/composed_prompt.json`
- Runtime request and audit: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/render_request.json`, `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/render_request_audit.json`

No identity, same-person, protected-trait, personality, health, or attractiveness inference is made. User preference can be recorded only after the requesting user directly reviews the saved image.
