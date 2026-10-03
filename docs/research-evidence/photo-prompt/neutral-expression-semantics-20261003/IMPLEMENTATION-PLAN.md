# 연구 결과를 시각 의미 데이터와 후보팩에 반영하는 계획

2026-10-03 · 제안 상태 · 이번 작업에서 운영 데이터·코드·인덱스는 수정하지 않았다.

우선순위는 **현재 의미 소유 범위와 라우팅을 확인하고, 기존 계약을 보강한 뒤, 부족한 관찰 단위만 추가하는 것**이다. 181행을 181개 별칭이나 44개 새 프로필로 옮기지 않는다. 장르·비하·역할·시간 정보는 그 뜻이 존재하는 층에 보존하며 후보가 원문에 없는 체형·사건을 만들지 않도록 한다.

## 1. 입력 고정과 선행 확인 — P0

현재 작업 트리에는 신체 형태 통합과 다른 작업이 있으며, 연구 마감 시 시각 계약·시각 인덱스·의미 인덱스 3개 파일이 병합 충돌 상태였다. 조사 시작 후 입력 74개 중 8개 해시가 달라졌으므로 [기존 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CORPUS-RECEIPT.json)의 HEAD만으로 A/B 기준선을 고정할 수 없다. 기존 병합 작업에서 충돌이 해소된 뒤, 구현 시작 시 registry·candidate corpus·관련 코드·정책·인덱스의 **실제 내용과 해시**를 별도 구현 증거 폴더에 보존한다. 기존 변경의 소유 범위를 먼저 확인하고 이 연구 범위와 섞인 상태로 커밋·인덱스 교체를 진행하지 않는다. 이번 연구 작업은 기존 충돌을 수정하지 않았다.

먼저 NR001–004의 유효한 V6 envelope와 frozen authorial core fixture를 만든다. 도덕적 타락, 몸에 실제 변화가 번지는 타락, 요청자 정의의 override, 해당 의미의 부정을 서로 독립 요청으로 고정한다. 초기 M09 진단은 artificial source row만 사용했으므로 이 단계에서 실제 `normalize_authorial_core`와 전체 source collection·resolver·candidate pack 경로를 거친다.

도덕 서사에서도 신체 변형 hard 의무가 발생하면 기존 `embodied_corruption_transition.activation.context_disambiguation`의 허용 근거를 좁힌다. `인물의 타락`, `changes allegiance` 같은 넓은 표현만으로 현재 신체 변화가 확정되는지 검토한다. broad alias 전면 삭제·제외어 나열에 앞서 요청된 의미, 직접 정의, 물리적 변화의 양의 증거를 구분한다. 신체 변화 요청의 기존 이전 표지·경계·현재 변화 계약은 함께 검증한다.

완료 조건: 현재 기준선의 실제 full-core 관찰, 원문/해석/core/선택/의무의 출처 연결, 도덕·신체 뜻의 분리와 정의·부정 우선이 기록돼 있다. 조건부 수정이 필요 없으면 해당 이유를 남기고 데이터 보강으로 넘어간다.

## 2. 기존 신체·표면 계약 보강 — P1

U01–15, U17, U27–36부터 적용한다. 원문에서 실제로 지칭한 소유자·부위·비교·속성을 유지하는 양의 `definition`, `paraphrase_examples`, `component_semantics`를 기존 owner 안에 추가한다. 원인·이력·평가를 넣지 않는 `reject_substitutes`와 evidence/render gate를 함께 보강한다.

우선 대상은 상대적 큰 가슴/전신 살집/곡선, 부착 폭/높이/돌출/분포, 골반 폭/둔부 돌출/허벅지 볼륨, 근육 크기/정의, 입술 구조, 피부 선형 띠/요철이다. `root height`·방향 등의 뜻은 현 owner 계약의 범위를 먼저 검토하고, 외부 분류가 미확인인 broad alias는 보류한다. 작은 가슴 요청을 큰 가슴 프로필의 긍정 활성화로 대신 표현하지 않는다.

표현별 결정은 [TERM-DECISIONS.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/TERM-DECISIONS.json)의 `preserve`, `do_not_add`, `external_evidence_scope`에 따른다. 근거가 있는 한 lemma가 같은 행의 다른 한국어 표현·속어까지 검증한 것으로 처리되지 않도록, 구현 데이터에 넣을 **개별 철자·품사·의미·문맥**을 다시 명시한다. 외부 근거 미연결 78행은 자동 exact 활성화 목록에 넣지 않는다. 형태가 명시된 좁은 절은 기존 계약으로 처리할 수 있다.

