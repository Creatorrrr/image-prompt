# Restore the unpublished integration history

Verified incoming main: `98847a8bcc35f85142fe0eb4322e35eacbe9fdc2`
Pre-pull cleanup checkpoint: `06bd1edb6dfc5f3b69aad78137ec3fd3755a9f97`
Branch in the bundle: `data-action-context-effects-20261001`
Final semantic dictionary: `c59474d21f2d1ae56d228811f4d086d82a88e2d137e630d484a6e9ef3766975c`

This delivery is a Git bundle of unpublished commits, not a remote publication. It retains both the pre-pull checkpoint and the final merge history. The incoming main commit and its ancestors are prerequisites, available from the public origin repository. The final merge commit is identified in the delivery manifest.

1. Concatenate the listed `.bundle.partNN` files in manifest order. Every part is below 10 MB
2. Verify the complete bundle SHA-256 against the manifest
3. In a repository containing the incoming main commit, run `git bundle verify <bundle>`
4. Fetch the bundle's branch into a new, unused local branch, for example `git fetch <bundle> refs/heads/data-action-context-effects-20261001:refs/heads/recovered-action-context-effects`
5. Inspect the recovered branch before switching or merging. Preserve any unrelated local work

The bundle contains the relevant source changes, generated index shards, tests and research evidence. Credentials and unrelated untracked files are excluded. It does not configure authentication, run an API call, or push anything.

Current integrated checks:

- `python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py`
- `python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index`
- `python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check`
- `python -m unittest tests.test_photo_action_context_effects_cleanup tests.test_photo_clothing_terminology_semantics -v`
- `python docs/research-evidence/photo-prompt/action-context-effects-integration-20261001/evaluate_merged_cache.py`

Historical checks belong to their historical source snapshot. To reproduce the 9,887-document cleanup results, use a separate worktree at the preserved cleanup checkpoint and run its `verify_saved_results.py`. Do not run that historical validator on the 10,174-document integrated corpus and call its expected snapshot mismatch a current regression.

The delivery manifest records bundle verification and an isolated recovery comparison. The source/evaluation history was not rewritten when upstream's scoped metadata validator fixed the old 22 errors. Both the historical failure logs and current successful validator result remain available.
