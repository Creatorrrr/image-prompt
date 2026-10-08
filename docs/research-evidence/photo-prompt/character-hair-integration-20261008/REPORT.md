# 캐릭터 헤어 리서치 데이터 반영 및 독립 이미지 검증

2026-10-08 작업. 조사 결과를 실제 작성 원본, 후보팩, 시각 의미 프로파일, 색인 및 현재 스킬 런타임에 반영했다. 테스트 컨셉과 필수 시각 조건은 데이터 접근 전에 각각 독립 서브에이전트가 정하고 동결했다. 이미지를 생성한 뒤 같은 조건으로 원본 픽셀을 검토했다. 데이터 작성·검색 노출·채택·프롬프트 감사·픽셀 판정은 별도로 기록했다.

## 데이터에 반영한 내용

기존 조사 패키지의 454개 키워드, 194개 의미 카드, 출처 기록을 유지했다. 키워드 입력은 참고 대화에서 UI로 확인한 TSV 전사본이며 원래 업로드 파일의 바이트 검증을 뜻하지 않는다. 조사 출처 105개 중 100개는 본문 또는 API를 직접 확인했고 5개는 확인 범위가 제한된 것으로 기록했다. 이번에는 그 카드와 부위별 수분 경계 투영 1개를 합쳐 195개 적용 결정을 만들었다. 새 후보 111개, 새 시각 의미 프로파일 111개, 기존 후보 31개의 설명 보강을 반영했다. 110개 선택적 후보 묶음이 컴파일된다. 개별 과정·진단·불충분한 출처·문맥 용어 53개는 보류 또는 문맥 항목으로 명시했다. 입력 용어 161개가 실행 후보와 직접 연결된다. 454개 명칭 모두를 신규 실행 후보나 검증 완료 항목으로 세지 않는다.

두 작성 원본은 [헤어 후보 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_character_hair_extension.json)과 [헤어 시각 의미 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_character_hair.json)이다. [적용 결정 195개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/INTEGRATION-MAP.json)와 [키워드별 연결표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/KEYWORD-APPLICATION-CROSSWALK.json)에서 새 후보·기존 항목·보류 사유·출처를 추적할 수 있다. 원래의 [상세 리서치](/Users/chasoik/Projects/image-prompt/docs/researches/2026-10-08-character-hair-visual-semantics.md)는 수정하지 않았다.

각 항목에는 관찰 가능한 구성 요소, 같은 머리의 소유 관계와 부위, 구성 요소 사이의 연결, 적용 속성, 혼동 경계, 원본 픽셀 판정 조건을 작성했다. 이름만으로 물성·염색 과정·출신·연령·성격을 단정하지 않는다. 새 프로파일의 강제 활성화에는 완전한 가시적 명제가 필요하며, `jellyfish cut`, `underlights` 같은 단독 명칭은 선택적 후보로 남는다. 머리 속성의 부모 범위를 함께 선언해 새 세부 속성 이름으로 기존 소유자·속성 잠금을 우회하지 못하게 했다.

중요한 기존 경계도 수정했다. 실제 젖은 머리와 건조한 wet-look 스타일링을 분리했다. 실제 수분 프로파일의 수분·부피·뭉침·무게 또는 국소 접촉 조건은 유지했다. balayage라는 시술 명칭 전체를 밝은 리본 배열로 간주하던 활성화 범위를 선택된 불규칙한 리본 무늬로 좁혔다. 그 리본 무늬는 옴브레 길이 그라데이션과 공존할 수 있다. hime의 기존 프로파일은 이미 앞머리를 필수로 요구하지 않아 유지했다. 기존 후보의 보강은 설명·표현 추가로 제한했다.

## 색인과 실행 상태

원본 manifest에 두 파일을 등록하고 유지보수 출처와 해시를 연결했다. semantic index는 10,999개 후보, visual profile index는 2,756개 프로파일·5,368개 exact term을 포함한다. Gemini `gemini-embedding-2`, 768차원과 같은 텍스트 레시피를 유지했다. 기존 후보 벡터 10,855개와 기존 프로파일 벡터 2,643개는 정확히 같은 텍스트·벡터로 재사용했고, 변경 텍스트 35개와 새 텍스트 222개를 임베딩했다. 삭제된 ID는 없다. [벡터 재사용 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/INDEX-REUSE-AUDIT.json)를 보존했다.

이미지 테스트는 모두 동일하게 발행된 generation `0a3b19f34fb2ef66f6406cbf4f38c9aac196ebc515b8bb918aa2d1c16fc40000`에 묶였다. 실제 후보 선택 모드는 `core_bm25f`였고, 같은 슬롯의 코어·동결 관찰 문구를 BM25F와 RRF로 검색했다. 후보팩의 `semantic_candidate_coverage=0`은 sensual contextual retrieval의 네 레인 값이다. 이를 전체 헤어 검색의 임베딩 커버리지로 일반화하지 않는다. 이번 이미지 실행이 헤어의 임베딩 검색 품질을 검증한 것은 아니다.

