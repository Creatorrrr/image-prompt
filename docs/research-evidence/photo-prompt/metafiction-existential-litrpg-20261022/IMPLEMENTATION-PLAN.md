# 리서치 결과의 데이터 반영 계획

이 문서는 연구 후의 실행 설계다. 이 조사에서는 아래 운영 반영·검색·이미지 실험을 실행하지 않았다.

## 1. 목표와 채택 조건

목표는 메타픽션·실존공포·LitRPG 요청에서 추상 단어만 반환하는 대신, 요청과 호환되는 **온전한 소유자·비교·매체·접속 관계**를 실제 후보로 발견하고 이미지에 옮길 수 있게 하는 것이다. 일반 요청에 공포·UI·복제·성적/폭력적 사건을 끼워 넣지 않는 조건도 함께 만족해야 한다.

데이터 수나 테스트 수 자체가 완료 기준은 아니다. 채택에는 다음 증거가 필요하다.

1. 의미: 원 용어 130개가 가시 형태·단서·시간·문맥의 경로를 유지하고, 초안의 한영 의미와 소유자·조건·효과를 실제 소스 기준으로 심사한다.
2. 발견: 핵심 12개 관계군 각각에 대해 한국어·영어 모두 호환하는 완전 소스가 실제 top8에 최소 하나 노출된다. CID/RID·원문·허용 역할·샘플 노출은 별도로 기록한다.
3. 경계: 문맥/일반 대조에서 요청에 없던 정체·생사·의식·동의·질병·성적/폭력적 사건을 자동 채택한 사례가 0건이어야 한다.
4. 표현: 핵심 사례의 요구 성분·방향·연속성·숫자·비교 대상이 원본 픽셀에서 보이고, 개별 gate뿐 아니라 전체 사례가 통과해야 한다. 가림과 부분 표현을 합격으로 세지 않는다.
5. 효과: 기존 대비 개선 주장은 같은 요청·예산·평가기준의 비교에서 확인한다. 수동으로 넣은 문장의 렌더 성공과 검색을 통한 개선을 구별한다.
6. 설치: 소스·인덱스·런타임 generation·검토 근거의 해시가 맞고 이전 세대로 돌아갈 방법이 검증되어야 한다. 설치 후에도 사용자 표현 수용은 별도다.

자연어 성능 일반화에는 이 패키지로 저술하지 않은 요청이 추가로 필요하다. 독립 요청이 없으면 `independent_holdout: NOT_AVAILABLE`로 남기고 개발 세트의 범위를 넘는 주장을 보류한다.

## 2. 시작 스냅샷과 중복 심사

첫 조사 HEAD는 `17c0dd349304a18abac290beae114f199114e379`다. 다수의 기존 dirty/untracked 파일이 있었고 보존했다. [BASELINE.json](BASELINE.json)은 추적 파일 7,936개와 manifest에 연결된 운영 보호 파일 62개의 해시를 담는다. 후보 원문 감사 시점은 총 19,471개 레코드·13,644개 바인딩·59개 모듈이었다. 이는 긍정 visual_option 수나 인덱스 RID 수가 아니다. 동시 작업으로 이후 상태는 달라질 수 있다.

실행 직전 HEAD, staged/unstaged/untracked 목록, manifest와 모든 모듈, slot catalog, search layout, 작업 소스와 설치된 runtime pointer를 다시 고정한다. 기존 연구 스냅샷을 새 상태로 덮지 않고 별도 baseline을 남긴다. 숫자 차이만으로 source/index 불일치라고 단정하지 않는다. 파일 종류와 ID 단위가 다른지 먼저 확인한다.

64개 초안 각각에 아래 판정을 붙인다. `new`는 조사 중 검색어가 안 나왔다는 이유로 확정할 수 없다.

| 판정 | 적용 조건 | 실제 작업 |
|---|---|---|
| reuse | 기존 완전 원문·가시 관계·조건·효과·역할이 요청을 그대로 충족 | 새 CID를 만들지 않고 기존 source를 사용. 필요한 검색 별칭은 의미를 바꾸지 않는 범위만 심사 |
| refine | 비교 개체·경계·부품·접점·한영 대응의 일부가 부족 | 기존 의미를 보존하는 명시 diff를 작성. 호환 불가한 강화라면 독립 variant로 분리 |
| new | 동등한 완전 관계가 없다고 실제 원문/조건/효과 검토로 확인 | 새 후보와 필요한 바인딩을 만들고 provenance를 연결 |
| context | 가시 외형으로 주장할 수 없는 의미·규칙·윤리·원전 정보 | 문맥/진단 경로에 유지. 긍정 이미지 처방으로 바꾸지 않음 |
| defer | 시간·상호작용·다중 패널·읽히지 않는 필수 텍스트 등 평가 단위가 맞지 않음 | 필요한 매체·검증을 명시하고 현 정지 이미지 qualification에서 분리 |

