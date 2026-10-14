"""Serialize root-selected literal source corrections into fresh review inputs.

All semantic choices below refer to individually authored whole before/after
records that root already read. This does not author facts, roles, modes,
signatures, approval statuses, or candidate read attestations.
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
GENERATION = '534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_candidate_corpus as corpus
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prepare
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]

OUT = HERE / 'native-inputs/11870-01250-01300-plan-03'


def read(name):
    return prepare.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': corpus.digest(read(name))}


def save(name, value, *, compressed=False):
    path = OUT / name
    raw = corpus.canonical_bytes(value) + b'\n'
    with path.open('xb') as stream:
        stream.write(gzip.compress(raw, mtime=0) if compressed else raw)
    return ref(str(path.relative_to(HERE)))


original = read('SOURCE.json.gz')
prior = read('native-inputs/first50-pending-source-plan-03/CURRENT-PROPOSAL.json.gz')
assert corpus.digest(original) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert corpus.digest(prior) == 'c72069b5c46207d63b950bfc26f8f7ac0f66d4cc1e3d0c02abedf64569265640'
catalog = read('CATALOG-FINAL-144-V4.json')
assert corpus.digest(catalog) == '5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
current = copy.deepcopy(prior)
current['slot_catalog'] = copy.deepcopy(catalog)
relation_name = 'authored/native_11870_formal02_1262_relation_revision_proposal_v1.json'
relation = read(relation_name)
assert corpus.digest(relation) == '1eaaac35a3c058c69da7b4439c194c05b14af2f32b00da2a507658726f46b5bc'
assert current['candidates'][relation['candidate_id']] == relation['source_current_formal02_full']
current['candidates'][relation['candidate_id']] = copy.deepcopy(relation['source_after_proposed_full'])
assert current['slot_bindings'] == original['slot_bindings']
assert current['policies'] == original['policies']
corpus.validate(current)
changes = {row['candidate_id']: copy.deepcopy(row) for row in
           read('native-inputs/08250-special-11128-17437-plan-01/SOURCE-APPROVAL.json')['changes']}
pending_name = 'authored/native_11870_first50_pending_resolution_v1.json'
pending = read(pending_name)
selected = [1258, 1264, 1265, 1272, 1275, 1278, 1280, 1286, 1296]
selected_rows = {row['candidate_id']: row for row in pending['records'] if row['ordinal'] in selected}
assert len(selected_rows) == 9
for cid, row in selected_rows.items():
    assert current['candidates'][cid] == row['source_after_proposed_full']
    reason = 'Root directly read and selected the complete literal proposal for fresh input only: ' + ' '.join(
        item['reason'] for item in row['exact_source_correction_proposals'])
    changes[cid] = {'candidate_id': cid, 'before': copy.deepcopy(original['candidates'][cid]),
        'after': copy.deepcopy(current['candidates'][cid]), 'delta': [], 'reason': reason,
        'provenance': [ref(pending_name), ref('native-inputs/first50-pending-source-plan-03/ROOT-SOURCE-SELECTION.json')]}
cid = relation['candidate_id']
changes[cid] = {'candidate_id': cid, 'before': copy.deepcopy(original['candidates'][cid]),
    'after': copy.deepcopy(current['candidates'][cid]), 'delta': [],
    'reason': 'Preserve the same actual announcing person using and holding the same raised gavel, with an independently frozen disjoint relation. Retain raised placement without adding a lifting trajectory, strike, hand geometry, profession or sale outcome. Exact newly authored relation proposal read by root; fresh input only.',
    'provenance': [ref(relation_name), ref('native_batches/review11870-01250-01300-02/ROOT-SEMANTIC-REOPEN-02.json')]}
# Mechanical delta serialization from the already selected complete records.
# No meaning, target, mode or field value is inferred here.
for cid, row in changes.items():
    if cid not in selected_rows and cid != relation['candidate_id']:
        assert row['after'] == current['candidates'][cid]
        continue
    before, after = row['before'], row['after']
    row['delta'] = [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key),
        'after_exists': key in after, 'after': after.get(key), 'reason': row['reason']}
        for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
changed = {cid for cid in original['candidates'] if original['candidates'][cid] != current['candidates'][cid]}
assert len(changed) == 45 and set(changes) == changed
OUT.mkdir(exist_ok=False)
snapshot = save('CURRENT-PROPOSAL.json.gz', current, compressed=True)
approval = {'schema': prepare.SOURCE, 'actor': '/root', 'original_source_sha256': corpus.digest(original),
    'current_source_sha256': corpus.digest(current), 'changes': [changes[cid] for cid in sorted(changes)],
    'binding_changes': [], 'policy_change': None,
    'reason': 'Preserve38 prior individually reviewed source changes, select9 literal pending-source proposals (2 overlap), and revise the same-announcer/gavel relation within the existing45 changed CIDs. Final144V4 is separately approved as fresh-review catalog. No proof, role/tag, read status or operating source is approved by preparation.'}
prepare.approve_source(ROOT, original, current, approval)
source_approval = save('SOURCE-APPROVAL.json', approval)
requirements = save('ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'prior_batch': ref('native_batches/review11870-01250-01300-02/BATCH.json'),
    'root_reopen': ref('native_batches/review11870-01250-01300-02/ROOT-SEMANTIC-REOPEN-02.json'),
    'independent_semantic_review': ref('worker-notes/native-evidence-11870-formal02-independent-semantic-review-20261015.json'),
    'neutral_witness_guide': {'file': 'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.md',
        'file_sha256': hashlib.sha256((ROOT / 'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.md').read_bytes()).hexdigest()},
    'final_catalog': ref('CATALOG-FINAL-144-V4.json'), 'source_approval': source_approval,
    'relation1262_proposal': ref(relation_name), 'pending_nine_proposals': ref(pending_name),
    'requirements': [
        'Actually read each complete original/current record, exact original5B row, own bindings, actual reference closure, all selected RID/profile/guard branches, each applicable complete144V4 specification and its relevant neighbors, and the exact prior judgement plus root/independent memos. Author fresh source-bound proof only after this read. No automatic old proof/catalog-hash/status conversion.',
        'The45-change snapshot includes the9 explicitly selected literal corrections and1262 relation correction. Other unresolved first50 records remain unresolved unless their entire actual meaning and conditions are resolved manually. Source1278 and1296 still lack the proposed source-local guard-v2 relationships in this input, so leave pending; do not synthesize or waive those relationships.',
        'Preserve all intrinsic source and exact old binding eligibility/display conditions. Do not infer human/age/body parts, type, material, actual owner or distinctness from role names, broad category or generic presence. Custom exact P remains a legitimate requirement when it matches complete actual meaning.',
        '1262 must retain the complete announcer-to-that-gavel relation, identical composite action value/operation/exact gavel receiver across EN/KO/application, retained raised placement and independently frozen actual disjoint relation. No invented lifting motion, striking, hand geometry, occupation, speech text or completed sale.',
        '1263/1269 retain independently positive atomic face/eyes/mouth/lips obligations on the actual declared carrier; no exact-body-array subset rule, inferred anatomy or face-to-eye retargeting.1284 remains pending under unchanged source/application owner ambiguity.',
        'Existing-owner selection may use the explicitly audited v3 selector contract only when independently frozen actual entity.presence and all precise P are already satisfied. Do not replace generic foreground or core_role names for an undeclared material surface. Keep required subject/event/concept E and locks intact.',
        'For one selected RID/actual owner/dimension/property, every E uses identical typed value/operation/actual receiver set. Actual owner aliases are equivalence only; part_of is not equality. P old value and E new value remain distinct. Branch/member source guards and source units must not be flattened.',
    ], 'prepared_count': 50, 'actual_read_count': 0, 'operational_native_qualified_count': 0,
    'root_acceptance_written': False, 'gemini_calls': 0,
})
old_plan = read('native-inputs/11870-01250-01300-plan-02/PLAN.json')
batch = read('native_batches/review11870-01250-01300-02/BATCH.json')
old_rows = {row['candidate_id']: (index, row) for index, row in enumerate(batch['records'])}
ids = old_plan['assignment']['ids']
plan = {key: copy.deepcopy(old_plan[key]) for key in
        ['schema', 'actor', 'original_snapshot', 'order', 'original_selection', 'assignment']}
plan.update(current_proposal=snapshot, catalog_approval=ref('NATIVE-CATALOG-APPROVAL-144-V4.json'),
    source_approval=source_approval, required_revisions={cid: {
        'prior_review': {'artifact': ref('native_batches/review11870-01250-01300-02/BATCH.json'),
            'pointer': '/records/' + str(old_rows[cid][0]), 'sha256': corpus.digest(old_rows[cid][1])},
        'memo_artifacts': [requirements],
        'reason': 'Fresh144V4 full-source direct review after literal source corrections, audited existing-owner selectors, and the exact1262 semantic reopen. Preserve original142 judgments as history; do not automatically convert them.'} for cid in ids},
    reason='Third immutable first50 input, latest144V4 with45 individually selected source changes. Preparation is bookkeeping only; fresh direct reads and individual semantic approval remain required.')
plan_ref = save('PLAN.json', plan)
output, receipt = prepare.write_inputs(plan_ref, 'review11870-01250-01300-03', actor='/root')
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
verification = save('ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-source45-input-verification/v1', 'actor': '/root',
    'source_snapshot': snapshot, 'source_approval': source_approval, 'plan': plan_ref,
    'catalog': ref('CATALOG-FINAL-144-V4.json'), 'source_changed_records': 45,
    'full18250_container_integrity': 'pass', 'exact_source_approval_validation': 'pass',
    'prepared_directory': str(output.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'],
    'actual_read_count': 0, 'native_approval_count': 0, 'canonical_changes': 0,
    'operational_qualified_count': 0, 'used_frozen_modules': modules,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0,
})
print(json.dumps({'snapshot': snapshot, 'prepared': str(output), 'verification': verification,
    'prepared_count': 50, 'actual_read_count': 0, 'native_approved': 0}))
