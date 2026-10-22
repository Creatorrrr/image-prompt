# SCP 데이터 반영과 독립 이미지 테스트

2026-10-22. 데이터 반영·검색 검증·기본 설치본 전환과 세 독립 이미지 테스트를 완료했다. 네이티브 호출 3회에서 이미지 3장이 반환됐다. 엄격한 전체 장면 합격은 0/3이며, 가시 관계의 일부 반영과 전체 장면 실패를 구분한다.

## 반영 범위

| 항목 | 결과 |
|---|---:|
| 시각 의미 카드 | 103 |
| 원 대화의 키워드 경로 | 268 |
| 새 선택형 시각 후보 | 69 |
| 새 문맥·진단·시간 설명 레코드 | 32 |
| 기존 후보 재사용 | 2 |
| 새 선택형 바인딩 | 145 |
| 기존 후보의 한국어 검색 표현 보완 | 1개 후보, 별칭 2개 |
| 전체 후보 / 바인딩 | 19,179 / 13,160 |
| 양성 검색 후보 / 실제 RID | 18,945 / 18,947 |

각 카드는 EN/KO 장면 의미, 소유 대상, 방향 관계, 관측 가능성, 혼동 경계, 출처·판본과 주장 한계를 보존한다. 32개 설명 레코드는 양성 이미지 재료 검색에서 제외했다. 특정 SCP의 능력·등급·기억·동의·인과·과거 사건은 외형만으로 확정하지 않는다. 구체적 장면 배치는 출처에 공식 디자인이 명시된 경우와 연구자가 저술한 선택형 실현을 구분한다.

실제 파일은 `skills/photo-prompt-image-generator/assets/`의 다음 항목이다.

- `photo_scp_semantics_20261022.json`: 103개 카드와 268개 경로, 기존 자료 재사용 판단.
- `photo_candidate_scp_20261022.json`: 새 시각 후보 69개와 진단 레코드 32개.
- `photo_candidate_scp_bindings_20261022.json`: 선택형 바인딩 145개.
- `photo_candidate_corpus_manifest.json`, `photo_candidate_search.json` 및 새 인덱스 폐쇄 집합.
- `photo_candidate_cosmic_horror_20261021.json`의 I08 대응 후보: 기존 원문·조건·효과·출처를 유지하고 한국어 검색 별칭 두 개만 추가.
- `retrieval-runtime.json`: 검증된 최종 검색 세대를 기본 설치본으로 지정.

후보는 선택 가능한 창작 재료다. 이번 등록은 완전한 native source/role 승인이나 자동 선택 권한을 부여하지 않는다. 이미지 실행은 `inspiration_only` / `skip` 판단을 기록하고 native chosen 배열을 비워 두었다.

## 검증과 설치 세대

원본/인덱스 정합성 검증, 실제 V4 소스의 V3 snapshot 일치, 설치본의 봉인·실행 환경 검사와 관련 회귀 테스트 96개가 통과했다. 기존 후보·바인딩·카탈로그·정책은 I08의 검색 별칭 보완을 제외하고 보존했다. 기존 CURRENT 파일, 첨부 이미지, 현재 SKILL.md의 바이트도 유지했다.

최종 기본 H-F2 세대:
`3e8e9f584fb06107a8d18ff9427151c2bb82da110658f70382f639261318e7df`

연결된 native source/index 세대:
`2c51083c75107eda987baf5561d54e4a926d2289f44f1292c502a52d548879d6`

세 이미지 테스트에 고정한 H-F2 세대:
`bfa3787341b3cd05e97e431acbb46f708c8e3fafb99e0e83f873e02c953fd65f`

두 SCP 세대의 차이는 **기존 I08 후보의 한국어 검색 별칭 두 개**다. 새 시각 후보 69개의 내용·조건·효과는 같다. 이미지 영수증을 최종 세대로 다시 쓰거나 재검색하지 않았다. 설치 세대의 커널과 임베딩 공간은 기준 세대와 동일하게 유지했다. 검색 임베딩은 로컬 EmbeddingGemma 2로 실행했다.

현재 스킬 경로: `.agents/skills/photo-prompt-image-generator/SKILL.md` → canonical skill.
SKILL SHA256: `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`.
참조 이미지 SHA256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.

## 실제 검색 결과와 한계

연구에서 저술한 78사례의 한·영 입력 156개에 대해 기준/후속 세대를 각각 검색했다. 38개 양성 사례는 카드와 함께 만든 **개발 세트**이며 독립 holdout은 확보하지 않았다.

