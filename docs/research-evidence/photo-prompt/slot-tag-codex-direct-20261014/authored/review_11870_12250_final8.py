"""Validate8 intent restorations; no canonical write, registration or model access."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
import photo_candidate_realizations as pr
L=runpy.run_path(str(R/'authored/review_11870_12250_final8_literals.py'));A=L['A']
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source()
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert dr.c.digest(d['slot_catalog'])=='4723660c37d3f665f883a81f0e8d35b8c690307406d18d63ade654527d5bec9c'
assert dr.c.digest(p)=='c5b08af3da0123f2736c87aa53b8fd8aa011a866e2a3b2aef83718f399acc2fc'
prior_file='authored/review_11870_12250_final17_reread.json';prior=json.loads((R/prior_file).read_text());before={x['candidate_id']:x['decision'] for x in prior['amendments'] if x['decision']['status']=='needs_boundary_review'}
assert hashlib.sha256((R/prior_file).read_bytes()).hexdigest()=='0a22158b427be2a33c0b453ab5759115b9368e1caa692b93156ccc66fd4417f9'
assert len(before)==8 and len(A)==8 and len({x[0] for x in A})==8
origin_path=dr.ROOT/L['ORIGIN'];origin=json.loads(origin_path.read_text());nodes={n['id']:n for n in origin['character_mechanism_graph']['runtime_nodes']}
output=R/'authored/review_11870_12250_final8.json';rows=[];cache={}
for o,after,meaning,reason,selected,effects in A:
 cid=p['ids'][o-12000];old=before[cid];record=d['candidates'][cid]
 assert pr.ids(record)==['base'] and dr.closure(d,cid)=={} and record['conditions']=={} and record['effects']==dict(dimensions=[],properties=[])
 prov=record['provenance'][0];node_id=prov['source'].split(':',1)[1];node=nodes[node_id]
 assert dr.c.digest(node)==prov['sha256'] and node['definition']==record['content']['definition']
 decision=copy.deepcopy(old);decision.update(meaning_summary=meaning,status='approved',uncertainties=[])
 decision['rejected_boundaries'].append(reason)
 decision['corrections']=[dict(pointer='/content/definition',before=record['content']['definition'],after=after,reason=reason),dict(pointer='/effects',before=copy.deepcopy(record['effects']),after=copy.deepcopy(effects),reason='Own only these individually reviewed carrier/property meanings on the clarified existing subject or garment. Source prerequisites, existing alternatives and no-new-carrier limits remain explicit; no unseen geometry, state value, cause or runtime permission is asserted.')]
 assert not decision['roles'] and not decision['facts']
 for slot,dim,owner,prop,quote,why in selected:
  f=dict(pointer='/content/definition',quote=quote,dimension=dim,target=owner,property=prop)
  decision['facts'].append(dict(f,realization_id='base'))
  decision['roles'].append(dict(slot_id=slot,semantic_role=d['slot_catalog'][slot]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=why,evidence=[f]))
 corrected=dr.corrected_record(record,decision['corrections']);assert corrected['record_kind']=='relationship_mechanism' and pr.ids(corrected)==['base']
 assert not set(dr.references(corrected))-set(dr.references(record))
 row={**dr.binding(d,cid,cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':dict(file=str(output.relative_to(dr.ROOT)),item=len(rows)+1,sha256=dr.c.digest(decision))}
 try:dr.validate_decision(row,d,binding_cache=cache)
 except Exception as e:raise ValueError((o,str(e))) from e
 rows.append(dict(ordinal=o,candidate_id=cid,before_authored_file=prior_file,before_authored_row_sha256=dr.c.digest(old),reread_id=f'review_11870_12250-final8-{o}-r3',model='gpt-6.1-sol',reasoning_effort='high',source_record_sha256=dr.c.digest(record),catalog_sha256=dr.c.digest(d['slot_catalog']),role_spec_sha256={slot:dr.c.digest(d['slot_catalog'][slot]) for slot,_,_,_,_,_ in selected},reference_sha256={},source_reread_complete=True,reference_reread_complete=True,full_corrected_source_reread=True,full_after_proposal_record=corrected,after_proposal_sha256=dr.c.digest(corrected),origin_evidence=dict(file=L['ORIGIN'],file_sha256=hashlib.sha256(origin_path.read_bytes()).hexdigest(),runtime_node_id=node_id,full_runtime_node=node,node_sha256=dr.c.digest(node),matches_source_provenance_sha256=True),source_contract_qualification=dict(restoration_basis='SHA-matched original node plus directly read original route context; metadata is not a positive evidence pointer',selected_source_roles_approved=True,native_effect_shape_and_decision_validation_passed=True,conditions_unchanged={},caller_must_supply_actual_owner_type_state_and_permission=True,textual_prerequisites_are_not_claimed_to_be_machine_enforced=True,canonical_source_applied=False,global_registration_or_runtime_pixel_qualification='not_performed'),resolved_prior_uncertainties=copy.deepcopy(old['uncertainties']),decision=decision))
assert {x['candidate_id'] for x in rows}==set(before)
support={}
for slot,indices in {'subject':[6,7,10,13,20],'action':[6,7,10,13,20],'prop':[7,10,13,20]}.items():
 for idx in indices:
  item=origin['slots'][slot][idx];support[f'/slots/{slot}/{idx}']=dict(sha256=dr.c.digest(item),record=item)
for idx,edge in enumerate(origin['character_mechanism_graph']['compatibility_edges']):
 if edge.get('topic_id') in {'hair_silhouette_state_change','wardrobe_role_state_separation','face_eye_gaze_impression','kemonomimi_nonhuman_anthropomorphism','creepy_cute_monster_moe'}:support[f'/character_mechanism_graph/compatibility_edges/{idx}']=dict(sha256=dr.c.digest(edge),record=edge)
body=dict(schema='photo-codex-direct-review-amendment/v1',source_sha256=dr.c.digest(d),source_snapshot_file_sha256=hashlib.sha256((R/'SOURCE.json.gz').read_bytes()).hexdigest(),catalog_sha256=dr.c.digest(d['slot_catalog']),packet_sha256=dr.c.digest(p),packet_file_sha256=hashlib.sha256((R/'packets/12000-250.json').read_bytes()).hexdigest(),amendments=rows,origin_route_context_actually_read=dict(file=L['ORIGIN'],file_sha256=hashlib.sha256(origin_path.read_bytes()).hexdigest(),records=support,use_limit='Carrier/source-class restoration only. Example occupations, age, actual actions, props, weather, species and event history were not adopted.'))
if '--write' in sys.argv:
 assert not output.exists(),'never overwrite frozen output';output.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(count=len(rows),statuses={'approved':len(rows)},ordinals=[x['ordinal'] for x in rows],unresolved=[],corrections_per_record=2,canonical_source_applied=False,written='--write' in sys.argv)))
