"""Capture only the canonical shared corpus, with native reference identities."""
from __future__ import annotations
import importlib
import subprocess
import sys
from pathlib import Path
from .common import MaintenanceError, decode, digest, finding, sha

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = PROJECT / 'skills/photo-prompt-image-generator'

def runtime(root: Path):
    code_root = Path(root).resolve()
    if not (code_root / 'scripts/photo_candidate_corpus.py').is_file():
        code_root = DEFAULT_ROOT
    directory = str(code_root / 'scripts')
    if directory not in sys.path:
        sys.path.insert(0, directory)
    rt = importlib.import_module('photo_runtime_sources')
    if rt.code_inventory(code_root) != rt.LOADED_CODE:
        raise MaintenanceError('runtime_restart_required', 'native implementation changed on disk')
    return rt, importlib.import_module('photo_candidate_corpus'), importlib.import_module('photo_candidate_sources')

def observation(root: Path) -> dict:
    def git(*args):
        try:
            return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    return {'source_root': str(root.resolve()), 'commit_observed': git('rev-parse', 'HEAD'),
            'dirty_observed': bool(git('status', '--porcelain', '--untracked-files=no'))}

def _scan(root, c, source_api):
    inventory = source_api.SourceInventory.load(root / 'assets')
    names = {c.MANIFEST_NAME: 'registration', **dict(inventory.rows)}
    paths = {name: root / 'assets' / name for name in names}
    if any(p.is_symlink() for p in paths.values()):
        raise MaintenanceError('source_symlink', 'native source must be a regular owned file')
    return {name: p.read_bytes() for name, p in paths.items()}

def make_inventory(corpus, raw):
    refs = {}
    for filename, content in raw.items():
        module = decode(content)
        if 'candidates' not in module:
            continue
        for identifier in module.get('candidates', {}):
            refs[identifier] = [{'file': filename, 'pointer': '/candidates/' + identifier}]
    bindings = {}
    for row in corpus['slot_bindings'].values():
        bindings.setdefault(row['candidate_id'], []).append(row)
    nodes = []
    kinds = {'visual_option': 'candidate', 'visual_profile': 'profile', 'visual_bundle': 'bundle'}
    for identifier, authored in sorted(corpus['candidates'].items()):
        record = {'id': identifier, **authored['content'], 'conditions': authored['conditions'], 'effects': authored['effects'],
                  'record_kind': authored['record_kind'], 'provenance': authored['provenance'],
                  'role_bindings': sorted(bindings.get(identifier, []), key=lambda r: r['id'])}
        node = {'id': identifier, 'kind': kinds.get(authored['record_kind'], authored['record_kind']),
                'slot': None, 'record': record, 'source_refs': refs.get(identifier, [])}
        node['entity_sha256'] = digest([node['kind'], None, record])
        nodes.append(node)
    return {'schema': 'photo-data-inventory/v2', 'nodes': nodes,
            'counts': {kind: sum(n['kind'] == kind for n in nodes) for kind in sorted({n['kind'] for n in nodes})}}

def capture_draft(root: Path, *, runtime_store: Path | None = None, after_capture=None) -> dict:
    root = root.resolve()
    rt, c, source_api = runtime(root)
    revision_path = rt.SnapshotPublisher(root, runtime_store).directory / 'SOURCE.json'
    revision = decode(revision_path.read_bytes()) if revision_path.is_file() else None
    raw = _scan(root, c, source_api)
    corpus = c.load(root / 'assets')
    c.validate(corpus)
    if after_capture:
        after_capture()
    if raw != _scan(root, c, source_api) or revision != (decode(revision_path.read_bytes()) if revision_path.is_file() else None):
        raise MaintenanceError('capture_changed', 'native source changed during capture')
    runtime(root)
    return {'inventory': make_inventory(corpus, raw), 'findings': [], 'source_files': raw,
            'binding': {'input_mode': 'draft', **observation(root), 'generation_id': None,
                        'cooperative_revision': revision, 'editing_pending': bool((revision or {}).get('editing')),
                        'source_fingerprint': digest({name: sha(value) for name, value in raw.items()}),
                        'source_manifest_sha256': sha(raw[c.MANIFEST_NAME])}}

def capture_generation(root: Path, store: Path, generation: str) -> dict:
    rt, c, source_api = runtime(root)
    snapshot = rt.RuntimeSnapshotProvider(root, store).load_generation(generation, independent_audit=True)
    raw = _scan(snapshot.root, c, source_api)
    from photo_shared_views import source
    return {'inventory': make_inventory(source(snapshot.data), raw), 'findings': [], 'source_files': raw,
            'binding': {'input_mode': 'generation', **observation(root), 'generation_id': generation,
                        'source_fingerprint': snapshot.manifest['source_fingerprint'],
                        'source_manifest_sha256': sha(raw[c.MANIFEST_NAME]),
                        'runtime_algorithm_sha256': snapshot.manifest['algorithm_sha256']}}

def current_generation(root: Path, store: Path):
    rt, _, _ = runtime(root)
    return rt.RuntimeSnapshotProvider(root, store).acquire(bootstrap=False)
