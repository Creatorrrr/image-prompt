# 4단계 — 공통 인덱스와 실제 검색어 임베딩

전역 positive 문서·벡터 18,186개를 신규 source hash에 연결했다. diagnostic 64개는 optional positive 검색에서 제외한다. 후보별 문서가 하나이므로 연결 추가가 문서 수·IDF·cosine/RRF 투표를 늘리지 않는다. 슬롯명·유형별 routing 문구는 새 visual text recipe에 넣지 않는다.

시각 프로필 3,834개는 대응 identity·전체 text·Gemini provider/model·768차원·기존 positive visual profile recipe/v2의 동일성을 검증한 뒤 재사용했다. 다른 14,352개는 Gemini gemini-embedding-2를 실제 호출해 새 벡터를 만들었다. source/ID/recipe/text/차원/finite/nonzero 검증과 신규 shard 전체 checksum 검사를 통과했다. 과거 ID 대응표는 외부 일회성 seed 생성에서만 읽었으며 신규 builder는 native ID seed/index와 실제 호출 기록만 읽는다.

3개 동결 core의 query text를 실제 provider로 생성하고 core/control hash·query recipe·space·vector checksum과 HTTP 실행 trace를 저장했다. 별도 private cache가 보관하며 immutable source에는 쓰지 않는다. 동일 요청 warm cache는 원래 provider 증거를 재사용한다. 실패는 명시적으로 실패하며 lexical fallback을 hybrid로 표시하지 않는다.

최종 상태: unique vector provider 결과 14,352개, 미완성 벡터 0개. 초기 connection/transport 결과를 확인할 수 없던 attempt 15개는 원본 증거를 보존하고 명시적 유지보수 재개로 복구했다. 원격 처리·과금 여부가 불명인 최초 attempt는 성공으로 세지 않는다. 최종 index의 성공 벡터는 HTTP 200 결과로 검증한다. 이후 provider는 연결 자체의 실패와 전송 결과 불명을 구분한다.

구조·변조 검사 26개 통과. 실제 세 query에서 BM25F와 정확한 full-corpus cosine을 실행했으며 초기 lexical index 생성 및 세 query 순위 합계는 21.632초다. 이는 공개 CLI p95나 자연 요청 의미 품질 수치가 아니다. 공개 CLI 연결·품질·runtime 감사는 다음 단계에서 검증한다.
