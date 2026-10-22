# 메타픽션 실존공포 LitRPG 데이터 반영과 이미지 검증

시각 후보 64개, 맥락 진단 10개, 키워드 경로 130개를 작업 사전에 반영하고, 후보 원문과 연결을 설치된 H-F2 검색 버전에 반영했다. 한국어·영어 검색 48개와 인덱스·설치 검증을 마쳤다. 세 독립 에이전트가 네이티브 이미지 생성을 각각 1회 실행해 2장이 반환됐고 1건은 출력 안전 검사에서 차단됐다. 반환된 두 장에서 핵심 주제 관계를 확인했지만, 두 테스트 모두 지정한 손의 좌우가 뒤바뀌어 전체 고정 기준은 부분 구현이다.

## 반영한 데이터

| 항목 | 반영 결과 | 적용 범위 |
| --- | ---: | --- |
| 완결된 시각 후보 | 64개 | 단일 프레임 35개, 서사적 상태의 시각적 비유 28개, 명시적인 3패널 시퀀스 1개 |
| 맥락 진단 | 10개 | 의식, 동일성, 동의, 자유의지, 임상 의미, 시간·인과 등의 해석 경계. 양성 시각 검색에서 제외 |
| 키워드 경로 | 130개 | 기존 용어·창작용 표현의 구분과 원래 순서를 보존 |
| 선택적 슬롯 연결 | 128개 | 36개 기존 슬롯에 연결. 슬롯 사전과 정책은 유지 |
| 검토 항목 | 549개 | 소유자·구성 요소·방향 관계의 동시 가시성을 점검하는 연구 메타데이터 |

시각 후보는 재현의 경계와 재귀, 문서와 기록의 불일치, 동일성과 복제, 물질화된 게임 규칙, 선택과 통제, 세계의 경계와 시간의 흔적, 신체와 시스템, 작가·관객·인물 관계의 여덟 묶음에 각각 8개씩 추가했다. 각 후보는 영문·국문 전체 문장, 관계의 양 끝점, 수와 상태, 출처, 혼동 경계와 입증할 수 없는 주장을 함께 보존한다.

장르명이나 별칭은 선택 가능한 자료를 발견하는 데 쓰인다. 책·상태창·어두운 조명 하나로 장르가 구현됐다고 판정하지 않으며, 소유자 그래프와 연구 게이트가 native 사실·권한·역할 승인으로 바뀌지도 않는다. F01은 3패널 시퀀스다. 한 장의 정지 화면을 시간 되돌림의 증거로 취급하지 않는다.

### 운영 파일

- [시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_metafiction_existential_litrpg_semantics_20261022.json)
- [후보 원문](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_metafiction_existential_litrpg_20261022.json)
- [슬롯 연결](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_metafiction_existential_litrpg_bindings_20261022.json)
- [의미와 적용 경계](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/metafiction-existential-litrpg-semantics.md)

기존 작업 원문 후보 19,727개와 연결 14,118개를 유지했다. 반영 후 작업 사전은 후보 19,801개, 연결 14,246개다. 설치 후속 버전은 초기 설치본 이후 다른 작업이 추가한 168개와 기존 원문 수정 6개도 현재 작업 폴더의 값 그대로 보존한다. 이번 주제의 추가량은 74개이며, 병행 주제의 이미지 품질을 이 테스트로 승인하지 않는다.

## 데이터와 검색 검증

작업용·설치용 인덱스의 원문, 전역 통계, 벡터, 페이로드와 연결 검증이 통과했다. 최종 사전 검사는 오류 0개다. 설치된 기록기는 H-F2 v2와 v10 기록을 지원하며, native CURRENT 파일의 해시는 유지됐다. 운영 검색 코드와 임베딩 공간도 유지했다.

| 검사 | 결과 |
| --- | --- |
| 원문과 기존 연결 보존 | 통과 |
| 작업용 인덱스 전체 검증 | 통과 |
| 설치용 인덱스 전체 검증 | 통과 |
| H-F2 봉인과 설치 검증 | 통과 |
| 설치된 Python·NumPy·기록기 점검 | 통과 |
| native CURRENT 유지 | 통과 |

