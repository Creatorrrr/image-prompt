# Authorized Codex source review delegation

The user explicitly authorized gpt-6.1-sol subagents on 2026-10-14. Each worker directly reads source content and judges meanings and slot roles. This is Codex review, not independent human review. Root integrates, validates, and commits; it does not claim to have personally read every worker source.

## Scope and boundaries

- Work only within the absolute ORDER.json ordinal range assigned by root. Stops are exclusive. Do not delegate further.
- Never call Gemini, any API or CLI generation/review model, or local generation/embedding/image models. No network is needed. Use stdlib/native source helpers with API keys absent and OS network denied.
- Read `skills/photo-prompt-image-generator/SKILL.md`, `references/maintenance.md`, this run's `CATALOG.json`, `direct_review.py`, and sample authored decisions. Source/catalog/packet hashes are mechanical bindings, not semantic approval.
- Preserve all concurrent work. Edit only your uniquely named files under `authored/`, your own nonoverlapping `packets/`, and your own `worker-notes/`. Do not edit canonical source, shared helpers, global reports, PROGRESS, decisions/, indexes, or git. Do not register or commit.

## Actual reading and judgements

Prepare complete immutable 250-record packets with direct_review.prepare(start,250). Read them in manageable chunks without truncating meaning fields, conditions, effects, alternatives or complete required reference closure. Exact duplicate strings may be denoted as equal; never hide distinct fields. Packet preparation or displaying a record is not review.

For each candidate write an individually authored meaning, actual kind, corrections (exact pointer/before/after/reason), every justified role with positive source quote and concrete owner/property/dimension, branch-specific actual realization IDs, rejected confusion boundaries, uncertainties and explicit status. Consult the actual role specification; existing slots/tags, labels, negative examples, quota, keyword rules or similarity alone are not positive evidence. Do not mechanically union member roles into profiles or bundles.

Use direct_review.validate_decision to check the explicit authored judgement in memory. Do not call register/verify: root owns global mutations. The existing authored/wire.py only expands explicit authored tuples and is suitable for simple visual_option/base records; do not use its base-only assumptions for profiles, bundles or true alternatives. Follow actual realization helpers and all references in those cases. Do not mass-generate decisions from source keywords, old bindings or metadata; scripts may only serialize actual individual judgements.

Retain intrinsic guards and report necessary native refinements separately. Do not infer image-wide changes from local properties, hidden private intent, actors from equipment, worn accessories from uncarried objects, sexuality from adulthood/material, or background/location/activity from a profession alone. Treat contradictory/empty policy text as diagnostic only with a substantive source-based reason; do not quarantine difficult or unfamiliar records just to finish. Unresolved sources remain explicit pending decisions.

Each 250-record management batch should have a uniquely named authored JSON document and optional explicit-literal authoring script. Also write `worker-notes/<task>-<start>-<stop>.json` containing task_name, agent_id (from your task context if available), model `gpt-6.1-sol`, reasoning_effort `high`, start, stop, packet paths, authored paths, complete_source_read true/false, directly_reviewed_count, unresolved ordinals, and specific qualification issues. Report each finished 250 block to root promptly; continue your assignment. Root binds this metadata and dispatched assignment to the registered rows. Never claim root authorship or independent review.

Example offline wrapper:

```sh
sandbox-exec -p '(version 1)(allow default)(deny network*)' /usr/bin/env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u OPENAI_API_KEY -u ANTHROPIC_API_KEY .venv/bin/python <your-script>
```

R is `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014`. ORDER.json, SOURCE.json.gz and CATALOG.json are immutable. Original total is 18,250; original source SHA is 125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b.