| 평가 | 첫 SCP 세대 | 별칭 보완 후 최종 세대 |
|---|---:|---:|
| 한국어 지정 후보 top8 | 37/38 | 38/38 |
| 영어 지정 후보 top8 | 38/38 | 38/38 |
| 핵심 8개 관계군 × 2언어 top8 | 15/16 | 16/16 |
| 전체 양성 지정 후보 top32 | 76/76 | 76/76 |
| 대조 입력 중 새 후보가 top8에 나온 입력 | 32/80 | 32/80 |

처음 한국어 문서 검열 사례의 기존 후보가 10위였고, 상위 8개에는 의복 무늬·치아·다른 사물 등 다른 매개체가 나왔다. 기존 후보는 영어로 종이·인쇄 줄·부분을 덮는 불투명 직사각형을 충분히 설명했으나 한국어는 짧은 제목 중심이었다. 같은 의미를 한국어 별칭으로 보완한 뒤 1위가 됐다. 개발 결과를 본 뒤의 보완이므로 일반화 성능 개선으로 해석하지 않는다.

대조 입력의 노출 32건은 자동 채택 32건을 뜻하지 않는다. 부정·비교 문장을 포함한 검색에서 관련 물성이 노출될 수 있다. 80개 대조 입력의 최종 프롬프트 채택 검사는 실행하지 않았으며, 전체 top8 정밀도나 무단 채택률 0%를 주장하지 않는다. 별도 독립 요청·문맥 채택 평가가 후속 과제다.

## 세 독립 실행의 사전 설계

세 에이전트는 전체 대화를 전달받지 않는 별도 컨텍스트에서 현재 사용자 요청·실제 주제 문맥·참조 이미지·각자의 랜덤 시드를 받았다. 현재 스킬과 허용된 중립 precore만으로 서로의 프롬프트와 후보 자료를 보기 전에 핵심 장면을 동결했다. 임의 장면 설정은 사용자의 정확한 요구로 승격하지 않았다.

| 실행 | 독립 컨셉 | 생성 전 고정한 핵심 관계 | 새 SCP 재료 실제 노출 / 사용 |
|---|---|---|---|
| A | The Bell That Pulls the Dust Upward | 유리 후드 속 종·지지대·먼지 경로, 양손의 별도 접점, 중단된 교정 작업 | 5개 / G08 완성 장치·연관 분해 부품·사이의 펼친 기록 |
| B | Reverse Rain — Manual Isolation at the Hydrology Vault | 바닥 물·기둥·상부 수집기, 양손 휠, 경계를 가로지르는 연결 배관·셔터 | 1개 / R06 금속판 구멍·젖은 막·판 가장자리에서 바닥까지 연결 |
| C | Cold Bay: The Shadow Kept Its Place | 고리·빈 받침·등·떨어진 벽 그림자, 양손 차단대·바닥 접촉 | 5개 / I04 투명 용기 안의 작은 시료·지지대·벽과의 간격 |

각 실행은 유용한 두 슬롯과 topic/baseline의 **독립 검색 4회**를 실행했다. creativity 1의 현재 규칙은 질의별 top32에서 8개를 비복원 표본 추출한다. 실행별 32개 occurrence와 A 31 / B 31 / C 30개의 서로 다른 소스를 모두 읽고 판단했다. 이것은 개발 세트의 top8 수치와 다른 노출 단계다.

절차상 공개 사항: B는 사전 필수 memory registry 조회에서 중립 워크플로 포인터와 과거 주제명에 노출됐다. 이전 프롬프트·이미지·연구 카드·후보 파일은 열지 않았지만 엄격한 과거 정보 접근 0건으로 표현하지 않는다. A는 슬롯 ID 확인 과정에서 전체 coverage 140행을 생성했으며 각 행을 검토하고 실제 검색은 두 슬롯으로 제한했다. B의 작성자 메타데이터와 A/B의 clarification 필드 오류는 기록을 남기고 수정했으며, 그 수정으로 프롬프트를 바꾸거나 후보를 재표본하지 않았다.

각 실행의 테스트 JSON, 후보별 검토, 대안 비교, 최종 프롬프트, 감사, 호출 기록은 `generated/photo-runs/scp-{a,b,c}-20261022-*`에 보존한다. 부모는 이미지 호출 전에 세 원래 테스트케이스를 별도 복사하고 SHA256을 등록했다. 참조 이미지는 얼굴·단발·앞머리 등 보이는 외형의 지침이며, 실제 신원·나이·이력은 판정하지 않는다.

