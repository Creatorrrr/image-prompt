"""Attempt every discovered unittest module in bounded independent processes."""
import collections,concurrent.futures,hashlib,json,re,subprocess,sys,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent/'full-suite-modules'
OUT.mkdir(exist_ok=False);sys.path.insert(0,str(ROOT))
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'));ids=[]
def flatten(item):
    if isinstance(item,unittest.TestSuite):
        for child in item:flatten(child)
    else:ids.append(item.id())
flatten(suite)
(OUT/'discovered-cases.json').write_text(json.dumps(ids,indent=2)+'\n')
counts=collections.Counter(x.split('.')[0]for x in ids)
modules=sorted(counts,key=lambda x:(-counts[x],x))
def run(name):
    start=time.monotonic();log=OUT/(name+'.log')
    with log.open('wb')as stream:
        result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',name+'.py','-v'],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    body=log.read_text(errors='replace');matches=re.findall(r'Ran (\d+) tests? in',body)
    return {'module':name,'exit_code':result.returncode,'seconds':round(time.monotonic()-start,3),'expected_discovered_cases':counts[name],'reported_cases':int(matches[-1])if matches else None,'failures':re.findall(r'^FAIL: (.+)$',body,re.M),'errors':re.findall(r'^ERROR: (.+)$',body,re.M),'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
records=[];start=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    for future in concurrent.futures.as_completed([pool.submit(run,m)for m in modules]):
        row=future.result();records.append(row)
        with(OUT/'completed.ndjson').open('a')as f:f.write(json.dumps(row)+'\n')
        print(json.dumps({'completed':len(records),'total_modules':len(modules),'module':row['module'],'exit_code':row['exit_code'],'cases':row['reported_cases']}),flush=True)
report={'schema_version':'photo-full-discovery-module-run/v1','workers':4,'seconds':round(time.monotonic()-start,3),'discovered_cases':len(ids),'modules':len(modules),'reported_cases':sum(r['reported_cases']or 0 for r in records),'passed_modules':sum(r['exit_code']==0 for r in records),'failed_modules':sum(r['exit_code']!=0 for r in records),'all_modules_attempted':len(records)==len(modules),'all_cases_executed':all(r['expected_discovered_cases']==r['reported_cases']for r in records),'proof_scope':'Every discovery module independently attempted with unchanged test code. Class setup errors can prevent discovered cases from running. This is module-isolated execution, not one-process ordering validation. The initial serial prefix is preserved separately.','records':sorted(records,key=lambda r:r['module'])}
(OUT/'SUMMARY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='records'}),flush=True)
sys.exit(0 if report['failed_modules']==0 and report['all_cases_executed']else 1)
