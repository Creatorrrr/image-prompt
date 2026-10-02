**시각 의미 데이터 반영 결과 — 2026-10-03**

현재 로더의 시각 프로필 1,496개 중 조사 대상으로 정한 15개와 캐릭터 의미 그래프의 kuudere 레코드 1개를 보강했다. 스킬과 런타임 로직은 이번 작업에서 수정하지 않았다. 기존 작업 파일을 기준으로 분리된 작업본을 만들고, 두 인덱스를 검증한 뒤 원문 데이터와 함께 적용했다. 최종 관련 회귀 검사와 원문·인덱스 일치 검증을 모두 통과했다.

- 문맥 의미: pilot, 원피스, 서사적 타락과 몸 위의 변화 경계, cowl, one-shoulder, ruching, split diopter, halation, broad/short lighting의 예문·반례·적용 범위를 보강했다.
- 이름 없는 구조: 목 개구부에 연결된 같은 천의 접힘, 의복 실 사이의 실제 열린 셀, 두 앞판의 고리·돌기 맞물림을 정의·컴포넌트·증거 표현·판정 설명에 함께 추가했다. 기존 증거 표현도 선택지로 유지했다.
- sheer의 아래층: 요청한 실제 신체, 아래 의복, 배경과 섬유층 사이의 투과 관계를 다룬다. 기존 불투명 아래 의복 선택도 유지한다. 아래층 선택이 고정된 뒤 다른 표면으로 바꾸면 결합 검사가 실패한다.
- kuudere의 범위: 침착한 외면과 특정 상대를 향한 친근함이 공존하는 일반 의미를 설명한다. 현재 시각 프로필은 그 관계를 실용적 도움과 같은 상대의 가시 결과로 표현하는 선택 연출이다. 필수 증거 8개와 관계 조건은 유지한다.

| 작성 데이터 파일 | 변경 레코드 |
|---|---|
| [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json) | pilot, one-piece dress, embodied transition, kuudere, sheer, split diopter, halation, broad/short의 9개 |
| [photo_prompt_visual_obligations_portrait_fashion_exposure.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json) | cowl, one-shoulder, ruching의 3개 |
| [photo_prompt_visual_obligations_clothing_structure.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_clothing_structure.json) | 목 개구부의 접힘과 앞판 잠금의 2개 |
| [photo_prompt_visual_obligations_textile_surface.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_textile_surface.json) | 실제 열린 셀의 미세 메시 1개 |
| [photo_prompt_character_moe_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json) | kuudere의 정의와 영어·한국어·일본어 설명 4개 필드 |

시각 프로필에는 승인된 초안의 88개 필드 연산을 적용했다. 필수 증거 필드 60개, 게이트 60개의 ID와 검토 해상도, 최소 내용어 수, all-of 필수 그룹, 출력 모드, 정확 용어와 강제 활성 조건을 보존했다. sheer에는 실제 의복 섬유층 뒤 신체를 가리키는 문맥 문장 2개를 추가했다. 중립 예문은 후보를 안내하며, 기존의 선택 절차를 통해 적용한다.

캐릭터 그래프의 첫 적용에서는 다국어 설명을 짧게 바꾸면서 기존 BM25F 회귀 자료의 쿨데레 긍정 2개와 가까운 반례 2개에서 회귀가 발생했다. 원래 작성 데이터의 구체적인 다국어 표현을 복원하고 한 가능한 연출이라는 범위를 덧붙여 해결했다. 정답 자료의 문장을 데이터에 복사하지 않았고, 검색 로직·역치·정답 자료는 유지했다. 최종 그래프 문장과 해시는 [보완 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/implementation/repair-plan.json)에 있다. 최초 초안과 조사 스냅샷은 당시 기준 자료로 남긴다.

기존 의복 투영 테스트는 초기 레코드 전체의 불변성을 전제로 하고 있었다. cowl, one-shoulder, ruching 세 항목의 예문·반례·범위 필드에서 기존 값이 그대로 남은 추가만 인정하도록 수정했다. 나머지 필드와 모든 다른 레코드는 전체 비교를 유지한다. [새 회귀 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_semantic_guidance_data.py)의 5개 테스트는 관계 누락, 별도 물건으로의 치환, 인쇄 대체, 리터럴 결합 누락, 요청된 아래층 변경과 필수 증거 누락을 확인한다.

| 파생 인덱스 | 최종 상태 |
|---|---|
| 시각 프로필 인덱스 | 1,496개, 변경한 15개 갱신, 나머지 1,481개 엔트리 동일, 정확 용어 3,624개 동일 |
| 의미 인덱스 | 9,700개, kuudere 1개 갱신, 나머지 9,699개 엔트리 동일, 활성 샤드 16개 |
| 벡터 공간 | gemini / gemini-embedding-2 / 768차원 유지 |

최종 레지스트리 SHA-256: `95204cd9f89fece88bc689837272c3fe8c7cf26b8255dec24e7069537d26adea`. 최종 사전 해시: `d8e967ea33f5619a3954f103c726774a7643ba156d82e15ea6a5d94ee0ee13c8`. 고유 변경 임베딩 항목은 16개이며 쿨데레 보완을 포함해 성공한 임베딩 항목 생성은 17회다. 원래 보호 파일 677개 중 이번 데이터·인덱스 7개와 필요한 테스트 1개를 제외한 669개는 바이트 해시가 같다. 기존 샤드 112개와 frozen holdout 11개도 보존했다. 옛 샤드를 삭제하지 않았다.

최종 관련 테스트: **100개 통과, 하위 검사 928개 통과**. 변경 전 기준 검사는 86개와 하위 검사 804개가 통과했다. `git diff --check`도 통과했다. 사전 전체 메타데이터 검사, 실제 생성 인덱스의 원문 해시·벡터 공간·엔트리 보존 검사는 통과했다. [기계 판독 검증 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/implementation/post-apply-validation.json)와 [적용 파일·해시 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/implementation/install-receipt.json)에서 확인할 수 있다.

독립 의미 평가 96개 언어 요청과 초기 이미지 비교 36회는 실행하지 않았다. LLM 평가와 이미지 생성 호출은 0회다. 이번 검사는 로컬 데이터·검색 회귀·증거 계약의 검증이며, 새 문맥에서의 의미 정확도, 모델의 차단 결과, 생성 이미지의 형상 보존이나 사용자 수용성을 확인한 결과가 아니다. 최초 코어가 고정된 이후 데이터가 후보·출력 근거로 쓰이는 기존 경계는 유지된다.

원어·도면·광학 자료의 조사 위치는 [출처와 접근 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/source-evidence.json), 변경 근거는 [상세 조사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/RESEARCH.md), 최초 반영 설계는 [계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003/INTEGRATION-PLAN.md)에 있다. 커밋과 푸시는 실행하지 않았다.
