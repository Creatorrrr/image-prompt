# 전기 의미 데이터와 후보팩 반영 계획

연구일 2026-10-08. 이 문서는 후속 구현 계획이며 아래의 구현·인덱싱·렌더 단계는 아직 실행하지 않았다.

## 1. 완료할 결과

같은 ‘전기’ 키워드에서도 사용자의 실제 문맥에 맞는 의미를 찾고, 후보를 채택했을 때 발생원·대상·경로·매질·표면의 연결이 유지되는 데이터를 만든다. broad label이나 검색 유사도로 새 의무를 만들지 않고, 비유·의료·문화·창작 의미를 자연 방전의 고정 형태로 바꾸지 않는다.

완료 상태는 다음 여섯 항목으로 나눠 보고한다.

| 증거 단계 | 완료 조건 |
|---|---|
| 조사·채택 ledger | 원문 seed 및 source-to-component 근거, 남은 조사 항목과 재사용 결정 |
| 원본 데이터 | 선택한 원자의 component·관계·owner·실제 effects가 검증되고 source manifest에 등록 |
| 파생 인덱스 | 같은 원본의 semantic/BM25F/visual manifest·shard·registry hash가 일치 |
| 실제 후보팩 | 동결 core에서 candidate exposure·선택/거절·scope effects·literal evidence를 확인 |
| 결과 이미지 | 별도 요청 범위에서 생성한 원본 이미지의 모든 필수 관계·가림·소유·lock 검사 |
| 사용자 판단 | 의미 충실도와 별도로 예술적 선호·실제 유용성 확인 |

이번 리서치는 첫 단계와 후속 설계까지 완료했다. 나머지 단계의 완료를 연구 통계로 대신하지 않는다.

## 2. P0를 다시 두 묶음으로 나눈다

**P0-A: 12개 원자부터 구현**한다. 각 원자는 current schema·owner binding·property effects를 실제로 검증할 수 있어야 한다. 단일 광원/장치와 종점 관계를 우선해 오류를 좁힌다.

| 묶음 | 연구 slug | 핵심 확인 |
|---|---|---|
| 대전 머리카락 | `radial_static_hair` | 같은 두피의 가닥; 바람과 구별; hair property lock |
| 스파크 | `short_spark_gap` | 양끝 금속 tip에 닿는 짧은 통로 |
| 아크 | `constricted_arc_bridge` | 두 전극 부착부와 연속 기둥; 지속 시간 gate 분리 |
| 코로나 | `tip_local_corona` | 같은 도체 끝에 국한된 기체 발광 |
| 관 속 glow | `bounded_glow_tube` | 같은 유리관 내부·전극 소유 |
| streamer | `streamer_tip_filaments` | 기점에 연결된 필라멘트와 가지 |
| spark gap 장치 | `declared_spark_gap_apparatus` | 물리적 간극; 비방전 상태도 허용 |
| plasma globe | `plasma_globe_center_radial` | 중앙 전극·가닥·inner glass의 연결 |
| 구름–지면 통로 | `cloud_ground_branched_channel` | 구름과 지상 종점; branch continuity |
| 내부 구름 섬광 | `intracloud_diffuse_illumination` | 같은 구름의 내부 광역; 통로 숨김을 허용 |
| 닫힌 회로 | `closed_circuit_loop` | source/load/return의 같은 경로 |
| 열린 스위치 | `open_switch_gap` | 같은 경로의 물리적 단절; 단락과 구별 |

**P0-B: 다음 12개 카드**는 A의 consumer/effect 검증 뒤 진행한다. 스프라이트·블루 제트·자이언틱 제트의 공간 관계, 구리 권선, 네온관과 LED 배열, 광원–젖은 표면 반사, 코일 장치, 오실로스코프, 직렬/병렬, 계기–노드 연결이 대상이다. 직렬/병렬·전압/전류계는 family를 각각 분해하고 설명 모형과 실제 장치 관측을 구분한다. 겉으로 유사한 장치 모두에 하나의 profile을 적용하지 않는다.

