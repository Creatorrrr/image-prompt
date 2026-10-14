"""Validate the exact fourteen selected source inputs using frozen local code.

Full-container integrity and source-guard syntax are structural evidence only.
No native proof, semantic classifier, operating source or model is invoked.
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
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as corpus
import photo_semantic_evidence as native

selection_path = HERE / 'ROOT-FIRST50-SOURCE-APPLICATION-SELECTION-04.json'
selection = json.loads(selection_path.read_bytes())
assert corpus.digest(selection) == 'ec36f900a2bbd0fa5558c87be3ce11546a4b26ec29ba313fcfb73934c7a75007'
base_path = ROOT / selection['current_source']['file']
before = json.loads(gzip.decompress(base_path.read_bytes()))
assert corpus.digest(before) == selection['current_source_canonical_sha256']
after = copy.deepcopy(before)
checks = []
for row in selection['selected_records']:
    cid = row['candidate_id']
    assert before['candidates'][cid] == row['source_before']
    assert corpus.digest(row['source_before']) == row['source_before_sha256']
    assert corpus.digest(row['source_after']) == row['source_after_sha256']
    own = {key: value for key, value in before['slot_bindings'].items() if value['candidate_id'] == cid}
    assert own == row['own_bindings_retained']
    after['candidates'][cid] = copy.deepcopy(row['source_after'])
    if 'native_guards' in row['source_after']['conditions']:
        native.validate_source_guards(row['source_after']['conditions']['native_guards'])
    checks.append({'ordinal': row['ordinal'], 'candidate_id': cid, 'before_after_digest_and_own_bindings_exact': True, 'source_guard_shape': 'pass'})
corpus.validate(after)
changed = [cid for cid in before['candidates'] if before['candidates'][cid] != after['candidates'][cid]]
assert set(changed) == {row['candidate_id'] for row in selection['selected_records']}
assert len(changed) == 14
assert before['slot_bindings'] == after['slot_bindings'] and before['policies'] == after['policies'] and before['slot_catalog'] == after['slot_catalog']
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {'schema': 'photo-root-source-application-input-verification/v1', 'actor': '/root',
    'selection': selection['current_source'], 'selection_raw_sha256': hashlib.sha256(selection_path.read_bytes()).hexdigest(),
    'selection_canonical_sha256': corpus.digest(selection), 'source_checks': checks,
    'full18250_container_integrity': 'pass', 'exact14_in_memory_source_changes_only': True,
    'first_validation_attempt': 'Helper incorrectly sent an absent optional native_guards key to its validator as an empty object. Corrected the helper to validate present guard objects only; selected source bytes unchanged.',
    'unchanged_other_candidates_bindings_catalog_policies': True,
    'proposed_in_memory_container_sha256': corpus.digest(after), 'proposed_container_saved_or_applied': False,
    'frozen_modules': modules, 'os_network_denied': True, 'provider_keys_removed': True,
    'local_inference_calls': 0, 'gemini_calls': 0, 'native_approvals': 0, 'operating_changes': 0,
    'boundary': 'Exact source input syntax/integrity only. Owner maps, modes, quote entailment, roles, actual graph and admission/lock consumers still require fresh whole-source native review.'}
path = HERE / 'ROOT-FIRST50-SOURCE-APPLICATION-VERIFICATION-04.json'
with path.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'source_inputs': len(checks), 'full_container_integrity': 'pass', 'frozen_generation': GEN.name, 'native_approvals': 0, 'operating_changes': 0}))
