---
name: image-prompt-skill-improver
description: Diagnose and improve an existing image-prompt or reverse-image-prompt skill from source/render comparisons, user aesthetic feedback, and test evidence. Use when repeated visual-fidelity failures should become generalizable skill rules, tools, or holdout evaluations; not for an ordinary one-off prompt or render.
---

# Image Prompt Skill Improver

## Purpose

Turn observed failures in an image-prompt workflow into the smallest reusable improvement that changes future behavior without encoding the motivating image as a universal preference.

Optimize for the user's perceptual goal. Begin with what the user values in the source or dislikes in the render, state it directly, and then translate that judgment into observable causes and prompt controls. Do not let an easy-to-measure detail displace the larger visual proposition.

## Modes and authority

Infer the requested mode from the user's verb:

- **Diagnose:** inspect history, prompts, source/render artifacts, and tests; explain the failure without editing.
- **Design:** propose a general correction and evaluation plan without editing.
- **Apply:** edit the target skill, its source-of-truth resources, tools, and tests when the user explicitly asks to apply, implement, or skillize the improvement.
- **Evaluate:** run static, behavioral, and, when requested and available, rendered-pixel evaluation. Generating images or using paid/external services requires the same authority it would outside this skill.

A diagnosis or review does not authorize edits, renders, publication, or unrelated policy changes. Preserve the target skill's existing purpose and the user's requested output contract.

## Required reading

Always read [references/improvement-method.md](references/improvement-method.md). It contains the causal diagnosis, abstraction, and evaluation method.

For a material revision or persisted evaluation, also read [references/iteration-record.md](references/iteration-record.md). Validate a completed record with:

```bash
python scripts/validate_iteration_record.py ITERATION.json
```

Before changing a target skill:

1. Read its complete `SKILL.md`, repository instructions, and the source modules or references that own the failing behavior.
2. Read its evaluation protocol when one exists. Do not load unrelated routed modules merely because they are nearby.
3. Identify generated or compiled files and their generator. Edit the source of truth first and regenerate derivatives.
4. Inspect relevant history and current tests. Treat historical conclusions as hypotheses until the current artifacts support them.

## Core workflow

### 1. Freeze the baseline and evidence boundary

Record the target skill revision, exact source and render artifacts, authored prompt bytes or hash when available, generator/version, settings, reference handling, and attempt policy. Missing artifacts remain missing; do not reconstruct them from memory.

Tag every material claim as one of:

- source observation
- user judgment
- prompt or skill inspection
- package or behavioral test result
- delivered-render observation or measurement
- generation-system outcome
- hypothesis or unresolved uncertainty

A blocked or absent render is a generation outcome, not pixel evidence.

### 2. Define the perceptual success contract

State the primary visual proposition or appeal before enumerating parts. When the user has said what attracts them or what feels wrong, preserve that language as judgment evidence. If the same aggregate property is independently visible and material in the source, retain it once as a bounded semantic anchor and immediately decompose it into visible causal controls. Decomposition constrains an abstract descriptor; it does not automatically replace or erase its global meaning.

Analyze at three scales:

- **Global:** proposition, dominant fidelity axis, major masses, hierarchy, tonal organization, and fidelity ceiling.
- **Regional:** proportion transitions, surface and material roles, local color/light behavior, topology, and attention.
- **Local:** only details whose failure materially changes the global or regional read.

Separate aesthetic invariants from dimensions that may vary without losing the target. Pose, exact placement, or incidental texture may be flexible even when form, light-to-form behavior, color relation, or hierarchy is invariant.

### 3. Locate the earliest divergence

Trace the chain:

```text
source evidence -> internal representation -> prompt actuation
-> generator and settings -> delivered pixels -> user judgment
```

Classify each mismatch before proposing a fix. Distinguish observation error, representation gap, prompt priority or interaction, generator response, stochastic variation, and external failure. Separate intrinsic form or surface from pose, perspective, illumination, material interaction, exposure, tone mapping, and processing.

### 4. Write falsifiable hypotheses

For each important mismatch, state:

- the suspected failing stage
- supporting evidence identifiers
- the mechanism that could produce the symptom
- what observation would falsify it
- confidence and remaining confounders

Do not infer prompt causality from a render difference alone. Inspect the exact prompt and controls first.

