# CJK Commercial Narrative Worldbuilding Expansion Goal

- 작성: 2026-08-07 14:16 KST
- 상태: completed
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@3ba2805`
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 진척 계약, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`

## 1. 목표와 실제 산출물

한중일 소설·만화·애니메이션·게임 업계에서 공식 장르, 플랫폼 태그, 시장 관용어, 비평 용어로 지칭되는 20개 서브컬처 세계관 클러스터를 신뢰할 수 있는 공개 출처로 모두 조사하고, 사진 프롬프트 생성기의 evidence ledger, 별도 CJK taxonomy, candidate pack, 한국어·영어·중국어·일본어 semantic retrieval에 실제 반영한다.

완료 후 사용자는 한국어 또는 관련 원어로 세계관을 요청해 대표 의상이나 장르 분위기만이 아니라 제도, 파벌, 자원경제, 의례·금기, 역사층, 정보 권위, 상태 시스템 중 최소 세 축이 장소·행동·도구·기록·마모 같은 관찰 가능한 증거로 연결된 오리지널 장면을 생성할 수 있어야 한다. 일반적인 인물·거리·판타지·문화 요청에는 CJK 특수 세계관 표지가 자동으로 새어 나오지 않아야 한다.

주요 제품 산출물은 다음과 같다.

1. 20개 주제의 원어 용어 층위, 출처, 세계 작동 규칙, 사진 가능한 증거, IP·문화 경계가 runtime candidate ID에 연결된 `research_evidence.jsonl` 확장.
2. 기존 일반 worldbuilding 파일과 분리된 `assets/photo_prompt_cjk_worldbuilding_extension.json` additive taxonomy. 기존 loader 계약으로 표현할 수 없다는 직접 증거가 있을 때만 최소 schema 변경을 허용한다.
3. 각 주제의 명시적 on-demand scoped route와 candidate pack. 각 route는 최소 두 개의 원자적 scene manifestation과 `subject/action/location/prop` 및 최소 세 개의 세계 작동 증거를 제공한다.
4. 구현 전에 동결한 한국어·영어·중국어·일본어 100개 preset-free retrieval holdout과 승인된 공개·추상 taxonomy 문자열로 재생성한 semantic index.
5. 기존 안전 자동 통과, candidate cap, generic theme leakage, deterministic golden, subculture, worldbuilding, frozen retrieval 계약을 보존하는 직접 검증 결과.

## 2. 조사하고 반영할 20개 주제

### A. 최우선 시장 세계관

1. 한국형 헌터·게이트·레이드 사회 — `헌터물`, `게이트물`, `던전물`, `각성자`
2. 탑등반·성좌·후원자 생태계 — `탑등반물`, `성좌물`, `시나리오`, `후원`
3. 중국 선협·수선 종문 세계 — `仙侠`, `修仙`, `宗门`, `境界`, `渡劫`
4. 현환·고무 문명과 선택적 영기부활 변형 — `玄幻`, `高武世界`; `灵气复苏`, `万族入侵`은 독립 선택 facet
5. 무한류·제천무한·부본 세계 — `无限流`, `诸天无限`, `副本`, `主神空间`
6. 일본식 이세계 생활권 — `異世界転生`, `異世界転移`, `冒険者ギルド`, `スローライフ`
7. 현대 던전·탐색자 방송 경제 — `現代ダンジョン`, `探索者`, `ダンジョン配信`
8. 규칙괴담·괴이부활·이상구역 — `规则怪谈`, `诡异复苏`, `怪谈副本`

### B. 제도·역사·문화 세계관

9. 현대전기·도시괴이·퇴마 조직 — `伝奇`, `怪異`, `妖怪`, `陰陽師`, `異能バトル`, `도시괴담`, `퇴마물`
10. 회귀·빙의·환생·천월의 시간 규칙 — `회빙환`, `책빙의`, `게임빙의`, `転生`, `憑依`, `穿越`, `重生`
11. 아카데미·명문가·이능 교육제도 — `아카데미물`, `명가물`, `異能学園`, `魔術学院`, `超能力学院`
12. 로맨스판타지·악역영애·오토메게임 귀족사회 — `로판`, `악녀물`, `북부대공`, `悪役令嬢`, `乙女ゲーム`, `古言`
13. 무협·무림·강호의 사회경제 — `무협`, `무림`, `강호`, `문파`, `武侠`, `江湖`, `门派`, `镖局`
14. 동아시아 신령·저승 관료제 — 한국 무속·도깨비·저승, 중국 `地府`, `妖怪`, `山海`, 일본 `黄泉`, `八百万`, `付喪神`

