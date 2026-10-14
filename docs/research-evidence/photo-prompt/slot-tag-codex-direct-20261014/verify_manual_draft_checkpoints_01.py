"""Verify explicit frozen draft evidence identities; never confer qualification.

Ranges are a root-selected checkpoint only. Read counts are workers' direct-read
attestations, not a count inferred from loading files. Source meanings, proposed
corrections, owner maps and tag assignments remain unaccepted research drafts.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NOTES = HERE / 'worker-notes'
paths = {}


def add(path, sha=None):
    path = path.resolve()
    if not path.is_relative_to(HERE) or not path.is_file():
        raise ValueError('outside/missing explicit evidence: ' + str(path))
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if sha is not None and actual != sha:
        raise ValueError('frozen hash changed: ' + str(path))
    if path.suffix == '.json':
        json.loads(raw)
    elif path.suffix == '.py':
        ast.parse(raw, filename=str(path))
    paths[str(path.relative_to(ROOT))] = actual


def rootpath(value):
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path if value.startswith('docs/') else HERE / path


def pinned(note):
    add(note)
    doc = json.loads(note.read_text())
    artifacts = doc.get('artifacts', {})
    if isinstance(artifacts, dict):
        for name, sha in artifacts.items():
            add(rootpath(name), sha)
    elif isinstance(artifacts, list):
        for row in artifacts:
            add(rootpath(row['path']), row['sha256'])
    for name, row in doc.get('files', {}).items():
        add(rootpath(name), row if isinstance(row, str) else row['byte_sha256'])
    for pathkey, shakey in [('authored_path', 'authored_sha256'),
                            ('authored_file', 'authored_sha256'),
                            ('source_packet', 'source_packet_raw_sha256'),
                            ('input_packet_file', 'input_packet_sha256')]:
        if doc.get(pathkey) and doc.get(shakey):
            add(rootpath(doc[pathkey]), doc[shakey])
    for row in doc.get('component_files', []):
        add(rootpath(row['draft']), row['draft_sha256'])
        add(rootpath(row['reread_note']), row['reread_note_sha256'])
    return doc


def main(stage):
    specifications = [
        ('/root/review_06250_07250', r'native_06250_00250_01250\.(\d{5})_(\d{5})\.json', 250, 500),
        ('/root/review_07250_08250', r'native-07250-(\d{5})-(\d{5})\.json', 3250, 3650),
        ('/root/review_12250_13000', r'native_12250_04250_05250\.(\d{5})_(\d{5})\.json', 4250, 4500),
        ('/root/review_09250_10500', r'native-09250-(\d{5})-(\d{5})\.json', 2250, 2500),
        ('/root/review_05250_06250', r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json', 5250, 5350),
    ]
    coverage = []
    for task, pattern, start, stop in specifications:
        selected = []
        seen = set()
        for note in sorted(NOTES.iterdir()):
            match = re.fullmatch(pattern, note.name)
            if match and start <= int(match[1]) < int(match[2]) <= stop:
                ordinals = set(range(int(match[1]), int(match[2])))
                if ordinals & seen:
                    raise ValueError('overlapping checkpoint ranges')
                seen.update(ordinals)
                pinned(note)
                selected.append(str(note.relative_to(ROOT)))
        if seen != set(range(start, stop)):
            raise ValueError('missing exact frozen checkpoint coverage: ' + task)
        coverage.append({'task': task, 'range': [start, stop],
                         'worker_attested_unique_source_reads': len(seen), 'notes': selected})
    pinned(NOTES / 'native-08250-06250-06300.json')
    coverage.append({'task': '/root/review_08250_09250', 'range': [6250, 6300],
                     'worker_attested_unique_source_reads': 50,
                     'notes': [str((NOTES / 'native-08250-06250-06300.json').relative_to(ROOT))]})
    # Root directly read all nine proposed complete before/after records; this
    # preserves their input proposals, not their native approval.
    for name in ['authored/native_11870_first50_pending_resolution_v1.json',
                 'worker-notes/native-11870-first50-pending-resolution-v1.json']:
        add(HERE / name)
    add(Path(__file__))
    report = {'schema': 'photo-root-manual-draft-checkpoint-verification/v1',
              'actor': '/root', 'coverage': coverage,
              'worker_attested_unique_read_count': sum(row['worker_attested_unique_source_reads'] for row in coverage),
              'all_pinned_raw_hashes_verified': True, 'json_and_python_ast_valid': True,
              'files': dict(sorted(paths.items())),
              'root_all_sources_personally_read_claimed': False,
              'source_corrections_or_new_role_decisions_accepted': False,
              'formal_native_proof_count_for_these_draft_ranges': 0,
              'operational_native_qualified_count': 0, 'canonical_changed': False,
              'gemini_calls': 0, 'network_calls': 0}
    output = HERE / 'ROOT-MANUAL-DRAFT-CHECKPOINT-01.json'
    with output.open('x') as stream:
        json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')
    if stage:
        if subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT):
            raise ValueError('preserve existing staged files')
        subprocess.run(['git', 'add', '--', *paths, str(output.relative_to(ROOT))], cwd=ROOT, check=True)
    print(json.dumps({'frozen_evidence_files': len(paths), 'bytes': sum((ROOT / p).stat().st_size for p in paths),
                      'worker_attested_unique_source_reads': report['worker_attested_unique_read_count'],
                      'formal_native_qualification': 0, 'root_semantic_acceptance': False, 'staged': stage}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', action='store_true')
    main(parser.parse_args().stage)