### 5. Generalize before editing

Move up the abstraction ladder:

```text
case symptom -> observable mismatch -> causal mechanism
-> missing representation or ownership rule -> reusable contract
-> deterministic aid or test -> held-out behavior
```

Prefer source-relative axes, relations, effect ownership, confidence, and invariant/flexible distinctions over a desired adjective, coordinate, subject, or numeric value from one case. Treat aggregate language and detailed controls as non-substitutable when both are source-supported: the aggregate retains the perceptual direction, while the decomposition bounds what it means in this image. A current-source descriptor must carry provenance, confidence, P0/P1 priority, a material-drift omission counterfactual, compatibility where applicable, and immediate literal decomposition. Generator/version calibration measures effectiveness; it is not the sole permission to state visible evidence.

Choose the narrowest correct layer:

- `SKILL.md` for shared purpose, routing, authority, and non-obvious invariants
- a routed module for conditional domain behavior
- a reference for substantial analysis or evaluation methods
- a versioned policy for controlled vocabularies or mappings
- a script for repeated deterministic transformation or validation
- tests and regression fixtures for motivating-case literals and expected behavior

Prefer replacing a faulty merge, attribution, or priority rule over accumulating counter-rules or negative prompt terms.

### 6. Implement the smallest coherent change

Keep case-specific nouns, pixels, preferred defaults, coordinates, and measurements out of runtime instructions. Store motivating literals only in clearly marked regression fixtures when they are useful evidence. A general rule allowing the analyst to retain whichever abstract descriptor the current source supports is not a case-specific default.

When a change introduces a structured intermediate representation, ensure its fields have single owners and that the final prompt contains the literal controls needed to actuate the representation. Diagnostic ledgers and abstract labels are not automatically generator controls.

Update source files, regenerate derived artifacts, and add behavior tests that exercise the new decision rather than merely matching headings or wording.

### 7. Evaluate in distinct evidence layers

Report separately:

1. package and structural validity
2. prompt-level behavior
3. generation delivery or blocking
4. rendered-pixel fidelity
5. user judgment

Use unrelated held-out cases and causal pairs where the changed rule is material. Include an invariant-preserving variation and an aesthetic-changing variation when that distinction is central. Keep before/after arms independent, match generator conditions, freeze each prompt within its arm, and use repeated renders when practical so sampling noise is not mistaken for improvement.

Use an independent evaluator only when it adds material confidence and delegation is available and authorized. Give it the raw task, target skill snapshot, and minimum artifacts; do not reveal the suspected bug or preferred answer.

### 8. Make a bounded decision

Use one decision label:

- `diagnosed`: evidence-backed cause analysis only
- `proposed`: general change designed but not applied
- `implemented`: source and tests changed, without claiming broader behavioral success
- `promote`: claim-scope evidence and unrelated holdouts passed
- `revise`: evidence supports another iteration
- `reject`: the hypothesis or change failed
- `blocked`: required evidence or authority is unavailable

Do not call a structural PASS a pixel PASS. Do not call one successful render universal improvement. User preference remains a separate claim even when technical fidelity improves.

## Anti-overfitting and scope guard

- The motivating case may remain a regression sample, never a runtime default or the sole promotion proof.
- Do not install a preferred subject, anatomy, palette, surface value, lighting direction, contrast level, crop, label, or generator workaround.
- Do not turn one sample's measurement thresholds into a universal taxonomy without independent calibration.
- Do not originate a closed list of preferred appearance, attractiveness, mood, or lighting labels merely to make prompting convenient. Classify observable axes and global gestalt independently. A label may come from the user, a versioned vocabulary, or a provenance-bound current-source observation; retain it only when material and immediately decomposed.
- Do not fix weak positive actuation by stacking synonyms or broad negatives. Repair ownership, strength, ordering, or causal separation.
- Do not add unrelated content, policy, moderation, or safety gates while addressing a fidelity mechanism.
- Preserve unsupported or unavailable evidence as uncertainty rather than filling it with plausible defaults.

## Handoff

Lead with the improvement outcome. Summarize the evolution from symptom to reusable mechanism, list changed files, report each verification layer, and name what remains unproved. If no edits were authorized, stop after the evidence-backed design.
