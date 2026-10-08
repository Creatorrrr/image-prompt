# 불 시각 의미·후보 데이터 반영과 독립 이미지 검증

2026-10-08 KST. 현재 작업 폴더에 실제 데이터를 반영하고, 사용자 제공 사진으로 독립된 세 서브에이전트가 프롬프트와 이미지를 만들었다. 세 장면 모두 불과 화원의 관계가 보였다. **기록된 필수 gate는 19/19 통과**했으며, 추가로 검사한 **얼굴빛의 화원 귀속과 실내 연기 경로는 실패 또는 관측 불충분**했다. 현재 데이터 관련 테스트 35개는 통과했지만, 전체 회귀 실행의 실패 22개 모듈은 해결되지 않았다.

## 반영된 데이터

| 대상 | 실제 반영 | 활성 원본 |
|---|---:|---|
| 신규 후보 | 127개, 20개 슬롯 | [fire relations 후보](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_fire_relations_extension.json) |
| 기존 후보 맥락 | 4개 ID 재사용, 의미·효과·소유 관계 유지 | 같은 후보 원본의 `existing_slot_context_extensions` |
| 시각 의미 프로필 | 131개, `authored_components/v2` | [fire relations 시각 의미](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_fire_relations.json) |
| 원본·관계 검사 gate | 521개 | 선택된 프로필의 전체 duty를 composition/runtime/review에 연결 |
| 비시각 맥락 | 24개 제외 | 온도·원인·과정·진단·동기 등을 픽셀 의무로 등록하지 않음 |
| 소스 등록 | candidate order 60, profile order 42, 모두 required | [source manifest](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json) |

광학 플레어 세 개(`pe_veiling_flare`, `pe_aligned_ghosts`, `pe_horizontal_anamorphic_streak`)와 `coronal_mass_ejection_observation_subject`는 기존 ID를 재사용했다. 모든 기존 후보를 현재 전체 로더와 fire 제외 로더로 비교하여, 이 네 ID의 paraphrase/context 추가를 제외한 기존 필드가 그대로임을 검사했다. 광학 효과를 공간의 불티·연기·새 광원으로 바꾸지 않았다.

화염, 발광하는 고체, 분리 입자, 연기, 표면 검댕, 빛을 받는 면, 수면 반사, 굴절하는 공기, 카메라 영상면을 각각 다른 owner/property로 선언했다. 머리·피부·의복 효과는 기존 `main_subject`의 실제 property에 연결하고, 의복 손상에는 coverage까지 포함했다. 잠금 우회를 검사하되 선언의 문법적 유효성과 실제 장면의 물리 관계를 구별했다.

각 프로필의 전체 세 요소는 연구자가 설계한 **선택적 실현**이다. 광범위한 `불`, `flare`, `corona`, `열` 같은 용어가 자동으로 특정 연출을 강제하지 않는다. 좁은 전체 proposition만 exact activation을 가질 수 있고, 자연 문장·유사 검색은 선택 가능한 후보 발견으로 남는다. 원래 연구의 창작 형태 일곱 개도 선택적 표현이며, 과학적 정의로 승격하지 않았다. 관측 채널·화원 위치 같은 비가시적 메타데이터는 native 픽셀 gate로 만들지 않았다.

155개 연구 카드의 채택 여부·candidate/profile ID·소유 관계·출처는 [ADOPTION-LEDGER](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/ADOPTION-LEDGER.json)에 있다. 연구의 7개 bundle 초안과 44개 회귀 계획 전체, 10개 pixel 계획 전체를 실행 완료한 것으로 주장하지 않는다. 이번 요청에서는 활성 후보/프로필, 직접 관련 회귀 검사와 아래 세 실용 장면을 수행했다.

출처 42개의 접근 수준과 인용 한계는 [원래 출처 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/SOURCES.json)에 남겼다. 전체 본문을 보지 못한 검색 발췌를 전체 논문 검토로 해석하지 않는다. 참조 대화의 제한된 반환 범위도 [기존 조사 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/RESEARCH.md)의 한계를 그대로 유지했다. 처음 조사한 27개 산출물의 SHA는 모두 동일하며, `research_only`였던 과거 기록을 현재 구현 완료 상태로 덮어쓰지 않았다.

## 최신 스킬과 독립성

