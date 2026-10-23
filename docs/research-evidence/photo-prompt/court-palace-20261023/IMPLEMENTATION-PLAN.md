# 리서치 결과 반영 계획

2026-10-23. 아래는 후속 구현 계획이며 이번에는 연구 폴더만 작성했다. 연구 초안은 runtime source로 import할 수 없다.

## 1. 목표와 완료 기준

요청된 시대·지역·복식·관계가 후보의 전체 의미와 일치하고, 검색에서 그 대안을 발견할 수 있으며, 선택했을 때 주인·부착·가림·접촉이 프롬프트와 실제 이미지에 유지되도록 한다. 장르 단어 하나로 왕관·궁녀·성적 관계·폭력·특정 미학을 강제하지 않는다.

전체 종료 조건은 `출처 검토 → canonical source/조건/효과/binding 검토 → native 의미 자격 → 호환 인덱스 → 실제 검색 → 프롬프트 전달 → 실제 픽셀 → 사용자 평가`다. 각 단계는 별도 상태를 기록한다. 코드 테스트 통과나 후보 노출이 다음 단계의 통과를 대신하지 않는다. 역사적 조합의 적합성도 이미지의 모양 충족과 별도로 기록한다.

## 2. 우선순위와 작업 단위

| 차수 | 작업 | 현재 연구 입력 | 완료 기준 |
|---|---|---|---|
| P0-a | 한영·embedding 과장 보정 | 당의 거들지·빈 왕좌 CID | 전체 뜻 일치; 기존 조건/효과/ID 보호; 해석과 외형 분리 |
| P0-b | 기존 구조 재사용 | 당의 옆트임·스토머커·기모노·마루·궁중 주거 | 중복 신규 등록 없이 필요한 구조만 연결; 전체 기존 의미 보존 |
| P0-c | 혼동이 큰 역사형 구조 | B01/B04/B05, D01/D02, E01, F02-F06 | 시기·지역·일습/부품·전후면 확인; 단독·비교 검색 구분 |
| P0-d | 관계 장면 | A08/A09, G01, I02/I04/I09 | 손·천·물건·문턱·좌석의 주인과 연속 접점 유지 |
| P0-e | 문맥 오판 방지 | K01-K15 | 혈통·동의·범죄·독성·반복·소리를 positive 외형 사실로 출력하지 않음 |
| P1-a | 추가 고증 40개 카드 | B06-B12, C03-C05, D05/D06, 남성복·부속 등 | 각 단독 물건의 유물·도판·시대·명칭 출처 확보; 복합 카드는 분할 |
| P1-b | 궁중 노동·식사·무용 | I06-I08, S31/S32 | 실제 도구·하중·작업·연행자별 의복 검토; static/sequence 구분 |
| P1-c | 세부 보석·머리·소재 | J03/J06, G02/F09, 각 지역 머리 | 부착점·시대·표면/내부 증거 보완; 재료 분석과 시각 추정 구분 |
| P2 | 원 대화의 미연결 세부 정의 | keyword-routes의 exact-definition-deferred | 필요도가 높은 원 항목부터 원전 확보; 확인되지 않은 내용은 유지하되 등록 보류 |

73개 초안을 모두 신규 CID로 만드는 목표는 없다. 재사용·보정·분할·보류를 마친 뒤 실제 운영 candidate/binding 수를 확정한다. 시대 혼합 판타지의 기존 대안을 역사형으로 덮어쓰지 않는다.

## 3. 단계 A — 최신 기준과 변경 경계 고정

입력: BASELINE.json, corpus-snapshot.json, existing-source-mapping.json, 원 대화 rows, 현재 HEAD·manifest·149-slot catalog. 구현 시작 시 현재 상태를 다시 읽어 별도의 integration-evidence 폴더에 기록한다. 연구 snapshot을 새 상태로 덮어쓰지 않는다.

이번 시작 시 tracked 상태는 수정 27개·삭제 2,454개가 있었다. 이 파일들을 복구하거나 이번 반영에 섞지 않는다. 파일명·record ID allowlist와 보호 hash를 확보한다. 현재 작업 트리·적합한 기존 worktree를 확인하고, 충돌 우려가 크면 별도 managed worktree에 허용된 파일/레코드만 구성한다. 게시가 요청되기 전 커밋/푸시는 하지 않는다.

완료 증거: 기준 SHA·기존 dirty 상태·후보/binding hash·allowlist·보호 대상·현재 source 형식. 전체 원본을 읽지 않고 lexical hit만으로 신규/부재 판단을 내리지 않는다.

## 4. 단계 B — 고증·번역·카드 분할

