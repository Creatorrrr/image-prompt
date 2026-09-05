**reverse-image-prompt 개선 및 과거 이미지 3건 재실행**

구조 개선을 반영했고, 서로 다른 새 대화의 서브에이전트 3개에서 과거 원본을 분석해 영문 프롬프트를 추출한 뒤 그 텍스트만으로 이미지 생성을 시도했다. 프롬프트·계획 검증은 3건 모두 통과했다. 이미지가 전달된 2건은 핵심 장면을 재현했지만 중요한 차이가 남아 **충실도 FAIL — 부분 재현**으로 평가했다. 나머지 1건은 생성 결과 검사에서 차단되어 **픽셀 미평가**다.

[수정된 SKILL.md](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/SKILL.md) · [구조 검증 기록](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/package-validation-final.json) · [최종 무결성 검사](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/final-integrity.json) · [개선 평가 기록](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/evaluations/2026-09-06-profile-context-and-forward-replay.json)

**반영한 개선**

- 진입 문서는 목적·실행 경로·출력 계약 중심으로 줄이고, 상세 통합 규칙은 [integration-contract.md](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/references/integration-contract.md)로 분리했다. 이미지 작업과 스킬 유지보수를 구분해, 구조 검토만으로 이미지 분석 절차가 시작되지 않게 했다.
- 기본 `prompt`와 증거 기록이 필요한 `audited` 계약을 명시적 블록으로 구분했다. [profile_context.py](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/tools/profile_context.py)는 선택한 계약의 전체 내용을 읽고, 누락·읽기 실패·잘못된 마커를 오류로 처리한다. 공통 규칙은 보존하며 원본 파일과 실제 읽은 내용의 해시를 남긴다.
- 라우트가 사용하는 모듈·lane·공통 지침을 해시로 묶고, 실제 라우트에 맞는 3–6개 분석 lane과 자원 부족 시 순차 실행을 명시했다. 순차 실행을 독립 분석으로 기록하지 않는다.
- 출력 계약의 중요도·인과 순서가 모델 어댑터보다 우선하도록 충돌을 정리했다. 독립형 프롬프트 검사를 [prompt_lint.py](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/tools/prompt_lint.py)로 분리하고, compact report의 선택적 종합 묘사 후보도 데이터 경계에서 검증한다. 텍스트 lint의 통과 범위는 외부 참조가 남았는지를 확인하는 좁은 검사다.
- 실제 실행 중 드러난 기존 검증기 결함 2개를 고쳤다. `audited` 라우트를 기본 `prompt`로 재구성하던 문제와, 피부 표면의 중요도를 인물 전체 중요도에 강제로 일치시키던 모순이다. 잘못된 프로필·누락된 영역 등을 거부하는 회귀 검사는 유지했다.
- [analysis-runtime.md](/Users/chasoik/Projects/image-prompt/skills/reverse-image-prompt/references/analysis-runtime.md)에 분석 모델 설정과 이미지 생성기 설정의 소유권, 실제 실행 시간·시도·실패 기록을 정리했다. [OpenAI latest-model 가이드](https://developers.openai.com/api/docs/guides/latest-model)의 지침 충돌 점검, 명시적 위임 정책, 작업에 맞는 검증 원칙을 참고했다. 문서 확인일은 2026-09-05다.

| 구조 측정 | 변경 전 | 변경 후 |
| --- | ---: | ---: |
| SKILL 진입 본문 단어 수 | 3,492 | 1,146 |
| 고정 5-lane 조건의 공통 지침 단어 수, prompt | 5,311 | 3,988 |
| 같은 조건의 공통 지침 단어 수, audited | 5,311 | 4,081 |

이는 **문서 단어 수**이며 모델 토큰 수나 속도 측정이 아니다. 같은 조건에서 각 lane에 배분되는 본문 단어 수의 합은 prompt 14,825→14,197, audited 14,825→14,835로, 상세 감사 부담은 거의 줄지 않았다. [측정 원본](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/structural-context-metrics.json)

**실제 테스트 결과**

과거 사용자 메시지에서 입력 이미지의 정확한 바이트를 복원했다. 추출 담당자에게는 해당 원본·동일 요청·스킬 사본을 제공했고, 과거 추출 프롬프트나 생성 결과는 제공하지 않았다. 결과를 본 뒤 다른 원본으로 교체하지 않았다. [선정·출처·해시](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/source-selection.json)

| 사례 / 과거 입력 날짜 | 원본 크기 | 프롬프트 | 생성 호출 / 전달 | 전달 크기 | 평가 |
| --- | --- | --- | --- | --- | --- |
| 1. 노란 헤드폰 옆모습 / 2026-07-24 | 1085×608 | 445단어, 2747바이트 | 1회 / 1장 | 1672×941 | 부분 재현, 충실도 FAIL |
| 2. 욕실 거울 셀카 / 2026-07-31 | 399×623 | 597단어, 3713바이트 | 2회 / 1장 | 1006×1564 | 부분 재현, 충실도 FAIL |
| 3. 낮은 시점 인물과 일러스트 배경 / 2026-08-23 | 969×1280 | 535단어, 3189바이트 | 2회 / 0장 | 없음 | 생성 차단, 픽셀 미평가 |

세 사례 모두 내장 `image_gen__imagegen`에 **고정된 `prompt` 한 필드만** 전달했다. 두 이미지 참조 옵션은 생략했다. 정확한 생성 모델·크기·품질 설정은 도구에 노출되지 않아 지정하거나 확인했다고 주장하지 않는다. 2·3번의 두 번째 호출은 최초 무전달 실패 뒤 동일한 프롬프트 바이트로 실행했으며, 결과를 개선하려는 재생성은 없었다.

**사례 1 — 노란 헤드폰 옆모습**

| 원본 | 추출 프롬프트로 생성 |
| --- | --- |
| ![사례 1 원본](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/inputs/case-01.jpg) | ![사례 1 생성 결과](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-01/output/render.png) |

가로 구도, 오른쪽을 향한 옆모습, 노란 헤드폰과 역광은 유지됐다. 얼굴·이어컵의 비중이 커지고 머리카락과 피부 경계가 더 선명해졌다. 원본의 밝고 씻긴 듯한 낮은 대비가 약해졌다. 중요한 포착 질감 차이가 있으므로 부분 재현을 PASS로 처리하지 않았다.

[추출 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-01/output/prompt.txt) · [생성 이미지](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-01/output/render.png) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-01/output/result.json)

