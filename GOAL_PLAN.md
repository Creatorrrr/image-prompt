# Research-Backed Scene Diversity and Render Quality Goal

- 작성: 2026-08-07 18:26 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: clean `main@7daff7a` (`origin/main`보다 4 commit ahead)
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: CJK commercial narrative worldbuilding expansion
- 현재 material failure: `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`

## 1. 목표와 실제 산출물

기존에 공개 근거를 조사해 반영한 `research`, `subculture`, `worldbuilding`, `CJK worldbuilding` 데이터 계층 전체를 감사하고, 주제별 프롬프트와 실제 이미지가 반복적인 직원·심사·기록·창구 장면으로 수렴하지 않도록 개선한다. 완료 후 짧은 주제 요청만으로도 사용자는 특정 작품을 복제하지 않으면서 장르가 픽셀에서 알아볼 수 있고, 하나의 핵심 사건과 인물의 이해관계가 있으며, 같은 주제에서도 서로 다른 장면 기능을 선택할 수 있는 사진형 이미지를 얻어야 한다.

기존 연구 데이터의 세계 작동 규칙과 출처는 지식 계층으로 보존한다. 렌더 계층은 그 지식을 한 프레임에 모두 나열하지 않고 `핵심 사건 1개 + 세계 증거 1~2개 + 이해관계 또는 결과 1개 + 장르 앵커 1개`로 희소하게 표현한다. 기존 라우팅 정확도, typed-domain 격리, 문화 provenance, IP·살아 있는 관습 경계, candidate cap, deterministic behavior, 안전 자동 통과는 유지한다.

주요 제품 산출물은 다음과 같다.

1. 기존 네 확장의 모든 route를 장면 기능·행위자 역할·장소 원형·장르 앵커 관점에서 분류한 동결 기준선과 실패 목록.
2. 지식 taxonomy와 렌더 장면 표현을 분리하는 최소 additive scene-expression 계약. 기존 필드로 표현할 수 있으면 새 schema를 만들지 않는다.
3. direct preset에도 적용되는 fail-closed atomic scene contract, 비어 있지 않은 topic/genre intent, 희소 evidence budget, 안정적인 candidate-pack 저장 경로.
4. 로판·상태창·학원물 파일럿과 감사에서 실패한 기존 연구 route의 실제 scene/data 개선.
5. 동결 routing holdout과 별도의 렌더·장면 다양성 표본 및 실제 이미지 검토 결과.
6. 필요한 경우 승인된 공개·추상 taxonomy 문자열만 사용하는 semantic index 재생성.

## 2. 범위와 비목표

### 범위

- `photo_prompt_research_extension.json` 17 preset / 165 slot entry
- `photo_prompt_subculture_extension.json` 33 preset / 179 slot entry
- `photo_prompt_worldbuilding_extension.json` 18 preset / 288 slot entry
- `photo_prompt_cjk_worldbuilding_extension.json` 20 preset / 356 slot entry
- 위 확장의 loader, intent routing, candidate-pack composition/audit, quality profile, semantic index와 관련 회귀
- 먼저 로판·상태창·학원물 세 실패 route를 교정하고, 같은 규칙으로 네 확장 전체를 측정해 실패한 route를 모두 교정한다.
- 기존 출처를 다시 복제하지 않는다. 새 장면 문법이나 문화적 시각 경계에 근거가 필요한 경우에만 공식 플랫폼, 제작 주체, 공공 문화기관, 학술·업계 1차 자료를 추가 조사한다.
- `market_origin`과 실제 화면에 드러나는 `diegetic_visual_provenance`를 분리한다. 시장 용어의 기원을 문화 스타일처럼 렌더하지 않는다.
- 사용자가 안전 평가를 별도로 요청하지 않으면 기존 단순 automatic pass를 유지한다.

### 비목표

