# 연기·표정 데이터 반영 계획

작성일: 2026-10-03. **이 문서는 구현을 위한 검토 가능한 계획이다. 운영 데이터·manifest·인덱스는 이번 조사에서 수정하지 않았다.**

## 1. 반영 순서와 완료 기준

국소 형태를 먼저 명확하게 만들고, 문맥별 조합을 얹은 뒤 검색과 픽셀을 비교한다. 시간·음성 요구는 해당 매체를 지원하는 후속 작업으로 남긴다. 새 별칭·후보의 숫자를 완료 기준으로 사용하지 않는다.

| 단계 | 산출물 | 완료 조건 | 예상 순서 |
|---|---|---|---|
| P0: 기준 고정·중복 정리 | 최신 원본 목록, ID 대응표, 영향 범위 | 기존 의미·guard 보존, 관련 병합 상태 확인, 혼합 리비전 제거 | 가장 먼저 |
| P1: 국소 형태 | 재사용 11개 검토, 새 형태 후보·프로필 | 가까운 눈·입·손 형태 구분, 소유권·속성 영향·부정문 검증 | 첫 반영 배치 |
| P2: 상황·복합·성인 호감 | 좁은 문맥 변형, optional bundle, 기존 graph 대응 | 문맥 밖 오활성화·배우/사건 발명·잠금 침범 없음 | P1 의미 검증 이후 |
| P3: 코미디·한국어 관용어 | 상황별 예문·반례, 스타일 선택형 | 번역 등가성·literal sense·크롭/시선 보존 검증 | P2와 일부 병행 가능 |
| P4: 시간·음성·방법론 | 시퀀스·음성·준비 메타데이터 설계 | 해당 매체 없으면 미검증 표시; 정지 PASS로 대체 금지 | 별도 지원 범위 확정 후 |

38개 새 후보·11개 프로필·11개 번들은 현재의 **제안 규모**이다. 일부는 검토 후 기존 항목에 합쳐지고, 일부는 분리되거나 삭제될 수 있다. 전체를 한 번에 등록할 필요는 없다. 처음에는 국소 입술·눈썹·손 형태 중 서로 다른 검증 문제를 가진 작은 배치를 선택한다.

## 2. 파일별 변경 위치

저장소 기준 경로는 `/Users/chasoik/Projects/image-prompt`이다. 아래 새 파일명은 제안이며 아직 생성·등록하지 않았다.

| 대상 | 변경 계획 | 범위 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_acting_expression.json` | 11개 프로필 초안 중 검토를 통과한 좁은 형태를 저장 | 기존 `photo-visual-obligation-registry-extension/v1` / relation v1 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_acting_expression_extension.json` | 새 후보·optional 번들과 검토된 context 추가 | 기존 `photo-prompt-research-extension/v1` |
| `photo_prompt_pose_vocabulary_extension.json` | 기본 눈·미소·윙크 후보의 동등한 표현·문맥을 재사용 | 기존 ID·가중치·guard·영향 범위 보존 |
| `photo_prompt_contextual_appeal_extension.json` | `expression.ctx_c126` 등 좁은 상황 항목 재사용 | 집중 중 lip bite를 일반 유혹으로 넓히지 않음 |
| `photo_prompt_tags.json` 및 기존 인물 확장 | `playful_smirk`, `deadpan_kindness`, 로봇 미세표정 등의 뜻 비교 | 광의 개념으로 덮어쓰지 않음 |
| `skills/photo-prompt-image-generator/scripts/prompt_generator.py` | 검토 후 확장 filename manifest에 등록 | 원본 의미가 정리되기 전 등록하지 않음 |
| `skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py` | 기본적으로 변경 불필요 | 기존 authored component 구조로 표현 가능한지 먼저 확인 |
| `skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py` | 기본적으로 변경 불필요 | 지원된 bundle·context·effect 계약을 사용 |
| `skills/photo-prompt-image-generator/references/retrieval-contract.md` | 형태/상황/시간/음성의 구분과 채택 예시 문서화 | 기존 frozen core→pack 순서 보존 |
| `tests/test_photo_acting_expression_data.py` (제안) | 실패 경계·문맥·소유권·잠금 회귀 | 실제 영향과 혼동을 검증; 데이터 행을 그대로 복제하는 테스트 지양 |
| 기존 파생 semantic/profile index | 검토된 원본을 기준으로 재생성 | 직접 패치하거나 다른 리비전의 벡터를 무조건 혼합하지 않음 |