### C. 시스템·미디어·운영 세계관

15. 상태창·시스템·직업·퀘스트 세계 — `상태창`, `시스템물`, `系统流`, `ステータス`, `スキル`
16. VRMMO·게임판타지·카드·가챠 세계 — `게임판타지`, `VRMMO`, `虚拟网游`, `游戏异界`, `電子競技`, `カードバトル`
17. 메카·괴수·특촬형 재난국가 — `ロボット`, `メカ`, `怪獣`, `特撮`, `変身ヒーロー`
18. 아포칼립스·비축·기지건설 — `아포칼립스물`, `재난생존`, `末世`, `囤货`, `基地建设`, `終末もの`
19. 영지·국가·던전 경영과 개척 — `영지물`, `국가경영물`, `던전운영물`, `领主`, `种田`, `基建`, `領地経営`, `開拓`
20. 마법소녀·아이돌·버추얼 크리에이터 미디어믹스 — `魔法少女`, `アイドル`, `変身`, `아이돌물`, `인방물`, `虚拟偶像`

## 3. 범위와 비목표

### 범위

- 공식 플랫폼 분류·태그, 출판사·제작사·게임사 자료, 공공 문화기관, 학술 원문, 창작자 또는 업계 인터뷰 등 공개 1차·권위 출처를 우선한다.
- 각 주제는 최소 3개의 독립 공개 URL을 갖고, 그중 최소 1개는 공식 플랫폼·산업·제작 주체의 1차 출처여야 한다. 공식 장르, 플랫폼 태그, 시장 관용어, 비평 용어를 `term_level`로 구분하고 서로 다른 용어를 거짓 동의어로 병합하지 않는다.
- 각 주제마다 최소 5개의 세계 작동 규칙, 최소 6개의 사진 가능한 evidence candidate, 최소 3개의 IP·문화·표현 경계를 기록한다.
- 세계 작동 축은 `institution / faction_relation / resource_economy / ritual_taboo / historical_layer / language_script / knowledge_authority / evidence_reliability / progression_system / media_economy` 중 선택한다.
- `헌터물`, `現代ダンジョン`, `高武·灵气复苏`처럼 인접하지만 사회 시스템이 다른 클러스터는 별도 route로 유지한다. `회빙환`처럼 서사 장치인 주제는 시간 기록, 원작 강제력, 분기 흔적, 기억 권위처럼 사진 가능한 세계 증거로 변환한다.
- 신령·무속·저승 주제는 실제 살아 있는 신앙이나 민족 전통을 장식적 스타일로 평면화하지 않는다. 공개 문화·학술 자료로 확인 가능한 추상 구조만 사용하고 비공개·성스러운·제한 지식을 수집하지 않는다.
- 특정 프랜차이즈를 증거로 참조할 수는 있으나 runtime taxonomy에는 작품명, 캐릭터, 고유 문양, 고유 UI, 고유 조직, 문장 또는 원문을 넣지 않는다.
- 이전 사용자 승인 범위에 따라 semantic index 재생성을 위해 공개·추상 taxonomy 문자열과 retrieval query만 Gemini로 전송할 수 있다. 출처 원문, 이미지, 개인정보, 비공개 자료, 실행 로그는 전송하지 않는다.

### 비목표

- 특정 작품·게임·애니메이션·캐릭터·실존 인물·단체 로고·브랜드 세계관을 복제하는 데이터 구축.
- 한중일 산업 전체를 완전하게 대표하거나 각 용어가 세 국가에서 같은 뜻이라고 주장하기.
- 살아 있는 종교 의례의 실제 수행 지침, 위험한 오컬트 절차, 폭력·무기 제작법을 제공하기.
- 새 범용 evaluator framework, 별도 데이터베이스, 서비스 또는 복잡한 안전 승인 흐름을 만드는 것.
- 렌더 이미지 품질을 실제 이미지 생성·검토 없이 주장하기. 이미지 생성, 배포, push, PR은 사용자가 별도로 요청할 때만 수행한다.
- 테스트·문서·schema·semantic index만 증가하고 20개 route가 실제 candidate pack으로 도달하지 못한 상태를 완료로 간주하기.

