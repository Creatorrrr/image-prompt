"""Select nine individually reviewed corrections for future fresh native input.

Root has directly reread every selected whole before/after and correction reason.
This is an input-only proposal, not a candidate approval or operating mutation.
No fact, tag, mode, owner selection, proof, or status is generated here.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'native-inputs/first50-pending-source-plan-03'
SELECTED_ORDINALS = [1258, 1264, 1265, 1272, 1275, 1278, 1280, 1286, 1296]


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def artifact(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': sha(read(path))}


def write(name, value, *, compressed=False):
    path = OUT / name
    raw = canonical(value) + b'\n'
    with path.open('xb') as stream:
        stream.write(gzip.compress(raw, mtime=0) if compressed else raw)
    return artifact(path)


original = read(HERE / 'SOURCE.json.gz')
prior_path = HERE / 'native-inputs/08250-special-11128-17437-plan-01/CURRENT-PROPOSAL.json.gz'
prior_approval_path = prior_path.with_name('SOURCE-APPROVAL.json')
prior = read(prior_path)
prior_approval = read(prior_approval_path)
proposal_path = HERE / 'authored/native_11870_first50_pending_resolution_v1.json'
if hashlib.sha256(proposal_path.read_bytes()).hexdigest() != 'e7f1ff6584bc0d09c6f804138d2ed1154ee8a595b34c89c48fe14a9359008592':
    raise ValueError('preserve reviewed pending-resolution bytes')
if sha(original) != '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b':
    raise ValueError('original source changed')
if sha(prior) != '557666c13c0597b1a1806626f138bd759b69ebd0334c36dfd1913f3bcceb62bb':
    raise ValueError('prior38 input snapshot changed')
proposals = read(proposal_path)
rows = {row['ordinal']: row for row in proposals['records']}
after = copy.deepcopy(prior)
chosen = []
for ordinal in SELECTED_ORDINALS:
    row = rows[ordinal]
    cid = row['candidate_id']
    if (sha(prior['candidates'][cid]) != row['source_before_current_sha256']
            or prior['candidates'][cid] != row['source_before_current_full']
            or sha(row['source_after_proposed_full']) != row['source_after_proposed_sha256']
            or not row['original_and_current_whole_reread_complete']
            or not row['proposed_whole_source_reread_complete']):
        raise ValueError('selected literal whole-source proposal mismatch: ' + str(ordinal))
    after['candidates'][cid] = copy.deepcopy(row['source_after_proposed_full'])
    chosen.append({'ordinal': ordinal, 'candidate_id': cid,
        'before_current_sha256': row['source_before_current_sha256'],
        'after_sha256': row['source_after_proposed_sha256'],
        'exact_selected_delta': copy.deepcopy(row['exact_source_correction_proposals']),
        'resolution_state': row['resolution_state'],
        'root_decision': 'Select the literal corrected meaning for fresh review input only; no proof, role or unresolved owner/branch/guard contract is approved.'})
if (after['slot_bindings'] != prior['slot_bindings']
        or after['slot_catalog'] != prior['slot_catalog']
        or after['policies'] != prior['policies']):
    raise ValueError('this selection must not change prior bindings/catalog/policies')
assert set(after['candidates']) == set(original['candidates'])
changed = sorted(cid for cid in original['candidates'] if original['candidates'][cid] != after['candidates'][cid])
assert len(changed) == 45
OUT.mkdir(exist_ok=False)
snapshot = write('CURRENT-PROPOSAL.json.gz', after, compressed=True)
note = write('ROOT-SOURCE-SELECTION.json', {
    'schema': 'photo-root-explicit-source-selection/v1', 'actor': '/root',
    'selected_source_proposals': artifact(proposal_path), 'prior_snapshot': artifact(prior_path),
    'prior_approval': artifact(prior_approval_path), 'selected_corrections': chosen,
    'root_personally_reread_all_nine_whole_before_after_and_deltas': True,
    'source_correction_count_from_original': 45, 'candidate_count': len(after['candidates']),
    'new_snapshot': snapshot, 'catalog_input_pending_separate_final_approval': True,
    'research_snapshot_preserves_prior142_catalog_until_explicit_final_catalog_input': True,
    'initial_validation_attempt': 'Original snapshot catalog has139 entries; prior research input has142. The first assertion rejected this expected existing catalog difference before writing any output. Corrected to assert no new change relative to the pinned prior snapshot.',
    'canonical_applied': False, 'candidate_tags_approved': 0,
    'native_proofs_approved': 0, 'old_batch_statuses_changed': False,
    'unresolved_native_contracts_preserved': True, 'gemini_calls': 0,
})
print(json.dumps({'snapshot': snapshot, 'root_selection': note, 'changed_records': len(changed)}))
