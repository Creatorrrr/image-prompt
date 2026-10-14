# Native fact modes and complete effect coverage: design only

This note is a proposal, not an approved schema, source correction, native qualification, or implementation. This worker edited only this new note in this follow-up. No production code/data, source effects, tests, index, runtime publication, global report, or Git state was changed. No inference, provider, Gemini, or network was invoked. Source reads used local JSON/gzip and existing Python standard-library parsing inside a network-denied, empty-environment sandbox. No new test results are claimed.

## Current evidence and scope

I read the current v2 implementation after root commit `17c868257`, current `photo_contracts.py`, `photo_candidate_realizations.py`, `photo_slot_semantics.py`, and `prompt_generator.py` admission code; the plan at `docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md` (especially stages 2 and 5); `NATIVE-QUALIFICATION-ISSUES.json`; `NATIVE-EVIDENCE-CONTRACT-VERIFICATION.json`; frozen `SOURCE.json.gz`/`ORDER.json`; the 11128 root-authored correction and selected source/spec examples below. The verification artifact reports source hash `125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b`, 18,250 source records, and 0 native-qualified records. Its 127 tests/107 subtests, existing closure/publication/acquire checks and zero inference are root's recorded validation, not rerun by this design worker.

Current v2 correctly rejects explicit null/empty/false native proof instead of activating absent-proof fallback. Preserve this distinction. V2 nevertheless conflates role meaning with mutation: every role fact must match `realizations.effects(record, rid).properties`, and `existing_owner_allowed` gathers prerequisites only from role evidence. There is no independently complete inventory of source semantic facts or carrier obligations on actual effects that lack a displayed role. `core_entry_eligible` requires all declared affected dimensions to be explicitly open and separately checks property locks. Therefore adding `age` merely to support a declared-age role creates a false age mutation and prevents ordinary use when age is frozen.

The plan already requires distinguishing source-declared context/preservation from actual effects, auditing whole effects/profile/member scope, preserving intrinsic guards, and versioning source/reader/proposal/validator contracts without a permissive legacy fallback. This design fits those requirements; it does not infer facts from slots or treat complete textual source review as native adoption.

## Actual local source cases and counterexamples

All ordinals below are zero-based `ORDER.json` positions, not inferred tags. Positive quotes are exact strings/substrings of the cited source fields. Effects listed as original are frozen SOURCE records. Root review corrections remain proposals; they are not silently described as canonical changes.

### 11128: declared adult versus changing age

Candidate `cand_17f21e3dd66a5d1aa97b3b38efaab469`, `/content/en`:

> adult wearing a pencil skirt in a natural standing or walking posture

Its `/content/contextual_usage/contexts/0/application_conditions/1` says:

> Every mentioned actor, object, garment and place outside the declared change scope must already be established in the frozen core; otherwise the candidate is inapplicable.

Another application condition preserves established reference appearance and requester-owned identity. Original effects are dimensions `appearance, material`, with `main_subject / wardrobe`; original conditions contain `for_any: human`. Root's explicitly reviewed `authored/root_11128_choices.py` proposes `standing`/`walking` render branches, common `age.declared`, `wardrobe.ensemble`, `body.pose`, a walking-only `action.walking`, and an adult-context condition. Root rationale explicitly calls adulthood already declared and forbids inferring it from skirt shape.

Proposed fact-mode correction: `adult` supports an intrinsic **prerequisite** `main_subject / age.declared = adult`, not an age mutation. Wardrobe and posture remain actual changes unless an explicitly source-supported preservation use has separately been reviewed. Walking adds its action effect only on walking. Material or framing must not be reintroduced from absent source evidence. The root proposal's age mutation must be explicitly corrected and fully rereviewed before v3 qualification; merely relabeling an existing effect as prerequisite cannot remove its lock obligation.

A frozen 30-year-old core can supply a separately authored, span-grounded `age.declared = adult` assertion. Do not derive this automatically from a number, the word human, skirt, appearance, `adult_allowed`, another optional cue, or the candidate itself. An adult secondary actor does not satisfy the primary owner's prerequisite. A core that gives only a minor/unknown age fails. Even with adult prerequisite satisfied, locked wardrobe/posture still deny actual changes.

