"""Run every discovered module once, partitioned into independent processes."""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
import unittest
from collections import Counter
from pathlib import Path

def flatten(suite):
 for item in suite:
  if isinstance(item,unittest.TestSuite):yield from flatten(item)
  else:yield item

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--workers',type=int,default=8);a=p.parse_args()
 os.chdir(a.root);a.output_dir.mkdir(parents=True,exist_ok=True)
 sys.path.insert(0, str(a.root/'tests'))
 suite=unittest.TestLoader().discover(str(a.root/'tests'),top_level_dir=str(a.root))
 def module_name(t):
  # Failed imports retain their actual module names and must be invoked.
  if t.__class__.__name__ == '_FailedTest':
   return t.id().split('unittest.loader._FailedTest.',1)[1]
  return t.__class__.__module__
 counts=Counter(module_name(t) for t in flatten(suite))
 partitions=[dict(modules=[],expected_tests=0) for _ in range(a.workers)]
 for module,n in sorted(counts.items(),key=lambda item:(-item[1],item[0])):
  dest=min(partitions,key=lambda b:b['expected_tests']);dest['modules'].append(module);dest['expected_tests']+=n
 (a.output_dir/'DISCOVERY.json').write_text(json.dumps(dict(total_tests=sum(counts.values()),module_count=len(counts),module_counts=dict(counts),partitions=partitions),indent=2)+'\n')
 def run(i,part):
  env=os.environ.copy();env['PHOTO_RUNTIME_STORE']=str(a.root/'.photo-runtime-test-partitions'/str(i));env['PYTHONUNBUFFERED']='1'
  env['PYTHONPATH']=str(a.root/'tests')+os.pathsep+str(a.root)
  logfile=a.output_dir/f'partition-{i}.log';started=time.monotonic()
  with logfile.open('w') as out:
   rc=subprocess.call([str(a.root/'.venv/bin/python'),'-m','unittest','-v',*part['modules']],cwd=a.root,env=env,stdout=out,stderr=subprocess.STDOUT)
  text=logfile.read_text();ran=re.search(r'Ran (\d+) tests? in ([\d.]+)s',text)
  result=dict(partition=i,exit_code=rc,elapsed_seconds=round(time.monotonic()-started,2),expected_tests=part['expected_tests'],ran_tests=int(ran.group(1)) if ran else None,log=str(logfile),modules=part['modules'],status='PASS' if rc==0 else 'FAIL')
  (a.output_dir/f'partition-{i}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);return result
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
  results=list(pool.map(lambda indexed:run(*indexed),enumerate(partitions)))
 complete=sum(r['ran_tests'] or 0 for r in results)==sum(counts.values())
 result=dict(schema_version='ethereal-gothic-full-suite/v1',discovered_tests=sum(counts.values()),discovered_modules=len(counts),workers=a.workers,complete_execution=complete,results=results,status='PASS' if complete and all(r['exit_code']==0 for r in results) else 'FAIL')
 (a.output_dir/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 return 0 if result['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
