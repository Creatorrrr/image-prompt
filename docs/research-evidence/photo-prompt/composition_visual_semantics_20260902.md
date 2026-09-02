# Composition visual-semantics evidence — 2026-09-02

## Scope

This note records the research abstraction behind twelve runtime visual-relation profiles. It is maintenance evidence only. Source titles, URLs, and research labels must not enter candidate prompts or runtime semantic text.

The profiles describe observable image relations, not universal aesthetic laws. Exact request-scoped terms may activate hard obligations. Paraphrases, component similarity, BM25F, embeddings, and fused retrieval remain advisory until explicitly selected.

## Sources and bounded derivations

- Amirshahi et al., *Evaluating the Rule of Thirds in Photographs and Paintings* (2014), DOI: https://doi.org/10.1163/22134913-00002024
  - The thirds grid can be operationalized as focal placement near thirds lines or intersections.
  - A thirds measure was only weakly related to aesthetic ratings; therefore the runtime profile asserts a spatial relation, never beauty or quality.
- Palmer, Gardner, and Wickens, *Aesthetic Issues in Spatial Composition* (2008): https://palmerlab.berkeley.edu/pdf/PalmerGardner%26Wickens-1.pdf
  - Center placement and inward-facing direction showed context-sensitive preference biases for single objects.
  - This supports distinct center-anchor and look/motion-room relations, not a universal placement preference.
- Wagemans et al., *A Century of Gestalt Psychology in Visual Perception I* (2012), DOI: https://doi.org/10.1037/a0029333 and full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/
  - Grouping and figure-ground organization are separate perceptual problems.
  - Similarity, continuity, symmetry, common region, connectedness, and border ownership support explicit pattern, leading-line, symmetry, enclosure, and figure-ground component groups.
- Itti and Koch, *Computational Modelling of Visual Attention* (2001), DOI: https://doi.org/10.1038/35058500 and PubMed: https://pubmed.ncbi.nlm.nih.gov/11256080/
  - Salience is context-dependent and combines feature conspicuity with scene/object constraints.
  - Candidate profiles therefore require subject-to-field and primary-to-secondary relations; a contrast adjective alone is not sufficient.
- Kourtzi and Kanwisher, *Activation in Human MT/MST by Static Images with Implied Motion* (2000), DOI: https://doi.org/10.1162/08989290051137594 and PubMed: https://pubmed.ncbi.nlm.nih.gov/10769305/
  - Static images can carry implied dynamic information.
  - The peak-action profile makes that information falsifiable through simultaneous cause, trajectory, and unfinished consequence.
- Yao and Fei-Fei, *Recognizing Human-Object Interactions in Still Images by Modeling the Mutual Context of Objects and Human Poses* (2012), DOI: https://doi.org/10.1109/TPAMI.2012.67 and PubMed: https://pubmed.ncbi.nlm.nih.gov/22392710/
  - Pose and interacted objects provide mutual context in still images.
  - Event-phase evidence therefore binds the actor or moving object to a visible trigger and consequence rather than accepting a generic action pose.
- Nikon, *5 Easy Composition Guidelines*: https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/5-easy-composition-guidelines
  - Industry practice describes thirds intersections, leading lines toward a focal area, and additional space in front of a directed subject.
  - These are translated into inspectable relations and remain guidelines rather than guaranteed aesthetic outcomes.
- Sony, *Lens Basics*: https://www.sony.com/electronics/support/articles/00268239
  - Field of view and camera distance change visible perspective and relative background scale.
  - Depth candidates must retain explicit plane anchors, overlap, and scale recession rather than relying on focal-length labels.

## Implemented profile map

| Profile | Observable all-of relation | Principal false substitute |
|---|---|---|
| `third_grid_focal_anchor_relation` | one primary anchor near a thirds intersection, off center, with surrounding field | grid overlay or contextless crop |
| `centered_primary_anchor_relation` | identity/action anchor at true frame center with central first-read dominance | symmetric background with an off-axis subject |
| `axial_bilateral_symmetry_relation` | explicit axis, paired contours, matched spacing and weight | one centered object |
| `asymmetric_counterbalance_relation` | dominant off-center mass, separated smaller counterweight, intentional field | random clutter or mirror symmetry |
| `leading_line_target_continuity` | physical origin, continuous path, termination at primary target | decorative stripe or line to nowhere |
| `look_motion_room_direction_relation` | visible direction vector, in-frame origin, more room ahead | empty space behind the subject |
| `subject_field_negative_space_relation` | large contiguous low-detail field, clean contour, hierarchy | empty crop or lost exposure |
| `frame_within_frame_boundary_relation` | scene-bound foreground opening, three-sided enclosure, near-plane depth | digital vignette or graphic border |
| `three_plane_depth_chain` | foreground/middle/background anchors, adjacent overlap, scale recession | flat collage bands or blur alone |
| `pattern_break_focal_exception` | stable repeated baseline and exactly one focal exception | random variety or several anomalies |
| `primary_secondary_figure_ground_hierarchy` | primary first-read, subordinate secondary, supportive ground | blur-only separation or equal focal points |
| `peak_action_event_phase` | in-frame cause, directional mid-transition, unfinished consequence | posed before-state or completed aftermath |

## Compatibility boundaries

- `centered_primary_anchor_relation` conflicts with `third_grid_focal_anchor_relation`.
- `axial_bilateral_symmetry_relation` conflicts with `asymmetric_counterbalance_relation`.
- `subject_field_negative_space_relation` conflicts with frame-filling crop candidates.
- Golden ratio, golden spiral, golden triangle, rule of odds, harmony, visual energy, and anti-composition remain advisory vocabulary. Current evidence does not justify universal beauty claims or default hard gates.
- Camera angle belongs to `camera_direction`, shot scale to `shot_scale`, focus behavior to `focus`, and physical panning to `motion`. The `composition` slot owns spatial relations only.

## Qualification rule

Every selected profile contributes its complete hard-gate set. Missing, partial, or unevidenced gates fail. Package and prompt PASS do not imply delivered-pixel PASS; technical pixel qualification does not imply requesting-user preference.
