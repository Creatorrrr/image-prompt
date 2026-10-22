from pathlib import Path
import sys,os,subprocess,json
root=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')
sys.path.insert(0,str(root/'scripts'))
from photo_installed_h_f2 import release,runtime_python
store=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed')
gid='fc8ae54d09d76258d0e77b8ab52037869fc9362fcb8331d847b8ea438f667196'
args=sys.argv[1:]
if not args or args[0] not in {'review-shape','review-audit'}:raise SystemExit('review-only wrapper')
native,manifest,_=release(store,gid,full=True)
env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONNOUSERSITE='1')
env.pop('PYTHONPATH',None)
for key in ['GEMINI_API_KEY','GOOGLE_API_KEY','ANTHROPIC_API_KEY','OPENAI_API_KEY']:env.pop(key,None)
launcher="import gc,sys,runpy;from pathlib import Path;gc.disable();entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));runpy.run_path(entry,run_name='__main__')"
raise SystemExit(subprocess.run([str(runtime_python(root,manifest)),'-I','-c',launcher,str(native/'scripts/photo_workflow.py'),*args],env=env).returncode)
