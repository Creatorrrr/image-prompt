# 사진 편집 효과 데이터 반영 계획

최초 계획 기록이다. 후속 사용자 요청으로 진행한 구현과 검증의 실제 결과는 [반영 보고서](implementation-report.md)에 기록한다. 전체 혼동쌍 48장 계획을 이번 독립 3장 검사로 완료했다고 간주하지 않는다.

2026-10-01. 현재 상태: 리서치·설계 완료, 운영 반영 미실행. 이 계획의 대상은 [조사 보고서](research-report.md)와 [245행 매핑](keyword-matrix.json)이다. 후보 25개·bundle 6개를 [연구 초안](runtime-projection-draft.json)으로 준비했다. 초안을 그대로 등록하는 작업과 의미·검색·픽셀 품질을 검증하는 작업은 구분한다.

## 1. 목표와 완료 기준

목표는 편집 용어가 **요청한 의미를 보존하면서, 올바른 적용 대상·공간 범위·계조 관계·세부 보존 조건을 가진 후보와 의미 의무로 연결**되도록 하는 것이다. 원문 245행은 metadata·연산·진단·룩이 섞여 있으므로 245개의 새 후보나 hard profile을 만드는 것을 목표로 삼지 않는다.

완료 기준은 다음과 같다.

1. 245행 모두에 재사용·추가·연산/metadata 경로·보류의 이유를 기록한다. 다른 owner의 동명 항목을 coverage로 세지 않는다.
2. 신규 후보는 출처, owner, concept units, 실제 영향 차원, 혼동 반례가 있다. 동일 슬롯 canonical 관계가 유효하고 cross-slot 동의어를 무리하게 연결하지 않는다.
3. 필수 요청 효과는 후보 발견 여부와 무관하게 frozen core의 요청 근거·semantic assertion 또는 기존 request-scoped binding으로 보존한다.
4. 후보팩에서 노출된 optional 성분을 선택하면 literal 최종 문장과 관계 근거가 연결된다. associated profile이 자동 hard 활성화되지 않는다.
5. 전체 차원 및 부분 속성 잠금, 부정, 사진 전체/사진 속 물체 scope를 지킨다. source/full details/compact view의 의무와 hash가 일치한다.
6. 실제 이미지 평가는 별도 artifact로 완료한다. `PARTIAL`은 실패이며 기술 충족과 사용자 판단을 분리한다.

## 2. 순서와 우선순위

원문은 88개 **설계 의미군**으로 묶었다. 그중 P0 41개, P1 38개, P2 9개다. 그룹 수는 우선순위 집계이며 각 그룹을 하나의 runtime 개념으로 합친다는 뜻이 아니다.

| 단계 | 작업 | 구체 산출물 | 통과 조건 |
|---|---|---|---|
| A. 의미와 적용 영역 정리 | 기존 혼합 label, owner, 조합 제외어, 부분 잠금 경로 검토 | 항목별 이행표·profile 재사용표·회귀 사례 | 기존 의미를 몰래 축소하지 않음; 동시 요청/잘못된 대체를 구분 |
| B. 기존 계약 재사용 | 확인한 17개 profile의 activation·evidence·gates 비교 | 재사용/수정/새 profile 필요 여부 | generic 효과에 adult 조건을 끌어오지 않음; 필수 요청 의미의 독립 근거 |
| C. 개별 후보와 조합 반영 | 1차 연구 초안 25개·6개를 검토하고 필요한 부분만 승격 | runtime extension·외부 maintenance 원장 | 소스 검증, 중복 ID, scope, member 참조, 컴포넌트 의무 검증 |
| D. 검색·바인딩·잠금 통합 | 정확어·의역·한국어·hard negative·공존 조합 검증 | frozen query cases·팩/selection/audit evidence | 올바른 sense/owner, 독립 activation, literal 근거, 잠금 보존 |
| E. 인덱스와 회귀 | 변경된 문장만 embed, hash 갱신, 관련 테스트 | 인덱스·manifest·holdout 결과 | stale hash 없음; 기존 unrelated case 손상 없음 |
| F. native 픽셀 검증 | 단일 효과, 혼동쌍, 조합, 출력 상태를 평가 | 원본 이미지·typed review·attempt ledger | 모든 필수 관찰 성분 충족; 차단 호출은 품질 점수 제외 |
| G. 후속 계열 확장 | 그래픽·물리 공정·작업/출력 정보 보강 | P1/P2 추가 batch와 각 근거 | 기존 batch 통과 후 같은 기준을 충족 |

