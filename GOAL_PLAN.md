# Research-Backed Subculture Illustration and Artwork Grammar Goal

- 작성: 2026-08-09 01:06 KST
- 상태: completed
- 대상: 새 `skills/subculture-illustration-image-generator`와 `skills/photo-prompt-image-generator`의 매체 라우팅 경계
- 기준 ref: `main@f86abef`
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: Reader-Centered Viewer Experience, Attachment, and Commercial Intent
- 자동 목표 상향: 비활성

## 1. 목표와 실제 산출물

### 원래 사용자 요청

제안된 서브컬처 일러스트·아트워크 24개 주제를 모두 연구하고, 평범한 소재·정적인 캐릭터 나열·표면적인 스타일 형용사에 머물지 않도록 실제 프롬프트 생성과 이미지 결과에 반영한다. 독자가 처음 보는 것, 뒤늦게 발견하는 것, 서사와 감정의 원인, 매체별 상업적 약속, 반복 가능한 작가적 선택이 최종 픽셀에서 판독되어야 한다.

### 최종 제품/동작

1. 새 `subculture-illustration-image-generator` 스킬이 자연어 요청을 한 장 일러스트, 표지, 키 아트, 카드/스플래시, 세로 스크롤, 굿즈/SD, 연작 설정화 중 맞는 출력 형식으로 라우팅한다.
2. 24개 주제의 연구 결과가 출처 추적 가능한 typed illustration grammar로 들어가며, 정확히 하나의 primary visual mechanism과 호환되는 소수 support atom만 최종 prompt에 결합된다.
3. 고창의성 요청은 소재 희귀성이나 작가 이름 대신 familiar anchor, 한 가지 changed rule, first-to-second-look reveal, 시선 계층, 의도적 생략, 반복 모티프, 선·에지·완성도 규칙을 조합해 작가적 선택을 만든다.
4. 표지·키 아트·썸네일·카드·웹툰·굿즈의 형식 차이는 동일한 그림 프롬프트 뒤에 비율만 붙이는 방식이 아니라 format-specific crop, hierarchy, text-safe area, sequential/reveal 또는 scale-preservation 계약으로 표현된다.
5. 기존 사진 스킬의 기본 결과와 semantic index는 변하지 않는다. 일러스트 요청은 사진 카메라·렌즈·photoreal 품질층에 억지로 통과시키지 않고 새 스킬로 명시적으로 안내한다.
6. 24개 동결 요청의 감사된 prompt와 6개 대표 형식의 실제 이미지가 존재하며, 실제 픽셀에서 주제·행동·시선·작가적 규칙·형식 적합성이 prompt metadata 없이 판독된다.

### 연구 범위: 24개 주제

1. 한 장의 서사 압축과 결정적 순간
2. 시선 동선과 초점 계층
3. 실루엣과 형태 언어
4. 명암 덩어리와 컬러 드라마투르기
5. 선·에지·붓질·완성도 계층
6. 여백과 정보 밀도의 리듬
7. 반복 모티프와 시각적 은유
8. 제스처·힘의 흐름·환경 반응
9. 다인물 관계의 화면 배치
10. 의상·소품·환경 상태 연속성
11. 변신과 특수효과의 인과 문법
12. 비인간·크리처의 기능적 디자인
13. 세력·마법·기술의 시각 시스템
14. 배경을 통한 생활사와 세계관 증거
15. 연작·설정화의 캐릭터 동일성
16. 라이트노벨·만화 표지의 작품 약속
17. 애니메이션·게임 키 아트의 시각적 선언
18. 썸네일·배너·표지의 크롭 내성
19. 카드·가챠·스플래시 일러스트 문법
20. 웹툰 세로 스크롤의 시간과 감정
21. 굿즈·스티커·SD 변환 시 정체성 보존
22. 캠페인 전체의 아트 디렉션
23. 한중일 시각 관습의 독해 차이
24. 팬아트·오마주·리믹스와 독창성/IP 경계

### 범위

- 각 주제별 학술 연구, 공식 플랫폼/산업 문서, 저작자·실무 1차 자료의 출처·한계·추론 수준 기록.
- 새 sibling skill의 SKILL, progressive references, 연구 evidence shards, typed grammar/format profile, prompt generator와 fail-closed audit.
- 기존 creative-direction/viewer-experience의 일반 원리를 일러스트에 맞게 재사용하되 사진 표현 토큰과 런타임은 공유하지 않는다.
- 24개 구현 전 동결 자연어 요청, prompt/audit holdout, 서로 다른 여섯 형식의 실제 이미지 qualification.
- 사진→일러스트의 명시적 경계와 기존 photo generator 회귀 방지.

### 비목표

- 특정 생존 작가, 스튜디오, 프랜차이즈의 스타일·캐릭터·고유 실루엣을 복제하지 않는다.
- 모든 미술사조, 모든 CJK 독자, 실제 감정·매출·바이럴 성과를 보편적으로 설명하거나 예측하지 않는다.
- 24개 주제를 각각 고정 preset이나 장식 키워드 묶음으로 만들지 않는다.
- 외부 semantic embedding 전송·index 재생성, 배포, commit, push, PR을 필수 범위에 넣지 않는다.
- 사람 패널, 유료 광고 실험, 장기 트래픽을 로컬 제품 자격의 필수 gate로 추가하지 않는다.

