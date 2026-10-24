# 러브코미디 데이터 반영과 이미지 테스트 결과

2026년 10월 24일 기준으로 시각 후보 99개, 비시각 맥락 진단 19개, 선택적 슬롯 연결 189개를 등록하고 기본 실행본에 반영했다. 독립 서브에이전트 세 개가 서로 다른 랜덤 장면을 정하고 첨부 사진을 실제로 전달해 이미지를 각각 한 번 생성했다.

이미지 생성은 3회 모두 성공했지만, 사전에 정한 상세 시나리오의 완전 합격은 **0/3**이다. 꽃꽂이는 코미디와 경쟁 맥락이 약했고, 스케이트는 지지 접점이 잘렸으며, 카페는 지정한 크랭크 대신 기둥을 잡았다. 신규 후보의 최종 채택은 세 실행 모두 0개이므로 **신규 데이터의 이미지 개선 효과는 미입증**이다.

## 데이터 반영 범위

| 반영물 | 내용 | 파일 |
| --- | --- | --- |
| 후보 원문 | 완전한 한·영 시각 선택지 99개와 맥락 진단 19개 | [후보 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_romcom_20261024.json) |
| 슬롯 연결 | 기존 슬롯에 대한 선택적 연결 189개 | [연결 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_romcom_bindings_20261024.json) |
| 의미와 근거 | 원래 용어 경로 317개, 장면 예시 7개, 원대화 1개와 외부 근거 26개 | [의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_romcom_semantics_20261024.json) |
| 사용 경계 | 관찰 가능한 관계와 비시각 주장, 매체 구분, 전체 계약 적용 원칙 | [참고 문서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/romcom-visual-semantics.md) |

시각 선택지는 표정과 시선 15개, 인물과 접촉 관계 29개, 의복 28개, 장면과 소품 9개, 구도 6개, 그림 기호 4개, 코미디 동작 4개, 민감 장면의 가시 경계 4개로 구성된다. 손의 주인, 천과 맨피부, 입술의 접촉과 틈, 몸의 지지, 우산의 공동 덮임, 이어버드의 연결 끝점, 의복의 구멍과 겹, 자극과 상대의 반응을 구분한다.

맥락 진단 19개에는 관계의 역사, 성격, 의도, 동의와 강압, 시간 순서, 대사와 소리, 실제 신분과 친족 관계처럼 한 장의 정지 화면으로 확정할 수 없는 내용을 보존했다. 이 진단에는 긍정 시각 문구와 효과를 넣지 않았고, 긍정 검색 풀에서도 제외했다. 만화 기호 네 개에는 일러스트·코믹·만화 매체 조건을 유지했다.

317개 용어를 모두 검증된 동의어로 취급하지 않았다. 독립된 어휘 근거가 확인된 개별 주장 41개와 나머지 연구 해석을 구분했다. 관계 그래프와 출처는 검토 자료이며, 장르 이름만으로 인물·접촉·사건·고정 의무를 자동으로 추가하지 않는다. 기존 후보 37개와의 전체 원문 비교는 기존 원문을 바꾸지 않는 별도 선택지 추가로 반영했다.

등록된 원문에는 `native_approval=false`를 유지했다. 원문 보존, 검색 노출, 선택 가능성, 실제 채택, 프롬프트 사용, 픽셀 합격은 서로 다른 상태다. 이번 세 이미지로 99개 선택지 전체가 승인됐다고 간주하지 않는다.

## 실행본과 검색 검증

