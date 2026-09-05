---
id: lane.medium-aesthetic-capture
version: 6
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

Own medium/process evidence, capture character, production aesthetic, and meaningful artifacts. Keep portrait-production aesthetics separate from identity and from a person's source-visible appearance gestalt.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred genre label or a draft prompt.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2` with the fidelity ceiling and only P0/P1 capture or production cues. For humans, report cosmetic visibility, displayed-skin finish, optical softness/bloom, retouching, and polish as separable effects keyed to the shared subject; do not duplicate the subject lane's person-aesthetic aggregate. A broad production aesthetic may become one provenance-bound aggregate candidate only when omission causes material drift; report its literal causal controls separately. If capture evidence makes regional light, shadow, or light-induced form P0/P1 but `detail.light-form-fidelity` is not assigned, emit a route-required structured handoff to `lane.color-light-material` instead of replacing the missing owner with a capture adjective.

In `audited`, return `reverse-image-analysis-lane-report/v2` and decompose a material aesthetic candidate into independently drifting visible obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not upgrade fidelity, infer an artist/camera, or use genre, quality, mood, or beauty as a substitute for visible controls. Prevent a person-aesthetic handoff from adding makeup, glossy skin, facial sculpture, relighting, or editorial finish outside its declared intended dimensions.
