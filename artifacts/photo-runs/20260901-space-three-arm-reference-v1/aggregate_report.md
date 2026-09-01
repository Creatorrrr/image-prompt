# Space visual-semantics three-arm qualification

## Outcome

All three independently generated holdouts passed the root pixel review under the precommitted `partial = fail` rule. Package and prompt audits were kept separate from the final pixel decision. User aesthetic preference remains unscored.

| Arm | Random profile | Complex concept | Package | Prompt request | Root pixels | Profile gates |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | `barred_spiral_galaxy_structure` | orbital observatory control room during a micrometeoroid alert | PASS | PASS | PASS | 5/5 |
| 02 | `microgravity_orbital_interior` | scheduled inspection in a crowded station module | PASS | PASS | PASS | 5/5 |
| 03 | `solar_flare_active_region_burst` | mobile lunar field laboratory halted mid-traverse | PASS | PASS | PASS | 5/5 |

Each saved image also passed all five common controls: visible-appearance continuity from the supplied adult portrait, adult-age continuity, gross structural coherence, required physical contact, and no reliance on pseudo-text for the tested scientific meaning.

## Independence and generation boundary

- Random seed: `2253228305`
- Three isolated agents; no sibling-arm inputs
- Candidate-pack contract: v6 in every arm
- Native image calls: one per arm, three total
- Semantic retries: zero
- Reference use: visible appearance only; no identity or same-person claim
- Optional candidate inspiration stayed advisory. Agents selected no optional candidate IDs when they conflicted with the frozen concept, while the new hard visual profiles remained bound into each v6 pack and composed prompt.

## Evidence layers

- Data and retrieval validation: repository tests and regenerated indexes
- Package evidence: each arm's `candidate_pack.json`
- Prompt evidence: each arm's `composed_prompt.json` and render-request audit
- Pixel evidence: each arm's saved `render.png`, self-review, and the independent root review
- User judgment: pending; not inferred from technical PASS

The qualification is bounded to these three random holdouts. It does not establish universal render fidelity for all 16 newly added space profiles.
