"""Candidate-free, source-grounded frozen facts and explicit owner relationships.

No source catalog, classifier, retrieval, model, or filesystem dependency. Values
are exact typed strings/string lists, never guessed semantic entailments.
"""
from __future__ import annotations
import copy

SCHEMA = 'photo-frozen-semantics/v1'
MAX_ROWS = 64
MAX_OWNERS = 32
# Protocol addresses only: declaring a role does not declare anatomy or properties.
CORE_ROLES = frozenset({'main_subject', 'secondary_subject', 'scene', 'image',
    'recording_camera', 'primary_face', 'secondary_face', 'primary_hair', 'secondary_hair',
    'primary_hands', 'secondary_hands', 'primary_garment', 'secondary_garment',
    'primary_prop', 'secondary_prop', 'foreground_surface', 'background_surface',
    'light_source', 'light_receiver', 'relationship_target'})
ROW_FIELDS = frozenset({'assertion_id', 'dimension', 'polarity', 'source_span_ids',
                        'axes', 'evidence', 'affected_dimensions'})
KINDS = {
    'owner': {'owner', 'owner_kind'},
    'role': {'role', 'owner'},
    'fact': {'owner', 'property', 'value_type', 'value'},
    'equivalent': {'left', 'right'},
    'part_of': {'left', 'right'},
    'disjoint': {'left', 'right'},
}


def concrete(value):
    return (isinstance(value, str) and bool(value.strip())
            and '*' not in value and not value.endswith('.'))


def typed_value(value):
    if not isinstance(value, dict) or set(value) != {'type', 'value'} or not concrete(value['type']):
        return False
    item = value['value']
    return (concrete(item) or isinstance(item, list) and 1 <= len(item) <= 8
            and all(concrete(row) for row in item) and len(set(item)) == len(item))


def value_key(value):
    item = value['value']
    return value['type'], tuple(item) if isinstance(item, list) else item


