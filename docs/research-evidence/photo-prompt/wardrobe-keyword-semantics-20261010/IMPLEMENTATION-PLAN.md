# 리서치를 시각 의미·후보 데이터에 반영하는 계획

작성일: 2026-10-10 KST. 이 문서는 반영 계획이며 현재 실행 완료 기록이 아니다. 조사 근거는 [리서치](RESEARCH.md), 구현 단위는 [카드](CARD-CATALOG.md), 작성 가능한 선택 변형은 [후보 초안](CANDIDATE-BLUEPRINTS.json)에 있다.

## 1. 목표와 완료 조건

사용자가 의상·색·장면의 의미를 지정했을 때, 데이터가 그 의미의 **부위·소유자·연결·현재 상태·혼동 경계**를 구체화하고, 열린 선택을 바꾸면서도 지정된 관계를 보존하도록 한다. 넓은 스타일명이 항상 같은 옷·색·장소·포즈를 선택하도록 만들지 않는다.

반영 완료는 다음 증거를 단계별로 확보한 상태로 정의한다.

1. 원자료의 명시·설명·선택·추정·제외·비착용 구분과 출처가 보존된다.
2. 기존 의미와 동등한 것은 기존 ID를 유지하고, 다른 소유자·상태·기법·관계는 구별된다.
3. 후보의 전체 효과·전제·관계와 프로필의 작성 구성요소가 데이터 계약을 통과한다.
4. 후보·프로필·번들·인덱스·게시 세대가 같은 검증 원본을 가리킨다.
5. 실제 pack에서 노출·거절·선택·개별 증거가 의도한 방식으로 동작한다.
6. 해당 요구가 있는 이미지의 필수 관계가 원본 해상도에서 확인된다.
7. 전체 이미지의 표현과 사용자 수용은 기술적 검증과 별도로 평가한다.

**이번 요청에서 완료한 것은 연구·초안·계획·연구 패키지의 구조 검증이다.** 아래 원본 편집·인덱스 재생성·런타임 게시·행동 회귀·이미지 비교는 실행하지 않았다.

## 2. 데이터 반영 위치

| 정보 | 반영 후보 원본 | 작성 방식 |
|---|---|---|
| 상의·목선·소매·패널·여밈·내외층 | `photo_prompt_clothing_structure_extension.json` | 기존 `garment_detail`·`wardrobe_style`의 의미를 대조; 다른 형상·관계는 구체 변형으로 분리 |
| 국소 핏·장력·기장·접촉 주름 | `photo_prompt_fashion_fit_extension.json` | 같은 의상·부위·접촉 대상의 관계, 지역 속성 효과를 선언 |
| 섬유·조직·표면·비침·반사·외형 추정 | `photo_prompt_textile_surface_extension.json` 및 관련 기존 원본 | 일반 표면과 특정 선택 변형 분리; 실제 섬유·제작법은 관찰 외 주장으로 관리 |
| 색 영역·파이핑·단일 강조·광원 분리 | `photo_prompt_color_relations_extension.json` | 표면·부위·수량·영역·역할 관계를 선언. 개별 색명 복제보다 소유자 연결 우선 |
| 가방·신발·레그웨어·주얼리·고정점 | `photo_prompt_accessory_structure_extension.json` | 지지 경로와 연결점, 신체 부위·개수·비대칭을 구분 |
| 아플리케·자수·리본·모티프·수선 | `photo_prompt_ornament_structure_extension.json` | 기법·부피·부착·개수·위치를 분리 |
| 고름·오비·전통복식 영감과 현대 변형 | `photo_prompt_traditional_clothing_detail_extension.json` | 원자료의 inspired·modern 한정을 보존; 고증 불충분 부분을 주석으로 유지 |
| 수영복의 연결·가림·선택 범위 | `photo_prompt_swimwear_extension.json` | 유형·지지·영역별 가림과 젖음의 별도 효과를 확인 |
| 리본–봉제선·파편–원 의상 등 범용 관계 | `photo_prompt_visual_grammar_extension.json` | 이미 있는 완전한 관계를 재사용하고 넓은 소재·콘셉트와 분리 |
| 비착용 의상 소품·손/소품 전달·장소 기능 | `photo_prompt_everyday_scene_extension.json` 및 적합한 기존 `prop`·`action` 원본 | 객체 상태·접촉 단계·행위자 귀속을 표현 |
| 조명·프레이밍·색조·이미지 평면 처리 | 기존 `lighting`·`portrait_composition`·`editing_effects` 원본 | 관찰 가능 범위·광원/표면색·그레인/섬유를 구분 |
| 구체적인 증거와 렌더 요구 | 각 해당 `photo_prompt_visual_obligations_*.json` | `authored_components` v1/v2에 작성. 컴파일된 파생 필드는 원본에서 직접 작성하지 않음 |
| 출처·정규화 검토·제외 문맥·불확실성 | 유지보수 근거 및 검토 결정 파일 | 자동 긍정 검색어·전역 부정 프롬프트·실제 사용 빈도로 승격하지 않음 |

