# 메디컬 호러 반영 및 독립 이미지 테스트 결과

시각 의미 카드 86개, 한영 키워드 경로 181개, 새 시각 후보 61개, 문맥·진단·보류 기록 23개, 선택적 슬롯 연결 183개를 반영했다. 기존 후보 2개는 원본을 보존해 재사용했다. 검색 인덱스와 설치된 기본 데이터에서도 이번 추가분을 확인했다.

독립 에이전트 3개가 서로 다른 콘셉트를 추첨하고, 첨부 인물 사진을 외형 참고로 사용해 프롬프트와 사전 판정 기준을 작성했다. 각 에이전트가 내장 이미지 도구를 정확히 한 번씩 호출해 총 3장을 생성했다. 세 장 모두 임상 공간과 불안한 상황은 읽히지만, 필수 공간·접촉 관계가 일부 어긋나 **전체 결과는 모두 PARTIAL, 엄격한 전체 사례 판정은 FAIL**이다.

## 데이터 반영과 검증

반영 결정, 소스의 지원 범위, 파일 목록과 검색 결과는 [ADOPTION-RESULTS.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/medical-horror-20261022/integration-evidence/ADOPTION-RESULTS.md)에 기록했다.

- 집중 데이터 검사 16개와 관련 기존 회귀 검사 52개가 통과했다. 최종 dictionary 검사 오류는 0개다.
- 연구 자료에서 만든 한영 128질의를 전후 각각 검색했다. 개발 질의 48개의 목표 후보 상위 10위 노출은 4/48에서 48/48로 증가했다. 독립 평가셋의 정확도나 이미지 품질 향상으로 해석하지 않는다.
- 일반 질의 24개 중 10개에도 새 의료 후보가 노출됐다. 전체 원본·조건·효과를 검토하고 비의료 요청과 충돌하는 후보를 거절하는 판단이 여전히 필요하다. [일반 질의 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/medical-horror-20261022/integration-evidence/control-source-review.json)에 실제 검토를 남겼다.
- 현재 작업 corpus는 다른 동시 작업을 포함해 후보 19,801개, 시각 검색 후보 19,438개, 연결 14,246개다. 이 전체 증가분을 이번 메디컬 호러 작업의 성과로 계산하지 않았다.
- 모든 새 소스의 `native_approval`은 false다. 출처는 정의·경계의 근거이며, 창작 장면 전체를 관측한 임상 사진의 증거로 취급하지 않았다.

## 생성 결과

| 실행 | 독립 콘셉트 | 실제 보인 핵심 | 실패·관측 한계 | 신규 데이터의 화면 반영 |
|---|---|---|---|---|
| A | 기록과 출구를 통제하는 퇴원 창구 | 빈 봉투, 유리 너머 인물 차트, 문 이음새를 가로지르는 빗장 | 봉투 아래가 카운터에 지지되지 않음. 인물 기준 좌우 손이 뒤바뀜. 강한 호러보다는 병원 행정의 불안에 가까움 | 새 후보 7개 노출, 미채택. 신규 데이터의 픽셀 기여는 NOT_ADOPTED |
| B | 출구를 차지한 진단 스캐너 | 링·플랫폼·문 관계, 손바닥 접촉과 장비 쪽 시선 | 플랫폼이 인물의 다음 걸음 쪽 대신 카메라 쪽으로 뻗음. 바퀴·발은 보이지 않아 이동성·모든 출구 봉쇄까지 입증하지 못함 | 새 후보 10개 노출, 미채택. 신규 데이터의 픽셀 기여는 NOT_ADOPTED |
| C | 한 표본만 해동된 듯한 동결보관실 | 밀봉 용기 속 표본·액면, 한 투명 용기와 여러 서리 낀 용기의 대비, 물방울·젖은 바닥, 표본 위에서 멈춘 손 | 좌우 손 동작이 뒤바뀜. 새 현미경 소스의 받침·작업대 접점이 가려져 완전한 관계는 미확인 | 새 후보 6개 노출, A08 한 개를 창작 참고로 반영. 현미경·라벨 있는 슬라이드·별도 표본 용기는 보이나 전체 소스 판정은 PARTIAL |

각 사례의 검토 기록은 공식 감사에서 유효했다. 이는 이미지의 완전 통과와 다르다. 공통 신체·접촉 필수 검사 5개는 A 3/5, B 5/5, C 4/5다. B는 공통 검사를 통과했어도 사례 고유의 플랫폼 방향 조건에 실패했다. B의 사전 장면 기준은 5/6, C는 6/7 통과이며, 부분 관측은 전체 통과로 올리지 않았다.

세 이미지 모두 호러 주제의 임상적 맥락은 구현했다. 다만 이번 검색에서 새 소스를 실제 최종 문장에 남긴 실행은 C 한 개다. A/B의 임상 장면은 에이전트가 후보 검색 전에 만든 코어에서 왔으므로 새 데이터의 효과로 돌리지 않았다. C에서도 보이는 구성 요소와 가려진 전체 관계를 구분했으며, 신규 소스의 native 자격이나 비교 이미지 없는 인과적 품질 향상은 주장하지 않는다.

### A: 퇴원 창구

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-a-image-v2/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-a-image-v2/arm-a-report.md) · [전체 소스 판단](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-a-image-v2/full-source-review.json)

![퇴원 창구: 빈 봉투와 유리 너머 기록, 빗장이 걸린 출구](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-a-image-v2/generated-image.png)

### B: 진단 스캐너

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/REPORT.md) · [전체 소스 판단](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/source-decisions.full.json)

![진단 스캐너: 링을 짚은 인물과 문 앞 장비, 카메라 쪽 플랫폼](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-b-image-v2/image.png)

