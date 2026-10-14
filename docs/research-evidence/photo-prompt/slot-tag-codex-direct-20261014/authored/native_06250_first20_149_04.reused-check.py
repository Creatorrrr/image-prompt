"""Offline, exact-current-source thirteen-proof full/compact technical checks.
The frozen core is an explicitly authored isolated request fixture, not a run.
"""
import sys,json,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert raw(G/'scripts/photo_semantic_evidence.py')=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
P=R/'native-inputs/prepared/review06250-00000-00020-149-04';O=R/'native_batches/review06250-00000-00020-149-04'
A=json.loads((P/'ASSIGNMENT.json').read_text());I=nr.artifact(ROOT,A['input']);S=nr.artifact(ROOT,I['current_snapshot']);B=json.loads((O/'BATCH.json').read_text())
verified=nr.verify_batch(str((P/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH.json').relative_to(ROOT)),str((O/'NOTE.json').relative_to(ROOT)))
assert verified['statuses']=={'approved':20,'diagnostic_reviewed':0,'pending':0} and not verified['root_accepted']

THEME=None
def fixture(dim,role,*,missing=False,whole=False,anchor=None,alias=False,missing_theme=False,wrong_theme=False,theme_on_other=False):
 text='The caller independently declares one image, its recording camera, and its scene. Their owner addresses are fixed before candidate selection. A separate unrelated owner is explicitly disjoint. Any stated property lock is requester authored. '+({'pet_theme_compatible':'The existing image content is independently compatible with a pet subject-matter theme; this does not choose a photographic genre or add a pet.','food_theme_compatible':'The existing image content is independently compatible with a food subject-matter theme; this does not choose a photographic genre or add food.','interior_space_theme_compatible':'The existing image content is independently compatible with an interior-space theme; this does not choose a photographic genre or add a room.'}.get(THEME,''))
 rows=[]
 def statement(aid,kind,**axes):
  rows.append({'assertion_id':aid,'dimension':'subject','polarity':'required','source_span_ids':['request_fixture'],'axes':{'native_schema':e.witnesses.SCHEMA,'kind':kind,**axes},'evidence':{'meaning':text},'affected_dimensions':['subject']})
 for role_name,owner,kind in [('image','actual_image','image'),('recording_camera','actual_camera','camera'),('scene','actual_scene','scene')]:
  statement('owner_'+owner,'owner',owner=owner,owner_kind=kind)
  if not (missing and role_name==role):statement('role_'+role_name,'role',role=role_name,owner=owner)
 statement('owner_other','owner',owner='unrelated_owner',owner_kind='entity')
 actual={'image':'actual_image','recording_camera':'actual_camera','scene':'actual_scene'}[role]
 statement('other_disjoint','disjoint',left=actual,right='unrelated_owner')
 if alias:
  statement('alias_owner','owner',owner='locked_alias',owner_kind='entity')
  statement('explicit_alias','equivalent',left='locked_alias',right=actual)
 if THEME and not missing_theme:
  rows.append({'assertion_id':'independent_theme','dimension':'concept','polarity':'required','source_span_ids':['request_fixture'],'axes':{'native_schema':e.witnesses.SCHEMA,'kind':'fact','owner':'unrelated_owner' if theme_on_other else actual,'property':'image.subject_matter.theme_compatibility','value_type':'image.subject_matter.theme_compatibility/v1','value':'wrong_theme' if wrong_theme else THEME},'evidence':{'meaning':text},'affected_dimensions':['concept']})
 locked=['subject']+(['concept'] if THEME else [])+([dim] if whole else [])
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'request_fixture','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':locked,'open_dimensions':[] if whole else [dim],'semantic_anchors':[] if anchor is None else [{'dimension':dim,'target':anchor[0],'property':anchor[1]}]}}

contract={'subject_category':'object','adult_allowed':True,'intent_constraints':{'domains':[],'subject_categories':[]}}
picked={'subject':{'en':'An independently declared object scene','tags':['object']},'action':{},'location':{}}
results=[]
for row in B['records']:
 if row['ordinal'] in {0,1,2,6,7,11,12}:continue
 cid=row['candidate_id'];record=copy.deepcopy(row['source_after']);record['content']['role_evidence']=row['proof']
 data={**S,'candidates':{**S['candidates'],cid:record}}
 e.validate(record,data['slot_catalog'],corpus=data)
 THEME={10:'pet_theme_compatible',13:'food_theme_compatible',19:'interior_space_theme_compatible'}.get(row['ordinal'])
 tag=next(iter(row['proof']['roles']));fact=next(f for f in row['proof']['facts'] if f['mode']=='effect');dim=fact['dimension'];prop=fact['property'];role=row['proof']['owner_maps']['base']['bindings'][0]['core_role']
 own=[v for v in S['slot_bindings'].values() if v['candidate_id']==cid];assert len(own)==1
 assert own[0]['conditions']=={'subject_applicability':{}}
 actual={'image':'actual_image','recording_camera':'actual_camera','scene':'actual_scene'}[role]
 matrix=[]
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(record,data)}})]:
  for bid in [None,own[0]['id']]:
   entry=c.entry(view,cid,bid,realization_id='base');core=fixture(dim,role)
   q=e.qualification(data['slot_catalog'][tag],view['candidates'][cid],source_data=data);assert q['status']=='eligible' and q['native_qualification']=='qualified',q
   admission=e.admission(entry,core);assert admission['allowed'],(row['ordinal'],label,bid,admission)
   assert g.core_entry_eligible(view,core,contract,picked,tag,entry),(row['ordinal'],label,bid)
   dims,effects,graph=e.permission_scope(entry,core)
   assert dims==[dim] and len(effects)==len([f for f in row['proof']['facts'] if f['mode']=='effect'])
   assert {x['property'] for x in effects}=={x['property'] for x in row['proof']['facts'] if x['mode']=='effect'}
   assert {x['target'] for x in effects}=={actual}
   assert not e.admission(entry,fixture(dim,role,missing=True))['allowed']
   if THEME:
    for defect in ['missing_theme','wrong_theme','theme_on_other']:
     assert not e.admission(entry,fixture(dim,role,**{defect:True}))['allowed'],(row['ordinal'],defect)
   assert not g.core_entry_eligible(view,fixture(dim,role,whole=True),contract,picked,tag,entry)
   cases=[]
   for name,anchor_owner,anchor_prop,alias in [('exact',actual,prop,False),('ancestor',actual,prop.split('.')[0],False),('alias','locked_alias',prop,True)]:
    locked=fixture(dim,role,anchor=(anchor_owner,anchor_prop),alias=alias)
    assert not e.property_scope_allowed(locked,dims,effects,record=entry),(row['ordinal'],name)
    assert not g.core_entry_eligible(view,locked,contract,picked,tag,entry),(row['ordinal'],name,'eligibility')
    cases.append(name)
   other=fixture(dim,role,anchor=('unrelated_owner',prop));assert e.property_scope_allowed(other,dims,effects,record=entry)
   sibling=fixture(dim,role,anchor=(actual,'unrelated.sibling_property'));assert e.property_scope_allowed(sibling,dims,effects,record=entry)
   matrix.append({'view':label,'binding_id':bid,'qualification':q,'admission':admission,'actual_permission_properties':effects,'whole_dimension_rejected':True,'original_exact_ancestor_alias_locks_rejected':cases,'explicit_disjoint_other_owner_allowed':True,'unrelated_property_allowed':True,'missing_independent_owner_rejected':True,'actual_own_binding_conditions':own[0]['conditions']})
 # Every positive field remains required; references cannot supply a missing ordinary App anchor.
 bad=copy.deepcopy(record);bad['content']['role_evidence']['source_units']=[u for u in bad['content']['role_evidence']['source_units'] if u['pointer']!='/content/ko']
 bad['content']['role_evidence']['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(bad['content']['role_evidence'])
 try:e.validate(bad,data['slot_catalog'],corpus={**data,'candidates':{**data['candidates'],cid:bad}})
 except ValueError:coverage_rejected=True
 else:raise AssertionError('missing KO ordinary/reference source coverage accepted')
 results.append({'ordinal':row['ordinal'],'candidate_id':cid,'own_binding':own[0],'matrix':matrix,'missing_positive_KO_coverage_rejected':coverage_rejected})

mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'raw_sha256':raw(p)}
out={'schema':'photo-manual-first20-actual-source-diagnostics/v1','generation':str(G),'native_module_sha256':raw(G/'scripts/photo_semantic_evidence.py'),'actual_modules':mods,'verification':{k:v for k,v in verified.items() if k!='records'},'results':results,'prepared_count':20,'actual_read_count':20,'new_authored_source_after_count':0,'fresh_current_selected_source_read_count':7,'unchanged_proof_exact_reuse_count':13,'new_native_proof_count':7,'guard_proposal_whole_after_read_count':0,'root_acceptance_count':0,'operational_adoption_count':0,'boundary':'Thirteen exact previous accepted source/proof pairs are revalidated against current04 source/catalog/closure without new signatures or semantic read counts. Seven new lighting source04 proofs are tested in a separate diagnostic. Technical full/compact actual-source fixture checks do not prove semantic entailment, a real user request, live generation, pixels or root acceptance. Original catalog139/compiled locator provenance is preserved. No desired candidate values are pre-frozen as prerequisites; independently declared neutral image/camera/scene owners are fixture inputs. Empty receiver arrays are manual per-fact decisions, not automatic defaults.'}
p=O/'DIAGNOSTIC-REUSED13.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',len(results),'proofs',sum(len(x['matrix']) for x in results),'full/compact x binding cases',raw(p))
