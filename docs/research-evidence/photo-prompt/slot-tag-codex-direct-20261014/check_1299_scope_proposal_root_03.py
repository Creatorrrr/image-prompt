"""Shape-only checks for an unselected source application, with model imports denied."""
import hashlib
import importlib.abc
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
FORBIDDEN = {'photo_local_embedding', 'photo_embedding_provider', 'torch', 'transformers', 'sentence_transformers',
             'tensorflow', 'jax', 'mlx', 'google', 'openai', 'anthropic', 'litellm', 'ollama'}
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in FORBIDDEN:
            raise AssertionError('provider/model import forbidden: ' + fullname)
sys.meta_path.insert(0, Deny())
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
assert Path(native.__file__).resolve().is_relative_to(GEN)
assert hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest() == 'f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
path = HERE / 'authored/native_1299_hands_exchange_application_proposal_03.json'
proposal = json.loads(path.read_bytes())
source = proposal['whole_proposed_after_source']
assert c.digest(source) == proposal['proposed_after_source_sha256']
assert proposal['root_source_selection'] is False and proposal['source_or_catalog_or_binding_changed'] is False
c.validate_conditions(source['conditions'], 'unselected03.conditions')
owners = native.owner_binding_plan(proposal['owner_map_intent_not_native_proof'])
assert all(row['target'] in owners for row in source['effects']['properties'])
assert all(fact['target'] in owners and set(fact.get('receivers', [])) <= set(owners)
           for fact in proposal['manual_P_E_intent_not_native_proof'])
framing = [fact for fact in proposal['manual_P_E_intent_not_native_proof'] if fact['mode'] == 'effect' and fact['dimension'] == 'framing']
assert len(framing) == 2 and all('framing_affected_owners' in fact['receivers'] for fact in framing)
assert any(fact['mode'] == 'prerequisite' and fact['target'] == 'framing_affected_owners'
           and fact['property'] == 'entity.presence' for fact in proposal['manual_P_E_intent_not_native_proof'])
report = {
    'schema': 'photo-root-unselected-source-shape-verification/v1', 'actor': '/root',
    'proposal_raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'source_after_sha256': c.digest(source), 'frozen_engine': str(GEN),
    'checks': ['exact source hash and unselected status', 'source guard shape', 'owner-map shape',
               'every source effect target mapped', 'every proposed fact target and receiver mapped',
               'both proposed framing effects explicitly include separately selected receiver scope',
               'scope members have explicit proposed exact presence obligation'],
    'checks_passed': 7, 'native_proofs_created': 0, 'qualification_or_admission_calls': 0,
    'semantic_completeness_proved': False, 'root_source_selected': False, 'operating_changes': 0,
    'forbidden_modules_loaded': [name for name in sys.modules if name.split('.')[0] in FORBIDDEN],
    'model_provider_Gemini_calls': 0,
    'boundary': 'These are shapes of an unselected literal. Existing scope validators do not verify semantic completeness. Fresh source-local quotes, all actual receivers, independent exact request/core inventory and actual consumer/lock tests remain required.',
}
assert not report['forbidden_modules_loaded']
out = HERE / 'ROOT-1299-SCOPE-PROPOSAL-SHAPE-03.json'
with out.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'checks_passed': 7, 'semantic_approval': False, 'native_proofs_created': 0}))
