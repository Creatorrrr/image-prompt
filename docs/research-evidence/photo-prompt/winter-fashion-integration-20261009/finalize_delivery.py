"""Export existing independent reviews and validate delivery bindings; no generation."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path('/Users/chasoik/Projects/image-prompt')
EVIDENCE = Path(__file__).resolve().parent
GENERATION = '922451d0548100a2825a0c2578ae3bee4f070f5b045b204c1af47731c9bce438'
REFERENCE_SHA = '06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
SKILL_SHA = '9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b'


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def workflow_artifact(workflow, key):
    return Path(workflow['artifacts'][key]['path'])


def export_b_existing_review():
    arm = EVIDENCE / 'arms/b'
    workflow = read(arm / 'run/workflow.json')
    ledger = [json.loads(s) for s in (arm / 'image_runs.ndjson').read_text().splitlines() if s.strip()]
    assert len(ledger) == 1
    run = ledger[0]
    winter = read(arm / 'winter_pixel_review.json')
    review = read(arm / 'render_review.json')
    audit = read(arm / 'render_review_audit_response.json')
    design = read(arm / 'independent_design.json')
    native = read(arm / 'native_tool_return_metadata.json')
    receipt = read(workflow_artifact(workflow, 'runtime_receipt'))
    exposure = read(arm / 'winter_exposure_selection.json')
    result = {
        'contract_version': 'winter-fashion-independent-result/v1',
        'arm_id': 'b',
        'task_state': 'first_attempt_test_complete_report_exported_by_coordinator',
        'report_export_provenance': {
            'exporter': 'root coordinator',
            'reason': 'Agent capacity error after independent pixel review, ledger, manifest and regular review audit had completed; same-agent export retry also hit capacity.',
            'independent_scene_prompt_generation_and_pixel_review_author': '/root/winter_coat_test',
            'agent_authored_source_records_unchanged': True,
            'new_generation_or_prompt_change_for_export': False,
        },
        'overall_strict_fidelity_result': 'fail',
        'concept': design['selected_concept'],
        'seed': design['random_seed'],
        'random_algorithm': design['random_algorithm'],
        'candidate_origin': design['candidate_origin'],
        'request_binding': read(EVIDENCE / 'DELEGATION-BINDINGS.json')['b'],
        'skill_sha256': run['skill_sha256'],
        'retrieval': {
            'pack_count': exposure['normal_retrieval_invocations'],
            'pack_id': run['pack_id'],
            'generation_id': receipt['generation_id'],
            'selected_new_winter_ids': exposure['selected_new_winter_candidate_ids'],
            'winter_opt_in_exposed': exposure['exposed_winter_visual_profile_ids'],
            'winter_opt_in_selected': exposure['selected_winter_visual_profile_ids'],
            'associated_bundle_profile_authority': 'advisory_only_not_promoted',
        },
        'native_generation': native,
        'ledger_run_id': run['run_id'],
        'regular_review': {
            'record_valid': audit['record_valid'],
            'audit_status': audit['status'],
            'technical_qualification': audit['technical_qualification'],
            'active_hard_gate_count': len(review['hard_gates']),
            'pass_count': sum(x['status'] == 'pass' for x in review['hard_gates'].values()),
            'fail_count': sum(x['status'] != 'pass' for x in review['hard_gates'].values()),
            'scope': 'Only active generic readability and embodiment gates; does not certify all winter goals or authored hand-side/hem order.',
        },
        'selected_winter_relation_pixels': winter['new_candidate_relations'],
        'independent_testcase_pixels': winter['checks'],
        'independent_goal_counts': winter['counts'],
        'additional_authored_fidelity_misses': winter['authored_fidelity_observations'],
        'user_judgment': winter['user_judgment'],
        'artifacts': {f: str(arm / f) for f in (
            'RESULT.json', 'REPORT.md', 'independent_design.json', 'independent_testcase_seal.json',
            'baseline_canonical.txt', 'final_prompt.txt', 'generated_image.png',
            'winter_exposure_selection.json', 'winter_pixel_review.json', 'render_review.json',
            'render_review_audit_response.json', 'image_runs.ndjson', 'run_manifest.json', 'run/workflow.json',
        )},
    }
    save(arm / 'RESULT.json', result)
    (arm / 'REPORT.md').write_text('''# B · 겨울 항구 승선 대기

독립 에이전트가 일반 지식의 6개 상황에서 seed `6236068004480667985`로 항구 컨셉을 골랐다. 과거 연구나 다른 arm을 보지 않고 core·baseline·목표를 봉인한 뒤 정상 pack 1개를 사용했다. 현재 스킬과 실제 첨부의 얼굴·헤어 참조로 native 이미지 1회만 생성했다. 재생성이나 fallback은 없다.

새 선택 관계 **2/2 PASS**, 원래 겨울 관찰 목표 **4/6 PASS**, 전체 복합 조건 **FAIL**이다. 같은 코트의 후드·목선 연결과 코트 아래 별도 얕은 누빔 층이 보인다. 하단 토글 두 쌍의 나무 막대는 식별되지 않고 중간 의복의 민소매 상태는 코트에 가린다. 별도 작성 조건인 스웨터/베스트 옷단 순서와 동작 손의 인물 기준 좌우도 원문과 다르다.

정규 review 기록 형식은 PASS이며 일반 가독성·신체 gate는 **8/8 PASS**다. 이 통과가 실패한 겨울 조건이나 손 좌우 조건을 인증하지 않는다. 새 겨울 opt-in 시각 프로필은 노출되지 않아 해당 경로는 미검증이다. 외관 참조는 동일 인물 보증이 아니며 요청자의 만족 판정은 아직 없다.

[프롬프트](final_prompt.txt), [원본 PNG](generated_image.png), [독립 픽셀 검토](winter_pixel_review.json), [정규 감사 반환](render_review_audit_response.json), [RESULT](RESULT.json).

독립 에이전트의 이미지 생성·검토·ledger·manifest·정규 감사 저장은 완료됐다. 마지막 보고서 출력과 동일 에이전트의 출력 재시도는 모델 용량 오류로 중단되어, 이 REPORT/RESULT는 조정자가 저장된 독립 기록에서 내보냈다. 원래 기록이나 프롬프트·이미지는 변경하지 않았다.
''')


def main():
    export_b_existing_review()
    bindings = read(EVIDENCE / 'DELEGATION-BINDINGS.json')
    mapping = read(EVIDENCE / 'AUTHORED-MAPPING.json')['mappings']
    owned_ids = {m[k] for m in mapping for k in ('candidate_id', 'bundle_id')}
    expected_source_hashes = {
        'skills/photo-prompt-image-generator/SKILL.md': SKILL_SHA,
        'skills/photo-prompt-image-generator/assets/photo_prompt_winter_fashion_extension.json': 'fedb671b06f4c47236c4aaa61eed652076e51412dedcd14d9ce6fc1aa7ab8dae',
        'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_winter_fashion.json': '06a662bd96d77890cb4b1f1d3791b3c656790bfaab28cbbf2ef7ab83c53ebe20',
    }
    checks = []

    def check(name, condition, detail=None):
        checks.append({'check': name, 'status': 'pass' if condition else 'fail', 'detail': detail})

    for path, expected in expected_source_hashes.items():
        actual = sha(ROOT / path)
        check('current_owned_source_identity:' + path, actual == expected, actual)
    configs = {
        'a': ('generated_result.png', 'final_prompt.txt', 0, 1, 4, 6, ['winter_wf36_v1']),
        'b': ('generated_image.png', 'final_prompt.txt', 2, 2, 4, 6, ['winter_wf25_v2', 'winter_wf33_v2']),
        'c': ('generated_image.native.png', 'final_prompt_en.txt', 3, 4, 3, 6, ['winter_wf30_v2', 'winter_wf78_v1', 'winter_wf01_v2', 'winter_wf65_v1']),
    }
    observations = {
        'a': 'Raised cables, colored knit motifs and shirt layer edges are visible. The adopted cardigan button does not join opposite front edges. One lower scarf end is occluded, and a returning string path around the branch cannot be established.',
        'b': 'Same-coat hood connection and separate shallow quilted inner layer are visible. The two lower opposing wooden toggles and sleeveless armhole are not assessable. Sweater/vest hem order and actor-relative acting-hand side differ from the authored prompt.',
        'c': 'Separate scarf ends, foremost tights interval and knit beneath an open coat are visible. A thick supporting slab under both forefoot and heel is absent; low block heels do not substitute for it. The collar boundary above the scarf is hidden.',
    }
    arms = []
    for arm_id, (image_name, prompt_name, relation_pass, relation_total, goal_pass, goal_total, concepts) in configs.items():
        arm = EVIDENCE / 'arms' / arm_id
        workflow = read(arm / 'run/workflow.json')
        rows = [json.loads(s) for s in (arm / 'image_runs.ndjson').read_text().splitlines() if s.strip()]
        check(arm_id + ':single_ledger_row', len(rows) == 1)
        run = rows[0]
        receipt = read(workflow_artifact(workflow, 'runtime_receipt'))
        packs = read(workflow_artifact(workflow, 'pack'))
        check(arm_id + ':single_normal_pack', isinstance(packs, list) and len(packs) == 1)
        pack = packs[0]
        composed_audit = read(workflow_artifact(workflow, 'composed_audit'))
        runtime_audit = read(workflow_artifact(workflow, 'runtime_audit'))
        review = read(workflow_artifact(workflow, 'visual_review'))
        audited = read(workflow_artifact(workflow, 'review_audit'))['visual']
        for key in ('pack', 'runtime_receipt', 'composed_audit', 'runtime_audit', 'visual_review', 'review_audit'):
            artifact = workflow['artifacts'][key]
            check(arm_id + ':workflow_artifact:' + key, sha(artifact['path']) == artifact['sha256'])
        image_path = arm / image_name
        image_sha = sha(image_path)
        with Image.open(image_path) as image:
            dimensions = list(image.size)
        check(arm_id + ':image_binding', run['image_hashes'] == [{'path': str(image_path), 'sha256': image_sha}])
        check(arm_id + ':first_native_success_without_retry', run['status'] == 'success' and run['attempt'] == 1 and run['image_call_count'] == 1 and run['retry_of'] is None and run['generation_environment'] == 'native_imagegen')
        check(arm_id + ':reference_binding', sha(bindings[arm_id]['reference']) == REFERENCE_SHA and run['reference_sha256'] == [REFERENCE_SHA])
        check(arm_id + ':request_envelope_binding', sha(bindings[arm_id]['envelope']) == bindings[arm_id]['envelope_file_sha256'])
        check(arm_id + ':same_source_generation', receipt['generation_id'] == GENERATION)
        check(arm_id + ':pack_identity', pack['pack_id'] == run['pack_id'])
        check(arm_id + ':final_prompt_matches_recorded_prompt', (arm / prompt_name).read_text().strip() == run['prompt_en'].strip())
        check(arm_id + ':audited_native_plan_identity', sha(run['native_render_plan_json']) == run['native_render_plan_sha256'])
        check(arm_id + ':compose_runtime_preflight_pass', composed_audit['status'] == 'pass' and runtime_audit['status'] == 'pass')
        check(arm_id + ':regular_review_record_valid', audited['schema_failures'] == [])
        selected_winter = [v for v in run['chosen_candidate_ids'] if v.split(':')[-1] in owned_ids]
        check(arm_id + ':selected_new_winter_count', len(selected_winter) == relation_total)
        check(arm_id + ':no_winter_profile_promoted', not any('winter_wf' in v for v in run['chosen_visual_concept_ids']))
        required = audited['required_hard_gates']
        hard_pass = sum(review['hard_gates'][gate]['status'] == 'pass' for gate in required)
        check(arm_id + ':hard_gate_count_matches_audit', len(required) == audited['required_hard_gate_count'])
        check(arm_id + ':review_image_identity', review['result_sha256'] == image_sha and review['result_image'] == str(image_path))
        check(arm_id + ':final_export_exists', (arm / 'RESULT.json').exists() and (arm / 'REPORT.md').exists())
        result = read(arm / 'RESULT.json')
        if arm_id == 'a':
            original_path = result['native_generation']['concrete_tool_returned_image']
            reported_counts = (result['pixel_review']['selected_new_winter_native_relation_pass_count'], result['pixel_review']['selected_new_winter_native_relation_total'])
        elif arm_id == 'b':
            original_path = result['native_generation']['native_returned_path']
            relations = result['selected_winter_relation_pixels']
            reported_counts = (sum(r['status'] == 'pass' for r in relations), len(relations))
        else:
            original_path = result['generation']['tool_reported_source_path']
            reported_counts = (result['selected_winter_relation_pixels']['pass_count'], result['selected_winter_relation_pixels']['total'])
        check(arm_id + ':original_native_bytes_preserved', sha(original_path) == image_sha)
        check(arm_id + ':new_relation_counts_match_independent_record', reported_counts == (relation_pass, relation_total))
        check(arm_id + ':winter_opt_in_not_exposed', 'winter_wf' not in json.dumps(pack['visual_concept_candidates']))
        arms.append({
            'arm_id': arm_id, 'image_path': str(image_path), 'sha256': image_sha,
            'dimensions': dimensions, 'review_scales': ['native'],
            'coordinator_observation': observations[arm_id],
            'selected_new_winter_ids': selected_winter, 'selected_concept_ids': concepts,
            'selected_new_relation_pass': relation_pass, 'selected_new_relation_total': relation_total,
            'original_sealed_goal_pass': goal_pass, 'original_sealed_goal_total': goal_total,
            'authored_original_goals_not_executed': 2 if arm_id == 'c' else 0,
            'regular_review_record_valid': not audited['schema_failures'],
            'active_generic_hard_gate_pass': hard_pass, 'active_generic_hard_gate_total': len(required),
            'full_complex_fidelity': 'fail', 'source_generation_id': receipt['generation_id'],
            'actual_image_call_count': run['image_call_count'],
            'final_prompt': str(arm / prompt_name), 'result': str(arm / 'RESULT.json'),
            'result_sha256': sha(arm / 'RESULT.json'), 'ledger_sha256': sha(arm / 'image_runs.ndjson'),
            'winter_direct_opt_in_profile_path': 'not_tested_no_exposure',
        })
    review = {
        'schema_version': 'winter-fashion-coordinator-pixel-review/v1',
        'reviewer': '/root', 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'Direct coordinator inspection of the saved originals; no regeneration or image modification. Cross-check against preserved independent agent reviews and exact artifact bindings.',
        'arms': arms,
        'summary': {'selected_new_relations_pass': 5, 'selected_new_relations_total': 7, 'full_complex_fidelity_pass': 0, 'full_complex_fidelity_total': 3, 'actual_native_image_calls': 3, 'retries': 0, 'fallbacks': 0},
        'boundaries': [
            'Only seven selected relations were tested; all 162 authored variants are not pixel-qualified.',
            'No winter visual-concept opt-in profiles were exposed; that path remains untested.',
            'No matched image before data integration was generated; no causal improvement conclusion.',
            'Two C original sock-endpoint objectives were omitted during agent-owned composition, not failed by the image model.',
            'Independence uses separate fork_turns=none tasks, recorded tool sequence and sealed authored provenance; hashes alone do not prove authorship order.',
            'Face/hair appearance reference is not an exact identity guarantee; user judgment is pending.',
            'B final export was performed by the coordinator after agent capacity errors; independent authored review records remain unchanged.',
        ],
    }
    save(EVIDENCE / 'COORDINATOR-PIXEL-REVIEW.json', review)
    validation = {'schema_version': 'winter-fashion-delivery-validation/v1', 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'pass' if all(c['status'] == 'pass' for c in checks) else 'fail', 'checks': checks, 'check_count': len(checks), 'new_test_execution': False, 'pixel_fidelity_result': 'partial_failures_preserved'}
    save(EVIDENCE / 'DELIVERY-VALIDATION.json', validation)
    assert validation['status'] == 'pass', [c for c in checks if c['status'] != 'pass']
    summary = read(EVIDENCE / 'AUTHORING-SUMMARY.json')
    summary['render_status'] = 'completed_three_independent_first_attempts_partial_failures'
    summary['render_summary'] = review['summary']
    save(EVIDENCE / 'AUTHORING-SUMMARY.json', summary)
    print(json.dumps({'status': validation['status'], 'checks': len(checks), 'render_summary': review['summary']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