완료 조건: NR015–028·058–059의 교차 형태와 원인 미추론 사례를 통과하고, 각 의미가 기존 owner에서 유지되거나 좁은 scope review로 보류돼 있다. 추가 프로필 수보다 중복 owner·강제된 다른 축·추가된 원인의 수가 0인지 확인한다.

## 3. 표정·시선·의복 관계의 부족분 — P1/P2

U16의 현재 입 내밂은 `expression`의 기존 항목을 전수 비교한 후 실제 동작이 빠진 경우에만 추가한다. `pouty`라는 평가·다의어 전체를 동작 exact 별칭으로 만들지 않는다. U18–19는 `pv_side_eye`, `pv_half_lidded`, `pv_gaze_direct`, `same_adult_target_coordinated_gaze` 등의 현재 방향/상태를 재사용하며 주체·대상 결속을 검증한다. 얼굴의 구조와 현재 동작은 다른 잠금으로 검토한다.

목 장식 U24는 accessory structure의 물체·부착 owner, 구속 U25는 연결·고정점과 현재 제한 동작을 먼저 비교한다. 재료 U26, 중앙 경계 U29는 기존 재료·의복 관계 owner와 중복 검사한다. `cleavage`를 목선 노출의 exact 동의어로 만들지 않고, 넓은 `sideboob`·`underboob`와 좁은 `pfe_` 구조의 포함 관계를 명시한다. 의복 아래 외곽과 일반 주름, 실제 부위명은 서로 대체하지 않는다.

추가가 필요할 때만 현재 로더가 읽는 확장 파일에 넣거나 새 확장 파일을 등록한다. 새 runtime 의미 저장소는 만들지 않는다. 새 프로필은 최소 구성요소, 부위·물체의 소유 관계, 시점, 혼동 대상, 거부 대체물, 필수 증거와 부분 실패 게이트를 갖춘다. exact 별칭은 해당 **전체 뜻**을 직접 요구하는 문맥과 부정·다의어 경계를 검증한 후에만 추가한다.

완료 조건: NR029–038·051–053·075–078·081–083 통과, 관련 계약의 포함/비동의 관계 명시, 한 요소만 있는 장면이 전체 프로필 통과로 처리되지 않는다.

## 4. 맥락 정보를 기존 계약에 연결 — P2

K01–12를 평가·발화·장르·역할·내면·시간의 해석 지침으로 적용한다. 실제 구현 위치는 기존 `contextual_usage`, `claim_limits`, activation 문맥 판별, authorial core의 관계/서사 필드다. 새 context JSON은 이번 연구의 검토 목록이며 독립 런타임 DB로 읽게 하지 않는다.

역할·동의·이력·게시 목적이 요청에 명시된 경우 그 정보를 삭제하지 않는다. 사진에서 확인할 수 없다는 이유로 원문에서 지우는 것과, 픽셀 근거로 검증됐다고 부르는 것은 각각 오류다. 불확실 합의를 consensual로 자동 변경하지 않으며, 소품이나 크기에서 역할·실제 취향을 추론하지 않는다. PWP·Dead Dove·darkfic·NTR·bimbofication 같은 표지는 별도 시각 사건을 사용자 원문이 알려 주기 전 자동 장면 템플릿으로 쓰지 않는다.

원문에서 관찰 절·관점·시간/이력을 분리한 의미 보존 장부를 구현 증거에 남긴다. 보존되지 않는 뜻은 단일 프레임 한계 또는 정보 부족으로 명시한다. 25개 이전 assistant 작성 예시는 현재 요청 source row·사용자 정의에 삽입하지 않는다.

완료 조건: NR039–057·060–063·084의 뜻 보존, 다의어 분리와 비추론 사례 통과. 장르·역할 명칭만 있는 경우 새 body_geometry나 노출·행동 의무가 생기지 않는다.

## 5. 후보 데이터와 효과·잠금 적합성 — P2

[CANDIDATE-DRAFTS.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CANDIDATE-DRAFTS.json)의 24개를 재사용·보강·중복 검사·복수 축 보류 순서로 처리한다. `NC` ID와 속성명은 연구용이다. 실제 export에서는 존재하는 runtime property inventory로 매핑하고 owner/target placeholder를 frozen core의 실제 ID에 바인딩한다.

모든 후보의 전체 정의·대상·부위·필요 객체·행동·가시성 전제는 frozen core에 먼저 있어야 한다. 후보 A가 후보 B의 전제를 만드는 방식은 채택하지 않는다. `affected_properties`는 target·dimension·property를 모두 명시하며, broad/unknown 효과·부분 선언은 잠금 호환으로 승인하지 않는다.

