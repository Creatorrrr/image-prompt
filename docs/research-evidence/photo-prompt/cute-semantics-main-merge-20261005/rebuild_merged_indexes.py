"""Rebuild from authored DATA, reusing unchanged vectors from either parent."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as g
import build_semantic_index as semantic_builder
import build_visual_profile_index as visual_builder

data = g.load_json(ASSETS / 'photo_prompt_tags.json')
expected = semantic_builder.base_payload(data, g.SEMANTIC_PROVIDER,
                                         g.SEMANTIC_MODEL_ID, g.DEFAULT_SEMANTIC_DIMENSIONS)
cache_root = HERE / 'index-parent-cache'
parents = {}
for name in ['main', 'local']:
    parent = g.load_semantic_index_payload(cache_root / name / 'photo_prompt_semantic_index.json')
    assert semantic_builder.metadata_matches(parent, expected)
    parents[name] = parent
entries = {}
origins = {}
missing = []
for key, kind, entry, slot in g.iter_semantic_entries(data):
    text = g.semantic_text_for_entry(entry, slot, kind=kind)
    for name, parent in parents.items():
        cached = parent['entries'].get(key)
        if cached and cached.get('text') == text and len(cached.get('vector', [])) == g.DEFAULT_SEMANTIC_DIMENSIONS:
            entries[key] = cached
            origins[key] = name
            break
    else:
        missing.append(key)
assert not missing, f'Review new embedding inputs before proceeding: {missing}'
checkpoint = cache_root / 'exact-match-checkpoint.json'
semantic_builder.write_payload(checkpoint, dict(expected, entries=entries))
def reject_network(*args, **kwargs):
    raise AssertionError('Every input has a verified compatible parent vector; no embedding call expected.')
semantic_builder.embed_texts_with_gemini = reject_network
payload = semantic_builder.build_resumable_index_payload(
    data, ASSETS / 'photo_prompt_semantic_index.json', checkpoint,
    g.SEMANTIC_PROVIDER, g.SEMANTIC_MODEL_ID, g.DEFAULT_SEMANTIC_DIMENSIONS,
    1, 0, 1, 1)
semantic_builder.write_sharded_payload(ASSETS / 'photo_prompt_semantic_index.json', payload,
                                     16, keep_stale_generations=True)
g.validate_semantic_index_metadata(payload, data)

registry = g.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
profile_cache_paths = [cache_root / n / 'photo_prompt_visual_profile_index.json'
                       for n in ['local', 'main']]
vectors = visual_builder.reusable_vectors(profile_cache_paths, registry,
    provider=g.SEMANTIC_PROVIDER, model=g.SEMANTIC_MODEL_ID,
    dimensions=g.DEFAULT_SEMANTIC_DIMENSIONS)
assert len(vectors) == len(registry['profiles'])
visual = g.build_visual_profile_index_payload(registry, vectors=vectors)
visual_builder.write_payload(ASSETS / 'photo_prompt_visual_profile_index.json', visual)
g.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', registry)

record = dict(dictionary_hash=g.dictionary_hash(data), semantic_entries=len(payload['entries']),
              visual_profiles=len(visual['entries']), new_embedding_calls=0,
              semantic_cache_origins=dict(Counter(origins.values())),
              semantic_source_by_id=origins,
              vector_reuse_rule='Exact input text, provider, model, dimensions; vectors copied unchanged.')
(HERE / 'INDEX-REBUILD.json').write_text(json.dumps(record, indent=2) + '\n')
print('Generated indexes:', record['semantic_entries'], record['visual_profiles'],
      '; unchanged-vector sources:', record['semantic_cache_origins'], '; new embedding calls: 0')
