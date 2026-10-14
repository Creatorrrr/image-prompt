"""Select fourteen manually reviewed source applications for a fresh input.

This is source-input adjudication only. No native proof/status/tag, old batch,
operating source, catalog or runtime is changed. Actual introduction and other
unreviewed application alternatives are not granted by an existing-only source.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(name):
    return json.loads((HERE / name).read_bytes())


def ref(name, pointer):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pointer': pointer}


current_name = 'native-inputs/08250-special-quote-color-plan-03/CURRENT-PROPOSAL.json.gz'
current = json.loads(gzip.decompress((HERE / current_name).read_bytes()))
assert digest(current) == '9df8f1fdc5506ff1a74caa615bf985d7e528a992e7809fa52003b3848414ec38'
options = {}
for n in [1, 2]:
    name = f'authored/native_remaining12_owner_scope_revision_{n:02d}.json'
    for index, row in enumerate(read(name)['records']):
        options[row['ordinal']] = (row['source_before'], row['source_after'], ref(name, f'/records/{index}'))
name = 'authored/native_11870_formal03_distinct3_source_proposals_v2.json'
for index, row in enumerate(read(name)['proposals']):
    options[row['ordinal']] = (row['whole_before_source'], row['whole_proposed_after_source'], ref(name, f'/proposals/{index}'))
name = 'authored/native_source_guard_v2_1278_1296_proposal_v1.json'
for index, row in enumerate(read(name)['records']):
    options[row['ordinal']] = (row['source_before_current_full'], row['source_after_proposed_full'], ref(name, f'/records/{index}'))
name = 'authored/native_11870_formal03_1290_ambient_thermal_source_proposal_v1.json'
row = read(name)
options[1290] = (row['whole_before_source'], row['whole_proposed_after_source'], ref(name, '/'))

reasons = {
    1253: 'Select the explicitly bounded physical counter reading: one independently declared counter separates two independently declared participant endpoints and gives a formal social impression. Their existence/disjointness is an application restriction, not a claim that the scene contains exactly two people. No occupation, numeric distance or access right is created.',
    1255: 'The same existing holder holds the same distinct existing object neutrally near self. Preserve actual holding, near-self placement and neutral presentation effects; remove the dangling below reference by spelling out the exact receiver addresses.',
    1256: 'Preserve blank badge OR access card, actual gaze endpoint and atomic eye evidence. Blank-badge absence of lettering remains a text effect; no workplace, authority, new target or generic anatomy inference.',
    1258: 'Keep safe voltage checking as selected action with its exact tester and measurement target, not a frozen already-checking state or safety certification. Preserve existing-only scope without inventing wire, probe, target topology, PPE or result.',
    1266: 'Preserve the same selected human and wand as actual distinct owners. The disjoint guard is independently checked; no extra actor, magic result or anatomy is introduced.',
    1271: 'Select the same independently declared hand and distinct Polaroid stack. Do not infer a second person, a total hand inventory, a stack count or ownership from a core-role label.',
    1273: 'Actual action-figure OR doll identity is separate from selected physical smallness and scene-prop role. The original human applicability condition remains exactly a condition and does not make the toy human.',
    1275: 'Use the actual selected studier and distinct tablet with the complete chosen interaction. This explicit owner restriction does not add another person or convert a selected action into a prerequisite.',
    1278: 'The same actual human owns the named face and participating hands-region. Blank face, warm/helpful impression and their contrast remain distinct effects. Impression is neither physical warmth, a helping act nor private emotion. Retain existing identity/appearance conditional preservation.',
    1284: 'The existing image and caller-selected actual face carry eye-focused album appearance. Atomic face/eyes evidence stays on that same declared carrier. No automatic primary face, extra eye node or anatomy; keep kpop OR album conditions.',
    1287: 'Actual colleague role, off-frame relation and image coverage apply to the same independently declared colleague and other person. Do not create a colleague/workplace, require the other person to be visible, or extend exclusion to every person.',
    1290: 'Keep sticky tropical weather and separately explicit ambient physical heat on the same selected scene/environment carrier. No extra air entity, sweat, humidity, country or season. The weather-only former footprint was incomplete.',
    1295: 'Select two real disjoint skin regions with their actual owners. Local aged-looking and young-looking texture are two semantic selections with explicit appearance/age permission projections, not four aging actions or chronological ages. Region owners may be equal or different only as independently declared; original baby provenance and family tags add nothing.',
    1296: 'Keep the existing physically warm mug and the same holder two distinct participating hands with actual holding and wrapping contact. Two does not assert a complete hand inventory. English held does not prove Korean wrapping: fresh proof must use its actual Korean/application witness.'}
selected = []
for ordinal, reason in reasons.items():
    before, proposed, origin = options[ordinal]
    cid = before['id']
    assert before == current['candidates'][cid], ordinal
    after = copy.deepcopy(proposed)
    root_delta = []
    if ordinal == 1255:
        key = 'application_contract'
        old = after['content'][key]
        needle = 'The holder/object E receiver addresses must be reciprocal as specified below.'
        replacement = 'Holding is performed by that same holder with that same held object as its receiver. Near-self placement is applied to that same held object with that same holder as its receiver. Neutral presentation is applied to that same held object; it asserts no private mental state.'
        assert old.count(needle) == 1
        after['content'][key] = old.replace(needle, replacement)
        root_delta.append({'pointer': '/content/' + key, 'before': old, 'after': after['content'][key], 'reason': 'Replace an in-source dangling cross-reference with the exact already-reviewed receiver meaning. No chosen effect is removed or added.'})
    assert after['id'] == cid and after['provenance'] == before['provenance']
    assert after['record_kind'] == before['record_kind']
    own = {key: value for key, value in current['slot_bindings'].items() if value['candidate_id'] == cid}
    deltas = []
    for key in sorted(set(before) | set(after)):
        if before.get(key) != after.get(key):
            assert key in ['content', 'effects', 'conditions'], (ordinal, key)
            deltas.append({'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key), 'after_exists': key in after, 'after': after.get(key), 'reason': reason})
    assert deltas
    selected.append({'ordinal': ordinal, 'candidate_id': cid, 'source_before': before, 'source_before_sha256': digest(before),
        'source_after': after, 'source_after_sha256': digest(after), 'proposal': origin, 'root_literal_refinement': root_delta,
        'exact_top_delta': deltas, 'own_bindings_retained': own, 'root_reason': reason,
        'whole_proposed_after_directly_read_in_continuous_session': True,
        'selection_scope': 'fresh_review_input_only', 'candidate_native_approval': False,
        'additional_pre_native_requirements': ['Fresh exact-field source-unit/fact adjudication, including all controls and branch clauses.', 'Whole real owner/receiver/P/E preservation and consumer/lock validation remain required.'] +
            (['Local-region age/skin role applicability must be separately approved in the next catalog. This source-input selection does not approve that catalog.'] if ordinal == 1295 else [])})
assert len(selected) == 14
report = {'schema': 'photo-root-source-application-selection/v1', 'actor': '/root',
    'research_only': True, 'current_source': ref(current_name, '/'), 'current_source_canonical_sha256': digest(current),
    'selected_records': selected, 'selected_count': 14,
    'pending_original_first50_ordinals': [1264, 1267, 1285, 1299],
    'pending_reason': 'Exact seat scope, grid-light reading, counterpart-chair interpretation and variable-member exchange framing still need complete manual contracts. No source effect is silently removed to close these holds.',
    'already_selected_quote_clarifications_unchanged': [1250, 1289], '1251_quote_only_reanchor_source_unchanged': True,
    'root_read_boundary': 'Complete selected original/current/after/ownbinding and exact effects/conditions were directly read in this continuous task. Root does not claim a new personal full5B read for every source12 row or a fresh whole-catalog read from this serializer.',
    'native_proofs_statuses_acceptances_changed': 0, 'operational_source_changes': 0,
    'slot_tags_changed': 0, 'gemini_calls': 0, 'network_calls': 0}
output = HERE / 'ROOT-FIRST50-SOURCE-APPLICATION-SELECTION-04.json'
with output.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'file': str(output.relative_to(ROOT)), 'canonical_sha256': digest(report), 'selected_source_inputs': len(selected), 'native_approvals': 0, 'operational_changes': 0}))
