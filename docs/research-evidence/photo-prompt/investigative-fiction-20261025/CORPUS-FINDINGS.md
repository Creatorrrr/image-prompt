# 현재 corpus 관찰과 기존 source 비교

2026-10-25 KST. [corpus-snapshot.json](corpus-snapshot.json)은 작업 시점의 working-tree manifest에 명시된 원천 121개 모듈의 해시를 보존한다. HEAD는 `85884333ca146a28bfa0c455fa1d9e64d5ee8099`다. 기존 checkout에는 수정 27건·삭제 2,454건·미추적 171건이 관찰되었고 이 연구의 정리 대상으로 취급하지 않았다. 이 수치는 최초 snapshot 시점의 Git 표시 개수이며 전체 파일 수나 최종 상태가 아니다.

|원천 관찰|개수|
|---|---:|
|전체 canonical source record|22,899|
|visual_option|15,124|
|visual_profile|3,834|
|relationship_mechanism|135|
|visual_bundle|2,204|
|relationship_concept|3|
|diagnostic|1,599|
|slot binding|17,836|
|manifest 중 누락 모듈/중복 CID|0 / 0|

전체 원천 수에는 diagnostic이 포함되므로 긍정 검색 source 수와 같지 않다. visual bundle의 branch 실현 문서 수도 별도다. 이 스냅샷만으로 설치된 검색 snapshot과 working tree의 동등성이나 native qualification의 현재 유효성을 확인한 것은 아니다.

## 탐색용 lexical 관찰

|정규식 묶음|적중 source 수|
|---|---:|
|investigation|82|
|scene_evidence|19|
|forensic|78|
|interview|28|
|digital_finance|1|
|narrative|8|
|noir|37|
|wardrobe|27|
|harm_context|127|

묶음은 겹친다. 검색한 범위는 source의 `content` JSON이며 별칭·메타데이터·진단 문장 때문에 오적중이 포함된다. 기본 content 밖의 모든 realization branch를 전수 의미 검색한 것도 아니다. `trench`에는 참호가, `fingerprint`에는 거울 손자국이, `witness`에는 초자연 사건 목격이 섞인다. 표의 1건을 ‘디지털·금융 수사 후보가 전체 corpus에 단 하나’라는 주장으로 읽으면 안 된다. 자연어 검색 rank·회수율·코사인 점수·native admissibility를 측정하지 않았다.

재현 코드 [audit_corpus.py](audit_corpus.py)는 기존 snapshot을 덮어쓰지 않는다. [corpus-hit-details.json](corpus-hit-details.json)은 이 방법으로 찾은 source의 전체 레코드·바인딩을 연구용으로 보존하며 최신 운영 truth로 쓰지 않는다. 구현 시에는 현행 source와 선택 branch를 다시 읽어 비교한다.

## 28건의 직접 비교와 처리 방향

[existing-source-decisions.json](existing-source-decisions.json)은 비교한 CID마다 전체 원문·조건·효과·바인딩과 canonical source 해시를 포함한다. 판단 개수는 refine 4, 별도 신규 3, reuse 검토 9, 제한적 재사용 4, context 재사용 1, context/범위 검토 5, sequence 검토 2다. 이들은 운영 승인 결과가 아니라 구현 제안이다.

|사례|관찰|구체 반영 방향|
|---|---|---|
|번호 표지|`ko`가 영어와 같고 현재 흔적 관계가 없음|번역 보완과 A02 배치 대안을 구분|
|표지 검사 행위|`examining an evidence marker`는 표지를 검사함|기존 행위를 보존하고 흔적 관찰은 별도 source|
|감식 매크로/요원/탁자|영어 복제·`in a ... table` 구문·일반적인 역할|한영/구문 수정과 실제 물체·장소·행위 추가를 분리|
|감식팀|역할 분리와 primary guard가 이미 있음|두 명/여러 명의 전체 의미·subject effects를 보존해 재사용|
|번호·눈금·방향·기록 묶음|완결 묶음이 이미 있으나 effects가 비어 있음|일부를 빼서 채택하지 않고 실제 효과를 먼저 검토|
|전체→중경→근접|composition/action에 여러 단계의 완료 포함|정지 상태와 sequence를 서로 다른 평가 경로로 분리|
|봉투·검체관·라벨|검체/기록 관계의 기존 한 실현|봉인 경계와 과거 전체 chain을 추가 보장한다고 보지 않음|
|괴이 보관 장비|write-blocked reader와 파형·봉인 트레이에 특정 세계 guard|guard 유지, 일반 디지털 장면은 독립 대안|
|붉은 실 보드|EN/embedding에 self-retension이 있음|마법 source 보존, 현실 핀/실 보드는 별도|
|트렌치 부품|견장·가슴 플랩·허리 고리/벨트가 이미 있음|장르별 CID 복제보다 기존 전체 source 재사용|
|문 빗장|문과 문틀의 연결이 이미 있음|모든 출입 불가능성까지 확장하지 않음|
|수갑|앉은 성인의 앞 손목 두 개와 체인|앉음·성인·소유자·체인 관계 유지|
|상해 분장|인조 피부에 그린 분장 표본|실제 멍·방어흔·삭흔 대체 충족 금지|
|인터뷰 마이크|단독 성인·중간 거리·앞쪽 마이크|두 사람 경찰 면담으로 자동 승격하지 않음|
|이동 중심 인신매매|모집→이동/은닉→착취의 선택적 경로|이동 없는 사례를 배제하는 보편 정의로 쓰지 않음|
|성적 침해/고문|원뜻에 여러 행위·문맥, effects는 style|역할·행위·목적·통제를 실제 직접 가시 사실/허가로 승인하지 않음|
|사지 절단 두 source|대응 신체와 분리 부분·경계·틈이 이미 있음|기존 전체 뜻·body geometry·조건을 검토. 사후성·원인·동의는 별도|
|성적/의료 문맥 diagnostic|임상 노출·성적 관심·역할극·침해·시체성애를 구분|context로 재사용하고 긍정 시각 검색으로 승격하지 않음|

기존 카드의 문제를 찾았다는 사실만으로 실제 운영 출력에서 그 문제가 발생했다고 단정하지 않는다. 이번 연구는 이 source들을 실제 검색·채택·생성으로 실행하지 않았다. 원천 해시의 유지 여부만 [VALIDATION.json](VALIDATION.json)에서 별도로 확인한다.
