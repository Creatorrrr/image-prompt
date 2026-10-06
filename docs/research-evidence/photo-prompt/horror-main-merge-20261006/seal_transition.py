"""Seal additive horror DATA and retain exact runnable V30 source bytes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PHOTO = Path('skills/photo-prompt-image-generator')
ILL = Path('skills/subculture-illustration-image-generator')
PARENT = 'c72abf1d7f05895b7546b07bcab9f8f39dbd3173'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def compare(left, right, path='', differences=None):
    if differences is None:
        differences = []
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(left.keys() | right.keys()):
            child = path + '/' + key
            if key not in left or key not in right:
                differences.append({'path': child, 'old': left.get(key), 'new': right.get(key)})
            else:
                compare(left[key], right[key], child, differences)
    elif left != right:
        differences.append({'path': path, 'old': left, 'new': right})
    return differences

def main():
    previous_dir = ROOT / 'docs/research-evidence/photo-prompt/water-main-merge-20261006'
    original = json.loads((previous_dir / 'V29-PARENT-SOURCE.json').read_bytes())
    previous = json.loads((previous_dir / 'V30-WATER-MAIN-PROOF.json').read_bytes())
    paths = {row['path'] for row in original['members']}
    paths.update(row['source_path'] for row in original['members'])
    paths.update(previous['source_files_after'])
    paths.update(previous['active_shards_after'])
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT / ILL / 'assets').glob('photo_regression_baseline_v*.json') if '_v31' not in p.name)
    paths.update([str((previous_dir / 'V30-WATER-MAIN-PROOF.json').relative_to(ROOT)),
                  str((previous_dir / 'V29-PARENT-SOURCE.json').relative_to(ROOT)),
                  'tests/photo_prompt_fixtures.py'])
    objects = {}
    for row in subprocess.check_output(['git', 'ls-tree', '-r', '-z', PARENT], cwd=ROOT).split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        objects[name.decode()] = (mode, blob)
    missing = sorted(paths - objects.keys())
    if missing:
        raise RuntimeError('Parent dependencies missing from Git: ' + repr(missing))
    members = []
    proc = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for name in sorted(paths):
            mode, blob = objects[name]
            proc.stdin.write((blob + '\n').encode()); proc.stdin.flush()
            header = proc.stdout.readline().decode().split()
            assert header[0] == blob and header[1] == 'blob'
            raw = proc.stdout.read(int(header[2])); assert proc.stdout.read(1) == b'\n'
            current = ROOT / name
            archived = HERE / 'v30-parent-source-files' / name
            source_path = name
            forced = name in {'tests/photo_prompt_fixtures.py', str(ILL / 'scripts/validate_illustration_assets.py'), str(ILL / 'assets/universal_scene_baseline_v2.json')}
            if forced or not current.is_file() or current.read_bytes() != raw:
                archived.parent.mkdir(parents=True, exist_ok=True)
                if archived.exists():
                    assert archived.read_bytes() == raw
                else:
                    archived.write_bytes(raw)
                archived.chmod(int(mode[-3:], 8))
                source_path = str(archived.relative_to(ROOT))
            members.append({'path': name, 'source_path': source_path, 'sha256': digest(raw),
                            'git_blob': blob, 'bytes': len(raw), 'mode': mode})
    finally:
        proc.stdin.close(); proc.wait()
    parent = {'schema': 'photo-v30-parent-source-manifest/v1', 'source_pin': PARENT,
              'source_tree': subprocess.check_output(['git', 'rev-parse', PARENT + '^{tree}'], cwd=ROOT, text=True).strip(),
              'member_count': len(members), 'total_member_bytes': sum(row['bytes'] for row in members), 'members': members}
    parent_path = HERE / 'V30-PARENT-SOURCE.json'; save(parent_path, parent)
    assets = ROOT / PHOTO / 'assets'
    source_files = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in sorted((ROOT / PHOTO).rglob('*'))
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.json', '.py', '.md') and '_index_shards' not in str(p.parent)}
    # Qualified support changes must also preserve old retained test modules.
    # Files containing this proof's digest are always archived, never self-hashed.
    support_files = {row['path']: digest((ROOT / row['path']).read_bytes()) for row in members
                     if row['path'].startswith('tests/') and row['path'] != 'tests/photo_prompt_fixtures.py'
                     and (ROOT / row['path']).is_file() and digest((ROOT / row['path']).read_bytes()) != row['sha256']}
    source_files.update(support_files)
    inventory = {p.name: digest(p.read_bytes()) for p in sorted(assets.glob('*.json'))}
    active = {}
    for name in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
        for row in json.loads((assets / name).read_bytes())['shards']:
            p = assets / row['path']; assert digest(p.read_bytes()) == row['sha256']
            active[str(p.relative_to(ROOT))] = row['sha256']
    illustration_assets = ROOT / ILL / 'assets'
    old_raw = (illustration_assets / 'photo_regression_baseline_v30_pack.json').read_bytes()
    raw = (ROOT / '.codex-artifacts/horror-main-current-pack.json').read_bytes()
    old, new = json.loads(old_raw)[0], json.loads(raw)[0]
    differences = compare(old, new)
    unchanged = ('authorial_core', 'creative_controls', 'embodiment_preflight', 'authorial_composition', 'negative_en')
    assert all(old[key] == new[key] for key in unchanged)
    candidate_changes = {slot: compare(old['slots'][slot]['candidates'], new['slots'][slot]['candidates'])
                         for slot in old['slots'] if old['slots'][slot]['candidates'] != new['slots'][slot]['candidates']}
    adoption = json.loads((HERE / 'AUTHORED-MERGE.json').read_bytes())
    proof = {'schema': 'photo-horror-main-transition/v31', 'previous_qualified_commit': PARENT,
             'previous_qualified_tree': parent['source_tree'], 'parent_manifest': str(parent_path.relative_to(ROOT)),
             'parent_manifest_sha256': digest(parent_path.read_bytes()), 'parent_member_count': len(members),
             'previous_manifest_sha256': digest((illustration_assets / 'photo_regression_baseline_v30.json').read_bytes()),
             'previous_validator_sha256': next(row['sha256'] for row in members if row['path'] == str(ILL / 'scripts/validate_illustration_assets.py')),
             'previous_universal_descriptor_sha256': next(row['sha256'] for row in members if row['path'] == str(ILL / 'assets/universal_scene_baseline_v2.json')),
             'previous_pack_sha256': digest(old_raw), 'previous_pack_id': old['pack_id'],
             'current_pack_sha256': digest(raw), 'current_pack_id': new['pack_id'],
             'reviewed_pack_delta': differences, 'reviewed_pack_delta_count': len(differences),
             'candidate_changes': candidate_changes, 'preserved_contract_keys': list(unchanged),
             'horror_source_sha256': adoption['horror_source_sha256'], 'horror_candidates': 155, 'horror_profiles': 155, 'horror_bundles': 11,
             'source_files_after': source_files, 'qualified_support_files_after': support_files,
             'source_inventory_after': inventory, 'active_shards_after': active,
             'frozen_inputs': json.loads((illustration_assets / 'photo_regression_baseline_v30.json').read_bytes())['frozen_inputs'],
             'native_image_calls_during_merge': 0,
             'historical_horror_render_generation': 'd947d6b68f2a19b4a65f2668c87dee3fd4fcebb69b68357bd2dc98ab8c13eb10',
             'proof_boundary': 'Merged source/retrieval integrity. Historical native images retain their original generation and A/B pass, C fail; no rerender or user acceptance is inferred.'}
    proof_path = HERE / 'V31-HORROR-MAIN-PROOF.json'; save(proof_path, proof)
    save(HERE / 'PACK-DELTA.json', {'count': len(differences), 'differences': differences, 'candidate_changes': candidate_changes})
    baseline = json.loads((illustration_assets / 'photo_regression_baseline_v30.json').read_bytes())
    baseline.update(schema='photo_regression_baseline/v31', historical_baseline={
        'path': 'photo_regression_baseline_v30.json', 'schema': 'photo_regression_baseline/v30', 'sha256': proof['previous_manifest_sha256']},
        change_scope='Add horror DATA to current main, retain remote water/runtime changes and byte-exact V1-V30 history.',
        sha256=proof['current_pack_sha256'], pack_id=new['pack_id'],
        purpose='Qualify the merged authored corpus and current boundary; preserve independent original pixel and user-decision records.')
    baseline['command'][-1] = '/tmp/subculture-illustration-photo-baseline-v31.json'
    baseline.pop('water_main_transition')
    baseline['horror_main_transition'] = {'evidence_path': str(proof_path.relative_to(ROOT)), 'evidence_sha256': digest(proof_path.read_bytes()),
                                         'previous_qualified_commit': PARENT, 'parent_manifest_sha256': proof['parent_manifest_sha256']}
    save(illustration_assets / 'photo_regression_baseline_v31.json', baseline)
    (illustration_assets / 'photo_regression_baseline_v31_pack.json').write_bytes(raw)
    for name in ('tests/photo_prompt_fixtures.py', str(ILL / 'scripts/validate_illustration_assets.py')):
        path = ROOT / name
        text = path.read_text()
        for key, value in [('PHOTO_V31_HORROR_PROOF_SHA256', digest(proof_path.read_bytes())),
                           ('V31_HORROR_PROOF_SHA256', digest(proof_path.read_bytes())),
                           ('PHOTO_V31_PARENT_MANIFEST_SHA256', proof['parent_manifest_sha256']),
                           ('V30_PARENT_SOURCE_SHA256', proof['parent_manifest_sha256'])]:
            text = re.sub(r'(?m)^(' + key + r' = [\"\x27])[^\"\x27]+([\"\x27])$',
                          lambda match: match.group(1) + value + match.group(2), text)
        path.write_text(text)
    descriptor = ROOT / ILL / 'assets/universal_scene_baseline_v2.json'
    original_descriptor = (ROOT / next(row['source_path'] for row in members if row['path'] == str(ILL / 'assets/universal_scene_baseline_v2.json'))).read_bytes()
    assert original_descriptor.count(proof['previous_validator_sha256'].encode()) == 1
    descriptor.write_bytes(original_descriptor.replace(proof['previous_validator_sha256'].encode(), digest((ROOT / ILL / 'scripts/validate_illustration_assets.py').read_bytes()).encode(), 1))
    print(json.dumps({'parent_members': len(members), 'delta_count': len(differences), 'candidate_changes': list(candidate_changes),
                      'proof_sha256': digest(proof_path.read_bytes()), 'parent_manifest_sha256': proof['parent_manifest_sha256']}))

if __name__ == '__main__':
    main()
