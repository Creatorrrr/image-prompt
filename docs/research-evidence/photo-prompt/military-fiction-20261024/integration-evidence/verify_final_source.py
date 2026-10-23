"""Check reviewed military delta and preserve unrelated task-start records."""
import gc
gc.disable()
import hashlib, json, sys
from pathlib import Path

O = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_corpus as corpus

def read(path):
    return json.loads(path.read_bytes())

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()

before = read(O / 'integration-baseline.json')
now = corpus.load(SKILL / 'assets')
new = read(O / 'new-native-records.json')
changed = read(O / 'changed-native-records.json')
drift = [cid for cid, sha in before['candidate_sha256'].items()
    if cid not in changed and digest(now['candidates'].get(cid)) != sha]
binding_drift = [bid for bid, sha in before['binding_sha256'].items()
    if digest(now['slot_bindings'].get(bid)) != sha]
assert not drift and not binding_drift, 'Unrelated task-start source changed'
assert all(now['candidates'][cid] == row for cid, row in {**new, **changed}.items())
assert digest(now['slot_catalog']) == before['catalog_sha256']
assert digest(now['policies']) == before['policies_sha256']
result = {
    'status': 'pass', 'reviewed_new_records_exact': len(new),
    'reviewed_existing_changes_exact': len(changed),
    'unrelated_task_start_candidates_preserved': len(before['candidate_sha256']) - len(changed),
    'task_start_bindings_preserved': len(before['binding_sha256']),
    'catalog_and_policies_preserved': True,
    'current_working_candidates': len(now['candidates']),
    'current_working_bindings': len(now['slot_bindings']),
    'skill_sha256': hashlib.sha256((SKILL / 'SKILL.md').read_bytes()).hexdigest(),
    'selected_runtime_at_check': read(SKILL / 'retrieval-runtime.json'),
    'raw_working_native_layout': 'Prior stale-layout diagnostic retained; sealed installed release is validated separately.',
    'source_corpus_load': 'pass', 'native_approval': False,
}
(O / 'final-source-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
