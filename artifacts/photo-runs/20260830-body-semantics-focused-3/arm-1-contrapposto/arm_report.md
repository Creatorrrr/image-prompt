# Arm 1 — contrapposto_weight_shift

## Outcome

Technical **FAIL** after the allowed two built-in image renders. The selected final file is `attempt-2.png` (SHA-256 `4ea9a0127e26a31b1bae24c5faf5b0749c7d6193b5103968a4a400e3ae81910a`). Three of the four exact profile gates pass in one image, but `vo_contrapposto_counter_tilt` remains insufficiently readable at thumbnail scale.

## Selected concept and pack

- Seed: `142076113`; Python `random.Random(seed).randrange(8)` selected zero-based index `7`.
- Concept: a night-ferry vehicle-deck loadmaster pauses between numbered lanes during a cargo-securing inspection, marking a checklist as an arriving truck approaches the ramp.
- Domain: industrial or transport operational editorial.
- Final v6 pack ID: `01e98ff747195536`; creativity `0.65`.
- Hard profile: `contrapposto_weight_shift`.
- Composed audit: PASS. Attempt 1 and attempt 2 runtime-input audits: PASS.

## Pixel gates on attempt 2

| Gate | Verdict | Direct observation |
|---|---|---|
| `vo_contrapposto_support_leg` | PASS | The image-left leg forms a nearly straight load column into a planted boot, with the trunk settled over it at thumbnail and native scales. |
| `vo_contrapposto_free_leg` | PASS | The image-right knee is flexed and its boot sits lightly forward across the support leg at both scales. |
| `vo_contrapposto_counter_tilt` | **FAIL** | At 213×320, hair, safety vest, and clipboard mask the landmarks; opposing shoulder and pelvic slopes are not unmistakable, so the silhouette can still read as a generic crossed-leg weight shift. |
| `vo_contrapposto_full_body_read` | PASS | Head, pelvis, both legs, both ankles, and both boots remain visible with floor margin at both scales. |

The first render failed the same counter-tilt gate. The sole targeted repair preserved the three passed gates and asked only for stronger opposed shoulder/pelvis slopes, but the second image did not make that geometry unambiguous. The two images are not combined; all four gates had to coexist in one saved image.

## Reference and judgment boundary

The supplied portrait was attached with role `facial appearance only` and SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`. The report makes no biometric identity, ethnicity, race, or same-person claim. User acceptance of the facial appearance and overall image remains pending.

## Audit notes

The original pre-core meaning and baseline were preserved. A first schema check rejected custom dimension `reference_appearance`; the original file/hash and error were retained, and only the schema label was normalized to supported dimension `reference_use`. A first composed preflight also exposed an underlength hard binding; that failed pack/composed pair was retained and the same meaning was expanded to satisfy the profile's minimum evidence length.

The shared `runs/image_runs.ndjson` was not modified. Parent merge input is `image_run_entry.json`; the independent v2 manifest is `run_manifest.json`.
