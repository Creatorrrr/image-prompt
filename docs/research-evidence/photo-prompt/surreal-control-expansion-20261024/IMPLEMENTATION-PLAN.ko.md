# surreal 시각 의미·후보 데이터 반영 계획

> 후속 실행 상태(2026-10-24): 사용자 추가 요청으로 source·index·설치 검색 세대 반영과 80질의 검증을 완료했다. 이미지 테스트의 최신 상태와 결과는 [반영·검증 보고서](integration-evidence/INTEGRATION-REPORT.ko.md)를 따른다. 아래는 최초 연구/계획 시점의 기록이다.

기준: 2026-10-24. 이 문서는 실행 가능한 후속 데이터 작업의 계획이다. 이번 단계의 산출물은 `REPORT.ko.md`와 그 근거이며 운영 반영 상태는 `NOT_STARTED`다.

## 1. 목표와 유지할 의미

범용 `surreal`의 공간·크기·인과·재질·분위기·상징적 관계를 지원하면서, 일상적·비기술적 장면과 선택적 약한 낯섦을 더 잘 저술·발견·판독할 수 있게 한다.

- 현재 0~3 정의와 기본값 0을 유지한다. 인물의 explicit fantasy는 0에서도 보존한다.
- 후보에 고정 surreal 등급이나 1/2/3 전용 풀을 부여하지 않는다. 3에서 요소 수나 필수 장식 수를 요구하지 않는다.
- source의 조건·전체 의미·effects·요청 lock을 보존한다. 창의성이나 surreal 값으로 사용자 소유 의미·closed dimension을 열지 않는다.
- 독립 baseline은 현재 skill의 허용 precore 정보만으로 확정한다. 이 조사나 예시 데이터는 core 이전의 영감 자료가 될 수 없다.
- source 연구 메타데이터를 native facts·owner 권한·guard 증거·필수 시각 의무로 취급하지 않는다.

## 2. 반영 범위와 파일

| 파일/영역 | 계획 변경 | 제한 |
|---|---|---|
| `assets/photo_surreal_control_semantics_20261024.json` (신규 제안 경로) | 연구 12원리, 선택한 완성 장면, 혼동·주장 한계·출처·선행 CID 연결 | 별도 연구/의미 레지스트리. 운영 corpus manifest의 후보 module로 등록하지 않음 |
| `assets/photo_candidate_surreal_control_20261024.json` (신규 제안 경로) | 최종 승인된 완성 시각 source와 선택한 진단 source | `photo-candidate-module/v3`의 실제 지원 shape로 저술. 연구 JSON 통째 복사 금지 |
| `assets/photo_candidate_surreal_control_bindings_20261024.json` (신규 제안 경로) | 기존 catalog 역할과 각 source의 실제 의미에 맞는 선택적 연결 | binding이 source 조건/effects를 덮어쓰거나 자격을 부여하지 않음 |
| `assets/photo_candidate_corpus_manifest.json` | 위 candidate/binding module 두 경로만 추가 | 기존 module·source 소유권 유지 |
| 기존 source module | 의미 보존형 alias/번역/정확한 명료화가 별도로 승인될 때만 수정 | 새 장면을 기존 source에 덮어쓰지 않음. 각 CID 전후 diff와 해시 기록 |
| `references/surreal-control-visual-semantics.md` (신규 제안 경로) | 현재 12군과 새 원리의 연결, 전체 의미/지각/강도 경계 | post-core만 읽도록 명시 |
| `references/maintenance.md`, `references/installed-h-f2.md` | 데이터 범위·검증 결과·활성 세대 안내 | 실제 완료된 내용만 기록 |
| 검색 산출물·세대·`retrieval-runtime.json` | 정확한 새 원문을 색인한 검증 세대 설치 후에만 갱신 | 현재 조사 단계에서는 갱신하지 않음 |
| `precore/creative_controls.json`, `SKILL.md`, 149-slot catalog, retrieval 정책/코드 | 기본 작업 범위 밖 | 필요성이 구체적으로 확인된 경우에만 별도 변경으로 검토 |

