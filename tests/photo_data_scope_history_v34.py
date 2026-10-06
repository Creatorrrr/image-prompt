"""Authenticated V34 merge boundary with independent upstream/local V33 replay."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path('docs/research-evidence/photo-prompt/data-quality-links-main-merge-20261007/history')
PROOF = BASE / 'V34-DATA-SCOPE-PROOF.json'
PROOF_SHA256 = '8ae1ae029becb12da5e742bd929b197d1a25497176f884e4fc90d67b9517d98d'
SOURCES = {
    'v32': ('SOURCE-V32.json', '585286017c217454dbf7ac6d4533c6ba8a02fe9be9475ce04e5c53321b64102a',
            '96e20422316276a4e0b5ed97f44152e4931e7504', 'ae809d09bc01042c15b77271764036871d28949d', 1377, 2609717339),
    'local-v33': ('SOURCE-LOCAL-V33.json', '118fa37945753eb99e9038eac2e6c1b4b3af6c60f4b951e0f0308b584ebb054d',
                  'd9dc3df7012f395c48d536ee9df80df060cd24f9', '0cc7030343555d5d05461255853dcd46fafd0a85', 1426, 2721602508),
    'upstream-v33': ('SOURCE-UPSTREAM-V33.json', '655eb68641abb736a1a8096fee6a84e0daf05d625074881a398412bf0b045b05',
                     'c4c0e4ed25981fc46c09de6e138247b5788ea43c', 'a101f732a007b65450fb621de0f333e4eb854fb5', 1422, 2729499412),
}
PHOTO = Path('skills/photo-prompt-image-generator/assets')
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')
DATA = frozenset((PHOTO / name).as_posix() for name in (
    'photo_prompt_photorealism_elements_extension.json', 'photo_prompt_realistic_background_extension.json',
    'photo_prompt_visual_obligations.json'))
INDEX = frozenset((PHOTO / name).as_posix() for name in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'))
RECOVERY = DATA | INDEX | {(PHOTO / 'photo_prompt_source_manifest.json').as_posix()}


def _fixtures():
    from tests import photo_prompt_fixtures
    return photo_prompt_fixtures


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode())


def source_manifest(stage, root):
    filename, expected_sha, pin, tree, count, size = SOURCES[stage]
    f = _fixtures()
    raw = f._v24_regular_path(root, (BASE / filename).as_posix()).read_bytes()
    if digest(raw) != expected_sha:
        raise AssertionError('Frozen ' + stage + ' original source manifest drift')
    manifest = json.loads(raw)
    rows = manifest.get('members') or []
    if (manifest.get('schema') != 'photo-merge-history-source/v1' or manifest.get('stage') != stage
            or manifest.get('source_pin') != pin or manifest.get('source_tree') != tree
            or manifest.get('member_count') != len(rows) or len(rows) != count
            or manifest.get('total_member_bytes') != size):
        raise AssertionError('Frozen ' + stage + ' original inventory drift')
    paths, backings = set(), {}
    for row in rows:
        name = f._v17_safe_path(row['path']).as_posix()
        source = f._v17_safe_path(row['source_path']).as_posix()
        identity = tuple(row.get(k) for k in ('git_blob', 'mode', 'bytes', 'sha256'))
        if (name in paths or row.get('git_commit') != pin or row.get('git_path') != name
                or row.get('mode') not in ('100644', '100755') or type(row.get('bytes')) is not int
                or row['bytes'] < 0 or not isinstance(row.get('sha256'), str) or len(row['sha256']) != 64
                or not isinstance(row.get('git_blob'), str) or len(row['git_blob']) != 40
                or any(c not in '0123456789abcdef' for c in row['sha256'] + row['git_blob'])
                or (source in backings and backings[source] != identity)):
            raise AssertionError('Frozen ' + stage + ' source provenance drift')
        paths.add(name)
        backings[source] = identity
    if (sum(r['bytes'] for r in rows) != size
            or any(p.as_posix() in paths for name in paths for p in Path(name).parents)
            or any(p.as_posix() in backings for name in backings for p in Path(name).parents)):
        raise AssertionError('Frozen ' + stage + ' source path overlap drift')
    return manifest


def exact_payload(root, row):
    path = _fixtures()._v24_regular_path(root, row['source_path'])
    raw = path.read_bytes()
    git_blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    if (path.stat().st_mode & 0o7777 != int(row['mode'][-3:], 8) or len(raw) != row['bytes']
            or digest(raw) != row['sha256'] or git_blob != row['git_blob']):
        raise AssertionError('Frozen merge original source payload or mode drift: ' + row['path'])
    return raw


def context(root):
    return any((root / p).exists() or (root / p).is_symlink() for p in (
        PROOF, BASE / SOURCES['upstream-v33'][0], ILLUSTRATION / 'assets/photo_regression_baseline_v34.json'))


def transition(root):
    raw = _fixtures()._v24_regular_path(root, PROOF.as_posix()).read_bytes()
    if digest(raw) != PROOF_SHA256:
        raise AssertionError('Frozen V34 DATA scope proof drift')
    proof = json.loads(raw)
    parent = source_manifest('upstream-v33', root)
    if (proof.get('schema') != 'photo-data-scope-transition/v34'
            or proof.get('previous_qualified_commit') != SOURCES['upstream-v33'][2]
            or proof.get('previous_qualified_tree') != SOURCES['upstream-v33'][3]
            or proof.get('parent_manifest_sha256') != SOURCES['upstream-v33'][1]
            or proof.get('parent_manifest') != (BASE / SOURCES['upstream-v33'][0]).as_posix()
            or proof.get('parent_member_count') != parent['member_count']
            or set(proof.get('preserved_source_paths') or []) != DATA | INDEX):
        raise AssertionError('Frozen V34 DATA scope lineage drift')
    local = source_manifest('local-v33', root)
    local_proof = 'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/V33-DATA-SCOPE-PROOF.json'
    if proof.get('parallel_local_qualification') != {
            'source_pin': SOURCES['local-v33'][2],
            'source_manifest': (BASE / SOURCES['local-v33'][0]).as_posix(),
            'source_manifest_sha256': SOURCES['local-v33'][1],
            'original_pack_sha256': 'd6f893dfeecad5968ba80db4e44689c09f99ab16f4b4aa6ae9b88fcc84a6e525',
            'original_proof': local_proof,
            'original_proof_sha256': 'ece1b90ed71faa5f1f12d29bddf674ffa300cfcd6da1283782c534dbe01fa3d6'}:
        raise AssertionError('Frozen V34 parallel local qualification lineage drift')
    row = next(r for r in local['members'] if r['path'] == local_proof)
    if digest(exact_payload(root, row)) != proof['parallel_local_qualification']['original_proof_sha256']:
        raise AssertionError('Frozen V34 parallel local qualification proof drift')
    return proof, parent


def previous_path(root, name, supplied=None):
    live = _fixtures()._v24_regular_path(root, name)
    if not context(root) or name not in RECOVERY:
        return live
    proof, _ = transition(root)
    manifest = source_manifest('v32', root)
    row = next(r for r in manifest['members'] if r['path'] == name)
    current = live.read_bytes()
    if (digest(current) != proof['source_files_after'][name]
            or live.stat().st_mode & 0o7777 != int(row['mode'][-3:], 8)):
        raise AssertionError('Frozen V34 retained live source payload or mode drift: ' + name)
    original = exact_payload(root, row)
    if supplied is not None and digest(supplied) not in {digest(current), digest(original)}:
        raise AssertionError('Frozen V34 supplied source payload drift: ' + name)
    return _fixtures()._v24_regular_path(root, row['source_path'])


def previous_payload(root, name, current):
    if not context(root) or name not in RECOVERY:
        return current
    return previous_path(root, name, current).read_bytes()


def materialize(stage, directory, *, source_root, link_verified=False):
    f = _fixtures()
    f._v24_empty_destination(directory)
    manifest = source_manifest(stage, source_root)
    for row in manifest['members']:
        exact_payload(source_root, row)
    directory.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.sealed-' + stage + '-', dir=directory.parent) as temporary:
        staged = Path(temporary) / 'tree'
        staged.mkdir()
        for row in manifest['members']:
            raw = exact_payload(source_root, row)
            target = staged / f._v17_safe_path(row['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            if link_verified:
                os.link(f._v24_regular_path(source_root, row['source_path']), target)
            else:
                target.write_bytes(raw)
                target.chmod(int(row['mode'][-3:], 8))
        f._v24_empty_destination(directory)
        staged.replace(directory)
    return manifest


def resolve_python(stage, root):
    expected = source_manifest(stage, root)['environment']
    configured = os.environ.get('PHOTO_V32_PYTHON' if stage == 'v32' else 'PHOTO_HISTORY_PYTHON')
    candidates = [configured] if configured else [sys.executable,
        str(Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'),
        shutil.which('python3.' + str(expected['python'][1]))]
    probe = "import json,sys,unicodedata; print(json.dumps({'implementation':sys.implementation.name,'python':list(sys.version_info[:3]),'unicode':unicodedata.unidata_version}))"
    for candidate in dict.fromkeys(p for p in candidates if p):
        try:
            result = subprocess.run([candidate, '-c', probe], capture_output=True, text=True, timeout=10, check=True)
            if json.loads(result.stdout) == expected:
                return Path(candidate).absolute(), expected
        except (OSError, ValueError, subprocess.SubprocessError):
            continue
    raise AssertionError('Exact ' + stage + ' Python/Unicode environment unavailable: ' + json.dumps(expected))


def replay(stage, directory, *, source_root, test_module=None, log_name=None):
    python, expected = resolve_python(stage, source_root)
    executable = directory / '.venv/bin/python'
    executable.parent.mkdir(parents=True, exist_ok=True)
    executable.symlink_to(python)
    environment = os.environ.copy()
    environment['GEMINI_API_KEY'] = ''
    environment['GOOGLE_API_KEY'] = ''
    # Original V33 tests select their nested V32 interpreter independently.
    environment.pop('PHOTO_HISTORY_PYTHON', None)
    with tempfile.TemporaryDirectory(prefix='photo-original-runtime-') as store:
        environment['PHOTO_RUNTIME_STORE'] = store
        setup = "import sys; sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish()"
        prepared = subprocess.run([str(python), '-c', setup], cwd=directory, env=environment,
                                  capture_output=True, text=True, timeout=300)
        if prepared.returncode:
            raise AssertionError('Original publisher failed: ' + prepared.stderr)
        if test_module:
            command = [str(python), '-m', 'unittest', test_module, '-v']
        else:
            version = 32 if stage == 'v32' else 33
            code = "import json,sys; from pathlib import Path; sys.path.insert(0,'skills/subculture-illustration-image-generator/scripts'); import validate_illustration_assets as v; print(json.dumps(v.validate_photo_regression_baseline(Path('skills/subculture-illustration-image-generator/assets'),baseline_version=" + str(version) + ")))"
            command = [str(python), '-c', code]
        result = subprocess.run(command, cwd=directory, env=environment, capture_output=True, text=True, timeout=900)
    if log_name:
        (source_root / BASE / log_name).write_text(result.stdout + result.stderr)
        (source_root / BASE / (log_name + '.environment.json')).write_text(json.dumps({
            'stage': stage, 'python': str(python), 'required_and_probed_environment': expected,
            'source_pin': SOURCES[stage][2], 'source_manifest_sha256': SOURCES[stage][1]}, indent=2) + '\n')
    if result.returncode:
        raise AssertionError('Original ' + stage + ' replay failed: ' + result.stdout + result.stderr)
    if not test_module:
        return json.loads(result.stdout.strip().splitlines()[-1])
    return result


def _apply(value, changes, require):
    for row in changes:
        parent = value
        parts = [p.replace('~1', '/').replace('~0', '~') for p in row['pointer'].split('/')[1:]]
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if row['operation'] == 'add':
            require(key not in parent and 'before' not in row, 'photo V34 added leaf already existed')
        else:
            require(row['operation'] == 'replace' and parent[key] == row['before'], 'photo V34 predecessor leaf drift')
        parent[key] = row['after']


def qualify_current(v, asset_dir, root, baseline, pack, raw, receipt=None):
    require = v._require
    try:
        proof, parent = transition(root)
    except (AssertionError, OSError, ValueError) as exc:
        require(False, str(exc))
    require(baseline.get('data_scope_transition') == {
        'evidence_path': PROOF.as_posix(), 'evidence_sha256': PROOF_SHA256,
        'previous_qualified_commit': SOURCES['upstream-v33'][2],
        'parent_manifest_sha256': SOURCES['upstream-v33'][1]}, 'photo V34 successor lineage drift')
    old_raw = (asset_dir / 'photo_regression_baseline_v33_pack.json').read_bytes()
    require(v._sha256(asset_dir / 'photo_regression_baseline_v33.json') == proof['previous_manifest_sha256']
        and digest(old_raw) == proof['previous_pack_sha256'] and digest(raw) == proof['current_pack_sha256'] == baseline['sha256']
        and raw == (asset_dir / 'photo_regression_baseline_v34_pack.json').read_bytes()
        and json.loads(raw) == [pack] and pack['pack_id'] == proof['current_pack_id'], 'photo V34 frozen pack bytes drift')
    pointers = ['/0/core_retrieval/canonical_sha256', '/0/core_retrieval/slot_corpus_sha256',
                '/0/pack_id', '/0/provenance/tags_hash', '/0/slots/motion/candidate_count']
    changes = proof['reviewed_pack_delta']
    require([r['pointer'] for r in changes] == pointers and all(r['operation'] == 'replace' for r in changes)
            and changes[-1]['before'] == 34 and changes[-1]['after'] == 33, 'photo V34 unregistered pack scope delta')
    expected = json.loads(old_raw)
    _apply(expected, changes, require)
    require(expected == [pack], 'photo V34 changed palette candidates, order, scene or hard duties')
    old_proof = json.loads(_fixtures()._v24_regular_path(root, proof['upstream_proof']).read_bytes())
    require(v._sha256(root / proof['upstream_proof']) == proof['upstream_proof_sha256'] == '9fe462ebda03f4dedb4038390f8d4b56929bd19157562d32f34b7529f9010eb0', 'photo V34 upstream V33 proof drift')
    inventory = {p.name: v._sha256(_fixtures()._v24_regular_path(root, p.relative_to(root).as_posix())) for p in (root / PHOTO).glob('*.json')}
    require(inventory == proof['source_inventory_after'] and set(inventory) == set(old_proof['source_inventory_after'])
            and set(proof['source_files_after']) == set(old_proof['source_files_after'])
            and all(inventory[n] == s for n, s in old_proof['source_inventory_after'].items() if (PHOTO / n).as_posix() not in DATA | INDEX)
            and all(proof['source_files_after'][n] == s for n, s in old_proof['source_files_after'].items() if n not in DATA | INDEX), 'photo V34 unreviewed palette, registration, DATA or runtime changed')
    for group in ('evidence_files', 'source_files_after', 'active_shards_after', 'retained_shards_before'):
        require(all(v._sha256(_fixtures()._v24_regular_path(root, n)) == s for n, s in proof[group].items()), 'photo V34 source, shard or evidence drift: ' + group)
    require(proof['retained_shards_before'] == old_proof['active_shards_after'], 'photo V34 original palette shard inventory drift')
    require(baseline['frozen_inputs'] == old_proof['frozen_inputs'] == proof['frozen_inputs']
        and all(v._sha256(root / n) == s for n, s in proof['frozen_inputs'].items())
        and v._public_photo_candidate_count(pack) == 64, 'photo V34 frozen scene or public count drift')
    originals = {}
    descriptor = (ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').as_posix()
    for row in parent['members']:
        payload = exact_payload(root, row)
        if row['path'] in DATA | {descriptor}:
            originals[row['path']] = payload
    allowed = {
        (PHOTO / 'photo_prompt_photorealism_elements_extension.json').as_posix(): ['/maintenance_ref/record_id', '/maintenance_ref/sha256', '/slots/platform_framing/0/for_any', '/slots/platform_framing/0/kind'],
        (PHOTO / 'photo_prompt_realistic_background_extension.json').as_posix(): ['/maintenance_ref/record_id', '/maintenance_ref/sha256', '/slots/motion/1/for_any', '/slots/motion/1/kind'],
        (PHOTO / 'photo_prompt_visual_obligations.json').as_posix(): ['/profiles/114/activation/exclude_if_any_terms', '/profiles/114/activation/hard_activation'],
    }
    require(set(proof['source_leaf_delta']) == set(allowed), 'photo V34 source scope inventory drift')
    require(proof.get('authored_delta_counts') == {'add': 6, 'replace': 4}
        and sum(r['operation'] == 'add' for rows in proof['source_leaf_delta'].values() for r in rows) == 6
        and sum(r['operation'] == 'replace' for rows in proof['source_leaf_delta'].values() for r in rows) == 4,
        'photo V34 scope/reference change count drift')
    for name, changes in proof['source_leaf_delta'].items():
        before = json.loads(originals[name])
        require([r['pointer'] for r in changes] == allowed[name]
            and all(r['operation'] == ('replace' if r['pointer'].startswith('/maintenance_ref/') else 'add') for r in changes),
            'photo V34 unregistered authored scope or maintenance leaf')
        if name.endswith('photo_prompt_visual_obligations.json'):
            require(before['profiles'][114]['id'] == 'cello_endpin_seated_bowed'
                and changes[1]['after']['contract_version'] == 'photo-visual-hard-activation/v1'
                and [g['id'] for g in changes[1]['after']['required_any_groups']] == ['cello_instrument', 'active_bowing', 'seated_support'], 'photo V34 cello activation scope drift')
        else:
            slot, index, identity = ('platform_framing', 0, 'pr_casual_crop_subject_legibility_candidate') if 'photorealism' in name else ('motion', 1, 'rb_shared_wind_response_candidate')
            require(before['slots'][slot][index]['id'] == identity
                and all(r['after'] == ['human'] for r in changes if r['operation'] == 'add'), 'photo V34 human candidate scope drift')
        _apply(before, changes, require)
        require(json.loads((root / name).read_bytes()) == before, 'photo V34 unreviewed source meaning changed')
    maintenance = proof.get('maintenance_scope_corrections') or {}
    extensions = DATA - {(PHOTO / 'photo_prompt_visual_obligations.json').as_posix()}
    require(set(maintenance) == extensions, 'photo V34 maintenance correction inventory drift')
    local = source_manifest('local-v33', root)
    local_records = {row['path']: row for row in local['members']}
    for name, row in maintenance.items():
        before = json.loads(originals[name])
        scoped = json.loads(exact_payload(root, local_records[name]))
        current = json.loads((root / name).read_bytes())
        old_ref, scoped_ref, new_ref = before.pop('maintenance_ref'), scoped.pop('maintenance_ref'), current.pop('maintenance_ref')
        directory = 'docs/research-evidence/photo-prompt/extension-maintenance/'
        require(row['previous_reference'] == old_ref == scoped_ref and row['current_reference'] == new_ref
            and row['previous_record_path'] == directory + old_ref['record_id'] + '.json'
            and row['current_record_path'] == directory + new_ref['record_id'] + '.json'
            and set(new_ref) == {'contract_version', 'record_id', 'sha256'}
            and new_ref['contract_version'] == old_ref['contract_version'] == 'photo-extension-maintenance-ref/v1'
            and new_ref['record_id'] != old_ref['record_id'], 'photo V34 maintenance reference lineage drift')
        old_raw = _fixtures()._v24_regular_path(root, row['previous_record_path']).read_bytes()
        new_raw = _fixtures()._v24_regular_path(root, row['current_record_path']).read_bytes()
        old_record, new_record = json.loads(old_raw), json.loads(new_raw)
        require(digest(old_raw) == row['previous_record_sha256'] and digest(new_raw) == row['current_record_sha256']
            and canonical_digest(old_record) == old_ref['sha256'] and canonical_digest(new_record) == new_ref['sha256']
            and old_record['record_id'] == old_ref['record_id'] and new_record['record_id'] == new_ref['record_id']
            and canonical_digest(before) == row['original_body_sha256'] == old_record['authored_source_sha256']
            and canonical_digest(current) == canonical_digest(scoped) == row['scoped_body_sha256'] == new_record['authored_source_sha256']
            and current == scoped and local_records[name]['sha256'] == row['scoped_source_raw_sha256'],
            'photo V34 maintenance record or authored body digest drift')
        changes = row['reviewed_record_delta']
        require([r['pointer'] for r in changes] == ['/authored_source_sha256', '/maintenance_only/source_revision/scope_correction', '/record_id']
            and [r['operation'] for r in changes] == ['replace', 'add', 'replace'], 'photo V34 unreviewed maintenance record delta')
        expected = json.loads(old_raw)
        _apply(expected, changes, require)
        require(expected == new_record, 'photo V34 maintenance evidence changed beyond versioned scope binding')
        correction = new_record['maintenance_only']['source_revision']['scope_correction']
        slot, identity = ('platform_framing', 'pr_casual_crop_subject_legibility_candidate') if 'photorealism' in name else ('motion', 'rb_shared_wind_response_candidate')
        require(correction['schema'] == 'photo-maintenance-scope-correction/v1'
            and correction['previous_maintenance_ref'] == old_ref
            and correction['previous_record_raw_sha256'] == row['previous_record_sha256']
            and correction['previous_scoped_source_raw_sha256'] == row['scoped_source_raw_sha256']
            and correction['candidate'] == {'slot': slot, 'id': identity, 'kind': ['human'], 'for_any': ['human']},
            'photo V34 maintenance scope correction lineage drift')
    old_descriptor = originals[descriptor]
    old_hash = proof['previous_validator_sha256'].encode()
    require(digest(old_descriptor) == proof['previous_universal_descriptor_sha256'] and old_descriptor.count(old_hash) == 1
        and (root / descriptor).read_bytes() == old_descriptor.replace(old_hash, v._sha256(Path(v.__file__)).encode(), 1), 'photo V34 universal descriptor changed beyond validator binding')
    if receipt is not None:
        require(all(receipt.get(k) == proof[k] for k in ('generation_id', 'source_fingerprint', 'algorithm_sha256')), 'photo V34 receipt source generation drift')
        from photo_runtime_sources import RuntimeSnapshotProvider
        RuntimeSnapshotProvider().from_receipt(pack, receipt)
