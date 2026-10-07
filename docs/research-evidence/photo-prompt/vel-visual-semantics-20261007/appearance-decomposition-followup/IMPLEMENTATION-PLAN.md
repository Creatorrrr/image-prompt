# 외형 요소 분해의 데이터 반영 계획

2026-10-07 · 상태: 연구·구현 계획 완료, active runtime 채택 미실행

기존 [60개 제안 계획](../IMPLEMENTATION-PLAN.md)의 관계 단위를 이 문서의 세부 보존 조건으로 보완한다. 전체 K001–K217 번호를 유지하고 465개 분해 요소를 입력 근거로 둔다. 28개 VD 카드는 같은 의미를 더 세밀하게 다룬 연구 설계이며 독립적인 28개 runtime profile로 모두 등록할 대상은 아니다.

겹치는 범위는 후속 계획을 우선 적용한다. 후보 초안 20개를 기존 46개와 합산해 66개 새 후보라고 부르지 않고, 기존 VEL/실제 source와 비교해 병합·분리 여부를 결정한다. 후속 45장 pilot도 기존 36장 pilot과 자동 합산하지 않는다. 먼저 아래 5군의 의미 보존 비교를 수행하고 남은 평가군은 결과에 따라 정한다.

## 1. 반영 목표와 완료 판정

사용자가 원문과 같은 외형을 요구했을 때, 후보가 의상 층을 합치거나 가림을 제거하거나 접촉 상대를 바꾸지 않게 한다. 특히 다음 다섯 묶음을 우선한다.

| 우선 묶음 | 반영해야 할 관계 | 기존 계획에 대한 변화 | 완료 시 필요한 증거 |
|---|---|---|---|
| 베스트·골지 탑 | 닫힌 허리 앞판, 남는 중앙 탑/넥타이, 탑과 재킷의 다른 표면 | VEL-002/004/005/021/023을 영역별로 세분화 | 층별 소유자·완전 효과 범위, 관련 항목 조회/선택 기록, 최종 문장 및 픽셀 |
| 양손 타월·얼굴 | 같은 타월 두 잡힘, 중앙 전면 가림, 작은 수영복 끈 창, 작은 입술 틈 | VEL-029/058/059/060의 실제 형태를 분리 | 두 손·천·뒤 의복 동시 가시성, 치아/비대칭 보존 |
| 유리 접촉·결로 | 접촉 패치, 반사와 투과의 별도 경로, 거울 표면 결로 | VEL-014/018/025/054의 owner 분리 | 접촉↔근접 대조, 광학 소유자·초점의 보존 |
| 비접촉 질책·물리 접촉 | 손–얼굴 간격, 신발–상대 의복 접촉, 별도 지지 발 | VEL-041/042/043을 도구·대상·지지점별로 분해 | 실제 경계/간격·지지, 비성적 문맥과 시간적 한계 |
| 붉은 코드·기계 발광 | 공중 기호, 틈의 광원, 금속 수신면, 혈흔 제외 | VEL-047/057/059/060의 색 원인·범위 분리 | no blood 아래 긍정 발광 유지, 다른 소유자/얼룩 거부 |

현재 native loader에서 읽은 기준은 source 100개, 슬롯 후보 10,518개, profile 2,308개다. 실제 구현을 시작할 때 이 스냅샷을 그대로 현재 값이라고 믿지 말고 다시 기준을 고정한다. 동시 작업이 있는 checkout에서는 구현용 격리 worktree와 선택적 diff를 사용하고 이미 진행 중인 변경을 보존한다.

## 2. 입력 자료를 다섯 층으로 나누기

`SOURCE-DECOMPOSITION.json`은 변경하지 않는다. `SEMANTIC-UNITS.json`의 217행이 source와 기존 VEL 단위·추가 VD 카드를 잇는 연구 원장이다.

