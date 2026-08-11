# Universal scene prompt holdout conflicts with literal-bound scene contracts

- Recorded: 2026-08-10 13:49 KST
- Status: resolved
- Resolved: 2026-08-11 11:27 KST
- Goal/checkpoint: Universal Scene Candidate Layer Goal / Stage 3 qualification-oracle integration
- Affected scope: `universal_scene_prompt_holdout_v1.jsonl`, scene-contract cross-validation, and the current 24-case qualification oracle
- Search terms: universal scene holdout, literal-bound contract, role projection, bridge obligation, contradictory oracle
- Related paths: `GOAL_PLAN.md`, `skills/subculture-illustration-image-generator/assets/universal_scene_prompt_holdout_v1.jsonl`, `skills/subculture-illustration-image-generator/assets/universal_scene_contract_holdout_v1.jsonl`, `skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py`
- Related passed reports: `docs/passed-reports/2026-08-11-universal-scene-public-boundary-integration.md`

## Failure

- Conditions or trigger: independently compare every frozen prompt expectation with the later literal-bound scene contract instead of validating the two files separately.
- Expected: fixed, closed, and open slot states and all eight canonical event-role states agree exactly; any fixed role value matches the canonical scene-contract bytes; requested bridge obligations map to the runtime's closed seven bridge types.
- Observed: the historical prompt holdout and literal-bound contracts are contradictory oracles. The independent comparison found 17 of 24 cases with slot-state mismatches, 30 role-state conflicts across 21 cases, 44 fixed-role value conflicts, and 34 noncanonical expected role labels. Eighteen prompt cases also name bridge requirements outside the runtime's closed seven-type enum. The validator accepted these because it checked each asset's local shape but did not compare their semantic projections.
- Example boundary: case 01 historically marked relation and recipient closed even though the request contains no literal negative for either; the literal-bound contract correctly leaves them open. Weakening that rule would reintroduce inferred constraints and violate the frozen scene-contract design.
- Later independent boundary: case 12 exposed that the v1 scene contract itself is not fully literal-bound. The request forbids attaching a human face or hands to a faceless, limbless cloud creature, but the contract closes the entire `prop` slot and `instrument` role using those phrases. That turns unavailable human manipulators into a universal no-object rule and blocks legitimate nonhand, body, environmental, or external-support interactions.
- Impact on the goal: a reported 24/24 result could pass while ignoring contradictory expectation fields. Prompt qualification cannot begin until there is one current, cross-validated oracle.

## Evidence

- The v1 prompt holdout and v1 scene-contract files remain byte-preserved as historical evidence.
- Independent read-only audit enumerated the mismatches before Stage 4 artifacts were created.
- Zero v3 prompt-qualification records or images have consumed a revised oracle.
- The first independent replay against the post-contract v2 mapping found only 3 of 24 current runtime selections satisfying every mapped canonical bridge type. This confirms the v2 oracle is not a copy of current output and that the runtime still has a material product gap rather than a paperwork-only mismatch.
- A provisional runtime rule named for handling-resource denial made the case-12 inference executable, confirming that copying scene-contract v1 byte-for-byte into the current oracle would preserve a holdout-shaped product defect rather than repair it.

## Cause assessment

- Confirmed cause: the prompt expectations were authored before the literal-bound scene-contract schema, then treated as if both were one frozen contract. The validator never encoded a lineage or cross-projection check.
- Confidence: high.
- Unknowns: none at the architecture boundary; per-case legacy labels and the case-12 contract correction require explicit reviewed mappings rather than deletion or silent relabeling.

## Resolution or next safe step

- Preserve v1 unchanged and label it historical pre-contract expectation evidence.
- Preserve scene-contract holdout v1 unchanged as historical evidence and add a post-contract scene-contract holdout v2. Its only reviewed semantic delta is case 12: `prop` and `instrument` become open, while explicit human facial-display, manipulator, and appendage unavailability plus forbidden human face/hand attachment remain intact.
- Add a versioned current holdout that records the v1 prompt and scene-contract lineage hashes and explicitly declares that it is a post-contract qualification revision, not a pre-implementation freeze.
- Project all six slot states and all eight canonical role states plus fixed values directly from the scene contract and require exact byte-equivalent validation.
- Preserve every historical noncanonical role and bridge label as a research/evidence obligation with a reviewed mapping to canonical slot, role, atom, resource, bridge, or pixel evidence. Runtime bridge requirements must use only the closed seven types, and every historical obligation must map to enforced runtime evidence.
- Add mutation tests for lineage hashes, all projections, mappings, and bridge closure. Anchor the new current-oracle and validator hashes from a committed baseline rather than trusting mutable self-reported hashes.
- Resolve only after both versioned current holdouts, exact cross-validator, focused mutations, all 24 v3 builds/audits, compiled-obligation replay, legacy replay, and the independent Stage 3 audit pass without changing either v1 asset.

## Lifecycle resolution (2026-08-11)

- Resolution: preserved prompt and scene-contract v1 bytes as historical evidence; added literal-bound scene-contract v2, a versioned current v2 oracle, reviewed expectation crosswalk, manifest, and baseline with exact lineage and projection validation.
- Verification: the current focused suite passed exact current-oracle lineage/mapping totals, all 24 deterministic builds and integrity audits, all 24 compiled-obligation replays, all 24 composition carriers, and legacy v1/v2 plus photo replay. The current rerun was 7/7 in 76.945 seconds; directional/source-authority regression was 15/15 in 4.019 seconds.
- Scope limit: this resolution applies to the public 24-case oracle and does not qualify hidden unseen contracts or rendered pixels.