## 4. 진척 계약

- 진척으로 인정: evidence가 runtime candidate ID에 연결됨, 별도 CJK taxonomy가 loader에서 사용됨, 주제 route가 실제 candidate pack을 생성함, 동결 원어 자연어가 실제 route를 발견함, 또는 제품 범위를 구속하는 구현 결정이 직접 증거와 함께 확정됨.
- 진척으로 인정하지 않음: 링크나 장르명만 수집함, 계획·문서·테스트·fixture·검증기만 추가함, 의상·무기·색감 같은 고립 vocabulary만 추가함, 실패한 기대값을 사후 삭제·완화함.
- Stage 1 이후 각 checkpoint는 실제 데이터/동작 delta 또는 측정된 candidate 결과를 남긴다. 검증-only checkpoint를 두 번 연속 만들지 않는다.
- 검증-only 작업 상한: 변경 중 focused 검증, Stage 4의 index/retrieval 검증, Stage 6의 닫힌 최종 회귀·독립 감사 한 번. 새 평가 framework는 기존 경로로 필수 기준을 검증할 수 없다는 직접 증거가 있을 때만 허용한다.
- 실행 지식 작업 상한: 시작·재개 시 metadata 우선으로 관련 보고서 전문 최대 5건, material failure당 통합 보고서 1개, 모든 기준 통과 뒤 closed qualification을 만족하는 성공 보고서 기본 최대 1개. 보고서는 별도 checkpoint나 진척이 아니다.
- 자동 목표 상향은 비활성이다.

## 5. 기준선과 적용할 실행 지식

### 현재 기준선

- branch/ref: clean `main@3ba2805`, `origin/main`보다 3 commit ahead
- 기존 subculture extension: 33개 on-demand practice preset
- 기존 general worldbuilding extension: 18개 on-demand world-system preset, 288 slot entry
- evidence ledger: 120행
- semantic index: Gemini `gemini-embedding-2`, 768 dimensions, 6,003 entries, 16 shard
- 기존 신규 worldbuilding retrieval: 72/72, 기존 semantic retrieval v4: 22/22
- 안전 계약: 사용자가 안전 평가를 별도 요청하지 않는 한 단순 automatic pass

### 적용할 과거 보고서

- `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`
  - bilingual 기대를 구현 전에 동결하고, 별도 additive extension·typed domain·scoped route·두 atomic scene·관찰 가능한 world-evidence slot 방식을 재사용한다.
  - 설명 전용 schema나 costume/mood preset 대신 기존 `subject/action/location/prop/situation/occasion/narrative/capture/procedure/surface` 축을 우선한다.
- `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`
  - specialty marker를 일반 요청과 격리하고 shared family/slot을 우선하며, 실제 semantic route와 generic negative control을 함께 검증한다.
- `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`
  - Gemini 현재 경로는 multi-input cardinality가 검증되지 않았으므로 index 재생성은 `--batch-size 1`과 cache/checkpoint를 유지한다.
- `docs/failed-reports/2026-08-07-subculture-surface-applicability-golden-drift.md`
  - global subject-category 또는 optional pool을 넓히지 않고 typed-domain narrow override를 사용해 unrelated RNG/golden을 보존한다.
- `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`
  - exact user-authored CJK scoped route가 resolve되면 nearby generic semantic preset과 경쟁시키지 않으며, 인접 CJK route끼리는 false synonym이 되지 않도록 distinction case를 고정한다.

현재 소스와 직접 측정한 증거가 보고서보다 우선한다. integration 또는 SDK가 바뀌어 교훈이 무효화되면 해당 lifecycle과 상호 링크를 같은 변경에서 갱신한다.

## 6. 실행 단계

