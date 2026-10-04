# Neutral new-author camera handoff schema

Read only the public SKILL procedure, current precore creative-control resolver/
definition and neutral catalog before drafting. This file is a neutral explanation
of the SKILL wire, not camera examples or implementation guidance. The complete
core/envelope/embodiment/feature-selection shapes remain those in SKILL.md.

## Authoring order for independent evaluation

1. Supply exact EN/KO requester text and resolved creative context first.
2. Coordinator freezes envelope and resolves only candidate-free precore controls.
3. Author reads that saved brief and the current neutral catalog, then writes all
   scene fields, baseline, anchors, assertion, feature selection and applicable
   embodiment review. No tests, candidate/profile data, old cases or code exposure.
4. Freeze complete authored semantic inputs. Technical hashes/offsets may be
   computed, but coordinator must not infer or repair subject/event/anchors/locks,
   pad prose or silently rewrite it. Record contract failures as delivered.
5. Validate pre-core record and use actual public generate_photo_prompt CLI with
   --new-author-camera-evidence, and --require-camera-evidence for each axis
   independently judged prescribed from the requester. Candidate data loads only
   after authored inputs validate. Evaluate ownership interpretation separately.

## Camera declaration, in existing semantic_assertions

```
assertion_id: author-chosen unique ID
dimension: camera
polarity: advisory when camera remains open; required only if already wholly locked
source_span_ids: exact active requester span IDs
affected_dimensions: [camera]
axes:
  camera_axis_review: camera_axis_review_v1
  capture_owner: camera if any axis is requested, otherwise unprescribed
  direction_requirement: requested | open | excluded
  height_requirement: requested | open | excluded
evidence:
  owner_phrase: exact baseline phrase naming actual capture camera (requested only)
  direction_phrase: exact baseline direction evidence (direction requested only)
  height_phrase: exact baseline height evidence (height requested only)
```

No requested axes: evidence is empty, not invented camera prose. Owner is at most
16 words; an axis phrase at most 24 words; each stays inside a clause. Each requested
axis phrase occurs in the corresponding existing camera-target viewpoint property
anchor, or justified whole-camera anchor. Do not lock an unrequested choice.
Excluded means negative-only prescription: no positive axis query is supplied;
it needs requester-grounded user_exclusions and is not an inferred opposite angle.

On a partial prescription camera stays open and its property anchor locks only the
requested meaning. Advisory handoff metadata is not permission to edit that duty.
Source/type/literal checks cannot establish correct capture ownership, lens
attachment, request interpretation or actual image quality; the author/reviewer
must judge those. The marker and requirement states are protocol metadata, never
words to add to baseline prose or candidate embedding data.
