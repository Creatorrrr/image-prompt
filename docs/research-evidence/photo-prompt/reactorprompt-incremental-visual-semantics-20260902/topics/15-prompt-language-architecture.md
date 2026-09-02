# Topic 15 — prompt language architecture, clause ownership, redundancy, translation drift, evidence budgeting, and contradictions

## Status and headline finding

This is a research/design artifact only. It does not change runtime assets, generated indexes, tests, candidate packs, or prompt behavior.

The incremental ReactorPrompt corpus supports strengthening **prompt-control provenance**, but it does not support a new global writing style or a new exact visual-obligation profile. Prompt length alone is not the main failure axis. The more consequential distinctions are:

1. whether a text span is an image specification, a reference-dependent edit, a meta-generator, analysis prose, non-image metadata, or an unknown payload;
2. whether a clause comes from exact requester text, an available current source, an explicitly selected exact profile, advisory retrieval, or an authorial open dimension;
3. whether two seemingly opposed phrases address the same actor, object, region, panel, time, variant, polarity, and requirement mode;
4. whether repeated wording adds a distinct observable component or merely spends prompt budget twice;
5. whether a translated string has a hash-bound source lineage or is only an unjoined advisory artifact;
6. whether every hard clause maps to a falsifiable thumbnail or native-resolution gate.

Accordingly, this report proposes three narrow structural control contracts—`photo-prompt-clause-ledger/v1`, `photo-prompt-clause-consistency/v1`, and `photo-corpus-prompt-lineage/v1`—and a bounded revision to the existing `photo-authorial-prompt-budget/v2`. It explicitly proposes **no new exact visual profile**: exact visual meaning should continue to be owned by the existing visual-obligation registry, while BM25F, embedding, fusion, and unreviewed translation remain advisory.

Decision: **proposed**. Everything below remains unimplemented; prompt-runtime qualification, new generation, delivered-pixel regression, and user judgment are unscored.

## Scope and sampling method

### Frozen inputs

