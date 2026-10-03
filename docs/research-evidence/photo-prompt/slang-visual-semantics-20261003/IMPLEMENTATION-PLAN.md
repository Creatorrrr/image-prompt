# 시각 의미·후보 데이터 반영 계획

기준일: 2026-10-03  
설계 입력: [연구 보고서](RESEARCH.md), [철자별 처분](TERM-DECISIONS.json), [현재 데이터 스냅샷](CURRENT-DATA-AUDIT.json)  
실행 상태: 계획만 작성. 운영 데이터·인덱스·후보팩은 이 연구에서 변경하지 않았다.

## 1. 반영할 결과를 먼저 정의하기

이번 보강이 해결해야 할 문제는 다음이다.

- 같은 표정 이름이 요청과 다른 입·혀·눈 변형을 강제하는 문제를 줄인다.
- 두 손·얼굴·다리·피부 문양의 구성 요소가 맞아도 소유·지지·동시성이 틀리는 결과를 검출한다.
- 부위 명칭이 크기·노출로, 평가어가 실제 욕망·동의로, 불룩한 복부가 임신 판정으로 확대되는 것을 막는다.
- 일반어·다의어·약어가 의도와 다른 뜻의 필수 의무로 활성화되는 것을 막는다.
- 기존 의미와 ID를 보존하면서 부족한 관찰 원자와 관계만 보강한다.

234개 표기를 그대로 alias에 넣는 방식은 채택하지 않는다. 28개 초안 역시 모두 실행 가능한 runtime 항목이 아니다. 6개 명시 보류를 제외한 22개도 owner·뜻·scope 검토가 끝나야 반영할 수 있다.

## 2. 연구 자료에서 authored 데이터로 가는 승격 단위

한 단어의 승격 기록에는 아래 정보를 포함한다.

| 필드 | 기록할 내용 |
|---|---|
| 입력 표기·뜻 | 원 대화 ST/SR ID, 선택한 뜻, 언어, 문맥 |
| 출처 | URL·확인일·직접 확인 표기·내용 범위·한계 |
| 의미를 보존하는 방식 | 원래 사건·평가·역할의 뜻과 관찰 외형의 경계 |
| 기존 owner | profile/candidate ID와 실제 파일 |
| 구성 원자 | U ID와 필요한 가시적 구성 |
| 관계 | 같은 인물·두 대상·지지·접촉·위치·동시성·시간 순서 |
| 활성화 조건 | adult context, user definition, 포함/배제, exact 문맥 |
| 검색 권한 | exact 필수 가능 여부와 BM25F/embedding advisory 구분 |
| 효과 | 실제 core target, dimension, property |
| 잠금·배제 | 부모/자식 경로 충돌, 인물 수·의복·프레임·사건 |
| 결과 | reuse / add / revise / hold / drop와 이유 |
| 검증 | 구조·회귀·팩·픽셀 결과 각각 별도 |

보고서의 U/SV ID는 연구 ID다. 실제 active ID를 미리 부여해 배포된 것처럼 보이지 않게 한다. 기존 owner가 있는 경우 먼저 재사용 또는 owner 수정으로 처리한다. **existing_slot_context_extensions는 paraphrases와 contexts만 변경할 수 있다.** 이를 이용해 기존 형상·효과·guard를 바꾸지 않는다. 의미 변경이 필요한 항목은 별도의 authored 수정과 영향 회귀를 갖는다.

187개 개별 어휘 근거 미확인 항목은 [LEXICAL-BACKLOG.json](LEXICAL-BACKLOG.json)에 있다. 이 숫자가 모두 시각 데이터의 누락 개수라는 뜻은 아니다. 상당수는 부위 별명·행위·평가·역할·축약형으로, 외형 후보보다 어휘·문맥 검증이 먼저다.

### 근거를 채택하는 조건

직접 사전·원어 작성자의 용례를 우선 사용한다. 기관 사전의 명확한 뜻은 그 뜻의 근거로 쓰고, 소규모 커뮤니티의 일반화 가능한지 불확실한 항목은 독립적인 용례를 추가 확인한다. 같은 사전의 미러 두 개는 독립 출처로 세지 않는다.