[최신 photo-prompt-image-generator SKILL](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 SHA는 `503f03f5ba8fb65181071858e93f17123223e40964c54e27ff8314b2bce948d0`이다. 이 작업에서 SKILL과 중립 controls/catalog를 수정하지 않았다. 세 에이전트는 `fork_turns=none`의 별도 문맥에서 시작했고, 다른 arm의 프롬프트·후보·이미지를 사용하지 않았다.

컨셉의 다양성을 위해 공예, 야외 화원, 생활 공간이라는 넓은 분야만 배정했다. arm 1과 arm 3은 그 안에서 독립 자유 선택으로 복잡한 장면을 만들었고, arm 2는 네 야외 옵션 중 난수로 골랐다. 세 난수 seed를 통제한 실험이나 통계적 무작위 비교라고 부르지 않는다. 각각의 선택 방법은 TESTCASE에 기록했다.

사용자 원문과 각 요청 envelope를 구분하여 보존했다. envelope는 에이전트 시작 후, 각 core freeze 전에 준비되었다. agent가 만든 구체적 테스트 요청을 사용자 인용으로 바꾸지 않았다. 후보·프로필·연구 자료를 보기 전에 기본 프롬프트, controls, feature selection, embodiment, authorial core를 freeze하고, 그 뒤 새 데이터 generation을 조회했다.

첨부 사진 SHA는 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 참조 범위는 얼굴의 보이는 비율과 검은 짧은 단발·가느다란 앞머리이며, 의복과 장소는 새로 구성했다. 실제 나이·인물 정체성은 판정하지 않았다. 세 arm의 frozen control은 sensual 1, fetish 0, surreal 0, creativity 1이었다.

## 실제 이미지와 데이터 기여

총 **native imagegen 호출 3회**, arm마다 한 번이다. 이미지 재생성·API fallback·기본 프롬프트 비교 렌더는 0회다. 실제 native 모델 식별자는 반환되지 않았으므로 모델명을 추정하지 않는다. 원본, byte 동일 프로젝트 복사본, ledger, manifest, 실패 입력과 회복 기록을 보존했다.

| arm과 장면 | 실제 선택한 신규 데이터 | 기록된 필수 gate | 추가 원본 픽셀 판정 |
|---|---|---:|---|
| 1: 비 오는 유리 공방에서 목걸이의 마지막 구슬 제작 | `fire_f012`, `fire_f033` | 5/5 embodiment | 6/6 추가 검사 PASS. 노즐→파란 화염→주황 유리 구슬과 차가운 목걸이 구슬의 구별이 보임 |
| 2: 비바람 속 해안에서 바람막이를 잡고 주전자를 가열 | `fire_f005`, `fire_f037`, **`fire_rel_f002` 전체** | 9/9: fire profile 4 + embodiment 5 | 7/9 추가 검사 PASS. 연료·화염·공극·분리 고체 형태는 확인. 얼굴빛의 단독 화원 귀속과 가로형 석호 장면은 FAIL |
| 3: 정전된 숙소에서 낮은 화덕 조리 단 곁의 귀가 후 휴식 | `fire_f096` | 5/5 embodiment | 6/7 추가 검사 PASS. 연속 벽돌 구조→같은 화구→그 위 주전자 관계는 확인. 화구→굴뚝 연기 경로는 FAIL |

필수 gate 19개 중 15개는 인체·접촉 embodiment, 4개는 이번에 추가한 F002 시각 프로필이다. **521개 전체를 렌더 검증한 결과가 아니다.** arm 1과 arm 3에서는 신규 fire 시각 프로필이 후보팩에 노출되지 않았으며, 일반 후보의 선택과 기여만 확인했다. arm 2에서는 신규 profile 네 개가 노출되어 F002 하나를 전체로 선택했다. profile 발견 범위는 제한적이다.

세 독립 baseline은 이미 불·화원·행동을 포함했다. 후속 데이터는 아래 literal 추가를 만들었고 실제 출력에서 해당 관계를 검사했다. 데이터 없이 만든 별도 이미지는 없으므로, 성공한 픽셀이 새 데이터 덕분에 개선됐다는 **반사실적 인과 효과는 입증하지 못했다.**

- arm 1: 화염 가장자리 양옆의 어두운 공기, 황동 노즐과의 연속 기반, 파란 화염과 황동·흑연의 서로 다른 물질색.
- arm 2: 노출된 나무 표면에 붙은 복수 화염과 공극, 원래 연료와 공기로 분리된 검은 중심/주황 가장자리의 고체 조각, 주전자·얼굴의 화원 쪽 빛.
- arm 3: 낮은 화구를 감싸는 연속 벽돌과 **같은 화구 바로 위** 주전자의 지지 관계.

### arm 1

[테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-1/TESTCASE.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-1/prompt-final.txt) · [전체 실행 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-1/RESULT.json) · [픽셀 추가 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-1/pixel-review-supplemental.json)

![유리 공방 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-1/render-001-original.png)

1536×1024. 노즐에서 구슬로 이어지는 파란 화염, 한 인물이 소유한 두 손과 연속 mandrel, 차가운 완성 구슬이 한 프레임에서 구별된다. agent가 계획한 좌우 손 배치는 뒤집혔으며, 연습 구슬의 특정 균열은 확실하게 보이지 않는다. 필수 주제 관계를 지우지 않는 부가 연출 차이로 기록했다.

### arm 2

[테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-2/TESTCASE.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-2/final_prompt_en.txt) · [전체 실행 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-2/ARM-RESULT.json) · [픽셀 추가 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-2/SUPPLEMENTAL-PIXEL-REVIEW.json)

![해안 화로 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-2/initial-native.png)

1237×1272. 나무 연료와 고체 잔불, 여러 화염 혀와 공극, 바람막이 손 접촉, 주전자 수증기와 연료 쪽 연무, 금속과 젖은 돌의 국소 따뜻한 빛이 보인다. 얼굴에는 위쪽 보조광과 금색 수평선도 있어 F037의 얼굴빛을 화로에만 귀속할 수 없다. 요청한 가로 프레임/고요한 석호도 구현되지 않아 **전체 agent 테스트케이스는 부분 실패**다. 이를 F002 전체 profile gate 통과와 구별했다.

### arm 3

[테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-3/TESTCASE.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-3/final-prompt.txt) · [전체 실행 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-3/DELIVERY.json) · [픽셀 추가 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-3/supplemental-pixel-review.json)

![실내 화덕 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/image-tests/arm-3/generated-images/attempt-1-native.png)

1448×1086. 같은 벽돌 화덕의 낮은 화구와 그 위 주전자, 장작에 붙은 화염, 아래 고체 잔불과 재, 두 손의 잔 접촉이 보인다. 컵·주전자 증기는 보이지만 화구에서 굴뚝 목으로 가는 별도 연기 경로는 확인되지 않는다. 증기를 연기로 대체하여 통과시키지 않았다. 주전자의 추가 nesting rim도 뚜렷하지 않다. **전체 agent 테스트케이스는 부분 실패**다.

각 에이전트가 저장한 원본과 축소본을 검사했고, coordinator도 세 원본과 whole-frame 축소본을 직접 재검사했다. [coordinator 원본 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/COORDINATOR-PIXEL-REVIEW.json)을 따로 남겼다. review-audit의 PASS는 기록 형식·바인딩 검증이며, 자동 시각 판독이나 사용자의 취향 판정이 아니다. 사용자 수락은 세 arm 모두 `pending`이다.

## 테스트 중 발견하여 고친 부분

선택된 시각 프로필이 있는 arm 2의 managed render 준비가 `effective_visual_contract_sha256` 누락으로 중단되었다. `photo_workflow.py`에서 composition 감사가 이미 바인딩한 hash만 render request로 넘기도록 두 줄을 추가했다. caller가 hash를 주입할 수 없고, 실제 pinned runtime auditor가 전체 계약을 재계산하여 검증한다.

native bridge는 shell 명령이 session ID를 반환했을 때 작업 완료 전의 부분 출력을 최종 실패로 취급했다. `photo_native_bridge.py`에서 같은 session의 완료까지 출력 조각을 모은 다음 exit code/JSON을 확인하도록 수정했다. image call은 완료 후 한 번만 실행한다. 새 transport 검사 4개에는 stale/null hash, caller injection, exec session yield 및 실패 시 0회 호출을 포함했다. 실제 arm 2의 긍정 경로도 별도로 통과했다.

이미지 도구가 반환한 파일 경로의 로컬 파싱, null review placeholder, ledger 원본 경로와 복사본 경로의 불일치, 기존 ledger에서 독립 manifest를 만드는 조정도 있었다. 각 실패 기록을 남기고 공식 helper로 일치시켰다. image tool 성공 후 같은 그림을 얻기 위해 다시 호출하지 않았다.

arm 3이 선택하지 않은 `fire_f097`은 설명의 ‘같은 fire bed’와 graph의 ‘forge’ endpoint가 충돌했다. 최종 primary에서는 endpoint와 대응 owner gate를 `declared_fire_bed`로 고쳤다. [F097 수정 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/BELLOWS-OWNER-CORRECTION.json)은 이전 maintenance record를 체인으로 유지한다. 슬롯·tag·alias·effect·baseline·이미지는 바꾸지 않았다. 이 후보는 선택·렌더되지 않았으므로 **수정된 F097의 이미지 성공은 주장하지 않는다.**

10월 1일 광학 소유 정리의 고정 검사는 이번 fire 맥락까지 읽어 exact 비교가 깨졌다. 고정 SourceInventory에서 이 후속 extension만 제외했고 기존 41개 exact 행·13개 수정 계획 검사를 그대로 유지했다. 신규 fire 회귀 검사는 현재 전체 로더에서 모든 기존 후보와 네 추가 맥락을 별도로 비교한다. 과거 expected row를 새 데이터로 덮어쓰지 않았다.

## 인덱스·런타임·보존

최초 반영에서 의미 인덱스 **10,567→10,694**, profile 인덱스 **2,321→2,452**로 증가했다. 동일 텍스트의 기존 의미 vector 10,563개와 기존 profile vector 2,321개는 전부 값이 동일하다. 신규 127개+기존 재사용 ID의 새 텍스트 4개+신규 profile 131개에만 새 입력이 필요했다. Gemini / gemini-embedding-2 / 768을 유지했고 batch 1을 사용했다. primary에는 동일 입력·동일 공간의 검증된 worktree cache를 사용했다. [최초 vector 재사용 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/VECTOR-REUSE.json)

F097 마지막 수정에서는 의미 vector 한 개만 다시 필요했다. 나머지 의미 **10,693개**, profile **2,452개 전체**의 텍스트·vector는 첫 통합 상태와 동일하다. source hash는 새 관계를 반영하도록 갱신했다. [F097 이후 vector 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/VECTOR-REUSE-AFTER-BELLOWS.json)

세 이미지가 사용한 데이터 generation은 `c37f392d21d2e87e34206b465cc718e5ce60db2a55ed72e560a4694dc56f417f`로 고정되어 있다. 최종 primary의 별도 generation은 `eb386a017d86c6ecf09ebc1ccb6eaeabec7c9c02b5ad2d43ad5972f81cc357d8`이고 fingerprint는 `4b592c69b5bc4413f11e77ab7cd3ce72b553ed5f892bf66d81baa71cd5209d7c`이다. image pack/receipt/manifest를 사후 수정해 이 최신 generation을 사용한 것으로 바꾸지 않았다. 최종 런타임은 실제 [발행 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/primary-runtime-final.log)에 있다.

최종 사전 검증 PASS, profile index check **2,452개/5,068 exact terms PASS**. 새 테스트 10개+candidate semantics 13개+transport 4개+고정 capture 8개인 **35개 관련 테스트 PASS**. 별도 managed workflow/transport 검사 12개도 PASS했다. [최종 관련 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/final-focused-with-historical-scope.log) · [workflow 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/workflow-focused-after-repair.log) · [사전 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/final-dictionary-validation.log) · [profile index 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/final-visual-index-check.log)

완료된 전체 발견 실행은 **225개 모듈**, **2,038개 발견/1,954개 실제 보고**, **199개 모듈 통과/26개 실패**였다. 84개는 class setup 중단으로 실행되지 않았다. 기존 이미지·core 산출물 overlay와 고정 capture scope의 제한된 재검증으로 4개 실패 모듈이 통과했고, **22개 모듈은 실패 상태**다. interpreter 누락을 고친 illustration 검사는 현재 후보팩 byte replay 실패를 다시 드러냈다. F097 마지막 수정 이후 균일한 전체 재실행은 하지 않았다.

남은 실패에는 V24/V35 sealed history의 SKILL·기존 source·증거 byte binding, 갱신된 current index/pack의 exact byte 비교, grammar dependency가 빠진 curated historical loader, 기존 profile/bundle metadata 투영, VEL/fire 추가 이전의 source-order expected 목록이 있다. **모든 실패를 기존 문제로 단정하지 않는다.** 일부는 이번에 의도적으로 새로 만든 current derived artifact를 고정 byte 비교가 거부한 경우다. [전체 실패 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/FULL-REGRESSION-CLASSIFICATION.md) · [전체 실행 원본 summary](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/full-suite-modules/SUMMARY.json)

기존 사진 스킬 파일·재귀 vector shard·텍스트 테스트 **4,016개**를 비교했다. 바꾼 기존 파일은 manifest 1개, index manifest 2개, runtime script 2개, 고정 capture test 1개인 **6개**이며, 그 밖의 비교 대상 변경·삭제는 **0개**다. 새 fire source·shard·evidence·test는 별도 추가 파일이다. old manifest row는 내용·순서가 정확한 prefix로 유지되었다. HEAD는 `30fc97a84fb3c8a7863adf0b8b60010dce73b444`로 같다. commit/push/PR/reset/stash는 하지 않았다. [최종 보존 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/PRESERVATION-FINAL.json) · [원래 조사 보존](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/RESEARCH-PRESERVATION.json)

격리 worktree는 실제 이미지 실행 경로와 immutable generation의 재현을 위해 보존했다. 프로젝트 복사본의 JSON은 원래 실행 경로를 유지한다. primary 복사 파일을 독립 재실행한 기록으로 바꾸지 않았으며, primary 이미지 SHA는 원본과 모두 일치한다.

## 결과를 반영한 후속 계획

| 순서 | 확인할 문제 | 반영·검증 방식 | 완료 조건과 현재 상태 |
|---|---|---|---|
| 완료 | F097 설명/graph owner 불일치 | owner endpoint와 gate만 수정, maintenance chain 및 재임베딩, 좁은 regression | 데이터 검사 PASS. 해당 후보의 render는 미실행 |
| 다음 1 | arm 1/3에서 fire profile 노출 0개 | 독립 자연 문장으로 후보/profile recall 표 작성. 소스·연료·가시 형태·관계의 component evidence를 추가하되 broad label을 hard duty로 승격하지 않음 | 후보와 profile별 노출·선택을 구분하고 인접 현상/부정/owner lock 회귀 통과. 미실행 |
| 다음 2 | F037 얼굴빛의 source ambiguity | 여러 외부 key와 금색 수평선이 없는 장면에서 화원과 얼굴의 위치를 한 crop에 유지하고 whole receiver 관계 검사 | 원본에서 얼굴빛과 화원 방향을 분리 확인. baseline/final 쌍이 없으면 causal gain은 미판정. 추가 render 미실행 |
| 다음 3 | 실내 화구 연기 경로 누락 | 화구와 굴뚝 목의 경로가 보이는 시점으로 새 독립 core 작성; 컵 증기와 연료 smoke의 owner를 따로 증거화 | 둘 다 보이거나 smoke 항목 FAIL. 증기 대체 금지. 추가 render 미실행 |
| 다음 4 | fire 131개 전체의 qualification 공백 | candle/ember/smoke/residue/heat shimmer/optical/solar/volcanic/body-surface 등 연구 matrix를 단계별 검증; 긴 whole 선언 재현과 독립 자연 query 시험을 분리 | 등록·검색·literal contribution·native gate·사용자 수락을 따로 기록. 기존 44개 회귀/10개 pixel 계획 전체 완료 아님 |
| 다음 5 | 22개 전체 회귀 실패 | 각 sealed history의 authenticated successor와 현재 loader dependency를 담당 범위에서 연결. 기존 archive·oracle byte는 보존하고 현재 의도적 metadata delta만 좁게 증명 | uniform 전체 재실행 및 setup-aborted 84개 포함 account. 이 작업에서는 미해결 |

이 계획은 새 데이터를 기본 요청에 무조건 붙이는 방식으로 구현하지 않는다. 사용자가 선택한 장면의 owner·관계·가시 요소를 강화하고, 선택되지 않은 연구 설명이 강제 연출이 되지 않도록 유지한다.
