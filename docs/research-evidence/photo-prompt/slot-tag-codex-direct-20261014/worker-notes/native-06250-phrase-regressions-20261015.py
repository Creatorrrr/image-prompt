"""Offline fixture runner; no provider, corpus publication or runtime build."""
from pathlib import Path
import hashlib
import io
import json
import sys
import unittest
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=Path(__file__).with_name('native-06250-phrase-regressions-20261015.json')
assert not OUT.exists()
names=['tests.test_photo_named_phrase_fields','tests.test_photo_semantic_evidence',
       'tests.test_photo_semantic_reference_units','tests.test_photo_semantic_reference_workflow',
       'tests.test_photo_native_v4_guards','tests.test_photo_native_owner_selection',
       'tests.test_photo_native_object_ownership','tests.test_photo_native_wardrobe_owners',
       'tests.test_photo_global_index']
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
def loaded():
    rows={}
    for name,module in sorted(sys.modules.items()):
        filename=getattr(module,'__file__',None)
        if filename and (name.startswith('photo_') or name.startswith('tests.test_photo_') or name=='prompt_generator'):
            path=Path(filename).resolve()
            if path.is_relative_to(ROOT):
                rows[name]={'path':str(path),'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    return rows
before=loaded()
class Result(unittest.TextTestResult):
    passed_subtests=0
    def addSubTest(self,test,subtest,err):
        if err is None:self.passed_subtests+=1
        super().addSubTest(test,subtest,err)
stream=io.StringIO()
result=unittest.TextTestRunner(stream=stream,verbosity=1,resultclass=Result).run(suite)
after=loaded()
assert all(after[name]==row for name,row in before.items())
report={'schema':'photo-named-phrase-offline-regressions/v1','task_name':'/root/review_06250_07250',
    'model':'gpt-6.1-sol','reasoning_effort':'high','test_modules':names,'test_count':result.testsRun,
    'passed_subtests':result.passed_subtests,'success':result.wasSuccessful(),
    'failures':[(str(t),text) for t,text in result.failures],
    'errors':[(str(t),text) for t,text in result.errors], 'skipped':[(str(t),text) for t,text in result.skipped],
    'loaded_modules':after,'modules_loaded_before_tests_unchanged_through_tests':True,
    'test_output':stream.getvalue(),'os_network_denied':True,'provider_environment_removed':True,
    'runtime_or_asset_builds':0,
    'temporary_fixture_layout_roundtrip_only':'Existing global-index/workflow regressions write isolated temporary fixtures; no real index/runtime/assets are opened or built.'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(stream.getvalue(),end='')
print('passed subtests',result.passed_subtests,'report',OUT,'rawsha',hashlib.sha256(OUT.read_bytes()).hexdigest())
if not result.wasSuccessful():raise SystemExit(1)
