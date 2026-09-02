# Topic 01 — composition, framing, crop, negative space, and attention hierarchy

## Status and headline finding

This is a research/design artifact only. It does not change runtime assets, generated indexes, tests, or prompt behavior.

The incremental ReactorPrompt corpus supports strengthening composition data, but it does **not** support adding a new global aesthetic default. The frozen skill data already has strong exact profiles for third-grid placement, centering, symmetry, counterbalance, leading lines, look/motion room, subject-field negative space, frame-within-frame, three-plane depth, pattern breaks, figure-ground hierarchy, and peak action. The material gaps are narrower:

1. crop words name a frame boundary but do not record which semantic anchors must survive that boundary, which exits are intentional, or whether a missing part is cropped, occluded, or absent;
2. multi-panel prompts can specify exact count, layout, and per-panel shot roles, but the current general composition profiles do not own that topology;
3. attention hierarchy needs an explicit owner. A face, action contact, prop, environmental sign, or textural exception can legitimately be the first read; “person first” cannot be a universal rule;
4. a multi-image post and a multi-panel image are different structures and must not share one implicit label.

Accordingly, this report proposes two narrow exact contracts—`crop_boundary_anchor_integrity` and `multi_panel_count_layout_sequence`—plus advisory candidate fields for hierarchy ownership, edge continuation, negative-space function, and series invariants. Existing exact composition profiles should be reused rather than duplicated.

## Scope and sampling method

### Frozen inputs