실제 schema 버전과 파일명은 실행 시 다시 확인한다. 새 의미 레지스트리만 추가하면 H-F2 문서가 자동으로 바뀌는 것은 아니다. 후보의 실제 긍정 문장과 지원되는 alias/의미 필드에 발견 가능한 내용을 넣고 정확한 인덱스를 다시 만들어야 한다.

## 3. 소스 격리와 기준선

현재 checkout은 많은 선행 변경·삭제를 포함한다. 작업 소스 22,864 CID와 설치 소스 22,353 CID 사이에도 차이가 있다. 이것을 이번 패치에 함께 게시하지 않는다.

1. 실행 직전 `evidence/corpus-state.json`의 module 해시, 설치 config, 관련 원문을 다시 확인한다.
2. 적절한 깨끗한 checkout 또는 관리 worktree를 사용한다. 사용자 선행 변경을 reset/restore로 제거하지 않는다.
3. 게시 기준 원격 SHA와 현재 설치 data generation을 명시한다. 연구 시점 이후 관련 source가 바뀌었으면 그 CID의 판단을 갱신한다.
4. 반영 allowlist를 확정하고 새 module만 먼저 작성한다. 기존 source 전수 digest와 catalog/policies 해시를 보존한다.
5. 설치본의 컴파일 형식과 작업 소스 형식이 다르므로 바이트 차이를 의미 변경으로 판정하지 않는다. CID/RID별 전체 source와 컴파일 provenance를 비교한다.
6. 배포 스냅샷에는 이번 module/의도한 명료화만 들어갔는지 확인한다. 다른 작업의 511 CID 차이를 무심코 포함하면 출판을 중단하고 범위를 다시 분리한다.

## 4. 첫 번째 데이터 묶음

P0 9개 새 완성 변형: **C01, C02, C04, C05, C09, R11, R13, R16, R17**. 기존 R23의 작은 문/의자 사례를 재사용 기준으로 함께 둔다.

| 후보 | 핵심 데이터 작업 | 검색/픽셀 구별점 |
|---|---|---|
| C01 실제 가지/반사 속 꽃 | 같은 화분·가지 대응·정상 찻잔 대조를 분리 저술 | 개화 과정이나 미래 예측을 검색 label로 붙이지 않음 |
| C02 돌 같은 베개 | 연속 광물 외관·오목한 형상·뺨 접촉 | 실제 경도/유연성은 미확인, 돌무늬 천 대조 |
| C04 내부 손잡이 | 같은 잔 내벽의 두 접합·열린 고리·손가락 소유 | 보이지 않는 모든 외벽의 손잡이 부재를 강제하지 않음 |
| C05 실내 구름 | 실내 경계·독립 덩어리·탁자/천장 사이 간격 | 벽화·조명·솜·김 대조 |
| C09 거대 찻잔 청소 | 같은 깊이·정상 싱크대·바닥 접지·실제 닦는 손 | 거대 배경/정상 찻잔으로 대체하지 않음 |
| R11 우산 그림자 | 닫힌 실물·펼쳐진 그림자·하나의 연결 수광면 | 다른 우산 그림·복수 광원과 구분 |
| R13 봉제 문틀 | 천 단·봉제 경첩·접힌 같은 외피·나무 기준 | 정상 문 앞 커튼과 구분 |
| R16 마른 예외 구역 | 강우/젖은 바깥·마른 안쪽·같은 포장 연속 | 물의 패턴과 보이지 않는 차양 부재를 혼동하지 않음 |
| R17 서리 가지 | 같은 가지의 두 전환 경계·서리 결정·녹색 구간 | 실제 계절/온도/성장 과정과 구분 |

