# 유혹적 표현 요소: 대체 표현 보강·후보 반영·독립 이미지 검증

시각 의미 데이터와 후보 데이터에 반영했다. **대체 표현·소유·관계·효과 범위는 검증됐지만, 복잡한 장면 전체의 원본 픽셀 조건은 0/3 PASS**다. 일부 형태가 보인 것과 전체 조건 충족을 구분했다. 요청한 세 독립 서브에이전트가 서로 다른 장면을 설계하고, 같은 첨부 원본을 사용해 각각 네이티브 이미지 1개를 생성했다.

## 데이터에 반영한 내용

| 범위 | 실제 반영 |
| --- | --- |
| 기존 후보 | 88개 후보에 한·영 대체 표현 176개 추가 |
| 기존 시각 의미 | 14개 프로필의 전체 표현·구성 요소에 대체 표현 142개 추가 |
| 새로운 현재 형태 | 후보 15개, 시각 프로필 13개, 관찰 구성 요소 42개 추가 |
| 새로운 프로필의 표현 | 전체 표현 26개와 구성 요소 표현 84개 추가 |
| 선택적 묶음 | 10개 추가. 각 프로필의 활성화 근거는 독립적으로 판단 |
| 기존 효과 정보 | 10개 후보의 소유·영향 속성 정보를 보완. 기존 명칭·별칭·선행 조건 보존 |
| 검색 인덱스 | 후보 10,000개, 시각 프로필 1,787개와 정확 용어 4,167개에 맞춰 재생성·검증 |

대체 표현은 같은 관찰 형태를 다시 설명하도록 작성했다. 예를 들어 스퀸치는 “아래 눈꺼풀 가장자리가 올라와 열린 눈 틈을 좁히는 상태”, 반쯤 열린 눈은 “동공 일부가 보이는 좁아진 눈 틈”으로 구분했다. 윗눈꺼풀 우세 형태는 별도 후보·프로필로 추가했다. 손끝의 자기 볼 접촉, 손바닥이 떨어진 접촉, 턱 아래 공중 간격, 실제 하중이 걸리는 턱 받침도 구별했다.

라펠을 가볍게 만지는 상태와 옷 가장자리를 집는 상태, 이미 있는 펜던트를 잡는 상태는 접촉 대상·손의 소유·옷감 반응·선행 조건을 분리했다. 자기 머리카락 뒤에서 보이는 눈은 머리카락과 눈이 같은 인물에게 속해야 한다. 머리 방향과 눈 방향 후보에는 `head.orientation`과 `eyes.gaze_direction`의 영향 정보를 함께 선언했다.

각막 반사점은 현재 프레임의 반사 형태를 뜻한다. 젖음·젖지 않음·감정의 증거로 사용하지 않는다. 브로드/쇼트는 카메라·얼굴 회전·밝은 볼의 관계이고, 루프는 코 그림자와 볼 그림자 사이의 밝은 간격이다. 두 조명 관계가 동시에 요청되면 각각 충족해야 한다.

기존 14개 프로필의 정의, 활성화 조건, 필수 구성 요소 수, 필수 증거 필드, 픽셀 게이트는 그대로 보존했다. 넓은 분위기 단어가 새로운 정밀 형태의 하드 의무로 바뀌지 않는다. 정지 이미지로 입술을 훑는 전체 동작, 시선 이동 순서, 손짓의 반복·지속 시간이나 내적 의도를 증명하지 않는다.

원래 120개 용어 중 100개에는 직접 보강한 데이터와의 연결을 기록했다. 나머지 20개는 기존 범위·맥락·시간적 표현을 유지했다. **100개 연결은 검색 성공률이나 픽셀 검증률이 아니다.**

입력과 반영 근거: [120개 용어 연결표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/TERM-ADOPTION-LEDGER.json), [기존 후보 대체 표현](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/CANDIDATE-ALTERNATIVES.psv), [기존 프로필 전체 대체 표현](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/PROFILE-ALTERNATIVES.psv), [앞선 상세 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/TERM-RESEARCH.json).

주요 작성 데이터: [후보 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_seduction_expression_extension.json), [시각 의미 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_seduction_expression.json). 다른 기존 파일의 수정 범위와 해시는 [최종 반영 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/PRIMARY-INSTALLATION-FINAL.json)에 남겼다.

## 독립된 세 장면의 테스트

각 에이전트는 장소·역할·사건·자세·관찰 기준을 후보 데이터 접근 전에 정했다. 같은 요청 원문을 사용했고, 세부 테스트 형태는 에이전트가 설계한 조건으로 기록했다. 사용자 요구나 정의로 재분류하지 않았다. 첨부 이미지는 보이는 얼굴·머리 참고로 사용했으며, 장면 속 수치 나이는 새 인물의 설계 선택이다.