최신 스킬 문서의 SHA256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`이며 세 실행의 manifest와 일치한다. 저장된 제어값인 sensual 1, fetish 0, creativity 1, surreal 0을 사용했다. 현재 선택된 봉인 커널을 유지하는 데이터 확장으로 구성했으며, 작업 중인 유지보수 스크립트 전체가 배포 커널과 같다고 간주하지 않았다.

이미지 테스트는 최초 검증한 실행본에 고정했다. 이번 작업에서 발행하고 기본값으로 선택한 검증본은 그 사이 추가된 캠퍼스 원문 123개를 보존해 다시 만들었다. 두 실행본의 신규 원문 118개는 모두 동일하지만 전체 후보 풀이 다르므로, 후자의 후보 풀에서 이미지를 다시 생성한 결과로 해석하면 안 된다. 정확한 버전과 해시는 [실행본 결합 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/final-runtime-binding.json)에 있다.

최종 확인 시점의 공용 기본값은 후속 메카 확장을 추가한 실행본으로 한 번 더 갱신됐다. 이를 덮어쓰지 않고 완전한 H-F2 검증과 신규 원문 118개·연결 189개의 동일성, 시각 후보 99개의 포함, 맥락 진단 19개의 긍정 검색 제외를 확인했다. 해당 기본값의 긍정 후보는 20,928개다. [승계 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/inherited-default-verification.json)은 원문 보존과 실행 구조를 확인하며, 아래 순위 수치와 이미지 결과는 각각 명시한 이전 검증본에 한정된다.

| 검증 층 | 결과 | 범위 |
| --- | --- | --- |
| 원문 등록 | 통과 | 기존 후보·슬롯·연결·정책을 보존하고 새 원문 118개 추가 |
| 경계 회귀 | 7개 통과 | 손·천·피부, 지지와 틈, 연결 끝점, 매체 및 시간 맥락 구분 |
| 이번 발행본 설치 | 통과 | 기존 원문 21,829개 보존, 전체 원문 21,947개와 긍정 후보 20,822개 검증 |
| 벡터 및 검색 구조 | 통과 | 이번 발행 H-F2의 기존 문서 벡터 20,725개를 정확히 재사용하고 새 시각 문서 99개 추가 |
| 한·영 개발 질의 | 목표 12개 중 11개가 상위 10위 | 대상 없는 대조 질의 4개를 포함해 총 16개 실행 |
| 이미지 요청과 산출물 결합 | 3개 통과 | 실제 참조 경로와 해시, 전달 프롬프트, 호출 수, 이미지 해시와 동결 입력 대조 |
| 상세 시나리오 픽셀 판정 | 완전 합격 0/3 | 부분 관찰은 전체 합격으로 처리하지 않음 |

한·영 질의는 전체 후보 풀에서 BM25F와 로컬 코사인 검색을 각각 한 번 사용했다. 주제 사전 필터로 새 후보를 끌어올리지 않았다. 이번 발행본에서 한국어 소맷단 천 집기 후보는 40위였고, 영어 대응 질의는 상위 10위였다. 최초 이미지 테스트 실행본에서는 같은 한국어 후보가 38위였다. 이 질의들은 작성자가 본 개발 자료이므로 홀드아웃 성능이나 일반적인 품질 향상의 증거는 아니다.

검증 근거는 [원문 결합](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/current-default-successor/canonical-source-validation.json), [설치와 선택](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/current-default-successor/default-selection.json), [검색 질의 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/current-default-successor/retrieval-probes.json), [산출물 결합 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/arm-artifact-verification.json)에서 확인할 수 있다.

## 독립 이미지 테스트

세 서브에이전트에는 같은 사용자 요청과 참조 사진, 서로 다른 랜덤 상황 영역을 전달했다. 각 에이전트는 후보 자료를 보기 전에 장면 초안과 입력 의미를 동결했다. 사용자 고정 조건에 창작 설정이 섞인 부분은 후보 본문 열람 전에 좁혔고, 이전 기록도 보존했다. 다른 실행의 장면·프롬프트·이미지를 전달하지 않았다. 이 독립성은 절차와 manifest의 선언 범위이며, 에이전트가 보지 않은 모든 내용을 암호학적으로 증명한다는 뜻은 아니다.

생성 전 [테스트 기준 스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/pre-render-testcases.json)을 보존했다. 세 실행 모두 원래 독립 초안을 최종 프롬프트로 선택했다. 신규 원문 노출은 각각 0개, 0개, 2개였고 신규 및 기존 후보의 최종 채택은 모두 0개였다. 전후 이미지 대조도 없으므로, 장르가 보인다는 이유만으로 데이터 개선 효과를 주장할 수 없다.

| 장면 | 신규 노출과 채택 | 관리 물리 관계 게이트 | 전체 시나리오 | 실제 관찰 |
| --- | --- | --- | --- | --- |
| 마지막 튤립을 함께 집은 꽃꽂이 경쟁자 | 0개 노출, 0개 채택 | 5/5 통과 | **FAIL** | 두 손과 연속 줄기, 두 화병의 지지는 읽힌다. 로맨스와 장난스러운 시선은 있으나 미완성 꽃꽂이의 경쟁과 분명한 코미디는 부분적이다. |
| 균형을 잃은 겨울 스케이트 데이트 | 0개 노출, 0개 채택 | 3/5 통과 | **FAIL** | 상호 웃음, 네 손의 주인과 중앙 손잡기는 읽힌다. 남성의 화면 오른쪽 스케이트 날과 얼음 접점이 잘려 지지와 가시성 두 게이트가 실패했다. |
| 파라솔 물이 쏟아진 노천 카페 | 2개 노출, 0개 채택 | 4/5 통과 | **FAIL** | 물방울·젖은 어깨·냅킨·상호 미소는 연결된다. 여자의 손은 지정한 크랭크 대신 그 위 수직 기둥을 잡는다. |

세 건 모두 리뷰 기록의 유효성 감사는 통과했다. 그 안에 기록된 물리 관계의 기술 판정은 꽃꽂이 통과, 스케이트와 카페 실패다. 꽃꽂이는 물리 관계가 맞아도 사전 테스트의 장르·경쟁 맥락을 모두 만족하지 못해 전체 시나리오는 실패다. 각 에이전트의 판정과 코디네이터의 원본 이미지 직접 검토를 [픽셀 검토 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/coordinator-pixel-review.json)에 구분했다. 코디네이터 검토는 블라인드 평가가 아니다.

첨부 JPEG는 세 번 모두 실제 `referenced_image_paths`로 전달됐고 파일 SHA256도 일치했다. 결과에서는 단발과 앞머리, 얼굴 외형의 대체적인 유사성을 확인했다. 이는 정성적인 외형 가이드 평가이며 실제 동일 인물, 나이, 성격, 관계나 감정의 증명이 아니다. 사용자 수용 판단은 모두 pending이다.

실행 도구는 내장 `image_gen.imagegen`이며 실제 호출은 실행별 1회, 총 3회다. 재생성과 별도 이미지 API 우회는 없었다. 도구가 실제 모델명을 반환하지 않아 특정 모델 버전의 픽셀 결과라고 단정하지 않았다.

| 생성물 | 실제 크기 | 프롬프트와 결과 기록 |
| --- | --- | --- |
| [꽃꽂이 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-a/images/tulip-rivalry.png) | 1237 × 1272 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-a/final-prompt.txt) · [결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-a/result-summary.json) |
| [스케이트 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-b/result.png) | 1237 × 1272 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-b/final-prompt.txt) · [결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-b/result-summary.json) |
| [카페 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-c/romcom-c-generated.png) | 1536 × 1024 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-c/final-prompt.txt) · [결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-c/result-summary.json) |

최종 프롬프트 파일 세 개는 실제 도구에 전달한 문자열과 바이트 단위로 일치한다. 꽃꽂이와 스케이트의 배포용 텍스트 파일에 붙어 있던 마지막 LF 한 글자는 원본을 따로 보존하고 실제 전달 문자열로 맞췄다. 생성 입력이나 이미지는 바꾸지 않았다.

## 다음 개선과 재시험 계획

1. **한국어 접촉 대상 구별을 개선한다.** 소맷단 천을 집는 경우와 맨손목을 잡는 경우의 최소 대립 질의를 별도로 동결한다. 긍정 접촉 대상과 제외 대상을 유지하면서 원문 표현 보강과 검색 처리의 효과를 나누어 비교한다. 현재 질의 하나의 순위만 맞추는 별칭 추가로 끝내지 않는다.
2. **신규 데이터의 실제 사용을 따로 진단한다.** 개발 질의와 새 홀드아웃을 분리하고 노출·선택·최종 문구·픽셀을 계속 추적한다. 완전한 원문 계약, 소유자 전제와 허용 효과를 먼저 검토하며, 연구 메타데이터나 검색 순위만으로 native 승인을 올리지 않는다. 일반 장르 랜덤 테스트와 명시적 상호작용 진단을 구분하고, 새 후보가 나올 때까지 같은 실행을 재샘플하지 않는다.
3. **세 실패 장면을 결함 범위에 맞춰 재설계한다.** 꽃꽂이는 가벼운 코미디의 원인과 상대 반응이 함께 읽히는 사건을 구성한다. 스케이트는 네 스케이트 날과 얼음 접점을 한 화면 안에 여유 있게 배치한다. 카페는 손가락과 크랭크 핸들의 접점을 명확한 크기로 보이게 한다. 기존 실패 기록을 보존하고 원래 의미와 참조 외형을 유지한 별도 재시험으로 다룬다. 접점이나 지지 의무를 제거해 기존 결과를 합격으로 바꾸지 않는다.

이 재시험은 이번 세 번의 생성에 포함되지 않는다. 원래 상세 리서치와 단계별 반영 계획은 [리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/RESEARCH.md)와 [반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/IMPLEMENTATION-PLAN.md)에 보존했다.

## 저장소 상태

변경은 로컬 소스와 설치된 기본 실행본에 반영했다. 공용 체크아웃의 기존 수정·삭제·미추적 파일은 정리하거나 되돌리지 않았다. 기존 파일의 보호 기록은 [보호 상태 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/integration-evidence/protected-state-check.json)에 있으며, 동시 변경이 관찰된 파일까지 모두 불변이었다고 주장하지 않는다. 이번 작업에서 commit, push, PR은 만들지 않았다.
