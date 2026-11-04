# Standalone H-F2 retrieval

`scripts/generate_photo_prompt.py` accepts the original request-envelope and authorial-core input JSON files, creative controls, embodiment review, and a separately authored and sealed slot-expression plan bound to the normalized core and controls. Obtain and author the plan using the same neutral catalog and plan-authoring process as the managed workflow. Do not invent slot goals or use candidate data to draft them.

```sh
python scripts/generate_photo_prompt.py \
  --request-envelope-json request-envelope-input.json \
  --authorial-core-json authorial-core-input.json \
  --creative-controls-json creative-controls.json \
  --embodiment-review-json embodiment-review.json \
  --slot-expression-plan-json slot-plan.json \
  --output-directory new-output-directory
```

The output directory must not already exist. `result.json` contains the H-F2 material, validation context, and their receipts; `raw/` contains the scores required to audit the receipt. Keep these together. The command verifies the configured installed generation and executes its sealed code in its bound local Python environment. Search results are creative reference material; they do not grant native candidate adoption. The command no longer accepts legacy source, retrieval-mode, or native-pack overrides. The prior array of native candidate packs is not returned; consumers must migrate to the H-F2 result contract. Use the managed workflow when continuing to compose and audit an image request.
