---
id: lane.color-light-material
version: 5
priority: 82
activation: matched
select_types: []
select_facets: []
select_module_ids:
  - detail.color-tone-fidelity
  - detail.light-form-fidelity
required_common_modules:
  - core.visual-evidence
  - core.background-color
  - core.fidelity-discipline
owns_sections:
  - color-tone
  - light-form
  - material-response
required_topics:
  - intrinsic-color
  - displayed-tone-scope
  - illumination-and-shadow
  - material-response
---

# Analysis lane: color, light, and material

## Role

Own causal separation of intrinsic color, displayed tone, illumination, shadow, and material response. For human skin, own displayed surface evidence only, never identity or biological color. Apply the routed fidelity modules rather than duplicating their rules here.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Receive subject/region identifiers as neutral handoff keys, not appearance conclusions.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. Report only P0/P1 regional color, displayed-tone, light-to-form, or material-response effects. When a compact illumination or form summary represents several relations, test its adequacy and retain the smallest independently drifting at-risk subset among target/reference region, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, background spill, and pose dependency. This list is a causal vocabulary, not a required inventory. Each residual names its source-relative regions and visible result; generic lighting or rig language never substitutes for those relations. For displayed skin, hand off subject/region, P0-P3 viewer priority, observation scope, stable axes, coverage, and confounds; do not supply a demographic label. Prefer stable visible results when physical attribution is uncertain.

In `audited`, return `reverse-image-analysis-lane-report/v2`, keep region/protected scope explicit, and split material intrinsic color, displayed tone, light, shadow, response, and cross-region results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. When pose or deformation changes the visible light-to-form result, record that dependency instead of treating the shading as intrinsic surface. Do not pool mixed regions, convert displayed skin into identity or biological truth, let an appearance anchor change an unowned skin axis, or let a global control erase a protected P0/P1 relation.
