# 5단계

전역 통계 기반 posting BM25F, 원본 cosine top-K 및 전체 영역을 닫는 읽기 생략 증명을 구현했다. 초기 spherical cap은 실제 데이터에서 모든 shard를 읽어 개선했다. 최종 routing은 4-bit 좌표 표현과 모든 원본에서 검증한 L2 오차 상한을 사용한다. 근사 값은 읽기 선택에만 쓰고 최종 점수·순위는 원본 벡터로 계산한다.

원본 vector 저장은 값이 정확히 복원되는 scaled-int32 또는 float64 codec을 사용한다. 18,186개 값의 손실 검증 0건, 재임베딩 0건이다. 최종 vector shard 3,850개, metadata 22,167,993바이트다.

실제 저장된 문서 벡터를 query로 사용한 8개 기하/점수 검사에서 두 lane 순위 차이 0건, vector 읽기 median 감소 49.33%다. 이 검사는 새 슬롯 provider query의 의미 품질 증거가 아니다. 짧은 query의 cold latency는 전체 적재 oracle보다 느린 사례가 있어 8단계의 실제 슬롯 workload에서 분리 측정·개선한다.