**사례 2 — 욕실 거울 셀카**

| 원본 | 추출 프롬프트로 생성 |
| --- | --- |
| ![사례 2 원본](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/inputs/case-02.jpg) | ![사례 2 생성 결과](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-02/output/render.png) |

얼굴을 가린 휴대전화, 두 갈래 땋은 머리, 내려온 카디건과 세면대는 유지됐다. 몸의 대각선은 약해지고 중심·수직 방향으로 정렬됐다. 카디건은 더 두껍고 거친 니트로 바뀌었으며, 상의와 하의 사이 간격과 세부 선명도가 커졌다. 왼쪽 메모도 더 작고 어둡다.

[추출 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-02/output/prompt.txt) · [생성 이미지](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-02/output/render.png) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-02/output/run-report.json)

**사례 3 — 낮은 시점 인물과 일러스트 배경**

![사례 3 원본](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/inputs/case-03.jpg)

프롬프트 추출과 bundle·plan·독립형 검사, 별도 검토는 통과했다. 첫 생성 호출은 이미지가 전달되지 않았고 정확한 실패 원인은 확보하지 못했다. 동일 바이트 재시도에서 `HTTP 400 moderation_blocked`, `moderation_stage=output`, `categories=[sexual]`이 반환됐다. 전달된 이미지가 없어 재현 여부를 평가할 수 없다. 이 결과로 원본이나 요청 자체가 정책을 위반한다고 판단하지 않는다. 차단 뒤 프롬프트 변경·생성기 전환·우회 시도는 하지 않았다.

