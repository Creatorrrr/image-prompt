"""Bind three completed native cases and coordinator observations to exact bytes.

This is an evidence finalizer, not a pixel classifier or a rendering adapter.
The observations below were authored after directly viewing the three unchanged
native PNGs and their inspection thumbnails. No runtime source is mutated here.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import struct

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
WT = Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
GENERATION = 'a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c'
SOURCE = '6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a'
SKILL = '9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b'
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
REFERENCE_SHA = '06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


CONFIG = {
    'knit_layer': {
        'label_ko': '강변 인쇄 공방의 첫 도판과 봄바람',
        'prompt_name': 'prompt_en.txt', 'manifest_name': 'run_manifest.json',
        'thumbnail': 'review_views/thumbnail.png',
        'expected_new_topic': [4, 5], 'expected_hard': [11, 11],
        'profile_claim': 'spring_sf057_02 explicitly selected and native-qualified; spring_sf104_2 not hard-activated',
        'topic_observations_ko': [
            '아이보리 베스트의 연속된 실 경계가 반복된 열린 셀을 둘러싼다. 셀 내부의 복숭아색 직물과 세이지색 안쪽 상의가 불투명한 실과 구별된다.',
            '복숭아색 블라우스의 투과, 커프·밑단 경계와 접힌 곳의 밀도 변화가 같은 직물 면에서 이어진다.',
            '블라우스와 스커트는 같은 착용자의 가까운 저채도 따뜻한 색이다. 그러나 사전 관찰표가 지정한 스커트 허리단은 블라우스 아래 가려져 있으므로 해당 끝점은 실패다.',
        ],
        'body_observations_ko': '오른손과 금속 클립·종이 상단·팽팽한 줄이 만나는 부분, 왼손이 아래 종이를 받치는 부분과 각 팔 연결이 읽힌다. 두 발은 바닥에 놓여 있다.',
        'supplemental_failures_ko': ['스커트 허리단 가림; 예정한 세 층의 모든 경계는 완전 관찰 불가'],
        'impression_ko': '창빛과 바람, 종이를 고정하는 행동 및 세 겹의 재료 차이가 공방의 현재 순간으로 연결된다.',
    },
    'bodice_hem': {
        'label_ko': '옥상 건조줄의 마지막 청사진',
        'prompt_name': 'final-prompt.txt', 'manifest_name': 'run_manifest.json',
        'thumbnail': 'review-thumbnail.png',
        'expected_new_topic': [9, 9], 'expected_hard': [8, 8],
        'profile_claim': 'spring_sf004_01 and spring_sf104_2 opt-ins were not exposed; no hard activation qualification',
        'topic_observations_ko': [
            '블라우스 목둘레는 가로 하단과 양쪽 올라가는 경계가 같은 두 모서리에서 이어지는 스퀘어 형태다. U/V나 뒤의 건조줄로 대체하지 않는다.',
            '따뜻한 베이지색 상의와 아이보리색 아래 의복이 같은 착용자에게 있다. 바깥으로 퍼지는 페플럼 끝과 그 아래 평평한 직물 면이 분리된다.',
            '이 arm의 사전 색 관찰 기준은 페플럼 끝과 아래 스커트 면이다. A arm의 별도 허리단 노출 기준을 사후에 추가하지 않는다. 숨은 봉제 연결이나 섬유 성분은 판정하지 않는다.',
        ],
        'body_observations_ko': '오른손이 탁자 위 파란 종이를 누르며 손가락 앞의 접힌 종이가 남아 있다. 왼손은 떨어진 나무 클립을 옆에 들고 있다. 얼굴·손·옥상 난간이 축소 화면에서도 구별된다.',
        'supplemental_failures_ko': ['레이스의 개별 둥근 끝은 thumbnail에서 전부 추적할 수 없어 보충 관찰 실패'],
        'impression_ko': '청사진의 차가운 파랑과 따뜻한 옷이 분리되고, 종이를 멈춘 순간의 시선과 옥상 공간이 자연스럽게 연결된다.',
    },
    'ornament_shoe': {
        'label_ko': '비 뒤 첫 배를 기다리는 접힌 항로',
        'prompt_name': 'prompt.en.txt', 'manifest_name': 'independent-run-manifest.json',
        'thumbnail': 'inspection/thumbnail.png',
        'expected_new_topic': [10, 10], 'expected_hard': [8, 10],
        'profile_claim': 'spring_sf071_1 and spring_sf107_02 opt-ins were not exposed; no hard activation qualification',
        'topic_observations_ko': [
            '세이지색 앞판의 두 위 모서리에 같은 원피스 어깨끈이 각각 연결된다. 앞판과 끈이 별도 살구색 블라우스 앞에 있고, 블라우스의 소매와 목 경계가 따로 남아 있다.',
            '양쪽 아이보리색 신발을 각각 확인했다. 각 발등을 가로지르는 실체 스트랩과 같은 신발의 안쪽·바깥쪽 연결이 보인다. 발목 리본을 그 스트랩 대신 사용하지 않는다.',
            '앞판에서 허리 연결과 사선 겹침, 아래 플리츠 및 밑단으로 이어지는 세이지색 의복은 한 벌로 읽힌다.',
        ],
        'body_observations_ko': '오른팔과 손은 종이 모서리의 나무 클립까지 연결되고 왼손·골반·두 발은 벤치와 바닥의 지지를 받는다. 그러나 같은 클립 턱이 종이와 와이어를 함께 잡는 끝점은 보이지 않는다. 접촉 및 그 접촉의 가시성은 실패다.',
        'supplemental_failures_ko': [
            '꽃은 지정한 블라우스보다 세이지색 어깨끈 위에 붙어 있다',
            '블라우스의 지정 대각선 주름 경로와 신발에서 발목 매듭으로 이어지는 완전한 리본 경로가 부족하다',
            '배를 향한 반응보다 카메라 쪽 얼굴과 게시판의 종이가 강조된다',
        ],
        'impression_ko': '젖은 선착장과 부드러운 옷의 관계는 설득력 있지만, 종이를 와이어에 다시 고정한다는 인과적 사건은 완성되지 않았다.',
    },
}

assert sha(REFERENCE) == REFERENCE_SHA
for root in [ROOT, WT]:
    assert sha(root / 'skills/photo-prompt-image-generator/SKILL.md') == SKILL

bindings = read(OUT / 'INDEPENDENT-ARM-BINDINGS.json')
copies = {row['arm']: row for row in read(OUT / 'NATIVE-IMAGE-COPIES.json')['images']}
cases = []
observations = []
for binding in bindings['arms']:
    arm = binding['arm']
    config = CONFIG[arm]
    directory = OUT / 'arms' / arm
    result = read(directory / 'stage2-result.json')
    state = read(directory / 'run/workflow.json')
    assert state['phase'] == 'review_record_validated'
    artifacts = state['artifacts']
    for role, artifact in artifacts.items():
        assert sha(artifact['path']) == artifact['sha256'], (arm, role)
    freeze = read(binding['freeze_receipt_path'])
    assert sha(binding['freeze_receipt_path']) == binding['freeze_receipt_sha256']
    assert freeze['contracts']['core'] == binding['core_canonical_sha256']
    for role, expected in freeze['files'].items():
        assert sha(artifacts[role]['path']) == expected, (arm, 'frozen', role)
    receipt = read(artifacts['runtime_receipt']['path'])
    assert receipt['generation_id'] == GENERATION and receipt['source_fingerprint'] == SOURCE
    manifest_path = directory / config['manifest_name']
    manifest = read(manifest_path)
    assert manifest['skill_sha256'] == SKILL and GENERATION in manifest['source_ref']
    assert manifest['authorial_core_sha256'] == binding['core_canonical_sha256']
    assert manifest['reference_sha256'] == [REFERENCE_SHA]
    assert manifest['cross_arm_inputs_used'] is False and manifest['image_call_count'] == 1
    ledger_path = directory / 'image_runs.ndjson'
    ledger = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]
    assert len(ledger) == 1
    row = ledger[0]
    assert row['image_call_count'] == 1 and row['status'] == 'success'
    assert row['authorial_core_sha256'] == binding['core_canonical_sha256']
    assert row['reference_sha256'] == [REFERENCE_SHA]
    assert row['run_id'] == manifest['ledger_run_id']
    assert row['runtime_prompt_sha256'] == manifest['runtime_prompt_sha256']
    prompt_path = directory / config['prompt_name']
    assert prompt_path.read_text().strip('\n') == row['prompt_en']
    copy = copies[arm]
    for path in [copy['native_saved_path'], copy['delivery_path']]:
        assert sha(path) == copy['sha256']
        raw = Path(path).read_bytes()
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        assert struct.unpack('>II', raw[16:24]) == (1024, 1536)
    assert row['image_hashes'][0]['sha256'] == copy['sha256']
    shape = read(artifacts['visual_review_shape']['path'])
    review = read(artifacts['visual_review']['path'])
    gates = review['hard_gates']
    if isinstance(gates, list):
        gates = {item['id']: item for item in gates}
    assert set(gates) == set(shape['review']['hard_gates'])
    assert review['result_sha256'] == copy['sha256']
    passed = sum(gate['status'] == 'pass' for gate in gates.values())
    assert [passed, len(gates)] == config['expected_hard']
    for definition in shape['gate_definitions']:
        scale = definition.get('review_scale', 'native')
        expected = {'native', 'thumbnail'} if scale == 'both' else {scale}
        assert expected <= set(gates[definition['id']]['reviewed_scales'])
    audit = read(artifacts['review_audit']['path'])['visual']
    assert not audit['schema_failures']
    assert audit['technical_qualified'] == (passed == len(gates))
    assert audit['user_judgment']['source'] == 'not_yet_received'
    if arm == 'knit_layer':
        counts = result['supplemental_new_candidate_review']
        observed = [counts['pass_count'], counts['pass_count'] + counts['fail_count']]
    elif arm == 'bodice_hem':
        counts = result['supplemental_topics']
        observed = [counts['pass_count'], counts['observation_count']]
    else:
        counts = result['pixels']['new_candidate_supplemental_all_of']
        observed = [counts['passed'], counts['total']]
    assert observed == config['expected_new_topic']
    failed = [key for key, gate in gates.items() if gate['status'] != 'pass']
    new_topic_pass = observed[0] == observed[1]
    binding.update({
        'generation': GENERATION, 'source_fingerprint': SOURCE,
        'image_call_count': 1, 'image_sha256': copy['sha256'],
        'delivery_image_path': copy['delivery_path'], 'ledger_run_id': row['run_id'],
        'stage2_result_path': str(directory / 'stage2-result.json'),
        'final_workflow_artifact_hashes_verified': len(artifacts),
        'frozen_file_hashes_verified': len(freeze['files']),
    })
    case = {
        'arm': arm, 'concept_ko': config['label_ko'],
        'stage2_result': {'path': str(directory / 'stage2-result.json'), 'sha256': sha(directory / 'stage2-result.json')},
        'prompt': {'path': str(prompt_path), 'file_sha256': sha(prompt_path), 'text_sha256': hashlib.sha256(row['prompt_en'].encode()).hexdigest()},
        'testcase_path': str(directory / 'TESTCASE.md'),
        'manifest': {'path': str(manifest_path), 'sha256': sha(manifest_path)},
        'ledger': {'path': str(ledger_path), 'sha256': sha(ledger_path), 'run_id': row['run_id']},
        'runtime_receipt': artifacts['runtime_receipt'], 'generation_id': GENERATION,
        'source_fingerprint': SOURCE, 'skill_sha256': SKILL, 'reference_sha256': REFERENCE_SHA,
        'image': copy, 'image_dimensions': [1024, 1536], 'actual_image_call_count': 1,
        'new_topic_all_of': {'passed': observed[0], 'total': observed[1], 'status': 'pass' if new_topic_pass else 'fail', 'classification': 'separate_supplemental_observation'},
        'effective_hard_gates': {'passed': passed, 'total': len(gates), 'status': 'pass' if not failed else 'fail', 'failed_ids': failed},
        'selected_topic_and_effective_hard_set_joint_result': 'pass' if new_topic_pass and not failed else 'fail',
        'additional_authorial_observations': 'contains_failures; see original per-arm supplemental record',
        'profile_activation_claim': config['profile_claim'],
        'user_acceptance': 'not_yet_received', 'observed_image_model': None,
    }
    cases.append(case)
    observations.append({
        'arm': arm, 'same_image_sha256': copy['sha256'],
        'directly_viewed': [copy['delivery_path'], str(directory / config['thumbnail'])],
        'reviewed_scales': ['native', 'thumbnail'],
        'new_topic_observations_ko': config['topic_observations_ko'],
        'body_observations_ko': config['body_observations_ko'],
        'supplemental_failures_ko': config['supplemental_failures_ko'],
        'whole_image_impression_ko': config['impression_ko'],
        'reference_scope_ko': '보이는 얼굴 형태와 짧고 어두운 bob·가느다란 앞머리만 대조했다. 실존 정체성, 치수, 성격, 나이, 생애는 판정하지 않는다.',
        'coordinator_agrees_with_recorded_new_topic_all_of': True,
        'coordinator_agrees_with_recorded_effective_hard_set': True,
        'additional_authorial_full_set': 'not_full_pass',
        'profile_activation_claim': config['profile_claim'],
        'new_topic_and_hard_result': case['selected_topic_and_effective_hard_set_joint_result'],
        'user_acceptance': 'not_yet_received',
    })

assert len(cases) == 3 and len({case['arm'] for case in cases}) == 3
write('INDEPENDENT-ARM-BINDINGS.json', bindings)
write('COORDINATOR-PIXEL-REVIEW.json', {
    'schema_version': 'spring-coordinator-pixel-review/v1',
    'reviewer': 'root coordinator direct visual inspection',
    'observed_at': datetime.now(timezone.utc).isoformat(), 'cases': observations,
    'claim_limit': 'Observations concern these unchanged native files only. Auditors bind records, not pixels. Three authorial concepts are examples, not a controlled comparison or statistical effectiveness test. User acceptance remains pending.',
})
write('FINAL-NATIVE-TESTS.json', {
    'schema_version': 'spring-final-native-tests/v1', 'status': 'completed_with_observed_failures',
    'actual_image_call_count_total': 3, 'case_count': 3, 'cases': cases,
    'shared_test_generation': GENERATION, 'shared_test_source_fingerprint': SOURCE,
    'coordinator_review_path': str(OUT / 'COORDINATOR-PIXEL-REVIEW.json'),
    'user_acceptance': 'not_yet_received',
    'qualification_limit': 'A: hard pass but new-topic all-of fail. B: selected-topic and hard pass, additional lace observation fail. C: new-topic pass but hard fail. No whole authorial observation set is claimed to fully pass.',
})
integration = read(OUT / 'runtime-integration.json')
integration['native_image_status'] = 'completed_with_observed_failures'
integration['native_image_evidence'] = str(OUT / 'FINAL-NATIVE-TESTS.json')
integration['coordinator_pixel_review'] = str(OUT / 'COORDINATOR-PIXEL-REVIEW.json')
integration['primary_runtime_final_freshness'] = read(OUT / 'FINAL-RUNTIME-FRESHNESS.json')
write('runtime-integration.json', integration)
print(json.dumps({'status': 'PASS', 'actual_native_calls': 3,
                  'cases': [{'arm': case['arm'], 'new_topic': case['new_topic_all_of'], 'hard': case['effective_hard_gates']} for case in cases]}, ensure_ascii=False, indent=2))
