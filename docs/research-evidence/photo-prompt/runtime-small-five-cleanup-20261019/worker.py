
import sys,os,json,unittest,hashlib
from pathlib import Path
project=Path(sys.argv[1]).resolve();small=json.loads(sys.argv[2]);drop_imports=sys.argv[3]=='1';sys.path.insert(0,str(project));sys.path.insert(0,str(project/'skills/photo-prompt-image-generator/scripts'));os.chdir(project)
import photo_runtime_sources as runtime
before_generator='photo_shared_views' in sys.modules
assert hasattr(runtime,'SearchReader') != drop_imports
assert hasattr(runtime,'photo_shared_views') != drop_imports
from photo_search_reader import LazyRuntimeData,identity
assert runtime.LazyRuntimeData is LazyRuntimeData and runtime.identity is identity
import prompt_generator as generator,audit_composed_prompt as audit
for name in small:assert not hasattr(audit if name=='english_prompt_word_count' else generator,name)
modules={}
for m in (runtime,generator,audit):
 p=Path(m.__file__).resolve();assert p.is_relative_to(project);modules[m.__name__]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
assert len(runtime.LOADED_CODE)==76
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
try:runtime._require_implementation({'code':{**runtime.LOADED_CODE,'scripts/foreign.py':'bad'},'environment':runtime.LOADED_ENVIRONMENT},None)
except runtime.FreshnessError as e:assert e.state=='runtime_restart_required'
else:raise AssertionError('source guard weakened')
suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[4:]);r=unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'status':'PASS' if r.wasSuccessful() and not r.skipped else 'FAIL','tests':r.testsRun,'skipped':len(r.skipped),'loaded_modules':modules,'source_guard_preserved':True,'shared_views_loaded_before_generator':before_generator}))
sys.exit(not r.wasSuccessful() or bool(r.skipped))
