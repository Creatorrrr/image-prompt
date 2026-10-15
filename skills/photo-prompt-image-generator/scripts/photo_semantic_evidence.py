"""Manually authored native facts; semantic support is distinct from mutation.

Absent proof remains explicitly unqualified during stage 5C, never a native
completion/adoption certificate. Present older/invalid proof fails closed.
"""
from __future__ import annotations
import copy
import contextlib
import contextvars
import photo_native_owner_resolution as owner_resolver
import photo_semantic_role_views as manual_views
import photo_native_permission as permission_envelope
import photo_candidate_corpus as c
import photo_candidate_realizations as realizations
from photo_precore_bridge import load
witnesses = load('photo_semantic_witnesses')

SCHEMA = 'photo-candidate-role-evidence/v4'
OWNER_SCHEMA = 'photo-native-owner-bindings/v2'
SELECTOR_OWNER_SCHEMA = 'photo-native-owner-bindings/v3'
MEMBER_OWNER_SCHEMA = 'photo-native-owner-bindings/v4'
MEMBER_SELECTION_SCHEMA = 'photo-request-owner-selections/v2'
MEMBER_GUARD_SCHEMA = 'photo-native-source-guards/v3'
_ACTIVE_RESOLUTION = contextvars.ContextVar('native_selected_resolution',default=None)
OWNER_SELECTION_SCHEMA = 'photo-request-owner-selections/v1'
MAX_OWNER_SELECTION_ENTRIES = 64
MODES = frozenset({'effect', 'prerequisite', 'preservation', 'context'})
OPERATIONS = frozenset({'set_value', 'add_entity', 'remove_entity', 'relocate', 'select_plane'})
NEGATIVE = frozenset({'confusion_boundaries', 'research_confusions', 'confounders',
    'failure_modes', 'excluded', 'exclusions', 'forbidden', 'avoid', 'negative',
    'research_source_urls', 'tags', 'facets', 'reject_substitutes', 'contrast_examples',
    'forbidden_prompt_terms', 'runtime_forbidden_labels', 'claim_limits', 'research_claim_limits',
    'provenance', 'acceptance', 'review', 'routing', 'conditions', 'applicability', 'retrieval_policy',
    'role_evidence', 'semantic_review', 'permission_envelope', 'affected_dimensions', 'affected_properties',
    'dimensions', 'properties', 'field', 'review_scale', 'evidence_field', 'evidence_fields', 'required_evidence_fields',
    'contract_version', 'schema', 'activation', 'match_terms', 'any_terms', 'all_terms',
    'evidence_terms', 'must_mention_any', 'context_terms', 'project_glossary_aliases',
    'aliases', 'keywords', 'terms', 'concept_terms', 'exact_terms', 'id', 'ids', 'candidate_id', 'candidate_ids', 'binding_id', 'source_candidate_id', 'family_ids', 'family_id', 'topic_ids', 'topic_id',
    'priority_dimension', 'priority_dimensions', 'selection_contract', 'profile_activation',
    'adoption', 'source_sha256', 'associated_profile_ids', 'schema_version'})
PROPERTY_FIELDS = ('dimension', 'target', 'property')
FACT_FIELDS = frozenset({'id', 'realization_id', 'pointer', 'quote', 'dimension', 'target',
                         'property', 'mode', 'value', 'requires'})
PROOF_FIELDS = frozenset({'schema', 'meaning_sha256', 'catalog_sha256', 'complete', 'facts',
                         'roles', 'owner_maps', 'source_units', 'effect_sets', 'review',
                         'dependencies', 'reference_sha256', 'guard_sets', 'profile_contracts'})
POSITIVE_FIELDS = frozenset({'en', 'ko', 'ja', 'phrase_en', 'phrase_ko', 'embedding_text', 'concept_units', 'relations',
    'definition', 'definitions_by_topic', 'paraphrases', 'manifestations', 'components',
    'semantics', 'authored_components', 'composition_instruction', 'concept_candidate',
    'render_requirements', 'render_gates', 'render_hard_gates', 'application_contract'})
MISSING = object()
MAX_FACTS = 4096
MAX_UNITS = 2048
MAX_REALIZATIONS = 32
MAX_DEPENDENCY_DEPTH = 8
GUARD_SUPPORT_SCHEMA = 'photo-native-guard-role-support/v1'
MAX_GUARD_SUPPORTS = 512
MAX_RID_GUARD_SUPPORTS = 64
GUARD_SUPPORT_FIELDS = frozenset({'schema','id','realization_id','pointer','quote','mode',
    'guard','endpoints','semantic_projection'})
SOURCE_UNIT_FIELDS = frozenset({'realization_id', 'pointer', 'quote', 'fact_refs', 'disposition'})
REFERENCE_UNIT_FIELDS = SOURCE_UNIT_FIELDS | {'reference_relation', 'retained_constraint_rationale'}
REFERENCE_RELATIONS = frozenset({'partial_restatement', 'selected_output_constraint', 'same_selected_owner'})


def _proof_fields_valid(proof):
    return PROOF_FIELDS <= set(proof) <= PROOF_FIELDS | {'guard_supports','manual_role_views','permission_envelopes'}


def _guard_support_rows(proof):
    if 'guard_supports' not in proof:
        return []
    rows=proof['guard_supports']
    if not isinstance(rows,list) or not 1<=len(rows)<=MAX_GUARD_SUPPORTS:
        raise ValueError('bounded nonempty explicit guard supports required')
    return rows


def _guard_support_rule(proof,row):
    """Exact own-source common/branch locator; presentation cannot self-certify."""
    rid=row['realization_id'];ref=row['guard'];cid=_proof_cid(proof)
    fields={'schema','declaring_candidate_id','declaring_realization_id',
        'source_condition_index','conditions_sha256','rule_id','rule_sha256'}
    if (not isinstance(ref,dict) or set(ref)!=fields or ref['declaring_candidate_id']!=cid
            or ref['declaring_realization_id']!=rid or type(ref['source_condition_index']) is not int
            or ref['source_condition_index'] not in (0,1)
            or not _sha256(ref['conditions_sha256']) or not _sha256(ref['rule_sha256'])):
        raise ValueError('guard support requires exact own CID/RID/source condition locator')
    cond=proof['guard_sets'][rid]['source_conditions'][ref['source_condition_index']]
    block=cond.get('native_guards')
    if not isinstance(block,dict) or ref['schema']!=block.get('schema'):
        raise ValueError('guard support schema differs from actual source guard')
    validate_source_guards(block)
    rules=[rule for rule in block['rules'] if rule['id']==ref['rule_id']]
    if (len(rules)!=1 or c.digest(cond)!=ref['conditions_sha256']
            or c.digest(rules[0])!=ref['rule_sha256']
            or ref['schema'] not in {SOURCE_GUARD_SCHEMA,SOURCE_TARGET_GUARD_SCHEMA}
            or rules[0]['kind'] not in {'owner_relation','frozen_entity_relation'}):
        raise ValueError('guard support source condition/rule changed or unsupported predicate')
    return rules[0]


def _validate_guard_supports(proof, *, record=None):
    """A manual relation projection is not a scalar frozen fact or a mutation."""
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    rows=_guard_support_rows(proof)
    if not rows:return {}
    result={};counts={};cid=_proof_cid(proof)
    compact='dependency_guards' in proof
    expected=GUARD_SUPPORT_FIELDS-({'pointer','quote'} if compact else set())
    fact_ids={fact['id'] for fact in proof['facts']}
    for row in rows:
        if (not isinstance(row,dict) or set(row)!=expected or row['schema']!=GUARD_SUPPORT_SCHEMA
                or not concrete_owned_value(row['id']) or row['id'] in result or row['id'] in fact_ids
                or not concrete_owned_value(row['realization_id'])
                or row['realization_id'] not in proof['effect_sets'] or row['mode']!='prerequisite'):
            raise ValueError('invalid/duplicate guard support or non-prerequisite mode')
        rid=row['realization_id'];counts[rid]=counts.get(rid,0)+1
        if counts[rid]>MAX_RID_GUARD_SUPPORTS:raise ValueError('too many actual-RID guard supports')
        rule=_guard_support_rule(proof,row);ref=row['guard'];eps=row['endpoints']
        v2=ref['schema']==SOURCE_TARGET_GUARD_SCHEMA
        keys={'left','right'} if v2 else {'left_role','right_role'}
        if not isinstance(eps,dict) or set(eps)!=keys:
            raise ValueError('guard support endpoints must preserve the actual schema keys')
        own_plan=owner_binding_plan(proof['owner_maps'][rid])
        for key,ep in eps.items():
            if (not isinstance(ep,dict) or set(ep)!={'candidate_id','target'}
                    or not isinstance(ep['candidate_id'],str) or not c.ID.fullmatch(ep['candidate_id'])
                    or not concrete_owned_value(ep['target'])):
                raise ValueError('explicit source-owner endpoint required, never actual-owner constants')
            if v2:
                if ep!={k:rule[key][k] for k in ('candidate_id','target')}:
                    raise ValueError('guard support endpoint differs from actual source-target rule')
            elif ep['candidate_id']!=cid:
                raise ValueError('v1 support endpoint must belong to its own source')
            if ep['candidate_id']==cid:
                plan=own_plan.get(ep['target'])
                if plan is None or plan['origin']!='existing':
                    raise ValueError('guard support requires explicitly bound existing endpoints')
                if not v2 and plan['selector_kind']=='core_role' and plan['core_role']!=rule[key]:
                    raise ValueError('v1 endpoint mapping differs from its actual neutral role')
        projection=row['semantic_projection']
        if (not isinstance(projection,dict) or set(projection)!=set(PROPERTY_FIELDS)
                or not all(concrete_owned_value(projection[k]) for k in PROPERTY_FIELDS)
                or projection['dimension'] not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
                or not any(ep=={'candidate_id':cid,'target':projection['target']} for ep in eps.values())):
            raise ValueError('guard support requires explicit owned semantic projection')
        if rule['kind']=='frozen_entity_relation' and any(projection[k]!=rule[k] for k in ('dimension','property')):
            raise ValueError('frozen relation projection cannot rewrite its actual property taxonomy')
        if not compact:
            if not isinstance(row['pointer'],str) or not isinstance(row['quote'],str) or not row['quote'].strip():
                raise ValueError('direct positive guard source anchor required')
            if record is not None and (row['pointer'] not in primary_paths(record,rid)
                    or row['quote'] not in positive_string(record,row['pointer'],realization_id=rid)):
                raise ValueError('guard support differs from its own positive source')
        result[row['id']]=row
    return result


def meaning_material(record):
    return {'id': record['id'], 'record_kind': record['record_kind'],
            'content': {k: v for k, v in record['content'].items()
                        if k not in {'role_evidence', 'semantic_review'}},
            'conditions': record['conditions'], 'effects': record['effects']}


def meaning_sha256(record):
    return c.digest(meaning_material(record))


def property_key(value):
    return tuple(value[key] for key in PROPERTY_FIELDS)


def native_contract_sha256(proof):
    material = {key:value for key,value in proof.items() if key != 'review'}
    review = proof.get('review') or {}
    material['review_bindings'] = {key:review.get(key) for key in ('original_review','source_correction')}
    return c.digest(material)


def _sha256(value):
    return isinstance(value,str) and len(value)==64 and all(ch in '0123456789abcdef' for ch in value)


def concrete_owned_value(value):
    return witnesses.concrete(value)


def proof_of(record):
    if '_semantic_evidence_guard' in record:
        return record['_semantic_evidence_guard']
    return record.get('content', record).get('role_evidence', MISSING)


def native_status(record):
    proof = proof_of(record)
    if proof is MISSING:
        return 'unqualified'
    return 'qualified' if isinstance(proof, dict) and proof.get('schema') == SCHEMA and proof.get('complete') is True else 'invalid'


def positive_string(record, pointer, *, realization_id=None):
    if not isinstance(pointer, str) or not pointer.startswith('/content/'):
        raise ValueError('positive fact requires a primary content pointer')
    keys = [key.replace('~1', '/').replace('~0', '~') for key in pointer[1:].split('/')]
    labels = keys[1:] if keys[1] != 'realization_content' else [keys[1], *keys[3:]]
    if set(labels) & NEGATIVE or any(key.endswith(('_id', '_ids')) for key in labels):
        raise ValueError('negative/routing/review metadata is not positive evidence')
    if keys[1] == 'realization_content' and (len(keys) < 4 or keys[2] != realization_id):
        raise ValueError('fact borrows text from a different actual realization')
    value = record
    try:
        for key in keys:
            if isinstance(value, list):
                if not key.isdigit() or str(int(key)) != key:
                    raise ValueError('noncanonical source index')
                value = value[int(key)]
            else:
                value = value[key]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('missing positive source pointer') from exc
    if not isinstance(value, str):
        raise ValueError('positive pointer must address a complete source string')
    return value


def primary_paths(record, rid):
    """Rendered semantic strings must have an authored whole-source disposition.

    Clause completeness is a manual review judgement, not proved by path coverage.
    """
    result = set()
    def visit(value, pointer):
        if isinstance(value, str) and value.strip():
            result.add(pointer)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                visit(child, pointer+'/'+str(i))
        elif isinstance(value, dict):
            for key, child in value.items():
                if key not in NEGATIVE and not key.endswith(('_id', '_ids')):
                    visit(child, pointer+'/'+key.replace('~', '~0').replace('/', '~1'))
    for key in POSITIVE_FIELDS & set(record['content']):
        visit(record['content'][key], '/content/'+key)
    choices = record['content'].get('realization_content')
    if choices:
        visit(choices[rid], '/content/realization_content/'+rid.replace('~', '~0').replace('/', '~1'))
    return result


def _validate_source_units(record, proof, facts, rid):
    """References retain manual local constraints; only direct units ground facts.

    A reference has one hop to a fact already supported at its exact primary
    field by a normal semantic unit in this CID/RID. It never supplies facts,
    roles, effects, owners or permissions. Natural-language entailment and the
    chosen relation remain explicit human review judgements.
    """
    units = [unit for unit in proof['source_units']
             if isinstance(unit, dict) and unit.get('realization_id') == rid]
    primary = primary_paths(record, rid)
    normal, references, direct = {}, {}, set()
    supports=_validate_guard_supports(proof,record=record);direct_guards=set()
    for unit in units:
        reference = unit.get('disposition') == 'semantic_reference'
        guard_refs=unit.get('guard_refs',[])
        expected = REFERENCE_UNIT_FIELDS if reference else SOURCE_UNIT_FIELDS | ({'guard_refs'} if 'guard_refs' in unit else set())
        if (set(unit) != expected or not isinstance(unit['pointer'], str)
                or not isinstance(unit['disposition'], str)
                or unit['disposition'] not in {'semantic', 'nonsemantic', 'semantic_reference'}
                or unit['quote'] != positive_string(record, unit['pointer'], realization_id=rid)):
            raise ValueError('invalid full-string source-unit disposition')
        if 'guard_refs' in unit:
            if unit['disposition']!='semantic':raise ValueError('only direct ordinary semantic units can ground guard supports')
            _strings(guard_refs,'source unit guard supports')
        _strings(unit['fact_refs'], 'source unit facts', empty=unit['disposition'] == 'nonsemantic' or bool(guard_refs))
        if reference:
            if (unit['pointer'] not in primary or unit['pointer'] in references
                    or not isinstance(unit['reference_relation'], str)
                    or unit['reference_relation'] not in REFERENCE_RELATIONS
                    or not isinstance(unit['retained_constraint_rationale'], str)
                    or not unit['retained_constraint_rationale'].strip()):
                raise ValueError('invalid bounded semantic reference relation or rationale')
            references[unit['pointer']] = unit
            continue
        if unit['pointer'] in normal:
            raise ValueError('invalid full-string source-unit disposition')
        if unit['disposition'] == 'nonsemantic' and unit['fact_refs']:
            raise ValueError('nonsemantic unit cannot supply facts')
        if any(ref not in facts or facts[ref]['realization_id'] != rid
               or facts[ref]['pointer'] != unit['pointer'] or facts[ref]['quote'] not in unit['quote']
               for ref in unit['fact_refs']):
            raise ValueError('unit borrows a foreign fact/source')
        normal[unit['pointer']] = unit
        direct.update(unit['fact_refs'])
        if any(ref not in supports or supports[ref]['realization_id']!=rid
                or supports[ref]['pointer']!=unit['pointer'] or supports[ref]['quote'] not in unit['quote']
                for ref in guard_refs):
            raise ValueError('unit borrows a foreign guard support/source')
        direct_guards.update(guard_refs)
    for pointer, unit in references.items():
        # A direct unit may cover distinct local clauses at this same field.
        # Calling the field nonsemantic at the same time is contradictory.
        if pointer in normal and normal[pointer]['disposition'] != 'semantic':
            raise ValueError('semantic reference conflicts with nonsemantic disposition')
        if any(ref not in direct or facts[ref]['realization_id'] != rid
               or facts[ref]['pointer'] not in primary or facts[ref]['pointer'] == pointer
               for ref in unit['fact_refs']):
            raise ValueError('semantic reference needs a distinct same-RID direct semantic anchor')
    if (not primary <= normal.keys() | references.keys()
            or direct != {fact['id'] for fact in facts.values() if fact['realization_id'] == rid}
            or direct_guards!={row['id'] for row in supports.values() if row['realization_id']==rid}):
        raise ValueError('complete source-unit/fact disposition required')


