# 07. Subject-prop interaction, contact, tool legibility, and object-state topology

## Status and bounded decision

- **Decision: proposed, unimplemented.** Add an opt-in, object-agnostic interaction-relation contract and coordinated candidate bundles. Do not make any observed prop, grip, or action pattern a global default.
- The proposal is narrower than a generic “hands look natural” rule. It represents `actor/effector -> contact or gap -> object affordance -> support/load path -> target -> visible state or consequence` as one owned relation.
- Exact hard gates apply only when the requester supplied the relation, an authorial semantic assertion locked it, or a narrow exact profile activated. BM25F/embedding retrieval and corpus frequency remain advisory.
- No runtime source, index, or test was changed. No new render was generated. Proposed render qualification and user judgment remain **UNSCORED**, not failed or zero-quality.

## 1. Scope and sampling method

### Frozen evidence boundary

- Corpus: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- Manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- Corpus scope: 1,182 posts, 4,908 delivered images, 924 non-empty prompt records, 904 unique prompt bodies, 258 missing prompts, post IDs 1565–2746.
- Authored-source inspection used the source hashes frozen by the shared brief. Unrelated concurrent working-tree edits were not treated as baseline evidence; generated semantic/profile indexes were not treated as authored sources.
- Evidence layers below remain separate:
  1. lexical prompt scan;
  2. direct observation of delivered corpus pixels;
  3. repository and contract inspection;
  4. design inference;
  5. future render qualification and user judgment, both currently unscored.

### Prompt scan

All 924 non-empty prompts were read programmatically. The scan used case-insensitive English lexical proxies because the stored prompt bodies in the sampled records are English. It counted both raw cue presence and conservative cue proximity:

- hand anatomy/control terms: `hand`, `finger`, `fingertip`, `thumb`, `palm`, `grip`;
- object/tool inventory: common held, carried, operated, consumed, displayed, and mounted nouns, plus generic `object`, `prop`, `tool`, and `product`;
- contact/control verbs: `hold`, `grip`, `grasp`, `carry`, `wield`, `pinch`, `support`, `touch`, and close variants;
- purposeful-operation verbs: `pour`, `stir`, `cut`, `write`, `type`, `adjust`, `fasten`, `feed`, `pluck`, `operate`, and narrowly constrained instrument play;
- transition phrases: `about to`, `paused halfway`, `reaching toward`, `handing`, `lifting`, `lowering`, `opening`, `closing`, `pouring`, `unsheathing`, `poised to`;
- topology terms: `handle`, `shaft`, `blade`, `rim`, `keywork`, `trigger`, `hinge`, `canopy`, `mouthpiece`, `valve`, `guard`, `hilt`, `major parts`, and related terms;
- physical contact/load cues: `contact shadow`, compression, indentation, deformation, `load-bearing`, `finger placement`, `contact point`, tension/slack, and grip pressure.

“Near object” means the two lexical matches occur within a 96-character window; transition proximity used 128 characters. An explicit-placement control required an object noun and a placement construction such as “satchel rests near” or “bag is placed beside” within 64 characters. The placement-control subset additionally excluded broad action verbs anywhere in the prompt. These are retrieval proxies, not semantic annotations.

### Pixel sample

I directly inspected **30 delivered images from 15 posts**, always image indices 01 and 02. The purposive stratification spans early, middle, and late incremental IDs and includes contact-required, transitional, and static/decorative controls:

- early: 1585, 1609, 1682, 1922, 1952;
- middle: 2191, 2298, 2340, 2362, 2383, 2388, 2422;
- late: 2566, 2673, 2711.

The sample is designed to expose relation failures, not estimate corpus-wide frequencies. Every pixel claim below has denominator 30 images / 15 posts unless a smaller row-level denominator is stated.

## 2. Prompt-side findings and counts

| Lexical proxy | Matching prompts | Interpretation boundary |
|---|---:|---|
| Any hand/control term | 521 | A hand mention does not establish an object relation. |
| Any object/tool inventory term | 699 | Broad inventory includes generic `object`, `prop`, `tool`, and `product`. |
| Any contact/control verb | 380 | Raw count includes contact unrelated to a tracked prop. |
| Contact/control verb near an object | 208 | Best broad proxy for held/carried/contact-required wording; still not a pixel claim. |
| Any purposeful-operation verb | 154 | Raw verbs may describe non-prop activity. |
| Purposeful-operation verb near an object | 43 | Stronger proxy for tool or functional use. |
| Any transition phrase | 64 | Includes transitions unrelated to object manipulation. |
| Transition phrase near an object | 31 | Candidate pool for pre-contact, active transition, or release-state review. |
| Any narrow topology term | 177 | Mentions a part or structural relation somewhere in the prompt. |
| Narrow topology term near an object | 47 | Candidate pool where recognition may depend on major parts or affordance. |
| Any narrow physical contact/load cue | 16 | Explicit physics is uncommon relative to general holding language. |
| Physical cue near a contact or object term | 5 | Very strict proxy for prompt-level contact/load evidence. |
| Explicit object-placement construction | 38 | Includes both static objects and placement inside action scenes. |
| Explicit placement with no broad action verb | 23 | Strict static/decorative-control pool, not an exhaustive count. |

