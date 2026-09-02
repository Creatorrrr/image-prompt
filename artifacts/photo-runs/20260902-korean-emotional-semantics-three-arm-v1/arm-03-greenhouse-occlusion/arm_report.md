# Arm 03 — Greenhouse Occlusion

## Outcome

PASS — the single generated image passed all 5/5 strict visual-obligation gates. Technical pixel qualification is complete; requesting-user aesthetic judgment remains pending.

- Final image: `final.png`
- SHA-256: `4cafa6ec3628e576d45e311f4c5624c26d3488ecda4f27615f51db3b5b0b62a4`
- Dimensions: 1086 × 1448
- Image calls: 1
- Retries: 0
- Fallback provider: not used
- Cross-arm inputs: false

## Reference boundary

The corrected reference path `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg` matched the required SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea` and was inspected before generation. It was attached only as `appearance_reference` for clearly adult facial proportions, long dark wavy hair, and visible natural texture. No identity, same-person, biometric, protected-trait, attractiveness, personality, occupation, ethnicity, nationality, or relationship claim is made.

## Prompt and runtime audit

The agent-authored `photo-composed-prompt/v3` is 360 words and preserves the frozen greenhouse seed-library, storm setting, fern overlap across both eyes and the nose bridge, and unfinished seed-envelope/drawer action. Both required clarifications were applied. The unrelated kuudere-relationship and medium-native-glitch concepts were rejected. All six sampled creative candidates were explicitly rejected, and no optional visual concept was promoted to a hard obligation.

- Composed audit: PASS, 0 blocking failures
- Composed quality: WARN only because the five frozen anchor intents were preserved through literal free description rather than retrieved candidate coverage
- Runtime request audit: PASS
- Exact negative bytes: match
- Reference count and hash: 1, match
- Effective visual-contract SHA-256: `3530b7a7f0e3fc3fd56af779175524b71ac249672c3e20681d9bb0f36a638100`

## Strict pixel gates

| Gate | Result | Direct pixel evidence |
|---|---|---|
| Adult subject readable | PASS | At thumbnail scale, one clearly adult subject remains readable through long hair, both hands, pale clothing, upright posture, and frontal orientation. |
| Eye-and-nose identity zone hidden | PASS | At native and thumbnail scales, one continuous fern overlaps both eyes and the nose bridge while forehead, cheeks, jaw, lips, and hair remain visible around it. |
| Scene-bound contact causes occlusion | PASS | Native pixels show the raised hand pinching the fern stem and holding the frond directly across the face. |
| Unfinished action and setting carry mood | PASS | The other hand holds a blank envelope at the mouth of an open specimen drawer; wet greenhouse panes, hanging plants, and drawer banks identify the setting. |
| Not crop, blur, empty scene, or silhouette | PASS | The full head is in frame, the image is sharp and exposed, and the physical fern—not a capture failure—causes the occlusion. |

Hard score: **5/5 PASS**. Partial or missing evidence would have failed; no gate used partial credit.

The porous fern permits tiny glimpses through leaflet gaps, but its physical overlap across both eyes and the nose bridge is unambiguous at both inspection scales. Drawer-label pseudo-text is a non-blocking synthesis artifact outside the declared gate set.

## Optional staging observations

These are observations, not hard gates and not claims about relationships, purity, body/health, or an actual multi-image sequence.

- Broad first-love nostalgia: partial. Rain, aged drawers, cream fabric, and mixed cool-warm light suggest broad adult nostalgia, but pixels establish no relationship or remembered event.
- Clear-serene: strong. Neutral mouth, relaxed shoulders, restrained palette, and still gesture read calmly at first glance.
- Airy-delicate styling: partial. The light cream blouse, fine fern, and soft hand positions are delicate; dense dark foliage and drawers reduce overall airiness.
- Soft milky grade: partial. Cream and lifted skin tones contribute, but cyan panes, bright lamps, and deep hair shadows preserve stronger contrast.
- Single photodump-member feeling: partial. Vertical compact-camera perspective and rain support it, though the frame remains deliberately composed and polished.

## Provenance and review boundary

`image_runs.ndjson` contains exactly one successful row. `run_manifest.json` records image-call count 1, the source/ref/skill/core/intent hashes, and `cross_arm_inputs_used: false`. `pixel_review.json` was audited successfully with the visual-obligations-capable reviewer: technical qualification is true, failed hard gates and schema failures are empty, and representative eligibility remains false because user aesthetic judgment has not yet been received.

`audit_image_render_review.py` is not applicable because this pack has no `photo-render-repair` contract; the strict visual-obligation review was instead audited by `audit_moe_render_review.py`, which supports non-moe effective visual-obligation gate sets.
