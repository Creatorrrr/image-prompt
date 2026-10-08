"""Collect this arm's actual immutable bindings, attempts and strict reviews."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
child = root / 'repair_1'

def read(path):
    return json.loads(Path(path).read_text())

def file(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

rows = [json.loads(x) for x in (root / 'image_runs.ndjson').read_text().splitlines() if x]
assert len(rows) == 2
assert rows[0] == read(root / 'parent_attempt_exact.json')
assert rows[1]['retry_of'] == rows[0]['run_id']
assert rows[1]['image_call_count'] == 2
(child / 'native_attempt_exact.json').write_text(json.dumps(rows[1], ensure_ascii=False, indent=2) + '\n')

attempts = []
for index, (run, row, pixel_name, formal_name, whole_name) in enumerate([
    (root, rows[0], 'pixel_review_attempt_1.json', 'render_review_attempt_1.json', 'whole_image_review_attempt_1.md'),
    (child, rows[1], 'pixel_review_repair_1.json', 'render_review_repair_1.json', 'whole_image_review_repair_1.md'),
]):
    state = read(run / 'workflow.json')
    pixel = read(run / pixel_name)
    composed = read(state['artifacts']['composed']['path'])
    effect = read(run / 'candidate_effect_record.json')
    core = read(state['artifacts']['authorial_core_normalized']['path'])
    controls = read(state['artifacts']['creative_controls']['path'])
    if index == 0:
        formal = read(state['artifacts']['review_audit']['path'])['visual']
        audit_binding = file(state['artifacts']['review_audit']['path'])
        formal_lane = 'managed_review_record_validated'
        record_valid = not formal['schema_failures'] and state['phase'] == 'review_record_validated'
        profile_ids = effect['new_visual_concept_profiles_exposed']
        new_ids = effect['new_catalog_ids']
        native_status = effect['native_pixel_status']
        audit_recovery = None
    else:
        independent = read(child / 'render_review_repair_1_audit.json')
        formal = independent['visual']
        audit_binding = file(child / 'render_review_repair_1_audit.json')
        formal_lane = independent['scope']
        record_valid = independent['record_valid']
        profile_ids = effect['new_fit_visual_concept_ids']
        new_ids = [x['id'] for x in effect['exposed_new_fit_rows']]
        native_status = effect['native_pixel_status']
        audit_recovery = {
            'native_capture_recovery': file(child / 'native_capture_recovery.json'),
            'initial_path_parse': file(child / 'native_tool_return_metadata_initial_path_parse.json'),
            'managed_review_diagnostic': file(child / 'managed_review_audit_diagnostic.json'),
            'historical_operation_status': state['operations'][0]['status'],
            'historical_observation': file(child / 'operations' / (state['operations'][0]['operation_id'] + '.observation.json')),
            'same_return_supported_recorder': file(child / 'native_return_recorder_result.json'),
            'independent_receipt_bound_full_audit': file(child / 'independent_bound_audit_full.json'),
            'actual_tool_request': file(child / 'native_tool_request_actual.json'),
            'additional_image_calls_for_recovery': 0,
        }
    selected_new = [x for x in row['chosen_candidate_ids'] if 'fit_ff' in x]
    literal = effect.get('literal_prompt_evidence') or effect.get('literal_relation_evidence')
    counts = {'pass': sum(x['status'] == 'pass' for x in pixel['gates'].values()), 'total': len(pixel['gates'])}
    attempts.append({
        'attempt': index + 1,
        'kind': 'initial' if index == 0 else 'one_bounded_repair',
        'run_directory': str(run),
        'image': file(row['image_paths'][0]),
        'prompt_file': file(run / 'final_prompt.txt'),
        'prompt_en_sha256': hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),
        'runtime_prompt_sha256': row['runtime_prompt_sha256'],
        'exact_native_plan': state['artifacts']['native_plan'],
        'ledger_path': str(root / 'image_runs.ndjson'),
        'ledger_run_id': row['run_id'],
        'retry_of': row['retry_of'],
        'ledger_row': file(root / 'parent_attempt_exact.json') if index == 0 else file(child / 'native_attempt_exact.json'),
        'actual_tool_calls_this_attempt': 1,
        'source_binding': state['source_binding'],
        'runtime_source_hashes': file(run / 'runtime_source_hashes.json'),
        'core_sha256': core['canonical_sha256'],
        'intent_lock_sha256': core['intent_lock']['canonical_sha256'],
        'creative_controls_sha256': controls['canonical_sha256'],
        'source_request_sha256': controls['source_request_sha256'],
        'pack_id': row['pack_id'],
        'pack': state['artifacts']['pack'],
        'runtime_receipt': state['artifacts']['runtime_receipt'],
        'composed': state['artifacts']['composed'],
        'composed_audit': state['artifacts']['composed_audit'],
        'runtime_audit': state['artifacts']['runtime_audit'],
        'test_case': file(run / 'test_case.json'),
        'candidate_effect_record': file(run / 'candidate_effect_record.json'),
        'new_candidate_exposure_ids': new_ids,
        'selected_new_candidate_ids': selected_new,
        'selected_all_candidate_ids': row['chosen_candidate_ids'],
        'new_fit_visual_profile_exposure_ids': profile_ids,
        'selected_visual_concept_ids': row['chosen_visual_concept_ids'],
        'literal_new_fit_evidence': literal,
        'new_candidate_native_status': native_status,
        'strict_fit_and_scene_gate_counts': counts,
        'strict_fit_and_scene_gates': pixel['gates'],
        'formal_review': file(run / formal_name),
        'formal_audit': audit_binding,
        'formal_audit_lane': formal_lane,
        'formal_record_valid': record_valid,
        'technical_qualification': 'pass' if formal['technical_qualified'] else 'fail',
        'formal_failed_gate_ids': [x['gate'] for x in formal['failed_hard_gates']],
        'user_judgment': formal['user_judgment'],
        'pixel_review': file(run / pixel_name),
        'whole_image_review': file(run / whole_name),
        'inspection_crop_provenance': file(run / 'inspection/crop_provenance.json'),
        'independent_manifest': file(run / 'run_manifest.json'),
        'capture_and_admission_limitation': audit_recovery,
    })

assert attempts[0]['creative_controls_sha256'] == attempts[1]['creative_controls_sha256']
assert all(x['formal_record_valid'] for x in attempts)
assert all(x['technical_qualification'] == 'fail' for x in attempts)
controls = read(read(root / 'workflow.json')['artifacts']['creative_controls']['path'])
projection = root / 'retry_context_1_properties_only'
result = {
    'schema_version': 'fashion-fit-arm-result/v1',
    'arm': 'arm_1',
    'status': 'completed_test_with_native_fidelity_failure',
    'concept': read(root / 'test_case.json')['concept'],
    'seed': read(root / 'test_case.json')['seed'],
    'seed_scope': 'Independent concept/control/retrieval randomness; native image_gen sampling seed is not exposed.',
    'cross_arm_inputs_used': False,
    'total_actual_image_gen_calls': 2,
    'actual_api_generation_calls': 0,
    'additional_generations_after_bounded_repair': 0,
    'first_ledger_row_preserved_by_value': True,
    'ledger': file(root / 'image_runs.ndjson'),
    'preserved_controls': {'canonical_sha256': controls['canonical_sha256'], 'controls': controls['controls'], 'adult_appeal': controls['adult_appeal'], 'resolved_emphasis': controls['resolved_emphasis']},
    'retry_projection': file(projection / 'retry_context.json'),
    'retry_projection_audit': file(projection / 'retry_projection_audit.json'),
    'retry_proof': file(projection / 'retry_proof.json'),
    'retry_decision': file(root / 'repair_decision_1_properties_only.json'),
    'retry_scope': read(child / 'test_case.json')['allowed_changes'],
    'fashion_fit_generation_diff': file(child / 'fashion_fit_generation_diff.json'),
    'source_comparison': 'The ff candidate extension changes only maintenance_ref.record_id and maintenance_ref.sha256 between these two generations. Its candidate meanings are unchanged; the visual-obligation extension is byte-identical. Concurrent unrelated corpus addition explains the new generation, without pre-core exposure.',
    'attempts': attempts,
    'data_effect_proof_boundary': {
        'new_candidate_exposure': 'pass',
        'compatible_new_candidate_adoption': 'pass',
        'literal_prompt_binding': 'pass',
        'same_garment_bilateral_native_relationship': 'fail_partial_not_pass_after_repair',
        'new_fit_visual_profiles': 'not_exposed_in_either_public_pack; no activation or profile pixel-pass claim',
        'causal_ablation': 'not_performed',
        'user_acceptance': 'not_yet_received',
    },
    'final_finding_ko': '신규 ff10_v2의 노출·선택·문구 바인딩은 확인했으나 양쪽 소매산 관계의 native 완전 실현은 실패했습니다. 수정본의 한쪽 raised/rolled edge, matching 차콜 바지와 cropped hem는 개선됐지만 반대쪽 ridge, 잠긴 앞단, 전체 허리밴드 및 뒤 밑단 가시성은 미충족입니다. 1회 기본+1회 bounded repair로 종료하며 사용자 판단은 미수신입니다.',
}
random_file = root.parent / 'independent_random_selection.json'
if random_file.is_file():
    result['independent_random_selection'] = file(random_file)
(root / 'arm_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
lines = [
    'arm_1 테스트를 기본 1회와 허용된 국소 수정 1회로 완료했습니다. 추가 생성과 API 전환은 없습니다. 독립 seed는 ' + str(result['seed']) + '이며 native 도구의 샘플 seed는 공개되지 않습니다.',
    '신규 ff10_v2는 두 공개 팩에서 노출·선택되었고 literal 관계 증거가 감사되었습니다. 신규 fit 시각 프로필은 양쪽 팩에서 노출되지 않아 활성화 성공을 주장하지 않습니다.',
    '첫 이미지와 수정 이미지는 strict custom 7개 중 각각 3개만 통과했습니다. 수정본의 화면 왼쪽 소매산은 raised/rolled edge와 접합선이 읽히지만 오른쪽에서 동등한 식별이 부족하여 전체 ff10 관계는 PARTIAL_NOT_PASS입니다. 버튼은 열려 있고 전체 허리밴드 양 끝과 양쪽 뒤 밑단 조건도 미충족입니다.',
    '첫 formal review는 managed record_valid PASS / technical FAIL(visibility)입니다. 수정 formal review는 동일 receipt 세대의 공식 worker·scale 감사와 실제 ledger/image/request 결합 검사에서 독립 record_valid PASS / technical FAIL(contact, visibility)입니다. 새 최종 contact 설명에 명시된 버튼 연결도 실패하기 때문에 최초 record와 서로 덮어쓰지 않습니다.',
    '수정 반환 메시지의 경로 추출 오류로 남은 preview_only 관측·원 operation 상태는 보존했습니다. 같은 실제 반환 바이트만 복사하고 지원되는 native-plan recorder로 ledger/manifest를 기록했습니다. 관리형 review admission은 preview_only 복구를 지원하지 않아 거절된 사실을 별도 기록하며, managed 성공 상태를 꾸며 쓰지 않았습니다.',
    '사용자 판단은 두 결과 모두 not_yet_received입니다. 기록의 형식 유효성, 미관, 데이터/프롬프트 감사는 native 핏 완전 실현이나 사용자 수용과 별개입니다.',
    '최초 이미지: ' + attempts[0]['image']['path'],
    '수정 이미지: ' + attempts[1]['image']['path'],
    '전체 증거와 파일 SHA: ' + str(root / 'arm_result.json'),
]
(root / 'arm_result.md').write_text('\n\n'.join(lines) + '\n')
print(json.dumps({'status': result['status'], 'summary': str(root / 'arm_result.json'), 'actual_image_calls': 2, 'custom_counts': [x['strict_fit_and_scene_gate_counts'] for x in attempts], 'formal_lanes': [x['formal_audit_lane'] for x in attempts]}, ensure_ascii=False))