A–E의 구현 검증과 F의 렌더 평가는 별도 결과다. 이번 요청에서는 연구용 구조와 계획을 준비했으며, 이미지 생성은 수행하지 않았다. 실제 생성은 후속 이미지 검증 요청에 따라 진행한다.

## 3. 단계 A: 먼저 고칠 의미와 계약

| 항목 | 현재 문제 또는 위험 | 처리 방안 |
|---|---|---|
| `slot:texture:halation` | film halation+bloom이 하나의 label | 새로운 atomic ID를 먼저 추가. 기존 ID의 조합 의미는 유지한 채 사용하는 preset/forced set/bundle을 조사하고 이행 |
| `cool_digicam_grain` | 차가운 색+노이즈+시대 룩 결합 | 색 편향, luma/chroma noise, 플래시, 압축 흔적 분리. 센서 고유색 alias 금지 |
| `iso3200_noise_grain` | 숫자 기기 정보+noise+grain 결합 | 장비·노출 metadata와 입자/노이즈의 관찰 성분을 분리. 실제 장비 이력을 생성 픽셀로 확정하지 않음 |
| `texture → material` | 영상면 효과가 피사체 재질로 이동할 수 있음 | 신규 효과는 기존 `grain_profile`/`quality`/`film_emulation` 등 알맞은 슬롯과 명시적 `style` scope 우선; `texture`를 쓰면 항목 override와 회귀 검증 |
| `motion → []` | bundle에 필요한 scope가 기본으로 비어 있음 | 신규 motion 후보에 `camera` 또는 실제 `lighting` 영향 선언. 모든 motion의 전역 scope를 임의로 바꾸지 않음 |
| roll-off의 `bloom` 제외어 | 잘못된 대체와 동시 요청을 같은 조건으로 막을 수 있음 | component/span 단위로 부정·대체·공존을 판정하는 사례를 추가. 단순 제외어 삭제로 negative를 무너뜨리지 않음 |
| diffusion의 `film halation`, panning의 `rear-curtain flash` 제외어 | 효과들이 결합되는 요청에서 sense가 사라질 수 있음 | 단독 대체와 명시적 공존을 짝지어 검증. 전체 문장 lexical veto의 범위를 검토 |
| 일반 후보의 부분 속성 잠금 | helper 존재만으로 전체 경로 보호를 확정할 수 없음 | ordinary pack → compact/full details → selection → independent audit에서 property effect가 유지·검사되는지 실험 |
| component 배열 | `visible_evidence` 여러 항목은 현재 one-of 계약 | 동시에 필요한 성분마다 별도 component ID를 두고 전체 literal evidence를 요구 |

`existing_slot_context_extensions`는 동등한 paraphrase와 context의 추가에 한정된다. 다른 owner·효과·행동의 의미로 기존 ID를 교체하는 수단으로 사용하지 않는다. 단순 alias 추가와 의미 변경을 이행표에서 구분한다. 기존 frozen core·pack·ledger artifact는 해당 시점의 의미를 보존한다.

## 4. 단계 B–C: 데이터 단위와 실제 변경 파일

### 연구 자료와 runtime 자료의 분리

