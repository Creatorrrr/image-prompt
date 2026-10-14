"""Prepare root's first20 against five manually read literal source corrections.

This serializes exact previously authored records. No native proof, candidate
status, role/mode assignment, signature or read attestation is created here.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prep
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
OUT = HERE / 'native-inputs/root-00000-00020-plan-01'


def read(name):
    return prep.reviews.read_json(HERE / name)


def artifact(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(name, value, *, compressed=False):
    path = OUT / name
    data = c.canonical_bytes(value) + b'\n'
    with path.open('xb') as stream:
        stream.write(gzip.compress(data, mtime=0) if compressed else data)
    return artifact(str(path.relative_to(HERE)))


original = read('SOURCE.json.gz')
current = copy.deepcopy(read('native-inputs/11870-01250-01300-plan-03/CURRENT-PROPOSAL.json.gz'))
assert c.digest(current) == '30924a72de7d3011af26b7ef7c0192ff12edd732131f3c18ed29748e805d5477'
proposal_name = 'authored/root_00000_00020_source_proposals_v1.json'
proposals = read(proposal_name)
assert c.digest(proposals) == '126f79a98640bfadedd40607cc92ff9830f8fda80f5a9eebe1777f7db4478629'
approval = copy.deepcopy(read('native-inputs/11870-01250-01300-plan-03/SOURCE-APPROVAL.json'))
for row in proposals['records']:
    cid = row['candidate_id']
    assert original['candidates'][cid] == current['candidates'][cid] == row['source_original_full']
    current['candidates'][cid] = copy.deepcopy(row['source_after_proposed_full'])
    before, after = row['source_original_full'], row['source_after_proposed_full']
    delta = [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key),
        'after_exists': key in after, 'after': after.get(key), 'reason': row['reason']}
        for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
    approval['changes'].append({'candidate_id': cid, 'before': before, 'after': after, 'delta': delta,
        'reason': row['reason'], 'provenance': [artifact(proposal_name), artifact('worker-notes/root-00000-00020-source-proposals-reread-01.json')]})
approval['changes'].sort(key=lambda row: row['candidate_id'])
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Preserve45 exact previous individually reviewed input corrections and select the5 complete literal root corrections after their whole after reread. No new proof/role/status/signature is installed. Catalog144V4 and bindings/policies are unchanged from the45-change input.'
assert len(approval['changes']) == 50
c.validate(current)
prep.approve_source(ROOT, original, current, approval)
OUT.mkdir(exist_ok=False)
snapshot_ref = save('CURRENT-PROPOSAL.json.gz', current, compressed=True)
approval_ref = save('SOURCE-APPROVAL.json', approval)
historical = read('decisions/batch_00000_00020.json')
order = read('ORDER.json')
compiled_path = HERE / 'decisions/batch_00000_00020.json'
compiled_sha = hashlib.sha256(compiled_path.read_bytes()).hexdigest()
selection_ref = save('ORIGINAL-SELECTION.json', {'schema': prep.SELECTION, 'actor': '/root',
    'original_source_sha256': c.digest(original), 'records': {cid: {
        'locator': {'file': str(compiled_path.relative_to(ROOT)), 'file_sha256': compiled_sha,
            'item': index + 1, 'row_sha256': c.digest(historical['decisions'][index])},
        'packet': artifact('packets/00000-020.json'),
        'reason': 'Exact original compiled item and whole source packet directly read by root; five literal corrections are separate fresh source decisions.'}
        for index, cid in enumerate(order[:20])}, 'reason': 'Root explicitly selects the first20 exact original compiled rows and full original packet; no old statuses are converted.'})
memo_ref = save('ROOT-REVIEW-REQUIREMENTS.json', {'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'proposal': artifact(proposal_name), 'after_reread': artifact('worker-notes/root-00000-00020-source-proposals-reread-01.json'),
    'final_catalog': artifact('CATALOG-FINAL-144-V4.json'),
    'requirements': [
        'Freshly read original/current source and exact5B row, own bindings, actual complete closure and actual RID/effects/conditions; manually author source units, owners, typed modes/values and role support against144V4. Preparation supplies no native proof or new read attestation.',
        'Select only explicit source-positive effects/prerequisites/context; preserve lens named classifications separately from sensor-dependent field of view, and mood from optical focus or private emotion. Do not assert physical motion from recorded blur.',
        'Keep light source/modifier carrier uncertainty, pet/food/interior theme obligations and actual-day-phase versus imitation-light ambiguity pending until each whole application is explicitly adjudicated. No metadata-to-positive-fact conversion or silent loss of source meaning.',
        'Old genre3/4 proofs remain immutable142 history; re-read complete source and final specification before writing any new proof. No auto re-signing or status reuse.'
    ], 'actual_read_count': 0, 'native_approved': 0, 'operational_changes': 0, 'gemini_calls': 0})
plan = {'schema': prep.PLAN, 'actor': '/root', 'original_snapshot': artifact('SOURCE.json.gz'),
    'current_proposal': snapshot_ref, 'order': artifact('ORDER.json'),
    'catalog_approval': artifact('NATIVE-CATALOG-APPROVAL-144-V4.json'),
    'source_approval': approval_ref, 'original_selection': selection_ref,
    'assignment': {'task_name': '/root', 'model': None, 'reasoning_effort': None,
        'start': 0, 'end': 20, 'ids': order[:20]}, 'required_revisions': {},
    'reason': 'Root explicitly prepares a fresh first20 final144V4 review with50 whole-source input corrections. All actual review judgements remain manual; ambiguous cues may remain pending.'}
old_genres = read('native_batches/root-genre-00003-00005-02/BATCH.json')
for index, cid in enumerate(order[:20]):
    old = historical['decisions'][index]
    prior = {'artifact': artifact('decisions/batch_00000_00020.json'), 'pointer': '/decisions/' + str(index), 'sha256': c.digest(old)}
    if index in (3, 4):
        prior = {'artifact': artifact('native_batches/root-genre-00003-00005-02/BATCH.json'),
            'pointer': '/records/' + str(index-3), 'sha256': c.digest(old_genres['records'][index-3])}
    plan['required_revisions'][cid] = {'prior_review': prior, 'memo_artifacts': [memo_ref],
        'reason': 'Exact original or prior native judgement retained; new144V4 source-bound individual native review, without automatically promoting old data.'}
plan_ref = save('PLAN.json', plan)
output, receipt = prep.write_inputs(plan_ref, 'root-00000-00020-01', actor='/root')
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(FROZEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
verification_ref = save('ROOT-PREPARATION-VERIFICATION.json', {'schema': 'photo-root-native-input-verification/v1',
    'snapshot': snapshot_ref, 'source_approval': approval_ref, 'plan': plan_ref, 'prepared_count': 20,
    'actual_read_count': 0, 'native_approved': 0, 'source_changed_records': 50,
    'full18250_container_integrity': 'pass', 'used_frozen_modules': modules,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0,
    'canonical_changes': 0, 'operational_native_qualified_count': 0})
print(json.dumps({'prepared': str(output), 'snapshot': snapshot_ref, 'verification': verification_ref,
    'prepared_count': 20, 'actual_read_count': receipt['actual_read_count'], 'native_approved': 0}))
