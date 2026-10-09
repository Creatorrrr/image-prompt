"""Run unchanged unittest modules in six isolated Python processes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import ast
import json
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
WORKER = '''import json,sys,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
modules=json.loads(Path(sys.argv[1]).read_text())
suite=unittest.defaultTestLoader.loadTestsFromNames(modules)
started=time.time()
result=unittest.TextTestRunner(verbosity=2).run(suite)
summary={"modules":modules,"tests_run":result.testsRun,"failures":[{"id":t.id(),"traceback":v} for t,v in result.failures],"errors":[{"id":t.id(),"traceback":v} for t,v in result.errors],"skips":[{"id":t.id(),"reason":v} for t,v in result.skipped],"seconds":time.time()-started,"success":result.wasSuccessful()}
Path(sys.argv[2]).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\\n")
sys.exit(0 if result.wasSuccessful() else 1)
'''

def main():
 area=HERE/'full-suite-parallel';area.mkdir(exist_ok=True)
 modules=[]
 for p in sorted((ROOT/'tests').glob('test*.py')):
  tree=ast.parse(p.read_text())
  count=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test') for n in ast.walk(tree))
  modules.append(('tests.'+p.stem,count))
 groups=[[] for _ in range(6)];weights=[0]*6
 for module,count in sorted(modules,key=lambda v:-v[1]):
  i=min(range(6),key=lambda k:weights[k]);groups[i].append(module);weights[i]+=count
 (area/'worker.py').write_text(WORKER)
 def run(i):
  inp=area/f'group-{i}.modules.json';out=area/f'group-{i}.result.json'
  inp.write_text(json.dumps(sorted(groups[i])))
  with (area/f'group-{i}.log').open('w') as log:
   result=subprocess.run([sys.executable,str(area/'worker.py'),str(inp),str(out)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  return i,result.returncode,json.loads(out.read_text())
 started=time.time();results=[]
 with ThreadPoolExecutor(max_workers=6) as pool:
  for future in as_completed([pool.submit(run,i) for i in range(6)]):
   i,code,r=future.result();results.append(r)
   print(json.dumps({'group':i,'exit_code':code,'tests':r['tests_run'],'failures':len(r['failures']),'errors':len(r['errors'])}),flush=True)
 summary={'schema':'parallel-unittest-summary/v1','processes':6,'module_count':len(modules),'tests_run':sum(r['tests_run'] for r in results),
  'failures':[v for r in results for v in r['failures']],'errors':[v for r in results for v in r['errors']],
  'skips':[v for r in results for v in r['skips']],'seconds':time.time()-started,'success':all(r['success'] for r in results)}
 (area/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in {'failures','errors','skips'}}),flush=True)
 return 0 if summary['success'] else 1

if __name__=='__main__':sys.exit(main())
