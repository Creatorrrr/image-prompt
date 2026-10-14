"""Preserve500 further disjoint manual drafts; no qualification or promotion."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('checkpoint01_primitives', HERE / 'verify_manual_draft_checkpoints_01.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


def main(stage):
    specifications = [
        ('/root/review_06250_07250', r'native_06250_00250_01250\.(\d{5})_(\d{5})\.json', 704, 804),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 4000, 4150),
        ('/root/review_12250_13000', r'native_12250_04250_05250\.(\d{5})_(\d{5})\.json', 4700, 4750),
        ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 2600, 2650),
        ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 5450, 5500),
        ('/root/review_08250_09250', r'native-08250-(\d{5})-(\d{5})\.json', 6450, 6550)]
    coverage = []
    for task, pattern, start, stop in specifications:
        seen, selected = set(), []
        for note in sorted(helpers.NOTES.iterdir()):
            match = re.fullmatch(pattern, note.name)
            if match and start <= int(match[1]) < int(match[2]) <= stop:
                ordinals = set(range(int(match[1]), int(match[2])))
                assert not seen & ordinals, 'overlapping checkpoint ranges'
                seen |= ordinals
                if task == '/root/review_08250_09250':
                    # These new notes store suffix labels as keys and explicit
                    # file/raw_sha256 objects as values; keep original bytes.
                    helpers.add(note)
                    document = json.loads(note.read_bytes())
                    for row in document['files'].values():
                        helpers.add(helpers.rootpath(row['file']), row['raw_sha256'])
                else:
                    helpers.pinned(note)
                selected.append(str(note.relative_to(ROOT)))
        assert seen == set(range(start, stop)), task
        coverage.append({'task': task, 'range': [start, stop],
                         'worker_attested_unique_source_reads': len(seen), 'notes': selected})
    helpers.add(Path(__file__))
    total = sum(row['worker_attested_unique_source_reads'] for row in coverage)
    assert total == 500
    output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-04.json'
    report = {'schema': 'photo-root-manual-draft-checkpoint-verification/v1', 'actor': '/root',
              'previous_checkpoint': 'ROOT-MANUAL-DRAFT-CHECKPOINT-03.json',
              'previous_disjoint_draft_candidates': 2512, 'coverage': coverage,
              'worker_attested_additional_unique_source_reads': total,
              'cumulative_disjoint_native_draft_candidates': 3012,
              'files': dict(sorted(helpers.paths.items())),
              'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
              'root_all_sources_personally_read_claimed': False,
              'source_corrections_or_new_role_decisions_accepted': False,
              'formal_native_proof_count_for_these_draft_ranges': 0,
              'operational_native_qualified_count': 0, 'canonical_changed': False,
              'catalog_boundary': 'Historical142V2 and fresh144V4 drafts retain their exact original input/spec hashes. No old tag, proof or status conversion.',
              'known_unapproved_boundaries': [
                  'Nonhuman flock spacing has a proposed proxemics scope gap, not an approved generic human-role inheritance.',
                  'Garment or accessory class alone does not prove actual wearing; known worker draft errata stay unapplied for individual correction.',
                  'Warm air, heat-haze and an emotional impression do not automatically establish a declared carrier temperature or wet surface.',
                  'Source labels, core roles, generic presence and candidate-specific metadata are not independently frozen anatomical/material/actual-owner facts.'],
              'gemini_calls': 0, 'network_calls': 0}
    with output.open('x') as stream:
        json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')
    if stage:
        assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
        subprocess.run(['git', 'add', '--', *helpers.paths, str(output.relative_to(ROOT))], cwd=ROOT, check=True)
        checked = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
        assert not checked.returncode, checked.stdout
        staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
        assert staged == set(helpers.paths) | {str(output.relative_to(ROOT))}
    print(json.dumps({'frozen_files': len(helpers.paths), 'additional_direct_drafts': total,
                      'cumulative_disjoint_direct_drafts': 3012, 'native_approvals': 0, 'staged': stage}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', action='store_true')
    main(parser.parse_args().stage)
