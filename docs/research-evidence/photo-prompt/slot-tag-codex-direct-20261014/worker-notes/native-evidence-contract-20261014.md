# Native role evidence v2: scoped implementation and integration conditions

This worker changed only `skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py`, `tests/test_photo_semantic_evidence.py`, and this note. The two implementation files were already untracked task work when inspected. No AGENTS.md file was present at repository root; the task's supplied AGENTS instructions applied. No canonical corpus, slot binding, index, runtime publication, global report, other hook, or Git state was changed by this worker. No Gemini, embedding inference, model, network request, or other agent was invoked.

## Existing helper intent and observed gaps

The initial helper recorded a complete semantic review bound to source meaning and role specifications. Its compact projection was intended for already validated sealed layouts. The existing-owner guard intended to prevent a body-detail candidate from introducing a person onto an object, while keeping actual wigs and depicted actors possible. Those goals are retained.

The inspected v1 facts omitted realization IDs. Validation only required some evidence property to occur in each selected branch; it did not require every fact to belong to its own exact branch. Compact facts removed all branch attribution. `claim_limits` and `research_claim_limits` could supply quotes. Existing-owner admission inspected only roles with owner `actor`, unconditionally accepted human/animal subject categories, and guessed anatomy from depiction/wig/body-part keywords. Consequently a face-dependent lighting or framing fact could bypass the actor filter, and a generic robot or abstract sculpture could acquire anatomy without a declared carrier.

## Implemented contract and before/after behavior

| Concern | Inspected v1 | Implemented v2 |
| --- | --- | --- |
| Native fact shape | pointer, quote, dimension, target, property | Same five fields plus mandatory realization_id and required_carriers |
| Different facts per actual RID | Branches shared one unscoped fact pool | Every fact names one actual qualified RID; every qualified RID has facts |
| Property validation | At least one pooled fact matched each branch | Every fact matches its own RID's actual property effect |
| Branch-specific strings | Could borrow another branch's realization_content | realization_content pointers must name the fact's exact RID |
| Positive source | Negative/routing denial omitted claim limits | Claim limits, research claim limits, negative/routing/review containers are denied |
| Compact/full fit | Compact facts lost RID | Both select exactly the requested RID, retaining carrier prerequisites |
| Existing carrier | Category and keyword shortcuts; actor roles only | Explicit grounded carrier facts, across all role owners and dimensions |
| Missing carrier review | No native carrier declaration | Missing required_carriers rejects full validation and yields incomplete qualification |
| Object/material/general light | Could be blocked through actor assumptions | Explicitly reviewed [] declares no existing carrier prerequisite |

Native schema is `photo-candidate-role-evidence/v2`; no compatibility path upgrades v1. Each native evidence fact has exactly:

```json
{
  "pointer": "/content/en",
  "quote": "sidelight across face planes",
  "dimension": "lighting",
  "target": "image",
  "property": "lighting.face_side",
  "realization_id": "base",
  "required_carriers": [{"target": "main_subject", "carrier": "face"}]
}
```

`required_carriers: []` is a real semantic review decision. It must never be supplied automatically from a tag, keyword, coarse category, property name, or default-empty conversion. Multiple prerequisites are conjunctive. The affected property owner can differ from its carrier owner, as in image lighting that requires a particular depicted face. Target/property spelling retains the existing nonblank/no wildcard/no trailing-dot contract: named IDs, Korean owner names, and hyphenated names are accepted without renaming. Carrier types are explicit extensible lowercase dotted identifiers; `hair` grants no implication about face, fingernails, live actors, or other types.

Full qualification and compact guards preserve exact selected-RID attribution. Full validation rejects a foreign property even if another fact on that RID happens to match. It rejects unqualified/foreign RIDs, uncovered qualified RIDs, duplicate native facts, foreign branch strings, malformed carrier declarations, and stale source/catalog/spec bindings. Qualification returns distinct actual matching properties without duplicate property rows. Existing-owner admission rejects missing native RID/carrier metadata rather than overlooking such facts.

## Core v3 existing-carrier witness

The existing extensible semantic_assertions wire accepts this subject assertion without adding a noun classifier:

```json
{
  "assertion_id": "carrier_1",
  "dimension": "subject",
  "polarity": "required",
  "source_span_ids": ["request_1"],
  "axes": {"carrier_target": "secondary_depiction", "existing_carriers": ["face"]},
  "evidence": {"carrier": "a painted face on a separate panel"},
  "affected_dimensions": ["subject"]
}
```