def effect_set(record, rid):
    if '_semantic_evidence_guard' in record:
        return copy.deepcopy(record['_semantic_evidence_guard']['effect_sets'][rid])
    return with_projection(record, realizations.effects(record, rid))


def with_projection(record, effects):
    effects = copy.deepcopy(effects)
    # This is an explicitly consumed profile projection, not a property inferred
    # from a role or title. Its original footprint must also be accounted for.
    projection = record['content'].get('concept_candidate') or {}
    if 'affected_dimensions' in projection or 'affected_properties' in projection:
        extra = {'dimensions': projection.get('affected_dimensions'),
                 'properties': projection.get('affected_properties')}
        c.validate_effects(extra, record['id']+'.concept_candidate')
        effects['dimensions'] = sorted(set(effects['dimensions']) | set(extra['dimensions']))
        effects['properties'] = [dict(zip(PROPERTY_FIELDS, key)) for key in
            dict.fromkeys(property_key(row) for row in effects['properties'] + extra['properties'])]
    return {'dimensions': sorted(effects['dimensions']),
            'properties': sorted(effects['properties'], key=property_key)}


def referenced_records(record, corpus):
    """Bind complete semantic CIDs and every explicitly consumed old role guard.

    A binding never establishes meaning/identity. Its exact whole digest and
    referenced CID closure prevent stale condition-only source qualifications
    during the temporary pre-migration presentation boundary.
    """
    def refs(value):
        if isinstance(value, str) and (c.ID.fullmatch(value) or c.BINDING_ID.fullmatch(value)):
            yield value
        elif isinstance(value, dict):
            for key, item in value.items():
                yield from refs(key); yield from refs(item)
        elif isinstance(value, list):
            for item in value:
                yield from refs(item)
    pending = set(refs(meaning_material(record))) - {record['id']}
    found = {}
    while pending:
        ref = pending.pop()
        if ref in found or ref == record['id']:
            continue
        field = 'slot_bindings' if c.BINDING_ID.fullmatch(ref) else 'candidates'
        if corpus is None or ref not in corpus[field]:
            raise ValueError('native reference closure requires the current full source/explicit role guard')
        target = corpus[field][ref]
        if field == 'slot_bindings':
            found[ref] = c.digest(target)
            material = target
        else:
            found[ref] = meaning_sha256(target)
            material = meaning_material(target)
        pending.update(set(refs(material)) - set(found) - {record['id']})
    return dict(sorted(found.items()))


def _strings(value, label, *, empty=False):
    result = c.strings(value, label)
    if not result and not empty:
        raise ValueError(label+' must not be empty')
    return result


def _fact_valid(fact):
    mode = fact.get('mode') if isinstance(fact, dict) else None
    expected = FACT_FIELDS | ({'operation', 'receivers'} if mode == 'effect' else set())
    if (not isinstance(mode,str) or mode not in MODES or set(fact) != expected
            or any(not concrete_owned_value(fact[key]) for key in
                   ('id', 'realization_id', 'dimension', 'target', 'property'))
            or not witnesses.typed_value(fact['value'])):
        raise ValueError('invalid native mode, typed value or owned fact shape')
    _strings(fact['requires'], 'fact prerequisites', empty=True)
    if mode == 'effect':
        if fact['operation'] not in OPERATIONS:
            raise ValueError('an actual effect needs an explicitly authored operation')
        _strings(fact['receivers'], 'effect receiver scope', empty=True)
    if fact['value']['type'] == 'frozen_property_reference/v1':
        if mode != 'preservation' or fact['value']['value'] != 'same':
            raise ValueError('only source-supported preservation can bind the frozen value')


def owner_binding_plan(owner_map):
    if (not isinstance(owner_map,dict) or set(owner_map)!={'schema','bindings'}
            or owner_map['schema'] not in {OWNER_SCHEMA,SELECTOR_OWNER_SCHEMA,MEMBER_OWNER_SCHEMA}
            or not isinstance(owner_map['bindings'],list) or len(owner_map['bindings'])>32):
        raise ValueError('bounded explicit source owner bindings required')
    result={}
    for row in owner_map['bindings']:
        modern=owner_map['schema']!=OWNER_SCHEMA
        fields={'target','origin','introduced_by','selector' if modern else 'core_role'}
        if (not isinstance(row,dict) or set(row)!=fields or not concrete_owned_value(row['target'])
                or row['target'] in result or row['origin'] not in {'existing','introduced'}
                or row['origin']=='existing' and row['introduced_by'] is not None
                or row['origin']=='introduced' and not concrete_owned_value(row['introduced_by'])):
            raise ValueError('ambiguous or incomplete owner binding')
        selector=row['selector'] if modern else {'kind':'core_role','role':row['core_role']}
        if not isinstance(selector,dict) or selector.get('kind') not in {'core_role','selected_existing_owner','selected_existing_member_scope'}:
            raise ValueError('unknown explicit owner selector')
        if selector['kind']=='core_role':
            if (set(selector)!={'kind','role'} or not isinstance(selector['role'],str)
                    or selector['role'] not in witnesses.CORE_ROLES):
                raise ValueError('exact neutral role selector required')
        elif selector['kind']=='selected_existing_member_scope':
            if (owner_map['schema']!=MEMBER_OWNER_SCHEMA or set(selector)!={'kind','scope_schema','target_semantics','receiver_semantics'}
                    or selector['scope_schema']!=witnesses.MEMBER_SCOPE_SCHEMA or selector['target_semantics']!='each_member'
                    or selector['receiver_semantics']!='all_members' or row['origin']!='existing' or row['introduced_by'] is not None):
                raise ValueError('explicit existing each-member/all-receiver scope selector required')
        elif set(selector)!={'kind'} or row['origin']!='existing' or row['introduced_by'] is not None:
            raise ValueError('selected owner is existing only with no default')
        result[row['target']]={**row,'selector_kind':selector['kind'],
            'core_role':selector.get('role')}
    return result


def _validate_owner_map(owner_map, facts, *, proof=None, rid=None):
    result=owner_binding_plan(owner_map)
    wanted={fact['target'] for fact in facts}
    wanted.update(owner for fact in facts if fact['mode']=='effect' for owner in fact['receivers'])
    if proof is not None:
        wanted.update(_own_guard_targets(proof,rid))
    if set(result)!=wanted:raise ValueError('owner map must cover the exact active fact/receiver owners')
    for target,row in result.items():
        creators=[fact for fact in facts if fact['mode']=='effect' and fact['operation']=='add_entity' and fact['target']==target]
        if row['selector_kind'] in {'selected_existing_owner','selected_existing_member_scope'} and creators:
            raise ValueError('selected existing owner cannot introduce an entity')
        if row['selector_kind']=='selected_existing_member_scope' and any(fact['mode']=='effect' and fact['target']==target and fact['operation'] in {'add_entity','remove_entity'} for fact in facts):
            raise ValueError('existing scope cannot add or remove members')
        if row['origin']=='introduced':
            creators=[fact for fact in creators if fact['id']==row['introduced_by']]
            if len(creators)!=1:raise ValueError('introduced owner needs its actual add_entity effect')
    return result


def owner_selection_requirements(proof,rid):
    return sorted(target for target,row in owner_binding_plan(proof['owner_maps'][rid]).items()
                  if row['selector_kind'] in {'selected_existing_owner','selected_existing_member_scope'})


def pending_owner_selection(entry):
    if proof_of(entry) is not MISSING and isinstance(proof_of(entry),dict) and proof_of(entry).get('has_owner_selectors') is False:return False
    if native_status(entry)!='qualified' or entry.get('_native_owner_selections') is not None:return False
    proof=proof_of(entry);rid=entry.get('_realization_id')
    ids=[rid] if rid is not None else proof['owner_maps']
    return any(owner_selection_requirements(proof,choice) or any(
        pending_owner_selection(_guard_entry(guard['guard'],child_rid,{}))
        for _,guard in selected_dependencies(proof,choice,entry.get('_native_dependency_selections',{}))
        for child_rid in guard['guard']['effect_sets']) for choice in ids)


def owner_selection_descriptors(proof,rid):
    if proof.get('has_owner_selectors') is False:return None
    nodes={};scoped=False
    def visit(guard,choice,mode):
        nonlocal scoped
        targets=owner_selection_requirements(guard,choice)
        if targets:
            cid=guard.get('candidate_id') or guard['review']['original_review']['candidate_id']
            key=(cid,choice)
            if key not in nodes:
                nodes[key]={'candidate_id':cid,'realization_id':choice,'meaning_sha256':guard['meaning_sha256'],
                    'qualification_sha256':guard.get('qualification_sha256',c.digest(guard)),
                    'targets':targets,'adoption_modes':[],
                    'prerequisite_facts':[{field:copy.deepcopy(fact[field]) for field in ('id','dimension','target','property','mode','value')}
                        for fact in guard['facts'] if fact['realization_id']==choice and fact['target'] in targets and fact['mode'] in {'prerequisite','preservation'}]}
            plan=owner_binding_plan(guard['owner_maps'][choice])
            if any(plan[target]['selector_kind']=='selected_existing_member_scope' for target in targets):
                scoped=True
                nodes[key]['target_selectors']=[{'target':target,'selector':copy.deepcopy(plan[target]['selector'])} for target in targets]
            if mode not in nodes[key]['adoption_modes']:nodes[key]['adoption_modes'].append(mode)
        for dependency,projected in _dependency_guards(guard,choice):
            for child_rid in dependency['realization_ids']:visit(projected['guard'],child_rid,dependency['selection'])
    visit(proof,rid,'root')
    return {'schema':'photo-owner-selection-requirements/v2' if scoped else 'photo-owner-selection-requirements/v1','nodes':[nodes[key] for key in sorted(nodes)]} if nodes else None


def validate_owner_selections(value,core,graph):
    if value is None:return {}
    modern=isinstance(value,dict) and value.get('schema')==MEMBER_SELECTION_SCHEMA
    fields={'schema','core_sha256','owner_graph_sha256','entries'}|({'member_scopes_sha256'} if modern else set())
    if (not isinstance(value,dict) or set(value)!=fields
            or value['schema'] not in {OWNER_SELECTION_SCHEMA,MEMBER_SELECTION_SCHEMA}
            or not _sha256(core.get('canonical_sha256')) or value['core_sha256']!=core['canonical_sha256']
            or core['canonical_sha256']!=c.digest({key:item for key,item in core.items() if key not in {'canonical_sha256','core_id'}})
            or value['owner_graph_sha256']!=c.digest(graph) or not isinstance(value['entries'],list)
            or not 1<=len(value['entries'])<=MAX_OWNER_SELECTION_ENTRIES):
        raise ValueError('exact frozen core/graph-bound owner selections required')
    if modern and value['member_scopes_sha256']!=c.digest(frozen_witnesses(core).get('member_scopes',[])):
        raise ValueError('selected frozen member scope table changed')
    entries={}
    for row in value['entries']:
        if (not isinstance(row,dict) or set(row)!={'candidate_id','realization_id','meaning_sha256','qualification_sha256','bindings'}
                or not isinstance(row['candidate_id'],str) or not c.ID.fullmatch(row['candidate_id'])
                or not concrete_owned_value(row['realization_id']) or not _sha256(row['meaning_sha256'])
                or not _sha256(row['qualification_sha256']) or not isinstance(row['bindings'],list) or not 1<=len(row['bindings'])<=32):
            raise ValueError('bounded exact CID/RID owner selection required')
        key=(row['candidate_id'],row['realization_id'])
        if key in entries or any(cid==key[0] for cid,_ in entries):raise ValueError('duplicate/conflicting owner selection CID/RID')
        targets=set()
        for binding in row['bindings']:
            if (not isinstance(binding,dict) or set(binding)!=({'target','selection'} if modern else {'target','owner_id'})
                    or not concrete_owned_value(binding['target']) or binding['target'] in targets):
                raise ValueError('exact unique source selection target required')
            selected=binding['selection'] if modern else {'kind':'existing_owner','owner_id':binding['owner_id']}
            if not isinstance(selected,dict):raise ValueError('tagged owner/scope selection required')
            if selected.get('kind')=='existing_owner':
                if set(selected)!={'kind','owner_id'} or not concrete_owned_value(selected['owner_id']) or selected['owner_id'] not in graph['owners']:
                    raise ValueError('exact existing frozen actual owner required')
            elif selected.get('kind')=='existing_member_scope' and modern:
                if set(selected)!={'kind','scope_id','scope_sha256'} or not concrete_owned_value(selected['scope_id']) or not _sha256(selected['scope_sha256']):
                    raise ValueError('exact independently frozen scope selection required')
            else:raise ValueError('unknown caller owner/scope selection')
            targets.add(binding['target'])
        entries[key]=row
    return entries


def member_requirement_paths(record, member_index):
    """Positive member render obligations, distinct from source/role conditions."""
    requirements=record['content']['member_candidates'][member_index].get('requirements',{})
    if not isinstance(requirements,dict) or not set(requirements)<={'concept_units','relations'}:
        raise ValueError('member requirements need explicit semantic/render units, not condition overrides')
    if 'concept_units' in requirements:
        _strings(requirements['concept_units'],'member concept units',empty=True)
    if 'relations' in requirements and (not isinstance(requirements['relations'],list)
            or any(not isinstance(row,dict) or not {'id','type','subject','object'}<=set(row)
                   or any(not concrete_owned_value(row[key]) for key in ('id','type','subject','object'))
                   for row in requirements['relations'])):
        raise ValueError('member relations require explicit complete positive endpoints')
    result=set()
    stem='/content/member_candidates/'+str(member_index)+'/requirements'
    def visit(value,pointer):
        if isinstance(value,str) and value.strip():result.add(pointer)
        elif isinstance(value,list):
            for index,item in enumerate(value):visit(item,pointer+'/'+str(index))
        elif isinstance(value,dict):
            for key,item in value.items():
                if key not in NEGATIVE and not key.endswith(('_id','_ids')):
                    visit(item,pointer+'/'+key.replace('~','~0').replace('/','~1'))
    visit(requirements,stem)
    return requirements,result