- Incremental manifest: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- Manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- Corpus scope: 1,182 posts, 4,908 delivered images, 924 non-empty prompts, 904 unique prompt bodies, post IDs 1565–2746.
- Target-skill reference revision: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- Frozen authored-source hashes used for overlap analysis:
  - visual obligations: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - tag/candidate data: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - quality layers: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`
  - generated visual-profile index: `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626`

The generated visual-profile index was treated as derivative evidence, not an authored source. Repository observations below refer to the frozen hashes, not unrelated later working-tree changes.

### Prompt scan

All 924 non-empty prompt records were scanned programmatically. Nine overlapping bilingual phrase groups were used: aspect/orientation, shot coverage, crop/edge policy, placement/balance, negative or directional space, foreground/depth/occlusion, line/axis/visual path, explicit attention hierarchy, and multi-panel layout.

The scan is lexical retrieval, not a classifier. A hit can occur in a positive instruction, a prohibition, or a comparison. Counts therefore describe **prompt-side wording only** and do not establish visual prevalence, authorial intent, or pixel success.

### Pixel sample

I inspected 40 delivered corpus images from 20 posts: the first two manifest images for every selected post. The sample exceeds the brief’s minimum of 24 images across 12 posts.

Sampling was purposive maximum variation rather than random prevalence estimation:

- early IDs: 1629/1630, 1649/1650, 1898/1899, 1926/1927;
- middle IDs: 2101/2102, 2299/2303, 2323/2325;
- late IDs: 2525/2526, 2629/2637, 2705/2707;
- ten topic-positive posts were paired with ten nearby or same-family controls;
- controls were chosen to expose an alternative topology, a lower-specificity prompt, an implicit genre composition, competing attention, or a conditional hard negative. They are not claimed to be “composition-free.”

All 40 images were inspected at high detail. Six representative images and four additional edge/crop examples were rechecked at original detail. Pixel comments are limited to visible pose, styling, framing, action, and spatial relations; no identity or protected-trait inference was made.

## Prompt-side findings and counts

| Lexical group | Matching prompts | Interpretation boundary |
|---|---:|---|
| orientation or aspect | 461 | Explicit vertical/horizontal/square/aspect wording; not proof that the delivered image obeys it. |
| shot scale or coverage | 373 | Named full-body/medium/close coverage; does not encode which anchors must remain visible. |
| crop or edge policy | 31 | High-precision boundary wording such as tight crop, out of frame, headroom, or frame exit; garment phrases such as “cropped top” were intentionally excluded. |
| placement or balance | 285 | Center, thirds, corners, symmetry, asymmetry, or counterbalance; includes negative uses such as avoiding artificial symmetry. |
| negative or directional space | 66 | Negative/copy/look/motion room wording; does not distinguish aesthetic space from UI-safe space. |
| foreground, depth, or occlusion | 540 | Deliberately broad retrieval including ordinary “background”; useful for candidate recall, not evidence of a three-plane contract. |
| line, axis, or visual path | 20 | Explicit diagonal, converging-line, frame-within-frame, or visual-path mechanisms. |
| attention hierarchy | 28 | Explicit focal point, first read, dominant focus, or primary/secondary focus wording. |
| multi-panel or graphic layout | 32 | Diptych/triptych/grid/collage/panel language; a post containing several files is not automatically in this group. |

Additional overlaps:

- 774/924 prompts matched at least one group.
- 533 matched at least two groups; 326 matched at least three; 148 matched at least four; 46 matched at least five.
- explicit attention hierarchy ∩ crop/edge policy: 3;
- negative/directional space ∩ crop/edge policy: 5;
- foreground/depth/occlusion ∩ attention hierarchy: 27;
- multi-panel layout ∩ shot coverage: 16.

These results support three bounded conclusions.

First, shot coverage and placement are common prompt vocabulary, while explicit crop-boundary ownership, line-target continuity, and first-read hierarchy are much less often literalized. Frequency alone does not justify defaulting the rarer relations, but their sparsity makes structured evidence especially useful when they are requested.

Second, many prompts co-mention several composition ideas. A candidate pack needs per-clause ownership: “close shot,” “face dominant,” “blue negative space,” and “arm out of frame” are not interchangeable synonyms for one composition tag.

Third, the 540-hit depth group is a recall bucket. Ordinary background descriptions must not activate a hard three-plane-depth or occlusion profile without literal component evidence.

## Pixel-side observations and sample IDs

The denominator for this section is 40 images from 20 posts. The table summarizes both inspected images for each post; it does not estimate frequencies across all 4,908 images.

| Post | Sampling role | Prompt-side composition cue | Delivered-pixel observation across `_01` and `_02` |
|---:|---|---|---|
| 1650 | positive | Full-body, centered standing, expression as focal point, long hallway perspective, vertical frame. | Both frames keep a centered standing figure and the full standing topology. Receding corridor/locker structure supports the central first read. Strong prompt/pixel alignment. |
| 1649 | nearby control | Candid vertical mirror-selfie genre and busy setting, without an exact frame-within-frame obligation. | Mirror boundaries, aisle depth, and phone/face overlap create a strong implicit topology. This shows that genre can produce a composition relation without authorizing a hard exact profile. |
| 1899 | positive | Three-image vertical collage with extreme-close, medium-close, and close roles in sequence. | Both files visibly contain three stacked horizontal bands with distinct face-scale roles and separators. Exact count and sequence survive. |
| 1898 | alternative-layout control | Four-image 2×2 poster grid. | Both files visibly resolve as a 2×2 grid with four cells and separators. This is a useful hard alternative to the three-panel case, not an absence-of-layout control. |
| 1629 | generic-wording stress | Vertical frame, minimal background, and “refined composition,” but no literal crop boundary. | `_01` reads around medium-long/mid-thigh coverage while `_02` reads as full-body. The generic adjective does not freeze coverage. |
| 1630 | nearby control | Close winter portrait without a structured crop contract. | Both frames are face-led close portraits, but the exact edge and coverage choices are supplied by the image, not by a literal prompt relation. |
| 1927 | crop/action positive that diverges | Both arms behind the head, hands outside frame, tight crop from raised arms to below chest. | Neither inspected frame realizes both raised arms with hidden hands. One visible hand instead holds hair near a lower edge, and the coverage extends below the requested chest endpoint. The core action/crop topology diverges. |
| 1926 | conditional look-room hard negative | Off-frame gaze to the right; no explicit look-room request. | The visible gaze points right while the larger dark open field lies mainly behind/left. This would fail an explicitly requested look-room relation, but it is not a prompt failure here because look room was not requested. |
| 2299 | positive | Head-to-mid-thigh coverage, slightly right placement, generous headroom, large foreground leaf, diagonal greenhouse structure. | Both frames retain a foreground leaf band and greenhouse depth. Subject placement varies around center/right, but the regional occlusion and depth proposition remain legible. |
| 2303 | same-family control | Mirror-selfie setting without the exact greenhouse layer contract. | Rounded mirror edge, reflection depth, and phone overlap produce another implicit frame-within-frame topology. It should remain advisory unless requested literally. |
| 2325 | positive | High handheld selfie, frame filling, diagonal/Dutch feel, minimal headroom, camera arm outside frame. | Both frames show high-angle face/torso fill, an exiting arm, and strong street diagonals. The arm exit is coherent continuation rather than an accidental missing limb. |
| 2323 | competing-attention control | Intentionally includes a partial dark-clad figure at left and bag/bottle cues at right. | Secondary objects and the partial figure visibly compete with the central subject. Competition is part of the candid proposition, so a universal “remove all competitors” rule would be wrong. |
| 2102 | positive | Close 9:16 phone selfie, high angle, natural crop, simple background. | Both frames keep face/upper-torso priority while one extended arm exits the frame. This is a valid genre-owned edge continuation. |
| 2101 | environment-primary control | Full-body street frame with large upper-left signs described as dominant. | The signs are a first-read or strong co-primary anchor in both images. A hierarchy profile must permit an environmental anchor to outrank a face when source evidence says so. |
| 2637 | positive | Centered vertical crouch, high angle, strong foreground, keep the full body visible, architecture/screens in depth. | Both frames keep a compact crouching action topology near center; limbs and ground relationship are readable while bright background elements compete. “Full body” here is better represented as complete action/contact topology than as a standing bounding box. |
| 2629 | alternative-relation control | Horizontal diagonal car pose with both feet visible. | The car body and reclining pose form a strong diagonal relation, and the visible feet close the action topology. The frame is relationally composed even without one of the current exact profile labels. |
| 2707 | positive | Face dominant, one arm cropped, face in upper-right, diagonal composition, a specified warm negative-space field, clear foreground. | Both files preserve face dominance and a substantial warm low-detail field while pose and exact crop differ. This is strong evidence for separating invariants from flexible dimensions. |
| 2705 | hierarchy hard control | Ordinary balcony medium portrait without an explicit hierarchy contract. | A bright wall lamp can compete with or precede the face at first read. The case should remain acceptable unless a subject-first hierarchy was actually requested. |
| 2526 | positive | Medium close low-angle selfie, face dominant high in frame, arm perspective, blue negative space. | Both frames retain a large blue sky field and face priority; the foreshortened arm is a strong secondary mass and its exit is source-supported. |
| 2525 | implicit-directional control | Square close lifestyle frame with off-camera gaze to the right, but no explicit look-room term. | The frames provide meaningful space in the gaze direction and a receding lower-body path. The pixel relation is real, but it cannot be attributed solely to an absent phrase. |

## Prompt/pixel alignment and divergences

### What aligned

1. **Literal relational constraints were often legible in the delivered pixels.** Posts 1650, 1899, 2299, 2325, 2707, and 2526 preserve most of their named center/coverage/panel/depth/edge/hierarchy relations.
2. **A first-read invariant can survive variation.** In post 2707, exact pose and crop change, while face dominance and the warm low-detail field remain. Candidate data should distinguish `invariant_fields` from `flexible_fields`.
3. **Edge exits can be intentional.** Selfie arms in 2102, 2325, and 2526 visibly continue toward the camera and leave the frame coherently. “Out of frame” is not automatically a defect.
4. **Compact poses change the meaning of full-body coverage.** Post 2637 remains action-complete even though crouching compresses the figure. Required visible anchors and contacts are more robust than a generic bounding-box rule.
5. **Exact panel count and geometry are visually discriminative.** The three stacked bands in 1899 and the four-cell grid in 1898 remain distinct even at reduced scale.

### What diverged or remained underdetermined

1. **Aesthetic adjectives did not actuate coverage.** Post 1629’s “refined composition” permits materially different crops. Such terms belong at most to advisory quality, not an exact hard obligation.
2. **Named crop endpoints did not guarantee action integrity.** Post 1927 fails the specified both-arms/hands-out topology. A shot-scale tag alone cannot diagnose that failure.
3. **Genre can create undeclared relations.** Mirror boundaries and phone overlap appear in 1649 and 2303 without an exact frame-within-frame request. Pixel presence does not retroactively make the prompt literal.
4. **Attention ownership varies.** The environmental sign in 2101 and deliberate intrusions in 2323 show that person-first or face-first cannot be global. The primary anchor and an intentional competitor must be source-conditioned.
5. **Open space has more than one function.** The warm field in 2707 supports hierarchy; the blue sky in 2526 supports atmosphere and hierarchy; UI-safe copy space would be a different contract. A single `negative_space` label loses this distinction.
6. **Prompt/pixel attribution remains correlational.** The corpus does not expose every generation setting, reference-image contribution, selection process, or discarded alternative. A good alignment is not proof that one phrase alone caused the result.

## Existing-data overlap and ownership

### Existing exact visual obligations

The frozen visual-obligation source already contains 12 narrow composition-relation profiles:

1. `third_grid_focal_anchor_relation`
2. `centered_primary_anchor_relation`
3. `axial_bilateral_symmetry_relation`
4. `asymmetric_counterbalance_relation`
5. `leading_line_target_continuity`
6. `look_motion_room_direction_relation`
7. `subject_field_negative_space_relation`
8. `frame_within_frame_boundary_relation`
9. `three_plane_depth_chain`
10. `pattern_break_focal_exception`
11. `primary_secondary_figure_ground_hierarchy`
12. `peak_action_event_phase`

These profiles already provide definitions, component semantics, contrast examples, composition instructions, evidence fields, thumbnail/native render gates, and reject substitutes. In particular:

- `subject_field_negative_space_relation` already owns a contiguous low-detail field, clean contour separation, first-read hierarchy, and native material/tone evidence that the field is intentional rather than deletion or exposure failure;
- `look_motion_room_direction_relation` already owns vector origin, direction, and greater space ahead rather than behind;
- `frame_within_frame_boundary_relation` already distinguishes a physical opening with boundary thickness/occlusion from a vignette;
- `primary_secondary_figure_ground_hierarchy` already distinguishes primary, subordinate, and supporting ground and rejects blur-only pseudo-hierarchy.

Adding new generic “negative space,” “look room,” “leading lines,” or “visual hierarchy” profiles would duplicate current semantics and create competing owners.

### Existing tags and candidate vocabulary

The frozen tag/candidate source already exposes:

- eight `shot_scale` values: `extreme_wide`, `wide`, `full_length`, `medium_long`, `medium`, `medium_close`, `close_up`, `extreme_close`;
- ten `placement` values: `centered`, `rule_of_thirds`, `negative_space`, `frame_filling`, `edge_tension`, `entering_frame`, `exiting_frame`, `layered_depth`, `foreground_frame`, `symmetry`;
- platform-frame concepts including vertical/square safe frames, `ui_safe_negative_space`, `thumbnail_safe`, `face_upper_middle`, `center_safe`, `blank_lower_third`, and `carousel_crop_safe`;
- composition, shot-scale, subject-framing, body-framing, and platform-framing slots.

This vocabulary names endpoints and broad patterns. It does not yet preserve a per-request ledger of required visible anchors, allowed frame exits, forbidden cut zones, or per-panel roles.

### Existing quality layer

`photographic_craft.dimensions[id=frame_hierarchy]` already owns the broad advisory principle: organize foreground, subject plane, and background into a clear reading order rather than allowing every detail to compete equally. Its refinements cover layered depth, close-frame focus/edge behavior, wide-frame reading paths, operational flow, and batch traceability.

### Recommended ownership boundary

| Concern | Owning layer | Why |
|---|---|---|
| General reading order, foreground interruption, edge awareness | quality layer `frame_hierarchy` | Broad craft guidance; should not hard-fail an image unless the request names a relation. |
| Shot scale, placement, platform-safe framing | tag/candidate vocabulary | Selectable descriptive facets with no automatic exact obligation. |
| Requested third-grid, look room, negative space, physical inner frame, leading-line target, figure-ground hierarchy | existing visual-obligation profiles | Already narrow, observable, and falsifiable. |
| Requested crop endpoints plus must-survive anchors and intentional exits | proposed `crop_boundary_anchor_integrity` exact profile | Current scale and placement facets do not own boundary semantics. |
| Requested in-image panel count, layout, order, and per-panel role | proposed `multi_panel_count_layout_sequence` exact profile | Not equivalent to a multi-file post or generic collage style. |
| Cross-variant invariants and allowed variation | candidate-pack provenance/authorial-core record | Useful for selection and regression, but not always a hard visual profile. |
| Generated visual-profile index | generated derivative only | Never the authored owner and never manually edited. |

## Proposed semantic components and confusion boundaries

### Component model

| Component | Observable evidence | Primary confusion boundary |
|---|---|---|
| `primary_anchor` | The requested face, action contact, object, environment feature, or pattern break is the first coherent proposition. | “Brightest thing” is not automatically the primary anchor; blur alone does not establish hierarchy. |
| `secondary_anchor_role` | A second element supports, counterbalances, intentionally competes, or is absent. | An intentional candid intrusion is not automatically clutter. |
| `shot_coverage` | Named scale plus the visible semantic anchors appropriate to the pose/action. | A crouching full-body topology is not the same rectangle as standing head-to-toe coverage. |
| `crop_boundary` | Each relevant frame edge has a requested endpoint or an explicitly flexible zone. | Garment “cropped top,” a close shot, and a crop operation are distinct concepts. |
| `frame_exit_continuity` | An arm, prop, motion trail, or body segment visibly continues toward an allowed edge. | Accidental truncation, missing anatomy, and intentional continuation must not be conflated. |
| `occlusion_owner` | A named foreground object, mirror/phone, body part, or scene structure visibly performs the occlusion. | Occlusion by an object is not the same as cropping at the image boundary. |
| `placement_relation` | Center, thirds, edge tension, symmetry, or counterbalance is measured relative to a named anchor. | Centered is not synonymous with bilateral symmetry. |
| `directional_space` | A visible gaze/motion/prop/line vector has more requested room ahead than behind. | Empty area behind the vector is not look/motion room. |
| `negative_space_function` | A contiguous low-detail field supports hierarchy, motion/look room, copy safety, or atmosphere. | Underexposure, overexposure, blur, deleted content, and an accidental loose crop are not automatically negative space. |
| `line_target_continuity` | A physical or visual line reaches or materially supports its named target. | A strong diagonal that terminates at a competing object is not necessarily a subject-leading line. |
| `depth_plane_chain` | Foreground interruption, subject plane, and background falloff remain separately readable. | Merely mentioning a background is not a three-plane topology. |
| `panel_topology` | Exact in-image count, geometry, separators, per-panel roles, and order are visible. | Several files attached to one post are not a collage inside one image. |
| `series_invariants` | Named relations remain stable while explicitly flexible pose/crop details can vary. | Repetition of all details is not required; silent loss of the primary proposition is not acceptable variation. |

### Exact-profile proposal 1: `crop_boundary_anchor_integrity`

Activation should require exact source evidence for a crop relation: a literal crop endpoint, `out of frame`/`outside frame`, `full body visible`, `head-to-mid-thigh`, `minimal/generous headroom`, or an equivalent user-authored clause. It must **not** activate from a shot-scale label alone or from garment terms.

Minimum observable component groups:

1. `coverage_target`: requested shot scale or explicit start/end boundary;
2. `required_visible_anchors`: semantic parts/contacts whose visibility makes the requested pose, action, product, or structure readable;
3. `permitted_frame_exits`: named parts allowed to continue outside a named edge, possibly empty;
4. `forbidden_cut_zones`: source-conditioned zones where a cut would destroy the proposition, possibly empty;
5. `occlusion_distinction`: whether missing content is caused by the frame edge, a named occluder, or intended self-overlap.

Confusion negatives:

- a cropped garment mistakenly activating image-crop semantics;
- a close-up with no literal boundary contract;
- a requested hand gesture cut away while another arm exit is allowed;
- a foreground leaf hiding an anchor but being recorded as frame-edge crop;
- “full body” reported as passed when the pose’s support/contact topology is not readable;
- an arm that simply disappears rather than continuing coherently toward the camera/edge.

Render gates:

- **thumbnail:** requested proposition and coverage class remain immediately readable; all high-priority required anchors survive reduction;
- **native:** each required anchor is visibly present; each permitted exit reaches the named edge with plausible continuation; no forbidden zone is cut; crop and object occlusion are correctly attributed;
- **both:** the intended pose/action/object topology remains complete even when its rectangular extent changes with pose.

### Exact-profile proposal 2: `multi_panel_count_layout_sequence`

Activation should require a literal in-image panel/collage/grid request with evidence for count or layout. It must not activate merely because a manifest post has multiple image files.

Minimum observable component groups:

1. `panel_count`: exact requested number;
2. `layout_geometry`: stack, row, grid, split, or other named arrangement;
3. `panel_boundaries`: readable separation without unintended merge;
4. `per_panel_role`: shot scale, moment, action, or subject role for each panel when specified;
5. `sequence_order`: top-to-bottom, left-to-right, temporal, or intentionally unordered.

Confusion negatives:

- three requested panels rendered as four cells;
- one panel duplicated while another role is omitted;
- borders or text boxes mistaken for panels;
- one continuous scene accidentally segmented by graphic artifacts;
- three separate output files counted as an in-image triptych;
- correct count but wrong per-panel shot-scale order.

Render gates:

- **thumbnail:** exact panel count and gross layout are immediately countable; no panel collapses into a decorative strip;
- **native:** separators remain continuous, each panel is independently coherent, specified role/order is preserved, and no duplicated or merged content substitutes for a missing panel;
- **both:** the hierarchy across the whole graphic does not erase the readability of any required panel.

## Candidate-pack/data proposals with exact suggested fields or layer

The following is a candidate/authorial-core record, not a proposal to place every field into every prompt. Fields remain `null` or absent unless supported by current requester/source evidence or a versioned vocabulary. Retrieval hits alone are advisory.

```yaml
composition_contract:
  provenance: requester | current_source | versioned_vocabulary
  source_evidence: "literal clause or bounded paraphrase"
  evidence_strength: weak | material | hard
  priority: P0 | P1 | P2

  primary_anchor:
    kind: face | action_contact | object | environment | pattern_break | other
    evidence: "what must read first"
  secondary_anchor:
    kind: face | action_contact | object | environment | pattern_break | none
    role: support | counterweight | intentional_competitor | none
  reading_order: []              # only when source evidence supports an order

  shot_coverage:
    scale: null                  # existing shot_scale enum
    required_visible_anchors: []
    permitted_frame_exits: []    # e.g. {anchor: camera_arm, edge: lower_right}
    forbidden_cut_zones: []
    occlusion_owner: scene_object | body_self_overlap | capture_device | frame_edge | none

  placement_relation:
    profile_id: null             # reuse an existing exact profile where applicable
    anchor: null

  directional_space:
    vector_owner: gaze | motion | prop | line | null
    ahead_side: left | right | up | down | null

  negative_space:
    function: hierarchy | look_motion_room | copy_safe | atmosphere | none
    field_owner: null
    exact_extent_evidence: null  # preserve a literal ratio only when source-authored

  panel_topology:
    panel_count: null
    layout: stack | row | grid | split | free_collage | null
    per_panel_roles: []
    reading_order: null
    divider_style: null

  invariant_fields: []
  flexible_fields: []
  omission_counterfactual: "what visible proposition fails if this relation is removed"
