"""Use the production builders with compatible parent vectors and no API calls."""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
DEST = Path('/Users/chasoik/.codex/worktrees/vocaloid-main-merge/image-prompt')
ASSETS = DEST / 'skills/photo-prompt-image-generator/assets'
HERE = PRIMARY / 'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/main-merge'
sys.path.insert(0, str(DEST / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg
import build_visual_profile_index as visual
import build_semantic_index as semantic

def offline(*args, **kwargs):
    raise AssertionError('Cache miss: review the required embedding before making any API call.')
visual.embed_texts_with_gemini = offline
semantic.embed_texts_with_gemini = offline
registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
vis = ASSETS / 'photo_prompt_visual_profile_index.json'
sem = ASSETS / 'photo_prompt_semantic_index.json'
cache = HERE / 'index-parent-cache'
cache.mkdir(exist_ok=True)
shutil.copy2(vis, cache / vis.name)
# Semantic cache remains usable until its final atomic write; old shards stay.
data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
meta = json.loads(sem.read_text())
provider, model, dims = meta['provider'], meta['embedding_model'], meta['embedding_dimensions']
vectors = visual.reusable_vectors([cache / vis.name, PRIMARY / 'skills/photo-prompt-image-generator/assets' / vis.name], registry,
                                  provider=provider, model=model, dimensions=dims)
profiles = registry['profiles']
missing = [p['id'] for p in profiles if p['id'] not in vectors]
assert not missing, missing
payload = visual.build_visual_profile_index_payload(registry, vectors=vectors, provider=provider, model=model, dimensions=dims)
visual.write_payload(vis, payload)
pg.load_visual_profile_index(vis, registry)
checkpoint = HERE / 'semantic-merged.partial.json'
assert not checkpoint.exists()
combined = semantic.build_resumable_index_payload(
    data, output=sem, checkpoint=checkpoint, provider=provider, model=model, dimensions=dims,
    batch_size=1, request_interval=0, retry_attempts=1, retry_initial_delay=0,
    cache_indexes=[sem, PRIMARY / 'skills/photo-prompt-image-generator/assets' / sem.name],
)
combined['created_at'] = datetime.now(timezone.utc).isoformat()
manifest = semantic.write_sharded_payload(sem, combined, shard_count=16, keep_stale_generations=True)
receipt = {'schema_version': 'vocaloid-main-merge-index-rebuild/v1', 'status': 'pass',
           'visual_profiles': len(profiles), 'semantic_entries': len(combined['entries']),
           'embedding_calls': 0, 'native_image_calls': 0, 'parent_vector_compatibility': [provider, model, dims],
           'reuse_requires': 'same stable entry, exact positive text, provider, model, dimensions',
           'stale_generations_preserved': True,
           'visual_index_sha256': hashlib.sha256(vis.read_bytes()).hexdigest(),
           'semantic_index_sha256': hashlib.sha256(sem.read_bytes()).hexdigest()}
(HERE / 'INDEX-REBUILD.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt))
