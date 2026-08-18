# Frozen A/B protocol

## Comparison boundary

- Arm A uses `photo-prompt-image-generator` end to end: frozen request envelope and authorial core, one candidate-pack v6, authored composition, composed-prompt audit, runtime-request audit, one built-in image-generation call, and pixel review.
- Arm B must not open or use `photo-prompt-image-generator`, its assets, references, scripts, packs, tests, prior prompts, or Arm A artifacts. It independently writes one prompt from the visual request and makes one built-in image-generation call.
- Both arms use the same attached face image only as a facial-appearance reference.
- Each arm gets one native generation attempt. No retry, fallback, or post-generation edit is allowed in this benchmark.
- The arms use separate context sessions and separate output directories. Neither arm may inspect the other arm before both have finished.
- A single stochastic pair supports a result for this trial only, not a general causal claim about the skill.

## Frozen visual request shared with both arms

Create one photorealistic image of an unmistakably adult woman as a syringe-holding obsessive-romance nurse. Use the attachment only for her facial appearance; clothing, pose, crop, setting, and composition are free. Make the nurse role, syringe, and concept legible in a single image. No text or watermark.

## Frozen 100-point pixel rubric

1. Reference-face appearance fidelity — 20
   - facial structure and overall likeness: 10
   - ash-blonde hair, wispy bangs, gray-brown eyes, pale luminous complexion, soft glossy lips: 10
2. Nurse and syringe legibility — 20
   - unmistakably adult nurse role: 10
   - coherent, clearly held syringe: 10
3. Obsessive-romance character behavior — 30
   - one identifiable adult relationship target or repeated same-target marker: 5
   - concrete target-directed action rather than pose/prop alone: 8
   - outward affect versus possessive-affection leak: 8
   - visible immediate consequence: 5
   - single-frame continuity and narrative readability: 4
4. Photographic, anatomical, and prop coherence — 20
   - face/body/hands: 10
   - syringe, clothing, environment, lighting: 10
5. Composition and concept integration — 10
   - focal hierarchy and thumbnail legibility: 5
   - mood supports the concept without overpowering facial identity: 5

## Review method

- Preserve each prompt and native output before review.
- Create an anonymous A/B mapping only after both renders finish.
- Inspect each image at overview/thumbnail scale and at native detail.
- Score visible pixels only. Prompt contracts and audit PASS are reported separately as process evidence.
