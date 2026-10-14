"""Actual frozen B1/B2 full/compact synthetic feasibility tests, not source1299 qualification.

This separately authored one-effect fixture isolates the existing scalar image
relation and literal PR protocol. Its fixture signatures are not independent
root research authority and must never be used as a current1299 native proof.
"""
import sys,json,copy,hashlib,datetime
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'same-image-pr-review11870-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(Path.cwd())]
import photo_candidate_corpus as c,photo_candidate_realizations as r,photo_semantic_evidence as n,photo_search_layout as layout,photo_global_index,photo_role_proposals,photo_slot_semantics,prompt_generator as g,audit_composed_prompt
from tests.test_photo_semantic_evidence import A,source,fact,seal,core,assertion
from tests.test_photo_native_source_guards_v2 import selected_map,choices
from tests.test_photo_native_owner_selection import sign_core
from tests.photo_native_schema import slot
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
assert Path(n.__file__).resolve()==G/'scripts/photo_semantic_evidence.py'
text='On one independently declared existing image select macro shot scale of the independently declared existing physical item. The existing item already visible in that same selected image remains visible there. Its independently frozen framing.visible_in relation must point to the same selected actual image, together with separate literal visible state. No other image or physical presence alone suffices. This isolated source does not add an item or select handoff, hands-only coverage or anatomy.'
facts=[fact('itemP','subject','item','entity.presence','prerequisite','present',[],quote='independently declared existing physical item'),fact('imageP','subject','image','entity.presence','prerequisite','present',[],quote='independently declared existing image'),fact('visiblePR','framing','item','subject.visibility','preservation','visible',['itemP','imageP'],quote='existing item already visible in that same selected image remains visible there'),fact('macroE','framing','image','shot.scale','effect','macro',['itemP','imageP','visiblePR'],quote='select macro shot scale',operation='set_value',receivers=['item'])]
data=source(text,facts,{'fixture_shot':slot('fixture_shot',['framing'],property_prefixes=['shot.scale'])},{'base':selected_map('item','image')})
ep=lambda t:{'kind':'source_target','candidate_id':A,'target':t}
data['candidates'][A]['conditions']={'native_guards':{'schema':'photo-native-source-guards/v3','rules':[{'id':'item_visible_in_selected_image','kind':'frozen_entity_relation','left':ep('item'),'right':ep('image'),'dimension':'framing','property':'framing.visible_in','value_type':'entity.owner_id/v1'}]}}
seal(data,{'fixture_shot':['macroE']});c.validate(data)

def make_core(relation_image='I',visibility='visible',*,alias=True,drop_relation=False,drop_visibility=False,drop_item=False,drop_image=False,relation_type='entity.owner_id/v1',wrong_active_span=False,lie_value_about_I2=False):
 target_text='I2'if lie_value_about_I2 else relation_image
 sentence='X is currently '+visibility+' in '+target_text+'. Its framing.visible_in relation points exactly to '+target_text+'.'
 heading='Independent controlled request: physical item X and images I, I2 and I_alias are separately declared existing and present. I and I2 are explicitly disjoint. '
 tail=('I_alias is an explicitly declared equivalent identifier for I. 'if alias else'I_alias is separately declared; no equivalence to I is supplied. ')+'Macro shot-scale selection remains open. The I2-only region of this request names the separately present second image I2.'
 baseline=heading+sentence+' '+tail
 frozen=core(['X','I','I2','I_alias'],role_bindings={},open_dimensions=['framing'])
 frozen['baseline_prompt_en']=baseline;frozen['source_request']=baseline;frozen['subject']='Controlled item and images'
 frozen['request_binding']={'active_spans':[{'source_span_id':'request_1','text':baseline},{'source_span_id':'image2','text':sentence if lie_value_about_I2 else'The I2-only region of this request names the separately present second image I2.'}]}
 rows=frozen['semantic_assertions']
 for row in rows:row['evidence']={'meaning':heading.strip()}
 for owner in ['X','I','I2','I_alias']:
  if owner=='X'and drop_item or owner=='I'and drop_image:continue
  row=assertion('present_'+owner,'fact',owner=owner,property='entity.presence',value_type='entity.presence/v1',value='present');row['evidence']={'meaning':heading.strip()};rows.append(row)
 sep=assertion('images_distinct','disjoint',left='I',right='I2');sep['evidence']={'meaning':'I and I2 are explicitly disjoint.'};rows.append(sep)
 if alias:
  row=assertion('actual_alias','equivalent',left='I_alias',right='I');row['evidence']={'meaning':'I_alias is an explicitly declared equivalent identifier for I.'};rows.append(row)
 if not drop_visibility:
  row=assertion('literal_visibility','fact',dimension='framing',owner='X',property='subject.visibility',value_type='subject.visibility/v1',value=visibility);row['evidence']={'meaning':sentence};rows.append(row)
 if not drop_relation:
  row=assertion('visible_in_actual_image','fact',dimension='framing',owner='X',property='framing.visible_in',value_type=relation_type,value=relation_image);row['evidence']={'meaning':sentence}
  if wrong_active_span or lie_value_about_I2:row['source_span_ids']=['image2']
  rows.append(row)
 frozen['intent_lock']={'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','identity','age','event','concept','count'],'open_dimensions':['framing'],'semantic_anchors':[{'dimension':'framing','target':'X','property':'subject.visibility'},{'dimension':'framing','target':'X','property':'framing.visible_in'}]}
 return sign_core(frozen)

