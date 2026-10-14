"""Prepare four exact fresh review inputs; confer no native qualification."""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prep
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = HERE / 'native-inputs/bounded-source-applications-plan-05'


def read(name):
    return prep.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(path, value, *, compressed=False):
    data = c.canonical_bytes(value) + b'\n'
    with path.open('xb') as stream:
        stream.write(gzip.compress(data, mtime=0) if compressed else data)
    return ref(str(path.relative_to(HERE)))


original = read('SOURCE.json.gz')
base = 'native-inputs/11870-01250-01300-plan-04/'
current = copy.deepcopy(read(base + 'CURRENT-PROPOSAL.json.gz'))
assert c.digest(current) == '88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest() == '7d9f7e7c69bc1f8186af9a289eb46defd0e953de9c27d1b0b770142ad2660205'
two_name = 'authored/native_remaining12_owner_scope_revision_02.json'
three_name = 'authored/native_remaining12_owner_scope_revision_03.json'
two = read(two_name)
three = read(three_name)
assert hashlib.sha256((HERE / two_name).read_bytes()).hexdigest() == '4380afa92bf9259ad455c43c88bee28bd632cddd8ce702abcde427862af8447d'
rows02 = {row['ordinal']: row for row in two['records']}
grid = three['records'][0]
assert grid['ordinal'] == 1267
spatial = grid['options'][2]
assert spatial['option_id'] == 'spatial_illumination_grid_choice'
assert c.digest(spatial['source_after']) == '6b8a8eda599d3a511ca89d8d82b59eed97bd5b21aaa02a339277b0fd25cdcc87'
choices = [
    (1264, rows02[1264], rows02[1264], two_name, '/records/1',
     'Explicitly choose the existing same-chair seat-part application as an editorial clarification. The original wording does not uniquely prove this topology. Preserve chair AND actual seat part, exact part_of and distinct scopes, chair orientation E, disturbed seat E and recent prior-history E. Do not infer a cause, residue or current overturning action. The original and other unselected seating-place interpretations remain in history; they are not folded into this application.'),
    (1267, grid, spatial, three_name, '/records/0/options/2',
     'Explicitly choose spatial grid illumination from the selected actual shrine-lantern source in the same independently declared illuminated region. This is an editorial clarification, not an original OR or unique entailment. Preserve source-use and spatial-grid effects with the actual light/source/region closure; do not add a region, receiving surface, particles, shrine location, faith, color or intensity.'),
    (1285, rows02[1285], rows02[1285], two_name, '/records/2',
     'Explicitly choose the participant-counterpart chair clarification. Preserve all five stated effects: against-chair placement, propped state, support contact, counterpart role and chair association, with exact actual endpoint receivers. Require the independently declared existing objects and distinct participant relation endpoints. Do not silently convert the chosen mutable role or association to already-frozen prerequisites, legal ownership, occupancy, romance or an added participant.'),
]
selected = []
for ordinal, parent, choice, name, pointer, reason in choices:
    cid = parent['candidate_id']
    assert current['candidates'][cid] == parent['source_before'], ordinal
    assert original['candidates'][cid] == parent['original_source'], ordinal
    after = copy.deepcopy(choice['source_after'])
    assert c.digest(after) == choice['source_after_sha256']
    bindings = [row for row in current['slot_bindings'].values() if row['candidate_id'] == cid]
    assert sorted(bindings, key=lambda row: row['id']) == sorted(parent['complete_own_bindings_unchanged'], key=lambda row: row['id'])
    selected.append({'ordinal': ordinal, 'candidate_id': cid, 'source_before': copy.deepcopy(current['candidates'][cid]),
        'source_after': after, 'root_reason': reason, 'proposal': dict(ref(name), pointer=pointer),
        'owner_plans': choice['owner_plans'], 'manual_intent_not_native_proof': choice['manual_P_E_receiver_intent_not_a_native_proof'],
        'root_read_boundary': 'Complete original/current/after, actual own bindings, source E/guard/owner/receiver intent and historical original review were directly read in this continuous root task; no new whole18250 or whole146 personal read is claimed.',
        'native_approval': False})
    current['candidates'][cid] = after
selection = {'schema': 'photo-root-bounded-source-application-selection/v1', 'actor': '/root',
    'parent_current_source_sha256': '88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8',
    'selected_records': selected, 'selected_count': 3, 'research_input_only': True,
    'unresolved_source_application': [1299],
    '1257_source_unchanged_reference_completion_only': True,
    'native_proof_or_status_or_operating_changes': 0, 'gemini_calls': 0}
selection_name = 'ROOT-BOUNDED-SOURCE-APPLICATION-SELECTION-05.json'
selection_ref = save(HERE / selection_name, selection)
approval = copy.deepcopy(read(base + 'SOURCE-APPROVAL.json'))
for row in selected:
    cid = row['candidate_id']
    before, after = original['candidates'][cid], row['source_after']
    old = next((item for item in approval['changes'] if item['candidate_id'] == cid), None)
    delta = [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key), 'after_exists': key in after,
        'after': after.get(key), 'reason': row['root_reason']} for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
    replacement = {'candidate_id': cid, 'before': before, 'after': copy.deepcopy(after), 'delta': delta,
        'reason': ((old['reason'] + ' Additional expressly selected application: ') if old else '') + row['root_reason'],
        'provenance': (old['provenance'] if old else []) + [selection_ref]}
    approval['changes'] = [item for item in approval['changes'] if item['candidate_id'] != cid] + [replacement]
