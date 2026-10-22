# 반영 계획

이 문서는 실행 가능한 후속 순서와 완료 기준이다. 이번 요청에서는 연구와 계획까지만 수행했다. 운영 데이터 변경·인덱스 게시·설치본 활성화·이미지 생성·커밋은 실행하지 않았다.

## 목표와 우선순위

같은 요청을 한국어와 영어로 읽었을 때 필요한 형태·재료·수량·관계가 유지되고, 정확한 판본의 선택형 후보가 노출되어야 한다. 장르 단어에서 필수 촉수·녹색·잔혹성·성적 관계·의학 진단을 새로 만들지 않아야 한다. 선택한 후보는 가려진 부분을 통과로 처리하지 않고 완전한 소유자·끝점·경계로 평가해야 한다.

84개 카드를 전부 신규 운영 카드로 추가하지 않는다. 7개 재사용·28개 정교화·22개 신규 제안·21개 문맥·6개 보류의 판단을 기존 source 전체와 다시 대조한다. 새 CID 수는 이 검토 후에만 정한다. 연구 ID R/K/D를 native CID/RID로 전환해 쓰지 않는다.

## 0. 구현 직전 기준 재수집

작업 시작 HEAD·dirty 상태·authored manifest·모든 참조 모듈·검색 manifest·slot catalog·semantic registry·설치 코드/세대의 정확한 SHA를 다시 저장한다. 이번 조사 도중 같은 checkout에서 다른 데이터 변경이 있었으므로 [BASELINE.json](BASELINE.json)과 [SOURCE-DRIFT.json](SOURCE-DRIFT.json)은 구현의 최신 기준이 아니다. 타 작업을 되돌려 예전 해시에 맞추지 않는다.

설치된 코드와 작업 소스의 경계를 먼저 확인한다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

현재 source index의 `space`, 텍스트 recipe, 문서 hash와 실제 설치본의 실행 identity를 읽는다. 이전 조사에 쓰인 임베딩 provider·차원·세대를 그대로 가정하지 않는다. 이 단계는 데이터 채택의 승인이나 이미지 검증이 아니다.

완료 조건: 재현 가능한 소스/코드/인덱스 목록과 작업 파일 allowlist, 보호할 기존 변경 목록이 함께 저장되어야 한다.

## 1. P0 — 기존 의미·번역·관계 정교화

| 대상 | 적용할 작업 | 완료 기준 |
|---|---|---|
| C119 / R22·R23 | 우상과 부조의 대상·날개·지지체 분리 | 한영에서 같은 대상·형상·재료·날개 관계. 정본과 저술 배치의 범위 표기 |
| C126 / R31 | 시연자·장치·관중의 한국어 명제 보강 | 영어의 소유자·방향이 한국어에서도 완전하게 읽힘 |
| C104·C169 / R39·R40 | 금속 원통 외관과 유리 변형 분리, 두 케이블 개별화 | 각 케이블의 원통 소켓과 특정 외부 장치 단자가 명시됨 |
| C173 / R52–R55 | 참가자·집단·경계 양쪽과 의도 분리 | gap/between의 두 끝이 저장된 source와 증거에 모두 존재 |
| C174 / R09 | 같은 ID와 다른 두 필드의 정확한 비교 | 문서 A/B 및 필드 A/B가 별개로 연결; 읽을 수 없는 텍스트 PASS 금지 |
| C120·C170 / R24·R25 | 전신 오중 구조와 국소 분기 구분 | 선택한 전체 계약을 유지. 전신 의무를 국소 사진으로 대체하지 않음 |
| C011·C012·C158 / R34 | 비늘과 연속 주름의 구조 분리 | 피부/의복/인쇄 패턴, 각 표면 소유자, 접점 구분 |
| C125·C171 / R30 | 무안면과 가림·가면 구분 | 머리 앞면 전체의 관찰 가능성 명시 |
| C028 / R37 | 의미 registry와 실제 native source 대응 재조사 | card_id 직접 매핑 부재를 곧 의미 부재로 판단하지 않음 |

수정의 중심은 `skills/photo-prompt-image-generator/assets/photo_candidate_cosmic_horror_20261021.json`의 해당 CID와 필요 시 그 binding이다. `photo_cosmic_horror_semantics_20261021.json`은 출처·의미 참고 registry로 동기화하되 이것을 실행 authority라고 가정하지 않는다. 현재 scripts/precore에서 해당 registry 파일명을 직접 참조하는 문자열은 찾지 못했으며, 실제 candidate loader의 완전 source 계약을 기준으로 검토해야 한다.

