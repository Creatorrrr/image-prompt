"""Offline synthetic-only final check; no actual candidate qualification."""
import hashlib,io,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
EXPECTED={'skills/photo-prompt-image-generator/scripts/photo_semantic_role_views.py':'74a1b412453766de85aef2c9a22f927f5b9b23de3ea4b3bd0358d1a69ae765f4','tests/test_photo_semantic_role_views.py':'971a0a162b0f87796dec0edce31e0edb7b8dac74f3c483d5bcce76ea6606a021'}
for name,sha in EXPECTED.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
from tests import test_photo_semantic_role_views as test
W=Path(__file__).resolve().parent
P=W/'ROOT-PURE-ROLE-VIEW-TESTS-01.json'
assert not P.exists()
class Result(unittest.TextTestResult):
    def __init__(self,*a,**k):super().__init__(*a,**k);self.ids=[];self.subtests=0
    def startTest(self,case):self.ids.append(case.id());super().startTest(case)
    def addSubTest(self,*a,**k):self.subtests+=1;super().addSubTest(*a,**k)
buffer=io.StringIO()
result=unittest.TextTestRunner(stream=buffer,verbosity=2,resultclass=Result).run(unittest.defaultTestLoader.loadTestsFromModule(test))
for name,sha in EXPECTED.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
assert not any(k.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx'} for k in sys.modules)
module=Path(test.v.__file__).resolve();testfile=Path(test.__file__).resolve()
log=W/'ROOT-PURE-ROLE-VIEW-TESTS-01.log';assert not log.exists();log.write_text(buffer.getvalue())
report={'schema':'photo-role-view-focused-synthetic-validation/v1','task':'/root','module':{'file':str(module),'sha256':hashlib.sha256(module.read_bytes()).hexdigest()},'test':{'file':str(testfile),'sha256':hashlib.sha256(testfile.read_bytes()).hexdigest()},'tests_run':result.testsRun,'unique_test_ids':len(set(result.ids)),'subtests':result.subtests,'failures':result.failures,'errors':result.errors,'skipped':result.skipped,'test_ids':result.ids,'success':result.wasSuccessful(),'scope':'synthetic pure module only; no native consumer integration or actual source semantic approval','network':'sandbox deny network; provider environment keys removed','provider_model_calls':0,'earlier_runs':[],'failure_history':'This fresh root focused run only. Historical worker runs retained separately; no new production change.'}
P.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(buffer.getvalue());print(json.dumps({k:v for k,v in report.items() if k!='test_ids'},ensure_ascii=False))
if not result.wasSuccessful():sys.exit(1)
