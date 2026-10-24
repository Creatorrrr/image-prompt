# 영지물 리서치 반영 계획

2026-10-24. **이 문서는 후속 구현 계획이다. 현재 운영 데이터·인덱스·runtime 반영은 수행하지 않았다.** 목표는 관련 요청의 정확한 의미와 완전한 시각 관계를 선택적으로 찾는 것이다. 장르어가 등장하면 신규 카드 전체를 강제하는 방식은 사용하지 않는다.

## 1. 우선순위와 데이터 결정

| 우선순위 | 범위 | 첫 작업 | 완료 조건 |
|---|---|---|---|
| P0 의미 경계 | K01–K08, K14 | 장원/봉토/직영지·신분·세목·시간·신화 분리 | 제도·시간·의도가 positive 물리 사실로 새지 않음 |
| P0 기존 재사용 | D02, F07와 기존 8 CID | 원문 전체·한국어·조건·effects·bundle·binding 비교 | 같은 뜻 중복 제거; 다른 뜻/허구 대안 보존 |
| P0 운영 관계 | A03/A04/A05/A06, B01/B06/B07, C01/C02, E01/E02/E03/E05/E06/E07 | owner·같은 물건·연결·접촉·수취 상태 저술 | 실제 endpoint·조건·효과·역할의 일관된 source |
| P1 생산·물류 | A07/A08, C03–C08, D04/D08 | 공정별 도판·입출구·하중·통과 경로 검토 | 수차/제분/축융·방적/직조·제련/단조 구별 |
| P1 복식·갑옷 | F01–F08, G01–G06 | 지역·연대·개별 유물·옷층·안쪽 부속 검토 | 외부 실루엣과 내부 구조 증거가 분리됨 |
| P1 주민·동아시아 | E08, I01/I02, K09/K20 | 기록·구휼·돌봄·지역 제도 보완 | 피부/복식·신분 오판과 제도 등치가 없음 |
| P2 확장 | H01–H04, K10–K19, 원문 보류 56행 | 필요도가 높은 세부 정의·도판부터 확보 | 허구/역사/문맥/직접 시각 주장이 구별됨 |

60개 초안을 모두 새 CID로 만드는 것이 목표는 아니다. 결과는 `reuse`, `correct`, `new`, `split`, `context_only`, `defer` 중 하나로 확정한다. 이 명칭은 연구 disposition이며 새로운 runtime wire-format enum을 뜻하지 않는다.

## 2. 단계 A — 최신 기준 고정과 기존 작업 보호

입력: 이번 `BASELINE.json`, `existing-source-mapping.json`, 현재 checkout·source manifest·slot catalog·설치된 세대.

1. 후속 구현 시작 시 HEAD, tracked/dirty/untracked 목록, source module·manifest·catalog hash를 다시 읽어 별도 `integration-evidence/BASELINE.json`에 저장한다. 이번 조사 snapshot을 덮어쓰지 않는다.
2. 현재 checkout과 연결된 worktree를 확인하고 적합한 기존 작업 공간을 우선 사용한다. 공유 파일 충돌 위험이 크면 관리되는 별도 worktree에 검토한 변경만 재구성한다.
3. 변경할 파일·기존 CID·binding ID allowlist를 먼저 만든다. 관련 없는 수정·삭제·untracked 파일을 복구·삭제·스테이징하지 않는다.
4. 실제 source maintenance에 들어가기 전 `photo_installed_h_f2.py --check-runtime`으로 설치된 실행 경로·recorder 경계를 확인한다. working source 변경과 설치된 runtime의 활성 상태를 혼동하지 않는다.

완료 증거: 새 기준 snapshot·allowlist·보호 hash·작업 공간 경계. 이 단계만으로 신규 source나 runtime은 활성화되지 않는다.

## 3. 단계 B — 원 항목과 사료의 정확한 범위 확정

입력: `reference-inventory.json`, `sources.json`, 60개 시각/20개 문맥 카드, 보류 56행.

