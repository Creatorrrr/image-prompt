# 동결 카메라 근거 전달 후속 개선 — 2026-10-03

범위는 검색 노출과 텍스트 계약이다. 공급자 호출과 이미지 생성은 0회이며,
렌더링 품질 개선을 주장하지 않는다.

## 변경과 적용 범위

- 신규 작성자는 요청된 카메라 방향·높이를 각각 검토하고 기존 `camera`
  속성 anchor에 영어 기본문의 literal evidence를 기록한다. 새 CLI의 반복 가능한
  `--require-camera-evidence direction|height`는 작성자가 선언한 요청 축의 근거가
  빠지면 candidate DATA 로드 전에 실패한다. 기존 동결 코어를 그대로 재현하기
  위해 무조건 켜지는 검사는 아니다. 신규 SKILL 작성 경로가 해당 flag를 요구한다.
  이 검사는 선언을 확인하며 요청 의미를 자동으로 판정하지 않는다.
- 명시적 소유 근거가 없는 `camera_direction`/`camera_height`에 한해 동결된
  `baseline_prompt_en`의 단일 카메라 직접 동작 절을 literal 질의로 투영한다.
  카메라 소유가 명확한 coordination만 유지한다. 본문의 다른 주체, 배경 문장,
  부정문, 여러 카메라, 묘사된 카메라는 근거로 추가하지 않는다. 모든 영어 문법이나
  간접 소유 표현을 해석하는 파서는 아니다. 불명 표현은 기존 조회 경로를 유지한다.
- 입력 코어, 잠금, DATA, 품질 계층, 속성 효과 계약, candidate 총량 64,
  optional 채택과 공개 shuffled 순서는 그대로다. 새 query projection은 빠진
  속성 잠금을 만들지 않는다. 검색 노출과 채택 가능성은 별도다.

신규 모듈은 post-core `scripts/photo_camera_evidence.py`에 있다. pre-core 허용
자료 목록과 DATA/index/embedding 입력은 변경하지 않았다. 재임베딩은 필요 없다.

## 동일 DATA 전후 결과

수정 전 runtime은 `31dbed9f0d22af97025cebcbceffc07b4250de35`이다. 최종 비교
runtime은 `c2b171001e4b7973ecdebadac0f03b4bc697e50c`이며 docs-only main
`bcb671ba488a31f4e84e5e0d8b0a740e4dd9c706`까지 통합했다. main의 추가분은
검증 문서이고 비교 DATA/runtime 기준선 바이트는 같다.

양쪽 production `load_runtime_data`에 quality layers를 포함했다. DATA는
9,819 semantic entries와 1,564 profiles이며 지문은 양쪽 모두
`ba85a857febb6e23f84b6ffc7f668c7cde9203217f424bff62bbf019eaceadc3`이다.
24개 입력 JSON과 정규화된 코어 해시는 전후 동일하다. [metrics.json](metrics.json)에
원시 focal 질의, 교집합, 노출 ID, 적합성 및 모든 후보 ID 집합 차이를 기록했다.

| 측정 | 수정 전 | 수정 후 |
| --- | ---: | ---: |
| 원본 006 올바른 올려다보기 노출 | 0 | 2 |
| 속성 보정 006 올바른 노출 | 1 | 1 |
| 속성 보정 006의 반환 camera 후보 적합성 | 모두 ineligible | 모두 ineligible |
| 입력·코어 해시 유지 | 24/24 | 24/24 |
| 후보 총량 | 24건 모두 64 | 24건 모두 64 |
| 후보 미채택·원문 유지 작성 감사 | — | 24/24 pass |

원본 006은 기본문의 `Position the camera below shelf level and tilt it upward
toward the locomotive`를 camera query로 전달한다. 후보 ID는
`extreme_low_angle_under_subject`, `extreme_low_hero_angle`이다. 더 강한
극단적 표현이므로 노출만으로 최선의 표현이나 안전한 의미 채택을 주장하지 않는다.
원본의 기존 잠금 메타데이터에는 카메라 부분 잠금이 없어 기계적 표기는 eligible다.
이것이 요청의 올려다보기 의미를 바꿀 허가는 아니다.

