# 초현실 포스트휴먼 주제의 세 독립 이미지 테스트 결과

서로 다른 컨셉을 독립적으로 확정한 세 서브에이전트가 최신 작업 공간의 사진 스킬과 새 검색 릴리스를 사용해 첨부 참조 이미지로 각각 한 장을 생성했다. 세 원본에서 참조 얼굴·헤어와 요청 주제의 모티프가 보였다. **정확한 장면 조건은 세 경우 모두 일부 실패했다.** 서브에이전트의 검사 뒤 root도 세 원본을 원본 해상도로 직접 열어 확인했다.

실제 내장 `image_gen` 호출은 총 3회, 보정 이미지 호출은 0회다. 세 원본은 각각 1237×1272이며 반환된 바이트를 그대로 보존했다. 요청한 모델·크기 메타데이터와 실제 반환 모델·해상도를 구분한다. 도구가 실제 모델명을 반환하지 않아 실제 모델은 미확인으로 남겼다. 사용자 수용은 아직 받지 않았다.

## 이미지와 판정

| 독립 컨셉 | 직접 확인한 구현 | 실패 또는 부분 증거 |
|---|---|---|
| 궤도 관측소의 관측자 | 창을 채우는 거대한 눈, 인물과 광학 장치, 가슴 조립부에서 수신기로 이어지는 관, 참조 외형 | 가슴 판이 피부 부품보다 의복 위 harness로 읽힘. 닫힌 피부 이음매 미확인. 큰 고리 장치의 바깥쪽 일부가 잘림 |
| 유기적인 씨앗집의 귀환 입주자 | 보철–손가락–벽 발광 뿌리망의 연속성, 손 옆 벽눈, 손목 기계·크리스털 장치, 참조 외형 | 상단 역전 정원 외에 아래 별도 opening이 생겨 단일 역전 문과 문턱 그림자 전체 조건은 실패 |
| 도시의 그림자 갱신 창구 | 참조 외형, 인공 손·광섬유 손목, 검은 인체형 형상, 행정 창구와 별 모양 광원 장치 | 검은 손이 판 위 손목 대신 반대 손목을 잡음. 손바닥→슬롯→그림자와 별→전달 띠의 끝점이 한 경로로 입증되지 않음 |

모티프가 가시적이라는 판정은 역사적 장르 소속, 실제 의식·생명·동일성 생존·마법 효력 또는 관객의 공포 반응을 증명하지 않는다. 부분/비가시 증거는 완전한 장면 조건의 PASS로 처리하지 않았다. 세부 검사 수는 각 컨셉에 맞게 달라 직접적인 점수 경쟁으로 사용하지 않는다.

### 궤도 관측소

![궤도 관측소의 관측자 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm1/image-original.png)

[실제 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm1/final-prompt.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm1/RESULT.md) · [픽셀 검사](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm1/pixel-test-attempt1.json)

공식 리뷰는 기록 유효 `true`, 기술 판정 `fail`이다. 추가한 일반적 닫힌 이음 경계 문장은 프롬프트에는 들어갔지만 원본 픽셀에서 피부와 맞닿은 인체 부품으로 구현되지 않았다. 이 실패를 새 데이터의 시각 구현 성공으로 세지 않는다.

### 씨앗집

![유기적인 씨앗집의 귀환 입주자 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm2/images/seed-house-initial.png)

[실제 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm2/prompt.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm2/result.md) · [픽셀 검사](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm2/pixel-test-report.json)

공식 신체·접촉 리뷰는 통과했다. 별도로 저술한 단일 역전 문 진단은 부분 실패다. 핵심 얼굴·보철·벽 접점이 명료하므로 배경 장식만을 바꾸기 위한 추가 호출은 하지 않았다.

### 그림자 갱신 창구

![도시 그림자 갱신 창구 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/image-attempt-1.png)

[실제 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/final-prompt.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/FINAL-REPORT.md) · [최종 증거](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-posthuman-20261022-arm3/final-result.json)

보조 장면 진단은 8개 중 3개, 공식 신체·접촉 gate는 5개 중 3개가 통과했다. 기록은 유효하나 기술 판정은 `fail`이다. 검은 형상이 등장했다는 인상만으로 의도한 손목 접촉과 전달 경로를 충족했다고 판정하지 않았다.

## 새 데이터가 실제로 기여한 범위

