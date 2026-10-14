# Manifest-bound inverse-review verification handoff, 2026-10-14

Status: independent research tool and isolated tests frozen for root review. No actual worker result has been run through this verifier by this worker. Root selects immutable inputs/checkpoints/notes and runs the real verification. The previous native-v3 production, integration, tests and authoring guides remain frozen and were not edited in this task.

New files in this task:

- `../verify_inverse_reviews.py`
- `tests/test_photo_direct_inverse_reviews.py` (repository-relative)
- this note

Tool byte SHA256: `77b75e54ff255022a719f1b12d0ea41343c3d780c45144dc56857cc2bf7655bf` (53,114 bytes).
Test byte SHA256: `2667b70f1a0765e439cc0c74683157bb82b018a42b4303eedb6ad4cb6aa089c3` (38,348 bytes).

## Scope and evidence boundary

The tool imports only Python standard-library modules. It does not import direct_review, inference providers, search readers, semantic classifiers, native qualification, or production publishing code. It does not execute scripts in selected artifacts. It performs no directory listing, wildcard discovery, network/model calls, Git actions, source correction, tag assignment, registration, CURRENT update or runtime publication.

It checks bound saved data and **worker declarations**. Passing does not prove the worker physically read the sources, root personally read every worker source, the fit assertion entails the quoted sentence, semantic accuracy, image pixels, native qualification, trained tags, a 141-slot search, or a runtime candidate-free core. Explicit false fields in the output retain these limits. Root's selection manifest is the trust boundary; the verifier cannot independently prove when a historical hash witness was first frozen.

`passed` applies only to the manifest-selected ranges. It does not imply all 139 slots were selected or finished. File names, prepared packets and unselected files never establish completion. Submitting only a completed checkpoint is valid; missing expected pairs inside that selected checkpoint fail. Selecting overlapping checkpoint ranges fails.

## Exact manifest contract

CLI requires all of `--root`, `--manifest`, and `--manifest-sha256` (the byte SHA256 of the exact manifest). Use the repository as root when selected artifact paths are repository-relative. Relative reference paths recorded by workers may resolve against either repository root or the manifest directory, but must identify exactly one already-selected descriptor. No undeclared reference is opened or probed.

```json
{
  "schema": "photo-direct-inverse-review-selection/v1",
  "artifacts": {
    "delegation": {
      "path": "docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/INVERSE-DELEGATION-139-01.json",
      "encoding": "json",
      "byte_sha256": "<root-pinned exact bytes SHA256>",
      "canonical_sha256": "<root-pinned canonical SHA256>"
    },
    "search": {"path": "<exact saved search path>", "encoding": "json", "byte_sha256": "<64 hex>", "canonical_sha256": "<64 hex>"},
    "plan": {"path": "<exact query-plan path>", "encoding": "json", "byte_sha256": "<64 hex>", "canonical_sha256": "<64 hex>"},
    "source": {"path": "<exact SOURCE.json.gz path>", "encoding": "gzip-json", "byte_sha256": "<compressed bytes SHA256>", "canonical_sha256": "<decompressed JSON canonical SHA256>"},
    "proposed": {"path": "<exact CATALOG-CORRECTED-PROPOSAL-01.json path>", "encoding": "json", "byte_sha256": "<wrapper bytes SHA256>", "canonical_sha256": "<wrapper JSON canonical SHA256>"},
    "review": {"path": "<exact worker checkpoint path>", "encoding": "json", "byte_sha256": "<64 hex>", "canonical_sha256": "<64 hex>"},
    "packet": {"path": "<exact worker-referenced preparation packet path>", "encoding": "json", "byte_sha256": "<64 hex>", "canonical_sha256": "<64 hex>"},
    "range_note": {"path": "<explicitly selected range worker-note>", "encoding": "bytes", "byte_sha256": "<64 hex>"}
  },
  "inputs": {
    "delegation": "delegation", "search": "search", "plan": "plan", "source": "source", "proposed_catalog": "proposed"
  },
  "reviews": [{
    "artifact": "review", "format": "09250-flat", "task": "/root/review_09250_10500",
    "range": [0, 6], "notes": ["range_note"]
  }]
}
```

