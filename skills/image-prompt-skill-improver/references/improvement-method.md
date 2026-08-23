# Evidence-driven image-prompt skill improvement

Use this method to improve an image-prompt skill from real source/render feedback without turning one successful repair into a universal style preference.

## The reusable evolution pattern

The work that motivated this skill progressed through four changes in reasoning quality:

1. **Inventory became proposition.** Early reconstruction could match clothing, pose, setting, or objects while missing why the image was appealing. Improvement began by naming the primary perceptual proposition, ranking global before regional before local evidence, and separating invariants from flexible pose or placement.
2. **Adjectives became causal axes.** Broad appearance words were not reliable controls. Form was decomposed into proportion, contour, tissue, tension, perspective, and hierarchy. Color was separated into intrinsic surface, illumination, global cast, exposure, tone response, and processing. Lighting was separated into visible result, source geometry, fill, local form contrast, gradient, shadow ownership, material response, and spill.
3. **Labels became summaries, not priors.** Familiar composite labels could communicate an appearance but also bias the analysis toward the examples installed in the skill. The robust direction was axis-first classification, optional external label provenance, compatibility review, literal control emission, and model/version calibration before a label was allowed to influence a production prompt.
4. **A valid prompt became only one evidence layer.** Package validation, routed-plan validation, prompt behavior, generation delivery, pixel fidelity, and user judgment answer different questions. Prompt freezing and independent evaluation made retries comparable; a blocked render remained unscored rather than being misreported as a visual failure.

This is not a fixed sequence of feature additions. It is an abstraction pattern: identify the user's perceptual criterion, find the earliest causal gap, represent it explicitly, actuate it once, and test it outside the motivating case.

## Start with the user's actual criterion

The user is often pointing to a gestalt before they have the technical vocabulary for it. Record the judgment directly and without euphemism. Then ask what visible relationships produce it.

Useful questions include:

- If pose or location changed slightly, what would still have to remain for the image to retain its appeal?
- Which single global change makes the render feel like a different image even though the object inventory matches?
- Which regions carry the proposition, and which merely support it?
- Is the perceived property intrinsic, induced by light or perspective, or produced by capture and processing?

Do not begin with the easiest discrepancy to name. A zipper, edge, or coordinate can be accurate while the overall hierarchy, form, surface, or tone is wrong.

## Build a perceptual contract at three scales

### Global

Record the primary proposition, dominant fidelity axis, major masses, attention order, broad tonal organization, subject/environment balance, and fidelity ceiling. This is where a technically detailed render can still fail aesthetically.

### Regional

Record transitions and relationships: proportion between adjacent forms, contour rhythm, material role, local color relationships, light gradients, topology, negative space, and edge interactions. Regional evidence explains how the global read is built.

### Local

Record a local feature only when changing it would affect the global or regional contract, establish identity or legibility, or diagnose a causal mechanism. Local completeness is not the goal.

For every invariant, record a source observation, causal controls, hierarchy role, and what may vary around it. A flexible dimension is deliberately permitted variation, not missing analysis.

## Find the earliest divergence

Use the earliest stage supported by evidence:

| Stage | Typical evidence | Corrective direction |
|---|---|---|
| Source observation | The source was misread or a confound was ignored | Re-observe, measure comparable regions, state uncertainty |
| Internal representation | The analysis has no field for a decisive relation or causal layer | Add a source-relative axis, relation, owner, or invariant |
| Prompt actuation | The representation exists but is absent, weak, duplicated, contradicted, or ordered too late | Repair literal controls, ownership, strength, and hierarchy |
| Generator response | The exact prompt is sound but the model systematically moves another axis | Calibrate the model/version or change the actuation strategy |
| Sampling | Identical conditions vary across attempts | Repeat without changing prompt bytes; report dispersion |
| External outcome | No image is delivered or the tool fails | Report the outcome separately; do not score pixels |
| User judgment | Technical similarity improves but the valued appeal does not | Revisit the perceptual contract rather than adding detail |

Later-stage symptoms do not prove earlier-stage causes. A dark render can come from intrinsic color wording, illumination wording, exposure, tone mapping, prompt competition, or model response. A different silhouette can come from anatomy wording, pose, perspective, garment pressure, light, or crop.

## Turn a complaint into a falsifiable hypothesis

A useful hypothesis has five parts:

1. **Symptom:** source-relative difference, at the correct scale.
2. **Stage:** earliest likely divergence.
3. **Mechanism:** how that stage could produce the difference.
4. **Evidence:** exact artifacts or observations supporting it.
5. **Falsifier:** a result that would show the hypothesis is wrong.

Weak: `the prompt needs stronger lighting words`.

