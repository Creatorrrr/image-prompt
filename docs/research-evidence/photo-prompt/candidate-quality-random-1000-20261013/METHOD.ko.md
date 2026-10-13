# 무작위 후보 1,000개 의미 품질 검사 방법

현재 canonical corpus 18,250개 전체에서 단순 무작위 비복원 표본 1,000개를 고정한다. 시스템 난수로 만든 seed, 정렬한 canonical ID 모집단, 추출 순서·원본 및 파일 SHA를 보존한다. 종류·슬롯별 균등 quota나 부적합 표본 제외/재추출을 하지 않는다. diagnostic을 포함한 6종류가 모집단이며 이번 표본에는 실제로 visual option 692, profile 196, bundle 106, relationship mechanism 6개가 선택됐다.

완전한 원본은 samples.jsonl, 참조 후보는 REFERENCE-RECORDS.json, 실제 slot binding/catalog는 별도로 고정했다. 감사자는 모든 1,000개에서 한영 표현·정의·시각 단위·관계·효과·기존 binding을 읽고 개별 판정을 기록한다. compact view는 중복 문구를 줄인 1차 읽기 자료이며 전체 기술 계약을 모두 표시하지 않는다. 의심 사례는 deep card 또는 원본 전체를 추가로 읽는다. 공통 claim limit는 COMMON-LIMITS.json으로 한 번 읽고 반복 문구를 참조한다.

평가 축:

- meaning: clear(구체적이고 일관된 의미), weak(지나치게 추상적/메타 문구/관찰 단서 부족), distorted(정의·표현·관계가 서로 다른 의미), uncertain(전문 용어의 근거 등 추가 확인 필요).
- translation: consistent, missing_ko(ko 필드가 실질적인 한국어 설명을 제공하지 않음), mismatch, not_applicable. 고유명사와 번역 누락을 구분한다.
- slot: appropriate, broad(관련은 있지만 범위가 넓음), wrong, unassigned. Profile/bundle/mechanism의 기존 binding 부재는 현재 허용된 구조이며 자동 오태그로 판단하지 않는다. 빈 태그는 별도 커버리지로 집계한다.
- flags: owner/relation/direction/범위/guard 불일치, 반복·메타 누출, 단일 정지 화면에서 확인 불가능한 역사·물성·소리·정신 상태의 과잉 확정 등을 구분한다.

단순한 원자 후보는 길이가 짧아도 실제 사물·형태를 명료하게 나타내면 의미가 있다. 추상적인 장르·의도·절차는 유효한 컨텍스트일 수 있으며, 구체적 시각 정의와 동일 수준으로 간주하지 않는다. '선택한 관찰 가능한 변형'을 전체 장르·문화·제작법의 유일한 정의로 오해하지 않는다. 태그 이름과 provenance의 원래 슬롯을 의미 정답으로 사용하지 않는다.

이 검사는 Codex의 정성적 텍스트 감사다. 다른 독립 전문가의 합의 라벨, production retrieval 정밀도, 생성 이미지·native pixels 검증을 대신하지 않는다. 자동 문자열·구조 검사는 지원 근거이며 의미 통과 판정을 만들지 않는다. 후보 원본·binding·index/runtime는 수정하지 않으며 이미지·임베딩 API를 호출하지 않는다.
