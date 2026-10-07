from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

QA = Path('/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/code-review')
PROJECT = Path('/Users/chasoik/.codex/worktrees/photo-data-quality-links/image-prompt')
ROOT = PROJECT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(PROJECT))
from tools.photo_data_maintenance.common import canonical, decode, sha, code_binding, MaintenanceError
from tools.photo_data_maintenance.corpus import capture_draft
from tools.photo_data_maintenance.report import write_report, load_report


def fixture(name, malformed_semantics=False):
    root = QA/'small-fixtures'/name/'skill'
    assets = root/'assets'
    assets.mkdir(parents=True)
    registry = decode((ROOT/'assets/photo_prompt_visual_obligations.json').read_bytes())
    registry['profiles'] = registry['profiles'][:1]
    if malformed_semantics:
        registry['profiles'][0]['semantics'] = 'unfinished draft semantics'
    payloads = {
        'photo_prompt_source_manifest.json': {
            'contract_version': 'photo-source-manifest/v1',
            'sources': [{'file': 'photo_prompt_optional_extension.json', 'kind': 'candidate',
                         'required': False, 'load_order': 0}]},
        'photo_prompt_tags.json': {'slots': {'prop': [{'id': 'small_fixture', 'en': 'a small local box'}]}},
        'photo_prompt_visual_obligations.json': registry,
        'photo_prompt_quality_layers.json': {'quality_policy_probe': 'version-A'},
    }
    for name, value in payloads.items():
        (assets/name).write_bytes(canonical(value))
    return root


def main():
    quality_root = fixture('quality')
    work = quality_root.parent
    source = quality_root/'assets/photo_prompt_quality_layers.json'
    original_raw = source.read_bytes()
    stable = capture_draft(quality_root, runtime_store=work/'runtime')
    assert stable['source_files']['photo_prompt_quality_layers.json'] == original_raw
    manifest = write_report(stable, work/'stable-report')
    archived = work/'stable-report/inputs/photo_prompt_quality_layers.json'
    assert archived.read_bytes() == original_raw
    assert manifest['files']['inputs/photo_prompt_quality_layers.json'] == sha(original_raw)
    load_report(work/'stable-report')
    capture_error = None
    try:
        capture_draft(quality_root, runtime_store=work/'runtime',
                      after_capture=lambda: source.write_bytes(canonical({'quality_policy_probe': 'version-B'})))
    except MaintenanceError as exc:
        capture_error = str(exc)
    assert capture_error and capture_error.startswith('capture_changed:'), capture_error
    quality_result = {'input_archived_byte_exact': True, 'manifest_input_checksum_matches': True,
                      'capture_changed_detected': True, 'capture_error': capture_error,
                      'stable_report_validation_status': manifest['validation_status'],
                      'fixture_json_bytes': sum(path.stat().st_size for path in quality_root.glob('assets/*.json')),
                      'report_path': str(work/'stable-report')}
    (QA/'small-quality-results.json').write_bytes(canonical(quality_result))

    semantics_root = fixture('semantics', malformed_semantics=True)
    work = semantics_root.parent
    command = [sys.executable, str(PROJECT/'tools/photo_data_maintenance/cli.py'), 'audit',
               '--source-root', str(semantics_root), '--runtime-store', str(work/'runtime'),
               '--output', str(work/'report')]
    run = subprocess.run(command, capture_output=True, text=True)
    (work/'cli.stdout').write_text(run.stdout)
    (work/'cli.stderr').write_text(run.stderr)
    assert run.returncode == 1, run.returncode
    assert 'Traceback' not in run.stderr, run.stderr
    report = load_report(work/'report')
    assert report['manifest']['validation_status'] == 'invalid'
    profile = next(row for row in report['inventory']['nodes'] if row['kind'] == 'profile')
    assert profile['record']['semantics'] == 'unfinished draft semantics'
    assert any(row['severity'] == 'error' for row in report['findings'])
    assert any(row['rule'] == 'authored_contract_invalid' for row in report['findings'])
    semantics_result = {'cli_exit_code': run.returncode, 'traceback': False,
                        'report_preserved': True, 'invalid_diagnosis_preserved': True,
                        'malformed_semantics_preserved': profile['record']['semantics'],
                        'error_count': report['manifest']['findings_count']['error'],
                        'fixture_json_bytes': sum(path.stat().st_size for path in semantics_root.glob('assets/*.json')),
                        'report_path': str(work/'report'), 'stdout_path': str(work/'cli.stdout'),
                        'stderr_path': str(work/'cli.stderr')}
    (QA/'small-semantics-results.json').write_bytes(canonical(semantics_result))
    all_results = {'quality_policy': quality_result, 'malformed_semantics': semantics_result,
                   'code_binding': code_binding()}
    (QA/'small-regressions-results.json').write_bytes(canonical(all_results))
    print(json.dumps(all_results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
