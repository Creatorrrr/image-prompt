# Photo Runtime Boundary and API Ledger Qualification

- Date: 2026-08-12
- Status: current
- Scope: `skills/photo-prompt-image-generator`
- Goal: `GOAL_PLAN.md` Photo Prompt Residual Runtime Boundary and Legacy Cleanup Goal
- Resolves: `../failed-reports/2026-08-11-photo-runtime-metadata-contamination.md`, `../failed-reports/2026-08-12-photo-api-ledger-provenance-drop.md`
- Supersedes: none

## Outcome

The skill now keeps research, market, policy, legal-status, and compatibility controls outside visual composition evidence while projecting only visual candidates, selected character atoms, visual evidence, and generic composition constraints to the composing agent. Candidate-pack v3 is the clean default; an explicit v2 projection reconstructs the previous public shape for compatibility. The explicit Images API helper carries the audited composition record through every attempt and links unchanged retries.

## Direct Product Evidence

- Candidate packs omit preset-family routing IDs, nine control-only facet families, and adult-eligibility, structural character-scene, and dynamically collected nonvisual graph tags. The generic guard matcher can still read control facets, while `safety_tier` is the only one with current in-repository guard consumers and cannot add a common soft relevance signal. Character packs retain one primary visual atom, at most two supports, public visual evidence, and generic adult-original/observable-evidence constraints; router anchors, policy/guard records, compatibility-edge IDs, market origin, and audience scope stay internal. The primary atom is represented once by `runtime_nodes[].role`; the redundant public `primary_runtime_id` was removed and the auditor derives it from that single authority.
- A pair sharing only `content_basis:rights_cleared_original` now scores `0.0`; adding the same public `manifestation_mode` produces a visual facet score of `1.0`. Internal guard tokenization still sees the control facet.
- The fixed CJK character route preserves its caring handoff, reciprocal gaze, route, and atomic scene. Its pack contains neither `market_label_nonvisual` nor `market_label_nonvisual_guard`, and the composed-prompt audit passes.
- Thirteen semantic entries and one direct-only compatibility label now describe original fictional artwork or observable work, crew, equipment, and action rather than ownership/copyright, development state, national-market comparison, or audience-priority metadata. The public preset projection also omits its internal family router. Confirmed zero-reference functions/constants and the disabled grammar's unused empty `policy_ids` projection were removed; compatibility branches such as `concept_mode=legacy`, monolithic/custom index loading, score-trace fallback, and direct-only presets remain covered.
- A synthetic failed-first/successful-second API run proves exact prompt/negative reuse, complete audited provenance forwarding, returned run-ID chaining, schema-covered ledger fields, and an accessible success path outside the repository.

## Semantic Refresh

- First index-delta payload: 11 ordered texts, 6,273 UTF-8 compact-JSON bytes, SHA-256 `cb58ebd6d01cdfd1f726f7397bb2e233345f2df3733a2f538f2c8d8e8ee25f96`.
- Second index-delta payload: 2 ordered CJK texts, 1,832 bytes, SHA-256 `700534e3a600587f4a1dbfcfe55fa7f581ef9c5c3ad0f6f7ae1161ecdcbe1d30`; 6,511 then-current vectors were reused and only those two texts were sent.
- Baseline-to-final delta: 13 ordered texts, 8,104 bytes, SHA-256 `0a7c856660c899448851606258cf7dc20887e98695358e970fbd851bbd29450c`; 6,500 vectors are byte-identical to `4acba60`, 13 vectors changed, and zero entries were added or removed.
- Final index: dictionary hash `76b4f712fb5bdd8aaf868853a0d59552aa815085da66e64ce5e6530cc9c196ca`, generation `76b4f712fb5bdd8a`, `semantic-text-v3`, `gemini-embedding-2`, 768 dimensions, 6,513 entries, 16 valid shards, one generation, no partial checkpoint.
- Candidate-pack v3 follow-up: raw metadata removal changed the dictionary hash to `27c394c2bddb44b57e528d516d6fd6dcc926cf6b8e54587db0d3c86f13a77d04` and generation to `27c394c2bddb44b5`, but the 6,513 ordered key/text pairs remained byte-identical with SHA-256 `f8dc5e9c5f2a3c355db77222c4b1b6648c34617692f8c552af26ebcdb8e93300`. All 6,513 vectors were reused, all 16 shard SHA values remained identical, and no Gemini request was sent.
- Global real retrieval: 22/22, using 71 ordered requests / 68 unique texts / 6,381 bytes / SHA-256 `5702e85ca1e2d2d14a5a921438a89cd9dd19ab667dd4b2b87be497e730398040`.
- Changed-route real retrieval: 3/3 expected presets, using 12 ordered requests / 812 bytes / SHA-256 `95d0c71bd372ce816342b1b7423f8818cc033117c5290606bc0e80e86d47d413`.
- CJK dungeon-stream delta retrieval: 5/5 expected presets, using 17 ordered and unique requests / 1,430 bytes / SHA-256 `31ac2034764ae6abf68fe4aef6db1a954c24311c2af3a4665718eff1aa756c1a`.

