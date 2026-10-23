"""Exercise existing sealed-runtime tests; restore the tracked selection byte-exact."""
from pathlib import Path
import unittest,sys,json,hashlib,io,time
ROOT=Path(__file__).resolve().parents[5]
PUB=Path(__file__).resolve().parent
skill=ROOT/'skills/photo-prompt-image-generator'
config=skill/'retrieval-runtime.json'
original=config.read_bytes()
local=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/retrieval-runtime.json').read_bytes()
started=time.monotonic()
stream=io.StringIO()
try:
 config.write_bytes(local)
 sys.path.insert(0,str(skill/'tests'))
 suite=unittest.defaultTestLoader.loadTestsFromNames(['test_h_f2_primary_proof_boundaries','test_h_f2_source_context','test_h_f2_sampling'])
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
finally:
 config.write_bytes(original)
 assert config.read_bytes()==original
(PUB/'regression-tests.txt').write_text(stream.getvalue())
report={'status':'pass' if result.wasSuccessful() else 'fail','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'elapsed_seconds':time.monotonic()-started,'tracked_config_restored_sha256':hashlib.sha256(original).hexdigest(),'test_only_installed_config_sha256':hashlib.sha256(local).hexdigest(),'test_only_generation_id':json.loads(local)['generation_id'],'source_and_installed_runtime_tests_distinct':True}
(PUB/'regression-tests.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report));sys.exit(not result.wasSuccessful())
