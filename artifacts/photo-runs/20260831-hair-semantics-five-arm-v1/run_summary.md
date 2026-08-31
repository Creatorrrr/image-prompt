# Hair visual-semantics five-arm qualification

## Outcome

The hairstyle candidate and visual-obligation layers were expanded and validated, then five independently frozen complex concepts were rendered once each with the supplied portrait attached as an appearance reference. All five candidate packs, composed prompts, and runtime requests passed their pre-render audits. Direct saved-pixel review produced three strict passes and two strict failures: 18 of 25 individual gates passed, while 3 of 5 complete arm contracts passed.

The referenced ChatGPT conversation contained the user's research question but no retained assistant answer. The implementation therefore treats that question as the scope and uses a new source-backed decomposition instead of claiming access to absent prior keywords.

## Data changes

- Seven strict profiles now decompose hair meaning into five observable components, five distinct prompt-evidence fields, five pixel gates, and explicit substitute failures: two-block cut, hime cut, cornrows, locs, bilateral twin tails, balayage placement, and wet/damp clumped state.
- Existing two-block, hime, cornrow, and locs candidates were enriched; bilateral twin tails, wet/damp clumped hair, and balayage ribbon placement were added to their correct style or color owners.
- `locs hairstyle` is the neutral runtime expression; `dreadlocks` remains a compatibility/search alias and is forbidden on the runtime prompt surface for the strict locs profile.
- Exact/contextual terms may create hard obligations. Embedding-only similarity stays optional and cannot create evidence or pixel gates by itself.
- Hairstyle names never infer nationality, ethnicity, personality, value, or biometric identity.

Changed contract surfaces:

- `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json`
- `docs/research-evidence/photo-prompt/research_evidence.jsonl`
- `tests/test_photo_hair_visual_semantics.py`
- `tests/fixtures/photo_prompt/hair_semantics_pixel_test_cases_v1.jsonl`
- `skills/photo-prompt-image-generator/scripts/audit_moe_render_review.py`

The visual review auditor now also accepts a non-moe pack when, and only when, an effective strict visual-obligations gate set exists. Packs with neither a moe qualification nor visual gates still fail closed.

## Research boundary

The data model uses hairstyle dimensions rather than label-only prompts: overall arrangement, length regions, cut disconnection, scalp attachment and row paths, tie-point topology, color placement, and temporary moisture state. Important source-backed boundaries include:

- K-Hairstyle's factorized attributes and multiple views support evaluating style, length, curl, bangs, side structure, color, and exceptional states separately: https://arxiv.org/abs/2102.06288
- Australia's haircut-structure standard separates sectioning, parting, lift, distribution, weight lines, shape, direction, texture, and color: https://training.gov.au/training/details/SHBHCUT001/unitdetails
- The clinical terminology review defines cornrows as scalp-affixed braids organized in rows and distinguishes locked clusters from precise braid crossings: https://pmc.ncbi.nlm.nih.gov/articles/PMC8072502/
- Smithsonian cultural history supports treating braids and locs as culturally meaningful without inferring a person's identity from a hairstyle: https://folklife.si.edu/magazine/black-hair-identity
- Wella's professional comparison supports irregular freehand balayage ribbons versus a full-width ombre gradient: https://blog.wella.com/us/balayage-vs-ombre-hair
- Hair-fiber scattering shows that highlights can arise from illumination alone, so shine cannot prove wetness: https://graphics.stanford.edu/papers/hair/
- Hair-bundle physics supports clumping and collapse under wet capillary forces: https://www.damtp.cam.ac.uk/user/gold/pdfs/ponytail_prl.pdf

Nine approved evidence rows preserve these abstractions and their limitations in the project research ledger.

## Five independent image tests

| Arm | Frozen complex concept | Target | Prompt/runtime | Strict pixels | Gate result | Main observation |
| --- | --- | --- | --- | --- | --- | --- |
| A | Orbital greenhouse pollination emergency | 히메컷 | PASS / PASS | FAIL | 3/5 | Long rear mass and step survive, but curved/tapered side sections can still read as a rounded bob-over-long-hair substitute. |
| B | Bioluminescent aquarium coral-health survey | 콘로우 | PASS / PASS | PASS | 5/5 | Narrow scalp-attached rows, parting lanes, and continuous paths remain jointly visible. |
| C | Desert radio-telescope calibration | 트윈테일 | PASS / PASS | FAIL | 0/5 | Only the image-right tie point and bundle are definite; the opposite side remains loose hair. |
| D | Flooded baroque library manuscript rescue | 발레아쥬 | PASS / PASS | PASS | 5/5 | Irregular ribbons, soft dark-root transition, varied mid/end placement, and base continuity survive. |
| E | Volcanic-glass workshop furnace observation | 젖은 다발 헤어 | PASS / PASS | PASS | 5/5 | Reduced volume, damp bundling, weighted adherence, and coherent moisture cues survive without relying on gloss alone. |

Every arm used one built-in `image_gen` call, the same attached reference bytes with SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`, a v6 candidate pack, and no cross-arm prompt or image input. The reference role was facial/general appearance continuity for an original adult, not biometric identity verification.

Per-arm packs, prompts, runtime requests, reviews, manifests, ledgers, and images are under `arms/`. The coordinator's direct original-pixel review is `shared/coordinator_pixel_review.json`.

## Validation

- Dictionary validator: PASS.
- Visual-profile index: PASS, 81 profiles and 477 exact terms.
- Semantic index: PASS, 6,909 Gemini `gemini-embedding-2` entries at 768 dimensions in 16 shards; dictionary hash `db5fc1508c0e65a0559c2771ee5782776171b48fc103d41690deed88d20c37a6`.
- Focused hair, visual-obligation, visual-profile retrieval, and BM25F suite: 49 tests PASS.
- Contradiction sampling: 2,070 generated combinations, zero violations.
- Generalization holdout: 24 of 24 PASS.
- Scene-expression routes: 112 of 112 PASS.
- Five composed-prompt audits: 5 of 5 PASS.
- Five concrete runtime-input audits: 5 of 5 PASS.
- Five saved images: 5 of 5 generated and hash-verified.

## Decision

`revise` for render fidelity. The package, routing, prompt, runtime, and provenance layers qualify, and three unrelated complex renders pass. Broad visual promotion is blocked by the hime-cut blunt-panel ambiguity and the twin-tail bilateral-gather failure. These failed images are retained as exact regression targets. User aesthetic acceptance remains unscored and must stay separate from the technical pixel verdict.
