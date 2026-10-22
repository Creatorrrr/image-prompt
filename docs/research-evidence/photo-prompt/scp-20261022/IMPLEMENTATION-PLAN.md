# SCP 조사 결과 반영 계획

2026-10-22. 이 문서의 구현·검색·이미지·설치는 **미실행**이다. 연구 산출물은 `assets`에 등록하지 않았다.

## 목표와 완료 기준

목표는 ‘SCP 용어가 더 많이 검색된다’가 아니라 **요청이 실제로 원하는 경계·매체·신체·공간 관계에 적합한 완전 후보가 노출되고, 선택 후 원래 의미를 훼손하지 않는 것**이다. 다음 결과를 따로 증명한다.

| 결과 | 완료 증거 |
|---|---|
| 자료 채택 | 채택한 각 카드의 reuse/refine/new/context/defer 결정, 실제 CID/RID, 원전·저작자·판본, 전체 source diff |
| 의미·소유 정확성 | 양쪽 끝점·운반체·조건·효과·완전 의무·역할의 직접 검토. 문맥과 시각 사실의 혼합 0건 |
| source/index 무결성 | 별도 staging에서 소스·모델 공간·벡터·문서/통계·manifest closure 검증 |
| 실제 검색/노출 | 고정된 한영 질의의 lane·실제 CID/RID·순위·표본·receipt 및 eligible/fit 판단 |
| 픽셀의 관계 구현 | 요청한 관계의 전체 연결과 가시성. partial/unobservable은 완전 합격이 아님 |
| 표현 품질 | 장면의 상황·시선·위계·감정적 설득력을 기술적 충실도와 별도로 평가 |
| 설치·활성화 | 검증된 소스/인덱스를 봉인한 설치 세대와 실제 선택 포인터, 롤백 경로 |

각 단계의 통과가 뒤 단계의 성공을 대신하지 않는다. 전체 카드 수를 구현 목표나 자동 승인 할당량으로 쓰지 않는다.

## 0. 재기준화와 격리

현재 체크아웃에는 다수의 기존 dirty/untracked 작업이 있다. `BASELINE.json`은 시작 HEAD와 추적 파일 3,634개의 해시를 남겼다. 조사 중 다른 작업에서 후보 수가 19,006에서 19,078로 바뀌었고 일부 소스·검색 파일도 움직였다. 이 연구의 옛 스냅샷을 운영 권위로 사용하지 않는다.

구현 시작 시 다음을 새로 고정한다.

1. HEAD, dirty/untracked 상태, source manifest의 전체 모듈 바이트/해시, catalog·search space·선택 설치 세대·CURRENT.
2. 기존 연구와 이번 연구에서 실제 구현에 필요한 변경의 목록. 현재 dirty 내용을 stash/reset/restore하여 격리하지 않는다.
3. 검토 가능한 별도 작업 공간과 `feature/` 브랜치. 사용자가 특별히 같은 작업 공간을 지정하면 그 범위에 맞춘다.
4. 비교할 기존 설치 세대와 staging 경로. 새 인덱스의 출력이 원본 assets를 향하지 않게 한다.

읽기 전용 점검은 다음 진입점이다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

이번에 dependencies/installed recorder 확인은 pass였고 NumPy 2.5.4, v10 신규 기록 지원을 확인했다. 이는 이번 SCP 자료를 설치하거나 검색한 증거가 아니다. 후속 standalone 유지보수에는 출력에 있는 실제 `runtime_python`을 사용하고, 실제 변경 전 다시 점검한다.

## 1. 채택 결정과 작업 묶음

103개 카드는 P0 34개, P1 39개, P2 30개다. 우선순위는 카드 JSON에 명시했다.

