#!/usr/bin/env python3
"""Prepare regenerated retrieval views while preserving every reviewed view.

The canonical view asset is an input, never overwritten. Changed or missing
candidate sources and conflicting view IDs require review before publication.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import photo_archived_legacy_evidence as legacy
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views
import photo_replay_reviewed_view_overlay as replay
import photo_reviewed_view_rebase as rebase

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
VIEWS = 'photo_candidate_retrieval_views_calibration_20261027.json'


def merge_reviewed(generated, baseline, records):
    """Restore missing reviewed views; reject conflicting or stale meanings."""
    views.validate(baseline, records, require_complete=False)
    if (not isinstance(generated, dict) or generated.get('schema') != views.SCHEMA
            or generated.get('recipe') != views.RECIPE or not isinstance(generated.get('views'), list)
            or generated.get('native_approval', False) is not False):
        raise ValueError('invalid generated view module')
    result = copy.deepcopy(generated)
    generated_rows = result['views']
    by_id = {row['id']: row for row in generated_rows}
    if len(by_id) != len(generated_rows):
        raise ValueError('duplicate generated view identity')
    merged = []
    restored = 0
    for row in baseline['views']:
        previous = by_id.get(row['id'])
        if previous is not None:
            if previous != row:
                raise ValueError('generated view conflicts with reviewed view: ' + row['id'])
            merged.append(previous)
            continue
        merged.append(copy.deepcopy(row))
        restored += 1
    baseline_ids = {row['id'] for row in baseline['views']}
    merged.extend(row for row in generated_rows if row['id'] not in baseline_ids)
    result['views'] = merged
    views.validate(result, records, require_complete=False)
    return result, restored


def prepare(generated, baseline, records, *, root=replay.ROOT, manifest=replay.FOLLOWUPS):
    result, restored = merge_reviewed(generated, baseline, records)
    registry = json.loads(Path(manifest).read_bytes())
    if registry.get('schema') != 'photo-reviewed-view-replay-sequence/v1' or not registry.get('overlays'):
        raise ValueError('missing reviewed overlay sequence')
    first = registry['overlays'][0]
    base = Path(root).resolve()
    path = (base / first['path']).resolve()
    if not path.is_relative_to(base):
        raise ValueError('overlay path outside repository')
    result, stages = replay.apply_registered(result, records, path.read_bytes(), first['sha256'],
                                              root=base, manifest=manifest)
    legacy_result = legacy.verify(records)
    covered = {(v['candidate_id'], v['realization_id']) for v in result['views']}
    positive = {(cid, rid) for cid, record in records.items() if record['record_kind'] != 'diagnostic'
                for rid in views.realization_ids(record)}
    return result, {'restored_reviewed_views': restored, 'views': len(result['views']),
                    'positive_realizations_without_view': len(positive - covered),
                    'overlay_stages': stages, 'legacy_evidence': legacy_result,
                    'research_originals': 'not retained or revalidated',
                    'runtime_activation': 'unchanged'}


def prepare_versioned(generated, baseline, records, *, release_path=rebase.RELEASE,
                      baseline_path=None, replay_manifest=replay.FOLLOWUPS,
                      root=replay.ROOT, mode='current'):
    """Replay the historical version, then apply an explicitly bound successor.

    Historical and current views may differ in meaning. The successor records
    their exact versions and source hashes; it does not assert equivalence or
    turn reviewed search views into native permission.
    """
    release, delta, migration, evidence = rebase.read_release(release_path)
    if (baseline_path is None or rebase.file_sha(baseline_path) != release['historical_baseline_sha256']
            or rebase.file_sha(replay_manifest) != release['historical_replay_manifest_sha256']):
        raise ValueError('historical baseline or overlay sequence changed')
    historical = rebase.historical_records(records, delta)
    if mode == 'historical':
        result, report = prepare(generated, baseline, historical, root=root, manifest=replay_manifest)
        report['release_mode'] = 'historical'
        report['historical_commit'] = release['historical_commit']
        report['historical_candidate_scope'] = 'reviewed-view and overlay sources; newer unrelated candidates remain'
        return result, report
    if mode != 'current':
        raise ValueError('unknown reviewed release mode')
    history, history_report = prepare(baseline, baseline, historical, root=root, manifest=replay_manifest)
    history_report['historical_candidate_scope'] = 'reviewed-view and overlay sources; newer unrelated candidates remain'
    rebase.validate_transitions(records, migration, evidence)
    current, transition = rebase.apply_rebase(history, records, release, migration)
    result, restored = merge_reviewed(generated, current, records)
    return result, {'release_mode': 'current', 'historical_replay': history_report,
                    'version_transition': transition, 'restored_current_views': restored,
                    'views': len(result['views']), 'runtime_activation': 'unchanged',
                    'native_approval': False}


def main():
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    p.add_argument('--assets', type=Path, default=ASSETS)
    p.add_argument('--input', type=Path, required=True, help='Newly generated or existing view module.')
    p.add_argument('--output', type=Path, required=True, help='New file; existing assets are never overwritten.')
    p.add_argument('--release-mode', choices=('current', 'historical'), default='current',
                   help='Replay historical evidence and optionally migrate to the pinned current release.')
    a = p.parse_args()
    if a.output.exists() or a.output.resolve() in {a.input.resolve(), (a.assets / VIEWS).resolve()}:
        raise ValueError('output must be a new file separate from both inputs')
    records = corpus.load(a.assets)['candidates']
    baseline = json.loads((a.assets / VIEWS).read_bytes())
    generated = json.loads(a.input.read_bytes())
    prepared, report = prepare_versioned(generated, baseline, records,
                                          baseline_path=a.assets / VIEWS, mode=a.release_mode)
    created = False
    try:
        with a.output.open('x', encoding='utf-8') as out:
            created = True
            json.dump(prepared, out, ensure_ascii=False, indent=2)
            out.write('\n')
    except BaseException:
        if created and a.output.exists(): a.output.unlink()
        raise
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
