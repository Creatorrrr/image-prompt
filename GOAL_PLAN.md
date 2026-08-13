# Natural-Language Adult Moe Image Goal

- 작성: 2026-08-12 17:44 KST
- 상태: active
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@3e86a88`
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: `photo-prompt-image-generator`가 포즈, 행동, 상황, 표정, 외형, 스타일, 분위기에서 실제로 모에한 이미지를 만들게 개선한다. 모에는 야함과 동일하지 않아 야하지 않아도 성립하지만, 2026-08-12 사용자 보정에 따라 성인 캐릭터의 은은한 성적 매력은 모에를 보조할 수 있다. 모에는 기본적으로 예쁘고 귀여운 미소녀/미소년이어야 하며, 단순히 성별이 맞는 일반 인물로는 부족하다.
- 최종 제품/결과: 자연스러운 한국어·일본어·영어 모에 요청이 전문 연구 별칭 없이 모에 응답 경로로 들어간다. 명시적 여성은 성인 미소녀, 명시적 남성은 성인 미소년, 명시적 중성/논바이너리는 그 표현을 보존한 예쁘고 귀여운 성인, 성별 미지정은 주류 기본값인 성인 미소녀로 라우팅된다. 이 외형적 진입 조건과 별도로 역할·종족·믹스인·관계를 보존한 한 장면에서 캐릭터 고유의 모에 메커니즘이 얼굴·손·자세·촉발 대상·즉시 결과로 읽힌다. 명시적 비성적 요청만 관능/페티시 스타일을 비활성화하고, 일반 성인 모에 요청은 낮은 강도의 관능미를 보조 축으로 허용하되 예쁨·귀여움·캐릭터 반응을 대체하지 않는다. 동결된 대표 렌더를 사용자가 기존 결과보다 모에하다고 직접 확인해야 목표가 끝난다.
- 범위: 자연어 의도·한국어 부정·likeness 파싱, 모에/갭모에/네코미미 라우팅, scoped adult-appeal 기본값, viewer/모에 응답 계약, 역할 보존형 장면 조립, 모에 장면 다양성, composed-prompt 감사, 자연어 회귀 사례, 제한된 이미지 렌더와 사용자 비교.
- 비목표: `subculture-illustration-image-generator`의 29요소 문법 재개편, 모든 인간 사진의 전역 sensual 기본값 변경, 모든 모에를 반드시 야하게 만드는 정책, 성적 매력으로 예쁨·귀여움·캐릭터성을 대체하는 구성, 특정 실존 인물/보호 캐릭터 복제, 미성년 또는 연령 모호 피사체의 성적 표현, 배포·push·PR, 대규모 선호도 조사나 신규 외부 평가 서비스, 이미지 모델 전체의 보편적 모에 성능 주장.

## 진척 계약

- 진척으로 인정: 실제 라우팅·파싱·후보팩·composer/audit 동작 변화, 역할 보존형 모에 장면 데이터 변화, 동결 입력에서 달라진 pack/prompt, 실제 렌더 후보와 사용자 판정.
- 진척으로 인정하지 않음: 연구 문서·별칭·fixture·테스트·평가표만 추가한 상태, `moe/cute` 형용사만 붙인 프롬프트, 기존 친절/협력 장면을 모에라고 재분류한 보고서, audit 또는 LLM 리뷰만 통과한 상태.
- 검증-only 작업 상한: 초기 기준선 1회 뒤 각 제품 단계당 focused 검증 1회, 제품 후보가 나온 뒤 렌더 자격 1회, 마지막 affected regression 1회. 검증-only checkpoint를 두 번 연속 만들지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, matching report 우선 갱신, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker`.

## 기준선과 고정 결정

- 현재 기준선: `모에한 성인 네코미미 츤데레 메이드`는 `two_person_rival_reflection`로 떨어지고 `character_grammar=false`, viewer 없음, 핵심 네 토큰 미충족, `모에한 성인 네코미미`가 likeness reference로 오염되며 `sensual_editorial=1`이 활성화된다. `갭모에`는 미라우팅이고 구현 문구 `갭모에 대비 구조`만 라우팅된다.
- 부정 기준선: `야하지 않은 모에한 성인 캐릭터`는 `야하지`와 `않은`이라는 양성 필수 토큰으로 분해되고 모에 경로는 비활성인 채 sensual 기본값이 유지된다.
- 데이터 기준선: character extension은 24 presets, 141 visual atoms, 72 atomic scenes를 갖지만 간단한 텍스트 집계에서 최소 44/72가 직장·교대·기술자·정비 맥락, 29/72가 수리·고치기 맥락, 34/72가 동료 맥락이며 static/expression-first 장면은 0이다.
- 평가 기준선: 저장된 내부 평가는 행동 가독성·actor/action/target/consequence·성인성·기술 품질을 모에 점수와 결합한다. 사용자는 기존 결과 중 어느 것도 모에하지 않다고 판정했으므로 이 평가의 `pass`는 사용자 결과 기준선이 아니다.
- 고정 설계:
  - `adult_age`와 `sexual_tone`을 분리한다. 명시적 nonsexual 모에만 `sexual_tone=nonsexual`, `sensual=0`, `fetish=0`으로 잠근다. 일반 성인 모에는 `sexual_tone=sensual_optional`과 기존 저강도 `sensual=1`, `fetish=0`을 유지하고, 명시적 sensual 요청은 scoped override로 강화할 수 있다. 어느 경우에도 sexual appeal은 미소녀/미소년 외형 진입 조건이나 캐릭터 고유 사건을 대신하지 않는다.
  - 모에는 `adult pretty+cute aesthetic entry condition + character_baseline + one primary mechanism + trigger/target + visible response + immediate consequence + continuity anchor`의 이중 계약이다. 외형만 있거나 사건만 있어도 통과하지 않는다.
  - `미소녀/미소년`은 실제 연령이 아니라 성인 캐릭터 디자인 범주로 해석한다. prompt는 20대 중반 이상과 성인 형태를 명시하고, 미성년·연령 모호·아기 얼굴·과대 눈을 배제한다.
  - 얼굴·손·촉발 대상을 같은 close/medium focal plane에 두되 모든 모에를 2인 친절 장면으로 만들지 않는다. expression-led, pose-led, solo, object-bond, private-joy, safe-fluster, earnest-effort 경로를 허용한다.
  - costume, ears/tail, blush, body morphology는 단독 primary가 될 수 없고 support만 가능하다. 이를 제거해도 주 메커니즘이 남아야 한다.
  - 이미지 생성은 동결된 소수 사례에만 사용하며 각 사례의 실패를 숨기거나 유리한 결과만 선택하지 않는다.