## 이미지 결과

세 에이전트가 첨부 참조 이미지를 실제 네이티브 호출에 포함해 각각 한 장을 생성했다. 부모도 반환된 세 파일을 직접 열어 원래 사전 테스트와 비교했다. 모든 실행은 재생성 없이 한 번에 종료했다. 얼굴·단발·앞머리의 인상은 세 장에서 유지되며, 실제 동일인 여부는 판정하지 않는다.

| 실행 | 관측한 반영 | 엄격한 미달 항목 | 판정 |
|---|---|---|---|
| A | 종·유리 후드·지지대·먼지 경로, 장치 오른쪽·부품 왼쪽·사이의 기록지 | 왼손 손바닥 접점과 닫힌 잠금 홈 불명확. 분해 부품 중 지지대가 받침과 붙어 있고 왼쪽 일부 잘림 | 전체 FAIL/partial. G08의 기본 배치는 확인되지만 더 강하게 정한 A6 완전 분해 사례는 FAIL |
| B | 양손 휠 접촉, 연결된 팔·지지 자세, 물/작업자 분리, 금속판 구멍과 젖은 막 | 물방울 방향은 하강으로도 읽힘. 배관-수집기 끝점이 위로 잘림. 젖은 막이 턱까지 이어지지만 실제 바닥 끝점 불명확 | 전체 FAIL/partial. R06 전체 관계도 FAIL |
| C | 분리된 고리와 벽 그림자, 양손 차단대·바퀴 접촉. 용기 안 시료·별도 지지대·간격 | 앞쪽 차단대와 오른쪽 패널을 잇는 힌지가 안 보이며 통로를 연속적으로 닫는 구조 불명확 | 전체 FAIL/partial. I04의 국소 가시 관계는 PASS |

**A의 G08 기본 배치 확인을 A6 합격으로 세지 않는다.** A6는 개별 부품을 완전히 분해하고 모든 필수 부품을 한 화면에 보여 주는 더 강한 사전 계약이었다. B의 managed 신체 동작 게이트는 통과했지만, 그 범위에는 배관 전체·수류 방향·R06 바닥 끝점이 들어 있지 않다. C의 I04 국소 PASS는 차단대의 전체 반응 관계나 시간에 따른 그림자 지속을 증명하지 않는다.

세 장 모두 임상적 시설·관찰 대상·작업자 행동이 읽힌다. A/C는 변칙적 공간 배치도 시각적으로 읽히지만, B는 수류 방향의 구별이 부족하다. 이미지 한 장은 역중력·변칙 원인·장치의 효능·시간에 따른 변화·실제 안전을 입증하지 않는다. baseline 이미지를 별도로 생성하지 않았으므로 자료 추가의 인과적 품질 향상을 주장하지 않는다. 사용자 수용은 아직 확인하지 않았다.

실제 테스트 결과는 `photo_scp_semantics_20261022.json`의 G08/R06/I04 카드에 범위를 명시한 `post_registration_evaluation_refs`로 연결했다. 등록 당시의 상태는 `pixel_status_at_registration`에 보존하고, 현재 `pixel_status`는 위 국소/부분 판정으로 갱신했다. 설치본에 봉인된 후보 원문·해시와 원 연구 증거는 유지했다. 후보 안의 연구 메타데이터는 등록 시점의 snapshot이며, 최신 평가 상태는 별도 의미 레지스트리와 영수증을 읽어야 한다.

| 실행 | 최종 프롬프트 | 실제 이미지 SHA256 |
|---|---|---|
| A | [final-prompt.txt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/scp-a-20261022-8757a1/final-prompt.txt) | `da7466fdb104b504c83c386654a37f085b6401abc9184bc5c4dec68f18e9427e` |
| B | [final-prompt.txt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/scp-b-20261022-3d75a9/final-prompt.txt) | `40667cb19611d5466cd7ccb466d26e85c6f2fae0d352ef01e697a69bab7598e4` |
| C | [final-prompt.txt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/scp-c-20261022-cc1d54/final-prompt.txt) | `edd7a24ceef954595663818c5349907fd985a87d26a254c2c8397d543f47fbcd` |

A — The Bell That Pulls the Dust Upward

![A 이미지](/Users/chasoik/Projects/image-prompt/generated/images/scp-a-bell-20261022-8757a1/scp-a-bell.png)

