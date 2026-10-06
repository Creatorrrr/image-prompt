"""Run every discovered test file in isolated processes, three at a time."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import time

E=Path(__file__).resolve().parent
W=E.parents[3]
OUT=E/'full-regression';OUT.mkdir(exist_ok=True)
modules=sorted('.'.join(p.relative_to(W).with_suffix('').parts) for p in (W/'tests').rglob('test*.py'))
retry='--retry-failed' in sys.argv
previous=json.loads((E/'FULL-REGRESSION-RESULT.json').read_text()) if retry else None
if retry:
    modules=[r['module'] for r in previous['failed_modules']]
    (E/'FULL-REGRESSION-INITIAL.json').write_text(json.dumps(previous,indent=2)+'\n')
env=os.environ.copy();env['PHOTO_RUNTIME_STORE']='/tmp/color-palette-main-merge-20261007/runtime-store';env['GEMINI_API_KEY']='';env['GOOGLE_API_KEY']=''
def run(module):
    started=time.monotonic();log=OUT/(module+'.log')
    with log.open('w') as stream:
        try:result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',module.split('.')[-1]+'.py','-v'],cwd=W,env=env,stdout=stream,stderr=stream,timeout=1800);code=result.returncode
        except subprocess.TimeoutExpired:code=124
    text=log.read_text();counts=re.findall(r'Ran (\d+) tests?',text)
    failures=re.findall(r'FAILED \(([^)]+)\)',text)
    skipped=re.findall(r'skipped=(\d+)',text)
    row={'module':module,'returncode':code,'tests':int(counts[-1]) if counts else 0,'duration_seconds':round(time.monotonic()-started,3),'skipped':int(skipped[-1]) if skipped else 0,'failure_summary':failures[-1] if failures else None,'log':str(log.relative_to(W))}
    (OUT/(module+'.json')).write_text(json.dumps(row,indent=2)+'\n')
    return row
started=time.monotonic();rows=[]
with ThreadPoolExecutor(max_workers=3) as pool:
    jobs={pool.submit(run,m):m for m in modules}
    for future in as_completed(jobs):
        row=future.result();rows.append(row)
        progress={'completed_modules':len(rows),'total_modules':len(modules),'tests':sum(r['tests'] for r in rows),'failed_modules':[r for r in rows if r['returncode']!=0],'latest':row}
        (E/'FULL-REGRESSION-PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
        print(json.dumps({k:v for k,v in progress.items() if k!='failed_modules'},ensure_ascii=False),flush=True)
if retry:
    initial={r['module']:r for r in previous['module_results']}
    initial.update({r['module']:r for r in rows});rows=list(initial.values());modules=previous['modules_collected']
report={'schema':'palette-main-merge-full-regression/v1','modules_collected':modules,'module_results':sorted(rows,key=lambda r:r['module']),'module_count':len(modules),'modules_completed':len(rows),'tests':sum(r['tests'] for r in rows),'skipped':sum(r['skipped'] for r in rows),'failed_modules':[r for r in rows if r['returncode']!=0],'status':'PASS' if all(r['returncode']==0 for r in rows) else 'FAIL','duration_seconds':round(time.monotonic()-started,3)+(previous['duration_seconds'] if retry else 0),'process_isolation':True,'workers':3,'external_api_credentials_disabled':True,'initial_sequential_discovery':'Interrupted before completion; original log retained. Every collected test file is rerun here.','retry_failed_modules':retry}
(E/'FULL-REGRESSION-RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['module_results','modules_collected','failed_modules']},ensure_ascii=False),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