1. 복합 표제를 원자 개념으로 분리한다. 예를 들어 `채찍형·낙인형·절단형`은 한 개 형벌로 등록하지 않는다. 원 행 ID는 이력으로 유지한다.
2. 시각 카드에 연결된 단어도 exact definition 인증으로 취급하지 않는다. `흙 집어 보기`는 E05의 곡물 견본 장면과 별도 실현이어야 하며 `장원법정`은 B08의 종이 모양으로 확정할 수 없다.
3. 37개 추가 구조/도판 검토 카드를 우선 처리한다. 나머지 카드도 도판 직접 검토 상태는 NOT_RUN이므로 역사 재현을 표방하려면 개별 표본을 붙인다.
4. 출처의 실제 주장과 저술한 장면을 분리한다. 사료의 규범·기술 설명, 박물관 유물, 후대 복원, 작품 공식 설정을 서로 다른 provenance로 남긴다.
5. 접근 실패·검색 발췌·초록만 확인한 출처는 본문 검토로 승격하지 않는다. S03/S36은 새 긍정 사실의 단독 근거로 쓰지 않는다.
6. 한국/일본/서유럽의 제도명은 서로의 번역 alias로 합치지 않는다. 물리적으로 비슷한 계량·측량 동작은 별도의 역사 문맥과 연결할 수 있다.

완료 증거: 개념별 정의·출처 위치·검토 수준·남은 논쟁·실제 시각 지원 범위. 미해결 항목은 `defer` 또는 `context_only`로 남긴다.

## 4. 단계 C — 기존 의미 재사용·보정·분할

아래 CID는 이번에 원문 전체를 직접 읽었지만 후속 구현 시 최신 hash를 재대조해야 한다.

- 영지 소품 묶음 `cand_1bd324372fab529e83751368b01edd9c`: 현재 소품 5종의 묶음·primary tag 조건을 보존한다. 새 업무 관계의 편의 때문에 원래 후보를 한 물건으로 축소하지 않는다. `effects={dimensions:[],properties:[]}`가 실제 추가 효과의 검토를 면제하지 않는다.
- 격자문 `cand_8f33f22aa0de5e3dbb8815b70d686d3e`, 관찰 구도 `cand_493311a3b926597783f631f889a05400`, bundle `cand_b9a6a8e1281f5d019c338b9f4e4b3198`: 우선 재사용/한국어 완전 의미 보정 검토. bundle 의존성과 양쪽 문 홈·전체 통로 의무를 보존한다.
- 파니에 부분 관계 `cand_dfd89db900735d9b8116fccb6c52a6d2`, `cand_22079d8d7f705caea3f446184813280f`: 표제가 같아도 원문 관계가 다르므로 같은 payload로 병합하지 않는다.
- 전체 파니에 `cand_a1425f8956985eaeafa7c7a7c954255a`: F07의 신규 정본보다 재사용을 먼저 검토한다. 허리 연결·받침·겉치마·폭 비교를 모두 보존한다.
- 로코코펑크 `cand_74c968440a0e56b1907e181579c565b4`: primary tag, 재사용 부품, 수리 흔적, 착용자에게 돌려주는 문맥을 보존한다. 영지물이라는 이유로 역사형으로 교체하지 않는다.

한영 보정은 명사·개수·소유자·부품·배치·상태·조건·negation·표현 층을 대조한다. 영문 긴 관계를 한국어 짧은 표제로 덮거나, 한국어 표제만 보고 영문을 임의로 새 의미로 고치지 않는다. 원래 의미가 바뀌는 분할은 새 정본으로 만들고 이력을 보존한다.

완료 증거: 기존 CID별 disposition, 원본/변경 hash, 전후 전체 뜻, 의존 binding·bundle 목록. 재사용 결정은 live retrieval나 native 자격의 PASS가 아니다.

## 5. 단계 D — 실제 데이터 반영 위치

아래 신규 경로는 제안이며 이번에는 생성하지 않았다. 경로 기준은 `/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/`이다.

