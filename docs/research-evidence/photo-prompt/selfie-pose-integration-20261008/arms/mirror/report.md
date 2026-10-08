거울 arm의 최초 native 이미지에서 공식 신체 gate 5개가 모두 PASS했습니다. 새 `sf_capture_physical_mirror` 후보가 명료화한 촬영자–휴대폰 그립–동일 반사 공간도 보입니다. 정확한 화면 응시는 UNOBSERVABLE이고, 작은 미소를 피곤함·안도로 읽는 감정 해석은 PARTIAL입니다. 사용자 수용 판단은 아직 받지 않았습니다.

[원본 이미지](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/generated_images/mirror-lantern-native-01.png) · [최종 프롬프트](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/final_prompt_en.txt) · [정확한 runtime 바이트](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/exact_runtime_prompt_en.txt) · [구조화 판정](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/qualification.json)

독립 seed `3220220004012724707`로 일반지식에서 만든 4개의 연결된 장면 중 종이등 수선이 선택됐습니다. 해안 수선 작업장의 첫 완성품, 파란 실로 잇댄 종이, 구겨진 손상 재료, 폰을 잡는 손과 대나무 손잡이를 받치는 손, 작은 미소를 한 순간으로 설계했습니다. 첨부의 보이는 얼굴·짧은 단발·앞머리만 참조했으며, 이 사람의 실제 이력은 장면의 근거가 아닙니다. 물리 거울과 촬영 높이·방향은 agent 선택이며 사용자 camera lock으로 만들지 않았습니다.

Phase 1의 8개 neutral feature 선택과 core를 후보 접근 전에 동결했습니다. V2에서도 원문/envelope/control/core/선택/embodiment/baseline/catalog의 파일 해시가 모두 처음과 같았습니다. core는 `efb1073ca77023cc2c801dd0edf024d755baa5c20fa6cc2a3e45a31665b5377d`입니다. [재사용 증거](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/v2_core_reuse_verification.json)가 이를 보존합니다.

최종 source generation은 `8d793f025f759eb7f782d0a194f9dd7f0781370aaff2bbea331146e940c3ab2f`, fingerprint는 `fe7ac255143e52fe70b9c64cc7bd02961d176b0258f35a1769aeff6b562a825c`, pack은 `3fcfe9e5ecaaa985`입니다. 새 `capture_mode`의 `slot:capture_mode:sf_capture_physical_mirror`가 실제 노출됐고 전체 관계를 읽어 채택했습니다. 추가 literal은 다음과 같습니다.

> The one reflected photographer operates the same phone gripped along its side edges by her right hand; that phone and her own reflected torso share the continuous workshop reflection around the hanging lantern.

수선 이야기·거울 선택·양손 역할·종이 재료와 표정은 독립 baseline의 기여입니다. 새 후보의 기여는 폰을 소유한 촬영자와 한 반사 공간의 명시적 연결이며, 그 연결이 실제 픽셀에서도 지원됩니다. 생성 비교 baseline은 없어 인과적 개선량은 측정되지 않았습니다. `sf_091`, `sf_092`, `sf_178`의 얼굴 가림/손거울 profile은 노출됐지만 현재 수선과 표정을 덜 읽히게 해 채택하지 않았습니다. `chosen_visual_concept_ids=[]`에 따라 이들의 opt-in gate는 생성되지 않았습니다. [기여 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/new_data_contribution.json)에 source ID, 노출, 선택, literal, 픽셀을 분리했습니다.

첫 V1의 `sf_097` 렌즈 응시 수정과 감사 결과는 [preflight 보존](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/v1-preflight/preservation_manifest.json)에 남아 있으며 실제 호출은 0회입니다. V2는 동결 baseline의 화면 확인 방향을 유지했고 V1의 lens-directed 문장을 사용하지 않았습니다. V2의 실제 built-in `image_gen` 호출은 1회, API 호출·추가 수정 생성은 0회입니다.

