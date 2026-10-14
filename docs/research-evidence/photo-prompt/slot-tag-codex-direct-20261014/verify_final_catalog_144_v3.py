"""Pure root verification of the accepted R02 catalog and input-only source45.

Use keyless env-i and OS network denial. No source/tag/proof/runtime writes.
The report distinguishes complete-container integrity from semantic approval.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GENERATION = '534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as corpus
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]


def read(name):
    return reviews.read_json(HERE / name)


def artifact(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': corpus.digest(read(name))}


original = read('SOURCE.json.gz')
catalog = read('CATALOG-FINAL-144-V3.json')
review = read('CATALOG-FINAL-144-V3-REVIEW.json')
approval = read('NATIVE-CATALOG-APPROVAL-144-V3.json')
reviews.fields(approval, {'schema','actor','status','catalog','catalog_count','catalog_ids','catalog_sha256','review','reason'}, 'root final catalog approval')
assert approval['schema'] == 'photo-codex-native-input-catalog-approval/v1'
assert approval['actor'] == '/root' and approval['status'] == 'final_approved'
assert approval['catalog_count'] == len(catalog) == 144
assert approval['catalog_ids'] == sorted(catalog)
assert reviews.artifact(ROOT, approval['catalog']) == catalog
assert approval['review'] == review
assert corpus.digest(catalog) == approval['catalog_sha256'] == '20ba9b75b3afa86ec02a1aa7a7d750eda86ca61c99573d03c94ea12ea9375c39'
reviews.verify_catalog(original['slot_catalog'], catalog, review, ROOT)
container = copy.deepcopy(original)
container['slot_catalog'] = copy.deepcopy(catalog)
corpus.validate(container)
proposed = read('native-inputs/first50-pending-source-plan-03/CURRENT-PROPOSAL.json.gz')
assert len(proposed['slot_catalog']) == 142
assert proposed['slot_bindings'] == original['slot_bindings'] and proposed['policies'] == original['policies']
assert sum(proposed['candidates'][cid] != record for cid, record in original['candidates'].items()) == 45
proposed['slot_catalog'] = copy.deepcopy(catalog)
corpus.validate(proposed)
current = corpus.load(ROOT / 'skills/photo-prompt-image-generator/assets')
assert corpus.digest(current) == corpus.digest(original) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {
    'schema': 'photo-root-final-catalog-verification/v1', 'actor': '/root',
    'catalog': artifact('CATALOG-FINAL-144-V3.json'),
    'review': artifact('CATALOG-FINAL-144-V3-REVIEW.json'),
    'input_approval': artifact('NATIVE-CATALOG-APPROVAL-144-V3.json'),
    'complete_139_to144_delta_verified': True, 'changed_specs_from139': len(review['changes']),
    'complete_18250_record_container_with144_catalog_integrity': 'pass',
    'input_only_45_proposed_record_container_with144_catalog_integrity': 'pass',
    'proposed_source45_is_not_prepared_or_native_approved': True,
    'frozen_code_generation': GENERATION, 'used_frozen_modules': modules,
    'root_read_basis': 'Root authored/reread12 full changed specs and whole source witnesses; delegated worker actually reread all144 complete specifications. Do not count schema/hash validation as semantic reading.',
    'initial_serializer_repairs': [
        'Two digest-accessor errors occurred before any output write; use the explicit photo_candidate_corpus public API.',
        'The first input-approval wire status approved was corrected to the required final_approved before input use. Exact pre-wire-fix JSON is preserved separately. Catalog definitions, review and semantic acceptance did not change.'],
    'os_network_denied': True, 'provider_keys_removed': True,
    'gemini_calls': 0, 'local_inference_inputs': 0, 'canonical_mutations': 0,
    'canonical_native_qualified_records': 0, 'stages05_08_complete': False,
    'later_actual_source_findings_require_separate_scope_revision': True,
}
with (HERE / 'ROOT-FINAL-CATALOG-144-V3-VERIFICATION.json').open('xb') as stream:
    stream.write(corpus.canonical_bytes(report) + b'\n')
print(json.dumps({key: value for key, value in report.items() if key != 'used_frozen_modules'}))
