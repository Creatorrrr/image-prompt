"""Readonly production API correctness probes, explicit controlled synthetic data.
Independent negative edits; common baseline serializers/fixtures are reused and
identified, with no mock wrapper substituted for a pipeline.
"""
import copy,hashlib,json,pathlib,sys
ROOT=pathlib.Path.cwd();sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture,entries,freeze,after_evidence
from tests.test_photo_native_source_guards_v2 import compound,compound_choices,hands_core,choices
from tests.test_photo_native_compound_evidence import A,B,dependencies
from tests.test_photo_semantic_evidence import seal
from tests.test_photo_native_owner_selection import sign_core
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_native_permission as p,photo_search_layout as layout,audit_composed_prompt as audit,prompt_generator as g
OUT=pathlib.Path(__file__).parent/'DATA-INTEGRITY-PROBE-v1.json';assert not OUT.exists()
rows=[]
def record(label,fn,expect):
 try:
  value=fn();actual=bool(value['allowed'] and value.get('status')=='qualified')if isinstance(value,dict)and'allowed'in value else bool(value)
  rows.append({'case':label,'expected':expect,'actual':actual,'pass':actual==expect,'result':value})
 except Exception as exc:rows.append({'case':label,'expected':expect,'actual':False,'pass':expect is False,'exception':type(exc).__name__,'reason':str(exc)})
# 1. Actual required child with two source branches: no default RID may be invented.
data=compound();child=data['candidates'][B];proof=child['content']['role_evidence'];original=copy.deepcopy(proof['facts'])
child['effects']['realizations']={'mode':'one','branches':[{'id':rid,'conditions':{},'context_terms':[],'effects':{'dimensions':[],'properties':[]}}for rid in ['alpha','beta']]}
proof['facts']=[{**copy.deepcopy(f),'id':f['id']+'_'+rid,'realization_id':rid}for rid in ['alpha','beta']for f in original]
proof['owner_maps']={rid:copy.deepcopy(proof['owner_maps']['base'])for rid in ['alpha','beta']}
seal(data,{'pose':['holding_alpha','holding_beta']},cid=B);dependencies(data,A,'base',[B]);seal(data,{'pose':['holding']});c.validate(data)
frozen=hands_core();choice=choices(data,frozen);choice['entries']+=choices(data,frozen,cid=B,rid='beta')['entries']
for shape in ['full','compact']:
 view=data if shape=='full'else {**data,'candidates':{cid:layout.guard_record(r,data)for cid,r in data['candidates'].items()}}
 selected=c.entry(view,A,realization_id='base',dependency_selections={B:'beta'},owner_selections=choice)
 missing=c.entry(view,A,realization_id='base',owner_selections=choice)
 foreign=c.entry(view,A,realization_id='base',dependency_selections={B:'gamma'},owner_selections=choice)
 record('required_child_'+shape+'_selected_beta',lambda:n.admission(selected,frozen),True)
 record('required_child_'+shape+'_missing_branch',lambda:n.admission(missing,frozen),False)
 record('required_child_'+shape+'_foreign_branch',lambda:n.admission(foreign,frozen),False)
 record('required_child_'+shape+'_missing_branch_permission',lambda:n.permission_scope(missing,frozen),False)
# Drop a mandatory reference only in the projected entry: exact transport must fail.
selected=c.entry(data,A,realization_id='base',dependency_selections={B:'beta'},owner_selections=choice);tampered=copy.deepcopy(selected)
if '_semantic_evidence_guard'in tampered:
 guard=tampered['_semantic_evidence_guard'];guard['dependencies']['base']=[];guard['dependency_guards']['base']=[]
 guard['compact_sha256']=c.digest({k:v for k,v in guard.items()if k!='compact_sha256'})
record('required_reference_removed_from_serialized_projection',lambda:n.admission(tampered,frozen),False)
# 2. Same actual image has conflicting macro/wide E assignments from distinct sources.
actual=source_fixture();mc=core_fixture();f,co=entries(actual,mc);joint=copy.deepcopy(actual);br=copy.deepcopy(joint['candidates'][A]);br['id']=B
br['content']['en']=br['content']['en'].replace('macro shot scale','wide shot scale')
for rule in br['conditions']['native_guards']['rules']:
 for side in ['left','right']:rule[side]['candidate_id']=B
br['content']['role_evidence']['facts'][-1]['quote']='select wide shot scale';br['content']['role_evidence']['facts'][-1]['value']['value']='wide'
joint['candidates'][B]=br;seal(joint,{'fixture_shot':['macroE']},cid=B);c.validate(joint)
ch=choices(joint,mc,{'item':'X','image':'I'});ch['entries']+=choices(joint,mc,{'item':'X','image':'I'},cid=B)['entries']
for shape in ['full','compact']:
 view=joint if shape=='full'else{**joint,'candidates':{cid:layout.guard_record(r,joint)for cid,r in joint['candidates'].items()}}
 ee=[c.entry(view,cid,realization_id='base',owner_selections=ch)for cid in [A,B]]
 record('same_actual_image_conflicting_E_'+shape,lambda:n._resolve_selected_native_contracts(ee,mc),False)
