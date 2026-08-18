# Blind Pixel Evaluation Protocol

The two candidate images were generated from the same face reference and the same high-level request. Candidate identity, prompt, workflow, and generation metadata are hidden. Inspect the reference and both candidates visually at overview and native detail before scoring.

## Rubric (100 points)

1. Face-reference fidelity — 20
   - Same-person facial resemblance, adult-age continuity, eye shape/spacing, face length, jaw/lower-face width, nose, lips, and pale-blonde framing hair.
2. Yandere concept legibility — 20
   - Tender affection and unsettling possessiveness coexist visibly; neither a generic friendly nurse nor a generic horror villain.
3. Nurse role and syringe readability — 15
   - Medical role is unmistakable; the syringe is visually clear, plausibly held, capped, and non-contact.
4. Character-specific story beat — 10
   - One coherent instant gives the gaze, expression, gesture, and prop a readable relational cause or consequence.
5. Photographic and anatomical coherence — 15
   - Realistic face, hands, syringe geometry, clothing, lighting, depth, and material continuity.
6. Composition and cinematic impact — 10
   - Clear focal hierarchy, useful framing, mood, and visual specificity without clutter.
7. Constraint compliance — 10
   - Clearly adult; new composition; no injection, blood, wound, injury, text, logo, or watermark.

## Decision rules

- Do not inspect prompts, manifests, sibling directories, candidate metadata, or mapping files.
- Score each category with image-grounded evidence and sum exactly to 100.
- Call out hard-constraint failures separately.
- Pick a winner, or a tie if the totals and evidence warrant one.
- State confidence and explain which visible differences actually decided the result.
- One stochastic pair supports only a scoped conclusion for this request.