철자마다 직접 근거가 있는지, 음차·번역·복수형·축약형의 매핑인지 구분한다. 원어 출처가 있다고 한국어 exact 별칭이 자동 검증된 것은 아니다. 접근 실패는 뜻이 없다는 증거가 아니며, 새 exact 활성화 근거도 아니다. 예문·빈도·기원·형태의 일반화는 각각 별도 근거가 필요하다.

## 3. P0: 공유 checkout 기준과 기존 표정 계약 정리

### P0-A. 실행 기준 재확인

이번 기준 진단은 HEAD `900848816f88a494e5bf16ea475a25074d584911`과 registry hash `e536af9904e7da752552ddbee04b590be3ebbb9a8803b640510f1f4c4e97d2d8`의 1,510 프로필·9,703 후보를 기록했다. 이후 같은 checkout에서 다른 통합 파일 변경이 관찰됐다. 옛 연구의 병합 충돌 상태를 현재 상태라고 추정하지 않는다. 기준 진단에서는 loader가 성공했다.

실제 반영 직전에 다음을 새 증거 폴더에 기록한다.

1. HEAD·branch·git status·대상 파일 SHA-256과 현재 loader 결과.
2. 현재 등록된 extension·profile ID·candidate ID·slot policy.
3. 이 연구 owner와 최신 데이터의 충돌·중복·변경 목록.
4. authored 데이터와 derived index가 일치하는지.
5. 기존 미커밋 변경의 소유와 범위. 본 연구와 무관한 변경을 덮어쓰거나 삭제하지 않음.

기준 감사 파일을 덮어써서 최초와 최종 상태를 섞지 않는다. 이번 파일 해시 수집은 객체·진단 read 뒤에 수행됐으므로 원자적인 한 시점의 snapshot이라는 보장은 없다. 다음 구현 receipt는 loader·진단 전후의 해시를 비교해 동시 변경 여부를 확인한다. 새 receipt를 남긴 뒤 후보 참조를 다시 검증한다. 다른 통합 중인 derived index를 중간 상태에서 재생성하지 않는다.

산출물: 구현 전 receipt, owner 대조표, 변경할 항목의 최종 disposition ledger. 이 단계의 loader 성공도 새 연구 데이터의 채택이나 픽셀 성공은 아니다.

### P0-B. 아헤가오의 범위 수정

대상 파일:

- [photo_prompt_visual_obligations.json](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json): `composite_overwhelmed_expression`.
- [photo_prompt_visual_obligations_acting_expression.json](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_acting_expression.json)와 [acting 후보](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_acting_expression_extension.json): 기존 얼굴 원자 대조.
- [pose 후보](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json): `pv_half_lidded / pv_parted_lips`.
- [neutral expression 프로필](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_neutral_expression.json): 입술 상태·평가의 경계 대조.

검토 항목: definition, paraphrases, component groups, minimum groups, required_evidence_fields, render_gates, reject_substitutes, claim limits, concept 후보와 실제 effect. 이름만 바꾸고 필수 gate가 여전히 같은 좁은 변형을 강제하는 불완전한 수정은 피한다.

설계 선택:

- **좁은 변형 보존**: 현재 형태를 명시적인 변형으로 남기고 넓은 이름의 적용 조건을 분리한다.
- **owner 내부 변형 선택**: 같은 owner에서 코어가 지정한 큰/작은 개구·눈 배치를 선택하고 그 변형의 필수 gate만 적용한다.

선택 기준은 기존 호출자의 요구·호환성·중복 활성화 여부다. 두 설계 모두 원래 장르·사건 의미를 일반 표정과 완전 동의어로 지우지 않는다. 현재 small-O/혀끝 변형을 원하는 요청도 보존한다.

최소 회귀: RG001–RG016의 relevant cases, 일반적인 멍한 얼굴의 오활성화, user-defined geometry 우선, 배제·성인 적용 조건, 큰 개구를 작은 O자로 바꾸지 않음. source row 진단의 한국어 부정 문장과 정규화된 excluded 입력을 혼동하지 않는다.

