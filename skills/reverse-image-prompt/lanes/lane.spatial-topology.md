---
id: lane.spatial-topology
version: 6
priority: 90
activation: matched
select_types:
  - concept
select_facets: []
select_module_ids:
  - subject.human
  - detail.pose-hands-gesture
  - detail.tight-selfie-hierarchy
  - detail.accessory-torso-budget
  - detail.face-hand-gesture
required_common_modules:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
owns_sections:
  - spatial-orientation
  - component-topology
  - contact-occlusion-support
required_topics:
  - orientation-coverage
  - component-relations
  - contact-and-occlusion
  - completion-risk
---

# Analysis lane: spatial topology

## Role

Own source-visible orientation, component topology, contact, support, occlusion, and completion risk. Use the assigned modules as the sole domain instructions.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive appearance conclusions or prompt wording.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. First decide whether orientation or topology is P0/P1. If it is, report one macro visible result, then hold the observed viewpoint and crop fixed and test whether that summary preserves the source-visible component-to-subject, subject-to-frame, facing or gaze, depth-order, support, contact, boundary, occlusion, and completion relations that jointly create the read. This is not a fixed checklist: inspect only relations supported by the current source. Mark the macro `sufficient`, `lossy`, or `uncertain`, and retain only decisive P0/P1 at-risk relations that the macro does not carry. Before handoff, treat each alignment-style phrase as a positive control and enumerate every spatial axis it would explicitly or implicitly actuate; never recommend a clause that normalizes an unsupported axis. Hand off appearance, color, and capture questions through the structured compact handoff.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting spatial results into atomic obligations, and retain confounded result directions.

## Completion gate

Dispose every required topic at the profile's depth. In `prompt`, run at most the counterfactual needed to establish P0/P1 materiality and the lightweight viewpoint-held summary-adequacy check above; a concise macro pose or topology plus only at-risk residual relations is sufficient. In `audited`, require an isolated per-axis neutralization test for each `flexible` or `not-material` decision, whole-orientation and viewpoint-held residual-alignment counterfactuals, full coupled-obligation handling, and an exact explicit/implicit effect audit for every emitted spatial clause. Low-confidence or wholly confounded axes become `uncertain` unless an invariant coupled effect preserves the joint result. Surface, garment, and boundary cues may corroborate but never replace source geometry. Never normalize ambiguous axes or complete hidden structure.
