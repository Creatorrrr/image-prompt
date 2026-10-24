"""Reconcile immutable run artifacts without generating or selecting new images."""
import datetime
import gzip
import hashlib
import json
import os
import pathlib
import struct

ROOT = pathlib.Path('/Users/chasoik/Projects/image-prompt')
T = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
REF = pathlib.Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
EXPECTED_REF = '06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
SKILL = ROOT / 'skills/photo-prompt-image-generator/SKILL.md'
RENDER_SKILL_SHA = '83b3239eda5b5e26b1c51dad268258eb21a24f3dbca3b814517eb89169390cb8'
RELEASE = 'af8d87d5a4f61d4f6f93734d05ef4899da9de01159e53a1e6e840c2bc3d48bff'
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(p):
    return json.loads(pathlib.Path(p).read_text())


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def save(name, value):
    (T / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


assert sha(REF) == EXPECTED_REF
new = set(read(T.parent / 'integration-evidence/new-visual-cids.json'))
assert len(new) == 87
root_pixels = {
    'schema': 'root-original-pixel-review/v1',
    'reviewer': 'root; independent inspection after all actual images were generated',
    'review_scope': 'Unmodified, tool-returned original PNGs viewed at original resolution',
    'rule': ['partial_is_fail', 'UNOBSERVABLE_NOT_PASS'],
    'arms': {
        'a': {
            'reference_appearance': 'pass',
            'new_generic_attribute': 'pass',
            'new_attribute_evidence': 'APPROVED is readable within the physical lower rail of the empty wall frame; it was absent from the independently frozen baseline.',
            'whole_new_card': 'not_adopted_not_passed',
            'whole_prompt': 'fail',
            'failures': ['Clerk grip is right of the ruler geometric midpoint.', 'Face gaze is nearer the clerk face than the specified measuring hand.'],
            'bounded_success': 'Ruler ends, award top corners, supporting hands and connected clerk arm are visible together.',
        },
        'b': {
            'reference_appearance': 'pass',
            'new_generic_attribute': 'not_demonstrated',
            'whole_new_card': 'not_adopted_not_passed',
            'whole_prompt': 'fail',
            'failures': ['Image-right supporting palm is mostly occluded; fingertips do not establish the complete two-palm support relation.'],
            'bounded_success': 'Horizontal tag, clip, stamp base and towel upper contact are visible.',
        },
        'c': {
            'reference_appearance': 'pass',
            'new_generic_attribute': 'not_demonstrated',
            'whole_new_card': 'not_adopted_not_passed',
            'whole_prompt': 'fail',
            'failures': ['Second arrival boot and its exterior-step support endpoint are outside the frame.', 'Specified attention toward the print trail is weak.'],
            'bounded_success': 'Main person feet and hand-to-handle-to-mop-head-to-floor path are visible.',
        },
    },
    'claim_limit': 'Observed face/hair resemblance is not proof of identity, age or actual affiliation. Generic institutional satire is not proof of named-genre fidelity. A visible generic property does not qualify its complete source card.',
}

paths = {
    'a': ('a/actual-tool-input.json', 'a/final-prompt.txt'),
    'b': ('b/actual-tool-request.json', 'b/exact-prompt.txt'),
    'c': ('c/v5/native-started.json', 'c/v5/final-prompt.txt'),
}
arms = {}
external = {REF, SKILL}
for arm, (capture_path, prompt_path) in paths.items():
    run = ROOT / f'generated/photo-runs/marine-literature-retest-20261024-{arm}-v5'
    workflow = run / 'workflow.json'
    state = read(workflow)
    assert state['phase'] == 'review_record_validated'
    assert state['h_f2_binding']['generation_id'] == RELEASE
    external.add(workflow)
    data = {}
    for role, binding in state['artifacts'].items():
        file = pathlib.Path(binding['path'])
        assert sha(file) == binding['sha256'], (arm, role)
        external.add(file)
        if role in ('composed', 'render_request', 'native_plan', 'h_f2_material', 'review_audit'):
            data[role] = read(file)
    capture = read(T / capture_path)
    actual_args = capture['payload'] if arm == 'c' else capture['arguments']
    payload = data['native_plan']['payload']
    prompt = data['composed']['prompt_en']
    assert actual_args == payload
    assert prompt == data['render_request']['runtime_prompt_en'] == payload['prompt']
    assert prompt.encode() == (T / prompt_path).read_bytes()
    assert payload['referenced_image_paths'] == [str(REF)]
    assert data['composed'].get('negative_en') is None
    assert data['render_request'].get('runtime_negative_en') is None
    assert not data['composed']['chosen_candidate_ids']
    assert len(state['operations']) == 1
    operation = state['operations'][0]
    assert len(operation['attempts']) == 1 and operation['status'] == 'complete'
    audit = data['review_audit']['visual']
    assert audit['schema_failures'] == [] and audit['technical_qualified'] is False
    material = data['h_f2_material']
    candidates = [row for goal in material['goals'].values() for row in goal['candidates']]
    cids = {row['cid'] for row in candidates}
    new_exposed = cids & new
    assert len(candidates) == 40
    assert len(new_exposed) == (2 if arm == 'a' else 0)
    windows = {qid: sorted({x.split('|')[0] for x in goal['sampling']['window_ids']} & new)
               for qid, goal in material['goals'].items()}
    original = run / 'original.png'
    if arm == 'a':
        returned = pathlib.Path(capture['returned_local_path'])
    elif arm == 'b':
        returned = pathlib.Path(read(T / 'b/actual-tool-result.json')['returned_concrete_path'])
    else:
        returned = pathlib.Path(read(T / 'c/v5/tool-observation.json')['returned_local_path'])
    assert original.read_bytes() == returned.read_bytes()
    dimensions = struct.unpack('>II', original.read_bytes()[16:24])
    external.update((original, returned))
    arms[arm] = {
        'workflow': str(workflow), 'phase': state['phase'],
        'installed_generation': RELEASE,
        'all_registered_artifact_hashes_match': True,
        'composed_runtime_plan_actual_capture_exact': True,
        'actual_input_evidence': str(T / capture_path),
        'same_reference_path_and_sha256': True,
        'reference_sha256': EXPECTED_REF,
        'prompt_path': str(T / prompt_path),
        'prompt_utf8_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
        'original': str(original), 'tool_original': str(returned),
        'original_sha256': sha(original), 'png_dimensions': dimensions,
        'saved_copy_byte_identical': True,
        'actual_operations': 1, 'actual_attempts': 1,
        'actual_image_tool_calls': 1, 'actual_model': 'unknown',
        'operation_id': operation['operation_id'],
        'ledger_run_id': operation['attempts'][0]['run_id'],
        'issued_occurrences': len(candidates), 'unique_issued_CIDs': len(cids),
        'new_exposed_CIDs': sorted(new_exposed),
        'new_in_rank_windows': windows,
        'new_generic_attributes_retained': 1 if arm == 'a' else 0,
        'new_whole_contracts_selected': 0,
        'technical_qualified': False,
        'review_record_schema_valid': True,
        'failed_managed_hard_gates': audit['failed_hard_gates'],
        'pixel_review': root_pixels['arms'][arm],
    }
    root_pixels['arms'][arm].update(original=str(original), original_sha256=sha(original))

assert 'APPROVED' not in (T / 'a/baseline.txt').read_text()
assert 'APPROVED' in (T / 'a/final-prompt.txt').read_text()
candidate = ASSETS / 'photo_candidate_marine_literature_20261024.json'
semantics = ASSETS / 'photo_marine_literature_semantics_20261024.json'
assert sha(candidate) == read(T / 'source-repair-verification.json')['source_sha256']
external.update((candidate, semantics, ROOT / 'skills/photo-prompt-image-generator/tests/test_topic_title_discovery_scope.py'))
old_hashes = read(T / 'raw-source-hashes.json')
drift = {k: {'at_activation': v, 'at_final_observation': sha(ASSETS / k) if (ASSETS / k).exists() else None}
         for k, v in old_hashes.items() if not (ASSETS / k).exists() or sha(ASSETS / k) != v}
config_path = ROOT / 'skills/photo-prompt-image-generator/retrieval-runtime.json'
config = read(config_path)
store = pathlib.Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed')
current_gen = store / 'h-f2-generations' / config['generation_id']
indexed_text = gzip.decompress((current_gen / 'indexed-documents.json.gz').read_bytes()).decode()
default_new = sorted(cid for cid in new if cid in indexed_text)
raw_index = read(ASSETS / 'photo_candidate_search.json')
final = {
    'schema': 'marine-retest-final-observation/v1', 'observed_utc': STAMP,
    'source_candidate_hash': sha(candidate), 'source_semantics_hash': sha(semantics),
    'render_time_skill_sha256': RENDER_SKILL_SHA,
    'final_observed_skill_sha256': sha(SKILL),
    'skill_changed_after_render_pin': sha(SKILL) != RENDER_SKILL_SHA,
    'topic_substring_guidance_still_present': 'A conversation title can itself mix' in SKILL.read_text(),
    'tested_installed_generation': RELEASE,
    'default_selector_at_final_observation': config,
    'default_contains_new_visual_CIDs': len(default_new),
    'default_activation_by_this_task': False,
    'default_activation_status': 'HELD_CONCURRENT_SOURCE_ADVANCE',
    'raw_index_layout_at_final_observation': raw_index['layout_id'],
    'raw_source_drift_since_guarded_activation': drift,
    'raw_index_claim_limit': 'Activation was exact for the captured 120-file source closure. Later concurrent source edits are listed; this task does not claim the still-selected raw index represents those later edits.',
    'skill_claim_limit': 'All three image runs pinned the then-current SKILL hash before image calls. A later concurrent document revision is not claimed to have been exercised by these completed image calls.',
    'concurrency_policy': 'Preserve concurrent authored source and selector updates; keep verified marine releases explicitly installed without overwriting the default selector.',
    'user_acceptance': 'pending',
}
save('root-pixel-review.json', root_pixels)
save('FINAL-STATE.json', final)
save('test-results-summary.json', {
    'schema': 'marine-retest-results/v1', 'observed_utc': STAMP, 'arms': arms,
    'totals': {'independent_agents': 3, 'actual_image_calls': 3,
               'reference_appearance_pass': 3, 'new_generic_prompt_to_pixel_transfer_pass': 1,
               'new_whole_source_qualified': 0, 'whole_prompt_pixel_pass': 0,
               'managed_technical_qualified': 0},
    'c_record_metadata_correction': str(T / 'c/v5/metadata-correction.append.json'),
    'c_corrected_ledger_is_same_attempt_duplicate_not_extra_generation': True,
    'user_acceptance': 'pending',
})

def link(label, path):
    return f'[{label}]({path})'

rows = []
for arm, label in [('a', 'A: 빈 표창의 치수 검사'), ('b', 'B: 수건 검수 의례'), ('c', 'C: 청소 직후 다시 생기는 발자국')]:
    item = arms[arm]
    report = T / ('c/v5/report.md' if arm == 'c' else f'{arm}/report.md')
    transfer = '일반 속성 1건: 액자 레일 안 APPROVED' if arm == 'a' else '신규 노출 0, 전이 미입증'
    failure = {'a': '자 중앙 쥠·시선 불일치', 'b': '두 번째 지지 손바닥 가림', 'c': '도착자 두 번째 발·외부 지지점 프레임 밖'}[arm]
    rows.append(f"|{link(label, report)}|{len(item['new_exposed_CIDs'])}|{transfer}|PASS|FAIL: {failure}|{link('원본', item['original'])} · {link('프롬프트', item['prompt_path'])}|")
report = f'''# 해병문학 데이터 보완 및 독립 3개 재시험

보완 후 같은 첨부 사진으로 독립 에이전트 3개가 서로 다른 무작위 컨셉을 작성하고 이미지를 각 1회 생성했다. **신규 자료의 일반 속성은 A 한 장에서 프롬프트→실제 도구 입력→원본 픽셀까지 확인했다. 신규 카드 전체 자격은 0/3, 전체 프롬프트·엄격한 픽셀 합격도 0/3이다.** 세 장 모두 참조의 관찰 가능한 얼굴·머리 외형은 반영됐다.

## 원인과 실제 보완

검색 실패는 등록 누락 하나가 아니었다. 장르 의미와 업무 지시가 섞인 질의, 짧은 영어 사물명 부족, 상위 32개 창 밖의 낮은 순위, 창 안 자료의 균등 8개 표본 미노출, 노출 자료의 조건·소유자·장면 부적합을 구분했다. 주제를 정확한 원문 부분 `해병문학`으로 인용하고 87개 후보의 영어 명칭을 보강했다. 시각 의미 자료에는 인물 기준 좌우, 전체 연결, 지지면, 그림자 수신면을 확인하는 안내를 추가했다. 기존 관찰 계약과 게이트는 보존했고 진단 247개를 긍정 후보로 승격하지 않았다.

같은 코퍼스·구현·질의에서 이름/검색 문서/임베딩만 교체한 오프라인 비교에서 이전 실제 12질의의 신규 후보 출현 합계가 top-8 **0→7**, top-32 **4→18**로 늘었다. 이번 독립 슬롯·초안 12질의는 top-8 **0→3**, top-32 **0→5**였다. 이는 후보 출현 합계이며 채택률이나 독립 holdout 정확도가 아니다. 정확한 주제로 좁혀도 장르 검색 자체의 의미 구별은 아직 약하다.

{link('상세 원인·통제 비교·절차 한계', T / 'ANALYSIS.md')} · {link('검색 비교 원자료', T / 'retrieval-ablation.json')} · {link('87개 계약 보존 검증', T / 'source-repair-verification.json')}

## 실제 원본 판정

|시험|신규 고유 노출|신규 데이터의 최종 기여|참조 외형|전체 픽셀|증거|
|---|---:|---|---|---|---|
{os.linesep.join(rows)}

A의 신규 V090은 물리적 운반체 내부에 글자를 두는 일반 속성만 참고했다. 원래 표어판 카드의 모든 인물·조건·구성을 채택한 것은 아니다. `APPROVED`가 기준 초안에 없고 최종 문구와 실제 원본의 액자 아랫레일에 있음을 확인했다. A의 보수적인 전체 카드 거절은 작성자의 경계 판단이며, typed 성인 조건의 자동 충돌이 입증됐다는 뜻은 아니다.

B와 C는 신규 후보가 최종 표본에 없었다. 원래 초안의 병영·의례·작업복·복도나 기존 자료의 발밑 음영을 신규 전이로 세지 않았다. 일반적인 군대 풍자 분위기만으로 해병문학의 고유 주제가 성공했다고 판정하지 않았다. 일부 성공한 접촉을 전체 연결 성공으로 올리지 않았으며 `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지했다.

## 실행·검증 경계

- 후보 접근 전 독립 컨셉·기준 초안·controls·픽셀 기준을 작성했다. 제목의 업무 표현 혼입을 이미지 호출 전에 고치면서 원래 초안·슬롯 질의 문자를 유지했다. 따라서 마지막 v5를 새 눈가림 저술시험으로 부르지 않는다. 새 관리 표본 seed도 달라져 전후 노출 차이를 주제 수정 단독 효과로 주장하지 않는다.
- 최종 3개 run의 스킬 pin은 `{RENDER_SKILL_SHA}`이고 당시 실제 설치된 고정 세대 `{RELEASE}`를 사용했다. 생성 종료 후 다른 작업이 스킬 문서와 기본 선택자를 추가 갱신했다. 그 후속 버전을 이번 이미지로 검증했다고 주장하지 않는다.
- 각 run의 감사 프롬프트·runtime 문구·native plan·실제 호출 기록이 동일하고, 같은 JPEG 경로와 SHA를 사용했다. 저장 PNG는 도구 반환 원본과 바이트가 같다. 실제 이미지 도구 호출은 총 3회이며 반환되지 않은 모델 ID는 unknown이다.
- 의미/범위 회귀 13개 통과, 신규 87개 색인 등록, 진단 긍정 누출 0, 원본/네이티브 소스 334개 왕복 동일성을 확인했다. 리뷰 기록 유효성과 픽셀 합격은 별개다. 세 기록은 유효하지만 기술 자격은 모두 실패다.
- C 원래 ledger의 스킬 해시 오기입은 원본을 보존하고 명시적 append 보정했다. 별도 보정 ledger는 같은 실제 시도의 메타데이터 사본이며 4번째 이미지 생성이 아니다.

{link('전체 전이·호출·해시 집계', T / 'test-results-summary.json')} · {link('root 원본 픽셀 판정', T / 'root-pixel-review.json')} · {link('C 메타데이터 보정', T / 'c/v5/metadata-correction.append.json')}

## 반영 상태와 남은 개선

후보·시각 의미 소스와 작업 인덱스에는 보완을 적용했다. 실제 시험 세대와 추가 합본 세대는 설치해 두었다. 기본 런타임 선택자는 동시 작업의 새 소스 발행을 덮어쓰지 않도록 교체를 보류했다. 최종 관찰의 기본 세대 `{config['generation_id']}`에서 이번 신규 CID는 {len(default_new)}개다. 작업 인덱스 활성화 때는 입력 120개가 정확했지만 이후 동시 소스 변경 {len(drift)}개가 있으므로 최신 전체 소스와 일치한다고 주장하지 않는다. 시점별 값과 경계는 {link('최종 상태', T / 'FINAL-STATE.json')}에 남겼다.

다음 데이터 개선은 (1) 장르명과 관찰 가능한 병영 관계를 연결하는 출처 기반 의미 설명을 독립 질의로 검증하고, (2) 카드 전체의 연령/소유자 조건과 실제 속성별 조건을 감사해 과도한 포괄 조건을 분리하며, (3) 나이가 필요 없는 비성적 사물 관계는 별도 자격을 가진 자료로 작성하는 순서가 적절하다. 기존 카드의 성인 조건을 조용히 지우거나 일부 속성으로 전체 자격을 부여하지 않는다. 다음 이미지에서는 A의 기하학적 중앙과 시선 목표, B의 양 손바닥 노출, C의 두 발과 외부 계단을 각각 구도에서 확보해야 한다. 이 항목들은 이번에 완료한 수정으로 세지 않는다.

이번 요청의 분석·보완·3개 실제 생성·원본 검증은 완료했으며, 데이터와 이미지의 전체 합격은 미달이다. 사용자 수락은 아직 받지 않았다.
'''
(T / 'RESULTS.md').write_text(report)

# Hash only this round's evidence, plus exact external artifacts already reconciled.
# Prune heavyweight staging/index/model copies; do not walk or rewrite other tasks.
excluded = {'build', 'successor-skill', 'successor-store', 'raw-assets', 'raw-index-cache', '__pycache__', '.staging'}
files = set(external)
for directory, subdirs, names in os.walk(T):
    subdirs[:] = [x for x in subdirs if x not in excluded]
    for name in names:
        if name not in ('SHA256SUMS.RETEST', 'package-integrity.json'):
            f = pathlib.Path(directory) / name
            if f.is_file():
                files.add(f)
entries = [(str(f), sha(f)) for f in sorted(files)]
checksum = T / 'SHA256SUMS.RETEST'
checksum.write_text(''.join(f'{digest}  {path}\n' for path, digest in entries))
assert all(sha(path) == digest for path, digest in entries)
save('package-integrity.json', {
    'schema': 'marine-retest-evidence-integrity/v1', 'observed_utc': STAMP,
    'status': 'pass', 'verified_files': len(entries),
    'checksum_file': str(checksum), 'checksum_sha256': sha(checksum),
    'scope': 'This round evidence and exact external input/run/output artifacts; heavy staged runtimes and prior-round checksums excluded.',
    'claim_limit': 'An integrity snapshot at the observation time, not a claim that concurrently edited workspace files stay unchanged forever.',
})
print(json.dumps({'status': 'pass', 'verified_files': len(entries), 'actual_images': 3,
                  'whole_pixel_pass': 0, 'new_generic_transfer': 1,
                  'default_new_visuals': len(default_new),
                  'post_activation_source_drift': list(drift),
                  'report': str(T / 'RESULTS.md')}, ensure_ascii=False))
