---
id: lane.color-light-material
version: 1
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

Return one `reverse-image-analysis-lane-report/v1` object. Keep region scope and protected regions explicit, expose unresolved causal attribution, and propose axis-level requirements rather than final adjectives or composite labels.

## Completion gate

Dispose every required topic and assigned module. Do not pool mixed regions, convert display color into biological truth, or let a global control erase a protected local relation.