Counts overlap. For example, one umbrella-closing prompt can match hand, contact, transition, topology, and object inventories. The broad raw placement pattern was not used because furniture and background descriptions created many false positives.

Prompt-side implications:

1. Object inventory is common, but literal contact/load evidence is sparse. “A prop exists” and “the actor controls it” must remain different assertions.
2. A smaller but useful transition set exists. A still image needs visible phase asymmetry or consequence; the word `closing` alone cannot prove direction.
3. Topology language appears often enough to support retrieval, but only a minority explicitly couples a major part to an object. Hard topology gates therefore require request evidence or an exact typed profile.
4. Static placement is a real neighboring class. A generic rule that forces every prop into a hand would corrupt legitimate still-life, resting, mounted, stored, and background states.

## 3. Pixel-side observations

The table records visible relations only. Descriptions of people are limited to visible adult presentation, pose, action, and spatial contact; no identity or protected-trait inference is made.

| Post | Prompt-side obligation | Image 01 pixel observation | Image 02 pixel observation | Relation lesson |
|---:|---|---|---|---|
| 1585 | Cybernetic arm gripping an enormous sword-lance | Weapon and mechanical arm form a readable continuum, but the boundary between held object and arm-mounted/integrated structure is ambiguous. | A mechanical hand contacts the shaft more clearly; the broad weapon class remains readable. | Object class can survive while ownership/contact mode fails. Integrated, mounted, and gripped are distinct states. |
| 1609 | Both hands grip katana overhead, poised to strike | Katana, two-hand overhead contact, wide stance, and pre-strike state read at first glance; overlapping hands weaken small-joint clarity. | Separate two-hand grip is clearer; the same pre-strike relation reads. | Thumbnail phase can pass while native contact anatomy remains a separate gate. |
| 1682 | Vintage leather satchel rests near the subject’s feet | Whole satchel is ground-supported and not contacted by the adult subject. | Satchel is partly cropped but still recognizable and ground-supported; the subject instead contacts the dog. | A visible prop near a person is not held or used. This is a static-placement control. |
| 1922 | Tote bag placed beside subject on bed; hands on lap | Bag is supported by the bed with no hand contact. | Same actor-free bag support relation reads. | Surface support and absence of actor contact can be the intended state. |
| 1952 | Holding an umbrella after rain | Curved handle, shaft, canopy, and hand contact are legible. | The same class and grip relation read. | A small set of diagnostic parts plus contact can make a tool legible. |
| 2191 | Smartphone held while posing with a large bouquet | Phone grip and phone class are first-read; bouquet dominates. Bouquet support is partly concealed. | Phone relation remains clear; bouquet support is even less explicit and reads through forearm/crook proximity. | Dominant object presence does not prove its support/contact relation; independent objects need independent obligations only when requested. |
| 2298 | One hand holds torn croissant near face, paused halfway through eating | One-hand hold, torn/bite state, and mouth proximity create a readable incomplete action. | The object is held with both hands, drifting from requested hand count, while torn state and mouthward trajectory preserve the event. | Event phase may survive an effector-count error; effector ownership needs its own gate when exact. |
| 2340 | Large red apple held with both hands | Apple class and two-hand contact are clear despite low lap placement. | Same simple topology and two-hand relation read. | Simple object topology is robust; contact remains separately inspectable. |
| 2362 | Both hands hold hay in front of goat’s mouth | Hands, hay, and goat mouth are co-located in one action loop. | Same actor-object-target loop reads, including mouth contact with the hay. | `actor -> object -> target` is stronger evidence of function than a role or prop label. |
| 2383 | Skincare product supported from below beside cheek; realistic size/weight; no floating | A jar-like product is held by relaxed fingers near the cheek. | The product becomes a pump bottle; grip remains readable but object topology/class changes across attempts. | Contact fidelity and class/topology fidelity can diverge; both must be scored when exact packaging matters. |
| 2388 | Plate on table with loosely placed melting ice; no decorative props | Plate support, ice overlap, meltwater, and surface contact read without an actor. | Same static still-life relation reads. | Physical contact is not synonymous with hand contact. Static material topology needs a positive control. |
| 2422 | Both hands slowly closing transparent umbrella; final drop falls from tip | Collapsed/partly collapsed canopy, two-hand contact, and visible tip drop read. | Same intermediate geometry and two-hand contact read. | One still does not unambiguously distinguish closing from opening; direction needs asymmetric state or residue. |
| 2566 | Left hand carries tote; fingers wrap handles; handles bend under weight; right hand swings | Grip, vertical load path, bent handles, hanging bag, and walking weight transfer read. | Same load-bearing silhouette and separate free arm read. | Load response is often more legible at thumbnail than a tiny palm contact shadow. |
| 2673 | Chopsticks lift noodles from bowl toward mouth | Chopstick grip, noodle bundle, bowl source, and mouth target form a connected path. | Mouthward action reads; source-to-bowl continuity is weaker. | Tool use needs effector, working object, source/target, and preferably a continuous causal path. |
| 2711 | Thumb-index pinch on daisy stem; flower 1–2 cm beside lips, not touching | Fine stem pinch is readable, but flower overlaps/touches the lip boundary rather than preserving the requested gap. | Same: contact with stem reads while the critical flower-mouth exclusion is weak or violated. | Required contact and required non-contact can coexist in one relation; both need explicit gates. |

