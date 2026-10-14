"""Actual selected-source seven-lighting proof tests in controlled independent fixture cores.
No model, retrieval index, generation, runtime activation or real requester claim.
"""
import sys,json,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert raw(Path(e.__file__))=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
P=R/'native-inputs/prepared/review06250-00000-00020-149-04';O=R/'native_batches/review06250-00000-00020-149-04';A=json.load(open(P/'ASSIGNMENT.json'));I=nr.artifact(ROOT,A['input']);S=nr.artifact(ROOT,I['current_snapshot']);B=json.load(open(O/'BATCH.json'))
verified=nr.verify_batch(str((P/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH.json').relative_to(ROOT)),str((O/'NOTE.json').relative_to(ROOT)));assert verified['statuses']=={'approved':20,'diagnostic_reviewed':0,'pending':0} and not verified['root_accepted']
ORDINALS=[0,1,2,6,7,11,12]

def fixture(n,*,defect=None,anchor=None,whole=None,alias=None,part=None):
 text=('This is an isolated caller-authored controlled fixture, not actual requester evidence. Existing source_A is an illumination source. Existing receiver_A and receiver_B are the complete existing receiving scope of that source, declared from all reviewed inputs before discovery. Each already receives illumination from source_A. All these existing owners are in scene_A. A separate unrelated other_source is present and is not the selected source. An unrelated other_receiver is also present and explicitly disjoint from the actual receivers. No desired selected source type, modifier, quality, day phase or phase treatment is frozen as a prerequisite.')
 if n==1:text+=' The same source_A is independently designated for laboratory use, not inferred from a laboratory room.'
 if n==12:text+=' Existing path_A is an illumination path with a window-mediated route from source_A; both actual receivers already receive via this same path_A. No window or path is added.'
 owners=['source_A','receiver_A','receiver_B','scene_A','other_source','other_receiver']+(['path_A'] if n==12 else [])
 if alias:owners.append(alias[0]);text+=' '+alias[0]+' is an explicitly equivalent alias of '+alias[1]+'.'
 if part:owners.append(part[0]);text+=' '+part[1]+' is explicitly a part of existing '+part[0]+'.'
 textsha=hashlib.sha256(text.encode()).hexdigest();inputs={'schema':e.witnesses.INPUT_SCHEMA,'complete':True,'items':[{'id':'request','kind':'request_text','sha256':textsha}]}
 binding={'request_sha256':textsha,'request_envelope_sha256':c.digest({'request_text':text,'input_inventory':inputs}),'active_spans':[{'span_id':'fixture','text':text,'start':0,'end':len(text)}],'input_inventory':inputs};rows=[]
 def stmt(aid,kind,dim='subject',**axes):rows.append({'assertion_id':aid,'dimension':dim,'polarity':'required','source_span_ids':['fixture'],'axes':{'native_schema':e.witnesses.SCHEMA,'kind':kind,**axes},'evidence':{'controlled_request':text},'affected_dimensions':[dim]})
 def fact(aid,owner,dim,prop,vt,value):stmt(aid,'fact',dim,owner=owner,property=prop,value_type=vt,value=value)
 for owner in owners:
  stmt('owner_'+owner,'owner',owner=owner,owner_kind='explicit_existing_owner')
  if not (alias and owner==alias[0]) and (owner!='receiver_B' or defect!='receiver_presence_missing'):fact('presence_'+owner,owner,'subject','entity.presence','entity.presence/v1','present')
 if defect!='source_kind_missing':fact('actual_source_kind','source_A','subject','entity.type','entity.type/v1','wrong_kind' if defect=='source_kind_wrong' else 'illumination_source')
 # Unrelated neutral main/light roles deliberately do not address selected source.
 stmt('neutral_main','role',role='main_subject',owner='other_source');stmt('neutral_light','role',role='light_source',owner='other_source')
 for owner in ['receiver_A','receiver_B']:
  if not (owner=='receiver_B' and defect=='last_relation_missing'):fact('received_from_'+owner,owner,'lighting','lighting.received_from','entity.owner_id/v1','other_source' if owner=='receiver_B' and defect=='last_relation_wrong' else 'source_A')
 for a,b in [('receiver_A','receiver_B'),('receiver_A','other_receiver'),('receiver_B','other_receiver'),('source_A','other_source')]:stmt('disjoint_'+a+'_'+b,'disjoint',left=a,right=b)
 if alias:stmt('locked_alias','equivalent',left=alias[0],right=alias[1])
 if part:stmt('actual_part','part_of',left=part[1],right=part[0])
 if n==1 and defect!='lab_designation_missing':fact('lab_designation','source_A','concept','context.application.laboratory_use','context.application.laboratory_use/v1','other_use' if defect=='lab_designation_wrong' else 'designated')
 if n==11:
  fact('actual_scene_kind','scene_A','subject','entity.type','entity.type/v1','scene')
  for owner in ['source_A','receiver_A','receiver_B']:
   if not (owner=='receiver_B' and defect=='scene_relation_missing'):fact('scene_of_'+owner,owner,'setting','setting.scene_owner','entity.owner_id/v1','other_source' if owner=='receiver_B' and defect=='scene_relation_wrong' else 'scene_A')
 if n==12:
  fact('actual_path_kind','path_A','subject','entity.type','entity.type/v1','illumination_path')
  if defect!='path_route_missing':fact('path_route','path_A','lighting','lighting.path.route','lighting.path.route/v1','other_route' if defect=='path_route_wrong' else 'window_mediated')
  fact('path_source','path_A','lighting','lighting.path.source','entity.owner_id/v1','other_source' if defect=='path_source_wrong' else 'source_A')
  for owner in ['receiver_A','receiver_B']:
   if not (owner=='receiver_B' and defect=='last_via_missing'):fact('via_'+owner,owner,'lighting','lighting.received_via','entity.owner_id/v1','other_source' if owner=='receiver_B' and defect=='last_via_wrong' else 'path_A')
 inventory={'schema':e.witnesses.MEMBER_SCOPE_SCHEMA,'complete':defect!='incomplete_scope','state':'unknown' if defect=='unknown_scope' else 'known_present','input_binding':e.witnesses.input_binding(binding),'reviewed_input_ids':['request'],'members':[{'owner_id':owner,'source_span_ids':['fixture'],'source_input_ids':['request']} for owner in ['receiver_A','receiver_B']]}
 stmt('complete_receiving_scope','existing_member_scope',scope_id='receiving_inventory',inventory=e.witnesses.canonical(inventory))
 # Frozen relation prerequisites use exact property anchors while lighting E remains open.
 anchors=[{'dimension':row['dimension'],'target':row['axes']['owner'],'property':row['axes']['property']} for row in rows if row['axes']['kind']=='fact' and row['dimension']=='lighting']
 if anchor:anchors.append({'dimension':anchor[0],'target':anchor[1],'property':anchor[2]})
 dims=['lighting']+(['timing'] if n==11 else []);locked=['subject','concept','setting'];opened=list(dims)
 if whole in opened:opened.remove(whole);locked.append(whole)
 core={'contract_version':'photo-authorial-core/v3','source_request':text,'subject':text,'baseline_prompt_en':text,'semantic_assertions':rows,'request_binding':binding,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':locked,'open_dimensions':opened,'semantic_anchors':anchors}}
 core['canonical_sha256']=c.digest(core);core['core_id']=core['canonical_sha256'][:16];return core

def choices(record,core,*,bad=None):
 frozen=e.frozen_witnesses(core);scope=next(row for row in frozen['member_scopes'] if row['scope_id']=='receiving_inventory');p=record['content']['role_evidence'];n=next(row['ordinal'] for row in B['records'] if row['candidate_id']==record['id']);bindings=[{'target':'illuminating_light','selection':{'kind':'existing_owner','owner_id':'source_A'}},{'target':'illuminated_receivers','selection':{'kind':'existing_member_scope','scope_id':'receiving_inventory','scope_sha256':c.digest(scope)}}]
 if n==11:bindings.append({'target':'scene','selection':{'kind':'existing_owner','owner_id':'scene_A'}})
 if n==12:bindings.append({'target':'illumination_path','selection':{'kind':'existing_owner','owner_id':'path_A'}})
 if bad=='missing_source':bindings=bindings[1:]
 elif bad=='wrong_source':bindings[0]['selection']['owner_id']='other_source'
 elif bad=='receiver_point_subset':bindings[1]['selection']={'kind':'existing_owner','owner_id':'receiver_A'}
 elif bad=='scope_hash':bindings[1]['selection']['scope_sha256']='0'*64
 result={'schema':e.MEMBER_SELECTION_SCHEMA,'core_sha256':core['canonical_sha256'],'owner_graph_sha256':c.digest(frozen['graph']),'member_scopes_sha256':c.digest(frozen['member_scopes']),'entries':[{'candidate_id':record['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':bindings}]};return result

contract={'subject_category':'object','adult_allowed':True,'intent_constraints':{'domains':[],'subject_categories':[]}};picked={'subject':{'en':'Independently declared existing objects','tags':['object']},'action':{},'location':{}}
results=[]
for n in ORDINALS:
 row=B['records'][n];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];data={**S,'candidates':{**S['candidates'],cid:rec}};e.validate(rec,S['slot_catalog'],corpus=data);own=[b for b in S['slot_bindings'].values() if b['candidate_id']==cid];assert len(own)==1 and own[0]['conditions']=={'subject_applicability':{}}
 matrix=[]
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}})]:
  for bid in [None,own[0]['id']]:
   core=fixture(n);mapping=choices(rec,core);entry=c.entry(view,cid,bid,realization_id='base',owner_selections=mapping);admission=e.admission(entry,core);assert admission['allowed'] and not admission.get('search_only'),(n,label,bid,admission)
   dims,props,graph=e.permission_scope(entry,core);expected_dims=['lighting']+(['timing'] if n==11 else []);assert dims==sorted(expected_dims)
   expected={}
   for f in row['proof']['facts']:
    if f['mode']=='effect':
     expected[(f['dimension'],f['property'])]={'source_A','receiver_A','receiver_B'} if f['dimension']=='lighting' else {'scene_A'}
   for key,owners in expected.items():assert {p['target'] for p in props if (p['dimension'],p['property'])==key}==owners,(n,key,props)
   for tag in row['proof']['roles']:
    q=e.qualification(S['slot_catalog'][tag],view['candidates'][cid],source_data=data);assert q['status']=='eligible',q
    assert g.core_entry_eligible(view,core,contract,picked,tag,entry),(n,label,bid,tag)
   rejected=[]
   defects=['source_kind_missing','source_kind_wrong','receiver_presence_missing','last_relation_missing','last_relation_wrong','incomplete_scope','unknown_scope']
   if n==1:defects+=['lab_designation_missing','lab_designation_wrong']
   if n==11:defects+=['scene_relation_missing','scene_relation_wrong']
   if n==12:defects+=['path_route_missing','path_route_wrong','path_source_wrong','last_via_missing','last_via_wrong']
   for defect in defects:
    badcore=fixture(n,defect=defect)
    try:badmapping=choices(rec,badcore);badentry=c.entry(view,cid,bid,realization_id='base',owner_selections=badmapping);allowed=e.admission(badentry,badcore)['allowed']
    except (ValueError,KeyError):allowed=False
    assert not allowed,(n,label,bid,defect);rejected.append(defect)
   for bad in ['missing_source','wrong_source','receiver_point_subset','scope_hash']:
    badentry=c.entry(view,cid,bid,realization_id='base',owner_selections=choices(rec,core,bad=bad));assert not e.admission(badentry,core)['allowed'],(n,bad);rejected.append(bad)
   unselected=c.entry(view,cid,bid,realization_id='base');assert not e.admission(unselected,core)['allowed'];probe=e.admission(unselected,core,allow_unselected=True);assert probe['allowed'] and probe.get('search_only'),probe
   lockcases=[]
   for (dim,prop),owners in expected.items():
    for owner in sorted(owners):
     for lockname,lockprop in [('exact',prop),('ancestor',prop.split('.')[0])]:
      locked=fixture(n,anchor=(dim,owner,lockprop));lockedentry=c.entry(view,cid,bid,realization_id='base',owner_selections=choices(rec,locked));ds,ps,gs=e.permission_scope(lockedentry,locked);assert not e.property_scope_allowed(locked,ds,ps,record=lockedentry),(n,owner,prop,lockname);assert not g.core_entry_eligible(view,locked,contract,picked,next(iter(row['proof']['roles'])),lockedentry);lockcases.append([dim,owner,prop,lockname])
     locked=fixture(n,anchor=(dim,'alias_locked',prop),alias=('alias_locked',owner));lockedentry=c.entry(view,cid,bid,realization_id='base',owner_selections=choices(rec,locked));ds,ps,gs=e.permission_scope(lockedentry,locked);assert not e.property_scope_allowed(locked,ds,ps,record=lockedentry),(n,owner,'alias');lockcases.append([dim,owner,prop,'alias'])
     locked=fixture(n,anchor=(dim,'whole_locked',prop),part=('whole_locked',owner));lockedentry=c.entry(view,cid,bid,realization_id='base',owner_selections=choices(rec,locked));ds,ps,gs=e.permission_scope(lockedentry,locked);assert not e.property_scope_allowed(locked,ds,ps,record=lockedentry),(n,owner,'part_owner');lockcases.append([dim,owner,prop,'ancestor_owner'])
   for dim in dims:
    locked=fixture(n,whole=dim);lockedentry=c.entry(view,cid,bid,realization_id='base',owner_selections=choices(rec,locked));assert not g.core_entry_eligible(view,locked,contract,picked,next(iter(row['proof']['roles'])),lockedentry),(n,dim,'whole')
   matrix.append({'view':label,'binding_id':bid,'admission':admission,'actual_permission_properties':props,'exact_all_receiver_scope':True,'actual_source_role_is_not_neutral_light_source':True,'rejected_missing_wrong_contracts':rejected,'original_property_all_actual_source_receiver_alias_ancestor_locks':lockcases,'whole_dimensions_rejected':dims,'unselected_final_rejected_search_only_probe':True,'own_binding':own[0]})
 results.append({'ordinal':n,'candidate_id':cid,'matrix':matrix})
mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'raw_sha256':raw(p)}
out={'schema':'photo-first20-lighting04-actual-source-diagnostic/v1','verification':{k:v for k,v in verified.items() if k!='records'},'actual_modules':mods,'results':results,'prepared_count':20,'fresh_complete_source_read_count':7,'unchanged_proof_byte_reuse_count':13,'new_proof_count':7,'root_accepted_count':0,'operating_adoption_count':0,'semantic_boundary':'These are caller-authored isolated exact-owner fixtures, not real requester evidence or saved pixels. Complete receiver membership is independently asserted before discovery and structurally pinned; code does not discover all real illuminated surfaces or semantically verify a dishonest completeness claim. No desired E value is supplied as P. All lighting source/Rx original canonical locks, receiver relations, old binding conditions and declared path/scene/lab qualifiers are tested. Shape/admission does not replace source entailment review or root acceptance.'};q=O/'DIAGNOSTIC-LIGHTING07.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS7',sum(len(x['matrix']) for x in results),'actual full/compact x oldbinding',raw(q))
