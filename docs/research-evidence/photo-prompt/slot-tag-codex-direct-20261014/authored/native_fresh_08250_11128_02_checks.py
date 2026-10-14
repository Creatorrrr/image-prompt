"""Independent literal core requests and exact frozen-v4 full/compact adversaries."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_11128_02.py')))
R=M['R'];FROZEN=M['FROZEN'];s=M['s'];c=M['c'];nr=M['nr'];CID=M['CID'];P=M['P'];O=M['O'];CAT=M['CAT']
# direct_review adds the working scripts path. All production imports used for
# these checks are explicitly frozen and all loaded paths are recorded below.
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
import photo_search_layout as layout
import prompt_generator as g
assert Path(s.__file__).is_relative_to(FROZEN)
for name in ['photo_candidate_corpus','photo_candidate_realizations','photo_semantic_evidence','photo_contracts','photo_search_layout']:
 module=sys.modules.get(name)
 if module is not None:assert Path(module.__file__).is_relative_to(FROZEN),(name,module.__file__)
BEFORE=M['BEFORE'];AFTER=copy.deepcopy(M['AFTER']);PROOF=M['PROOF'];AFTER['content']['role_evidence']=PROOF
CORPUS={'slot_catalog':CAT,'slot_bindings':{},'candidates':{CID:AFTER}}
def assertion(aid,kind,dimension='subject',**axes):
 return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['request'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'literal':TEXT},'affected_dimensions':[dimension]}
def core(state,*,overlap=False):
 global TEXT
 TEXT='An existing adult person is present as the main subject. The outfit, posture and activity are open.'
 if state=='known_present':TEXT+=' Existing reference hair color is black and requester-fixed identity is person_A. Preserve both.'
 elif state=='known_absent':TEXT+=' No reference appearance or requester-fixed identity is supplied or declared.'
 else:TEXT+=' Whether any reference appearance or requester-fixed identity is established has not been reviewed.'
 if overlap:TEXT+=' The already specified pencil-skirt outfit is fixed and belongs to reference appearance.'
 sha=hashlib.sha256(TEXT.encode()).hexdigest()
 host={'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha}]}
 request={'request_sha256':sha,'request_envelope_sha256':hashlib.sha256(('explicit fixture envelope '+TEXT).encode()).hexdigest(),'input_inventory':host,'active_spans':[{'source_span_id':'request','text':TEXT}]}
 rows=[assertion('owner','owner',owner='person_A',owner_kind='human'),assertion('role','role',role='main_subject',owner='person_A'),assertion('presence','fact',owner='person_A',property='entity.presence',value_type='entity.presence/v1',value='present'),assertion('adult','fact',dimension='age',owner='person_A',property='age.declared',value_type='age.declared/v1',value='adult')]
 anchors=[]
 if state=='known_present':
  rows.extend([assertion('hair_color','fact',dimension='appearance',owner='person_A',property='appearance.hair_color',value_type='appearance.hair_color/v1',value='black',scope_kinds=['reference_appearance'],source_input_ids=['request']),assertion('identity','fact',dimension='identity',owner='person_A',property='subject.identity',value_type='subject.identity/v1',value='person_A',scope_kinds=['requester_identity'],source_input_ids=['request'])])
  anchors.append({'dimension':'appearance','target':'person_A','property':'appearance.hair_color'})
 if overlap:
  rows.append(assertion('fixed_wardrobe','fact',dimension='appearance',owner='person_A',property='wardrobe.ensemble',value_type='wardrobe.ensemble/v1',value='pencil_skirt',scope_kinds=['reference_appearance'],source_input_ids=['request']))
  anchors.append({'dimension':'appearance','target':'person_A','property':'wardrobe.ensemble'})
 frozen={'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':request,'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','age','identity','count','concept'],'open_dimensions':['appearance','pose','action','camera','lighting','material','composition','timing','event','relationship','role','body_geometry'],'semantic_anchors':anchors}}
 for scope in ['reference_appearance','requester_identity']:
  facts=s.frozen_witnesses(frozen)['facts']
  items=[{k:row[k] for k in ['assertion_id','dimension','target','property','value']} for row in facts if scope in row.get('scope_kinds',[])]
  payload={'schema':'photo-frozen-scope-inventory/v1','complete':True,'input_binding':s.witnesses.input_binding(request),'reviewed_input_ids':['request'],'state':state,'items':items}
  rows.append(assertion('scope_'+scope,'scope_inventory',owner='person_A',scope_kind=scope,inventory=s.witnesses.canonical(payload)))
 s.frozen_witnesses(frozen);return frozen
CORES={state:core(state) for state in ['known_absent','known_present','unknown']};CORES['same_value_overlap']=core('known_present',overlap=True)
def extend_negative_request(x,phrase):
 # The wrong-owner adversary has a genuinely separately declared owner; it
 # must not fail merely because a test helper supplied stale literal evidence.
 text=x['baseline_prompt_en']+' '+phrase;x['baseline_prompt_en']=text;x['subject']=text
 x['request_binding']['active_spans'][0]['text']=text
 sha=hashlib.sha256(text.encode()).hexdigest();x['request_binding']['request_sha256']=sha
 x['request_binding']['request_envelope_sha256']=hashlib.sha256(('explicit fixture envelope '+text).encode()).hexdigest()
 x['request_binding']['input_inventory']['items'][0]['sha256']=sha
 for row in x['semantic_assertions']:
  if row['axes']['kind']=='scope_inventory':
   payload=json.loads(row['axes']['inventory']);payload['input_binding']=s.witnesses.input_binding(x['request_binding']);row['axes']['inventory']=s.witnesses.canonical(payload)
 return {'assertion_id':'other','dimension':'subject','polarity':'required','source_span_ids':['request'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'owner','owner':'person_B','owner_kind':'human'},'evidence':{'literal':phrase},'affected_dimensions':['subject']}
CASES=[]
for state in ['known_absent','known_present']:
 CASES.append((state,CORES[state],True))
CASES.extend([('unknown',CORES['unknown'],False),('same_value_overlap',CORES['same_value_overlap'],False)])
for defect in ['presence_absent','adult_absent','adult_wrong_value','presence_wrong_owner','adult_wrong_owner','role_absent','input_inventory_absent','scope_absent','scope_wrong_owner','scope_wrong_item_value','scope_incomplete','input_stale','reviewed_input_missing']:
 x=copy.deepcopy(CORES['known_present'])
 if defect in ['presence_absent','adult_absent']:x['semantic_assertions']=[r for r in x['semantic_assertions'] if r['assertion_id']!=defect.split('_')[0]]
 elif defect=='adult_wrong_value':next(r for r in x['semantic_assertions'] if r['assertion_id']=='adult')['axes']['value']='child'
 elif defect in ['presence_wrong_owner','adult_wrong_owner']:
  x['semantic_assertions'].append(extend_negative_request(x,'Another already established person person_B is distinct from the main subject.'))
  next(r for r in x['semantic_assertions'] if r['assertion_id']==defect.split('_')[0])['axes']['owner']='person_B'
  s.frozen_witnesses(x)
 elif defect=='role_absent':x['semantic_assertions']=[r for r in x['semantic_assertions'] if r['assertion_id']!='role']
 elif defect=='input_inventory_absent':x['request_binding'].pop('input_inventory')
 elif defect=='scope_absent':x['semantic_assertions']=[r for r in x['semantic_assertions'] if not r['assertion_id'].startswith('scope_')]
 else:
  row=next(r for r in x['semantic_assertions'] if r['assertion_id']=='scope_reference_appearance');payload=json.loads(row['axes']['inventory'])
  if defect=='scope_wrong_owner':row['axes']['owner']='unbound_other'
  elif defect=='scope_wrong_item_value':payload['items'][0]['value']['value']='white'
  elif defect=='scope_incomplete':payload['complete']=False
  elif defect=='input_stale':payload['input_binding']['input_inventory_sha256']='0'*64
  elif defect=='reviewed_input_missing':payload['reviewed_input_ids']=[]
  row['axes']['inventory']=s.witnesses.canonical(payload)
 CASES.append((defect,x,False))
RESULT=[];LOCKS=[];AUDITS=[]
for rid in ['standing','walking']:
 full=s._guard_entry(PROOF,rid,{})
 compact=c.entry(CORPUS,CID,realization_id=rid)
 for label,entry in [('full',full),('compact',compact)]:
  for name,frozen,allowed in CASES:
   result=s.admission(entry,frozen);assert result['allowed'] is allowed,(rid,label,name,result)
   RESULT.append({'rid':rid,'form':label,'case':name,'expected_allowed':allowed,'actual':result})
   actual_eligible=g.core_entry_eligible(CORPUS,frozen,{'adult_allowed':True,'subject_category':'human','intent_constraints':{'subject_categories':['human'],'domains':[]}}, {'subject':{'tags':['human']}},'wardrobe_style',entry)
   assert actual_eligible is allowed,(rid,label,name,'whole_consumer')
  good=CORES['known_present'];receipt=s.admission(entry,good);prompt='The established black hair color and person_A requester identity remain unchanged.'
  ev={'scope_preservation_evidence':{'scope_reference_appearance':{'hair_color':{'owner':'person_A','value':{'type':'appearance.hair_color/v1','value':'black'},'prompt_evidence':prompt}},'scope_requester_identity':{'identity':{'owner':'person_A','value':{'type':'subject.identity/v1','value':'person_A'},'prompt_evidence':prompt}}}}
  s.audit_scope_preservation(receipt,ev,prompt);AUDITS.append({'rid':rid,'form':label,'case':'exact_final_literal_evidence','passed':True})
  for bad in [{}, {'scope_preservation_evidence':{}}, {'scope_preservation_evidence':{**ev['scope_preservation_evidence'],'foreign':{}}}]:
   try:s.audit_scope_preservation(receipt,bad,prompt)
   except ValueError:AUDITS.append({'rid':rid,'form':label,'case':'missing_or_foreign_final_evidence','rejected':True})
   else:raise AssertionError('bad final evidence accepted')
  for defect in ['wrong_owner','wrong_value','nonliteral_phrase']:
   bad=copy.deepcopy(ev);row=bad['scope_preservation_evidence']['scope_reference_appearance']['hair_color']
   if defect=='wrong_owner':row['owner']='person_B'
   elif defect=='wrong_value':row['value']['value']='white'
   else:row['prompt_evidence']='A preservation phrase absent from the final prompt.'
   try:s.audit_scope_preservation(receipt,bad,prompt)
   except ValueError:AUDITS.append({'rid':rid,'form':label,'case':defect,'rejected':True})
   else:raise AssertionError('incorrect final preservation evidence accepted')
  for effect in PROOF['effect_sets'][rid]['properties']:
   bad=copy.deepcopy(CORES['known_absent']);bad['intent_lock']['semantic_anchors'].append({'dimension':effect['dimension'],'target':'person_A','property':effect['property']})
   dims,props,_=s.permission_scope(entry,bad);allowed=s.property_scope_allowed(bad,dims,props)
   assert allowed is False;LOCKS.append({'rid':rid,'form':label,'property':effect,'denied':True})
  dims,props,_=s.permission_scope(entry,CORES['known_absent']);assert s.property_scope_allowed(CORES['known_absent'],dims,props)
VERIFIED=nr.verify_batch(str((P/'ASSIGNMENT.json').relative_to(Path.cwd())),str((O/'BATCH.json').relative_to(Path.cwd())),str((O/'NOTE.json').relative_to(Path.cwd())))
modules={name:{'file':str(Path(module.__file__)),'sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()} for name,module in sys.modules.items() if getattr(module,'__file__',None) and (name.startswith('photo_') or name in ['native_reviews','direct_review'])}
OUT={'schema':'fresh-native-11128-isolated-validation/v1','production_generation':str(FROZEN),'production_modules':modules,'candidate_free_fixture_cores':CORES,'full_compact_cases':RESULT,'property_lock_negatives':LOCKS,'final_literal_audits':AUDITS,'batch_verification':{k:v for k,v in VERIFIED.items() if k!='records'},'proof_fact_count':len(PROOF['facts']),'source_unit_count':len(PROOF['source_units']),'semantic_accuracy_from_shape_alone':False,'root_accepted':False,'operating_native_qualified_count':0}
path=R/'authored/native_fresh_08250_11128_02_checks.json';assert not path.exists();path.write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'cases':len(RESULT),'locks':len(LOCKS),'audits':len(AUDITS),'validation':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
