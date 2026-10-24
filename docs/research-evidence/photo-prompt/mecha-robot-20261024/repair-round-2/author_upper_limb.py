from pathlib import Path
import json,copy,hashlib,uuid,shutil,subprocess
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;S=R/'skills/photo-prompt-image-generator';A=S/'assets'
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert not (O/'source-change.json').exists(),'Already authored; preserve evidence'
files=['photo_candidate_mecha_robot_20261024.json','photo_candidate_mecha_robot_bindings_20261024.json','photo_mecha_robot_semantics_20261024.json']
write(O/'working-source-before.json',{f:read(A/f) for f in files})
cfg=read(S/'retrieval-runtime.json');store=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed');N=store/'generations'/cfg['native_generation_id'];B={'config':cfg,'store':str(store),'native':str(N),'h_f2':str(store/'h-f2-generations'/cfg['generation_id'])};write(O/'before.json',B)
ns=uuid.UUID('8b9ba548-98ca-4baa-9556-3ce444246ba6');cid='cand_'+uuid.uuid5(ns,'mecha-robot:A12').hex
proposal="An adult wears an external support along one arm over clothing. A shoulder harness joins an exposed rigid bracket fixed to an upper-arm cuff; an external elbow hinge links that cuff to a forearm cuff, with the human wrist visibly distinct beyond the cuff."
ko='성인이 옷 바깥으로 한쪽 팔을 따라 외부 지지 구조를 착용한다. 어깨 하네스는 위팔 커프에 고정된 노출된 단단한 브래킷과 이어지고, 외부 팔꿈치 경첩이 위팔 커프와 아래팔 커프를 연결하며 사람의 손목은 커프 끝 너머에서 구분되어 보인다.'
relations=[('frame','outside','adult_arm'),('harness','joins','bracket'),('bracket','fixed_to','upper_arm_cuff'),('upper_arm_cuff','joins','elbow_hinge'),('elbow_hinge','joins','forearm_cuff'),('human_wrist','part_of','adult_arm'),('human_wrist','beyond','forearm_cuff')]
card={'id':'A12','title_ko':'상지 착용 프레임의 노출된 연결 경로','family':'A','seed_term_fragments':['외골격','상지 보조 프레임'],'source_ids':['S11'],'proposal_en':proposal,'proposal_ko':ko,'owners':['adult_arm','frame','harness','bracket','upper_arm_cuff','elbow_hinge','forearm_cuff','human_wrist'],'directed_relations':[{'from':a,'predicate':b,'to':c} for a,b,c in relations],'confusion_boundaries_ko':['하체 외골격을 상지 프레임으로 오인','갑옷 소매와 외부 지지 구조 혼동','어깨 끈과 위팔 커프 사이 숨은 연결을 추정','사람 손목과 기계 말단 소유자 혼합'],'claim_limit_ko':'연결 경로의 외형만 제안한다. 실제 동력·하중 보조·의료 효과·신체 개조·특정 제조사 모델의 재현은 입증하지 않는다.','proposed_slots':['object_structure','body_form','contact_point'],'basis':'authored_visual_repair_variant_informed_by_existing_component_distinctions','source_support_scope':'Bounded wearable-versus-biological augmentation distinction only. Exact upper-limb bracket/cuff geometry is authored, not a manufacturer model claim.','priority':'P0','view_requirement':'The same harness root, bracket, both cuffs, external hinge and distinct human wrist must be identifiable together at the original saved scale. Adjacent straps do not prove a hidden bracket.','detail_gate':'Review whole original and native pixels; partial or unobservable cannot pass.','native_approval':False,'automatic_activation':False,'runtime_registration':True,'source_image_review':'NOT_RUN_FOR_THIS_REALIZATION','pixel_status':'NOT_RUN','language_review':'paired authored EN/KO; full text preserved, independent review pending','candidate_id':cid,'registration_status':'authored_source_module','integration_status':'optional_visual_source'}
card['render_gates']=[{'id':'A12-C0','kind':'complete_realization','required_en':proposal,'required_ko':ko,'partial_is_fail':True,'unobservable_policy':'UNOBSERVABLE_NOT_PASS','status':'NOT_RUN'}]+[{'id':f'A12-R{i}','relation':e,'both_endpoints_required':True,'partial_is_fail':True,'unobservable_policy':'UNOBSERVABLE_NOT_PASS','status':'NOT_RUN'} for i,e in enumerate(card['directed_relations'],1)]
module=read(A/files[0]);template=module['candidates']['cand_0eb3c2c02e9c54c2a092062b880ba007'];record={'id':cid,'record_kind':'visual_option','content':{'en':proposal,'ko':ko,'definition':'Wearable upper-limb exoskeleton with an exposed harness-to-cuff linkage. '+proposal,'aliases':['상지 착용 프레임의 노출된 연결 경로','upper-limb wearable external support frame'],'application_contract':template['content']['application_contract'],'research_semantics':copy.deepcopy(card)},'conditions':{},'effects':copy.deepcopy(template['effects']),'provenance':[{'source':'Authored upper-limb visible-connection repair variant of mecha research A05 component distinction; bounded wearable-versus-biological augmentation context https://www.cyberdyne.jp/en/products/about-hal; exact mechanism authored, no manufacturer reproduction claim.','sha256':hashlib.sha256((O/'request.txt').read_bytes()).hexdigest()}]}
assert cid not in module['candidates'];module['candidates'][cid]=record;write(A/files[0],module)
bindings=read(A/files[1]);catalog=read(A/'photo_candidate_slot_catalog.json')['slot_catalog'];newbind={}
for slot in card['proposed_slots']:
 bid='bind_'+uuid.uuid5(ns,cid+':'+slot).hex
 newbind[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':catalog[slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
bindings['slot_bindings'].update(newbind);write(A/files[1],bindings)
registry=read(A/files[2]);registry['cards'].append(card)
# The lower-limb card stays unchanged; original broad routes remain advisory.
write(A/files[2],registry)
write(O/'new-native-records.json',{cid:record});write(O/'changed-native-records.json',{});write(O/'new-bindings.json',newbind)
write(O/'source-change.json',{'new_card':'A12','new_candidate':cid,'new_positive_records':1,'new_optional_bindings':len(newbind),'existing_candidate_changes':0,'old_A05_is_lower_limb_not_upper_limb':True,'ordinary_search_sampling_policy_changed':False,'native_approval':False})
# Copy an immutable current baseline; model files must be regular, Python env only may link.
stage=O/'successor-skill';manifest=read(N/'manifest.json')
for rel,row in manifest['members'].items():
 target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(N/rel,target)
 expected=row['sha256'] if isinstance(row,dict) else row;assert hashlib.sha256(target.read_bytes()).hexdigest()==expected
lock=read(S/'embedding-runtime.lock.json')
for rel,row in lock['files'].items():
 p=stage/lock['package']/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/lock['package']/rel,p);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
(stage/'.runtime/embedding-python').symlink_to(S/'.runtime/embedding-python',target_is_directory=True)
# Reuse verified maintenance builder, preserving all existing module records/bindings.
source=(O.parent/'integration-evidence/build_release.py').read_text()
source=source.replace("write(STAGE/'assets'/module,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':{cid:new[cid] for cid in fresh}})","module_body=read(STAGE/'assets'/module);module_body['candidates'].update({cid:new[cid] for cid in fresh});write(STAGE/'assets'/module,module_body)")
source=source.replace("binding_data=read(binding_source);binding_data['schema']=c.MODULE_SCHEMAS['slot_bindings']","binding_data=read(STAGE/'assets'/binding_module);binding_data['slot_bindings'].update(read(O/'new-bindings.json'));binding_data['schema']=c.MODULE_SCHEMAS['slot_bindings']")
(O/'build_release.py').write_text(source)
install=(O.parent/'integration-evidence/install_release.py').read_text();install=install.replace("ROOT=O.parents[4]","ROOT=O.parents[4]");(O/'install_release.py').write_text(install)
print(json.dumps(read(O/'source-change.json')),flush=True)
