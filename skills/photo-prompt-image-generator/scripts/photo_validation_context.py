"""Core-derived validation contracts. No candidate retrieval or augmentation.

The historical workflow transport still calls this artifact ``pack``; its wire
type is deliberately distinct from a native candidate pack. Old packs keep the
old compiler, receipt and audits. New H-F2 runs compile only validation inputs.
"""
import copy
import photo_candidate_corpus as corpus

SCHEMA = 'photo-validation-context/v1'
FORBIDDEN = {'candidate_pool', 'candidate_bindings', 'role_views', 'role_proposals',
             'creative_augmentation', 'photographic_integration', 'photographic_craft',
             'visual_proposition', 'artistic_final_touch', 'quality_profile'}


def is_context(value):
    return isinstance(value, dict) and value.get('contract_version') == SCHEMA


def validate(value):
    if not is_context(value) or FORBIDDEN & set(value):
        raise ValueError('invalid core validation context or legacy candidate payload')
    if value.get('pack_id') != corpus.digest(dict(value, pack_id=None))[:16]:
        raise ValueError('validation context content changed')
    for key in ('authorial_core', 'creative_controls', 'embodiment_preflight',
                'intent_preservation', 'authorial_composition', 'negative_intent_guard',
                'global_retrieval', 'provenance'):
        if not isinstance(value.get(key), dict):
            raise ValueError('missing validation contract: ' + key)
    return value


