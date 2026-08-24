---
id: lane.global-composition
version: 1
priority: 100
activation: always
select_types:
  - core
select_facets: []
select_module_ids:
  - concept.primary-relationship
required_common_modules: []
owns_sections:
  - direct-appeal
  - global-composition
  - major-region-hierarchy
required_topics:
  - perceptual-proposition
  - frame-and-crop
  - major-regions
  - fidelity-mode
---

# Analysis lane: global composition

## Role

Own the image-wide proposition, frame, crop, major-region hierarchy, and dominant fidelity mode. Apply the assigned core modules; this file does not redefine their visual rules.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and the route-assigned modules. Do not receive another lane's findings or a draft prompt.

## Output contract

Return one `reverse-image-analysis-lane-report/v1` object. Record source observations, material findings, uncertainties, omission checks, and handoffs under the owned sections. Propose control requirements, not final prompt prose.

## Completion gate

Dispose every required topic, review every assigned module, retain source uncertainty, and report cross-lane dependencies without resolving them by assumption.
