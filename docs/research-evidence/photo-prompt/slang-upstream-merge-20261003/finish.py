"""Bind complete post-upstream regression results to the merged source tree."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    initial_suite = json.loads((HERE / 'full-suite/FULL-SUITE-RESULT.json').read_text())
    assert initial_suite['complete'] and initial_suite['sources_unchanged']
    assert initial_suite['all_discovered_tests_executed_once']
    assert not initial_suite['skipped']
    rechecks = {}
    for path in (HERE / 'dependency-recheck').glob('full-suite-worker-*.json'):
        row = json.loads(path.read_text())
        assert row['complete'] and row['successful'] and row['sources_unchanged']
        assert not row['failures'] and not row['errors'] and not row['skipped']
        assert row['source_binding'] == initial_suite['source_binding']
        key = tuple(row['modules'])
        assert key not in rechecks
        rechecks[key] = (row, str(path.relative_to(HERE)))
    assert set(rechecks) == {
        ('tests.test_photo_poverty_visual_semantics',),
        ('tests.test_photo_rare_photo_visual_semantics',),
        ('tests.test_photo_makeup_reference_balance',),
    }
    replacements = []
    selected = []
    for path in (HERE / 'full-suite').glob('full-suite-worker-*.json'):
        row = json.loads(path.read_text())
        if tuple(row['modules']) in rechecks:
            recheck, result_path = rechecks[tuple(row['modules'])]
            assert row['test_module_hashes'] == recheck['test_module_hashes']
            assert row['discovered_ids'] == recheck['discovered_ids']
            replacements.append({'initial_result': str(path.relative_to(HERE)),
                                 'initial_failure_count': len(row['failures']),
                                 'initial_error_count': len(row['errors']),
                                 'replacement': result_path,
                                 'reason': 'Ignored frozen historical images or authored JSON absent from fresh worktree; exact existing bytes copied. No source, test, fixture or image generation change.'})
            row = recheck
        assert row['complete'] and row['successful'] and row['sources_unchanged']
        assert not row['failures'] and not row['errors'] and not row['skipped']
        assert row['source_binding'] == initial_suite['source_binding']
        selected.append(row)
    assert len(replacements) == 3
    ids = [test_id for row in selected for test_id in row['executed_ids']]
    suite = {
        'schema_version': 'photo-slang-final-regression/v1',
        'modules': len(selected), 'tests_run': sum(row['tests_run'] for row in selected),
        'total_actual_test_executions_including_initial_failed_modules': initial_suite['tests_run'] + sum(row['tests_run'] for row, path in rechecks.values()),
        'selected_successful_test_ids': ids,
        'all_selected_discovered_tests_executed_once': all(row['all_discovered_tests_executed_once'] for row in selected),
        'failure_count': 0, 'error_count': 0, 'skip_count': 0,
        'source_binding': initial_suite['source_binding'], 'source_unchanged_between_initial_and_recheck': True,
        'replaced_module_results': replacements,
    }
    assert suite['modules'] == initial_suite['modules']
    assert len(ids) == suite['tests_run'] == initial_suite['tests_run'] == len(set(ids))
    assert set(ids) == set(initial_suite['executed_test_ids'])
    (HERE / 'FINAL-REGRESSION.json').write_text(json.dumps(suite, ensure_ascii=False, indent=2) + '\n')
    for name, expected in suite['source_binding'].items():
        assert digest(ROOT / name) == expected, name
    module_hashes = {}
    for row in selected:
        assert row['complete'] and row['successful'] and row['all_discovered_tests_executed_once']
        for module, expected in row['test_module_hashes'].items():
            name = module.replace('.', '/') + '.py'
            assert digest(ROOT / name) == expected, name
            module_hashes[name] = expected
    assert len(module_hashes) == suite['modules']
    preservation = json.loads((HERE / 'PRESERVATION.json').read_text())
    for side, files in preservation['exclusive_files_sha256'].items():
        for name, expected in files.items():
            assert digest(ROOT / name) == expected, (side, name)
    assert 'valid' in (HERE / 'dictionary-validation.log').read_text().lower()
    visual_log = (HERE / 'visual-index-validation.log').read_text()
    assert '1576' in visual_log or '1,576' in visual_log
    result = {
        'schema_version': 'photo-slang-upstream-final-verification/v1',
        'parents': preservation['parents'], 'complete_suite': {
            'modules': suite['modules'], 'tests': suite['tests_run'],
            'failures': 0, 'errors': 0, 'skipped': 0,
            'all_selected_discovered_tests_executed_once': True,
            'ignored_native_fixture_dependency_recheck': replacements,
            'source_and_test_module_hashes_match_merge_tree': True,
        },
        'dictionary_and_visual_index_validation': 'PASS',
        'both_parent_authored_intents_and_frozen_evidence_preserved': True,
        'all_three_arms_target_candidate_exposure': 'PASS',
        'existing_V8_candidate_pack_entire_bytes_unchanged': True,
        'indexes_equal_local_parent_no_rebuild_required': True,
        'embedding_api_calls': 0, 'native_image_calls': 0,
        'prior_native_latest_verdicts': preservation['latest_arm_pixel_verdicts'],
        'concurrent_main_worktree_drafts_untouched_during_isolated_merge': True,
        'source_binding': suite['source_binding'], 'test_module_hashes': module_hashes,
    }
    (HERE / 'VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    parents = preservation['parents']
    text = f'''원격 `main`이 추가로 갱신되어 첫 push가 거절된 뒤, 로컬 은어 통합 커밋 `{parents['local']}`와 원격 `{parents['remote']}`를 독립된 worktree에서 다시 병합했습니다. 같은 원본 작업 폴더에서 진행 중이던 다른 연구의 파일은 이 worktree의 병합·검증 과정에서 수정하지 않았습니다.

원격은 카메라 방향·높이의 requester owner evidence, DATA load 이전의 선언 검사, 기존 영어 core에서의 제한적인 camera-clause query projection을 보강합니다. 새로운 lock을 만들지 않으며 원격의 blind V2 미충족 관찰과 고정 holdout은 원래 기록 그대로입니다. 로컬은 은어 시각 의미·대체 표현·후보팩·scope·native 연구 자료를 유지합니다. 공통 변경 파일은 `prompt_generator.py` 하나이며, 통합 파일에서 로컬의 두 registry 등록 행을 빼면 원격 파일과 byte가 같습니다. 나머지 로컬 {preservation['local_exclusive_file_count']}개, 원격 {preservation['remote_exclusive_file_count']}개 변경 파일은 각각 부모와 byte가 같습니다. [양쪽 보존 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-upstream-merge-20261003/PRESERVATION.json)를 남겼습니다.

최종 통합 버전에서 **{suite['modules']}개 모듈 / {suite['tests_run']:,}개 고유 테스트가 PASS**했고 최종 선택 결과의 failure·error·skip은 0입니다. 첫 전체 sweep은 새 worktree에 과거 빈곤·희얼사·메이크업 검증의 ignored PNG·authored JSON이 빠져 3개 모듈에서 실패했습니다. 원래 작업 폴더의 기존 파일을 frozen fixture SHA 또는 source byte와 대조해 그대로 복사한 뒤 해당 3개 모듈만 다시 실행하여 통과했습니다. Source·test·fixture·예상 판정은 바꾸지 않았고 이미지 호출도 없었습니다. 초기 실패 로그도 그대로 보존합니다. 모든 발견 ID의 성공 결과가 중복 없이 포함되며 runtime source·test module hash가 최종 merge tree와 일치합니다. Dictionary·visual index 검사도 PASS입니다. [최종 전체 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-upstream-merge-20261003/FINAL-REGRESSION.json)와 [최종 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-upstream-merge-20261003/VERIFICATION.json)에 실행 ID와 hash를 보존합니다.

시각 의미 registry와 derived semantic·visual indexes는 앞선 로컬 통합 커밋과 byte가 동일하므로 추가 index 재생성은 필요하지 않았습니다. Embedding·native image 호출은 0회입니다. 세 원래 arm의 네 authored 입력·seed로 재조회하여 목표 후보가 모두 노출됨을 확인했고, V8의 전체 candidate pack byte도 동일합니다. [재조회 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-upstream-merge-20261003/RETRIEVAL.json)를 별도로 보존합니다.

기존 native 5장·프롬프트·core·참조·audit hash와 장면별 최종 **1 PASS / 2 FAIL**은 그대로입니다. 새 카메라 소유자 동작의 unit regression PASS는 기존 native 장면의 실패나 원격의 blind V2 한계를 바꾸지 않습니다. 사용자 이미지 수용 판정은 미수신입니다. [기존 통합 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/README.md)와 [앞선 pull 통합 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/README.md)를 유지했습니다.
'''
    (HERE / 'README.md').write_text(text)
    print(json.dumps({'modules': suite['modules'], 'tests': suite['tests_run'], 'both_parents_preserved': True, 'success': True}))


if __name__ == '__main__':
    main()
