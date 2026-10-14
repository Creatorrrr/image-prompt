"""Root prepares fresh direct reviews after guard support, never signs proofs."""
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
import photo_semantic_evidence as native
import prepare_native_inputs as prep
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = HERE / 'native-inputs/guard-support-rechecks-plan-07-R02'


def read(name):
    return prep.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')
    return ref(str(path.relative_to(HERE)))


assert Path(native.__file__).is_relative_to(GEN)
assert hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest() == '6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
base = 'native-inputs/bounded-source-applications-plan-05/'
template = read(base + 'PLAN-01264.json')
current = prep.reviews.artifact(ROOT, template['current_proposal'])
assert c.digest(current) == '9ecd6dd135e49a9c5d41fb80ba1a9edfd22efd1de15b5d29ca5660bc0cc4d023'
order = prep.reviews.artifact(ROOT, template['order'])
OUT.mkdir(exist_ok=False)
requirements = save(OUT / 'ROOT-REQUIREMENTS.json', {
    'schema': 'photo-root-guard-role-fresh-review-requirements/v1', 'actor': '/root',
    'frozen_generation': str(GEN), 'native_raw_sha256': '6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9',
    'actual_read_count_created': 0, 'native_approvals': 0,
    'requirements': [
        'Actually directly read complete original/current/prior5B/ownbinding/selected reference closure/fullafter and all used full146V5 specs/neighbors. Preparation and helper validity confer no read count or semantics.',
        'Keep old04/05 drafts, unsigned facts and all failed precision/consumer checks immutable. Fresh proof must reflect current actual whole-source judgments, never re-sign the prior proof or fill absent scalar meaning automatically.',
        'Guard-only role support must name an actual own common or actual branch condition/rule/index/schema and direct ordinary positive quote in the same CID/RID, retain full spec and actual endpoints, and execute a verified predicate on an independent core. Scalar P facts or invented constant owner IDs are not relation substitutes.',
        '1264 retains the exact existing same-chair actual seat part and part_of relation without merging them; all11 scalar facts and chair orientation, seat disturbed state, seat recent history remain full actual E/receivers/locks.',
        '17437 requires all18 actual RIDs and full own source/profile/selected child closure, all204 prior precision occurrences and complete source units. Adult prerequisites, conditional youthful-adult styling, exact haughty-smug-poised baseline, cheek color not heat, and help/setback/recovery/history conditions retain their literal modes and scopes.',
        'Qualify direct normal facts, full source units, semantic references and guard refs separately. Sourcefit cannot grant adoption. Test full/compact/admission/actual oldbinding/profile conditions, absent-owner/wrong-guard provenance and each whole E/receiver/property/dimension lock.',
        'Use only frozen188c code for final checks while B2 working files change. No Gemini, model/provider execution, network, Git, operating/source/catalog/status/runtime mutation. All exact module hashes, fresh read boundary and failures must be recorded.']})
prepared = []
for ordinal, task, batch_name, selection_name, output_name in [
    (1264, '/root/review_11870_12250', 'native_batches/review11870-01264-05/BATCH.json', base + 'ORIGINAL-SELECTION-01264.json', 'review11870-01264-06'),
    (17437, '/root/review_08250_09250', 'native_batches/review08250-17437-04/BATCH.json', 'native-inputs/08250-special-11128-17437-plan-01/ORIGINAL-SELECTION-17437.json', 'review08250-17437-05'),
]:
    cid = order[ordinal]
    previous = read(batch_name)['records'][0]
    assert previous['candidate_id'] == cid and previous['proof'] is None
    assert set(read(selection_name)['records']) == {cid}
    plan = copy.deepcopy(template)
    plan.update(assignment={'task_name': task, 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'start': ordinal, 'end': ordinal + 1, 'ids': [cid]},
        original_selection=ref(selection_name), required_revisions={cid: {
            'prior_review': {'artifact': ref(batch_name), 'pointer': '/records/0', 'sha256': c.digest(previous)},
            'memo_artifacts': [requirements], 'reason': 'Fresh direct review on newly published exact guard-support contract, without source or prior proof conversion.'}},
        reason='Root assigns one complete direct recheck after actual guard-support publication; no source/proof/status approval from preparation.')
    plan_ref = save(OUT / f'PLAN-{ordinal:05d}.json', plan)
    directory, receipt = prep.write_inputs(plan_ref, output_name, actor='/root')
    prepared.append({'ordinal': ordinal, 'task': task, 'directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
save(OUT / 'ROOT-PREPARATION-VERIFICATION.json', {'schema': 'photo-root-guard-role-fresh-preparation/v1',
    'actor': '/root', 'prepared': prepared, 'requirements': requirements, 'prepared_count': 2,
    'actual_read_count_created_by_preparation': 0, 'native_approvals': 0,
    'source_catalog_binding_proof_status_operating_changes': 0, 'Gemini_calls': 0})
print(json.dumps({'prepared_count': 2, 'actual_reads_created': 0, 'native_approvals': 0}))
