"""Exercise actual private/applied modules; no inference or runtime publication."""
import hashlib
import importlib
import inspect
import json
import os
from pathlib import Path
import sys
import unittest

project=Path(sys.argv[1]).resolve(); removed=sys.argv[2]=='1'
configuration=json.loads((Path(__file__).parent/'TARGETS.json').read_bytes())
os.chdir(project)
sys.path.insert(0,str(project))
sys.path.insert(0,str(project/'skills/photo-prompt-image-generator/precore'))
sys.path.insert(0,str(project/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
import audit_composed_prompt
import photo_runtime_sources as runtime

for name in configuration['functions']:
    assert hasattr(generator,name) != removed, name
loaded={}
for name in dict.fromkeys(['prompt_generator','audit_composed_prompt','photo_runtime_sources',*configuration['imports']]):
    module=importlib.import_module(name)
    for binding in configuration['imports'].get(name,[]):
        assert hasattr(module,binding) != removed,(name,binding)
    path=Path(module.__file__).resolve(); assert path.is_relative_to(project),path
    loaded[name]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert len(runtime.LOADED_CODE)==76
values=[runtime.algorithm_binding(value) for value in (generator,{},None)]
assert all(value==values[0] for value in values)
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
try:
    runtime._require_implementation({'code':{**runtime.LOADED_CODE,'scripts/foreign.py':'bad'},'environment':runtime.LOADED_ENVIRONMENT},None)
except runtime.FreshnessError as error:
    assert error.state=='runtime_restart_required'
else: raise AssertionError('implementation guard weakened')
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[3:]))
print(json.dumps({'status':'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL',
    'tests':result.testsRun,'skipped':len(result.skipped),'loaded_modules':loaded,'code_files':len(runtime.LOADED_CODE),
    'implementation_guard_preserved':True,'algorithm_module_dict_none_inputs_equal':True,
    'algorithm_without_code':{k:v for k,v in values[0].items() if k!='code'},
    'algorithm_binding_signature':str(inspect.signature(runtime.algorithm_binding)),
    'failures':[(test.id(),detail.replace(str(project),'<project>')) for test,detail in result.failures],
    'errors':[(test.id(),detail.replace(str(project),'<project>')) for test,detail in result.errors]}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
