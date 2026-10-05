"""Seal the nine-leaf DATA change and its exact, offline V22 parent source.

Run after the paired qualification export, with the immutable DATA-only commit.
All Git reads disable lazy fetching. No archive, provider, or network is used.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PHOTO = Path('skills/photo-prompt-image-generator')
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')
ASSETS = ROOT / ILLUSTRATION / 'assets'
PARENT = '900bf2efdd17fbc6a6ef3aa340f3526b1e01f223'
SOURCE_TREE = 'c43547aaeb90ee315dcaa32537be768d18b9ee72'
V22_PROOF = Path('docs/research-evidence/photo-prompt/gothic-sharded-main-merge-20261005/V22-ORNAMENT-BINDING-PROOF.json')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT,
        env=dict(os.environ, GIT_NO_LAZY_FETCH='1'))


def delta(before, after, pointer=''):
    if type(before) is not type(after):
        return [{'pointer': pointer, 'before': before, 'after': after}]
    if isinstance(before, dict) and before.keys() == after.keys():
        return [row for key in sorted(before) for row in delta(before[key], after[key], pointer + '/' + key)]
    if isinstance(before, list) and len(before) == len(after):
        return [row for i, (a, b) in enumerate(zip(before, after)) for row in delta(a, b, pointer + '/' + str(i))]
    return [] if before == after else [{'pointer': pointer, 'before': before, 'after': after}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--parent-only', action='store_true')
    args = parser.parse_args()
    commit = git('rev-parse', args.source_commit + '^{commit}').decode().strip()
    assert git('rev-parse', commit + '^').decode().strip() == PARENT
    assert git('rev-parse', commit + '^{tree}').decode().strip() == SOURCE_TREE
    old = json.loads(git('show', f'{PARENT}:{V22_PROOF}'))
    assert digest(git('show', f'{PARENT}:{V22_PROOF}')) == '711a95d51bbfba26b10dba0b41bb98daf559698b23469291312e087cb2ca783d'
    previous_manifest = json.loads((ROOT / old['source_parent_manifest']).read_bytes())
    previous_members = {row['path']: row for row in previous_manifest['members']}
    validator = str(ILLUSTRATION / 'scripts/validate_illustration_assets.py')
    descriptor = str(ILLUSTRATION / 'assets/universal_scene_baseline_v2.json')
    hashes = old['source_files'] | old['active_semantic_shards'] | old['active_visual_shards']
    hashes.update({name: digest(git('show', f'{PARENT}:{name}')) for name in (validator, descriptor)})
    dependencies = {}
    for field in ('immutable_history', 'historical_dependencies', 'source_parent_files', 'retained_visual_shards'):
        for name, sha in old[field].items():
            assert name not in dependencies or dependencies[name] == sha, name
            dependencies[name] = sha
    for name in (str(V22_PROOF), old['source_parent_manifest'], old['maintenance_path'],
                 str(ILLUSTRATION / 'assets/photo_regression_baseline_v22.json'),
                 str(ILLUSTRATION / 'assets/photo_regression_baseline_v22_pack.json')):
        dependencies[name] = digest(git('show', f'{PARENT}:{name}'))
    for name in hashes:
        dependencies.pop(name, None)
    members, dependency_rows = [], []
    for target, rows in ((hashes, members), (dependencies, dependency_rows)):
        for name, sha in sorted(target.items()):
            raw = git('show', f'{PARENT}:{name}')
            assert digest(raw) == sha, name
            tree_row = git('ls-tree', PARENT, '--', name).decode().strip().split()
            mode, blob = tree_row[0], tree_row[2]
            prior = previous_members.get(name)
            if rows is dependency_rows:
                kind, backing = 'retained_dependency', name
            elif prior and prior['sha256'] == sha and prior['git_blob'] == blob:
                kind, backing = 'reuse_v21_parent_source', prior['source_path']
            elif '_index_shards/' in name:
                kind, backing = 'reuse_retained_vector_shard', name
            else:
                kind = 'new_immutable_snapshot_same_git_blob'
                backing = str(HERE.relative_to(ROOT) / 'v22-parent-source-files' / name)
                output = ROOT / backing
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(raw)
                output.chmod(int(mode[-3:], 8))
            assert (ROOT / backing).is_file() and digest((ROOT / backing).read_bytes()) == sha, backing
            rows.append({'path': name, 'source_path': backing, 'kind': kind,
                'git_commit': PARENT, 'git_path': name, 'git_blob': blob,
                'mode': mode, 'bytes': len(raw), 'sha256': sha})
    counts = {kind: sum(row['kind'] == kind for row in members) for kind in sorted({row['kind'] for row in members})}
    assert len(members) == 168 and len(dependency_rows) == 261
    assert counts == {'reuse_v21_parent_source': 129, 'reuse_retained_vector_shard': 31,
                      'new_immutable_snapshot_same_git_blob': 8}
    manifest = {'schema': 'photo-v22-parent-source-manifest/v1', 'source_pin': PARENT,
        'member_count': len(members), 'dependency_count': len(dependency_rows),
        'total_member_bytes': sum(row['bytes'] for row in members), 'counts': counts,
        'previous_manifest_path': old['source_parent_manifest'],
        'previous_manifest_sha256': old['source_parent_manifest_sha256'],
        'members': members, 'dependencies': dependency_rows}
    write(HERE / 'V22-PARENT-SOURCE.json', manifest)
    if args.parent_only:
        print(digest((HERE / 'V22-PARENT-SOURCE.json').read_bytes()))
        return
    current_sources = {name: digest(git('show', f'{commit}:{name}')) for name in old['source_files']}
    source_deltas = [{'path': name, 'previous': old['source_files'][name], 'current': current_sources[name]}
                     for name in sorted(current_sources) if old['source_files'][name] != current_sources[name]]
    expected = {str(PHOTO / 'assets' / name) for name in (
        'photo_prompt_ornament_structure_extension.json', 'photo_prompt_visual_obligations_ornament_structure.json',
        'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json')}
    assert {row['path'] for row in source_deltas} == expected
    leaf_deltas = []
    for name in sorted(expected):
        if name.endswith(('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json')):
            continue
        before = json.loads(git('show', f'{PARENT}:{name}'))
        after = json.loads(git('show', f'{commit}:{name}'))
        leaf_deltas += [dict(file=name, **row) for row in delta(before, after)]
    assert len(leaf_deltas) == 9 and all(isinstance(row['before'], str) and isinstance(row['after'], str) for row in leaf_deltas)
    def active(name):
        index = json.loads(git('show', f'{commit}:{PHOTO / "assets" / name}'))
        return {str(PHOTO / 'assets' / row['path']): row['sha256'] for row in index['shards']}
    semantic = active('photo_prompt_semantic_index.json')
    visual = active('photo_prompt_visual_profile_index.json')
    assert visual == old['active_visual_shards']
    assert sorted(semantic.values()) == sorted(old['active_semantic_shards'].values())
    paths = git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
    assert len(paths) == 20 and set(paths) == expected | set(semantic)
    exact_files = {name: digest(git('show', f'{commit}:{name}')) for name in paths}
    previous_raw = (ASSETS / 'photo_regression_baseline_v22_pack.json').read_bytes()
    current_raw = (ASSETS / 'photo_regression_baseline_v23_pack.json').read_bytes()
    assert digest(previous_raw) == '41bb856b70185e9a797939b60379b3888a35078c759b0640061f906172a9fc87'
    assert digest(current_raw) == 'c01e698c9d356073dc53031bebc440194b6537edcce88c01b7aaf6bda4d95037'
    previous, current = json.loads(previous_raw)[0], json.loads(current_raw)[0]
    pack_delta = delta(previous, current)
    assert {row['pointer'] for row in pack_delta} == {'/pack_id', '/provenance/tags_hash'}
    reviewed = {'bindings': [{'path': row['pointer'][1:], 'previous': row['before'], 'current': row['after']} for row in pack_delta],
        'optional_blocks': [], 'all_other_pack_fields_exactly_equal': True, 'slot_candidates_and_order_unchanged': True}
    qualification_path = HERE / 'QUALIFICATION.json'
    qualification = json.loads(qualification_path.read_bytes())
    assert qualification['source_commit'] == commit
    assert all(digest((ROOT / name).read_bytes()) == sha for name, sha in qualification['files'].items())
    proof = {'schema': 'photo-lobe-boundary-two-binding-transition/v23',
        'source_commit': commit, 'source_tree': SOURCE_TREE, 'source_parents': [PARENT], 'previous_qualified_commit': PARENT,
        'previous_proof_path': str(V22_PROOF), 'previous_proof_sha256': digest((ROOT / V22_PROOF).read_bytes()),
        'previous_manifest_sha256': digest((ASSETS / 'photo_regression_baseline_v22.json').read_bytes()),
        'previous_pack_sha256': digest(previous_raw), 'current_pack_sha256': digest(current_raw),
        'previous_pack_id': previous['pack_id'], 'current_pack_id': current['pack_id'], 'public_candidate_count': 64,
        'reviewed_pack_delta': reviewed, 'reviewed_source_deltas': source_deltas,
        'reviewed_source_leaf_deltas': leaf_deltas, 'exact_data_paths': sorted(paths), 'exact_data_files': exact_files,
        'candidate_20_file_seal_sha256': '8bf0dfe263cd9dace49de1f54b4744ab915e56dd49658511f2ef879dc6033f75',
        'source_files': current_sources,
        'source_inventory_after': {p.name: digest(p.read_bytes()) for p in sorted((ROOT / PHOTO / 'assets').glob('*.json'))},
        'active_semantic_shards': semantic, 'active_visual_shards': visual,
        'retained_semantic_shards': old['active_semantic_shards'], 'retained_visual_shards': old['retained_visual_shards'],
        'source_parent_manifest': str((HERE / 'V22-PARENT-SOURCE.json').relative_to(ROOT)),
        'source_parent_manifest_sha256': digest((HERE / 'V22-PARENT-SOURCE.json').read_bytes()),
        'source_parent_files': {row['source_path']: row['sha256'] for row in members},
        'immutable_history': old['immutable_history'], 'historical_dependencies': dependencies,
        'maintenance_path': old['maintenance_path'], 'maintenance_sha256': old['maintenance_sha256'],
        'previous_validator_sha256': hashes[validator],
        'universal_v2_before_path': next(row['source_path'] for row in members if row['path'] == descriptor),
        'universal_v2_before_sha256': hashes[descriptor], 'visual_entry_count': 1879, 'semantic_entry_count': 10082,
        'qualification_path': str(qualification_path.relative_to(ROOT)), 'qualification_sha256': digest(qualification_path.read_bytes()),
        'qualification_scope': ['nine authored contrast/rejection string leaves', 'frozen pack changes only tags_hash and pack_id',
            'four synthetic natural pairs and normal controls', 'three natural visual-candidate order changes disclosed',
            'all V1 through V22 history unchanged', 'no adoption, final prompt, image, or pixel acceptance claim']}
    write(HERE / 'V23-LOBE-BINDING-PROOF.json', proof)
    baseline = copy.deepcopy(json.loads((ASSETS / 'photo_regression_baseline_v22.json').read_bytes()))
    del baseline['ornament_data_transition']
    baseline.update(schema='photo_regression_baseline/v23', historical_baseline={
        'path': 'photo_regression_baseline_v22.json', 'schema': 'photo_regression_baseline/v22',
        'sha256': proof['previous_manifest_sha256']}, sha256=proof['current_pack_sha256'], pack_id=proof['current_pack_id'],
        change_scope='Correct nine lobe contrast/rejection DATA leaves; the frozen pack changes only tags_hash and pack_id.',
        purpose='Preserve the frozen candidate contract and disclose natural presentation-order changes separately from adoption or pixels.')
    baseline['command'][-1] = '/tmp/subculture-illustration-photo-baseline-v23.json'
    baseline['lobe_boundary_transition'] = {'source_commit': commit, 'source_tree': SOURCE_TREE,
        'previous_qualified_commit': PARENT, 'evidence_sha256': digest((HERE / 'V23-LOBE-BINDING-PROOF.json').read_bytes()),
        'source_files': current_sources, 'reviewed_pack_delta': reviewed}
    write(ASSETS / 'photo_regression_baseline_v23.json', baseline)
    print(json.dumps({'source_commit': commit, 'proof_sha256': digest((HERE / 'V23-LOBE-BINDING-PROOF.json').read_bytes()),
        'parent_manifest_sha256': digest((HERE / 'V22-PARENT-SOURCE.json').read_bytes()), 'snapshot_files': 8,
        'snapshot_bytes': sum(row['bytes'] for row in members if row['kind'] == 'new_immutable_snapshot_same_git_blob')}, indent=2))


if __name__ == '__main__':
    main()