- 관련 과거 실행 보고서와 적용 교훈:
  - `docs/failed-reports/2026-08-11-photo-mandatory-intent-polarity-contamination.md`: phrase-level typed polarity를 재사용하고 부정/soft guidance를 양성 mandatory intent로 보내지 않는다.
  - `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`: 기존 96건은 literal alias contract일 뿐 독립 자연어 holdout이 아니므로, 구현 전에 별도 자연어 사례를 동결한다.
  - `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`: prompt/audit PASS와 픽셀 행동 가독성을 분리하고 손 방향·공유 대상·한 가지 반응을 단순하게 고정한다.
  - `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`: 별도 태그·고정 문구·테스트만 추가하지 않고 실제 candidate selection과 composition을 바꾼다.
  - `docs/passed-reports/2026-08-11-research-backed-moe-grammar-v2.md`: one-primary/two-support와 shared-event 구조는 재사용하되 해당 보고서는 illustration prompt evidence일 뿐 photo pixel/user preference 증거로 사용하지 않는다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 자연어 계약 동결과 파서 수정 | 구현 전에 KO/JA/EN 자연어 positive·hard-negative 사례를 고정하고, 모에/갭모에/네코미미 및 한국어 multiword negation을 typed intent로 해석하며 control adjective가 name/likeness가 되는 경로를 차단한다 | 기준선 명령과 같은 CLI pack 재생, 파서 focused tests | 대표 문장이 character route에 들어가고 핵심 의미가 typed coverage를 가지며 likeness 오염과 부정 polarity 오염이 0건 |
| 2. scoped 모에 정책과 응답 계약 | 명시적 모에 경로에 viewer contract와 `moe_response_contract/v10`을 자동 부착하고 성인 미소녀/미소년 외형 진입 조건, 관계 register, 능동적 반발, 분리된 돌봄 행동·또래 호감 시선축, 무문자 배경 제어, 50–120단어 hard budget을 적용한다. 명시적 nonsexual은 0/0으로 잠그고 일반 성인 모에는 저강도 sensual 보조 축을 유지하며 명시적 sensual override도 보존한다 | 여성/남성/중성/미지정 라우팅, 외형-only·사건-only·부정표정-only·과업 지향 온기·손만 보는 호감·마망식 인자함을 츤데레로 대체·화면 밖 가상 시선축·두 번째 전체 얼굴·머리와 홍채의 동방향·generic side-eye·정면 눈맞춤·단일 미세표정·배경문자·121단어 이상 mutation, explicit-nonsexual/generic/sensual 3분기, 기존 ordinary-human/adult-appeal focused regression | 비성적 모에 pack은 0/0, 일반 모에 pack은 sensual 1/fetish 0, 명시적 sensual 요청은 override를 유지한다. 츤데레는 `peer_liking_under_denial`, lower care anchor, 화면 가장자리의 흐린 부분 상대 얼굴 단서, 그 반대 3/4 머리·코축과 홍채만의 사선 복귀, 부드러운 아래눈꺼풀·억누른 한쪽 입꼬리를 요구한다. 명시적 마망·모성적 요청은 `nurturant_benevolence`와 인자한 표정을 보존하며 인과 사건을 50–120단어 안에 함께 가짐 |
| 3. 역할 보존형 구성과 감사 | 사용자 역할·종족·믹스인·관계를 scene에 투영하고 baseline/mechanism/trigger/response/consequence/continuity를 compact prompt에 결합한다. label-only, attribute-only, generic-kindness, role replacement, impossible multi-action을 감사에서 거부한다 | 츤데레 메이드·케모노미미·solo private joy·gap·hard-negative composed prompt의 audit | 대표 positive prompts가 역할을 보존하고 50–120단어 내에서 한 메커니즘을 가시화하며 모든 negative mutation이 fail-closed |
| 4. 장면 다양성 재균형 | 기존 연구 노드를 유지하면서 직장·수리·동료 완성 장면 의존을 줄이고 solo/dyad, 일상/취미/이동/판타지, expression/pose/action/relationship-led 메커니즘을 실제 selectable blueprint로 추가·교체한다 | scene audit와 고정 seed 분포/선택 표본 | 직장·수리·동료가 각각 과반이 아니고, static/expression-first를 포함한 여러 메커니즘이 사용자 역할을 교체하지 않고 선택됨 |
| 5. 제한된 실제 렌더와 사용자 판정 | 이전 실패를 대표하는 동결 사례 4종을 보존하고, 사용자 피드백 뒤에는 첨부된 가상 성인 인물의 얼굴을 고정한 `TSUNDERE CARE` 보정 후보를 정확히 1회 생성해 숨김 없는 비교표로 제시한다 | metadata-free thumbnail/native 기술 검사 후 사용자에게 직접 모에 여부·은은한 성적 매력의 기여·기존 대비 판단 요청 | 사용자가 대표 결과를 모에하다고 명시하고 기존보다 낫다고 판단하며 요청별 sexual tone이 맞음. 미달이면 원인별 구현 수정은 최대 2회만 수행 |
| 6. 회귀·문서·실행 지식 정리 | 최종 동작에 맞춰 skill/reference를 갱신하고 affected photo regression을 실행하며 material report lifecycle을 양방향 정리한다 | focused photo suites, dictionary/scene/semantic checks, `git diff --check`, 최종 criterion review | 아래 최종 기준 전부 통과하고 검증되지 않은 범위를 명시함 |

