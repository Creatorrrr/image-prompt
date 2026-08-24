# Distributed analysis orchestration

Use this contract after facet/module routing and before the salience plan. The existing `modules/*.md` files remain the only domain-analysis source of truth; lane files own separation of responsibility, inputs, outputs, and completion gates.

## 1. Build the route

Resolve modules first, then produce `reverse-image-analysis-route/v1` with `tools/route_resolver.py --analysis-route`. Routing is shallow: it selects analysis lanes but does not make visual conclusions. A non-core module that reaches no lane is a visible route failure.

Use three to five material lanes for an ordinary image; do not create one worker per module. `lane.global-composition` is always required. Other lanes activate from the selected modules.

## 2. Isolate lane analysis

When the host supports delegation and the user permits it, run all required lanes concurrently in separate clean contexts. Each worker is read-only and receives only:

- the exact same source bytes or accessible artifact plus SHA-256;
- the raw user request and resolved intent mode;
- the route fingerprint;
- its complete lane file;
- its route-assigned modules, including required common modules; and
- the `reverse-image-analysis-lane-report/v1` schema below.

Do not pass another lane's report, an expected conclusion, a failure diagnosis, a prior prompt/render, a preferred label, or main-session draft prose. A worker must not edit the skill, author the final prompt, generate an image, or delegate again.

If delegation is unavailable, process the same lanes sequentially into the same report schema. Finish and freeze each report before starting the next; do not feed earlier conclusions forward. Mark `execution.mode=sequential-fallback` and every report `independent_context=false`. This preserves coverage, not independence.

## 3. Lane report schema

Each lane returns one compact JSON object:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/v1",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 15}],
  "topic_dispositions": [
    {"topic": "appearance-drift-risk", "disposition": "analyzed", "finding_ids": ["lane.subject-appearance:f1"], "reason": ""}
  ],
  "findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "scale": "regional",
      "axis": "form",
      "observation": "source-relative observation",
      "source_evidence": ["visible cue"],
      "confidence": "medium",
      "causal_origin": "intrinsic",
      "materiality": "material",
      "proposed_role": "primary",
      "default_drift_risk": "high",
      "confounders": []
    }
  ],
  "control_requirements": [],
  "omission_checks": [],
  "handoffs": [],
  "conflicts": []
}
```

Every required topic is disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`. Findings use source-relative observations, not final prompt excerpts. There is no fixed finding count. Human appearance findings are non-identifying generation approximations; factual identity or nationality requires user/trusted metadata outside image inference.

## 4. Integrate by owner key

The main session combines reports into one `reverse-image-analysis-bundle/v1`; it does not concatenate their prose. Merge by `owner_key`, semantic axis, region/subject, causal owner, direction, and role. Keep one final invariant/control owner per material effect.

Every finding is disposed exactly once as `retained`, `merged`, `diagnostic-only`, `rejected`, or `uncertain`. `rejected` and `uncertain` require reasons. A material primary finding may not be dropped or demoted; it must reach a primary final invariant, or integration remains incomplete. Embed the reconciled plan as `integrated_plan.payload` and record the SHA-256 of its canonical JSON as `integrated_plan.sha256`. Every retained or merged `final_invariant_id` and `final_role` must exist unchanged in that hash-bound plan.

Treat these as material conflicts: opposite directions for one owner key; competing causal owners for one effect; primary-to-supporting demotion; intrinsic-versus-induced attribution disagreement; or a broad label that adds unsupported content. Resolve obvious duplicates and lane ownership mechanically. Send only the unresolved issue and source evidence to a separate clean-context adjudicator. Do not vote; preserve `uncertain` when evidence does not decide.

## 5. Independent coverage review

After integration, give an independent read-only critic the raw request, exact source/hash, route, compact reports, and integrated plan—without the main reasoning transcript. The critic reports only `route-gap`, `topic-gap`, `merge-loss`, `unsupported-addition`, `ownership-conflict`, `role-strength-drift`, `scope-leakage`, or `unresolved-uncertainty`.

The critic binds its report to the same source SHA-256, route fingerprint, and integrated-plan SHA-256 and lists every reviewed finding and plan-invariant ID. It returns `pass`, `revise-route`, `revise-integration`, or `blocked`; it neither edits the plan nor writes prompt prose. Do not freeze the prompt before an independent critic returns `pass`, including under sequential fallback. A `revise-route` result adds the missing lane and reruns it; `revise-integration` repeats the merge. Persist route, reports, adjudications, critic result, plan, and prompt as distinct evidence when generation or evaluation is requested.

## 6. Validation and evidence boundary

Validate the bundle with `tools/analysis_bundle.py`. The validator proves route/report coverage, source/route/plan hashes, finding-to-plan invariant binding, independence claims, role continuity, conflict adjudication, and critic gating. Validate the embedded plan separately with `tools/salience_plan.py`; the bundle checker does not prove either plan semantics or visual correctness. Package validity, lane coverage, salience-plan validity, prompt fidelity, delivered pixels, and user judgment remain separate evidence layers.
