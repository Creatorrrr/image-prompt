# Gaslamp Fantasy 데이터 반영 계획

상태: **PLAN_NOT_APPLIED**. 2026-10-23. 리서치 결과를 실제 source·검색·이미지 성능으로 연결하기 위한 실행 단위와 종료 조건이다. 이번 요청에서 운영 파일·설치본·인덱스를 수정하지 않았다.

## 1. 목표와 유지할 경계

목표는 장르 단어의 노출량이 아니라 **서로 다른 의미의 검색, 정확한 역할 선택, 소유자/연결 관계의 보존, 가시 실현**을 개선하는 것이다.

- 113개 의미 카드 중 79개 가시/대리 실현은 채택 검토의 재료다. 79개 신규 CID를 만들라는 할당량이 아니다.
- 34개 context 카드는 외형 태그·강제 profile로 변환하지 않는다.
- `reuse / refine / new / context / defer`를 항목마다 결정한다. 어휘 일치 0은 신규의 충분조건이 아니다.
- `proxy`는 복잡한 제도/상태를 증명하지 않는다. 선택한 가시 부분과 비가시 주장을 함께 보존한다.
- 초기 독립 core/요청 의미가 후보 데이터에 의해 소급 변경되면 실패다. 선택된 후보도 requester의 열린 차원과 모든 실제 영향 범위에 맞아야 한다.
- 검색 노출·native 자격·literal prompt·픽셀·사용자 판단을 별도 성과로 보고한다.

## 2. P0/P1 우선순위

| 단계 | 먼저 처리할 범위 | 이유 | 완료 증거 |
|---|---|---|---|
| P0-A | G00/G01, gaslight/gaslighting, bustle, calling card, medium, construct, 시대/판본 | 어휘 일치가 잘못된 의미를 활성화하는 경로 차단 | 원문-카드-기존 CID 판단표와 독립 경계 질의 |
| P0-B | G03~G07, G12, G23, G27/G28/G33 | 광원·부품·실루엣·물건 구조의 명확한 차이 | 완전 source/conditions/effects/RID/owner 비교 |
| P0-C | G40/G42/G43/G51/G52/G56/G61/G67/G69 | 매체/반사면·접점·동일 소유자 보존 | typed native facts·owner map·guard/permission 검토 |
| P0-D | G24/G38/G45/G57/G68/G74/G75/G80/G83/G86/G87, G91~G97/G101/G102/G104/G110/G111 | 법·동의·생사·원인·정체를 외형으로 오인하는 문제 | context 유지 및 비가시 대조의 차단 결과 |
| P1 | 도시/온실/수집/복식 소품·미학의 추가 변형 | 기존 자료의 재사용과 다양성 확대 | 역할별 의미 검토·한영 동등성·검색 회귀 |
| 보류 | 골상학 구체 도표, 전통별 의식 문양, 정확한 일부 복식/도구 판본 | 현재 공식 색인/문맥만으로 세부 표준형을 인증할 수 없음 | 개별 소장품 본문·사진/기술 사료 확인 후 별도 승격 |

보류는 주제 삭제가 아니다. 현재 문맥과 한계를 남기고, 부족한 근거가 생긴 세부만 운영 채택을 미룬다.

## 3. 단계 0: 구현 전 기준선과 역사 증거 보존

1. 새 HEAD·manifest·module·slot catalog·검색 layout/recipe·설치본 pointer·dirty 상태를 다시 snapshot으로 남긴다. 이 연구의 BASELINE과 corpus snapshot을 덮어쓰지 않는다.
2. 적합한 현재 checkout/attached worktree를 확인한다. source를 수정할 단계에서는 기존 dirty 작업과 분리할 필요가 있으면 관리 worktree를 사용한다.
3. 공개 출처의 이미지/도판과 텍스트를 구분해 검토한다. G05/G12/G23/G34 등에서 보강한 근거는 지역·연대·소장품별 변형으로 고정한다.
4. 참조 대화 뒷부분은 Chrome에서 확보해 **별도 보완 snapshot**으로 추가했다. 217개 화면 표 행의 현재 coverage와 최초 20,000자 제한 기록을 함께 보존한다. 이후 대화/출처가 달라지면 새 snapshot으로 기록한다.

종료 조건: 구현 allowlist와 보호 hash 목록, source/설치본 차이, 획득 범위/미검증 목록이 명확하다. 다른 작업의 파일을 정리하지 않는다.

## 4. 단계 1: 기존 source에 대한 의미 단위 결정

출발점은 [adoption-decisions.json](adoption-decisions.json)의 18개 제안이다. 검색 후보의 이름이나 tags만 보지 않고 아래를 읽는다.

`content 전체 → 모든 realization/branch → conditions → effects → 실제 binding → native evidence/owner/guard/permission → 기존 문헌/검토 기록`

