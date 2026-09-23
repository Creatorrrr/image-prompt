# Arm C targeted qualification

- Request envelope SHA-256: `0b21b8d8e5d32383ba973ace642f33d7e8cca6a9f308cf2f409cec6a68a306b6` (the coordinator's scenario condition was not added to requester text).
- Independent baseline SHA-256: `7d910a82b2082e98f7fec4b9b0611c4a8650963b260eb2b9294e49eeb97ed00d`. The seed selected a compact lived-in living room and a blue paperback being returned to its shelf gap. The original exploratory throw scene remains in the parent arm folder.
- Source/index check: `ed_clean_room_reset` appears in the everyday-scene visual-obligation source and generated visual-profile index. Pack `5b9fe4387d4f08f6` exposed `visual-concept:ed_clean_room_reset` as eligible. The composer selected it; the effective hard visual contract SHA-256 is `71e5986b60d40e3f19783f77829e6e2a38346cb56d434ca3be8082b5f3682331` with four `vo_ed_clean_room_reset_*` gates. Exposure, selection, and hard activation are recorded separately in `candidate_exposure.json`.
- The pre-render `test_case.json` fixes four positive relation gates, confusion targets, five embodiment gates, both review scales, and `partial_is_fail`. Its SHA-256 is `407649d80a147d62fa73006bd54e580a8a267231a3b36d0724f22e1a9843dad6`.
- Composition and exact render-request audits passed for both prompts. Native `image_gen__imagegen` received the attached portrait as visible adult appearance guidance and delivered two local PNGs. The source image and local copies have matching hashes. The two attempts are in `image_runs.ndjson`; `run_manifest.json` refers to attempt 2 and `run_manifest_attempt_1.json` preserves attempt 1.

| Attempt | Scales inspected | Hard gates passed | Hard gates failed | Decision |
| --- | --- | ---: | ---: | --- |
| 1 | 384×512, 1086×1448 | 3 | 6 | FAIL |
| 2, one bounded camera/framing/lighting retry | 512×341, 1536×1024 | 4 | 5 | FAIL |

Attempt 2 improved visible standing support. The selected relation still failed because the book's movement into a receiving gap is ambiguous, the sideboard mark does not establish a recently cleared surface at both scales, and the draped throw does not clearly show an unfinished task. Contact with a distinct shelf gap and the critical projection also failed. The open walking path, body ownership, joint reach, and standing support passed. The exact per-gate pixel observations and schema-valid audit are in `pixel_review_attempt_2.json` and `pixel_review_audit_attempt_2.json`.

Final technical result: **FAIL** under `partial_is_fail`. User judgment remains pending and is not inferred from prompt audit or pixels. No further image call was made after the one allowed retry.
