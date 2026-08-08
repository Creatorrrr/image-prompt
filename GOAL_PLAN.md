# Reader-Centered Viewer Experience, Attachment, and Commercial Intent Goal

- 작성: 2026-08-08 22:06 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@4ee5041`
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: Viewer-Perceived Creative Direction and Authorial Voice (`docs/passed-reports/2026-08-08-viewer-perceived-creative-direction.md`)
- 자동 목표 상향: 비활성

## 1. 목표와 실제 산출물

### 원래 사용자 요청

창의성·독창성·작가성을 소재의 희귀함이나 장식으로만 다루지 않고, 이미지를 보는 독자가 왜 멈추고, 이해하고, 감정·공감·몰입·애착을 느끼며, 저장·재관람·공유·구매하는지를 프롬프트 생성의 입력으로 반영한다. 상업 이미지와 서브컬처 캐릭터에서도 각기 다른 독자 욕구와 행동 목적을 구분하며, 이를 후보팩 주제 데이터 증설이 아닌 일반 생성·선택·감사·픽셀 검수 계약으로 구현한다.

### 최종 제품/동작

1. 사용자가 창의적·작가적 결과, 독자 반응, 감동·공감·몰입·애착, 상업 목적, 서브컬처 캐릭터 관계를 명시하면 별도 재질문 없이 `viewer_experience` 경로가 활성화된다. 명시적 creative-direction 실행은 항상 이 경로를 포함한다.
2. 에이전트는 정확히 하나의 주 독자 욕구와 하나의 일관된 의도 경험을 선택하고, 첫 시선의 초점, 해석 가능한 질문, 감정의 원인이 되는 actor/action/target/consequence, 필요한 애착 채널, 선택적인 재관람 보상과 상업 목적을 구체화한다.
3. 보이는 증거만 `prompt_en`에 literal binding하고, “독자는 감동한다” 같은 결과 선언, 감정 나열, 얼굴/아동형 외형, 장르 용어, 스타일 형용사는 독자 경험의 증거로 인정하지 않는다.
4. 기존 `creative_direction`의 familiar anchor, one rule break, reveal path와 authorial grammar는 유지하되 `viewer_experience`가 “왜 독자가 신경 쓰는가”를 보완한다. 표면 craft와 provenance/실제 작가 이력은 계속 분리한다.
5. 상업·서브컬처·감동/의미의 고정 세 사례가 감사된 프롬프트와 최초 실제 이미지에서 각기 다른 독자 경험을 metadata-free로 전달하며, 주제·제품·성인성·사진적 정합성을 잃지 않는다.

### 범위

- `SKILL.md`, concept routing, composition/creative-direction references, 새 progressive-disclosure viewer-experience reference.
- candidate pack의 일반 `viewer_experience` composition contract와 agent-authored composed object.
- composed prompt audit, focused/unit tests, 고정 3사례 holdout과 기존 형식의 metadata-free visual review.
- 명시적 creative/commercial/subculture/affective 요청의 agent-layer 자동 활성화와 ordinary request 보수 기본값 보존.
- 기존 candidate provenance, scene/character grammar, automatic safety, negative byte preservation, typed cultural/IP/adult guards 보존.

### 비목표

- 후보팩 taxonomy·preset·semantic text·임베딩·주제별 장면 데이터를 추가하지 않는다.
- 인간의 실제 감정·구매·장기 애착을 세 이미지나 LLM 검수만으로 보편적으로 증명하지 않는다.
- 사람 패널, 장기 트래픽 실험, 광고 플랫폼 연동, 배포, commit, push, PR을 필수 범위에 넣지 않는다.
- 얼굴·아기 도식·과도한 각성·클릭베이트를 보편 engagement 공식으로 만들지 않는다.
- provenance, 진짜 작가 이력이나 시장 성과를 픽셀에서 추론하거나 꾸며내지 않는다.

## 2. 진척 계약

- 진척으로 인정: user request가 실제 viewer contract를 활성화하는 skill/runtime 변화, 감사가 소비하는 binding 구현, 서로 다른 목적의 감사된 프롬프트, 실제 PNG와 제품 원인 수리.
- 진척으로 인정하지 않음: 연구 요약·문서·스키마·fixture·테스트·리뷰 양식만 추가, 감정 단어/스타일 형용사 증가, `engagement` 단일 점수, prompt audit PASS만으로 독자 경험 주장, 여러 이미지 중 유리한 결과 선별.
- Stage 1 이후 각 checkpoint는 코드/스킬 동작 변화, 감사된 최종 프롬프트, 실제 이미지 또는 binding 구현 결정을 남긴다.
- 검증-only 작업 상한: focused 검증은 각 제품 변경 경계에서 한 번, full suite와 최종 visual gate는 Stage 6에서 한 번만 실행한다. 검증-only checkpoint를 연속으로 두지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.

## 3. 기준선과 고정 조건

### 현재 기준선

- `creative_direction`은 viewer-side surprise-to-insight와 authorial vantage/timing/omission/material rule을 이미 강제하고 실제 3사례 픽셀 자격을 통과했다.
- 현재 계약에는 target audience/context, primary viewer need, affect evidence, attachment channel, reinspection reward, commercial objective가 없어서 “왜 독자가 신경 쓰는가”와 “어떤 행동 목적을 위한 이미지인가”는 binding되지 않는다.
- character grammar는 sparse action/relationship evidence를 제공하지만 그것이 독자에게 care·relatedness·identity 중 무엇을 약속하는지는 선택하지 않는다.
- prompt audit는 literal evidence를 확인할 뿐 실제 감정 반응을 증명하지 않으며, 현재 visual review도 독자 욕구나 상업 목적별 판독을 직접 평가하지 않는다.

### 고정 활성화 행렬

- 명시적 creative/original/ingenious/authorial 요청: `creative_direction`과 `viewer_experience` 모두 자동 활성화.
- 명시적 독자 반응·감동·공감·몰입·애착·재관람 요청: `viewer_experience` 활성화, 창의성은 별도 명시가 있을 때만 상향.
- 명시적 광고·브랜드·상품 행동 목적: `viewer_experience` 활성화하고 commercial objective를 하나만 선택.
- 명시적 서브컬처 캐릭터의 관계·귀여움·애착 목적: `viewer_experience` 활성화하고 장르 literacy와 non-morphological attachment evidence를 요구.
- ordinary factual/documentary/photo 요청: 새 계약 absent, 기존 보수 경로 유지.

### 고정 세 사례

1. **상업/기억**: 재사용 가능한 무표기 보온병을 신뢰할 수 있고 기억에 남게 소개하는 광고 사진. `product_detail`, need `trust`, objective `remember`; 제품 즉시 판독과 기능 evidence가 재관람 장치보다 우선한다.
2. **서브컬처/애착**: 성인 현장 조사원과 작은 비인간 동료가 망가진 장비를 함께 복구하는 귀엽고 관계 중심의 사진. `full_screen`, need `relatedness`, attachment `reciprocity`; 귀여움은 youth morphology가 아니라 directed mutual action으로 표현한다.
3. **감동/의미**: 오래 살던 집을 떠나는 성인의 마지막 아침을 작가적으로 표현한 사진. `full_screen`, need `meaning`, attachment `self_relevance`; 한 주 감정 경험과 인과적으로 연결된 재관람 보상을 요구한다.

세 사례의 natural-language request, 예상 contract, fixed seed `900101`–`900103`, focus criteria를 구현 전에 동결한다. holdout/review 한 벌만 추가하는 이유는 기존 creative review가 originality/ingenuity/intentionality만 평가해 reader need, affect cause, attachment와 commercial-goal compatibility를 확인할 수 없기 때문이다.

### 적용한 과거 실행 지식

- `docs/passed-reports/2026-08-08-viewer-perceived-creative-direction.md`: familiar anchor와 one rule change, metadata-free pixels, bounded repair를 유지하며 candidate topic data를 늘리지 않는다.
- `docs/failed-reports/2026-08-08-creative-direction-pixel-premise-legibility.md`: literal prompt evidence는 relation rendering을 보장하지 않는다. 강한 모델 prior를 한 번 수리해도 이기지 못하면 이미 개발된 다른 시각 realization을 사용하고 anomaly를 쌓지 않는다.
- `docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`: subculture attachment는 nonvisual market labels가 아니라 한 primary visual mechanism과 최대 두 support cues의 sparse event로 표현한다.
- `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`: object presence가 아니라 actor, hand/action direction, target, simultaneous consequence를 고정하고 픽셀에서 재검증한다.
- `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`: 풍부한 evidence나 contract PASS가 흥미·인식·감정을 증명하지 않는다. 한 사건과 sparse clues를 사용하고 knowledge와 render expression을 분리한다.

## 4. 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 목표·holdout 동결 | 활성화 행렬, 세 natural requests, expected contract와 metadata-free focus를 구현 전에 저장 | 현재 pack에 viewer contract가 없고 기존 creative/character 계약이 유지됨을 직접 확인 | 성공 기준이 구현 전 고정되고 이전 목표 산출물과 작업 트리가 보존됨 |
| 2. Viewer-experience 생성 경로 | topic data 없는 `photo-viewer-experience/v1` candidate contract, agent-layer 자동 라우팅, progressive reference와 composition workflow 구현 | creative/commercial/subculture/affective 사례에서 enabled, ordinary 사례에서 absent; pack preset/slot equality | 사용자가 별도 필드 지시 없이 하나의 need·experience·context·objective 계약을 받음 |
| 3. Binding audit | composed `viewer_experience`, visible prompt evidence, affect actor/action/target/consequence, attachment/reinspection conditional rules, affect stacking·outcome-claim gaming 거부 구현 | 정상 3유형 PASS, missing/array-stacking/nonliteral/장르용어-only/상업 충돌 mutation FAIL | 문서 선언이 아니라 최종 prompt에 독자 경험의 시각 원인이 반영됨 |
| 4. 세 최종 프롬프트 | 고정 세 사례에 서로 다른 need/context/objective를 가진 감사 PASS prompt와 rationale 생성 | focused tests와 composed audit; negative bytes 및 scene/character contract 보존 | 상업 clarity, 상호 애착, 의미·재관람이 서로 섞이지 않고 각 prompt에 구체화됨 |
| 5. 실제 이미지 자격 | 각 사례 최초 PNG 1개와 metadata-free pixel review; 실패 시 product cause 기록 후 사례당 pristine rerender 최대 1회 | 원본 해상도와 썸네일 양쪽에서 first focal/premise/affect cause/goal compatibility 검수 | 3/3이 모든 필수 focus PASS, prompt metadata 없이 감정 원인과 목적을 설명 가능, topic/photo/safety 회귀 없음 |
| 6. 닫힌 회귀와 lifecycle | focused 결과, full unit, dictionary/scene/candidate 계약, visual review, `git diff --check`, 실행 지식 lifecycle 정리 | 기존 validator와 full suite 한 번, 최종 artifact hash/contract 확인 | 모든 완료 기준 통과, 미해결 material failure 없음, 실제 skill/runtime/audit/prompt/PNG 존재 |

## 5. 최종 완료 기준

1. 명시적 creative/commercial/subculture/affective viewer 요청은 별도 재질문 없이 viewer-experience 경로를 활성화하고 ordinary 요청은 기존 pack·prompt 동작을 유지한다.
2. 새 contract는 후보팩 주제·semantic index를 바꾸지 않으며 하나의 `primary_viewer_need`, 하나의 `intended_experience`, target context/audience, first-glance hook과 commercial objective를 구분한다.
3. affect는 actor/action/target/consequence의 보이는 원인으로 binding되고, 결과 선언·감정 나열·스타일 문구·얼굴이나 youth morphology·장르 용어만으로 PASS할 수 없다.
4. `care|relatedness|identity`는 적절한 attachment channel과 directed relation evidence를 요구하고, product `comprehend|act|remember` 목적은 제품 판독·신뢰를 수수께끼나 장식보다 우선한다.
5. audit는 missing contract, 다중 primary need/experience, nonliteral visual evidence, affect stacking, attachment/reinspection 조건 위반과 commercial-goal 충돌을 거부하면서 기존 ordinary/creative composed prompt를 회귀시키지 않는다.
6. 고정 세 사례의 감사된 실제 최초 또는 허용된 한 번의 pristine repair 이미지가 3/3 metadata-free 필수 focus를 통과하고 주제·제품·성인성·IP·사진적 정합성을 유지한다.
7. 기존 creative direction, character grammar, scene expression, candidate pack, safety와 negative-byte 계약 및 focused/full 회귀와 `git diff --check`가 통과한다.
8. 실제 skill/runtime/audit 변경, 감사된 세 prompt, 세 PNG와 versioned visual review가 존재한다. 계획·테스트·fixture·보고서만으로 완료할 수 없다.

## 6. 검증 수준과 예산

- 위험 수준: 중간. 로컬 agent composition/audit 계약을 바꾸며 외부 배포는 없지만, ordinary prompt 회귀·감정 과잉 지시·제품 가독성 훼손·이미지 모델 relation loss 위험이 있다.
- 반복 중: 변경 함수 focused tests와 세 rule-mode pack/audit만 실행한다.
- 이미지 예산: 세 사례 최초 1개씩. 필수 픽셀 relation 실패 시 cause-specific 구현/프롬프트 수리 후 사례당 pristine rerender 최대 1개; 실패 결과 보존, 이미지 편집과 batch selection 금지.
- 최종: dictionary/scene/candidate validator, full unit 1회, visual review/hash 검사 1회. 새 서비스나 사람 패널은 추가하지 않는다.
- LLM metadata-free review는 이번 로컬 제품 자격 evidence이며 실제 인구집단 감정·구매 효과의 증명으로 표현하지 않는다.
- taxonomy/semantic text/index가 바뀌면 범위를 벗어난다. 외부 임베딩 전송이나 index rebuild를 시작하지 말고 먼저 질문한다.

## 7. 중단 조건

- 같은 근본 원인의 구현/픽셀 수리 1회 뒤에도 필수 관계가 보이지 않을 때에는 기준을 완화하지 않고 실패 evidence와 model/product boundary를 보고한다.
- 통과를 위해 기존 safety, adult, IP, cultural provenance, scene/character grammar를 약화해야 할 때.
- 실제 감정·구매 효과를 주장하려면 사람 모집, 유료 광고, 장기 트래픽 또는 외부 서비스가 필수인 지점에 도달할 때. 로컬 구현은 계속하되 해당 주장은 blocked external evidence로 분리한다.
- 현재 `main`의 미푸시 7커밋이나 선행 자격 artifact를 훼손·재작성해야 할 때.
- commit, push, 배포, semantic index 변경, credential 또는 파괴적 변경이 필요할 때에는 별도 권한을 요청한다.

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

### 2026-08-08 22:06 KST / 목표 생성 및 실행 지식 적용

- product delta: 완료된 creative-direction 목표 위에 독자 욕구·감정 원인·애착·재관람·상업 목적을 일반 composition/audit/pixel 계약으로 추가하는 새 후속 목표를 고정했다.
- direct evidence: current source와 report metadata를 확인하고 exact product/failure match 5건을 전문 검토해 활성화 행렬, sparse evidence, metadata-free pixel gate와 수리 상한에 적용했다. `main@4ee5041` 작업 트리는 깨끗하고 원격보다 7커밋 앞서 있으며 선행 결과는 current 상태다.
- remaining product gap: Stage 1 holdout 동결부터 viewer contract/runtime/audit, 세 prompt와 실제 image qualification, 닫힌 회귀가 남아 있다.
- blocker: 없음.
- execution-knowledge paths: 3절의 passed 2건과 failed 3건.

### 2026-08-08 22:11 KST / Stage 1 viewer holdout 동결

- product delta: 상업/기억, 서브컬처/상호 애착, 감동/의미의 세 natural-language 사례와 서로 다른 context·need·objective·attachment 기대값, 고정 seed, metadata-free pixel focus를 `assets/render_viewer_experience_holdout_v1.jsonl`에 구현 전에 동결했다.
- direct evidence: 현재 `main@4ee5041`의 동일 세 rule-mode pack은 `viewer_experience`가 모두 absent이고 pack ID는 `cd2a38dd083d563b`, `69fedb0b5f6de842`, `618310a49bde8f66`이다. 세 번째만 기존 `creative_direction`이 present여서 선행 계약과 새 viewer 계약의 차이를 직접 확인했다. JSONL 3행 parse/count와 `git diff --check`가 통과했다.
- remaining product gap: Stage 2 viewer contract/runtime/agent routing과 Stage 3 binding audit 구현이 남아 있다.
- blocker: 없음.
- execution-knowledge paths: 기존 5건 재사용, 새 material failure 없음.

### 2026-08-08 22:23 KST / Stage 2-3 viewer contract와 binding audit

- product delta: topic taxonomy를 추가하지 않고 `photo-viewer-experience/v1` candidate contract, explicit `--viewer-experience`, high-creativity 자동 포함, agent-layer commercial/subculture/affective routing 문서와 composed `viewer_experience` audit를 구현했다. 하나의 need/experience, audience/context, actor/action/target/consequence, attachment/reinspection/commercial conditional binding을 강제한다.
- direct evidence: ordinary pack은 새 필드 absent이고 explicit viewer pack은 기존 presets/slots/negative와 동일하며, high-creativity pack은 creative와 viewer 계약을 함께 갖는다. 정상 계약과 missing/stacked/nonliteral/outcome-claim/weak-label/youth-morphology/commercial/reinspection mutation focused tests가 통과했다.
- remaining product gap: 세 고정 prompt와 실제 PNG의 metadata-free 제품 자격 및 전체 회귀가 남았다.
- blocker: 없음.
- execution-knowledge paths: `references/viewer-experience-contract.md`, 새 material failure 없음.

### 2026-08-08 22:34 KST / Stage 4-5 감사 prompt와 최초 렌더 자격

- product delta: 상업 trust/remember, 서브컬처 relatedness/reciprocity, 의미 meaning/self_relevance의 서로 다른 composed prompt를 작성하고 내장 이미지 도구로 사례당 최초 1장만 생성했다. 세 prompt는 audit와 quality 모두 PASS, failures/warnings 0이며 negative bytes를 보존했다.
- direct evidence: 제품은 무표기 보온병·분리 뚜껑·손의 gasket 유지보수가 즉시 읽히고, 동료 장면은 성인 작업자의 pliers 응답과 비인간 동료의 brush/위험 지시가 한 고장에 수렴하며, 이사 장면은 열쇠 제거와 열린 문 뒤로 가구 부재의 밝은 벽 흔적과 마모 경로가 재해석을 만든다. PNG SHA-256은 `25c1c1c48c5980c2b4561016626fb9fa973ab232dfc647b61a1c76aea9ce0b2b`, `ec0b6fa6dab542904b5d423bdb4f6bf35819f82cebf162612504ffbac1acf1d9`, `92a88152fdde6efbae5cdfc17eb611d4bd8b3eb7b9f0aa74625c9e0a1dfe9b58`이며 편집·재렌더·batch selection은 0이다.
- remaining product gap: 전체 회귀, semantic-index 무변경, diff와 lifecycle 종료 확인이 남았다.
- blocker: 없음. 이사 장면의 작은 hook patch는 명확한 열쇠 모양이 아니지만 복수의 가구 부재 흔적과 문으로 향하는 바닥 경로가 동일한 causal second reading을 유지한다는 한계를 리뷰에 기록했다.
- execution-knowledge paths: `assets/render_viewer_experience_visual_review_v1.json`, 새 material failure 없음.

### 2026-08-08 23:08 KST / Stage 6 닫힌 회귀와 목표 완료

- product delta: holdout과 versioned visual review를 skill resource로 연결하고 contract test를 추가했으며, 최종 구현·문서·감사·실제 렌더·ledger·lifecycle을 닫았다.
- direct evidence: dictionary validator PASS, merged scene audit 112/112 PASS, semantic index check PASS(`dictionary_hash=930f5f4359ed51f5784cc0b75923f2702495590c48811dd359c776660d07d6d2`, 6,513 entries, index diff 없음), visual review 3/3·18/18 focus PASS, focused 4/4 PASS, full unit `Ran 404 tests in 1673.594s` OK, `git diff --check` PASS다.
- remaining product gap: 없음. 사람 집단의 실제 감정·기억·구매 효과는 이 로컬 자격의 주장 범위 밖이며 별도 human evaluation이 필요하다.
- blocker: 없음.
- execution-knowledge paths: `docs/passed-reports/2026-08-08-reader-centered-viewer-experience.md`; unresolved material failed report 없음.
