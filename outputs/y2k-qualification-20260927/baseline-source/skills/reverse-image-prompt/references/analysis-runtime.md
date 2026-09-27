# Analysis runtime and generation binding

Read when configuring an analysis harness or recording execution evidence. The analysis model reads an image and authors text; the downstream image generator produces pixels. Their settings, capability evidence, and identities are separate.

## Configuration ownership

The caller owns the analysis model, reasoning effort, available delegation, tool permissions, and image-input transport. Record only exposed values; use `unknown` or `not-exposed` otherwise. A skill cannot prove which backend ran merely by naming a model. The generator adapter owns supported generation settings; never put analysis model IDs, reasoning settings, telemetry, or internal hashes into `PROMPT:`.

The [OpenAI latest-model guide](https://developers.openai.com/api/docs/guides/latest-model), checked 2026-09-05, currently describes GPT-6 Astra. It recommends auditing conflicting skill instructions, explicitly tuning delegation, and calibrating verification to the task. For a caller actually migrating an API harness, use the current guide for supported parameters; preserve effective reasoning settings and compare results rather than installing one universal effort preset. Tool calling, async operations, and prompt caching are caller capabilities, not instructions to invent settings on an unavailable tool.

## Evidence to retain

For a live test, record:

- Exact source bytes/hash and known dimensions; attached preview dimensions are not a substitute.
- The skill snapshot file manifest and route fingerprint; profile-context reads include source and rendered-view hashes.
- Per-case workspace and context mode (`delegated`, `sequential-fallback`, or `mixed`). A separate folder alone is not independent reasoning; record whether conversation history or earlier results were supplied.
- Exposed analysis model/effort and downstream tool/model separately, or an explicit unavailable value.
- Start/end timestamps and actual route/lane/integration/critic/repair events, report bytes, retry/reroute counts, and prompt hashes. Do not estimate timings from analysis prose.
- Exact generation request, attempted prompt hash, reference handling, supplied settings, response artifact, delivered dimensions, and attempt outcome.

The route's `execution_budget` is a declared limit. The caller must enforce it around scheduling and repairs; route validation alone does not establish observed compliance. Report actual counts beside limits and mark unavailable telemetry as unavailable. Do not claim that this package includes an API scheduler.

## Generation boundary

Follow the user's requested conditioning. For text-only reconstruction, submit the frozen extracted prompt verbatim and no source/reference image. Record tool options as applied, unsupported, auto, or unbound; a prompt suggestion is not an API parameter. An exact size setting is established only by supported tool binding and delivered dimensions. Do not silently switch generators or change prompt bytes after a failure.

Use a bounded attempt policy declared before generation. Record every result, including a block or transport failure. Assess delivered pixels independently of structural validators; a successful tool call does not prove fidelity, and a single attempt cannot establish comparative superiority.
