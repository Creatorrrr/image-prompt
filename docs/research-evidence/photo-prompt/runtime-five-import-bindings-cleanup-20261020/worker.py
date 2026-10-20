"""Exercise the exact current/private source; no real network or model calls."""
import ast,hashlib,importlib,inspect,json,os,sys,unittest
from pathlib import Path
project=Path(sys.argv[1]).resolve();removed=sys.argv[2]=='1';config=json.loads((Path(__file__).parent/'TARGETS.json').read_bytes())
os.chdir(project);skill=project/'skills/photo-prompt-image-generator';sys.path[:0]=[str(project),str(skill/'scripts'),str(skill/'precore')]
names=['prompt_generator','audit_composed_prompt','photo_workflow_worker','generate_images_via_api','photo_workflow_state','photo_api_render','photo_contracts','photo_runtime_sources']
mods={name:importlib.import_module(name) for name in names}
for row in config['imports']:
    assert hasattr(mods[row['module']],row['binding'])!=removed,row
    assert hasattr(mods[row['provider']],row['imported']),row
assert mods['photo_workflow_worker'].bound_path is mods['photo_workflow_state'].bound_path
assert mods['photo_workflow_worker'].read_json is mods['photo_workflow_state'].read_json
assert mods['generate_images_via_api'].prepare_api_render is mods['photo_api_render'].prepare_api_render
assert mods['generate_images_via_api'].save_preflight is mods['photo_api_render'].save_preflight
assert issubclass(mods['photo_workflow_state'].WorkflowError,Exception) and issubclass(mods['photo_api_render'].PreflightError,Exception)
runtime=mods['photo_runtime_sources'];binding=runtime.algorithm_binding(mods['prompt_generator'])
assert binding==runtime.algorithm_binding(None)==runtime.algorithm_binding({})
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
try:runtime._require_implementation({'code':{**runtime.LOADED_CODE,'scripts/foreign.py':'bad'},'environment':runtime.LOADED_ENVIRONMENT},None)
except runtime.FreshnessError:pass
else:raise AssertionError('implementation guard weakened')
loaded={}
for name,m in mods.items():
    p=Path(m.__file__).resolve();assert p.is_relative_to(project),p
    loaded[name]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[3:]))
print(json.dumps({'status':'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL','tests':result.testsRun,'skipped':len(result.skipped),
    'loaded_modules':loaded,'provider_definitions_retained':True,'implementation_guards_preserved':True,'algorithm_without_code':{k:v for k,v in binding.items() if k!='code'},
    'failures':[(t.id(),x.replace(str(project),'<project>')) for t,x in result.failures],'errors':[(t.id(),x.replace(str(project),'<project>')) for t,x in result.errors]}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
