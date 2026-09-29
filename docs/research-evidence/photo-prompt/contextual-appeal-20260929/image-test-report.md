# 두 조사 통합 후 독립 이미지 테스트

두 조사 자료의 반영과 세 이미지 생성은 완료했다. **새 후보 231개가 실제 이미지 제작에 활용됐다는 검증은 통과하지 못했다.** 사전·색인·계약 검사는 통과했으나, 세 후보팩에서 새 후보가 반환되지 않았다. 기존 후보에 새로 붙인 귀 장식 문맥 하나만 선택됐다.

세 독립 에이전트는 `gpt-6-sol`, 추론 `max`로 각자 복잡한 장면을 정했다. 저장 기본값 `1/0`은 유지하고 이번 실행만 `sensual_editorial=3`, `fetish_fashion=3`을 사용했다. 각자 코어를 고정한 뒤 v6 후보팩을 정확히 한 번 만들고 첨부 사진을 얼굴·머리 외형 참고로 사용했다. 이는 후보 모집단에서 확률 추출한 무작위 실험은 아니다.

내장 이미지 생성 도구는 총 4회 호출했고 이미지 3장을 보존했다. 정비소 첫 호출만 출력 안전 필터에 차단됐으며 동일한 프롬프트·참고 이미지·인수로 한 번 더 호출해 성공했다. 나머지는 첫 호출에 성공했다. 생성 모델의 세부 ID는 도구가 노출하지 않았으므로 Sol은 프롬프트 작성 에이전트 모델을 뜻한다.

| 장면 | 기본 관찰 기준 | 후보 추가 관계 | 신체 필수 검사 | 주요 미충족 |
|---|---:|---:|---:|---|
| 심야 정비소 | 2/5 | 0/1 | 2/5 | 끈·링의 연속 접촉, 바닥 광선, 원숄더 좌우 |
| 새벽 여객선 | 4/5 | 0/2 | 4/5 | 손목–로켓 사슬, 팔꿈치 지지, 유리 반사 출처 |
| 극장 분장실 | 3/5 | 1/1* | 5/5 | 느슨한 힌지·기울기, 무심한 표정 |

부분 관찰은 실패로 계산했다. 숫자는 미적 품질 점수가 아니다. *분장실의 추가 관계는 손·귀·금속 접촉과 귀 윤곽 확보라는 범위에서 에이전트가 통과로 판정했다. 부모 검토에서도 이 큰 관계는 보이지만, 문장에 적힌 정확한 고정부 아래쪽 집기는 판별하기 어렵다. 따라서 모든 세부의 통과나 새 문맥의 인과 효과로 확대하지 않는다.

## 검색 단계에서 확인된 문제

각 축에서 전체 4,913개 후보가 검색 대상에 들어갔고 모두 임베딩 커버리지가 있었다. 새 후보는 212개가 입장했다. 18개는 `setting` 변경 차원 때문에, 1개는 기존 슬롯의 대상 범위 때문에 제외됐다. 입장한 212개는 검색 순위와 다양성 선택을 거쳐 최종 12개로 압축되는 단계에서 모두 빠졌다. 안전 필터가 212개를 제거한 것이 아니다. 전체 후보팩 어디에도 새 `ctx_` 후보가 없었다.

실제 쿼리는 장면 전체와 설정 정의를 함께 담는다. 작은 접촉·착용 관계보다 전반적인 패션·구도 후보가 우세할 수 있다는 것이 후속 가설이다. 어떤 문자열이나 점수 항이 원인인지는 별도의 제거 비교를 하지 않아 확정하지 않는다. 새 ID 우대나 의무 채택 규칙으로 결과를 맞추지 않았다.

[후보 입장 진단](production-admission-diagnostic.json) · [실제 쿼리 재구성](production-query-diagnostic.json) · [기계 판독 결과](image-test-results.json)

## 원본 이미지와 독립 검토

### 비 오는 심야 오토바이 정비소

[원본 이미지](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/craft/craft-native-02.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/craft/final_prompt_en.txt) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/craft/completion_summary.json)

