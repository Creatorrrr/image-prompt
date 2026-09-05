---
id: lane.spatial-topology
version: 7
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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. First decide whether orientation or topology is P0/P1. If so, report one macro, then hold viewpoint and crop while testing its source-visible component, frame, facing/gaze, depth, support/contact, boundary, occlusion, and completion relations. Inspect only current-source evidence. Mark the macro `sufficient`, `lossy`, or `uncertain`; retain only decisive P0/P1 residuals. Distinguish region-to-frame position from inter-region direction. Separately disposition material proximity, overlap, and surviving visibility; if direction survives extreme displacement, hand off both frame relations, the inter-region relation, and a direction-held counterfactual. Treat alignment phrases as positive controls over every explicit or implicit axis. Hand off appearance, color, and capture questions structurally.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting results into atomic obligations, retain confounded directions, and close every high-degeneracy cross-component placement.

## Completion gate

Dispose every required topic at the profile's depth. In `prompt`, run at most the counterfactual needed to establish P0/P1 materiality and the lightweight viewpoint-held summary-adequacy check above; a concise macro pose or topology plus only at-risk residual relations is sufficient. In `audited`, require an isolated per-axis neutralization test for each `flexible` or `not-material` decision, whole-orientation and viewpoint-held residual-alignment counterfactuals, full coupled-obligation handling, and an exact explicit/implicit effect audit for every emitted spatial clause. Low-confidence or wholly confounded axes become `uncertain` unless an invariant coupled effect preserves the joint result. Surface, garment, and boundary cues may corroborate but never replace source geometry. Never normalize ambiguous axes or complete hidden structure.