- 특정 작품, 캐릭터, UI, 문장, 로고, 실존 인물 또는 살아 있는 의례를 복제하는 것.
- 장르 인식성을 높인다는 이유로 읽을 수 있는 상태창, 학교 문장, 가문 문장 같은 IP 유사 표지를 강제하는 것.
- 기존 동결 routing 기대를 이미지 취향에 맞춰 삭제·완화하는 것.
- 모든 route를 같은 수의 장면이나 같은 서사 문법으로 기계적으로 평준화하는 것.
- 새 범용 evaluator 서비스, 별도 데이터베이스, 복잡한 안전 승인 흐름을 만드는 것.
- 문서·테스트·fixture만 늘어난 상태를 완료로 간주하는 것.
- commit, push, PR 또는 배포. 사용자가 별도로 요청할 때만 수행한다.

## 3. 제품 원칙과 구속 결정

1. **지식과 장면을 분리한다.** `world_mechanism`, research evidence, term provenance는 무엇이 세계를 작동시키는지 설명한다. scene expression은 그중 무엇을 한 프레임에 보여 줄지 결정한다.
2. **운영 다큐멘터리는 하나의 선택지다.** inspection, registration, audit, handoff는 주제에 맞을 때 유지하지만 기본 장면 또는 유일한 장면이 될 수 없다.
3. **장면 기능을 원자적으로 선택한다.** `confrontation`, `revelation`, `threshold`, `controlled_action`, `aftermath`, `intimate_decision`, `environmental_spectacle`, `operational_documentary` 같은 기능 중 하나를 먼저 고르고 subject/action/location/prop을 같은 scene tag로 묶는다.
4. **장르 앵커는 읽을 수 있는 UI가 아니다.** 상태창은 관찰되는 규칙 변화와 대가, 학원물은 시험·수업·경쟁의 사건, 로판은 계급·관계·계약의 선택과 결과처럼 화면 사건으로 표현한다.
5. **희소 evidence budget을 사용한다.** 한 프롬프트에 6~7개 제도를 모두 넣지 않는다. 핵심 사건을 가리는 증거는 후보 팩에 남아 있어도 최종 조합에서 제외한다.
6. **시장 기원은 시각 provenance가 아니다.** `kr_market`, `jp_market`, `cn_market`은 용어·유통 맥락으로만 쓰고, 실제 장면이 특정 문화적 시대·생활양식을 요구할 때만 근거 있는 시각 provenance를 별도로 선택한다.
7. **창의성 토글보다 eligible scene pool을 먼저 고친다.** 자동 모드는 주제에 맞는 비운영 장면도 선택할 수 있어야 한다. 사용자가 다큐멘터리·기록·운영을 명시하면 운영 장면을 우선할 수 있다.
8. **계약 검증과 픽셀 검증을 구분한다.** prompt audit PASS는 이미지 품질 PASS가 아니다. 최종 완료에는 실제 렌더와 주제 인식성 검토가 필수다.

## 4. 진척 계약

- 진척으로 인정: 실제 route의 eligible scene이 다양해짐, direct pack에 atomic scene/topic intent가 fail-closed로 적용됨, 행정 장면 편향이 measured pack/render에서 감소함, 주제 인식성이 실제 이미지에서 개선됨, 또는 기존 연구 route의 근거 있는 장면 표현이 추가됨.
- 진척으로 인정하지 않음: 계획·보고서·테스트만 추가함, validator를 완화함, 이미지 실패를 prompt audit PASS로 덮음, 장르 단어를 capture context에만 추가함, 기존 holdout 기대를 사후 변경함.
- Stage 1은 유일한 setup checkpoint다. 이후 각 checkpoint는 제품 데이터/동작 delta 또는 실제 생성·렌더 후보를 남긴다.
- 검증-only checkpoint를 두 번 연속 만들지 않는다. 동일 근본 원인의 수리는 최대 2회이며 실패하면 기준을 낮추지 않고 material failure를 갱신한다.
- 실행 지식은 metadata 우선으로 검색하고 전문은 최대 5건만 읽는다. 현재 소스와 직접 측정한 증거가 보고서보다 우선한다.
- 자동 목표 상향은 비활성이다.

## 5. 기준선과 적용할 실행 지식

### 확인된 기준선 실패

