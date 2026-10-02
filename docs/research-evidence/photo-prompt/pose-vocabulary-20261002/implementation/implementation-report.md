# 포즈 조사 데이터 반영

2026-10-02. [원래 조사와 반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/README.md)에 대한 후속 구현이다. 현재의 core 기반 V6 후보 검색 계약을 사용하며, 과거 preset·recipe·sampler 경로를 복원하지 않았다.

## 반영 범위

원래 236개 관찰 정의 중 153개를 새 선택 후보로 추가하고, 19개는 기존 후보에 동등한 표현과 사용 맥락만 덧붙였다. 변형·동작 단계·개별 출처·참고 픽셀 확인이 남은 64개는 보류했다. 독립 에이전트가 먼저 고정한 테스트 자세를 검토하는 과정에서 좌면 지지와 발레의 명시적 변형 5개를 추가로 검토했으므로, 최종 추가량은 **158개 후보, 34개 시각 의미 프로필, 34개 선택 번들**이다.

| 기존 슬롯 | 새 후보 |
|---|---:|
| body_pose | 51 |
| contact_point | 33 |
| body_orientation | 17 |
| hand_pose | 22 |
| gaze_engagement | 5 |
| expression | 9 |
| action | 8 |
| relational_action | 13 |

현재 런타임에는 112개 슬롯의 후보 9,590개, 시각 의미 프로필 1,419개, 의미 검색 문서 9,626개가 있다. 두 검색 인덱스를 재구축하고 전체 live loader에서 출처·스키마·해시 정합성을 확인했다. 이전 인덱스 세대와 다른 작업의 변경 사항은 보존했다.

새 런타임 파일은 [선택 후보 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json)과 [시각 의미 프로필 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_pose_vocabulary.json)이다. 생성기에는 두 확장의 등록만 추가했으며, 후보 수 상한이나 선택 정책을 바꾸지 않았다.

## 의미와 소유권

각 후보는 관찰 가능한 구성요소, 몸·파트너·접촉 대상의 소유자, 영향 차원과 속성 범위를 가진다. 사람 수, 의상, 정체성, 표정, 프레이밍을 자세 단어에서 자동으로 만들어 내지 않는다. 짝이 필요한 항목에는 실제 복수 주체 맥락의 guard를 둔다. 기존 19개 후보의 명칭·구성요소·효과·guard는 유지했다.

프로필의 필수 구성요소는 원본 이미지의 all-of 게이트로 투영된다. 이름이나 번들만 검색됐다는 이유로 활성화하지 않으며, 명시적 자세 표현 또는 자율 opt-in이 필요하다. bare 별칭·동음이의어·부정 표현은 자세를 강제하지 않는다. 부분 충족이나 필요한 부위의 가림은 성공으로 집계하지 않는다. 지지·균형은 보이는 배열을 평가하며 실제 힘을 측정한 것으로 해석하지 않는다.

좌면의 교차 정강이와 손바닥 지지는 바닥 자세의 전역 동의어가 아닌 별도 변형이다. 발레는 양발이 바닥에 닿는 2번 위치, 얕은 demi-plié, 머리 위 둥근 팔 배열만 구체화했다. [Pittsburgh Ballet Theatre의 자세 설명](https://pbt.org/community/resources-audience-members/ballet-101/basic-ballet-positions/)과 연결된 발·팔 도판을 직접 확인했고, [Ballet Jörgen의 용어 설명](https://www.jorgendance.ca/ballet-vocabulary/ballet-terms-p/)을 함께 사용했다. 학교별 번호 차이나 broad plié·port de bras 전체의 자격을 주장하지 않는다.

[처리 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/implementation-disposition-ledger.json), [추가 변형](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/refined-variants.json), [추가 출처](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/supplemental-sources.json)에 근거·반례·보류 이유를 보존했다. maintenance 기록은 런타임 의미 입력에서 분리했다. 렌더 결과는 별도 [독립 이미지 테스트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/README.md)에서 기록하며 원래 연구·출처·과거 평가 자료는 다시 생성하지 않았다.

## 검증과 후속 이미지 테스트

포즈 계약 테스트 8개가 통과했다. 실제 core 검색, 후보 감사의 재계산, 소유자·속성 lock 범위, 기존 의미 보존, 파트너 guard, 부정/동음이의/변형 경계, 프로필의 원본 all-of 투영을 확인했다. dictionary validator와 시각 프로필 인덱스 검사도 통과했다.

세 에이전트는 후보 접근 전에 서로 다른 난수 seed, 컨셉, baseline, core, 신체 배열 검토, 혼동 오답과 픽셀 기준을 고정했다. 이후 같은 소스 manifest로 각각 V6 팩을 한 번씩 만들고, 첨부 이미지를 얼굴·머리의 보이는 외관 참고로 사용한다. 새 장면의 주체는 성인으로 명시했다. 실제 정체성·나이·생체적 유사성·성격을 추론하지 않는다.

첫 팩에서는 좌면 교차 정강이, 반무릎, 발레 하체 2개가 노출됐고, 좌면 손바닥 지지·발레 팔·V 사인은 노출되지 않았다. 새 프로필 34개 중 이번 세 팩에서 opt-in으로 노출된 프로필은 없다. 따라서 해당 baseline 자세의 픽셀이 성공하더라도 새 후보 또는 프로필의 채택 성공으로 바꾸어 세지 않는다. 세 사례는 고정한 독립 저작과 실제 반영을 점검하는 통합 사례이며, 임의 모집단 holdout이나 반영 전후 인과 비교가 아니다.

전체 회귀는 115개 모듈의 **1,148개 테스트를 빠짐없이 실행**했다. 첫 완전 실행에서 과거 전체 inventory 비교 5건과 다른 skill의 현재 photo fingerprint 3건이 실패했다. 과거 fixture의 기존 bundle ID/순서/의미와 원래 source hash는 그대로 보호하고, 이후의 선택 번들·동등 맥락 overlay를 분리해 비교하도록 바꿨다. 다른 skill의 live photo boundary는 동일한 고정 core·64개 후보 ID·negative를 확인한 뒤 pack fingerprint 두 필드만 갱신했다. 과거 V1–V4 자료와 픽셀 게이트를 고쳐 통과시키지 않았다. 관련 최종 **62개 테스트가 모두 통과**했으며 미해결 실패는 없다. 최초 전체 실행 로그와 실패 ID도 보존했다. 두 번째 전체 실행을 했다고 주장하지 않는다.

[최종 검증 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/final-verification.json)에 원래 실패와 각 재실행의 정확한 ID/로그/해시가 있다. [live boundary 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/photo-boundary-refresh.json)은 기존 후보 inventory·baseline·negative가 동일함을 보존했다. 불필요한 소스 재작성·preset 복구·후보 상한 확대는 하지 않았다.

원본 3장에서는 반영 대상 **3/7 PASS**, 일반 지식 OK 대조 **1/1 PASS**, 복합 장면 **0/3 PASS**다. 실제 새 후보 노출·채택은 **4/7**, 새 opt-in 프로필 직접 채택은 **0개**다. 작성·runtime 감사 3/3 PASS와 원본 픽셀 결과를 구분했다. 소스 110개와 동결 자료·tool 원문·원장·이미지 바이트의 무결성 검사 **403개 PASS**를 별도로 확인했다. 자세의 일부가 맞아도 전체 장면을 성공으로 올리지 않았으며, 사용자 판단은 별도로 남겼다.
