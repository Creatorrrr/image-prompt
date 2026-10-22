# 리서치 결과 반영 계획

2026-10-22 / 연구 초안 기준. 이 문서는 구현·활성화 결과가 아니다.

## 목표와 우선순위

목표는 포크 호러 요청의 뜻을 보존하면서 구체적인 후보를 찾고, 완전한 관계를 선택하고, 실제 표현을 검증할 수 있게 하는 것이다. 150개 용어를 자동 profile 150개로 만들거나 초안 70개를 모두 신규 CID로 넣는 것이 아니다.

| 순서 | 범위 | 반영 이유 | 완료 조건 |
|---|---|---|---|
| P0-A 의미 경계 | X01~X19 전체 | 장르·문화·희생·동의·시간·도상 혼동을 먼저 차단 | 각 원 항목에 context/defer 및 검증 상태 기록. 가시 사실로 승격되지 않음 |
| P0-B 공간과 공동체 | L01/L03~L06/L12/L13, R01~R05/R07 | 사물 나열을 넘어 장소와 인간의 행위를 연결 | 기존 R01과 일반 경계 후보 비교, 중복 없는 완전 관계, 양끝 가시 기준 |
| P0-C 의례 물체 | O01/O02/O06~O11/O15, F02/F03 | 재료·운반·용기 내부·표식 위치 등 실제 표현 공백 | 은닉/개봉 등 선택 branch의 일관성, 문화별 출처 범위 보존 |
| P0-D 한국·일본 구분 | K01~K08, J01/J03 | 금줄·시메나와, 신목·기둥·새, 상징물·시신 혼동 방지 | 지역·제차에 맞는 출처와 역할 검토, 한국/일본 대조 사례 통과 |
| P0-E 관측 한계 | V01, F01 | 시신/원인/희생과 대낮/위협의 차이 | 가시 관측과 장르·인과 해석을 분리한 판정 |
| P1 확장 | 나머지 가시 카드와 전승별 후속 조사 | 구체적 요청을 다룰 표현 폭 확대 | 개별 원전 확인 후 선택적으로 채택. 후보 수 할당 없음 |

P1에는 성인 나체 V07과 신체·의례 관계 V02~V06도 포함한다. 이는 의미를 누락하는 결정이 아니라, 기본 장르 요청에 자동 추가하지 않고 명시 요청과 개별 소스의 완전한 조건에서 다루는 순서다.

## 0. 구현 직전 재기준화

현재 작업트리에는 다른 작업의 수정·미추적 파일이 있다. 이 연구는 기존 파일을 되돌리거나 stash/reset하지 않았다. `BASELINE.json`과 `VALIDATION.json`의 hash 비교는 각 시점만 설명한다. 구현 시작 직전에 HEAD, dirty/untracked, manifest의 모듈 전부, `photo_candidate_search.json`, `retrieval-runtime.json`, 선택된 코드/데이터 세대와 포인터를 다시 기록한다.

독립 작업 공간이 필요하면 기존 적절한 worktree를 우선 확인한다. 필요한 dirty 소스를 가져와야 한다면 exact 파일 allowlist와 원본 해시를 기록한다. 브랜치/체크아웃만 최신으로 만들어 진행 중인 작업을 누락하지 않는다.

읽기 전용 확인 진입점:

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

이 검사 PASS는 설치된 recorder/의존성 확인이다. 이 연구의 채택·인덱스·이미지 적합성을 보증하지 않는다.

## 1. 카드별 채택 결정을 남긴다

각 가시 카드 70개와 문맥 카드 19개에 다음 중 하나를 결정한다. 결정은 최신 원문·조건·effects·선택 RID·binding·프로필 의무를 읽은 뒤 내려야 한다. `existing-source-mapping.json`은 시작점의 full record snapshot이며 native 의미 승인은 아니다.

| 결정 | 조건 | 남길 증거 |
|---|---|---|
| reuse | 기존 complete source가 같은 소유·부분·수·관계를 갖고 추가 효과도 요청에 적합 | 실제 CID/RID, owner 파일, 조건·효과·의무 비교 |
| refine | 의미는 맞으나 번역·표현·질의 지원 또는 명확한 근거가 부족 | 수정 전후 source diff, 원래 의미 보존, index 재생성 필요 |
| new | 가장 가까운 기존 complete source로 필요한 구조를 충족할 수 없음 | 이웃 CID와 부족한 관계, 신규 소스의 정확한 의미 |
| context | 서사·의도·원인·시간·음성·관객 효과 등의 경계 | 긍정 시각 후보 아님을 loader 계약에 맞게 보존 |
| defer | 원전·판본·지역·역사적 근거가 아직 약함 | 빠진 출처·확인 질문·재개 조건 |

예상 초기 결정은 R01 `reuse 우선`, K01 `기존 일반 경계와 분리한 new 검토`, O09/O10 `서로 다른 완전 실현`, X18 `문맥 경계 우선/원전별 외형 보류`다. 현재 결정을 native 승인이 끝난 것처럼 기록하지 않는다.