위 9개는 데이터 작업의 시작 묶음이다. 전역 의미 중복 검토나 관측성 검토에서 같은 source가 확인되면 재사용으로 바꾸고, 단순 변주가 늘어나는 후보는 등록하지 않는다. 9건을 반드시 모두 채택하는 quota는 없다.

## 5. 카드별 source 저술 절차

각 실제로 반영할 카드에 대해 다음을 수행한다.

1. 인용 이웃 source의 전체 원문, 실제 RID, 조건, 효과, component/application contract를 읽는다. 루트 제목·태그·연구 그래프만 보고 재사용하지 않는다.
2. **동일 완성 관계**면 기존 CID를 보존해 재사용한다. **기존 의미를 보존하는 번역/명료화**면 그 CID의 scoped diff로 정제한다. 대상·재질·상태·끝점·사용 관계가 달라지면 **새 완성 변형**으로 독립 저술한다.
3. 새 CID/binding ID는 repository 규칙에 맞춰 안정적으로 발급한다. 연구 ID(C01/R11 등)를 운영 CID로 사용하지 않는다.
4. EN/KO 모두에 같은 대상 수·소유자·상태·접촉·연속/분리·재현 매체를 보존한다. 영어의 한 장면과 한국어 제목만 대응시키지 않는다.
5. 시각적 positive proposition과 적용 한계/진단을 구분한다. ‘미래’, ‘자율성’, ‘실제 온도’ 같은 비가시 개념을 alias로 붙여 완료된 것처럼 검색시키지 않는다.
6. source가 바꾸는 실제 dimension과 property를 카드마다 저술한다. 모든 카드에 전체 dimension union이나 `concept` 하나만 기계적으로 붙이지 않는다. 객체 geometry·material·light·relationship 등의 실제 영향과 owner를 점검한다.
7. frozen owner가 필요한 source라면 정확한 현재 지원 소유자/전제/선택 계약을 별도로 만족시킨다. 연구 owner graph가 이 권한을 공급하지 않는다.
8. 선행 prerequisites/조건을 약화하지 않는다. broad effects가 불편하다는 이유로 삭제하지 않고 별도 근거 검토를 한다.
9. 연구 metadata·source refs·영어/한국어 전문을 해시로 연결한다. 출처 digest가 실제 웹페이지 바이트인지 연구 사양 바이트인지 구분한다.
10. 필수 관측 대상은 선택한 후보의 원문 전체에 한정한다. 설정만으로 전 후보의 조건이 한꺼번에 활성화되거나 새 보편 체크리스트가 생기지 않게 한다.

## 6. 의미/발견 경로

`discovery-routes.json`을 작성용 출발점으로 사용한다. 관계별 한영 자연어·혼동 경계와 source 대상을 연결한다.

- `surreal=1/2/3`을 후보 alias나 검색 가중치로 넣지 않는다. 설정 할당은 topic query에서 제거되고, 저술된 baseline·role 의도에서 실제 관계가 발견되어야 한다.
- ‘초현실’, ‘몽환’ 같은 넓은 말만 반복하지 않는다. 내부 손잡이/inner handle, 반사에서만 꽃이 핌/reflection-only blossom처럼 실제 관계의 검색 표현을 쓴다.
- 서정·온화함·공포·유머는 맥락적 표현 의도다. 해당 단어가 나왔다고 특정 후보를 필수로 만들지 않는다.
- 기존 `surreal_concept` catalog 설명은 명시적 현실 이탈 중심이고, `surreal_physics_detail`에는 정상 정합성 이웃도 있다. 이 문구·연결의 개선 필요성은 별도로 검토하되, data patch에 숨겨 retrieval 동작이나 requester lock을 바꾸지 않는다.
- 정상 반사·광원 일관성은 supporting realism으로 구분한다. 태그를 정리하더라도 현재 전역 검색의 인구나 native 조건을 은밀하게 바꾸지 않는다.
- 진단 기록은 `record_kind=diagnostic` 또는 현재 동등한 제외 경로로 보관한다. 16개 진단을 긍정 후보 수에 합산하지 않는다.

