# 시각 의미 데이터·후보팩 반영 계획

2026-10-05 KST · 계획 완료 · 아래 작성 데이터 수정·인덱스 갱신·회귀·이미지 생성은 아직 실행하지 않음

반영 순서는 **현재 원자의 정확한 설명 보강 → 복합 표정·접촉 관계 → 소유가 다른 변형 → 매체·대비 맥락 → 후보팩과 이미지 검증**으로 둔다. 140개 표제어를 140개의 새로운 활성 후보나 hard profile로 복제하지 않는다. 구현량은 기존 후보의 실제 동등성 심사 후 확정한다.

## 1. 목표와 완료 기준

목표는 자연어 요청의 표현과 문맥을 보존하면서, 후보팩이 실제 보여야 하는 형태·관계를 제공하도록 작성 데이터를 강화하는 것이다. 각 배치의 완료 여부는 다음 증거로 판단한다.

|단계|필요한 증거|통과로 대체할 수 없는 것|
|---|---|---|
|작성 데이터|실제 owner·slot·ID, 긍정 설명, 소유·관계, 전체 효과, 유지할 guard|리서치 JSON 구조 PASS|
|검색 인덱스|현재 작성 바이트와 맞는 의미/프로필 인덱스, 동일 모델 메타데이터|과거 인덱스 파일의 존재|
|요청 해석|후보 접근 전 고정한 요청·core, 정의·부정·매체·인원·속성 고정|후보 설명을 복사해 만든 core|
|후보팩|해당 요청에 실제 노출된 목표 ID와 부적합 처리 이유|저장소에서 후보가 검색됨|
|선택|실제 채택·거절 ID와 묶음 성분·효과의 추적|후보가 pack에 들어 있음|
|프롬프트|도구에 실제 보낸 문장·인자·참조와 해시|제안 프롬프트·내부 audit PASS|
|원본 이미지|필수 성분·관계의 all-of 결과, 가림 별도 기록|몇 가지 비슷한 분위기·색·외형|
|귀여움·대비 전달|사람의 비교 평가, 필요한 두 축을 각각 인식|기하·접촉만 통과|
|사용자 수락|실제 결과에 대한 수락|앞 단계의 자동 PASS|

## 2. 먼저 고정할 입력과 범위

구현 시작 시 현재 checkout·HEAD·작성 소스·코드의 해시를 다시 기록한다. 이번 `CHECKOUT-SNAPSHOT.json`은 조사 시점의 기준이지 미래 구현의 최신 상태가 아니다. 현재 다른 작업의 변경이 많은 상태이므로, 그 변경을 보존하고 의도한 작성 레코드만 심사·반영할 수 있는 checkout을 사용한다. 조사 결과만으로 기존 변경을 함께 커밋하거나 게시하지 않는다.

원래 140개 목록과 `ANNOTATIONS.tsv`, 출처 확인 상태를 증거로 유지한다. `SEMANTIC-UNITS.json`·`CANDIDATE-DRAFTS.json`은 연구용 제안 스키마다. 런타임 자산에 파일째 복사하거나 로더에 연결하지 않는다.

별도의 검증 요청과 의미 축은 **후보 설명을 보기 전에** 원 요청·공개 1차 의미에서 작성·고정한다. 이번 420개 회귀와 18개 이미지 seed는 연구 주석에서 파생되므로, 독립적인 holdout이라고 부르지 않는다. 작성 배치를 보기 전에 마련한 별도 문장·동형 오인·정의 변경·속성 고정 사례가 필요하다.

## 3. 파일별 반영 배치

표의 경로는 `skills/photo-prompt-image-generator/assets/` 아래다. `RUNTIME-MAPPING.json`은 140개 모두의 파일·슬롯과 효과 제안을 제공한다. 확인된 기존 파일·슬롯과 아직 적합성을 심사하지 않은 속성 경로를 구별한다.

