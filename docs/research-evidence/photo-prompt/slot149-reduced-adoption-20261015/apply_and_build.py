"""Install only the verified staged delta, then rebuild using local vectors only."""
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path[:0] = [str(SKILL / 'scripts'), str(SKILL / 'precore')]
os.environ['PHOTO_EMBEDDING_BACKEND'] = 'embeddinggemma2-local'
os.environ['HF_HUB_OFFLINE'] = os.environ['TRANSFORMERS_OFFLINE'] = '1'
for key in ('GEMINI_API_KEY', 'GOOGLE_API_KEY'):
    os.environ.pop(key, None)
import photo_candidate_corpus as c
import photo_local_embedding as local
from photo_runtime_sources import source_update
from build_shared_candidate_index import build


def main():
    assets = SKILL / 'assets'
    staged = Path('/tmp/photo149-staged-assets-20261015')
    before = c.load(assets)
    assert c.digest(before) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
    source_report = json.loads((HERE / 'STAGE03.json').read_text())
    after = c.load(staged)
    assert c.digest(after) == source_report['result_sha256']
    relation_report = json.loads((HERE / 'STAGED-RELATIONS.json').read_text())
    names = list(relation_report['source_files_sha256'])
    for name in names:
        assert hashlib.sha256((assets / name).read_bytes()).hexdigest() == relation_report['source_files_sha256'][name]
    changed = [name for name in names if (assets / name).read_bytes() != (staged / name).read_bytes()]
    assert set(changed) == set(relation_report['changed_files']) | {source_report['changed_file']}
    assert len(after['slot_catalog']) == 149 and len(after['candidates']) == 18250
    backup = Path('/tmp/photo149-operating-before-20261015')
    backup.mkdir(exist_ok=False)
    for name in changed:
        (backup / name).write_bytes((assets / name).read_bytes())
    space = local.space()
    assert space['provider'] == 'embeddinggemma2-local'
    with source_update(SKILL):
        for name in changed:
            temporary = assets / (name + '.slot149-pending')
            with temporary.open('xb') as handle:
                handle.write((staged / name).read_bytes())
            temporary.replace(assets / name)
        assert c.digest(c.load(assets)) == c.digest(after)
        report = build(assets, HERE / 'build-cache', space=space, batch_size=32)
        assert report['records'] == 18180
        assert report['vector_reuse'] == 18180
        assert report['provider_calls'] == report['provider_cache_hits'] == 0
        assert c.digest(c.load(assets)) == c.digest(after)
    result = dict(schema='photo-slot149-operating-install/v1', source_before_sha256=c.digest(before),
                  source_after_sha256=c.digest(after), changed_authored_files=changed,
                  corpus_validation='PASS', local_build=report, Gemini_calls=0,
                  candidate_changes=1, new_bindings=2, deferred_bindings=3489,
                  unchanged_candidates=18249, slots=149, native_qualified_candidates=1)
    with (HERE / 'STAGE04.json').open('x') as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
