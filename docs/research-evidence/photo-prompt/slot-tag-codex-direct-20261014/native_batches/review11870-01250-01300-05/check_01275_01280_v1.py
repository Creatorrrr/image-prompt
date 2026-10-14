"""Controlled independent actual endpoint/P witnesses and fullcompact consumer/lock negatives."""
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
J=json.loads((O/'CHECKPOINT-01275-01280-v1.json').read_text());assert c.digest(J)=='e3afc369d6a9720080149895043c49c12168d1496dd37a2a6071dcdbfcec1aeb';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
TEXT='Independent synthetic baseline: existing human person P and exact star-map tablet T are distinct, tablet declared star-map representation content fixed. Existing recording camera C, image I and railing R; existing human person P. Caller selects existing human character U, existing actual face F and existing hands-region H containing declared hands. F and H are distinct and each actually part of same U, with neutral independent presence for each. Existing scene Q. Only declared candidate effect dimensions are mutable. This is a controlled synthetic request, not a source-derived witness or real request.'
def assertion(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}}
def core(owners,roles,values,relations,opendims):
 rows=[assertion('o'+str(j),'owner',owner=x,owner_kind='entity')for j,x in enumerate(owners)]+[assertion('r'+str(j),'role',owner=x,role=role)for j,(role,x)in enumerate(roles)]+[assertion('f'+str(j),'fact',d,owner=x,property=p,value_type=t,value=v)for j,(d,x,p,t,v)in enumerate(values)]+[assertion('rel'+str(j),kind,left=l,right=r)for j,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':TEXT}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
study=core(['P','T'],[('main_subject','P'),('primary_prop','T')],[('subject','P','entity.type','entity.type/v1','human'),('subject','T','props.type','props.type/v1','star_map_tablet'),('concept','T','representation.content','representation.content/v1','star_map')],[('disjoint','P','T')],['action','relationship'])
rail=core(['C','I','R'],[('recording_camera','C'),('image','I'),('primary_prop','R')],[('subject','C','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','R','props.type','props.type/v1','railing')],[],['camera','composition'])
person=core(['P'],[('main_subject','P')],[('subject','P','entity.type','entity.type/v1','human')],[],['appearance'])
parts=core(['U','F','H'],[],[('subject','U','entity.presence','entity.presence/v1','present'),('subject','F','entity.presence','entity.presence/v1','present'),('subject','H','entity.presence','entity.presence/v1','present'),('subject','U','entity.category','entity.category/v1','human'),('subject','F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','H','entity.type','entity.type/v1','hands_region'),('subject','H','anatomy.hands.presence','anatomy.hands.presence/v1','present')],[('part_of','F','U'),('part_of','H','U'),('disjoint','F','H')],['expression','character_response'])
scene=core(['Q'],[('scene','Q')],[('subject','Q','entity.presence','entity.presence/v1','present')],[],['setting'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def entry(o):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0],realization_id='base')
def choose(o,k,view='full',bindings=None):
 e=entry(o);k=copy.deepcopy(k)
 if o==1278 and bindings is not False:
  k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];selected=bindings or[('character','U'),('face','F'),('hands','H')]
  e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':x}for t,x in selected]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