## 진행 현황 (2026-08-13)

- 완료: 32개 KO/JA/EN 자연어 positive·hard-negative fixture, 자연어 모에/갭모에/마망·모성적 모에/일반 다정한 돌봄 라우팅, 한국어·일본어·영어 nonsexual polarity, likeness 오염 차단. 여성·남성·중성·성별 미지정 외형 라우팅, 일반 모에의 `sensual_optional` 분기, 명시적 readable-text 요청의 제한적 예외를 각각 포함한다. 마망·모성적 관계 요청과 네코미미가 결합돼도 관계성을 우선해 `quiet_care_trace + nurturant_benevolence`를 주 경로로 쓰고 귀 반사는 `nonhuman_reflex_leak` 보조로 내린다. 완료 감사에서 순차 alias 치환이 `猫耳メイド`/`ツンデレメイド`의 뒤쪽 역할을 누락시키는 결함을 발견해 원문 기준 단일-pass 치환으로 수정했으며, 25개 positive와 7개 hard-negative 모두 공개 래퍼의 실제 후보팩 생성까지 32/32 통과한다.
- 완료: `moe_response_contract/v8`, 자동 viewer experience, 성별 미지정 성인 미소녀 기본값과 여성/남성/중성 presentation 라우팅. 명시적 비성적 성인 모에의 0/0은 유지하고, 일반 성인 모에는 `sensual_optional` 1/0을 사용한다. 츤데레에는 `peer_liking_under_denial`, 명시적 마망·모성적 돌봄에는 `nurturant_benevolence`, 일반 다정한 돌봄에는 `directed_care_without_role_inference`, 기타 메커니즘에는 `character_specific_reveal`을 부착한다. `denial_care_leak`는 능동적 반발, 화면 아래의 손·상처·물건 care-action anchor, 같은 성인 상대의 별도 face-level relationship anchor, 머리는 피하되 홍채가 얼굴 높이 시선축으로 돌아가며 은은한 사적 호감을 억누르는 표정을 각각 literal evidence로 요구한다. 손·상처·물건만 보는 온기, 마망식 인자함, 화면 밖 얼굴, generic side-eye는 츤데레 근거로 통과시키지 않는다. 명시적 마망 경로에서는 반대로 편안한 눈썹·참을성 있는 부드러운 눈·안심시키는 입매·보호적 주의를 하나의 literal expression phrase로 요구하며 능동적 반발을 강제하지 않는다. 단순한 다정함만으로 마망 관계를 추론하지 않는다.
- 완료: baseline/trigger/target/visible response/consequence/continuity에 더해 `event_phase`를 필수화하고 settled endpoint를 fail-closed 처리.
- 완료: 네코미미를 전신 수인과 분리해 compact living ears + human limbs 계약으로 제한하고, 요청되지 않은 하트·스파클·블러시 원·만화 반응표시를 scoped negative에 추가.
- 완료: atomic scene 28개를 추가해 selectable scene corpus를 72개에서 100개로 확장. 직장·수리·동료는 각각 과반 미만이며 solo, static, expression-led, pose-led, private-joy를 포함한다. 마지막 기본 장면들은 자연스러운 일반 모에 route에서만 선택되고, 츤데레용 장면은 다친 성인 또래를 퉁명스럽게 돌보면서 본심을 숨기는 관계 register에만 결박된다. direct preset의 기존 4장면 순환 계약은 유지한다.
- 완료: 동결 4사례 최초 렌더를 숨김 없이 보존. 픽셀 실패가 확인된 메이드·바리스타·일반 캐릭터만 1회 제품 수정 후 다시 렌더하고, 각 attempt의 pack/prompt/audit/request/image를 분리 보존.
- 외형 계약 이전 회차의 픽셀 자격: 경호원 `pass`, 메이드 `pass_with_defect`(큰 슬리브, 귀 방향 모호), 바리스타 `partial`(종족/기호 문제 해결, 귀 반사·거품 흔적 약함), private joy `partial`(중간 배열은 보이나 catch/fingerprint 모호). 이는 모에 판정이 아니라 가독성 판정임.
- 완료: 원자 장면이 4개로 늘어난 런타임 계약을 갱신하고, rule-mode 후보팩 fallback이 선택 장면 밖 location 후보를 노출하던 회귀를 양쪽 projection 경로에서 fail-closed 처리. 79개 일반화 + 24개 holdout + 6개 domain holdout이 다시 통과했다.
- 완료: 사전 validator, 112/112 scene audit, semantic contradiction/generalization/holdout, JSON/Python 형식, `git diff --check`, 현재 의미 색인(6513 entries) 검사를 통과했다.
- 이전 외형-contract 경계에서 완료: affected 모듈 `tests.test_prompt_generator` + `tests.test_photo_prompt_contract_v2` 329/329 통과(655.502초). 네 aesthetic-contract 렌더 사례의 후보팩은 당시 코드와 바이트 동일했다.
- 사용자 기준 보정 후 현재: 직전 최종 라운드에서 생성된 메이드 attempt 3은 새 외형 계약 이전 결과로 보존했다. 새 기준은 기존 평가 문구 보정이 아니라 제품 acceptance condition 변경이므로, 기존 시도를 숨기지 않는 조건으로 영향받는 대표 사례당 1회의 bounded aesthetic-contract qualification을 허용한다.
- 제품 결함 수정: 일반 남성 모에 요청은 계약에서 `adult_bishonen`이었지만 rule sampler가 먼저 `elderly_commuter`를 고르는 순서 오류가 있었다. 자연어 모에 route를 일반 preset/subject sampling보다 먼저 적용하고, 명시 preset 및 좁은 역할/mixin recipe는 계속 우선하도록 수정했으며 male/generic/ordinary 회귀로 고정했다.
- 새 외형 계약 렌더: 네 사례 모두 계약에서 요구한 성인 여성·pretty+cute 외형 단서와 비성적 framing은 픽셀에 남았다. 기술적 사건 자격은 guard `pass`, maid `pass_with_defect`(half-sleeve 경계 약함), barista `partial`(귀 방향과 foam consequence 약함), private joy `pass_with_defect`(낙하 조각은 선명하나 손 접촉·wet trace 모호)로 판정했다. 사용자는 네 결과 모두 기존보다 낫지 않다고 판정했고 `TSUNDERE CARE`만 상대적으로 더 모에에 가깝다고 했다. 비성적이라는 관찰은 합격 조건이 아니며, 일반 성인 모에에서는 은은한 성적 매력이 도움이 될 수 있다는 추가 보정도 받았다.
- 입력 필터 기록: private-joy 최초 aesthetic-contract 요청은 image-generation 입력 moderation `other`로 차단되어 이미지가 생성되지 않았다. 부정문에서 오탐 가능 표현을 제거하되 성인·비성적·외형·사건 의미를 유지한 1회 moderation retry로 결과를 생성했고 원 요청/차단/retry를 모두 보존했다.
- 완료: 첨부된 가상 성인 인물을 sole reference로 고정하고 얼굴 치환·평균화·구조적 미화·de-aging을 거부하는 identity-mode pack/audit 계약을 구현했다. `TSUNDERE CARE`와 낮은 강도의 성인 매력을 결합한 후보를 정확히 1회 생성했으며 reference와 native 결과를 byte-identical project copy로 보존했다. agent native review는 동일성 `pass_with_minor_drift`, 들어 올린 밴드 단계 `pass_with_minor_ambiguity`, 귀 방향 `partial`, 금지한 하트와 가짜 배경 글자 `fail`로 기록했다.
- 픽셀 결함 환류: 동일 인물 후보의 차갑고 우울한 얼굴, 큰 귀, 약한 귀 방향, 하트·가짜 글자 침입을 숨기지 않고 v4 계약으로 환류했다. 동일 seed 최종 후보팩 `739ac872fdaef91b`에서 `affective_leak_phrase`, `background_control_phrase`, human-ear 크기 기준, 서로 다른 귀 각도, 하트·pseudo-writing·menu/chalkboard/signage 부정 항목이 실제 노출된다. 사용자가 readable text를 명시한 경우만 background control과 관련 negative를 제한적으로 해제하는 회귀도 고정했다. 이 제품 보강 뒤 새 렌더는 사용자 판정 전 추가하지 않았다.
- 완료: v4와 명시적 readable-text 예외 환류 경계에서 affected 모듈 `tests.test_prompt_generator` + `tests.test_photo_prompt_contract_v2` 330/330 통과(594.018초). 현재 semantic index 6,513 entries/16 shards는 dictionary hash `8da2e290167ab69c...`와 일치하며 contradiction 2,001/0 violations, public generalization 79/79, holdout 24/24, domain holdout 6/6, retrieval holdout 22/22를 통과했다. JSON/Python 형식과 `git diff --check`도 통과했다.
- v4 렌더 진행: 감사된 동일 인물 v4 프롬프트로 native image generation 1회를 실행했으나 출력 단계 moderation `sexual`로 픽셀 없이 차단되었다(request ID `fd828001-2def-4b7c-8702-151c1c0614ac`). 이는 모에/품질 실패로 세지 않으며 `render_request_post_pixel_contract.json`과 matching failed report에 보존했다. 성적 매력은 도움이 될 수 있으나 필수는 아니라는 사용자 보정에 따라, identity·pretty+cute·warm leak·care event·귀·무문자 배경은 고정하고 optional sensual 문구만 제거한 nonsexual runtime retry 1회를 허용한다.
- v4 nonsexual runtime retry: Exactly one native result was returned after the moderation block and was copied byte-identically as `render_post_pixel_contract_nonsexual_retry.png`. The hidden comparison sheet `identity_v4_comparison.png` includes the reference, prior v3 fixed identity, and v4 retry. Agent technical review resolved hearts, pseudo-writing, cold/melancholy first read, and ambiguous unfinished bandage state, but rated the result `partial` because the ears are still too large/nearly symmetric and active tsundere denial is weak. The positive prompt is also 211 words—above the skill's roughly 50-120 word target—and the current audit failed to warn, so compactness remains a product/audit gap. This does not establish moe or improvement.
- v5 compactness repair: The moe contract now exposes an English 50-120-word budget and the composed-prompt audit fails outside it. The same fixed-identity seed emits pack `6ff8946f91f5e4a4`; a 119-word sensual-optional composition passes contract and photographic-integration preflight with only manual pixel/user-review warnings. The final affected modules `tests.test_prompt_generator` + `tests.test_photo_prompt_contract_v2` pass 330/330 (594.877 seconds). It was not rendered, so the prior v4 image remains the sole new pixel result for user judgment.
- 사용자 판정 수신: fixed-identity v3 `render_identity_control.png`는 완전한 합격은 아니지만 모에에 약간 가까우며 기존 `TSUNDERE CARE`보다 낫다. 그 코스튬에서 현재 저강도 성적 매력은 적절하므로 유지한다. 남은 핵심 결함은 삐친 표정과 시선 속에서 상대를 좋아하는 본심이 은은하게 비치지 않는다는 점이다. v4 nonsexual retry는 츤데레로서는 퇴보해 츤데레 느낌이 사라졌지만, 마망으로서는 이미 괜찮고 더 인자한 표정이면 개선될 수 있다는 별도 신호로 분류한다.
- v6 제품 및 단일 렌더: fixed-identity v3를 츤데레 기준선으로 고정한 pack `9f88d9c473fcbc7b`와 120단어 composed prompt가 `active_denial_phrase`와 `concealed_affection_phrase`를 각각 결합해 preflight `pass`를 받았다. 기존 인물·코스튬·손·밴드·카페·구도·저강도 성적 매력을 고정하고 표정과 눈 방향만 바꾸는 이미지 편집을 정확히 1회 실행해 `render_concealed_affection_v6.png`로 보존했다. agent 픽셀 판정은 능동적 반발 강화 `pass`, 동일성·장면·성적 톤 보존 `pass`, 상대 지향의 숨긴 호감 `fail`이다. 눈은 상대에게 되돌아오기보다 더 옆을 경계하고 억눌린 거의-미소도 읽히지 않아, 모에 또는 개선으로 주장하지 않는다.
- v6 최종 기술 검증: affected 모듈 `tests.test_prompt_generator` + `tests.test_photo_prompt_contract_v2` 330/330 통과(596.992초). 최신 v6 composed prompt 재감사 `pass`, dictionary metadata `pass`, 현재 scene-expression 112/112, semantic index 6,513 entries와 dictionary hash `8da2e290167ab69c...` 일치를 확인했다. 이는 제품 계약과 산출물 무결성 증거이며 픽셀 모에 합격 증거가 아니다.
- v7 preflight 환류: v6 픽셀에서 고객 눈이 화면 밖인데 `toward the customer's eyes`라는 문구만으로 감사가 통과해 실제 시선 종착점을 판별할 수 없었던 원인을 제품 계약으로 환류했다. 같은 seed의 pack `ae0a72d33f2f4dd7`은 `recipient_anchor_phrase`와 `recipient_gaze_vector`를 노출한다. 고객의 bandaged hand를 lower foreground near-lens POV로 고정하고, 머리는 비낀 채 홍채만 그 손으로 돌아오며 lower lids와 억누른 입꼬리를 결합한 120단어 prompt가 preflight `pass`를 받았다. 기존 v6 off-frame-eye 문구와 generic side-eye mutation은 fail-closed 한다. 이 v7 prompt는 사용자 v6 판정 전 렌더하지 않았다.
- v7 최종 기술 검증: 모에 관련 focused 7/7 통과(32.030초), affected 모듈 전체 330/330 통과(596.059초). v7 composed prompt 재감사 `pass`, dictionary metadata `pass`, scene-expression 112/112, semantic index 6,513 entries와 dictionary hash `8da2e290167ab69c...` 일치를 확인했다. 이는 구성 결함 폐쇄와 회귀 부재의 증거이며 모에 픽셀 합격 증거가 아니다.
- v8 관계 벡터 환류: v7은 고객의 손을 돌봄 행동의 대상이자 호감 시선의 종착점으로 동시에 써, 문장에 `fond`가 있어도 픽셀에서는 상처를 살피는 마망 시선으로 읽힐 수 있었다. 같은 seed의 최신 pack `96e0c368be262947`은 `peer_liking_under_denial`, `care_action_anchor_phrase`, `relationship_gaze_anchor_phrase`를 노출한다. 손은 lower foreground의 행동 앵커로 남기고 같은 성인 고객의 face-level near-lens eye line을 별도 관계 앵커로 두며, 홍채가 그 높은 시선축으로 돌아갈 때만 `private liking`을 허용하는 120단어 prompt가 preflight `pass`다. 손으로 돌아가는 시선, 마망식 인자함, generic side-eye, 화면 밖 얼굴, 두 앵커 합치기 다섯 mutation은 모두 fail-closed 한다. 명시적 마망에는 네 가지 인자한 미세표정을 요구하고 일반적인 다정한 돌봄은 별도 `directed_care_without_role_inference`로 두어 마망을 과추론하지 않는다. 이 계약을 아래의 단일 v8 렌더에 사용했다.
- v8 최종 기술 검증: focused routing/tone/identity/tsundere-audit/mamang-expression 5/5 통과(20.521초), affected 모듈 전체 331/331 통과(599.202초). 최신 v8 composed prompt는 120단어로 감사 `pass`, 다섯 결함 mutation은 모두 의도한 check에서 `fail`이다. dictionary metadata `pass`, scene-expression 112/112, semantic index 6,513 entries/768 dimensions와 dictionary hash `8da2e290167ab69c...`, JSON/Python 형식과 `git diff --check`도 통과했다. 이 결과는 구성·라우팅·회귀 안전성 증거이며 새 픽셀의 모에 합격 증거가 아니다.
- v8 마망-네코미미 합성 보강: 종족 분기가 care 분기보다 앞서던 탓에 `인자한 마망 ... 네코미미 메이드`가 `nonhuman_reflex_leak + character_specific_reveal`로 잘못 덮이던 결함을 수정했다. KO/JA/EN 세 합성 fixture와 실제 wrapper 후보팩은 모두 `quiet_care_trace + nurturant_benevolence + nonhuman_reflex_leak support`를 유지한다. 첨부 가상 성인의 동일성, 메이드 의상, 저강도 sensual 1/fetish 0을 고정한 pack `9ac4204b61eb436e`과 118단어 composed prompt가 감사 `pass`다. 편안한 눈썹·참을성 있는 부드러운 눈·안심시키는 입·차분한 보호적 주의 중 하나가 빠지거나 generic kindness 또는 츤데레식 사적 호감으로 대체되는 여섯 mutation은 모두 `moe_response_benevolent_affect`에서 fail-closed 한다. 새 이미지는 생성하지 않았으므로 이 결과는 마망 픽셀 개선의 증거가 아니다.
- v8 경계 당시 코드 최종 기술 검증: affected 모듈 `tests.test_prompt_generator` + `tests.test_photo_prompt_contract_v2` 331/331 통과(613.925초). dictionary metadata `pass`, scene-expression 112/112, semantic index 6,513 entries/768 dimensions와 dictionary hash `8da2e290167ab69c...`, JSON/Python 형식과 `git diff --check`도 통과했다. 이는 당시 라우팅·구성·회귀 안전성 증거이며 새 츤데레/마망 픽셀의 모에 합격 증거는 아니다.
- v6 오른쪽 최종 판정 정정: 사용자가 요청한 것은 오른쪽 결과에 대한 agent 판정이었는데 이를 사용자 판정 대기로 잘못 남겼다. 원본 픽셀을 다시 확인한 결과, v6는 볼·입술의 삐침은 v3보다 강하지만 시선이 성인 상대에게 되돌아가는 호감이 아니라 옆을 경계하는 눈으로 읽힌다. 아래눈꺼풀의 부드러움과 억누른 거의-미소도 보이지 않아 숨긴 호감은 `fail`, v3 대비 츤데레 모에 개선은 `fail`로 확정한다.
- v8 단일 렌더 및 agent 판정: 첨부 가상 성인을 sole identity/age reference로, v3를 장면·메이드 의상·손·밴드·카메라·사용자 승인 저강도 성적 톤 reference로 분리해 정확히 1회 생성했다. native PNG와 project copy는 SHA-256 `e85d2502...`로 byte-identical하고 run `a00261551ffb9579`에 실제 runtime prompt를 `audit_status=not_run`으로 기록했으며 재시도나 후보 선택은 없다. C(v8)는 v6의 경계하는 옆눈을 고치고 v3/v6보다 즉시 예쁘고 귀여운 미소녀 인상, 더 선명한 삐침, 상대 지향 온기를 보인다. 반면 정면 눈맞춤이 너무 직접적이라 본심이 은은하게 새는 느낌이 약하고, 머리-홍채 분리와 억누른 거의-미소가 보이지 않으며, 첨부 인물보다 눈이 커지고 턱·볼 비율이 어려진 동일성 drift와 큰 귀가 남는다. 따라서 agent 자격은 `technical_partial`이며 모에 성공으로 주장하지 않는다.
- v9 제품 환류: C의 알려진 결함을 새 이미지 없이 `moe_response_contract/v9`에 반영했다. 츤데레는 이름뿐인 `head aside`를 더는 허용하지 않고, 명명된 3/4 머리 회전·렌즈를 비낀 코축·같은 성인 상대 쪽으로 홍채만 움직이는 작은 사선 복귀·부드러워지는 아래눈꺼풀·올라가려다 눌리는 한쪽 입꼬리를 모두 요구한다. `reference_identity_phrase`는 눈 크기/형태/간격, 얼굴 길이, 하관·턱 너비와 확대·원형화·단축·협소화 금지를 요구하며 identity-mode negative에도 눈 확대, 얼굴 단축, 턱 축소, dollification, de-aging을 추가했다. 같은 seed 최종 pack `4e0494bace97848c`와 120단어 v9 composition은 preflight `pass`; 정면 눈맞춤, 일반 head-aside, 아래눈꺼풀만, 입꼬리만, 약한 동일성 앵커, 합쳐진 관계 앵커 여섯 mutation은 모두 의도한 check에서 `fail`이다. 새 픽셀은 생성하지 않았다.
- v9 렌더 승격 감사: 후보팩이 일반·관계 메커니즘·종족·동일성의 23개 hard gate를 노출하고 `audit_moe_render_review.py`가 결과 경로/SHA, 각 gate의 exact pass/fail과 픽셀 근거, 실제 사용자 판정 출처를 fail-closed 검증한다. 기술 gate 전부가 pass여도 사용자 판정 전에는 pending이며, 사용자가 좋아한다고 해도 동일성 또는 시선 gate가 하나라도 실패하면 대표 후보가 될 수 없다. C를 소급 적용한 review는 schema failure 0건, hard-gate failure 12건으로 `failed_technical_hard_gates`이며, 특히 정면성 6개와 동일성 5개 및 귀 크기 1개가 승격을 막는다.
- v9 최종 기술 검증: `tests.test_photo_prompt_contract_v2` 56/56 통과(270.352초), `tests.test_prompt_generator` 276/276 통과(341.456초)로 affected 합계 332/332다. dictionary metadata `pass`, scene-expression 112/112, semantic index 6,513 entries/768 dimensions와 dictionary hash `8da2e290167ab69c...`, JSON/Python 형식, 현재 v9 composed 재감사, `git diff --check`가 모두 통과했다. 이는 v9 제품 계약·감사와 비모에 회귀 부재의 증거일 뿐, 새 v9 픽셀이나 사용자 모에 합격 증거는 아니다.
- v9 D 단일 렌더와 실패 판정: 첨부 인물은 sole identity/age, A(v3)는 장면·의상·손·밴드·구도·저강도 성적 톤 reference로 분리해 정확히 1회 생성했고 `render_peer_liking_v9.png`로 보존했다. D는 C보다 동일 인물의 눈 크기·얼굴 길이·턱 너비·성인성이 회복됐고 정면 눈맞춤도 피했지만, 머리와 홍채가 함께 같은 옆 방향을 보아 상대에게 되돌아가는 본심이 없고 아래눈꺼풀·억누른 입꼬리·귀 방향도 실패했다. v9 23개 gate 중 8개가 실패해 대표 승격 불가다. 또한 실제 runtime negative가 pack negative와 byte-identical하지 않아 런타임 계약상으로도 실패했으며, 결과를 삭제하거나 재시도하지 않았다.
- v10 제품 및 런타임 환류: D는 상대 얼굴이 화면 밖의 가상 eye line뿐이라 머리 방향과 홍채 종착점을 픽셀에서 검증할 수 없었던 구성 결함을 드러냈다. `moe_response_contract/v10`은 같은 성인 상대의 흐린 부분 단서—화면 상단 가장자리의 바깥쪽 한 눈과 관자/옆얼굴 조각—를 요구하고, 주인공의 3/4 머리·코가 그 반대편을 향하며 홍채만 단서로 복귀하게 한다. 일반 `duplicate faces` negative는 이 경로에서 제거하고 `duplicate primary subject`, `second full recipient face`로 대체했다. 현재 코드로 다시 동결한 같은 seed pack `0256f9b41cebb3a8`, 120단어 composition, 네 결함 mutation, 정확한 runtime request `4e410822e79a8deb`이 모두 preflight를 통과했으며 negative/reference bytes도 일치한다. 새 픽셀은 생성하지 않았다.
- v10 완료 감사에서 발견한 일반화 결함 수정: 역할 없는 자연어 츤데레 요청이 legacy `candid_iphone_portrait` 선호에 가로막히거나 gap/nekomimi route가 `natural_moe_default` 장면 부재로 종료되던 문제를 수정했다. 관계 register와 일치하는 일상 기본 장면을 우선하고, 명시적 역할은 계속 보존한다. `without sensual framing`도 nonsexual control로 인식해 내부 `sensual` 양성 토큰이 부정을 뒤집지 못하게 했다. 독립 no-preset KO/JA/EN 네 문장 회귀가 실제 candidate pack과 선택 장면까지 통과한다.
- v10 최종 기술 검증: 일본어 복합 alias 수정과 32-case 공개 래퍼 회귀를 포함해 `tests.test_photo_prompt_contract_v2` 59/59 통과(345.805초), `tests.test_prompt_generator` 276/276 통과(245.583초)로 affected 합계 335/335다. dictionary metadata `pass`, scene-expression 112/112, contradiction 2,001/0, generalization 79/79, holdout 24/24, domain holdout 6/6, retrieval holdout 22/22가 통과했다. 의미 색인은 6,513개 텍스트와 벡터가 모두 그대로 재사용됐고 현재 dictionary hash `d693b97c31dc93ba...`로 결박됐다. 현재 코드로 v10 pack/composition/runtime request를 재생성해 세 파일의 SHA가 모두 이전과 동일하고 pack `0256f9b41cebb3a8`, runtime prompt `4e410822e79a8deb`, exact negative/reference audit PASS, render count 0을 재확인했다. 이는 v10의 구성·런타임 결박과 비모에 경로의 회귀 부재를 확인한 것이며, 렌더 0회이므로 모에 픽셀 합격 증거가 아니다.
- Remaining: v10은 기술적으로 다음 한 번을 재현 가능하게 준비했지만 기존 계획의 같은 원인별 구현 수정 상한과 사용자 terminal judgment를 임의로 우회하지 않는다. 다음 렌더를 허용한다면 정확히 1회만 실행하고 25개 hard gate를 모두 통과한 뒤 사용자에게 A(v3) 대비 실제 모에·개선 여부를 판정받아야 한다.

