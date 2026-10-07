# Camera authoring guidance and the V36 current boundary

The camera guide now describes the contract's actual input form. Partial direction and height constraints use separate `dimension=camera`, `target=camera` property anchors for `viewpoint.direction` and `viewpoint.height`. Combined property strings can pass declaration checks while failing to protect the corresponding overlap. Whole-camera dimension locks remain valid when the whole camera is prescribed, and unprescribed freedoms remain open. The existing total of 1–16 anchors, axis declarations, CLI flags and legacy handling are unchanged.

The guide and its six pure reproduction tests were preserved at `8a6e44fdcf42c1c605dca74b84374020dc1e85b9`. The inactive exact-history helper and its 22 tests were preserved at `534d393b8e4aff7bd45f2502d72b4d1e8448d5a3`. This successor activates the current boundary with an additive validator dispatcher, a V36 descriptor/pack, and one exact validator-hash substitution in the universal descriptor. It changes no photo production code, DATA, schema, provider behavior or anchor limit. The data-improvement count increment is zero.

## Two separate comparisons

The original V35 artifact/source is pinned to `8c2029ea1fecbe206820da6bffa70d2745ada6e2`. Current upstream is `4f3d524ed035de8592e4b0c6ad5030b41ffc55af`, including its earlier P0 and later visual-grammar changes.

| Case | Pack ID | Pack SHA-256 | Environment |
| --- | --- | --- | --- |
| Immutable V35 | `8cf04c2eba2ea3bf` | `1f18f0d6f8c79c856c1bd4162585a53fc7ed379607e11d1123cfff7a8eea22b7` | recorded CPython 3.14.3 / Unicode 16 |
| Fresh unedited 4f3 | `f1d5de6f1a273b65` | `3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075` | CPython 3.12.14 / Unicode 15 |
| Same current source plus guide correction | `f1d5de6f1a273b65` | `3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075` | same current runtime |

V35 → current is an observed historical-to-current difference, with a Python/Unicode mismatch. It is not a same-environment causal experiment. The current → corrected-guide comparison is a same-runtime control and is byte-identical.

The historical comparison contains **42 leaf operations across seven of 29 public surfaces**. The proof represents those same changes as 33 exact operations by replacing three changed arrays with their complete before/after values. Both forms reconstruct the whole actual current pack; no field is ignored.

- A graphite-line → paper junction → strand → raised-flower candidate and optional bundle are added, including their complete ownership, relation, applicability and adoption information. A transition-stage retrieval slot becomes active
- `mounted_albumen_card_print` disappears from the selected medium candidates
- The creative sample changes from `pe_deep_readability` to `matching_reflections_and_depth`, including camera → concept metadata and removal of the optical-focus property and owner relation
- Clarification v2 adds eight applicability diagnostics. The two adult-character interpretations remain gated; `pa_primary_rectangles_orthogonal` changes from requiring an adult context to eligible
- Authored slot pool counts, retrieval bindings and provenance also change

The original pack has 106 candidate occurrences / 99 unique IDs; current has 108 / 100. The comparison's 110 records are their union across candidate groups. Both packs retain 64 public slot candidates. [CANDIDATE-DELTA.json](CANDIDATE-DELTA.json) lists every group and ordered ID, hashes every full record, and includes complete before/after records for every changed, added or removed occurrence. [OBSERVED-LEAF-DELTA.json](OBSERVED-LEAF-DELTA.json) contains all 42 operations, and [PUBLIC-SURFACES.json](PUBLIC-SURFACES.json) binds all 29 fields.

The other 22 full surfaces are unchanged, including the authorial core and intent lock, anchors, exclusions, controls, negatives, safety, embodiment and composition. The baseline composition explicitly declines optional augmentation and preserves the original prompt. This is a qualification of authored meaning and guards, not an image-quality result.

Source inspection separately identifies the retained P0 changes: the `affectionate warmth`, `다정한 애정` and `優しい愛情` aliases belong to shared `surface_affect.open_warmth`, not a deredere profile; yandere intentionality is advisory while its remaining required evidence stays distinct. The upstream grammar addition also changed the `ae_lip_press` text/vector. Those are upstream changes, and their cost is not assigned to this task.

## Freshness and checks

One fresh local publication from packaged indexes produced generation `456ab66e03ca8c8196458ca9fbdf81c9d5ec082feaf2980f00cdfbd4754ff703`, source fingerprint `64ddd1e44c0137305a401ce5c34cbb71766bd56e3b7ebd406bd81c70a8cdd95a`, and algorithm hash `3fde760470ecdd9e06e95113fbf3af604dfe42f601e1f806ec71d2aa6d00ca3a`. Current indexes contain 10,511 semantic and 2,265 visual entries.

Each actual source root independently acquired its namespace, captured live source, generated the fixed seed-910000 pack with the real CLI, and replayed its exact private receipt. Each passed ordinary authorial, core retrieval, full composed-prompt and runtime-request audits. The source fingerprint covers registered assets, precore JSON, scripts/precore Python and the interpreter; it excludes SKILL prose and the illustration qualification code. Both root captures equal the fresh generation, so the empty doc delta does not rely on serving an unchecked edited root from a stale store.

The active default public validator passed again in 103.275 seconds with a fresh real CLI output and receipt recomputation. All 26 focused successor tests passed, including malformed/overlapping deltas, type distinctions, source bindings and rejection of a mismatched asset directory before helper loading. [VALIDATION.json](VALIDATION.json) records that run and its limits; [QUALIFICATION.json](QUALIFICATION.json) records the two-source control. Previously preserved six camera and 22 history tests were not rerun or relabeled as new results.

The proof authenticates all 156 current sources, the 63 immutable historical baseline files and four frozen inputs. Current 32-shard membership derives from exact 4f3 manifests; original V35's 32 shards remain separately bound to its original manifests. Six bodies are shared and 26 differ. Neither inventory substitutes for the other.

## Historical limit and reproduction

The unedited original V35 qualifier genuinely rejects the new current pack with `ValidationFailure: photo V35 frozen pack bytes drift`; [PREEXISTING-V35-FAILURE.json](PREEXISTING-V35-FAILURE.json) preserves its exact call and implementation/input hashes. The successor does not turn that original failure into a historical pass.

Explicit V35 dispatch now selects authenticated original 8c code and retains the original checks. Its fresh probe stops with `HistoricalReplayUnavailable`: the current interpreter is 3.12.14 / Unicode 15, while original history requires 3.14.3 / Unicode 16. The exact historical runtime was not installed or replaced. Broader ancestor payload availability is also incomplete in this sparse environment and was not materialized. No full historical suite passed here, and no historical assertion or artifact was weakened or rewritten.

From a checkout containing the pinned local Git objects and packaged active indexes, use CPython 3.12.14 / Unicode 15 and a separately published local `PHOTO_RUNTIME_STORE`. The V36 descriptor preserves the four original input files and seed; only its output filename changes. Run `python -B -m unittest -v tests.test_photo_camera_guidance_v36`, then call `validate_illustration_assets.validate_photo_regression_baseline` with that checkout's canonical illustration asset directory. Current validation requires the existing store and refuses implicit publisher/fetch/cache-rebuild fallbacks. Exact original historical dispatch additionally requires its declared interpreter and authenticated original closure.

This work made zero provider, image or embedding calls. Private receipts, source captures, runtime stores, complete execution traces and guard-setup diagnostics remain local. Only the compact public evidence required to inspect and reproduce this boundary is included. Latest-main publication must still check the remote tip and preserve any subsequent upstream changes.
