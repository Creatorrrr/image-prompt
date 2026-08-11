# Intent-preserving photo prompt optimization

- Recorded: 2026-08-11 14:33 KST
- Status: active
- Qualification: resolved-material-failure
- Goal/problem signature: Preserve all public photo-prompt behavior while preventing internal soft, negative, and meta guidance from becoming positive mandatory intent; keep explicit subject and no-people meaning authoritative; and reduce deterministic candidate-pack cost.
- Search terms: typed requirement polarity, mandatory intents, compact prompt budget, exact subject route, no_people, alias cache
- Affected scope: `skills/photo-prompt-image-generator` wrapper requirement routing, generator contract/provenance, candidate intent construction, subject/facet routing, compact rendering, bounded alias matching, focused regressions, and contract documentation
- Excluded scope: semantic-index format or regeneration, image generation, pixel-quality review, candidate-pack v3 redesign, public CLI removal, deployment, commit, push, and PR
- Related paths: `GOAL_PLAN.md`, `skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`, `tests/test_photo_prompt_contract_v2.py`
- Resolves: `docs/failed-reports/2026-08-11-photo-mandatory-intent-polarity-contamination.md`

## Reproduction context

- Repository/ref: `image-prompt`, local `main`; baseline `4e992a97278e73bb58f2c656f45836ef1ba1e4e6`
- Runtime: project `.venv` Python 3.14.3, rule mode, fixed seed 42
- Fixed concepts: `회사원`, `제빵사`, `고양이`, `사람 없는 화장품 제품 사진`
- External conditions: no credential, paid service, image generation, deployment, or external mutation was used

## Successful approach

- Keep public/direct compatibility while routing wrapper-generated recipe guidance through hidden typed role, negative, and soft fields only where candidate-pack or explicit compact composition needs them.
- Construct an intent contract from source, polarity, priority, and mandatory status. Keep user-authored visible requirements hard, role and soft guidance advisory, and negative constraints excluded from the positive mandatory set.
- Give exact curated subject aliases bounded precedence and carry request-level no-people exclusions through subject sampling, literal quality-facet inference, and adult-appeal eligibility.
- Keep the compact positive prompt within its final budget by omitting duplicated internal prose while retaining role evidence and the unchanged negative prompt.
- Cache the pure alias matcher with a bounded 65,536-entry LRU and remove dead candidate-term work; verify cached and uncached output bytes directly.

## Evidence and scoped completion criteria

| Criterion | Direct evidence | Result |
|---|---|---|
| Positive intent polarity is preserved | Fixed company pack has 1 phrase-level mandatory intent; role and soft rows are advisory, negative rows are excluded, and prior meta/negative tokens are absent from positive mandatory intent | pass |
| Explicit subject and no-people state are authoritative | Fixed cat selects the curated non-human animal subject with adult defaults off; no-people product has no human subject/facet/adult activation while its exclusion remains auditable | pass |
| Compact and pack budgets are met | Company pack is 95,146 minified bytes versus 151,732 baseline; compact prompt is 105 words versus 191 baseline and retains office-worker identity evidence | pass |
| User hard requirements remain hard | A literal additional requirement remains one required phrase through provenance, mandatory intent, and rendering | pass |
| Determinism and performance are preserved | Three fixed warm runs were 2.813, 2.047, and 2.125 seconds; median 2.125 seconds versus 7.260 baseline. All three stdout hashes match, and cached/uncached stdout and stderr are byte-identical | pass |
| Existing photo contracts do not regress | 309 focused photo tests pass; direct golden snapshots, immutable photo candidate boundary, v1/v2 replay, dictionary, semantic-index, scene-expression, and contradiction checks pass | pass |
| Full-suite boundary does not worsen | Full discovery ran 505 tests and retained exactly 11 failures / 1 error in the pre-existing universal-scene test module; photo failures and new failure classes are 0 | pass |

## Verification summary

- `tests.test_prompt_generator` plus `tests.test_photo_prompt_contract_v2`: 309 tests, pass.
- Dictionary validator: pass. Scene-expression audit: 112/112. Semantic index: 6,513 entries across 16 shards, pass.
- Contradiction audit: 667 presets x 3 generations = 2,001 generations, 0 violations.
- Golden direct concept/explain snapshots, immutable photo candidate-pack boundary, aggregate illustration validator, and v1/v2 exact replay: pass.
- Fixed cached/uncached comparison SHA-256: `9b9a0f6d9a8e8cd20814346ee80137a2f0473f1838adc60b6003e80200a8c7ec` for both stdout streams; stderr is empty for both.
- `git diff --check`: pass.

## Retained limitations

- These checks qualify deterministic text, routing, schema, compatibility, and runtime behavior only. No image was generated, so they do not prove rendered-image aesthetics, subject legibility, or audience response.
- The full repository suite is not green. Its 11 failures / 1 error are an unchanged, unrelated universal-scene baseline and are not claimed as fixed here.
- Semantic-index storage, loading, embeddings, and memory use were not changed or requalified.

## Reuse guidance

- Prefer typed source/polarity contracts over placing generated policy prose into user-facing additional requirements.
- Preserve hard user phrases as atomic mandatory intent; advisory role evidence can remain auditable without becoming a hard composed-prompt obligation.
- Use narrow exact subject routes before generic matching, and propagate request exclusions across every downstream eligibility layer.
- Re-run focused packs, compact budget, cached/uncached byte parity, golden/frozen replay, and the full-suite baseline comparison when these paths change.
