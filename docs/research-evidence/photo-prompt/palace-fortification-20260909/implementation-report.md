# 궁전·성채 시각 의미 데이터 반영과 독립 생성 검증

2026-09-09. 기준 커밋: `29d4d42a4114922991e3e0678c458c164a43124b`. 사용자 요청에 따라 조사안을 운영 데이터에 반영하고, 서로의 컨셉과 프롬프트를 공유하지 않은 서브에이전트 세 개가 첨부 인물 이미지를 참조해 각각 한 번 생성했다. 결과 판정은 아래 실행 증거와 함께 읽는다.

## 반영 범위

- 시각 프로필 34개, 프로필별 관찰 가능한 관계 3개, 총 102개 픽셀 기준.
- location 후보 34개, composition 후보 34개, 총 68개. 선택 가능한 관계 묶음 34개.
- 프로필 레지스트리 및 연구 확장 로더 연결, 필수 확장 목록 추가.
- 시각 프로필 인덱스 437개/정확 용어 1,942개, Gemini 의미 검색 인덱스 8,378개/768차원 재생성. 신규 후보 68개 전부 인덱스 포함 및 사전 해시 일치 확인.
- 사료 출처, 역사적 범위, 주장 한계는 연구 문서·유지관리 기록에 두고 긍정 프롬프트 후보의 검색 텍스트에 섞지 않았다.

궁전·고성·성채 같은 넓은 이름만으로 해자, 총안, 금박, 폐허나 특정 시대를 강제하지 않는다. 선택된 변형의 세 구성 관계를 모두 명시한 요청만 필수 프로필로 활성화하며, 의미 검색 결과와 에이전트가 추가한 해석은 선택 사항으로 남는다. 건축 프로필은 인물 없는 장면에도 사용할 수 있다.

세부 목록은 [profile-matrix.md](profile-matrix.md), 근거는 [research-report.md](research-report.md), 설치 소스는 [install-runtime.py](install-runtime.py)에 있다. 이전 `artifact-check.json`은 반영 전 연구 산출물의 검사 스냅샷이며 현재 구현 검사로 해석하지 않는다.

## 검증 수준

데이터 등록, 검색 결과, 실제 프롬프트 채택, 생성 이미지, 사용자 미적 판단을 분리한다. 하나의 필수 픽셀 기준이 부분 충족이면 해당 이미지의 종합 판정은 실패다. 참조 인물의 외형 유사성은 시각 비교이며 신원 인증이 아니다. 기본 프롬프트에 이미 존재한 관계가 잘 그려졌다는 이유로 새 데이터의 인과적 개선 효과를 주장하지 않는다.

공통 실행 자료: `artifacts/photo-runs/20260909-palace-three-arm-v1/`.
참조 이미지 SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.

## 데이터 및 통합 검사

- 전용 회귀 검사 6개 통과: 34개 프로필의 완전 관계/구성 요소 누락, 동음이의어·부정·넓은 양식어, 포트컬리스와 도개교 구분 및 공존, 의미 검색의 강제 승격 방지, 잠긴 차원/불완전 묶음, 유지관리 해시와 출처 누출 방지.
- 사전 메타데이터 검사 통과. 장면 표현 라우팅 감사 112/112 통과. 이는 등록/라우팅 검사이며 픽셀 증거가 아니다.
- 시각 프로필 인덱스 `--check` 통과. 실제 의미 인덱스의 사전 해시 및 신규 68개 문서 포함 통과: `runtime-verification.json`.
- 자연어 6개 질의의 BM25F 상위 12개에서 관련 신규 후보 검색 확인: `retrieval-diagnostic.json`. 이 검사는 실제 후보팩의 노출·채택을 대신하지 않는다.
- 기존 초기 회귀 37개 메서드 실행에서 실패 12건. 해당 beastkin/golden 검사 12개 메서드를 수정 전 커밋의 별도 추출본에서도 실행해 같은 실패 사례 12건을 재현했다. 스냅샷의 실제 출력까지 전부 동일하다는 뜻은 아니다. `early-regression.log`, `baseline-regression.log` 참조.
- 전체 테스트 수집은 76개 모듈/1,119개 메서드였다. 전체 실행은 중단했으므로 전체 회귀 통과를 주장하지 않는다. 검색·후보 통합 검사 18개는 별도 실행해 통과했다. 새 묶음 34개와 유지관리 기록 1개 추가에 맞춰 기존 개수 스냅샷을 151→185, 13→14로 갱신한 뒤 재검증했다. 원래 실패 로그도 남겼다. `full-tests.log`, `integration-regression.log`, `integration-regression-final.log` 참조.

## 독립 세 실행

각 에이전트는 원문 요청 envelope, 무작위 선택값, baseline, authorial core, intent lock, 필수 픽셀 기준을 후보 검색 전에 저장했다. 코어를 바꿔 신규 데이터 노출을 유도하지 않았다. 각 실행의 프롬프트 작성·감사·실제 이미지·판정·해시는 자신의 arm 디렉터리에 있다.

