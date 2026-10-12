"""Verify the exact stage 5 transition before replaying earlier source contracts."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_DIR = Path('docs/research-evidence/photo-prompt/extension-maintenance')
TRANSITION_FILE = 'slot-retrieval-subject-context-20261012.json'
TRANSITION_SHA256 = 'c835f4c39d566aea86aa99cd55085dec76eabddd79f9a67cb3a8aab30e2401ef'
CATCHUP_FILE = 'photo-prompt-tags-history-catchup-20261012.json'
CATCHUP_SHA256 = '5984551e5736f4fea30978e6706132425bf3da5023c06ea786b92949d47ff84e'
EMT_FILE = 'emt-patient-transport-context-20261012.json'
EMT_SHA256 = '76ab6847308fb7d89c269d0fd8b5dba4bab0ed4ae2ed7a2fa047d2649b9cb744'
SOIL_FILE = 'soil-stage7-context-20261012.json'
SOIL_SHA256 = '2b975bccb186a9638133c8535b9cd8be16f69077822acd2c93d1875c795813d8'
SOIL_SOURCE = 'skills/photo-prompt-image-generator/assets/photo_prompt_soil_earth_extension.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()


def subject_context_transition(*, root=ROOT):
    raw = (root / RECORD_DIR / TRANSITION_FILE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != TRANSITION_SHA256:
        raise AssertionError('Stage 5 transition evidence changed')
    transition = json.loads(raw)
    if (transition['contract_version'] != 'photo-subject-context-source-transition/v1'
            or transition['base_commit'] != '330fd9b548f5cc2282acd8655d360a23b78cd423'):
        raise AssertionError('Unexpected stage 5 source baseline')
    return transition


def _sealed_record(root, filename, expected_sha256, version, *, source_file='skills/photo-prompt-image-generator/assets/photo_prompt_tags.json'):
    raw = (root / RECORD_DIR / filename).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise AssertionError('Source maintenance transition changed')
    record = json.loads(raw)
    if record['contract_version'] != version or record['source_file'] != source_file:
        raise AssertionError('Unexpected source maintenance transition')
    return record


def _rewind_root_source(current, *, root):
    """Reverse exact, sealed post-stage-5 changes before legacy reconstruction."""
    action = _sealed_record(root, EMT_FILE, EMT_SHA256, 'photo-source-metadata-transition/v1')
    catchup = _sealed_record(root, CATCHUP_FILE, CATCHUP_SHA256, 'photo-source-history-catchup/v1')
    if (action['base_commit'] != catchup['current_base_commit']
            or action['before_authored_canonical_sha256'] != catchup['current_authored_canonical_sha256']
            or catchup['stage5_transition_file'] != TRANSITION_FILE
            or catchup['stage5_transition_sha256'] != TRANSITION_SHA256):
        raise AssertionError('Source maintenance predecessor changed')
    body = {k: v for k, v in current.items() if k != 'maintenance_ref'}
    if digest(body) != action['after_authored_canonical_sha256']:
        raise AssertionError('Unreviewed current source change')
    prior = copy.deepcopy(body)
    if len(action['updates']) != 1:
        raise AssertionError('Unexpected EMT source transition')
    update = action['updates'][0]
    if (update['slot'], update['id']) != ('action', 'emt_assess_secure_transport_patient'):
        raise AssertionError('Unexpected EMT source identity')
    rows = [row for row in prior['slots']['action'] if row['id'] == update['id']]
    if len(rows) != 1 or digest(rows[0]) != action['after_entry_canonical_sha256']:
        raise AssertionError('EMT transition target changed')
    row = rows[0]
    if set(update['fields']) != {'tags', 'requires_primary_any_tags', 'primary_context_alternatives'}:
        raise AssertionError('Unexpected EMT source fields')
    for field, change in update['fields'].items():
        if (field in row) != change['after']['present'] or row.get(field) != change['after']['value']:
            raise AssertionError('EMT transition changed')
        if change['before']['present']:
            row[field] = copy.deepcopy(change['before']['value'])
        else:
            row.pop(field)
    if (digest(row) != action['before_entry_canonical_sha256']
            or digest(prior) != action['before_authored_canonical_sha256']):
        raise AssertionError('EMT predecessor reconstruction changed')
    if digest(prior) != catchup['current_authored_canonical_sha256']:
        raise AssertionError('Root source catch-up predecessor changed')
    if (catchup['other_source_changes'] != 0 or len(catchup['entry_ko_updates']) != 55
            or len(catchup['category_overrides_added']) != 4):
        raise AssertionError('Unexpected root source catch-up scope')
    seen = set()
    for change in catchup['entry_ko_updates']:
        key = (change['slot'], change['id'])
        if key in seen or change['field'] != 'ko':
            raise AssertionError('Duplicate or non-label historical change')
        seen.add(key)
        rows = [row for row in prior['slots'][change['slot']] if row['id'] == change['id']]
        if (len(rows) != 1 or rows[0]['ko'] != change['after']
                or digest(rows[0]) != change['after_entry_canonical_sha256']):
            raise AssertionError('Historical label transition changed')
        rows[0]['ko'] = copy.deepcopy(change['before'])
        if digest(rows[0]) != change['before_entry_canonical_sha256']:
            raise AssertionError('Historical label predecessor changed')
    overrides = prior['slot_applicability']['subject_category_overrides']
    for key, value in catchup['category_overrides_added'].items():
        if overrides.get(key) != value:
            raise AssertionError('Historical category transition changed')
        del overrides[key]
    if digest(prior) != catchup['predecessor_authored_canonical_sha256']:
        raise AssertionError('Stage-5 source predecessor changed')
    return prior


def _rewind_soil_source(current, *, root):
    """Reverse the sealed stage-7 soil applicability update before Stage 5."""
    record = _sealed_record(root, SOIL_FILE, SOIL_SHA256,
        'photo-source-metadata-transition/v1', source_file=SOIL_SOURCE)
    if (record['before_commit'] != '747f1da4751f7498e85c6cd3213ee772ce3cd59d'
            or record['after_commit'] != 'e7a694b10fb502b7991e5bdcbe15c361f2ffc800'
            or record['before_git_blob_sha1'] != 'e11761793c1cdae2bbd31757a24212cc19fc9fb3'
            or record['after_git_blob_sha1'] != 'b9d0c0f19c785fa0595f688fd9acec038d06c40f'
            or record['other_source_changes'] != 0 or len(record['updates']) != 2):
        raise AssertionError('Unexpected soil source transition')
    body = {k: v for k, v in current.items() if k != 'maintenance_ref'}
    if digest(body) != record['after_authored_canonical_sha256']:
        raise AssertionError('Unreviewed current source change')
    before = copy.deepcopy(body)
    expected = [('subject', 'soil_e077'), ('subject', 'soil_e078')]
    if [(u['slot'], u['id']) for u in record['updates']] != expected:
        raise AssertionError('Unexpected soil transition identities')
    for update in record['updates']:
        rows = [r for r in before['slots'][update['slot']] if r['id'] == update['id']]
        if len(rows) != 1 or digest(rows[0]) != update['after_entry_canonical_sha256']:
            raise AssertionError('Soil transition target changed')
        row = rows[0]
        if set(update['fields']) != {'primary_context_alternatives'}:
            raise AssertionError('Unexpected soil source fields')
        change = update['fields']['primary_context_alternatives']
        if (change['before']['present'] or not change['after']['present']
                or row.get('primary_context_alternatives') != change['after']['value']):
            raise AssertionError('Soil transition changed')
        del row['primary_context_alternatives']
        if digest(row) != update['before_entry_canonical_sha256']:
            raise AssertionError('Soil predecessor entry changed')
    if digest(before) != record['before_authored_canonical_sha256']:
        raise AssertionError('Soil predecessor reconstruction changed')
    return before


def before_stage05_subject_context(current, source_file, *, root=ROOT):
    """Reverse only authenticated deltas; reject every unreviewed live field."""
    item = subject_context_transition(root=root)['sources'][Path(source_file).name]
    if str(source_file) != item['source_file']:
        raise AssertionError('Unexpected stage 5 source path')
    name = Path(source_file).name
    body = (_rewind_root_source(current, root=root)
            if name == 'photo_prompt_tags.json'
            else _rewind_soil_source(current, root=root)
            if name == 'photo_prompt_soil_earth_extension.json'
            else {k: v for k, v in current.items() if k != 'maintenance_ref'})
    if digest(body) != item['after_sha256']:
        raise AssertionError('Unreviewed current source change')
    prior = item['prior_maintenance_ref']
    if prior is not None:
        reference = current['maintenance_ref']
        record = json.loads((root / RECORD_DIR / (reference['record_id'] + '.json')).read_text())
        previous = json.loads((root / RECORD_DIR / (prior['record_id'] + '.json')).read_text())
        if (digest(record) != reference['sha256'] or digest(previous) != prior['sha256']
                or record['authored_source_sha256'] != item['after_sha256']
                or record['prior_maintenance_ref'] != prior
                or record['source_transition'] != {'file': TRANSITION_FILE,
                    'sha256': TRANSITION_SHA256, 'source': Path(source_file).name}):
            raise AssertionError('Stage 5 maintenance chain changed')
    elif 'maintenance_ref' in current:
        raise AssertionError('Unexpected maintenance reference')
    before = copy.deepcopy(current)
    if name in ('photo_prompt_tags.json', 'photo_prompt_soil_earth_extension.json'):
        before = copy.deepcopy(body)
    for addition in item['additions']:
        rows = before['slots'][addition['slot']]
        matched = [r for r in rows if r['id'] == addition['entry']['id']]
        if matched != [addition['entry']]:
            raise AssertionError('Stage 5 added row changed')
        rows.remove(matched[0])
    for update in item['updates']:
        rows = [r for r in before['slots'][update['slot']] if r['id'] == update['id']]
        if len(rows) != 1:
            raise AssertionError('Stage 5 changed identity is not unique')
        for field, change in update['fields'].items():
            if change['before']['present']:
                rows[0][field] = copy.deepcopy(change['before']['value'])
            else:
                rows[0].pop(field)
    for field, change in item['top_level_changes'].items():
        if change['before']['present']:
            before[field] = copy.deepcopy(change['before']['value'])
        else:
            before.pop(field)
    if prior is not None:
        before['maintenance_ref'] = copy.deepcopy(prior)
    if digest({k: v for k, v in before.items() if k != 'maintenance_ref'}) != item['before_sha256']:
        raise AssertionError('Stage 5 historical source reconstruction changed')
    return before