|순서·배치|대상 번호·형태|작성 owner|실제 작업|배치 종료 조건|
|---|---|---|---|---|
|A. 기존 원자·오인 경계|#11–34, #40·44·48·57·63–68·74·82·115·118 등|`photo_prompt_pose_vocabulary_extension.json`, `photo_prompt_acting_expression_extension.json`, `photo_prompt_subculture_appearance_extension.json`|기존 ID·guard를 유지. 동일 형태에만 검토한 paraphrase·context 추가. 반개안/지토메·미소 후보의 대안 구분|의미·owner·효과를 넓히지 않은 재사용, 새 별칭의 동형 오인·부정 회귀 통과|
|B. 복합 표정|웃음 참기·양안 미소·코 찡긋 미소·강아지 눈·작은 O·눈물 미소|acting expression owner와 `photo_prompt_visual_obligations_acting_expression.json`|눈·입·볼·머리·시선의 기존 원자를 명시적 관계로 조합. 부족한 국소 형태만 새 원자|같은 얼굴 소유, 눈·입의 동시 상태, 감정 사실을 덧붙이지 않는 조건|
|C. 손가락·손목·얼굴 접점|#35–56의 새 변형과 #129|pose owner와 `photo_prompt_visual_obligations_pose_vocabulary.json`|엄지검지 교차·양손하트 변형·볼하트·검지 끝 접촉·틈새 눈·손키스 위상을 각각 분리|손가락 연결·접점·좌우·남은 가시 증거와 명명 변형 근거|
|D. 몸의 지지·상호작용|#58–90, #130·132|pose owner, 필요한 기존 prop owner|몸통·머리·시선 독립 축, 발 지지, 손-물체와 A-B 소유 관계를 묶음으로 작성|인원·물체·동작·관계 고정 통과. 허공 접촉·잘못된 대상·가려진 접점 미통과|
|E. 카메라·빛|#91–110|`photo_prompt_portrait_composition_extension.json`, `photo_prompt_lighting_extension.json` 및 해당 프로필 owner|샷 범위·카메라 높이·방향·몸 회전·투영·초점·반사·톤을 분리. 기존 component 재사용부터|동형 단어가 다른 해부·행동·렌즈 후보를 harden하지 않음. 필수 손·눈·접점의 크롭 유지|
|F. 조형·의복·기호|#3·4, #111–124|body morphology, textile surface, clothing structure, accessory structure, subculture appearance, color relations, motion graphics owners|비례·섬유·덮임·부착·색 관계·도식 기호를 실제 소유와 매체로 분리|실사·그림·인쇄·장식·메이크업·실제 피부의 구별, 나이·체형·종족 고정|
|G. 맥락·대비|#1–10, #125–128, #133–140|`photo_prompt_character_moe_extension.json`의 일반 관계 구조; 필요한 선택형 스타일 owner|표면 태도·대상 행동·결과, 관능/귀여움, 어두운 상징/밝은 조형을 독립 축으로 작성|고정 의상·소품을 정의로 만들지 않음. 두 대비 층과 사용자 정의 보존|

시각 프로필은 현재 의미가 동등한 프로필부터 재사용한다. 각 표제어에 무조건 새 hard profile을 만들지 않는다. 신규 프로필이 필요하면 해당 extension의 실제 관찰 성분과 좁은 활성 맥락을 연결하고, 외부 profile 파일·maintenance 기록을 현재 계약에 맞춰 작성한다.

별도의 `photo_prompt_cute_contrast_extension.json`은 **G 배치에서 기존 owner로 담기 어려운 선택형 스타일 조합이 남을 때만 검토할 새 파일**이다. 연구 매핑에는 제안 owner로 표시되어 있으며 현재 존재하지 않는다. 만들기로 결정하면 일반 로더의 `RESEARCH_EXTENSION_FILENAMES`, `candidate_semantic_policy.required_extensions`, 필요할 경우 `VISUAL_OBLIGATION_EXTENSION_FILENAMES`에 등록한다. `귀여움`·`야미카와이`를 감지하는 새 Python 분기나 전용 프롬프트 라우터를 추가하지 않는다.

## 4. 재사용·조합·분리의 의사 결정

1. **완전히 같은 형태·owner·guard**: ID를 유지하고 검토한 표현·해석 context만 보강한다. `existing_slot_context_extensions`는 의미·효과·guard 교체 도구가 아니다.
2. **동일 원자의 새로운 조합**: component IDs를 재사용하고 동일 얼굴·손·대상에 대한 관계를 authored bundle로 작성한다. 겹치는 대안은 모두 필수 구성원으로 넣지 않는다.
3. **일부 성분만 지원**: `pv_parted_lips`가 O형 곡률을 보장하지 않는 것처럼 부족한 형태·관계를 별도 작성한다. 부분 재사용을 전체 지원으로 기록하지 않는다.
4. **다른 접점·좌우·소유자·재질·매체**: 별도 변형 후보 또는 explicit axis로 나눈다. 자기 소매를 잡는 손의 별칭에 상대 소매 당기기를 덧붙이지 않는다.
5. **넓은 문화·평가·연출 개념**: 고정 포즈가 아닌 선택형 구현 패턴으로 남긴다. 특정 파스텔·인형·큰 눈·리본을 모든 용례에 강제하지 않는다.

