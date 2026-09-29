# 세 독립 이미지 검증 · 2026-09-28

이 문서는 새 시각 의미 데이터가 후보팩에 노출되는지와, 선택한 관찰 키워드가 실제 생성 이미지에 보이는지를 구분해 기록한다. 원본 참고 사진은 995×1022 JPEG이며 보이는 얼굴·헤어 외의 신원, 실제 나이, 체형 또는 동의 추정에 사용하지 않았다. 세 에이전트는 서로의 콘셉트나 결과를 읽지 않고 각자 seed와 코어를 먼저 고정했다. 원본 요청의 사용자 수용 판단은 아직 없다.

## 데이터 및 후보팩 노출

확장 자산은 원자 후보 251개와 관찰 관계·조합 묶음 116개를 포함한다. 최초 고정 코어로 작성한 세 후보팩은 새 `sff_` 항목을 하나도 노출하지 않았다. B 팔에서 적용 태그만 제거해 재검사해도 결과는 0개였다. 성인 패션 프리셋의 의상·하드웨어 필터와 품질 계층의 슬롯 캐리어를 데이터로 연결하고 동일 코어/seed로 다시 만든 팩에서는 각 에이전트의 `adult_appeal.axes.fetish_fashion.candidate_inventory`에 `sff_` 항목 10개가 노출됐다. 이 항목들은 기본 `slots` 카탈로그나 하드 시각 프로필로 자동 채택된 것이 아니다.

## 이미지 결과

| 독립 팔 | seed · 콘셉트 | 원본 생성 | 별도 개발용 대안 | 선택한 신규 원자 픽셀 판정 |
|---|---|---|---|---|
| A | 73117 · 역사적 아틀리에 | 출력 안전 차단, 동일 입력 재시도 연결 오류. 원본 `UNSCORED` | `arm_a/developmental_alternative.png` 저장 | `y01` PASS, `y06` PASS, `h05` FAIL. D링은 있으나 스트랩 통과·복귀 경로가 보이지 않음. 종합 FAIL. |
| B | 84293 · 야간 트램 세척 정비고 | 출력 안전 차단. 원본 `UNSCORED` | `arm_b/developmental_alternative.png` 저장 | `y01` PASS, `h09` PASS, `b11` PASS. 개발용 대안 한정. |
| C | 95479 · 햇빛 드는 절벽 케이블카 승강장 | `arm_c/arm_c_render_01.png` 저장 | 없음 | `y01` PASS, `y06` PASS, `h09` PASS. 원본 목표 3개 통과. |

선택 ID는 `sff_pro_` 접두사를 가진다. `y01`은 드레스 위의 별도 코르셋, `y06`은 가죽처럼 보이는 구조와 새틴처럼 보이는 드레스의 겹침, `h05`는 D링을 통과하는 스트랩 경로, `h09`는 두 스트랩 끝의 버클 결합, `b11`은 레이스 밑 부츠 텅과 아일릿 열이다. 소재의 실제 화학적 성분, 착용자의 실제 나이와 신원은 픽셀로 증명할 수 없다. 부분 충족은 통과로 계산하지 않는다.

A와 B의 개발용 이미지는 노출과 인상을 줄여 별도 프롬프트로 생성했다. 그 픽셀 통과는 차단된 원본 프롬프트의 성공을 뜻하지 않는다. C는 요청한 좌우 손의 지정에 불확실성이 있으나 문기둥 접촉과 승차 동작은 보인다. 세 이미지 모두 사용자 선호·수용 판정은 보류다.

## 재현 근거

- 각 팔의 고정 코어와 첫 팩, 수정 후 팩, 선택 후보, 감사, 이미지 호출, 런 기록, 픽셀 판정은 `outputs/sensual-fetish-qualification-20260928/arm_{a,b,c}/`에 보존했다. `outputs/`는 저장소에서 무시되는 로컬 증거 경로다.
- A: `qualification_result.json`, `candidate_pixel_review.json`, `run_manifest.json`, `image_runs.ndjson`. 첫 코어 이전에 상위 수준 메모를 열람했으므로 엄격한 blind precore 격리 주장에는 한계가 있다. 다른 팔의 입력은 사용하지 않았다.
- B: `qualification_summary.md`, `pixel_review.json`, `pixel_review_developmental.json`, 원본·개발용 개별 manifest 및 `image_runs.ndjson`.
- C: `candidate_pixel_review.json`, `run_manifest.json`, `image_runs.ndjson`, 원본 화면과 관찰용 crop. 소스 확장 SHA 기록 수정은 `source_ref_correction.json`에 남겼으며 이미지 호출은 한 번이었다.
- `validate_photo_prompt_dictionary.py`, `eval_semantic.py --check-index`, `git diff --check` 통과. 후보팩 범용 커버리지 검사 6건도 실패 0건이었다.
