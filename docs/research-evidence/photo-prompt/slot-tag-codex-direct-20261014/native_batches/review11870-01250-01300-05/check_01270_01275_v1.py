"""Explicit independent controlled fixtures; every effect target/Rx, typed P and branch boundary."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-05';D=R/'native-inputs/prepared/review11870-01250-01300-05';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import prompt_generator as generator
import photo_search_layout as layout
import photo_role_proposals as proposals
assert hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest()=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
assert hashlib.sha256(Path(generator.__file__).read_bytes()).hexdigest()=='c7cba5732ef623c32ad3ac13459985fc8d1a2d00b26194d3d0ce2fd41f8c6138'
J=json.loads((O/'CHECKPOINT-01270-01275-v1.json').read_text());assert c.digest(J)=='1cd50cd12727f0020c5ea022b629c754246ab91bcaf0225260c890ef3c1e30d3';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
TEXT='Independent synthetic baseline: existing fairy-light source L and image I; actual hand H and Polaroid print set T explicitly distinct; existing leather surface B and different freshwater surface W. Existing action figure F and existing doll D are alternative caller targets, never newly added; human applicability is independently declared in the test contract. Existing air volume A and scene Q. These declarations are synthetic controlled witnesses, not a real request or source-derived core.'
def assertion(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}}
def core(owners,roles,values,relations,opendims):
 rows=[assertion('o'+str(j),'owner',owner=x,owner_kind='entity')for j,x in enumerate(owners)]+[assertion('r'+str(j),'role',owner=x,role=role)for j,(role,x)in enumerate(roles)]+[assertion('f'+str(j),'fact',d,owner=x,property=p,value_type=t,value=v)for j,(d,x,p,t,v)in enumerate(values)]+[assertion('rel'+str(j),kind,left=l,right=r)for j,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':TEXT}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
light=core(['L','I'],[('light_source','L'),('image','I')],[('lighting','L','lighting.source.type','lighting.source.type/v1','fairy_lights'),('subject','I','entity.presence','entity.presence/v1','present')],[],['camera'])
hand=core(['H','T'],[('primary_hands','H'),('primary_prop','T')],[('subject','H','entity.type','entity.type/v1','hand'),('subject','T','props.type','props.type/v1','polaroid_print_set')],[('disjoint','H','T')],['action','role'])
leather=core(['B','W'],[],[('subject','B','entity.presence','entity.presence/v1','present'),('material','B','surface.material','surface.material/v1','leather'),('subject','W','entity.presence','entity.presence/v1','present'),('material','W','surface.material','surface.material/v1','freshwater')],[],['material'])
toy=core(['F','D'],[],[('subject','F','props.type','props.type/v1','action_figure'),('subject','D','props.type','props.type/v1','doll')],[],['appearance','role'])
air=core(['A','Q'],[('light_receiver','A'),('scene','Q')],[('subject','A','entity.type','entity.type/v1','air_volume'),('subject','Q','entity.presence','entity.presence/v1','present')],[],['lighting','atmosphere'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def entry(o,rid,binding=True):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0]if binding else None,realization_id=rid)
def choose(o,rid,k,owner=None,view='full'):
 e=entry(o,rid);k=copy.deepcopy(k)
 if owner is not None:
  k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];target='surface'if o==1272 else'toy'
  e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':rid,'meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':target,'owner_id':owner}]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
configs=[(1270,'base',light,None,'environment',[('fact','L','lighting.source.type'),('fact','I','entity.presence')]),(1271,'base',hand,None,'human',[('fact','H','entity.type'),('fact','T','props.type'),('disjoint','H','T')]),(1272,'base',leather,'B','environment',[('fact','B','entity.presence'),('fact','B','surface.material')]),(1273,'small_action_figure',toy,'F','human',[('fact','F','props.type')]),(1273,'small_doll',toy,'D','human',[('fact','D','props.type')]),(1274,'base',air,None,'environment',[('fact','A','entity.type'),('fact','Q','entity.presence')])]
results=[];views=[];extra=[]
for o,rid,k,owner,category,atoms in configs:
 e,k=choose(o,rid,k,owner);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for view in ['full','compact']:
  z,kk=choose(o,rid,k,owner,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,rid,view,receipt)
  assert generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,rid,view,'baseconsumer',generator.entry_block_reason(z,picked(category)))
  checks.append({'case':'independent_precise_P_and_actual_branch','view':view,'admission':receipt,'same_actual_ownbinding_consumer_allowed':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,rid,bad,owner,view)
   assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,rid,view,'property',prop)
   assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,rid,view,'consumerproperty',prop)
   checks.append({'case':'every_actual_E_target_and_receiver_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_ownbinding_consumer_denied':True})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['open_dimensions'].remove(dim);bad['intent_lock']['locked_dimensions'].append(dim);z,kk=choose(o,rid,bad,owner,view)
   assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,rid,view,'whole',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_ownbinding_consumer_denied':True})
 for kind,x,p in atoms:
  a=next(a for a in k['semantic_assertions']if a['axes']['kind']==kind and((kind=='fact'and a['axes']['owner']==x and a['axes']['property']==p)or(kind!='fact'and a['axes']['left']==x and a['axes']['right']==p)))
  bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,kk=choose(o,rid,bad,owner,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,rid,view,'missingP',a,receipt);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z)
   checks.append({'case':'manually_identified_required_precise_P_or_disjoint','view':view,'removed':a,'admission':receipt,'actual_ownbinding_consumer_denied':True})
 results.append({'ordinal':o,'realization_id':rid,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'core':k,'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks})
 if o==1271:
  rec=S['candidates'][e['id']];guard=layout.guard_record(rec,S)
  for role in ['relational_action','contact_point']:
   spec=S['slot_catalog'][role];full=n.qualification(spec,rec,source_data=S);compact=n.qualification(spec,guard,source_data=S);assert full==compact and full['status']=='eligible'and full['matched_manual_role_views'],(role,full,compact)
   noauthority=n.qualification(spec,guard);assert noauthority['status']=='review_required'
   proposal=proposals.propose(S,role,e['id'],[]);assert proposal['semantic_fit']['status']=='eligible'
   for view in ['full','compact']:
    z,kk=choose(o,rid,k,owner,view);assert generator.core_entry_eligible(S,kk,contract(category),picked(category),role,z)
   assert ds==['action','role']
   views.append({'role':role,'fullcompact_qualification':full,'without_fullsource_authority':noauthority,'proposal':proposal,'same_actual_ownbinding_consumer_newrole_fullcompact_allowed':True,'canonical_E_dimensions_unchanged':ds,'canonical_E_target_Rx_properties':ps})
# A fresh actual owner choice and exact selected toy identity are mandatory; branch source guards are not decoration.
for o,rid,k,wrong,category in [(1272,'base',leather,'W','environment'),(1273,'small_action_figure',toy,'D','human'),(1273,'small_doll',toy,'F','human')]:
 for view in ['full','compact']:
  z,kk=choose(o,rid,k,wrong,view);receipt=n.admission(z,kk);assert not receipt['allowed'];assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),z['_presentation_role'],z);extra.append({'ordinal':o,'rid':rid,'view':view,'case':'wrong_actual_selected_precise_identity','admission':receipt,'consumer_denied':True})
  z,kk=choose(o,rid,k,None,view);receipt=n.admission(z,kk);assert not receipt['allowed'];extra.append({'ordinal':o,'rid':rid,'view':view,'case':'caller_selection_missing','admission':receipt})
# Intrinsic human remains despite unrestricted prop/contact roles. Never type the toy itself as a human.
for o,rid,k,owner in [(1271,'base',hand,None),(1273,'small_action_figure',toy,'F'),(1273,'small_doll',toy,'D')]:
 for view in ['full','compact']:
  z,kk=choose(o,rid,k,owner,view);assert not generator.core_entry_eligible(S,kk,contract('object'),picked('object'),z['_presentation_role'],z);extra.append({'ordinal':o,'rid':rid,'view':view,'case':'source_intrinsic_human_not_waived_by_new_role','object_consumer_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_role_view_checks':views,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Six actualRID controlled independent fixtures for five sourceproofs. Every actualE+Rx property, whole dimension, exactrequiredP/disjoint and selectedbranch identity checked fullcompact.1271 two manualviews retain full actionE and actualsamehand/printsetRx; no relationshipE. No realrequest freeze/runtime/render/pixel/rootapproval.'}
p=O/'CHECKS-01270-01275-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
