# 군대물 데이터 반영 계획

2026-10-24 KST. 이 계획의 입력은 전체 원문 393행, 시각 초안 104개, 문맥 구분 52개, 출처 포인터 40개와 기존 후보 감사 결과다. 현재 작업은 연구 파일 작성까지다. 아래 운영 파일 작성·설치·이미지 호출은 실행하지 않았다.

## 목표와 완료 기준

군대물 요청의 생활·의례·장구·정비·전투·함정·항공·귀환·성인 패션 범위를 넓히면서, 사용자가 정한 의미·인원·포즈·옷·매체·접점을 보존한다. 신규 후보 수를 목표치로 삼지 않는다. 기존 완결 소스 재사용과 문맥 경로 보존도 강화 결과로 센다.

완료는 다음 증거를 각각 가진 상태다.

1. 393개 원문 행마다 `reuse/refine/new/context/defer` 결정, 관련 source 또는 보류 이유가 있다. 한 복합어를 구성요소 하나와 동의어로 만들지 않는다.
2. 등록한 각 CID/RID에 완결 한영 문장, intrinsic 조건·effects, 소유자·연결·선택 branch·기존 구성원 의존성이 있다. 연구 그래프는 proof를 대신하지 않는다.
3. 변경한 소스와 필요한 인접 계약의 검사가 통과한다. 변경 전후 source closure와 runtime selection을 기록한다.
4. 정확한 최종 source union으로 staging 검색을 만들고, 같은 질의를 원본·stage에서 비교한다. 등록·native qualification·설치 검색 노출은 별도 판정이다.
5. 실제 이미지 검증을 진행할 경우 독립 작성 입력·전체 채택 소스·전송 prompt·receipt·저장 픽셀의 접점 검토까지 연결된다. 차단·미관찰·일부 성공을 전체 PASS로 올리지 않는다.

연구 구조 검증만 끝난 현재 상태에 위 2~5의 완료 표시를 붙이지 않는다.

## 0단계 — 변경 경계를 고정한다

연구 시작 시 HEAD는 `52128de98276e8987abe28ded90292affaaf7768`였고 tracked 파일만 수정 29개·삭제 2,454개가 있었다. untracked 변경도 별도로 존재했다. 이 수치는 깨끗한 원본이라는 의미가 아니다.

- 구현 시작 때 현재 HEAD·manifest closure·원문 모듈 해시·binding·slot catalog·`retrieval-runtime.json`·native generation을 다시 읽는다.
- 작업 트리에 연구 당시 변경이 남아 있으면 적절한 현재 checkout이나 작업용 worktree에서 진행한다. 오래된 연구 snapshot을 최신 구현 원본으로 덮어쓰지 않는다.
- 기존 데이터는 실제 재사용/보완 대상만 명시적으로 변경하고 allowlist를 남긴다. 본 연구 폴더 밖의 미완료 작업을 포함하지 않는다.
- 현재 설치 선택 snapshot은 [runtime-selection.snapshot.json](runtime-selection.snapshot.json)에 있다. 설치 generation은 연구용 authored manifest와 별도 상태다.

## 1단계 — 우선 추가 확인할 자료

| 우선 | 대상 | 조사할 구체 사항 | 통과 조건 |
|---|---|---|---|
| P0 | 한국군 복제·계급 표장 | 국가·군종·시기·용도·계급별 공식 도판과 배치 | 문서 버전·정확한 도판 위치·관찰 내용이 연결됨 |
| P0 | 경례·어깨총·받들어총 | 국가·무기·행사별 실제 그림, 손바닥·총·손·어깨 관계 | 관찰한 한 변형만 한영 완결 대안으로 작성 |
| P0 | 캐리어·리그·PALS·슬링·하네스 | 수납·장착·지지·몸/옷의 층과 숨은 내부 | 필수 접점이 존재하며 성능을 외형으로 주장하지 않음 |
| P1 | 한국 병영생활 | 특정 시기의 생활관·관물대·점호·불침번·PX·급식 | 제도·속어 정의와 실제 장면 자료를 분리 |
| P1 | 역사 군복 | 돌먼·펠리스·브리치즈·샤코·버스비·퍼티·Battle Dress | 국적·연식·accession·착용/물체 표본 구분 |
| P1 | 차량·항공·함정 | 전차/자주포, APC/IFV, 헬기 객실, 함교·격벽·해치 | 유형 역할과 특정 모델의 보이는 구조를 분리 |
| P1 | 소화기·포·탄약 표본 | 총검·박격포·곡사포·견인포·탄약/탄창/클립 | 부품과 완제품·역할·모델 경계, 단순 실루엣 오인 사례 기록 |
| P2 | 색·소재·센서 | 색명과 표본 조명, 소프트아머 단면, 대즐, 열/광증폭/융합 | 실제 도판·센서 화면·실물 경계를 확인한 범위만 주장 |
| P2 | 성인 코스튬·서브컬처 | 핀업·택티컬 메이드·비키니 아머·젖음·하네스의 디자인 경계 | 실제 군복과 허구 디자인 분리, 노출·성적 행위 자동 추가 없음 |
| P2 | 문맥·비평 용어 | 절차어·프래깅·War porn·Nazisploitation 등 | 적절한 1차 설명·비평/서지 출처와 해석을 구분 |

