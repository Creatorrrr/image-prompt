"""Load the actual qualified source and run existing tests without model inference."""
import ast
import hashlib
import importlib
import inspect
import json
import os
from pathlib import Path
import sys
import unittest

project = Path(sys.argv[1]).resolve()
removed = sys.argv[2] == '1'
os.chdir(project)
sys.path.insert(0, str(project))
sys.path.insert(0, str(project/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
import audit_composed_prompt
import photo_runtime_sources as runtime

bindings = {'photo_contracts': ['hashlib', 'json', 'Any'],
            'photo_embodiment': ['copy', 'hashlib', 'json', 'Any'],
            'photo_shared_views': ['Path', 'index']}
loaded = {}
for name in [*bindings, 'photo_runtime_sources', 'prompt_generator', 'audit_composed_prompt']:
    module = importlib.import_module(name)
    for binding in bindings.get(name, []):
        assert hasattr(module, binding) != removed, (name, binding)
    path = Path(module.__file__).resolve()
    assert path.is_relative_to(project), path
    loaded[name] = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
tree = ast.parse(Path(runtime.__file__).read_bytes())
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'algorithm_binding')
has_local = any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'get' for t in n.targets) for n in function.body)
assert has_local != removed
values = [runtime.algorithm_binding(value) for value in (generator, {}, None)]
assert all(value == values[0] for value in values)
assert len(runtime.LOADED_CODE) == 76
runtime._require_implementation({'code': runtime.LOADED_CODE, 'environment': runtime.LOADED_ENVIRONMENT}, None)
try:
    runtime._require_implementation({'code': {**runtime.LOADED_CODE, 'scripts/foreign.py': 'bad'},
        'environment': runtime.LOADED_ENVIRONMENT}, None)
except runtime.FreshnessError as error:
    assert error.state == 'runtime_restart_required'
else:
    raise AssertionError('implementation guard weakened')
suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[3:])
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'status': 'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL',
    'tests': result.testsRun, 'skipped': len(result.skipped), 'loaded_modules': loaded,
    'implementation_guard_preserved': True, 'code_files': len(runtime.LOADED_CODE),
    'algorithm_without_code': {key: value for key, value in values[0].items() if key != 'code'},
    'algorithm_module_dict_none_inputs_equal': True,
    'algorithm_binding_signature': str(inspect.signature(runtime.algorithm_binding)),
    'failures': [(test.id(), detail.replace(str(project), '<project>')) for test, detail in result.failures],
    'errors': [(test.id(), detail.replace(str(project), '<project>')) for test, detail in result.errors]}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
