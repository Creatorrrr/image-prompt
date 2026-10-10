"""Use canonical builders and compatible complete caches; refuse new embeddings."""
import argparse
import datetime
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import build_semantic_index as semantic
import build_visual_profile_index as visual
import prompt_generator as generator
from photo_source_manifest import SourceInventory
from photo_runtime_sources import source_update

parser = argparse.ArgumentParser()
parser.add_argument('--cache-root', type=pathlib.Path, action='append', required=True)
parser.add_argument('--label', default='scoped')
args = parser.parse_args()
provider, model, dimensions = generator.SEMANTIC_PROVIDER, generator.SEMANTIC_MODEL_ID, generator.DEFAULT_SEMANTIC_DIMENSIONS

def deny_embedding(texts, **kwargs):
    raise RuntimeError(f'Offline build requires {len(texts)} uncached embeddings; no provider invocation was made.')

cache_semantic = [root / 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json' for root in args.cache_root]
cache_semantic.append(ASSETS / 'photo_prompt_semantic_index.json')
cache_visual = [root / 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json' for root in args.cache_root]
cache_visual.append(ASSETS / 'photo_prompt_visual_profile_index.json')
for path in cache_semantic:
    metadata = json.loads(path.read_text())
    assert metadata['semantic_text_recipe'] == semantic.SEMANTIC_TEXT_RECIPE_VERSION
for path in cache_visual:
    metadata = json.loads(path.read_text())
    assert metadata['semantic_text_recipe'] == generator.VISUAL_PROFILE_TEXT_RECIPE_VERSION

data = semantic.load_json(ASSETS / 'photo_prompt_tags.json')
semantic.embed_texts_with_gemini = deny_embedding
checkpoint = pathlib.Path.home() / '.cache/image-prompt/wardrobe-main-publication-20261010' / (args.label + '-semantic.partial.json')
checkpoint.parent.mkdir(parents=True, exist_ok=True)
payload = semantic.build_resumable_index_payload(data, output=ASSETS / 'photo_prompt_semantic_index.json',
    checkpoint=checkpoint, provider=provider, model=model, dimensions=dimensions,
    batch_size=1, request_interval=0, retry_attempts=1, retry_initial_delay=0,
    cache_indexes=cache_semantic)
payload['created_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
inventory = SourceInventory.load(ASSETS)
registry = visual.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json', inventory=inventory)
vectors = visual.reusable_vectors(cache_visual, registry, provider=provider, model=model, dimensions=dimensions)
missing = [profile['id'] for profile in registry['profiles'] if profile['id'] not in vectors]
assert not missing, f'Offline visual build requires uncached profiles: {missing}'
visual_payload = visual.build_visual_profile_index_payload(registry, vectors=vectors, provider=provider, model=model, dimensions=dimensions)
with source_update(SKILL):
    semantic.write_sharded_payload(ASSETS / 'photo_prompt_semantic_index.json', payload, shard_count=16, keep_stale_generations=True)
    visual.write_payload(ASSETS / 'photo_prompt_visual_profile_index.json', visual_payload)
report = {'schema_version':'wardrobe-publication-index-build/v1', 'status':'PASS', 'label':args.label,
    'semantic_entries':len(payload['entries']), 'visual_profiles':len(visual_payload['entries']),
    'visual_exact_terms':len(visual_payload['exact_lookup']), 'embedding_provider':provider,
    'embedding_model':model, 'embedding_dimensions':dimensions, 'new_embedding_calls':0,
    'cache_roots':[str(root) for root in args.cache_root],
    'recipe_identity_and_full_text_and_vector_space_checked':True,
    'indexes_built_from_scoped_authored_source':True,
    'runtime_publication':'separate full validation before activation'}
(HERE / (args.label + '-index-build.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False), flush=True)