연구 자료에는 `source_ids`, `semantic_kind`, `owner_scope`, 진단/연산/metadata, 설계 추론, pixel 상태를 남긴다. 현재 runtime extension root는 allowlist가 있으므로 연구용 필드를 그대로 넣지 않는다. runtime에는 허용된 슬롯 entry, `concept_units`, `relations`, `affected_dimensions`, 검토한 property effects, optional bundle을 투영한다.

`canonical_concept_id`는 같은 슬롯의 실제 ID로만 연결한다. `film_emulation`의 halation과 `quality`의 optical diffusion에 하나의 cross-slot canonical ID를 주지 않는다. 용어의 문맥 관계는 maintenance 원장에 기록하고, runtime에서 서로 다른 visible component로 유지한다.

| 변경 대상 | 예정 내용 | 조건 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json` | 검토한 atomic 후보와 optional bundle | 새 파일 이름은 제안; loader 등록 전 schema·scope·참조 통과 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_editing_effects.json` | 기존으로 표현할 수 없는 입자/노이즈/블룸/세부 보존 등의 새 의무 | 독립 요청 근거와 충분한 gates가 있을 때만 신설. 기존 17개 재사용 우선 |
| 기존 color/capture/lighting visual-obligation 자산 | activation·혼동 경계·공존 사례를 필요한 범위에서 수정 | 현재 profile ID와 필수 성분 유지; 수정된 라우팅·render mutation 회귀 필요 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json` | candidate policy의 required extension 등록과 필요한 legacy 이행 | 신규 차원 `postprocess`를 만들지 않고 기존 30개 차원 사용 |
| `skills/photo-prompt-image-generator/scripts/prompt_generator.py` | extension 목록 등록, 필요 시 일반 후보 scope/property 전파 | 기존 helper를 재사용하고 데이터만으로 해결되는 부분은 코드 변경 불필요 |
| `skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py` | 필요 시 일반 candidate/bundle의 property effect·eligibility 계약 보완 | 실패 사례로 필요성이 입증된 부분만 변경; full/source hash와 migration 검증 |
| `skills/photo-prompt-image-generator/scripts/compose_pack_view.py`, `audit_composed_prompt.py` | 필요 시 새 scope 정보와 의무가 유지되는지 보완 | 선택·문장 근거를 실제로 소비하는 곳에서 검증 |
| `docs/research-evidence/photo-prompt/extension-maintenance/` | 출처·owner·의미/연산/이력 구분·이행 기록 | 기존 maintenance-ref 계약으로 hash 연결; pre-core 필수 읽기 자료로 만들지 않음 |
| semantic/profile index와 manifest/shards | 변경된 데이터 hash 및 텍스트 반영 | 호환되는 기존 벡터 재사용, 변경 텍스트만 batch size 1로 embed |
| `tests/test_photo_editing_effects_semantics.py`와 전용 fixture | 의미 혼동·공존·잠금·owner·검색의 실제 반례 | label 존재만 확인하는 테스트보다 의미·경로 실패를 포착 |

`SKILL.md`를 편집 용어 사전으로 확장하거나, 후보를 읽기 전에 특정 데이터 정의를 반드시 기억하도록 요구하지 않는다. 유지보수 조사와 실요청의 core-before-retrieval 격리를 함께 지킨다.

### 1차 후보 25개와 조합 6개

초안은 구조를 검토하기 위한 제한된 표본이다. 기본 가중치 1.0은 중립 placeholder이며 성능·사용 빈도에 근거한 값이 아니다. 실제 적용 전에 applicability·preset filter·ranking·scope를 보완한다.

| 후보 계열 | 초안 수 | 내용 |
|---|---:|---|
| 입자·디지털 노이즈 | 4 | fine/coarse film-like grain, luma/chroma noise |
| 영상 결함·세부 | 3 | JPEG-like edge blocks, sharpening halo, readable microdetail |
| 번짐 | 6 | local bloom, film red-orange edge halo, neutral optical diffusion, veiling, discrete ghosts, light leak |
| 계조·색 | 7 | lifted black floor, gentle roll-off, muted chroma, warm-highlight/cool-shadow split, bright open tones, tonal duotone, selected-object color splash |
| 피부·초점·움직임 | 5 | texture-preserving tone evening, extended near/far focus, depth-dependent defocus, tracked panning, flash core+ambient trace |

| 조합 초안 | 의무 성분 | 검토할 혼동 |
|---|---|---|
| Bright local bloom | 밝은 계조+점진적 롤오프+하이라이트 국부 번짐 | overexposure/전역 blur로 대체하지 않음 |
| Film edge and grain | 밝은 경계의 색 halo+영상면 입자+계조 | 전역 붉은 색·재질 손상으로 대체하지 않음 |
| Neutral diffusion detail | 광학 확산형 번짐+읽히는 세부 | 필름형 적주황 halo가 항상 필수라는 가정 |
| Digital flash trace | 디지털 luma noise+flash core+주변 셔터 흔적+압축 흔적 | CCD 장비 이력·인물 중복을 자동 확정하지 않음 |
| Muted lifted-black finish | 절제된 색+열린 검정+미세 입자 | 모든 nostalgic 요청의 고정 recipe로 쓰지 않음 |
| Tonal duotone detail | 두 색의 계조 매핑+피사체 세부 | 배경·옷 두 색만으로 의무를 만족시키지 않음 |

Bundle은 관련된 원자 성분을 제안하고 선택한 조합의 근거를 확인하는 단위다. 검색·노출·선택은 profile hard 활성화의 증거가 아니다. `hard_profile_ids`라는 source 필드 이름에 의존하지 말고 컴파일된 advisory 관계와 `independent_request_evidence_only` 계약을 확인한다.

1차 다음의 batch는 **기존 의미의 빈칸**을 기준으로 정한다. roll-off/tonal color·광학 관계·움직임의 재사용을 먼저 통과시키고, grain/noise·retouch 보존·scope를 추가한 뒤, 남은 디테일/결함·시대 룩을 보완한다. 최종 신규 항목 수는 245행 이행표의 재사용 판정 후 결정한다.

## 5. 단계 D–E: 실제 동작 검증과 인덱스

### 검색·바인딩 기준

[검증 계획](validation-plan.json)에 포함한 사례를 다음 네 층으로 실행한다.

| 층 | 검사 내용 | 결과의 한계 |
|---|---|---|
| 어휘/의미 검색 | exact routing, 동등 의역, 한국어, embedding-only holdout, 다른 owner의 negative | 후보가 검색됨은 선택·픽셀 성공이 아님 |
| scope와 applicability | 전체 차원 잠금, 옷 색·피부·구도 등의 부분 속성 잠금, 비인물/성인 조건, 부정 | field 선언과 경로 검사를 함께 확인 |
| 채택·최종 문장 | 필요한 component 모두의 literal phrase·relation 근거, compact/full hash, 선택 미이행 rejection | 프롬프트 의미 충족과 픽셀 충족 분리 |
| 조합·변이 | bloom+roll-off, diffusion+film halo, panning+rear-curtain; 한 성분 삭제·대체·과도한 전역화 | 부정 hard negative와 정당한 공존을 동시에 검증 |

필수 효과는 후보 검색 실패 시에도 core의 independent 요청 의무로 유지한다. metadata-only 요청은 미감 preset이나 피부·몸·재질 후보를 추가하지 않는다. Relighting·inpainting·retouch 등의 편집 작업은 실제 입력·마스크·보존 영역을 제공받은 별도 경로에서 비교 검증한다.

현재 frozen holdout은 결과가 안 좋다고 정답·문장을 바꾸지 않는다. 새로운 editing 전용 query split에 source-backed paraphrase와 adjacent negative를 기록하고, 기존 unrelated case는 그대로 재실행한다.

### 실행할 기존 테스트

데이터 반영 후 먼저 새 editing 사례와 관련 경로를 검증한다.

```bash
.venv/bin/python -m unittest tests.test_photo_editing_effects_semantics -v
.venv/bin/python -m unittest tests.test_photo_candidate_semantics tests.test_photo_composer_view -v
.venv/bin/python -m unittest tests.test_photo_capture_elements_visual_semantics tests.test_photo_lighting_visual_semantics tests.test_photo_color_relations -v
.venv/bin/python -m unittest tests.test_photo_visual_profile_retrieval tests.test_photo_visual_obligations -v
.venv/bin/python -m unittest tests.test_photo_authorial_core_v6 tests.test_photo_precore_feature_selection tests.test_photo_adult_appeal_scope -v
```

첫 번째 모듈은 앞으로 만들 대상이다. 나머지는 현재 존재하는 관련 테스트다. 코드·schema 공용 경로가 바뀌면 영향을 받는 scope/selection/audit suite와 전체 suite까지 넓힌다. 연구 문서만 작성한 이번 단계에서는 이 구현 테스트 결과를 만들어냈다고 보고하지 않는다.

### 인덱스 갱신

후보 label/alias/concept 또는 dictionary hash가 바뀌면 semantic index를 재생성한다. registry가 바뀌면 text가 같더라도 profile index hash를 갱신한다. 현재 CLI에서 지원하는 옵션을 확인했다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 1 --progress
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

변경되지 않은 embedding input·provider·model·dimension의 벡터는 재사용한다. `build_semantic_index.py`에는 현재 `--check` 옵션이 없다. 인덱스 저장 hash·실제 index fixture를 소비하는 기존 검색 테스트와 manifest를 확인하고, 필요하면 `--dry-run`으로 예정 metadata를 검토한다. API 키는 기존 환경을 사용하고 출력하거나 문서에 기록하지 않는다. 이번 조사에서는 재생성·embedding 호출을 실행하지 않았다.

## 6. 단계 F: 픽셀 자격 검증 설계

이 단계는 후속 이미지 검증 요청에서 실행한다. 아래 수량은 단계적 평가를 설계하기 위한 제안이다. 연구 초안의 구조 통과만으로 모든 항목을 render-qualified로 올리지 않는다.

1차는 8개 혼동쌍을 각 2조건·3독립 렌더로 비교하는 48개 이미지 규모를 제안한다. 효과별 gate가 안정된 후 4개 공존 조합을 추가한다. 모델·reference·생성 제약·비용에 따라 실행 수는 요청 범위에서 확정하고, 실패로 특정 case를 삭제하지 않는다.

| 혼동쌍/조합 | native 픽셀에서 반드시 볼 점 |
|---|---|
| roll-off / bloom | 밝은 계조의 점진적 전이와 하이라이트 주변의 공간 번짐을 구분 |
| film halation / neutral optical diffusion | 색 halo의 경계·범위와 확산의 색·세부 감소를 구분 |
| veiling / discrete ghost | 국부 veil·대비와 분리된 광원 관련 모양을 구분 |
| film grain / digital noise | 밝기·색 노이즈, 영상면 입자, 장면의 표면 질감을 구분 |
| shallow focus / global blur | 초점 대상, 깊이에 따른 변화, 배경·전경의 관계 |
| panning / uncontrolled camera blur | 대상 가독성과 배경 흔적의 방향·관계 |
| tone-evening / skin smoothing | 미세 피부결 보존, 국부 색 정리, 얼굴 기하 연속성 |
| tonal duotone / object two-color palette | 계조별 색 매핑과 실제 물체 색 배치를 구분 |
| bloom+roll-off | 두 효과를 모두 충족; 하나가 다른 효과를 삼키지 않음 |
| diffusion+film halo | 중립 확산과 색 경계 halo를 각 scope에서 관찰 |
| panning+rear-curtain | 추적 관계와 flash/ambient 시간 흔적의 공존 |
| film grain+retouch 보존 | 영상면 입자와 피부 미세결의 owner가 유지됨 |

밝은 광원·암부·색 경계가 없는 장면에는 해당 광학 효과가 판정 불가능할 수 있다. 평가 장면은 효과를 관찰할 기회를 포함하되 사용자 요구를 바꾸지 않는다. 출력 HDR·ICC·bit depth는 표시 환경과 파일 metadata의 추가 확인이 필요하고, 보이는 밝기만으로 PASS를 주지 않는다.

각 run에 requester/core/pack/selection/prompt/negative의 원문과 hash, 실제 사용한 후보·프로필, 모델·reference 범위, 시도와 차단 상태, 원본 artifact, 픽셀 gate별 증거를 남긴다. 비교 조건은 의도한 효과 성분만 바꾼다. 프롬프트 수정·도구 차단·대조군 변경이 있으면 intervention으로 기록한다.

판정은 `PASS`, `PARTIAL`, `FAIL`, `NOT_OBSERVABLE` 등을 사용하는 해당 typed review schema를 기준으로 하고 필수 성분의 `PARTIAL`은 실패다. 기존 schema가 이 enum을 허용한다고 임의로 가정하지 않고 저장 전에 확인한다. 차단·생성 오류는 평가 이미지 수에서 제외하되 attempt ledger에는 보존한다. 픽셀 충족과 사용자 선호·수용은 별도 열로 남긴다.

## 7. 단계 G: 나머지 계열의 보강

| batch | 범위 | 추가 조사·구현 기준 |
|---|---|---|
| 세부·결함 | local contrast/clarity/texture/structure/dehaze, grain/noise, JPEG/banding/moiré, dust/scratches | 개별 공간 패턴을 지원하는 원문과 native 대조를 보강; 피부·옷·배경 material과 분리 |
| 편집 작업 | healing/clone, dodge/burn, masks, geometry, compositing, merge/stack | 원본·입력 레이어·target/mask·보존 영역 계약. 단일 생성 룩만으로 실행 이력 보증 금지 |
| 시대·매체 | digicam/CCD, instant/disposable, film-scan, cross/bleach | 장비 조건·작가 사례의 범위를 기록. 일반형에는 adult 제한·종이 테두리 등 기존 특정 profile의 조건을 자동 적용하지 않음 |
| 그래픽·공정 | poster/halftone/glitch, cyanotype·silver/platinum/wet plate, photogram/luminogram | whole image와 depicted artifact owner, 사진 medium과의 충돌, 공정 provenance를 구분 |
| 작업·출력 | RAW, nondestructive, LUT/preset/action/batch, ICC/color space/soft proof/bit depth/HDR | 자동 aesthetic 후보에서 제외하거나 visible projection을 별도 정의. 파일/장치/작업 실행 증거로 검증 |

JPEG·moiré·instant/disposable·CCD 룩 등은 현재 그룹 수준의 근거가 곧 개별 hard profile의 충분한 정의는 아니다. 후속 저수준 pattern·기기별 사례 조사를 완료하고 이행표에 근거가 연결된 경우에만 승격한다. Action/batch 같은 기능의 실제 실행 지원이 필요하면 사용 도구의 공식 문서·버전에 맞는 별도 연산 계획을 작성한다.

## 8. 반영 이후 기록할 상태

각 의미군과 runtime 후보에 `research_ready → schema_valid → exposed_in_pack → selected_with_evidence → prompt_audited → native_pixels_qualified → user_judgment`를 별도로 기록한다. 이 상태는 연구·검증 원장에 두며 현재 runtime JSON의 새 필드를 임의로 만들지 않는다.

다음 작업의 권장 시작점은 단계 A의 혼합 의미·공존 제외어·부분 잠금 경로 검증과 단계 B의 기존 프로필 재사용이다. 그 결과를 반영해 연구 초안에서 필요한 후보만 단계 C로 옮긴다. 단계별 통과 근거 없이 신규 후보·hard 의무·preset을 한꺼번에 확대하지 않는다.