구체적인 기존 CID와 판정은 [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) 및 [reviewed-neighbors.json](reviewed-neighbors.json)에 있다. C01은 기존 도플갱어 관계를 우선 검토한다. C05/G01은 기존 보철 접점을 재사용하되 옆의 분리 부품·기어·피부 경계를 추가하면 전체 효과를 다시 심사한다. B02/B03/B05는 기존 문서·삭제·불일치 후보와 겹치므로 복사 등록하지 않는다. D01의 TTRPG 기존 소품은 `ttrpg_practice` 조건을 제거해 판타지 세계 내부 상태창으로 재활용하지 않는다.

## 3. 제안 파일과 데이터 계약

다음은 **후속 구현에서 만들 수 있는 경로**이며 현재 생성한 운영 파일이 아니다.

| 제안 대상 | 내용 |
|---|---|
| `assets/photo_metafiction_existential_litrpg_semantics_20261022.json` | 승인된 가시 성분·방향 관계·문맥 구분·출처/판본·혼동 경계 |
| `assets/photo_candidate_metafiction_existential_litrpg_20261022.json` | 중복 심사를 통과한 완전 시각 원문/조건/효과의 후보 |
| `assets/photo_candidate_metafiction_existential_litrpg_bindings_20261022.json` | 검토된 실제 slot 연결만. 한 카드의 모든 슬롯 제안을 무조건 등록하지 않음 |
| `references/metafiction-existential-litrpg-semantics.md` | 사용자가 이해할 수 있는 의미 구분과 선택 원칙 |
| corpus manifest / search layout | 검증된 소스 모듈 등록과 별도 인덱스 생성의 결과만 반영 |

현재 149개 슬롯 가운데 이 초안이 제안하는 슬롯은 36개다. `candidate-drafts.json`에 현재 슬롯의 의미 역할·dimension·property prefix를 참고 정보로 붙였다. 이것은 역할 적합 판정이나 native owner selector·허용 효과가 아니다. 특히 다음을 구별한다.

- `visible_text`: 실제 글자·수치의 판독. 그 글이 참이라는 의미는 별도다.
- `image_detail`: 사진/화면 안의 도상. 실제 인물을 자동 추가하지 않는다.
- `object_structure` / `contact_point`: 프레임·소켓·체인·빗장의 실제 연결과 양 끝.
- `subject_count` / `relational_action`: 별도 몸·접지·손동작. 같은 얼굴을 같은 자아로 확정하지 않는다.
- `reflection_logic`: 실물과 반사의 관계. 거울이 아닌 매체나 정신질환과 자동 동치 금지.
- `surreal_concept` / `space_condition`: 요청이 허용한 공간 변화. 파일 손상·광학 효과와 구별.
- `narrative_clue` / `situation_context`: 단서와 문맥. 단일 프레임에서 비가시 사실의 승인 경로로 쓰지 않는다.
- `format` / `narrative_phase`: F01 같은 명시 다중 패널은 단일 프레임의 시간 증거로 평가하지 않는다.

각 후보에서 새로 생기거나 변하는 대상·개수·몸 부위·문자·재질·방향·접점·반사·피해 표현을 모두 효과 심사에 넣는다. 예를 들어 D08은 화면·짧은 문자·두 성인·거리·손 자세를 추가하므로 단순 `visible_text` 효과 하나로 축소할 수 없다. 기존 조건/승인과 독립 core에 부딪치면 후보 전체를 거절하거나 새로 저술해야 한다.

원문 양성 텍스트에는 온전한 가시 제안만 넣는다. 비가시 주장 한계·거절 예·민감한 사건명·출처 작품명이 긍정 검색 텍스트에 섞여 일반 요청에 노출되지 않게 경로를 나눈다. 별칭으로 `철학적 좀비=무표정`, `메타픽션=글리치`, `호감도=동의` 같은 동치를 만들지 않는다.

넓은 장르명과 요청별 시각 선택은 분리한다. 연구 카드가 native 사실, 하드 프로파일, requester owner, 성적/폭력적 의미를 자동 활성화하면 안 된다. 엔진 수정은 자료 저술과 기존 계약으로 해결할 수 없는 구체적 실패가 확인됐을 때만 별도 문제로 설계한다.

## 4. 격리된 소스와 인덱스

현재 작업 소스 search layout은 로컬 `embeddinggemma2-local`, `google/embeddinggemma-2`, 768차원, `embeddinggemma2-retrieval/v1`을 선언했다. 이는 해당 manifest의 설정이며 이번에 임베딩 추론을 실행하거나 설치 세대와의 동등성을 검증했다는 뜻이 아니다.

구현은 별도 staging assets에서 진행한다. 기존 원문·모델 revision·패키지 hash·recipe·정규화·차원이 모두 일치하는 벡터만 재사용하고, 바뀐 텍스트는 같은 공간에서 새로 계산한다. 원격 모델로 자동 우회하지 않는다. 현재 CLI에는 `--assets`, `--backend`, `--output-assets`, `--verify`, `--publish`, `--runtime-store`가 있으므로 다음과 같이 source와 output을 분리할 수 있다. 아래 경로는 실행자가 정한 절대 staging 경로로 대체해야 하는 예시다.