A는 설계 후 기억 레지스트리의 제목·키워드만 조회했다고 기록했다. 이전 롤아웃·프롬프트·리서치 본문은 열지 않았고 다른 arm의 입력도 사용하지 않았다. 이 절차를 완전한 블라인드 비교 실험으로 해석하지 않는다.

각 장면마다 1회 생성했고 추가 생성, 베스트 샷 선택, 이미지 편집은 하지 않았다. 결과를 본 뒤 프롬프트나 평가 기준을 수정하지 않았다. 관찰 불가와 부분 충족은 전체 판정에서 실패로 계산했다.

| 독립 장면 | PASS / FAIL / 관찰 불가 | 원본에서 확인한 것 | 주요 실패 | 전체 |
| --- | --- | --- | --- | --- |
| A: 공공 수영장 분실물 창구에서 서로 다른 방향의 안내를 비교하는 성인 이용자 | 3 / 2 / 2 | 양손 높이 차, 자기 볼 손끝 접촉, 장면 단서 | 눈꺼풀 비대칭과 홍채 방향 반대. 입꼬리 미세 차와 센티미터 간격 관찰 불충분 | FAIL |
| B: 무대 의상 수선사가 자신의 앞치마와 동료 망토 끈을 분리하는 순간 | 4 / 4 / 1 | 자기 앞치마 주름 집기, 고개 회전과 렌즈 시선 | 양손 손바닥·손등 방향 반대, 브로치와 닳은 끈 끝의 관계 불일치, 동료 정수리 크롭 | FAIL |
| C: 폐쇄된 시골 건널목에서 반무릎 자세로 케이블을 시험하는 성인 기술자 | 4 / 2 / 5 | 작은 눈 반사점, 장면·일부 작업 단서 | 브로드 밝기 관계와 루프 그림자 간격 실패. 다리 소유·뒤꿈치 지지·전체 케이블 경로 관찰 불충분 | FAIL |

총 27개 독립 조건은 **11 PASS, 8 FAIL, 8 관찰 불가**다. 일반 신체 구현 감사는 A의 필수 5개 게이트가 통과했으나 A의 독립 미세 형태 조건은 실패했다. B·C는 신체 구현 필수 게이트도 각각 2개 실패했다. 일반 감사의 성공이 더 엄격한 장면 전체 판정을 대신하지 않는다.

### A 원본

![공공 수영장 분실물 창구 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/generated_original.png)

[프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/prompt_en.txt) · [독립 평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/qualification_report.md)

### B 원본

![무대 의상 수선 작업실 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-b/generated_images/backstage-snapped-braid-native-1/original.png)

[프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-b/final_prompt.txt) · [독립 평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-b/REPORT.md)

### C 원본

![시골 건널목 신호함 현장 작업 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/generated_images/rural-signal-native-attempt-1.png)

[프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/final_prompt.txt) · [독립 평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/QUALIFICATION-REPORT.ko.md)

## 데이터 존재·노출·선택·픽셀의 차이

A에서는 새 윗눈꺼풀 형태와 양손 높이 차 후보가 정상 팩에 노출돼 선택됐다. 양손 높이 차는 픽셀에서 통과했고, 윗눈꺼풀 형태는 엄격하게 확인되지 않았다. 볼 접촉은 보였지만 해당 새 접촉 후보는 노출되지 않았으므로 그 후보가 만든 결과라고 기록하지 않았다.

B에서는 보강한 옆눈 시선 후보를 선택했다. 작은 옷 주름 후보는 노출되지 않았다. 노출된 손 옆면 후보는 요청한 손바닥·손등 정면 방향과 달라 거절했다. 머리·눈 방향 후보의 누락된 효과 정보는 당시 구성 감사에서 발견했고, 그 후보를 실제 생성 선택에서 제거했다. 이후 최종 데이터에 효과 정보를 보완했다. B의 이미지는 그 수정 후보를 선택해서 만든 결과가 아니다.

C에서는 새 각막 반사점 후보가 노출·선택됐다. 반무릎·루프·브로드 대상 후보는 해당 정상 팩에 노출되지 않았다. 반사점의 부분 성공이 나머지 관계 실패를 덮지 않는다.

**새 시각 프로필은 세 팩 모두 노출·선택·하드 활성화가 0이었다.** 새 프로필 전체의 실제 이미지 구현은 이번 테스트로 검증되지 않았다. 구현한 형태가 검색 이전의 독립 baseline에도 들어 있었으므로, 반영 전·후의 인과적 개선 역시 주장하지 않는다.

세 이미지는 `qualification-v1` 데이터로 생성했다. 생성에 쓰인 전체 런타임 146개 파일과 해시를 [불변 소스 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/frozen-source-v1/SOURCE-MANIFEST.json)에 보존했다. 최종 데이터는 `final-v3`다. 선택한 4개 후보의 병합된 의미·팩 표면이 유지되고 같은 고정 core·seed의 검색 재실행에서 다시 노출됨을 확인했다. V2→V3 작성 데이터의 차이는 외부 출처 기록 연결뿐이며 후보 사전 해시는 같다. 이미지의 생성 버전을 최종 버전으로 바꿔 기록하지 않았다.

