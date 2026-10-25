# 스포츠 후보 실제 활용 재검증

## 이전 활용 확인

이전 A/B/C의 실제 최종 composed object, 발행 material sources와 query별 결정 기록을 대조했다. 새 후보의 직접 활용은 **세 팔 모두 0개**였다. A에는 R02·R03, B에는 S01·S03·S04가 제시됐고, C에는 새 스포츠 후보가 제시되지 않았다. 세 최종 프롬프트는 각자의 독립 baseline과 SHA-256까지 같았다. [검증 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/prior-use-audit.json)

검색 순위 창, 실제 제시, 검토, 최종 문구 기여와 저장 픽셀은 각각 다르다. 이전 두 반환 이미지에 스포츠가 보인다는 사실은 새 후보가 사용됐다는 증거가 아니었다.

## 원인과 보강

1. 기존 시각 후보 100개에는 세 구성군·소유 그래프가 연구 메타데이터로 있었으나 실제 `concept_units`, `relations`, `keywords` 검색 필드는 비어 있었다. 기존 시각 문구는 검색됐지만, 구성 요소와 관계의 개별 의미 필드가 기여하지 못했다.
2. 이전에 제시된 새 후보 일부는 다른 단계·종목이거나 기본 구상에 이미 있던 내용이었다. 양궁의 컴파운드 소스, 수영의 수중·접영 단계처럼 구체적인 전체 의미가 맞지 않는 소스는 적절히 제외됐다. 독립 기본안을 선호한다는 이유로 호환 가능한 실험 대안도 렌더되지 않았다.
3. 계주의 새 A04는 순위 창에 들었지만 실제 표본에는 뽑히지 않았다. 이 동작 자체는 오류로 간주하거나 최신 후보를 우대하도록 수정하지 않는다.

### 적용한 변경

- 기존 100개 후보의 en/ko 전체 시각 문구, 원래 조건·효과·출처·적용 경계는 보존했다.
- 구성 요소와 소유 관계를 실제 positive 검색 필드에 명시하고, 중복된 definition은 종목·단계의 한정된 정의로 바꿨다. 한국어 카드명과 종목명은 lookup 단서이며 강제 활성화가 아니다.
- 조합 가능한 장비 구조 후보 6개를 추가했다: 사이클 후드/레버, 물통/케이지, 피겨 부츠/날 접점, 부츠 끈 경로, 깃털 셔틀 구조, 라켓 구조. 모두 세 관찰 구성군과 명시적인 부분 경계·해석 한계를 갖는다.
- 진단 기록 330개는 변경하지 않았다. 전체 native 승인이나 픽셀 승인도 부여하지 않았다.
- 검색 코드·모델·가중치·샘플링 정책은 바꾸지 않았다. 발행되지 않은 CID를 프롬프트에 수입하지 않는다.

[검색 필드 전후](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/search-field-enrichment.json): 구성 의미 0→636, 명시 관계 0→328, lookup 0→212개. 이 수치는 원래 문구에 없던 모든 지식이 새로 생겼다는 뜻이 아니라, 실제 검색 필드로 옮긴 단위의 수다.

### 자료의 한정된 확인 범위