```sh
python3 skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --assets /ABS/STAGING/SOURCE_ASSETS \
  --backend embeddinggemma2-local \
  --output-assets /ABS/STAGING/BUILT_ASSETS

python3 skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --assets /ABS/STAGING/BUILT_ASSETS --verify
```

`--verify`의 코드 경로와 출력 변형 여부는 실행 시 다시 확인한다. 빌드 성공을 검증 성공으로, 검증 성공을 게시로 해석하지 않는다. 이 단계에는 `--publish`를 넣지 않는다. 새 인덱스에서 source ID/text hash, duplicate ownership, CID/RID·branch, binding, vector/posting 범위, payload/routing closure, 누락·오류·source drift를 확인한다.

## 5. 검색·노출 평가

[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)는 개발 64개·경계 32개·일반 16개·비가시 12개, 총 124사례/248개 한영 질의다. 모두 `NOT_RUN`이며 독립 holdout이 아니다. 가시 카드와 함께 만든 개발 사례라는 한계를 유지한다.

원문을 그대로 반복한 개발 질의뿐 아니라 구현 착수 전에 독립적인 자연 요청을 별도로 확보한다. 실제 정답은 연구 카드 ID가 아니라 심사한 **CID/RID + 허용 슬롯 + owner/조건 적합성 + 완전 원문**이다. 여러 정답이 있을 수 있고 조건상 불가능한 소스를 정답으로 억지 등록하지 않는다.

각 run에서 요청 원문 bytes, 독립 core, controls, 슬롯 계획·owner, source/index SHA, 설치 generation, language, query scope, seed·sampling recipe를 고정한다. 현재 코드의 creativity별 창/표본 수를 다시 확인하고 frozen receipts와 연결한다. replay/resume은 검색·표본을 다시 만들지 않는다.

슬롯별 검색과 주제/기본 프롬프트에 대한 전체 장면 검색은 독립 경로를 유지한다. 두 결과를 임의로 합쳐 순위를 다시 만들지 않는다. 각 경로에서 다음을 따로 측정한다.

| 지표 | 목적 |
|---|---|
| source 존재와 eligibility | corpus 부재와 조건 부적합을 구별 |
| top8에 완전 호환 소스 포함 | 실제 검색의 발견 가능성 |
| sampled exposure | 정답이 순위에 있어도 실제 사용자에게 보였는지 |
| 선택·채택과 literal prompt evidence | 노출이 실제 장면에 반영됐는지 |
| 잘못된 자동 채택 | broad label·숫자·장신구가 권리/동의/사건으로 바뀌는지 |
| 한영 차이·오탐·누락 | 번역·질의·pool·랭크·조건 중 원인 분리 |

핵심 12개 관계군은 각 언어 모두 실제 top8에 최소 한 개 완전 호환 소스가 있어야 한다. 나머지 개발 사례는 각 언어 90% 이상의 포함률을 제안 목표로 두되, 실패를 사후 제외하거나 문턱을 낮추지 않는다. 안전한 일반 요청에 무단 사건을 **채택**한 사례는 0이어야 한다. 잡음 후보가 검색되는 것과 실제 의미 채택은 별도로 보고한다.

풀이에 정답이 없으면 순위 조정으로 해결할 수 없다. 같은 단어가 top8에 있다고 의미 적합으로 세지 않는다. 새 후보가 한 번도 노출·채택되지 않았다면 이미지 개선의 원인으로 주장하지 않는다.

## 6. 픽셀 비교·채택·복구

첫 비교는 [PIXEL-PLAN.md](PIXEL-PLAN.md)의 핵심 12개 × 3 arms = 36개 결과를 대상으로 한다. source/slot/graph 통과와 원본 픽셀의 완전성은 다르다. 비교 중 결과가 나쁘다고 의미를 바꾸거나 요구를 빼고 원래 사례 통과로 표시하지 않는다.

보고 단위는 `검색 성공`, `원문 채택`, `구조 감사`, `생성 성공`, `개별 관계 visible`, `전체 사례 PASS`, `표현 선호`, `사용자 수용`으로 나눈다. 차단되어 반환 픽셀이 없으면 시각 품질의 실패/합격으로 채점하지 않는다. 명확한 자원/정책/환경 오류는 유효하지 않은 시도로 남긴다.

위 기준을 통과한 범위만 snapshot publication과 설치 대상으로 삼는다. 기존 활성 세대와 source/index 해시를 보존하고 이전 pointer로 복구한 뒤 읽기 전용 검증을 할 수 있어야 한다. 설치·평가·커밋·푸시 상태를 각각 기록한다. 사용자가 후속 구현·커밋을 요청하면 그 범위만 allowlist로 stage하며 관련 없는 dirty 파일을 포함하지 않는다.

검증 미달 관계는 해당 범위를 HOLD로 남긴다. 다른 카드의 합격 수로 실패를 덮지 않는다. 연구 완료는 이 실행 목표의 달성을 뜻하지 않는다.
