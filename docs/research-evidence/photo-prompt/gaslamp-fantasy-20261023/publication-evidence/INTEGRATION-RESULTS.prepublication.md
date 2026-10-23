# Gaslamp Fantasy 반영 및 독립 이미지 검증

2026-10-23. 이 문서는 앞선 연구 원본의 `PLAN_NOT_APPLIED` 상태를 덮어쓰지 않는 후속 실행 기록이다. 데이터 등록·설치 활성화, 고정 질의 검색, 독립 에이전트 3개의 실제 이미지 생성·픽셀 검토를 완료했다. 장르 가시성은 3/3, 엄격한 전체 관계 충족은 0/3이다.

## 실제 반영

- 의미 카드 113개, 원 대화의 키워드 경로 217개, 가시 성분/관계 검사점 445개.
- 신규 완전한 한영 시각 후보 72개와 선택적 슬롯 연결 144개.
- 양의 시각 검색에서 제외하는 진단 35개: 문맥 34개와 개별 유물 검토가 필요한 골상학 모형 1개.
- 기존 후보 6개 재사용: 호출 벨, 버슬, 모발 로켓, 도식/주석이 있는 펼친 책, 인간/비인간의 공유 양피지, 손목 커프와 의자 고정점.
- 기존 source와의 연결은 각 source의 완전한 조건/효과/표현을 따른다. 원 연구 초안의 모든 한정어가 재사용 source에 있다는 뜻은 아니다. 모발 로켓의 유리, 벨의 특정 레버/스프링 등 미포함 한정어를 소급 추가하지 않았다.

실제 파일은 [의미 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_gaslamp_fantasy_semantics_20261023.json), [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_gaslamp_fantasy_20261023.json), [슬롯 연결](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_gaslamp_fantasy_bindings_20261023.json)이다. 후보/연결 모듈은 실제 manifest에 등록했다. 각 새 후보는 소유자·접점·매체·혼동 경계·출처 범위·주장 한계를 함께 가진다.

장르명은 가스등·안개·영국·특정 복식·고어·성적 의미를 자동 강제하지 않는다. 가스등과 gaslighting, 버슬과 시장의 bustle, 방문 명함과 플레잉 카드, 맨틀과 노출 불꽃, 실제 인화물과 그 안의 상을 구분한다. 물질/의학/법률/계급/동의/생사/시간/초자연 원인은 외형만으로 확정하지 않는다.

## 의미와 실행의 경계

슬롯 연결 144개는 후보 제안용 presentation tag이며 역할 승인/접촉 증명이 아니다. 예컨대 흡혈귀의 송곳니가 목 가까이에 있다는 문장은 실제 접촉을 증명하지 않고, 손에 든 렌즈가 몸에 착용되었다는 뜻도 아니다. 전체 source 의미와 current 역할 정의가 맞는지 선택 시 검토해야 한다.

새 자료는 검색·저술을 위한 source 등록이다. 연구 그래프/출처/슬롯 태그는 typed native fact, owner permission 또는 `native_approval`을 부여하지 않는다. native 자격은 `not_qualified`로 유지했다. 실제 검색 노출, 전체 source의 호환성, 최종 프롬프트, 도구 입력과 저장된 픽셀을 별도로 검증한다.

[소스 검증](integration-evidence/source-validation.json), [항목별 채택/재사용 판단](integration-evidence/adoption-review.json), [기존 설치본 보존 검증](integration-evidence/maintenance/canonical-source-validation.json)을 남겼다. 신규 동의어만 나열한 자료가 아니라 완전한 가시 명제와 소유자/관계를 등록했다.

공용 작업 폴더에서는 다른 작업의 source 수정이 함께 진행 중이다. 루트 dictionary/index 검사는 `layout source/space mismatch`를 보고했다. 공용 인덱스를 덮어써 통과로 포장하지 않고, 기존 설치본의 20,329개 후보를 그대로 보존한 별도 source/index에서 검증한다. 자체 변경 직후 기존 후보/연결/catalog/policy 불변을 확인했으며, 뒤이어 생긴 타 작업의 변경은 별도 snapshot으로 남긴다.

## 독립성 및 참조 범위

코디네이터가 실제 사용자 문장과 앞선 실제 사용자 문장의 `Gaslamp Fantasy` 지시 관계를 동결한 뒤, 대화 이력 없이 시작한 독립 에이전트 정확히 3개에 전달했다. 얼굴/헤어 참조 범위를 기록했으며 실제 인물의 신원·나이·성격을 이미지에서 추정하지 않았다. 의상/배경/직무/사건은 창작자의 선택이다.

