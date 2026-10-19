"""Mandatory source-opted permission and typed final preservation.

Trust boundary: only the orchestration process calls freeze_* after independent
manual review. Serialized candidate/core/composed fields never create handles.
Hashes bind reviewed inputs; they do not prove natural-language or pixel truth.
"""
from __future__ import annotations
import contextlib
import contextvars
import copy
import json
import weakref
import photo_permission_comparison as comparison
import photo_candidate_corpus as c

SCHEMA = 'photo-native-permission-envelope/v1'
_ACTIVE = contextvars.ContextVar('native_permission_trusted_session', default=None)
_HANDLES = weakref.WeakKeyDictionary()

class _Handle:
    __slots__ = ('__weakref__',)
    def __new__(cls):
        raise TypeError('trusted freeze API required; handles are not serialized input')

def _handle(kind, payload):
    h = object.__new__(_Handle)
    _HANDLES[h] = (kind, copy.deepcopy(payload))
    return h

def _payload(handle, kind):
    if type(handle) is not _Handle or handle not in _HANDLES or _HANDLES[handle][0] != kind:
        raise ValueError('trusted '+kind+' handle required')
    return copy.deepcopy(_HANDLES[handle][1])

def _require(test, message):
    if not test: raise ValueError(message)

def _keys(value, names, label):
    _require(isinstance(value, dict) and set(value) == set(names.split()), 'exact '+label+' fields required')

def _review(value):
    _require(isinstance(value, str) and bool(value.strip()), 'independent review identity required')

def declaration(record):
    return record.get('content',record).get('permission_envelope')

def validate_source_only_declaration(record):
    """Stage5C authoring syntax only; never native qualification/adoption."""
    import photo_semantic_evidence as n
    import photo_candidate_realizations as realizations
    d=declaration(record)
    if d is None:return
    _keys(d,'schema realizations','source-only permission declaration')
    _require(d['schema']==SCHEMA and isinstance(d['realizations'],dict)
             and set(d['realizations'])==set(realizations.ids(record)), 'source-only actual RID inventory required')
    for rid,contract in d['realizations'].items():
        _keys(contract,'canonical_effect_refs basis preservation','source-only RID permission contract')
        refs=contract['canonical_effect_refs']
        _require(isinstance(refs,list) and refs and len(refs)==len(set(refs))
             and all(n.concrete_owned_value(v) for v in refs), 'bounded explicit future E locator inventory required')
        effects=realizations.effects(record,rid)
        _require(effects['properties'] and set(effects['dimensions'])=={v['dimension'] for v in effects['properties']},
             'source-only opt-in retains exact nonempty declared E addresses')
        _require(isinstance(contract['basis'],list) and len(contract['basis'])==len(refs)
             and {v.get('fact_ref') for v in contract['basis']}==set(refs), 'source-only basis inventory required')
        for b in contract['basis']:
            _keys(b,'fact_ref unit_pointer rationale','source-only ordinary pointer basis')
            _require(b['unit_pointer'] in n.primary_paths(record,rid)
                and bool(n.positive_string(record,b['unit_pointer'],realization_id=rid).strip()), 'ordinary positive source pointer required')
            _review(b['rationale'])
        _require(isinstance(contract['preservation'],list) and len(contract['preservation'])<=comparison.MAX_EFFECTS,
                 'bounded source-only PR descriptors required')
        seen=set()
        for pr in contract['preservation']:
            _keys(pr,'fact_ref image_target relation_guard_id relation_property','source-only preservation descriptor')
            _require(pr['fact_ref'] not in seen and all(n.concrete_owned_value(v) for v in pr.values())
                and pr['image_target']=='image' and pr['relation_property']=='framing.visible_in', 'explicit scalar image PR locator required')
            seen.add(pr['fact_ref'])
    # Future fact locator-to-meaning, modes/values/Rx/ordinary unit membership
    # are deliberately unproved until a fresh full native proof is authored.


