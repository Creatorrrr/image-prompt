# 캠퍼스 데이터 반영 및 독립 이미지 테스트

현재 상태: 데이터 등록·실행 스냅샷 설치·검색 개발 검증·독립 이미지 3회 생성·원장/리뷰 기록·부모 픽셀 재검토 완료. 전체 장면 기준 1/3 통과, 신규 source의 픽셀 기여는 0/3 미확립이며 방법상 한계를 함께 보존한다. 최종 machine 결과는 `FINAL-VALIDATION.json`이다.

## 반영한 데이터

- 시각 의미 카드 124개, 원 대화 용어 356행의 관련 경로, 출처 범위·소유자 관계·혼동 경계·관찰 불가 기준을 등록했다.
- 새 CID 123개 = 전체 관계를 포함한 선택적 한영 시각 후보 100개 + 시간/문맥 진단 23개. 진단은 positive 시각 재료 검색에서 제외했다.
- 기존 손깍지 CID 1개를 원문 변경 없이 재사용했고 선택적 binding 220개를 추가했다. 초안 101개와 새 시각 후보 100개의 차이는 이 재사용 1개다.
- 원래 후보 22,508개, binding 17,256개와 기존 모듈 바이트를 등록 시점에 보존했다. 이후 관찰한 다른 작업의 변경은 `post-registration-observation.json`에 별도 기록한다.
- source의 조건/effects를 슬롯에 맞춰 축소하지 않았다. 연구 관계 그래프를 native permission이나 native qualification으로 승격하지 않았다.

실제 source는 `skills/photo-prompt-image-generator/assets/photo_candidate_campus_life_20261024.json`, `photo_candidate_campus_life_bindings_20261024.json`, `photo_campus_life_semantics_20261024.json`이다. `source-preservation.json`과 `canonical-source-validation.json`을 참조한다.

## 검색 및 실행 데이터

`successor.json`의 H-F2 generation `8490ccab7b23d1bf8f79d58eb422cc19c68a5163d131b970f69fb7158dd29024`를 설치하고 기본 검색 대상으로 활성화했다. native generation은 `61d9a80aeb4311da49c609bb799970e35eb74919718a4c755420c0ab2c6f5a43`다. 기존 sealed 실행 데이터의 후보·정책·슬롯·코드를 보존하고 이번 데이터만 추가했다. 작업 트리의 다른 미설치 변경까지 활성화하지 않았다.

기존 문서 벡터 20,625개는 바이트/공간/recipe 호환성을 확인하여 그대로 재사용했고, 새 시각 후보 문서 100개를 로컬 임베딩했다. 실행 데이터의 검색 모집단은 20,723 CID/20,725 RID이다. 전체 source·문서·postings·statistics·local execution·vector coverage 및 배포된 native validator가 통과했다. 설치 시 CURRENT 쓰기는 0회이며 기본 선택 설정 `retrieval-runtime.json`을 갱신했다. 설치된 recorder가 `h-f2-v2` pack을 실제로 지원함을 확인했다.

테스트 완료 시 다른 작업이 기본 실행 버전을 `ee1d9eca47bb51f8629090b0cb0235cc2e841d4551f8d2277783dfa7a18f76cb`로 전진시킨 것을 확인했다. 이 최신 기본 버전에도 campus 원문 123개와 binding 220개가 정확히 보존됐고, positive 100개는 인덱스에 포함·진단 23개는 제외됨을 확인했다. 코드 binding은 테스트 버전과 동일하며 현재 기본 검색 모집단은 20,822 CID/20,824 RID이다. 테스트의 고정 generation을 바꾸거나 이후 기본 버전을 되돌리지 않았다. `post-test-default-observation.json`을 참조한다.