상황 조건은 가능한 한 기존 `for_any` 등 applicability, `coherence_rules.slot_context_rules`, 명시적 효과 선언, 프로필 activation을 활용한다. **`contextual_usage`의 해석 문장 자체는 강제 guard가 아니다.** 필요한 조건을 현재 계약으로 강제할 수 없다면 해당 항목은 연구 데이터 또는 수동 채택 전용으로 남기고, 별도 코드 변경의 필요성을 기록한다. 모르는 guard 필드나 새 슬롯을 임의로 만들지 않는다.

## 3. P0: 최신 기준과 재사용 대응을 고정

1. 작업 트리·HEAD·관련 원본 상태를 기록한다. 이번 조사는 `0adb5f6e...`에 고정되어 있으므로 최신 병합이 완료된 원본으로 다시 좁은 diff를 확인한다.
2. 기존 프로필·후보 ID와 exact alias, positive component text, affected properties, guard를 비교한다. 원본 74개 파일과 새 기준의 SHA-256을 따로 남긴다.
3. 9개 기본 expression 원자, `pv_side_eye`, `playful_smirk`의 재사용 조건을 검토한다. 동등한 뜻이면 `existing_slot_context_extensions`의 paraphrases/contexts 추가를 고려한다. 뜻·소유자·동작·영향이 달라지면 새 후보로 분리한다.
4. `expression.ctx_c126`의 과업 집중 문맥, `micro_precise_microexpression`의 로봇 의미, `deadpan_kindness`의 친절, `bystander_double_take`의 방관자 역할을 보존한다.
5. 원 대화의 368행 모두에 route를 유지한다. metadata-only나 sequence-only도 누락으로 취급하지 않되, 해당 표현을 지원한다고 허위 집계하지 않는다.

P0 완료 자료는 `source manifest + reuse matrix + selected batch IDs + excluded/deferred rationale`이다. 기존 내용을 지우거나 충돌을 편의상 한쪽 선택으로 처리할 필요가 없다.

## 4. P1: 국소 형태를 의미 데이터로 만드는 규칙

각 프로필은 네 가지 질문에 답해야 한다.

| 질문 | 필수 데이터 |
|---|---|
| 이름 없이 무엇이 보여야 하는가? | definition, visual components, 한국어/영어 paraphrase |
| 누구의 어떤 부분이며 어디를 향하는가? | actor binding, 좌우, 눈/머리 방향, 손/입 소유권 |
| 비슷해 보이는 무엇과 다른가? | contrast examples와 reject substitutes |
| 무엇을 보면 통과인가? | 같은 source component에서 나온 prompt evidence와 native pixel gate |

`authored_components`의 각 요소에 `match_terms`, `evidence_field`, `evidence_terms`, `min_content_words`, `instruction`, `render_gate`를 쓴다. semantic discovery, literal prompt evidence, composition instruction, gate가 서로 다른 뜻을 갖지 않도록 같은 요소를 투영한다. 증거 필드는 `_phrase`, gate는 `vo_*`로 작성하고 원본 픽셀 검토를 기본으로 한다.

첫 배치로 권장하는 혼동 쌍은 다음과 같다.

- 입술 누름 ↔ 입술 조임 ↔ 안으로 말기 ↔ 앞으로 오므림.
- 입술 사이 작은 틈 ↔ 턱 하강 ↔ 큰 입 벌림.
- 눈썹 안쪽 상승 ↔ 전체 상승 ↔ 한쪽 상승 ↔ 미간 내림.
- 눈썹 상승 ↔ 위 눈꺼풀 상승, 볼 상승 ↔ 아래 눈꺼풀 상승.
- 고개 방향 ↔ 홍채 방향, 한 눈 닫힘 ↔ 두 눈 닫힘.
- 자기 손이 자기 입을 가림 ↔ 상대 손이 가림 ↔ 손이 볼에 닿음.