P0-B의 수는 카드 수다. 분해 후 실제 후보 수는 달라지며 24라는 수를 맞추기 위한 항목 생성은 하지 않는다.

## 3. P1과 P2의 처리

P1 54개는 P0에서 확인한 관계·effects 패턴을 적용해 적란운/오로라 재사용, 자연 흔적, 의료 장치 연결, 역사 유물, 조명·도금, 문화 도상을 확장한다. 필요한 장치 판본과 매질이 다르면 sibling을 쓴다.

P2 38개는 현재 채택 보류다. 다음 조사와 분해 결과가 있어야 반영한다.

- 오비탈·밴드·전자/정공: 반도체·양자 모형에 대한 직접 1차 설명과 표시 규칙.
- motor/actuator/UPS/ESS/protective devices: 실제 제조사/기관의 특정 판본 형태와 연결; 사진에서 확인 가능한 기능 근거의 범위.
- ribbon/staccato/upward lightning/ELVES/flicker: 정지 형태와 시간적 명제의 분리, 필요한 계측 기록.
- Lichtenberg 고체 표본·Meissner·차폐: 표본/시연 조건을 확인하고 시각 형태와 원인을 분리.
- ball lightning: 관측 사례와 창작 재현의 provenance를 유지하며 보편 외형 규격을 만들지 않음.
- 원문 22번: 성인 문화·강압·의료 용도 의미를 유지하며 device-specific 외형 자료를 추가. 자동 성적/폭력적 scene recipe는 만들지 않음.
- 원문 23/26번: 문화 도상 판본 확인; weapon/barrier/armor/core/EMP/reanimation family를 source·target·carrier별로 분해.

현재 context 후속 경로에 남은 155개 seed에는 이들 영역의 비가시적 개념·단위·기능·세부 판본이 포함된다. 의미를 삭제하지 않고, 새 독립 시각 후보로 만들기 전 필요한 근거를 명시한다.

## 4. 원본 데이터 구조와 source 등록

기존 계약을 확장 없이 사용한다. 연구용 `observation_mode`, 출처, evidence grade, priority, draft 상태는 연구 폴더에 남긴다. 현재 runtime validator에 없는 필드를 extension에 복사하지 않는다.

신규 파일이 필요하면 다음 **제안 basename**을 사용한다. 아직 만들거나 등록하지 않았다.

- `skills/photo-prompt-image-generator/assets/photo_prompt_electrical_relations_extension.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_electrical_relations.json`

등록 권위는 `photo_prompt_source_manifest.json` 하나다. 실행 시점의 기존 파일·같은 의미·등록 순서를 다시 읽고 충돌 없는 이름·load_order로 추가한다. 후보 목록을 별도의 Python 상수에 중복 등록하지 않는다.

| 원본 영역 | 들어갈 내용 | 들어가지 않을 내용 |
|---|---|---|
| 후보 entry | 긍정 ko/en/paraphrase, bounded concept units, 실제 directed relations, 검증된 effects | URL·source title·오인 예시·연구 상태·원문 dump |
| visual profile | 선택된 의미의 정의, component evidence, 혼동 경계, claim limits, 선택 범위에 맞는 gate | broad electricity label에서 모든 전기 형태를 강제하는 조건 |
| contextual usage | 술어의 용도·비유·ordinary reading·한계 | 독립 물체나 행위 template로 승격한 숨은 기능 |
| 별도 evidence ledger | provenance, 조사 한계, reuse/sibling 결정, 실제 채택 ID, 미채택 이유 | 런타임 검색 정답·랭킹·고정 선택 명령 |

### owner와 effects

각 `relations`의 subject/object를 실제 요청의 같은 장치·구름·피부·수광면에 묶는다. local role 이름과 `selected_*` target은 이번 연구의 제안이며 consumer 검증을 통과한 runtime target이 아니다. 도구가 문자열 관계를 구조적으로 허용해도 실제 소유·공간 관계를 이해한다는 증거가 되지 않는다.

