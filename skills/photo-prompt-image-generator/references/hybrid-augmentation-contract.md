# Candidate Augmentation Contracts

## Current Creative Augmentation

The `photo-candidate-pack/v6` path exposes `photo-creative-augmentation/v1` only after one request-envelope-bound `photo-authorial-core/v3` and `photo-intent-lock/v2` have established the standalone baseline and locked requester meaning. Every transformed candidate declares affected dimensions and may touch only open dimensions.

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

V6 keeps an active adult-fashion contract at top-level `adult_appeal` rather than inside a hybrid route. Record its composed interpretation in `adult_appeal_brief`. Candidate adoption is optional, but exact axis intensities, blend, explicit adult subject, agency, and the existing combination audit remain mandatory. The controls snapshot and contextual appeal contract govern each axis.


## Contextual adult appeal

Bound v6 packs use `photo-contextual-appeal/v2` and dimension scope v4. Both axes can express contextual relationships through their declared unlocked portrayal, clothing, action and photographic dimensions. Read [contextual appeal](contextual-appeal.md) for the conditional review fields.

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
