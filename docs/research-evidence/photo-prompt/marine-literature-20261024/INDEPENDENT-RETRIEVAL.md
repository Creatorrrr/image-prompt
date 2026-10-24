# 독립 장면 검색의 관찰 결과

카드 내용을 명시한 개발 질의와 무작위 전체 장면은 다른 시험이다. 개발 질의 83개 중 특정 카드에 매핑된 64개에서 top-8은 58개, top-32는 61개였다. 이것은 독립 holdout 정확도나 원뜻·소유 관계 판단의 합격률이 아니다. 원래 제안한 95% 목표를 달성했다고 표시하지 않는다.

## 후보 조회 전 확정한 세 장면

|arm|독립 컨셉|직접 선택한 슬롯|검색|
|---|---|---|---|
|A|부츠 한 짝을 장식된 받침 위에서 엄숙히 검열하는 병영 쿠튀르|wardrobe_style, contact_point|슬롯2 + topic/baseline2|
|B|해안 도로에서 예비 바퀴를 의전 대상으로 대하는 고장 차량 장면|action, social_cue|슬롯2 + topic/baseline2|
|C|침수된 생활관 복도에 고무보트 행정 검열대를 차린 장면|space_condition, social_cue|슬롯2 + topic/baseline2|

요청 원문·참조 이미지·controls는 공통이며 baseline/core·슬롯 목표·픽셀 게이트는 각 agent가 후보 조회 전에 작성했다. 다른 arm의 후보나 결과를 서로 공유하지 않았다. 실제 요청 파일과 해시는 dispatch 전에 준비했지만 공식 neutral envelope init은 dispatch 후, agent들이 core 작성을 보류한 상태에서 완료했다. 따라서 envelope가 dispatch 이전에 발행됐다고 주장하지 않는다. 후보 조회 이전 의미 동결 기록과 이 절차상의 시점 한계를 함께 보존한다.

## 순위 창과 실제 노출

최신 스킬의 creativity=1 정책은 질의당 rank-32 창에서 8개를 균등 비복원 추출한다. 순위 창에 있었다는 사실과 agent에게 실제 전달된 후보를 구분한다.

|arm|rank-32 안의 신규 자료|실제 전달된 신규 CID|신규 후보 채택|
|---|---|---|---|
|A|topic의 V060 16위|0개|0개|
|B|topic의 V060 16위|V060 1개|0개: 예비 바퀴 장면에 컨테이너 탑은 무관|
|C|topic의 V060 16위, baseline의 V065 23위|0개|0개|

세 arm의 slot lane에는 신규87CID가 rank-32 안에 없었다. 이 결과로 신규 후보가 전체 코퍼스에 없다고 판단하지 않는다. 등록·인덱스 포함 검증은 별도로 통과했다. 반대로, 이번 이미지가 장르와 닮았더라도 신규 후보가 프롬프트에 전달됐다는 증거로 삼지 않는다.

실제 `__request_topic__` 질의에는 실행 지시인 ‘랜덤한 컨셉을 정하여’, ‘첨부한 이미지를 활용하여 프롬프트 작성하고 이미지 생성’과 해병문학 주제명이 함께 들어갔다. 이것이 노출 감소에 얼마나 기여했는지는 분리 실험하지 않았다. 다중 사건을 담은 긴 baseline, 슬롯이 요구한 의미와 개별 카드의 차이, rank-window sampling도 함께 검토해야 한다. 수치에 맞추려고 질의·게이트·컨셉·샘플 seed를 사후 수정하지 않았다.

## 후속 개선 계획

1. 요청 원문 보존과 검색용 주제 문장 구성을 분리한다. 실행 지시가 실제 주제 질의에 들어가는 경로를 확인하고, requester meaning·참조 조건은 그대로 유지하는 회귀 사례를 만든다.
2. 동일한 frozen query에서 전체 순위, rank-window, 샘플 노출, 의미상 적합성, 채택을 각각 집계한다. 신규 자료라는 이유만으로 가산점이나 강제 채택을 넣지 않는다.
3. 모자 구조·패치 운반체·부츠 부품·식판 구획·차량 승객실·침상 통로 등 개별 관찰 계약을 실제로 요구하는 별도 독립 시험을 설계한다. 컨셉과 필수 게이트를 먼저 동결하고 조회하며, 장르명만으로 특정 외형이나 민감 장면을 강제하지 않는다.
4. 현재 낮은 순위 6개를 한영 의미 차이·기존 재사용 범위·문맥/관찰 불가능성 별로 검토한다. `RETRIEVAL-FOLLOWUP.json`에 원질의와 순위를 보존했다. 같은 개발 질의의 점수만 올린 결과를 일반화하지 않는다.
5. 신규 후보가 실제 채택된 장면에서 source→prompt→도구 입력→원본 픽셀을 연결해 검증한다. 현재 세 장면의 신규 데이터 전이 결과는 `NO_NEW_SOURCE_TRANSFER`이며, 96개 카드의 픽셀 qualification은 하지 않는다.

근거: `integration-evidence/retrieval-qualification.json`, `independent-frozen-query-texts.json`, `independent-window-vs-exposure.json`, `new-visual-cids.json`, 각 `image-tests/` arm의 전체 source review와 전이 판정. 원본 픽셀 결과는 `INTEGRATION-RESULTS.md`에서 따로 기록한다.