- 로판 최종 이미지는 상속·재정 소품은 보이나 중국 사극 회계 회의로 읽히며, 로맨스판타지의 관계·선택·계급 긴장이 약하다.
- 상태창 최종 이미지는 게임 규칙이나 능력 변화보다 현대 관공서·서비스 창구로 읽힌다.
- 학원물 최종 이미지는 능력 교육·시험·경쟁보다 행정 자원 배분 작업실로 읽힌다.
- 세 candidate pack 모두 `documentary_photo + documentary`, 직원/관리자, 실내 카운터·테이블, 검사·대조·인계 장면으로 수렴했다.
- CJK action 46개 중 31개가 checking/cross-checking/comparing/coordinating 계열이고, subject 46개 중 43개가 staff/clerk/inspector/administrator 등 운영 역할을 포함한다.
- 기존 CJK 완료 목표는 최소 세 world axis와 여섯 world-evidence를 최적화했고 실제 렌더 품질은 명시적으로 제외했다. 따라서 기존 routing/evidence 자격은 유효하지만 이미지 품질 자격으로 재사용할 수 없다.

### 적용할 과거 보고서

- `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`: additive extension, typed domain, provenance, frozen route와 leakage 계약은 보존한다. 여섯 evidence를 최종 렌더에 모두 강제하는 부분은 재사용하지 않는다.
- `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`: specialty route 격리와 shared taxonomy는 보존하되, 실제 렌더 품질은 이번 목표에서 새로 검증한다.
- `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`: index 재생성 시 `--batch-size 1`과 cache/checkpoint를 유지한다.
- `docs/failed-reports/2026-08-07-subculture-surface-applicability-golden-drift.md`: global applicability를 넓히지 않고 narrow typed override로 legacy RNG를 보존한다.
- `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`: exact scoped route는 nearby generic semantic preset보다 우선한다.

## 6. 실행 단계

| 단계 | 실제 산출물 또는 동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 실패 기록·전수 기준선 동결 | 현재 3개 렌더를 material failure로 기록하고 네 확장의 모든 preset을 scene function, role, location, genre anchor, provenance로 분류한 동결 artifact를 만든다. route 유형별 수용 기준과 최종 표본을 구현 전에 고정한다. | JSON/schema, route 88개 누락 0, 현재 이미지의 metadata-free 판정과 구조 통계 | 실패 목록과 변경 대상이 구현을 보지 않은 상태로 고정되고 기존 성공 보고서의 재사용 경계가 상호 링크됨 |
| 2. scene-expression·candidate contract 구현 | 기존 필드를 우선 재사용해 scene function, topic/genre intent, sparse evidence budget과 diegetic provenance를 pack에 전달한다. direct preset도 선택된 하나의 scene tag로 fail-closed가 되고, official stdout writer가 숫자 spelling을 보존한다. | focused unit, 동일 seed deterministic pack, direct preset의 enabled scene contract, canonical pack hash | 파일럿 route에서 비운영 장면이 실제 eligible 후보이며 누락·혼합 scene은 audit가 실패함 |
| 3. 로판·상태창·학원물 파일럿 교정 | 각 route를 최소 4 atomic scene / 3 scene function으로 확장하고 최소 2개는 비운영 사건으로 만든다. anti-overfit 문구가 장르 정체성을 지우지 않게 고치고 market/visual provenance를 분리한다. | route별 fixed seed pack, 세 주제 × 서로 다른 scene function 실제 렌더, 최대 2회 원인 수리 | 세 주제 모두 픽셀에서 주제·핵심 사건·이해관계를 알아볼 수 있고 서로 같은 행정 골격으로 수렴하지 않음 |
| 4. 네 연구 확장 전체 개선 | 동결 감사에서 실패한 모든 route에 비운영/관계/행동/환경 장면과 장르 앵커를 추가한다. 본질적으로 기록적인 route는 예외 이유와 다른 장면 기능을 명시한다. 새 시각 문법 주장에만 출처를 추가한다. | route별 scene-function/role/location 분포, protected-reference scan, fixed-seed pack | narrative-world route는 4 scene / 3 function 이상, 다른 전문 route는 2 function 이상 또는 근거 있는 예외이며 실패 route가 미수정으로 남지 않음 |
| 5. retrieval·index·실제 표본 검증 | dictionary hash가 바뀌면 승인된 추상 text만 batch 1로 index를 재생성한다. 기존 frozen retrieval을 그대로 통과시키고 네 확장에서 사전 동결한 층화 표본을 실제 렌더한다. | index hash/shard/order, 기존 retrieval/leakage/cap, versioned visual review artifact | routing 회귀 없이 표본이 주제 인식성·독창성·서사적 관심·world evidence·장면 다양성 기준을 통과함 |
| 6. 닫힌 최종 자격 판정 | focused 결과를 고정한 뒤 full validator/unit/contradiction/applicability/retrieval과 시각 수용 게이트를 한 번 실행한다. 실패 보고서를 resolved로 갱신하고 자격이 있을 때만 성공 보고서 1개를 만든다. | 명령별 결과와 8개 criterion matrix, `git diff --check` | 아래 완료 기준이 모두 pass하고 docs/tests만이 아닌 제품 파일 delta가 존재함 |

