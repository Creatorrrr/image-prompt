"""Preserve 847 additional disjoint direct-review drafts without approving them.

Only frozen note attestations determine read counts. Hash, syntax and exact
range checks confer no source meaning, tag, native proof or operational status.
"""
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


def pin_note(note, task):
    document = json.loads(note.read_bytes())
    if task == '/root/review_08250_09250' and document.get('files'):
        helpers.add(note)
        for row in document['files'].values():
            helpers.add(helpers.rootpath(row['file']), row['raw_sha256'])
    else:
        helpers.pinned(note)
    for row in document.get('immutable_manifest', []):
        helpers.add(helpers.rootpath(row['file']), row['raw_sha256'])
    if task == '/root/review_11870_12250':
        for key in ['literal_authoring', 'prepared_packet', 'unsigned_draft']:
            row = document[key]
            helpers.add(helpers.rootpath(row['file']), row['file_sha256'])
    if task == '/root/review_07250_08250' and document.get('literal_file'):
        for key in ['input', 'authored', 'literal']:
            helpers.add(helpers.rootpath(document[key + '_file']), document[key + '_raw_sha256'])


def main(stage):
    specifications = [
        ('/root/review_06250_07250', r'native_06250_00250_01250\.(\d{5})_(\d{5})\.json', 804, 994),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 4150, 4250),
        ('/root/review_12250_13000', r'native_12250_04250_05250\.(\d{5})_(\d{5})\.json', 4750, 4950),
        ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 2650, 2750),
        ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 5500, 5600),
        ('/root/review_08250_09250', r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json', 6550, 6645),
        ('/root/review_11870_12250', r'native-11870-(\d{5})-(\d{5})-literal-draft-v1\.json', 1408, 1460),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 7250, 7260)]
    coverage, all_seen = [], set()
    for task, pattern, start, stop in specifications:
        selected, seen = [], set()
        for note in sorted(helpers.NOTES.iterdir()):
            match = re.fullmatch(pattern, note.name)
            if match and start <= int(match[1]) < int(match[2]) <= stop:
                ordinals = set(range(int(match[1]), int(match[2])))
                assert not seen & ordinals, 'overlapping checkpoint notes'
                seen |= ordinals
                pin_note(note, task)
                selected.append(str(note.relative_to(ROOT)))
        assert seen == set(range(start, stop)), ('incomplete frozen range', task, start, stop)
        assert not all_seen & seen
        all_seen |= seen
        coverage.append({'task': task, 'range': [start, stop], 'worker_attested_unique_source_reads': len(seen), 'notes': selected})
    supplements = [
        'worker-notes/native-11870-01433-01443-fullspec-read-supplement-v2.json',
        'authored/native_06250_00250_01250.00800.neighbor-r02.json',
        'authored/native_06250_00250_01250.00942.neighbor-r02.json',
        'authored/native_06250_00250_01250.00942.neighbor-r03.json',
        'authored/native_08250_06250_07250.06603_06609.metadata-fact-revision-01.json']
    for name in supplements:
        helpers.add(HERE / name)
    helpers.add(Path(__file__))
    assert len(all_seen) == 847
    report = {'schema': 'photo-root-manual-draft-checkpoint-verification/v1', 'actor': '/root',
              'previous_checkpoint': 'ROOT-MANUAL-DRAFT-CHECKPOINT-04-R02.json',
              'previous_disjoint_draft_candidates': 3012, 'coverage': coverage,
              'worker_attested_additional_unique_source_reads': len(all_seen),
              'cumulative_disjoint_native_draft_candidates': 3859,
              'files': dict(sorted(helpers.paths.items())),
              'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
              'frozen_supplements': supplements,
              'root_all_sources_personally_read_claimed': False,
              'source_corrections_or_new_role_decisions_accepted': False,
              'formal_native_proof_count_for_these_draft_ranges': 0,
              'operational_native_qualified_count': 0, 'canonical_changed': False,
              'catalog_boundary': 'Exact historical142V2 or explicit144V4 inputs retained per checkpoint. Proposed145V5 is not an approved or converted input.',
              'known_unapproved_boundaries': [
                  'Actual positive paraphrases and embedding text must be retained; aliases/tags are not positive visual evidence.',
                  'The6603/6609 alias-only draft facts are withdrawn by a separate immutable proposal, without changing the old drafts.',
                  'The1433:1443 six-neighbor read attestation is replaced only by the explicit fresh-read supplement; the original unsupported prior-read statement stays visible.',
                  'The942 neighbor labels were corrected twice in separate research proposals. Neither proposal creates a new slot or approves a candidate.',
                  'Partial path inventory, a typed fact draft and quote membership do not establish whole clause coverage or core-owner permission.'],
              'gemini_calls': 0, 'network_calls': 0}
    output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-05.json'
    if stage:
        assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip(), 'preserve existing index'
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
    print(json.dumps({'frozen_files': len(helpers.paths), 'additional_direct_drafts': len(all_seen), 'cumulative_disjoint_direct_drafts': 3859, 'native_approvals': 0, 'staged': stage}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', action='store_true')
    main(parser.parse_args().stage)
