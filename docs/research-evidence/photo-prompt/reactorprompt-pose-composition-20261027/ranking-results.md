# 포즈·구도 장문 질의와 패션 검색 순위 개선 — 2026-10-27

검증된 검색 릴리스를 기본 검색에 반영했다. Luna max 서브에이전트 5개가 장문 질의 원인, 패션 원문·특징, 검색 코드, 독립 의미 판정, 설치 검증을 나누어 수행했다.

## 결과

- 남아 있던 장문 질의 19개 중 10개가 상위 8개에 새로 진입했다. 이 19개의 타깃 중앙 순위는 **32 → 7**이다. 9개는 상위 8개 밖에 남아 있다.
- 원래 장면 질의 64개의 최종 판정은 **완전 일치 51 / 부분 일치 7 / 실패 2 / 관찰 불가 4**다. 동일 기준으로 재판정한 기준 설치본은 41 / 14 / 5 / 4였다. 기존 완전 일치 41개와 의미 질의 24개를 모두 유지했고, 기존 부분 일치가 실패로 떨어진 실제 회귀도 없었다.
- 패션 46개 질의의 140개 필수 특징은 **139개 유지, 1개 강화, 손실 0개**다. 순서가 같은 질의는 44/46이고 두 질의에서 후보 한 개씩 바뀌었다. 긴 검은 코트의 높은 칼라·젖은 어깨 하이라이트 근거가 강화됐다. 장신구 목록은 음료를 든 손에 착용한 증거로 인정하지 않았다.
- 새 대조 질의 24개는 기존 완전 일치 6개를 보존했다. 나머지 18개는 전체 자료에 완전한 같은-RID 근거가 없는 자료 공백이며, 잘못된 소유자·색상·각도 관계를 완전 일치로 인정한 경우는 0개다.

## 원인과 변경

기존 19개 타깃은 모두 검색 풀에 있었다. 17개는 BM25F와 임베딩 양쪽에서 상위 8개 밖에 있었고, 자연어 질문에는 기존 명시적 역할 헤더 경로가 적용되지 않았다. 조사·어형 차이, 질문과 원문의 표현 차이, 여러 속성·소유자의 관계가 합산 점수에 충분히 드러나지 않는 문제가 겹쳤다. 패션에서 밀린 기존 후보 13개도 삭제되지 않았고, 같은 해시로 9~12위에 남아 있었다. 포즈·구도 자료와의 전역 검색 경쟁이 순위 변동의 원인이었다.

검색은 기존 전체 양성 풀에서 BM25F 한 번과 로컬 cosine 한 번을 유지한다. 그 뒤 같은 주 원문 필드가 요청된 속성을 함께 뒷받침하는 질문에 제한된 순위 보정을 적용한다. 색상·수치는 질의와 원문에서 대상이 각각 연결되어야 한다. 중복 EN/KO/definition은 유효한 한 필드의 근거를 무효화하지 않고, 서로 다른 필드에 흩어진 사실은 하나의 완전한 근거로 합치지 않는다. 알 수 없는 대상과 처리하지 못하는 광택·무늬 조건은 가산하지 않는다.

발목 표현을 추가하고 서 있는 자세를 인접한 다리 명사에 잘못 연결하던 문제를 고쳤다. 거울 속 동일 인물과 머리/프레임 기울기를 묻는 열린 질문은 원문 직접 표현과 같은 선택 RID의 효과가 함께 확인될 때만 안정적으로 먼저 배치한다. 부정·인용·불확실성은 별도로 검증하며, 질문에 정답 값을 주입하지 않는다. 모든 보정은 발견용이고 native/semantic 승인 권한을 만들지 않는다. 영수증은 봉인된 가중치와 근거를 재생하고, 호출자가 바꾼 가중치를 거부한다.

## 장문 질의 19개

| 질의 | 이전 순위 | 반영 후 순위 | 상위 8개 진입 |
|---|---:|---:|---|
| P02 EN | 16 | 4 | 신규 진입 |
| P03 KO | 51 | 51 | 남음 |
| P04 KO | 184 | 2 | 신규 진입 |
| P06 KO | 30 | 30 | 남음 |
| P09 EN | 29 | 7 | 신규 진입 |
| P09 KO | 20 | 28 | 남음 |
| P11 EN | 52 | 6 | 신규 진입 |
| P13 KO | 176 | 3 | 신규 진입 |
| C02 EN | 32 | 2 | 신규 진입 |
| C02 KO | 243 | 2 | 신규 진입 |
| C03 EN | 96 | 100 | 남음 |
| C04 KO | 9 | 9 | 남음 |
| C05 KO | 10 | 1 | 신규 진입 |
| C08 KO | 26 | 26 | 남음 |
| C10 KO | 86 | 1 | 신규 진입 |
| C11 EN | 230 | 230 | 남음 |
| C11 KO | 10 | 10 | 남음 |
| C12 KO | 32 | 50 | 남음 |
| C14 KO | 207 | 5 | 신규 진입 |

