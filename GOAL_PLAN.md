# Photo Prompt Intent-Preserving Optimization Goal

- 작성: 2026-08-11 12:42 KST
- 상태: completed
- 완료: 2026-08-11 14:33 KST
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@4e992a97278e73bb58f2c656f45836ef1ba1e4e6`
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 이전 완료 목표: `docs/passed-reports/2026-08-11-universal-scene-public-boundary-integration.md`
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: 개선이 누적된 photo-prompt-image-generator를 모든 기능을 유지하면서 무리하지 않는 범위에서 프롬프트와 로직 중심으로 리팩터링한다.
- 최종 제품/결과:
  1. 사용자 필수 시각 요구, 역할 positive anchor, soft guidance, negative constraint가 서로 다른 타입과 극성으로 처리된다.
  2. 후보 팩의 `mandatory_intents`에는 positive visible intent만 들어가며 내부 메타 문장과 금지어가 positive prompt 의무로 승격되지 않는다.
  3. rule mode에서 명시적인 피사체와 `no_people`가 sampler, 품질 facet, adult-appeal eligibility 전체에 일관되게 적용된다.
  4. compact 직접 프롬프트와 candidate pack이 내부 정책 중복을 줄이면서 사용자 요구, 역할 정체성, negative bytes, creative/viewer/hybrid 계약을 보존한다.
  5. 반복 intent/rule 계산을 제거하여 고정 조건 성능을 개선하되 성능-only 경로의 결정적 출력은 byte-identical하게 유지한다.
- 범위: wrapper와 generator의 요구사항 전달·계약·렌더링, intent routing, candidate-pack intent/quality 구성, composed audit, 필요한 quality-layer 정책, focused regression, 최소 문서 정합성.
- 비목표: semantic index 저장 형식·지연 로딩, 새 embedding 또는 index 재생성, candidate-pack 전면 v3 재설계, 대규모 파일 분할, API ledger adapter, 이미지 생성·픽셀 A/B, 배포, commit, push, PR.

## 진척 계약

- 진척으로 인정: 실제 generator/auditor/routing 동작 변화, 고정 입력에서 잘못된 intent·subject·facet가 교정된 결과, 보존 조건을 만족하는 측정된 성능 개선.
- 진척으로 인정하지 않음: 테스트·계획·보고서·schema·benchmark 도구만 증가한 상태, golden을 새 오동작에 맞춰 갱신, 검증기를 확장해 제품 결함을 우회, 파일 분할만 한 상태.
- Stage 1 이후 모든 checkpoint는 product delta 또는 고정 조건의 측정된 최종 후보를 포함한다.
- 검증-only 작업 상한: 반복 중에는 변경 경로 focused 검증만 수행하고 전체 unit discovery·semantic integrity·contradiction 검사는 최종 후보에서 각 한 번만 수행한다. 검증-only checkpoint를 연속으로 두지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.

## 기준선과 고정 비교 조건

### 현재 기준선

- 작업 트리는 clean이고 `main`과 `origin/main`은 `4e992a97278e73bb58f2c656f45836ef1ba1e4e6`으로 동일하다.
- `회사원`, rule, seed 42, hybrid candidate pack은 pretty 222,881 bytes, minified 151,732 bytes, mandatory 93개, uncovered 60개다. `Avoid`, `glamour`, `pin-up`, `fetish`, `minors-coding`, `Soft`, `visual`, `guidance`가 positive mandatory intent에 포함된다.
- 같은 `회사원` 직접 prompt는 compact 191 words, standard 236 words, detailed 349 words다. compact 120-word 예산 이후 내부 additional requirements가 붙는다.
- `고양이`, rule, seed 42는 `young_actor`를 선택하고 human adult-appeal 기본값을 활성화한다.
- `사람 없는 화장품 제품 사진`, rule, seed 42는 adult appeal은 차단하지만 `사진`이 `photographer_role_model`과 매칭되어 human quality facet을 추가한다.
- 고정 `회사원` candidate-pack 프로파일의 변경 전 wall time은 7.211초와 7.308초이며 기준 중앙값은 7.260초다. 탐색적 순수 alias cache는 출력 SHA를 유지한 채 약 2.97초였으나 제품 코드에는 반영되지 않았다.
- skill validator, dictionary validator, 112/112 scene-expression audit, 6,513-entry semantic-index integrity, 2,001 contradiction generation/0 violations는 통과했다.
- 전체 502 unit discovery는 photo 영역 밖 universal-scene에서 11 failures/1 error가 있어 baseline부터 green이 아니다. 최종 결과는 이 실패 집합을 늘리지 않고 photo 관련 실패 0을 요구한다.

### 고정 입력과 비교 규칙

- 핵심 교정 입력: `회사원`, `제빵사`, `고양이`, `사람 없는 화장품 제품 사진`; 모두 rule mode, seed 42, candidate pack과 direct compact 경로를 사용한다.
- hard user intent 보존 입력: 명시적 `--additional-requirement` 한 건을 넣고 문구가 mandatory/audit/render 경로에서 유지되는지 확인한다.
- 호환성 입력: 기존 ordinary preset, eligible human adult default, explicit 0/0 adult opt-out, hybrid augmentation, creative direction, viewer experience의 대표 기존 테스트를 재사용한다.
- 성능 비교: 같은 checkout·Python·command·seed에서 warm run 3회의 중앙값을 사용한다. 성능-only 변경은 canonical JSON SHA가 같아야 한다.
- intentional correctness delta는 새 회귀 계약으로 고정하고, 무관한 golden·RNG 순서·negative bytes는 변경하지 않는다.

### 적용한 과거 실행 지식

- `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`: 명시적 typed route는 generic semantic 경쟁보다 우선하며 negative control을 함께 유지한다.
- `docs/failed-reports/2026-08-07-subculture-surface-applicability-golden-drift.md`: 좁은 예외를 위해 global eligibility를 넓혀 RNG와 무관한 golden을 흔들지 않는다.
- `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`: exact user-authored route precedence와 domain quarantine을 재사용하고 generic 요청 동작은 보존한다.
- `docs/passed-reports/2026-08-08-viewer-perceived-creative-direction.md`: creative contract, one-rule authorial grammar, 120-word composed prompt와 negative-byte 경계를 보존한다.
- `docs/passed-reports/2026-08-08-reader-centered-viewer-experience.md`: viewer need와 actor/action/target/consequence audit를 유지하고 prompt audit를 실제 관객 반응 증거로 확대 해석하지 않는다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 기준선과 회귀 계약 동결 | 기존 테스트 경로에 polarity, explicit subject, no-people, compact budget, user-hard-intent 사례를 추가하고 material failure를 실행 지식에 기록한다. | 새 테스트가 현재 오동작을 정확히 재현하고 기존 통과 사례는 유지되는지 확인 | 실패 원인과 의도된 출력 변화가 구현 전에 고정됨 |
| 2. typed requirement와 prompt 조립 | user visible, role positive, soft, negative를 분리하고 phrase-level mandatory intent와 final-budget-aware compact 조립을 구현한다. | `회사원`/`제빵사` focused pack·audit·direct replay | meta/negative mandatory 0, user hard intent 보존, negative bytes 동일, 회사원 compact 50–120 words, minified pack 120,000 bytes 이하 |
| 3. 명시적 피사체와 no-people 라우팅 | 좁은 curated subject route와 request-level exclusion을 sampler·facet·adult eligibility에 전달한다. | `고양이`와 no-people product positive/negative control | 고양이는 animal/non-human subject이고 adult default off; no-people pack에는 human facet/subject/adult activation이 없음; generic human 경로는 동일 |
| 4. 결정적 성능 개선과 bounded cleanup | alias match, intent constraint, rule context의 반복 계산을 제거하고 unused candidate-term 계산과 중복 render-directive 블록만 정리한다. 필요한 SKILL/reference 정합성을 최소 갱신한다. | 고정 3-run 성능, canonical SHA, focused photo suites, validator/index/contradiction, 전체 discovery와 `git diff --check` 각 최종 1회 | 중앙값 5.082초 이하 또는 기준 대비 30% 이상 단축, 성능-only 출력 byte parity, photo 실패 0, baseline 외 새 전체-suite 실패 0 |

## 최종 완료 기준

1. 기존 public CLI 옵션, low-level neutral `generate_once`, semantic/rule/hybrid, adult defaults/opt-out, creative/viewer/hybrid, safety, negative, composed-audit 기능이 유지된다.
2. 내부 soft/meta/negative 문장은 positive mandatory intent가 아니며 user-authored hard visible requirement와 역할 정체성의 positive evidence는 계속 감사 가능하다.
3. 고정 `고양이`와 no-people product가 올바른 subject/facet/adult 결과를 만들고 generic human/animal/product negative controls를 회귀시키지 않는다.
4. `회사원` compact direct prompt는 50–120 words이고 minified candidate pack은 120,000 bytes 이하이며, 길이가 긴 명시적 사용자 요구는 조용히 삭제·절단하지 않고 별도 hard constraint로 보존한다.
5. 고정 성능 중앙값은 5.082초 이하 또는 기준 대비 30% 이상 개선되고, 성능-only 변경 전후 canonical output SHA가 동일하다.
6. focused photo tests, dictionary validator, semantic-index integrity, contradiction check가 통과하고 전체 discovery의 photo 실패는 0이며 알려진 unrelated baseline 실패 집합을 늘리지 않는다.
7. 실제 코드/정책/프롬프트 동작 변경 없이 테스트·문서·보고서만 존재하는 상태로는 완료할 수 없다. 이미지 품질, 보편적 관객 반응, semantic-index 메모리 개선은 완료 주장에 포함하지 않는다.

## 완료 증거

- typed role/negative/soft requirement와 source/polarity/priority/mandatory intent 계약을 구현했다. public additional-requirement와 ordinary direct/golden/frozen 경계는 유지했다.
- exact `고양이` subject route와 request-level no-people 전파를 적용해 non-human/no-people subject, facet, adult-appeal 결과를 교정했다.
- 고정 `회사원` pack은 151,732에서 95,146 minified bytes로 줄었고 mandatory/uncovered는 93/60에서 1/1로 줄었다. compact direct prompt는 191에서 105 words로 줄면서 역할 evidence를 유지했다.
- 고정 3회 성능은 2.813/2.047/2.125초, 중앙값 2.125초로 기준 7.260초 대비 약 70.7% 단축됐다. 세 출력 SHA와 캐시 on/off stdout/stderr가 byte-identical하다.
- focused photo 309 tests, dictionary, 112/112 scene-expression, 6,513-entry semantic-index integrity, 2,001 contradiction generation/0 violations, golden/frozen replay, `git diff --check`가 통과했다.
- 전체 discovery는 505 tests, 11 failures/1 error로 기존 unrelated universal-scene 기준선과 동일하며 photo 신규 실패는 0이다.
- 이미지 생성·픽셀 검토는 수행하지 않았고 이미지 품질이나 관객 반응은 완료 주장에 포함하지 않는다.
- 실행 지식: `docs/failed-reports/2026-08-11-photo-mandatory-intent-polarity-contamination.md`를 resolved로 갱신하고 `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`와 양방향 연결했다.

## 검증 수준과 예산

- 위험 수준: 중간. 로컬 prompt/routing/runtime 변경이며 외부 상태 변경은 없지만 deterministic output, negative polarity, adult eligibility와 기존 composition contract가 중요하다.
- 반복 중 focused 검증: 변경한 함수와 네 개 고정 입력, 관련 기존 photo contract test만 실행한다.
- 최종 검증: fixed performance 3-run 한 번, focused photo suites 한 번, dictionary/index/contradiction 한 번, full discovery 한 번, `git diff --check` 한 번.
- 구현 iteration: 동일 root cause별 최대 2회. 두 번째 실패 뒤에는 기준 완화, golden 덮어쓰기, verifier 확대를 하지 않고 failure report를 갱신하고 안전한 후속 결정을 요청한다.
- 검증 확장 전 질문 조건: semantic index 재생성, 새 embedding/API/유료 서비스, 이미지 생성, pack schema 전면 버전업, public CLI/JSON 필드 제거, 대규모 모듈 이동이 필요할 때.

## 중단 조건과 진행 로그

- 중단하고 질문할 조건: 사용자 요구를 보존하면서 120-word/pack-size 목표를 동시에 만족할 수 없음, 기존 public contract 제거 필요, unrelated dirty work 발견, credential·외부 비용·배포·파괴적 변경 또는 실질적 범위 확대 필요.
- 실패 iteration 한도: 고정 조건에서 같은 원인의 product repair 최대 2회.
- 로그 형식: `product delta -> direct evidence -> remaining product gap -> blocker`.
- 자동 stretch나 P3 semantic-index 최적화로 넘어가지 않는다.

## 실행 지식 계약

- 시작·재개 때 `docs/failed-reports/`와 `docs/passed-reports/`의 파일명·헤더 메타데이터를 범위, 경로, 환경, 오류, 접근법, lifecycle, 최신순으로 평가한다. 기본 전문 읽기는 최대 5건이며 현재 소스와 직접 증거가 과거 보고서보다 우선한다.
- material failure가 가정·완료 기준을 깨거나 rollback/redesign을 요구하거나 재발 가능하면 재시도 전에 기존 matching report를 갱신하거나 `docs/failed-reports/YYYY-MM-DD-<slug>.md` 하나로 통합한다. transient typo나 즉시 교정된 명령 오류는 기록하지 않는다.
- 모든 저장 증거는 현재 시스템 날짜·시간을 사용하고 credential, token, secret, 민감 endpoint, 고객·개인정보를 제거한다. 원문을 저장할 수 없으면 sanitized conclusion과 접근 제한 증거 참조만 남긴다.
- 최종 기준이 모두 통과한 뒤 성공 보고서는 목표당 기본 최대 1건만 허용한다. `material failed report 해결`, `같은 고정 조건에서 기본/문서 접근 실패 뒤 발견한 비자명한 대안`, `현재 코드·문서에서 싸게 복원할 수 없는 다단계 재현 절차` 중 하나를 명시적으로 만족해야 한다.
- 실패/성공 lifecycle 링크는 같은 변경에서 양방향으로 갱신한다. 해결된 failure는 `resolved`와 `Related passed reports`를, 성공은 대응 failed report를 기록한다. 기존 성공이 무효화되면 이를 `superseded`로 갱신한다.
- 보고서 작성은 checkpoint나 product progress가 아니며 구현을 지연시키지 않는다. 최종 요약에 적용·생성·갱신한 실행 지식 경로를 모두 기록한다.
