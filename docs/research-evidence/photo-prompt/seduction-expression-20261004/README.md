# 유혹적 표현 요소 조사 패키지

참조 대화의 120개 항목을 기반으로 시각 의미와 후보팩 데이터를 보강하기 위한 상세 연구와 반영 계획을 작성했다. 시작 2026-10-04 / 완료 2026-10-05 KST.

먼저 [리서치 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/RESEARCH.md)를 읽고, 구현에는 [반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/IMPLEMENTATION-PLAN.md)과 [120항목 상세 대응표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/CATALOGUE.md)를 사용한다.

| 구분 | 수량 | 의미 |
|---|---:|---|
| 참조 항목 / 독립 출처 | 120 / 39 | 원 대화 전체와 출처 범위 확인 |
| 해석어 / 명시적 시간 항목 | 15 / 9 | 서로 겹치지 않는 연구 분류;범용 형태 강제와 정지 시간 추정 방지 |
| 대응한 기존 후보 / 프로필 | 157 / 17 | 실제 ID 존재 확인;pack 노출/선택 성공 수 아님 |
| 기존 후보 보강 / 신규 제안 | 22 / 14 | 검토 후 설치 가능한 필드 초안;신규는 중복 검토 필요 |
| 기존 프로필 보강 / 신규 제안 | 14 / 12 | 정확한 형태/가시성 초안;문맥·target 매핑 검토 필요 |
| 선택형 묶음 | 10 | broad mood의 필수 recipe 아님 |
| 항목 검토 프로브 / 경계 회귀 | 120 / 45 | 테스트 계획;실행된 테스트 수 아님 |
| 원본 픽셀 장면군 | 8 | 계획;생성 이미지 수 아님 |

현재 작성 자산의 조사 시점 목록은 후보 9,949개/프로필 1,774개다. 원문 문자열 프로브 히트 71/120은 의미 커버리지나 검색 성공률이 아니다.

**활성 자산·코드·인덱스를 수정하지 않았고 이미지도 생성하지 않았다.** 패키지 구조와 참조 연결은 `validate_research_package.py`로 검사하며 결과는 [VALIDATION.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/VALIDATION.json)에 기록한다. 구조 PASS는 런타임이나 픽셀 PASS가 아니다.

2026-10-05 검사는 PASS다. 현재 계약의 검사기로 후보 초안 36건을 검사하고, 프로필 template 12건과 선택 묶음 10건을 메모리에서 투영/컴파일했다. 조사 입력 88개 파일의 해시는 모두 그대로였다. 실제 core 바인딩·검색/팩·선택·이미지 검증은 이후 반영 단계의 조건으로 남아 있다.

## 파일 안내

- `REFERENCE-KEYWORDS.json`: 원 대화 번호·용어·뜻·분해 예시와 확보 방법.
- `TERM-SPECS.psv`, `TERM-RESEARCH.json`, `CATALOGUE.md`: 사람이 편집하는 원본과 구조화/가독성 출력.
- `SOURCES.json`, `SOURCES.md`: 39개 출처의 링크·지지 주장·한계.
- `SOURCE-SNAPSHOT.json`, `CURRENT-DATA-AUDIT.json`, `CURRENT-INVENTORY.json`: 조사 시점 입력 해시·문자 프로브·발견 기록.
- `CANDIDATE-DRAFTS.json`, `PROFILE-DRAFTS.json`, `BUNDLE-DRAFTS.json`: 설치되지 않은 연구 초안. wrapper를 runtime loader에 등록하지 않는다.
- `REGRESSION-PLAN.json`, `PIXEL-QUALIFICATION-PLAN.json`: 의미/계약과 이미지 검증 계획.
- `PACKAGE-SUMMARY.json`, `VALIDATION.json`: 수량과 패키지 검증 결과.
- `audit_current_data.py`: 입력/인벤토리 조사. 재실행하면 조사 스냅샷을 갱신하므로 과거 증거를 보존하려면 새 폴더를 사용한다.
- `build_research_package.py`: 기존 연구 원본에서 JSON과 상세 대응표/출처 장부를 생성.
- `validate_research_package.py`: 패키지 구조·ID·source·초안·계획·입력 변경 상태 검사.

이 폴더의 JSON은 모두 연구 자료다. 출처 의미, 작성 데이터, 검색 적격성, pack 노출, 선택, 프롬프트/런타임, 원본 픽셀, 사용자 수용을 분리한다.