def _requirement_semantics(binding):
    return {key:value for key,value in binding.items() if key not in {'pointer','quote','child_fact_id'}}


def _child_semantics(fact):
    return {key:value for key,value in fact.items() if key not in {'id','realization_id','pointer','quote'}}


def validate_requirement_binding(record, parent_rid, member_index, dependency, child_proof):
    requirements,paths=member_requirement_paths(record,member_index)
    proof=dependency.get('requirement_bindings')
    if not requirements:
        if proof is not None:raise ValueError('absent member requirements cannot gain invented obligations')
        return
    if (not isinstance(proof,dict) or set(proof)!={'source_sha256','realizations'}
            or proof['source_sha256']!=c.digest(requirements) or not isinstance(proof['realizations'],dict)
            or set(proof['realizations'])!=set(dependency['realization_ids'])):
        raise ValueError('positive member requirements need manual source/actual-child-RID bindings')
    for child_rid,bindings in proof['realizations'].items():
        if not isinstance(bindings,list) or len(bindings)>MAX_FACTS:
            raise ValueError('bounded manually reviewed member requirement facts required')
        child_facts={fact['id']:fact for fact in child_proof['facts'] if fact['realization_id']==child_rid}
        covered=set()
        for binding in bindings:
            fact=child_facts.get(binding.get('child_fact_id')) if isinstance(binding,dict) else None
            if (fact is None or set(binding)!=(set(fact)-{'id','realization_id'})|{'child_fact_id'}
                    or binding['pointer'] not in paths or not isinstance(binding['quote'],str)
                    or not binding['quote'].strip() or binding['quote'] not in positive_string(
                        record,binding['pointer'],realization_id=parent_rid)
                    or _requirement_semantics(binding)!=_child_semantics(fact)):
                raise ValueError('requirement adds unqualified meaning/effect or differs from the actual selected child fact')
            covered.add(binding['pointer'])
        if covered!=paths:
            raise ValueError('every positive member requirement needs explicit fact-mode and actual-effect coverage')


def _compile_manual_role_views(record,catalog):
    """Structural output only, called after the native whole-source checks.

    This is not a capability or a public caller-authored source context. Full
    qualification/publication must independently supply the actual record.
    """
    proof=record['content']['role_evidence']
    if 'manual_role_views' not in proof:return None
    rows=proof['manual_role_views']
    if not isinstance(rows,list) or not 1<=len(rows)<=manual_views.MAX_VIEWS:
        raise ValueError('bounded nonempty explicit manual role views required')
    ids=sorted(realizations.ids(record))
    context={'candidate_id':record['id'],'actual_realization_ids':ids,
        'meaning_sha256':meaning_sha256(record),'catalog_by_id':catalog,
        'facts':proof['facts'],'source_units':proof['source_units'],
        'positive_fields':[{'realization_id':rid,'pointer':pointer,
            'text':positive_string(record,pointer,realization_id=rid)}
            for rid in ids for pointer in sorted(primary_paths(record,rid))],
        'closure_snapshot':{key:proof[key] for key in manual_views.CLOSURE_FIELDS}}
    validated=manual_views.validate_full_views(rows,context=context)
    expected=manual_views.compact_views(validated,authoritative_contract_sha256=c.digest(context))
    return validated,expected


def _ordinary_role_fact(spec,fact):
    return (fact['dimension'] in spec['dimensions'] and any(
        fact['property']==prefix.rstrip('.') or fact['property'].startswith(
            prefix if prefix.endswith('.') else prefix+'.') for prefix in spec['property_prefixes']))


def _role_fact_support(spec,role,fact,*,view_authority=None):
    # A semantic view changes only the explicit role support decision. The
    # complete canonical value/mode/property/owner/operation/Rx stays original.
    if (fact['realization_id'] not in role['realization_ids'] or fact['mode'] not in role['support_modes']
            or fact['mode']=='context' and spec['semantic_role']!='contextual'):
        raise ValueError('role fact is outside its reviewed spec/mode/actual RID')
    if _ordinary_role_fact(spec,fact):return None
    if view_authority is None or not role.get('view_refs'):
        raise ValueError('out-of-prefix role fact requires its explicit source-qualified manual view')
    actual,expected=view_authority
    support=manual_views.selected_support(actual,expected_binding=expected,
        role_id=spec['id'],realization_id=fact['realization_id'],fact_id=fact['id'])
    original={key:value for key,value in fact.items() if key not in {'pointer','quote'}}
    if (support is None or not set(support['view_ids'])<=set(role['view_refs'])
            or support['fact']!=original):
        raise ValueError('manual view does not support this unchanged canonical role fact')
    return support


def _validate_manual_view_usage(proof):
    rows={row['id']:row for row in proof.get('manual_role_views',[])};used=set()
    for tag,role in proof['roles'].items():
        refs=role.get('view_refs',[])
        if 'view_refs' in role:_strings(refs,'explicit role manual views')
        for ref in refs:
            view=rows.get(ref)
            if (view is None or view['role_id']!=tag or view['realization_id'] not in role['realization_ids']
                    or not {row['fact_id'] for row in view['canonical_fact_refs']}<=set(role['fact_refs'])):
                raise ValueError('manual view must bind its exact same-source role/facts/actual RID')
            used.add(ref)
    if used!=set(rows):raise ValueError('unused or foreign manual role view')


def _lookup_manual_view_authority(record,source_data):
    """Rebuild expected support from the independently pinned full source.

    Never take an expected binding from the compact/public receipt under test.
    Lazy source_data.candidates loads the existing hash-verified payload. The
    runtime/final auditor owns its independently acquired source generation.
    """
    if source_data is None:raise ValueError('manual role view requires independent full-source authority')
    cid=record['id'];source=source_data['candidates'][cid]
    if '_semantic_evidence_guard' in source:
        raise ValueError('compact metadata is not full-source role-view authority')
    expected_guard=compact(source,source_data)  # All native whole-source checks.
    if expected_guard is None or 'manual_role_view_bindings' not in expected_guard:
        raise ValueError('actual full source has no qualified manual role views')
    if '_semantic_evidence_guard' in record:
        if proof_of(record)!=expected_guard:raise ValueError('manual role compact differs from full-source qualification')
        actual=proof_of(record)['manual_role_view_bindings']
    else:
        if record!=source:raise ValueError('manual role full source differs from pinned source')
        actual=_compile_manual_role_views(record,source_data['slot_catalog'])[0]
    return actual,expected_guard['manual_role_view_bindings']


def validate(record, catalog, *, catalog_sha256=None, corpus=None, _stack=()):
    if '_semantic_evidence_guard' in record:
        raise ValueError('native source validation requires full positive source, not a compact guard')
    if corpus is not None and record['id'] in corpus.get('candidates',{}):
        authoritative=corpus['candidates'][record['id']]
        if permission_envelope.declaration(authoritative) is not None and c.digest(record)!=c.digest(authoritative):
            raise ValueError('mandatory source differs from actual full corpus authority')
    proof = record['content'].get('role_evidence', MISSING)
    if proof is MISSING:
        permission_envelope.validate_source_only_declaration(record)
        return  # Stage 5C only: source remains explicitly unqualified.
    if (not isinstance(proof, dict) or not _proof_fields_valid(proof) or proof['schema'] != SCHEMA
            or proof['complete'] is not True or proof['meaning_sha256'] != meaning_sha256(record)
            or proof['catalog_sha256'] != (catalog_sha256 or c.digest(catalog))
            or not isinstance(proof['review'], dict)
            or set(proof['review']) != {'basis', 'whole_source_reviewed', 'source_correction',
                                        'original_review', 'native_review'}
            or not isinstance(proof['review']['basis'], str) or not proof['review']['basis'].strip()
            or proof['review']['whole_source_reviewed'] is not True
            or proof['review']['source_correction'] is not None
            and (not isinstance(proof['review']['source_correction'], dict)
                 or set(proof['review']['source_correction']) != {'before_sha256', 'after_sha256', 'rationale'}
                 or proof['review']['source_correction']['after_sha256'] != proof['meaning_sha256']
                 or not all(isinstance(value, str) and value.strip()
                            for value in proof['review']['source_correction'].values()))):
        raise ValueError('stale, incomplete or unsupported native source qualification')
    original, native = proof['review']['original_review'], proof['review']['native_review']
    if (not isinstance(original,dict) or set(original) != {'candidate_id','source_record_sha256',
            'catalog_sha256','decision_sha256','artifact'} or original['candidate_id'] != record['id']
            or any(not _sha256(original[key]) for key in ('source_record_sha256','catalog_sha256','decision_sha256'))
            or not concrete_owned_value(original['artifact'])
            or not isinstance(native,dict) or set(native) != {'reviewer','method','native_contract_sha256'}
            or not concrete_owned_value(native['reviewer']) or native['method'] not in
                {'codex_direct_source_read','codex_subagent_direct_source_read'}
            or native['native_contract_sha256'] != native_contract_sha256(proof)):
        raise ValueError('original review provenance or new native authoring binding is incomplete')
    correction = proof['review']['source_correction']
    if correction is not None and (not _sha256(correction['before_sha256'])
                                  or correction['before_sha256'] == correction['after_sha256']):
        raise ValueError('an explicit source correction requires distinct exact meaning hashes')
    if record['id'] in _stack or len(_stack) > MAX_DEPENDENCY_DEPTH:
        raise ValueError('cyclic native adopted dependency')
    for pointer in record['content'].get('member_candidates', []):
        if (not isinstance(pointer,dict) or not isinstance(pointer.get('candidate_id'),str)
                or not c.ID.fullmatch(pointer['candidate_id']) or corpus is None
                or pointer['candidate_id'] not in corpus['candidates']):
            raise ValueError('native member identity needs an explicit current CID; no binding-only fallback')
        if pointer.get('binding_id') is not None:
            bid=pointer['binding_id']
            if (not isinstance(bid,str) or not c.BINDING_ID.fullmatch(bid)
                    or bid not in corpus['slot_bindings']
                    or corpus['slot_bindings'][bid]['candidate_id'] != pointer['candidate_id']
                    or pointer.get('presentation_role',corpus['slot_bindings'][bid]['slot_id']) != corpus['slot_bindings'][bid]['slot_id']):
                raise ValueError('explicit temporary presentation guard refers to a different CID/role')
    if proof['reference_sha256'] != referenced_records(record, corpus):
        raise ValueError('native complete reference meaning/explicit guard closure changed')
    ids = set(realizations.ids(record))
    if len(ids) > MAX_REALIZATIONS:
        raise ValueError('native actual realization inventory is unbounded')
    if (not isinstance(proof['roles'], dict) or not isinstance(proof['facts'], list)
            or len(proof['facts']) > MAX_FACTS or not isinstance(proof['source_units'], list)
            or len(proof['source_units']) > MAX_UNITS
            or not isinstance(proof['owner_maps'], dict) or set(proof['owner_maps']) != ids
            or not isinstance(proof['effect_sets'], dict) or set(proof['effect_sets']) != ids
            or not isinstance(proof['dependencies'], dict) or set(proof['dependencies']) != ids
            or not isinstance(proof['guard_sets'],dict) or set(proof['guard_sets'])!=ids
            or not isinstance(proof['profile_contracts'],dict) or set(proof['profile_contracts'])!=ids):
        raise ValueError('native facts/units/owner maps must cover actual RIDs')
    facts = {}
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    for fact in proof['facts']:
        _fact_valid(fact)
        if fact['id'] in facts or fact['realization_id'] not in ids or fact['dimension'] not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
            raise ValueError('duplicate fact, unknown RID or dimension')
        if (not isinstance(fact['quote'], str) or not fact['quote'].strip()
                or fact['quote'] not in positive_string(record, fact['pointer'], realization_id=fact['realization_id'])):
            raise ValueError('fact quote differs from its exact positive source')
        facts[fact['id']] = fact
    for fact in facts.values():
        if any(ref not in facts or facts[ref]['realization_id'] != fact['realization_id']
               or facts[ref]['mode'] not in {'prerequisite', 'preservation'} or ref == fact['id']
               for ref in fact['requires']):
            raise ValueError('fact requires an actual same-RID frozen obligation')
    supports=_validate_guard_supports(proof,record=record)
    for rid in ids:
        if proof['guard_sets'][rid] != source_guard_set(record,rid,corpus):
            raise ValueError('native intrinsic/selected/presentation guard inventory changed')
        if proof['profile_contracts'][rid] != realizations.profile_contract(record,rid):
            raise ValueError('native selected profile obligation contract changed')
        dependencies = proof['dependencies'][rid]
        expected_members = realizations.member_ids(record, rid)
        if (not isinstance(dependencies, list) or len(dependencies) > 8
                or any(not isinstance(row, dict) or set(row) not in [
                    {'candidate_id','realization_ids','meaning_sha256','qualification_sha256','selection'},
                    {'candidate_id','realization_ids','meaning_sha256','qualification_sha256','selection','requirement_bindings'}]
                    for row in dependencies)
                or len({row['candidate_id'] for row in dependencies}) != len(dependencies)
                or {row['candidate_id'] for row in dependencies} != expected_members):
            raise ValueError('complete exact selected member dependencies required')
        pointers = {row['candidate_id']:row for row in record['content'].get('member_candidates', [])}
        for dependency in dependencies:
            pointer = pointers[dependency['candidate_id']]
            member_index=record['content']['member_candidates'].index(pointer)
            requirements,_=member_requirement_paths(record,member_index)
            if pointer.get('presentation_role') and pointer['presentation_role'] not in catalog:
                raise ValueError('unknown explicit native member presentation role')
            adoption = pointer.get('adoption')
            if (dependency['selection'] not in {'required', 'explicit_optional'}
                    or dependency['selection'] == 'required' and adoption not in {'required', 'mandatory'}
                    or dependency['selection'] == 'explicit_optional' and adoption != 'optional'):
                raise ValueError('native member selection must preserve explicit canonical adoption; no default-all')
            child = corpus['candidates'][dependency['candidate_id']]
            child_proof = child['content'].get('role_evidence')
            _strings(dependency['realization_ids'], 'actual child realization choices')
            if (not set(dependency['realization_ids']) <= set(realizations.ids(child))
                    or not requirements and set(dependency['realization_ids']) != set(realizations.ids(child))
                    or native_status(child) != 'qualified'
                    or dependency['meaning_sha256'] != meaning_sha256(child)
                    or dependency['qualification_sha256'] != c.digest(child_proof)):
                raise ValueError('adopted child source/qualification/actual choices changed')
            validate_requirement_binding(record,rid,member_index,dependency,child_proof)
            validate(child, catalog, catalog_sha256=catalog_sha256, corpus=corpus,
                     _stack=(*_stack, record['id']))
        validate_guard_namespaces(proof,rid,corpus=corpus)
        selected = [fact for fact in facts.values() if fact['realization_id'] == rid]
        actual = effect_set(record, rid)
        if proof['effect_sets'][rid] != actual:
            raise ValueError('native complete effect set differs from actual selected source')
        declared = {property_key(fact) for fact in selected if fact['mode'] == 'effect'}
        if declared != {property_key(row) for row in actual['properties']}:
            raise ValueError('every actual effect needs effect-mode coverage; non-effect labels cannot waive it')
        if set(actual['dimensions']) != {fact['dimension'] for fact in selected if fact['mode'] == 'effect'}:
            raise ValueError('coarse/dimension-only effects need explicit source refinement before qualification')
        _selected_contract(proof, rid, actual)
        _validate_source_units(record, proof, facts, rid)
    if any(not isinstance(unit, dict) or unit.get('realization_id') not in ids for unit in proof['source_units']):
        raise ValueError('source unit names a foreign RID')
    if record['record_kind'] == 'diagnostic' and (proof['roles'] or proof['facts'] or supports):
        raise ValueError('diagnostic cannot certify positive semantic facts')
    view_authority=_compile_manual_role_views(record,catalog)
    for tag, role in proof['roles'].items():
        if (tag not in catalog or not isinstance(role, dict)
                or not {'spec_sha256','scope','realization_ids','fact_refs','support_modes'} <= set(role)
                or not set(role) <= {'spec_sha256','scope','realization_ids','fact_refs','support_modes','guard_refs','view_refs'}):
            raise ValueError('unknown role or native role contract')
        spec = catalog[tag]
        guard_refs=role.get('guard_refs',[])
        if 'guard_refs' in role:_strings(guard_refs,'role guard supports')
        if 'view_refs' in role:_strings(role['view_refs'],'explicit role manual views')
        _strings(role['realization_ids'], 'role RIDs'); _strings(role['fact_refs'], 'role facts',empty=bool(guard_refs))
        _strings(role['support_modes'], 'role modes')
        if (role['spec_sha256'] != c.digest(spec) or role['scope'] not in {'whole_record', 'positive_alternative'}
                or not set(role['realization_ids']) <= ids or not set(role['support_modes']) <= MODES
                or role['scope'] == 'whole_record' and set(role['realization_ids']) != ids):
            raise ValueError('role spec/scope/mode contract changed')
        covered = set()
        for ref in role['fact_refs']:
            fact = facts.get(ref)
            if fact is None:raise ValueError('role fact is outside its reviewed spec/mode/actual RID')
            _role_fact_support(spec,role,fact,view_authority=view_authority)
            covered.add(fact['realization_id'])
        for ref in guard_refs:
            support=supports.get(ref)
            if support is None:raise ValueError('role needs direct same-source guard support')
            projection=support['semantic_projection']
            if (support['realization_id'] not in role['realization_ids'] or support['mode'] not in role['support_modes']
                    or projection['dimension'] not in spec['dimensions']
                    or not any(projection['property']==prefix.rstrip('.') or projection['property'].startswith(
                        prefix if prefix.endswith('.') else prefix+'.') for prefix in spec['property_prefixes'])):
                raise ValueError('role guard support is outside its reviewed spec/mode/actual RID')
            covered.add(support['realization_id'])
        if covered != set(role['realization_ids']):
            raise ValueError('role needs source support on every qualified RID')
        if guard_refs and set(role['support_modes'])!={facts[ref]['mode'] for ref in role['fact_refs']}|{supports[ref]['mode'] for ref in guard_refs}:
            raise ValueError('guard-backed role modes must match its actual direct support union')
    _validate_manual_view_usage(proof)
    permission_envelope.validate_declaration(record,proof)