개별 원전 조사가 먼저 필요한 항목은 최소한 Imbolc/Lughnasadh 세부 차이, Morris/Hobby Horse 지역형, Cunning Folk 직능, fairies/changeling/banshee/black dog/wild hunt/rusalka/yamauba 각 판본, sin-eater/senicide, hieros gamos/ritual orgy, Sheela-na-gig의 개별 유물, 강신무/세습무·공수·손님굿, katashiro/kegare/harae/tsukimono 등이다. 43개 출처가 이 항목 모두의 독립 검증을 대신하지 않는다.

## 2. 데이터 반영 위치와 소유권

아래는 후속 구현의 예상 파일이며 이번에 작성하지 않았다.

| 예상 경로 | 역할 |
|---|---|
| `skills/photo-prompt-image-generator/assets/photo_folk_horror_semantics_20261022.json` | 원 번호·출처 범위·판본·카드·채택 결정을 연결하는 추적 레지스트리. intrinsic effects의 두 번째 권위가 되지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_folk_horror_20261022.json` | 검토를 통과한 신규 V3 후보 소스만 등록. 실제 CID/RID와 소유 파일을 생성 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_folk_horror_bindings_20261022.json` | 현행 slot catalog에 직접 의미가 맞는 역할 연결만 저술 |
| 기존 후보 owner 파일 | refine 결정한 CID의 원래 소유 파일만 좁게 수정. 전체 shard 일괄 재작성 금지 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 검토한 모듈을 명시 등록 |
| `skills/photo-prompt-image-generator/references/folk-horror-visual-semantics.md` | 유지보수·판본·혼동 경계. 일반 생성의 precore 재료로 읽히지 않게 유지 |
| 영향받은 회귀 fixture | 실제 소유·효과·역할·언어·비가시 경계를 검증하는 최소 사례 |

`candidate-drafts.json`은 runtime loader 입력이 아니다. 연구 ID·source URL·owner graph·문서의 PASS를 native proof로 복사하지 않는다. 현재 parser가 허용하는 필드와 source-unit 계약을 확인한 뒤 저술한다. 문맥 레코드도 현재 운영 스키마의 허용 계약으로 별도 검토한다.

## 3. 한영·소유·조건·효과를 함께 검토한다

각 후보는 한 실제 선택 실현의 전체 의미를 담는다. `phrase_en`과 `phrase_ko` 모두 같은 소유자·수·상태·범위·재료·접점을 보존해야 한다. 별칭·태그·출처 설명으로 긍정 필드에 빠진 사실을 대신하지 않는다. 부정 예·claim limit·박해자의 주장은 양의 시각 사실 또는 embedding의 긍정 요구로 섞지 않는다.

| 예 | 필수 소유/조건 검토 | 효과 검토 |
|---|---|---|
| O06 마리 루어드 | 두개골 형상·장대·천·운반자는 다른 owner/part. 사람 머리에 해골을 이식하지 않음 | prop, material, appearance, person presence/count, pose, setting의 실제 변경 전부 |
| O09/O10 방어병 | 밀봉/개봉은 서로 배타적 실현. 핀·머리카락은 O10에만 가시 | contents, container state, object arrangement, visibility |
| K01 금줄 | 양 기둥·줄·숯·솔가지·꼬임. 시데와 고추를 자동 추가하지 않음 | boundary geometry, material, attachments, placement |
| K06 굿 | 연행자와 악사는 별도 실제 owner. 북의 소유자를 바꾸지 않음 | human count, action, setting, costume/context prerequisites |
| J03 내방신 | 가면·의상은 성인 착용자 소유. 해당 지역 판본을 확인 | count, costume, relationship, action, meal props |
| E05 마나낭갈 | 동일 존재로 선언한 상·하체와 날개의 실제 관계 | anatomy/body geometry, body count/identity, appearance, spatial separation |
| V07 성인 나체 | 성인 문맥과 외형이 충족되는 요청에서만 검토 | clothing/exposure, body presentation, setting. 의례명만으로 채택 불가 |

새로운 optional 인물을 추가하면 기존 인물 수 lock과 충돌할 수 있다. `prop` 역할로 제안되더라도 source 전체가 사람·행동·배경을 바꾸면 모든 effects를 확인한다. 역할 이름·어휘 일치만으로 direct 승인을 주지 않는다. intrinsic/role 조건이 실패한 소스를 unbound proposal로 우회하지 않는다.

## 4. 구조와 의미 회귀

사전 validator와 영향받은 계약 검사를 수행한다. 기존 source의 historical proof와 새 소스의 proof를 분리한다. 다음 실패가 있으면 인덱스 단계로 넘기지 않는다.

