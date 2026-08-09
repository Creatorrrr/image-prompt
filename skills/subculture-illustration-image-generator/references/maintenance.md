# Illustration Skill Maintenance

## Keep Research and Runtime Separate

- Store citations, limitations, and provenance in `assets/research_evidence_illustration/`.
- Store only abstract visual/router/guard nodes and evidence IDs in the runtime graph.
- Never copy source prose, actual artist names, studio names, protected titles, or franchise designs into prompt candidates.
- Use only `source_supported`, `cross_source_synthesis`, and `design_inference`. Cross-source synthesis requires two independent source records; the topic matrix does not count as a source.

## Validate Before Use

Run:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py
```

The validator must cover research references, typed node roles, compatibility, route/format coverage, the typed image-generation retry policy, frozen holdouts, protected-name boundaries, current v2 prompt qualification, the generation-free case-01 v2 preflight and approval boundary, and explicit legacy replay of immutable v1 prompt/render evidence. It is not a pixel evaluator.

Read top-level `status` as validator execution/integrity only. Read `product_qualification_status` for the actual aggregate qualification; it remains `partial` while any required render case lacks a qualified final image.

## Preserve the Photo Boundary

The illustration skill must not import photo generator modules, load photo tags or quality layers, or regenerate the photo semantic index. Re-run the frozen photo baseline after changes. Only the photo skill's descriptive sibling-routing text may change in this goal.

## Change Discipline

- Freeze new natural-language and render expectations before adding routes.
- Prefer a shared mechanism family and typed compatibility over flat presets.
- Keep one primary plus at most two supports.
- Add a node only when it produces observable evidence that an existing node cannot express.
- Record material research, routing, audit, or pixel failures before retrying. Do not lower a gate to accept a failed image.
- Add a new qualification version when a pack or composed contract changes. Never mutate a historical pack, composed prompt, audit, result, image, or its recorded hash to make it satisfy a newer contract.
