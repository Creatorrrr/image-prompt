from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;read=lambda n:json.loads((p/n).read_text());sha=lambda n:hashlib.sha256((p/n).read_bytes()).hexdigest();r=read('native_result.json');m=read('run_manifest.json');kw=read('keyword_pixel_results.json');pr=read('pixel_review.json');pa=read('pixel_review_audit.json');sel=read('candidate_exposure_and_selection.json');f=read('core_freeze.json');ps=read('pixel_status_summary.json');snap=read('source_snapshot.json')
summary={'contract_version':'angle-motion-arm-summary/v1','arm':'high_angle','topic':'하이 앵글','seed':7350812925794127079,'random_staging':{'setting':'paper conservation studio','action':'pressing a paper sheet flat with a soft brush','props':'metal ruler and shallow pigment dish','lighting':'diffuse north-window daylight'},'authorial_staging_is_requester_definition':False,'requester_definition_present':False,'interpretation_basis':'agent_general_knowledge','pack_id':m['pack_id'],'run_id':m['ledger_run_id'],'prompt_id':m['prompt_id'],'runtime_prompt_id':read('runtime_audit.json')['runtime_prompt_id'],'pack_count':1,'image_call_count':1,'native_tool':'image_gen.imagegen','cli_api_fallback_count':0,'image_edit_or_regeneration_count':0,'selected_candidates':[{'id':row['candidate_id'],'reason':row['artistic_interpretation'],'prompt_evidence':row['prompt_evidence']} for row in sel['selection_records']],'selected_candidate_pixel_evidence':{
 'slot:lighting:soft_window':'Window daylight illuminates linen, paper and table in one consistent direction; broad soft shadows survive.',
 'slot:shot_scale:full_length_body_shot':'Entire seated support and both shoes remain visible, with floor margin.',
 'integration:physical_contact':'Brush bristles visibly meet the paper. The simultaneous left-palm far-corner support fails.',
 'integration:material_trace':'Uneven deckled edges and fiber flecks are visible. A locally lifted edge flattening beside the brush is not assessable.'},
 'chosen_visual_concept_ids':[],'focal_semantic_coverage':'required typed high_angle_camera assertion bound before retrieval','statuses':ps,'keyword_component_pass_count':5,'keyword_component_required_count':5,'whole_scene_component_pass_count':5,'whole_scene_component_required_count':6,'embodiment_pass_count':4,'embodiment_required_count':5,'effective_visual_gates':[],'render_review_audit':{'schema_failures':pa['schema_failures'],'qualification_status':pa['qualification_status'],'failed_hard_gates':[x['gate'] for x in pa['failed_hard_gates']]},'key_failures':['Left hand uses fingertips at the near/right paper edge rather than palm support at the frozen far corner.','The intended lifted edge flattening beside the broad brush is not legible; partial action realization remains fail.'],'measurement_limit':kw['measurement_limit'],'user_aesthetic_acceptance':'pending','original_saved_path':r['saved_path'],'image_sha256':r['sha256'],'png_dimensions':[r['png_width'],r['png_height']],'source_ref':m['source_ref'],'source_snapshot_sha256':snap['snapshot_tar_sha256'],'core_freeze_original_sha256':sha('core_freeze.json'),'original_core_file_sha256':f['authorial_core_file_sha256'],'canonical_core_sha256':m['authorial_core_sha256'],'intent_lock_sha256':m['intent_lock_sha256'],'test_case_sha256':f['test_case_sha256'],'freeze_verification':'all_unchanged','input_isolation':f['input_isolation'],'retrieval_observation':sel['retrieval_observation'],'files':{n:str(p/n) for n in ['generated.png','report.md','arm_summary.json','request_envelope.json','request_original.txt','authorial_core.json','baseline_prompt_en.txt','precore_feature_selection.json','precore_validation.json','embodiment_review.json','random_staging.json','test_case.json','core_freeze.json','freeze_verification.json','candidate_pack.json','composer_view.json','selected_candidate_details.json','candidate_exposure_and_selection.json','composed_prompt.json','composition_audit.json','final_prompt_en.txt','image_render_request.json','native_tool_args.json','runtime_prompt_en.txt','runtime_audit.json','native_result.json','keyword_pixel_results.json','pixel_review.json','pixel_review_audit.json','pixel_status_summary.json','review_420px.png','image_runs.ndjson','run_manifest.json','source_snapshot.json','skill_source_snapshot.tar','imagegen.SKILL.snapshot.md']}}
