from pathlib import Path
import datetime
import hashlib
import json

ARM = Path(__file__).resolve().parent

def read(name):
    return json.loads((ARM / name).read_text())

def write(name, value):
    (ARM / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

state = read('run/workflow.json')
audit = read('review_audit.json')['visual']
copy = read('image_copy_receipt.json')
observed = read('native_tool_return_metadata.json')
pixel = read('PIXEL-TEST-RESULTS.json')
data = read('DATA-CONTRIBUTION.json')
manifest = read('run_manifest.json')
receipt = read('candidate_pack.runtime-receipt.json')
rows = [json.loads(line) for line in (ARM / 'image_runs.ndjson').read_text().splitlines() if line]
review = read('visual_render_review.json')
assert state['technical_qualification'] == 'pass'
assert audit['technical_qualified'] and not audit['schema_failures'] and not audit['failed_hard_gates']
assert audit['required_hard_gate_count'] == 5
assert len(rows) == 1 and rows[0]['status'] == 'success' and rows[0]['image_call_count'] == 1
assert manifest['contract_version'] == 'photo-independent-run-manifest/v2'
assert manifest['cross_arm_inputs_used'] is False and manifest['ledger_run_id'] == rows[0]['run_id']
assert manifest['image_call_count'] == 1
assert sha(copy['native_path']) == copy['sha256'] == sha(copy['arm_local_path'])
assert len(review['hard_gates']) == 5 and all(row['status'] == 'pass' for row in review['hard_gates'].values())
assert review['user_judgment']['source'] == 'not_yet_received'
assert sum(row['status'] == 'pass' for row in pixel['test_results']) == 7
assert sum(row['status'] == 'fail' for row in pixel['test_results']) == 1
assert receipt['pack_sha256'] == read('composer_view.json')['source_pack_sha256']

pixel.update(hard_gate_status='pass', hard_gate_pass_count=5, hard_gate_fail_count=0,
             review_audit_file=str(ARM / 'review_audit.json'), user_aesthetic_acceptance='not_yet_received')
write('PIXEL-TEST-RESULTS.json', pixel)

source = read('SOURCE-RECEIPT.json')
source['postcore_source_binding'].update(pack_canonical_sha256=receipt['pack_sha256'],
                                       pack_file_sha256=sha(ARM / 'candidate_pack.json'))
source['execution'] = {
    'tool': 'image_gen.imagegen', 'actual_image_call_count': 1, 'api_call_count': 0,
    'actual_tool_started_at_utc': observed['started_at_utc'],
    'actual_tool_ended_at_utc': observed['ended_at_utc'],
    'reservation_timestamp_not_actual_tool_start': state['operations'][0]['timestamp'],
    'operation_id': observed['operation_id'], 'ledger_run_id': rows[0]['run_id'],
    'native_image_path': copy['native_path'], 'arm_local_image_path': copy['arm_local_path'],
    'image_sha256': copy['sha256'], 'actual_native_dimensions': copy['dimensions'],
    'observed_image_model': None, 'outcome': 'returned_success',
}
source['qualification'] = {
    'composed_audit': 'pass', 'runtime_audit': 'pass', 'review_audit': 'pass',
    'hard_gate_pass_count': 5, 'hard_gate_fail_count': 0,
    'strict_authored_testcase_pass_count': 7, 'strict_authored_testcase_fail_count': 1,
    'strict_authored_testcase_status': 'fail',
    'remaining_fail': 'scene_and_feeling: tentative relief is ambiguous',
    'soil_data_components': 'pass', 'user_aesthetic_acceptance': 'not_yet_received',
}
source['independent_manifest'] = {
    'path': str(ARM / 'run_manifest.json'), 'sha256': sha(ARM / 'run_manifest.json'),
    'binding_proof': str(ARM / 'MANIFEST-BINDING.json'), 'ledger_rows': 1,
    'no_duplicate_append': True,
}
source['local_handling_recoveries'] = [
    {'file': 'LOCAL-SAVE-RECOVERY.json', 'scope': 'Missing optional PIL in metadata helper and premature native-result input; recovered from the already returned native file without re-invocation.'},
    {'file': 'MANIFEST-BINDING.json', 'scope': 'Current native operation exposes record_args in workflow.json; the earlier journal-path assumption was corrected only in the arm-local helper.'},
    {'file': 'REVIEW-IMAGE-BINDING.json', 'scope': 'Official review names the actual native path recorded by the observed attempt. The workspace copy is byte-identical.'},
]
write('SOURCE-RECEIPT.json', source)

files = {name: str(ARM / path) for name, path in {
    'testcase': 'TESTCASE.json', 'core': 'authorial_core.json',
    'baseline_prompt': 'baseline_prompt_en.txt', 'final_prompt': 'final_prompt_en.txt',
    'runtime_prompt': 'runtime_prompt_en.txt', 'image': 'result_image.png',
    'data_contribution': 'DATA-CONTRIBUTION.json', 'pixel_test_results': 'PIXEL-TEST-RESULTS.json',
    'formal_review': 'visual_render_review.json', 'review_audit': 'review_audit.json',
    'ledger': 'image_runs.ndjson', 'manifest': 'run_manifest.json',
    'source_receipt': 'SOURCE-RECEIPT.json', 'report': 'report.md',
}.items()}
result = {
    'schema_version': 'soil-independent-arm-result/v1', 'arm': 'arm-2', 'status': 'completed',
    'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'concept': {'id': 'earth_pigment_workbench', 'ko': '흙 안료 작업실에서 부서진 흙 미장 부조를 복원하는 순간',
                'seed': 3830837209, 'draw_index': 3, 'precore_independently_frozen': True,
                'exploration_area_is_agent_owned': True},
    'request': {'envelope_file_sha256': 'fcaa4749a7553ecb813c0d01b873c16982e348bf0d3db5dc8764dce68fd193d8',
                'raw_request_sha256': 'e01d0ad2bb1da5978db473bef7ce3e0212453e8f35839532c8ba05a27dbc7fff',
                'raw_user_text_preserved': True, 'active_span_ids': ['concept', 'reference']},
    'bound_source': {'generation_id': receipt['generation_id'], 'source_fingerprint': receipt['source_fingerprint'],
                     'skill_sha256': source['skill_sources'][0]['sha256'], 'pack_id': rows[0]['pack_id'],
                     'pack_file_sha256': sha(ARM / 'candidate_pack.json'),
                     'pack_canonical_sha256': receipt['pack_sha256'],
                     'authorial_core_sha256': manifest['authorial_core_sha256'],
                     'intent_lock_sha256': manifest['intent_lock_sha256']},
    'creative_controls': {'sensual': 1, 'fetish': 0, 'creativity': 1, 'surreal': 0,
                          'emphasis': 'sensual_led', 'reference_edit_mode': 'off; supplied face/hair reference still attached'},
    'execution': source['execution'], 'image': copy,
    'audits': {'feature_selection': 'pass, 9 categories, no warnings', 'composed_prompt': 'pass',
               'composed_quality': 'warn, four core-anchor coverage warnings preserved by literal free description',
               'runtime_prompt': 'pass', 'review_record': 'pass', 'technical_qualification': 'pass',
               'independent_manifest': 'validated through existing recorder functions; exact managed row preserved',
               'hard_gates': {name: row['status'] for name, row in review['hard_gates'].items()}},
    'strict_authored_testcase': {'status': 'fail', 'pass_count': 7, 'fail_count': 1,
                                'results': pixel['test_results'], 'partial_is_fail': True},
    'soil_topic_and_data': {
        'soil_theme_and_material_relations': 'pass',
        'exposed_new_candidate_ids': ['slot:color:soil_e021', 'slot:location:soil_e099'],
        'selected_new_candidate_ids': ['slot:color:soil_e021'],
        'rejected_new_candidate_ids': ['slot:location:soil_e099'],
        'new_visual_profile_exposure_count': 0, 'new_visual_profile_selection_count': 0,
        'selected_candidate_pixel_components': '3 pass / 0 fail',
        'literal_added_prompt_evidence': data['new_soil_candidate_exposure'][0]['literal_final_prompt_evidence'],
        'baseline_already_contained': 'Soil topic, powder/clod/wet filler states, supported repair action and apron/working-hand residues.',
        'data_increment': 'Local reddish-brown filler hue, same-hue grains owned by that patch, and hue ending at the ragged patch-to-old-panel boundary.',
        'causal_image_improvement_vs_ablation': 'not_tested: no baseline-only rendered control image',
    },
    'limitations': [
        'The emotional change from concentration into tentative relief is not distinct; its authored expectation remains fail.',
        'The actual native frame is 1237×1272 rather than the agent-owned landscape preference; all critical relations remain visible.',
        'Working-hand soil is clearest along index-side skin; exact thumb localization is weaker.',
        'No new soil visual profile was returned or selected, so this arm does not prove those profiles runtime/pixel effectiveness.',
        'Technical and pixel observations do not substitute for requesting-user aesthetic acceptance.',
    ],
    'user_aesthetic_acceptance': 'not_yet_received',
    'independence': {'cross_arm_inputs_used': False,
                     'writes_confined_to': 'arm-2 artifacts; native image output was created by the tool',
                     'shared_operational_code_or_indexes_modified': False},
    'files': files,
}
write('ARM-RESULT.json', result)

