from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

QA = Path('/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/code-review')
PROJECT = Path('/Users/chasoik/.codex/worktrees/photo-data-quality-links/image-prompt')
ROOT = PROJECT/'skills/photo-prompt-image-generator'
RUN = QA/'final-json-fixtures'
sys.path.insert(0, str(PROJECT))
from tools.photo_data_maintenance.common import MaintenanceError, canonical, code_binding, decode, sha
from tools.photo_data_maintenance.corpus import capture_draft
from tools.photo_data_maintenance.report import load_report


def fixture(name, slot_value=None, bad_semantics=False, bad_quality=False):
    directory = RUN/name
    root = directory/'skill'
    assets = root/'assets'
    assets.mkdir(parents=True)
    profile = decode((ROOT/'assets/photo_prompt_visual_obligations.json').read_bytes())
    profile['profiles'] = profile['profiles'][:1]
    if bad_semantics:
        profile['profiles'][0]['semantics'] = 'unfinished'
    slots = {'prop': [{'id': 'fixture_box', 'en': 'a small local box'}]} if slot_value is None else slot_value
    payloads = {
        'photo_prompt_source_manifest.json': {
            'contract_version': 'photo-source-manifest/v1',
            'sources': [{'file': 'photo_prompt_optional_extension.json', 'kind': 'candidate',
                         'required': False, 'load_order': 0}]},
        'photo_prompt_tags.json': {'slots': slots},
        'photo_prompt_visual_obligations.json': profile,
        'photo_prompt_quality_layers.json': [] if bad_quality else {'quality_policy_probe': 'version-A'},
    }
    raw = {}
    for filename, data in payloads.items():
        raw[filename] = (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode()
        (assets/filename).write_bytes(raw[filename])
    return root, raw


def audit_case(name, **kwargs):
    root, inputs = fixture(name, **kwargs)
    directory = root.parent
    command = [sys.executable, str(PROJECT/'tools/photo_data_maintenance/cli.py'), 'audit',
               '--source-root', str(root), '--runtime-store', str(directory/'runtime'),
               '--output', str(directory/'report')]
    completed = subprocess.run(command, capture_output=True, text=True)
    (directory/'cli.stdout').write_text(completed.stdout)
    (directory/'cli.stderr').write_text(completed.stderr)
    assert completed.returncode == 1, (name, completed.returncode, completed.stdout, completed.stderr)
    assert 'Traceback' not in completed.stderr and 'Traceback' not in completed.stdout, (name, completed.stderr)
    assert (directory/'report/manifest.json').is_file(), (name, completed.stderr)
    report = load_report(directory/'report')
    manifest = report['manifest']
    assert manifest['validation_status'] == 'invalid', (name, manifest['validation_status'])
    assert manifest['binding']['input_mode'] == 'draft' and manifest['binding']['generation_id'] is None
    assert report['links'] is None
    assert manifest['findings_count']['error'] > 0
    for filename, raw in inputs.items():
        archived = directory/'report/inputs'/filename
        assert archived.read_bytes() == raw, (name, filename)
        assert manifest['files']['inputs/'+filename] == sha(raw), (name, filename)
    if 'slot_value' in kwargs:
        assert any(row['rule']=='source_records_invalid' and row['details'].get('field')=='photo_prompt_tags.json'
                   for row in report['findings']), (name, report['findings'])
    if kwargs.get('bad_semantics'):
        assert any(row['kind']=='profile' and row['record']['semantics']=='unfinished' for row in report['inventory']['nodes'])
    if kwargs.get('bad_quality'):
        assert any(row['rule']=='source_json_invalid' and row['details'].get('field')=='photo_prompt_quality_layers.json'
                   for row in report['findings']), (name, report['findings'])
    result = {'case':name, 'exit_code':completed.returncode, 'validation_status':manifest['validation_status'],
              'error_count':manifest['findings_count']['error'], 'traceback':False,
              'all_input_raw_bytes_archived':True,'input_manifest_checksums_match':True,
              'draft_not_queryable':report['links'] is None,
              'fixture_json_bytes':sum(map(len,inputs.values())),
              'rules':sorted({row['rule'] for row in report['findings']}),
              'report_directory':str(directory/'report'), 'stdout_log':str(directory/'cli.stdout'),
              'stderr_log':str(directory/'cli.stderr')}
    (QA/('final-'+name+'-results.json')).write_bytes(canonical(result))
    return result


def quality_capture_check():
    root, inputs = fixture('quality-capture')
    directory = root.parent
    original = inputs['photo_prompt_quality_layers.json']
    stable = capture_draft(root, runtime_store=directory/'runtime')
    assert stable['source_files']['photo_prompt_quality_layers.json']==original
    source = root/'assets/photo_prompt_quality_layers.json'
    capture_error = None
    try:
        capture_draft(root, runtime_store=directory/'runtime',
                      after_capture=lambda:source.write_bytes(b'{"quality_policy_probe":"version-B"}\n'))
    except MaintenanceError as exc:
        capture_error = str(exc)
    assert capture_error and capture_error.startswith('capture_changed:'), capture_error
    result = {'case':'quality-capture','quality_input_collected_byte_exact':True,
              'capture_changed_detected':True,'capture_error':capture_error,
              'fixture_directory':str(directory)}
    (QA/'final-quality-capture-results.json').write_bytes(canonical(result))
    return result


def main():
    before = code_binding()
    results = [audit_case('slots-empty-array',slot_value=[]),
               audit_case('slots-string',slot_value='unfinished'),
               audit_case('semantics-string',bad_semantics=True),
               audit_case('quality-invalid-type',bad_quality=True),
               quality_capture_check()]
    assert before == code_binding(), 'Implementation changed while validating'
    summary = {'result':'pass', 'cases':results,'code_binding':before,
               'scope':'Local JSON draft regression only; no runtime publication or external calls.'}
    (QA/'final-json-regressions-results.json').write_bytes(canonical(summary))
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