검색 결과의 발췌만 본 자료는 본문·도판 확인 전 상태를 유지한다. 403을 받은 자료는 정식 대체 출처나 브라우저 공개 본문으로 보완한다. 이번 연구에서는 이 후속 도판 검토가 끝났다고 표시하지 않았다.

## 2단계 — 전체 키워드 결정을 확정한다

[keyword-atlas.json](keyword-atlas.json)에 아래 구현용 결정 컬럼을 추가한 별도 작업표를 만든다. 연구본은 보존한다.

| 결정 | 기준 | 다음 작업 |
|---|---|---|
| reuse | 같은 완결 문장·모든 조건·부수효과가 목적에 맞음 | 기존 CID/RID 유지, 필요할 때만 검토된 optional binding 추가 |
| refine | 기존 소스의 번역·관계·별칭·효과 범위에 구체적 문제 | 바뀌는 의미와 영향 범위를 기록, 필요하면 별도 대안 선택 |
| new | 전체 기존 소스와 의미를 비교해 새 완결 실현이 필요 | 새 ID, 원문·조건·전체 effects·조건부 branch 작성 |
| context | 제도·동기·진단·법적 지위·소리·시간·비평 등 | 보존하되 positive 시각 후보의 별칭이나 효과로 승격하지 않음 |
| defer | 표본·정의·접점·현행 스키마가 불충분 | 필요한 자료·판정 질문·보류 범위를 명시 |

`context`에 고어·피해·행위 같은 보이는 표현이 일부 포함될 수 있다. 그 개념 전체를 한 부분 카드로 정의할 수 없다는 뜻이며 삭제·비가시 분류의 확정은 아니다. 실제 등록은 더 좁은 시각 실현과 원래 문맥을 함께 유지한다. 미세한 인식표 문자·계급장·PALS가 필요한 실현은 화면에서 판독 가능한 크기인지 먼저 검토한다.

기존 감사의 어휘 0건은 신규 작성 허가가 아니다. 전체 bilingual content, 조건, effects, intrinsic guard, 필요 구성원·선택 realization까지 비교한다. 47개 snapshot은 출발점이며 전체 의미 중복 조사 완료를 뜻하지 않는다.

## 3단계 — 기존 후보의 좁은 수정부터 처리한다

1. **경례 번역**: `cand_59849d02f9cc501bb453ac8d42a8ede7`의 EN·KO·concept_units·embedding text를 의미상 맞춘다. 손바닥 방향의 ‘지정한 변형’ 전제를 지우지 않는다. V49의 오른손·왼손을 기존 소스에 무조건 덧붙이지 않는다. source facts·effects·기존 관계 계약에 미치는 영향을 확인한다.
2. **flight deck의 문맥**: `cand_7c21122f9000531c8cc8f8ad22e90b35`는 항공기 조종실의 전체 문장이다. ‘비행갑판’의 별칭을 항공모함으로 확장하지 않는다. 기존 항공 요청의 노출을 유지하는 한정 표현과 별도 항공모함 갑판 대안을 검토한다.
3. **트렌치 재사용**: `cand_5ccf05cc8bd152caaf61d576b37698b8`와 V20을 비교한다. 같은 의미라면 신규 CID를 만들지 않는다. 소스의 모든 여밈·층·효과는 유지한다.
4. **들것 구분**: 기존 바퀴 들것에는 구급대원 2명·바퀴·매트리스가 포함된다. V67의 도수 천 들것으로 이름만 바꿔 쓰지 않는다. 사람 수나 역할이 잠겨 있으면 전체 소스 채택도 그 제약을 따라야 한다.
5. **가터·인쇄물**: 기존 가터 연결은 같은 다리·클립·밴드를 유지한다. 종이 핀업과 항공기 노즈아트는 서로 다른 carrier이므로 별도 대안을 둔다.

