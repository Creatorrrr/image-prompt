# 수사물 데이터 반영과 독립 이미지 테스트

2026-10-25 KST. 사용자 요청에 따른 데이터 반영과 독립 에이전트 3개의 실제
참조 이미지 생성·관찰을 완료했다. 데이터·설치 검증은 통과했고, 수사물 주제는
3/3 장면에서 읽힌다. 모든 사전 관계를 충족한 strict 전체 장면은 0/3이며,
신규 후보 채택도 0/3이므로 신규 데이터의 생성 효과는 입증되지 않았다.

|검증 층위|결과|
|---|---|
|실제 데이터 반영|시각 후보 66개·제외 진단용 47개·선택적 binding 132개 추가, 기존 5개 표현 수정|
|설치·데이터 보존·전체 검색 검증|통과; 갱신된 기본 설치본에도 변경분 보존|
|독립 core·사전 testcase·설치 세대 고정|3/3 검증; 동일 최신 skill·동일 원본 참조|
|실제 생성|built-in 3회 성공, 품질 재생성 0회|
|얼굴·머리 참조와 broad 수사 주제|3/3 관찰|
|strict 전체 장면|0/3|
|신규 source의 픽셀 효과·기존 대비 개선|미입증|
|사용자 수용|pending|

완료 기록은 [FINAL.json](integration-evidence/FINAL.json)이며, 개별 최종
프롬프트·테스트케이스·이미지·독립 manifest·평가 기록까지 연결한다.

|독립 장면|실제 이미지에서 확인한 주제|엄격한 실패 지점|개별 결과|
|---|---|---|---|
|A 금융 기록 대조|동일 계좌·금액의 화면과 명세서 비교|연필 끝이 일치하는 항목을 짚지 않음|[A](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-a/FINAL-RESULT.json)|
|B 훼손 봉인 조사|카메라·스케일을 사용하는 현장 조사와 별도 카트 담당자|절단 끝 사이 간격·전체 지지 가시성 부족|[B](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-b/arm-result.json)|
|C 선착장 탐문|인물 사진·메모·지도와 직원 응답|시선·좌우 손 역할·정확한 표적 관계 어긋남|[C](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-c/FINAL-RESULT.json)|

최종 프롬프트: [A](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-a/final-prompt.txt) · [B](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-b/final-prompt.txt) · [C](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-c/final-prompt.txt)

## 실제 반영 범위

321개 용어를 다루는 339개 advisory route와 원래 시각 카드 76개·문맥 카드
40개의 구분을 유지했다. 신규 optional visual 후보 66개와 diagnostic 47개,
선택적 binding 132개를 추가했다. Diagnostic은 문맥 40개·근거 보류 6개·교육도
1개이며 positive 검색에서 제외된다. 인접한 기존 complete source 3개를
그 원래 범위로 재사용하고, 기존 후보 5개의 한글·별칭 표현을 좁게 수정했다.
기존 조건·효과·출처와 나머지 후보·정책·binding은 보존했다.

- [시각 후보 source](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_investigative_fiction_20261025.json)
- [의미 registry](../../../../skills/photo-prompt-image-generator/assets/photo_investigative_fiction_semantics_20261025.json)
- [추가 binding](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_investigative_fiction_bindings_20261025.json)
- [카드→CID 대응](integration-evidence/card-candidate-map.json)
- [재사용·보류 판단](integration-evidence/adoption-decisions.json)

이번 변경분만 적용한 시점의 작업 source 수는 22,899→23,012다. 이후 같은
작업 폴더에 별도 음악·스포츠 작업의 모듈이 동시 추가됐으므로 현재 작업
폴더 전체 수와 이 변경분을 구분한다. 그 별도 모듈은 수정하지 않았다.
실제 선택된 설치본의
기준은 다른 세대의 22,388개였으므로, 설치 후속본에는 해당 기존 source를
보존한 채 수사물 113개만 더한 22,501개가 있다. 작업 폴더에만 있던 별도
주제의 변경을 이번 설치에 함께 실어 보내지 않았다. 설치 kernel 코드는
변경하지 않았다. Source가 추가됐다는 이유로 native approval을 부여하지 않는다.