## 4. Prompt/pixel alignment and divergence

### Strong alignment patterns in this sample

- **Grip plus diagnostic topology:** katana, ordinary umbrella, apple, and smartphone remain recognizable while contact is visible.
- **Load path:** the tote’s handles bend and the bag hangs below the hand, providing causal support evidence beyond hand proximity.
- **Actor-object-target loop:** hay reaches the goat’s mouth; noodles move from bowl through chopsticks toward the mouth. These relations communicate function better than occupational, costume, or setting shorthand.
- **Static support:** satchel-on-ground, tote-on-bed, and plate-on-table remain coherent without actor contact. This is an essential negative control against “all props should be held.”

### Divergences exposed by the sample

- **Class is not ownership:** post 1585 can read as an integrated or mounted weapon even while the broad sword-lance class is present.
- **Phase is not exact effector geometry:** post 2298 preserves “halfway through eating” while drifting from one hand to two.
- **Contact is not class fidelity:** post 2383 preserves a held-product relation but changes jar/pump topology.
- **Intermediate shape is not direction:** post 2422 plausibly shows a partly collapsed umbrella, but the same still could represent opening unless direction evidence is added.
- **Fine contact is not exclusion compliance:** post 2711 renders a plausible finger-stem pinch while losing the required flower-mouth gap.
- **Prompt specificity is not pixel proof:** “contact shadow inside the palm” in post 2566 is too small to judge confidently at whole-frame scale, while bent handles and hanging load are clearly visible.

These observations support a decomposed relation contract. A single `intended_interaction_matches` flag is useful for coarse repair, but it cannot explain which local relation failed.

## 5. Existing-data overlap and ownership

### Candidate/tag source

The frozen `photo_prompt_tags.json` already contains useful but fragmented evidence:

| Slot | Count | Rows with `requires_primary_any_tags` | Relevant strength | Gap |
|---|---:|---:|---|---|
| `action` | 511 | 37 | Broad action inventory, including detailed instrument operations. | Action can be selected without a compatible object, contact patch, target, or result. |
| `prop` | 559 | 33 | Broad object inventory and some strong object-specific topology. | Object existence does not encode owner or state. |
| `relational_action` | 37 | 0 | Offering, pushing, placing, sliding, handover, and related exchanges. | Mostly phrase-level; giver/receiver contact and transfer phase are not one typed record. |
| `prop_direction` | 15 | 0 | Instrument axes, toward-partner handoff, set-down, pull-back, hidden/tucked/propped states. | Direction is separate from contact and phase. |
| `contact_point` | 24 | 0 | Strong instrument-specific contacts such as reed/lips/keys or bow hair/strings. | No generic actor-part/object-part relation schema. |
| `hand_pose` | 21 | 0 | Mug hold, visible phone hold, bag-strap hold, surface rests. | Mixes portrait gesture inventory with interaction meaning. |
| `duty_prop_state` | 8 | 0 | Radio in use, scanned card, open clipboard, and related work-state hints. | State wording does not necessarily supply visible operation/result evidence. |
| `procedure_step` | 18 | 10 | Preparation, inspection, transfer, intervention, monitoring. | Process stage is not tied to one prop relation. |
| `transition_stage` | 6 | 0 | Transformation/dissolve stages. | It does not cover ordinary object manipulation phases. |
| `narrative_phase` | 36 | 7 | Includes instrument attack, sustained control, and setup/check phases. | Strong local clusters exist, but no shared object-agnostic state topology. |