def validate_declaration(record, proof):
    """Symmetric source/proof opt-in, with direct ordinary source E anchors."""
    d = declaration(record)
    if d is None:
        _require('permission_envelopes' not in proof, 'proof cannot introduce a permission contract')
        return
    validate_source_only_declaration(record)
    _keys(d, 'schema realizations', 'source permission declaration')
    _require(d['schema'] == SCHEMA and isinstance(d['realizations'], dict)
             and set(d['realizations']) == set(proof['effect_sets']), 'exact permission RID inventory required')
    _require(proof.get('permission_envelopes') == d, 'source permission contract missing or changed in proof')
    for rid,contract in d['realizations'].items():
        validate_rid_contract(record,proof,rid,contract)


def validate_rid_contract(record,proof,rid,contract):
    import photo_semantic_evidence as n
    _keys(contract, 'canonical_effect_refs basis preservation', 'source RID permission contract')
    facts = {f['id']: f for f in proof['facts'] if f['realization_id'] == rid}
    refs = contract['canonical_effect_refs']
    _require(isinstance(refs, list) and refs and len(refs) == len(set(refs))
             and set(refs) == {k for k, f in facts.items() if f['mode'] == 'effect'}, 'all original E refs required')
    _require(isinstance(contract['basis'], list) and len(contract['basis']) == len(refs)
             and {b.get('fact_ref') for b in contract['basis']} == set(refs), 'exact direct E basis inventory required')
    for b in contract['basis']:
        _keys(b, 'fact_ref unit_pointer rationale', 'permission positive basis')
        f = facts[b['fact_ref']]
        units = [u for u in proof['source_units'] if u['realization_id'] == rid and u['pointer'] == b['unit_pointer']
                 and u['disposition'] == 'semantic' and f['id'] in u['fact_refs']]
        _require(len(units) == 1 and f['pointer'] == b['unit_pointer'] and f['quote'] in units[0]['quote']
                 and b['unit_pointer'] in n.primary_paths(record, rid), 'permission E basis must be ordinary full positive source')
        _review(b['rationale'])
    _require(isinstance(contract['preservation'], list) and len(contract['preservation']) <= comparison.MAX_EFFECTS,
             'bounded explicit preservation inventory required')
    _require({p.get('fact_ref') for p in contract['preservation']}=={k for k,f in facts.items() if f['mode']=='preservation'},
             'every source scalar preservation must retain a final obligation')
    seen = set()
    for p in contract['preservation']:
        _keys(p, 'fact_ref image_target relation_guard_id relation_property', 'scalar preservation descriptor')
        _require(p['fact_ref'] not in seen, 'duplicate scalar preservation descriptor'); seen.add(p['fact_ref'])
        f = facts.get(p['fact_ref'], {})
        _require(f.get('mode') == 'preservation' and f.get('value', {}).get('type') != 'frozen_property_reference/v1'
                 and p['relation_property'] == 'framing.visible_in' and p['image_target']=='image', 'literal scalar PR and exact image relation required')
        rules = [r for cond in proof['guard_sets'][rid]['source_conditions']
                 for r in (cond.get('native_guards') or {}).get('rules', []) if r['id'] == p['relation_guard_id']]
        _require(len(rules) == 1, 'one own-source same-image relation guard required')
        r = rules[0]
        _require(r.get('kind') == 'frozen_entity_relation' and r.get('dimension') == 'framing'
                 and r.get('property') == p['relation_property'] and r.get('value_type') == 'entity.owner_id/v1'
                 and r.get('left') == {'kind':'source_target','candidate_id':record['id'],'target':f['target']}
                 and r.get('right') == {'kind':'source_target','candidate_id':record['id'],'target':p['image_target']},
                 'PR guard must bind the same actual source item and image')