개발용 8개 장면과 경계 8개, 일반 장면 4개, 비시각적 주장 4개를 각각 한국어·영어로 검색했다. 기존·새 버전에서 총 96회 검색했으며, 새 버전의 개발용 쿼리 16개 모두 목표 후보가 상위 10개에 나왔다.

| 쿼리 묶음 | 쿼리 수 | 새 후보의 상위 10개 노출 |
| --- | ---: | ---: |
| 원문을 바탕으로 만든 개발용 장면 | 16 | 목표 후보 16개 모두 |
| 의미 경계 통제 | 16 | 4개 쿼리 |
| 일반 장면 통제 | 8 | 0개 쿼리 |
| 비시각적 주장 통제 | 8 | 3개 쿼리 |

통제 쿼리의 노출 7건은 [개별 의미 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/control-exposure-review.json)에 기록했다. 예를 들어 문이 합류하는 구조는 평범한 건축일 수도 있고, 같은 A7 태그는 수적 동일성이나 부활을 증명하지 않는다. 검색 노출은 자동 채택이나 주제 입증이 아니며, 선택할 때 전체 원문과 현재 장면의 관계를 별도로 검토한다.

이 검색은 원문을 바탕으로 만든 개발·통제 검사다. 독립적인 일반화 평가나 이미지 품질의 인과적 개선율은 아니다. 기존 124개 리서치 케이스의 NOT_RUN 기록은 변경하지 않았으며, 이번에 실행한 24개 케이스와 [48개 쿼리 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/retrieval-qualification.json)를 구분했다.

## 독립 이미지 테스트 설계

세 에이전트는 다른 에이전트나 후보 자료를 보기 전에 서로 다른 컨셉과 기본 프롬프트, 판정 기준을 고정했다. 후보 접근 전에는 검색 슬롯과 쿼리도 봉인했다. 모두 같은 사용자 요청과 첨부 참조를 사용했으며, 컨셉의 구체적인 소품과 연출은 에이전트가 독립적으로 작성했다.

| 테스트 | 랜덤 seed | 컨셉 | 원본 픽셀에서 검사할 관계 |
| --- | --- | --- | --- |
| 1 | 7884083814177649068 | 삭제선이 출구로 이어지는 심야 교정실 | 원고와 실제 공간의 경계, 삭제된 경로에 대한 반응, 인물과 연결된 게임 자원 |
| 2 | 4911031398887879632 | 비활성화된 이동 명령에 손이 붙잡힌 페리 개찰구 | 실제 손목과 평면 명령 타일의 연속 경계, 선택 상태와 저항, 같은 인물의 표현 |
| 3 | 2827595675329473862 | 얼굴 기록이 소실되는 극장 물품보관대 | 현재 장면을 담는 재귀 기록, 같은 얼굴 기록의 소실, 해당 기록의 게임 상태·복원 UI |

각 에이전트는 검색된 전체 자료를 검토하고, 후보별 사용·비사용과 기본 프롬프트 대비 대안을 기록한 뒤 이미지 생성 전 감사를 수행한다. 참조 JPEG는 네이티브 도구의 실제 이미지 입력으로 전달한다. 한 테스트당 이미지 호출은 1회다. 결과가 일부만 보이면 부분 구현으로, 보이지 않으면 비관측으로 판정한다. 실제 의식, 진짜 자유의지, 부활 전후의 동일성, 기억 소실과 과거 인과는 정지 화면의 입증 대상에 넣지 않는다.

최신 작업 스킬의 고정 설정은 sensual 1, fetish 0, creativity 1, surreal 0이다. 사용자가 요청한 주제와 실제 참조 입력을 유지하며 임의의 배제문은 추가하지 않는다.

### 독립 테스트에서 실제 반환된 자료

| 테스트 | 전체 소스 수 | 쿼리별 반환 합계 | 이번 신규 후보 |
| --- | ---: | ---: | --- |
| 1 | 38 | 40 | 0개 |
| 2 | 23 | 24 | A01·A02·G03, 3개 |
| 3 | 30 | 32 | A01·A02·B04·D01·H08, 5개 |

세 테스트 모두 발급된 자료의 첫 페이지에서 전체 소스가 표시된 것을 확인했다. 동일 소스가 다른 쿼리에서 반환된 경우에는 각 occurrence를 따로 검토한다. 신규 후보는 세 테스트를 합쳐 서로 다른 6개가 노출됐다. 1번은 신규 후보가 반환되지 않았으므로 그 이미지가 주제를 잘 표현하더라도 신규 후보 사용의 증거가 되지 않는다.

