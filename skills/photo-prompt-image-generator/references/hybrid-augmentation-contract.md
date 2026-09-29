# Candidate Augmentation Contracts

## V5 Creative Augmentation

The compatibility `photo-candidate-pack/v5` path does not expose `hybrid_augmentation` or three fixed routes. It exposes `photo-creative-augmentation/v1` only after one request-envelope-bound `photo-authorial-core/v2` and `photo-intent-lock/v1` have established the standalone baseline and locked requester meaning. Every transformed candidate declares affected dimensions and may touch only open dimensions.

The generator forms one advisory pool only after existing applicability, conflict, identity/species/no-people, negative, safety, and explicit user-exclusion guards. Semantic mode ranks that pool from the redacted core query; rule mode uses context and lexical fallback for reproducible offline inspection. Scores remain private. Relative rank partitions the pool into `near`, `adjacent`, and `lateral`; creativity changes only the allowed bands, while seed performs weighted sampling without replacement inside them.

Every sampled row requires a decision under `creative_augmentation_brief.decisions`:

```json
{
  "creative_augmentation_brief": {
    "decisions": [
      {
        "candidate_id": "slot:texture:example",
        "decision": "transformed",
        "rationale": "Why this material strengthens the frozen core.",
        "artistic_interpretation": "The new role it plays in this scene.",
        "transformation": "How context, causality, gesture, material, framing, light, mood, or timing changed.",
        "prompt_evidence": "newly authored literal visible phrase with a relation or consequence"
      },
      {
        "candidate_id": "slot:mood:example",
        "decision": "rejected",
        "rationale": "Why it weakens or confuses the core."
      }
    ]
  }
}
```

Rejecting all sampled rows is valid. Transform at most three; include transformed IDs in `chosen_candidate_ids`, keep rejected IDs out, and do not duplicate transformed rows in `candidate_interpretations`. Candidate `concept_terms` are unordered material. Evidence needs at least four content words and two newly authored words beyond those terms.

V5 keeps an active adult-fashion contract at top-level `adult_appeal` rather than inside a hybrid route. Record its composed interpretation in `adult_appeal_brief`. Candidate adoption is optional, but exact axis intensities, blend, explicit adult subject, agency, and the existing combination audit remain mandatory. This is compatibility with the existing policy, not new adult routing.

## V4 Hybrid Augmentation

Use this compatibility contract when a v4 candidate pack contains `hybrid_augmentation.enabled: true`. In `photo-hybrid-augmentation/v2`, treat the pack as optional source vocabulary: keep the agent-authored concept core, inspect all three candidate-sourced routes, and artistically transform or reject their details. The pack never supplies final prompt prose. Validation and provenance protect this creative step; they do not replace the agent's authorship.

## Activation

In v4, the contract is present when `--hybrid-augmentation` is explicit, when high creative direction requires it, or when an eligible adult-appeal axis is active. The normal skill workflow uses v6 typed-core creative augmentation instead. Eligible human v4 candidate packs also activate the configured `sensual=1`, `fetish=0` adult-fashion default; no-people and non-human packs do not activate it.

## Candidate Routes

The pack exposes three routes assembled from actual eligible candidate IDs:

- `material_world`: material, garment, texture, color, prop, and world specificity;
- `action_camera`: action, pose, gaze, framing, camera, and composition consequences;
- `light_second_reading`: light, focus, mood, traces, particles, and reinspection evidence.

Each route contains two to four details. A detail declares its candidate ID, slot, intended function, source, and unordered `concept_terms`. These are semantic ingredients, not a phrase template and not a checklist that must all appear. Do not restore their source order, join them into pseudo-prose, or merge routes. Consider every route, then select exactly one or reject all three with a concrete reason.

When a route is selected, decide every detail as `transformed` or `rejected`. Transform one to three details. Include transformed IDs in `chosen_candidate_ids`; for each, state the artistic interpretation, what changed, which context/causality/gesture/material/framing/light/mood/timing dimension changed, and what marginal value it adds. Bind a newly authored literal phrase that gives the cue a concrete relation or consequence beyond its source terms. Keep rejected IDs out of `chosen_candidate_ids`.

These transformed rows already satisfy the v4 authorship requirement, so do not duplicate them in top-level `candidate_interpretations`. That top-level field covers ordinary chosen candidates outside `augmentation_brief`.

Use this composed shape beside the ordinary fields:

```json
{
  "augmentation_brief": {
    "concept_core": "The agent-authored governing idea.",
    "routes_considered": [
      {"route_id": "material_world", "decision": "selected", "reason": "Why it fits."},
      {"route_id": "action_camera", "decision": "rejected", "reason": "Why it does not."},
      {"route_id": "light_second_reading", "decision": "rejected", "reason": "Why it does not."}
    ],
    "selected_route_id": "material_world",
    "decisions": [
      {
        "candidate_id": "slot:texture:example",
        "decision": "transformed",
        "function": "material_detail",
        "rationale": "Why it supports the core.",
        "marginal_contribution": "What becomes less distinctive if removed.",
        "artistic_interpretation": "What the ingredient means in this authored scene.",
        "transformation": "How its context or relationship was changed.",
        "transformation_dimensions": ["material", "causality"],
        "prompt_evidence": "newly authored literal visible prompt phrase with a relation or consequence"
      }
    ]
  }
}
```

