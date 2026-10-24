import subprocess,sys,json
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');B=R/'docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/b';run=R/'generated/photo-runs/marine-literature-retest-20261024-b-v5';wrapper=R/'docs/research-evidence/photo-prompt/marine-literature-20261024/integration-evidence/run_managed_scheduled.py';py=R/'.venv/bin/python'
steps=[('runtime-audit-result.json',['prepare-render','--run',str(run),'--parameters',str(B/'transport.json'),'--lane','native']),('native-plan-result.json',['native-plan','--run',str(run)]),('native-started-result.json',['native-started','--run',str(run)])]
for name,args in steps:
 with (B/name).open('w') as out:
  p=subprocess.run([str(py),str(wrapper),*args],cwd=R,stdout=out,text=True)
 if p.returncode:raise SystemExit(p.returncode)
 v=json.loads((B/name).read_text())
 print(json.dumps({'step':args[0],'status':v.get('status'),'phase':v.get('phase'),'operation_id':v.get('operation_id')}),flush=True)
 if v.get('status') not in ['pass']:raise SystemExit(2)
print(json.dumps({'ready_for_exact_native_tool_call':True,'started_file':str(B/'native-started-result.json')}),flush=True)
