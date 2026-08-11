# Photo candidate-pack mandatory-intent polarity contamination

- Recorded: 2026-08-11 12:42 KST
- Status: resolved
- Resolved: 2026-08-11 14:33 KST
- Goal/checkpoint: Photo Prompt Intent-Preserving Optimization / Stage 1
- Affected scope: `skills/photo-prompt-image-generator` wrapper requirement routing, candidate-pack mandatory intents, quality facets, composed audit, compact prompt rendering
- Search terms: mandatory_intents, additional_requirements, soft visual guidance, negative polarity, candidate pack bloat, no_people facet
- Related paths: `skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`

## Failure

- Conditions or trigger: Generate fixed rule-mode seed-42 candidate packs for `회사원`, `제빵사`, `고양이`, and `사람 없는 화장품 제품 사진` through the public wrapper.
- Expected: Only positive visible user intent and deliberate positive role anchors become mandatory prompt content; soft guidance remains optional and negative constraints remain negative. Explicit subject and no-people meaning must govern subject, facet, and adult eligibility.
- Observed: `회사원` produces 93 mandatory intents including meta tokens and negative vocabulary such as `Avoid`, `pin-up`, `fetish`, and `minors-coding`; 60 are uncovered. `제빵사` token `handling` activates a cleanroom robot subject facet. `고양이` selects `young_actor` and enables human adult appeal. The no-people product request blocks adult appeal but still gains a human facet from `사진` matching `photographer_role_model`.
- Impact on the goal: Candidate composition can be forced to repeat negative or nonvisual policy vocabulary in the positive prompt, packs are unnecessarily large, explicit subject fidelity can fail, and eligibility/facet evidence can contradict the request.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Public local wrapper commands using `--selection-mode rule --seed 42 --hybrid-augmentation --emit-candidate-pack --n 1`; direct compact replay for `회사원`; source trace through requirement forwarding, tokenization, mandatory-intent construction, quality facet inference, and composed audit.
- Result: `회사원` pack 222,881 pretty bytes / 151,732 minified bytes, mandatory 93 / uncovered 60; compact direct prompt 191 words. Source inspection confirms soft requirements are converted to `Soft visual guidance: ...`, all additional requirements enter mandatory intent sources, and the auditor requires literal or asserted positive prompt coverage.

## Cause assessment

- Confirmed cause or current hypothesis: Generated role guidance, safety exclusions, user-authored hard requirements, and soft cues share the untyped `additional_requirements` channel. Candidate-pack construction tokenizes every source into individual words without preserving polarity or provenance semantics. Request-level no-people state is not propagated to later literal subject-facet inference, and basic explicit animal aliases do not resolve `고양이` before subject sampling.
- Confidence: confirmed
- Remaining unknowns: The smallest backward-compatible internal representation that preserves role identity and every existing creative/viewer/hybrid audit without carrying full policy prose into the positive mandatory contract.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Prior structural audit only | Identified pack size and uncovered-intent risk but did not change product behavior | It did not trace polarity loss and explicit subject routing through the current August runtime |
| Exploratory pure alias-match cache | Preserved output SHA and reduced fixed-input runtime to about 2.97 seconds | It proves a performance opportunity but does not repair polarity, routing, or prompt size |

## Resolution or next safe step

- Resolution/workaround: Internal recipe guidance now uses typed role, negative, and soft channels while the public additional-requirement contract remains unchanged. Candidate intent construction preserves polarity and provenance, exact curated subject routes precede generic competition, and no-people exclusions propagate through subject, facet, and adult-appeal selection. Compact typed rendering omits duplicated internal policy prose. A bounded alias-match cache and removal of dead repeated work reduce deterministic runtime without changing output bytes.
- Verification: The fixed `회사원` pack is 95,146 minified bytes with 1 mandatory / 1 uncovered intent; its compact direct prompt is 105 words and retains the office-worker role evidence without an appended requirements block. Fixed three-run median is 2.125 seconds versus the 7.260-second baseline, and cached/uncached stdout and stderr are byte-identical. Focused photo suites, dictionary validation, semantic-index integrity, 2,001 contradiction generations, golden/frozen replays, and diff checks pass. Full discovery remains at the unrelated baseline of 505 tests with 11 failures / 1 error and adds no photo failure.
- Next safe step if unresolved: Resolved for the scoped text/runtime contract. Reopen only if requirement-source fields, compact rendering, subject routing, or candidate-pack audit semantics change.

## Reuse guidance

- Avoid: Treating internal prose, soft cues, or negative safety floors as user-authored positive visible intent; widening global subject eligibility to fix one explicit concept.
- Prefer: Typed provenance and polarity, phrase-level audit contracts, narrow curated explicit routes, and request-level exclusion propagation.
- Applicable when: Adding role recipes, safety guidance, soft anchors, literal subject inference, or mandatory-intent audit behavior.
- Re-check when: Requirement source fields, concept routing, quality facets, adult eligibility, prompt word budgeting, or candidate-pack schema changes.
