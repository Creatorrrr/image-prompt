# 캠퍼스물 연구 반영 계획

## 목표와 완료의 기준

목표는 캠퍼스 장르의 전형을 자동 삽입하는 것이 아니라, 요청자가 고른 대학생활·전공·복식·포즈를 **구체적인 구조와 관계로 선택할 수 있게 하는 것**이다. 이번 단계는 연구 패키지와 반영 설계까지 완료한다. 아래 source/검색/설치/이미지/발행 단계는 후속 구현 계획이며 실행 결과가 아니다.

용어 행 356개 → 카드 124개 → 초안 101개라는 숫자를 신규 운영 후보 수나 품질 성공률로 해석하지 않는다. 여러 카드가 같은 기존 CID를 재사용할 수 있고 한 카드의 묶인 용어가 여러 구조로 분할되어야 할 수도 있다. 최종 신규 CID 수는 심사 후 결정한다.

## P0: 신원·관계 추론과 가시 관계 손실부터 막는다

1. **범위와 현재 상태 재기준화.** 실제 구현 직전 HEAD·manifest·모듈 해시·slot catalog·search layout/recipe·설치 source·CURRENT를 다시 읽는다. 이번 BASELINE과 source snapshot은 덮어쓰지 않는다. 별도 `integration-evidence/<stage>/`에서 새 증거를 만든다. 기존 dirty/untracked는 보호한다.
2. **장르와 신원 문맥 분리.** C01~C04, C07~C15, C20~C22는 context/boundary로 보존한다. 캠퍼스·과잠·NA가 학생 신원·성인 여부·성적 의미·동의·교수 권한을 생성하지 못하게 한다. source의 context route를 positive 시각 후보로 가져오지 않는다.
3. **전공·기능 단위.** 대형 강의실 S01, 과사 S03, 협업실 S07, 설계실 S09, 생활구역 S11, 공동 노트북 A13, 공동 도면 A14를 우선 검토한다. 기존 홈룸·공책·서가·단일 생활실의 의미를 조용히 바꾸지 않는다.
4. **핵심 복식 경계.** 과잠/바시티 W01과 레터 스웨터 W02, OCBD W04, 작업용 닫힌 가운 W23, 학위 가운/후드/모자 W27과 sub fusc W28을 우선한다. 기관·행사·위험별 조건을 보존한다.
5. **교차 인물 접촉.** A21·A23·A25·A27·A29·A30·A32·A37·A38과 P07의 화면 경계를 우선한다. 인물/물체 수, 의복 착용자, 손 주인, 머리/골반 지지, 손목의 연속 연결을 source 전체 계약으로 다룬다.

P0의 source 완성 기준은 위 카드의 native 원문·조건·effects·owner 선택·slot 역할이 검증되고 문맥 항목이 positive에 섞이지 않는 것이다. 단순 태그 수나 카드 수를 기준으로 완료하지 않는다.

## P1: 일상·패션·연출의 선택 폭을 확장한다

- 통학·휴식·공연·공동 제작·공간별 조명·캠퍼스 바깥 생활권을 보강한다. 실제 요구가 없는 벚꽃·야식·과잠·노을을 매번 추가하지 않는다.
- W03/W05/W07/W08/W09/W21/W22/W24/P08/S14처럼 묶인 용어는 실제 구조별로 분할한다. 예: 후디/집업/크루넥, 카디건/베스트, 니삭스/오버니/타이츠, 로퍼/메리제인, 앞치마/스크럽/커버올, 열린 중정/정류장. 현재 한 표본은 나머지 대안의 정확 의미를 충족하지 않는다.
- W11~W22의 파티복·시어·레이스·란제리풍은 **성인 인물·요청 문맥·구조·핏**을 따로 확인한다. 옷 명칭만으로 성적 행동·취향·동의를 붙이지 않는다. baby tee의 baby를 아동 모델로 읽지 않는다.
- GAPS.md의 미학·지역·소재·역사 고증을 보강한다. 출처 미확인을 외부 검증 완료로 승격하지 않는다.

## 실제 변경 경로와 데이터 계약

아래 경로는 **제안**이며 아직 생성/수정하지 않았다.

