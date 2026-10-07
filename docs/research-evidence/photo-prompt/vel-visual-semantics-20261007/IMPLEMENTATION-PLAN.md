# vel 리서치 반영 계획

작성일: 2026-10-07 (Asia/Seoul)  
현재 상태: 계획·초안. 0개 런타임 파일 변경, 0회 인덱스 재생성, 0회 이미지 생성.  
핵심 자료: [연구 결과](RESEARCH.md), [60개 카드](SEMANTIC-CARDS.md), [파일 매핑](RUNTIME-MAPPING.json).

**추가 외형 분해 반영:** 실제 채택 시 [후속 구현 계획](appearance-decomposition-followup/IMPLEMENTATION-PLAN.md)을 함께 적용한다. 기존 60개 의미를 28개 관계 카드로 세분화하고 13개 새 관계 trial·7개 재사용 검토를 제안했다. generic 구조·원문 사례값·선택 예시·부정 조건·관찰 한계를 먼저 분리하며, 기존 raw 연구 데이터와 초기 검증은 변경하지 않는다.

## 1. 목표와 채택 기준

목표는 원문 표현의 **상태·정도·소유자·관계가 보존된 후보를 찾고 선택할 수 있도록 하는 것**이다. 단어 수, alias 수, 검색 이웃 수, 한 장의 미적 선호만으로 강화 완료를 판정하지 않는다.

| 완료 단계 | 필요한 근거 |
|---|---|
| 데이터 무결성 | 출처/owner/효과/관계/부정 범위가 일관되고 현행 validator 통과 |
| 검색 발견 | 동등 의미의 자연어에서 후보 노출; 인접 의미와 부정 요청의 경계 유지 |
| 후보 채택 | frozen-core/intent-lock/연령/노출/정체성/사건 정도와 호환 |
| 프롬프트·runtime binding | 선택 후보와 증거·target/property·negative-intent가 현행 audit를 통과 |
| 이미지 기술 검증 | 원래 크기에서 선택한 필수 관계의 모든 gate가 관측됨 |
| 사용자 판단 | 실제 사용자가 요청 의미·선호·개선 여부를 판단 |
| 일반적 강화 주장 | 선언한 비교군과 반복에서 재현되는 개선; 검색·기술 audit만으로 대체 불가 |

조사 중 현재 authored corpus는 98개 source, 10,500개 slot entry, 2,290개 profile이었다. 반영 시점에 다시 캡처한다. 현재 primary의 미반영 변경을 제외한 HEAD만 사용하면 연구가 본 데이터와 달라질 수 있다.

## 2. P0: 출처·부정·정도·소유자 경계부터

### 배치 A — 기존 경계 확인과 필요한 데이터 보완

대상: VEL-047/049/058/059/060 및 원본 K189–K217.

1. 20개 부정 지시를 연구 provenance와 개발 fixture에 남긴다.
2. `no blood` / `no gore`가 허용된 전투·무장 의미를 지우거나 피의 긍정 증거를 만들지 않는지 확인한다.
3. `不要血腥`, `不要殺戮場面`, `rather than`의 범위와 negative-list 출처를 보존한다.
4. anatomy-defect의 `broken wrists`, `dislocated shoulders`를 원하는 injury와 분리한다.
5. 붉은 machine light/code particles, bandage motif, 얼굴 lock, adult 조건을 수위·피해·동의의 증거로 사용하지 않는다.
6. current generic contracts에 이미 정상 지원되면 구현을 추가하지 않는다. 재현 가능한 실패가 있을 때 positive 의미 또는 공통 데이터 경계를 고친다. 토픽별 문자열 치환·새로운 safer-meaning router를 만들지 않는다.

완료 조건: 현행 의미 권위를 유지하는 paired positive/negative/context tests. 원래 가림·노출·action을 연구자의 선호로 바꾸지 않는다.

### 배치 B — 재사용 가치가 큰 기존 관계

우선 카드: VEL-003/008/009/010/016/027/033/031.

- 슬릿: `pfe_slit`, `pfe_slit_candidate`.
- 새틴: `satin_directional_luster_drape_surface`, `y2kr_satin`.
- 레이스 트림: `lace_trim_attached_edge`, `lace_trim_edge`.
- 목선: `decolletage_neckline_exposure`와 `pfe_cleavage`의 별도 경계.
- 젖은 머리: `wet_damp_clumped_hair_state`, `hr_wet_hair_skin_contact`.
- 무릎 자세: tall/heel/half-kneel의 서로 다른 지지 구조.
- holstered: 현재 물건·소지 후보의 상태 관계.
- 얼굴과 의복 특징 공동 가독성: `pfe_face_garment`.

