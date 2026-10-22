# 리서치 결과의 데이터 반영 계획

현재 완료 범위는 연구·기존 데이터 진단·한영 초안·검증 설계다. 아래는 후속 구현 계획이며 운영 파일을 변경하거나 설치한 결과가 아니다.

## 1. 구현 직전 현재 상태를 다시 고정한다

BASELINE 이후 manifest 모듈 수가 59에서 61로 바뀐 것을 관찰했다. 진행 중인 다른 수정·미추적 파일을 되돌리거나 전체 stage하지 않는다. HEAD·branch·dirty/untracked·manifest의 전 모듈·`photo_candidate_search.json`·`retrieval-runtime.json`·설치 세대/포인터를 다시 기록한다. 작업에 필요한 현재 dirty 소스가 있다면 allowlist와 파일 해시를 포함한 별도 구현 기준을 고정한다.

읽기 전용 설치 상태 확인은 저장소 루트에서 다음 진입점으로 수행한다. 이번 연구에서는 운영 검사를 실행하지 않았다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

이 검사는 선택된 설치 코드·Python·recorder 의존성의 확인이다. 새 데이터의 의미·검색·픽셀 승인이 아니다. 검증 당시 체크아웃에서 지원 인자와 runtime Python을 확인한다.

## 2. 카드마다 하나의 채택 결정을 기록한다

| 결정 | 판단 조건 | 저장할 증거 |
|---|---|---|
| reuse | 기존 **전체 선택 원문**이 같은 owner·수·구조·끝점·모드를 갖고 모든 부가 효과도 요청에 맞음 | CID/RID, owner 파일, 전체 조건·effects·binding·선택 branch·의무 비교 |
| refine | 의미는 같으나 번역·정의·질의 노출·근거·표현이 부족 | 전후 diff, 기존 의미 보존, 영향을 받는 native proof와 인덱스 재검증 범위 |
| new | 가장 가까운 기존 complete source로 필요한 관계를 충족할 수 없음 | 비교 CID, 정확히 빠진 관계, 새 소스 전체 문장·조건·효과 |
| context | 동의·진단·의식·시간·음향·역사·의도·법적 상태 | positive 시각 사실로 승격하지 않는 저장·loader 계약 |
| defer | 개별 정의·시대·부위·임상 형상·원전 근거가 부족 | 누락 자료, 재개 조건, 보류한 주장 |

초기 재사용 우선은 D16의 봉합 연결과 L01의 배양 구조다. D04–D08은 배액·주입·구강·마스크·목 경로를 각각 비교한다. 같은 `tube` alias나 슬롯 때문에 합치지 않는다. X 카드는 장르 자동 활성화·진단 단정을 막는 문맥이며 candidate 양성 레코드로 일괄 복사하지 않는다.

## 3. 구현 묶음과 우선순위

| 단계 | 구체 범위 | 완료 기준 |
|---|---|---|
| P0a | A01–A05/A07–A11의 공간 관계, D01–D07/D10–D13의 기구·표기·표본 | 기구·경계·끝점·표면·텍스트를 구별하고 중복 후보 판정을 완료 |
| P0b | E01/E03–E05/E07/E11/E12의 단서·가림·프레이밍 | 진단·동의·의식을 추가하지 않고 관측 가능한 관계만 저술 |
| P1 | W01–W03/W05–W12의 상처·층·접점, D08/D14–D18, L01–L06/L09, 관람·퇴원 구도 | 모형·허구·성인·스케일의 조건이 한영 전체에 보존되고 가장 가까운 대체형과 분리 |
| P2 | A06/A10의 시대별 재현, W04의 부위별 탈출, L07/L08, E08/E10/E13와 X01–X22 | 출처별 전문 확인·문맥 경계·별도 선택 조건 충족; 부족하면 defer 유지 |