이미지 리뷰가 끝난 뒤 보조 컷 7개의 candidate/profile 효과 선언 14곳에 있던 하이픈 속성 경로를 정규화했다. `hair.style` 부모 효과는 그대로 유지했다. 최초 유지보수 기록은 보존하고 [v2 후속 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008-v2.json)을 만들었다. [속성 경로 변경 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/PROPERTY-PATH-REVIEW.json)과 [전체 positive text/vector 동일 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/FINAL-METADATA-INDEX-AUDIT.json)를 남겼다. 새 임베딩 요청을 거부하는 helper로 두 색인을 다시 만들었고 기존 벡터가 모두 동일했다. 현재 기본 스킬과 테스트 저장소의 최종 generation은 `2c8f19fb3d231c611eb3309ec02d681ce530db8cfda05a1a3671f21d6724c7c6`이다. [발행 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/RUNTIME-PUBLICATION.json)에 이미지 테스트 버전과 최종 버전을 함께 명시했다. 마지막 변경은 속성 경로와 출처 metadata이며, 이미지 테스트의 선택 항목·의미 문구·필수 조건을 변경하지 않았다. 새 최종 generation으로 이미지를 다시 생성했다고 주장하지 않는다.

## 독립 컨셉, 프롬프트, 실제 이미지

