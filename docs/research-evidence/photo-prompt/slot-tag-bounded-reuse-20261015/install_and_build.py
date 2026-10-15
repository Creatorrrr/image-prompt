"""Install only staged binding/policy bytes, reuse local vectors and publish."""
import time
from common import *
from stage_and_verify import verify
import build_shared_candidate_index as builder
import photo_local_embedding as local
from photo_runtime_sources import source_update, SnapshotPublisher, RuntimeSnapshotProvider


def forbidden_embedding(*args, **kwargs):
    raise RuntimeError('Bounded tag-only build must reuse all document vectors; inference forbidden')


def main():
    before = source()
    stage = read(HERE / 'STAGE03.json')
    staged = Path(stage['staged_assets'])
    after = c.load(staged)
    verification = verify(before, after, read(HERE / 'MIGRATION.json'))
    assert verification['result_sha256'] == stage['result_sha256']
    assets = SKILL / 'assets'
    names = stage['raw_stage']['source_files_sha256']
    for name, sha in names.items():
        assert hashlib.sha256((assets / name).read_bytes()).hexdigest() == sha
    changed = stage['raw_stage']['changed_files']
    assert all('slot_bindings_' in name or name == 'photo_candidate_policies.json' for name in changed)
    backup = Path('/tmp/photo-bounded-tags-operating-before-' + str(time.time_ns()))
    backup.mkdir()
    for name in changed:
        (backup / name).write_bytes((assets / name).read_bytes())
    old_search = assets / 'photo_candidate_search.json'
    (backup / old_search.name).write_bytes(old_search.read_bytes())
    space = local.space()
    assert space['provider'] == 'embeddinggemma2-local'
    builder.embed = builder.embed_many = forbidden_embedding
    with source_update(SKILL):
        for name in changed:
            temporary = assets / (name + '.bounded-tags-pending')
            with temporary.open('xb') as handle:
                handle.write((staged / name).read_bytes())
            temporary.replace(assets / name)
        assert c.digest(c.load(assets)) == stage['result_sha256']
        print(json.dumps({'source_installed': True, 'changed_source_files': changed}), flush=True)
        build = builder.build(assets, HERE / 'build-cache', space=space)
        assert build['records'] == build['vector_reuse'] == 18180
        assert build['provider_calls'] == build['provider_cache_hits'] == 0
    print(json.dumps({'local_build_verified': True, 'layout_id': build['layout_id']}), flush=True)
    publication = SnapshotPublisher(SKILL).publish()
    save('PUBLICATION.json', publication)
    snapshot = RuntimeSnapshotProvider(SKILL).acquire(bootstrap=False)
    assert snapshot.generation_id == publication['generation_id']
    assert len(snapshot.data['slot_catalog']) == 149
    assert snapshot.cache_status == 'lazy_verified'
    metrics = dict(snapshot.data.reader.metrics)
    assert metrics['vector_reads'] == metrics['payload_reads'] == 0
    snapshot.data.reader.close()
    report = {'status': 'PASS', 'result_sha256': stage['result_sha256'],
        'changed_authored_files': changed, 'backup': str(backup), 'local_build': build,
        'publication': publication, 'acquire_status': snapshot.cache_status,
        'reader_metrics_at_acquire': metrics, 'document_inference_forbidden': True,
        'candidate_changes': 0, 'new_bindings': 10, 'deferred_released': 6,
        'native_qualified': 1, 'Gemini_calls': 0, 'network': 'OS-denied'}
    save('STAGE04.json', report)
    print(json.dumps({'status': 'PASS', 'generation_id': publication['generation_id'],
                      'layout_id': build['layout_id'], 'document_vectors_reused': 18180}), flush=True)


if __name__ == '__main__':
    main()
