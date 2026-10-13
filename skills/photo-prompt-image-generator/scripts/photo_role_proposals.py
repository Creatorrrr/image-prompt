"""Request-local roles; persistent slot membership is never required."""
import copy
import photo_candidate_corpus as c


def propose(data, slot, cid, eligible_bindings):
    compatible = sorted(eligible_bindings)
    preferred = [bid for bid in compatible if data['slot_bindings'][bid]['slot_id'] == slot]
    bid = (preferred or compatible or [None])[0]
    original = data['slot_bindings'][bid] if bid else None
    effects = copy.deepcopy(original['effects'] if original else data['candidates'][cid]['effects'])
    target = set(data['slot_catalog'][slot]['dimensions'])
    fit = bool(target and target & set(effects['dimensions']))
    value = {'schema': 'photo-request-role-proposal/v1', 'target_slot_id': slot, 'candidate_id': cid,
             'source_binding_id': bid, 'eligible_source_binding_ids': compatible,
             'effects': effects, 'conditions': copy.deepcopy(original['conditions'] if original else {}),
             'source_record_sha256': c.digest(data['candidates'][cid]),
             'applicability_status': 'eligible' if fit else 'review_required',
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