configs=[(1275,study,'human',[('fact','P','entity.type'),('fact','T','props.type'),('fact','T','representation.content'),('disjoint','P','T')]),(1276,rail,'environment',[('fact','C','entity.type'),('fact','I','entity.presence'),('fact','R','props.type')]),(1277,person,'human',[('fact','P','entity.type')]),(1278,parts,'human',[('fact','U','entity.presence'),('fact','F','entity.presence'),('fact','H','entity.presence'),('fact','U','entity.category'),('fact','F','anatomy.face.presence'),('fact','H','entity.type'),('fact','H','anatomy.hands.presence'),('part_of','F','U'),('part_of','H','U'),('disjoint','F','H')]),(1279,scene,'environment',[('fact','Q','entity.presence')])]
results=[];views=[];extra=[]
for o,k,category,atoms in configs:
 e,k=choose(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for view in ['full','compact']:
  z,kk=choose(o,k,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,view,receipt);assert generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,view,'baseconsumer')
  checks.append({'case':'independent_precise_P_source_guards','view':view,'admission':receipt,'same_actual_ownbinding_consumer_allowed':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,bad,view)
   assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,'property',prop);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,view,'consumerproperty',prop)
   checks.append({'case':'every_actual_E_target_and_receiver_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_ownbinding_consumer_denied':True})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['open_dimensions'].remove(dim);bad['intent_lock']['locked_dimensions'].append(dim);z,kk=choose(o,bad,view);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,view,'whole',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_ownbinding_consumer_denied':True})
 for kind,x,p in atoms:
  a=next(a for a in k['semantic_assertions']if a['axes']['kind']==kind and((kind=='fact'and a['axes']['owner']==x and a['axes']['property']==p)or(kind!='fact'and a['axes']['left']==x and a['axes']['right']==p)))
  bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,kk=choose(o,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,view,'missingP',a,receipt);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z)
   checks.append({'case':'every_manually_identified_required_P_preservation_existing_origin_or_actualguard','view':view,'removed':a,'admission':receipt,'actual_ownbinding_consumer_denied':True})
 results.append({'ordinal':o,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'core':k,'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks})
 if o==1275:
  rec=S['candidates'][e['id']];guard=layout.guard_record(rec,S);spec=S['slot_catalog']['relational_action'];full=n.qualification(spec,rec,source_data=S);compact=n.qualification(spec,guard,source_data=S);assert full==compact and full['status']=='eligible'and full['matched_manual_role_views'];proposal=proposals.propose(S,'relational_action',e['id'],[]);assert proposal['semantic_fit']['status']=='eligible'
  for view in ['full','compact']:
   z,kk=choose(o,k,view);assert generator.core_entry_eligible(S,kk,contract(category),picked(category),'relational_action',z)
  assert ds==['action','relationship'];views.append({'ordinal':o,'role':'relational_action','fullcompact_qualification':full,'proposal':proposal,'actual_sameoldbinding_newrequestedrole_fullcompact_allowed':True,'canonical_E_dimensions_unchanged':ds,'canonical_E_properties':ps})
# Ownbinding conditions remain consumer obligations even when source evidence is semantically qualified.
for domain in ['documentary','craft','wildlife','product','jewelry','food']:
 for view in ['full','compact']:
  z,kk=choose(1277,person,view);assert not generator.core_entry_eligible(S,kk,contract('human',[domain]),picked('human'),z['_presentation_role'],z);extra.append({'ordinal':1277,'view':view,'case':'exact_ownbinding_deny_domain','domain':domain,'consumer_denied':True})
for o,k in [(1275,study),(1277,person),(1278,parts)]:
 for view in ['full','compact']:
  z,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('animal'),picked('animal'),z['_presentation_role'],z);extra.append({'ordinal':o,'view':view,'case':'source_human_not_waived_by_animal_display_or_genericrole','consumer_denied':True})
for view in ['full','compact']:
 z,kk=choose(1278,parts,view,False);receipt=n.admission(z,kk);assert not receipt['allowed'];extra.append({'ordinal':1278,'view':view,'case':'all_actual_owner_choices_missing','admission':receipt})
 bad=copy.deepcopy(parts);bad['semantic_assertions'].append(assertion('extra_person','owner',owner='V',owner_kind='entity'))
 for a in bad['semantic_assertions']:
  if a['axes']['kind']=='part_of'and a['axes']['left']=='H':a['axes']['right']='V'
 z,kk=choose(1278,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'];extra.append({'ordinal':1278,'view':view,'case':'hands_belong_to_different_actual_character','admission':receipt})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_role_view_checks':views,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Controlled independent fixture only. Every actual E+Rx property/whole dimension/exactP+preservation/source relation guard and selectedexistingpresence tested fullcompact.1275 studying manualview leaves actual unfamiliarity E intact.1278 samehuman-part ownership not bodyinheritance/ownermerge;1277 actualowndomain deny preserved. No source/Git/code/runtime/operating mutation.'}
p=O/'CHECKS-01275-01280-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
