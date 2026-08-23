# Improvement iteration record

Persist this record for material skill revisions, before/after evaluations, or any claim that an observed failure has been generalized. It keeps source evidence, hypotheses, implementation, and promotion claims auditable without requiring the motivating artifact to enter runtime instructions.

The validator checks evidence references and claim-scope gates. It cannot decide whether an image was interpreted correctly or whether the implemented rule is genuinely general.

## Minimal shape

```json
{
  "schema_version": "image-prompt-skill-improvement/v1",
  "target": {
    "skill_path": "<path>",
    "baseline_revision": "<commit-hash-tag-or-snapshot-id>",
    "candidate_revision": "<commit-hash-tag-working-tree-or-null>"
  },
  "goal": {
    "claim_scope": "structural | prompt-behavior | render-fidelity | user-aesthetic",
    "request": "<what the user asked to improve>"
  },
  "evidence": [
    {
      "id": "e-source",
      "kind": "source-observation",
      "claim": "<source-relative observation>",
      "artifact": "<path hash command result or conversation reference>"
    }
  ],
  "perceptual_contract": {
    "primary_success_condition": "<the proposition that must survive>",
    "user_appeal": "<direct user judgment or null>",
    "invariants": [
      {
        "id": "invariant-id",
        "statement": "<source-relative invariant>",
        "evidence_ids": ["e-source"],
        "causal_controls": ["<observable control axis or relation>"]
      }
    ],
    "flexible_dimensions": ["<dimension allowed to vary>"]
  },
  "mismatches": [
    {
      "id": "mismatch-id",
      "scale": "global | regional | local",
      "axis": "<visual axis>",
      "source_state": "<source-visible state>",
      "render_state": "<delivered-render state or unavailable>",
      "evidence_ids": ["e-source"]
    }
  ],
  "hypotheses": [
    {
      "id": "hypothesis-id",
      "stage": "observation | representation | prompt-priority | prompt-interaction | generator-response | sampling | external | user-contract",
      "statement": "<causal hypothesis>",
      "evidence_ids": ["e-source"],
      "falsifier": "<what result would weaken or disprove it>"
    }
  ],
  "intervention": {
    "status": "none | proposed | implemented",
    "target_layers": ["entrypoint | module | reference | policy | tool | test"],
    "general_rule": "<case-independent correction>",
    "generalization_basis": "<why it should transfer>",
    "hypothesis_ids": ["hypothesis-id"],
    "changed_paths": [],
    "case_specific_runtime_defaults": []
  },
  "evaluation": {
    "package": {"status": "not-run", "evidence_ids": []},
    "prompt": {"status": "not-run", "evidence_ids": []},
    "render": {"status": "unscored", "evidence_ids": []},
    "user": {"status": "unscored", "evidence_ids": []},
    "holdouts": []
  },
  "decision": {
    "status": "diagnosed | proposed | implemented | promote | revise | reject | blocked",
    "claim_scope": "structural | prompt-behavior | render-fidelity | user-aesthetic",
    "rationale": "<bounded conclusion>",
    "evidence_ids": ["e-source"]
  }
}
```

## Evidence kinds

- `source-observation`
- `user-judgment`
- `prompt-inspection`
- `prompt-evaluation`
- `package-check`
- `render-observation`
- `generation-outcome`
- `repository-history`
- `measurement`
- `external-research`

Use `render-observation` only when pixels were delivered and inspected. Use `generation-outcome` for a block, timeout, empty result, or transport failure.

## Holdout rows

Each holdout row has this shape:

```json
{
  "id": "holdout-id",
  "case_role": "motivating | held-out",
  "status": "pass | fail | blocked | unscored",
  "covered_axes": ["<axis or relation exercised>"],
  "evidence_ids": ["<evidence-id>"]
}
```

The current case is `motivating`. A behavior, render, or user-aesthetic promotion needs at least one passing `held-out` row. Choose unrelated cases and causal variations rather than cosmetic copies.

## Evaluation semantics

- `package` PASS/FAIL cites `package-check` evidence.
- `prompt` PASS/FAIL cites `prompt-evaluation` evidence.
- `render` PASS/FAIL cites delivered `render-observation` evidence. Without pixels, use `blocked` or `unscored`.
- `user` PASS/FAIL cites `user-judgment` evidence.
- Any `blocked` layer cites the artifact or authority record that caused the block; `unscored` may remain empty.

Required promotion layers depend on `claim_scope`:

| Claim scope | Required PASS layers |
|---|---|
| `structural` | package |
| `prompt-behavior` | package and prompt, plus an unrelated passing holdout with prompt-evaluation evidence |
| `render-fidelity` | package and prompt and render, plus an unrelated passing holdout with render-observation evidence |
| `user-aesthetic` | package and prompt and render and user, plus an unrelated passing holdout with render-observation evidence |

An implemented change may truthfully stop at `implemented` when later evidence is unavailable. Do not weaken the record to obtain `promote`.

## Validation

```bash
python scripts/validate_iteration_record.py ITERATION.json
```

Success prints a JSON report with `"status": "ok"`. A validation error prints all detected issues and exits nonzero.