세 서브에이전트는 대화 기록을 넘겨받지 않고 최신 canonical 스킬을 읽었다. 스킬 SHA256은 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`이며 `.agents` 사본과 일치했다. 컨셉·기본 프롬프트·헤어 조건·촬영 계획을 데이터 접근 전에 동결한 [사전 테스트 등록부](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/PRE-RENDER-TEST-REGISTRY.json)를 남겼다. 다른 에이전트의 코어나 프롬프트를 공유하지 않았다.

공통 제어값은 sensual 1, fetish 0, surreal 0, creativity 1이었다. seed는 독립 컨셉과 후보 선택의 추적 값이며 native 이미지 모델의 샘플링 seed를 뜻하지 않는다. 제공한 얼굴 사진은 보이는 얼굴 특징의 참고로 사용하고, 테스트용 헤어는 에이전트가 별도로 설계했다. 참조 사진의 실제 신원·연령·성격·신체 유사성을 추론하지 않았다. 이미지 생성에는 built-in native image tool을 사용했다. 관찰 가능한 모델명이 반환되지 않아 이미지 모델은 unknown으로 기록했다.

| 컨셉과 독립 seed | 동결한 헤어 조건 | 실제 후보 사용 | 첫 이미지 판정 |
|---|---|---|---|
| A. 폭우로 출항이 지연된 마지막 페리의 광학 수리실. 손상된 항해용 투명 필름을 수동 프로젝터에서 정렬. 14986281802291613258 | 조밀하고 짧은 일자 앞머리, 양쪽 턱선의 짧은 보브, 윗가슴까지 내려오는 긴 아래 패널 2개, 뚜렷한 두 길이 층, 모든 경계·끝점의 같은 프레임 가시성 | jellyfish/micro-fringe 관련 새 후보는 작성 원본과 색인에는 있으나 실제 팩에 미노출. 다른 길이·형태 후보는 거절. 헤어 후보·프로파일 채택 없음 | 미통과. 두 층은 보이지만 앞머리는 성기고 눈썹 가까이에 있으며, 양쪽 짧은 절단선이 불명확하고 긴 끝점이 지정한 윗가슴보다 낮음 |
| B. 누수 뒤 온실의 표본 압착 작업대에서 종이를 정리. 3927461530 | 오른쪽 귀 뒤 한 묶음과 한 자유 꼬리, 오른쪽 관자놀이에서 시작하는 세 가닥 땋음, 같은 묶음 뿌리로 이어지는 연결, 파란 천 리본의 감긴 뿌리·매듭·고리 2개·끝 2개, 그 바로 위에서 머리에 접촉한 은색 초승달 핀 | 첫 팩의 기존 `sca_h09` 채택. 이번에 보강한 새 표현은 팩 표면에 없어서 보강 효과로 주장하지 않음. 필요한 땋음·리본 관련 후보는 미노출 | 미통과. 땋음 시작점이 정수리 쪽이고 연결 끝점은 가려짐. 초승달 핀이 리본 뿌리에서 떨어져 있음 |
| C. 비를 지나온 천체관 기술자가 작업대에서 천공 별 원판을 수리. 2795109987673587965 | 어두운 갈색 겉층, 귀·목덜미에서 어깨 끝까지 이어지는 은색 안층, 겉층의 안층 겹침, 건조하고 분리된 크라운, 두 색 층의 끝 수 cm에만 젖은 뭉침과 실제 물방울 | 새 `chrh_hair_color_state_underlights`가 실제 팩에 노출되고 채택됨. 지역 수분 후보·프로파일은 미노출 | 미통과. 겉/안층의 소유·겹침은 확인했지만 양쪽 끝의 물방울과 끝 수 cm로 제한된 수분 경계를 충분히 확인할 수 없음 |

A의 [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_a/final_prompt_en.txt), [원본 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_a/generated_images/arm_a_last_ferry_native_attempt_1.png), [에이전트 판정](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_a/native_pixel_review.json), [root 독립 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/ROOT-A-INITIAL-PIXEL-REVIEW.json)을 연결했다. root는 A1 FAIL, A2 UNOBSERVABLE_NOT_PASS, A3 FAIL, A4–A5 PASS로 판정했다. 에이전트는 A1/A2를 통과로 보았으나 A3를 실패로 보았다. 두 리뷰를 모두 보존했고 전체 미통과라는 결론은 같다.

B의 [첫 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/final_prompt.txt), [첫 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/results/attempt_1.png), [root 첫 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/ROOT-B-INITIAL-PIXEL-REVIEW.json)을 보존했다. root와 에이전트 모두 B1/B4 PASS, B2/B5 FAIL, B3 UNOBSERVABLE_NOT_PASS로 판정했다.

B는 원래의 B1–B5·컨셉·참조·제어값을 유지한 채 카메라, 머리 경로, 접촉과 가림에 한정한 보정 1회를 실행했다. [보정 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/repair_1/final_prompt.txt)와 [보정 원본 1237×1272](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/results/attempt_2.png)를 보존했다. 핀은 리본 뿌리 바로 위에서 머리에 접촉하여 B5가 통과했다. 땋음의 시작은 여전히 정수리 가까이 있으며 땋음 끝의 같은 뿌리 연결이 가려져 B2/B3는 미통과다. 꼬리 끝은 윗가슴보다 아래로 내려가 B1도 실패했다. root는 B4를 통과로 보았고 에이전트는 고리·끝의 개수를 확실히 분리할 수 없어 UNOBSERVABLE_NOT_PASS로 보았다. 에이전트는 해부학적 좌우가 반대라는 B1 관찰도 추가했다. [에이전트 보정 리뷰](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/native_hair_review_2.json)와 [root 보정 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/ROOT-B-REPAIR-PIXEL-REVIEW.json)는 서로의 판정을 읽기 전에 동결했고 각각 보존했다. 전체 조건을 낮추지 않은 공통 결론은 FAIL이다. 보정 팩의 crown-braid 후보는 경로가 맞지 않아 거절했으며, 이 보정에서는 후보나 시각 의미 프로파일을 채택하지 않았다. 핀 위치 개선을 새 데이터의 채택 효과로 주장하지 않는다.

[B의 상세 결과와 실행 증거](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/FINAL_REPORT.md)도 연결했다. 네이티브 호출은 A 1회, B 2회, C 1회로 총 4회다. 세 컨셉의 헤어 all-of 통과는 0/3이다. 마지막 이미지가 더 나아진 부분과 아직 실패한 조건을 구분했다.

C의 [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_c/final_prompt.txt), [원본 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_c/generated_images/planetarium-disc-initial-20261008/image.png), [데이터 기여 보고](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_c/data_contribution_report.json), [상세 결과](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_c/FINAL_REPORT.md)를 연결했다. root는 C1–C4 PASS, C5 UNOBSERVABLE_NOT_PASS로 판정했다. 에이전트는 젖은 뭉침이 귀·목 아래 길이까지 퍼졌다는 관찰로 C5 FAIL로 판정했다. 각 관찰과 공통 미통과 결론을 유지했다.

새 underlights가 노출·채택·프롬프트 표현·픽셀의 밝은 안층까지 연결된 사실은 확인했다. 원래 기본 프롬프트에도 색 대비가 있으므로 한 장만으로 데이터가 초래한 품질 향상을 인과적으로 분리 입증하지는 않았다. 일반 embodiment 리뷰의 통과도 별도로 동결한 헤어 all-of의 통과로 취급하지 않았다. 각 이미지의 ledger, native transport, tool 반환 경로와 사본 SHA, v2 독립 manifest를 보존했다. 사용자 수용 판정은 아직 없다.

## 자동 검사와 기존 작업 보존

전체 unittest discovery의 228개 모듈, 1,971개 테스트를 끝까지 실행했다. 첫 실행은 30개 모듈에서 실패했다. 헤어 관련 58개 검사는 통과했다. 작업 트리 런타임 발행 이전 상태 때문에 실패한 3개 모듈은 발행 후 39개 테스트가 통과했다. 새 보강 파일의 의존 항목을 제외한 과거 fixture가 새 파일을 함께 읽는 오류 1건을 고쳤고, 해당 모듈의 16개 테스트가 통과했다. 기존 23개 항목의 보존 assertion은 유지했다.

나머지 26개 실패 모듈의 실패 사례는 이번 반영 전 파일과 모드를 복원한 별도 스냅샷에서도 재현했다. 전체 suite는 PASS가 아니다. 선행 실패가 뒤의 원인을 가릴 수 있으므로 모든 실패 원인을 완전히 분리했다고도 주장하지 않는다. 역사적 스킬·자료 SHA 불일치와 다른 분야의 과거 픽셀 fixture를 이번 헤어 테스트에 맞춰 수정하지 않았다. [전체 검사 원기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/FULL-TEST-DISCOVERY.json)과 [실패 대조 및 수정 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/FULL-TEST-CLASSIFICATION.json)를 남겼다.

마지막 metadata 변경 뒤 주 작업 공간에서 헤어 경계 검사 6개, 전체 데이터 validator, visual profile index check를 다시 실행해 통과했다. 후보와 프로파일의 13,755개 positive text/vector를 이전 테스트 버전과 대조해 모두 동일함을 확인했다. 전체 semantic source/manifest 준비가 완료된 뒤 기본 런타임과 별도 테스트 저장소를 발행했다. 순수 속성 경로 정규화 뒤에는 관련 검사와 데이터·색인·발행 검사를 실행했으며, 56분 걸린 전체 1,971개 검사를 반복하지는 않았다.

현재 원본·파생 파일 44개를 관리 worktree에도 동기화했고, worktree 기본 런타임도 주 작업 공간과 같은 최종 generation으로 발행했다. 시작 스냅샷 654개 파일 중 이번 작업이 변경한 기존 경로 7개를 제외한 647개의 바이트와 권한이 그대로임을 확인했다. snapshot 밖의 작업까지 검증했다고 일반화하지 않는다. [최종 보존 및 소유 경로·해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-integration-20261008/FINAL-PRESERVATION.json)를 남겼다. Git HEAD는 시작과 같은 `791bd1ca3128627b9aefa22e0ab64041fe9c369f`이다. 커밋·푸시는 요청되지 않아 수행하지 않았다.

## 이 결과를 반영한 후속 검증 계획

1. 후보 노출부터 개선한다. A/B의 동결된 기본 문구를 검색 회귀 자료로 삼아 길이 층·관자놀이 땋음·묶음 뿌리 연결·장식 접촉 같은 같은 소유자의 지역 관계가 검색되는지 측정한다. 단순 이름·우연한 긴 장면 문구·반대 길이 후보가 우선되는 혼동을 대조한다. 후보 ID 강제 주입이나 필수 채택으로 노출 실패를 숨기지 않는다. 검색 방식이나 슬롯 예산 변경은 별도 변경과 회귀 검증으로 다룬다.
2. 이번 3개 사례를 유일한 데이터 품질 기준으로 확대하지 않는다. 리서치의 69개 최소 대조쌍과 20개 경계 사례를 단계적으로 실행한다. dry wet-look/실제 수분, 안층/표면 하이라이트, 세 가닥 땋음/단일 꼬임, 리본 뿌리/땋음 끝 천, 명칭만 있는 입력/완전한 명제를 우선한다. 같은 소유자·다른 소유자, 부모 속성 잠금, 같은 명제의 한·영 표현을 포함한다.
3. 픽셀 검증은 현재 실패 조건을 그대로 보존한다. A는 이마의 연속 절단선과 양쪽 턱선·윗가슴 끝점을 동시에 읽을 수 있는 구도를 시험한다. B는 관자놀이 첫 교차점부터 뿌리까지 열린 경로와 그 뿌리 바로 위의 핀 접촉을 검증한다. C는 두 색 층의 젖은 끝 경계와 실제 물방울이 원본에서 읽히는 크기·조명 조건을 비교한다. 머리 전체의 광택이나 소품의 물을 해당 모발 수분의 대체 증거로 인정하지 않는다.
4. 추후 품질 개선을 주장하려면 같은 동결 코어·참조·제어값으로 후보 반영 전후를 짝지어 비교한다. 먼저 실제 노출과 채택 여부를 확인하고, 서로 독립적인 원본 리뷰를 보존한다. 검색 통과, 프롬프트 통과, 헤어 픽셀 통과, 사용자 수용을 각각 보고한다.
