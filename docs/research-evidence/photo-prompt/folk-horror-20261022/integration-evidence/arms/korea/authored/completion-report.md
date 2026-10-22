# Folk Korea independent arm completion

완료 상태: 실제 native 생성 1회 성공, 원본 픽셀의 전체 의도 충족은 FAIL. 리뷰 기록의 형식/바인딩은 검증 통과했으며 실패 판정을 완화하지 않았다. 사용자 수락은 pending이다.

- Run: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/folk-korea-20261022-6e9460-s3`
- Prompt: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/folk-korea-20261022-6e9460-s3/final-prompt.txt`
- Original copy: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/folk-korea-20261022-6e9460-s3/generated-original.png`
- 원본 크기: 1330×1182 PNG
- 원본 SHA-256: `bcf4e46d1be21096bda18d164218c984691bbce915eecfcf14c7ce5daf05da95`
- 참조: `/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg`
- 참조 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`
- Latest skill SHA-256: `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`
- Final prompt SHA-256: `b850daf50098b1a2aa83131c7f9b080e7ecf39aebc66d9bcc156e56cfcc4f2c5`
- Tool: `image_gen.imagegen`, actual calls **1**, API/CLI fallback **0**

## Independent scene and boundary

Six independently authored Korean-village situations were subjected to a local OS-entropy draw, selecting a well-at-dawn encounter. A fictional adult archivist stops beside a closed communal well and wet bare footprints while two residents stay in separate house thresholds. The reference supplies visible face/hair appearance only; actual identity, age, biography or temperament were not inferred. All scene particulars were authored before retrieval. No other arm prompt, candidates, image or results were read.

The first prepared run bound the full neutral slot catalog by an unintended scope-free prepare command. It remains preserved without candidate retrieval or image calls. This final run keeps the same draw/request/controls seed/core/baseline and explicitly seals three relevant slots. See setup-restart.md.

## Gate results

| Boundary | Result | Evidence |
|---|---|---|
| Independent core / controls / neutral features / embodiment | PASS | managed freeze and slot seal; frozen request/reference inventories |
| New installed generation | PASS | H-F2 `0ad30ffe246d77f7c711ea49244b407b71ff747cbc33b380f6f12aaacd657cf2`; native `4cf1bf4117010c240ccb49148e2ee1bd5be2ca58d79c1f1521888aa16f9c0b20` |
| Retrieval and complete source/occurrence review | PASS | 3 slots + 2 whole-scene queries; 40 occurrences, 38 unique sources; source-review.json/full-source-records.json/returned-occurrences.json |
| Candidate-informed comparison | COMPLETE | eight complete alternatives plus exact frozen baseline; composition-comparison.md |
| Final prompt / runtime / native plan | PASS | compose-command-v2.json, prepare-render-command.json, native-plan-command.json |
| Actual generation / saved bytes / ledger / independent manifest | PASS | one call; returned tool path copied byte-for-byte; image-provenance.json/image_runs.ndjson/run_manifest.json |
| Original-pixel body checks | 4 PASS, 1 FAIL | visual-review.authored.json; visibility_and_projection=fail/partial |
| Original pre-render tests | 2 PASS, 2 UNOBSERVABLE_NOT_PASS | pixel-test-results.json |
| Review record validity | PASS | review-audit-command.json: status=pass, record_valid=true |
| Technical image qualification | FAIL | review-audit-command.json: technical_qualification=fail |
| Native whole-source qualification | NOT_ESTABLISHED | no native candidate selected; material native_approval=false |
| Newly added CID to pixels | NOT_TESTED | no new CID naturally exposed or retained |
| Requesting-user acceptance | pending | no direct user judgment |

The initial composition audit failed because clarification evidence was serialized as a list rather than a literal string; only that wire shape was repaired. The later PASS used the same final prompt bytes and consumed no image call.

## New-source exposure and use

Natural topic-related returns included existing `cand_1f1816e8fc67563886f54dfcac2b1a75` (material card R12, reused as current registry R01), `cand_cf10b18c7fa75a3a86e310963870e86f`, `cand_2abe883103a65d9395a7432e314820e5`, and `cand_fd97cb14fc7c573b9628a17d99421dc4`. The coordinator confirmed none are newly added CIDs. All 40 occurrences were skipped after complete-source applicability and whole-image comparison. Matching baseline details were not retroactively credited to retrieved data. Final prompt equals the independently frozen baseline. There is therefore no adopted new card → literal prompt → pixels trace in this arm, and no CID was injected to manufacture one.

## Pixel judgment

The original image supports the reference-guided short dark bob, fringe and general facial impression at environmental scale; two separately owned hands hold the notebook; both boots meet the ground coherently. A quiet occupied village, doorstep witnesses, visible covered well and unusual wet bare sole shapes create a plausible folk-horror impression. This does not prove a supernatural event, shared belief, authentic ritual or actual history.

The well lid and rim are cropped on the left. The nearest wet mark merges with damp ground, and the trail runs toward the lower foreground instead of establishing the complete intended route to the woman's boots. Foreground soles and a partial lid cannot prove the missing origin, full boundary or endpoint relation. Those relations remain **UNOBSERVABLE_NOT_PASS**. The body visibility/projection gate is fail with partial observability; no unseen deformity is diagnosed. The imagined narrative is more specific than what the pixels establish.

The saved manifest's status=success records the generation outcome. It does not override the separate technical_qualification=fail or pending user acceptance. No additional generation or repair was performed.