| 경로 | 반영할 내용 | 지켜야 할 계약 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_campus_life_semantics_20261024.json` | source별 확인 범위·카드·route·triage | 기존 semantic registry 구조와 호환성 심사. 실패 출처·시간/신원 문맥 보존 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_campus_life_20261024.json` | 심사 후 채택한 가시적 선택안만 | native module/v3 후보 전체 필드, 안정 CID, 한영 명제 완전 일치, 가시 관계 보존 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_campus_life_bindings_20261024.json` | 실제 기능에 맞는 optional binding | 유효한 기존 149-slot catalog 사용, 단순 명칭 유사도에 따른 multi-tagging 금지 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 확정된 authored 모듈만 등록 | 다른 연구 모듈/정책을 지우지 않고 정확 source 합집합 유지 |
| `skills/photo-prompt-image-generator/tests/test_campus_life_semantics.py` | 유효성·문맥 분리·관계/개수·한영·회귀 사례 | 실제 의미 경계를 검사하고 구현을 그대로 복제한 형식 검사만으로 대체하지 않음 |
| `docs/research-evidence/photo-prompt/campus-fiction-20261024/integration-evidence/` | 심사·native·검색·프롬프트·픽셀·설치·발행 영수증 | 연구 당시 snapshot과 새 단계의 증거를 분리 |

리서치의 `suggested_slots`는 mapping 제안이다. 해당 slot에 잘 맞는다는 이유만으로 source의 개수·접촉·신원·장면 효과를 생략하지 않는다. 실제 native `effects.dimensions/properties`는 최종 문장 전체가 도입·수정하는 owner/개수/복장/접촉/지지/포즈/공간/조명/글자/매체 경계에서 작성하고 현재 validator와 effect permission에 맞춰 심사한다.

## 기존 후보 심사 절차

`existing-records.json`의 14개 후보에는 원문 전체와 모든 binding을 보존했다. `triage-authored.json`의 제안은 재사용 6, 정제 6, 문맥 분리 2이다. 승인이나 변경이 아니다.

1. CID별 원문·realization·conditions·effects·binding·native evidence를 최신 상태에서 읽는다. label·alias·태그만 비교하지 않는다.
2. 연구 카드의 **명제·owner·개수·연결·가림·매체 경계**를 기존과 대조한다.
3. `reuse`: 완전히 충족하는 의미는 기존 CID/binding 보존. 추가한 손 주인·의복 층·물건 수가 없다면 중복 생성을 피한다.
4. `refine`: 부족한 관계만 고치되 의미 변경·실현 분기·이전 사용자 의도를 검토한다. 일반화가 불가능하면 별도 신규 realization으로 둔다. 볼 지지와 턱 지지, 공책 공유와 노트북 공유, 열린 가운과 닫힌 가운은 같지 않다.
5. `new`: 기존 원문의 의미 전체로 충족할 수 없을 때만 신규 등록. lexical 0건은 신규의 충분 근거가 아니다.
6. `context`: genre·학적·동의·진단·기관 권한·시간·소리·원인·출처/세계관 제한을 보존한다. `defer`: 세부 구조·출처·native owner/effects 근거가 부족하면 보류한다.

SCP 특정 포럼 후보를 캠퍼스 익명게시판으로 재태깅하거나, 교복 위 열린 가운을 실제 위험작업용 닫힌 가운으로 해석하는 방식은 채택하지 않는다. 원래의 세계관·조건·의무를 보존한 별도 실현을 검토한다.

## 검증 순서와 통과/보류 기준

| 단계 | 확인할 것 | 통과 기준/실패 처리 |
|---|---|---|
| R0 연구 무결성 | 참조 356행 연결·출처 상태·graph endpoint·초안/문맥 분리 | 이번 validator의 구조 확인. 사실성·native·검색·픽셀 합격의 의미는 없음 |
| R1 native source | corpus load/validator·CID·조건·한영 명제·owner/effects·역할 | 최신 source에서 오류 0. 바뀐 record는 현재 native qualification 절차 수행. 연구 JSON을 직접 import하지 않음 |
| R2 검색 source closure | 정확한 합쳐진 authored source와 인덱스 구성 | source hash·candidate/binding closure 검증. 누락·해시 불일치 시 HOLD |
| R3 검색 품질 | 한영·슬롯별·전체 주제별 결과와 혼동 사례 | 수동 정답 지정 후 적합한 후보가 top8에 있는지, 잘못된 정확 의미/기관/신원/성적 태그가 채택되는지 비교. 36개 개발 경계 사례에서 금지된 자동 의미 채택 0을 요구. 지표는 평가 전에 고정 |
| R4 프롬프트 전달 | 노출 CID → 선택 CID → 전체 한영 명제 → 실제 이미지 도구 입력 | 각 단계의 선택/거절 이유와 literal evidence 보존. 검색 노출만으로 채택 성공 처리 금지 |
| R5 native pixels | 12사례의 전체 owner/count/contact/support/framing 계약 | 전체 계약의 모든 필수 gate 충족. 가림·부분 성공은 전체 실패. 차단은 BLOCKED_UNSCORED |
| R6 설치/수용/발행 | installed source·CURRENT·native audit·사용자 판단·commit/remote SHA | 각 단계 독립 기록. 로컬 검증이 설치·픽셀·수용·push를 대신하지 않음 |

R3의 초기 cohort는 카드 파생 124개/248질의와 별도 손으로 쓴 경계 36개/72질의다. 둘 다 연구를 보고 작성한 **개발용**이다. 독립 holdout으로 부르지 않는다. 구현자가 보지 않은 한국/해외·학부/대학원·비캠퍼스 일반 요청·다의어·성인/나이 미확정·다중 인물/물체 사례의 holdout을 후속 단계에서 별도 동결하고 정답을 먼저 심사한다. 단순 contains로 검색 품질을 평가하지 않는다.

## 인덱스와 runtime 적용

조사 시점 search 파일의 선언은 `photo-candidate-search-layout/v1`, `embeddinggemma2-local`, 768차원, `embeddinggemma2-retrieval/v1`이다. 이는 파일을 읽은 결과이며 shards·실행 runtime의 검증 결과가 아니다. 구현 때 최신 상태를 다시 읽는다.

현재 확인한 구현 entrypoint는 `scripts/build_shared_candidate_index.py`, `scripts/photo_h_f2_search.py`, `scripts/photo_candidate_corpus.py`, `scripts/validate_photo_prompt_dictionary.py`이다. build CLI 옵션은 실제 구현 시 해당 파일의 parser에서 확인한다. recipe/layout/model/revision/document identity가 모두 호환되는 벡터만 재사용하고, v2 document vector를 v1로 재명명하지 않는다. 공유 source가 변경되면 exact merged source 합집합으로 다시 계산/검증한다.

기존 slot 검색을 유지하고 전체 주제/기본 프롬프트의 독립 검색도 함께 평가한다. 현재 CURRENT를 바로 바꾸지 말고 별도 index/runtime snapshot으로 자격을 확인한다. native 조건 오류나 HOLD가 남으면 설치 보류다.

프롬프트는 `요청 의미·controls·독립 구도 동결 → 후보 검색 → 선택/거절 → 허용된 open dimensions만 구체화 → audit → 실제 입력 저장` 순서다. 익숙한 과잠·서가·벚꽃을 다양성 수치만 맞추려고 넣지 않는다. 사용자가 잠근 인물 수·의상·접촉·전공·장면을 바꾸지 않는다.

## 발행과 복구

후속 구현을 발행할 때도 원본 연구 baseline을 유지한다. 현재 checkout의 기존 dirty/untracked를 보호하고 필요하면 분리 worktree에서 구현한다. source·binding·semantic registry·파생 index의 명시적 allowlist를 확정한 뒤 staged 경로와 blob hash를 대조한다. 불필요한 `.LOCK`·이미지 실행 부산물·기존 dirty 파일은 넣지 않는다.

commit·main 병합·push·설치 여부는 따로 기록한다. 실제 remote SHA가 local/tracking과 일치함을 확인한 뒤 전용 worktree를 정리한다. 이 문서에는 발행 완료나 설치 완료 주장이 없다.