Important existing-code distinction: `contract.adult_allowed` is computed from human/nonsexual context plus adult domain or adult-appeal intensity; it is not proof of declared adulthood. The existing `requires_adult_context` guard must not be silently repurposed as an exact age witness or removed through fact modes. Any guard correction needs its own explicit source/policy review. Age evidence, permitted treatment, and sexual-tone constraints stay separate.

### Face presence is not skin/anatomy mutation

`cand_9c8f24f563ae57148d6b44472bdead38`, `/content/en`:

> underlit face horror

Original effects declare only lighting and no concrete properties. A legitimate refinement would independently review face presence as a prerequisite and illumination as an effect on a declared receiver; `horror` also needs an explicit reviewed disposition instead of being dropped because the tag is lighting. A frozen face-bearing teacup depiction can supply a face carrier if that exact representation is declared. A plain teacup or unspecified robot cannot. Underlighting does not thereby grant a new face, new species, new skin tone, or altered face geometry.

Ordinal 467, `cand_97a0b7731a8458448e49feefab4c15ad`, says `wet mud caked skin texture`; original material dimension has no properties. Existing skin is prerequisite; caked mud/visible surface state is a possible actual effect and is not preservation just because skin already exists. Ordinal 653, `cand_f84864db8c935fc49fd4d8525090f1ec`, says `UI projection cast onto skin`; existing receiving skin, projected pattern, and any actual emitted UI/light/visible text effects need separate review. A generic `skin` carrier never authorizes all those effects.

Counterexamples with explicit identity consequences: ordinal 890 `cand_a14eb7881f4750e4805585f99a28b309` says `a pointed ear and tail trait set` but currently has empty effects; ordinal 912 `cand_74140d53214251308fcc028b14da05f4` says `intense slit-pupil gaze` but currently declares expression only. Existing actor/eyes cannot turn newly introduced ears/tail/pupil shape into carrier-only prerequisites. If preservation of exactly already-declared traits is actually intended, exact frozen trait values must be witnessed and the entire usage/effect correction explicitly reviewed. Otherwise the actual anatomy/species/appearance changes remain effects or qualification remains pending.

### Existing focus versus a new focus choice

Ordinal 710, `cand_88b4db9dfee155ef8c2b1de640e5c3fa`, `/content/en`:

> precise focus on the eyes

Original effect dimension is camera, with empty concrete properties. The focus spec describes placement/priority of the focus plane and named planes' relative sharpness. Existing eyes are prerequisite; selecting/reprioritizing the eye focus plane is an actual camera effect and must respect frozen focus. Do not label this preservation merely because a face already exists or the result would look plausible.

Ordinal 3939, `cand_3055a98268eb5ef5b8576b26c9c6dc98`, `/content/en`:

> fixed-ROI time-series acquisition maintaining the same landmark, field and focus relationship

Original effects are empty; microscopy is only a current routing prerequisite. The `maintaining the same ... focus relationship` phrase can support **preservation** of an exact already declared focus relation. It does not choose a new focus plane or silently change optics. The same source also mentions ROI, landmark, field, and time-series acquisition: each needs disposition. Preserving focus alone cannot exempt a newly added acquisition method/time structure from effect checks, or certify that a single still image proves time-series acquisition. If no exact frozen focus relation is available, preservation cannot be instantiated. This case is a full-cue rereview requirement, not a ready-qualified focus candidate.

### Existing prop identity versus adding an object

Ordinal 83, `cand_a0a928e2615c55aa9f84f637391bf07f`, `/content/en`: `a violin bow prop`; original effects are empty. The noun does not state whether a bow is already present or is to be added. A `prop` tag or `carrier: object` cannot resolve that ambiguity. An addition requires an explicitly reviewed inventory/identity/count/placement footprint and permission for its actual affected scope. An already-present-bow use needs the exact frozen object identity and type/value, not an unrelated violin bow on a background poster. No mode can be selected automatically by matching candidate words to the core; ambiguous usage remains pending until the source/use contract is explicitly clarified and rereviewed.