| 층 | 저장/표현할 내용 | runtime 사용 |
|---|---|---|
| 뜻의 핵심 구조 | 같은 타월, 실제 열린 고리, 지정된 접촉 대상, 두 층의 상대 위치 | 선택된 의미의 완전한 구성으로 사용 |
| 원자료의 사례값 | S02의 색/문양/칼라/넥타이, S07의 가림 범위/끈, S16의 장비색 | 사례 재현 또는 명시 요청에서만 결합 |
| 선택 가능한 실현 | 특정 주름·반사 배치, 불안의 한 연기 예, 결로의 국소 패턴 | 작성 도움. 유일한 표정/재질 형상으로 강제하지 않음 |
| 범위/극성 guard | no blood, 기존 핏·슬릿 유지, OR 대안, noncontact, 부상 소유자 | 기존 requester/frozen-core 조건과 양립 검사 |
| 관찰 한계 | 숨은 패드, 실제 힘/속도/지속, 감정/동의, 법적 나이, 실제 재료 성능 | 설명/검증 메타데이터. 픽셀 PASS의 대체 근거로 사용하지 않음 |

현재 465개 atom의 `runtime_ready=false`와 `is_hard_obligation=false`를 유지한다. `직접 분해`라는 이름만으로 atom을 `authored_components`에 전부 복사하지 않는다. 36개 문맥 결합과 32개 해석 예시도 한 묶음 필수 profile로 등록하지 않는다. 원문에 색/도구/위치가 없는데 분해에서 구체화한 경우에는 사례 주장 또는 연구자 실현으로 표시한다.

P01–P11과 `new_original_source_read`는 참조 대화의 provenance 주장이다. 사례 replay나 hard alias를 채택하기 전에 실제 원자료의 해당 구간을 확보해 K010의 중앙 구조, K071의 치아, K114의 신발, K209/210의 타월·끈, K213의 기념물 위치를 우선 확인한다. 확인하지 못한 항목은 generic 관계 연구를 계속할 수 있지만 “원문/이미지 독립 인증” 상태로 승격하지 않는다.

## 3. 기존 데이터를 먼저 정확히 재사용하기

| 현행 항목 | 사용할 수 있는 부분 | 그대로 대체하면 안 되는 부분 |
|---|---|---|
| `y2kr_rib_tank` | 민소매 탑 표면의 반복 세로 니트 골 | 흰색/U목선/밀착/전체 층위가 자동 포함되지는 않음 |
| `sw_rib` | 수영복 패널의 골 relief 구분 | 다른 의복으로 바꾸는 데 domain/owner 검토 필요 |
| `vg_faille_crossgrain_ribs_profile` | 직물 표면에 붙은 가로 리브의 연속성 | 니트 세로 골의 alias로 합치지 않음 |
| `lace_trim_attached_edge` | 바탕 원단에 부착한 좁은 열린 셀 띠 | 밑의 피부 투과나 의복 전체 투명도를 보장하지 않음 |
| `satin_directional_luster_drape_surface` | 원단 경계/주름과 광택의 연속성 | 젖음·실크 섬유·원문 없는 드레이프 형상을 강제하지 않음 |
| `pfe_slit` | 두 마감 가장자리·하나의 연속된 다리·나머지 치마 | 원래 트임 시작 높이는 source/request 별도로 보존 |
| `pfe_one_shoulder` | 원래 한 어깨 지지 디자인 | 두 끈 중 하나가 흘러내린 현재 상태의 대체가 아님 |
| `water_rel_w159` | 타월 연속면·겹침·가장자리 접촉 | 양손으로 앞에 든 천의 전면 가림과 구별 |
| `head_eye_counterorientation_relation` / `pv_gaze_direct` | 머리 방향과 안구 목표 분리 | 모든 시선에 특정 정서·정면 머리를 부여하지 않음 |
| `rb_glass_reflection_transmission` | 특정 건축 유리의 반사/내부 읽힘 | 반대편 facade를 요구하므로 거울 초상/신체 접촉에 그대로 사용하지 않음 |
| `status_led_glow` | 기계 광원의 방향을 검토할 이웃 | 상태 LED와 공중 코드, 틈의 진홍 빛은 동일 의미가 아님 |

재사용 검토는 7개 VD 카드에서 수행한다. `EXISTING-ENTRY-REVIEW.json`에 native loader가 읽은 전체 항목을 보존했다. 표의 이름이 닮았다는 이유로 alias를 넓히지 않는다. 새로운 owner·material·object·action이 필요한 경우에는 독립 후보나 명시적 adapter 작업으로 둔다.

## 4. 실제 작성할 데이터와 순서

### 4.1 작은 pilot에 필요한 후보부터 작성

