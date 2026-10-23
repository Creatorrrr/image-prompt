# 아톰펑크 데이터 반영 및 독립 이미지 테스트

상태: 데이터 등록·봉인 검색 버전 설치/활성화, 독립 3개 이미지 생성, 실제 픽셀 검토 및 유효한 성공/실패 기록의 managed 감사까지 완료했다.

## 반영 범위

- 시각 선택지 88개: 완전한 영어/한국어 장면 의미, 대상 소유자, 연결 끝점, 구성요소, 혼동 경계, 적용 조건과 효과를 유지했다.
- 문맥/구분용 진단 데이터 13개: 역사·정치·오디오·시간·정체성·동의 등 단일 정지화면으로 입증하지 못하는 주장을 보존하되 positive 검색에서 제외했다.
- 선택적 역할 바인딩 176개, 원래 키워드 경로 191개, 의미 카드 101개와 출처 53개를 연결했다.
- 기존 후보/바인딩/정책/카탈로그를 이 작업에서 덮어쓰지 않았다. 최초 등록 시점의 기존 후보 20,054개와 바인딩 14,687개 및 기존 모듈 바이트 보존 검사를 통과했다.
- 연구 원본 30개 파일의 해시가 유지됐다. 연구 메타데이터와 출처는 native qualification, 강제 프로필, 사용자 요구 또는 픽셀 입증으로 승격하지 않았다.

운영 원본: `skills/photo-prompt-image-generator/assets/photo_candidate_atompunk_20261023.json`, `photo_candidate_atompunk_bindings_20261023.json`, `photo_atompunk_semantics_20261023.json` 및 공통 corpus manifest. 규칙 설명은 `references/atompunk-semantics.md`와 maintenance 문서에 연결했다.

## 실제 검색 버전

- H-F2 generation: `478e710376544a898d6f634abba1a015f78e8a1b61932c8189bc1672abbf3c32`
- native generation: `acc673bbfea60a6d2ba17d351c99359007575260c1ea47571f133f0e87854bf3`
- store: `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`
- positive CID 19,710 / RID 19,712. 이전 검증 버전의 후보와 벡터를 보존하고 이번 시각 후보 88개의 실제 로컬 문서 벡터를 추가했다. 진단 13개는 검색 대상에 들어가지 않는다.
- 검증된 설치 부모에 이번 101개만 추가했다. 동시에 다른 작업이 수정 중인 미발행 working 후보는 설치하지 않았다. 두 neutral precore 파일의 미사용 import 정리만 명시적 allowlist로 최신 코드에 맞췄다.
- 전체 source/index/vector/code closure 검증, 배포 코드의 실제 H-F2/native validator 및 실제 recorder/NumPy 확인을 통과한 뒤 기본 버전을 활성화했다. CURRENT 포인터 쓰기는 0회다.

## 검증

- 아톰펑크 source 회귀 8개 PASS: positive/diagnostic 분리, 메타데이터 비승격, 191 경로, 소유자/관계, 4개 안테나와 방사형 램프 구별, EN/KO 경계 등.
- 설치 kernel의 topic-context/negative-policy 회귀 13개 PASS.
- 설치 validator/실제 recorder/dependencies PASS.
- raw working 전체 인덱스도 별도 staging에서 갱신/전체 검증한 뒤, 원본 source 해시가 그대로일 때만 반영했다. 후보 20,341개 / positive 19,858개 / binding 15,120개의 최종 사전 검증이 errors=[]로 통과했다. 다른 동시 신규 소스의 작성 내용은 보존했고, 설치 검색 버전은 바꾸지 않았다. 최초 외부 clockpunk 중복 dimension 오류는 다른 작성자가 해결했고, 뒤이은 stale layout 문제는 이 갱신으로 해소됐다. `working-index-adoption.json`과 `working-dictionary-validation-final.log`에 증거가 있다.

## 독립 테스트 설계

각 서브에이전트는 다른 arm, 연구 카드와 후보를 읽기 전에 자체 무작위 컨셉, 완성 장면의 baseline/core 및 픽셀 체크리스트를 동결했다. 공통 원문 요청과 정확한 이전 사용자 주제 문구만 coordinator envelope로 전달했다. 컨셉의 세부 장면은 agent-owned다. 참조 초상은 직접 확인한 얼굴/헤어 인상만 사용하며 실제 정체성·나이·국적을 추론하지 않는다.