실제 검색 인덱스는 선택된 봉인 설치본에서 재구축했다. 이번 작업은 다른
작업의 source와 상태를 가진 작업 폴더의 legacy `photo_candidate_search.json`을
쓰지 않았으며, 초기 source 검증에서도 무변경을 확인했다. 이후 그 파일은
별도 동시 작업의 corpus/index 갱신 중 변경된 것으로 관찰돼 덮어쓰거나
되돌리지 않았다. 실행 세대와 인덱스는 각 arm의 runtime receipt·pack에 고정돼 있다.

## 검증 설계

설치본 전체 문서·임베딩·seal·native source를 검증하고, 동결한 개발 요청
20개와 일반 대조 요청 6개를 기준 세대와 후속 세대에서 각각 전체 풀 검색한다.
지정한 신규 CID의 순위는 신규 source 노출을 측정한다. 기존 후보가 의미상
이미 요청을 충족하는지는 전수 판정하지 않으므로 이 수치를 의미 recall,
품질 개선량 또는 독립 holdout 성능으로 해석하지 않는다.

사용자가 요청한 독립 에이전트 3개는 서로의 장면·후보를 보지 않고 랜덤
컨셉, core, 관찰축, 사전 pixel gate와 슬롯 계획을 먼저 동결했다. 모든 arm은
같은 최신 skill 해시와 실제 사용자 요청 envelope를 쓰고 첨부 portrait의
보이는 얼굴·머리만 참고한다. 인물의 신원·나이·직업을 reference에서 추론하지
않으며, 역할과 사건은 작성자가 선택한 장면 설정이다. 후보 조회 뒤에는
complete source 심사, 선택·기각 이유, compose audit, 실제 native 호출,
저장 이미지 관찰을 각각 남긴다.

|Arm|독립 컨셉|사전 테스트 기준|
|---|---|---|
|A|기부금 기록의 수취계좌를 명세서와 화면에서 대조|동일 표적의 문서·화면 대조, 손과 시선의 관계|
|B|하역장에서 절단된 운송 상자의 봉인을 조사|끊어진 봉인, 같은 표적을 향한 카메라·눈금자, 보조자의 카트 지지|
|C|마지막 배편 이후 선착장 직원에게 탐문|사진·동선 지도를 매개로 한 면담, 서로 구분되는 접촉·시선|

소품과 수사물 분위기만 보이는 경우와 전체 필수 관계가 구현된 경우는
구별한다. 읽을 수 없는 글자나 가려진 접촉은 strict 성공으로 세지 않는다.
세 장면은 현재 후속본 테스트이며 baseline과의 이미지 A/B가 아니다.

## 현재 증거

- [작업 source 검증](integration-evidence/source-integration-validation.json)
- [설치 source 보존 검증](integration-evidence/canonical-source-validation.json)
- [봉인된 후속 세대](integration-evidence/successor.json)

봉인·복사·배포 validator와 기본 runtime preflight를 통과한 뒤 설치 선택을
수사물 후속 세대로 바꿨다. H-F2 generation은
`1a3ceaf5e5fcf9fd3f023461918cf204d47b4532751041d85c20fb2b6067b503`, native
generation은 `2cc2ab01662d1b508488562983b65b2b9a260d30cb91e1ab9364530b376ad5e1`다.
기존 문서 vector 21,083개를 그대로 재사용했고 새로 계산한 서로 다른 문서
vector는 71개다. Positive 후보는 21,086→21,152개, 후속 RID는 21,154개다.
설치 과정의 CURRENT 쓰기는 0회다.

이후 공동 작업이 기본 설치 세대를
`d75d1546f9bdb3537d1316c0e14a5a04903fd29b1cedcfc63caefa328b690cd1`로
갱신했다. 이를 이전 세대로 되돌리지 않고
[실제 source 보존](integration-evidence/final-default-preservation.json)과
[전체 배포 H-F2 검증·인덱스 보존](integration-evidence/final-default-search-preservation.json)을
확인했다. 신규 두 모듈은 테스트 설치본과 동일하며, 기존 수정 5개의 전체
native snapshot(내용·조건·효과·출처)도 동일하다. 내부 literal 저장 형태의
정규화 차이는 의미 변경으로 세지 않았다. 기본 인덱스에는 신규 positive
66개가 모두 있고 신규 diagnostic은 0개이며, kernel 코드 해시도 보존됐다.
세 이미지 테스트는 처음 검증한 수사물 세대에 계속 고정돼 있었다.

