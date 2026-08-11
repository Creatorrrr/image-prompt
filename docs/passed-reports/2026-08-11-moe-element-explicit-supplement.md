# Research-backed 29-element moe supplement without candidate-pack drift

- Recorded: 2026-08-11 KST
- Status: superseded
- Qualification: bounded-product-integration
- Goal/problem signature: Reconstruct 34 source articles as 29 independent moe elements, research their observable mechanisms, and make every element usable in illustration prompts without changing existing safety, retry, negative-prompt, photo, or universal-scene contracts.
- Search terms: 29 moe elements, 34 articles, explicit-only resolver, supplemental prompt plan, frame honesty
- Affected scope: `skills/subculture-illustration-image-generator` moe research asset, executable element asset, standalone plan/audit runtime, skill references, and focused tests
- Excluded scope: image generation, rendered-pixel qualification, 29×29 exhaustive combinations, candidate-pack schema changes, universal-scene hidden qualification, safety/filter changes, deployment, push, and PR
- Related paths: `GOAL_PLAN.md`, `skills/subculture-illustration-image-generator/assets/illustration_moe_elements_v1.json`, `skills/subculture-illustration-image-generator/assets/research_evidence_moe_elements/research_v1.json`, `skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py`, `tests/test_subculture_illustration_moe_elements.py`
- Related failed reports: `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`
- Reuses: `docs/failed-reports/2026-08-08-character-moe-research-provenance-overclaim.md`, `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`, `docs/failed-reports/2026-08-08-character-moe-final-integration-contract-drift.md`

## Reproduction context

- Repository/ref: `image-prompt`, local `main`; baseline `c10becc`
- Runtime: local Python standard-library JSON/hash runtime and unittest
- External work: source pages and independent public references were read-only; no credential, paid API, image generation, deployment, or remote mutation was used
- Preservation boundary: existing candidate-pack/composed schemas and universal-scene assets were not edited

## Successful approach

1. Verify the original inventory instead of trusting the conversation summary: five category pages expose 34 articles; five two-article lineages reduce to 29 independent topics.
2. Separate research roles: retain every origin URL, link at least one independent source per element, and state uncertain meme origins as limitations rather than facts.
3. Compile terms into nine typed mechanisms. Culture labels route explicit choices; concrete relation, garment, pose, expression, geometry, or hazard clauses provide visible evidence.
4. Keep integration additive: a separate plan and audit replay asset hashes, IDs, aliases, frame requirements, combinations, and literal evidence without adding fields to historical candidate packs.
5. Preserve format honesty: prior relationships and transformations need paired/sequence output, and the screen-shake illusion remains an interactive substrate rather than a static motion claim.
6. Preserve user boundaries: ordinary concept prose selects nothing; safety, refusal, retry, negative prompt, photo routing, and universal selection remain unchanged.

## Evidence and scoped completion criteria

| Criterion | Direct evidence | Result |
|---|---|---|
| Original inventory | 34 unique `origin_record` URLs, exact 29 ordered IDs and category counts 8/6/7/3/3/2 | pass |
| Research provenance | Every element has origin and independent source IDs plus an explicit limitation and design inference | pass |
| Executable coverage | 29/29 explicit IDs build deterministic source-bound plans and literal prompt blocks | pass |
| Prompt evidence | Every generated direct prompt passes all element-owned evidence groups; one removed contact phrase fails | pass |
| Selection boundary | Empty input selects none; all reviewed aliases resolve; arbitrary concept sentences do not | pass |
| Combination boundary | Six representative combinations pass; three closed incompatibilities and invalid frame modes fail | pass |
| Integrity | Canonical plan ID, asset hashes, replay and forged-selection mutations are checked | pass |
| Existing contracts | Retry and photo baseline hashes remain exact; illustration-photo boundary passes 3/3 | pass |

## Verification commands

```bash
.venv/bin/python -m unittest tests.test_subculture_illustration_moe_elements -v
.venv/bin/python -m unittest tests.test_subculture_illustration_photo_boundary -v
.venv/bin/python -m py_compile \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_element_plan.py
ruff check \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_element_plan.py \
  tests/test_subculture_illustration_moe_elements.py
ruff format --check \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_element_plan.py \
  tests/test_subculture_illustration_moe_elements.py
python -m json.tool skills/subculture-illustration-image-generator/assets/illustration_moe_elements_v1.json
python -m json.tool skills/subculture-illustration-image-generator/assets/research_evidence_moe_elements/research_v1.json
git diff --check
```

## Retained limitations

- No image was generated. Prompt evidence and planning audit do not prove rendered anatomy, clothing construction, optical motion, relation readability, or salience.
- The named origin of the strategic-occlusion selfie and several social-meme first-post claims remain low-confidence community history.
- Only six representative combinations are qualified. The runtime permits at most three explicit elements and does not claim exhaustive pairwise compatibility.
- The supplement is not a candidate-pack or universal-scene qualification and must not be used to claim hidden generalization.

## Reuse guidance

- Prefer: explicit-only selection, culture-label versus visible-construction separation, source versus design-inference separation, minimum frame contracts, asset-hash replay, and a standalone supplement when historical pack schemas must stay byte-stable.
- Avoid: keyword-scanning arbitrary concepts, injecting unrequested elements, treating a label as prompt evidence, or describing a single portrait as proof of a prior relationship or transformation.
- Re-check when: any of the 29 records, reviewed aliases, source URLs, prompt clauses, frame modes, incompatibility pairs, plan schema, or audit replay changes.

## Supersession

- Superseded by: `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`
- Reason: The implementation remains useful as an inventory/provenance prototype, but it did not place research-backed candidates in the ordinary candidate pack or alter intent, preference, creativity, ranking, or composition behavior required by the user's original outcome.