# Nonserialized transport witnesses, issued only by an explicit independently
# pinned source freeze or trusted immutable runtime-generation acquisition. Self-rehashed
# serialized compact payloads are never registered by admission itself.
_TRANSPORTS = {}

def _issue_validated_transport(record, proof, compact):
    manifest=declaration(record)
    original=c.digest(proof)
    row={'candidate_id':record['id'],'qualification_sha256':original,
         'meaning_sha256':proof['meaning_sha256'],'required':manifest is not None}
    _TRANSPORTS[original]=copy.deepcopy(row)
    _TRANSPORTS[c.digest(compact)]=copy.deepcopy(row)

def _register_generation_transports(guards, *, source_fingerprint, corpus_sha256):
    """Trusted runtime-provider hook after immutable generation verification.

    Not an entry/candidate API. A raw SearchReader checksum is insufficient:
    provider must verify generation, source/code fingerprint and layout first.
    No mandatory plan is issued, only source-preserving transport identity.
    """
    import photo_semantic_evidence as n
    _require(n._sha256(source_fingerprint) and n._sha256(corpus_sha256), 'verified generation source/corpus pins required')
    def visit(proof):
        if not isinstance(proof,dict) or proof.get('schema')!=n.SCHEMA:return
        _require(proof.get('compact_sha256')==c.digest({k:v for k,v in proof.items() if k!='compact_sha256'}), 'verified generation compact changed')
        row={'candidate_id':proof['candidate_id'],'qualification_sha256':proof['qualification_sha256'],
             'meaning_sha256':proof['meaning_sha256'],'required':'permission_envelopes' in proof,
             'source_fingerprint':source_fingerprint,'corpus_sha256':corpus_sha256}
        _TRANSPORTS[c.digest(proof)]=row
        for rows in proof['dependency_guards'].values():
            for child in rows:visit(child['guard'])
    for record in guards.values():visit(n.proof_of(record))

def transport(entry):
    import photo_semantic_evidence as n
    proof=n.proof_of(entry)
    _require(isinstance(proof,dict), 'qualified source transport required')
    row=_TRANSPORTS.get(c.digest(proof))
    _require(row is not None, 'source-bound validated transport required; self-hash is not authority')
    _require(row['candidate_id']==n._proof_cid(proof) and row['meaning_sha256']==proof.get('meaning_sha256')
        and row['qualification_sha256']==proof.get('qualification_sha256',c.digest(proof)), 'validated transport/source identity changed')
    return row

def authoritative_native_source(data,entry):
    import photo_semantic_evidence as n
    try:
        proof=n.proof_of(entry)
        cid=n._proof_cid(proof) if isinstance(proof,dict) else entry.get('source_candidate_id',entry.get('id'))
        record=data['candidates'][cid]
        return declaration(record) is not None or n.native_status(record)=='qualified'
    except (KeyError,TypeError,ValueError):return False


def matches_source(data,entry):
    """Consumer full/lazy authoritative data must agree with the actual entry."""
    import photo_semantic_evidence as n
    proof=n.proof_of(entry)
    if not isinstance(proof,dict):return not required(entry) and not authoritative_native_source(data,entry)
    try:
        cid=n._proof_cid(proof);record=data['candidates'][cid];actual=n.proof_of(record)
        if n.native_status(record)!='qualified':return False
        expected=actual if '_semantic_evidence_guard' in record else n.compact(record,data)
        return c.digest(proof) in {c.digest(actual),c.digest(expected)}
    except (ValueError,KeyError,TypeError,IndexError):return False


