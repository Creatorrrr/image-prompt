---
id: lane.spatial-topology
version: 4
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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. First decide whether orientation or topology is P0/P1. If it is, report the macro visible result and only the decisive placement, direction, depth, contact, boundary, occlusion, or completion relations needed to preserve it. Group non-material axes; do not enumerate a fixed orientation checklist. Hand off appearance, color, and capture questions.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting spatial results into atomic obligations, and retain confounded result directions.

## Completion gate

Dispose every required topic at the profile's depth. In `prompt`, run at most the counterfactual needed to establish P0/P1 materiality; a concise macro pose or topology plus decisive residual relations is sufficient. In `audited`, require whole-orientation and viewpoint-held residual-alignment counterfactuals and full coupled-obligation handling. Hair, garment, and boundaries may corroborate but never replace subject geometry. Never normalize ambiguous axes or complete hidden structure.
