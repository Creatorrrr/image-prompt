# Clockpunk 반영과 독립 이미지 시험

완료된 실행 기록이다. 원래 연구 단계의 `NOT_RUN` 판정은 당시
스냅샷으로 보존하며, 후속 실행 결과를 이 문서와 `integration-evidence/`,
`image-tests/`에 따로 기록한다.

88개 의미 카드와 213개 키워드 경로를 운영 데이터에 연결했다. 신규 레코드는
시각 후보 74개와 양성 검색에서 제외되는 진단 17개이며, 선택적 연결 137개를
추가했다. 기존 후보 6개는 태엽/탈진/캠의 역할, 정지 사진의 입증 한계,
오러리와 아스트롤라베 영감의 허구 장치 구분에 맞춰 표현을 교정했다.
기존 조건·효과·출처와 나머지 레코드, 연결, 카탈로그, 정책은 보존 검증했다.

추가 기술 검토가 필요한 A09, A10, B03, B05, B11, E02, G02는 진단으로
보류했다. 서로 다른 장면을 한 후보로 결합하지 않도록 E05, M03, M04를
각각 두 대안으로 나눴다. 새 자료는 선택적 탐색 자료이며 연구 그래프나
출처 표기가 전체 native 의미 자격을 부여하지 않는다.

세 서브에이전트는 대화 이력을 상속하지 않고 동일한 사용자 입력과 참고
사진만 전달받았다. 각자 4~5개 대안을 저술한 뒤 기록한 seed로 하나를
추첨했으며, baseline·관찰 기준·표현 계획을 후보 접근 전에 동결했다.
넓은 탐색 분야만 조정자가 나눠 주었으며 세부 장면과 부품은 각자가 정했다.

| Arm | 독립 컨셉 | 사전 관찰 기준 |
|---|---|---|
| A | 태엽식 모종 관수 장치 | 관계 5개와 얼굴·머리 참고 |
| B | 운하 출발소의 기계식 노선표 | 관계 6개와 얼굴·머리 참고 |
| C | 정오 독서 마당의 그늘 장치 | 참고 외형을 포함한 관계 6개 |

관찰 기준은 에이전트가 만든 실험 조건이며 사용자 고정 조건으로 승격하지
않는다. 연결의 양 끝과 경로가 함께 보여야 통과한다. 일부만 보이거나 가려진
경우는 실패이며, 정지 이미지는 실제 운동·정확도·물리적 성능을 증명하지
않는다. 검색 노출, 프롬프트 사용, 실제 참고 이미지 전달, 저장된 픽셀,
사용자 수용은 서로 다른 결과로 기록한다.

기본 런타임 설치와 전체 검증을 통과했다. 최종 기본 H-F2는
`86e91bb00125886973c27b8df38329c9af9cfc302d579dda1da9e3637fa63573`,
이미지 시험의 고정 H-F2는
`1357d4e9171988e46ea9825a2ce4bed4afdd875ca4e29cb24c3f93c02ceaa608`이다.
동시 게시된 다른 주제 데이터를 최종 기본 버전에 보존했으며, 두 버전의 코드와
Clockpunk 신규·교정 레코드 97개가 정확히 동일함을 검증했다.
코드 SHA는 `ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef`다.
CURRENT는 변경하지 않았으며 설치 설정만 검증 후 갱신했다.

최종 기본 버전은 레코드 20,329개, 양성 CID 19,846개, RID 19,848개다.
기존 레코드 20,232개는 그대로 보존했고 6개만 교정했다. 작업 중인 저술
데이터는 별도 진단 레코드 등을 포함하며 사전 검증 결과 20,341개, 연결
15,120개, 오류 0개였다. 저술 checkout과 선택된 봉인 실행본을 혼동하지 않는다.

실제 전체 풀 검색은 한국어·영어 240개, 변경 전 경계 질의는 64개 실행했다.
등록된 시각 카드가 대상인 142개 개발 질의는 모두 대상 후보가 top10에 노출됐다.
카드 문장을 사용한 개발 질의이므로 독립 holdout 정확도나 개선율이 아니다.
경계 질의 64개 중 43개에는 새 후보가 top10에 나타났다. 관련 구조뿐 아니라
황동 꽃병과 황동 시계 부품처럼 부적합한 이웃도 있다. 각 사례의 소유자·주장
경계를 [별도 검토](integration-evidence/boundary-query-review.json)에 기록했고
정밀도 통과로 판정하지 않았다.

실제 managed 역할 검색에서는 B와 C의 기계 구조를 해부학으로 해석해
0건을 반환하는 결함도 발견했다. [원본 근거와 후속 구현 계획](RETRIEVAL-FOLLOWUP.md)을
남겼으며 질의 변경·후보 강제 삽입·재추첨으로 원래 결과를 덮지 않았다.
이 문제는 일반 풀의 개발 질의 노출률과 별개다.

