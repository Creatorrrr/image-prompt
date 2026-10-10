from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('/Users/chasoik/Projects/image-prompt')
ARM = Path(__file__).resolve().parent


def read(path):
    return json.loads(Path(path).read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (ARM / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


state = read(ARM / 'requalification_run/workflow.json')
old_state = read(ARM / 'run/workflow.json')
artifact = lambda role: read(state['artifacts'][role]['path'])
manifest = read(ARM / 'run_manifest.json')
lines = [line for line in (ARM / 'image_runs.ndjson').read_text().splitlines() if line.strip()]
assert len(lines) == 1, 'one official ledger row required'
ledger = json.loads(lines[0])
composed = artifact('composed')
render = artifact('render_request')
receipt = artifact('runtime_receipt')
freeze = artifact('freeze_receipt')
compose_audit = artifact('composed_audit')
runtime_audit = artifact('runtime_audit')
review_audit = read(ARM / 'native_review_audit_02.stdout.json')
review = read(ARM / 'native_pixel_review_02.json')
first_review = read(ARM / 'native_pixel_review_01.json')
meta = read(ARM / 'native_result_metadata_01.json')
started = read(ARM / 'native_started_01.json')
selection = read(ARM / 'candidate_selection_and_semantic_review.json')
whole = read(ARM / 'whole_image_and_supplemental_review.json')
preparation = read(ARM / 'requalification_preparation.json')
first_exposure = read(ARM / 'first_pack_new_wkr_exposure.json')
new_exposure = read(ARM / 'requalification_new_wkr_exposure.json')
checks = {}


def check(name, condition):
    checks[name] = bool(condition)
    assert checks[name], name


check('single_completed_native_operation', len(state['operations']) == 1
      and len(state['operations'][0]['attempts']) == 1
      and state['operations'][0]['status'] == 'complete')
check('diagnostic_run_no_image_operation', not old_state['operations'])
check('official_manifest_ledger_operation_link', manifest['ledger_run_id'] == ledger['run_id']
      == state['operations'][0]['last_event']['ledger_run_id'])
for field in ['arm_id', 'worktree_id', 'skill_sha256', 'source_ref', 'candidate_pack_version',
              'image_call_count', 'tool', 'generation_environment', 'authorial_core_sha256',
              'intent_lock_sha256', 'runtime_prompt_sha256', 'pack_id', 'effective_visual_contract_sha256']:
    check('manifest_matches_ledger_' + field, manifest[field] == ledger[field])
check('actual_calls_one', manifest['image_call_count'] == meta['actual_image_call_count'] == 1)
check('no_cross_arm_inputs', manifest['cross_arm_inputs_used'] is False
      and ledger['cross_arm_inputs_used'] is False)
check('tool_environment_exact', manifest['tool'] == 'image_gen'
      and manifest['generation_environment'] == 'native_imagegen')
check('skill_hash_current', digest((ROOT / 'skills/photo-prompt-image-generator/SKILL.md').read_bytes())
      == manifest['skill_sha256'])
check('original_request_envelope', digest((ARM / 'request_envelope.json').read_bytes())
      == '5eef50881a21d8050217cdbdc589e5e7a47b09985fa138f01e4f6bb19945ddcd')
for copy in preparation['copies']:
    check('frozen_byte_identical_' + copy['role'], Path(copy['source']).read_bytes() == Path(copy['copy']).read_bytes())
check('core_hash_bound', freeze['contracts']['core'] == manifest['authorial_core_sha256']
      == receipt['bindings']['authorial_core_sha256'])
check('intent_lock_bound', freeze['contracts']['intent_lock'] == manifest['intent_lock_sha256'])
check('qualification_generation', receipt['generation_id']
      == 'c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14')
check('qualification_source', receipt['source_fingerprint']
      == 'c934e9f60126fe1f111ede9e80bf045907624404589b8d28fb45ebd669b73444')
check('manifest_receipt_generation_binding', manifest['source_ref']
      == 'generation:' + receipt['generation_id'] + ';source_fingerprint:' + receipt['source_fingerprint'])
check('positive_export_exact', (ARM / 'final_prompt.txt').read_text() == composed['prompt_en'])
check('positive_hash_bound', digest(composed['prompt_en'].encode())[:16] == ledger['prompt_id'])
check('runtime_hash_bound', digest(render['runtime_prompt_en'].encode()) == manifest['runtime_prompt_sha256'])
check('runtime_positive_negative_exact', render['runtime_prompt_en']
      == composed['prompt_en'] + '\n\nAvoid: ' + composed['negative_en'])
check('started_payload_exact', started['payload']['prompt'] == render['runtime_prompt_en']
      and started['payload']['referenced_image_paths'] == render['referenced_image_paths'])
check('one_attached_reference', len(render['referenced_image_paths']) == len(manifest['reference_sha256']) == 1)
check('reference_hash_bound', digest(Path(render['referenced_image_paths'][0]).read_bytes())
      == manifest['reference_sha256'][0])
image = Path(meta['copied_image_path'])
original = Path(meta['concrete_source_path_returned_by_tool'])
image_hash = digest(image.read_bytes())
check('original_copy_exact', original.read_bytes() == image.read_bytes())
check('image_hash_all_bound', image_hash == meta['image_sha256'] == review['result_sha256']
      == manifest['image_hashes'][0]['sha256'] == state['operations'][0]['result_binding']['sha256'])
check('all_gate_verdicts_preserved_after_schema_fix', review['hard_gates'] == first_review['hard_gates'])
check('exact_derived_gate_set', set(review['hard_gates']) == set(artifact('visual_review_shape')['hard_gates']))
check('review_record_valid', review_audit['record_valid'] is True)
check('prompt_runtime_audits_pass', compose_audit['status'] == runtime_audit['status'] == 'pass')
check('technical_fail_preserved', state['technical_qualification'] == review_audit['technical_qualification'] == 'fail')
pass_ids = [gate for gate, value in review['hard_gates'].items() if value['status'] == 'pass']
fail_ids = [gate for gate, value in review['hard_gates'].items() if value['status'] == 'fail']
check('three_pass_four_fail', len(pass_ids) == 3 and len(fail_ids) == 4)
check('user_acceptance_pending', state['user_judgment']['genuinely_moe'] == 'pending')
status = subprocess.run([str(ROOT / '.venv/bin/python'),
                         str(ROOT / 'skills/photo-prompt-image-generator/scripts/photo_workflow.py'),
                         'status', '--run', str(ARM / 'requalification_run')],
                        cwd=ROOT, capture_output=True, text=True, check=True)
(ARM / 'final_workflow_status.json').write_text(status.stdout)
(ARM / 'final_workflow_status.stderr.json').write_text(status.stderr)
workflow_status = json.loads(status.stdout)
check('no_stale_roles_and_review_validated', workflow_status['stale_roles'] == []
      and workflow_status['phase'] == 'review_record_validated')
(ARM / 'runtime_prompt_exact.txt').write_text(render['runtime_prompt_en'])
check('runtime_export_exact', digest((ARM / 'runtime_prompt_exact.txt').read_bytes())
      == manifest['runtime_prompt_sha256'])
integrity = {'schema_version': 'arm-a-final-integrity/v1',
             'checked_at': datetime.now(timezone.utc).isoformat(), 'status': 'pass',
             'checks': checks, 'frozen_byte_identical_role_count': len(preparation['copies']),
             'ledger_row_count': len(lines), 'ledger_run_id': ledger['run_id'],
             'ledger_sha256': digest((ARM / 'image_runs.ndjson').read_bytes()),
             'manifest_sha256': digest((ARM / 'run_manifest.json').read_bytes()),
             'official_manifest_was_not_rewritten': True, 'image_sha256': image_hash,
             'final_phase': workflow_status['phase'], 'stale_roles': [],
             'record_valid': True, 'technical_qualification': 'fail', 'user_acceptance': 'pending'}
save('final_integrity_check.json', integrity)

profiles = []
for candidate_id in composed['chosen_visual_concept_ids']:
    item = next(item for item in selection['new_candidate_review'] if item['candidate_id'] == candidate_id)
    gate_id = 'vo_' + candidate_id.split(':', 1)[1] + '_1'
    profiles.append({**item, 'full_relation_native_gate_id': gate_id,
                     'full_relation_native_status': review['hard_gates'][gate_id]['status'],
                     'native_evidence': review['hard_gates'][gate_id]['evidence']})

error_files = ['compose_metadata_repair_01.json', 'native_metadata_load_preparation_error_01.json',
               'native_local_save_preparation_error_01.json', 'native_review_metadata_repair_01.json',
               'final_integrity_preparation_error_01.json']
paths = {key: str(ARM / value) for key, value in {
    'report': 'final_report.json', 'summary': 'final_report.md',
    'pixel_review': 'native_pixel_review_02.json', 'whole_image_review': 'whole_image_and_supplemental_review.json',
    'review_audit': 'native_review_audit_02.stdout.json', 'workflow_status': 'final_workflow_status.json',
    'native_crop_manifest': 'pixel_review_crop_manifest.json', 'new_exposure': 'requalification_new_wkr_exposure.json',
    'full_profile_details': 'requalification_wkr_full_details.json', 'selection_review': 'candidate_selection_and_semantic_review.json',
    'manifest': 'run_manifest.json', 'ledger': 'image_runs.ndjson', 'integrity': 'final_integrity_check.json',
    'positive_prompt': 'final_prompt.txt', 'runtime_prompt': 'runtime_prompt_exact.txt'}.items()}
paths['image'] = str(image)
report = {
    'schema_version': 'arm-a-independent-wardrobe-test-report/v1', 'arm_id': 'a',
    'completion': 'Requested one initial native image and strict original-pixel review completed.',
    'scene': 'A traveler helps another passenger close suitcase webbing in a coastal ferry waiting room as boarding resumes after rain.',
    'scene_ownership': 'Agent-selected independently; not relabeled as requester prescription.',
    'random_selection_evidence': read(ARM / 'precore_random_concept.json'),
    'frozen_controls': whole['controls_calibration']['frozen'],
    'frozen_binding': freeze['contracts'], 'skill_sha256': manifest['skill_sha256'],
    'request_envelope_sha256': digest((ARM / 'request_envelope.json').read_bytes()),
    'fourteen_frozen_roles_byte_identical_for_requalification': True,
    'retrieval': {'total_retrieve_calls': 2, 'diagnostic_run_calls': 1, 'qualification_run_calls': 1,
                  'diagnostic_pack_preserved_not_reused': True,
                  'diagnostic_pack_id': first_exposure['pack_id'],
                  'diagnostic_new_wkr_counts': {key: len(value) for key, value in first_exposure['new_wkr_ids'].items()},
                  'qualification_pack_id': manifest['pack_id'], 'pack_version': manifest['candidate_pack_version'],
                  'generation_id': receipt['generation_id'], 'source_fingerprint': receipt['source_fingerprint'],
                  'pack_sha256': receipt['pack_sha256'],
                  'qualification_new_wkr_counts': {key: len(value) for key, value in new_exposure['new_wkr_ids'].items()},
                  'qualification_new_wkr_ids': new_exposure['new_wkr_ids']},
    'selected_new_profiles': profiles,
    'declined_new_profiles': [item for item in selection['new_candidate_review'] if item['decision'] == 'rejected'],
    'audits': {'prompt_contract': compose_audit, 'runtime_text_and_reference': runtime_audit,
               'review_record_validity': review_audit,
               'boundary': 'Contract and record validity passes do not establish actual pixel qualification.'},
    'native_execution': {**meta, 'operation_id': state['operations'][0]['operation_id'], 'operation_status': 'complete',
                         'moderation_blocks': 0, 'native_tool_errors': 0, 'reference_actual_attached_count': 1,
                         'reference_path': render['referenced_image_paths'][0],
                         'reference_sha256': manifest['reference_sha256'][0], 'cross_arm_inputs_used': False},
    'native_qualification': {'technical_qualification': 'fail', 'partial_is_fail': True, 'hard_gate_count': 7,
                             'pass_count': 3, 'fail_count': 4, 'pass_gate_ids': pass_ids, 'fail_gate_ids': fail_ids,
                             'hard_gates': review['hard_gates'], 'image_sha256': image_hash, 'review_scale': 'native'},
    'whole_image': whole,
    'user_acceptance': {'status': 'pending', 'direct_requester_judgment_received': False, 'comparison_render_available': False},
    'ledger_and_manifest': {'integrity_status': 'pass', 'official_first_append_only': True, 'ledger_rows': 1,
                            'ledger_run_id': ledger['run_id'], 'provider_return_status': ledger['status'],
                            'provider_return_success_does_not_prove_pixel_success': True,
                            'manifest_contract': manifest['contract_version'],
                            'first_record_includes_independent_metadata': True,
                            'wrapper_path': str(ARM / 'native_result_with_independent_manifest.py'),
                            'skill_sources_modified_by_arm': False},
    'preserved_errors': [{'path': str(ARM / filename), 'record': read(ARM / filename)} for filename in error_files],
    'current_tool_or_schema_blockers': [],
    'final_prompts': {'positive_path': paths['positive_prompt'], 'positive_text': composed['prompt_en'],
                      'positive_sha256': digest(composed['prompt_en'].encode()),
                      'positive_word_count': len(composed['prompt_en'].split()), 'negative_text': composed['negative_en'],
                      'exact_runtime_path': paths['runtime_prompt'], 'exact_runtime_text': render['runtime_prompt_en'],
                      'exact_runtime_sha256': manifest['runtime_prompt_sha256']},
    'artifacts': paths,
}
save('final_report.json', report)
summary = '''Arm a의 최초 이미지 1장 생성과 원본 픽셀 리뷰를 완료했습니다. 코트 옆 공기 틈(WK008)은 실패, 동일 가방의 두 연결부 지지(WK080)는 통과했습니다. 전체 파생 hard-gate 7개는 통과 3개·실패 4개로 픽셀 자격은 FAIL입니다.

여객선 대합실에서 함께 짐 잠금장치를 다루는 상황, 소재 표면과 지역 색상, 스카프 두 꼬리 및 시계 소유 관계는 읽힙니다. 집중한 얼굴과 작은 미소, 공유 행동이 따뜻한 여행 사진을 만들지만, 코트 옆 틈과 버클 혀를 하우징으로 넣는 정확한 접합 동작은 확인되지 않습니다. 한 발이 들린 교차 다리 자세도 최종 검토된 두 발 바닥 지지 상태와 다릅니다.

| 검증 층 | 결과 |
| --- | --- |
| Prompt audit | PASS, quality WARN 4개: 최소 requester anchor를 자유 서술·assertion으로 보존 |
| Runtime text/reference audit | PASS |
| 리뷰 기록 유효성 | PASS |
| WK008 전체 관계 | FAIL: 몸통 옆 패널의 독립 공기 틈이 가려짐 |
| WK080 전체 관계 | PASS: 동일 가방 양쪽 연결부와 스트랩 가지가 보임 |
| 전체 픽셀 hard-gate | 3 PASS / 4 FAIL, technical qualification FAIL |
| 원장·manifest 무결성 | PASS, 공식 recorder 단일 행·첫 기록에 독립 metadata 포함 |
| 전체 상황·미학 | 공유 도움과 출항 맥락이 읽히며 은근한 얼굴 중심 매력 유지 |
| 사용자 수용 | PENDING, 비교 렌더 없음 |

내장 image_gen 생성은 정확히 1회이며 수리 렌더·API fallback은 0회입니다. 실제 모델명은 도구가 반환하지 않았습니다. 원본 1237×1272 픽셀과 byte-identical 복사본을 보존했습니다. 조회는 최초 진단 1 pack과 동일 frozen 입력의 requalification 1 pack, 총 2회이며 최초 pack은 최종 구성에 재사용하지 않았습니다. 새 qualification pack에 신규 ordinary 1개·bundle 0개·visual concept 3개가 노출됐습니다. WK008/WK080을 선택했고 WK006 조끼와 WK077 샌들은 얼굴·손·코트·가방 구성을 유지하려는 미학적 판단으로 거절했습니다.

형식 오류(0 강도 축 누락, null 사용자 판단), 로컬 준비 오류(메타데이터 출력 잘림, PIL 부재 및 미생성 복사 경로), 최종 prompt 내보내기의 추가 개행을 모두 보존했습니다. metadata·로컬 복사·텍스트 내보내기만 보완했으며 실제 생성 prompt·이미지·gate 판정은 바꾸지 않았습니다. 현재 도구나 스키마 때문에 막힌 항목은 없습니다.

- [이미지](images/ferry-waiting-room-native-01.png)
- [최종 positive prompt](final_prompt.txt) · [실제 호출 prompt](runtime_prompt_exact.txt)
- [전체 상세 보고](final_report.json) · [원본 픽셀 판정](native_pixel_review_02.json)
- [원장](image_runs.ndjson) · [공식 manifest](run_manifest.json) · [최종 무결성 검사](final_integrity_check.json)
'''
summary += '\nCore SHA256: `' + manifest['authorial_core_sha256'] + '`\n'
summary += '\nQualification generation: `' + receipt['generation_id'] + '`\n'
summary += '\nImage SHA256: `' + image_hash + '`\n'
(ARM / 'final_report.md').write_text(summary)
print(json.dumps({'integrity': 'pass', 'checks': len(checks), 'frozen_identical_roles': 14,
                  'record_valid': True, 'technical_qualification': 'fail', 'hard_gates': {'pass': 3, 'fail': 4},
                  'actual_image_calls': 1, 'ledger_rows': 1, 'user_acceptance': 'pending',
                  'report': paths['report']}, ensure_ascii=False))