성인 군인 역할 모델은 상위 subject 재료로 유지할 수 있지만 세부 의복·계급·장비의 증거를 대신하지 않는다.

## 4단계 — 세 묶음으로 시각 데이터를 작성한다

| 묶음 | 연구 입력 | 구현 핵심 |
|---|---|---|
| A. 연결·착용·지지 | V30~V44, V49~V69, V98~V102 | 장구의 부착, 포즈의 관절·접점·지지, 장치와 매체 경계 |
| B. 생활·의복·공간 | V01~V29, V45~V48, V70~V82, V93~V95, V103~V104 | 비전투 범위, 옷 층, 표장, 신체 차이, 표면과 원인의 분리 |
| C. 성인 패션·표현 | V83~V92, V96~V97 | 그림/실물, 허구/기능, 성인 스타일과 제도·동의의 분리 |

104개는 검토할 설계 대안의 수다. 104개 신규 운영 후보 생성 약속이 아니다. source 비교와 표본 검토에서 재사용·분리·통합·보류가 가능하다. 한국·외국·역사·가상 군복의 임의 조합을 한 묶음에서 승인하지 않는다.

제안 운영 파일은 다음과 같다. 실제 구현 시점의 V3 계약을 다시 확인한다.

- `assets/photo_military_fiction_semantics_20261024.json`: 의미 경계·출처 범위·키워드 route·연구 연결 메타데이터.
- `assets/photo_candidate_military_fiction_20261024.json`: 검토된 완결 한영 visual option과 필요한 excluded diagnostic.
- `assets/photo_candidate_military_fiction_bindings_20261024.json`: 기존 catalog의 실제 role 범위에 맞춘 optional binding.
- `references/military-fiction-semantics.md`: 등록 수·보류·기존 소스 변경·검증 결과·주장 한계.
- corpus manifest: 실제 확정 모듈만 등록. 연구 JSON 경로를 runtime 입력에 넣지 않는다.

각 CID/RID에 다음을 작성한다.

- **전체 positive 문장**: 임의로 한 소스의 손, 다른 소스의 소유자, 또 다른 branch의 전제를 모아 완결된 것처럼 취급하지 않는다. 조건부 대안은 서로 배타적인 상태를 union하지 않는다.
- **조건**: 이미 필요한 사람·옷·장구인지, 해당 실현이 새로 추가하는 것인지 구분한다. 닫힌 캐리어에 내부 판 사실을 만들지 않는다.
- **effects**: 선택 role만이 아니라 source가 실제 바꾸는 인원·나이·주체·옷·포즈·소품·공간·관계·매체를 모두 반영한다. 부분 property lock이 있으면 정확한 target/property를 검토한다.
- **소유·경계**: 신체 부위, 의복, 부착면, 끈 양끝, 지지면, 화면·그림 속 대상의 각각의 owner를 보존한다.
- **한영 동등성**: 영어 관계를 한국어 한 단어로 축약하지 않는다. 별칭은 의미 확장이나 새로운 전제를 공급하는 수단이 아니다.
- **native source review**: 실제 realization의 field-local source anchors·own guards·효과·profile duties를 검토한다. 연구 gate·출처 URL·태그는 source proof가 아니다.

이번 초안의 role 이름은 현행 slot catalog와 대조해 정리했다. 이름의 존재가 실제 source-to-role 적합성을 증명하지는 않는다. 신규 슬롯·보편 군대 장면 template·특정 사건을 강제하는 profile은 우선 만들지 않는다.

## 5단계 — 소스 검증과 검색 설치를 분리한다

현재 checkout에서 지원을 확인한 entrypoint와 유지보수 문서를 따라 단계별로 실행한다. 아래는 후속 실행 순서이며 이번에는 `--check-runtime`의 읽기 전용 확인만 수행했다.

