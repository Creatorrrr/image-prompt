# Pre-render testcase: ferry fashion portrait, creativity 2

Status: authored expectations only. No image has been generated or evaluated.

Run: e203470ea7f94deea1a67d16a7f3ff78  
Pack: 9af45f92a53633b2  
Prompt SHA-256: aa2253075792b8c97517dfb714ee5724f36e1f81ffae7d19f13e55756c1b787b  
Reference input: the supplied portrait is scoped to visible face and hair guidance only.

## Visual checks for a returned image

1. **Requester meaning:** The output reads as a photographic editorial fashion image with one visible person and clothing as the clear visual focus. It preserves the supplied portrait’s visible face and dark straight hair with a soft fringe. No identity, age, body, or profession inference is made.
2. **Fashion legibility:** A layered outfit with clean lines and one muted accent remains readable as the primary visual subject. The outer cloth responds subtly to the breeze without a specific garment, fiber, seam, or closure being required.
3. **Connected turn:** The person is visibly paused in a three-quarter turn toward the receding pier. Shoulders and hips connect naturally, the glance reads toward the pier, and the moment still feels observed rather than a rigid catalog pose.
4. **Support and balance:** Both shoe soles visibly rest flat on the same ferry deck. The person’s weight is plausibly balanced over both feet, and usable deck remains visible around both contacts. A hidden/off-frame foot or a lifted foot does not pass.
5. **Whole-frame readability:** The full-length frame keeps the visible face, hair, layered clothing outline, both shoes, deck contacts, pier, and open shoreline legible together. The turn must not crop the face or support endpoints.
6. **Source-linked context relation:** The person’s pierward action and the receding pier cue are both visible in the same image; a textual implication without a readable cue does not pass.
7. **Soft-light contribution:** Overcast skylight visibly produces broad gentle transitions across the person and nearby ferry surfaces. The flat shoe/deck contacts remain readable under that light. The narrow warm cabin reflection appears across the windbreak glass and stays subordinate to clothing.
8. **Expression and mood:** A small almost-smile supports the quiet, poised instant between leaving and arriving; the expression does not replace the visible action or clothing focus.

## Failure observations to record

Record partial visibility as a failure of the corresponding joint criterion: face or hair unclear; outfit secondary; shoulders/hips disconnected; gaze detached from the pier; either sole not visibly supported; deck around shoes missing; pier/shoreline unreadable; broad light or support contacts not legible together; or reflection dominating the outfit. Prompt and compose-audit success are not evidence that returned pixels pass these checks.
