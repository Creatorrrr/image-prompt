# Arm 3 — upper-lip philtral contour focused render

## Outcome

Technical verdict: **PASS**. All four exact `upper_lip_philtral_contour` render gates coexist in the single saved first-attempt image. No repair render was needed. Facial-appearance resemblance and overall preference remain **pending requesting-user judgment**.

## Selected randomized concept

- Seed: `394414666`
- Selection: `random.Random(seed).randrange(8)`
- Zero-based selected index: `1`
- Concept: a lunar seed-archive conservator pausing during a spectral germination scan in a humid nocturnal conservatory, fully clothed in a high-collared cobalt field coat while holding a luminous seed plate
- Domain: `speculative botanical or scientific close portrait`

The eight independent pre-core candidates and exact selection are preserved in `concept_selection.json`.

## Pack and audit binding

- Candidate-pack contract: `photo-candidate-pack/v6`
- Pack ID: `bc2da31d2a6a73ac`
- Creativity: `0.65`
- Generator-normalized core SHA-256: `253fae362842a9c7495407745c5c81b259c2bbf0347792993108668e5beb367e`
- Generator-normalized intent-lock SHA-256: `51674db17a35d508dc295260cd2b266ca0416a26c4d440bf2588b4653010f637`
- Visual-intent SHA-256: `6b083c3a77d1bfc0546f10ab23552b59b37ef795c9aea8ebbdf928c763db81c0`
- Effective visual-contract SHA-256: `72e6cfacc51e790a3a5ec29d61b9150989e17a88e5dc6b0ec43ad4216a83fdf9`
- Composed audit: `PASS`; quality `WARN` only because three frozen mandatory-intent phrases were preserved by literal free description rather than a retrieved candidate
- Exact runtime-request audit: `PASS`
- Image calls: `1`; repair calls: `0`

The initial pre-core freeze is preserved as `authorial_core.initial_frozen.json`. Before any pack was created, generator schema preflight rejected one ungrounded runtime-only label and two unsupported open-dimension names. Only those metadata entries were removed; the 154-word baseline and substantive semantic fields remained unchanged. Both initial and runtime-valid hashes are recorded in `core_hashes.json`, `hashes.json`, and `provenance.json`.

## Final image

- Path: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260830-body-semantics-focused-3/arm-3-philtral-contour/attempt-1.png`
- SHA-256: `e7b570767d61cdc86f0e3e43655f8a5fc856dea33ab6125834e15a80f13bb999`
- Dimensions: `1122x1402`
- Tool: built-in `image_gen`
- Reference role: facial appearance only

## Exact pixel gates

| Gate | Required scale | Verdict | Direct observation |
|---|---|---|---|
| `vo_philtrum_paired_ridges` | native | PASS | Two shallow raised skin ridges separately flank a continuous midline depression between the nose base and upper lip. |
| `vo_philtrum_upper_lip_arc` | both | PASS | The groove ends at a center dip between two upper-lip peaks; the paired arc remains discernible in the `256x320` whole-frame thumbnail. |
| `vo_philtrum_face_geometry_coherent` | native | PASS | Nose base, philtral planes, vermilion border, lip volume, corners, and surrounding texture join coherently without fusion or broken anatomy. |
| `vo_philtrum_not_makeup_only` | both | PASS | Surface-light relief above the vermilion, not lip color alone, carries the two ridges, groove, and paired edge; thumbnail and native form agree. |

Native full image, whole-frame thumbnail, and supplemental native mouth crop were each viewed directly. The crop supports inspection but does not replace the native and whole-frame thumbnail judgments.

## Boundaries and handoff

- The generated adult subject is fully clothed and the photograph is nonsexual.
- No identity, ethnicity, race, health, beauty-value, or biometric inference was performed.
- Technical pixel qualification does not establish resemblance or user preference.
- No other arm prompt, pack, image, or result was read or used.
- Shared source, tests, and `runs/image_runs.ndjson` were not modified.
- Parent-mergeable single run entry: `image_run_entry.json`
- Independent v2 manifest: `run_manifest.json`
- Complete hash/provenance inventory: `hashes.json` and `provenance.json`

## Limitation

Thumbnail survival was tested at the recorded `256x320` proportional whole-frame scale, not every possible smaller display. The pixel review is direct agent visual evidence, not an independent human or instrument measurement; requesting-user judgment remains pending.
