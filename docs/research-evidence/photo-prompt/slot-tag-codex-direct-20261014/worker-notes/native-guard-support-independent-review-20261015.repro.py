"""Read-only independent synthetic review; no candidate qualification or runtime writes."""
from pathlib import Path
import copy,hashlib,importlib.abc,json,sys,time,unittest
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
OUT=Path(__file__).with_suffix('.results.json')
if OUT.exists():raise SystemExit('immutable output exists')
class NoModels(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}:
            raise AssertionError('model-capable import denied: '+fullname)
sys.meta_path.insert(0,NoModels())
import photo_embedding_provider as provider
attempts=[]
def denied(*args,**kwargs):
    attempts.append('embedding');raise AssertionError('embedding execution denied')
provider.embed=denied;provider.embed_many=denied
from tests import test_photo_native_guard_role_support as f
from tests import test_photo_native_source_guards_v2 as v
from tests.test_photo_semantic_evidence import assertion,seal,reattest
c=f.c;e=f.e;A=f.A;B=f.B
OBS=[]
class IndependentAdversaries(unittest.TestCase):
    def test_raw_v1_alias_selected_endpoint_is_not_silently_canonicalized(self):
        observed=[]
        for schema in ['v1','v2']:
            data=f.relation_source(schema);p=data['candidates'][A]['content']['role_evidence']
            p['owner_maps']['base']={'schema':e.SELECTOR_OWNER_SCHEMA,'bindings':[
                {'target':'face','origin':'existing','introduced_by':None,'selector':{'kind':'selected_existing_owner'}},
                {'target':'actor','origin':'existing','introduced_by':None,'selector':{'kind':'core_role','role':'main_subject'}}]}
            rows=copy.deepcopy(p['guard_supports']);seal(data,{});f.attach(data,rows,'anatomical_connection');c.validate(data)
            frozen=f.relation_core();frozen['semantic_assertions'] += [
                assertion('alias_face','owner',owner='face_alias',owner_kind='entity'),
                assertion('alias_edge','equivalent',left='face_alias',right='actual_face'),
                assertion('face_presence','fact',owner='actual_face',property='entity.presence',value_type='entity.presence/v1',value='present')]
            v.sign_core(frozen)
            for alias in [False,True]:
                mapping=v.choices(data,frozen,{'face':'face_alias' if alias else 'actual_face'})
                results=[e.admission(entry,frozen)['allowed'] for entry in f.entries(data,owner_selections=mapping)]
                self.assertEqual(results,[schema=='v2' or not alias]*2)
                observed.append({'schema':schema,'selected_alias':alias,'full_compact_allowed':results})
        OBS.append({'case':'actual_v1_raw_vs_v2_canonical_selected_point','observed':observed})

    def test_required_child_common_support_cannot_become_optional_borrowing(self):
        data=v.compound();rec=data['candidates'][A]
        rec['conditions']['native_guards']['rules'].insert(0,v.relation('parent_child_holder',f.endpoint('hand_a'),f.endpoint('holder',B)))
        data['slot_catalog']['anatomical_connection']=f.slot('anatomical_connection',['body_geometry'],property_prefixes=['anatomy.connection'])
        seal(data,{'pose':['holding']},cid=B);f.dependencies(data,A,'base',[B]);seal(data,{'pose':['holding']})
        row=f.support(data,projection={'dimension':'body_geometry','target':'hand_a','property':'anatomy.connection.ownership'})
        f.attach(data,[row],'anatomical_connection');c.validate(data)
        frozen=v.hands_core();mapping=v.compound_choices(data,frozen)
        self.assertTrue(all(e.admission(x,frozen)['allowed'] for x in f.entries(data,owner_selections=mapping)))
        rec['content']['member_candidates'][0]['adoption']='optional'
        rec['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        rows=copy.deepcopy(rec['content']['role_evidence']['guard_supports']);seal(data,{'pose':['holding']});f.attach(data,rows,'anatomical_connection')
        with self.assertRaisesRegex(ValueError,'namespace'):c.validate(data)
        OBS.append({'case':'optional_child_is_not_parent_common_guard_namespace','full_validate':'rejected'})

    def test_guard_support_does_not_waive_missing_effect_fact(self):
        data=v.hands_source();data['slot_catalog']['anatomical_connection']=f.slot('anatomical_connection',['body_geometry'],property_prefixes=['anatomy.connection'])
        seal(data,{'pose':['holding']});row=f.support(data,projection={'dimension':'body_geometry','target':'hand_a','property':'anatomy.connection.ownership'})
        f.attach(data,[row],'anatomical_connection');c.validate(data)
        p=data['candidates'][A]['content']['role_evidence'];p['facts']=[x for x in p['facts'] if x['id']!='holding'];p['roles'].pop('pose')
        for unit in p['source_units']:unit['fact_refs']=[x for x in unit['fact_refs'] if x!='holding']
        reattest(data)
        with self.assertRaisesRegex(ValueError,'effect-mode coverage'):c.validate(data)
        OBS.append({'case':'missing_E_cannot_be_replaced_by_guard_only_positive_unit','full_validate':'rejected'})

    def test_guard_only_map_cannot_inject_unused_owner(self):
        data=f.relation_source('v2');p=data['candidates'][A]['content']['role_evidence']
        p['owner_maps']['base']['bindings'].append({'target':'foreign','core_role':'secondary_subject','origin':'existing','introduced_by':None});reattest(data)
        with self.assertRaisesRegex(ValueError,'exact active'):c.validate(data)
        OBS.append({'case':'unused_guard_only_owner_map_entry','full_validate':'rejected'})

    def test_guard_support_cannot_ground_a_scalar_requires_id(self):
        data=v.hands_source();data['slot_catalog']['anatomical_connection']=f.slot('anatomical_connection',['body_geometry'],property_prefixes=['anatomy.connection'])
        seal(data,{'pose':['holding']});row=f.support(data,projection={'dimension':'body_geometry','target':'hand_a','property':'anatomy.connection.ownership'})
        f.attach(data,[row],'anatomical_connection');c.validate(data)
        p=data['candidates'][A]['content']['role_evidence'];next(x for x in p['facts'] if x['id']=='holding')['requires']=[row['id']];reattest(data)
        with self.assertRaisesRegex(ValueError,'same-RID frozen obligation'):c.validate(data)
        OBS.append({'case':'guard_relation_not_scalar_fact_or_requires_value','full_validate':'rejected'})

    def test_relation_projection_cannot_be_promoted_to_effect_permission(self):
        for schema in ['v1','v2']:
            data=f.relation_source(schema);p=data['candidates'][A]['content']['role_evidence']
            p['guard_supports'][0]['mode']='effect';p['roles']['anatomical_connection']['support_modes']=['effect'];reattest(data)
            with self.subTest(schema=schema),self.assertRaisesRegex(ValueError,'non-prerequisite'):c.validate(data)
        OBS.append({'case':'projection_mode_cannot_be_effect','full_validate':'both schemas rejected'})

    def test_guard_common_support_cannot_borrow_presentation_only_predicate(self):
        data=f.relation_source('v1');rec=data['candidates'][A];p=rec['content']['role_evidence']
        conditions=copy.deepcopy(rec['conditions']);rec['conditions']={}
        p['guard_sets']['base']['source_conditions'][0]={};p['meaning_sha256']=e.meaning_sha256(rec)
        p['guard_supports'][0]['guard']['conditions_sha256']=c.digest(conditions);reattest(data)
        with self.assertRaisesRegex(ValueError,'schema differs'):c.validate(data)
        OBS.append({'case':'presentation_predicate_has_no_own_common_support_locator','full_validate':'rejected'})

class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.ids=[];self.subtests=0
    def startTest(self,test):self.ids.append(test.id());super().startTest(test)
    def addSubTest(self,test,subtest,err):self.subtests+=1;super().addSubTest(test,subtest,err)
def hashes():
    names=['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py','tests/test_photo_native_guard_role_support.py','skills/photo-prompt-image-generator/scripts/photo_native_owner_resolution.py','tests/test_photo_native_member_scope_resolution.py']
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
before=hashes();start=time.monotonic()
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(f.GuardRoleSupportTests),unittest.defaultTestLoader.loadTestsFromTestCase(f.GuardRoleClosureTests),unittest.defaultTestLoader.loadTestsFromTestCase(IndependentAdversaries)])
result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
after=hashes()
report={'schema':'photo-native-independent-guard-support-review-tests/v1','task':'/root/native_evidence','executions':result.testsRun,'unique_tests':len(set(result.ids)),'subtests':result.subtests,'test_ids':result.ids,'failures':[(t.id(),trace) for t,trace in result.failures],'errors':[(t.id(),trace) for t,trace in result.errors],'skips':[(t.id(),why) for t,why in result.skipped],'successful':result.wasSuccessful(),'elapsed_seconds':time.monotonic()-start,'before':before,'after':after,'bytes_unchanged':before==after,'embedding_attempts':attempts,'model_modules_loaded':[m for m in sys.modules if m.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}],'observations':OBS,'excluded_focused_test':'GuardRoleRealTransportTests; no temporary runtime build/publication/acquire executed by this independent runner','scope':'Synthetic fixtures only; no actual source approval or native qualification'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['executions','unique_tests','subtests','successful','bytes_unchanged','embedding_attempts','model_modules_loaded']}))
raise SystemExit(0 if result.wasSuccessful() and before==after else 1)
