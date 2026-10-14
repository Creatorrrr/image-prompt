"""Source-bound role qualifications; never a tag-based search admission filter.

The complete evidence is verified while maintaining the authored corpus. A
sealed layout can carry its compact projection without loading every payload.
The evidence is a recorded semantic judgement, not an accuracy certificate.
"""
from __future__ import annotations

import copy
import re
import photo_candidate_corpus as c
import photo_candidate_realizations as realizations

SCHEMA = 'photo-candidate-role-evidence/v2'
NEGATIVE = frozenset({'confusion_boundaries', 'research_confusions', 'confounders',
    'failure_modes', 'excluded', 'exclusions', 'forbidden', 'avoid', 'negative',
    'research_source_urls', 'tags', 'facets', 'reject_substitutes', 'contrast_examples',
    'forbidden_prompt_terms', 'runtime_forbidden_labels', 'claim_limits',
    'research_claim_limits', 'provenance', 'acceptance', 'review', 'routing',
    'conditions', 'applicability', 'retrieval_policy'})
FACT_FIELDS = frozenset({'pointer', 'quote', 'dimension', 'target', 'property',
                         'realization_id', 'required_carriers'})
PROPERTY_FIELDS = ('dimension', 'target', 'property')
CARRIER_TYPE = re.compile(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*\Z')
MISSING = object()


def meaning_material(record):
    content = {k:v for k,v in record['content'].items()
               if k not in {'role_evidence', 'semantic_review'}}
    return {'id':record['id'], 'record_kind':record['record_kind'], 'content':content,
            'conditions':record['conditions'], 'effects':record['effects']}


def meaning_sha256(record):
    return c.digest(meaning_material(record))


def positive_string(record, pointer, *, realization_id=None):
    if not isinstance(pointer, str) or not pointer.startswith('/content/'):
        raise ValueError('role evidence must quote primary positive content')
    keys = [raw.replace('~1', '/').replace('~0', '~') for raw in pointer[1:].split('/')]
    if (set(keys) & (NEGATIVE | {'role_evidence', 'semantic_review'})
            or keys[1] == 'activation' and
            (len(keys) < 4 or keys[2] not in {'exact_terms', 'project_glossary_aliases'})):
        raise ValueError('routing, negative or review metadata is not positive evidence')
    if (keys[1] == 'realization_content' and
            (realization_id is None or len(keys) < 4 or keys[2] != realization_id)):
        raise ValueError('positive source belongs to a different realization')
    value = record
    try:
        for key in keys:
            if isinstance(value, list):
                if not key.isdigit() or str(int(key)) != key:
                    raise ValueError('noncanonical source array index')
                value = value[int(key)]
            else:
                value = value[key]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('missing positive source pointer') from exc
    if not isinstance(value, str):
        raise ValueError('role quote pointer must name a source string')
    return value


def carrier_requirements_valid(value):
    """An empty list is an explicit reviewed decision, never an inferred default."""
    if not isinstance(value, list):
        return False
    seen = set()
    for row in value:
        if (not isinstance(row, dict) or set(row) != {'target', 'carrier'}
                or not concrete_owned_value(row['target'])
                or not isinstance(row['carrier'], str)
                or not CARRIER_TYPE.fullmatch(row['carrier'])):
            return False
        key = (row['target'], row['carrier'])
        if key in seen:
            return False
        seen.add(key)
    return True


def concrete_owned_value(value):
    """Preserve existing authored owner/property spelling, including named owners."""
    return (isinstance(value, str) and bool(value.strip())
            and '*' not in value and not value.endswith('.'))


def property_key(value):
    return tuple(value[k] for k in ('dimension', 'target', 'property'))


def validate(record, catalog, *, catalog_sha256=None):
    proof = record['content'].get('role_evidence', MISSING)
    if proof is MISSING:
        return
    if (not isinstance(proof, dict) or set(proof) != {
            'schema', 'meaning_sha256', 'catalog_sha256', 'complete', 'roles', 'review'}
            or proof['schema'] != SCHEMA or proof['complete'] is not True
            or proof['meaning_sha256'] != meaning_sha256(record)
            or proof['catalog_sha256'] != (catalog_sha256 or c.digest(catalog))
            or not isinstance(proof['roles'], dict) or not isinstance(proof['review'], dict)):
        raise ValueError(record['id']+': stale or incomplete role qualification')
    ids = set(realizations.ids(record))
    if record['record_kind'] == 'diagnostic' and proof['roles']:
        raise ValueError('diagnostic record cannot qualify positive roles')
    for tag, role in proof['roles'].items():
        if (tag not in catalog or not isinstance(role, dict) or set(role) !=
                {'spec_sha256', 'scope', 'realization_ids', 'evidence'}):
            raise ValueError('unknown role or qualification field')
        spec = catalog[tag]
        if (role['spec_sha256'] != c.digest(spec)
                or role['scope'] not in {'whole_record', 'positive_alternative'}
                or not c.strings(role['realization_ids'], tag+'.realizations')
                or not set(role['realization_ids']) <= ids
                or (role['scope'] == 'whole_record' and set(role['realization_ids']) != ids)
                or not isinstance(role['evidence'], list) or not role['evidence']):
            raise ValueError('role definition or selection scope changed')
        covered = set()
        seen = set()
        for fact in role['evidence']:
            if not isinstance(fact, dict) or set(fact) != FACT_FIELDS:
                raise ValueError('per-realization fact and reviewed carrier requirements are mandatory')
            rid = fact['realization_id']
            if not isinstance(rid, str) or rid not in role['realization_ids']:
                raise ValueError('role evidence names an unqualified realization')
            if (not isinstance(fact['quote'], str) or not fact['quote'].strip()
                    or fact['quote'] not in positive_string(record, fact['pointer'], realization_id=rid)
                    or fact['dimension'] not in spec['dimensions']
                    or any(not concrete_owned_value(fact[k]) for k in ('target', 'property'))
                    or not any(fact['property'] == p.rstrip('.')
                               or fact['property'].startswith(p if p.endswith('.') else p+'.')
                               for p in spec['property_prefixes'])
                    or not carrier_requirements_valid(fact['required_carriers'])):
                raise ValueError('role quote, owned meaning or carrier declaration differs from source contract')
            properties = {property_key(p) for p in realizations.effects(record, rid)['properties']}
            if property_key(fact) not in properties:
                raise ValueError('fact has no matching property in its exact source realization')
            digest = c.digest(fact)
            if digest in seen:
                raise ValueError('duplicate source evidence')
            seen.add(digest)
            covered.add(rid)
        if covered != set(role['realization_ids']):
            raise ValueError('each qualified realization requires its own positive source evidence')


def compact(record):
    """Called only when building a layout from the fully validated corpus.

    RID and carrier requirements remain semantic guards; only source quotes and
    pointers are dropped. The layout seal binds this projection to full sources.
    """
    proof = record['content'].get('role_evidence', MISSING)
    if proof is MISSING:
        return None
    return {'schema': SCHEMA, 'meaning_sha256': proof['meaning_sha256'],
            'catalog_sha256': proof['catalog_sha256'], 'complete': proof['complete'],
            'roles': {tag: {key: (copy.deepcopy(value) if key != 'evidence' else [
                {field: copy.deepcopy(fact[field]) for field in
                 (*PROPERTY_FIELDS, 'realization_id', 'required_carriers')} for fact in value])
                for key, value in role.items()} for tag, role in proof['roles'].items()}}


def qualification(spec, record, realization_id='base'):
    proof = record.get('_semantic_evidence_guard',
                       record.get('content', {}).get('role_evidence', MISSING))
    if proof is MISSING:
        return None
    result = {'status': 'review_required', 'reason': 'incomplete_native_role_evidence',
              'matched_properties': [], 'meaning_terms': []}
    if not isinstance(proof, dict) or proof.get('schema') != SCHEMA or proof.get('complete') is not True:
        return result
    role = proof['roles'].get(spec['id'])
    if role is None:
        return {**result, 'status': 'incompatible',
                'reason': 'reviewed_complete_meaning_does_not_support_role'}
    if role['spec_sha256'] != c.digest(spec):
        return {**result, 'reason': 'role_definition_changed_since_source_review'}
    if realization_id not in role['realization_ids']:
        return {**result, 'status': 'incompatible',
                'reason': 'role_not_supported_by_selected_realization'}
    selected = (realizations.effects(record, realization_id) if record['effects'].get('realizations')
                else record['effects'])
    properties = {property_key(p) for p in selected['properties']}
    facts = [fact for fact in role['evidence'] if fact.get('realization_id') == realization_id]
    if not facts or any('required_carriers' not in fact or
                        not carrier_requirements_valid(fact['required_carriers']) for fact in facts):
        return result
    # Every fact is bound to this branch; one coincidentally shared property
    # cannot hide a stale or foreign second fact.
    if any(property_key(fact) not in properties for fact in facts):
        return {**result, 'reason': 'qualified_property_missing_from_selected_realization'}
    matched = [dict(zip(PROPERTY_FIELDS, key)) for key in
               dict.fromkeys(property_key(fact) for fact in facts)]
    return {**result, 'status': 'eligible', 'reason': 'source_reviewed_owned_positive_evidence',
            'matched_properties': matched}


def grounded_carriers(core):
    """Read explicit frozen owner anatomy; no noun/category or candidate inference.

    Core v3 normalization already binds active spans to the requesting envelope.
    Here we additionally require each carrier declaration to use those exact
    active span IDs and carry frozen baseline evidence. Values are extensible:
    'hair' does not imply face, nails, a live actor or any other carrier.
    """
    if core.get('contract_version') != 'photo-authorial-core/v3':
        return set()
    spans = (core.get('request_binding') or {}).get('active_spans') or []
    active = {row.get('source_span_id', row.get('span_id')) for row in spans
              if isinstance(row, dict) and isinstance(row.get('text'), str) and row['text'].strip()
              and isinstance(row.get('source_span_id', row.get('span_id')), str)
              and row.get('source_span_id', row.get('span_id'))}
    baseline = core.get('baseline_prompt_en', '')
    result = set()
    for row in core.get('semantic_assertions') or []:
        if not isinstance(row, dict):
            continue
        axes = row.get('axes') or {}
        if not isinstance(axes, dict) or 'existing_carriers' not in axes:
            continue
        source_ids = row.get('source_span_ids')
        target = axes.get('carrier_target')
        carriers = axes.get('existing_carriers')
        phrases = row.get('evidence')
        if (row.get('dimension') != 'subject' or row.get('polarity') != 'required'
                or 'subject' not in (row.get('affected_dimensions') or [])
                or not isinstance(source_ids, list) or not source_ids
                or any(not isinstance(value, str) for value in source_ids)
                or len(set(source_ids)) != len(source_ids) or not set(source_ids) <= active
                or not concrete_owned_value(target)
                or not isinstance(carriers, list) or not carriers
                or any(not isinstance(value, str) or not CARRIER_TYPE.fullmatch(value) for value in carriers)
                or len(set(carriers)) != len(carriers)
                or not isinstance(phrases, dict) or not phrases
                or not isinstance(baseline, str)
                or any(not isinstance(value, str) or not value.strip() or value not in baseline
                       for value in phrases.values())):
            continue
        result.update((target, carrier) for carrier in carriers)
    return result


def existing_owner_allowed(entry, core, contract, catalog):
    """All active facts need explicitly grounded existing carriers, if declared.

    This checks existence only. Property/dimension permissions and frozen owner
    aliases are enforced separately; existence never grants mutation permission.
    'contract' and 'catalog' remain caller inputs but categories/role owners do
    not establish anatomy. An unqualified legacy record has no native assertion.
    """
    proof = entry.get('_semantic_evidence_guard', entry.get('role_evidence', MISSING))
    if proof is MISSING:
        return True
    if not isinstance(proof, dict) or proof.get('schema') != SCHEMA or proof.get('complete') is not True:
        return False
    rid = entry.get('_realization_id', 'base')
    active = {property_key(p) for p in entry.get('affected_properties', [])}
    required = set()
    for role in proof['roles'].values():
        if rid not in role['realization_ids']:
            continue
        if any(not isinstance(fact, dict) or 'realization_id' not in fact
               or 'required_carriers' not in fact
               or not carrier_requirements_valid(fact['required_carriers'])
               for fact in role['evidence']):
            return False
        facts = [fact for fact in role['evidence'] if fact['realization_id'] == rid]
        if not facts:
            return False
        for fact in facts:
            if property_key(fact) not in active:
                return False
            required.update((row['target'], row['carrier']) for row in fact['required_carriers'])
    return required <= grounded_carriers(core)