현재 SKILL 문서 SHA256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`다. 각 arm은 이 최신 문서를 읽었다. 검색 실행 코드는 `release-base.json`에 기록한 검증된 sealed kernel을 유지한다. 최신 문서 사용과 작업 트리의 모든 실행 코드 설치를 같은 주장으로 취급하지 않는다.

원본 source용 인덱스 첫 빌드는 동시 source 추가를 감지해 활성화 전에 중단했다. 남아 있던 이 작업 소유의 revision token을 정확히 확인하여 현재 source 합집합으로 복구 빌드했다. 오류 로그와 소유권·복구 결과는 보존한다. 다른 작업의 파일을 되돌리거나 오래된 인덱스를 활성화하지 않는다.

복구 빌드의 전체 검증은 후보 22,849개/positive 21,267개에서 통과했다. 그 직후 다른 작성자가 동일 source 합집합으로 만든 layout을 활성화한 것을 감지했다. 자체 빌드의 통과와 현재 활성 layout의 통과를 혼동하지 않도록 현재 layout을 대상으로 읽기 전용 전체 검사를 다시 실행했고, 오류 0개로 통과했다. 검사 전후 source/layout 일치와 새 campus 레코드 123개의 완전한 원문 보존도 확인했다. 최종 전체 source는 CID 22,849개/binding 17,760개이며 `source-validation.final.json`을 따른다. 이 전체 작업 트리 수량과 별도 설치한 안정된 실행 스냅샷 수량을 합치지 않는다.

## 검증 결과의 범위

- 의미 경계 회귀검사 12개 통과: 문맥 진단 제외, 소유자, 의복 구조, 신체 지지 경로, 화면 경계, native 비승인 등.
- 한영 검색 개발 질의 274개 실행: 카드 설명 파생 202개 + 별도 저술 경계 72개.
- 카드 설명 파생 202개 모두 목표 CID가 상위 8개에 노출되었다. 원문과 가까운 개발용 질의이며 독립 holdout 성공률이나 기존 대비 향상률이 아니다.
- 경계 질의 중 시각 목표를 둔 56개에서는 49개가 목표 CID를 상위 8개에 노출했다. 나머지 7개는 `retrieval-boundary-followups.json`에 남겼다. 관련 용어로 연결된 한 가지 형상과 질의가 요구한 세부 대안의 차이를 먼저 검토해야 한다. 단순히 검색 점수를 올려 해결했다고 볼 수 없다.
- 새 문맥 진단 23개의 positive 검색 누출은 0건이다. 이것이 프롬프트나 이미지가 모든 문맥 경계를 준수했다는 증명은 아니다.
- source 등록/인덱스 검증/검색 노출/후보 선택/실제 프롬프트/실제 생성/픽셀/사용자 수용을 분리한다. 연구 데이터 자체의 native approval은 false를 유지한다.

## 독립 테스트 설계

동일한 실제 사용자 요청과 첨부 이미지 파일을 각 arm에 전달했다. 각 arm은 다른 arm의 core·후보 선택·프롬프트·이미지를 보지 않고, 자기 분야의 무작위 선택을 기록하고 core/controls와 사전 관찰 gate를 동결했다. 후보 source는 그 이후에만 검색했다. 부모가 다른 arm의 컨셉을 요청자 의무로 추가하지 않았다. 기본 controls는 각 arm에서 별도로 해석했으며 추가 controls를 강제하지 않았다.

- A: 도예 공동 작업, 식은 가마 선반 위 작품 배치와 공동 기록.
- B: 천문 동아리 축제 암막 부스, 투사기-스크린-별 투사 경로.
- C: 졸업 가운 반납대, 가운 착용자-빈 옷걸이-반납 가운 걸이대 관계.

A는 중립 feature catalog를 무작위 방향 선택보다 먼저 읽은 절차 순서 차이를 스스로 기록했다. 후보 데이터나 다른 arm으로부터 받은 아이디어 오염은 보고되지 않았지만, 이를 완벽한 절차 준수로 숨기지 않는다.

각 arm의 생성은 1회로 제한하고 사용자 첨부 파일을 실제 tool input에 전달한다. 도구가 모델 식별자를 노출하지 않으면 모델명은 확인 불가로 남긴다. 요구 요소가 일부만 보이거나 가려지면 전체 사례는 통과로 세지 않는다. blocked/no pixels는 `BLOCKED_UNSCORED`로 구별한다.

실제 픽셀 결과와 증거 사슬은 아래에 기록한다.

## 후보 노출에서 확인한 제한

`parent-exposure-check.json`으로 세 arm의 실제 issued material을 확인했다. A에는 신규 A16(보드 설명)·A21(학사모 조정), B에는 A22(우산 공유), C에는 F05(문틀 안 먼 인물과 여백)가 노출됐다. 각 arm의 동결 장면과 전체 source/effects가 맞지 않는 후보를 강제 채택하지 않는다. 이 세 무작위 테스트는 새 source가 실제 최종 프롬프트에 전달되는지를 보장하지 않는다.

이 결과에서 후속 보강은 다음처럼 분리해야 한다. 첫째, source와 닮은 개발 질의의 높은 검색률을 일반적인 캠퍼스 주제 질의의 성능으로 대체하지 않는다. 실제 issued query의 적합한 후보 노출을 별도 평가한다. 둘째, 묶인 관련 용어에 아직 없는 정확한 형상은 사전에 독립 후보로 저술하고 owner/effects를 재검토한다. 현재 source를 사후에 부분 채택하거나 locked dimension을 임의로 풀지 않는다. 셋째, 새 후보와 일치하는 관찰 관계를 포함한 추가 테스트는 후보를 보지 않은 독립 core와 사전 gate로 새로 설계해야 한다. 이번 세 arm의 core를 검색 결과에 맞춰 바꾸어 성공률을 올리지 않는다.

## 실제 생성과 부모 픽셀 재검토

생성은 arm마다 1회, 총 3회 성공했다. 첨부 JPEG SHA256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`를 각 native payload의 실제 파일 경로 및 reference binding과 대조했다. `parent-pre-render-input-check.json`과 `parent-native-plan-check.json`은 동결된 입력·최종 프롬프트·참조 파일의 바이트 연결을 확인한다. 생성 도구 응답은 모델 식별자를 제공하지 않았으므로 observed model은 확인 불가다. 계획상의 `gpt-image-2`/`1024x1536`를 관측 결과로 쓰지 않았다.