현재 수동 대조의 경로는 맥락 패턴 22개, 대안 재사용 4개, 경계 심사가 필요한 재사용 25개, 기존 원자 조합 11개, 일부 성분 재사용 22개, 동등 후보 재탐색 또는 새 변형 검토 56개다. 마지막 56개는 **현재 데이터에 의미가 없다는 판정이 아니다**. 자세한 기존 동등 후보 검색을 구현 직전에 다시 진행한다.

## 5. 실제 후보·묶음에 작성할 내용

각 runtime candidate는 현재 스키마에 맞는 ID·ko/en·검토한 긍정 paraphrase, 적용 guard, 관찰 원자, 관계, 모든 `affected_dimensions`·`affected_properties`를 가져야 한다. 연구 JSON의 임의 필드를 runtime extension에 추가하지 않는다.

예를 들어 상대 소매 당기기 변형은 다음 의미를 선언한다.

```text
actor A의 손가락 → actor B의 소매 끝 → B의 팔로 이어지는 의복
손가락 집기와 천 경계의 실제 접점
행동·자세·관계 효과 및 명시된 의복/물체 효과 전부 검토
기존 core에 선언된 A·B와 소매에 결합; 인원·새 사건을 임의 추가하지 않음
```

꽃받침의 `pv_flower_chin`처럼 이미 완결된 원자는 그대로 재사용한다. `pv_mug_grip`·`pv_hem_hold`처럼 `pose`와 `relationship`을 함께 선언한 기존 후보는 그 전체 효과를 보존한다. 슬롯 이름이 `contact_point`라는 이유로 관계 효과를 삭제하거나, 다른 차원으로 옮겨 잠금을 우회하지 않는다. 새로운 인물·소품이 필요한 경우 `count`·`subject`·`event` 등의 고정도 확인한다.

후보의 긍정 검색 문장에는 관찰 의미만 넣는다. 출처·주장 한계·금지 대조·프로세스 상태·ID·출처 URL은 별도 maintenance 근거에 남긴다. 단어가 대조 목록에서 발견됐다는 이유로 긍정 검색되면 실패다.

실제 사람·동물·물체·도식 캐릭터의 비례와 재질은 typed `subject_category` 및 현재 적용 guard로 구분한다. `for_any: human`인 body 원자를 인형·동물용으로 무조건 재사용하지 않는다. 비인간 형상에 현재 owner가 맞지 않으면 해당 domain의 별도 후보를 심사한다. 연구의 `declared_object` 속성 제안이 기존 인체 스키마와 이미 호환된다는 뜻은 아니다.

공개 pack은 현재 V6의 요청별 optional 구조를 유지한다. 배열 순서는 의미·우선순위가 아니므로 회귀는 후보·묶음의 **안정된 ID**로 검사한다. 선택 시 묶음 성분·관계를 모두 보존하는 의무와, 원래 요청에서 활성화된 hard profile을 구분한다. bundle 선택만으로 연결된 hard profile이 활성화됐다고 간주하지 않는다.

## 6. 승격 전 해결할 항목

|항목|추가 확인과 결정|
|---|---|
|엄지검지 손하트|Unicode의 다중 용례와 실제 손 방향 대조. 기존 `pv_finger_heart` 보류 disposition·maintenance 근거·회귀 기대를 함께 갱신하거나 새 좁은 ID로 분리|
|양손·볼·반쪽 하트|손목·손끝 접점의 변형을 몇 개의 좁은 topology로 채택할지 결정. 모든 손하트에 한 접점을 강제하지 않음|
|테헤페로|원저자 원문 또는 직접 제작한 신뢰할 수 있는 실제 예시에서 혀끝·미소·윙크·손 변형 대조. 접근 실패 동안 자동 문화 alias 승격 보류|
|갸루피스|직접 촬영 사례의 원본 사진에서 V·손면·손목·전방 방향 대조. 의복 갸루와도 분리|
|일반 캐치라이트|젖은 눈·고정된 수직 두 광원·특정 형상 없는 일반 반사의 후보를 구분. 기존 좁은 ID를 무조건 확장하지 않음|
|소매로 가린 손|겉의 소매 연속성과 위치만 의무로 삼을지, 보이는 손가락 접점을 따로 요청할지 결정|
|성인 매력|기존 `ae_coquettish_variant`의 adult/flirt guard 유지. 중립적인 미소·눈맞춤·애교 전체를 성인 연출로 한정하지 않음|
|야미·구로의 사건/장식|단어의 전체 범위는 보존하되 구체 요청의 매체·소유·사건을 선언. 일괄 순화나 일괄 현실 손상 변환을 하지 않음|
|갭모에 등 개념|기존 family와 현대 concept_profiles의 차이 대조. 일반 actor-target-action-consequence 구조에서 표현할 수 있는지 먼저 확인|