def freeze_source_authority(source_data, *, expected_snapshot_sha256, reviewer):
    """Trusted full-corpus selection. Expected digest comes from independent review.

    No file loading, discovery, inference, or candidate-provided expected pins.
    Every qualified source and closure is validated here before explicit trusted
    transport issuance. Selected full sources are rechecked when a plan freezes.
    """
    import photo_semantic_evidence as n
    _review(reviewer)
    _require(c.digest(source_data) == expected_snapshot_sha256, 'independent full source snapshot mismatch')
    data = copy.deepcopy(source_data)
    _require(isinstance(data.get('candidates'), dict) and isinstance(data.get('slot_catalog'), dict)
             and isinstance(data.get('slot_bindings'), dict), 'actual full corpus required')
    issuance=[]
    for r in data['candidates'].values():
        if declaration(r) is not None:
            _require(n.native_status(r) == 'qualified', 'mandatory source requires native qualification')
        if n.native_status(r)=='qualified':
            n.validate(r,data['slot_catalog'],corpus=data)
            issuance.append((r,n.proof_of(r),n.compact(r,data)))
        elif n.native_status(r)!='unqualified':
            raise ValueError('invalid source cannot receive independent authority')
    # Atomic issuance only after every qualified source/closure was checked.
    # Neither n.validate nor n.compact calls this trust operation.
    for record,proof,compact in issuance:_issue_validated_transport(record,proof,compact)
    return _handle('source authority', {'data':data,'snapshot':expected_snapshot_sha256,'reviewer':reviewer})

def _source_context(authority, node, manual):
    import photo_semantic_evidence as n
    data = authority['data']; cid = node['candidate_id']; rid = node['realization_id']; r = data['candidates'][cid]
    n.validate(r, data['slot_catalog'], corpus=data)
    proof = n.proof_of(r)
    _require(n.native_status(r) == 'qualified' and node['meaning_sha256'] == n.meaning_sha256(r)
             and node['qualification_sha256'] == c.digest(proof), 'actual full source authority differs from selected entry')
    required = declaration(r)
    if required is not None:
        contract = required['realizations'][rid]
        _require(manual == contract, 'manual contract differs from required full source contract')
    else:
        contract = manual
    _keys(contract, 'canonical_effect_refs basis preservation', 'selected manual permission contract')
    validate_rid_contract(r,proof,rid,contract)
    facts = [copy.deepcopy(f) for f in proof['facts'] if f['realization_id'] == rid]
    units = [copy.deepcopy(u) for u in proof['source_units'] if u['realization_id'] == rid and u['pointer'] in n.primary_paths(r, rid)]
    # Full native validation checks all reference units/constraints. The direct
    # basis below remains ordinary; no reference quote becomes a direct E claim.
    ctx = {'candidate_id':cid,'realization_id':rid,'source_snapshot_sha256':authority['snapshot'],
           'catalog_sha256':c.digest(data['slot_catalog']),'source_record':copy.deepcopy(r),'actual_effect_set':n.effect_set(r,rid),
           'facts':facts,'source_units':units,
           'positive_fields':[{'realization_id':rid,'pointer':p,'text':n.positive_string(r,p,realization_id=rid)}
                              for p in sorted(n.primary_paths(r,rid))],
           'ownbindings':{k:copy.deepcopy(v) for k,v in data['slot_bindings'].items() if v['candidate_id']==cid},
           'closure_snapshot':{'guards':copy.deepcopy(r['conditions']),'guard_set':copy.deepcopy(proof['guard_sets'][rid]),
              'profiles':copy.deepcopy(proof['profile_contracts'][rid]),'reference_sha256':copy.deepcopy(proof['reference_sha256']),
              'dependencies':copy.deepcopy(proof['dependencies'][rid]),'selected_children':copy.deepcopy(node['selected_children'])},
           'canonical_effect_refs':copy.deepcopy(contract['canonical_effect_refs']),
           'required_preservation_refs':[p['fact_ref'] for p in contract['preservation']]}
    ordinary = {'schema':'research-permission-envelope-contract/v1','candidate_id':cid,'realization_id':rid,'basis':copy.deepcopy(contract['basis'])}
    return comparison.bind_source(ctx, ordinary), contract

