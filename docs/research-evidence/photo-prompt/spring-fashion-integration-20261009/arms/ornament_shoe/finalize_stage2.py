import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ARM=Path(__file__).resolve().parent
def read(path): return json.loads(Path(path).read_text())
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(name,value): (ARM/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

state=read(ARM/'run/workflow.json');artifacts=state['artifacts']
assert state['phase']=='review_record_validated' and state['technical_qualification']=='fail'
assert sha(artifacts['freeze_receipt']['path'])=='68bec324c559647921cb4fed7bf1273c7222ec0632a3c0dac371a25b3ea190fe'
freeze_receipt=read(artifacts['freeze_receipt']['path'])
for role,expected_sha in freeze_receipt['files'].items():
    assert artifacts[role]['sha256']==expected_sha and sha(artifacts[role]['path'])==expected_sha
receipt=read(artifacts['runtime_receipt']['path'])
assert receipt['generation_id']=='a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c'
assert receipt['source_fingerprint']=='6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a'
composed=read(artifacts['composed']['path']);audit=read(artifacts['composed_audit']['path'])
runtime_audit=read(artifacts['runtime_audit']['path']);review_audit=read(artifacts['review_audit']['path'])
visual=review_audit['visual'];assert visual['schema_failures']==[] and visual['technical_qualified'] is False
meta=read(ARM/'native-result-metadata.json');topic=read(ARM/'new-topic-pixel-review.json')
gates=read(ARM/'exact-hard-gate-checklist.json');baseline=read(ARM/'baseline-supplemental-pixel-review.json')
rows=[json.loads(x) for x in (ARM/'image_runs.ndjson').read_text().splitlines() if x.strip()]
assert len(rows)==1 and rows[0]['image_call_count']==1 and meta['native_invocations']==1
assert sha(meta['saved_image'])==meta['sha256']
assert sha(artifacts['authorial_core_normalized']['path'])=='dde5df21d0b9807a7a2633330ec1bb455fd11b7232725204a9da9a52b5f0f127'
assert sha(artifacts['request_envelope_input']['path'])=='c66753a536517e5d8dcfb4d32141e8380cdfa671075f7345f923cdd23d19fa8e'
assert sha(ARM/'data-fragment.json')=='00348552889e432d79c60f482f0649ca65e2d2bbb51282353fb8c3ce8aa08124'
assert audit['status']=='pass' and runtime_audit['status']=='pass'
assert set(read(artifacts['visual_review_shape']['path'])['review']['hard_gates'])==set(gates['required_gate_ids'])

files={k:{'path':str(ARM/name),'sha256':sha(ARM/name)} for k,name in {
    'prompt':'prompt.en.txt','new_topic_plan':'new-topic-observation-plan.json','new_topic_review':'new-topic-pixel-review.json',
    'baseline_supplement':'baseline-supplemental-pixel-review.json','user_duty_review':'user-duty-pixel-review.json',
    'artistic_review':'artistic-impression-review.json','exact_hard_checklist':'exact-hard-gate-checklist.json',
    'ledger':'image_runs.ndjson','independent_manifest':'independent-run-manifest.json','manifest_validation':'independent-manifest-validation.json',
    'native_tool_result_metadata':'native-result-metadata.json','native_preinvoke_bindings':'native-preinvoke-bindings.json',
    'inspection_manifest':'inspection-manifest.json',}.items()}
result={
    'schema_version':'spring-fashion-stage2-result/v1','arm_id':'ornament_shoe','completed_at':datetime.now(timezone.utc).isoformat(),
    'status':'completed_with_pixel_failures','concept_name_ko':'비 뒤 첫 배를 기다리는 접힌 항로','concept_name_en':'Folded Routes Before the First Returning Ferry','independent_concept_seed':7825148642666662853,
    'runtime':{'store':'/Users/chasoik/.cache/image-prompt/photo-runtime-spring-fashion-20261009','generation_id':receipt['generation_id'],'source_fingerprint':receipt['source_fingerprint'],'skill_sha256':'9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b','receipt':artifacts['runtime_receipt'],'pack_id':audit['pack_id'],'pack':artifacts['pack'],'receipt_exact_READY_match':True},
    'freeze_preservation':{'authorial_core_canonical_sha256':rows[0]['authorial_core_sha256'],'intent_lock_canonical_sha256':rows[0]['intent_lock_sha256'],'request_envelope_sha256':artifacts['request_envelope_input']['sha256'],'normalized_core_file_sha256':artifacts['authorial_core_normalized']['sha256'],'unchanged':True,'verified_frozen_file_count':len(freeze_receipt['files']),'verified_frozen_roles':list(freeze_receipt['files']),'freeze_receipt':artifacts['freeze_receipt'],'other_arm_inputs_used':False,'shared_assets_or_indexes_modified_by_this_stage':False},
    'selection':{'chosen_candidate_ids':composed['chosen_candidate_ids'],'new_slot_candidate_ids':['slot:garment_detail:spf_sf071_1','slot:footwear:spf_sf107_02'],'chosen_visual_concept_ids':composed['chosen_visual_concept_ids'],'effective_visual_contract_sha256':audit['effective_visual_contract_sha256'],'new_spring_profile_ids':['spring_sf071_1','spring_sf107_02'],'new_spring_visual_concept_opt_ins_exposed':False,'spring_profile_hard_activation':'not_verified_not_promoted','authorial_optional_creation':'Sage apron over-dress over the separate apricot blouse and added solid instep straps are authorial choices on open appearance properties; they do not rewrite the user envelope or frozen core.'},
    'native_execution':{'tool':'image_gen','lane':'native','actual_image_call_count':1,'operation_id':meta['operation_id'],'ledger_run_id':rows[0]['run_id'],'ledger_row_count':1,'native_tool_origin_path':meta['observed_origin_image'],'saved_image_path':meta['saved_image'],'image_sha256':meta['sha256'],'dimensions':meta['dimensions'],'byte_identical_copy':True,'runtime_prompt_sha256':rows[0]['runtime_prompt_sha256'],'prompt_sha256':hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),'referenced_image_paths':['/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'],'reference_sha256':rows[0]['reference_sha256'],'reference_scope':'visible face and hair only','requested_model_via_native_tool':None,'observed_model':None,'additional_calls_or_API_fallback':False,'native_plan':artifacts['native_plan']},
    'audits':{'composed':{'status':audit['status'],'quality_status':audit['quality_status'],'warnings':audit['warnings'],'artifact':artifacts['composed_audit']},'runtime':{'status':runtime_audit['status'],'artifact':artifacts['runtime_audit']},'pixel_review_record':{'status':'pass','record_valid':True,'schema_failures':visual['schema_failures'],'technical_qualification':'fail','artifact':artifacts['review_audit']},'generic_review':'not_applicable_no_render_repair_contract'},
    'pixels':{'actual_effective_hard_gates':{'passed':gates['passed'],'total':gates['total'],'required_gate_ids':gates['required_gate_ids'],'failed_gate_ids':gates['failed_gate_ids'],'qualification':'fail'},'new_candidate_supplemental_all_of':{'status':topic['overall_status'],'passed':topic['passed_observations'],'total':topic['total_observations'],'candidate_results':topic['candidate_results'],'kept_outside_hard_gates':True},'requester_duties':{'status':'pass','passed':4,'total':4},'baseline_supplemental':{'status':'fail','passed':baseline['passed'],'total':baseline['total'],'failed_observation_ids':[x['observation_id'] for x in baseline['observations'] if x['status']=='fail']},'material_failure':'The clip does not visibly couple the paper corner and a wire in the same jaw; that critical endpoint is absent or occluded. Flower ownership, diagonal blouse drape and shoe-ribbon continuity also fail supplemental observation.','observation_scales':['thumbnail','native'],'final_image_bytes_unchanged':True},
    'user_judgment':state['user_judgment'], 'files':{**files,'composed':artifacts['composed'],'visual_pixel_review':artifacts['visual_review']},
    'execution_notes':['The project Python virtualenv lacked Pillow during initial save-helper preparation; no copy or ledger row was written then. The exact returned PNG was subsequently copied using standard-library byte/hash/IHDR checks, with dimensions corroborated by the bundled Pillow runtime. No image tool reinvocation occurred.','An initial metadata display mislabeled the render-request file hash as an effective contract hash; native-preinvoke-bindings.json and all managed artifacts retain the distinct correct hashes.','A supplemental review authoring key was corrected to the actual obs_reference plan ID before review audit; the frozen plans, composed prompt, core and run inputs were unchanged.']
}
save('stage2-result.json',result)
text=f'''# C 테스트케이스: 비 뒤 첫 배를 기다리는 접힌 항로

독립 난수 seed는 `7825148642666662853`이다. 첨부 참조의 보이는 얼굴·짧은 검은 머리만 사용하여, 비 뒤 선착장에서 시간표의 종이 모서리를 다시 고정하는 현재 순간을 구성했다. 장면, 의상, 소품, 카메라와 구체 기하는 authorial 선택이며 사용자 lock이 아니다. 원문 envelope와 frozen core는 그대로 유지했다.

| 검증 층 | 결과 |
| --- | --- |
| Immutable READY generation/receipt | 정확히 일치 |
| Composed / native runtime 감사 | PASS / PASS |
| Native image_gen 실제 호출 / ledger 행 | 1 / 1 |
| 기존 선택 원피스 계약 | 5/5 관찰 PASS |
| Embodiment 계약 | 3/5 PASS, 2 FAIL |
| 정확한 effective hard union | 8/10, 기술 자격 FAIL |
| 신규 bundle 보충 all-of | 10/10 관찰 PASS |
| 신규 spring 프로필 hard activation | 미노출·미검증, 승격 없음 |
| 원래 사용자 의미 4 anchor | 4/4 관찰 PASS |
| 기존 authorial 보충 관찰 | 4/9 PASS |
| 사용자 판단 | not_yet_received |

신규 선택은 `bundle:spf_sf071_1_bundle`(원본 슬롯 `spf_sf071_1`)과 `bundle:spf_sf107_02_bundle`(원본 슬롯 `spf_sf107_02`)이다. 앞판의 두 어깨끈 연결과 별도 블라우스 앞에 놓이는 층, 각 신발의 발등 스트랩 및 자기 신발의 반대편 두 끝 고정을 생성 전에 4 component + 6 directed relation 표로 고정했다. 양쪽 신발을 따로 관찰했고 partial/unobservable은 실패로 처리했다. 이 10개 보충 항목은 runtime `hard_gates`에 넣지 않았다. `spring_sf071_1`, `spring_sf107_02` 프로필은 별도 opt-in이 노출되지 않아 hard activation을 주장하지 않는다.

별도로 실제 노출된 기존 `visual-concept:one_piece_dress_construction`을 opt-in했다. Sage 앞판·허리 연결·사선 앞판·플리츠 밑단이 한 벌로 읽히며 원피스의 5개 native/thumbnail 게이트가 통과했다. 실제 exact union은 `exact-hard-gate-checklist.json`에 그대로 기록했다.

실패한 hard gate는 `embodiment_contact_and_space`, `embodiment_visibility_and_projection`이다. 손가락이 종이 모서리의 나무 클립을 잡지만, 같은 클립 턱이 와이어까지 잡는 관계와 그 끝점은 보이지 않는다. 단순히 손과 종이가 보인다는 이유로 전체 접촉을 통과시키지 않았다. 보충 관찰에서 꽃은 블라우스보다 sage 어깨끈에 붙고, 블라우스 대각선 드레이프와 신발에서 발등 X를 거쳐 발목 매듭으로 이어지는 리본 경로도 완전하게 나타나지 않았다.

전체 인상은 조용하고 따뜻한 봄 선착장 사진으로 설득력 있다. 실제 이미지는 보는 사람 쪽으로 향하는 얼굴과 게시판에 붙은 종이로 표현되어, 원래의 돌아오는 배를 향한 반응과 종이·와이어 수선 관계는 약해졌다. 예술적 인상은 기술 자격이나 사용자 수용을 대체하지 않는다.

생성 이미지: [{Path(meta['saved_image']).name}]({meta['saved_image']}) — {meta['dimensions'][0]}×{meta['dimensions'][1]}, SHA256 `{meta['sha256']}`. 도구가 실제 반환한 로컬 파일에서 byte-identical 복사했고 원본은 남겼다.

프롬프트: [prompt.en.txt]({ARM/'prompt.en.txt'}). 감사된 객체: [composed.json]({artifacts['composed']['path']}). 최종 결과: [stage2-result.json]({ARM/'stage2-result.json'}). Ledger: [image_runs.ndjson]({ARM/'image_runs.ndjson'}). 독립 manifest: [independent-run-manifest.json]({ARM/'independent-run-manifest.json'}). 정식 리뷰: [visual-pixel-review.json]({ARM/'visual-pixel-review.json'}). 신규 topic 리뷰: [new-topic-pixel-review.json]({ARM/'new-topic-pixel-review.json'}).

Runtime generation은 `{receipt['generation_id']}`, source fingerprint는 `{receipt['source_fingerprint']}`이다. 추가 재생성, API/CLI fallback, 다른 arm 입력, shared asset/index 수정은 수행하지 않았다. 이미지 검토용 crop/thumbnail은 arm 안에 별도로 두었고 최종 원본 픽셀은 변경하지 않았다.
'''
(ARM/'TESTCASE.md').write_text(text)
validation={'status':'pass','stage2_result_sha256':sha(ARM/'stage2-result.json'),'testcase_sha256':sha(ARM/'TESTCASE.md'),'managed_phase':state['phase'],'image_call_count':1,'ledger_rows':len(rows),'exact_hard_gate_set_matches_shape':True,'supplemental_plan_preinvoke_sha_matches':sha(ARM/'new-topic-observation-plan.json')==read(ARM/'native-preinvoke-bindings.json')['supplemental_plan_sha256'],'all_frozen_artifact_hashes_preserved':True,'image_hash_matches_ledger_and_manifest':True,'review_schema_valid':True,'technical_qualification':'fail','user_judgment_source':state['user_judgment']['source']}
save('stage2-validation.json',validation)
print(json.dumps({**validation,'status':'completed_with_pixel_failures','artifact_validation':'pass','stage2_result':str(ARM/'stage2-result.json'),'testcase':str(ARM/'TESTCASE.md')},ensure_ascii=False))
