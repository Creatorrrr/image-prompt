# 데이터 반영 계획

상태: 조사·설계 완료 / 운영 반영 전. 2026-10-22.

목표는 200개 용어를 200개의 강제 프로파일로 만드는 것이 아니다. 사용자가 독립적으로 정한 의미를 보존하면서, 현재 부족한 가시 관계를 발견·선택·구현할 수 있게 하는 것이다. 최종 신규 CID 수는 재사용·중복 검토 뒤 결정한다. 이번 구조 초안 128개와 한영 실현안 32개를 그대로 일괄 등록하지 않는다.

## 우선순위와 예상 변경 범위

| 단계 | 대상 | 반영 내용 | 완료 산출물 |
|---|---|---|---|
| P0 | 72개 카드: still 38, proxy 12, advisory 20, sequence 2 | 가시 실현 50개는 재사용/보완/신규 검토. 20개 넓은 개념과 2개 순차 개념은 자동 의무를 막는 경계·평가에 우선 반영. | 72행의 명시적 adoption 결정, 실제 CID/RID 매핑, 자연어·대조 평가. |
| P1 | 97개 카드 | 장소 변주·스케일·소품·얼굴·재질·몸/공간·성인 맥락의 세밀한 구분. | P0와 같은 형태의 소스·번역·효과 검토. |
| P2 | 31개 카드 | 음향·순차 표현·유동적 태그·원전이 더 필요한 비평 맥락. | 별도 매체 대응과 추가 출처 계획. 정지 사진의 의무로 우회 등록하지 않음. |

우선 P0 50개 가시 카드 중 L003/029/041/042/050/054, L061~068, L073~075/080, L090/095/096/102/103/106/109/112, L129/130/135/138/139, L143/144/153/154/155/157 등을 중심으로 고른다. 광각/심도 L146, 신호/광학 L156, JPEG/일반 glitch L158은 P0여도 분기 설계가 먼저다. 실제 카드 전체 목록과 우선순위의 정본은 semantic-cards.json이며 이 문장의 발췌 목록은 할당량이 아니다.

예상 데이터 파일 이름은 아래와 같다. **이번 조사에서는 이 운영 경로에 파일을 만들지 않았다.**

- `assets/photo_liminal_dreamcore_semantics_20261022.json`: 추적용 의미 레지스트리. 실제 의미·effect의 두 번째 소유자가 되지 않도록 한다.
- `assets/photo_candidate_liminal_dreamcore_20261022.json`: 리뷰된 신규 V3 후보만. 재사용할 원자는 기존 CID를 보존한다.
- `assets/photo_candidate_liminal_dreamcore_bindings_20261022.json`: 검토한 역할 관계만. 슬롯 라벨이 소스 의미를 덮어쓰지 못한다.
- `assets/photo_candidate_corpus_manifest.json`: 위 후보·binding 모듈의 명시 등록.
- 필요한 기존 후보 파일: EXISTING-MAPPING.tsv의 23개 CID 중 실제로 refine하기로 정한 소유 파일만. 16개 shard 파일 전체를 일괄 재작성하지 않는다.
- `references/liminal-dreamcore-semantics.md`: 유지보수와 판정 한계. 일반 사진 요청의 precore 재료로 노출하지 않는다.
- `tests/fixtures/liminal_dreamcore/`: 의미 경계·정확 텍스트·owner 오류·검색 평가 자료. 연구 레지스트리를 runtime 권위로 사용하지 않는다.

새 필드가 기존 loader의 허용 계약 밖이면 먼저 버전·허용 필드·primary-text projection·source-unit coverage를 검토한다. 알 수 없는 `research_*` 필드를 넣고 validator가 무시하길 기대하는 방식은 사용하지 않는다. 기존 cosmic/biopunk 레지스트리 형식은 참고 자료이며 소스 자격이나 loader 호환성의 자동 증거가 아니다.

## 0. 현재 상태 재확인과 작업 경계

이번 BASELINE.json은 조사 시작 시점의 증거다. 실제 구현 시작 시 HEAD, dirty/untracked 목록, manifest 모듈·slot catalog·search manifest·installed config·관련 CURRENT 및 sealed generation을 다시 해시한다. 운영 설치본과 working source의 서로 다른 세대를 구분한다.