1. 각 등록 예정 항목에 단독 유물 페이지/의궤 도판/복식사 연구를 추가한다. 박물관 설명·전시 재현·현대 공연·상업 복원·당대 기록을 출처 유형으로 구별한다.
2. 원삼/활옷, 무지기/대슘, 각 관모, 명 봉관/청 머리, 폴로네즈/맨투아/랑글레즈, 자마/앙가르카 등 비교 카드는 단독 realization으로 분리한다. 전시 비교 장면을 유지하려면 별도의 완전 장면 대안으로 저술한다.
3. 각 표본의 지역·시대·착용자·의식·관계된 부속을 고정한다. 통칭/이칭이 겹치는 용어는 문헌별 범위를 보존한다. 오래된 명칭의 일률적 재번역을 피한다.
4. KO/EN에서 같은 명사·수량·위치·여밈·부착점·negation·행위가 유지되는지 대조한다. 영문 전체 뜻을 한글의 broad 표제로 덮지 않는다.
5. 모든 인물의 손·팔·발·머리와 모든 물건의 주인을 표시한다. 서로 다른 사람의 손이 바뀌거나 실제 몸과 그림 속 몸이 합쳐지지 않게 한다.

완료 증거: 각 후보의 출처 지원 주장·저술한 장면 주장·추가 검토 상태·그림/현실 층·정확한 owner graph. 출처가 인접 맥락만 지지하는 경우 등록 보류를 해제하지 않는다.

## 5. 단계 C — 실제 파일과 권위 범위

아래 신규 파일은 모두 제안 경로다. 기준은 `/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/`다.

| 경로 | 반영 내용 | 권위 |
|---|---|---|
| `assets/photo_court_palace_semantics_20261023.json` | 검토한 카드·source·혼동 경계·원 항목 경로·기존 CID 판단 | 유지보수 sidecar; 자동 profile 권위 없음 |
| `assets/photo_candidate_court_palace_20261023.json` | 완전 시각 대안, 별도로 분리한 context/diagnostic | canonical candidate의 단일 저술 원본 |
| `assets/photo_candidate_court_palace_bindings_20261023.json` | 검토한 CID→149개 기존 slot 중 적합 role와 조건 | 역할 적합성만; 의미/effect 복제 금지 |
| `assets/photo_candidate_corpus_manifest.json` | candidate/binding 모듈 등록 | 운영 source 진입점 |
| `references/court-palace-semantics.md` | 시대·역할·원전 경계와 실제 검증 상태 | 사람용 유지보수 설명 |
| `references/maintenance.md` | 확장 참조와 검증 상태 링크 | 안내 |
| 기존 `_002/_003/_006/_007/_010/_014` 중 허용 CID | 검토된 번역/검색 설명 보정 | 다른 레코드 및 dirty 변화 보호 |

인덱스 파일은 source와 자격이 확정된 뒤 현재 저장소의 빌더로 생성한다. 연구 JSON을 source manifest에 그대로 연결하지 않는다. 새 sampler·새 slot·새 pre-core 키워드 강제·장르 profile 자동 활성화는 이번 보강 목표에 필요하지 않다.

## 6. 단계 D — 역할·효과·조건과 native 의미 자격

현재 149개 slot 중 해당 범위를 우선 검토한다.

| 요소 | 검토할 role | 효과 범위의 유의점 |
|---|---|---|
| 전체 포즈/손 모양 | body_pose, hand_pose | pose; 접촉·지지는 별도 관계 검토 |
| 옷의 절개/주름/트임 | garment_detail | appearance; 사람 신체의 구조 변화로 옮기지 않음 |
| 시대·의식의 착장 문맥 | attire_context | appearance/role; 실제 품계·제도 사실 자동 확정 금지 |
| 머리·몸에 단 장식 | wearable_accessory | 착용자·부착 위치 필수 |
| 단독 전시 물건 | object_structure, prop | 형상과 장면 역할 분리; 손의 주인 추가 금지 |
| 손·물건·바닥의 배치 | prop_placement, composition | 정본 의미와 이미 고정된 수량/접촉 보존 |
| 문턱·대기·통과 | location, proxemics, composition | setting/relationship; intimacy나 품계 추론 금지 |
| 소재·반사 | surface_material, texture | material 외형; 재료 분석·원산지 판정과 분리 |
| 의례 이름·사건 단서 | occasion_context, narrative_clue | 사건·시간·제도 사실은 외형만으로 입증 못 함 |

effect는 role 이름이나 tags에서 자동 추출하지 않는다. 옆으로 넓은 옷의 실루엣과 신체 비율은 carrier가 다르다. `silhouette_proportion`의 body_geometry를 사용하려면 옷/몸의 소유와 허용된 property를 분명하게 검토한다. 빈 effects를 이유로 어떤 장면 변경도 자유롭다고 보지 않는다.

전시된 당의의 garment_detail 적합성과 기존 human 전용 binding의 거부 영역은 별도 검토한다. 새로운 전시 role를 만들거나 조건을 완화할 경우 기존 거부의 이유와 회귀 영향을 확인한다. 기존 조건을 조용히 삭제하지 않는다.

native 자격은 CID·정본 hash·현재 role/effect closure에 묶어 기록한다. 이전 연구 카드의 gate나 기존 다른 세대 자격을 새 의미에 재사용하지 않는다. 현재 자격 절차/CLI를 실행 전에 확인하고, 종료 코드와 저장된 판정을 읽는다.