An actual existing-object contrast is ordinal 10929, `cand_5ed028784dfa54d3a320233188ec990d`, `/content/en`:

> Composition preserves the already requested source-scoped relation: The staff rests in the figure's proper left elbow bend and leans against the same-side shoulder.

Its effect is `image_plane / layout` under composition. Existing exact staff/figure identity and elbow–shoulder relation are prerequisites/preservation; changing composition to make that relation readable is a distinct possible effect. The source does not license adding another staff, making a right-side relation left-side, or moving the staff while claiming only composition changed. Explicitly bind the same figure, proper left elbow, same-side shoulder and staff; a second figure's matching pose is insufficient.

Ordinal 11337, `cand_2362f777c3ed514db65b7a271ed5a7bc`, says `the specified padding belongs inside the already chosen garment; the garment outer contour reflects that specified padding; the actor anatomical proportions remain separately specified`. Original effect is appearance / main_subject / body.garment. Garment identity/padding ownership and actor anatomy preservation must be distinct from any garment-shell contour change. Do not change the actor's body volume by hiding it behind a garment effect or invent padding from a generic garment carrier.

## Three design options

### A. Extend role facts in place, plus an independent whole-record obligation ledger

Add `mode` and typed values/requirements to existing role evidence, but require a separate per-RID ledger that covers every actual effect, prerequisites and preservation constraints even when no role cites them. Keep role evidence source/spec/RID-bound. This is the smallest-looking code change and can preserve much v2 shape.

Cost: the same fact can be duplicated in several roles and in the whole ledger with disagreeing modes, values, owner bindings or carrier prerequisites. It therefore needs stable shared fact IDs and equality checks anyway. A role being added/removed must not change the whole cue's effect eligibility. I do not recommend maintaining independent duplicated fact bodies.

### B. Per-RID source fact inventory; roles reference facts; complete effects are checked independently — recommended minimum

Introduce one versioned native semantic contract (`v3` proposal) with a complete fact inventory per actual RID. Roles reference immutable fact IDs rather than owning duplicate facts. The actual canonical `effects` structure remains the mutation authority until explicitly source-corrected; mode metadata cannot subtract effects at runtime. Every expanded actual effect has a reviewed inventory effect fact and all its own prerequisites, whether or not any role displays that fact.

Four authored modes have separate meanings:

| Mode | Admission obligation | Mutation permission |
| --- | --- | --- |
| effect | Match an actual canonical effect reference; obey all affected dimension/property/owner/whole-cue locks and prerequisites | Only this mode describes the reviewed actual mutation/added constraint |
| prerequisite | Match a positive typed frozen-core fact with exact bound owner, property/relation and value | None; candidate/other optional cues cannot be the witness |
| preservation | Bind an exact frozen value/relation and verify the candidate preserves it; retain that obligation through rendering/composition | None for the preserved property; any separate visibility/layout change remains an effect |
| context | Preserve explicitly source-stated interpretation/provenance/applicability meaning with no automatic visible consequence | None; cannot add place/person/occupation/mental state/physical cause |

Normative context that constrains an owner/value must also have an explicit prerequisite obligation; naming it context cannot waive its witness. Optional interpretive context, such as ordinary-office usage of a skirt, does not create an office or turn office context into a mandatory prerequisite. A contextual role may cite context only when its actual spec explicitly supports that non-rendering meaning and the proposal/renderer carries that limitation. `semantic_role=contextual` is not the same enum as fact `mode=context`; direct/contextual role semantics and optional adoption policy remain separate.

Prerequisite/preservation facts can support semantic role discovery where the reviewed spec actually covers declared/preserved meaning, such as declared age, but `matched_properties` must no longer imply mutation. Return explicit `support_mode`/`fact_refs` separately from the whole cue's actual mutation footprint. Adopting an age-supported role cannot strip the same cue's wardrobe/pose effects. An unsupported contextual interpretation cannot become positive visible evidence just by using a read-only mode.

This option closes both v2 failures without a renderer-wide transaction calculus. Source corrections and explicit typed core witnesses are still necessary before qualified adoption.