근거: [원본·호출·고정 입력 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/ARTIFACT-VERIFICATION.json), [선택 후보 검색 재실행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/final-v2-retrieval-replay/REPLAY-SUMMARY.json), [최종 의미 호환성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/FINAL-V3-COMPATIBILITY.json), [부모 에이전트 원본 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/PARENT-PIXEL-REVIEW.json).

## 소스와 회귀 검증

대체 표현과 각 구성 요소의 한·영 all-of, 한 요소 누락, 다른 인물의 접촉, 부정·넓은 분위기 용어, 부분 속성 잠금, 입술 접촉과 혀 돌출의 차이를 검사했다. 이전에 발행된 `playful_smirk` 원본 행을 정확히 유지했고 대체 표현은 추가 확장에 남겼다.

기존 이력 검사는 새 확장 의존성을 제외하고, 봉인된 10개 메타데이터 수정만 정확히 역적용하여 예전 상태를 비교한다. 역사적 기대값·입력·검색 질의는 바꾸지 않았다. 선언하지 않은 묶음 멤버 변경은 역적용 도구가 거절하는 회귀 검사도 추가했다. 출처 기록은 파일별로 봉인하여 원래 보류 제안과 리서치 근거를 보존했다.

현재 후보 사전 SHA-256은 `d30f83105f11191865ec451aa1b4c6d7393b8e63b8d0b1a23b1bf79b3c916a9c`다. 생성한 인덱스가 이 사전과 정확히 대응한다. V1~V12 사진 경계 기록은 바이트 그대로 두고 V13을 추가했으며, 고정 core·요청 원문·controls·신체 검토, 장면·구도 계약, 공개 후보 64개, 네거티브와 비공개 필드 경계를 보존했다. 검사 코드가 V13을 인식하도록 두 선언만 확장하고, 현재 universal V2 기록의 검사 코드 SHA 필드 하나를 다시 연결했다. universal의 원래 오라클·장면·불변 조건은 모두 그대로다.

최종 사전·인덱스 검증은 통과했다. 관련 이력·가드·출처 검사 86개와 새 통합 검사 17개가 통과했다. 전체 unittest 발견 1,416개를 162개 모듈로 나눠 독립 프로세스에서 실행했고, **1,416/1,416 PASS, 실패·오류·skip 0**이다. 자세한 실행 결과는 [검증 요약](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/VERIFICATION-SUMMARY.json)에 기록했다.

기존 dirty/untracked 작업을 선택적으로 보존하고 검토한 파일만 반영했다. 과거의 참조되지 않는 인덱스 세대를 삭제하지 않았다. 커밋·푸시·배포는 수행하지 않았다. 사용자 수락 판단은 아직 받지 않았다.

## 후속 반영 계획

1. **선택적 프로필 노출을 먼저 점검한다.** 이번 고정 core를 유지한 채, 정상 검색에서 구성 요소 전체·소유·관계가 충족되는지 분석한다. 넓은 분위기 이름으로 하드 의무를 활성화하거나 원하는 후보를 강제로 끼워 넣지 않는다. 한국어·영어의 독립 표현과 가까운 오인 형태를 포함해 새로운 검색 평가 자료를 고정한다.
2. **좌우 좌표와 손의 면 방향을 분리 검증한다.** 인물 기준 좌우와 화면 좌우의 대응, 손바닥 주름/손등 손마디, 시선 목표를 명시적으로 구별한다. A의 눈꺼풀·홍채, B의 손 면을 먼저 독립 조건으로 재검증한 뒤 원래 복잡한 장면으로 돌아간다. 실패한 원본과 기존 평가 기준은 유지한다.
3. **접촉·지지·소품 연결의 가시성을 확보한다.** 손가락 hook, 브로치–끈 끝, 무릎–정강이–발 소유, 뒤꿈치 접촉, 전체 케이블 경로를 가리는 크롭·의복·투영을 줄이는 촬영 선택을 검토한다. 원래 충족 조건을 낮추지 않는다. 센티미터 조건은 알려진 크기의 기준 물체나 교정 정보가 있어야 판정할 수 있다.
4. **조명 관계는 독립해서 확인한다.** 얼굴 yaw, 넓은 볼, 밝은 볼을 함께 판정하고 루프의 코 그림자/볼 그림자/밝은 간격을 별도로 평가한다. 반사점 하나나 분위기만으로 조명 전체를 통과시키지 않는다.
5. **재검증은 고정된 조건과 모든 시도를 남긴다.** 추가 이미지 생성이 필요한 후속 작업에서는 선택된 후보와 실제 프롬프트의 연결을 유지하고, 원본 픽셀 all-of와 사용자 판단을 따로 기록한다. 성공 사례만 고르는 방식으로 현재 0/3 결과를 대체하지 않는다.
