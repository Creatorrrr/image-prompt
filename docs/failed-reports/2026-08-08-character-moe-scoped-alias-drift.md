# Character-moe scoped aliases did not activate frozen multilingual routes

- Recorded: 2026-08-08 02:44 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Moe and Subculture Character Grammar / Stage 3
- Affected scope: `character_moe_grammar` intent routing for the frozen 96-case KO/EN/JA/ZH holdout
- Search terms: character moe scoped alias drift, domain-first routing, multilingual exact route
- Related paths: `skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json`, `skills/photo-prompt-image-generator/assets/semantic_retrieval_holdout_character_moe_v1.jsonl`

## Failure

- Conditions or trigger: Run the frozen 96-case character-moe routing assertions after adding the 24 presets, graph, scenes, and initial short aliases.
- Expected: Every case activates `character_moe_grammar` and exactly its one frozen scoped route while generic negative requests remain outside the domain.
- Observed: The first focused run stopped on topic 1 before the character domain could activate. After aggregating the initial route aliases into the domain gate, only 11/96 cases routed and 85/96 remained unmatched.
- Impact on the goal: The graph and direct presets worked, but multilingual natural-language requests could not reach 23 of the 24 routes reliably. Stage 3 could not pass.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `python -m unittest tests.test_photo_prompt_contract_v2.PhotoPromptContractV2Tests.test_character_moe_research_graph_routes_and_sparse_runtime_contract` plus a read-only per-case routing trace.
- Result: Initial failure at `character_moe_01_ko_01`; intermediate inventory `pass=11 fail=85`. Direct preset pack materialization and the 24-node graph validation had already passed, isolating the defect to routing aliases.

## Cause assessment

- Confirmed cause or current hypothesis: Existing scoped routing is domain-first. The new domain aliases initially contained only generic grammar labels, and many route aliases were paraphrases rather than literal short spans present in the implementation-before holdout intents.
- Confidence: confirmed
- Remaining unknowns: Real semantic-index competition remains to be checked after the dictionary hash changes and the approved index rebuild runs.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Four short aliases per route | Direct aliases were unique and descriptive | Most were not literal substrings of the frozen natural-language requests, and scoped routes cannot activate before their domain |
| Add all initial route aliases to the domain | Topic 1 and ten other language cases routed | Paraphrase drift remained in 85 cases |
| Replace each route's four aliases with one short, unique literal span per frozen language and aggregate the same spans into the domain | Focused 96-case assertion and generic negative controls passed | Resolved without adding whole holdout sentences or broad single-token aliases |

## Resolution or next safe step

- Resolution/workaround: Kept exactly four route-specific KO/EN/JA/ZH aliases per preset, each a short discriminative phrase contained in its frozen request. The domain gate reuses those 96 phrases plus six explicit grammar labels. Broad terms such as `cute`, `character`, `idol`, `streamer`, Korean `모에`, or Chinese `萌` alone were not added.
- Verification: The focused contract test passed, including 96 unique cases, exact one-route equality, 24-route coverage, six generic negative controls, direct pack materialization, default automatic safety pass, and candidate caps.
- Next safe step if unresolved: Rebuild the approved semantic index once and run the same holdout through real semantic retrieval; do not weaken exact-route expectations if embedding competition appears.

## Reuse guidance

- Avoid: Treating a semantically similar paraphrase as sufficient for a literal scoped-route gate, or adding broad genre words to make a holdout pass.
- Prefer: Freeze natural requests first, choose a short unique literal phrase in each language, share it between domain and scoped-route gates, and retain generic negative controls.
- Applicable when: A domain-first router adds multilingual exact routes on top of semantic retrieval.
- Re-check when: Alias normalization, domain gating, or a frozen retrieval intent changes.