현재 슬롯 정책 기준으로 NC10·11·14·23·24는 보류다. `relational_action`은 action, `wearable_accessory`는 appearance, `body_pose`는 pose만 선언된 슬롯인데 후보의 실제 효과는 더 넓다. 전체 의미를 유지하는 여러 grounded 후보로 분해할 수 있는지 검토하고, 분해로도 효과가 사라지지 않으면 해당 후보 유형과 slot policy를 함께 검토한다. 단순히 넓은 차원 배열을 더하거나 후보를 다른 슬롯으로 옮겨 잠금 검사를 우회하지 않는다. 빈 `slot_dimensions`도 무제한 변경 허가로 해석하지 않는다.

완료 조건: NR064–075의 미선택 advisory, 정의 우선, 전제·대상·속성 잠금, 복수 효과, 예산·검색 오염 사례가 통과하고 보류 후보가 암묵적으로 채택되지 않는다.

## 6. 파일별 변경 위치

| 위치 | 계획된 변경 | 선행 조건 |
| --- | --- | --- |
| [기본 시각 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json) | 기존 신체·초대·타락 계약의 문맥·구성요소·반례 검토 | full-core 타락 진단과 기존 변경 범위 확인 |
| [신체 형태 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_body_morphology.json) | 부착·돌출·분포·표면·현 자세의 독립 축 보강 | 기존 미커밋 body 통합을 기준선으로 고정 |
| [신체 후보 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_body_morphology_extension.json) | 기존 좁은 clause 후보의 정의·효과·대비 보강 | runtime 속성명과 부위별 잠금 매핑 |
| [지역 노출 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json) | 좁은 옷 구조와 넓은 지역 표현의 범위 비교 | broad 별칭의 범위 불일치 해결 |
| [일반 후보](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) 및 현 확장 owner | 기존 시선·재료·돌봄 후보 재사용/문맥 연결 | 실제 source owner 확인·중복 검사 |
| [생성기](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py)·[후보 의미 정책](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py) | 데이터만으로 해결되지 않는 문맥/효과/대상 결속 검토 | 정책 수정 필요성의 실패 fixture 확보 |
| [retrieval contract](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/retrieval-contract.md) | 원문 의미 보존·현재 관찰/맥락 분리·broad alias와 좁은 owner 포함 관계 명시 | 코드·데이터의 실제 계약과 일치 |
| [visual index builder](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py)·[semantic index builder](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_semantic_index.py)와 생성 인덱스 | 확정한 데이터만 기존 경로로 재생성 | 데이터·정책 확정, source hash·model/dimension 계약 확인 |
| tests 및 fixtures | 기존 body/pose/visual/core/candidate 테스트에 실제 사례 배치 | 연구 JSON을 실행 테스트로 착각하지 않음 |

테스트 위치는 [body morphology](/Users/chasoik/Projects/image-prompt/tests/test_photo_body_morphology_semantics.py), [visual profile retrieval](/Users/chasoik/Projects/image-prompt/tests/test_photo_visual_profile_retrieval.py), [candidate semantics](/Users/chasoik/Projects/image-prompt/tests/test_photo_candidate_semantics.py), [authorial core V6](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core_v6.py), [portrait fashion exposure](/Users/chasoik/Projects/image-prompt/tests/test_photo_portrait_fashion_exposure.py), [pose vocabulary](/Users/chasoik/Projects/image-prompt/tests/test_photo_pose_vocabulary_semantics.py)를 우선 검토한다. 데이터만 복제해 자기 자신을 확인하는 테스트 대신 소유자·의미·잠금·관찰 관계가 다른 사례를 둔다.

## 7. 검색·전체 후보팩 비교와 채택 기준 — P3

데이터와 의미 정책 수정이 끝난 뒤 새 기준선에서 인덱스를 만든다. visual index와 semantic index의 registry/data hash, model ID·vector dimension, 생성 시각을 기록하고 기존 벡터 재사용은 builder가 같은 문서·모델 계약을 확인한 경우에만 허용한다. 이번 연구 중에는 인덱스를 재생성하지 않았다.

같은 frozen request/core와 같은 설정으로 A=수정 전, B=수정 후를 비교한다. 순서는 exact 문맥 → BM25F → embedding → 전체 V6 pack이며, 각 단계의 input hash·해석 출처·hit·eligibility·노출·선택·hard/optional 상태를 저장한다. 하나의 전체 pack 안에서 slot-focused query를 사용하며 슬롯별로 다른 core를 만들지 않는다. `required_slots` 자체가 사용자 의미라는 가정을 추가하지 않는다.