![비 오는 심야 오토바이 정비소](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/craft/craft-native-02.png)

켜진 전조등, 기름때 묻은 손, 허리의 가죽 패널과 강한 패션 방향은 보인다. 끈이 원래 어깨끈이라는 사실이나 정확한 링 통과는 확인되지 않는다. 후보에서 추가한 원숄더는 인물의 좌우가 반전됐다. 촬영 구도 밖의 부츠 접지는 검증할 수 없다.

- 수리 전후의 변화는 정지 사진으로 증명하지 않는다.
- 기준선의 완료된 수리를 입증하겠다는 일부 조건은 기술적 능력 또는 시간 변화까지 포함해 단일 프레임 검사로는 과도하다. 현재의 점등·도구·접점으로 범위를 좁힐 필요가 있다.

### 새벽 여객선의 창문과 은빛 로켓

[원본 이미지](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/sensory/sensory-native-01.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/sensory/final_prompt_en.txt) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/sensory/completion_summary.json)

![새벽 여객선의 창문과 은빛 로켓](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/sensory/sensory-native-01.png)

유리의 물방울, 손끝과 은색 물건 사이의 공극, 아래로 향한 시선, 광택 코트와 부드러운 천의 대비는 보인다. 사슬의 손목부터 물건까지 이어지는 전체 경로와 팔걸이 지지는 가려진다. 강한 붉은 수직 반사는 유리 표면보다 창밖 수면의 반사로 읽힌다.

- 시선이 손과 물건이 있는 영역으로 향하는 것은 보이지만 양안의 정확한 3D 초점까지 입증하는 판정은 아니다.
- 응결과 외부 빗물, 실제 실크 섬유, 물건의 사적 의미를 픽셀만으로 확정하지 않는다.

### 극장 분장실 거울 앞 귀 장식 조절

[원본 이미지](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/mirror/mirror-native-01.png) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/mirror/final_prompt_en.txt) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-runs/research-integration-20260929/mirror/completion_summary.json)

![극장 분장실 거울 앞 귀 장식 조절](/Users/chasoik/Projects/image-prompt/generated_images/research-integration-20260929/mirror/mirror-native-01.png)

거울, 손과 귀 장식의 접촉, 노출된 귀 윤곽, 새틴과 버클, 분장실 맥락은 보인다. 느슨한 힌지와 정확한 기울기는 구분하기 어렵고, 작은 미소는 즉흥적 실수보다 의도한 포즈로 읽힌다.

- 보강된 기존 후보의 손·귀·금속 접촉은 관찰되지만 최종 문장의 정확한 고정부 아래쪽 집기는 별도로 입증하기 어렵다.
- 기준선에도 귀 접촉과 거울이 이미 있으므로 추가 문맥이 이미지의 차이를 일으켰다는 인과 주장은 하지 않는다.

## 남은 개선 방향

장면 전체 검색 외에 작은 행위·접촉·착용 방식에 초점을 둔 짧은 의미 질의를 비교할 필요가 있다. 새로운 자료라는 이유로 우선순위를 주는 대신, 실제 장면과 관계가 맞는 후보가 충분히 노출되는지 별도 사례에서 측정해야 한다. 후보 노출 → 선택 → 프롬프트 추가 → 픽셀 관계를 각각 기록하고, 선택되지 않은 후보를 이미지로 검증했다고 세지 않는다.

키워드를 지정한 통제 테스트도 별도로 필요하다. 현재의 독립 컨셉 세 개는 기존 스킬의 자연스러운 검색 사용을 관찰하는 데 유효했지만, 새 후보 전체의 렌더링 능력이나 취향 개선을 검증한 실험은 아니다. 정확한 현재 접촉과 공간을 평가하고, 수리 전후 변화·개인 기억·냄새·욕망처럼 정지 사진 밖의 주장은 분리해야 한다.

이번 실행 중에는 런타임 소스를 바꾸지 않았으며 65개 파일의 동결 해시가 유지됐다. 사용자 취향 판단은 아직 받지 않았다. 검색 개선안과 추가 생성은 이 결과에 몰래 섞지 않았다.
