"""Bounded additional permission comparison, called only by the native trusted coordinator.
Adapted from immutable reviewed permission-envelope-prototype-02.

Expected pins are independent trust roots supplied by the full-source/request
review caller. A caller replacing those trust roots cannot be detected here.
No resolver, I/O, source discovery, alias projection, E construction or guard waiver.
"""
from dataclasses import dataclass
import hashlib
import json

MAX_NODES, MAX_EFFECTS, MAX_OWNERS, MAX_ANCHORS, MAX_PAIRS = 8, 32, 64, 128, 4096


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def keys(value, names, label):
    require(isinstance(value, dict) and set(value) == set(names.split()), 'exact '+label+' fields required')


def text(v):
    return isinstance(v, str) and bool(v.strip())


def unique(values, limit, label, empty=False):
    require(isinstance(values, list) and (empty or values) and len(values) <= limit
            and all(text(v) for v in values) and len(set(values)) == len(values), 'bounded unique '+label+' required')


def at(value, pointer):
    require(isinstance(pointer, str) and pointer.startswith('/'), 'exact pointer required')
    for part in pointer[1:].split('/'):
        value = value[part.replace('~1', '/').replace('~0', '~')]
    return value


def footprint(f):
    return {k:f[k] for k in ('dimension', 'target', 'property', 'mode', 'operation', 'value', 'receivers', 'requires')}


@dataclass(frozen=True, slots=True)
class BoundSource:
    """Immutable structural bytes, NOT a qualified-source capability."""
    payload: bytes


@dataclass(frozen=True, slots=True)
class IndependentPins:
    """Externally retained expected values, never populated from a candidate receipt."""
    source_bindings: dict
    resolved_view_sha256: str
    inventory_sha256: str
    assessment_sha256: str


def _bind_source(context, contract):
    """Bind full supplied source structure; semantic/full-source truth remains external."""
    context, contract = json.loads(canonical(context)), json.loads(canonical(contract))
    keys(context, 'candidate_id realization_id source_snapshot_sha256 catalog_sha256 source_record actual_effect_set facts source_units positive_fields ownbindings closure_snapshot canonical_effect_refs required_preservation_refs', 'full source context')
    keys(contract, 'schema candidate_id realization_id basis', 'envelope contract')
    cid, rid = context['candidate_id'], context['realization_id']
    require(contract['schema'] == 'research-permission-envelope-contract/v1'
            and contract['candidate_id'] == cid and contract['realization_id'] == rid
            and context['source_record']['id'] == cid, 'exact CID/RID/source binding required')
    facts = {f['id']:f for f in context['facts']}
    require(len(facts) == len(context['facts']), 'unique source fact IDs required')
    unique(context['canonical_effect_refs'], MAX_EFFECTS, 'canonical E refs', empty=True)
    unique(context['required_preservation_refs'], MAX_EFFECTS, 'PR refs', empty=True)
    fields = {(v['realization_id'],v['pointer']):v['text'] for v in context['positive_fields']}
    units = {(v['realization_id'],v['pointer']):v for v in context['source_units'] if v['disposition'] in {'semantic','semantic_reference'}}
    for (r,p),v in fields.items():
        require(r == rid and at(context['source_record'], p) == v and '/tags' not in p and '/aliases' not in p,
                'exact actual positive field required')
    require(set(units)==set(fields), 'all supplied full positive fields need ordinary units')
    require(context['closure_snapshot'].get('guards')==context['source_record']['conditions'], 'whole intrinsic conditions/guards must be retained')
    for (r,p),u in units.items():
        require(fields.get((r,p)) == u['quote'], 'ordinary full positive unit required')
    effect_ids = context['canonical_effect_refs']
    effects = []
    for fid in effect_ids:
        f = facts[fid]
        require(f['mode'] == 'effect' and f['realization_id'] == rid, 'original E mode/RID required')
        effects.append(f)
    # Direct source declaration is preserved; no role/prefix-based effect inference.
    declared = {(v['dimension'],v['target'],v['property']) for v in context['actual_effect_set']['properties']}
    require(declared == {(f['dimension'],f['target'],f['property']) for f in effects}, 'complete original canonical E addresses required')
    require(set(context['actual_effect_set']['dimensions']) == {f['dimension'] for f in effects}, 'complete original dimensions required')
    for f in context['facts']:
        require(f['realization_id'] == rid and f['mode'] in {'effect','prerequisite','preservation','context'}, 'exact source fact mode/RID required')
        if f['mode'] == 'effect':
            require(any(footprint(f) == footprint(e) for e in effects), 'extra or changed canonical E forbidden')
        if f['mode'] == 'prerequisite':
            require(not any(all(f[k] == e[k] for k in ('target','property','value')) for e in effects), 'desired E cannot be pre-frozen as P')
        for ref in f['requires']:
            require(ref in facts and facts[ref]['mode'] in {'prerequisite','preservation'}, 'original same-RID obligations required')
    require(isinstance(contract['basis'], list) and len(contract['basis']) == len(effects), 'each E needs one ordinary source basis')
    require({b['fact_ref'] for b in contract['basis']} == set(effect_ids), 'exact E basis coverage required')
    for b in contract['basis']:
        keys(b, 'fact_ref unit_pointer rationale', 'source positive basis')
        f = facts[b['fact_ref']];u = units.get((rid,b['unit_pointer']))
        require(u is not None and u['disposition']=='semantic' and f['pointer'] == b['unit_pointer'] and f['quote'] in u['quote']
                and f['id'] in u['fact_refs'] and text(b['rationale']), 'ordinary direct positive E support required')
    for ref in context['required_preservation_refs']:
        require(ref in facts and facts[ref]['mode']=='preservation', 'actual source PR required')
    binding = {'schema':'research-full-source-envelope-binding/v1','candidate_id':cid,'realization_id':rid,
               'source_snapshot_sha256':context['source_snapshot_sha256'], 'catalog_sha256':context['catalog_sha256'],
               'full_context_sha256':digest(context),'source_record_sha256':digest(context['source_record']),
               'positive_units_sha256':digest(context['source_units']),'closure_sha256':digest(context['closure_snapshot']),
               'canonical_E_set_sha256':digest(effects),'contract_sha256':digest(contract)}
    return BoundSource(canonical({'context':context,'contract':contract,'binding':binding}))


