"""Offline explicit regression runner; never a source/CID acceptance artifact."""
from pathlib import Path
import hashlib,json,sys,time,unittest,importlib.abc
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
OUT=Path(__file__).with_suffix('.json')
if OUT.exists():raise SystemExit('immutable result already exists')
class NoModelImports(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}:
            raise AssertionError('model import forbidden in guard regression: '+fullname)
sys.meta_path.insert(0,NoModelImports())
import photo_embedding_provider as provider
blocked=[]
def no_embedding(*args,**kwargs):
    blocked.append('embedding_entrypoint');raise AssertionError('embedding execution forbidden in guard regression')
provider.embed=no_embedding;provider.embed_many=no_embedding
NAMES=[
 'tests.test_photo_native_adoption','tests.test_photo_native_authorial_meaning',
 'tests.test_photo_native_compound_evidence','tests.test_photo_native_emt_guards',
 'tests.test_photo_native_fact_wire','tests.test_photo_native_golem_obligation',
 'tests.test_photo_native_guard_role_support','tests.test_photo_native_independent_manifest',
 'tests.test_photo_native_joint_assignments','tests.test_photo_native_maintenance',
 'tests.test_photo_native_member_scope_resolution','tests.test_photo_native_object_ownership',
 'tests.test_photo_native_owner_selection','tests.test_photo_native_runtime_freshness',
 'tests.test_photo_native_source_guards_v2','tests.test_photo_native_v4_guards',
 'tests.test_photo_native_wardrobe_owners','tests.test_photo_semantic_evidence',
 'tests.test_photo_slot_semantics','tests.test_photo_semantic_reference_units',
 'tests.test_photo_semantic_reference_workflow','tests.test_photo_direct_native_adoption',
 'tests.test_photo_direct_native_reviews']
def files():
    paths=sorted((ROOT/'skills/photo-prompt-image-generator/scripts').glob('*.py'))
    paths+=sorted((ROOT/'skills/photo-prompt-image-generator/precore').rglob('*.py'))
    paths+=[ROOT/'tests/test_photo_native_guard_role_support.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.ids=[];self.subtests=0
    def startTest(self,test):self.ids.append(test.id());super().startTest(test)
    def addSubTest(self,test,subtest,err):self.subtests+=1;super().addSubTest(test,subtest,err)
start=time.monotonic();before=files()
suite=unittest.defaultTestLoader.loadTestsFromNames(NAMES)
result=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(suite)
after=files()
report={'schema':'photo-guard-role-offline-tests/v1','task':'/root/review_07250_08250',
 'model':'gpt-6.1-sol','effort':'high','modules':NAMES,
 'excluded_model_capable_test':'tests.test_photo_native_search_maintenance',
 'executions':result.testsRun,'unique_tests':len(set(result.ids)),'subtests':result.subtests,
 'failures':[(test.id(),trace) for test,trace in result.failures],
 'errors':[(test.id(),trace) for test,trace in result.errors],
 'skipped':[(test.id(),why) for test,why in result.skipped],
 'test_ids':result.ids,'successful':result.wasSuccessful(),
 'elapsed_seconds':round(time.monotonic()-start,3),'blocked_embedding_attempts':blocked,
 'model_imports_loaded':[m for m in sys.modules if m.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}],
 'before_hashes':before,'after_hashes':after,'source_bytes_stable':before==after,
 'boundary':'Synthetic fixtures and temporary runtime snapshots only; no actual source/proof/native approval or operational publication.'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['executions','unique_tests','subtests','successful','elapsed_seconds','blocked_embedding_attempts','model_imports_loaded','source_bytes_stable']}),flush=True)
raise SystemExit(0 if result.wasSuccessful() and before==after else 1)
