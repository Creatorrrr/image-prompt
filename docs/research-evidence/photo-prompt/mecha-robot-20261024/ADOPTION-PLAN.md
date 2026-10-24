# 메카·로봇 시각 의미 및 후보 데이터 반영 계획

2026-10-24 KST. 이 문서는 초기 리서치에서 세운 실행 순서와 완료 기준을 보존한다. 작성 당시에는 research-only였으며 아래 운영 파일을 만들거나 수정하지 않았다. 이후 사용자 요청으로 수행한 데이터 등록과 독립 이미지 3장 테스트의 실제 결과·보류·검증 범위는 [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md)를 따른다. 아래 계획 전체가 자동으로 완료됐다는 뜻은 아니다.

## 1. 반영 원칙

1. 원 요청의 의미와 인물·기체·장비·공간·행동의 소유자를 먼저 동결한다. `메카`라는 단어가 없어도 같은 관계면 후보를 검토하고, 단어가 있어도 무관한 후보는 채택하지 않는다.
2. 연구의 owner graph는 작성·검토용이다. 인용, 카드 ID, 검색 rank, role tag, graph 자체가 typed fact·기존 owner 선택·수정 권한을 주지 않는다.
3. 후보는 전체 한영 의미를 검토한다. 부품 수·소유자·연결·피복·매체층·조건·영향 차원이 다르면 동일 CID의 동의어로 처리하지 않는다.
4. broad genre·성인 취향·작품 고유어 route는 선택적 탐색이다. 그 경로가 새 사람·무장·노출·장치·화면·사건을 자동 추가하지 않는다.
5. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지한다. source·검색·프롬프트·픽셀·사용자 판단은 각각 별도 기록한다.

## 2. 우선순위와 반영 단위

| 순위 | 반영 묶음 | 우선 카드 | 완료를 가르는 조건 |
|---|---|---|---|
| P0-1 | 기체/착용자/인간형/인공표면의 구분 | A01, A03–A06 | 안드로이드·사이보그·외골격·탑승형 오인 방지. 각 연결 대상의 소유 분리 |
| P0-2 | 구조·장착·직동 액추에이터 | B01–B06, B09 | 외장과 프레임, 양끝 고정, 링크·축·지지, 팩과 장착점 구분 |
| P0-3 | 콕핏과 조종자의 접점 | C01–C04, C07 | 손잡이·발판·좌석·하네스 앵커·양손/양발 연결을 완전 보존 |
| P0-4 | 설비 케이블·유체·열·노즐 | D01, D04–D06 | 양끝·연속 경로·패널 뿌리·노즐 방향. 자원 종류를 추정하지 않음 |
| P0-5 | 지지 자세·인양·정비 | H02–H03, H06–H07, I01, I04 | 모든 접점과 실제 지지 대상, 손·다리·기계 팔의 소유 보존 |
| P0-6 | 파괴와 표현층 | J01, J03, J05, K01, K04 | 기계와 유기체 손상, 실제 공간과 표시 영상, 도면과 사진 구분 |
| P1 | 형태·무장·표면·복식·동작 다양성 | 나머지 준비 카드 | 전체 의미 중복 제거, 잠긴 속성 침범과 자동 성적 분류 방지 |
| HOLD | 특정 항G 모델 구조·특정 영상 연출 | G03, K06 | 필요한 공식 도판/원저자 영상 설명을 확인한 후 재판정 |

P0는 묶음별 순차 반영 순서다. semantic-cards.json의 개별 priority는 초기 고위험 대표 카드 표시이며, 이 표의 모든 하위 카드를 자동 운영 승격한다는 뜻은 아니다.

## 3. 기존 후보의 처리 결정을 먼저 확정

- **그대로 재사용**: 우주 서비스 모듈 라디에이터 CID는 실제 요청이 그 모듈 문맥일 때 원문 전체를 사용한다. 메카 등판이면 소유자가 달라지므로 새 context variant로 검토한다.
- **기존 의미 정교화 또는 별도 세부 후보**: A01의 거대 탑승형, A05의 착용 프레임, G01의 파일럿 복장은 기존 source·binding·guard·effect를 읽고 세부안을 비교한다. generic 후보가 유용하면 남기고 새 관계 후보와 병존시킨다.
- **metadata 검토**: 외골격 source의 `android` keyword와 `partial_cyborg` facet이 실제 의미에 맞는지 평가한다. HAL의 제조사 용어를 지우는 조치와 생물학적 개조를 가정하지 않는 조치는 구분한다. 근거 없는 일괄 삭제는 하지 않는다.
- **신규 제안**: 나머지 대부분은 새 optional source 후보이지만 아직 corpus-wide semantic dedupe를 끝내지 않았다. 현재 108은 신규 운영 CID 수가 아니다.
- **진단 전용**: 32개 맥락 구분은 positive retrieval에 넣지 않는다. 작품 고유어·의식·동의·정신 공유·직업·시간을 외형 후보의 동의어로 편입하지 않는다.

