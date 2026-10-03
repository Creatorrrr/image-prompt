"""Bind authored sources, native attempts and complete regression results."""
from __future__ import annotations

import ast
import hashlib
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def corpus_receipt():
    sys.path.insert(0, str(SKILL / 'scripts'))
    import prompt_generator as pg
    data = pg.load_runtime_data()
    registry = data[pg.VISUAL_OBLIGATIONS_DATA_KEY]
    index = read(SKILL / 'assets/photo_prompt_semantic_index.json')
    paths = sorted((SKILL / 'assets').glob('*.json'))
    paths += sorted((SKILL / 'scripts').glob('*.py'))
    paths += sorted((SKILL / 'precore').glob('*.json'))
    paths += sorted((SKILL / 'precore').glob('*.py'))
    shards = []
    for descriptor in index['shards']:
        shard = SKILL / 'assets' / descriptor['path']
        assert digest(shard) == descriptor['sha256'], shard
        shards.append(shard)
    paths += shards
    baseline = ROOT / 'skills/subculture-illustration-image-generator/assets'
    historical = {}
    import subprocess
    for version in range(1, 8):
        path = baseline / f'photo_regression_baseline_v{version}.json'
        before = subprocess.check_output(['git', 'show', f'HEAD:{path.relative_to(ROOT)}'], cwd=ROOT)
        assert path.read_bytes() == before, path
        historical[str(path.relative_to(ROOT))] = digest(path)
    old = read(baseline / 'photo_regression_baseline_v7.json')
    for name, expected in old['frozen_inputs'].items():
        path = ROOT / name
        assert digest(path) == expected, name
        historical[name] = expected
    paths += [baseline / 'photo_regression_baseline_v8.json',
              baseline / 'universal_scene_baseline_v2.json',
              baseline.parent / 'scripts/validate_illustration_assets.py']
    receipt = {
        'schema_version': 'photo-slang-final-corpus-receipt/v1',
        'stage': 'after all native calls and eligibility/legacy-fixture repairs',
        'native_source_is_this_corpus': False,
        'native_source_receipt': 'qualified-inputs.json',
        'native_source_archive': 'native-data-snapshot.tar.gz',
        'profiles': len(registry['profiles']),
        'slot_candidates': sum(len(rows) for rows in data['slots'].values()),
        'semantic_index_entries': index['entry_count'],
        'semantic_provider': index['provider'],
        'embedding_model': index['embedding_model'],
        'embedding_dimensions': index['embedding_dimensions'],
        'current_semantic_shards': len(shards),
        'files': {str(path.relative_to(ROOT)): digest(path) for path in paths},
        'immutable_history_and_inputs': historical,
        'pixel_qualification_claim': 'None. Source/index integrity is separate from native pixel qualification.',
    }
    write(HERE / 'FINAL-CORPUS-RECEIPT.json', receipt)
    return receipt


