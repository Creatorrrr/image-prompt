# 6단계

슬롯별 전체 positive 공간의 BM25F+embedding+RRF 실행을 구현했다. 모든 독립 순위를 얻은 후 요청 unique 예산과 슬롯 표시 예산을 공정하게 배분한다. 태그 없는 후보와 다른 태그 후보가 request-local 역할 제안으로 반환된다.

후속 조회는 두 lane prefix를 확장하고 RRF를 재결합한다. 비활성·차단·결과 없음·예산 제외를 구분하며 explicit 지정은 등록된 모든 슬롯을 검색할 수 있다. 차단 슬롯도 explicit 검색 시 두 lane을 실행하고 채택을 차단한다. 원본 payload는 채택 가능한 표시 후보에만 materialize하며 guard/rejection 검사는 metadata에서 한다.

슬롯 순서 변경의 동일 결과, 전체 unique 예산이 검색 실행을 생략하지 않는 것, 무태그/다른 태그 제안, 필수 query set 거부 및 명시적 keyword 진단을 검증했다. 합성 벡터 단위 검증이며 공개 workflow 통합과 실제 provider 검증은 7–8단계다.