def build(data, core, controls, embodiment):
    import prompt_generator as g
    import photo_shared_views
    if hasattr(data, 'for_core'):
        data = data.for_core(core)
    result = g.prepare_candidate_source(data, core, controls, embodiment)
    result['provenance']['global_candidate_ids'] = []
    trace = result['semantic_trace']
    contract = trace['generation_contract']
    # Policy/meaning compilation may inspect source rules, never optional role
    # inventories. No native slot retrieval or candidate-pack compiler is called.
    rules = photo_shared_views.RequestCandidates(data, (), {})
    character = g.compile_character_response_contract(core, data=rules)
    resolution = g.candidate_pack_resolve_visual_profiles(rules, result, trace, character)
    obligations = g.candidate_pack_visual_obligations(rules, result, trace, character, resolution)
    clarification = g.candidate_pack_semantic_clarification(rules, result, trace, obligations, None, resolution)
    mandatory, uncovered = g.candidate_pack_mandatory_intents(result, trace, {})
    provenance = copy.deepcopy(result['provenance'])
    provenance['retrieval_query'] = g.authorial_core_retrieval_text(core)[1]
    provenance.pop('authorial_core', None)
    provenance.pop('embodiment_preflight', None)
    provenance.pop('candidate_pool_creativity', None)
    provenance.pop('global_candidate_ids', None)
    provenance['embodiment_preflight_required'] = True
    lock = core['intent_lock']
    policy = {'contract_version': g.AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION,
              'source_authorial_core_sha256': core['canonical_sha256'],
              'source_intent_lock_sha256': lock['canonical_sha256'],
              'allowed_dimensions': copy.deepcopy(lock['open_dimensions']),
              'minimum_authorial_decisions': 0, 'minimum_preserved_evidence_phrases': 0,
              'dimension_policy': 'distinct_open_dimensions_only',
              'insufficient_freedom_policy': 'do_not_invent_open_dimensions'}
    policy['canonical_sha256'] = corpus.digest(policy)
    binding = {'composed_field': 'authorial_core_binding',
               'minimum_preserved_evidence_phrases': 0, 'minimum_authorial_decisions': 0,
               'evidence_must_be_literal_in_baseline_and_final_prompt': True,
               'source_intent_lock_sha256_required': True, 'all_semantic_anchor_ids_required': True,
               'authorial_decisions_limited_to_open_dimensions': True,
               'contract_version': g.AUTHORIAL_CORE_BINDING_CONTRACT_VERSION,
               'source_authorship_policy_sha256': policy['canonical_sha256']}
    source = {'contract_version': 'photo-validation-source/v1',
              'corpus_sha256': data['_search_reader'].meta['corpus_sha256'],
              'core_sha256': core['canonical_sha256'], 'controls_sha256': controls['canonical_sha256']}
    source['canonical_sha256'] = corpus.digest(source)
    context = {'contract_version': SCHEMA, 'pack_id': None,
               'authorial_core': copy.deepcopy(core), 'creative_controls': copy.deepcopy(controls),
               'provenance': provenance, 'global_retrieval': source,
               'negative_en': result['negative_en'], 'negative_intent_guard': result['negative_intent_guard'],
               'embodiment_preflight': result['provenance']['embodiment_preflight'],
               'mandatory_intents': mandatory, 'uncovered_intents': uncovered,
               'intent_contract': g.candidate_pack_intent_contract(rules, result, trace, {}),
               'coverage': {'intent_constraints': copy.deepcopy(contract.get('intent_constraints', {}))},
               'safety': copy.deepcopy(contract.get('safety') or {'mode': 'automatic', 'evaluation_requested': False, 'status': 'pass', 'requires_user_approval': False, 'items': []}),
               'authorial_composition': {'enabled': True, 'prompt_budget': g.authorial_prompt_budget_contract(),
                                         'authorship_policy': policy, 'core_binding_contract': binding},
               'intent_preservation': {'contract_version': g.INTENT_PRESERVATION_CONTRACT_VERSION,
                   'source_authorial_core_sha256': core['canonical_sha256'],
                   'source_intent_lock_sha256': lock['canonical_sha256'],
                   'priority_order': ['requesting_user_definition', 'requesting_user_semantic_anchor',
                                      'requesting_user_modifier_or_exclusion', 'agent_prepack_interpretation',
                                      'creative_augmentation'],
                   'required_anchor_ids': [row['anchor_id'] for row in lock['semantic_anchors']],
                   'locked_dimensions': copy.deepcopy(lock['locked_dimensions']),
                   'open_dimensions': copy.deepcopy(lock['open_dimensions']),
                   'material_change_action': 'stop_and_rebuild_core_after_requester_input',
                   'creative_change_boundary': 'open_dimensions_only_and_subordinate'},
               'adult_appeal': g.candidate_pack_contextual_adult_appeal(rules, result, {}, authorial_core=core)}
    optional = {'character_response': character, 'visual_obligations': obligations,
                'semantic_clarification': clarification,
                'semantic_assertion_obligations': g.compile_semantic_assertion_obligations(core),
                'render_repair': g.compile_render_repair_contract(core),
                'creative_direction': g.candidate_pack_creative_direction(result),
                'viewer_experience': g.candidate_pack_viewer_experience(result)}
    context.update({key: value for key, value in optional.items() if value is not None})
    context['pack_id'] = corpus.digest(context)[:16]
    return validate(context)