11개 프로필은 원어·형태 검토 후 필요하면 분해한다. “눈물 참기”의 모든 실현을 눈물 고임+입술 누름으로 하드 고정하지 않는다. 현재 초안 `ae_profile_held_tears_lips`는 **두 형태가 명시된 좁은 문구**에만 해당한다.

관찰 요소는 얼굴의 기본 형상과 구분한다. 동작 전 프레임을 쓸 수 있으면 동일 배우 중립 비교를 포함하고, 단일 이미지에서 자연 눈썹 높이·주름과 동작을 구분하기 어려우면 불확실하게 평가한다. 코딩 인증이나 근육 힘 측정을 대신했다고 주장하지 않는다.

## 5. P2: 문맥 변형과 번들

32개 감정 묶음은 요청의 의미 축으로 유지하고, 형태는 복수 선택지로 제공한다. 문맥 변형에는 출처에 따른 뜻, 저작한 선택형, 필요한 원문 증거, 금지되는 상황 전환을 함께 둔다.

| 패턴 | 필요한 조건 | 금지되는 자동 변화 |
|---|---|---|
| smug/smirk | 요청된 우위·자만·장난의 뜻 구분 | 비대칭 강제, 장난을 적개심으로 교체 |
| coy/새침 | 요청의 수줍음·꺼림·차가운 태도 구분 | 모든 새침을 성인 유혹으로 교체 |
| sultry/smoldering | weather/fire와 배우 표현의 분리 | 성적 톤 또는 분노 자동 추가 |
| lip bite/wink | 과업·놀이·성인 교류의 문맥 구분 | 노출·접촉·파트너·성적 톤 발명 |
| 울면서 웃음·공손한 분노 | 각 의미가 원문에 있고 선택형이 양립 가능 | 실제 마음·정직성·동의 판정 |
| 재회·안도 뒤 울음 | 사건과 배우 관계가 원문에 있음 | 배경 사건·순서·추가 인물 발명 |

`visual_semantics` bundle은 관련 candidate ID, slot, profile ID, component groups, confusion boundaries, owner relations를 묶는다. bundle은 optional이고, 관련 프로필이 연결됐다는 이유만으로 하드 의무가 되지 않는다.

`affected_dimensions`와 `affected_properties`는 **실제로 바뀌는 것**을 선언한다. 얼굴 후보에 시선 변화가 있으면 eyes.eyeline을, 머리 기울임·돌림이 있으면 pose/head.orientation을 포함한다. 손과 소품은 해당 소유자의 속성을 사용한다. `main_subject`는 초안의 임시 소유자이므로 실제 요청의 배우 ID에 바인딩한다.

현재 graph v2의 surface/affiliation/leak timing 축과 대응할 수 있으면 재사용한다. 감정 누출·underlying affect는 저작한 연기 설정으로 쓰며 이미지에서 실제 숨은 마음을 알아낸 상태로 기록하지 않는다. 전술은 시도와 결과를 분리한다.

문맥 변형을 평가할 때 `contextual_usage` 설명을 읽었다는 사실과 실제 guard가 적용됐다는 사실을 나눈다. 후보 노출만으로 frozen core를 바꾸지 않는다. 전체 후보팩은 한 번에 구성하되 관련 슬롯들의 선택은 optional이고 모두 거절 가능하다.

## 6. P3/P4: 지원할 수 없는 증거를 명시적으로 분리

코미디·한국어 관용어는 같은 단어를 일반 장면, 코미디 장면, literal scene에서 대비한다. Mug는 컵/강도행위/표정 연기를, 동공지진은 당황의 관용어/영상 시선 변화/실제 동공 표현을 구분한다. “영혼 없음”을 임상 상태로, “킹받음”을 고정 악역으로 바꾸지 않는다.

