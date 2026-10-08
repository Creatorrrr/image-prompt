"""Discover every unittest module with isolated Python processes (four workers)."""
import concurrent.futures,json,re,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
LOGS=HERE/'full-test-modules';LOGS.mkdir(exist_ok=True)
paths=sorted((ROOT/'tests').glob('test_*.py'))
started=time.time()
def run(path):
    log=LOGS/(path.stem+'.log')
    with log.open('wb') as stream:
        result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',path.name,'-v'],
                              cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    text=log.read_text(errors='replace')
    counts=re.findall(r'^Ran (\d+) tests? in ([\d.]+)s$',text,re.M)
    failures=re.findall(r'^(?:FAIL|ERROR): (.+)$',text,re.M)
    return {'module':path.stem,'exit_code':result.returncode,'tests':int(counts[-1][0]) if counts else 0,
            'seconds':float(counts[-1][1]) if counts else None,'failures':failures,'log':str(log.relative_to(ROOT))}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures=[pool.submit(run,path) for path in paths]
    for future in concurrent.futures.as_completed(futures):
        row=future.result();results.append(row)
        summary={'status':'running','module_count':len(paths),'completed_modules':len(results),
                 'completed_tests':sum(r['tests'] for r in results),'failed_modules':sum(r['exit_code']!=0 for r in results),
                 'elapsed_seconds':round(time.time()-started,2),'results':sorted(results,key=lambda r:r['module'])}
        (HERE/'FULL-TEST-DISCOVERY.json').write_text(json.dumps(summary,indent=2)+'\n')
        if len(results)%20==0 or row['exit_code']!=0:
            print(json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)
summary['status']='passed' if not summary['failed_modules'] else 'failed'
(HERE/'FULL-TEST-DISCOVERY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)
raise SystemExit(bool(summary['failed_modules']))
