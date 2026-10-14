"""Request-local roles; persistent slot membership is never required."""
import copy
import photo_candidate_corpus as c
import photo_global_index as index
import photo_slot_semantics as semantics
import photo_candidate_realizations as realizations


def propose(data, slot, cid, eligible_bindings, declared_bindings=None, *, realization_ids=None):
    compatible = sorted(eligible_bindings)
    preferred = [bid for bid in compatible if data['slot_bindings'][bid]['slot_id'] == slot]
    declared = [bid for bid in (declared_bindings if declared_bindings is not None else data['slot_bindings'])
                if data['slot_bindings'][bid]['candidate_id'] == cid
                and data['slot_bindings'][bid]['slot_id'] == slot]
    bid = (preferred or sorted(declared) or [None])[0]
    original = data['slot_bindings'][bid] if bid else None
    reader=data.get('_search_reader')
    record=reader.meta['guards'][cid] if reader is not None else data['candidates'][cid]
    positive = reader.meta['positive_blobs'][cid] if reader is not None else ' '.join(
        text for field in index.fields(record).values() for text in field)
    ids = realizations.ids(record) if realization_ids is None else list(realization_ids)
    if not ids:raise ValueError('no eligible realization for role proposal')
    choices=[]
    for rid in ids:
        effects=realizations.effects(record,rid)
        fit=semantics.fit(data['slot_catalog'][slot],{**record,'effects':effects},positive,
                          realization_id=rid)
        choices.append(({'eligible':0,'review_required':1,'incompatible':2}[fit['status']],rid,fit,effects))
    _,rid,fit,effects=min(choices,key=lambda row:(row[0],row[1]))
    if declared and not preferred:
        fit.update(status='incompatible', reason='declared_role_conditions_not_satisfied')
    value = {'schema': 'photo-request-role-proposal/v3', 'target_slot_id': slot, 'candidate_id': cid,
             'source_binding_id': bid, 'eligible_source_binding_ids': compatible,
             'effects': effects, 'conditions': copy.deepcopy(record['conditions']),
             'role_conditions': copy.deepcopy(original['conditions'] if original else {'subject_applicability': {}}),
             'semantic_fit': fit,
             'realization_id':rid, 'eligible_realization_ids':ids,
             'source_record_sha256': reader.meta['record_sha256'][cid] if reader is not None else c.digest(record),
             'applicability_status': fit['status'], 'semantic_role': fit['semantic_role'],
             'adoption': 'optional', 'scope': 'request', 'persistent_tag_write': False}
    value['proposal_id'] = 'role_' + c.digest(value)[:32]
    return value


def entry(data, proposal):
    return c.entry(data, proposal['candidate_id'], proposal['source_binding_id'],
                   realization_id=proposal['realization_id'])


def validate(data, proposal, eligible_bindings):
    expected = propose(data, proposal['target_slot_id'], proposal['candidate_id'], eligible_bindings,
                       realization_ids=proposal['eligible_realization_ids'])
    if proposal != expected:
        raise ValueError('role proposal changed authored conditions/effects/owner')
    return entry(data, proposal)