완료 조건: 한 이름이 특정 변형을 무조건 강제하지 않으며, 명시한 원래 형태·사건·배제를 잃지 않는다. 기존 owner 참조와 active ID 호환성을 확인한다.

## 4. P1: 기존 후보 재사용과 부족한 형태 원자

### P1-A. 얼굴 원자

| 초안 | 처리 | 우선 대상 |
|---|---|---|
| SV01–03 | 상방·안쪽·좌우 동공 배치의 owner 검토 후 원자 작성 | acting/neutral expression |
| SV04 | pv_half_lidded 재사용 | pose vocabulary 후보 |
| SV05 | ae_deadpan_form 전체 뜻이 맞을 때만 재사용 | acting expression |
| SV06–07 | pv_parted_lips / ae_slack_jaw 재사용 | pose/acting |
| SV08 | 입술 경계를 넘는 혀의 위치·범위 원자 검토 | 기존 composite owner와 대조 |
| SV09 | 원인이 지정되지 않은 볼 색 표면 단위 검토 | skin_condition 및 appearance scope |

재사용에는 실제 같은 의미라는 조건이 붙는다. 예를 들어 deadpan 후보는 눈썹만 바꾸는 후보가 아니므로 입까지 고정하는 효과가 코어에 맞지 않으면 적용하지 않는다. 기존 broad `face.expression` 효과를 임의로 더 좁은 eye-only 효과로 표기하지 않는다.

볼 색은 조명·화장·생리 원인과 분리한다. 새 surface 후보의 `face` 효과는 보수적인 부모 경로다. 세부 경로를 쓰려면 코어·producer·auditor의 실제 binding이 일치하는지 확인한 뒤 정의한다.

추천 첫 배치: 기존 항목 재사용·문맥 보강을 먼저 반영하고, 새로운 원자는 작은 3–5개 단위로 회귀한다. batch 크기는 작업 제안이며 확정 구현 수가 아니다.

### P1-B. 양손과 얼굴의 결합

SV10은 `pv_double_v` 재사용이다. 양손의 V와 손목·팔 소유를 이미 정의하므로 복제하지 않는다.

SV11은 현재 `expression` 슬롯 범위를 넘어서 보류했다. 현행 contract가 지원하는 방식 안에서 기존 얼굴 owner와 양손 owner를 같은 target·동시 관계로 연결할 수 있는지 먼저 확인한다. 필요하면 결합 프로필을 검토하되 원자 owner의 의미를 중복 정의하지 않는다. expression 슬롯에 pose 효과를 숨기거나 슬롯 정책을 광범위하게 열지 않는다.

완료 조건: 한 손 V·두 인물 한 손씩·추가 팔·얼굴 가림을 실패 또는 UNOBSERVABLE로 구분한다. 사용한 대상 수·옷·프레임은 코어에 따른다.

### P1-C. 하트눈의 매체 분리

SV12는 코어가 이미 허용한 매체에서 동공 영역의 문양을 검토한다. SV13은 눈을 대신하는 기호가 style까지 영향을 줄 수 있어 보류했다. SV14는 반사·렌즈·후가공 carrier가 확정되지 않아 보류했다.

후보 파일은 실제로 사용되는 owner를 대조한 뒤 정한다. 단순히 neutral expression 연구에서 나온 용어라고 모두 neutral 파일에 넣지 않는다. 필요하다면 appearance 중심의 작은 extension을 등록하되, 그 전에 기존 eye_detail·editing·character-moe 데이터에서 중복을 확인한다.

완료 조건: 한쪽/양쪽, 동공/눈 전체/반사광의 차이, 그래픽/실사의 잠금, 떠 있는 하트·목걸이의 대체 실패가 검증된다.

### P1-D. 다리·전신 지지 관계

대상:

- [pose vocabulary 프로필](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_pose_vocabulary.json)
- [pose vocabulary 후보](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json)
- 기존 pose 연구의 보류 disposition

