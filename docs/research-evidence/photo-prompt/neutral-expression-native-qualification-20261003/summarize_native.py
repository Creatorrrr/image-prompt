"""Join three independent arms after root inspection of their original pixels."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import struct

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
EV=HERE.parent/'neutral-expression-integration-20261003'
REFERENCE=Path('/tmp/codex-remote-attachments/01a0fd79-2285-74a3-aa0a-d730ee5f3d68/4534277A-EC33-4F2A-A046-29E8AB66DBBE/1-사진-1.jpg')

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

CONFIG={
 'a':{'concept':'비가 그친 골목 제본 수리실','keywords':['plump: 아래배 국소 볼륨','curvaceous: 지정 몸통 옆선','fleshy: 위팔 살집'],'image':'generated_images/arm-a-book-repair-20261003T032108Z/native.png','prompt':'prompt_en.txt','negative':'negative_en.txt','freeze':'precore_freeze_manifest.json','initial_review':'supplemental_pixel_review.json','hard_review':'native_hard_gate_review.json','hard_audit':'native_hard_gate_review_audit.json','runtime_args':'native_tool_args.json','runtime_audit':'native_render_request_audit.json','composed_audit':'composed_audit.stdout.json','ledger':'runs/image_runs.ndjson','ordinary':['slot:silhouette_proportion:ne_regional_soft_volume','slot:silhouette_proportion:ne_regional_contour_transition'],'parent_observation':'위팔의 둥근 살집과 제본 책/실 접촉은 관찰된다. 아래배 앞쪽의 니트 수평 주름은 몸의 볼륨과 분리하기 어렵다. 가까운 팔이 지정 옆선을 가려 lower-rib→flank→lower-belly의 안/밖 곡선과 연속성을 모두 확인할 수 없다. 이 부분과 가림을 FAIL로 판정한 agent 결과에 동의한다.'},
 'b':{'concept':'저녁 산업 광학 시험실의 분할 거울·원형 짐벌','keywords':['willowy: 몸통 대비 긴 사지','slender: 좁은 가로 폭','sinewy: 얕은 팔 근육·힘줄 윤곽'],'image':'generated_images/optical-bay-attempt-01.png','prompt':'standalone_prompt_en.txt','negative':'standalone_negative_en.txt','freeze':'freeze_manifest.json','initial_review':'pixel_test_review.json','hard_review':'render_review.json','hard_audit':'render_review_audit.json','runtime_args':'native_image_args.json','runtime_audit':'runtime_audit.json','composed_audit':'composed_audit.json','ledger':'image_runs.ndjson','ordinary':['slot:silhouette_proportion:willowy_long_limb_proportion','slot:silhouette_proportion:bm_wiry_definition'],'parent_observation':'머리부터 양발이 들어온 프레임에서 몸통과 긴 다리/가까운 팔의 비율 및 좁은 팔다리 윤곽이 읽힌다. 팔은 조명 그라데이션이 주된 표면 단서로 근육·힘줄 경계를 분리하기 어렵다. 두 접촉 손 중 조절 휠 손이 가슴 높이에 있어 양손의 허리 높이 조건을 충족하지 않는다. 거울과 시험실은 보이지만 새로 놓은 작은 부품을 기존 장치에서 특정하기 어렵다. 해당 FAIL 판정에 동의한다.'},
 'c':{'concept':'시장 위 옥상 판화실의 종이등·가죽 파우치·도자기','keywords':['pouty: 현재 전방 입술 내밂','side-eye: 종이등 방향 눈동자','smooth: 피부와 도자기 각각의 표면','supple: 가죽 입구의 현재 굽힘'],'image':'generated_image.png','prompt':'prompt_en.txt','negative':'negative_en.txt','freeze':'freeze_manifest.json','initial_review':'independent_pixel_review.json','hard_review':'render_review.json','hard_audit':'render_review_audit.json','runtime_args':'native_tool_args.json','runtime_audit':'native_request_audit.json','composed_audit':'composed_audit.json','ledger':'image_runs.ndjson','ordinary':['slot:gaze_engagement:pv_side_eye'],'parent_observation':'거의 정면인 얼굴에 대해 두 눈동자가 화면 오른쪽 위 종이등으로 치우친다. 작은 둥근 입 틈과 입술 전방 내밂/모인 양끝이 읽힌다. 피부의 미세결을 남긴 빛 전이는 단단한 도자기 유약 반사와 구별되고, 엄지가 닿은 가죽 윗입구의 굽힘과 연결된 fold가 보인다. 정한 현재 관찰 gate의 PASS에 동의한다. 세로 방향보다 거의 정사각형인 출력, 도자기를 감싸 쥔 손, 낡은 파우치 아랫면은 별도 장면 차이로 보존한다. 복원성·반복 탄성은 판정하지 않는다.'},
}

def main():
    ops=read(EV/'OPERATIONAL-INPUTS.json')
    mismatches=[r['path'] for r in ops['inputs'] if sha(Path(r['path']))!=r['sha256']]
    assert not mismatches,mismatches
    rows=[]
    for arm,c in CONFIG.items():
        folder=HERE/f'arm-{arm}';image=folder/c['image'];raw=image.read_bytes()
        assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        dimensions=list(struct.unpack('>II',raw[16:24]));digest=sha(image)
        freeze=read(folder/c['freeze']);frozen=freeze.get('file_sha256',freeze.get('files'));drift=[]
        for name,v in frozen.items():
            path=Path(v['path']) if isinstance(v,dict) else folder/name
            expected=v['sha256'] if isinstance(v,dict) else v
            if sha(path)!=expected:drift.append(name)
        assert not drift,(arm,drift)
        manifest=read(folder/'run_manifest.json')
        assert manifest['image_call_count']==1 and manifest['cross_arm_inputs_used'] is False
        assert manifest['image_hashes']==[{'path':str(image),'sha256':digest}]
        assert manifest['reference_sha256']==[sha(REFERENCE)]
        initial=read(folder/c['initial_review']);hard=read(folder/c['hard_review']);audit=read(folder/c['hard_audit'])
        assert initial['result_sha256']==hard['result_sha256']==digest
        hard_gates=hard['hard_gates'];assert set(hard_gates)==set(audit['required_hard_gates'])
        assert audit['schema_failures']==[]
        initial_failed=[g['gate_id'] for g in initial['gates'] if g['status']!='pass']
        hard_failed=[k for k,v in hard_gates.items() if v['status']!='pass']
        assert audit['technical_qualified']==(not hard_failed)
        runtime=read(folder/c['runtime_audit']);composed=read(folder/c['composed_audit']);args=read(folder/c['runtime_args'])
        assert runtime['status']==composed['status']=='pass'
        runtime_sha=hashlib.sha256(args['prompt'].encode()).hexdigest()
        assert runtime_sha[:16]==runtime['runtime_prompt_id']
        assert args['referenced_image_paths']==[str(REFERENCE)]
        assert runtime['selected_visual_concept_ids']==manifest['chosen_visual_concept_ids']
        ledger_rows=[json.loads(line) for line in (folder/c['ledger']).read_text().splitlines() if line.strip()]
        assert any(r.get('run_id')==manifest['ledger_run_id'] for r in ledger_rows)
        rows.append({'arm':arm.upper(),'concept_ko':c['concept'],'synthetic_test_author':'independent_arm_agent','tested_keywords':c['keywords'],'core_inputs_frozen_before_project_data_access':True,'frozen_files_checked':len(frozen),'frozen_input_mismatches':[],'cross_arm_inputs_used':False,'operational_manifest_sha256':sha(EV/'OPERATIONAL-INPUTS.json'),'pack_id':manifest['pack_id'],'normalized_core_sha256':manifest['authorial_core_sha256'],'intent_lock_sha256':manifest['intent_lock_sha256'],'ordinary_candidates_adopted':c['ordinary'],'optional_visual_concepts_adopted':manifest['chosen_visual_concept_ids'],'prompt_path':str((folder/c['prompt']).relative_to(ROOT)),'prompt_sha256':sha(folder/c['prompt']),'runtime_prompt_sha256':runtime_sha,'negative_path':str((folder/c['negative']).relative_to(ROOT)),'composition_audit':'PASS','exact_runtime_audit':'PASS','native_image_path':str(image.relative_to(ROOT)),'native_image_sha256':digest,'native_dimensions':dimensions,'actual_native_call_count':1,'native_generation_status':'success','observed_native_model':'unknown','initial_frozen_gates':{'pass':len(initial['gates'])-len(initial_failed),'total':len(initial['gates']),'failed_ids':initial_failed},'adopted_profile_and_embodiment_gates':{'pass':len(hard_gates)-len(hard_failed),'total':len(hard_gates),'failed_ids':hard_failed,'schema_failures':[]},'overall_strict_keyword_case_result':'PASS' if not initial_failed and not hard_failed else 'FAIL','parent_original_native_inspection':True,'parent_agrees_with_agent_gate_results':True,'parent_observation':c['parent_observation'],'partial_is_fail':True,'user_aesthetic_acceptance':'pending','ledger_run_id':manifest['ledger_run_id'],'arm_report_audit':str((folder/c['hard_audit']).relative_to(ROOT))})
    report={'schema_version':'neutral-independent-native-qualification/v1','execution_complete':True,'independent_agents':3,'actual_native_image_calls':3,'saved_original_images':3,'operational_files_checked':len(ops['inputs']),'operational_input_mismatches':mismatches,'image_cases_passed':sum(r['overall_strict_keyword_case_result']=='PASS' for r in rows),'image_cases_failed':sum(r['overall_strict_keyword_case_result']=='FAIL' for r in rows),'image_cases_blocked':0,'initial_frozen_gates_passed':sum(r['initial_frozen_gates']['pass'] for r in rows),'initial_frozen_gate_count':sum(r['initial_frozen_gates']['total'] for r in rows),'derived_gates_passed':sum(r['adopted_profile_and_embodiment_gates']['pass'] for r in rows),'derived_gate_count':sum(r['adopted_profile_and_embodiment_gates']['total'] for r in rows),'gate_count_boundary':'Independent and derived conditions overlap semantically; their counts are separate, not independent quality samples.','arms':rows,'scope_boundary':'This proves normal V6 exposure, optional adoption, exact audited reference/prompt binding and three current original-pixel observations. No before/after generation ablation or universal keyword reliability is claimed. Native generation success, pixel qualification and user acceptance are separate.','reference_scope':'Visible face and hair only; adult age roles body and events are explicitly synthetic arm authorship.'}
    save(HERE/'ROOT-INDEPENDENT-PIXEL-REVIEW.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='arms'},ensure_ascii=False))

if __name__=='__main__':main()