현재 full-record 심층 검토는 4개 CID다. 후속 작업에서는 모든 신규안의 가까운 기존 source를 전체 EN/KO·조건·효과·binding까지 비교하고 `reuse / refine / new_context / new / defer`를 카드별로 확정한다. 이름이 비슷하다는 이유만으로 합치거나 lexical 0건을 근거로 새 후보 수를 확정하지 않는다.

## 4. 운영 반영 파일과 경계

후속 구현의 예상 파일은 다음과 같다. 날짜는 실제 반영 시점과 저장소 관례에 맞춰 고정한다.

| 파일 | 역할 |
|---|---|
| `skills/photo-prompt-image-generator/assets/photo_mecha_robot_semantics_20261024.json` | 검토된 시각 카드와 진단의 source metadata. runtime authority 아님 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_mecha_robot_20261024.json` | 전체 한영 optional source. 네이티브 corpus schema와 검토 결과에 맞춰 작성 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_mecha_robot_bindings_20261024.json` | 실제 의미가 맞는 role의 선택적 binding만 등록 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 검토한 새 모듈만 파일명/kind 기준으로 추가 |
| `skills/photo-prompt-image-generator/references/mecha-robot-visual-semantics.md` | 용어 범위·소유자·혼동·맥락과 source/pixel 한계 |
| `skills/photo-prompt-image-generator/references/maintenance.md` | 최종 구현 범위와 미검증 경계를 간결하게 안내 |
| `skills/photo-prompt-image-generator/tests/test_mecha_robot_semantics.py` | 의미 경계·관계 보존·데이터 통합의 실제 회귀만 추가 |

새 슬롯은 현재 계획에 필요하지 않다. research 초안의 pose/costume 같은 작성용 이름을 운영 슬롯으로 간주하지 않고 현재 catalog의 `body_pose`, `garment_detail`, `wardrobe_style`, `surface_material`, `scale_relation`, `relational_action`, `gaze_target` 등으로 대응시켰다. 현재 19개 슬롯·231개 제안은 semantic fit 검토 전이며 approved binding 수가 아니다. 단일 source의 몸·의복·기계·공간·인원·매체에 미치는 전체 효과를 모두 검토해야 한다.

## 5. 단계별 구현과 검증

### 단계 A — 연구 정리와 보류 해소

원문 323개 보존 항목의 route/context를 점검하고 108개 카드의 EN/KO에서 수·좌우·동작·피복·매체층을 대조한다. 후보와 실제 source의 의미 동등성은 별도 판단한다. 403·404·초록만 읽음·인용 지원 미확인을 registry에 유지한다. 상세 항G 모델, 정확한 변형 운동, 각 작품의 판본별 구조·도판, 카토키·이타노 명칭 근거는 필요한 범위부터 추가 조사한다. 레이버/예거/드리프트의 기본 공식 정의는 이번 조사에서 확인했다.

합격: 각 카드는 한영 전체 의미, 실제 source support 범위, 소유 관계, 관찰 한계와 검토 상태가 일치한다. 보류 카드를 분리한 채 나머지 준비 데이터의 반영은 진행할 수 있다.

### 단계 B — source와 native qualification

source graph를 실제 typed source fact로 자동 변환하지 않는다. 현재 네이티브 검토·source-unit 요구를 따라 각 positive field의 직접 근거, 실제 owner, 효과, 조건, role fit을 작성·검토한다. 선택 가능한 기존 owner가 필요하면 해당 개체의 재질·구조·관계 prerequisite를 검증한다. 외골격 프레임 source가 새 사람을 필요로 한다면 `subject`가 잠긴 기계 장면에 몰래 사람을 생성해서는 안 된다.

합격: 운영 validator와 해당 full source/native 검토에서 유효한 레코드만 후보 모듈에 등록한다. 출처 citation과 research graph가 있다는 이유만으로 native approval을 true로 만들지 않는다. 양언어의 전체 내용이 달라지거나 필수 양끝이 빠지면 보류한다.

### 단계 C — source 및 index 통합

현재 작업본은 변경이 많으므로 적용할 파일을 명시하고 다른 작업의 manifest·후보·검색 shard·runtime pointer를 보호한다. 좁은 변경 범위로 source 검증 후 정확히 합쳐진 source union에서 index를 새로 만든다. 기존 vector의 ID·전체 text hash·recipe·provider/model/dimensions·integrity가 모두 맞을 때만 재사용한다. 구형 layout을 새 이름으로 바꾸어 재사용하지 않는다.