def _check_authority(context, authority):
    import photo_semantic_evidence as n
    data=authority['data']
    for cid,node in context['nodes'].items():
        record=data['candidates'].get(cid)
        _require(record is not None, 'selected source absent from independent full authority')
        n.validate(record,data['slot_catalog'],corpus=data)
        proof=n.proof_of(record)
        _require(node['meaning_sha256']==n.meaning_sha256(record) and node['qualification_sha256']==c.digest(proof),
                 'selected source qualification differs from independent full authority')
        allowed={c.digest(proof),c.digest(n.compact(record,data))}
        _require(context['entries'][cid]['proof_sha256'] in allowed, 'full/compact transport differs from independent full source')


def _original_preservations(context, contracts, core):
    """Typed frozen PR+same-image atoms, independently parsed from actual core."""
    import photo_semantic_evidence as n
    frozen = context['frozen']; graph = frozen['graph']; out = []
    by_id = {a['assertion_id']:a for a in core['semantic_assertions']}
    for cid, node in context['nodes'].items():
        bindings = {b['target']:b for b in node['bindings']}
        for descriptor in contracts[cid]['preservation']:
            matches = [f for f in node['expanded_facts'] if f['fact_id'] == descriptor['fact_ref']]
            _require(len(matches) == 1, 'scalar preservation cannot borrow a member-scope aggregate')
            f = matches[0]; images = bindings.get(descriptor['image_target'], {}).get('members', [])
            _require(len(images) == 1 and f['mode'] == 'preservation', 'one actual scalar image/PR required')
            item = f['target']['canonical_owner_id']; image = images[0]['canonical_owner_id']
            scalar = [a for a in frozen['facts'] if a['dimension'] == f['dimension'] and a['property'] == f['property']
                      and n._same_entity(graph,a['target'],item) and a['value'] == f['value']]
            relation = [a for a in frozen['facts'] if a['dimension'] == 'framing' and a['property'] == descriptor['relation_property']
                        and n._same_entity(graph,a['target'],item) and a['value']['type'] == 'entity.owner_id/v1'
                        and isinstance(a['value']['value'],str) and n._same_entity(graph,a['value']['value'],image)]
            _require(len(scalar) == len(relation) == 1, 'actual frozen scalar PR and same-image relation required')
            sa, ra = by_id[scalar[0]['assertion_id']], by_id[relation[0]['assertion_id']]
            out.append({'candidate_id':cid,'realization_id':node['realization_id'],'fact_ref':f['fact_id'],
                'relation_guard_id':descriptor['relation_guard_id'],'target':item,'image':image,
                'dimension':f['dimension'],'property':f['property'],'value':copy.deepcopy(f['value']),
                'relation_property':descriptor['relation_property'],'core_assertion_id':sa['assertion_id'],
                'relation_assertion_id':ra['assertion_id'],'source_span_ids':copy.deepcopy(sa['source_span_ids']),
                'relation_source_span_ids':copy.deepcopy(ra['source_span_ids']),
                'core_assertion_sha256':c.digest(sa),'relation_assertion_sha256':c.digest(ra),
                'input_binding':copy.deepcopy(comparison.core_input_binding(core))})
    return out

