"""Pure offline StageA verification; writes a new, explicitly named report only."""
import io,json,hashlib,time,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/precore'))
R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
OUTPUT=R/'worker-notes/native-existing-member-scope-stageA-RESULTS-01-20261015.json'
LOG=R/'worker-notes/native-existing-member-scope-stageA-TESTS-01-20261015.log'
assert not OUTPUT.exists() and not LOG.exists()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py',ROOT/'skills/photo-prompt-image-generator/precore/photo_authoring_wire.py',ROOT/'tests/test_photo_existing_member_scope_witnesses.py']
pins=[{'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'raw_sha256':h(p)} for p in paths]
modules=['tests.test_photo_existing_member_scope_witnesses','tests.test_photo_native_fact_wire','tests.test_photo_native_v4_guards','tests.test_photo_workflow_precore','tests.test_photo_creative_control_wire_replay','tests.test_photo_precore_feature_selection']
class Result(unittest.TextTestResult):
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.ids=[];self.subtests=[]
 def startTest(self,test):self.ids.append(test.id());super().startTest(test)
 def addSubTest(self,test,subtest,outcome):
  self.subtests.append({'test':test.id(),'subtest':str(subtest),'success':outcome is None});super().addSubTest(test,subtest,outcome)
suite=unittest.TestLoader().loadTestsFromNames(modules);stream=io.StringIO();started=time.monotonic()
result=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=Result).run(suite)
elapsed=time.monotonic()-started
assert all(h(ROOT/pin['file'])==pin['raw_sha256'] for pin in pins)
from tests.test_photo_existing_member_scope_witnesses import fixture,TEXT
rows,env=fixture();oldpath=R/'worker-notes/native-member-stageA-before-20261015/skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py'
namespace={};exec(compile(oldpath.read_text(),str(oldpath),'exec'),namespace)
try:
 namespace['read'](rows,env['active_spans'],TEXT,intent_lock={'locked_dimensions':['subject']},request_binding=env)
 old={'result':'unexpected_accept'}
except ValueError as ex:old={'result':'expected_reject','exception':'ValueError','message':str(ex),'before_raw_sha256':h(oldpath)}
report={'schema':'photo-native-member-stageA-tests/v1','command':"/usr/bin/env -i HOME=/Users/chasoik PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 "+str(Path(__file__).relative_to(ROOT)),
 'modules':modules,'executions':result.testsRun,'unique_tests':len(set(result.ids)),'subtest_executions':len(result.subtests),'failures':len(result.failures),'errors':len(result.errors),'skips':len(result.skipped),'elapsed_seconds':elapsed,
 'executed_code':pins,'test_ids':result.ids,'subtests':result.subtests,'failures_detail':[(x.id(),trace) for x,trace in result.failures], 'errors_detail':[(x.id(),trace) for x,trace in result.errors],
 'before_probe':old,'development_runs_before_this_report':[{'tests':16,'result':'PASS; tool-output evidence only'},{'tests':17,'result':'PASS; tool-output evidence only'}],
 'scope':'Exact frozen code focused new tests plus existing neutral wire/precore regression. Not runtime member resolution, source qualification, rendered pixels or independently observed membership/completeness.', 'calls':{'provider':0,'model':0,'Gemini':0,'network':0,'git_mutations':0}}
LOG.write_text(stream.getvalue());report['log']={'file':str(LOG.relative_to(ROOT)),'raw_sha256':h(LOG)}
OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['executions','unique_tests','subtest_executions','failures','errors','skips','elapsed_seconds']},ensure_ascii=False));print(str(OUTPUT.relative_to(ROOT)),h(OUTPUT))
if not result.wasSuccessful() or old['result']!='expected_reject':sys.exit(1)
