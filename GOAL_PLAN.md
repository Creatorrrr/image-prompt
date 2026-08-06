# Photo Prompt Subculture Research Expansion Goal

- 작성: 2026-08-06 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 재시도 한계, 중단 조건을 정의한다.

## 1. 목표와 실제 산출물

18개 서브컬처 주제를 신뢰할 수 있는 출처로 조사하고, 조사 결과를 사진 프롬프트 생성기의 증거 원장·taxonomy·candidate-pack·semantic retrieval에 실제 반영한다. 사용자가 한국어 또는 영어로 주제를 명시하면 해당 문화의 참여 방식, 제작 과정, 장소, 물성, 사회적 맥락이 응집력 있는 후보로 노출되어야 하며, 명시하지 않은 일반 프롬프트에는 서브컬처 표지가 새어 나오지 않아야 한다.

실제 산출물은 다음과 같다.

1. 18개 주제를 모두 포함하는 출처 기반 research matrix와 추상화된 `research_evidence.jsonl` 레코드.
2. 일회성 인물 프리셋의 나열이 아니라 여러 주제가 공유할 수 있는 제작·공연·팬덤·게임·차량 계열의 재사용 가능한 slot/facet/family 데이터.
3. 각 주제를 명시적으로 호출할 수 있는 gated preset 또는 동등한 on-demand route와 candidate pack.
4. 한국어·영어 자연어 표현을 고정한 semantic retrieval holdout과 재생성된 semantic index.
5. 기존 일반·안전·테마 누출 계약을 보존한다는 회귀 증거와 독립 검토 결과.

## 2. 범위: 조사할 18개 주제

### A. 팬 창작·출판·가상 창작

1. 코스프레 제작·수선·행사 참여
2. 동인지·Artist Alley·팬 창작 판매 공간
3. zine·risograph·DIY 출판
4. VTuber·virtual creator 제작 환경
5. 아이돌·애니메이션 팬덤의 물질문화

### B. 모형·커스터마이징·메이커 문화

6. 플라모델·garage kit·kitbashing
7. 미니어처·diorama
8. 인형·plush·toy customization
9. fursuit·mascot suit fabrication
10. custom PC·mechanical keyboard·cyberdeck

### C. 패션·공연·음악 현장

11. Lolita coordinate culture
12. Decora·Gyaru·Heisei/Y2K street culture
13. Visual Kei·live-house
14. Goth·Cybergoth·New Romantic·rave
15. DIY punk·noise·shoegaze

### D. 놀이·차량 문화

16. retro gaming·arcade·LAN·speedrun
17. TRPG·miniature wargaming
18. lowrider·tuner·itasha

## 3. 설계 원칙과 불변 조건

- 출처는 박물관·도서관·협회·행사 운영 주체·제작 도구의 공식 문서·학술 자료 등 1차 또는 권위 자료를 우선한다. 커뮤니티 관행은 복수 출처로 교차 확인한다.
- 저장하는 것은 출처 URL, 확인 일자, 추상화된 관찰, 설계 결정뿐이다. 원문 프롬프트·원본 이미지·긴 인용문·개인정보·비공개 커뮤니티 자료는 저장하지 않는다.
- 먼저 기존 slot과 facet을 재사용하고, 여러 주제에서 반복되는 실제 구분을 표현할 수 없을 때만 새 항목을 추가한다.
- 고유명사, 실제 인물, 상표·로고, 특정 저작권 캐릭터의 재현을 taxonomy 핵심으로 삼지 않는다. 시각 언어는 일반화된 제작법·장소·물성·참여 역할로 기술한다.
- 모든 신규 서브컬처 route는 명시적 요청 또는 semantic match에서만 활성화한다. 일반 프롬프트의 자동 선택 pool에는 넣지 않는다.
- 성인·연령 불명 인물은 중립적으로 다루며, 미성년자 성적 대상화, 페티시화, 문화적 조롱을 암시하는 결합은 만들지 않는다.
- 안전 계약은 현재의 단순 기본 통과 구조를 유지한다. 사용자가 별도 안전 평가를 요청하지 않는 한 새 복잡한 평가 workflow를 만들지 않되, 데이터 자체의 명백한 금지 결합과 누출 회귀는 검증한다.
- semantic index sharding은 저장 형식이며 retrieval 의미론을 바꾸지 않는다. 재생성 전후에 manifest/hash와 고정 case를 확인한다.

