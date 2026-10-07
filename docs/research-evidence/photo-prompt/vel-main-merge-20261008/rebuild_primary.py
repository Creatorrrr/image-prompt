"""Rebuild combined primary indexes offline using only exact compatible vectors."""
from pathlib import Path
import json
import runpy
import sys

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
WORK = Path(__file__).resolve().parents[4]
SKILL = PRIMARY/'skills/photo-prompt-image-generator'
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL/'scripts'))
import prompt_generator as pg
import build_semantic_index as sem
import build_visual_profile_index as visual

data = pg.load_json(SKILL/'assets/photo_prompt_tags.json')
expected = sem.base_payload(data, pg.SEMANTIC_PROVIDER, pg.SEMANTIC_MODEL_ID,
                            pg.DEFAULT_SEMANTIC_DIMENSIONS)
texts = {key: pg.semantic_text_for_entry(entry, slot, kind=kind)
         for key, kind, entry, slot in pg.iter_semantic_entries(data)}
entries = {}
for path in [SKILL/'assets/photo_prompt_semantic_index.json',
             WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json']:
    payload = pg.load_semantic_index_payload(path)
    if not sem.metadata_matches(payload, expected):
        continue
    for key, row in payload['entries'].items():
        if (key in texts and row.get('text') == texts[key]
                and len(row.get('vector', [])) == pg.DEFAULT_SEMANTIC_DIMENSIONS):
            entries[key] = row
assert len(entries) == len(texts), 'Unresolved embedding inputs; no API calls authorized by this offline merge'
registry = pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
profile_cache = WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json'
profile_vectors = visual.reusable_vectors(
    [profile_cache, SKILL/'assets/photo_prompt_visual_profile_index.json'], registry,
    provider=pg.SEMANTIC_PROVIDER, model=pg.SEMANTIC_MODEL_ID,
    dimensions=pg.DEFAULT_SEMANTIC_DIMENSIONS)
assert len(profile_vectors) == len(registry['profiles']), 'Unresolved visual embedding inputs'
cache = PRIMARY/'.codex-artifacts/vel-main-merge-20261008/compatible-semantic.partial'
sem.write_payload(cache, {**expected, 'entries': entries}, compact=True)
sys.argv = ['build_semantic_index.py', '--checkpoint', str(cache), '--batch-size', '1',
            '--progress', '--keep-stale-generations', '--no-runtime-publication']
try:
    runpy.run_path(str(SKILL/'scripts/build_semantic_index.py'), run_name='__main__')
except SystemExit as exc:
    if exc.code:
        raise
sys.argv = ['build_visual_profile_index.py', '--cache-index',
            str(WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json'),
            '--batch-size', '1', '--no-runtime-publication']
try:
    runpy.run_path(str(SKILL/'scripts/build_visual_profile_index.py'), run_name='__main__')
except SystemExit as exc:
    if exc.code:
        raise
(OUT/'PRIMARY-INDEX-REBUILD.json').write_text(json.dumps({
    'semantic_entries': len(texts), 'exact_compatible_semantic_vectors': len(entries),
    'pending_semantic_embeddings': 0,
    'visual_profiles': len(registry['profiles']),
    'exact_compatible_visual_vectors': len(profile_vectors),
    'pending_visual_embeddings': 0,
    'provider_model_dimensions_and_text_checked': True,
    'canonical_builders': ['build_semantic_index.py', 'build_visual_profile_index.py'],
    'source_root': str(SKILL)}, indent=2)+'\n')
