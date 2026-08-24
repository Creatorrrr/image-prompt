---
id: lane.subject-appearance
version: 1
priority: 85
activation: matched
select_types:
  - subject
  - style
select_facets: []
select_module_ids:
  - detail.human-face-likeness
  - detail.human-body-form
  - detail.clothing-fashion
required_common_modules:
  - core.visual-evidence
  - core.fidelity-discipline
owns_sections:
  - subject-form
  - human-appearance-evidence
  - person-prior-candidate
  - skin-visibility-evidence
required_topics:
  - subject-role
  - visible-form
  - appearance-drift-risk
  - intrinsic-induced-confounds
---

# Analysis lane: subject appearance

## Role

Own visible subject form and non-identifying appearance evidence. For humans, separate frame prominence from fidelity salience, identity context from generation approximation, and intrinsic surface evidence from induced effects.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred demographic label, another lane's conclusions, or draft prompt prose.

## Output contract

Return one `reverse-image-analysis-lane-report/v1` object. A broad human finding is a source-visible generation approximation, never inferred nationality or factual identity. Record default-drift risk, geometry sufficiency, and omission counterfactual; hand surface-color and lighting attribution to the color/light lane.

## Completion gate

Dispose every required topic and assigned module. A small or secondary subject may still be fidelity-primary. Unsupported identity inference and silent broad-prior omission both fail this lane.
