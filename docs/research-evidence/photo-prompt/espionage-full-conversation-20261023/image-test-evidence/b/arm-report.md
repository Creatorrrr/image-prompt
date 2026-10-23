# Arm B 검증 결과

전체 strict **FAIL (5/6)**. 원본 참조 JPEG를 실제 첨부해 native image_gen을 **정확히 1회** 호출했다. API·대체 모델·재시도는 0회다. 사용자 수용은 pending이다.

| 고정한 픽셀 기준 | 판정 |
|---|---|
| 참조 얼굴·보브·앞머리 외관 안내 | visible PASS |
| 두 인물의 손–같은 여권 양끝 접촉 | visible PASS |
| 머리부터 허벅지 중간까지의 정확한 crop | visible FAIL |
| 두 문설주·상부 문틀과 선택적 전경 가림 | visible PASS |
| 수평 카메라 프레임과 배우 몸/고개 방향의 구분 | visible PASS |
| 저조도 + 머리/코트 어깨의 차가운 림광 | visible PASS |

하단이 의도한 허벅지 중간보다 아래로 내려간다. 부분 충족을 전체 통과로 올리지 않았다. 카메라 높이·실제 광원의 정확한 위치·실제 신원·나이는 픽셀로 확정하지 않았다.

신규 full-conversation CID `cand_fdc4b1d7ed4357a0b64c3f72487de8f8`(관찰자 손과 열린 폴더 POV)이 노출됐으나, 기존 owner 근거와 source 전체 효과/프레임 조건을 충족하지 않아 미채택했다. 신규 source 문장 반영은 0개이며 실제 구현 판정은 **BLOCKED_UNSCORED**다. 기존 자료의 일반적인 전경 어깨 흐림만 `inspiration_only`로 사용했고 native chosen CID는 `[]`다. 신규 자료의 등록·노출·채택·문장·픽셀을 구분했다.

6개 검색에서 40개 query/CID/RID occurrence, 38개 고유 source를 전체 native/조건/effect로 검토했다. light_direction은 source-scope projection 뒤 0개를 반환했다. 이를 수정검색하거나 다른 source를 억지로 채택하지 않았다. 초안·테스트·검색 plan을 유지했다.

동결/feature/compose/runtime/native-plan/ledger/review-record 감사는 PASS다. 공식 embodiment 5개 gate가 PASS인 것과 전체 strict FAIL은 별개다. 최초 staged store의 ancillary 모델 누락은 실제 검색 전에 실패했고, 동일 generation이 설치된 경로에서 최초 검색을 수행했다. 두 구성 감사 필드 오류는 생성 전에 스키마에 맞춰 고쳤다.

독립 pre-core freeze와 plan sealing 후, 상태 확인 도구에서 이전 arm 완료 요약이 우발적으로 노출된 예외가 있다. 현재 다른 full arm의 파일·프롬프트·이미지는 읽지 않았으며 이전 요약은 이번 선택·프롬프트·판정에 사용하지 않았다. 따라서 zero exposure라고 주장하지 않는다. 자세한 기록은 independence-declaration.json에 보존했다.

- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/final-prompt.txt)
- [이미지 복사본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/results/ferry-passport-native.png)
- [고정 기준별 픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/strict-pixel-review.json)
- [공식 embodiment 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/visual-render-review.json)
- [전체 결과와 계층별 상태](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/arm-result.json)
- [독립 실행 manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/run_manifest.json)
- [비교와 source별 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-b/composition-comparison.md)

원본 반환 파일은 `/Users/chasoik/.codex/generated_images/01a16923-8a4a-7780-b80b-3b46ccd5da68/exec-ad44fd89-f426-4269-a25e-82bf2a0bad0a.png`에 남겨 두었다. 원본과 복사본 SHA256은 `1e27e5145fe8d80bd5d71511e8c07fa246adbb23af53ac70f4891fb58116b986`로 같다.