```

Recommended field-level ownership:

- put `required_visible_anchors`, `permitted_frame_exits`, `forbidden_cut_zones`, and `occlusion_owner` in the composition candidate/authorial-core record and bind them to `crop_boundary_anchor_integrity` only when activation is exact;
- put `panel_count`, `layout`, `per_panel_roles`, and `reading_order` in the candidate record and bind them to `multi_panel_count_layout_sequence` only for in-image layout language;
- extend or consume the existing `frame_hierarchy` quality layer for advisory first/second/ground ordering; do not introduce a global face-first default;
- retain existing placement/negative-space/look-room/leading-line/depth profiles as the sole hard owners of those literal relations;
- retain `invariant_fields` and `flexible_fields` in provenance-aware candidate data rather than turning every stable sample trait into a hard profile;
- never edit the generated visual-profile index directly; regenerate it only in a later authorized implementation phase.

## Regression and held-out tests

These are design candidates, not executed tests. A future qualification should freeze independent inputs per arm, keep prompt evidence and pixel scoring separate, and use `partial_is_fail` for any required gate.

### Positive and divergence cases grounded in the inspected corpus

| Test ID | Source topology | Expected gate behavior |
|---|---|---|
| `rp1650_centered_fullbody_corridor` | Centered standing coverage plus receding corridor. | Pass centered anchor and action-complete coverage; do not require bilateral scene symmetry. |
| `rp1899_three_stack_sequence` | Three stacked panels with three shot roles. | Pass exact count/layout/order. A four-cell output or role duplication fails. |
| `rp1898_four_grid_control` | 2×2 four-cell grid. | Pass only the four-grid contract; fail a three-panel contract. |
| `rp1629_generic_refined_no_contract` | Generic “refined composition” with varying coverage. | Must not activate an exact crop-boundary profile. |
| `rp1927_raised_arm_crop_divergence` | Both arms/hands-out and tight endpoint requested, not delivered. | Fail required action anchors and requested crop topology; a roughly close crop is insufficient. |
| `rp1926_wrong_side_room_conditional` | Rightward gaze with larger field behind. | Fail only when look-room is explicitly requested; otherwise remain unscored for that profile. |
| `rp2299_foreground_leaf_owner` | Head-to-mid-thigh, roof headroom, foreground leaf, greenhouse depth. | Attribute leaf occlusion to foreground, not frame crop; retain required coverage anchors. |
| `rp2325_selfie_arm_exit` | High close selfie with camera arm outside frame. | Pass coherent permitted exit; fail if the arm disappears internally or a required hand gesture is lost. |
| `rp2101_environment_primary` | Dominant upper-left environmental sign. | Permit environment-first hierarchy when source-authored; do not force face-first. |
| `rp2323_intentional_competitor` | Partial figure and objects intentionally compete. | Preserve `intentional_competitor`; do not auto-clean the frame. |
| `rp2637_crouch_action_complete` | Full-body crouch in a compact silhouette. | Judge head/hands/knees/feet/support topology, not standing height or a fixed body-box ratio. |
| `rp2707_hierarchy_invariant` | Face dominance and warm field survive crop/pose variation. | Preserve named invariants while allowing flexible pose/crop fields. |
| `rp2526_sky_field_selfie` | Face priority, arm perspective, blue open field. | Pass face/field/exit relations; keep arm as a legitimate strong secondary mass. |

### Hard negatives

1. **Garment lexical collision:** “cropped top” with no image boundary instruction must not activate crop semantics.
2. **Blur-only hierarchy:** a sharp subject against blur fails if a brighter or semantically stronger competitor destroys the requested first read.
3. **Empty exposure substitute:** a clipped white or crushed black region without contour/material evidence does not pass negative space.
4. **Wrong-side direction:** open space behind a requested gaze or motion vector does not pass look/motion room.
5. **Genre overactivation:** `mirror selfie` alone remains advisory unless a physical frame-within-frame relation is explicitly required.
6. **Centered/symmetric collision:** a centered subject in an asymmetrical setting must not activate axial bilateral symmetry.
7. **Crop/occlusion collision:** an anchor hidden by a foreground object cannot be reported as a successful intentional frame exit.
8. **Multi-file/panel collision:** four files in one post do not satisfy a requested 2×2 in-image grid.
9. **Bright-environment false rejection:** a source-authored environment-primary frame must not fail a person-first rule that was never requested.
10. **Compressed-pose false failure:** a crouch that preserves all action contacts must not fail merely because it is not a standing head-to-toe silhouette.

### Held-out non-portrait cases

1. **Product and package:** preserve the hero object’s outline, functional cap/opening, and label region while allowing an explicitly cropped support surface. Do not require readable text unless separately requested.
2. **Architecture:** validate a physical frame-within-frame through opening boundaries, thickness, and depth with no person present.
3. **Tool/action documentary frame:** preserve hand/tool/workpiece contact and the visible result while allowing nonessential body regions to exit the frame.
4. **Food/process sequence:** enforce a three-panel preparation/process/result order without copying portrait-specific face hierarchy.
5. **Landscape motion room:** give a moving vehicle/animal/object visible space ahead, with no face or gaze dependency.
6. **Copy-safe commercial frame:** distinguish a source-authored clean copy field from aesthetic atmospheric negative space and from accidental blank exposure.

## Limitations and bounded decision

- The prompt scan is phrase-based. It has high recall for literal terminology but does not resolve every negation, translation nuance, or implicit composition.
- The 40-image sample is purposive and only 0.8% of 4,908 delivered images. No sampled pixel ratio is generalized to the full corpus.
- Delivered corpus pixels establish only what is visible in those artifacts. They do not establish the generator, seed, reference contribution, selection history, or causal effect of any one clause.
- No new image was generated, no independent render arm was run, and no proposed gate has been render-qualified.
- Current runtime behavior, package consistency, generated-index consistency after a hypothetical edit, and user judgment remain unscored.
- No external source was necessary: the frozen repository contracts already define the relevant mechanisms, and the corpus provides direct prompt/pixel evidence for the identified gaps. This avoids importing generic composition folklore as a new default.
- The two proposed exact profiles and candidate fields remain unimplemented. A future implementation must add source/registry/generated-index/test lineage in the correct owning layers and must re-run package, prompt, request, and pixel checks separately.

Bounded decision by proposal:

- **proposed:** `crop_boundary_anchor_integrity` as a narrow exact visual-obligation profile;
- **proposed:** `multi_panel_count_layout_sequence` as a narrow exact visual-obligation profile;
- **proposed:** provenance-aware candidate fields for anchor ownership, allowed exits, forbidden cut zones, occlusion owner, panel topology, and invariant/flexible fields;
- **revise:** candidate selection should link literal requests to the existing 12 composition profiles and use `frame_hierarchy` only as broad advisory craft guidance;
- **reject:** new duplicate global profiles for generic negative space, generic hierarchy, generic leading lines, or face-first composition;
- **reject:** treating corpus frequency, genre implication, BM25F/embedding retrieval, or a multi-file post as permission for a hard exact obligation.

## Evidence appendix

### Inspected image paths

Each listed post contributed `_01` and `_02`, for 40 inspected images total:

```text
generated/reactorprompt-export-20260902-incremental/images/1629_DY7SCUgGi2w_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1630_DY7XOrumtD0_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1649_DY9Zr6JGkM3_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1650_DY9ZkxOmshC_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1898_DZuSUeeGr4m_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1899_DZuSLuTms2I_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1926_DZ2lMpAmhMl_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/1927_DZ2hDNGmlld_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2101_DaeuqxKmsFW_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2102_DaffrQFGkl8_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2299_DbcuYZ-GmbV_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2303_DbcqIbnmvEm_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2323_DbiaDwWGu-1_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2325_DbiZ-JXGi_d_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2525_DcIofIDGmZD_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2526_DcIwVe3GryI_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2629_DcgO61yGnce_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2637_DcfQm3DmoSa_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2705_DcqEFBlGiPU_{01,02}.jpg
generated/reactorprompt-export-20260902-incremental/images/2707_DcqC17IGtsA_{01,02}.jpg
```

### Prompt-scan heuristic and command

The exact execution used Python `re.search` over every non-empty `prompt` value. The compact pattern vocabulary below reproduces the group boundaries; alternatives were joined with case-insensitive word-boundary regexes and the Korean literals shown here.

```text
orientation_or_aspect:
  vertical | portrait orientation | landscape orientation | horizontal | square |
  9:16 | 4:5 | 1:1 | aspect ratio | 세로 | 가로 | 정사각형
