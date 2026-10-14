"""Preserve499 additional direct-review drafts without granting qualification.

The explicit disjoint ranges follow workers' frozen read attestations. File
hash/AST checks do not establish semantic truth or root personal source reads.
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


def main(stage):
    specs = [
        ('/root/review_06250_07250', r'native_06250_00250_01250\.(\d{5})_(\d{5})\.json', 638, 704),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 3900, 4000),
        ('/root/review_12250_13000', r'native_12250_04250_05250\.(\d{5})_(\d{5})\.json', 4600, 4700),
        ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 2550, 2600),
        ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 5400, 5450),
        ('/root/review_08250_09250', r'native-08250-(\d{5})-(\d{5})\.json', 6400, 6450),
    ]
    coverage = []
    for task, pattern, start, stop in specs:
        seen = set()
        selected = []
        for note in sorted(helpers.NOTES.iterdir()):
            match = re.fullmatch(pattern, note.name)
            if match and start <= int(match[1]) < int(match[2]) <= stop:
                ordinals = set(range(int(match[1]), int(match[2])))
                if seen & ordinals:
                    raise ValueError('overlapping selected checkpoint ranges')
                seen |= ordinals
                helpers.pinned(note)
                selected.append(str(note.relative_to(ROOT)))
        if seen != set(range(start, stop)):
            raise ValueError('incomplete selected frozen range: ' + task)
        coverage.append({'task': task, 'range': [start, stop],
                         'worker_attested_unique_source_reads': len(seen), 'notes': selected})
    for first, last in [(1325, 1350), (1350, 1375), (1375, 1400), (1400, 1408)]:
        note = HERE / f'worker-notes/native-11870-{first:05d}-{last:05d}-literal-draft-v1.json'
        document = helpers.pinned(note)
        for key in ['draft', 'literal', 'input', 'preserved_literal_v1', 'preserved_incomplete_larger_range_literal']:
            row = document.get(key)
            if row:
                helpers.add(ROOT / row['file'], row['file_sha256'])
        coverage.append({'task': '/root/review_11870_12250', 'range': [first, last],
                         'worker_attested_unique_source_reads': last-first, 'notes': [str(note.relative_to(ROOT))]})
    for name in ['authored/root_00000_00020_source_proposals_v1.py',
                 'authored/root_00000_00020_source_proposals_v1.json',
                 'worker-notes/root-00000-00020-source-proposals-reread-01.json',
                 'worker-notes/native-09250-catalog-v4-read-001.json',
                 'worker-notes/native-09250-flame-2589-v4-boundary-001.json',
                 'worker-notes/native_06250_catalog144v4_read_and_selector_helper_00684.json']:
        helpers.add(HERE / name)
    errata = HERE / 'worker-notes/native_05250_05250_06250.task-identity-errata-20261014.json'
    helpers.add(errata, 'c5abf43c22f94bed838c89f500e7a6913d1188e0064fa658a61ee01750501aac')
    helpers.add(errata.with_suffix('.sha256'))
    for name in ['native-09250-boundary-followup-005.json', 'native-09250-boundary-followup-006.json']:
        helpers.add(HERE / 'worker-notes' / name)
    helpers.add(Path(__file__))
    total = sum(row['worker_attested_unique_source_reads'] for row in coverage)
    assert total == 499
    output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-03.json'
    report = {
        'schema': 'photo-root-manual-draft-checkpoint-verification/v1', 'actor': '/root',
        'previous_checkpoint': 'ROOT-MANUAL-DRAFT-CHECKPOINT-02.json',
        'previous_disjoint_draft_candidates': 2013, 'coverage': coverage,
        'worker_attested_additional_unique_source_reads': total,
        'cumulative_disjoint_native_draft_candidates': 2512,
        'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
        'files': dict(sorted(helpers.paths.items())),
        'root_all_sources_personally_read_claimed': False,
        'source_corrections_or_new_role_decisions_accepted': False,
        'formal_native_proof_count_for_these_draft_ranges': 0,
        'operational_native_qualified_count': 0, 'canonical_changed': False,
        'known_draft_errata': [
            'An old05250 task-name typo is preserved with an explicit15-file identity erratum; no additional semantic read is claimed.',
            'Wrong surface_material require_domain_match proposals remain unapplied and queued for individual correction. They are not approved by this checkpoint.',
            '11870 GRWM recording-purpose overreach v1 is preserved; selectedv2 removes that unsupported inference without suppressing presentation meaning.'],
        'catalog_boundary': 'Mixed historical142V2 and explicit new144V4 research drafts; exact per-checkpoint catalog bytes stay preserved. No automatic reclassification, proof conversion or final semantic approval. Root separately read20 original/current records and proposes5 corrections; these are not added to the2512 distinct draft count.',
        'gemini_calls': 0, 'network_calls': 0,
    }
    with output.open('x') as stream:
        json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')
    if stage:
        if subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip():
            raise ValueError('preserve existing staged files')
        subprocess.run(['git', 'add', '--', *helpers.paths, str(output.relative_to(ROOT))], cwd=ROOT, check=True)
    print(json.dumps({'frozen_evidence_files': len(helpers.paths),
        'bytes': sum((ROOT / name).stat().st_size for name in helpers.paths),
        'additional_direct_draft_candidates': total, 'cumulative_direct_drafts': 2512,
        'formal_native_qualification': 0, 'root_semantic_acceptance': False, 'staged': stage}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', action='store_true')
    main(parser.parse_args().stage)