The instrument rows demonstrate that coordinated `action + prop + contact_point + prop_direction + narrative_phase` evidence works when authored carefully. The risk is independent retrieval of incompatible rows. A relation bundle should coordinate these parts rather than inflate each slot with aliases.

### Quality layer

`photo_prompt_quality_layers.json` already provides the correct generic mechanism vocabulary:

- `physical_contact` includes contact shadow, compression, weight, and pressure;
- the baseline rejects props listed as labels without contact shadow, reflection, weight, or physical interaction;
- `relational_coordination` asks hands, spacing, and a shared object to make coordination legible;
- `process_stage_evidence`, `health_access_functional_participation`, `sports_phase_contact_response`, and `education_activity_evidence` link contact to stage, tool, target, or result.

However, ownership is split: `action_camera` owns `action` and `hand_pose`, while `material_world` and `light_second_reading` can both supply `prop`. The generic relation should be compiled once, then let quality routes add only compatible physical or photographic evidence.

### Narrow visual obligations

Existing exact profiles already prove the value of hard relational components:

- `hands_free_supported_drink_load` separates visible base contact, compression, center-of-mass support, and both hands being clear;
- `aircraft_pilot_operation` binds operator, primary control/checklist contact, and matching flight state;
- instrument profiles bind diagnostic parts, contact points, direction, and playing phase;
- professional-duty profiles bind role to action/tool/target/result rather than costume alone.

These are good narrow obligations, not a reason to route every generic `holding` prompt into a hard profile.

### Existing repair contract

The current object-agnostic `photo-request-lineage/v2` repair target already freezes:

- actor and object phrases;
- `interaction_state` in `held | wielded | used | handed_off | carried | worn | sheathed | mounted | resting | other`;
- actor-object contact in `required | transitional | absent | unspecified`;
- protected dimensions, allowed local repair axes, source spans, relation origin, and literal interaction/recognition evidence.

Its coarse render gates cover object class, gross structure, intended interaction, and contact anatomy; its retry policy correctly states that removal, relocation, concealment, or transfer is not repair.

The main gap is decomposition. `used`, `carried`, `mounted`, `resting`, and `handed_off` mix role, support, phase, and topology in one enum. `required/transitional/absent/unspecified` does not say who touches which part, whether the touch controls or merely supports, what bears load, what target is affected, or what visible consequence proves use.

### Single-owner recommendation

1. The request envelope and authorial semantic assertion own requested object identity and action meaning.
2. A future compiled interaction relation owns effector, contact/gap, support, phase, target, topology, and consequence as one graph.
3. Candidate data may suggest compatible renderable details only after the graph is frozen.
4. Quality layers own generic physics and photographic legibility, not object identity.
5. Exact visual obligations own narrow compound terms only.
6. Request-lineage repair preserves the inherited graph and changes only permitted local rendering axes.

## 6. Proposed observable components

### Generic relation graph

Use a minimal graph that can represent both contact and intentional non-contact:

```text
actor.effector
  -- contact_mode / required_gap --> object.affordance_part
  -- support_or_load_path --------> actor | surface | ground
object.working_end
  -- target_relation -------------> target_or_workpiece
state_before -> state_visible -> state_after_implied
                                  -> visible_consequence
```

Not every relation needs every edge. A static plate needs surface support and material contact but no actor. A theremin-like controller can require a visible gap and a device response instead of touch. A carried tote needs grip, load path, and handle deformation but no workpiece target.

### Component groups

