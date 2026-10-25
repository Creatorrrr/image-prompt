"""Consolidate completed independent native tests and exact local evidence."""
from pathlib import Path
import datetime, hashlib, json, shutil

O = Path(__file__).resolve().parent
R = O.parent
ROOT = O.parents[4]
S = ROOT / 'skills/photo-prompt-image-generator'

def read(path):
    return json.loads(path.read_bytes())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    protocol = read(O / 'three-arm-protocol.frozen.json')
    assert sha(S / 'SKILL.md') == protocol['latest_skill']['sha256']
    active = read(O / 'active-release-validation.json')
    assert read(S / 'retrieval-runtime.json') == active['config']
    qualification = read(O / 'retrieval-qualification.json')
    assert qualification['summary']['generation_id'] == active['config']['generation_id']
    assert read(O / 'source-preservation.final.json')['status'] == 'pass'
    assert not read(O / 'dictionary-validation.final.json')['errors']
    parent = read(O / 'parent-pixel-review.json')
    assert parent['status'] == 'complete'
    results = {a: read(O / f'arms/{a}/FINAL-RESULT.json') for a in 'abc'}
    c = results['c']
    d = R / 'image-test-evidence/c'
    planpath = Path(c['native_execution']['reference_attachment']['native_plan_path'])
    plan = read(planpath)
    payload = plan['payload']
    assert payload['referenced_image_paths'] == [protocol['reference']['path']]
    assert plan['references'][0]['sha256'] == protocol['reference']['sha256']
    prompt = payload['prompt']
    assert hashlib.sha256(prompt.encode()).hexdigest() == c['hashes']['final_prompt_sha256']
    assert read(Path(c['paths']['composed']))['prompt_en'] == prompt
    (d / 'prompt.txt').write_text(prompt)
    write(d / 'native-payload.json', payload)
    for source, name in [(O / 'arms/c/FINAL-RESULT.json', 'arm-result.json'),
            (Path(c['paths']['testcase']), 'testcase.json'),
            (Path(c['paths']['pixel_review']), 'pixel-review.json')]:
        shutil.copyfile(source, d / name)
    write(d / 'transport-verification.json', {
        'status': 'pass', 'native_plan_path': str(planpath),
        'native_plan_sha256': sha(planpath),
        'prompt_sha256': c['hashes']['final_prompt_sha256'],
        'composed_prompt_matches_native_payload': True,
        'reference_path': protocol['reference']['path'],
        'reference_sha256': protocol['reference']['sha256'],
        'reference_in_native_attachment_parameter': True,
        'user_acceptance': 'pending'})
    a, b = results['a'], results['b']
    calls = [a['execution']['actual_image_tool_call_count'],
        b['native_execution']['actual_image_call_count'],
        c['native_execution']['actual_calls']]
    assert calls == [1, 1, 1]
    assert a['pixel_review']['managed_record_valid']
    assert b['audits']['managed_review']['record_valid']
    assert c['audits']['managed_review_record_valid']
    assert not a['incomplete_required_steps'] and not c['incomplete_required_steps']
    tested_release = a['release']['h_f2_generation_id']
    assert b['release']['generation_id'] == tested_release
    assert c['hashes']['h_f2_generation_id'] == tested_release
    exposure = [(9, 9), (2, 4), (0, 0)]
    assert (a['source_exposure']['new_music_unique_sources'],
        a['source_exposure']['new_music_occurrences']) == exposure[0]
    assert (b['retrieval']['new_music_exposure_unique'],
        b['retrieval']['new_music_exposure_occurrences']) == exposure[1]
    assert (c['retrieval']['new_music_sampled_unique'],
        c['retrieval']['new_music_sampled_occurrences']) == exposure[2]
    cases = []
    names = ['오후 작은 무대의 밴드 트리오', '리사이틀실의 피아노 리허설',
        '새벽 홈 스튜디오의 신시사이저 녹음']
    for i, arm in enumerate('abc'):
        folder = R / 'image-test-evidence' / arm
        row = next(row for row in protocol['arms'] if row['arm'] == arm)
        assert sha(folder / 'testcase.json') == row['prospective_testcase']['sha256']
        receipt = Path(row['freeze_receipt']['path'])
        assert sha(receipt) == row['freeze_receipt']['sha256']
        shutil.copyfile(receipt, folder / 'freeze-receipt.json')
        core = receipt.parent / 'authorial_core_normalized.json'
        shutil.copyfile(core, folder / 'authorial-core.json')
        review = next(row for row in parent['arms'] if row['arm'] == arm)
        assert sha(folder / 'image.png') == review['image']['sha256']
        assert read(folder / 'transport-verification.json')['status'] == 'pass'
        cases.append({'arm': arm, 'concept_ko': names[i],
            'native_calls': calls[i], 'image_path': str((folder / 'image.png').resolve()),
            'image_sha256': sha(folder / 'image.png'),
            'prompt_path': str((folder / 'prompt.txt').resolve()),
            'prompt_sha256': sha(folder / 'prompt.txt'),
            'testcase_sha256': sha(folder / 'testcase.json'),
            'native_tool_reference_attachment_verified': True,
            'new_music_sampled_unique': exposure[i][0],
            'new_music_sampled_occurrences': exposure[i][1],
            'new_music_retained_inspiration': 0, 'new_music_native_adoption': 0,
            'theme_visibility': review['music_theme'],
            'strict_whole_scene': review['strict_whole_scene'],
            'passed_gates': review['passed_gates'], 'total_gates': review['total_gates'],
            'record_valid': True, 'technical_qualification': 'fail',
            'user_acceptance': 'pending'})
    data = read(O / 'data-integration.json')
    report = {'schema': 'music-band-integration-and-image-results/v1',
        'status': 'completed_with_documented_pixel_failures',
        'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_delta': {key: data[key] for key in [
            'positive_new', 'diagnostic_new', 'bindings_new', 'reused_complete_sources',
            'semantic_cards', 'keyword_rows']},
        'native_approval_for_new_sources': False,
        'working_source_preservation': read(O / 'source-preservation.final.json'),
        'active_installed_release': active['config'],
        'active_release_contains_byte_identical_music_sources': True,
        'image_test_release': tested_release,
        'image_test_native_release': a['release']['native_generation_id'],
        'latest_skill_sha256': protocol['latest_skill']['sha256'],
        'search': qualification['summary'], 'cases': cases,
        'summary': {**parent['summary'], 'actual_native_image_calls': 3,
            'reference_attachments_verified': 3, 'retry_calls': 0,
            'native_record_valid': 3, 'technical_qualification_passes': 0,
            'new_music_retained_inspiration_cases': 0,
            'new_music_native_adoption_cases': 0,
            'causal_improvement': 'not_established',
            'user_acceptance': 'pending'},
        'tests': {'focused_semantic_boundaries': '17 passed',
            'dictionary': read(O / 'dictionary-validation.final.json'),
            'active_runtime': read(O / 'active-runtime-check.json')},
        'commit_or_push_performed': False,
        'incomplete_required_steps': []}
    write(O / 'FINAL-RESULT.json', report)
    table = '\n'.join(
        f"| {v['arm'].upper()} | {v['concept_ko']} | {v['new_music_sampled_unique']} / "
        f"{v['new_music_sampled_occurrences']} | {v['passed_gates']}/{v['total_gates']} | 실패 |"
        for v in cases)
    document = f"""# 음악물 데이터 반영과 이미지 검증 결과

음악물·밴드물 시각 카드 124개를 데이터에 반영하고, 첨부 사진을 실제 참조로 전달해 독립 서브에이전트 세 곳에서 이미지를 각 한 장 생성했다. 음악 주제와 얼굴·머리 참고는 3/3 장면에 보였다. 사전에 확정한 모든 관계를 함께 보여야 하는 엄격 전체 장면 기준은 0/3 통과했다.

## 반영한 데이터

| 항목 | 반영 |
| --- | --- |
| 한영 시각 의미 카드 | 124개 |
| 새로운 완전한 선택형 시각 후보 | 122개 |
| 기존 완전한 원문 재사용 | 2개 |
| 문맥 구분과 연구 보류 진단 | 20개 + 12개 |
| 선택형 바인딩 | 370개 |
| 원문 키워드 추적 | 392행 |

악기·연주 손동작, 녹음과 공연 노동, 복식·머리, 관객, 합주와 이야기 소재를 포함했다. 손과 악기의 소유자, 지지, 접점, 케이블의 양 끝과 방향을 같은 명제 안에 보존했다. 팜 뮤트와 운지 손 뮤트, 슬랩과 팝, 크로스핸드와 오픈핸드, 어쿠스틱 크로스스틱과 전자 패드, MIDI 데이터와 오디오 파형을 서로 바꾸지 않는다. Punk/Funk, comping의 두 용법, conductor·wedge·turntable 등의 문맥 구분도 보존했다.

기존 IEM과 관객 마이크 원문은 오른쪽 귀·뒤 허리 수신기 및 전면 배리어 등의 전체 조건을 유지해 재사용했다. 나머지 122개를 새로운 선택형 원문으로 등록했다. 32개 진단은 긍정 검색 풀에서 제외한다. 새 자료는 모두 native_approval false이며, 연구 정의나 이번 이미지가 원문 전체의 native 자격을 부여하지 않는다.

실제 파일은 [시각 의미 데이터](../../../../skills/photo-prompt-image-generator/assets/photo_music_band_semantics_20261025.json), [후보](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_music_band_20261025.json), [바인딩](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_music_band_bindings_20261025.json)이다. [카드와 후보 매핑](integration-evidence/card-candidate-map.json)이 모든 카드의 등록·재사용·문맥 경로를 잇는다. [리서치](RESEARCH.md)와 [1차 출처](SOURCES.md)의 정의·문맥 근거는 저작한 장면 전체의 기하학을 입증하지 않는다.

## 데이터와 검색 검증

의미 경계 검증 17개와 후보 사전 검증을 통과했다. 작업 전 23,012개 후보와 17,968개 바인딩의 원문·조건·effects·정책은 유지됐다. 최종 작업 사전 23,596개에는 이번 154개 외에 동시 작업 추가분 430개가 포함된다. 이 숫자 전체를 이번 음악 추가량으로 세지 않는다.

새 자료가 포함된 전체 긍정 풀에서 한영 자연어 개발 질의 88개, 카드 문장 smoke 질의 248개, 일반 장면 대조 6개를 실제 실행했다.

| 검색 확인 | 결과 |
| --- | --- |
| 명시된 목표가 있는 자연어 질의 | 68개 |
| 목표 중 하나가 상위 8개 안에 노출 | 64/68 |
| 목표 중 하나가 상위 32개 안에 노출 | 66/68 |
| 모든 지정 목표가 상위 32개 안에 노출 | 63/68 |
| 카드 문장 목표가 상위 8개 안에 노출 | 248/248 |
| 일반 장면에서 새 음악 후보가 상위 10개 안에 노출 | 0/6 |

개발자가 작성한 질의와 카드 파생 smoke이므로 독립 holdout 정확도로 해석하지 않는다. 다중 목표의 일부와 두 영어 질의의 목표 순위가 남았다. 검색 규칙이나 원문을 이 질의에 맞추어 수정하지 않았다. [현재 버전 검색 결과](integration-evidence/retrieval-qualification.json), [남은 순위 사례](integration-evidence/retrieval-gaps.json), [원문 보존 검증](integration-evidence/source-preservation.final.json)을 보존했다.

동시 설치 변경을 발견해 기존 기본 버전을 덮어쓰지 않았다. 음악만 추가한 successor를 검증했고, 이후 실제 기본 버전에 동일한 음악 후보·바인딩이 포함된 것을 파일 해시와 전체 seal로 확인했다. 해당 기본 버전에서도 342질의를 재실행하고 로컬 runtime을 확인했다. [설치 검증](integration-evidence/active-release-validation.json)에 동시 수정된 다른 주제 원문 10건도 분리해 기록했다.

현재 기본 H-F2는 {active['config']['generation_id']}이다. 이미지 세 팔은 공통으로 {tested_release}에 고정했다. 두 버전의 음악 후보와 바인딩은 byte 단위로 같고, source kernel 코드는 같지만 전체 검색 모집단은 다르다. 이미지 결과를 다른 모집단의 재생성 결과로 표시하지 않는다.

## 독립 이미지 테스트

세 팔은 최신 SKILL과 허용된 중립 입력, 원 요청, 참고 사진만으로 무작위 콘셉트·초안·판정 기준을 먼저 동결했다. 서로의 콘셉트·프롬프트·결과를 공유하지 않았다. 한 팔당 실제 image_gen.imagegen 한 번, 총 3회이며 재시도와 추가 생성은 0회다. 첨부 사진은 텍스트 경로만 적은 것이 아니라 referenced_image_paths로 실제 전달됐고 부모 검토에서도 payload·참조 SHA·최종 프롬프트 일치를 확인했다. 사용 범위는 보이는 얼굴과 단발머리 참고다.

| 팔 | 무작위 콘셉트 | 새 음악 후보 노출 고유/등장 | 가시 판정점 통과 | 엄격 전체 |
| --- | --- | --- | --- | --- |
{table}

각각 [A 프롬프트](image-test-evidence/a/prompt.txt)·[A 테스트케이스](image-test-evidence/a/testcase.json)·[A 픽셀 리뷰](image-test-evidence/a/pixel-review.json), [B 프롬프트](image-test-evidence/b/prompt.txt)·[B 테스트케이스](image-test-evidence/b/testcase.json)·[B 픽셀 리뷰](image-test-evidence/b/pixel-review.json), [C 프롬프트](image-test-evidence/c/prompt.txt)·[C 테스트케이스](image-test-evidence/c/testcase.json)·[C 픽셀 리뷰](image-test-evidence/c/pixel-review.json)를 보존했다.

A는 기타 양손 접촉, 삼인 합주와 상호 시선이 보였다. 기타에서 앰프까지 같은 케이블의 전 경로, 드러머의 의자 지지, 스틱과 스네어 헤드 접촉을 모두 확인하기 어려웠다.

B는 한 사람·양손·건반과 벤치 지지가 명확했다. 오른발이 먼쪽 페달과 일부 조립체를 가려, 정확한 오른쪽 페달 접점과 전체 구조가 함께 보이는 조건은 부분 관찰이었다. 가림만으로 해부학적 오류를 진단하지 않았다.

C는 얼굴, 건반·노브 조작과 DAW 파형 화면이 보였다. 실제 배우 기준 오른손이 건반, 왼손이 노브를 조작해 동결한 좌우 역할이 반전됐고, USB 경로와 끝점이 오른쪽 프레임 밖으로 나갔다.

부모도 세 원본을 직접 보고 같은 전체 실패 결론을 기록했다. 총 21개 중 13개 가시 판정점이 통과했지만, 각 장면의 모든 기준이 함께 충족돼야 하므로 이 합계를 전체 성공률로 바꾸지 않는다. [부모 픽셀 리뷰](integration-evidence/parent-pixel-review.json)와 각 팔의 독립 결과·ledger·manifest를 보존했다. 프롬프트·렌더 감사와 픽셀 리뷰 기록 감사는 통과했고, 세 장의 기술적 전체 판정은 실패다. compose의 authored-evidence 경고 A6/B4/C5는 최종 원문 증거로 요청 의미를 유지한 비차단 경고로 남겼다.

새 음악 자료의 최종 retained inspiration과 native 채택은 세 팔 모두 0이다. A와 B는 후보를 검토한 후 독립 초안을 유지했고, C에는 새 음악 자료가 표본으로 전달되지 않았으며 기존 일반 혼합광 자료만 참고했다. 주제 가시성 3/3은 관찰 결과이고, 새 데이터 때문에 좋아졌다는 인과적 증거는 없다. 사용자 수용은 pending이다.

### A 밴드 트리오

![밴드 트리오]({cases[0]['image_path']})

### B 피아노 리허설

![피아노 리허설]({cases[1]['image_path']})

### C 홈 스튜디오

![홈 스튜디오]({cases[2]['image_path']})

## 다음 검증에서 유지할 기준

가려진 끝점을 성공으로 처리하거나, 좌우 역할이 바뀐 결과에 맞춰 명제를 바꾸지 않는다. 다음 장면 설계에서는 기타 케이블의 단일 경로와 드러머 지지, 피아노의 세 페달 조립체, 배우 기준 좌우 손과 USB 양 끝을 담을 시점을 우선 검토한다. 이 자료는 새 native 승인이 필요한 완전한 원문과 그림의 관찰 항목을 연결하는 후속 근거로 사용할 수 있다. 채택을 강제하거나 세 이미지의 실패를 숨기기 위한 추가 생성은 하지 않았다.

[전체 기계 판독 결과](integration-evidence/FINAL-RESULT.json), [동결한 3팔 프로토콜](integration-evidence/three-arm-protocol.frozen.json), [원본 이미지 해시](integration-evidence/parent-pixel-review.json), [현재 반영 안내](../../../../skills/photo-prompt-image-generator/references/music-band-semantics.md)를 함께 제공한다. 이미지는 native 반환 원본과 byte 단위로 동일하며 보정·재인코딩하지 않았다. commit/push는 실행하지 않았다.
"""
    (R / 'INTEGRATION-RESULTS.md').write_text(document)
    readme = (R / 'README.md').read_text()
    readme = readme.replace('현재 authored source', '리서치 baseline authored source')
    readme = readme.replace('검색·이미지 검증은 미실행.',
        '이후 실행 결과는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)에 기록했다.')
    readme = readme.split('## 현재 상태')[0] + """## 현재 상태

시각 카드 124개를 새 선택형 후보 122개와 기존 완전 원문 재사용 2개로 반영했다. 문맥·연구 보류 진단 32개, 선택형 바인딩 370개와 키워드 392행을 보존했다. 현재 기본 검색 버전에 동일한 음악 데이터가 포함된 것을 검증했다.

독립 서브에이전트 세 곳에서 첨부 사진을 실제 참조로 한 이미지 3장을 생성했다. 주제·얼굴과 머리 참고는 3/3에 보였지만, 사전 엄격 전체 장면 기준은 0/3 통과했다. 새 음악 후보 채택과 인과적 이미지 개선은 입증되지 않았다. 자세한 결과, 이미지, 프롬프트와 테스트케이스는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)에 있다.

validation.json과 기존 SHA256SUMS는 최초 연구 완료 당시의 기록이다. 적용 후 검증과 파일 해시는 integration-evidence에 별도로 보존한다. commit/push는 실행하지 않았다.
"""
    (R / 'README.md').write_text(readme)
    ref = S / 'references/music-band-semantics.md'
    text = ref.read_text()
    marker = '\n## Integration evidence\n'
    if marker in text:
        text = text.split(marker)[0]
    ref.write_text(text + marker + """
The applied evidence is recorded in the topic's INTEGRATION-RESULTS.md and
integration-evidence/FINAL-RESULT.json. Whole-pool development queries, literal
card smoke, independent material exposure and pixels retain separate results.
Three reference-guided native calls visibly realized music subjects. All three
failed their frozen strict whole-scene criteria due to incomplete relation
visibility; one also reversed the actor-relative hand assignments. New music
material was sampled in two arms, retained/native-adopted in none. These image
tests grant no new source native qualification or causal improvement claim.
""")
    print(json.dumps(report['summary'], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
