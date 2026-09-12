"""Bounded parallel unittest discovery; preserve every module's output and status."""
from pathlib import Path
import concurrent.futures,json,subprocess,sys,time,re,unittest
ROOT=Path.cwd();OUT=ROOT/"docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/full-suite"
OUT.mkdir(parents=True,exist_ok=True)
suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"),top_level_dir=str(ROOT))
def flatten(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from flatten(x)
  else:yield x
tests=list(flatten(suite));modules=sorted({t.__class__.__module__ for t in tests})
(OUT/"discovery.json").write_text(json.dumps({"count":len(tests),"modules":modules,"test_ids":[t.id() for t in tests]},indent=2)+"\n")
def run(m):
 start=time.monotonic()
 try:
  p=subprocess.run([sys.executable,"-m","unittest",m,"-v"],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  log=p.stdout;rc=p.returncode
 except subprocess.TimeoutExpired as e:
  log=(e.stdout or b"").decode() if isinstance(e.stdout,bytes) else e.stdout or "";rc=124
 (OUT/(m+".log")).write_text(log)
 counts=re.findall(r"Ran (\d+) tests?",log)
 bad=re.findall(r"^(?:FAIL|ERROR): ([^\n]+)",log,re.M)
 return {"module":m,"returncode":rc,"seconds":round(time.monotonic()-start,2),"reported_test_count":int(counts[-1]) if counts else None,"failures":bad}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(run,m) for m in modules]
 for f in concurrent.futures.as_completed(futures):
  row=f.result();results.append(row)
  (OUT/"progress.json").write_text(json.dumps({"completed":len(results),"total_modules":len(modules),"results":sorted(results,key=lambda r:r["module"])},indent=2)+"\n")
  print(row["module"],row["returncode"],len(results),"/",len(modules),flush=True)
summary={"discovered_test_count":len(tests),"module_count":len(modules),"reported_test_count":sum(x["reported_test_count"] or 0 for x in results),"results":sorted(results,key=lambda x:x["module"]),"status":"PASS" if all(x["returncode"]==0 for x in results) else "FAIL"}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="results"}),flush=True)

