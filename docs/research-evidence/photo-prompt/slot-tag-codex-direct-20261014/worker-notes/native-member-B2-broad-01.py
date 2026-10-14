"""Explicit offline B2 integration regression; no model-capable imports/calls."""
from pathlib import Path
import hashlib,importlib.abc,json,sys,time,unittest
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google.genai'}:raise AssertionError('model/provider import forbidden: '+fullname)
sys.meta_path.insert(0,DenyModels())
calls=[]
def no(*a,**k):calls.append('embedding');raise AssertionError('scalar/batch/local model execution forbidden')
import photo_embedding_provider as provider
provider.embed=no;provider.embed_many=no
NAMES=['tests.test_photo_native_existing_member_scope','tests.test_photo_native_member_scope_transport','tests.test_photo_native_adoption','tests.test_photo_native_authorial_meaning','tests.test_photo_native_compound_evidence','tests.test_photo_native_fact_wire','tests.test_photo_native_guard_role_support','tests.test_photo_native_independent_manifest','tests.test_photo_native_joint_assignments','tests.test_photo_native_maintenance','tests.test_photo_native_member_scope_resolution','tests.test_photo_native_object_ownership','tests.test_photo_native_owner_selection','tests.test_photo_native_runtime_freshness','tests.test_photo_native_source_guards_v2','tests.test_photo_native_v4_guards','tests.test_photo_native_wardrobe_owners','tests.test_photo_semantic_evidence','tests.test_photo_slot_semantics','tests.test_photo_semantic_reference_units','tests.test_photo_semantic_reference_workflow','tests.test_photo_direct_native_adoption','tests.test_photo_direct_native_reviews','tests.test_photo_existing_member_scope_witnesses','tests.test_photo_semantic_role_views','tests.test_photo_role_proposals','tests.test_photo_candidate_realizations','tests.test_photo_realization_content','tests.test_photo_candidate_corpus','tests.test_photo_workflow_precore','tests.test_photo_workflow_state']
# These existing real-assets classes need a model-module static space validator.
# They are intentionally not loaded/executed under this hard model-import deny.
EXCLUDED=['tests.test_photo_native_emt_guards.NativeEMTGuardTests','tests.test_photo_native_golem_obligation.PhotoSlotRetrievalIntegrationTests','tests.test_photo_native_search_maintenance']
class R(unittest.TextTestResult):
 def __init__(self,*a,**k):super().__init__(*a,**k);self.ids=[];self.subtests=0
 def startTest(self,t):self.ids.append(t.id());super().startTest(t)
 def addSubTest(self,t,s,e):self.subtests+=1;super().addSubTest(t,s,e)
def hashes():
 paths=sorted((ROOT/'skills/photo-prompt-image-generator/scripts').glob('*.py'))+sorted((ROOT/'skills/photo-prompt-image-generator/precore').rglob('*.py'))
 paths += [ROOT/'tests/test_photo_native_existing_member_scope.py',ROOT/'tests/test_photo_native_member_scope_transport.py']
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
before=hashes();start=time.monotonic();r=unittest.TextTestRunner(verbosity=2,resultclass=R).run(unittest.defaultTestLoader.loadTestsFromNames(NAMES));after=hashes()
report={'schema':'photo-B2-offline-tests/v1','modules':NAMES,'excluded_model_capable':EXCLUDED,'executions':r.testsRun,'unique':len(set(r.ids)),'subtests':r.subtests,'test_ids':r.ids,'failures':[(t.id(),s) for t,s in r.failures],'errors':[(t.id(),s) for t,s in r.errors],'skips':[(t.id(),s) for t,s in r.skipped],'successful':r.wasSuccessful(),'calls':calls,'model_modules_loaded':[m for m in sys.modules if m.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}],'before_hashes':before,'after_hashes':after,'bytes_stable':before==after,'elapsed':time.monotonic()-start}
out=Path(__file__).with_suffix('.json');assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['executions','unique','subtests','successful','bytes_stable','calls','model_modules_loaded','elapsed']}))
raise SystemExit(0 if r.wasSuccessful() and before==after else 1)
