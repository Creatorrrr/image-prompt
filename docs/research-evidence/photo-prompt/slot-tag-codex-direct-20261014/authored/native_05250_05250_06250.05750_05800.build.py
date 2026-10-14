"""Serialize explicit cells and check bindings; no semantic generation."""
import copy, hashlib, json, runpy, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
import direct_review as dr
import photo_semantic_evidence as ne
P=json.loads((R/'authored/native_05250_05250_06250.05750_05800.packet.json').read_text())
prior_path=R/'authored/native_05250_05250_06250.05750_05795.draft_before_reread.json'
prior=json.loads(prior_path.read_text())
prior_by_ordinal={row['ordinal']:row for row in prior['records']}
CAT=json.loads((R/'CATALOG-FINAL-144-V4.json').read_text())
D=runpy.run_path(str(R/'authored/native_05250_05250_06250.05750_05800.literals.py'))['D']
rows=[]
for ordinal,a in D.items():
    assert ordinal==5750+len(rows)
    p=P['records'][ordinal-5750]
    after=copy.deepcopy(p['after_existing5B'])
    text_delta=[]
    for correction in a.get('text_corrections',[]):
        parts=correction['pointer'][1:].split('/')
        parent=after
        for key in parts[:-1]:parent=parent[key]
        key=parts[-1]
        assert parent[key]==correction['before']
        parent[key]=correction['after']
        text_delta.append(dict(pointer=correction['pointer'],before_exists=True,before=correction['before'],
            after_exists=True,after=correction['after'],reason=correction['reason']))
    effects=dict(dimensions=sorted({dim for dim,target,prop in a['effects']}),
        properties=sorted([dict(dimension=dim,target=target,property=prop) for dim,target,prop in a['effects']],
            key=lambda row:(row['dimension'],row['target'],row['property'])))
    after['effects']=effects
    assert ne.realizations.ids(after)==['base']
    facts=[]
    for ident,path,claim,quote in a['anchors']:
        dim,target,prop,mode,typ,value,requires,operation,receivers=a['claims'][claim]
        assert quote in ne.positive_string(after,path,realization_id='base')
        fact=dict(id=ident,realization_id='base',pointer=path,quote=quote,dimension=dim,
            target=target,property=prop,mode=mode,value=dict(type=typ,value=value),requires=requires)
        if mode=='effect':
            assert operation is not None and receivers is not None
            fact.update(operation=operation,receivers=receivers)
        else: assert operation is None and receivers is None
        facts.append(fact)
    byid={f['id']:f for f in facts}
    assert len(byid)==len(facts)
    for fact in facts:
        assert all(ref in byid and byid[ref]['mode'] in {'prerequisite','preservation'} for ref in fact['requires'])
    units=[]
    for path,refs in a['units'].items():
        quote=ne.positive_string(after,path,realization_id='base')
        assert refs and all(byid[ref]['pointer']==path for ref in refs)
        units.append(dict(realization_id='base',pointer=path,quote=quote,fact_refs=refs,disposition='semantic'))
    assert ne.primary_paths(after,'base') <= set(a['units'])  # Actual native contract permits reviewed extra positive strings.
    assert {ref for unit in units for ref in unit['fact_refs']}==set(byid)
    assert {tuple(f[k] for k in ('dimension','target','property')) for f in facts if f['mode']=='effect'}==set(a['effects'])
    roles={}
    for tag,(refs,modes) in a['roles'].items():
        for ref in refs:
            fact=byid[ref]
            assert fact['dimension'] in CAT[tag]['dimensions']
            assert any(fact['property'].startswith(prefix) for prefix in CAT[tag]['property_prefixes'])
            assert fact['mode'] in modes
        roles[tag]=dict(spec_sha256=dr.c.digest(CAT[tag]),scope='whole_record',realization_ids=['base'],fact_refs=refs,support_modes=modes)
    literal_bindings=a['bindings'] if 'bindings' in a else [a['binding']]
    bindings={}
    for bid,slot,role,semantic,conditions,weight in literal_bindings:
        assert bid not in bindings
        bindings[bid]=dict(id=bid,candidate_id=p['candidate_id'],slot_id=slot,role=role,semantic_role=semantic,conditions=conditions,weight=weight)
    assert dr.c.canonical_bytes(p['own_existing_bindings'])==dr.c.canonical_bytes(bindings)
    assert not p['required_reference_records'] and not p['explicit_reference_bindings']
    assert after['conditions']==p['source_before']['conditions']
    delta=text_delta
    if effects!=p['after_existing5B']['effects']:
        delta.append(dict(pointer='/effects',before_exists=True,before=p['after_existing5B']['effects'],
            after_exists=True,after=effects,reason=a['effect_reason']))
    rows.append(dict(ordinal=ordinal,candidate_id=p['candidate_id'],status='manual_native_draft_not_qualified',
        meaning=a['meaning'],source_before=p['source_before'],historical5B_after=p['after_existing5B'],
        source_after_proposal=after,source_delta_from_historical5B_after=delta,source_proposal_approved=False,
        original5B=p['registered5B'],original_compiled_locator=p['original_compiled_locator'],
        actual_rids=['base'],facts=facts,role_proposals=roles,source_units=units,
        local_effect_sets={'base':effects},original_own_bindings=p['own_existing_bindings'],
        binding_intent=a['binding_intent'],dependencies=a['dependencies'],
        reference_records=p['required_reference_records'],reference_bindings=p['explicit_reference_bindings'],
        source_intrinsic_conditions=after['conditions'],owner_maps=None,owner_resolution=a['owner_issue'],
        creation_permission_proposed=a['creation_permission'],creation_permission_approved=False,
        rejected_boundaries=[a['boundary']],formal_native_proof=None,native_signature=None))