### C. Fully explicit source operation graph plus request-specific application plans

Record source-bound operations and owner/entity relations as a complete graph; a request-specific frozen plan binds exact core owners/values, effect operations, preserved invariants, required context, emitted text segments and actual selected member branches. The executor checks a proof-carrying before/after delta against frozen intent. This can express genuine source-supported alternative uses, distinct owners, part hierarchies, and value-preserving applications precisely.

Cost: new normalization, composition/audit/receipt contracts and a much larger verification surface. A request planner must not decide that an equal-looking mutation becomes preservation, manufacture a missing existing prop, or invent a new RID. Every operation/application alternative still needs source-supported manual authoring and explicit guards. This is a later extension of B, not a reason to delay B's complete coverage invariant or silently loosen v2.

## Concrete minimum contract for option B

A fact conceptually has `{fact_id, source_candidate_id, actual_realization_id, pointer, quote, dimension, target, property, mode, typed_value_or_relation, prerequisites, review_binding}`. Effect-mode fields additionally require an authored operation and exact effect references. Mode-specific fields are exact schemas, not an open free-form bag. This is a shape proposal, not a written native record.

- **Bindings:** retain complete meaning hash, catalog/spec hashes, exact positive pointer/quote, actual selected RID, reference closure hashes, reviewed source correction identity, and explicit native metadata author/review provenance. Negative/routing/review/claim-limit metadata cannot supply positive facts. Branch-specific quote paths cannot borrow another RID. No null/empty/false proof fallback; missing mode/values/coverage means incomplete qualification.
- **Values:** values use declared typed namespaces and exact canonical equality; for adult, e.g. `{type: declared_age_category/v1, value: adult}` under `age.declared`. Structured relations identify every participant, side, predicate, and relevant value. No fuzzy/lexical/category entailment. `exists: true`, `already_exists`, or a free generic carrier name is not an identity/value witness.
- **Actual operations:** an effect records its reviewed operation, such as add_entity, set_value, remove_entity, relocate, or select_plane, and the exact affected owners/value/receiver scope. The enum is a versioned contract, never guessed from property paths. A newly added bow has an explicitly introduced source-local entity ID and an actual permitted inventory operation; it cannot masquerade as a pre-existing frozen owner. A later effect using an entity introduced by another selected effect needs an explicit source-bound dependency and both effects must remain permitted. Such an internal dependency never satisfies a prerequisite that explicitly requires an owner already present in the frozen core. Source wording that does not distinguish addition/retention remains pending instead of receiving an operation default.
- **Grounded core:** a required assertion must name active exact source span IDs, frozen baseline evidence, explicit owner/property and typed value. Existing core axes can transport flat `fact_owner`, `fact_property`, `fact_value_type`, `fact_value` strings, but a consumer must validate their schema; generic axes currently normalize scalar/list strings, so arbitrary nested value objects must not be smuggled through stringification. Structured relations/owner graphs need an explicitly versioned wire extension or bounded explicit assertion representation. Positive subject/type/category or keyword lists alone do not supply this fact.
- **Owner binding:** match source-local owner variables to exact explicitly declared frozen core entity IDs. If a candidate refers to one face/garment/staff, bind its actual carrier node or an explicitly unique part relation, not any node of that type. A named secondary owner remains secondary. Multiple possible owners or unknown identity means review required, never choose the first matching word.
- **Prerequisite witness:** the bound core fact must exactly match owner/property/relation/value and required polarity. A source fact, a tag/facet, retrieval similarity, or another optional picked candidate cannot witness its own prerequisite. Conflicting excluded/frozen facts cannot be outvoted by an existential carrier type.
- **Preservation:** either match an explicit source value or bind a source-supported `same_as_frozen_core` value reference to one exact grounded core fact. Seal the resolved value/reference digest in the application receipt and audit it after composition. The reference supplies an already frozen value; it is not permission to invent an unspecified value. If the core lacks the required exact relation, preservation is unbound. Source `maintaining the same` can support such a reference; plain `precise focus on the eyes` does not automatically do so.
- **Mode support:** each role records referenced fact IDs and a manually reviewed mode-support rationale bound to its actual spec. Existing property/dimension/spec boundary checks continue on the semantic support fact even when it is non-mutating. Effects/prerequisites on other properties stay in the whole-cue ledger instead of being forced to fit the displayed slot. Native proposals distinguish semantic support from actual candidate adoption eligibility.

