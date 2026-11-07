"""Versioned, source-bound bridge from historical reviewed views to current data.

Historical candidates and overlays are replayed as historical evidence. A
hash-pinned delta then selects previously sealed current views. Changes in the
view wording are not asserted equivalent, and this module grants no native
qualification or permission.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path

import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views

RELEASE = Path(__file__).resolve().parents[1] / 'data/reviewed-views/06-current-release.json'


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _artifact(directory, name, expected):
    if not isinstance(name, str) or Path(name).name != name:
        raise ValueError('reviewed release artifact path must be a local file name')
    path = Path(directory) / name
    if not path.is_file() or file_sha(path) != expected:
        raise ValueError('reviewed release artifact missing or changed: ' + name)
    return path


def read_release(path=RELEASE):
    path = Path(path)
    release = json.loads(path.read_bytes())
    if release.get('schema') != 'photo-reviewed-current-release/v1' or release.get('native_approval') is not False:
        raise ValueError('unsupported reviewed current release')
    root = path.parent
    historical_path = _artifact(root, release['historical_delta_file'], release['historical_delta_sha256'])
    rebase_path = _artifact(root, release['current_rebase_file'], release['current_rebase_sha256'])
    evidence_path = _artifact(root, release['source_transition_evidence_file'], release['source_transition_evidence_sha256'])
    historical = json.loads(gzip.decompress(historical_path.read_bytes()))
    rebase = json.loads(gzip.decompress(rebase_path.read_bytes()))
    evidence = json.loads(evidence_path.read_bytes())
    if (historical.get('schema') != 'photo-reviewed-historical-candidate-delta/v1'
            or historical.get('historical_commit') != release['historical_commit']
            or rebase.get('schema') != 'photo-reviewed-current-rebase/v1'
            or rebase.get('native_approval') is not False
            or rebase.get('historical_delta_sha256') != release['historical_delta_sha256']
            or rebase.get('historical_baseline_sha256') != release['historical_baseline_sha256']
            or rebase.get('replay_manifest_sha256') != release['historical_replay_manifest_sha256']
            or rebase.get('anchor_generation_id') != release['current_anchor_generation_id']
            or evidence.get('schema') != 'photo-reviewed-source-transition-evidence/v1'
            or evidence.get('generation_id') != release['current_anchor_generation_id']):
        raise ValueError('reviewed release bindings disagree')
    return release, historical, rebase, evidence


def historical_records(records, delta):
    old = dict(records)
    changes = delta.get('records')
    if not isinstance(changes, dict) or not changes:
        raise ValueError('historical candidate delta is missing')
    for cid, record in changes.items():
        if cid not in records or not isinstance(record, dict) or record.get('id') != cid:
            raise ValueError('historical candidate delta contains an unknown owner')
        old[cid] = record
    return old


def validate_transitions(records, rebase, evidence):
    saved = evidence.get('records')
    camera = rebase['camera_projection']
    makeup = rebase['makeup_alias_change']
    if not isinstance(saved, dict) or set(saved) != {camera['candidate_id'], makeup['candidate_id']}:
        raise ValueError('source transition evidence is incomplete')
    cid = camera['candidate_id']
    if (cid not in records or corpus.digest(saved[cid]) != camera['active_record_sha256']
            or corpus.digest(records[cid]) != camera['working_record_sha256']
            or camera['only_removed_field'] != '/content/role_evidence'):
        raise ValueError('camera search source projection changed')
    projected = copy.deepcopy(saved[cid])
    if not isinstance(projected.get('content', {}).pop('role_evidence', None), dict) or projected != records[cid]:
        raise ValueError('camera source projection changes more than native evidence')
    cid = makeup['candidate_id']
    if (cid not in records or corpus.digest(saved[cid]) != makeup['before_record_sha256']
            or corpus.digest(records[cid]) != makeup['after_record_sha256']
            or makeup.get('primary_meaning_changed') is not False):
        raise ValueError('makeup source transition changed')
    previous = copy.deepcopy(saved[cid])
    previous['content']['aliases'] += makeup['aliases_added']
    if previous != records[cid]:
        raise ValueError('makeup source transition changes more than reviewed aliases')


def apply_rebase(historical_module, records, release, rebase):
    original = historical_module['views']
    by_id = {row['id']: row for row in original}
    if len(by_id) != len(original) or len(original) != release['expected_historical_views']:
        raise ValueError('historical reviewed view population changed')
    replacements = {}
    for change in rebase['replacements']:
        vid = change['id']
        if (vid in replacements or vid not in by_id or corpus.digest(by_id[vid]) != change['before_view_sha256']
                or change['after_view'].get('id') != vid
                or any(change['after_view'].get(field) != by_id[vid].get(field)
                       for field in ('candidate_id', 'realization_id', 'key', 'kind'))):
            raise ValueError('reviewed view replacement is stale or duplicated')
        replacements[vid] = change['after_view']
    result = copy.deepcopy(historical_module)
    result['views'] = [copy.deepcopy(replacements.get(row['id'], row)) for row in original]
    known = set(by_id)
    for row in rebase['additions']:
        if row['id'] in known:
            raise ValueError('reviewed view addition is duplicated')
        known.add(row['id'])
        result['views'].append(copy.deepcopy(row))
    if len(result['views']) != release['expected_current_views']:
        raise ValueError('rebased reviewed view population changed')
    views.validate(result, records, require_complete=False)
    return result, {'historical_views': len(original), 'replaced_views': len(replacements),
                    'added_views': len(rebase['additions']), 'current_views': len(result['views']),
                    'semantic_equivalence_asserted': False, 'native_approval': False}