이 조건은 전체 연구의 중단 사유가 아니다. 근거가 충분한 원자·설명·관계 배치는 먼저 반영할 수 있고, 특정 명명 변형의 hard activation만 별도로 보류한다.

## 7. 회귀와 인덱스 검증

`REGRESSION-PROPOSALS.json`의 420건은 각 항목에 긍정 묘사, 틀린 형태·소유의 대조, 정의·부정·매체·속성 고정/가림 사례를 붙인 제안이다. 실제 작성 ID·요청 스키마·기대 결과로 변환해 실행한다. 같은 annotation에서 만든 긍정 문장을 그대로 검색하는 성공만으로 일반화를 주장하지 않는다.

|배치|관련된 현재 테스트 파일|
|---|---|
|표정·입·눈|`tests/test_photo_acting_expression_data.py`, `tests/test_photo_pose_vocabulary_semantics.py`|
|후보 작성·잠금·선택|`tests/test_photo_candidate_semantics.py`, `tests/test_photo_control_span_ownership.py`, `tests/test_photo_authorial_core_v6.py`|
|검색과 오인 경계|`tests/test_photo_core_retrieval.py`, `tests/test_photo_visual_profile_retrieval.py`, `tests/test_photo_bm25f_retrieval.py`, `tests/test_photo_positive_retrieval.py`|
|개념·소유·매체|`tests/test_photo_character_response_concepts.py`, `tests/test_photo_object_morphology_ownership.py`, `tests/test_photo_motion_graphics_semantics.py`|
|카메라·조명|`tests/test_photo_portrait_composition_semantics.py`, `tests/test_photo_lighting_visual_semantics.py`, `tests/test_photo_lighting_composition_boundary_data.py`|
|인덱스|`tests/test_photo_semantic_index.py` 및 실제 profile index의 current-source 검사|

작은 배치에서는 변경과 연결된 테스트를 실행하고, 실제 실패·스키마 변경·배치 간 충돌이 생기면 해당 범위를 확장한다. 이 리서치 파일만 검증할 때는 runtime 전체 회귀를 실행할 필요가 없다. 아래는 **구현 후 사용할 명령 예시**다.

```sh
python3 -m unittest discover -s tests -p 'test_photo_acting_expression_data.py'
python3 -m unittest discover -s tests -p 'test_photo_candidate_semantics.py'
python3 -m unittest discover -s tests -p 'test_photo_core_retrieval.py'
python3 -m unittest discover -s tests -p 'test_photo_visual_profile_retrieval.py'
```

작성 데이터를 심사·변환한 뒤 의미 인덱스와 프로필 인덱스를 재생성한다. 병합된 작성 소스를 기준으로 만들고 생성 파일의 충돌에서 한쪽 결과를 선택하지 않는다. 캐시 벡터는 긍정 입력 문자열·provider·model·dimensions가 같을 때만 재사용한다. 이 단계는 필요 시 외부 임베딩 호출을 수반하므로 호출 수·재사용 수를 기록한다.

