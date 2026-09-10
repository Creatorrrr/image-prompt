# 색 조합 관계 데이터 반영과 3개 독립 이미지 테스트

2026-09-10. 실제 사용자 요청에 따라 연구 데이터를 런타임에 반영하고, 첨부 인물 사진을 참조한 이미지 3장을 생성했다. 각 장면은 독립 에이전트가 별도 난수 시드로 정했다. 재생성은 하지 않았다.

**배색 키워드의 픽셀 재현은 2/3 장면 통과, 1/3 부분 실패다. 신규 데이터의 전체 채택 검증은 불완전하다.** 프롬프트 검사 통과, 후보 노출, 데이터 채택, 생성 픽셀, 사용자 선호를 서로 다른 결과로 기록했다.

## 반영한 데이터

| 구분 | 반영 내용 |
|---|---|
| 색 관계 후보 | 89개: 완전한 관계 후보 64개, 넓은 해석을 위한 자문 후보 25개 |
| 시각 의미 프로파일 | 64개, 각각 2개 구성요소와 2개 픽셀 게이트 |
| 선택 가능한 관계 묶음 | 64개, 구성원·영역 권한·출처 해시 검증 |
| 원 연구의 66개 계열 | 47개는 선택 가능한 구체 관계, 7개는 자문만, 4개는 기존 데이터 재사용, 8개는 단일 프레임 런타임 제외 |
| 실제 의미 인덱스 | 8,532개 항목, gemini-embedding-2, 768차원 |
| 실제 시각 프로파일 인덱스 | 전체 566개 프로파일, 2,071개 exact term |

핵심 파일:

- [후보·묶음 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_color_relations_extension.json)
- [시각 의미 프로파일](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_color_relations.json)
- [66개 계열의 반영 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/coverage.json)
- [재현 가능한 작성 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/build_color_data.py)
- [출처 및 범위 한계 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_color_relations_extension.json)
- [원 리서치 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-combination-patterns-20260910/report.md), [27개 출처](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-combination-patterns-20260910/sources.json)

반영 단위는 색 이름이 아니라 **어느 대상·영역에 어떤 색 관계가 보이는가**다. 유채색 단색과 무채색, 분열 보색과 삼각 배색, 고채도/저채도의 반대 방향, 따뜻한 피사체/차가운 배경과 그 역방향, 키라이트/필라이트의 색, 방사형/동심형, 공간 그라데이션/톤 매핑, 듀오톤/트라이톤 등을 분리했다.

조명 후보는 `lighting`과 `color` 권한을 함께 요구한다. 색면의 배열·분할 후보는 `color`와 `composition` 권한을 함께 요구한다. 강제 배색 비율, 특정 색쌍, 의상, 얼굴·피부 변화, 문화·성격 의미를 기본값으로 넣지 않았다. 색상환의 기하를 사용하는 경우 실제 선택 단계에서 RYB 등의 색상환을 명시해야 한다.

넓은 명칭이나 의미 검색의 유사도는 자동으로 필수 조건이 되지 않는다. 완전한 관계 문장에 대한 exact 활성화 또는 작성자가 선택한 전체 프로파일에만 구성요소·증거 문구·픽셀 게이트가 연결된다. 넓은 검색 후보를 노출하려면 데이터 문장을 기본 프롬프트에 미리 넣어야 했던 초기 조건은 새 색 프로파일에서 제거했다. 의미 검색의 결과는 계속 자문이고, 선택하면 모든 구성요소를 검증한다. 이 결정의 회귀검사는 `test_semantic_similarity_is_advisory_even_for_close_visual_query`다.

등휘도와 동시 대비의 정확한 성립은 측정·지각 검증이 필요하다. 팔레트 연속성·진행·전환·역전·모티프·코딩은 순서 있는 복수 프레임의 계약이 필요하므로 이번 단일 이미지의 필수 프로파일로 만들지 않았다. 기존 low-key 조명 프로파일은 일반적인 어두운 팔레트보다 좁으며, Photoshop Selective Color 조절은 선택 영역의 색 보존과 동일한 것으로 등록하지 않았다.

## 독립 테스트 설계

사용자 원문 전체를 변경 없이 요청 봉투에 저장한 후 위임했다. 각 에이전트는 스킬 절차·사용자 원문·첨부 사진·일반 지식만으로 기본 프롬프트와 신체 동작 검토를 작성하고 해시를 동결했다. 그 뒤에만 로컬 데이터와 후보팩을 조회했다. 다른 에이전트의 장면이나 프롬프트는 입력으로 사용하지 않았다.

실험 키워드 묶음은 코디네이터가 나누었고, 세부 장면은 에이전트가 난수로 정했다. 이 실험 설정을 사용자가 직접 정의한 의미로 위장하지 않았다. 한 봉투의 실제 사용자 원문을 공유하되 세 코어는 각각 독립이다.

