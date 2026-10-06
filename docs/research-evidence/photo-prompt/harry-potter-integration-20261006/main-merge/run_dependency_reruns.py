from pathlib import Path
import json,unittest,sys
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));ids=set()
for p in OUT.glob('full-suite-part-*.json'):
 for item in json.loads(p.read_bytes())['details']:
  name=item['test_id']
  if any(prefix in name for prefix in ('test_photo_makeup_reference_balance.','test_photo_poverty_visual_semantics.','test_photo_rare_','test_photo_liminal_active_use_korean_data_cleanup.')):ids.add(name)
assert ids
statuses={};details=[]
class Result(unittest.TextTestResult):
 def addSuccess(self,t):statuses[t.id().removeprefix('tests.')]='PASS';super().addSuccess(t)
 def addFailure(self,t,e):statuses[t.id().removeprefix('tests.')]='FAIL';details.append({'test_id':t.id().removeprefix('tests.'),'traceback':self._exc_info_to_string(e,t)});super().addFailure(t,e)
 def addError(self,t,e):statuses[t.id().removeprefix('tests.')]='ERROR';details.append({'test_id':t.id().removeprefix('tests.'),'traceback':self._exc_info_to_string(e,t)});super().addError(t,e)
 def addSubTest(self,t,st,e):
  if e:statuses[t.id().removeprefix('tests.')]='FAIL';details.append({'test_id':t.id().removeprefix('tests.'),'traceback':self._exc_info_to_string(e,t)})
  super().addSubTest(t,st,e)
with (OUT/'dependency-reruns.final.log').open('w') as stream:r=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=Result).run(unittest.TestLoader().loadTestsFromNames(['tests.'+name for name in sorted(ids)]))
(OUT/'DEPENDENCY-RERUNS.json').write_text(json.dumps({'tests_run':r.testsRun,'successful':r.wasSuccessful(),'outcomes':statuses,'details':details},indent=2)+'\n')
print('dependency reruns',statuses)
# A pre-existing exact historical inventory mismatch is retained, never rebaselined.
remaining={name for name,value in statuses.items() if value!='PASS'}
expected={'test_photo_liminal_active_use_korean_data_cleanup.LiminalActiveUseKoreanDataCleanupTests.test_complete_merged_state_and_twenty_one_keeps_remain_exact'}
sys.exit(0 if remaining==expected and all('glass_near_contact_reflected_fringes' in row['traceback'] for row in details) else 1)
