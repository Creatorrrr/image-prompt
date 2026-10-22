# 독립 생성 세 장의 실제 결과

최신 `photo-prompt-image-generator` 작업 스킬과 실제 첨부 reference를 사용했다. 서로 다른 세 서브에이전트가 후보 검색 전에 컨셉·baseline·사전 판정 기준을 고정한 뒤 검색·원문 검토·대안 비교·프롬프트 작성·내장 이미지 생성·픽셀 검토를 수행했다. 각 arm 1회 생성, 재시도 0회다. 코디네이터도 같은 원본을 직접 열어 대조했다.

**주제의 시각적 단서는 나타났지만, 복합 관계 전체 통과는 0/3이다.** 아래 숫자는 원래 사전 gate 중 충족한 개수이며 이미지 품질 점수나 사용자 선호 점수가 아니다. 부분 반영과 가려져 확인 불가는 완전 통과로 세지 않았다. 신규 데이터로 인한 품질 개선은 아직 입증되지 않았다.

|Arm|복잡한 컨셉|사전 기준|미충족 관계|
|---|---|---|---|
|A|마른 운하 여관의 차 나눔과 별을 품은 다른 그릇|3/6|나무→산호 전환 경계, 거의 소진된 물, 그릇 간 증기 끝점·공간 깊이|
|B|철도 온실에서 팔의 막을 돌보고 외부 거대 생태로 작은 생물이 이동|3/7|좌우 팔의 역할, 건조부/습윤부 대비, 이동·같은 뿌리의 전체 접합|
|C|거주 도시의 유기적 설비 수리와 작은 수조 속 거대한 눈|6/8|역전 폐허·반대 그림자, 명확한 막 압축·각 램프까지의 마지막 공급 경로|

## A — 환대와 자원 배분

![A: 마른 운하 여관의 차 나눔](/Users/chasoik/Projects/image-prompt/generated/photo-runs/genre-fusion-a-20261022-0aa8c0b3/delivery/image.png)

[최종 프롬프트](image-tests/arm-a-prompt.txt) · [사전 기준](image-tests/arm-a-preregistered-testcase.json) · [에이전트 픽셀 검토](image-tests/arm-a-agent-pixel-review.json) · [코디네이터 대조](image-tests/arm-a-coordinator-pixel-review.json)

등불·난로가 있는 생활 공간, 주인의 붓기 동작과 손님의 같은 그릇, 창밖 마른 수로는 읽힌다. 산호와 천체 그릇도 같은 카운터에 있다. 그러나 산호가 나무 자체의 연속 변환인지, 증기가 실제 인간 찻그릇에서 시작해 별 그릇 안으로 들어가는지는 명확하지 않다. 물이 줄어든 외형과 마지막 식수라는 서사 사실도 다르다.

이번 신규 C01·G01 두 후보가 검색됐다. G01의 익숙한 가까운 그릇과 먼 풍경이라는 범용 구도만 영감으로 참고했으며 원문 전체 채택은 0이다. 그 보조 gate 역시 내부 깊이가 모호해 미통과다. 코디네이터의 초기 5/6 판정은 끝점 대조 후 3/6으로 정정했으며 초기 기록을 보존했다.

## B — 신체 변화의 돌봄과 생태

![B: 철도 온실의 막 돌봄](/Users/chasoik/Projects/image-prompt/generated/photo-runs/genre-fusion-b-20261022-b3ac6f55-slots4/image.png)

[최종 프롬프트](image-tests/arm-b-prompt.txt) · [사전 기준](image-tests/arm-b-preregistered-testcase.json) · [에이전트 픽셀 검토](image-tests/arm-b-agent-pixel-review.json) · [코디네이터 대조](image-tests/arm-b-coordinator-pixel-review.json)

한 팔에 연결된 반투명 막과 다른 손의 지지, 젖은 이끼·온실의 생활 도구·창밖 쇠퇴한 철도는 명확하다. 다만 팔의 좌우 역할은 사전 배치와 반대로 보이고, 젖어 펴진 부분과 마른 채 말린 부분의 대비가 충분하지 않다. 작은 생물의 행렬이 뿌리를 따라 올라가도 그 뿌리가 외부 거대 생물에 붙는 마지막 접합은 가려져 있다.

이번 신규 A01·C11 두 후보를 검토했지만 완전한 대안 10개와 비교한 뒤 baseline을 유지했다. 신규 영감·원문 채택은 모두 0이다. 초기 슬롯 준비 오류는 검색 전에 발생했고, 같은 core·baseline·사전 기준의 재바인딩 이력과 seed 차이를 따로 남겼다.

## C — 거주 도시의 시설 유지

![C: 유기적 설비 수리와 검은 수조의 눈](/Users/chasoik/Projects/image-prompt/generated/photo-runs/genre-fusion-c-20261022-c8c512a7/image.png)

[최종 프롬프트](image-tests/arm-c-prompt.txt) · [사전 기준](image-tests/arm-c-preregistered-testcase.json) · [에이전트 픽셀 검토](image-tests/arm-c-agent-pixel-review.json) · [코디네이터 대조](image-tests/arm-c-coordinator-pixel-review.json)

몸 같은 막·낡은 청색 시설·황동 부품과 정비 동작, 머그·빵·거주 창문, 같은 시설 아래의 거대한 눈이 한 공간에 강하게 통합된다. 반면 홍채의 폐허가 거꾸로 매달린 형태인지와 관 그림자에 반하는 원형 그림자는 명확하지 않다. 액체가 찬 출구와 램프가 있어도 압축 경계와 각 공급 말단이 모두 노출된 것은 아니다.

이번 신규 후보의 실제 노출은 **0개**다. D16은 기존 다크 판타지 corpus의 후보로, 낮게 보이는 붉은 태양의 범용 연출에만 영감으로 사용했다. 신규로 잘못 분류한 초기 보고서는 보존하고 정정했다. 신규 원문 채택도 0이다. 코디네이터의 초기 7/8은 압축·말단 대조 후 6/8로 정정했다.

## 판정의 범위

18개 관리형 질의에서 후보 occurrence 136회, 고유 CID 112개를 검토했고 이번 신규 96 CID와의 교집합은 4개다. 신규 자료의 범용 영감 1건과 완전 채택 0건을 구분한다. 새 후보의 전체 source 관계에 대한 픽셀 자격, 96개 카드·217개 gate의 전수 통과, baseline 대비 품질 개선 또는 사용자 수용은 검증하지 않았다. 새 데이터가 선택되지 않은 장면의 성공이나 실패를 그 데이터의 생성 효과로 귀속하지 않는다.

얼굴·머리는 첨부 파일의 외형 안내를 비교한 것으로 실제 신원·나이의 일치를 보장하지 않는다. 붉은 태양·마른 풍경은 허구의 장르 단서이며 실제 항성 진화·연대·사회 윤리·돌봄의 효능을 입증하지 않는다. 사용자 평가는 pending이다.

[반영 및 후속 검증 계획](INTEGRATION-RESULTS.md) · [모든 이미지·프롬프트·실행 기록 경로와 해시](IMAGE-TEST-RESULTS.json)
