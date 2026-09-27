# Independent arm A result

Concept: heritage-exhibition print installation in an art deco tram depot at rainy blue hour (seed 287413). One v6 candidate pack and one native image_gen call; the portrait was inspected and actually attached as visible face/hair appearance guidance only.

The native 1024×1536 image was retained byte-identically as `generated_images/tram-depot-hosiery.png`. Its SHA-256 is `5d315d30640ff388234f02504ca68eaabbbee728b2e97d6deb97bf718130bc0f`. The same image was reviewed at native and 256×384 thumbnail scale.

| Frozen target | Actual pixels |
|---|---|
| Mini skirt exterior silhouette | PASS |
| Both bare-thigh intervals between hem and above-knee stocking top | PASS |
| Continuous sheer hosiery with transmitted skin tone | PASS |
| Directional hosiery surface sheen | FAIL — mostly matte, ambiguous sheen at thumbnail |

The pack exposed and the composer fully opted into `pfe_hosiery_sheen`, `pfe_hosiery_sheer`, and `pfe_thigh_skin_band`. No new-family wardrobe slot candidates or bundles were exposed. The mini-skirt exterior profile was absent; its independently frozen manual target passed, but no absent candidate was injected and no absent-profile adoption is claimed.

Pre-core selection, composed prompt, and exact runtime audits passed. Composed audit retained four informational warnings that the mandatory intent is covered by authored prose. The render-review record has no schema failures, but technical qualification is `failed_technical_hard_gates`: sheen gates 1 and 2 fail, and the exact left-upper/right-lower frame grip is reversed. The other 11 of 14 derived gates pass.

The additional manual common review also records an open upper blouse collar and wet-looking interior aisle instead of the authored fully buttoned blouse and dry floor. Both feet and the frame bottom remain visibly supported. Full-body coverage, face/hair guidance and architecture are legible. These are independent agent judgments, not requester acceptance.

See `render_review.json` and `render_review_audit.json` for the exact derived gate set, `target_review.json` for the frozen manual target/common gates, and `candidate_exposure_adoption.json` for honest discovery/adoption boundaries. `run_manifest.json` and `runs/image_runs.ndjson` record actual call count 1. No retry, CLI fallback, sibling inputs, shared-ledger writes, or production-source modifications were made. All 97 source snapshot hashes and all pre-render artifact hashes remain unchanged.