## 4. 현재 기준선과 승인

- 현재 연구 확장: preset 17개, slot 24개, evidence row 20개.
- 현재 관련 데이터는 `photo_prompt_research_extension.json`에 additive merge되고, semantic index는 생성 산출물이다.
- 기존 일반화·frozen·domain·semantic holdout은 기대값을 결과에 맞춰 약화하지 않는다.
- 과거 자연어 semantic 검증에서 정확한 preset 명칭이 아닌 자유 표현의 라우팅 공백이 관찰되었으므로, 이번에는 주제명 일치만이 아니라 한국어·영어 자연 paraphrase를 먼저 고정한다.
- 사용자는 현재 대화에서 taxonomy text의 Gemini 외부 전송과 semantic index 재생성을 승인했다. 공개·추상화된 taxonomy 문자열에만 사용하고 원문 자료나 민감정보는 전송하지 않는다.
- 이미지 API 생성과 원격 publication은 이번 완료 기준에 포함하지 않는다.

## 5. 실행 단계

### Stage 1 — 기준선·research protocol·고정 case 확정 (`completed`)

- 기존 taxonomy와 18개 주제의 중복/공백을 측정한다.
- 각 주제에 대해 `participation role / activity / setting / object / material / process state / social context / visual boundary`를 기록하는 공통 research matrix를 고정한다.
- 구현 결과를 보기 전에 주제별 한국어·영어 자연어 retrieval case와 허용되는 target family를 작성한다.
- 제품 구속 결정: 기존 extension을 무한히 키우지 않고 별도 subculture extension으로 분리할지, 기존 loader를 재사용할지 저장 크기와 merge 계약을 근거로 확정한다.

### Stage 2 — 18개 주제 병렬 조사와 증거 데이터 반영 (`completed`)

- 주제를 6개 연구 묶음으로 나누어 독립적으로 조사하고, 서로 겹치는 표현과 문화별 고유 경계를 교차 검토한다.
- 각 주제마다 최소 2개의 독립적인 권위 출처를 찾고, 이미지 생성에 유용한 추상 관찰과 피해야 할 과적합 단서를 남긴다.
- 검증된 관찰을 `research_evidence.jsonl`에 append-only로 반영한다.
- 제품 delta: 이후 taxonomy 결정이 출처와 주제에 역추적 가능해진다.

### Stage 3 — 재사용 가능한 taxonomy와 gated route 구현 (`completed`)

- 공통 제작 단계, 행사/공연 단계, 팬 참여 관계, 매체·재료, 장소, 커스터마이징 상태를 재사용 가능한 slot/facet/family로 구현한다.
- 18개 주제 각각에 최소 하나의 명시적 on-demand route를 제공하되, 표현력이 같은 기존 preset은 확장하고 근접 중복 preset은 만들지 않는다.
- subject/action/location/prop/surface가 한 장면으로 결합되도록 required slot과 applicability를 설정한다.
- 제품 delta: 모든 주제에서 문화적으로 구체적이면서 사진적으로 실행 가능한 candidate pack을 만들 수 있다.

### Stage 4 — bilingual semantic retrieval과 index 재생성 (`completed`)

- Stage 1에서 동결한 한국어·영어 자연어 case를 active holdout에 추가한다.
- Gemini embedding으로 semantic index를 재생성하고 monolith/manifest/shard 무결성 및 deterministic ordering을 확인한다.
- 실패 case는 기대값을 바꾸지 않고 aliases, embedding text, family routing, slot coverage 순으로 수정한다.
- 제품 delta: exact preset ID를 모르는 사용자도 명시한 주제의 올바른 route를 발견할 수 있다.

### Stage 5 — candidate pack 품질·누출·회귀 수리 (`completed`)