| 예 | 결정 방향 | 하지 말아야 할 축약 |
|---|---|---|
| 모발 로켓 | 기존 CID 재사용. 비애도 대조까지 이미 존재 | Gaslamp 이름을 붙인 동일 후보 복제 |
| 크리놀린/버슬 | 기존 실루엣/owner를 보존하고 필요 시 별도 내부 구조 변형 | 기존 record에 owner가 없었다고 보고하거나 숨은 후프를 가시 통과로 계산 |
| 샤틀렌 | 고리와 체인 두 CID가 같은 허리 계통인지 연결 검토 | 각각 보이기만 하면 같은 물건이라고 간주 |
| 온실 | 일반 온실과 기존 성인+빗장 실현의 동등성 추가 조사 | 기존 CID의 요구를 빼고 중립 온실로 사용 |
| 요정 계약 | 기존 공유 문서 관계 재사용, effects의 실제 target/property 범위 재검토 | 모든 차원×모든 소유자에 같은 property를 배치 |
| 플랑셰트/갈바니즘 | generic writing/lab source와 비교 후 신규 결정 | 어휘 0 hit를 의미 부재로 단정 |
| 법률/성적 지위 | context 유지 | 반지·드레스·책을 신분/동의의 확정 증거로 처리 |

새 CID는 기존 native identity 규칙으로 발급하고 실제 RID를 확인한다. 연구의 G/D/K 번호를 CID/RID처럼 쓰지 않는다. 검토 결과는 `reuse/refine/new/context/defer`와 기존 source canonical hash에 묶는다.

종료 조건: 채택하려는 모든 실현에 결정 사유·기존 CID 또는 신규 이유·원문/번역·관계·변형 범위가 있다. 미해결 중복은 등록하지 않는다.

## 5. 단계 2: source와 native 역할 증거 작성

예상 작성 위치는 다음과 같다. **파일명은 제안이며 현재 존재/등록/실행을 의미하지 않는다.**

