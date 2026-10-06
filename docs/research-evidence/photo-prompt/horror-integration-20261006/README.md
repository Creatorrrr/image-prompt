# 호러 데이터 반영과 독립 이미지 검증

시각 의미와 후보 데이터를 주 작업 폴더에 반영하고 현재 실행용 버전으로 게시했다. 세 독립 에이전트가 첨부 사진을 활용해 서로 다른 복잡한 장면을 작성·생성했고, 원본 픽셀을 검증했다. 핵심 주제는 세 장면에서 확인됐다. 전체 필수 검증은 A/B 통과, C 미통과다.

## 실제 반영

- 새 후보 155개, 새 시각 의미 프로필 155개, 선택형 묶음 11개.
- 전체 후보 10,403개, 시각 의미 프로필 2,236개, 묶음 1,007개. 두 인덱스를 현재 데이터에 맞춰 갱신했다.
- 기존 유사 항목 21개를 완전한 동의어로 치환하지 않았다. 조사상의 조합 예시 6개는 선택형 묶음에 대응한다. 나머지 68개는 비시각적 맥락·소리·시간 변화·비평 주제·미검증 문화 변형으로 보존했다. 민속 변형 6개와 이를 요구하는 묶음 1개는 보류했다.
- 후보에는 한국어 해석, 영어의 관찰 가능한 전체 명제, 구성 요소, 관계, 속성 범위 및 혼동 경계를 넣었다. 장르명이나 근접 검색이 사용자 요구를 새로 만들지 않는다. 선택하면 모든 비교 대상과 구성 요소를 보존해야 한다.

[반영 대응표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/ADOPTION-MAP.json) · [이미지 검증에 사용한 게시 버전](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/PRIMARY-RUNTIME-PUBLICATION-FINAL.json) · [소스 해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/INTEGRATED-SOURCE-HASHES-FINAL.json)

## 최종 실행 버전 확인

이미지 검증 기록은 실제 사용한 고정 버전 `d947d6b6`에 연결돼 있다. 반영 후 다른 작업에서 기존 색 관계·의복 표면 데이터 등 15개 파일이 변경됐으며 이 변경은 보존했다. 현재 주 작업 폴더는 새 게시 버전 `11a2c533`(revision 11)으로 실행되고, 현재 소스와 실행 버전의 일치 및 소스 검증을 확인했다. 이번 호러 소스 두 파일과 `SKILL.md`는 이미지 검증에 사용한 버전과 바이트가 같다. 현재 주 작업 폴더에서도 호러 전용 테스트 10개가 모두 통과했다. 이전 이미지의 검색 영수증을 새 버전으로 다시 해석하지 않았다.

[현재 주 작업 폴더 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/PRIMARY-LIVE-STATE.json) · [최종 전달 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/DELIVERY-VALIDATION.json) · [현재 소스 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/primary-live-source-validation.log) · [현재 호러 테스트 재확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/primary-live-horror-recheck.log)

## 검색에서 발견한 문제와 보완

첫 독립 검색에서 A는 새 거울 후보를 찾았지만 B/C는 해당 공동체 경계·조직/금속 접합 프로필을 찾지 못했다. 추가 인물·물체를 주 피사체 변경으로 너무 넓게 선언한 속성 범위와, 구성 요소당 한 개의 긴 표현만 허용한 발견 어휘가 원인이었다. 실제 변경 대상의 범위와 15개 주요 관계의 일반적인 대체 표현을 보완했다. 강제 활성화 용어, 선택 후 모든 증거 요건, 원본 픽셀 기준은 그대로 유지했다.

요청·코어·창작 설정을 바꾸지 않고 새 게시 버전으로 다시 검색하자 B/C의 핵심 프로필이 노출됐다. 초기 실패도 보존했다. 이 재실행은 보완 후 개발 검증이며 새 블라인드 표본으로 주장하지 않는다.

[초기 보완 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/ADMISSION-REVISION.initial.json) · [추가 소유자 범위 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/ADMISSION-REVISION.json) · [입력 바이트 동일성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/INPUT-REPLAY-INTEGRITY.json) · [독립성 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/INDEPENDENCE-RECORD.json)

## 원본 이미지 결과

