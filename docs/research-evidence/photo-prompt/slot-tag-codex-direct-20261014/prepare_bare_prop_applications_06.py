"""Prepare four individually selected prop applications, never approve proofs."""
from __future__ import annotations
import copy
import gzip
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
OUT = HERE / 'native-inputs/bare-prop-applications-plan-06'


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
base = 'native-inputs/bounded-source-applications-plan-05/'
current = copy.deepcopy(read(base + 'CURRENT-PROPOSAL.json.gz'))
assert c.digest(current) == '9ecd6dd135e49a9c5d41fb80ba1a9edfd22efd1de15b5d29ca5660bc0cc4d023'
assert hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest() == '6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
name = 'authored/native_06250_bare_props_01236_00259_00807_00924_C_20261015.json'
assert ref(name)['file_sha256'] == 'a327680e9a9370f7dce922a61b26ffe4cf630088b28c331d521af1a6919db2f7'
proposal = read(name)
reasons = {
    1236: 'Individually choose adding one new astronaut-helmet scene prop; the bare noun alone did not uniquely determine addition. Preserve original EN/KO/embedding exactly. KO helmet supplies only the helmet type component, not prop status/addition/count. No head, wearer, astronaut occupation, space scene or breathing performance is selected.',
    259: 'Individually choose adding one new socket-wrench prop with full subject/count effects. Preserve original labels, intrinsic human condition and actual binding. This does not select a worker, repair, garage, vehicle, bolt contact or placement.',
    807: 'Individually choose adding one new stethoscope prop with full subject/count effects. The bare original fields restate only its type; do not infer a doctor, patient, wearing, examination, contact or medical result.',
    924: 'Individually choose adding one new conch-shell prop with full subject/count effects. Preserve original labels and intrinsic human condition; no living conch, mermaid, sound, sea location or detailed shell anatomy is selected.',
}
selected = []
for index, row in enumerate(proposal['records']):
    ordinal, cid = row['ordinal'], row['candidate_id']
    assert ordinal in reasons and current['candidates'][cid] == row['source_before'] == original['candidates'][cid]
    assert c.digest(row['source_after']) == row['source_after_sha256']
    before, after = row['source_before'], copy.deepcopy(row['source_after'])
    assert {key: value for key, value in after['content'].items() if key != 'application_contract'} == before['content']
    assert sorted([value for value in current['slot_bindings'].values() if value['candidate_id'] == cid], key=lambda value: value['id']) == sorted(row['own_bindings_unchanged'], key=lambda value: value['id'])
    selected.append({'ordinal': ordinal, 'candidate_id': cid, 'source_before': copy.deepcopy(before), 'source_after': after,
        'reason': reasons[ordinal], 'proposal': dict(ref(name), pointer=f'/records/{index}'),
        'whole_original_current_5B_bindings_and_C_after_direct_root_read': True,
        'root_choice_boundary': 'This is an explicit bounded editorial application for this source, not a noun classifier or original unique entailment. Prior A/B options and original source remain historical; no source-wide policy is inferred.',
        'scope': row['required_carrier'], 'permission': row['permission_boundary'],
        'native_approval': False})
    current['candidates'][cid] = after
assert len(selected) == 4
selection_ref = save(HERE / 'ROOT-BARE-PROP-APPLICATION-SELECTION-06.json', {
    'schema': 'photo-root-bare-prop-application-selection/v1', 'actor': '/root',
    'parent_source_sha256': '9ecd6dd135e49a9c5d41fb80ba1a9edfd22efd1de15b5d29ca5660bc0cc4d023',
    'selected_records': selected, 'selected_count': 4, 'research_only': True,
    'search_labels_or_embedding_recipe_changed': False,
    'all_three_actual_subject_and_count_effects_retained': True,
    'original_field_reference_bound_only_to_type': True,
    'new_prop_address_must_be_unoccupied_no_fallback_or_existing_prop_reuse': True,
    'native_approvals': 0, 'operating_source_or_bindings_or_catalog_changes': 0, 'Gemini_calls': 0})
approval = copy.deepcopy(read(base + 'SOURCE-APPROVAL.json'))
for row in selected:
    cid = row['candidate_id']; before, after = original['candidates'][cid], row['source_after']
    assert not any(item['candidate_id'] == cid for item in approval['changes'])
    approval['changes'].append({'candidate_id': cid, 'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
        'delta': [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key), 'after_exists': key in after, 'after': after.get(key), 'reason': row['reason']}
            for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)],
        'reason': row['reason'], 'provenance': [selection_ref]})
