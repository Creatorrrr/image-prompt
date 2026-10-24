# 해병문학 데이터 보완 및 독립 3개 재시험

보완 후 같은 첨부 사진으로 독립 에이전트 3개가 서로 다른 무작위 컨셉을 작성하고 이미지를 각 1회 생성했다. **신규 자료의 일반 속성은 A 한 장에서 프롬프트→실제 도구 입력→원본 픽셀까지 확인했다. 신규 카드 전체 자격은 0/3, 전체 프롬프트·엄격한 픽셀 합격도 0/3이다.** 세 장 모두 참조의 관찰 가능한 얼굴·머리 외형은 반영됐다.

## 원인과 실제 보완

검색 실패는 등록 누락 하나가 아니었다. 장르 의미와 업무 지시가 섞인 질의, 짧은 영어 사물명 부족, 상위 32개 창 밖의 낮은 순위, 창 안 자료의 균등 8개 표본 미노출, 노출 자료의 조건·소유자·장면 부적합을 구분했다. 주제를 정확한 원문 부분 `해병문학`으로 인용하고 87개 후보의 영어 명칭을 보강했다. 시각 의미 자료에는 인물 기준 좌우, 전체 연결, 지지면, 그림자 수신면을 확인하는 안내를 추가했다. 기존 관찰 계약과 게이트는 보존했고 진단 247개를 긍정 후보로 승격하지 않았다.

같은 코퍼스·구현·질의에서 이름/검색 문서/임베딩만 교체한 오프라인 비교에서 이전 실제 12질의의 신규 후보 출현 합계가 top-8 **0→7**, top-32 **4→18**로 늘었다. 이번 독립 슬롯·초안 12질의는 top-8 **0→3**, top-32 **0→5**였다. 이는 후보 출현 합계이며 채택률이나 독립 holdout 정확도가 아니다. 정확한 주제로 좁혀도 장르 검색 자체의 의미 구별은 아직 약하다.

[상세 원인·통제 비교·절차 한계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/ANALYSIS.md) · [검색 비교 원자료](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/retrieval-ablation.json) · [87개 계약 보존 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/source-repair-verification.json)

## 실제 원본 판정

|시험|신규 고유 노출|신규 데이터의 최종 기여|참조 외형|전체 픽셀|증거|
|---|---:|---|---|---|---|
|[A: 빈 표창의 치수 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/a/report.md)|2|일반 속성 1건: 액자 레일 안 APPROVED|PASS|FAIL: 자 중앙 쥠·시선 불일치|[원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/marine-literature-retest-20261024-a-v5/original.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/a/final-prompt.txt)|
|[B: 수건 검수 의례](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/b/report.md)|0|신규 노출 0, 전이 미입증|PASS|FAIL: 두 번째 지지 손바닥 가림|[원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/marine-literature-retest-20261024-b-v5/original.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/b/exact-prompt.txt)|
|[C: 청소 직후 다시 생기는 발자국](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/report.md)|0|신규 노출 0, 전이 미입증|PASS|FAIL: 도착자 두 번째 발·외부 지지점 프레임 밖|[원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/marine-literature-retest-20261024-c-v5/original.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/final-prompt.txt)|

A의 신규 V090은 물리적 운반체 내부에 글자를 두는 일반 속성만 참고했다. 원래 표어판 카드의 모든 인물·조건·구성을 채택한 것은 아니다. `APPROVED`가 기준 초안에 없고 최종 문구와 실제 원본의 액자 아랫레일에 있음을 확인했다. A의 보수적인 전체 카드 거절은 작성자의 경계 판단이며, typed 성인 조건의 자동 충돌이 입증됐다는 뜻은 아니다.