### Whole fact/effect coverage invariants

For RID r, let E(r) be the **actual expanded effect set**, from canonical base + selected branch, exactly selected member references, profile/concept effects actually consumed, and explicit joint effects. Preserve source owner/property/dimension and origin references. Do not union unselected branches or optional members; do not omit a member because it lacks a displayed role. Coarse/wildcard/dimension-only effects need an explicit reviewed disposition and cannot become an empty allowed set.

Require both directions:

1. Every e in E(r) is linked to at least one mode=effect fact bound to that exact effect origin/signature and RID. Every such fact carries an explicitly reviewed complete prerequisite list, including [] only after actual review.
2. Every mode=effect fact resolves to actual E(r), not a prerequisite/context/preservation row or a different RID/member. There are no orphan mutation claims and no canonical effects excused by non-effect mode labels.
3. Every non-effect fact remains outside the mutation footprint. If the same canonical effect still exists, a non-effect label cannot absorb it; qualification fails until the effect is covered as an effect or an explicit corrected source/review removes it.
4. Whole-cue eligibility checks all E(r) effects and the complete fact obligations, regardless of displayed role. Thus an age role cannot hide an untagged face-lighting effect with a missing face carrier, and a new tag cannot weaken conditions.
5. A manually reviewed source-unit ledger accounts for each semantically active selected positive body/branch/member passage, intrinsic conditions and preservation/negative obligations. Units have exact pointers/quotes (and optionally offsets), fact refs or an explicit non-semantic disposition, plus a whole-source review attestation/hash. Do not count metadata strings as positive visual facts or manufacture effects for connective text. Mechanical equality proves coverage against the authored ledger, **not** that a reviewer extracted every clause correctly. Existing erroneous/empty canonical effects therefore still require full semantic rereview rather than a claim that set equality proves truth.
6. Runtime compact projection retains modes, typed values/value refs, owner binding requirements, complete E(r) obligation coverage and hashes; it may drop source prose only after full validation/sealing. Full and compact admission must produce the same selected-RID decision and reasons. A trimmed role-only compact guard is insufficient.

Source effect corrections are first-class reviewed changes: before/after exact record, rationale for each added/removed/narrowed property/dimension, full text and dependency rereview, new source/catalog/reference bindings, and fresh regression evidence. A narrower precise effect set cannot inherit the old coarse effect's approval automatically. Neither mode authoring nor runtime equality removes a conservative source lock footprint without this correction workflow.

## Owner identity and lock scopes

A canonical owner hierarchy and an explicit grounded equivalence/disjointness map are complementary:

- Stable source/core owner IDs carry exact authored spellings. Entity IDs are not parsed for anatomy. Alias edges mean **same entity**, supported by positive source/core evidence. `face_surface` is not automatically an alias for `main_subject`.
- `owned_part(face_A, actor_A)` is a **part hierarchy**, not full entity equality. A primary-subject lock can explicitly cover that entity and its owned parts. A face-specific lock covers that face's relevant property subtree, not a second actor's face. Depicted actor versus live actor and displayed equipment versus recording apparatus need distinct graph relation types; depiction is not identity equivalence.
- `disjoint(actor_A, actor_B)` requires explicit grounded distinct identity/count, not different target strings. Different spellings alone prove neither equality nor disjointness. Validate equivalence symmetry/transitivity, hierarchy acyclicity, and no equivalence/disjointness conflict. Shared property locks use explicit lock scope/receiver scope plus property ancestry independently of effect dimension.
- A whole-scene palette/light operation lists its actual receiver scope. Using `scene` or `image` as a fresh target cannot escape a frozen local garment/skin/actor light. If the declared scope can reach a locked receiver and disjointness/receiver exclusion is unresolved, deny that application pending review. Conversely, a proven separate actor/receiver can remain editable when its actual dimensions/properties are open and no whole-scene lock covers it.

