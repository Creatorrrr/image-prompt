# Creative Direction Contract

Use this contract only when the candidate pack contains `creative_direction.enabled: true`. It is an agent composition procedure, not a topic taxonomy, preset family, score claiming historical novelty, or permission to weaken the scene, safety, character, candidate-provenance, or negative-prompt contracts.

## What the Contract Optimizes

The target is a viewer-side experience: the frame first offers a recognizable scene, then makes one non-default premise discoverable, and finally lets its physical consequences recover one coherent meaning. Novel adjectives, unusual styling, visual busyness, randomness, and distance from other candidate tokens are not sufficient.

Treat the legacy `creative_exploration` field as bounded slot-level search diversity. Treat `creative_direction` as concept development and selection. A run may have both fields, but one does not prove the other.

`artistic_final_touch` is a surface-craft suggestion. Shared light, a quiet imperfection, or a material trace may improve photographic finish, but repeating that sentence is never evidence of an authorial point of view.

## Develop Before Composing

Write a `creative_brief` beside the ordinary composed fields.

1. Name at least three likely first-answer clichés in `ordinary_baseline` and explicitly reject them in `rejected_cliches`.
2. Develop at least four proposals using distinct operator IDs exposed in the pack. Do not write four variations of the same anomaly.
3. Give every proposal a familiar anchor, the viewer's expected reading, exactly one changed rule, at least two visible consequences, one aboutness, and a short unique `signature_phrase` that could appear naturally in the final prompt.
4. Critique the proposals for topic fidelity, consequence legibility, reveal economy, photographic realizability, and cliché distance. Select exactly one; do not average or stack the others.
5. Give the selected proposal an authorial grammar: where the camera is, which instant it withholds or catches, what the frame deliberately omits, and what physical/material relation repeats across the image.

The operator IDs are abstract moves. They do not prescribe a genre:

- `structural_analogy`: translate a relationship into space, matter, or causality.
- `expectation_inversion`: reverse one expected relation while retaining the familiar scene.
- `absence_as_evidence`: show a missing thing only through its traces and responses.
- `rule_extension`: extend one ordinary rule into an unexpected domain.
- `temporal_fold`: let before and after coexist through one trace, gesture, or reflection.
- `relational_reversal`: let setting, prop, foreground, or background assume a causal role.
- `functional_recontextualization`: give one familiar object a new coherent function.
- `controlled_impossibility`: introduce one impossible law with consistent material consequences.

## Selected Concept Shape

The composed object retains `pack_id`, `prompt_en`, exact `negative_en`, `chosen_candidate_ids`, and `composer: agent`, then adds:

```json
{
  "creative_brief": {
    "ordinary_baseline": ["first cliche", "second cliche", "third cliche"],
    "rejected_cliches": ["first cliche", "second cliche", "third cliche"],
    "proposals": [
      {
        "id": "concept_1",
        "operator_id": "absence_as_evidence",
        "premise": "One concise conceptual proposition.",
        "familiar_anchor": "The immediately recognizable scene.",
        "viewer_expectation": "What a viewer initially assumes.",
        "rule_break": "One and only one changed causal or perceptual rule.",
        "visible_consequences": ["first physical result", "second physical result"],
        "aboutness": "The human or thematic meaning recovered from those results.",
        "signature_phrase": "a natural literal visual phrase unique to this proposal"
      }
    ],
    "selected_proposal_id": "concept_1",
    "selection_rationale": "Why this proposal is the most legible and economical, not merely the strangest.",
    "selected_concept": {
      "proposal_id": "concept_1",
      "familiar_anchor": "Exact value from the selected proposal.",
      "rule_break": "Exact value from the selected proposal.",
      "visible_consequences": ["exact first result", "exact second result"],
      "reveal_path": ["first reading", "noticed disruption", "recovered meaning"],
      "aboutness": "Exact value from the selected proposal.",
      "authorial_grammar": {
        "vantage": "A motivated camera position.",
        "timing": "A motivated instant or duration.",
        "omission": "What the frame deliberately withholds.",
        "material_rule": "A repeated physical relation that unifies the frame."
      },
      "prompt_evidence": {
        "familiar_anchor_phrase": "literal prompt substring",
        "rule_break_phrase": "literal prompt substring",
        "visible_consequence_phrases": ["literal prompt substring", "literal prompt substring"],
        "reveal_path_phrases": ["literal prompt substring", "literal prompt substring", "literal prompt substring"],
        "authorial_grammar_phrases": {
          "vantage": "literal prompt substring",
          "timing": "literal prompt substring",
          "omission": "literal prompt substring",
          "material_rule": "literal prompt substring"
        }
      }
    }
  }
}
```

`proposals` must contain at least four complete objects even though the example shows one. `selected_concept` must copy the selected proposal's anchor, rule, consequence chain, and aboutness exactly.

## Binding and Image Review

The audit verifies the development structure and literal prompt bindings. It rejects missing or duplicate moves, stacked rule-break fields, an unknown selection, a selected-concept mismatch, an unselected signature in the prompt, missing consequence/reveal evidence, reused evidence strings, and authorial evidence borrowed from fixed `artistic_final_touch` wording.

An audit pass does not prove that the image model rendered the idea. When generating an image, inspect the pixels without the prompt and require:

- topic fidelity and photographic coherence;
- one recognizable anchor and one non-default core premise;
- exactly one rule change with at least two visible consequences;
- a discoverable surprise-to-insight path;
- a deliberate vantage, timing, omission, or material system that supports the same aboutness;
- no unrelated anomaly stacking, explanatory typography, or metadata dependence.

Preserve the first render. If a required relationship is absent, record the concrete product/model cause before a bounded pristine retry; do not generate a batch and select the most favorable image.
