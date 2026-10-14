"""Only condition/owner-map shapes; no candidate qualification or admission."""
import hashlib, importlib.abc, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
forbidden={'photo_local_embedding','photo_embedding_provider','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in forbidden:raise AssertionError('provider/model import forbidden: '+fullname)
sys.meta_path.insert(0,Deny())
R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
pins=['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py','skills/photo-prompt-image-generator/scripts/photo_slot_semantics.py','skills/photo-prompt-image-generator/scripts/photo_role_proposals.py','tests/test_photo_native_manual_role_views.py','tests/test_photo_native_manual_role_view_transport.py']
def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in pins}
before=hashes()
import photo_semantic_evidence as e
import photo_candidate_corpus as c
p1=json.loads((R/'authored/native_1299_hands_exchange_application_proposal_01.json').read_text())['unselected_restricted_editorial_option']
p2=json.loads((R/'authored/native_1299_hands_exchange_application_proposal_02.json').read_text())
checks=[]
for name,row,ownerkey in [('01',p1,'owner_map_intent_only'),('02',p2,'owner_map_intent_not_native_proof')]:
 source=row['whole_proposed_after_source'];plan=row[ownerkey]
 c.validate_conditions(source['conditions'],'proposal.conditions');checks.append(name+':existing condition shape')
 owners=e.owner_binding_plan(plan);checks.append(name+':existing owner-map shape')
 assert all(x['target'] in owners for x in source['effects']['properties']);checks.append(name+':every source effect target explicitly mapped')
after=hashes();assert before==after
report={'checks':checks,'checks_passed':len(checks),'production_test_hashes_before':before,'production_test_hashes_after':after,'bytes_stable':before==after,'forbidden_modules_loaded':[x for x in sys.modules if x.split('.')[0] in forbidden],'native_proofs_created':0,'qualification_calls':0,'admission_calls':0,'model_provider_embedding_network_calls':0,'meaning_boundary':'Only existing condition/map shape and target coverage checked. No actual core/source proof/whole receiver/selected closure/final/runtime admission validation.'}
out=Path(__file__).with_suffix('.json');assert not out.exists();out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
