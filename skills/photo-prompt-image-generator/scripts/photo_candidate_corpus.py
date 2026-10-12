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

SCHEMA = 'photo-candidate-corpus/v1'
MANIFEST_SCHEMA = 'photo-candidate-corpus-source/v1'
MANIFEST_NAME = 'photo_candidate_corpus_manifest.json'
KINDS = frozenset({'visual_option', 'visual_profile', 'relationship_concept',
                   'relationship_mechanism', 'visual_bundle', 'diagnostic'})
MODULE_SCHEMAS = {
    'candidates': 'photo-candidate-module/v1',
    'slot_catalog': 'photo-slot-catalog/v1',
    'slot_bindings': 'photo-candidate-slot-bindings/v1',
    'policies': 'photo-candidate-policy/v1',
}
CORPUS_FIELDS = frozenset({'schema', 'candidates', 'slot_catalog', 'slot_bindings', 'policies'})
ID = re.compile(r'cand_[0-9a-f]{32}\Z')
BINDING_ID = re.compile(r'bind_[0-9a-f]{32}\Z')
TAG_ID = re.compile(r'[a-z][a-z0-9_]*\Z')


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


def validate_effects(value, field):
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    if not isinstance(value, dict) or set(value) != {'dimensions', 'properties'}:
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


def validate(corpus):
    if not isinstance(corpus, dict) or corpus.get('schema') != SCHEMA or set(corpus) != CORPUS_FIELDS:
        raise ValueError('native candidate corpus contract required')
    for field in ('candidates', 'slot_catalog', 'slot_bindings', 'policies'):
        if not isinstance(corpus[field], dict):
            raise ValueError(f'{field} must be an object')
    canonical_bytes(corpus)  # Reject NaN/Infinity anywhere, including policy metadata.
    candidates, catalog, bindings = (corpus[k] for k in ('candidates', 'slot_catalog', 'slot_bindings'))
    for candidate_id, row in candidates.items():
        if (not isinstance(candidate_id, str) or not ID.fullmatch(candidate_id) or not isinstance(row, dict)
                or set(row) != {'id', 'record_kind', 'content', 'effects', 'provenance'}
                or row.get('id') != candidate_id or row.get('record_kind') not in KINDS):
            raise ValueError(f'invalid global candidate identity: {candidate_id}')
        if not isinstance(row['content'], dict) or 'id' in row['content']:
            raise ValueError(f'{candidate_id}: content must not own a second identity')
        if {'affected_dimensions', 'affected_properties'} & set(row['content']):
            raise ValueError(f'{candidate_id}: effects have one canonical owner')
        validate_effects(row['effects'], candidate_id)
        if not isinstance(row['provenance'], list) or not row['provenance']:
            raise ValueError(f'{candidate_id}: source provenance required')
        for origin in row['provenance']:
            if (not isinstance(origin, dict) or not isinstance(origin.get('source'), str)
                    or not origin['source'] or not re.fullmatch(r'[0-9a-f]{64}', str(origin.get('sha256', '')))):
                raise ValueError(f'{candidate_id}: invalid source provenance')
    for tag, row in catalog.items():
        if (not isinstance(tag, str) or not TAG_ID.fullmatch(tag) or not isinstance(row, dict) or row.get('id') != tag
                or set(row) != {'id', 'description', 'dimensions', 'applicability'}
                or not isinstance(row['description'], str) or not isinstance(row['applicability'], dict)):
            raise ValueError(f'invalid role tag: {tag}')
        strings(row['dimensions'], tag + '.dimensions')
        validate_effects({'dimensions':row['dimensions'],'properties':[]}, tag)
    seen = set()
    for binding_id, row in bindings.items():
        if (not isinstance(binding_id, str) or not BINDING_ID.fullmatch(binding_id) or not isinstance(row, dict)
                or set(row) != {'id', 'candidate_id', 'slot_id', 'role', 'conditions', 'effects', 'weight'}
                or row['id'] != binding_id or row['candidate_id'] not in candidates
                or row['slot_id'] not in catalog or not isinstance(row['role'], str) or not row['role']
                or not isinstance(row['conditions'], dict)):
            raise ValueError(f'invalid/dangling binding: {binding_id}')
        if (type(row['weight']) not in (int, float) or not math.isfinite(row['weight'])
                or not 0 < row['weight'] <= 5):
            raise ValueError(f'{binding_id}: invalid weight')
        key = (row['candidate_id'], row['slot_id'], row['role'])
        if key in seen:
            raise ValueError(f'duplicate candidate/tag/role relationship: {key}')
        seen.add(key)
        if {'id', 'candidate_id', 'slot_id', 'binding_id', 'record_kind', 'effects',
                'affected_dimensions', 'affected_properties', 'content', 'provenance'} & set(row['conditions']):
            raise ValueError(f'{binding_id}: conditions cannot overwrite identity or effects')
        validate_effects(row['effects'], binding_id)
    # Candidate refs are explicit, qualified native IDs, never bare label aliases.
    def references(value):
        if isinstance(value, dict):
            for key, nested in value.items():
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


def entry(corpus, candidate_id, binding_id=None):
    """Native semantic record, optionally with an explicitly selected role."""
    record = corpus['candidates'][candidate_id]
    result = copy.deepcopy(record['content'])
    result['id'] = candidate_id
    result['record_kind'] = record['record_kind']
    effects = record['effects']
    if binding_id is not None:
        binding = corpus['slot_bindings'][binding_id]
        if binding['candidate_id'] != candidate_id:
            raise ValueError('role belongs to a different candidate')
        result.update(copy.deepcopy(binding['conditions']))
        result['binding_id'] = binding_id
        result['weight'] = binding['weight']
        effects = binding['effects']
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