## 2. 진척 계약

- 진척으로 인정: 연구가 실행 가능한 visual atom·compatibility/guard·format contract로 연결된 제품 변경, 감사 PASS 최종 prompt, 실제 이미지, 또는 실패 픽셀을 원인별로 수리한 제품 delta.
- 진척으로 인정하지 않음: 출처 목록·보고서·schema·fixture·테스트·감사기만 증가, 유명 스타일명·감정 형용사·디테일 수 증가, prompt audit PASS만으로 작가성이나 렌더 가독성 주장.
- Stage 1 이후 각 checkpoint는 연구 evidence뿐 아니라 그 evidence가 소비되는 grammar/format/prompt 또는 실제 render를 함께 전진시킨다.
- 검증-only 작업 상한: focused 검증은 각 제품 경계에서 한 번, 전체 회귀와 독립 검토는 마지막 stage에서 한 번만 수행한다. 검증-only checkpoint를 연속으로 두지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.

## 3. 기준선, 가정과 동결 조건

### 현재 기준선

- `photo-prompt-image-generator`는 사진 prompt 전용이며 `concept-routing.md`에서 poster, UI, typography, webtoon, sticker 등 non-photographic 출력을 강제로 통과시키지 말라고 명시한다.
- 기존 creative direction은 familiar anchor, one changed rule, reveal path, vantage/timing/omission/material rule을 제공하고, viewer experience는 첫 시선·감정 인과·애착·상업 목적을 제공한다.
- 기존 character-moe 연구는 24개 캐릭터 주제를 sparse visual grammar로 실행하지만 illustration-specific line, value mass, edge, crop, format, sequential grammar는 제공하지 않는다.
- 현재 작업 트리는 깨끗하고 `main@f86abef`는 `origin/main`보다 8커밋 앞서 있다. 선행 미푸시 커밋과 생성 이미지는 변경하지 않는다.

### 고정 아키텍처 가정

- 사진 스킬 내부에 illustration camera mode를 덧붙이지 않고 새 sibling skill을 만든다. 사진 스킬에는 설명·라우팅 경계만 최소 수정한다.
- 연구 knowledge와 실행 grammar를 분리한다. source-supported, cross-source synthesis, design inference, router, guard를 같은 의미로 취급하지 않는다.
- 특정 작가명 대신 `controlled_omission`, `edge_hierarchy`, `mark_rhythm`, `motif_transformation`, `shape_contrast`, `value_grouping`, `focal_route` 같은 관찰 가능한 선택을 사용한다.
- 색·형태·CJK 관습을 감정·성격·국적의 보편 법칙으로 쓰지 않는다. audience literacy와 context를 별도 조건으로 둔다.
- 구현 전 24개 자연어 prompt holdout과 여섯 render case의 필수·금지 pixel focus를 동결한다. 구현 후 기준 완화는 금지한다.

### 동결할 여섯 실제 렌더 형식

1. 단일 캐릭터 내러티브 일러스트: 서사 압축, 시선 동선, 선/에지, 반복 모티프.
2. 다인물 서브컬처 키 아트: 실루엣 분리, 관계 topology, 세력 디자인, 작가적 시각 선언.
3. 라이트노벨/만화 표지: 작품 약속, title-safe hierarchy, 축소 판독과 세로 crop.
4. 카드/가챠 스플래시: frame-safe silhouette, 변신/FX 인과, 희소성을 UI 색이 아닌 장면 결과로 표현.
5. 세로 스크롤 웹툰 구간: scroll reveal, 시간 지연, close-up과 여백 리듬, 동일 인물 연속성.
6. 크리처 굿즈/SD 변환 보드: 기능적 원형과 축약형 사이 정체성 보존, 보호 IP 비복제.

### 적용한 과거 실행 지식

- `docs/passed-reports/2026-08-08-reader-centered-viewer-experience.md`: 하나의 viewer need와 보이는 actor/action/target/consequence를 유지하고 실제 감정·구매 효과로 과장하지 않는다.
- `docs/passed-reports/2026-08-08-viewer-perceived-creative-direction.md`: familiar anchor, one changed rule, reveal, vantage/timing/omission/material rule을 유지하며 작가명이나 표면 craft를 authorial voice로 대체하지 않는다.
- `docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`: 연구 provenance와 runtime visual atom을 분리하고 one primary plus sparse supports, 구현 전 holdout, metadata-free pixel qualification을 재사용한다.
- `docs/failed-reports/2026-08-08-creative-direction-pixel-premise-legibility.md`: literal prompt binding은 픽셀 relation을 보증하지 않는다. 한 번의 원인별 수리 뒤에도 강한 model prior가 이기면 anomaly를 쌓지 않고 이미 연구된 다른 시각 realization을 선택한다.
- `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`: 물체 존재가 directed/simultaneous action의 증거가 아니다. actor, direction, target, consequence를 동결하고 원본 픽셀에서 검증한다.