세 에이전트는 최신 `SKILL.md`(SHA-256 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`)와 neutral precore만 읽어 기본 프롬프트를 독립 동결했다. 후보·연구 메뉴·다른 arm의 프롬프트는 동결 전에 제공하지 않았다. 설정은 saved defaults `sensual=1`, `fetish=0`, `surreal=0`, `creativity=1`이며 사용자 설정을 날조하지 않았다. [원문/이미지 해시와 배정](integration-evidence/request-context/coordinator-bindings.json), [독립 core 동결](integration-evidence/independent-core-freezes.json)을 남겼다.

| Arm | 독립 선택 컨셉 | 결과 전 동결한 핵심 가시 관계 |
|---|---|---|
| A | 운하 다리에서 밤의 가스등 공공 설비 점검 | 인물/밸브 캐비닛/배관/옅은 영체/가스등의 경계와 연결 |
| B | 심령 장치 수리공방의 유리 종 | 유리 안 반투명 손과 바깥 수리공의 손끝, 유리 양면의 같은 지점, 균열/서리 |
| C | 철도 후원자의 응접실에서 통행증 교섭 | 통행증의 왁스 봉인에서 상대의 인장 반지까지 이어진 광선 실의 양끝 |

세 컨셉의 창작 영역은 무작위 배정했다. 개별 에이전트가 자신의 seed로 구체 장면을 정했다. 이 배정과 세부 staging은 requester lock이 아니다. 세 컨셉은 데이터 유무만 바꾼 A/B 실험이 아니므로 결과 차이를 데이터의 인과 효과로 주장하지 않는다.

## 판정 규칙

`partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 적용한다. 부분 성분이나 분위기가 맞아도 핵심 관계의 양끝/경계/연속성이 보이지 않으면 전체 통과가 아니다. 생성되지 않은 시도는 픽셀 점수가 없으며, 프롬프트 감사 PASS는 이미지 PASS가 아니다. 사용자 판단은 실제 사용자 답변 전까지 pending이다.

검색은 기존 151사례의 한영 질의 302개와 별도 장면 표현 12쌍 24개, 총 326개를 결과 확인 전에 고정했다. 새 표현의 작성자는 연구를 보았으므로 독립 blind holdout이라고 부르지 않는다. source가 없는 문맥/보류 사례를 검색 recall의 유효 gold나 픽셀 성공으로 계산하지 않는다.

## 실행 결과

설치·deployed 검증과 기본 selector 활성화는 PASS. H-F2 generation은 `2aaccb50dfc6c5f6b3d05477c5e1ad5b9f2dac1c66105308d1b238745415941a`, native generation은 `60c4745d6dca3b92d86646cfc86062daa326e6f96c2def8347afbfa549413f04`이다. 양의 CID 19,918개와 실제 RID 문서 19,920개를 포함한다. 기존 H-F2 문서 벡터 19,848개를 바이트 그대로 재사용했고 72개의 새 문서만 해당 recipe로 임베딩했다. 기존 native CURRENT에는 쓰지 않았다. [설치/활성화 결과](integration-evidence/maintenance/install-active.json), [빌드 결과](integration-evidence/maintenance/successor.json).

세 arm은 이 exact generation/store로 고정했고 최초 검색이 모두 완료되었다. A와 B는 각 4질의×8건을 받았다. C는 접점 0건, 시대 8건, 주제 8건, 기본 장면 1건을 받았으며 빈 슬롯을 다른 후보로 채우거나 다시 검색하지 않았다.

| Arm | 새 source 노출 | 최종 저술에서의 범위 |
|---|---|---|
| A | G03 가시 버너/불꽃/유리 하우징, G106 영체 노동자/주전자/컵 | G03에서 일반적인 버너/불꽃/하우징 구조를 참고한 국소 명시. native 후보 채택 아님. G106 제외. |
| B | G19 수집장/표본/라벨, G106 영체 노동자/주전자/컵 | 둘 다 전체 관계가 기존 장면과 맞지 않아 제외. 독립 baseline 유지. |
| C | G79 두 성인의 가까운 얼굴 | 현재 참조가 성인 선언/접근 관계의 권한을 공급하지 않아 제외. |

[실제 노출 A](integration-evidence/arm-a-new-source-exposure.json), [B](integration-evidence/arm-b-new-source-exposure.json), [C](integration-evidence/arm-c-new-source-exposure.json). 노출은 source 호환성이나 native 채택의 증거가 아니다. 특히 B/C는 새 source를 쓰지 않으므로 이후 이미지에서 장르가 보여도 신규 데이터의 인과 효과로 해석하지 않는다.

실행 연결 중단으로 미완료 감사/대량 질의 프로세스가 사라진 일을 기록했다. core·query·pack·seed·prompt를 바꾸지 않고 미완료 검증만 재개한다. [실행 기록](integration-evidence/maintenance/resource-scheduling.json).

### 고정 질의 검색 결과

326개 질의의 full positive pool 검색과 이전 버전 144개 대조 질의를 실제 계산했다. 같은 로컬 임베딩 실행 증거와 기존 production kernel을 사용했다. 두 큰 인덱스를 동시에 메모리에 보유하지 않도록 프로세스를 나눴으며 검색식·source·벡터·질의·gold·정책은 바꾸지 않았다.

| 원래 동결한 양의 split | 등록된 가시 target 질의 | top8 | top32 |
|---|---:|---:|---:|
| development | 156 | 154 | 156 |
| paraphrase_probe | 16 | 14 | 16 |
| new_scene_phrasing | 24 | 23 | 24 |
| 합계 | 196 | 191 (97.45%) | 196 (100%) |

이는 전체 풀의 target 순위이며 실제 arm의 무작위 8개 표본에 항상 포함된다는 뜻이 아니다. 개발/연구를 본 작성자의 질의이며 blind holdout도 아니다. G70 보류 질의 두 개는 유효 가시 target이 없어 분모에서 제외했다.

상위8 밖인 다섯 질의를 결과에 맞춰 고치지 않았다: G28 버슬(한14위/영10위), G42 사진 매체 경계 안의 이중상(한15위), G56 공유 양피지 양끝(한15위), G61 거울 속 인물 부재(한22위). 다음 개선은 한국어 관계/매체 표현을 별도 새 동결 질의로 검증하는 단계다.

경계 84개·비시각 28개·일반 16개는 단순 gold-CID 노출 순위로 의미 정합성이나 안전한 채택을 통과시킬 수 없다. 비시각 질의는 `BLOCKED_UNSCORED`를 유지한다. 이전 top8 집합과의 평균 중복은 일반 질의7.875/8, 경계7.595/8, 비시각7.75/8이었다. 이것은 회귀 관찰 수치이며 모든 기존 의미/픽셀 동작의 무회귀 증명이 아니다.

[전체 질의/순위](integration-evidence/maintenance/retrieval-qualification.json), [분모/누락/대조 분석](integration-evidence/maintenance/retrieval-analysis.json), [실행 방식 변경 기록](integration-evidence/maintenance/probe-orchestration-review.json).

대형 임시 build/source/store 복사본 약2.05GB는 삭제하지 않고 저장소 밖 캐시에 옮겼다. 설치 runtime은 그대로이며 [캐시 위치/이동 기록](integration-evidence/maintenance/build-cache-archive.json)을 남겼다.

### 실제 생성 원본과 픽셀 관찰

정확히 3개 독립 에이전트가 첨부 참조로 각각 built-in image 도구를 1회 호출했다. 세 원본을 코디네이터도 직접 열어 확인했다. 장르 가시성은 3/3이며, 사전 전체 관계 기준은 0/3이다. 실패한 원본을 보존했으며 추가 생성/유리한 결과의 재선택은 하지 않았다.

| Arm | 생성·참조·장르 | 엄격한 전체 판정 | 실제 미충족 |
|---|---|---|---|
| A 가스등 점검 | 1회 생성, 얼굴/헤어 참조와 시대 도시/영체 확인 | FAIL | 왼손이 열린 문 가장자리 대신 고정 덮개에 놓임. 덮개가 배관/영체 경로 일부를 가려 전체 연속성은 UNOBSERVABLE_NOT_PASS. |
| B 영혼종 수리 | 1회 생성, 시대 공방/유리 종/내부 손/서리 확인 | FAIL | 밝은 접점이 두 손끝과 유리벽 마지막 윤곽을 가려 같은 점에서의 양면 접촉을 입증하지 못함. |
| C 통행증 교섭 | 1회 생성, 시대 응접실/문서 교환/빛의 실 확인 | FAIL | 실은 붉은 봉인에서 연속되지만 윗끝이 지정한 인장 반지 금속 대신 인접 손가락에 닿아 보임. 가까운 대상은 지정 대상과 같지 않음. |

세 실행 모두 compose/runtime/native-plan 감사 PASS, 실제 호출1회/ledger1행, 최종 `review_record_validated`다. 리뷰 기록 검사는 record_valid=true이며 이미지의 technical qualification은 모두 fail이다. 생성 status=success는 도구 출력 성공이며 픽셀 통과를 뜻하지 않는다. [최종 3-arm 검증표](integration-evidence/FINAL-TEST-MATRIX.json).

사진 전체의 미감·참조 외형·장르 표현은 관찰했지만 정확한 관계가 모두 구현됐다는 판정으로 확대하지 않았다. 신원·실제 나이·직업·연료 성분·법적 합의·실제 초자연 원인·시간상의 인과는 이미지에서 확정하지 않는다. 사용자 수용 판단은 pending이다.

A에서 참고한 G03의 유리 하우징/내부 버너/노출 불꽃 및 두 관계, 총5개 검사점은 보인다. 이는 일반적인 source-informed 표현 관찰이며 전체 native source 승인이나 다른 후보의 성공을 부여하지 않는다. B/C는 신규 source 최종 사용0이므로 주제 재현 테스트와 신규 자료의 인과 효과를 구분한다. 모든 신규 source의 native_approval=false, native_qualification=not_qualified를 유지한다.

A의 코디네이터 최초 연속성 판정은 가시 연결 형태를 넓게 인정했으나, 원본의 덮개 가림을 다시 확인해 UNOBSERVABLE_NOT_PASS로 정정했다. 이전 판정과 수정 이유를 삭제하지 않았다. [코디네이터 원본 픽셀 검토](integration-evidence/coordinator-pixel-review.json), [생성 전 판정 입력](integration-evidence/pixel-test-inputs.json).

| Arm | 최종 프롬프트 | 원본 이미지 | 세부 판정 |
|---|---|---|---|
| A | [prompt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-a-v3/final-prompt.txt) | [1024×1536 PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-a-v3/results/native-original.png) | [agent 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-a-v3/arm-report.md) |
| B | [prompt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-b/final-prompt.txt) | [1237×1272 PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-b/images/spirit-bell.png) | [agent 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-b/arm-report.json) |
| C | [prompt](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-c-neutral-rebuild/final-prompt.txt) | [1312×1199 PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-c-neutral-rebuild/generated-image.png) | [agent 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/gaslamp-20261023-c-neutral-rebuild/final-summary.json) |

### 관찰 결과의 후속 반영 계획

현재 source/index와 실패 원본은 동결한다. 아래는 이번 점수를 고치는 재시도가 아니라 별도 사례로 검증할 후속 계획이다.

1. **가림/소유자**: A의 고정 덮개와 열린 문을 분명히 분리하고 왼손이 잡을 문 모서리를 카메라 쪽으로 배치한다. 배관과 영체의 전 구간을 가리는 구조물이 없는 시점을 새 사례에서 비교한다.
2. **유리 경계/공동 접점**: B의 손끝·유리벽 경계가 보존되도록 접점 발광의 밝기와 면적을 줄이고 두 손끝의 외곽선과 유리면을 같은 초점면에서 보여 준다. 서리만 보이는 결과를 양면 접촉 성공으로 계산하지 않는다.
3. **지정 종점**: C의 반지 금속 베젤을 손가락 끝과 분리해 보여 주고, 실의 끝이 베젤에 닿는 경계를 새 사례의 필수 가시 항목으로 둔다. 반지 근처의 피부에 닿는 결과는 계속 실패다.
4. **검색 공백**: 상위8 밖에 남은 다섯 양의 질의와 C contact_point의 반환0을 후속 검토 대상으로 둔다. 한국어의 뒤/앞, 매체 경계, 두 소유자/한 매체, 거울 속 부재를 완전한 명제로 보강한다. 새 출처/후보가 필요하면 기존 full source 조건/효과를 분해해 빌려 쓰지 않고 별도 검토하며, 넓은 장르명에 수동 boost를 걸지 않는다.
5. **범위와 자격**: 현재 세 표본은 한낮·비가스등 Gaslamp 변형을 픽셀 검증하지 않았다. 이 변형을 별도 새 테스트로 만들고, 연구를 보지 않은 작성자의 질의를 결과 전에 동결한다. 72개 신규 후보의 개별 native 자격은 complete source·소유자/관계·허용 조건·runtime·실제 픽셀 증거를 각각 갖춘 뒤 별도 심사한다.

작업 소스와 기본 selector의 [최종 상태/해시](integration-evidence/final-source-state.json)를 기록했다. 공용 dirty checkout 전체의 루트 index는 source/layout 불일치 상태이며 이번 스킬 경로는 별도 검증한 설치 generation을 사용한다. commit/push는 요청되지 않았고 수행하지 않았다.