To reject all routes, set `selected_route_id` to `none`, mark every route rejected, provide `all_rejected_reason`, and leave `decisions` empty. This is valid when every candidate would weaken the core concept.

## Adult Appeal Axes

Normal v6 runs first resolve `precore/creative_controls.json` using its candidate-free resolver. The core binds the resulting `creative_controls_sha256`; pass that same snapshot with `--creative-controls-json`. Read its current values, source, definitions and ordinal level meanings before authoring wardrobe, portrayal and the photographic direction. The generator and composed audit preserve the binding. Later CLI overrides must agree with the snapshot. Old unbound calls remain compatible and make no claim that their settings informed the initial draft.

The axes are independent and may share one expressive choice. Use the frozen
short definitions and level meanings from the pre-core snapshot. `sensual`
expresses broadly interpreted human attraction and desire. `fetish` expresses a
distinctive focus of attraction or fascination across objects, bodies, clothing,
materials, roles, situations, behaviors and sensory qualities. Neither control
is confined to fashion; contextual use supplies the interpretation.

The authoritative defaults and 0–3 meanings live in the pre-core definition file. Zero disables added treatment without deleting requested meaning; positive levels describe supporting, clearly readable or leading aesthetic intent. They are not native image parameters, exposure fractions, item counts, or proof of image quality. Emphasis follows active intensities unless explicitly selected; it cannot reactivate an inactive axis.

Bound v6 packs use `photo-contextual-appeal/v2` and dimension scope v4. Both axes can express contextual relationships through their declared unlocked portrayal, clothing, action and photographic dimensions. Read [contextual appeal](contextual-appeal.md) for the conditional review fields. Legacy preset/tag/minimum-intensity admission remains only for unbound or older calls; archived scope v1/v2 packs retain their original meanings.

Current scope v4 preserves whole-dimension and property locks. Role, setting,
relationship and timing effects additionally require an explicit open dimension;
other declared portrayal dimensions retain the adult-axis scope exception.
Whole-look candidates with unknown property effects are rejected when they may
replace a protected property. Keep the full affected scope; independently author
a compatible choice rather than silently narrowing a candidate's effects.

Old run artifacts remain unchanged. Previous control names and v1 control
snapshots are not accepted by the current resolver; use the retained historical
implementation for old runs. No input aliases or artifact migration are provided.

Candidate adoption is optional. For each active axis, the existing `adult_appeal_brief` explains how the direction serves this scene. A baseline realization may be retained without inventing a new detail:

```json
{
  "adult_subject_phrase": "literal explicitly adult phrase",
  "agency_phrase": "literal self-directed action phrase",
  "axes": {
    "sensual": {
      "intensity": 2,
      "realization": "baseline",
      "affected_dimensions": [],
      "artistic_interpretation": "How the initial portrayal and wardrobe carry this direction.",
      "prompt_evidence": "literal phrase present in both baseline and final prompt"
    },
    "fetish": {
      "intensity": 1,
      "realization": "refined",
      "affected_dimensions": ["material"],
      "artistic_interpretation": "How a compatible material refinement supports the same photograph.",
      "prompt_evidence": "literal final prompt phrase"
    }
  },
  "blend": {"emphasis": "sensual_led"}
}
```

Copy actual values from the pack rather than treating the example as defaults. `baseline` introduces no axis candidate or changed dimensions; its evidence must remain literal in both prompts. `refined` declares every changed dimension, including the complete effects of adopted candidates. For any partially locked dimension, add `affected_properties` rows with `dimension`, `target`, and `property`, using the same canonical paths as the core. Parent properties include their children. Candidate and direct-authoring paths obey the same protected meanings. This also applies to adult candidates selected through `creative_augmentation`.

Keep requested intensity and constraint reasons visible; explain a limited realization in the existing interpretation instead of declaring aesthetic success. The agent must judge coherence and perceptual strength. Mechanical audit checks integrity, scope and literal evidence, not whether a sentence is sufficiently sensual or stylish. Only an axis with no remaining dimensions is disabled by dimension scope; the configured request remains recorded.

The existing subject eligibility, explicit opt-outs, nonsexual requester meaning and combination checks remain applicable. Initial eligibility comes from the declared requester context, never inferred attractiveness or a reference person's presumed traits. Keep the subject unambiguously adult and original. Do not infer adulthood from face, body, clothing, ethnicity, or market origin.

## Combination Audit and Review Boundary

Audit styling, pose, framing, and camera together. The current hard rule rejects sheer or lingerie-coded styling combined with an extreme ground-level angle. Stacked body emphasis plus a lower angle is a quality warning requiring intentional review. These project checks do not override platform policy or image-tool enforcement.

Audit PASS proves candidate provenance, explicit artistic decisions, transformation budgets, newly authored context, and literal prompt binding. It does not prove rendered detail, tasteful balance, safety-tool acceptance, popularity, or audience response. Review generated pixels without prompt metadata; validate audience appeal through separate human or engagement evaluation.

## Legacy Replay

`photo-hybrid-augmentation/v1` appears only in `--candidate-pack-version v3|v2` replay packs. It retains the older `accepted|modified|rejected` states, two-to-five adoption budget, literal candidate labels, and one adopted inventory candidate per active axis. Do not use that contract for new composition; it exists so historical packs and consumers remain auditable.