- broad genre label이 모든 의례·고어·나체·특정 문화권을 강제함.
- 금줄과 시메나와, 장승과 솟대, poppet과 저주, witches' marks와 피부 낙인이 뒤섞임.
- 밀봉된 불투명 병의 내부를 보았다고 기록함.
- 동의·혈통·사인·액체 성분·전후 변신·음성의 사실을 스틸 픽셀로 판정함.
- 한 언어에서 owner·물성·수·관계가 빠지거나 바뀜.
- 선택하지 않은 branch 또는 의무를 union해 장면이 불가능해짐.
- 연구의 context/claim limit를 긍정 factual text로 편입함.

현재 유지보수 문서의 검사 예:

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

실제 구현 시 해당 체크아웃·선택 런타임의 지원 인자와 Python을 확인한다. 이 연구에서는 위 두 운영 검사를 실행하거나 실패 결과를 고치지 않았다.

## 5. 독립 인덱스와 검색 평가

양의 의미 텍스트가 바뀌는 수정은 인덱스 갱신 대상이다. 운영 검색 manifest는 `photo_candidate_search.json`이며 legacy index 경로로 대체하지 않는다. 별도 staging 세대에서 provider/model/space/dimension/recipe/text hash/vector integrity를 묶고, 정확히 맞는 검증된 벡터만 재사용한다. build 중 원본이 바뀌면 활성화하지 않는다.

연구 폴더의 평가 질의는 개발 24, 경계 16, 일반 대조 8, 비가시 대조 4인 총 52사례/104개 한영 질의다. 실제 질의·lane·slot·CID/RID·complete source·노출·선택 이유·오탐을 보존한다. `keyword_only` 진단과 실제 hybrid 검색 결과를 섞지 않는다.

초기 목표는 P0 양성 사례의 한영 각각 eligible complete-source Recall@10 90% 이상, 가시/문맥 경계의 오승격 0건, 일반 대조·고정 owner/count/노출 제약의 위반 0건이다. 이 수치는 제안한 목표이며 달성 결과가 아니다. top-10에 뜬 후보 중 의미가 다른 후보를 정답으로 세지 않는다. role 적합도와 전체 scene 효과를 따로 주석화한다.

독립 holdout은 실제 구현·튜닝을 마친 뒤 다른 사람이 12개 이상의 새로운 자연어 요청으로 작성한다. 본 평가 질의를 단순 번역·어순 변경해 독립 holdout이라 부르지 않는다. 사람이 없으면 저술/튜닝과 분리한 새 평가 라운드임을 명시하고 완전 독립성을 주장하지 않는다.

## 6. 선택·프롬프트·이미지 검증

원 요청의 의미와 창의성 controls로 후보 없는 baseline/core를 먼저 동결한다. 연구 폴더·후보·슬롯 조회가 그 독립 코어의 근거로 들어가면 새로 작성한다. 이후 기존 후보와 보강 후보를 의미·소유·변경 가능 범위·완전한 시각 의무로 비교한다. 전부 거절하거나 baseline을 유지하는 판단도 허용한다.

선택한 후보는 source 전체의 실제 효과와 literal prompt evidence를 묶는다. audit PASS는 생성 전 무결성 증거이며 그림의 표현 성공이 아니다. [PIXEL-PLAN.md](PIXEL-PLAN.md)의 첫 12사례를 A 독립 baseline / B 현행 후보 / C 보강 후보로 비교한다. 반드시 같은 requester 의미·controls·생성 설정을 보존하고, 장면 전체의 이해 가능성과 source별 hard gates를 따로 평가한다.

## 7. 봉인·설치·활성화와 롤백

구조·한영 검색·의미 오탐·필수 원본 이미지 검토가 완료된 범위만 봉인한다. 연구 단계가 끝났다고 자동 설치하지 않는다. 실제 운영 변경을 진행하는 후속 범위에서 검토한 source/index/code allowlist, 설치 세대와 현재 포인터, 이전 세대 복구 경로를 함께 기록한다. source edit, index build, generation sealing, installation, CURRENT activation, commit/push는 각각 별도 상태다.

이미지/도구 미지원·차단 사례에는 NO_PIXELS 또는 NOT_RUN을 남긴다. 실패를 다른 모티프로 바꿔 충족했다고 보지 않는다. 부분·가림·필수 접점 부재는 `partial_is_fail`이며 `UNOBSERVABLE_NOT_PASS`다. 관객의 공포·아름다움·선호·사용자 수락은 원본의 물리적 준수와 구별한다.

## 최종 반영 보고 형식

카드별 채택 결정과 실제 CID/RID, 수정한 owner 파일, 구조 검사, 검색 노출/오탐, 선택/프롬프트 증거, 원본 이미지 판정, 설치/활성화 상태, commit/push 상태를 각각 보고한다. 이번 작업의 현재 상태는 연구 문서·구조화 초안·반영 계획 작성 완료이며 이 실행 단계들은 미수행이다.
