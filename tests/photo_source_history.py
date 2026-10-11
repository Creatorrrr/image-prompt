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


def before_stage05_subject_context(current, source_file, *, root=ROOT):
    """Reverse only authenticated deltas; reject every unreviewed live field."""
    item = subject_context_transition(root=root)['sources'][Path(source_file).name]
    if str(source_file) != item['source_file']:
        raise AssertionError('Unexpected stage 5 source path')
    body = {k: v for k, v in current.items() if k != 'maintenance_ref'}
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
