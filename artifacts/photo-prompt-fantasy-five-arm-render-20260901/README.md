# Fantasy visual-semantics five-arm render test

This run freezes the user's request, five independently authored baseline prompts, the selected visual-obligation profiles, and the pixel-review gates before any candidate pack is consulted.

- Request SHA-256: `bd1cb8b8164a8bdf10ce9eaf7f4c12d6136e8c135841be4c48af53f054caa882`
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Randomization: deterministic SHA-256-derived shuffle, recorded in `coordinator/selection_manifest.json`
- Reference scope: visible facial appearance, hair, and restrained makeup balance for an original adult fictional woman only; no identity or biometric claim
- Outcome layers: source/index proof, candidate-pack proof, prompt audit, rendered pixels, and user acceptance remain separate

Final result: target-keyword gates passed completely in 2/5 arms; the full 14-gate set passed in 1/5 arms. See `report.md` and `coordinator/final_summary.json`. User judgment remains pending.