[52회 전체 풀 검색](integration-evidence/retrieval-qualification.json)에서 후속
세대는 개발 요청 20개의 지정 신규 후보를 모두 1위로 노출했다. 기준 세대에는
이 신규 CID가 원래 없으므로 기준 0→후속 20은 구조적인 추가 source 노출이다.
기존 대안의 의미 충족도를 전수 판정하지 않았고, 작성자가 본 연구 내용에서
만든 요청이므로 recall 개선·holdout 성능·이미지 품질 향상을 뜻하지 않는다.
일반 대조 6개 중 이브닝드레스 요청 1개에는 해당 의상 후보가 top 10에
나왔고 나머지 5개에는 신규 후보가 없었다. 이는 요청과 부합하는 선택적
의상 노출이며 수사 장면의 강제 주입이나 실제 채택의 증거는 아니다.
진단용 신규 47개는 positive 결과에 한 번도 포함되지 않았다.

실제 arm의 managed 검색은 개발 순위 probe와 다르다. A는 4개 query에서
24 occurrence·23개 unique source를 반환했고 신규 1개가 노출됐다. B는
5개 query에서 40 occurrence·36개 unique source를 반환했고 신규 1개가
두 query에 노출됐다. C는 4개 query에서 32 occurrence·31개 unique source를
반환했으나 신규 source 노출은 0개다. A의 빈 narrative_clue 반환도 그대로
유지했다. A의 정확한 scope witness를 확인하니 claim-limit 문장의 부정 표현을
projection이 `nonpositive_scope_without_requested_change`로 처리해 반환이 0개였다.
두 lane 검색은 수행됐다. 이는 해당 query projection의 제한이며 자료가 없다는
증거가 아니다. [실제 검색 노출](integration-evidence/managed-retrieval-exposure.json)은
후보 채택이나 이미지 구현 판정과 별개이며, 이를 개발 요청 20/20 결과와
합쳐 일반 성능으로 주장하지 않는다.

Source 검토 후 A·B는 독립 baseline을, C는 baseline에 기존 source의 일반적인
팔 지지 표현을 참고한 대안을 선택했다. 신규 수사물 source의 실제 채택은
0/3이다. 따라서 이 세 장의 주제 구현 결과가 좋더라도 신규 데이터의 픽셀
효과가 검증된 것은 아니다. 조건에 맞지 않는 source를 억지로 사용하거나
검색을 다시 뽑아 채택을 만들어내지 않았다.

## 저장 이미지 관찰

A는 화면의 연결 계좌와 종이 명세서에 `A-17 / 9,800,000`이 정확히 반복돼
금융 수사 문맥이 분명하다. 손·팔 소유와 참고 얼굴·머리도 읽힌다. 다만
연필 끝은 붉은 원의 위·왼쪽을 향해, 원을 짚는 정확한 접촉과 같은 항목을
겨냥하는 행위 관계가 실패했다. 에이전트와 루트 모두 3/5 gate pass, strict
전체 장면 fail로 판정했다. 루트 평가는 에이전트의 최종 픽셀 판정을 읽기
전에 실제 저장 이미지를 보고 작성했다.

- [A 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-a/investigative-fiction-a.png)
- [A 루트 픽셀 판정](integration-evidence/root-pixel-review-a.json)

B의 실제 생성 이미지를 에이전트와 루트가 각각 직접 확인했다. 얼굴·머리,
카메라와 눈금자를 사용하는 조사 동작, 별도 담당자의 양손·카트 손잡이는
보인다. 두 절단 끝 사이의 명확한 봉인 간격, 완전한 지지 관계, 모든 결정적
관계의 동시 가시성은 미달이다. 에이전트는 5/8 gate를 pass로 기록했고,
루트는 봉인 상태를 포함한 topic_realization의 엄격한 전체 조건도 partial로
판정해 4/8로 기록했다. 두 평가 모두 broad 수사 주제는 visible, strict 전체
장면은 fail이다. 점수를 합치거나 서로 다른 이미지의 성분을 모아 통과시키지
않았다.

