# 공통 후보풀 전환 1단계

origin/main `6baa89ab0781401c5565cbdbbffe30153979b317`까지 pull/fast-forward 했다. 원격의 EMT·토양 맥락과 기존 로컬 원본·private extension을 함께 적재했다. 파생 semantic index는 원본과 전체 text가 일치하는 기존 벡터 12,056개를 골라 재생성했으며 embedding API 호출은 0건이다.

112개 슬롯 12,020개 레코드, semantic 문서 12,056개, visual profile 3,834개, bundle 2,204개를 조사했다. 전체 source hash·레코드별 실효 의미·적용 조건·검색 text hash와 기존 실행 의존 목록을 저장했다. 원본 전체와 벡터는 운영 경로 밖의 SHA 기록으로 보관했다.

동결된 기존 자연 요청 20개의 입력 바이트와 core binding을 검증하고 production API로 lexical baseline pack 20개를 생성했다. 새 discovery maintenance 요청 12개도 migration 비교 전에 고정했다. 이 사례는 blind 또는 이미지 품질 검증이 아니다.

원격 EMT 맥락 검사 및 기존 core retrieval 검사 9개가 통과했다(115.566초). 인덱스 전체의 source/text addressability도 통과했다. 새 hybrid 연결, 의미상 중복 병합, migration은 아직 실행하지 않았다.

다음 단계는 새 스키마·다대다 연결·무결성 검증기 도입이다.