shot_scale_or_coverage:
  extreme wide | wide shot | full-body | full-length | three-quarter |
  medium long | medium shot | medium close | close-up | extreme close |
  head-to-toe | waist-up | chest-up | head and shoulders | head-to-mid-thigh |
  upper-body | entire body | whole body | 전신 | 반신 | 클로즈업 | 상반신 | 허리 위
crop_or_edge_policy:
  tight crop | tightly cropped | cropped/crop at/from/below/above | out of frame |
  outside frame | frame cuts | cut off | partially out of frame | minimal/generous headroom |
  headroom | fill the frame | frame-filling | edge tension | frame exit |
  프레임 밖 | 화면 밖 | 여백 없이 | 헤드룸
placement_or_balance:
  centered | off-center | left/right weighted | upper/lower corners | rule of thirds |
  symmetry | asymmetry | balanced composition | counterbalance | dead center |
  slightly left/right of center | 중앙 | 정중앙 | 좌측 | 우측 | 비대칭 | 대칭
negative_or_directional_space:
  negative/empty/open/copy space | look/looking/lead/nose/motion room |
  room/space ahead or in front | gaze direction | 네거티브 스페이스 | 여백 | 시선/진행 방향
foreground_depth_or_occlusion:
  foreground | midground | background | layered depth | depth layer | leading line |
  receding | vanishing point | perspective line | frame within frame |
  foreground occlusion/blur/object/element | partially obscured | occluded | three-plane |
  전경 | 중경 | 배경 | 원근 | 소실점 | 가림 | 레이어드 깊이