20개 후보 초안은 **13개 새 관계 trial + 7개 기존 항목 검토**다. 우선 VD-001/002/021/023/024를 작은 pilot 묶음으로 작성한다. 범용 구조와 사례 파라미터를 먼저 분리해 데이터 파일을 결정한다. 다른 후보/guard의 동시 대량 채택은 앞 단계 결과를 본 뒤 진행한다.

새 관계를 한 authored extension에 넣는다면 제안 basename은 `photo_prompt_vel_appearance_relations_extension.json`과 대응 visual-profile source다. 아직 존재하는 파일이 아니며 확정 경로도 아니다. 기존 clothing/water/visual-grammar 등의 source와 중복 범위를 검토해 최종 이름/구성을 정한다. 기존 의미의 동등한 확장은 소유 source에서 좁게 수정한다.

연구의 source_case/provenance 필드를 runtime candidate에 그대로 새 필드로 추가하지 않는다. 역사적 증거는 연구 디렉터리에 두고, runtime에는 현재 schema가 허용하는 positive concept units, directed relations, applicability, 완전한 effects, contextual limits만 번역한다.

### 4.2 모든 실제 효과의 property 범위를 해결

`RUNTIME-MAPPING.json`에는 현행 항목에서 읽은 dimension/target/property 모양과 추가 작업을 기록했다. 해당 anchor는 adapter의 예시이며, 새 관계의 완전한 effect를 인증한 것은 아니다.

- 베스트/타월: 의복 구조와 표면, 손/팔 배치, 가림을 바꾸는 범위를 함께 검토한다. appearance 하나만 적고 pose 변화를 숨기지 않는다.
- 신발–상대 접촉: 주체 A, 상대 B, 접촉 신발, 다른 지지 발, 바닥을 실제 actor/object에 바인딩한다. 상대의 속성을 `main_subject`에 억지로 저장하지 않는다.
- 눈과 머리: `head.orientation`과 `eyes.gaze_direction`을 나눈다. 카메라 높이/방향/초점은 camera 소유로 둔다.
- 발광: 기계 aperture 광원, 공중 기호, 금속 수신면과 color/lighting/material의 실제 변경 범위를 선언한다.
- 기존 잠금: 요청의 의상·피복·표정·손·카메라와 겹치는 effect가 잠겨 있으면 후보를 노출/선택하지 않는다. 명확한 요청 자체의 형상은 후보 미선택을 이유로 삭제하지 않는다.

새 관계를 표현하기 위해 명명된 후보나 인물 전용 parser 분기를 추가하지 않는다. 현재 generic actor/target/property 체계로 가능한지 먼저 검토하고, 부족하면 공유 adapter의 좁은 변경과 다른 도메인의 회귀를 함께 설계한다.

### 4.3 선택된 구성의 `authored_components` 작성

각 component는 실제 소유자·경계·관계와 minimum view를 담는다. 전체를 선택한 경우에만 all-of 구성으로 검증한다. broad 키워드의 exact alias가 완전한 형태 의무를 만들지 않게 한다. 다만 사용자가 직접 지정한 정확한 형상은 후보와 별도로 보존해야 한다.

예를 들어 VD-024에는 같은 타월 두 grab points, 중간 앞 가림, 뒤 의복의 작은 strap window가 있지만, generic held towel profile에는 산호색·허벅지 높이를 보편 필수로 넣지 않는다. 이 둘은 각각 source-case realization과 generic relation이다. VD-001도 특정 색을 빼고 허리 영역/상흉부 영역의 다른 layer relation을 작성한다.

generated `component_semantics`, `required_evidence_fields`, `evidence_requirements`, `render_gates`, `composition_instruction`을 연구 JSON에서 그대로 hand-edit하지 않는다. 현행 maintenance 계약에 따라 `authored_components`에서 canonical하게 파생한다.

### 4.4 source manifest와 인덱스 재생성

모든 후보/profile extension은 단일 `photo_prompt_source_manifest.json`에서 등록한다. load order·중복 ID·required-file 상태를 검사한다. authored source 검증 → canonical semantic/visual builders → deep index checks → runtime publication 순서로 수행한다.