원본은 1237×1272 PNG이며 tool이 반환한 실제 로컬 파일을 편집 없이 복사했습니다. 이미지 SHA-256은 `f73a839b60a97f7d30ec1396b3f8645baaaa719e5ec1e837a67ec0b809648da2`입니다. 원본 전체를 `view_image(detail=original)`로 직접 열었습니다. 아래 좌표는 원본의 좌상단 기준 수동 추정 영역입니다. 공식 gate는 정확한 pack/composed에서 도출된 5개만 사용했습니다.

| 공식 gate | 판정 | 원본 영역 (x1–x2, y1–y2) | 픽셀 근거·한계 |
| --- | --- | --- | --- |
| embodiment_body_ownership | PASS | 휴대폰 손 (278–465, 259–596), 종이등 손·손잡이 (692–881, 588–811) | 두 손이 같은 몸의 서로 다른 팔·소매로 이어진다. |
| embodiment_joint_chain_and_reach | PASS | 폰 팔·그립 (182–464, 322–870), 등 팔·그립 (726–868, 588–760) | 각 팔이 한 작업에 배정되고 관절·도달 관계가 자연스럽다. 일부 팔꿈치 표면은 옷에 가려진다. |
| embodiment_support_and_balance | PASS | 몸통 (130–793, 402–1271), 손잡이·등 (566–1002, 632–1202) | 직립 몸통과 가벼운 매달린 등 하중이 일관된다. 발은 허용된 3/4 크롭 밖이며 특정 발 자세를 검증했다고 주장하지 않는다. |
| embodiment_contact_and_space | PASS | 폰 그립 (279–465, 323–586), 대나무 그립 (718–875, 604–706) | 손·폰 경계와 손·대나무 접촉이 구별되고 등은 몸 옆/앞으로 자연스럽게 매달린다. |
| embodiment_visibility_and_projection | PASS | 얼굴 (424–700, 106–457), 프레임 좌·우·아래와 등 전체 | 폰·두 그립·등·얼굴·작업대가 같은 물리 반사 공간에서 읽힌다. 정확한 응시 대상은 별도 관찰이다. |

공식 외 관찰에서는 물리 거울 촬영자/폰 소유, 같은 반사 공간, 참조 얼굴·헤어의 외형 사용, 파란 실과 종이/대나무 수선 관계가 PASS입니다. 원본 (752–818, 785–1189)의 파란 seam, (845–1171, 469–1011)의 구겨진 재료·작업대, (918–992, 657–718)의 실타래가 수선 상황을 연결합니다. 작은 미소는 보이지만 정확한 피곤함·안도는 PARTIAL입니다. 폰 화면이 반사에 보이지 않아 실제 화면을 응시하는지는 UNOBSERVABLE이며, 어떤 렌즈가 활성화됐거나 셔터가 눌렸는지도 UNOBSERVABLE입니다. 이 보조 관찰을 공식 gate PASS로 대체하지 않았습니다.

전체 인상은 차분한 작업장 셀프포트레이트이며 얼굴과 밝은 수선 등으로 시선이 모입니다. 인물이 실제 작업물과 관계를 맺어 소품 나열보다 장면이 읽힙니다. 새로 생긴 어두운 앞치마는 열린 appearance 선택과 양립합니다. 종이의 실제 수분 함량, 최초 성공·축제 이력, 정확한 내부 감정은 이미지로 입증되지 않습니다. [artist notes](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/artist_notes.json)에 이 강점과 한계를 별도로 기록했습니다.

최종 composed audit와 image-render-request audit가 PASS했고, [moe review](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/moe_render_review.json)의 exact gate set 감사도 PASS했습니다. generic `photo-image-render-review/v1`은 효과적인 `render_repair` 계약이 없어 적용 대상이 아닙니다. [review audit](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/review_audit.json)는 `technical_qualification=pass`, `user_judgment.source=not_yet_received`를 보존합니다. 공식 결함이 관찰되지 않아 추가 생성하지 않았고, 감정/응시 불확실성은 원래 판정대로 남겼습니다. [ledger](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/image_runs.ndjson)와 [독립 manifest](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/mirror/run_manifest.json)가 실제 호출, 참조 해시, prompt/runtime/image 해시와 source를 연결합니다. native image-model 이름은 도구가 공개하지 않아 unknown입니다.