시간 스키마는 이 연구의 제안이며 **현재 runtime에 존재한다고 가정하지 않는다**. 후속 매체가 지원될 때 `actor_id`, `event_reference`, `ordered_frames`, `onset`, `apex`, `offset`, `latency`, `visibility` 등을 정의한다. 정의되지 않은 시간 값이나 측정 단위를 현재 사진 후보에 끼워 넣지 않는다.

음성은 실제 샘플의 pitch/loudness/quality/delivery를 평가한다. 목소리·숨소리·흐느낌을 얼굴 형태 gate로 대체하지 않는다. 연기 방법명은 preparation provenance, emotional truth·range·chemistry는 사람의 문맥 평가에 남긴다.

영상 데이터셋이 필요하면 CASME II의 접근·이용 조건, 주석 규약, 대상·라이선스·데이터 분할을 먼저 확인한다. 논문을 읽은 것과 사용 권리를 확인하거나 데이터 품질을 검증한 것은 다르다. 이번 작업에는 데이터셋 다운로드나 모델 학습이 없다.

## 7. 회귀·검색·프롬프트 평가

[REGRESSION-CASES.jsonl](REGRESSION-CASES.jsonl)의 75개 사례는 저작된 기대값이다. 아직 resolver에 실행하지 않았고 통과 결과로 집계하지 않는다. 구현 단계에서는 아래를 별도로 측정한다.

| 평가 층 | 입력 | 확인 기준 |
|---|---|---|
| 의미/activation | 한국어·영어, 부정·인용·다의어·actor reversal | 전체 문맥과 부정 범위에 맞는 profile만 활성화 |
| 검색 | 라벨 있는/없는 형태, 기존 표현, 오타·철자 변형 | positive definition/components에서 찾고 반례·출처·ID만으로 양성 검색하지 않음 |
| 후보 노출 | 같은 frozen core와 locks | eligible 후보와 제외 이유, 슬롯별 위치·번들 참조 확인 |
| 채택 | optional 제안 + 구체 속성 영향 | 선택 전 advisory, 선택 후도 잠긴 속성·새 객체·관계 침범 없음 |
| literal prompt | 프로필의 각 component phrase | 실제 프롬프트 바이트에 필요한 관계·소유자가 남음 |
| 픽셀 | 원본 이미지 | 각 필수 요소의 PASS/FAIL/UNOBSERVABLE |

75개에서 저작·개발용 일부를 골라 수정하고, 나머지는 손대지 않은 문맥 변형·번역 holdout으로 보관한다. 반복 실행에 노출된 항목을 계속 holdout이라고 부르지 않는다. 같은 후보를 단순히 다시 말한 문자열만으로 구성하지 않고 원인·대상·부정·좌우·크롭이 바뀌는 쌍을 포함한다.

필수 실패 방지 기준은 **넓은 감정어의 자동 하드 형태 전환, actor/target 뒤집힘, lock 침범, metadata-only의 정지 PASS가 0건**인 것이다. 특정 범위에서의 0건 결과는 그 범위의 증거일 뿐 일반적인 무오류 보증이 아니다.

검색은 top-k에 동일 concept ID가 등장했다는 수치만으로 성공 처리하지 않는다. 뜻과 배우·요소가 맞는 후보인지 사람이 판정하고, Recall@k와 문맥 밖 오탐을 함께 기록한다. k는 현재 pack 노출 한도 안에서 사전에 정하고 데이터 수정 이후 바꾸지 않는다. BM25F와 embedding은 별도 결과로 남긴다.

표본 크기가 작으므로 임의의 95% 성공률을 통과선으로 선포하지 않는다. 먼저 쌍별 실패를 확인하고, 실제 트래픽 범위를 대표하는 추가 frozen 표본을 계획한다. 후보 수가 늘어 검색 노출이 밀리는 기존 항목의 회귀도 점검한다.

## 8. 이미지 비교와 수용 판단

[PIXEL-PLAN.json](PIXEL-PLAN.json)의 11쌍은 형태마다 다음 조건을 고정한다.

