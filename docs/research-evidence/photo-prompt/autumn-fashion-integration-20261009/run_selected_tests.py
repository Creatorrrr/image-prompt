import sys,json,unittest,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
sys.path.insert(0,str(Path.cwd()/"tests"))
ids=json.loads(Path(sys.argv[1]).read_text())
suite=unittest.defaultTestLoader.loadTestsFromNames(ids)
started=time.time()
r=unittest.TextTestRunner(verbosity=2).run(suite)
s={"cwd":str(Path.cwd()),"requested_tests":ids,"tests_run":r.testsRun,"failures":[{"id":t.id(),"traceback":v} for t,v in r.failures],"errors":[{"id":t.id(),"traceback":v} for t,v in r.errors],"skips":[{"id":t.id(),"reason":v} for t,v in r.skipped],"seconds":time.time()-started,"success":r.wasSuccessful()}
Path(sys.argv[2]).write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n")
sys.exit(0 if r.wasSuccessful() else 1)
