"""Prepare fresh special inputs from individually chosen complete source fixes.

Root's quote clarifications and single color-address correction are input
decisions only. No proof, signature, role or worker status is installed here.
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
OUT = HERE / 'native-inputs/08250-special-quote-color-plan-03'


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


def exact_differences(before, after, pointer=''):
    if type(before) is not type(after): return [(pointer, before, after)]
    if isinstance(before, dict):
        return sum([exact_differences(before.get(key), after.get(key), pointer + '/' + key) for key in sorted(before.keys() | after.keys())], [])
    if isinstance(before, list):
        if len(before) != len(after): return [(pointer, before, after)]
        return sum([exact_differences(left, right, pointer + '/' + str(index)) for index, (left, right) in enumerate(zip(before, after))], [])
    return [] if before == after else [(pointer, before, after)]


original = read('SOURCE.json.gz')
current = copy.deepcopy(read('native-inputs/root-00000-00020-plan-01/CURRENT-PROPOSAL.json.gz'))
assert c.digest(current) == 'f1a7b55527c677e3401a19aec37e57e36a0f07584c0464536bce8b9f141897be'
approval = copy.deepcopy(read('native-inputs/root-00000-00020-plan-01/SOURCE-APPROVAL.json'))
quote_name = 'authored/root_quote_local_source_clarifications_v1.json'
quote = read(quote_name)
assert c.digest(quote) == 'e9e62b4ce60d3fa42278afb0b9f8da4b6eebee6c155c77a785656476fa583a0b'
color_name = 'authored/native_resolution_08250_17437_144v4_source_proposal_02.json'
color = read(color_name)
assert c.digest(color) == '08e25e0777d1207b28ddbf074c4352f125308829819557f394e834998105b062'
assert hashlib.sha256((HERE / color_name).read_bytes()).hexdigest() == '1fbd7af42b486a8b21c09ad860911d3aaa683c1da187b21b19fb8adad0119864'
differences = exact_differences(color['source_before'], color['source_after'])
assert len(differences) == 6
assert {row[0] for row in differences} == {
    '/effects/realizations/branches/4/effects/properties/0/property',
    '/effects/realizations/branches/7/effects/properties/1/property',
    '/effects/realizations/branches/10/effects/properties/2/property',
    '/effects/realizations/branches/13/effects/properties/0/property',
    '/effects/realizations/branches/15/effects/properties/1/property',
    '/effects/realizations/branches/17/effects/properties/2/property'}
assert all(old == 'skin.state.localized_cheek_warm_color' and new == 'skin.color.localized_cheek_warm_color' for _, old, new in differences)
selected = [(row['candidate_id'], row['source_before'], row['source_after'], row['reason'], [ref(quote_name)]) for row in quote['records']]
selected.append((color['candidate_id'], color['source_before'], color['source_after'],
    'One visible local cheek color warming remains one appearance E. Replace its six actual color addresses, preserve exact dimensions/targets/E count/18 branch bodies/conditions and recovery relations. No separate skin-state, thermal, cosmetic, blood-flow or private-emotion proposition is added. Proposal01 duplicate effects are not selected.',
    [ref(color_name), ref('worker-notes/native-fresh-08250-17437-02-color-reassessment.json')]))
for cid, before, after, reason, provenance in selected:
    assert current['candidates'][cid] == before
    current['candidates'][cid] = copy.deepcopy(after)
    prior = next((row for row in approval['changes'] if row['candidate_id'] == cid), None)
    original_before = original['candidates'][cid]
    delta = [{'pointer': '/' + key, 'before_exists': key in original_before, 'before': original_before.get(key),
              'after_exists': key in after, 'after': after.get(key), 'reason': reason}
             for key in sorted(set(original_before) | set(after)) if original_before.get(key) != after.get(key)]
    replacement = {'candidate_id': cid, 'before': original_before, 'after': after,
        'delta': delta, 'reason': ((prior['reason'] + ' Further explicit input correction: ') if prior else '') + reason,
        'provenance': (prior['provenance'] if prior else []) + provenance}
    approval['changes'] = [row for row in approval['changes'] if row['candidate_id'] != cid] + [replacement]
approval['changes'].sort(key=lambda row: row['candidate_id'])
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Preserve the fifty prior whole-source input decisions and incorporate only four explicitly chosen current-source corrections: three quote-local clarifications and one six-address local cheek-color replacement. No proof/role/status/signature or operating source is installed.'
assert current['slot_bindings'] == original['slot_bindings'] and current['policies'] == original['policies']
c.validate(current)
prep.approve_source(ROOT, original, current, approval)
OUT.mkdir(exist_ok=False)
snapshot_ref = save('CURRENT-PROPOSAL.json.gz', current, compressed=True)
approval_ref = save('SOURCE-APPROVAL.json', approval)
requirements = save('ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'source_clarifications': ref(quote_name), 'color_source_proposal': ref(color_name),
    'exact_six_color_field_differences': differences,
    'root_source_input_selection_only': True,
    'requirements': [
        'Freshly read every complete original/current source, exact5B row, actual own binding, closure, all actual RIDs and optional/profile conditions/effects plus complete used final144V4 specs and neighbors. Do not copy/re-sign old proof, catalog hash or statuses.',
        '11128 common Korean now says 자연스럽게. Every common-Korean natural_standing/natural_walking fact must itself cite that complete qualifier, with correct branch. Retain wardrobe, adult P and actual standing/walking posture, walking-only action E, established-reference/identity preservation and all property locks.',
        '17437 keeps exactly eighteen existing realization choices and every optional expression/recovery/helper condition. Add only independently supported precise atomic face/eyes/eyelids/brow/mouth prerequisites demanded by the complete common text; no anatomy may be derived from face/category or introduced by the cue.',
        'The six cheek-color branches now have one skin.color.localized_cheek_warm_color E each. Review skin_tone from its actual color meaning. Do not retain skin_condition without separate positive state meaning and do not add duplicate skin-state E to force slot coverage. Physical thermal state, cosmetics and blood flow are not inferred.',
        'Keep youthful-adult age E, peer-rival actual endpoints, same owned face, half-lidded response, presentation/style/poise, all selected source units and existing/introduced scope, helper-only disjointness, recovery-only prior-disruption guards and independent optional clauses. Unknown whole meaning remains pending.',
        'Preserve source/binding conditions and exact typed values, operations, receiver sets; locks apply to whole actual E. No provider/Gemini/network, operating write, runtime publication or Git by reviewer.'
    ], 'prepared_count': 2, 'actual_read_count': 0, 'new_native_approvals': 0,
    'operational_native_qualified_count': 0, 'gemini_calls': 0})
results = []
for ordinal, old_plan_name, prior_name, batch_id in [
    (11128, 'PLAN-11128.json', 'native_batches/review08250-11128-03/BATCH.json', 'review08250-11128-04'),
    (17437, 'PLAN-17437.json', 'native_batches/review08250-17437-02/BATCH.json', 'review08250-17437-03')]:
    old = read('native-inputs/08250-special-catalog144-v4-plan-02/' + old_plan_name)
    cid = old['assignment']['ids'][0]
    prior = read(prior_name)
    assert len(prior['records']) == 1 and prior['records'][0]['candidate_id'] == cid
    plan = {key: copy.deepcopy(old[key]) for key in ['schema', 'actor', 'original_snapshot', 'order', 'original_selection', 'assignment', 'catalog_approval']}
    plan.update(current_proposal=snapshot_ref, source_approval=approval_ref,
        required_revisions={cid: {'prior_review': {'artifact': ref(prior_name), 'pointer': '/records/0', 'sha256': c.digest(prior['records'][0])},
            'memo_artifacts': [requirements, ref(quote_name) if ordinal == 11128 else ref(color_name)],
            'reason': 'Fresh explicit corrected-source review under identical144V4. Preserve exact prior judgment as history; no automatic proof or status promotion.'}},
        reason='Root-selected exact source input correction and fresh whole-native review only; no operating activation.')
    plan_ref = save(old_plan_name, plan)
    directory, receipt = prep.write_inputs(plan_ref, batch_id, actor='/root')
    results.append({'ordinal': ordinal, 'plan': plan_ref, 'prepared_directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
save('ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-special-corrected-input-verification/v1', 'actor': '/root',
    'snapshot': snapshot_ref, 'source_approval': approval_ref, 'results': results,
    'full18250_integrity_and_exact_source_approval_validation': 'pass',
    'four_individually_chosen_current_source_corrections': True,
    'source_changed_records_vs_original': len(approval['changes']),
    'catalog_sha256': c.digest(current['slot_catalog']), 'used_frozen_modules': modules,
    'prepared_count': 2, 'actual_read_count': 0, 'new_native_approvals': 0,
    'operational_changes': 0, 'os_network_denied': True, 'provider_keys_removed': True,
    'provider_or_embedding_calls': 0, 'gemini_calls': 0})
print(json.dumps({'results': results, 'source_sha256': c.digest(current), 'source_changed_records_vs_original': len(approval['changes']), 'native_approvals': 0}))
