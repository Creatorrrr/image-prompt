# 첩보물 전체 대화 보강·재테스트 결과

크롬에서 참조 대화의 전체 본문과 **500행**을 확인해 누락 **160행**을 보강했다. **시각 대안 42개·문맥 diagnostic 160개·선택적 바인딩 71개**를 추가하고 기본 실행본에 설치했다. 원본 사진을 실제 첨부한 새 독립 이미지 생성은 **3/3 성공**, 사전 strict 전체 통과는 **0/3**이다. 세 실행 모두 **신규 후보 정식 채택·영감 반영 0개**여서, 이번 이미지가 새 데이터에 의해 개선됐다는 결론은 내릴 수 없다.

## 확보·반영 범위

500행은 단일 용어 480개, 혼동 구분 8행, 창작 조합 12행이다. 기존 340행 대비 추가 범위는 정치/조직 13, 성/친밀감/착취 17, 심문/고문/구금/암살 22, 심리/윤리 12, 서사 18, 공간/소품 17, 기관명 16, 구분 8, 표면 흔적 13, 촬영 12, 조합 12행이다. 헤어 20항목은 기존 범위에 이미 있었다.

원래 정의와 새 시각 대안은 동일시하지 않는다. 실제 신분·충성·동의·강요·진단·원인·시간·소리·진위·화학·성능을 표정이나 복장으로 확정하지 않는다. 연구 그래프와 출처는 native 승인으로 쓰지 않는다. 기존 외형 65행과 표본 의존 항목은 보류를 유지했다. 창작 조합 12개는 강제 프로필로 설치하지 않았다.

- [출처·경계·반영 방법](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/RESEARCH.md)
- [전체 500행과 연결 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/KEYWORD-ATLAS-FULL500.md)
- [42개 시각 의미 카드와 관찰 게이트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/VISUAL-CARDS.md)
- [기존/신규 registry 연결 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/registry-closure.json)

## 설치·검색 검증

이 작업에서 설치·검색 검증한 H-F2 `6d1d1389408abd7ddecd1da9e50ed007c4a87ce04f9fe547a49154127b7c6738` / native `60b5493720dafb20cc5cd24af5fcafd4980d8bb83c6cc9530eabaa0e3bcf8ae4`. 동시 발표된 다른 주제 자료를 보존한 기준선 **21,480개 record 전체와 모든 기존 binding/catalog/policy/커널**을 유지하고 202개 record를 추가했다. 작업 사전·native index·전체 배포 검증·recorder 검사·새 source round-trip이 통과했다. 원래 연구 34개 파일과 이전 결과/이미지 등 56개 integration member는 해시가 유지됐다. 공유 corpus/index/runtime 포인터의 정당한 후속 갱신은 별도 기록했다.

| 질의군 | 한/영 질의 | 목표 후보 상위 8 |
|---|---:|---:|
| 원문 smoke | 84 | 84 |
| 자연어 재표현 | 36 | 36 |
| 일반/비시각/혼동 대조 | 20 | 별도 경계 비교 |

일반·비시각 대조 16개는 기존 상위 8이 모두 유지되고 새 후보 유입이 없었다. 혼동 대조 4개에는 관련 신규 후보 5회가 노출됐다. 이는 긍정 채택이나 false-positive 판정이 아니다. 모든 source 진단 기록은 긍정 검색에서 제외됐다. 실제 BM25F 1회+local cosine 1회를 질의마다 확인했다. 원문과 연구자 재표현이므로 독립 holdout이나 픽셀/채택 성공은 아니다.

이미지 arm은 동일 보강 202개가 들어간 설치본 `607f27b10495bfaad80edd62ec932b863fb8365098ea90e4cb3b694ec656fa25`에 고정했다. 이후 최종 union은 다른 주제 변경을 추가 보존했고 동일 보강 source 및 71 binding row와 검색을 재검증했다. 이미지 기록을 최종 union에서 생성한 것으로 바꾸지 않았다.

## 세 독립 이미지 테스트

현재 로컬 최신 SKILL SHA `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`. 세 새 에이전트는 각자 무작위 전체 장면과 기준을 자료 검색 전에 봉인했다. 각 native 호출은 정확히 1회, 원본 portrait의 실제 referenced_image_paths와 SHA를 확인했다. API/fallback/재생성은 0회이며 관찰된 모델 ID는 도구가 제공하지 않았다.

