"""Root accepts four exact manually read research proofs; no activation."""
from __future__ import annotations
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
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(reviews.read_json(path))}


note_path = HERE / 'worker-notes/native-06250-C4-formal06-final-20261015.json'
assert hashlib.sha256(note_path.read_bytes()).hexdigest() == 'e9961794017a115c5569bd0c7d4236e7fea8dab5dfbda6e694127e80e739838c'
note = reviews.read_json(note_path)
counts = note['validation_counts']
assert [counts[key] for key in ['full_native_proofs_validated', 'native_review_batch_integrity_passed',
    'full_compact_times_no_binding_actual_binding_matrix_rows', 'whole_subject_count_lock_rejections',
    'occupied_primary_prop_admission_rejections', 'missing_external_human_and_candidate_self_tag_rejections',
    'introduced_frozen_prerequisite_self_witness_rejections']] == [4, 4, 16, 32, 16, 32, 4]
selected = reviews.read_json(HERE / 'ROOT-BARE-PROP-APPLICATION-SELECTION-06.json')
after = {row['candidate_id']: row['source_after'] for row in selected['selected_records']}
accepted = []
for ordinal in [1236, 259, 807, 924]:
    out = HERE / f'native_batches/review06250-{ordinal:05d}-06'
    assignment = HERE / f'native-inputs/prepared/review06250-{ordinal:05d}-06/ASSIGNMENT.json'
    verified = reviews.verify_batch(str(assignment.relative_to(ROOT)), str((out / 'BATCH.json').relative_to(ROOT)), str((out / 'NOTE.json').relative_to(ROOT)))
    row = reviews.read_json(out / 'BATCH.json')['records'][0]
    cid, proof = row['candidate_id'], row['proof']
    assert row['source_after'] == after[cid] and row['status'] == 'approved'
    assert len(proof['facts']) == 3 and set(proof['roles']) == {'prop'}
    assert all(fact['mode'] == 'effect' and fact['pointer'] == '/content/application_contract' for fact in proof['facts'])
    assert [fact['operation'] for fact in proof['facts']] == ['add_entity', 'set_value', 'set_value']
    assert [fact['property'] for fact in proof['facts']] == ['entity.presence', 'props.type', 'entity.count']
    assert proof['facts'][2]['value']['value'] == 'one'
    assert all(unit['fact_refs'] == ['new_type'] and unit['reference_relation'] == 'partial_restatement'
        for unit in proof['source_units'] if unit['disposition'] == 'semantic_reference')
    assert proof['owner_maps']['base']['bindings'][0]['origin'] == 'introduced'
    assert proof['owner_maps']['base']['bindings'][0]['introduced_by'] == proof['facts'][0]['id']
    reason = ('Root accepts this exact bounded C research proof after complete original/current/C after/5B/ownbinding/empty closure and actual3facts/all sourceunits/owner/effects/guards/prop and relevant neighbors direct review. '
        'The individual editorial application adds one independent scene prop, not an original bare-noun unique entailment or corpus-wide rule. Only the application directly supports addition/presence/local count. '
        'Original fields partially restate type only; helmet Korean does not directly establish scene-prop status. No wearer/person/location/action/performance/material/color/placement follows. '
        'Original external human condition and actual binding remain cumulative, introduced primary_prop must be vacant with no fallback/self-witness, and all subject/count effects retain whole locks. '
        'Worker exact frozen188c full/compact/actual-binding/occupied/missing-human/whole-lock and self-witness checks were reviewed as worker validation, not rerun or described as root tests. '
        'Root independently verifies the full exact batch and acceptance binding; no operating source/catalog/binding/tag/runtime/pixel acceptance or full-corpus approval.')
    acceptance = {'schema': reviews.ACCEPTANCE, 'actor': '/root',
        **{key: verified[key] for key in ['assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256']},
        'reviews': {key: {'review_sha256': c.digest(value), 'status': 'approved'} for key, value in verified['records'].items()},
        'reason': reason}
    save(out / 'ROOT-ACCEPTANCE.json', acceptance)
    reviews.verify_acceptance(ROOT, ref(out / 'ROOT-ACCEPTANCE.json'), verified)
    accepted.append({'ordinal': ordinal, 'candidate_id': cid, 'acceptance': ref(out / 'ROOT-ACCEPTANCE.json'),
        'batch_sha256': verified['batch_sha256'], 'facts': 3, 'units': len(proof['source_units'])})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
save(HERE / 'ROOT-BARE-PROP-RESEARCH-ACCEPTANCE-06.json', {
    'schema': 'photo-root-bare-prop-research-acceptance/v1', 'actor': '/root',
    'root_whole4_selected_sources_and12actualfacts15units_read': True,
    'root_source_selection': 'ROOT-BARE-PROP-APPLICATION-SELECTION-06.json',
    'accepted_research_records': accepted, 'worker_validation_counts': counts,
    'worker_validation_handoff': ref(note_path), 'used_frozen_modules': modules,
    'root_tests_not_claimed_as_worker_tests': True,
    'candidate_operationally_registered_or_index_runtime_changed': False,
    'native_operating_qualified_records': 0, 'model_embedding_provider_network_calls': 0,
    'Gemini_calls': 0, 'stages05_08_complete': False})
print(json.dumps({'research_accepted': len(accepted), 'facts': 12, 'units': 15, 'operational_native_qualified': 0}))
