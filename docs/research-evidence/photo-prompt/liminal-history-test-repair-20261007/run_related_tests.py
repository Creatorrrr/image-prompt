from pathlib import Path
import io,json,unittest,sys
ROOT=Path.cwd()
sys.path.insert(0, str(ROOT))
OUT=ROOT/'docs/research-evidence/photo-prompt/liminal-history-test-repair-20261007'
before=(OUT/'test_before.py').read_text()
namespace={'__name__':'liminal_original_probe','__file__':str(ROOT/'tests/test_photo_liminal_active_use_korean_data_cleanup.py')}
exec(compile(before,namespace['__file__'],'exec'),namespace)
log=io.StringIO()
original=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.TestSuite([
 namespace['LiminalActiveUseKoreanDataCleanupTests']('test_complete_merged_state_and_twenty_one_keeps_remain_exact')]))
(OUT/'failure-before.log').write_text(log.getvalue())
print('Original:',original.testsRun,'failures',len(original.failures),'errors',len(original.errors),flush=True)
names=json.loads((OUT/'test-selection.json').read_text())
with (OUT/'related-tests.log').open('w') as stream:
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
report={'selected_test_ids':len(names),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'success':result.wasSuccessful(),'failing_ids':[t.id() for t,_ in result.failures+result.errors],'full_suite_run':False}
(OUT/'TEST-RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
