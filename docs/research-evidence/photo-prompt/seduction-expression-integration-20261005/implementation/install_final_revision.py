"""Install only reviewed paths after revalidating primary-workspace hashes."""
from pathlib import Path
import hashlib
import json
import os
import shutil

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
SOURCE = Path('/Users/chasoik/.codex/worktrees/seduction-paraphrases/image-prompt/.integration-final')
HERE = Path(__file__).resolve().parent
ASSET_DIR = Path('skills/photo-prompt-image-generator/assets')

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

previous = read(HERE / 'PRIMARY-INSTALLATION-FINAL.json')
expected = {row['path']: row['after_sha256'] for row in previous['files']}
baseline = {row['path']: row['sha256'] for row in read(HERE.parent / 'baseline-inputs.json')['files']}
applied = read(HERE / 'APPLIED-CHANGES-FINAL.json')
ready = read(HERE / 'FINAL-REVISION-READY.json')
index = read(SOURCE / ASSET_DIR / 'photo_prompt_semantic_index.json')
paths = [str(ASSET_DIR / row['path']) for row in index['shards']]
paths += [str(ASSET_DIR / name) for name in applied['authored_files']]
paths += [applied['registration_file'],
          'tests/fixtures/photo_prompt/seduction_expression_integration_baseline.json',
          'tests/test_photo_seduction_expression_integration.py',
          str(ASSET_DIR / 'photo_prompt_visual_profile_index.json'),
          str(ASSET_DIR / 'photo_prompt_semantic_index.json')]
paths += ['tests/photo_prompt_fixtures.py',
          'tests/test_photo_krummholz_korean_alias_data_cleanup.py',
          'tests/test_photo_protostar_korean_alias_data_cleanup.py',
          'tests/test_photo_shelf_return_korean_state_data_cleanup.py',
          'tests/test_photo_liminal_active_use_korean_data_cleanup.py',
          'tests/test_photo_pose_vocabulary_semantics.py',
          'tests/test_photo_scene_data_cleanup.py',
          'tests/fixtures/photo_prompt/seduction_expression_scope_delta.json',
          'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py',
          'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v13.json']
assert len(paths) == len(set(paths))
for name in applied['authored_files']:
    assert sha(SOURCE / ASSET_DIR / name) == applied['source_hashes_after'][name]
    assert sha(SOURCE / ASSET_DIR / name) == ready['asset_sha256'][name]

checks = []
for name in paths:
    target, source = PRIMARY / name, SOURCE / name
    assert source.is_file(), name
    before = sha(target)
    old = expected.get(name, baseline.get(name))
    if name == 'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py':
        original = source.read_bytes()
        for revised, prior in [
            (b'version for version in (13, 12, 11, 10, 9, 8, 7)', b'version for version in (12, 11, 10, 9, 8, 7)'),
            (b'baseline_version in {6, 7, 8, 9, 10, 11, 12, 13}', b'baseline_version in {6, 7, 8, 9, 10, 11, 12}'),
        ]:
            assert original.count(revised) == 1
            original = original.replace(revised, prior)
        old = hashlib.sha256(original).hexdigest()
        (HERE / 'illustration-validator-before-v13.py.txt').write_bytes(original)
    new = sha(source)
    assert before == old or (old is None and before == new), f'Unexpected primary drift: {name}'
    checks.append({'path': name, 'before_sha256': before, 'expected_before_sha256': old,
                   'after_sha256': new, 'changed': before != new})

compatibility = []
for name in applied['authored_files']:
    before = read(PRIMARY / ASSET_DIR / name)
    after = read(SOURCE / ASSET_DIR / name)
    before.pop('maintenance_ref', None)
    after.pop('maintenance_ref', None)
    compatibility.append({'path': name, 'qualification_selected_meanings_and_v2_authored_data_unchanged': before == after})
assert all(row['qualification_selected_meanings_and_v2_authored_data_unchanged'] for row in compatibility)
(HERE / 'FINAL-V3-COMPATIBILITY.json').write_text(json.dumps({
    'final_revision': 'final-v3', 'compared_primary_revision': 'final-v2',
    'candidate_dictionary_sha256': ready['candidate_dictionary_hash'],
    'source_checks': compatibility, 'native_image_calls': 0,
    'boundary': 'Only maintenance references changed between these two authored-data revisions. Final-v2 retrieval replay remains valid for the identical final-v3 candidate dictionary. Preserved native images were generated with qualification-v1.'
}, ensure_ascii=False, indent=2) + '\n')

for row in checks:
    if not row['changed']:
        continue
    source, target = SOURCE / row['path'], PRIMARY / row['path']
    assert sha(target) == row['before_sha256'], f'Concurrent change: {row["path"]}'
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.seduction-final-install.tmp')
    assert not temporary.exists(), str(temporary)
    shutil.copy2(source, temporary)
    assert sha(temporary) == row['after_sha256']
    os.replace(temporary, target)
    assert sha(target) == row['after_sha256']

payload = {'status': 'installed', 'revision': 'final-v3', 'primary': str(PRIMARY),
           'source': str(SOURCE), 'files': checks,
           'reviewed_path_count': len(checks), 'changed_path_count': sum(row['changed'] for row in checks),
           'unrelated_authored_inputs_preserved': True,
           'old_unreferenced_shards_deleted': False, 'commit_performed': False, 'push_performed': False,
           'native_images_revision': 'qualification-v1; immutable source snapshot retained in qualification/frozen-source-v1'}
(HERE / 'PRIMARY-INSTALLATION-FINAL.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: value for key, value in payload.items() if key != 'files'}, ensure_ascii=False))