def compact(record, corpus=None, _stack=()):
    proof = record['content'].get('role_evidence', MISSING)
    if proof is MISSING:
        return None
    if not isinstance(proof, dict) or proof.get('schema') != SCHEMA:
        raise ValueError('only fully validated native v4 can be compacted')
    if not _stack:
        if corpus is None:
            raise ValueError('native compact seal requires the full current source/catalog')
        validate(record,corpus['slot_catalog'],corpus=corpus)
    result = copy.deepcopy(proof)
    if 'manual_role_views' in proof:
        result.pop('manual_role_views')
        result['manual_role_view_bindings']=_compile_manual_role_views(record,corpus['slot_catalog'])[1]
    result.pop('source_units'); result.pop('review')
    for fact in result['facts']:
        fact.pop('pointer'); fact.pop('quote')
    for support in result.get('guard_supports',[]):
        support.pop('pointer');support.pop('quote')
    result['candidate_id'] = record['id']
    result['qualification_sha256'] = c.digest(proof)
    result['dependency_guards'] = {}
    if record['id'] in _stack or len(_stack) > MAX_DEPENDENCY_DEPTH:
        raise ValueError('cyclic or unbounded dependency projection')
    for rid, rows in proof['dependencies'].items():
        projected = []
        for row in rows:
            if corpus is None:
                raise ValueError('compound projection requires its actual referenced corpus')
            child = corpus['candidates'][row['candidate_id']]
            projected.append({'candidate_id': row['candidate_id'],
                'meaning_sha256':meaning_sha256(child),
                'qualification_sha256':c.digest(child['content']['role_evidence']),
                'guard': compact(child, corpus, (*_stack, record['id']))})
        result['dependency_guards'][rid] = projected
    result['has_owner_selectors']=any(owner_selection_requirements(result,rid) for rid in result['owner_maps']) or any(
        row['guard'].get('has_owner_selectors',False) for rows in result['dependency_guards'].values() for row in rows)
    result['compact_sha256'] = c.digest(result)
    return result


def qualification(spec, record, realization_id='base', *, source_data=None):
    result = {'status': 'review_required', 'reason': 'native_source_unqualified_stage05c',
              'native_qualification': native_status(record), 'matched_properties': [],
              'meaning_terms': [], 'fact_refs': [], 'support_modes': []}
    if result['native_qualification'] != 'qualified':
        if result['native_qualification'] != 'unqualified':
            result['reason'] = 'incomplete_or_unsupported_native_evidence'
        return result
    proof = proof_of(record)
    try:permission_envelope.transport(record)
    except (ValueError,KeyError,TypeError):
        return {**result,'native_qualification':'invalid','reason':'independent_source_transport_authority_required'}
    if '_semantic_evidence_guard' not in record and (not _proof_fields_valid(proof)
            or proof.get('meaning_sha256') != meaning_sha256(record)
            or (proof.get('review') or {}).get('native_review',{}).get('native_contract_sha256') != native_contract_sha256(proof)):
        return {**result,'native_qualification':'invalid','reason':'native_source_authoring_binding_changed'}
    role = proof['roles'].get(spec['id'])
    if role is None:
        return {**result, 'status': 'incompatible', 'reason': 'reviewed_complete_meaning_does_not_support_role'}
    if role['spec_sha256'] != c.digest(spec):
        return {**result, 'reason': 'role_definition_changed_since_source_review'}
    if realization_id not in role['realization_ids']:
        return {**result, 'status': 'incompatible', 'reason': 'role_not_supported_by_selected_realization'}
    selected = [fact for fact in proof['facts'] if fact['id'] in role['fact_refs'] and fact['realization_id'] == realization_id]
    selected_guards=[row for row in proof.get('guard_supports',[])
        if row['id'] in role.get('guard_refs',[]) and row['realization_id']==realization_id]
    selected_effects = (realizations.effects(record, realization_id) if record['effects'].get('realizations')
                        else record['effects'])
    actual = with_projection(record, selected_effects)
    try:
        _selected_contract(proof, realization_id, actual)
    except (ValueError, KeyError, TypeError):
        return {**result, 'reason': 'qualified_actual_effect_set_changed'}
    if not selected and not selected_guards:
        return {**result, 'reason': 'role_has_no_selected_fact'}
    view_supports=[]
    try:
        view_authority=None
        if 'manual_role_views' in proof or 'manual_role_view_bindings' in proof or 'view_refs' in role:
            if source_data is None:return {**result,'reason':'manual_role_view_full_source_authority_required'}
            view_authority=_lookup_manual_view_authority(record,source_data)
        for fact in selected:
            support=_role_fact_support(spec,role,fact,view_authority=view_authority)
            if support is not None:view_supports.append(support)
    except (ValueError,KeyError,TypeError,IndexError):
        return {**result,'native_qualification':'invalid','reason':'manual_role_view_or_original_role_binding_changed'}
    optional_views=({'matched_manual_role_views':view_supports} if view_supports else {})
    if selected_guards:
        return {**result,**optional_views,'status':'eligible','reason':'source_reviewed_guard_evidence_requires_admission',
            'fact_refs':[fact['id'] for fact in selected],
            'guard_refs':[row['id'] for row in selected_guards],
            'guard_admission_required':True,
            'matched_guard_supports':[{'guard_support_id':row['id'],'mode':row['mode'],
                'guard':copy.deepcopy(row['guard']),'semantic_projection':copy.deepcopy(row['semantic_projection'])}
                for row in selected_guards],
            'support_modes':sorted({fact['mode'] for fact in selected}|{row['mode'] for row in selected_guards}),
            'matched_properties':[dict(zip(PROPERTY_FIELDS,key)) for key in dict.fromkeys(property_key(fact) for fact in selected)]}
    return {**result, **optional_views, 'status': 'eligible', 'reason': 'source_reviewed_mode_specific_evidence',
            'fact_refs': [fact['id'] for fact in selected], 'support_modes': sorted({fact['mode'] for fact in selected}),
            'matched_properties': [dict(zip(PROPERTY_FIELDS, key)) for key in dict.fromkeys(property_key(fact) for fact in selected)]}


def frozen_witnesses(core):
    if core.get('contract_version') != 'photo-authorial-core/v3':
        raise ValueError('native qualification requires frozen core v3')
    result = witnesses.read(core.get('semantic_assertions') or [],
                            (core.get('request_binding') or {}).get('active_spans') or [],
                            core.get('baseline_prompt_en', ''), intent_lock=core.get('intent_lock') or {},
                            request_binding=core.get('request_binding') or {})
    return result


def admission(entry,core,*,allow_unselected=False,_nested=False,_whole_entry=None,source_data=None):
    if source_data is not None and permission_envelope.authoritative_native_source(source_data,entry) and not permission_envelope.matches_source(source_data,entry):
        return {'status':'invalid','allowed':False,'reason':'actual_native_source_transport_mismatch'}
    if native_status(entry)=='qualified':
        try:permission_envelope.transport(entry)
        except (ValueError,KeyError,TypeError):
            return {'status':'invalid','allowed':False,'reason':'source_bound_native_transport_required'}
    if permission_envelope.required(entry):
        if permission_envelope.session_binding() is None:
            return {'status':'invalid','allowed':False,'reason':'mandatory_permission_authority_plan_missing'}
        allow_unselected=False
    if native_status(entry)!='qualified':return _admission(entry,core,allow_unselected=allow_unselected,_nested=_nested,_whole_entry=_whole_entry)
    try:
        proof=proof_of(entry);rid=entry.get('_realization_id','base')
        if rid not in proof['effect_sets'] or allow_unselected and pending_owner_selection(entry):
            return _admission(entry,core,allow_unselected=allow_unselected,_nested=_nested,_whole_entry=_whole_entry)
        root=_whole_entry or entry.get('_native_guard_root') or entry
        root_proof=proof_of(root);root_rid=root.get('_realization_id','base')
        if allow_unselected and _pending_dependency_choice(root_proof,root_rid,root.get('_native_dependency_selections',{})):
            # A discovery probe is not a closed final selection. Resolve only
            # actual known nodes, and let the existing bounded alternative
            # probes/evaluator mark its missing edges search-only. Never reuse
            # this partial view for strict final permission or a stored receipt.
            probes=[root]
            if _proof_cid(proof)!=_proof_cid(root_proof):probes.append(entry)
            context=_resolve_selected_native_contracts(probes,core,node_only=True);context['discovery_partial']=True
            token=_ACTIVE_RESOLUTION.set(context)
            try:return _admission(entry,core,allow_unselected=True,_nested=_nested,_whole_entry=_whole_entry)
            finally:_ACTIVE_RESOLUTION.reset(token)
        with bound_selected_resolution([root],core):
            return _admission(entry,core,allow_unselected=allow_unselected,_nested=_nested,_whole_entry=_whole_entry)
    except (ValueError,KeyError,TypeError,IndexError):
        return {'status':'invalid','allowed':False,'reason':'native_obligation_unverified'}


def _admission(entry, core, *, allow_unselected=False, _nested=False, _whole_entry=None):
    """Whole-cue obligations, including effects with no displayed role.

    Source carriers must already be frozen; introduced entities never self-witness
    a prerequisite. The separate permission check still sees every actual effect.
    """
    status = native_status(entry)
    if status == 'unqualified':
        if permission_envelope.required(entry):
            return {'status':'invalid','allowed':False,'reason':'mandatory_permission_source_unqualified'}
        return {'status': status, 'allowed': True, 'reason': 'stage05c_search_pool_only_not_native_adoption'}
    denied = {'status': 'invalid', 'allowed': False, 'reason': 'native_obligation_unverified'}
    if status != 'qualified':
        return denied
    try:
        proof = proof_of(entry); rid = entry.get('_realization_id', 'base')
        if '_realization_id' not in entry and rid not in proof['effect_sets']:
            if not allow_unselected:
                return {**denied, 'reason':'explicit_realization_selection_required'}
            alternatives = [admission(_guard_entry(proof, choice, entry.get('_native_dependency_selections', {}),owner_selections=entry.get('_native_owner_selections')),
                                      core, allow_unselected=True, _nested=True) for choice in proof['effect_sets']]
            return {'status':'qualified', 'allowed':any(row['allowed'] for row in alternatives),
                    'reason':'search_probe_only_requires_explicit_realization',
                    **({'search_only':True} if any(row['selector_kind']=='selected_existing_member_scope' for mapping in proof['owner_maps'].values() for row in owner_binding_plan(mapping).values()) else {})}
        actual = {'dimensions': sorted(entry.get('affected_dimensions', [])),
                  'properties': sorted(entry.get('affected_properties', []), key=property_key)}
        facts, bindings = _selected_contract(proof, rid, actual)
        frozen = frozen_witnesses(core); graph = frozen['graph']
        whole_entry = _whole_entry or entry.get('_native_guard_root') or entry
        if allow_unselected and pending_owner_selection(entry):
            probe=evaluate_native_guards(entry,core,frozen=frozen,whole_entry=whole_entry,allow_unselected=True)
            if not probe['allowed']:return {**denied,'reason':probe['reason']}
            return {'status':'qualified','allowed':True,'search_only':True,
                    'reason':'explicit_existing_owner_selection_required','owner_selection_requirements':owner_selection_requirements(proof,rid)}
        context,node=_resolved_node(entry,core)
        scoped=any(row['selector_kind']=='existing_member_scope' for row in node['bindings'])
        actual_owners={row['target']:row['members'][0]['owner_id'] for row in node['bindings'] if row['selector_kind']!='existing_member_scope'}
        owner_bindings=([copy.deepcopy(row) for row in node['bindings'] if row['selector_kind'] in {'selected_existing_owner','existing_member_scope'}] if scoped else _point_adapter(node)[1])
        resolutions = []
        for expanded in node['expanded_facts']:
            fact=next(fact for fact in facts if fact['id']==expanded['fact_id'])
            _fact_valid_runtime(fact)
            if fact['mode'] not in {'prerequisite', 'preservation'}:
                continue
            binding = bindings[fact['target']]
            actual_owner=expanded['target']['owner_id']
            if binding['origin'] != 'existing':
                return denied
            matches = [row for row in frozen['facts'] if row['dimension'] == fact['dimension']
                       and row['property'] == fact['property']
                       and witnesses.owner_relation(graph, row['target'], actual_owner) == 'overlap'
                       and _same_entity(graph, row['target'], actual_owner)]
            if len(matches) != 1:
                return denied
            match = matches[0]
            reference = fact['mode'] == 'preservation' and fact['value'] == {'type': 'frozen_property_reference/v1', 'value': 'same'}
            if not reference and witnesses.value_key(match['value']) != witnesses.value_key(fact['value']):
                return denied
            resolutions.append({'fact_id': fact['id'], 'core_assertion_id': match['assertion_id'],
                                'owner': actual_owner, 'value': copy.deepcopy(match['value']),
                                **({'scope_member':copy.deepcopy(expanded['target']['scope_provenance'])} if 'scope_provenance' in expanded['target'] else {})})
        guards_receipt = evaluate_native_guards(entry, core, frozen=frozen,
            whole_entry=whole_entry, allow_unselected=allow_unselected)
        if not guards_receipt['allowed']:
            return {**denied, 'reason':guards_receipt['reason']}
        resolved_guard_supports=_guard_support_admission(entry,frozen,guards_receipt,actual_owners)
        selections = entry.get('_native_dependency_selections', {})
        if not isinstance(selections, dict) or any(not isinstance(key, str) or not isinstance(value, str)
                                                 for key,value in selections.items()):
            return denied
        children = []; used = set()
        for dependency, guards in selected_dependencies(proof, rid, selections):
            cid = dependency['candidate_id']; used.add(cid)
            choices = dependency['realization_ids']
            chosen = selections.get(cid, choices[0] if len(choices)==1 else None)
            if chosen not in choices:
                if not allow_unselected or chosen is not None:
                    return {**denied, 'reason':'explicit_dependency_realization_required'}
                results = [admission(_guard_entry(guards['guard'], choice, selections,
                                        extra_conditions=proof['guard_sets'][rid]['member_conditions'][cid],owner_selections=entry.get('_native_owner_selections'),guard_root=whole_entry),
                                     core, allow_unselected=True, _nested=True, _whole_entry=whole_entry) for choice in choices]
                successful = [row for row in results if row['allowed']]
                if not successful:
                    return denied
                children.append({'candidate_id':cid,'search_only':True,'admissions':successful})
                continue
            result = admission(_guard_entry(guards['guard'], chosen, selections,
                                  extra_conditions=proof['guard_sets'][rid]['member_conditions'][cid],owner_selections=entry.get('_native_owner_selections'),guard_root=whole_entry),
                               core, allow_unselected=allow_unselected, _nested=True, _whole_entry=whole_entry)
            if not result['allowed']:
                return denied
            used.update(result.get('used_dependency_ids', []))
            children.append({'candidate_id':cid,'realization_id':chosen,'admission':result})
        if not _nested and not allow_unselected and not set(selections) <= used:
            return {**denied, 'reason':'unused_or_foreign_dependency_selection'}
        search_only = guards_receipt.get('search_only') or any(
            row.get('search_only') or row.get('admission',{}).get('search_only') for row in children)
        if not search_only:
            validate_joint_effect_assignments([entry], core)
        return {'status': 'qualified', 'allowed': True, 'reason': 'whole_native_obligations_verified',
                'resolved_frozen_facts': resolutions, 'dependencies':children, 'native_guards':guards_receipt,
                **({'permission_envelope':copy.deepcopy(context['permission_envelope_receipt'])} if context.get('permission_envelope_receipt') else {}),
                **({'resolved_guard_supports':resolved_guard_supports} if 'guard_supports' in proof else {}),
                'used_dependency_ids':sorted(used),**({'search_only':True} if search_only else {}),**({'owner_resolution':{'candidate_id':proof.get('candidate_id'),
                    'realization_id':rid,'meaning_sha256':proof['meaning_sha256'],'qualification_sha256':proof.get('qualification_sha256',c.digest(proof)),
                    'bindings':owner_bindings}} if owner_bindings else {})}
    except (ValueError, KeyError, TypeError, IndexError):
        return denied


