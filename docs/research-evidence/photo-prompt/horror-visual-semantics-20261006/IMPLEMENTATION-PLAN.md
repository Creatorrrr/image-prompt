# 호러 데이터 반영 계획

2026-10-06 KST · 상태: PROPOSED_NOT_RUN. 현재 요청의 완료 범위는 연구와 반영 계획이다.

## 목표와 완료 조건

단어 수를 늘리는 대신 문맥에 맞는 의미를 검색하고, 실제로 보여야 하는 구성·소유자·관계를 후보팩에 전달한다. 사용자가 요구하지 않은 인원·종·복식·노출·위협·피·의식·조명은 자동 추가하지 않는다.

완료 조건은 다음 증거를 각각 통과하는 것이다.

- 원본 의미: 구체 관계와 인접 개념을 구분하고 문헌·판본 공백을 보존한다.
- 원본 자산: 고유 ID, 올바른 슬롯·facet·component·bundle·manifest 등록, 기존 의도 보존.
- 검색: 정확한 문맥·부정·유사어·동음이의어·정의 우선 처리와 advisory lane 분리.
- 후보팩: 노출과 선택을 따로 확인하고 선택 시 모든 관계·멤버 증거를 보존한다.
- 프롬프트·runtime: literal evidence, property/intent locks, source와 core hash, strict gate-set.
- 이미지: 각 지정 소유자와 비교 관계가 같은 원본 출력에서 모두 보임.
- 실제 평가: 지시 충족·공포 인상·예술적 선호·사용자 수용을 별도 기록함.

현재 완료된 것은 연구 패키지 작성과 구조 검증뿐이다. 위 실행 완료 조건은 아직 적용 전이다.

## 0단계: 기존 체크아웃과 의미 기준 확보

현재 기본 체크아웃에 다른 작업의 미반영 변경이 많이 있다. [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json)에 HEAD, branch, 당시 status와 기존 skill/tests 파일 792개 해시를 기록했다. 다른 작업을 stash·reset·commit하지 않는다.

실제 반영을 시작할 때 해당 작업에 맞는 활성 worktree를 확인하고 필요하면 깨끗한 작업 공간을 사용한다. dirty authored source를 읽어야 한다면 원본 스냅샷을 먼저 확보하고 기존 의도별로 병합한다. 현재 연구의 SHA와 live source가 달라졌다면 영향 범위를 다시 계산한다.

보존할 원본은 `human_ghost_identity_breach`, `uncanny_coherence_mismatch`, `liminal_transition_use_gap`, 환등 공연, 유령선과 광학 고스트 등이다. 기존 exact alias 또는 profile의 duty를 넓히는 작업과 새 구체 관계를 추가하는 작업을 혼동하지 않는다.

**완료 조건:** 원본별 변화와 신규 proposal을 구분하고 새 ID/기존 ID의 의미 대응을 검토한 revision manifest가 있음.

연구 후반의 해시 비교에서 기존 7개 파일의 변화가 감지됐다. [SOURCE-DRIFT-NOTE.md](SOURCE-DRIFT-NOTE.md)의 skill·composition·authorial core·audit 관련 파일을 실제 반영 전에 다시 대조한다. 당시 current loader/compiler를 이용한 연구 구조 검증은 통과했지만 이 스냅샷을 덮어쓰기 기준으로 쓰지 않는다.

## 1단계: 원본 배치와 중복 해소

