"""Compare the pulled origin authorship with the merged summer contribution."""
import hashlib
import json
import sys
from pathlib import Path

main = Path('/Users/chasoik/Projects/image-prompt')
pub = Path('/Users/chasoik/.codex/worktrees/summer-fashion-publication-20261009/image-prompt')
evidence = main / 'docs/research-evidence/photo-prompt/summer-fashion-publication-20261009'
origin = json.loads((evidence / 'origin-pull.json').read_text())
base = Path(origin['origin_authored_snapshot']) / 'skills/photo-prompt-image-generator/assets'
assets = pub / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(pub / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
import build_visual_profile_index as visual
from photo_source_manifest import SourceInventory

old_inventory, new_inventory = SourceInventory.load(base), SourceInventory.load(assets)
old_data = generator.load_json(base / 'photo_prompt_tags.json', inventory=old_inventory)
new_data = generator.load_json(assets / 'photo_prompt_tags.json', inventory=new_inventory)
old_rows = {key: entry for key, kind, entry, slot in generator.iter_semantic_entries(old_data)}
new_rows = {key: entry for key, kind, entry, slot in generator.iter_semantic_entries(new_data)}
missing = sorted(set(old_rows) - set(new_rows))
assert not missing, missing
changes = {key: sorted(field for field in set(old_rows[key]) | set(new_rows[key])
                       if old_rows[key].get(field) != new_rows[key].get(field))
           for key in old_rows if old_rows[key] != new_rows[key]}
reused = {'fit_ff09_v1_candidate', 'fit_ff52_v1_candidate', 'fit_ff52_v2_candidate',
          'clt_ct031_v1', 'clt_ct064_v1', 'clt_ct064_v2', 'clt_ct065_v2'}
assert {key.rsplit(':', 1)[-1] for key in changes} == reused
assert all(set(fields) == {'paraphrases'} for fields in changes.values()), changes
for key in changes:
    assert set(old_rows[key].get('paraphrases', [])) <= set(new_rows[key].get('paraphrases', []))
old_registry = visual.load_visual_obligation_registry(base / 'photo_prompt_visual_obligations.json', inventory=old_inventory)
new_registry = visual.load_visual_obligation_registry(assets / 'photo_prompt_visual_obligations.json', inventory=new_inventory)
for label, before, after in (
    ('profiles', old_registry['profiles'], new_registry['profiles']),
    ('bundles', old_data.get('candidate_bundles', []), new_data.get('candidate_bundles', []))):
    old = {row['id']: row for row in before}
    new = {row['id']: row for row in after}
    assert all(new.get(key) == value for key, value in old.items()), label + ': existing records changed'
    assert len(new) - len(old) == 159, (label, len(old), len(new))
old_manifest = json.loads((base / 'photo_prompt_source_manifest.json').read_text())
new_manifest = json.loads((assets / 'photo_prompt_source_manifest.json').read_text())
assert new_manifest['sources'][:len(old_manifest['sources'])] == old_manifest['sources']
source_drift = [path.name for path in base.iterdir() if path.is_file() and path.name != 'photo_prompt_source_manifest.json'
                and hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256((assets / path.name).read_bytes()).digest()]
assert not source_drift, source_drift
scope = json.loads((evidence / 'authored-scope.json').read_text())
new_source_paths = [path for path in scope['authored_paths'] if Path(path).name.startswith(('photo_prompt_summer_', 'photo_prompt_visual_obligations_summer_'))]
assert len(new_source_paths) == 14
assert all(hashlib.sha256((pub / path).read_bytes()).hexdigest() == scope['copied_sha256'][path] for path in new_source_paths)
result = dict(status='pass', origin_main=origin['origin_main'],
    remote_top_level_asset_files_preserved=len(list(base.iterdir())) - 1,
    missing_baseline_semantic_ids=missing, existing_semantic_changes=changes,
    new_semantic_entries=len(new_rows) - len(old_rows),
    baseline_profiles=len(old_registry['profiles']), merged_profiles=len(new_registry['profiles']),
    baseline_bundles=len(old_data.get('candidate_bundles', [])), merged_bundles=len(new_data.get('candidate_bundles', [])),
    baseline_manifest_rows=len(old_manifest['sources']), merged_manifest_rows=len(new_manifest['sources']),
    raw_remote_source_drift=source_drift, summer_raw_source_files_preserved=14,
    boundary='All origin authored files and existing profile/bundle records are preserved; only seven reviewed semantic-equivalent paraphrase lists extend existing candidates.')
(evidence / 'both-intents-preservation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