SV15는 착좌한 무릎 간격의 새 관계 검토, SV16은 `pv_wide_stance` 재사용, SV17은 M형 변형 검토, SV18은 지지 owner와 팔다리 벌림의 결합, SV28은 `pv_chair_straddle`의 조건부 재사용이다.

M字開脚 출처는 최소 형태만 확인하므로 세부 support variant를 어휘의 보편 정의로 만들지 않는다. 장면 코어가 선택한 좌면·바닥·발 상태·시점에 맞춘 변형을 작성하고, 불충분한 변형은 보류한다.

완료 조건: 발폭≠무릎폭, 서기≠앉기, M형≠의자 스트래들, 대자≠다리만 벌림이 구분된다. 카메라나 프레임 잠금을 포즈 후보가 바꾸지 않는다.

## 5. P1/P2: 몸·의복·문양 데이터

### 몸 형상

SV19/SV20은 기존 regional soft volume과 abdominal projection을 재사용한다. broad body 효과는 특정 복부·가슴 잠금과 겹치므로 거절되어야 한다. SV21은 `bust_prominence_relation`의 concept를 실제 열린 target/property에 바인딩한 뒤 재사용한다.

부위 명칭의 alias를 모든 큰 형태 후보에 붙이지 않는다. 육덕의 전체 양감, 가슴의 존재감, 부착 폭·볼륨 분포·간격, 복부 돌출은 별개 owner를 유지한다. 보테배의 문맥에 명시된 원인은 보존하면서 형상에서 원인을 새로 추론하지 않는다.

대상 파일:

- [body morphology 프로필](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_body_morphology.json)
- [body morphology 후보](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_body_morphology_extension.json)
- [neutral expression 후보](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_neutral_expression_extension.json)

### 비교·동역학·편집

SV22는 두 인물 target·count·외관 비교의 보류다. `actor_A/B`는 연구용 자리표시자이며 실제 코어 target이 아니다. 기존 두 인물의 ID에 바인딩하고 명시 비교를 지킬 수 있을 때만 별도 검토한다. `bm_breast_asymmetry`는 한 몸의 좌우 관계이므로 재사용하지 않는다.

SV23은 정지 이미지에서 운동을 입증할 수 없어 보류한다. motion 슬롯의 빈 dimension 목록은 wildcard 허가가 아니다. SV25도 단일 이미지의 편집 전후를 만들 후보가 아니므로 보류한다.

SV24는 요청에 명시된 패딩 의복 외곽만 후보화한다. `wardrobe` 효과가 의복의 색·노출·형태 잠금과 겹치면 차단한다. 실제 신체 크기를 바꾸지 않는다. 슴부조작의 어휘 범위는 패딩·외관 변화와 별도의 편집 이력을 나눠 기록한다.

### 피부 문양

SV26/SV27은 skin carrier·배꼽 상대 위치·같은 몸·개별 motif topology의 검토 대상이다. `ctx_c151`은 일반 타투 문맥의 재사용 참고이며 하복부 특수 문양과 자동 동치가 아니다.

처음에는 사용자가 명시한 중립 추상 문양으로 위치·연결·의복 잠금의 픽셀 gate를 검증한다. 장르 이름에서 생식·소유·타락·발광·하트를 자동 추가하지 않는다. 모든 원뜻은 언어층에 남긴다. 실제 사용자 요구가 정책에 의해 처리되지 못하면 해당 호출 결과를 그대로 기록하고 뜻을 바꿔 재호출하는 방식으로 검증하지 않는다.

## 6. P2: 어휘·문맥 보강과 비시각 의미의 보존

우선 묶음은 다음이다.

