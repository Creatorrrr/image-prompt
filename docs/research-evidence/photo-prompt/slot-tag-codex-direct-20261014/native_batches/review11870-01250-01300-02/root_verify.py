"""Root verification of frozen formal02; no semantic status is promoted."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GENERATION = '534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as corpus
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]


def artifact(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': corpus.digest(reviews.read_json(path))}


result = reviews.verify_batch(
    str((HERE / 'native-inputs/prepared/review11870-01250-01300-02/ASSIGNMENT.json').relative_to(ROOT)),
    str((OUT / 'BATCH.json').relative_to(ROOT)), str((OUT / 'NOTE.json').relative_to(ROOT)))
batch = reviews.read_json(OUT / 'BATCH.json')
assert corpus.digest(batch) == 'f0fab35a9944399b96f0d99535b6cbbcf76f13faed54e61c45c5d3e5731b3cfa'
assert len(batch['records']) == 50
assert sum(row['status'] == 'approved' for row in batch['records']) == 31
assert sum(row['status'] == 'pending' for row in batch['records']) == 19
groups = {}
facts_count = units_count = 0
for row in batch['records']:
    if row['status'] != 'approved':
        continue
    proof = row['proof']
    facts_count += len(proof['facts'])
    units_count += len(proof['source_units'])
    for fact in proof['facts']:
        if fact['mode'] != 'effect':
            continue
        key = (row['candidate_id'], fact['realization_id'], fact['dimension'], fact['target'], fact['property'])
        value = (corpus.canonical_bytes(fact['value']), fact['operation'], frozenset(fact['receivers']))
        assert key not in groups or groups[key] == value
        groups[key] = value
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {key: value for key, value in result.items() if key != 'records'}
report.update({
    'schema': 'photo-root-frozen-native-batch-verification/v1',
    'frozen_code_generation': GENERATION, 'used_frozen_modules': modules,
    'facts_checked': facts_count, 'source_units_checked': units_count,
    'source_local_effect_groups': len(groups), 'source_local_assignment_conflicts': 0,
    'root_semantic_acceptance_written': False, 'root_accepted_records': 0,
    'independent_semantic_review': artifact(HERE / 'worker-notes/native-evidence-11870-formal02-independent-semantic-review-20261015.json'),
    'root_reopen_ordinals': [1262],
    'reason': 'Shape-valid historical142V2 batch is preserved. The same-announcer/raised-gavel relation needs a source/fact/receiver/guard revision; latest144 catalog also needs fresh bound review. Neither the31 worker statuses nor exact12 custom P obligations are automatically promoted or erased.',
    'root_personally_read_all31_full_proofs_in_this_check': False,
    'actual_normalized_request_freeze_or_runtime_acceptance_verified': False,
    'os_network_denied': True, 'provider_keys_removed': True,
    'gemini_calls': 0, 'local_inference_inputs': 0,
})
with (OUT / 'ROOT-VERIFICATION-01.json').open('xb') as stream:
    stream.write(corpus.canonical_bytes(report) + b'\n')
print(json.dumps({key: value for key, value in report.items() if key != 'used_frozen_modules'}))
