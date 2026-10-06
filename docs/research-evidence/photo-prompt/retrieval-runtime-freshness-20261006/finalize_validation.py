"""Retain the completed discovery run and subsequent per-file repair results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
RUN = Path('/tmp/photo-freshness-full-isolated')
PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
REPAIRED_LOGS = {
    'test_photo_b5_guidance_boundary_history': '/tmp/photo-freshness-b5-repaired.log',
    'test_photo_cf40_source_boundary_history': '/tmp/photo-freshness-cf40-repaired.log',
    'test_photo_camera_evidence_structure': '/tmp/photo-freshness-camera-repaired.log',
    'test_photo_ct073_back_band_data': '/tmp/photo-freshness-ct073-data-repaired.log',
    'test_photo_ct073_boundary_history': '/tmp/photo-freshness-ct073-boundary-repaired.log',
    'test_photo_scene_budget_boundary_history': '/tmp/photo-freshness-scene-history-repaired.log',
    'test_photo_structure_boundary_history': '/tmp/photo-freshness-structure-history-repaired.log',
    'test_photo_v24_historical_fixture': '/tmp/photo-freshness-v24-history-repaired.log',
    'test_photo_visual_obligations': '/tmp/photo-freshness-visual-registry-repaired.log',
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    initial = read(RUN / 'RESULTS.json')
    discovery = read(RUN / 'DISCOVERY.json')
    if not initial['complete']:
        raise SystemExit('The discovery run is still running; no final result written.')
    records = [read(RUN / (name + '.json')) for name in discovery['modules']]
    failing = [row for row in records if row['failures'] or row['errors']]
    expected = {
        'test_photo_candidate_semantics',
        'test_photo_character_appearance_100',
        'test_photo_liminal_active_use_korean_data_cleanup',
    }
    if {row['module'] for row in failing} != expected:
        raise SystemExit('Unexpected remaining failure; inspect before finalizing.')
    freshness = next(row for row in records if row['module'] == 'test_photo_runtime_freshness')
    assert freshness['tests'] == 25 and not freshness['failures'] and not freshness['errors']
    repaired = [row['module'] for row in records if row != next(old for old in initial['results'] if old['module'] == row['module'])]
    failures = [item for row in records for item in row['failures']]
    errors = [item for row in records for item in row['errors']]
    methods = sorted({item['id'].split(' (', 1)[0] for item in failures + errors})
    summary = {
        'schema': 'photo-full-file-isolated-final-regression/v1',
        'complete': True,
        'all_tests_pass': False,
        'initial_discovery_tests': discovery['test_count'],
        'executed_tests_after_repairs': sum(row['tests'] for row in records),
        'module_count': len(records),
        'failure_events_including_subtests': len(failures),
        'error_events': len(errors),
        'remaining_failing_test_methods': methods,
        'remaining_failure_classification': 'Reproduced using original main code and original test expectations; see ORIGINAL-* evidence.',
        'repaired_modules': repaired,
        'results': records,
        'proof_boundary': 'Every discovered test file ran in an independent interpreter. Later corrected files were rerun; initial results are retained separately. The initial discovery preceded the added CURRENT relabel guard test. No completed single-process full-suite pass is claimed.',
    }
    destination = EVIDENCE / 'full-regressions'
    destination.mkdir(exist_ok=True)
    shutil.copy2(RUN / 'DISCOVERY.json', destination / 'DISCOVERY.json')
    shutil.copy2(RUN / 'RESULTS.json', destination / 'INITIAL-RESULTS.json')
    for module in discovery['modules']:
        shutil.copy2(RUN / (module + '.json'), destination / (module + '.json'))
        log = Path(REPAIRED_LOGS[module]) if module in REPAIRED_LOGS else RUN / (module + '.log')
        shutil.copy2(log, destination / (module + '.log'))
        if module in REPAIRED_LOGS:
            initial_logs = destination / 'initial-logs'
            initial_logs.mkdir(exist_ok=True)
            shutil.copy2(RUN / (module + '.log'), initial_logs / (module + '.log'))
    write(EVIDENCE / 'FULL-REGRESSIONS.json', summary)
    write(EVIDENCE / 'FRESHNESS-TESTS.json', freshness)
    owned = [
        'audit_composed_prompt.py', 'build_core_slot_index.py', 'build_semantic_index.py',
        'build_visual_profile_index.py', 'core_slot_index_storage.py', 'generate_photo_prompt.py',
        'photo_runtime_sources.py', 'photo_source_manifest.py', 'prompt_generator.py',
        'publish_photo_runtime_snapshot.py', 'sync_photo_runtime_source.py',
        'validate_photo_prompt_dictionary.py',
    ]
    validation = {
        'schema': 'photo-runtime-freshness-validation/v1',
        'runtime_applied_to_primary': True,
        'main_qualification_root': str(ROOT),
        'main_qualification_base': 'cb496c1db984f9fe5d632fa764aae4d3f6aedf63',
        'primary_final_source': read(EVIDENCE / 'PRIMARY-FINAL-SOURCE.json'),
        'freshness_tests': {'count': 25, 'failures': 0, 'errors': 0, 'evidence': 'FRESHNESS-TESTS.json'},
        'full_regressions': {key: value for key, value in summary.items() if key != 'results'},
        'equivalence': {'frozen_inputs': 24, 'slot_documents': 10088, 'full_index_and_public_packs_equal': True, 'evidence': 'EQUIVALENCE.json'},
        'primary_checks': {'dictionary': 'PASS', 'historical_loader_and_intellectual_tests': 36, 'camera_boundary_tests': 2, 'synthetic_registry_tests': 3, 'publisher_race_and_CURRENT_relabel_tests': 2},
        'primary_combined_run_note': 'The final 88-test combined run initially passed 87 tests and timed out at the process barrier under concurrent load. The wait budget was increased without changing assertions; the race and CURRENT guard reran successfully. All 25 lifecycle tests subsequently passed in the main qualification run.',
        'remote_proof_boundary': 'Real fresh fetch, commit observation and failure behavior were tested against a temporary Git remote. Full corpus publication was tested separately. No production-remote end-to-end run is claimed.',
        'main_V28_qualification_location': 'V28 assets, validator and retained V27 parent belong to the main qualification worktree. The older primary lineage retains its authored data with the new runtime; it is not relabeled V28.',
        'external_primary_commit_preserved': '199670d3d85c006d5d534e44394926404045942c',
        'commit_or_push_performed': False,
        'primary_runtime_script_sha256': {name: hashlib.sha256((PRIMARY / 'skills/photo-prompt-image-generator/scripts' / name).read_bytes()).hexdigest() for name in owned},
    }
    write(EVIDENCE / 'VALIDATION.json', validation)
    print(json.dumps({key: summary[key] for key in ('executed_tests_after_repairs', 'module_count', 'failure_events_including_subtests', 'error_events', 'remaining_failing_test_methods', 'repaired_modules')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