타깃 순위가 내려간 3개도 표에 그대로 표시했다. 타깃 ID의 순위와 실제 의미 충족을 구분해 판정했다. 예를 들어 C12 KO는 타깃 순위가 내려갔지만 새 중앙 배치 근거로 부분 일치가 개선됐다. 이전 판정의 라벨 정정은 성과에 합산하지 않았다.

남은 9개는 P03 KO, P06 KO, P09 KO, C03 EN, C04 KO, C08 KO, C11 EN/KO, C12 KO다. 같은 원문 안에서 필요한 속성·소유자 관계를 충분히 확인하지 못하는 경우, 단일 속성 질문의 범위, 전역 순위 경쟁이 남아 있다. C11의 원래 루브릭에는 질문에 없는 85mm/f2와 앉은 눈높이 조건도 있다. 그 값을 질의에 덧붙여 점수를 올리지 않았다. 세부 근거와 후속 보완 대상은 [잔여 분석](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/analysis/longform/REMAINING-v5.md)에 정리했고, V6에서 추가로 해결한 C05/C10은 위 표에 반영했다.

검은 네일 폴리시의 직접 원문 근거는 없으며, 비대칭 홀터 넥과 목을 감싸는 구조도 각각의 기록에 나뉘어 있다. 이 자료 공백을 순위 개선이나 다른 색상·다른 착용 관계로 채워졌다고 판정하지 않았다.

## 검증과 적용 범위

- 실제 설치본 158개 질의(장면 64, 의미 24, 패션 46, 대조 24)와 158개 원문 순위 근거를 모두 재생했다. 원래 134개는 프로토타입과 후보 순서·원점수·전체 근거 trace까지 정확히 일치한다.
- 기존 및 추가 경계 테스트 **141/141** 통과. 실제 `search_material`과 `audit_packet`도 4개 질의, creativity=2, 고정 seed에서 통과했고 근거/정책 변조를 거부했다.
- 원문 파일 **1,155개**, H2 데이터 파일 **4,102개**, 모델 바인딩과 문서 벡터 바이트가 이전 설치본과 같다. 기존 질의 벡터를 그대로 재사용했다. 새 대조 질의 24개만 최초에 로컬 인코딩한 뒤 양쪽에 같은 벡터를 사용했다. 유료 API와 이미지 호출은 없었다.
- 기본 H2: `6f20b240e3b1c858b3893d37c4130cf80fc37108a2ec20c0362d6dba1ef8882d`
- 기본 Native: `75ebe2b9c088d4b1bce2b1018cd493251fa58fdb854a159a3a264031525e63f8`
- Native 코드 115개 중 검토한 5개 파일만 변경·추가했다. 기존 설치 세대와 CURRENT 포인터는 보존했다. Git HEAD와 staging은 유지했다.

설치 검증 도구의 오래된 가정(새 모듈 멤버, 추가된 정책, trace 버전)을 실제 봉인 코드 계약에 맞췄다. 도구 이전 버전, 실패 메타데이터·원래 매니페스트, 승인 핀 변경과 영수증의 권한 연결 정정은 runtime/archives 및 root-review에 보존했다. 실패한 COW 임시 복사본과 이번에 새로 생긴 18개 바이트코드 캐시는 정리했다. 실행 사실·코드·데이터는 그대로이고, 기본 전환은 모든 독립 검증 뒤 지원되는 원자적 CAS 설치기로 수행했다.

## 근거

- [최종 장면·의미·대조 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/evaluation-design/FINAL-INSTALLED-JUDGMENTS.md)
- [최종 패션 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/analysis/fashion/FINAL-INSTALLED-FASHION.md)
- [설치본 158개 평가 영수증](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/runtime/receipts/evaluate-explicit-result.json)
- [영수증 감사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/runtime/receipt-audit.json)
- [실제 검색 패킷 및 변조 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/runtime/smoke-material/6f20b240e3b1c858b3893d37c4130cf80fc37108a2ec20c0362d6dba1ef8882d/smoke-receipt.json)
- [기본 전환 영수증](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/runtime/default-activation.json)
- [변경 외 파일 보존 감사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/ranking-20261027/root-review/final-protected-files-audit.json)
