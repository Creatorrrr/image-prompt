# 호러 시각 의미·후보팩 연구 패키지

2026-10-06 KST. [호러 요소 조사](chatgpt-conversation://6ac3d144-ccfc-83ee-9e05-2f1a96060604)의 17개 절을 모두 확인하여 표 249행과 본문 1행을 대조했다. 연구용 초안이며 활성 데이터에 적용하지 않았다.

- [상세 리서치](RESEARCH.md): 기존 데이터, 새 관계와 혼동 경계, 민속·매체·신체·욕망·공간·색·조명·소리의 반영 범위.
- [파일별 반영 계획](IMPLEMENTATION-PLAN.md): 우선순위, 현재 schema, source manifest, index·검색·후보팩·원본 이미지 검증.
- [의미 카드 250개](SEMANTIC-CARDS.md), [입력 키워드](SEED-INVENTORY.json), [전체 대응](SEED-COVERAGE.json).
- [후보 초안 161개](CANDIDATE-DRAFTS.json): 시각 실현 155개와 문화·판본 근거 보류 6개. 현재 채택 준비 완료는 0개.
- [선택형 묶음 12개](BUNDLE-DRAFTS.json), [팔레트와 색 소유자 12개](PALETTE-DRAFTS.json), [기존 인접 ID 21개와 원본 배치](RUNTIME-MAPPING.json).
- [출처 35개와 각각의 확인 수준](SOURCES.md). 문헌 일부/초록/메타데이터/조회 실패를 구분하며, 전체 키워드의 사실 검증으로 집계하지 않는다.
- [v2 component compiler 예시 3개](PROFILE-PROTOTYPES.json), [개발 검증 728건 + 통제 14건의 계획](REGRESSION-PLAN.json), [픽셀 검증 22개 그룹의 계획](PIXEL-QUALIFICATION-PLAN.json).
- [구조·compiler 투영·원본 보존 검증](VALIDATION.json), [연구 기준 원본 스냅샷](CHECKOUT-SNAPSHOT.json), [수치와 미실행 상태](RESEARCH-STATS.json).
- [연구 중 기존 파일 7개 변경 감지](SOURCE-DRIFT-NOTE.md): 실제 채택 전에 현재 authorial·composition·audit 계약을 다시 대조한다. authored assets와 인덱스는 같은 해시였다.

`build_research.py`는 CARD-INPUT 두 파일에서 연구 산출물을 재생성한다. `validate_research.py`는 참조 연결, 실제 기존 ID, source-only metadata 경계, compiler 투영과 필수 component 미연결 거절, 원본 SHA-256을 확인한다.

계획된 742건의 검증과 22개 이미지 그룹은 실행 결과가 아니다. 실제 등록·인덱스 재생성·후보팩 실행·이미지 생성은 수행하지 않았다. 250개 카드를 한번에 runtime에 복사하지 말고 반영 계획의 의미 검토·배치·완료 조건을 적용한다.