| 경로 | 내용 | 권위 범위 |
|---|---|---|
| `assets/photo_estate_management_semantics_20261024.json` | 검토한 카드·원 행 연결·혼동·출처·disposition | 유지보수 sidecar. 자동 역할/사실/선택 권위 없음 |
| `assets/photo_candidate_estate_management_20261024.json` | 승인된 완전한 한영 시각 실현, 분리된 문맥 진단 | native source 형식으로 별도 저술한 정본 |
| `assets/photo_candidate_estate_management_bindings_20261024.json` | 기존 149개 슬롯 중 검토된 role 연결 | 역할 적합성만 담당. 정본 effects 복제 금지 |
| `assets/photo_candidate_corpus_manifest.json` | candidate/binding 모듈 명시 등록 | 운영 source 진입점 |
| `references/estate-management-semantics.md` | 의미·시대·지역·비가시 경계·실제 검증 상태 | 사람용 안내 |
| `references/maintenance.md` | 위 안내 링크와 실제 상태 | 유지보수 문서 |
| 기존 CID를 실제 소유한 `_001/_004/_007/_008/_009/_013/_015`, court-palace module | 승인된 개별 보정 | 허용 CID만 변경; 파일 전체 정렬·정규화하지 않음 |

연구 JSON을 manifest에 직접 등록하지 않는다. 이 보강 때문에 pre-core 절차, 기본 creative controls, sampler, 검색 엔진, 새 슬롯, 장르어 자동 hard activation을 추가할 필요는 없다. 새 필드나 새 native 기능이 꼭 필요하면 데이터 보강과 별도 범위로 판단한다.

## 6. 단계 E — owner·조건·effects·role의 수동 검토

입력: 정본화할 완전 실현과 현재 native 규격.

1. 각 사람·손·물체·물질·문서·화면·기계 부품에 실제 owner를 준다. ‘담당자’라는 이름만으로 기존 요청의 어떤 사람에게나 연결하지 않는다.
2. 후보가 도입하는 모든 효과를 적는다. C08은 위치만 바꾸는 후보가 아니라 사람·배·널판·짐·수레·창고·하중 접촉까지 도입할 수 있다. 소유·수량·허용 dimension/property를 모두 검토한다.
3. 표현 층을 분리한다. 지도 위 구획/현실 밭, 패널의 표시 재고/실제 창고, 문장 그림/실제 격자문을 같은 owner로 합치지 않는다.
4. 단독 실현은 완전한 선택지로 유지한다. D06 평형추식과 D07 인력식을 별도 realization으로 선택하며, F07 파니에와 다른 시대 버슬을 자동 합치지 않는다.
5. 선택한 원문에 필요한 기존 owner나 재료 전제가 없으면 optional 후보를 미선택으로 남긴다. 태그 일치·유일한 인물·slot 이름은 선택 권한이 아니다.
6. native source-unit·guard·effect·role 검토는 해당 시점의 실제 규격과 검증 도구에 맞춰 작성한다. 이번 graph·출처·gate는 review 입력이며 native 증거가 아니다.

현재 연결 초안의 주요 role는 `object_structure`, `garment_detail`, `hand_pose`, `body_pose`, `contact_point`, `prop_placement`, `location`, `composition`, `gaze_target`, `proxemics`, `narrative_clue`, `attire_context`, `wearable_accessory`, `surface_material`, `texture`다. 이름 존재 여부만 확인했으며 실제 각 role의 subject/domain 조건과 property 의미는 별도 검토한다. 연구 중 모호한 `gaze` 제안은 실제 catalog의 `gaze_target`으로 정정했다.

완료 증거: 정본 의미·실제 source hash·owner/조건/effects closure·binding별 승인/보류. 어느 단계에서도 연구 카드 수만으로 source 자격을 승인하지 않는다.

## 7. 단계 F — source 검사와 호환 인덱스 재생성