## 7. 최종 완료 기준

1. 네 연구 확장의 모든 preset이 동결 감사에 포함되고, 새 scene-expression 기준에 실패한 route가 미수정 상태로 남지 않는다.
2. narrative-world route는 최소 4 atomic scene과 3 scene function을 가지며 최소 2개는 비운영 사건이다. 다른 전문 route는 최소 2 function을 가지거나 본질적 예외가 근거와 함께 기록된다.
3. direct preset candidate pack은 enabled fail-closed `scene_contract`, 비어 있지 않은 topic/genre intent, 하나의 selected provenance, sparse evidence budget을 갖고 장면 혼합을 audit가 거부한다.
4. `market_origin`과 `diegetic_visual_provenance`가 분리되고, CJK 복합 route가 시장 라벨을 실제 문화 양식처럼 평면화하지 않는다.
5. 로판·상태창·학원물 실제 최종 렌더가 각각 주제 인식성, 핵심 사건, 인물의 이해관계, 장면 고유성을 통과하며 행정 창구/감사 테이블 골격으로 수렴하지 않는다.
6. 네 확장의 사전 동결 층화 렌더 표본이 주제 인식성, 독창성, 서사적 관심, 세계 증거, 장면 다양성 시각 게이트를 통과한다. 실패 시 verifier나 기대를 완화하지 않는다.
7. 기존 frozen semantic routing, typed-domain 격리, generic leakage 0, candidate cap, deterministic behavior, IP·문화·살아 있는 관습 경계와 기본 safety automatic pass가 유지된다.
8. dictionary/index/candidate/audit/contradiction/applicability/retrieval/full unit과 `git diff --check`가 통과하고 제품 데이터 또는 runtime 코드가 실제로 변경된다.

## 8. 검증 수준과 재시도 예산

- 위험 수준: 중간. 로컬 데이터와 생성 경로 변경이지만 semantic retrieval, deterministic selection, 문화 구분, 실제 이미지 품질에 회귀 위험이 있다.
- Stage 2~4는 변경 route focused tests와 fixed-seed pack만 반복한다. Stage 3 렌더는 주제당 서로 다른 scene function을 사용하고 동일 원인 수리는 최대 2회다.
- Stage 5에서 semantic index 재생성은 최대 1회, 네트워크 일시 오류는 1회 재시도한다. `--batch-size 1`을 유지한다.
- Stage 5의 층화 렌더 표본은 구현 전 고정한 12개 route(확장별 3개)를 기본으로 한다. 기준선에서 표본 크기가 부족하다는 직접 증거가 있을 때만 늘리고 이유를 기록한다.
- Stage 6 full suite와 전체 visual acceptance는 한 번만 실행한다. 실패 후 기대값 삭제·완화나 렌더 성공본만 골라내기는 금지한다.
- 이미지 생성은 기존 내장 image tool을 사용하고 prompt/negative bytes, seed, pack ID, chosen IDs와 결과 경로를 로컬 artifact에 보존한다.

## 9. 중단하고 질문할 조건

