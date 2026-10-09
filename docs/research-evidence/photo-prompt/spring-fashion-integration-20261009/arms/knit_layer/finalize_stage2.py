"""Assemble exact source, frozen-input, native-attempt and review evidence."""
from pathlib import Path
import hashlib
import json

ARM=Path(__file__).resolve().parent
RUN=ARM/'run'
WT=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
value=lambda p:json.loads(Path(p).read_text())
s=value(RUN/'workflow.json')
assert s['phase']=='review_record_validated'
for item in s['artifacts'].values():
 assert sha(item['path'])==item['sha256'], item['path']
a=s['artifacts']
pack=value(a['pack']['path']); pack=pack[0] if isinstance(pack,list) else pack
composed=value(a['composed']['path'])
receipt=value(a['runtime_receipt']['path'])
request=value(a['render_request']['path'])
plan=value(a['native_plan']['path'])
meta=value(ARM/'native-result-metadata.json')
review=value(a['visual_review']['path'])
audit=value(a['review_audit']['path'])
supp=value(ARM/'supplemental-new-candidate-review.json')
topic=value(ARM/'supplemental-topic-review.json')
manifest=value(ARM/'run_manifest.json')
ledger=[json.loads(x) for x in (ARM/'image_runs.ndjson').read_text().splitlines() if x.strip()]
managed=[json.loads(x) for x in (RUN/'native_image_runs.ndjson').read_text().splitlines() if x.strip()]
assert len(ledger)==len(managed)==1
assert ledger[0]['run_id']==managed[0]['run_id']==manifest['ledger_run_id']
assert len(s['operations'])==1 and len(s['operations'][0]['attempts'])==1
assert s['operations'][0]['status']=='complete'
assert meta['actual_image_call_count']==ledger[0]['image_call_count']==manifest['image_call_count']==1
assert meta['image_sha256']==sha(meta['project_image_path'])==sha(meta['source_returned_path'])==review['result_sha256']
expected_generation='a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c'
expected_source='6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a'
expected_skill='9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b'
assert s['source_binding']['generation_id']==receipt['generation_id']==expected_generation
assert s['source_binding']['source_fingerprint']==receipt['source_fingerprint']==expected_source
assert sha(WT/'skills/photo-prompt-image-generator/SKILL.md')==manifest['skill_sha256']==expected_skill
assert sha(a['freeze_receipt']['path'])=='19b8bd835e6bb9baa87304c4a32bf5a435f771d02425ce60df748d33e9741950'
assert a['baseline']['sha256']=='9731cd7a5e950155a296e4269d3bb247360ae09cde87ad52d9b4f5926fe102b7'
assert sha(ARM/'request_envelope.json')==a['request_envelope_input']['sha256']=='81731e13b667c5f32f60476d3a826f47bfa7a8c45651eb0c69fcd33e3f25a1ac'
assert pack['authorial_core']['canonical_sha256']==manifest['authorial_core_sha256']=='97ece69a1d3d842933a440b9a99891dd640e1cf943a85509f06b72787c61f3b3'
assert pack['authorial_core']['intent_lock']['canonical_sha256']==manifest['intent_lock_sha256']=='b60a431e8837cd6fb5d8d42c5d3ac3c03821c965cd7831217aff2cac439b82a0'
started=value(ARM/'native-started.stdout.json')
assert started['payload']==plan['payload']
assert plan['payload']['prompt']==request['runtime_prompt_en']==composed['prompt_en']+'\n\nAvoid: '+composed['negative_en']
assert request['referenced_image_paths']==plan['payload']['referenced_image_paths']
assert request['references'][0]['sha256']==sha(request['referenced_image_paths'][0])==manifest['reference_sha256'][0]
assert set(review['hard_gates'])==set(audit['visual']['required_hard_gates'])
assert len(review['hard_gates'])==11
assert audit['visual']['technical_qualified'] is True and not audit['visual']['schema_failures']
assert review['user_judgment']['source']=='not_yet_received'
result={
 'schema_version':'spring-fashion-independent-stage2-result/v1',
 'arm_id':'knit_layer','concept_name':'강변 인쇄 공방의 첫 도판과 봄바람',
 'status':'completed_with_supplemental_visibility_failure',
 'generation':expected_generation,'source_fingerprint':expected_source,'skill_sha256':expected_skill,
 'runtime_store':s['source_binding']['runtime_store'],'runtime_receipt':a['runtime_receipt'],
 'pack_id':pack['pack_id'],'pack':a['pack'],
 'frozen_preservation':{'freeze_receipt':a['freeze_receipt'],'authorial_core_sha256':manifest['authorial_core_sha256'],
                        'intent_lock_sha256':manifest['intent_lock_sha256'],'baseline':a['baseline'],
                        'request_envelope_file_sha256':sha(ARM/'request_envelope.json'),
                        'raw_request_sha256':a['request_raw']['sha256'],'frozen_input_changes':0},
 'selected_new_ids':['visual-concept:spring_sf057_02','bundle:spf_sf104_2_bundle'],
 'new_source_ids_applied':['spring_sf057_02','spf_sf104_2'],
 'chosen_candidate_ids':composed['chosen_candidate_ids'],'chosen_visual_concept_ids':composed['chosen_visual_concept_ids'],
 'associated_color_profile':{'id':'spring_sf104_2','hard_activation':False,'native_hard_profile_qualification':'not_tested'},
 'prompt_path':str(ARM/'prompt_en.txt'),'composed':a['composed'],
 'prompt_en_sha256':hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),
 'runtime_prompt_sha256':manifest['runtime_prompt_sha256'],
 'native_attempt':{'tool':'image_gen','observed_image_model':None,'image_call_count':1,'operation_id':plan['operation_id'],
                   'ledger_run_id':ledger[0]['run_id'],'outcome':'returned','source_returned_path':meta['source_returned_path'],
                   'project_image_path':meta['project_image_path'],'dimensions':meta['dimensions'],'image_sha256':meta['image_sha256'],
                   'native_plan':a['native_plan'],'metadata_path':str(ARM/'native-result-metadata.json'),
                   'execution_adapter':'managed native-started plus exact payload and shared full native-error capture'},
 'audits':{'composed':a['composed_audit'],'runtime':a['runtime_audit'],'review':a['review_audit'],
           'review_record_valid':True,'technical_qualification':s['technical_qualification'],
           'audit_boundary':'Auditors validate input/review records; direct agent inspection supplies the pixel judgments.'},
 'native_pixel_review':{'path':str(ARM/'native-pixel-gate-review.json'),'hard_gate_count':11,'pass_count':11,'fail_count':0,
                        'exact_hard_gate_ids':list(review['hard_gates']),'shape':a['visual_review_shape'],
                        'native_review_views':str(ARM/'review-view-manifest.json')},
 'supplemental_new_candidate_review':{'path':str(ARM/'supplemental-new-candidate-review.json'),'all_of_result':'fail',
                                       'pass_count':4,'fail_count':1,'failed_row_ids':['warm_bundle_boundaries'],
                                       'reason':'The preplanned skirt waistband endpoint is covered by the blouse; source palette and wearer relation are observed.'},
 'supplemental_topic_review':{'path':str(ARM/'supplemental-topic-review.json'),'pass_count':10,'fail_count':1,
                              'qualitative_count':1,'failed_observation_ids':['O06']},
 'ledger_path':str(ARM/'image_runs.ndjson'),'manifest_path':str(ARM/'run_manifest.json'),
 'managed_internal_ledger_path':str(RUN/'native_image_runs.ndjson'),
 'ledger_counting_boundary':'The independent and managed ledgers identify the same one actual native call and run_id, not two invocations.',
 'independence':{'cross_arm_inputs_used':False,'other_arm_reads':0,'authoring_seed':198294653418842,'retrieval_seed':83671},
 'user_judgment':review['user_judgment'],
 'limitations':['Associated spring_sf104_2 was not activated as a hard profile.',
                'The full optional waistband observation set did not qualify.',
                'No user acceptance or exact fiber/process/hidden-garment absence is inferred.'],
}
(ARM/'stage2-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
gate_table='\n'.join('| '+k+' | PASS | '+', '.join(v['reviewed_scales'])+' |' for k,v in review['hard_gates'].items())
md=f'''# 강변 인쇄 공방의 첫 도판과 봄바람 — A / knit_layer

실제 built-in `image_gen` 1회로 참조 사진을 첨부해 생성했다. 결과는 1024×1536 PNG다. 원본과 프로젝트 복사본 SHA256은 `{meta['image_sha256']}`로 동일하다.

- 이미지: [{Path(meta['project_image_path']).name}]({meta['project_image_path']})
- 프롬프트: [prompt_en.txt]({ARM/'prompt_en.txt'})
- 상세 결과: [stage2-result.json]({ARM/'stage2-result.json'})
- 독립 ledger: [image_runs.ndjson]({ARM/'image_runs.ndjson'}) / [run_manifest.json]({ARM/'run_manifest.json'})

동결된 core·원문·locks·baseline은 그대로 유지했다. 난수 seed `198294653418842`로 pre-core에 독립적으로 선택한 인쇄 공방 순간이며, retrieve seed는 `83671`이다. 다른 arm의 폴더·프롬프트·pack·이미지를 읽지 않았다.

검증 runtime generation은 `{expected_generation}`, source fingerprint는 `{expected_source}`다. 실제 receipt와 모든 managed native 단계에서 같은 세대를 사용했다. 원문 envelope SHA256은 `{result['frozen_preservation']['request_envelope_file_sha256']}`, core는 `{manifest['authorial_core_sha256']}`, intent lock은 `{manifest['intent_lock_sha256']}`다.

실제 노출된 신규 `visual-concept:spring_sf057_02`와 `bundle:spf_sf104_2_bundle`을 authorial/optional로 선택했다. 전자는 니트의 연속 실 경계·진짜 열린 셀을 hard opt-in한다. 후자는 `spf_sf104_2`의 같은 착용자에게 속한 블라우스/스커트의 인접한 저채도 따뜻한 색과 분리된 의복 경계를 적용한다. `spring_sf104_2` associated profile은 자동 hard 활성화하지 않았다. 기존 `visual-concept:sheer_garment_optical_layering`은 실제 투과 레이어에 명시 opt-in했다.

composed/runtime 감사와 native plan은 PASS다. 네이티브 실행 operation은 `{plan['operation_id']}`, ledger run ID는 `{ledger[0]['run_id']}`다. managed 내부 ledger와 독립 ledger는 동일한 실제 1회를 각 provenance 형태로 기록하며 합산하지 않는다. 도구가 이미지 모델명을 반환하지 않아 observed model은 unknown이다.

`review-shape`에서 정확히 유도된 11개 hard gates를 같은 저장 PNG의 전체 프레임, 1:1 native crops, 320×480 thumbnail로 검토했다. 기록 감사 PASS, technical qualification PASS, direct pixel observation 11/11 PASS다. 감사기는 픽셀을 추론하지 않으며 관찰 근거는 agent가 직접 작성했다.

| 정확한 runtime hard gate | 관찰 | 요구 scale |
| --- | --- | --- |
{gate_table}

별도 신규 후보의 사전 all-of 관찰표는 **4/5 PASS, 전체 FAIL**이다. 니트 두 효과와 같은 wearer·따뜻한 색 관계는 관찰됐다. 그러나 미리 정한 `warm_bundle_boundaries`의 두 번째 끝점인 **스커트 waistband가 블라우스에 가려져** 완전한 관찰을 할 수 없다. 다른 skirt outline으로 사후 대체하지 않았다. 전체 topic review에서도 같은 이유로 O06을 FAIL로 보존했다. 이 supplemental 실패를 runtime hard gate에 추가하거나 hard PASS로 바꾸지 않았다.

- 정확한 관찰: [native-pixel-gate-review.json]({ARM/'native-pixel-gate-review.json'})
- 신규 후보 all-of: [supplemental-new-candidate-review.json]({ARM/'supplemental-new-candidate-review.json'})
- 전체 인상·topic: [supplemental-topic-review.json]({ARM/'supplemental-topic-review.json'})

밝고 공기가 도는 공방, 실제 클립 행동, 니트/투과/안쪽 상의의 재료 위계가 함께 읽힌다. 얼굴·짧은 검은 bob·가느다란 fringe는 첨부 사진의 보이는 외형을 안내로 사용했다. 실제 정체성·성격·생애·치수·정확한 섬유/공정·숨은 미착용은 추론하지 않았다. 생성된 full-body crop은 authorial mid-calf 제안보다 넓다. 추가 신발·작업실 문구는 보충 요소로 남는다.

사용자 judgment는 **not_yet_received / pending**이다. 별도 root 재검토와 실제 사용자 선호를 agent 기술 관찰로 대신하지 않는다.
'''
(ARM/'TESTCASE.md').write_text(md)
print(json.dumps({'status':result['status'],'stage2_result':str(ARM/'stage2-result.json'),'stage2_sha256':sha(ARM/'stage2-result.json'),
                  'testcase':str(ARM/'TESTCASE.md'),'hard_gates':'11/11 pass','supplemental_new':'4/5; all-of fail','image_call_count':1},ensure_ascii=False))
