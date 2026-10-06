"""Independent read-only checks; write only the review result beside this script."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path('/workspace/scratch/ce8f20680f5a/image-prompt-lobe-after900')
OUT = Path(__file__).resolve().parent
BASE = '900bf2efdd17fbc6a6ef3aa340f3526b1e01f223'
SOURCE = '9654fc13070baa1c8d4c3b31fbf80972234f85b9'
EVIDENCE = Path('docs/research-evidence/photo-prompt/lobe-boundary-integration-20261005')
ILL = Path('skills/subculture-illustration-image-generator')
PHOTO = Path('skills/photo-prompt-image-generator')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT,
                                   env=dict(os.environ, GIT_NO_LAZY_FETCH='1'))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_bytes())


def diff(before, after, pointer=''):
    if type(before) is type(after):
        if isinstance(before, dict) and before.keys() == after.keys():
            return [row for key in sorted(before) for row in diff(before[key], after[key], pointer + '/' + key)]
        if isinstance(before, list) and len(before) == len(after):
            return [row for i, (a, b) in enumerate(zip(before, after)) for row in diff(a, b, pointer + '/' + str(i))]
    return [] if before == after else [{'pointer': pointer, 'before': before, 'after': after}]


def tree(commit):
    result = {}
    for row in git('ls-tree', '-r', '-z', commit).split(b'\0'):
        if row:
            header, name = row.split(b'\t')
            mode, kind, blob = header.decode().split()
            result[name.decode()] = (mode, blob)
    return result


def functions(raw):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(raw).body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def main():
    assert git('rev-parse', 'HEAD').decode().strip() == SOURCE
    assert git('rev-parse', SOURCE + '^').decode().strip() == BASE
    assert git('rev-parse', SOURCE + '^{tree}').decode().strip() == 'c43547aaeb90ee315dcaa32537be768d18b9ee72'
    parent_tree, source_tree = tree(BASE), tree(SOURCE)
    changed = sorted(name for name in parent_tree.keys() | source_tree.keys()
                     if parent_tree.get(name) != source_tree.get(name))
    proof = load(EVIDENCE / 'V23-LOBE-BINDING-PROOF.json')
    assert proof['source_commit'] == SOURCE and proof['source_parents'] == [BASE]
    assert len(changed) == 20 and changed == sorted(proof['exact_data_paths'])
    seal_path = OUT.parent / 'lobe-boundary-candidate/candidate-20-file-seal.json'
    assert sha(seal_path.read_bytes()) == '8bf0dfe263cd9dace49de1f54b4744ab915e56dd49658511f2ef879dc6033f75'
    candidate_seal = json.loads(seal_path.read_bytes())
    for row in candidate_seal['files']:
        raw = (ROOT / row['path']).read_bytes()
        assert sha(raw) == row['sha256'] == proof['exact_data_files'][row['path']]
        assert len(raw) == row['bytes']
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == source_tree[row['path']][1]

    manifest = load(EVIDENCE / 'V22-PARENT-SOURCE.json')
    assert len(manifest['members']) == 168 and len(manifest['dependencies']) == 261
    destinations = set()
    for row in manifest['members'] + manifest['dependencies']:
        assert row['path'] not in destinations
        destinations.add(row['path'])
        assert row['git_commit'] == BASE and row['git_path'] == row['path']
        assert (row['mode'], row['git_blob']) == parent_tree[row['path']]
        path = ROOT / row['source_path']
        assert not path.is_symlink()
        raw = path.read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == row['git_blob']
    source_map = {row['path']: row['source_path'] for row in manifest['members']}
    leaf_deltas = []
    for name in sorted(changed):
        if Path(name).name in ('photo_prompt_ornament_structure_extension.json',
                               'photo_prompt_visual_obligations_ornament_structure.json'):
            leaf_deltas += [dict(file=name, **row) for row in diff(load(source_map[name]), load(name))]
    assert len(leaf_deltas) == 9 and leaf_deltas == proof['reviewed_source_leaf_deltas']
    assert all(isinstance(row['before'], str) and isinstance(row['after'], str) for row in leaf_deltas)

    vectors = {}
    for filename in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
        path = str(PHOTO / 'assets' / filename)
        before, after = load(source_map[path]), load(path)
        assert len(before['shards']) == len(after['shards']) == 16
        count, ids = 0, set()
        for old, new in zip(before['shards'], after['shards']):
            assert old['sha256'] == new['sha256']
            old_raw = (ROOT / PHOTO / 'assets' / old['path']).read_bytes()
            raw = (ROOT / PHOTO / 'assets' / new['path']).read_bytes()
            assert raw == old_raw and sha(raw) == new['sha256']
            entries = json.loads(raw)['entries']
            assert len(entries) == new['entry_count'] and not (ids & set(entries))
            ids.update(entries)
            assert all(isinstance(row['vector'], list) and len(row['vector']) == after['embedding_dimensions']
                       and all(type(value) in (int, float) for value in row['vector']) for row in entries.values())
            count += len(entries)
        assert count == before['entry_count'] == after['entry_count']
        vectors[filename] = count
    assert sum(vectors.values()) == 11961

    old_pack_path = ILL / 'assets/photo_regression_baseline_v22_pack.json'
    new_pack_path = ILL / 'assets/photo_regression_baseline_v23_pack.json'
    assert sha((ROOT / old_pack_path).read_bytes()) == '41bb856b70185e9a797939b60379b3888a35078c759b0640061f906172a9fc87'
    assert sha((ROOT / new_pack_path).read_bytes()) == 'c01e698c9d356073dc53031bebc440194b6537edcce88c01b7aaf6bda4d95037'
    pack_delta = diff(load(old_pack_path), load(new_pack_path))
    assert {row['pointer'] for row in pack_delta} == {'/0/pack_id', '/0/provenance/tags_hash'}
    assert len(pack_delta) == 2

    history = []
    for path, (_, blob) in parent_tree.items():
        m = re.match(r'^skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v(\d+)(?:[_.])', path)
        if m and int(m[1]) <= 22:
            raw = (ROOT / path).read_bytes()
            assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == blob
            history.append(path)
    validator_path = str(ILL / 'scripts/validate_illustration_assets.py')
    old_validator = git('show', BASE + ':' + validator_path)
    new_validator = (ROOT / validator_path).read_bytes()
    old_functions, new_functions = functions(old_validator), functions(new_validator)
    changed_functions = sorted(name for name in old_functions if old_functions[name] != new_functions.get(name))
    assert changed_functions == ['validate_photo_regression_baseline']
    new_names = sorted(set(new_functions) - set(old_functions))
    assert new_names == ['_validate_v23_lobe_boundary_successor']
    old_dispatch = next(node for node in ast.parse(old_validator).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'validate_photo_regression_baseline')
    new_dispatch = next(node for node in ast.parse(new_validator).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'validate_photo_regression_baseline')
    new_dispatch.body = [node for node in new_dispatch.body if not (
        isinstance(node, ast.If) and ast.unparse(node.test) == 'baseline_version == 23')]
    for node in ast.walk(new_dispatch):
        if isinstance(node, (ast.Set, ast.Tuple)):
            node.elts = [value for value in node.elts if not (
                isinstance(value, ast.Constant) and value.value == 23)]
    assert ast.dump(new_dispatch, include_attributes=False) == ast.dump(old_dispatch, include_attributes=False)
    helpers = 'tests/photo_prompt_fixtures.py'
    old_helpers, new_helpers = functions(git('show', BASE + ':' + helpers)), functions((ROOT / helpers).read_bytes())
    assert all(new_helpers.get(name) == body for name, body in old_helpers.items())
    old_tests = ast.parse(git('show', BASE + ':tests/test_photo_ornament_boundary_history.py'))
    new_tests = ast.parse((ROOT / 'tests/test_photo_ornament_boundary_history.py').read_bytes())
    def test_methods(module):
        return {node.name: ast.dump(node, include_attributes=False) for node in ast.walk(module)
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
    assert test_methods(old_tests) == test_methods(new_tests)
    descriptor_path = str(ILL / 'assets/universal_scene_baseline_v2.json')
    old_descriptor = git('show', BASE + ':' + descriptor_path)
    assert old_descriptor.count(sha(old_validator).encode()) == 1
    assert (ROOT / descriptor_path).read_bytes() == old_descriptor.replace(sha(old_validator).encode(), sha(new_validator).encode(), 1)

    names = set(git('diff', '--name-only', 'HEAD').decode().splitlines())
    names.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    inventory = {name: {'sha256': sha((ROOT / name).read_bytes()), 'bytes': (ROOT / name).stat().st_size}
                 for name in sorted(names)}
    result = {'status': 'pass', 'source_commit': SOURCE, 'parent_commit': BASE,
              'integration_file_count': len(inventory), 'files': inventory,
              'exact_data_paths': changed, 'source_string_leaves': len(leaf_deltas),
              'source_deltas': leaf_deltas, 'archive_members': 168, 'archive_dependencies': 261,
              'all_429_archived_payloads_match_parent_git_tree': True,
              'byte_identical_active_shards': 32, 'vector_counts': vectors,
              'vector_arrays_unchanged': True, 'v1_through_v22_unchanged_assets': history,
              'historical_validator_helpers_unchanged': True, 'historical_fixture_helpers_unchanged': True,
              'dispatcher_only_registers_v23_without_relaxing_historical_numeric_checks': True,
              'retained_v22_test_methods': sorted(test_methods(old_tests)),
              'pack_delta': pack_delta, 'descriptor_only_validator_hash_changed': True,
              'proof_sha256': sha((ROOT / EVIDENCE / 'V23-LOBE-BINDING-PROOF.json').read_bytes())}
    (OUT / 'static-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in ('files', 'source_deltas', 'exact_data_paths', 'v1_through_v22_unchanged_assets', 'retained_v22_test_methods', 'pack_delta')}, indent=2))


if __name__ == '__main__':
    main()