| arm | 후보 접근 전 선택한 컨셉 | core SHA256 | 사전 핵심 검증 |
|---|---|---|---|
| A | 도로변 미래 박람회 공공 텔레보팅 부스 | `63650c11183f5df23fa31bc6eb92a57f2059d17a013c2b31512c22f2e4664fc8` | 아날로그 부스/캐노피, 부품의 같은 소유자, 손–카드–슬롯, 도로변 문맥 |
| B | 달 거주지의 아침 식사와 갤리 창 | `defb21f2996f8cfbd4143a67c2568306ee86ae306a0aec77107567a25d8b5110` | atomic-era 형태/아날로그/생활 공간, 갤리–창–달 표면, 손–컵 |
| C | 열린 달 탐사 캡슐을 들여다보는 방문자와 가이드 | `97fb96ffc26538b5575beb2ff976479120b5a71efc72a021967a4200f8c17e7f` | 캡슐–전시–계기판, 가이드의 가리킴, 방문자의 손–림 |

세 arm 모두 새 아톰펑크 소스의 실제 검색 노출을 확인했다(A 8종, B 4종, C 5종; 각 arm 내 고유 CID 수). 진단 데이터 노출은 0이다. `three-arm-source-exposure.json`에 출처 ID와 원문을 남겼다.

모든 arm은 위 generation을 명시적으로 고정한다. 검색 노출, full-source 검토, 선택적 inspiration, 실제 프롬프트 수송, 실제 이미지 생성 및 저장 픽셀을 각각 구분한다. material을 native chosen CID로 승격하지 않는다. 필수 구별 요소가 일부 가려지면 `partial_is_fail`, 보이지 않으면 `UNOBSERVABLE_NOT_PASS`다. 이미지에서 의미가 읽히더라도 실제 역사/원인/정체성/시간 연속성이나 사용자 수락은 입증하지 않는다.

## 이미지 결과

독립 서브에이전트 3개가 각각 built-in native imagegen을 1회 호출했다. 3회 모두 이미지 반환·프로젝트 저장·원본 해시 기록·직접 픽셀 확인을 완료했다. 추가 생성과 API fallback은 없다. 세 장 모두 아톰펑크 주제와 참고 얼굴/헤어 guidance가 관찰된다. 사전 세부 테스트는 각 4/5 PASS, 1개 partial FAIL이므로 전체 엄격 통과는 **0/3**이다. 세부 테스트는 agent-owned 장면 검증이며 추가 사용자 필수 요구로 승격되지 않는다.

| arm | 장면 | 새 아톰펑크 소스 노출 / 실제 프롬프트 사용 | 실제 픽셀 판정 |
|---|---|---|---|
| A | 미래 박람회 투표 부스 | 8종 / M05의 화면–하우징 경계만 부분 영감 | 4/5. 캐노피 지붕의 들린 외곽선이 상단 crop으로 확인되지 않음 |
| B | 달 거주지 아침 식사 | 4종 / 전체 대안 비교 후 baseline 유지, 48 occurrence 모두 skip | 4/5. 보조 손의 정확한 flat-palm 접촉 상태가 불명확 |
| C | 열린 달 탐사 캡슐 전시 안내 | 5종 / B09의 일반적 지지대 반복 리듬만 부분 영감 | 4/5. 방문자의 시선이 같은 계기를 향하는지 확인되지 않음 |

152개 material occurrence(48/48/56)와 각 arm 내 143개 고유 출처(45/47/51)의 조건·효과·전체 의미를 검토했다. A의 contact_point와 B의 visual_hierarchy query는 반환 0개였다. B의 경우 봉인 query에 있던 `without competing with her presence`가 installed scope projection에서 `no_independently_requested_positive_change`로 처리된 제한을 기록했고, plan을 바꾸거나 재샘플하지 않았다. 신규 시각 후보의 고유 노출은 전체 arm 합집합 16종이며, 완전한 native 소스 채택은 0이다. 부분 영감도 whole-source adoption 또는 native qualification으로 표시하지 않았다. baseline 이미지와 비교 생성한 품질 향상 실험은 수행하지 않았고, 완성 프롬프트 대안 비교와 실제 저장 픽셀 검토를 분리했다.