| 순서 | 자료 | 반영 방향 |
|---|---|---|
| P0-a | I01/I08/T01 및 기존 접합 이웃 | source/선택 branch/조건/효과가 맞는 기존 CID를 먼저 재사용. 원문을 줄여 연구 문장으로 교체하지 않음 |
| P0-b | I02/I03/I04/I11, M01/M04, C01/C02/C05, R01/R02/R03, T04, F02/F04, B01 | 장비·용기·경계·두 끝점의 부족한 관계만 신규/보완 저술 |
| P0-c | I10/I13/I14, C04/C06, R09, F05/F07, K05, B06/B07, E05 및 기타 P0 문맥 | 분류·정보·동의·교리·비공개 절차의 오인 방지. 기존 context/diagnostic 재사용 우선 |
| P0-d | K03, E02/E08 | 웹 공동체 의미, 권리·판본 경계와 선택된 번호 개체의 가시 속성을 분리 |
| P1 | 나머지 현재 형태·매개체·사회적 배치 | 주된 P0 공백을 해결한 뒤 장면 다양성과 혼동 경계를 확장 |
| P2 | 복잡한 조직·종족·한국어 문맥·재앙·서사/개체 판본 | 필요한 실제 요청과 원전이 있을 때 진행. 추가 근거가 없으면 context/defer 유지 |

각 카드는 반드시 다음 중 하나를 결정한다.

- `reuse`: 기존 전체 소스와 선택 RID/역할이 같은 실현을 완전히 공급한다. 기존 CID와 원본 바이트 의미를 보존한다.
- `refine`: 같은 의미의 번역·질의 지원·명시성이 부족하다. 추가되는 사실과 단순 발견용 표현의 diff를 분리한다.
- `new`: 필요한 독립 관계를 기존 complete source가 공급하지 않는다. 가장 가까운 CID와 왜 대체할 수 없는지 적는다.
- `context`: 인과·역사·능력·정체·동의·교리 등의 선언/해석으로 남긴다. 양성 시각 속성으로 승격하지 않는다.
- `defer`: 판본·정의·이미지 권리·저작자·관계의 근거가 부족하다. 재개에 필요한 원전 또는 판단을 명시한다.

`existing-source-mapping.json`의 15개 이웃을 시작점으로 쓴다. 이것만으로 일반 표본·기계·보호복 전 영역의 비교가 끝난 것은 아니다. 다른 연구의 동시 반영분까지 다시 읽어 중복 CID와 의미 확장을 막는다.

## 2. 반영 위치와 데이터 저술

아래는 예상 경로이며 이번에는 만들지 않았다.

| 경로 | 역할 |
|---|---|
| `assets/photo_scp_semantics_20261022.json` | 원전·판본·카드·채택 결정을 추적하는 보조 registry. native source 의미의 두 번째 권위가 아님 |
| `assets/photo_candidate_scp_20261022.json` | 승인한 신규 V3 후보만. 연구 JSON의 일괄 import 금지 |
| `assets/photo_candidate_scp_bindings_20261022.json` | 149-slot catalog의 실제 의미와 조건을 검토한 역할 연결만 |
| `assets/photo_candidate_corpus_manifest.json` | 검토한 모듈의 명시적 등록 |
| 기존 CID의 실제 owner 파일 | refine으로 확정한 정확한 레코드만. shard 전체 재작성 금지 |
| `references/scp-visual-semantics.md` | 유지보수용 판본·혼동·권리 가이드. 일반 요청의 precore 재료가 아님 |
| 영향받은 테스트/fixture | 해당 의미·소유·조건·의무·락·오탐의 회귀 |
| 외부 provenance/라이선스 sidecar | 현 schema가 담지 못하는 원전 저작자·파생 설명의 추적. 임의 필드를 native payload에 넣지 않음 |

저술할 양성 소스에는 선택된 실현의 한영 문장, 각 owner와 부위, 연결의 양끝, 조건, intrinsic effects, 완전한 positive source-unit/조건부 의무를 명시한다. 연구의 `claim_limit`, 오인 예, 불가시 설명을 positive embedding text에 섞지 않는다. `source_ids`나 source 이름만으로 새 시각 fact의 권위를 만들지 않는다.

`candidate-drafts.json`은 runtime schema와 호환되지 않는다. `DR-*`는 실제 CID/RID가 아니며 native approval·receipt·source-unit disposition이 없다. 초안의 effects는 `UNKNOWN_PENDING_FULL_SOURCE_REVIEW`다. 이를 빈 effects로 바꿔 권한 검사를 통과시키지 않는다.

한영 검토는 명사 대응에 그치지 않는다. ‘같은 팔’, ‘각각 다른 몸’, ‘두 케이블 모두의 양끝’, ‘창 안의 실물’, ‘화면 안의 영상’, ‘용기 안쪽 액체’, ‘완전히 가린 면’을 양 언어에 유지한다. E06처럼 일부 구성만 저술한 번호 개체는 전체 원문 충실도로 등록하지 않는다.