| 실행 | 독립 컨셉 | 신규 데이터 노출 및 채택 |
|---|---|---|
| A | 안개가 걷히는 성문에서 말린 리넨 배너를 운반하는 섬유 보존가; 반쯤 내린 포트컬리스와 쌍탑 성문 | `pf_portcullis`, `pf_gate_sequence` 프로필 노출. 포트컬리스 채택; 코어에 없던 외곽 방어구역을 요구하는 gate_sequence 거절 |
| B | 겨울 아침 궁전의 목재 패널 벽과 깊은 창가 좌석; 바이올린 케이스를 콘솔에 내려놓는 인물 | `pf_rocaille_boiserie`, `pf_window_seat` 노출. 창가 좌석 채택; 직사각 목재 패널에 불필요한 rocaille 조개·거울 조건 거절 |
| C | 나스르 양식에서 영감을 받은 수로·회랑 중정에서 식물을 그리는 삽화가 | 신규 프로필 노출·채택 없음. 기본 프롬프트의 수로·회랑 구현만 평가 가능 |

신규 슬롯 후보와 묶음은 세 후보팩 모두 노출 0개다. 따라서 이번 생성 실험은 후보팩 신규 슬롯/묶음의 실제 채택 효과를 입증하지 못한다. 등록·검색 가능성과 생성 단계 노출은 구분해야 한다. 선택하지 않은 프로필까지 장면의 필수 조건으로 승격하지 않았다.

픽셀 결과와 종합 결정은 아래와 같다.

## 실제 픽셀 결과

각 원본을 담당 에이전트가 저장 후 열어 판정했고, 조정자도 세 저장 이미지를 열어 교차 검토했다. A에서 수직 홈의 존재와 격자-홈의 접속을 구분해 재확인했다. 조정자 기록: `coordinator-pixel-review.json`.

| 실행 | 사전 고정 게이트 | 선택 신규 프로필 게이트 | 전체 판정 | 실패한 관찰 관계 |
|---|---:|---:|---|---|
| A | 4/5 | 포트컬리스 1/3 | FAIL | 아치 밖의 수직 트랙과 안쪽 격자 끝이 떨어져 있어 양끝이 홈 안에 들어가는 접속과 그 홈을 따른 하강을 확인할 수 없음 |
| B | 3/5 | 창가 좌석 2/3 | FAIL | 오른쪽 reveal이 프레임 밖; 바이올린 케이스 주 손잡이가 아닌 작은 끝 고리에 손이 닿음 |
| C | 4/5 | 선택 없음 | FAIL | 수로·회랑은 보이지만 드레스 하단이 잘려 전신 구도 미충족 |

합계는 사전 기준 11/15 충족, 이미지 단위 0/3 통과다. 세 프롬프트/런타임 감사가 통과했어도 이 픽셀 결과를 대체하지 않는다. A/B의 선택 프로필 픽셀 감사에는 스키마 오류가 없으며 기술 기준 실패가 그대로 보존됐다. C는 선택 프로필이 없어 사전에 고정한 실행별 기준으로 판정했다.

### 생성 이미지와 프롬프트

A — [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-a/final-prompt.txt), [픽셀 리뷰](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-a/pixel-review.json)

![A 성문과 섬유 보존가](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-a/generated.png)

B — [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-b/final-prompt.txt), [픽셀 리뷰](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-b/pixel-review.json)

![B 목재 패널과 창가 좌석](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-b/generated.png)

C — [프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-c/final-prompt.txt), [픽셀 리뷰](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-c/pixel-review.json)

![C 수로와 회랑 중정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260909-palace-three-arm-v1/arm-c/generated.png)

## 결론과 남은 개선 과제

데이터 반영과 독립 세 번의 생성·검증은 완료했다. 운영 등록과 선택 프로필의 프롬프트 반영은 확인했지만, 이번 실험에서 완전한 픽셀 성공과 신규 슬롯/묶음의 채택 효과는 확인하지 못했다. 따라서 데이터 전체를 렌더 검증 완료 또는 품질 개선 입증으로 승격하지 않는다. 사용자 미적 판단도 미수집 상태다. `improvement-iteration.json`의 결정은 `implemented`, 렌더 평가는 `fail`이다.

후속 과제는 서로 구분한다. (1) 정상 후보팩에서 새 슬롯/묶음이 노출되지 않는 구간을 실제 검색·선별 기록으로 좁힌다. 독립 자연어 검색에서는 관련 후보가 검색됐으므로 인덱스 누락으로 단정하지 않는다. (2) 관계 양 끝의 접속과 양측 reveal을 한 프레임에서 볼 수 있는 구도를 다음 별도 실험으로 검증한다. (3) 같은 조건의 수정 전/후 통제 생성 없이 데이터의 인과적 개선을 주장하지 않는다. 이번 고정 실행을 성공할 때까지 재생성하거나 기존 결과를 대체하지 않았다.