2번의 `expression`과 `transformation_stage`는 `primary_focus_source_witnesses` 투영에서 0개였다. 얼굴 반응을 설명한 쿼리의 `connected`·`wrist`도 `anatomical_connection` 역할로 해석됐다. 3번의 `prop_state`는 `without proving actual memory loss`를 비양성 범위로 해석해 0개가 됐다. 이는 전체 후보 사전에 관련 자료가 없다는 뜻과 구분한다. 봉인된 쿼리를 사후 변경하거나 추가 검색으로 성공 사례를 고르지 않았다. [실제 반환과 빈 투영의 근거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/managed-retrieval-exposure.json)를 보존했다.

## 이미지 결과

| 테스트 | 생성 결과 | 원본 픽셀 판정 | 프롬프트 |
| --- | --- | --- | --- |
| 1. 심야 교정실 | 출력 단계 `moderation_blocked`, 이미지 없음 | 평가 불가 `blocked_unscored` | [영문 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/metafiction-20261022-arm1/final-prompt.txt) |
| 2. 페리 개찰구 | 1392×1130 PNG | **부분 구현**. 팔이 평면 손 아이콘으로 이어지고 LEAVE·WAIT·동일 인물의 게임 초상은 보인다. 지정한 오른팔/왼손 배정이 뒤바뀌었고 지지발의 바닥 접촉은 크롭으로 비관측이다. | [영문 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/metafiction-20261022-arm2/final_prompt_en.txt) |
| 3. 극장 물품보관대 | 1237×1272 PNG | **부분 구현**. 현재 장면을 담는 재귀 사진, 같은 얼굴의 3단계 소실, LV 12·MEMORY 1·RESTORE가 명료하다. 지정한 오른엄지 대신 왼엄지가 빈 초상을 누르며, 정확한 시선 대상은 부분 관측이다. | [영문 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/metafiction-20261022-arm3/final-prompt.txt) |

루트 검토자는 두 저장 원본과 실제 첨부 JPEG를 `view_image(detail=original)`로 직접 확인하고 파일 SHA-256·치수·디코딩 무결성을 따로 확인했다. [고정 기준별 독립 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/ROOT-PIXEL-REVIEW.json)에 관측 근거와 실패를 보존했다. 사전 기준을 모두 통과한 테스트는 0개이며, 이는 핵심 주제 관계가 보인다는 관측과 구분한다. 손의 좌우는 에이전트가 사전에 선택한 연출 세부이지 사용자가 지정한 외모나 실제 신원 정보가 아니다.

세 런의 composition·runtime 감사는 모두 통과했다. composition에는 각 6개의 `uncovered intent preserved by authored evidence` 경고가 있어 그대로 보존했다. 2번과 3번은 리뷰 기록 형식 검증이 통과했지만 `technical_qualification=fail`이다. 1번은 실제 이미지가 없어 픽셀 리뷰를 실행하지 않았다. 세 런의 `deliver` 통과는 프롬프트 전달 감사이며 이미지 수락이나 시각 게이트 통과를 뜻하지 않는다. 사용자 수락은 모두 `pending`이다.

1번 도구는 `output` 단계, `sexual` 카테고리의 구조화된 오류를 반환했다. 요청 ID는 `4ccafaf1-0631-4da4-84a5-65314791184f`다. 반환 픽셀이 없으므로 실제 출력 내용이나 차단의 세부 원인을 추정하지 않았다. 다른 모델·API로 우회하거나 재생성하지 않았다.

### 신규 데이터의 기여와 한계

1번과 2번은 완결된 대안을 기본안과 비교한 뒤 기본 프롬프트를 그대로 유지했다. 신규 후보의 실제 영감 사용은 0개다. 3번은 D01의 전체 조건과 효과를 검토한 뒤, 고유한 인물·수·연필·세 칸 구도를 거절하고 일반적인 종이의 절단면과 휨만 국소 영감으로 사용했다. 이미지에서 종이의 가장자리와 물성은 보이지만, 이것만으로 해당 후보가 결과를 개선했다고 입증할 수 없다.

