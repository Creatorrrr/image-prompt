# 흙·땅 시각 의미·후보 데이터 반영 계획

작성일: 2026-10-08 KST  
상태: 연구·계획 완료, 운영 반영 전  
근거: [리서치 종합](research-report.md), [120개 연구 카드](research-cards.md), [현재 원본 inventory](existing-inventory.json)

**먼저 문맥의 뜻과 기존 항목을 확정하고, 다음에 선택한 관찰 구현을 원본에 반영한다.** 신규 후보와 profile 수량을 미리 성공 기준으로 잡지 않는다. 96쌍의 초안에서 재사용·통합·분리·보류가 발생할 수 있으며, 실제 반영 수량은 검토된 의미 단위에서 결정한다.

## A. 원본 고정과 범위 확정

1. 구현 시작 시 HEAD·dirty/untracked 상태, source manifest와 모든 실제 로더 원본의 SHA-256을 다시 수집한다. 이번 inventory는 로컬 작업 원본이며 원격 main·게시 runtime의 증거가 아니다.
2. source_update의 협력 변경 상태와 runtime 세대를 확인한다. 공유 작업에서 인덱스 변경이 관측되었으므로 mutable 원본과 게시 세대를 혼용하지 않는다.
3. 기존 작업과 분리할 필요가 있으면 적합한 활성 worktree를 확인한 뒤 재사용한다. 문서 작성만으로 별도 checkout을 만들 필요는 없다.
4. 이번 연구 파일의 버전·해시를 고정하고, 구현에서 바꿀 candidate/profile ID 목록과 기존 ID의 변경 이유를 먼저 작성한다.

완료 증거: 구현 전 원본 지문, 기존 작업 보존 범위, 도구/계약 버전, 채택할 연구 단위와 기존 ID의 명시적 대응.

## B. 표제어의 sense와 관찰 방식을 확정

| 작업 | 첫 범위 | 산출물 | 완료 기준 |
|---|---|---|---|
| 동음·다의어 | 식토, 소성, 토성, 군도, 매장, 자기, 대지, 지각, 사직, 석기 | term+문맥+sense+negative의 유지보수 표 | 다른 뜻의 요청이 서로의 물체·행위를 강제하지 않음 |
| 측정·시간 의미 | pH·CEC·비옥도·투수성·함양·압밀·동토 | 정의와 claim_limits | 외형 표현이 측정·기간·원인 판정으로 승격되지 않음 |
| 도식·현미경 의미 | 지하수·판구조·입경·균근·어글루티네이트 | 표현 방식과 실제 가능한 배율 | 요청하지 않은 투시·화살표·거대화 없음 |
| 분류·문화 문맥 | WRB, 지신/사직, Gaia/Geb, Pachamama/Apu | 명명 문맥과 특정 자료별 범위 | 자료 없는 보편 외형·성별·체형·시대 레시피 없음 |

keyword-routing의 group→연구 queue는 이 단계의 작업 입구다. term→완전 외형 또는 exact activation으로 import하지 않는다. Korean/English 입력에서도 전후 문맥을 보며 의미를 판단한다.

출처 미완료의 우선 후속 조사는 WRB 2024 정정 PDF, 개별 토양군의 진단·현장 사진, 종별 미세 생물 형태, 콥/판축의 상세 구성, 군사 참호의 시기별 자료, 시에나·오커의 안료 자료, 성적 하위문화 WAM/sploshing의 명확한 1차 정의다. 일반 splosh 동사 사전은 마지막 항목의 근거로 사용할 수 없다. 미완료 자료를 사용하는 물리적 후보는 검증된 외형 범위만 남기고 정체성·원인 주장을 제한한다.

완료 증거: source 상태가 연결된 term별 sense 결정과 표현 방식. 새로운 runtime routing 로직은 이 계획의 기본 범위가 아니다.

## C. 기존 자료의 의미·ID를 검토