현재 등록표의 134개 확장을 먼저 사용한다. 의미적으로 묶일 원본이 없을 때만 새 확장 파일을 만들고, 그 경우 `photo_prompt_source_manifest.json`에 종류·필수 여부·종류별 연속 load order를 정확하게 등록한다. 새 슬롯을 먼저 만드는 방식은 피한다.

현재 `precore/visual_feature_catalog.json`은 중립적인 관찰 축이다. 503개 키워드 사전·의상 조합·카드·후보를 이 카탈로그 또는 `SKILL.md`에 복사하지 않는다. 기초 프롬프트 독립 작성과 이후 데이터 조회 사이의 경계는 그대로 유지한다.

## 3. 첫 반영 범위: P0-A, 16개 카드

| 카드 | 처리 | 파일·주요 슬롯 | 완료할 의미 |
|---|---|---|---|
| WK002 | 정규화 주석 | 근거·검토 파일 | 앞여밈과 칼라 끝 버튼의 불확실성 |
| WK007 | 기존 관계 대조 후 보강 | clothing structure / garment detail | 외층 앞단·내층·외층 소매 귀속 |
| WK011 | 상태가 다른 후보 대조 | everyday scene 또는 적합한 prop | 비착용 블레이저·지지면·착용 블라우스 |
| WK014 | 모호성 주석 | 근거·검토 파일 | 슬립/캐미솔, tube/halter 대안 유지 |
| WK016 | 추정 상태 주석 | 근거·검토 파일 | bikini/tankini와 peach/coral 추정 분리 |
| WK025 | 인셋 관계 대조 | clothing structure / garment detail | 같은 목선 안의 좁은 레이스 |
| WK032 | 분리 구조 대조 | clothing structure / garment detail | 위팔 밴드·소매·몸판과의 틈 |
| WK038 | 기존 ID 재사용 우선 | `clt_ct031_v1` | 두 몸판 패널을 잇는 곡선 접합 |
| WK040 | 안감 관계 대조 | clothing structure / garment detail | 같은 치마의 겉층과 안감 노출 |
| WK046 | 완전한 기존 관계 재사용 | `vg_ribbon_to_garment_seam` | 리본 꼬리–접합점–계속되는 봉제선 |
| WK061 | 값·위치·소유자 대조 | garment detail + text 효과 | 같은 저지 앞판에 숫자 10 |
| WK069 | 선택 그룹 주석 | 근거·검토 파일 | 다섯 후보색이 동시 배색이 아님 |
| WK070 | 단일 면 관계 대조 | color relations | 붉은 면 하나의 시작점·흐름·색 귀속 |
| WK074 | 지역 물성 관계 대조 | textile / clothing structure | 불투명 몸판과 별도 시어 소매 |
| WK088 | 손 접촉·방향 대조 | action + fit | 같은 밑단의 국소 아래 당김 |
| WK091 | 복수 소유자 관계 대조 | action / everyday scene | 두 행위자·손·트레이·접촉 단계 |

16개 중 4개는 주석·모호성·선택 그룹이며 이미지 후보로 직접 내보내지 않는다. 나머지도 12개 신규 후보를 반드시 만들라는 뜻은 아니다. 의미 대조 결과에 따라 재사용·동등한 문맥 확장·구체 변형 추가로 나눈다. 첫 묶음은 잘못된 의미 합치기를 줄이면서 기존 관계 재사용이 실제로 작동하는지 확인할 수 있는 범위이다.

첫 묶음 이후에는 남은 P0 37개를 색·장식 수량, 물질 상태, 액세서리 고정, 프레이밍 순으로 나누어 반영한다. P1 71개는 소재·형태·생활 장면의 조합 폭을 넓힌다. P2 1개는 제복 고증 주석을 유지하며, 별도 국가·시기·계급 근거를 확보하기 전 고증 프로필로 승격하지 않는다.

## 4. 기존 항목 유지·보강·신규 추가의 판단 규칙

