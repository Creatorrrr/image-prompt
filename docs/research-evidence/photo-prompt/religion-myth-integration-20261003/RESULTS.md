# 종교·신화 시각 의미 반영 및 3개 독립 이미지 테스트

시각 의미와 후보팩 반영은 완료했다. 실제 이미지 검증은 **최종 0/3 PASS, 3/3 FAIL**이다. 키워드가 일부 보이는 것과 완전한 관계를 구현하는 것을 구분했다. 결과 파일·원본 이미지·프롬프트·실패 증거를 그대로 보존했다.

## 반영한 데이터

| 범위 | 완료 내용 |
|---|---|
| 기존 의미 프로파일 12개 | 완전한 대체 표현 24개와 기존 신화·그리핀 구성요소의 대체 증거 문장 55개. 기존 exact 활성화·필수 그룹·픽셀 게이트 유지. |
| 신규 의미 프로파일 54개 | 출처와 변형 범위를 명시한 구성요소 157개, 한국어·영어 대체 표현 281개. 완전한 긴 표현만 exact 의무이며 검색 적중은 선택 후보. |
| 기존 슬롯 후보 64개 | 원래 슬롯의 뜻·관계·소유 필드를 유지하며 대체 표현 추가. |
| 신규 구도 후보·묶음 각 80개 | 이미 코어가 정한 대상과 관계의 가독성을 돕는 image_plane.layout 후보. |
| 보류 | prop 소유 계약 없는 연구 27개, 연구 전용 맥락 30개. 추가 확인 변형 26개에는 hard 프로파일을 만들지 않음. |

운영 로드 결과는 112 슬롯, 9,783 후보, 1,564 시각 프로파일, 9,819 의미 인덱스 문서다. Gemini gemini-embedding-2 768차원을 사용했고, 기존 벡터 1,498개는 그대로 재사용했다. 대체 표현의 조건·출처·혼동 경계는 [INTEGRATION.md](INTEGRATION.md), [MAINTENANCE.json](MAINTENANCE.json), [INTEGRATION-AUDIT.json](INTEGRATION-AUDIT.json)에 연결된다. 박물관 원 도판을 직접 픽셀 검증한 범위로 확대하지 않았다.

## 실제 생성 결과

각 에이전트는 같은 사용자 원문을 유지하며, 저장된 무작위 seed로 서로 다른 키워드 조합을 선택하고 독립 baseline·core·구현 계획·픽셀 조건을 먼저 동결했다. 다른 arm의 프롬프트·이미지·결과를 컨셉 입력으로 사용하지 않았다. 세 번째 arm의 coordinator 메시지에는 심장 계량의 검토 관심 사항이 포함되어 완전한 맹검이라는 주장은 하지 않는다. 첨부 사진은 가상 성인의 보이는 얼굴·눈·단발 외형에 사용했다. 실제 신원·나이·신앙·신체 유사성·동의·사용자 선호를 판정하지 않았다.

| 독립 컨셉 | 실제 채택한 의미 | 최종 원본의 판정 |
|---|---|---|
| A: 자수와 광배의 현대 무대 리허설 | 거북과 감긴 뱀, 전신 만돌라의 새 프로파일 및 대응 구도. 두광은 동결 자체 조건으로 검사. | **FAIL**. 만돌라 하단 끝점이 신발 뒤에 가리고 발이 외곽선 아래로 나온다. 거북의 짧은 꼬리는 확인 불가. |
| B: 박물관 무대의 세이렌–키마이라 조우 | 인간–새 세이렌, 사자–염소–뱀 키마이라의 새 프로파일 및 대응 구도. | **FAIL**. 몸 연결과 꼬리는 읽히지만 세이렌 왼쪽 날개 바깥 깃털이 프레임에 잘린다. |
| C: 생명실이 끊어진 뒤 열린 문 | 보강된 모이라이 행위와 세계축 연결 후보. 마아트 소상 변형은 고정한 깃털 계량 장면과 달라 거절. | **FAIL**. 방적이 감긴 릴로 대체되고 실이 절단되지 않으며 소유자행 실이 분기한다. 심장의 동일 소유 표시와 토트 필기 접점은 확인 불가. |

ALL_OF의 필수 하나라도 빠지면 FAIL, 가려 확인할 수 없으면 UNOBSERVABLE이다. 여러 시도의 통과 부분을 합치지 않는다. coordinator도 저장된 native 원본을 따로 열어 확인했다. C의 세 역할 조건은 coordinator가 실제 방적·절단까지 요구해 더 엄격하게 FAIL로 평가했으며, 에이전트의 개별 카운트를 덮어쓰지 않았다. 전체 판정은 양쪽 모두 FAIL이다.

