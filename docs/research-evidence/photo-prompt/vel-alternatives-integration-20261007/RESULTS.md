# 시각 의미 대체 표현 반영 및 세 독립 테스트 결과

시각 의미·후보 데이터와 인덱스를 주 작업 공간에 반영했다. 세 독립 에이전트의 프롬프트·조회·선택 기록과 실제 생성 시도를 완료했으며, 이미지 두 장을 확보했다. 한 시도는 생성 서비스의 출력 심사에서 차단되어 픽셀을 검증하지 못했다. **세 이미지가 모두 전달되거나 모든 키워드가 통과한 결과는 아니다.**

## 데이터에 반영한 내용

| 반영 대상 | 실제 변경 |
|---|---|
| 기존 시각 의미 | 24개 프로필에 한·영 대체 표현 96개 추가 |
| 기존 후보 | 34개 항목에 동등한 표현 112개 및 문맥 경계 추가 |
| 새 관계 | 후보·시각 의미 13쌍, 전체 관계 표현 27개, 구성 요소 표현 78개 |
| 검색·실행 | 합쳐진 현재 주 작업 공간으로 semantic 문서 10,567개와 시각 프로필 2,321개의 인덱스 갱신 및 runtime publication |
| 원본 연결 | 217개 키워드 대조표 유지; 184행은 관련 보강/신규 데이터, 33행은 기존 의미·작성·관측·극성 경계 유지 |

기존 프로필의 활성화 조건·구성 의무·픽셀 게이트는 유지했다. 대체 표현을 곧바로 hard alias로 만들지 않았다. 골지/평면 줄무늬, 실제 O링/원판, 몸에 두른 타월/양손 타월, 창/거울, 접촉/가까움처럼 물체·소유자·관계가 다른 항목은 분리했다.

[구현 요약](IMPLEMENTATION-SUMMARY.json), [항목별 채택 근거](ADOPTION.json), [217개 키워드 연결](KEYWORD-ADOPTION.json), [실행 generation](RUNTIME-PUBLICATIONS.json)을 함께 저장했다. 이전 연구 원문·후속 분해·historical snapshot을 바꾸지 않았으며, 주 작업 공간의 동시 작업은 별도 추가 병합으로 보존했다. 병합 전 스냅샷의 소유 변경 밖 240개 파일은 같은 bytes를 유지했다.

## 실제 이미지 결과

| 독립 테스트 | 원문 키워드 판정 | 보강 데이터 반영 | 전체 시험 결과 |
|---|---|---|---|
| 조력 발전소 | 6개 중 5개 통과, 1개 부분 충족 | 보강된 머리·눈 목표 후보를 조회·상세 확인·채택하고 새 문구로 작성. 픽셀에서는 목표 분리가 불충분 | 부분 충족 |
| 오페라 분장실 | 반환 이미지 없음 | 새 열린 고리·작은 입술 틈 후보 2개를 채택하고 부착점·구멍·치아 가림을 최종 문구에 작성 | 출력 심사 차단, 판정 불가 |
| 해안 정류장 | 7개 중 6개 통과, 1개 실패 | 보강된 머리·눈 목표 후보를 채택. 픽셀에서는 지정된 목표 방향을 따르지 않음 | 결로·시선·승차권 지지 관계 실패 |

각 에이전트는 다른 무작위 시드로 컨셉을 정하고 후보 접근 전에 기본 프롬프트와 core를 동결했다. 서로의 pack·프롬프트·이미지·리뷰를 입력으로 사용하지 않았다. 동일한 원본 사진을 실제 reference 입력으로 전달했으며, native `image_gen.imagegen` 실제 호출은 각 1회, 총 3회다. 원본 사진의 SHA-256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 파일이 반환된 두 결과는 각각 1237×1272이며 원본 bytes와 동일하게 주 작업 공간에 복사했다.

에이전트별 픽셀 리뷰와 별도로 coordinator도 전체 장면과 native 크기를 직접 확인했다. [통합 결과](TEST-RESULTS.json), [별도 픽셀 관찰](COORDINATOR-PIXEL-REVIEW.json), [전달 파일 SHA](DELIVERED-IMAGES.json)에 기록했다. 이미 독립 baseline에 있었던 표현을 후보 데이터가 만들어낸 효과로 계산하지 않았다. 세 테스트는 조회→채택→최종 문구→이미지 경로를 확인한 작은 시험이며 데이터 전후 A/B나 일반 성공률 측정이 아니다.

### 조력 발전소

![조력 발전소 결과](/Users/chasoik/Projects/image-prompt/generated_images/vel-alternatives-20261007/tidal-relay.png)