| 파일·표면 | 처리 | 현재 연구의 투영 자료 |
|---|---|---|
| `assets/photo_prompt_horror_extension.json` — 신규 제안 | 기존 source에 맞는 것은 재사용하고 남은 slot 후보·짧은 concept_units·relations·선택형 visual_semantics를 추가 | CANDIDATE-DRAFTS, BUNDLE-DRAFTS |
| `assets/photo_prompt_visual_obligations_horror.json` — 신규 제안 | 구체 비교 관계의 authored_components를 추가. broad mood는 새로운 exact hard alias로 추가하지 않음 | PROFILE-PROTOTYPES, SEMANTIC-UNITS |
| `assets/photo_prompt_legend_extension.json` | 이미 있는 원귀·유령·귀환 정체의 의미를 보존하며 인접 coverage만 검토 | EXISTING-DATA-CATALOG, RUNTIME-MAPPING |
| `assets/photo_prompt_imaginal_extension.json` | 일반 언캐니·리미널·환등 공연·공간 모순과의 중복 및 다른 의미 검토 | EXISTING-DATA-CATALOG |
| 조명·촬영·색·재질 관련 기존 source | `low_key`, `high_key`, `rim_light`, `backlight`, `deep_focus`, `shallow_depth`, `frame_within_frame` 등을 재사용 가능한 범위에서 보강 | REUSE-CRAFT-CATALOG |
| `assets/photo_prompt_source_manifest.json` | candidate와 visual_profile 원본을 여기에만 등록. 현재 row order와 required 정책을 유지 | CURRENT-CONTRACT |
| `photo_prompt_semantic_index.json` 및 참조 shards | 원본에서 재생성 | 원본 채택 뒤에만 실행 |
| `photo_prompt_visual_profile_index.json` 및 참조 shards | compiled registry에서 재생성 | profile 채택 뒤에만 실행 |
| `docs/research-evidence/photo-prompt/horror-visual-semantics-20261006/` | 출처·판본·조회 한계·ID 대응·planned 검증 보존 | 본 패키지 |
| `tests/fixtures/photo_prompt/horror_visual_semantics_v1.jsonl` — 신규 제안 | 독립 문맥 요청, 문화 혼동, optical/media 음성, 부정/lock 조건 | REGRESSION-PLAN을 개발용 출발점으로 사용 |

표의 신규 자산과 fixture는 아직 없다. 정확한 source basename·load order·required 여부는 반영 시 current manifest를 기준으로 확정한다. generator의 filename 목록이나 `required_extensions`를 별도로 authoring하지 않는다.

21개 기존 인접 매핑은 동일 의미로 확인한 목록이 아니다. 예를 들어 `appearing_only_in_reflection`의 현실 부재 계약은 표정이 다른 일반 반사 계약으로 덮어쓰지 않는다. 동일하게 `hard_flash`는 모든 hard light의 동의어가 아니므로 광질 설명만 공유하고 플래시 장치 의미를 보존한다.

**완료 조건:** 신규 후보 ID 충돌·의미상 중복·부적절한 기존 의미 확장이 제거됨. proposed entry의 empty tags/aliases와 제한된 fields는 live 채택 전에 current schema·compatibility·facet를 구체적으로 작성함.

## 2단계: P0 — 비교 관계와 소유자

먼저 다음 관계를 작은 추가분으로 구현한다.

| 관계 | 필요한 소유자와 증거 | 주요 반증 |
|---|---|---|
| 거울 표정·자세 불일치 | 실제 인물 / 거울 면 / 같은 반사 정체 / 특정 입·손 상태 | 다른 사람, 다른 촬영 각도, 전체 반사 붕괴 |
| 독립 그림자 자세 | caster / 연결된 그림자 / 광원 / 다른 손 자세 | 두 번째 caster, 설명 가능한 여러 광원 |
| 추가 인원 반사·CCTV | 대응하는 실제 구역 / optical 또는 display plane / 명확한 인원 비교 | 화면 밖 인원, 다른 시점·시야 |
| 도플갱어 | 동일 외형 / 독립 물리 위치 / 행동 차이 | 정상 반사, 단순 쌍둥이 |
| 반투명 몸 | 몸 경계 / 통과해 보이는 뒤 구조 / 정상 주변 가림 | 투명 옷, unrelated double exposure |
| 부유 | 발 둘 / 바닥 / 틈 / 지지·그림자 관계 | 발 crop, 바닥 안개, 단순 점프 |
| 신체 접합 | 같은 몸 / 서로 다른 구조 / 연결띠 또는 접점 | 별도 소품, 목걸이, 의상 접착만 |
| dust·최근 사용 모순 | 쌓인 표면 / 국소 지워진 영역 / 읽히는 윤곽 | 전체 grunge overlay, 칠한 실루엣 |

형상 변형은 실제 해부학 고장과 구별하여 frozen request가 허용한 허구 body geometry에만 적용한다. 조명 profile과 body profile이 필요한 눈·발·접합을 서로 가리지 않는지 composition 수준에서 검사한다.

`photo-authored-visual-components/v2`로 모든 비교 구성원을 discovery group에 선언하고 collective obligation에 연결한다. discovery 최소 충족은 활성화된 전체 evidence/pixel duty를 줄이는 조건이 아니다. exact activation은 명확한 관계 문구에만 한정하고 broad “horror/uncanny/ghost”는 새 hard profile의 트리거로 사용하지 않는다.

