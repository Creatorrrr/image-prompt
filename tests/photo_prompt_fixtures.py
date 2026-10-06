"""Authored, candidate-free inputs shared by current photo contract tests."""

from __future__ import annotations
import builtins
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills/photo-prompt-image-generator/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import prompt_generator
import audit_composed_prompt
import audit_image_render_request


V17_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/glass-main-merge-20261005/V17-PARENT-SOURCE.json'
)
V17_PARENT_MANIFEST_SHA256 = '2ba4ade97e8bb150a91b708c090cdce57d5180789504c54c4c0272dafdf1548e'
V17_PARENT_COMMIT = '977a5d8680eabf24c6e19993340b4a72f884b24a'
V17_PARENT_VALIDATOR = 'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'
V17_SUPPORT_MANIFEST = V17_PARENT_MANIFEST.with_name('V17-VALIDATOR-SUPPORT.json')
V17_SUPPORT_MANIFEST_SHA256 = '005642904a7a21891696fd21e93d6bde445a6747c903515f48ad762d9c0efb40'
V18_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/cf40-history-repair-20261005/V18-PARENT-SOURCE.json'
)
V18_PARENT_MANIFEST_SHA256 = '20c5964ab21353c99ad1b747ac9abe0f9e99ff0efc32b68a3ace3409954d6d51'
V18_PARENT_COMMIT = 'e68da84497b2c0f9d67dae33199a51f4aa163898'
V19_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/b5-guidance-integration-20261005/V19-PARENT-SOURCE.json'
)
V19_PARENT_MANIFEST_SHA256 = '114862610fdc1bba449bcefd8d86ec79b17806c56bd051958a8bf69089f43416'
V19_PARENT_COMMIT = '9105a63d9b261f91219875e15f346d6d52e477bc'
V20_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/visual-profile-shards-20261005/V20-PARENT-SOURCE.json'
)
V20_PARENT_MANIFEST_SHA256 = '0949707e066ccfb73396b5825f4d70bdc79b2155e091d4233913bd7eba147e6b'
V20_PARENT_COMMIT = '1d30c96a3a05abfa91f49ac98f205f4e09202a19'
V21_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/gothic-sharded-main-merge-20261005/V21-PARENT-SOURCE.json'
)
V21_PARENT_MANIFEST_SHA256 = 'ceea06a904b6605e5ee359eefb1f2b9e031d7a385ca17beeca89d4bb8c289088'
V21_PARENT_COMMIT = '726c51b015294930f0ad98ca126cde11e6caead2'
V22_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/lobe-boundary-integration-20261005/V22-PARENT-SOURCE.json'
)
V22_PARENT_MANIFEST_SHA256 = 'dd9e41534d3587a87c762725887f330e72b751cc0b9a34192a8dd5469cab9bb7'
V22_PARENT_COMMIT = '900bf2efdd17fbc6a6ef3aa340f3526b1e01f223'
V23_PARENT_MANIFEST = Path(
    'docs/research-evidence/photo-prompt/structure-maintenance-20261006/main-integration/V23-PARENT-SOURCE.json'
)
V23_PARENT_MANIFEST_SHA256 = '971f33aae01e0c79559f99a894800dba488917694bbaaff87148593ea516d76a'
V23_PARENT_COMMIT = 'baa876d8299930b8897a282f65779d4412d056b5'


def _v17_safe_path(value: str) -> Path:
    if (not isinstance(value, str) or not value or '\\' in value or ':' in value
            or '\x00' in value or value.startswith('/')
            or any(part in ('', '.', '..') for part in value.split('/'))
            or str(PurePosixPath(value)) != value):
        raise AssertionError('Unsafe V17 historical source path')
    return Path(value)


def _v17_regular_path(root: Path, value: str) -> Path:
    relative = _v17_safe_path(value)
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise AssertionError('Unsafe V17 historical source symlink')
    if not current.is_file():
        raise AssertionError(f'Missing V17 historical source payload: {value}')
    return current