def native_receipt():
    configurations = [
        (1, 1, '12f41bac0560d57b', 'attempt-1/native.png', 'prompt.txt',
         'attempt-1/composed_prompt.json', 'attempt-1/native_args.json',
         'attempt-1/composed_audit.json', 'attempt-1/render_request_audit.json'),
        (2, 1, '73a136f24792ce74', 'native_attempt_1.png', 'prompt.en.txt',
         'composed_prompt.json', 'native_args.json',
         'composed_audit.json', 'render_request_audit.json'),
        (2, 2, 'fc913eab5a125801', 'native_attempt_2.png', 'prompt.retry1.en.txt',
         'composed_prompt.retry1.json', 'native_args.retry1.json',
         'composed_audit.retry1.json', 'render_request_audit.retry1.json'),
        (3, 1, '73b4a398bd884f7c', 'native-attempt-1.png', 'prompt.txt',
         'composed_prompt.json', 'native_args.json',
         'composed_audit.json', 'render_request_audit.json'),
        (3, 2, '4f217a3d5607589f', 'native-attempt-2.png', 'final_prompt.txt',
         'composed_prompt.retry.json', 'native_args.retry.json',
         'composed_audit.retry.json', 'render_request_audit.retry.json'),
    ]
    wanted = {row[2] for row in configurations}
    shared = [json.loads(line) for line in (ROOT / 'runs/image_runs.ndjson').read_text().splitlines()]
    shared = [row for row in shared if row.get('run_id') in wanted]
    assert len(shared) == 5 and {row['run_id'] for row in shared} == wanted
    shared = {row['run_id']: row for row in shared}
    review = read(HERE / 'ROOT-PIXEL-REVIEW.json')
    reviewed = {(row['arm'], row['attempt']): row for row in review['attempts']}
    reference_hash = digest(HERE / 'reference-photo.jpg')
    attempts = []
    for arm, attempt, run_id, image_name, prompt_name, composition_name, args_name, ca_name, ra_name in configurations:
        folder = HERE / f'tests/agent-{arm}'
        image, prompt = folder / image_name, folder / prompt_name
        composed = read(folder / composition_name)
        args = read(folder / args_name)
        pack = read(folder / 'candidate_pack.json')[0]
        ledger = shared[run_id]
        own = [json.loads(line) for line in (folder / 'image_runs.ndjson').read_text().splitlines()]
        own = [row for row in own if row['run_id'] == run_id]
        assert len(own) == 1 and own[0] == ledger, run_id
        assert ledger['status'] == 'success'
        assert ledger['tool'] == 'image_gen.imagegen' and ledger['generation_environment'] == 'codex_native'
        assert ledger['image_paths'] == [str(image)]
        assert ledger['reference_sha256'] == [reference_hash]
        assert ledger['prompt_en'] == composed['prompt_en']
        assert prompt.read_text().removesuffix('\n') == composed['prompt_en']
        assert ledger['negative_en'] == composed['negative_en']
        assert ledger['pack_id'] == composed['pack_id'] == pack['pack_id']
        assert ledger['authorial_core_sha256'] == pack['authorial_core']['canonical_sha256']
        assert ledger['intent_lock_sha256'] == pack['authorial_core']['intent_lock']['canonical_sha256']
        assert args['referenced_image_paths'] and all(digest(Path(p)) == reference_hash for p in args['referenced_image_paths'])
        runtime_name = ('runtime_prompt.txt' if arm == 1 else
                        'runtime_prompt.en.txt' if arm == 2 and attempt == 1 else
                        'runtime_prompt.retry1.en.txt' if arm == 2 else
                        'runtime_prompt.txt' if attempt == 1 else 'runtime_prompt.retry.txt')
        runtime = folder / runtime_name
        assert runtime.read_text().removesuffix('\n') == args['prompt']
        for name in (ca_name, ra_name):
            audit = read(folder / name)
            assert audit['status'] == 'pass' and not audit.get('failures'), name
        expected = reviewed[(f'agent-{arm}', attempt)]
        assert digest(image) == expected['sha256'], image
        raw = image.read_bytes()
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        dimensions = list(struct.unpack('>II', raw[16:24]))
        assert dimensions == [1237, 1272]
        paths = [image, prompt, runtime, folder / composition_name, folder / args_name,
                 folder / ca_name, folder / ra_name, folder / 'candidate_pack.json',
                 folder / 'authorial_core.json', folder / 'request_envelope.json',
                 folder / 'creative_controls.json', folder / 'embodiment_review.json']
        attempts.append({
            'arm': f'agent-{arm}', 'attempt': attempt, 'run_id': run_id,
            'pack_id': pack['pack_id'], 'dimensions': dimensions,
            'positive_prompt_body_sha256': hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),
            'runtime_prompt_body_sha256': hashlib.sha256(args['prompt'].encode()).hexdigest(),
            'verdict': expected['verdict'],
            'files_sha256': {str(p.relative_to(HERE)): digest(p) for p in paths},
            'ledger_binding_verified': True, 'audits_passed': True,
        })
    archive = read(HERE / 'native-data-archive-receipt.json')
    assert digest(HERE / 'native-data-snapshot.tar.gz') == archive['sha256']
    assert archive['all_member_hashes_match'] is True
    result = {
        'schema_version': 'photo-slang-native-integrity/v1',
        'native_call_count': 5, 'arms': 3, 'original_pack_count': 3,
        'native_image_model_id': None,
        'native_model_disclosure': 'The built-in tool returned no specific image model identifier.',
        'reference_sha256': reference_hash, 'attempts': attempts,
        'latest_arm_verdicts': review['latest_arm_verdicts'],
        'partial_is_fail': True, 'user_acceptance': 'not_yet_received',
        'source_archive_hash_verified': True,
        'source_snapshot_note': 'Native attempts retain the earlier complete source snapshot. Current candidate exposure fixes are a separate retrieval replay with zero image calls.',
    }
    write(HERE / 'NATIVE-INTEGRITY.json', result)
    return result


def regression_receipt():
    full = read(HERE / 'final/FULL-SUITE-RESULT.json')
    assert full['complete'], 'Full sweep is still running'
    results = []
    original = sorted((HERE / 'final').glob('full-suite-worker-*.json'))
    for path in original:
        row = read(path)
        if row['modules'] == ['tests.test_photo_visual_obligations']:
            path = HERE / 'final-repair/full-suite-worker-1.json'
            row = read(path)
        assert row['complete'] and row['successful'], path
        assert not row['failures'] and not row['errors'], path
        results.append((path, row))
    expected = {f'tests.{p.stem}' for p in (ROOT / 'tests').glob('test*.py')}
    actual = [module for path, row in results for module in row['modules']]
    assert len(actual) == len(set(actual)) and set(actual) == expected
    modules = {}
    authored = 0
    for path, row in results:
        for module in row['modules']:
            source = ROOT / (module.replace('.', '/') + '.py')
            count = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_')
                        for n in ast.walk(ast.parse(source.read_text())))
            authored += count
            modules[module] = {'source_sha256': digest(source),
                               'result_path': str(path.relative_to(HERE)),
                               'result_sha256': digest(path), 'tests_run': row['tests_run']}
    result = {
        'schema_version': 'photo-slang-complete-verification/v1',
        'successful': True, 'modules': len(modules),
        'authored_test_methods': authored,
        'tests_run': sum(row['tests_run'] for path, row in results),
        'failures': [], 'errors': [],
        'skipped': [item for path, row in results for item in row['skipped']],
        'coverage': 'Every discovered test module has a complete successful result. After the stable-corpus sweep, only the failed test module was rerun in full following explicit scope setup repairs. No runtime, authored data, index or frozen expected fixture was changed during or after that sweep.',
        'initial_sweep_retained': 'FULL-SUITE-RESULT.json',
        'stable_corpus_sweep_retained': 'final/FULL-SUITE-RESULT.json',
        'repaired_module': 'tests.test_photo_visual_obligations',
        'module_results': modules,
    }
    write(HERE / 'VERIFICATION-RESULT.json', result)
    return result


if __name__ == '__main__':
    corpus = corpus_receipt()
    native = native_receipt()
    regression = regression_receipt()
    print(json.dumps({'profiles': corpus['profiles'], 'slot_candidates': corpus['slot_candidates'],
                      'native_calls': native['native_call_count'],
                      'verified_tests': regression['tests_run'], 'modules': regression['modules'],
                      'successful': regression['successful']}))
