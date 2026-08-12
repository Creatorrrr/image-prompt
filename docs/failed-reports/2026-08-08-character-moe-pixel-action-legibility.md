# Character-moe prompt contracts passed while two pixel actions remained ambiguous

- Recorded: 2026-08-08 03:23 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Moe and Subculture Character Grammar / Stage 5
- Affected scope: frozen eight-family render holdout, direct `--scene-function` selection, transformation dual identity, adult competence-with-care
- Search terms: character moe pixel action legibility, transformation gear ambiguity, simultaneous care action, scene function CLI
- Related paths: `tests/fixtures/photo_prompt/render_character_moe_quality_holdout_v1.jsonl`, `skills/photo-prompt-image-generator/assets/photo_prompt_scene_expression_character_moe.json`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `generated_images/character-moe-8-family-validation-20260808_030639`

## Failure

- Conditions or trigger: Generate the eight implementation-before frozen family cases through direct rule-mode presets, exact requested scene functions, candidate-pack composition audit, built-in image generation, and prompt-metadata-free pixel inspection.
- Expected: Every case visibly carries its target character mechanism and directed action without relying on the prompt or result metadata.
- Observed: The initial CLI rejected all eight newly authored target scene functions because it validated only the legacy facet vocabulary. After that loader defect was fixed, the hair-state scene still described a bicycle courier instead of the frozen mountain-rescue subject. Six corrected cases passed, but the first transformation render read as an ordinary firefighter repairing workwear rather than a civilian/transformed dual identity. The first adult-inclusive render placed water and headphones in the coworker's hands while the technician worked; its allowed edit made the handoff clear but removed simultaneous console operation.
- Impact on the goal: Prompt audit PASS was insufficient for two of eight pixel mechanisms. Stage 5 and the goal remain incomplete until revised implementation wording produces direct visual evidence in a bounded new qualification.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: direct wrapper packs with seeds `880801` through `880808`, requested scene functions from the frozen holdout, and original-resolution inspection of `generated_images/character-moe-8-family-validation-20260808_030639/*/final.png`.
- Result: CLI allowlist failed closed before rendering; the fixed structural test later passed all eight exact selections. Pixel results are preserved in `07-transformation/result.json` as `pass_with_limitations` and in `08-adult-inclusive/result.json` as `fail`; root review treats both as pre-fix failures.

## Cause assessment

- Confirmed cause or current hypothesis: The CLI's global allowlist was not derived from authored render blueprints. Separately, the first transformation atom used only generic protective workwear and the adult-care atom requested two objects plus console repair without fixing hand direction, so the image model could satisfy the nouns while losing the mechanism.
- Confidence: confirmed for CLI and action wording; high for pixel realization.
- Remaining unknowns: Whether one simplified revised atom per failed family will remain legible in a single bounded render without converging on a franchise costume or sacrificing the simultaneous action.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Legacy `facet_vocab.scene_function` CLI validation | Rejected the new frozen functions | Authored blueprint functions were never added to the runtime allowlist |
| First transformation image plus one targeted edit | Repair and burden were clear | The garment still read as ordinary emergency-service equipment; edit budget was exhausted |
| First adult-inclusive image | Console competence was clear | Care direction existed only as an inferred completed handoff |
| One adult-inclusive targeted edit | Water/headphone handoff became clear | The edit removed the technician's console-operating hand, so the two actions no longer coexisted |

## Resolution or next safe step

- Resolution: CLI-valid functions are now derived from all resolved authored blueprints and wrapper selection is asserted for all eight frozen cases. The hair scene matches the frozen rescue context. The transformation atom separates ordinary clothes from an original transformed-state overlayer with a restrained non-symbolic inner-seam material effect. The competence-with-care atom fixes one hand on exposed reset controls, the other extending water, with headphones already within the coworker's reach.
- Verification: Both pre-fix failures remain preserved. Each revised implementation received exactly one new pristine candidate pack, audited prompt, and built-in initial image with no edit. Root original-resolution review passed the transformed-state/civilian separation, repair burden, and ordinary pager conflict in `07-transformation-revision/final.png`; it also passed simultaneous reset-control operation, directed water handoff, and reachable headphones in `08-adult-inclusive-revision/final.png`. Both audits report status/quality PASS and empty failures/warnings.
- Next safe step if unresolved: Stop after the second implementation repair, leave the report active, and do not weaken the frozen pixel criteria or select among multiple successful-looking renders.

## Reuse guidance

- Avoid: Treating prompt audit, object presence, or a post-hoc narrative as proof that a directed or simultaneous character action is visible.
- Prefer: Freeze the actor, hand direction, shared target, and one materially distinctive genre cue in the atomic scene; then inspect pixels without prompt metadata.
- Applicable when: A character mechanism depends on two actions by the same subject, dual identity, handoff direction, or a genre state that ordinary workwear can mimic.
- Re-check when: Scene-function vocabularies, atomic actions, or image-model behavior changes.
