"""Compare changed preparation CLIs in private source, without doing work."""
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt');HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import checks
import four_patch
from history_state import new

private=Path(sys.argv[1]);cases={}
for label in ('control','combined'):
    project=private/label;skill=project/'skills/photo-prompt-image-generator';rows={}
    for module,part in [('prepare_photo_run','precore'),('prepare_retry_context','scripts')]:
        path=skill/part/(module+'.py')
        cmd=['/usr/bin/sandbox-exec','-p',four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))',
            str(ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'),'-I','-B','-c',
            "import runpy,sys;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",str(path.parent),str(path),'--help']
        child=subprocess.run(cmd,cwd=project,env=checks.environment(),capture_output=True,text=True,timeout=30)
        assert child.returncode==0 and 'usage:' in child.stdout.lower(),child.stderr
        normalized=child.stdout.replace(str(project.resolve()),'<project>').replace(str(project),'<project>')
        rows[module]={'exit_code':child.returncode,'stdout':child.stdout,'stderr':child.stderr,
            'normalized_stdout_sha256':hashlib.sha256(normalized.encode()).hexdigest()}
    cases[label]=rows
assert {m:r['normalized_stdout_sha256'] for m,r in cases['control'].items()}=={m:r['normalized_stdout_sha256'] for m,r in cases['combined'].items()}
new(HERE/'CLI-HELP.json',{'status':'PASS','cases':cases,'scope':'--help only; no freeze/retry state transaction, model inference or API call',
    'normalized_help_outputs_equal':True,'Gemini_calls':0,'CURRENT_writes':0})
print('2 private CLI help outputs equal',flush=True)
