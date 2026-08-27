---
id: lane.subject-appearance
version: 6
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

Own visible subject form and non-identifying appearance evidence. For humans, separate externally sourced identity context, non-identifying person prior, displayed-skin surface, and appearance gestalt, as well as frame prominence from fidelity salience and intrinsic evidence from induced effects.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred demographic label, another lane's conclusions, or draft prompt prose.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. Report four independently prioritized decisions: exact identity context only from the raw user request or trusted metadata; an optional non-identifying person prior corrected by decisive geometry; displayed-skin axes and region scope; and an optional person-aesthetic gestalt. Mark a coupled macro finding with summary adequacy and only source-supported at-risk residuals. Never propose race, ethnicity, nationality, or another protected identity from source pixels. Hand color/light attribution to its lane through the structured compact handoff.

`beautiful`, `attractive`, `model-like`, or another aggregate appearance reading may be reported as a separate P0/P1 candidate when source evidence and the omission counterfactual support it. Record intended and protected effect dimensions plus the owner needed for each intended decomposition; identity context is always protected. The aggregate cannot replace prior, geometry, skin, scale, expression, garment, pose, light/color, or capture findings. In `audited`, return `reverse-image-analysis-lane-report/v2`, supply `human-appearance/v3`, and split independently drifting results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. A small or secondary subject may still be fidelity-primary. Unsupported identity inference or an aggregate without an effect budget fails. A broad prior may be omitted when local geometry is sufficient and default drift is low; record residual uncertainty instead of repeated omission tests.
