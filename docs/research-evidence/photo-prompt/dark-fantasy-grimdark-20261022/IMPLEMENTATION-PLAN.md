# 리서치 결과 반영 계획

상태: 연구·설계 완료 / 운영 반영 전. 2026-10-22.

목표는 247개 용어를 247개 자동 의무로 만드는 것이 아니다. 요청자가 정한 의미를 먼저 보존하고, 필요한 구체적 표현을 발견·비교·선택·검증할 수 있게 한다. 72개 카드는 P0 45개, P1 27개이며 신규 CID 수가 아니다. P0 중 4개는 문맥 경계 카드이므로 긍정 시각 후보를 만들지 않는다.

## 단계별 범위와 완료 조건

| 단계 | 할 일 | 완료 증거 | 다음 단계로 넘기지 않을 상태 |
|---|---|---|---|
| 0 재기준화 | dirty/untracked·소스/검색/설치 포인터 확인, 독립 작업 공간 확보 | 정확한 HEAD와 source SHA, manifest closure, 변경 allowlist | 조사와 최신 작업 상태를 혼합 |
| 1 의미/재사용 판단 | 247개 route와 72개 카드에 reuse/refine/new/context/defer 결정 | 실제 CID/RID, 원문과 필요한 관계의 차이, 원전 범위 | 어휘 0건을 바로 new로 처리 |
| 2 소스 저술 | 선택한 실현의 한영·소유·조건·효과·완전 의무 | full source review, source-unit/native 자료, 번역 검토 | 연구 메타데이터를 native 권위로 사용 |
| 3 구조/회귀 | dictionary 및 영향받은 의미/락/역할 검증 | scoped checks와 실패 사례의 음성 결과 | broad label로 의무가 켜짐 |
| 4 별도 인덱스 | staging에서 검증된 공간으로 임베딩·빌드 | exact model/recipe/hash/coverage, 독립 verify | 현행 manifest/CURRENT에 미검증 게시 |
| 5 검색/선택 | 한영 56개 개발 사례와 별도 독립 holdout | query·lane·실제 CID/RID·노출·선택 이유·오탐 | 순위/태그만으로 의미 적합 판정 |
| 6 이미지 비교 | 12개 핵심 사례의 3 arm 비교, 필요할 때 반복 | prompt·runtime·원본 픽셀·전체 장면의 별도 기록 | 가려진 접점·부분 표현을 합격 |
| 7 설치/마감 | 변경을 봉인·검증한 뒤 정책에 맞게 설치/활성화 | 설치 세대/포인터·롤백 경로·전후 증거 | source 변경을 설치본 반영으로 보고 |

## 0. 구현 기준과 작업 경계

현재 체크아웃에는 다른 진행 중 변경이 많다. 이 연구 폴더만 별도 산출물로 남겼으며 기존 소스·테스트·포인터를 되돌리지 않았다. 실제 구현은 별도 작업 공간/검토 가능한 브랜치에서 시작한다. 필요한 dirty 변경을 명시적으로 목록화하고, 현재 파일을 stash/reset/restore하는 방식으로 격리하지 않는다.

`BASELINE.json`은 시작 시점 증거다. 조사 중 manifest와 설치 포인터가 움직였으므로 새 구현 시점에 재기준화한다. corpus audit의 49개 모듈 해시는 그 읽기 스냅샷에만 적용한다.

현재 문서에 있는 읽기 전용 진입점은 다음과 같다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

후속 NumPy 유지보수에는 출력의 `runtime_python`을 쓴다. 현재 작업 소스, 검색 manifest, 선택된 sealed code/data generation의 세대를 각각 기록한다. 연구 폴더의 본문·초안은 precore 입력이나 runtime registry가 아니다.

## 1. 채택 판단과 우선순위

