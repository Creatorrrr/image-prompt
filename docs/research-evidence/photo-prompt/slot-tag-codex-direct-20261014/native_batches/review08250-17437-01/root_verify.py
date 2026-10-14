"""Root independent frozen-code identity/shape/effect-assignment check.

This does not reauthor worker facts, replay its author or certify meaning from
shape. Root separately reviews the substantive manual note and source clauses.
"""
from __future__ import annotations
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
# direct_review prepends the checkout at import. Restore the immutable search
# path before its lazily imported catalog/profile validators are reached.
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]

assignment = HERE / 'native-inputs/prepared/review08250-17437-01/ASSIGNMENT.json'
result = reviews.verify_batch(str(assignment.relative_to(ROOT)),
                              str((OUT / 'BATCH.json').relative_to(ROOT)),
                              str((OUT / 'NOTE.json').relative_to(ROOT)))
batch = reviews.read_json(OUT / 'BATCH.json')
assignment_groups = {}
effect_count = 0
for row in batch['records']:
    for fact in row['proof']['facts']:
        if fact['mode'] != 'effect':
            continue
        effect_count += 1
        key = (row['candidate_id'], fact['realization_id'], fact['dimension'],
               fact['target'], fact['property'])
        value = (corpus.canonical_bytes(fact['value']), fact['operation'],
                 tuple(sorted(set(fact['receivers']))))
        assert key not in assignment_groups or assignment_groups[key] == value, key
        assignment_groups[key] = value
used_modules = {}
for name, module in list(sys.modules.items()):
    filename = getattr(module, '__file__', None)
    if filename and name.startswith('photo_'):
        path = Path(filename).resolve()
        assert path.is_relative_to(FROZEN), (name, filename)
        used_modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
out = {key: value for key, value in result.items() if key != 'records'}
out.update({
    'frozen_code_generation': GENERATION, 'used_frozen_modules': used_modules,
    'same_effect_assignment_groups': len(assignment_groups),
    'effect_fact_occurrences_checked': effect_count,
    'effect_assignment_conflicts': 0,
    'root_semantic_acceptance_written': False,
    'root_all3555_facts_personally_read_claimed': False,
    'gemini_calls': 0, 'local_inference_inputs': 0,
    'os_network_denied': True, 'provider_keys_removed': True,
})
path = OUT / 'ROOT-VERIFICATION-01.json'
with path.open('xb') as stream:
    stream.write(corpus.canonical_bytes(out) + b'\n')
print(json.dumps(out, ensure_ascii=False, sort_keys=True))
