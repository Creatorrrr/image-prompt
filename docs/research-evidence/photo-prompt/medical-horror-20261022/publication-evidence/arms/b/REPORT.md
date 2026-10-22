# B 독립 테스트 결과

**결론: PARTIAL — 사전 장면 기준 6개 중 5개 통과. 모든 기준 동시 통과가 필요한 strict whole-case는 FAIL.**

독립 무작위 콘셉트는 “출구를 차지한 이동식 진단 스캐너”이다. Built-in `image_gen`을 정확히 1회 실행하고 반환 원본을 보존했다. 관리형 기록·신체 관계 감사는 PASS지만, 이는 아래 B03 방향 관계의 실패나 사용자 수용을 대체하지 않는다. 재생성·대체 공급자 호출은 없었다.

## 실제 산출물

- 이미지: [image.png](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/image.png) — 1237×1272, SHA-256 `5fe1469a7a4ff9ede9d3fb98bbeaa6319f1974a995c87719a2c9454b4500e0e6`
- 최종 프롬프트: [final-prompt.txt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/final-prompt.txt) — 322 words, SHA-256 `98d1254d263c52286ed82fd29705d881584def26e19e74cd338affd6f8bf8a91`
- 원본 보존·도구 반환 경로: [native-tool-result.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/native-tool-result.json); 원래 `$CODEX_HOME/generated_images` 파일을 남기고 동일 바이트를 복사했다.
- 원문 요청·동결 재현 증거: [request.txt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/request.txt), [replay-equivalence.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/replay-equivalence.json)

## 사전 기준의 원본 픽셀 판정

| Gate | 결과 | 원본에서 확인한 내용 |
|---|---|---|
| B01 얼굴·짧은 단발 참고 | PASS | 얼굴 비율과 짧은 검은 bob·분리된 앞머리가 읽힌다. 외형 참고이며 신원 인증이 아니다. |
| B02 장치 구조 | PASS | 원형 gantry·열린 aperture·금속 레일 환자 받침대의 같은 장치 관계가 보인다. |
| B03 출구·받침대 방향 | **FAIL** | 문과 복도 및 장치의 통로 점유는 보인다. 받침대는 인물 쪽보다 카메라 쪽, 인물 옆으로 뻗어 요구된 방향 전체를 충족하지 못했다. |
| B04 소유·접촉 | PASS | 손바닥 접점과 wrist→forearm→elbow→shoulder가 같은 인물로 이어진다. |
| B05 반응 관계 | PASS | 장치 쪽 시선·머리 방향, 좁혀진 눈썹과 멈춘 접촉이 함께 읽힌다. 실제 내면·병력은 추정하지 않는다. |
| B06 임상적 불안 | PASS | 임상 장치의 큰 규모, 어두운 빈 복도, 긴장된 작은 표정이 일상 진료 사진보다 불안한 정지를 만든다. 호러 강도는 절제되어 있다. |

사전 기준은 수정하지 않았고 SHA-256 `0f9e886b9463d992a8bd541905c5f1a0d2e9f8fd4231db6c1ee865940c608a3e`를 재확인했다. `UNOBSERVABLE_NOT_PASS`와 `partial_is_fail`을 유지했다. 원본 전체와 리샘플링 없는 얼굴·상체·손·스캐너 crop을 확인했다. [pixel-testcase-review.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/pixel-testcase-review.json), [review-crops.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/review-crops.json)에 판정·관측 근거가 있다.

## 새 데이터 노출과 화면 기여

3개 slot(`contact_point`, `prop_state`, `situation_context`)과 2개 whole-scene query로 5개 검색을 실행했다. 37개 서로 다른 원본과 40개 query/CID/RID 발생을 모두 검토했다. 새 medical-horror schema 후보 10개가 노출됐다. **10개 모두 skip, `inspiration_only` 0, qualified native 채택 0, 최종 literal 운반 0**이다. `native_approval=false`를 승인된 채택으로 바꾸지 않았다.

| 신규 ID | 실제 노출 CID | 사용 | 최종 literal |
|---|---|---|---|
| E07 신체 노출을 줄이는 진료 가림막 | `cand_c07d20f2829154b7b43b99e296a0f05c` | skip | 없음 |
| E05 불가능한 구조가 화면 안에만 존재 | `cand_66ad0c43fd9650308aba65e66c137e97` | skip | 없음 |
| D17 바늘과 떨어진 손의 거리 | `cand_8e27f525176b5fa993ec050da820173a` | skip | 없음 |
| L09 서로 다른 코드가 붙은 같은 외형의 시료 | `cand_6ec311e081c256239949646a57a6b768` | skip | 없음 |
| E13 해부 기록과 덮인 운반대의 역사 대리형 | `cand_3158f518cf02570b84f68b3c692b30e7` | skip | 없음 |
| D11 서로 다른 코드가 보이는 팔찌와 차트 | `cand_10355f068a37536987be9febe2d4fdb5` | skip | 없음 |
| L02 배양 플라스크·라벨·관찰 배율의 분리 | `cand_845f970f594f5fa793a0261bbcabe6e5` | skip | 없음 |
| D18 머리 표면의 전극과 별도 장치 | `cand_5b5451b3a37d5d27bbd6a5dd00deb154` | skip | 없음 |
| E01 침상 난간과 닿지 않는 호출기 | `cand_652d61d36a315952b7d0183774537377` | skip | 없음 |
| E04 검사 화면 앞에서 가려지는 얼굴 | `cand_b6217834063b569eb5a2b6beff32d428` | skip | 없음 |

