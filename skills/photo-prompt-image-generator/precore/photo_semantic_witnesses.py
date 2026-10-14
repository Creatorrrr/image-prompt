"""Candidate-free, source-grounded frozen facts and explicit owner relationships.

No source catalog, classifier, retrieval, model, or filesystem dependency. Values
are exact typed strings/string lists, never guessed semantic entailments.
"""
from __future__ import annotations
import copy
import hashlib
import json
import re

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
    'scope_inventory': {'owner', 'scope_kind', 'inventory'},
    'existing_member_scope': {'scope_id', 'inventory'},
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


def read(assertions, spans, baseline, *, intent_lock=None, request_binding=None):
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
    facts, fact_ids, row_ids, scopes, member_scopes = [], set(), set(), [], []
    for row in native:
        axes = row['axes']; kind = axes.get('kind')
        if (set(row) != ROW_FIELDS or axes.get('native_schema') != SCHEMA or not isinstance(kind,str) or kind not in KINDS
                or set(axes) not in [({'native_schema', 'kind'} | KINDS[kind]),
                    *([{'native_schema', 'kind'} | KINDS[kind] | {'scope_kinds','source_input_ids'}] if kind=='fact' else [])]
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
        elif kind == 'scope_inventory':
            if not concrete(axes['owner']) or axes['scope_kind'] not in SCOPE_KINDS:
                raise ValueError('invalid explicit scope inventory owner/kind')
            scopes.append({'assertion_id':row['assertion_id'],'owner':axes['owner'],
                           'scope_kind':axes['scope_kind'],'inventory':decode_inventory(axes['inventory'])})
        elif kind == 'existing_member_scope':
            if not concrete(axes['scope_id']):
                raise ValueError('existing member scope needs an explicit inventory address')
            text = axes['inventory']
            if not isinstance(text, str) or len(text.encode('utf-8')) > MAX_MEMBER_INVENTORY_BYTES:
                raise ValueError('existing member inventory exceeds its exact UTF-8 byte bound')
            member_scopes.append({'assertion_id':row['assertion_id'], 'scope_id':axes['scope_id'],
                'source_span_ids':copy.deepcopy(row['source_span_ids']), 'inventory':decode_inventory(text)})
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
            if 'scope_kinds' in axes:
                facts[-1].update(scope_kinds=copy.deepcopy(axes['scope_kinds']),
                                 source_input_ids=copy.deepcopy(axes['source_input_ids']))
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
    validate_scope_inventories(scopes,facts,graph,request_binding)
    result={'schema': SCHEMA, 'graph': graph, 'facts': facts, 'scope_inventories':scopes}
    if member_scopes:
        if len(assertions) > MAX_ROWS:
            raise ValueError('member scopes retain the total frozen assertion row bound')
        validate_existing_member_scopes(member_scopes, facts, graph, spans, request_binding)
        # Absence preserves the original no-member-scope result bytes exactly.
        result['member_scopes'] = member_scopes
    if intent_lock is not None:validate_lock_support(assertions,result,intent_lock)
    return result


def normalize_check(raw, normalized, spans, baseline, intent_lock=None, request_binding=None):
    """Do not accept dict/bool/number coercion or whitespace loss in native axes."""
    for before, after in zip(raw, normalized):
        axes = before.get('axes') if isinstance(before, dict) else None
        if isinstance(axes, dict) and 'native_schema' in axes and axes != after['axes']:
            raise ValueError('native semantic axes must survive normalization exactly')
    read(normalized, spans, baseline, intent_lock=intent_lock, request_binding=request_binding)


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


SCOPE_KINDS = frozenset({'reference_appearance','requester_identity'})
INPUT_SCHEMA = 'photo-request-input-inventory/v1'
SCOPE_SCHEMA = 'photo-frozen-scope-inventory/v1'
MAX_INPUTS = 32


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def validate_input_inventory(value, request_sha256):
    if (not isinstance(value,dict) or set(value)!={'schema','complete','items'}
            or value['schema']!=INPUT_SCHEMA or type(value['complete']) is not bool
            or not isinstance(value['items'],list) or len(value['items'])>MAX_INPUTS):
        raise ValueError('explicit bounded request input inventory required')
    ids=set()
    for item in value['items']:
        if (not isinstance(item,dict) or set(item)!={'id','kind','sha256'}
                or not concrete(item['id']) or item['id'] in ids
                or item['kind'] not in {'request_text','text','reference_image','identity_reference','other'}
                or not isinstance(item['sha256'],str) or re.fullmatch(r'[0-9a-f]{64}',item['sha256']) is None
                or item['kind']=='request_text' and item['sha256']!=request_sha256):
            raise ValueError('invalid, duplicate or stale request input entry')
        ids.add(item['id'])
    if value["complete"] and sum(item["kind"]=="request_text" for item in value["items"])!=1:
        raise ValueError("complete input inventory must include the exact request text once")
    return copy.deepcopy(value)


def input_binding(envelope):
    result={'request_sha256':envelope.get('request_sha256'),
            'request_envelope_sha256':envelope.get('request_envelope_sha256',envelope.get('canonical_sha256'))}
    if 'input_inventory' in envelope:
        inventory=validate_input_inventory(envelope['input_inventory'],result['request_sha256'])
        result['input_inventory_sha256']=digest(inventory)
    return result


def decode_inventory(text):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('duplicate scope inventory key')
            result[key]=value
        return result
    if not isinstance(text,str) or len(text)>65536:
        raise ValueError('scope inventory must be bounded exact canonical JSON text')
    value=json.loads(text,object_pairs_hook=unique,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('invalid number')))
    if canonical(value)!=text:
        raise ValueError('scope inventory canonical JSON must survive wire exactly')
    return value


