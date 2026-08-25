# Distributed analysis orchestration

Use this contract after facet/module routing and before prompt drafting. Domain evidence still comes from the selected `modules/*.md`; lane files define independent ownership and reporting.

## 1. Choose an analysis profile

Resolve `reverse-image-analysis-route/v2` with `tools/route_resolver.py --analysis-route --analysis-profile PROFILE`.

- `prompt` is the default for an ordinary one-image prompt or diagnosis. It preserves separate lane analysts and an independent critic, but collects only viewer-material evidence.
- `audited` is for actual source/render evaluation, measured fidelity work, skill evaluation, or an explicit request for a full evidence ledger. It retains `reverse-image-analysis-lane-report/v2`, `spatial-orientation/v4`, `human-appearance/v2`, and `reverse-image-analysis-bundle/v2`.

Do not enter `audited` merely because a human, readable face, complicated scene, or routed detail module is present. Escalate only when the task requires audited evidence or the compact profile reports one unresolved P0/P1 conflict that cannot be represented honestly.

Both profiles use the same routed set of three to five material lanes for an ordinary image. `lane.global-composition` is always required. A non-core module that reaches no lane is a visible route failure.

## 2. Run one isolated lane wave

When clean-context delegation is available and permitted, run all required lanes concurrently. Each read-only worker receives only:

- the same source artifact and SHA-256;
- raw request and resolved intent;
- route fingerprint, analysis profile, and execution budget;
- its lane file and complete route-assigned modules; and
- the profile's report schema.

Do not pass another lane's result, a preferred conclusion, previous prompt/render, or draft prose. Workers do not write files, generate, author the final prompt, or delegate again.

If delegation is unavailable, freeze each report before starting the next and mark `sequential-fallback`; do not claim independence. Do not rerun a successful lane to seek more detail. A missing or malformed report may be retried once for that lane only; source/hash mismatch or an actual route gap may restart the affected route once.

## 3. Compact prompt report