## 7. 데이터·검색 검증

구조 검증은 현재 도구를 사용한다. 단순 문서 수정만의 전역 suite 실행은 필요 없지만 실제 module/index를 바꾸면 관련 integrity 검사를 수행한다.

```bash
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

위 `.venv`가 현재 환경의 NumPy/임베딩 의존성을 충족하지 않으면 runtime check가 보고한 스킬 전용 Python을 사용한다. 이 명령들을 이번 리서치의 실행 결과로 오해하지 않는다. 실제 반영 시 exact help와 지원 환경을 다시 확인한다.

필수 데이터 확인:

- ID/module 소유권·한영 원문·조건/effects·binding·진단 제외·source hash 참조가 유효하다.
- 기존 source/policy/catalog가 허용 diff 밖에서는 그대로다.
- alias·정의 등 검색 문장을 바꿨으면 해당 문서의 recipe/text hash를 갱신하고 새/변경 문서 벡터를 검증한다. 변경 없는 문서는 정확한 text/model/recipe/proof가 일치할 때만 재사용한다.
- native source qualification, role approval, 검색 노출은 따로 기록한다. H-F2의 `native_approval=false` 자체는 오류가 아니며, source 전체 채택 권한도 아니다.

검색 비교는 **관계 요청 20개와 정상/경계 요청 20개**, 각각 한국어·영어로 총 80질의를 개발 세트로 준비한다. 사례는 `retrieval-evaluation-plan.json`에 있다. 같은 저술자가 후보를 보고 작성한 개발 질의를 독립 holdout이라고 부르지 않는다. 별도로 후보 원문을 보지 않은 실제 요청/paraphrase를 확보해 평가한다.

현재 설치 세대와 staged 세대에 같은 입력을 사용해 실제 H-F2를 측정한다. lexical-neighbors.json의 연구용 BM25 수치를 그 결과로 재사용하지 않는다. 각 질의의 lane 호출·CID/RID·source hash·rank/sample window를 보존한다.

평가 항목은 목표 관계의 노출, 잘못된 매체/소유자/상태의 노출, 정상 대조에서의 불필요한 초현실 제안, 온전한 의미를 사용할 수 있는지다. 정상 질의에서도 optional 재료가 나올 수 있는 recall형 검색이므로 **노출 자체**와 **최종 잘못된 추가**를 구분한다. `surreal=0`을 이유로 사용자 명시 판타지를 제외시키는 회귀도 별도 검사한다.

## 8. staged 세대와 설치

1. source module이 완성되면 native와 H-F2가 같은 canonical pool을 가진 독립 세대를 만든다. 현재 저장소의 whole-pool build/qualification 경로를 사용한다. code-only stager로 데이터 변경을 위장하지 않는다.
2. 새 source/문서/벡터/통계/코드 inventory와 두 세대 ID를 저장한다. 설치본과 다른 코드 변경이 섞였으면 별도 diff와 qualification을 요구한다.
3. 데이터 범위, 실제 검색 비교, receipt replay 및 필요한 focused tests를 exact staged generation에서 검증한다.
4. 기존 설치 세대를 보존한 채 `--no-activate`로 설치·런타임을 확인한다.
5. 검증이 끝난 정확한 같은 세대를 활성화하고 `retrieval-runtime.json`을 실제 영수증과 대조한다. research-only 레지스트리 파일은 누락/과다 설치 여부를 확인한다.
6. 새 managed run이 새 세대를 바인딩하는지 확인한다. 기존 run은 원래 세대와 frozen source를 유지한다. 현재 native `CURRENT`에 대한 불필요한 쓰기는 하지 않는다.

```bash
python3 skills/photo-prompt-image-generator/scripts/install_photo_h_f2_runtime.py \
  --source-store QUALIFIED_STORE --generation-id QUALIFIED_ID --no-activate