def freeze_permission_inventory(core, inventory, *, expected_inventory_sha256, reviewer):
    """Separate trusted pre-discovery review capability, with no candidate inputs.

    No inventory is synthesized here. All source inputs/owners/locks must have
    been manually inventoried before discovery. The chronology and semantic
    completeness remain trusted caller attestations, not self-hash proofs.
    """
    import photo_semantic_evidence as n
    _review(reviewer)
    _require(c.digest(inventory)==expected_inventory_sha256, 'independent inventory review hash mismatch')
    frozen=n.frozen_witnesses(core)
    _require(inventory.get('phase')=='before_discovery' and inventory.get('complete') is True
        and inventory.get('state')=='known' and inventory.get('core_payload_sha256')==c.digest(core)
        and inventory.get('core_sha256')==core.get('canonical_sha256')
        and inventory.get('input_binding')==comparison.core_input_binding(core)
        and inventory.get('topology_sha256')==c.digest(frozen['graph'])
        and set(inventory.get('owners',[]))==set(frozen['graph']['owners'])
        and inventory.get('anchors')==comparison.anchors_from_core(core), 'incomplete/stale pre-discovery inventory')
    rb=core['request_binding']
    _require(rb['input_inventory']['complete'] is True
        and set(inventory.get('reviewed_input_ids',[]))=={v['id'] for v in rb['input_inventory']['items']}
        and set(inventory.get('reviewed_span_ids',[]))=={v['span_id'] for v in rb['active_spans']},
        'every independent input/span must be reviewed before discovery')
    return _handle('permission inventory',{'core_sha256':c.digest(core),'inventory':inventory,'reviewer':reviewer,
                                        'inventory_sha256':expected_inventory_sha256})


def prepare_permission_review(authority, inventory, core, entries, *, contracts):
    """Lossless mechanical review packet, never an impact decision or approval.

    A separately frozen pre-discovery inventory is required before exposing the
    actual selected view. Human reviewers must author every impact/rationale.
    Returned dictionaries cannot be injected as trusted handles or receipts.
    """
    import photo_semantic_evidence as n
    a=_payload(authority,'source authority');i=_payload(inventory,'permission inventory')
    _require(i['core_sha256']==c.digest(core), 'pre-discovery inventory core changed')
    context=n._resolve_selected_native_contracts(entries,core);_check_authority(context,a)
    _require(set(contracts)==set(context['nodes']), 'complete actual selected closure contracts required')
    bindings={};sources={}
    for cid,node in context['nodes'].items():
        bound,_=_source_context(a,node,contracts[cid]);bindings[cid]=comparison.source_binding(bound)
        sources[cid]=json.loads(bound.payload)['context']
    return {'schema':'photo-native-permission-manual-review-packet/v1',
        'source_snapshot_sha256':a['snapshot'],'core_sha256':c.digest(core),
        'inventory_sha256':i['inventory_sha256'],'source_bindings':bindings,
        'resolved_view':copy.deepcopy(context['view']),'whole_selected_source_contexts':sources,
        'preservation_obligations':_original_preservations(context,contracts,core),
        'manual_impact_decisions_authored':False,'native_approval':False}


def freeze_permission_plan(authority, core, entries, *, inventory, assessment, contracts, reviewer):
    """Trusted manual plan freeze, never callable through a serialized receipt.

    Inventory is independently reviewed before discovery. Assessment/contract
    decisions are manually authored after reading the full selected source.
    Completeness is an attested semantic judgement, bounded and fail-closed.
    """
    import photo_semantic_evidence as n
    from photo_contracts import property_effects_allowed
    a = _payload(authority, 'source authority'); _review(reviewer)
    inventory_capability=_payload(inventory,'permission inventory')
    _require(inventory_capability['core_sha256']==c.digest(core), 'inventory belongs to another core')
    inventory=inventory_capability['inventory']
    context = n._resolve_selected_native_contracts(entries,core)
    _check_authority(context,a)
    _require(set(contracts) == set(context['nodes']), 'complete manual selected closure contracts required')
    bound=[];pins={};full_contracts={}
    for cid,node in context['nodes'].items():
        b, contract = _source_context(a,node,contracts[cid]);bound.append(b);pins[cid]=comparison.source_binding(b);full_contracts[cid]=contract
    expected = comparison.IndependentPins(pins,c.digest(context['view']),c.digest(inventory),c.digest(assessment))
    result = comparison.compare(bound, core=core,resolved_view=context['view'],inventory=inventory,assessment=assessment,
        expected=expected,primitives={'property_effects_allowed':property_effects_allowed,'owner_relation':n.witnesses.owner_relation})
    _require(result['permission_only_pass'], 'permission envelope denied: '+str(result['reasons']))
    obligations = _original_preservations(context,full_contracts,core)
    p = {'authority_snapshot':a['snapshot'],'core_sha256':c.digest(core),'view_sha256':c.digest(context['view']),
         'owner_graph':copy.deepcopy(context['frozen']['graph']),'inventory':copy.deepcopy(inventory),'assessment':copy.deepcopy(assessment),'contracts':copy.deepcopy(full_contracts),
         'source_bindings':pins,'result':result,'obligations':obligations,'reviewer':reviewer}
    p['plan_sha256']=c.digest(p)
    return _handle('permission plan',p)