(p/'arm_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
lines=[
 '# high_angle 독립 arm 결과',
 '',
 '하이 앵글 키워드 픽셀 기준은 **5/5 통과**입니다. 전체 고정 복합 장면은 **5/6**, embodiment는 **4/5**로 **실패**입니다. 왼손의 지지 방식과 위치가 `far-corner palm support`에서 가까운 종이 가장자리의 손끝 접촉으로 바뀌었습니다. 종이의 들린 부분이 붓 옆에서 펴지는 결과도 충분히 식별되지 않습니다. `partial_is_fail`을 적용했으며 최초 이미지를 그대로 보존했습니다. 사용자 미적 판정은 pending입니다.',
 '',
 '## 실행 및 의미 출처',
 '',
 '- 독립 seed: `7350812925794127079`; `secrets.randbits(64)` → Python MT19937. 설정/행동/소품/빛 옵션과 draw를 `random_staging.json`에 저장했습니다.',
 '- 장면: 종이 보존 공간의 낮은 작업대에서 성인 창작 캐릭터가 붓으로 종이를 펴는 순간. 금속 자·얕은 안료 접시와 창빛을 함께 배치했습니다. 이는 agent staging이며 사용자 정의·배제·semantic assertion으로 위장하지 않았습니다.',
 '- 사용자 정의 없음. 하이 앵글 의미는 일반 지식에 기반한 해석으로 `interpretation_provenance`에 구분했습니다. 카메라의 높은 위치와 하향 사선 투영을 required typed assertion으로 생성 전에 고정했습니다.',
 '- 전체 raw requester text는 `request_envelope.json.request_text`와 byte-equal이며 active spans만 topic/reference/workflow 해석에 사용했습니다. 위임 브리프를 사용자 텍스트로 사용하지 않았습니다.',
 '- 참조 사진을 original로 직접 확인하고 동일한 실제 파일을 native `referenced_image_paths`에 첨부했습니다. SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`. 얼굴과 머리의 보이는 외형만 사용했습니다.',
 '- 중립 category 9개를 먼저 선택했습니다. pre-core validator valid=true, warnings=[]. core/embodiment/testcase/focal 기준은 후보 전에 고정했고 최종 SHA 검증에서 변경되지 않았습니다.',
 '',
 '## 후보 및 감사',
 '',
 f'- 일반 candidate pack v6 + semantic selection 정확히 1개. Pack `{m["pack_id"]}`, run `{m["ledger_run_id"]}`, composed prompt `{m["prompt_id"]}`, native runtime prompt `{summary["runtime_prompt_id"]}`.',
 '- Compact composer view를 먼저 읽은 후 선택 4개에 대해서만 full details를 읽었습니다. 다음 후보를 선택했습니다.',
 '',
 '| 후보 | 선택 이유 | 픽셀 근거 |',
 '| --- | --- | --- |'
]
for row in summary['selected_candidates']:lines.append('| `'+row['id']+'` | '+row['reason']+' | '+summary['selected_candidate_pixel_evidence'][row['id']]+' |')
lines +=[
 '',
 '- 창빛과 전체 신체 프레이밍에 각각 authored decision을 추가했습니다. 모든 locked anchor 및 카메라 assertion evidence 4개는 원문 유지했습니다. 선택 안 한 opt-in visual concept는 `[]`이며 render gate를 만들지 않았습니다.',
 '- 체형·성격·음료 지지·다른 인물/동작/카메라 시점 후보는 거절했습니다. creative 후보 6개도 모두 거절했습니다. 도메인 routing에 pigment `dish`가 food로 읽힌 오염이 있지만 원본 종이 작업 장면은 유지했습니다.',
 '- Composition audit status=pass, runtime exact-request audit status=pass. warning 5개는 후보가 커버하지 못한 frozen intent를 자유 서술/anchor로 보존했다는 정보입니다. 픽셀 통과를 뜻하지 않습니다.',
 '',
 '## 원본 및 축소 픽셀 판정',
 '',
 '| 하이 앵글 component | 원본 | 420 px | 근거 |',
 '| --- | --- | --- | --- |'
]
for row in kw['components']:lines.append('| `'+row['component_id']+'` | pass | pass | '+row['scale_results']['original']['evidence']+' |')
lines +=[
 '',
 '머리 윗면·어깨 윗면·넓은 상판·바닥이 함께 보이고, 얼굴과 상판 앞면은 남아 있어 사선 하향 시점으로 판정했습니다. 상체가 가까워 크게 보이고 발은 바닥 방향으로 멀어집니다. 이 투영은 높은 위치의 카메라 해석을 지지하지만 실제 카메라 높이·정확한 pitch·초점거리 수치를 증명하지 않습니다.',
 '',
 '| 전체 scene component | 판정 | 근거 |',
 '| --- | --- | --- |'
]
for row in pr['supplemental_observations']['full_scene_components']:lines.append('| `'+row['component_id']+'` | '+row['status']+' | '+row['evidence']+' |')
lines +=[
 '',
 '| 실효 hard gate | 판정 |',
 '| --- | --- |'
]
for key,row in pr['hard_gates'].items():lines.append('| `'+key+'` | '+row['status']+' |')
lines +=[
 '',
 'Pixel review audit에는 schema failure가 없습니다. `embodiment_contact_and_space`가 실패해 qualification_status=`failed_technical_hard_gates`, technical_qualified=false, representative_eligible=false입니다. generic render_repair 계약은 이 초기 arm에 없으므로 그 감사는 적용 대상이 아닙니다. 사용자의 미적 수락은 별도 pending이며 agent가 대신 판정하지 않았습니다.',
 '',
 '## 보존 및 경계',
 '',
 f'- 도구: native `image_gen.imagegen`, 실제 호출 1회. CLI/API fallback·추가 호출·수정·재생성 0회.',
 f'- 반환 원본: `{r["concrete_returned_original_path"]}`. 이 구체 경로에서 작업 폴더로 복사했고 동일 SHA를 확인했습니다.',
 f'- 저장 결과: [{p.name}/generated.png]({r["saved_path"]}), {r["png_width"]}×{r["png_height"]} PNG, {r["bytes"]} bytes, SHA-256 `{r["sha256"]}`.',
 f'- source `{m["source_ref"]}`의 clean skill tree를 tar snapshot으로 보존했습니다. Skill SHA `{m["skill_sha256"]}`. Core 원본 파일 SHA `{f["authorial_core_file_sha256"]}`, normalizer canonical SHA `{m["authorial_core_sha256"]}`는 서로 다른 해시 표면입니다.',
 '- Ledger 1행과 manifest v2를 자기 arm 폴더에 저장했습니다. ledger/manifest status=success는 이미지 도구의 반환·저장을 의미하며, 전체 장면 또는 픽셀 gate 성공을 뜻하지 않습니다.',
 '- 다른 arm/과거 실험/기존 후보를 초기 의미 입력으로 사용하지 않았습니다. 주 데이터·인덱스·코드·fixture 및 공유 ledger는 변경하지 않았습니다.',
 '',
 f'요청 원문: [request_original.txt]({p/"request_original.txt"}). 최종 영문: [final_prompt_en.txt]({p/"final_prompt_en.txt"}). 실제 native 요청: [image_render_request.json]({p/"image_render_request.json"}). 상세 경로는 [arm_summary.json]({p/"arm_summary.json"})에 있습니다.'
]
(p/'report.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'report':str(p/'report.md'),'summary':str(p/'arm_summary.json'),'keyword':'pass','full_scene':'fail','embodiment':'fail','run_id':m['ledger_run_id']},ensure_ascii=False,indent=2))
