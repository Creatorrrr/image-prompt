---
id: lane.color-light-material
version: 3
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

Own causal separation of intrinsic color, displayed tone, illumination, shadow, and material response. Apply the routed fidelity modules rather than duplicating their rules here.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Receive subject/region identifiers as neutral handoff keys, not appearance conclusions.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. Report only P0/P1 regional color, displayed-tone, light-to-form, or material-response effects and the minimum protected relation needed to avoid drift. Prefer stable visible results when physical attribution is uncertain; group non-material axes instead of completing full ledgers.

In `audited`, return `reverse-image-analysis-lane-report/v2`, keep region/protected scope explicit, and split material intrinsic color, displayed tone, light, shadow, response, and cross-region results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not pool mixed regions, convert displayed skin color into biological truth, or let a global control erase a protected P0/P1 relation.
