# Generic manual role-view integration — read-only release plan

Recommend **three production files and two new tests**: `photo_semantic_evidence.py`, `photo_slot_semantics.py`, `photo_role_proposals.py`; proposed new `tests/test_photo_native_manual_role_views.py` and `tests/test_photo_native_manual_role_view_transport.py`. No code/test edit is authorized or performed in this task. B2 remains frozen.

The committed pure helper (385 lines) and its full test (304 lines), plus 08250 handoff/API obligations, were directly read. The helper binds exact structure; it neither qualifies source truth nor infers the meaning of a facet. Its expected binding must be independently supplied by the native full-source validation path. Its class and hashes are not authentication capabilities.

The current fit chain is `role_proposals.propose(data) -> slot_semantics.fit -> native.qualification`. The proposal has actual corpus data today, including lazy access to full pinned records. Pass this source context explicitly through that existing chain. For an opted-in candidate, load the full source via `source_data.candidates[CID]` (the existing lazy `SearchReader.record` checks its published record digest), run full native validation and derive the expected binding from that source. Compare the compact receipt under test to this independently derived binding. Do not use the receipt, public pack `authored_record`, metadata flag, supplied expected hash or Python class as its own authority. Initial stateless bounded compilation avoids a new cross-request authority cache.

Proposed opt-in authoring shape:

- Top proof remains `photo-candidate-role-evidence/v4`; optional nonempty `manual_role_views` holds exact existing helper v1 view declarations.
- A role may add nonempty unique `view_refs`; its original `fact_refs` stay canonical. A failing dimension/prefix fact needs its own explicit exact view. Ordinary dimension+prefix support remains unchanged. Views do not bypass mode, actual RID, role coverage or guard support checks.
- Build helper context only after original full source/fact/unit/effect/owner/guard/dependency/profile validation. Positive fields come from native primary-path/positive-string policy, and the ordinary unit must directly name that same canonical fact. References, guard text and metadata cannot anchor it.
- Compact emits a generated `manual_role_view_bindings` field only for this opt-in and keeps exact role `view_refs`. Seal it with existing compact hash and whole-proof qualification hash. Keep `native_contract_sha256` implementation unchanged; optional authored fields are naturally included, and absent-field bytes remain unchanged.
- Every view must be consumed by its exact role/facts/RID, with all canonical target/receiver positions and complete P/PR requires. No property/dimension alias or new E is generated.

The same native support helper serves full validation and qualification. It can return an exact view as an exception to ordinary role taxonomy only, retaining the complete original canonical fact. Source-local and actual-owner E consistency, all receivers, P/PR per member, actual guards, selected child/profile duties, whole permissions and locks remain B2 responsibilities and are unchanged. Guard-only role support remains separate. A preservation reference sentinel cannot turn into a positive trait; context cannot become direct.

Existing transport appears sufficient without a new pass-through field: `c.entry`/layout delegate to native compact; lazy data retain full payload access; public packs retain complete authored records and proposals; global audit replays the same proposal with pinned source data; full composition and fresh runtime already revalidate source and whole actual closure. These are concrete existing paths, not a claim that future integration tests have passed. Add an extra file only after a preserved execution shows an actual drop.

Implementation order after root release:

1. Native optional shape, full-source compiler, common direct-or-view support and sealing; focused authority/old-byte tests.
2. Explicit source context through slot semantics and role proposals; independently build expected binding for opted-in full/compact lookup.
3. Real isolated lazy/public-pack/compose/fresh-runtime tests, including selected member/profile and one-B1-per-full-audit checks; any failed drop trace goes to root before expanding files.
4. Hard model-import/embedding denial, env-i plus OS network deny, applicable existing regressions, immutable logs/hashes/diff and freeze. Parent separately reviews actual source/proof and performs operating publication/Git.

The paired JSON specifies 15 adversarial groups: exact ordinary quote occurrence and wrong-field/RID rejection; unsupported out-of-prefix facts; self-hashed/forged receipts and missing external authority; every P/PR and receiver; unchanged joint E/locks; required/optional/profile closure; separate guard support; stale source/spec/proof pins; immutable pack and fresh runtime; existing resource caps. Parent-named first50 seven relational cases,1271 hand-held and1286 mirror are later manual-review targets only. No source/proof is changed or approved here. The1264 typed-person issue remains root-owned.

No tests were rerun for this planning task. No production/test/source/catalog/proof/status/runtime/index/Git modification and no provider/model/embedding/network call.