사용할 저장소 명령은 다음과 같다. 이 명령은 후속 실행 계획이며 이번 리서치에서 실행한 것으로 기록하지 않는다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
# 위 결과의 runtime_python 또는 실제 준비된 dependency runtime 사용
<runtime_python> skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
<runtime_python> skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
# 최종 source 검토 이후 새 index build 및 sealed generation 검증은
# references/maintenance.md의 현재 명령·model recipe에 따라 별도 실행
```

합격: 새 source/index identity·전체 통계·payload/vector closure·호환 recipe가 검증된다. source 검증만으로 설치/활성화를 주장하지 않는다.

### 단계 D — 실제 검색과 맥락 통제

`retrieval-regression-plan.json`의 한영 자연어 48쌍과 12개 통제 사례를 검토된 sealed generation에서 실행한다. 슬롯별 독립 검색을 유지하고 전체 theme+baseline 후보 탐색도 따로 기록한다. 실제 query context·issued receipt·CID/RID·EN/KO·상위 선택지를 남기고 언어별/role별 부적합과 누락을 확인한다. 카드 문장을 그대로 질의한 경우만 성공하는 것은 자연어 노출 검증으로 충분하지 않다.

합격 기준은 먼저 최소표본을 읽어 고정한다. P0 자연어 질의는 사전 지정한 적합 source가 실제 top8 선택지에 노출되는지, 전체 source 의미·role·잠금 조건에 맞는지 각각 판정한다. 통제 사례에서 새 인물·장치·노출·화면·고유어의 무단 추가가 하나라도 발견되면 활성화를 보류한다. 부정확한 노출을 줄이려고 요청 의미를 부정문으로 삭제하지 않는다.

### 단계 E — 프롬프트 전달과 픽셀 검증

이미지 테스트가 요청된 후 실행할 세 가지 독립 장면을 아래에 준비했다. 이번에는 생성하지 않았다. 각 장면은 baseline·선택 후보·owner/property lock·실제 prompt literal·실제 saved pixels를 별도로 기록한다.

| 장면 | 확인할 관계 | 대표 실패 |
|---|---|---|
| A. 전선 정비 | B03의 실린더 양끝 + D01 케이블 경로 + I04 공구 접점 | 격납고 분위기는 맞지만 한쪽 고정점·케이블 끝·체결부가 가려짐 |
| B. 성인 탑승 준비 | C01 해치 접점 또는 C02/C03 착좌 접점 중 한 완전 장면을 선택 | 외부 전경에 작은 콕핏을 넣고 내부 네 접점까지 성공했다고 주장 |
| C. 안드로이드/부품 회수 | J01 또는 J03의 분리·표면 경계와 지정 소유 | 기계 유체가 혈액이 됨, 합성 표면이 인간 상해로 바뀜, 소유자 혼합 |

한 사진에 모든 카드를 과밀하게 넣지 않는다. 선택한 필수 관계는 줄이거나 격하하지 않고, 선택 전 장면 비교에서 실현 가능한 완전 대안을 고른다. 전체 장면과 원본 해상도 세부를 확인한다. 보간 확대·부분 crop·local impression은 숨은 전체 경로의 증거가 아니다. 가려짐은 `BLOCKED_UNSCORED` 또는 해당 관찰 실패로 기록하고 `partial_is_fail`을 지킨다. source registration·검색 노출·프롬프트 literal·saved pixel·요청자 선호의 결과는 합치지 않는다.

### 단계 F — 설치·활성화·공유

source, 검색, prompt transport를 검증한 새 sealed release를 별도로 준비하고 현행 recorder와 dependency를 확인한다. 설치와 활성화는 구분한다. 기존 pointer·release·run history를 보존하고 필요한 rollback 경로를 남긴다. 사용자에게 어떤 층이 완료됐는지 그대로 보고한다.

commit/push 또는 publication을 진행할 때는 해당 파일만 명시적으로 stage하고 staged name/blob와 제외 파일 해시를 확인한다. 최종 local/tracking/remote SHA를 따로 검증한 뒤 전용 임시 작업물만 정리한다. 현재 리서치 단계에서는 commit/push/PR·운영 활성화를 수행하지 않는다.

## 6. 이번 턴에서 확보한 검증과 아직 없는 증거

확보: 원 대화 전체 범위의 Chrome 확인, 기존 source 탐색 및 4건 full-record 비교, 출처별 지원 범위, 108개 한영 초안·413개 관계, 실제 catalog 19개/231개 제안, 읽기 전용 installed recorder 점검, 연구 산출물 무결성 확인.

아직 없음: 후보 전수 중복 비교, 독립 번역 검토, full native source qualification, 승인 role fit, 운영 source 등록·index rebuild, 새 release 설치·활성화, 실제 자연어 검색 결과, compose audit/transport, 새 이미지·픽셀·사용자 수용. 수량이나 schema PASS는 이 증거들을 대신하지 않는다.
