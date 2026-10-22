# 실제 시험에서 발견한 검색 후속 과제

데이터 등록·인덱스 무결성 통과와 역할별 후보 노출은 별도다. 고정 버전
`1357d4e9171988e46ea9825a2ce4bed4afdd875ca4e29cb24c3f93c02ceaa608`의
실제 managed 검색에서 다음을 관찰했다. 엔진은 이 작업에서 변경하지 않았다.

| 원래 역할/질의 | 실제 분류·반환 | 판정 |
|---|---|---|
| B `object_structure`: “A hand-built weight-driven departure indicator … visible part connections …” | `hand`, `connections`를 근거로 `anatomical_connection`, 0건 | 기계의 제작 방식과 부품 연결을 해부학으로 해석한 오류 |
| C `object_structure`: “Human-scale clockwork public shade drive … connected rod …” | `scale`, `connected`를 근거로 `anatomical_connection`, 0건 | 규모를 뜻하는 수식어를 신체 부위로 해석한 오류 |
| B `contact_point`: 실제 인물의 손·팔과 기계 접점 | `anatomical_connection`, 0건 | 손·팔 표현은 실제로 존재함. 앞의 두 오분류와 구분하고 접촉 역할의 source witness 부족을 별도 조사 |

모두 BM25F와 local cosine은 각각 1회 실행됐다. 이후의
`primary_focus_source_witnesses` 투영에서 지원되는 source가 0개가 됐다.
원본 질의·쿼리별 전체 결과·해시를 각 run에 보존했다. 성공처럼 보이도록
질의를 바꾸거나 후보를 강제 삽입하거나 재추첨하지 않았다.
간결한 교차 검사는 `integration-evidence/managed-query-projection-summary.json`에 있다.

후속 구현은 문맥에서 실제 소유자와 관계가 성립하는지 확인해야 한다.
`hand-built`의 제작 방식, `human-scale`의 규모, 실제 손·팔 연결을 구별한다.
Clockpunk라는 라벨이나 특정 CID를 예외로 허용하는 우회는 사용하지 않는다.
기존 동물·인체·식물의 실제 해부학 연결 검색도 함께 보존해야 한다.

검증 순서는 다음과 같다.

1. 위 두 원본 기계 질의와 실제 손목·팔꿈치·잎자루 연결 질의를 동결된 회귀
   fixture로 만들고 현재 결과를 재현한다.
2. 역할의 실제 부품 소유자·연결 대상과 수식어의 의미를 검토하는 수정안을
   구현한다. 소스 자격·조건·효과·권한 검사는 유지한다.
3. 같은 질의와 같은 데이터에서 오분류가 사라지는지, 정당한 해부학 검색과
   일반 접촉 검색이 유지되는지 검증한다. 후보 개수 증가만으로 통과시키지 않는다.
4. 코드만 바뀐 봉인 successor를 만들고 원본 run을 보존한 새 revision에서
   managed 검색을 재검증한다. 이후 새 이미지 실험에서 연결 픽셀을 비교한다.

240개 일반 풀 개발 질의의 노출률은 이 역할 투영 결함을 검증하거나
해결하지 않는다. 이미지의 Clockpunk 인상 또한 검색 결함 해결의 증거가 아니다.