Replace every placeholder with a root-selected immutable binding; this example is not an executable manifest. The five `inputs` keys are required and exactly named as shown. `artifacts` and `reviews` must be nonempty. Every descriptor is read and checked, even if only selected as auxiliary evidence. Optional `size_bytes` is checked too. JSON canonicalization uses UTF-8, `ensure_ascii=False`, sorted keys, separators `(',', ':')`, `allow_nan=False`. Canonical hash of a plan descriptor is the **whole JSON**, including its self-declared `canonical_sha256`; the plan's internal hash is independently recomputed excluding that field. Proposed catalog wrapper canonical hash and its inner `catalog` hash are likewise distinct.

Supported `encoding`: `json`, `gzip-json`, `bytes`. JSON duplicate keys and NaN/Infinity are rejected. Artifact paths cannot escape root, traverse `..`, or redirect through symlinks. Bytes and canonical hash errors stop row verification; unbound review bytes are never adjudicated. An invalid selection-manifest hash raises an error before reading descriptors.

Add every file named by a selected worker's `input_hashes` and every recorded packet reference to `artifacts` with its own fixed hash. In particular, 11870 checkpoints name CATALOG.json, WORKER-INSTRUCTIONS.md (initial checkpoint), and/or Python helpers (later chunks). Add range notes explicitly via selected descriptors and each review's `notes` list. Notes are byte-bound auxiliary material; Markdown prose is not automatically converted into review verdicts or completion claims. A descriptor alone does not constitute a direct-read declaration.

For 07250 use `format: "07250-rows"`, its exact selected half-open range/task, and an additional `impact: "<artifact ID>"` pointing to the separately descriptor-bound impact JSON. The impact's adjudication link is checked against **canonical JSON SHA**, as actually authored, not byte SHA. It must refer back to the selected adjudication artifact and agree on range, task, counts, original verdict spellings and native/stage proof boundaries. The original impact object is preserved in the verification result.

For 11870 use `format: "11870-slots"` and `/root/review_11870_12250`. For 07250 task is `/root/review_07250_08250`. Actual assignments come from the selected immutable delegation; root-selected checkpoint ranges must lie inside them. No filename-derived assignments are accepted.

## Frozen auxiliary hashes and prior reads

A selected `.py` or a descriptor with `mutable_auxiliary: true` requires `initial_hash_witness`. The witness must point to an already-selected JSON artifact and its **previously recorded** byte SHA string:

```json
{
  "path": "<exact helper.py path>",
  "encoding": "bytes",
  "byte_sha256": "<previously closed initial helper byte SHA>",
  "initial_hash_witness": {
    "artifact": "<selected frozen review or initial-ledger ID>",
    "pointer": "/input_hashes/authored~1helper.py/bytes_sha256"
  }
}
```

The pointer uses ordinary JSON-pointer escaping (`/` inside a key becomes `~1`). A current helper with different bytes fails against both the descriptor and closed witness. Missing, self-attested or mismatching witnesses fail. Never measure an accumulating `author.py` now and label that new value its initial frozen hash. Root must select the authentic earlier witness; this tool does not reconstruct an absent history or certify the witness's historical authenticity.

11870 explicit `exact_duplicate_of` / `duplicate_record_equal_to` must refer to a selected read ID of the same worker and exact full source hash, earlier in the same selected file or in an earlier selected range. Missing prior artifacts, wrong source/worker, later/self references and cycles fail. Select earlier frozen review checkpoints as additional `reviews` entries when they are needed to witness reuse. Duplicate selected review pairs remain prohibited.

09250's `prior_frozen_inverse_fullread` contains no read ID in the actual format. It can only be witnessed by an earlier manifest-selected same-worker checkpoint with that exact CID/full source hash and a non-reuse full-read claim. The verifier does not find one by searching the authored directory or by treating a prepared packet as a read. Missing prior evidence fails rather than inventing a physical read.

07250 has no per-read reuse identity in these samples. Its pair declarations and unique source counts are preserved, but this parser does not invent fresh-read versus reuse counts from repeated CIDs.

## Three formats and explicit field variants

