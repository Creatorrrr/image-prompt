"""Actual fixed-runtime full/compact/consumer regressions on five newly authored research proofs."""
from boot import *
import prompt_generator as generator
J=json.loads((O/'BATCH-v1.json').read_text());COR=copy.deepcopy(S)
for row in J['records']:
 rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];COR['candidates'][row['candidate_id']]=rec
# These concrete fixture inventories were individually authored before candidate admission. No role word supplies anatomy, type or state.
VALUE_ROWS={
9629:[('subject','entity.presence','entity.presence/v1','present'),('subject','entity.type','entity.type/v1','human'),('subject','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','anatomy.nose.presence','anatomy.nose.presence/v1','present'),('subject','anatomy.skin.nose_bridge.presence','anatomy.skin.nose_bridge.presence/v1','present')],
9762:[('subject','entity.presence','entity.presence/v1','present'),('subject','entity.type','entity.type/v1','human'),('subject','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','anatomy.mouth.presence','anatomy.mouth.presence/v1','present'),('subject','anatomy.lips.presence','anatomy.lips.presence/v1','present'),('expression','mouth.state.seam','mouth.state/v1','closed')],
9834:[('subject','entity.presence','entity.presence/v1','present'),('subject','entity.type','entity.type/v1','human'),('subject','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','anatomy.mouth.presence','anatomy.mouth.presence/v1','present'),('subject','anatomy.mouth_corners.presence','anatomy.mouth_corners.presence/v1','present'),('subject','anatomy.cheeks.presence','anatomy.cheeks.presence/v1','present'),('subject','anatomy.eyes.presence','anatomy.eyes.presence/v1','present'),('appearance','eyes.structure.aperture_state','eyes.aperture/v1','partly_open')],
9853:[('subject','entity.presence','entity.presence/v1','present'),('subject','entity.type','entity.type/v1','human'),('subject','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','anatomy.eyes.presence','anatomy.eyes.presence/v1','present'),('subject','anatomy.upper_eyelids.presence','anatomy.upper_eyelids.presence/v1','present'),('subject','anatomy.lower_eyelids.presence','anatomy.lower_eyelids.presence/v1','present'),('subject','anatomy.irises.presence','anatomy.irises.presence/v1','present'),('appearance','eyes.structure.aperture_state','eyes.aperture/v1','partly_open')],
9868:[('subject','entity.presence','entity.presence/v1','present'),('subject','entity.type','entity.type/v1','human'),('subject','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','anatomy.mouth.presence','anatomy.mouth.presence/v1','present'),('subject','anatomy.lips.presence','anatomy.lips.presence/v1','present')]}
TEXTS={9629:'Independent synthetic request: existing selected human H has an existing face, nose and actual nose-bridge skin. Every stated atomic part is present on H. H is a part of existing whole B; F is an existing part of H; HA is exactly H. O is a distinct existing object with a face depiction and independently declared matching parts where its variant states so. Z is a separate human. Local expression is open; no actual request, emotion, age or candidate inference is involved.',9762:'Independent synthetic request: existing selected human H has an existing face, mouth and lips and its mouth seam is explicitly closed. Every stated atomic part is present on H. H is part of B; F part of H; HA exactly H. O is a distinct object with its own explicitly declared matching face parts and closed seam only in its variant; Z is a separate human. Local expression is open.',9834:'Independent synthetic request: existing selected human H has an existing face, mouth with mouth corners, cheeks and eyes. Every atomic part is present on H, and the same eyes have the exact partly_open aperture state. H is part of B; F part of H; HA exactly H. O is a distinct object with separately declared matching face parts and partly_open aperture only in its variant; Z is a separate human. Expression is open.',9853:'Independent synthetic request: existing selected human H has an existing face, eyes, upper eyelids, lower eyelids and irises. All those atomic parts are present on H, and the same eyes have the exact partly_open aperture state. H is part of B; F part of H; HA exactly H. O is a distinct object with separately declared matching face parts and partly_open aperture only in its variant; Z is a separate human. Expression is open.',9868:'Independent synthetic request: existing selected human H has an existing face, mouth and lips. All those atomic parts are present on H. H is part of B; F part of H; HA exactly H. O is a distinct object with separately declared matching facial parts only in its variant; Z is a separate human. Expression is open.'}
def core(o):
 text=TEXTS[o]
 def ar(i,kind,dimension='subject',**axes):return {'assertion_id':i,'dimension':dimension,'polarity':'required','source_span_ids':['independent_fixture'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':text}}
 rows=[ar('owner_'+owner,'owner',owner=owner,owner_kind='entity')for owner in ['H','HA','B','F','O','Z']]
 rows += [ar('alias','equivalent',left='H',right='HA'),ar('parent','part_of',left='H',right='B'),ar('child','part_of',left='F',right='H'),ar('otherObject','disjoint',left='H',right='O'),ar('otherHuman','disjoint',left='H',right='Z'),ar('objectHuman','disjoint',left='O',right='Z')]
 rows += [ar('f'+str(i),'fact',d,owner='H',property=p,value_type=t,value=val) for i,(d,p,t,val) in enumerate(VALUE_ROWS[o])]
 rows += [ar('objectType','fact',owner='O',property='entity.type',value_type='entity.type/v1',value='object'),ar('separateHumanType','fact',owner='Z',property='entity.type',value_type='entity.type/v1',value='human')]
 k={'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'independent_fixture','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':['expression'],'semantic_anchors':[]}}
 pin(k);return k

def pin(k):k['canonical_sha256']=c.digest({key:val for key,val in k.items()if key not in {'canonical_sha256','core_id'}})
def selection(row,k,owner):
 graph=n.frozen_witnesses(k)['graph'];guard=n.compact(COR['candidates'][row['candidate_id']],COR)
 return {'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':row['candidate_id'],'realization_id':'base','meaning_sha256':guard['meaning_sha256'],'qualification_sha256':guard['qualification_sha256'],'bindings':[{'target':'main_subject','owner_id':owner}]}]}
def entry(row,k,owner='H',binding=None,view='full'):
 z=c.entry(COR,row['candidate_id'],binding,realization_id='base',owner_selections=selection(row,k,owner))
 z.pop('_semantic_evidence_guard' if view=='full' else 'role_evidence',None)
 return z
contract={'subject_category':'human','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
checks=[];fixtures=[]
def check(label,got,want,**context):
 assert bool(got)==bool(want),(label,got,want,context)
 checks.append({'case':label,'expected':want,'actual':bool(got),**context})
for row in J['records']:
 o=row['ordinal'];cid=row['candidate_id'];r=COR['candidates'][cid];k=core(o);fixtures.append({'ordinal':o,'base_core':k})
 # Same source address and all Rx intact in full and compact; qualification never projects E dimensions for manual role views.
 for form in ['full','compact']:
  z=entry(row,k,view=form);a=n.admission(z,k);check('selected_human_admission',a['allowed'],True,ordinal=o,form=form,result=a)
  check('open_original_expression_property',n.property_scope_allowed(k,z['affected_dimensions'],z['affected_properties'],record=z),True,ordinal=o,form=form)
  dims,props,graph=n.permission_scope(z,k);assert dims==['expression'] and props==[{'dimension':'expression','target':'H','property':'face.expression'}]
  for tag in row['proof']['roles']:
   rec=r if form=='full' else {**r,'_semantic_evidence_guard':n.compact(r,COR)}
   if form=='compact':rec=copy.deepcopy(rec);rec['content'].pop('role_evidence')
   q=n.qualification(CAT[tag],rec,source_data=COR);check('actual_role_qualification',q['status']=='eligible',True,ordinal=o,form=form,slot=tag,result=q)
   check('actual_role_consumer',generator.core_entry_eligible(COR,k,contract,picked,tag,z),True,ordinal=o,form=form,slot=tag)
  # Every P and PR individually missing/wrong type/wrong owner must fail; these are controlled request variants, no source mutation.
  for d,prop,vt,value in VALUE_ROWS[o]:
   for defect in ['missing','wrong_value','different_owner','wrong_type_namespace']:
    bad=copy.deepcopy(k);matches=[f for f in bad['semantic_assertions'] if f['axes']['kind']=='fact' and f['axes'].get('owner')=='H' and f['axes'].get('property')==prop];assert len(matches)==1;f=matches[0]
    if defect=='missing':bad['semantic_assertions'].remove(f)
    elif defect=='wrong_value':f['axes']['value']='wrong_value'
    elif defect=='wrong_type_namespace':f['axes']['value_type']='different.namespace/v1'
    else:
     # O already has objectType. Relocate human type to F, which is a part, not equivalent to H.
     f['axes']['owner']='F' if prop=='entity.type' else 'O'
    pin(bad);zz=entry(row,bad,view=form);a=n.admission(zz,bad);check('PPR_'+defect,a['allowed'],False,ordinal=o,form=form,property=prop,result=a)
  # Alias H is allowed. All same-owner H, alias HA, ancestor B, child F property and whole expression locks deny consumer.
  za=entry(row,k,'HA',view=form);check('actual_alias_selected',n.admission(za,k)['allowed'],True,ordinal=o,form=form);check('alias_consumer',generator.core_entry_eligible(COR,k,contract,picked,'expression',za),True,ordinal=o,form=form)
  for owner in ['H','HA','B','F']:
   bad=copy.deepcopy(k);bad['intent_lock']['semantic_anchors']=[{'dimension':'expression','target':owner,'property':'face.expression'}];pin(bad);zz=entry(row,bad,view=form)
   check('original_target_alias_parent_child_property_lock',n.property_scope_allowed(bad,zz['affected_dimensions'],zz['affected_properties'],record=zz),False,ordinal=o,form=form,locked_owner=owner)
   for tag in row['proof']['roles']:check('all_role_locked_original_property_consumer',generator.core_entry_eligible(COR,bad,contract,picked,tag,zz),False,ordinal=o,form=form,slot=tag,locked_owner=owner)
  bad=copy.deepcopy(k);bad['intent_lock']['open_dimensions']=[];bad['intent_lock']['locked_dimensions'].append('expression');pin(bad);zz=entry(row,bad,view=form)
  for tag in row['proof']['roles']:check('whole_expression_lock_all_role_consumer',generator.core_entry_eligible(COR,bad,contract,picked,tag,zz),False,ordinal=o,form=form,slot=tag)
  # Select O with every other matching source-required part/state; Z remains explicitly human, global for_any human still satisfied.
  bad=copy.deepcopy(k)
  for f in list(bad['semantic_assertions']):
   if f['axes']['kind']=='fact' and f['axes'].get('owner')=='H' and f['axes'].get('property')!='entity.type':f['axes']['owner']='O'
  pin(bad);zz=entry(row,bad,'O',view=form);a=n.admission(zz,bad);check('selected_object_plus_separate_human',a['allowed'],False,ordinal=o,form=form,result=a)
  for tag in row['proof']['roles']:check('global_human_does_not_rescue_selected_object',generator.core_entry_eligible(COR,bad,contract,picked,tag,zz),False,ordinal=o,form=form,slot=tag,global_picked=['human'])
  # Actual original ownbindings remain unchanged and conjunctive; none are invented for new role views.
  bids=[bid for bid,b in COR['slot_bindings'].items()if b['candidate_id']==cid]
  for bid in bids:
   bz=entry(row,k,binding=bid,view=form);tag=COR['slot_bindings'][bid]['slot_id'];assert bz['_role_conditions']==COR['slot_bindings'][bid]['conditions'];check('ownbinding_admission',n.admission(bz,k)['allowed'],True,ordinal=o,form=form,binding=bid)
   check('ownbinding_consumer_human',generator.core_entry_eligible(COR,k,contract,picked,tag,bz),True,ordinal=o,form=form,binding=bid)
   cp=copy.deepcopy(picked);cp['subject']={'kind':['animal'],'tags':['animal']};check('source_human_AND_binding_human_OR_animal',generator.core_entry_eligible(COR,k,contract,cp,tag,bz),False,ordinal=o,form=form,binding=bid)
 # Structural adversaries mutate only disposable in-memory proof copies; never write forged native artifacts or qualify them.
 for defect in ['canonical_property_renamed','E_cloned','view_fact_hash_changed','view_role_changed','source_app_changed','requires_human_removed']:
  bad=copy.deepcopy(r);pf=bad['content']['role_evidence'];e=next(f for f in pf['facts']if f['mode']=='effect')
  if defect=='canonical_property_renamed':e['property']='face.local_geometry'
  elif defect=='E_cloned':pf['facts'].append({**copy.deepcopy(e),'id':'forged_copy'})
  elif defect=='view_fact_hash_changed':pf['manual_role_views'][0]['canonical_fact_refs'][0]['fact_sha256']='0'*64
  elif defect=='view_role_changed':pf['manual_role_views'][0]['role_id']='body_form'
  elif defect=='source_app_changed':bad['content']['application_contract']+=' Unsupported change.'
  else:e['requires'].remove('owner_human')
  try:n.validate(bad,CAT,corpus={**COR,'candidates':{**COR['candidates'],cid:bad}});rejected=False
  except (ValueError,KeyError,TypeError):rejected=True
  check('tampered_'+defect,rejected,True,ordinal=o)
verified=nr.verify_batch(str((D/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH-v1.json').relative_to(ROOT)),str((O/'NOTE-v1.json').relative_to(ROOT)),root=ROOT,here=R)
summary={k:value for k,value in verified.items()if k!='records'}
res={'schema':'photo-worker-five-expression-final-checks/v1','task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'batch_sha256':c.digest(J),'source26_sha256':c.digest(S),'fixed_generation':str(G),'modules':modules(),'checks':checks,'assertion_count':len(checks),'all_passed':True,'full_batch_verification':summary,'synthetic_independent_cores':fixtures,'scope':'Only controlled independently authored artificial requester cores against the five actual source26 proofs, full/compact and unchanged actual ownbindings. No actual requester, source application, root acceptance, rendering or operating approval is claimed.','root_acceptance':0,'operating_native':0,'provider_model_network_calls':0}
save(O/'CHECKS-v2.json',res);print(json.dumps({'checks':len(checks),'canonical':c.digest(res),'raw':hashlib.sha256((O/'CHECKS-v2.json').read_bytes()).hexdigest(),'batch_verify':summary},ensure_ascii=False))
