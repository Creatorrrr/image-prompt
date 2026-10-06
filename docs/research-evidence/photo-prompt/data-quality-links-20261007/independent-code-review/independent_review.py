from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

PROJECT = Path('/Users/chasoik/.codex/worktrees/photo-data-quality-links/image-prompt')
ROOT = PROJECT / 'skills/photo-prompt-image-generator'
QA = Path('/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/code-review')
BASESTORE = QA.parents[1] / 'runtime-base'
sys.path.insert(0, os.environ.get('PHOTO_QA_IMPLEMENTATION', str(PROJECT)))
from tools.photo_data_maintenance.common import canonical, decode, digest, sha, code_binding
from tools.photo_data_maintenance.corpus import capture_draft, capture_generation
import tools.photo_data_maintenance.corpus as corpus_api
corpus_api.DEFAULT_ROOT = ROOT
from tools.photo_data_maintenance.links import build_links, query
from tools.photo_data_maintenance.report import write_report, load_report


def record(name, value):
    (QA / (name + '.json')).write_bytes(canonical(value))
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


def draft_copy(name):
    root = QA / name / 'skill'
    assets = root / 'assets'
    assets.mkdir(parents=True)
    registration = decode((ROOT / 'assets/photo_prompt_source_manifest.json').read_bytes())
    names = {'photo_prompt_source_manifest.json', 'photo_prompt_tags.json',
             'photo_prompt_visual_obligations.json', 'photo_prompt_quality_layers.json'}
    names.update(row['file'] for row in registration['sources'])
    for filename in names:
        origin = ROOT / 'assets' / filename
        if origin.is_file():
            shutil.copyfile(origin, assets / filename)
    return root


def baseline():
    generation = decode(next(BASESTORE.glob('local/*/CURRENT.json')).read_bytes())['generation_id']
    captured = capture_generation(ROOT, BASESTORE, generation)
    manifest = write_report(captured, QA / 'baseline-report')
    report = load_report(QA / 'baseline-report', require_links=True)
    # Decode authored references independently. No use of build_links to form expected edges.
    expected = set()
    entry_slots = {}
    bundles = []
    refs_valid = True
    for filename, raw in captured['source_files'].items():
        value = decode(raw) if raw is not None else {}
        for slot, rows in (value.get('slots') or {}).items():
            for row in rows:
                entry_slots.setdefault(row['id'], []).append(slot)
        bundles.extend(value.get('visual_semantics') or [])
    for bundle in bundles:
        bid = 'bundle:' + bundle['id']
        for member in bundle['candidate_ids']:
            scoped = (bundle.get('candidate_slots') or {}).get(member)
            matches = [slot for slot in entry_slots.get(member, []) if scoped is None or slot == scoped]
            assert len(matches) == 1, (bid, member, matches)
            expected.add(('slot:' + matches[0] + ':' + member, 'member_of', bid))
        for profile in [*(bundle.get('hard_profile_ids') or []), *([bundle['hard_profile_id']] if bundle.get('hard_profile_id') else [])]:
            expected.add((bid, 'associated_with', 'profile:' + profile))
    actual = {(edge['source'], edge['type'], edge['target']) for edge in report['links']['edges']}
    assert expected == actual, {'missing': sorted(expected-actual), 'extra': sorted(actual-expected)}
    cquery = query(report['inventory'], report['links'], 'slot:light_shape:lit_clean_vertical_catchlight_pair')
    pquery = query(report['inventory'], report['links'], 'profile:clamshell_dual_source_portrait_light')
    cpaths = {tuple(row['nodes']) for row in cquery['paths']}
    ppaths = {tuple(row['nodes']) for row in pquery['paths']}
    expected_path = ('slot:light_shape:lit_clean_vertical_catchlight_pair', 'bundle:clean_beauty_clamshell', 'profile:clamshell_dual_source_portrait_light')
    assert expected_path in cpaths and expected_path in ppaths
    record('baseline-results', {
        'code_binding': code_binding(), 'generation_id': generation,
        'counts': report['inventory']['counts'], 'edge_count': len(actual),
        'source_edge_independent_comparison': 'pass', 'clamshell_bidirectional': 'pass',
        'bundle_count': len(bundles), 'finding_counts': manifest['findings_count'],
        'report_id': manifest['report_id'], 'report_directory': str(QA/'baseline-report')})


def draft_quality_race():
    root = draft_copy('draft-quality-race')
    layer = root / 'assets/photo_prompt_quality_layers.json'
    before_sha = sha(layer.read_bytes())
    def change_quality():
        layer.write_bytes(b'{"invalid_quality_policy":true}')
    try:
        result = capture_draft(root, runtime_store=QA/'draft-quality-race/runtime', after_capture=change_quality)
    except ValueError as exc:
        record('draft-quality-race-results', {
            'source_quality_changed': sha(layer.read_bytes()) != before_sha,
            'capture_error': str(exc), 'capture_did_not_raise': False,
            'before_quality_sha256': before_sha, 'after_quality_sha256': sha(layer.read_bytes()),
            'report_created': (QA/'draft-quality-race/report').exists(), 'code_binding': code_binding()})
        return
    manifest = write_report(result, QA/'draft-quality-race/report')
    record('draft-quality-race-results', {
        'source_quality_changed': sha(layer.read_bytes()) != before_sha,
        'source_quality_archived': 'photo_prompt_quality_layers.json' in result['source_files'],
        'capture_did_not_raise': True,
        'validation_status': manifest['validation_status'],
        'errors': manifest['findings_count']['error'],
        'before_quality_sha256': before_sha, 'after_quality_sha256': sha(layer.read_bytes()),
        'source_fingerprint': result['binding']['source_fingerprint'], 'code_binding': code_binding()})


def draft_bad_semantics():
    root = draft_copy('draft-bad-semantics')
    profile_path = root / 'assets/photo_prompt_visual_obligations.json'
    value = decode(profile_path.read_bytes())
    value['profiles'][0]['semantics'] = 'unfinished draft semantics'
    profile_path.write_bytes(canonical(value))
    cmd = [sys.executable, str(PROJECT/'tools/photo_data_maintenance/cli.py'), 'audit',
           '--source-root', str(root), '--runtime-store', str(QA/'draft-bad-semantics/runtime'),
           '--output', str(QA/'draft-bad-semantics/report')]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    (QA/'draft-bad-semantics/cli.stdout').write_text(completed.stdout)
    (QA/'draft-bad-semantics/cli.stderr').write_text(completed.stderr)
    record('draft-bad-semantics-results', {
        'returncode': completed.returncode, 'report_created': (QA/'draft-bad-semantics/report').exists(),
        'stderr_tail': completed.stderr[-3500:], 'command': cmd, 'code_binding': code_binding()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['baseline', 'draft-quality-race', 'draft-bad-semantics'])
    parser.add_argument('--version')
    args = parser.parse_args()
    mode = args.mode
    if args.version:
        QA = QA / args.version
    QA.mkdir(parents=True, exist_ok=True)
    {'baseline': baseline, 'draft-quality-race': draft_quality_race,
     'draft-bad-semantics': draft_bad_semantics}[mode]()