- 기존 승인 범위를 넘어 출처 원문, 이미지, 개인정보, 비공개·성스러운 자료를 외부로 보내야 할 때.
- 새로운 유료 서비스, 대량 생성 비용, 배포, 파괴적 변경 또는 공개 publication이 필요할 때.
- 기존 frozen routing 기대를 약화해야만 통과하거나 generic 기본 선택 의미를 바꿔야 할 때.
- 같은 근본 원인의 수리 2회 뒤에도 필수 product/visual criterion이 실패할 때.
- 문화 provenance를 공개 권위 자료로 구분할 수 없어 거짓 시각 양식을 만들 위험이 있을 때. 이 경우 market-only route로 축소하는 선택지를 제시한다.

## 10. 실행 지식·진행 로그 계약

- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/` metadata를 우선 검색하고 전문은 관련도 순 최대 5건만 읽는다.
- material failure는 재시도 전에 matching failed report에 통합한다. 실패가 과거 성공 보고서의 재사용을 제한하면 양방향 링크를 같은 변경에 남긴다.
- 완료 기준을 모두 직접 검증한 뒤에만 기존 material failure를 `resolved`로 바꾸고 `Qualification: resolved-material-failure` 성공 보고서를 목표당 최대 1개 작성한다.
- 각 checkpoint 로그는 `product delta -> direct evidence -> remaining gap -> blocker -> execution-knowledge paths` 순서로 이 파일에 추가한다.
- credential, token, secret, 민감 endpoint, 개인 정보와 출처 원문은 보고서·로그에 저장하지 않는다.
- commit/push는 별도 사용자 요청 전까지 수행하지 않는다.

## 11. Codex 실행 프롬프트

```text
/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Continue from the first incomplete stage, preserve frozen routing and safety/IP/cultural contracts, record any material failure before retrying, and do not claim completion from documents, tests, prompt audits, or routing scores without the required product and rendered-image evidence.
```

## 12. 진행 로그

### 2026-08-07 / Stage 1 material failure 및 기준선 시작

- product delta: 활성 장기 목표를 기존 CJK taxonomy 구축에서 전 연구 확장의 scene diversity와 실제 render quality 개선으로 전환했다. 88개 preset의 구현 전 구조를 `render_scene_expression_baseline_v1.json`에 동결하고, 네 확장별 3개씩 총 12개 최종 렌더 표본을 `render_scene_quality_holdout_v1.jsonl`에 고정했다.
- direct evidence: 로판·상태창·학원물 세 최종 이미지를 다시 검사했고 prompt audit 결과와 픽셀 인식 결과가 불일치함을 확인했다. 구조 감사는 research 17, subculture 33, worldbuilding 18, CJK 20 route를 누락 없이 포함했고, 기존 explicit render contract 부재와 narrative scene/function 부족 때문에 기준선 88/88을 개선 대상으로 판정했다. 렌더 holdout은 12행·12 unique case·12 unique preset이며 각 확장에 정확히 3행이다.
- remaining gap: runtime scene contract 구현, 파일럿과 전수 데이터 교정, 실제 A/B 렌더가 남아 있다.
- blocker: 없음. semantic index 외부 전송은 이전에 승인된 공개·추상 taxonomy text 범위만 유지한다.
- execution-knowledge paths: 본 문서 5절의 passed 2건과 failed 3건을 관련도 순으로 적용했고, 새 material failure를 별도 보고서로 통합했다.

### 2026-08-07 / Stage 2 scene-expression contract 구현

- product delta: 선택된 direct preset의 atomic scene tag에서 subject/action/location/prop을 fail-closed로 묶고, `render_contract`, topic intent, `evidence_budget`, `diegetic_visual_provenance`를 candidate pack과 composed-prompt audit에 연결했다. preset-local weight multiplier로 범용 dictionary를 오염시키지 않고 documentary 선택 비중을 낮췄으며, `--output-file`로 JSON 숫자 spelling을 재직렬화 없이 보존한다.
- direct evidence: 새 scene-expression extension은 dictionary metadata validator와 Python compile을 통과했다. 3개 파일럿 × seed 1..64에서 route당 4 scene, 3개 이상 scene function, documentary subject/medium/genre 각각 16/64 이하를 확인했고, 장면 혼합·필수 core slot 누락·evidence 초과 조합을 감사기가 거부했다. canonical output-file hash 회귀와 기존 CJK/worldbuilding focused tests도 통과했다.
- remaining gap: 나머지 85 route의 명시적 render contract와 장면 기능 보강, semantic index 재생성, 층화 렌더가 남아 있다.
- blocker: 없음.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-subculture-surface-applicability-golden-drift.md`의 narrow typed override와 `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`의 exact scoped precedence를 유지했다.