## 4. 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 목표·요청·픽셀 기준 동결 | 이 계획, 24개 자연어 holdout, 6개 render focus, 기존 photo baseline hash/대표 pack을 구현 전에 저장 | JSON parse, topic/format coverage, 현재 photo pack과 boundary 직접 확인 | 구현 전 성공 기준과 회귀 기준이 고정되고 사용자 작업이 보존됨 |
| 2. 24주제 병렬 연구와 evidence 모델 | 주제당 matrix 1 + 독립 source 2의 research shards; mechanisms, observable illustration evidence, compatibility/conflict, counterexamples, format/audience/IP boundaries, source-specific provenance | 24×3 행·주제별 URL 3개·참조 무결성·source/synthesis/inference 구분; 독립 연구 감사 1회 | 24주제 모두 출처·한계와 실행 가능한 추상 메커니즘을 가지며 Critical/High 0 |
| 3. Typed illustration grammar와 스킬 런타임 | 새 skill, 24 routes와 공유 visual families, typed visual/router/guard nodes, sparse compatibility, format profiles, deterministic candidate pack 생성 | 24 direct routes, visual-only runtime selection, no artist/IP names, photo baseline byte equality | 자연어 요청이 한 primary mechanism과 소수 support, authorial/format contract를 가진 candidate pack을 생성함 |
| 4. Agent composition과 fail-closed audit | final English illustration prompt composition contract, viewer/authorial evidence binding, format별 crop/sequential/scale 규칙과 audit 구현 | 24 정상 prompt PASS; missing focal route, style-name proof, decorative motif soup, universal color/shape inference, format mismatch, nonliteral evidence mutation FAIL | 24주제의 연구가 실제 prompt에 보이는 결정으로 반영되고 문서 선언만으로 통과할 수 없음 |
| 5. 여섯 실제 이미지 자격 | 동결된 6형식의 pristine candidate pack, 감사 prompt, 최초 이미지와 metadata-free native/thumbnail/crop review | 사례별 최초 1장; 필수 pixel failure 시 제품 원인 수리 후 편집 또는 pristine rerender 중 하나만 최대 1회 | 6/6 최종 이미지가 주제·first/second look·authorial rule·format focus를 통과하고 실패 시도도 보존됨 |
| 6. 닫힌 회귀·독립 감사·lifecycle | 24 research/prompt 결과, 6 render 결과, photo 경계, 전체 tests와 실행 지식 lifecycle을 닫음 | focused/full tests 각 최종 1회, dictionary/audit, image hash, `git diff --check`, 독립 read-only audit 1회 | 최종 8기준 모두 통과하고 미해결 material failure가 없으며 실제 skill/runtime/prompt/image가 존재함 |

## 5. 최종 완료 기준

1. 24개 주제 각각에 matrix 1개와 독립 source record 2개가 있고, topic 안에서 URL 3개가 서로 다르며 모든 mechanism은 source-supported, cross-source synthesis, design inference 중 하나와 유효 evidence reference를 가진다.
2. 새 illustration skill과 실행 가능한 typed grammar가 존재하며 모든 24 route가 최소 하나의 visual atom을 제공하고 nonvisual market term, policy, 실제 작가명, 보호 IP를 prompt candidate로 선택하지 않는다.
3. 자연어 24개 holdout은 정확한 route/format을 선택하고 한 primary mechanism과 제한된 compatible supports를 구성하며, generic photo 요청·기존 photo candidate pack·semantic index는 변하지 않는다.
4. composed audit는 focal route, first/second-look evidence, actor/action/target/consequence, authorial choice와 format contract의 literal binding을 요구하고 style-name proof, 장식 나열, 색/형태/문화의 보편 추론, format mismatch를 거부한다.
5. 표지, 키 아트, 썸네일/crop, 카드/스플래시, 세로 스크롤, 굿즈/SD의 매체 규칙이 typed profiles로 구분되며 단순 aspect-ratio suffix로 대체되지 않는다.
6. 24개 동결 요청 모두 감사 PASS prompt를 만들고, 6개 실제 최종 이미지가 native와 지정 thumbnail/crop에서 metadata-free 필수 focus 100%를 통과한다. 실패 시도와 bounded repair 이력은 숨기지 않는다.
7. 기존 photo creative/viewer/character/scene/safety/negative-byte 계약과 대표 frozen pack이 회귀하지 않고, 새 경로가 camera/lens/photoreal 토큰을 illustration에 강제하지 않는다.
8. source evidence, skill/runtime/audit 변경, 24 prompt 결과, 6 PNG와 versioned review, focused/full 검증, `git diff --check`, 독립 최종 감사가 존재한다. 계획·테스트·문서·index만으로 완료할 수 없다.

## 6. 검증 수준과 예산

- 위험 수준: 중간. 로컬 신규 skill과 routing boundary를 추가하며 외부 배포는 없지만, 연구 과장·작가/IP 모방·사진 경로 오염·프롬프트 PASS와 픽셀 실패 간 괴리 위험이 있다.
- 연구 예산: 주제당 정확히 3 source record를 기본으로 한다. 필수 메커니즘의 근거가 상충하거나 출처 접근이 불가능할 때만 주제당 1개를 추가하고 이유를 기록한다.
- 반복 중: shard/schema 검증과 변경된 generator/audit의 focused tests만 실행한다.
- 이미지 예산: 6사례 최초 1장씩. 필수 픽셀 실패 시 원인별 구현/프롬프트 수리 후 사례당 targeted edit 또는 pristine rerender 중 하나만 최대 1회; batch selection 금지.
- 최종: 전체 unit suite 1회, research/grammar/prompt validators 1회, photo regression 1회, image hash/review 1회, 독립 read-only audit 1회.
- 새 semantic index, 외부 embedding, 사람 패널, 유료 서비스나 추가 verifier family가 필수로 보이면 먼저 질문한다.