## 최종 완료 기준

1. 자연스러운 KO/JA/EN `모에`, `갭모에`, `야하지 않은 성인 모에`, `네코미미 츤데레 메이드` 요청이 전문 별칭 없이 올바른 character route와 mechanism에 도달한다.
2. 대표 pack에서 viewer와 `moe_response_contract/v10`이 활성이고, 미지정/여성은 성인 미소녀, 남성은 성인 미소년, 명시적 중성은 그 표현을 보존한 예쁘고 귀여운 성인으로 라우팅된다. 명시적 nonsexual은 sensual/fetish 0/0, 일반 성인 모에는 1/0의 보조 가능 상태이며, 명시적 sensual override와 ordinary non-moe 인간 경로는 의도한 호환성을 유지한다. `denial_care_leak`는 `peer_liking_under_denial`, 능동적 반발, lower care-action anchor, 같은 성인 상대의 화면 상단 흐린 부분 얼굴 단서, 단서 반대 방향의 3/4 머리·코축과 홍채만의 복귀, 아래눈꺼풀과 억누른 한쪽 입꼬리를 요구한다. 손·상처·물건만 보는 온기, 마망식 인자함, 화면 밖 가상 시선축, 두 번째 전체 얼굴, 머리·홍채 동방향, generic side-eye, 정면 눈맞춤, 단일 positive microcue만으로는 통과하지 않는다. 명시적 마망·모성적 요청은 `nurturant_benevolence`로 치유계 경로에 들어가 편안한 눈썹·부드러운 눈·안심시키는 입매·보호적 주의를 모두 literal evidence로 보존한다. 일반 다정한 돌봄은 `directed_care_without_role_inference`로 분리되어 마망 관계를 추론하지 않는다.
3. 역할·종족·믹스인·관계가 prompt와 scene에 보존되고 control text가 name/likeness 또는 양성 mandatory intent로 오염되지 않는다.
4. 최종 프롬프트는 explicit adult + pretty/beautiful + cute/charming + 최소 두 가지 구체적 얼굴/눈/입/머리/스타일 근거를 먼저 결합하고, 한 가지 주 모에 메커니즘의 baseline, trigger/target, visible response, consequence, continuity를 얼굴·손·대상에 결합한다. 일반 인물, costume/ears/blush-only, 또는 외형-only는 통과하지 않는다.
5. selectable scene corpus는 직장·수리·동료 각각 과반 편향을 벗어나고 solo 및 expression/pose-led 경로를 포함한다.
6. 독립 자연어 positive/hard-negative, audit mutation, 기존 character routing, adult-appeal, viewer, dictionary/scene regression이 통과한다.
7. 제한된 실제 렌더에서 기술적 가독성, 성인성, 요청된 성적 톤을 확인하고, 사용자가 새 대표 결과를 실제로 모에하며 기존보다 낫다고 직접 판정한다.
8. 변경된 skill/reference가 모에와 성적 매력을 동일시하지 않되 성인 캐릭터의 성적 매력을 허용 가능한 보조 축으로 다루고, 귀여움·친절·태그·성적 매력 어느 하나도 모에 전체를 대체하지 않으며 audit/LLM 평가가 사용자 반응 증거를 대체하지 않는다고 명시한다.

