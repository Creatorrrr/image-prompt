"""Actual source25 soil3 full/compact native controls; independent synthetic core evidence."""
import copy,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';D=R/'native-inputs/prepared/review09250-soil3-149-01';O=R/'native_batches/review09250-soil3-149-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');forbidden=[]
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:forbidden.append(fullname);raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
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
A=read(D/'ASSIGNMENT.json');I=nr.artifact(ROOT,A['input']);S=nr.artifact(ROOT,I['current_snapshot']);B=read(O/'BATCH.json');assert H(S)=='5180d1fed3654e938ac5377ce87238ce6853bd61c944d02249b2d2ab8d6eeea1'
verified=nr.verify_batch(str((D/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH.json').relative_to(ROOT)),str((O/'NOTE.json').relative_to(ROOT)));assert verified['statuses']=={'approved':3,'pending':0,'diagnostic_reviewed':0} and not verified['root_accepted']
# These literal core requirements are independently authored fixture declarations, not copied source E values.
CORE_FACTS=[('presence','subject','entity.presence','entity.presence/v1','present'),('kind','subject','entity.type','entity.type/v1','soil_face'),('exposure','material','surface.exposure','surface.exposure/v1','exposed'),('soil','material','surface.material','surface.material/v1','soil')]
BROKEN=('broken','material','surface.state','surface.state/v1','broken')
def fixture(o,*,defect=None,anchor=None,whole=False,alias=False,part=False,disjoint=True,second_eligible=False):
 values=CORE_FACTS+([BROKEN] if o==11595 else []);declared=[]
 for aid,dim,prop,vt,val in values:
  if defect=='missing_'+aid:continue
  who='other_A' if defect=='other_owner_'+aid else 'surface_A'
  actual='wrong_declared_value' if defect=='wrong_'+aid else val
  declared.append((aid,who,dim,prop,vt,actual))
 if second_eligible:
  declared += [('second_'+aid,'surface_B',dim,prop,vt,val) for aid,dim,prop,vt,val in values]
 text='Independent controlled caller fixture, not a real user request. The caller declares surface_A to be an existing physical soil-face carrier and other_A a separately declared owner. No desired ped, pore, crumb organization or surface_structure value is a frozen prerequisite. No neutral primary/foreground owner role is assigned. The following typed factual declarations are independently frozen by this controlled caller: '+ ' ; '.join(who+' has '+dim+'/'+prop+' as '+vt+' value '+val for aid,who,dim,prop,vt,val in declared)+'.'
 if disjoint:text+=' surface_A and other_A are explicitly disjoint.'
 if alias:text+=' alias_A is explicitly the same owner as surface_A.'
 if part:text+=' surface_A is explicitly part of parent_A.'
 if second_eligible:text+=' surface_B is another independently present exposed soil face; it is explicitly disjoint from surface_A and other_A. Either is selected only by an explicit actual owner choice.'
 rows=[]
 def stmt(aid,kind,dim='subject',**axes):rows.append({'assertion_id':aid,'dimension':dim,'polarity':'required','source_span_ids':['controlled_request'],'axes':{'native_schema':n.witnesses.SCHEMA,'kind':kind,**axes},'evidence':{'controlled_request':text},'affected_dimensions':[dim]})
 stmt('owner_surface','owner',owner='surface_A',owner_kind='soil_face');stmt('owner_other','owner',owner='other_A',owner_kind='other_physical_surface')
 if disjoint:stmt('separate_owners','disjoint',left='surface_A',right='other_A')
 if alias:stmt('owner_alias','owner',owner='alias_A',owner_kind='explicit_alias');stmt('same_alias','equivalent',left='alias_A',right='surface_A')
 if part:stmt('owner_parent','owner',owner='parent_A',owner_kind='whole_ground');stmt('owned_part','part_of',left='surface_A',right='parent_A')
 if second_eligible:
  stmt('owner_second','owner',owner='surface_B',owner_kind='soil_face');stmt('second_disjoint','disjoint',left='surface_B',right='surface_A');stmt('second_other_disjoint','disjoint',left='surface_B',right='other_A')
 anchors=[]
 for aid,who,dim,prop,vt,val in declared:
  stmt('actual_'+aid,'fact',dim,owner=who,property=prop,value_type=vt,value=val)
  if dim=='material':anchors.append({'dimension':dim,'target':who,'property':prop})
 if anchor:anchors.append({'dimension':anchor[0],'target':anchor[1],'property':anchor[2]})
 core={'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'controlled_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject']+(['material'] if whole else []),'open_dimensions':[] if whole else ['material'],'semantic_anchors':anchors}}
 core['canonical_sha256']=H(core);core['core_id']=core['canonical_sha256'][:16];return core

def selections(rec,core,owner='surface_A'):
 p=rec['content']['role_evidence'];return {'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':core['canonical_sha256'],'owner_graph_sha256':H(n.frozen_witnesses(core)['graph']),'entries':[{'candidate_id':rec['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':H(p),'bindings':[{'target':'selected_surface','owner_id':owner}]}]}
def contract(category='environment',domain=None):return {'subject_category':category,'adult_allowed':False,'intent_constraints':{'domains':domain or [],'subject_categories':[]}}
def picked():return {'subject':{'en':'Independently declared exposed soil face in controlled environment','tags':['environment']},'action':{},'location':{}}
def entry_for(view,rec,core,bid=None,owner='surface_A',choice=True):return c.entry(view,rec['id'],bid,realization_id='base',**({'owner_selections':selections(rec,core,owner)} if choice else {}))
results=[];checks=0;allcores=[]
def check(condition,label,*details):
 global checks
 checks+=1
 if not condition:raise AssertionError((label,*details))
for row in B['records']:
 o=row['ordinal'];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=copy.deepcopy(row['proof']);data={**S,'candidates':{**S['candidates'],cid:rec}};n.validate(rec,S['slot_catalog'],corpus=data)
 own=[v for v in S['slot_bindings'].values() if v['candidate_id']==cid];check(len(own)==1 and own[0]['slot_id']=='texture' and own[0]['conditions']=={'subject_applicability':{}},'own binding exact',o);matrix=[];positive=fixture(o);allcores.append({'ordinal':o,'core':positive})
 check(not any(z.get('axes',{}).get('property')=='surface_structure' for z in positive['semantic_assertions']),'desired E absent from core',o)
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}})]:
  for bid in [None,own[0]['id']]:
   core=fixture(o);entry=entry_for(view,rec,core,bid);ad=n.admission(entry,core);check(ad['allowed'] and not ad.get('search_only'),'baseline admission',o,label,bid,ad)
   check(len(ad['resolved_frozen_facts'])==(5 if o==11595 else 4),'all PPR resolved',o,ad)
   check({v['owner'] for v in ad['resolved_frozen_facts']}=={'surface_A'},'all PPR actual same owner',o,ad)
   dims,props,graph=n.permission_scope(entry,core);check(dims==['material'] and props==[{'dimension':'material','target':'surface_A','property':'surface_structure'}],'original exact E scope',o,label,bid,dims,props)
   check(n.property_scope_allowed(core,dims,props,record=entry),'positive material identity preserved while texture open',o)
   for role in ['texture','surface_material']:
    q=n.qualification(S['slot_catalog'][role],view['candidates'][cid],source_data=data);check(q['status']=='eligible' and q['native_qualification']=='qualified','role fullcompact source fit',o,label,role,q)
    check(g.core_entry_eligible(view,core,contract(),picked(),role,entry),'actual per-role consumer',o,label,bid,role)
   # No owner inference even with only one qualifying actual soil face.
   nochoice=entry_for(view,rec,core,bid,choice=False);check(not n.admission(nochoice,core)['allowed'],'missing explicit selection denied',o)
   probe=n.admission(nochoice,core,allow_unselected=True);check(probe.get('search_only') is True,'missing choice search-only',o,probe)
   check(not g.core_entry_eligible(view,core,contract(),picked(),'texture',nochoice),'consumer rejects missing selection',o)
   failures=[]
   for field in ['presence','kind','exposure','soil']+(['broken'] if o==11595 else []):
    for kind in ['missing','wrong','other_owner']:
     defect=kind+'_'+field;badcore=fixture(o,defect=defect);bad=entry_for(view,rec,badcore,bid);receipt=n.admission(bad,badcore);check(not receipt['allowed'],'bad exact sameowner typed requirement',o,label,bid,defect,receipt)
     for role in ['texture','surface_material']:check(not g.core_entry_eligible(view,badcore,contract(),picked(),role,bad),'consumer PPR rejection',o,defect,role)
     failures.append({'defect':defect,'allowed':False,'reason':receipt['reason']})
   badowner=entry_for(view,rec,core,bid,owner='other_A');check(not n.admission(badowner,core)['allowed'],'selected unqualified owner denied',o)
   stale=selections(rec,core);stale['core_sha256']='0'*64;bad=c.entry(view,cid,bid,realization_id='base',owner_selections=stale);check(not n.admission(bad,core)['allowed'],'stale selection denied',o)
   locks=[]
   # surface_structure is one atomic segment: no proper dotted ancestor exists.
   # * and surface* exercise actual owner-wide and bounded-prefix uncertainty guards.
   lock_cases=[('original_property','surface_A','surface_structure',False,False,True,'material'),('other_dimension_same_property','surface_A','surface_structure',False,False,True,'appearance'),('owner_wide_ancestor_wildcard','surface_A','*',False,False,True,'material'),('bounded_surface_prefix_wildcard','surface_A','surface*',False,False,True,'material'),('explicit_alias','alias_A','surface_structure',True,False,True,'material'),('explicit_parent_scope','parent_A','surface_structure',False,True,True,'material'),('unknown_other_owner_overlap','other_A','surface_structure',False,False,False,'material')]
   for name,who,prop,alias,part,disjoint,dim in lock_cases:
    locked=fixture(o,anchor=(dim,who,prop),alias=alias,part=part,disjoint=disjoint);le=entry_for(view,rec,locked,bid);ld,lp,_=n.permission_scope(le,locked);check(not n.property_scope_allowed(locked,ld,lp,record=le),'actual source property lock',o,name)
    for role in ['texture','surface_material']:check(not g.core_entry_eligible(view,locked,contract(),picked(),role,le),'consumer lock',o,name,role)
    locks.append({'case':name,'target':who,'property':prop,'allowed':False})
   whole=fixture(o,whole=True);we=entry_for(view,rec,whole,bid)
   for role in ['texture','surface_material']:check(not g.core_entry_eligible(view,whole,contract(),picked(),role,we),'whole material dimension lock',o,role)
   for name,core,owner in [('explicit_disjoint_same_property',fixture(o,anchor=('material','other_A','surface_structure')),'surface_A'),('same_owner_unrelated_property',fixture(o,anchor=('material','surface_A','unrelated.sibling')),'surface_A'),('explicit_alias_selection',fixture(o,alias=True),'alias_A'),('second_independent_existing_soil_face',fixture(o,second_eligible=True),'surface_B')]:
    ce=entry_for(view,rec,core,bid,owner=owner);receipt=n.admission(ce,core);check(receipt['allowed'],'positive distinct/alias existing owner control',o,name,receipt)
    for role in ['texture','surface_material']:check(g.core_entry_eligible(view,core,contract(),picked(),role,ce),'positive control consumer',o,name,role)
   # Literal soil preservation remains a required fact and same-property lock.
   for property in ['surface.material','surface.exposure']:
    check(not n.property_scope_allowed(positive,['material'],[{'dimension':'material','target':'surface_A','property':property}]),'preserved original property raw mutation denied',o,property)
   matrix.append({'view':label,'binding_id':bid,'positive_admission':ad,'resolved_effects':props,'per_role_consumer_pass':['texture','surface_material'],'PPR_defects':failures,'lock_controls':locks,'whole_material_denied':True,'disjoint_unrelated_alias_secondowner_controls_allowed':True})
 # Exact existing own-binding guard layer AND is tested by an isolated stricter binding fixture.
 guarded=copy.deepcopy(data);guarded['slot_bindings'][own[0]['id']]['conditions']={'subject_applicability':{'deny_domains':['science_inspection']}};cc=fixture(o);ge=entry_for(guarded,rec,cc,own[0]['id']);check(n.admission(ge,cc)['allowed'],'stricter binding does not replace native PPR',o)
 for role in ['texture','surface_material']:check(not g.core_entry_eligible(guarded,cc,contract(domain=['science_inspection']),picked(),role,ge),'old binding guard AND consumer',o,role)
 rejected=[]
 for defect in ['missing_App','missing_KO','missing_relation_endpoint','reference_only_App','metadata_fact','E_as_P','canonical_property_rename','unsigned_stronger_value']:
  bad=copy.deepcopy(rec);p=bad['content']['role_evidence'];ef=next(f for f in p['facts'] if f['mode']=='effect')
  if defect=='missing_App':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/application_contract']
  elif defect=='missing_KO':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/ko']
  elif defect=='missing_relation_endpoint':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/relations/0/object']
  elif defect=='reference_only_App':p['source_units']=[u for u in p['source_units'] if not (u['pointer']=='/content/application_contract' and u['disposition']=='semantic')]
  elif defect=='metadata_fact':ef.update(pointer='/content/concept_terms/0',quote=bad['content']['concept_terms'][0])
  elif defect=='E_as_P':ef['mode']='prerequisite';ef.pop('operation');ef.pop('receivers')
  elif defect=='canonical_property_rename':ef['property']='surface.texture'
  else:ef['value']['value']='unsigned_stronger_value'
  if defect!='unsigned_stronger_value':p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
  try:n.validate(bad,S['slot_catalog'],corpus={**data,'candidates':{**data['candidates'],cid:bad}})
  except ValueError as err:rejected.append({'case':defect,'error':str(err)});checks+=1
  else:raise AssertionError((o,defect,'invalid proof accepted'))
 results.append({'ordinal':o,'candidate_id':cid,'original_ownbinding':own[0],'full_compact_binding_cases':matrix,'stricter_binding_isolated_guard_AND_control':True,'invalid_proofs_rejected':rejected})
modules={}
for name,m in sorted(sys.modules.items()):
 if (name.startswith('photo_') or name=='prompt_generator') and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();check(p.is_relative_to(G),'fixed module path',name,str(p));modules[name]={'file':str(p),'raw_sha256':raw(p)}
check(not forbidden,'no provider/local model imports',forbidden)
def save(name,obj):
 p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');print(name,raw(p),H(obj));return {'file':str(p.relative_to(ROOT)),'file_sha256':raw(p),'sha256':H(obj)}
cores=save('CONTROLLED-CORES-v1.json',{'schema':'photo-soil3-independent-controlled-cores/v1','source':'Independent manually declared controlled caller facts only; not a real requester or candidate-derived E baseline.','cores':allcores})
out={'schema':'photo-soil3-source25-actual-controls/v1','task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'source_sha256':H(S),'catalog_sha256':H(S['slot_catalog']),'batch_raw_sha256':raw(O/'BATCH.json'),'batch_sha256':H(B),'actual_assertions':checks,'full_compact_ownbinding_baselines':12,'per_role_consumer_baselines':24,'generation':str(G),'actual_modules':modules,'controlled_cores':cores,'results':results,'root_acceptance':0,'production_changes':0,'network_calls':0,'model_calls':0,'Gemini_calls':0,'forbidden_import_attempts':forbidden,'atomic_property_ancestor_boundary':'Original surface_structure is single-segment; no proper dotted ancestor exists. Actual exact, owner-wide wildcard, bounded surface* uncertainty, alias, parent-owner/part hierarchy, cross-dimension same property and whole dimension locks tested without renaming property.','boundary':'Full/compact source qualification, explicit existing-owner admission and prompt_generator per-role consumer eligibility are actual fixed-module executions on exact source25 records and their exact original own bindings. Controlled core declarations are independent synthetic fixtures, not real request truth, provider execution, pixels, complete multiple-candidate union/final prompt or root acceptance. Direct raw preserved-property lock checks are not a second qualified candidate. Isolated stricter binding copies test AND layering and do not edit original source/bindings.'}
checksref=save('ACTUAL-CHECKS-v1.json',out);save('COMPLETION-v1.json',{'schema':'photo-soil3-native-completion/v1','task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'source_sha256':H(S),'catalog_sha256':H(S['slot_catalog']),'batch_sha256':H(B),'actual_checks':checksref,'worker_native_source_statuses':{'approved':3,'pending':0},'root_accepted':False,'operating_qualified':0,'fresh_native_proofs':3,'reused_native_proofs':0,'actual_assertions':checks,'full_compact_ownbinding_baselines':12,'per_role_consumer_baselines':24,'new_unique_bulk_count':0,'bulk_next_ordinal':11600,'source_outside_assigned3_edited':0,'prior_artifacts_unchanged':True});print('PASS soil3 controls',checks)
