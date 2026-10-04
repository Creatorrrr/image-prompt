"""Keep retained local drafts searchable without publishing their derived indexes."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
PUBLISHED_ROOT = next(p for p in Path(__file__).resolve().parents if (p / '.git').exists())
ASSETS = PRIMARY / 'skills/photo-prompt-image-generator/assets'
PUBLISHED = PUBLISHED_ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
import build_semantic_index as semantic
import build_visual_profile_index as visual


def cache_miss(*args, **kwargs):
    raise AssertionError('Unexpected local draft embedding cache miss')


def rebuild():
    semantic.embed_texts_with_gemini = cache_miss
    visual.embed_texts_with_gemini = cache_miss
    sem = ASSETS / 'photo_prompt_semantic_index.json'
    vis = ASSETS / 'photo_prompt_visual_profile_index.json'
    old = json.loads(sem.read_text())
    provider, model, dimensions = (old[k] for k in ('provider', 'embedding_model', 'embedding_dimensions'))
    data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    with tempfile.TemporaryDirectory(prefix='primary-draft-indexes-') as directory:
        directory = Path(directory)
        shutil.copy2(vis, directory / vis.name)
        vectors = visual.reusable_vectors([directory / vis.name, PUBLISHED / vis.name], registry,
                                         provider=provider, model=model, dimensions=dimensions)
        assert all(row['id'] in vectors for row in registry['profiles'])
        payload = visual.build_visual_profile_index_payload(registry, vectors=vectors, provider=provider,
                                                           model=model, dimensions=dimensions)
        visual.write_payload(vis, payload)
        combined = semantic.build_resumable_index_payload(
            data, output=sem, checkpoint=directory / 'local.partial.json', provider=provider,
            model=model, dimensions=dimensions, batch_size=1, request_interval=0,
            retry_attempts=1, retry_initial_delay=0, cache_indexes=[sem, PUBLISHED / sem.name])
        semantic.write_sharded_payload(sem, combined, shard_count=16, keep_stale_generations=True)
    pg.load_visual_profile_index(vis, registry)
    pg.validate_semantic_index_metadata(pg.load_semantic_index_payload(sem), data)
    receipt = {
        'status': 'pass', 'scope': 'Local retained drafts only; not the published source tree',
        'dictionary_hash': combined['dictionary_hash'], 'registry_hash': payload['registry_sha256'],
        'semantic_entries': len(combined['entries']), 'visual_profiles': len(registry['profiles']),
        'embedding_calls': 0, 'native_image_calls': 0,
        'authored_drafts_modified': False, 'shards_deleted': False,
        'semantic_index_sha256': hashlib.sha256(sem.read_bytes()).hexdigest(),
        'visual_index_sha256': hashlib.sha256(vis.read_bytes()).hexdigest(),
        'full_suite_qualification': 'Applies to the isolated published tree; local drafts remain uncommitted.',
    }
    out = PRIMARY / 'docs/research-evidence/photo-prompt/seduction-expression-main-merge-20261005/PRIMARY-WORKING-INDEXES.json'
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    return receipt


if __name__ == '__main__':
    print(json.dumps(rebuild()))
