# 기존 코퍼스와의 차이

진단 기준: 20,054 candidates / 14,687 bindings / 75 manifest modules. [원문 29개](existing-source-snapshots.json), [관계로 고른 이웃 8개](topology-neighbors.json), [지정 긍정 필드 어휘 탐색](CORPUS-AUDIT.json)을 함께 읽는다. 첫 두 어휘 일치의 선택 순서는 manifest 순서이며 검색 순위가 아니다. 두 스냅샷 집합은 중첩될 수 있다.

|기존 의미/원문|관찰한 조건·효과/관계|반영 판단|
|---|---|---|
|`cand_6002ff059dd85912ad9037019ee3299f` 압력 전이실|안·밖 해치와 전이실, 외부 시야의 완전 명제. location/object_structure/space_condition 연결.|V11 reuse 제안. 신규 장르명 CID로 복제하기 전에 실제 canonical 사실·effect·역할 자격을 검토한다.|
|`cand_437476164ca957b29be8f79121d9d23d` 라디에이터|단열 담요 모듈·패널·연결 배관을 구분. body_geometry/composition/material/relationship/setting 효과가 있다.|V14 reuse 제안. 물체 추가와 배관 연결도 공간·재료·기하를 바꾼다. props만의 사소한 변경이라고 취급하지 않는다.|
|`cand_0331b45fc2e85e2bbb4611167d7187a0` ECLSS|물 회수·공기 처리·산소 유닛의 분리와 연결.|V72 reuse 제안. 과학적으로 올바른 기능명도 실제 작동·폐쇄율을 승인하지 않는다.|
|`cand_7b74028598cd503abdcd5256886084e5` EVA worker|성인 작업자·압력복·생명유지 배낭·tether의 짧은 명제. effect는 subject.|V10 refine. 줄 양 끝·하네스·선체 고정점은 추가 관계이며 기존 subject-only 효과를 그대로 복사하면 불충분하다.|
|`cand_1fb8cbe7a3515a028ee63ae7f2877291` 동면실|닫힌 캡슐 열 중 열린 빈 캡슐 하나와 성인이 포함됨.|V06은 중립적 개별 캡슐 장면이다. 기존 실종/빈자리 명제를 삭제해 같은 뜻으로 간주하지 않는다.|
|`cand_e3a169af62dc52b08d248c262e7140e1` 세대별 흔적|수리 가구·키 표시·겹친 생활 흔적.|V05 공동 재배/생활은 다른 완전 장면이다. 기존 흔적이 실제 여러 세대의 연속을 증명하지 않는 경계를 유지한다.|
|`cand_190e6d55275459aa9918a04695be8300` 생체 선체|리브 아치와 합쳐지는 살 같은 배관.|V08의 바깥 막·골조·클램프는 다른 토폴로지다. horror와 살아 있음이 자동 추가되지 않도록 완전 대안을 분리한다.|
|`cand_610afa98d8c8552a99d827ad83f47f01` 군체 도상|여러 몸·연결 실·공통 방향. composition/concept의 여러 owner 효과.|V36 refine. 공통 시선·연결 토폴로지·인격 수를 분리한다. 원문보다 강한 공유 의식 사실을 만들지 않는다.|
|`cand_56d99594f24b554e83f1d3448b66ea0d` 족보 책|`for_any: human`; prop; 빈 dimensions/properties.|인간 원문 조건을 외계·합성 인물로 넓히지 않는다. 빈 효과가 신규 완전 장면에도 적합하다는 뜻은 아니다.|
|`cand_2e8fa0a713815781929ac63edcbd30ed` 세관/번역|`requires_primary_any_tags: conlang_conculture_world_trade_scene`; contextual situation 역할; domain 조건.|우주항이라는 이유로 선행 태그/role 조건을 삭제하지 않는다. 구조가 겹쳐도 조건 호환은 별도다.|
|`cand_045fafa56b725614acbde563a5d0f294` 항해·관세·지도|원문은 해안 지도와 world survey 조건.|성간 항로망과 현재 해안 cartography를 의미 동등으로 바꾸지 않는다.|
|`carrier` 314개 일치|우편 배달원·운반 흐름 등 다양한 의미 포함.|우주 항모의 검색 coverage로 세지 않는다.|
|`cylinder` 10개 일치|리볼버 실린더와 스쿠버 통이 최초 이웃.|오닐 거주지 없음의 증거나 있음의 증거가 아니다. 스쿠버 후보의 수중 태그·장비 owner 조건을 유지한다.|
|`holographic` 7개 일치|색상 팔레트, 실제 광택 표면을 가진 휴대 화면 등.|공중 도식·극중 표시와 다른 의미다. 표면 광택 candidate의 color 효과를 장치 생성에 재사용하지 않는다.|
|`cassette` 12개 일치|음악 기록·카탈로그·무브랜드 매체와 dungeon-synth 태그 등.|미래 단말의 물리 매체와 독립적으로 검토한다. 아날로그 호러·우주 배경을 자동 부여하지 않는다.|

android·cyborg·symbiosis 등의 이웃도 [원문 스냅샷](existing-source-snapshots.json)에 있다. 여기서 후보가 발견됐다는 사실은 native source qualification이나 실제 제시를 증명하지 않는다. 신규 등록 전에는 literal 이웃뿐 아니라 전체 의미·기능·소유 관계를 탐색하고 same-role guard 우회가 없는지 확인해야 한다.
