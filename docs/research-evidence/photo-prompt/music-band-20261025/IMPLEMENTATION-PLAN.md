# 시각 의미·후보 데이터 반영 계획

현재 완료 범위는 연구와 반영 설계다. 연구 JSON을 운영 모듈에 직접 복사하지 않는다. 원문 392행을 유지하면서 가시 명제·비가시 문맥·추가 표본을 심사하고 현재 schema/qualification 경로로 변환한다.

## 먼저 반영할 범위

| 순서 | 대상 | 연구 카드 | 이유와 완료 기준 |
|---|---|---|---|
| P0-1 | 기존 원문 재사용/분기와 다의어 | existing-triage.json 9건, N02/N04/N05/N08/N10/N12/N15 | 기존 CID를 보존할 것과 새 실현을 분리. 지휘자/도체, MIDI/미디, 웨지/신발, Punk/Funk, 재즈/녹음 컴핑의 무단 의미 채택 0 |
| P0-2 | 악기 연주·접촉·지지 | A01–A32, 특히 A06–A08/A11–A21/A24–A31 | 구체 연주법·소유자·악기·손·현·활·페달 접점 보강. 기존 더블베이스 4건도 검토하되 일렉 베이스와 구별 |
| P0-3 | 제작·무대 노동 | B01–B14/C01–C14 | 화면/도면과 실물, 마이크/모니터, DI/페달, 채널/배치, 실제 단계 구분. A/B/C는 총 60개 초안이며 신규 CID 60개라는 뜻은 아님 |
| P1-1 | 복식·헤어와 장르 조건 | E01–E20/F01–F08, N12/N14 | 개별 표본을 보강한 뒤 28개 초안 심사. 하네스/악기 스트랩, 코르셋/뷔스티에, 플랫폼/웨지, 소재/반사 분리 |
| P1-2 | 합주·쇼맨십·군중 | G01–G16/H01–H04 | 다중 인물과 악기 소유·단일 마이크·지지 손·동적 프록시 구분. 운동/안전/합의를 정지 사진에서 확정하지 않음 |
| P2 | 서사·성인 표현·어두운 소재 | H05–H20, N17–N20 | 인과·시간·직무·욕망·강요·건강을 외형과 분리. 부족한 표본은 research hold 유지하며 원문 뜻을 삭제하지 않음 |

가시성이 낮다는 이유로 중요도를 낮춘 것이 아니다. 비가시 의미는 후보를 많이 만드는 대신 정확한 문맥·sense 경계로 먼저 보존한다. 카드 수는 검토 가능한 초안의 규모이고 성과 지표나 신규 레코드 할당량이 아니다.

## 반영 파일과 소유 역할

