"""Native shared candidate corpus. Imports perform no filesystem or network IO.

Candidate identity is independent of role tags. This module accepts only the
native corpus contract; migration input parsing belongs outside the runtime.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from pathlib import Path

SCHEMA = 'photo-candidate-corpus/v3'
MANIFEST_SCHEMA = 'photo-candidate-corpus-source/v3'
MANIFEST_NAME = 'photo_candidate_corpus_manifest.json'
KINDS = frozenset({'visual_option', 'visual_profile', 'relationship_concept',
                   'relationship_mechanism', 'visual_bundle', 'diagnostic'})
MODULE_SCHEMAS = {
    'candidates': 'photo-candidate-module/v3',
    'slot_catalog': 'photo-slot-catalog/v2',
    'slot_bindings': 'photo-candidate-slot-bindings/v3',
    'policies': 'photo-candidate-policy/v1',
}
CORPUS_FIELDS = frozenset({'schema', 'candidates', 'slot_catalog', 'slot_bindings', 'policies'})
ID = re.compile(r'cand_[0-9a-f]{32}\Z')
BINDING_ID = re.compile(r'bind_[0-9a-f]{32}\Z')
TAG_ID = re.compile(r'[a-z][a-z0-9_]*\Z')
INTRINSIC_CONDITION_FIELDS = frozenset({'for_any', 'for_all', 'exclude_for_any', 'not_for',
    'requires_any_tags', 'requires_any', 'requires_all_tags', 'requires_all',
    'exclude_any_tags', 'exclude_any', 'requires_primary_any_tags', 'requires_facets', 'exclude_facets',
    'subject_applicability', 'requires_adult_context'})


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def decode(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'nonfinite JSON: {value}')))


def strings(value, field):
    if (not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value)
            or len(value) != len(set(value))):
        raise ValueError(f'{field}: expected unique nonempty strings')
    return value


def validate_effects(value, field, *, branches=True):
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    if (not isinstance(value, dict) or not {'dimensions', 'properties'} <= set(value)
            or set(value) - {'dimensions', 'properties', 'realizations'}
            or (not branches and 'realizations' in value)):
        raise ValueError(f'{field}: dimensions and properties are required')
    dimensions = strings(value['dimensions'], field + '.dimensions')
    if not set(dimensions) <= AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
        raise ValueError(f'{field}: unknown effect dimension')
    properties = value['properties']
    if not isinstance(properties, list):
        raise ValueError(f'{field}: properties must be a list')
    seen = set()
    for row in properties:
        if (not isinstance(row, dict) or set(row) != {'dimension', 'target', 'property'}
                or any(not isinstance(v, str) or not v.strip() for v in row.values())
                or row['dimension'] not in dimensions):
            raise ValueError(f'{field}: invalid property ownership/effect')
        key = tuple(row[k] for k in ('dimension', 'target', 'property'))
        if key in seen:
            raise ValueError(f'{field}: duplicate property effect')
        seen.add(key)
    if 'realizations' in value:
        contract = value['realizations']
        if (not isinstance(contract, dict) or set(contract) != {'mode', 'branches'}
                or contract['mode'] not in {'one', 'optional'}
                or not isinstance(contract['branches'], list) or not contract['branches']):
            raise ValueError(f'{field}: invalid conditional effect contract')
        seen_ids = set()
        for row in contract['branches']:
            if (not isinstance(row, dict) or not {'id', 'conditions', 'effects', 'context_terms'} <= set(row)
                    or set(row) - {'id', 'conditions', 'effects', 'context_terms', 'member_candidate_ids', 'component_units', 'concept_units'}
                    or not isinstance(row['id'], str) or not TAG_ID.fullmatch(row['id'])
                    or row['id'] == 'base' or row['id'] in seen_ids):
                raise ValueError(f'{field}: invalid or duplicate realization')
            seen_ids.add(row['id'])
            validate_conditions(row['conditions'], field + '.' + row['id'])
            strings(row['context_terms'], field + '.context_terms')
            if 'concept_units' in row:
                strings(row['concept_units'], field + '.concept_units')
            validate_effects(row['effects'], field + '.' + row['id'], branches=False)
            if 'member_candidate_ids' in row:
                strings(row['member_candidate_ids'], field + '.members')
            if 'component_units' in row:
                if not isinstance(row['component_units'], dict):
                    raise ValueError(f'{field}: component realizations must be an object')
                for key, units in row['component_units'].items():
                    if not isinstance(key, str) or not strings(units, field + '.component_units'):
                        raise ValueError(f'{field}: empty component realization')


def validate_conditions(conditions, field):
    if not isinstance(conditions, dict) or not set(conditions) <= INTRINSIC_CONDITION_FIELDS:
        raise ValueError(f'{field}: invalid intrinsic condition contract')
    for key, value in conditions.items():
        if key == 'requires_adult_context':
            if type(value) is not bool:
                raise ValueError(f'{field}: adult condition must be boolean')
        elif key == 'subject_applicability':
            if not isinstance(value, dict):
                raise ValueError(f'{field}: subject policy must be an object')
        else:
            strings(value, field + '.' + key)


def validate(corpus):
    if not isinstance(corpus, dict) or corpus.get('schema') != SCHEMA or set(corpus) != CORPUS_FIELDS:
        raise ValueError('native candidate corpus contract required')
    for field in ('candidates', 'slot_catalog', 'slot_bindings', 'policies'):
        if not isinstance(corpus[field], dict):
            raise ValueError(f'{field} must be an object')
    canonical_bytes(corpus)  # Reject NaN/Infinity anywhere, including policy metadata.
    candidates, catalog, bindings = (corpus[k] for k in ('candidates', 'slot_catalog', 'slot_bindings'))
    catalog_sha256 = digest(catalog)
    for candidate_id, row in candidates.items():
        if (not isinstance(candidate_id, str) or not ID.fullmatch(candidate_id) or not isinstance(row, dict)
                or set(row) != {'id', 'record_kind', 'content', 'conditions', 'effects', 'provenance'}
                or row.get('id') != candidate_id or row.get('record_kind') not in KINDS):
            raise ValueError(f'invalid global candidate identity: {candidate_id}')
        if not isinstance(row['content'], dict) or 'id' in row['content']:
            raise ValueError(f'{candidate_id}: content must not own a second identity')
        if {'affected_dimensions', 'affected_properties'} & set(row['content']):
            raise ValueError(f'{candidate_id}: effects have one canonical owner')
        if INTRINSIC_CONDITION_FIELDS & set(row['content']):
            raise ValueError(f'{candidate_id}: intrinsic conditions have one canonical owner')
        validate_conditions(row['conditions'], candidate_id)
        validate_effects(row['effects'], candidate_id)
        import photo_candidate_realizations
        photo_candidate_realizations.validate_content(row)
        for branch in row['effects'].get('realizations', {}).get('branches', []):
            available = {p['candidate_id'] for p in row['content'].get('member_candidates', [])}
            if not set(branch.get('member_candidate_ids', [])) <= available:
                raise ValueError(f'{candidate_id}: realization references a foreign bundle member')
            component_ids = {p['id'] for p in row['content'].get('components', [])}
            if not set(branch.get('component_units', {})) <= component_ids:
                raise ValueError(f'{candidate_id}: realization references a foreign component')
        if not isinstance(row['provenance'], list) or not row['provenance']:
            raise ValueError(f'{candidate_id}: source provenance required')
        for origin in row['provenance']:
            if (not isinstance(origin, dict) or not isinstance(origin.get('source'), str)
                    or not origin['source'] or not re.fullmatch(r'[0-9a-f]{64}', str(origin.get('sha256', '')))):
                raise ValueError(f'{candidate_id}: invalid source provenance')
        import photo_semantic_evidence
        photo_semantic_evidence.validate(row, catalog, catalog_sha256=catalog_sha256)
    import photo_slot_semantics
    for tag, row in catalog.items():
        if (not isinstance(tag, str) or not TAG_ID.fullmatch(tag) or not isinstance(row, dict) or row.get('id') != tag
                or not isinstance(row['description'], str) or not isinstance(row['applicability'], dict)):
            raise ValueError(f'invalid role tag: {tag}')
        photo_slot_semantics.validate(tag, row, set(catalog), strings)
        strings(row['dimensions'], tag + '.dimensions')
        validate_effects({'dimensions':row['dimensions'],'properties':[]}, tag)
    seen = set()
    for binding_id, row in bindings.items():
        if (not isinstance(binding_id, str) or not BINDING_ID.fullmatch(binding_id) or not isinstance(row, dict)
                or set(row) != {'id', 'candidate_id', 'slot_id', 'role', 'semantic_role', 'conditions', 'weight'}
                or row['id'] != binding_id or row['candidate_id'] not in candidates
                or row['slot_id'] not in catalog or not isinstance(row['role'], str) or not row['role']
                or not isinstance(row['conditions'], dict)
                or row['semantic_role'] != catalog[row['slot_id']]['semantic_role']):
            raise ValueError(f'invalid/dangling binding: {binding_id}')
        if (type(row['weight']) not in (int, float) or not math.isfinite(row['weight'])
                or not 0 < row['weight'] <= 5):
            raise ValueError(f'{binding_id}: invalid weight')
        key = (row['candidate_id'], row['slot_id'])
        if key in seen:
            raise ValueError(f'duplicate candidate/tag relationship: {key}')
        seen.add(key)
        if (set(row['conditions']) != {'subject_applicability'}
                or not isinstance(row['conditions']['subject_applicability'], dict)):
            raise ValueError(f'{binding_id}: role conditions cannot override intrinsic meaning')
    # Candidate refs are explicit, qualified native IDs, never bare label aliases.
    def references(value):
        if isinstance(value, str):
            if ID.fullmatch(value) and value not in candidates:
                raise ValueError(f'dangling candidate reference: {value}')
            if BINDING_ID.fullmatch(value) and value not in bindings:
                raise ValueError(f'dangling binding reference: {value}')
        if isinstance(value, dict):
            if 'candidate_id' in value and 'binding_id' in value:
                binding = bindings.get(value['binding_id'])
                if binding is None or binding['candidate_id'] != value['candidate_id']:
                    raise ValueError('referenced binding belongs to another candidate')
            for key, nested in value.items():
                references(key)
                if key in {'candidate_id', 'candidate_ref', 'canonical_candidate_ref'} and isinstance(nested, str) and nested not in candidates:
                    raise ValueError(f'dangling candidate reference: {nested}')
                if key == 'candidate_refs':
                    for candidate_id in strings(nested, key):
                        if candidate_id not in candidates:
                            raise ValueError(f'dangling candidate reference: {candidate_id}')
                references(nested)
        elif isinstance(value, list):
            for nested in value:
                references(nested)
    references(corpus)
    visiting,visited=set(),set()
    def bundle_members(candidate_id):
        if candidate_id in visiting:
            raise ValueError('cyclic bundle member reference: '+candidate_id)
        if candidate_id in visited:return
        visiting.add(candidate_id)
        for member in candidates[candidate_id]['content'].get('member_candidates',[]):
            bundle_members(member['candidate_id'])
        visiting.remove(candidate_id);visited.add(candidate_id)
    for candidate_id in candidates:bundle_members(candidate_id)
    for candidate_id, row in candidates.items():
        seen_refs = {candidate_id}
        target = row['content'].get('canonical_candidate_ref')
        while target:
            if target not in candidates or target in seen_refs:
                raise ValueError(f'{candidate_id}: missing or cyclic canonical candidate reference')
            seen_refs.add(target)
            target = candidates[target]['content'].get('canonical_candidate_ref')
    return corpus


def load(assets, manifest_name=MANIFEST_NAME):
    assets = Path(assets).resolve()
    manifest = decode((assets / manifest_name).read_bytes())
    if (not isinstance(manifest, dict) or set(manifest) != {'schema', 'modules'}
            or manifest.get('schema') != MANIFEST_SCHEMA or not isinstance(manifest['modules'], list)):
        raise ValueError('native candidate source manifest required')
    corpus = {'schema': SCHEMA, 'candidates': {}, 'slot_catalog': {}, 'slot_bindings': {}, 'policies': {}}
    seen = set()
    for row in manifest['modules']:
        if (not isinstance(row, dict) or set(row) != {'file', 'kind'}
                or row['kind'] not in MODULE_SCHEMAS or not isinstance(row['file'], str)):
            raise ValueError('invalid source module')
        path = (assets / row['file']).resolve()
        if path.parent != assets or path.suffix != '.json' or path in seen:
            raise ValueError('duplicate or escaping source module')
        seen.add(path)
        payload = decode(path.read_bytes())
        field = row['kind']
        if (not isinstance(payload, dict) or set(payload) != {'schema', field} or payload['schema'] != MODULE_SCHEMAS[field]
                or not isinstance(payload[field], dict)):
            raise ValueError(f'{path.name}: invalid module schema')
        target = corpus[field]
        for key, value in payload[field].items():
            if key in target:
                raise ValueError(f'duplicate authored owner: {field}.{key}')
            target[key] = value
    return validate(corpus)


def entry(corpus, candidate_id, binding_id=None, *, realization_id=None):
    """Native semantic record, optionally with an explicitly selected role."""
    record = corpus['candidates'][candidate_id]
    result = copy.deepcopy(record['content'])
    result['id'] = candidate_id
    result['record_kind'] = record['record_kind']
    if '_semantic_evidence_guard' in record:
        result['_semantic_evidence_guard'] = copy.deepcopy(record['_semantic_evidence_guard'])
    result.update(copy.deepcopy(record['conditions']))
    effects = record['effects']
    if realization_id is not None:
        import photo_candidate_realizations as realizations
        effects = realizations.effects(record, realization_id)
        selected = realizations.branch(record, realization_id)
        result['_realization_id'] = realization_id
        result.update(realizations.project_content(record, realization_id))
        result.pop('realization_content', None)
        if selected:
            if 'concept_units' in selected:
                result['concept_units'] = copy.deepcopy(selected['concept_units'])
            wanted = realizations.member_ids(record, realization_id)
            if 'member_candidates' in result:
                result['member_candidates'] = [p for p in result['member_candidates'] if p['candidate_id'] in wanted]
            for component in result.get('components', []):
                if component['id'] in selected.get('component_units', {}):
                    component['concept_units'] = copy.deepcopy(selected['component_units'][component['id']])
    if binding_id is not None:
        binding = corpus['slot_bindings'][binding_id]
        if binding['candidate_id'] != candidate_id:
            raise ValueError('role belongs to a different candidate')
        result['_role_conditions'] = copy.deepcopy(binding['conditions'])
        result['_presentation_role'] = binding['slot_id']
        result['_semantic_role'] = binding['semantic_role']
        result['binding_id'] = binding_id
        result['weight'] = binding['weight']
    result['affected_dimensions'] = list(effects['dimensions'])
    result['affected_properties'] = copy.deepcopy(effects['properties'])
    return result


def role_entries(corpus, tag):
    """A native role view, not a source tree or candidate identity namespace."""
    for binding_id, binding in corpus['slot_bindings'].items():
        if binding['slot_id'] == tag:
            yield entry(corpus, binding['candidate_id'], binding_id)


def all_entries(corpus, kinds=None):
    for candidate_id, record in corpus['candidates'].items():
        if kinds is None or record['record_kind'] in kinds:
            yield entry(corpus, candidate_id)