def source_binding(bound):
    require(type(bound) is BoundSource, 'full structural source binding required')
    return json.loads(bound.payload)['binding']


def core_input_binding(core):
    rb=core['request_binding']
    require('input_inventory' in rb, 'complete independent input inventory required')
    return {'request_sha256':rb.get('request_sha256'),'request_envelope_sha256':rb.get('request_envelope_sha256',rb.get('canonical_sha256')),
            'input_inventory_sha256':digest(rb['input_inventory'])}


def anchors_from_core(core):
    """Exact lock inventory only; this is not semantic scope discovery."""
    lock = core['intent_lock'];result = []
    for a in lock.get('semantic_anchors', []):
        keys(a, 'dimension target property', 'protected anchor')
        result.append({'kind':'property',**a})
    for d in lock.get('locked_dimensions', []):
        result.append({'kind':'whole_dimension','dimension':d,'target':'*','property':None})
    require(len(result) <= MAX_ANCHORS and len({digest(a) for a in result}) == len(result), 'bounded unique actual anchors required')
    return sorted(result, key=digest)


def joint_properties_allowed(left, right, *, owner_graph, property_primitive):
    """Permission-only comparison of two unchanged expanded E owner unions.

    Reuse the independently pinned property primitive's exact/parent/child/
    wildcard and grounded owner-overlap protocol. These temporary comparison
    rows are neither source E facts nor assignments or receiver expansions.
    Distinct property spellings are not aliases; the manual joint review still
    independently decides semantic influence between unrelated property paths.
    """
    left_owners = sorted({left['target']['canonical_owner_id'], *left['canonical_receivers']})
    right_owners = sorted({right['target']['canonical_owner_id'], *right['canonical_receivers']})
    lock = {'contract_version':'photo-intent-lock/v2', 'semantic_anchors':[
        {'dimension':right['dimension'], 'target':owner, 'property':right['property']}
        for owner in right_owners]}
    comparison = [{'dimension':left['dimension'], 'target':owner, 'property':left['property']}
                  for owner in left_owners]
    return property_primitive(lock, [left['dimension']], comparison, owner_graph=owner_graph)


