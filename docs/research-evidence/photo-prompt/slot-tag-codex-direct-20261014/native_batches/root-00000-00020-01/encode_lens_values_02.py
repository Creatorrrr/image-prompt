"""Root's explicit typed-mm lexeme correction to the rejected unsigned batch.

Preserve all original files. Select literal string50/string24 within their
already declared mm value types; do not widen the witness schema or infer FOV.
No source, role, owner, mode, status or catalog is changed by this correction.
"""
import copy
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


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'sha256': c.digest(json.loads(path.read_bytes()))}


def save(name, value):
    path = OUT / name
    with path.open('xb') as stream: stream.write(c.canonical_bytes(value) + b'\n')
    return ref(path)


old = json.loads((OUT / 'BATCH.json').read_bytes())
batch = copy.deepcopy(old)
changes = []
for ordinal, number, lexeme in [(9, 50, '50'), (17, 24, '24')]:
    row = batch['records'][ordinal]
    assert row['ordinal'] == ordinal
    proof = row['proof']
    for fact_id in ['en0', 'ko0']:
        fact = next(f for f in proof['facts'] if f['id'] == fact_id)
        assert fact['property'] == 'lens.focal_length_mm'
        assert fact['value'] == {'type': 'lens.focal_length_mm/v1', 'value': number}
        fact['value'] = {'type': 'lens.focal_length_mm/v1', 'value': lexeme}
        changes.append({'ordinal': ordinal, 'fact_id': fact_id,
            'before': {'type': 'lens.focal_length_mm/v1', 'value': number}, 'after': copy.deepcopy(fact['value'])})
    proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
note = json.loads((OUT / 'NOTE.json').read_bytes())
note['batch_sha256'] = c.digest(batch)
batch_ref = save('BATCH-WIRE-02.json', batch)
note_ref = save('NOTE-WIRE-02.json', note)
memo = save('ROOT-WIRE-REENCODING-02.json', {'schema': 'photo-root-explicit-wire-correction/v1', 'actor': '/root',
    'rejected_batch': ref(OUT / 'BATCH.json'), 'rejected_note': ref(OUT / 'NOTE.json'),
    'selected_batch': batch_ref, 'selected_note': note_ref, 'changes': changes,
    'initial_verification_failure': 'verify_batch rejected a numeric literal because the existing typed witness value schema permits concrete strings or bounded string lists. No native approval was granted by that failed check.',
    'reason': 'Literal50mm and24mm remain the exact declared focal lengths. Root chooses the lexical strings50/24 under the explicit lens.focal_length_mm/v1 unit type, separately retaining standard/wide_angle named classifications. This is an explicit typed encoding correction to new unaccepted research proofs; no numeric inference, schema widening or catalog/status conversion.',
    'source_role_owner_mode_operation_property_receiver_status_catalog_changed': False,
    'original_files_preserved': True, 'root_semantic_acceptance_written': False,
    'operating_native_qualified_count': 0, 'canonical_changes': 0, 'provider_calls': 0, 'gemini_calls': 0})
print(json.dumps({'batch': batch_ref, 'note': note_ref, 'memo': memo}))
