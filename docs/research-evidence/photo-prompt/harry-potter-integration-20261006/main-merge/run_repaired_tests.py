from pathlib import Path
import json,unittest,sys,time
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
modules=['tests.test_photo_harry_appearance_semantics','tests.test_photo_appearance_boundary_history','tests.test_photo_ct073_back_band_data']
statuses={};details=[]
class Result(unittest.TextTestResult):
 def addSuccess(self,t):statuses[t.id().removeprefix('tests.')]='PASS';super().addSuccess(t)
 def addFailure(self,t,e):statuses[t.id().removeprefix('tests.')]='FAIL';details.append(self._exc_info_to_string(e,t));super().addFailure(t,e)
 def addError(self,t,e):statuses[t.id().removeprefix('tests.')]='ERROR';details.append(self._exc_info_to_string(e,t));super().addError(t,e)
 def addSubTest(self,t,st,e):
  if e:statuses[t.id().removeprefix('tests.')]='FAIL';details.append(self._exc_info_to_string(e,t))
  super().addSubTest(t,st,e)
with (OUT/'repaired-tests.final.log').open('w') as stream:r=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=Result).run(unittest.TestLoader().loadTestsFromNames(modules))
(OUT/'REPAIRED-TESTS.json').write_text(json.dumps({'tests_run':r.testsRun,'successful':r.wasSuccessful(),'outcomes':statuses,'details':details},indent=2)+'\n')
print('repaired tests',r.testsRun,'success',r.wasSuccessful())
sys.exit(0 if r.wasSuccessful() else 1)
