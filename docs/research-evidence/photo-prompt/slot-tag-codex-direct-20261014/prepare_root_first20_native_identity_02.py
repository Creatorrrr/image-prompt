"""Correct only root session metadata after the pre-write assignment rejection.

The failed plan and literal sources are preserved byte-for-byte. Root's model
and effort are not observed, so use the protocol's explicit unspecified values.
No semantic source, proof, status or read attestation is authored here.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prep
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
DIR = HERE / 'native-inputs/root-00000-00020-plan-01'


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'sha256': c.digest(prep.reviews.read_json(path))}


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')
    return ref(path)


failed = DIR / 'PLAN.json'
plan = prep.reviews.read_json(failed)
assert plan['assignment']['task_name'] == '/root'
assert plan['assignment']['model'] is None and plan['assignment']['reasoning_effort'] is None
plan['assignment']['model'] = 'session_model_unspecified'
plan['assignment']['reasoning_effort'] = 'session_effort_unspecified'
plan_ref = save(DIR / 'PLAN-IDENTITY-02.json', plan)
out, receipt = prep.write_inputs(plan_ref, 'root-00000-00020-01', actor='/root')
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(FROZEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
note = save(DIR / 'ROOT-PREPARATION-VERIFICATION.json', {'schema': 'photo-root-native-input-verification/v1',
    'actor': '/root', 'preserved_rejected_plan': ref(failed), 'corrected_plan': plan_ref,
    'initial_failure': 'Root session identity None/None rejected by validate_assignment_identity before any prepared input files were written. Replaced only those metadata fields with the explicit session_model_unspecified/session_effort_unspecified declarations in a new immutable plan.',
    'semantic_or_source_fields_changed_from_preserved_plan': False,
    'source_changed_records': 50, 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0,
    'native_proofs_or_statuses_or_tag_approvals_created': 0, 'operational_native_qualified_count': 0,
    'full18250_snapshot_and_exact_original_rows_valid': True, 'used_frozen_modules': modules,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0, 'canonical_changes': 0})
print(json.dumps({'prepared': str(out), 'verification': note, 'prepared_count': 20,
    'actual_read_count': 0, 'native_approved': 0}))