def read(assertions, spans, baseline, *, intent_lock=None):
    """Validate the bounded native namespace inside normalized assertions.

    The calling core validator binds these spans to the exact user envelope.
    Every native row is also required and backed by frozen baseline evidence.
    """
    if not isinstance(assertions, list) or not isinstance(spans, list) or not isinstance(baseline, str):
        raise ValueError('frozen semantic witnesses require normalized core inputs')
    native = [row for row in assertions if isinstance(row, dict)
              and isinstance(row.get('axes'), dict) and 'native_schema' in row['axes']]
    if len(native) > MAX_ROWS:
        raise ValueError('too many frozen semantic witness rows')
    active = {row.get('source_span_id', row.get('span_id')) for row in spans
              if isinstance(row, dict) and concrete(row.get('source_span_id', row.get('span_id')))
              and isinstance(row.get('text'), str) and row['text'].strip()}
    graph = {'schema': SCHEMA, 'owners': {}, 'roles': {}, 'equivalent': [], 'part_of': [], 'disjoint': []}
    facts, fact_ids, row_ids = [], set(), set()
    for row in native:
        axes = row['axes']; kind = axes.get('kind')
        if (set(row) != ROW_FIELDS or axes.get('native_schema') != SCHEMA or not isinstance(kind,str) or kind not in KINDS
                or set(axes) != {'native_schema', 'kind'} | KINDS[kind]
                or not concrete(row['assertion_id']) or row['assertion_id'] in row_ids
                or row.get('polarity') != 'required'
                or not isinstance(row.get('affected_dimensions'), list)
                or row['dimension'] not in row['affected_dimensions']
                or not isinstance(row.get('source_span_ids'), list) or not row['source_span_ids']
                or any(not concrete(value) for value in row['source_span_ids'])
                or len(set(row['source_span_ids'])) != len(row['source_span_ids'])
                or not set(row['source_span_ids']) <= active
                or not isinstance(row.get('evidence'), dict) or not row['evidence']
                or any(not isinstance(value, str) or not value.strip() or value not in baseline
                       for value in row['evidence'].values())):
            raise ValueError('invalid or ungrounded frozen semantic witness')
        row_ids.add(row['assertion_id'])
        if kind != 'fact' and (row['dimension'] != 'subject' or row['affected_dimensions'] != ['subject']):
            raise ValueError('owner statements require frozen subject grounding')
        if kind == 'owner':
            if (not concrete(axes['owner']) or not concrete(axes['owner_kind'])
                    or axes['owner'] in graph['owners']):
                raise ValueError('duplicate or untyped frozen owner')
            graph['owners'][axes['owner']] = axes['owner_kind']
        elif kind == 'role':
            if axes['role'] not in CORE_ROLES or not concrete(axes['owner']) or axes['role'] in graph['roles']:
                raise ValueError('duplicate or unknown canonical core role')
            graph['roles'][axes['role']] = axes['owner']
        elif kind == 'fact':
            value = {'type': axes['value_type'], 'value': axes['value']}
            if not concrete(axes['owner']) or not concrete(axes['property']) or not typed_value(value):
                raise ValueError('invalid frozen typed fact')
            key = (row['dimension'], axes['owner'], axes['property'])
            if key in fact_ids:
                raise ValueError('duplicate or contradictory frozen fact')
            fact_ids.add(key)
            facts.append({'assertion_id': row['assertion_id'], 'dimension': row['dimension'],
                          'target': axes['owner'], 'property': axes['property'], 'value': copy.deepcopy(value)})
        else:
            if not concrete(axes['left']) or not concrete(axes['right']) or axes['left'] == axes['right']:
                raise ValueError('owner relation requires two explicit owners')
            pair = [axes['left'], axes['right']]
            if kind != 'part_of':
                pair.sort()
            if pair in graph[kind]:
                raise ValueError('duplicate owner relation')
            graph[kind].append(pair)
    if len(graph['owners']) > MAX_OWNERS:
        raise ValueError('too many frozen owners')
    for row in facts:
        if row['target'] not in graph['owners']:
            raise ValueError('frozen fact refers to an undeclared owner')
    canonical, _ = validate_graph(graph)
    known = set()
    for row in facts:
        key = (row['dimension'], canonical[row['target']], row['property'])
        if key in known:
            raise ValueError('aliased owners carry duplicate or contradictory facts')
        known.add(key)
    result={'schema': SCHEMA, 'graph': graph, 'facts': facts}
    if intent_lock is not None:validate_lock_support(assertions,result,intent_lock)
    return result


def normalize_check(raw, normalized, spans, baseline, intent_lock=None):
    """Do not accept dict/bool/number coercion or whitespace loss in native axes."""
    for before, after in zip(raw, normalized):
        axes = before.get('axes') if isinstance(before, dict) else None
        if isinstance(axes, dict) and 'native_schema' in axes and axes != after['axes']:
            raise ValueError('native semantic axes must survive normalization exactly')
    read(normalized, spans, baseline, intent_lock=intent_lock)


