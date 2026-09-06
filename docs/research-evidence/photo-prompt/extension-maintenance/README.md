# Extension maintenance records

The ten `photo_prompt_*_extension.json` records preserve former prose-only
`semantic_policy` and `representation_modes` declarations. Each runtime extension
references its immutable maintenance record by ID and canonical JSON SHA-256.
The records include the pre-migration source-file hash. They are documentation,
not a second executable policy source, and their prose is not copied into packs.

The original extension `visual_semantics` rows remain the authored source for
102 optional candidate bundles. The loader validates and compiles those rows;
the pack, compact view, selected component evidence, and relation evidence use
the compiled result. Legacy `hard_profile_id(s)` fields become advisory
`associated_profile_ids`; they do not independently activate a profile.

`candidate-data-review-20260906.json` records selected candidate corrections by
stable slot/ID and current record hash. Its contract verification status is
separate from rendered-image evidence and requester judgment. The source slot
ownership table is conservative and leaves uncertain scopes unavailable for
bundle adoption. It is not a claim that all candidate meanings have been
externally verified.

The actual generator integration artifacts are under
`docs/analysis/2026-09-06-photo-data-implementation/candidate-contracts/`. They
preserve a generated v6 pack, the exact detail view, and selected bundle evidence.
That evidence is a focused contract fixture, not an independently rendered trial.