벡터 재사용은 입력 텍스트 bytes, provider/model/dimensions와 recipe/policy hash가 모두 맞는 경우만 허용한다. 새 데이터나 recipe가 바뀌었는데 이전 vector를 ID만 보고 재사용하지 않는다. 기존 다른 작업의 generated index diff를 섞어 채택하지 않는다. 일반 live 요청이 stale index를 숨기려고 임의 재빌드하는 방식도 사용하지 않는다.

이 단계의 구현/배포는 이번 요청에서 실행하지 않았다. 실제 시작 시 격리 기준과 source revision 상태를 먼저 고정한다.

## 5. 작성·조회·선택 경로에서 반영할 규칙

새 연구를 일반 prompt 작성의 pre-core 템플릿으로 사용하지 않는다. 원래 요청의 상황·행동·대상·반응·결과를 독립적으로 읽고 core를 동결한 뒤, 필요한 표현 도움을 조회한다. 추가 데이터의 존재가 새 가림·신발 접촉·무기·정서를 발명할 권한이 되지 않는다.

32개 감정/역할 예시는 ordinary optional authoring 도움으로 남긴다. 추상 의미 자체는 머리 색·눈꺼풀 각도·고정 포즈·장소가 없는 의미 층으로 유지한다. 얼굴 하나를 자신감·동의·불안의 충분조건으로 exact 활성화하지 않는다.

6개 bundle은 선택형 메뉴다. “거울·결로·시선” 메뉴를 조회했다고 타월·레이스·젖음까지 추가하지 않고, “양손 타월·얼굴”을 선택했다고 몸에 두른 타월을 요구하지 않는다. 카드의 원자료가 다른 경우 출처/역할/연령 문맥을 섞지 않는다.

메뉴의 `card_ids`는 연구 카드 참조다. 실제 runtime bundle에는 후보 초안으로 번역된 멤버만 넣고, guard 카드는 문맥/검토 규칙으로 남긴다. 후보가 아닌 guard ID를 runtime member처럼 복사하지 않는다.

성적 문맥, 비성적 친밀감, 갈등, 실제 접촉, 부상 흔적은 원래 출처의 의미 층을 유지한다. 미성년/연령 혼용·미확인 출처의 비성적 액션/언쟁을 성인 관능성 예시로 재해석하지 않는다. 설명문의 성인 추정도 실제 연령 인증으로 바꾸지 않는다.

## 6. 회귀 검증 계획

`REGRESSION-PLAN.json`의 193개는 실행 예정 사양이다. 실제 코드 테스트를 작성할 때 현행 계약에 맞춘 fixture와 예상 결과를 확정하며, 계획 행 수를 통과 테스트 수라고 보고하지 않는다.

| 회귀 축 | 대표 대조 | 기대 결과 |
|---|---|---|
| 층/소유자 | 검정 베스트는 남지만 흰 탑 삭제 | source-case keeper 위반 |
| 실제 형상 | 골지↔평면 줄무늬, 고리↔원판 | 동의어 활성화 금지 |
| 상태 | 내려온 두 끈 중 하나↔원래 원숄더 | 현재 상태와 설계 구분 |
| 연결 | 양손이 서로 다른 타월을 잡음 | 같은 대상 관계 위반 |
| 가림 | 팔을 벌리자 중앙 타월이 열림 | positive coverage 유지 실패 |
| 접촉 | pressed↔near/reflected overlap | 근접/광학 이미지로 대체 금지 |
| 비접촉 | 손을 가려 gap를 통과 | 미관찰, 통과 아님 |
| 행위 단계 | 무장↔발사, lowered sword↔공격 | 준비/현재 상태의 확대 금지 |
| 색 원인 | no blood↔모든 빨강 삭제 | 광원/기호는 유지 |
| 논리 | wet OR clingy, choker OR armor | 대안을 all-of로 변경 금지 |
| 시간/계측 | steady pressure, slow draw, 1–2 mm | 정지/스케일 없는 관찰은 해당 수치 미점수 |
| 어휘/조회 | 부정 lingerie 토큰의 positive 검색 | 극성 firewall 유지 |
| 효과 잠금 | 타월 후보가 잠긴 손/몸/카메라 변경 | complete effects와 requester locks 재검사 |
| 외형 참조 | 고개 회전을 얼굴 재설계로 보정 | projection과 appearance redesign 분리 |

