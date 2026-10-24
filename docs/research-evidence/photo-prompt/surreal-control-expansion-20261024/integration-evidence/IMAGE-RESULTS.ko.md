# 독립 3컨셉 이미지 결과

**실제 호출 3회, 저장 원본 3장. 초현실 주제 가시성은 3/3이며, 사전 시나리오 전체 통과는 1/3이다.** 부분 구현을 pass로 올리지 않았다. 추가 재생성은 하지 않았다. 원본 픽셀은 coordinator도 직접 재검토했다. 이 재검토는 blind 평가가 아니며 사용자 수용은 미수신이다.

| Arm | 컨셉 | 사전 기준 | 전체 판정 |
|---|---|---:|---|
| a | 광물처럼 보이는 커튼의 천 주름 | 3/4 | FAIL |
| b2 | 실제 자세와 어긋난 연결된 그림자 | 6/6 | PASS |
| c | 열린 세탁기 안으로 이어지는 바다 | 4/5 | FAIL |

## a: 광물처럼 보이는 커튼의 천 주름

[원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-a/images/surreal-a-original.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-a/final_prompt_en.txt) · [사전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-a/independent_testcase.json) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-a/arm_result.json)

![광물처럼 보이는 커튼의 천 주름](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-a/images/surreal-a-original.png)

연속 회색 광맥, 두껍고 거친 광물 같은 단면, 큰 천 주름, 같은 커튼 가장자리에 닿은 손끝, 옆의 단단한 대리석 조각과 가위가 함께 보인다. reference의 짙은 단발·가는 앞머리와 얼굴의 보이는 외관을 따른다.

사전 기준은 커튼 모서리가 손가락을 감싸 도는 말림까지 요구했다. 손끝 접촉과 큰 주름은 보이지만 손가락 주위를 감싼 연속 말림은 충분히 읽히지 않아 partial→fail.

봉제 문틀 후보의 정상 재질 비교물 전략을 영감으로 참고해 작은 rigid marble offcut을 추가했다. 문틀·봉제 외피 전체는 구현하지 않았고, 돌 베개 C02의 소재 연속성은 baseline에 이미 있어 새 기여로 세지 않았다.


## b2: 실제 자세와 어긋난 연결된 그림자

[원본](/Users/chasoik/Projects/image-prompt/generated/images/surreal-autonomous-shadow-20261024-b2/original.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-b2/final-prompt.txt) · [사전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-b2/scenario_test_case.json) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-b2/arm-result.json)

![실제 자세와 어긋난 연결된 그림자](/Users/chasoik/Projects/image-prompt/generated/images/surreal-autonomous-shadow-20261024-b2/original.png)

인물의 양팔과 손은 아래에 있고 벽의 그림자 한 손만 머리 위로 올라간다. 두 신발에서 바닥을 따라 벽·바닥 경계와 벽 실루엣으로 이어지는 어두운 경로, 같은 보브형 머리와 상체 윤곽, 벽 질감 위 평면 그림자가 한 프레임에서 보인다. 얼굴과 단발의 보이는 reference 외관도 따른다.

R11 닫힌 우산/펼쳐진 그림자를 실제로 받았지만 완성 대안 비교 후 skip했다. 기존 광원/수광면 후보의 정상 처마 그림자 비교만 최종 영감이다. 이 이미지의 자세 불일치는 독립 baseline에 선행해 있었으므로 새 데이터 효과로 세지 않는다.


## c: 열린 세탁기 안으로 이어지는 바다

[원본](/Users/chasoik/Projects/image-prompt/generated/images/surreal-c-sea-in-washer-20261024/image.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-c/authoring-c/final-prompt.txt) · [사전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-c/authoring-c/test-case.json) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal-expansion-20261024-c/authoring-c/result-summary.md)

![열린 세탁기 안으로 이어지는 바다](/Users/chasoik/Projects/image-prompt/generated/images/surreal-c-sea-in-washer-20261024/image.png)

가까운 고무 가스켓과 파도, 먼 수평선이 같은 개구부 안에 보이고 밖으로 열린 유리문과 힌지는 별개다. 인물의 주의가 개구부를 향하고 얼굴·단발의 reference 외관이 보인다.

손은 에이전트가 사전 시나리오에 적은 열린 유리문의 외곽 테두리가 아니라 고정 세탁기 입구에 닿는다. 서기에서 낮게 앉기로 바뀐 자세와 오른쪽 문 외곽의 crop도 저술상 staging drift로 별도 기록한다.

새 C06/C10/R13은 실제 노출·전체 검토 뒤 최종 기여 0. 기존 후보의 가까운/먼 얼굴 윤곽을 위한 framing 문장만 영감으로 썼다.

## 데이터 활용과 검증의 한계

- 세 arm 모두 같은 새 H-F2 세대에서 새 후보를 받았다. [실제 새 source 노출](managed-new-source-exposure.json)은 A 2개/B2 1개/C 3개다.
- 최종 새 CID 영감의 실제 유지: A의 R13 1건, B2/C 0건. 원본 새 후보의 완성 장면을 native 채택하거나 전체 조건을 이미지로 검증한 것은 0건이다. NOT_TESTED를 성공이나 실패 분모로 바꾸지 않는다.
- 따라서 이 세 장은 명시한 surreal 주제의 여러 독립 구현과 실제 후보 검토/선택을 보여 준다. 신규 19개 전체의 이미지 성공률이나 데이터의 인과적 개선 효과를 입증하지 않는다.
- 실제 saved controls는 surreal=0이며 명시 surreal 주제를 보존했다. 0~3 단계별 강도 calibration, 일반 장면에서의 unrequested adoption 비교, 독립 holdout은 별도 미실시다.
- 손의 위치·모서리 말림은 에이전트가 정한 사전 시나리오다. 이를 원래 사용자가 지정한 세부 pose/접촉으로 바꾸어 기록하지 않는다.
- 보이는 재질·주름·실루엣·공간 경계를 판정한다. 실제 석재 연성, 그림자의 자율성, 실제 차원 관통이나 인물의 신원은 정지 이미지로 입증하지 않는다.

[coordinator 직접 관측 JSON](coordinator-pixel-review.json) · [전체 반영 보고서](INTEGRATION-REPORT.ko.md)