1. 일반어와 겹치는 부위·음식·통화·팬·도구: melons, buns, booba, booty, bazookas, gooner, doable, dong 등.
2. 철자·축약형의 구별: 아헤·AWP·암타·이키顔, 한국어/일본어 표기, ㄱㄴ·ㅇㅆ 등의 약어.
3. 평가어·관심 목적: 꼴리다·임최몸·bimbo/himbo·MILF/DILF·thirst trap.
4. 서사·역할·변화: NTR/네토리, 타락, 도구화·소유·생식 역할의 주장.
5. 부위·행위·음성·시점 어휘: 정확한 뜻은 연구층에 보존하고 시각 후보의 근거와 구분.

출처를 확인한 철자만 검증 상태를 올린다. 프레임워크 출처가 관련되어 있다고 같은 분류의 20개 표기까지 사전 검증 완료로 처리하지 않는다. 원문 역할어를 일반 body shape에 넣지도 않고, 원문 뜻을 삭제한 순화어를 동치 alias로 넣지도 않는다.

대상은 request interpretation·언어 문맥·배제·claimed role의 계약을 검토한 뒤 정한다. runtime에 연구용 source metadata를 복사하지 않는다. 활성화 alias와 검색 paraphrase에는 실제 시각 뜻에 동치인 범위만 넣고, 설명·혼동 경계·holdout은 인덱스 밖 근거 원장에 보관한다.

완료 조건: 각 승격 표기는 출처·문맥·보존할 뜻·금지 추론·현재 owner가 연결되며, 부위·역할·사건의 뜻을 외모 후보로 일괄 치환하지 않는다.

## 7. 인덱스와 runtime 검증 순서

순서는 authored 수정 → focused validation → derived index 재생성 → frozen-core 팩 비교다. derived index를 수동 편집해 authored 충돌을 가리지 않는다. 변경된 텍스트의 벡터와 hash는 새로 계산하며 호환되는 벡터만 재사용한다.

실행 전 실제 scripts의 옵션과 최신 checkout을 확인한다. 아래는 **이 연구에서 실행하지 않은 후속 검증 절차**다.

```sh
.venv/bin/python -m unittest tests.test_photo_pose_vocabulary_semantics tests.test_photo_body_morphology_semantics tests.test_photo_acting_expression_data tests.test_photo_neutral_expression_alternatives tests.test_photo_candidate_semantics tests.test_photo_visual_profile_retrieval tests.test_photo_core_retrieval tests.test_photo_authorial_core_v6
```

변경한 owner에 해당하는 모듈부터 실행하고, 모두 통과한 뒤 새 이슈가 없다면 반복 확대하지 않는다. source-only JSON 연구 파일의 구조 검증과 실제 구현의 단위·계약 회귀를 구분한다.

인덱스 경로:

- [build_visual_profile_index.py](../../../../skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py): registry·output·cache-index·check 옵션.
- [build_semantic_index.py](../../../../skills/photo-prompt-image-generator/scripts/build_semantic_index.py): tags·output·provider/model·checkpoint·dry-run 옵션.
- [prompt_generator.py](../../../../skills/photo-prompt-image-generator/scripts/prompt_generator.py): 실제 extension 등록과 runtime loader.
- [photo_candidate_semantics.py](../../../../skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py): 후보 scope·context 확장.
- [photo_contracts.py](../../../../skills/photo-prompt-image-generator/scripts/photo_contracts.py): 부모/자식 property 잠금.

외부 임베딩 호출과 비용은 실제 구현 배치에서 확인한다. 연구 산출물 작성만으로 인덱스 재생성 호출을 시작하지 않는다. 서비스 credentials나 벡터 값을 증거 문서에 노출하지 않는다.

## 8. frozen-core 후보팩 비교

동일한 정규화 요청·user definitions·frozen authorial core·intent lock·creative controls·seed·provider·모델 설정을 보존한다. 프로젝트의 기존 기본값을 이 연구로 변경하지 않는다. 비성적 표정·자세 연구의 픽셀 비교는 해당 연구 요청의 명시 조건을 사용한다.

각 케이스에서 기록한다.