reused=[]
for index,row in enumerate(rows):
    previous=prior_by_ordinal.get(row['ordinal'])
    if previous is not None and dr.c.canonical_bytes(previous['source_after_proposal'])==dr.c.canonical_bytes(row['source_after_proposal']):
        row['source_reread_exact_reuse']=dict(candidate_id=row['candidate_id'],
            current_pointer='/records/'+str(index)+'/source_after_proposal',
            previous_file=str(prior_path.relative_to(R)),
            previous_file_byte_sha256=hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            previous_pointer='/records/'+str(row['ordinal']-5750)+'/source_after_proposal',
            source_record_sha256=dr.c.digest(row['source_after_proposal']),
            comparison='complete canonical JSON exactly equal; no semantic string/condition/effect omitted')
        reused.append(row['ordinal'])
stop=5750+len(rows)
doc=dict(schema='photo-worker-manual-native-draft/v1',task_name='/root/review_05250_06250',
    model='gpt-6.1-sol',reasoning_effort='high',source_sha256=P['source_sha256'],
    catalog_sha256=dr.c.digest(CAT),prepared_count=50,actual_read_count=len(rows),
    fully_authored_count=len(rows),complete_interval=[5750,stop],unread_or_unauthored_tail=[stop,5800],
    formal_root_input_assignment_pending=True,formal_native_qualified_count=0,
    whole_final_catalog_reviewed=False,records=rows)
out=R/f'authored/native_05250_05250_06250.05750_{stop:05d}.draft_before_reread.json'
with out.open('x') as f:f.write(json.dumps(doc,ensure_ascii=False,separators=(',',':'))+'\n')
print(json.dumps(dict(path=str(out.relative_to(R)),actual_read_count=len(rows),fully_authored_count=len(rows),
    qualified=0,byte_sha256=hashlib.sha256(out.read_bytes()).hexdigest())))
print(json.dumps(dict(exact_source_reuse_ordinals=reused,previous_directly_read_source_file=str(prior_path.relative_to(R)) if prior_path else None,
    per_CID_pointers_hashes_and_complete_equality_bindings_saved_in_each_record=True)))
for row in rows:
    if 'source_reread_exact_reuse' not in row:
        print(row['ordinal'],json.dumps(row['source_after_proposal'],ensure_ascii=False,separators=(',',':')))
