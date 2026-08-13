# Natural moe composite request blocked by single-mixin gate

- Recorded: 2026-08-12 18:07 KST
- Status: resolved
- Resolved: 2026-08-13 07:28 KST
- Goal/checkpoint: natural Korean moe request routing and role/species/mixin preservation
- Affected scope: `photo-prompt-image-generator` concept wrapper review gates
- Search terms: `mixin_shape`, `츤데레`, `수인`, `네코미미`, `applied_mixins`
- Related paths: `skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py`, `skills/photo-prompt-image-generator/assets/concept_recipes.json`
- Related passed reports: none

## Failure

- Conditions or trigger: Generate one candidate pack from the concept `야하지 않은 모에한 성인 네코미미 츤데레 메이드` while preserving `네코미미` as a human-with-living-cat-ears trait rather than a full beastkin body.
- Expected: Preserve `메이드`, `츤데레`, and `네코미미`, then emit one nonsexual moe-response candidate pack.
- Observed: The original exclusive `츤데레` `mixin_shape` gate rejected the explicitly requested second mixin. Reusing the broader `수인` route also over-expanded the body contract beyond the user's nekomimi request.
- Impact on the goal: The representative multi-trait moe request cannot reach candidate-pack composition or rendering.

### Regression found during completion audit (2026-08-13)

- Conditions or trigger: Generate public-wrapper packs from the frozen Japanese compounds `性的ではない猫耳の成人ツンデレメイドが、世話を焼いたことを隠す萌える瞬間` and `母性的で優しいママみのある、美しくてかわいい成人猫耳メイドの萌える写真`.
- Expected: The first preserves maid + tsundere + nekomimi; the second preserves maid + nekomimi + nurturant benevolence, exactly as the Korean and English parallel cases do.
- Observed: The first keeps the two mixins but loses the maid role and falls to `character_gap_contrast_scene`. The second keeps the maid role and `nonhuman_reflex_leak` support label but loses the feline species-family lock and forced living-ear slots.
- Impact on the goal: Japanese adjacent aliases are not compositionally preserved end to end even though the intent-only fixture passes.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: wrapper `--explain-concept` output for the representative concept.
- Result: The request could not simultaneously retain the maid role, tsundere contradiction, and compact human nekomimi anatomy under the existing exclusive mixin shape.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed. The recipes modeled `mixin_shape` as exclusive, while `네코미미` was not represented separately from the broader beastkin surface/anatomy contract.
- Confidence: confirmed
- Remaining unknowns: Rendered-pixel moe quality remains a later acceptance checkpoint, not evidence from this gate test.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Map `네코미미` to the broad `수인` contract | Rejected as the final design | It admitted body-rooted fur and animal-limb evidence that a human nekomimi request did not ask for |
| Add a dedicated `네코미미` mixin and narrow `츤데레` compatibility | Passed wrapper generation | Both independent gate sets remained active and the merged anchors resolved |
| Sweep all frozen positive natural-language cases through the public wrapper | Korean and English composites preserve role/species; two Japanese compounds did not | Sequential alias replacement inserted Korean canonical text beside the next Japanese alias, so the next boundary check saw an artificial Korean word character and skipped it |
| Replace aliases in one pass against the original source text | Passed | Every adjacent alias keeps the lexical boundaries that existed in the user's request; inserted canonical text cannot suppress or recursively trigger another alias |
| Promote all 32 frozen intent cases to public-wrapper materialization | Passed 32/32 | All 25 positive requests preserve response, tone, and materialized role/scene contracts; all seven hard negatives remain outside `moe_response` |

## Resolution or next safe step

- Resolution/workaround: The original dedicated `네코미미` scope remains valid. `canonicalize_concept` now constructs one longest-first alias alternation and replaces matches in one pass against the original source text. Thus `猫耳メイド` and `ツンデレメイド` preserve both adjacent aliases without an inserted Korean canonical value changing the next boundary.
- Verification: The 32-case frozen KO/JA/EN contract now runs end to end through the public wrapper: 25/25 positives preserve route, mechanism, support, relationship where requested, aesthetic baseline, text intent, and sexual tone; seven/7 hard negatives do not receive `moe_response`. Role cases preserve the expected preset and subject, all maid cases preserve the frill-apron costume, and all seven nekomimi composites preserve the exact feline family plus compact living-ear slots. Nonsexual cases materialize 0/0 adult-appeal axes while generic or explicit sensual adult moe materializes the configured 1/0 support. The complete affected suites pass 335/335 (`test_photo_prompt_contract_v2` 59/59 in 345.805 seconds and `test_prompt_generator` 276/276 in 245.583 seconds).

## Reuse guidance

- Avoid: Disabling review gates or allowing arbitrary extra mixins globally.
- Prefer: Give materially different anatomy scopes separate mixins, declare narrow compatibility, and keep each mixin's independent evidence gates active.
- Applicable when: Two user-explicit mixins are designed to compose and their guard contracts remain independently enforceable.
- Re-check when: Adding another natural-language alias that expands to more than one mixin.
