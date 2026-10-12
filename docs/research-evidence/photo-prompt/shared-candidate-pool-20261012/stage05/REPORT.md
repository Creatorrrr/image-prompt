# 5단계 — 공개 전역 hybrid와 native v7 팩

공개 `generate_photo_prompt.py`의 기본값은 `hybrid_required`다. immutable generation의 전체 positive 후보 중 subject/context/exclusion guard를 통과한 집합에 전역 BM25F·exact cosine·RRF를 한 번 적용한다. 요청 슬롯/태그 필터를 적용하지 않는다. 명시적 `keyword_only`는 diagnostic이며 embedding lane은 not_requested로 기록한다.

12,020개 연결의 기존 주체 적용 조건과 guard 역할을 conditions에 명시했다. 태그만 바꾸어도 주체/맥락 guard는 바뀌지 않는다. per-role limit 4/2와 전역 unique 64를 유지하며 한 후보의 복수 역할이 lexical 문서나 cosine/RRF 투표를 늘리지 않는다. source 변경 후 인덱스를 새 hash에 연결할 때 모든 18,186개 native identity/full text/recipe/vector가 일치하여 API 호출 0건으로 재사용했다.

v7의 candidate_pool이 원본 payload를 한 번 보관하고 role_views·성인 표현·시각 프로필·묶음·관계 뷰는 native ID를 참조한다. 무태그 후보도 풀에 포함한다. 효과가 미확정인 발견은 review_required이며 retrieval이 자동 채택/새 requester 의무를 만들지 않는다. query vector는 public pack에 넣지 않고 private v2 receipt에 저장한다. native generation/cache는 별도 namespace를 사용한다.

공개 CLI로 동결 요청 3개를 실행했다. 모두 BM25F/vector lane이 executed이고 unique 64를 준수한다. 파란 컵 사례는 역할 뷰 16개, 역할 노출 28개, 무태그 노출 36개다. 세 쿼리는 4단계의 실제 provider 결과를 hash 검증해 재사용했다. native composer overview 및 원본과의 재검증도 통과했다. 다대다·무태그·태그 이동·guard 우회 거부·keyword-only 구분 등 검사 32개 통과.

표본 standalone CLI 시간은 cold 52.795초, 같은 generation의 후속 프로세스 30.708/28.909초다. 이 시점의 latency/meaning 품질 qualification은 아직 완료하지 않았다. composition·receipt 독립 재계산/변조 감사는 6단계, 전체 평가·성능은 7단계에서 검증한다. 구 원본과 미사용 reader 제거는 9단계에 남아 있다.