B와 C는 신규 후보가 최종 표본에 없었다. 원래 초안의 병영·의례·작업복·복도나 기존 자료의 발밑 음영을 신규 전이로 세지 않았다. 일반적인 군대 풍자 분위기만으로 해병문학의 고유 주제가 성공했다고 판정하지 않았다. 일부 성공한 접촉을 전체 연결 성공으로 올리지 않았으며 `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지했다.

## 실행·검증 경계

- 후보 접근 전 독립 컨셉·기준 초안·controls·픽셀 기준을 작성했다. 제목의 업무 표현 혼입을 이미지 호출 전에 고치면서 원래 초안·슬롯 질의 문자를 유지했다. 따라서 마지막 v5를 새 눈가림 저술시험으로 부르지 않는다. 새 관리 표본 seed도 달라져 전후 노출 차이를 주제 수정 단독 효과로 주장하지 않는다.
- 최종 3개 run의 스킬 pin은 `83b3239eda5b5e26b1c51dad268258eb21a24f3dbca3b814517eb89169390cb8`이고 당시 실제 설치된 고정 세대 `af8d87d5a4f61d4f6f93734d05ef4899da9de01159e53a1e6e840c2bc3d48bff`를 사용했다. 생성 종료 후 다른 작업이 스킬 문서와 기본 선택자를 추가 갱신했다. 그 후속 버전을 이번 이미지로 검증했다고 주장하지 않는다.
- 각 run의 감사 프롬프트·runtime 문구·native plan·실제 호출 기록이 동일하고, 같은 JPEG 경로와 SHA를 사용했다. 저장 PNG는 도구 반환 원본과 바이트가 같다. 실제 이미지 도구 호출은 총 3회이며 반환되지 않은 모델 ID는 unknown이다.
- 의미/범위 회귀 13개 통과, 신규 87개 색인 등록, 진단 긍정 누출 0, 원본/네이티브 소스 334개 왕복 동일성을 확인했다. 리뷰 기록 유효성과 픽셀 합격은 별개다. 세 기록은 유효하지만 기술 자격은 모두 실패다.
- C 원래 ledger의 스킬 해시 오기입은 원본을 보존하고 명시적 append 보정했다. 별도 보정 ledger는 같은 실제 시도의 메타데이터 사본이며 4번째 이미지 생성이 아니다.

[전체 전이·호출·해시 집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/test-results-summary.json) · [root 원본 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/root-pixel-review.json) · [C 메타데이터 보정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/metadata-correction.append.json)

## 반영 상태와 남은 개선

후보·시각 의미 소스와 작업 인덱스에는 보완을 적용했다. 실제 시험 세대와 추가 합본 세대는 설치해 두었다. 기본 런타임 선택자는 동시 작업의 새 소스 발행을 덮어쓰지 않도록 교체를 보류했다. 최종 관찰의 기본 세대 `ba9fcdc839a29e99ca3dab3ac83aba713665ed6ede9122f60af649042234f5e4`에서 이번 신규 CID는 0개다. 작업 인덱스 활성화 때는 입력 120개가 정확했지만 이후 동시 소스 변경 1개가 있으므로 최신 전체 소스와 일치한다고 주장하지 않는다. 시점별 값과 경계는 [최종 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/FINAL-STATE.json)에 남겼다.

다음 데이터 개선은 (1) 장르명과 관찰 가능한 병영 관계를 연결하는 출처 기반 의미 설명을 독립 질의로 검증하고, (2) 카드 전체의 연령/소유자 조건과 실제 속성별 조건을 감사해 과도한 포괄 조건을 분리하며, (3) 나이가 필요 없는 비성적 사물 관계는 별도 자격을 가진 자료로 작성하는 순서가 적절하다. 기존 카드의 성인 조건을 조용히 지우거나 일부 속성으로 전체 자격을 부여하지 않는다. 다음 이미지에서는 A의 기하학적 중앙과 시선 목표, B의 양 손바닥 노출, C의 두 발과 외부 계단을 각각 구도에서 확보해야 한다. 이 항목들은 이번에 완료한 수정으로 세지 않는다.

이번 요청의 분석·보완·3개 실제 생성·원본 검증은 완료했으며, 데이터와 이미지의 전체 합격은 미달이다. 사용자 수락은 아직 받지 않았다.