1. **Actor and effector ownership** — which visible adult subject, limb, mouth, body support region, or tool end owns the relation; exact left/right/both only when requested.
2. **Object identity and role** — manipulated tool, carried load, offered item, consumed item, displayed prop, mounted fixture, worn item, stored item, or support surface.
3. **Contact or gap mode** — grip, pinch, cradle, press, pull, push, suspend, guide, surface rest, mouth contact, non-contact control, or required absence.
4. **Contact patch** — actor part and object part meet at a visible, physically plausible region.
5. **Affordance and working end** — handle/rim/shaft/control/body versus blade/tip/bristles/nozzle/food bundle; retain literal part names from the request or source profile.
6. **Support and load path** — what carries weight, where it continues, and whether center of mass and gravity agree.
7. **Localized material response** — bend, sag, tension, compression, indentation, contact shadow, displaced liquid, or no response when the relation is explicitly non-load-bearing.
8. **Target/source topology** — source container, destination, mouth, workpiece, partner, wall, table, or environmental target and the spatial relation between them.
9. **Temporal phase** — pre-contact, contact onset, active manipulation, sustained control, release onset, post-release, or static supported/stored state.
10. **Visible consequence** — cut, poured stream, displaced part, contacted food, opened closure, restored result, or another localized effect; optional where holding alone is the requested meaning.
11. **Object topology** — minimum diagnostic parts, connectivity, orientation, and one coherent body; ornamental differences remain non-blocking unless requested.
12. **Visibility budget** — the critical contact patch, affordance, working end, and target must survive crop/occlusion at their assigned review scale.

### Confusion boundaries and false substitutes

- nearby, foreground, dominant, or similarly lit prop **is not** held, owned, or used;
- hand near an object **is not** contact;
- intersection or fusion through a palm **is not** a grasp;
- an object behind or against the actor **is not** carried unless the support relation is visible;
- a wrist/crook occlusion **is not** a proven grip;
- costume, setting, title, or occupational styling **is not** tool operation;
- object-class recognition **is not** affordance use;
- generic shadow, reflection, or deformation **is not** contact evidence unless localized to the asserted patch;
- pre-contact **is not** active use, and active use **is not** post-action consequence;
- partly open/closed geometry without direction evidence **is not** proof of opening versus closing;
- target proximity **is not** target-directed action without a path, orientation, or result;
- two visible hands **do not** prove both hands contact the same object;
- one shared object **does not** prove handoff without giver/receiver ownership and a transfer phase;
- support contact and manipulating grip are different modes;
- sheathed, mounted, resting, stored, and displayed are legitimate requested states, not generic failures;
- wall placement is a hard negative only when it replaces a frozen held/used/carried/handoff relation. A requested wall-mounted fixture is a positive control;
- removal, concealment, relocation, or transfer to another actor/limb is not a valid fidelity repair unless the requester explicitly corrects the parent relation.

## 7. Candidate-pack and data proposal

### A. New optional authored source: `photo-object-interaction/v1`

Prefer one coordinated relation record over independently retrieved action, prop, and contact fragments. Suggested exact fields:

```json
{
  "contract_version": "photo-object-interaction/v1",
  "relation_id": "...",
  "source_span_ids": ["..."],
  "evidence_source": "user_request | authorial_core | exact_visual_profile | advisory_candidate",
  "importance": "primary | supporting | decorative",
  "actor_id": "literal stable id",
  "effector_roles": [
    {
      "effector": "left_hand | right_hand | both_hands | mouth | foot | body_support | tool_end | none",
      "role": "control | stabilize | support | receive | release | noncontact_control",
      "contact_mode": "grip | pinch | cradle | press | pull | push | suspend | guide | surface_rest | mouth_contact | noncontact_gap | none",
      "actor_part_phrase": "literal evidence",
      "object_part_phrase": "literal evidence"
    }
  ],
  "object_id": "literal stable id",
  "object_phrase": "literal evidence",
  "object_role": "manipulated_tool | carried_load | offered_item | consumed_item | displayed_prop | mounted_fixture | worn_item | stored_item | support_surface",
  "relation_family": "hold | carry | operate | consume | offer | transfer | support | display | mount | store | noncontact_control",
  "interaction_phase": "pre_contact | contact_onset | active | sustained | release_onset | post_release | static",
  "contact_expectation": "required | transitional | absent | unspecified",
  "affordance_part_phrase": "literal or empty",
  "working_end_phrase": "literal or empty",
  "support_chain": ["object_id", "supporter_id", "ground_or_surface_id"],
  "load_response": ["handle_bend | sag | tension | compression | indentation | contact_shadow | none | unspecified"],
  "source_id": "literal or empty",
  "target_id": "literal or empty",
  "target_relation": "toward | from | into | onto | through | beside | away_from | none",
  "state_before_phrase": "literal or empty",
  "state_visible_phrase": "literal evidence",
  "state_after_implied_phrase": "literal or empty",
  "visible_consequence_phrase": "literal or empty",
  "minimum_visible_parts": ["literal diagnostic parts"],
  "critical_contact_visibility": "thumbnail | native | both | not_applicable",
  "maximum_occlusion": "literal bounded instruction",
  "positive_evidence_phrases": ["byte-stable prompt evidence"],
  "reject_substitutes": ["typed negative ids"],
  "flexible_dimensions": ["ornament | minor_material | minor_pose | camera | framing | lighting"]
}
```

