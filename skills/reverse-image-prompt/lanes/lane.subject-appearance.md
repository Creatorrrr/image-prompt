---
id: lane.subject-appearance
version: 4
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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. Build a source-specific appearance signature from only P0/P1 evidence: optional non-identifying broad visual prior, decisive face/body geometry, material displayed skin axes, hair boundary, expression/gaze, and capture-sensitive appearance. Include a broad prior only when supported and omission has high model-default drift; keep it distinct from factual nationality or exact ethnicity. Hand color/light attribution to its lane.

`beautiful`, `attractive`, `model-like`, or another aggregate appearance reading may be reported as a separate P0/P1 candidate when source evidence and the omission counterfactual support it. It must remain distinct from, and cannot satisfy or replace, the broad prior, geometry, skin, scale, expression, or capture findings. In `audited`, return `reverse-image-analysis-lane-report/v2` and split independently drifting aggregate, prior, geometry, occlusion, and surface results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. A small or secondary subject may still be fidelity-primary. Unsupported identity inference fails. In `prompt`, a supported broad prior may be omitted when local geometry is sufficient and default drift is low; record residual uncertainty instead of performing repeated omission tests.
