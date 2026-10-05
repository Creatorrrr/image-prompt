# V21 visual-profile index storage boundary

This boundary preserves all V1–V20 manifests, candidate packs, immutable proofs and source snapshots. The generated visual index now uses one manifest plus sixteen integrity-bound, content-addressed JSON shards. No vectors were regenerated and no network credentials are needed for migration or validation.

## Provenance

- Previous qualified source: `1d30c96a3a05abfa91f49ac98f205f4e09202a19`
- Storage migration source: `4da854c640d50b85703ad8471779afb02ccdeaa6`
- V20 parent manifest: `V20-PARENT-SOURCE.json`, pinned to the exact original source commit
- V21 proof: `V21-STORAGE-BINDING-PROOF.json`, sealed in the current validator

The V20 parent manifest has 149 exact source members and 207 sealed validation dependencies. It reuses 144 already-retained historical payloads and adds only five snapshots (634,887 bytes): the original validator, universal descriptor, skill instructions, and two authoring references. Each record carries its Git commit, blob identity, mode, byte length and SHA-256. Historical fixtures verify every payload before writing any output, reject path traversal and symlinks, and never invoke Git or substitute current files.

## Preserved contracts

- All 1,813 entries, vectors, entry insertion order and the complete logical index payload are equal to the original monolithic index
- Exact lookup, BM25F, registry/source hashes, embedding provider/model/dimensions and policies retain their original values
- The frozen 64-candidate pack is byte-identical to V20, including candidate order, owner/core/control metadata, negative prompt and privacy boundary
- The active semantic shard generation is unchanged
- V20 keeps its original source checks and its original rejection of V21; its tests run the archived V20 validator against the archived V20 source
- The current validator registers only the specific V21 successor; V22 remains unsupported
- The universal descriptor differs only in the bound current validator hash

The current proof permits exactly four changed existing source files: the visual index manifest, its builder, its runtime caller, and maintenance guidance. The new storage module is the sole source-inventory addition. Sixteen new visual shards are bound separately. Any changed, missing or additional active shard, altered source, extra top-level DATA file, changed historical input or coordinated proof/pack rehash fails the sealed boundary.

## Qualification scope

This is a storage-layout and deterministic frozen-input equivalence claim. It does not establish future independently authored output equivalence or image quality. No image generation was performed.

Focused checks:

```sh
python -m unittest discover -s tests -p 'test_photo_v20_historical_fixture.py'
python -m unittest discover -s tests -p 'test_photo_b5_guidance_boundary_history.py'
python -m unittest discover -s tests -p 'test_photo_visual_storage_boundary_history.py'
```

Use the normal current-boundary validator entry point to also execute the frozen generation command against current source.