| 테스트 | 이번 추가 데이터의 핵심 관계 | 필수 픽셀 검증 | 전체 기술 판정 |
|---|---|---|---|
| A — 침수 창고와 거울 | 실제 두 손의 상자 지지 / 반사 속 펼친 손의 불일치, 새 후보 구성 요소 3/3 | 10/10 | 통과 |
| B — 밝은 과수원의 공동체 | 공동체의 안쪽 경계 / 바깥 방문자 / 제한된 이동 경로, 새 프로필 3/3 | 8/8 | 통과 |
| C — 승강기와 신체·금속 접합 | 같은 몸에서 피부·금속 구조가 연속, 새 프로필 2/2 | 첫 결과와 교정본 모두 6/7 | 실패 |

C는 골반이 가드레일에 눌려 지탱되는 접촉을 확인할 수 없어 `UNOBSERVABLE_NOT_PASS`다. 한 번 교정해 지지물을 추가했지만 실제 접촉은 계속 가려졌다. 두 시도의 원본·감사·ledger를 보존했다.

A는 새 후보를 실제로 채택했지만 새 `hvr_profile_`는 노출되지 않았다. 기존의 호환되는 언캐니 프로필이 정식 픽셀 기준을 제공했고, 새 후보의 세 구성 요소와 관계는 별도로 확인했다. B/C는 새 시각 의미 프로필의 전체 계약을 실제로 선택했다.

![A — 거울의 손동작 불일치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/images/A-mirror.png)

[A 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/prompts/A.txt) · [A 전체 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/qualification/arm-a/qualification_report.md)

![B — 공동체와 이동 경계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/images/B-orchard.png)

[B 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/prompts/B.txt) · [B 전체 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/qualification/arm-b/qualification_report.md)

![C — 연속된 조직/금속 접합, 교정본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/images/C-junction-corrected.png)

[C 교정 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/prompts/C-corrected.txt) · [C 첫 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/images/C-junction-initial.png) · [C 전체 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/qualification/arm-c/qualification_summary.json) · [두 시도 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/qualification/arm-c/correction-attempt-2/attempt_comparison.json)

## 검증 범위

실제 네이티브 호출은 총 4회(A 1, B 1, C 2)이며, 반환된 실제 파일을 같은 바이트로 보존했다. 첨부 사진 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이고 얼굴·머리 외관을 참고했다. 피사체의 설정과 사건은 창작이다. 각 팔은 데이터 열람 전에 독립 장면과 입력을 동결했으며 다른 팔의 장면을 읽지 않았다. 요청 봉투는 에이전트 생성 후 전달됐지만 전원이 작성 전에 기다렸다. 이 순서 차이는 독립성 기록에 명시했다.

입력 감사와 코드 검증은 픽셀 판단과 구분했다. A/B의 픽셀 감사 종료 코드 1은 사용자 평가 대기를 포함한 도구 계약이며, 기록된 기술 자격은 충족한다. C는 실제 필수 게이트 미충족이다. 사용자 판단은 세 경우 모두 `not_yet_received`다. 공포 강도는 검토자의 정성 평가로 A/B의 인상은 절제된 수준이다. 그릇 재질·정확한 군중 배열·시선·층수·브레이크 미끄러짐 등 모든 서사 세부가 완전히 구현됐다고 주장하지 않는다.

후보 계약·시각 의미·실행 버전 신선도·새 호러 데이터에 대한 75개 테스트 범위를 확인했다. 전체 실행에서 74개 통과, 기존 유지보수 근거 파일 누락에 따른 실행 환경 오류 1개가 있었으며 해당 파일을 복사한 후 같은 테스트가 통과했다. 새 호러 전용 테스트는 10개이며 구성 요소 누락·잘못된 비교 대상·광범위 용어의 강제 활성화·잠긴 속성 침범을 검증한다. 소스 검증도 통과했다.

[전체 결과 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/RESULT.json) · [루트 원본 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/ROOT-PIXEL-REVIEW.json) · [회귀 실행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/focused-regression-final.log) · [누락 파일 재확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/maintenance-reference-recheck.log) · [새 호러 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/horror-data-tests-final.log) · [소스 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/horror-integration-20261006/source-validation-final.log)

현재 생성 사례는 세 핵심 주제와 보조 안개 관계까지 확인한다. 다른 151개 시각 해석의 네이티브 판정은 후속 검증 범위다. 기존 조사에서 계획한 22개 픽셀 그룹 전체가 완료됐다는 의미로 해석하지 않는다. 고유한 요청과 더 단순한 비교 구도로 새 표본을 작성해 확장하고, C는 지지 접촉을 가리지 않는 시점으로 물리적 관계부터 확인하는 것이 다음 단계다.
