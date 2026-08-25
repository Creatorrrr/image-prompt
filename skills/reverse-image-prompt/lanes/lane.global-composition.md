---
id: lane.global-composition
version: 3
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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`: one primary viewer read, only P0/P1 proposition, frame/crop, and major-region findings, compact P2 support, and grouped P3/non-material topics. Use a change counterfactual only to decide whether a region or crop is identity-bearing. Propose controls, not prompt prose.

In `audited`, return `reverse-image-analysis-lane-report/v2` and split material frame, crop, and region-hierarchy results into independently drifting atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth, review every assigned module, retain source uncertainty, and report cross-lane dependencies without resolving them by assumption. Do not itemize minor scenery merely because it is visible.
