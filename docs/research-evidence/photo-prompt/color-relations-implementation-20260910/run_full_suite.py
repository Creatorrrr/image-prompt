"""Run every test module in separate bounded processes; do not rewrite fixtures."""
import concurrent.futures
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
LOGS = HERE/'full-suite-modules'
LOGS.mkdir(exist_ok=True)
os.chdir(ROOT)
sys.path.insert(0,str(ROOT))
suite=unittest.defaultTestLoader.discover('tests')

def flatten(s):
    for t in s:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t

cases=list(flatten(suite))
modules=sorted({t.__class__.__module__ for t in cases})
counts={m:sum(t.__class__.__module__==m for t in cases) for m in modules}
start=time.time()
results=[]

def run(module):
    begin=time.time();log=LOGS/(module+'.log')
    with log.open('w') as f:
        done=subprocess.run([str(ROOT/'.venv/bin/python'),'-m','unittest','tests.'+module,'-v'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    text=log.read_text()
    return {'module':module,'expected_test_count':counts[module],
        'executed_test_count':int(re.search(r'Ran (\d+) tests?',text).group(1)) if re.search(r'Ran (\d+) tests?',text) else None,
        'exit_code':done.returncode,'elapsed_seconds':round(time.time()-begin,2),
        'failure_headers':re.findall(r'^(?:FAIL|ERROR): .+$',text,re.M),'log':str(log.relative_to(ROOT))}

def save():
    (HERE/'full-suite-parallel-status.json').write_text(json.dumps({'status':'running' if len(results)<len(modules) else 'completed',
      'mode':'all discovered modules in isolated processes; concurrency 6; no test filtering',
      'expected_test_count':len(cases),'module_count':len(modules),'completed_modules':len(results),
      'elapsed_seconds':round(time.time()-start,2),'results':sorted(results,key=lambda x:x['module'])},indent=2)+'\n')

save()
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    futures=[pool.submit(run,m) for m in modules]
    for f in concurrent.futures.as_completed(futures):
        r=f.result();results.append(r);save()
        print(f"{len(results)}/{len(modules)} {r['module']}: exit {r['exit_code']}",flush=True)
save()