| 테스트 | 시드 | 독립 장면 | 실험 키워드 |
|---|---:|---|---|
| A | 1110891406 | 폭풍 후 산악 관측소에서 우량계를 다루는 관측자 | Split Complementary, Color Echo, Color Framing |
| B | 1361614120 | 야간 천문관에서 별 투영기를 조절하는 작업자 | Cross-Color Lighting, Colored Rim Light, Background Color Wash |
| C | 1986106126 | 대형 색면 앞에서 유약 샘플을 배열하는 도예가 | Muted-on-Vivid, Diagonal Color Split, Color Blocking |

각 기본 프롬프트는 223–247단어, 최종 프롬프트는 311–327단어다. 최종 프롬프트·참조 파일·런타임 요청을 감사한 뒤 native imagegen 참조 편집을 1회씩 수행했다. 이미지 3장은 모두 1086×1448이며 원본 크기와 축소 보기로 확인했다. 얼굴의 외형 유사성을 관찰했으며 실제 인물의 신원 확인을 주장하지 않는다.

## 실제 후보 노출과 채택

| 테스트 | 실제 노출된 새 시각 프로파일 | 채택 | 새 슬롯 / 새 묶음 노출 |
|---|---|---|---|
| A | complementary, split_complementary | split_complementary 1개 | 0 / 0 |
| B | cross_color_light, colored_rim | 두 프로파일 | 0 / 0 |
| C | color_blocks, diagonal_split | 두 프로파일 | 0 / 0 |

프로파일의 자문 검색 조건을 수정하기 전후 조회를 모두 저장했다. 세 arm의 공개 팩 ID와 후보 노출은 전후 동일했다. 기존 조회 상한은 프로파일 후보 2개이고, A와 C의 팩에는 color/color_grading 슬롯 자체가 없었다. B의 기존 lighting 슬롯에서도 새 색 후보가 선택 풀의 공개 결과에 나오지 않았다. 인덱스에 존재한다는 사실만으로 슬롯 또는 묶음이 실제 노출됐다고 판단하지 않았다.

따라서 **9개 실험 관계 중 신규 데이터의 실제 채택이 확인된 것은 5개**다. 나머지 4개는 데이터가 아니라 독립 기본 프롬프트가 작성한 조건으로 생성기에 전달됐다. 64개 묶음은 구조·권한 검사를 통과했지만 이번 자연스러운 조회 3회에서의 사용성은 검증되지 않았다. 이 제한은 렌더 성공과 별개의 배포 판단 항목으로 남긴다.

## 실제 이미지 판정

| 테스트 | 배색 키워드 픽셀 판정 | 선택된 색 게이트 | 신체·접촉 게이트 | 핵심 관찰 |
|---|---|---:|---:|---|
| A | 3/3 통과 | 2/2 | 5/5 | 파란 문틀·배경, 노랑주황 목도리, 빨강주황 코트가 분리됨. 목도리·표지·먼 지붕의 색 반복과 양쪽 파란 프레임도 보임 |
| B | 1/3 통과, 부분 실패 | 0/4 | 5/5 | 청록 소매·호박색 머리·자홍색 머리 윤곽광은 보임. 지정된 얼굴·블라우스의 청록/호박색 분할과 어깨의 자홍 윤곽광이 부족하여 해당 색 게이트 모두 실패 |
| C | 3/3 통과 | 4/4 | 5/5 | 선명한 파랑/빨강 대각 배경, 저채도 회색 인물, 분리된 세 도자기 색면과 질감·두께가 보임 |

**B는 선언한 대상과 영역을 기준으로 색 게이트 4개 모두 실패다.** 최초 리뷰는 소매·머리에서 보이는 일반적 효과를 프로파일 통과로 보고 얼굴·어깨의 누락을 별도 실패로 분리했다. 코디네이터 검토에서 원래 게이트가 명시한 “declared owners and scope” 조건에 어긋남을 확인했다. 에이전트가 변경 없는 최종 프롬프트와 원본 픽셀을 다시 대조해 네 게이트를 실패로 정정했다. 현재 감사 결과는 `technical_qualified: false`, `failed_technical_hard_gates`이며, 이전 리뷰·감사·보고서는 `arm-b/initial-review-v1/`에 보존했다. 이미지 재생성이나 평가 기준의 사후 완화는 없었다.

A에는 젖은 문턱, 추가 문구, 불규칙한 우량계 숫자라는 부수적 차이가 있다. 색 관계 통과를 모든 프롬프트 세부사항의 완전한 재현으로 확대하지 않았다. C의 저채도/고채도 대비는 보이지만 해당 새 프로파일이 미노출이므로 새 데이터가 그 결과를 만들었다고 주장하지 않는다.

