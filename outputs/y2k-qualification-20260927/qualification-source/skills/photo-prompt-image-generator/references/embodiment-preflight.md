# Embodiment preflight

Post-core only. The pre-core reasoning and neutral review shape live in `SKILL.md`. This reference explains bindings and review interpretation, not a catalog of preferred poses.

## Ownership and scope

The agent supplies `--embodiment-review-json` with the independently reviewed baseline. The generator validates it against the exact baseline and creates `photo-embodiment-preflight/v1`, binding the normalized core, intent lock, baseline review, and check set. It does not infer human anatomy from a costume, name, role, or retrieved subject category. The review stays outside retrieval, requester meaning, and the negative prompt.

Use the current requested bodily structure. A still life or a portrait with no material bodily mechanism can explain `not_applicable`. A contact, support, articulation, or occluded limb that matters to the image uses `body_action`; decide the five checks individually. Do not mark all five inapplicable to bypass the review. Composition may introduce an applicable action to a previously inapplicable scene, but may not downgrade an applicable baseline or any of its applicable checks to bypass review.

`supported` records a plausible qualitative realization. `requester_intended` preserves a specifically requested departure and requires both literal realization and exact active requester text; the validator checks provenance, not whether that text truly describes the departure. Neither status certifies geometry. `needs_revision` and `unresolved` are blocking findings. Do not relabel uncertainty as support just to get an audit pass. If a detail cannot be inferred, assess whether it matters before adding geometry or asking a question.

## Final composition binding

After rereading the complete final prompt, add:

```json
{
  "embodiment_review": {
    "source_contract_sha256": "<pack.embodiment_preflight.canonical_sha256>",
    "review": {
      "contract_version": "photo-embodiment-review/v1",
      "provenance": "agent_postcomposition",
      "prompt_sha256": "<SHA-256 of exact prompt_en UTF-8 bytes>",
      "scope": "<body_action or not_applicable>",
      "summary": "<what was reviewed in this complete final version>",
      "checks": {}
    }
  }
}
```

For `body_action`, populate all five checks using the neutral shape in `SKILL.md`. A substantive control may serve more than one check; do not pad the prompt with duplicate clauses. Keep meta-review explanations out of runtime prose. Rehashing is the last step after a real re-review, not an automatic repair for stale evidence.

If the core's meaning is clear but the proposed realization is inconsistent, repair agent-authored staging before the first freeze. After freeze, preserve literal locked evidence and use only the allowed composition changes. A required frozen change needs the existing lineage/rebuild path, preserving requester intent and the meaningful contact. Do not copy the motivating case's body part, target, direction, or numerical joint values into generic defaults.

## Runtime boundary

Copy `source_embodiment_preflight_sha256` from the policy into `photo-image-render-request/v2`. With this policy, the runtime prompt is exactly `prompt_en`, optionally followed by `\n\nAvoid: ` and the unchanged nonempty `negative_en`. Additional positive runtime prose must first be incorporated into composition and reviewed. This closes the path where a reviewed prompt is embedded in a larger, unreviewed pose instruction.

Older packs without this policy retain their historical audit behavior. The opt-in flag is required by the normal skill procedure, not retroactively imposed on saved v6 files or direct compatibility callers. Omitting or mutating the policy in a marked pack fails audit.

## Pixel review

The exact composed review determines the additional hard gates below. Include a gate for each final check whose status is not `not_applicable`; review at native scale, using the overall frame to assess ownership and projection. Every gate is judged against the current requested structure, including an explicitly intended departure, rather than universal human proportions.

| Gate | Pixel question |
| --- | --- |
| `embodiment_body_ownership` | Do the important parts visibly belong to the intended actor and structure? |
| `embodiment_joint_chain_and_reach` | Are connected segments, articulation, and the reach to the target coherent? |
| `embodiment_support_and_balance` | Do the visible supports and load-bearing relationships agree with the intended state? |
| `embodiment_contact_and_space` | Does the intended contact survive with coherent boundaries and available space? |
| `embodiment_visibility_and_projection` | Does the view make the critical relation assessable, accounting for foreshortening and occlusion? |

Use the existing `moe-render-review/v1` record and `audit_moe_render_review.py --pack ... --composed ... --review ...`. Its exact checklist is the union of these gates and the existing active character/visual gates. With only embodiment gates, use `photo-embodiment-preflight/v1` as the review's `contract_version`. Keep image path/hash and requester judgment requirements. A critical relationship hidden beyond assessment is not a pass; use `fail` with an explanation of visibility rather than claiming a diagnosed deformity. Harmless occlusion or atypical anatomy alone is not failure.

The audit validates a submitted review; it does not inspect pixels, solve inverse kinematics, estimate failure probability, or establish user preference. Structural and prompt-review results must remain separate from rendered-fidelity claims.