## 검증 수준과 예산

- 위험 수준: medium, offline product behavior and prompt-policy change. 외부 배포나 destructive mutation은 없다.
- 반복 중 focused 검증: 수정한 parser/router/policy/contract/audit/scene에 대응하는 기존 테스트와 새 동결 사례만 실행한다.
- 렌더 예산: 최초 4회. 한 원인에 대한 제품 수정 후 최대 두 번의 추가 qualification round를 허용하되 각 round는 실패 사례만 다시 생성한다. 2026-08-12 사용자가 최종 라운드 도중 외형적 acceptance condition을 직접 추가했으므로, 그 이전 결과를 모두 보존하고 사례당 1회만 새 aesthetic-contract qualification을 추가한다. edit나 best-of-N으로 실패를 숨기지 않는다.
- 최종 검증: affected photo unit/contract suites, dictionary/scene/semantic integrity와 최종 네 사례 pack/audit를 한 번 수행한다. 독립 검토는 기존 최종 기준만 재확인하고 새 기준을 만들지 않는다.
- 검증 확장 전 질문 조건: 기존 경로로 필수 기준을 확인할 수 없어 새 evaluator/schema/service가 필요하거나, 사용자 판정 대신 장기 패널·실트래픽을 필수화해야 하거나, 전역 sensual 정책 변경이 필요할 때만 중단하고 묻는다.

