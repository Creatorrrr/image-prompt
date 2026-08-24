---
id: lane.medium-aesthetic-capture
version: 1
priority: 78
activation: matched
select_types:
  - medium
select_facets: []
select_module_ids:
  - detail.low-quality-artifacts
required_common_modules:
  - core.visual-evidence
  - core.fidelity-discipline
owns_sections:
  - medium-evidence
  - capture-character
  - portrait-production-aesthetic
required_topics:
  - medium-and-process
  - capture-fidelity-ceiling
  - production-aesthetic
  - artifact-preservation
---

# Analysis lane: medium, aesthetic, and capture

## Role

Own medium/process evidence, capture character, production aesthetic, and meaningful artifacts. Keep regional or cultural portrait aesthetics separate from a person's identity.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred genre label or a draft prompt.

## Output contract

Return one `reverse-image-analysis-lane-report/v1` object. Decompose any broad aesthetic candidate into visible causal findings and flag uncalibrated shorthand as an omission risk or uncertainty.

## Completion gate

Dispose every required topic and assigned module. Do not upgrade fidelity, infer an artist/camera, or use a broad genre label as a substitute for visible controls.