def is_scope_inventory(row):
    axes=row.get('axes') if isinstance(row,dict) else None
    return isinstance(axes,dict) and axes.get('native_schema')==SCHEMA and axes.get('kind')=='scope_inventory'


def is_existing_member_scope(row):
    axes = row.get('axes') if isinstance(row, dict) else None
    return (isinstance(axes, dict) and axes.get('native_schema') == SCHEMA
            and axes.get('kind') == 'existing_member_scope')


MEMBER_SCOPE_SCHEMA = 'photo-frozen-existing-member-scope/v1'
MAX_MEMBER_SCOPES = 8
MAX_MEMBERS = 32
MAX_MEMBER_INVENTORY_BYTES = 65536


def validate_existing_member_scopes(scopes, facts, graph, spans, request_binding):
    """Freeze an explicitly closed local inventory, never a synthetic entity.

    Membership/completeness are authored before discovery, not independently
    observed by this function. No kinds, anatomy, counts, descendants or scope
    applicability are inferred. Runtime set resolution is a separate contract.
    """
    if len(scopes) > MAX_MEMBER_SCOPES:
        raise ValueError('too many existing member scopes')
    if not isinstance(request_binding, dict) or 'input_inventory' not in request_binding:
        raise ValueError('existing members require independently pinned complete request inputs')
    host = validate_input_inventory(request_binding['input_inventory'], request_binding.get('request_sha256'))
    bound = input_binding(request_binding)
    if (not host['complete'] or set(bound) != {'request_sha256', 'request_envelope_sha256', 'input_inventory_sha256'}
            or any(not isinstance(value, str) or re.fullmatch(r'[0-9a-f]{64}', value) is None
                   for value in bound.values())):
        raise ValueError('existing members require complete exact request/envelope/input binding')
    input_ids = [item['id'] for item in host['items']]
    request_id = next(item['id'] for item in host['items'] if item['kind'] == 'request_text')
    active = {row.get('source_span_id', row.get('span_id')) for row in spans
              if isinstance(row, dict) and concrete(row.get('source_span_id', row.get('span_id')))}
    canonical_owners, _ = validate_graph(graph)
    presence = {canonical_owners[fact['target']] for fact in facts
                if fact['dimension'] == 'subject' and fact['property'] == 'entity.presence'
                and fact['value'] == {'type':'entity.presence/v1', 'value':'present'}}
    seen = set()
    for scope in scopes:
        sid, inv = scope['scope_id'], scope['inventory']
        if sid in seen or sid in graph['owners'] or sid in graph['roles']:
            raise ValueError('duplicate member scope or scope address used as an owner/role')
        seen.add(sid)
        if (not isinstance(inv, dict)
                or set(inv) != {'schema', 'complete', 'state', 'input_binding', 'reviewed_input_ids', 'members'}
                or inv['schema'] != MEMBER_SCOPE_SCHEMA or inv['complete'] is not True
                or inv['state'] != 'known_present' or inv['input_binding'] != bound
                or inv['reviewed_input_ids'] != input_ids
                or not isinstance(inv['members'], list) or not 1 <= len(inv['members']) <= MAX_MEMBERS):
            raise ValueError('existing member scope must be complete, present, nonempty and input-bound')
        members = set()
        for member in inv['members']:
            if (not isinstance(member, dict) or set(member) != {'owner_id', 'source_span_ids', 'source_input_ids'}
                    or not concrete(member['owner_id']) or member['owner_id'] not in canonical_owners):
                raise ValueError('existing scope members must be flat declared actual owners')
            owner = canonical_owners[member['owner_id']]
            if owner in members:
                raise ValueError('duplicate canonical member; aliases are not additional members')
            members.add(owner)
            if owner not in presence:
                raise ValueError('each existing member needs an independent exact atomic presence fact')
            span_ids, ids = member['source_span_ids'], member['source_input_ids']
            if (not isinstance(span_ids, list) or not span_ids or any(not concrete(x) for x in span_ids)
                    or len(span_ids) != len(set(span_ids)) or not set(span_ids) <= active
                    or not set(span_ids) <= set(scope['source_span_ids'])
                    or not isinstance(ids, list) or not 1 <= len(ids) <= MAX_INPUTS
                    or any(not concrete(x) for x in ids) or len(ids) != len(set(ids))
                    or not set(ids) <= set(input_ids) or request_id not in ids):
                raise ValueError('each member needs exact active membership spans and pinned input provenance')
    for fact in facts:
        value = fact['value']
        if value['type'] == 'entity.owner_id/v1':
            values = value['value'] if isinstance(value['value'], list) else [value['value']]
            if any(item in seen for item in values):
                raise ValueError('a member scope address cannot be an entity relation endpoint')