| 단계 | 실제 산출물 또는 동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 기준선·용어 계약·동결 case | 별도 `cjk_narrative_world` domain과 additive extension 설계를 확정하고, 20 route × 5개인 100개 preset-free 자연어 case를 구현 전에 동결한다. 각 route는 한국어 2개, 영어 1개, 관련 중국어·일본어 원어 2개를 기본으로 하되 기원 시장에 맞춰 원어 분포를 기록한다. | JSONL parse/schema, ID·target uniqueness, 모든 route 5개, 인접 route distinction matrix 직접 검토 | runtime 구현을 보지 않고 100개 기대와 20개 route ID, `term_level/market_origin` 계약이 고정됨 |
| 2. 20개 병렬 조사와 evidence 반영 | 최대 8개 독립 연구 묶음으로 공식 플랫폼·산업·학술 출처를 조사하고, 원문을 복사하지 않은 추상 evidence row를 ledger에 append한다. | 주제별 URL·source type·term level·world mechanism·boundary·candidate ID 참조 검사 | 20/20 주제가 독립 URL 3개 이상, 공식/1차 출처 1개 이상, 필수 research matrix를 충족함 |
| 3. CJK taxonomy와 on-demand route 구현 | 별도 CJK extension, shared families/slots/facets, loader merge, typed domain, 주제별 scoped route를 구현한다. 각 route는 두 atomic scene과 최소 세 개의 관찰 가능한 세계 작동 증거를 제공한다. | dictionary validator, 20 direct route × seed 2개의 candidate pack, scene-tag 원자성·candidate cap | 20/20 route가 실제 pack을 만들고 각각 서로 다른 두 scene이 도달 가능하며 isolated costume/mood preset이 아님 |
| 4. 다국어 semantic retrieval과 index 반영 | 100개 frozen case를 active retrieval에 연결하고 승인된 추상 taxonomy text만 사용해 cache 재사용·batch 1로 semantic index를 재생성한다. | manifest/hash/shard/order check와 동일한 100개 real retrieval | 기대값 완화 없이 100/100가 의도 route를 찾고 인접 route distinction 및 index 무결성이 통과함 |
| 5. 과적합·문화 경계·누출 수리 | 모든 route의 pack을 검사해 세계 규칙 응집성, IP 의존, 원어 false synonym, 문화 flattening, generic leakage를 데이터·라우팅 원인에서 최대 2회 수리한다. | route별 fixed-seed pack, protected-reference scan, generic/K-style/fantasy/cosplay/occupation 및 adjacent-CJK negative controls, 기존 focused holdout | measured CJK leakage 0, 보호 대상 고유표현 0, provenance/term-level 경계 유지, 기존 focused 회귀 pass |
| 6. 닫힌 최종 자격 판정 | validator, index, contradiction/applicability, 기존 public/frozen/subculture/worldbuilding/CJK retrieval과 전체 unit suite를 한 번 실행하고 독립 서브에이전트가 기존 완료 기준만 재검토한다. | 명령별 exit/result와 criterion matrix | 아래 8개 완료 기준이 모두 pass이며 독립 감사에 미해결 중대 결함이 없음 |

## 7. 최종 완료 기준

1. 20개 주제 모두 독립 공개 URL 3개 이상, 공식·1차 출처 1개 이상, 세계 작동 규칙 5개, 사진 가능한 evidence 6개, IP·문화·표현 경계 3개 이상이 runtime candidate ID와 연결된다.
2. 공식 장르·플랫폼 태그·시장 관용어·비평 용어의 층위와 시장 기원이 보존되고, `헌터물`, `現代ダンジョン`, `高武·灵气复苏` 같은 인접어가 거짓 동의어로 합쳐지지 않는다.
3. 20개 모두 명시적 on-demand route를 가지며 실제 candidate pack에 `subject/action/location/prop`과 최소 세 개의 세계 작동 증거가 포함된다.
4. 각 주제에서 두 개 이상의 서로 다른 원자적 scene manifestation이 도달 가능하고, 결과가 하나의 의상·무기·문양·색감·상태창에만 의존하지 않는다.
5. 신규 taxonomy는 shared family/slot/facet 중심이며 특정 IP·브랜드·캐릭터·실존 인물·고유 UI·실제 제한 의례에 의존하지 않는다. 문화·신앙 provenance 경계가 구조적으로 유지된다.
6. 구현 전 동결한 100개 한국어·영어·중국어·일본어 자연어 case가 기대 route를 100/100 발견하며 실패 기대값을 삭제·완화하지 않는다.
7. 신규 route는 명시적 요청에서만 활성화되고 기존 generic/K-style/fantasy/cosplay/occupation 및 인접 CJK negative control의 측정된 신규 theme leakage가 0이다.
8. dictionary, semantic manifest/hash/shard/order, candidate-pack integrity, contradiction/applicability, 기존 public/frozen/domain/subculture/worldbuilding/retrieval holdout과 전체 unit suite가 통과하고, 한 번의 독립 감사가 미해결 중대 결함을 찾지 않는다.

