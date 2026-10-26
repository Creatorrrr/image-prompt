# ReactorPrompt 의상·패션 수집 및 보강

상태: 키워드·의미 카드·후보 등록, 작업 폴더 검색 검증, 기본 설치 버전 전환 및 한·영 조회 진단 완료.

최종 상태 확인: 2026-10-25 21:27 KST. 선택 버전과 원본·인덱스 일치, source update 종료(`editing:null`, epoch 194)를 확인했다. 커밋·푸시는 하지 않았다.

## 수집 범위

2026-10-25 18:15 KST에 동결한 `reactor-prompts-magazine.pages.dev` 아카이브를 기존 두 수집본과 비교했다. 기존 게시물 ID와 본문·이미지가 이어지므로 기존 ReactorPrompt 수집의 증분 원본으로 사용했다. 예전 Vercel 주소는 확인 당시 `DEPLOYMENT_DISABLED`였다.

- 현재 사이트 목록: 4,596개 게시물, 19,736개 이미지.
- 새 게시물 수집: 1,849개, 이미지 8,057개. 새 게시물 중 본문이 있는 것은 1,042개, 사이트 원문이 비어 있는 것은 807개다.
- 기존 게시물의 이미지 829개와 본문 17개를 별도로 비교·보충했다. 역사적 본문을 새 원문의 빈 값으로 덮어쓰지 않았다.
- 의상 추출 입력: 수집본의 프롬프트 파일 4,613개 중 비어 있지 않은 3,335개와 번역 캐시 2,872개. 번역 래퍼의 원문 블록을 사용하고 동일 본문을 합쳐 2,974개 문서를 만들었다. 다른 시점의 서로 다른 본문은 보존했다.

원문·이미지와 전체 위치 정보는 gitignore된 `generated/trend-scout/raw/`에 보존한다. 번역 래퍼 자체는 한국어 의미의 증명이 아니며, 새 한·영 후보 설명은 별도로 작성·대조한다.

## 추출 결과

Luna max 서브에이전트 4개가 문서를 분담하고, 별도 에이전트가 누락·중의성 검토, 데이터 통합, 검색 반영을 맡았다. 문서 2,974개를 모두 처리해 20개 분류의 표현 2,556개를 모았다.

| 분류 | 표현 수 | 분류 | 표현 수 |
|---|---:|---|---:|
| 의복 | 897 | 액세서리 | 196 |
| 재단·디테일 | 178 | 색·표면 마감 | 139 |
| 신발 | 126 | 장신구 | 125 |
| 헤어·메이크업 | 118 | 스타일·미감 | 117 |
| 직물 조직 | 109 | 소재 | 88 |
| 핏·실루엣 | 86 | 의복 상태 | 70 |
| 무늬 | 51 | 양말·스타킹 | 48 |
| 가방 | 45 | 여밈 | 41 |
| 머리쓰개 | 37 | 브랜드 맥락 | 35 |
| 착용 동작 | 30 | 레이어링 | 20 |

정규화는 유니코드 NFKC, 대소문자, 공백, 대시 차이로 제한했다. 비슷한 단어를 자동으로 같은 뜻이라고 합치지 않았다. 하나의 의복을 설명하는 수식어 결합은 보존하되 쉼표로 연결된 서로 다른 물건을 한 표현으로 만들지 않았다.

정확한 원문 위치에 대한 용어 부여는 51,771건이며, 서로 다른 위치는 49,974개다. 같은 위치에 일반어와 복합어가 함께 걸릴 수 있어 두 수치는 다르다. 긍정 48,694건, 금지·부정 1,537건, 맥락상 언급 1,528건, 불확실 12건을 구분했다. 빈도는 중복 제거된 문서 기준이며 웹 게시물 수나 이미지 수가 아니다.

## 검토와 한계

모든 문서의 coverage, 원문 해시, 문자 위치, 용어 참조를 검증했다. 별도 검토에서 76개 표면형의 1,348개 출현을 점검했고, 기존 추출과 겹치지 않은 443건을 의복 관련 350건 보충, 비의복 61건 제외, 불확실 32건 보류로 나눴다. 20개 분류와 긍정·부정·맥락을 나눈 60개 층화 표본도 대조했다.

중앙 수리 17건은 삭제 12건과 polarity 변경 5건이다. 예를 들어 호박의 `ribbed`, 차내 재질의 `worn`, 촬영 구도 목록의 `레이어드`는 의상 용례에서 제외했다. 원래 서브에이전트 출력은 동결하고 수리 요청·이전 값·적용 결과를 별도로 기록했다.

