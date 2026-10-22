# 독립 실험 3 — 끝나지 않는 방송 종료 멘트

이미지 생성 1회는 성공했습니다. 아날로그 호러의 인상은 보이지만, 사전 정의한 실제 인물의 닫힌 입과 CRT의 열린 입이라는 완전 조건은 충족하지 못해 **전체 주제 사례는 FAIL**입니다. 실제 입술도 약간 벌어져 있습니다.

## 산출물

- 프롬프트: [final_prompt.txt](final_prompt.txt) — 독립 동결 baseline을 그대로 유지했습니다.
- 이미지: [generated_image.png](generated_image.png), 1448 × 1086.
- 사전 gate: [theme_pixel_gates.json](theme_pixel_gates.json).
- 실제 픽셀 검토: [theme_pixel_review.json](theme_pixel_review.json).
- 자료 추적: [theme-integration-trace.json](theme-integration-trace.json).
- 37개 source 개별 검토: [material_reviews.json](material_reviews.json).
- 완성된 4개 대안과 비교: [composition-comparison.md](composition-comparison.md).

## 실제 픽셀 판정

| 사전 gate | 관찰 | 결과 |
|---|---|---|
| 아날로그 캐리어 | 실제 CRT와 화면에 국한된 줄무늬·색 번짐·수평 트래킹 깨짐 | PASS |
| 신호 속 모순 | 두 얼굴 및 크게 열린 CRT 입은 보이지만 실제 입도 약간 벌어짐 | **FAIL** |
| 공공방송 종료 환경 | 책상 마이크·원고·음향 벽·장비·ON AIR·GOOD NIGHT | PASS |
| 참조 외형 | 짧은 검은 보브·앞머리와 얼굴 외형 가이드의 시각적 유사성 | PASS |
| 장르 가독성 | 평범한 제작 부스와 훼손된 익숙한 방송 얼굴의 대비 | PASS |

모든 gate는 원본 해상도에서 관찰했습니다. 입과 손은 리샘플링하지 않은 crop도 확인했습니다. `partial_is_fail` 및 `UNOBSERVABLE_NOT_PASS`를 적용했고, 사후에 gate를 완화하지 않았습니다. 별도 native 신체 검토 5개 gate는 모두 visible/PASS이며 그 기록 감사도 PASS입니다. 이 신체 기술 판정은 전체 주제 사례의 실패를 덮지 않습니다.

## 실행과 참조 증거

`image_gen.imagegen`을 1회 사용했고 CLI fallback·재생성은 하지 않았습니다. `exact_native_payload.json`과 `precall_bound_audit_proof.json`에 호출 전 정확한 프롬프트·원본 참조 경로·파일 해시·감사 영수증을 보존했습니다. 원본 portrait는 `referenced_image_paths`로 실제 전달했습니다. `native_tool_result_metadata.json`은 도구가 반환한 구체적 파일 경로를 기록하고, `run_manifest.json`과 arm 전용 ledger는 1회 성공 및 이미지/참조 SHA를 연결합니다. 관찰된 이미지 모델 식별자는 제공되지 않았습니다.

- 이미지 SHA256: `58c42b6eb767e99cb5e084114843a6f78b17e05d0ee7cb1dec7dc4fc65cd307e`
- 참조 SHA256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`
- 동결 core SHA256: `f5577d19c41a6a97f3fa650844ae83d1a5f46abf7cc14576e402feb97429c7bd`

## 자료 영향과 한계

지정 H-F2 generation `d5aec2788e925fb6e8b27831b0055a2545067372edf87a6d5c7ea233a716ebfa`에서 positive pool을 축소하지 않고 3개 역할과 topic/baseline의 총 5개 질의를 실행했습니다. 40회 노출/37개 고유 source를 전부 검토했습니다. Coordinator가 실제 CID와 이번 등록 crosswalk를 대조한 결과 새 71개 시각 자료 및 재사용 A064의 노출은 **0개**입니다. 이는 검색 coverage 결과이며, 새 자료가 이번 이미지를 개선했다는 근거가 아닙니다. 모든 native chosen list는 비었고, 후보 정보로 바꾼 최종 구문은 없습니다. 화면 색·재킷·아카이브 표현·저조도 노이즈의 대안보다 두 얼굴을 직접 비교하는 독립 baseline을 택했습니다.

한 장의 이미지는 지속되는 음성·시간 순서·초자연 원인을 증명하지 않습니다. 참조 외형 유사성은 실제 신원 확인이 아니며 사용자 acceptance는 **pending**입니다.