세 에이전트 모두 전용 의미 JSON과 전용 참고 문서를 직접 열어 읽지는 않았다. 검색 후 반환된 canonical source에 포함된 의미·조건·효과를 검토했다. 따라서 이 실험은 설치된 후보의 실제 노출과 원문 검토, 참조 이미지 생성, 주제의 픽셀 구현을 검사한다. 별도 의미 레지스트리 문서의 직접 소비나 데이터 갱신의 인과적 품질 개선을 입증하는 실험은 아니다. 전체 원문을 native 권한이나 사실로 승인한 사례도 없다.

### 생성된 원본

**2. 비활성화된 이동 명령에 붙잡힌 개찰구**

![페리 개찰구에서 팔이 게임 명령 아이콘으로 이어지는 장면](/Users/chasoik/Projects/image-prompt/generated/photo-runs/metafiction-20261022-arm2/images/arm2-disabled-departure.png)

**3. 얼굴 기록이 소실되는 물품보관대**

![재귀 장면과 소실되는 얼굴 기록을 들고 있는 물품보관대 장면](/Users/chasoik/Projects/image-prompt/generated/photo-runs/metafiction-20261022-arm3/result.png)

### 후속 보완의 우선순위

1. 검색 투영의 세 빈 결과를 별도 회귀 사례로 유지하고, 얼굴 반응의 관계 표현과 비시각적 입증 제한이 양성 역할 초점을 지우는 경계를 검토한다. 이번 봉인 쿼리와 결과는 변경하지 않는다.
2. 다음 생성 실험에서는 손의 소유자와 인물 기준 좌우가 실제 경계·초상 접점에 함께 드러나는 구도를 비교한다. 이번 실패를 지우는 사후 통과 기준은 만들지 않는다.
3. 신규 데이터의 개선 효과를 측정하려면 동일한 독립 요청·입력·생성 예산으로 기존/신규 검색 자료를 비교하는 별도 실험이 필요하다. 이번 두 원본은 인과적 개선이나 사용자 수락의 증거로 쓰지 않는다.

## 재현 정보

- 테스트에 사용하는 H-F2 버전: `a70efe4c584dbf52528dd2a0d56c8d5ba96489c0195af9034e1d2a79986514dc`
- 연결된 native 원문 버전: `d12314c84854d0f9c2ffbd87f52b4112d9adc0ec5fdfba6a240a93522ede4d17`
- 작업 원문 SHA-256: `6e59a955b17a7abc00bc642947f48932fb133bd034987918c87059b80cb255ca`
- 사용한 SKILL.md SHA-256: `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`
- 첨부 참조 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`

위 스킬은 테스트 고정과 이미지 호출 당시 사용한 최신 작업 버전이다. 호출 이후인 `2026-10-22 11:00:01 UTC`에 작업 폴더의 SKILL.md가 `6ce8dc08646795b01c08bbd1029c9b7d43901d36cc859f9f788aefa9413b417c`로 추가 변경됐다. 변경분은 재시도 경로 문구와 실패 경로 안내 한 문단이며, 이를 역으로 제거하면 사용한 버전의 해시가 정확히 복원된다. 이번 작업은 해당 변경을 작성하거나 되돌리지 않았다. 각 1회 예산과 재호출 없음은 유지했다. 설치된 검색 버전·코드·native CURRENT와 참조 JPEG는 최종 검사에서도 유지됐다. [버전 경계와 최종 원문 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/final-state-verification.json)에 근거를 보관했다.

운영 후보는 작성 V3에서 설치 V4 canonical native/meaning 형식으로 변환된다. 바이트 동일성이 아니라 복원된 74개 원문 값과 128개 연결 값이 정확히 일치함을 확인했다. 별도 의미 레지스트리는 작업 폴더의 검토 데이터이며 설치 원문의 두 번째 소유자가 아니다. 검색 자료는 canonical 후보에 들어 있는 source-bound 의미를 노출한다.

[증거 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/integration-evidence/)에는 보존 검사, 전체 인덱스 검증, 설치 기록, 검색 결과와 독립 테스트 입력을 보관한다. 사용자 수락과 미적 선호는 별도 판단으로 남긴다. 커밋과 푸시는 요청되지 않아 수행하지 않았다.