이는 전체 문서 처리와 특정 누락·오분류 검토를 확인한 결과다. 모든 의상 표현의 의미와 소유자를 빠짐없이 정확하게 추출했다는 보증이나 통계적 정밀도 추정은 아니다. 보류 항목은 새 긍정 후보의 근거로 사용하지 않는다.

## 의미·후보 반영

새 의미 카드 34개, 후보 34개, 슬롯 binding 34개를 추가했다. 구성은 전체 착장 15개, 헤어·메이크업 2개, 소재·구조 6개, 희귀 의복·구성 11개다. 한복 치마의 패널·주름, 옥스퍼드 조직과 면 섬유의 구분, 한 패널에 한정된 무늬, 홀터톱과 헤드스카프의 동일 프린트, 비대칭 시폰 드레이프, 프린트에만 한정된 바램 등을 원문 근거로 작성했다.

각 카드에는 한·영의 완전한 제안문, 가시 형태·관계, 소유자, 조건·효과, 혼동 경계와 정확한 긍정 출현 근거를 남겼다. 카드 근거는 538개다. 별도 서브에이전트가 34개 전부를 대조해 번역·관계·조건·효과 관련 발견 17건을 해결했으며 미해결 건은 없다. 이 17건은 추출 목록의 중앙 수리 17건과 다른 검토다.

전체 2,556개 표현에는 다음과 같이 명시적인 처리 경로를 부여했다. 단어가 일치한다고 전체 후보의 뜻이 동일하다고 취급하지 않는다.

| 처리 경로 | 표현 수 |
|---|---:|
| 원문상 긍정 근거가 새 선택 후보를 뒷받침 | 306 |
| 긍정 시각 어휘로 보존하되 단독 후보를 만들지 않음 | 2,001 |
| 헤어·미용 어휘로 보존하되 일치하는 원문 절이 없어 단독 후보를 만들지 않음 | 113 |
| 맥락상 언급만 있음 | 53 |
| 부정·금지 용례만 있어 진단용으로 보존 | 20 |
| 브랜드 참조로만 보존 | 33 |
| 정적 의복 속성이 아닌 동작 | 30 |

기존 의류 역할 후보 3,552개를 대조했다. 최종 자산에 기록한 비교는 native `2884a17d…`/H-F2 `f5905cd6…`의 역사적 snapshot 기준이며 현재 설치 membership 주장으로 사용하지 않는다. 비교 lead 32개는 전체 의미 동등성이나 재사용 승인을 부여하지 않았고, 새 binding에 기존 CID dependency는 없다. 이름만으로 매듭 형상을 알 수 없는 taiko musubi 등은 보류했다.

작업 manifest에는 최신 기존 129개 모듈을 보존하면서 새 후보·binding 모듈 두 개만 추가했다(총 131개). 등록 직전·직후 기존 모듈의 해시가 모두 동일함을 확인했다. 다른 작업의 변경을 과거 수집 기준으로 원복하지 않았다.

키워드 관찰, 기존 후보와의 의미 동등성, 검색 노출, 실제 후보 채택, 이미지 품질과 사용자 수용은 서로 다른 판정이다. 이번 새 제안은 native 승인이나 픽셀 품질 증명을 만들지 않는다.

## 검색 검증

작업 폴더 V3 인덱스의 공식 `--verify`와 전체 사전 검사가 모두 통과했다. 후보 23,657개 중 긍정 21,646개를 담으며, binding은 18,621개다. 첫 갱신에서 기존 벡터 21,612개를 재사용하고 새 34개를 로컬 EmbeddingGemma로 계산했다. 이후 병행 작업의 스포츠 모듈 변경을 보존해 다시 갱신했으며, 이때 21,646개 벡터를 모두 재사용했다. 최종 layout은 `27527cafa266a6dc5b0fd5f584565b095d30d4395699cf4be373d1a5d4f4b112`이고 현재 원본 corpus SHA와 일치한다. 두 번째 갱신 직전·직후 등록된 모듈·코드의 해시가 같고 source update가 정상 종료된 것을 확인했다.

초기 전체 V3 사전 검사는 이번 추가분 밖의 스포츠 데이터 `cand_f5c5596c36a15042b5daef110b98f5ce`의 기존 `relations` 형식 오류를 보고했다. 병행 스포츠 작업의 수정 후 최종 작업 폴더 V3 전체 사전 검사는 통과했다.

