arm-2 — **흙 안료 작업실에서 부서진 흙 미장 부조를 복원하는 순간**

실제 native 이미지 생성 **1회**로 테스트를 완료했습니다. 프롬프트·runtime·공식 픽셀 리뷰 감사는 PASS이며, 신체·도구 관계의 hard gate 5개도 모두 PASS입니다. 독립적으로 동결한 자체 기대값은 **7 pass / 1 fail**입니다. 장면과 집중은 명확하지만 “안도로 전환”은 구별하기 어려워 fail을 보존했습니다. 미학적 사용자 수락은 `not_yet_received`입니다.

컨셉 seed `3830837209`의 단일 draw index 3으로 네 가능성 중 하나를 선택했습니다. 연구·후보 접근 전에 실제 원문·active spans·creative controls·TESTCASE·core를 동결했습니다. 저장값은 sensual 1, fetish 0, creativity 1, surreal 0입니다. 참조는 직접 보이는 얼굴과 헤어 외형에만 사용했고 실제 정체성·성격·생애는 추정하지 않았습니다.

신규 **soil_e021**을 선택해 붉은 갈색 보수 흙 패치, 그 패치에 속한 같은 색 입자, 밝은 기존 흙 부조와의 국소 경계를 최종 문장에 추가했습니다. 세 성분은 실제 이미지에서도 관찰됩니다. 신규 **soil_e099**의 발굴 단면·격자·매장 유물 관계는 실내 부조 복원 목적과 달라 기각했습니다. 새 흙 시각 프로필은 **노출 0 / 선택 0**입니다.

흙의 분말·덩이·젖은 상태와 복원 동작은 독립 baseline에 이미 있었습니다. 이번 기여는 색·입자·경계의 소유 관계를 명시한 부분입니다. baseline-only 대조 이미지를 생성하지 않았으므로 이미지 수준의 인과적 개선 효과는 입증하지 않았습니다.

| 자체 기대값 | 결과 |
|---|---|
| 건조 덩이·분말·젖은 흙 상태 | pass |
| 원흙 → 분쇄·체질 → 채움 연결 | pass |
| 손상 → 나이프 접촉 → 보수 결과 | pass |
| 앞치마 직물의 흙 손자국 | pass |
| 작업 손 피부에 붙은 흙 | pass |
| 참조 얼굴·짧은 검은 보브 외형 | pass |
| 양팔·지지 손·도구 접촉 | pass |
| 집중에서 안도로 바뀌는 정서 | fail |

실제 파일은 **1237×1272 PNG**입니다. 전체 프레임과 native 해상도에서 확인했고, native 원본과 arm 로컬 복사는 SHA-256 `d643b29c19db9a526bf6c8ae473e617cb6519dcbe3d5c1e4912bad2eab0fe534`로 동일합니다. 거의 정사각형인 결과는 agent가 선택한 landscape 구상과 다르지만 중요한 물질·지지·접촉 관계를 가리지 않습니다. 손의 흙 흔적은 엄지보다 검지 쪽에서 더 뚜렷합니다.

manifest v2는 기존 recorder의 검증 함수를 사용해 실제 managed ledger 행의 모든 필드와 같은 입력으로 만들었습니다. ledger에는 실제 호출 **1개 행**만 있습니다. 로컬 준비 오류는 복구 기록에 남겼으며 이미지 도구 재호출과 공유 스크립트 변경 없이 반환 파일의 바이트와 실제 호출 기록을 보존했습니다.

주요 산출물: [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/final_prompt_en.txt), [결과 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/result_image.png), [기여 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/DATA-CONTRIBUTION.json), [픽셀 자체 테스트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/PIXEL-TEST-RESULTS.json), [공식 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/visual_render_review.json), [리뷰 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/review_audit.json), [ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/image_runs.ndjson), [독립 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/run_manifest.json), [source receipt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/SOURCE-RECEIPT.json), [종합 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/ARM-RESULT.json).

![흙 부조 복원 작업 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-2/result_image.png)
