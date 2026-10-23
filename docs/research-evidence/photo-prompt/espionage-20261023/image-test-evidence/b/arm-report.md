# Arm B 결과

실제 native 생성 1회 성공. 사전 테스트 전체 strict 판정은 **FAIL**이다. 문화 행사·공개 직원 역할·카탈로그 아래 단일 카드와 두 접점·참조 외관·신체 구조는 보이지만, 여성의 제3 방문객 환대와 남성의 카드 특정 시선이 동시에 분명하지 않다. 사용자 수용은 아직 미확인이다.

| 사전 gate | 관찰 | 판정 |
|---|---|---|
| cultural_event | visible | PASS |
| public_cover | visible | PASS |
| screened_transfer | visible | PASS |
| public_hidden_attention | partial | FAIL |
| reference_appearance | visible | PASS |
| embodiment | visible | PASS |

신규 데이터는 4개 독립 쿼리의 32 occurrence/29 source 중 `cand_f7ce8f05d63a57f387d77f4b29d65e9e` 1개가 노출됐다. 이 source는 테이블 건너 사진을 제시하는 전체 가시 배치와 frozen existing-owner/part 근거를 요구한다. 이 core에는 photo/table/owner graph가 없어 미채택했다. 신규 source의 픽셀 구현은 검증되지 않았다. 기존 `cand_9f3e4647e0d05c31a65e015e901243ad`의 warm-subject/cool-environment 의미만 color-only inspiration으로 보존했다. native whole-source qualification이나 선택을 주장하지 않는다.

최종 프롬프트: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/final-prompt.txt
이미지: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/results/museum-liaison.png
이미지 SHA256: 13da6593b02993bd6962b644ae810067e6161fbd9a75b260c6120d8025653af3

Composition/runtime/native recording/review-record audit은 PASS. 5개 embodiment gate는 native 원본 관찰로 모두 PASS. Composition quality 경고는 5개 frozen intent를 authored evidence로 보존했다는 uncovered-intent 알림이다. 기계 audit PASS는 별도 사전 주제 attention gate 실패를 무효화하지 않는다.

참조는 원본 파일을 직접 보고 정확한 path/hash로 실제 attachment했다. 생성 원본은 보존하고 프로젝트 사본과 해시 일치를 확인했다. 1536×1024 원본, 무보간 손/얼굴 crop, 768×512 thumbnail을 점검했다. 실제 native 호출 1회, API/fallback/재생성 0회.

독립 manifest: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/native-manifest.json
Ledger: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/native-image-runs.ndjson
전체 기계 보고: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/arm-result.json
상세 관계 판정: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/theme-pixel-review.json
후보 비교: /Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/composition-comparison.md
