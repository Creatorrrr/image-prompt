"""Root explicitly accepts7 reviewed proofs and retains13 pending judgements.

No full-corpus/operating approval. The independent reviewer read all20 complete
sources and7 proofs, root read all20 semantic findings and typed inventories,
and frozen shape plus controlled full/compact lock checks passed separately.
"""
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as c
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'sha256': c.digest(reviews.read_json(path))}


def save(name, value):
    path = OUT / name
    with path.open('xb') as stream: stream.write(c.canonical_bytes(value) + b'\n')
    return ref(path)


peer_path = HERE / 'worker-notes/native-07250-root-first20-independent-review-01.json'
assert hashlib.sha256(peer_path.read_bytes()).hexdigest() == 'fc413cbc8b7b6381baeb131ac6722dc7bc05c93e673ff157c12ed6cd88433e16'
peer = reviews.read_json(peer_path)
assert peer['aggregate_semantic_result']['additional_semantic_blockers_found'] == []
assert peer['aggregate_semantic_result']['meaning_preserved_proof_rows'] == [3, 4, 5, 9, 16, 17, 18]
controls = reviews.read_json(OUT / 'ROOT-CONTROLLED-VERIFICATION-03.json')
assert controls['admission_checks'] == 14 and controls['full_consumer_checks'] == 42
prepared = HERE / 'native-inputs/prepared/root-00000-00020-01'
verified = reviews.verify_batch(prepared / 'ASSIGNMENT.json', OUT / 'BATCH-WIRE-02.json', OUT / 'NOTE-WIRE-02.json')
assert verified['statuses'] == {'approved': 7, 'pending': 13, 'diagnostic_reviewed': 0}
assert verified['batch_sha256'] == controls['batch_sha256'] == peer['selected_batch']['canonical_sha256']
for finding in peer['findings']:
    row = next(row for row in verified['records'].values() if row['ordinal'] == finding['ordinal'])
    assert c.digest(row) == finding['selected_row_sha256']
    assert (c.digest(row['proof']) if row['proof'] else None) == finding['selected_proof_sha256']
acceptance = {'schema': reviews.ACCEPTANCE, 'actor': '/root',
    **{key: verified[key] for key in ['assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256']},
    'reviews': {cid: {'review_sha256': c.digest(row), 'status': row['status']} for cid, row in verified['records'].items()},
    'reason': 'Root explicitly accepts these7 source-bound144V4 positive proof judgements and the exact13 pending statuses after direct original/current/5B/own-binding/full-source reads, literal manual proof authoring, whole-source after reread, independent first20 semantic review, frozen exact shape checks and14 admission/42 full-consumer controls. Lens focal length strings retain exact declared mm units and named classes without sensor-FOV inference; image blur, proposed atmosphere and physical place remain distinct. Pending meanings are not promoted. No complete18250 approval, actual request replay, shared operational adoption or pixels are claimed.'}
acceptance_ref = save('ROOT-ACCEPTANCE.json', acceptance)
reviews.verify_acceptance(ROOT, acceptance_ref, verified)
summary_ref = save('ROOT-REVIEW-SUMMARY.json', {'schema': 'photo-root-native-review-summary/v1', 'actor': '/root',
    'selected_batch': ref(OUT / 'BATCH-WIRE-02.json'), 'selected_note': ref(OUT / 'NOTE-WIRE-02.json'),
    'acceptance': acceptance_ref, 'independent_review': ref(peer_path),
    'shape_verification': ref(OUT / 'ROOT-SHAPE-VERIFICATION-02.json'),
    'controlled_verification': ref(OUT / 'ROOT-CONTROLLED-VERIFICATION-03.json'),
    'root_direct_whole_source_reads': 20, 'root_direct_whole_source_after_correction_reads': 5,
    'independent_whole_source_reads': 20, 'native_proofs_reviewed': 7, 'native_facts': 18,
    'accepted_positive_ordinals': [3, 4, 5, 9, 16, 17, 18], 'pending_count': 13,
    'catalog_sha256': verified['catalog_sha256'], 'current_source_sha256': verified['current_source_sha256'],
    'historical_numeric_batch_retained_and_not_accepted': True,
    'failed_fixture_import_provenance_check_retained_and_not_counted_as_complete': True,
    'controlled_generic_fixture_supplies_no_source_specific_feature_or_material_or_anatomy_facts': True,
    'actual_request_freeze_pack_runtime_or_pixels_verified': False,
    'operational_native_qualified_count': 0, 'canonical_changes': 0, 'stage05_complete': False,
    'stages06_08_complete': False, 'provider_calls': 0, 'gemini_calls': 0})
print(json.dumps({'acceptance': acceptance_ref, 'summary': summary_ref, 'accepted_positive': 7,
    'pending': 13, 'operational_qualified': 0}))