## Verification

- Affected photo full regression: 319 tests and 597 subtests PASS. After the final redundant public-primary-ID removal, the 45-test candidate-pack/audit contract suite passed again.
- Dictionary and semantic-index integrity: PASS.
- Scene-expression: 112/112 PASS.
- Contradiction: 667/667 generated presets, zero declared-rule violations.
- Generalization / frozen holdout / domain holdout v2: 79/79, 24/24, 6/6 PASS.
- Remaining repository tests: 206 PASS and 1,134 subtests PASS; all 12 non-pass outcomes are the previously recorded `subculture-illustration` universal-scene baseline (previous runner summary: 11 failures and 1 error). No photo test failed.
- Public projection sweep: 667/667 direct presets generated; 663,094 public string fields scanned; zero final-prompt, non-ID process/source/market/legal/audience phrase, private key, private tag, control facet, or preset-family findings.
- Static legacy/source sweep: 751 top-level functions and 159 constants across 26 Python files have no zero-load definitions. No research-source name or source URL exists in the runtime skill outside operational API/schema URLs and the explicit rejection patterns.

## Candidate-Pack v3 Follow-up (2026-08-12)

- Removed unused `authorship_basis`, `audience_scope`, `character_family`, `character_topic`, `content_basis`, `cultural_provenance`, `market_origin`, `term_level`, and character-scene `audience_familiarity`/`market_origin` fields from the primary runtime assets. The dictionary validator rejects their reintroduction. `safety_tier` remains because it has a live hard-guard consumer.
- Renamed the internal adult inventory link to `inventory_preset_id`. Candidate-pack v3 drops that bookkeeping field, character `domain`/`topic_id`/`family_id`, and nonfunctional quality/craft/final-touch source traces. Explicit v2 restores the prior field names, source values, profile ID, and compatibility selection handle.
- Replayed all 667 direct presets against `c2b3600` with fixed per-preset seeds. Normalized v2 pack, selection, and prompt/negative mismatch counts were each zero. The same current sweep found zero v3 retired-key, old-profile, old-selection-handle, or pack-integrity findings.
- Final affected qualification: 276 generator tests and 46 candidate-pack/audit contract tests pass; scene-expression 112/112, contradiction 667/667 with zero violations, generalization 79/79, frozen holdout 24/24, and domain holdout v2 6/6 pass.

## Limits and Retained Boundaries

- This refactor did not render images, so it does not add pixel-quality evidence.
- No out-of-repository candidate-pack consumer was available. The default contract is therefore versioned as v3 while `--candidate-pack-version v2`, the programmatic v2 option, previous IDs, and the old pack shape remain available for explicit compatibility.
- The character-moe multilingual 96-case set remains a literal routing contract, not an independent semantic holdout. Independent character semantic claims require new implementation-before paraphrases.
- Internally stable identifiers such as `aligning_rights_cleared_original_vehicle_wrap` and control values such as `rights_cleared_original` remain only behind the v2/internal compatibility boundary; v3 exposes neutral handles and they do not enter semantic text, soft relevance scoring, or final prompts.
- Typed non-research provenance used by audit branching, such as candidate applicability source, intent source, and selected-blueprint source, remains in its contract fields; it is not treated as composition evidence. Removing those fields safely would require a versioned consumer audit rather than this bounded cleanup.
- Quality-layer source traces and public character topic/family/domain identifiers remain reconstructable only through the explicit v2 adapter; they are absent from default v3 packs and primary authoring data where they have no runtime consumer.
- Historical reports and evidence still contain research and prior contract terminology by design. They are repository evidence, not runtime authoring or composition data, and were not rewritten.
