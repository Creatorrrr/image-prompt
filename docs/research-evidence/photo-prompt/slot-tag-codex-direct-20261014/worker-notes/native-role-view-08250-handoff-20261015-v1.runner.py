"""Offline synthetic-only final check; no actual candidate qualification."""
import hashlib,io,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from tests import test_photo_semantic_role_views as test
W=Path(__file__).resolve().parent
P=W/'native-role-view-08250-handoff-20261015-v1.validation.json'
assert not P.exists()
class Result(unittest.TextTestResult):
    def __init__(self,*a,**k):super().__init__(*a,**k);self.ids=[];self.subtests=0
    def startTest(self,case):self.ids.append(case.id());super().startTest(case)
    def addSubTest(self,*a,**k):self.subtests+=1;super().addSubTest(*a,**k)
buffer=io.StringIO()
result=unittest.TextTestRunner(stream=buffer,verbosity=2,resultclass=Result).run(unittest.defaultTestLoader.loadTestsFromModule(test))
module=Path(test.v.__file__).resolve();testfile=Path(test.__file__).resolve()
log=W/'native-role-view-08250-handoff-20261015-v1.validation.log';assert not log.exists();log.write_text(buffer.getvalue())
report={'schema':'photo-role-view-focused-synthetic-validation/v1','task':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','module':{'file':str(module),'sha256':hashlib.sha256(module.read_bytes()).hexdigest()},'test':{'file':str(testfile),'sha256':hashlib.sha256(testfile.read_bytes()).hexdigest()},'tests_run':result.testsRun,'unique_test_ids':len(set(result.ids)),'subtests':result.subtests,'failures':result.failures,'errors':result.errors,'skipped':result.skipped,'test_ids':result.ids,'success':result.wasSuccessful(),'scope':'synthetic pure module only; no native consumer integration or actual source semantic approval','network':'sandbox deny network; provider environment keys removed','provider_model_calls':0,'earlier_runs':[{'tests':20,'failures':0,'errors':0},{'tests':22,'failures':0,'errors':0}],'failure_history':'No observed test failure. Proactively tightened malformed nested input handling, exact typed value and accepted-cap coverage before final handoff.'}
P.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(buffer.getvalue());print(json.dumps({k:v for k,v in report.items() if k!='test_ids'},ensure_ascii=False))
if not result.wasSuccessful():sys.exit(1)