**완료 조건:** exact 문맥 양성·부정·approximate advisory·선택 미채택·선택 증거 누락·owner 변경·gate 누락 검증이 current contract에서 모두 통과함.

## 3단계: P1 — 장르·공간·빛·색·재질

250개 카드를 한 번에 live source로 복사하지 않는다. P0가 통과한 뒤 아래 순서로 작은 의미 단위를 반영한다.

1. 유지된 사용 공간과 부재, 좁은 출구, 전경 가림, deep/shallow focus의 증거 충돌.
2. 밝은 낮의 위협, 공동체 경계, 코즈믹 공간 기준 모순, 지알로의 불완전 목격.
3. 키광/보조광·광원 방향·shadow edge·림 영역·practical source.
4. 12개 팔레트의 색 소유자와 크기·영역·수신 표면. HEX 자체를 hard gate로 만들지 않음.
5. 젖은 머리 피부 접촉, 부식과 닦인 접점, 균사 경계, 신체 접합 재질.

optional 묶음 12개는 scene preset이 아니다. 선택하지 않으면 추가 duty가 없고, 선택하면 멤버와 directed relation을 완전하게 보존한다. 순위·점수·candidate order는 의미 권한이 아니다. 새 raw score나 private routing 답 목록을 공개 pack에 추가하지 않는다.

현재 `slot_dimensions`에서 `prop`와 `gaze_target`처럼 빈 범위인 슬롯도 있다. 이를 임의로 `action` 또는 `expression`으로 승격하지 않는다. 후보의 실제 효과가 기존 락 아래 실현될 수 없으면 거절하거나 현재 지원하는 관계/profile/authorial 표현으로 옮긴다. `body_geometry`, `color`, `material` 등 실제 canonical dimension을 사용한다.

**완료 조건:** 같은 frozen meaning에서 과도한 detail quota 없이 제안을 선택하거나 거절할 수 있음. 속성 락·인원·종·필요 가림·매체 영역을 바꾸는 후보는 유효하게 차단됨.

## 4단계: P2 — 문화·판본과 추가 출처

| 항목 | 채택 전 필요한 추가 증거 |
|---|---|
| 처녀귀신 | 흰 소복·풀어진 머리의 대중매체 도상과 역사적 전승을 구별하는 원문·이미지 소장품 또는 작품 판본 |
| 물귀신 | 특정 수역·망자 맥락과 매체별 젖은 외형을 각각 확인하는 자료 |
| 유레이 | 선택한 판화/회화의 직접 소장품 record와 보이는 복식·lower-body 처리 |
| 장산범 | 현대 괴담·웹툰·영화별 외형과 모방 규칙의 일차 자료 |
| 구울 | 전승의 시체/무덤 관계와 현대 작품 해부학을 구별하는 자료 |
| 페낭갈란 | 말레이 지역·전승 판본의 신뢰할 자료와 다른 동남아 머리 분리 존재의 비교 |

총각귀신·객귀·무주고혼, splatterpunk 계보, ero-guro 역사 범위와 일부 금기 정의도 근거 공백을 후속 조사한다. 지금의 metadata-only 문헌이나 원 대화 인용을 전문 확인으로 계산하지 않는다.

문화·작품 판본은 연구 sidecar에 둔다. retired `cultural_provenance`, `market_origin`, `term_level` 등의 runtime 키로 되살리지 않는다. 의식·기호·의복을 다른 문화의 기본값으로 교환하지 않는다.

**완료 조건:** 고정 외형을 넣을 만큼 구체적인 판본 근거가 있거나, 요청으로 판본을 명확히 선택할 수 있음. 확인되지 않은 변형은 held로 유지함.

## 5단계: 시간·음향과 맥락 데이터의 반영

시간 항목 16개, 음향 항목 18개, 비시각/비평 맥락 28개는 연구 정의와 confusion boundary를 보존한다. 정지 이미지 pipeline에 “목소리가 들림”, “오래 멈춤”, “빛이 깜박임” 같은 검증 불가 hard gate를 추가하지 않는다.