표의 단계는 자동 승인 순서가 아니다. 각 카드의 `priority`와 묶음 내 실제 영향 범위를 함께 검토한다. 수술·민감부위·폭력·성 관련 단어를 편의상 삭제하지 않고, 각 문맥을 정의와 가시 제안으로 나눠 판단한다.

## 4. 반영할 파일과 단일 권위

아래 경로는 후속 구현의 예상 대상이다. 이번에 생성·수정하지 않았다.

| 경로 | 역할 |
|---|---|
| `skills/photo-prompt-image-generator/assets/photo_medical_horror_semantics_20261022.json` | 출처·원 용어·카드·채택 결정과 실제 CID/RID를 잇는 레지스트리 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_medical_horror_20261022.json` | 승인한 신규 **complete source**만 담는 v3 후보 모듈 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_medical_horror_bindings_20261022.json` | 현행 slot catalog 의미를 직접 충족하는 역할 연결 |
| 재사용/수정 CID의 기존 owner 파일 | refine에 필요한 부분만 수정. 전 shard 일괄 재작성 금지 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 승인한 모듈 명시 등록 |
| `skills/photo-prompt-image-generator/references/medical-horror-visual-semantics.md` | 출처 한계·혼동 경계·유지보수 지침 |
| 실제 영향받은 회귀 fixture | 연결·가림·텍스트·단면·조건·번역·문맥의 회귀 |

현재 `photo_candidate_corpus.py`의 native 레코드는 `id / record_kind / content / conditions / effects / provenance`를 소유한다. intrinsic 조건과 effects는 top-level 단일 권위다. 연구 카드의 추정 dimensions·owner graph·source refs를 권한이나 native proof로 복사하지 않는다. `candidate-drafts.json`은 runtime 스키마가 아니다.

branch가 있다면 선택한 RID의 조건·효과·의무를 함께 읽는다. 구강·마스크·기관절개, 닫힌 병·개봉 병, 표면 사진·단면 모형은 각각 독립적인 완전 실현 또는 명시적 상호 배타 branch로 저술한다. 서로 다른 branch의 일부를 합쳐 불가능한 장치를 만들지 않는다.

## 5. 원문·번역·조건·효과·역할을 함께 검토한다

한영 두 문장 모두 대상·수·성인/모형 설정·접점·경로·가림·문자·화면 안팎을 보존한다. `fictional`, `illustrative`, `staged`는 삭제 가능한 수식이 아니다. 자료의 정의와 긍정 실현을 분리하며 claim limit·부정 예·허구적 기관의 주장은 양성 embedding 텍스트로 섞지 않는다.

| 카드 | 필수 원문 검토 | 실제 영향 검토 |
|---|---|---|
| D04 배액 | 피부 외부 시작점·관·벌브·환자복 고정 | patient body region/contact, tube/bulb object structure, gown contact/placement |
| D05 주입 | 주머니·펌프·팔 접점의 같은 관 | 기구·팔·기존 인물 수·구도·가시 범위 |
| D06/D07/D08 | 입/마스크/목을 각각 분리 | 얼굴·목 geometry, 장치 연결·의복·가림; 임의 진단 없음 |
| D11 코드 불일치 | 두 코드가 동일 화면에서 실제로 다름 | 두 텍스트 owner·프레이밍·초점·크기; 신원 오류는 없음 |
| W03 누공 도식 | 양 끝과 연속 통로, 명시적 단면 매체 | anatomy/model structure, medium, 필요한 내부 가시성 |
| E06 관람 | 관람자·유리·시연대·성인 모형은 별도 대상 | 인물 수·관계·배경·가림을 모두 실제 효과로 검토 |
| E07 진료 가림 | 환자·문·가림막의 시야 관계 | 노출·의복·상대 위치; 동의·성적 의미는 효과에 추가하지 않음 |

슬롯은 검색 역할이며 소스 전체 effects를 소유하지 않는다. `prop`으로 제안된 소스라도 사람·행동·배경·count를 바꾸면 모두 검토한다. role 부적합/보류된 binding을 unbound 경로로 우회하지 않는다. 동일 owner에 모든 dimension을 기계적으로 곱하는 방식으로 권한을 늘리지 않는다.

