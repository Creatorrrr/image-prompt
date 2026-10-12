# 공통 후보풀 전환 2단계

후보 원본·관리 슬롯 태그·다대다 역할 연결·정책을 별도 native schema로 구현했다. 전역 ID는 슬롯과 분리되며, 실제 파일의 소유권도 전역 ID별로 유일하다. source manifest는 새 스키마만 읽으며 구 slots 트리를 변환하거나 지원하지 않는다.

다대다 연결·무태그 후보·태그 변경 시 identity 보존·외부 참조·중복 소유·조건을 통한 ID/효과 덮어쓰기·잘못된 effect 차원·canonical cycle·NaN/중복 JSON key·경로 이탈·구 구조 거부에 대한 의미 있는 검사 14개가 통과했다. 원본 코드 import는 candidate 데이터나 네트워크에 접근하지 않는다.

기존 runtime 동작은 아직 전환하지 않았고, 신규 corpus와 ID에 실제 데이터를 넣는 migration은 다음 단계다.