- **09250 flat:** `individual_reviews`, `slot_reviews`, `actual_read_ledger`, assigned/completed slot ranges; separate baseline/proposed verdicts remain separate. The source-binding hash, complete source conditions/effects, actual RIDs, exact reference hashes, positive fit_fact and lane positions (when authored) are checked. Complete read ledger covers parent plus required closure CID union. Original literal fields remain under `raw_artifact` and each normalized row's `raw`.
- **11870 nested initial:** `slot_reviews[*].individual_judgments`, `direct_read_log`, `assigned_sorted139_range`, `closure_read_id`, `complete_semantic_source_read`, `closure_complete`, `all_distinct_semantic_fields_conditions_effects_alternatives_read`, `binding_ids`, `actual_realization_ids`, `exact_duplicate_of`.
- **11870 nested later chunks:** same schema, but explicitly observed `parent_assigned_sorted139_range`, `full_source_read_id`, `full_semantic_source_conditions_effects_alternatives_read`, `complete_required_closure_read`, `frozen_binding_ids`, `realization_ids`, `duplicate_record_equal_to`. The parent subrange must be inside the root delegation and contain the selected checkpoint. It never replaces the root assignment. Known duplicate alias fields must agree. Optional full `proposal141_spec` is checked when supplied. This is a bounded compatibility parser, not a spelling/meaning inference mechanism.
- **07250 flat rows plus impact:** `rows`, original `judgement`, `actual_root_effects`, `actual_effects_by_realization`, intrinsic conditions, full source hash, CID reference hashes, binding-definition hashes and declared full scope are checked.

11870's single `authored_status` is a baseline verdict; the authored proposed impact/spec fields are retained. The tool does **not** copy it into a new proposed-catalog fit verdict. 07250's `fit/unfit/hold` and impact literals likewise remain authored as given. 09250's `fit/not_fit/defer`, 11870's `fit/nonfit/pending`, and explicit pending/defer values keep their original spelling. There is no cross-format verdict conversion, tag approval or silent repair.

## Mechanical checks and limits

1. Delegation/model/effort/task, half-open range containment, complete sorted baseline slot ordering, source/catalog/bindings/plan/search/proposed catalog hashes; explicit baseline/proposed spec and query bindings.
2. For **each selected slot**, recompute the union of the first three saved BM25F ranks, embedding ranks (called `dense` by workers), and saved RRF ranks. Exact expected `(slot ordinal, CID)` pairs are required, with no duplicates or selected-range overlap. This replays no search model, embedding inference, RRF oracle or runtime query.
3. Full parent record SHA, kind, complete conditions/effects and the exact list of actual RIDs. For 07250, exact root-plus-selected-branch effects are independently reconstructed per actual RID; unselected branch properties do not leak. Source pointers must address strings under `/content`, quotes must be nonblank **exact substrings**, and source/candidate hashes or identities in anchors must agree. No paraphrase/whitespace normalization is performed.
4. Required closure traverses exact ID-valued dictionary keys and string values recursively: both CID and binding IDs, including each binding's resolved CID and nested references. Full records and full binding definitions (including guards) are hashed. CID-looking words inside prose do not become invented references. Missing closure/binding records, changed targets/conditions or incomplete declarations fail.
5. 11870 explicitly declares binding IDs and pins the entire frozen source containing their definitions; the tool verifies that exact ID set and computes their current frozen definition hashes. 07250 supplies full binding hashes. Actual 09250 samples lack separate binding-read fields: if a source requires bindings, the generic full-closure claim is insufficient and fails `missing_binding_read_declaration`. Supported explicit fields are `binding_ids_actually_read` or `binding_sha256`; the verifier never adds them or fabricates an acknowledgement. Root may preserve the original artifact and require a new separately authored, bound read declaration in subsequent review work.
6. For an authored **fit** only: a manually authored positive fact is mandatory; its dimension must be in the corresponding spec, its property must equal a declared prefix stem or be below a declared property prefix (matching existing direct-review punctuation rules), and its owner must be nonblank, non-wildcard and not end with a dot. Source-local names/Korean owners remain exact literals. There is no new lowercase-only naming restriction.
7. `spec.owners` contains categories such as `entity`, while authored owners can be concrete strings such as `other_declared_adults`. There is no source-independent exact equivalence map in these worker formats. The tool therefore records the literal owner and validates its shape; it **does not infer category-to-owner equivalence, anatomy or alias relationships**. Human semantic owner/spec suitability remains unverified. It does not reject a named owner just because it is not the literal string `entity`.
8. Primary fit facts anchored only in routing/discovery/negative/review/schema labels fail separately as `metadata_only_primary_fit`: activation, aliases, terms/keywords, match/any/all/exact/evidence/context terms, validation evidence-field labels, IDs, family/topic IDs, priority dimensions, claim limits, exclusions, review/provenance and other explicit deny labels. Quoted literals and authored fit verdicts are retained. This is a pointer-surface failure, not an automatic assertion that the authored semantic verdict is false. Natural-language positive bodies such as definition, concept units, relation sentences, embedding_text, rendered instructions, and member requirements/concept_units are not blocked merely for their positive field name. The tool still does not establish their truth or entailment. Nonfit/defer/pending evidence is not promoted into a primary positive fit fact.