- **재사용:** 대상·상태·관계·효과가 이미 같으면 기존 ID와 선언을 유지한다. WK046의 리본–봉제선은 이 경로를 우선한다.
- **동등한 표현 확장:** 같은 외형·소유자·전제를 한국어/영어로 다시 표현하는 경우만 `aliases`·`keywords`·`paraphrases`와 기존 문맥 확장에 추가한다.
- **선택 변형 분리:** 넓은 개념은 그대로 두고, 구체적으로 선택 가능한 목선·기장·패널·재질 반사 등의 변형을 각각 제안한다. ‘비숍’과 ‘벨’, ‘홀터’와 ‘스파게티’처럼 다른 연결을 동의어로 합치지 않는다.
- **다른 관계·상태 추가:** 착용→옆에 놓임, 몸판 소매→분리 위팔 소매, 개별 색→한 붉은 면, 한 인물 손→두 인물 전달처럼 실제 효과가 다르면 다른 후보로 검토한다.
- **주석 유지:** 재료 추정·원문의 모호성·미입력 색·군복 고증·프레임 밖 상태는 긍정 후보의 새 확정 의미로 만들지 않는다.

연구 카드의 `seed_keyword_ids`는 추적 관계이며 런타임 alias 목록이 아니다. 503개 표제어를 관련 카드의 구체적인 문장에 모두 동의어로 붙이지 않는다. `[후보→번들→프로필]` 연결도 후보가 프로필 전체 외형을 충족했다는 증거가 아니다.

## 5. 후보·프로필·번들 작성 기준

후보에는 짧은 긍정 명제 `concept_units`, 방향 있는 `relations`, `affected_dimensions`, `affected_properties`를 작성한다. 그 관계에 필요한 의상·부품·사람·소품이 실제 장면에 있거나 선언한 열린 효과로 일관되게 도입 가능한지 검토한다. 한 슬롯의 이름만 보고 다른 부수 효과를 누락하지 않는다.

예를 들어 트레이 전달은 손 위치만의 변화가 아니다. 다른 행위자·트레이·접촉 단계·관계·장면 구도에 영향이 있을 수 있다. 모든 영향을 선언하고, 인물 수·의상·장소가 잠겨 있으면 그 의미를 바꾸지 않는다. 추가 행위자가 허용되지 않으면 해당 후보를 거절할 수 있어야 한다.

`CANDIDATE-BLUEPRINTS.json`의 150개 초안은 이미 이 구분을 가지고 있지만, 선택 변형 일부는 관계 끝점의 구체 작성이 남아 있다. 속성 효과도 최종 변형·대상 기준으로 검토해야 한다. 이 초안을 그대로 런타임에 복사하는 계획은 아니다.

프로필의 기본 의미와 혼동 경계는 구체적인 관찰에 맞춘다. 구성요소가 단순하면 `photo-authored-visual-components/v1`, 동일한 관계에 여러 끝점·증거가 필요한 경우는 v2의 `components`, `discovery`, `obligations`를 사용한다. 모든 구성요소가 의무에 연결되며, 발견 임계값은 선택한 전체 관계의 증거·픽셀 의무를 줄이지 않는다.

기존 원본의 `component_semantics`, `required_evidence_fields`, `evidence_requirements`, `render_gates`, `composition_instruction`은 컴파일된 필드이므로 새 원본 프로필에서 수작업으로 중복 작성하지 않는다. 렌더 게이트의 작성 정보는 허용된 `authored_components` 내부에 둔다.

정확한 현재 요청의 뜻이나 명시한 사후 선택이 근거가 되는 경우에만 구체 의무를 바인딩한다. BM25F·임베딩·넓은 스타일명·과거 예시만으로 필수 증거·음성적 제외·픽셀 의무를 새로 생성하지 않는다. 20개 조합은 언제나 선택 참고이고, 일반 후보를 모두 거절하는 결과도 유효하다.

23개 과거 제외 조건은 문맥별 반례 쌍으로 보관한다. 현재 요청이 그 제외를 지정하지 않았다면 런타임 negative pool에 넣지 않는다. 검정실버 장면의 레이스 제외가 다른 고딕 의상에 전파되거나, 미니 한복의 저고리 크롭 제외가 데님 한복에 전파되어서는 안 된다.

## 6. 작업 순서와 저장소 보존