1. 사용자 요청, authorial core, intent lock을 **후보 검색 전에** 고정한다.
2. baseline은 고정 원본 데이터, proposed는 검토된 요소만 추가한다. 같은 모델·설정·배우 수·크롭·시선·의상·배경을 사용한다. seed를 지원하지 않으면 seed 동일성을 주장하지 않는다.
3. 초안 단계의 제안은 각 arm 3회로 시작한다. 총 66개 예정 출력이며 아직 생성하지 않았다. 이 수량은 소규모 진단용으로 충분성의 통계적 보증이 아니다.
4. 얼굴·눈·입·손의 원본 픽셀에서 각 gate를 평가한다. 좌우가 중요한 경우 배우 기준 좌우와 화면 기준 좌우를 별도 기록한다.
5. 눈물은 조명 반사와, 눈 주름은 기본 얼굴 주름과, 입술 누름은 단순 닫힘과 대비한다. 같은 배우의 중립 프레임이 없고 차이가 애매하면 불확실하게 기록한다.
6. 모든 적용 gate가 PASS일 때만 기술적 qualification으로 기록한다. **partial_is_fail**, 가려진 필수 요소는 UNOBSERVABLE, 생성 차단은 MODERATION_BLOCKED/미채점이다.
7. 기술적 통과 뒤에도 “자연스러운가”, “요청한 연기의 의미를 전달하는가”, “원래 의도를 보존하는가”를 별도 사용자 판단으로 남긴다.

전체 평가가 실패하면 성공한 일부 요소를 전체 재현으로 집계하지 않는다. 잠긴 크롭 때문에 입이 보이지 않으면 크롭을 임의로 넓혀 통과시키지 않는다. 원 요청에 맞는 다른 선택형이나 관찰 가능성이 높은 후속 구성을 검토 대상으로 기록한다.

## 9. 반영 검증과 배포 가능한 묶음

반영 시 현재 프로젝트의 dictionary validator, visual profile compiler, semantic/profile index builder를 사용한다. 원본 extension의 합의가 끝난 후 파생 index를 재생성한다. 이번 조사에서 확인한 도구는 다음이다.

- `scripts/validate_photo_prompt_dictionary.py`
- `scripts/build_visual_profile_index.py`
- `scripts/build_semantic_index.py`
- `scripts/visual_profile_contracts.py`
- `scripts/photo_candidate_semantics.py`

위 경로의 기준 디렉터리는 `skills/photo-prompt-image-generator`이다. 실행 옵션은 반영 당시의 `--help`와 해당 원본을 확인한다. 이번 리서치를 끝내기 위해 운영 index를 재생성할 필요는 없다.

다음 테스트는 관련 행위가 바뀔 때 실행할 기존 확인 대상이다: `test_photo_candidate_semantics.py`, `test_photo_visual_profile_retrieval.py`, `test_photo_positive_retrieval.py`, `test_photo_core_retrieval.py`, `test_photo_bm25f_retrieval.py`, `test_photo_semantic_index.py`. 새로운 75개 문맥 사례는 실제 입력 계약에 연결한 뒤 실행하고, JSON 구조 검사와 의미 동작 통과를 따로 보고한다.

반영 완료 묶음은 `원본 SHA + 데이터 ID 목록 + 좁은 diff + schema/guard 결과 + 검색/후보 노출 결과 + 프롬프트 바이트 + 원본 이미지/게이트 + 미검증 항목`이다. 이전 데이터 보존을 확인하고, semantic retrieval 품질과 픽셀 결과가 달라지는 원인을 구별한다.

처음 출고 가능한 범위는 P1에서 검증된 좁은 형태와 동등 표현이다. P2/P3는 문맥 guard와 실패 사례를 통과한 항목만 포함한다. P4는 해당 매체 지원이 없으면 연구 메타데이터로 남긴다. 이런 단위로 반영하면 원 대화의 폭을 유지하면서도 현재 사진 도구가 실제로 보장할 수 있는 범위를 넘지 않는다.