B — Reverse Rain — Manual Isolation at the Hydrology Vault

![B 이미지](/Users/chasoik/Projects/image-prompt/generated/images/scp-b-reverse-rain-20261022-3d75a9/result.png)

C — Cold Bay: The Shadow Kept Its Place

![C 이미지](/Users/chasoik/Projects/image-prompt/generated/images/scp-c-shadow-kept-20261022-cc1d54/image-1.png)

## 결과를 반영한 후속 우선순위

이번 데이터와 모델의 렌더 실패를 혼동하지 않는다. 끝점·가림·부분 충족을 검사하는 조건은 이미 데이터에 있고, 실제 실패도 그 조건으로 검출했다. 생성 실패를 덮기 위해 출처 의미를 줄이거나 비슷한 후보를 중복 등록하지 않았다.

1. A형 장면은 좌우 부품 전체와 손바닥·잠금 홈을 크게 보이는 구도로 미리 배치한다. 완전 분해가 필요하면 각 분리 부품과 접점을 단순한 동선으로 만든다.
2. B형 장면은 배관의 출발·경계 통과·도착과 젖은 막의 실제 바닥 끝점을 프레임 안에 확보한다. 정지 프레임의 방향 단서는 별도 검사하고, 실제 역방향 운동 검증은 순차 프레임 과제로 둔다.
3. C형 장면은 연속된 한 차단대의 힌지·패널·바퀴를 모두 보여 주어 폐쇄 동작의 경로를 읽히게 한다.
4. 검색의 후속 검증은 이번 카드에서 유도하지 않은 자연 요청을 별도로 고정하고, 일반/비가시 문맥의 실제 최종 채택까지 평가한다. 새 자료 노출과 안전한 문맥 판단을 각각 측정한다.

위 내용은 후속 개선 계획이며 추가 이미지 호출·동영상 생성·재시험은 실행하지 않았다.

## 증거와 재현 경계

- [데이터 보존·실제 등록](integration-evidence/data-validation.json)
- [최종 개발 검색 전체 결과](integration-evidence/search-development-results.json)
- [첫 검색 결과와 미달 사례](integration-evidence/initial-search-development-results.json)
- [검색 보완의 의미 검토](integration-evidence/recall-repair-review.json)
- [출시 범위와 보류한 주장](integration-evidence/search-qualification-review.json)
- [기본 설치본 전환](integration-evidence/installed-activation.json)
- [실행 환경 검증](integration-evidence/active-runtime-validation.json)
- [실제 이미지 실행의 후보 노출](integration-evidence/actual-exposure.json)
- [호출·프롬프트·참조·84개 워크플로 파일 해시 대조](integration-evidence/image-test-summary.json)
- [의미 카드에 연결한 사후 평가](integration-evidence/semantic-evaluation-registration.json)
- [A 실행 결과](integration-evidence/arm-a-result.json), [B 실행 결과](integration-evidence/arm-b-result.json), [C 실행 결과](integration-evidence/arm-c-result.json)
- [원 테스트케이스의 부모 사전 등록](integration-evidence/parent-pre-image-registration.json)
- [부모의 A 픽셀 판정](integration-evidence/parent-pixel-review-a.json), [B 픽셀 판정](integration-evidence/parent-pixel-review-b.json), [C 픽셀 판정](integration-evidence/parent-pixel-review-c.json)
- [회귀 테스트 96개](integration-evidence/regression-tests.log)

초기 연구의 `VALIDATION.json`은 당시의 구조 검증·기준선 이동 기록으로 보존했다. 이번 반영의 증거는 이 문서와 `integration-evidence/`다. 소스 출처와 판본·권리 경계는 [RESEARCH.md](RESEARCH.md), [sources.json](sources.json), [LICENSE-NOTE.md](LICENSE-NOTE.md)에 있다.

이번 작업은 커밋·푸시를 실행하지 않았다. 작업 중 HEAD가 `dcce9c3...`에서 `c6f7449...`로 이동한 별도 dark-fantasy 커밋을 관측했지만, 이 작업의 SCP 모듈은 HEAD manifest에 없고 변경된 작업 파일에 보존돼 있다. 기준선에서 기존 파일의 바이트와 전체 후보·바인딩을 대조해 무관한 작업을 보존했다. 향후 커밋 시 기존 미추적 cosmic 모듈의 I08 별칭 두 개와 공유 manifest/index/runtime 변경의 범위를 다시 분리해야 한다.