세 에이전트는 후보나 다른 에이전트의 컨셉을 보기 전에 각 core를 확정했다. 동일한 실제 사용자 원문, 원 대화의 정확한 사용자 주제 인용, 참조 바이트를 사용했다. 서로 다른 컨셉은 각자의 자유 선택이며, 3번만 세 저술안 사이의 `secrets.choice` 추첨을 기록했다. 세 선택을 모두 통계적 무작위 표본이라고 부르지 않는다.

최초 managed 검색은 13질의, 97회 후보 노출, 전체 82개 고유 source였다. 이번 신규 모듈 88 CID 집합을 직접 대조해 새 후보를 식별했다. `native_approval=false`라는 상태만으로 신규라고 분류하지 않았다.

| 컨셉 | 새 후보 자연 노출 | 최종 효과 |
|---|---|---|
| 궤도 관측소 | C03, G06, L03, J01 4개 | J01 전체 장면은 거절. 기존 가슴 패널의 일반적인 닫힌 이음 경계만 국소 영감으로 명시했으나 픽셀 구현 실패 |
| 씨앗집 | E01 1개 | 두 뿌리·기둥·바닥 틈의 모든 끝점을 넣는 완성 대안이 핵심 접점을 작게 만들어 비교 후 거절. 프롬프트 변화 0 |
| 그림자 창구 | I04 1개 | 두 생물 껍질과 공통 막의 전체 구조가 독립 인물/그림자 컨셉과 달라 거절. 프롬프트 변화 0 |

새 후보의 검색 노출, 국소 영감, 전체 원문 채택, 프롬프트 반영, 실제 픽셀 구현을 별도로 기록했다. 네 주제의 핵심 컨셉은 검색 전에 이미 저술돼 있었으므로 새 데이터에 그 아이디어의 공로를 돌리지 않는다. **이번 세 장으로 새 데이터의 이미지 품질 개선이나 72개 원문의 완전한 시각 재현을 입증하지는 못했다.** 이미지 A/B 비교도 하지 않았다.

## 추가 보정이 호출되지 않은 이유

1번의 신체 패널과 3번의 핵심 접촉을 한 차례씩 보정하려 했으나, 공개 재시도 경로가 child freeze 검증을 통과하지 못했다. 새 ID 경로는 projection이 `representable`로 통과한 뒤 `retry_input_invalid`를 반환했다. NumPy가 있는 스킬 전용 Python에서 같은 입력을 재현해도 같았다. 기존 ID와 원 envelope를 유지하는 경로는 `parent_request_id must differ from the current request` 규칙으로 거절됐다. 3번의 공개 입력 비교에서는 새 envelope에 맞춘 scope inventory 바인딩과 부모의 닫힌 assertion 보존 사이의 충돌도 관찰했다. 포괄적인 `retry_input_invalid`의 정확한 내부 원인은 확인하지 않았다.

[현재 사진 스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md:38)의 “An unrepresentable lineage-v2 scope stays blocked” 지침에 따라 참조·의미·검사를 완화하거나 수동 이미지 호출로 우회하지 않았다. 첫 실패 이미지와 감사 기록은 그대로 남겼다. 이 차단은 이미지 도구의 거절이나 보정 이미지의 재실패를 뜻하지 않는다. 보정 이미지 호출 자체가 0회다.

1번은 보정 초기에 coordinator source 첫 165줄을 열람한 phase 규칙 이탈을 스스로 보고했다. 이후 추가 source/private 열람 없이 공개 projection 경로를 사용했다. 초기 세 core의 독립 확정과 이 보정 절차의 이탈을 구별하며, 전체 보정 과정이 완전한 phase 준수였다고 주장하지 않는다. 공개 도움말에 없던 route/axis 지원값은 root가 공개 상수로 확인했고 장면 영감에는 사용하지 않았다.

다음 작업의 우선순위는 원 envelope의 변경을 closed inventory에 재바인딩하면서 참조 property anchors를 보존할 수 있도록 재시도 계약을 검토하는 것이다. 지원 route/axis를 공개 schema에 명시하고, 그 경로가 검증된 뒤 1번과 3번의 핵심 관계만 다시 생성하면 된다. 후보를 더 넣는 것으로 이 접촉·바인딩 문제를 해결할 수는 없다.

## 증거

[세 실행의 해시와 원본·ledger 연결](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/integration-evidence/three-arm-final-evidence.json) · [root 원본 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/integration-evidence/root-pixel-reviews.json) · [데이터·설치 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/INTEGRATION-RESULTS.md)