세 독립 arm에서 네이티브 호출 각 1회, 총 3회가 모두 이미지를 반환했다.
참고 JPEG의 실제 전달과 원본의 동일 바이트 보존, ledger·manifest·리뷰 기록을
검증했다. API fallback과 재생성은 0회다.

세 장 모두 Clockpunk 장면과 얼굴·머리 참고가 보인다. **사전의 엄격한 전체
장면 기준 통과는 0/3**이다. 다음 개별 통과 수는 각 담당자의 원래 판정이다.
C는 참고 외형을 6개 항목 안에 포함하며, A/B의 참고 외형은 별도다.

| Arm | 무작위 선택 | 담당자 사전 기준 | 전체 | 주요 실패 |
|---|---|---|---|---|
| A | 태엽식 모종 관수 장치 | 2/5 | FAIL | 기어 맞물림, 캠–레버–밸브 연결, 왼손–트레이 테두리 접촉 |
| B | 운하 출발소의 기계식 노선표 | 2/6 | FAIL | 추 하단 잘림, 비맞물림 기어, 피니언–랙 단절, 탈진기–진자 연결 |
| C | 정오 독서 마당의 그늘 관리인 | 3/6 | FAIL | 기어 맞물림, 크랭크–로드–차양의 연속 경로, 책이 새 그늘로 들어가는 배치 |

세 메뉴의 대안 수/seed/선택 index(0부터)는 A: 4 / `10252606791326872420` / 3,
B: 5 / `16062716169931929420` / 4, C: 4 / `7322402510208628601` / 0이다.
재추첨·다른 arm의 입력 사용은 없었다.

새 Clockpunk 자료의 직접 프롬프트 영향은 A01을 기존 태엽 형태를 명료화하는
`inspiration_only`로 쓴 A에서만 기록됐다. B/C는 노출된 자료를 장면에 맞지
않아 제외했다. 전체 native source 채택은 0이다. 따라서 세 이미지의 장르
인상을 새 데이터의 인과적 품질 향상이나 전체 데이터의 픽셀 검증으로
주장하지 않는다.

root도 세 원본을 직접 검사해 전체 FAIL을 확인했다. A의 물이 닿는 흙과
어두운 착수 지점은 잎에 가려졌다는 더 보수적인 판정을 별도로 남겼다.
담당자의 A-G3 PASS를 덮어쓰지 않았다.

관리형 review 기록은 셋 모두 유효하다. A/C의 `technical_qualification`은
FAIL이고 B는 신체 소유·관절·지지·접촉·가시성의 다섯 검사에 한해 PASS다.
B의 이 PASS는 추·기어·랙·탈진기의 연결 성공을 뜻하지 않는다. 동결된
별도 기계 실험은 2/6으로 FAIL이다. 사용자 수용 판단은 미확인이다.

| Arm | 실제 도구 전달 프롬프트 | 원본 | 원래 기준·상세 판정 |
|---|---|---|---|
| A | [native prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/prompts/arm-a-native-prompt.txt) | [PNG](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-independent-a-20261023/clockpunk-seedling-keeper.png) | [기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-a/testcase.json) · [담당 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-a/arm-a-report.md) · [root 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/coordinator-pixel-review-a.json) |
| B | [native prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/prompts/arm-b-native-prompt.txt) | [PNG](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-20261023-independent-b/original.png) | [기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-b/testcase.frozen.json) · [담당 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-b/arm-report.md) · [root 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/coordinator-pixel-review-b.json) |
| C | [native prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/prompts/arm-c-native-prompt.txt) | [PNG](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-20261023-independent-c/noon-shade-keeper-original.png) | [기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-c/testcase.json) · [담당 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-c/result-report.md) · [root 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/coordinator-pixel-review-c.json) |

다음 회귀에서는 구성 요소를 더 늘리지 않고, 한 평면에 읽히는 기어 접점과
하나의 연속 출력 경로를 우선한다. A는 캠–레버–밸브 및 트레이 손 접점,
B는 추의 하단 여백과 구동 피니언–랙, C는 차양까지 이어지는 로드와 책의
명확한 그늘 경계를 우선한다. 새로운 실험에서는 원래 실패를 보존하고 새
revision을 사용한다. 먼저 위의 역할 오분류 회귀를 수정·검증한다.

커밋·푸시는 이 작업에서 수행하지 않았다. 무결성 manifest는
`INTEGRATION-SHA256SUMS`이며, 재현 가능한 상세 기록은
`integration-evidence/FINAL-RESULT.json`과 각 arm 보고서에 있다.


### A: 태엽식 모종 관수 장치

![태엽식 모종 관수 장치](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-independent-a-20261023/clockpunk-seedling-keeper.png)


### B: 운하 출발소의 기계식 노선표

![운하 출발소의 기계식 노선표](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-20261023-independent-b/original.png)


### C: 정오 독서 마당의 그늘 관리인

![정오 독서 마당의 그늘 관리인](/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-20261023-independent-c/noon-shade-keeper-original.png)

