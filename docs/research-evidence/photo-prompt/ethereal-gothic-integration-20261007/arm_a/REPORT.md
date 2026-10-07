# Arm A 독립 자격검증

기본 이미지 1개에서 새 후보의 천 로제트·생화 관계를 실제 원본 픽셀로 확인했습니다. 신체 관계 5개 gate는 모두 관찰 PASS이며 auditor는 `technical_qualified=true`를 반환했습니다. 사용자 판단은 pending입니다. Render audit 종료코드 1은 `visual_technical_qualified_user_judgment_pending` 상태이며 technical/schema 실패는 없습니다.

[원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/native_image_attempt_1.png) · [Standalone prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/final_prompt_en.txt) · [취합 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/QUALIFICATION-RESULT.json)

원본: 1237×1272, SHA256 `2614f27720eed20653b29470f0d7b62273d23d804a01661f43c47139333c4d33`. Built-in `image_gen.imagegen` 실제 1회, attempt 1 성공. Native 반환 파일과 Arm A 보관 파일은 동일 bytes입니다. 다른 arm 입력, core 재작성, pack 변조, 반복 생성, CLI fallback은 없습니다.

## 독립 장면과 고정 입력

OS 난수 seed `4697092674311968183`으로 일반 지식에서 만든 7개 이동·전달·교통 장면 중 index 5의 마지막 회차 정류장 트램을 골랐습니다. 꽃 운반 여행자가 문 옆에서 상자를 안정시키고 가지를 안으로 되돌리는 현재 순간입니다. 성인 설정과 상황·동작·옷·카메라는 agent-owned이며 참조는 사진에서 보이는 얼굴·단발·앞머리 범위입니다.

Baseline 427단어와 9개 관찰 범주는 후보를 읽기 전에 고정했고 selection validator는 경고 없이 PASS했습니다. 최종 474단어는 같은 raw request/core/controls와 source fingerprint `2476149f066c2867e9dd10ba7444ecd4f41cffdf3d00023909bd30a3828bc4f4`에서 작성했습니다. Normal retrieval mode는 `core_bm25f`입니다.

## 새 데이터의 실제 경로

| 단계 | 실제 증거 |
|---|---|
| 노출 | 새 `egr_closed_eyes_composed_repose`, `egr_fabric_rosette_vs_living_flower` 두 entry |
| 선택 | `augmentation:adult_appeal:sensual:garment_detail:egr_fabric_rosette_vs_living_flower` |
| 미선택 | 완전히 눈을 감는 후보는 stem을 보고 안정시키는 현재 행동의 가독성 때문에 미선택 |
| 새 profile / bundle | 이 pack에 새 narrow profile·새 bundle 노출 없음, opt-in 없음 |
| 감사 | Composition 및 reference/runtime audit PASS. Composition의 4개 경고는 후보로 미리 덮이지 않은 frozen anchor를 최종 자유 서술로 보존했다는 기록 |
| Native | 채택한 새 후보의 모든 material/owner component 관찰 PASS |

기존 baseline의 `A small dark floral clasp at the collar echoes the cargo's living blossoms.`를 아래로 바꿨습니다.

> At her collar, a charcoal silk rosette is built from folded cloth petals with visibly doubled hem edges; in the case beside her hand, separate ivory blossoms have soft botanical petals connected to their own brown stems. A quiet pewter glint catches the rosette's dense folds, while warm ivory light reveals the thin living petals on the twig she steadies.

## 원본 구성 요소 관찰

| 구성 요소 | 결과 | 원본 관찰 |
|---|---|---|
| 천 로제트 | PASS | 목깃의 검은 장식이 여러 겹 접힌 천 꽃잎으로 구성됨 |
| 천 가장자리 | PASS | 바깥·안쪽 꽃잎에 접힌 rim과 중첩 경계가 읽힘 |
| 생화 꽃잎 | PASS | 흰 꽃잎·노란 수술·잎과 꽃봉오리가 식물 구조로 읽힘 |
| 자기 줄기 연결 | PASS | 손이 잡은 갈색 가지와 꽃의 pedicel·분지 연결이 보임 |
| 별개 소유·재료 관계 | PASS | 목깃의 천 장식과 상자 위 손에 들린 생화가 같은 프레임 안에서 분리됨 |

[Native component 관찰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/new_data_native_review.json)와 [정확한 strict gate 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/native_render_review.json)를 별도로 남겼습니다. Strict gate 집합은 body ownership, joint chain/reach, support/balance, contact/space, visibility/projection 5개이며 실제 source helper에서 도출했습니다.

## 판단의 범위

고요한 표정·검은 식물 무늬 레이스·생화·일반적인 목깃 꽃 장식·금빛과 아이보리 빛·트램 상황은 baseline에도 있었습니다. 그런 요소의 이미지 출현이 새 DATA의 인과효과를 증명하지는 않습니다. 채택한 material 관계는 명시적인 prompt delta와 이 이미지의 native 관찰 증거가 있지만 baseline render/ablation이 없어 이미지 개선의 인과효과와 사용자 취향은 미확인입니다.

하단 손은 상자 전체 밑바닥을 평평하게 받치는 모습보다 손잡이/가까운 아랫모서리를 지지하는 grip으로 읽힙니다. 상자의 왼쪽 끝과 발은 잘렸으나 핵심 접촉과 brass 지지는 평가 가능합니다. 참조 외형의 연속성은 관찰했으며 신원 확인이나 실제 나이·성격·몸 추정은 하지 않았습니다.

[Ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/image_runs.ndjson) · [독립 manifest v2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/run_manifest.json) · [Prompt literal delta](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/data_prompt_delta.json) · [Source pin](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/source_pin.json)