필수 계약 테스트는 actual source schema, exact contextual activation, owner/effect applicability, optional exposure, 선택된 literal evidence, composed/runtime receipt에 맞춰 실행한다. 의미가 똑같은 새 source를 넣어도 generator의 named branch 추가 없이 동작하는지 확인한다. anatomy plausibility는 agent-owned review를 유지하고 태그나 포즈 template로 대체하지 않는다.

## 7. native 픽셀 검증 계획

14개 평가군의 각각은 전 장면과 native 세부를 함께 검토한다. 핵심 pilot은 VD-001/002/021/023/024의 5군이다. 문구 표현 비교를 먼저 수행한다면 **5군 × 3문구 × 3반복 = 45장**을 계획한다. 현재 생성은 0장이다.

세 문구는 (A) 같은 뜻을 명시한 간결한 관계 표현, (B) 참조 외형 분해의 의미 약화/과잉을 수정한 표현, (C) 소유자·부착·가림을 강화한 표현이다. A도 필수 뜻을 누락한 막연한 라벨만으로 만들지 않는다. 원래 분해의 알려진 약점을 그대로 둔 별도 스트레스 실험은 이 비교와 섞지 않는다.

각 문구의 baseline이 달라지면 core hash도 다를 수 있다. **한 frozen core를 유지한 runtime A/B라고 주장하지 않는다.** 각 arm은 자기 요청을 독립적으로 동결하고 인원/성인 설정·의상/소재·노출/가림·행동·부정 범위가 의미상 동등한지 먼저 검토한다. 동일 provider/model/version/크기/참조 범위를 기록하고, provider가 지원할 때만 seed를 통제한다. 매 이미지의 prompt/core/receipt hash를 보존한다.

이 비교는 문구 실현 가능성 검증이다. 후보 데이터의 실제 효과를 주장하려면 별도 실험에서 동일하게 확인된 frozen 요청과 compatible open properties를 사용해 이전/이후 source/index generation, 노출, 상세 읽기, 선택, 최종 literal 표현을 기록한다. 어느 arm이 required preflight를 통과하지 못하면 비용을 써서 이를 성공 이미지로 비교하지 않는다.

모든 선언된 owner/component/relation이 있어야 통과다. 예컨대 타월은 양손 지지와 중앙 가림, 고리는 열린 구멍과 부착, 유리 접촉은 실제 접촉 패치를 모두 요구한다. 세부만 있고 전체 관계가 틀린 경우도 실패다. 부분 실현은 실패, 전달 이미지 없음/blocked/가려 확인 불가는 미점수다. 압력/속도/시간은 해당 증거가 없으면 따로 미점수로 남긴다.

세 반복은 작은 pilot이며 모집단 성공률이나 모든 장면 우월성의 근거가 아니다. 결과가 충분할 때만 나머지 9군, 다언어 holdout, 다른 소재/포즈/소유자·상호작용으로 확장한다.

## 8. 단계별 산출물과 상태

| 단계 | 산출물 | 현재 상태 | 다음 단계 진입 조건 |
|---|---|---|---|
| 원본/후속 분석 정합성 | 원본 두 첨부·217행/465atom·SHA·대조표 | 완료 | 기존 8 필드/극성/출처 보존 |
| 근거와 관계 설계 | 28카드·20후보 초안·6메뉴·46메모 | 완료 | source-case/optional/claim guard 분리 |
| runtime adapter 및 authored data | 13trial/7review의 실제 schema/effects | 미실행 | 전체 owner/effect/locked-property 매핑 |
| source/index/publication | scoped diff·manifest·canonical builds | 미실행 | 검증된 source revision 및 깊은 인덱스 검사 |
| 조회/선택/문장 검증 | bound pack·상세 조회·선택·composed/runtime audit | 미실행 | required intent 유지·실제 노출/선택 기록 |
| 픽셀/사용자 평가 | native 결과와 gate별 판정 | 미실행 | 사전 고정된 조건·관찰 범위의 증거 |

이번 완료는 추가 리서치와 반영 가능한 설계의 완성이다. 코드/active 데이터 변경, 인덱스 배포, live pack, 이미지, commit/push/PR은 수행하지 않았다. 연구 구조 검증 결과는 [VALIDATION.json](VALIDATION.json)에 기록한다.
