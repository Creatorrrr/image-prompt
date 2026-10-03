"""Preserve both authored intents and regenerate indexes from exact caches."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SNAPSHOT = Path('/tmp/image-prompt-slang-merge-20261003-otvpg0ba')
ASSETS = Path('skills/photo-prompt-image-generator/assets')
REGISTRY = ASSETS / 'photo_prompt_visual_obligations.json'
VISUAL = ASSETS / 'photo_prompt_visual_profile_index.json'
SEMANTIC = ASSETS / 'photo_prompt_semantic_index.json'
sys.path.insert(0, str(ROOT / ASSETS.parent / 'scripts'))
import prompt_generator as pg
import build_semantic_index as sb

helpers = runpy.run_path(ROOT / 'docs/research-evidence/photo-prompt/semantic-guidance-merge-20261003/reconcile_merge.py')
merge_json = helpers['merge_json']
choose_vector = helpers['choose_vector']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def git_bytes(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def semantic_cache(manifest, ref=None):
    rows = {}
    for descriptor in manifest['shards']:
        path = ASSETS / descriptor['path']
        current = ROOT / path
        raw = current.read_bytes() if current.exists() else b''
        if sha(raw) != descriptor['sha256']:
            assert ref is not None, path
            raw = git_bytes(ref, path)
        assert sha(raw) == descriptor['sha256'], path
        shard = json.loads(raw)['entries']
        assert len(shard) == descriptor['entry_count']
        assert not rows.keys() & shard.keys()
        rows.update(shard)
    assert len(rows) == manifest['entry_count'] and set(rows) == set(manifest['entry_order'])
    return {**manifest, 'entries': rows}


def main():
    source = read(SNAPSHOT / 'SNAPSHOT.json')
    base, remote = source['base'], source['remote']
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == remote
    parents = {name: read(SNAPSHOT / name / REGISTRY) for name in ('base', 'local', 'remote')}
    expected = merge_json(parents['base'], parents['local'], parents['remote'])
    # Check Git's authored merge before normalizing its JSON serialization.
    assert read(ROOT / REGISTRY) == expected
    by = {name: {p['id']: p for p in registry['profiles']} for name, registry in parents.items()}
    changed = {name: {pid for pid, row in by[name].items() if row != by['base'].get(pid)}
               for name in ('local', 'remote')}
    assert not changed['local'] & changed['remote']
    actual = {p['id']: p for p in expected['profiles']}
    assert all(actual[pid] == by['local'][pid] for pid in changed['local'])
    assert all(actual[pid] == by['remote'][pid] for pid in changed['remote'])
    exclusive_local = {}
    for name, digest in source['local_files'].items():
        if Path(name) in (REGISTRY, VISUAL, SEMANTIC):
            continue
        assert sha((ROOT / name).read_bytes()) == digest, name
        exclusive_local[name] = digest
    remote_paths = subprocess.check_output(['git', 'diff', '--name-only', base, remote], cwd=ROOT, text=True).splitlines()
    exclusive_remote = {}
    for name in remote_paths:
        if Path(name) in (REGISTRY, VISUAL):
            continue
        raw = git_bytes(remote, name)
        assert (ROOT / name).read_bytes() == raw, name
        exclusive_remote[name] = sha(raw)
    for name, digest in source['protected_unrelated_files'].items():
        assert sha((ROOT / name).read_bytes()) == digest, name
    (ROOT / REGISTRY).write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n')
    save('PRESERVATION.json', {
        'schema_version': 'photo-slang-authored-merge-proof/v1',
        'base': base, 'pulled_remote': remote, 'local_stash': source['stash_oid'],
        'local_modified_profile_ids': sorted(changed['local']),
        'remote_modified_profile_ids': sorted(changed['remote']),
        'overlapping_modified_profile_ids': [],
        'each_modified_profile_equals_its_authored_parent': True,
        'exclusive_local_files': exclusive_local,
        'exclusive_remote_files': exclusive_remote,
        'protected_unrelated_files': source['protected_unrelated_files'],
        'unrelated_file_count': len(source['protected_unrelated_files']),
        'registry_sha256': sha((ROOT / REGISTRY).read_bytes()),
    })

    data = pg.load_json(ROOT / ASSETS / 'photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(ROOT / REGISTRY)
    metadata = sb.base_payload(data, pg.SEMANTIC_PROVIDER, pg.SEMANTIC_MODEL_ID, pg.DEFAULT_SEMANTIC_DIMENSIONS)
    semantic_parents = {
        'local': semantic_cache(read(SNAPSHOT / 'local' / SEMANTIC)),
        'remote': semantic_cache(json.loads(git_bytes(remote, SEMANTIC)), remote),
    }
    visual_parents = {name: read(SNAPSHOT / name / VISUAL) for name in ('local', 'remote')}
    semantic_counts, visual_counts = Counter(), Counter()
    semantic_provenance, visual_provenance = {}, {}
    bm25f = pg.build_semantic_bm25f_payload(data)
    entries = {}
    for key, kind, row, slot in pg.iter_semantic_entries(data):
        text = pg.semantic_text_for_entry(row, slot, kind=kind)
        vector = choose_vector(key, text, semantic_parents, metadata, semantic_counts, semantic_provenance)
        entries[key] = {'kind': kind, 'slot': slot, 'id': row['id'], 'text': text,
                        'vector': vector, 'bm25f_document': bm25f['documents'][key]}
    vectors = {p['id']: choose_vector(p['id'], pg.visual_profile_semantic_text(p),
                                    visual_parents, metadata, visual_counts, visual_provenance)
               for p in registry['profiles']}
    semantic = {**metadata, 'entries': entries,
                'bm25f': {key: value for key, value in bm25f.items() if key != 'documents'}}
    pg.validate_semantic_index_metadata(semantic, data)
    manifest = sb.write_sharded_payload(ROOT / SEMANTIC, semantic, keep_stale_generations=True)
    visual = pg.build_visual_profile_index_payload(registry, vectors=vectors,
        provider=metadata['provider'], model=metadata['embedding_model'], dimensions=metadata['embedding_dimensions'])
    (ROOT / VISUAL).write_text(json.dumps(visual, ensure_ascii=False, indent=2) + '\n')
    loaded = pg.load_semantic_index_payload(ROOT / SEMANTIC)
    pg.validate_semantic_index_metadata(loaded, data)
    pg.load_visual_profile_index(ROOT / VISUAL, registry)
    assert loaded['entries'] == entries
    save('INDEX-RECONCILIATION.json', {
        'schema_version': 'photo-slang-merged-index-proof/v1',
        'profiles': len(vectors), 'exact_terms': len(visual['exact_lookup']),
        'slot_candidates': sum(len(rows) for rows in data['slots'].values()),
        'semantic_entries': len(entries), 'dictionary_hash': metadata['dictionary_hash'],
        'registry_sha256': visual['registry_sha256'],
        'semantic_exact_text_reuse': dict(semantic_counts),
        'visual_exact_text_reuse': dict(visual_counts),
        'matching_text_provider_model_dimensions_required': True,
        'shared_matching_vectors_equality_checked': True,
        'bm25f_recomputed_from_merged_authored_data': True,
        'embedding_api_calls': 0, 'native_image_calls': 0,
        'historical_shards_deleted': 0,
        'semantic_shards': [str(ASSETS / row['path']) for row in manifest['shards']],
        'semantic_entry_provenance': semantic_provenance,
        'visual_entry_provenance': visual_provenance,
    })
    print(json.dumps({'local_profile_changes': sorted(changed['local']),
                      'remote_profile_changes': sorted(changed['remote']),
                      'profiles': len(vectors), 'semantic_entries': len(entries),
                      'visual_cache': dict(visual_counts), 'semantic_cache': dict(semantic_counts),
                      'embedding_api_calls': 0}))


if __name__ == '__main__':
    main()