approval['changes'].sort(key=lambda row: row['candidate_id'])
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Retain all prior reviewed research revisions and add exactly three expressly selected bounded source clarifications. Source1257 stays unchanged for a fresh same-field/reference completion. No native proof, tag, status or operating activation is granted.'
assert current['slot_catalog'] == read('CATALOG-FINAL-146-V5.json')
assert current['slot_bindings'] == original['slot_bindings'] and current['policies'] == original['policies']
c.validate(current)
prep.approve_source(ROOT, original, current, approval)
OUT.mkdir(exist_ok=False)
snapshot = save(OUT / 'CURRENT-PROPOSAL.json.gz', current, compressed=True)
source_approval = save(OUT / 'SOURCE-APPROVAL.json', approval)
requirements = save(OUT / 'ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root', 'selection': selection_ref,
    'source_approval': source_approval, 'prepared_count': 4, 'actual_read_count': 0, 'native_approvals': 0,
    'requirements': [
        'Actually read the entire original/current/exact prior5B/ownbindings/reference closure/wholeafter plus complete used146V5 definitions and relevant neighbors. Reuse a prior direct read only at identical bytes with its exact attestation; never count preparation/hash/shape as new reading.',
        'The three selected application clarifications are editorial choices with explicit limits, not source-entailed topologies or an original OR. Retain each full actual guard, effect and complete receiver/owner closure. No extra count or participant is inferred.',
        'Source1257 is unchanged. The full EN qualitative light-drizzle/minimal umbrella-need degree can be a canonical direct fact; the whole application may be a manually reviewed partial restatement retaining evaluative/no-prop/no-safety constraints. Do not force its short light-drizzle quote to independently prove the full degree or delete the weather E.',
        'Use exact own positive field anchors and ordinary normal units; every reference is one-hop to an independent direct normal fact on the same actual CID/RID. Retain all remaining full-field constraints and old intrinsic plus binding gates.',
        'If a source relation is needed for semantic role support, preserve the source guard; do not fabricate a constant entity-ID scalar prerequisite, duplicate E, change permissions or hide a genuine role to make a proof pass. Keep a technical hold until the actual published contract supports it.',
        'Keep1299 hands-only exchange pending until its variable actual-member interpretation and runtime contract are independently resolved. No fake aggregate body owner or assumed number of hands/people.',
        'All original formal04 artifacts remain immutable. A new completion does not imply a fresh review of the other46 sources or their native approval. No Gemini/model/network/Git/operating writes/publication.'
    ]})
old = read(base + 'PLAN.json')
original_selection = prep.reviews.artifact(ROOT, old['original_selection'])
old_batch_name = 'native_batches/review11870-01250-01300-04/BATCH.json'
old_batch = read(old_batch_name)
prior = {row['ordinal']: (index, row) for index, row in enumerate(old_batch['records'])}
order = prep.reviews.artifact(ROOT, old['order'])
prepared = []
for ordinal in [1257, 1264, 1267, 1285]:
    cid = order[ordinal]
    selection_one = copy.deepcopy(original_selection)
    selection_one['records'] = {cid: selection_one['records'][cid]}
    selection_one['reason'] = 'Exact historical original selection for one expressly assigned bounded fresh completion; all prior rows remain unchanged.'
    one_ref = save(OUT / f'ORIGINAL-SELECTION-{ordinal:05d}.json', selection_one)
    index, previous = prior[ordinal]
    plan = {key: copy.deepcopy(old[key]) for key in ['schema', 'actor', 'original_snapshot', 'order', 'catalog_approval']}
    plan.update(current_proposal=snapshot, source_approval=source_approval, original_selection=one_ref,
        assignment={'task_name': '/root/review_11870_12250', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
            'start': ordinal, 'end': ordinal + 1, 'ids': [cid]},
        required_revisions={cid: {'prior_review': {'artifact': ref(old_batch_name), 'pointer': '/records/' + str(index), 'sha256': c.digest(previous)},
            'memo_artifacts': [requirements], 'reason': 'Fresh single-source direct completion after explicit editorial application or source-local reference repair; prior04 pending status/proof remains immutable.'}},
        reason='Prepare one exact current source for bounded fresh manual review, not automatic proof/status conversion.')
    plan_ref = save(OUT / f'PLAN-{ordinal:05d}.json', plan)
    directory, receipt = prep.write_inputs(plan_ref, f'review11870-{ordinal:05d}-05', actor='/root')
    prepared.append({'ordinal': ordinal, 'directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
save(OUT / 'ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-bounded-source-application-preparation/v1', 'actor': '/root',
    'source': snapshot, 'source_approval': source_approval, 'source_changed_records_vs_original': len(approval['changes']),
    'new_source_choices': 3, 'prepared': prepared, 'actual_read_count_created_by_preparation': 0,
    'native_proof_or_status_or_operating_changes': 0, 'actual_frozen_modules': modules,
    'full18250_source_and_catalog_container_and_approval_validation': True,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0})
print(json.dumps({'source_sha256': c.digest(current), 'selected_source_choices': 3, 'prepared_count': 4, 'actual_read_count': 0, 'native_approvals': 0}))
