# 초현실 포스트휴먼 사이언스 판타지 데이터 반영 결과

2026년 10월 22일. 기존 리서치의 72개 가시 장면과 16개 문맥 구분을 운영 source에 등록하고, 검색 인덱스와 설치 릴리스를 갱신했다. 182개 키워드는 개념별 의미와 혼동 경계를 유지한 선택 경로로 연결했다. 장르 이름만으로 장면 묶음을 자동 적용하지 않는다.

## 반영 범위

| 항목 | 이번 추가 | 반영 후 전체 |
|---|---:|---:|
| 가시 후보 | 72 | 긍정 검색 CID 19,187 |
| 문맥 진단 후보 | 16 | source CID 19,471 |
| 선택적 슬롯 연결 | 144 | 13,644 |
| 키워드 의미 경로 | 182 | 이번 확장의 연구 레지스트리 |

16개 문맥 진단은 긍정 장면 검색에서 제외한다. 업로드와 자아 생존, 의식, 생식 메커니즘, 동의, 친족, 권리, 역사, 감각, 초자연적 효력 등을 외형과 구별한다. 단일 장면에서 확인할 수 없는 의미를 케이블·빛·유기적 형태로 대체하지 않는다.

72개 장면은 재료 전이, 이중 이미지와 반사 차이, 신체와 장치의 접점, 외부 인지 장치, 유기 건축, 의례적 기계, 규모와 내포 세계, 반복과 흔적, 합성 신체, 신체 경계, 친밀성과 돌봄, 포스트휴먼 일상의 12군이다. 한영 원문 전체와 재료·개수·부분·소유자·방향·접점·연속/분리 조건을 보존했다. 일부 관계만 보이거나 필요한 끝점이 가려진 장면은 원 후보 전체의 구현으로 통과시키지 않는다.

| 운영 파일 | 역할 |
|---|---|
| [시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_surreal_posthuman_science_fantasy_semantics_20261022.json) | 182개 키워드 경로, 88개 의미 기록, 문맥 경계와 원전 열람 범위 |
| [후보 source](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_surreal_posthuman_science_fantasy_20261022.json) | 가시 장면 72개와 문맥 진단 16개 |
| [슬롯 연결](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_surreal_posthuman_science_fantasy_bindings_20261022.json) | 기존 catalog 역할을 이용한 선택적 연결 144개 |
| [사용과 판정 지침](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/surreal-posthuman-science-fantasy-semantics.md) | 전체 의미 보존, 추론 한계와 실제 픽셀 판정 |

원전 참조는 개별 개념 자료와 가족군 배경을 구분한다. 182개 정의가 모두 독립적인 원전 검증을 마쳤다는 뜻은 아니다. 구체적인 장면은 이번에 저술한 선택안이며 인용 작품의 정본 디자인이 아니다. 전체 corpus에서 의미상 완전히 새로운 장면이라는 주장도 하지 않는다.

## 보존과 설치

반영 직전 후보 19,383개, 슬롯 연결 13,500개, catalog와 정책을 보존했다. 기존 36개 이웃 후보의 전체 source도 현재 값과 다시 대조했다. source 원문 검증과 인덱스 검증은 통과했다. 작업 전부터 수정돼 있던 파일은 그대로 유지하고, 기존 파일 중 이번에 바꾼 것은 module manifest, 검색 manifest, 검색 기본 버전 설정, maintenance 안내의 추가 문단이다.

로컬 임베딩으로 신규 가시 문서 72개를 만들고 기존 문서 벡터 19,117개를 그대로 재사용했다. 검색 코드와 임베딩 공간은 바꾸지 않았다. Gemini 호출은 없었다. 검증한 릴리스를 설치한 다음 기본 검색 설정으로 선택했다. 기존 `CURRENT.json` 포인터에는 쓰지 않았다.

| 버전 증거 | 값 |
|---|---|
| H-F2 generation | `0df1fb14b8c36b9580c218e0e931039dc695593c3f5d9cdc30f61d6c8ede42b9` |
| native generation | `19795ff984fbc3d90e804d7a74b8ca2d138defa2134be76a64858e6c9d669c9f` |
| 코드 SHA256 | `96b67dedcfea019115cd46c6542287d7102e46cd12a486f1e817d79f3c634d0e` |
| 작성 시점 SKILL SHA256 | `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35` |

설치 검증은 source와 검색 자료의 일관성을 뜻한다. 새 후보의 native 의미 자격은 `not_qualified`이며, 메타데이터나 슬롯 연결은 기존 요청의 소유권·조건을 바꾸는 권한을 주지 않는다. 현재 H-F2 흐름에서는 core를 독립적으로 확정한 뒤 후보별 전체 source를 검토하고 `inspiration_only` 또는 `skip`으로 판단한다.

## 반영 전후 검색

계획한 112사례 중 18사례를 골라 한영 36질의를 반영 전후에 각각 실행했다. 전체 pool 검색 총 72회다. 개발용 12사례의 한영 24질의에서는 의도한 새 후보가 모두 상위 8개에 들었다. 원문에서 만든 개발 질의이므로 독립 holdout 정확도나 품질 향상을 뜻하지 않는다.

경계·일반·비가시 질의 12개 중 6개에서 새 후보가 상위 8개에 노출됐다. 특히 평범한 다실의 주전자와 컵을 묻는 질의에 물줄기가 사슬로 전환되는 후보 A03이 영어 1위, 한국어 7위로 나왔다. 일반 장면에는 이 변환이 맞지 않으므로 채택하지 않아야 한다. 새 후보가 높은 순위에 있다는 사실을 적합성으로 간주할 수 없는 구체적인 사례다.

창백한 인공인물 초상 질의의 두 인공 몸/두 초상 카드, 기억 장치 질의의 종과 케이블 등도 전체 소유자·개수·장치 의미를 비교해 기본 채택하지 않았다. 비성적 손 접촉은 성적 관계나 동의의 증거로 해석하지 않았다. 이 검토는 검색 후보의 의미 검토이며 해당 12질의의 이미지 생성 검증은 아니다.

| 검색 증거 | 위치 |
|---|---|
| 전후 질의와 상위 8개, 목표 순위 | [retrieval qualification](/Users/chasoik/Projects/image-prompt/generated/maintenance/surreal-posthuman-science-fantasy-20261022/retrieval-qualification.json) |
| 경계 질의의 원문과 조건 | [full source evidence](/Users/chasoik/Projects/image-prompt/generated/maintenance/surreal-posthuman-science-fantasy-20261022/control-full-source-review-input.json) |
| 개별 의미 판정과 검색 잡음 | [control semantic review](/Users/chasoik/Projects/image-prompt/generated/maintenance/surreal-posthuman-science-fantasy-20261022/control-semantic-review.json) |
| 보존 검사와 설치 영수증 | [integration evidence](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/integration-evidence) |

나머지 94사례와 독립 holdout은 실행하지 않았다. 사용자 요청의 세 독립 이미지 테스트는 별도 결과에서 실제 후보 노출, 최종 프롬프트, 참조 전달, 저장한 원본 픽셀을 구분해 판정한다. 커밋과 푸시는 수행하지 않았다.