우선 P0의 가시 카드 41개와 문맥 경계 4개를 처리한다. 공간 D01~04/D06/D09~14, 사물 O01~09/O12, 사회 R01/R02/R05~08/R12, 연결 M01~04/M06~08/M12, 빛/물성 F01~04/F06, 문맥 X05~08이 대상이다. P1 27개는 장소·원전·정황·성인 외형의 대안을 확장한다. 이 순서가 자동 채택/생성 할당량은 아니다.

각 카드의 결정은 다음을 포함한다.

- `reuse`: 기존 CID와 선택 RID의 조건·원문·추가 세부·의무가 모두 맞는 경우. 연구안의 짧은 문장으로 기존 소스를 축약하지 않는다.
- `refine`: 실제 공백이 표현/번역/질의 지원에 있고 원래 의미를 보존할 수 있을 때. source diff와 인덱스 갱신 필요를 기록한다.
- `new`: 필요한 구조·소유·관계가 기존 complete source로 충족되지 않는 경우. 가장 가까운 기존 CID와 정확한 차이를 남긴다.
- `context`: 서사·원인·동의·의도·감각·평가로 남길 경우. 긍정 시각 단위나 강제 profile로 우회하지 않는다.
- `defer`: 원전/정의가 아직 약하거나 매체가 맞지 않을 경우. 추가 근거와 재개 조건을 적는다.

18개 기본 레코드와 추가 topology 이웃을 먼저 검토한다. `living armor`의 hollow/animated, organic shell with gap, worn organic interface는 별개 branch다. `ossuary/necropolis`, `chiaroscuro/tenebrism`, 일반 grimoire/특정 신화 금서도 이름을 합쳐 의미를 넓히지 않는다.

## 2. 후보와 의미 자료의 반영 위치

예상 경로이며 이번 조사에서는 만들지 않았다.

| 파일 | 역할 |
|---|---|
| `assets/photo_dark_fantasy_grimdark_semantics_20261022.json` | 출처·원전·카드·채택 판단의 추적용 레지스트리. native 소스 의미/effect의 두 번째 권위가 되지 않음. |
| `assets/photo_candidate_dark_fantasy_grimdark_20261022.json` | 승인된 신규 V3 소스만. 재사용 소스의 CID는 보존. |
| `assets/photo_candidate_dark_fantasy_grimdark_bindings_20261022.json` | 실제 149개 catalog 의미에 맞춰 검토한 역할 연결만. |
| `assets/photo_candidate_corpus_manifest.json` | 검토한 모듈의 명시 등록. |
| 필요한 기존 owner 파일 | refine하기로 결정한 CID의 소유 파일만 수정. shard 전체 일괄 재작성 금지. |
| `references/dark-fantasy-grimdark-semantics.md` | 유지보수 기준·원전 범위·혼동 경계. 일반 요청의 precore 재료로 노출하지 않음. |
| 영향받은 테스트/fixture | 한영·소유·락·오탐·시간/감각 경계의 회귀. |

새 필드가 loader 계약에 없는 경우 먼저 허용 필드와 버전을 검토한다. `research_*`를 넣고 validator가 무시하길 기대하지 않는다. `candidate-drafts.json`은 loader 입력 형식이 아니며 CID/RID/native proof가 없다.

각 소스에는 실제 선택된 실현의 한영 긍정 문장, 각 entity/part의 소유, 모든 endpoint, 전제, intrinsic effects, 조건부/원자 의무를 직접 저술한다. registry의 claim limit·부정 예·비평 해설을 embedding text나 긍정 프롬프트에 섞지 않는다. negative는 기존 소유/승인 경로를 보존한다.

번역은 단어 대응뿐 아니라 ‘같은 착용자’, ‘안쪽 테두리’, ‘양쪽 접합’, ‘세 사슬 전부’, ‘창을 통해 보이는 내용’, ‘어둠 우세’를 양 언어에서 보존해야 한다. 소스 필드마다 필요한 literal support를 남기며 별칭/메타데이터를 긍정 사실의 증거로 쓰지 않는다.