def _same_entity(graph, left, right):
    canonical, _ = witnesses.validate_graph(graph)
    return left in canonical and right in canonical and canonical[left] == canonical[right]


def _guard_entry(proof, rid, selections, *, extra_conditions=None,owner_selections=None,guard_root=None):
    actual = proof['effect_sets'][rid]
    return {**({'_native_guard_root':guard_root} if guard_root is not None else {}),
            '_semantic_evidence_guard':proof, '_realization_id':rid,
            '_native_dependency_selections':selections, '_native_owner_selections':owner_selections, '_native_extra_conditions':copy.deepcopy(extra_conditions or []),
            'affected_dimensions':actual['dimensions'],'affected_properties':actual['properties']}


def _dependency_guards(proof, rid):
    dependencies = proof['dependencies'][rid]
    guards = proof.get('dependency_guards', {}).get(rid, [])
    if len(dependencies) != len(guards):
        raise ValueError('selected dependency guards are incomplete')
    by_id = {row['candidate_id']:row for row in guards}
    if len(by_id) != len(guards):
        raise ValueError('duplicate selected dependency guard')
    result = []
    for row in dependencies:
        guard = by_id.get(row['candidate_id'])
        if (guard is None or guard['meaning_sha256'] != row['meaning_sha256']
                or guard['qualification_sha256'] != row['qualification_sha256']
                or not set(row['realization_ids']) <= set(guard['guard']['effect_sets'])
                or native_status({'_semantic_evidence_guard':guard['guard']})!='qualified'
                or guard['guard']['meaning_sha256'] != row['meaning_sha256']):
            raise ValueError('selected dependency source or proof changed')
        requirement=row.get('requirement_bindings')
        if requirement is not None:
            if set(requirement.get('realizations',{}))!=set(row['realization_ids']):
                raise ValueError('selected member requirement actual RID binding changed')
            for child_rid,bindings in requirement['realizations'].items():
                facts={fact['id']:fact for fact in guard['guard']['facts'] if fact['realization_id']==child_rid}
                for binding in bindings:
                    fact=facts.get(binding['child_fact_id'])
                    if fact is None or _requirement_semantics(binding)!=_child_semantics(fact):
                        raise ValueError('selected member requirement fact/effect changed')
        result.append((row,guard))
    return result


def selected_dependencies(proof, rid, selections):
    """Optional members add obligations only after explicit CID/actual-RID choice."""
    for dependency, guard in _dependency_guards(proof, rid):
        if dependency.get('selection') not in {'required', 'explicit_optional'}:
            raise ValueError('native dependency selection mode missing')
        if dependency['selection'] == 'required' or dependency['candidate_id'] in selections:
            yield dependency, guard


def dependency_choices(proof, rid):
    result = {}
    for dependency, projected in _dependency_guards(proof, rid):
        cid = dependency['candidate_id']; choices = dependency['realization_ids']
        if cid in result and result[cid] != choices:
            raise ValueError('the same source cannot acquire conflicting actual choices')
        result[cid] = copy.deepcopy(choices)
        for choice in choices:
            for child, child_choices in dependency_choices(projected['guard'], choice).items():
                if child in result and result[child] != child_choices:
                    raise ValueError('conflicting shared child choices')
                result[child] = child_choices
    return result


def effect_closure(candidate_id, proof, rid, selections):
    """Public source/RID-addressed coverage, not a target-flattened effect list."""
    rows = [{'candidate_id':candidate_id, 'realization_id':rid,
             'effects':copy.deepcopy(proof['effect_sets'][rid]),
             'owner_map':copy.deepcopy(proof['owner_maps'][rid])}]
    for dependency, projected in selected_dependencies(proof, rid, selections):
        cid = dependency['candidate_id']; choices = dependency['realization_ids']
        choice = selections.get(cid, choices[0] if len(choices)==1 else None)
        if choice not in choices:
            raise ValueError('an actual child realization must be explicitly selected')
        rows.extend(effect_closure(cid, projected['guard'], choice, selections))
    return rows


def _selected_contract(proof, rid, actual):
    if 'dependency_guards' in proof and proof.get('compact_sha256') != c.digest(
            {key:value for key,value in proof.items() if key!='compact_sha256'}):
        raise ValueError('sealed compact native guard changed')
    if rid not in proof.get('guard_sets',{}) or rid not in proof.get('profile_contracts',{}):
        raise ValueError('native v4 guard/profile inventory missing')
    if rid not in proof['effect_sets'] or actual != proof['effect_sets'][rid]:
        raise ValueError('actual selected effects changed')
    _validate_guard_supports(proof)
    facts = [fact for fact in proof['facts'] if fact['realization_id'] == rid]
    by_id = {}
    for fact in facts:
        _fact_valid_runtime(fact)
        if fact['id'] in by_id:
            raise ValueError('duplicate selected fact')
        by_id[fact['id']] = fact
    assignments = {}
    for fact in facts:
        if fact['mode'] != 'effect':
            continue
        key = property_key(fact)
        # Repeated language/source anchors describe the same assignment. There
        # is no implicit partial-value merge or semantic synonym conversion.
        value = (c.canonical_bytes(fact['value']), fact['operation'], frozenset(fact['receivers']))
        if key in assignments and assignments[key] != value:
            raise ValueError('conflicting effect assignment; author distinct properties or an explicit aggregate value')
        assignments[key] = value
    for fact in facts:
        if any(ref not in by_id or by_id[ref]['mode'] not in {'prerequisite', 'preservation'}
               or ref == fact['id'] for ref in fact['requires']):
            raise ValueError('foreign or non-frozen selected prerequisite')
    visited, visiting = set(), set()
    def visit(ref):
        if ref in visiting:
            raise ValueError('cyclic fact prerequisites')
        if ref in visited:
            return
        visiting.add(ref)
        for child in by_id[ref]['requires']:
            visit(child)
        visiting.remove(ref); visited.add(ref)
    for ref in by_id:
        visit(ref)
    if ({property_key(fact) for fact in facts if fact['mode'] == 'effect'} !=
            {property_key(row) for row in actual['properties']}
            or {fact['dimension'] for fact in facts if fact['mode'] == 'effect'} != set(actual['dimensions'])):
        raise ValueError('effect-mode coverage cannot waive actual mutations')
    return facts, _validate_owner_map(proof['owner_maps'][rid], facts, proof=proof, rid=rid)


def _fact_valid_runtime(fact):
    # Full quotes are deliberately absent from sealed compact guards.
    sample = {**fact, 'pointer': '/content/en', 'quote': 'sealed source'}
    _fact_valid(sample)


def _normalized_bindings(proof,rid,selections):
    plan=owner_binding_plan(proof['owner_maps'][rid]);cid=_proof_cid(proof)
    row=selections.get((cid,rid));wanted=owner_selection_requirements(proof,rid)
    if wanted:
        if row is None:raise ValueError('explicit_existing_owner_selection_required')
        if (row['meaning_sha256']!=proof['meaning_sha256'] or row['qualification_sha256']!=proof.get('qualification_sha256',c.digest(proof))
                or {binding['target'] for binding in row['bindings']}!=set(wanted)):
            raise ValueError('owner selection source/proof/target inventory changed')
    elif row is not None:raise ValueError('caller cannot override fixed role owner bindings')
    supplied={binding['target']:binding.get('selection',{'kind':'existing_owner','owner_id':binding.get('owner_id')}) for binding in row['bindings']} if row else {}
    result=[]
    for target,binding in plan.items():
        kind=binding['selector_kind']
        if kind=='core_role':
            selected={'kind':'fixed_role','role':binding['core_role']} if binding['origin']=='existing' else {
                'kind':'introduced_point','role':binding['core_role'],'introduced_by':binding['introduced_by']}
        else:
            selected=copy.deepcopy(supplied[target]);expected='existing_member_scope' if kind=='selected_existing_member_scope' else 'existing_owner'
            if selected.get('kind')!=expected:raise ValueError('point/scope selection kind differs from source contract')
            if expected=='existing_owner':selected['kind']='selected_existing_owner'
            else:selected.update(target_semantics=binding['selector']['target_semantics'],receiver_semantics=binding['selector']['receiver_semantics'])
        result.append({'target':target,'origin':binding['origin'],'selection':selected})
    return result


def _resolve_selected_native_contracts(entries,core,*,node_only=False):
    """Source-checked coordinator; caller projections/receipts are never inputs.

    Full corpus.entry sources are validated/compacted by their actual corpus.
    Sealed layout inputs retain that qualification, and final audit freshly
    validates pinned full sources again. B1 hashes authenticate neither source
    semantics nor a caller-supplied self-hashed projection.
    """
    frozen=frozen_witnesses(core);graph=frozen['graph'];nodes={};source_entries={};roots=[];owner_selection=None
    for entry in entries:
        chosen=entry.get('_native_owner_selections')
        if owner_selection is not None and chosen!=owner_selection:raise ValueError('joint owner selection inputs differ')
        if chosen is not None:owner_selection=chosen
    selections=validate_owner_selections(owner_selection,core,graph)
    def visit(entry,path):
        proof=proof_of(entry);rid=entry.get('_realization_id','base');cid=_proof_cid(proof)
        permission_envelope.transport(entry)
        if native_status(entry)!='qualified' or not isinstance(cid,str) or not c.ID.fullmatch(cid):raise ValueError('qualified source CID required')
        if cid in path or len(path)>MAX_DEPENDENCY_DEPTH:raise ValueError('cyclic/unbounded selected source')
        actual={'dimensions':sorted(entry.get('affected_dimensions',[])), 'properties':sorted(entry.get('affected_properties',[]),key=property_key)}
        facts,plan=_selected_contract(proof,rid,actual)
        if 'dependency_guards' not in proof:
            if (not _proof_fields_valid(proof) or (proof.get('review') or {}).get('native_review',{}).get('native_contract_sha256')!=native_contract_sha256(proof)):
                raise ValueError('full source native authoring binding changed')
            if any(row['selector_kind']=='selected_existing_member_scope' for row in plan.values()):
                raise ValueError('scope application requires full-source validated sealed entry')
        choices=entry.get('_native_dependency_selections',{})
        if not isinstance(choices,dict):raise ValueError('exact dependency choices required')
        children=[]
        if not node_only:
            for dependency,projected in selected_dependencies(proof,rid,choices):
                child_id=dependency['candidate_id'];ids=dependency['realization_ids'];choice=choices.get(child_id,ids[0] if len(ids)==1 else None)
                if choice not in ids:raise ValueError('explicit_dependency_realization_required')
                child=_guard_entry(projected['guard'],choice,choices,owner_selections=owner_selection)
                visit(child,(*path,cid));n=nodes[child_id]
                children.append({key:n[key] for key in ('candidate_id','realization_id','meaning_sha256','qualification_sha256','projection_sha256')}|{'selection':dependency['selection']})
        used={fact['target'] for fact in facts}|{target for fact in facts if fact['mode']=='effect' for target in fact['receivers']}
        node={'candidate_id':cid,'realization_id':rid,'meaning_sha256':proof['meaning_sha256'],
            'qualification_sha256':proof.get('qualification_sha256',c.digest(proof)),
            'bindings':_normalized_bindings(proof,rid,selections),'guard_only_targets':sorted(_own_guard_targets(proof,rid)-used),
            'facts':[{key:copy.deepcopy(value) for key,value in fact.items() if key not in {'pointer','quote'}} for fact in facts],
            'selected_children':children}
        node['projection_sha256']=owner_resolver.node_digest(node)
        if cid in nodes and nodes[cid]!=node:raise ValueError('conflicting selected source/RID/mapping closure')
        nodes[cid]=node;source_entries[cid]={'proof_sha256':c.digest(proof),'dependency_selections':copy.deepcopy(choices),
            'permission_required':permission_envelope.required(entry)}
    for entry in entries:
        visit(entry,());root={'candidate_id':_proof_cid(proof_of(entry)),'realization_id':entry.get('_realization_id','base')}
        if root not in roots:roots.append(root)
    scoped=any(binding['selection']['kind']=='existing_member_scope' for node in nodes.values() for binding in node['bindings'])
    if not node_only and isinstance(owner_selection,dict) and owner_selection.get('schema')==MEMBER_SELECTION_SCHEMA:
        used={(cid,node['realization_id']) for cid,node in nodes.items() if any(binding['selection']['kind'] in {'selected_existing_owner','existing_member_scope'} for binding in node['bindings'])}
        if set(selections)!=used:raise ValueError('missing/unused/foreign selected-closure owner bindings')
    projection={'schema':owner_resolver.SCHEMA,'context_kind':owner_resolver.EXACT_CONTEXT if 'canonical_sha256' in core or 'core_id' in core else owner_resolver.FIXED_CONTEXT,
        'owner_graph_sha256':c.digest(graph),'roots':roots,'nodes':list(nodes.values())}
    if projection['context_kind']==owner_resolver.EXACT_CONTEXT:projection['core_sha256']=core.get('canonical_sha256')
    if scoped:projection['member_scopes_sha256']=c.digest(frozen.get('member_scopes',[]))
    try:view=owner_resolver.resolve_selected_contracts(core,projection)
    except ValueError as exc:
        if str(exc)=='conflicting joint actual-owner effect assignment':
            raise ValueError('conflicting actual-owner effect assignment' if len(nodes)==1 else 'conflicting joint effect assignment') from exc
        raise
    return {'view':view,'nodes':{row['candidate_id']:row for row in view['nodes']},'entries':source_entries,
        'core_sha256':c.digest(core),'owner_selections':copy.deepcopy(owner_selection),'frozen':frozen,'scoped':scoped,
        'permission_session_binding':permission_envelope.session_binding()}