검증할 대표 변경은 머리카락 geometry, 기체 발광 geometry, 피부 marking, 기판 material state, 장치 topology, 수광면 반사, camera artifact다. source color·surface local color·global grade를 각각 구분한다. 손과 피부의 pose/appearance를 바꾸는 간접 효과가 있다면 함께 선언한다.

prop·aftermath_trace·motion·capture_context 등은 현재 기본 ownership dimension이 없거나 제한적이다. 새 entry에 실제 변경 범위를 선언·검증하기 전 `core_assertion_discovery`를 켜지 않는다. 이번 blueprint는 이를 모두 false로 제안했다. target/property가 소비되지 않는다는 사실을 무시하고 빈 effects로 채택하지 않는다.

### hard activation

사용자 요구·정의·부정·기존 lock이 우선한다. exact term은 전체 문맥과 carrier, 매질, subtype이 맞는지 확인해야 한다. 검색 score, broad tag, 번개와 닮은 프린트, bundle membership은 hard duty의 근거가 아니다. definition-essential 조건과 선택 가능한 촬영 색·구도·시간·장치 상태를 분리한다. 희미한 코로나를 설명하기 위해 모든 사람이 하얗게 과노출되는 부가 효과를 넣지 않는다.

## 5. 구현 절차와 제출물

### A — 최신 기준점과 보존

구현 시작 시 최신 HEAD, dirty/untracked paths, manifest, authored source/index hashes를 다시 기록한다. 이번 `CHECKOUT-BEFORE.json`은 연구 시점의 469개 보호 파일과 상태다. 새로운 구현 시점의 working tree를 대신하지 않는다.

기존 dirty 파일을 reset·stash·덮어쓰지 않는다. 적합한 검증 checkout이 있으면 재사용하고, 없으면 필요한 범위만 별도로 검증한다. 후속 branch가 필요하면 `codex/` prefix를 따른다. merge/push/PR은 별도 요청 범위다.

제출물: 최신 snapshot, P0-A의 실제 채택 카드/ID ledger, 보호 파일 목록, 기존 ID 유지 및 sibling 결정.

### B — 원자 작성과 현재 계약 검증

원본 candidate/profile을 작성하고 현재 compiler·validator로 확인한다. `authored_components`의 현재 버전과 obligations 형태를 실제 코드에서 확인한 후 작성한다. 연구 필드가 많다는 이유로 새 스키마/라우터/슬롯을 만들지 않는다.

source-to-component 근거, 필요/선택 구별, 실제 owner binding, 영향을 주는 모든 property, locked color/skin/wardrobe/geometry mutation을 검사한다. family를 단일 후보로 등록하지 않는다.

제출물: scoped authored diff, current registry/manifest validation, consumer 지원 근거, incomplete-owner/lock 우회 negative 결과. 구조 검사와 의미 검토를 분리해 보고한다.

### C — 파생 인덱스와 런타임 정합성

등록된 원본에서 semantic index와 visual profile index를 각각 재생성한다. 같은 embedding text·entry key·provider·model·dimensions가 확인된 vector만 재사용한다. 새 text에는 새 embedding이 필요하다. batch size 1을 적용하며 변화 없는 source에 대한 전체 재호출은 하지 않는다. BM25F 문서와 corpus 통계는 같은 원본에서 재생성한다.

생성된 index를 수동으로 합치거나 기존 출력의 row index·hash만 바꾸지 않는다. 최신 runtime publication 정책에 맞춰 협력적인 multi-file source update와 검증된 snapshot publication을 완료하고, 불일치한 generation을 활성화하지 않는다. 기존 generation·증거를 자동 삭제하는 작업은 이 계획의 필수 범위가 아니다.