| 경로 | 반영할 내용 | 반영 조건 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_music_band_semantics_20261025.json` | 승인한 카드·문맥·키워드 sense·출처·hold의 authored metadata | 실제 적용일 suffix 재결정 가능. 연구와 runtime 상태 분리, 한영 뜻·음향/시간·성인 조건 보존 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_music_band_20261025.json` | 심사한 완전한 선택 명제만 native module/v3 후보로 작성 | 현재 validator의 실제 schema 확인. stable CID 1개 payload owner. 신규/분기/재사용 대조표 필수 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_music_band_bindings_20261025.json` | 검토한 역할 적합성만 optional binding으로 등록 | 현재 149-slot catalog의 실제 spec·owner/property로 심사. 슬롯 이름·장르 유사성으로 다중 태그하지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 확정된 모듈의 정확한 합집합 | 기존 모듈 제거·덮어쓰기 금지. manifest/개별 source 해시 동결 후 build |
| `skills/photo-prompt-image-generator/references/music-band-semantics.md` | 의미·동작·장치·장르 경계와 유지보수 안내 | 연구를 초기 프롬프트의 강제 장면 사전으로 사용하지 않음 |
| `skills/photo-prompt-image-generator/tests/test_music_band_semantics.py` | 의미 충돌·조건·소유자·개수·효과·한영·미디어 경계 회귀 | 형식만 반복하는 검사 대신 아래 실제 오류/반례를 사용 |
| 이 폴더의 후속 `integration-evidence/` | 자격·검색·전달·픽셀·설치/발행 영수증 | 이번 연구 스냅샷과 분리하고 실행한 단계만 pass로 기록 |

현재 manifest는 후보 22,899건을 포함한다. 등록된 출처 파일 121개의 해시와 음악 관련 어휘 hit 90건을 `corpus-audit.json`/`existing-records.json`에 보존했다. hit에는 실제 오탐이 포함된다. 이 수치는 실행 시점에 다시 확인한다.

## 후보 심사의 구체 순서

1. 원문 행의 전체 뜻·절·복합어를 읽고 `sense`를 정한다. 사용자가 직접 정의한 뜻과 나중에 추가한 수정을 가장 먼저 보존한다. `Kxxx → A/B/C/E/F/G/H 선택안 → Nxx 문맥 → Qxx 추가 연구`를 유지한다. 카드가 연결됐다는 이유로 원래 용어 전체가 검증됐다고 표시하지 않는다.
2. 기존 CID의 `content` 전체 positive fields·realizations·conditions·effects·provenance·binding·native evidence를 현재 상태에서 읽는다. `existing-triage.json` 9건은 제안이며 승인이 아니다. 90건 전체를 의미 심사한 것으로 확대하지 않는다.
3. 원래 의미 전체를 유지하는 재사용은 CID와 binding을 보존한다. 오른귀-케이블-수신기, 관객 쪽 마이크 등은 현재 문장 그대로 쓸 수 있는지 먼저 확인한다. 성인 손끝 후보의 adult와 현재 장면 요소 조건, 슈게이즈 후보의 `shoegaze_practice`를 삭제하지 않는다.
4. 새 손·악기·스트랩·화면·관객·인원·지지 대상이 늘면 추가 effect와 조건을 검토한다. 여러 첼로 CID를 합쳐 A26을 만들거나 MIDI 화면 노트를 더하는 것은 별도 전체 명제다. 기존 CID의 뜻을 조용히 넓히지 않는다.
5. 소유자를 명시한다. 인물의 오른손/왼손, 자기 악기, 지지 스트랩, 악기 부품, 바닥, 화면/도면/사진/거울 속 표현을 서로 다른 owner로 둔다. `part_of`, `contacts`, `supported_by`, `connects_to`, `faces`, `depicted_in`의 양끝이 사라지지 않게 한다. 단순 단어 동시출현은 관계 자격이 아니다.
6. 효과는 최종 명제 전체에서 계산·심사한다. 인물·의상·개수·접촉·지지·포즈·장면·조명·글자·표현 매체의 실제 변화가 현재 dimension/property lock과 양립해야 한다. 연구의 `proposed_slots`는 무승인 제안이다. source conditions를 binding이 완화하지 않는다.
7. exact native field-local positive anchors, source units, owner/effect 조건, 선택 RID와 역할 자격을 현행 절차로 심사한다. 연구 카드의 ID·그래프·출처 URL은 native typed fact나 qualification을 대신하지 않는다. 번역의 수·좌우·접점·선후 관계를 별도로 수동 검토한다.
8. 문맥 기록은 긍정 시각 후보에서 분리한다. 장르·학적·직무·음향·시간·건강·동의·강요·권리의 진단 기록을 optional prop 후보로 등록해 우회하지 않는다. 필요하면 현행 diagnostic 형식으로 보존하되 runtime 노출 방식은 현재 코드를 확인한다.

## 구체적인 실패 방지 항목

- A19는 **오픈 림샷**이다. 원문의 rimshot 전체를 이 좁은 접점으로 덮어쓰지 않는다. A20은 **어쿠스틱 스네어**이며 특정 전자패드에 그대로 적용하지 않는다.
- A04의 손가락 모양만으로 코드 음정을 확정하지 않는다. 표준 튜닝·현/프렛·음정이 필요하면 이를 별도 정확 실현으로 작성한다.
- A14의 4현/6현, A32의 6인 합창, H03의 현악사중주, H04의 특정 재즈 트리오는 선택한 편성이다. 일반 '베이스', '합창', '콰르텟', '트리오'에 이 구성을 강제하지 않는다.
- IEM 케이블을 다른 멤버 허리로 연결하거나 두 기타리스트의 손/악기를 교환하지 않는다. 서핑에서 손 주인·몸의 지지 부위가 가려지면 전체 관계를 통과시키지 않는다.
- 마이크 커핑은 실제 그릴을 감싼 손으로 추가 조사할 수 있으나 좋은 발성법·피드백 없음으로 설명하지 않는다. 그릴을 가리면 지향성과 피드백 조건이 달라질 수 있다는 문맥을 보존한다.
- 성인 무대 표현을 학교/나이 미확정 요청으로 자동 이전하지 않는다. 단순 복식·직무 단어에서 욕망·성적 지향·강요·동의를 추론하지 않는다. 소리·시간·정체성이 핵심이면 'still proxy'의 부분 성공을 전체 성공으로 보고하지 않는다.

## 검색 인덱스와 설치 경계

읽기 전용 `photo_installed_h_f2.py --check-runtime`는 통과했다. 실행 Python·선택 generation·실제 recorder·NumPy와 v10 새 쓰기 지원을 `runtime-check.json`에 저장했다. 이것은 **의존성과 recorder 검사**이며 최신 authored 데이터가 installed 검색에 들어 있거나 124개 카드가 검색된다는 증거가 아니다.

운영 통합 때는 `references/maintenance.md`와 `references/installed-h-f2.md`의 최신 절차 및 CLI parser를 다시 읽는다. 변경된 authored source와 정확한 합쳐진 corpus를 동결한 뒤 offline index를 생성한다. source/text recipe/provider/model/dimensions/vector integrity가 모두 일치하는 벡터만 재사용한다. 기존 native index와 installed H-only+F2 release가 별도 경계임을 유지한다.

기존 슬롯별 검색과 `__request_topic__`/`__baseline_prompt__`의 독립 검색을 함께 평가한다. 데이터 이름·최근 날짜·장르 태그를 순위 보너스나 사전 필터로 넣지 않는다. 별도 stage에서 source closure·native qualification·검색 회귀를 확인하고 code/data allowlist로 sealed release를 만든다. 설치·활성화·CURRENT·사용자 수용·발행 상태는 각각 기록한다. 실패하면 이전 sealed release를 유지하고 연구만 보존한다.

## 검증 완료 기준과 실행 순서

| 단계 | 실행할 검증 | 완료 기준 |
|---|---|---|
| R0 | 연구 구조·원문 추적·출처 연결·초안 상태·해시 | 이번 연구 validator 통과. 사실 전체 검증·native·픽셀과 별개 |
| R1 | 선택 카드의 표본 보강·한영·소유자·조건·슬롯·native 자격 | 선택한 각 source/RID와 변경 effects의 실제 근거가 모두 충족. 미충족은 보류 |
| R2 | 관련 의미/계약 회귀와 dictionary validation | 경계·소유자·조건 손실 0. 영향 있는 code만 추가 검사 |
| R3 | 합쳐진 source/index/vector closure와 sealed generation 검증 | source 해시·정확 범위 일치. 누락·차원/recipe 혼용은 실패 |
| R4 | 같은 입력을 전/후 release에서 검색·선택·전달 비교 | `EVALUATION-PLAN.md`의 사전 고정 지표를 충족. 노출과 채택을 별도 측정 |
| R5 | 실제 도구 입력·이미지 저장·관계 픽셀 평가 | 16개 prospective 사례의 모든 선택 관계/접점이 실제로 보임. 부분은 전체 pass 불가 |
| R6 | installed runtime·사용자 판단·발행·복구 | 실행된 단계별 실제 영수증과 SHA 확인. 수용은 사용자의 실제 판단 필요 |

## 변경 격리와 발행

후속 구현 시작 시 기존 dirty/untracked를 다시 조사한다. 공유 checkout에 관련 없는 수정이 많으므로 현재 작업 또는 적절한 attached worktree를 확인하고 필요하면 별도 worktree에서 구현한다. 정확한 허용 경로·기존 source 해시·새 CID/기존 CID·binding·파생 index를 대조한다. 다른 연구의 수정·삭제·실행 부산물을 포함하지 않는다.

현재 요청의 산출물은 이 연구 폴더다. 실제 source 통합·이미지 생성·설치·commit/merge/push 단계는 후속 작업의 범위와 결과로 기록한다. 여기서는 그 작업을 완료한 것으로 표시하지 않는다.