@contextlib.contextmanager
def trusted_permission_session(authority, plan, *, after_state=None):
    a=_payload(authority,'source authority');p=_payload(plan,'permission plan')
    _require(a['snapshot']==p['authority_snapshot'], 'plan/source authority mismatch')
    after = _payload(after_state,'after state') if after_state is not None else None
    if after is not None:_require(after['plan_sha256']==p['plan_sha256'], 'after state belongs to another source plan')
    token=_ACTIVE.set((a,p,after))
    try:yield
    finally:_ACTIVE.reset(token)

def session_binding():
    active=_ACTIVE.get()
    return None if active is None else (active[0]['snapshot'],active[1]['plan_sha256'],
         active[2]['after_sha256'] if active[2] else None)

def required(entry):
    import photo_semantic_evidence as n
    proof=n.proof_of(entry)
    if declaration(entry) is not None or isinstance(proof,dict) and 'permission_envelopes' in proof:return True
    if isinstance(proof,dict) and _TRANSPORTS.get(c.digest(proof),{}).get('required'):return True
    active=_ACTIVE.get()
    if active is None:return False
    try:cid=n._proof_cid(proof) if isinstance(proof,dict) else entry.get('source_candidate_id',entry.get('id'))
    except (KeyError,TypeError):return True
    return declaration(active[0]['data']['candidates'].get(cid,{})) is not None

def enforce(context, entries, core):
    """Same B1 view and exact authority, mandatory even through compact/lazy routes."""
    active=_ACTIVE.get()
    expected_required = set()
    if active is not None:
        expected_required={cid for cid in context['nodes'] if declaration(active[0]['data']['candidates'].get(cid,{})) is not None}
    if not expected_required and not any(required(e) for e in entries) and not any(
            context['entries'][cid].get('permission_required') for cid in context['nodes']):return None
    _require(active is not None, 'mandatory permission authority/plan missing')
    a,p,_=active
    _require(p['core_sha256']==c.digest(core) and p['view_sha256']==c.digest(context['view']), 'stale permission core/selected B1 view')
    _check_authority(context,a)
    _require(set(context['nodes'])==set(p['source_bindings']), 'permission plan selected closure changed')
    return copy.deepcopy({'schema':'photo-native-permission-receipt/v1','plan_sha256':p['plan_sha256'],
        'source_snapshot_sha256':a['snapshot'],'resolved_view_sha256':p['view_sha256'],
        'inventory_sha256':c.digest(p['inventory']),'assessment_sha256':c.digest(p['assessment']),
        'original_permission_scope_sha256':c.digest(p['result']['original_permission_scope']),
        'preservation_obligations':p['obligations']})

