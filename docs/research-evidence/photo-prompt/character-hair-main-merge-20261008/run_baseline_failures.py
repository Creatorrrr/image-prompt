"""Replay known failure modules on the untouched fetched main checkout."""
from pathlib import Path
import concurrent.futures,json,re,subprocess,sys,time
HERE=Path(__file__).resolve().parent
BASE=Path('/Users/chasoik/.codex/worktrees/character-hair-merge-baseline/image-prompt')
LOGS=HERE/'baseline-test-modules';LOGS.mkdir(exist_ok=True)
modules=json.loads((HERE/'baseline_modules.json').read_text());started=time.time();results=[]
def run(name):
    log=LOGS/(name+'.log')
    with log.open('wb') as stream:p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',name+'.py','-v'],cwd=BASE,stdout=stream,stderr=subprocess.STDOUT)
    text=log.read_text(errors='replace');counts=re.findall(r'^Ran (\d+) tests? in ([\d.]+)s$',text,re.M);failures=re.findall(r'^(?:FAIL|ERROR): (.+)$',text,re.M)
    return {'module':name,'exit_code':p.returncode,'tests':int(counts[-1][0]) if counts else 0,'failures':failures,'log':str(log.relative_to(HERE))}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for row in pool.map(run,modules):
        results.append(row);summary={'status':'running','baseline_commit':'791bd1ca3128627b9aefa22e0ab64041fe9c369f','completed_modules':len(results),'elapsed_seconds':round(time.time()-started,2),'results':results};(HERE/'BASELINE-FAILURES.json').write_text(json.dumps(summary,indent=2)+'\n')
summary['status']='complete';(HERE/'BASELINE-FAILURES.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='results'}))