## 3. 역할·효과·의무를 검토할 핵심 사례

| 사례 | 필요한 검토 |
|---|---|
| I03 장갑 포트 | 두 장갑은 도구다. 상자-포트의 기계 접합을 biological anatomy로 승인하지 않음 |
| M01 방호복 | 후드/커프 접속은 garment 구조이며 실제 차폐 효능은 별도 |
| C02 차폐 | 머리 방향과 가려진 시각 대상의 실제 노출을 혼동하지 않음 |
| R01 SRA | `reality_anchor` 슬롯 이름과 장치 이름을 연결하지 않음. prop/object 구조로 저술하고 기능은 context |
| T04 ARI | 장치 사진과 장치로 취득한 시야를 분기. 화면 오라를 인물 피부 발광으로 투사하지 않음 |
| G07 로봇 | 금속 관절은 object_structure. 생물 몸의 부위라는 근거 없이 anatomical_connection으로 연결하지 않음 |
| F02 보철 | 동일 생물 주체의 피부-커프-보철을 검토하고 독립 장신구와 구별 |
| F03 네트워크 | 두 인물/장치/케이블을 다른 owner로 보존하며 모든 접점을 검토. 연결이 집단 정신의 증거는 아님 |
| B01 조직 다리 | 두 독립 몸과 양쪽 연속 접점. 한쪽 가림·겹침은 완전 PASS 금지 |
| K03 골목길 | 이름 해석은 웹 공동체. 다른 요청에서 문맥상 실제 골목을 뜻하면 그 사용자 의미를 우선 |
| K08/N02 화면 | 실물·화면·화면 속 도상을 구별하고 자동 reflection/image_detail 역할 부여 금지 |
| E02/E08 | 원전 재질/얼굴/복장과 권리/무한성/시간 기능을 별도 검토 |

요청별 owner는 실제 독립 core의 해당 대상을 바인딩한다. 연구 카드의 owner 키가 frozen requester owner가 되는 것은 아니다. broad label·alias·metadata·role proposal이 인물·부위·개수·성적 문맥·행동을 암묵 생성하지 못하게 한다. 기존 negative 소유·승인 경로와 requester lock도 유지한다.

검증은 변경한 계약부터 진행한다. 현재 관련 dictionary validator와 semantic-boundary/source-context/primary-proof/validation-context/sampling 테스트를 구현 시 다시 확인한다. 자료 저술로 해결되는 공백에 엔진 변경을 추가하지 않는다. 조건/효과/원문 의무가 달라지면 이전 proof·receipt를 재사용하지 않는다.

## 4. 별도 인덱스와 source closure

조사 시 작업 소스의 search manifest는 `embeddinggemma2-local / google/embeddinggemma-2`, 768차원, `embeddinggemma2-retrieval/v1`을 선언했다. 실제 설치된 sealed H-F2와 작업 소스의 manifest를 같은 것으로 가정하지 않는다.

새 source/index는 별도 staging assets에서만 만든다. 모델 revision·package hash·recipe·공간·벡터 무결성과 정확한 source ID/text hash가 모두 맞는 기존 벡터만 재사용한다. 바뀐 문장은 그 공간에서 재계산하고 누락/불명 오류를 기록한다. 원격 모델로 자동 우회하지 않는다. `--verify` 성공과 source/current pointer activation은 별도다.

후속 실행의 개념적 순서는 `staged source 검증 → staged build → 독립 verify → source closure 재대조 → 검색 qualification`이다. 빌더가 manifest를 쓸 수 있으므로 원본 assets를 출력으로 사용하지 않는다. 모듈의 중복 소유, bindings, selected branches, source-unit, posting/vector 범위, 문서 수/통계, payload/routing closure, source drift를 함께 검증한다.

## 5. 실제 검색·노출 평가

`EVALUATION-CASES.tsv`는 78사례/156개 한영 입력이다. 38개 양성 질의는 카드와 함께 저술했으므로 개발 세트다. 경계 20개는 잘못된 동치 판단을 거절하는 engineering control이다. 자연어 검색 성능의 독립 holdout으로 부르지 않는다.