1. 수정한 정본·binding의 실제 invariants를 먼저 검증한다. 현재 유지보수 문서의 dictionary validator와 source/index verifier를 사용한다. 실패한 source는 등록을 보류한다.
2. source의 한영·검색 텍스트·recipe가 바뀐 항목은 현재 선언된 provider/model/dimensions/recipe와 일치하는 벡터로 새로 만든다. 이전 recipe 벡터의 버전 이름만 바꾸지 않는다.
3. 재사용 벡터는 ID·전체 텍스트 hash·recipe·모델 공간·무결성이 모두 맞는 경우에만 사용한다. 변경된 텍스트의 이전 벡터를 재사용하지 않는다.
4. 동시 작업으로 source가 바뀌면 정확한 병합 source에서 다시 검증/빌드한다. index build 중 source drift가 있으면 활성화를 중단한다.
5. 현재 유지보수 절차의 `validate_photo_prompt_dictionary.py`, `build_shared_candidate_index.py --verify`, 필요 시 호환 빌드/게시 절차를 사용한다. source 게시와 sealed generation 설치·활성화는 별도 상태로 기록한다.

완료 증거: source/manifest/index hash·실제 recipe·벡터 신규/재사용 내역·전체 coverage·검증된 게시 세대. 검색 성공이나 이미지 성공은 아직 아님.

## 8. 단계 G — 실제 검색과 프롬프트 전달 검증

실제 요청→독립 기본 프롬프트→해당 슬롯 검색과 별도 주제/기본 프롬프트 검색→정본 전체 보기→선택·조건·효과 검토→composition audit의 순서를 지킨다.

- 192개 계획 사례 중 변경된 source와 관련된 cases를 실행한다. 한영 자연어 질의, 부정, 사람 없음, 전시 물건, 일반 현대 대조를 포함한다.
- 예상 CID만 찾는 검사와 사용자의 자연어를 이해하는 검사를 구별한다. CID 직접 지정·키워드 태그 노출은 자연 질의 성공이 아니다.
- 슬롯 결과와 `__request_topic__`, `__baseline_prompt__` 결과를 따로 저장한다. 단일 pooled 결과로 대체하지 않는다.
- source 조건·role fit·frozen owner/property 제약·완전 adopted 의미를 실제 pack에서 확인한다. 빈 effects·작업용 태그로 허용 범위를 우회하지 않는다.
- 신규 장르 후보가 일반 계약서·정비·옷 피팅·곡물 사진에 중세 인물·성을 강제로 도입하지 않는지 확인한다.

완료 증거: 재현 가능한 질의·receipt·실제 결과·고려/채택/거절 이유·프롬프트 literal 관계·audit. 저장된 이미지의 실제 관계는 아직 미검증이다.

## 9. 단계 H — 픽셀 검증과 게시 상태

이미지 생성이 요청되는 후속 단계에서 평가 계획의 우선 3개 독립 장면부터 생성한다. 요청/기본 프롬프트/선택 source/최종 prompt/transport/원본 이미지/review를 arm별로 보존한다. 한 장면의 국소 성공으로 전체 source나 다른 장면을 승인하지 않는다.

픽셀은 모든 채택된 필수 부품·owner·양끝·연결·상태를 같은 프레임에서 확인한다. 일부만 보이면 partial, 가려지면 UNOBSERVABLE_NOT_PASS, 안전 차단으로 이미지가 없으면 BLOCKED_UNSCORED다. 법적 신분·동의·시간·실제 수익·충성은 픽셀 PASS에 포함하지 않는다.

게시가 나중에 요청되면 명시 allowlist로 스테이징하고 source/index 검증, staged 이름·blob 비교, 보호 상태 비교, 커밋, 실제 remote SHA 확인 순으로 진행한다. 다른 작업을 섞지 않으며 전용 worktree의 정리는 원격 일치 후 수행한다. 이번 연구에서는 커밋·푸시·게시·runtime 활성화가 모두 미수행이다.

## 10. 구현 인수 기준

데이터 반영 완료는 승인된 source·binding·정확한 index 세대가 검증된 상태다. 자연어 검색 완료는 실제 질의·receipt·선택 판단까지 확인한 상태다. 이미지 실현 완료는 저장된 원본 픽셀의 전체 필수 관계가 통과한 상태다. 사용자 수용은 사용자의 판단으로 남긴다. 이 네 상태를 하나의 ‘완료’로 합치지 않는다.