동등한 뜻이면 기존 entry의 등가 paraphrase/context만 보완한다. 다른 소재·행동·object·owner·필수 조건이면 별도 variant다. 기존 가방 chain이나 성인 assault profile을 일반 의상 chain/학생의 비성적 제압과 동일시하지 않는다.

기존 opaque-lace/opaque-fit variant를 재사용하는 경우 그 선택된 variant의 의무는 유지한다. 그 조건을 일반 lace/satin/fitted의 전역 기본값으로 복제하지 않는다.

## 3. P0 관계 trial: 여섯 대비군의 일곱 카드

| 우선 군 | 카드 | 추가할 정확한 관계 | 인접 의미·실패 |
|---|---|---|---|
| 한쪽 끈 위치 | VEL-012 | 해당 shoulder 아래의 같은 garment strap과 두 attachment | designed one-shoulder, bag strap, 추가 노출 |
| 원단 상태 | VEL-014/015 | wet region / contact-tension / transmission 각각의 owner | wet→자동 투과, glare→비침, 체형 변경 |
| chain/ring | VEL-021 (020과 비교) | 실제 attachment와 연속 link·처짐 | floating chain, 장식→구속 |
| 몸-침구 | VEL-024 | 같은 접촉부의 지지·국소 눌림·연결 주름 | 다른 위치의 임의 주름, levitation |
| 비접촉 갈등 | VEL-043 | speaker/listener와 hand-face의 열린 간격 | 질책→타격, emotional wounded→상처 |
| 국소 흔적 | VEL-047 | mark substrate·범위·독립 신체 연속성 | smear→gore, red light→혈흔 |

각 trial은 새 후보 ID를 즉시 확정하기 전에 기존 entry 전체와 의미·전제·효과를 비교한다. 원래 24개 new-relation 카드 중 나머지는 이 배치의 결과와 겹침을 확인한 후 진행한다. 연구 카드를 그대로 대량 import하지 않는다.

## 4. 실제 데이터 형식과 반영 위치

[46개 초안](CANDIDATE-DRAFTS.json)은 22개 재사용 검토와 24개 새 관계 trial이다. `runtime_ready=false`이며 실제 distributable schema로 검증되지 않았다.

새 후보의 최소 정보:

- 같은 의미의 영어/한국어 표현과 좁은 문맥;
- 어떤 물건·부위의 속성인지 나타내는 `concept_units`;
- 방향을 보존하는 `relations`의 subject/type/object;
- 정확한 `affected_dimensions`와 실제 target/property;
- 필요한 전제와 적용 guard;
- 선택 시 요구되는 가시 증거와 혼동 반례.

예: VEL-012의 연구 projection은 다음처럼 잡을 수 있다. 아래 target/property는 장면에 맞게 검증해야 하는 제안이다.

```json
{
  "id": "vel_relation_012",
  "slot": "garment_detail",
  "concept_units": [
    "one selected garment strap lies below its own shoulder crest",
    "the same strap remains attached to the garment front and rear",
    "the opposite side retains its independently declared state"
  ],
  "relations": [
    {
      "id": "selected_side",
      "type": "lies_below",
      "subject": "selected garment-owned strap",
      "object": "same-side shoulder crest"
    }
  ],
  "affected_dimensions": ["appearance"],
  "affected_properties": [
    {
      "dimension": "appearance",
      "target": "main_subject",
      "property": "clothing.strap_state"
    }
  ]
}
```

`side`, garment identity, attachment와 final-context 전제가 binding돼야 한다. 이 projection만으로 새 broad exact activation이나 후보 채택을 허용하지 않는다. 노출 범위·반대쪽 strap·핏·대상 연령의 변화는 이 후보의 허가된 효과가 아니다.

| 데이터 군 | 기존/제안 경로 |
|---|---|
| 핏·슬릿·목선·strap·wet cloth | 기존 `photo_prompt_portrait_fashion_exposure_extension.json` 및 해당 visual obligations |
| 코르셋형 seam | 기존 clothing structure source; historical/bustier 의미와 먼저 비교 |
| 장식 attachment | 기존 accessory structure source; object-owner별 variant |
| 거울 김·젖은 표면 | 기존 water relations source; camera/scene/glass 층 구분 |
| 일반 소지·접촉·지지·비접촉 간격 | 제안 `photo_prompt_interaction_state_extension.json` + corresponding visual obligations |
| 효과 충돌·파손·국소 흔적·glass contact | 제안 `photo_prompt_scene_state_relations_extension.json` + corresponding visual obligations |
| 추상 정서·시간·내부 기능 | 연구 기록/창작 지침/claim limit; 형태 prototype으로 옮기지 않음 |
| 부정·identity·연령 | existing generic contract/현재 request grounding; 새로운 토픽 router 아님 |

