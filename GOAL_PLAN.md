# Research-Backed Moe Grammar and Candidate-Pack Integration Goal

- 작성: 2026-08-11 17:54 KST
- 상태: complete
- 대상: `skills/subculture-illustration-image-generator`
- 기준 ref: `main@c10becc`
- 권위 입력: ChatGPT conversation `6a7acde9-4414-83ee-927b-1432db7c99dc`, 원 블로그의 34개 글, 독립 자료, 현재 저장소 계약
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: 29개 모든 모에요소마다 조사할 주제를 도출하고 실제로 조사한 뒤, 그 지식을 후보팩 또는 스킬에 반영해 사용자의 의도와 세부 취향을 더 정확히 이해하고 더 창의적이며 취향에 맞는 프롬프트를 만든다.
- 최종 제품/결과: 고정 문장 supplement가 아니라, 요소·세부 유형·매력 메커니즘·취향 축을 해석해 실제 후보를 선택하는 research-backed moe grammar와 이를 포함하는 additive candidate-pack v4 및 composer/audit 경로.
- 범위: 29개 연구 dossier, typed 후보 그래프, 자연어 요소·세부 취향 해석, creativity 기반 후보 다양화, 후보팩/composer/audit 통합, focused prompt qualification.
- 비목표: 기존 안전 제약·필터·refusal·negative prompt·retry 변경, v1~v3 역사 자산 변경, universal-scene 전체 재자격, hidden 1,152-run, 배포·push·PR, 보편적 독자 선호나 실제 이미지 품질 주장.

## 진척 계약

