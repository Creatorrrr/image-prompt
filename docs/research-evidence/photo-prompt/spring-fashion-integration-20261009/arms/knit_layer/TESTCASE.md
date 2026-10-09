# 강변 인쇄 공방의 첫 도판과 봄바람 — A / knit_layer

실제 built-in `image_gen` 1회로 참조 사진을 첨부해 생성했다. 결과는 1024×1536 PNG다. 원본과 프로젝트 복사본 SHA256은 `795800ed38b1c4206fc0a59d94cf3dbd5ba3f32bbd959231eabc72687a8642b6`로 동일하다.

- 이미지: [knit-layer.png](/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt/generated_images/riverside-print-spring-knit-7390e5e48c564d6885d7c25676f4cffd/knit-layer.png)
- 프롬프트: [prompt_en.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/prompt_en.txt)
- 상세 결과: [stage2-result.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/stage2-result.json)
- 독립 ledger: [image_runs.ndjson](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/image_runs.ndjson) / [run_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/run_manifest.json)

동결된 core·원문·locks·baseline은 그대로 유지했다. 난수 seed `198294653418842`로 pre-core에 독립적으로 선택한 인쇄 공방 순간이며, retrieve seed는 `83671`이다. 다른 arm의 폴더·프롬프트·pack·이미지를 읽지 않았다.

검증 runtime generation은 `a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c`, source fingerprint는 `6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a`다. 실제 receipt와 모든 managed native 단계에서 같은 세대를 사용했다. 원문 envelope SHA256은 `81731e13b667c5f32f60476d3a826f47bfa7a8c45651eb0c69fcd33e3f25a1ac`, core는 `97ece69a1d3d842933a440b9a99891dd640e1cf943a85509f06b72787c61f3b3`, intent lock은 `b60a431e8837cd6fb5d8d42c5d3ac3c03821c965cd7831217aff2cac439b82a0`다.

실제 노출된 신규 `visual-concept:spring_sf057_02`와 `bundle:spf_sf104_2_bundle`을 authorial/optional로 선택했다. 전자는 니트의 연속 실 경계·진짜 열린 셀을 hard opt-in한다. 후자는 `spf_sf104_2`의 같은 착용자에게 속한 블라우스/스커트의 인접한 저채도 따뜻한 색과 분리된 의복 경계를 적용한다. `spring_sf104_2` associated profile은 자동 hard 활성화하지 않았다. 기존 `visual-concept:sheer_garment_optical_layering`은 실제 투과 레이어에 명시 opt-in했다.

composed/runtime 감사와 native plan은 PASS다. 네이티브 실행 operation은 `7390e5e48c564d6885d7c25676f4cffd`, ledger run ID는 `9b2b99f4e392fcc7`다. managed 내부 ledger와 독립 ledger는 동일한 실제 1회를 각 provenance 형태로 기록하며 합산하지 않는다. 도구가 이미지 모델명을 반환하지 않아 observed model은 unknown이다.

`review-shape`에서 정확히 유도된 11개 hard gates를 같은 저장 PNG의 전체 프레임, 1:1 native crops, 320×480 thumbnail로 검토했다. 기록 감사 PASS, technical qualification PASS, direct pixel observation 11/11 PASS다. 감사기는 픽셀을 추론하지 않으며 관찰 근거는 agent가 직접 작성했다.

| 정확한 runtime hard gate | 관찰 | 요구 scale |
| --- | --- | --- |
| vo_spring_sf057_02_visible_variant | PASS | native |
| vo_sheer_textile_first_read | PASS | thumbnail |
| vo_sheer_weave_edge_legibility | PASS | native |
| vo_sheer_transmission_relationship | PASS | native, thumbnail |
| vo_sheer_layer_coherence | PASS | native |
| vo_sheer_not_optical_or_generation_substitute | PASS | native, thumbnail |
| embodiment_body_ownership | PASS | native |
| embodiment_joint_chain_and_reach | PASS | native |
| embodiment_support_and_balance | PASS | native |
| embodiment_contact_and_space | PASS | native |
| embodiment_visibility_and_projection | PASS | native |

별도 신규 후보의 사전 all-of 관찰표는 **4/5 PASS, 전체 FAIL**이다. 니트 두 효과와 같은 wearer·따뜻한 색 관계는 관찰됐다. 그러나 미리 정한 `warm_bundle_boundaries`의 두 번째 끝점인 **스커트 waistband가 블라우스에 가려져** 완전한 관찰을 할 수 없다. 다른 skirt outline으로 사후 대체하지 않았다. 전체 topic review에서도 같은 이유로 O06을 FAIL로 보존했다. 이 supplemental 실패를 runtime hard gate에 추가하거나 hard PASS로 바꾸지 않았다.

- 정확한 관찰: [native-pixel-gate-review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/native-pixel-gate-review.json)
- 신규 후보 all-of: [supplemental-new-candidate-review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/supplemental-new-candidate-review.json)
- 전체 인상·topic: [supplemental-topic-review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/supplemental-topic-review.json)

밝고 공기가 도는 공방, 실제 클립 행동, 니트/투과/안쪽 상의의 재료 위계가 함께 읽힌다. 얼굴·짧은 검은 bob·가느다란 fringe는 첨부 사진의 보이는 외형을 안내로 사용했다. 실제 정체성·성격·생애·치수·정확한 섬유/공정·숨은 미착용은 추론하지 않았다. 생성된 full-body crop은 authorial mid-calf 제안보다 넓다. 추가 신발·작업실 문구는 보충 요소로 남는다.

사용자 judgment는 **not_yet_received / pending**이다. 별도 root 재검토와 실제 사용자 선호를 agent 기술 관찰로 대신하지 않는다.