| 경로 | 목적 | 연결 방법 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_gaslamp_fantasy_semantics_20261023.json` | 채택된 카드·출처·관계·한계 보존 | provenance/참조용 registry. 이름만 추가해도 런타임이 자동 읽는다고 가정하지 않음 |
| `.../assets/photo_candidate_gaslamp_fantasy_20261023.json` | 실제 native candidates | `photo-candidate-module/v3`의 허용 field·native 의미 계약에 맞춤 |
| `.../assets/photo_candidate_gaslamp_fantasy_bindings_20261023.json` | 실제 슬롯 연결 | `photo-candidate-slot-bindings/v3`, 각 role/semantic_role을 현 catalog와 검증 |
| `.../assets/photo_candidate_corpus_manifest.json` | candidate/binding 모듈 등록 | 현 loader의 허용 module kind만 사용. 별도 semantic registry를 임의 kind로 넣지 않음 |
| `.../tests/`의 해당 corpus/native/owner/search 평가 | 필수 회귀 검증 | 현재 구현과 실제 실패 경로에 맞춰 좁게 추가/실행 |
| `docs/research-evidence/photo-prompt/gaslamp-fantasy-20261023/integration-evidence/<phase>/` | 후속 실행 증거 | 연구 원본과 분리하고 새 source/index/run hash를 기록 |

현 `photo_candidate_corpus.py`의 `load`는 manifest에 명시된 모듈을 결합한 뒤 검증한다. JSON을 하나 저장했다는 이유로 데이터가 노출된다고 보고하지 않는다.

각 채택 실현은 다음을 수작업으로 검토한다.

- **positive 의미:** EN/KO가 같은 사람 수·소유자·부품·현재 상태·접점·매체·실재/가상 구분을 보존한다.
- **native facts:** 현 `photo-candidate-role-evidence/v4` 계약에 맞는 실제 source pointer/quote와 meaning/catalog hash를 사용한다. 연구 graph 자체는 native 자격이 아니다.
- **owners/relations:** 장치/착용자/신체 부위/인화물의 소유자를 구분한다. 같은 단어가 두 객체를 뜻할 때 재사용한 ID로 합치지 않는다.
- **effects:** 실제 바뀌는 dimension·owner·property만 적는다. 대상 수가 늘어난다고 모든 차원과 곱하지 않는다.
- **conditions/guards:** applicability·성인 선언이 필요한 문맥·실제 owner 선택·요청에 필요한 prerequisite을 현재 native 계약에 기록한다. 장르명에 매달린 보편 조건을 만들지 않는다.
- **bindings:** 한 후보의 여러 슬롯 노출은 각 역할이 성립할 때만 허용한다. `prop`이 된다고 자동으로 `action`, `mood`, `world`까지 부여하지 않는다.
- **context:** 비가시 claims를 양의 visual prose나 negative keyword bag에 섞지 않는다. 현재 context 역할의 지원 범위를 검토하고, 지원되지 않으면 연구 문맥으로 유지한다.

종료 조건: source loader·native 역할/owner/permission 검증이 통과하고 미자격은 미자격으로 보고된다. `native_approval:true`를 문서 생성으로 부여하지 않는다.

## 6. 단계 3: 별도 인덱스와 실제 검색

1. `build_shared_candidate_index.py`의 **별도 `--output-assets` 경로**를 사용한다. 운영 asset에서 기본 build를 실행하면 pointer를 바꿀 수 있으므로 금지한다.
2. source 합집합·canonical hash를 확정한 뒤 그 소스에서 파생 index를 만든다. 기존 벡터는 embedding space·recipe·text hash가 모두 호환되는 경우만 재사용한다. v2 벡터를 v1이라는 이름으로 바꾸지 않는다.
3. 별도 source/index 검증을 완료한다. source 수, positive 수, binding 수, shard closure, 문서-벡터 text hash와 query recipe를 확인한다.
4. [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)의 151사례/302개 한영 질의를 실제로 실행한다. 현재 파일은 전부 `NOT_RUN`이며 reference card 번호는 아직 native gold CID/RID가 아니다.
5. 채택 결정에 따라 native CID/RID gold와 허용 role을 수작업으로 작성한다. 카드의 자기 문장을 사용한 개발 79사례를 독립 holdout으로 포장하지 않는다. 별도 새 표현·장면 조합을 최소 12쌍 작성하고 결과를 보기 전에 동결한다.
6. 기존 slot 검색과 주제/기본 프롬프트 기반 독립 검색을 모두 확인한다. 두 경로의 결과를 합쳐 한 경로의 누락을 숨기지 않는다.

기록: `query → lane → CID/RID → rank → 적용 가능한 실제 role → native status → 거절 이유`. Top8 노출/Recall과 role-fit 오탐은 별도다. corpus에 없는 candidate를 gold에 넣어 reranking 실패라고 부르지 않는다.

제안하는 승격 기준은 **평가 시작 전에 고정**한다.

- P0의 필수 의미·관계는 각 한영 질의에서 적합한 전체 실현이 top8에 있어야 한다. 조사상 재사용 후보만 필요한 경우 불필요한 신규가 없어도 된다.
- gaslighting/bustle/medium/construct 등의 잘못된 의미가 가시 변형으로 선택되거나 hard obligation을 만들면 P0 실패다.
- 비가시 대조 14사례는 픽셀 점수로 성공 처리하지 않는다. `BLOCKED_UNSCORED` 또는 명시적 context 한계가 필요하다.
- 일반 대조에서 요청하지 않은 사람·시대·복장·성적 의미·장르 장식을 강제하면 실패다.
- 기존 결과와 한영 쌍의 차이는 실제 결과와 함께 보고한다. 연구 단계에서 목표치 달성이나 개선율을 미리 쓰지 않는다.

종료 조건: 모든 P0 실패가 해소되거나 보류 source로 분리되고, 기존 검색 회귀·gold 한계가 설명된다. source 검증만으로 검색 완료를 선언하지 않는다.

## 7. 단계 4: 프롬프트 전달과 native pixels

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 12군×3 arm, 최초 36장 비교를 수행한다. 이 수는 실행/비용 발생 기록이 아닌 계획이다. 선택한 이미지 도구의 당시 지원·권한을 확인하고 실행 시점의 기존 사용자 승인 범위를 따른다.

각 군은 독립적인 요청/core를 후보 조회 전에 만들고, 군 안에서는 그 동결 core·creative controls를 A/B/C에 동일하게 사용한다. A는 추가 후보 없음, B는 현재 source, C는 채택 검토 source다. 바꾸는 것이 데이터일 때 구도·연령·기본 해석까지 달라지면 데이터 효과를 해석할 수 없다. 동시에 core에 없는 후보를 필수로 만들지 않는다.

Literal evidence·선택 CID/RID·영향 범위·prompt hash·transport hash·이미지 파일을 각각 남긴다. 실제 요청 의미를 살리는 통합 저술을 평가하며, 모든 검색 후보를 전시하는 화면은 만들지 않는다.

종료 조건: component와 relation의 양끝이 같은 출력에서 관찰된다. 가림/작은 크기/관계 단절/대체물은 `UNOBSERVABLE_NOT_PASS` 또는 실패다. 부분 성분 합계와 scene 전체 성공은 별도다. 생성 파일이 없는 실패는 픽셀 증거가 아니며 moderation 결과를 덮어쓰지 않는다.

## 8. 단계 5: 활성화·게시와 최종 보고

데이터·검색·필수 native pixel 기준을 충족한 source만 설치/게시 대상으로 삼는다. 실제 배포가 요청되면 명시 allowlist로 stage하고 staged 이름과 blob hash를 비교한다. 원격 게시 완료는 local/tracking SHA뿐 아니라 실제 원격 SHA로 확인한 뒤 보고한다. 관련 없는 dirty/untracked 파일은 보존한다.

**이번 연구 종료 시 요구하는 증거:** 출처/한계·113카드/79초안·217행 연결·기존 source 판단·평가/픽셀 계획·연구 구조 검증과 보호 hash 비교. **실행해야 할 후속 일:** native source 반영, 별도 index/embedding, 실제 검색, prompt/image/pixel, 설치, commit/push. 이 두 목록을 같은 완료 상태로 합치지 않는다.