영상 또는 음향 기능을 실제로 작업할 때에는 별도 매체 계약으로 source 위치·처리·duration·순서·동기화 증거를 설계한다. 아직 그 runtime 구현을 이 데이터 연구에 포함하지 않는다. 시각적 대체 단서를 선택할 수 있어도 원래 소리·시간 의미가 성공한 것으로 판정하지 않는다.

## 6단계: 인덱스·계약·검색 검증

활성 원본을 실제 채택한 뒤 실행할 명령이다. 이번 연구에서는 실행하지 않았다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 1 --progress
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python -m unittest tests.test_photo_candidate_semantics tests.test_photo_core_retrieval tests.test_photo_bm25f_retrieval tests.test_photo_visual_profile_retrieval tests.test_photo_visual_profile_shards tests.test_photo_prepack_isolation -v
```

영향 범위에 맞는 새 호러 fixture·registry/manifest·composition/strict gate-set 테스트를 먼저 실행하고, 여러 독립 경로 변경 또는 미해결 회귀 위험이 있으면 full discovery로 확장한다. 위 명령이 모든 새 호러 테스트를 대체하지 않는다.

인덱스는 authored source에서 재생성한다. entry key, 완전한 embedding text, provider, model, dimensions가 동일한 벡터만 재사용한다. 생성 shards를 먼저 durable하게 저장한 뒤 manifest를 전환한다. 동작 중인 reader와 다른 manifest가 가리키는 파일을 제거하지 않는다. 새 출처 URL·원문·연구 ID가 semantic text와 공개 pack에 섞이지 않는지 검사한다.

검색 검증은 source-derived 개발 사례 728건과 전역 통제 14건을 출발점으로 한다. 구현 전에 별도 작성한 KR/EN/CJK 자연 요청, 기존 frozen holdout을 일반화 평가에 사용하고 실패를 맞추려고 정답을 약화하지 않는다. “분류 논문에서 horror를 설명해줘”와 실제 호러 이미지 요청, quoted keyword와 active request, ghostwriter/ghost kitchen/광학 ghosting을 구분한다.

**완료 조건:** dictionary·registry·manifest hash, exact/BM25F/vector recipe와 shards가 current authored source와 일치함. 신규 데이터 노출과 hard authority가 별도로 증명됨.

## 7단계: 후보팩부터 원본 픽셀까지

22개 [검증 그룹](PIXEL-QUALIFICATION-PLAN.json)을 적용한다. source-held 그룹은 판본 근거 확보 뒤 진행한다.

A는 채택 전 독립 baseline, B는 같은 요청 의미에 검토한 신규 데이터를 사용하는 비교, C는 별도 요청으로 선언한 인접 혼동 control이다. C의 정답·요청은 다르므로 A/B 개선 비교에 섞지 않는다. A/B의 generation 조건이 불일치하거나 renderer 변동을 통제할 수 없으면 인과적 개선 주장은 제한한다.

각 실행에서 다음을 보존한다.

- 실제 요청·reference 사용 범위·core/intent-lock/creative controls 해시.
- 후보 pack·노출 inventory·채택/거절·literal component/relation evidence.
- 최종 prompt/runtime의 정확한 bytes, 두 audit, 생성 outcome·원본 파일·SHA-256.
- 선언된 전체 hard-gate set과 동일 이미지의 native/both-scale review.
- 지시 충족, 공포 인상·주제 전달·미적 선호, 사용자 판단을 별도 필드로 기록.

partial_is_fail를 유지한다. 가려진 비교 대상은 UNOBSERVABLE_NOT_PASS, 생성 차단은 BLOCKED_UNSCORED다. 프롬프트에 뜻이 있거나 전체 unit test가 통과한 것으로 픽셀 성공을 주장하지 않는다.

**완료 조건:** 각 반영 배치가 실제로 노출·선택되어 관련 관계를 원본 픽셀에서 모두 실현한 evidence가 있음. 전체 데이터가 검증된 것처럼 검증 범위를 늘려 보고하지 않음.

## 이 연구에서 실제 수행한 검증

```bash
.venv/bin/python docs/research-evidence/photo-prompt/horror-visual-semantics-20261006/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/horror-visual-semantics-20261006/validate_research.py
```

자세한 결과는 VALIDATION.json에 기록한다. 이는 research artifact의 연결·compiler 투영·원본 보존 검사이며, live adoption/index/retrieval/render 성공 증거가 아니다.
