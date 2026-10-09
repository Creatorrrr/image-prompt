# 여름 패션 데이터 반영과 독립 이미지 검증

상태: 데이터와 실제 인덱스 반영 완료. 독립 서브에이전트 3개의 실제 이미지 호출과 검토 완료. 반환 이미지 2개, 출력 차단 1개, 추가 호출 0회. 생성된 두 이미지 모두 일부 신규 구조를 충족하지만 전체 필수 조건을 모두 충족하지는 않는다.

- 원본 조사: 299개 용어 행, 118개 의미 가족, 68개 출처.
- 166개 후보 초안 중 159개 독립 가시 변형 추가, 7개 기존 의미 재사용.
- 159개 선택 후보, 159개 시각 명세, 159개 선택 번들, 469개 원본 픽셀 게이트.
- 원료/브랜드/성능/숨은 착용 등 4개 명세 가족은 자동 픽셀 후보를 만들지 않음.
- 본 반영 시점의 기존 114개 슬롯 유지. 후보 11462→11621, 시각 명세 3251→3410, 번들 1621→1780.
- 기존 후보의 의미·기존 명세·번들 보존. 7개 기존 후보에는 검토된 동등 검색 표현만 추가.
- 최신 스킬 SHA-256 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`; 미러 동일. 스킬 동작 코드는 수정하지 않음.
- actual Gemini embedding 2, 768 dimensions, batch size 1. 동일 입력 텍스트·공간에 한해 캐시 재사용. 공식 빌더가 최종 전체 행과 BM25F를 재검증함.
- 세 이미지 케이스가 사용한 고정 generation `4d983fa8c19d53c5be8f1269ef5897d9c04ae02a90ed3e3d76eff0e7e47cb756`.
- 세 이미지 케이스의 고정 source fingerprint `3627d26fe90e911e3c3ce6001eed297d98767530a3bbe2b042078ae5af1c8060`.
- 메인 적용 당시 보존 검사 9118개: 변경 손실 0. 동시 가을 패션 변경을 보존하고 매니페스트 객체를 병합함. 커밋·푸시 없음.

실행과 원본 픽셀 검증, 전반적 이미지 품질, 요청자 선호는 데이터 등록과 별도 증거다. 모든 신규 변형을 이미지로 검증했다는 뜻은 아니다.

## 확인 자료

- [원본 상세 조사](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-summer-fashion-visual-semantics-research.md)
- [초안-실제 ID 매핑](draft-to-runtime.json)
- [299개 원본 행의 가족별 적용 범위](runtime-coverage.json)
- [기존 의미 보존 검사](compiled-preservation.json)
- [메인 적용·보존 영수증](primary-application-receipt.json)
- [실제 임베딩 문맥 검색 검증](real-profile-paraphrase-check.json)
- [새 게이트·소스 스냅샷](data-ready.json)
- [185개 범위 회귀 검사 결과](scoped-tests-resolved.json)
- [최종 데이터·고정 입력·실제 호출·이미지 해시 대조](final-delivery-integrity.json)
- [동시 변경 후 현재 메인에서 수행한 추가 검사](current-source-checks.json)
- [검토에서 도출한 후속 계획](follow-up-plan.json)

## 반영 구조와 검증 범위

새 데이터는 기존 7개 의미 영역에 14개 가산 소스로 등록했다. 후보는 선택 가능한 표현이며, 시각 명세는 구성 요소와 소유자·관계를 명시한다. 번들은 같은 소유자의 여러 요소와 관계를 함께 선택하는 단위다. 일반 용어나 유사 문맥 검색으로 관련 명세가 자동 필수화되지 않으며, 번들의 연관 프로필도 선택 없이 필수 게이트로 승격되지 않는다.

| 기존 의미 영역 | 추가 후보/명세/번들 각각 | 추가 원본 픽셀 게이트 |
|---|---:|---:|
| clothing_structure | 89 | 261 |
| coverage | 9 | 27 |
| fit | 6 | 18 |
| swimwear | 21 | 61 |
| textile | 9 | 27 |
| ornament | 19 | 57 |
| style | 6 | 18 |
| 합계 | 159 | 469 |

데이터 검사에는 소유자와 문자 관계의 완전성, 기존 색/소재 속성 고정과의 충돌, 긍정/부정·완전 표현/이름만 있는 표현의 구분, 번들 구성과 관계의 누락 변이, 소스 해시와 인덱스의 일치가 포함된다. 회귀 범위는 14개 모듈의 서로 다른 185개 검사다. 첫 전체 실행의 184개가 통과했고, 격리 체크아웃에 없던 기존 가을 조사 JSON 2개 때문에 1개가 오류를 냈다. 해당 원본 증거를 그대로 복사한 뒤 같은 검사 1개를 재실행하여 통과했다. 총 실행 186회, 남은 실패 0개이며, 테스트 코드나 판정을 완화하지 않았다.

최종 전달 대조 중 작업 범위 밖 소스/테스트 20개와 파생 인덱스 2개가 이후 변경됐고, 메인의 현재 generation은 `b980b1d3f880f799b6a262bed44fc7562efeec0a5ad9841fa47ebb025c3557a8`, source fingerprint는 `3f056e6b7788b63a4c74494c7ae7663b5d79a21c608fea86c757fe80d6967bd9`로 갱신됐다. 첫 대조의 불일치는 [원본 기록](final-delivery-initial-current-drift.json)에 보존했다. 해당 변경은 덮어쓰거나 되돌리지 않았다. 이번에 적용한 비파생 파일 54개(여름 소스·증거·테스트·기존 반환 세대의 샤드)는 검토한 격리본과 같은 바이트를 유지한다.

갱신된 현재 메인에서도 여름 회귀 검사 11개를 재실행해 모두 통과했고, 사전 검증과 시각 인덱스 `--check`도 통과했다(현재 전체 명세 3686개, 정확 일치 표현 6489개). 검사의 시작과 종료 source fingerprint가 같았다. 이 추가 검사는 새로운 메인의 여름 적용 유효성 확인이며, 14개 모듈 전체를 새 버전에서 재실행했다는 뜻은 아니다. 이미지 3건은 각자 보존된 원래 고정 세대를 계속 사용하므로 이후 메인 변경으로 호출이나 픽셀 판정을 재귀속하지 않는다.

사전 조사 출처·초안·매핑·정비 이력은 배포용 런타임 데이터 밖에 둔다. 실제 섬유 성분, 브랜드 진위, UPF 등 성능, 숨은 패딩/지지·착용 상태는 사진만으로 증명하지 않는다. 해당 정보만 있는 4개 가족은 자동 픽셀 후보에서 제외했다.

## 독립 케이스

각 케이스는 OS 난수에 따라 별도 구상을 선택하고 후보를 보기 전에 고정했다. 같은 실제 사용자 요청과 참조 이미지, 같은 최신 스킬·데이터 세대를 사용한다. 참조는 얼굴·머리의 보이는 모습에만 사용하고 실제 인물의 나이·신체·생애·성격을 추정하지 않는다.

| 케이스 | 독립 복잡한 컨셉 | 신규 주제의 실제 관찰 | 전체 필수 게이트 | 실제 호출 결과 |
|---|---|---|---|---|
| A | 비 뒤 도시 카페에서 차양 물길과 의자를 동시에 정리 | 스코트 앞판·바지 구성·동일 소유자 관계 3개 충족. 버뮤다 길이는 무릎 부근에 도달하지 않음 | 7/13 충족, 부분 충족을 실패로 판정 | 1회, 이미지 반환 |
| B | 수영장 얕은 계단에서 회수한 젖은 타일을 친구에게 건네기 | 크롭 상의와 별도 하이웨이스트 하의의 관계를 후보·번들로 채택. 픽셀 검증 미실행 | 8개 미실행, 통과 0개로 기록 | 1회, 출력 moderation_blocked |
| C | 운하 옆 책가게에서 바람에 들린 지도에 돌 누르개 놓기 | 플러터 소매 3/3 충족. A라인 두 구성·같은 드레스 관계 관찰 | 7/8 충족, 부분 충족을 실패로 판정 | 1회, 이미지 반환 |

각 케이스의 새 ID 노출·선택·문자 증거·native 호출과 실제 저장 이미지의 구성 요소/소유자/연결 끝점을 별도로 확인한다. 가려진 끝점·부분 충족은 통과로 계산하지 않는다.

모든 케이스의 최종 합성 감사와 runtime 감사는 통과했다. 원본 이미지의 관찰 판정은 별도 기록이며, 메타데이터 감사의 통과로 대체하지 않았다. 두 반환 이미지의 공식 검토 기록은 유효하고 기술 자격은 실패다. 사용자 수용은 아직 확인되지 않았다.

### A: 카페

신규 선택은 `bundle:suf_sf073_v1_bundle` 스코트와 `visual-concept:suf_sf069_v1` 버뮤다다. 기존 `sheer_garment_optical_layering`도 명시적으로 선택했다. 스코트는 앞 겹침판과 두 바지 밑단, 같은 허리 소유 관계가 원본 크롭에 보인다. 그러나 바지 밑단은 허벅지 중간에 머물러 버뮤다의 무릎 부근 길이·밑단-무릎 관계 2개 게이트가 실패했다.

줄무늬 셔츠의 연속 직물 표면과 옷의 경계는 읽히지만, 같은 직물 면을 통과해 안쪽 크로셰의 경계가 보인다는 증거는 부족하다. 열린 앞섶이나 크로셰 구멍으로 안쪽이 보이는 것은 선택한 셔츠 면의 투과 증거가 아니다. 시어의 첫 인지·같은 면의 투과·밀도-투과 관계 3개가 실패했고, 투과를 확인할 수 없는 부분은 `UNOBSERVABLE_NOT_PASS`로 보존했다.

차양 고리와 의자 난간의 그립, 발의 지면 지지, 의자 앞 다리가 들린 상태는 보인다. 지정한 인물 기준 왼손-고리/오른손-의자 역할은 반대로 생성되어 접촉 동작의 정확성이 실패했다. 이는 해부학 결함 판정이 아니다. 전체 13개 게이트 중 7개 통과·6개 실패다. 스코트 번들 관찰 3개는 이 13개의 별도 게이트가 아니며 별도로 기록한다.

- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/final-prompt-en.txt)
- [원본 이미지](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/results/final.png)
- [케이스 요약](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/case-summary.json)
- [픽셀 검토](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/review.md)

### B: 수영장

신규 선택은 `slot:garment_detail:suf_sf002_v2_candidate`와 `bundle:suf_sf002_v2_bundle`이다. 동일한 전경 인물의 짧은 외투 밑단과 별도 하이웨이스트 하의의 관계를 최종 프롬프트에 명시했다. 친구의 수영복 등판과 스트랩은 별도 저작 요소이며, 주인공에 귀속된 신규 후보를 친구 옷으로 치환하지 않았다. 이 팩에서는 신규 `suf_` 시각 프로필이 노출되지 않았고 연관 프로필을 강제 선택하지 않았다.

실제 호출은 HTTP 400, `moderation_blocked`, 출력 단계, `sexual` 분류로 끝났다. request ID는 `b081484d-123e-49ac-b89d-1ea53be675b2`다. 반환 이미지가 없으므로 필수 픽셀 게이트 8개와 신규 번들 관찰 4개는 모두 `NOT_RUN_NOT_PASS`다. 차단 문자열을 그대로 보존했고 재시도나 CLI 우회 호출은 수행하지 않았다. 제공자 분류는 실제 인물의 나이나 이미지 품질 판정으로 해석하지 않는다.

사용한 [photo-prompt-image-generator 스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 [런타임 규칙](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/image-runtime.md:54)은 “Explicit moderation blocks stop unchanged retries.”라고 명시한다. 이 제공자 오류가 명시적인 출력 차단이므로 같은 요청의 자동 재호출을 중단했다.

- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_b/final-prompt.txt)
- [케이스 요약](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_b/case-summary.json)
- [검토와 차단 기록](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_b/review.md)
- [원본 오류 증거](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_b/native-error-evidence.json)

### C: 책가게

신규 선택은 `visual-concept:suf_sf032_v1` 플러터 소매와 `bundle:suf_sf058_v2_bundle` A라인이다. 중복되는 일반 후보 `slot:wardrobe_style:suf_sf058_v2_candidate`는 노출됐지만 선택하지 않았다. 어깨에서 이어지는 소매와 곡선으로 벌어진 자유 가장자리, 위팔과 떨어진 공간이 같은 드레스에 보여 신규 소매 3개 게이트가 모두 통과했다. 드레스 옆선이 밑단 쪽으로 넓어지는 두 구성·관계도 원본에서 관찰됐다.

두 손·돌·지도 접촉은 일관되지만, 지정한 인물 기준 왼손-지도 누르기/오른손-돌 잡기 역할은 반대로 생성됐다. 전체 8개 필수 게이트 중 접촉 정확성 1개가 실패했다. 별도 저작 관찰 12개 중 8개는 충족했고 가방 좌우·지도 방향 시선·손 역할·두 신발의 뒤꿈치 관찰이 미충족이다. 뒤꿈치의 가려진 부분은 통과로 계산하지 않았다.

- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/final-prompt.txt)
- [실제 runtime 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/final-runtime-prompt.txt)
- [원본 이미지](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/generated_images/case-c-canal-bookstall.png)
- [케이스 요약](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/case-summary.json)
- [픽셀 검토](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/review.md)

## 통합 판정과 후속 반영 계획

실제 도구 호출 3회에서 이미지 2개가 반환됐고 1개는 출력 차단됐다. 생성 이미지의 필수 게이트는 합계 21개 중 14개 충족·7개 실패이며, B의 8개는 미실행이다. 케이스 전체 조건의 완전 통과는 0개다. 신규 데이터에 속한 선택 프로필의 직접 픽셀 게이트 6개 중 4개가 충족됐고, 선택한 스코트·A라인 번들의 구성/관계도 관찰됐다. 이는 선택한 소수 변형에 대한 결과이며 신규 159개 변형·469개 게이트 전체를 검증한 결과가 아니다.

코디와 장소, 인물의 얼굴·머리 참고는 두 사진에서 대체로 일관되게 읽힌다. 참조 보존은 눈으로 확인한 가시 모습의 판단이며 동일 인물 인증이나 신체 유사성의 정량 검증은 아니다. 한 장의 사진에서 바람·유체의 동적 원인을 확정하지 않으며, 사진에 보이는 결과·접촉만 판정한다. 주 에이전트도 A/C 원본과 주요 원본 크롭을 독립적으로 확인했고, 길이·투과 부족과 손 역할의 반전 판정에 동의한다.

다음 계획은 이번 실패를 성공으로 재분류하지 않고 별도 실패 사례로 재사용한다. 현재 스킬 데이터의 고정 버전과 의미를 검토 도중 수정하지 않았다.

| 우선순위 | 관찰된 공백 | 다음 반영/검증 | 통과 기준 |
|---|---|---|---|
| P1 | 스코트 결합에서 버뮤다 밑단이 짧아짐 | 현재 무릎 랜드마크 게이트 유지. 버뮤다 단독·스코트 단독·결합을 나란히 검증할 대조 케이스 마련 | 두 바지 밑단과 같은 인물의 무릎이 한 원본에서 보이고 무릎 부근 관계 충족 |
| P1 | 열린 앞섶을 투과처럼 오인할 가능성 | 연속 직물 면·안쪽 불투명 층·그 경계의 통과 경로를 분리한 대조 케이스와 실패 크롭 사용 | 동일 셔츠 면을 통한 안쪽 경계와 더 조밀한 접힘의 투과 차이가 원본에서 확인됨 |
| P1 | A/C의 인물 기준 좌우 역할 반전 | 소유자→어깨→팔→손→물체 끝점을 보존한 양방향 동작 케이스로 접촉 검증 보강 | 지정한 왼손/오른손의 물체 역할과 실제 접촉이 모두 일치 |
| P2 | B의 신규 시각 프로필 미노출 | 고정 코어 그대로의 검색 로그와 별도 한/영 문맥 질의를 비교. 후보와 연관 프로필의 선택 경로를 각각 점검 | 관련 프로필이 선택 가능한 위치에 노출되고 이름만 있는 입력은 필수 활성화하지 않음 |
| P2 | B의 출력 차단으로 픽셀 검증 공백 | 차단 영수증을 유지. 의미 변경이 필요한 새 검증은 요청자가 새 범위를 명시한 별도 실행으로 관리 | 제공자가 수용한 실제 이미지에 대해서만 검증 시작. 현재 차단 건은 계속 미실행 |
| P2 | 소수 변형만 실제 생성으로 검증됨 | 조사에서 정한 18개 대표 검증 그룹으로 확장하고 구성·관계·소유자 혼동을 우선 배치 | 데이터/검색/프롬프트/원본 픽셀/사용자 수용 상태를 각각 집계 |

개별 에이전트의 ledger와 공식 manifest는 각 케이스 폴더에 보존했다. Manifest의 독립성·스킬·소스 정보는 실제 ledger 행에 별도 저작 provenance를 연결한 것이며 추가 이미지 호출이 아니다. 원본 파일 해시는 [최종 대조 기록](final-delivery-integrity.json)에서 확인할 수 있다.
