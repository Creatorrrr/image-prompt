import copy
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views
import photo_prepare_reviewed_views as prepare
import photo_reviewed_view_rebase as rebase


def row(record, key='whole', kind='whole'):
    cid = record['id']
    return {'id': views.view_id(cid, 'base', key), 'candidate_id': cid, 'realization_id': 'base',
            'key': key, 'kind': kind, 'source_record_sha256': views.digest(record),
            'text_en': record['content']['en'], 'text_ko': record['content']['ko'],
            'source_quotes': [{'pointer': '/content/en', 'quote': record['content']['en']}],
            'native_approval': False}


def test_rebase_preserves_versions_and_rejects_stale_evidence():
    old = {'id': 'c1', 'record_kind': 'visual_option', 'content': {'en': 'blue coat', 'ko': '파란 코트'}, 'effects': {}}
    new = {'id': 'c1', 'record_kind': 'visual_option', 'content': {'en': 'red coat', 'ko': '빨간 코트'}, 'effects': {}}
    before, after = row(old), row(new)
    historical = {'schema': views.SCHEMA, 'recipe': views.RECIPE, 'views': [before], 'native_approval': False}
    release = {'expected_historical_views': 1, 'expected_current_views': 1}
    change = {'replacements': [{'id': before['id'], 'before_view_sha256': corpus.digest(before),
                                'after_view': after}], 'additions': []}
    result, report = rebase.apply_rebase(historical, {'c1': new}, release, change)
    assert result['views'] == [after]
    assert historical['views'] == [before]
    assert report['semantic_equivalence_asserted'] is False
    changed = copy.deepcopy(change)
    changed['replacements'][0]['before_view_sha256'] = '0' * 64
    with pytest.raises(ValueError, match='stale'):
        rebase.apply_rebase(historical, {'c1': new}, release, changed)
    changed = copy.deepcopy(change)
    changed['replacements'][0]['after_view']['source_quotes'][0]['quote'] = 'blue coat'
    with pytest.raises(ValueError, match='quote'):
        rebase.apply_rebase(historical, {'c1': new}, release, changed)
    changed = copy.deepcopy(change)
    changed['replacements'][0]['after_view']['kind'] = 'context'
    with pytest.raises(ValueError, match='stale'):
        rebase.apply_rebase(historical, {'c1': new}, release, changed)


def test_transition_cannot_add_native_authority_or_change_primary_meaning():
    camera = {'id': 'camera', 'content': {'en': 'above eyes'}}
    active = copy.deepcopy(camera)
    active['content']['role_evidence'] = {'reviewed': True}
    makeup_before = {'id': 'makeup', 'content': {'en': 'head', 'aliases': ['cosmetic']}}
    makeup_after = copy.deepcopy(makeup_before)
    makeup_after['content']['aliases'].append('doll makeup display')
    records = {'camera': camera, 'makeup': makeup_after}
    migration = {
        'camera_projection': {'candidate_id': 'camera', 'active_record_sha256': corpus.digest(active),
                              'working_record_sha256': corpus.digest(camera),
                              'only_removed_field': '/content/role_evidence'},
        'makeup_alias_change': {'candidate_id': 'makeup', 'before_record_sha256': corpus.digest(makeup_before),
                                'after_record_sha256': corpus.digest(makeup_after),
                                'aliases_added': ['doll makeup display'], 'primary_meaning_changed': False},
    }
    evidence = {'records': {'camera': active, 'makeup': makeup_before}}
    rebase.validate_transitions(records, migration, evidence)
    assert 'role_evidence' not in records['camera']['content']
    changed = copy.deepcopy(records)
    changed['makeup']['content']['en'] = 'a different head'
    with pytest.raises(ValueError, match='transition'):
        rebase.validate_transitions(changed, migration, evidence)
    changed = copy.deepcopy(evidence)
    changed['records']['camera']['content']['en'] = 'below eyes'
    with pytest.raises(ValueError, match='projection'):
        rebase.validate_transitions(records, migration, changed)


def test_pinned_rebase_artifact_fails_closed_when_changed(tmp_path):
    manifest = json.loads(rebase.RELEASE.read_bytes())
    shutil.copyfile(rebase.RELEASE, tmp_path / rebase.RELEASE.name)
    for key in ('historical_delta_file', 'current_rebase_file', 'source_transition_evidence_file'):
        name = manifest[key]
        shutil.copyfile(rebase.RELEASE.parent / name, tmp_path / name)
    artifact = tmp_path / manifest['current_rebase_file']
    artifact.write_bytes(artifact.read_bytes() + b'tampered')
    with pytest.raises(ValueError, match='artifact missing or changed'):
        rebase.read_release(tmp_path / rebase.RELEASE.name)


def test_real_historical_overlay_replay_and_current_rebase():
    assets = ROOT / 'assets'
    records = corpus.load(assets)['candidates']
    baseline_path = assets / prepare.VIEWS
    baseline = json.loads(baseline_path.read_bytes())
    generated = json.loads((assets / 'photo_candidate_retrieval_views_nurse_uniform_final_followup_20261107.json').read_bytes())
    result, report = prepare.prepare_versioned(generated, baseline, records, baseline_path=baseline_path)
    stages = report['historical_replay']['overlay_stages']
    assert len(stages) == 5 and sum(x['already_present'] for x in stages) == 622
    assert report['historical_replay']['legacy_evidence'] == {'archives': 1, 'candidates': 467}
    assert report['version_transition']['replaced_views'] == 1250
    assert report['version_transition']['added_views'] == 1376
    assert report['views'] == len(result['views']) == 26927
    assert report['native_approval'] is False