```sh
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

`--dry-run`은 작성 입력과 계획을 읽는 단계이며 기존 인덱스의 정확성이나 노출을 보장하지 않는다. `--check`도 이미지 품질·사용자 평가를 대신하지 않는다.

## 8. 후보팩 노출·선택의 종료 조건

독립적으로 고정한 요청마다 core→registry→index→pack→선택→실제 프롬프트의 ID·해시를 보존한다. 다음 항목을 분리해 기록한다.

- 기존·새·보강 후보 중 무엇이 실제 pack에 노출됐는지, 부족한 성분은 무엇인지.
- 노출된 후보가 정의·부정·매체·owner·open dimension·속성 고정 때문에 거절됐는지.
- 사용자가 좁게 요청한 형태에서 해당 프로필이 활성화됐는지. 근사 검색이나 넓은 문화 이름만으로 활성화되지 않는지.
- 채택한 묶음의 모든 성분·관계가 실제 프롬프트에 남았는지. 거절된 optional 묶음이 프롬프트에 새로 흘러들지 않는지.

공유 가능한 pack에는 내부 점수·순위·출처 주장 등을 더하지 않는다. 노출/선택이 0이라면 원인을 해결하기 전 데이터가 이미지 개선을 일으켰다는 결론을 내리지 않는다.

## 9. 원본 이미지와 인상 평가

`PIXEL-QUALIFICATION-PLAN.json`에 꽃받침, 엄지검지 손하트, 두 사람 하트, 한쪽 볼, 양안 미소, 코이 시선, 상대 소매, 컵, 한쪽 뒤꿈치, 모에소데, 담요, 탑다운, 보케, 캐치라이트, 성인 매력 대비, 야미, 구로, 갭모에의 18개 사례를 설계했다.

첫 배치는 **18개 요청 × A/B 두 이미지 = 36개 원본 이미지**와 **18개 후보팩 부정 대조**다. A는 반영 전 작성 데이터, B는 반영 후 데이터이며 같은 긍정 요청·core·참조·출력 조건을 사용한다. C는 반영 후 데이터에 별도로 고정한 부정·정의 변경·잠금 요청을 주는 pack 검사이고, 동일 조건의 세 번째 이미지로 점수를 비교하지 않는다. 이번 연구에서 생성·예약하지 않았다.

18개 연구 seed를 독립 core라고 부르지 않는다. 실제 검증 전에 의미 축·소유·성분·평가 해상도를 독립적으로 다시 고정한다. 넓은 관능·귀여움·섬뜩함의 평가를 임의의 한 포즈로 대체하지 않는다. 먼저 각 요청에서 표현하기로 한 실제 자세·행동·모티프를 명시한다.

원본 이미지에서 필수 성분과 관계를 개별 판정하고 전체는 `partial_is_fail`로 계산한다. 가려진 손가락·접점은 `UNOBSERVABLE`이며 통과가 아니다. 단, 요청이 소매 외곽만 요구했다면 처음부터 가린 손가락을 필수 조건으로 삼지 않는다. 그래픽/실물, 투영상 정렬/물리 접촉도 각각 맞는 방식으로 평가한다.

실제 사용한 프롬프트·인자·참조·원본 이미지·작성/인덱스/core 해시·노출/선택 ID를 모두 남긴다. 생성 차단은 형태 실패와 분리해 `BLOCKED_UNSCORED`로 기록한다. 자동으로 더 순한 의미로 바꿔 같은 사례가 통과했다고 기록하지 않는다.

형태 통과 후에는 A/B를 익명으로 비교하며 다음을 따로 묻는 평가표를 사용한다: 귀여움이 읽히는가, 원래 요청을 보존했는가, 해당 대비의 두 축이 각각 읽히는가, 보이지 않는 감정·병력·관계 등의 설정이 불필요하게 추가됐는가. 기하 PASS와 귀여움 PASS, 사용자 수락은 서로 다른 결과로 보고한다.

반복·추가 이미지는 실패 원인이나 미해결 불확실성이 생긴 경우에 한해 설계한다. 한 장의 성공이나 우연한 부분 충족으로 일반화·완료를 주장하지 않는다.

## 10. 최종 반영 보고와 이번 작업의 경계

실제 구현 보고에는 작성 데이터의 변화, 회귀, 인덱스, 후보팩 노출·선택, 실제 프롬프트, 원본 이미지, 인상 평가, 사용자 수락을 각각 기재한다. 적용한 후보·프로필 ID와 남은 명명 변형의 보류 사유를 적고, 관련 없는 기존 변경과 구현 배치를 분리한다.

이번 작업의 완료 범위는 **140개 연구·현재 데이터 대조·파일별 반영안·회귀/이미지 검증 설계·연구 산출물 구조 검증**이다. 런타임 자산·코드·인덱스 반영이나 커밋·게시, 이미지 생성은 이 계획에 포함된 다음 실행 단계이며 이번 작업에서는 수행하지 않았다.
