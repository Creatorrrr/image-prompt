"""Root reopens four field-local anchors; source and five effects stay exact."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore'), str(HERE)]
import photo_candidate_corpus as c
import prepare_native_inputs as prep
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = HERE / 'native-inputs/partner-chair-quote-recheck-plan-08'


def read(name):
    return prep.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')
    return ref(str(path.relative_to(HERE)))


batch_name = 'native_batches/review11870-01285-05/BATCH.json'
batch = read(batch_name)
assert c.digest(batch) == 'ed905ae65160c2d3c9aaf3a4aedf5d09dc1160dcbb11b8e9cd678a8c6a8966ad'
row = batch['records'][0]; proof = row['proof']; cid = row['candidate_id']
assert row['status'] == 'approved' and len(proof['facts']) == 19
bad = [fact for fact in proof['facts'] if fact['id'] in {'counterpartEN', 'counterpartKO', 'assocEN', 'assocKO'}]
assert len(bad) == 4 and len(proof['effect_sets']['base']['properties']) == 5
memo = save(HERE / 'native_batches/review11870-01285-05/ROOT-SEMANTIC-REOPEN-01.json', {
    'schema': 'photo-root-field-local-semantic-reopen/v1', 'actor': '/root',
    'batch': ref(batch_name), 'candidate_id': cid, 'status': 'hold_fresh_field_local_reanchors_required',
    'root_direct_read': 'Whole current05 source, all19 actual facts, all3 whole units, all5 roles, owner maps, source guards/effect set/dependencies/profile and whole relevant role specs; earlier original/current/5B/ownbinding/source-choice read retained at unchanged bytes.',
    'affected_facts': bad,
    'finding': 'The short partner chair / 상대 의자 quotes do not independently state the full two-actual-participant counterpart relationship and same selected counterpart association. The explicit application does. Source-wide disambiguation must not be silently transferred into field-local direct canonical anchors.',
    'direct_path_control': 'participant_role already supports actual relationship.role.counterpart dimension/prefix; this is quote precision, not a generic role projection gap.',
    'source_and_effects_must_remain': 'All exact source text, four actual existing selected endpoints, three original source guards and five complete chosen E groups/targets/receivers/whole locks remain unchanged.',
    'repair_direction': 'Fresh manual review can use the complete own application as canonical direct counterpart/association facts, and separately reviewed one-hop partial references from the original short fields. Preserve their local placement/state/support meanings. Do not delete genuine E or convert it to P.',
    'shape_and_prior_consumers_do_not_establish_field_local_entailment': True,
    'old_batch_note_proof_or_status_modified': False, 'root_acceptance': False,
    'native_operating_qualified_records': 0, 'Gemini_calls': 0})
OUT.mkdir(exist_ok=False)
template = read('native-inputs/bounded-source-applications-plan-05/PLAN-01285.json')
plan = copy.deepcopy(template)
plan['required_revisions'] = {cid: {'prior_review': {'artifact': ref(batch_name), 'pointer': '/records/0', 'sha256': c.digest(row)},
    'memo_artifacts': [memo], 'reason': 'Root HOLD of four over-complete field-local language anchors; fresh direct source review and source-local references, no source/effect conversion.'}}
plan['reason'] = 'Prepare one fresh1285 field-local proof repair after root meaning review. Source, catalog and all five actual effects stay exact.'
plan_ref = save(OUT / 'PLAN-01285.json', plan)
directory, receipt = prep.write_inputs(plan_ref, 'review11870-01285-06', actor='/root')
save(OUT / 'ROOT-PREPARATION-VERIFICATION.json', {'schema': 'photo-root-partner-chair-field-recheck-preparation/v1',
    'actor': '/root', 'plan': plan_ref, 'root_reopen': memo,
    'prepared': [{'ordinal': 1285, 'directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0}],
    'actual_read_count_created_by_preparation': 0, 'source_catalog_binding_or_proof_status_changes': 0,
    'native_approvals': 0, 'Gemini_calls': 0})
print(json.dumps({'prepared_count': 1, 'new_reads_from_preparation': 0, 'root_hold': 1, 'native_approvals': 0}))
