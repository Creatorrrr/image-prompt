# B 독립 이미지 테스트 결과

컨셉: 마지막 클램프 — 우주로 열린 냉동 보관실과 유인 복도를 가르는 임시 투명 압력막.

Native imagegen 호출은 정확히 1회이고 실제 참조 파일이 local referenced_image_paths에 첨부됐다. 생성·저장·ledger 기록은 성공했으며, 관리형 픽셀 리뷰는 record_valid=true / technical_qualification=fail이다. 독립 testcase는 3 PASS / 3 FAIL로 전체 FAIL이다. 사용자 수락은 pending이다. 실제 이미지 모델명은 도구가 제공하지 않아 unknown/null로 유지했다.

- 이미지: images/native-attempt1.png (1536×1024)
- 이미지 SHA-256: 575691523e9d3829fd5d9cfcf10bc6de9a4a8d2d0186f18dbd8aeac636f33d35
- 도구 원본: /Users/chasoik/.codex/generated_images/01a163f1-49a4-7483-80ce-e5cebe7179fb/exec-be728bbc-912f-45f2-bfe4-c426a0cb9923.png
- exact prompt: final-prompt.txt, SHA-256 ad165eeb588d3acfce10b4c37d01c4f1a526427457d75a6196200bdadd3b35a6
- Core canonical SHA-256: fde610416463d7bef720888d43fd0354d58750763b51f16f4bf56f173c694325
- Testcase SHA-256: 4257fc0a3d2b8cb7b5b8148a871f6a43267814dc1e251dbf4dde6d4ed37d1164
- Controls canonical SHA-256: 087113fcc3f188e7d4d5a5835ea3e35ba584bdbca5bfe27aa199545c897f03bf
- Saved controls: sensual=1, fetish=0, creativity=1, surreal=0; overrides={}
- Installed H-F2 generation: c34c69bb6a031f2938987cc687a51481e01d24710e7ba06f5e05f4130a91f849
- Native generation: f764682eefe81421e209e28d5dddfeb63981a25834c73799790f44a09fcff431
- 실행 스킬 SHA-256: f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089
- Recorded source HEAD: 7119ab133ed0f9f9cdf25bce717d5dd9bc4e6be6
- Actual shared checkout: /Users/chasoik/Projects/image-prompt
- Ledger: image_runs.ndjson, 1 row, run_id=28a8cef1bb14fba9
- Independent manifest: run_manifest.json; cross_arm_inputs_used=false is an explicit declaration, not proof inferred from image diversity.

## Source exposure and final use

Three role queries and two whole-scene queries were issued once. contact_point returned zero due the sealed context phrase "without hiding the clamp" being projected as nonpositive_scope_without_requested_change. physical_motion, space_condition, request_topic and baseline_prompt each exposed eight candidates; all 32 query/CID/RID occurrences were distinct and individually reviewed in source-reviews.json. No query was changed or resampled.

New space-horror V02 (cand_85efea06edc050df8e26491433c115f0, source 2f9ab2ed6c2213275f75be112401cc3607f410b1907e22c1cc635b4b9ad32966) and V64 (cand_ad404f4ef4a959779e011d2753f31587, source a35eb9f9e441900063f288c42161e91c71250cbdb96c7a4b74f7bda73e090efa) were exposed by the baseline query. Both were skipped. All H-F2 material uses are skip; final inspiration_only=0 and native whole-source adoption=0. Therefore these pixels test the independently authored space-horror scene, not a demonstrated causal improvement from adoption of the new candidates.

Three complete English alternatives were compared at creativity 1: A1 pooled tears/closed lips, A2 a peeling membrane corner, A3 watching the corridor from doorway shadow. The baseline won because one face-hand-gap attention line and one failure mechanism were clearer. Full texts and candidate-specific comparisons are in composition-comparison.md. Agent-chosen staging was not promoted into requester facts. First core/testcase/controls remain unchanged.

## Every independent testcase gate

| Gate | Result | Observability | Pixel finding |
|---|---|---|---|
| B01 pressure boundary | FAIL | partial | Clear sheet, clamps, two frosted capsules and star-filled hull tear are present, but full upper-right/right perimeter attachment is cropped or body-occluded. |
| B02 last clamp contact | FAIL | partial | Right hand grips the red lever and left palm braces the same jamb; the required short seam to the left of the lever is not independently distinguishable. |
| B03 pressure direction | FAIL | partial | The bright stream flares into the foreground/right corridor side; membrane bow into the bay is ambiguous. |
| B04 reference appearance | PASS | visible | Assessable face broadly matches the supplied short dark bob/fringe, eyes, rounded cheeks and pink lips; identity and age are not inferred. |
| B05 embodied support | PASS | visible | A floor knee, opposite planted boot, torso and both connected working arms form a plausible supported crouch on the corridor side. |
| B06 visible story | PASS | visible | Improvised spacecraft survival repair is readable from the hand, fragile sheet, frozen bay and nearby exterior breach; this qualitative reading does not override failed physical relations. |

Managed embodiment gates: ownership PASS, joint-chain/reach PASS, support/balance PASS, contact/space PASS, visibility/projection FAIL(partial). The exact review was accepted as a valid failure record. Gate evidence is in visual_review.json; independent gate detail is in pixel_review.testcase.json.

## Whole-image observations and limits

The warm reference-guided face, purposeful grip, cold bay reflections and exposed void give a clear human survival stake. The bright polished scene reads closer to restrained science-fiction danger than oppressive dread. Her raised gaze does not follow the gap, and the failed flow/perimeter relations weaken the intended mechanism. Subtle personal appeal is perceived as supporting; no added fetish fixation or surreal symbolic relation is evident. These are image-grounded observations, not user preference or acceptance. No additional image call, API/CLI fallback, or repair was performed.

## Exact final prompt

```text
A photographic space-horror scene records a dangerous moment aboard a spacecraft. At the right side of a wide rectangular hatch, a woman whose facial appearance and hairstyle follow the supplied portrait crouches beside the final clamp of a temporary clear pressure partition. Her dark chin-length bob and wispy fringe frame large brown eyes, softly rounded cheeks and natural pink lips. Her concentrated face carries an intimate, vulnerable presence within the emergency; a small sheen of perspiration catches the work light. She wears a fitted off-white thermal coverall with worn utility seams. The corridor around her still holds breathable air. Beyond the transparent partition, two frost-coated cryogenic storage capsules flank a torn opening in the ship's outer wall, exposing small sharp stars in black space. The partition is the thin physical boundary preserving the corridor. Its upper and side edges are already captured by evenly spaced metal clamps; its clear sheet bows away from her into the depressurized bay. At the lower-right corner, a short unfinished seam remains visibly open just to the left of a red over-center lever. Fine white condensation threads stream through that gap away from the corridor toward the open bay. She has one knee on the corridor floor and the opposite boot planted firmly beside her. Her right hand closes around the red lever, folding it toward the lower-right jamb; her left palm braces the same solid jamb above the clamp. Her arms remain on the corridor side of the sheet. She watches the remaining gap as she works, lips slightly parted, with the incompletely closed lever and the escaping threads visible together. Photograph from the corridor at a shallow oblique angle, wide enough to include all four partition edges, her face, both connected arms, the grounded knee and boot, and the torn hull beyond. Keep the clamp large and unobstructed beside her hand. A warm portable work lamp describes her face and fingers against cold blue reflections on the transparent sheet; a dim red service beacon recedes into the bay. The vulnerable clear surface, purposeful hand, and indifferent patch of outer space form the photograph's visual hierarchy, with tactile condensation and restrained documentary grain.
```
