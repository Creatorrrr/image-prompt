"""Root manual-role-view and domain-override whole-path offline regression; no actual source acceptance."""
from pathlib import Path
import hashlib,json,sys,time,unittest,importlib.abc
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
OUT=Path(__file__).with_suffix('.json')
LOG=Path(__file__).with_suffix('.log')
if OUT.exists():raise SystemExit('immutable result already exists')
class NoModelImports(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx'}:
            raise AssertionError('model import forbidden in B2 regression: '+fullname)
sys.meta_path.insert(0,NoModelImports())
import photo_embedding_provider as provider
blocked=[]
def no_embedding(*args,**kwargs):
    blocked.append('embedding_entrypoint');raise AssertionError('embedding execution forbidden in B2 regression')
provider.embed=no_embedding;provider.embed_many=no_embedding
import photo_local_embedding as local
local.infer=no_embedding
NAMES=['tests.test_photo_native_adoption', 'tests.test_photo_native_authorial_meaning', 'tests.test_photo_native_compound_evidence', 'tests.test_photo_native_emt_guards', 'tests.test_photo_native_fact_wire', 'tests.test_photo_native_golem_obligation', 'tests.test_photo_native_guard_role_support', 'tests.test_photo_native_independent_manifest', 'tests.test_photo_native_joint_assignments', 'tests.test_photo_native_maintenance', 'tests.test_photo_native_member_scope_resolution', 'tests.test_photo_native_object_ownership', 'tests.test_photo_native_owner_selection', 'tests.test_photo_native_runtime_freshness', 'tests.test_photo_native_source_guards_v2', 'tests.test_photo_native_v4_guards', 'tests.test_photo_native_wardrobe_owners', 'tests.test_photo_semantic_evidence', 'tests.test_photo_slot_semantics', 'tests.test_photo_semantic_reference_units', 'tests.test_photo_semantic_reference_workflow', 'tests.test_photo_direct_native_adoption', 'tests.test_photo_direct_native_reviews', 'tests.test_photo_application_contract_fields', 'tests.test_photo_existing_member_scope_witnesses', 'tests.test_photo_named_phrase_fields', 'tests.test_photo_native_search_maintenance', 'tests.test_photo_global_index', 'tests.test_photo_search_layout', 'tests.test_photo_search_reader', 'tests.test_photo_workflow_precore', 'tests.test_photo_creative_control_wire_replay', 'tests.test_photo_precore_feature_selection', 'tests.test_photo_native_existing_member_scope', 'tests.test_photo_native_member_scope_transport', 'tests.test_photo_semantic_role_views', 'tests.test_photo_global_retrieval', 'tests.test_photo_candidate_realizations', 'tests.test_photo_realization_content', 'tests.test_photo_candidate_corpus', 'tests.test_photo_workflow_state']
def files():
    paths=sorted((ROOT/'skills/photo-prompt-image-generator/scripts').glob('*.py'))
    paths+=sorted((ROOT/'skills/photo-prompt-image-generator/precore').rglob('*.py'))
    paths+=[ROOT/'tests/test_photo_native_manual_role_views.py',ROOT/'tests/test_photo_native_manual_role_view_transport.py',ROOT/'tests/test_photo_entry_domain_override.py',ROOT/'tests/test_photo_native_guard_role_support.py', ROOT/'tests/test_photo_native_member_scope_resolution.py', ROOT/'tests/test_photo_native_search_maintenance.py',ROOT/'tests/test_photo_native_existing_member_scope.py',ROOT/'tests/test_photo_native_member_scope_transport.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.ids=[];self.subtests=0
    def startTest(self,test):self.ids.append(test.id());super().startTest(test)
    def addSubTest(self,test,subtest,err):self.subtests+=1;super().addSubTest(test,subtest,err)
NAMES += ['tests.test_photo_native_manual_role_views','tests.test_photo_native_manual_role_view_transport','tests.test_photo_entry_domain_override']
NAMES += ['tests.test_photo_native_permission_envelope','tests.test_photo_native_permission_transport']
start=time.monotonic();before=files()
before['tests/test_photo_native_permission_transport.py']=hashlib.sha256((ROOT/'tests/test_photo_native_permission_transport.py').read_bytes()).hexdigest()
before['tests/test_photo_native_permission_envelope.py']=hashlib.sha256((ROOT/'tests/test_photo_native_permission_envelope.py').read_bytes()).hexdigest()
suite=unittest.defaultTestLoader.loadTestsFromNames(NAMES)
def flatten(value):
    for item in value:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item
all_tests=list(flatten(suite))
excluded=[]
suite=unittest.TestSuite(all_tests)
with LOG.open('x') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=Result).run(suite)
after=files()
after['tests/test_photo_native_permission_transport.py']=hashlib.sha256((ROOT/'tests/test_photo_native_permission_transport.py').read_bytes()).hexdigest()
after['tests/test_photo_native_permission_envelope.py']=hashlib.sha256((ROOT/'tests/test_photo_native_permission_envelope.py').read_bytes()).hexdigest()
report={'schema':'photo-native-permission-envelope-offline-regression/v1','task':'/root/review_11870_12250',
 'modules':NAMES,
 'all_existing_current_asset_configuration_tests_included':True,
 'actual_inference_module_worker':repr(local._WORKER),
 'log_raw_sha256':hashlib.sha256(LOG.read_bytes()).hexdigest(),
 'executions':result.testsRun,'unique_tests':len(set(result.ids)),'subtests':result.subtests,
 'failures':[(test.id(),trace) for test,trace in result.failures],
 'errors':[(test.id(),trace) for test,trace in result.errors],
 'skipped':[(test.id(),why) for test,why in result.skipped],
 'excluded_static_configuration_ids':excluded,'test_ids':result.ids,'successful':result.wasSuccessful(),
 'elapsed_seconds':round(time.monotonic()-start,3),'blocked_embedding_attempts':blocked,
 'model_imports_loaded':[m for m in sys.modules if m.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx'}],
 'before_hashes':before,'after_hashes':after,'source_bytes_stable':before==after,
 'boundary':'Synthetic fixtures and temporary runtime snapshots only; no actual source/proof/native approval or operational publication.'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['executions','unique_tests','subtests','successful','elapsed_seconds','blocked_embedding_attempts','model_imports_loaded','source_bytes_stable']}),flush=True)
raise SystemExit(0 if result.wasSuccessful() and before==after and not blocked and local._WORKER is None else 1)