`en`, `ko`, `definition`, `application_contract` 및 selected realization의 positive field마다 직접 확인한 명제가 있어야 한다. 제목·경고·메타데이터로 빠진 수량·재료·관계를 대신하지 않는다. 정확한 source field-local anchor, 실제 CID/RID, 소유자와 조건·효과 전체가 함께 검토되어야 한다. 일반적인 `composition.cosmic_realization` 같은 효과 명칭은 의미·role 적합성·property 권한 검토를 대신하지 못한다.

완료 조건: 변경 source마다 한영 의미 비교표, 정확한 기존/new CID 판단, 전체 관계 graph, scope/effect/guard 검토가 남아야 한다. 기존 조건을 줄이거나 binding으로 intrinsic 효과를 덮어쓰면 실패다.

## 2. P1 — 관계를 강화하는 신규 제안

22개 신규 초안은 목표치가 아니라 선택 목록이다. 먼저 아래 네 묶음에서 중복 여부·전체 장면의 실현 가능성을 확인한다.

1. **기록·증거:** R06·R08·R10·R11. 서로 다른 매체와 대응 표식, 실물과 이미지 안 피사체의 소유 공간을 보강한다. 그림·기록·복사본의 존재가 인과·진위를 증명하지 않는다는 한계를 유지한다.
2. **몸 비례·관측·접경:** R15·R16·R20·R21·R32. 통로, 얼음 경계, 창/문의 다른 외부, 벽 접점, 분말 윤곽을 실제로 보여준다. 전부 원전의 정본 장치 디자인이라고 표기하지 않는다.
3. **물건의 정체성:** R23·R48·R49·R51. 부조·일곱 지지대·가지형 표식·열쇠의 소유 관계를 분리한다. R49의 정확 도판은 원문 이미지 검토 전에는 승인하지 않는다.
4. **생활·비적대적 관계:** R13·R38·R57. 아름다운 꿈의 도시, 돌봄 접점, 휴면처럼 보이는 자세를 대안으로 제공한다. 언제나 오염·적대·패배를 기본 의미로 삼지 않는다.

신규 파일이 필요하면 별도 candidate/binding 모듈을 만든 뒤 authored manifest에 명시적으로 등록한다. 현재 관계 변형 24개와도 중복을 검토한다. 이번 연구 JSON을 operating manifest에 직접 넣거나 연구 파일 경로를 runtime import 대상으로 삼지 않는다. 선택한 하나의 완전 실현만 effects·owner graph·gate에 들어가며 다른 대안을 동시에 합치지 않는다.

슬롯 제안은 현 149개 catalog 중에서만 작성했다. 다만 `prop`, `narrative_clue`, `species_marker` 등의 분류명·dimensions 겹침만으로 binding을 승인하지 않는다. 각 역할의 실제 의미, intrinsic conditions, selected owner·receiver·affected property, 요청의 닫힌 속성을 검토한다. 모든 후보를 하나의 general/genre 슬롯에 몰아넣지 않는다.

완료 조건: 중복 판정 후 채택한 source만 신규 등록하며, 나머지는 연구 자료에 보존한다. 데이터 보강을 이유로 routing·ranking·core 의미를 바꾸는 엔진 수정은 이 계획의 기본 범위가 아니다.

## 3. 문맥 21개·보류 6개 처리

K 카드가 모두 별도 runtime 후보가 되어야 하는 것은 아니다. 장르·철학·동의·혈통·진단·시간·소리·냄새·효능은 의미·해석 참고 자료에 유지한다. 기존 문맥 record를 활용할 때도 broad label에서 hard profile을 활성화하거나 exact request의 의미를 바꾸지 않는다.

보류는 K09·K10·K11·K12·K19·K26이다. 필요한 추가 증거는 [ACCESS-LIMITS.md](ACCESS-LIMITS.md)에 있다. 원전 누락 구절, 최초 창작자 서지, 이론 원저, 선택한 판본의 정확한 도판을 확보한 다음 재평가한다. 보류를 지우거나 비슷한 촉수 그림으로 채운 뒤 완료로 세지 않는다.

## 4. 구조·source 검증과 인덱스

프로젝트의 현 유지보수 규칙과 당시 CLI `--help`를 확인하고 다음 검사들을 변경 범위에 맞춰 실행한다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

위 명령은 이 조사에서 실행하지 않았다. 구현 시 실제 설치본이 보고한 적절한 Python/의존성을 사용한다. working source 검사와 설치본 검사를 혼동하지 않는다. 원본 source hash와 관계 없는 과거 PASS를 새 데이터의 검증으로 재사용하지 않는다.

