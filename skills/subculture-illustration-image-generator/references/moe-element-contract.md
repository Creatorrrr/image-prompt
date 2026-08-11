# Research-Backed Moe Grammar v2

## Product boundary

The layer covers the exact 29 reviewed element IDs reconstructed from 34 origin articles. It has two versioned paths:

- `subculture-illustration-moe-element-plan/v1` is the immutable fixed-clause prototype retained for replay.
- `subculture-illustration-moe-grammar/v2` plus `subculture-illustration-candidate-pack/v4` is the product path. It selects among research-backed subtypes and composes real candidate/atom IDs into one sparse event.

Activation always requires an explicit element ID or complete reviewed alias supplied to the API. Ordinary request prose is never scanned to activate elements, and contextual words may only rank variants inside an already selected element. One to three elements may be selected. Their order declares the governing primary first.

This layer does not change safety evaluation, refusal/filter behavior, negative prompts, retry policy, photo routing, or universal-scene eligibility. The base v1-v3 pack is embedded unchanged and its safety/negative fields are exact-copied into v4.

## Research authority

The raw authority lives in five dossier shards under `assets/research_evidence_moe_elements/dossiers_v2/`:

- `narrative.json`: darkening/corruption, NTR/BSS, mesugaki, maternal care, morals committee, TSF, yandere, contempt/derision.
- `wardrobe.json`: 2015/2017 virgin-killer lineages, reverse bunny, dolphin shorts, thermal bodysuit, stockings, classic bunny.
- `body.json`: I-balance, thigh gap, axilla, adult finger-sucking gesture, glasses, ponytail, abdomen.
- `staging_social.json`: implied staging, screen-shake illusion, ahegao, pajama challenge, bubble-tea challenge, strategic-occlusion selfie.
- `fantasy.json`: sensory-suppression magic and quicksand.

Every dossier keeps at least three research questions, distinct semantic subtypes, appeal mechanisms, observable or narrative evidence, preference axes, executable candidates, compatibility/format implications, source-supported claims, cross-source synthesis, design inference, and limitations. Weak origin or popularity claims remain explicitly weak; source prose and culture labels are not copied as visual tags.

`compile_moe_grammar_v2.py` deterministically binds the exact five file hashes, legacy v1 inventory/research hashes, `intent_corpus_v2.json`, and `illustration_moe_compatibility_v2.json`. The normalized grammar contains 29 dossiers and 233 researched candidates. Re-running the compiler must reproduce the stored JSON object exactly.

## Intent and selection

`intent_corpus_v2.json` contains:

- 29 neutral requests, each selecting the canonical researched candidate;
- 29 paired preference requests, each selecting a materially different subtype and candidate key;
- 6 representative multi-element requests with an explicit primary/support order;
- 12 baseline-v4 review cases.

Candidate precedence is:

1. explicit multi-cue preference-axis/candidate evidence inside the selected element;
2. creative-development contract;
3. the stored numeric creativity band;
4. stable seed tie-break.

One isolated word is not enough to route a material variant because it may occur in a negated comparison. A preference route needs at least two matching candidate cues or two matched axis values. With no material preference, creativity `0.5` chooses the one canonical novelty-1 candidate. An explicit creative/authorial request activates the existing high-development contract and targets novelty 2 without changing the stored `0.5` value.

The selected pack records the original token, matched cues, selected candidate ID, reason, target novelty, subtype, preference profile, source claims, representation, resources, and compatibility tags. Unselected sibling elements never enter the pack.

## Sparse bundle and compatibility

The global bundle is exactly one governing primary plus at most two supports:

- one element: its primary plus two evidence supports;
- two elements: first element primary, second element primary-as-support, one evidence support from the governing element;
- three elements: first element primary, the remaining two element primaries as supports.

Compatibility is typed and sparse. `illustration_moe_compatibility_v2.json` owns frame requirement, camera profile, resource claims, hard conflicts, synergies, bounded fallback, and representative decisions. It does not materialize a 29-by-29 matrix. Known impossible pairs such as I-balance/thigh-gap, classic/reverse bunny, and strategic-selfie/bubble-tea fail closed. Darkening plus TSF is allowed only as one catalyst-driven sequence. The screen-shake illusion requires an interactive output and cannot be asserted from a static prompt.

## Composition and audit

`generate_moe_candidate_pack.py` wraps an already built v1-v3 pack. The final v4 draft uses one hierarchy:

1. base scene foundation;
2. one governing candidate direction;
3. up to two subordinate visible directions;
4. one shared-event compatibility bridge.

Do not append a separate label list or 29-element prompt block. Every selected candidate and atom ID appears in `required_chosen_candidate_ids`, and every selected atom phrase appears in `moe_evidence` and the composed prompt. `audit_moe_candidate_pack` deterministically replays selection, checks the unchanged base pack, exact safety/negative preservation, one-primary/two-support cardinality, chosen IDs, literal node evidence, and source/asset hashes.

The v4 audit proves selection and prompt binding only. It does not prove that pixels rendered correctly, that the audience prefers the result, that a meme's historical origin is certain, or that the base composed prompt passed its ordinary audit. Run the ordinary composed-prompt audit for the base workflow and inspect generated pixels separately when an image is requested.

## Commands

Compile the normalized grammar:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v2.py
```

Wrap an ordinary pack and compose a v4 draft:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  --base-pack /tmp/illustration-pack.json \
  --element moe_glasses \
  --preference-text "두꺼운 각진 아세테이트 안경, 오른쪽 temple을 올리는 순간" \
  --compose-from "An adult repairer pauses during one visible workshop action"
```

Focused validation:

```bash
.venv/bin/python -m unittest tests.test_subculture_illustration_moe_elements -v
ruff check \
  skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v2.py \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  tests/test_subculture_illustration_moe_elements.py
```

The focused suite directly covers 29 neutral selections, 29 material preference deltas, 6 sparse combinations, creativity `0.5` preservation, deterministic compilation, prompt composition/audit, mutation rejection, and frozen retry/photo hashes. It intentionally does not run universal 24x417, hidden 1,152-run qualification, image generation, or exhaustive pairwise combinations.
