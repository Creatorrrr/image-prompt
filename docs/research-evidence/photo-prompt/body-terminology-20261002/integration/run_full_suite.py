"""Run the complete unittest discovery as isolated module processes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
parser = argparse.ArgumentParser()
parser.add_argument('--output-directory', default=str(BASE))
OUT = Path(parser.parse_args().output_directory).resolve()
OUT.mkdir(parents=True, exist_ok=True)
LOGS = OUT / 'full-suite-modules'
LOGS.mkdir(exist_ok=True)
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), top_level_dir=str(ROOT))

def cases(node):
    if isinstance(node, unittest.TestSuite):
        for item in node:
            yield from cases(item)
    else:
        yield node

discovered = list(cases(suite))
modules = sorted({test.__class__.__module__ for test in discovered})
if 'unittest.loader' in modules:
    unittest.TextTestRunner().run(suite)
    raise SystemExit('Discovery failed; no partial module summary is accepted.')
manifest = dict(schema_version='complete-unittest-discovery/v1',
    python=sys.executable, module_count=len(modules), test_count=len(discovered),
    test_ids=[test.id() for test in discovered], workers=6)
(OUT / 'FULL-TEST-DISCOVERY.json').write_text(json.dumps(manifest, indent=2) + '\n')

def run(module):
    start=time.monotonic()
    log=LOGS / (module + '.log')
    with log.open('w') as output:
        result=subprocess.run([sys.executable, '-m', 'unittest', module], cwd=ROOT,
            stdout=output, stderr=subprocess.STDOUT)
    content=log.read_text()
    count=re.search(r'Ran (\d+) tests?', content)
    return dict(module=module, exit_code=result.returncode,
        seconds=round(time.monotonic()-start,3),
        tests_run=int(count[1]) if count else None, log=str(log.relative_to(ROOT)))

results=[]
with ThreadPoolExecutor(max_workers=6) as executor:
    pending={executor.submit(run,module):module for module in modules}
    for future in as_completed(pending):
        results.append(future.result())
        progress=dict(status='RUNNING', completed_modules=len(results), module_count=len(modules), results=results)
        (OUT / 'FULL-TEST-PROGRESS.json').write_text(json.dumps(progress, indent=2) + '\n')
        if len(results)%10==0 or results[-1]['exit_code']:
            print(len(results), '/', len(modules), 'modules complete;',
                  'failures:', sum(r['exit_code']!=0 for r in results), flush=True)

failed=[r for r in results if r['exit_code']]
summary=dict(schema_version='complete-unittest-module-results/v1',
    status='PASS' if not failed else 'FAIL', module_count=len(modules),
    discovered_tests=len(discovered), tests_run=sum(r['tests_run'] or 0 for r in results),
    failed_modules=[r['module'] for r in failed], results=sorted(results,key=lambda r:r['module']))
(OUT / 'FULL-TEST-RESULTS.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'}), flush=True)
raise SystemExit(bool(failed))