속성 보정 arm은 기존 camera owner 근거를 우선 사용한다. camera 방향 행 49개
모두 효과 범위가 누락돼 관련 부분 잠금에서는 계속 ineligible다. 명시적 효과
범위만 추가해도 잠긴 동일 속성과 겹치는 효과는 현재 계약에서 허용되지 않는다.
원본 기본문에는 이미 요청된 시점과 천장 가시성이 있으며 모든 optional 후보를
거절해 유지할 수 있다. 원래 누락은 후보 노출 지표였다.

## 대조군, 실패 보존과 한계

패치 전에 같은 실행자가 새 EN/KO 요청과 영어 기본문 14건을 동결했다. 별도
평가자의 blind set으로 부르지 않는다. SHA-256은
`49949e329be314f81c2f49205266a85967a4a01f4670076fd5c8b7f81c1b6f0a`이며
양성 6건의 literal 절 전달은 0/6→6/6, 음성 8건의 projection abstention은
8/8 유지다. 낮지만 수평인 카메라와 물체만 위를 향하는 장면을 구분한다.

부모가 제공한 첫 독립 V1은 작성자가 repository/code/candidate/fix를 보지 않은
14건이다. 수정 전 평가에서 양성 0/6, 음성 abstention 8/8이었다. 이후
구현을 수정했으므로 개발 대조군으로 보존한다. 후속 결과는 양성 1/6,
음성 8/8이다. 모든 기대 span과 실패는 그대로다. 영어 baseline 계약에 해당하지
않는 raw KO prose도 추출 결과를 기록했으며, 실제 생성 계약과 동일하다고 부르지
않는다. 간접 capture-camera 표현과 지원 밖 문법은 남은 제한이다.

`evaluate_owned_clauses.py`는 raw 추출, 전달한 질의, synthetic caller probe와
속성 적합성을 구분한다. caller probe의 candidate-free wire/budget scaffolding은
독립 작성자의 동결 scene core가 아니다. 최초 scaffolding 오류 보고와 수정된
보고를 모두 보존했다. Expected span을 입력 anchor/lock으로 사용하지 않았다.
새 fallback이 abstain해도 기존 generic slot projection이 optional camera 후보를
노출할 수 있다. Abstention을 slot 전체의 생략이나 채택 적합성으로 보고하지 않는다.

24개 팩 중 후보 ID 집합이 바뀐 것은 원본 006뿐이다. 카메라 방향 두 대안이
올려다보기 두 후보로 교체됐고, 높이 후보는 한 개가 빠지고 두 개가 들어왔다.
같은 64 안에서 optional motion 후보 하나가 빠졌다. 카메라 높이 후보의 의미
정확도나 전체 후보 precision 향상은 검증하지 않았다.

초기 42-method 검사에서 원본 006이 여전히 실패한 로그와 잘못된 public V6
`selected` 필드를 읽은 테스트 오류를 보존했다. 배경 문장을 카메라 객체 설명과
구분하도록 수정했고 신규 검사 18개가 통과했다.
[실패 기록](../../../failed-reports/upward-camera-owner-fallback-20261003.md)을 참조한다.

## 검증과 재현

전체 탐색은 1,339 tests/153 modules를 실행했다. 검사 중 소유 절 경계를
보강해 source snapshot이 달라진 113개 모듈을 최종 소스로 재실행했다. 현재
발견되는 1,341 tests/153 modules의 모든 ID를 정확히 한 번씩 집계했다.
1,336개 메서드는 성공했고 5개 메서드가 기존 자산 누락으로 실패하거나 오류를
냈다. 신규 실패·오류 ID는 0이다. 선택된 모든 모듈의 runtime/DATA 파일 지문이
최종 소스와 일치한다. `test-summary.json`은 탐색 결과와 최종 검사를 구분한다.
기존 한국 감성 JPEG, 메이크업 입력/관찰 JSON, 빈곤 PNG, rare-photo JSON
누락은 원본 main에서도 같은 10개 subtest 실패·1개 오류로 재현된다.
과거 V1–V6 및 현재 V7 경계·픽셀 결과·의미 기대값은 수정하지 않았다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/evaluate.py \
  --runtime-repo /path/to/before-or-after --data-repo /path/to/pinned-main \
  --frozen-inputs /path/to/frozen --output /tmp/upward-replay

.venv/bin/python docs/research-evidence/photo-prompt/upward-camera-owner-20261003/evaluate_owned_clauses.py \
  --runtime-repo /path/to/before-or-after --data-repo /path/to/pinned-main \
  --test-repo /path/to/implementation --fixture /path/to/frozen-owner-cases.json \
  --output /tmp/owner-evaluation.json
