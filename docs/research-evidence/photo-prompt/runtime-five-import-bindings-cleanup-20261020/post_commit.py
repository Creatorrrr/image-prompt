"""Verify the exact local commit and protect original work after index changes."""
from pathlib import Path
import json
import subprocess
import run
from history_state import new

t=run.state.read(run.E/'TARGETS.json');plan=run.state.read(run.E/'STAGED-CHECK.json')
head=run.state.git(run.ROOT,'rev-parse','HEAD').decode().strip()
assert run.state.git(run.ROOT,'rev-parse','HEAD^').decode().strip()==t['base_head']
actual=set(run.state.git(run.ROOT,'diff-tree','--no-commit-id','--name-only','-r','-z',head).decode().split('\0'))-{''}
assert actual==set(plan['allowed_paths'])
assert all(run.digest(run.state.git(run.ROOT,'show',head+':'+p))==h for p,h in t['index'].items())
assert not run.state.git(run.ROOT,'diff','--cached','--name-only')
private=Path(run.state.read(run.E/'PRIVATE-PROJECTS.json')['private_parent'])
run.verify(private/'POST-COMMIT-PRESERVATION.json',full=True,committed=True)
new(private/'POST-COMMIT.json',{'status':'PASS','commit':head,'parent':t['base_head'],'branch':run.state.git(run.ROOT,'branch','--show-current').decode().strip(),
    'committed_paths':len(actual),'source_paths':sorted(run.TARGETS),'only_reviewed_paths_committed':True,'staging_empty':True,'original_dirty_work_preserved':True,
    'CURRENT_count':len(run.baseline()['pointers']),'CURRENT_writes':0,'Gemini_calls':0,'push':False})
print(json.dumps(run.state.read(private/'POST-COMMIT.json'),ensure_ascii=False,indent=2))