- Incremental manifest: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- Manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- Translation snapshot: `generated/reactorprompt-export-20260902-incremental/raw/translations.json`
- Translation snapshot SHA-256: `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586`
- Corpus scope: 1,182 posts, 4,908 delivered corpus images, 924 non-empty prompts, 904 unique prompt bodies, 258 missing prompts; post IDs 1565–2746.
- Target-skill reference revision: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- Frozen authored-source hashes used for ownership comparison:
  - visual obligations: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - tag/candidate data: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - quality layers: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`
  - generated visual-profile index: `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626`

The generated index was treated as derivative evidence, never as an authored owner. Repository statements below refer to the frozen research-start sources and the target skill contract, not unrelated concurrent working-tree changes.

### Required instruction and authored-source inspection

The design-mode method was taken from:

- `.agents/skills/image-prompt-skill-improver/SKILL.md`
- `.agents/skills/image-prompt-skill-improver/references/improvement-method.md`
- `.agents/skills/image-prompt-skill-improver/references/iteration-record.md`
- `skills/photo-prompt-image-generator/SKILL.md`
- `skills/photo-prompt-image-generator/references/composition-contract.md`
- `skills/photo-prompt-image-generator/references/concept-routing.md`
- `skills/photo-prompt-image-generator/references/maintenance.md`
- frozen authored `photo_prompt_visual_obligations.json`, `photo_prompt_tags.json`, and `photo_prompt_quality_layers.json`

These sources establish the existing envelope/core/intent-lock boundary, exact-profile versus advisory-retrieval distinction, semantic-assertion ownership, prompt-budget policy, compatibility checks, and generated-index derivation rule.

### Full prompt scan

All 924 non-empty prompt records were scanned programmatically. The scan measured whitespace-token length, exact prompt-body duplication, strict normalized clause repetition, bilingual/code-switch markers, section/header forms, reference markers, exclusion language, randomizer language, placeholder/reference tokens, non-image/meta recall, and lexical collision pairs.

These are prompt-side retrieval heuristics, not semantic classifiers. A match can be a positive clause, a negative clause, an example, a quoted phrase, a different panel, or a different actor. Counts do not prove a contradiction, redundancy, translation defect, image prevalence, or pixel success.

### Pixel sample

I directly inspected the first two downloaded manifest images for 14 selected posts: **28 actual corpus images across 14 posts**. This exceeds the required 24 images across 12 posts.

The sample is purposive and architecture-controlled rather than a prevalence sample:

- early IDs: 1799, 1897, 1927;
- middle IDs: 1998, 2171, 2286, 2305, 2311;
- late IDs: 2471, 2542, 2545, 2556, 2628, 2741;
- positives include a compact concrete specification, explicit panel ownership, named anchor sections, a bilingual duplicated specification, and a recent sectioned exact specification;
- nearby or hard controls include a sparse reference-only edit, an action/crop clause that visibly diverges, non-image metadata, an option-rich randomizer, identical prompt bytes attached to different posts, a video request represented by two still-image files, and analysis prose stored in the prompt field.

The manifest does not label each associated file as input reference, generation output, contact sheet, or other role. Therefore the report calls them **delivered corpus files/images**, not verified model outputs. Pixel observations are limited to visible capture, styling, action, and spatial relations; identity, same-person status, protected traits, actual relationships, and occupation were not inferred.

## Prompt-side findings and counts

### Length and budget distribution

Whitespace-token counts across all 924 non-empty prompts were:

| Statistic | Words |
|---|---:|
| minimum | 2 |
| first quartile | 112 |
| median | 185 |
| third quartile | 261 |
| 90th percentile | 340 |
| 95th percentile | 491 |
| maximum | 1,708 |

Using the current `photo-authorial-prompt-budget/v2` absolute bands as a descriptive comparison, not as a pass/fail audit:

| Approximate word band | Prompts | Boundary |
|---|---:|---|
| under 48 | 7 | Can be valid if the request is genuinely sparse, but often cannot carry a full evidence ledger. |
| 48–360 | 837 | Inside the ordinary absolute/recommended region. |
| 361–640 | 63 | Above the recommended ceiling but inside the absolute maximum. |
| over 640 | 17 | Outside the current absolute maximum; several are generators, shot lists, or large option inventories rather than one compact still-image specification. |

This distribution does not show that shorter prompts are better. It shows that a word count needs an evidence denominator. A 491-word prompt may carry many literal P0/P1 obligations, while a 1,000-word option inventory may contain mutually exclusive branches that must not all become active evidence.

Longest whitespace-token prompts included post 2305 (1,708), 2556 (1,237), 2531 (1,117), 2543 (1,056), 2537 (1,042), and 2568 (1,041). Length is a triage signal only.

### Architecture-recall counts

The following overlapping bilingual regex groups were run over all 924 prompts:

| Recall group | Matching prompts | Interpretation boundary |
|---|---:|---|
| reference/source marker | 278 | Mentions such as reference, attached, uploaded, supplied, `@image_n`, or Korean equivalents; not proof that the referenced file is available or role-labeled. |
| identity/copy boundary wording | 247 | Includes preserve/copy/distinct-face language; no pixel identity evaluation was performed. |
| randomizer or choose-one wording | 30 | Candidate alternatives must not be interpreted as simultaneous all-of obligations. |
| negative/exclusion directive | 583 | Includes `no`, `without`, `avoid`, `do not`, or Korean equivalents anywhere in the text; many are legitimate requester exclusions. |
| explicit negative header | 53 | Section labels such as `NEGATIVE`, `AVOID`, or `금지`; a header does not reveal whether each item is requester-authored or generic. |
| explicit section/header structure | 284 | Uppercase labels, bracketed headings, or Markdown headings; sectioning can help ownership but does not guarantee correct scope. |
| placeholder/reference token | 25 | Includes brace/bracket placeholders and `@image_n` forms; unresolved tokens need a binding check. |
| any Hangul in manifest prompt | 58 | Source-language observation only. |
| adjacent Latin/Hangul code-switch artifact | 6 | A narrow orthographic signal; not by itself a translation error. |
| non-image/meta recall | 66 | Broad recall for metrics, sharing/community language, or prompt-analysis prose; requires human/structured role review before exclusion. |

The non-image/meta group is intentionally recall-oriented. Confirmed examples include post 2286, whose prompt is only view-count/date metadata, and post 2628, whose prompt explains a prompt/like-count analysis. A non-empty string is therefore not sufficient evidence that a record is an image specification.

### Duplicate bodies and redundant clauses

- 904 unique bodies among 924 prompts means exact body reuse is present.
- Exact grouping found 17 duplicated-body groups containing 37 rows; the largest group contains four rows.
- Posts 2542 and 2545 have byte-identical prompt bodies but different post IDs, shortcodes, captions, and associated image sets.
- A strict normalized-clause detector—sentence/newline/semicolon split, punctuation stripped, minimum five tokens, exact equality—flagged post 2543 with repeated clauses. The detector intentionally misses paraphrase and translated duplicates.

Exact prompt reuse is not inherently an error. It becomes an error only if the system collapses distinct post/reference/seed/model/selection lineage or assumes identical prompt bytes imply identical pixels. Likewise, an anchor summary plus a more literal component decomposition can be useful non-redundant layering. Repetition should be judged by semantic effect and ownership, not string similarity alone.

### Lexical collision is not contradiction

A deliberately broad co-occurrence scan returned the following review buckets:

| Lexical pair in the same prompt | Prompts | Common valid separation |
|---|---:|---|
| photoreal/photographic vs illustration/anime/painting | 183 | Positive medium clause plus negative substitute. |
| no-text wording vs text/typography/signage wording | 196 | Required blank/readable-text exclusion plus environmental sign or quoted failure class. |
| sharp/crisp/focused vs soft/blur/bokeh | 195 | Subject sharp, background soft; different regions or focus planes. |
| symmetry vs asymmetry | 25 | Symmetric layout with natural facial/material asymmetry. |
| centered vs off-center/thirds | 18 | Different panels, primary versus secondary anchors, or prohibition/comparison. |
| eye-level vs high/low/top-down | 10 | Multi-shot or reference-versus-output hierarchy. |
| full-body/full-length vs close-up/tight crop | 8 | Multi-panel/multi-shot roles or a true same-frame conflict. |
| direct gaze vs off-camera/side gaze | 16 | Different actors, panels, shots, time beats, or a true same-subject conflict. |

No row in this table is a proven contradiction. A contradiction exists only when two **active**, incompatible, all-of clauses share the same owner dimension, actor/object, region, panel/shot, time/variant, priority, and polarity context, with no explicit hierarchy that resolves them.

### Translation snapshot boundary

`raw/translations.json` contains four top-level language maps—`en`, `ko`, `ja`, and `zh`—with 1,436 entries each. Two exact-join checks found:

- 0/924 manifest prompt bodies equal to the English translation value at the manifest `originalIndex`-derived key;
- 0/924 manifest prompt bodies present byte-for-byte anywhere among the English translation values.

This is **not evidence that 924 translations are wrong**. It is evidence that the frozen manifest prompt rows and the translation snapshot have no demonstrated shared key/byte lineage. Positional comparison would be unsafe. Semantic translation-drift evaluation requires, at minimum, an explicit `source_prompt_sha256`, source language, target language, translator/version, post/shortcode, and reviewed alignment state.

Several translation-snapshot strings contain visibly mixed machine/code-switch forms. Because they cannot be safely joined to manifest rows, they remain translation-snapshot evidence only and must not create exact visual obligations for this corpus.

## Pixel-side observations and sample IDs

The denominator for this section is 28 images from 14 posts. Each row summarizes the two inspected files `_01` and `_02`. It does not estimate frequency across all 4,908 images.

| Post | Sampling role | Prompt-side architecture | Delivered-pixel observation across `_01` and `_02` |
|---:|---|---|---|
| 1799 | sparse reference-dependent hard control | Requests restoration of an attached occult/strange photo but supplies almost no literal visible content in the manifest prompt. | One file shows a sepia library-like occult scene; the other shows a symmetric ritual-chamber scene. The large difference cannot be explained from the prompt body. Without reference-role and availability lineage, alignment is unscored rather than failed. |
| 1897 | compact concrete positive | About 134 words with reference/identity instructions, studio, half-body, pose, dress, jewelry, hard key, shadows, and white seamless background. | Both files visibly preserve the half-body studio/editorial proposition, dark strapless garment, graphic hand/neck pose, strong light/shadow, jewelry, and white field. Identity was not assessed. Compact wording can carry a coherent observable contract. |
| 1927 | clause-loss hard control | Specifies both arms behind the head, hands outside frame, and a tight crop from raised arms to below chest. | In both files the hands are visible near the braid rather than both hidden behind the head; the requested action/crop topology is not preserved. Moderate length and specificity do not guarantee pixel success. |
| 1998 | bilingual repetition positive | Repeats many appearance, prop, wardrobe, setting, and capture clauses in English and Korean. | Both files visibly show the pink side-bun hair, cat-ear headband, white lace parasol, layered sheer white styling, and bright urban street. Alignment does not prove that bilingual duplication caused the success or that every repeated phrase was necessary. |
| 2171 | strong per-panel ownership positive | Three stacked panels with exact top/middle/bottom face regions and roles. | Both files visibly preserve three stacked panels, their count/order, and the top lips/hand, middle eyes, bottom profile roles. This is strong evidence for scoped clause ownership. |
| 2286 | non-image payload hard control | Prompt field contains only view-count/date metadata. | The two files are visibly different editorial/fashion scenes. Prompt/pixel alignment is not applicable; the row should be excluded from image-spec candidate extraction unless another source supplies the actual prompt. |
| 2305 | one-of/randomizer hard control | A 1,708-word meta-generator enumerates content formats, themes, tone, text lengths, backgrounds, colors, fonts, layouts, and random choices. | One file is a clean paper quote card; the other is a handwritten note attached to a window. Each realizes one branch, while most enumerated branches are necessarily absent. Unchosen branches are `not_applicable`, not failed hard evidence. |
| 2311 | compact concrete positive | About 204 words specify a waist-up cornfield portrait, head/eyes/hand relations, low bun, denim garment, moody exposure, foreground leaves, and finish. | Both files visibly preserve the cornfield portrait, lowered/closed-eye direction, hand-near-neck action, dark denim styling, foreground leaves, and moody underexposure. This is another compact, high-ownership positive. |
| 2471 | explicit anchor-section positive | Labels `IDENTITY`, `STYLE`, `PALETTE`, `LIGHTING`, `SCENE/ACTION`, and `FRAMING`. | Both files visibly preserve a close/upper-torso field portrait, dark blazer/white shirt/striped tie/backpack straps, green field, direct gaze, warm backlight, rim-lit loose hair, shallow background, and vertical framing. Identity was not assessed. Named sections help human traceability, but their contents still need typed scope. |
| 2542 | identical-prompt lineage control A | Byte-identical to post 2545; asks for a bubble-tea corridor selfie with detailed face, shirt, cup, hand, lighting, material, and capture clauses. | The first two files instead visibly show a wet-hair bathroom scene with a towel and phone. Because file role is not labeled, this cannot be classified confidently as a failed output versus an input/reference set. |
| 2545 | identical-prompt lineage control B | Same exact prompt bytes as 2542, but a different post/shortcode/caption. | Both files visibly realize the corridor selfie, drink in the lower-left foreground, light pinstriped shirt, visible hand/cup/straw, direct playful expression, and window-side light. The 2542/2545 pair proves that prompt bytes alone do not own complete image lineage. |
| 2556 | modality/image-role hard control | A 1,237-word 15-second video request specifies exactly seven shots, reference hierarchy, two adult-presenting characters, dialogue, sound, and event chronology. | The two delivered files are one 16:9 room scene still and one three-view character/wardrobe sheet. Neither can prove seven-shot count, chronology, dialogue, or sound. The manifest does not identify either file as reference, storyboard, or final output, so those gates are unscored. |
| 2628 | analysis-prose hard control | Prompt field is a Korean explanation of terms correlated with likes, not an image request. | The two files show unrelated portrait/fashion scenes. Image-spec candidate extraction should reject or quarantine this prompt role; no prompt/pixel failure should be assigned. |
| 2741 | recent high-ownership positive | Separates reference scope, subject/appearance, wardrobe, camera, light, finish, palette, and exclusions. | Both files visibly preserve a close portrait, short tousled dark bob, freckles, terracotta eye/lip treatment, textured scarlet outer garment, ivory collar, cyan background, hard directional sunlight, sharp facial anchors, and background softness. The clause groups align visibly without requiring every phrase to be repeated. |

## Prompt/pixel alignment and divergences

### What aligned

1. **Scoped role clauses can survive variation.** Post 2171 preserves panel count, order, and per-panel face-region roles; post 2741 preserves several separately owned appearance, wardrobe, color, light, and focus relations across two files.
2. **Compact prompts can be complete enough.** Posts 1897 and 2311 carry coherent observable propositions without approaching the long-tail word counts. This does not prove a universal optimum; it shows why evidence coverage is a better denominator than raw length.
3. **Explicit anchors improve auditability.** Post 2471 makes style, palette, light, scene/action, and framing easy to trace. The pixel sample visibly retains much of that structure, although identity remains outside this audit.
4. **Exact layout ownership is more reliable than unscoped prose.** The three-panel roles in post 2171 are easier to audit than a flat list of composition words because each clause has an explicit panel owner.

### What diverged or remained unscorable

1. **Specific wording can still lose a relation.** Post 1927’s arms/hands/crop topology visibly diverges even though the prompt is neither sparse nor vague. Prompt audit is not pixel success.
2. **Bilingual duplication does not prove added causality.** Post 1998 aligns, but the two languages repeat many of the same semantic effects. The corpus cannot tell whether the duplication helped, was ignored, or merely consumed context.
3. **Option inventories are not simultaneous contracts.** Post 2305’s files realize different branches. Treating all choices as required would manufacture hundreds of false failures and inflate the evidence budget.
4. **Prompt bytes do not identify image roles.** The exact 2542/2545 prompt pair is associated with visibly different image sets; post 2556 mixes a scene still and a character sheet. Reference/output/storyboard role must be explicit before pixel attribution.
5. **Non-empty does not mean image prompt.** Posts 2286 and 2628 make candidate extraction unsafe without a payload-role gate.
6. **Reference-dependent rows can be blocked, not wrong.** Post 1799 lacks the attached source needed to evaluate its only meaningful instruction. Missing conditioning should yield `unscored_reference_missing`, not a semantic or pixel score of zero.

The sample supports architecture proposals only. It does not establish causal superiority, corpus-wide pixel rates, model behavior, or user preference.

## Existing-data overlap and ownership

### Existing prompt contract

The current skill already owns several crucial boundaries:

- the requester envelope preserves exact source bytes and active spans;
- the authorial core is frozen before local candidate data is introduced;
- `photo-intent-lock/v1` records anchor coverage and locked versus open dimensions;
- semantic assertions own required literal evidence for exact concepts;
- `authorial_core_binding` preserves source anchors and substantive baseline phrasing while allowing bounded authorial decisions;
- `photo-authorial-prompt-budget/v2` sets absolute 48–640 words, recommends 360, and allows an evidence-adjusted ceiling based on hard-evidence word count plus connective headroom;
- compatible evidence may overlap naturally rather than being duplicated;
- requester exclusions remain distinct from the modern prompt's generic intent-neutral defect controls;
- prompt/render request audits do not substitute for pixel review.

These mechanisms should be extended, not replaced.

### Existing exact visual obligations

The frozen visual-obligation registry already establishes:

- exact, boundary-aware source terms may activate hard obligations;
- negated terms do not activate a profile;
- semantic examples and semantic similarity only create optional/advisory candidates;
- embedding retrieval never activates a hard obligation;
- requester definitions and explicit requirements outrank profiles and candidate inspiration;
- each exact profile owns literal evidence, component semantics, confusion substitutes, and render gates.

Prompt architecture must not duplicate those visual semantics in a parallel registry. Its job is to preserve which exact profile or source span owns each clause and which profile gate the clause maps to.

### Existing candidate and quality data

The frozen tag/candidate source already has semantic policies, slot routing and pick order, slot priorities, coherence rules, and explicit soft/hard compatibility pairs. The quality source already owns subject/domain routing, applicability guards, visual-proposition guidance, and selection balance.

These layers are useful but insufficient for prompt-language provenance:

- slot compatibility is usually candidate-level and does not encode actor, region, panel, shot, time, or polarity;
- a semantic family hit cannot show whether a phrase was exact source evidence or advisory retrieval;
- slot priority does not reveal whether a clause is `all_of`, `one_of`, optional, or flexible;
- word budget does not expose repeated semantic effects or unowned prose;
- the corpus export does not establish prompt-to-translation or image-role lineage.

### Recommended ownership boundary

| Concern | Owning layer | Boundary |
|---|---|---|
| Exact requester bytes, active spans, reference boundary, locked/open dimensions | existing requester envelope, authorial core, and intent lock | Must remain source-authoritative. |
| Exact visible meaning and hard render gates | existing visual-obligation profile selected by exact evidence | Do not create a second language-only visual profile. |
| Broad concept/style/camera/etc. suggestions | existing candidate/tag and quality layers | BM25F/embedding/fusion remain advisory until selected. |
| Per-clause source, scope, polarity, requirement mode, priority, and gate mapping | proposed `photo-prompt-clause-ledger/v1` | Structural record, not a creative vocabulary. |
| Same-scope incompatibility and unresolved placeholder checks | proposed `photo-prompt-clause-consistency/v1` | Typed preflight rule; lexical pairs alone never hard-fail. |
| Evidence-adjusted length, duplication groups, unowned prose, and compression | revision of existing `photo-authorial-prompt-budget/v2` | Extend the current owner; do not add a competing budget policy. |
| Manifest prompt role, source hash, translation lineage, reference/output file role | proposed `photo-corpus-prompt-lineage/v1` | Research/ingestion owner; must not silently rewrite runtime prompts. |
| Generated candidate/visual indexes | derivative only | Never manually authored or treated as provenance. |

## Proposed semantic components and confusion boundaries

### Observable control components

| Component | Observable or auditable evidence | Confusion negative |
|---|---|---|
| `source_provenance` | Exact span ID and one of requester, current source, selected exact profile, selected advisory candidate, or authorial open dimension. | A BM25F/embedding hit labeled as requester evidence. |
| `prompt_role` | Whole-record role: still/video image spec, edit instruction, reference-dependent request, meta-generator, analysis prose, non-image metadata, or unknown. | Any non-empty field assumed to be an image spec. |
| `owner_dimension` | Subject, action, wardrobe, prop, environment, composition, camera, light, color, finish, text, exclusion, etc. | One generic “style” owner swallowing camera, light, and material clauses. |
| `owner_scope` | Actor/object, body/object region, panel/shot, time beat, variant, and output modality. | “Sharp subject / soft background” collapsed into one contradictory focus value. |
| `polarity` | Positive requirement, requester exclusion, or intent-neutral defect prevention. | `photorealistic` and `no illustration` treated as incompatible positives. |
| `requirement_mode` | `all_of`, `one_of`, optional, flexible, or example-only. | Every randomizer branch promoted to hard evidence. |
| `priority` | P0 proposition, P1 supporting constraint, or P2 finish/preference. | Fine grain competing equally with actor/action/topology. |
| `literal_prompt_evidence` | Exact phrase or generated clause that actuates the component. | A label such as “visible evidence” without literal content. |
| `semantic_effect_group` | Clauses that aim at one rendered effect, with decomposed subcomponents retained. | Anchor summary and necessary component expansion removed as a duplicate. |
| `conflict_relation` | Typed incompatibility with the exact competing clause and resolution state. | Keyword co-occurrence called a contradiction without scope. |
| `gate_binding` | At least one thumbnail/native gate for each active hard component, or an explicit nonpixel/unscored reason. | Prompt phrase presence counted as render success. |
| `artifact_role` | Input reference, generated output, storyboard/contact sheet, comparison, unknown. | Every post image treated as the model output of the manifest prompt. |
| `translation_lineage` | Source hash/language, target hash/language, translator/version, alignment state, and reviewed drift fields. | Positional or visual similarity used as a join key. |

### Contradiction rule

Two clauses are a hard contradiction only if all of the following are true:

1. both are active in the same chosen variant;
2. both are `all_of` or otherwise simultaneously required;
3. both share the same owner dimension;
4. both refer to the same actor/object and the same relevant region;
5. both refer to the same panel/shot and time beat;
6. neither is a requester exclusion describing a forbidden substitute;
7. no explicit reference hierarchy or priority resolves the difference;
8. their values cannot coexist observably.

Examples that must **not** hard-fail:

- subject sharp plus background soft;
- hard key light plus soft fill light;
- centered graphic layout plus natural facial asymmetry;
- direct gaze in panel one plus off-camera gaze in panel two;
- photorealistic positive plus `no illustration` exclusion;
- exactly one randomly chosen camera setup from an option list;
- a current-source appearance anchor plus an explicitly different new composition.

Examples that should fail when scoped to one still/shot/variant:

- `full body visible` and `face-only crop` for the same subject in the same panel;
- `no readable text anywhere` and an exact readable headline in the same visual layer;
- `eyes closed` and `direct eye contact with the lens` for the same subject at the same instant;
- two incompatible exact panel counts with no variant or hierarchy resolution;
- unresolved `@image_2` evidence when no second input is available.

### Redundancy rule

Clauses are redundant only when they share the same source authority, semantic effect, owner scope, strength, priority, and gate, and the later clause adds no observable component or necessary disambiguation.

Do not collapse:

- a compact anchor and its necessary observable decomposition;
- a P0 relation and a P1 material cue that makes it legible;
- actor-specific versions of the same action;
- different panel/shot/time owners;
- requester wording and a provenance-preserving literal assertion when both are contractually required.

Do group for budgeting:

- bilingual clauses that add no distinct source nuance after reviewed alignment;
- repeated generic quality stacks that map to the same finish gate;
- the same exclusion repeated in a negative header and final suffix;
- synonyms that do not change strength, owner, or observable result.

### Translation-drift fields

Only a hash-bound translation pair can be evaluated. Drift should be recorded by dimension rather than one opaque score:

- negation/polarity loss;
- actor/object or region reassignment;
- panel/shot/time reassignment;
- `all_of` converted to `one_of`, or vice versa;
- quantity/count/aspect change;
- reference-hierarchy loss;
- exact-profile trigger added or removed;
- strength/priority change;
- ambiguity introduced;
- culturally specific term left unresolved.

An unjoined translation remains advisory text and cannot activate an exact visual obligation.

## Candidate-pack and data proposals

### 1. Exact structural contract: `photo-prompt-clause-ledger/v1`

Suggested record:

```json
{
  "contract_version": "photo-prompt-clause-ledger/v1",
  "clause_id": "clause-0007",
  "source_span_ids": ["request-span-03"],
  "provenance_kind": "requester_exact",
  "selected_candidate_id": null,
  "selected_visual_profile_id": null,
  "owner_dimension": "focus",
  "actor_object_id": "subject-1",
  "region_id": "eyes",
  "panel_shot_id": "panel-2",
  "time_beat_id": null,
  "variant_id": "variant-a",
  "polarity": "positive",
  "requirement_mode": "all_of",
  "priority": "P0",
  "literal_prompt_evidence": "keep both eyes sharp",
  "semantic_effect_group": "panel-2-eye-legibility",
  "compatible_clause_ids": [],
  "conflicts_with_clause_ids": [],
  "resolution_state": "resolved",
  "thumbnail_gate_ids": ["panel-count-and-eye-role"],
  "native_gate_ids": ["both-eyes-in-focus"],
  "nonpixel_status": null
}
```

Rules:

- exact source provenance is immutable;
- advisory candidates become authored clauses only after explicit selection and remain labeled advisory-origin;
- every active P0/P1 clause must bind to a gate or an explicit nonpixel/unscored reason;
- profiles remain the owner of profile component semantics; the ledger stores selection and mapping, not a copied profile body;
- one-of branches receive separate `variant_id` values and are never counted simultaneously.

### 2. Exact structural contract: `photo-prompt-clause-consistency/v1`

Suggested fields:

```json
{
  "contract_version": "photo-prompt-clause-consistency/v1",
  "active_variant_id": "variant-a",
  "unresolved_placeholders": [],
  "unscoped_clause_ids": [],
  "candidate_conflict_pairs": [],
  "hard_conflict_pairs": [],
  "resolved_by_hierarchy": [],
  "resolved_by_scope": [],
  "resolved_by_polarity": [],
  "resolved_by_requirement_mode": [],
  "status": "pass"
}
```

The detector may use lexical pairs for candidate recall, but only typed ledger comparison may emit a hard conflict. A hard conflict must name both clauses and the shared scope that makes coexistence impossible.

### 3. Revision of `photo-authorial-prompt-budget/v2`

Keep the current 48–640 absolute boundary, 360-word recommendation, and evidence-adjusted ceiling until an independent evaluation justifies changing them. Add diagnostic fields rather than a competing budget contract:

```json
{
  "hard_evidence_word_count": 0,
  "connective_optional_headroom": 160,
  "words_by_priority": {"P0": 0, "P1": 0, "P2": 0},
  "words_by_owner_dimension": {},
  "semantic_effect_group_count": 0,
  "duplicate_effect_groups": [],
  "unowned_clause_ids": [],
  "optional_prose_word_count": 0,
  "randomizer_branch_word_count": 0,
  "active_variant_word_count": 0,
  "compression_candidates": [],
  "budget_status": "pass"
}
```

Budget policy:

- count only the active variant toward the final prompt, not the complete randomizer library;
- preserve P0/P1 literal evidence before compressing P2 finish prose;
- compress repeated effect groups before deleting distinct gates;
- treat below-minimum or above-maximum length as an auditable condition, not automatic pixel quality;
- a prompt that cannot fit all hard evidence must escalate rather than silently drop obligations.

### 4. Research/ingestion contract: `photo-corpus-prompt-lineage/v1`

Suggested fields:

```json
{
  "contract_version": "photo-corpus-prompt-lineage/v1",
  "post_id": 2545,
  "shortcode": "DcQzmaomt-X",
  "prompt_sha256": "...",
  "source_language": "en",
  "source_payload_kind": "text",
  "prompt_role": "image_spec",
  "reference_required": true,
  "reference_available": "unknown",
  "modality": "still_image",
  "artifact_roles": [
    {"image_index": 1, "sha256": "...", "role": "unknown"}
  ],
  "translation_rows": [
    {
      "target_language": "ko",
      "source_prompt_sha256": "...",
      "translation_sha256": "...",
      "translator_version": "...",
      "alignment_status": "reviewed_aligned",
      "drift_dimensions": []
    }
  ],
  "candidate_extraction_status": "eligible"
}
```

Minimum `prompt_role` enum:

- `image_spec`
- `video_spec`
- `edit_instruction`
- `reference_dependent_request`
- `meta_generator`
- `analysis_prose`
- `non_image_metadata`
- `unknown`

Minimum `artifact_role` enum:

- `input_reference`
- `generated_output`
- `storyboard_or_contact_sheet`
- `comparison_or_example`
- `unknown`

Candidate extraction must exclude or quarantine `analysis_prose`, `non_image_metadata`, unresolved `unknown`, and reference-dependent rows whose only observable content is unavailable. `meta_generator` should be parsed into option branches before any candidate frequency is counted.

### 5. Advisory retrieval provenance

Existing candidate packs should add or preserve, rather than flatten:

- `retrieval_method`: exact alias, BM25F, embedding, fusion, manual selection;
- `retrieval_score` and `retrieval_rank`;
- `source_candidate_id` and source version/hash;
- `selection_state`: retrieved, reviewed, selected, rejected;
- `selection_reason`;
- `promoted_clause_ids`;
- `exact_source_overlap`: none/partial/exact;
- `hard_activation_allowed`: false unless an exact source/profile rule independently permits it.

Retrieval metadata is advisory provenance. It is not literal evidence and must never be copied into `source_span_ids`.

## Thumbnail and native-resolution gates

Prompt architecture has a preflight stage and a pixel stage. Passing preflight cannot satisfy a pixel gate.

### Preflight gates

1. Every active P0/P1 clause has exact source or selected-candidate provenance.
2. Every clause has owner dimension, actor/object, relevant region, panel/shot/time/variant scope, polarity, requirement mode, and priority.
3. Every hard clause maps to at least one thumbnail/native gate or a named nonpixel status.
4. No unresolved placeholder/reference remains.
5. No same-scope hard conflict remains.
6. One-of branches are separated and only one active branch is composed.
7. Exact source provenance is not replaced by a translation or retrieval paraphrase.
8. Prompt budget is computed after semantic-effect grouping and active-variant selection.

### Thumbnail gates

At reduced scale, require the P0 proposition and gross ownership topology to remain legible:

- correct principal actor/object/action/target relation;
- correct gross panel/shot count and reading order when a single image contains them;
- correct dominant placement, crop class, and directional relation;
- no P0 element silently replaced by an advisory candidate;
- if a clause is only natively observable, its thumbnail status is `not_applicable`, not failed.

### Native-resolution gates

At native resolution, test the fine clauses that actually require detail:

- material/texture distinctions and local light response;
- hand/object contact, small occlusion, and anatomy topology;
- exact readable or intentionally unreadable text requirements;
- fine appearance anchors and reference-conditioned details when the reference is available and role-labeled;
- focus-plane ownership, small count, surface state, and micro-artifact exclusions;
- translation-sensitive quantities, polarity, and actor/region ownership after reviewed alignment.

### Status rules

- unchosen randomizer branch: `not_applicable`;
- missing required reference: `unscored_reference_missing`;
- unknown image artifact role: `unscored_artifact_role_unknown`;
- non-image prompt payload: `not_applicable_image_spec`;
- prompt audit passed but no pixel inspected: `pixel_unscored`;
- partial hard-gate success: fail under `partial_is_fail`, never silently average to pass.

## Regression and held-out tests

### Positive structural regressions

1. **Region-scoped focus:** `subject sharp, background soft` must pass consistency and create different region owners.
2. **Source-role lighting:** `hard key, soft fill` must pass and bind to different light-source roles.
3. **Panel-scoped gaze:** direct gaze in panel one and off-camera gaze in panel two must pass.
4. **Layout versus organic asymmetry:** centered/symmetric poster layout plus natural facial asymmetry must pass.
5. **Positive/negative medium:** photorealistic plus `no illustration` must pass as positive plus requester exclusion.
6. **One-of generator:** exactly one selected option is active; unchosen branches are N/A and excluded from final word count.
7. **Anchor plus decomposition:** a concise `LIGHTING ANCHOR` and necessary key/fill/shadow component clauses remain distinct, compatible evidence rather than false duplicates.
8. **Exact source versus advisory:** a BM25F candidate may be retrieved but cannot populate requester span IDs or activate a hard profile.
9. **Duplicate prompt lineage:** posts 2542 and 2545 retain separate post, caption, image, reference, generation, and review lineage despite identical prompt hashes.
10. **Reference-only blocked state:** post 1799 becomes unscored/blocked without an available role-labeled reference, not quality zero.

### Hard-negative regressions

1. **Same-frame crop conflict:** full body and face-only crop, same subject/panel/time/variant, both P0 all-of, must fail.
2. **Same-layer text conflict:** no readable text anywhere plus an exact readable title in the same layer must fail unless one is explicitly a quoted negative or another output variant.
3. **Same-beat gaze conflict:** eyes closed plus direct eye contact, same subject and instant, must fail.
4. **Count conflict:** exactly three panels plus exactly four panels in the same variant, without hierarchy, must fail.
5. **Missing binding:** unresolved `@image_2` must block composition.
6. **Translation negation loss:** a reviewed target string that drops `do not copy identity` must fail alignment and cannot harden.
7. **Translation owner drift:** `her left hand holds the cup` translated as the other actor's hand must fail alignment.
8. **Bilingual duplicate inflation:** aligned duplicated clauses must count as one semantic effect group for budget diagnostics.
9. **Meta contamination:** posts 2286 and 2628 must be rejected/quarantined from image-spec candidate extraction.
10. **Artifact-role ambiguity:** a character sheet or input reference cannot be scored as a failed final output until its role is known.

### Held-out coverage

The controls must include more than single-subject portraits:

- product packshot with exact printed versus intentionally blank label regions;
- food scene with foreground garnish sharp and table/environment soft;
- architecture interior with multiple rooms/planes and no human subject;
- documentary process with actor/tool/workpiece ownership;
- multi-subject interaction with separate gaze/contact clauses;
- multi-panel graphic with different shot scales and one text-bearing panel;
- video/storyboard with repeated actor identity but time-scoped actions;
- reference edit where style transfers but composition/identity explicitly do not;
- bilingual prompt with reviewed equivalent wording and another with intentional culturally specific non-equivalence;
- randomizer with nested one-of and optional branches;
- non-image metadata and analysis prose controls;
- exact duplicate prompt body with distinct reference and generation lineage.

## Limitations and bounded decision

1. The full-corpus counts are lexical heuristics. They are useful for recall and test design, not semantic prevalence or contradiction rates.
2. Only 28 of 4,908 images were directly inspected. No sampled pixel proportion is generalized to the full image corpus.
3. The first two files per selected post were inspected deterministically, but the manifest does not identify input reference, output, storyboard, or comparison roles.
4. Model, version, seed, complete request envelope, reference bytes, rejected generations, selection process, and post-processing are not established for every post.
5. The translation snapshot cannot be safely joined to manifest prompt rows. Translation drift is therefore a proposed evaluation design, not a measured corpus rate.
6. Exact identity preservation and same-person status were not evaluated. Pixel observations are limited to visible appearance, styling, action, capture, and spatial relations.
7. No external source was required: the frozen corpus, directly inspected pixels, and repository-authored contracts were sufficient for this architecture study.
8. No runtime code, asset, index, test, candidate pack, prompt, or render was changed or qualified.

Bounded decision: **proposed**.

- Proposed exact structural contracts: `photo-prompt-clause-ledger/v1`, `photo-prompt-clause-consistency/v1`, `photo-corpus-prompt-lineage/v1`.
- Proposed revision: extend `photo-authorial-prompt-budget/v2` with ownership/effect-group diagnostics; do not replace it.
- Proposed exact visual-obligation profiles: **none**. Reuse the existing exact profiles selected from literal source evidence.
- Unverified: runtime integration, schema migration, prompt budget calibration, translation alignment, image-role recovery, regression implementation, new renders, pixel qualification, and user judgment.

## Evidence appendix

### Pixel sample and inspected paths

All paths are relative to `generated/reactorprompt-export-20260902-incremental/`:

| Post | Inspected files |
|---:|---|
| 1799 | `images/1799_DZSPKOvmhQF_01.jpg`, `images/1799_DZSPKOvmhQF_02.jpg` |
| 1897 | `images/1897_DZsDnRbGvza_01.jpg`, `images/1897_DZsDnRbGvza_02.jpg` |
| 1927 | `images/1927_DZ2hDNGmlld_01.jpg`, `images/1927_DZ2hDNGmlld_02.jpg` |
| 1998 | `images/1998_DaH-6uQGv4P_01.jpg`, `images/1998_DaH-6uQGv4P_02.jpg` |
| 2171 | `images/2171_Da2cYqGmsCX_01.jpg`, `images/2171_Da2cYqGmsCX_02.jpg` |
| 2286 | `images/2286_DbTdiCnmtuB_01.jpg`, `images/2286_DbTdiCnmtuB_02.jpg` |
| 2305 | `images/2305_DbctI1qmkn9_01.jpg`, `images/2305_DbctI1qmkn9_02.jpg` |
| 2311 | `images/2311_DbX4S5XGmns_01.jpg`, `images/2311_DbX4S5XGmns_02.jpg` |
| 2471 | `images/2471_DcAcq6LGuaR_01.jpg`, `images/2471_DcAcq6LGuaR_02.jpg` |
| 2542 | `images/2542_DcQz7tWmu9k_01.jpg`, `images/2542_DcQz7tWmu9k_02.jpg` |
| 2545 | `images/2545_DcQzmaomt-X_01.jpg`, `images/2545_DcQzmaomt-X_02.jpg` |
| 2556 | `images/2556_DcQElb4Gjy8_01.jpg`, `images/2556_DcQElb4Gjy8_02.jpg` |
| 2628 | `images/2628_DcgPtJoGg_S_01.jpg`, `images/2628_DcgPtJoGg_S_02.jpg` |
| 2741 | `images/2741_Dcx0xZ8mlev_01.jpg`, `images/2741_Dcx0xZ8mlev_02.jpg` |

### Reproducibility commands

Corpus and word-band scan:

```bash
python3 - <<'PY'
import json, re
from collections import Counter
rows = [r for r in json.load(open('generated/reactorprompt-export-20260902-incremental/manifest.json'))
        if isinstance(r.get('prompt'), str) and r['prompt'].strip()]