자료 작성에 쓴 표현의 개발 사례와 별도로 새로운 동의 표현, 대상/부위 교체, 부정 범위, 물체 문맥, 혼합 의복 문맥의 holdout을 고정한다. holdout 문장과 기대 결과는 인덱스 패러프레이즈·키워드·예제로 넣지 않는다. 동일 후보 수·활성 슬롯·core/support 구분 아래 비교한다.

| 지표 | 정의와 채택 기준 |
| --- | --- |
| 의미 보존 | 요청의 부위·관계·평가·시간 원자가 유지됐는지;핵심 원자 누락 0 |
| 의무 과잉 | 원문에서 근거 없는 hard 의미·대상·부위 수;P0 fixture에서 0 |
| 속성 침범 | 잠긴 target/dimension/property 변경 수;0 |
| 전제 생성 | 후보가 요청에 없는 주체·대상·사건·가시성 전제를 만드는 수;0 |
| 관련 후보 접근 | 각 요청의 전체 범위에 적합한 후보가 제한 예산 안에 있는지;예산 충족만으로 성공 처리 안 함 |
| pack 예산 | 일반 후보 최대 64,core 슬롯당 최대 4,support 슬롯당 최대 2;현재 계약과 함께 검증 |
| 중복·범위 혼동 | 같은 관찰 뜻의 owner 중복과 broad 별칭→좁은 계약 오역;해결 또는 명시 보류 |
| 신규 회귀 | 기존 관련 test 실패 ID와 새 의미 실패;기존 기준선과 비교하여 새 실패 0 |

ranking 숫자 하나만으로 채택하지 않는다. exact는 요청의 뜻을 정확히 확인한 경우에만 hard일 수 있고, BM25F/embedding은 선택 전 advisory다. 적절한 후보가 없거나 core와 잠금이 충돌하면 모두 거절할 수 있어야 한다.

## 8. 픽셀 검증과 마감 — P4

의미·팩 검증이 끝난 구현에 한해 이후 별도 이미지 검증을 설계한다. 우선 입술 구조/현재 동작, 눈·대상 결속, 부착 폭/돌출의 교차, 직물 존재/투과, 옆·아래 옷 경계, 가까운 다리의 연속 배경을 대표 사례로 고정한다. 비교군의 prompt/negative bytes, request/core hash, 선택·효과·assertion, 참고 범위, 생성 환경과 seed 등 실제 제공 가능한 통제를 동일하게 기록한다.

이미지를 보기 전 evidence gate를 고정한다. 부위·소유자·물체 연결·필수 구성요소 중 일부만 보이는 경우 `PARTIAL`이며 `partial_is_fail`로 실패 처리한다. 시간·내면·합의·이력은 원문 근거와 현재 장면의 관찰을 구분한다. 참고 사진은 명시된 성인 얼굴·머리 외관 범위를 지키고 체형·정체성·성격의 근거로 쓰지 않는다.

blocked 호출은 pixels가 없는 시도로 기록하고 픽셀 품질 점수에 넣지 않는다. 데이터 audit·index·pack 통과와 기술적 픽셀 통과, 사용자 수용은 별도 상태다. 이번 요청은 연구와 계획이므로 이미지 생성·픽셀 성공 판정은 수행하지 않았다.

최종 구현 산출물은 변경된 owner/candidate 목록, 각 원 표현의 보존·보류 장부, actual input hashes, 실행된 fixture 결과, holdout A/B pack 비교, 수행한 경우 픽셀 결과다. 실패한 묶음은 해당 연구 범위의 데이터·코드·파생 인덱스 변경만 함께 되돌리고 기존 unrelated 변경은 보존한다. 보류 78개 표현과 복수 효과 후보를 무검증 상태로 포함시키지 않아야 반영을 완료했다고 판단할 수 있다.

현재 연구 패키지를 재구성·검증하는 명령은 아래와 같다. 기본 모드는 충돌 발생 전 성공한 live 검증에서 보존한 참조 목록을 사용한다. 이는 계획 회귀·팩·이미지를 실행하거나 최신 runtime 입력을 통과시키는 명령이 아니다.

```sh
.venv/bin/python docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/build_research_package.py
```

기존 충돌이 해소되고 구현 기준선을 고정한 후에는 같은 명령에 `--reference-mode live`를 붙여 최신 병합 로더와 실제 슬롯에서 참조를 다시 확인한다. live 실패를 기록 모드 PASS로 대체해 운영 반영 가능하다고 판정하지 않는다.