- [Shimano 부품 매뉴얼](https://si.shimano.com/en/pdfs/um/07R0B/UM-07R0B-002-ENG.pdf): 브래킷 커버와 레버 부품 구분. 선택한 손 위치는 저작 제안이다.
- [Elite 물통 케이지](https://www.elite-it.com/en/bottle-cages/carbon/vico-carbon): 물통을 감싸는 케이지 구조. 실제 튜브 배치와 구도는 저작 제안이다.
- [Riedell 2023 카탈로그](https://ice.riedellskates.com/Portals/2/images/ice/content-page-graphics/downloads-page/IceCatalog_2023_WebDisplay.pdf): 부츠 밑창/굽과 날 마운트 구분. 현행 경기 적합성 자료가 아니다.
- [Riedell 끈 안내](https://ice-blog.riedellskates.com/how-to-lace-ice-skates/): 아일릿·훅의 구분. 보이는 끈만으로 착용 안전성이나 편안함을 주장하지 않는다.
- [Yonex 깃털 셔틀](https://yonex-fareast.com/product/aerosensa-20/): 이 깃털·코르크 변형의 재질. 모든 셔틀의 재질로 일반화하지 않는다.
- [BWF 2016 구조도](https://system.bwfbadminton.com/documents/folder_1_81/Regulations/Laws/Part%20II%20Section%201A%20-%20Laws%20of%20Badminton%20-%20June%202016%20Revised%202.pdf): 라켓 머리·스트링·샤프트·손잡이 구분에만 사용한 역사 자료다.

접근 수준(본문/PDF 또는 검색 발췌)과 출처 범위는 [출처 레지스트리](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/supplemental-sources.json)에 보존했다. 부품 자료가 사진 전체의 사실성이나 원생 의미 승인을 대신하지 않는다.

## 새 테스트 설계

새 직접 사용자 요청을 원문 그대로 바인딩하고 이전 스포츠 주제·참조 이미지 사용을 이어받았다. 이전 세 종목을 모두 똑같이 제외한 중립 목록에서 시드를 고정해 사이클·피겨·배드민턴을 추출했다. 새 독립 서브에이전트 세 개는 서로의 자료와 보강 데이터를 보기 전에 baseline, 최소 사용자 의미, 특징 선택, 신체 검토, testcase와 슬롯 의도를 동결했다. 세부 종목·단계·옷·구도는 사용자 고정 조건으로 승격하지 않았다.

이번 목적은 **후보를 사용한 유효 실험 변형을 실제 실행할 수 있는지**다. 장비 후보 6개는 새로 고른 세 종목의 국소 구조 범위를 보강했다. 종목 전체·330개 경로 전체의 일반적인 검색 성공률을 추정하는 표본은 아니다. 정상 발행 자료 안에서 조건과 전체 의미가 맞는 변형을 완성하고, 기본안과의 정확한 문구 차이·소스 CID/RID/hash·관찰 타깃을 보존한다. 그 변형의 예술적 우월성이나 데이터 추가의 독립적인 인과 효과를 가정하지 않는다. 부적합 후보 강제 삽입·조건 절단·unissued CID 사용·시드 재추첨은 하지 않는다. 합당한 변형이 없으면 활용 0을 기록한다.

기본 스킬과 컨트롤은 유지한다. 후보 ID는 H-F2의 `inspiration_only` 증거로 기록하며 native chosen 목록에는 넣지 않는다. 각 새 테스트는 참조를 실제 전달하는 native `image_gen` 1회와 원본 관찰을 수행한다.

## 검증 상태

- 의미·실제 검색 필드 회귀 검사 22개 PASS.
- 전체 canonical source 검증 PASS. 기존 설치 후보 23,596개 중 관련 없는 23,496개는 정확히 보존했다. 스포츠 100개만 검토된 의미 필드로 보강했고 새 스포츠 6개와 동시 작업의 새 기록 21개를 합쳐 23,623개를 검증했다.
- 전체 슬롯 카탈로그·기존 연결·정책 보존. 실행 커널 변경 없음.
- 작업 저장소 검색 인덱스 `34c9f22013e985bb118e6bf5e3b09ec9c6d9abd6dc0682f1233e09349b80ba9f` 활성화 PASS. 기존 샤드 삭제 0개.

- 설치된 H-F2 실행본 `f5905cd6954bd25e4d396d58ce7cbb4ceda1ed94e971c1001a5bf849c961a940` 활성화 및 실제 런타임 확인 PASS. 기존 코드 해시는 유지했다. [설치 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/installation.json)
- 설치 후 전체 authored module 목록과 바이트 해시가 검증 당시와 같고 동시 작업의 추가 21개도 보존됨을 확인했다. [보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/post-installation-preservation.json)
- 새 실제 발행 자료: A 39개 소스/48회 노출 중 스포츠 6개(U01·U02 포함), B 35개/40회 중 스포츠 7개(U03·U04 포함), C 32개/40회 중 스포츠 10개(U05·U06 포함). U01–U06 여섯 후보가 모두 정상 발행 자료에 들어왔다. [직접 집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/retest-issued-source-audit.json)

## 실제 활용 검증 결과

**이전 0/3팔 → 이번 3/3팔에서 실제 최종 문구 기여를 확인했다.** 세 기본안의 바이트는 그대로 보존됐고 세 최종안은 각각 달라졌다. 부모가 관리형 구성 object에서 전체 128개 query/CID/RID/source-hash 결정을 실제 발행 자료와 대조해 일치를 검증했다. 단지 설명에 ID를 붙인 것이 아니라 아래에 적힌 새로운 구조·관계가 실제 도구 프롬프트에 추가됐다. [부모 직접 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/retest-actual-use-audit.json)

| 팔 | 실제 활용 소스 | 기본안에 추가된 실질 내용 | 실제 활용/발행 노출 |
|---|---|---|---:|
| A 사이클 | U01·U02 | 손바닥-후드·별도 레버와 손가락의 국소 관계, 프레임에 붙은 케이지-물통-노출된 목/뚜껑 | 2개 / 39개 고유 소스·48회 |
| B 피겨 | U03 | 부츠 밑창·굽 → 마운트 → 좁은 날 → 얼음 접점의 분리, 밑창이 얼음 위에 남는 구조 | 1개 / 35개·40회 |
| C 배드민턴 | D01·U05·U06 | 라켓을 든 쪽 앞발 소유, 셔틀의 둥근 베이스·깃대·벌어진 끝, 닫힌 라켓 림·교차 스트링·감긴 그립 | 3개 / 32개·40회 |

활용한 여섯 고유 소스 중 **5개는 이번에 추가한 장비 후보, 1개(D01)는 기존 스포츠 후보의 보강본**이다. U04 끈 후보는 제시됐지만 최종안에 쓰이지 않았으므로 활용 0으로 남긴다. 최종 채택은 H-F2 `inspiration_only`의 실제 문구 기여이며, 계약적 native chosen 두 목록은 모두 빈 배열이다. 이를 native 승인이나 전체 코퍼스 승인으로 바꾸지 않았다.

최종 도구 프롬프트 SHA-256은 A `c8187b6a0dd7eb7c4d9a44e7df1612cb428fd35a3f6373f154073358bd514ea1`, B `30f0464247e3c491a7f65e89ee6163748ea868ad47d4f15ff8adddfacb7a4cc6`, C `46ddbfe145579ec217020782bde2777745f51d66c2eb33eda2b94521b7e7b347`이다. 세 manifest와 각 1행 ledger, 실제 참조 파일 SHA, runtime request를 대조했다. 세 팔 모두 참조 SHA `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`가 일치했고 네이티브 생성은 각 1회, 반환 원본은 3장이다.

작성 이후 보존된 스킬 실측과 최종 실행/검토 스킬은 `d666eb93c9335508f0e5db27efa90b8915e9638eeda694703de05df8a0446957`이다. 최초 읽기의 바이트 스냅샷이 없는 팔에서는 그 최초 시점까지 암호학적으로 증명한다고 주장하지 않는다. 각 팔의 원본 선언을 기준으로 기록했으며 부모 초기 요약의 다른 해시를 소급 기록하지 않았다. 실행은 위 f590 설치본에 고정했다. A의 초기 발행 상태 확인 시도는 원래 발행 lock의 종료를 기다린 후 이미 bound인 증거를 검증한 것뿐이다. 두 번째 검색·추첨·issue·commit은 없었다.

## 원본 픽셀 검증

부모도 세 원본을 직접 열어 에이전트의 평가와 대조했다. **픽셀에서 전체 엄격 통과는 피겨 1/3팔**이다. 이미지 생성 성공·문구 활용 성공과 픽셀 전체 통과를 분리한다.

| 팔 | 선택 소스의 세부 구성군 | 완전 관찰된 소스 | 신체·지지·투영 게이트 | 엄격 결과와 한계 |
|---|---:|---|---:|---|
| A | 5/6 | U02 3/3; U01 2/3 | 1/5 | FAIL. 손가락이 별도 레버 옆에 놓인 전체 관계는 가림. 바퀴 접지·페달·신발 하단과 헬멧 윗부분도 프레임 밖 |
| B | 3/3 | U03 3/3 | 5/5 | PASS. 밑창/굽·마운트·하나의 날·얼음 접점이 동시에 보임 |
| C | 6/9 | U06 3/3; D01 1/3; U05 2/3 | 4/5 | FAIL. 앞발/라켓이 네트 쪽이라는 공간 관계를 입증하지 못함. 셔틀의 넓은 끝은 측면 팬처럼 보여 열린 원뿔 입구/깊이까지 완전 관찰되지 않음 |

C에서는 라켓 손과 앞발이 같은 쪽이라는 사실만으로 D01을 통과시키지 않는다. 원래 구성군의 `toward the net`, `near the net`까지 확인해야 한다. 부모의 초기 관찰은 이 정확한 공간 조건을 빠뜨렸고, 정확한 카드 문구 대조 후 정정했다. 초기 기록도 superseded로 보존했다. U05의 측면 윤곽 또한 열린 끝을 자동 증명하지 않는다. 이들은 관찰 부족이며 장비 결함·불법 동작·운동 능력·의도를 단정하지 않는다.

B의 부츠 윗부분은 흰색, 밑창·굽은 갈색으로 생성됐다. 최종 저작 문구의 색상과 작은 차이가 있으나 U03 소스는 밑창 색상을 요구하지 않으므로 구조 게이트와 별도로 기록했다. 세 장 모두 참조의 짧은 검은 머리·앞머리·눈·얼굴 비례의 외관 대응은 보이며, 신원 인증으로 해석하지 않는다.

### 원본과 상세 근거

- A: [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/a/original.png), [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/a/authored/final-prompt.txt), [소스·정확한 변경](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/a/authored/utilization-report.json), [비교안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/a/authored/composition-comparison.md), [원본 평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/a/authored/source-pixel-review.json).
- B: [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/b/original.png), [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/b/authored/final_prompt.txt), [소스·정확한 변경](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/b/authored/utilization.json), [보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/b/authored/arm-report.md).
- C: [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/c/original.png), [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/c/authored/final_prompt.txt), [소스·정확한 변경](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/c/authored/utilization-evidence.json), [보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/c/authored/final-report.md).

## 운영 반영과 해석 한계

[새 활용·픽셀 레지스트리](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/registries/photo_sports_fiction_utilization_evidence_20261025.json)에 source CID/RID/hash, 최종 프롬프트 SHA, 이미지 SHA, 구성군 관찰과 전체 기술 판정을 기록했다. 기존 픽셀 레지스트리의 최초 세 팔과 차단 증거는 그대로 보존하고 이 후속 근거만 연결했다. 레지스트리는 positive 후보 검색에 들어가지 않으며 native 승인도 바꾸지 않는다.

이 결과는 실제 활용 경로가 작동함을 증명한다. 이전과 종목·구도·후보 사용 실험의 선택 목적이 달라졌고, 동일 기본안의 대조 이미지가 없으므로 데이터 추가가 미적 품질을 개선했다고 추정할 수 없다. 전체 102개 조사 카드·330개 경로·100개 기존 시각 후보의 원생 승인으로 일반화하지 않는다. 사용자 판단은 모두 pending이다.

남은 국소 실패는 다음 관련 검증에서 명시적인 공간/가시성 관찰 대상으로 유지한다. 사이클은 전체 바퀴·페달·신발 여백과 손가락-레버 투영을 동시에 확보해야 한다. 배드민턴은 카메라·선수·네트의 앞뒤 순서를 먼저 정의하고, 셔틀 열린 끝을 관찰할 수 있는 각도를 별도로 확보해야 한다. 후보명·동의어를 늘리거나 이미 제시된 후보를 더 강하게 활성화하는 문제로 바꾸지 않는다. 이번 재시험의 최초 세 원본과 실패 기록은 그대로 남긴다.


### 최종 동시 작업 보존 확인

이미지 시험은 f590에 바인딩된 증거다. 마무리 중 다른 작업이 기본 실행본을 `0c489235e02de580bfca1a76fdf1ea35b6fa070748c9ee13b301a61c65ee4c21`로 갱신했다. 두 실행본의 **전체 H-F2 candidate source SHA-256가 동일**하고 스포츠 canonical 소스와 bindings도 바이트까지 같음을 확인했다. 코드 차이는 `scripts/prepare_retry_context.py` 하나이며 이번 시험은 재시도를 사용하지 않았다. 새로운 기본 실행본의 코드까지 이번 픽셀이 시험했다고 확대 주장하지 않는다. 다른 작업의 새 fashion module 두 개도 보존했으며 기존 module 파일 해시의 변경은 없다. [검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/concurrent-runtime-advance.json)

운영 근거 연결 후 최종 스포츠 회귀 검사 22개 PASS. [최종 보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/final-preservation-and-evidence-check.json)
