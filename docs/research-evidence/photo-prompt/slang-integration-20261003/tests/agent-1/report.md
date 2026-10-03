1번 독립 테스트는 원본 한 장에서 공식 gate 10/10과 얼굴·양손 관찰 테스트 7/7을 통과했습니다. 원본 이미지의 부분 실패나 UNOBSERVABLE은 발견되지 않아 native 이미지 도구를 한 번만 호출했습니다. 사용자 선호 판정은 아직 받지 않았습니다.

난수 seed는 187680095935288485입니다. 선택한 콘셉트는 항구 창고 인형극 축제 리허설의 매표소 고장 직후, 성인 희극 공연자의 얼굴과 양손 V가 동시 표시되는 한 프레임.

![1번 native image](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/attempt-1/native.png)

[독립 standalone prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/prompt.txt) · [정확한 runtime prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/runtime_prompt.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/testcase.json) · [후보팩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/candidate_pack.json) · [실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/run_manifest.json)

| 관찰 항목 | 원본 판정 |
|---|---|
| 양쪽 위동공과 아래 공막 | PASS |
| 좁은 입술 틈보다 큰 개구 | PASS |
| 중앙 아래입술 경계를 넘는 혀 | PASS |
| 오른손 검지·중지 V | PASS |
| 왼손 검지·중지 V | PASS |
| 분리된 두 손목에서 같은 인물의 팔로 연결 | PASS |
| 얼굴·양손의 같은 인물 동시성 | PASS |

현재 통합 데이터에서 복합 얼굴 표정 대체 표현과 양손 V 전체 묶음이 실제 후보팩에 노출되어 채택되었습니다. 얼굴 후보의 전체 opt-in 계약을 활성화했고, 큰 개구 변형을 보존하면서 같은 성인 얼굴에서 세 요소가 함께 존재한다는 최종 문구를 명시했습니다. 양손 V 묶음은 손가락 모양·팔 소유자·손바닥 방향을 함께 보존합니다.

동공·개구·혀·양손 V·팔 연결과 공연 콘셉트는 이미 데이터 조회 전에 고정한 baseline에 있었습니다. 새 데이터의 원자 ID들은 이 한 팩의 일반 슬롯 목록에 노출되지 않았습니다. 이 결과는 대체 표현의 노출·적합한 채택·해당 이미지의 픽셀 생존을 확인하며, 인과적인 개선 효과나 원은어의 전체 의미를 검증하지 않습니다.

공식 감사는 technical_qualified=true, failed_hard_gates=[], schema_failures=[]를 반환했습니다. requesting-user judgment가 pending이므로 감사 명령의 종료 코드는 1이고 representative_eligible=false입니다. 이 종료 코드를 이미지 실패로 바꾸지 않았습니다.

원본에서 카메라의 높은 각도와 전방 몸 기울기는 baseline보다 강하고, 종이 표는 주로 바닥과 매표기 주변의 잔여 흔적으로 보입니다. 이들은 추가 hard gate가 아닌 사진의 보조 관찰입니다.

원본은 1237×1272 PNG이며 SHA-256은 fc381f7d2e70e73f51dde70b2113400a18613276f3a71df07e4d99f718476e79입니다. 실제 native 이미지 모델 이름은 도구에서 반환되지 않았습니다. 참조 사진은 얼굴·머리카락의 보이는 외관만 안내하며 실제 정체성·나이·몸·선호·동의를 증명하지 않습니다.

[픽셀 증거와 공식 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/attempt-1/pixel_review_audit.json) · [보조 관찰 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/attempt-1/supplemental-fidelity.json) · [후보 기여 구분](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/selection-and-contribution.json)