- 각 주제의 direct route와 bilingual semantic route에서 candidate pack을 생성해 필수 slot, coherence, conflict, applicability, IP/로고 과적합을 검사한다.
- 일반 portrait, 기존 cosplay/fantasy/K-style, 직업, 다큐멘터리 고정 case에서 신규 서브컬처 표지 누출이 0인지 확인한다.
- 발견된 실패는 최대 2회의 원인별 수리 round 안에서 데이터나 라우팅을 고친다.
- 제품 delta: 주제별 표현력과 기존 일반화 보존을 동시에 만족하는 qualified 데이터가 남는다.

### Stage 6 — 닫힌 자격 판정과 독립 감사 (`completed`)

- dictionary validator, focused tests, frozen/generalization/domain/semantic gate, 전체 unit suite를 한 차례 닫힌 순서로 실행한다.
- 독립 서브에이전트가 출처 추적성, 18개 coverage, 누출 방지, 테스트 증거를 한 번 감사한다. 이 감사는 새로운 완료 기준을 추가하지 않는다.
- 모든 기준이 직접 증거로 충족된 경우에만 목표를 완료로 표시한다.

## 6. 완료 기준

1. 18개 주제 각각에 최소 2개의 독립적인 권위 출처와 추상화된 설계 관찰이 연결되고 evidence contract를 통과한다.
2. 18개 주제 모두 명시적인 direct route를 가지며 candidate pack에 일관된 subject/action/location/prop 또는 동등한 필수 축이 포함된다.
3. 신규 데이터가 재사용 가능한 공통 family/slot/facet을 중심으로 설계되고, 이름만 다른 근접 중복 preset과 특정 IP·실존 인물·브랜드 의존 항목이 없다.
4. 구현 전에 동결한 한국어·영어 자연어 case가 기대 family/route를 발견하며, 실패 기대값을 사후 완화하지 않는다.
5. 신규 route는 on-demand로만 활성화되고 기존 generic/K-style/fantasy/cosplay 및 일반 주제 고정 case의 theme leakage가 0이다.
6. dictionary validator, semantic index metadata/hash/shard integrity, contradiction/applicability 및 candidate-pack contract가 모두 통과한다.
7. 기존 public generalization, frozen holdout, domain holdout, 기존 semantic holdout과 전체 unit suite가 회귀 없이 통과한다.
8. 최종 독립 감사에서 18개 coverage·출처 추적성·과적합 방지·검증 증거에 미해결 중대 결함이 없다.

## 7. 검증·재시도 계약

- 초기 case와 target family는 index 재생성 전에 저장하고 이후 실패를 이유로 삭제하거나 약화하지 않는다.
- 변경 영역별 focused test를 먼저 실행하되, 전체 suite는 Stage 6에서 한 번 실행한다.
- 같은 근본 원인의 구현 재시도는 최대 2회다. 반복되는 material failure는 재시도 전에 `docs/failed-reports/`에 sanitized evidence와 함께 기록한다.
- 네트워크·외부 embedding의 일시 오류는 한 번 재시도할 수 있다. 반복되면 로컬 데이터 구현을 보존하고 external gate를 명시적 blocker로 보고한다.
- visual quality는 구조적 prompt/candidate 품질까지만 주장한다. 실제 렌더 품질은 별도의 이미지 생성·visual review 없이는 주장하지 않는다.

## 8. 중단 조건과 비목표

다음은 자동 확장하지 않는다.

- 유료 이미지 생성 또는 대규모 visual A/B.
- 실제 브랜드·캐릭터·연예인 식별을 위한 데이터셋 구축.
- frozen holdout 기대값 약화, 기본 generic selection 의미 변경, ANN/근사 검색 도입.
- 저장소 밖 배포, 커밋, push, PR 생성. 사용자가 별도로 요청할 때만 수행한다.

이번 목표의 비목표:

- 모든 지역·시대 변형을 완전하게 백과사전화하기.
- 커뮤니티 구성원의 정체성을 고정된 외형 stereotype으로 환원하기.
- 18개 주제별로 이미지를 생성해 렌더 품질을 입증하기.

## 9. 실행 지식 계약

- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/`의 파일명과 header metadata를 먼저 검색하고, 전문은 가장 관련된 non-superseded 보고서 최대 5개만 읽는다.
- 현재 소스와 직접 측정한 증거가 과거 보고서와 기억보다 우선한다.
- credential, token, secret, 민감 endpoint, 개인정보를 계획·보고서·증거 원장에 저장하지 않는다.
- passed report는 모든 완료 기준을 통과한 뒤 material failure 해결, 기본 접근 실패 뒤의 비자명한 대안, 또는 값비싼 다단계 재현 중 하나에 해당할 때만 목표당 최대 1개 작성한다.
- 각 checkpoint는 제품/사용자 관찰 delta, 직접 증거, 구속 결정, 다음 단계, 열린 위험을 기록한다.

## 10. 진행 기록

### 2026-08-06 / 목표 초기화

- 기존 `GOAL_PLAN.md`의 창의성 목표가 `complete`임을 확인하고 이번 목표로 교체했다.
- 작업트리는 clean, branch는 `main`, 기준 commit은 `cfd8e92`다.
- `docs/failed-reports/`와 `docs/passed-reports/`에는 template 외 보고서가 없어 상충하는 실행 지식이 없다.
- 현재 연구 확장 기준선은 preset 17개, slot 24개, evidence 20행이다.
- 다음 단계: 고정 bilingual case와 공통 research matrix를 작성하고 18개 주제 병렬 조사를 시작한다.

### 2026-08-06 / Stage 1

- 제품 또는 사용자 관찰 delta: 아직 runtime 동작을 바꾸기 전에 18개 대주제와 그 안의 서로 다른 실천을 구분하는 bilingual semantic case 70개를 `semantic_retrieval_holdout_subculture_v1.jsonl`로 동결했다.
- 직접 증거:
  - JSONL 70행이 모두 parse되고 retrieval holdout loader의 schema validation을 통과했다.
  - Lolita/Decora/Gyaru/Y2K, goth/cybergoth/New Romantic/rave, punk/noise/shoegaze, arcade/LAN/speedrun, TRPG/wargaming, PC/keyboard/cyberdeck, lowrider/tuner/itasha를 서로 다른 target route로 고정했다.
  - 기존 `lowrider_night_meet`는 자동차·제작·공동체가 아니라 `fashion_model + standing_silence + underground_parking_lot + neon`이어서 새 lowrider route의 기반으로 사용하지 않기로 했다.
  - 기존 `warehouse_rave_uv`의 잘못된 family와 `punk_basement_show`의 glow-stick/UV 누출은 신규 데이터 추가와 함께 교정할 대상으로 고정했다.
- 구속 결정:
  - 기존 112 KB 연구 extension을 계속 비대하게 만들지 않고 같은 additive schema를 쓰는 `photo_prompt_subculture_extension.json`을 별도 로드한다.
  - 여러 문화를 한 preset의 무작위 cross-product로 섞지 않는다. 공통 slot/facet은 재사용하되 문화적으로 다른 실천은 별도 on-demand preset으로 둔다.
  - 공통 research matrix 축은 `participant role`, `workflow state`, `authorship/rights relation`, `venue/presentation context`, `material/media basis`, `social relation`, `visual boundary`로 고정한다.
- 다음 단계: 서브에이전트의 권위 출처 조사를 모두 회수해 evidence row와 reusable taxonomy로 변환한다.
- 열린 위험: 70개 real-embedding retrieval case는 index 재생성 전에는 의도적으로 실패한다. 기대 route를 결과에 맞춰 변경하지 않는다.

### 2026-08-06 / Stage 2

- 제품 또는 사용자 관찰 delta: 18개 상위 주제를 공식 행사 규칙, 박물관·보존기관 자료, 공식 제작 문서와 학술 자료로 조사하고, 선별한 독립 출처 46개를 기존 원장에 append-only로 연결했다.
- 직접 증거:
  - `research_evidence.jsonl`은 총 66행, 고유 ID 66개이며 신규 `subculture_practice` 행은 서로 다른 URL 46개다.
  - 모든 evidence `candidate_ids`가 병합된 5,607개 preset/slot ID 카탈로그의 부분집합이다.
  - 고정된 18개 theme-to-route 집합 각각에 서로 다른 출처 URL이 최소 2개 존재한다.
- 구속 결정:
  - 원문·이미지·특정 캐릭터 디자인은 저장하지 않고, 역할·공정·물성·권리 관계·행사 단계만 추상화했다.
  - 출처 수를 늘리는 것보다 서로 다른 세부 실천의 경계를 설명하는 자료를 우선해 46개 행으로 제한했다.
- 다음 단계: bilingual holdout을 실제 index에 연결한다.
- 열린 위험: 출처 근거는 taxonomy 설계의 추적성을 입증하지만 실제 렌더 품질을 입증하지 않는다.

### 2026-08-06 / Stage 3

- 제품 또는 사용자 관찰 delta: 별도 `photo_prompt_subculture_extension.json`에 신규 preset 33개와 기존 punk/rave 교정 route 2개, 공통 family 6개, 재사용 slot entry 179개를 구현했다.
- 직접 증거:
  - dictionary validator가 병합 사전의 ID·filter·facet 참조를 통과했다.
  - 35개 direct route를 seed별로 실제 실행해 모든 required slot이 선택되고 선택값이 authored filter에 속함을 확인했다.
  - `subculture_practice` route는 사용자 intent가 같은 domain으로 라우팅된 경우에만 자동 발견되며, direct preset 호출은 유지된다.
  - 잘못된 기존 `lowrider_night_meet`는 direct-ID 호환만 남기고 자동 pool과 semantic index 대상에서 제외했다.
- 구속 결정:
  - 일반 성인 연령 표지를 성인 콘텐츠와 혼동하지 않도록 `age_context_only`를 도입했다. 안전 기본 통과 계약은 그대로다.
  - surface/capture applicability와 camera/light/texture authored defaults를 확장 파일에서만 추가해 legacy 세부항목 누출을 막았다.
- 다음 단계: 승인된 taxonomy 문자열로 semantic index를 재생성하고 70개 고정 retrieval case를 실행한다.
- 열린 위험: 실제 embedding ranking에서 근접한 패션·음악·팬덤 세부 route가 혼동될 수 있다. 기대 target은 변경하지 않고 데이터 표현을 수정한다.

### 2026-08-07 / Stage 4

- 제품 또는 사용자 관찰 delta: 한국어·영어 70개 자연어 문장이 exact preset ID를 몰라도 35개 세부 실천 route를 각각 발견하며, 별칭이 없는 서브컬처 표현은 기존 semantic fallback을 유지한다.
- 직접 증거:
  - 승인된 공개 taxonomy 문자열만 Gemini embedding에 전송해 index를 재생성했다. 최종 index는 `gemini-embedding-2`, 768차원, 5,697개 entry, 16개 shard이며 dictionary hash는 `a9134e078d28ac0da2b34ca01b57db13289d4bab8082c7530a56e09ea3e63346`다.
  - manifest hash, shard별 hash, entry 합계와 순서를 독립 계산해 monolith와 일치함을 확인했고 `--check-index`가 통과했다.
  - 초기 real retrieval은 30/70이었다. 기대값은 유지하고 대분류 alias 정규화와 명시적 실천어 기반 `scoped_routes`를 추가한 뒤 기본 seed의 동일 70개 case가 70/70 통과했다.
  - `scoped_routes` 정책은 35개 route와 정확히 대응하고, 70개 고정 문장 각각을 하나의 기대 route로만 좁힌다는 구조 테스트가 통과했다.
- 구속 결정:
  - 세부 장르 간 혼동을 preset weight로 과적합하지 않고, canonical bilingual 실천어가 실제로 일치할 때만 같은 domain의 후보를 제한한다.
  - generic `cosplay`라는 단어만으로 제작 route를 강제하지 않아 “fashion rather than cosplay” 같은 부정 비교와 기존 cosplay portrait를 오염시키지 않는다.
- 다음 단계: 기존 semantic holdout, 일반화·frozen·domain gate와 direct candidate pack 누출 검사를 실행한다.
- 열린 위험: 고정 alias 밖의 매우 간접적인 표현은 semantic fallback 품질에 의존한다. 이번 완료 범위는 동결한 자연어 case와 generic 누출 보존까지다.

### 2026-08-07 / Stage 5

- 제품 또는 사용자 관찰 delta: 35개 세부 route가 응집된 candidate pack을 만들면서 일반 portrait, K-style, fantasy/cosplay, 직업·차량 다큐멘터리 요청에는 신규 서브컬처 domain과 route가 활성화되지 않는다.
- 직접 증거:
  - 35개 direct route를 실제 생성해 각 preset의 필수 `subject/action/location/prop` 축과 모든 authored filter 선택을 검증했다.
  - 신규 extension에는 대표적인 특정 IP·캐릭터·플랫폼·행사 브랜드 이름이 없고, 기존 generic/K-style/fantasy/cosplay/직업 negative control에도 `subculture_practice` 또는 세부 route가 검출되지 않았다.
  - public generalization 79/79, frozen holdout 24/24, domain holdout v2 6/6, 기존 semantic retrieval v4 22/22가 통과했다.
  - contradiction gate는 605개 preset을 각 3회, 총 1,815개 생성해 violation 0을 기록했다.
- 구속 결정:
  - 명시적 세부 실천어가 없는 경우 35개 신규 route를 자동 pool에서 계속 제외한다. 새로운 전역 가중치나 기존 preset 기대값 변경은 하지 않았다.
  - 실제 이미지 생성은 승인 범위와 완료 기준 밖이므로 candidate pack의 구조적 사진 실행 가능성까지만 판정한다.
- 다음 단계: validator·index·전체 test suite를 닫힌 순서로 한 번 실행하고 독립 감사를 받는다.
- 열린 위험: 렌더 모델별 시각 품질과 고정 case 밖의 희귀 은어 표현은 이번 검증만으로 보장하지 않는다.

### 2026-08-07 / Stage 6

- 제품 또는 사용자 관찰 delta: 18개 서브컬처의 출처 기반 후보가 direct ID와 한국어·영어 자연어로 호출되며, 기존 일반 주제와 결정론적 golden 결과를 보존하는 qualified 데이터 상태가 됐다.
- 직접 증거:
  - 최종 dictionary validator와 semantic `--check-index`가 통과했다. index는 5,697 entry, 768차원, 16개 shard, dictionary hash `a9134e078d28ac0da2b34ca01b57db13289d4bab8082c7530a56e09ea3e63346`다.
  - 첫 전체 suite는 전역 human surface applicability가 기존 golden의 RNG를 바꾼 누출을 발견해 `414 passed, 722 subtests passed, 1 failed`로 닫혔다. fixture는 바꾸지 않고 typed-domain override로 수리했다.
  - 집중 golden 5/5, subculture focused 3/3, 수리 후 전체 suite `414 passed, 723 subtests passed`가 통과했다.
  - 독립 read-only 감사가 8개 완료 기준을 모두 PASS로 판정했고 중대 blocker 없이 `QUALIFIED PASS`를 반환했다.
  - material failure와 수리 절차는 `docs/failed-reports/` 두 건에, 재사용 가능한 성공 절차는 `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`에 기록했다.
- 구속 결정:
  - golden drift를 신규 기능의 의도된 변화로 취급하지 않았다. 일반 human slot pool은 이전 의미를 유지하고 `subculture_practice`에서만 좁은 예외를 허용한다.
  - source traceability와 구조적 candidate-pack 품질까지만 완료로 판정한다. 이미지 렌더 품질은 별도 이미지 생성·visual review가 없으므로 주장하지 않는다.
- 다음 단계: 없음. 커밋·push·이미지 생성은 사용자가 별도로 요청할 때만 수행한다.
- 열린 위험: 매우 간접적인 희귀 은어는 semantic fallback 품질에 의존하며, 모델별 렌더 결과는 검증되지 않았다. 둘 다 이번 목표의 명시적 완료 범위 밖이다.

## Codex 실행 프롬프트

`/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Resume from its latest checkpoint, scan only relevant report metadata before acting, deliver product deltas before expanding verification, persist material failures before retry, obey the stop conditions, and mark the goal complete only when every completion criterion has direct evidence.`