def _v17_parent_manifest(source_root: Path = ROOT) -> dict:
    """The fixed digest authenticates the complete mapping, not a self-reported seal."""
    raw = _v17_regular_path(source_root, V17_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V17_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V17 parent source manifest drift')
    manifest = json.loads(raw)
    if (manifest.get('schema') != 'photo-v17-parent-source-manifest/v1'
            or manifest.get('source_pin') != V17_PARENT_COMMIT
            or manifest.get('member_count') != 149
            or len(manifest.get('members', [])) != 149
            or len(manifest.get('dependencies', [])) != 31):
        raise AssertionError('Frozen V17 parent source manifest shape drift')
    members = manifest['members']
    records = members + manifest['dependencies']
    paths, sources = set(), set()
    for row in records:
        path = _v17_safe_path(row['path']).as_posix()
        source = _v17_safe_path(row['source_path']).as_posix()
        _v17_safe_path(row['git_path'])
        if path in paths or source in sources:
            raise AssertionError('Duplicate V17 historical source path')
        paths.add(path)
        sources.add(source)
        if (row['git_commit'] != V17_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0
                or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V17 historical source provenance drift')
    expected_counts = {'reuse_committed_evidence': 109,
                       'reuse_retained_semantic_generation': 16,
                       'new_immutable_snapshot_same_git_blob': 24}
    if (manifest['counts'] != expected_counts
            or {kind: sum(row['kind'] == kind for row in members)
                for kind in expected_counts} != expected_counts
            or sum(row['bytes'] for row in members) != manifest['total_member_bytes']):
        raise AssertionError('Frozen V17 historical source inventory drift')
    shard_prefix = 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index_shards/7ed22190c0382b63/'
    shards = {row['path'] for row in members
              if row['kind'] == 'reuse_retained_semantic_generation'}
    if shards != {f'{shard_prefix}shard-{index:03d}.json' for index in range(16)}:
        raise AssertionError('Frozen V17 retained semantic generation drift')
    for row in members:
        if row['kind'] == 'reuse_retained_semantic_generation':
            allowed = row['source_path'] == row['path']
        elif row['kind'] == 'new_immutable_snapshot_same_git_blob':
            allowed = row['source_path'] == (V17_PARENT_MANIFEST.parent /
                'v17-parent-source-files' / row['path']).as_posix()
        else:
            allowed = row['source_path'].startswith('docs/research-evidence/photo-prompt/')
        if not allowed:
            raise AssertionError('Unregistered V17 historical source backing path')
    return manifest


def _v17_verified_payload(source_root: Path, row: dict) -> bytes:
    raw = _v17_regular_path(source_root, row['source_path']).read_bytes()
    blob = hashlib.sha1(f'blob {len(raw)}\0'.encode('ascii') + raw).hexdigest()
    if (len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']
            or blob != row['git_blob']):
        raise AssertionError(f'Frozen V17 historical source payload drift: {row["path"]}')
    return raw


def materialize_v17_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Reconstruct the 149 exact source files and 31 sealed dependencies without Git.

    Reused old shards are mandatory historical inputs, even after a new generation
    becomes active. There is no fallback to live DATA or recursive docs copying.
    """
    manifest = _v17_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V17 historical destination must be an empty directory')
    # Validate every payload before creating any historical member. Check again
    # while copying so the written bytes are the bytes whose seals were verified.
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def _v17_support_manifest(source_root: Path = ROOT) -> dict:
    raw = _v17_regular_path(source_root, V17_SUPPORT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V17_SUPPORT_MANIFEST_SHA256:
        raise AssertionError('Frozen V17 validator support manifest drift')
    manifest = json.loads(raw)
    names = {'illustration_runtime', 'illustration_audit', 'universal_scene_runtime'}
    if (manifest['schema'] != 'photo-v17-validator-support/v1'
            or manifest['source_pin'] != V17_PARENT_COMMIT
            or len(manifest['members']) != 3
            or {row['module'] for row in manifest['members']} != names):
        raise AssertionError('Frozen V17 validator support inventory drift')
    for row in manifest['members']:
        expected = str(Path(V17_PARENT_VALIDATOR).with_name(row['module'] + '.py'))
        if (row['path'] != expected or row['git_path'] != expected
                or row['git_commit'] != V17_PARENT_COMMIT or row['mode'] not in ('100644', '100755')
                or row['source_path'] != (V17_PARENT_MANIFEST.parent /
                    'v17-validator-support' / expected).as_posix()):
            raise AssertionError('Frozen V17 validator support provenance drift')
    return manifest


def pinned_v17_validator(directory: Path, *, source_root: Path = ROOT):
    """Load the original validator and its three sealed local imports in isolation."""
    manifest = _v17_parent_manifest(source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, source_root, version=17)


def _isolated_parent_validator(directory: Path, raw: bytes, source_root: Path, *, version: int):
    """The V17/V18 validators share the same three immutable support modules."""
    support = _v17_support_manifest(source_root)
    payloads = [(row, _v17_verified_payload(source_root, row)) for row in support['members']]
    for row, payload in payloads:
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        target.chmod(int(row['mode'][-3:], 8))
    path = directory / V17_PARENT_VALIDATOR
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    prefix = f'_archived_photo_v{version}_' + hashlib.sha256(str(directory).encode()).hexdigest()[:16]
    modules, specs = {}, {}
    for name in [row['module'] for row in support['members']] + ['validate_illustration_assets']:
        spec = importlib.util.spec_from_file_location(prefix + '_' + name, path.with_name(name + '.py'))
        modules[name] = importlib.util.module_from_spec(spec)
        specs[name] = spec

    def historical_import(name, globals=None, locals=None, fromlist=(), level=0):
        # These exact local names include lazy universal-scene imports. Never
        # accept a same-named live/cached module; stdlib imports remain ordinary.
        if level == 0 and name in modules:
            return modules[name]
        return builtins.__import__(name, globals, locals, fromlist, level)

    previous = {module.__name__: sys.modules.get(module.__name__) for module in modules.values()}
    try:
        for module in modules.values():
            module.__dict__['__builtins__'] = dict(vars(builtins), __import__=historical_import)
            # Dataclass annotation processing needs a module entry during load.
            sys.modules[module.__name__] = module
        for name, module in modules.items():
            specs[name].loader.exec_module(module)
    finally:
        for name, original in previous.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
    return modules['validate_illustration_assets']


def archived_v17_validator(directory: Path, *, source_root: Path = ROOT):
    materialize_v17_parent_source(directory, source_root=source_root)
    return pinned_v17_validator(directory, source_root=source_root)


def _v18_parent_manifest(source_root: Path = ROOT) -> dict:
    raw = _v17_regular_path(source_root, V18_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V18_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V18 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'reuse_v17_parent_source': 129, 'reuse_retained_v18_data': 18,
              'new_immutable_snapshot_same_git_blob': 2}
    if (manifest['schema'] != 'photo-v18-parent-source-manifest/v1'
            or manifest['source_pin'] != V18_PARENT_COMMIT
            or manifest['member_count'] != 149 or len(manifest['members']) != 149
            or len(manifest['dependencies']) != 193 or manifest['counts'] != counts
            or manifest['validator_support_manifest'] != V17_SUPPORT_MANIFEST.as_posix()
            or manifest['validator_support_manifest_sha256'] != V17_SUPPORT_MANIFEST_SHA256):
        raise AssertionError('Frozen V18 parent source manifest shape drift')
    previous = {row['path']: row for row in _v17_parent_manifest(source_root)['members']}
    members = manifest['members']
    paths = set()
    for row in members + manifest['dependencies']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if path in paths:
            raise AssertionError('Duplicate V18 historical source path')
        paths.add(path)
        if (row['git_commit'] != V18_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V18 historical source provenance drift')
    if (len({row['source_path'] for row in members}) != 149
            or {kind: sum(row['kind'] == kind for row in members) for kind in counts} != counts
            or sum(row['bytes'] for row in members) != manifest['total_member_bytes']):
        raise AssertionError('Frozen V18 historical source inventory drift')
    assets = 'skills/photo-prompt-image-generator/assets/'
    retained = {assets + 'photo_prompt_tags.json', assets + 'photo_prompt_semantic_index.json'}
    retained.update(assets + f'photo_prompt_semantic_index_shards/7ff3e10cc7163368/shard-{index:03d}.json'
                    for index in range(16))
    if {row['path'] for row in members if row['kind'] == 'reuse_retained_v18_data'} != retained:
        raise AssertionError('Frozen V18 retained DATA generation drift')
    for row in members:
        if row['kind'] == 'reuse_v17_parent_source':
            old = previous.get(row['path'], {})
            allowed = all(row[key] == old.get(key) for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        elif row['kind'] == 'reuse_retained_v18_data':
            allowed = row['source_path'] == row['path']
        else:
            allowed = row['path'] in (V17_PARENT_VALIDATOR,
                'skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json')
            allowed = allowed and row['source_path'] == (V18_PARENT_MANIFEST.parent /
                'v18-parent-source-files' / row['path']).as_posix()
        if not allowed:
            raise AssertionError('Unregistered V18 historical source backing path')
    if any(row['source_path'] != row['path'] for row in manifest['dependencies']):
        raise AssertionError('Unregistered V18 historical dependency backing path')
    return manifest


def materialize_v18_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Copy only the fixed e68 source and enumerated pre-existing dependencies."""
    manifest = _v18_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V18 historical destination must be an empty directory')
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v18_validator(directory: Path, *, source_root: Path = ROOT):
    manifest = materialize_v18_parent_source(directory, source_root=source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, directory, version=18)


def _v19_parent_manifest(source_root: Path = ROOT) -> dict:
    """Authenticate the exact V19 source; never substitute current guidance."""
    raw = _v17_regular_path(source_root, V19_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V19_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V19 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'reuse_v18_parent_source': 144, 'reuse_retained_v19_data': 2,
              'new_immutable_snapshot_same_git_blob': 3}
    if (manifest['schema'] != 'photo-v19-parent-source-manifest/v1'
            or manifest['source_pin'] != V19_PARENT_COMMIT
            or manifest['member_count'] != 149 or len(manifest['members']) != 149
            or manifest['dependency_count'] != 199 or len(manifest['dependencies']) != 199
            or manifest['counts'] != counts
            or manifest['validator_support_manifest'] != V17_SUPPORT_MANIFEST.as_posix()
            or manifest['validator_support_manifest_sha256'] != V17_SUPPORT_MANIFEST_SHA256):
        raise AssertionError('Frozen V19 parent source manifest shape drift')
    previous = {row['path']: row for row in _v18_parent_manifest(source_root)['members']}
    members = manifest['members']
    paths = set()
    for row in members + manifest['dependencies']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if path in paths:
            raise AssertionError('Duplicate V19 historical source path')
        paths.add(path)
        if (row['git_commit'] != V19_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V19 historical source provenance drift')
    if (len({row['source_path'] for row in members}) != 149
            or {kind: sum(row['kind'] == kind for row in members) for kind in counts} != counts
            or sum(row['bytes'] for row in members) != manifest['total_member_bytes']):
        raise AssertionError('Frozen V19 historical source inventory drift')
    retained = {'skills/photo-prompt-image-generator/assets/photo_prompt_subculture_appearance_extension.json',
                'skills/photo-prompt-image-generator/assets/photo_prompt_textile_surface_extension.json'}
    snapshots = {V17_PARENT_VALIDATOR, 'skills/photo-prompt-image-generator/SKILL.md',
                 'skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json'}
    for row in members:
        if row['kind'] == 'reuse_v18_parent_source':
            old = previous.get(row['path'], {})
            allowed = all(row[key] == old.get(key) for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        elif row['kind'] == 'reuse_retained_v19_data':
            allowed = row['path'] in retained and row['source_path'] == row['path']
        else:
            allowed = row['path'] in snapshots and row['source_path'] == (
                V19_PARENT_MANIFEST.parent / 'v19-parent-source-files' / row['path']).as_posix()
        if not allowed:
            raise AssertionError('Unregistered V19 historical source backing path')
    if any(row['source_path'] != row['path'] for row in manifest['dependencies']):
        raise AssertionError('Unregistered V19 historical dependency backing path')
    return manifest


def materialize_v19_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Copy only the pinned 9105 source and its sealed dependencies, without Git."""
    manifest = _v19_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V19 historical destination must be an empty directory')
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v19_validator(directory: Path, *, source_root: Path = ROOT):
    manifest = materialize_v19_parent_source(directory, source_root=source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, directory, version=19)


def _v20_parent_manifest(source_root: Path = ROOT) -> dict:
    """Authenticate the exact V20 source; never substitute current guidance."""
    raw = _v17_regular_path(source_root, V20_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V20_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V20 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'reuse_v19_parent_source': 144,
              'new_immutable_snapshot_same_git_blob': 5}
    if (manifest['schema'] != 'photo-v20-parent-source-manifest/v1'
            or manifest['source_pin'] != V20_PARENT_COMMIT
            or manifest['member_count'] != 149 or len(manifest['members']) != 149
            or manifest['dependency_count'] != 207 or len(manifest['dependencies']) != 207
            or manifest['counts'] != counts
            or manifest['validator_support_manifest'] != V17_SUPPORT_MANIFEST.as_posix()
            or manifest['validator_support_manifest_sha256'] != V17_SUPPORT_MANIFEST_SHA256):
        raise AssertionError('Frozen V20 parent source manifest shape drift')
    previous = {row['path']: row for row in _v19_parent_manifest(source_root)['members']}
    members = manifest['members']
    paths = set()
    for row in members + manifest['dependencies']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if path in paths:
            raise AssertionError('Duplicate V20 historical source path')
        paths.add(path)
        if (row['git_commit'] != V20_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V20 historical source provenance drift')
    if (len({row['source_path'] for row in members}) != 149
            or {kind: sum(row['kind'] == kind for row in members) for kind in counts} != counts
            or sum(row['bytes'] for row in members) != manifest['total_member_bytes']):
        raise AssertionError('Frozen V20 historical source inventory drift')
    snapshots = {V17_PARENT_VALIDATOR, 'skills/photo-prompt-image-generator/SKILL.md',
                 'skills/photo-prompt-image-generator/references/composition-contract.md',
                 'skills/photo-prompt-image-generator/references/retrieval-contract.md',
                 'skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json'}
    for row in members:
        if row['kind'] == 'reuse_v19_parent_source':
            old = previous.get(row['path'], {})
            allowed = all(row[key] == old.get(key) for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        else:
            allowed = row['path'] in snapshots and row['source_path'] == (
                V20_PARENT_MANIFEST.parent / 'v20-parent-source-files' / row['path']).as_posix()
        if not allowed:
            raise AssertionError('Unregistered V20 historical source backing path')
    if any(row['source_path'] != row['path'] for row in manifest['dependencies']):
        raise AssertionError('Unregistered V20 historical dependency backing path')
    return manifest


def materialize_v20_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Copy only the pinned 1d30 source and its sealed dependencies, without Git."""
    manifest = _v20_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V20 historical destination must be an empty directory')
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v20_validator(directory: Path, *, source_root: Path = ROOT):
    manifest = materialize_v20_parent_source(directory, source_root=source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, directory, version=20)


def _v21_parent_manifest(source_root: Path = ROOT) -> dict:
    """Authenticate the V21 source independently of today's expanded DATA."""
    raw = _v17_regular_path(source_root, V21_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V21_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V21 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'reuse_v20_parent_source': 141,
              'reuse_content_addressed_vector_shard': 16,
              'new_immutable_snapshot_same_git_blob': 9}
    if (manifest['schema'] != 'photo-v21-parent-source-manifest/v1'
            or manifest['source_pin'] != V21_PARENT_COMMIT
            or manifest['member_count'] != 166 or len(manifest['members']) != 166
            or manifest['dependency_count'] != 216 or len(manifest['dependencies']) != 216
            or manifest['counts'] != counts
            or manifest['previous_manifest_path'] != V20_PARENT_MANIFEST.as_posix()
            or manifest['previous_manifest_sha256'] != V20_PARENT_MANIFEST_SHA256):
        raise AssertionError('Frozen V21 parent source manifest shape drift')
    previous = {row['path']: row for row in _v20_parent_manifest(source_root)['members']}
    paths = set()
    for row in manifest['members'] + manifest['dependencies']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if path in paths:
            raise AssertionError('Duplicate V21 historical source path')
        paths.add(path)
        if (row['git_commit'] != V21_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V21 historical source provenance drift')
    for row in manifest['members']:
        if row['kind'] == 'reuse_v20_parent_source':
            old = previous.get(row['path'], {})
            allowed = all(row[key] == old.get(key) for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        elif row['kind'] == 'reuse_content_addressed_vector_shard':
            allowed = (row['source_path'] == row['path']
                       and row['path'].startswith('skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index_shards/'))
        else:
            allowed = row['source_path'] == (
                V21_PARENT_MANIFEST.parent / 'v21-parent-source-files' / row['path']).as_posix()
        if not allowed:
            raise AssertionError('Unregistered V21 historical source backing path')
    if (len({row['source_path'] for row in manifest['members']}) != 166
            or {kind: sum(row['kind'] == kind for row in manifest['members']) for kind in counts} != counts
            or sum(row['bytes'] for row in manifest['members']) != manifest['total_member_bytes']
            or any(row['source_path'] != row['path'] for row in manifest['dependencies'])):
        raise AssertionError('Frozen V21 historical source inventory drift')
    return manifest


def materialize_v21_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Restore all sealed V21 files before replay; no Git or live-source fallback."""
    manifest = _v21_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V21 historical destination must be an empty directory')
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v21_validator(directory: Path, *, source_root: Path = ROOT):
    manifest = materialize_v21_parent_source(directory, source_root=source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, directory, version=21)


def archived_validator_with_v21_source(directory: Path, *, version: int, source_root: Path = ROOT):
    """Explicitly feed unchanged predecessor helpers their frozen V21 inputs."""
    helpers = {18: archived_v18_validator, 19: archived_v19_validator, 20: archived_v20_validator}
    if version not in helpers:
        raise AssertionError('Unsupported V21-backed predecessor fixture')
    with tempfile.TemporaryDirectory(prefix='sealed-v21-inputs-') as saved:
        frozen = Path(saved)
        materialize_v21_parent_source(frozen, source_root=source_root)
        return helpers[version](directory, source_root=frozen)


def _v22_parent_manifest(source_root: Path = ROOT) -> dict:
    """Authenticate V22 independently of the current lobe wording and validator."""
    raw = _v17_regular_path(source_root, V22_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V22_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V22 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'reuse_v21_parent_source': 129, 'reuse_retained_vector_shard': 31,
              'new_immutable_snapshot_same_git_blob': 8}
    if (manifest['schema'] != 'photo-v22-parent-source-manifest/v1'
            or manifest['source_pin'] != V22_PARENT_COMMIT
            or manifest['member_count'] != 168 or len(manifest['members']) != 168
            or manifest['dependency_count'] != 261 or len(manifest['dependencies']) != 261
            or manifest['counts'] != counts
            or manifest['previous_manifest_path'] != V21_PARENT_MANIFEST.as_posix()
            or manifest['previous_manifest_sha256'] != V21_PARENT_MANIFEST_SHA256):
        raise AssertionError('Frozen V22 parent source manifest shape drift')
    previous = {row['path']: row for row in _v21_parent_manifest(source_root)['members']}
    paths = set()
    for row in manifest['members'] + manifest['dependencies']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if path in paths:
            raise AssertionError('Duplicate V22 historical source path')
        paths.add(path)
        if (row['git_commit'] != V22_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V22 historical source provenance drift')
    for row in manifest['members']:
        if row['kind'] == 'reuse_v21_parent_source':
            old = previous.get(row['path'], {})
            allowed = all(row[key] == old.get(key) for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        elif row['kind'] == 'reuse_retained_vector_shard':
            allowed = (row['source_path'] == row['path']
                       and row['path'].startswith('skills/photo-prompt-image-generator/assets/')
                       and '_index_shards/' in row['path'])
        elif row['kind'] == 'new_immutable_snapshot_same_git_blob':
            allowed = row['source_path'] == (
                V22_PARENT_MANIFEST.parent / 'v22-parent-source-files' / row['path']).as_posix()
        else:
            allowed = False
        if not allowed:
            raise AssertionError('Unregistered V22 historical source backing path')
    if (len({row['source_path'] for row in manifest['members']}) != 168
            or {kind: sum(row['kind'] == kind for row in manifest['members']) for kind in counts} != counts
            or sum(row['bytes'] for row in manifest['members']) != manifest['total_member_bytes']
            or any(row['source_path'] != row['path'] or row['kind'] != 'retained_dependency'
                   for row in manifest['dependencies'])):
        raise AssertionError('Frozen V22 historical source inventory drift')
    return manifest


def materialize_v22_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Restore the exact V22 source without Git, symlinks, or live-source fallback."""
    manifest = _v22_parent_manifest(source_root)
    records = manifest['members'] + manifest['dependencies']
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V22 historical destination must be an empty directory')
    for row in records:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in records:
        raw = _v17_verified_payload(source_root, row)
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v22_validator(directory: Path, *, source_root: Path = ROOT):
    manifest = materialize_v22_parent_source(directory, source_root=source_root)
    row = next(row for row in manifest['members'] if row['path'] == V17_PARENT_VALIDATOR)
    raw = _v17_verified_payload(source_root, row)
    return _isolated_parent_validator(directory, raw, directory, version=22)


def _v23_parent_manifest(source_root: Path = ROOT) -> dict:
    """Authenticate the complete V23 input tree before the structural migration."""
    raw = _v17_regular_path(source_root, V23_PARENT_MANIFEST.as_posix()).read_bytes()
    if hashlib.sha256(raw).hexdigest() != V23_PARENT_MANIFEST_SHA256:
        raise AssertionError('Frozen V23 parent source manifest drift')
    manifest = json.loads(raw)
    counts = {'new_immutable_snapshot_same_git_blob': 16,
              'reuse_immutable_history': 430, 'reuse_sealed_v22_backing': 128}
    if (manifest['schema'] != 'photo-v23-parent-source-manifest/v1'
            or manifest['source_pin'] != V23_PARENT_COMMIT
            or manifest['source_tree'] != 'a727c9dd6f4894b10f17cd8c94245c2d39418f7f'
            or manifest['member_count'] != 574 or len(manifest['members']) != 574
            or manifest['counts'] != counts
            or manifest['previous_manifest_path'] != V22_PARENT_MANIFEST.as_posix()
            or manifest['previous_manifest_sha256'] != V22_PARENT_MANIFEST_SHA256):
        raise AssertionError('Frozen V23 parent source manifest shape drift')
    previous = _v22_parent_manifest(source_root)
    old = {row['path']: row for row in previous['members'] + previous['dependencies']}
    paths = set()
    for row in manifest['members']:
        path = _v17_safe_path(row['path']).as_posix()
        _v17_safe_path(row['source_path'])
        if (path in paths or row['git_commit'] != V23_PARENT_COMMIT or row['git_path'] != path
                or row['mode'] not in ('100644', '100755') or type(row['bytes']) is not int
                or row['bytes'] < 0 or len(row['sha256']) != 64 or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])):
            raise AssertionError('Frozen V23 historical source provenance drift')
        paths.add(path)
        if row['kind'] == 'reuse_sealed_v22_backing':
            allowed = all(row[key] == old.get(path, {}).get(key)
                          for key in ('source_path', 'git_blob', 'mode', 'bytes', 'sha256'))
        elif row['kind'] == 'reuse_immutable_history':
            allowed = row['source_path'] == path
        elif row['kind'] == 'new_immutable_snapshot_same_git_blob':
            allowed = row['source_path'] == (
                V23_PARENT_MANIFEST.parent / 'v23-parent-source-files' / path).as_posix()
        else:
            allowed = False
        if not allowed:
            raise AssertionError('Unregistered V23 historical backing path')
    if ({kind: sum(row['kind'] == kind for row in manifest['members']) for kind in counts} != counts
            or sum(row['bytes'] for row in manifest['members']) != manifest['total_member_bytes']):
        raise AssertionError('Frozen V23 historical source inventory drift')
    return manifest


def materialize_v23_parent_source(directory: Path, *, source_root: Path = ROOT) -> dict:
    """Restore original V23 source and dependencies without Git or live fallback."""
    manifest = _v23_parent_manifest(source_root)
    if directory.is_symlink() or (directory.exists() and any(directory.iterdir())):
        raise AssertionError('V23 historical destination must be an empty directory')
    for row in manifest['members']:
        _v17_verified_payload(source_root, row)
    directory.mkdir(parents=True, exist_ok=True)
    for row in manifest['members']:
        target = directory / _v17_safe_path(row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_v17_verified_payload(source_root, row))
        target.chmod(int(row['mode'][-3:], 8))
    return manifest


def archived_v23_validator(directory: Path, *, source_root: Path = ROOT):
    """Load V23 with its exact sealed support modules, isolated from live imports."""
    materialize_v23_parent_source(directory, source_root=source_root)
    scripts = directory / Path(V17_PARENT_VALIDATOR).parent
    prefix = '_archived_photo_v23_' + hashlib.sha256(str(directory).encode()).hexdigest()[:16]
    modules, specs = {}, {}
    for name in ('illustration_runtime', 'illustration_audit', 'universal_scene_runtime',
                 'validate_illustration_assets'):
        spec = importlib.util.spec_from_file_location(prefix + '_' + name, scripts / (name + '.py'))
        modules[name] = importlib.util.module_from_spec(spec)
        specs[name] = spec

    def historical_import(name, globals=None, locals=None, fromlist=(), level=0):
        if level == 0 and name in modules:
            return modules[name]
        return builtins.__import__(name, globals, locals, fromlist, level)

    previous = {module.__name__: sys.modules.get(module.__name__) for module in modules.values()}
    try:
        for module in modules.values():
            module.__dict__['__builtins__'] = dict(vars(builtins), __import__=historical_import)
            sys.modules[module.__name__] = module
        for name, module in modules.items():
            specs[name].loader.exec_module(module)
    finally:
        for name, original in previous.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
    return modules['validate_illustration_assets']


def load_v23_candidate_fixture(path: Path, extension_files: tuple[str, ...]) -> dict:
    """Read a legacy candidate snapshot with sealed V23 code in a fresh process."""
    manifest = _v23_parent_manifest()
    prefix = 'skills/photo-prompt-image-generator/'
    with tempfile.TemporaryDirectory(prefix='v23-candidate-runtime-') as saved:
        directory = Path(saved)
        for row in manifest['members']:
            if row['path'].startswith((prefix + 'scripts/', prefix + 'precore/')):
                target = directory / _v17_safe_path(row['path'])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(_v17_verified_payload(ROOT, row))
        names = directory / 'extensions.json'
        names.write_text(json.dumps(extension_files))
        output = directory / 'loaded.json'
        script = (
            'import json,sys; from pathlib import Path; '
            'sys.path.insert(0,sys.argv[1]); import prompt_generator as generator; '
            'generator.RESEARCH_EXTENSION_FILENAMES=tuple(json.loads(Path(sys.argv[3]).read_text())); '
            'Path(sys.argv[4]).write_text(json.dumps(generator.load_json(sys.argv[2]),ensure_ascii=False))'
        )
        result = subprocess.run(
            [sys.executable, '-c', script, str(directory / prefix / 'scripts'),
             str(path), str(names), str(output)], capture_output=True, text=True, timeout=60,
        )
        if result.returncode:
            raise AssertionError('Historical V23 candidate load failed: ' + result.stderr)
        return json.loads(output.read_text())


def archived_v16_validator(directory: Path):
    """Replay V16 with its immutable runtime and DATA, not today's registry."""
    archive = ROOT / 'docs/research-evidence/photo-prompt/cute-semantics-main-merge-20261005/V16-PARENT-SOURCE.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == '921d8d9c43cc1e56abc068b3f76435fd93fb9a84d9727606e65b0511ba4220a4'
    with zipfile.ZipFile(archive) as saved:
        for name in saved.namelist():
            path = Path(name)
            assert not path.is_absolute() and '..' not in path.parts
        saved.extractall(directory)
    assets = directory / 'skills/subculture-illustration-image-generator/assets'
    current = ROOT / 'skills/subculture-illustration-image-generator/assets'
    for path in current.iterdir():
        if path.is_file() and not (assets / path.name).exists():
            shutil.copyfile(path, assets / path.name)
    (directory / 'docs').symlink_to(ROOT / 'docs', target_is_directory=True)
    (directory / 'tests').symlink_to(ROOT / 'tests', target_is_directory=True)
    path = directory / 'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'
    spec = importlib.util.spec_from_file_location('archived_photo_v16_validator', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_TEST_PROMPT_BUDGET_EXTENSION = (
    "Fine-grained surface cues, coherent near-to-far depth, controlled highlights, legible "
    "shadow detail, and an intentional focal hierarchy keep the completed photographic frame "
    "specific, balanced, natural, and visually unambiguous."
)


def envelope(request_text: str, active_texts: tuple[str, ...] | None = None) -> dict:
    active_texts = active_texts or (request_text,)
    spans = []
    search_from = 0
    for index, text in enumerate(active_texts):
        start = request_text.find(text, search_from)
        if start < 0:
            raise AssertionError(f"active text is not in request: {text!r}")
        end = start + len(text)
        spans.append(
            {
                "span_id": f"scope_{index + 1}",
                "start": start,
                "end": end,
                "text": text,
            }
        )
        search_from = end
    return {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": "test-request",
        "request_text": request_text,
        "request_sha256": hashlib.sha256(request_text.encode("utf-8")).hexdigest(),
        "active_spans": spans,
    }


def core(
    source_request: str,
    *,
    interpreted_intent: str = (
        "A quiet rainlit still life centered on blue porcelain and restrained domestic calm"
    ),
    subject: str = "one blue porcelain teacup",
    setting: str = "a quiet rainlit kitchen counter",
    event: str = "steam rises while window reflections drift across the glaze",
    visual_priorities: tuple[str, ...] = (
        "blue porcelain glaze",
        "rainlit window reflections",
        "delicate rising steam",
    ),
    baseline_prompt_en: str = (
        "A blue porcelain teacup rests on a dark kitchen counter while delicate rising "
        "steam catches rainlit window reflections, with a quiet domestic mood, restrained "
        "slate colors, shallow focus, and tactile glaze detail."
    ),
    definitions: tuple[dict, ...] = (),
    interpretations: tuple[dict, ...] | None = None,
    exclusions: tuple[str, ...] = (),
    runtime_forbidden_labels: tuple[str, ...] = (),
    locked_dimensions: tuple[str, ...] = ("concept", "subject", "event"),
    open_dimensions: tuple[str, ...] = (
        "framing",
        "composition",
        "lighting",
        "camera",
        "color",
        "material",
        "atmosphere",
        "relationship",
    ),
    anchor_evidence: tuple[str, ...] | None = None,
) -> dict:
    if len(prompt_generator.authorial_request_content_words(baseline_prompt_en)) < (
        prompt_generator.AUTHORIAL_PROMPT_MIN_WORDS
    ):
        baseline_prompt_en = f"{baseline_prompt_en.rstrip()} {_TEST_PROMPT_BUDGET_EXTENSION}"
    if interpretations is None:
        interpretations = (
            {
                "term": "governing request",
                "source_text": source_request,
                "basis": "request_context",
                "resolution": interpreted_intent,
                "sources": [],
            },
        )
    if anchor_evidence is None:
        candidates = [subject, event, *visual_priorities]
        evidence_candidates = [
            phrase for phrase in candidates if phrase.casefold() in baseline_prompt_en.casefold()
        ]
        baseline_tokens = baseline_prompt_en.split()
        for start in range(0, max(len(baseline_tokens) - 3, 0), 2):
            phrase = " ".join(baseline_tokens[start : start + 4]).strip(" ,.;:!?")
            if phrase and phrase.casefold() in baseline_prompt_en.casefold():
                evidence_candidates.append(phrase)
        unique_evidence: list[str] = []
        seen_evidence: set[str] = set()
        for phrase in evidence_candidates:
            key = phrase.strip().casefold()
            if key and key not in seen_evidence:
                seen_evidence.add(key)
                unique_evidence.append(phrase)
        anchor_evidence = tuple(unique_evidence)
    evidence_rows = list(anchor_evidence)
    if len(evidence_rows) < len(locked_dimensions):
        raise AssertionError(
            "test core needs one distinct baseline evidence phrase per locked dimension"
        )
    return {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": source_request,
        "interpreted_intent": interpreted_intent,
        "subject": subject,
        "setting": setting,
        "event": event,
        "visual_priorities": list(visual_priorities),
        "baseline_prompt_en": baseline_prompt_en,
        "user_definitions": list(definitions),
        "interpretation_provenance": list(interpretations),
        "unresolved_ambiguities": [],
        "user_exclusions": list(exclusions),
        "runtime_forbidden_labels": list(runtime_forbidden_labels),
        "intent_lock": {
            "contract_version": "photo-intent-lock/v2",
            "priority": "requesting_user",
            "semantic_anchors": [
                {
                    "anchor_id": f"anchor_{dimension}",
                    "source_text": source_request,
                    "dimension": dimension,
                    "prompt_evidence": evidence_rows[index],
                }
                for index, dimension in enumerate(locked_dimensions)
            ],
            "locked_dimensions": list(locked_dimensions),
            "open_dimensions": list(open_dimensions),
        },
        "style": {
            "domain": "general_photo",
            "family": "context-led photographic study",
            "evidence": ["restrained color hierarchy", "tactile material detail"],
        },
        "variation_key": "current-test",
        "semantic_assertions": [],
        "request_lineage": None,
    }


def review(prompt: str, provenance: str = "agent_prepack") -> dict:
    """Synthetic review binding for tests of contracts other than embodiment.

    Actual body-action review cases live in test_photo_embodiment. This helper
    does not claim physical or rendered-image qualification.
    """
    return {
        "contract_version": "photo-embodiment-review/v1",
        "provenance": provenance,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "scope": "not_applicable",
        "summary": "Synthetic contract fixture; physical review is tested in the dedicated embodiment suite.",
        "checks": {},
    }


def candidate_source(data: dict, frozen: dict, *, seed: int = 7, controls: dict | None = None,
                     overrides: dict | None = None, context: dict | None = None,
                     visual_intent: dict | None = None) -> dict:
    """Supply complete current inputs for tests of downstream contracts."""
    import copy
    snapshot = controls
    if snapshot is None:
        values = {"sensual": 0, "fetish": 0, "creativity": 1, "surreal": 0, **(overrides or {})}
        snapshot = prompt_generator.creative_controls.resolve(
            frozen["source_request"], overrides=values, context=context or {}, seed=7)
        binding = frozen["request_binding"]
        request = prompt_generator.normalize_request_envelope({
            "contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
            "request_id": binding["request_id"], "request_text": frozen["source_request"],
            "request_sha256": binding["request_sha256"], "active_spans": binding["active_spans"],
        })
        raw = copy.deepcopy(frozen)
        for key in ("canonical_sha256", "core_id", "request_binding"):
            raw.pop(key, None)
        raw["intent_lock"] = {key: value for key,value in raw["intent_lock"].items()
                              if key in {"contract_version","priority","semantic_anchors","locked_dimensions","open_dimensions"}}
        if isinstance(raw.get("request_lineage"),dict):raw["request_lineage"].pop("canonical_sha256",None)
        raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
        bound = prompt_generator.normalize_authorial_core(raw,request_envelope=request,creative_control_snapshot=snapshot)
        frozen.clear();frozen.update(bound)
    return prompt_generator.prepare_candidate_source(data,frozen,snapshot,
        review(frozen["baseline_prompt_en"]),seed=seed,visual_intent=visual_intent)


def composition_review(pack: dict, prompt: str) -> dict:
    return {
        "source_contract_sha256": pack["embodiment_preflight"]["canonical_sha256"],
        "review": review(prompt, "agent_postcomposition"),
    }


def run_current(
    core_input: dict,
    *,
    seed: int = 91,
    creativity: int = 1,
    envelope_input: dict | None = None,
    extra_args: tuple = (),
) -> dict:
    """Invoke the normal public CLI with all authored current inputs."""
    import copy
    import json
    import subprocess
    import tempfile

    raw = copy.deepcopy(core_input)
    request = envelope_input or envelope(raw["source_request"])
    snapshot = prompt_generator.creative_controls.resolve(
        raw["source_request"],
        overrides={"sensual": 0, "fetish": 0, "creativity": creativity, "surreal": 0},
        seed=7,
    )
    raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, value in {
            "core": raw,
            "envelope": request,
            "controls": snapshot,
            "review": review(raw["baseline_prompt_en"]),
        }.items():
            path = Path(tmp) / (name + ".json")
            path.write_text(json.dumps(value, ensure_ascii=False))
            paths[name] = str(path)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "generate_photo_prompt.py"),
                "--seed",
                str(seed),
                "--authorial-core-json",
                paths["core"],
                "--request-envelope-json",
                paths["envelope"],
                "--creative-controls-json",
                paths["controls"],
                "--embodiment-review-json",
                paths["review"],
                *extra_args,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            raise AssertionError(result.stderr)
        return json.loads(result.stdout)[0]


def historical_freeze(evidence: Path) -> dict:
    """Validate archived evidence bytes without executing its retired runtime."""
    import json
    raw = (evidence / "frozen-inventory-queries.json").read_bytes()
    expected = (evidence / "frozen-sha256.txt").read_text().split()[0]
    assert hashlib.sha256(raw).hexdigest() == expected, "historical freeze changed"
    frozen = json.loads(raw)
    for name, digest in frozen["artifact_sha256"].items():
        original = evidence / name
        preserved = evidence / "preparation-revisions/pre-maintenance-binding" / name
        candidates = [original, preserved]
        assert any(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == digest
                   for p in candidates), "historical artifact changed: " + name
    return frozen


def historical_states(evidence: Path, frozen: dict) -> dict:
    """Read the frozen source delta; source hashes belong to that prior run."""
    import copy
    import gzip
    import json
    baseline = json.loads(gzip.decompress((evidence / "baseline-merged-data.json.gz").read_bytes()))
    states = {label: copy.deepcopy(baseline) for label in frozen["state_dictionary_hashes"]}
    for item in frozen["inventory"]:
        for label, data in states.items():
            rows = data["slots"][item["slot"]]
            position = next(i for i, row in enumerate(rows) if row["id"] == item["id"])
            assert rows[position] == item["before"]
            rows[position] = copy.deepcopy(item["before"] if label == "baseline"
                                          else item.get(label, item.get("proposal", item["before"])))
    return states


def bundle_meanings(bundles: list, *, within: list | None = None) -> list:
    """Compare authored meanings, optionally projecting a historical ID inventory.

    Projection keeps order and missing entries remain visible in the comparison;
    later optional bundles do not rewrite a frozen historical inventory.
    """
    if within is not None:
        historical_ids = {row['id'] for row in within}
        bundles = [row for row in bundles if row['id'] in historical_ids]
    return [{key: value for key, value in row.items() if key != "source_sha256"}
            for row in bundles]


def seduction_scope_delta() -> dict:
    """Read the sealed metadata delta; historical expected rows stay untouched."""
    import json
    path = ROOT / 'tests/fixtures/photo_prompt/seduction_expression_scope_delta.json'
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == 'd8fba33b9a40ac6bf190fb785fb001ab70582a0112f67ca4394f7301f25250a4'
    return json.loads(raw)


def seduction_historical_source_scope(data: dict) -> dict:
    """Reverse only ten exact metadata edits for an older source comparison."""
    import copy
    result = copy.deepcopy(data)
    for change in seduction_scope_delta()['metadata_rows']:
        row = next((r for r in result['slots'].get(change['slot'], [])
                    if r['id'] == change['id']), None)
        if row is None:
            continue  # The historical loader may exclude the owning extension.
        for field in change['changed_fields']:
            assert row.get(field) == change['after'].get(field), (change['id'], field)
            if field in change['before']:
                row[field] = copy.deepcopy(change['before'][field])
            else:
                row.pop(field, None)
    return result


def seduction_historical_bundles(bundles: list) -> list:
    """Reverse exact scoped member metadata, preserving every bundle duty."""
    import copy
    import json
    import photo_candidate_semantics as semantics
    policy = json.loads((ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json').read_text())['candidate_semantic_policy']
    changes = {(row['slot'], row['id']): row for row in seduction_scope_delta()['metadata_rows']}
    result = copy.deepcopy(bundles)
    for bundle in result:
        for member in bundle['member_candidates']:
            change = changes.get((member['slot'], member['entry_id']))
            if change is None:
                continue
            before = semantics.semantic_source(change['before'], member['slot'], policy)
            after = semantics.semantic_source(change['after'], member['slot'], policy)
            actual = {key: value for key, value in member.items() if key not in {'id', 'slot', 'entry_id'}}
            assert actual in (before, after), f'Unsealed bundle member change: {member["id"]}'
            for field in set(before) | set(after):
                if field in before:
                    member[field] = copy.deepcopy(before[field])
                else:
                    member.pop(field, None)
    return result


def project_slot_candidate(data: dict, slot: str, entry: dict) -> tuple[dict, dict]:
    """Exercise current public projection and lossless detail, without retrieval."""
    import copy
    import compose_pack_view as views
    import photo_candidate_semantics as semantics
    variant = dict(data, slots=dict(data["slots"]))
    variant["slots"][slot] = [entry if row["id"] == entry["id"] else row
                              for row in data["slots"][slot]]
    candidate, _ = prompt_generator.candidate_pack_summarize_slot_candidate(
        variant, slot, {"id": entry["id"], "applicability_status": "eligible"})
    projected = {"contract_version": "photo-candidate-pack/v6",
                 "slots": {slot: {"slot": slot, "candidates": [candidate]}}}
    prompt_generator.candidate_pack_project_candidate_surfaces(projected)
    semantics.apply_public_semantics(projected, {
        candidate["id"]: semantics.semantic_source(entry, slot, data["candidate_semantic_policy"])})
    prompt_generator.candidate_pack_recompute_id(projected)
    detail = views.build_view(projected, [candidate["id"]])
    views.verify_view(projected, detail)
    return candidate, detail
