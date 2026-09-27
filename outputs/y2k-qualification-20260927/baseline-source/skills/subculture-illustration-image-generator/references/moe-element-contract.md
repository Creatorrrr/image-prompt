# Canonical and Visual Meaning-Aware Moe Grammar v5

## Product boundary

The immutable base covers the exact 29 reviewed element IDs reconstructed from 34 origin articles. The current effective view has 45 selectable IDs because one researched successor layer refines NTR and adds sixteen independent concepts. It has five versioned paths:

- `subculture-illustration-moe-element-plan/v1` is the immutable fixed-clause prototype retained for replay.
- `subculture-illustration-moe-grammar/v2` plus `subculture-illustration-candidate-pack/v4` is immutable historical product replay.
- `subculture-illustration-moe-grammar/v3` plus `subculture-illustration-candidate-pack/v5` is immutable meaning-only replay.
- `subculture-illustration-moe-grammar/v4` plus `subculture-illustration-candidate-pack/v6` is immutable historical visual replay.
- `subculture-illustration-moe-grammar/v5` plus `subculture-illustration-candidate-pack/v7` is the default product path. Its small manifest hash-binds v4 plus the seventeen-profile addition before composing real candidate/atom IDs into one sparse event.

Activation always requires an explicit element ID or complete reviewed alias supplied to the API. Ordinary request prose is never scanned to activate elements, and contextual words may only rank variants inside an already selected element. One to three elements may be selected. Their order declares the governing primary first. V5 preserves the v4 alias types and adds one ambiguity type:

- `exact`: another complete name for the same concept;
- `variant`: a complete name for one particular visual lineage and therefore a hard candidate-subtype restriction;
- `carrier`: a concrete visual construction that can carry the concept without replacing its canonical meaning;
- `related`: useful search/context vocabulary that is not sufficiently equivalent to activate the element and must fail closed.
- `ambiguous`: a complete surface form with multiple materially different reviewed senses; it must fail with concrete variant choices rather than choose one silently.

This layer does not change refusal/filter behavior, negative prompts, retry policy, photo routing, or universal-scene eligibility. The base v1-v3 pack is embedded unchanged and its safety/negative fields are exact-copied into v7. The semantic binding records that downstream safety evaluation must consider both the original request and canonical meaning; removing a runtime label never authorizes semantic substitution or policy evasion.

## Research authority

The raw authority lives in five dossier shards under `assets/research_evidence_moe_elements/dossiers_v2/`:

- `narrative.json`: darkening/corruption, NTR/BSS, mesugaki, maternal care, morals committee, TSF, yandere, contempt/derision.
- `wardrobe.json`: 2015/2017 virgin-killer lineages, reverse bunny, dolphin shorts, thermal bodysuit, stockings, classic bunny.
- `body.json`: I-balance, thigh gap, axilla, adult finger-sucking gesture, glasses, ponytail, abdomen.
- `staging_social.json`: implied staging, screen-shake illusion, ahegao, pajama challenge, bubble-tea challenge, strategic-occlusion selfie.
- `fantasy.json`: sensory-suppression magic and quicksand.

Every dossier keeps at least three research questions, distinct semantic subtypes, appeal mechanisms, observable or narrative evidence, preference axes, executable candidates, compatibility/format implications, source-supported claims, cross-source synthesis, design inference, and limitations. Weak origin or popularity claims remain explicitly weak; source prose and culture labels are not copied as visual tags.

`illustration_moe_grammar_v2.json` and its compiler remain byte-stable historical evidence. `moe_meaning_contracts_v1.json` binds the exact five dossier hashes and adds one ordered contract per element: canonical definition, essential and non-equivalent semantics, preference axes, runtime-label policy, semantic fidelity, visible component groups, false substitutes, forbidden inferences, adult requirement, and media capability.

