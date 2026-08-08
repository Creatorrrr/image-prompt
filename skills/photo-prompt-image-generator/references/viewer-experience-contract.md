# Viewer Experience Contract

Use this contract only when the candidate pack contains `viewer_experience.enabled: true`. It is a composition and local image-review procedure, not a score predicting human emotion, purchase, virality, or long-term attachment.

## Compose One Viewer Promise

1. Declare the viewing context and the target audience's required literacy. Use `required_prior_knowledge: none` when the frame must work without insider knowledge.
2. Select exactly one `primary_viewer_need` and write one scalar `intended_experience`. Mixed feeling is allowed inside one coherent experience; a list of emotions is not.
3. State one `viewer_promise`: why this frame deserves attention. Do not copy this interpretation into the visible prompt as an outcome claim.
4. Design one first-glance hook and one interpretive question. A product-detail image may use `none` for the question when immediate comprehension or action is the objective.
5. Ground affect in one visible causal chain: actor, action, target, and consequence.
6. Select an attachment channel, reinspection mode, and commercial objective. Use `none` when they do not apply.
7. Bind only visible evidence phrases into `prompt_en`.

## Composed Shape

```json
{
  "viewer_experience": {
    "target_audience": {
      "literacy": "general|genre_literate|subculture_literate|expert",
      "required_prior_knowledge": "none or a narrow explicit scope"
    },
    "viewing_context": "feed_thumbnail|full_screen|poster|product_detail",
    "primary_viewer_need": "insight|care|relatedness|identity|meaning|recovery|aspiration|trust",
    "intended_experience": "one coherent experience",
    "viewer_promise": "why the frame deserves attention",
    "first_glance_hook": "the visible focal relation",
    "interpretive_question": "one resolvable question or none",
    "affect_evidence": {
      "actor": "visible causal actor",
      "action": "directed action",
      "target": "visible target",
      "consequence": "visible cost, response, or state change"
    },
    "attachment_channel": "none|agency|reciprocity|continuity|self_relevance",
    "reinspection_reward": {
      "mode": "none|causal_second_reading",
      "description": "a second clue that changes the first reading"
    },
    "commercial_objective": "none|stop|comprehend|remember|act|share|return",
    "prompt_evidence": {
      "first_glance_hook_phrase": "literal prompt substring",
      "affect_actor_phrase": "literal prompt substring",
      "affect_action_phrase": "literal prompt substring",
      "affect_target_phrase": "literal prompt substring",
      "affect_consequence_phrase": "literal prompt substring",
      "attachment_phrase": "conditional literal substring",
      "reinspection_reward_phrase": "conditional literal substring",
      "commercial_legibility_phrase": "conditional literal substring"
    }
  }
}
```

## Conditional Rules

- `care`, `relatedness`, and `identity` require a non-`none` attachment channel and `attachment_phrase`.
- `causal_second_reading` requires a concrete description and `reinspection_reward_phrase` tied to the same event. Noncommercial creative-direction runs require it.
- `comprehend`, `remember`, and `act` require `commercial_legibility_phrase`. Keep product identity and function immediately readable; do not hide them behind a puzzle.
- A face, gaze, or expression may support affect but cannot replace action, target, and consequence.
- Do not use baby face, childlike proportions, oversized eyes, or other youth morphology as attachment evidence. Adult character routes retain explicit-adult and non-inference guards.
- Do not use `cute`, `moe`, `anime`, `cinematic`, `emotional`, or similar labels alone as evidence. Show what the character or object does.
- Do not write `the viewer feels`, `evokes empathy`, `creates attachment`, `memorable image`, or other response declarations as evidence.
- Keep one primary need. Do not stack care, awe, nostalgia, arousal, romance, and surprise to simulate depth.

## Commercial and Subculture Boundaries

Commercial objectives are distinct: stopping, comprehension, memory, action, sharing, and return are not interchangeable. Product-detail `comprehend` or `act` may use no reinspection reward. Never sacrifice product or subject legibility for an attention trick, unsupported claim, logo, or explanatory text.

For subculture characters, scope audience literacy explicitly. Let general viewers read the action while genre-literate viewers recover extra meaning. Express attachment through agency, reciprocity, continuity, or self-relevance; a market term, costume, ethnicity, body shape, or protected design is not relationship evidence.

## Image Review

Prompt audit is preflight only. Inspect generated pixels without prompt or result metadata at thumbnail and native size. Require:

- one stable first-glance focal hierarchy;
- the event, product, or premise to be recoverable;
- the affect cause to be visible as action and consequence;
- the selected attachment channel or commercial objective to remain intact;
- any reinspection reward to support the same causal meaning;
- topic, adult/IP/cultural boundaries, and photographic coherence to remain intact.

Record this as local product qualification. Human audience response still requires a separate human evaluation and must not be inferred from audit or image-review PASS.
