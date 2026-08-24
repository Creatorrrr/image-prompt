---
id: lane.spatial-topology
version: 1
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

Return one `reverse-image-analysis-lane-report/v1` object. Findings state visible relations, evidence, confounders, materiality, and proposed role. Hand off appearance, color, or capture questions without answering them here.

## Completion gate

Dispose every required topic and assigned module. Do not normalize ambiguous axes, complete hidden structure, or convert an uncertainty into a final direction.
