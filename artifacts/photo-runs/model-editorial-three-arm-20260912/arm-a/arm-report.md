# Arm A — coastal cape lookbook

Result: the frozen scene renders recognizably, but this arm does **not** qualify the new model/editorial data. Its single actual candidate pack exposed no new `mep_` slot or visual profile and no bundle. The complete frozen pixel testcase also fails because the required localized warm reflection on the garment edge is not clearly visible.

Image: [cape-lookbook.png](generated_images/cape-lookbook.png), 1086 × 1448. SHA-256 `097b76433c3b0616220a5256ef30698e7235e80c745252be93f823dade1cf4ee`.

Native runtime: `image_gen.imagegen`, exactly one call, supplied reference actually attached. The concrete native output was copied into this arm; original retained. No API fallback, quality retry, or other arm inputs. `image-result.json`, `native_tool_arguments.json`, `runtime_request.json`, local `image_runs.ndjson`, and `run_manifest.json` preserve provenance.

## Independent concept and freeze

Seed `4078680847` used Python `random.Random(seed).choice` over independent prepack pools in `random-design.json`. Reserved family was coordinator-owned garment-aware fashion lookbook. Random choices: coastal ferry terminal; burgundy wool cape over tapered trousers; right hand lightly lifting a small outer hem section; cool skylight with small warm side reflection; chrome folding chair. This concept and its choices are agent-owned, not requesting-user definitions. Exact requesting-user envelope bytes and generation-request span were copied and verified before project data access.

The initial English baseline, authorial core v3, embodiment review and observable test criteria were frozen before project references/scripts/assets. See `prepack-checksums.json`. Normalization yields core hash `520acf0230694f2fc814965101efb61d5036b550cf8d5189f87aec9b12055403` and intent-lock hash `af78603f2d04d2bd2cc042302584923d09bc338b909ca116a94c562baf2470b1` in pack `c2a0abee91865d4f`.

## Actual exposure and selection

- New `mep_` slots: **0 exposed, 0 selected**.
- New `mep_` profiles: **0 exposed, 0 selected**.
- Bundles: **0 exposed, 0 selected**.
- Optional visual concepts actually exposed: `deliberate_underarm_salience` and `one_piece_dress_construction`. Both rejected because a low-arm cape over trousers cannot preserve its frozen meaning while adopting either.
- Existing creative candidates selected after complete detail inspection: `slot:subject_framing:full_body_framing` and `slot:composition:strong_leading_lines_vanish`. They became a grounded portrait crop and receding terminal-window rhythm. Other creative suggestions were rejected.

`exposure-selection.json` records this failure. There is no effective visual-obligation hash. No selected optional profile was silently credited. The focal garment-aware keyword has no typed assertion or selected hard profile in this run; its frozen supplemental testcase remains agent review, a workflow coverage gap. The machine PASS must not be presented as comprehensive focal coverage.

## Audit and pixel results

Composed audit: PASS, four warnings about baseline anchor coverage through free description. Runtime exact-input audit: PASS, exact reference hash verified. These preflight results do not establish image fidelity.

The image was reviewed as a full frame and at its native original resolution. The exact derived gate set is five embodiment gates; all five pass in `pixel-review.json`. The review audit validates the record with `technical_qualified: true`, `representative_eligible: false`, and user judgment pending (exit 1 reflects pending representative promotion).

| Frozen pixel criterion | Result | Observation |
| --- | --- | --- |
| Garment construction and color | PASS | Burgundy textured wool cape, shaped shoulder seam, curved hem, charcoal tapered trousers and black boots are readable. |
| Garment-aware presentation | PASS | Cape dominates frame; garment front and falling cloth remain inspectable. |
| Hem pinch | PASS | Her right thumb/index on screen left pinch a small hem section; the fold falls back toward her thigh. |
| Body and contact | PASS | Coherent forearm-to-hand chains through side openings; both soles grounded; chair clear of boots. |
| Ferry terminal setting | PASS | Terminal windows, sea, coast, ferry and departure sign visibly support the location. |
| Cool skylight plus warm garment-edge reflection | **FAIL** | Cool illumination and warm floor/wall accents are visible, but the required localized warm reflection does not clearly belong to a garment edge. Background warmth cannot substitute. |
| Reference face and hair | PASS | Dark wavy hair, eye appearance, oval face and lip proportions visually correspond to supplied portrait. This does not authenticate identity. |

Every required test component must coexist: `partial_is_fail`. Overall frozen testcase: **FAIL**. New model/editorial data qualification: **FAIL at exposure / not exercised in pixels**. No causal improvement over an old-data control can be claimed. User judgment remains `not_yet_received`.