설치 기준으로 고정한 V4 snapshot에는 그 수정이 아직 없어서 `cand_007db1a9c5a552a3a1c16dbbaa6d0e1e`의 같은 종류 오류가 남아 있다. 관계 행이 `subject/predicate/object` 구조여서 필수 `id/type` 형식과 맞지 않는다. 이는 검사에서 보고된 사례이며 전체 오류 개수의 전수 집계가 아니다. 해당 [고정 snapshot의 스포츠 모듈](/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations/409e65bb548578f4b995b530a8ea4ba906120b3102c57f89c8e455d4e165a544/assets/photo_candidate_sports_fiction_20261025.json)은 그대로 보존했다. 새 의상 모듈의 독립 검사와 소스·인덱스 무결성 검증은 통과했지만, 설치 snapshot의 전체 사전 검사까지 통과했다고 주장하지 않는다. 작업 폴더의 다른 미발행 코드·데이터를 이번 패션 변경과 함께 설치하지 않았다.

기존 설치 코드 112개 파일과 기존 검색 RID 21,614개·벡터를 그대로 보존해 새 후보 34개를 추가했다. 새 H-F2 버전은 `d27a09ba46f95a228189cd1025b1fcea922ac1b39fa3480eb441882a6f2d5d73`, 연결된 native 버전은 `ec205b351a70ef3bad3eab981ab14131f90bade1efb32cbe46b4c437e4cfe96e`다. H-F2에는 긍정 CID 21,646개와 RID 21,648개가 있다. 설치·명시 버전 무결성 검사 후 기존 기본 버전이 바뀌지 않았음을 확인하고 새 버전으로 전환했다. 전환 후 기본 runtime 검사와 workflow 도움말 dispatch도 통과했다. 이미지 생성과 외부 유료 embedding API는 호출하지 않았다.

새 CID 34개에 대해 원문에서 고른 짧은 키워드를 한국어·영어로 68번 조회했다. 21,646개 전체 CID 중 상위 8개 결과에 해당 새 후보가 포함된 것은 3건(영어 1/34, 한국어 2/34)이었다. 모든 CID가 전체 순위 어딘가에 포함된다는 사실은 전체 pool 검색의 성질이므로 검색 성공 근거로 사용하지 않는다. 이 진단은 실행·인덱싱 smoke이며, 새 후보가 일반적인 짧은 질의에서 우선 검색된다는 보증이나 후보 채택·이미지 품질의 증명이 아니다.

추가로 각 카드의 실제 한·영 제안문을 사용한 68개 조회에서는 68개 모두 해당 후보가 1위로 검색됐다(영어 34/34, 한국어 34/34). 따라서 새 내용의 한·영 인덱싱과 조회는 확인했지만, 같은 제안문을 다시 질의한 진단이므로 독립적인 검색 품질 평가로 해석하지 않는다. 모든 조회는 로컬 encoder를 사용했고, 진단 중 기본 버전이 바뀌지 않았음을 확인했다.

## 결과 열기

- [추가 게시물 목록](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-export-20261025-pages-incremental/comparison-new-posts.csv)
- [증분 수집 결과](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-export-20261025-pages-incremental/final-report.ko.md)
- [전체 키워드 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/exports/fashion-keywords.csv): 2,556행. 영문·한국어, 분류, 관찰형, 문서 빈도, polarity와 후보 연결을 포함한다. 근거 문서 ID는 셀 크기를 제한하기 위해 처음 5개만 표시한다.
- [전체 키워드 JSON](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/exports/fashion-keywords.json): 모든 근거 문서 ID와 처리 경로를 보존한다.
- [시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_reactorprompt_fashion_semantics_20261025.json)
- [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_reactorprompt_fashion_20261025.json)
- [슬롯 binding](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_reactorprompt_fashion_bindings_20261025.json)
- [유지보수 참고 문서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/reactorprompt-fashion-semantics.md)
- [독립 한·영·관계 검토](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/integration/bilingual-owner-review.json)
- [한·영 제안문 조회 진단](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/runtime/stage/fashion-authored-endpoint-probes-d27a09ba46f95a228189cd1025b1fcea922ac1b39fa3480eb441882a6f2d5d73.json)
- [최종 검색·설치 검증 결과](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/runtime/FINAL-RESULT.md)
- [최종 검색·설치 검증 JSON](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/runtime/FINAL-RESULT.json)

## 근거 파일

- 새 수집본: `generated/trend-scout/raw/reactorprompt-export-20261025-pages-incremental/final-report.json`
- 의상 작업 원본: `generated/trend-scout/raw/reactorprompt-fashion-20261025/`
- 입력 목록: `corpus-manifest.json`, `corpus.jsonl`
- 최종 표현·위치: `merged/terms.json`, `merged/occurrences.jsonl`
- 입력 해시: `merged/final-input-hashes.json`
- 전체 검증: `qa/merged-final-verification.json`
- 중앙 수리·보충: `merged/qa-overlay-audit.json`
- 분류·표본 한계: `qa/semantic-review-scope.json`, `qa/rare-lexeme-coverage-summary.json`
