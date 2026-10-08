#!/usr/bin/env python3
"""Run every unittest discovery module with bounded independent processes."""
import argparse
import collections
import concurrent.futures
import json
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--workers',type=int,default=6);args=p.parse_args()
root=args.root.resolve();output=root/'docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/full-suite-modules';output.mkdir(exist_ok=True)
sys.path.insert(0,str(root));suite=unittest.defaultTestLoader.discover(str(root/'tests'))
ids=[]
def flatten(item):
    if isinstance(item,unittest.TestSuite):
        for child in item:flatten(child)
    else:ids.append(item.id())
flatten(suite)
counts=collections.Counter(x.split('.')[0] for x in ids)
modules=sorted(counts,key=lambda x:(-counts[x],x))
def run_module(name):
    start=time.time();log=output/(name+'.log')
    with log.open('wb') as stream:
        result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',name+'.py','-v'],cwd=root,stdout=stream,stderr=subprocess.STDOUT)
    text=log.read_text(errors='replace');matches=re.findall(r'Ran (\d+) tests? in',text)
    return {'module':name,'exit_code':result.returncode,'seconds':round(time.time()-start,3),
        'expected_discovered_cases':counts[name],'reported_cases':int(matches[-1]) if matches else None,
        'failures':re.findall(r'^FAIL: (.+)$',text,re.M),'errors':re.findall(r'^ERROR: (.+)$',text,re.M),'log':str(log)}
records=[];start=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
    futures={pool.submit(run_module,name):name for name in modules}
    for future in concurrent.futures.as_completed(futures):
        record=future.result();records.append(record)
        with (output/'completed.ndjson').open('a') as f:f.write(json.dumps(record)+'\n')
        print(json.dumps({'completed':len(records),'total_modules':len(modules),'module':record['module'],'exit_code':record['exit_code'],'cases':record['reported_cases']}),flush=True)
report={'schema_version':'photo-full-discovery-module-run/v1','workers':args.workers,'seconds':round(time.time()-start,3),
        'discovered_cases':len(ids),'modules':len(modules),'reported_cases':sum(r['reported_cases'] or 0 for r in records),
        'passed_modules':sum(r['exit_code']==0 for r in records),'failed_modules':sum(r['exit_code']!=0 for r in records),
        'all_cases_accounted':all(r['expected_discovered_cases']==r['reported_cases'] for r in records),
        'records':sorted(records,key=lambda r:r['module'])}
(output/'SUMMARY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)
sys.exit(0 if report['failed_modules']==0 and report['all_cases_accounted'] else 1)
