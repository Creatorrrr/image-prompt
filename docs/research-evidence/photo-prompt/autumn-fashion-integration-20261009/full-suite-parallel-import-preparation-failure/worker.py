import json,sys,time,unittest
from pathlib import Path
modules=json.loads(Path(sys.argv[1]).read_text())
suite=unittest.defaultTestLoader.loadTestsFromNames(modules)
started=time.time()
result=unittest.TextTestRunner(verbosity=2).run(suite)
summary={"modules":modules,"tests_run":result.testsRun,"failures":[{"id":t.id(),"traceback":v} for t,v in result.failures],"errors":[{"id":t.id(),"traceback":v} for t,v in result.errors],"skips":[{"id":t.id(),"reason":v} for t,v in result.skipped],"seconds":time.time()-started,"success":result.wasSuccessful()}
Path(sys.argv[2]).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
sys.exit(0 if result.wasSuccessful() else 1)
