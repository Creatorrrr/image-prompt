import sys,json,copy,runpy,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import native_reviews as nr;import photo_semantic_evidence as n
L=runpy.run_path(str(R/'authored/native_12250_09250_10250.09450_09500.literals.py'));D=L['D'];OPS=L['OPS'];P=json.loads((R/'authored/native_12250_09250_10250.09450_09500.input.json').read_text());CAT=json.loads((R/'CATALOG-FINAL-149-V6.json').read_text());rows=[]
def at(v,p):
 for k in p[1:].split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 return v
for ordinal,a in D.items():
 assert ordinal==9450+len(rows);p=P['records'][ordinal-9450];before=p['source_before'];after=copy.deepcopy(before);effects=dict(dimensions=sorted({e[0] for e in a['effects']}),properties=[dict(zip(('dimension','target','property'),e)) for e in a['effects']]);delta=[]
 # Historical proposals remain distinct from operating source and require explicit authored corrections below.
 for old in p['registered5B']['row']['corrections']:
  assert any(c['pointer']==old['pointer'] and c['before']==old['before'] and c['after']==old['after'] for c in a.get('text_corrections',[])) or any(c['pointer']==old['pointer'] and c['before']==old['before'] and c['after']==old['after'] and c['disposition']=='withdrawn_not_applied_to_operating_source' and bool(c['reason']) for c in a.get('historical_correction_dispositions',[]))
 after['effects']=effects
 if effects!=before['effects']:delta.append(dict(pointer='/effects',before_exists=True,before=before['effects'],after_exists=True,after=effects,reason=a['meaning']+' Whole source requires this concrete footprint; contextual role naming does not waive real mutation. '+a['boundary']))
 for correction in a.get('text_corrections',[]):
  pointer=correction['pointer'];assert at(after,pointer)==correction['before'];parent=after
  for key in pointer[1:].split('/')[:-1]:parent=parent[int(key)] if isinstance(parent,list) else parent[key]
  key=pointer.split('/')[-1];parent[int(key) if isinstance(parent,list) else key]=correction['after'];delta.append(dict(pointer=pointer,before_exists=True,before=correction['before'],after_exists=True,after=correction['after'],reason=correction['reason']))
 assert nr.exact(nr.apply_delta(before,delta),after)
 facts=[]
 for ident,pointer,quote,dim,target,prop,mode,vtype,value,requires in a['facts']:
  assert quote in n.positive_string(after,pointer,realization_id='base')
  f=dict(id=ident,realization_id='base',pointer=pointer,quote=quote,dimension=dim,target=target,property=prop,mode=mode,value=dict(type=vtype,value=value),requires=requires)
  if mode=='effect':operation,receivers=OPS[ordinal][ident];f.update(operation=operation,receivers=receivers)
  facts.append(f)
 assert set(OPS[ordinal])=={f['id'] for f in facts if f['mode']=='effect'}
 roles={tag:dict(spec_sha256=d.c.digest(CAT[tag]),scope='whole_record',realization_ids=['base'],fact_refs=refs,support_modes=modes) for tag,(refs,modes) in a['roles'].items()}
 for tag,r in roles.items():
  for ref in r['fact_refs']:
   f=next(f for f in facts if f['id']==ref);assert f['dimension'] in CAT[tag]['dimensions'];assert any(f['property'].startswith(prefix) for prefix in CAT[tag]['property_prefixes']);assert f['mode'] in r['support_modes']
 units=[dict(realization_id='base',pointer=pointer,quote=at(after,pointer),fact_refs=refs,disposition='semantic') for pointer,refs in a['units'].items()];assert {u['pointer'] for u in units}==n.primary_paths(after,'base')
 for f in facts:assert any(u['pointer']==f['pointer'] and f['id'] in u['fact_refs'] for u in units)
 authored_bindings={}
 for bid,slot,role,semantic,conditions,weight in a.get('bindings',[a.get('binding')]):
  binding=dict(id=bid,candidate_id=p['candidate_id'],slot_id=slot,role=role,semantic_role=semantic,conditions=conditions,weight=weight);authored_bindings[bid]=binding
 assert p['own_bindings']==authored_bindings;assert p['reference_records']=={} and p['reference_bindings']=={}
 assert after['conditions']==before['conditions'] and after['record_kind']==a['kind']
 rows.append(dict(ordinal=ordinal,candidate_id=p['candidate_id'],status='manual_native_draft_not_qualified',meaning=a['meaning'],original_source=p['original_source'],current_snapshot_sha256=P['current_snapshot_sha256'],source_before=before,historical5B_after=p['historical5B_after_correction_proposal'],source_after=after,delta=delta,original5B=p['registered5B'],historical_correction_dispositions=a.get('historical_correction_dispositions',[]),actual_rids=['base'],all_roles_individually_considered=True,role_proposals=roles,facts=facts,source_units=units,local_effect_sets={'base':effects},guard_sets={'base':dict(source_conditions=[before['conditions'],{}],member_conditions={})},profile_contracts={'base':None},original_own_bindings=authored_bindings,binding_policy='Exact actual own binding ID/CID/conditions/slot/role/semantic_role/weight manually retained. No new binding ID or new-role binding policy is fabricated. Its condition is AND with intrinsic source condition; catalog broadening never erases the old guard. Binding migration remains root/policy work.',dependencies={'base':[]},reference_records={},reference_bindings={},owner_maps=a.get('owner_maps'),source_application_analysis=a.get('source_application_analysis'),owner_resolution=a['owner_issue'],rejected_boundaries=[a['boundary']],formal_native_proof=None,native_signature=None,creation_permission_proposed=any(f.get('operation')=='add_entity' for f in facts),creation_permission_approved=False))
start=9450;stop=start+len(rows);out=R/f'authored/native_12250_09250_10250.{start:05d}_{stop:05d}.draft_before_reread.json';doc=dict(schema='photo-worker-manual-native-research-draft/v2',task_name='review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',source_sha256=P['source_sha256'],current_snapshot_sha256=P['current_snapshot_sha256'],current_snapshot_file=P['current_snapshot_file'],source_snapshot_catalog_sha256=P['source_snapshot_catalog_sha256'],catalog_file=P['catalog_file'],review_catalog_separately_root_pinned=True,catalog_sha256=d.c.digest(CAT),prepared_count=50,actual_read_count=len(rows),fully_authored_count=len(rows),complete_interval=[start,stop],unread_prepared_tail=[stop,9500],records=rows,whole_final_catalog_reviewed=False,formal_native_qualified_count=0)
d.write(out,doc);print(json.dumps(dict(path=str(out),count=len(rows),actual_read_count=len(rows),prepared_count=50)))
for r in rows:print(r['ordinal'],json.dumps(r['source_after'],ensure_ascii=False,separators=(',',':')))
