from pathlib import Path
import json,subprocess,sys,re,time
out=Path.cwd()/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912';base=Path(json.loads((out/'head-baseline.json').read_text())['path']);m='tests.test_photo_suggestive_editorial_visual_semantics'
p=subprocess.run([sys.executable,'-m','unittest',m,'-v'],cwd=base,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
log=p.stdout;(out/'head-comparison'/f'{m}.complete-fixture.log').write_text(log)
current=next(r for r in json.loads((out/'full-suite/progress.json').read_text())['results'] if r['module']==m)
failures=re.findall(r'^(?:FAIL|ERROR): ([^\n]+)',log,re.M)
row={'module':m,'baseline_returncode':p.returncode,'baseline_failures':failures,'current_failures':current['failures'],'same_failure_names':failures==current['failures'],'complete_fixture_rerun':True,'reason':'Restored omitted tracked HEAD docs and fixture artifacts; preliminary incomplete-copy run remains in logs.'}
(out/'head-comparison/complete-fixture-result.json').write_text(json.dumps(row,indent=2)+'\n');print(row['same_failure_names'])
