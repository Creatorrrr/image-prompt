"""Preserve610 newly frozen disjoint manual drafts; confer no qualification.

The exact root-selected ranges below are workers' direct-read attestations,
not a count inferred from prepared files, hashes, or proof-shaped JSON.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('checkpoint06_primitives', HERE / 'verify_manual_draft_checkpoints_06.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
helpers = previous.helpers


def pin_nested_artifacts(value):
    if isinstance(value, dict):
        if isinstance(value.get('file'), str):
            expected = value.get('file_sha256', value.get('raw_sha256'))
            path = helpers.rootpath(value['file'])
            if expected and path.resolve().is_relative_to(HERE):
                helpers.add(path, expected)
        for key, child in value.items():
            if isinstance(key, str) and key.startswith('docs/') and isinstance(child, str) and len(child) == 64:
                path = helpers.rootpath(key)
                if path.resolve().is_relative_to(HERE): helpers.add(path, child)
            pin_nested_artifacts(child)
    elif isinstance(value, list):
        for child in value: pin_nested_artifacts(child)


def main(stage):
    historical_seen = set()
    chain = ['01', '02', '03', '04-R02', '05', '06', '07', '08']
    for number in chain:
        report = json.loads((HERE / f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())
        for row in report['coverage']:
            actual = set(range(*row['range']))
            assert not historical_seen & actual, ('duplicate historical range', number, row)
            historical_seen |= actual
    assert len(historical_seen) == 5115
    specifications = [
        ('/root/review_12250_13000', r'native_12250_04250_05250\.(\d{5})_(\d{5})\.json', 5150, 5250),
        ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 2900, 3000),
        ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 5800, 5900),
        ('/root/review_08250_09250', r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json', 6715, 6755),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 7370, 7395),
        ('/root/review_06250_07250', r'native_06250_08250_09250\.(\d{5})_(\d{5})\.json', 8250, 8450),
        ('/root/review_11870_12250', r'native-11870-(\d{5})-(\d{5})-146v5-v1\.json', 1500, 1545),
    ]
    coverage, new_seen = [], set()
    for task, pattern, start, stop in specifications:
        notes, seen = [], set()
        for note in sorted(helpers.NOTES.iterdir()):
            match = re.fullmatch(pattern, note.name)
            if match and start <= int(match[1]) < int(match[2]) <= stop and note.name != 'native_06250_08250_09250.08250_08277.json':
                ordinals = set(range(int(match[1]), int(match[2])))
                assert not seen & ordinals
                seen |= ordinals
                document = json.loads(note.read_bytes())
                if task in {'/root/review_06250_07250', '/root/review_11870_12250'}:
                    helpers.add(note)
                    pin_nested_artifacts(document)
                elif task == '/root/review_08250_09250' and document.get('artifacts'):
                    helpers.add(note)
                    for name, row in document['artifacts'].items():
                        assert set(row) == {'raw_sha256'}
                        helpers.add(helpers.rootpath(name), row['raw_sha256'])
                else:
                    previous.pin_note(note, task)
                notes.append(str(note.relative_to(ROOT)))
        assert seen == set(range(start, stop)), ('missing frozen range', task, start, stop)
        assert not (new_seen | historical_seen) & seen
        new_seen |= seen
        coverage.append({'task': task, 'range': [start, stop], 'worker_attested_unique_source_reads': len(seen), 'notes': notes})
    supplements = []
    plan = ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'
    helpers.paths[str(plan.relative_to(ROOT))] = hashlib.sha256(plan.read_bytes()).hexdigest()
    helpers.add(Path(__file__))
    assert len(new_seen) == 610 and len(historical_seen | new_seen) == 5725
    report = {
        'schema': 'photo-root-manual-draft-checkpoint-verification/v1', 'actor': '/root',
        'previous_checkpoint': 'ROOT-MANUAL-DRAFT-CHECKPOINT-08.json',
        'previous_disjoint_draft_candidates': 5115, 'coverage': coverage,
        'worker_attested_additional_unique_source_reads': len(new_seen),
        'cumulative_disjoint_native_draft_candidates': 5725,
        'files': dict(sorted(helpers.paths.items())),
        'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
        'frozen_supplements': supplements, 'historical_ranges_exactly_disjoint': True,
        'root_all_sources_personally_read_claimed': False,
        'source_corrections_or_new_role_decisions_accepted': False,
        'formal_native_proof_count_for_these_draft_ranges': 0,
        'operational_native_qualified_count': 0, 'canonical_changed': False,
        'fresh06250_read_boundary': '200 actual full original/current/exact5B/ownbinding/closure reads and manual fact drafts; current5B wholeafter reread200, NEW proposed source-after reread0, formal native0. Do not count this as200 newly authored full afters or approved sources.',
        'catalog_boundary': 'Historical142V2/144V4 or explicitly assigned146V5 remains exactly bound per worker draft. Research146V5 approval does not re-sign earlier source, role, mode, or proof decisions.',
        'known_unapproved_boundaries': [
            'All actual positive fields, including named phrase fields, need direct whole-clause review. Aliases and metadata are not positive native evidence.',
            'A restricted existing-prop or P-only source proposal is not accepted merely because its shape passes. Preserve the original intended generated content and actual effect permissions.',
            'Physical traits, anatomical regions, conditional histories, ownership topology and whole effect/receiver closure remain manually unresolved where noted.',
            'Read counts, generated preparation packets, fact counts, schema validity, hashes and synthetic consumers are not semantic acceptance or native operating qualification.',
        ],
        'gemini_calls': 0, 'network_calls': 0,
    }
    output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-09.json'
    if stage:
        assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
    with output.open('x') as stream:
        json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')
    if stage:
        expected = set(helpers.paths) | {str(output.relative_to(ROOT))}
        subprocess.run(['git', 'add', '--', *sorted(expected)], cwd=ROOT, check=True)
        result = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout
        staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
        assert staged <= expected
        for name in expected:
            assert subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT) == (ROOT / name).read_bytes(), name
    print(json.dumps({'frozen_files': len(helpers.paths), 'additional_direct_drafts': len(new_seen), 'cumulative_disjoint_direct_drafts': 5115, 'native_approvals': 0, 'staged': stage}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', action='store_true')
    main(parser.parse_args().stage)