### C: 동결보관실

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/report.md) · [전체 소스 판단](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/source-decisions.full.json) · [A08 관계 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/source-contribution-gates.review.json)

![동결보관실: 서리 낀 용기 사이의 투명 표본과 현미경·슬라이드](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/rendered/cryobank-thaw-anomaly.png)

## 실행의 독립성과 증거 범위

각 에이전트는 다른 실행의 콘셉트·프롬프트·이미지를 입력으로 쓰지 않았다. 후보 검색 전에 독립 추첨·코어·계획·사전 픽셀 기준을 고정했고, 생성·검토까지 각자 진행했다. 코디네이터는 저장된 원본과 필요한 원본 픽셀 crop을 별도로 보았다. 첨부 사진은 얼굴과 짧은 머리의 시각적 연속성을 위한 참고이며 실제 신원·진료 이력·감정의 인증 자료가 아니다.

총 15회 질의의 104개 반환 항목을 검토했다. 각 질의는 BM25F와 로컬 cosine 검색을 한 번씩 수행했다. 실행별 새 CID 노출은 7/10/6개이며 세 실행 합집합은 17개다. A의 contact_point 0건은 원본 witness projection, C의 concept_tension 0건은 작성한 문맥이 exclusion-only로 해석된 결과로 기록했다. 데이터 부재로 보고하지 않았으며 고정 계획을 바꾸어 재질의하지 않았다.

실행 준비 시점에 확인한 최신 스킬 문서 해시는 세 실행 모두 `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`다. 검증한 공통 커널 코드 해시는 `96b67dedcfea019115cd46c6542287d7102e46cd12a486f1e817d79f3c634d0e`다. 세 이미지의 검색은 이번 데이터만 추가해 검증·설치한 `3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5` 릴리스에 고정했다. 동시 작업에서 갱신된 기본 릴리스 `a70efe4c584dbf52528dd2a0d56c8d5ba96489c0195af9034e1d2a79986514dc`에는 이번 원본 84/84, 연결, 시각 후보 61/61이 포함됨을 별도로 확인했다. 세 이미지를 해당 기본 릴리스로 생성했다고 보고하지 않는다. 종료 검사 중 작업 스킬도 다시 바뀌었으므로, 이후 버전까지 이미지 테스트했다고 주장하지 않는다.

초기의 prompt_only 실행 등록은 공식 절차로 image-v2에 동일하게 재현했다. 코어·controls·잠금과 저자 계획은 유지했고, 새 콘셉트를 재추첨하지 않았다. C의 첫 composed 감사에서 발견한 필드 타입은 공식 재감사로 수정했으며 실제 프롬프트는 바뀌지 않았다. 첫 실패 기록을 보존했다. 각 실행은 이미지 1회, 재생성 0회, 대체 provider 0회다.

앞선 보존 검사에서는 보호 파일 165개 중 예상한 인덱스·런타임 설정만 달라졌고 기존 후보와 코드·SKILL 바이트 보존을 확인했다. 그러나 마지막 산출물 검사에서는 공통 코드 5개가 그때의 바이트와 달라졌고, 이어 스킬 문서와 workflow shape도 바뀌었다. 저장소 HEAD도 다른 주제의 병합으로 `332d989…`에서 `242e73c…`로 전진했다. 두 관측의 인과관계나 정확한 외부 수정 주체는 확인하지 않았다. 코디네이터와 의료 에이전트들은 이 공통 파일을 수정하지 않았으며, 해당 변경을 되돌리지 않았다. [동시 변경 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/medical-horror-20261022/integration-evidence/concurrent-source-drift.json)에 전후 해시와 한계를 남겼다. 보호 파일 전체 동일성 및 종료 시점 스킬 동일성 검사의 실패를 보존했고, 앞선 52개 검사로 이후 작업 코드까지 통과했다고 주장하지 않는다. 실제 이미지에 고정된 설치 세대와 매니페스트의 테스트 버전 기록은 그대로다. 종료 시 관측한 스킬 해시는 `6ce8dc08646795b01c08bbd1029c9b7d43901d36cc859f9f788aefa9413b417c`이며 이 후속 버전으로는 이미지를 다시 생성하지 않았다.

기존 dirty 수정은 이번 작업의 변경으로 취급하지 않는다. 전역 CURRENT는 관측상 동일하고 이번 작업의 CURRENT 쓰기는 0회다. 이번 작업에서 커밋·푸시는 수행하지 않았다. 최초 연구 패키지의 28개 체크섬은 모두 일치하며 원래 NOT_RUN 기록은 역사적 결과로 보존했다. 최종 증거 검사는 이미지·프롬프트·원장·독립 실행 기록의 일치를 확인하되, 공통 소스 변화는 별도 경고로 남긴다.

## 남은 개선점

후속 개선은 새 동의어 추가보다, 일반 질의에서의 의료 후보 노출 억제와 전체 소스 적합성 판단, 좌우 손·지지점·장비 진행 방향의 생성 충실도를 우선해야 한다. A08의 전체 관계를 확인하려면 현미경 받침까지 보이는 구도가 필요하다. 이번에는 실패를 지우는 재생성을 하지 않았으며, 사용자 수용과 비교 이미지에 대한 선호 평가는 아직 없다. 3개의 사례로 전체 86개 의미 카드나 61개 새 시각 후보의 픽셀 자격을 확정하지 않는다.

[최종 산출물 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/medical-horror-20261022/integration-evidence/completion-validation.json) · [증거 파일 색인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/medical-horror-20261022/integration-evidence/EVIDENCE-INDEX.json)