기존 동시 작업이 많으므로 구현은 독립 작업 폴더/검토 가능한 브랜치에서 수행하고, 필요한 현재 dirty 변경은 명시적으로 목록화해 옮긴다. 현재 체크아웃의 코드·후보를 stash/reset/restore하거나 CURRENT를 되돌리지 않는다. 조사 산출물은 변경 입력으로 사용하되 BASELINE과 다른 소스는 rebaseline 기록을 남긴다.

읽기 전용 설치 확인의 현행 진입점:

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

후속 유지보수 Python은 이 결과의 `runtime_python`을 사용한다. 임의 `.venv`에서 NumPy가 된다고 설치본의 의존성이 확인된 것으로 보지 않는다.

완료 조건: 구현용 기준 SHA·소스 해시·포인터·보존 allowlist를 기록하고, 다른 작업을 변경하지 않는 대상 경로가 확정됨.

## 1. 200개 경로와 기존 23개 CID의 통합 판단

각 카드에 `reuse / refine / new / context / defer` 중 하나를 결정한다. 이 결정은 구조 초안과 별도이며, 한 카드의 대안은 서로 배타적일 수 있다.

1. 기존 primary field·조건·선택 branch·binding·bundle 의존성을 전체로 읽는다. 카드 제목이나 top label만 비교하지 않는다.
2. 같은 원자가 있으면 CID와 기존 제약을 보존한다. `fine film grain`, CCTV 관점, pool-caustic light, hotel corridor를 이름만 바꿔 중복 생성하지 않는다.
3. 새로 필요한 관계가 무엇인지 적는다. 예: 기존 pool 후보를 재사용하되, ‘같은 문틀이 수면 아래 있다’는 관계는 기존 closed-pool 의미만으로 충족되지 않는다.
4. 기존 `underwater caustic`, `after the last train`, `instant-film`, domain deny 등 고유 한정을 일반 표현으로 삭제하지 않는다.
5. `between_use_transition_place`의 넓은 exact_terms와 5요소 특수 실현을 검토한다. 해당 특수 실현을 유지하거나 선택형으로 세분화하되, broad label만으로 의미를 추가하는 경로는 따로 수정·회귀한다.
6. 민감한 항목도 분석 경로를 유지한다. 외형·피해·동의·원인·서사·정서를 한 effect로 합치지 않는다.

완료 조건: 200행이 모두 판단됨. 새 항목은 필요 관계와 가까운 기존 CID를 설명하고, defer는 이유·추가 근거·후속 매체를 남김. 23개 기존 mapping은 통합 후보 목록이지 native 승인 목록이 아님.

## 2. 리뷰 가능한 소스 레코드로 저술

각 선택 실현에 한영 positive phrase, owner graph, 완전한 관찰 성분, 조건, effect, 주장 한계의 저장 위치, 출처 범위를 작성한다. REALIZATIONS.tsv의 문장은 시작점이며 출처·언어·owner 의미를 재검토해야 한다.

| 대상 | 반드시 기록할 관계 | 변경 허용 범위 검토 |
|---|---|---|
| 물·공간 | 수면과 동일 계단/문틀, 두 방과 실제 개구부, 반사 대상과 수광면 | location, object_structure, 액체/습윤, reflection, lighting이 실제로 무엇을 바꾸는지 전부 열거. |
| 얼굴 | 실제 인체, 별개 천, 사진 표면의 블러, 작은 원거리 인물 | 기존 subject/얼굴/복장/기록 락에 대한 변경을 구분. |
| 매체 | 실제 방, 화면 물체, 표시 영상, 후처리 캡션 | 오류 범위가 전체 이미지인지 화면 내부인지 명시. |
| 스케일 | 비교자와 같은 지면, 뿌리/발/밑면, 명시한 두 endpoint | 새 성인·사물을 추가할 권한까지 포함. |
| 구속·의료·성인 문맥 | 실제 접촉·장치·anchor, 명시한 성인 맥락 | 실제 동의·욕망·진단·사망을 자동 부여하지 않음. |

연구용 `claim_limit`, 부정 예, 원전 해설, 정서 라벨은 검색용 긍정 사실·영문 prompt·embedding text에 합치지 않는다. 검색어 보완은 실제 표현의 한영 대응과 관계를 지원하는 범위로 제한한다. 별칭만 추가해 모든 장르 검색에서 순위 투표가 늘어나는 설계를 피한다.

슬롯 binding은 149개 현행 catalog의 실제 소유 property와 의미를 기준으로 한다. 기본 장소 후보가 관련돼 보인다는 이유로 `mood`, `narrative_core`, `surreal_concept`에 동시에 direct 승인하지 않는다. 기존 owner를 변형하는 후보는 현재 요청에서 실제 owner 선택과 전제의 독립 증거가 필요하다. source 조건은 binding이나 unbound proposal로 우회할 수 없어야 한다.