Stronger: `the prompt names overall brightness but does not independently control bright-plane coverage and local form contrast; if adding independent controls changes neither axis across repeated matched renders, the prompt-actuation hypothesis is weakened`.

The wording in the stronger example illustrates causal structure, not a preferred lighting target.

## Generalize at the mechanism boundary

Use this abstraction ladder:

```text
one render symptom
-> source-relative mismatch
-> causal confounds
-> missing distinction or ownership rule
-> reusable intermediate representation
-> literal prompt actuation
-> behavior and pixel tests
```

Good reusable units include:

- invariant versus flexible dimension
- intrinsic versus induced property
- axis values with confidence and evidence
- relation or topology ownership
- source-relative target strength
- clause ownership and aggregate-effect budgets
- external label provenance and compatibility
- versioned model-response calibration

Poor reusable units include:

- the desired adjective from one image
- a particular person's proportions
- fixed pixel coordinates or sampled values
- one garment, pose, background, or crop
- one generator's undocumented workaround
- a growing blacklist of words that happened to drift once

## Choose the implementation layer

Put a rule where it changes the intended behavior with the least collateral effect:

- **Entrypoint:** shared routing, intent modes, output boundary, or evidence-layer distinctions.
- **Module:** behavior that applies only to a subject, medium, risk, or fidelity facet.
- **Reference:** substantial analysis, evaluation, or model-specific procedure needed conditionally.
- **Policy:** deterministic, versioned vocabulary or mapping whose status and calibration are explicit.
- **Script:** repeated calculation, classification, comparison, or record validation.
- **Test/fixture:** concrete motivating artifacts, counterexamples, and held-out expectations.

If a generated bundle or manifest exists, its source modules are authoritative. Regenerate the bundle and verify source/generated consistency instead of editing both independently.

## Preserve a clean control chain

For every material runtime phrase, be able to answer:

- Which invariant or mismatch does it serve?
- Which causal layer owns it?
- What source evidence supports its direction and strength?
- Does another phrase push the same effect?
- Which unintended axes can it move?
- How will the output be checked?

An internal measurement, category, or summary label does not improve generation until a literal prompt clause actuates it. Conversely, repeating literal synonyms can overweight a single effect even when every phrase is individually correct.

## Design evaluations that can disprove the change

### Static and package layer

Run the target skill's validators, manifests, route checks, generated-file checks, and focused unit tests. These prove internal consistency only.

### Prompt behavior layer

Use source artifacts not used to write the correction. Check semantic ownership, causal separation, source-relative strength, proposition ordering, and fidelity ceiling. Judge behavior, not exact words or headings.

Include causal pairs when relevant:

- same proposition with a flexible dimension changed
- similar inventory with a primary invariant changed
- same intrinsic property under a changed inducing condition
- changed intrinsic property under a comparable inducing condition
- one control axis changed while adjacent axes remain fixed

### Render layer

Match model/version, settings, aspect ratio, reference handling, and attempt policy. Freeze prompts within arms. Compare both thumbnail gestalt and native-scale regions. Use repeat attempts when resources permit, and treat a missing render as unscored.

### User layer

Ask whether the target appeal improved, not only whether named details match. User judgment can reveal that the perceptual contract was wrong even when measurements moved in the expected direction.

## Promotion claims

Match the claim to the evidence:

- Package tests can support `structurally valid`.
- Held-out prompt review can support `prompt behavior improved`.
- Delivered comparisons can support `render fidelity improved for these conditions`.
- User confirmation can support `the intended appeal improved for this user and case`.

Promotion requires claim-scope evidence and at least one unrelated held-out success for behavior or render claims. A single motivating case remains regression evidence. Generator calibration is scoped to the recorded model/version and conditioning path.

## Common failure patterns

- **Detail-first repair:** adds accurate local wording while the global proposition remains wrong. Rebuild the global and regional contract first.
- **Label-first repair:** treats a familiar adjective as ground truth. Classify independent axes first and use a label only as a reviewed summary.
- **Negative accumulation:** adds prohibitions to offset overstrong positive wording. Remove or reassign the positive cause.
- **Prompt-only success claim:** equates route or lint PASS with visual success. Keep evidence layers separate.
- **Single-render causality:** credits the edit for stochastic output. Freeze conditions and repeat or narrow the claim.
- **Case leakage:** moves the motivating subject, values, or coordinates into runtime instructions. Keep them in regression fixtures.
- **Framework growth:** adds a new field or module without an owner, actuator, or test. Every representation must terminate in behavior or be removed.
- **Policy drift:** expands a fidelity repair into unrelated moderation, content, or product policy. Keep the intervention inside the diagnosed mechanism and authorization.