## 8. 검증 수준과 재시도 예산

- 위험 수준: 중간. 로컬 데이터·라우팅 변경이며 배포나 외부 사용자 상태 변경은 없지만 semantic retrieval, deterministic output, 언어·문화 구분에 회귀 위험이 있다.
- 반복 중 focused 검증: 변경한 CJK extension/loader/route, direct generation, frozen 100개 retrieval만 실행한다.
- 최종 검증: Stage 6에서 기존 전체 회귀와 독립 감사를 한 번 수행한다. 독립 감사는 새 성공 기준을 추가하거나 제품을 재설계하지 않는다.
- 동일 근본 원인의 데이터/라우팅 수리는 최대 2회다. 두 번 실패하면 기준을 약화하거나 verifier를 확장하지 않고 material failure를 기록해 blocker와 가장 작은 선택지를 보고한다.
- 네트워크 또는 Gemini 일시 오류는 한 번 재시도한다. 반복되면 로컬 taxonomy 구현을 보존하고 external retrieval gate만 분리해 보고한다.
- semantic index는 현재 검증된 `--batch-size 1`을 사용한다. 변경하려면 별도 cardinality probe의 직접 성공 증거가 필요하다.
- 실제 렌더 품질은 이번 목표에서 주장하지 않는다. 구조적 prompt/candidate 품질과 semantic 접근성까지만 자격을 부여한다.

## 9. 중단하고 질문할 조건

- 기존 승인 범위를 넘어서는 출처 원문·비공개 자료·이미지·개인정보의 외부 전송이 필요할 때.
- 기존 frozen 기대를 약화해야만 통과하거나 generic 기본 선택 의미를 바꿔야 할 때.
- 특정 문화·신앙의 비공개·성스러운·접근 제한 자료 없이는 구현할 수 없을 때. 공개 산업·문화 자료로 축소하는 선택지를 먼저 제시한다.
- 유료 서비스, 이미지 대량 생성, 파괴적 변경, 배포, push, PR 또는 20개 밖의 실질적 범위 확대가 필요할 때.
- 같은 원인의 수리 2회와 외부 오류 1회 재시도 후에도 필수 기준이 실패할 때.

## 10. 실행 지식 계약과 진행 로그

- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/`의 파일명·header metadata를 먼저 검색하고 exact path/module/environment/error/approach match를 우선한다. non-superseded와 최신 항목을 우선하고 전문은 기본 최대 5건만 읽는다. 현재 소스와 직접 증거가 항상 우선한다.
- 보고서나 로그를 쓰기 전에 시스템 날짜·시간을 얻고 credential, token, secret, 민감 endpoint, 고객·개인정보를 제거한다. 출처 원문을 저장하지 않고 sanitized 결론과 공개 URL만 남긴다.
- 완료 기준을 무효화하거나 rollback·redesign·blocker를 만드는 material failure는 재시도 전에 기존 matching report를 갱신하거나 `docs/failed-reports/YYYY-MM-DD-<slug>.md`에 통합한다. transient typo는 기록하지 않는다.
- 모든 완료 기준이 직접 증거로 통과한 뒤에만 성공 보고서를 고려한다. 성공은 `material failure 해결`, `고정 조건에서 기본 접근 실패 후 비자명한 대안`, `현재 코드에서 값싸게 복구할 수 없는 다단계 재현 절차` 중 하나를 명시적으로 충족할 때만 목표당 기본 최대 1개 작성한다. 단순 테스트 통과나 편리한 명령은 성공 보고서가 아니다.
- failure 해결, 성공 무효화, supersession이 발생하면 양방향 lifecycle 링크를 같은 변경에서 갱신한다. 빈 optional section은 제거한다.
- 진행 로그 형식: `product delta -> direct evidence -> remaining product gap -> blocker -> execution-knowledge paths`.

### 2026-08-07 / 목표 초기화

- product delta: 완료된 18개 일반 세계관 목표를 20개 CJK 상업 서사 세계관 목표로 교체하고, 별도 additive extension, 원어 용어 층위, 100개 사전 동결 retrieval, route별 두 atomic scene 계약을 확정했다.
- direct evidence: clean `main@3ba2805`; 기존 general worldbuilding 18 route와 semantic index 6,003 entry/16 shard; 선행 목표의 validator, 72/72 retrieval, 전체 393 tests, 독립 감사가 통과한 기준선.
- remaining product gap: 신규 CJK research evidence, 20개 executable route, 다국어 retrieval/index, leakage·회귀 자격 판정이 아직 없다.
- blocker: 없음. 공개·추상 taxonomy 문자열과 query의 Gemini 전송 및 semantic index 재생성은 이전 사용자 승인 범위 안에서 수행한다.
- execution-knowledge paths: `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`, `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`, `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`, `docs/failed-reports/2026-08-07-subculture-surface-applicability-golden-drift.md`, `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`.

### 2026-08-07 / Stage 1 CJK 용어·route·retrieval 기대 동결

- product delta: `semantic_retrieval_holdout_cjk_worldbuilding_v1.jsonl`에 20개 route별 5개, 총 100개의 preset-free 기대를 구현 전에 동결했다. 한국 기원 route는 한국어 3개·영어 2개, 중국·일본 기원 route는 한국어 2개·영어 1개·해당 원어 2개, 교차 route는 한국어 2개·영어 1개·중국어 1개·일본어 1개로 고정했다.
- direct evidence: JSONL 100행이 모두 parse되고 ID 100개와 target route 20개가 유일하며, 각 route가 정확히 5행을 가진다. 기존 extension merge는 새 facet vocab·preset·slot·applicability를 표현할 수 있으므로 `photo-prompt-research-extension/v1` schema는 유지한다.
- binding implementation decision: 별도 `photo_prompt_cjk_worldbuilding_extension.json`과 새 typed domain `cjk_narrative_world`을 사용한다. `market_origin = kr/cn/jp/cross_cjk`를 유지하고 `term_level`은 조사 결과에 맞춰 `official_platform_category / official_required_keyword / literary_genre / platform_tag / market_term / market_trope / market_subtype / market_shorthand / critical_analytic_label / game_derived_lexicon / industry_term / production_form / living_practice_boundary`처럼 출처 층위를 보존한다. 특히 `高武`, `灵气复苏`, `万族入侵`, `異世界転生`, `異世界転移`, `회귀`, `빙의`, `환생`, `古言`, `悪役令嬢`를 동일 alias로 병합하지 않는다. 기존 열 개 world-evidence slot을 재사용하며 설명 전용 slot은 만들지 않는다.
- remaining product gap: 20개 research matrix와 evidence ledger, CJK extension·loader·domain routing, semantic index와 100/100 real retrieval이 아직 없다.
- blocker: 없음. 8개 읽기 전용 연구 묶음이 공식·산업·학술 출처를 병렬 조사 중이다.
- execution-knowledge paths: 위 5개 선행 보고서의 계약을 적용하며 신규 material failure는 없다.

### 2026-08-07 / Stage 2 20개 시장·용어·세계 작동 조사와 evidence 반영

- product delta: 8개 독립 읽기 전용 연구 묶음으로 20개 주제를 모두 조사하고 `research_evidence.jsonl`에 `cjk_narrative_world` 60행을 append했다. 주제별 정확히 3개 고유 URL과 1개 research matrix를 두고, runtime route·공통 world-evidence entry·원자 장면 prop ID에 연결했다. 구현 전 holdout에서 특정 작품에 가까운 `주신 공간/主神空间`, 성좌물의 `화신·코인·시나리오` 결합, 부자연스러운 선협 허가증, `高武=灵气复苏=万族入侵`, 이세계의 길드 편중, 규칙괴담의 의료 오염·문서 아카이브 편중을 제거했다.
- direct evidence: 신규 evidence는 60행·20 topic·60 unique source URL이며 각 topic이 정확히 3행, 공식/1차 출처 최소 1개, matrix 정확히 1개, world mechanism 5개 이상, runtime photographic evidence ID 6개 이상, boundary 3개 이상을 충족한다. candidate/photographic ID는 새 extension의 실제 catalog ID allowlist로 검증했다. 100행 holdout은 ID·기대 target을 삭제하지 않은 채 자연스러운 원어와 false-synonym 경계를 강화했다.
- binding implementation decision: 복합 주제는 route 수를 임의로 늘리는 대신 한 route 안에서 원자 장면을 분리한다. 신령·저승은 KR/CN/JP provenance별 세 장면을 구조적으로 잠그고, VRMMO·카드·확률은 네 장면, 괴수·메카는 네 장면, 마법소녀·아이돌·버추얼은 세 장면으로 분리한다. 각 candidate pack은 선택된 한 장면의 tag만 상속한다.
- remaining product gap: loader/domain 코드와 품질 라우팅은 추가되었으나 dictionary validator, 20 route candidate pack, 100 real retrieval, semantic index, leakage·전체 회귀 자격 판정이 아직 남아 있다.
- blocker: 없음. 출처 원문·이미지·비공개 자료는 외부로 전송하지 않았으며 semantic index 단계에서도 공개·추상 taxonomy text와 holdout query만 승인 범위 안에서 전송한다.
- execution-knowledge paths: 기존 5개 선행 보고서 계약을 그대로 적용했으며 신규 material failure는 없다.

### 2026-08-07 / Stage 3 별도 CJK taxonomy·typed domain·원자 route 구현

- product delta: `photo_prompt_cjk_worldbuilding_extension.json`을 별도 additive pack으로 추가하고 loader에 연결했다. `cjk_narrative_world` typed domain, 6개 shared family, 20개 scoped route, 46개 원자 장면, 356개 slot entry를 구현했으며 `photo_prompt_quality_layers.json`에 좁은 도메인 프로필과 20개 on-demand alias route를 추가했다. scene별 subject/action/location/prop/situation/occasion은 같은 scene tag와 cultural provenance를 공유하며 공통 narrative/capture/procedure/surface evidence와 결합한다.
- direct evidence: dictionary metadata validator pass; 신규 focused unit test pass. 20개 preset 모두 domain override가 `cjk_narrative_world` 하나이고, seed 1..3에서 각 route가 최소 2개 서로 다른 subject scene에 도달했다. 선택된 여섯 원자 slot은 하나의 scene prefix와 provenance로 잠겼고 candidate pack은 world-evidence slot과 market facet을 유지하면서 총 candidate cap 이하를 만족했다.
- binding implementation decision: 일반 `worldbuilding_system`과 CJK 시장 route를 별도 typed domain으로 유지한다. `cjk_spirit_underworld_bureaucracy`는 3 provenance scene, `cjk_vrmmo_card_liveops_world`와 메카·괴수 route는 각 4 scene, 미디어 route는 3 scene을 사용한다. 특정 작품에 가까운 고유어는 runtime extension에서 완전히 제거하고 단순 부정문에도 보존하지 않는다.
- remaining product gap: semantic index에 신규 376 catalog item이 아직 없고, 100개 실제 retrieval, 인접 route 및 generic leakage, 전체 회귀·독립 감사가 남아 있다.
- blocker: 없음. Stage 4는 승인된 공개·추상 taxonomy text와 holdout query만 Gemini에 전송하며 검증된 `--batch-size 1`을 사용한다.
- execution-knowledge paths: `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`의 batch cardinality 교훈과 `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`의 exact scoped-route 우선권을 적용했다.

### 2026-08-07 / Stage 4 다국어 semantic index와 100개 실제 retrieval

- product delta: 승인된 공개·추상 taxonomy 문자열만 Gemini `gemini-embedding-2`에 batch size 1로 전송해 semantic index를 6,003개에서 6,379개 항목으로 재생성했다. 20개 route의 한국어·영어·중국어·일본어 100개 사전 동결 query를 preset 고정 없이 실제 semantic 후보팩 경로로 연결했다.
- direct evidence: index manifest/hash/shard/order 검사가 `dictionary_hash=bc71093b39831eec5a370b5cbf9f046c1d53569391b4fa888aade55f1f33e437`, 6,379 entry, 768 dimensions, 16 shard로 통과했다. CJK retrieval은 100/100 pass, 실패 0이며 모든 case가 기대한 단일 preset, `cjk_narrative_world` 품질 profile, CJK intent domain을 유지했다. 기대값 삭제·완화, 실패 후 재시도, 사후 taxonomy 변경은 없었다.
- remaining product gap: generic 및 인접 CJK 누출, 보호 표현·문화 provenance, 기존 subculture/worldbuilding/v4 retrieval, contradiction/applicability와 전체 unit 회귀, 독립 감사가 남아 있다.
- blocker: 없음. 외부 전송은 승인된 taxonomy text와 100개 query로 제한했고 출처 원문·이미지·개인정보·실행 로그는 전송하지 않았다.
- execution-knowledge paths: 기존 batch-response 및 scoped-route semantic competition 실패 보고서의 계약이 현재 구현에서 유효했으며 신규 material failure는 발생하지 않았다.

### 2026-08-07 / Stage 5 과적합·문화 경계·누출 검증

- product delta: CJK specialty route를 명시 요청에만 활성화하는 typed-domain 경계를 유지하고, 공식·1차 출처·승인 상태·재사용 경계·용어 층위 ledger 검증을 focused contract에 고정했다. 신규 CJK index로 기존 active, subculture, general-worldbuilding retrieval을 다시 실행해 인접 의미 공간의 선택 안정성을 확인했다.
- direct evidence: CJK route별 seed 1..3 후보팩에서 최소 두 원자 장면과 동일 scene-prefix·단일 cultural provenance·candidate cap을 확인했다. generic portrait/fantasy/cosplay/occupation/실제 신앙·무술·재난·일반 streamer/idol 등 10개 negative control의 신규 CJK route 누출은 0이고 runtime 보호 표현 scan도 0이다. 실제 semantic retrieval은 CJK 100/100, 기존 v4 22/22, subculture 70/70, general worldbuilding 72/72로 모두 실패 0이다. 20개 topic은 주제별 공식·1차 출처 최소 1개와 승인·review·reuse 계약을 유지한다.
- remaining product gap: 전체 unit suite, dictionary·index 재확인, contradiction/applicability 및 public/frozen/domain rule holdout의 닫힌 실행, 독립 감사가 남아 있다.
- blocker: 없음. 기존 retrieval 기대를 수정하거나 신규 CJK 기대를 완화하지 않았고 동일 근본 원인의 수리 예산도 사용하지 않았다.
- execution-knowledge paths: 기존 general-worldbuilding 및 subculture 통과 보고서의 격리 계약이 재생성된 index에서도 유지됐으며 신규 material failure는 발생하지 않았다.

### 2026-08-07 / Stage 6 닫힌 최종 자격 판정

- product delta: 20개 CJK route, 60개 evidence row, 100개 frozen retrieval, 재생성 index와 기존 회귀를 하나의 닫힌 criterion matrix로 자격 판정하고 독립 서브에이전트가 기존 8개 완료 기준만 정적 감사했다.
- direct evidence: dictionary validator와 index integrity가 통과했다. contradiction은 643 preset × 3 seed, 총 1,929 generation에서 violation 0이다. public/frozen/domain rule holdout은 79/79, 24/24, 6/6이며 실제 semantic retrieval은 CJK 100/100, v4 22/22, subculture 70/70, worldbuilding 72/72이다. 전체 `python3 -m unittest discover -s tests`는 394 tests, 1,532.888초, OK이고 `git diff --check`도 통과했다. 독립 감사 verdict는 PASS, 미해결 critical/high 0, 일반 결함 0이다.
- criterion matrix: (1) 20 topic research/evidence PASS, (2) term-level·market-origin distinction PASS, (3) 20 executable on-demand route PASS, (4) route별 두 atomic scene·provenance lock PASS, (5) shared taxonomy·IP/living-practice boundary PASS, (6) frozen multilingual retrieval 100/100 PASS, (7) measured generic/adjacent leakage 0 PASS, (8) dictionary/index/candidate/contradiction/applicability/retrieval/unit 회귀 PASS.
- verification limits: 실제 렌더 이미지 품질은 목표 범위 밖이라 주장하지 않는다. 독립 감사는 이미 확보한 장시간 gate를 재실행하지 않고 결과와 코드 경로를 대조했으며, 출처 URL의 현재 가용성·전체 IP 우주·holdout 동결 시점 자체는 현재 working tree만으로 독립 재증명하지 않았다. 미해결 완료 차단 결함은 없다.
- blocker: 없음. 목표의 8개 완료 기준이 모두 충족되어 상태를 `completed`로 닫는다.
- execution-knowledge paths: 기존 5개 선행 보고서의 계약으로 충분했으며 새 material failure나 재사용 가치가 높은 비자명한 성공 절차가 없어 추가 passed/failed report는 만들지 않았다.
