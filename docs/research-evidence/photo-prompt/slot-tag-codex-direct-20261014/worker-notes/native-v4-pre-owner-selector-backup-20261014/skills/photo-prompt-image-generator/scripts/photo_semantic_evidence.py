"""Manually authored native facts; semantic support is distinct from mutation.

Absent proof remains explicitly unqualified during stage 5C, never a native
completion/adoption certificate. Present older/invalid proof fails closed.
"""
from __future__ import annotations
import copy
import photo_candidate_corpus as c
import photo_candidate_realizations as realizations
from photo_precore_bridge import load
witnesses = load('photo_semantic_witnesses')

SCHEMA = 'photo-candidate-role-evidence/v4'
OWNER_SCHEMA = 'photo-native-owner-bindings/v2'
MODES = frozenset({'effect', 'prerequisite', 'preservation', 'context'})
OPERATIONS = frozenset({'set_value', 'add_entity', 'remove_entity', 'relocate', 'select_plane'})
NEGATIVE = frozenset({'confusion_boundaries', 'research_confusions', 'confounders',
    'failure_modes', 'excluded', 'exclusions', 'forbidden', 'avoid', 'negative',
    'research_source_urls', 'tags', 'facets', 'reject_substitutes', 'contrast_examples',
    'forbidden_prompt_terms', 'runtime_forbidden_labels', 'claim_limits', 'research_claim_limits',
    'provenance', 'acceptance', 'review', 'routing', 'conditions', 'applicability', 'retrieval_policy',
    'role_evidence', 'semantic_review', 'affected_dimensions', 'affected_properties',
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
POSITIVE_FIELDS = frozenset({'en', 'ko', 'ja', 'embedding_text', 'concept_units', 'relations',
    'definition', 'definitions_by_topic', 'paraphrases', 'manifestations', 'components',
    'semantics', 'authored_components', 'composition_instruction', 'concept_candidate',
    'render_requirements', 'render_gates', 'render_hard_gates'})
MISSING = object()
MAX_FACTS = 4096
MAX_UNITS = 2048
MAX_REALIZATIONS = 32
MAX_DEPENDENCY_DEPTH = 8


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


def _validate_owner_map(owner_map, facts):
    if (not isinstance(owner_map, dict) or set(owner_map) != {'schema', 'bindings'}
            or owner_map['schema'] != OWNER_SCHEMA or not isinstance(owner_map['bindings'], list)
            or len(owner_map['bindings']) > 32):
        raise ValueError('bounded explicit source owner bindings required')
    result = {}
    for row in owner_map['bindings']:
        if (not isinstance(row, dict) or set(row) != {'target', 'core_role', 'origin', 'introduced_by'}
                or not concrete_owned_value(row['target']) or not isinstance(row['core_role'],str)
                or row['core_role'] not in witnesses.CORE_ROLES
                or row['target'] in result or row['origin'] not in {'existing', 'introduced'}
                or row['origin'] == 'existing' and row['introduced_by'] is not None
                or row['origin'] == 'introduced' and not concrete_owned_value(row['introduced_by'])):
            raise ValueError('ambiguous or incomplete owner binding')
        result[row['target']] = row
    wanted = {fact['target'] for fact in facts}
    wanted.update(owner for fact in facts if fact['mode'] == 'effect' for owner in fact['receivers'])
    if set(result) != wanted:
        raise ValueError('owner map must cover the exact active fact/receiver owners')
    for target, row in result.items():
        if row['origin'] == 'introduced':
            creators = [fact for fact in facts if fact['id'] == row['introduced_by']]
            if (len(creators) != 1 or creators[0]['mode'] != 'effect'
                    or creators[0]['operation'] != 'add_entity' or creators[0]['target'] != target):
                raise ValueError('introduced owner needs its actual add_entity effect')
    return result


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


def validate(record, catalog, *, catalog_sha256=None, corpus=None, _stack=()):
    if '_semantic_evidence_guard' in record:
        raise ValueError('native source validation requires full positive source, not a compact guard')
    proof = record['content'].get('role_evidence', MISSING)
    if proof is MISSING:
        return  # Stage 5C only: source remains explicitly unqualified.
    if (not isinstance(proof, dict) or set(proof) != PROOF_FIELDS or proof['schema'] != SCHEMA
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
        units = [unit for unit in proof['source_units'] if isinstance(unit, dict) and unit.get('realization_id') == rid]
        covered, referenced = set(), set()
        for unit in units:
            if (not isinstance(unit, dict) or set(unit) != {'realization_id', 'pointer', 'quote', 'fact_refs', 'disposition'}
                    or unit['pointer'] in covered or unit['disposition'] not in {'semantic', 'nonsemantic'}
                    or unit['quote'] != positive_string(record, unit['pointer'], realization_id=rid)):
                raise ValueError('invalid full-string source-unit disposition')
            _strings(unit['fact_refs'], 'source unit facts', empty=unit['disposition'] == 'nonsemantic')
            if unit['disposition'] == 'nonsemantic' and unit['fact_refs']:
                raise ValueError('nonsemantic unit cannot supply facts')
            if any(ref not in facts or facts[ref]['realization_id'] != rid
                   or facts[ref]['pointer'] != unit['pointer'] or facts[ref]['quote'] not in unit['quote']
                   for ref in unit['fact_refs']):
                raise ValueError('unit borrows a foreign fact/source')
            covered.add(unit['pointer']); referenced.update(unit['fact_refs'])
        if not primary_paths(record, rid) <= covered or referenced != {fact['id'] for fact in selected}:
            raise ValueError('complete source-unit/fact disposition required')
    if any(not isinstance(unit, dict) or unit.get('realization_id') not in ids for unit in proof['source_units']):
        raise ValueError('source unit names a foreign RID')
    if record['record_kind'] == 'diagnostic' and (proof['roles'] or proof['facts']):
        raise ValueError('diagnostic cannot certify positive semantic facts')
    for tag, role in proof['roles'].items():
        if (tag not in catalog or not isinstance(role, dict) or set(role) !=
                {'spec_sha256', 'scope', 'realization_ids', 'fact_refs', 'support_modes'}):
            raise ValueError('unknown role or native role contract')
        spec = catalog[tag]
        _strings(role['realization_ids'], 'role RIDs'); _strings(role['fact_refs'], 'role facts')
        _strings(role['support_modes'], 'role modes')
        if (role['spec_sha256'] != c.digest(spec) or role['scope'] not in {'whole_record', 'positive_alternative'}
                or not set(role['realization_ids']) <= ids or not set(role['support_modes']) <= MODES
                or role['scope'] == 'whole_record' and set(role['realization_ids']) != ids):
            raise ValueError('role spec/scope/mode contract changed')
        covered = set()
        for ref in role['fact_refs']:
            fact = facts.get(ref)
            if (fact is None or fact['realization_id'] not in role['realization_ids']
                    or fact['mode'] not in role['support_modes'] or fact['dimension'] not in spec['dimensions']
                    or not any(fact['property'] == prefix.rstrip('.') or fact['property'].startswith(
                        prefix if prefix.endswith('.') else prefix+'.') for prefix in spec['property_prefixes'])
                    or fact['mode'] == 'context' and spec['semantic_role'] != 'contextual'):
                raise ValueError('role fact is outside its reviewed spec/mode/actual RID')
            covered.add(fact['realization_id'])
        if covered != set(role['realization_ids']):
            raise ValueError('role needs source support on every qualified RID')


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
    result.pop('source_units'); result.pop('review')
    for fact in result['facts']:
        fact.pop('pointer'); fact.pop('quote')
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
    result['compact_sha256'] = c.digest(result)
    return result


def qualification(spec, record, realization_id='base'):
    result = {'status': 'review_required', 'reason': 'native_source_unqualified_stage05c',
              'native_qualification': native_status(record), 'matched_properties': [],
              'meaning_terms': [], 'fact_refs': [], 'support_modes': []}
    if result['native_qualification'] != 'qualified':
        if result['native_qualification'] != 'unqualified':
            result['reason'] = 'incomplete_or_unsupported_native_evidence'
        return result
    proof = proof_of(record)
    if '_semantic_evidence_guard' not in record and (set(proof) != PROOF_FIELDS
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
    selected_effects = (realizations.effects(record, realization_id) if record['effects'].get('realizations')
                        else record['effects'])
    actual = with_projection(record, selected_effects)
    try:
        _selected_contract(proof, realization_id, actual)
    except (ValueError, KeyError, TypeError):
        return {**result, 'reason': 'qualified_actual_effect_set_changed'}
    if not selected:
        return {**result, 'reason': 'role_has_no_selected_fact'}
    return {**result, 'status': 'eligible', 'reason': 'source_reviewed_mode_specific_evidence',
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


def admission(entry, core, *, allow_unselected=False, _nested=False, _whole_entry=None):
    """Whole-cue obligations, including effects with no displayed role.

    Source carriers must already be frozen; introduced entities never self-witness
    a prerequisite. The separate permission check still sees every actual effect.
    """
    status = native_status(entry)
    if status == 'unqualified':
        return {'status': status, 'allowed': True, 'reason': 'stage05c_search_pool_only_not_native_adoption'}
    denied = {'status': 'invalid', 'allowed': False, 'reason': 'native_obligation_unverified'}
    if status != 'qualified':
        return denied
    try:
        proof = proof_of(entry); rid = entry.get('_realization_id', 'base')
        if '_realization_id' not in entry and rid not in proof['effect_sets']:
            if not allow_unselected:
                return {**denied, 'reason':'explicit_realization_selection_required'}
            alternatives = [admission(_guard_entry(proof, choice, entry.get('_native_dependency_selections', {})),
                                      core, allow_unselected=True, _nested=True) for choice in proof['effect_sets']]
            return {'status':'qualified', 'allowed':any(row['allowed'] for row in alternatives),
                    'reason':'search_probe_only_requires_explicit_realization'}
        actual = {'dimensions': sorted(entry.get('affected_dimensions', [])),
                  'properties': sorted(entry.get('affected_properties', []), key=property_key)}
        facts, bindings = _selected_contract(proof, rid, actual)
        frozen = frozen_witnesses(core); graph = frozen['graph']
        actual_owners = resolve_owner_bindings(proof, rid, graph)
        for binding in bindings.values():
            if binding['origin'] == 'existing' and binding['core_role'] not in graph['roles']:
                return denied
            if binding['origin'] == 'introduced' and binding['core_role'] in graph['roles']:
                return denied
        resolutions = []
        for fact in facts:
            _fact_valid_runtime(fact)
            if fact['mode'] not in {'prerequisite', 'preservation'}:
                continue
            binding = bindings[fact['target']]
            if binding['origin'] != 'existing':
                return denied
            matches = [row for row in frozen['facts'] if row['dimension'] == fact['dimension']
                       and row['property'] == fact['property']
                       and witnesses.owner_relation(graph, row['target'], actual_owners[fact['target']]) == 'overlap'
                       and _same_entity(graph, row['target'], actual_owners[fact['target']])]
            if len(matches) != 1:
                return denied
            match = matches[0]
            reference = fact['mode'] == 'preservation' and fact['value'] == {'type': 'frozen_property_reference/v1', 'value': 'same'}
            if not reference and witnesses.value_key(match['value']) != witnesses.value_key(fact['value']):
                return denied
            resolutions.append({'fact_id': fact['id'], 'core_assertion_id': match['assertion_id'],
                                'owner': actual_owners[fact['target']], 'value': copy.deepcopy(match['value'])})
        whole_entry = _whole_entry or entry
        guards_receipt = evaluate_native_guards(entry, core, frozen=frozen,
            whole_entry=whole_entry, allow_unselected=allow_unselected)
        if not guards_receipt['allowed']:
            return {**denied, 'reason':guards_receipt['reason']}
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
                                        extra_conditions=proof['guard_sets'][rid]['member_conditions'][cid]),
                                     core, allow_unselected=True, _nested=True, _whole_entry=whole_entry) for choice in choices]
                successful = [row for row in results if row['allowed']]
                if not successful:
                    return denied
                children.append({'candidate_id':cid,'search_only':True,'admissions':successful})
                continue
            result = admission(_guard_entry(guards['guard'], chosen, selections,
                                  extra_conditions=proof['guard_sets'][rid]['member_conditions'][cid]),
                               core, allow_unselected=allow_unselected, _nested=True, _whole_entry=whole_entry)
            if not result['allowed']:
                return denied
            used.update(result.get('used_dependency_ids', []))
            children.append({'candidate_id':cid,'realization_id':chosen,'admission':result})
        if not _nested and not allow_unselected and not set(selections) <= used:
            return {**denied, 'reason':'unused_or_foreign_dependency_selection'}
        return {'status': 'qualified', 'allowed': True, 'reason': 'whole_native_obligations_verified',
                'resolved_frozen_facts': resolutions, 'dependencies':children, 'native_guards':guards_receipt,
                'used_dependency_ids':sorted(used)}
    except (ValueError, KeyError, TypeError, IndexError):
        return denied


def _same_entity(graph, left, right):
    canonical, _ = witnesses.validate_graph(graph)
    return left in canonical and right in canonical and canonical[left] == canonical[right]


def _guard_entry(proof, rid, selections, *, extra_conditions=None):
    actual = proof['effect_sets'][rid]
    return {'_semantic_evidence_guard':proof, '_realization_id':rid,
            '_native_dependency_selections':selections, '_native_extra_conditions':copy.deepcopy(extra_conditions or []),
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
    facts = [fact for fact in proof['facts'] if fact['realization_id'] == rid]
    by_id = {}
    for fact in facts:
        _fact_valid_runtime(fact)
        if fact['id'] in by_id:
            raise ValueError('duplicate selected fact')
        by_id[fact['id']] = fact
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
    return facts, _validate_owner_map(proof['owner_maps'][rid], facts)


def _fact_valid_runtime(fact):
    # Full quotes are deliberately absent from sealed compact guards.
    sample = {**fact, 'pointer': '/content/en', 'quote': 'sealed source'}
    _fact_valid(sample)


def resolve_owner_bindings(proof, rid, graph):
    """Source addresses canonical roles; only the core supplies actual identity.

    Introduced local addresses are separate from frozen entities. They cannot
    witness existence or inherit an ungrounded disjointness exception.
    """
    witnesses.validate_graph(graph)
    result = {}
    for row in proof['owner_maps'][rid]['bindings']:
        role = row['core_role']
        if row['origin'] == 'existing':
            if role not in graph['roles']:
                raise ValueError('required canonical owner role has no explicit frozen binding')
            result[row['target']] = graph['roles'][role]
        else:
            if role in graph['roles']:
                raise ValueError('introduced role is already occupied in the frozen core')
            result[row['target']] = 'native-introduced:' + proof['meaning_sha256'] + ':' + rid + ':' + row['target']
    return result


def permission_scope(entry, core):
    """Resolve only explicit owner bindings; unknown alias overlap remains denied."""
    frozen = frozen_witnesses(core)
    effects = copy.deepcopy(entry.get('affected_properties', []))
    dimensions = set(entry.get('affected_dimensions', []))
    proof = proof_of(entry)
    if native_status(entry) == 'qualified':
        rid = entry.get('_realization_id', 'base')
        mapping = resolve_owner_bindings(proof, rid, frozen['graph'])
        actual = []
        for fact in proof['facts']:
            if fact['realization_id'] == rid and fact['mode'] == 'effect':
                for target in dict.fromkeys([fact['target'], *fact['receivers']]):
                    actual.append({'dimension': fact['dimension'], 'target': mapping[target], 'property': fact['property']})
        effects = [dict(zip(PROPERTY_FIELDS, key)) for key in dict.fromkeys(property_key(row) for row in actual)]
        selections = entry.get('_native_dependency_selections', {})
        for dependency, guards in selected_dependencies(proof, rid, selections):
            choices = dependency['realization_ids']; cid = dependency['candidate_id']
            chosen = selections.get(cid, choices[0] if len(choices)==1 else None)
            if chosen not in choices:
                raise ValueError('actual dependency realization must be selected before applying effects')
            child_dimensions, child_effects, _ = permission_scope(
                _guard_entry(guards['guard'], chosen, selections), core)
            dimensions.update(child_dimensions); effects.extend(child_effects)
    effects = [dict(zip(PROPERTY_FIELDS, key)) for key in dict.fromkeys(property_key(row) for row in effects)]
    return sorted(dimensions), effects, frozen['graph']


def existing_owner_allowed(entry, core, contract, catalog):
    return admission(entry, core)['allowed']


def property_scope_allowed(core, dimensions, effects, *, record=None, realization_id=None):
    """Property lock checks use the same explicit identities as native admission."""
    from photo_contracts import property_effects_allowed
    try:
        graph = frozen_witnesses(core)['graph']
        mapped = copy.deepcopy(effects)
        if record is not None and native_status(record) == 'qualified':
            proof = proof_of(record)
            rid = realization_id or record.get('_realization_id')
            if rid is None and len(proof['owner_maps']) == 1:
                rid = next(iter(proof['owner_maps']))
            if rid not in proof['owner_maps']:
                return False
            owners = resolve_owner_bindings(proof, rid, graph)
            for row in mapped or []:
                row['target'] = owners.get(row['target'], row['target'])
        return property_effects_allowed(core.get('intent_lock') or {}, dimensions, mapped, owner_graph=graph)
    except (ValueError, KeyError, TypeError):
        return False


SOURCE_GUARD_SCHEMA = 'photo-native-source-guards/v1'
GUARD_FIELDS = {
    'preserve_established_scope': {'id','kind','owner_role','scope_kind','known_absent','known_present','unknown'},
    'owner_relation': {'id','kind','relation','left_role','right_role'},
    'frozen_value': {'id','kind','owner_role','dimension','property','value'},
    'frozen_entity_relation': {'id','kind','left_role','right_role','dimension','property','value_type'},
}


def validate_source_guards(block):
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


def evaluate_native_guards(entry,core,*,frozen=None,whole_entry=None,allow_unselected=False):
    frozen=frozen or frozen_witnesses(core);graph=frozen['graph']
    canonical,ancestors=witnesses.validate_graph(graph)
    receipts=[];preserved=[];pending=False;whole_entry=whole_entry or entry
    for layer_index,conditions in enumerate(condition_layers(entry)):
        block=conditions.get('native_guards')
        if block is None:continue
        validate_source_guards(block)
        for rule in block['rules']:
            roles={key:graph['roles'].get(rule[key]) for key in ('owner_role','left_role','right_role') if key in rule}
            if any(owner is None for owner in roles.values()):
                return {'allowed':False,'reason':'native_guard_owner_not_established'}
            receipt={'layer':layer_index,'rule_id':rule['id'],'kind':rule['kind'],'owners':roles}
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
                    if allow_unselected and _pending_dependency_choice(proof,whole_rid,selections):
                        pending=True;receipt['effect_check']='explicit_dependency_selection_required'
                    else:
                        dims,effects,owner_graph=permission_scope(whole_entry,core)
                        from photo_contracts import property_effects_allowed
                        locks={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':item['dimension'],'target':item['target'],
                                                   'property':item['property']} for item in inv['items']]}
                        if not property_effects_allowed(locks,dims,effects,owner_graph=owner_graph):
                            return {'allowed':False,'reason':'native_established_scope_effect_overlap'}
                    preserved.append(copy.deepcopy(scope))
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
