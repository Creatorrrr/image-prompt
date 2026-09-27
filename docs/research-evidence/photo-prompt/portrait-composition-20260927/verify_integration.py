"""Read back installed sources, generated indexes and unchanged pre-existing vectors."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    semantic = pg.load_semantic_index_payload(ASSETS / 'photo_prompt_semantic_index.json')
    visual = read(ASSETS / 'photo_prompt_visual_profile_index.json')
    pg.validate_semantic_index_metadata(semantic, data)
    pg.validate_visual_profile_index_metadata(visual, registry)
    before = HERE / 'integration/pre-rebuild'
    old_manifest = read(before / 'photo_prompt_semantic_index.json')
    old_entries = {}
    for shard in old_manifest['shards']:
        path = ASSETS / shard['path']
        assert sha(path) == shard['sha256'], path
        old_entries.update(read(path)['entries'])
    assert set(old_entries) <= set(semantic['entries'])
    unchanged = sum(semantic['entries'][key] == value for key, value in old_entries.items())
    assert unchanged == len(old_entries)
    old_visual = read(before / 'photo_prompt_visual_profile_index.json')['entries']
    assert all(visual['entries'][key] == value for key, value in old_visual.items())
    extension = read(ASSETS / 'photo_prompt_portrait_composition_extension.json')
    reference = extension['maintenance_ref']
    record = read(ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' / (reference['record_id'] + '.json'))
    assert reference['sha256'] == cs.digest(record)
    raw = dict(extension)
    raw.pop('maintenance_ref')
    assert record['authored_source_sha256'] == cs.digest(raw)
    profile_source = read(ASSETS / 'photo_prompt_visual_obligations_portrait_composition.json')
    assert record['visual_profile_source_sha256'] == cs.digest(profile_source)
    profiles = [p for p in registry['profiles'] if p['id'].startswith('pc_')]
    expected = {f"slot:{slot}:{e['id']}" for slot, rows in extension['slots'].items() for e in rows}
    assert expected <= set(semantic['entries'])
    files = [SKILL / 'SKILL.md', SKILL / 'scripts/prompt_generator.py', ASSETS / 'photo_prompt_tags.json',
             ASSETS / 'photo_prompt_semantic_index.json', ASSETS / 'photo_prompt_visual_profile_index.json',
             ASSETS / 'photo_prompt_visual_obligations.json',
             *[ASSETS / name for name in pg.RESEARCH_EXTENSION_FILENAMES],
             *[ASSETS / name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]]
    result = {
        'schema_version': 'portrait-composition-runtime-integration/v1',
        'status': 'pass_for_source_and_generated_index_integrity',
        'dictionary_hash': pg.dictionary_hash(data),
        'visual_registry_sha256': visual['registry_sha256'],
        'counts': {
            'new_atoms': len(expected), 'new_optional_bundles': sum(b['id'].startswith('pc_bundle_') for b in data['candidate_bundles']),
            'new_profiles': len(profiles), 'new_gates': sum(len(p['render_gates']) for p in profiles),
            'semantic_index_entries': len(semantic['entries']), 'visual_index_profiles': len(visual['entries'])
        },
        'preserved_preexisting_index_entries': {'semantic': unchanged, 'visual': len(old_visual)},
        'source_snapshot': {str(path.relative_to(ROOT)): sha(path) for path in files},
        'claim_boundary': 'Does not certify candidate exposure, selection or image pixels.'
    }
    out = HERE / 'integration/verification.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'source_snapshot'}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
