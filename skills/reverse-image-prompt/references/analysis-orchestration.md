# Distributed analysis orchestration

Use this contract after facet/module routing and before prompt drafting. Domain evidence still comes from the selected `modules/*.md`; lane files define independent ownership and reporting.

## 1. Choose an analysis profile

Resolve `reverse-image-analysis-route/v2` with `tools/route_resolver.py --analysis-route --analysis-profile PROFILE`.

- `prompt` is the default for an ordinary one-image prompt or diagnosis. It preserves separate lane analysts and an independent critic, but collects only viewer-material evidence.
- `audited` is for actual source/render evaluation, measured fidelity work, skill evaluation, or an explicit request for a full evidence ledger. It retains `reverse-image-analysis-lane-report/v2`, `spatial-orientation/v5`, `human-appearance/v3`, and `reverse-image-analysis-bundle/v2`.

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

In `prompt`, each lane returns `reverse-image-analysis-lane-report/compact-v2`:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/compact-v2",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 20}],
  "primary_read": "one sentence naming what this lane says the viewer must retain",
  "material_findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "viewer_priority": "P0",
      "representation": "atomic",
      "observation": "source-relative visible result",
      "source_evidence": ["decisive visible cue"],
      "confidence": "medium",
      "change_counterfactual": "what visibly becomes a different image if changed",
      "default_drift_risk": "high",
      "control_requirement": "causal requirement, not final prompt prose",
      "summary_adequacy": null,
      "aggregate_descriptor_candidate": {
        "phrase": "optional current-source aggregate reading",
        "candidate_source": {
          "kind": "source-visible-approximation",
          "reference": "current source hash or observation id"
        },
        "confidence": "high",
        "viewer_priority": "P0",
        "omission_counterfactual": "material-drift",
        "decomposition_requirements": ["owned visible control requirement"],
        "effect_budget": {
          "intended_dimensions": ["face-form", "hair-boundary"],
          "protected_dimensions": ["identity-context", "pose-occlusion", "capture-treatment"]
        }
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

Set `representation` to `atomic` when the observation is already one independently drifting result. Set it to `macro-summary` when one compact pose, topology, lighting, surface, or capture read compresses several source-visible relations. Every macro summary carries `summary_adequacy.verdict = sufficient | lossy | uncertain`. A sufficient summary has no residuals. A lossy or uncertain summary lists only P0/P1 `at_risk_relations`, each with source-relative subject/region ids, relation kind, visible result, evidence, confidence, control requirement, causal owner lane, and any material dependencies. This is a lightweight loss audit, not an atomic ledger: do not enumerate relations the summary already preserves.

`aggregate_descriptor_candidate` is optional and case-bound. Include it only when the phrase itself carries a P0/P1 gestalt not preserved by detail alone; its decomposition requirements remain separately owned. A human aggregate additionally declares intended and protected dimensions, always protecting identity context. Exact identity context uses a separate provenance-bound integration handoff (`user-supplied` or `trusted-metadata`, external reference, viewer priority, no pixel inference). Never fill either field from a preferred vocabulary. Split a compact finding only when two visible results can drift independently and both are P0/P1. Otherwise keep the causal result together. Compact reports do not create exhaustive atomic obligations, full color/light ledgers, `spatial-orientation/v5`, or `human-appearance/v3`.

After the lane wave, close every structured P0/P1 handoff before integration. A lane-to-lane handoff names its source finding or residual ids, target lane, required routed module, reason, and `route_required: true`. The target lane must be present and the required module must be assigned to it. An absent target or owner is `route-gap`, not an ignorable advisory; use the existing one-reroute budget to refine the facet map, then rerun only the affected route. A provenance note intended only for the integrator sets `route_required: false` and does not invent a lane dependency. When tool execution is available, validate the temporary or persisted set with:

```json
{
  "schema_version": "reverse-image-analysis-compact-set/v2",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "route": {},
  "lane_reports": []
}
```

```bash
python tools/compact_reports.py COMPACT_SET.json
```

The checker validates schema, source/route binding, summary residual shape, module assignment, and handoff closure. It does not validate the visual interpretation.

## 4. Viewer-first integration

The main session integrates by owner key and visible effect, never by concatenating lane prose. Before writing the prompt, assign one cross-lane priority:

- `P0 source signature`: changing it makes a viewer read a materially different image. Put its causal controls first.
- `P1 structural identity`: major subject gestalt, face/form/surface, space, clothing silhouette, pose/action, topology, lighting, color, or capture evidence needed to preserve that signature.
- `P2 supporting`: recognizable but safely compressed into an existing clause or one later cue.
- `P3 incidental`: omit unless the user explicitly asks for it.

Priority is counterfactual and source-specific, not category-specific. Face, skin presentation, room geometry, garment silhouette, pose, camera distance, or any other field can outrank the rest. Conversely, a visible field can remain P2/P3 even when a routed module analyzed it.

For a material human, make four independent, source-prioritized decisions:

- exact identity context only from user/trusted external provenance and only when P0/P1;
- one non-identifying broad person prior only when supported, omission-sensitive, and immediately corrected by decisive geometry;
- displayed skin value/chroma/undertone/finish with its own viewer priority, region, and observation scope;
- one optional person-aesthetic or attractiveness gestalt with intended/protected dimensions and immediate owner-correct decomposition.

Pixels never establish race, ethnicity, nationality, or another protected identity. A broad prior is non-identifying and never acts as likeness by itself; keep it adjacent to authoritative geometry. A person-aesthetic aggregate may emit once when high/medium-confidence P0/P1 evidence and a material-drift omission counterfactual support it. It leads only its declared intended controls and cannot alter protected identity, pose, crop, scale, age presentation, garment coverage, skin/cosmetics, light/color, or capture polish.

Draft the prompt from P0 to P2. Give each P0/P1 effect one causal owner and one prompt control, merge compatible P2 evidence into those clauses, and omit P3. Specificity follows viewer impact: do not give a long incidental inventory enough repetition to overpower the source signature. For a source where pose and illumination jointly determine form, keep this causal order unless the source proposition requires a tighter merge: proposition, camera/crop, macro spatial result, at-risk spatial residuals, pose-bound Light/Form relations, surface or garment response, then background and capture. Later prose must not normalize or symmetrize an earlier source-relative spatial control.

## 5. Compact independent critic and repair budget

Give one independent read-only critic the source/hash, route, compact reports, priority map, and draft prompt without the main reasoning transcript. It checks only blocking visual failures:

- lost or contradicted P0/P1 evidence;
- a generic attractiveness, mood, or style prior replacing source-specific appearance instead of leading an owned decomposition;
- unsupported broad-person inference;
- external identity context inferred from pixels, or appearance wording leaking into a protected dimension;
- source-significant face/skin, space, clothing, pose, topology, light, or color drift;
- a macro summary marked or functioning as sufficient while it hides a decisive source-visible residual relation;
- a P0/P1 handoff whose target lane or required module is absent from the route;
- generic lighting language replacing independently drifting regional Light/Form relations;
- a later clause neutralizing, symmetrizing, or otherwise overriding an earlier pose relation, including alignment-style wording whose implicit affected axes were omitted from the draft's effect audit;
- literal prompt text that leaks internal provenance (`source-relative`, `source-visible`, `source-specific`, `source-supported`, `current-source`) or requires an absent attached/source/reference/input/provided/original image to resolve its target;
- a P2/P3 detail outranking a P0/P1 control; or
- a route/source mismatch.

The critic returns `pass`, `targeted-repair`, or `blocked`, with exact affected finding/control IDs. Advisories about P2/P3 completeness do not trigger work. Apply at most one local repair to the named controls; do not rerun successful lanes or restart integration. If one repair cannot resolve a P0/P1 uncertainty without guessing, keep the uncertainty visible in diagnostic mode or tell the user the fidelity limit. Do not iterate toward v2, v3, or v4 merely to make the analysis look complete.

When runtime telemetry is available, the orchestrator records route, lane-wall, integration, critic, and repair durations plus report sizes. Lane workers do not spend analysis time estimating their own timing.

## 6. Audited profile

In `audited`, each lane returns `reverse-image-analysis-lane-report/v2`. Every required topic is individually disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`; each material finding is split into independently drifting atomic visible-result obligations. Integrate them into `reverse-image-analysis-bundle/v2`, dispose every finding and obligation once, bind retained obligations through `source_obligation_ids`, and preserve role and causal ownership.

Use `spatial-orientation/v5`, isolated per-axis neutralization evidence, exact explicit/implicit spatial prompt-effect audits, and both human orientation counterfactuals only here. The raw-source critic must independently inspect the complete literal spatial clauses for synonymous or implicit axis pulls; declared audit ids alone are not semantic proof. Use `human-appearance/v3` and full Color/Tone or Light/Form ledgers only here or when the user explicitly requests those measured contracts. Existing validators remain authoritative:

```bash
python tools/analysis_bundle.py ANALYSIS_BUNDLE.json
python tools/salience_plan.py PLAN.json --prompt PROMPT.txt
```

The audited critic binds to source, route, reports, obligations, plan hash, and the literal prompt. It reads the prompt once more without the source or analysis context and blocks unresolved external reference language even when every ledger excerpt is present. It may request one targeted integration repair and one verification pass. Only a route gap or source-artifact mismatch may rerun an affected lane. If the repair budget is exhausted, report `blocked`; never start an open-ended refinement loop.

## 7. Evidence boundary

Route validity, package validity, lane coverage, prompt behavior, delivered pixels, and user judgment are separate evidence layers. A compact prompt can be useful without claiming audited completeness, and an audited bundle can be valid without proving visual fidelity.
