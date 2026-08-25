---
id: lane.medium-aesthetic-capture
version: 4
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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1` with the fidelity ceiling and only the P0/P1 capture or production cues whose change would alter the viewer's read. Compress P2 artifacts and omit P3 inventory. A broad aesthetic or mood reading may become one provenance-bound aggregate candidate when it is high-confidence P0/P1 evidence and omission causes material drift; report its literal causal controls separately so integration can retain-and-decompose it.

In `audited`, return `reverse-image-analysis-lane-report/v2` and decompose a material aesthetic candidate into independently drifting visible obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not upgrade fidelity, infer an artist/camera, or use a genre, quality, mood, or beauty label as a substitute for visible controls. Do not erase a material aggregate reading merely because the controls have been decomposed.