### 2026-08-07 / Stage 3 로판·상태창·학원물 실제 렌더 교정

- product delta: CJK 파일럿 3 route를 각각 4 atomic scene / 3개 이상 scene function으로 확장하고, 운영 장면 외에 관계 선택·대가 폭로·경쟁자 구조 같은 사건을 추가했다. `market_origin`과 화면 provenance를 분리하고 world clue를 1~2개로 제한했다.
- direct evidence: fixed seed candidate pack 3개 모두 composed audit `status=pass`, `quality_status=pass`, failures/warnings 0이었다. 내장 image tool 실제 결과에서 로판은 가상 유럽풍 공개 약혼 선택, 상태창은 붕괴 구조와 능력 대가, 학원은 성인 순위 시험 중 경쟁자 구조로 읽혔고 이전의 회계 회의·서비스 창구·행정 워크숍 골격이 재현되지 않았다. pack/prompt/negative/chosen IDs, 원장 run ID, PNG hash·크기와 수동 픽셀 판정은 `generated_images/scene-expression-pilot-v1-20260807_184900/`에 보존했다.
- remaining gap: 세 파일럿만으로 전 연구 확장 전체를 자격화할 수 없다. 동결 감사의 나머지 route 보강과 12-case holdout 실제 렌더가 남아 있다.
- blocker: 최초 로판 image-tool 요청이 일시적 network error로 실패했으나 결과물 생성 전 오류였고, 동일 bytes 재전송 1회로 성공했다. 원장에 오류와 retry chain을 모두 남겼으며 지속 blocker는 없다.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`의 픽셀 실패 원인을 직접 교정했고, 기존 passed 보고서는 routing/evidence 근거로만 사용했다.

### 2026-08-07 / Stage 4 네 연구 확장 전체 scene-expression 보강

- product delta: research 17, subculture 33, worldbuilding 18, CJK 20 route 전체에 preset render-contract 기본값을 연결하고, 기존 subject/action/location/prop에서 resolved atomic scene blueprint를 구성했다. 이 네 장면 atom은 ordinary sampler 후보가 아니라 별도의 mandatory render instruction으로 유지한다. worldbuilding 18 route와 파일럿을 제외한 CJK 17 route에는 각각 두 개의 주제별 비운영 사건을 별도 compact shard로 추가했다. 로판·상태창·학원 파일럿도 중복 semantic slot 없이 같은 blueprint 경로로 통합했다.
- direct evidence: current 구조 감사에서 88/88 route가 explicit contract를 갖고 통과했으며 narrative route는 4개 scene과 최소 3개 function, specialty route는 최소 2개 function을 충족했다. seed 1..64가 route별 모든 blueprint에 도달하고, 숫자 seed cycle은 4-scene route에서 16회씩 균등하며 3-scene route도 최대 편차 1이다. 각 scene은 subject/action/location/prop 네 core slot, 단일 diegetic provenance와 clue 1~2개를 유지하고 protected-reference scan 및 candidate cap을 통과했다.
- remaining gap: 실제 semantic retrieval 회귀와 사전 동결 12-case 렌더의 픽셀 수용 판정, 최종 full suite가 남아 있다.
- blocker: 없음. 새 render metadata는 semantic text entry를 늘리지 않았고, 기존 6,379개 벡터를 모두 재사용할 수 있는 구조다.
- execution-knowledge paths: 기존 네 extension의 research evidence와 typed-domain route를 삭제하거나 넓히지 않았고, 새 장면 표현만 분리 shard에 추가해 기존 성공 보고서의 routing 자격 경계를 보존했다.

### 2026-08-07 / Stage 4 sampler provenance 회귀 수리

- product delta: 초안에서 resolved scene atom을 ordinary candidate pool에 합성했던 표현을 제거하고, `render_contract.selected_scene.atomic_scene`과 `selected_render_blueprint` fail-closed group으로 분리했다. 장면 atom을 최종 문장에 모두 요구하되 같은 controlled core slot의 일반 candidate ID 선택은 거부한다. `--scene-function`은 direct preset에만 적용되는 optional control로 만들고, no-people 요청은 명시적으로 non-human인 blueprint만 허용하도록 fail-closed 처리했다.
- direct evidence: 합성 후보 초안은 frozen generalization 79건 중 17건에서 `candidate_pool_not_sampler_exact`를 일으켰고 material failure의 Attempts에 기록했다. 분리 후 generalization 79/79, holdout 24/24, domain holdout v2 6/6, retrieval holdout v4 22/22와 contradiction 643 preset에서 위반 0을 확인했다. 새 no-people/scene-function focused 회귀 2건도 통과했다.
- remaining gap: 이 수리 이후의 최종 full suite와 수용 게이트를 Stage 6에서 한 번 실행해야 한다.
- blocker: 없음. frozen 기대나 candidate cap을 완화하지 않았다.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`에 실패 표현과 다음 안전 수리를 통합했고, sampler exactness는 기존 generalization fixture를 변경하지 않고 복구했다.