def validate_scope_inventories(scopes, facts, graph, request_binding):
    scoped=[fact for fact in facts if 'scope_kinds' in fact]
    if not scopes and not scoped:return
    if not isinstance(request_binding,dict) or 'input_inventory' not in request_binding:
        raise ValueError('scope evidence requires independently pinned request input inventory')
    host=validate_input_inventory(request_binding['input_inventory'],request_binding.get('request_sha256'))
    bound=input_binding(request_binding)
    if set(bound)!={'request_sha256','request_envelope_sha256','input_inventory_sha256'} or any(
            not isinstance(value,str) or re.fullmatch(r'[0-9a-f]{64}',value) is None for value in bound.values()):
        raise ValueError('scope evidence needs exact request/envelope/input inventory SHA')
    input_ids=[item['id'] for item in host['items']]
    canonical_owners,ancestors=validate_graph(graph)
    for fact in scoped:
        kinds,ids=fact['scope_kinds'],fact['source_input_ids']
        if (not isinstance(kinds,list) or not kinds or len(kinds)!=len(set(kinds)) or not set(kinds)<=SCOPE_KINDS
                or not isinstance(ids,list) or not 1<=len(ids)<=8 or any(not concrete(x) for x in ids)
                or len(ids)!=len(set(ids)) or not set(ids)<=set(input_ids)):
            raise ValueError('scoped frozen fact requires explicit exact input provenance')
    seen=set()
    by_id={fact['assertion_id']:fact for fact in facts}
    for scope in scopes:
        owner=canonical_owners.get(scope['owner'])
        key=(owner,scope['scope_kind'])
        if owner is None or key in seen:raise ValueError('duplicate/undeclared scope inventory owner')
        seen.add(key);inv=scope['inventory']
        if (not isinstance(inv,dict) or set(inv)!={'schema','complete','input_binding','reviewed_input_ids','state','items'}
                or inv['schema']!=SCOPE_SCHEMA or type(inv['complete']) is not bool
                or inv['input_binding']!=bound or inv['reviewed_input_ids']!=input_ids
                or inv['state'] not in {'known_absent','known_present','unknown'}
                or not isinstance(inv['items'],list) or len(inv['items'])>MAX_ROWS):
            raise ValueError('stale, incomplete or invalid scope inventory binding')
        expected={fact['assertion_id'] for fact in scoped if scope['scope_kind'] in fact['scope_kinds']
            and (canonical_owners[fact['target']]==owner or owner in ancestors[canonical_owners[fact['target']]])}
        present=set()
        for item in inv['items']:
            if not isinstance(item,dict) or set(item)!={'assertion_id','dimension','target','property','value'}:
                raise ValueError('scope item must repeat the exact independently frozen fact')
            aid=item['assertion_id'];fact=by_id.get(aid)
            if (aid in present or aid not in expected or fact is None
                    or item!={name:fact[name] for name in item}):
                raise ValueError('scope item owner/value/input provenance differs from its frozen fact')
            present.add(aid)
        if inv['state']=='known_absent' and (present or expected):
            raise ValueError('known absence contradicts established scoped facts')
        if inv['state']=='known_present' and not present:
            raise ValueError('present scope must list established protected items')
        if inv['complete'] and host['complete'] and inv['state']=='known_present' and present!=expected:
            raise ValueError('complete present inventory omits scoped frozen facts')