위 파일 이름의 기존 여부와 실제 source는 [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)에 남겼다. 제안된 신규 source 네 개는 아직 만들지 않았다. 기존 source가 더 정확하면 새 source pair를 만들지 않고 소규모 보완한다.

Visual profile이 필요하면 current `photo-authored-visual-components/v2` compiler 경로로 작성한다. component group, required evidence field, render gate를 연결하고 새 `vo_*` gate ID 충돌을 검사한다. 기존 profile을 선택하면 그 profile의 모든 gate를 보존한다.

`low neckline`, `wet`, `weapon`, `kneeling`, `blood` 같은 broad term을 새로운 단독 hard exact activation으로 등록하지 않는다. 좁은 관계의 hard activation은 문맥 양성/부정 근거가 확보된 경우에만 별도로 검토한다.

## 5. 후보팩 조합과 provenance

12개 bundle draft는 **선택형 조합 메뉴**다. 목록 전체가 자동 필수라는 뜻이 아니다. 예를 들어 holstered/held/partly-drawn은 하나의 무기에 동시에 적용할 상태가 아니라 별도 대안이다. 선택된 멤버들만 같은 owner·event·core 의미에서 공존하도록 조합한다.

normal v6의 순서를 유지한다.

1. 현재 요청·control과 독립적인 전체 장면을 작성하고 core를 동결한다.
2. frozen core로 slot retrieval/visual resolution을 실행한다.
3. 후보의 실제 전제·owner·효과를 확인한다.
4. 선언된 open dimension 안에서만 선택·구체화한다.
5. 채택한 후보의 evidence/obligation을 final prompt에 바인딩한다.
6. compose/audit와 image review를 각각 기록한다.

연구 source URL, source title, raw prompt, 대량 K vocabulary, private score/rank/vector는 public candidate 의미로 보내지 않는다. 원본 K ID와 외부 R ID는 `docs/research-evidence/photo-prompt/`의 evidence linkage에 보존한다.

`candidate-pack/v6`의 공개 스키마 변경, pre-core keyword 분기, 새 semantic safety enum, retired metadata 복구는 이 데이터 강화에 필요하지 않다.

## 6. source manifest와 인덱스

채택이 결정된 작은 authored batch에서만 수행한다.

1. 반영할 원본 JSON과 loader/contract의 현재 hash를 다시 기록한다.
2. 필요한 source만 ordered `photo_prompt_source_manifest.json`에 등록한다.
3. 현재 generation/manifest 계약에 맞는 cooperative build를 사용한다. 진행 중인 다른 writer를 우회하거나 무관한 shard를 삭제하지 않는다.
4. semantic text와 BM25F projection을 현재 recipe로 다시 생성한다.
5. visual profile registry가 바뀌면 visual-profile index도 다시 생성한다.
6. provider/model/dimensions/exact text/hash가 모두 같은 vector만 재사용한다. 새 의미 text는 새 embedding이 필요할 수 있다.
7. source/registry/dictionary/text/policy/shard hash 불일치가 남으면 정상 검색 성공을 주장하지 않는다.
8. generated index나 historical proof를 손으로 수정하지 않는다.

과거 bundle/baseline가 full source hash에 묶인 경우 원래 source와 증거를 보존한다. 새 의미가 바뀌면 검토된 successor를 만들고 leaf delta와 parent proof를 남긴다. 과거 PASS 파일의 checksum을 새 데이터에 맞춰 덮지 않는다.

## 7. 검증 실행 순서

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)은 462개 개발 사양이며 아직 실행하지 않았다. 무결성 검사와 semantic regression의 성공을 구별한다.

### 데이터·검색

- dictionary/registry와 compiler validation;
- 기존 의미·ID·활성 alias·gate 유지;
- native positive-field projection에서 actual limitations/contrast/source prose가 positive prototype으로 유입되지 않음;
- 한국어/영어 자연 paraphrase 양성, 부정 범위, 다의어·인접 형태 음성;
- Chinese negative examples와 negative-list provenance;
- 같은 소유자·wrong-owner·target reversal;
- candidate 발견과 hard activation의 구별;
- untagged discovery, zero adoption, missing final premise, locked-context conflict;
- 새로운 데이터로 holdout을 수정해 실패를 숨기지 않음.

### 후보팩·프롬프트

