"""Prepare two explicitly reopened research inputs; never rewrite old proofs.

All semantic decisions in the root memos below were read and authored by root.
Loops only bind the already frozen row/artifact identities and prepare inputs.
No source/body/effect/tag change, proof, read attestation or acceptance is made.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import native_reviews as reviews
import prepare_native_inputs as prepare

c = reviews.dr.c


def ref(path):
    path = ROOT / path if not isinstance(path, Path) else path
    value = reviews.read_json(path)
    return dict(file=str(path.relative_to(ROOT)),
                file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                sha256=c.digest(value))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')
    return ref(path)


common_plan = reviews.read_json(HERE / 'native-inputs/08250-special-11128-17437-plan-01/PLAN-11128.json')
fifty_old = HERE / 'native_batches/review11870-01250-01300-01'
fifty_batch = reviews.read_json(fifty_old / 'BATCH.json')
fifty_dir = HERE / 'native-inputs/11870-01250-01300-plan-02'
guide = ROOT / 'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.md'
fifty_memo = write(fifty_dir / 'ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'prior_batch': ref(fifty_old / 'BATCH.json'),
    'prior_note': ref(fifty_old / 'NOTE.json'),
    'prior_root_reopen': ref(fifty_old / 'ROOT-REVIEW-REOPEN-01.json'),
    'namespace_proposal': ref(HERE / 'authored/native_11870_first50_prereq_namespace_revision_v1.json'),
    'namespace_note': ref(HERE / 'worker-notes/native-11870-first50-prereq-namespace-revision-v1.json'),
    'guide': {'file': str(guide.relative_to(ROOT)),
              'file_sha256': hashlib.sha256(guide.read_bytes()).hexdigest()},
    'root_read': 'Read all32 proposed source en/ko/application summaries and all50 exact before/after prerequisite tuples with reasons. This is not a claim to have personally read every whole proof or all50 complete originals.',
    'requirements': [
        'Freshly read whole original/current source, every selected RID/profile/guard/dependency, exact original 5B row and own bindings, final142 V2 specs and all exact revision memos. New proof and read attestation only after that read; old files stay byte-identical.',
        'Manually review the26 common presence tuple changes against neutral shared tuple conventions. No alias, copied signature, automatic re-signing or core tailored to the candidate.',
        '1263 and1269 express minimum carrier parts, not exhaustive anatomy. Manually author independent atomic eyes/mouth/lips prerequisites actually required by the whole source; do not implement global array-subset matching.',
        '1284 current eye-to-primary_face mapping has unresolved owner scope. Keep pending unless a separately explicit whole-source/application revision is reviewed and approved. A face is not silently an eye.',
        'The16 custom prerequisites are not automatically invalid or replaceable by generic existence. Keep their precise type/material/anatomy/owner constraints, or record a specific unresolved contract. Independently supplied exact witnesses are necessary for admission.',
        'For the same RID, actual owner, dimension and property, all effect assignments need identical typed value, operation and receiver set. Preserve legitimate prerequisite old-value versus effect new-value differences. No synonym/partial merge shortcuts.',
        'All18 previously pending rows stay pending unless actually resolved by the assigned source contract. No pending-resolution source proposals are applied in this input. Generic-owner cases wait for the explicit owner selector contract rather than arbitrary foreground restrictions.'
    ],
    'source_after_changed': False, 'proof_written': False,
    'root_acceptance_written': False, 'operational_native_qualified_count': 0,
    'gemini_calls': 0,
})
plan = reviews.read_json(HERE / 'native-inputs/11870-01250-01300-plan-01/PLAN.json')
plan = copy.deepcopy(plan)
for key in ('current_proposal', 'source_approval'):
    plan[key] = copy.deepcopy(common_plan[key])
plan['required_revisions'] = {}
for index, row in enumerate(fifty_batch['records']):
    cid = row['candidate_id']
    plan['required_revisions'][cid] = {
        'prior_review': {'artifact': ref(fifty_old / 'BATCH.json'),
                         'pointer': f'/records/{index}', 'sha256': c.digest(row)},
        'memo_artifacts': [fifty_memo],
        'reason': 'Explicit fresh review after root reproduced neutral prerequisite interoperability failure. Exact old judgement preserved; source unchanged; atomic carrier/owner/E-assignment issues require individual direct review.'}
plan['reason'] = 'Second immutable50 input: current38-change research source only; reopen all exact frozen judgements for neutral witnesses and individual semantics. No automatic proof/read/status/native approval.'
plan_ref = write(fifty_dir / 'PLAN.json', plan)
output, receipt = prepare.write_inputs(plan_ref, 'review11870-01250-01300-02', actor='/root')
print(json.dumps({'prepared': str(output.relative_to(ROOT)), 'count': receipt['prepared_count'], 'read': receipt['actual_read_count']}))

single_old = HERE / 'native_batches/review08250-11128-01'
single_batch = reviews.read_json(single_old / 'BATCH.json')
assert len(single_batch['records']) == 1
single_dir = HERE / 'native-inputs/08250-11128-plan-02'
single_memo = write(single_dir / 'ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'prior_batch': ref(single_old / 'BATCH.json'),
    'prior_note': ref(single_old / 'NOTE.json'),
    'actual_root_verification': ref(single_old / 'ROOT-VERIFICATION-01.json'),
    'literal_value_proposal': ref(HERE / 'authored/native_fresh_08250_11128_01_value_revision_proposal.json'),
    'literal_value_note': ref(HERE / 'worker-notes/native-fresh-08250-11128-01-value-revision.json'),
    'root_read': 'Previously read whole original/current11128 source; now read all71 exact facts,26 units and full proof metadata. Read both exact value revisions and complete rationale. Shape/source/catalog/provenance verifier passed, but semantic effect assignment conflict blocks root acceptance.',
    'requirements': [
        'Freshly reread the exact assigned full original/current/standing/walking sources, guards, effects, profile body, source units, own bindings and original compiled judgement; preserve the previous BATCH/NOTE bytes.',
        'Manually use natural_standing and natural_walking for the two identified body.pose effects after the full selected source reread. The shorter common Korean quote supports posture only; selected full body supplies naturalness. It must not be called standalone entailment.',
        'Every same-RID actual owner/dimension/property effect must have one exact typed value/operation/receiver set; no automatic synonym alias or change to source/body/effect fields.',
        'Retain independent adult/scope prerequisite and known-present/absent/unknown guard boundaries; repeat actual full/compact admission and final preservation evidence checks. New required-revision proof and read declaration are mandatory.'
    ],
    'source_after_changed': False, 'old_shape_valid': True,
    'old_root_accepted': False, 'proof_written': False,
    'root_acceptance_written': False, 'operational_native_qualified_count': 0,
    'gemini_calls': 0,
})
plan = copy.deepcopy(common_plan)
row = single_batch['records'][0]
plan['required_revisions'] = {row['candidate_id']: {
    'prior_review': {'artifact': ref(single_old / 'BATCH.json'),
                     'pointer': '/records/0', 'sha256': c.digest(row)},
    'memo_artifacts': [single_memo],
    'reason': 'Fresh proof must explicitly supersede two conflicting effect values after direct full-source reread, without changing the source or silently re-signing the old shape-valid proof.'}}
plan['reason'] = 'Second immutable11128 input for two explicitly reviewed canonical effect values; source unchanged; preparation is not reading or approval.'
plan_ref = write(single_dir / 'PLAN.json', plan)
output, receipt = prepare.write_inputs(plan_ref, 'review08250-11128-02', actor='/root')
print(json.dumps({'prepared': str(output.relative_to(ROOT)), 'count': receipt['prepared_count'], 'read': receipt['actual_read_count']}))