다음은 **후속 구현에서 사용할 진입점**이다. 이번 연구에서는 실행하지 않았다. 실제 checkout의 help와 publication 옵션을 확인하고 한 번의 scoped 구현에 맞춰 실행한다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

제출물: source/index hashes, cache reuse 내역과 실제 신규 호출 수, shard checksum, BM25F freshness, registry-hash check, runtime snapshot status.

### D — 동결 의미에서 실제 후보팩까지 확인

평가 요청을 해석할 때 연구 카드·기존 candidate inventory·평가 답안을 기본 prompt의 뜻 사전으로 사용하지 않는다. 현재 neutral pre-core controls/catalog의 허용 범위만 유지한다. 독립 core와 requester-owned meaning을 동결한 후 프로젝트 검색을 수행한다.

현재 경로인 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → obligations/concept candidates/clarification → immutable V6 pack을 검증한다. 실제로 어떤 source의 candidate가 노출됐는지, 어떤 의미가 조건 때문에 거절됐는지, 무엇을 선택했는지, final prompt에서 carrier/관계가 어떻게 보존됐는지 기록한다. zero adoption도 유효하다. 공개 pack에 score·rank·matched answer ID를 추가하지 않는다.

제출물: frozen request/core/pack/receipt, exposure와 selection의 구분, verified effects, literal evidence, composition/runtime audit. pack 출력의 후편집 대신 현재 workflow의 successor 경로를 사용한다.

### E — 회귀와 이미지 평가

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 36개 계획 사례는 keyword alias를 되풀이하는 검사보다 carrier 교환, 끝점 누락, negation/definition, 숨은 속성, 문맥 전환, effects 우회, 가림을 검사한다. 이 사례들은 연구자가 카드 작성 후 만든 공개 계획 사례이며 독립 blind holdout이 아니다.

구현 변경에 맞는 dictionary·component·source-manifest·retrieval·intent-lock·runtime suite를 먼저 실행한다. 변화의 파급 범위나 unresolved regression risk가 넓을 때 full discovery로 확대한다. baseline failure와 새 regression을 구분하고 historical fixture 의미를 약화하지 않는다.

이미지 평가는 별도 요청이 있을 때 실행한다. 예산·모델·출력 크기·같은 frozen core·동일한 효과 scope를 고정해 baseline/보강 결과를 비교한다. 이미지 모델의 확률성과 생성 조건 때문에 한 쌍의 결과만으로 인과적 개선을 확정하지 않는다. 연구 자료를 이미 읽은 평가를 blind로 보고하지 않는다.

우선 비교할 여섯 장면군은 (1) spark/arc/corona, (2) plasma globe 중앙/유리경계, (3) cloud-ground/IC와 TLE 연결, (4) circuit/probe/device continuity, (5) visible source–wet ground reflection, (6) 의료/문화/비유에서 literal discharge 누출 방지다. 원본 해상도에서 요구된 모든 duty를 평가하며 가려지거나 부분만 보이면 통과가 아니다. 의도하지 않은 신규 duty를 native 평가 기준에 넣지 않는다. 소리·전압·극성·동의·의료 성과는 사진으로 평가하지 않는다.

제출물: runtime bytes/audits, 원본 이미지, all-of duty 결과, whole-scene 관찰, 실용적·예술적 선호와 사용자 수락의 별도 기록.

## 6. 운영 완료 조건

P0-A 12개가 의미·scope·owner·consumer·검색·선택 검증을 통과하고 기존 의미/dirty 작업을 보존했을 때 첫 데이터 반영 단위를 완료로 보고한다. P0-B, P1, P2는 실제 채택 ledger에 따라 별도 단위로 진행한다. 연구 카드 116개나 blueprint 95개가 존재한다는 이유로 전체가 반영됐다고 보고하지 않는다.

최종 보고에는 조사 완료, 원본 채택 수, 등록/인덱스 상태, 실제 후보 노출·선택, 미실행 checks, 이미지 평가, 사용자 판단, commit/push 상태를 구분한다.
