# arm-01 action-boundary report

Status: **visual technical qualification PASS; requesting-user judgment pending**.

The seeded concept is one visibly adult woman standing beside a linen-curtained window in a snow-bright apartment bedroom, midway through fastening the upper edge of a moss-green brushed-cotton wrap blouse. Her fingers hold the same left-collarbone boundary that reveals a bounded cream opaque foundation layer. A folded linen scarf on a chair is the sole secondary prop; the camera choice is a 75 mm lens just below eye level.

## Outcome

- Final image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-eunggolsa-independent-v2/arm-01-action-boundary/final.png`
- Native image: 1086 × 1448, SHA-256 `6d98239814914a9abd96df95223f7265224b0960dfec8e4ef9051e64c8eef951`
- Review thumbnail: 288 × 384, SHA-256 `73e43976fbc811c7ed2634e999ca3dc682d8b5a5dd7ab2b0d9e63eb85cccab8b`
- Image tool calls: exactly 1 built-in `image_gen` call; no retry and no fallback
- Candidate pack: exactly 1 successful v6 pack, `e79f7cca07c6441a`
- Cross-arm inputs: none

## Gate result

| Assigned profile | PASS | FAIL | Total |
| --- | ---: | ---: | ---: |
| `adult_everyday_controlled_reveal_moment` | 9 | 0 | 9 |
| `soft_window_private_room_adult_portrait` | 5 | 0 | 5 |
| **Combined** | **14** | **0** | **14** |

No gate was graded partial. The review policy treated every partial, ambiguous, or missing observation as FAIL. Native inspection confirmed hand contact, the attached edge/loop relation, doubled fabric thickness, overlap shadow, fold tension, and gravity. Thumbnail inspection confirmed the adult face and changed boundary as the first two subject-level focal relations while retaining the self-directed action and bedroom context.

## Audit boundaries

- Frozen arm input, source snapshot, skill, registry, indexes, candidate dictionary, and appearance reference all matched their expected SHA-256 values.
- The composed prompt audit passed. Its quality status is `warn` only because 430 words exceed the default 360-word target; required literal evidence raises the effective advisory ceiling to 498 words, and the prompt stays below the 640-word hard maximum.
- The exact runtime prompt, negative bytes, intent-lock hash, effective visual contract, reference path, and reference hash passed the runtime request audit before generation.
- Prompt/runtime PASS was not used as pixel proof. The returned native image and 288 × 384 thumbnail were inspected separately, then all 14 current hard gates were recorded and schema-audited.
- Pixel review is technically qualified with zero schema failures and zero failed gates. `representative_eligible` remains false because no direct requesting-user quality judgment has been received; that is not a pixel-gate failure.

The supplied portrait was used only for visible adult facial proportions, long dark wavy hair, and visible natural skin texture. This arm makes no identity, same-person, biometric, protected-trait, health, attractiveness, personality, occupation, ethnicity, nationality, or relationship inference.
