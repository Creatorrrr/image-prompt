# 2단계 검증

18,250개 canonical ID와 12,020개 기존 연결을 유지했다. 6,674개 후보의 필수 조건을 본문에서 canonical conditions로 분리했고, 후보와 동일했던 연결 효과 사본 12,020개를 제거했다. 역할별 subject policy는 연결에서 보존한다. 효과는 후보 한 곳에만 존재한다.

필수 조건은 검색 대상 자격을 먼저 검사한다. 고정 동작을 정확히 설명하는 후보의 발견과 그 동작을 수정할 자격을 구별한다. 역할 제시는 모든 canonical 효과를 열린 차원·속성 잠금과 다시 대조한다. 같은 역할의 선언 조건 실패를 무연결 제안으로 우회하지 않는다. 다른 역할의 조건을 잘못 상속하지 않는다.

모든 슬롯에 의미 경계·소유 범위·속성 경로·영한 설명·core focus·우선순위를 부여했다. 실제 소유 속성과 의미 보조 근거가 일치해야 eligible이고, 근거가 불명확하면 review_required다. 차원 일치·태그·단어 하나만으로 의미 승인하지 않는다. 이전 native V1 원본, V1 질의 context, V8 팩은 운영 경로에서 거절한다.

- 관련 계약·검색 테스트 71개 통과, 통합 테스트 31개 통과.
- 확대 실행 358개는 초기 10 failure / 3 error였다. 필수 조건의 옛 위치를 읽던 2개, 고정 동작의 발견/변경 구별을 검증하던 8 subcase, 빈 optional pool을 가정하지 못한 3개를 수정했다. 실패 로그를 보존했다.
- 수정 후 관련 회귀 109개와 source/lock/maintenance 추가 회귀 5개가 통과했다. 전체 확대 테스트 재실행은 최종 3단계 통합에서 수행한다. 전체 358개가 통과했다고 보고하지 않는다.
- source/index 사전 검증 통과. 모든 18,186개 positive 본문·recipe가 동일하여 벡터 18,186개를 재사용했고 문서 embedding provider 호출은 0개였다. payload·posting·float64 vector closure 및 native publication을 검증했다.
- 실제 영한 질의 8개에 대해 BM25F·exact cosine·RRF 전체 스캔 일치, skip certificate, 초기 payload/posting/vector 읽기 0, 64MiB cache·64 descriptor 한계를 검증했다. 팩 영수증 재검산과 optional 후보를 거절하는 합성 감사도 통과했다. 실제 숫자·generation·provider/cache 경위는 STAGE02-HYBRID-VERIFICATION.json에 기록했다.

이 단계의 운영 슬롯 ID는 아직 112개다. 이름 변경·통합·분해 및 기존 관계 이관은 다음 3단계에서 수행한다. 무결성·회귀·검색 순위 검증이며 전체 후보 의미 심사나 생성 이미지 품질 증거가 아니다.