# exact same verified store/id, activation only after qualification
python3 skills/photo-prompt-image-generator/scripts/install_photo_h_f2_runtime.py \
  --source-store QUALIFIED_STORE --generation-id QUALIFIED_ID
```

이 경로는 이미 qualified된 세대를 설치하는 절차이며 새로운 데이터나 이미지 품질을 승인하는 명령이 아니다.

## 9. 이미지·강도 검증

이미지 생성은 후속 요청에서 실행한다. `calibration-plan.json` 8군은 비교 설계이고 아직 frozen run이 아니다.

첫 단계는 Pro의 현관 화분·독서 구름·거대 찻잔·사용자 지정 용 보존 4군×4단계=16장이다. 실제 관계가 판독될 때 같은 4군의 3반복, 총 48장 파일럿으로 확장한다. 인물 없는 우산·자연 서리·건축 외피·도자 커튼 군을 후속 범위로 포함한다. 독립 seed 지원·반환 모델·화면비·원본 크기는 실제 응답대로 기록한다.

각 arm은 실제 사용자 요청의 정확한 envelope, controls, 독립 core, feature selection, embodiment review를 freeze한 뒤 현재 관리 흐름으로 검색·비교·compose audit·render를 수행한다. 다른 강도 arm의 프롬프트나 후보를 첫 baseline 영감으로 섞지 않는다. 실험 통제를 위한 보존 조건은 실제 사용자가 정한 실험 요청에만 기록하고 일반 창작 요청의 lock으로 옮기지 않는다.

픽셀 리뷰는 다음을 분리한다.

1. 사용자 소유의 주제·행동·참조 범위·명시 판타지가 보존되는가.
2. 선택한 완성 관계의 모든 핵심 owner/경계/접촉/상태가 같은 프레임에서 관측되는가.
3. 정상적인 경쟁 해석과 비교해 의도한 관계가 읽히는가.
4. 그 관계가 사진 전체에서 보조·명확·주도의 어떤 역할을 하는가.
5. 주된 인상·정서·작품 선호가 어떤가.

3~5는 선택 장면의 해석·평가이며 새로운 universal hard gate로 자동 편입하지 않는다. 1~2의 기존 hard duty는 partial/unobservable이면 해당 완전 관계의 pass가 아니다. 설정 3에서도 사용자 의미를 제거하거나 원문 계약을 축소해 난도를 낮추지 않는다. 실패한 모든 호출을 분모에 남긴다.

## 10. 완료와 롤백

각 단계를 별도로 완료 판정한다.

| 단계 | 완료 증거 |
|---|---|
| 연구 | 원본 취득, 출처 범위, 이웃 source별 결정, 새 관계/진단/평가 계획 |
| source 반영 | allowlist diff·한영·조건/effects 검토, 구조 검사 |
| 검색 반영 | staged 세대·정확한 vector/recipe·실제 질의·receipt replay |
| 최종 저술 활용 | source별 결정, 대안 비교, literal evidence와 compose audit |
| 이미지 | 저장된 원본·실제 관계 가시성·강도 역할·실패 분모 |
| 사용자 수용 | 실제 사용자 판단. 에이전트의 PASS로 대체하지 않음 |

문서·메타데이터의 통과만으로 충분한 시각 표현을 입증했다고 하지 않는다. 이미지까지 수행하지 않는 데이터 출판은 그 한계를 명시하면 가능하다.

롤백 시 이전의 검증된 H-F2/native 세대를 다시 선택하고 이전 `retrieval-runtime.json`과 영수증을 대조한다. 새 세대·원본·실패 증거는 지우지 않는다. source rollback은 이번 CID/module allowlist만 대상으로 하며 사용자 선행 변경과 다른 연구 모듈에는 쓰지 않는다. 기존 run이 새 세대로 재바인딩되지 않았는지 확인한다.