| 단계 | 수행 내용 | 산출물·통과 조건 |
|---|---|---|
| A0 | 구현 시점의 checkout·HEAD·원본·등록표·인덱스·dirty 파일을 새로 스냅샷 | 이번 연구 스냅샷을 최신 상태로 가정하지 않음 |
| A1 | 필요하면 격리 worktree에서 기존 의미 대조 및 16개 첫 묶음 검토 | 후보/프로필/번들의 ID별 유지·보강·추가·보류 결정 |
| A2 | 원본 데이터와 출처·문맥 기록 편집 | 전체 효과·소유자·긍정 검색 표현·조건을 검토 |
| A3 | 사전·참조·프로필 작성 구조 검증 | 중복 ID, 깨진 후보–번들–프로필 참조, 미등록 파일 등이 없음 |
| A4 | 시맨틱·시각 프로필 인덱스 재생성 및 깊은 일관성 점검 | 동일 원본 세대와 텍스트/벡터 공간 호환성 확인 |
| A5 | 검증한 불변 런타임 세대 게시 | 현재 pointer와 source fingerprint, 생성 완료 상태 일치 |
| A6 | 실제 후보 pack·상세 선택·구성 감사 | 노출·선택·거절·관계 증거·부분 속성 잠금이 검증됨 |
| A7 | 48개 관련 회귀 시나리오 및 8개 이미지 비교 계획 실행 | 기계적 계약, 현재 이미지의 관계 충족, 전체 표현을 별도 판정 |
| A8 | 사용자 요청 범위에 맞춰 전달·커밋·게시 | 원본·인덱스·런타임·픽셀·수용·Git 상태를 따로 보고 |

수정 중인 기본 checkout의 다른 작업은 reset·stash·전체 stage로 처리하지 않는다. 관련 원본은 ID와 의도별로 병합하고 파생 인덱스는 최종 원본에서 다시 만든다. 충돌 난 인덱스를 한쪽 파일 전체로 선택하지 않는다. 실행 단계에서는 확인한 관련 파일만 좁게 stage하고, 커밋·원격 반영 여부는 사용자 요청에 맞춰 별도로 다룬다.

협력 유지보수에는 기존 `source_update(root, store)` 경계를 사용한다. 원본 변경 후 게시가 끝나기 전의 `source_revision_pending`을 최신 세대 검증 완료로 해석하지 않는다. 이전 요청의 receipt·역사적 프로필·이미지 판정을 새 데이터로 다시 써서 맞추지 않는다.

## 7. 인덱스·관리 도구와 비용 계획