Core normalization already binds request_binding spans to the exact requesting envelope and validates typed assertion fields. The guard additionally requires nonempty exact active source-span IDs, required subject polarity/dimension, subject in affected_dimensions, exact explicit carrier_target, a distinct typed carrier list, and nonempty evidence phrases occurring in frozen baseline_prompt_en. Advisory/excluded assertions, foreign span IDs, missing frozen evidence, other owners, and broad category labels do not supply carrier witnesses. A primary object can have an explicitly declared secondary depiction: only that exact secondary owner receives its face carrier. Face-bearing teacup depictions can qualify; an ordinary teacup does not. Named actors still need explicitly authored relevant carriers.

This validates grounding and explicit declarations mechanically, not the truth of an authored interpretation. It assumes the core has passed its normal envelope/core validator. A reviewer must still ensure that a source span and frozen phrase actually describe the claimed owner/carrier.

## Root integration conditions

1. Keep direct_review.py's five-field common facts and optional sixth realization_id contract. Expand common facts only into the actual reviewed RIDs; preserve explicitly scoped facts and their exact branch properties.
2. Add a separate manually authored native-carrier metadata review stage. Each expanded native fact needs an explicitly reviewed required_carriers value. An absent value is incomplete qualification, including for material/image/light facts whose correct reviewed value may be []. No default generation is authorized.
3. Bind each native proof to the exact resulting source meaning, catalog, and spec hashes after reviewed source corrections. Run full native validation before compact projection/layout sealing.
4. Root-owned core-authoring guidance needs to explain carrier_target/existing_carriers and exact owner spelling. The guard itself provides no noun/category inference or fallback anatomy.
5. Existing-carrier admission checks only existence. Root-owned permission/property locks remain independently mandatory. A declared face/fingernail does not grant permission to change a frozen property.
6. Canonical qualification is still incomplete until all relevant explicit native carrier decisions and source/RID facts are authored and validated. This worker did not qualify any canonical record and does not claim all 18,250 records are qualified.

## Root-owned owner-alias/property-lock investigation

`photo_contracts.py` was inspected but not edited. Its property lock target overlap uses textual dotted-prefix overlap. A narrow offline probe against the inspected implementation used a frozen main_subject / skin.color appearance anchor and a lighting effect on the same skin.color property:

- main_subject target: denied (False).
- face_surface target: allowed (True).
- secondary_depiction target: allowed (True).

The first allowed case is a bypass when face_surface denotes the same primary owner. The latter may represent a genuinely distinct owner and must not be silently aliased by word guessing. Dimension changes alone already cannot bypass an overlapping exact target/property lock.

Concrete suggested regression for root: anchor `{dimension: appearance, target: main_subject, property: skin.color}` and effect `{dimension: lighting, target: face_surface, property: skin.color}` must fail when source-owned owner equivalence says face_surface belongs to main_subject. Keep same-owner exact-target denial and cross-dimension denial. Separately test an explicitly grounded distinct secondary depiction and an unrelated unlocked property.

Conservative immediate patch option, if no explicit source-owned alias/disjoint-owner contract can be supplied yet: in `property_effects_allowed`, deny any overlapping locked property regardless of textual target spelling, i.e. replace the final conjunction of target and property overlap with property overlap alone. This closes spelling-based bypasses but intentionally also denies changing the same property on a genuinely separate owner until owner separation is explicitly represented. That limitation must be reported. Longer-term exact alternative: accept a source-grounded owner equivalence/disjointness map, canonicalize only explicitly equivalent owners, and fail closed on unresolved owner identity when the property overlaps. Do not manufacture owner equivalence from face/body/robot keywords. Root owns the final scoped patch and its compatibility decision.

## Offline validation

Final command (all inherited credentials/environment removed; network denied):

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_photo_semantic_evidence tests.test_photo_candidate_corpus tests.test_photo_candidate_realizations tests.test_photo_slot_semantics tests.test_photo_search_layout -q
```

Result: **81 tests passed**, including **29 native semantic evidence tests**, in 5.880 seconds in the final run. Tests cover distinct per-RID positive facts, per-fact properties, foreign branch strings, claim-limit/negative/routing/review rejection, compact/full equality, missing native metadata, teacup versus face-bearing depiction, wig hair versus fingernails, human/animal category without anatomy declarations, generic robot/abstract sculpture/named actor without guessed anatomy, face lighting and framing without actor role ownership, independent object/material/image-light slots, secondary owner carriers, image effects with subject prerequisites, exact Korean/named/hyphenated owner IDs, frozen property denial on the same owner, and compatibility with the current core-v3 typed assertion normalizer.

These are meaningful counterfactual fixtures and mechanical contract checks. They do not establish full-corpus semantic truth, retrieval quality, generated image pixels, or user acceptance. No image generation or embedding inference was run.
