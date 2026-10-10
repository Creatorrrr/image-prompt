import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARM = ROOT.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
state = load(ROOT / 'run/workflow.json')
old_state = load(ARM / 'run/workflow.json')
bound = lambda role: load(state['artifacts'][role]['path'])
checks = {}
for role, info in state['artifacts'].items():
    checks['artifact_digest_' + role] = sha(info['path']) == info['sha256']
for role in ['request_raw', 'request_envelope_input', 'creative_controls', 'authorial_core_input', 'authorial_core_normalized', 'embodiment_review', 'feature_selection', 'baseline']:
    checks['neutral_bytes_equal_' + role] = Path(state['artifacts'][role]['path']).read_bytes() == Path(old_state['artifacts'][role]['path']).read_bytes()
checks['review_record_validated'] = state['phase'] == 'review_record_validated'
checks['technical_fail_preserved'] = state['technical_qualification'] == 'fail'
checks['current_generation'] = state['source_binding']['generation_id'] == 'c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14'
checks['current_fingerprint'] = state['source_binding']['source_fingerprint'] == 'c934e9f60126fe1f111ede9e80bf045907624404589b8d28fb45ebd669b73444'
ledger = [json.loads(x) for x in (ROOT / 'image_runs.ndjson').read_text().splitlines() if x.strip()]
manifest = load(ROOT / 'run_manifest.json')
composed = bound('composed')
plan = bound('native_plan')
review = bound('visual_review')
audits = bound('review_audit')
meta = load(ROOT / 'image_result_metadata.json')
checks['one_ledger_attempt'] = len(ledger) == 1 and ledger[0]['image_call_count'] == 1 and ledger[0]['attempt'] == 1
checks['manifest_native_one_call'] = manifest['image_call_count'] == 1 and manifest['generation_environment'] == 'native_imagegen'
checks['one_completed_operation'] = len(state['operations']) == 1 and state['operations'][0]['status'] == 'complete' and len(state['operations'][0]['attempts']) == 1
checks['no_cross_arm_inputs'] = manifest['cross_arm_inputs_used'] is False and ledger[0]['cross_arm_inputs_used'] is False
checks['prompt_exact'] = (ROOT / 'prompt_en.txt').read_text() == composed['prompt_en']
checks['tool_payload_exact'] = load(ROOT / 'native_tool_payload.json') == plan['payload']
checks['runtime_text_exact'] = plan['payload']['prompt'] == composed['prompt_en'] + '\n\nAvoid: ' + composed['negative_en']
checks['runtime_prompt_sha'] = hashlib.sha256(plan['payload']['prompt'].encode()).hexdigest() == ledger[0]['runtime_prompt_sha256']
refs = plan['payload']['referenced_image_paths']
checks['actual_single_reference_attachment'] = refs == ['/tmp/codex-remote-attachments/01a1212e-a00b-7170-8446-16480b2873ff/BAA7D121-91EF-4AF5-A73E-C42EEEE77809/1-사진-1.jpg']
checks['reference_exact_bytes'] = sha(refs[0]) == '048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c' == ledger[0]['reference_sha256'][0]
checks['actual_image_byte_copy'] = sha(meta['returned_source_path']) == sha(meta['saved_image_path']) == meta['image_sha256'] == manifest['image_hashes'][0]['sha256'] == review['result_sha256']
checks['review_hard_gate_count'] = len(review['hard_gates']) == 9
checks['review_status_count'] = sum(x['status'] == 'pass' for x in review['hard_gates'].values()) == 6 and sum(x['status'] == 'fail' for x in review['hard_gates'].values()) == 3
checks['review_schema_valid_but_not_qualified'] = not audits['visual']['schema_failures'] and audits['visual']['technical_qualified'] is False
checks['user_judgment_pending'] = review['user_judgment']['source'] == 'not_yet_received' and review['user_judgment']['genuinely_moe'] == 'pending'
checks['different_seeds_preserved'] = old_state['retrieval_seed'] == 1872214162960451119 and state['retrieval_seed'] == 7180700068034827031
checks['composed_audit_pass'] = bound('composed_audit')['status'] == 'pass'
checks['runtime_audit_pass'] = bound('runtime_audit')['status'] == 'pass'
assert all(checks.values()), [k for k, v in checks.items() if not v]
(ROOT / 'final_evidence_check.json').write_text(json.dumps({'status': 'pass', 'checks': checks, 'boundary': 'Artifact identity/record/schema verification only; it does not replace the authored direct-pixel judgments.'}, ensure_ascii=False, indent=2) + '\n')

