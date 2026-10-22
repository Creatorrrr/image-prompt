# arm3 독립 이미지 검증 결과

컨셉: **도시 그림자 갱신 창구**. 독립 3안 중 무작위 선택 후 후보 접근 전에 core를 고정했다. 실제 이미지 호출은 **1회**, 수리 이미지 호출은 **0회**다.

- 원본 보존 복사: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/image-attempt-1.png` (1237×1272, SHA256 `e664e38ab54782eb28bea2dde5325a776a9428c023a980915bf5cd31502a5d0d`)
- 생성에 전달한 정확한 문장: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/final-prompt.txt`
- 실제 tool 원본: `/Users/chasoik/.codex/generated_images/01a16265-732a-7fe0-9efc-04ee527927ed/exec-4135847f-5604-4ac3-8dd4-f4d07c054d77.png`
- pack `c87477dd0ac705a3`, ledger run `ac9bff48feeaacf3`; ledger와 독립 manifest는 이 폴더에 있다.

## 실제 픽셀 판정

참조의 타원형 얼굴, 갈색 눈, 짧고 어두운 보브와 성긴 앞머리는 확인된다. 실제 신원이나 나이를 추론하지 않았다. 살아 있는 얼굴과 도자기 손/투명 광섬유 손목의 연결, 자율적인 검은 형상, 별을 담은 기계, 어두운 행정 창구가 보여 네 주제의 가시적 모티프는 존재한다.

정확한 장면은 **실패**다. 검은 손은 판 위에 놓인 손목이 아니라 반대쪽 들린 손목을 잡는다. 손바닥–투입구–그림자 연속 경로와 별–리본 발광 연결도 전부 확인되지 않는다. 원본을 native scale로 직접 보았다. 부분 가시성은 통과로 올리지 않았다. 보조 검사 3/8 통과, 5/8 실패. 공식 embodiment gate 3/5 통과, 2/5 실패이며 review-audit는 `record_valid=true`, `technical_qualification=fail`을 저장했다.

## 신규 데이터의 실제 기여

4개 독립 검색에서 32개 CID/RID occurrence(32개 distinct source)를 반환했다. 신규 I04 `cand_841fc814f0a7575481546628b0d8c568` / RID `base`가 `__request_topic__`에 자연 노출됐다. 이 자료는 두 생물 외피와 공유 막의 모든 연결을 요구하고 subject 전체효과 및 `not_qualified` 경계가 있어 채택하지 않았다. 나머지도 source별 사유와 네 개의 완성 대안을 비교해 기록했다.

**노출 1, 신규 자료 채택 0, 신규 retained effect 없음.** 최종 프롬프트는 frozen baseline과 byte-identical하다. 네 주제가 이미지에 보인다는 사실을 신규 후보의 생성 기여 증거로 해석하지 않는다.

## 수리 차단

관찰된 접촉/가시성 결함만 고치는 draft와 공식 retry projection은 준비했다. 동일 입력을 검증된 bound runtime으로 다시 freeze해도 `retry_input_invalid`가 발생했다. coordinator가 마지막으로 제공한 동일 request_id envelope는 원래 inventory binding과 일치하지만, 공개 neutral validator가 `request_lineage parent_request_id must differ from the current request`로 거절했다. 새 ID/기존 ID 양쪽 경로의 공개 결속 충돌을 보존하고 중단했다. 참조 삭제, inventory 완화, 감사 우회 또는 추가 이미지 호출은 하지 않았다.

- 공식 픽셀 검토: `visual-review-attempt-1.json`, `review-audit-1-result.json`
- 전체 장면/주제/참조 검토: `supplemental-pixel-review-attempt-1.json`
- source 판단/대안: `composition-comparison.md`, `decoded-source-review.json`, `source-use-summary.json`
- 수리 공개 결속 증거: `public-retry-binding-check.json` (retry-1 내부), `same-request-repair-public-check.json`, `retry-1-bound/freeze-error-observed.json`
- 독립성/실행 증거: `run-manifest.json`, `sealed-execution-proof.json`, `image-runs.ndjson`

사용자 수용 판단은 **pending / not_yet_received**다. 이 결과는 데이터 등록·검색·선택·프롬프트·픽셀·사용자 수용을 분리한다.
