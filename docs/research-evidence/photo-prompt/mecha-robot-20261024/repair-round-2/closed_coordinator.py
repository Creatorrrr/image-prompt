"""Invoke the closed projector with scheduling-only GC adjustment."""
import gc,json,sys
gc.disable()
sys.path.insert(0,sys.argv[1])
import prepare_retry_context as p
d=json.load(open(sys.argv[2]));argv=['prepare']
for k,v in d.items():argv.extend(['--'+k.replace('_','-'),v])
from argparse import Namespace
p.prepare(Namespace(**{k:__import__("pathlib").Path(v) for k,v in d.items()}))
print("closed projection PASS",flush=True)
