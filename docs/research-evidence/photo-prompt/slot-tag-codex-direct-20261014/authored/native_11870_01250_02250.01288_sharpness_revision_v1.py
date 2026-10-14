"""Fresh 1288 acuity amendment. Old50 remain immutable; no full native proof."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored'
prior=A/'native_11870_01250_02250.01250_01300.draft_v1.json'
assert hashlib.sha256(prior.read_bytes()).hexdigest()=='78b85ff916d60bff1b98382443f5ab13da27f46a14029d9d3603ac189c7abd32'
D=json.loads(prior.read_text());before=next(x for x in D['rows'] if x['ordinal']==1288)
cp=R/'CATALOG-FINAL-142-V2.json';CAT=json.loads(cp.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert sha(CAT)=='0d7cab7b4add7279b0faa629bb5df72829da0c756adc6db21dcd7c09d56b971f'
after=copy.deepcopy(before['source_proposal'])
after['effects']={'dimensions':['camera'],'properties':[
 {'dimension':'camera','target':'camera','property':'camera.movement'},
 {'dimension':'camera','target':'image','property':'image.motion.blur'},
 {'dimension':'camera','target':'image','property':'image.sharpness.subject'}]}
# Authored explicitly after rereading original/previous complete source and four
# complete current specs. Sharpness names image acuity, not a focal plane.
contract=after['content']['application_contract']
def fact(id,pointer,quote,dimension,target,prop,mode,namespace,value,requires,operation,receivers):
 f={'id':id,'realization_id':'base','pointer':pointer,'quote':quote,'dimension':dimension,'target':target,'property':prop,'mode':mode,'value':{'type':namespace,'value':value},'requires':requires}
 if mode=='effect':f.update(operation=operation,receivers=receivers)
 return f
facts=[
 fact('camera__application_contract','/content/application_contract',contract,'camera','camera','camera.presence','prerequisite','camera.presence/v1','present',[],None,None),
 fact('image__application_contract','/content/application_contract',contract,'composition','image','image.presence','prerequisite','image.presence/v1','present',[],None,None),
 fact('subject__application_contract','/content/application_contract',contract,'subject','subject','entity.presence','prerequisite','entity.presence/v1','present',[],None,None),
 fact('pan__en','/content/en','panning motion blur with the subject sharp','camera','camera','camera.movement','effect','camera.movement/v1','panning',['camera__application_contract'],'set_value',[]),
 fact('blur__en','/content/en','panning motion blur with the subject sharp','camera','image','image.motion.blur','effect','image.motion.blur/v1','panning_motion_blur',['camera__application_contract','image__application_contract','subject__application_contract'],'set_value',[]),
 fact('sharp__en','/content/en','panning motion blur with the subject sharp','camera','image','image.sharpness.subject','effect','image.sharpness.subject/v1','declared_subject_sharp',['image__application_contract','subject__application_contract'],'set_value',['subject']),
 fact('pan__ko','/content/ko','panning motion blur with the subject sharp','camera','camera','camera.movement','effect','camera.movement/v1','panning',['camera__application_contract'],'set_value',[]),
 fact('blur__ko','/content/ko','panning motion blur with the subject sharp','camera','image','image.motion.blur','effect','image.motion.blur/v1','panning_motion_blur',['camera__application_contract','image__application_contract','subject__application_contract'],'set_value',[]),
 fact('sharp__ko','/content/ko','panning motion blur with the subject sharp','camera','image','image.sharpness.subject','effect','image.sharpness.subject/v1','declared_subject_sharp',['image__application_contract','subject__application_contract'],'set_value',['subject']),
 fact('pan__application_contract','/content/application_contract',contract,'camera','camera','camera.movement','effect','camera.movement/v1','panning',['camera__application_contract'],'set_value',[]),
 fact('blur__application_contract','/content/application_contract',contract,'camera','image','image.motion.blur','effect','image.motion.blur/v1','panning_motion_blur',['camera__application_contract','image__application_contract','subject__application_contract'],'set_value',[]),
 fact('sharp__application_contract','/content/application_contract',contract,'camera','image','image.sharpness.subject','effect','image.sharpness.subject/v1','declared_subject_sharp',['image__application_contract','subject__application_contract'],'set_value',['subject'])]
owners={'base':{'schema':'photo-native-owner-bindings/v2','bindings':[
 {'target':'camera','core_role':'recording_camera','origin':'existing','introduced_by':None},
 {'target':'image','core_role':'image','origin':'existing','introduced_by':None},
 {'target':'subject','core_role':'main_subject','origin':'existing','introduced_by':None}]}}
roles=[
 {'tag':'camera_movement','spec_sha256':sha(CAT['camera_movement']),'scope':'whole_record','realization_ids':['base'],'fact_refs':['pan__en'],'support_modes':['effect'],'conditions':{'subject_applicability':{}},'role':'optional','semantic_role':'direct','weight':.9,'intent':'Explicit panning capture movement, distinct from subject motion and image blur.'},
 {'tag':'motion_rendering','spec_sha256':sha(CAT['motion_rendering']),'scope':'whole_record','realization_ids':['base'],'fact_refs':['blur__en'],'support_modes':['effect'],'conditions':{'subject_applicability':{}},'role':'optional','semantic_role':'direct','weight':.9,'intent':'Explicit recorded panning motion blur on image, not a physical subject trajectory.'},
 {'tag':'image_detail','spec_sha256':sha(CAT['image_detail']),'scope':'whole_record','realization_ids':['base'],'fact_refs':['sharp__en'],'support_modes':['effect'],'conditions':{'subject_applicability':{}},'role':'optional','semantic_role':'direct','weight':.85,'intent':'Subject sharp states image acuity/edge result on the existing image. No optical focal-plane mechanism or named-plane priority is added.'}]
units=[
 {'realization_id':'base','pointer':'/content/en','quote':after['content']['en'],'fact_refs':['pan__en','blur__en','sharp__en'],'disposition':'semantic'},
 {'realization_id':'base','pointer':'/content/ko','quote':after['content']['ko'],'fact_refs':['pan__ko','blur__ko','sharp__ko'],'disposition':'semantic'},
 {'realization_id':'base','pointer':'/content/application_contract','quote':contract,'fact_refs':['camera__application_contract','image__application_contract','subject__application_contract','pan__application_contract','blur__application_contract','sharp__application_contract'],'disposition':'semantic'}]
fs={f['id']:f for f in facts}
for f in facts:
 assert f['quote']==after['content'][f['pointer'].split('/')[-1]]
 assert all(fs[ref]['mode']=='prerequisite' for ref in f['requires'])
 assert f['mode']!='effect' or f['operation']=='set_value'
assert {(f['dimension'],f['target'],f['property']) for f in facts if f['mode']=='effect'}=={(x['dimension'],x['target'],x['property']) for x in after['effects']['properties']}
for role in roles:
 spec=CAT[role['tag']]
 for ref in role['fact_refs']:
  f=fs[ref];assert f['dimension'] in spec['dimensions']
  assert any(f['property']==p.rstrip('.') or f['property'].startswith(p if p.endswith('.') else p+'.') for p in spec['property_prefixes'])
assert all('focus.' not in f['property'] and f.get('operation')!='select_plane' for f in facts)
assert after['conditions']==before['source_before']['conditions']=={}
source_changes=[
 {'pointer':'/content/application_contract','before':None,'after':contract,'reason':'Explicitly require independently declared existing camera/image/subject addresses; no added entity or subject movement. These still require actual prerequisite/core-role consumption in the later full-v4 proof.'},
 {'pointer':'/effects','before':before['source_before']['effects'],'after':after['effects'],'reason':'Original composition-only routing footprint is refined to actual panning camera movement, image motion blur and subject-bounded recorded acuity. Sharpness is set_value, not optical plane selection or preservation.'}]
packet={'schema':'native-direct-manual-draft-amendment/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','ordinal':1288,'candidate_id':before['candidate_id'],'before_authored_file':str(prior),'before_authored_file_bytes_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),'before_authored_row_sha256':sha(before),'source_sha256':D['source_sha256'],'catalog_sha256':sha(CAT),'original_source_full':before['source_before'],'previous_frozen_source_proposal_full':before['source_proposal'],'new_exact_source_after':after,'new_exact_source_after_sha256':sha(after),'source_corrections_from_before5B':source_changes,'source_delta_from_previous_frozen_proposal':[{'pointer':'/effects','before':before['source_proposal']['effects'],'after':after['effects'],'reason':'Remove focal-plane claim while retaining panning/blur and subject receiver; record subject image acuity explicitly.'}],'native_fact_draft':facts,'owner_maps_draft':owners,'source_units_draft':units,'proposed_roles_and_binding_intent':roles,'rejected_roles':{'focus':'No focal plane or priority/relative sharpness of named planes is declared. Sharp subject alone names a recorded acuity result.','composition':'No independent arrangement clause is stated in the positive source.'},'actual_rids':['base'],'required_cid_closure':{},'member_binding_closure':{},'old_own_binding_full':before['existing_own_bindings_full'],'own_binding_review':'Old composition optional/direct/weight1/empty applicability is display policy, not intrinsic source meaning. The three newly proposed roles each have deliberately unrestricted current applicability; no original source guard is removed. Existing typed camera/image/subject and receiver linkage remain mandatory.','source_proposal_whole_reread_complete':False,'full_native_proof':None,'native_signature':None,'formal_root_input_rebind_required':True,'local_checks':'Only explicit source/fact quote, dependency, effect and spec-dimension/prefix shape checks; no full-v4 proof validation, core witness, parity, registration or operation.'}
out=A/'native_11870_01250_02250.01288_sharpness_revision_pre_reread_v1.json';assert not out.exists();out.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n');print(str(out));print('PRE_REREAD_SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
