"""Verify immutable upstream sources and append-only autumn context enrichment."""
from pathlib import Path
import copy, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
from photo_source_manifest import SourceInventory

def raw(commit, name):
    return subprocess.check_output(['git', 'show', commit + ':' + name], cwd=ROOT)

def main():
    receipt = json.loads((HERE / 'MANIFEST-MERGE.json').read_text())
    upstream = subprocess.check_output(['git', 'rev-parse', 'MERGE_HEAD'], cwd=ROOT).decode().strip()
    authored = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    manifest_name = 'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json'
    previous = json.loads(raw(upstream, manifest_name))
    current = json.loads((ROOT / manifest_name).read_text())
    assert current['sources'][:len(previous['sources'])] == previous['sources']
    checked = []
    for row in previous['sources']:
        name = 'skills/photo-prompt-image-generator/assets/' + row['file']
        body = (ROOT / name).read_bytes()
        assert body == raw(upstream, name), name
        checked.append({'path': name, 'sha256': hashlib.sha256(body).hexdigest()})
    additions = current['sources'][len(previous['sources']):]
    assert {row['file'] for row in additions} == {
        'photo_prompt_autumn_fashion_extension.json', 'photo_prompt_visual_obligations_autumn_fashion.json'}
    for row in additions:
        name = 'skills/photo-prompt-image-generator/assets/' + row['file']
        assert (ROOT / name).read_bytes() == raw(authored, name), name
    before_inventory = SourceInventory(ASSETS, tuple((r['file'], r['kind'], r['required'], r['load_order']) for r in previous['sources']))
    before = pg.load_json(ASSETS / 'photo_prompt_tags.json', inventory=before_inventory)
    after = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    old = {key: (kind, entry, slot) for key, kind, entry, slot in pg.iter_semantic_entries(before)}
    new = {key: (kind, entry, slot) for key, kind, entry, slot in pg.iter_semantic_entries(after)}
    assert set(old) <= set(new), 'An upstream semantic identity was removed'
    extension = json.loads((ASSETS / 'photo_prompt_autumn_fashion_extension.json').read_text())
    changes = {f'slot:{slot}:{entry_id}': update for slot, entries in extension['existing_slot_context_extensions'].items() for entry_id, update in entries.items()}
    assert len(changes) == 17
    changed = []
    for key, (kind, entry, slot) in old.items():
        actual = new[key][1]
        if key not in changes:
            assert actual == entry, ('Unintended compiled upstream change', key)
            continue
        expected = copy.deepcopy(entry)
        pg.photo_candidate_semantics.extend_slot_contexts({slot: [expected]}, {slot: {entry['id']: changes[key]}})
        assert actual == expected, ('Non-additive autumn enrichment', key)
        old_text = pg.semantic_text_for_entry(entry, slot, kind=kind)
        merged_text = pg.semantic_text_for_entry(actual, slot, kind=kind)
        changed.append({'key': key, 'upstream_text': old_text, 'merged_text': merged_text,
                        'upstream_constraints_and_effects_unchanged': True,
                        'appended_paraphrases': changes[key].get('paraphrases', []),
                        'appended_contexts': changes[key].get('contexts', [])})
    created = set(new) - set(old)
    authored_keys = {f'slot:{slot}:{entry["id"]}' for slot, entries in extension['slots'].items() for entry in entries}
    assert created == authored_keys and len(created) == 112
    registry_path = ASSETS / pg.VISUAL_OBLIGATION_REGISTRY_FILENAME
    old_profiles = {p['id']: p for p in pg.load_visual_obligation_registry(registry_path, inventory=before_inventory)['profiles']}
    new_profiles = {p['id']: p for p in pg.load_visual_obligation_registry(registry_path)['profiles']}
    for identity, profile in old_profiles.items():
        assert new_profiles[identity] == profile, ('Upstream visual profile changed', identity)
    assert len(set(new_profiles) - set(old_profiles)) == 112
    result = {'upstream_commit': upstream, 'autumn_authored_commit': authored,
              'upstream_registered_source_count': len(checked), 'upstream_sources_byte_identical': checked,
              'upstream_manifest_rows_identical': True, 'autumn_sources_byte_identical_to_authored_commit': True,
              'upstream_semantic_identities_preserved': len(old), 'unchanged_upstream_semantic_entries': len(old) - len(changes),
              'reviewed_append_only_enrichments': changed, 'new_autumn_candidates': len(created),
              'upstream_visual_profiles_unchanged': len(old_profiles), 'new_autumn_visual_profiles': 112,
              'removed_upstream_identities': [], 'removed_constraints_or_effects': []}
    (HERE / 'BOTH-SIDES-PRESERVED.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v, (list, dict))}, ensure_ascii=False))

if __name__ == '__main__':
    main()