def _context_has_node(context,entry,core):
    """Identity-only read adapter, never admission/closure authority."""
    if context is None or context['core_sha256']!=c.digest(core):return False
    proof=proof_of(entry);cid=_proof_cid(proof);node=context['nodes'].get(cid)
    return (node is not None and node['realization_id']==entry.get('_realization_id','base')
        and c.digest(proof)==context['entries'][cid]['proof_sha256']
        and entry.get('_native_owner_selections')==context['owner_selections'])


def _context_covers(context,entries,core,*,allow_partial=False):
    if context is not None and context.get('discovery_partial') and not allow_partial:return False
    if context is None or context['core_sha256']!=c.digest(core):return False
    if context.get('permission_session_binding')!=permission_envelope.session_binding():return False
    roots={row['candidate_id'] for row in context['view']['roots']}
    def closure_matches(entry,path=()):
        if not _context_has_node(context,entry,core):return False
        proof=proof_of(entry);cid=_proof_cid(proof);rid=entry.get('_realization_id','base')
        if cid in path or len(path)>MAX_DEPENDENCY_DEPTH:return False
        choices=entry.get('_native_dependency_selections',{})
        if not isinstance(choices,dict):return False
        original=context['entries'][cid]['dependency_selections']
        if any(original.get(key)!=value for key,value in choices.items()):return False
        selected=[]
        for dependency,projected in selected_dependencies(proof,rid,choices):
            child_id=dependency['candidate_id'];ids=dependency['realization_ids']
            choice=choices.get(child_id,ids[0] if len(ids)==1 else None)
            if choice not in ids:return False
            child=_guard_entry(projected['guard'],choice,choices,owner_selections=context['owner_selections'])
            if not closure_matches(child,(*path,cid)):return False
            selected.append((child_id,choice,dependency['selection']))
        cached=[(row['candidate_id'],row['realization_id'],row['selection']) for row in context['nodes'][cid]['selected_children']]
        return selected==cached
    def descendant(root,child):
        pending=[row['candidate_id'] for row in context['nodes'][root]['selected_children']];seen=set()
        while pending:
            cid=pending.pop()
            if cid==child:return True
            if cid not in seen:
                seen.add(cid);pending.extend(row['candidate_id'] for row in context['nodes'][cid]['selected_children'])
        return False
    for entry in entries:
        if not _context_has_node(context,entry,core):return False
        # Discovery-only node views are usable solely by internal probes. They
        # can never be reused by bound_selected_resolution's strict entrance.
        if context.get('discovery_partial'):continue
        cid=_proof_cid(proof_of(entry))
        if cid not in roots:
            # Descendant choice subsets are authority only for a real child of
            # an exact active root. An arbitrary stand-alone node cannot borrow
            # its parent's additional selected closure or owner mappings.
            root=entry.get('_native_guard_root')
            if not isinstance(root,dict):return False
            root_id=_proof_cid(proof_of(root))
            if root_id not in roots or not closure_matches(root) or not descendant(root_id,cid):return False
        if not closure_matches(entry):return False
    return True


@contextlib.contextmanager
def bound_selected_resolution(entries,core):
    active=_ACTIVE_RESOLUTION.get()
    if _context_covers(active,entries,core):
        active['permission_envelope_receipt']=permission_envelope.enforce(active,entries,core)
        yield active;return
    context=_resolve_selected_native_contracts(entries,core);token=_ACTIVE_RESOLUTION.set(context)
    try:
        context['permission_envelope_receipt']=permission_envelope.enforce(context,entries,core)
        yield context
    finally:_ACTIVE_RESOLUTION.reset(token)


def _resolved_node(entry,core):
    context=_ACTIVE_RESOLUTION.get()
    if not _context_covers(context,[entry],core,allow_partial=True):raise ValueError('fresh selected resolution context required')
    return context,context['nodes'][_proof_cid(proof_of(entry))]


def _point_adapter(node):
    owners={};bindings=[]
    for binding in node['bindings']:
        if binding['selector_kind']=='existing_member_scope':raise ValueError('scope is not a scalar owner address')
        member=binding['members'][0];owners[binding['target']]=member['owner_id']
        if binding['selector_kind']=='selected_existing_owner':bindings.append({'target':binding['target'],
            'selector_kind':'selected_existing_owner','owner_id':member['owner_id'],'presence_assertion_id':member['presence_assertion_id']})
    return owners,bindings


def owner_resolution(proof,rid,graph,*,core=None,owner_selections=None):
    entry=_guard_entry(proof,rid,{},owner_selections=owner_selections)
    context=_ACTIVE_RESOLUTION.get()
    if not _context_has_node(context,entry,core or {}):context=_resolve_selected_native_contracts([entry],core or {},node_only=True)
    if context['frozen']['graph']!=graph:raise ValueError('frozen owner graph differs from actual core')
    return _point_adapter(context['nodes'][_proof_cid(proof)])


def resolve_owner_bindings(proof,rid,graph,*,core=None,owner_selections=None):
    return owner_resolution(proof,rid,graph,core=core,owner_selections=owner_selections)[0]


def validate_joint_effect_assignments(entries,core):
    if not entries:return
    with bound_selected_resolution(entries,core):pass


def _collect_permission_scope(entry,core,*,_nested=False):
    if native_status(entry)!='qualified':
        return sorted(entry.get('affected_dimensions',[])),copy.deepcopy(entry.get('affected_properties',[])),frozen_witnesses(core)['graph']
    root=entry.get('_native_guard_root') or entry
    with bound_selected_resolution([root],core) as context:
        _,node=_resolved_node(entry,core);wanted=set()
        def visit(cid):
            if cid in wanted:return
            wanted.add(cid)
            for edge in context['nodes'][cid]['selected_children']:visit(edge['candidate_id'])
        visit(node['candidate_id'])
        # Filter one already-expanded view in source traversal order. No scope
        # or owner resolution here; preserve legacy raw aliases and order.
        props={};dims=set()
        def collect(cid):
            for fact in context['nodes'][cid]['expanded_facts']:
                if fact['mode']!='effect':continue
                dims.add(fact['dimension'])
                owners=[fact['target']['owner_id'],*(member['owner_id'] for receiver in fact['receiver_expansions'] for member in receiver['members'])]
                for owner in owners:
                    key=(fact['dimension'],owner,fact['property']);props.setdefault(key,dict(zip(PROPERTY_FIELDS,key)))
            for edge in context['nodes'][cid]['selected_children']:collect(edge['candidate_id'])
        collect(node['candidate_id'])
        return sorted(dims),list(props.values()),context['frozen']['graph']


def _preservation_permission_scope(entry,core):
    # A source preservation prerequisite applies to the complete actually
    # chosen union, including other independent roots in this same audit.
    context=_ACTIVE_RESOLUTION.get()
    if _context_covers(context,[entry],core):
        scope=context['view']['permission_scope']
        return scope['dimensions'],scope['literal_properties'],scope['owner_graph']
    return _collect_permission_scope(entry,core)


def existing_owner_allowed(entry, core, contract, catalog):
    return admission(entry, core)['allowed']


def property_scope_allowed(core, dimensions, effects, *, record=None, realization_id=None,owner_selections=None):
    """Actual triples stay actual; source-addressed effects use the shared view."""
    from photo_contracts import property_effects_allowed
    try:
        if record is not None and permission_envelope.required(record) and native_status(record)!='qualified':
            return False
        graph=frozen_witnesses(core)['graph'];mapped=copy.deepcopy(effects)
        if record is not None and native_status(record)=='qualified':
            proof=proof_of(record);rid=realization_id or record.get('_realization_id')
            if rid is None and len(proof['owner_maps'])==1:rid=next(iter(proof['owner_maps']))
            if rid not in proof['owner_maps']:return False
            entry={**record,'_realization_id':rid,'affected_dimensions':proof['effect_sets'][rid]['dimensions'],
                'affected_properties':proof['effect_sets'][rid]['properties']}
            if owner_selections is not None:entry['_native_owner_selections']=owner_selections
            if _has_target_guards(entry) and not admission(entry,core)['allowed']:return False
            dimensions,mapped,graph=_collect_permission_scope(entry,core)
        return property_effects_allowed(core.get('intent_lock') or {},dimensions,mapped,owner_graph=graph)
    except (ValueError,KeyError,TypeError,IndexError):return False


SOURCE_GUARD_SCHEMA = 'photo-native-source-guards/v1'
SOURCE_TARGET_GUARD_SCHEMA = 'photo-native-source-guards/v2'
GUARD_FIELDS = {
    'preserve_established_scope': {'id','kind','owner_role','scope_kind','known_absent','known_present','unknown'},
    'owner_relation': {'id','kind','relation','left_role','right_role'},
    'frozen_value': {'id','kind','owner_role','dimension','property','value'},
    'frozen_entity_relation': {'id','kind','left_role','right_role','dimension','property','value_type'},
}


def validate_source_guards(block):
    if isinstance(block,dict) and block.get('schema') in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:
        return _validate_target_guards(block)
    if (not isinstance(block,dict) or set(block)!={'schema','rules'} or block['schema']!=SOURCE_GUARD_SCHEMA
            or not isinstance(block['rules'],list) or not 1<=len(block['rules'])<=64):
        raise ValueError('bounded typed native source guards required')
    seen=set()
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    for rule in block['rules']:
        kind=rule.get('kind') if isinstance(rule,dict) else None
        if (not isinstance(kind,str) or kind not in GUARD_FIELDS or set(rule)!=GUARD_FIELDS[kind]
                or not concrete_owned_value(rule['id']) or rule['id'] in seen):
            raise ValueError('invalid or duplicate typed source guard')
        seen.add(rule['id'])
        for key in ('owner_role','left_role','right_role'):
            if key in rule and (not isinstance(rule[key],str) or rule[key] not in witnesses.CORE_ROLES):
                raise ValueError('guard roles must use exact neutral protocol addresses')
        if kind=='preserve_established_scope':
            if (not isinstance(rule['scope_kind'],str) or rule['scope_kind'] not in witnesses.SCOPE_KINDS or rule['known_absent']!='not_applicable'
                    or rule['known_present']!='preserve_all_frozen_items' or rule['unknown']!='review_required'):
                raise ValueError('preservation guards cannot grant a mutation or unknown-state fallback')
        elif kind=='owner_relation':
            if not isinstance(rule['relation'],str) or rule['relation'] not in {'part_of','disjoint'} or rule['left_role']==rule['right_role']:
                raise ValueError('explicit distinct roles and grounded owner relation required')
        else:
            if not isinstance(rule['dimension'],str) or rule['dimension'] not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS or not concrete_owned_value(rule['property']):
                raise ValueError('frozen guard requires an exact dimension/property')
            if kind=='frozen_value' and not witnesses.typed_value(rule['value']):
                raise ValueError('frozen guard needs an exact typed value')
            if kind=='frozen_entity_relation' and rule['value_type']!='entity.owner_id/v1':
                raise ValueError('entity relation guard must bind an actual frozen owner ID')


def source_guard_set(record,rid,corpus=None):
    selected=realizations.branch(record,rid)
    source_conditions=[copy.deepcopy(record['conditions']),copy.deepcopy(selected['conditions'] if selected else {})]
    members={}
    for pointer in record['content'].get('member_candidates',[]):
        cid=pointer['candidate_id']
        if cid not in realizations.member_ids(record,rid):continue
        old={}
        if pointer.get('binding_id'):
            if corpus is None:raise ValueError('explicit member presentation guard needs the full source')
            binding=corpus['slot_bindings'][pointer['binding_id']]
            if binding['candidate_id']!=cid:raise ValueError('presentation guard belongs to another CID')
            old=binding['conditions']
        members[cid]=[copy.deepcopy(pointer.get('conditions',{})),copy.deepcopy(old)]
    for conditions in [*source_conditions,*(value for rows in members.values() for value in rows)]:
        c.validate_conditions(conditions,record['id']+'.native_guards')
    return {'source_conditions':source_conditions,'member_conditions':members}


def condition_layers(entry):
    if native_status(entry)=='qualified':
        proof=proof_of(entry);rid=entry.get('_realization_id','base')
        if rid not in proof['guard_sets'] and '_realization_id' not in entry:
            common=[value['source_conditions'][0] for value in proof['guard_sets'].values()]
            if not common or any(value!=common[0] for value in common):
                raise ValueError('unselected source lacks one exact common intrinsic condition')
            layers=[copy.deepcopy(common[0])]
        else:
            layers=copy.deepcopy(proof['guard_sets'][rid]['source_conditions'])
    else:
        layers=[copy.deepcopy(entry.get('_source_conditions') or {}),copy.deepcopy(entry.get('_selected_conditions') or {})]
    layers += [copy.deepcopy(entry.get('_role_conditions') or {}),*copy.deepcopy(entry.get('_native_extra_conditions') or [])]
    for conditions in layers:c.validate_conditions(conditions,'native condition conjunction')
    return layers


def _pending_dependency_choice(proof,rid,selections):
    for dependency,projected in selected_dependencies(proof,rid,selections):
        cid=dependency['candidate_id'];choices=dependency['realization_ids']
        chosen=selections.get(cid,choices[0] if len(choices)==1 else None)
        if chosen is None:return True
        if chosen not in choices:raise ValueError('foreign selected dependency RID')
        if _pending_dependency_choice(projected['guard'],chosen,selections):return True
    return False


def _guard_support_enabled(entry):
    proof=proof_of(entry)
    return isinstance(proof,dict) and any(row['realization_id']==entry.get('_realization_id','base')
        for row in _guard_support_rows(proof))


def _guard_execution_metadata(proof,rid,index,conditions,rule,graph):
    """Opt-in source provenance, reconstructed rather than a caller receipt."""
    if conditions!=proof['guard_sets'][rid]['source_conditions'][index]:
        raise ValueError('guard execution differs from its sealed own source layer')
    cid=_proof_cid(proof)
    return {'guard_schema':conditions['native_guards']['schema'],
        'declaring_candidate_id':cid,'declaring_realization_id':rid,
        'activation_candidate_id':cid,'activation_realization_id':rid,
        'source_layer':'source_common' if index==0 else 'source_branch',
        'source_condition_index':index,'pointer':'/source_conditions/'+str(index),
        'conditions_sha256':c.digest(conditions),'rule_sha256':c.digest(rule),
        'meaning_sha256':proof['meaning_sha256'],
        'qualification_sha256':proof.get('qualification_sha256',c.digest(proof)),
        'reference_sha256':copy.deepcopy(proof['reference_sha256']),
        'owner_graph_sha256':c.digest(graph)}


