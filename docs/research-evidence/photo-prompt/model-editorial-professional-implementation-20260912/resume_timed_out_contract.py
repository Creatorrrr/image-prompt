"""Continue unfinished/failed methods only; preserve the initial timeout record."""
from pathlib import Path
import json,re,subprocess,sys,concurrent.futures,time
ROOT=Path.cwd();OUT=ROOT/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912';m=sys.argv[1] if len(sys.argv)>1 else 'tests.test_photo_prompt_contract_v2';DEST=OUT/('timeout-resume' if m=='tests.test_photo_prompt_contract_v2' else 'timeout-resume-'+m.split('.')[-1]);DEST.mkdir(exist_ok=True)
partial=(OUT/'full-suite'/f'{m}.log').read_text();passed=set(re.findall(r'^\w+ \((tests\.[^)]+)\) \.\.\. (?:ok|skipped[^\n]*)$',partial,re.M));all_ids=[i for i in json.loads((OUT/'full-suite/discovery.json').read_text())['test_ids'] if i.startswith(m+'.')];remaining=[i for i in all_ids if i not in passed];base=Path(json.loads((OUT/'head-baseline.json').read_text())['path'])
plan={'module':m,'original_timeout_seconds':900,'completed_pass_or_skip_count':len(passed),'completed_pass_or_skip_ids':sorted(passed),'target_count':len(remaining),'target_ids':remaining,'expected_total_methods':len(all_ids),'reason':'Remaining methods plus any prior failed methods run with full failure output; already passed/skipped methods are not repeated.'};(DEST/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('resume',len(remaining),'of',len(all_ids),flush=True)
def run(label,cwd):
 start=time.monotonic()
 try:
  p=subprocess.run([sys.executable,'-m','unittest',*remaining,'-v'],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900);log=p.stdout;rc=p.returncode
 except subprocess.TimeoutExpired as e:log=e.stdout.decode() if isinstance(e.stdout,bytes) else e.stdout or '';rc=124
 (DEST/f'{label}.log').write_text(log)
 counts=re.findall(r'Ran (\d+) tests?',log);r={'label':label,'returncode':rc,'seconds':round(time.monotonic()-start,2),'reported_test_count':int(counts[-1]) if counts else None,'failures':re.findall(r'^(?:FAIL|ERROR): ([^\n]+)',log,re.M)}
 (DEST/f'{label}.json').write_text(json.dumps(r,indent=2)+'\n');print(label,r['returncode'],r['reported_test_count'],flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 f1=pool.submit(run,'current',ROOT);f2=pool.submit(run,'head',base);current=f1.result();head=f2.result()
result={'module':m,'all_module_methods_finished':current['reported_test_count']==len(remaining) and current['returncode'] in (0,1),'total_unique_methods_completed':len(passed)+(current['reported_test_count'] or 0),'current':current,'head':head,'baseline_returncode':head['returncode'],'baseline_failures':head['failures'],'current_failures':current['failures'],'same_failure_names':head['failures']==current['failures'],'replayed_targeted_after_timeout':True,'original_timeout_preserved':True}
(DEST/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['current','head','baseline_failures','current_failures']},indent=2))