전체 source 조건·효과, 선언되지 않은 adult/owner 요구, subject 효과, 다른 소품·문자·화면 관계와 장면 가시성 비용을 개별 검토했다. 같은 “의료”라는 표지만으로 단편을 가져오지 않았다. 6개 완전한 대안을 기본안과 같은 기준으로 비교한 뒤, 검색 전 카메라 메모에서 준비한 사선 시점 명확화만 최종안에 반영했다. **이번 B 결과는 데이터의 검색 노출을 증명하지만 신규 후보가 화면을 개선했다는 증거는 아니다.**

- 전원본: [material-view.all.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/material-view.all.json), [source-details.decoded-full.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/source-details.decoded-full.json)
- 발생별 결정: [h-f2-material-decisions.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/h-f2-material-decisions.json)
- 후보별 전체 판단: [source-decisions.full.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/source-decisions.full.json)
- 완전한 대안·최종 비교: [composition-comparison.md](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/composition-comparison.md)
- 신규 데이터 운반 기록: [new-data-contribution.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/new-data-contribution.json)

## 기술적 검증과 바인딩

- 관리형 `controls → freeze → slot seal → retrieve → compose-audit → prepare-render → authorize → native-plan → native-started → native-result → review-shape → review-audit`를 완료했다.
- Compose audit: PASS, failures 없음. 후보가 의미를 덮지 않고 authored evidence로 보존됐다는 uncovered-intent quality warning 4개를 보존했다.
- Managed pixel review: record valid, technical qualification PASS, 정확한 embodiment gate 5개 PASS. 별도 B03 장면 실패는 그대로 유지했다. [visual-review.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/visual-review.json), [managed-review-audit.command.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/managed-review-audit.command.json)
- 실제 H-F2 binding: `3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5`, store `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`. [actual-h-f2-binding.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/actual-h-f2-binding.json)
- Validation receipt의 별도 native validation generation은 `c92dfffe22c45949e950a62e6ad923ccca8816a40f404ef27ad16e8dabe53088`이다. H-F2 데이터 세대와 혼동하지 않았다.
- Core: `7c6e4cdc47fa414d666a9645d050100025333e517a300edd8f929eb9b8fe859f`
- Intent lock: `00e9f90c75030f363b1546f494116bfc25059685e643f4a2f47c1ec72ab1b1d1`
- Controls: `73984ac640e0dbc75da973b1d06745dd96cbd95df77172d41802a0bef336ec37` — sensual 1 / fetish 0 / surreal 0 / creativity 1 / auto→sensual_led.
- 동결 시 스킬: `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`
- Reference: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`; 얼굴 비율·짧은 단발 외형 참고만 사용.
- Ledger: [image-runs.ndjson](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/image-runs.ndjson) 한 줄, run ID `87b0933c4165b93a`, tool `image_gen`, image call count 1. 실제 관측 모델명은 반환되지 않아 null이다. [run_manifest.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/run_manifest.json)

## 장면 해석과 한계

A short-haired woman in a pale blue clinical tunic stands beside a large illuminated circular apparatus. One palm presses lightly against its outer casing. A padded metal-sided table extends from the ring toward the foreground. Through the opening, a long empty corridor recedes into near-blackness. Her eyes turn toward the apparatus side, her brows pinch slightly, and her parted lips interrupt an otherwise still pose. The arrangement feels watchful and uneasy, with cold equipment occupying more of the image than the person. The table runs beside her rather than directly into her next step.

이는 같은 작성자가 키워드·강도 라벨 없이 먼저 서술한 장면 읽기이며, 프롬프트를 모르는 별도 검토자의 blind experiment로 주장하지 않는다. 짧은 단발과 얼굴·목선의 자연스러운 매력은 장치 관계를 보조한다. 바퀴와 발은 crop 밖이므로 이동식 기능이나 정확한 발 지지를 증명하지 않는다. 사진 밖에 다른 출구가 없다는 사실, 장치의 자율성·치료 피해·병력·동의·진단도 입증하지 않는다. 사용자 선호·수용은 pending이다. [artistic-pixel-observations.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/artistic-pixel-observations.json)

B는 shared source·스킬·runtime pointer·다른 arm을 수정하지 않았고 commit/push를 수행하지 않았다. 독립 기본안과 사전 판정 기준은 유지했다.
