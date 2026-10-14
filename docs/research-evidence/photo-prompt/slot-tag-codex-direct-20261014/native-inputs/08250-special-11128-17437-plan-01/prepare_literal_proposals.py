"""Root bookkeeping for two explicitly selected source drafts, not approval.

The literal source alternatives and fact inventory were directly authored by
the assigned worker. Root selected revision4 after the recorded individual
adjudications. No semantic field or tag is inferred by this serializer.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
OUT = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
import native_reviews as reviews
import prepare_native_inputs as prep
c = reviews.dr.c


def write(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')


def ref(path):
    return {'file': str(path.relative_to(ROOT)),
            'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': c.digest(reviews.read_json(path))}


original = reviews.read_json(HERE / 'SOURCE.json.gz')
order = reviews.read_json(HERE / 'ORDER.json')
base = HERE / 'native-inputs/11870-01250-01300-plan-01'
current = reviews.read_json(base / 'CURRENT-PROPOSAL.json.gz')
approval = reviews.read_json(base / 'SOURCE-APPROVAL.json')
draft_path = HERE / 'authored/native_resolution_08250_revision4_sources.json'
draft = reviews.read_json(draft_path)
note_path = HERE / 'worker-notes/native-resolution-08250-revision4-full-inventory.json'
previous = reviews.read_json(HERE / 'authored/native_diverse_08250_proofs.json')['rows'][0]
previous_profile = reviews.read_json(HERE / 'authored/native_diverse_08250_17437_pending.json')
cid_skirt = 'cand_17f21e3dd66a5d1aa97b3b38efaab469'
cid_profile = 'cand_d15b4c6334a45b61a7407a022a2cc8e0'
assert order[11128] == cid_skirt and order[17437] == cid_profile
assert previous['ordinal'] == 11128 and previous_profile['candidate_id'] == cid_profile

prior_path = OUT / 'PRIOR-UNSIGNED-JUDGEMENTS.json'
write(prior_path, {
    'schema': 'photo-root-exact-prior-unsigned-judgements/v1', 'actor': '/root',
    'judgements': {cid_skirt: previous, cid_profile: previous_profile},
    'original_artifacts': [ref(HERE / 'authored/native_diverse_08250_proofs.json'),
                           ref(HERE / 'authored/native_diverse_08250_17437_pending.json')],
    'old_judgements_accepted_or_resigned': False,
    'reason': 'Preserve exact earlier pending judgements; fresh review must explain their supersession.'})

root_review_path = OUT / 'ROOT-INPUT-SOURCE-REVIEW.json'
write(root_review_path, {
    'schema': 'photo-root-special-source-review-input/v1', 'actor': '/root',
    'selected_source_artifact': ref(draft_path), 'worker_read_note': ref(note_path),
    'root_full_original_source_reads': [cid_skirt, cid_profile],
    'root_full_after_source_personally_read': [cid_skirt],
    'root_profile_after_review': 'Common complete components/discovery/obligations/semantics, all18 RID selection/effect/condition definitions and the five optional manifestations were inspected. Root does not claim personally reading every repeated selected-body leaf or3555 facts. Worker attests complete source-after reading; fresh proof reread is assigned below.',
    'individual_adjudications': {
        cid_skirt: 'Keep actual pencil-skirt wardrobe and standing/walking alternatives. Adult declaration is an existing prerequisite. Reference appearance/identity preservation is conditional on explicit complete frozen input/scope inventory, not an unconditional reference requirement. Ordinary skirt is not a fetish/adult-treatment tag witness.',
        cid_profile: 'Keep adult prerequisite separate from actual youthful-adult visible-age effect. Face belongs to the existing rival. No mandatory distinct counterpart; helper only for selected help and explicitly distinct. One-up is optional independently declared context. Cheek warmth is a visible local color choice without temperature/gratitude inference; mouth warmth is separate. Recovery requires independently declared prior disruption but no selected setback/warmth. Retain only actually chosen optional obligations, and situation.small_setback exact spelling.',
    },
    'current_original_17437_compiled_selection': {
        'file': 'decisions/review_08250_09250_17250_17500.json', 'item': 188,
        'row_sha256': '5589091c1c3a1fb7cd17f66c32f9bf171b2900b426643e3675faa40ca6a6d92c'},
    'old_17437_initial_locator_not_automatically_rebound': True,
    'approval_scope': 'Exact drafts selected for fresh source/spec/RID/proof review only; not final native meaning or operating adoption.',
    'canonical_source_changed': False, 'native_proofs_authored': False,
})

LITERAL_REASONS = {
    cid_skirt: {
        'content': 'Clarify the existing conditional reference/identity preservation and author separate full standing/walking bodies; retain whole-direction skirt/posture meaning and contextual limits.',
        'conditions': 'Retain human applicability, make explicit adult context and conditional preserve-if-established reference/identity guards; no supplied-reference prerequisite.',
        'effects': 'Refine wardrobe effect, remove unsupported material mutation, preserve standing/walking pose OR and walking-only action.'},
    cid_profile: {
        'content': 'Use exact common grouped component source and18 manually authored actual combinations of the independently optional incident groups. Keep exact selected seven-field body and compiled duties; remove stale common compiled duplication.',
        'conditions': 'Require independently established adult context, actual owned face and declared peer-rival role. Selected helper and prior-disruption rules stay in their actual RID branches.',
        'effects': 'Record common actual youthful-adult age presentation, lid aperture, styling, expression and bearing, plus selected-only setback/help/mouth/cheek/recovery effects. Existing adulthood, identity and anatomy are not mutations.'},
}
for cid in (cid_skirt, cid_profile):
    before = original['candidates'][cid]
    after = copy.deepcopy(draft['resolution_proposed_records'][cid])
    assert after['id'] == cid and after['provenance'] == before['provenance']
    delta = [dict(pointer='/' + field, before_exists=True, before=copy.deepcopy(before[field]),
                  after_exists=True, after=copy.deepcopy(after[field]), reason=reason)
             for field, reason in LITERAL_REASONS[cid].items()]
    assert reviews.exact(reviews.apply_delta(before, delta), after)
    current['candidates'][cid] = after
    approval['changes'].append({
        'candidate_id': cid, 'before': before, 'after': after, 'delta': delta,
        'reason': 'Select the individually adjudicated revision4 draft for fresh review; no native acceptance is implied.',
        'provenance': [ref(draft_path), ref(note_path), ref(root_review_path)],
    })
assert len(approval['changes']) == 38
proposal_path = OUT / 'CURRENT-PROPOSAL.json.gz'
with proposal_path.open('xb') as stream:
    stream.write(gzip.compress(c.canonical_bytes(current), mtime=0))
approval['current_source_sha256'] = c.digest(current)
approval['reason'] = 'Preserve the prior36 exact review-input changes and select2 explicit special drafts for fresh review. Bindings/policies remain unchanged; no proof, role status or operating source is applied.'
approval_path = OUT / 'SOURCE-APPROVAL.json'
write(approval_path, approval)

CASES = [
    (cid_skirt, 11128, 'review_03250_04250_11000_11250.json', 129, '11000-250.json', '11128'),
    (cid_profile, 17437, 'review_08250_09250_17250_17500.json', 188, '17250-250.json', '17437'),
]
outputs = []
for cid, ordinal, filename, item, packet_name, name in CASES:
    file = HERE / 'decisions' / filename
    row = reviews.read_json(file)['decisions'][item - 1]
    assert row['candidate_id'] == cid
    if cid == cid_profile:
        assert c.digest(row) == '5589091c1c3a1fb7cd17f66c32f9bf171b2900b426643e3675faa40ca6a6d92c'
    locator = {'file': str(file.relative_to(ROOT)),
               'file_sha256': hashlib.sha256(file.read_bytes()).hexdigest(),
               'item': item, 'row_sha256': c.digest(row)}
    packet_ref = ref(HERE / 'packets' / packet_name)
    assert packet_ref['sha256'] == row['packet_sha256']
    selection_path = OUT / ('ORIGINAL-SELECTION-' + name + '.json')
    write(selection_path, {
        'schema': prep.SELECTION, 'actor': '/root',
        'original_source_sha256': c.digest(original),
        'records': {cid: {'locator': locator, 'packet': packet_ref,
                         'reason': 'Explicitly select the actual current historical compiled row; old pilot locators remain preserved.'}},
        'reason': 'Exact original source/catalog/current compiled file/item/row/packet binding.'})
    old_judgement = previous if cid == cid_skirt else previous_profile
    plan = {
        'schema': prep.PLAN, 'actor': '/root',
        'original_snapshot': ref(HERE / 'SOURCE.json.gz'),
        'current_proposal': ref(proposal_path), 'order': ref(HERE / 'ORDER.json'),
        'catalog_approval': ref(HERE / 'NATIVE-CATALOG-APPROVAL-142-V2.json'),
        'source_approval': ref(approval_path), 'original_selection': ref(selection_path),
        'assignment': {'task_name': '/root/review_08250_09250', 'model': 'gpt-6.1-sol',
                       'reasoning_effort': 'high', 'start': ordinal, 'end': ordinal + 1, 'ids': [cid]},
        'required_revisions': {cid: {
            'prior_review': {'artifact': ref(prior_path), 'pointer': '/judgements/' + cid,
                             'sha256': c.digest(old_judgement)},
            'memo_artifacts': [ref(root_review_path), ref(draft_path), ref(note_path)],
            'reason': 'Fresh full original/current/spec/RID/guard/profile/compiled provenance review must explicitly supersede the exact earlier pending judgement; no old proof/hash resignation.'}},
        'reason': 'Fresh exact special source input after v4 code/runtime integration; review input only with zero automatic reading/proof/native approval.'}
    plan_path = OUT / ('PLAN-' + name + '.json')
    write(plan_path, plan)
    output, receipt = prep.write_inputs(ref(plan_path), 'review08250-' + name + '-01', actor='/root')
    outputs.append({'ordinal': ordinal, 'output': str(output.relative_to(ROOT)),
                    'prepared_count': receipt['prepared_count'], 'actual_read_count': receipt['actual_read_count']})
print(json.dumps({'prepared_inputs': outputs, 'current_source_sha256': c.digest(current),
                  'catalog_sha256': c.digest(current['slot_catalog']),
                  'native_proofs_written': 0, 'canonical_source_changed': False}))
