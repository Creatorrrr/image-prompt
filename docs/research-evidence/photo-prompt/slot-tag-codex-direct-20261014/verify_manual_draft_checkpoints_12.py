"""Freeze 685 further disjoint worker-read drafts, without native approval."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('checkpoint10_helpers', HERE / 'verify_manual_draft_checkpoints_10_R02.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
h = old.helpers

seen = set()
for number in ['01', '02', '03', '04-R02', '05', '06', '07', '08', '09', '10', '11']:
    report = json.loads((HERE / f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())
    for row in report['coverage']:
        interval = set(range(*row['range']))
        assert not seen & interval
        seen |= interval
assert len(seen) == 6715

specifications = [
    ('/root/review_12250_13000', r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json', 9425, 9525),
    ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 3100, 3250),
    ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 6050, 6150),
    ('/root/review_08250_09250', r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json', 6845, 6915),
    ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 7505, 7570),
    ('/root/review_06250_07250', r'native_06250_08250_09250\.(\d{5})_(\d{5})\.json', 8750, 8950),
]
coverage, added = [], set()
for task, pattern, start, stop in specifications:
    local, notes, boundaries = set(), [], []
    for note in sorted(h.NOTES.iterdir()):
        match = re.fullmatch(pattern, note.name)
        if not match:
            continue
        first, last = map(int, match.groups())
        if task == '/root/review_12250_13000' and (first, last) in {(9400, 9425), (9450, 9475)}:
            continue
        trimmed_aggregate = task == '/root/review_12250_13000' and (first, last, start) == (9400, 9450, 9425)
        if not (first < stop and last > start and last <= stop and (first >= start or trimmed_aggregate)):
            continue
        interval = set(range(max(first, start), min(last, stop)))
        assert not local & interval, (task, note.name)
        local |= interval
        value = json.loads(note.read_bytes())
        h.add(note)
        if task == '/root/review_12250_13000':
            for row in value['artifacts']:
                assert set(row) in [{'path', 'sha256'}, {'path', 'raw_sha256'}]
                h.add(h.rootpath(row['path']), row.get('raw_sha256', row.get('sha256')))
            old.pin_nested_artifacts(value)
        elif task == '/root/review_06250_07250':
            old.pin_nested_artifacts(value)
        elif task == '/root/review_08250_09250' and value.get('artifacts'):
            for name, row in value['artifacts'].items():
                h.add(h.rootpath(name), row['raw_sha256'])
        else:
            old.previous.pin_note(note, task)
        notes.append(str(note.relative_to(ROOT)))
        boundaries.append({'note_range': [first, last], 'counted_range': [max(first, start), min(last, stop)]})
    assert local == set(range(start, stop)), (task, sorted(set(range(start, stop)) - local))
    assert not (seen | added) & local
    added |= local
    coverage.append({'task': task, 'range': [start, stop], 'worker_attested_unique_source_reads': len(local),
                     'notes': notes, 'exact_count_boundaries': boundaries})
assert len(added) == 685 and len(seen | added) == 7400

plan = ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'
h.paths[str(plan.relative_to(ROOT))] = hashlib.sha256(plan.read_bytes()).hexdigest()
h.add(Path(__file__))
report = {
    'schema': 'photo-root-manual-draft-checkpoint-verification/v1', 'actor': '/root',
    'previous_checkpoint': 'ROOT-MANUAL-DRAFT-CHECKPOINT-11.json',
    'previous_disjoint_draft_candidates': 6715, 'coverage': coverage,
    'worker_attested_additional_unique_source_reads': 685,
    'cumulative_disjoint_native_draft_candidates': 7400, 'files': dict(sorted(h.paths.items())),
    'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
    'historical_ranges_exactly_disjoint': True, 'root_all_sources_personally_read_claimed': False,
    'source_corrections_or_new_role_decisions_accepted': False,
    'formal_native_proof_count_for_these_draft_ranges': 0,
    'operational_native_qualified_count': 0, 'canonical_changed': False,
    'fresh06250_read_boundary': '200 whole original/current/exact5B/own-binding/closure and current5B-after direct reads with manual drafts; new authored source-after reads0, formal0.',
    'catalog_boundary': 'Notes keep exact earlier and149 research inputs and actual reading provenance. No automatic catalog-hash, source or proof conversion.',
    'known_unapproved_boundaries': [
        '9400:9450 aggregate counts only new9425:9450; its earlier first25 and9450:9475 partial are not counted twice.',
        '8948 literal-amendment01 corrects quote overreach without overwriting its frozen original draft.',
        '3159 staging_degree classification requires the recorded immutable correction; shape PASS is not semantic approval.',
        'Footwear/sock scope and existing-source application proposals are unselected pending root semantic review.',
        'Candidate1299 remains pending: a proposed physical handoff restriction has not closed every actual framing receiver.',
        'Prepared packets, mutable buffers and partial native-proof checkpoints are excluded from these counts.',
        'Whole-source worker reading, syntax and hashes do not establish final tag truth or operating native qualification.',
    ], 'gemini_calls': 0, 'network_calls': 0,
}
output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-12.json'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
with output.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
names = sorted(set(h.paths) | {str(output.relative_to(ROOT))})
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= set(names)
for name in names:
    assert subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT) == (ROOT / name).read_bytes(), name
print(json.dumps({'files': len(names), 'additional_direct_drafts': 685, 'cumulative': 7400, 'native_approvals': 0}))
