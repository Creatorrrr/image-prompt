Arm C qualification: blocked, pixels unscored

Independent random seed: `8f0040ca75299371254dbda8c32957fd`.
Scene: a fictional adult woman in a theater prop repair room just after the final curtain, holding a curling scenery plan flat with a red enamel paperweight while briefly glancing across the table toward the photographer. Supplied reference uses visible face/hair appearance only; the original is unchanged.

Frozen targets: true grayscale except the single red paperweight; raised charcoal dark floor with readable hair/shelf detail; local dodge-and-burn cheek tone evening with readable pores. All three are agent-authored advisory testing goals, not requester-prescribed scene locks.

Single v6 pack: `a025b7e5aa06507c`. Target-effect candidates and visual concepts were not exposed. The only exposed new editing row was `slot:motion:pe_camera_sweep`; it was rejected because camera-motion traces compete with the crisp face/skin/hand test. No editing ID was invented, no candidate or visual concept selected, and no second pack generated.

Precore validation, composed prompt audit and exact native runtime/reference audit: PASS. Baseline/final prompt: 262 whitespace-counted words, unchanged from independent freeze. Canonical runtime core SHA-256: `a7aff6a3462a015b8a5c985d13dbdc48160493ef9a67b395ea477a0e8fcbff51`; intent lock: `7a26d10876c1f9502c89381a46295016eb8a2787739e3e1daad485a50eb6446a`.

Exactly one built-in `image_gen.imagegen` call occurred. It returned `moderation_blocked`, output stage, category `sexual`, request ID `7bbaf540-2f1a-9950-9126-11a0a41ee429`. Raw native error is retained exactly in `attempt-01-native-error.json` with SHA-256 `24f7cba92769a3a8e694e63c14e89be56e03433b156d81f0bfca01bb4e211bad`. No delivered image path exists. No CLI fallback, prompt mutation, downgrade or additional image call followed.

Color splash, lifted blacks, skin detail, all five physical gates and scoped reference appearance are UNSCORED. Strict all-of verdict: `unscored_blocked`. This is not a pixel quality failure or a technical pixel pass. User acceptance remains `not_yet_received`.

Primary artifacts: `qualification_result.json`, `pre_render_test_case.json`, `pack_exposure.json`, `pixel_review.json`, `image_runs.ndjson`, `run_manifest.json`, `composed_prompt.json`, `prompt_en.txt`, `negative_en.txt`, `render_request.json`, `render_request_audit.json`, `interventions.json`. The arm-local ledger run ID is `a74369d920440caa`. Every output is confined to this arm directory; no other arm input was consulted.
