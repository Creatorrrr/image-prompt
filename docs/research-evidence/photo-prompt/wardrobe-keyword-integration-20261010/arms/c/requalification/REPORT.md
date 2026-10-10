C 사례는 첨부 사진의 얼굴·헤어를 사용한 항구 모자 리본 수선 장면입니다. 내장 image_gen 최초 1장 생성·저장·원장 기록·원본 픽셀 평가를 완료했습니다. 구조적 감사와 리뷰 기록은 유효하지만 완전한 native 기술 합격은 **FAIL**, 사용자 평가는 대기입니다.

[최초 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/generated_images/harbor_hat_repair_c_first.png) · [최종 675단어 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/prompt_en.txt) · [실제 native 전달 인수](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/native_tool_payload.json) · [원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/image_runs.ndjson) · [run manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/run_manifest.json)

| 증거 층 | 결과 |
|---|---|
| 구성 감사 | PASS, requester anchor의 자유 서술 보존 관련 quality warning 4개 |
| Native 전달 감사 | PASS, 실제 참조 첨부 1개 |
| 이미지 호출/복사 | native 1회, 1024×1536, 원본과 byte 동일 |
| 픽셀 리뷰 기록 감사 | PASS: record_valid=true, schema 오류 없음 |
| 필수 native 조건 | 9개 중 6 PASS / 3 FAIL, technical_qualification=fail |
| 전체 인상 | 일관된 항구 수선, 의상·색·장소가 자연스럽게 연결됨 |
| 사용자 수락 | pending / not_yet_received |

신규 노출은 ordinary 2 / bundle 2 / visual 2 / clarification 2입니다. WK095 ordinary를 같은 치마와 벤치 좌면의 압축 접힘으로 채택해 픽셀 PASS를 확인했습니다. WK047 visual opt-in은 같은 재킷 커프의 직조와 박음질 인접 관계로 채택했지만, 가는 실의 얽힘이 해결되지 않아 FAIL입니다. WK111은 문 가림과 의복 리본 접합이 새로 필요하고, WK104는 별도 위팔 소매/몸판 틈이 없으므로 거절했습니다. 중복 bundle은 동일 관계를 다시 채택하지 않았습니다.

| 필수 조건 | 판정 |
|---|---|
| vo_wkr_wk047_selected_relation_1 | FAIL (native) |
| vo_vg_face_hands_place_readability_1 | PASS (native, thumbnail) |
| vo_vg_face_hands_place_readability_2 | PASS (native, thumbnail) |
| vo_vg_face_hands_place_readability_3 | PASS (native, thumbnail) |
| embodiment_body_ownership | PASS (native) |
| embodiment_joint_chain_and_reach | PASS (native) |
| embodiment_support_and_balance | PASS (native) |
| embodiment_contact_and_space | FAIL (native) |
| embodiment_visibility_and_projection | FAIL (native) |

커프 미세 얽힘, 오른손-바늘-새 스티치의 완전한 접합과 가시성 때문에 3개 필수 조건이 실패했습니다. 손과 접촉점의 광학 가독성은 통과하며, 바늘 소유의 실패와 구분했습니다. 별도 관계 검토에서도 주름의 위쪽 끝–밑단 연속성, 모자 밴드–리본 끝의 같은 앵커 및 공유 바람 방향, 가방의 opposite-shoulder 사선 경로와 여러 접합 끝점은 부분 실패로 보존했습니다. 전체 인상을 이유로 미세 관계를 합격시키지 않았습니다.

[정확한 hard-gate 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/visual_review.json) · [소유자/끝점/수량/지역 물성 관찰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/supplemental_pixel_review.json) · [전체 인상/controls 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/whole_image_review.json) · [1:1 crop/thumbnail 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/pixel_inspection/inspection_manifest.json) · [파일·호출 일치 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/c/requalification/final_evidence_check.json)

현재 generation=c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14, fingerprint=c934e9f60126fe1f111ede9e80bf045907624404589b8d28fb45ebd669b73444, pack=666c74bd17c7291b. 최초 진단 pack 550a5b8eee6fe659는 보존했고 재사용하지 않았습니다. 각 run은 정확히 1회 조회(arm 총 2회), 이미지 arm 총 1회, repair/API fallback 0회입니다.

진단 retrieval_seed=1872214162960451119, 재검증=7180700068034827031. neutral 8역할/core/baseline/controls는 byte 동일하지만 검색 seed가 달라 **matched before/after 인과 실험은 아닙니다**. 현 세대의 실제 노출·선택·첫 픽셀 사용을 검증했습니다.

이미지 SHA256: `dfe64895937e3ec1e14d1b4810c9a9395a6d84e6097a043b45c0dc13daecf50e`. Prompt SHA256: `bfc5d2313efb93398bd882f267dd7d200c01ec31a8244739a3b2b17afae95723`. Core SHA256: `d368b0d5ced6bc5d0cdeb23f482044766d2f697b133be1a22ec33d007a443cb8`. Controls SHA256: `22790c772c6c714a29e2f1bf12a4e05cf853bb8a0772fb469d731fce507268e2`. Effective visual SHA256: `ea8d6874db93bbb7c7d3b0137600a8fb3c9394ca9f030a3aae6e297557ae98dd`.

