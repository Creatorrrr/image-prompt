# Military independent image test A

Completed one native `image_gen` invocation with the exact audited baseline prompt and the supplied face/hair reference. The image is stored at `/Users/chasoik/Projects/image-prompt/generated/photo-runs/military-20261024-a/image.png` (1237 × 1272; 2,200,111 bytes; SHA256 `4e361032e9b59a16573ee7e1ee509940f7349cff85261f62d86da2fcb984f918`). Raw tool JSON, original returned PNG and the byte-identical workspace copy are preserved; the embedded raw-tool PNG was verified equal to the saved image.

The concept is a soldier settling a comrade’s ceremonial shoulder cord before formation. The independent random draw used seed `2526402208739747887`. The core, neutral feature choices, embodiment review and prospective testcase were frozen before candidate access and are unchanged.

## Observed result

The topic is visible: olive ceremonial uniforms, shoulder boards, a waiting formation, flagpole/courtyard and a practical two-person cord adjustment. The main face and dark chin-length bob remain reference guided. The strict whole-scene result is **partial**. The right-hand pinch occurs lower/inside on the upper-chest braid rather than beside the left epaulette. Other meaningful body ownership, reach, light support and visibility checks pass. The image is also framed more tightly than the authored knee-up suggestion.

`visual-review.json` has exactly the derived five embodiment gates: four pass, `embodiment_contact_and_space` fails. `review-audit-result.json` admits the record (`record_valid: true`) and correctly reports `technical_qualification: fail`. This is an accepted failure record, not a successful whole-scene qualification. Requester judgment remains pending.

## Retrieval and source effect

The pinned H-F2 generation is `b89c136eaf8d05128cc10f5d4c01cbfe313a73aad7ecdedae9fc983177b6760a`, with native generation `64d0831bea3f21d4a2ab0e9b8b6a8a11718c34332aca0ea69b6a1943056785a8`. One authored attire-context query plus exact request-topic and baseline queries returned 24 occurrences / 24 distinct sources. All complete source bodies, conditions and effects were reviewed. The comparison includes three complete alternative prompts, with all 24 final decisions recorded as `skip`; native choices are empty. The baseline remains byte-identical to the final/runtime prompt.

**None of the 173 newly registered military CIDs was returned.** Existing related `cand_caede85359805141a4fe4457d4424b58` / `base` appeared in `attire_context` with source SHA `43b4687dc4fb9b519bdcb0b0dd2d486af76c1cb1c31b2c327087388704b34598`; it is an older source, not this integration’s new or reviewed-reuse target. Its full adult/whole-uniform inspection meaning was not adopted. An earlier new-source classification was corrected in the authored audit inputs, with previous versions preserved. There is no evidence from this arm that the new data caused the visible military topic or improved image quality.

## Bindings and evidence

- Core canonical SHA256: `865ae8e4f0f488694931df6548775812a2f14f8866b13dfd145ddfcee36e304c`.
- Intent-lock SHA256: `5ac92707e05357734b87f5582984921350215f366b0318f2f3a3d03ea1295044`.
- Runtime prompt SHA256: `a50d524de4150cbc549bf815cc31622bb2178e4b5fb0a2704358ee32d77ace62`.
- Prospective testcase SHA256: `10ff3f62fc5902d6a9207c5eda1efa79cdd5d86fc543908b2c10ee92b78eeea8`.
- Reference SHA256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.
- Ledger run: `ff34f0c157fce2ef`; exact invocation count 1; no retry or fallback.

The main result is `RESULTS.json`; prospective pixel observations are `testcase-results.json`; full-image artistic observations are `whole-image-observations.json`; source decisions are `source-reviews.json` and `composition-comparison.md`. `image_runs.ndjson`, `run_manifest.json`, the managed execution revisions and raw tool result retain the runtime/recorder binding. `artifact-hashes.json` enumerates every saved file and digest in this arm. Metadata PASS values establish binding and review-record validity, not pixel success or user acceptance.