def validate_graph(graph):
    if (not isinstance(graph, dict) or set(graph) != {'schema', 'owners', 'roles', 'equivalent', 'part_of', 'disjoint'}
            or graph['schema'] != SCHEMA or not isinstance(graph['owners'], dict)
            or len(graph['owners']) > MAX_OWNERS
            or any(not concrete(key) or not concrete(value) for key, value in graph['owners'].items())):
        raise ValueError('explicit owner graph required')
    if (not isinstance(graph['roles'], dict) or not set(graph['roles']) <= CORE_ROLES
            or any(not isinstance(owner, str) or owner not in graph['owners'] for owner in graph['roles'].values())
            or any(role in graph['owners'] and role != owner for role, owner in graph['roles'].items())):
        raise ValueError('canonical role needs an unambiguous declared actual owner')
    parent = {key: key for key in graph['owners']}
    def root(node):
        while parent[node] != node:
            node = parent[node]
        return node
    for kind in ('equivalent', 'part_of', 'disjoint'):
        rows = graph[kind]
        if not isinstance(rows, list) or len(rows) > MAX_ROWS:
            raise ValueError('unbounded owner relation list')
        seen = set()
        for pair in rows:
            if (not isinstance(pair, list) or len(pair) != 2
                    or any(not isinstance(node, str) or node not in parent for node in pair)
                    or pair[0] == pair[1] or tuple(pair) in seen):
                raise ValueError('invalid or dangling owner relation')
            seen.add(tuple(pair))
            if kind == 'equivalent':
                parent[root(pair[0])] = root(pair[1])
    canonical = {node: root(node) for node in parent}
    for node, alias in canonical.items():
        if graph['owners'][node] != graph['owners'][alias]:
            raise ValueError('equivalent owners have contradictory explicit kinds')
    ancestors = {node: set() for node in set(canonical.values())}
    for child, owner in graph['part_of']:
        child, owner = canonical[child], canonical[owner]
        if child == owner:
            raise ValueError('an owner cannot contain itself through an alias')
        ancestors[child].add(owner)
    changed = True
    while changed:
        changed = False
        for node, known in ancestors.items():
            larger = known | set().union(*(ancestors[value] for value in known)) if known else known
            if node in larger:
                raise ValueError('cyclic owner hierarchy')
            if larger != known:
                ancestors[node] = larger; changed = True
    for left, right in graph['disjoint']:
        left, right = canonical[left], canonical[right]
        if (left == right or left in ancestors[right] or right in ancestors[left]
                or any(left in scope and right in scope for scope in ancestors.values())):
            raise ValueError('owner equivalence/hierarchy contradicts disjointness')
    return canonical, ancestors


def owner_relation(graph, left, right):
    if left == right:
        return 'overlap'
    if graph is None:
        return 'unknown'
    canonical, ancestors = validate_graph(graph)
    left, right = graph['roles'].get(left, left), graph['roles'].get(right, right)
    if left not in canonical or right not in canonical:
        return 'unknown'
    left, right = canonical[left], canonical[right]
    if left == right or left in ancestors[right] or right in ancestors[left]:
        return 'overlap'
    left_scope, right_scope = ancestors[left] | {left}, ancestors[right] | {right}
    for first, second in graph['disjoint']:
        first, second = canonical[first], canonical[second]
        if first in left_scope and second in right_scope or second in left_scope and first in right_scope:
            return 'disjoint'
    return 'unknown'


def is_native_fact(row):
    axes=row.get('axes') if isinstance(row,dict) else None
    return (isinstance(axes,dict) and axes.get('native_schema')==SCHEMA and axes.get('kind')=='fact')


def validate_lock_support(assertions, frozen, intent_lock):
    """A partial requester property lock can freeze exactly that fact's scope.

    This grants no mutation permission and never changes open/locked dimensions.
    Owned parts are not identity aliases and cannot broaden a narrow anchor.
    """
    locked=set(intent_lock.get('locked_dimensions') or [])
    graph=frozen['graph'];canonical,_=validate_graph(graph)
    def identity(value):
        value=graph['roles'].get(value,value)
        return canonical.get(value)
    for row in assertions:
        axes=row.get('axes') if isinstance(row,dict) else None
        if not isinstance(axes,dict) or 'native_schema' not in axes:
            continue
        if set(row['affected_dimensions'])<=locked:
            continue
        if not is_native_fact(row) or row['affected_dimensions'] != [row['dimension']]:
            raise ValueError('native owner/role/relations require whole subject locking')
        owner=identity(axes['owner']);prop=axes['property']
        supported=any(isinstance(anchor,dict) and anchor.get('dimension')==row['dimension']
            and concrete(anchor.get('property')) and '*' not in anchor['property']
            and owner is not None and identity(anchor.get('target'))==owner
            and (prop==anchor['property'] or prop.startswith(anchor['property']+'.'))
            for anchor in intent_lock.get('semantic_anchors') or [])
        if not supported:
            raise ValueError('native frozen fact needs its whole dimension or exact owner/property anchor')