def _compare(bound_sources, *, core, resolved_view, inventory, assessment, expected, primitives):
    """Additional comparison only. Never returns native eligible/qualified status.

    primitives must be the independently pinned frozen property_effects_allowed
    and owner_relation callables. The helper never resolves owners a second time.
    """
    require(type(expected) is IndependentPins and expected.source_bindings, 'independent authority pins required')
    canonical([core,resolved_view,inventory,assessment])
    require(1 <= len(bound_sources) <= MAX_NODES, 'bounded selected source closure required')
    contexts = {}
    for bound in bound_sources:
        require(type(bound) is BoundSource, 'full source structure required')
        p = json.loads(bound.payload);b = p['binding'];cid=b['candidate_id']
        require(cid not in contexts and expected.source_bindings.get(cid) == b, 'independent full-source binding mismatch')
        # A freely constructed BoundSource is never trusted solely by its own hash.
        require(source_binding(bind_source(p['context'],p['contract'])) == b, 'source structure was altered')
        contexts[cid] = p['context']
    require(set(contexts) == set(expected.source_bindings), 'complete exact source authority inventory required')
    require(digest(resolved_view) == expected.resolved_view_sha256, 'same independently frozen B1 view required')
    require(resolved_view['canonical_sha256'] == digest({k:v for k,v in resolved_view.items() if k!='canonical_sha256'}), 'B1 view self-integrity mismatch')
    require(digest(inventory) == expected.inventory_sha256, 'independent pre-discovery inventory mismatch')
    require(digest(assessment) == expected.assessment_sha256, 'independent manual assessment mismatch')
    nodes=resolved_view['nodes'];require({n['candidate_id'] for n in nodes} == set(contexts), 'selected CID closure mismatch')
    graph=resolved_view['permission_scope']['owner_graph'];vc=resolved_view['context']
    require(core['canonical_sha256'] == vc['core_sha256'] and digest(graph) == vc['owner_graph_sha256'], 'exact core/topology binding required')
    # Native core canonical protocol is checked by B1; exact raw core input is also pinned here.
    keys(inventory, 'schema phase core_sha256 core_payload_sha256 input_binding topology_sha256 owners scope_members anchors reviewed_input_ids reviewed_span_ids complete state reviewer reason witnesses', 'independent inventory')
    require(inventory['schema']=='research-independent-permission-inventory/v1' and inventory['phase']=='before_discovery'
            and inventory['complete'] is True and inventory['state']=='known' and text(inventory['reviewer']) and text(inventory['reason']), 'complete independently reviewed pre-discovery inventory required')
    require(inventory['core_sha256']==vc['core_sha256'] and inventory['core_payload_sha256']==digest(core)
            and inventory['input_binding']==core_input_binding(core) and inventory['topology_sha256']==vc['owner_graph_sha256'], 'stale inventory core/input/topology')
    unique(inventory['owners'], MAX_OWNERS, 'all actual owners')
    require(set(inventory['owners']) == set(graph['owners']), 'all independently declared owners must be inventoried')
    input_ids={r['id'] for r in core['request_binding']['input_inventory']['items']}
    span_ids={r['span_id'] for r in core['request_binding']['active_spans']}
    require(core['request_binding']['input_inventory']['complete'] is True
            and set(inventory['reviewed_input_ids'])==input_ids and set(inventory['reviewed_span_ids'])==span_ids, 'missing or unreviewed actual input/span')
    anchors=anchors_from_core(core)
    require(inventory['anchors']==anchors, 'missing or extra protected anchor/whole-dimension inventory')
    scope_members={};effects={};preservations=[];full_original=[]
    for node in nodes:
        ctx=contexts[node['candidate_id']];require(node['realization_id']==ctx['realization_id'], 'actual RID mismatch')
        facts={f['id']:f for f in ctx['facts']};bindings={b['target']:b for b in node['bindings']}
        for b in node['bindings']:
            if b['selector_kind']=='existing_member_scope':
                sid=b['selection']['scope_id'];members=[m['owner_id'] for m in b['members']]
                require(members and (sid not in scope_members or scope_members[sid]==members), 'inconsistent actual member scopes')
                scope_members[sid]=members
        selected={f['fact_id'] for f in node['expanded_facts'] if f['mode']=='effect'}
        require(selected==set(ctx['canonical_effect_refs']), 'canonical E inventory changed')
        for f in node['expanded_facts']:
            source=facts[f['fact_id']]
            for k in ('mode','dimension','property','value','requires'):
                require(f[k]==source[k], 'canonical fact field changed: '+k)
            require(f['source_target']==source['target'], 'original source target changed')
            require(f['target'] in bindings[source['target']]['members'], 'target differs from same B1 binding')
            if f['mode']=='effect':
                require(f['operation']==source['operation'] and f['source_receivers']==source['receivers'], 'original op/all source Rx changed')
                expansions=[{'source_target':t,'selector_kind':bindings[t]['selector_kind'],'members':bindings[t]['members']} for t in source['receivers']]
                require(f['receiver_expansions']==expansions and f['canonical_receivers']==sorted({m['canonical_owner_id'] for b in expansions for m in b['members']}), 'all actual B1 Rx must remain unchanged')
                ek=digest({k:f[k] for k in ('candidate_id','realization_id','fact_id','expansion_index','target')})
                require(ek not in effects, 'duplicate canonical effect')
                effects[ek]=f;full_original.append(f)
            if f['fact_id'] in ctx['required_preservation_refs']:
                require(f['mode']=='preservation', 'PR mode changed')
                # Explicit request supplement, NOT a claim B1/B2 proved image PR matching.
                image=bindings.get('image',{}).get('members',[])
                require(len(image)==1, 'one exact active image required for research PR')
                candidates=[w for w in inventory['witnesses'] if w.get('source_fact_ref')==f['fact_id'] and w.get('candidate_id')==node['candidate_id']]
                require(len(candidates)==1, 'one independent same-item/same-image PR witness required')
                w=candidates[0]
                keys(w, 'candidate_id source_fact_ref target image dimension property value assertion_id input_ids span_ids frozen', 'PR witness')
                require(w['target']==f['target']['canonical_owner_id'] and w['image']==image[0]['canonical_owner_id']
                        and w['dimension']==f['dimension'] and w['property']==f['property'] and w['value']==f['value'] and w['frozen'] is True
                        and w['assertion_id'] in {a['assertion_id'] for a in core['semantic_assertions']}
                        and set(w['input_ids'])<=input_ids and w['input_ids'] and set(w['span_ids'])<=span_ids and w['span_ids'], 'missing/wrong/stale item/image visibility witness')
                native=[a for a in core['semantic_assertions'] if a['assertion_id']==w['assertion_id']]
                require(len(native)==1 and native[0]['axes'].get('owner')==w['target'] and native[0]['dimension']==w['dimension']
                        and native[0]['axes'].get('property')==w['property'] and native[0]['axes'].get('value_type')==w['value']['type']
                        and native[0]['axes'].get('value')==w['value']['value'], 'presence or another fact cannot proxy visibility')
                preservations.append(w)
    require(inventory['scope_members']==scope_members, 'independent complete scope differs from same B1 view')
    require(1<=len(effects)<=MAX_EFFECTS, 'bounded canonical E required')
    keys(assessment, 'schema inventory_sha256 resolved_view_sha256 source_bindings_sha256 reviewer anchors joint', 'manual semantic assessment')
    require(assessment['schema']=='research-source-anchor-impact-review/v1' and text(assessment['reviewer'])
            and assessment['inventory_sha256']==digest(inventory) and assessment['resolved_view_sha256']==digest(resolved_view)
            and assessment['source_bindings_sha256']==digest(expected.source_bindings), 'stale source/scope manual review')
    wanted={(e,digest(a)) for e in effects for a in anchors}
    joint_wanted={tuple(sorted((a,b))) for a in effects for b in effects if a!=b and effects[a]['candidate_id']!=effects[b]['candidate_id']}
    require(len(wanted)+len(joint_wanted)<=MAX_PAIRS, 'bounded exhaustive pair cap exceeded')
    decisions={};extra=[];reasons=[]
    for d in assessment['anchors']:
        keys(d, 'effect_key anchor_key impact reason input_ids span_ids preservation_ref', 'manual source/anchor decision')
        pair=(d['effect_key'],d['anchor_key'])
        require(pair in wanted and pair not in decisions and d['impact'] in {'affects','disjoint','unknown'} and text(d['reason'])
                and d['input_ids'] and set(d['input_ids'])<=input_ids and d['span_ids'] and set(d['span_ids'])<=span_ids, 'exact reviewed source/anchor pair and evidence required')
        decisions[pair]=d
        require(d['preservation_ref'] is None or any(w['source_fact_ref']==d['preservation_ref'] for w in preservations), 'unmatched claimed preservation')
        if d['preservation_ref'] is not None:
            anchor=next(a for a in anchors if digest(a)==d['anchor_key'])
            prs=[w for w in preservations if w['source_fact_ref']==d['preservation_ref']]
            require(anchor['kind']=='property' and any(anchor['target']==w['target']
                    and anchor['dimension']==w['dimension'] and anchor['property']==w['property'] for w in prs),
                    'a different owner/property/dimension cannot borrow item preservation')
        if d['impact']=='unknown':reasons.append('unknown anchor impact '+str(pair))
        if d['impact']=='affects':
            a=next(a for a in anchors if digest(a)==d['anchor_key']);extra.append(a);reasons.append('effect affects protected anchor '+str(pair))
    require(set(decisions)==wanted, 'missing source/anchor or whole-dimension decision')
    joint_seen=set()
    for d in assessment['joint']:
        keys(d, 'effect_keys impact reason input_ids span_ids', 'joint source effect decision')
        pair=tuple(sorted(d['effect_keys']))
        require(pair in joint_wanted and pair not in joint_seen and d['impact'] in {'affects','disjoint','unknown'} and text(d['reason'])
                and d['input_ids'] and set(d['input_ids'])<=input_ids and d['span_ids'] and set(d['span_ids'])<=span_ids, 'exact joint source review required')
        joint_seen.add(pair)
        if d['impact']!='disjoint':reasons.append('joint effect conflict or unknown '+str(pair))
    require(joint_seen==joint_wanted, 'missing joint source effect decision')
    scope=resolved_view['permission_scope'];primitive=primitives['property_effects_allowed']
    require(resolved_view['expanded_facts_sha256']==digest([n['expanded_facts'] for n in nodes])
            and resolved_view['permission_scope_sha256']==digest(scope), 'B1 expanded/scope transport digest mismatch')
    require(set(scope['dimensions'])=={f['dimension'] for f in full_original}, 'original effect dimensions cannot shrink')
    raw_expected={(f['dimension'],t,f['property']) for f in full_original for t in
                  [f['target']['owner_id'],*(m['owner_id'] for r in f['receiver_expansions'] for m in r['members'])]}
    require({(r['dimension'],r['target'],r['property']) for r in scope['literal_properties']}==raw_expected
            and len(scope['literal_properties'])==len(raw_expected), 'original literal target/Rx permission union missing or changed')
    ledger={}
    for f in full_original:
        k=(f['dimension'],f['target']['canonical_owner_id'],f['property'])
        entry={'dimension':f['dimension'],'target':f['target']['canonical_owner_id'],'property':f['property'],
               'value':f['value'],'operation':f['operation'],'receivers':f['canonical_receivers'],'sources':[]}
        prior=ledger.setdefault(k,entry)
        require(all(prior[n]==entry[n] for n in ('value','operation','receivers')), 'joint canonical assignments conflict')
        prior['sources'].append({k:f[k] for k in ('candidate_id','realization_id','fact_id','source_target','expansion_index','target')})
    require(resolved_view['effect_assignments']==[ledger[k] for k in sorted(ledger)], 'same B1 canonical assignment ledger required')
    require(callable(primitive) and callable(primitives['owner_relation']), 'independent frozen primitives required')
    if not primitive(core['intent_lock'],scope['dimensions'],scope['literal_properties'],owner_graph=graph):reasons.append('original target/Rx property lock')
    if set(scope['dimensions']) & set(core['intent_lock']['locked_dimensions']):reasons.append('original whole-dimension lock')
    # Exact B1 scope is never weakened, even if the manual plan falsely says disjoint.
    require(scope['properties']==sorted([dict(zip(('dimension','target','property'),v)) for v in
        {(f['dimension'],t,f['property']) for f in full_original for t in [f['target']['canonical_owner_id'],*f['canonical_receivers']]}], key=lambda v:(v['dimension'],v['target'],v['property'])), 'B1 original permission union missing or changed')
    # Known overlapping cross-candidate paths cannot be waived by a manual row.
    # Compare every actual target/Rx on both sides with the same pinned primitive
    # used for original locks, including aliases, part ancestors and unknown
    # owner separation. No new source fact, property alias or permission waiver.
    for a,b in joint_wanted:
        left,right=effects[a],effects[b]
        if not joint_properties_allowed(left, right, owner_graph=graph, property_primitive=primitive):
            reasons.append('actual joint property-path overlap')
    return {'schema':'research-permission-only-result/v1','permission_only_pass':not reasons,'reasons':sorted(set(reasons)),
            'original_expanded_effects':json.loads(canonical(full_original)), 'original_permission_scope':json.loads(canonical(scope)),
            'additional_anchor_comparisons':extra,'preservation_obligations':preservations,
            'pair_count':len(wanted)+len(joint_wanted),'binding':{'source_bindings':expected.source_bindings,'resolved_view_sha256':digest(resolved_view),
            'inventory_sha256':digest(inventory),'assessment_sha256':digest(assessment)},'native_qualified':False,'consumer_integrated':False}


def bind_source(context, contract):
    try:
        return _bind_source(context, contract)
    except (KeyError, TypeError, IndexError, StopIteration, RecursionError) as exc:
        raise ValueError('malformed full source envelope structure') from exc


def compare(bound_sources, **kwargs):
    try:
        return _compare(bound_sources, **kwargs)
    except (KeyError, TypeError, IndexError, StopIteration, RecursionError) as exc:
        raise ValueError('malformed permission comparison structure') from exc
