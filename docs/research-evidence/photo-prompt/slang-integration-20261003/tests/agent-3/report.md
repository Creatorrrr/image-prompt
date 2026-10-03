# Agent 3 independent native test

최종 엄격 판정은 **FAIL**입니다. 두 원본 모두 양눈의 작은 붉은 하트와 같은 피부의 네 요소 문양은 보이지만, 배꼽→중앙 문양 거리/전체 문양 폭 비율이 선택한 4/6 관계에 못 미칩니다. 첫 결과 약 0.25, 위치만 명확히 한 재시도 약 0.39이며 목표는 약 0.67입니다. 실제 렌즈 인쇄 매체는 렌즈 경계가 분해되지 않아 declaration-supported / physically UNOBSERVABLE입니다. 정지 생성 영상은 제조 방식이나 후처리 여부를 증명하지 않습니다.

난수 seed는 6406798815013629455입니다. 독립 선택은 유리 지붕 식물 작업실, 흐린 skylight와 brass 반사, 4개 matching paper shapes와 blue paint bottle, pigment settling inspection moment입니다. 가상의 27세 성인 아트 퍼포머라는 설정, 비성적 아트 범위, 정확한 문양 기하학은 작성한 테스트 선택입니다. 참조는 보이는 얼굴·헤어에만 사용했습니다.

새 데이터의 sv_pupil_heart_motif / sv_lower_abdominal_skin_marking은 작성 파일에는 존재하지만 실제 V6 pack 8dca6d97f2a90323에 노출되지 않았습니다. 관련 optional profile/후보를 선택하지 않았고, 모든 구체적 문양은 baseline에서 왔습니다. 따라서 이 이미지 결과를 데이터 통합의 기여로 인정하지 않습니다. Root가 보고한 원인은 adult 태그가 sensual=0에서 adult-content 필터로 처리된 것입니다. 이 arm은 수정 전 source snapshot/receipt와 exposure FAIL을 보존했습니다.

두 프롬프트의 composition/runtime 감사는 PASS입니다. 일반 embodiment 5개 gate는 두 원본 모두 PASS로 기록되었고 schema/hash 감사도 통과했습니다. 이 감사는 미노출 target 프로필이나 국소 위치 관계의 성공을 대신하지 않습니다. 사용자의 미적 선호·수락은 pending입니다.

| 원본 관찰 | 첫 결과 | 재시도 |
| --- | --- | --- |
| 양쪽 동공 영역의 하트 위치·형태 | PASS | PASS |
| 실제 printed contact-lens 매체 | UNOBSERVABLE | UNOBSERVABLE |
| 같은 피부 / 배꼽 아래 / 허리밴드 위 | PASS | PASS |
| 중앙 닫힌 마름모 + 안쪽을 향한 대칭 C 곡선 둘 + 아래 수직 stem, 4개 분리 | PASS | PASS |
| 피부 문양의 하트 0개 | PASS | PASS |
| 한 원본에서 두 관찰 영역 가독성 | PASS | PASS |
| 4/6 상대 위치 비율 | FAIL | FAIL |

- 첫 프롬프트: [prompt.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/prompt.txt)
- 재시도 독립 실행 프롬프트: [final_prompt.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/final_prompt.txt)
- 첫 native PNG: [native-attempt-1.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/native-attempt-1.png)
- 재시도 native PNG: [native-attempt-2.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/native-attempt-2.png)
- 후보 기여: [candidate_review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/candidate_review.json)
- 정확한 픽셀 기록: [pixel_review.attempt-1.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/pixel_review.attempt-1.json), [pixel_review.attempt-2.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/pixel_review.attempt-2.json)
- 독립 ledger/manifest: [image_runs.ndjson](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/image_runs.ndjson), [run_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/run_manifest.json)

실제 built-in image_gen 호출은 총 2회이고 model identifier는 tool에서 노출되지 않았습니다. 두 원본 모두 1237×1272이며 native bytes를 그대로 workspace에 복사했습니다. 추가 생성, CLI/model fallback, 다른 arm 입력, 두 결과의 부분 통과 합산은 하지 않았습니다.