아래는 **미실행 명령 순서**이다. 격리된 구현 checkout에서 관련 원본과 출력 경로를 확인한 뒤 사용한다. 플래그는 현재 스크립트 정의에서 확인했다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/publish_photo_runtime_snapshot.py
```

두 번째·세 번째 명령은 새 임베딩 텍스트가 있으면 외부 임베딩 호출을 만들 수 있다. 현재 연구에는 호출이 없다. 구현 전에 dry-run과 변경된 텍스트 수로 추가 호출·시간·출력 규모를 산정한다. 같은 ID만으로 이전 벡터를 재사용하지 않는다. 공급자·모델·차원·정확한 입력 문장과 레시피의 호환을 확인하고, 호환되는 벡터만 기존 빌더로 재사용한다. 호환 여부가 확인되지 않은 새 문장을 기존 벡터에 붙이는 방식은 사용하지 않는다.

후보 슬롯의 BM25F는 검증한 런타임 원본에서 도출한다. 별도 연구 CSV를 런타임 검색 캐시로 넣지 않는다. 게시가 끝난 뒤 `tools.photo_data_maintenance`의 `build`·`query`·`diff`로 선언된 후보–번들–프로필의 양방향 연결을 다시 점검한다. 이 관리 보고서도 검색 성공이나 의미 충족을 증명하지 않으므로 실제 pack 조회를 별도로 확보한다.

## 8. 회귀와 이미지 검증 계획

[회귀 계획](REGRESSION-PLAN.json)은 48개 시나리오를 갖는다. 주요 묶음은 출처·극성·불확실성, 소유자·접합·수량·방향, 지역 물성·부분 속성 잠금, 선택성·전제·검색 오염, 인덱스·런타임 현재성이다. 이는 계획이며 실행된 테스트 개수가 아니다.

기존 검증 모듈은 변경 범위에 맞춰 사용한다: `test_photo_clothing_terminology_semantics`, `test_photo_fashion_fit_semantics`, `test_photo_color_relations`, `test_photo_visual_grammar_integration`, `test_photo_textile_opacity_effect_scope`, `test_photo_candidate_semantics`, `test_photo_prepack_isolation`, `test_photo_runtime_freshness`. 기존 불변식이 충분하면 유사한 테스트를 중복 추가하지 않고, 실제 새 관계·오류 경계를 위한 사례만 추가한다. 모든 모듈·전체 suite를 관성적으로 반복 실행하지 않는다.

[이미지 비교 계획](NATIVE-VALIDATION-PLAN.json)은 8개 장면, 장면당 기존/보강 데이터 2조건, 최초 16장으로 설계했다. 이는 미래에 해당 생성 범위가 요청된 경우의 예산이며 이번에 이미지를 생성하지 않았다.

| 비교 | 초점 |
|---|---|
| N01 | 리본 매듭 하나·같은 꼬리·접합점·계속되는 봉제선 |
| N02 | 불투명 몸판·분리 시어 소매·위팔 고정 밴드 |
| N03 | 착용 블라우스·손 접촉·비착용 블레이저 |
| N04 | 하이로 밑단·걸음·같은 치마 안감의 국소 노출 |
| N05 | 한 붉은 면·시작점·연속성·반복 제한 |
| N06 | 같은 치맛단을 아래로 당기는 접촉·방향·신발 관찰 상태 |
| N07 | 트레이 하나·두 인물의 손·인물별 의상 귀속 |
| N08 | 체인의 두 고정점·처짐·검정 내부의 재질 경계 |

두 조건은 실제 요청과 active span, 독립 작성해 고정한 authorial core, 기본 프롬프트, creative controls, 모델·전송 파라미터, 참조 바인딩, 시도 예산과 판정표를 같게 한다. 연구 시나리오를 사람이 말한 요청으로 relabel하지 않는다. 생성 단계에는 실제 요청 원문을 담은 별도 envelope가 필요하다. 후보·프로필 데이터는 core 동결 뒤에만 조회한다. 지원되는 렌더 seed가 있으면 동일하게 하고, 없다면 확률적 차이를 기록한다.

선택 후보나 최종 세부 표현은 조건별로 달라질 수 있으므로 pack→선택→최종 프롬프트 차이를 함께 저장한다. 이 비교는 탐색적인 표본이다. 한 쌍의 성공을 일반 성공률·데이터 단독 인과·항상 더 좋은 미학으로 주장하지 않는다.

각 이미지에서 전체 인상과 원본 해상도의 필수 접합·끝점·부위 상태를 함께 본다. 일부만 구현되거나 필수 연결이 가려진 경우는 통과가 아니다. 부수적인 숨은 지지 구조까지 전신으로 강제로 드러내는 규칙은 만들지 않는다. 실제 요청의 초점과 필요한 관찰 범위를 유지한다.

생성 차단은 `blocked_unscored`로 기록하고 프롬프트·오류·시도 횟수를 보존한다. 유사 프롬프트를 반복해 우회한 결과를 검증으로 쓰지 않는다. 사용자의 명시 수정이 있다면 별도 계보와 의미로 재작성한다.

## 9. 결과 보고 형식

각 카드·구현 묶음에 다음 열을 둔다: `authored_source`, `source_validation`, `index_consistency`, `runtime_generation`, `candidate_exposed`, `candidate_selected`, `prompt_audit`, `native_pixel_review`, `whole_image_observation`, `user_acceptance`, `commit`, `push`.

PASS는 해당 증거층에만 적용한다. 구조 PASS를 이미지 PASS로 옮기거나, 선택된 후보 ID를 실제 부위 재현으로 간주하지 않는다. 사용자 판단이 없으면 `pending`을 사용한다. 기존 기록은 그대로 보존하고 후속 결과를 추가한다.

## 10. 이번 완료 상태

| 항목 | 상태 |
|---|---|
| 503개 원본 사전 및 출처 구분 확보 | 완료 |
| 136개 현재 원본 파일의 어휘 대조 | 완료; 의미·런타임 검증과 분리 |
| 125개 카드, 150개 후보 초안, 20개 조합, 23개 문맥 경계 | 완료; 연구 단계 |
| 단계별 반영 위치·첫 16개 범위·검증 계획 | 완료 |
| 연구 패키지 구조·참조·원본 수 검증 | `PACKAGE-VALIDATION.json`에 기록 |
| 실제 런타임 원본 편집·인덱스 재생성·게시 | 미실행 |
| 임베딩 호출·pack 실행·행동 회귀·이미지 비교 | 미실행 |
| 생성 이미지·커밋·푸시 | 0 / 없음 / 없음 |
