---
id: lane.information-layout
version: 3
priority: 75
activation: matched
select_types: []
select_facets: []
select_module_ids:
  - subject.document-data-diagram
  - medium.screenshot-ui
  - concept.screen-frame-within-frame
  - detail.text-logo-label
required_common_modules:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
owns_sections:
  - information-hierarchy
  - reading-order
  - text-and-ui-legibility
required_topics:
  - container-hierarchy
  - reading-order
  - text-legibility
  - interface-boundaries
---

# Analysis lane: information layout

## Role

Own information hierarchy, reading order, text/UI legibility, and nested frame boundaries. Existing routed modules remain the domain source of truth.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive other lane conclusions or final wording.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1` with only P0/P1 container hierarchy, reading order, legibility, or nested-boundary findings; compress supporting structure and group unreadable or incidental detail. In `audited`, return `reverse-image-analysis-lane-report/v2` with atomic layout obligations. Never transcribe unreadable content or write final prose.

## Completion gate

Dispose every required topic at the profile's depth. Preserve low legibility and distinguish the source image frame from screens, documents, or embedded panels.