독립 일반 지식의 4개 후보 장면에서 저장한 seed 10774828166673935651의 균등 추출(index 0)로 사례를 골랐습니다. 다른 arm 입력은 사용하지 않았습니다. sensual 1 / fetish 0 / surreal 0 / creativity 1을 처음부터 유지했습니다. 사진은 눈에 보이는 얼굴·헤어만 안내하며 신원·실제 연령·성격·몸매·이력은 추론하지 않았습니다.

최초 진단 감사 실패와 재구성 메타데이터 인용 개수 실패, native payload 보존 도우미의 status 이름 가정 오류를 모두 보존했습니다. 전자는 중복 인용만 제거했으며 positive prompt는 바꾸지 않았습니다. 실제 image_gen 오류나 차단은 없었습니다. 내장 recorder의 원장 ts는 operation 예약 시각이며 실제 호출 시작/종료는 image_result_metadata.json에 별도로 보존했습니다. 이미지 재시도 및 별도 수리 렌더는 하지 않았습니다.

최종 positive prompt:

```text
Create a coherent complex photographic scene, one connected moment of everyday activity. The central subject is a woman whose visible face and hair follow the supplied reference image. Use the reference for facial contours, dark eyes, natural pink lips and the dark chin-length bob with wispy fringe. Her clothing, fictional travel circumstances and bodily staging belong to this new scene. On a stone ferry quay after a passing shower, she sits on a weathered wooden bench and repairs the mustard-colored ribbon around a woven straw hat. The hat rests across her thighs with its crown tilted toward the camera. A short section of the ribbon has lifted from the crown; several older stitches and the still-loose tail make the small failure readable. Her left thumb and index finger press the folded ribbon against the straw crown. Her right hand holds a single slender needle between thumb and index finger, a few centimeters above the band, drawing one length of ochre thread through the ribbon and straw. The thread visibly connects that needle to the new stitch. Both forearms belong visibly to her relaxed shoulders, with elbows bent forward over her lap; her hands occupy separate spaces on either side of the stitch. Her feet rest on the quay stones, knees support the hat, and the bench supports her seated weight. She wears an open moss-green cotton twill chore jacket over an ivory rib-knit scoop-neck top, with a rust-colored pleated midi skirt falling over her knees. Beside her left thigh, the rust skirt gathers into short compressed folds where that same skirt meets the bench seat; a thin contact shadow follows the cloth-to-wood junction. Across the front of that rust skirt, long raised pleat ridges alternate with darker recessed valleys from the upper skirt down toward its lower hem, opening slightly over the bent knees. Rolled jacket cuffs expose a slightly lighter inner twill at her wrists; the outer sleeves retain small diagonal folds near the bent elbows. On the moss jacket's turned cuff, a small stitched hem borders a locally readable weave. Fine interlaced yarns remain visible across the same textile surface beside its stitched edge. A walnut-brown leather crossbody bag hangs at her near hip, its narrow strap crossing from the opposite shoulder and joining the bag through small brass rings. A soft canvas sewing pouch lies open beside her on the bench, with a small thread spool inside. Tan leather ankle boots make quiet contact with the damp grey paving. A few short loose strands curve out from her own bob, remaining visibly rooted at the same temple. The mustard ribbon tail rises from its attached hat-band anchor, with the pinned section staying against the crown. In the sea breeze, those rooted strands bend in fine small arcs while the wider attached ribbon makes a softer curl toward the same open harbor side. She looks down at the stitch with patient concentration, lips softly parted, shoulders at ease; the attraction is the close, unperformed presence of a person absorbed in a practical task. Beyond her, a ferry boarding ramp and a low mooring bollard situate the waiting place, with muted blue water farther away. A small puddle beside the bench catches the pale sky. Make an observed travel lifestyle photograph in a portrait two-by-three frame, from a front three-quarter viewpoint at conversational distance. Frame her head, connected shoulders and arms, the sewing contact and boots together, leaving a narrow stretch of quay and harbor to one side. Late-afternoon side light warms her face and straw hat while the water remains cool. The face and repairing hands form the first focal group, the loose ribbon is the second read, and the ferry setting stays subordinate. Use natural skin texture and enough depth of field for the needle-to-stitch connection and fabric surfaces to remain readable. Her face retains readable features at the selected portrait scale. The needle-holding hand and pinned ribbon fold remain legible together in the same focal zone. The ferry boarding ramp establishes the harbor setting through its recognizable outline beyond the bench.
```

최종 negative prompt:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

실제 전송은 positive 문장 뒤에 정확히 두 줄바꿈과 `Avoid: ` 및 위 negative 문장을 붙였습니다. 첫 이미지 생성 뒤 prompt를 수정하지 않았습니다.
