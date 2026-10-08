# 셀카 포즈 데이터 반영 및 3개 독립 이미지 실험

시각 의미·후보 데이터를 주 작업공간에 반영했고, 세 독립 서브에이전트가 서로 다른 복합 컨셉과 첨부 외형 참조로 각 한 번씩 이미지를 생성했다. **새 후보 채택은 2/3이며, 주제의 완전한 픽셀 대응은 부분 성공이다.** 공식 기준 통과와 새 데이터의 기여를 구분한다.

## 데이터 반영

- 후보 104개: 연구 단위 98개에서 분리한 101개 변형과 촬영 입력 후보 3개.
- 새 시각 프로필 101개와 필수 관찰 관계 303개. 기존 물리 거울 프로필 1개를 수정해 지정된 나이·인물 수·가림을 보존한다.
- 원래 180개 번호 단위는 새 변형 또는 기존 구성요소 재사용 경로를 갖는다. 기존 구성요소와 부분 일치가 전체 포즈의 동의어임을 뜻하지 않는다.
- 책의 한 손/양손, 립스틱/브러시/퍼프의 도구 접점, 눈웃음/입 중립형, 손 가림/폰 가림, 높이/방향, 촬영 손/다른 작업 손을 구분한다.
- 양손·그룹·소품 후보에는 입력 전제를 기록했다. bare bambi와 cat-heart의 새 이름 활성화는 보류했다.
- 촬영 방식은 장르 제한이 있는 기존 capture_context와 분리했다. 이름 없는 의미 검색은 optional이며 필수 조건으로 승격하지 않는다.

작성 데이터: [후보](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_selfie_pose_extension.json) · [시각 프로필](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_selfie_pose.json) · [180개 반영 경로](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/coverage-180.json) · [초기 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-semantics-20261008/README.md)

## 실험 결과

| 독립 컨셉 | 새 후보 채택 | 공식 기준 | 새 주제 및 한계 | 검토 파일 |
|---|---|---:|---|---|
| 비에 손상된 축제 종이등 수선 후 거울 셀카 | slot:capture_mode:sf_capture_physical_mirror | 5/5 | 보이는 폰 그립과 동일 반사 공간은 확인. 화면 응시와 실제 렌즈 활성은 확인 불가. | [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/final_prompt_en.txt) · [상세 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/report.md) |
| 회전목마 수선실에서 부러진 목재 조각을 보여주는 초광각 셀카 | slot:capture_mode:sf_071_base | 9/9 | 촬영 팔과 얼굴 지향, 가까운 손·물체와 먼 공간은 확인. 실제 렌즈 높이·기기 접촉은 확인 불가로 PARTIAL. | [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/final-prompt-v2.txt) · [상세 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/report.md) |
| 누수에서 씨앗을 지키는 온실의 양손 작업 셀프포트레이트 | 채택 0 | 5/5 | 두 손의 작업 역할은 보임. 새 촬영 후보는 거절했으며 고정 장치·타이머 원인은 확인 불가. 수로 높이·방향·크롭은 기본 구성과 불일치. | [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/fixed/final_prompt.v2.txt) · [상세 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/fixed/report.md) |

각 생성 원본은 1237×1272이며 편집하지 않았다. 원래 요청·참조 파일·동결 코어·controls·후보 팩·런타임 입력·생성 기록·픽셀 판정의 해시를 보존했다. 첫 조회에서 발견한 결손을 보완한 후 같은 코어로 다시 조회했고, 이전 예약에는 실제 호출이 없었다. 독립 기준을 생성 결과에 맞춰 완화하거나 추가하지 않았다.

공식 19개 기준은 기존 신체 계약과 B의 기존 pc16 관계 프로필에서 나왔다. **새 sf_profile을 직접 선택한 사례는 0개**다. 새 시각 프로필 101개가 이미지에서 모두 검증됐다는 뜻이 아니다. 카메라·타이머의 실제 작동, 정확한 감정·정체성·나이·이력은 이미지로 확정하지 않는다. 비교 생성 없이 후보 때문에 이미지가 개선됐다고 주장하지 않는다. 사용자 수용은 아직 판정되지 않았다.

고정 촬영 입력 후보가 C에 조회되지 않은 점은 남은 결손이다. 고정 장치·타이머 원인을 위한 전용 픽셀 프로필은 설계상 추가하지 않았으므로, 존재하지 않는 그 프로필의 미노출을 실패로 세지 않는다.

## 검증과 남은 결손