독립 작성 에이전트의 리뷰 후 코디네이터도 저장된 세 원본 이미지를 직접 보고 핵심 색 관계와 B의 실패를 재확인했다. 아래 결과에는 실패 이미지도 그대로 보존했다.

### A — 산악 관측소

![A 산악 관측소](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-a/generated-attempt-1.png)

[A 전체 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-a/arm-report.md)

### B — 천문관: 부분 실패

![B 천문관](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-b/generated_images/planetarium-attempt-1/image.png)

[B 전체 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-b/arm-report.md) · [엄격한 장면 실패 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-b/supplemental-pixel-review.json)

### C — 도자기 작업실

![C 도자기 작업실](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-c/generated_images/ceramic-color-20260910/attempt-1.png)

[C 전체 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/color-three-arm-20260910/arm-c/arm-report.md)

## 코드·데이터 검증

- 색 관계 전용 테스트: 8/8 통과. 불완전 문장·부정문·넓은 명칭의 hard 활성화 차단, 반대 방향·유사 기법 분리, 선택 계약과 게이트 동반 유지, 모든 영향 차원의 권한, 출처 해시, 실제 인덱스 포함을 검사했다.
- 사전 메타데이터 및 두 실제 인덱스 검증: 통과.
- 관련 후보·검색·v6 검사: 첫 실행 49개 중 47개 통과, 과거 고정 개수 185/14를 검사하던 2개 실패. 데이터 추가 전에도 묶음이 273개여서 고정값이 낡은 상태였다. 개수 기대값을 작성된 원본과 실제 컴파일 결과의 정확한 일치 및 중복 없음 검사로 갱신했고, 해당 후보 의미 모듈 13/13 통과했다.
- 전체 회귀검사: **79개 모듈, 1,156개 테스트 실행 완료. 실패 44건(하위 사례 포함), 오류 3건이 남았다.** 실패한 10개 모듈의 해당 메서드·사례는 색 데이터 추가 전 작업 상태에서도 모두 재현했다. 전체 녹색 통과를 주장하지 않는다. 기존 장면/의상 라우팅, 고정 스킬 문구, 과거 항목 개수, 바이트 해시 및 선택 목록 계약의 실패가 포함된다. 생성 결과 바이트가 이전 데이터와 동일하다는 의미도 아니다. [최종 검증 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/validation-final.json) · [전체 검사 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/full-suite-combined.json) · [실패 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/baseline-failure-comparison.json)

전체 검사는 오래 걸리는 단일 순차 실행을 보존 후 모듈별 격리 실행으로 전환했다. 초기 실행기의 프로젝트 경로 누락으로 빠진 4개 모듈은 따로 실행했으며, 정상 discovery의 79개 모듈·1,156개 테스트와 최종 실행 집합·개수의 일치를 확인했다. 테스트 실행기 자체의 import 오류는 프로젝트 검사 결과에 섞지 않았다. 실패 비교는 필요한 실패 메서드 또는 원문 그대로의 실패 fixture 행만 재실행했으며, 원본 fixture와 golden snapshot은 수정하지 않았다.

기존 swimwear/embodiment 수정 및 삭제된 별도 스킬 작업은 유지했다. 의미 인덱스 빌더가 기본적으로 이전 세대 샤드를 정리하므로, 기존 tracked 샤드 16개를 정확히 복원했고 기존 untracked 세대는 그대로 재사용된 8,443개 항목으로 재구성해 변경 전 데이터 기준 재계산과 비교했다. 기록은 [shard-preservation.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-relations-implementation-20260910/shard-preservation.json)에 남겼다. 후속 인덱스 갱신에는 `--keep-stale-generations`가 필요하다.

## 남아 있는 한계

1. 일반 조회에서 색 슬롯과 묶음의 노출을 늘리는 후속 라우팅 검증이 필요하다. 이번 결과는 새 시각 프로파일 5개의 실제 선택·렌더 증거다.
2. B의 색 조명은 인물의 임의 영역에서 보이는 것과 지정된 얼굴·어깨에서 보이는 것을 더 엄격하게 구분해야 한다. 기존 실패를 보존했으며 재시도로 성공률을 바꾸지 않았다.
3. 원래 데이터와 새 데이터의 동일 조건 대조 이미지가 없으므로 인과적 품질 향상은 입증되지 않았다.
4. 세 이미지는 전체 89개 후보·64개 프로파일에 대한 보편 검증이 아니다. 정확한 색 좌표·면적 비율·등휘도 검증도 수행하지 않았다.
5. 사용자의 미적 선호·대표 이미지 승인은 대기 상태다. 테스트 완료를 자동 승격과 같게 취급하지 않는다.
