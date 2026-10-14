"""Pure actual-owner expansion of an explicitly selected, source-checked projection.

B2 must construct this input from qualified source/actual RID and sealed condition
frames. Digests here bind transport; a self-hashed projection is not source truth.
This module parses no source proof, role evidence, guard, catalog or discovery
text, and grants no admission or mutation permission. Functions do no I/O.
"""
from __future__ import annotations
import copy
import re
from photo_precore_bridge import load

witnesses = load('photo_semantic_witnesses')
SCHEMA = 'photo-native-selected-resolution-input/v1'
VIEW_SCHEMA = 'photo-native-resolved-owner-view/v1'
FIXED_CONTEXT = 'fixed_point_witness_context'
EXACT_CONTEXT = 'exact_core_bound_context'
MAX_FACTS = 4096
MAX_BINDINGS = 32
MAX_SELECTED_NODES = 64
MAX_DEPTH = 8
MAX_EDGES = 8
MODES = frozenset({'effect', 'prerequisite', 'preservation', 'context'})
OPERATIONS = frozenset({'set_value', 'add_entity', 'remove_entity', 'relocate', 'select_plane'})
NODE_FIELDS = frozenset({'candidate_id', 'realization_id', 'meaning_sha256', 'qualification_sha256',
    'projection_sha256', 'bindings', 'guard_only_targets', 'facts', 'selected_children'})
FACT_FIELDS = frozenset({'id', 'realization_id', 'mode', 'dimension', 'target', 'property', 'value', 'requires'})
EDGE_FIELDS = frozenset({'candidate_id', 'realization_id', 'meaning_sha256', 'qualification_sha256',
                         'projection_sha256', 'selection'})


def digest(value):
    return witnesses.digest(value)


def node_digest(node):
    """Exact private node projection digest, distinct from qualification digest."""
    return digest({key:value for key,value in node.items() if key != 'projection_sha256'})


def _shape(value, fields, message):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(message)


