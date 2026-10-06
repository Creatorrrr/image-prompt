"""Read-only bundle verification; optional source-only cleaning preflight.

Default mode imports no project code and performs no normalization or retrieval.
The optional preflight mode has not been replay-tested for this bundle.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def canonical(obj):
    return sha_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def undo(obj, delta, pointer_key):
    pieces = delta[pointer_key].strip('/').split('/')
    parent = obj
    for part in pieces[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    key = int(pieces[-1]) if isinstance(parent, list) else pieces[-1]
    assert parent[key] == delta['after'], delta
    parent[key] = delta['before']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True, help='Checkout at the exact pinned commit')
    ap.add_argument('--preflight', action='store_true', help='Explicitly run eight source-only normalizations; no retrieval')
    args = ap.parse_args()
    bundle = Path(__file__).resolve().parent
    repo = args.repo.resolve()
    manifest = load(bundle / 'manifest.json')
    actual = {str(p.relative_to(bundle)) for p in bundle.rglob('*') if p.is_file()}
    assert actual == set(manifest['files']) | {'manifest.json'}, 'Unexpected or missing bundle files'
    for name, expected in manifest['files'].items():
        p = bundle / name
        assert p.stat().st_size == expected['bytes'] and sha(p) == expected['sha256'], name
        if p.suffix == '.json':
            load(p)
    assert len(actual) == manifest['total_files_including_manifest']
    assert sum((bundle / name).stat().st_size for name in actual) == manifest['total_bytes_including_manifest']
    source = load(bundle / 'source-pin.json')
    head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    assert head == source['commit'], 'Source commit mismatch'
    food_pin = load(bundle / 'food/source-pin.json')
    hashes = {food_pin['base'] + '/' + name: value for name, value in food_pin['files'].items()}
    hashes.update(source['additional_files_sha256'])
    for name, expected in hashes.items():
        assert sha(repo / name) == expected, name
    fm = load(bundle / 'food/manifest.json')
    for name, expected in fm['files'].items():
        p = bundle / 'food' / name
        assert sha(p) == expected['sha256'] and p.stat().st_size == expected['bytes'], name
    assert sha(bundle / 'food/manifest.json') == source['food_package_manifest_sha256']
    adapter = load(bundle / 'cleaning/adapter-provenance.json')
    preflight = load(bundle / 'cleaning/preflight-receipt.json')
    states = {x['case_id']: x for x in adapter['states']}
    for c in preflight['cases']:
        cid = c['case_id']
        directory = bundle / 'cleaning/inputs' / cid
        for name, binding in c['input_hashes'].items():
            assert sha(directory / name) == binding['final_sha256'], (cid, name)
        core = load(directory / 'authorial_core.json')
        assert canonical(core) == states[cid]['adapter_v2']['core_canonical_sha256']
        env = load(directory / 'request_envelope.json')
        raw = (directory / 'request.raw.txt').read_text()
        assert env['request_text'] == raw, cid
        for delta in reversed(adapter['adapter_v2']['deltas']):
            if delta['case_id'] == cid:
                undo(core, delta, 'core_json_pointer')
        assert canonical(core) == states[cid]['adapter_v1']['core_canonical_sha256']
        for delta in reversed(adapter['adapter_v1']['deltas']):
            if delta['case_id'] == cid:
                undo(core, delta, 'json_pointer')
        assert canonical(core) == states[cid]['original']['core_canonical_sha256']
        reconstructed_bytes = (json.dumps(core, ensure_ascii=False, indent=2) + '\n').encode()
        assert sha_bytes(reconstructed_bytes) == states[cid]['original']['core_file_sha256'], cid
    verdict = load(bundle / 'cleaning/verdict.json')
    semantic = load(bundle / 'cleaning/semantic-review.json')
    counts = {}
    for case in semantic['cases']:
        for row in case['rows'].values():
            key = row['scene_classification']
            counts[key] = counts.get(key, 0) + 1
    assert counts == verdict['scene_classification_counts']
    assert len(verdict['pairings']) == 16
    assert len(preflight['attempts']) == 13 and len(preflight['cases']) == 8
    assert sum(p['pure_property_path_check'] for p in verdict['pairings']) == 16
    assert all(p['dimensions_not_open'] == ['relationship'] and not p['all_declared_dimensions_open'] for p in verdict['pairings'])
    print(json.dumps({'verification': 'PASS', 'files': len(actual), 'bytes': manifest['total_bytes_including_manifest'], 'source_files_checked': len(hashes), 'project_code_imported': False, 'semantic_reruns': 0}))
    if not args.preflight:
        return
    assert sys.version_info[:3] == (3, 12, 14), 'Historical source preflight used CPython 3.12.14'
    sys.dont_write_bytecode = True
    approved_sources = {(repo / name).resolve() for name in hashes if name.endswith('.py')}
    approved_inputs = {(bundle / name).resolve() for name in manifest['files'] if name.startswith('cleaning/inputs/')}
    stdlib = Path(sysconfig.get_path('stdlib')).resolve()
    stdlib_dynamic = stdlib / 'lib-dynload'

    def guard(event, values):
        if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn')) or event in {'os.system', 'os.putenv', 'os.unsetenv'}:
            raise RuntimeError('Optional source preflight forbids network, processes and environment changes')
        if event != 'open' or not values or isinstance(values[0], int):
            return
        p = Path(os.fsdecode(values[0])).resolve()
        mode = values[1] if len(values) > 1 else 'r'
        flags = values[2] if len(values) > 2 else 0
        if (isinstance(mode, str) and any(x in mode for x in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)):
            raise PermissionError('Source preflight is read-only')
        if p in approved_sources or p in approved_inputs:
            return
        if stdlib in p.parents and not any(x in p.parts for x in ('site-packages', 'dist-packages')):
            return
        if stdlib_dynamic in p.parents:
            return
        raise PermissionError('Source preflight denied an unsealed or non-source file read')

    # The same default verification above has already checked every imported source hash.
    # PermissionError on bytecode probes permits fallback to the approved .py source.
    sys.addaudithook(guard)
    sys.path.insert(0, str(repo / food_pin['base'] / 'scripts'))
    import prompt_generator as generator
    from photo_camera_evidence import camera_authoring_declaration, require_camera_evidence
    results = []
    for c in preflight['cases']:
        directory = bundle / 'cleaning/inputs' / c['case_id']
        envelope = generator.load_request_envelope_arg(str(directory / 'request_envelope.json'))
        controls = load(directory / 'creative_controls.json')
        core = generator.load_authorial_core_arg(str(directory / 'authorial_core.json'), request_envelope=envelope, creative_control_snapshot=controls)
        require_camera_evidence(core, c['required_camera_axes'])
        lock = core['intent_lock']
        camera = camera_authoring_declaration(core, required='camera' in set(lock['locked_dimensions']) | set(lock['open_dimensions']))
        generator.photo_embodiment.build_policy(core, load(directory / 'embodiment_review.json'))
        assert core['canonical_sha256'] == c['latest_normalized_core_sha256'], c['case_id']
        assert camera == c['latest_camera_declaration'], c['case_id']
        results.append({'case_id': c['case_id'], 'normalized_core_sha256': core['canonical_sha256'], 'passed': True})
    print(json.dumps({'source_only_preflight': results, 'retrieval_calls': 0, 'api_calls': 0, 'writes': 0}))


if __name__ == '__main__':
    main()
