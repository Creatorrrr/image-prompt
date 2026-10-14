"""Pure bindings for manually reviewed views of unchanged canonical facts.

This module does not qualify a source or prove natural-language entailment. The
native caller must first validate the actual full source, facts, ordinary units,
owners, effects and complete condition/dependency/profile closure. No self-hash
or Python result is a provenance/authentication capability. Compact lookup needs
an independently retained exact binding from that full validation/publication.
No guard evaluation, core selection, property projection or permission occurs.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re

MAX_VIEWS = 128
MAX_FACT_REFS = 8
MAX_ENDPOINT_REFS = 32
MAX_POSITIVE_BASIS = 8
MODES = frozenset({'effect', 'prerequisite', 'preservation', 'context'})
SCHEMA = 'photo-manual-semantic-role-view/v1'
COMPACT_SCHEMA = 'photo-manual-semantic-role-view-bindings/v1'
CONTEXT_FIELDS = frozenset({'candidate_id', 'actual_realization_ids', 'meaning_sha256',
    'catalog_by_id', 'facts', 'source_units', 'positive_fields', 'closure_snapshot'})
CLOSURE_FIELDS = frozenset({'owner_maps', 'effect_sets', 'guard_sets', 'dependencies',
    'profile_contracts', 'reference_sha256'})
VIEW_FIELDS = frozenset({'schema', 'id', 'candidate_id', 'realization_id', 'role_id',
    'spec_sha256', 'canonical_fact_refs', 'normal_anchors', 'endpoint_refs',
    'requires_refs', 'whole_closure_sha256', 'manual_semantic_facet',
    'whole_value_retained', 'manual_boundary_rationale'})
FACT_FIELDS = frozenset({'id', 'realization_id', 'pointer', 'quote', 'dimension',
    'target', 'property', 'mode', 'value', 'requires'})
HEX = re.compile(r'[0-9a-f]{64}\Z')
CID = re.compile(r'cand_[0-9a-f]{32}\Z')


def _bytes(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8')
    except (ValueError, TypeError, OverflowError, RecursionError) as exc:
        raise ValueError('finite JSON binding required') from exc


def _digest(value):
    return hashlib.sha256(_bytes(value)).hexdigest()


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _concrete(value):
    return _text(value) and '*' not in value and not value.endswith('.')


def _typed(value):
    if not isinstance(value, dict) or set(value) != {'type', 'value'} or not _concrete(value['type']):
        return False
    item = value['value']
    return (_concrete(item) or isinstance(item, list) and 1 <= len(item) <= 8
            and all(_concrete(row) for row in item) and len(set(item)) == len(item))


def _sha(value):
    return isinstance(value, str) and HEX.fullmatch(value) is not None


def _keys(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError('exact ' + label + ' fields required')


def _strings(value, label, *, empty=False, limit=None):
    if (not isinstance(value, list) or not empty and not value
            or limit is not None and len(value) > limit
            or any(not _text(item) for item in value)
            or len(set(value)) != len(value)):
        raise ValueError('bounded unique ' + label + ' required')


def _rows(value, limit, label, *, empty=False):
    if not isinstance(value, list) or not empty and not value or len(value) > limit:
        raise ValueError('bounded ' + label + ' required')


@dataclass(frozen=True, slots=True)
class ValidatedViewBindings:
    """Immutable structural result; never a source qualification certificate.

    Payload bytes prevent mutable input aliases. Constructing/reconstructing this
    class does not authenticate a source. External authority remains mandatory.
    """
    _payload: bytes

    @property
    def source_contract_sha256(self):
        return json.loads(self._payload)['source_contract_sha256']

    @property
    def views_sha256(self):
        return json.loads(self._payload)['views_sha256']


def _context(context):
    _keys(context, CONTEXT_FIELDS, 'source context')
    cid = context['candidate_id']
    if not isinstance(cid, str) or not CID.fullmatch(cid) or not _sha(context['meaning_sha256']):
        raise ValueError('actual CID and source meaning digest required')
    _strings(context['actual_realization_ids'], 'actual RIDs', limit=32)
    rids = set(context['actual_realization_ids'])
    _keys(context['closure_snapshot'], CLOSURE_FIELDS, 'whole closure')
    for key in CLOSURE_FIELDS - {'reference_sha256'}:
        if not isinstance(context['closure_snapshot'][key], dict) or set(context['closure_snapshot'][key]) != rids:
            raise ValueError('whole closure must retain every actual RID')
    if not isinstance(context['closure_snapshot']['reference_sha256'], dict):
        raise ValueError('complete reference closure required')
    if not isinstance(context['catalog_by_id'], dict):
        raise ValueError('actual catalog required')
    _rows(context['facts'], 4096, 'source facts', empty=True)
    facts = {}
    for fact in context['facts']:
        mode = fact.get('mode') if isinstance(fact, dict) else None
        _keys(fact, FACT_FIELDS | ({'operation', 'receivers'} if mode == 'effect' else set()), 'canonical fact')
        if (mode not in MODES or any(not _text(fact[key]) for key in
                ('id', 'realization_id', 'pointer', 'quote', 'dimension', 'target', 'property'))
                or fact['id'] in facts or fact['realization_id'] not in rids):
            raise ValueError('unique actual-RID canonical fact required')
        _keys(fact['value'], {'type', 'value'}, 'typed value')
        if not _typed(fact['value']):
            raise ValueError('actual typed value required')
        _strings(fact['requires'], 'original requires', empty=True)
        if mode == 'effect':
            if fact['operation'] not in {'set_value', 'add_entity', 'remove_entity', 'relocate', 'select_plane'}:
                raise ValueError('original operation required')
            _strings(fact['receivers'], 'original receivers', empty=True)
        facts[fact['id']] = fact
    _rows(context['positive_fields'], 2048, 'actual primary fields', empty=True)
    fields = {}
    for field in context['positive_fields']:
        _keys(field, {'realization_id', 'pointer', 'text'}, 'positive field')
        key = (field['realization_id'], field['pointer'])
        if (field['realization_id'] not in rids or not _text(field['pointer'])
                or not _text(field['text']) or key in fields):
            raise ValueError('unique full positive field required')
        fields[key] = field['text']
    _rows(context['source_units'], 2048, 'ordinary source units', empty=True)
    normal = {}
    for unit in context['source_units']:
        if not isinstance(unit, dict):
            raise ValueError('source-unit object required')
        if unit.get('disposition') != 'semantic':
            continue  # References/nonsemantic units never anchor a view.
        _keys(unit, {'realization_id', 'pointer', 'quote', 'fact_refs'} | {'disposition'}
              | ({'guard_refs'} if 'guard_refs' in unit else set()), 'ordinary semantic unit')
        key = (unit['realization_id'], unit['pointer'])
        if key in normal or key not in fields or unit['quote'] != fields[key]:
            raise ValueError('ordinary unit must be the exact full positive field')
        _strings(unit['fact_refs'], 'ordinary direct fact refs', empty=True)
        if 'guard_refs' in unit:
            _strings(unit['guard_refs'], 'ordinary guard refs', empty=True)
        for ref in unit['fact_refs']:
            fact = facts.get(ref)
            if (fact is None or (fact['realization_id'], fact['pointer']) != key
                    or fact['quote'] not in unit['quote']):
                raise ValueError('normal unit must directly support its own same-RID fact')
        normal[key] = unit
    _bytes(context)  # Finite JSON and independent snapshot, not source validation.
    return cid, rids, facts, fields, normal


def _requires(facts, refs, rid):
    required, visiting, visited = set(), set(), set()

    def visit(ref):
        if ref in visiting:
            raise ValueError('cyclic original requires')
        if ref in visited:
            return
        fact = facts.get(ref)
        if fact is None or fact['realization_id'] != rid:
            raise ValueError('requires must retain actual same-RID facts')
        visiting.add(ref)
        for child in fact['requires']:
            row = facts.get(child)
            if row is None or row['mode'] not in {'prerequisite', 'preservation'}:
                raise ValueError('requires must name actual frozen obligations')
            required.add(child)
            visit(child)
        visiting.remove(ref)
        visited.add(ref)
    for ref in refs:
        visit(ref)
    return required


def _validate_full_views(views, *, context):
    """Check exact manual-view bindings against caller-validated full data.

    Context is NOT a qualification boolean; its primary-field policy and whole
    source correctness must already have been checked by the native caller.
    Return value certifies structural bindings only, not semantic truth.
    """
    # Canonical roundtrip both validates finite JSON and prevents input aliases.
    context = json.loads(_bytes(context))
    views = json.loads(_bytes(views))
    cid, rids, facts, fields, normal = _context(context)
    _rows(views, MAX_VIEWS, 'manual role views', empty=True)
    whole_closure = _digest(context['closure_snapshot'])
    bindings, seen = [], set()
    for view in views:
        _keys(view, VIEW_FIELDS, 'manual role view')
        if (view['schema'] != SCHEMA or not _text(view['id']) or view['id'] in seen
                or view['candidate_id'] != cid or view['realization_id'] not in rids):
            raise ValueError('unique exact CID/RID role view required')
        seen.add(view['id'])
        rid, role_id = view['realization_id'], view['role_id']
        if not _text(role_id):
            raise ValueError('actual role required')
        spec = context['catalog_by_id'].get(role_id)
        if (not isinstance(spec, dict) or spec.get('id') != role_id
                or spec.get('semantic_role') not in {'direct', 'contextual'}
                or view['spec_sha256'] != _digest(spec)
                or view['whole_closure_sha256'] != whole_closure):
            raise ValueError('whole spec or owner/guard closure changed')
        if any(not _text(view[key]) for key in
               ('manual_semantic_facet', 'whole_value_retained', 'manual_boundary_rationale')):
            raise ValueError('explicit manual facet, retained value and boundary required')
        _rows(view['canonical_fact_refs'], MAX_FACT_REFS, 'canonical fact refs')
        refs = {}
        for ref in view['canonical_fact_refs']:
            _keys(ref, {'fact_id', 'fact_sha256', 'mode'}, 'canonical ref')
            fact = facts.get(ref['fact_id'])
            if (fact is None or ref['fact_id'] in refs or fact['realization_id'] != rid
                    or ref['mode'] != fact['mode'] or ref['fact_sha256'] != _digest(fact)
                    or fact['mode'] == 'context' and spec['semantic_role'] != 'contextual'
                    or fact['value']['type'] == 'frozen_property_reference/v1'):
                raise ValueError('unchanged canonical fact/mode/actual value required')
            refs[ref['fact_id']] = fact
        required = _requires(facts, refs, rid)
        _strings(view['requires_refs'], 'complete frozen obligation refs', empty=True)
        if set(view['requires_refs']) != required:
            raise ValueError('whole original requires closure required')
        _rows(view['normal_anchors'], MAX_POSITIVE_BASIS, 'positive normal anchors')
        anchors, anchored, anchor_seen = [], set(), set()
        for anchor in view['normal_anchors']:
            _keys(anchor, {'fact_id', 'pointer', 'source_unit_sha256', 'full_field_sha256',
                           'facet_quote', 'start', 'stop'}, 'normal anchor')
            fact = refs.get(anchor['fact_id'])
            key = (rid, anchor['pointer'])
            unit = normal.get(key)
            text = fields.get(key)
            start, stop = anchor['start'], anchor['stop']
            if (fact is None or unit is None or anchor['pointer'] != fact['pointer']
                    or fact['id'] not in unit['fact_refs']
                    or anchor['source_unit_sha256'] != _digest(unit)
                    or anchor['full_field_sha256'] != _digest(text)
                    or not _text(anchor['facet_quote']) or type(start) is not int or type(stop) is not int
                    or not 0 <= start < stop <= len(text)
                    or text[start:stop] != anchor['facet_quote']
                    or anchor['facet_quote'] not in fact['quote']):
                raise ValueError('facet needs exact canonical-quote and normal full-field anchor')
            # Pin the occurrence inside an actual canonical quote occurrence, not
            # a same-word occurrence in another sentence of the full field.
            quote_start = text.find(fact['quote'])
            inside_quote = False
            while quote_start != -1 and quote_start <= start:
                if stop <= quote_start + len(fact['quote']):
                    inside_quote = True
                    break
                quote_start = text.find(fact['quote'], quote_start + 1)
            if not inside_quote:
                raise ValueError('facet occurrence lies outside its canonical quote')
            anchor_key = (anchor['fact_id'], anchor['pointer'], start, stop)
            if anchor_key in anchor_seen:
                raise ValueError('duplicate normal anchor')
            anchor_seen.add(anchor_key)
            anchored.add(fact['id'])
            anchors.append({'fact_id': fact['id'], 'pointer_sha256': _digest(anchor['pointer']),
                'source_unit_sha256': anchor['source_unit_sha256'],
                'full_field_sha256': anchor['full_field_sha256'],
                'facet_sha256': _digest(anchor['facet_quote']), 'start': start, 'stop': stop})
        if anchored != set(refs):
            raise ValueError('every canonical ref needs its own direct normal anchor')
        _rows(view['endpoint_refs'], MAX_ENDPOINT_REFS, 'actual endpoint refs')
        endpoints, ep_seen = [], set()
        allowed = set(refs) | required
        for endpoint in view['endpoint_refs']:
            if not isinstance(endpoint, dict):
                raise ValueError('original endpoint position object required')
            fields_expected = {'fact_id', 'position'}
            if endpoint.get('position') == 'receiver':
                fields_expected |= {'index'}
            _keys(endpoint, fields_expected, 'endpoint position')
            fact = facts.get(endpoint.get('fact_id'))
            position = endpoint.get('position')
            index = endpoint.get('index')
            if fact is None or fact['id'] not in allowed or position not in {'target', 'receiver'}:
                raise ValueError('endpoint must name original canonical/frozen fact position')
            if position == 'receiver' and (fact['mode'] != 'effect' or type(index) is not int
                    or not 0 <= index < len(fact['receivers'])):
                raise ValueError('actual original receiver position required')
            ep_key = (fact['id'], position, index)
            if ep_key in ep_seen:
                raise ValueError('duplicate endpoint position')
            ep_seen.add(ep_key)
            endpoints.append(endpoint)
        mandatory = {(fact['id'], 'target', None) for fact in refs.values()}
        mandatory.update((fact['id'], 'receiver', i) for fact in refs.values()
                         for i in range(len(fact.get('receivers', []))))
        if not mandatory <= ep_seen:
            raise ValueError('all original canonical target and receiver positions required')
        for fact in refs.values():
            actual = {key: value for key, value in fact.items() if key not in {'pointer', 'quote'}}
            bindings.append({'view_id': view['id'], 'candidate_id': cid, 'realization_id': rid,
                'role_id': role_id, 'spec_sha256': view['spec_sha256'], 'fact_sha256': _digest(fact),
                'fact': actual, 'anchors': [a for a in anchors if a['fact_id'] == fact['id']],
                'endpoint_refs': endpoints, 'requires_refs': view['requires_refs'],
                'whole_closure_sha256': whole_closure, 'manual_view_sha256': _digest(view)})
    payload = {'schema': COMPACT_SCHEMA, 'candidate_id': cid,
        'source_contract_sha256': _digest(context), 'views_sha256': _digest(views), 'bindings': bindings}
    return ValidatedViewBindings(_bytes(payload))


def validate_full_views(views, *, context):
    """Return immutable structural bindings, never source qualification.

    The native caller supplies already validated actual full-source data; exact
    binding checks do not establish the truth/provenance of that caller input.
    Malformed JSON-shaped inputs fail consistently with ValueError.
    """
    try:
        return _validate_full_views(views, context=context)
    except (KeyError, TypeError, IndexError, RecursionError) as exc:
        raise ValueError('malformed manual role-view binding') from exc


def compact_views(validated, *, authoritative_contract_sha256):
    """Project structural bindings only within caller's full validated flow.

    The required external digest is supplied by the native full validator, not
    read from a candidate receipt. This is binding equality, not authentication.
    """
    if type(validated) is not ValidatedViewBindings:
        raise ValueError('full-view validation result required')
    result = json.loads(validated._payload)
    if not _sha(authoritative_contract_sha256) or result['source_contract_sha256'] != authoritative_contract_sha256:
        raise ValueError('independent authoritative full-source binding required')
    result['receipt_sha256'] = _digest(result)
    return result


def selected_support(validated_or_receipt, *, expected_binding, role_id, realization_id, fact_id):
    """Lookup only against an independently retained exact validated binding.

    expected_binding must come from full source qualification/publication. A
    receipt's own hash alone is never sufficient; absence or mismatch fails.
    Output is structural support, never eligible/qualified or a permission.
    """
    if not isinstance(expected_binding, dict) or set(expected_binding) != {
            'schema', 'candidate_id', 'source_contract_sha256', 'views_sha256', 'bindings', 'receipt_sha256'}:
        raise ValueError('independent exact expected binding required')
    expected = json.loads(_bytes(expected_binding))
    if (expected['schema'] != COMPACT_SCHEMA or not _sha(expected['receipt_sha256'])
            or expected['receipt_sha256'] != _digest({k: v for k, v in expected.items() if k != 'receipt_sha256'})):
        raise ValueError('invalid externally expected binding')
    if type(validated_or_receipt) is ValidatedViewBindings:
        actual = compact_views(validated_or_receipt,
                               authoritative_contract_sha256=expected['source_contract_sha256'])
    elif isinstance(validated_or_receipt, dict):
        actual = json.loads(_bytes(validated_or_receipt))
    else:
        raise ValueError('validated views or bound compact receipt required')
    if actual != expected:
        raise ValueError('view receipt differs from independent qualified-source binding')
    if any(not _text(value) for value in (role_id, realization_id, fact_id)):
        raise ValueError('exact role/RID/fact lookup required')
    rows = [row for row in actual['bindings'] if row['role_id'] == role_id
            and row['realization_id'] == realization_id and row['fact']['id'] == fact_id]
    if not rows:
        return None
    return {'support_kind': 'manual_semantic_role_view', 'view_ids': [row['view_id'] for row in rows],
            'fact': json.loads(_bytes(rows[0]['fact'])),
            'source_contract_sha256': actual['source_contract_sha256']}