낡은 밝은 금속과 어두운 구조물, 유리 물방울, 미래 작업복/갑옷 실루엣, 차가운 반사, 기계의 국소 진홍 빛은 확인했다. 작동 팔은 지정한 오른팔 대신 왼팔이다. 머리의 레버 방향과 눈의 램프 방향도 충분히 분리되어 보이지 않는다. 다섯 일반 신체 게이트는 통과하지만 이것이 위 시험 항목의 전부 통과를 뜻하지 않는다.

[프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_1/final_prompt.txt) · [키워드/관계 픽셀 결과](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_1/pixel_test_results.json) · [기여 추적](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_1/data_contribution_trace.json)

### 오페라 분장실

프롬프트·runtime 감사는 통과했지만 출력 단계의 `moderation_blocked`로 이미지가 반환되지 않았다. 차단을 특정 키워드가 일으켰다는 인과 주장은 하지 않는다. 원본 오류·요청 ID·한 번의 실제 호출과 독립 ledger를 보존했다.

일상복 대체안을 검토했으나 현재 `provider_blocked` 실행 경로는 변경·추가 호출을 `failure_route_cannot_rerender`로 거부한다. 다른 failure class로 재분류하지 않았고 추가 생성은 0회다. [스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)은 “Treat required bindings and audits as correctness checks”라고 규정한다. 이는 바인딩/감사를 유지해야 한다는 요구이며, 실제 추가 호출 거부는 [현재 구현의 조건](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_retry_projection.py:142)에서 확인했다.

[감사된 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_2/prompt_en.txt) · [차단/실행 요약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_2/arm_summary.json) · [미생성 일상복 초안](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_2/ordinary_theatre_alternative/ordinary_theatre_prompt_draft.txt)

### 해안 정류장

![해안 정류장 결과](/Users/chasoik/Projects/image-prompt/generated_images/vel-alternatives-20261007/coastal-bus-shelter.png)

새틴 광택, 국소 젖음과 밀착, 물방울, 젖은 머리, 피부 하이라이트와 자연스러운 피부 질감은 확인했다. 유리의 물방울과 별개인 결로의 흐린 층은 확인하지 못했다. 머리/눈은 버스와 승차권을 향하지 않으며, 승차권의 인쇄된 부분이 폴더 위에서 받쳐지는 관계도 성립하지 않는다. 신체 게이트 5개 중 접촉·공간 게이트 1개가 실패했다.

[프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_3/final_prompt_en.txt) · [키워드/관계 픽셀 결과](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_3/pixel_test_results.json) · [기여 추적](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_3/data_contribution_trace.json)

## 회귀 검증

변경 관련 고유 테스트 157개 중 156개가 통과했다. 남은 1개는 작업 기준 `629bf4a8`의 원래 테스트와 원래 candidate source bytes로 동일하게 재현한 기존 liminal 역사 범위 실패다. 새 대체 표현 테스트 8개는 주 작업 공간에서도 모두 통과했다. validator와 깊은 runtime publication 검증은 두 작업 공간 모두 통과했고 전체 suite 완주는 주장하지 않는다.

[검증 요약](VALIDATION.json), [기존 실패 재현](BASELINE-REGRESSION.json), `logs/`에 실제 실행 근거를 보존했다. 역사 oracle의 기대값이나 holdout을 새 결과에 맞게 바꾸지 않았다.

## 결과를 다음 검증에 반영할 지점

대체 표현의 저장·조회·후보 선택·최종 문구 반영은 확인했다. 보강된 머리/눈 관계의 완전한 픽셀 실현이나 새 고리/입술 관계의 픽셀 qualification은 확보하지 못했다. 다음 검증에서는 머리·동공·기존 목표를 같은 프레임에서 읽게 하는 배치, 눈 높이에 대한 실제 목표 방향, 손·물체·받침의 동일 접촉 패치를 먼저 검토해야 한다. 결로는 단순 물방울·배경 defocus와 별도의 표면 층으로 시험해야 한다. 이런 검토를 모든 시선·타월·젖음 키워드의 강제 recipe로 만들지는 않는다.

데이터/index 성공, 일반 신체 게이트, 개별 키워드/관계 픽셀 결과, 사용자 선호는 서로 다른 판정이다. 사용자 선호는 아직 미수집이다. 커밋·push·PR은 생성하지 않았다.

## 후속 조치: 반복 테스트 실패 수정

2026-10-08에 위 liminal 기존 실패의 역사 비교 범위를 수정했다. 데이터·인덱스·고정 기대값은 유지하고 과거 replay와 현재 검토 항목 검증을 분리했다. 별도 메타데이터 승계 검사도 수정 후 재검증했다. 관련 고유 테스트의 최종 판정은 184개 통과이며, 최초 실행과 수정 후 재검증을 구분한 [후속 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/liminal-history-test-repair-20261007/README.md)을 참고한다. 위 최초 실행 통계와 로그는 역사 기록으로 유지한다.