words = [len(re.findall(r'\S+', r['prompt'])) for r in rows]
print(len(rows), len({r['prompt'] for r in rows}))
print(Counter('<48' if n < 48 else '48-360' if n <= 360 else '361-640' if n <= 640 else '>640'
              for n in words))
PY
```

Architecture-recall pattern definitions used for the count table:

```python
checks = {
    "reference/source marker": r"\b(reference|attached|uploaded|supplied|@image[_\s-]?\d|image[_\s-]?\d)\b|첨부|업로드|참조|레퍼런스",
    "identity/copy boundary": r"\b(identity|same person|distinct facial|do not copy|preserve (?:her|his|their|the) (?:exact )?face|face unchanged)\b|정체성|얼굴.*그대로|닮지",
    "randomizer/one-of": r"\b(random(?:ly|izer)?|choose (?:exactly )?one|select (?:one|a)|one of)\b|무작위|랜덤|하나를 고",
    "negative/exclusion": r"\b(no|without|avoid|do not|never|exclude|must not)\b|금지|없(?:이|는)|하지 마|피하",
    "negative header": r"(?im)^\s*(?:negative prompt|negative constraints?|avoid|금지(?:\s*사항)?|네거티브)",
    "section/header": r"(?im)^\s*(?:[A-Z][A-Z0-9 _/-]{2,}:|\[[^\]]{2,40}\]|[#]{1,4}\s+)",
    "placeholder/reference token": r"\{[^{}]+\}|\[[A-Za-z0-9_ -]{2,}\]|<[^<>]+>|@image[_\s-]?\d"
}
```

The non-image/meta recall additionally searched metrics, prompt-analysis, sharing, and community phrases such as `조회수`, `좋아요를 받은`, `views`, `followers`, `community chat`, `please share`, `permission to use`, and `photo today`. Every such hit requires role review; the regex is not an exclusion classifier.

Manifest prompt and image lineage inspection:

```bash
jq '.[] | select(.id==2542 or .id==2545 or .id==2556 or .id==2628) |
    {id, shortcode, source_thread_id, originalIndex, prompt_source, caption, prompt, images}' \
  generated/reactorprompt-export-20260902-incremental/manifest.json
```

Frozen authored-policy inspection:

```bash
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json |
  jq '{schema_version, activation_policy, evidence_policy, retrieval_policy, precedence}'
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json |
  jq '{version, semantic_policy, slot_priorities, slot_pick_order, coherence_rules}'
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json |
  jq '{schema_version, intent_routing, visual_proposition, selection_balance, applicability_guards}'
```

Translation join diagnostics:

```bash
python3 - <<'PY'
import json
rows = [r for r in json.load(open('generated/reactorprompt-export-20260902-incremental/manifest.json'))
        if isinstance(r.get('prompt'), str) and r['prompt'].strip()]
tr = json.load(open('generated/reactorprompt-export-20260902-incremental/raw/translations.json'))
en = tr['en']
values = {v for v in en.values() if isinstance(v, str)}
positional = sum(en.get(f"prompt_{r['originalIndex']}") == r['prompt'] for r in rows)
anywhere = sum(r['prompt'] in values for r in rows)
print({k: len(v) for k, v in tr.items()}, positional, anywhere)
PY
```

### External sources

None. No external source was materially necessary for the bounded corpus and repository-contract findings above.
