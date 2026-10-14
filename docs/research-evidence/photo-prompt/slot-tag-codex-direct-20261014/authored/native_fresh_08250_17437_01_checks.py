"""Candidate-independent literal requests; actual fresh v4 proof adversaries."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_17437_01.py')))
R=M['R'];FROZEN=M['FROZEN'];s=M['s'];c=M['c'];rr=M['rr'];nr=M['nr'];CID=M['cid'];P=M['P'];O=M['O'];CAT=M['CAT'];PROOF=M['PROOF'];CHOICES=M['CHOICES']
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
import photo_search_layout as layout
import audit_composed_prompt as audit
import prompt_generator as g
def assertion(id,dim,axes,evidence):return {'assertion_id':id,'dimension':dim,'polarity':'required','source_span_ids':['request'],'axes':{'native_schema':'photo-frozen-semantics/v1',**axes},'evidence':{'literal':evidence},'affected_dimensions':[dim]}
def owner(id,kind,evidence):return assertion(id+'_owner','subject',{'kind':'owner','owner':id,'owner_kind':kind},evidence)
def role(id,kind,evidence):return assertion(id+'_'+kind,'subject',{'kind':'role','role':kind,'owner':id},evidence)
def frozen(id,dim,own,prop,typ,value,evidence):return assertion(id,dim,{'kind':'fact','owner':own,'property':prop,'value_type':typ,'value':value},evidence)
def anchor(id,dim,own,prop,evidence):return {'anchor_id':id,'dimension':dim,'target':own,'property':prop,'source_text':evidence,'prompt_evidence':evidence}
REQUEST='Photograph Iri, an explicitly adult person with unmistakably adult body and face presentation. Iri is already declared a peer and peer rival as a scene role; no counterpart is specified. Iri has an existing face that belongs to Iri. Preserve the declared adult status and the unmistakably adult body and face presentation. Leave visible youthful-adult age presentation, styling, facial expression, eyelid opening and whole-body bearing open. Do not infer biological or numeric age or child or teen morphology.'
HELP_REQUEST='Jan is an already established helper, distinct from Iri. Jan may visibly help Iri, with help activity left open.'
RECOVERY_REQUEST='A prior brief disruption is already declared as story context for Iri. A recovery attempt at the selected instant is open; the past disruption need not be visible now.'
def core_for(help_selected=False,recovery_selected=False):
 text=REQUEST+(' '+HELP_REQUEST if help_selected else '')+(' '+RECOVERY_REQUEST if recovery_selected else '')
 rows=[owner('iri','person','Iri'),role('iri','main_subject','Iri'),owner('iri_face','face','existing face'),role('iri_face','primary_face','existing face'),assertion('face_belongs_to_iri','subject',{'kind':'part_of','left':'iri_face','right':'iri'},'existing face that belongs to Iri'),
 frozen('iri_presence','subject','iri','entity.presence','entity.presence/v1','present','Iri'),frozen('face_presence','subject','iri_face','anatomy.face.presence','anatomy.face.presence/v1','present','existing face'),
 frozen('declared_adult','age','iri','age.declared','age.declared/v1','adult','explicitly adult person'),frozen('adult_body','age','iri','age.presentation.body','age.presentation.body/v1','unmistakably_adult','unmistakably adult body and face presentation'),frozen('adult_face','age','iri_face','age.presentation.face','age.presentation.face/v1','unmistakably_adult','unmistakably adult body and face presentation'),frozen('declared_peer','role','iri','participant.role.peer','participant.role.peer/v1','declared','already declared a peer and peer rival'),frozen('declared_peer_rival','role','iri','participant.role.peer_rival','participant.role.peer_rival/v1','declared','already declared a peer and peer rival')]
 anchors=[anchor('declared_age','age','iri','age.declared','explicitly adult person'),anchor('body_range','age','iri','age.presentation.body','unmistakably adult body and face presentation'),anchor('face_range','age','iri_face','age.presentation.face','unmistakably adult body and face presentation')]
 if help_selected:rows += [owner('jan','person','Jan'),role('jan','secondary_subject','Jan'),assertion('helper_distinct','subject',{'kind':'disjoint','left':'jan','right':'iri'},'distinct from Iri'),frozen('helper_presence','subject','jan','entity.presence','entity.presence/v1','present','already established helper')]
 if recovery_selected:
  rows.append(frozen('prior_disruption','timing','iri','narrative.context.prior_disruption','narrative.prior_disruption/v1','declared','prior brief disruption is already declared'));anchors.append(anchor('prior_context','timing','iri','narrative.context.prior_disruption','prior brief disruption is already declared'))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'request','text':text}]},'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','role'],'open_dimensions':['age','appearance','expression','pose','action','event','timing'],'semantic_anchors':anchors},'semantic_assertions':rows,'user_exclusions':[]}
REC=copy.deepcopy(M['T']);REC['content']['role_evidence']=PROOF;DATA={'candidates':{CID:REC},'slot_catalog':CAT,'slot_bindings':{}}
COMPACT=layout.guard_record(REC,DATA);COMPACT_DATA={**DATA,'candidates':{CID:COMPACT}}
def eligible(entry,core):
 return g.core_entry_eligible(DATA,core,{'adult_allowed':True,'subject_category':'human','intent_constraints':{'subject_categories':['human'],'domains':[]}}, {'subject':{'tags':['human']}},'age_presentation',entry)
CASES=[];LOCKS=[];PROFILES=[];CORES={}
COMMON_EVIDENCE={'adult_role_phrase':'The adult peer rival is unmistakably adult in body and face.','haughty_baseline_phrase':'The haughty baseline uses half-lidded eyes and a poised face.','smug_expression_phrase':'A smug expression and superior smirk remain on Iri face.','adult_youthful_styling_phrase':'Fresh adult styling remains visible on Iri.','appearance_inference_exclusion_phrase':'Adult behavior carries the archetype, not childlike proportions.'}
SELECTED_EVIDENCE={'setback':('setback_selected_phrase','A small visible setback stays local to Iri.'),'help':('help_selected_phrase','The declared rival receives help from the established helper Jan.'),'mouth_warmth':('mouth_warmth_selected_phrase','A brief softening at the same rival mouth corner remains local.'),'cheek_warmth':('cheek_warmth_selected_phrase','A bounded visible cheek warmth on the same rival remains local.'),'recovery':('recovery_selected_phrase','The same rival tries to regain the superior smirk after declared disruption.')}
for rid,chosen in CHOICES:
 good=core_for('help' in chosen,'recovery' in chosen);CORES[rid]=good;s.frozen_witnesses(good)
 entries=[('full',s._guard_entry(PROOF,rid,{})),('compact',c.entry(COMPACT_DATA,CID,realization_id=rid))]
 obligations=['iri_presence','face_presence','declared_adult','adult_body','adult_face','declared_peer','declared_peer_rival']+(['helper_presence'] if 'help' in chosen else [])+(['prior_disruption'] if 'recovery' in chosen else [])
 for form,entry in entries:
  result=s.admission(entry,good);assert result['allowed'],(rid,form,result)
  dims,props,_=s.permission_scope(entry,good);assert s.property_scope_allowed(good,dims,props)
  assert eligible(entry,good),(rid,form,'whole_consumer')
  CASES.append({'rid':rid,'form':form,'case':'all_exact_frozen_requirements','allowed':True,'native_guard_receipt':result['native_guards']})
  for aid in obligations:
   for defect in ['missing','wrong_owner','wrong_value']:
    bad=copy.deepcopy(good)
    if defect=='missing':bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!=aid]
    elif defect=='wrong_value':next(x for x in bad['semantic_assertions'] if x['assertion_id']==aid)['axes']['value']='explicitly_wrong_value'
    else:
     bad['baseline_prompt_en']+=' Rui is an unrelated comparison person.';bad['request_binding']['active_spans'][0]['text']=bad['baseline_prompt_en'];bad['semantic_assertions'].append(owner('rui','person','Rui'))
     item=next(x for x in bad['semantic_assertions'] if x['assertion_id']==aid);item['axes']['owner']='rui'
     if item['dimension'] not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['semantic_anchors'].append(anchor('wrong_'+aid,item['dimension'],'rui',item['axes']['property'],'Rui'))
    result=s.admission(entry,bad);assert not result['allowed'],(rid,form,aid,defect,result)
    CASES.append({'rid':rid,'form':form,'case':defect,'assertion_id':aid,'allowed':False,'reason':result['reason']})
  for aid in ['face_belongs_to_iri']+(['helper_distinct'] if 'help' in chosen else []):
   bad=copy.deepcopy(good);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!=aid];result=s.admission(entry,bad);assert not result['allowed'],(rid,aid)
   CASES.append({'rid':rid,'form':form,'case':'missing_explicit_owner_relation','assertion_id':aid,'allowed':False,'reason':result['reason']})
  for ix,p in enumerate(props):
   bad=copy.deepcopy(good);bad['intent_lock']['semantic_anchors'].append(anchor('effect_lock_'+str(ix),p['dimension'],p['target'],p['property'],'Iri' if p['target']!='jan' else 'Jan'))
   assert not s.property_scope_allowed(bad,dims,props) and not eligible(entry,bad),(rid,p)
   LOCKS.append({'rid':rid,'form':form,'case':'actual_property_lock','effect':p,'denied':True})
  age=copy.deepcopy(good);age['intent_lock']['open_dimensions'].remove('age');age['intent_lock']['locked_dimensions'].append('age');assert not eligible(entry,age)
  same=copy.deepcopy(good);same['intent_lock']['semantic_anchors'].append(anchor('same_age','age','iri','age.presentation.youthful_adult','Iri'));same['semantic_assertions'].append(frozen('same_age_value','age','iri','age.presentation.youthful_adult','age.presentation.youthful_adult/v1','youth_appearing_adult','Iri'));assert not s.property_scope_allowed(same,dims,props)
  appearance=copy.deepcopy(good);appearance['intent_lock']['open_dimensions'].remove('appearance');appearance['intent_lock']['locked_dimensions'].append('appearance');assert not eligible(entry,appearance)
  age_only=[p for p in props if p['dimension']=='age'];assert s.property_scope_allowed(appearance,['age'],age_only)
  LOCKS.extend([{'rid':rid,'form':form,'case':case,'denied':True} for case in ['whole_age_lock','same_current_age_value_lock','whole_appearance_lock_from_independent_appearance_effects']])
  if 'help' not in chosen:assert 'secondary_subject' not in s.frozen_witnesses(good)['graph']['roles']
 # Both complete and compact selected projections compile exactly the chosen
 # duties. Literal evidence below is independently written, never first-match
 # copied from discovery labels or used as a source positive fact.
 selected_full=c.entry(DATA,CID,realization_id=rid);selected_compact=c.entry(COMPACT_DATA,CID,realization_id=rid)
 assert selected_full['_selected_profile_contract']==selected_compact['_selected_profile_contract']==PROOF['profile_contracts'][rid]
 evidence={**COMMON_EVIDENCE,**dict(SELECTED_EVIDENCE[k] for k in chosen)}
 prompt=' '.join(evidence.values())+' Iri retains the existing adult declaration and adult body and face while visibly presenting as a youthful adult.'
 interpretation={'realization_id':rid,'selected_profile_contract':PROOF['profile_contracts'][rid],'selected_profile_evidence':evidence}
 for form,entry in [('full_selected',selected_full),('compact_selected',selected_compact)]:
  audit.audit_selected_native_profile(entry,interpretation,prompt)
  for defect in ['missing_contract','wrong_contract','missing_duty','foreign_duty','nonliteral_evidence']:
   bad=copy.deepcopy(interpretation)
   if defect=='missing_contract':bad.pop('selected_profile_contract')
   elif defect=='wrong_contract':bad['selected_profile_contract']['compiled_sha256']='0'*64
   elif defect=='missing_duty':bad['selected_profile_evidence'].pop('adult_role_phrase')
   elif defect=='foreign_duty':bad['selected_profile_evidence']['foreign_phrase']='An unchosen mandatory helper appears.'
   else:bad['selected_profile_evidence']['adult_role_phrase']='A different adult rival phrase absent from prompt.'
   try:audit.audit_selected_native_profile(entry,bad,prompt)
   except ValueError:pass
   else:raise AssertionError((rid,form,defect))
  PROFILES.append({'rid':rid,'form':form,'selected_contract':PROOF['profile_contracts'][rid],'literal_positive_evidence':interpretation,'prompt':prompt,'negative_cases':5,'all_passed':True,'required_field_count':len(evidence)})
noage=core_for();noage['adult_allowed']=True;noage['semantic_assertions']=[x for x in noage['semantic_assertions'] if x['assertion_id']!='declared_adult'];assert not s.admission(s._guard_entry(PROOF,'baseline',{}),noage)['allowed']
VERIFIED=nr.verify_batch(str((P/'ASSIGNMENT.json').relative_to(Path.cwd())),str((O/'BATCH.json').relative_to(Path.cwd())),str((O/'NOTE.json').relative_to(Path.cwd())))
modules={name:{'file':str(Path(module.__file__)),'sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()} for name,module in sys.modules.items() if getattr(module,'__file__',None) and (name.startswith('photo_') or name in ['visual_profile_contracts','native_reviews','direct_review','audit_composed_prompt','candidate_semantics_generator'])}
assert not {name:v for name,v in modules.items() if name.startswith('photo_') and '/generations/' not in v['file']}
OUT={'schema':'fresh-native-17437-isolated-validation/v1','production_generation':str(FROZEN),'production_modules':modules,'candidate_independent_cores':CORES,'full_compact_cases':CASES,'lock_negatives':LOCKS,'selected_profile_audits':PROFILES,'adult_permission_without_declared_age_rejected':True,'age_is_not_automatically_appearance_alias':True,'batch_verification':{k:v for k,v in VERIFIED.items() if k!='records'},'proof_fact_count':len(PROOF['facts']),'source_unit_count':len(PROOF['source_units']),'semantic_accuracy_from_shape_alone':False,'root_accepted':False,'operating_native_qualified_count':0}
path=R/'authored/native_fresh_08250_17437_01_checks.json';assert not path.exists();path.write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'full_compact_cases':len(CASES),'lock_negatives':len(LOCKS),'profile_positives':len(PROFILES),'profile_negatives':sum(x['negative_cases'] for x in PROFILES),'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
