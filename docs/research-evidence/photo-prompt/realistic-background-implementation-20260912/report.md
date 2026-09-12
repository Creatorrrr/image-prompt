# 현실적 배경 데이터 반영 및 독립 3안 렌더 검증

시각 의미 데이터와 후보팩에 반영하고, 첨부 인물 사진을 사용해 독립된 서브에이전트 3개가 만든 복잡한 장면을 생성·검토했다. **최종 사전등록 기준은 A 5/5, B 5/5, C 4/5이다. C는 흐린 날 광질이 직접광으로 바뀌어 전체 실패로 판정했다.** 선택한 배경 관계의 구현과 전체 장면의 충실도는 별도로 기록했다.

## 반영한 데이터

| 구분 | 결과 |
|---|---:|
| 신규 시각 의미 프로필 | 32 |
| 중복 생성 대신 기존 계약 재사용 | 5 |
| 신규 후보 항목 | 37 |
| 런타임 후보 묶음 | 16 |
| 최종 시각 인덱스 | 619 프로필 / 2,124 정확 활성화 문구 |
| 최종 의미 인덱스 | 8,590 항목 / 768차원 / 16개 샤드 |

[시각 의미 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_realistic_background.json)와 [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_realistic_background_extension.json)를 별도 확장 파일로 등록했다. 항목별 원천·재사용·슬롯 매핑은 [source-coverage.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/source-coverage.json)에 있다.

37개 관계는 공간 접속·사용 흔적·설비 부착·수선·마모·물자국, 재료별 반사·젖고 마른 경계·유리 투과와 반사, 창·실내등·혼합광·반사광·그림자·접촉, 노출·하이라이트·대기 원근·초점·원근·가림, 국소 움직임·바람·노이즈·렌즈 현상·처리 절제, 깨끗한 공간·물건 밀도·하중·유리 얼룩·식생·도장 경계·연광·경광·필름 질감을 다룬다. 각 신규 프로필에는 **동일 이미지의 지정 대상에서 모두 보여야 하는 구성요소 3개와 게이트 3개**가 있다.

`realistic`, `documentary`, `RAW`, `HDR`, `available light`, `film grain` 같은 넓은 말만으로 특정 오염·광학 효과를 강제하지 않는다. 짧은 검색 단위는 선택 후보를 찾는 데 사용되며 하드 활성화 별칭이 아니다. 사용자가 완전한 관계를 요구하거나 작성자가 선택한 계약에 필요한 구성요소만 판정한다. 촬영 이력·실제 장소·재료 진단의 진위를 단일 이미지로 인증하지 않는다.

기존 계약을 재사용한 5개는 젖은 표면의 광원 반사, 하이라이트 전이, 심도에 따른 초점 저하, 연광, 경광이다. 연구의 6개 설계 가설은 직접 실험 근거가 없는 상태를 유지했으며, 런타임에는 연구 출처·검증 결과를 섞지 않았다. [상세 연구](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-20260912/report.md), [19개 출처와 지원 범위](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-20260912/sources.json), [원래 98개 평가 명세](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-20260912/evaluation-cases.jsonl)는 그대로 보존했다. 98개는 실행한 자동 테스트 수가 아니다.

## 실제 노출 실패로 확인한 문제와 수정

첫 팩은 A·C에 새 후보를 노출하지 못했다. B에는 새 프로필 1개가 있었지만 특정 ‘로비’와 재료를 고정해 티 갤러리에 맞지 않았으므로 선택하지 않았다. 이 단계에서 인덱스 성공을 후보 노출 성공으로 처리하지 않았다.

수정 사항은 다음과 같다.

