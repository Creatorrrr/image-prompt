import json,sys,time,unittest,traceback
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tests'))
ids_path=Path(sys.argv[1]);ids=json.loads(ids_path.read_text())
start=time.monotonic()
log=ids_path.with_suffix('.log')
with log.open('w') as stream:
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(ids))
report={'requested_ids':ids,'tests_run':result.testsRun,'seconds':round(time.monotonic()-start,3),'successful':result.wasSuccessful(),'failures':[{'id':t.id(),'trace':trace} for t,trace in result.failures],'errors':[{'id':t.id(),'trace':trace} for t,trace in result.errors],'skipped':[{'id':t.id(),'reason':reason} for t,reason in result.skipped]}
ids_path.with_suffix('.result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:report[k] for k in ['tests_run','seconds','successful']}))
sys.exit(0 if result.wasSuccessful() else 1)