- A: [독립 결과](qualification/arm_a/RESULTS.md) · [최종 프롬프트](qualification/arm_a/standalone_prompt_attempt_2.txt) · [픽셀 원장](qualification/arm_a/pixel_review.json) · [coordinator 검토](qualification/arm_a/coordinator_review_attempt_2.json)
- B: [독립 결과](qualification/arm_b/RESULTS.md) · [최종 프롬프트](qualification/arm_b/standalone_prompt.txt) · [픽셀 원장](qualification/arm_b/pixel_review.json) · [coordinator 검토](qualification/arm_b/coordinator_review_attempt_2.json)
- C: [독립 결과](qualification/arm_c/RESULTS.md) · [최종 프롬프트](qualification/arm_c/standalone_prompt.txt) · [픽셀 원장](qualification/arm_c/pixel_review.json) · [coordinator 검토](qualification/arm_c/coordinator_review_attempt_02.json)

![A 최종 원본: 거북과 뱀 자수 및 광배](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/attempt_2.png)

![B 최종 원본: 세이렌과 키마이라](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/image_attempt_2.png)

![C 최종 원본: 세계축, 심장 계량, 모이라이](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/image.png)

## 생성 당시 소스와 최종 데이터 검증

총 6회 native image_gen 호출을 실제 수행했다. 각 arm의 프롬프트·runtime 감사는 PASS였고, 이미지 픽셀은 FAIL이었다. 첫 생성 이후 한 번 수정하는 범위로 평가했고 원래 첨부 사진과 참조 해시를 유지했다. [생성 당시 소스 스냅샷](native-generation-source-snapshot/MANIFEST.json)은 마지막 검색 조건 보강 전의 원본이다. 최종 데이터에서 새 native 이미지 호출은 하지 않았고, 기존 생성 binding·코어·프롬프트·이미지 바이트·실패를 소급 교체하지 않았다.

최종 같은 동결 코어에 대한 재검색에서 A/B의 네 새 구도 및 네 프로파일과 C의 두 보강 후보 모두 노출된다. [최종 소스 재검색](qualification/FINAL-SOURCE-REPLAY.json)은 retrieval 검증이며 final-source 픽셀 성공의 근거가 아니다. A의 ri_head_halo는 여전히 프로파일 목록에 없고 자체 두광 조건만 실제 픽셀로 검사했다.

검사 중 발견한 두 데이터 문제는 해결했다. 일반 찻잔/뷰티 요청에 관련 없는 도상이 섞이던 상태에는 신규 프로파일의 구성요소 확인 조건과 신규 후보의 특징적 코어 조건을 적용했다. 실제 연결 설명이 있는 세이렌·키마이라 본문에는 그 관계를 말하는 선택적 대체 표현을 추가했다. 전체 구성요소 그룹과 선택 후 픽셀 조건은 축소하지 않았다.

초기 전체 unittest 분할 검사에서 1,263개를 실행했고 회귀 실패 4개를 발견했다. 과거 merged-state 검사에는 나중에 추가된 대체 표현을 엄격히 분리해 역사적 비교를 유지했다. 사진 baseline 오류 3개는 통합 전 소스의 격리 재실행으로 원인을 확인하고 현재 기준을 v6로 추가했다. v1–v5 바이트, 오라클 및 과거 픽셀 실패 기록은 유지했다. 최종 변경 관련 검사와 추가 회귀는 final-verification-*.json 및 [VERIFICATION.json](VERIFICATION.json)에 기록했다. 초기 전체 검사와 최종 부분 재검증을 합친 증거이며, 최종 스냅샷에서 전체 suite를 다시 실행했다고 표현하지 않는다.

## 다음 개선의 적용 기준

- 만돌라·날개·꼬리: 외곽선의 끝과 팔다리가 실제 프레임 안에 있고 지지면에 가리지 않는 조건을 유지한다. 프롬프트의 여백 지시만으로 통과시키지 않는다.
- 모이라이: 같은 실의 생성·측정·절단·소유자를 한 연속 경로로 확인한다. 여러 붉은 줄이나 이미 감긴 릴을 대체 성공으로 인정하지 않는다.
- 계량 장면: 심장–깃털과 심장–마아트 소상 변형의 경계를 유지하고, 손·필기 도구·기록 표면의 접점과 동일 소유 표시를 실제 픽셀로 확인한다.
- 이후 이미지 개선은 새 실행 원장과 그대로 유지한 기준으로 재검사한다. 이번 결과로 전체 54개 프로파일 또는 80개 후보의 이미지 성능을 일반화하지 않는다.

코드·데이터·문서·원본은 작업 공간에 저장했다. 커밋·푸시·게시 작업은 수행하지 않았다.