1. 긴 예시 문장 외에 짧고 관찰 가능한 긍정 의미 단위를 추가했다. 전체 관계의 정확 활성화 조건은 유지했다.
2. 환경 초점·먼 풍경·깨끗한 실내·금속 응답에서 불필요하게 고정된 장소와 재료 예시를 일반화했다. 해당 장면의 형태·표면을 실제 문구에서 지정하도록 했다.
3. 인물 장면을 배제하던 `surface_material` 슬롯의 재료 응답 후보를 환경에서도 사용할 수 있는 `texture`로 옮겼다.
4. 같은 슬롯의 여러 항목을 동시에 선택해야 해서 현재 공동 채택 정책을 통과할 수 없는 연구 묶음 6개는 런타임에서 제외하고 연구 자료에 남겼다. `rbb_residential_street`, `rbb_storefront_night`, `rbb_sunny_courtyard`, `rbb_maintained_home`, `rbb_repair_workshop`, `rbb_day_transit`이다. 기존 14개에 일반적인 재료·초점 및 풍경 깊이 묶음 2개를 더해 최종 16개다. 건조한 낮 묶음에서는 부적합한 실내 청결 구성요소를 제거했다.
5. 선택 시각 프로필 및 묶음의 후보 상한을 각각 2개에서 8개로 넓혔다. 순위 알고리즘이나 하드 활성화 기준은 바꾸지 않았다. 영향은 현실적 배경에만 한정되지 않으며 다른 요청에서도 선택 가능 후보가 늘 수 있다.
6. 기존 긍정 검색 투영이 읽던 선택 필드 `semantics.visual_components`를 사전 검증기에서도 명시적으로 허용하고, 비어 있거나 중복·비문자열인 값은 거부하도록 했다.
7. 새 선택 후보가 생겨도 ‘미선택’을 명시해야 하므로 authorship 테스트 픽스처에 `chosen_visual_concept_ids: []`를 추가했다. 감사 규칙은 완화하지 않았다.

최초 실패 이후 수정한 데이터를 같은 코어로 다시 평가했으므로, **이 결과는 노출 문제를 보정한 뒤의 재검증이며 손대지 않은 독립 홀드아웃이 아니다.** 세 에이전트의 콘셉트·초기 프롬프트·기준은 서로의 출력이나 데이터 문구를 보기 전에 고정했고, 수정 팩에서도 코어와 랜덤 시드를 유지했다.

## 3개 이미지 결과

| 안 | 독립 작성 콘셉트 / 시드 | 최종 새 데이터 노출 | 채택 | 사전등록 판정 |
|---|---|---|---|---|
| A | 비가 갠 경사지 버스 환승장 / 1751180039 | 프로필 1, 묶음 6 | 설비 부착 프로필 + 재료·초점 묶음 | **5/5 PASS** |
| B | 깨끗한 티 테이스팅 갤러리 / 2026091202 | 프로필 3, 묶음 3 | 청결·재료·연광 묶음 | **5/5 PASS** |
| C | 저수지 위 고산 식물정원 테라스 / 17705118996401894872 | 프로필 0, 묶음 6 | 풍경 깊이 묶음 | **4/5 FAIL** |

일반 슬롯에 독립 항목으로 노출된 `rb_` 후보는 최종 3안 모두 0개였다. 이번 실제 채택 경로는 **프로필과 공동 채택 묶음**이다. 모든 슬롯 검색 경로가 개선됐다고 주장하지 않는다.

### A — 설비의 부착과 재료·깊이

[![A 미리보기](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-a/revision-2/review-thumbnail.png)](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-a/revision-2/generated.png)

배수 격자가 보행면과 맞물리고, 우측 벽의 배관은 브래킷에 부착되어 있으며, 설비 사이의 통로가 이어진다. 콘크리트·타일·금속·유리를 구분할 수 있고 인물–쉼터–아파트의 세부가 거리 순서에 따라 줄어든다. 왼손 난간 접촉·오른손 가방·양발 지지가 함께 보인다.

사전등록 5/5, 신체 5개와 선택 프로필 3개의 하드 게이트 8/8, 묶음 구성 2개와 공동 관계 1개가 통과했다. [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-a/revision-2/final_prompt.txt) · [상세 결과](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-a/revision-2/test_results.json)

### B — 청결·서로 다른 표면 응답·같은 유리면의 투과와 반사

[![B 미리보기](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-b/revision-2/thumbnail-02.png)](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-b/revision-2/generated-02.png)

석재의 넓은 음영과 금속 선반의 좁은 은색 반사 띠가 구별된다. 은색 금속은 아래의 따뜻한 발광 스트립과 별개로 보인다. 프레임으로 구획된 같은 유리면에 먼 선반의 투과와 창·수목의 반사가 공존한다. 사람·컵·접시·카운터의 지지 관계도 확인했다. 연광은 소매와 가까운 카운터의 명암으로 판정했으며, 더 단단한 바닥 그림자를 연광의 증거로 사용하지 않았다.