# 3. Trusted synthetic source/core plan and independent typed result correspondence.
a,plan=freeze(actual,mc,f)
with p.trusted_permission_session(a,plan):
 for shape,e in [('full',f),('compact',co)]:record('mandatory_baseline_'+shape,lambda:n.admission(e,mc),True)
 record('mandatory_final_missing_typed_result',lambda:n.audit_final_scalar_preservation([f],mc),False)
for defect in ['none','hidden','wrong_image','scalar_owner_image','relation_owner_image','missing_visibility','wrong_type','foreign_input','changed_topology']:
 after=core_fixture('I2'if defect=='wrong_image'else'I','hidden'if defect=='hidden'else'visible')
 scalar=next(x for x in after['semantic_assertions']if x['assertion_id']=='visible');relation=next(x for x in after['semantic_assertions']if x['assertion_id']=='image_relation')
 if defect=='scalar_owner_image':scalar['axes']['owner']='I'
 elif defect=='relation_owner_image':relation['axes']['owner']='I'
 elif defect=='missing_visibility':after['semantic_assertions'].remove(scalar)
 elif defect=='wrong_type':scalar['axes']['value_type']='image.visibility/v1'
 elif defect=='foreign_input':scalar['source_span_ids']=['not_an_input_span']
 elif defect=='changed_topology':after['semantic_assertions']=[x for x in after['semantic_assertions']if x['assertion_id']!='images_disjoint']
 sign_core(after)
 def result_call():
  state=p.freeze_after_state(plan,after,expected_after_sha256=c.digest(after),evidence=after_evidence(plan),reviewer='independent controlled result reviewer')
  with p.trusted_permission_session(a,plan,after_state=state):return n.audit_final_scalar_preservation([f],mc)
 record('typed_after_'+defect,result_call,defect=='none')
# 4. Same bound context must not survive changed input/core/owner choice/session.
with p.trusted_permission_session(a,plan):
 with n.bound_selected_resolution([f],mc):
  record('cache_unchanged_core_full',lambda:n.admission(f,mc),True)
  record('cache_unchanged_core_compact',lambda:n.admission(co,mc),True)
  for defect in ['hidden','wrong_image','input_text','same_owner_wrong_mapping']:
   changed=core_fixture('I2'if defect=='wrong_image'else'I','hidden'if defect=='hidden'else'visible');e=copy.deepcopy(f)
   if defect=='input_text':changed['source_request']+=' additional independent input';sign_core(changed)
   if defect=='same_owner_wrong_mapping':e['_native_owner_selections']['entries'][0]['bindings'][1]['owner_id']='I2'
   record('cache_changed_'+defect,lambda:n.admission(e,changed),False)
  token=p._ACTIVE.set(None)
  try:record('cache_session_removed',lambda:n.admission(f,mc),False)
  finally:p._ACTIVE.reset(token)
# Real native final audit, not patched: complete overall audit_composed_prompt is a separate boundary.
composed={'chosen_candidate_ids':[A],'candidate_interpretations':[{'candidate_id':A,'realization_id':'base'}],'owner_selections':f['_native_owner_selections'],'prompt_en':'The existing physical item remains visible in image I with macro shot scale.'};pack={'authorial_core':mc,'creative_controls':{}}
record('actual_native_final_without_session',lambda:not audit.audit_native_adoptions(pack,composed,actual),False)
state=p.freeze_after_state(plan,mc,expected_after_sha256=c.digest(mc),evidence=after_evidence(plan),reviewer='independent controlled result reviewer')
with p.trusted_permission_session(a,plan,after_state=state):
 record('actual_native_final_typed_result_no_mock',lambda:not audit.audit_native_adoptions(pack,composed,actual),True)
result={'schema':'independent-native-permission-data-integrity-probe/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','cases':rows,'counts':{'total':len(rows),'pass':sum(x['pass']for x in rows),'unexpected':sum(not x['pass']for x in rows)},'fixture_boundary':'Common explicit writer-controlled source/core serializers reused; adversarial edits, two-source conflict, child branch alpha/beta and typed result mutations independently authored. All actual calls without mock. audit_native_adoptions is the native final subpipeline, not complete pack/composition/render pipeline. No original1299 semantic approval/pixels/operating/source/code/Git/model/network mutation.','code_pins':[{'file':m.__file__,'raw_sha256':hashlib.sha256(pathlib.Path(m.__file__).read_bytes()).hexdigest()}for m in [p,n,c,layout,audit,g]],'controlled_sources':{'required_child':data,'conflicting_joint':joint,'mandatory_scalar':actual},'controlled_cores':{'required_child':frozen,'mandatory_scalar':mc}}
OUT.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps({'counts':result['counts'],'unexpected':[x for x in rows if not x['pass']],'artifact':str(OUT)},ensure_ascii=False))