[reuse-plan.json](reuse-plan.json)의 12개 연구 단위·20개 참조를 기준으로 아래 판단을 수행한다.

| 의미 | 현재 참조 예 | 권장 반영 |
|---|---|---|
| 다각형 건열 | water_w120 / water_rel_w120 | 기존 ID 유지; 건열·균열판·동토 반례와 한국어 문맥 보강 |
| 샘·출수 물길 | water_w002 / water_rel_w002 | 출구·연결된 물길·바탕 관계 유지; 지하 압력은 문맥으로 유지 |
| 우각호·망상하천 | water_w069, water_w070 계열 | 실제 수역 topology 재사용; 폭넓은 하천 이름으로 harden하지 않음 |
| 육계사주 | water_w077 계열 | 양끝 연결과 물의 양쪽 경계 재사용 |
| 카르스트 배수 | karst_closed_depression_losing_stream_resurgence | 보이지 않는 지하 연결의 claim limit 유지; 동굴 내부 후보와 분리 |
| 생물 토양 피각 | biological_soil_crust_patch 등 | 거시 피각과 미생물 확대 의미를 분리; 자연 한국어·관찰 배율 보강 |
| 동결 융해 토양 | freeze_thaw_soil_polygon_patch | 기존 입단/균열 표현과 실제 얼음 쐐기 표현의 동등성 검토 |
| 골렘 | constructed_golem_subject / golem_constructed_material_agency | 흙 몸체만으로 관절·작용 결과의 기존 필수 의미를 잃지 않음 |
| 로버 작업 흔적 | rover_sample_trace_prop | 시료·공구·같은 작업 지점 연결 유지; ISRU 성공을 추론하지 않음 |

같은 형태·owner·행위의 동등한 문장만 기존 paraphrase로 추가한다. 기존 구조에서 existing_slot_context_extensions는 paraphrases/contexts 보강에 제한되어 있으므로 다른 owner·효과·전제는 새로운 항목 또는 별도 유지보수 수정이 필요하다. 문맥 설명은 현재 해석용 저장 면이며 자동으로 검색 임베딩에 반영된다고 가정하지 않는다.

완료 증거: reuse/enrich/new/split/defer 결정, 대상 내용 해시, 보존해야 할 기존 의미, 실제 변경 파일·ID. 단순 문자열/벡터 근접성으로 자동 병합하지 않는다.

## D. P0 물리 단위를 첫 배치로 작성

P0 26단위 중 20개 물리 초안이 있다. E012는 재사용이므로 최대 19개 신규 구현 제안에서 시작한다. 실제 추가 수량은 C의 판단에 따라 줄어들 수 있다.

| 묶음 | 연구 단위 | 첫 구현의 목표 |
|---|---|---|
| 입자·기질 | E002, E004, E005 | 입경/원마도/입단을 각각 owned component로 유지 |
| 분진·상태·흔적 | E007–E012, E014 | 발생점·물/바탕 경계·국소 광택·압흔·밀려난 가장자리 |
| 단면·색 | E016, E017, E019, E021 | 수직 연속성·층 경계·기반암 접촉·물체색 |
| 침식·생물성 바탕 | E036, E038, E080, E081 | 내리막 물길·하안/뿌리·낙엽/바탕의 연결 |
| 몸과 의복 | E109, E110 | 국소 두께와 부착·청결/피막 경계; 기존 피부·의복 잠금 |

E004는 둥근 자갈과 각진 쇄석을 분리한다. E005는 입단과 경운 흙덩이의 주장 범위를 제한한다. E016의 depth scale·E021의 colour reference는 조사용 변형의 소품이다. 일반 풍경에는 그 소품을 기본 필수 요소로 강제하지 않는다. E007은 이미 core에 있는 바퀴 등의 발생점과 연결되는 구현이며 바퀴를 새로 추가할 일반 먼지 레시피가 아니다.