def audit(context, composed, source_data):
    """Reuse core/meaning/physical validators without native candidate stages."""
    import audit_composed_prompt as ca
    validate(context)
    failures, warnings = [], []
    if not isinstance(composed, dict):
        return {'status': 'fail', 'quality_status': 'pass', 'pack_id': context['pack_id'],
                'failures': [{'check': 'output_contract', 'reason': 'composed prompt must be an object'}], 'warnings': []}
    prompt = composed.get('prompt_en', '')
    for key in ('pack_id', 'prompt_en', 'negative_en', 'composer', 'chosen_candidate_ids', 'chosen_visual_concept_ids'):
        if key not in composed:
            failures.append({'check': 'output_contract', 'reason': 'missing ' + key})
    if composed.get('pack_id') != context['pack_id'] or composed.get('composer') != 'agent' or not isinstance(prompt, str) or not prompt.strip():
        failures.append({'check': 'output_contract', 'reason': 'invalid identity, composer or prompt'})
    if not isinstance(prompt, str):
        prompt = ''
    if composed.get('negative_en') != context['negative_en']:
        failures.append({'check': 'negative_en', 'reason': 'negative text differs from frozen policy'})
    if composed.get('global_retrieval_sha256') != context['global_retrieval']['canonical_sha256']:
        failures.append({'check': 'global_retrieval_binding', 'reason': 'validation source binding changed'})
    if composed.get('chosen_candidate_ids') or composed.get('creative_augmentation_brief'):
        failures.append({'check': 'candidate_authority', 'reason': 'H-F2 material is not native adoption authority'})
    for key in ('chosen_candidate_ids', 'chosen_visual_concept_ids'):
        if not isinstance(composed.get(key), list) or any(not isinstance(cid, str) for cid in composed[key]):
            failures.append({'check': 'output_contract', 'reason': key + ' must be an explicit string list'})
    for check in (ca.audit_negative_intent_guard, ca.audit_creative_direction,
                  ca.audit_character_response_v8, ca.audit_semantic_assertion_obligations_v8,
                  ca.audit_render_repair_v8, ca.photo_embodiment.audit_composed,
                  ca.audit_visual_obligations, ca.audit_viewer_experience,
                  ca.audit_semantic_clarification):
        if check == ca.audit_negative_intent_guard:
            failures.extend(check(context, prompt))
        elif check == ca.photo_embodiment.audit_composed:
            failures.extend(check(context, composed))
        else:
            failures.extend(check(context, composed, prompt))
    failures.extend(ca.audit_authorial_core(context, composed, prompt, warnings))
    adult_failures, adult_warnings = ca.audit_adult_appeal(context, composed, prompt, set(), {})
    failures.extend(adult_failures); warnings.extend(adult_warnings)
    if context['safety'].get('status') != 'pass' or context['safety'].get('requires_user_approval'):
        failures.append({'check': 'safety', 'reason': 'source safety contract is not pass'})
    assertions = composed.get('coverage_assertions')
    if assertions is not None:
        mandatory_texts = {row.get('text') for row in context['mandatory_intents']}
        if not isinstance(assertions, dict):
            failures.append({'check': 'coverage_assertions', 'reason': 'coverage assertions must be an object'})
        else:
            for key, raw in assertions.items():
                if key not in mandatory_texts or any(not ca.text_contains_term(prompt, phrase) for phrase in ca.assertion_values(raw)):
                    failures.append({'check': 'coverage_assertions', 'reason': 'unknown intent or nonliteral evidence', 'intent': key})
    if composed.get('candidate_interpretations') or 'owner_selections' in composed:
        failures.append({'check': 'candidate_authority', 'reason': 'validation context has no native candidate/owner selections'})
    for intent in context['mandatory_intents']:
        if not any(ca.text_contains_term(prompt, term) for term in ca.assertion_terms_for_intent(intent, composed)):
            failures.append({'check': 'mandatory_intent', 'reason': 'missing requester intent', 'intent': intent.get('text')})
        elif intent.get('status') == 'uncovered':
            warnings.append({'check': 'uncovered_intent', 'reason': 'uncovered intent preserved by authored evidence', 'intent': intent.get('text')})
    effective, effective_failures = ca.derive_effective_visual_obligation_contract(context, composed)
    failures.extend(effective_failures)
    return {'status': 'fail' if failures else 'pass', 'quality_status': 'warn' if warnings else 'pass',
            'pack_id': context['pack_id'], 'validation_context_version': SCHEMA,
            'chosen_candidate_count': 0,
            'chosen_visual_concept_ids': (effective or {}).get('selected_visual_concept_ids', []),
            'effective_visual_contract_sha256': ca.effective_visual_obligation_sha256(effective),
            'render_repair_contract_sha256': (context.get('render_repair') or {}).get('canonical_sha256'),
            'failures': failures, 'warnings': warnings}
