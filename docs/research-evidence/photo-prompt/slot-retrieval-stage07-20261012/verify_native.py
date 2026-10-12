"""Frozen native-script requests through the real public candidate-pack CLI."""
import argparse
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--lane', required=True)
    parser.add_argument('--expect-after', action='store_true')
    parser.add_argument('--default-store', action='store_true')
    parser.add_argument('--runtime-store', type=Path)
    parser.add_argument('--only', action='append')
    args = parser.parse_args()
    skill = args.root / 'skills/photo-prompt-image-generator'
    sys.path.insert(0, str(skill / 'scripts'))
    import prompt_generator as g
    import audit_composed_prompt as audit
    from photo_runtime_sources import RuntimeSnapshotProvider, default_store
    fixtures = args.root / 'tests/fixtures/photo_prompt/native_alias_v1'
    rows = json.loads((OUT / 'CASES-FROZEN.json').read_text())
    if args.only:
        rows = [row for row in rows if row['key'] in args.only]
    identities = {row['native_alias']: row['source_candidates'][0]
                  for row in json.loads((OUT / 'EXPECTATIONS.json').read_text())}
    store = args.runtime_store or (Path(default_store()) if args.default_store else OUT / (args.lane + '-runtime-store'))
    snapshot = RuntimeSnapshotProvider(skill, store).acquire()
    destination = OUT / args.lane
    destination.mkdir(exist_ok=True)

    def run(row):
        start = time.monotonic()
        key = row['key']
        directory = destination / key
        directory.mkdir(exist_ok=True)
        path = fixtures / key / 'fixture.json'
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['fixture_sha256']:
            raise RuntimeError('frozen fixture changed: ' + key)
        values = json.loads(path.read_text())
        for name, source in [('request-envelope', 'request_envelope_input'),
                ('authorial-core', 'authorial_core_input'), ('creative-controls', 'creative_controls'),
                ('embodiment-review', 'embodiment_review')]:
            save(directory / (name + '.json'), values[source])
        command = [str(PYTHON), str(skill / 'scripts/generate_photo_prompt.py')]
        for name in ['request-envelope', 'authorial-core', 'creative-controls', 'embodiment-review']:
            command += ['--' + name + '-json', str(directory / (name + '.json'))]
        command += ['--new-author-camera-evidence', '--seed', '17', '--runtime-store', str(store),
                    '--output-file', str(directory / 'candidate-pack.json')]
        save(directory / 'generate-command.json', command)
        result = subprocess.run(command, cwd=args.root, capture_output=True, text=True)
        (directory / 'generate.log').write_text(result.stdout + result.stderr)
        identity = identities[row['native_alias']]
        summary = dict(key=key, mode=row['mode'], native_alias=row['native_alias'],
            target=identity['document_id'], exit_code=result.returncode, failures=[],
            seconds=round(time.monotonic() - start, 2))
        if result.returncode:
            summary['failures'].append('public_cli_failed')
            summary['error'] = result.stderr or result.stdout
            return summary
        pack = json.loads((directory / 'candidate-pack.json').read_text())[0]
        summary.update(target_hit=any(candidate['id'] == identity['document_id']
            for info in pack['slots'].values() for candidate in info['candidates']),
            target_rank=next((i + 1 for i, candidate in enumerate(
                pack['slots'].get(identity['slot'], {}).get('candidates', []))
                if candidate['id'] == identity['document_id']), None),
            slot_ids={slot: [candidate['entry_id'] for candidate in info['candidates']]
                for slot, info in pack['slots'].items()},
            authorial_core_sha256=pack['authorial_core']['canonical_sha256'],
            generation_id=snapshot.generation_id,
            recomputation_issues=audit.audit_core_retrieval(pack, snapshot.data))
        for slot, info in pack['slots'].items():
            if len(info['candidates']) > g.candidate_pack_slot_limit(slot):
                summary['failures'].append('slot_cap_changed')
        if sum(len(info['candidates']) for info in pack['slots'].values()) > 64:
            summary['failures'].append('global_cap_changed')
        tampered = copy.deepcopy(pack)
        slot = next(iter(tampered['slots']))
        tampered['slots'][slot]['candidates'].pop()
        summary['omission_detected'] = bool(audit.audit_core_retrieval(tampered, snapshot.data))
        view = subprocess.run([str(PYTHON), str(skill / 'scripts/compose_pack_view.py'),
            '--pack', str(directory / 'candidate-pack.json'), '--output', str(directory / 'composer-view.json')],
            cwd=args.root, capture_output=True, text=True)
        (directory / 'view.log').write_text(view.stdout + view.stderr)
        summary['view_exit_code'] = view.returncode
        if summary['authorial_core_sha256'] != row['authorial_core_sha256']:
            summary['failures'].append('frozen_core_binding')
        if summary['recomputation_issues'] or not summary['omission_detected'] or view.returncode:
            summary['failures'].append('recomputation_or_view')
        if args.expect_after and summary['target_hit'] != (row['mode'] == 'positive'):
            summary['failures'].append('expected_candidate_presence')
        if row['category'] == 'object' and 'costume_style' in pack['slots']:
            summary['failures'].append('human_clothing_on_printed_card')
        return summary

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run, rows):
            results.append(result)
            save(OUT / (args.lane + '-cases.json'), results)
            print(json.dumps({key: result[key] for key in ['key', 'exit_code', 'target_hit', 'target_rank', 'failures']
                if key in result}, ensure_ascii=False), flush=True)
    save(OUT / (args.lane + '-runtime.json'), dict(generation_id=snapshot.generation_id,
        source_fingerprint=snapshot.manifest['source_fingerprint'], sealed_root=str(snapshot.root)))
    failures = [result['key'] for result in results if result['failures']]
    print(json.dumps(dict(cases=len(results), positive_hits=sum(bool(result.get('target_hit'))
        for result in results if result['mode'] == 'positive'),
        adjacent_false_hits=sum(bool(result.get('target_hit')) for result in results if result['mode'] != 'positive'),
        failures=failures)), flush=True)
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
