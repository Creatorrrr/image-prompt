"""Record real unittest outcomes and selector-level baseline evidence."""
import argparse
import json
from pathlib import Path
import sys
import unittest

OUT = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--lane', required=True)
p.add_argument('selectors', nargs='*')
args = p.parse_args()
sys.path.insert(0, str(args.root))
loader = unittest.TestLoader()
suite = (loader.loadTestsFromNames(args.selectors) if args.selectors
         else loader.discover(str(args.root / 'tests'), top_level_dir=str(args.root)))
with (OUT / (args.lane + '-tests.log')).open('w') as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
data = dict(tests_run=result.testsRun, failures=[dict(selector=t.id(), traceback=s)
    for t, s in result.failures], errors=[dict(selector=t.id(), traceback=s)
    for t, s in result.errors], skipped=[dict(selector=t.id(), reason=s)
    for t, s in result.skipped], successful=result.wasSuccessful(),
    root=str(args.root), lane=args.lane)
(OUT / (args.lane + '-tests.json')).write_text(json.dumps(data, ensure_ascii=False,
    indent=2) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in data.items()}),
    flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