approval['changes'].sort(key=lambda row: row['candidate_id'])
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Preserve all prior individually reviewed research changes, adding exactly four bounded prop applications. No automatic noun rule, native proof/status/tag activation or operating source change.'
assert current['slot_catalog'] == read('CATALOG-FINAL-146-V5.json')
assert current['slot_bindings'] == original['slot_bindings'] and current['policies'] == original['policies']
c.validate(current)
prep.approve_source(ROOT, original, current, approval)
OUT.mkdir(exist_ok=False)
snapshot = save(OUT / 'CURRENT-PROPOSAL.json.gz', current, compressed=True)
approval_ref = save(OUT / 'SOURCE-APPROVAL.json', approval)
requirements = save(OUT / 'ROOT-REQUIREMENTS.json', {'schema': 'photo-root-bare-prop-review-requirements/v1',
    'actor': '/root', 'selection': selection_ref, 'native_approvals': 0,
    'requirements': [
        'Read whole exact original/current/5B/ownbinding/closure/after plus all used whole146 specs and neighbors. Preparation creates no read count.',
        'Each source has three original application E facts: new independent object addition/presence, type, local one-object count. No P-only source replacement or E0. Subject and count whole locks must reject the complete cue.',
        'Only the actual application directly grounds addition/presence/count. Bare original EN/KO/embedding provide one-hop partial restatement of type only, retaining every local qualifier. Helmet Korean does not independently assert prop status.',
        'Introduced address is primary_prop and must be unoccupied, exact creator-linked, with no fallback/reuse/self-witness of a frozen existing P. No global scene/person count follows.',
        'Keep original intrinsic human and all actual binding policies independently cumulative; add no wearer/location/action/performance/material/color/placement. Formal full/compact/oldbinding/lock consumers need direct checks before root acceptance.',
        'No model/provider/network/Gemini/Git/operating writes, no auto-resigning old proof. Preserve A/B/C drafts and old historical statuses.']})
template = read(base + 'PLAN-01257.json')
order = prep.reviews.artifact(ROOT, template['order'])
packets = {1236: 'packets/01000-250.json', 259: 'packets/00250-100.json', 807: 'packets/00750-250.json', 924: 'packets/00750-250.json'}
prepared = []
for index, row in enumerate(proposal['records']):
    ordinal, cid = row['ordinal'], row['candidate_id']; assert order[ordinal] == cid
    locator = {key: row['original_compiled_locator'][key] for key in ['file', 'file_sha256', 'item', 'row_sha256']}
    one_ref = save(OUT / f'ORIGINAL-SELECTION-{ordinal:05d}.json', {'schema': prep.SELECTION, 'actor': '/root',
        'original_source_sha256': c.digest(original), 'records': {cid: {'locator': locator, 'packet': ref(packets[ordinal]),
            'reason': 'Actual exact historical compiled row and full original packet; no alternative row substituted.'}},
        'reason': 'One exact independently selected source with preserved original historical review provenance.'})
    plan = {key: copy.deepcopy(template[key]) for key in ['schema', 'actor', 'original_snapshot', 'order', 'catalog_approval']}
    plan.update(current_proposal=snapshot, source_approval=approval_ref, original_selection=one_ref,
        assignment={'task_name': '/root/review_06250_07250', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'start': ordinal, 'end': ordinal + 1, 'ids': [cid]},
        required_revisions={cid: {'prior_review': {'artifact': ref(name), 'pointer': f'/records/{index}', 'sha256': c.digest(row)},
            'memo_artifacts': [requirements], 'reason': 'Fresh manual completion after explicit root C application selection, not automatic proof approval.'}},
        reason='Prepare one exact bounded new-prop application for direct native review, retaining prior historical provenance.')
    plan_ref = save(OUT / f'PLAN-{ordinal:05d}.json', plan)
    directory, receipt = prep.write_inputs(plan_ref, f'review06250-{ordinal:05d}-06', actor='/root')
    prepared.append({'ordinal': ordinal, 'directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
save(OUT / 'ROOT-PREPARATION-VERIFICATION.json', {'schema': 'photo-root-bare-prop-preparation/v1',
    'actor': '/root', 'source': snapshot, 'source_approval': approval_ref, 'selection': selection_ref,
    'source_changed_records_vs_original': len(approval['changes']), 'selected_new_applications': 4,
    'prepared': prepared, 'actual_read_count_created_by_preparation': 0, 'native_approvals': 0,
    'full18250_container_and_exact_source_approval_validated': True,
    'canonical_source_bindings_catalog_or_status_changed': False, 'Gemini_calls': 0})
print(json.dumps({'changed_CIDs_vs_original': len(approval['changes']), 'prepared': 4, 'new_reads': 0, 'native_approvals': 0, 'source_sha256': c.digest(current)}))
