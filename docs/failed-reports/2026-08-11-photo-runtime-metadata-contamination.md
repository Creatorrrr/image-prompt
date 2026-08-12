# Photo runtime research-metadata contamination

- Recorded: 2026-08-11 19:39 KST
- Status: resolved — runtime boundary, semantic rebuild, and real retrieval holdout qualified
- Goal/checkpoint: Photo Prompt Runtime Metadata Boundary Refactor / Stage 1
- Affected scope: `skills/photo-prompt-image-generator` semantic text, intent routing, candidate-pack relevance, render contracts, final prompt text, and distributable assets
- Search terms: source-grounded, provenance_scope, market_researched, cited interview study, character_moe_grammar, semantic text, candidate-pack metadata
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_subculture_extension.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_worldbuilding_extension.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`, `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`

## Failure

- Conditions or trigger: Inspect the current semantic text recipe and generate fixed rule-mode candidate packs for specialty presets plus a compact direct prompt for `character_cjk_term_normalization_scene`.
- Expected: Source titles, research-process labels, provenance markers, internal IDs, tags, and evaluation terminology remain private control or repository evidence; semantic relevance and positive prompt fields use only user vocabulary and observable visual meaning.
- Observed: Semantic text includes stable IDs, tags, kind, and every facet. Candidate relevance corpora include IDs and tags. Specialty render contracts promote `source-grounded` into positive mandatory intent, and the CJK character preset renders `market terminology retained as nonvisual provenance` into `prompt_en`. Generic route phrases can also activate `character_moe_grammar` without explicit character context.
- Impact on the goal: Internal development language can influence semantic similarity and quality-layer selection, leak into agent-visible candidate packs, or become literal final-prompt prose. Literal routing fixtures also overstate independent generalization when their exact phrases are reused as production aliases.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Local read-only scans and fixed rule-mode generation with seed 42; no external API, credential, private input, or image generation.
- Result: Current manifest contains 6,513 entries. Entry-text counts are 134 for `character_moe`, 136 for `source_grounded`, 376 for market-researched markers, and 816 for `provenance_scope` (counts overlap). The 24 character routes expose 96 unique aliases; all 96 appear in the domain alias list and each of the 96 literal routing cases contains exactly one. A source-ledger comparison found zero exact source-title or source-URL matches in operational JSON, isolating the defect to derived process metadata rather than copied citations. The current manifest references one 16-shard generation while four additional tracked generations occupy about 183 MB.

## Cause assessment

- Confirmed cause or current hypothesis: One generic text-construction path treats public visual semantics and private control metadata as equivalent. Research-derived runtime data also reused development-state labels in display, embedding, provenance, and mandatory-intent fields. Domain-first routing was repaired against exact fixture spans by copying all scoped aliases into the domain gate.
- Confidence: confirmed
- Remaining unknowns: Whether any out-of-repository candidate-pack consumer depends on the removed legacy private marker strings; no in-repository dependency remains.

## Resolution or next safe step

- Resolution/workaround: Offline product mitigation completed. Candidate relevance and integration corpora now whitelist public visual/user text; generic character routes require character-specific context while all 96 literal routing contracts remain valid. Raw research evidence is under `docs/research-evidence/photo-prompt/`, evaluation-only fixtures are under `tests/fixtures/photo_prompt/`, and semantic-text-v3 excludes stable IDs, tags, kind, and facets. Public display/embedding/scene fields no longer contain source/process, `provenance`, or market-control prose. The builder prunes older generations only after the new manifest is durable.
- Verification: The focused relevance/polarity/hybrid/routing, relocated fixture, shard round-trip/prune, dictionary validator, and 6,513-entry semantic-input checks pass. `test_photo_prompt_contract_v2` passed 44/44 and `test_prompt_generator` passed 272/272, including the real compact-shard byte-preservation test that previously failed closed against the old index. Default-path generalization (79/79), holdout (24/24), domain holdout v2 (6/6), current-scene audit (112/112), and the one-run contradiction sweep over 667 presets (667/667, zero declared-rule violations) pass. A fresh Korean/English detailed rule-mode generation over all 667 direct presets produced zero forbidden-marker findings and zero generation errors. The independent forward test found one CJK visual-atom/final-prompt leak; it was fixed and converted into validator/contract regression coverage. The approved rebuild completed with 6,513 entries, `semantic-text-v3`, 768 dimensions, 16 hash-valid shards, exact runtime entry order, one current generation, and no partial checkpoint. The separately approved retrieval payload contained 22 cases and 71 ordered requests (68 unique texts), 6,381 UTF-8 JSON bytes, SHA-256 `5702e85ca1e2d2d14a5a921438a89cd9dd19ab667dd4b2b87be497e730398040`; the real `gemini-embedding-2` retrieval holdout passed 22/22. Final index, dictionary, skill, diff, forbidden-marker, partial-artifact, and stale-path checks pass. The full 526-test suite returned exactly the unrelated pre-existing universal-scene baseline of 11 failures and 1 error, with no additional photo failures. Historical photo baseline v1 remains byte-immutable; the current v2 baseline and 10 intentional golden changes pass.
- Next safe step if unresolved: None for this defect. If an out-of-repository consumer reports reliance on a removed private marker, treat that as an explicit compatibility request rather than restoring metadata to semantic or public prompt fields.

## Reuse guidance

- Avoid: Embedding or rendering IDs, tags, facet names, source-grounded/researched labels, citation roles, or evaluation fixture terminology.
- Prefer: Separate user aliases, observable visual text, private typed controls, and repository-only evidence; classify literal alias tests as contracts rather than holdouts.
- Applicable when: Adding research-derived domains, semantic fields, render contracts, provenance facets, or multilingual exact routing.
- Re-check when: Semantic text recipe, candidate-pack public fields, intent routing policy, extension data, or index generation changes.
