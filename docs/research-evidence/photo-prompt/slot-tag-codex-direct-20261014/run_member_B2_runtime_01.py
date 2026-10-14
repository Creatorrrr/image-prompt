"""Zero-inference operating publication gated on the exact root B2 regression."""
from __future__ import annotations
import hashlib
import importlib.abc
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'member-B2-integration-01'
SCRIPTS = ROOT / 'skills/photo-prompt-image-generator/scripts'
sys.path[:0] = [str(ROOT), str(SCRIPTS)]
regression = json.loads((HERE / 'run_member_B2_root_integration_01.json').read_bytes())
assert regression['successful'] and not regression['errors'] and not regression['failures'] and not regression['skipped']
assert not regression['blocked_embedding_attempts'] and not regression['model_imports_loaded']
assert regression['source_bytes_stable'] and regression['executions'] >= 438
pins = regression['after_hashes']
assert pins['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py'] == '35fbb2b6af1140f914b73fadd6e3833629ad6409efbbcf9c281f2f606b607548'


def verify():
    for name, expected in pins.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name


class NoModels(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch', 'transformers', 'sentence_transformers', 'tensorflow', 'jax', 'mlx'}:
            raise RuntimeError('No model import allowed during metadata-only B2 publication: ' + fullname)


verify()
sys.meta_path.insert(0, NoModels())
OUT.mkdir(exist_ok=False)
import photo_local_embedding as local


def forbidden(*args, **kwargs):
    raise RuntimeError('B2 metadata publication forbids all local/provider inference')


local.infer = forbidden
spec = importlib.util.spec_from_file_location('root_B2_runtime_helper', HERE / 'root_verify_native_v4.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
helper.HERE = OUT
helper.runtime()
verify()
assert local._WORKER is None
with (OUT / 'FROZEN-PRODUCTION-PINS.json').open('x') as stream:
    json.dump({'schema': 'photo-root-runtime-production-pins/v1', 'all_pins_before_and_after_equal': True,
        'pins': pins, 'regression': 'run_member_B2_root_integration_01.json', 'local_inference_forbidden': True,
        'canonical_source_catalog_or_native_qualifications_changed': False}, stream, sort_keys=True, indent=2)
    stream.write('\n')
