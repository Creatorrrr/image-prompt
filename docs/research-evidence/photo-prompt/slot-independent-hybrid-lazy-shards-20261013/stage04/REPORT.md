# 4단계

metadata만 적재하는 reader와 immutable candidate repository, 64MiB 이하 LRU cache를 구현했다. 초기 vector/payload/posting read는 모두 0건이다. 실제 cold 초기화 1.896초, peak RSS 762,609,664바이트로 측정했다. 이는 아직 공개 workflow 전환 전의 reader 측정이다.

기존 동결 요청 20건에서 전체 원본과 compact guard projection의 eligible 후보·binding·frozen contract가 정확히 일치했다. 첫 비교의 차이는 JSON canonical 순서에 따른 binding 배열 순서였으며 양쪽에서 ID 정렬을 명시하여 결정성을 고정했다.

metadata·본문 SHA 검증, read-only vector, cache 상한/eviction, 같은 mtime 변조 및 아직 읽지 않은 필수 shard 누락 거부를 검증했다.