인덱스는 staged source에서 먼저 만들고 텍스트 recipe·ID·전체 text hash·provider/model/dimensions·vector integrity가 모두 같은 벡터만 재사용한다. 달라진 정의·번역의 임베딩은 해당 후속 작업 범위에서만 생성한다. `photo_candidate_search.json`이 관찰된 운영 index manifest이며 과거 index 파일명은 사용하지 않는다. 완전한 source/payload/posting/vector closure를 검증한 뒤에만 게시 가능한 generation으로 취급한다.

`--publish`와 설치본 활성화는 이 연구의 실행 항목이 아니다. 구현 작업에서 데이터 qualification·검색·픽셀 결과와 별개로 게시/활성화 상태를 명시하고, 보호할 기존 설치본과 CURRENT를 유지한 상태에서 먼저 stage한다.

## 5. 독립 검색·의미 평가

[80사례/160개 입력](EVALUATION-CASES.tsv)을 development set으로 사용한다. 평가 문장은 source 문장 그대로의 재생이 아니라 짧은 자연어·대조 조건·일반 요청을 포함한다. 구현 중 이 파일을 보고 튜닝했다면 이를 holdout으로 부르지 말고 새 paraphrase holdout을 따로 동결한다.

각 활성·명시 요청 슬롯에 대해 candidate-free query, query text/hash, 실제 provider/space, top-k CID/RID·source text, 선택 조건·role fit·effect·guard, 거절 이유를 저장한다. 키워드 진단과 실제 hybrid 검색을 구분하며 묵시적으로 keyword-only로 대체하지 않는다. 한국어와 영어는 각각 실제 검색을 실행한다.

검색 단계 제안 기준:

- P0 양성의 전문가가 지정한 적합 source가 슬롯별 top-10에 노출되는지 먼저 기록한다. 노출은 의미 적합·채택 PASS와 별개다.
- 한영 명제 보존율과 role별 precision을 별도 기록한다. 수량·재료·끝점·판본이 바뀌면 전체 사례 실패다.
- 26개 경계 사례와 12개 일반 대조군에서 broad genre의 새 hard 의무, 인종/진단/동의 추정, 닫힌 속성 변경은 0건이어야 한다.
- 12개 비가시·미해결 사례를 visible PASS로 올리거나 보류 사실을 지우면 실패다.
- 전체 수치뿐 아니라 실패한 실제 query·후보·source 문장을 보존한다. 평균 recall로 특정 판본 오류를 숨기지 않는다.

일반 대조군에서 관련 비장르적 재료가 선택되는 것 자체는 실패가 아니다. 원래 요청의 의미를 바꾸거나 코스믹 장면을 의무로 만드는지를 검사한다. 기존 자료가 적합하면 유지하며 57개 초안을 채택하기 위한 억지 quota를 만들지 않는다.

## 6. Native·픽셀·선호의 독립 판정

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 12사례×3안 비교를 첫 단계로 제안한다. source/native qualification, pack 노출, composed prompt의 완전 증거, 실제 저장 이미지, requester의 선호는 서로 다른 결과다.

변경된 prompt는 fresh audit와 같은 sealed execution을 요구한다. 선택한 카드의 모든 부품과 관계가 동일한 계획 시야에서 읽혀야 한다. 가림을 숨겨서 통과시키거나, 전체 의무를 임의의 인상으로 축소하지 않는다. R24·R48처럼 다수 뒷면/끝점이 필요한 장면은 구도 단계에서 불가능하면 후보를 채택하지 않는다. 명시적 요청의 의무라면 요청 의미를 보존하는 재구성/명확화 경로를 사용한다.

완료 조건: 실제 픽셀에서 각 gate가 visible/partial/unobservable로 판정되고 전체 사례 통과와 장르·예술적 인상·관객 선호가 따로 기록되어야 한다. 거부나 API 오류는 이미지 실패가 아닌 `BLOCKED_UNSCORED`다. 사용자 선호는 자동 승인하지 않는다.

## 7. 전달과 복구

변경 source와 파생 index/설치본의 상태를 각각 보고한다. 요청된 경우에만 검토한 allowlist로 commit하며 기존 dirty/untracked 변경을 섞지 않는다. 게시/설치 이후 문제가 있으면 보관한 이전 generation과 정확한 pointer로 복구한다. 타 작업의 소스를 되돌려 해결하지 않는다.

완료 보고에는 채택/미채택 카드, 실제 source/CID/RID, 수행한 구조·검색·픽셀 검사, 실패·보류, commit/push/activation 상태를 포함한다. 이 계획이나 구조 PASS를 운영 반영 완료로 보고하지 않는다.