def _guard_support_admission(entry,frozen,receipt,actual_owners):
    """Bind reviewed relation support to a fresh, actually executed predicate."""
    proof=proof_of(entry);rid=entry.get('_realization_id','base');cid=_proof_cid(proof)
    selected=[row for row in _validate_guard_supports(proof).values() if row['realization_id']==rid]
    if not selected or receipt.get('search_only'):
        return []
    graph=frozen['graph'];canonical,_=witnesses.validate_graph(graph);resolved=[]
    for row in selected:
        rule=_guard_support_rule(proof,row);ref=row['guard'];index=ref['source_condition_index']
        candidates=[item for item in receipt['rules'] if
            item.get('guard_schema')==ref['schema'] and item.get('declaring_candidate_id')==cid
            and item.get('declaring_realization_id')==rid and item.get('activation_candidate_id')==cid
            and item.get('activation_realization_id')==rid and item.get('source_condition_index')==index
            and item.get('source_layer')==('source_common' if index==0 else 'source_branch')
            and item.get('conditions_sha256')==ref['conditions_sha256']
            and item.get('rule_id')==ref['rule_id'] and item.get('rule_sha256')==ref['rule_sha256']
            and item.get('kind')==rule['kind'] and item.get('status')=='verified']
        if len(candidates)!=1:raise ValueError('guard support lacks one exact executed source predicate')
        item=candidates[0]
        if (item.get('owner_graph_sha256')!=c.digest(graph)
                or item.get('meaning_sha256')!=proof['meaning_sha256']
                or item.get('qualification_sha256')!=proof.get('qualification_sha256',c.digest(proof))
                or item.get('reference_sha256')!=proof['reference_sha256']):
            raise ValueError('guard support executed source/qualification/owner closure changed')
        v2=ref['schema']==SOURCE_TARGET_GUARD_SCHEMA
        if v2 and item.get('endpoints')!={key:rule[key] for key in row['endpoints']}:
            raise ValueError('executed source-target endpoints differ from reviewed guard')
        owners=item['owners']
        if item.get('canonical_owners')!={key:canonical[value] for key,value in owners.items()}:
            raise ValueError('executed canonical owner closure changed')
        for key,ep in row['endpoints'].items():
            if ep['candidate_id']!=cid:continue  # v2 evaluator checked the exact required selected closure.
            actual=actual_owners[ep['target']]
            if (canonical[actual]!=canonical[owners[key]] if v2 else actual!=owners[key]):
                raise ValueError('guard support owner binding differs from actual schema execution')
        if rule['kind']=='frozen_entity_relation' and not concrete_owned_value(item.get('core_assertion_id')):
            raise ValueError('frozen relation support lacks its executed core assertion')
        resolved.append({'guard_support_id':row['id'],'realization_id':rid,'mode':row['mode'],
            'semantic_projection':copy.deepcopy(row['semantic_projection']),
            'guard':copy.deepcopy(ref),'execution':copy.deepcopy(item)})
    return resolved


def _evaluate_role_guards(entry,core,*,frozen=None,whole_entry=None,allow_unselected=False):
    frozen=frozen or frozen_witnesses(core);graph=frozen['graph']
    canonical,ancestors=witnesses.validate_graph(graph)
    receipts=[];preserved=[];pending=False;whole_entry=whole_entry or entry
    for layer_index,conditions in enumerate(condition_layers(entry)):
        block=conditions.get('native_guards')
        if block is None:continue
        validate_source_guards(block)
        if block['schema'] in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:continue
        for rule in block['rules']:
            roles={key:graph['roles'].get(rule[key]) for key in ('owner_role','left_role','right_role') if key in rule}
            if any(owner is None for owner in roles.values()):
                return {'allowed':False,'reason':'native_guard_owner_not_established'}
            receipt={'layer':layer_index,'rule_id':rule['id'],'kind':rule['kind'],'owners':roles}
            if layer_index<2 and _guard_support_enabled(entry):
                proof=proof_of(entry);rid=entry.get('_realization_id','base')
                receipt.update(_guard_execution_metadata(proof,rid,layer_index,conditions,rule,graph),
                    canonical_owners={key:canonical[value] for key,value in roles.items()})
            kind=rule['kind']
            if kind=='owner_relation':
                left,right=roles['left_role'],roles['right_role']
                satisfied=(canonical[right] in ancestors[canonical[left]] if rule['relation']=='part_of'
                           else witnesses.owner_relation(graph,left,right)=='disjoint')
                if not satisfied:return {'allowed':False,'reason':'native_owner_relation_unverified'}
            elif kind in {'frozen_value','frozen_entity_relation'}:
                owner=roles.get('owner_role',roles.get('left_role'))
                matches=[fact for fact in frozen['facts'] if fact['dimension']==rule['dimension']
                         and fact['property']==rule['property'] and _same_entity(graph,fact['target'],owner)]
                if len(matches)!=1:return {'allowed':False,'reason':'native_frozen_guard_fact_missing'}
                expected=rule['value'] if kind=='frozen_value' else {'type':rule['value_type'],'value':roles['right_role']}
                if witnesses.value_key(matches[0]['value'])!=witnesses.value_key(expected):
                    return {'allowed':False,'reason':'native_frozen_guard_value_mismatch'}
                receipt['core_assertion_id']=matches[0]['assertion_id']
            else:
                owner=roles['owner_role']
                scopes=[row for row in frozen['scope_inventories'] if row['scope_kind']==rule['scope_kind']
                        and _same_entity(graph,row['owner'],owner)]
                host=(core.get('request_binding') or {}).get('input_inventory')
                if (len(scopes)!=1 or not host or host['complete'] is not True
                        or scopes[0]['inventory']['complete'] is not True or scopes[0]['inventory']['state']=='unknown'):
                    return {'allowed':False,'reason':'native_preservation_scope_review_required'}
                scope=scopes[0];inv=scope['inventory'];receipt.update(state=inv['state'],scope_assertion_id=scope['assertion_id'])
                if inv['state']=='known_present':
                    proof=proof_of(whole_entry);whole_rid=whole_entry.get('_realization_id','base')
                    selections=whole_entry.get('_native_dependency_selections',{})
                    if allow_unselected and (_pending_dependency_choice(proof,whole_rid,selections) or pending_owner_selection(whole_entry)):
                        pending=True;receipt['effect_check']='explicit_dependency_selection_required'
                    else:
                        dims,effects,owner_graph=_preservation_permission_scope(whole_entry,core)
                        from photo_contracts import property_effects_allowed
                        locks={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':item['dimension'],'target':item['target'],
                                                   'property':item['property']} for item in inv['items']]}
                        if not property_effects_allowed(locks,dims,effects,owner_graph=owner_graph):
                            return {'allowed':False,'reason':'native_established_scope_effect_overlap'}
                    preserved.append(copy.deepcopy(scope))
            if 'guard_schema' in receipt:receipt['status']='verified'
            receipts.append(receipt)
    return {'allowed':True,'reason':'search_only_dependency_selection_required' if pending else 'all_native_guards_verified',
            'rules':receipts,'preserved_scopes':preserved,'search_only':pending}


def audit_scope_preservation(receipt, interpretation, prompt):
    required={}
    def collect(admission_receipt):
        for scope in (admission_receipt.get('native_guards') or {}).get('preserved_scopes',[]):
            required[scope['assertion_id']]={item['assertion_id']:item for item in scope['inventory']['items']}
        for dependency in admission_receipt.get('dependencies',[]):
            if 'admission' in dependency:collect(dependency['admission'])
    collect(receipt)
    evidence=interpretation.get('scope_preservation_evidence',{})
    if not isinstance(evidence,dict) or set(evidence)!=set(required):
        raise ValueError('final established scope preservation evidence is incomplete or foreign')
    for scope,items in required.items():
        provided=evidence[scope]
        if not isinstance(provided,dict) or set(provided)!=set(items):
            raise ValueError('every frozen scope item needs final preservation evidence')
        for aid,item in items.items():
            row=provided[aid]
            if (not isinstance(row,dict) or set(row)!={'owner','value','prompt_evidence'}
                    or row['owner']!=item['target'] or row['value']!=item['value']
                    or not isinstance(row['prompt_evidence'],str) or not row['prompt_evidence'].strip()
                    or row['prompt_evidence'] not in prompt):
                raise ValueError('final owner/value/prompt evidence differs from the frozen scope')


# v2 addresses source-local owners in a checked selected closure. No role-word,
# anatomy, source-fact, or owner-selection inference occurs here.
TARGET_GUARD_FIELDS = {
    'owner_relation': {'id','kind','relation','left','right'},
    'frozen_value': {'id','kind','owner','dimension','property','value'},
    'frozen_entity_relation': {'id','kind','left','right','dimension','property','value_type'},
    'preserve_established_scope': {'id','kind','owner','scope_kind','known_absent','known_present','unknown'},
}


def _guard_endpoints(rule):
    if rule.get('kind')=='for_each_member':return [rule['scope'],*_guard_endpoints(rule['rule'])]
    return [rule[key] for key in ('owner','left','right') if key in rule and rule[key].get('kind')=='source_target']


def _validate_target_guards(block):
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    if (set(block)!={'schema','rules'} or not isinstance(block['rules'],list) or not 1<=len(block['rules'])<=64):
        raise ValueError('bounded source-target guards required')
    def endpoint(ep,variable=None):
        if variable is not None and isinstance(ep,dict) and ep.get('kind')=='bound_member':
            if set(ep)!={'kind','variable'} or ep['variable']!=variable:raise ValueError('exact lexically bound member required')
        elif (not isinstance(ep,dict) or set(ep)!={'kind','candidate_id','target'} or ep['kind']!='source_target'
                or not isinstance(ep['candidate_id'],str) or not c.ID.fullmatch(ep['candidate_id']) or not concrete_owned_value(ep['target'])):
            raise ValueError('exact CID/source-target endpoint required')
    def atom(rule,variable=None):
        kind=rule.get('kind') if isinstance(rule,dict) else None
        if not isinstance(kind,str) or kind not in TARGET_GUARD_FIELDS or set(rule)!=TARGET_GUARD_FIELDS[kind] or not concrete_owned_value(rule['id']):
            raise ValueError('exact nonnested scalar atomic member predicate required')
        for key in ('owner','left','right'):
            if key in rule:endpoint(rule[key],variable)
        if variable is not None and not any(rule.get(key)=={'kind':'bound_member','variable':variable} for key in ('owner','left','right')):
            raise ValueError('quantified atom must actually use its bound member')
        if kind=='owner_relation':
            if not isinstance(rule['relation'],str) or rule['relation'] not in {'part_of','disjoint'} or rule['left']==rule['right']:raise ValueError('distinct explicit relation endpoints required')
        elif kind=='preserve_established_scope':
            if (not isinstance(rule['scope_kind'],str) or rule['scope_kind'] not in witnesses.SCOPE_KINDS or rule['known_absent']!='not_applicable'
                    or rule['known_present']!='preserve_all_frozen_items' or rule['unknown']!='review_required'):
                raise ValueError('preservation requires complete frozen scope or review')
        else:
            if not isinstance(rule['dimension'],str) or rule['dimension'] not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS or not concrete_owned_value(rule['property']):raise ValueError('exact frozen dimension/property required')
            if kind=='frozen_value' and not witnesses.typed_value(rule['value']):raise ValueError('exact frozen typed value required')
            if kind=='frozen_entity_relation' and rule['value_type']!='entity.owner_id/v1':raise ValueError('exact actual-owner value type required')
    seen=set()
    for rule in block['rules']:
        if not isinstance(rule,dict) or not concrete_owned_value(rule.get('id')) or rule['id'] in seen:raise ValueError('invalid/duplicate target guard')
        seen.add(rule['id'])
        if rule.get('kind')=='for_each_member':
            if (block['schema']!=MEMBER_GUARD_SCHEMA or set(rule)!={'id','kind','scope','member_variable','rule'}
                    or not concrete_owned_value(rule['member_variable'])):raise ValueError('explicit bounded member quantifier required')
            endpoint(rule['scope']);atom(rule['rule'],rule['member_variable'])
        else:atom(rule)


def _proof_cid(proof):
    if not isinstance(proof,dict):raise ValueError('qualified source CID required')
    return proof.get('candidate_id') or proof['review']['original_review']['candidate_id']


def _own_guard_targets(proof,rid):
    cid=_proof_cid(proof);targets=set()
    for conditions in proof['guard_sets'][rid]['source_conditions']:
        block=conditions.get('native_guards')
        if block is None:continue
        validate_source_guards(block)
        if block['schema'] in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:
            targets.update(ep['target'] for rule in block['rules'] for ep in _guard_endpoints(rule)
                           if ep['candidate_id']==cid)
    for row in _guard_support_rows(proof):
        if row['realization_id']==rid:
            targets.update(ep['target'] for ep in row['endpoints'].values() if ep['candidate_id']==cid)
    return targets


def _check_endpoint_plans(conditions,namespace):
    block=conditions.get('native_guards')
    if block is None:return
    validate_source_guards(block)
    if block['schema'] not in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:return
    for rule in block['rules']:
        endpoints=([(rule['scope'],True),*((ep,False) for ep in _guard_endpoints(rule['rule']))] if rule.get('kind')=='for_each_member' else [(ep,False) for ep in _guard_endpoints(rule)])
        for ep,quantified in endpoints:
            plans=namespace.get(ep['candidate_id'])
            if not plans or any(ep['target'] not in plan or plan[ep['target']]['origin']!='existing' for plan in plans):
                raise ValueError('guard endpoint outside exact existing-owner source namespace')
            if any((plan[ep['target']]['selector_kind']=='selected_existing_member_scope')!=quantified for plan in plans):
                raise ValueError('explicit point versus quantified scope guard endpoint required')


def validate_guard_namespaces(proof,rid,*,corpus):
    """Qualification checks every declared branch; optional guards stay scoped."""
    cid=_proof_cid(proof)
    def node_plan(p,choice):return owner_binding_plan(p['owner_maps'][choice])
    def children(p,choice):
        result={}
        for dep in p['dependencies'][choice]:
            child=corpus['candidates'][dep['candidate_id']]['content']['role_evidence']
            result[dep['candidate_id']]=(dep,child)
        return result
    def own_namespace(p,choice):
        ns={_proof_cid(p):[node_plan(p,choice)]}
        for child_id,(dep,child) in children(p,choice).items():
            if dep['selection']=='required':ns[child_id]=[node_plan(child,ch) for ch in dep['realization_ids']]
        return ns
    own=own_namespace(proof,rid)
    for conditions in proof['guard_sets'][rid]['source_conditions']:_check_endpoint_plans(conditions,own)
    for child_id,(dep,child) in children(proof,rid).items():
        conditions=proof['guard_sets'][rid]['member_conditions'][child_id]
        member={cid:[node_plan(proof,rid)],child_id:[node_plan(child,ch) for ch in dep['realization_ids']]}
        _check_endpoint_plans(conditions[0],member)
        for choice in dep['realization_ids']:_check_endpoint_plans(conditions[1],own_namespace(child,choice))


def _has_target_guards(entry):
    def contains(value):
        if isinstance(value,dict):
            return value.get('schema') in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA} or any(contains(x) for x in value.values())
        return isinstance(value,list) and any(contains(x) for x in value)
    root=entry.get('_native_guard_root') or entry
    return contains(proof_of(root)) or contains(root.get('_role_conditions')) or contains(entry.get('_native_extra_conditions'))


