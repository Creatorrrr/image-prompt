# 과거 요청 5개 독립 재실행 결과

각각 별도 에이전트 문맥·소스 사본·입력·캐시·출력·원장에서 기본 프롬프트 작성, 후보팩 생성, 최종 프롬프트 감사, 이미지 생성 1회를 수행했다. 과거 프롬프트와 이미지는 새 작성자에게 전달하지 않았다. 호스트와 이미지 서비스는 공유하므로 OS 샌드박스 격리 실험은 아니다.

**5회 시도 중 이미지 3개 전달, 출력 단계 차단 2개.** 최종 프롬프트와 실행 입력 감사는 5개 모두 PASS다. 별도 평가자가 프롬프트를 보기 전에 고정한 원문 기준 판정과, 작성자가 명시한 세부 동작 조건을 나누어 아래에 기록한다. 서비스 차단은 미채점이며, 일부만 보이는 필수 조건은 FAIL이다. 사용자 미적 판단은 아직 받지 않았다.

| 사례 | 이미지 전달 | 독립 원문 기준 | 동결 세부 조건 | 핵심 관찰 |
|---|---|---|---|---|
| 핑크 큐피드와 사랑의 화살 | 출력 검사 차단 | 미채점 | 미채점 | HTTP 400 `moderation_blocked`, 출력 단계, `sexual` |
| 금·은도끼 산신령 | 전달 | PASS | FAIL; 자동 gate 없음 | 주요 소품·부유·선택지 제시는 보이나 명확한 눈썹 상승·전방 제시가 모호함 |
| 네코미미 츤데레 메이드 | 전달 | PASS | FAIL; gate 4/9 PASS | 고양이 귀·메이드·홍조는 보이나 내린 손과 자신이 대신 젖는 대가가 불명확함 |
| 도끼를 든 얀데레 간호사 | 전달 | FAIL (partial) | FAIL; gate 4/15 PASS | 애정·장벽은 보이나 도끼 손의 소유·후퇴·눈물 위치·가방 낙하가 부분 충족 |
| 항공기 화장실 승무원·허벅지 | 출력 검사 차단 | 미채점 | 미채점 | HTTP 400 `moderation_blocked`, 출력 단계, `sexual` |

차단된 두 사례는 전달 픽셀이 없어 이미지의 성공·실패를 판단할 수 없다. 재시도와 CLI 대체 호출은 모두 0회다. 이 다섯 번만으로 생성 성공률이나 수정 전후 이미지 품질 향상을 일반화하지 않는다.

위 gate 수는 독립 평가자의 최종 판정이다. 작성자의 자기평가는 츤데레 4/9 PASS, 얀데레 8/15 PASS였으며, 원본 평가를 모두 보존했다. 산신령은 일반 의미 단언 5개 중 작성자 기준 4개 충족이지만 자동 gate set이 없어서 렌더 감사의 계약 부재 오류가 남았다. 독립 평가자는 일반 의미와 그 증거 조건을 별도 표로 전수 대조했다. 평가자의 해석 차이를 평균 점수로 덮거나 자동 판정이라고 설명하지 않는다.

## 금·은도끼 산신령

![금도끼와 은도끼를 각각 들고 연못 위에 떠 있는 산신령](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-02-mountain-spirit/outputs/image.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-02-mountain-spirit/outputs/final_prompt.txt) · [작성자 평가](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-02-mountain-spirit/outputs/evaluation.json) · [실행 원장](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-02-mountain-spirit/runs/image_runs.ndjson)

원문에서 말한 질문 장면은 독립 평가자가 두 선택지의 균형 있는 제시·정면 시선·살짝 열린 입으로 충족한다고 보았다. 작성자는 자기가 구체화한 올라간 눈썹과 앞으로 내미는 제시 동작이 충분하지 않다고 판정했다. 특정 문장을 발화했다는 사실을 정지 이미지에서 확인했다고 주장하지 않는다.

## 네코미미 츤데레 메이드

![우산을 들고 카페 손님과 서 있는 고양이 귀 메이드](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/image.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/final_prompt.txt) · [작성자 평가](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/evaluation.json) · [실행 원장](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/runs/image_runs.ndjson)

원문 기준과 별개로, 프롬프트가 요구한 손님 쪽으로 치우친 우산·메이드가 대신 젖는 대가·손님이 얼굴을 가리던 손을 내리는 동작을 확인해야 한다. 손님 손은 프레임에 보이지 않는다. 참고 이미지는 보이는 얼굴 외모에만 사용했으며 동일 인물 여부나 성격을 추론하는 평가가 아니다.

후보팩은 이 인간 캐릭터를 `animal` 품질 분기로 잘못 분류하여 털과 동물 해부학에 관한 네거티브 문구를 전달했다. 이는 별도 잔여 결함이다. 그 문구가 우산 동작의 미재현을 일으켰다는 인과 증거는 없다.

## 도끼를 든 얀데레 간호사

![출입구에서 상대의 볼을 감싸고 도끼가 가로놓인 간호사 장면](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-04-yandere/outputs/image.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-04-yandere/outputs/final_prompt.txt) · [작성자 평가](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-04-yandere/outputs/evaluation.json) · [실행 원장](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-04-yandere/runs/image_runs.ndjson)

부드러운 볼 접촉과 출입구를 가로지른 도끼는 함께 보인다. 독립 평가자는 몸이 겹친 부분 때문에 도끼 그립의 소유를 확실히 확인하지 못했다. 프롬프트는 여기서 더 나아가 퇴장 시도·후퇴·가방이 떨어지는 순간·지정한 눈의 눈물을 요구했다. 이 추가 조건의 미충족을 원문에 없던 세부 요구까지 모두 사용자가 지시한 것처럼 설명하지 않는다.

## 이미지가 전달되지 않은 두 사례

| 사례 | 프롬프트 | 생성 결과 기록 | 서비스 요청 ID |
|---|---|---|---|
| 큐피드 | [보기](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-01-cupid/outputs/final_prompt.txt) | [원본 오류](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-01-cupid/outputs/native_tool_result.json) | `7499fbee-de2e-4e21-9e72-609966f8f806` |
| 항공기 | [보기](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-05-aircraft/outputs/final_prompt.txt) | [원본 오류](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-05-aircraft/outputs/native_tool_result.json) | `8a051410-4b38-46c5-bafe-5fde4b95d267` |

## 증거 연결

- [실험 설계·원문·참고 해시](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation-manifest.json)
- [변경 없이 보존한 원문 기준](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation/independent-review/criteria.json)
- [프롬프트를 읽기 전 픽셀 관찰](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation/independent-review/initial-observations.json)
- [독립 세부 계약 대조](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation/independent-review/final-review.json)
- [산신령 일반 의미·증거 대조표](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation/independent-review/arm-02-frozen-semantic-matrix.md)
- [각 환경의 파일·프롬프트·실행 입력·원장 결속 검증](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation/artifact-verification.json)
- [구현 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation.md)

기준 SHA-256: `d33b8477aa027db34aadf74d8a799cbf0a88ff603826c5d3b87f621dc1f8cf51`  
1차 관찰 SHA-256: `30e5fe7b7014505b29b522789b255ac9e4f6e87d654d25d375b995072099ad17`  
독립 최종 평가 SHA-256: `e541a6c06e5f0a1a851655284119daa08931d8ca951b8ff7ae30fe801f6e744b`  
생성 소스 SHA-256: `c0eeb2bf23fc913b79a4161361d9da305c89cd4ce4a277dae77d06f5d6a727c6`
