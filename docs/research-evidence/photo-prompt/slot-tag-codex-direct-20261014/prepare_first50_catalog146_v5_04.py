"""Prepare a fresh first50 review from the reviewed146 catalog/source choices.

No existing proof, mode, status or read attestation is converted. Only exact
root-selected source records and prior source approvals are serialized here.
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
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prep
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = HERE / 'native-inputs/11870-01250-01300-plan-04'


def read(name):
    return prep.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(name, value, *, compressed=False):
    path = OUT / name
    data = c.canonical_bytes(value) + b'\n'
    with path.open('xb') as stream:
        stream.write(gzip.compress(data, mtime=0) if compressed else data)
    return ref(str(path.relative_to(HERE)))


original = read('SOURCE.json.gz')
current = copy.deepcopy(read('native-inputs/08250-special-quote-color-plan-03/CURRENT-PROPOSAL.json.gz'))
assert c.digest(current) == '9df8f1fdc5506ff1a74caa615bf985d7e528a992e7809fa52003b3848414ec38'
approval = copy.deepcopy(read('native-inputs/08250-special-quote-color-plan-03/SOURCE-APPROVAL.json'))
selection_name = 'ROOT-FIRST50-SOURCE-APPLICATION-SELECTION-04.json'
selection = read(selection_name)
assert c.digest(selection) == 'ec36f900a2bbd0fa5558c87be3ce11546a4b26ec29ba313fcfb73934c7a75007'
catalog = read('CATALOG-FINAL-146-V5.json')
assert c.digest(catalog) == '3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
current['slot_catalog'] = copy.deepcopy(catalog)
for row in selection['selected_records']:
    cid = row['candidate_id']
    assert current['candidates'][cid] == row['source_before']
    current['candidates'][cid] = copy.deepcopy(row['source_after'])
    old = next((item for item in approval['changes'] if item['candidate_id'] == cid), None)
    before, after = original['candidates'][cid], row['source_after']
    delta = [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key), 'after_exists': key in after, 'after': after.get(key), 'reason': row['root_reason']}
             for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
    assert delta
    replacement = {'candidate_id': cid, 'before': before, 'after': copy.deepcopy(after), 'delta': delta,
        'reason': ((old['reason'] + ' Further explicitly selected source application: ') if old else '') + row['root_reason'],
        'provenance': (old['provenance'] if old else []) + [ref(selection_name), ref('ROOT-FIRST50-SOURCE-APPLICATION-VERIFICATION-04.json')]}
    approval['changes'] = [item for item in approval['changes'] if item['candidate_id'] != cid] + [replacement]
approval['changes'].sort(key=lambda item: item['candidate_id'])
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Preserve all prior individually reviewed source inputs and add exactly the14 root-selected complete application revisions. New146V5 catalog is separately approved for fresh review only. No proof, role, tag, status or operating source is changed.'
assert current['slot_bindings'] == original['slot_bindings'] and current['policies'] == original['policies']
c.validate(current)
prep.approve_source(ROOT, original, current, approval)
OUT.mkdir(exist_ok=False)
snapshot = save('CURRENT-PROPOSAL.json.gz', current, compressed=True)
source_approval = save('SOURCE-APPROVAL.json', approval)
requirements = save('ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'catalog': ref('CATALOG-FINAL-146-V5.json'), 'source_application_selection': ref(selection_name),
    'prior_batch': ref('native_batches/review11870-01250-01300-03/BATCH.json'),
    'prior_root_reopen': ref('native_batches/review11870-01250-01300-03/ROOT-SEMANTIC-REOPEN-01.json'),
    'source_quote_clarifications': ref('authored/root_quote_local_source_clarifications_v1.json'),
    'source_approval': source_approval,
    'requirements': [
        'Actually read each full original/current record, exact original5B row and ownbinding, actual complete reference closure, all source clauses/control fields/actual RIDs and profile/optional conditions/effects, complete applicable146V5 definitions and relevant neighbors. The136 unchanged specs retain explicit prior read provenance only when their exact bytes and actual prior read are established. No new whole146 read count from hashes.',
        'Author fresh exact-source native evidence after direct review. Do not copy/re-sign prior proof, catalog hash, mode or statuses. Preserve the exact03 prior judgment and root reopen per CID as history.',
        '1250 fleeting caught softening now has its own complete Korean translation/application.1251 source is unchanged: use full 얼굴을 꽉 채우는 뷰티 클로즈업 for face-tight extent rather than only 뷰티 클로즈업.1289 inside now appears in EN/KO/application itself. Never borrow a qualifier from a different pointer, language or optional branch.',
        'The14 source applications are1253/1255/1256/1258/1266/1271/1273/1275/1278/1284/1287/1290/1295/1296. Use their actual complete after, guards and effects.1255 replaces dangling below with explicit actual receiver prose. Source-input selection grants no native mode, role, value or core evidence.',
        '1290 keeps sticky tropical weather and separately explicit material thermal.state.ambient hot on the same independently selected scene/environment. No extra air node or humidity/sweat inference.1295 keeps two local aged/young skin assignments with consistently scoped appearance and age projections; no chronological age, human P, baby, family or extra owner.',
        '1278 blank face and warm/helpful impression are separate actual effects; impression is not physical warmth or a helping act.1296 preserves physically warm mug, exactly two distinct participating hands belonging to the same actual holder, holding and wrapping contact. English held alone cannot prove wrapping; use actual KO/application. Do not turn participating two into total anatomy inventory.',
        'Keep1264/1267/1285/1299 pending unless a complete separately root-reviewed source resolution is supplied. No forced chair-seat part, projected surface/array count, counterpart relationship or fake aggregate hands-only scope. No source effect removal to force approval.',
        'Retain every intrinsic source and exact old binding eligibility/display guard conjunctively. Actual skin, face/eyes/parts/type, existing/disjoint/part relations and exact receiver sets need independently declared core evidence. Category labels and presence do not donate anatomy, substance or a primary owner.',
        'For actual equivalent owners and one selected RID/dimension/property, all E assignments use identical value/operation/receiver set. part_of is not equality. P old value and E new value remain distinct; whole E locks stay strict. All mandatory child and explicitly selected optional effects remain in joint admission.',
        'Do not use Gemini, providers, network, operating writes, runtime publication, registration/global promotion or Git. Do not claim shape/hash/consumer fixtures prove visual semantics or pixels.'
    ], 'prepared_count': 50, 'actual_read_count': 0, 'candidate_native_approvals': 0, 'operating_changes': 0, 'gemini_calls': 0})
old = read('native-inputs/11870-01250-01300-plan-03/PLAN.json')
batch_name = 'native_batches/review11870-01250-01300-03/BATCH.json'
batch = read(batch_name)
prior_rows = {row['candidate_id']: (index, row) for index, row in enumerate(batch['records'])}
plan = {key: copy.deepcopy(old[key]) for key in ['schema', 'actor', 'original_snapshot', 'order', 'original_selection', 'assignment']}
plan.update(current_proposal=snapshot, catalog_approval=ref('NATIVE-CATALOG-APPROVAL-146-V5.json'), source_approval=source_approval,
    required_revisions={cid: {'prior_review': {'artifact': ref(batch_name), 'pointer': '/records/' + str(prior_rows[cid][0]), 'sha256': c.digest(prior_rows[cid][1])},
        'memo_artifacts': [requirements], 'reason': 'Fresh whole-source direct review under exact146V5 after explicit source/quote/owner application corrections; prior03 remains immutable, with no automatic status or proof conversion.'} for cid in plan['assignment']['ids']},
    reason='Fourth immutable first50 input. Exact146V5 and14 selected source applications plus prior quote fixes; fresh complete direct semantic/native review only, not operating activation.')
plan_ref = save('PLAN.json', plan)
directory, receipt = prep.write_inputs(plan_ref, 'review11870-01250-01300-04', actor='/root')
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
verification = save('ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-first50-catalog146-input-verification/v1', 'actor': '/root',
    'snapshot': snapshot, 'source_approval': source_approval, 'plan': plan_ref,
    'catalog': ref('CATALOG-FINAL-146-V5.json'), 'source_changed_records_vs_original': len(approval['changes']),
    'new_individually_selected_source_revisions': 14, 'full18250_container_and_exact_source_approval_validation': 'pass',
    'prepared_directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0,
    'candidate_native_approvals': 0, 'operating_changes': 0, 'used_frozen_modules': modules,
    'os_network_denied': True, 'provider_keys_removed': True, 'local_inference_calls': 0, 'gemini_calls': 0})
print(json.dumps({'prepared': str(directory.relative_to(ROOT)), 'source_sha256': c.digest(current), 'source_changed_records': len(approval['changes']), 'catalog_count': len(catalog), 'prepared_count': 50, 'actual_read_count': 0, 'candidate_approvals': 0}))
