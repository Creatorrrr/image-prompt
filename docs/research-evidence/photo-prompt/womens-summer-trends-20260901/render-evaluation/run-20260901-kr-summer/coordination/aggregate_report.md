# Korean summer visual-semantics three-arm result

Completed: 2026-09-02 (Asia/Seoul)

## Outcome

| Arm | Complex concept | Pack / prompt / runtime | Pixel result | User judgment |
|---|---|---|---|---|
| Capri | Rain-cleared Seoul rooftop greenhouse at cobalt blue hour | PASS / PASS / PASS | 5/5 PASS | pending |
| Harem | Dawn vinyl market under a concrete rail viaduct after rain | PASS / PASS / PASS | 5/5 PASS | pending |
| Lace trim | Late-night laundromat beside a rain-slick intercity bus terminal | PASS / PASS / PASS | blocked; 5 gates unscored | pending |

The overall render-fidelity decision is `revise`. Both delivered images satisfy every fixed target gate, but the lace arm was blocked at output moderation and returned no pixels. A blocked generation is not a pixel failure and cannot be converted into a PASS by its audited prompt or runtime request.

## Delivered images

- Capri: `capri/generated_capri.png`, 1023×1537, SHA-256 `dd03e2df1921d8cc0d37e3dc4c571c92428de34e34d51ffc356cada24ac2afb3`.
- Harem: `harem/generated.png`, 1024×1536, SHA-256 `5b3ed5999ff7dcb0d71020fe840c51e4a5e7bdd0c1a7fb97c6eaf7c7df6eb7db`.
- Lace trim: no image path or image hash; `lace/generation_outcome.json` records one blocked call and no retry.

## Root pixel reinspection

The coordinator reopened both delivered native images after all independent arms completed. The capri image visibly preserves two trouser legs, paired below-knee calf hems, paired bare ankle gaps, all lower-body landmarks, and the length boundary against Bermuda and ankle crops. The harem image visibly preserves one gathered waist, a roomy seat/crotch, bilateral hip-thigh volume, two gathered ankle cuffs, and the boundary against straight wide, smooth balloon, and low-volume jogger substitutes.

This reinspection was not blind to the arm assignment or subagent verdict. It is a direct pixel corroboration, not a second independent generation. The full gate-by-gate record is in `coordination/root_direct_pixel_review.json`.

## Evidence boundary

The supplied portrait was used only for visible adult appearance cues. No artifact or review asserts identity, same-person status, biometrics, protected traits, health, attractiveness, personality, or nationality. Technical gate qualification also does not establish the requesting user's aesthetic preference, which remains pending.