The actual 09250 checkpoint contains an action fit anchored at `/content/authored_components/components/1/evidence_terms/0`. That exact source surface illustrates why a separate metadata-only fit-anchor failure exists. This observation does not edit or invert its authored verdict, and is not a full verification of that actual checkpoint.

## Counts

Each selected review summary separates delegated assignment's prepared top3-union pair count (recomputed from the saved search), actual selected checkpoint pair declarations, expected selected pairs, unique parent sources, unique closure sources, closure sources additional to parents, combined unique sources, and binding definitions. Explicit authored prepared/read/impact counts are checked where present.

Global counts distinguish pair occurrences, distinct pairs, selected slots, unique parent/closure/combined sources, explicitly declared reuse occurrences and ledger occurrences. Ledger units remain format-specific: 09250 logs unique parent-plus-closure records, 11870 logs per pair with closure declarations, 07250 uses per-pair full-read claims without reuse identities. They are not a physical I/O measurement or a common count of newly read documents. Raw per-format counts and transport descriptions remain available for root review.

## Output and execution

Without `--output`, CLI prints only a compact status/count summary and writes nothing. With an explicit `--output`, it creates a **new** JSON using exclusive create, within the selected manifest's directory subtree and root. Existing files, CURRENT-named files, non-JSON destinations and symlink redirects are refused. Failed verification can be preserved as a new immutable report; it is never patched into a pass. No default output or global registration exists.

Example (paths/hashes deliberately placeholders; root supplies exact selected names):

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  python3 docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/verify_inverse_reviews.py \
  --root /Users/chasoik/Projects/image-prompt \
  --manifest docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/ROOT-SELECTED-INVERSE-MANIFEST.json \
  --manifest-sha256 '<exact selected manifest byte SHA256>' \
  --output docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/ROOT-SELECTED-NEW-VERIFICATION.json
```

## Offline validation

Executed only isolated fixture tests, shaped from the actual three worker formats and the explicitly observed later 11870 field variant. No actual inverse-result verification, source change, 141-slot rerun or operating artifact mutation was performed by this worker.

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p test_photo_direct_inverse_reviews.py -q
```

Result: **33 tests passed**. A second run with a `unittest.TextTestResult.addSubTest` counter recorded **33 tests / 38 subtests, 0 failures, 0 errors**, 2.707 seconds. Fixtures cover all parsers/known field variants, literal verdict preservation, source/kind/conditions/effects/RIDs, branch-property isolation, CID/binding-only closure, hash/guard changes, pointer escapes and exact quotes, metadata-only fit failures, named owners and spec prefixes, exact pair completeness and duplication, prepared-versus-actual scope, explicit read reuse/cycles/orphans, closed initial auxiliary mutation, duplicate JSON keys/NaN, paths/symlinks, no-directory-discovery APIs and exclusive explicit output.

Remaining root work: select authentic immutable artifact/hash scope (including earlier reads and all named auxiliaries), run actual data verification, inspect failures without rewriting original judgments, and separately perform any newly authorized manual reread/reanchoring. This tool/test handoff is not actual corpus qualification or a root claim of reading all worker sources.
