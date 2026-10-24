# 영지물 실패 보완과 동일 컨셉 재시험

2026-10-24, Asia/Seoul. **동일 첨부 이미지·동일 세 컨셉으로 독립 서브에이전트 3개가 각각 한 번씩 다시 생성했다. 주제는 3/3에서 읽히지만 엄격한 전체 장면 통과는 이전 0/3 → 이번 0/3이다.** 부분 개선과 잔여 실패를 아래처럼 구분한다. 기본 검색본의 보류 적용과 검증도 완료했다.

## 실패 원인과 반영한 보완

[원인 분석](CAUSE-ANALYSIS.md)은 실제 픽셀 결함과 원인 가설을 구분한다. 원래 실패는 A의 가려진 운반 경로·배수 끝점·접지 및 잘못된 시선 대상, B의 서로 다른 구획 지시·경계 가림·다른 기록 면, C의 숨은 손 접점·과도하게 벌어진 빵이다. 소품을 더 나열하기보다 **행위자 → 손/시선 → 실제 대상 → 접점/연결 → 카메라에서의 가시성**을 분리했다. 가려진 해부학적 오류나 인물의 의도·신분·법적 유효성을 추정하지 않는다.

새로운 선택형 시각 자료 8건과 역할 연결 21건을 등록했다. 자료는 길의 합류점, 배수의 양 끝, 같은 작업 대상의 시선, 같은 지도 구획, 지도와 제본 장부 대응, 실제 펜 접촉, 네 손의 지지, 작은 빵 균열을 구체화한다. 의미 sidecar에는 혼동 경계와 실패 관찰·판정·출처를 연결했다. **재시험 후 R04를 보류 진단으로 바꿔 최종 긍정 후보는 7건, 진단 1건이다.** R04의 원래 한영 문장과 조건·effects·출처 및 21개 연결 행은 보존했다. [변경 수량](DATA-REPAIRS.json), [카드–후보 대응](card-candidate-map.json), [R04 보류 결정](runtime-r04-hold-rebased/hold-decision.json).

R04는 두 사람에게 연결된 손가락이 불투명한 탁상 지도의 닫힌 구획 내부 두 점에 닿으면서 외곽 전체가 가려지지 않는 구도다. 이번 B에서 경계가 실제로 가려졌고 공존 가능한 투영을 확인하지 못했다. 반복 문장으로 해결됐다고 간주하지 않고 긍정 검색에서 보류했다. 이는 모든 가능한 구도의 기하학적 불가능성을 증명한 것이 아니며, 원래의 전체 경계 판정을 완화하지 않는다.

- [보완 후보 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_estate_visibility_repairs_20261024.json)
- [21개 역할 연결](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_estate_visibility_repair_bindings_20261024.json)
- [보완 의미·관찰 sidecar](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_estate_management_repair_semantics_20261024.json)
- [영지물 참조 문서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/estate-management-semantics.md)

기존 영지물 후보 78건·연결 56건·기존 의미 sidecar는 원래 해시를 유지한다. 재시험에 쓴 8개 긍정 후보 스냅샷은 불변으로 보존하고, 이후의 R04 보류는 새 소스/기본 검색 세대로 구분했다. 이번 이미지가 보류 후 검색본에서 생성됐다는 뜻은 아니다.

입력 계보의 재바인딩 오류도 수정했다. 부모의 고정 입력·행위·외모는 유지하면서 새 child의 실제 scope inventory 증거 해시만 엄격하게 다시 연결하고, 부모 감사는 부모의 전체 검증된 봉인 런타임에서 수행한다. 정책이나 이미지 판정 기준을 낮추지 않았다. 새 [16개 회귀 검사](retry-rebinding-tests.txt)와 기존 [30개 retry 정책 검사](retry-policy-tests.txt)가 통과했다. [시험/정본 코드 동등성](test-working-code-equivalence.json)은 미사용 import를 제외한 AST 일치를 확인한다.