[추출 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-03/output/prompt.txt) · [전체 실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-03/output/report.json) · [반환된 실패 원문](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/cases/case-03/output/generation-response.attempt-02.raw.txt)

**독립성과 실행 조건**

사례별 조정자는 이전 대화 이력을 넘기지 않은 새 서브에이전트였고, 각자 원본·스킬 사본·출력 폴더를 사용했다. 같은 운영체제와 파일시스템을 공유하므로 OS 샌드박스 격리는 아니다. 내부 5개 분석 lane 중 새 대화에서 완료된 수는 사례별 1·2·1개였고, 나머지 4·3·4개는 실제 용량 제한 뒤 기록된 순차 실행으로 완료했다.

프롬프트 검토자는 사례 조정자의 추론 대화와 분리된 root였지만, 세 사례를 공통으로 검토했다. 픽셀 평가도 root가 원본을 보며 수행했으므로 블라인드 평가가 아니다. 사례 3에서 협업 목록 조회가 다른 사례의 상태 요약을 우연히 노출했다. 다른 사례의 산출물·과거 프롬프트·과거 생성 이미지는 열거나 분석에 사용하지 않았으나, 완전한 정보 차단을 주장하지 않는다.

분석을 시작한 v1과 최종 검증 v3 사이에는 위 검증기 결함 2개 및 회귀 검사만 변경했다. 이미지 해석 지침과 라우트 입력 바이트는 바뀌지 않았고, 이전 사본·실패 기록도 보존했다. v3의 113개 고정 파일은 현재 작업 스킬 및 세 사례 사본 모두 일치한다. 최종 평가 기록은 실행 후 추가한 문서이며 해당 실행 스냅샷에 포함되지 않는다. 스냅샷에 없는 부수 파일의 부재까지 검사한 것은 아니다.

**검증 범위와 남은 문제**

전체 테스트는 **311개, subtest 267개 통과**다. 구조 검사 대상은 37개 모듈·6개 lane이며, 컴파일 결과의 125개 필수 anchor와 23개 라우팅 시나리오, manifest 및 스킬 형식 검사도 통과했다. 별도로 세 사례의 고정된 bundle·plan·prompt를 검사하는 9개 최종 실행이 통과했고, 원본과 생성 요청 바이트·검토한 계획의 해시를 대조했다. [근거](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/package-validation-final.json)

원본별 평가 기준은 생성 전에 고정했다. 실제 픽셀 평가는 수동으로 보이는 구도·관계·표면·색과 빛·포착 질감을 비교한 결과다. 정량적 색·빛 보정 평가와 사용자 선호 평가는 미평가다. 인물의 신원이나 동일인 여부를 비교하지 않았다. [생성 전 기준](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/source-render-review-contract.json) · [생성 후 픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/reverse-skill-improvement-20260905-224431/root-render-reviews.json)

세 입력은 모두 과거의 인물 사례여서 새 holdout이나 사물·풍경 전반의 품질을 입증하지 않는다. 변경 전 스킬로 같은 생성기를 다시 실행한 비교군도 없다. 기록된 사례별 전체 경과 시간은 약 68.6·73.6·68.7분이며, 상세 감사 작성·대기·용량 제한 복구·검증기 수정·기록 작성을 포함한다. 이를 순수 분석 시간이나 개선 전후 속도 비교로 해석할 수 없다.

두 생성물에 공통으로 남은 문제는 원본의 낮은 선명도와 부드러운 표면이 더 또렷하고 강한 재질 표현으로 바뀐다는 점이다. 다음 검증에서는 포착 질감·재질 묘사의 배치와 세부 묘사량을 한 요소씩 바꾸는 비교가 유용하다. 지금 결과만으로 원인이 프롬프트 길이인지 생성기의 표현 경향인지 확정하거나, 사례별 표현을 스킬 기본값으로 추가하지 않았다.