- request envelope·core·controls의 hash와 사용한 후보 corpus/index hash.
- 필요한 profile과 실제 source·match_basis·hard/advisory 권한.
- 후보 노출 목록·순위·중복과 실제 채택/거절 이유.
- target/property·dimension·count·의복·카메라·배제 유지 여부.
- core4/support2/total64 예산.
- 완성 prompt와 audit 결과. 모두 거절한 팩도 정당한 결과인지.
- native pixel 평가가 필요한 경우 그 결과를 별도 연결.

처음에는 데이터 의미·scope를 검증하는 좁은 케이스를 사용하고, 이후 표정+손+문양처럼 관계가 결합된 코어를 평가한다. 전후 성능을 비교할 때 각각 다른 코어를 작성하지 않는다.

추천 측정값은 mandatory meaning preservation, wrong-sense hard activation, wrong-owner relation, lock violation, eligible-candidate exposure, unjustified adoption, budget violation이다. 평가 표본·원래 실패·개선·악화의 원자료를 함께 남긴다. 이 연구에는 그 성능 수치가 없다.

## 9. 픽셀 검증과 사용자 수용

92개 holdout에서 native_pixels 층인 사례를 먼저 고른다. 어휘 설명 사례를 이미지 생성 성공률의 분모에 넣지 않는다. 평가어·역할어의 핵심 검증은 원뜻 보존과 무근거 외형 추가 방지다.

픽셀 checklist:

- 얼굴: 눈꺼풀·동공·고개 축, 작은 틈/큰 개구, 입술 경계와 혀.
- 손: 두 개의 V, 손가락 수, 손목·팔 연결, 같은 인물, 손바닥 방향.
- 눈 문양: 위치·좌우 수·carrier·매체.
- 자세: 골반·지지면·관절 연결·무릎/발 간격·시점.
- 몸: 지정 영역·인접 윤곽·의복/원근과 실제 형태의 구분.
- 문양: 같은 피부면·배꼽 상대 위치·지정 topology·가림.

원본 픽셀에서 all-of, partial_is_fail을 적용한다. 필수 요소가 안 보이면 UNOBSERVABLE이며 이미지 품질 성공으로 합산하지 않는다. generation error·moderation block은 호출 상태로 기록하며 시각 품질 FAIL이나 의미 성공으로 대체하지 않는다. 기술 gate 통과와 사용자의 선택은 별도다.

이번에는 서비스 호출·이미지·사용자 수용 결과가 없으므로 모든 해당 상태를 NOT_GENERATED_OR_EVALUATED로 유지한다.

## 10. 배치별 완료·보류 기준

| 배치 | 완료 산출물 | 다음 단계에 넘기는 조건 |
|---|---|---|
| 0: 기준 정리 | 최신 receipt, owner 대조, 변경 ledger | 현재 authored/index loader 일치 |
| 1: 표정 범위 | 이름/변형 결정, 필요한 원자, 해당 회귀 | 큰/작은 입·눈·배제·기존 변형 보존 |
| 2: 손·자세 | 기존 reuse와 부족한 관계 | 동일 소유·지지·가시성·잠금 검증 |
| 3: 눈·몸·문양 | carrier·regional effect·명시 비교 | count/medium/body/wardrobe 잠금 검증 |
| 4: 언어 문맥 | 승격 철자의 출처·뜻·다의성 원장 | source 없는 group-wide alias 없음 |
| 5: 통합 평가 | 인덱스·동일 코어 팩·필요한 픽셀 결과 | 근거층별 PASS/FAIL/UNOBSERVABLE/보류 |
| 6: 채택 | 변경별 disposition과 실제 사용자 판단 | 기술 성공과 사용자 수용 별도 기록 |

명시 보류 6개: SV11(얼굴+손 scope), SV13(눈 기호+style), SV14(carrier), SV22(두 target 비교), SV23(시간 증거), SV25(편집 전후). 보류가 해제되더라도 기존 slot 정책을 포괄적으로 열어 문제를 덮지 않는다.

마감 기준은 alias 수나 후보 수 증가가 아니다. 필요한 뜻을 잃지 않고, 요구하지 않은 형상·사건·사람을 추가하지 않으며, 전체 구성·소유·잠금을 검증할 수 있는 상태다.