def entries(frozen,image='I'):
 selected=choices(data,frozen,{'item':'X','image':image})
 return [('full',c.entry(data,A,realization_id='base',owner_selections=selected)),('compact',c.entry({**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}},A,realization_id='base',owner_selections=selected))]
outcomes=[];boundary=[];complete=[]
cases=[('same_I',{},'I',True),('same_I2',{'relation_image':'I2'},'I2',True),('explicit_alias',{'relation_image':'I_alias'},'I',True),('same_item_other_image',{'relation_image':'I2'},'I',False),('missing_relation',{'drop_relation':True},'I',False),('missing_literal_PR',{'drop_visibility':True},'I',False),('hidden_PR_contradiction',{'visibility':'hidden'},'I',False),('missing_item_presence',{'drop_item':True},'I',False),('missing_image_presence',{'drop_image':True},'I',False),('wrong_relation_value_type',{'relation_type':'framing.visible_in/v1'},'I',False),('same_name_no_equivalence',{'relation_image':'I_alias','alias':False},'I',False)]
for name,kwargs,image,expected in cases:
 frozen=make_core(**kwargs)
 for wire,entry in entries(frozen,image):
  admission=n.admission(entry,frozen);eligible=g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry)
  assert admission['allowed']==expected,(name,wire,admission)
  assert eligible==expected,(name,wire,'consumer',eligible)
  row={'name':name,'wire':wire,'expected_admission':expected,'actual_admission':admission,'actual_core_entry_eligible':eligible,'fixture_core_sha256':frozen['canonical_sha256'],'actual_1299_source_or_authority_used':False};outcomes.append(row)
  if name in ['same_I','same_item_other_image','hidden_PR_contradiction']and wire=='full':complete.append({'name':name,'core':frozen,'entry':entry,'admission':admission})
# Actual legacy property lock stays separate from eligibility and is never waived.
frozen=make_core();frozen['intent_lock']['semantic_anchors'].append({'dimension':'framing','target':'I','property':'shot.scale'});sign_core(frozen)
for wire,entry in entries(frozen):
 admission=n.admission(entry,frozen);eligible=g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry)
 assert admission['allowed']and not eligible;outcomes.append({'name':'original_macro_property_lock','wire':wire,'expected_admission':True,'actual_admission':admission,'expected_core_entry_eligible':False,'actual_core_entry_eligible':eligible})
# Deliberately false trusted core assertion: existing code cannot prove natural
# language fact truth or exact active-span semantics merely from matching tuples.
for name,kwargs in [('unrelated_but_active_source_span',{'wrong_active_span':True}),('I2_source_span_but_falsely_typed_I',{'lie_value_about_I2':True})]:
 frozen=make_core(**kwargs)
 for wire,entry in entries(frozen):
  a=n.admission(entry,frozen);assert a['allowed'];boundary.append({'name':name,'wire':wire,'actual_admission':a,'mechanically_matches_tuple':True,'semantically_valid_independent_core_witness':False,'not_a_safety_or_actual1299_approval':True})
 if name=='I2_source_span_but_falsely_typed_I':complete.append({'name':name,'core':frozen,'entry':entries(frozen)[0][1],'admission':boundary[-2]['actual_admission']})
def pin(p):return {'file':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
modules={name:pin(Path(m.__file__).resolve())for name,m in sys.modules.items()if getattr(m,'__file__',None)and(name.startswith('photo_')or name in ['prompt_generator','audit_composed_prompt'])}
assert all(str(G)in v['file']for v in modules.values()),modules
x={'schema':'same-image-PR-frozen-synthetic-experiment/v1','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'synthetic_only_source_full':data,'actual_safety_cases':outcomes,'actual_trusted_core_semantic_boundaries':boundary,'complete_examples':complete,'actual_loaded_modules':modules,'source1299_proof_qualified_or_resigned':False,'actual_original_E3_source_was_not_test_fixture':True,'validation_boundary':'Actual frozen native schema/B1/B2 full/compact admission and core_entry_eligible for independently authored one-E synthetic module fixture only. No actual1299 proof, source root authority, normalized workflow freeze, envelope integration, final output preservation or operating validation.','network_denied':True,'API_keys_absent':True,'production_source_Git_model_network_changes':0};p=O/'GUARD-EXPERIMENT-v2.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('safety_cases',len(outcomes),'semantic_boundary_probes',len(boundary),'canon',c.digest(x))