세 run의 최종 phase는 모두 `review_record_validated`이고 리뷰 schema 실패는 0개다. managed 신체관계 기술 판정은 A/C PASS, B FAIL(접촉/투영 2개 gate)로 유효하게 기록됐다. 사전 전체 장면 테스트의 각 partial FAIL은 별도로 그대로 유지했다. 세 run ledger 모두 현재 최신 `SKILL.md` 해시 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`와 일치한다.

부모가 저장된 세 이미지를 직접 보고 사전 체크리스트와 동결 baseline을 대조했다. B의 손 접촉은 초기 부모 예비 판정 후 정확한 `left palm rests flat on the counter` 문구와 대조해 partial FAIL로 수정했다. 초기 판정은 `parent-pixel-review.v1.json`에 보존했으며 테스트 조건 자체는 바꾸지 않았다. 최종 판정은 `parent-pixel-review.json`이다. 사용자 수락은 pending이다.

### A: 미래 박람회 투표 부스

![A 투표 부스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/atompunk-20261023-independent-a/image-attempt-1.png)

같은 부스에 속한 볼록 CRT, 2개 아날로그 계기, 회전 조절기, 점등한 amber lamp, 카드 슬롯과 궤도 장식이 함께 보인다. 카드와 손/연결된 팔 및 슬롯의 접촉도 보인다. 램프 점등은 실제 투표 선택이나 수락 인과를 입증하지 않는다. 다음 동일 의미 검증은 캐노피 바깥 윤곽이 프레임 안에 함께 보이도록 시점·프레이밍을 조정하는 것이 우선이다.

### B: 달 거주지 아침 식사

![B 달 거주지](/Users/chasoik/Projects/image-prompt/generated/images/atompunk-b-lunar-breakfast-20261023/attempt-1.png)

크림/청록 곡면 설비와 크롬, 실제 눈금/바늘 계기, 벽에 연결된 볼트형 원형 창 및 달 표면, 머그와 아침 식사 단서가 동시에 보인다. 오른손 그립은 명확하다. 반대손은 손가락이 굽고 손바닥 평면/전체 접촉이 확정되지 않으므로 해당 완전 타깃은 부분 실패다. 해부학적 결함으로 진단하지 않는다. 다음 검증은 보조 손의 평면과 접촉 경계가 읽히는 시점·순간을 확보한다.

### C: 달 탐사 캡슐 전시 안내

![C 달 탐사 캡슐](/Users/chasoik/Projects/image-prompt/generated/images/atompunk-independent-c-20261023/lunar-capsule-exhibition-attempt1.png)

원형 금속 개구부 안에 바늘 계기, 토글과 램프가 보이고, 가이드 손끝과 계기판의 연결 및 방문자의 손–림 접촉은 읽힌다. 관람객/궤도 전시물/기둥/달 경로 도상이 공공 전시장 문맥을 지지한다. 방문자 눈길은 가이드 쪽으로 읽혀 같은 계기를 함께 본다는 관계는 부분 실패다. 다음 검증은 방문자 눈의 방향과 가이드 손끝/큰 계기를 같은 관측 가능한 선상에 배치한다.

### 프롬프트와 재현 파일

실제 native-plan의 exact prompt는 `PROMPTS.md`와 `prompts/arm-{a,b,c}-native.txt`에 복사했다. `prompt-transport-summary.json`은 실제 native-plan 경로/해시, prompt 문자열 해시 및 참고 파일 해시를 보존한다.

- A run: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/atompunk-20261023-independent-a` — `independent-arm-report.md`, `artifact-index.json`, `testcase-pixel-review.json`, `image_runs.ndjson`.
- B run: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/atompunk-20261023-independent-b` — `independent-pixel-review.json`, `supplemental-review.json`, `visual-review.json` 및 workflow receipts.
- C run: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/atompunk-20261023-independent-c` — `completion_report.json`, `pre_material_pixel_review.json` 및 workflow receipts.

## 기본 검색 버전의 후속 갱신

동시 작업이 이후 기본 버전을 추가 갱신했다. 마지막 검증 snapshot은 H-F2 `86e91bb00125886973c27b8df38329c9af9cfc302d579dda1da9e3637fa63573`, native `2716f0cf11debb32ae3096dbfa130994dd270a1b01376b04b5002b4fe3deee3d`이며, code hash는 테스트 버전과 같다. 부모가 full release seal과 이번 후보/바인딩 2개 모듈의 정확한 바이트 해시 보존을 검증했다. 이번 101개/176개는 유지돼 있다. 3개 이미지 run은 기존에 명시적으로 고정한 `478e...` 세대를 계속 사용하므로 중간 default 변경으로 재검색하거나 다른 소스로 바뀌지 않았다. `current-default-verification.json`에 확인 시점과 증거를 남겼고, 이전 확인은 `.v1.json`에 보존했다.

## 실행/보존

실제 이미지 호출은 사용자 요청 범위에서 built-in imagegen을 사용한다. API fallback은 하지 않는다. 임의 차단 우회나 감사 PASS 조작은 허용하지 않는다. 실패한 시도도 보존한다.

설치된 세대, 연구 원본, 작성 소스, 독립 run, 로그와 receipts는 유지한다. 디스크 압박으로 이번 작업의 재생성 가능한 중간 복제본 약 873 MiB만 해시 allowlist를 남기고 삭제했다(`reproducible-cleanup.json`); 다른 작업/설치 세대는 삭제하지 않았다. commit/push/PR은 수행하지 않았다.