사전등록 5/5, 선택 묶음의 3개 구성군·9개 세부 관계 및 공동 관계가 통과했다. 묶음 ID는 `rbb_clean_clinic`이지만 실제 계약은 일반 실내 관계이며 프롬프트에 병원을 추가하지 않았다. [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-b/revision-2/final_prompt.txt) · [채택 데이터 검토](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-b/revision-2/adopted_pixel_review.json)

**첫 B 이미지는 금속 선반 반사가 불명확해 4/5 FAIL이었다.** 그때는 신규 데이터 채택도 0개였다. [첫 이미지](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-b/generated-01.png)와 실패 기록을 유지했다. 두 이미지 차이만으로 데이터의 인과적 개선을 입증하지 않는다.

### C — 거리별 깊이는 통과, 고정한 광질은 실패

[![C 미리보기](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-c/revision-2/review_thumbnail.png)](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-c/revision-2/generated_image.png)

근경 석재의 거친 세부, 중경 정원과 호수, 원경 산의 낮아진 대비가 순서대로 보인다. 그늘진 관목 아래 잔설과 젖은 하부 계단·마른 상부 발판도 지정된 위치에 있다. 원경 산의 눈으로 관목 아래 눈을 대체하지 않았다. 선택한 깊이 묶음의 2개 구성요소와 공동 관계는 통과했다.

하지만 C5는 석재·식생뿐 아니라 고정한 흐린 하늘의 광질까지 요구한다. 이미지에는 직접광의 선명한 그림자가 있어 **부분 구현 → 실패**로 판정했다. 에이전트의 최초 5/5 의견도 별도 보존하고, 상위 재검토를 반영해 최종 4/5로 고쳤다. [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-c/revision-2/final_prompt.txt) · [최종 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/arm-c/revision-2/test_results.json)

## 검증과 남은 범위

- 최종 전용 테스트 **10개**, 관련 의미·후보·코어·뷰어·검색 테스트 **81개**, 보정한 authorship 테스트 **9개**, 합계 **100개 통과**.
- 사전 메타데이터, 두 생성 인덱스의 원천 일치, 장면 감사, `git diff --check` 통과.
- 3안 모두 합성 프롬프트와 실제 이미지 호출 요청 감사 통과. 각 호출에 첨부 이미지의 정확한 경로가 연결됐고, 결과 이미지·프롬프트·코어·팩 해시와 원장을 보존했다.
- 후보팩 호출은 초기/수정 각 3개로 총 6개, native 이미지 생성은 A 1회·B 2회·C 1회로 총 4회다. C의 실패를 숨기기 위한 추가 생성은 하지 않았다.
- 전체 회귀 스윕은 데이터 수정 중 중단한 **진단용 불완전 실행**이다. 81개 모듈 중 39개의 종료·시간초과 결과만 수집했으며 전체 통과라고 주장하지 않는다. 별도로 비교한 기존 beastkin·golden 실패 지점 12개는 변경 전 복원본에서도 재현됐다. 실패 위치 일치가 모든 출력의 동일함을 의미하지는 않는다. golden을 새 결과로 덮어쓰지 않았다.
- C의 `botanical` 배경이 인물 주체 대신 `plant` 조언용 분류를 유발하는 기존 라우팅 문제는 기록했다. 고정 코어·실제 프롬프트·생성 인물은 유지됐고, 이번 데이터 반영 중 그 별도 라우팅 알고리즘은 수정하지 않았다.
- 실제 이미지로 본 것은 37개 전체가 아니라 **신규 5개 및 재사용 1개 관계군의 선택 사례**다. 나머지 항목의 이미지 재현율, 다른 모델·시드의 성공률, 인과적 품질 향상은 아직 확인되지 않았다.
- 원본과 축소본을 서브에이전트와 상위 에이전트가 검토했다. 외모 유사성은 관찰 의견이며 정확한 신원 판별 결과가 아니다. 사용자 최종 판단은 대기 상태다.

[최종 집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/delivery-summary.json) · [상위 픽셀 재검토](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/realistic-background-three-arm-20260912/parent_pixel_review.json) · [소스·참조 해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/final-source-manifest.json) · [기존 실패 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/baseline-comparison.json)

기존 model-editorial 및 다른 작업 변경은 보존했다. 커밋·푸시는 수행하지 않았다.
