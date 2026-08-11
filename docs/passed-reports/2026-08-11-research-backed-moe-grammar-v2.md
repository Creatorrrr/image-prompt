# Research-backed 29-element moe grammar changes actual candidate selection and composition

- Recorded: 2026-08-11 18:50 KST
- Status: passed
- Qualification: bounded product integration and prompt-evidence qualification
- Goal/problem signature: Research all 29 reviewed moe elements and use the findings to improve intent interpretation, material preference selection, creative variation, and prompt composition rather than appending one fixed clause.
- Affected scope: five dossier shards, paired intent corpus, compiled grammar, sparse compatibility, additive candidate-pack v4 wrapper, shared-event composer/audit, skill references, focused tests
- Excluded scope: safety/filter/refusal/retry changes, universal-scene requalification, hidden 1,152-run, image generation, pixel quality, blind reader preference, exhaustive 29x29 compatibility, deployment/push/PR
- Related failure: `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`
- Superseded prototype: `docs/passed-reports/2026-08-11-moe-element-explicit-supplement.md`

## Product result

1. Five claim-level raw dossier shards cover the exact 29-ID inventory. Every element has at least three research questions, multiple semantic subtypes, preference axes, source-backed claims, observable/narrative evidence, executable English candidate operations, format/camera implications, design inference, and explicit limitations.
2. `compile_moe_grammar_v2.py` normalizes those shards without discarding them and binds their exact hashes, the legacy inventory, the 58 paired single-element requests, and the sparse compatibility asset. The current result contains 29 dossiers, 233 candidates, and 198 normalized source records.
3. Neutral creativity `0.5` selects one canonical novelty-1 candidate. Material multi-cue preferences select a different typed subtype/key. An explicit creative cue activates the existing high-development contract and targets novelty 2 while the stored numeric value remains `0.5`.
4. Candidate-pack v4 embeds the unchanged v1-v3 pack, copies safety and negative prompts exactly, and exposes selected candidate plus atom IDs in the real composition contract.
5. Sparse composition is global: exactly one governing primary and at most two supports across all selected elements. The composer writes a base-scene → governing-event → subordinate-evidence → shared-event-bridge hierarchy instead of a standalone label/clause suffix.
6. The audit reloads the source-bound assets, deterministically replays selection, checks base-pack integrity, safety/negative equality, candidate IDs, sparse cardinality, literal node evidence, and composed evidence projection.

## Direct evidence

| Criterion | Evidence | Result |
|---|---|---|
| Research completeness | 29/29 dossiers, all required research fields, exact source/hash loading | pass |
| Candidate richness | 233 researched candidates; each element has at least five candidates and novelty levels 0/1/2 | pass |
| Neutral intent | 29/29 neutral requests select the expected canonical candidate key | pass |
| Material taste delta | 29/29 paired preference requests select the expected different subtype and key | pass |
| Sparse combinations | 6/6 requests preserve declared element order, one primary, and at most two supports | pass |
| Composition | Every selected atom phrase and real ID is bound; prompt contains one shared-event hierarchy and no `moe_` labels | pass |
| Creativity | Creative cue targets novelty 2 while stored creativity remains exactly 0.5 | pass |
| Mutation rejection | Missing literal node phrase and forged chosen-ID list fail the v4 audit | pass |
| Representative prompts | `qualification_v2.json` records 12/12 current-grammar prompt-evidence passes | pass |
| Preserved boundaries | Base safety and negative prompt exact; retry and photo baseline SHA-256 values unchanged; v1 supplement replay still passes | pass |

Current pinned artifact hashes:

- `illustration_moe_grammar_v2.json`: `4d77fc2c9d8cf7d94af0742c4bd577e19b8193629dcf9df1c5c6dc2e33383a9b`
- `illustration_moe_compatibility_v2.json`: `56e6a8293d2a19b4fac95c07f3d540e3d9dda0f18e9e9704ddf169d4a55249c2`
- `intent_corpus_v2.json`: `068031909677a3881611359cbeafe70e502f5f2b352d08507c14b502453f8f90`
- `qualification_v2.json`: `fdc800124e0780d656530b3020cfb95b618da1f315a155353abdd6f27c38edf5`

## Verification commands

```bash
python3 skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v2.py
PYTHONPATH=skills/subculture-illustration-image-generator/scripts \
  python3 skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v2.py
python3 -m unittest tests.test_subculture_illustration_moe_elements -v
ruff check \
  skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v2.py \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v2.py \
  tests/test_subculture_illustration_moe_elements.py
python3 -m py_compile \
  skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v2.py \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v2.py
git diff --check
```

## Honest limits

- This is deterministic planning and literal prompt evidence, not rendered-pixel proof. Clothing topology, anatomy, optical interaction, relation readability, and salience still require image inspection.
- The 12 comparison scores certify the frozen contract evidence; they are not a blind human-preference study or a universal claim about reader taste.
- Community-source chronology remains explicitly uncertain where no primary or scholarly origin source exists.
- V4 wraps, but does not alter, the ordinary v1-v3 base pack. Its base composed-prompt audit remains a separate required workflow gate before rendering.
- Compatibility is typed and sparse; only the six requested combinations and named conflict/repair rules were directly qualified, not all 406 pairs.

## Reuse guidance

- Prefer: research question → claim/source boundary → subtype and preference axis → executable candidate → one shared event → literal evidence.
- Avoid: one culture label as a prompt tag, one fixed clause per element, per-element three-node bundles, or a list appended after a finished prompt.
- Re-run the compiler, 29+29+6 focused suite, and 12-case qualification whenever any dossier, paired intent, candidate operation, selector, compatibility rule, or composer changes.
