"""Actual full/compact source-native controls for the five individually authored proofs."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';D=R/'native-inputs/prepared/review05250-simple5-149-01';O=R/'native_batches/review05250-simple5-149-01'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as n
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
def H(x):return c.digest(x)
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
assert raw(n.__file__)=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
A=read(D/'ASSIGNMENT.json');I=nr.artifact(ROOT,A['input']);S=nr.artifact(ROOT,I['current_snapshot']);B=read(O/'BATCH.json')
assert H(S)=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
verified=nr.verify_batch(str((D/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH.json').relative_to(ROOT)),str((O/'NOTE.json').relative_to(ROOT)))
assert verified['statuses']=={'approved':5,'pending':0,'diagnostic_reviewed':0} and not verified['root_accepted']
TAGS={6131:'game_liveops_card_adjudication_scene',6162:'mecha_kaiju_mecha_sortie_scene',6191:'xianxia_sect_secret_realm_scene',6214:'character_affection_distance_spectrum_scene_atomic_scene'}
EXPECTED={6131:[('setting','setting.location')],6162:[('setting','setting.location')],6191:[('setting','setting.location')],6214:[('setting','setting.location'),('timing','timing.event_phase'),('atmosphere','mood.quiet')],6220:[('style','image.detail')]}
def fixture(o,*,defect=None,anchor=None,whole=None,alias=False,part=False):
 image=o==6220;owner='image_A' if image else 'scene_A';role='image' if image else 'scene';kind='image' if image else 'scene'
 text=('This is an independently authored controlled request fixture, not a real user request. The caller declares existing '+owner+' to be the '+kind+' context, independently maps the '+role+' address to it, and independently declares its presence and type. The unrelated owner other_A is explicitly disjoint. No desired location, closing phase, quiet atmosphere or clean-edge effect is already required.')
 if o in [6131,6162,6191]:text+=' The caller explicitly selected the cjk_narrative_world request domain and the independently specified primary story context for this controlled case.'
 if o==6214:text+=' The caller explicitly selected the character_scene_grammar request domain and independently specified the primary affection-distance scene context.'
 if image:text+=' On this same existing whole image, object contours are independently continuous and small surface details independently readable. Preserve both actual image properties, without creating or changing physical objects.'
 if alias:text+=' alias_A is explicitly the same owner as '+owner+'.'
 if part:text+=' '+owner+' is explicitly a part of existing parent_A; the protected parent property covers that actual child scope.'
 spans=[{'source_span_id':'controlled_request','text':text}];rows=[]
 def stmt(aid,kind,dim='subject',**axes):rows.append({'assertion_id':aid,'dimension':dim,'polarity':'required','source_span_ids':['controlled_request'],'axes':{'native_schema':n.witnesses.SCHEMA,'kind':kind,**axes},'evidence':{'controlled_request':text},'affected_dimensions':[dim]})
 def fact(aid,who,dim,prop,vt,value):stmt(aid,'fact',dim,owner=who,property=prop,value_type=vt,value=value)
 stmt('owner_actual','owner',owner=owner,owner_kind=kind);stmt('owner_other','owner',owner='other_A',owner_kind='unrelated')
 stmt('actual_disjoint','disjoint',left=owner,right='other_A')
 if defect!='missing_role':stmt('actual_role','role',role=role,owner=owner)
 if defect!='missing_presence':fact('actual_presence',owner,'subject','entity.presence','entity.presence/v1','absent' if defect=='wrong_presence' else 'present')
 if defect!='missing_kind':fact('actual_kind',owner,'subject','entity.type','entity.type/v1','unrelated_kind' if defect=='wrong_kind' else kind)
 if alias:stmt('alias_owner','owner',owner='alias_A',owner_kind='alias');stmt('alias_equivalent','equivalent',left='alias_A',right=owner)
 if part:stmt('parent_owner','owner',owner='parent_A',owner_kind='whole');stmt('actual_part','part_of',left=owner,right='parent_A')
 anchors=[]
 if image:
  for aid,prop,vt,val in [('contours','image.contour.continuity','image.contour.continuity/v1','continuous'),('details','image.small_surface_detail.readability','image.small_surface_detail.readability/v1','readable')]:
   if defect==f'missing_{aid}':continue
   who='other_A' if defect==f'other_owner_{aid}' else owner
   fact('actual_'+aid,who,'style',prop,vt,'wrong_value' if defect==f'wrong_{aid}' else val)
   anchors.append({'dimension':'style','target':who,'property':prop})
 dims=sorted({d for d,p in EXPECTED[o]});locked=['subject'];opened=dims[:]
 if whole:opened.remove(whole);locked.append(whole)
 if anchor:anchors.append({'dimension':anchor[0],'target':anchor[1],'property':anchor[2]})
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':spans},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':locked,'open_dimensions':opened,'semantic_anchors':anchors}}
def contract_for(o,missing_domain=False):return {'subject_category':'object','adult_allowed':True,'intent_constraints':{'domains':[] if missing_domain else (['cjk_narrative_world'] if o in [6131,6162,6191] else ['character_scene_grammar'] if o==6214 else []),'subject_categories':[]}}
def picked(o,missing=False):return {'subject':{'en':'An independently specified primary context in this controlled fixture','tags':[] if missing else ([TAGS[o]] if o in TAGS else ['object'])},'action':{},'location':{}}
results=[];check_count=0
for row in B['records']:
 o=row['ordinal'];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];data={**S,'candidates':{**S['candidates'],cid:rec}}
 n.validate(rec,S['slot_catalog'],corpus=data);own=[x for x in S['slot_bindings'].values() if x['candidate_id']==cid];assert len(own)==1
 assert own[0]['conditions']=={'subject_applicability':{}}
 actual='image_A' if o==6220 else 'scene_A';matrix=[]
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}})]:
  for bid in [None,own[0]['id']]:
   entry=c.entry(view,cid,bid,realization_id='base');core=fixture(o);admission=n.admission(entry,core)
   assert admission['allowed'] and not admission.get('search_only'),(o,label,bid,admission);check_count+=1
   assert len(admission['resolved_frozen_facts'])==(4 if o==6220 else 2)
   assert all(r['core_assertion_id'] for r in admission['resolved_frozen_facts'])
   for tag in row['proof']['roles']:
    q=n.qualification(S['slot_catalog'][tag],view['candidates'][cid],source_data=data)
    assert q['status']=='eligible' and q['native_qualification']=='qualified',(o,tag,q)
    assert g.core_entry_eligible(view,core,contract_for(o),picked(o),tag,entry),(o,label,bid,tag)
    check_count+=2
   dims,props,graph=n.permission_scope(entry,core)
   assert {(p['dimension'],p['property'],p['target']) for p in props}=={(d,p,actual) for d,p in EXPECTED[o]},(o,props)
   assert set(dims)=={d for d,p in EXPECTED[o]};check_count+=1
   badcases=[]
   defects=['missing_role','missing_presence','wrong_presence','missing_kind','wrong_kind']+(['missing_contours','wrong_contours','other_owner_contours','missing_details','wrong_details','other_owner_details'] if o==6220 else [])
   for defect in defects:
    receipt=n.admission(entry,fixture(o,defect=defect));assert not receipt['allowed'],(o,defect,receipt);check_count+=1;badcases.append({'defect':defect,'receipt':receipt})
   if o in TAGS:
    assert not g.core_entry_eligible(view,core,contract_for(o),picked(o,missing=True),next(iter(row['proof']['roles'])),entry),(o,'intrinsic tag gate bypass');check_count+=1
    assert not g.core_entry_eligible(view,core,contract_for(o,missing_domain=True),picked(o),next(iter(row['proof']['roles'])),entry),(o,'domain gate bypass');check_count+=1
   lockcases=[]
   for dim,prop in EXPECTED[o]:
    for name,owner,lockprop,alias,part in [('exact_original',actual,prop,False,False),('ancestor_property',actual,prop.split('.')[0],False,False),('actual_alias','alias_A',prop,True,False),('actual_parent','parent_A',prop,False,True)]:
     locked=fixture(o,anchor=(dim,owner,lockprop),alias=alias,part=part)
     assert not n.property_scope_allowed(locked,dims,props,record=entry),(o,name)
     assert not g.core_entry_eligible(view,locked,contract_for(o),picked(o),next(iter(row['proof']['roles'])),entry),(o,name,'consumer');check_count+=2
     lockcases.append([dim,prop,name])
    locked=fixture(o,whole=dim);assert not g.core_entry_eligible(view,locked,contract_for(o),picked(o),next(iter(row['proof']['roles'])),entry),(o,dim,'whole');check_count+=1
    other=fixture(o,anchor=(dim,'other_A',prop));assert n.property_scope_allowed(other,dims,props,record=entry),(o,'unrelated disjoint');check_count+=1
   sibling=fixture(o,anchor=(EXPECTED[o][0][0],actual,'unrelated.sibling_property'));assert n.property_scope_allowed(sibling,dims,props,record=entry);check_count+=1
   matrix.append({'view':label,'binding_id':bid,'positive_admission':admission,'actual_effects':props,'actual_dimensions':dims,'missing_wrong_owner_type_PR':badcases,'original_property_alias_ancestor_whole_controls':lockcases,'intrinsic_primary_tag_missing_rejected':o in TAGS,'explicitly_disjoint_same_property_control_allowed':True})
 # Source-proof coverage and mutation controls run on the same actual full source.
 rejected=[]
 for defect in ['missing_App','missing_KO','reference_only_App','metadata_fact','E_as_P','canonical_property_rename','unsigned_stronger_value']:
  bad=copy.deepcopy(rec);p=bad['content']['role_evidence'];ef=next(f for f in p['facts'] if f['mode']=='effect')
  if defect=='missing_App':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/application_contract']
  elif defect=='missing_KO':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/ko']
  elif defect=='reference_only_App':
   p['source_units']=[u for u in p['source_units'] if not (u['pointer']=='/content/application_contract' and u['disposition']=='semantic')]
  elif defect=='metadata_fact':ef.update(pointer='/content/aliases/0',quote=bad['content']['aliases'][0])
  elif defect=='E_as_P':ef['mode']='prerequisite';ef.pop('operation');ef.pop('receivers')
  elif defect=='canonical_property_rename':ef['property']='role_prefix.renamed_property'
  else:ef['value']['value']='unsigned_stronger_unasserted_value'
  if defect!='unsigned_stronger_value':p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
  try:n.validate(bad,S['slot_catalog'],corpus={**data,'candidates':{**data['candidates'],cid:bad}})
  except ValueError as error:rejected.append({'defect':defect,'error':str(error)});check_count+=1
  else:raise AssertionError((o,defect,'invalid proof accepted'))
 results.append({'ordinal':o,'candidate_id':cid,'own_binding_whole':own[0],'matrix':matrix,'invalid_proof_controls_rejected':rejected})

# Exact6220 PR still conflicts with a selected mutation of the preserved property.
# This is an explicitly controlled second source effect, not a new corpus proof.
row=next(r for r in B['records'] if r['ordinal']==6220);cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];data={**S,'candidates':{**S['candidates'],cid:rec}};entry=c.entry(data,cid,realization_id='base')
pr_union_controls=[]
for prop in ['image.contour.continuity','image.small_surface_detail.readability']:
 locked=fixture(6220);dims=['style'];effects=[{'dimension':'style','target':'image_A','property':prop}]
 assert not n.property_scope_allowed(locked,dims,effects)
 pr_union_controls.append({'property':prop,'changed_preservation_property_rejected_by_actual_frozen_lock':True});check_count+=1

modules={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);modules[name]={'file':str(p),'raw_sha256':raw(p)}
out={'schema':'photo-source96-simple5-actual-fullcompact-checks/v1','task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','source_sha256':H(S),'catalog_sha256':H(S['slot_catalog']),'batch_raw_sha256':raw(O/'BATCH.json'),'batch_sha256':H(B),'generation':str(G),'actual_modules':modules,'verification':{k:v for k,v in verified.items() if k!='records'},'actual_check_assertions':check_count,'full_compact_binding_baselines':sum(len(r['matrix']) for r in results),'results':results,'PR_property_mutation_controls':pr_union_controls,
 'harness_history':['The proof authoring first in-memory validation rejected App ordinary units borrowing EN/concept-unit facts across fields. Before any BATCH existed,6220 App was explicitly split into ordinary local P/context anchors and a one-hop selected_output_constraint reference to the actual EN/concept PR anchors. No frozen proof was edited or silently resigned.','First controlled consumer baseline omitted the independently required request domain and correctly failed. The fixture now explicitly declares its cjk_narrative_world/character_scene_grammar domain and tests missing domain as a rejection; no source guard was waived.','The final direct raw-triple PR lock control initially passed a qualified source record, whose wrapper correctly replaced the supplied triples with its own actual source E. The raw-triple control now omits record, exercising only the documented raw actual-triple permission path. This is explicitly not another qualified candidate or a complete multi-candidate union test.'],
 'boundary':'These are manually authored controlled synthetic existing scene/image fixtures, not actual user requests or visible image evidence. Every baseline P/type and6220 continuous/readable PR is independently supplied in controlled source text/core. Desired E values are never supplied as prerequisite values. Actual full/compact admission and consumer eligibility/permission/primary-tag/owner/property/alias/ancestor/whole locks run against the exact selected source; this does not semantically certify an actual unknown inventory or output pixels. The final2 PR checks are direct actual property-permission checks, not a complete multi-candidate union/admission test.',
 'root_acceptance':0,'operating_adoption':0,'model_calls':0,'network_calls':0,'Git':0}
path=O/'ACTUAL-CHECKS-v1.json';assert not path.exists();path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
note={'schema':'photo-source96-simple5-completion-note/v1','task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','batch_sha256':H(B),'actual_checks':{'file':str(path.relative_to(ROOT)),'file_sha256':raw(path),'sha256':H(out)},'native_source_approved_by_worker':5,'pending':0,'fresh_native_proofs':5,'actual_check_assertions':check_count,'actual_full_compact_binding_baselines':20,'root_accepted':False,'operating_qualified':0,'new_unique_bulk_count':0,'source_proposal_and_all_prior_batches_unchanged':True}
p=O/'COMPLETION-v1.json';assert not p.exists();p.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
for p in [path,p]:print(json.dumps({'file':str(p.relative_to(ROOT)),'raw_sha256':raw(p),'canonical_sha256':H(read(p))},ensure_ascii=False))
print('PASS5 actual checks',check_count)