| Arm | 무작위 컨셉 | 실제 픽셀 크기 | 사전 장면 gate | 전체 장면 판정 | 신규 CID 노출/채택 |
|---|---|---|---|---|---|
| A | 도예 공동 작업 | 1312×1199 | 4/6 통과 | 부분 실패: 요구한 명확한 손가락 폭의 손잡이 간격과 해결 결과가 충분히 보이지 않음 | 2/0 |
| B | 천문 동아리 축제 부스 | 1536×1024 | 3/4 통과 | 부분 실패: 렌즈가 전경을 향하고 스크린은 뒤에 있어 투사 경로가 맞지 않음 | 1/0 |
| C | 졸업 가운 반납대 | 1024×1536 | 5/5 통과 | 장면 gate 통과: 가운·학사모·학위 커버·빈 옷걸이·반납대·가운 걸이대 관계가 보임 | 1/0 |

부모가 세 원본 이미지를 직접 열어 재검토했고 결과를 `parent-pixel-review.json`에 기록했다. 세 장 모두 캠퍼스 주제와 참조의 시각적 외형이 읽히지만, 엄격한 전체 장면 기준은 1/3 통과다. C의 발 접점은 프레임 밖이므로 관측했다고 주장하지 않는다. 최신 SKILL은 핵심 동작이 아닌 보통의 프레임 밖 지지를 허용하므로, 이를 사후에 새로운 전신/발 노출 gate로 만들지 않았다. 실제 인물의 신원·나이·재학·졸업·시간적 전후 관계는 입증하지 않는다.

최종 ledger는 세 arm 모두 성공 행 1개·실제 호출 1회·`h-f2-v2`·cross-arm input false이며, 동결한 입력 hash와 최종 프롬프트/참조/이미지 hash를 부모가 다시 대조했다. 관리형 리뷰 기록은 3/3 유효하다. 관리형 신체 접점 qualification은 A fail/B pass/C pass지만, B의 별도 사전 광학 경로 gate가 실패했으므로 B 전체 장면 실패는 유지한다. 합성 감사의 authored-evidence warnings는 A 6개/B 5개/C 6개이며 기계 감사 통과나 저자 설명이 픽셀·신원·사용자 수용 증거를 대체하지 않는다.

모든 최종 프롬프트에서 chosen candidate는 0개이고 새 source 명제의 전송도 0건이다. 따라서 **신규 데이터 → 선택 → 실제 제출 프롬프트 → 픽셀의 완전한 기여 증거는 0/3, 미확립**이다. 캠퍼스처럼 보이는 성공을 신규 데이터 검증으로 계산하지 않는다. source의 native approval은 false, 사용자 수용은 pending을 유지한다.

원본 이미지와 프롬프트:

- A: [원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/a/parent-original.png), [실제 제출 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/a/parent-submitted-prompt.txt)
- B: [원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/b/parent-original.png), [실제 제출 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/b/parent-submitted-prompt.txt)
- C: [원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/c/parent-original.png), [실제 제출 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/arms/c/parent-submitted-prompt.txt)

## 방법상 한계와 다음 검증의 조건

`parent-methodology-review.json`은 기계 감사 통과와 별도로 사용자 소유 범위의 의미를 점검한다. A의 공동 실습, B의 동아리 준비, C의 실내라는 저자 선택이 사용자-bound evidence에 섞여 있었다. 이 과도한 범위는 후보 비교에 영향을 줄 수 있다. 따라서 새 후보 미채택을 데이터 품질 하나의 원인으로 단정하거나 최신 스킬 전체 절차가 엄격히 입증됐다고 주장하지 않는다. 기존 core·ledger·이미지를 사후에 다른 lineage로 재명명하지 않는다.

다음 검증은 (1) 사용자 소유 anchor를 캠퍼스 주제와 참조 외형의 최소 의미로 좁히고 저자 선택을 열어 두기, (2) 절차문이 섞인 질의와 순수 주제/실제 장면 질의를 대조하되 새 검색은 별도 lineage로 기록하기, (3) 아직 없는 세부 형상을 독립 후보로 먼저 저술하기, (4) 후보를 보기 전에 새 독립 core와 관계 gate를 확정하여 새 CID 채택·실제 문장 전송을 확인한 후 픽셀을 판정하기 순서가 필요하다. 이번 결과를 새 데이터의 픽셀 qualification으로 승격하지 않는다.

## 보존 및 발행 상태

최초 연구 snapshot 32개 파일의 checksum은 전부 유지했다. source 등록 당시 기존 후보·binding·정책·모듈 바이트를 보존했고, 이후 공유 작업 트리의 관찰 차이는 별도 기록했다. 무수정 원본 이미지, 정확한 제출 프롬프트, arm 보고서, 원장/manifest snapshot과 부모 검토는 이 폴더에 모았다. source/index/config 변경과 작업 범위는 `change-scope.json` 및 각 build/validation 보고서로 추적한다. 로컬 데이터 반영·설치·이미지 테스트까지 수행했으며 이 작업에서 commit/push는 하지 않았다.