완료 증거: 선택한 physical realization의 Korean/English 구성 문장, owner별 evidence/gate, 모든 부착·압력·층위·연결의 관계, 최소 1개 역관계·다른 owner·부정 요청.

## E. 원본 파일과 기존 계약에 반영

권장 신규 파일 이름은 photo_prompt_soil_earth_extension.json과 photo_prompt_visual_obligations_soil_earth.json이다. **아직 만들거나 등록하지 않은 제안 이름**이다. 재사용 판단에 따라 일부 내용은 기존 물·자연환경·공예 자료에 소폭 보강하는 편이 적합할 수 있다.

| 원본 항목 | 작성 필드 | 검토 기준 |
|---|---|---|
| candidate | ko/en, keywords/paraphrases, embedding_text | 넓은 과학·문화 label과 선택한 형태의 차이를 보존 |
| candidate semantic surface | concept_terms, concept_units, relations | 구체적인 관찰 phrase와 방향 있는 관계; 같은 단어만 반복하지 않음 |
| 효과 범위 | affected_dimensions, affected_properties | 실제 바뀌는 owner·속성; material 편집이 pose/appearance/setting 잠금을 우회하지 않음 |
| candidate 문맥 | 현행 requires/exclude/contextual_usage 면 | frozen core 및 최종 scene의 전제; 해석 메모를 search guard로 오인하지 않음 |
| visual profile | activation, semantics, claim_limits | 이름·유사도가 전체 외형을 harden하지 않음 |
| authored components | 현행 v1 또는 필요한 v2 | collective 관계는 v2 검토; source에서 compiler projection 중복 작성 없음 |
| runtime expression | definition_with_optional_label 등 현행 값 | 추상 label 없이도 물리적 의미가 읽힘 |
| maintenance provenance | research unit/source/status/content hash | runtime source에 미지원 연구 키를 추가하지 않음 |

현재 96개 draft는 Python source 계약/컴파일을 통과했지만 최종 필드/의미 검토가 남아 있다. 특히 다중 변형의 E024, E067, E100, 서로 가까운 E018/E023, 취향/정체성 문맥은 split/merge/defer를 확정해야 한다. E100의 닫힌 봉분과 내부 석실을 같은 자연 사진의 필수 gate로 import하지 않는다.

profile와 candidate는 서로 다른 검색·활성화 면으로 유지한다. profile와 연관된 bundle을 도입한다면 같은 소유 관계와 선행 조건을 만족하는 실제 member만 묶는다. 번들 선택은 profile 전체 활성화의 증거가 아니다. 모양을 넓은 스타일이나 프리셋에 일괄 연결하지 않는다.

## F. 원본·검색·runtime 검증

아래 명령은 **향후 구현 뒤의 실행 계획**이며 이번 작업에서 실행한 명령이 아니다. 실행 전 현재 CLI help와 source_update 상태를 재확인한다.

~~~bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --help
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --help
~~~

1. 원본 키·중복 ID·source manifest·bundle 참조·effect 범위를 검사한다.
2. 실제 변경으로 영향받는 candidate와 visual index를 canonical builder에서 재생성한다. 벡터 재사용은 entry key와 **전체 embedding text, provider, model, dimension이 모두 같을 때**만 허용한다. 새/변경 텍스트는 현재 유지보수 계약의 batch-size 1 방식을 따른다.
3. semantic index는 전체 slot 원본으로 BM25F document와 통계를 재계산한다. visual registry hash가 바뀌면 visual index도 재생성한다. 생성 index나 shard conflict를 손으로 맞추지 않는다.
4. 두 index와 slot preparation이 같은 source 세대를 가리키는지 깊이 검사하고 publish_photo_runtime_snapshot.py의 게시 결과를 확인한다. CURRENT만 먼저 바꾸거나 게시 실패를 이전 세대로 숨기지 않는다.
5. source와 runtime content hash·generation·개별 request receipt가 맞는 상태에서 V6 pack을 생성한다. primary checkout을 사용 중인 과거 pack을 최신 mutable source로 다시 해석하지 않는다.