The relation vocabularies may be closed and generic, but object names, object parts, state phrases, and consequences should remain literal evidence rather than a universal noun ontology. `other` should not silently satisfy a hard profile; unsupported exact relations should remain explicit literals or unscored.

### B. Coordinated advisory candidate bundles

Add a future authored candidate source or a coordinated `interaction_relation` slot, with each row producing compatible multi-slot evidence. Suggested candidate-row fields:

```json
{
  "id": "carry_load_handle_response",
  "ko": "...",
  "en": "...",
  "weight": 0.0,
  "tags": ["interaction_relation", "carry", "load_path"],
  "requires_primary_any_tags": ["carry", "bag", "basket", "container"],
  "relation_family": "carry",
  "component_terms": ["effector contact", "load path", "localized response"],
  "positive_evidence": ["fingers close around the requested handle", "the load hangs below that contact", "the handle bends or tensions under the same load"],
  "reject_substitutes": ["nearby_object", "crook_only_support", "floating_load", "wall_placement"],
  "suggested_review_scales": {"relation": "thumbnail", "contact": "native"},
  "embedding_text": "..."
}
```

Candidate families worth authoring first:

1. `carry_load`: contact on handle/strap plus continuous load path and bend/sag/tension;
2. `consume_lift`: source container -> utensil/food -> mouth target at an incomplete phase;
3. `offer_handoff`: giver contact, object, receiver reach/contact, and one explicit transfer boundary;
4. `operate_tool`: control hand on affordance, working end at target, and localized result;
5. `open_close_transition`: one stabilizing effector, one actuating effector, asymmetric intermediate geometry, and direction residue;
6. `static_surface_support`: object/surface contact, shadow/pressure/material response, and no invented actor contact;
7. `fine_pinch`: thumb-index pad contact, small-object silhouette, relaxed remaining fingers, and any required face/object gap;
8. `noncontact_control`: visible hand-object gap, assigned control field, and device/result response.

Candidate frequency must not change defaults. Exact object-specific topology remains in narrow prop/profile data; generic bundles only express the relation skeleton.

### C. Quality-layer strengthening

Extend the generic quality mechanism only when an interaction relation is active:

- `contact_patch_legibility`: local contact/gap is visible at the assigned scale;
- `affordance_working_end_legibility`: control part and working end remain distinguishable;
- `support_load_continuity`: gravity, center of mass, tension/compression, and support agree;
- `target_consequence_continuity`: object orientation and any visible result share one causal path;
- `transition_direction_evidence`: intermediate state includes an asymmetry, residue, or consequence that distinguishes direction.

Do not let quality retrieval invent a tool, target, contact, hand count, or phase absent from the request.

### D. Object-agnostic repair extension

Preserve the current repair contract’s strongest rule: removal, relocation, concealment, or transfer is not repair. A future optional relation detail should freeze only graph structure, not named-object defaults:

- freeze actor/object IDs, effector role, relation family, phase, contact expectation, requested gap, support chain, target relation, diagnostic parts, and literal evidence;
- permit `object_geometry` only to restore the same class/major-part connectivity;
- permit `contact_geometry` and `local_pose` only to restore the same effector, contact mode, and affordance;
- permit `occlusion` changes only to reveal the frozen contact/parts, never to hide or reassign them;
- permit camera/framing/light/material changes only when the request lineage already allows those dimensions;
- use `parent_preserved` for an inherited relation and `requester_corrected` only for an explicit correction such as “the object should actually be wall-mounted, not held”;
- omit repair targets for decorative background objects unless the requester made their state meaningful.

Suggested conditional repair gates:

| Gate | Scale | Activate when |
|---|---|---|
| `object_class_and_major_parts_legible` | both/native | Object is primary/supporting and class exactness matters. |
| `owner_and_effector_match` | thumbnail | Actor/hand/limb ownership is locked. |
| `critical_contact_or_gap_matches` | native | Contact is required/transitional/absent. |
| `affordance_use_coherent` | both | The relation is `operate`, `wield`, or exact grip. |
| `support_and_load_path_coherent` | both | Object is carried, suspended, worn, or surface-supported. |
| `target_and_consequence_connected` | both | Tool/use/consume/feed/transfer has a target or result. |
| `transition_phase_evidenced` | both | Pre-contact, active transition, release, or post-event timing is locked. |
| `critical_parts_within_visibility_budget` | native | Topology/contact would otherwise be hidden by crop or occlusion. |

