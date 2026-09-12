from pathlib import Path
import concurrent.futures,json,subprocess,sys,time,re
ROOT=Path.cwd();OUT=ROOT/"docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912";BASE=Path(json.loads((OUT/"head-baseline.json").read_text())["path"])
DEST=OUT/"head-comparison";DEST.mkdir(exist_ok=True)
previous=json.loads((DEST/"progress.json").read_text()) if (DEST/"progress.json").exists() else {"results":[]}
results={r["module"]:r for r in previous["results"]};running={}
def run(m):
 start=time.monotonic()
 try:
  p=subprocess.run([sys.executable,"-m","unittest",m,"-v"],cwd=BASE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
  log=p.stdout;rc=p.returncode
 except subprocess.TimeoutExpired as e:
  log=(e.stdout or b"").decode() if isinstance(e.stdout,bytes) else e.stdout or "";rc=124
 (DEST/(m+".log")).write_text(log)
 return {"module":m,"baseline_returncode":rc,"seconds":round(time.monotonic()-start,2),"baseline_failures":re.findall(r"^(?:FAIL|ERROR): ([^\n]+)",log,re.M)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 while True:
  path=OUT/"full-suite/progress.json"
  try:current=json.loads(path.read_text())
  except (FileNotFoundError,json.JSONDecodeError):time.sleep(2);continue
  failed={r["module"]:r for r in current["results"] if r["returncode"]}
  for m in failed:
   if m not in results and m not in running:
    if failed[m]["returncode"]==124:
     results[m]={"module":m,"baseline_returncode":None,"baseline_failures":[],"current_failures":failed[m]["failures"],"same_failure_names":False,"baseline_status":"not_replayed_full_module_timeout_requires_targeted_resume"}
    else:running[m]=pool.submit(run,m)
  for m,f in list(running.items()):
   if f.done():
    row=f.result();row["current_failures"]=failed[m]["failures"]
    row["same_failure_names"]=row["baseline_failures"]==row["current_failures"]
    results[m]=row;del running[m];print(m,row["same_failure_names"],flush=True)
  (DEST/"progress.json").write_text(json.dumps({"baseline_head":json.loads((OUT/"head-baseline.json").read_text())["head"],"results":list(results.values()),"running":list(running)},indent=2)+"\n")
  if (OUT/"full-suite/summary.json").exists() and not running and set(failed)<=set(results):break
  time.sleep(5)
(DEST/"summary.json").write_text(json.dumps({"results":list(results.values()),"all_failure_names_reproduced":all(r["same_failure_names"] for r in results.values())},indent=2)+"\n")