def bind_guard_root(entry,root):
    """Attach checked-source context, not a caller-authored condition frame."""
    result=copy.deepcopy(entry)
    result['_native_guard_root']=copy.deepcopy(root.get('_native_guard_root') or root)
    return result


def _guard_context(entry,*,whole_entry=None,allow_unselected=False):
    root=whole_entry or entry.get('_native_guard_root') or entry
    root=root.get('_native_guard_root') or root
    selections=root.get('_native_dependency_selections',{});owners=root.get('_native_owner_selections')
    nodes={};incoming={};pending=set();probed=set()
    def walk(current,stack=()):
        p=proof_of(current);rid=current.get('_realization_id','base');cid=_proof_cid(p)
        if cid in stack or len(stack)>MAX_DEPENDENCY_DEPTH:raise ValueError('cyclic guard context')
        _selected_contract(p,rid,p['effect_sets'][rid])
        if cid in nodes:
            old=nodes[cid]
            if old['rid']!=rid or old['proof']!=p:raise ValueError('conflicting selected guard node')
            return
        node={'proof':p,'rid':rid,'entry':current,'required':set()};nodes[cid]=node
        for dep,guard in selected_dependencies(p,rid,selections):
            child=dep['candidate_id'];choices=dep['realization_ids']
            if dep['selection']=='required':node['required'].add(child)
            chosen=selections.get(child,choices[0] if len(choices)==1 else None)
            if chosen is None and allow_unselected:
                if _proof_cid(proof_of(entry))==child and entry.get('_realization_id','base') in choices:
                    chosen=entry.get('_realization_id','base');probed.add(child)
                else:
                    pending.add(child);continue
            if chosen not in choices:raise ValueError('guard requires exact selected dependency RID')
            incoming.setdefault(child,[]).append((cid,rid,p['guard_sets'][rid]['member_conditions'][child]))
            walk(_guard_entry(guard['guard'],chosen,selections,owner_selections=owners),(*stack,cid))
    walk(root)
    cid=_proof_cid(proof_of(entry));rid=entry.get('_realization_id','base')
    if cid not in nodes or nodes[cid]['rid']!=rid or nodes[cid]['proof']!=proof_of(entry):
        raise ValueError('entry is not the exact selected guard node')
    if entry.get('_native_owner_selections')!=owners:
        raise ValueError('member owner mapping differs from selected root')
    if any(selections.get(key)!=value for key,value in entry.get('_native_dependency_selections',{}).items()):
        raise ValueError('member dependency choice differs from selected root')
    # Anonymous/injected v2 member layers have no standing. Their exact source
    # must be reconstructed from the selected parent's sealed member guard set.
    declared=[cond for _,_,rows in incoming.get(cid,[]) for cond in rows]
    for cond in entry.get('_native_extra_conditions',[]):
        if (cond.get('native_guards') or {}).get('schema') in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA} and cond not in declared:
            raise ValueError('anonymous or foreign source-target member guard')
    frames={key:[] for key in nodes}
    def add(active,declaring,declaring_rid,layer,pointer,conditions,allowed,proof):
        _check_endpoint_plans(conditions,{key:[owner_binding_plan(nodes[key]['proof']['owner_maps'][nodes[key]['rid']])]
            for key in allowed if key in nodes}) if not pending else None
        block=conditions.get('native_guards')
        if not block or block['schema'] not in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:return
        validate_source_guards(block)
        for rule in block['rules']:
            if any(ep['candidate_id'] not in allowed for ep in _guard_endpoints(rule)):
                raise ValueError('foreign CID in source-target guard frame')
        frames[active].append({'declaring_candidate_id':declaring,'declaring_realization_id':declaring_rid,
            'activation_candidate_id':active,'activation_realization_id':nodes[active]['rid'],
            'layer':layer,'pointer':pointer,'conditions_sha256':c.digest(conditions),
            'meaning_sha256':proof['meaning_sha256'],'qualification_sha256':proof.get('qualification_sha256',c.digest(proof)),
            'reference_sha256':copy.deepcopy(proof['reference_sha256']),'allowed':allowed,'block':block})
    for key,node in nodes.items():
        p=node['proof'];choice=node['rid'];allowed={key,*node['required']}
        for i,cond in enumerate(p['guard_sets'][choice]['source_conditions']):
            add(key,key,choice,'source_common' if i==0 else 'source_branch','/source_conditions/'+str(i),cond,allowed,p)
        for parent,parent_rid,conds in incoming.get(key,[]):
            parent_proof=nodes[parent]['proof'];path='/member_conditions/'+key+'/'
            add(key,parent,parent_rid,'member_pointer',path+'0',conds[0],{parent,key},parent_proof)
            add(key,parent,parent_rid,'member_presentation',path+'1',conds[1],allowed,parent_proof)
    # Direct presentation is source-bound by corpus.entry and freshly rebuilt by
    # final audit. A caller-supplied role condition is never its own provenance.
    for current in (root,entry) if root is not entry else (root,):
        cond=current.get('_role_conditions') or {}
        if (cond.get('native_guards') or {}).get('schema') not in {SOURCE_TARGET_GUARD_SCHEMA,MEMBER_GUARD_SCHEMA}:continue
        binding=current.get('_native_presentation_guard');key=_proof_cid(proof_of(current))
        if (not isinstance(binding,dict) or set(binding)!={'record','sha256'} or c.digest(binding['record'])!=binding['sha256']
                or binding['record'].get('candidate_id')!=key or binding['record'].get('id')!=current.get('binding_id')
                or binding['record'].get('conditions')!=cond):
            raise ValueError('source-target presentation guard lacks pinned binding provenance')
        n=nodes[key];add(key,key,n['rid'],'presentation','/binding/'+binding['record']['id'],cond,{key,*n['required']},n['proof'])
        if frames[key] and frames[key][-1]['layer']=='presentation':frames[key][-1]['binding_sha256']=binding['sha256']
    return {'root':root,'nodes':nodes,'frames':frames,'pending':pending,'probed':probed,'selections':selections,'owners':owners}


def _evaluate_target_guards(entry,core,*,frozen,whole_entry=None,allow_unselected=False):
    context=_guard_context(entry,whole_entry=whole_entry,allow_unselected=allow_unselected)
    graph=frozen['graph'];canonical,ancestors=witnesses.validate_graph(graph)
    active=_proof_cid(proof_of(entry));receipts=[];preserved=[];pending=bool(context['probed'])
    resolved=_ACTIVE_RESOLUTION.get()
    def binding(ep,frame):
        cid=ep['candidate_id'];target=ep['target']
        if cid not in frame['allowed']:raise ValueError('guard CID outside condition namespace')
        if cid in context['pending']:return None
        node=context['nodes'].get(cid)
        if node is None:raise ValueError('guard node is not selected')
        plan=owner_binding_plan(node['proof']['owner_maps'][node['rid']]);source=plan.get(target)
        if source is None or source['origin']!='existing':raise ValueError('frozen guard requires existing source owner')
        if allow_unselected and context['owners'] is None and source['selector_kind']!='core_role':return None
        if resolved is not None:
            match=resolved['nodes'].get(cid)
            if match is None or match['realization_id']!=node['rid']:raise ValueError('guard outside shared resolved closure')
            return next(row for row in match['bindings'] if row['target']==target)
        # Discovery may evaluate independent fixed endpoints while other choices
        # are absent. It does not resolve or fabricate scope members.
        if allow_unselected and context['owners'] is None and source['selector_kind']=='core_role':
            owner=graph['roles'].get(source['core_role'])
            if owner not in canonical:raise ValueError('guard owner not established')
            return {'selector_kind':'fixed_role','members':[{'owner_id':owner,'canonical_owner_id':canonical[owner]}]}
        raise ValueError('fresh shared guard resolution required')
    def point(ep,frame,variable=None,member=None):
        if ep.get('kind')=='bound_member':
            if ep.get('variable')!=variable or member is None:raise ValueError('unbound member endpoint')
            return member['owner_id']
        row=binding(ep,frame)
        if row is None:return None
        if row['selector_kind']=='existing_member_scope':raise ValueError('scalar guard cannot implicitly lift a scope')
        return row['members'][0]['owner_id']
    def atom(rule,frame,receipt,variable=None,member=None):
        nonlocal pending
        pairs={key:point(rule[key],frame,variable,member) for key in ('owner','left','right') if key in rule}
        receipt.update(rule_id=rule['id'],kind=rule['kind'],endpoints=copy.deepcopy({key:rule[key] for key in pairs}),owners=pairs)
        if (_guard_support_enabled(entry) and frame['declaring_candidate_id']==active and frame['layer'] in {'source_common','source_branch'}):
            receipt.update(guard_schema=frame['block']['schema'],rule_sha256=c.digest(rule),source_layer=frame['layer'],
                source_condition_index=0 if frame['layer']=='source_common' else 1,owner_graph_sha256=c.digest(graph),
                canonical_owners={key:canonical[value] if value is not None else None for key,value in pairs.items()})
        if any(value is None for value in pairs.values()):pending=True;receipt['status']='review_required';return None
        kind=rule['kind']
        if kind=='owner_relation':
            left,right=pairs['left'],pairs['right']
            valid=canonical[right] in ancestors[canonical[left]] if rule['relation']=='part_of' else witnesses.owner_relation(graph,left,right)=='disjoint'
            if not valid:return 'native_owner_relation_unverified'
            receipt['owner_graph_sha256']=c.digest(graph)
        elif kind in {'frozen_value','frozen_entity_relation'}:
            owner=pairs.get('owner',pairs.get('left'))
            matches=[row for row in frozen['facts'] if row['dimension']==rule['dimension'] and row['property']==rule['property'] and _same_entity(graph,row['target'],owner)]
            if len(matches)!=1:return 'native_frozen_guard_fact_missing'
            value=matches[0]['value'];valid=(witnesses.value_key(value)==witnesses.value_key(rule['value']) if kind=='frozen_value' else
                value['type']==rule['value_type'] and isinstance(value['value'],str) and _same_entity(graph,value['value'],pairs['right']))
            if not valid:return 'native_frozen_guard_value_mismatch'
            receipt['core_assertion_id']=matches[0]['assertion_id']
        else:
            owner=pairs['owner'];scopes=[row for row in frozen['scope_inventories'] if row['scope_kind']==rule['scope_kind'] and _same_entity(graph,row['owner'],owner)]
            host=(core.get('request_binding') or {}).get('input_inventory')
            if (len(scopes)!=1 or not host or host['complete'] is not True or scopes[0]['inventory']['complete'] is not True or scopes[0]['inventory']['state']=='unknown'):
                return 'native_preservation_scope_review_required'
            scope=scopes[0];inv=scope['inventory'];receipt.update(state=inv['state'],scope_assertion_id=scope['assertion_id'])
            if inv['state']=='known_present':
                root=context['root']
                if allow_unselected and (context['pending'] or pending_owner_selection(root)):
                    pending=True;receipt['effect_check']='explicit_selected_closure_required'
                else:
                    dims,effects,owner_graph=_preservation_permission_scope(root,core)
                    from photo_contracts import property_effects_allowed
                    locks={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{key:item[key] for key in PROPERTY_FIELDS} for item in inv['items']]}
                    if not property_effects_allowed(locks,dims,effects,owner_graph=owner_graph):return 'native_established_scope_effect_overlap'
                preserved.append(copy.deepcopy(scope))
        receipt['status']='verified';return None
    for frame in context['frames'][active]:
        for rule in frame['block']['rules']:
            receipt={key:copy.deepcopy(value) for key,value in frame.items() if key not in {'block','allowed'}}
            if rule['kind']=='for_each_member':
                collection=binding(rule['scope'],frame)
                receipt.update(rule_id=rule['id'],kind=rule['kind'],rule_sha256=c.digest(rule),scope=copy.deepcopy(rule['scope']),member_variable=rule['member_variable'])
                if collection is None:
                    pending=True;receipt['status']='review_required';receipt['member_results']=[];receipts.append(receipt);continue
                if collection['selector_kind']!='existing_member_scope':raise ValueError('quantifier requires an explicitly selected member scope')
                receipt['scope_selection']=copy.deepcopy(collection['selection']);receipt['member_results']=[]
                for index,member in enumerate(collection['members']):
                    item={key:copy.deepcopy(value) for key,value in receipt.items() if key not in {'member_results'}}
                    item.update(quantified_rule_id=rule['id'],member_index=index,member=copy.deepcopy(member))
                    reason=atom(rule['rule'],frame,item,rule['member_variable'],member)
                    if reason:return {'allowed':False,'reason':reason}
                    receipt['member_results'].append(item)
                receipt['status']='verified' if all(row['status']=='verified' for row in receipt['member_results']) else 'review_required'
            else:
                reason=atom(rule,frame,receipt)
                if reason:return {'allowed':False,'reason':reason}
            receipts.append(receipt)
    return {'allowed':True,'reason':'search_only_source_target_required' if pending else 'all_native_guards_verified',
        'rules':receipts,'preserved_scopes':preserved,'search_only':pending}


def evaluate_native_guards(entry,core,*,frozen=None,whole_entry=None,allow_unselected=False):
    root=whole_entry or entry.get('_native_guard_root') or entry
    proof=proof_of(root);rid=root.get('_realization_id','base')
    pending=allow_unselected and (pending_owner_selection(root) or _pending_dependency_choice(proof,rid,root.get('_native_dependency_selections',{})))
    if pending:return _evaluate_native_guards(entry,core,frozen=frozen,whole_entry=whole_entry,allow_unselected=True)
    with bound_selected_resolution([root],core):
        return _evaluate_native_guards(entry,core,frozen=frozen,whole_entry=whole_entry,allow_unselected=allow_unselected)


def _evaluate_native_guards(entry,core,*,frozen=None,whole_entry=None,allow_unselected=False):
    frozen=frozen or frozen_witnesses(core)
    role=_evaluate_role_guards(entry,core,frozen=frozen,whole_entry=whole_entry,allow_unselected=allow_unselected)
    if not role['allowed'] or not _has_target_guards(entry):return role
    target=_evaluate_target_guards(entry,core,frozen=frozen,whole_entry=whole_entry,allow_unselected=allow_unselected)
    if not target['allowed']:return target
    pending=role['search_only'] or target['search_only']
    return {'allowed':True,'reason':'search_only_source_target_required' if pending else 'all_native_guards_verified',
        'rules':role['rules']+target['rules'],'preserved_scopes':role['preserved_scopes']+target['preserved_scopes'],
        'search_only':pending}


def permission_scope(entry,core,*,source_data=None):
    if permission_envelope.required(entry) and native_status(entry)!='qualified':
        raise ValueError('mandatory permission source requires qualified source obligations')
    if source_data is not None and permission_envelope.authoritative_native_source(source_data,entry) and not permission_envelope.matches_source(source_data,entry):
        raise ValueError('actual native source transport mismatch')
    """v2 conditions and final permission share one strict selected-root audit."""
    if native_status(entry)=='qualified' and _has_target_guards(entry):
        root=entry.get('_native_guard_root') or entry
        result=admission(root,core)
        if not result['allowed'] or result.get('search_only'):raise ValueError('native source-target guard permission denied')
        # Also validates that a materialized member belongs to that exact root.
        _guard_context(entry)
        if root is not entry and not admission(entry,core,_nested=True,_whole_entry=root)['allowed']:
            raise ValueError('native member presentation guard permission denied')
    return _collect_permission_scope(entry,core)


def audit_final_scalar_preservation(entries,core):
    if not entries:return None
    with bound_selected_resolution(entries,core) as context:
        return permission_envelope.final_preservation(context,entries,core)