## 3. 소유자·효과·슬롯 검토

슬롯 제안은 현재 catalog에 존재함을 확인했지만 native 의미 승인은 아직 아니다. location에 어울리는 후보를 mood/narrative/genre에서도 자동 direct 승인하지 않는다. intrinsic 조건을 먼저 적용하고 role 조건을 바인딩/요청별 unbound proposal로 우회하지 않는다.

| 사례 | 정식 반영 전 반드시 해결할 것 |
|---|---|
| O03 향로 | 위 고리·손·용기·각 사슬의 양끝·연기 시작점. 실제 사슬 수를 정확히 선언하고 모든 연결 검토. |
| M07 생체 갑옷 | 판/덩굴/노출 피부가 선택한 동일 착용자 소유인지. 기존 빈 갑옷/외피 gap과 분기. |
| M06 몸 융합 | 두 몸의 신원·연속 조직·양쪽 접점. 수/몸/의상·관계 변경 effect 전부. |
| R07 수호 | 방패와 비인간/피란민을 별도 owner로 분리. 화살은 방패에 박히며 인체에 이식하지 않음. |
| X01 성인 근접 | 두 성인과 각자의 손·시선·거리. 욕망·합의·관계 성립을 시각 fact로 만들지 않음. |
| D02 묘실 | 실제 열린 벽/절개 모형/도해 매체를 분기. 사진 요청에 설명 없는 건축 도해를 추가하지 않음. |
| F09 수척함 | 창백·야윔·의상 여유를 서로 다른 branch로 검토. 진단·사망·굶주림을 외형에 붙이지 않음. |
| F06 천체 | 붉은 달과 일식의 천체/빛 관계를 별도 branch로 저술. |

기존 owner를 변형하는 경우 실제 요청에서 independently grounded owner와 전제를 선택한다. 숫자/인체/의상/배경을 단어 하나로 암묵 생성하지 않는다. 조사 카드의 `owners`는 runtime의 frozen owner가 아니다. native guards·선택 closure·원문 의무와 mutation footprint를 함께 검토한다. 아직 모르는 effect를 ‘변경 없음’으로 등록하지 않는다.

## 4. 변화에 맞는 검증과 인덱스

현재 존재하는 관련 진입점은 dictionary validator 및 `test_h_f2_semantic_boundaries.py`, `test_h_f2_primary_proof_boundaries.py`, `test_h_f2_source_context.py`, `test_h_f2_gap_sources.py`, `test_h_f2_sampling.py`, `test_h_f2_validation_context.py`, `test_topic_context_and_negative_policy.py`다. 실제 변경한 계약의 사례부터 실행한다. 자료 보강만으로 해결되는 문제에 engine 변경을 추가하지 않는다.

필수 음성 회귀는 다음과 같다.

1. 빈 갑옷을 생체 착용 갑옷으로 채택하거나, 기존 gap을 접합으로 바꿈.
2. 조직 접점 한쪽이 가렸는데 양쪽 접합을 통과시킴.
3. 세 사슬 중 한 가닥이 용기와 분리됐는데 향로 전체를 통과시킴.
4. 배수 없는 장식에 gargoyle이라는 이유로 물을 추가함.
5. 보이는 금속 손 모양 함을 실제 손/성유물 내용으로 판정함.
6. 암호화의 crypt substring이나 고스 머리색을 묘실/고딕 서사 의미로 채택함.
7. 단순 저노출를 chiaroscuro/tenebrism의 완전 구현으로 통과시킴.
8. 장르만으로 미선택 profile·성적 의미·인물·해부학·사건을 강제함.
9. 동의·혈연·악취·실제 사망·영구 불사·집단 파괴 의도를 픽셀로 판정함.
10. source/RID/역할/의무가 바뀌었는데 이전 native proof·receipt를 재사용함.