For a hard profile, all activated gates pass together; a partial relation is a failure. For advisory candidates, no hard gate exists until the authorial core explicitly adopts the relation.

## 8. Regression and held-out tests

### Causal one-axis mutations

Every negative should preserve unrelated camera, lighting, wardrobe, environment, and object appearance while changing one relation axis:

| Mutation | Positive fixture | Hard-negative mutation | Expected boundary |
|---|---|---|---|
| Removal | Hand holds requested umbrella/tool. | Delete the action-bearing object. | Fails class and relation; not a repair. |
| Concealment | Critical grip and affordance remain visible. | Crop or occlude the contact patch/diagnostic parts while leaving a nearby object. | Fails visibility and contact; nearby object cannot substitute. |
| Transfer | Requested actor/hand owns object. | Put object in another actor’s hand or the wrong limb. | Fails owner/effector gate even if object and action remain plausible. |
| Wall placement | Requested object is held/used in hand. | Hang the same object on a wall rack while actor poses nearby. | Fails intended state; use only when held/used/carried/handoff is frozen. |
| Wall-placement positive control | Requested lamp/tool is explicitly wall-mounted/stored. | Keep coherent mount points and no invented hand contact. | Must pass; wall location is not a universal negative. |
| Contact removal | Required pinch/grip closes on the affordance. | Insert a visible 1–2 cm gap. | Fails required contact. |
| False fusion | Fingers wrap around the handle. | Object intersects palm/fingers without a readable wrap or joint spacing. | Fails native contact anatomy. |
| Affordance swap | Hand holds handle/shaft/control. | Hand grips blade, working edge, nozzle, or unrelated body panel. | Fails functional affordance while class may pass. |
| Phase collapse | Partly closing/opening object includes phase evidence. | Show fully open or fully closed state with no actuation cue. | Fails locked transitional phase. |
| Direction ambiguity | Intermediate state includes actuator direction/residue. | Keep same intermediate shape but remove all directional evidence. | `opening` versus `closing` becomes unscored/fail for exact direction. |
| Topology corruption | Minimum diagnostic parts connect coherently. | Duplicate, omit, reverse, or disconnect one major part. | Fails topology even if contact remains. |
| Target disconnection | Tool/food path reaches source/target. | Point working end away, detach noodles from chopsticks, or break handoff alignment. | Fails target/consequence continuity. |
| Load-response deletion | Tote handle bends/tensions and bag hangs. | Keep grip but make handles rigid, bag floating, or load direction inconsistent. | Fails load path. |
| Exclusion violation | Fingers pinch flower while flower remains beside lips. | Preserve pinch but move flower onto the lip. | Required contact passes; required non-contact fails. |
| False activation of decorative control | Satchel rests near feet or tote rests on bed. | Put it into the actor’s hand without request evidence. | Fails intended static state; “more interaction” is not automatically better. |

### Positive corpus fixtures for later tests

- simple grip/topology: 1609, 1952, 2340;
- target-directed function: 2362, 2673;
- load-bearing carry: 2566;
- transition: 2298, 2422;
- fine contact plus exclusion: 2711;
- class/contact divergence: 1585, 2383;
- static/decorative controls: 1682, 1922, 2388.

### Held-out object families

Do not validate only on the motivating corpus nouns. Later fixtures should include:

- hand tool with handle and working end: wrench, ladle, paintbrush;
- carried load with flexible attachment: parcel strap, basket, camera strap;
- transfer object: cup, folder, access card;
- open/close mechanism: jar lid, zipper, folding fan;
- non-contact device: touchless sensor or field controller;
- explicitly wall-mounted object: lamp, control panel, or stored tool as a positive control.

At least one held-out case should make object class easy but the relation wrong, and another should make the relation plausible while one diagnostic part is wrong.

## 9. Limitations

- The 30-image sample is purposive, not random. No sampled success/failure proportion is generalized to all 4,908 images.
- Only two images per selected post were inspected; other delivered images from the same post may differ.
- Prompt lexical counts are overlapping proxies. Generic words, negations, reference-image instructions, and long-distance clause structure can produce false positives or negatives.
- A single reviewer performed the pixel inspection; there is no inter-rater agreement measurement.
- Delivered pixels demonstrate behavior of this corpus only. They do not prove future model behavior or runtime candidate quality.
- No prompt composition audit, image-generation run, formal pixel-review JSON, or user review was performed for the proposal.
- No external source was needed: the design terms are defined operationally from the frozen corpus and existing repository contracts rather than borrowed as a new photographic taxonomy.