| arm | 장면 | 실제 보인 것 | strict 실패 | 공식 기술 qualification |
|---|---|---|---|---|
| A | 서고 계단 연락원 | 커프에 연결된 낱실·마모 경계·물방울·봉투/계단 | crease 입체 구조, 오른손 엄지→flap 접점 | fail |
| B | 항구 검문소 여권 교환 | 두 인물의 손과 같은 booklet·전경 가림·림광 | 허벅지 중간보다 낮은 crop | pass (embodiment 5/5), strict는 fail |
| C | 창가 도시어/콘택트시트 | 4칸·종이 경계·두 클립·사진/실제 창과 gate 구분 | 손가락이 아래 여백 대신 오른쪽 여백에 접촉 | fail |

신규로 노출된 것은 A의 coat tear/opaque lining, B의 POV hands/folder, C의 temple moisture beads다. 각각 고정한 장면의 전체 조건/소유자/효과와 맞지 않아 미채택했다. A/B는 기존 일반 source에서만 국소 inspiration을 유지했고 C는 독립 baseline 그대로다. 새 source의 픽셀 성공은 **UNSCORED_NOT_ADOPTED**, 장면 자체의 사전 strict는 **FAIL**이다. 이미지 호출/저장 성공과 공식 리뷰 기록 유효성도 전체 strict와 구분했다.

B/C는 봉인 후 상태 확인 도구에서 이전 테스트의 완료 요약을 우발적으로 본 예외를 기록했다. 현재 다른 full arm의 파일·완전한 프롬프트·이미지는 읽지 않았다는 선언과 변하지 않은 봉인을 보존했다. 완전 블라인드 노출 실험이라고 주장하지 않는다. 코디네이터도 원본 픽셀을 직접 재검토했다. B 상부 lintel 가시성은 코디네이터가 추가 보수 판정으로 남겼으며, B3 crop 실패와 전체 결론은 같다. C의 gate 비교는 native crop 재검토로 확인했으며 초기 불확실성 기록도 보존했다.

### A. 서고 계단의 연락원

[실제 전송한 정확한 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/prompts/A.txt) · [독립 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-a/arm-a-final.json) · [코디네이터 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/coordinator-pixel-A.json)

![서고 계단의 연락원](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-a/managed-v2/result.png)

### B. 항구 검문소의 여권 교환

[실제 전송한 정확한 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/prompts/B.txt) · [독립 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/arm-result.json) · [코디네이터 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/coordinator-pixel-B.json)

![항구 검문소의 여권 교환](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/results/ferry-passport-native.png)

### C. 창가의 도시어·콘택트시트

[실제 전송한 정확한 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/prompts/C.txt) · [독립 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-c/arm-report.json) · [코디네이터 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/coordinator-pixel-C.json)

![창가의 도시어·콘택트시트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-c/results/contact-sheet-window.png)

## 후속 계획과 남은 한계

[구체적인 후속 반영·검증 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/FOLLOWUP-PLAN.md)에 실제 장면의 후보 노출/전체 조건/채택 추적, A의 crease·엄지 접점, B의 정확한 crop, C의 아래 여백 접점을 우선순위로 남겼다. 추가 생성으로 이번 실패를 덮지 않았다. 기존 미검토 65행과 표본 의존 항목도 개별 source 검토 전까지 보류한다.

초기 staged store는 recorder import 검사를 통과했지만 실제 native loader가 쓸 모델 부속 파일이 없어 세 arm 모두 검색 전에 중단됐다. 실제 installer의 SHA 검증 모델 배치와 full deployed 검증 후 같은 generation의 설치 경로로 해결했고 source/core/plan을 바꾸지 않았다. 동시에 기본 실행본이 갱신되어 기존 선택을 덮어쓰지 않았으며, 이를 보존한 union을 별도로 설치했다. [오류·복구 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/pre-retrieval-incident.json)에 남겼다.

[원본 참조·정확 프롬프트·세 ledger·원본/복사 hash 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/native-artifact-validation.json) / [최종 설치 source 동등성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/installed-data-equivalence.json) / [기계 판독 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/RESULTS.json). 사용자 수용은 pending이다. 이 작업에서는 commit/push를 수행하지 않았다.

최종 확인 중 다른 작업의 후속 기본 실행본 `8421c8b02c7c23b4557898bc1c463d1991533e95e3ceb4ef9758890909217e8c`가 발표됐다. 이를 덮어쓰지 않았고 보강 source 202개와 binding 71행이 같은 내용으로 유지됨을 검증했다. 위 140개 질의의 측정값은 명시한 자체 검증 union의 결과이며 후속 실행본으로 재표시하지 않았다. [후속 기본 실행본 보존 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/post-publication-default-observation.json)