def freeze_after_state(plan, after_core, *, expected_after_sha256, evidence, reviewer):
    """Independent typed result input, not prompt substring or candidate receipts.

    Evidence explicitly maps each original obligation to result scalar/relation
    assertions. Native witness parsing checks active spans/types/topology. The
    trusted caller still reviews actual source meaning; pixels are not inferred.
    """
    import photo_semantic_evidence as n
    p=_payload(plan,'permission plan');_review(reviewer)
    _require(c.digest(after_core)==expected_after_sha256, 'independent typed after-state hash mismatch')
    frozen=n.frozen_witnesses(after_core);binding=n.witnesses.input_binding(after_core['request_binding'])
    graph=frozen['graph'];canonical,_=n.witnesses.validate_graph(graph)
    _require(graph==p['owner_graph'], 'result actual owner/alias/ancestor topology differs from frozen plan')
    _require(binding is not None and after_core['request_binding']['input_inventory']['complete'] is True,
             'complete independent after-state input inventory required')
    _require(isinstance(evidence,list) and len(evidence)==len(p['obligations']), 'all scalar PR result evidence required')
    wanted={(o['candidate_id'],o['realization_id'],o['fact_ref']) for o in p['obligations']};seen=set();receipts=[]
    assertions={a['assertion_id']:a for a in after_core['semantic_assertions']}
    for e in evidence:
        _keys(e,'candidate_id realization_id fact_ref original_assertion_sha256 original_relation_sha256 scalar_assertion_id relation_assertion_id','typed after-state PR evidence')
        key=(e['candidate_id'],e['realization_id'],e['fact_ref'])
        _require(key in wanted and key not in seen,'missing/duplicate/foreign result preservation');seen.add(key)
        o=next(o for o in p['obligations'] if key==(o['candidate_id'],o['realization_id'],o['fact_ref']))
        _require(e['original_assertion_sha256']==o['core_assertion_sha256'] and e['original_relation_sha256']==o['relation_assertion_sha256'],
                 'result evidence must bind original scalar and image source assertions')
        _require(o['target'] in canonical and o['image'] in canonical, 'same original actual item/image required in result')
        rows={f['assertion_id']:f for f in frozen['facts']};s=rows.get(e['scalar_assertion_id']);r=rows.get(e['relation_assertion_id'])
        _require(s is not None and r is not None and n._same_entity(graph,s['target'],o['target'])
             and s['dimension']==o['dimension'] and s['property']==o['property'] and s['value']==o['value']
             and n._same_entity(graph,r['target'],o['target']) and r['dimension']=='framing'
             and r['property']==o['relation_property'] and r['value']['type']=='entity.owner_id/v1'
             and isinstance(r['value']['value'],str) and n._same_entity(graph,r['value']['value'],o['image']),
             'typed result contradicts or omits same-item/same-image scalar preservation')
        receipts.append({'obligation':copy.deepcopy(o),'result_evidence':copy.deepcopy(e),
            'scalar_assertion':copy.deepcopy(assertions[s['assertion_id']]),'relation_assertion':copy.deepcopy(assertions[r['assertion_id']]),
            'result_input_binding':copy.deepcopy(binding),
            'result_source_spans':[copy.deepcopy(span) for span in after_core['request_binding']['active_spans']
                if span.get('source_span_id',span.get('span_id')) in set(assertions[s['assertion_id']]['source_span_ids']+assertions[r['assertion_id']]['source_span_ids'])],
            'result_input_inventory':copy.deepcopy(after_core['request_binding']['input_inventory'])})
    payload={'schema':'photo-native-final-preservation-receipt/v1','plan_sha256':p['plan_sha256'],
       'source_snapshot_sha256':p['authority_snapshot'],'after_input_sha256':expected_after_sha256,
       'after_core':copy.deepcopy(after_core),'receipts':receipts,'reviewer':reviewer}
    payload['after_sha256']=c.digest(payload)
    return _handle('after state',payload)

def final_preservation(context, entries, core):
    receipt=enforce(context,entries,core)
    if receipt is None:return None
    active=_ACTIVE.get();a,p,after=active
    if p['obligations']:
        _require(after is not None and after['plan_sha256']==p['plan_sha256'], 'independently frozen typed final PR state required')
        return {k:copy.deepcopy(v) for k,v in after.items() if k!='after_core'}
    return {'schema':'photo-native-final-preservation-receipt/v1','plan_sha256':p['plan_sha256'],
            'source_snapshot_sha256':a['snapshot'],'receipts':[]}