### 2026-08-07 / Stage 5 semantic index 재물질화 시작

- product delta: 변경된 dictionary hash에 맞춰 semantic index manifest와 16개 hash shard를 새 generation 경로로 재물질화했다.
- direct evidence: 빌더가 시작 시점에 `Embedded 6379/6379 entries`를 보고해 모든 semantic text/vector가 기존 index에서 일치 재사용됐고 Gemini 임베딩 요청은 발생하지 않았다. `--check-index`는 dictionary hash `e6ca5dbebce5e2547ee2d6be6227be157f2a5779098d3299684f4ead8570fb48`, 6,379 entries, 768 dimensions, semantic-text-v2를 `status: ok`로 검증했다.
- remaining gap: 기존 frozen retrieval/leakage/contradiction 회귀와 12개 holdout의 current pack·실제 이미지·수동 픽셀 판정이 남아 있다.
- blocker: 없음. 승인된 외부 전송 범위였으나 cache hit 100%라 taxonomy text를 외부로 보내지 않았다.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`에 따라 batch size 1과 기존 index cache를 유지했다.

### 2026-08-07 / Stage 5 retrieval·12-case 실제 렌더 완료

- product delta: frozen 12-case holdout에 맞춰 research, subculture, worldbuilding, CJK 각 3개 pack을 서로 다른 scene function으로 생성하고 내장 image tool로 실제 렌더했다. 모든 selected scene atom을 ordinary sampler pool 밖에서 조합했고, 12개 composed prompt는 88~120 words, contract/quality audit PASS, failures/warnings 0을 유지했다. solarpunk와 학원물은 최초 픽셀 판정의 구체적 원인을 보존한 뒤 이미지 편집을 각 1회만 수행했다.
- direct evidence: `render_scene_quality_visual_review_v1.json`의 metadata-free 판정은 12/12 case, 36/36 review focus를 통과했다. 스포츠 선취 동작, 자연 변화 전선, 문화재 상태 선택, 비주얼계 공연, TTRPG 공동 폭로, 로우라이더 전시 문턱, 변칙 기록 침입, 솔라펑크 돌봄 전력 배분, 던전 신스 대피 선택, 로판 약혼 거부, 상태 능력 대가, 성인 능력학원 경쟁자 구조가 서로 다른 픽셀 사건으로 읽혔다. 12개 원 생성과 2개 편집은 canonical prompt ID 검증 후 `runs/image_runs.ndjson`에 기록했다.
- remaining gap: 최신 source/data 상태에서 validator, full unit, contradiction/applicability/retrieval, index와 visual acceptance를 닫힌 Stage 6 게이트로 한 번 실행해야 한다.
- blocker: 없음. 상태창은 readable UI 없이 원인-대가로 표현되어 범용 초능력 생존물과 인접하고, 로우라이더 hydraulic 움직임은 mid-lift보다 낮은 차체와 안내 동작으로 암시되는 제한을 visual review에 명시했다.
- execution-knowledge paths: 첫 index manifest 이후 holdout이 드러낸 route-specific scene function을 보강하면서 manifest를 cache-only로 다시 물질화했다. 12개 렌더 생성 시 hash는 `97259bdbe6660b48163d09e41793fbe57ca14cee4cbed960b8458494d843473e`였다. 최종 sampler-preservation 수리 후 current hash는 `ad0496bbb45e0db76c786cdf5b8d4e88e7c1853686daad63cc978f7e004fd6ff`, 6,379 entries, 16 shards, 768 dimensions이다. 모든 물질화가 6,379/6,379 vector를 재사용해 Gemini 요청과 taxonomy text 외부 전송은 0이었고, 중간의 미참조 untracked shard 세대는 삭제해 current·기존 tracked 세대만 보존했다.

### 2026-08-07 / Stage 6 첫 닫힌 게이트와 material failure

- product delta: 없음. 수용 기준을 바꾸지 않고 current source에 대해 real acceptance, contradiction, full unit을 실행했다.
- direct evidence: acceptance gate는 실제 Gemini embedding, mock=false에서 generalization 79/79, holdout 24/24, domain v2 6/6, retrieval v4 22/22, visual 12/12와 focus 36/36을 통과했다. contradiction은 643 preset × 3회, 1,929 생성에서 violation 0이었다. full unit은 399개 중 397개만 통과했다. 실패 1은 학원 route의 ordinary subject multiplier가 기존 seed 1..3 subject 다양성을 2개 이상에서 1개로 축소한 제품 회귀이고, 실패 2는 generic pack의 새 disabled render 필드 둘을 exact-key 기대에 반영하지 않은 테스트 계약 누락이다.
- remaining gap: redundant subject multiplier를 제거해 기존 sampler 다양성을 복구하고, generic pack이 새 필드를 disabled로 제공함을 테스트한 뒤 영향을 받은 focused 회귀와 current 전체 게이트를 다시 닫아야 한다.
- blocker: 없음. 같은 원인의 첫 최종 수리이며 retry budget 안이다.
- execution-knowledge paths: 이 두 실패를 `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`의 Attempts에 먼저 통합했다. frozen expectation이나 acceptance threshold는 변경하지 않는다.

### 2026-08-07 / Stage 6 수리 후 최종 자격 통과

- product delta: redundant subject multiplier 세 개를 제거해 ordinary CJK sampler의 기존 seed 다양성을 복구하고, generic pack exact-key 회귀가 additive `render_contract`와 `evidence_budget`을 disabled 상태로 요구하도록 갱신했다. current 인덱스는 cache-only로 `ad0496…` generation에 물질화했으며, 실패 보고서를 resolved로 전환하고 성공 보고서 한 건을 작성했다.
- direct evidence: focused 두 실패 2/2 통과, dictionary validator 통과, current scene audit 88/88, index 6,379 entries/16 shards/768d status OK. 수리 후 contradiction은 643 preset × 3회 = 1,929 생성에서 violation 0, full unit은 399/399를 통과했다. 최종 real acceptance는 mock=false, dictionary `ad0496…`, generalization 79/79, holdout 24/24, domain v2 6/6, retrieval v4 22/22, diversity 3/3, bleed 4/4, candidate 6/6, visual 12/12와 focus 36/36으로 `passed=true`다.
- remaining gap: 이 목표의 필수 기준은 없다. 선택적 `soft_promotion_ready=false`, status-system의 UI 없는 장르 인접성, lowrider의 암시적 hydraulic motion은 성공 보고서에 제한으로 남긴다. commit/push는 목표 범위 밖이며 별도 사용자 요청 전에는 수행하지 않는다.
- blocker: 없음.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`가 resolved되었고, `docs/passed-reports/2026-08-07-research-scene-expression-render-quality.md`가 8개 criterion matrix와 재사용 경계를 보존한다.
