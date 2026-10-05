"""Run the unchanged unittest methods in isolated processes, grouped by module."""
import collections
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT))
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),top_level_dir=str(ROOT))
def flat(s):
    for item in s:
        if isinstance(item,unittest.TestSuite):yield from flat(item)
        else:yield item
counts=collections.Counter(test.id().rsplit('.',2)[0] for test in flat(suite))
groups=[[] for _ in range(6)];loads=[0]*6
for module,count in sorted(counts.items(),key=lambda x:(-x[1],x[0])):
    idx=min(range(6),key=lambda x:loads[x]);groups[idx].append(module);loads[idx]+=count
plan=dict(test_count=sum(counts.values()),module_count=len(counts),groups=[dict(index=i,expected_tests=loads[i],modules=mods) for i,mods in enumerate(groups)])
(HERE/'FULL-REGRESSION-PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
running=[]
for i,modules in enumerate(groups):
    log=HERE/f'full-regression-group-{i}.log';handle=log.open('w')
    p=subprocess.Popen([sys.executable,'-u','-m','unittest',*modules],cwd=ROOT,stdout=handle,stderr=subprocess.STDOUT)
    running.append((i,p,handle,log))
done=[]
while running:
    for row in running[:]:
        i,p,handle,log=row
        if p.poll() is None:continue
        handle.close();done.append(dict(index=i,exit_code=p.returncode,log=str(log.relative_to(ROOT)),expected_tests=loads[i]));running.remove(row)
        print(f'group {i}: exit={p.returncode}, expected_tests={loads[i]}',flush=True)
    if running:time.sleep(1)
result=dict(test_count=sum(counts.values()),module_count=len(counts),groups=sorted(done,key=lambda r:r['index']),all_pass=all(r['exit_code']==0 for r in done))
(HERE/'FULL-REGRESSION-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
sys.exit(0 if result['all_pass'] else 1)