`compile_moe_grammar_v3.py` deterministically combines that meaning source with the v2 candidate object, removes placeholder subtypes, replaces metadata-contaminated display definitions with canonical definitions, and rejects forbidden runtime labels in candidate prompt fragments. The v3 grammar contains the same 29 dossiers, 233 researched candidates, and 198 sources. Re-running it with `--check` must reproduce the stored bytes exactly.

`image_search_evidence_v1.json` adds one qualitative image-search record per element: multilingual queries, confidence, recurring visible features, confounds, representative URLs when a stable non-explicit source was found, and explicit limitations. Empty representative-URL arrays are allowed and stay paired with honest confidence/limitations; they must not be filled with inferred or unstable sources merely to satisfy a count.

`moe_meaning_contracts_v2.json` is an extension, not a replacement for v1 meaning. Each of its 29 contracts hash-binds the v1 contract and one image-evidence record, types every legacy alias, assigns every one of the 233 candidate subtypes to exactly one of 52 visual variants, and gives each variant:

- all required v1 component-group IDs;
- literal `all_of_en` anchors and a bounded `any_of` minimum;
- topology edges, camera requirements, temporal states, and interactions;
- known negative visual confounds for later rendered-pixel review;
- supported output modes.

`compile_moe_grammar_v4.py` deterministically attaches those contracts to the v3 grammar. Neither compiler rewrites v1-v3 inputs.

`moe_visual_additions_v1.json` is a separately versioned successor source built by `build_moe_visual_additions_v1.py`. It contains 33 reviewed source records and seventeen profiles: an NTR visual refinement plus female-leopard pose, the three-lineage cat-pose family, a brief partial underwear glimpse, the blond-tanned delinquent-coded adult archetype, the glasses-woman archetype, the literary-woman archetype, gumiho, dragon, dokkaebi, ghost, robot, assassin, soldier, aircraft pilot, tights, and bandage. Each profile carries a Korean definition, essential and non-equivalent semantics, typed aliases, source-scoped claims with confidence, qualitative visual evidence, observable component groups, adult and runtime-label policy, three novelty-level candidates, mutually exclusive variants, and compatibility. Community-only etymology remains low confidence. Korean folklore identities stay separate from Japanese or Western near-neighbors; Western dragon, wyvern, and Korean/East-Asian dragon anatomy do not collapse; role concepts require target, unit, or flight-task relations rather than one costume; tights remains structurally distinct from base stockings; tan never implies ethnicity; sexualized or age-ambiguous examples are excluded.

`compile_moe_grammar_v5.py` emits a small manifest rather than copying the full v4 grammar. The manifest authenticates the exact v4 bytes, addition bytes, 45-element/281-candidate effective view, and aggregate meaning, visual, evidence, and compatibility hashes. Bare `고양이 자세` and `cat pose` are ambiguous and non-activating; callers choose a reviewed all-fours, cat-paw portrait, or yoga variant. Historical v1-v4 files remain byte-stable.

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

The selected pack records the original token, its alias relation, matched cues, selected candidate ID, reason, target novelty, subtype, preference profile, source claims, representation, resources, compatibility tags, semantic fidelity, canonical meaning-contract hash, selected visual-variant ID, and visual-contract hash. It embeds each complete selected canonical and visual contract in order. Unselected sibling elements and non-selected visual lineages never enter the pack.

## Sparse bundle and compatibility

The global bundle is exactly one governing primary plus at most two supports:

- one element: its primary plus two evidence supports;
- two elements: first element primary, second element primary-as-support, one evidence support from the governing element;
- three elements: first element primary, the remaining two element primaries as supports.

Compatibility is typed and sparse. `illustration_moe_compatibility_v2.json` remains the immutable authority for the base 29; v5 appends sixteen profiles and a bounded rule delta from the additions asset without materializing an all-pairs matrix. Known impossible pairs such as I-balance/thigh-gap, classic/reverse bunny, strategic-selfie/bubble-tea, base glasses/glasses-woman duplication, female-leopard/cat-pose geometry, and separate stockings/tights construction fail closed. Gold-tan styling plus NTR is allowed only when appearance and relationship topology are independently evidenced. The screen-shake illusion requires an interactive output and cannot be asserted from a static prompt.

