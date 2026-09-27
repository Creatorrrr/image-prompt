# high_angle 독립 arm 결과

하이 앵글 키워드 픽셀 기준은 **5/5 통과**입니다. 전체 고정 복합 장면은 **5/6**, embodiment는 **4/5**로 **실패**입니다. 왼손의 지지 방식과 위치가 `far-corner palm support`에서 가까운 종이 가장자리의 손끝 접촉으로 바뀌었습니다. 종이의 들린 부분이 붓 옆에서 펴지는 결과도 충분히 식별되지 않습니다. `partial_is_fail`을 적용했으며 최초 이미지를 그대로 보존했습니다. 사용자 미적 판정은 pending입니다.

## 실행 및 의미 출처

- 독립 seed: `7350812925794127079`; `secrets.randbits(64)` → Python MT19937. 설정/행동/소품/빛 옵션과 draw를 `random_staging.json`에 저장했습니다.
- 장면: 종이 보존 공간의 낮은 작업대에서 성인 창작 캐릭터가 붓으로 종이를 펴는 순간. 금속 자·얕은 안료 접시와 창빛을 함께 배치했습니다. 이는 agent staging이며 사용자 정의·배제·semantic assertion으로 위장하지 않았습니다.
- 사용자 정의 없음. 하이 앵글 의미는 일반 지식에 기반한 해석으로 `interpretation_provenance`에 구분했습니다. 카메라의 높은 위치와 하향 사선 투영을 required typed assertion으로 생성 전에 고정했습니다.
- 전체 raw requester text는 `request_envelope.json.request_text`와 byte-equal이며 active spans만 topic/reference/workflow 해석에 사용했습니다. 위임 브리프를 사용자 텍스트로 사용하지 않았습니다.
- 참조 사진을 original로 직접 확인하고 동일한 실제 파일을 native `referenced_image_paths`에 첨부했습니다. SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`. 얼굴과 머리의 보이는 외형만 사용했습니다.
- 중립 category 9개를 먼저 선택했습니다. pre-core validator valid=true, warnings=[]. core/embodiment/testcase/focal 기준은 후보 전에 고정했고 최종 SHA 검증에서 변경되지 않았습니다.

## 후보 및 감사

- 일반 candidate pack v6 + semantic selection 정확히 1개. Pack `14641278dd8e497c`, run `345aa373062f1a5c`, composed prompt `3df013dbf2b360da`, native runtime prompt `1eabb0ab70ea3c65`.
- Compact composer view를 먼저 읽은 후 선택 4개에 대해서만 full details를 읽었습니다. 다음 후보를 선택했습니다.

| 후보 | 선택 이유 | 픽셀 근거 |
| --- | --- | --- |
| `slot:lighting:soft_window` | A single diffuse window source unifies the actor with the work surfaces. | Window daylight illuminates linen, paper and table in one consistent direction; broad soft shadows survive. |
| `slot:shot_scale:full_length_body_shot` | Body coverage is necessary to read upper-near and lower-receding perspective. | Entire seated support and both shoes remain visible, with floor margin. |
| `integration:physical_contact` | Fine bristle contact establishes the action at the paper surface. | Brush bristles visibly meet the paper. The simultaneous left-palm far-corner support fails. |
| `integration:material_trace` | Local paper fibers and edge irregularity reveal the material being flattened. | Uneven deckled edges and fiber flecks are visible. A locally lifted edge flattening beside the brush is not assessable. |

- 창빛과 전체 신체 프레이밍에 각각 authored decision을 추가했습니다. 모든 locked anchor 및 카메라 assertion evidence 4개는 원문 유지했습니다. 선택 안 한 opt-in visual concept는 `[]`이며 render gate를 만들지 않았습니다.
- 체형·성격·음료 지지·다른 인물/동작/카메라 시점 후보는 거절했습니다. creative 후보 6개도 모두 거절했습니다. 도메인 routing에 pigment `dish`가 food로 읽힌 오염이 있지만 원본 종이 작업 장면은 유지했습니다.
- Composition audit status=pass, runtime exact-request audit status=pass. warning 5개는 후보가 커버하지 못한 frozen intent를 자유 서술/anchor로 보존했다는 정보입니다. 픽셀 통과를 뜻하지 않습니다.

## 원본 및 축소 픽셀 판정

| 하이 앵글 component | 원본 | 420 px | 근거 |
| --- | --- | --- | --- |
| `elevated_downward_projection` | pass | pass | The large visible tabletop, the crown of the bob, the upper shoulder surfaces and the floor behind/beside the seated actor jointly read as an elevated camera aimed downward. The viewpoint is clearly above her face even though she lifts her eyes to it. |
| `multiple_top_planes` | pass | pass | Hair crown is visible at the upper center, shoulder/shirt tops occupy the middle, paper and wooden tabletop spread across the lower-left, and floor texture is exposed at right and beneath the stool. |
| `body_depth_recession` | pass | pass | The head and upper torso dominate the upper-middle frame, while knees and the two shoes taper into the lower-right floor space. This qualitative recession agrees with the downward view; it is not a measured camera height. |
| `oblique_not_orthographic_overhead` | pass | pass | Her face, chest-facing shirt plane, near/front table edge and stool side are all visible, so the camera retains an oblique side component instead of producing a flat overhead plan. |
| `orientation_not_dutch_substitute` | pass | pass | The upright wall joint and drying-rack posts provide stable vertical references. Table and window sill diagonals arise from perspective; frame roll is not carrying the high-angle effect. |

머리 윗면·어깨 윗면·넓은 상판·바닥이 함께 보이고, 얼굴과 상판 앞면은 남아 있어 사선 하향 시점으로 판정했습니다. 상체가 가까워 크게 보이고 발은 바닥 방향으로 멀어집니다. 이 투영은 높은 위치의 카메라 해석을 지지하지만 실제 카메라 높이·정확한 pitch·초점거리 수치를 증명하지 않습니다.

| 전체 scene component | 판정 | 근거 |
| --- | --- | --- |
| `reference_face_hair` | pass | The generated actor has a short dark bob with fine bangs, dark visible eyes, and a softly rounded facial outline broadly corresponding to the supplied appearance reference. This is qualitative appearance correspondence, not identity verification. |
| `paper_studio` | pass | A large fibrous sheet lies on a used wooden worktable; a multi-level paper drying rack and the window sill are visible in the same studio. |
| `brush_press_and_stabilize` | fail | The right hand grips a broad brush with bristles touching the paper. The left hand instead uses fingertips along the near/right paper edge; its palm is raised and does not press the far corner as frozen. The sheet is broadly flat, but a lifted edge flattening immediately beside the bristles is not legible. These missing simultaneous components make the complete action fail. |
| `seated_support` | pass | The hips sit on the square wooden stool visible at right, the trouser legs descend coherently beneath the apron, and both shoes meet the floor. The torso leans toward a reachable table surface. |
| `props_and_light` | pass | A metal ruler and shallow blue pigment dish occupy the left table area, away from the brush-paper contact. Window daylight and soft material shadows reveal paper fibers and linen folds; compass direction is not verifiable from the image. |
| `whole_frame_visibility` | pass | Both hands, brush contact, paper sheet, stool and both shoes are included in the same saved frame. The exact wrong left-hand contact is visible rather than concealed. |

| 실효 hard gate | 판정 |
| --- | --- |
| `embodiment_body_ownership` | pass |
| `embodiment_joint_chain_and_reach` | pass |
| `embodiment_support_and_balance` | pass |
| `embodiment_contact_and_space` | fail |
| `embodiment_visibility_and_projection` | pass |

Pixel review audit에는 schema failure가 없습니다. `embodiment_contact_and_space`가 실패해 qualification_status=`failed_technical_hard_gates`, technical_qualified=false, representative_eligible=false입니다. generic render_repair 계약은 이 초기 arm에 없으므로 그 감사는 적용 대상이 아닙니다. 사용자의 미적 수락은 별도 pending이며 agent가 대신 판정하지 않았습니다.

## 보존 및 경계

- 도구: native `image_gen.imagegen`, 실제 호출 1회. CLI/API fallback·추가 호출·수정·재생성 0회.
- 반환 원본: `/Users/chasoik/.codex/generated_images/01a0e22b-a5a2-7051-9d67-f47ab199a3b6/exec-a166287f-7916-47d0-8874-7b094d980548.png`. 이 구체 경로에서 작업 폴더로 복사했고 동일 SHA를 확인했습니다.
- 저장 결과: [high_angle/generated.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/generated.png), 1237×1272 PNG, 2472942 bytes, SHA-256 `1a8f9cf36313cda20de09cbb68ab4d440d52610996f43ee4353ed679e9c28e59`.
- source `89384cd990223b4e4e44404253f554f23d8cbd3c`의 clean skill tree를 tar snapshot으로 보존했습니다. Skill SHA `f11cf68b6394d374eadb1b1349d4355521625c7d0dbd025cafd6f0b1ba94dc30`. Core 원본 파일 SHA `933f4ce97b7a3a8cca95eac372201f065556b0240abccc8db5a142e4f5cbd5d9`, normalizer canonical SHA `64baa92fdad94d12649896577401460a2a193e4852ec4ac61082434cdd394c99`는 서로 다른 해시 표면입니다.
- Ledger 1행과 manifest v2를 자기 arm 폴더에 저장했습니다. ledger/manifest status=success는 이미지 도구의 반환·저장을 의미하며, 전체 장면 또는 픽셀 gate 성공을 뜻하지 않습니다.
- 다른 arm/과거 실험/기존 후보를 초기 의미 입력으로 사용하지 않았습니다. 주 데이터·인덱스·코드·fixture 및 공유 ledger는 변경하지 않았습니다.

요청 원문: [request_original.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/request_original.txt). 최종 영문: [final_prompt_en.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/final_prompt_en.txt). 실제 native 요청: [image_render_request.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/image_render_request.json). 상세 경로는 [arm_summary.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/arm_summary.json)에 있습니다.
