# Wuxia five-arm independent pixel qualification

## Outcome

The wuxia data and candidate-pack layer passed its validators, all five independent prompt/runtime pipelines passed, and all five one-shot image generations succeeded. Strict pixel qualification is **2/5 scenes**: 20 of 25 individual hard gates passed, but a scene qualifies only when all five of its gates pass. The requesting user's visual preference and acceptance judgment remain pending and separate.

## Experimental controls

- Five independent subagents received separate frozen request envelopes, authorial cores, visual intents, and candidate packs.
- Each arm used the same frozen portrait only as an `appearance_reference`; SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.
- Each arm made exactly one built-in image-generation call. There were no retries and no cross-arm image or prompt inputs.
- Every candidate pack is `photo-candidate-pack/v6` and binds one request-scoped hard profile with exactly five pixel gates.
- Each subagent reviewed its own saved pixels at the prescribed thumbnail/native scales. The coordinator independently inspected all five thumbnails and originals and agrees with every gate result below.
- Partial evidence counts as failure. Prompt audit PASS and runtime audit PASS are not pixel PASS.

## Consolidated result

| Arm | Random complex concept | Bound hard profile | Pack | Prompt / runtime | Pixel gates | Strict result | Failed evidence |
|---|---|---|---|---|---:|---|---|
| 01 | rain-polished rooftop herbal-courier cipher | `wuxia_rooftop_qinggong_traversal` | `596e5bf84da40cad` | PASS / PASS | 5/5 | **PASS** | none |
| 02 | misty bamboo-stream aerial duel | `wuxia_bamboo_forest_aerial_duel` | `d10f0a998fa91d5c` | PASS / PASS | 5/5 | **PASS** | none |
| 03 | snowbound courier-inn jade-tally standoff | `jianghu_inn_identity_standoff` | `2e85c8e8b5dec4ca` | PASS / PASS | 4/5 | **FAIL** | three eyelines do not converge on the tally |
| 04 | canal-market bridge intervention and boat escape | `xia_protective_intervention_event` | `132dce81495a566c` | PASS / PASS | 2/5 | **FAIL** | incomplete three-role framing; threat targets intervener, not courier; interposition line is therefore partial |
| 05 | storm-bright desert biaoju departure | `biaoju_guarded_cargo_departure` | `19c47c76a2417610` | PASS / PASS | 4/5 | **FAIL** | cart, threshold, tracks, and road do not form one continuous route |

## Per-arm coordinator review

### Arm 01 — rooftop herbal cipher: PASS, 5/5

- Multiple tiled roof planes and the alley gap form one route.
- A specific left eave and localized splash own the takeoff.
- The complete adult body occupies the intermediate trajectory; hair and robe lag agree with travel direction.
- A separate right roof supplies a plausible landing zone.
- The combined start–transit–destination evidence reads as a human qinggong crossing, not unsupported flight or a static roof pose.
- Image: `../arm01_rooftop_herbal_cipher/generated.png`; SHA-256: `93a0eb97a1f9eeb4ff68afa12d1abd7ace047325d41ef4bb38c51a5d888e17a8`.

### Arm 02 — bamboo stream duel: PASS, 5/5

- Foreground, midground, and receding bamboo create a legible depth corridor.
- Two complete adults remain separate and anatomically coherent.
- Their paths oppose one another from the left root shelf and right boulder.
- The blades meet at one central spark while both landing/support anchors remain visible.
- The scene reads as a two-person bamboo-owned duel, not a portrait or unanchored levitation tableau.
- Image: `../arm02_bamboo_stream_duel/generated_image.png`; SHA-256: `cd925b268b7290e157b699d0cde7a6b51459b68cea1520a55d898bc78beb898e`.

### Arm 03 — snowbound inn: FAIL, 4/5

- The table, snow-lit entry, and staircase define the required inn structure.
- The lead, stair traveler, and server occupy separate zones; tea service remains intact and the scene has not collapsed into a brawl.
- Failure: the lead watches the server, the stair traveler looks down/forward, and the server watches the kettle. Their attention does not converge on the jade tally, so a single identity-testing relation is not visible.
- Image: `../arm03_snowbound_inn/render.png`; SHA-256: `5b42c7a067babca9cf027f6cb7064df54ccb43b85f31ea49a5f2097126a9a5a9`.

### Arm 04 — market-bridge intervention: FAIL, 2/5

- The weapon contact and courier movement toward the boat produce a delayed-threat/escape-opening consequence, and the event is more than heroic styling.
- Failure: the aggressor is cropped at the frame edge and the courier's extended arm is clipped, so three complete roles are not preserved.
- Failure: the aggressor's body and polearm visibly aim at the central intervener rather than at the courier.
- Failure: because the aggressor-to-courier threat line is absent, the intervener cannot visibly occupy that exact line; proximity alone is insufficient.
- Image: `../arm04_market_bridge_intervention/render_attempt_01.png`; SHA-256: `9fd6a8f38ae4cef60f368ecd07bee802d01fc11a35a538c346a5a46ef7ec98b5`.

### Arm 05 — desert biaoju: FAIL, 4/5

- A fortified loading origin, sealed crates on one cart, and front/rear/flank adult escorts establish guarded commercial cargo rather than a merchant-only caravan or generic wagon.
- Failure: the cart points diagonally toward the viewer while the road bends away to the right; no uninterrupted wheel-and-hoof trace joins the yard threshold, cart, and onward road.
- Image: `../arm05_desert_biaoju/generated_image.png`; SHA-256: `cbee0483139c0b53ffd344b9ae0e30e870528fc013e978554ce3b12c7cb55a76`.

## Appearance-reference boundary

Broad visible cues from the portrait—an adult subject with long near-black wavy center-parted hair and a softly oval facial presentation—remain recognizable to varying degrees across the five renders. Fine facial and eye-color details are less confidently judgeable in wider action scenes. This is an appearance-continuity observation only, not a biometric identity, same-person, ethnicity, nationality, personality, health, or attractiveness claim.

## Data and reproducibility links

- Data/candidate-pack validation: `data_pack_validation.md`.
- Structured qualification result: `qualification_summary.json`.
- Frozen random assignment: `prepack_test_matrix.json`.
- Freeze/correction manifest: `prepack_freeze_manifest.json`.
- Each arm directory preserves its request envelope, authorial core, visual intent, candidate pack, composed prompt, prompt audit, render request, runtime audit, generated image, independent pixel review, run manifest, and append-only ledger.

Optional props and atmosphere made each case deliberately complex, but they were not allowed to substitute for profile-owned event geometry. The absent red umbrella in Arm 02, for example, does not invalidate a 5/5 bamboo-duel result; conversely, attractive décor or signage cannot rescue a failed inn attention relation.