핵심 의미 검증 대상은 전체-request sense, 자연 Korean/English 발견, 다른 owner·역관계·부정, broad label의 불필요한 hard 활성화, source-followup 상태, partial lock, 이미 잠긴 framing/appearance/material이다.

80개 canary는 32개 sense 대조, 28개 owner 관계 대조, 12개 비가시성/부정, 8개 property 잠금 계획으로 구성한다. 실제 구현 뒤 예상 결과·노출·eligibility·선택·필수 의무를 각각 기록한다. canary 문장으로 정확성을 인증하지 않고 별도의 독립 자연 요청을 추가한다.

관련 검증은 물 관계·자연환경·후보 의미·시각 profile·core retrieval·source manifest·runtime freshness·문맥/잠금 모듈에서 시작한다. 실제 변경 범위에 맞는 검사를 통과한 뒤 요구되는 전체 검사를 수행한다. 이전부터 재현되는 실패가 있으면 이전 baseline과 새 실패를 분리하여 보고하며 gate를 약화하지 않는다.

완료 증거: 검토된 원본 diff, source manifest, 두 index의 깊이 검사, runtime 게시 generation, 실제 candidate/profile 노출 및 강제 여부의 사례별 결과.

## G. 프롬프트·픽셀·사용자 판단

[검증 시나리오군 12개](validation-case-plan.json)를 사용한다. 변형 분리를 포함하면 최소 16개의 개별 장면이 되는 현재 계획이다. 이미지 생성은 향후 명시된 생성/qualification 범위에서 수행한다.

| 검사 층 | 성공 조건 | 성공으로 볼 수 없는 것 |
|---|---|---|
| candidate discovery | 목표 의미가 적격한 선택지로 노출됨 | 슬롯에 문자열이 존재함 |
| adoption | 열린 효과 범위 안에서 실제 선택됨 | 검색 hit·bundle 연관 |
| prompt/runtime | 같은 core·source 세대, 완전 evidence와 owner 관계 | 코드 계약 통과만 |
| native pixels | 모든 필수 요소·부착·방향·같은 표면이 실제 보임 | 프롬프트에 적혀 있음·일부 요소만 구현됨 |
| user judgment | 요청한 미학·의미가 사용자의 목적에 맞음 | 연구자 자체 점수 |

미세 재료는 원본 픽셀을 검사한다. 지형 topology는 연결 양끝을 포함하는 전체 프레임에서 확인한다. 국소 피부/천 접촉은 모든 접촉부가 같은 crop에서 보여야 한다. 과학 분류·화학·시간·정체성·취향·동의는 픽셀의 pass/fail 대상이 아니다.

누락이나 잘못된 owner의 부분 구현은 partial_is_fail로 기록한다. 검색 문구·prompt 수정만으로 native pixel 상태를 pass로 갱신하지 않는다. 이미지 실패를 해결하기 위해 request lock이나 독립 core를 소급 약화하지 않는다.

## H. 후속 배치와 최종 납품

P1은 토양 구조·분류 문맥·배수/수역 연결·건축/도예, P2는 지질 시간·문화·재해 원인·하위문화·천체 미세 시료를 순차 반영한다. 연구 card별 source pending이 있는 경우 물리적 구현과 그 배후 주장을 분리하여 채택·보류한다.

최종 기록에는 실제 추가/수정/재사용/보류한 ID, source 상태, 원본과 index/runtime 세대, 수행한 검사와 미수행한 검사, 실패한 장면과 native pixels, 사용자 판단을 구분한다. commit/push/PR은 실제 수행한 경우에만 별도로 기록한다.

실행 순서는 A→B→C→D→E→F→G이며, H는 각 배치의 결과를 모으는 납품 단계다. 이번 요청의 산출물은 이 연구·계획 패키지까지다.
