# 3단계

18,186개 원본 벡터를 정밀도 손실 없이 공간 shard 1,024개로 배치했다. canonical payload 286개, 전역 BM25F posting block 373개, routing node 2,047개를 생성했다. metadata 압축 크기는 29,224,830바이트다. 신규 provider 호출은 0건이다.

모든 원본 row, 단일 locator, 전체 vector coverage, 모든 node의 포함 경계, 전체 BM25F 통계 및 term TF를 원본에서 재계산해 검증했다. 새 manifest는 staging 상태이며 기존 운영 manifest를 변경하지 않았다.