result = {
    'arm_id': 'c', 'concept': 'harbor_hat_repair',
    'concept_random_seed': 10774828166673935651,
    'concept_random_method': 'Persisted independent Random(seed) uniform choice among four general-knowledge scene ideas; selected index 0 before candidate access.',
    'run': str(ROOT / 'run'), 'image_path': meta['saved_image_path'], 'image_sha256': meta['image_sha256'], 'dimensions': meta['dimensions'],
    'prompt_path': str(ROOT / 'prompt_en.txt'), 'prompt_sha256': hashlib.sha256(composed['prompt_en'].encode()).hexdigest(), 'prompt_word_count': len(composed['prompt_en'].split()),
    'native_tool_payload_path': str(ROOT / 'native_tool_payload.json'),
    'ledger_path': str(ROOT / 'image_runs.ndjson'), 'manifest_path': str(ROOT / 'run_manifest.json'), 'ledger_run_id': ledger[0]['run_id'],
    'generation_id': state['source_binding']['generation_id'], 'source_fingerprint': state['source_binding']['source_fingerprint'], 'pack_id': composed['pack_id'],
    'diagnostic_pack_id': '550a5b8eee6fe659', 'diagnostic_generation_id': '9037716cffb61fc18147ed9936b8181bd632378e7ff823cdfbcab4706f0f1af7',
    'retrieval_calls': {'diagnostic': 1, 'requalification': 1, 'arm_total': 2},
    'image_calls': {'native': 1, 'diagnostic': 0, 'repair': 0, 'api_fallback': 0},
    'retrieval_seeds': {'diagnostic': old_state['retrieval_seed'], 'requalification': state['retrieval_seed']},
    'neutral_eight_roles_byte_identical': True, 'matched_before_after_causal_experiment': False,
    'causal_limit': 'Core/controls match, retrieval seeds differ; evidence qualifies actual current-generation exposure, selections and first native pixels rather than causal improvement.',
    'core_sha256': ledger[0]['authorial_core_sha256'], 'controls_sha256': '22790c772c6c714a29e2f1bf12a4e05cf853bb8a0772fb469d731fce507268e2',
    'intent_lock_sha256': ledger[0]['intent_lock_sha256'], 'skill_sha256': ledger[0]['skill_sha256'], 'reference_sha256': ledger[0]['reference_sha256'][0],
    'controls': {'sensual': 1, 'fetish': 0, 'surreal': 0, 'creativity': 1, 'emphasis': 'sensual_led'},
    'new_wkr_exposure_unique': {'ordinary': 2, 'bundle': 2, 'visual': 2, 'clarification': 2},
    'chosen_candidate_ids': composed['chosen_candidate_ids'], 'chosen_visual_concept_ids': composed['chosen_visual_concept_ids'],
    'new_wkr_pixel_results': {'wkr_wk095_selected_relation': 'pass', 'wkr_wk047_selected_relation': 'fail'},
    'declined_new_relations': {'wkr_wk111': 'Requires a new foreground door plus garment-ribbon seam owner unrelated to the hat repair.', 'wkr_wk104': 'Continuous jacket sleeves do not supply separate upper-arm band/sleeve/bodice-gap relation.'},
    'composed_audit': {'status': bound('composed_audit')['status'], 'quality_status': bound('composed_audit')['quality_status'], 'failures': bound('composed_audit')['failures']},
    'runtime_audit': {'status': bound('runtime_audit')['status']},
    'native_review_record': {'valid': True, 'required_hard_gates': 9, 'passed': 6, 'failed': 3, 'technical_qualification': 'fail', 'failed_gate_ids': [k for k,v in review['hard_gates'].items() if v['status'] == 'fail']},
    'whole_image_impression': 'One natural and quietly attractive supported harbor hat repair; person/hands/hat read first and color/material/place form a coherent scene.',
    'supplemental_failures': ['Full pleat bundle continuity/topology', 'Ribbon-band anchor and shared airflow direction', 'Exact right-needle/thread/stitch ownership and endpoints', 'Opposite-shoulder crossbody route/plural attachment completeness', 'Tan boot shade renders medium brown'],
    'user_acceptance': 'pending_not_yet_received',
    'preserved_errors': [
        str(ARM / 'diagnostic_generation_9037716c'),
        str(ROOT / 'composition_audit_attempts/attempt_1'),
        str(ROOT / 'composition_audit_attempts/metadata_repair.json'),
        str(ROOT / 'native_payload_save_attempt_error.json'),
        str(ARM / 'execution_preparation_errors.ndjson'),
    ],
    'native_invocation_error': None, 'cross_arm_inputs_used': False,
    'git_commit_push': 'not_performed; arm-owned evidence files only',
}
(ROOT / 'result_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
lines = [
    'C 사례는 첨부 사진의 얼굴·헤어를 사용한 항구 모자 리본 수선 장면입니다. 내장 image_gen 최초 1장 생성·저장·원장 기록·원본 픽셀 평가를 완료했습니다. 구조적 감사와 리뷰 기록은 유효하지만 완전한 native 기술 합격은 **FAIL**, 사용자 평가는 대기입니다.',
    '',
    f"[최초 이미지]({meta['saved_image_path']}) · [최종 675단어 프롬프트]({ROOT / 'prompt_en.txt'}) · [실제 native 전달 인수]({ROOT / 'native_tool_payload.json'}) · [원장]({ROOT / 'image_runs.ndjson'}) · [run manifest]({ROOT / 'run_manifest.json'})",
    '',
    '| 증거 층 | 결과 |', '|---|---|',
    '| 구성 감사 | PASS, requester anchor의 자유 서술 보존 관련 quality warning 4개 |',
    '| Native 전달 감사 | PASS, 실제 참조 첨부 1개 |',
    '| 이미지 호출/복사 | native 1회, 1024×1536, 원본과 byte 동일 |',
    '| 픽셀 리뷰 기록 감사 | PASS: record_valid=true, schema 오류 없음 |',
    '| 필수 native 조건 | 9개 중 6 PASS / 3 FAIL, technical_qualification=fail |',
    '| 전체 인상 | 일관된 항구 수선, 의상·색·장소가 자연스럽게 연결됨 |',
    '| 사용자 수락 | pending / not_yet_received |',
    '',
    '신규 노출은 ordinary 2 / bundle 2 / visual 2 / clarification 2입니다. WK095 ordinary를 같은 치마와 벤치 좌면의 압축 접힘으로 채택해 픽셀 PASS를 확인했습니다. WK047 visual opt-in은 같은 재킷 커프의 직조와 박음질 인접 관계로 채택했지만, 가는 실의 얽힘이 해결되지 않아 FAIL입니다. WK111은 문 가림과 의복 리본 접합이 새로 필요하고, WK104는 별도 위팔 소매/몸판 틈이 없으므로 거절했습니다. 중복 bundle은 동일 관계를 다시 채택하지 않았습니다.',
    '',
    '| 필수 조건 | 판정 |', '|---|---|',
]
for gid, value in review['hard_gates'].items():
    lines.append(f"| {gid} | {value['status'].upper()} ({', '.join(value['reviewed_scales'])}) |")
lines += [
    '',
    '커프 미세 얽힘, 오른손-바늘-새 스티치의 완전한 접합과 가시성 때문에 3개 필수 조건이 실패했습니다. 손과 접촉점의 광학 가독성은 통과하며, 바늘 소유의 실패와 구분했습니다. 별도 관계 검토에서도 주름의 위쪽 끝–밑단 연속성, 모자 밴드–리본 끝의 같은 앵커 및 공유 바람 방향, 가방의 opposite-shoulder 사선 경로와 여러 접합 끝점은 부분 실패로 보존했습니다. 전체 인상을 이유로 미세 관계를 합격시키지 않았습니다.',
    '',
    f"[정확한 hard-gate 리뷰]({ROOT / 'visual_review.json'}) · [소유자/끝점/수량/지역 물성 관찰]({ROOT / 'supplemental_pixel_review.json'}) · [전체 인상/controls 리뷰]({ROOT / 'whole_image_review.json'}) · [1:1 crop/thumbnail 증거]({ROOT / 'pixel_inspection/inspection_manifest.json'}) · [파일·호출 일치 검증]({ROOT / 'final_evidence_check.json'})",
    '',
    f"현재 generation={result['generation_id']}, fingerprint={result['source_fingerprint']}, pack={result['pack_id']}. 최초 진단 pack 550a5b8eee6fe659는 보존했고 재사용하지 않았습니다. 각 run은 정확히 1회 조회(arm 총 2회), 이미지 arm 총 1회, repair/API fallback 0회입니다.",
    '',
    '진단 retrieval_seed=1872214162960451119, 재검증=7180700068034827031. neutral 8역할/core/baseline/controls는 byte 동일하지만 검색 seed가 달라 **matched before/after 인과 실험은 아닙니다**. 현 세대의 실제 노출·선택·첫 픽셀 사용을 검증했습니다.',
    '',
    f"이미지 SHA256: `{result['image_sha256']}`. Prompt SHA256: `{result['prompt_sha256']}`. Core SHA256: `{result['core_sha256']}`. Controls SHA256: `{result['controls_sha256']}`. Effective visual SHA256: `{manifest['effective_visual_contract_sha256']}`.",
    '',
    '독립 일반 지식의 4개 후보 장면에서 저장한 seed 10774828166673935651의 균등 추출(index 0)로 사례를 골랐습니다. 다른 arm 입력은 사용하지 않았습니다. sensual 1 / fetish 0 / surreal 0 / creativity 1을 처음부터 유지했습니다. 사진은 눈에 보이는 얼굴·헤어만 안내하며 신원·실제 연령·성격·몸매·이력은 추론하지 않았습니다.',
    '',
    '최초 진단 감사 실패와 재구성 메타데이터 인용 개수 실패, native payload 보존 도우미의 status 이름 가정 오류를 모두 보존했습니다. 전자는 중복 인용만 제거했으며 positive prompt는 바꾸지 않았습니다. 실제 image_gen 오류나 차단은 없었습니다. 내장 recorder의 원장 ts는 operation 예약 시각이며 실제 호출 시작/종료는 image_result_metadata.json에 별도로 보존했습니다. 이미지 재시도 및 별도 수리 렌더는 하지 않았습니다.',
    '',
    '최종 positive prompt:', '', '```text', composed['prompt_en'], '```', '',
    '최종 negative prompt:', '', '```text', composed['negative_en'], '```', '',
    '실제 전송은 positive 문장 뒤에 정확히 두 줄바꿈과 `Avoid: ` 및 위 negative 문장을 붙였습니다. 첫 이미지 생성 뒤 prompt를 수정하지 않았습니다.',
]
(ROOT / 'REPORT.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'evidence_checks': len(checks), 'evidence_status': 'pass', 'report': str(ROOT / 'REPORT.md'), 'summary': str(ROOT / 'result_summary.json'), 'native_qualification': 'fail', 'hard_gate_pass': 6, 'hard_gate_fail': 3}, ensure_ascii=False))