Minimum safe behavior before this metadata exists is unresolved-owner denial for an overlapping locked property, with an explicit reason; do not flatten all targets globally or announce a permanent ban on second-actor changes. The prior note's property-only rejection was a conservative temporary option, not the desired identity contract. Exact hierarchy/equivalence/disjointness is the recommended design. No alias generation from face/body/person/robot strings or candidate tags.

## Proposed verification matrix (not implemented or run in this follow-up)

1. After an explicit approved 11128 correction removes false age mutation, an exact frozen primary adult + open wardrobe/pose admits standing; age remains locked. Walking additionally needs action permission. The other branch's action cannot leak.
2. The same candidate with minor/unknown age, only a secondary adult, `adult_allowed` only, the candidate's own adult quote, or a bare human carrier fails the adult prerequisite. No implicit age inference from outfit or numbers.
3. Keep canonical age.declared effect but relabel its only fact prerequisite: effect-coverage validation fails. Removing it without an approved before/after source correction fails review binding. Changed source/spec/member hashes invalidate all related modes.
4. Face underlighting permits a declared face-bearing depiction and denies no-face teacup/unspecified robot; it cannot change frozen face anatomy/skin tone. Caked-mud/skin projection actually modifying frozen surface/pattern cannot be relabeled existing-skin context.
5. Pointed ears/tail/slit-pupil additions need actual relevant mutation permission. A prior exact frozen trait can support only a separately source-supported preserved-trait use, with exact owner and values. Human/eye carrier existence alone is insufficient.
6. New eye focus fails frozen different focus; already-preserved focus succeeds only for a source-supported preservation use and exact frozen relation. The 3939 time-series/ROI/landmark clauses still need their own complete dispositions. Preserving focus does not waive a new acquisition/timing effect.
7. A violin bow addition without an existing exact bow needs its real inventory/count/placement permission. A preserved existing bow must bind its exact object identity; a second bow/poster does not witness it. Ambiguous noun-only source cannot acquire mode automatically.
8. Preserved staff relation checks the same staff/figure/proper-left elbow/same-side shoulder. Open composition can change readability but cannot move/add staff or invert laterality under preservation. Padding alters a declared garment shell only; actor proportions stay preserved.
9. Add a non-role actual effect requiring a face; choose only an unrelated wardrobe/age role: whole-cue coverage still requires the face. Missing effect prerequisite metadata, default [] or fake already_exists fails. Removing/adding a role does not change whole-cue admission.
10. Uncovered actual property, orphan effect fact, foreign effect origin/RID, omitted selected member/profile/joint effect, unselected member union, broad effect replaced by a narrow row without review, and mode/typed-value omission all fail.
11. Explicit equivalence/owned-part binds face_A to primary actor_A: frozen skin.color blocks the same property on that face across dimension changes. No edge: overlapping owner identity is unresolved, not silently disjoint. Grounded actor_B/face_B disjoint from A can be changed when its own scope is open. Conflicting hierarchy/equivalence/disjointness declarations fail.
12. Scene palette/light reaching a locked local receiver fails even with a different target string; an explicitly bounded disjoint receiver application can pass. Missing receiver scope is not an empty set.
13. Null/false/empty proof cannot activate old fallback. Full and compact decisions/selected facts/whole effects/preservation obligations agree for all positive and negative cases. Native schema changes require reader/proposal/validator/auditor/receipt integration; semantic fixtures do not prove pixels or full-corpus truth.

## Recommended next bounded step

Agree the option-B fact-mode/value/owner/coverage schema, then manually author a tiny uncommitted design fixture set for 11128, underlit face, 710/3939, existing staff versus ambiguous bow, and one whole-effect-without-role counterexample. Any actual source correction must be presented with exact before/after and complete rereview; first prove offline validators and full/compact parity on those cases before adopting canonical records. Preserve native-qualified=0 until such records are actually authored, corrected where necessary, fully validated, and integrated with their dependent source/index/runtime contracts. This note does not authorize or claim that implementation/publication occurred.