하나의 pinned source generation과 요청 envelope/core/control/hash로 후보팩을 실행한다. 유효 의미 수정이 필요한 경우 envelope/core/pack를 함께 다시 작성한다. 비교 실험의 두 arm은 의미를 동일하게 유지한다.

노출된 후보 ID, 채택/거절 근거, property target, selected gates, final prompt literal evidence, runtime request audit를 기록한다. 검색이 되었다는 이유로 선택 성공·픽셀 성공을 보고하지 않는다.

관련 기존 suite의 시작 후보는 portrait fashion exposure, clothing/accessory structure, pose vocabulary, acting expression, water relations, violence/crime, candidate semantics, composed prompt 및 prop conditional contact다. 실제 수정 면에 해당하는 focused suite부터 실행하고, 새 실패나 넓은 regression 우려가 있을 때만 확대한다. 연구 문서만 작성한 이번 단계에서 이 suite들의 PASS를 주장하지 않는다.

### native pixels와 사용자 판단

18개 대비군 중 PX01/PX03/PX06/PX07/PX11/PX15가 우선 여섯 군이다. 계획 수는 2 arm×3 반복×6군=36장이다. 이 연구에서는 생성 비용과 API 호출이 발생하지 않았다.

- model/provider/version, 실제 control snapshot, core/hash, reference scope, prompt/negative, seed가 노출되면 seed를 기록;
- 가능한 경우 같은 seed로 비교하되 byte-identical 이미지나 완전한 통제를 보장하지 않음;
- 고정된 native 원본을 보고 identity, owner, support, contact/gap, attachment, requested degree를 all-of 검사;
- 평가 순서와 arm 표시를 가리고 source label을 보지 않는 평가를 계획;
- 미관과 관계 정확도를 따로 기록;
- 선택된 관계의 일부만 읽히면 whole-scene PASS 불가;
- pressure·duration·hidden padding·actual consent·medical diagnosis를 gate로 인증하지 않음;
- 생성 차단은 BLOCKED_UNSCORED로 기록하고 우회하거나 조용히 의미를 바꿔 재시도하지 않음;
- 최초의 모든 필수 gate PASS 뒤 사용자 판단을 따로 받음.

이후 계획된 군의 확대는 처음 여섯 군의 미해결 결과와 다음 배치의 새 의미에 맞춰 결정한다. 36장 계획 자체가 자동 생성 권한이나 성공 보장은 아니다.

## 8. P1/P2와 보류

P1: 정리된 source 경계를 바탕으로 나머지 관계 trial을 검토한다. 반사 시선·손-머리·효과 원점/충돌·파손 owner·일어나기 support·glass-plane contact가 중심이다.

P2/claim hold: 숨겨진 패드의 실제 구조, 재장전의 미관측 단계, 지속 압력, partial armor의 보호 성능, 실제 샤워 이력, 명령의 정확한 대사, 항복의 진위, 피해의 진단·원인·책임. 이러한 의미를 삭제하지 않고 적합한 evidence layer에 둔다.

연령 미확인·학생·15세·teen/young adult 혼용 원 source는 성적 enrichment/replay의 씨앗으로 사용하지 않는다. 비성적 액션·언쟁·기하 관계의 분석과 보강은 가능하다. 후속 qualification은 original replay와 독립적인 fictional case임을 명시한다.

## 9. Git와 전달

실제 구현 때는 해당 세션의 active worktree와 source state를 먼저 확인한다. 현재 미반영 authored work를 몰래 제외하거나 새로운 worktree에 무조건 HEAD만 복사하지 않는다. 기준이 승인된 current snapshot인지 clean commit인지 명확히 정하고 필요한 파일만 checksum으로 비교한다.

제안 branch prefix는 `codex/`다. 실제 branch 생성·commit·push·PR·merge는 이번 연구에서 수행하지 않았다. 구현 배치의 authored JSON, manifest, regenerated indexes, 해당 tests와 evidence만 선택적으로 stage한다. 진행 중인 unrelated 파일을 reset/revert/stage하지 않는다.

## 10. 연구 패키지 재검증

아래 명령은 이번 연구 패키지의 연결·원본 보존·출처·draft 상태만 검사한다. 런타임 자격이나 이미지 품질 테스트가 아니다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/validate_research.py
```

자료를 다시 조립할 때는 현재 coverage snapshot과 reviewed card를 사용한다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/build_research_artifacts.py
```

현재 corpus 대조를 다시 실행하면 baseline이 달라질 수 있다. 기존 완료 snapshot을 먼저 보존하고 fresh snapshot으로 실행해야 하며, 역사적인 연구 결과를 같은 이름으로 덮어 새 결과처럼 제시하지 않는다.
