"""Seal the reviewed DATA successor and its exact, offline V21 parent source."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PHOTO = Path('skills/photo-prompt-image-generator')
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')
ASSETS = ROOT / ILLUSTRATION / 'assets'
V21_PROOF = Path('docs/research-evidence/photo-prompt/visual-profile-shards-20261005/V21-STORAGE-BINDING-PROOF.json')
SOURCE_COMMIT = 'fafa885a88e344e6f2709a457b557f5986b6fa08'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    source_commit = SOURCE_COMMIT
    parent = git('rev-parse', source_commit + '^').decode().strip()
    source_tree = git('rev-parse', source_commit + '^{tree}').decode().strip()
    old = json.loads((ROOT / V21_PROOF).read_bytes())
    parent_manifest = json.loads((ROOT / old['source_parent_manifest']).read_bytes())
    previous_members = {row['path']: row for row in parent_manifest['members']}
    validator = str(ILLUSTRATION / 'scripts/validate_illustration_assets.py')
    descriptor = str(ILLUSTRATION / 'assets/universal_scene_baseline_v2.json')
    hashes = dict(old['source_files'])
    hashes.update(old['active_semantic_shards'])
    hashes.update(old['active_visual_shards'])
    hashes.update({name: digest(git('show', f'{parent}:{name}')) for name in (validator, descriptor)})
    dependencies = {}
    for field in ('immutable_history', 'historical_dependencies', 'source_parent_files'):
        for name, sha in old[field].items():
            assert name not in dependencies or dependencies[name] == sha, name
            dependencies[name] = sha
    for name in (str(V21_PROOF), old['source_parent_manifest'],
                 str(ILLUSTRATION / 'assets/photo_regression_baseline_v21.json'),
                 str(ILLUSTRATION / 'assets/photo_regression_baseline_v21_pack.json')):
        dependencies[name] = digest(git('show', f'{parent}:{name}'))
    for name in hashes:
        dependencies.pop(name, None)
    members, dependency_rows = [], []
    for target, rows in ((hashes, members), (dependencies, dependency_rows)):
        for name, sha in sorted(target.items()):
            raw = git('show', f'{parent}:{name}')
            assert digest(raw) == sha, name
            tree_row = git('ls-tree', parent, '--', name).decode().strip().split()
            mode, blob = tree_row[0], tree_row[2]
            prior = previous_members.get(name)
            if rows is dependency_rows:
                kind, backing = 'retained_dependency', name
            elif (prior and prior['sha256'] == sha and prior['git_blob'] == blob
                  and digest((ROOT / prior['source_path']).read_bytes()) == sha):
                kind, backing = 'reuse_v20_parent_source', prior['source_path']
            elif '_index_shards/' in name:
                kind, backing = 'reuse_content_addressed_vector_shard', name
            else:
                kind = 'new_immutable_snapshot_same_git_blob'
                backing = str(HERE.relative_to(ROOT) / 'v21-parent-source-files' / name)
                output = ROOT / backing
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(raw)
                output.chmod(int(mode[-3:], 8))
            assert (ROOT / backing).is_file() and digest((ROOT / backing).read_bytes()) == sha, backing
            rows.append({'path': name, 'source_path': backing, 'kind': kind,
                         'git_commit': parent, 'git_path': name, 'git_blob': blob,
                         'mode': mode, 'bytes': len(raw), 'sha256': sha})
    counts = {kind: sum(row['kind'] == kind for row in members) for kind in sorted({row['kind'] for row in members})}
    manifest = {'schema': 'photo-v21-parent-source-manifest/v1', 'source_pin': parent,
                'member_count': len(members), 'dependency_count': len(dependency_rows),
                'total_member_bytes': sum(row['bytes'] for row in members),
                'counts': counts, 'previous_manifest_path': old['source_parent_manifest'],
                'previous_manifest_sha256': old['source_parent_manifest_sha256'],
                'members': members, 'dependencies': dependency_rows}
    write(HERE / 'V21-PARENT-SOURCE.json', manifest)
    previous_pack_raw = (ASSETS / 'photo_regression_baseline_v21_pack.json').read_bytes()
    current_pack_raw = (HERE / 'canonical-pack-current.json').read_bytes()
    previous_pack, current_pack = json.loads(previous_pack_raw)[0], json.loads(current_pack_raw)[0]
    reviewed = json.loads((HERE / 'REVIEWED-PACK-DELTA.json').read_bytes())
    current_sources = {name: digest((ROOT / name).read_bytes()) for name in old['source_files']}
    added = {str(PHOTO / 'assets' / name) for name in (
        'photo_prompt_ornament_structure_extension.json', 'photo_prompt_visual_obligations_ornament_structure.json')}
    current_sources.update({name: digest((ROOT / name).read_bytes()) for name in added})
    deltas = [{'path': name, 'previous': old['source_files'][name], 'current': current_sources[name]}
              for name in sorted(old['source_files']) if old['source_files'][name] != current_sources[name]]
    assert {row['path'] for row in deltas} == {str(PHOTO / 'scripts/prompt_generator.py'),
        *(str(PHOTO / 'assets' / name) for name in (
            'photo_prompt_tags.json', 'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'))}
    photo_assets = ROOT / PHOTO / 'assets'
    semantic = json.loads((photo_assets / 'photo_prompt_semantic_index.json').read_bytes())
    visual = json.loads((photo_assets / 'photo_prompt_visual_profile_index.json').read_bytes())
    def active(index):
        result = {}
        for row in index['shards']:
            name = str((photo_assets / row['path']).relative_to(ROOT))
            result[name] = digest((ROOT / name).read_bytes())
        return result
    proof = {'schema': 'photo-ornament-data-reviewed-pack-transition/v22',
             'source_commit': source_commit, 'source_tree': source_tree, 'source_parents': [parent],
             'previous_qualified_commit': parent,
             'previous_proof_path': str(V21_PROOF), 'previous_proof_sha256': digest((ROOT / V21_PROOF).read_bytes()),
             'previous_manifest_sha256': digest((ASSETS / 'photo_regression_baseline_v21.json').read_bytes()),
             'previous_pack_sha256': digest(previous_pack_raw), 'current_pack_sha256': digest(current_pack_raw),
             'previous_pack_id': previous_pack['pack_id'], 'current_pack_id': current_pack['pack_id'],
             'public_candidate_count': 64, 'reviewed_pack_delta': reviewed,
             'reviewed_source_deltas': deltas, 'added_source_files': sorted(added),
             'source_files': current_sources,
             'source_inventory_after': {p.name: digest(p.read_bytes()) for p in sorted(photo_assets.glob('*.json'))},
             'active_semantic_shards': active(semantic), 'active_visual_shards': active(visual),
             'retained_visual_shards': old['active_visual_shards'],
             'source_parent_manifest': str((HERE / 'V21-PARENT-SOURCE.json').relative_to(ROOT)),
             'source_parent_manifest_sha256': digest((HERE / 'V21-PARENT-SOURCE.json').read_bytes()),
             'source_parent_files': {row['source_path']: row['sha256'] for row in members},
             'immutable_history': old['immutable_history'], 'historical_dependencies': dependencies,
             'maintenance_path': 'docs/research-evidence/photo-prompt/extension-maintenance/ornament-structure-20261005-v1.json',
             'maintenance_sha256': digest((ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance/ornament-structure-20261005-v1.json').read_bytes()),
             'previous_validator_sha256': hashes[validator],
             'universal_v2_before_path': next(row['source_path'] for row in members if row['path'] == descriptor),
             'universal_v2_before_sha256': hashes[descriptor],
             'new_candidate_count': 66, 'new_profile_count': 66,
             'enriched_candidate_ids': ['hw_brocade_raised_motifs_1', 'hw_damask_tonal_pattern_1', 'pf_muqarnas_location'],
             'visual_entry_count': 1879, 'semantic_entry_count': 10082,
             'qualification_scope': ['authored DATA and registration', 'origin sharded storage preserved',
                 'exact reviewed metadata and optional-list changes', 'all 64 slot candidates and their order preserved',
                 'core controls embodiment negative and privacy preserved', 'all V1 through V21 history unchanged',
                 'no new image generation or pixel acceptance claim']}
    write(HERE / 'V22-ORNAMENT-BINDING-PROOF.json', proof)
    baseline = copy.deepcopy(json.loads((ASSETS / 'photo_regression_baseline_v21.json').read_bytes()))
    del baseline['visual_index_storage_transition']
    baseline.update(schema='photo_regression_baseline/v22', historical_baseline={
        'path': 'photo_regression_baseline_v21.json', 'schema': 'photo_regression_baseline/v21',
        'sha256': proof['previous_manifest_sha256']}, sha256=proof['current_pack_sha256'], pack_id=proof['current_pack_id'],
        change_scope='Add optional ornament DATA to the V21 sharded registry; bind only the reviewed six metadata leaves and two optional lists.',
        purpose='Qualify DATA and candidate-contract preservation separately from native pixels and user acceptance.')
    baseline['command'][-1] = '/tmp/subculture-illustration-photo-baseline-v22.json'
    baseline['ornament_data_transition'] = {'source_commit': source_commit, 'source_tree': source_tree,
        'previous_qualified_commit': parent, 'evidence_sha256': digest((HERE / 'V22-ORNAMENT-BINDING-PROOF.json').read_bytes()),
        'source_files': current_sources, 'active_visual_shards': proof['active_visual_shards'],
        'reviewed_pack_delta': reviewed}
    write(ASSETS / 'photo_regression_baseline_v22.json', baseline)
    (ASSETS / 'photo_regression_baseline_v22_pack.json').write_bytes(current_pack_raw)
    print(json.dumps({'source_commit': source_commit, 'parent': parent, 'members': len(members),
        'dependencies': len(dependency_rows), 'counts': counts,
        'parent_manifest_sha256': digest((HERE / 'V21-PARENT-SOURCE.json').read_bytes()),
        'proof_sha256': digest((HERE / 'V22-ORNAMENT-BINDING-PROOF.json').read_bytes())}, indent=2))


if __name__ == '__main__':
    main()