## 7. 중단 조건

- 동일한 근본 원인의 research/runtime/pixel 수리가 두 번 실패할 때에는 기준을 완화하거나 더 많은 이미지를 선별하지 않고 material failure를 보고한다.
- 통과를 위해 기존 safety, explicit-adult, cultural provenance, IP/person/style boundary 또는 photo default를 약화해야 할 때.
- 24주제의 근거가 특정 작품·작가 사례에만 의존해 추상화할 수 없거나, CJK 관습을 보편 법칙으로 주장해야만 route를 만들 수 있을 때 해당 route를 guard/router로 제한하고 제품 gap을 보고한다.
- 외부 semantic text 전송, index 재생성, credential, 유료 API, 배포, commit, push, PR 또는 파괴적 변경이 필요할 때 별도 권한을 요청한다.
- 선행 8개 미푸시 커밋이나 기존 생성 artifact를 수정·삭제해야 할 때 중단한다.

## 8. 실행 지식 계약

- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/`의 filename/header metadata를 관련도·환경·상태·최신순으로 검색하고 전문은 기본 최대 5건만 읽는다. 현재 source와 direct evidence가 과거 보고서보다 우선한다.
- material failure가 가정이나 완료 기준을 깨거나 수리 방향을 바꾸면 재시도 전에 matching failed report를 생성 또는 갱신한다. 같은 원인은 한 보고서에 통합한다.
- 저장 전 현재 날짜·시간을 확인하고 credential, token, secret, 민감 endpoint, 고객·개인정보와 불필요한 원문을 제거한다. 필요하면 sanitized 결론과 접근 제한 evidence reference만 남긴다.
- 실패가 기존 passed report의 적용 범위를 깨면 failed/passed 양쪽 lifecycle을 같은 변경에서 연결한다. 해결 시 failed를 `resolved`, 새 성공 보고서에 `Resolves`; 대체 시 양쪽 `Superseded by`/`Supersedes`를 기록한다.
- 모든 최종 기준을 직접 통과한 뒤에만 목표당 기본 최대 한 개의 passed report를 작성한다. 자격은 material failed report 해결, 동일 고정 조건에서 기본/문서화 접근 실패 뒤의 비자명한 대체, 또는 현재 코드만으로 싸게 복구할 수 없는 다단계 재현 절차 중 하나여야 한다.
- 목표가 blocked/partial이면 passed report를 만들지 않고 matching failed report 또는 최종 진행 로그에 검증된 sub-result를 남긴다.
- 실행 보고는 별도 stage/checkpoint가 아니며 제품 진척을 대신하거나 다음 product delta를 지연시키지 않는다.

## 9. 진행 로그 형식

각 checkpoint는 다음 순서로 이 파일에 추가한다.

`product delta -> direct evidence -> remaining product gap -> blocker -> execution-knowledge paths`

## 10. Codex 실행 프롬프트

```text
/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Preserve its scope, progress contract, validation budget, completion criteria, and full execution-knowledge contract. Use metadata-first report search with at most five full reads by default; current evidence wins. Sanitize stored evidence, update stale or resolved reports bidirectionally, record material failures before retry, and create at most one qualified reusable success by default only after all final criteria pass. Reporting is not product progress or a separate checkpoint. After setup, advance through product or measured-result checkpoints, use focused verification during iteration, and run one risk-proportional final verification. Do not add verification programs or external gates unless the plan requires them or a real product defect makes them necessary. Ask before any material scope or validation expansion.
```

## 11. 진행 로그

### 2026-08-09 01:06 KST / 목표 생성·기준선·실행 지식 적용

- product delta: 사진 기본 경로를 보존하면서 24개 서브컬처 illustration 연구를 새 typed grammar와 실제 prompt/image로 연결하는 후속 목표를 고정했다.
- direct evidence: 깨끗한 `main@f86abef`, `origin/main` 대비 8커밋 ahead, 기존 non-photographic boundary와 creative/viewer/character 계약을 확인했다. 관련 report metadata 전체를 스캔하고 exact-match passed 3건·resolved failed 2건만 전문 검토해 sparse grammar, 구현 전 holdout, metadata-free pixel gate와 수리 상한에 적용했다.
- remaining product gap: 24개 요청·6개 픽셀 기준 동결, 병렬 연구, 새 skill/runtime/audit, 24 prompt와 6 render, 닫힌 회귀가 남아 있다.
- blocker: 없음. 새 sibling skill은 사진 스킬의 명시적 경계를 지키기 위한 보수적 아키텍처 결정이다.
- execution-knowledge paths: 3절에 기록한 passed 3건과 failed 2건.

### 2026-08-09 01:09 KST / Stage 1 구현 전 holdout 동결

- product delta: 24개 주제별 한국어 자연어 요청·route·format·필수/금지 focus와 6개 실제 렌더 사례를 구현 전에 동결했다. 여섯 render가 24 topic을 중복 없이 정확히 한 번씩 묶어 single illustration, ensemble key art, cover/crop, card/FX, vertical scroll, creature/campaign adaptation을 검증한다.
- direct evidence: `illustration_prompt_holdout_v1.jsonl`은 24행·24 topic·24 seed, `render_illustration_quality_holdout_v1.jsonl`은 6행·6 format이며 포함 topic 24개가 모두 고유하다. 기존 photo `street_documentary` rule pack의 exact SHA-256 `8b3bc3c4...c216c`, pack `5e64d0990c415a3b`, selected IDs와 negative를 별도 baseline으로 고정했다.
- remaining product gap: 24 topic source research, typed grammar/runtime/audit, 24 composed prompt와 6 actual render가 남았다.
- blocker: 없음.
- execution-knowledge paths: 기존 5건 재사용, 새 material failure 없음.

### 2026-08-09 01:36 KST / Stage 2 24주제 연구·정규화 완료

- product delta: 24개 주제 각각에 topic matrix 1개와 독립 source 2개를 두고, 192개 메커니즘·264개 고유 candidate를 출처 추적 가능한 여섯 research shard로 편입했다. 모든 matrix가 observable illustration evidence, format/viewer implication, compatibility/conflict/counterexample/boundary를 제공한다.
- direct evidence: aggregate validator가 72 rows, 24 topics, topic별 서로 다른 URL 3개, 264/264 unique candidate IDs, closed provenance enum을 zero error로 확인했다. 최종 provenance는 source-supported 63, cross-source synthesis 72, design inference 57이며 cross-source 72개는 모두 해당 topic의 독립 source 2개를 참조한다. 저장소 shard hash는 검토된 `/tmp` packet과 일치한다.
- remaining product gap: 이 연구를 소비하는 typed graph·format profile·deterministic runtime, 24 composed prompt, 6 render qualification이 남아 있다.
- blocker: 없음. 전체 URL은 71개지만 같은 공식 GDC 자료가 서로 다른 두 주제에서 재사용된 경우이며, 각 topic 내부 URL 3개 고유성 계약은 모두 통과한다.
- execution-knowledge paths: `docs/failed-reports/2026-08-09-illustration-research-schema-drift.md`, `docs/failed-reports/2026-08-09-illustration-research-provenance-overclaim.md`를 원인 보존 상태로 resolved 처리했다.

### 2026-08-09 02:11 KST / Stage 3 typed grammar·분리 런타임 완료

- product delta: 새 sibling skill에 24 route, 6 format family/10 surface variant, 264 typed runtime node(visual 209/router 28/guard 27), 수동 의미 검토한 sparse bundle 48개와 stdlib-only deterministic candidate-pack runtime을 구현했다. 사진 skill에는 sibling 라우팅 문구만 추가했다.
- direct evidence: 통합 validator가 research 72/24/192/264, runtime 24/6/10/264/48, normalized alias collision 0, graph candidate ID/definition/role와 research exact match, frozen request route·format 24/24, 동일 입력 canonical bytes를 확인했다. focused tests 14개가 24 route, sparse/typed/integrity mutation, photo frozen SHA/pack/selected IDs/negative, photo import·asset boundary를 통과했다.
- remaining product gap: 24개 agent-composed prompt 감사, 6개 실제 이미지와 metadata-free format review, 최종 전체 회귀·독립 감사가 남아 있다.
- blocker: 없음. 첫 real pack inspection에서 post-render lifecycle evidence가 pre-render format field로 섞인 결함을 발견했으나, phase-specific field로 분리하고 사후 pixel PASS 주장 우회도 차단했다.
- execution-knowledge paths: `docs/failed-reports/2026-08-09-illustration-audit-pixel-evidence-conflation.md`를 해결 상태로 기록했다.

### 2026-08-09 02:21 KST / Stage 4 24개 composed prompt 자격 완료

- product delta: 24개 동결 자연어 요청 모두에 대해 실제 deterministic candidate pack을 생성하고, 서로 다른 여섯 agent 작업자가 최종 영문 illustration prompt·creative development·literal evidence를 작성했다. 결과는 4-case 단위 여섯 shard로 저장해 단일 대형 fixture를 피했다.
- direct evidence: root가 24 pack을 현행 runtime으로 재생성해 canonical object exact match를 확인하고, 현행 audit 결과가 저장된 audit와 exact match함을 검증했다. 24/24 status·quality PASS, integrity/failures/warnings 0, pack/prompt/selected signature 모두 unique이며 3 rejected ordinary answers·4 distinct operators·1 selected proposal 계약을 전부 충족했다.
- remaining product gap: 여섯 format 대표 이미지를 실제 생성하고 native/thumbnail/crop/sequence 픽셀에서 first/second look, authorial rule, action causality와 형식 적합성을 확인해야 한다. 전체 photo/full regression과 독립 최종 감사도 남아 있다.
- blocker: 없음. 프롬프트 길이는 257–450 words(평균 364.9)이며 profile에 고정 길이 gate는 없다. 이는 상세 계약 자격 결과이고 실제 렌더의 정보 과부하는 다음 pixel gate에서 직접 판정한다.
- execution-knowledge paths: Stage 3의 phase-boundary failed report를 현행 audit 우회 검사까지 닫았으며 새 material prompt failure는 없다.

### 2026-08-09 02:51 KST / Stage 5 여섯 형식 실제 렌더·bounded repair 종료

- product delta: 여섯 독립 작업자가 frozen request마다 pristine pack·감사 prompt를 만들고 built-in image generation을 최초 1회씩 실행했다. cover의 글리프는 원인 구절을 무각인 fracture staple로 바꾸고 단일 targeted edit로 해결했다. second-look cue는 앞으로 전용 비가림 carrier를 요구하고, 실패한 compound micro-shape를 같은 형태로 강조하지 않고 이미 개발한 더 단순한 consequence로 바꾸도록 skill/runtime guidance를 보강했다. 로컬 결과를 versioned review에 연결하고 candidate pack·현행 audit·result/PNG hash·dimensions를 선택적으로 검증하는 validator 경로도 추가했다.
- direct evidence: ensemble key art, cover/crop, card/FX, vertical-scroll sequence, creature adaptation board 5건은 native와 요구 thumbnail/crop/sequence view를 통과했다. single narrative는 frozen primary focus 5개·320px 2개·금지 4개를 통과했지만, 최초와 유일한 edit 모두 subordinate clasped-hands shadow가 한 팔/손가락 군집으로 읽혀 `second_look_ev_early_anomaly`가 실패했다. `render_illustration_quality_visual_review_v1.json`은 5 pass/1 fail, 실패 final 없음, 모든 attempt hash를 보존하며 `--verify-local-images`가 이 상태를 재검증했다.
- remaining product gap: 완료 기준 6의 6/6 최종 PNG는 아직 5/6이다. 독립 최종 감사와 전체 suite는 실행하되 passed report와 goal complete는 금지한다. source guidance 수정 뒤 더 단순한 second-look carrier를 쓰는 새 pristine qualification 1장은 현재 동결 예산 밖이므로 사용자 승인 전 실행하지 않는다.
- blocker: `illustration_render_01_single_narrative`의 bounded repair 1회가 소진됐다. 기준을 낮추거나 batch에서 유리한 이미지를 고르지 않는다.
- execution-knowledge paths: `docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md` open; `docs/failed-reports/2026-08-09-illustration-audit-generic-subject-false-positive.md`는 generic subject 과검출을 회귀 테스트와 함께 resolved 처리했다.

### 2026-08-09 03:23 KST / Stage 6 전체 회귀·독립 감사 종료, 목표 partial 유지

- product delta: 계획상 한 번의 전체 suite에서 발견된 sibling audit 이름 충돌을 제품 경계에서 해결했다. illustration 감사 핵심은 byte-identical `illustration_audit.py`라는 고유 import 이름을 사용하고, 기존 `audit_composed_prompt.py`는 명령 호환 래퍼로 유지한다. validator와 계약 테스트도 고유 핵심만 가져오며 실제 바인딩 파일을 회귀 검사한다.
- direct evidence: 전체 suite는 421 tests/1611.021s를 실행해 기존 테스트를 통과했으나, photo 감사가 먼저 캐시된 순서에서 illustration 테스트만 6 failures·12 errors를 냈다. 수리 후 같은 원인 순서를 의도적으로 재현한 photo-first 19 tests가 모두 통과했다. 최종 validator는 research 72/24/192/264, runtime 24 routes·6 families·10 variants·48 bundles·264 nodes, prompt 24/24, local render hash/pack/audit 6/6를 검증하고 pixel qualification을 숨김없이 partial 5 pass/1 fail로 보고했다. skill quick validation, py_compile, CLI import, `git diff --check`도 통과했다. 독립 재감사 판정은 Critical 0, High 1 open(case 01), Medium 2 open(case 02 orientation deviation, 수리 후 전체 421-suite green 미증명)이다.
- remaining product gap: 완료 기준 6과 8은 여전히 실패다. case 01의 더 단순하고 비가림인 material-state second-look carrier를 사용한 새 pristine qualification이 실제 픽셀에서 통과해야 하며, 전체 suite 수리 후 검증은 예산을 지키기 위해 원인 재현 모듈로 닫고 421 tests를 재실행하지 않았다.
- blocker: case 01은 최초 1회와 허용된 repair 1회를 모두 소진했다. 새 이미지 1장 자격 실행은 동결 예산 밖이므로 사용자 승인이 필요하다. 목표는 `active/partial`, passed report와 goal complete는 금지한다.
- execution-knowledge paths: `docs/failed-reports/2026-08-09-illustration-audit-module-name-collision.md` resolved; `docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md` open; 독립 감사 `/tmp/subculture-illustration-independent-final-audit.md`와 블라인드 기록 `/tmp/subculture-illustration-blind-observations.md`.

### 2026-08-09 04:15 KST / Stage 6 후속 v2 second-look 계약·case 01 사전 자격

- product delta: 현행 candidate/composed 계약을 v2로 올려 second-look을 primary carrier와 서로 다른 안전 fallback carrier, 보호 locus, 정확한 consequence, 검토 scale에 결속했다. 24개 prompt qualification을 v2로 전량 재생성하면서 v1 pack·prompt·audit를 별도 legacy 경로로 byte 재현 가능하게 보존했다. 실패한 case 01에는 compound 손 그림자를 제거하고 넓은 brass seam material boundary를 primary, 비어 있는 receiving mat의 dry surface state를 fallback으로 쓰는 generation-free successor preflight를 추가했다.
- direct evidence: v1 24건과 v2 24건 모두 현행 validator에서 pack canonical 재생성·저장 audit exact equality·status/quality PASS·issue array 0을 통과했다. case 01 preflight pack `db15b9138a402405`, prompt SHA-256 `e0af5c7c9e239b1361b501631454d3e44c32253ced62ae2f2c436ccdece4351e`, plan SHA-256 `b1482fef3ddc0c22c1009cfde79a02329559656df5f5bfe8abcb29f099279325`가 exact 재생성되며 image action 3종 false, 별도 승인 필요 true, initial=`primary_carrier`, 유일한 조건부 repair=`fallback_carrier`로 검증된다. focused illustration/photo tests 28/28가 승인 선반영·primary 반복 수리·preflight PNG 유입도 fail-closed로 거부했고, `--verify-local-images`가 기존 v1 실패 이미지·result를 포함한 6개 artifact hash 불변성을 확인했다. 집계 validator는 구조 무결성 `status=pass`와 제품 픽셀 자격 `product_qualification_status=partial`을 분리해 더 이상 최상위 PASS만으로 완성을 오인하지 않는다.
- remaining product gap: preflight와 prompt audit은 픽셀 현저성을 증명하지 않는다. 실제 완료 기준 6은 여전히 5/6이며, 새 primary carrier가 native scale에서 판독되는지 한 장의 pristine render로 확인해야 한다. 실패할 경우에만 선언된 fallback으로 한 번 수리할 수 있다. 픽셀 통과 뒤에도 metadata-free native/320px 및 동결 focus·금지 수렴 검토, plan SHA/attempted role/result·PNG hash와 versioned review 반영, open failure lifecycle 해소, 현행 전체 suite green, 독립 최종 감사가 완료 기준 8에 남는다.
- blocker: 새 render는 기존 동결된 case 01 예산을 모두 소진한 뒤의 별도 successor qualification이므로 사용자 명시 승인이 필요하다. 또한 기존 421-test 전체 실행은 import 충돌 수리 전 실패했고 단일 full-run 예산을 소진했으므로, 픽셀 통과 뒤 현행 전체 suite를 한 번 더 실행하는 검증 확대도 사용자 승인이 필요하다. 승인 전에는 이미지 생성·편집이나 421-test 재실행을 하지 않고 목표를 `active/partial`로 유지한다.
- execution-knowledge paths: `skills/subculture-illustration-image-generator/assets/render_case01_v2_preflight/`; `docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md` open; `docs/failed-reports/2026-08-09-illustration-audit-module-name-collision.md` resolved but post-fix full-suite green remains unproven; v1 render review는 수정하지 않았다. 2026-08-09 04:22 KST 독립 read-only preflight 감사 판정은 Critical 0, High 1(pixel 5/6), Medium 2(post-fix full-suite·case02 orientation 한계)였다.

### 2026-08-09 11:13 KST / Stage 5·6 successor 실제 렌더 종료, 두 carrier 모두 실패

- product delta: 사용자 승인 뒤 고정 v2 prompt로 `primary_carrier` 최초 이미지를 정확히 한 장 생성하고, strict blind pixel 실패 뒤 선언된 `fallback_carrier`로 targeted edit를 정확히 한 번 사용했다. 두 native 이미지와 320px·진단 crop, 독립 blind observation, exact prompt/edit prompt, 승인 범위, pack/audit/plan/image hash를 전용 result에 보존했다. versioned successor review와 validator를 추가해 preflight 대기 상태와 실제 실패 결과를 분리하고, thin line과 substrate design-aligned surface state를 pixel PASS로 오인하지 않는 실무 규칙을 skill reference에 반영했다.
- direct evidence: primary PNG `5ff90d9ad61c6772d5147dc3f0f4a6f6553401291b116b76c80540cf758cc4e1`(1149×1369)은 frozen first-read·authorial·thumbnail·forbidden focus를 모두 통과했지만 broad pale seam 대신 thin red-white threshold trace로 수렴했다. fallback PNG `3d58ae585c7e6e9269b56e03f3767f11cd4deeef854a571c3c3092df8ced0b29`(1149×1368)은 넓은 밝은 mat center를 만들었으나 regular woven border와 일치하고 rain bead/moisture front가 끊기는 증거가 없어 rug coloration으로 읽혔다. 서로 독립된 metadata-free 검토가 각 역할을 FAIL로 판정했다. 현행 validator는 successor attempt 2·repair 1·qualified role null·final 없음·aggregate 5 pass/1 fail을 local hash와 함께 검증하며, 실패 carrier 승격 변이까지 포함한 focused illustration/photo tests는 30/30 PASS다.
- remaining product gap: 완료 기준 6의 second-look pixel focus와 6/6 final PNG가 충족되지 않았고, 따라서 기준 8의 미해결 material failure·현행 full-suite green·최종 PASS 감사도 충족되지 않았다. 나머지 24주제 연구, typed grammar, 24 prompt, photo 경계와 5개 render는 그대로 통과한다.
- blocker: primary와 서로 다른 fallback까지 모두 소진되어 현재 qualification의 이미지 예산과 수리 경로가 끝났다. 같은 목표에서 더 생성하거나 유리한 variant를 고르거나 기준을 완화할 수 없다. 사용자 승인한 421-test 재실행은 pixel PASS 이후 조건부였으므로 조건 불충족으로 실행하지 않았다. 후속 진척에는 현재와 materially different한 render strategy/model capability, 새 사전 carrier 계약과 새 예산을 별도 목표로 승인해야 한다.
- execution-knowledge paths: `generated_images/subculture-illustration-case01-v2-qualification-20260809_105207/01-single-narrative/result.json`; `skills/subculture-illustration-image-generator/assets/render_case01_v2_visual_review.json`; `docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md` open. 기존 v1 failure와 새 v2 두 attempt 모두 불변 보존하며 `final.png`는 없다.

### 2026-08-09 12:21 KST / Stage 5 v3 구조 전환 자격 PASS·Stage 6 전체 회귀 PASS

- product delta: 사용자 후속 승인으로 기존 line/substrate carrier를 반복하지 않고, 검은 문간에 고립된 황동 종의 물리적 관계를 primary로 사용하는 새 preflight를 동결했다. 수직 체인, 기울어진 종 몸체, 별도 변위된 clapper, cuff-to-clapper 붉은 실, 미접촉 handoff gap을 서로 독립된 증거로 결속하고, 무늬 없는 석판의 불규칙 건조 상태는 primary 실패 시에만 쓰는 fallback으로 남겼다. 새 pristine 이미지를 정확히 한 장 생성했으며 primary가 통과해 편집은 호출하지 않았다.
- direct evidence: pack `db15b9138a402405`, prompt SHA-256 `4efc3a3cc6874b9befcdddf8e5a6893cc8ec0b6c5d85b12867a92c0cbef578ea`, plan SHA-256 `b2e69c250153c8e4f3821f6826cc7e001861db5a38816d4914e8ac09e6ddbb76`를 동결했다. `initial.png`와 byte-identical `final.png`은 1024×1536, SHA-256 `95b9b3c311af85de3092c30b0e4272929e307decfc3e68434917b1d7eba1b796`이다. 독립 metadata-free review가 native와 213×320 모두에서 handoff first read, bell second look, thread states, edge/omission, 동결 focus 5개·thumbnail 2개·금지 수렴 4개를 통과시켰다. fallback은 `not_attempted`로 보존된다. 집계 validator는 과거 v1·v2 partial을 불변 보존하면서 현행 제품 자격을 6 pass/0 fail로 보고하고 local pack/audit/plan/result/PNG/native/blind hashes를 검증한다.
- regression: `python3 -m unittest discover -s tests`가 현행 소스에서 437 tests를 1483.337초에 실행해 failures 0, errors 0으로 통과했다. 실행 결과를 versioned review에 기록한 뒤 focused illustration/photo boundary 33/33과 `git diff --check`가 재통과했다. 이전 audit import collision의 full-process uncertainty와 second-look pixel-legibility 실패 보고서는 resolved로 갱신했다.
- remaining product gap: 제품·픽셀·전체 회귀 기준은 닫혔다. 계획상 마지막 독립 read-only 감사가 8개 완료 기준과 lifecycle 기록의 자기모순·과장 여부를 확인해야 하며, 그 전에는 목표 상태를 완료로 바꾸지 않는다.
- blocker: 없음.
- execution-knowledge paths: `skills/subculture-illustration-image-generator/assets/render_case01_v3_preflight/`; `skills/subculture-illustration-image-generator/assets/render_case01_v3_visual_review.json`; `generated_images/subculture-illustration-case01-v3-qualification-20260809_114514/01-single-narrative/result.json`; `/tmp/illustration-v3-final-validator.json`.

### 2026-08-09 12:34 KST / 독립 최종 감사·lifecycle 완료

- product delta: 새 제품 변경 없이 최종 자격의 독립성·불변성·실행 지식 lifecycle을 닫았다. 메타데이터를 보기 전에 native/320px 픽셀 관찰을 별도 고정한 뒤 v1·v2 failure와 v3 pass, 24 research/prompt, typed runtime, photo boundary, full/focused 검증을 역검증했다.
- direct evidence: 독립 감사 판정은 PASS, Critical 0, High 0, Medium blocker 0이다. v1 6개 artifact와 v2 result·두 PNG·모든 review view·blind 기록의 SHA가 기존 기록과 일치하며 두 세대 모두 final 없음이 확인됐다. v3는 pack exact 재생성, prompt/audit/plan hash, initial 1·repair 0, initial/final byte equality, native tool·blind record·thumbnail hash가 모두 일치한다. local validator product PASS/6-of-6, focused 33/33, full 437/437, photo protected asset baseline diff 0, `git diff --check` PASS를 대조했다.
- completion: 5절의 8개 완료 기준은 모두 PASS다. illustration failed report 6개를 모두 `resolved`로 유지하고 단일 성공 보고서 `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`에서 bidirectional lifecycle과 재사용 원칙을 연결했다. 목표 상태를 `completed`로 변경한다.
- retained limit: case 02 portrait master는 동결된 generic key-art 계약의 필수 orientation/export가 아니고 320/640 focus가 통과했으므로 비차단이다. 향후 landscape 납품을 요구하면 별도 qualification이 필요하다. 로컬 픽셀 PASS는 실제 감정·매출·법적 clearance·역사적 독창성을 증명하지 않는다.
- blocker: 없음.
- execution-knowledge paths: `/tmp/subculture-illustration-v3-final-blind-audit.md`; `/tmp/illustration-v3-final-validator.json`; `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`.
