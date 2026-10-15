"""Request-local roles; persistent slot membership is never required."""
import copy
import photo_candidate_corpus as c
import photo_global_index as index
import photo_slot_semantics as semantics
import photo_candidate_realizations as realizations
import photo_semantic_evidence as evidence


def propose(data, slot, cid, eligible_bindings, declared_bindings=None, *, realization_ids=None,
            dependency_selections=None):
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
        effects=(evidence.effect_set(record,rid) if evidence.native_status(record)=='qualified'
                 else realizations.effects(record,rid))
        fit=semantics.fit(data['slot_catalog'][slot],record,positive,
                          realization_id=rid,source_data=data)
        choices.append(({'eligible':0,'review_required':1,'incompatible':2}[fit['status']],rid,fit,effects))
    _,rid,fit,effects=min(choices,key=lambda row:(row[0],row[1]))
    if declared and not preferred:
        fit.update(status='incompatible', reason='declared_role_conditions_not_satisfied')
    if any(c.binding_review_status(data, key) == 'deferred' for key in declared):
        fit.update(status='incompatible', reason='declared_role_semantic_review_deferred')
    if c.deferred_dependency_bindings(data, record):
        fit.update(status='incompatible', reason='dependency_binding_semantic_review_deferred')
    dependency_choices = {}; effect_closure = []
    if evidence.native_status(record) == 'qualified':
        proof = (record['_semantic_evidence_guard'] if '_semantic_evidence_guard' in record
                 else evidence.compact(record, data))
        dependency_choices = evidence.dependency_choices(proof, rid)
        selections = dependency_selections or {}
        if not isinstance(selections, dict) or not set(selections) <= set(dependency_choices):
            raise ValueError('role proposal contains foreign dependency selections')
        descriptor=evidence.owner_selection_descriptors(proof,rid)
        try:
            effect_closure = evidence.effect_closure(cid, proof, rid, selections)
            if fit['status']!='incompatible' and descriptor is not None and evidence.pending_owner_selection(c.entry(data,cid,realization_id=rid,dependency_selections=selections)):
                fit.update(status='review_required',reason='explicit_existing_owner_selection_required')
        except ValueError:
            if fit['status'] != 'incompatible':
                fit.update(status='review_required', reason='actual_dependency_realization_selection_required')
    value = {'schema': 'photo-request-role-proposal/v4', 'target_slot_id': slot, 'candidate_id': cid,
             'native_qualification':fit['native_qualification'],
             'dependency_selections':copy.deepcopy(dependency_selections or {}),
             'dependency_choices':dependency_choices, 'native_effect_closure':effect_closure,
             'source_binding_id': bid, 'eligible_source_binding_ids': compatible,
             'effects': effects, 'conditions': copy.deepcopy(record['conditions']),
             'role_conditions': copy.deepcopy(original['conditions'] if original else {'subject_applicability': {}}),
             'semantic_fit': fit,
             'realization_id':rid, 'eligible_realization_ids':ids,
             'source_record_sha256': reader.meta['record_sha256'][cid] if reader is not None else c.digest(record),
             'applicability_status': fit['status'], 'semantic_role': fit['semantic_role'],
             'adoption': 'optional', 'scope': 'request', 'persistent_tag_write': False}
    if evidence.native_status(record)=='qualified' and descriptor is not None:
        value['owner_selection_requirements']=descriptor
    value['proposal_id'] = 'role_' + c.digest(value)[:32]
    return value


def entry(data, proposal,*,owner_selections=None):
    return c.entry(data, proposal['candidate_id'], proposal['source_binding_id'],
                   realization_id=proposal['realization_id'], dependency_selections=proposal['dependency_selections'],owner_selections=owner_selections)


def validate(data, proposal, eligible_bindings):
    expected = propose(data, proposal['target_slot_id'], proposal['candidate_id'], eligible_bindings,
                       realization_ids=proposal['eligible_realization_ids'],
                       dependency_selections=proposal['dependency_selections'])
    if proposal != expected:
        raise ValueError('role proposal changed authored conditions/effects/owner')
    return entry(data, proposal)
