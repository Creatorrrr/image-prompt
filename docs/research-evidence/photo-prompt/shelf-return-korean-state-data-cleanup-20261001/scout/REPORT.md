# Resource-allocation continuity DATA scout

## Decision

- Exactly 12 priority-3 rows reviewed: 11 keeps and one qualified, uncommitted Korean-label-only proposal
- Proposed row: `slot:aftermath_trace:pov_reduced_purchase_set_trace`
- Concrete contradiction: current Korean says `되돌린 한 품목의 진열 공백` (the returned item's display gap), while its English label and complete concept unit say that the returned item's original shelf position is restored
- Replace only that phrase with `되돌린 한 품목이 놓인 원래 진열 위치` (the original display position occupied by the returned item). The smaller completed essential purchase, shared frame, actor/resource continuity and all other source fields stay unchanged
- This does not claim the entire shelf is stocked. An unrelated display gap can coexist
- The mismatch already exists in the original authored proposal. This is source-language consistency repair, not an English runtime-semantic-loss repair

## Source chain

`photo_prompt_poverty_extension.json` /slots/action/0 (line 320 onward) returns one staple from the basket to its source display and completes the reduced payment. /slots/composition/0 (line 1115 onward) keeps source shelf, returning hand, finite payment and reduced paid set on one axis. /slots/aftermath_trace/0 (lines 1476–1498) is the disputed same-item endpoint.

Original `candidate-data-proposal.json` lines 255, 258 and 259 contain those same action, composition and result meanings. The result's original Korean repeats the gap mismatch; its original English agrees with the action's returned-to-source state. The existing `food_access_budget_choice_event` profile preserves same-adult return, reduced completed purchase and source-to-result continuity. No new profile rule or stronger gate is proposed.

The source report's lines 18–43, 254–264 and 291–309 support cause → same adult response → immediate resource result and narrow optional slot roles. S01, S04, S07, S09, S10 and S16 were checked in the frozen evidence ledger. They support abstract need/resource dimensions or representation limits, not literal photographic prototypes or personal-income diagnosis. Historical ledger candidate lists are not treated as exhaustive reverse bindings.

## Keeps

1. `pov_food_item_return_action`: basket → same item's original display → completed reduced payment remains intact
2. `pov_finite_payment_basic_basket_prop`: basic-food set and one visibly finite payment resource remain intact
3. `pov_remaining_supply_division_action`: active transfer from one near-empty source to several portions remains intact
4. `pov_single_source_staple_container_prop`: depleted single source and distinct destination containers remain intact
5. `pov_depleted_container_after_portion_trace`: original source's post-allocation depletion remains intact
6. `pov_choose_one_defer_one_action`: one need met, competing need deferred, same adult and finite resource remain intact
7. `pov_two_essential_need_anchors_prop`: two distinct basic needs and one shared limited resource remain intact
8. `pov_paid_one_deferred_one_trace`: provisioned/prepared side and inactive/sealed/deferred side coexist; retain source-authored material variants
9. `pov_shift_end_budget_reconcile_action`: paid work → same-actor allocation → unresolved remainder survives; matching result and positive embedding preserve shortfall, so English “remainder” alone does not justify expansion
10. `pov_work_output_pay_essentials_prop`: work output, nonidentifying compensation and essential costs remain linked
11. `pov_remaining_essential_shortfall_trace`: post-allocation unmet/deferred essential need remains intact

Every selected row has an explicit complete English concept unit. Compiled members preserve those units exactly. Selected rows and four bundles contain no authored explicit `relations` arrays; their relationships are carried by those units, bundle components and existing profiles. Nothing was truncated or reversed there, and no speculative new relation endpoints were added. Maintenance reference digest, exact family bindings and compiled bundle source digests validate. Optional atoms are not required to independently repeat every full-profile component.

## Actual V6 gate

- Production `build_candidate_pack(..., 'v6')` and hash-verifying `compose_pack_view.verify_view` were used
- Genuine source subject `pov_food_budget_adult_subject` remains present, with human/adult kind/tags and the required food-access family; `compatible_with_picked(..., forced=False)` passes for both rows. All other selected rows also pass their matching adult-subject compatibility checks
- No no-subject shortcut, forced choice, eligibility change, core rewrite or soft-policy clearing was used
- Synthetic rule-mode contract fixture; controlled candidate exposure is explicitly recorded. The generated core, creative controls, provenance, negative guard and soft policy remain unchanged
- Before and proposed actual full packs, details and overviews are byte-for-structure equal. Both pack IDs are `946d69ecd0b85dc6`
- The existing English concept unit already preserves the restored shelf position and smaller paid set; it remains unchanged and optional. No final English prompt improvement is claimed

## Frozen probes and limits

Eight fresh independently written EN/KO probes were frozen before the V6 gate: one positive pair, one unrelated-display-gap coexistence pair, and two near-miss pairs (unfinished removal and different-actor restocking). They remain unmeasured. Freeze SHA-256: `7a26c024437035c10be738c4f7da6357c034e1f1bd1c79681882eeed9520d053`.

No source/index writes, retrieval measurements, paid calls, commits or image generation occurred. This is a read-only scout with an in-memory source proposal, not an accepted change. No schema, parser, runtime, weight, affected dimension, eligibility, activation or guard change is proposed. Existing authored situational poverty context and nonidentifying adult boundaries are preserved; no personal worth, identity, economic status or hidden biography is inferred from appearance.

A later authorized promotion would need the usual dictionary/index validation because the dictionary label changes. It must not convert this scout's controlled surface preservation into a natural-retrieval, final-adoption, composed-prose or pixel claim.

## Artifacts

- `source-inventory-and-decisions.json`: exact 12 rows, original proposal pointers, source ledger records, semantic and bundle bindings, per-row reasons
- `frozen-proposal-and-unmeasured-probes.json`: exact one-field before/proposed row and immutable unmeasured probes
- `proposed-only.patch`: unapplied single-line source patch
- `generated-contract.json`: original synthetic generated contract
- `before-actual-v6.json`, `proposed-actual-v6.json`: full actual packs plus verified details/overviews
- `surface-summary.json`: preserved fields, candidate/full-pack equality and scope
- `twelve-source-compatibility-checks.json`: strict adult-subject compatibility checks

The initial row-hash comparison used compact JSON while the coverage map uses standard JSON separators. It was corrected to the map producer's exact recipe; source/proposal/probe bytes and expectations did not change, and no retrieval was run. This was a scout assertion correction, not a repository defect.