## 10. Final recommendation

**Proposed:** introduce an opt-in `photo-object-interaction/v1` relation graph, coordinated advisory interaction bundles, and conditional object-agnostic repair gates. Preserve existing narrow profiles and the current no-removal/no-relocation/no-concealment/no-transfer repair rule. Do not add a global “person must hold prop” default and do not turn corpus frequency into activation authority.

The first qualification round should use independent positive/hard-negative pairs for carry load, source-tool-target action, transition direction, fine contact plus required gap, static support, and requested wall mounting. Until those prompts are composed and rendered under frozen independent inputs, implementation quality, pixel quality, and user judgment remain unscored.

## Evidence appendix

### Inspected post IDs and image paths

All paths are relative to `generated/reactorprompt-export-20260902-incremental/`.

```text
1585  images/1585_DY01212mlsY_01.jpg  images/1585_DY01212mlsY_02.jpg
1609  images/1609_DY4gSNEmr9G_01.jpg  images/1609_DY4gSNEmr9G_02.jpg
1682  images/1682_DY_14psmlnp_01.jpg  images/1682_DY_14psmlnp_02.jpg
1922  images/1922_DZ2Ha3dmvH5_01.jpg  images/1922_DZ2Ha3dmvH5_02.jpg
1952  images/1952_DZ47JtkmmH3_01.jpg  images/1952_DZ47JtkmmH3_02.jpg
2191  images/2191_Da7Er3_GttO_01.jpg  images/2191_Da7Er3_GttO_02.jpg
2298  images/2298_Dbcq_-4mgy5_01.jpg  images/2298_Dbcq_-4mgy5_02.jpg
2340  images/2340_DbnJwlFGmnk_01.jpg  images/2340_DbnJwlFGmnk_02.jpg
2362  images/2362_DbqMGYMGgLv_01.jpg  images/2362_DbqMGYMGgLv_02.jpg
2383  images/2383_Dbu64Fgmt3t_01.jpg  images/2383_Dbu64Fgmt3t_02.jpg
2388  images/2388_Dbuy3raGlV7_01.jpg  images/2388_Dbuy3raGlV7_02.jpg
2422  images/2422_Db0XqjAmnZ_01.jpg  images/2422_Db0XqjAmnZ_02.jpg
2566  images/2566_DcQ20r-mp-i_01.jpg  images/2566_DcQ20r-mp-i_02.jpg
2673  images/2673_Dcllog9mqn5_01.jpg  images/2673_Dcllog9mqn5_02.jpg
2711  images/2711_DcqCkahGovW_01.jpg  images/2711_DcqCkahGovW_02.jpg
```

### Reproduction commands

```bash
shasum -a 256 generated/reactorprompt-export-20260902-incremental/manifest.json

jq '[.[] | select((.prompt // "") | length > 0)] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq -r '.[] | select(.id==1585 or .id==1609 or .id==1682 or .id==1922 or .id==1952 or .id==2191 or .id==2298 or .id==2340 or .id==2362 or .id==2383 or .id==2388 or .id==2422 or .id==2566 or .id==2673 or .id==2711) | [.id,.shortcode,.prompt_file,.images[0].local_file,.images[1].local_file] | @tsv' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

git show HEAD:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json | \
  jq -r '["action","prop","relational_action","prop_direction","contact_point","hand_pose","duty_prop_state","procedure_step","transition_stage","narrative_phase"][] as $s | [$s, (.slots[$s] | length), ([.slots[$s][] | select(has("requires_primary_any_tags"))] | length)] | @tsv'

rg -n 'RENDER_REPAIR_INTERACTION_STATES|RENDER_REPAIR_CONTACT_EXPECTATIONS|render_repair_target_gates|removal_relocation_concealment_or_transfer_is_not_repair' \
  skills/photo-prompt-image-generator/scripts/prompt_generator.py

rg -n 'action_camera|material_world|light_second_reading|props listed as labels|physical_contact|relational_coordination|education_activity_evidence' \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json
```

The prompt-scan counts were produced by a read-only Python pass over `manifest.json` using the lexicons and proximity windows documented in §1; the explicit-placement subset used the documented object/placement construction and broad action exclusion. The 30 images were opened at original detail and inspected individually.

### External sources

None. No external terminology was needed to establish the corpus-derived relation boundaries or the existing repository ownership model.
