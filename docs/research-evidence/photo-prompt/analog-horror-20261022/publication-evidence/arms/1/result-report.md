# 독립 테스트 Arm 1 — 빈 의자에 앉아 있는 녹화 속 얼굴

독립 로컬 난수로 선택한 컨셉은 개인 VHS 녹화물 안에는 누군가 앉아 있지만, 실제 방의 같은 의자는 비어 있는 장면이다. 후보 접근 전에 382단어 기준 프롬프트와 코어를 동결했고, 이후 일반적인 TV 베젤 경계만 보강한 392단어 최종 프롬프트를 감사해 생성했다.

- Frozen core: `49f724db2c14e89a363ae740a38576abd6e77f62ed6ec02dd519f39497e43b1c`
- H-F2 material generation: `d5aec2788e925fb6e8b27831b0055a2545067372edf87a6d5c7ea233a716ebfa`
- Internal native validation closure: `001cc620209e5bfa3a23f8d0ef41766eb8e96446887d809739094e7435b76c52`
- Final exact prompt SHA256: `26f4bb06a9c5efd19e7799520ac1bdfa36741cf1323cae7bebcf83388359c84a`
- Native initial image calls: **1**, built-in `image_gen.imagegen`; observed model unavailable.
- Original reference was actually passed through `referenced_image_paths`, SHA256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.
- Returned/copied image SHA256: `1fee87e777c1425b6614386a8ad5a93b841d6d64da3e38359991af846cede4b9`; image 1536×1024.

4 full-pool queries returned 32 occurrences / 30 unique sources. Every occurrence has a source-hash-bound decision and every source has its complete meaning/conditions/effects review. Newly registered A038 and A049 were exposed. A038’s two-adult/table source was skipped. A049’s whole adult-viewer/TV-room contract was not adopted because its full age/count/subject conditions and source qualification were not supplied. Only a generic independently justified plastic bezel boundary influenced the final open composition. Native chosen CID lists remain empty.

The comparison preserves a full baseline, bezel clarification, bright modern room, 4:3/date framing and doorway-view option. The bezel clarification wins for screen ownership without adding a second story or crowding the chair comparison.

The actual saved PNG was opened through `view_image`. The seven authored scene gates and five embodiment gates are each `visible`/`pass`; the scene whole-case result is `pass` under `partial_is_fail` and `UNOBSERVABLE_NOT_PASS`. The generated chair occupancy, empty physical chair, matching diagonal seam, screen-local corruption and checking gaze are readable together. This is a scene-level observation, not native qualification or proof of all A038/A049 source gates. The displayed figure resembles the foreground woman in broad cues, so unfamiliar identity is unproven. Actual medium history, dates, temporal motion, sound and supernatural causation remain unproven. Reference guidance is appearance only. User acceptance remains **pending** and no rendered baseline exists for a preference/improvement claim.

Managed `review-audit` completed with `status: pass`, `record_valid: true`, `technical_qualification: pass`. User judgment remains `not_yet_received` / pending.

## Files

- `final-prompt.txt`: exact human-readable prompt.
- `composed.json`: authored composition and 32 occurrence decisions; immutable audited copy is referenced by workflow state.
- `generated-image.png`: unchanged copied native output.
- `exact-native-precall-proof.json`: exact prompt/reference and audit bindings saved before the image call.
- `native-tool-call-start.json`, `native-tool-result-metadata.json`, `image-copy-proof.json`, `image_runs.ndjson`: actual invocation/result proof.
- `material-semantic-review.json`, `composition-comparison.md`, `theme-integration-trace.json`: source meaning, comparison and final impact.
- `theme-pixel-review.json`, `visual-review.json`, `whole-image-observations.json`: native pixel observations and claim limits.
- `review-audit-output.json`: final managed review audit result.