## 중단 조건과 실행 지식

- 사용자 역할 보존과 generic natural-language routing이 충돌하면 broad `모에` alias를 전체 사진 도메인에 퍼뜨리지 말고 explicit character context guard로 제한한다.
- 같은 고정 사례가 같은 원인으로 두 번 구현 수정 후에도 실패하면 기준을 완화하거나 evaluator를 확장하지 않고 실패 이미지·pack·감사 결과와 다음 선택지를 사용자에게 제시한다.
- 사용자 판정이 필요한 최종 기준은 LLM 합의나 문서 주장으로 대체하지 않는다. 사용자 응답 전에는 목표를 complete로 표시하지 않는다.
- credential, token, secret, 민감 endpoint, 고객/개인정보는 보고서·로그·렌더 ledger에 저장하지 않는다. 필요하면 sanitized 결론과 접근 제한 evidence reference만 기록한다.
- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/` 파일명·header metadata를 module/path, environment, status, 최신순으로 평가하고 전문은 기본 최대 5건만 읽는다. 서로 충돌하면 현재 source와 직접 evidence가 우선한다.
- material failure는 재시도 전에 기존 matching failed report를 우선 갱신하고 같은 원인을 한 보고서에 통합한다. resolved/superseded lifecycle 변경은 관련 양쪽 보고서에 같은 변경으로 연결한다.
- 모든 최종 기준 통과 뒤에만 성공 보고서를 기본 최대 1건 작성한다. 자격은 기존 material failure 해결, 기본/문서화된 접근 실패 뒤 비자명한 대안, 또는 현재 코드만으로 비싸게 복원되는 다단계 재현 절차 중 하나여야 한다. 단순 테스트·문서·중간 빌드 통과는 자격이 아니다.
- 목표가 blocked/partial이면 passed report를 만들지 않고 matching failed report의 resolution/workaround 또는 최종 진행 요약에 검증된 부분 결과를 남긴다.
- 실행 지식 보고는 별도 stage/checkpoint가 아니며 제품 delta를 대체하거나 다음 구현을 지연하지 않는다.
- 적용 실행 지식: 위 5개 보고서. 새 material failure가 생기면 경로를 진행 로그와 최종 요약에 기록한다.

## Codex 실행 계약

- 이 `GOAL_PLAN.md`의 범위, 진척 계약, 검증 예산, 완료 기준을 권위 있는 경계로 사용한다.
- setup 이후 각 checkpoint는 product delta, 사용자-visible artifact, measured candidate result 또는 binding implementation decision을 남긴다. 테스트·문서·schema만으로 완료하지 않는다.
- 반복 중 focused 검증을 사용하고 마지막에 위험 비례 최종 검증을 한 번 수행한다.
- 최종 보고에는 실제 산출물, 변경 파일, 핵심 검증과 결과, 완료 기준별 pass/fail, 실행 지식 경로, 남은 위험을 포함한다.
- material scope 또는 validation program 확대 전에는 사용자에게 질문하며 자동 target uplift는 하지 않는다.