## 독립 작성과 최신 스킬

세 최종 작성자는 무이력의 별도 컨텍스트·run 디렉터리에서 원래 컨셉·action·참조 외모를 보존하는 닫힌 projection을 받아 코어를 확정했다. 코어 동결 뒤에만 후보를 검색했고 다른 arm 프롬프트나 이미지를 전달하지 않았다. C 준비 세션 하나는 다른 arm 요약 노출을 발견해 작성·검색·생성 없이 종료하고 깨끗한 새 세션으로 교체했다. A에서 저작 후 확인한 다른 arm의 처리 상태 메타데이터도 실행 기록에 공개했으며, 다른 arm의 프롬프트·픽셀을 작성에 사용하지 않았다. 이 절차 기록은 접근할 수 없는 내부 상태의 독립성을 증명하지 않는다. [검색 전 동결](pre-retrieval-independent-freeze.json).

세 작성자는 생성 직전 최신 [스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)을 읽고 SHA `e26f7fbefab8a3385ceb1780909513544d8deb011efd390cbb545e43b0b49cf9`의 실제 snapshot을 보존했다. 이 개정의 새 rank-anchor 샘플링 정책은 이미 발급된 과거 receipt를 유지한다. 이번 조회는 개정 전에 동결·발급된 uniform receipt를 그대로 사용했으며, **이번 이미지가 새 rank-anchor 정책을 시험했다는 주장은 하지 않는다.** seed 변경·재검색·강제 후보 주입은 없다.

