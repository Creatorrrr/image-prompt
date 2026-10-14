"""Root zero-inference metadata publication after exact integrated regressions."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'guard-support-integration-01'
SCRIPTS = ROOT / 'skills/photo-prompt-image-generator/scripts'
sys.path[:0] = [str(ROOT), str(SCRIPTS)]
regression = json.loads((HERE / 'run_guard_member_root_integration_02.json').read_bytes())
assert regression['successful'] and not regression['errors'] and not regression['failures']
assert not regression['blocked_embedding_attempts'] and not regression['model_imports_loaded']
assert (regression['executions'], regression['unique_tests'], regression['subtests']) == (411, 399, 991)
pins = regression['after_hashes']


def verify():
    for name, expected in pins.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name


verify()
OUT.mkdir(exist_ok=False)
import photo_local_embedding as local


def forbidden(*args, **kwargs):
    raise RuntimeError('Root runtime verification forbids local inference as well as provider execution')


local.infer = forbidden
spec = importlib.util.spec_from_file_location('root_guard_support_runtime', HERE / 'root_verify_native_v4.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
helper.HERE = OUT
helper.runtime()
verify()
with (OUT / 'FROZEN-PRODUCTION-PINS.json').open('x') as stream:
    json.dump({'schema': 'photo-root-runtime-production-pins/v1',
        'all_pins_before_and_after_equal': True, 'pins': pins,
        'regression': 'run_guard_member_root_integration_02.json',
        'local_inference_forbidden': True}, stream, sort_keys=True, indent=2)
    stream.write('\n')
