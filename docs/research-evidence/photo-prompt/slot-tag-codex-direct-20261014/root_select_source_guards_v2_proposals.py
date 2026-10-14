"""Record root's explicit two-source input decisions after actual manual reading.

This is not semantic inference, proof generation, native approval or activation.
The exact literal before/after records are copied from the independently
authored proposal; the root decisions below were made individually.
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
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/e54254ce78fde43d717a5c6e1670a0ffa5b50050fdafcf4b813930e42ecd0a7f'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as corpus
import photo_semantic_evidence as native

name = 'authored/native_source_guard_v2_1278_1296_proposal_v1.json'
path = HERE / name
proposal = json.loads(path.read_bytes())
assert hashlib.sha256(path.read_bytes()).hexdigest() == '1de44eaf27b82709c3f9079d5792657c9571c879b5b2b1e13a4a2dce11ab3fbe'
assert corpus.digest(proposal) == '42579f7cf2a970c89c0570caee9a9b6837712d5c097b5140103719d4a7629a0e'
current = json.loads(gzip.decompress((HERE / 'native-inputs/11870-01250-01300-plan-03/CURRENT-PROPOSAL.json.gz').read_bytes()))
assert corpus.digest(current) == proposal['current_source_canonical_sha256']
hypothetical = copy.deepcopy(current)
for row in proposal['records']:
    assert current['candidates'][row['candidate_id']] == row['source_before_current_full']
    hypothetical['candidates'][row['candidate_id']] = copy.deepcopy(row['source_after_proposed_full'])
corpus.validate(hypothetical)
decisions = [
    {'ordinal': 1278, 'source_after_selected_for_new_input': True,
     'meaning': 'Blank facial response, warm/helpful presentation of the same character hands, and their contrast remain three actual effects. Hand impression remains untagged whole E, with no temperature, helping act, private emotion or forced finger pose.',
     'application': 'Existing independently declared face and plural hands-region of one existing human character, each explicitly selected. Preserve original human and own binding gates, require actual part_of/disjoint graph facts and the exact custom human value on that selected character. No main-role donor, synthetic anatomy or group creation.',
     'proof_material_status': 'Source decision only; all fifteen fact fragments and role choices need fresh formal review. No proof/signature/status from the proposal is accepted.'},
    {'ordinal': 1296, 'source_after_selected_for_new_input': True,
     'meaning': 'The same existing warm mug is held by two distinct participating existing hands of the same existing holder. Select qualitative physical warmth, both holding acts and the Korean wrapping/contact meaning as effects, retaining exact endpoints.',
     'both_interpretation': 'The Korean two hands identifies the participating pair. Neither source language asserts exactly two hands in the holder entire anatomical inventory. Additional hands alone are not a contradiction; no exhaustive-total or visible-framing count assertion is approved. Exact pair membership and all source/core protected scopes remain mandatory.',
     'application': 'Each selected hand is part_of the same holder and disjoint from the other hand and mug. Holder remains guard-only. No implicit left/right, human-only anatomy, drink, steam, heating cause, finger geometry or comfort.',
     'proof_material_status': 'The source after is selected, but the43 combined material facts are not approved proof. In the next formal proof omit or redesign held_contact_en and held_contact_emb: English held in both hands alone does not entail wrapping. Preserve wrapping E using the exact positive Korean/application quotes; English units can retain their two holding E anchors. Do not waive wrapping, weaken its lock or invent another field merely to fit a role.'},
]
out = {'schema': 'photo-root-source-guard-proposal-selection/v1', 'actor': '/root',
       'proposal': {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'sha256': corpus.digest(proposal)},
       'catalog_sha256': proposal['catalog_canonical_sha256'],
       'root_direct_read_scope': {'original_current_proposed_complete_records': [1278, 1296],
           'exact_original5B_rows_and_current_own_bindings': [1278, 1296],
           'manual_material_facts': 43, 'complete_source_units': 7, 'proposed_roles': 6,
           'all_maps_conditions_effects_and_complete_worker_note_read': True,
           'latest_full_specs_and_neighbors': proposal['actual_read_scope']['latest_full_specs_and_neighbors'],
           'whole144_new_read_claimed': False},
       'decisions': decisions, 'hypothetical18250_container_validation': 'pass',
       'validation_frozen_generation': GEN.name,
       'fresh_input_prepared': False, 'new_native_proofs_or_signatures': 0,
       'native_statuses_changed': False, 'canonical_or_binding_changes': False,
       'operational_native_qualified_count': 0, 'gemini_calls': 0,
       'next': 'Combine these individually selected source literals with separately read relation-gap proposals into a fresh immutable input. Require fresh whole-source native review and independent controls before root acceptance.'}
for modname, module in list(sys.modules.items()):
    if modname.startswith('photo_') and getattr(module, '__file__', None):
        assert Path(module.__file__).resolve().is_relative_to(GEN)
target = HERE / 'ROOT-SOURCE-GUARD-V2-TWO-SOURCE-SELECTION-01.json'
with target.open('x') as stream:
    json.dump(out, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'path': str(target), 'selected_source_inputs': 2, 'proof_approvals': 0,
                  'hypothetical_container': 'pass', 'sha256': corpus.digest(out)}))