- [B 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-b/archive-loading-bay.png)
- [B 루트 픽셀 판정](integration-evidence/root-pixel-review-b.json)

C에서는 사진·노트·지도를 매개로 선착장 직원에게 탐문하는 주제와 장소가
분명하다. 에이전트는 3/6, 루트는 2/6 gate를 strict pass로 판정했다. 에이전트는
증인의 지도 접촉을 pass로 봤고, 루트는 요구된 정확한 부두 지점과 손끝이
짚는 분기를 구별해 C2를 partial로 판정했다. 두 평가 모두 strict 전체 장면은
fail이다. 조사자의 시선은 지도
지점보다 직원 얼굴을 향하고, 직원의 손끝은 부두 모양 표식 자체가 아닌
오른쪽 위 분기를 짚는다. 사진을 든 팔도 선언한 왼손과 뒤바뀌어 있다.
노트 위 펜 끝에는 사전 계획의 멈춘 기록 동작을 확정할 가시적인 뜬 간격이
없다. 이는 캐릭터 소유자가 바뀌었다는 뜻이 아니라 같은 인물 내 좌우 손과
정확한 표적의 관계가 달라졌다는 판정이다.

- [C 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-c/generated-image.png)
- [C 루트 픽셀 판정](integration-evidence/root-pixel-review-c.json)

루트 직접 관찰 기준 broad 수사물 주제는 3/3, 모든 사전 gate를 충족하는
strict 전체 장면은 0/3이다. 신규 후보 채택도 0/3이므로 이 결과로 신규
데이터의 생성 효과나 기존 대비 개선을 주장하지 않는다. 각 장면은 built-in
생성 1회이며 품질 재생성은 없다. 세 arm 모두 managed 평가 기록은 유효하고
최종 phase는 `review_record_validated`, 픽셀 기술 판정은 `fail`이다. 실제 이미지·
prompt hash, 변경하지 않은 사전 testcase, 독립 manifest와 pin을 루트가 다시
대조해 [최종 검증](integration-evidence/FINAL.json)을 통과했다.
Commit/push와 사용자 수용 판정은 이번 결과에 포함하지 않는다.

## 확인된 한계에 따른 후속 보완 순서

1. `수사물 용어 정리`라는 대화 표제에서 실제 장르어와 문서 작업어를 구분하는
   topic query 범위를 별도 개발 요청으로 검증한다. C에서 일반 정리·포즈
   source가 주로 나왔으므로, 현재 표제 전체 검색을 충분한 장르 검색으로
   간주하지 않는다. 원 사용자 입력과 topic 연결은 그대로 추적해야 한다.
   A에서 드러난 positive 변화 의도와 claim-limit의 혼합도 별도 고정 요청으로
   검증해, 부정된 법적·서사적 결론이 긍정 시각 요청 전체를 지우지 않게 한다.
2. 실제 반환 source의 인물 조건과 전체 명제가 장면에 맞는지 먼저 심사한다.
   조건을 reference에서 추정하거나 기존 조건을 지워 채택률을 높이지 않는다.
   발견한 미지원 관계가 필요하면 별도의 complete optional source를 작성하고
   새 조건·효과·owner 심사를 받는다.
3. 신규 source의 효과를 검증할 다음 실험은 이번 3장과 분리해 사전 등록한다.
   source별 적합·부적합 요청, 각 조건, 대안 source와 최종 문장 운반을 함께
   기록하고 실제 채택된 source만 픽셀 검증 대상으로 센다. 이번 노출 개발
   요청이나 실패 이미지를 독립 holdout으로 재명명하지 않는다.
4. B의 봉인 절단 끝·간격, 스케일의 같은 표면, 인물·카트 지지를 함께 읽을 수
   있는 구도를 별도 장면 설계 문제로 다룬다. 검색·audit 통과를 가시성의
   대리 지표로 쓰지 않는다.

이 순서는 확인된 부족분에 대한 계획이며, 아직 실행하지 않은 추가 생성이나
개선 효과를 완료로 기록하지 않는다.
