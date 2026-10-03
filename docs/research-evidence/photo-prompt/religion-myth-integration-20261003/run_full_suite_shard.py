#!/usr/bin/env python3
"""Execute every normally discovered test once across independent processes."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
shard = int(sys.argv[1])
count = 4
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))

def cases(value):
    for item in value:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item

modules = {}
for test in cases(suite):
    modules.setdefault(test.__class__.__module__, []).append(test)
groups = [[] for _ in range(count)]
loads = [0] * count
for module in sorted(modules, key=lambda name: (-len(modules[name]), name)):
    target = min(range(count), key=lambda index: (loads[index], index))
    groups[target].append(module)
    loads[target] += len(modules[module])
selected = unittest.TestSuite(test for name in sorted(groups[shard]) for test in modules[name])
ids = [test.id() for test in cases(selected)]
plan = {'shard': shard, 'shard_count': count, 'modules': sorted(groups[shard]),
        'test_count': len(ids), 'all_discovered_count': suite.countTestCases(),
        'test_ids': ids, 'test_ids_sha256': hashlib.sha256('\n'.join(ids).encode()).hexdigest()}
(HERE / f'full-suite-shard-{shard}-plan.json').write_text(json.dumps(plan, indent=2) + '\n')
result = unittest.TextTestRunner(verbosity=2).run(selected)
out = {'shard': shard, 'tests_run': result.testsRun,
       'failures': [test.id() for test, _ in result.failures],
       'errors': [test.id() for test, _ in result.errors],
       'skipped': [test.id() for test, _ in result.skipped],
       'expected_failures': [test.id() for test, _ in result.expectedFailures],
       'unexpected_successes': [test.id() for test in result.unexpectedSuccesses],
       'successful': result.wasSuccessful(), 'test_ids_sha256': plan['test_ids_sha256']}
(HERE / f'full-suite-shard-{shard}-result.json').write_text(json.dumps(out, indent=2) + '\n')
sys.exit(0 if result.wasSuccessful() else 1)