```

역사적 원인은 [생산 추적](../renewed-framing-optical-coverage-20261003/upward-view-production-trace.md),
이전 merged 구현은 [전후 보고](../retrieval-runtime-improvement-20261003/README.md)에 있다.
공개 배열은 shuffled presentation이며 원시 검색 순위로 사용하지 않는다.

진단 원본과 동결 입력은 [diagnostic-evidence.tar.gz](diagnostic-evidence.tar.gz)에
보존했다. [manifest.json](manifest.json)은 압축 내 각 파일의 SHA-256을 기록하고,
[SHA256SUMS](SHA256SUMS)는 공개 증거 파일을 검증한다. 최초 실패 로그, 변경 전/후
24개 pack과 trace, 독립 V1 미해결 결과, caller scaffolding 오류와 수정 보고,
전체·최종 재검사 로그 및 기본문 미채택 감사가 포함된다.

작성자가 선언한 요구 축 검사도 production CLI로 확인했다. 속성 보정 006은
`--require-camera-evidence direction --require-camera-evidence height`로 통과했고,
카메라 속성 anchor가 빠진 원본 006은 같은 flag에서 DATA 로드 전에 exit 1로
거절됐다. Legacy 원본의 flag 없는 재현은 그대로 가능하다.

## 최종 독립 blind V2 — 미해결 재현율을 그대로 보존

별도 작성자는 repository, 구현, 이전 holdout에 노출되지 않았다. EN/KO 요청
각 7건과 각각 59–66단어 영어 baseline을 수신 전에 runtime
`6665684fd5c3a73591b4c5b4508c4cc5f5d3da1f`로 동결했다. 평가 후 runtime을
조정하지 않았다. 요청·영어 기본문·기대 owner 및 방향/높이 predicate span은
전달된 그대로 보존했고 SHA-256은
`8ad46e1ac0448dddc3503299b4b5b24e786a04902c41143f455d9c960a5a9a07`이다.

| V2 측정 | 수정 전 | 동결 수정 후 |
| --- | ---: | ---: |
| 양성 소유 절 추출 | 0/6 | 0/6 |
| 음성 literal projection abstention | 8/8 | 8/8 |
| production caller 코어 수락 | 13/14 | 13/14 |
| 새로운 소유 절 전달 | 0 | 0 |
| camera 질의·후보 노출 변화 | — | 0건 |

`taking this photograph`, `making the image`, `used to take the picture` 등의
camera 수식과 lens로 이어지는 간접 소유 절은 현재 제한 문법에서 추출하지
못한다. KO_LOW의 국소 upward 부정도 현재 전체 문장 부정 guard에서는 positive
수평 방향과 함께 abstain한다. 따라서 일반화된 capture-camera 재현율 개선은
입증되지 않았다. V2 기대값을 구현에 맞춰 바꾸거나 새 사례로 문법을 튜닝하지 않았다.

KO_TWO는 `No single capture direction can be selected from this scene`가 기존
blanket-negative 코어 계약에 걸려 양쪽 모두 거절됐다. 문장을 다시 써 통과시키지
않았고 해당 사례의 retrieved IDs는 null이다. Raw extractor abstention 8/8을
production 코어 수락 14/14로 표현하지 않는다. 나머지 13개의 synthetic caller
질의와 반환 camera IDs는 전후 같으며, 기존 generic projection은 잘못된 방향의
optional 후보도 노출한다. 추출 abstention은 slot 노출 없음이나 적합한 의미
채택을 뜻하지 않는다. 모든 양성의 camera 부분 잠금을 counterfactual로 선언하면
방향 행은 0/49 compatible이며 이 guards도 완화하지 않았다.

[변경 전](independent-v2-before.json), [동결 변경 후](independent-v2-after.json),
[분리 집계](independent-v2-summary.json)에 코어 오류와 모든 기대 span을 기록했다.
독립 V2가 제공한 것은 영어 prose와 span이지 완전한 frozen scene core가 아니다.
주체 label, candidate-free anchor/wire scaffold는 executor가 caller 검사용으로
만들었으며 독립 작성자의 핵심 장면 해석으로 주장하지 않는다. 첫 독립 V1의
최초 0/6과 seen 후 개발 결과 1/6은 그대로이며 V2와 구분한다.