## 6. 구조·의미 회귀와 검색 검증

구현한 스키마·단일 권위·condition/effect·branch·한영 보존·원본 closure부터 검증한다. 구체적인 현재 명령과 지원 인자를 확인한 뒤 사전 validator와 영향받은 테스트를 수행한다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

여기 적은 운영 명령은 계획이며 이번 연구의 실행 결과가 아니다. 검증에 실패하면 그 범위를 고친 후 다음 단계로 진행한다.

별도 staging 인덱스에서 provider/model/space/dimension/recipe/source text hash/vector integrity를 고정한다. 정확히 호환되는 기존 벡터만 재사용한다. 현재 검색 manifest는 `photo_candidate_search.json`이다. 연구 폴더를 active corpus로 추가하거나 운영 포인터를 먼저 바꾸지 않는다.

[평가 질의](EVALUATION-CASES.tsv)는 개발 24·혼동 경계 20·일반 대조 12·비가시 대조 8, 총 64사례/128개 한영 질의다. 전부 `NOT_RUN`이다. 기존 슬롯 검색과 독립 whole-scene 경로에서 각각 실제 질의·lane·slot·CID/RID·원문·순위·노출·오탐을 남긴다. 라벨 hit, keyword-only 진단과 실제 hybrid 결과를 구별한다.

초기 제안 기준은 P0 개발 사례에서 **한영 각각 eligible complete-source Recall@10 ≥90%**, 경계 사례에서 금지 대체형의 정답 채점 0건, 문맥→가시 사실의 오승격 0건, 일반 대조에서 비요청 의료·고어·노출·인물 수 변경 0건이다. 90%는 탐색 커버리지 목표다. 실제 채택한 소스의 모든 hard gate·조건·lock은 100% 충족해야 한다. 부분 일치는 정답으로 세지 않는다.

개발 질의가 저술 문장과 같은 라운드에서 만들어진 한계가 있다. 튜닝을 마친 뒤 다른 사람이 쓴 새로운 요청 16개 이상으로 holdout을 구성한다. 같은 질의를 번역하거나 어순만 바꾼 것을 독립 holdout이라고 부르지 않는다.

## 7. 선택·프롬프트·원본 이미지·운영 반영

원 요청과 creativity controls만으로 후보 없는 baseline/core를 먼저 동결한다. 연구 자료·후보 목록이 독립 core를 결정하는 재료로 들어가지 않게 한다. 그 후 전체 의미·허용된 변경 범위 안에서 기존/보강 후보를 비교하며 모두 거절하거나 baseline을 유지할 수 있다.

선택한 CID/RID의 전체 실현과 literal prompt evidence를 감사한다. 구도 때문에 필요한 끝점이 안 보이면 후보 채택이나 프롬프트 PASS로 이미지 성공을 대신하지 않는다. [픽셀 계획](PIXEL-PLAN.md)의 12개 사례×3 arms에서 원본 이미지를 비교한다. 검색 노출·선택·문장 운반·이미지 관계·의료 호러 읽힘·작품성·사용자 수락은 각각 별도 상태다.

검색·구조·원본 이미지가 승인된 좁은 범위만 봉인하고 설치 검증·활성화·롤백을 수행한다. source edit, index build, sealed generation, installation, active pointer, commit/push를 각각 보고한다. 현재 연구만으로 설치나 CURRENT를 바꾸지 않는다. 실제 commit이 요청되면 검토한 파일 allowlist만 stage하고 기존 dirty 파일은 보호한다. push는 별도 요청 범위를 따른다.

롤백은 이전 소스·인덱스·설치 세대의 해시/포인터를 보존한 상태에서 수행한다. 부분 설치나 source/index hash 불일치, 실제 검색의 원문 불일치, 동의·진단 오승격, 일반 대조 회귀가 있으면 활성화하지 않는다.