등록·전체 작성 데이터·두 인덱스·게시 검사를 통과했다. 변경 범위 검사 35개와 수정 후 관련 검사 6개가 통과했다. 실제 Gemini 의미 질의 네 개에서는 새 프로필 3개를 optional로 조회했고 인접 hard-negative 네 개는 통과했다. 이름을 쓰지 않은 샤카의 새 프로필 조회는 실패했으며 그대로 기록했다. 이것은 연구 작성자의 진단 질의이며 독립 holdout이나 통계적 성능 증명이 아니다.

전체 229개 모듈을 격리 실행했다. 2,079개 발견 중 1,995개를 실행했고 84개는 class setup 실패로 실행하지 못했다. 원래 26개 실패 모듈 중 격리 복사 결손 3개 모듈과 이번 거울 표현 회귀 1개 모듈은 관련 재검사로 해결했다. **남은 22개 모듈 실패는 변경 전 바이트로도 재현되며 전체 회귀는 미통과다.** 과거 테스트·골든·픽셀 기준을 수정해 통과시키지 않았다. [회귀 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/regression-classification.json) · [원래 전체 로그 요약](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/full-suite-modules/SUMMARY.json)

마지막 거울 표현 회귀 수정은 이미지 생성 후 기존 “any facial occlusion” 의미를 복원한 metadata 수정이다. 이미지의 원래 세대와 receipt를 유지한다. 새 후보/프로필 작성 파일과 채택된 계약·19개 판정 기준은 동일하며, 해당 거울 프로필은 세 실험에서 선택되지 않았다. [세대 간 보존 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/render-to-final-source-compatibility.json)

최종 주 작업공간 runtime generation은 `e0926b3e4361d0f603410293ecb44adcec6e378916982be02d80d6761cf206a4`다. [게시 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/primary-runtime-publication-revision-3.json). 초기 추적 파일 22,993개와 적용 artifact 40개를 대조했다. 요청 밖 추적 파일의 변화와 HEAD 변화는 없었다. 초기 ignored/untracked 파일 전체에 대한 해시 보증은 아니다. 기존 원본과 복구 ZIP을 유지했으며 커밋·푸시·원격 배포는 수행하지 않았다.

## 다음 개선 계획

| 순서 | 개선 대상 | 작업 | 통과 기준 |
|---|---|---|---|
| P0 | 고정 촬영 후보 조회 | 기존 세 코어를 보존한 진단 묶음에서 카메라 소유·지원 장치·셔터 입력이 focal query에 어떻게 반영되는지 추적한다. 특정 ID 강제 채택이나 cap 증가로 맞추지 않는다. | 고정/직접/거울의 타당한 후보를 조회하고 양손과 충돌하는 전체 의미는 거절할 수 있다. |
| P0 | 샤카와 인접 손 모양 | 작성 문구를 복사하지 않은 양언어 서술, 손가락 단위 양성·음성, 손 소유와 크롭 결손을 묶어 의미 검색을 검증한다. | 샤카가 조회되며 록·손가락 하트·안테나가 필수 샤카 조건을 만들지 않는다. |
| P1 | 새 시각 프로필의 실제 선택 | 명칭 없는 독립 복합 상황에서 전제를 이미 갖춘 새 프로필을 선택해 명시 증거와 정확한 gate를 동결한다. | 후보·프로필 조회, 전체 의미 채택, 런타임 근거, 픽셀 관계를 각각 기록한다. |
| P1 | 크롭·가림·기하 | 한 팔 촬영/양손 작업, 눈·폰 가림, 높이/방향, 가까운 손/먼 배경에 대해 정답과 혼동 장면을 짝지어 검증한다. | 필요한 소유·접점을 native에서 볼 수 있으며 일부 일치나 가림은 전체 PASS가 되지 않는다. |
| P2 | 넓은 용어 범위 | 연구의 13개 렌더 가족을 차례로 시험하고 정의가 불확실한 이름은 출처·관습을 추가 검증한다. | 소수의 좋은 셀카를 전체 180개 포즈 검증으로 확대 해석하지 않는다. |

후속 작업은 이 보고서의 계획이며 추가 생성·자동화는 시작하지 않았다.

## 생성 원본

거울 수선실

![거울 수선실 셀카](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/generated_images/mirror-lantern-native-01.png)

회전목마 수선실

![회전목마 수선실 초광각 셀카](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/generated-native-attempt-1.png)

온실 씨앗 보호

![온실 양손 작업 셀프포트레이트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/fixed/generated_images/greenhouse_seed_rescue_attempt_1.png)