## Composition and audit

`generate_moe_candidate_pack.py` wraps an already built v1-v3 pack. The default v7 draft uses one hierarchy:

1. base scene foundation;
2. one governing candidate direction;
3. up to two subordinate visible directions;
4. one shared-event compatibility bridge.

Do not append a separate label list or 29-element prompt block. Before composition, add a label-free visible phrase for every required v1 meaning component group that the selected primary atom does not already carry. Then bind the selected visual variant's all-of anchors, the required number of any-of alternatives, topology, camera, temporal, and interaction phrases. Intersect candidate and variant output modes and fail when no shared mode exists. Every selected candidate and atom ID appears in `required_chosen_candidate_ids`; every selected atom phrase appears in `moe_evidence`; every canonical contract appears in `meaning_evidence`; and every selected visual variant appears in `visual_evidence`.

`audit_moe_candidate_pack` reloads the local v5 manifest, v4 base, and additions and deterministically replays selection. It checks the unchanged base pack, exact safety/negative preservation, original-request hash, canonical and visual asset hashes/bytes, typed alias policy, candidate-subtype ownership, one-primary/two-support cardinality, chosen IDs, literal node evidence, every required visual phrase and any-of minimum, forbidden runtime labels, adult declaration, and supported output mode. Recomputing an embedded contract hash or `pack_id` cannot authorize changed meaning or a cross-lineage variant.

The v7 audit proves selection, canonical/visual contract binding, and prompt components only. Negative visual confounds are deliberately carried into `visual_evidence` as pixel-review criteria rather than treated as forbidden words: a valid positive prompt may say “rather than a generic smug face.” The audit does not prove that pixels rendered correctly, that the audience prefers the result, that a meme's historical origin is certain, or that the base composed prompt passed its ordinary audit. Run the ordinary composed-prompt audit for the base workflow and inspect generated pixels separately when an image is requested.

## Commands

Build and compile the current visual grammar:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/build_moe_meaning_contracts_v2.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v3.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v4.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/build_moe_visual_additions_v1.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v5.py --check
```

Wrap an ordinary pack and compose a v7 draft:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  --base-pack /tmp/illustration-pack.json \
  --element moe_glasses \
  --preference-text "두꺼운 각진 아세테이트 안경, 오른쪽 temple을 올리는 순간" \
  --compose-from "An adult repairer pauses during one visible workshop action"
```

Use `--grammar-version v4` only for historical v6 visual replay, `v3` for historical v5 meaning-only replay, and `v2` for historical v4 replay.

Focused validation:

```bash
.venv/bin/python -m unittest tests.test_subculture_illustration_moe_elements -v
.venv/bin/python skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v4.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v5.py --check
ruff check \
  skills/subculture-illustration-image-generator/scripts/build_moe_meaning_contracts_v2.py \
  skills/subculture-illustration-image-generator/scripts/build_moe_visual_additions_v1.py \
  skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v4.py \
  skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v5.py \
  skills/subculture-illustration-image-generator/scripts/moe_meaning_contract.py \
  skills/subculture-illustration-image-generator/scripts/moe_visual_contract.py \
  skills/subculture-illustration-image-generator/scripts/moe_visual_addition.py \
  skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py \
  skills/subculture-illustration-image-generator/scripts/generate_moe_candidate_pack.py \
  skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v4.py \
  skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v5.py \
  tests/test_subculture_illustration_moe_elements.py
```

The focused suite directly covers historical v2/v4, v3/v5, and v4/v6 replay plus all 45 v5 canonical selections, all 267 merged typed aliases, related/ambiguous rejection, variant-lineage isolation, prompt composition/audit, sensitive-label omission, contract/component/media mutation rejection, and frozen retry/photo hashes. The 312-case v5 qualification is semantic/visual prompt preflight only. Neither check runs image generation, pixel review, universal 24x417, hidden 1,152-run qualification, or exhaustive pairwise combinations.
