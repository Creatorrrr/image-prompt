"""Request-local roles; persistent slot membership is never required."""
import copy
import photo_candidate_corpus as c
import photo_global_index as index
import photo_slot_semantics as semantics


def propose(data, slot, cid, eligible_bindings, declared_bindings=None):
    compatible = sorted(eligible_bindings)
    preferred = [bid for bid in compatible if data['slot_bindings'][bid]['slot_id'] == slot]
    declared = [bid for bid in (declared_bindings if declared_bindings is not None else data['slot_bindings'])
                if data['slot_bindings'][bid]['candidate_id'] == cid
                and data['slot_bindings'][bid]['slot_id'] == slot]
    bid = (preferred or sorted(declared) or [None])[0]
    original = data['slot_bindings'][bid] if bid else None
    reader=data.get('_search_reader')
    record=reader.meta['guards'][cid] if reader is not None else data['candidates'][cid]
    effects = copy.deepcopy(record['effects'])
    positive = reader.meta['positive_blobs'][cid] if reader is not None else ' '.join(
        text for field in index.fields(record).values() for text in field)
    fit = semantics.fit(data['slot_catalog'][slot], record, positive)
    if declared and not preferred:
        fit.update(status='incompatible', reason='declared_role_conditions_not_satisfied')
    value = {'schema': 'photo-request-role-proposal/v2', 'target_slot_id': slot, 'candidate_id': cid,
             'source_binding_id': bid, 'eligible_source_binding_ids': compatible,
             'effects': effects, 'conditions': copy.deepcopy(record['conditions']),
             'role_conditions': copy.deepcopy(original['conditions'] if original else {'subject_applicability': {}}),
             'semantic_fit': fit,
             'source_record_sha256': reader.meta['record_sha256'][cid] if reader is not None else c.digest(record),
             'applicability_status': fit['status'], 'semantic_role': fit['semantic_role'],
             'adoption': 'optional', 'scope': 'request', 'persistent_tag_write': False}
    value['proposal_id'] = 'role_' + c.digest(value)[:32]
    return value


def entry(data, proposal):
    return c.entry(data, proposal['candidate_id'], proposal['source_binding_id'])


def validate(data, proposal, eligible_bindings):
    expected = propose(data, proposal['target_slot_id'], proposal['candidate_id'], eligible_bindings)
    if proposal != expected:
        raise ValueError('role proposal changed authored conditions/effects/owner')
    return entry(data, proposal)
