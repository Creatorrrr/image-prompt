# Analysis runtime and generation binding

Read before delegating analysis tasks, configuring an analysis harness, or recording execution evidence. The analysis model reads an image and authors text; the downstream image generator produces pixels. Their settings, capability evidence, and identities are separate.

## Configuration ownership

The caller owns the analysis model, available delegation, tool permissions, and image-input transport, and applies the task-adaptive reasoning-effort policy below. An explicit user effort request takes precedence within its stated scope; the parent's configured effort alone is not such a request. Record only exposed values; use `unknown` or `not-exposed` otherwise. A skill cannot prove which backend ran merely by naming a model. The generator adapter owns supported generation settings; never put analysis model IDs, reasoning settings, telemetry, or internal hashes into `PROMPT:`.

For an API-harness migration, consult the current [OpenAI latest-model guide](https://developers.openai.com/api/docs/guides/latest-model) for supported parameters and compare results under matched effective settings. Tool calling, async operations, and prompt caching are caller capabilities, not instructions to invent settings on an unavailable tool.

## Task-adaptive effort policy

`reverse-image-analysis-effort/v1` chooses effort separately for each lane, critic, and any authorized delegated repair. Select the smallest level that can complete that task's required evidence and checks:

| Task level | Selected effort | Work that justifies it |
|---|---|---|
| Routine | `low` | Narrow mechanical or format checks, or one unambiguous visible fact without material interpretation or interacting constraints. |
| Standard | `medium` | Ordinary compact visual analysis, source-relative evidence selection, or a compact critic for a straightforward route. |
| Complex | `high` | Material topology/occlusion or mixed-medium interpretation, multiple interacting fidelity risks, or complete audited obligations and source/ledger reconciliation. |
| Exceptional | `xhigh` | A specific unresolved P0/P1 causal conflict or coupled constraint that the affected task must reconcile and that `high` cannot adequately cover. |

Do not select `max` automatically. Use it only for an explicit user request that applies to that task. A human, readable face, long report, many lanes, or parent set to `max` does not by itself justify escalation. `prompt` and `audited` govern evidence scope; effort does not change the selected profile, lane count, coverage, or retry/repair limits.

`tools/route_resolver.py --analysis-route` supplies `reasoning_effort` and `effort_rationale` for every lane and the critic. Its route-based defaults are `medium` for standard compact tasks, `high` for materially specialized scope or audited work, and a critic selected from the actual review burden. The router does not inspect pixels or claim these defaults are empirically optimal. Before dispatch, the caller assesses the exact task against the source and table; a routine task may use `low`, and only an evidenced exceptional task may use `xhigh`. Record any adjustment and its task-local reason separately from the immutable route. Recompute for the critic's actual draft/reports, an allowed affected-lane reroute, or a targeted repair; do not raise unaffected or successful tasks.

When the delegation tool exposes an effort parameter, pass the selected value explicitly. With Codex `spawn_agent`, pass `reasoning_effort` and `fork_turns="none"`, then supply only the clean-context inputs allowed by the orchestration contract. A prose instruction inside the worker message does not bind runtime effort, and omitting the parameter can inherit the parent's setting. Keep the inherited model unless the user or applicable instructions request a model change. Do not use a full-history fork to get around clean-context isolation or an effort override restriction.

Bind only effort values supported by the actual tool/model. For automatic selection, use the selected level if supported; otherwise use the next higher supported level up to `xhigh`. If none is available, use the highest supported lower level and disclose the limitation. Never fall back silently to `max` or pretend an unsupported user-requested value was applied. If effort is not controllable, record `not-exposed` or `unsupported`; keep declared selection separate from effective execution. Sequential fallback cannot change the already running parent's effort and must disclose that boundary.

An effort increase does not authorize another lane wave, critic, or repair. Adjust only a call already allowed by the execution budget; report unresolved P0/P1 limits when no authorized call remains. Validate selection/dispatch separately from image fidelity and measure any latency or quality benefit before claiming it.

## Evidence to retain

For a live test, record:

- Exact source bytes/hash and known dimensions; attached preview dimensions are not a substitute.
- The skill snapshot file manifest and route fingerprint; profile-context reads include source and rendered-view hashes.
- Per-case workspace and context mode (`delegated`, `sequential-fallback`, or `mixed`). A separate folder alone is not independent reasoning; record whether conversation history or earlier results were supplied.
- Per-task selected/requested effort, selection reason, exposed applied effort/model, any user override or supported-value fallback, and downstream tool/model separately. Mark unavailable applied values explicitly; a selected value or submitted argument alone is not backend confirmation.
- Start/end timestamps and actual route/lane/integration/critic/repair events, report bytes, retry/reroute counts, and prompt hashes. Do not estimate timings from analysis prose.
- Exact generation request, attempted prompt hash, reference handling, supplied settings, response artifact, delivered dimensions, and attempt outcome.

The route's `execution_budget` is a declared limit. The caller must enforce it around scheduling and repairs; route validation alone does not establish observed compliance. Report actual counts beside limits and mark unavailable telemetry as unavailable. Do not claim that this package includes an API scheduler.

## Generation boundary

Follow the user's requested conditioning. For text-only reconstruction, submit the frozen extracted prompt verbatim and no source/reference image. Record tool options as applied, unsupported, auto, or unbound; a prompt suggestion is not an API parameter. An exact size setting is established only by supported tool binding and delivered dimensions. Do not silently switch generators or change prompt bytes after a failure.

Use a bounded attempt policy declared before generation. Record every result, including a block or transport failure. Assess delivered pixels independently of structural validators; a successful tool call does not prove fidelity, and a single attempt cannot establish comparative superiority.