완료 조건: 채택한 모든 CID/RID의 full source와 번역이 리뷰되고, source의 조건·한정·effect가 누락되지 않음. 레지스트리·슬롯 tag·연구 보고서 자체는 자격 증거로 사용하지 않음.

## 3. 구조·의미·회귀 검증

먼저 현행 dictionary validator를 별도 작업 소스에서 실행한다. 변경에 따라 현재 존재하는 `test_h_f2_semantic_boundaries.py`, `test_h_f2_primary_proof_boundaries.py`, `test_h_f2_source_context.py`, `test_h_f2_literal_text.py`, `test_h_f2_whole_scene.py`, `test_h_f2_sampling.py`의 관련 사례를 실행한다. 모든 기존 테스트나 149개 슬롯 전체가 검증됐다고 확대하지 않는다.

새 회귀는 적어도 다음 실패를 구별한다.

- 문이 물 옆에만 있는데 submerged-door로 통과함.
- 물결빛의 수광면 대신 타일 인쇄 무늬를 채택함.
- 얼굴이 가려졌는데 smooth faceless로 통과함.
- 화면 속 얼굴 편집이 실제 인체 변형 effect로 새어 나옴.
- 두 문 숫자가 안 읽히는데 번호 모순으로 통과함.
- 문 밖이 안 보이는 것을 지리적 단절이나 사라진 출구로 확정함.
- 실제 방까지 VHS/JPEG 오류로 변형함.
- 넓은 화각만으로 deep-focus를 통과시킴.
- 빈 방·리미널·Dreamcore라는 라벨만으로 선택하지 않은 하드 프로파일을 활성화함.
- 따뜻한 Dreamcore에 공포 요소·얼굴 결손·폭력을 강제함.
- 동의·상해 원인·생사·소리·시간 변화를 보이지 않는 상태에서 통과시킴.
- 바뀐 candidate source hash나 RID에 옛 native proof·receipt를 재사용함.

완료 조건: 데이터 무결성과 필요한 engine 경계의 focused checks 통과. 자연어 의미 검토는 자동 파싱 PASS와 별도 기록. 문제가 데이터로 해결되면 engine을 수정하지 않는다.

## 4. 별도 인덱스 생성과 검증

현행 작업 트리는 로컬 EmbeddingGemma 2를 쓴다. source text/recipe/model/space/vector integrity가 정확히 맞는 벡터만 재사용한다. 바뀐 후보·표현은 새 문서 임베딩이 필요하며 ‘태그만 바뀌었으니 비용 0’으로 단정하지 않는다. 다른 모델·차원·recipe의 벡터를 섞거나 Gemini로 자동 우회하지 않는다.

구현 후 별도 assets에서 실행할 예시다. 경로 변수는 그때 확정한 **전체 staged skill**을 가리킨다. 현재 프로젝트에서 이 명령을 실행한 것은 아니다.

```sh
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$STAGED_SKILL/assets" --backend embeddinggemma2-local \
  --cache "$BUILD_CACHE" --batch-size 32
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$STAGED_SKILL/assets" --backend embeddinggemma2-local --verify
```

빌더는 주어진 assets의 manifest를 이동시킬 수 있으므로 반드시 staging 경로에서 실행한다. `--output-assets`와 `--publish`를 동시에 쓰지 않는다. full source·posting 통계·payload·vector extent·routing bounds·closure를 검증한다. 빌드 도중 소스가 바뀌면 재기준화하고, 무관한 변경을 되돌리지 않는다.

완료 조건: staged layout 검증, 사용/재사용/캐시/추론 수량, 모델 공간, 변경된 query/document text, 실제 source SHA가 기록됨. 아직 운영 설치·CURRENT 활성화가 아님.

## 5. 실제 검색과 의미 노출 평가

EVALUATION-CASES.tsv의 48개는 development 32, ordinary-control 12, nonvisual-control 4다. 모두 이번 연구를 보며 작성한 개발 코호트이며 독립 holdout이 아니다. 별도의 사용자/독립 작성 자연어 holdout을 새로 고정한 뒤 확장 품질을 판단한다. 카드 ID는 목표 개념 표지이며, 구현 후 검증된 실제 CID와 RID를 매핑해야 정답 집합이 된다.

