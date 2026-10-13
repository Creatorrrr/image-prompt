# 1단계 검증 기준

112개 슬롯 × 2개 언어 검사 행렬과 전체 스캔 oracle을 준비했다. 기존 태그 수를 의미 품질 정답으로 사용하지 않는다. bilingual focus는 2단계에서 중립 정의로 확정한다.

현재 전체 적재 경로: `photo_global_index.load`, `photo_shared_views.assemble`, `photo_global_retrieval.eligible`, `capture_sources`, `_verify_generation`, `load_generation(independent_audit=True)`, `audit_global_retrieval.audit`, `dictionary_hash`. 새 runtime에서 본문 접근과 source SHA 바인딩을 분리해야 한다.

BASELINE.json은 실제 원본/인덱스의 cold 적재 측정이다. GATES.json은 신규 성능 측정 전 고정한 목표다. 의미 품질과 실제 provider 검증은 후속 단계에서 별도로 수행한다.