labels = {
    'earth_material_states': '건조 덩이·분말·젖은 흙 상태',
    'raw_to_processed_connection': '원흙 → 분쇄·체질 → 채움 연결',
    'repair_cause_action_result': '손상 → 나이프 접촉 → 보수 결과',
    'residue_owner_apron': '앞치마 직물의 흙 손자국',
    'residue_owner_hand': '작업 손 피부에 붙은 흙',
    'reference_appearance': '참조 얼굴·짧은 검은 보브 외형',
    'body_and_tool_relation': '양팔·지지 손·도구 접촉',
    'scene_and_feeling': '집중에서 안도로 바뀌는 정서',
}
lines = [
    'arm-2 — **흙 안료 작업실에서 부서진 흙 미장 부조를 복원하는 순간**', '',
    '실제 native 이미지 생성 **1회**로 테스트를 완료했습니다. 프롬프트·runtime·공식 픽셀 리뷰 감사는 PASS이며, 신체·도구 관계의 hard gate 5개도 모두 PASS입니다. 독립적으로 동결한 자체 기대값은 **7 pass / 1 fail**입니다. 장면과 집중은 명확하지만 “안도로 전환”은 구별하기 어려워 fail을 보존했습니다. 미학적 사용자 수락은 `not_yet_received`입니다.', '',
    '컨셉 seed `3830837209`의 단일 draw index 3으로 네 가능성 중 하나를 선택했습니다. 연구·후보 접근 전에 실제 원문·active spans·creative controls·TESTCASE·core를 동결했습니다. 저장값은 sensual 1, fetish 0, creativity 1, surreal 0입니다. 참조는 직접 보이는 얼굴과 헤어 외형에만 사용했고 실제 정체성·성격·생애는 추정하지 않았습니다.', '',
    '신규 **soil_e021**을 선택해 붉은 갈색 보수 흙 패치, 그 패치에 속한 같은 색 입자, 밝은 기존 흙 부조와의 국소 경계를 최종 문장에 추가했습니다. 세 성분은 실제 이미지에서도 관찰됩니다. 신규 **soil_e099**의 발굴 단면·격자·매장 유물 관계는 실내 부조 복원 목적과 달라 기각했습니다. 새 흙 시각 프로필은 **노출 0 / 선택 0**입니다.', '',
    '흙의 분말·덩이·젖은 상태와 복원 동작은 독립 baseline에 이미 있었습니다. 이번 기여는 색·입자·경계의 소유 관계를 명시한 부분입니다. baseline-only 대조 이미지를 생성하지 않았으므로 이미지 수준의 인과적 개선 효과는 입증하지 않았습니다.', '',
    '| 자체 기대값 | 결과 |', '|---|---|',
]
lines += ['| ' + labels[row['id']] + ' | ' + row['status'] + ' |' for row in pixel['test_results']]
lines += [
    '', '실제 파일은 **1237×1272 PNG**입니다. 전체 프레임과 native 해상도에서 확인했고, native 원본과 arm 로컬 복사는 SHA-256 `' + copy['sha256'] + '`로 동일합니다. 거의 정사각형인 결과는 agent가 선택한 landscape 구상과 다르지만 중요한 물질·지지·접촉 관계를 가리지 않습니다. 손의 흙 흔적은 엄지보다 검지 쪽에서 더 뚜렷합니다.', '',
    'manifest v2는 기존 recorder의 검증 함수를 사용해 실제 managed ledger 행의 모든 필드와 같은 입력으로 만들었습니다. ledger에는 실제 호출 **1개 행**만 있습니다. 로컬 준비 오류는 복구 기록에 남겼으며 이미지 도구 재호출과 공유 스크립트 변경 없이 반환 파일의 바이트와 실제 호출 기록을 보존했습니다.', '',
    '주요 산출물: ' + ', '.join('[' + label + '](' + files[name] + ')' for name, label in [
        ('final_prompt', '최종 프롬프트'), ('image', '결과 이미지'), ('data_contribution', '기여 기록'),
        ('pixel_test_results', '픽셀 자체 테스트'), ('formal_review', '공식 리뷰'), ('review_audit', '리뷰 감사'),
        ('ledger', 'ledger'), ('manifest', '독립 manifest'), ('source_receipt', 'source receipt'),
    ]) + ', [종합 결과](' + str(ARM / 'ARM-RESULT.json') + ').', '',
    '![흙 부조 복원 작업 결과](' + files['image'] + ')', '',
]
(ARM / 'report.md').write_text('\n'.join(lines))
assert all(Path(path).is_file() for path in files.values())
assert read('ARM-RESULT.json')['execution']['actual_image_call_count'] == 1
print(json.dumps({'result': str(ARM / 'ARM-RESULT.json'), 'report': str(ARM / 'report.md'),
                  'actual_image_call_count': 1, 'hard_gates': '5 pass / 0 fail',
                  'self_tests': '7 pass / 1 mood fail', 'soil_components': '3 pass / 0 fail',
                  'user_acceptance': 'not_yet_received'}))