현재 H-F2는 순위 상위 목록 전체를 그대로 보여 주지 않는다.

| creativity | CID 중복 제거 순위 창 | 쿼리별 표본 한도 |
|---:|---:|---:|
| 0 | 8 | 4 |
| 1 | 32 | 8 |
| 2 | 96 | 12 |
| 3 | 256 | 16 |

따라서 **순위 창 진입**, **발행된 표본에 노출**, **실제 채택**을 나눠 평가한다. 특정 source가 top32에 있다는 사실만으로 사용자가 보는 8개에 포함됐다고 보고하지 않는다.

1. 각 arm에서 사용자 의미·controls·baseline을 candidate-free 상태로 고정한다. 이 연구의 제안 문장을 독립 baseline인 것처럼 쓰지 않는다.
2. 현행 `prepare-slot-intents → seal-slot-intents → retrieve → view` 흐름으로 필요한 슬롯만 별도 저술한다. 두 독립 whole-scene 검색도 그대로 유지한다.
3. 한국어/영어 자연 질의를 따로 실행한다. query text·slot focus·source generation·sampling seed·CID/RID·순위 창·표본·receipt·거절/채택 사유를 저장한다. 슬롯 검색을 whole-scene 검색으로 대체하지 않는다.
4. BM25F, cosine, RRF, 순위 창 및 실제 표본을 따로 본다. source metadata의 라벨 일치가 semantic fit의 증거는 아니다.
5. 먼저 creativity 1에서 네 고정 표본 seed로 비교한다. query embedding을 임의로 새로 만들어 receipt 재현을 맞추지 않는다. creativity 0/2/3은 경계·회귀 대상으로 별도 확인한다.

제안하는 첫 통과 기준은 P0 자연어 관계 질의의 양 언어 `완전 적합 CID/RID Recall@32 ≥ 90%`, 일반 대조군의 리뷰된 precision이 기준 대비 2%p 넘게 악화하지 않음, 요청 락·owner·필수 조건 위반 0건이다. 이는 앞으로 측정할 목표이며 현재 달성치가 아니다. 전체 정답 inventory를 만들지 않은 경우 `Recall` 대신 `목표 후보 노출률`로 명명한다. 표본 노출은 네 seed의 비율과 최악 사례를 함께 보고하고, 순위 지표로 숨기지 않는다.

같은 CID여도 부적합 branch를 찾으면 적합으로 세지 않는다. ordinary control에서 관련 후보가 검색된 것 자체는 실패가 아니다. 해당 후보가 조건을 어기며 채택되거나 넓은 라벨로 의무를 생성하면 실패다. 전부 거절하는 판단도 허용한다.

## 6. 이미지 평가와 운영 전환

필수 픽셀 비교는 PIXEL-PLAN.md의 12군 × 3 arm = 36장 제안에서 시작한다. 이번 요청은 연구·계획이므로 생성 호출은 하지 않았다. 실제 실험 범위와 생성 도구가 확정된 후 수행한다. 자동 prompt audit는 이미지 품질을 증명하지 않는다.

검색·픽셀·의미 경계의 기준이 충족되면 source/index/code closure를 묶어 staged generation을 봉인하고 설치한다. 작업 소스 게시와 installed H-F2 code/data 세대의 채택은 별도 단계다. 현재 포인터와 복구 가능한 세대를 백업한 뒤 검토된 대상만 활성화하고, 새 요청 하나로 실제 세대·receipt·저장 이미지를 확인한다. HOLD가 나면 포인터를 옮기지 않는다.

커밋/푸시가 후속 범위에 포함될 때는 reviewed path allowlist로만 stage한다. 데이터 반영·CI·검색 자격·native source 승인·픽셀 결과·사용자 수용·commit/push/배포 상태를 각각 보고한다. source가 바뀐 후보의 옛 승인 결과를 현재 승인으로 세지 않는다.

## 이번에 완료한 것과 남은 것

완료: 참조 200행 확인, 41개 출처의 범위 기록, 200개 카드와 128개 구조 초안, 32개 한영 실현안, 기존 23개 매핑, 48개 평가 계획, 소유자·근거 링크·무결성 검사.

미실행: 운영 후보 편집, 정식 native qualification, 임베딩 추론, index build/publish, 실제 H-F2 평가, 독립 holdout, 이미지 생성·픽셀 리뷰, CURRENT 활성화, commit/push. 이 경계는 연구 패키지 PASS와 별개다.