```text
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

데이터를 바꾼 후 사전 인덱스가 stale한 상태는 정상적인 중간 단계일 수 있다. 이전 인덱스의 통과를 새 데이터의 검증으로 기록하지 않는다. 실제 build/publish/install 옵션은 구현 시점의 CLI 도움말, [maintenance.md](../../../../skills/photo-prompt-image-generator/references/maintenance.md), [installed-h-f2.md](../../../../skills/photo-prompt-image-generator/references/installed-h-f2.md)를 다시 확인한 후 확정한다.

변경한 사전·원문·effects·binding·한영 번역·전체 realization 관련 focused 검사를 우선한다. 실패나 변경 범위가 더 넓은 회귀 가능성을 보일 때 검사를 확장한다. 계약을 그대로 복사하는 새 테스트나 거대한 전체 suite를 문서 편집만을 위해 실행하지 않는다.

검색용 문서가 바뀌면 **최종 source union**으로 별도 staging index를 만든다. 문서 ID·전체 텍스트 hash·recipe·provider/model·차원·vector integrity가 모두 같을 때만 기존 벡터를 재사용한다. 새 embedding이 필요한 범위는 실제 설정·도구·비용 권한을 확인해 처리한다. 설치된 H-F2는 sealed source/code/index/vector를 읽으므로 assets 수정이나 native build 통과만으로 기본 검색이 바뀌었다고 보고하지 않는다.

## 6단계 — 검색·채택·프롬프트를 평가한다

[EVALUATION-PLAN.md](EVALUATION-PLAN.md)와 [evaluation-cases.json](evaluation-cases.json)을 사용한다. 개발용 질의와 독립 holdout을 구분한다. 원문·카드를 본 이 연구자가 작성한 질의는 holdout이라고 부르지 않는다.

원본과 stage에서 공통 양성 pool·동일 모델/recipe·동일 질의·정책을 사용한다. BM25F, local embedding/cosine, RRF 결과와 실제 CID/RID/source hash를 기록한다. 주제 전용 pool, 슬롯 prefilter, 키워드 강제 가산점으로 결과를 만들지 않는다. slot별·request topic·baseline 검색을 독립적으로 확인한다.

직접적인 부품 질의는 해당 완결 대안의 검색 노출을, 복합 장르 질의는 오해 없이 선택 가능한 재료의 노출을 평가한다. 문맥어에 무기·폭력·노출·진단이 자동 추가되는지는 **채택·최종 prompt 단계**에서 검사한다. 목록에 후보가 노출된 것 자체와 실제 잘못 채택된 것을 같은 실패로 세지 않는다.

동일 의미를 한영·원어·자연스러운 묘사로 나누고, 올림/내림 NVG·전투복/무늬·인쇄물/기체 그림·군장/패션 하네스·바퀴 들것/도수 들것을 대조한다. creativity에 따라 rank window와 sampling이 달라지므로 원 rank와 실제 sample을 모두 보존한다. seed를 고정할 수 있는 비교에서는 같은 seed를 쓰고, 지원되지 않으면 그 한계를 기록한다.

프롬프트 작성자는 스킬의 독립 authoring 경계를 따른다. 후보·연구 카드·평가 예시를 읽고 작성한 baseline을 독립 입력이라고 표시하지 않는다. 각 실제 요청에서 core를 먼저 동결하고 source·전체 조건을 검토한 뒤 선택한다.

## 7단계 — 실제 이미지 평가는 별도 실행한다

초기 비교는 12개 장면에 대해 원본/확장 **24장**을 제안한다. 이는 실행된 호출 수나 현재 이미지 생성 승인으로 간주하지 않는다. 실제 요청·reference scope·creative controls·모델·비교 예산을 고정한 뒤 수행한다.

장면: 생활관 점호, 슬링 양끝, PALS 부착, 열린 캐리어 판, 올린 NVG, 무전 수화기, 지도 공통 지점, 해치 상체, 도수 들것, 노즈아트, 성인 패션 하네스, 재회 포옹. 각 장면의 모든 핵심 접점은 동시에 읽혀야 한다. 원본에 없는 장비를 확장 조건만의 입력에 적어 두고 검색 개선이라고 주장하지 않는다.

`partial_is_fail`, `UNOBSERVABLE_NOT_PASS`, `BLOCKED_UNSCORED`, `TRANSPORT_FAILED`를 구분한다. 관계 충실도·전체 장면 전달·미감 선호도도 따로 기록한다. 반복 생성은 최초 실패를 지우지 않으며 기술적 검증 통과를 시각 품질 향상·사용자 수용으로 바꾸지 않는다.

## 활성화와 복구

이전 sealed generation과 설정을 보존하고 새 release를 검증한 뒤 기본 선택을 전환한다. 현재 선택이 다른 작업으로 갱신되었다면 최신 source union으로 재검토하며 예전 snapshot을 덮어쓰지 않는다. 실패 시 이전 선택으로 되돌리고 실패 결과는 남긴다.

마지막 보고에는 연구 완료, 원문 등록, source qualification, staging 검색, 설치 선택, 실제 채택, 정확한 prompt 전송, 저장 픽셀, 사용자 수용을 별도 상태로 적는다. 이번 요청에서는 연구와 계획만 완료하며 commit·push·운영 설치는 수행하지 않는다.
