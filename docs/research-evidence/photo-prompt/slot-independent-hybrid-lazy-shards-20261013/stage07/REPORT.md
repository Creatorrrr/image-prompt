# 7단계

native candidate pack V8, generation/receipt/current V3로 교체하고 슬롯 query set·역할 제안·source binding을 연결했다. 공개 prepare/compose/view/API 전 단계의 계약을 갱신했다.

게시 시 source/전체 layout을 검증하고 generation을 독립 파일로 복사한다. 요청은 게시 때 봉인한 filesystem identity가 그대로인 자료의 SHA를 재사용하고 변한 자료만 다시 검증한다. metadata와 필요한 shard만 적재하며 요청에 generation 자동 생성이나 전체 BM25 cache 재생성이 없다. 게시 전 새 source는 차단된다.

운영 감사는 posting으로 점수를 재계산하고 cosine의 실제 방문 영역 및 모든 생략 영역의 오차 경계를 확인한다. fresh worker의 원본 issued receipt에서 후보팩 전체가 정확히 재생된다. 변조·same-mtime 변경·미게시 source·pending epoch·게시 경쟁 및 구 pack 거부를 검증했다. 의미 품질과 실제 provider 증거는 다음 단계다.