line_axis_or_visual_path:
  diagonal composition/framing | strong diagonal | visual path/flow | S-curve |
  leading line target | axial composition | frame within frame | converging lines |
  대각선 구도 | 시선 유도선 | 프레임 속 프레임
attention_hierarchy:
  focal point | first read | visual/attention hierarchy | primary/secondary focus |
  draws the eye | dominant focal | face/subject dominant | hierarchy of attention |
  초점점 | 시선이 먼저 | 주 피사체 | 시각적 위계
multipanel_or_graphic_layout:
  diptych | triptych | split-screen | two/three/four-panel | 2x2 | collage |
  contact sheet | comic panel | panel/grid layout | 2/3/4분할 | 콜라주 | 패널 구도
```

Core command shape:

```bash
python - <<'PY'
import json, re
rows = json.load(open('generated/reactorprompt-export-20260902-incremental/manifest.json'))
texts = [(str(r['id']), r.get('prompt') or '') for r in rows if (r.get('prompt') or '').strip()]
# G contains the nine case-insensitive phrase-group regexes documented above.
hits = {name: {rid for rid, text in texts if re.search(rx, text)} for name, rx in G.items()}
for name in G:
    print(name, len(hits[name]))
print('any', len(set().union(*hits.values())))
PY
```

### Repository inspection commands

```bash
shasum -a 256 \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json

jq -r '.profiles[] | [.id,.category] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json

jq '{shot_scale:.facet_vocab.shot_scale,
     placement:.facet_vocab.placement,
     platform_frame:.facet_vocab.platform_frame}' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json

jq '.photographic_craft.dimensions[] | select(.id=="frame_hierarchy")' \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json
```

Image inspection used the local image viewer on every listed path with `detail=high`; representative crop/edge cases were reopened with `detail=original`.

### External sources

None. External terminology was not needed to define the proposed mechanisms; the corpus pixels and frozen authored repository contracts were sufficient for this bounded design study.

## Final bounded status

**proposed** — research/design only; implementation, runtime behavior, render qualification, and user judgment are all still unscored.
