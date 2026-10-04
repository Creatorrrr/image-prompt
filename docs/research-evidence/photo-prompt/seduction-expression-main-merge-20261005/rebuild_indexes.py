"""Rebuild merged projections with exact, vector-space-compatible parent caches."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile

ROOT = next(p for p in Path(__file__).resolve().parents if (p / '.git').exists())
HERE = Path(__file__).resolve().parent
PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
import build_visual_profile_index as visual
import build_semantic_index as semantic


def cache_miss(*args, **kwargs):
    raise AssertionError('Uncached positive text needs a separately reviewed embedding request.')


visual.embed_texts_with_gemini = cache_miss
semantic.embed_texts_with_gemini = cache_miss
vis = ASSETS / 'photo_prompt_visual_profile_index.json'
sem = ASSETS / 'photo_prompt_semantic_index.json'
metadata = json.loads(sem.read_text())
provider, model, dimensions = (metadata[key] for key in ('provider', 'embedding_model', 'embedding_dimensions'))
registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
with tempfile.TemporaryDirectory(prefix='seduction-merged-index-cache-') as temporary:
    temporary = Path(temporary)
    shutil.copy2(vis, temporary / vis.name)
    vectors = visual.reusable_vectors(
        [temporary / vis.name, PRIMARY / 'skills/photo-prompt-image-generator/assets' / vis.name],
        registry, provider=provider, model=model, dimensions=dimensions,
    )
    missing = [profile['id'] for profile in registry['profiles'] if profile['id'] not in vectors]
    assert not missing, missing
    payload = visual.build_visual_profile_index_payload(
        registry, vectors=vectors, provider=provider, model=model, dimensions=dimensions,
    )
    visual.write_payload(vis, payload)
    pg.load_visual_profile_index(vis, registry)
    combined = semantic.build_resumable_index_payload(
        data, output=sem, checkpoint=temporary / 'merged.partial.json',
        provider=provider, model=model, dimensions=dimensions, batch_size=1,
        request_interval=0, retry_attempts=1, retry_initial_delay=0,
        cache_indexes=[sem, PRIMARY / 'skills/photo-prompt-image-generator/assets' / sem.name],
    )
    manifest = semantic.write_sharded_payload(sem, combined, shard_count=16, keep_stale_generations=True)

receipt = {
    'status': 'pass', 'strategy': 'Production builders; exact stable-ID and positive-text reuse after provider/model/dimensions compatibility checks',
    'embedding_calls': 0, 'native_image_calls': 0,
    'semantic_entries': len(combined['entries']), 'visual_profiles': len(registry['profiles']),
    'exact_terms': len(payload['exact_lookup']), 'provider': provider, 'model': model, 'dimensions': dimensions,
    'dictionary_hash': combined['dictionary_hash'], 'registry_hash': payload['registry_sha256'],
    'semantic_index_sha256': hashlib.sha256(sem.read_bytes()).hexdigest(),
    'visual_index_sha256': hashlib.sha256(vis.read_bytes()).hexdigest(),
    'old_shards_preserved': True,
}
(HERE / 'INDEX-REBUILD.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False))
