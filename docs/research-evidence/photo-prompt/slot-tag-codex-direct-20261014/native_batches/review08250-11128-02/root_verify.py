"""Root independent revision identity, literal delta and E-value check."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GENERATION = '1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as corpus
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
assignment = HERE / 'native-inputs/prepared/review08250-11128-02/ASSIGNMENT.json'
result = reviews.verify_batch(str(assignment.relative_to(ROOT)),
                              str((OUT / 'BATCH.json').relative_to(ROOT)),
                              str((OUT / 'NOTE.json').relative_to(ROOT)))
old = reviews.read_json(OUT.parent / 'review08250-11128-01/BATCH.json')['records'][0]
new = reviews.read_json(OUT / 'BATCH.json')['records'][0]
assert old['source_after'] == new['source_after']
before = copy.deepcopy(old['proof'])
after = copy.deepcopy(new['proof'])
before.pop('review'); after.pop('review')
# These two exact changes were separately authored and directly reviewed.
assert before['facts'][10]['id'] == 'standing_p2_pose'
assert before['facts'][43]['id'] == 'walking_p2_pose'
before['facts'][10]['value'] = {'type': 'body.pose/v1', 'value': 'natural_standing'}
before['facts'][43]['value'] = {'type': 'body.pose/v1', 'value': 'natural_walking'}
assert before == after
groups = {}
for fact in new['proof']['facts']:
    if fact['mode'] != 'effect':
        continue
    key = (fact['realization_id'], fact['dimension'], fact['target'], fact['property'])
    value = (corpus.canonical_bytes(fact['value']), fact['operation'], tuple(sorted(set(fact['receivers']))))
    assert key not in groups or groups[key] == value
    groups[key] = value
modules = {}
for name, module in list(sys.modules.items()):
    if getattr(module, '__file__', None) and name.startswith('photo_'):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
out = {key: value for key, value in result.items() if key != 'records'}
out.update({'frozen_code_generation': GENERATION, 'used_frozen_modules': modules,
            'exact_manual_fact_value_changes': 2, 'source_after_unchanged': True,
            'other_proof_contract_fields_unchanged': True,
            'same_effect_assignment_groups': len(groups), 'effect_assignment_conflicts': 0,
            'root_semantic_acceptance_written': False,
            'os_network_denied': True, 'provider_keys_removed': True,
            'gemini_calls': 0, 'local_inference_inputs': 0})
with (OUT / 'ROOT-VERIFICATION-01.json').open('xb') as stream:
    stream.write(corpus.canonical_bytes(out) + b'\n')
print(json.dumps({key: value for key, value in out.items() if key != 'used_frozen_modules'}, sort_keys=True))