인덱스는 별도 전체 staged skill에서 만든다. 현 search manifest가 선언한 local embedding 모델/차원/recipe를 구현 시 다시 검증한다. 현재 관찰은 `embeddinggemma2-local`, `google/embeddinggemma-2`, 768차원이다. source text/ID/recipe/model/revision/space/vector integrity가 일치하는 기존 벡터만 재사용하고 바뀐 문장은 재계산한다. 원격 모델로 자동 우회하지 않는다.

다음은 **미실행 예시**다. 경로 변수는 구현 시 확정한 절대 staging 경로이며 현재 운영 assets를 가리키지 않는다. CLI의 해당 옵션 존재만 소스로 확인했다.

```sh
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$STAGED_SKILL/assets" --backend embeddinggemma2-local \
  --cache "$BUILD_CACHE" --batch-size 32
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$STAGED_SKILL/assets" --backend embeddinggemma2-local --verify
```

빌더는 주어진 assets의 manifest를 바꿀 수 있으므로 원본 assets에서 실행하지 않는다. `--output-assets`와 `--publish`를 혼합하지 않는다. full source·문서 수·통계·payload·posting/vector 범위·routing/closure를 검증하고 모델 추론/재사용/캐시 수량을 기록한다. 소스가 바뀌면 재기준화한다. staged verify는 설치/활성화가 아니다.

## 5. 검색 평가와 종료 기준

EVALUATION-CASES.tsv는 development 24, boundary 16, ordinary control 12, nonvisual control 4의 **56개 사례, 112개 한영 질의**다. 연구자가 카드와 함께 작성했으므로 개발 코호트다. 별도의 사용자/독립 작성 자연어 holdout을 구현 시작 전에 고정한다. 숫자만 늘린 재서술을 holdout으로 부르지 않는다.

각 질의는 frozen core·슬롯/역할 의미·언어·창의성·실제 query bytes·모델/recipe·데이터 SHA를 함께 고정한다. 요청 의미와 기존 owner/락은 후보를 보기 전에 작성한다. 현행 creativity별 순위 창/표본 규칙은 실행 시 코드에서 다시 확인하고 exact seed/receipt와 rank→노출→선택을 구분한다. 모든 149개 슬롯을 같은 장르 쿼리로 강제 탐색하지 않는다.

정답은 카드 ID가 아니라 실제 reviewed CID/RID/role와 그 허용 문맥이다. 노출률, 의미 적합도, 의무 완전성, 한영 차이, ordinary control의 오염, context 오판을 따로 집계한다. profile/락 위반과 비가시 의미 자동 확정은 0건이어야 한다. 양성 노출률의 수치 목표는 기준선 결과를 본 뒤 새 데이터에 유리하게 정하지 말고 평가 실행 전에 정한다. 비교에서 떨어지거나 설명되지 않는 오탐이 있으면 해당 자료는 HOLD/defer하며 다른 통과 항목의 수로 덮지 않는다.

## 6. 이미지와 설치

PIXEL-PLAN.md의 36장 첫 비교는 프롬프트·런타임·원본 픽셀·전체 장면 품질을 분리한다. 필수 관계가 가려지면 unobservable이고 부분 통과는 전체 통과가 아니다. 사용자 취향/승인은 에이전트의 기술 판정과 별도다. 연구만으로 실제 생성 품질 개선을 주장하지 않는다.

이미지 호출은 후속 구현/평가 범위가 정해진 때 진행한다. 이번 요청에서는 이미지·임베딩 API나 다른 모델 검토를 호출하지 않았다.

설치는 source/index/승인 artifact를 봉인한 뒤 현재 유지보수 절차로 stage·qualification·비활성 설치·검증·활성화 순서를 따른다. old CURRENT·sealed generation·run history는 복구 경로로 보존한다. 정확한 변경 경로만 커밋하고, 커밋/푸시/PR·설치·활성화를 각각 구분해서 보고한다. 이번에는 구현·커밋·푸시·설치가 수행되지 않았다.
