# LACE independent arm result

- Concept: late-night self-service laundromat beside a rain-slick intercity bus terminal
- Candidate pack: `photo-candidate-pack/v6`, pack `73ae9d32b40fed67`, seed `26090173`
- Applied candidate: `slot:light_type:long_exposure_drag`, transformed into distant amber bus-light trails while the torso remains flash-frozen
- Hard profile: `lace_trim_attached_edge`
- Appearance reference: visible adult appearance cues only; no identity, same-person, biometric, protected-trait, personality, or nationality inference
- Composed audit: PASS; 201 words, with only the non-blocking 180-word concise-target warning
- Runtime audit: PASS; exact prompt, negative string, intent-lock hash, reference path, and reference SHA all bound
- Native image call: one call, BLOCKED at output moderation (`sexual`); no image bytes or local path returned
- Pixel verdict: UNSCORED, because there are no delivered pixels; prompt/runtime PASS is not pixel PASS
- User judgment: PENDING

| Gate | Scale | Status | Reason |
|---|---|---|---|
| `vo_summer_lace_trim_base_material` | thumbnail | unscored | No pixels delivered |
| `vo_summer_lace_trim_narrow_band` | both | unscored | No pixels delivered |
| `vo_summer_lace_trim_openwork_motifs` | native | unscored | No pixels delivered |
| `vo_summer_lace_trim_attachment_and_scallop` | native | unscored | No pixels delivered |
| `vo_summer_lace_trim_not_print_whole_or_detached` | both | unscored | No pixels delivered |

The configured one-call policy was honored; no retry was attempted.