def _sha(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _names(value, limit, message, *, empty=True):
    if (not isinstance(value, list) or len(value) > limit or not empty and not value
            or any(not witnesses.concrete(x) for x in value) or len(value) != len(set(value))):
        raise ValueError(message)
    return value


def _identity(value):
    return value['candidate_id'], value['realization_id']


def _signature(value):
    return tuple(value[key] for key in ('realization_id', 'meaning_sha256', 'qualification_sha256', 'projection_sha256'))


def _facts(node):
    facts = node['facts']
    if not isinstance(facts, list) or len(facts) > MAX_FACTS:
        raise ValueError('bounded selected fact inventory required')
    by_id, assignments = {}, {}
    for fact in facts:
        mode = fact.get('mode') if isinstance(fact, dict) else None
        if not isinstance(mode, str) or mode not in MODES:
            raise ValueError('explicit fact mode required')
        _shape(fact, FACT_FIELDS | ({'operation', 'receivers'} if mode == 'effect' else set()),
               'exact normalized fact fields required')
        if (any(not witnesses.concrete(fact[key]) for key in ('id', 'realization_id', 'dimension', 'target', 'property'))
                or fact['realization_id'] != node['realization_id'] or fact['id'] in by_id
                or not witnesses.typed_value(fact['value'])):
            raise ValueError('duplicate, foreign or untyped selected fact')
        _names(fact['requires'], MAX_FACTS, 'exact unique same-node prerequisite IDs required')
        if fact['value']['type'] == 'frozen_property_reference/v1' and (
                mode != 'preservation' or fact['value']['value'] != 'same'):
            raise ValueError('frozen value reference is preservation only')
        if mode == 'effect':
            if not isinstance(fact['operation'], str) or fact['operation'] not in OPERATIONS:
                raise ValueError('explicit actual operation required')
            _names(fact['receivers'], MAX_BINDINGS, 'bounded exact source receiver targets required')
            key = fact['dimension'], fact['target'], fact['property']
            signature = (witnesses.canonical(fact['value']), fact['operation'], frozenset(fact['receivers']))
            if key in assignments and assignments[key] != signature:
                raise ValueError('conflicting source-local effect assignments')
            assignments[key] = signature
        by_id[fact['id']] = fact
    for fact in facts:
        if any(ref not in by_id or ref == fact['id'] or by_id[ref]['mode'] not in
               {'prerequisite', 'preservation'} for ref in fact['requires']):
            raise ValueError('foreign or non-frozen selected prerequisite')
    # An iterative walk also bounds malformed long chains without Python recursion.
    done = set()
    for fid in by_id:
        stack = [(fid, False)]; active = set()
        while stack:
            current, leaving = stack.pop()
            if leaving:
                active.remove(current); done.add(current); continue
            if current in done:
                continue
            if current in active:
                raise ValueError('cyclic selected prerequisite facts')
            active.add(current); stack.append((current, True))
            stack.extend((ref, False) for ref in reversed(by_id[current]['requires']))
    return facts


def _nodes(projection):
    if not isinstance(projection['nodes'], list) or not isinstance(projection['roots'], list) or not projection['roots']:
        raise ValueError('explicit nonempty root and complete selected node inventories required')
    nodes = {}
    for node in projection['nodes']:
        _shape(node, NODE_FIELDS, 'exact normalized selected node required')
        if (any(not witnesses.concrete(node[key]) for key in ('candidate_id', 'realization_id'))
                or any(not _sha(node[key]) for key in ('meaning_sha256', 'qualification_sha256', 'projection_sha256'))
                or node['candidate_id'] in nodes or node['projection_sha256'] != node_digest(node)
                or not isinstance(node['bindings'], list) or len(node['bindings']) > MAX_BINDINGS
                or not isinstance(node['selected_children'], list) or len(node['selected_children']) > MAX_EDGES):
            raise ValueError('duplicate, stale or unbounded selected source node')
        _names(node['guard_only_targets'], MAX_BINDINGS, 'exact unique own-sealed guard-only targets required')
        _facts(node)
        nodes[node['candidate_id']] = node
    roots, seen_roots = [], set()
    for root in projection['roots']:
        _shape(root, {'candidate_id', 'realization_id'}, 'exact selected root identity required')
        if any(not witnesses.concrete(root[key]) for key in root) or root['candidate_id'] in seen_roots:
            raise ValueError('duplicate or invalid selected root')
        seen_roots.add(root['candidate_id']); roots.append(root['candidate_id'])
        if root['candidate_id'] not in nodes or _identity(root) != _identity(nodes[root['candidate_id']]):
            raise ValueError('selected root is missing its exact source/RID node')
    incoming = {cid:[] for cid in nodes}
    for cid, node in nodes.items():
        children = set()
        for edge in node['selected_children']:
            _shape(edge, EDGE_FIELDS, 'exact selected dependency edge required')
            child = edge['candidate_id']
            if (not witnesses.concrete(child) or child in children or child not in nodes
                    or not isinstance(edge['selection'], str) or edge['selection'] not in {'required', 'explicit_optional'}
                    or _signature(edge) != _signature(nodes[child])):
                raise ValueError('duplicate, missing or conflicting actual selected child')
            children.add(child)
            incoming[child].append({'candidate_id':cid, 'realization_id':node['realization_id'],
                                    'selection':edge['selection']})
    visited, active, heights, walk_order = set(), set(), {}, []
    def visit(cid, depth):
        if depth > MAX_DEPTH or cid in active:
            raise ValueError('cyclic or unbounded selected closure')
        if cid in heights:
            if depth + heights[cid] > MAX_DEPTH:
                raise ValueError('unbounded shared selected closure')
            return heights[cid]
        active.add(cid); visited.add(cid); walk_order.append(cid); height = 0
        for edge in nodes[cid]['selected_children']:
            height = max(height, 1 + visit(edge['candidate_id'], depth+1))
        active.remove(cid); heights[cid] = height
        return height
    for cid in roots:
        visit(cid, 0)
    if visited != set(nodes):
        raise ValueError('unused or foreign selected source nodes')
    return nodes, incoming, walk_order


def _context(core, projection, needs_exact, uses_scope):
    if not isinstance(core, dict) or core.get('contract_version') != 'photo-authorial-core/v3':
        raise ValueError('frozen core v3 witness context required')
    assertions = core.get('semantic_assertions')
    if not isinstance(assertions, list) or len(assertions) > witnesses.MAX_ROWS:
        raise ValueError('existing total core assertion bound retained')
    if not isinstance(core.get('request_binding'), dict) or not isinstance(core.get('intent_lock'), dict):
        raise ValueError('exact frozen witness and intent-lock objects required')
    kind = projection['context_kind']
    if kind == FIXED_CONTEXT:
        if needs_exact or 'canonical_sha256' in core or 'core_id' in core:
            raise ValueError('fixed-point hash-absent context cannot resolve selected owners or ignore a supplied hash')
    elif kind == EXACT_CONTEXT:
        actual = digest({key:value for key,value in core.items() if key not in {'canonical_sha256', 'core_id'}})
        if (not _sha(core.get('canonical_sha256')) or projection.get('core_sha256') != actual
                or core['canonical_sha256'] != actual
                or 'core_id' in core and core['core_id'] != actual[:16]):
            raise ValueError('exact frozen canonical core binding required')
    else:
        raise ValueError('explicit tagged frozen resolution context required')
    frozen = witnesses.read(assertions, (core.get('request_binding') or {}).get('active_spans') or [],
        core.get('baseline_prompt_en', ''), intent_lock=core.get('intent_lock') or {},
        request_binding=core.get('request_binding') or {})
    graph = frozen['graph']
    if not _sha(projection['owner_graph_sha256']) or projection['owner_graph_sha256'] != digest(graph):
        raise ValueError('frozen actual owner graph binding changed')
    canonical, _ = witnesses.validate_graph(graph)
    context = {'kind':kind, 'owner_graph_sha256':digest(graph), 'frozen_witnesses_sha256':digest(frozen)}
    if kind == EXACT_CONTEXT:
        context['core_sha256'] = core['canonical_sha256']
    scopes = frozen.get('member_scopes', [])
    if uses_scope or 'member_scopes_sha256' in projection:
        if (kind != EXACT_CONTEXT or not _sha(projection.get('member_scopes_sha256'))
                or projection['member_scopes_sha256'] != digest(scopes)):
            raise ValueError('exact independently frozen member scope table binding required')
        context.update(member_scopes_sha256=digest(scopes), input_binding=witnesses.input_binding(core.get('request_binding') or {}))
    return frozen, canonical, context


def _binding_kinds(nodes):
    kinds = []; selected_nodes = 0
    for node in nodes.values():
        selected = False
        for binding in node['bindings']:
            _shape(binding, {'target', 'origin', 'selection'}, 'exact normalized source binding required')
            selection = binding['selection']
            if not isinstance(selection, dict) or not isinstance(selection.get('kind'), str):
                raise ValueError('explicit tagged point or scope selection required')
            kind = selection['kind']; kinds.append(kind)
            selected |= kind in {'selected_existing_owner', 'existing_member_scope'}
        if selected:
            selected_nodes += 1
    if selected_nodes > MAX_SELECTED_NODES:
        raise ValueError('too many caller-selected owner binding nodes')
    return kinds


def _resolve_node(node, frozen, canonical, scopes):
    graph = frozen['graph']; facts = node['facts']; resolved = {}; bindings = []
    present = {canonical[fact['target']]:fact['assertion_id'] for fact in frozen['facts']
        if fact['dimension'] == 'subject' and fact['property'] == 'entity.presence'
        and fact['value'] == {'type':'entity.presence/v1', 'value':'present'}}
    used = {fact['target'] for fact in facts}
    used.update(target for fact in facts if fact['mode']=='effect' for target in fact['receivers'])
    guard_only = set(node['guard_only_targets'])
    if guard_only & used:
        raise ValueError('guard-only targets must be the exact additional own-sealed addresses')
    for binding in node['bindings']:
        target, origin, selection = binding['target'], binding['origin'], binding['selection']
        if not witnesses.concrete(target) or target in resolved or not isinstance(origin, str) or origin not in {'existing', 'introduced'}:
            raise ValueError('duplicate or invalid explicit source target')
        kind = selection['kind']; members = []
        def point(owner, presence=False):
            if owner not in canonical:
                raise ValueError('existing point is not declared in the frozen graph')
            result = {'owner_id':owner, 'canonical_owner_id':canonical[owner]}
            if presence:
                if canonical[owner] not in present:
                    raise ValueError('selected existing owner lacks independent atomic presence')
                result['presence_assertion_id'] = present[canonical[owner]]
            return result
        if kind == 'fixed_role':
            _shape(selection, {'kind','role'}, 'exact fixed role selector required')
            role = selection['role']
            if origin!='existing' or not isinstance(role, str) or role not in witnesses.CORE_ROLES or role not in graph['roles']:
                raise ValueError('fixed role needs its explicitly declared existing owner')
            members = [point(graph['roles'][role])]
        elif kind == 'selected_existing_owner':
            _shape(selection, {'kind','owner_id'}, 'exact selected actual point required')
            if origin!='existing' or not witnesses.concrete(selection['owner_id']):
                raise ValueError('caller-selected point is existing only')
            members = [point(selection['owner_id'], True)]
        elif kind == 'existing_member_scope':
            _shape(selection, {'kind','scope_id','scope_sha256','target_semantics','receiver_semantics'},
                   'exact each-member/all-receiver scope selector required')
            sid = selection['scope_id']
            if (origin!='existing' or not witnesses.concrete(sid) or sid not in scopes
                    or not _sha(selection['scope_sha256']) or selection['scope_sha256']!=digest(scopes[sid])
                    or selection['target_semantics']!='each_member' or selection['receiver_semantics']!='all_members'):
                raise ValueError('exact existing scope address/hash and complete expansion semantics required')
            scope = scopes[sid]
            for index, member in enumerate(scope['inventory']['members']):
                item = point(member['owner_id'], True)
                item['scope_provenance'] = {'scope_id':sid, 'scope_sha256':selection['scope_sha256'],
                    'scope_assertion_id':scope['assertion_id'], 'member_index':index,
                    'source_span_ids':copy.deepcopy(member['source_span_ids']),
                    'source_input_ids':copy.deepcopy(member['source_input_ids'])}
                members.append(item)
        elif kind == 'introduced_point':
            _shape(selection, {'kind','role','introduced_by'}, 'exact introduced point creator required')
            role = selection['role']
            creators = [fact for fact in facts if fact['mode']=='effect' and fact['target']==target
                        and fact['operation']=='add_entity']
            if (origin!='introduced' or not isinstance(role,str) or role not in witnesses.CORE_ROLES
                    or role in graph['roles'] or len(creators)!=1 or not witnesses.concrete(selection['introduced_by'])
                    or creators[0]['id']!=selection['introduced_by']):
                raise ValueError('introduced point requires its exact creation and unoccupied role')
            owner = 'native-introduced:'+node['meaning_sha256']+':'+node['realization_id']+':'+target
            if owner in canonical:
                raise ValueError('introduced address is already an existing frozen owner')
            members = [{'owner_id':owner, 'canonical_owner_id':owner}]
        else:
            raise ValueError('unknown point/scope selection tag')
        row = {'target':target, 'origin':origin, 'selector_kind':kind,
               'selection':copy.deepcopy(selection), 'members':members}
        resolved[target] = row; bindings.append(row)
    if set(resolved) != used | guard_only:
        raise ValueError('source binding inventory is missing, unused or foreign')
    for target in guard_only:
        if resolved[target]['origin']!='existing':
            raise ValueError('frozen guard-only targets cannot be introduced')
    expanded = []
    for fact in facts:
        binding = resolved[fact['target']]
        if fact['mode'] in {'prerequisite','preservation'} and binding['origin']!='existing':
            raise ValueError('introduced point cannot self-witness a frozen obligation')
        if fact['mode']=='effect':
            if binding['selector_kind']=='selected_existing_owner' and fact['operation']=='add_entity':
                raise ValueError('selected existing owner cannot introduce an entity')
            if binding['selector_kind']=='existing_member_scope' and fact['operation'] in {'add_entity','remove_entity'}:
                raise ValueError('existing scope cannot introduce or remove members')
            receiver_rows = [{'source_target':target, 'selector_kind':resolved[target]['selector_kind'],
                              'members':copy.deepcopy(resolved[target]['members'])} for target in fact['receivers']]
        for index, member in enumerate(binding['members']):
            row = {'candidate_id':node['candidate_id'], 'realization_id':node['realization_id'],
                'fact_id':fact['id'], 'source_target':fact['target'], 'target':copy.deepcopy(member),
                'expansion_index':index, 'mode':fact['mode'], 'dimension':fact['dimension'],
                'property':fact['property'], 'value':copy.deepcopy(fact['value']), 'requires':copy.deepcopy(fact['requires'])}
            if fact['mode']=='effect':
                row.update(operation=fact['operation'], source_receivers=copy.deepcopy(fact['receivers']),
                           receiver_expansions=copy.deepcopy(receiver_rows),
                           canonical_receivers=sorted({item['canonical_owner_id'] for receiver in receiver_rows for item in receiver['members']}))
            expanded.append(row)
    return bindings, expanded


def resolve_selected_contracts(core, projection):
    """Resolve one explicit selected closure; never discover, qualify or approve it.

    Full/sealed compact inputs must be normalized by B2 to this same protocol.
    Every P/PR/context/E is address-expanded; B2 still matches frozen values and
    guards, applies all property/dimension locks, and audits immutable receipts.
    """
    base = {'schema','context_kind','owner_graph_sha256','roots','nodes'}
    if not isinstance(projection, dict) or projection.get('schema')!=SCHEMA:
        raise ValueError('versioned selected resolution projection required')
    expected = base if projection.get('context_kind')==FIXED_CONTEXT else base | {'core_sha256'}
    if 'member_scopes_sha256' in projection:
        expected = expected | {'member_scopes_sha256'}
    _shape(projection, expected, 'exact tagged context and selected projection fields required')
    if projection.get('context_kind')==FIXED_CONTEXT and 'member_scopes_sha256' in projection:
        raise ValueError('fixed point context cannot ignore supplied member scope pins')
    nodes, incoming, walk_order = _nodes(projection)
    kinds = _binding_kinds(nodes)
    uses_scope = 'existing_member_scope' in kinds
    frozen, canonical, context = _context(core, projection,
        uses_scope or 'selected_existing_owner' in kinds, uses_scope)
    scopes = {scope['scope_id']:scope for scope in frozen.get('member_scopes', [])}
    result_nodes, ledger, footprint = [], {}, set()
    for cid in sorted(nodes):
        node = nodes[cid]
        bindings, facts = _resolve_node(node, frozen, canonical, scopes)
        result_nodes.append({'candidate_id':cid, 'realization_id':node['realization_id'],
            'meaning_sha256':node['meaning_sha256'], 'qualification_sha256':node['qualification_sha256'],
            'projection_sha256':node['projection_sha256'], 'bindings':bindings, 'expanded_facts':facts,
            'selected_children':copy.deepcopy(node['selected_children']), 'incoming':copy.deepcopy(incoming[cid])})
        for fact in facts:
            if fact['mode']!='effect':
                continue
            owner = fact['target']['canonical_owner_id']
            key = fact['dimension'], owner, fact['property']
            signature = (witnesses.canonical(fact['value']), fact['operation'], tuple(fact['canonical_receivers']))
            if key in ledger and ledger[key]['signature']!=signature:
                raise ValueError('conflicting joint actual-owner effect assignment')
            if key not in ledger:
                ledger[key] = {'signature':signature, 'dimension':fact['dimension'], 'target':owner,
                    'property':fact['property'], 'value':copy.deepcopy(fact['value']), 'operation':fact['operation'],
                    'receivers':copy.deepcopy(fact['canonical_receivers']), 'sources':[]}
            ledger[key]['sources'].append({key:copy.deepcopy(fact[key]) for key in
                ('candidate_id','realization_id','fact_id','source_target','expansion_index','target')})
            footprint.update((fact['dimension'], target, fact['property']) for target in [owner,*fact['canonical_receivers']])
    assignments = [{key:value for key,value in ledger[item].items() if key!='signature'} for item in sorted(ledger)]
    properties = [dict(zip(('dimension','target','property'), key)) for key in sorted(footprint)]
    # Legacy scalar adapters preserve raw actual IDs and first-source order.
    # This projects the SAME expanded facts, never a second owner/scope lookup.
    by_id = {node['candidate_id']:node for node in result_nodes}
    literal = {}
    for cid in walk_order:
        for fact in by_id[cid]['expanded_facts']:
            if fact['mode']!='effect':
                continue
            owners = [fact['target']['owner_id'], *(item['owner_id']
                for receiver in fact['receiver_expansions'] for item in receiver['members'])]
            for owner in owners:
                key = fact['dimension'], owner, fact['property']
                literal.setdefault(key, dict(zip(('dimension','target','property'), key)))
    result = {'schema':VIEW_SCHEMA, 'context':context, 'projection_sha256':digest(projection),
        'roots':copy.deepcopy(projection['roots']), 'nodes':result_nodes, 'effect_assignments':assignments,
        'permission_scope':{'dimensions':sorted({row['dimension'] for row in assignments}), 'properties':properties,
                            'literal_properties':list(literal.values()),
                            'owner_graph':copy.deepcopy(frozen['graph'])}}
    result['expanded_facts_sha256'] = digest([node['expanded_facts'] for node in result_nodes])
    result['permission_scope_sha256'] = digest(result['permission_scope'])
    result['canonical_sha256'] = digest(result)
    return result
