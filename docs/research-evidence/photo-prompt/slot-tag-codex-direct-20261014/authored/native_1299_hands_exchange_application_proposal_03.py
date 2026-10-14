"""Root-authored alternative; no source selection, proof or operating change."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
parent_path = HERE / 'native_1299_hands_exchange_application_proposal_02.json'
parent = json.loads(parent_path.read_bytes())
before = copy.deepcopy(parent['whole_before_source'])
after = copy.deepcopy(parent['whole_proposed_after_source'])
after['content']['en'] = 'Macro framing of existing hands physically handing off one existing item, with only their hands visible as participant anatomy.'
after['content']['ko'] = '기존 물체 하나를 실제로 주고받는 여러 기존 손의 매크로 구도. 참여자의 신체 부위는 그 손들만 보인다.'
after['content']['application_contract'] = (
    'This revised candidate deliberately selects one bounded physical-handoff application of the former ambiguous exchange label. '
    'It does not claim that the old label uniquely established an item handoff, and it does not qualify gesture-only or information exchanges. '
    'Use one independently declared existing initiating hand, the complete nonempty independently declared existing other-hands scope, '
    'and one independently declared existing generic physical item. Select these exact targets from the frozen request/input/core before discovery. '
    'Each hand must have independently declared entity presence and the exact entity.type/v1 value hand. '
    'The item must have independent entity presence and the exact entity.kind/v1 value physical_item. '
    'The initiating hand must be explicitly disjoint from each other hand, and the item explicitly disjoint from every hand. '
    'These are application prerequisites, not new entities, a fixed anatomical count, a subtype inferred from a label or a category-to-owner default. '
    'Retain every independently declared ownership and part relationship. Neither human identity, a common carrier nor different people is required. '
    'Select macro shot scale and hands-only participant framing. Only the participating hands are visible as participant anatomy; '
    'the existing item remains visible, and this does not require deletion of unrelated background. '
    'Perform the physical handoff in progress on the selected item with every selected hand as an actual receiver. '
    'Keep that performed action as an effect rather than a frozen-action prerequisite, context or preservation. '
    'Both image framing effects require the separately selected complete framing_affected_owners inventory. '
    'That inventory must already be explicitly authored from all actual frozen request inputs before discovery, with exact existing presence for every member. '
    'It must name every actual owner affected by this macro coverage and crop, including the selected item and hands and each separately declared affected carrier, '
    'body region or other scene object. Its membership must be directly reviewed against the actual request, topology and selected framing. '
    'An inventory label, complete flag, hash or successful selector validation does not establish that semantic completeness. '
    'Do not invent a carrier, equate a hand with its carrier, infer descendants or construct this inventory from a discovered candidate. '
    'Both framing effects have the item, every selected hand and every member of that complete framing inventory as actual receivers. '
    'The independent framing scope may overlap the explicitly repeated hand/item endpoints; expand the exact union without inventing another entity or omitting an actual receiver. '
    'If any affected carrier or body region cannot be independently addressed and included, this application is not eligible. '
    'Apply all actual owner, ancestor, partial-property and whole-dimension locks to this complete union. '
    'No exact finger pose, contact configuration, support geometry, item coordinate, trajectory, completed ownership transfer, item subtype, '
    'camera hardware, focal length, focus plane or depth of field is selected here. If an actual selected application adds any such mutation, '
    'it requires its own complete source/effect/receiver review before use. Preserve independent identity and topology.'
)
for rule in after['conditions']['native_guards']['rules']:
    value_rule = rule.get('rule', rule)
    if value_rule.get('kind') == 'frozen_value':
        assert value_rule['property'] == 'body.part.kind'
        value_rule['property'] = 'entity.type'
        value_rule['value'] = {'type': 'entity.type/v1', 'value': 'hand'}
owner_map = copy.deepcopy(parent['owner_map_intent_not_native_proof'])
owner_map['bindings'].append({
    'target': 'framing_affected_owners', 'origin': 'existing', 'introduced_by': None,
    'selector': {'kind': 'selected_existing_member_scope', 'scope_schema': 'photo-frozen-existing-member-scope/v1',
                 'target_semantics': 'each_member', 'receiver_semantics': 'all_members'},
})
intents = copy.deepcopy(parent['manual_P_E_intent_not_native_proof'])
for fact in intents:
    fact.pop('quote', None)
    fact['new_quote_review_required'] = True
    if fact['property'] == 'body.part.kind':
        fact['property'] = 'entity.type'
        fact['value'] = {'type': 'entity.type/v1', 'value': 'hand'}
        fact['protocol'] = 'Explicit source-defined hand type; not a common presence default or inferred anatomy.'
    if fact['mode'] == 'effect' and fact['dimension'] == 'framing':
        fact['receivers'].append('framing_affected_owners')
intents.append({'dimension': 'subject', 'target': 'framing_affected_owners', 'property': 'entity.presence',
                'mode': 'prerequisite', 'value': {'type': 'entity.presence/v1', 'value': 'present'},
                'protocol': 'Exact common presence for each independently declared scope member; no new owner.',
                'new_quote_review_required': True})
digest = lambda value: hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
proposal = {
    'schema': 'photo-root-bounded-source-application-proposal/v1', 'actor': '/root', 'ordinal': 1299,
    'candidate_id': before['id'], 'status': 'unselected_proposal_requires_fresh_direct_review',
    'parent': {'file': str(parent_path.relative_to(HERE.parents[4])), 'raw_sha256': hashlib.sha256(parent_path.read_bytes()).hexdigest()},
    'whole_before_source': before, 'whole_proposed_after_source': after,
    'before_source_sha256': digest(before), 'proposed_after_source_sha256': digest(after),
    'exact_top_delta': [{'pointer': '/' + key, 'before': before.get(key), 'after': after.get(key)}
                        for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)],
    'owner_map_intent_not_native_proof': owner_map,
    'manual_P_E_intent_not_native_proof': intents,
    'root_actual_code_read_boundary': [
        'photo_semantic_evidence.py _collect_permission_scope and property_scope_allowed',
        'photo_contracts.py property_effects_allowed',
        'precore/photo_semantic_witnesses.py validate_graph, owner_relation and validate_existing_member_scopes',
        'photo_native_owner_resolution.py actual point/scope selection and every effect receiver expansion',
    ],
    'root_actual_spec_read': ['shot_scale', 'subject_framing', 'relational_action', 'action', 'composition',
                              'camera_distance', 'lens', 'depth_of_field', 'hand_pose', 'contact_point', 'prop', 'prop_state'],
    'source_choice_boundary': 'The revised EN/KO make the physical-handoff restriction explicit. It is a proposed editorial correction, not preservation of every possible original interpretation. Root has not selected or applied it.',
    'scope_boundary': 'The existing member-scope protocol checks input provenance and exact frozen membership, not semantic completeness. This proposal requires explicit manual completeness review and adds no automatic owner closure, global wildcard or permission waiver.',
    'required_fresh_checks': [
        'Whole original/current/binding/proposal/fullspec read; exact source03 clauses and every P/PR/E/context fact need new source-local quotes.',
        'Demonstrate actual source-qualified point plus plural member scopes, typed hand/item witnesses and complete framing union on frozen50fd92.',
        'Check different and same carriers, explicit owned non-hand regions, overlapping exact Rx unions, all receiver and ancestor property locks and whole-dimension locks.',
        'Reject missing/stale/incomplete selections and scopes, nonexistent or omitted endpoints, introduced items and candidate-created membership; inspect semantic completeness independently.',
        'Full/compact/admission/role/permission/compose/runtime parity before qualification; no shape-to-truth claim.',
    ],
    'source_or_catalog_or_binding_changed': False, 'native_proof_created': False,
    'root_source_selection': False, 'operating_changes': 0, 'Gemini_or_model_or_network_calls': 0,
}
output = HERE / 'native_1299_hands_exchange_application_proposal_03.json'
with output.open('x') as stream:
    json.dump(proposal, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'proposal': str(output), 'raw_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                  'after_source_sha256': digest(after), 'selected': False, 'native_proof_created': False}))
