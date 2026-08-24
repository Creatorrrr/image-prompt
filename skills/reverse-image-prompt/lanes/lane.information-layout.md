---
id: lane.information-layout
version: 1
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

Return one `reverse-image-analysis-lane-report/v1` object with evidence-scoped layout findings, uncertainties, completion risks, and handoffs. Do not transcribe unreadable content or write the final prompt.

## Completion gate

Dispose every required topic and assigned module. Preserve low legibility and distinguish the source image frame from screens, documents, or embedded panels.
