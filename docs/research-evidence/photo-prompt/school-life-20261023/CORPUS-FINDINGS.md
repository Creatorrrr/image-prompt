# 기존 source 조사와 반영 판단

현재 원문 모듈을 읽은 스냅샷이며 검색 실행·native source 심사·설치본 검증은 수행하지 않았다.
관찰: 81개 모듈, 20,341개 CID, 15,120개 binding, 149개 catalog 슬롯.

|좁힌 가시 원문 검색|CID 수|
|---|---|
|school|14|
|classroom|11|
|uniform|18|
|boarding|1|
|council|0|
|cultural_festival|0|
|school_club|0|
|exam|11|
|prom|1|
|bullying|0|
|dark_academia|7|
|gyaru|4|

검색은 en/ko/phrase 필드만 대상으로 한다. aliases·예시·설명에 대한 넓은 검색과 수치가 다르다. `exam`이 `example`, `boarding`이 승차, `prom`이 텔레프롬프터를 잡는 오류를 줄였다. 검색 0건은 의미적 부재나 신규 후보 확정의 증거가 아니다.

각 기존 CID의 전체 record·조건·effects·binding은 corpus-snapshot.json에 저장했다. 아래는 채택 전 triage 제안이다.

|실제 CID|제안|카드|이유|
|---|---|---|---|
|cand_564ee719d63f5899909f03532490e2b1|separate_context|C03, W01, W02, W03|성인 교복 코스프레 인물. 실제 학생이나 일반 교복 구조 후보로 재분류하지 않는다. adult 명칭과 실제 조건의 일치도 추후 native 심사한다.|
|cand_0df22ad2652f5d239338e75226f22c52|reuse_review|W01, W02, W03|교복 체계 일반 문맥은 재사용 검토. 특정 칼라/입깃/레이어 전체가 기존 원문에 있다는 뜻은 아니다. attire_context의 contextual binding 유지.|
|cand_ac61ab4384135edbb8a909b1ec0c8dbe|reuse_review|S01|일반 교실 위치의 기존 선택지. 앞 칠판·책상·통로 구조는 원문에 없으므로 새 의무로 간주하지 않는다.|
|cand_98a65f70c792575ea2f5f0c767ca52b9|refine_review|S01, C02|2000년대 한국이라는 고증 주장이 있으나 물리 성분이 없다. 시대 실물 자료 보강 전 범용 교실의 증거로 사용하지 않는다.|
|cand_455838fef14a5caba8aa45911dc42aae|reuse_review|S10, C01|오크 서가 도서관을 선택한 경우 재사용 검토. 학교 장르에 자동 부여하지 않는다.|
|cand_c65e606e900d508aac906a5b71291cb2|separate_context|C04|성인 갸루 실천·styling 문맥. 학생/불량/성적 행동으로 확대하지 않으며 requires_primary_any_tags를 유지한다.|
|cand_ed0409b561f759cfaa90fd00877e4889|refine_review|A04, A14|책·행·주석·시선·양손의 완전 관계와 effects 유지. 원문의 구체 관계보다 짧은 한글 label을 전체 의미로 오인하지 않는다. 새로운 공동학습과는 별개.|
|cand_17e89ecffe7e5634b84e66e15af751f4|reuse_review|W03|교복 부품 일관성을 점검하는 동작. 착용 의복 자체를 공급하는 후보와 구별.|
|cand_a853ef841c6c5b6c86e6f6b9f5f58ae4|reuse_review|S01, A14|교실 천장 형광등이라는 광원. 2000년대 고증·학교급·번아웃 의미는 없다.|
|cand_58771df5cae55656b194e4946a19e36d|reuse_review|C03, W08|한쪽 어깨 검은 백팩은 소품·접촉 원문으로만 재사용. 학생 신원과 등교 목적을 입증하지 않는다.|

운영 인덱스는 `photo_candidate_search.json`; 관찰된 layout 및 space는 corpus-snapshot.json에 보존한다. 이 연구는 source 총수와 index metadata_count를 직접 동일시하지 않으며, positive/diagnostic 투영과 source SHA closure를 검증하지 않았다.

현재 maintenance 문서의 native V3 source / V10 pack / issued receipt / 설치 세대 경계를 따른다. 연구 owner graph는 actual native fact·guard·effect·permission·role view를 생성하지 않는다. 모든 조건과 의무는 전체 선택 분기를 검토해 후속 작성해야 한다.