## 7. 단계 E — 격리 인덱스와 실제 검색

1. 현재 source union을 기준으로 호환 recipe와 layout을 확인한다. 다른 v1/v2 vector를 이름만 바꿔 재사용하지 않는다.
2. source·binding·정본 hash의 closure를 검증한다. 새 인덱스는 별도 출력 위치에 만들고 검증 전 CURRENT/installed pointer를 바꾸지 않는다.
3. slot별 검색과 whole-scene 검색을 모두 유지한다. 동일한 snapshot·controls·core에서 baseline과 보강본을 비교한다.
4. evaluation-cases.json의 개발 73개/문맥 15개 한영 질의, 별도 CONFUSION-CASES.tsv 24쌍 48개 한영 질의를 사용한다. 합계 136개 case/272개 언어별 query. 실제 운영 slot에 맞지 않는 query는 실행 전에 명시적으로 수정하고 변경 이력을 남긴다.
5. 직접 구별 항목은 평가자가 CID 동등 집합과 허용 대안을 먼저 판정한 뒤 top8 관련 후보·off-era 후보·owner 오류·문맥 positive 누출을 평가한다. 자기 카드의 문장을 그대로 검색한 성적만으로 일반 사용성 주장을 하지 않는다. 원 용어 단독·자연스러운 묘사·대조 부정·장르만 있는 입력도 포함한다.
6. 실패가 pool 진입인지 ranking인지, source 의미인지 binding 조건인지, 언어 불일치인지 분리한다. 반환되지 않은 후보는 reranking만으로 고칠 수 없다.

제안된 채택 gate: P0 필수 구조는 각 언어/검색 lane의 top8에 검토된 적합 후보가 최소 1개 있어야 한다. 잘못된 시대 후보가 결과에 있다는 사실과 그것을 정답으로 선택/강제한 오류는 구별하여 측정한다. 문맥 항목의 비가시 주장을 positive 사실로 강제하거나 core 잠금을 침범하는 경우는 1건도 허용하지 않는다. 이 임계값은 실행 전 고정하며 현재 측정 결과가 아니다.

## 8. 단계 F — 프롬프트와 픽셀 평가

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 P0 여덟 군을 실행한다. 최초 검증 규모는 군별 baseline 1장+보강 1장, 16장이다. 이것은 통계적 우월성 실험이 아니라 결함 검출용 최소 비교다. 실패한 관계만 구성/가시성을 수정하여 별도 버전으로 재시험한다. 도구 결과의 moderation block은 생성물 없음으로 기록하고 픽셀 점수는 BLOCKED_UNSCORED다.

각 팔은 같은 requester core·잠금·참조 범위·controls·출력 조건을 보존한다. 기존 후보·새 후보의 실제 노출·선택·거절·literal prompt 문구·이미지 파일·gate 판정을 따로 기록한다. requester가 특정하지 않은 장면은 목적·물건·인물 관계·반응의 전체 효과를 비교하여 더 적절한 대안을 선택한다. 복잡한 장식의 수가 품질을 대신하지 않는다.

종료 조건: 요구된 모든 관계가 같은 이미지에서 관찰 가능해야 case PASS. 보이지 않음은 UNOBSERVABLE_NOT_PASS, 일부만 됨은 partial_is_fail. 역사 고증·픽셀·사용자 수용의 세 판정은 분리한다. 사용자 평가는 마지막까지 미확인으로 남길 수 있으며 자동 승인하지 않는다.

## 9. 단계 G — 활성화·게시·롤백

검토된 source와 호환 인덱스의 hash, native 및 실제 검색 증거를 확보한 뒤에만 설치 활성화를 검토한다. 변경 전후 pointer와 manifest·source·index 세대와 롤백 경로를 보존한다. 이미지 검증 상태가 미실행이면 그 한계를 명시한다.

사용자가 커밋/푸시를 요청하면 게시 allowlist를 별도로 확정한다. 새 연구 폴더·허용 source 레코드·허용 binding·생성 인덱스 closure만 포함한다. 기존 dirty 파일은 blob/hash로 보호한다. 현재 원격과의 병합이 필요하면 양쪽 저술 source를 보존하고 정확한 합본에서 인덱스를 재생성한다. local/tracking/live remote SHA가 일치한 후에만 전용 임시 worktree 정리를 검토한다.

## 10. 작업 종료 상태표

이번 완료: 조사·source snapshot·88개 카드·73개 초안·원 키워드 경로·평가 및 반영 계획·연구 구조 검증.

후속 미실행: 원전 추가 고증·운영 CID/binding 반영·native 자격·index/embedding·검색·설치 활성화·프롬프트 실행·이미지 생성·픽셀 평가·사용자 수용·커밋/푸시. 이번 연구가 완료되었다고 후속 단계도 완료된 것으로 표시하지 않는다.