- 진척으로 인정: 완료된 요소별 dossier, 실행 가능한 후보/번들 추가, 후보팩에 노출되는 선택 결과, 실제 composed prompt 변화, 사용자 취향을 반영한 서로 다른 후보 선택, 결함을 닫는 제품 수정.
- 진척으로 인정하지 않음: URL 수집만 완료, 요소당 고정 문장 하나, 테스트·manifest·validator만 추가, 별도 supplement만 통과, prompt literal 자기검증, 검증 체계 확대.
- 검증-only 작업 상한: 제품 단계마다 focused check 1회, 최종 affected regression 1회. 두 번 연속 verification-only checkpoint 금지.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 새 실패 보고서는 distinct material failure에만, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker` 순서로만 기록한다.

## 기준선과 적용 교훈

- 현재 기준선: 34개 원문을 29개 요소로 정리했고 63개 source row와 요소별 alias/limitation/frame mode가 있다. 그러나 각 요소는 한 개 `prompt_clause_en`으로 축약되고 runtime은 이를 이어 붙이며, 기존 candidate pack·composer·selection graph는 변경되지 않았다.
- 보존할 자산: 34→29 inventory, source URLs, source/design-inference 구분, 불확실성, frame honesty, safety/photo/retry 불변 경계.
- 교체할 자산: single-clause element model, supplement-local pseudo candidate IDs, literal-only self-audit, 세부 유형·취향·창의성 없는 resolver.
- 고정 비교 조건: ordinary creativity 기본값은 0.5이며 creative cue는 high-development 계약을 활성화하되 저장 숫자를 임의로 바꾸지 않는다. 요소 자체는 사용자 요청에 나타날 때만 활성화하고 주변 문맥은 세부 유형·관점·강도를 선택하는 데 사용한다.
- 적용 보고서:
  - `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`: 이번 재설계의 직접 원인.
  - `docs/failed-reports/2026-08-08-character-moe-research-provenance-overclaim.md`: claim별 provenance와 router/visual atom 분리.
  - `docs/failed-reports/2026-08-08-character-moe-final-integration-contract-drift.md`: 다른 route family를 generic 필드에 억지로 맞추지 않고 typed field로 통합.
  - `docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`: one primary + 최대 two supports의 sparse executable grammar.
  - `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`: familiar anchor, one changed rule, first/second-look와 format-native composition.

## 29개 연구 계약

모든 dossier는 `definition_and_history`, `semantic_subtypes`, `appeal_mechanisms`, `observable_or_narrative_evidence`, `preference_axes`, `candidate_realizations`, `compatibility_and_conflicts`, `format_implications`, `source_supported_claims`, `cross_source_synthesis`, `design_inference`, `limitations`를 갖는다. 사실 주장은 exact source IDs에 연결하며, 출처가 약하면 미확정으로 남긴다.

| 요소 | 필수 연구 주제 |
|---|---|
| 흑화·타락 | 원인·주체성·가역성, 동일 인물 표식, 전후 가치·외형 대비 |
| NTR·네토라레 | NTR/네토리/네토라세/BSS 관점, 기존 관계·인지·동의·상실 시점 |
| 메스가키 | 위계 역전, 대상화된 도발, 말·표정·거리, 자신감과 역당황의 갭 |
| 마망·돌봄 | 돌봄 행동, 안정기지 감정, 생활·회복·정서 수용 장면, 역할 역전 |
| 풍기위원 | 실제 직무와 창작 관습, 역할 표식·규칙 소품, 통제와 감정 붕괴의 대비 |
| TS·TSF | 변환 원인·단계·영구성, identity continuity, 당사자·주변인 관점 |
| 얀데레 | 애정과 집착의 대비, 통제·감시·위협 단계, 대상·경쟁자·결과 |
| 매도·경멸 | 직접 발화와 비언어 경멸, 강도·코미디성, 카메라 권력각도와 대상 반응 |
| 동정을 죽이는 옷·스웨터 | 2015 blouse/skirt와 2017 backless knit 계보, 구조·시점·기대 반전 |
| 역바니걸 | classic bunny 불변 표식, coverage inversion, 중심·사지 분포와 앞·뒤 시점 |
| 돌핀 팬츠 | 실제 복식명·구조, curved hem·piping·slit, 소재·fit·동작 실루엣 |
| 히트텍 바디수트 | 상표와 generic bodysuit 분리, 이너웨어·단독 연출, 소재·연속 구조 |
| 스타킹 | stockings/hold-ups/garter/pantyhose/tights 구분, 지지 방식·길이·투명도·패턴 |
| 바니걸 | 역사적 uniform과 현대 trope, 핵심 부속품·소재·silhouette·view variants |
| I자 밸런스 | biomechanics, 지지 방식, 관절 연속성, 세로 silhouette와 camera |
| Thigh gap | anatomy·stance·lens 영향, negative space와 의상, 자연·과장 변형 |
| 겨드랑이 | shoulder/scapula/arm mechanics, pose·lighting·garment interaction |
| 손가락 빨기 | hand-mouth contact anatomy, gesture intent, gaze·crop, 유사 제스처 구분 |
| 안경 | frame·fit·optics, eye visibility, adjusting/removing gestures, impression variants |
| 포니테일 | tie point·tension·hair mass, high/low/side variants, gravity·motion lag |
| 배·복부 | torso anatomy, twist·compression·breathing, garment framing·surface light |
| 전연령 암시 연출 | occlusion·T-junction·Kuleshov·reaction, contextual suggestion와 보이지 않는 사실 경계 |
| 화면 흔들기 착시 | perceptual mechanism, contrast/phase/spatial-frequency substrate, 실제 interaction 조건 |
| 아헤가오 | eyes·pupils·mouth·tongue·fluid·asymmetry 구성, intensity와 stylistic variants |
| 파자마 챌린지 | oversized before/gathered after 구조, rear grip·tension folds, 일반 잠옷 장면과 구분 |
| 버블티 챌린지 | torso-cup support geometry, hands-free proof, straw/contact/camera와 코미디 변형 |
| 전략적 가림 셀카 | mirror·phone·direct/reflected hand geometry, handedness·T-junction·crop |
| 감각차단 마법 | 차단 감각, 시전자·대상·동시 사건, 외재화 cue와 인지 비대칭 |
| 퀵샌드 | 실제 물성·fiction exaggeration, entrapment stage, struggle/rescue pose와 tone |

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 목표·기준선 정상화 | 기존 supplement 성공을 scoped prototype로 재분류하고 새 outcome-first plan, 29 neutral + 29 preference-bearing request corpus를 고정한다. | 현재 asset/runtime diff와 58 request coverage 직접 검토 | 완료 판정이 실제 candidate-pack 통합 없이는 불가능함 |
| 2. 전 주제 research dossier | 다섯 research stream으로 29 dossier를 작성하고 main agent가 하나의 schema/provenance 언어로 정규화한다. | 모든 factual claim의 source refs와 모든 element의 required fields 확인 | 29/29 dossier complete, single-clause-only element 0 |
| 3. typed moe grammar | `illustration_moe_grammar_v2`에 routers, visual/narrative atoms, primary/support candidates, preference axes, bundles, compatibility/conflicts를 구현한다. | 29 neutral requests와 variant probes가 실제 후보를 선택 | 자료상 복수 유형은 서로 다른 candidate IDs로 실행됨 |
| 4. candidate-pack v4 통합 | `moe_intent`, `moe_grammar`, selection reasons, alternatives와 실제 moe candidate IDs를 pack/composer/audit에 연결한다. v1~v3 dispatch는 유지한다. | request -> pack -> composed prompt end-to-end 29/29 | 최종 prompt가 supplement append가 아니라 기존 scene/format/authorial grammar와 합성됨 |
| 5. 취향·창의성 반영 | preference cues가 subtype·viewpoint·intensity·camera·material 후보를 바꾸고, creativity/seed는 같은 intent 안에서 호환 가능한 다양한 선택을 만든다. | 29 preference cases + 6 cross-element combinations + fixed seed comparison | explicit preference 우선, unrequested element 0, adjective-only variation 0 |
| 6. 집중 최종 자격 | 12 representative baseline-vs-v4 prompts를 intent fidelity, research specificity, coherent event, authorial choice, no label soup로 검토하고 affected regressions를 한 번 실행한다. | focused tests, v1~v3 byte replay, photo/retry hashes, one final independent review | 모든 최종 기준 충족 후에만 goal complete와 success report 작성 |

## 최종 완료 기준

1. 29개 모든 요소에 완전한 research dossier와 실행 가능한 후보가 있다.
2. 복수 계보·관점·세부 유형이 있는 요소가 하나의 고정 문장으로 축소되지 않는다.
3. 사용자의 요소명과 주변 취향 단서가 typed interpretation과 selection reason에 남는다.
4. 실제 selected moe candidate IDs가 candidate pack과 composed prompt evidence에 결속된다.
5. 최종 프롬프트는 선택된 요소들을 기존 장면·형식·authorial grammar와 하나의 사건으로 합성한다.
6. 기본 creativity 0.5와 creative-cue 계약을 보존하면서, 창의성은 후보·changed rule 선택을 실제로 바꾼다.
7. v1~v3, photo routing, retry, negative prompt, 기존 안전·필터 동작은 변경되지 않는다.
8. 검증·문서만으로 완료할 수 없으며, 29 direct + 29 preference + 6 combination + 12 representative prompt outputs가 직접 제품 동작을 입증한다.

## 검증 수준과 예산

- 위험 수준: ordinary offline implementation. 외부 상태 변경 없음.
- 반복 중: 해당 dossier/grammar/runtime focused checks만 실행한다.
- 최종: affected test modules, v1~v3 replay, photo/retry boundary, 독립 검토 1회.
- 명시적 제외: universal 24x417, hidden 1,152-run, 전체 이미지 생성, 29x29 exhaustive combinations, 새 qualifier framework.
- 실제 이미지 A/B는 core goal 완료 후 사용자가 원할 때 별도 목표로만 진행한다.
- 검증 확장 전 질문 조건: 기존 경로로 필수 기준을 직접 확인할 수 없거나 검증 작업이 구현 작업보다 커질 때.

## 중단 조건과 진행 로그

- 같은 설계가 동일 원인으로 두 번 실패하면 세 번째 verifier/runner를 만들지 않고 원인을 failed report에 기록한 뒤 설계를 바꾸거나 사용자에게 질문한다.
- 원 출처가 세부 변형을 지지하지 않으면 근거 없는 candidate 수를 채우지 않고, 확인된 한계와 대안을 기록한다.
- 후보팩 v4가 기존 v1~v3 byte replay를 깨면 v1~v3를 수정하지 않고 additive dispatch 경계를 고친다.
- 안전·필터 변경이 필요해 보이는 경우 이 목표에서는 진행하지 않고 별도 작업으로 남긴다.
- 외부 유료 API, 이미지 생성, 배포, push, PR이 필요하면 먼저 사용자 승인을 받는다.
- 실행 지식 보고서: `docs/failed-reports/2026-08-11-moe-element-supplement-underintegration.md`; 완료 시 조건을 만족할 경우 새 passed report 최대 1건.

## 완료 증거

- 29/29 source-bound dossier가 다섯 raw shard에 존재하며 compiler가 exact hash를 검증한다.
- `illustration_moe_grammar_v2.json`: 29 elements, 233 candidates, 198 sources, SHA-256 `4d77fc2c9d8cf7d94af0742c4bd577e19b8193629dcf9df1c5c6dc2e33383a9b`.
- 29/29 neutral request는 canonical candidate key를, 29/29 preference request는 서로 다른 기대 subtype/key를 선택한다.
- 6/6 cross-element request는 정확히 one global primary plus at most two supports를 사용하고, 12/12 prompt-evidence comparison은 current grammar 및 v4 audit에 결속되어 pass한다.
- creative cue는 base `creative_development_required`와 moe novelty 2를 활성화하지만 stored creativity `0.5`를 바꾸지 않는다.
- v1 fixed-clause replay, base safety/negative equality, retry/photo baseline hashes, mutation rejection을 focused suite에서 함께 확인했다.
- 성공 보고서: `docs/passed-reports/2026-08-11-research-backed-moe-grammar-v2.md`.
- 미주장: 실제 이미지 픽셀 품질, 보편적 독자 선호, hidden generalization, exhaustive pairwise compatibility.