구현에 착수하기 전에 현재 카드에서 유도하지 않은 별도 자연 요청 24개를 고정한다. 사용할 독립 요청이 없으면 `independent_holdout: NOT_AVAILABLE`로 보고 개발 세트의 범위를 넘는 일반화 주장을 보류한다.

각 arm에서 requester 의미·핵심 장면·controls·슬롯/소유·질의 bytes·언어·모델 공간·source/index SHA·설치 세대를 고정한다. 슬롯별 독립 검색과 topic/baseline의 독립 전체 장면 검색을 유지하고, 결과를 합쳐 순위를 바꾸지 않는다. 현재 코드의 creativity별 창/표본 규칙을 실행 시 확인하고 seed·실제 노출·receipt를 저장한다. replay/resume으로 새 검색이나 재표본을 만들지 않는다.

정답은 연구 카드 ID가 아니라 **검토한 실제 CID/RID/허용 역할과 문맥**이다. 다음 목표는 실행 전에 고정할 제안이다.

- 핵심 8개 관계군 I01/I02/I03/I08/M01/R01/F02/B01: 양 언어에서 호환하는 완전 소스가 최소 1개 실제 top8에 포함되어야 한다. 별도의 sampled exposure도 기록한다.
- 나머지 양성 개발 세트: 각 언어에서 호환 source top8 포함률 90% 이상을 목표로 한다. 사전 조건 때문에 정답이 불가능한 사례는 사후 제외하지 않고 원인과 HOLD를 남긴다.
- requester lock/owner/선택 의무 위반, 비가시 효과의 자동 확정, 일반 대조에서 무단 SCP 정체·성적/폭력적 사건을 **채택**한 사례는 0건이어야 한다.
- top8의 잡음률, 양 언어 차이, 미노출 원인을 별도로 표로 낸다. 단순 태그·이름·같은 실루엣을 적합으로 세지 않는다.

어떤 failure도 다른 카드의 합격 수로 덮지 않는다. pool에 없는 정답은 순위 조정으로 해결할 수 없고, 노출이 0인 새 자료를 이미지 개선의 원인으로 주장할 수 없다.

## 6. 픽셀 비교와 표현 평가

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 12사례 × 3 arm = 최초 36장 계획이다. 현재는 NOT_RUN이며 이미지 호출을 수행하지 않았다. 후속 구현/평가 범위가 정해지면 그 범위에서 진행한다.

같은 독립 core를 바탕으로 A 기본 장면, B 기존 후보 자료, C 검토한 보강 자료를 비교한다. 하나의 case에서 새 자료가 노출·선택되었는지를 먼저 기록한다. 사용하지 않은 새 자료의 효과를 주장하지 않는다. seed를 통제할 수 없는 provider라면 그 한계를 기록하고 완전히 일치한 조건이라고 부르지 않는다.

필수 관계는 전체 owner·접점·경계가 같은 프레임에서 읽혀야 한다. 프롬프트 감사 PASS는 픽셀 증거가 아니다. 차단되어 반환 픽셀이 없으면 `BLOCKED_UNSCORED`, 가림은 `unobservable`, 일부 충족은 `partial`로 남긴다. 통과한 한 접점을 전체 장면 합격으로 올리지 않는다. 추가 반복은 실제 실패·불확실성에 따라 범위를 정한다.

## 7. 설치·마감

소스/의무/인덱스/검색 qualification을 마친 자료만 현재 유지보수 절차에 따라 봉인한다. 설치 전 검증, 비활성 설치, 설치 세대 재검증, 활성화와 롤백 경로 확보를 구분한다. old CURRENT·sealed generation·과거 run/receipt를 보존한다.

정확한 변경 파일만 allowlist로 stage하고, 캐시 diff·보호 파일 해시·요구 검증을 확인한다. 커밋·푸시·PR·설치·활성화·이미지 승인·사용자 판단을 각각 보고한다. 연구·개발 수치가 사용자 수용을 대신하지 않는다.

이 계획을 따르는 구현은 현재 baseline/포인터/등록 상태를 다시 확인하는 것에서 시작한다. **이번 완료 상태는 조사와 계획, 연구 자료 구조 검사까지다.**
