# Lobed-opening boundary qualification

This evidence qualifies a nine-string DATA correction to the three- and four-lobed opening rejection boundaries. The four-lobed contract no longer rejects its own quatrefoil geometry; the three-lobed boundary explicitly distinguishes openings with a different lobe count. Positive meaning, candidate membership, owners, eligibility, components, prompt evidence requirements, and render gates are preserved.

**Exact candidate-order invariance failed in three of the four natural cases.** The stone, timber, and painted-panel visual-candidate lists changed order. The unchanged runtime orders candidates by a hash of each complete candidate record. Updating the rejection strings therefore changes presentation positions. Applying that existing formula to the before records with only the documented rejection strings replaced reproduces the actual after lists exactly. All candidate ID sets and other candidate-list orders are preserved; the non-target visual candidates retain their relative order. The presentation change could affect later composer choices, which were not measured. An acceptance criterion requiring exact order preservation remains unmet.

## Evidence and scope

The four requests are synthetic and mechanism-informed. Their author did not inspect candidate data, and the before adjudicator did not inspect the proposed correction. This is not real-user evidence or a domain-blind cohort; the paired after review deliberately examines the proposal and both sides. No candidate adoption, final prompt, final audit, rendered image, or image improvement is established.

| Case | Positive-meaning adjudication | Positional / ID-aligned changes | Exact visual order |
| --- | --- | --- | --- |
| Three-lobed stone opening | Three-lobed compatible; four-lobed incompatible count | 161 / 12 | Changed |
| Four-lobed timber opening | Four-lobed compatible; three-lobed incompatible count | 66 / 9 | Changed |
| Painted four-lobed solid panel | Both opening meanings incompatible with solid paint | 169 / 12 | Changed |
| Single round brick opening | Neither target exposed; lobed meanings incompatible if applied | 6 / 6 | Preserved |

The mismatched-count optional exposure and offering aperture meanings for a solid painted panel remain known limitations. Runtime eligibility is not evidence of semantic appropriateness. The target obligations remain conditional opt-in payloads; none of these four packs has an active top-level `visual_obligations` section.

The original timber command failed before pack creation because its setting field lacked three concrete content words. That failure is preserved. Its separately frozen admission adapter changes only `authorial_core.setting` from `A riverside garden` to `a weathered timber gate at a riverside garden`, an unchanged span already present in the request and baseline. Both successful timber runs use this same adapter. Requests, baselines, controls, locks, assertions, and other core fields are unchanged.

## Source identity and receipt interpretation

[QUALIFICATION.json](QUALIFICATION.json) binds this evidence to the source commit, its parent, its source tree, and the original 20-file candidate seal. `source_commit` identifies the committed form of the reviewed DATA/index candidate, rather than the later V23 baseline-integration commit. The original local candidate had parent `900bf2efdd17fbc6a6ef3aa340f3526b1e01f223` and 20-file seal SHA-256 `8bf0dfe263cd9dace49de1f54b4744ab915e56dd49658511f2ef879dc6033f75`.

The preserved after command receipts still say `source: 900bf2efdd17fbc6a6ef3aa340f3526b1e01f223`. They were run against that base plus the locally sealed 20-file candidate, before its commit was created. Their `source_role`, the candidate seal, and the independent file checks distinguish this from a clean-parent run. Those historical bytes have not been rewritten to imply generation at a later commit. The historical candidate summary likewise describes its state at the time it was written.

The actual frozen regression pair is separate from the four natural cases. It reuses the exact V22 and V23 asset packs. Its full comparison has exactly two changes: `/0/pack_id` and `/0/provenance/tags_hash`. All other content and order is identical. The frozen request and baseline live in the existing `tests/fixtures/photo_prompt/current_boundary/core.json`; the envelope, controls, and review are the adjacent fixture files. This shows regression preservation, not lobed-profile adoption or image improvement.

## Reading and verifying the subset

- [Before adjudication](qualification/lobe-before-independent-review/review.md), [structured findings](qualification/lobe-before-independent-review/adjudication.json), and exact source/public-pack extracts preserve the independent before assessment
- [Paired after review](qualification/lobe-after-independent-review/review.md), [full comparisons](qualification/lobe-after-independent-review/all-public-pack-deltas.json), and [summary](qualification/lobe-after-independent-review/summary.json) preserve both positional and separately ID-aligned differences
- `qualification/lobed-opening-authoring/` contains the complete four-case frozen inputs, provenance, bindings, and admission-validation records
- `qualification/lobed-opening-authoring-setting-adapter-01/` preserves the timber adapter and original admission failure; the original failed command and stderr are retained under `qualification/lobed-opening-before-900/`
- The before and after directories contain all eight complete natural candidate packs and their command receipts
- `qualification/lobe-boundary-candidate/` contains the original 20-file seal and candidate build summary; the after review retains every candidate file check and all 32 index-shard identity checks
- [PATH-MAP.json](qualification/PATH-MAP.json) maps historical absolute input/output references to repository-relative files. Every copied artifact retains its exact original bytes. The actual frozen pack files are reused from the V22/V23 assets rather than duplicated

From the repository root, run:

```sh
python docs/research-evidence/photo-prompt/lobe-boundary-integration-20261005/qualification/verify.py
```

This standard-library verifier reads the sealed files, checks relocation and original author/reviewer manifests, rechecks the adapter, reproduces both full public-pack comparisons and the ordering effect, checks the actual frozen pair, and verifies the sealed candidate and index-shard bytes. It makes no network, Git, API, image, or credential calls and writes no files. It does not rerun generation or claim a new independent semantic adjudication. The historical `lobe-after-independent-review/compare.py` is preserved as sealed evidence with its original machine paths; use `verify.py` for this relocated subset.

The `files` object in `QUALIFICATION.json` is a repository-relative path to SHA-256 mapping. It covers this README, every qualification artifact, and the exact existing repository dependencies used by the verifier. It intentionally excludes `QUALIFICATION.json` itself to avoid a circular hash.