In `prompt`, each lane returns `reverse-image-analysis-lane-report/compact-v1`:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/compact-v1",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 16}],
  "primary_read": "one sentence naming what this lane says the viewer must retain",
  "material_findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "viewer_priority": "P0",
      "observation": "source-relative visible result",
      "source_evidence": ["decisive visible cue"],
      "confidence": "medium",
      "change_counterfactual": "what visibly becomes a different image if changed",
      "default_drift_risk": "high",
      "control_requirement": "causal requirement, not final prompt prose",
      "aggregate_descriptor_candidate": {
        "phrase": "optional current-source aggregate reading",
        "candidate_source": {
          "kind": "source-visible-approximation",
          "reference": "current source hash or observation id"
        },
        "confidence": "high",
        "viewer_priority": "P0",
        "omission_counterfactual": "material-drift",
        "decomposition_requirements": ["owned visible control requirement"]
      }
    }
  ],
  "supporting_findings": [],
  "grouped_non_material_topics": [
    {"topics": ["intrinsic-induced-confounds"], "reason": "not viewer-material here"}
  ],
  "uncertainties": [],
  "handoffs": [],
  "conflicts": [],
  "escalation": {"required": false, "reason": ""}
}
```

Use the smallest causally sufficient evidence set. Detail P0 and P1; compress P2 into a mergeable supporting cue; group P3 and other non-material required topics with one evidence-based reason. Do not enumerate hidden, unreadable, or non-material axes merely to complete a checklist. Run a counterfactual only when it decides P0/P1 materiality or resolves a high default-drift risk.

`aggregate_descriptor_candidate` is optional and case-bound. Include it only when the phrase itself carries a P0/P1 gestalt not preserved by detail alone; its decomposition requirements remain separately owned. Never fill it from a preferred vocabulary. Split a compact finding only when two visible results can drift independently and both are P0/P1. Otherwise keep the causal result together. Compact reports do not create exhaustive atomic obligations, full color/light ledgers, `spatial-orientation/v4`, or `human-appearance/v2`.

## 4. Viewer-first integration

The main session integrates by owner key and visible effect, never by concatenating lane prose. Before writing the prompt, assign one cross-lane priority:

- `P0 source signature`: changing it makes a viewer read a materially different image. Put its causal controls first.
- `P1 structural identity`: major subject gestalt, face/form/surface, space, clothing silhouette, pose/action, topology, lighting, color, or capture evidence needed to preserve that signature.
- `P2 supporting`: recognizable but safely compressed into an existing clause or one later cue.
- `P3 incidental`: omit unless the user explicitly asks for it.

Priority is counterfactual and source-specific, not category-specific. Face, skin presentation, room geometry, garment silhouette, pose, camera distance, or any other field can outrank the rest. Conversely, a visible field can remain P2/P3 even when a routed module analyzed it.

For a material human, build only the compact appearance signature needed by the image:

- one non-identifying broad visual generation prior only when source evidence supports it and omission creates high model-default drift;
- decisive local face or body geometry;
- displayed skin value/chroma/undertone/finish only where visibly stable and material;
- hair mass or boundary, expression/gaze, and capture treatment only when they carry P0/P1.

A broad prior never states factual nationality or exact ethnicity and never acts as likeness by itself. Keep it immediately adjacent to source-specific geometry, which remains authoritative. `beautiful`, `attractive`, `model-like`, or a similar aggregate appearance reading may be its own P0/P1 finding when high-confidence current-source evidence and a material-drift omission counterfactual support it. Retain the aggregate once before its decomposition; it cannot replace or override broad appearance, geometry, skin presentation, scale, expression, or capture treatment, and it grants no extra polish.

Draft the prompt from P0 to P2. Give each P0/P1 effect one causal owner and one prompt control, merge compatible P2 evidence into those clauses, and omit P3. Specificity follows viewer impact: do not give a long incidental inventory enough repetition to overpower the source signature.

## 5. Compact independent critic and repair budget

Give one independent read-only critic the source/hash, route, compact reports, priority map, and draft prompt without the main reasoning transcript. It checks only blocking visual failures:

- lost or contradicted P0/P1 evidence;
- a generic attractiveness, mood, or style prior replacing source-specific appearance instead of leading an owned decomposition;
- unsupported broad-person inference;
- source-significant face/skin, space, clothing, pose, topology, light, or color drift;
- a P2/P3 detail outranking a P0/P1 control; or
- a route/source mismatch.

The critic returns `pass`, `targeted-repair`, or `blocked`, with exact affected finding/control IDs. Advisories about P2/P3 completeness do not trigger work. Apply at most one local repair to the named controls; do not rerun successful lanes or restart integration. If one repair cannot resolve a P0/P1 uncertainty without guessing, keep the uncertainty visible in diagnostic mode or tell the user the fidelity limit. Do not iterate toward v2, v3, or v4 merely to make the analysis look complete.

When runtime telemetry is available, the orchestrator records route, lane-wall, integration, critic, and repair durations plus report sizes. Lane workers do not spend analysis time estimating their own timing.

## 6. Audited profile

In `audited`, each lane returns `reverse-image-analysis-lane-report/v2`. Every required topic is individually disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`; each material finding is split into independently drifting atomic visible-result obligations. Integrate them into `reverse-image-analysis-bundle/v2`, dispose every finding and obligation once, bind retained obligations through `source_obligation_ids`, and preserve role and causal ownership.

Use `spatial-orientation/v4` and both human orientation counterfactuals only here. Use `human-appearance/v2` and full Color/Tone or Light/Form ledgers only here or when the user explicitly requests those measured contracts. Existing validators remain authoritative:

```bash
python tools/analysis_bundle.py ANALYSIS_BUNDLE.json
python tools/salience_plan.py PLAN.json --prompt PROMPT.txt
```

The audited critic binds to source, route, reports, obligations, and plan hash. It may request one targeted integration repair and one verification pass. Only a route gap or source-artifact mismatch may rerun an affected lane. If the repair budget is exhausted, report `blocked`; never start an open-ended refinement loop.

## 7. Evidence boundary

Route validity, package validity, lane coverage, prompt behavior, delivered pixels, and user judgment are separate evidence layers. A compact prompt can be useful without claiming audited completeness, and an audited bundle can be valid without proving visual fidelity.