참조 이미지 SHA는 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`로 세 arm 모두 같다. 얼굴·짙은 단발·앞머리의 외형만 참조했고 실존 신원·연령·배경을 확정하지 않는다.

고정 재시험 검색본은 H-F2 `90792f0673868e3286cf7ddb36bf49a558f43111dc780a1fdd21340708d83c60`, native `1a72bf0aef2060ffde2c7b07de4c97a8eaefd13878744109e2ad7242b08ece4e`다. 전체 설치 검증을 통과한 동일본을 세 arm이 명시적으로 사용했다. 후속 기본 검색본과 혼동하지 않는다.

## 실제 자연 검색과 사용

| Arm | goal / 반환 occurrence / 고유 원문 | 노출된 보완 카드 | 최종 사용 |
|---|---|---|---|
| A | 4 / 25 / 23 | R02, R03, R07 | 독립 수정 baseline 유지, 보완 자료 채택 0 |
| B | 7 / 40 / 37 | R04, R07 | 일반 overcast 조명 1건 영감, 보완 자료 채택 0 |
| C | 5 / 32 / 31 | R07 | 독립 수정 baseline 유지, 보완 자료 채택 0 |

세 arm 모두 native chosen CID는 0이다. 보완 자료 4/8 카드만 한 arm 이상에 노출됐고 R01·R05·R06·R08은 미노출이다. 독립 수정 프롬프트에 유사 관계가 있어도 미채택 자료의 사용 효과로 계산하지 않는다. [실제 노출](actual-agent-retrieval-exposure.json), [빈 결과와 query projection](actual-query-projections.json).

B의 contact_point/prop_placement와 C의 hand_pose는 공개 scope projection에서 후보가 0개였고 이를 보존했다. 참조형 topic 문구에서 일반 학교·아이돌 등의 잡음이 생긴 것도 기록했다. 다음 개선에서는 실제 이전 사용자 주제 바이트의 적법한 문맥 연결을 검토할 수 있지만, 이번 조회를 사후 수정하지 않았다. **이번 실험으로 데이터 추가 자체의 인과 효과는 확인되지 않았다.**

## 실제 이미지 결과

내장 이미지 도구로 새 호출 3회, 새 이미지 3장, arm별 1회다. 도구는 실제 모델 버전을 반환하지 않았으므로 특정 모델명으로 실제 호출을 단정하지 않는다. 세 PNG 검증과 첨부 해시·최종 프롬프트·native runtime 프롬프트·계획 해시·원장·부모 retry ID를 교차 확인했고 각 arm의 bound artifact 32개도 해시 일치를 확인했다. 세 정식 리뷰는 모두 `record_valid=true`, `technical_qualification=fail`이다. 유효한 감사·원장이 픽셀 통과를 뜻하지 않는다. [호출·계보·해시 종합 검사](three-image-integrity.json).

| 컨셉 | 실제 개선 | 남은 실패와 작성 단계 문제 | 엄격 전체 판정 |
|---|---|---|---|
| A · 가동 중인 곡물 타작장 점검 | 완전한 부츠 윤곽·일반 접지, 배수 출구의 물줄기와 낮은 젖은 땅이 보임. 현장 책임자의 얼굴이 작업 방향으로 향함 | 길의 실제 합류점은 가림. 특정 수레를 보는 시선은 확정 불가. 부츠는 지정된 돌바닥 대신 인접 흙·자갈 길에 닿음. 새 baseline이 현장 도면을 장부판으로 대체해 도면 대응 검사가 빠짐 | FAIL |
| B · 토지 경계 청원과 도면·장부 대조 | 두 손가락이 같은 amber 구획 안의 점을 지시. 관리자 시선은 청원자에게 향함 | 손·팔이 닫힌 경계 일부를 가림. 서기관은 뒤의 별도 작은 책에 씀. 앞쪽 도면 장부에 향하는 펜은 청원자가 들어 소유자·대상·대응 행 관계 실패 | FAIL |
| C · 공동 화덕에서 빵을 건네는 주민 만남 | 화덕·빵·곡물·기록과 공동 전달 장면은 읽힘 | 네 손 중 뒤쪽 두 손목·접점 연결은 가림. 깊은 V형 벌어짐은 작은 시작 균열이 아님. 기존 A07의 별도 뚜껑 닫힌 곡물함은 새 baseline에서 미유지 | FAIL |

A의 기존 두 수레와 현장 도면, C의 완전한 A07 곡물함 구도는 이번 baseline에서 일부 빠졌다. 이는 **실험 비교 범위의 회귀**이며 모두를 사용자 소유의 새 필수 조건으로 소급하지 않는다. A가 한 수레만 지정했으므로 두 번째 수레 미출현을 별도 모델 수량 실패로 세지 않는다. C의 닫힌 곡물함도 새 필수 gate로 세지 않고 `NOT_RETAINED`로 기록했다. 기존 C의 A07 한 사례 통과가 이번 이미지에서도 유지됐다고 주장하지 않는다. [기존 소스 관계 회귀](prior-source-regressions.json).

정식 일반/신체 gate는 A 6 PASS·3 FAIL, B 6 PASS·3 FAIL, C 2 PASS·7 FAIL이다. 서로 다른 장면 기준이므로 이를 합산한 공통 정확도는 계산하지 않는다. 보이지 않는 손을 해부학적 오류로 진단하지 않으며, A의 근처 지면 접지는 정확히 선언된 돌바닥과의 접지로 승격하지 않는다. 총괄은 실제 원본 PNG를 별도로 보았다. B/C는 작성자의 예비 관찰을 볼 수 있어 블라인드 평가가 아니다.

### A · 타작장 점검

![A 재시험](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-repair-a/images/result.png)

[실제 최종 프롬프트](final-prompts/a.txt) · [총괄 픽셀 관찰](independent-pixel-review-a.json)

### B · 토지 경계 청원

![B 재시험](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-repair-b/results/estate-boundary-repair-b.png)

[실제 최종 프롬프트](final-prompts/b.txt) · [총괄 픽셀 관찰](independent-pixel-review-b.json)

### C · 공동 화덕의 빵 전달

![C 재시험](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-repair-c/result.png)

[실제 최종 프롬프트](final-prompts/c.txt) · [총괄 픽셀 관찰](independent-pixel-review-c.json)

## 남은 실패의 프롬프트 보완

세 작성자는 자신의 결과를 본 뒤 구체적인 영어 교체 문장과 구도 수리를 작성했다. A는 원래 계획 소유자·대응 도면과 노출된 길 합류점·실제 돌 접지, B는 서기관→펜→동일 도면 장부 행의 연속 배치, C는 네 손바닥의 가로 한 줄과 독립 손목 통로·작은 윗균열·넓은 아랫껍질 연결부를 제안했다. 각 제안과 허용 의미 검토는 [후속 프롬프트 보완안](FOLLOWUP-PROMPT-REPAIRS.md)에 연결했다. **이 후속 초안은 미생성·미감사이며 추가 호출은 0회다.** 이미 실패한 출력·판정·동결 프롬프트를 사후 수정하지 않는다.

`partial_is_fail`, `UNOBSERVABLE_NOT_PASS`, `BLOCKED_UNSCORED`를 유지한다. 주제 유사성은 3/3이지만 엄격한 전체 장면은 0/3이고 native 자료 자격 부여는 0건이다. 장면당 한 장, 짝지은 대조 이미지 없는 검사이므로 전체 정확도·일반화·데이터 단독 개선을 입증하지 않는다. 원 연구의 계획 192건은 실행하지 않았다. 사용자 미적 수용은 피드백 전까지 `PENDING`이다. 커밋·푸시는 하지 않았다.

## 기본 검색본의 최종 반영과 검증

R04 보류 처리를 반영한 최종 기본 검색본을 전체 검증 후 선택했다.

- H-F2: `7d6ced82dd73dbab01fc84770319b583a20a4e893bfe9c102c5bb82341eafeb5`
- native: `0e0b1295bab55f295f9c7e58f865b612b8f24c57a665350ded7aab03850d9ff0`
- 커널 SHA: `d5d1e66c30d4569764d501637f6122dfa92a5c7f49b57be89a434891fa839ecf`
- 새 계열 최종 긍정 후보 7건 인덱스 포함, R04 진단 1건 긍정 검색 제외. 8개 소스 원문 왕복 일치, 연결 21개 행 일치.
- 이 변경 직전 기본본의 다른 source module 107개와 모든 봉인 코드 바이트를 보존했다. 같은 보완 모듈 안의 나머지 7개 레코드도 그대로다. R04의 한영 문장·조건·effects·출처는 유지했다.
- 실제 설치본의 Python·recorder 호환 검사와 배포된 H-F2/native 전체 검증이 통과했다. `CURRENT` 직접 쓰기는 0회다.
- 유지보수 조회 12개에서 긍정 표적 7개는 모두 1위/표시 상위 8개에 포함됐고, 보류 R04의 긍정 노출은 0이다. 일반 대조 4개에는 이 새 긍정 계열이 표시되지 않았다. 이는 자료에 가까운 표현의 소스/검색 점검이며 독립 검색 성능 평가나 실제 arm의 채택·픽셀 성공이 아니다.

동시 기본본 변경을 발견한 오래된 활성화는 중단했고, 최신 메카 소스와 rank-anchor 코드를 보존한 기준 위에 **단일 R04 보류 변경만** 다시 만들었다. 처음의 8개 긍정 테스트본과 후속 기본본을 분리한다. 최종 기본본에서 이미지를 또 생성하지 않았다.

[최종 기본 선택](DEFAULT-PUBLICATION-TARGET.json) · [전체 설치 검증](runtime-r04-hold-rebased/install-active.json) · [설치본 실행 호환 검사](runtime-r04-hold-rebased/runtime-check.json) · [원문·코드 보존](runtime-r04-hold-rebased/final-source-preservation.json) · [실제 유지보수 조회](runtime-r04-hold-rebased/runtime-probes.json) · [완료 기록](FINAL-RESULT.json)
