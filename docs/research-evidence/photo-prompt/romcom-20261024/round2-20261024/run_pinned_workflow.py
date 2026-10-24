"""Verified explicit launcher for all managed commands; does not alter the shared default."""
from pathlib import Path
import os,sys,subprocess,json
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from photo_installed_h_f2 import release,runtime_python,option
STORE=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed')
GEN='22aa903c2257bc2b3da9dfe9361e54d186c2d5569733e63ecd30a9e62ffe46fb'
native,manifest,native_manifest=release(STORE,GEN)
args=sys.argv[1:]
if not args:raise SystemExit('managed command required')
run=option(args,'--run')
if run and (Path(run)/'workflow.json').is_file():
 state=json.loads((Path(run)/'workflow.json').read_text());bound=state.get('h_f2_binding')
 if bound and (bound['generation_id']!=GEN or Path(bound['store']).resolve()!=STORE.resolve()):raise SystemExit('existing run bound to a different release')
if args[0] in {'retrieve','resume'}:
 if option(args,'--generation-id') not in {None,GEN}:raise SystemExit('wrong explicit generation')
 if option(args,'--runtime-store') not in {None,str(STORE)}:raise SystemExit('wrong explicit store')
 if option(args,'--generation-id') is None:args+=['--generation-id',GEN,'--runtime-store',str(STORE)]
 if option(args,'--retrieval-policy') is None:args+=['--retrieval-policy','h-f2']
 if option(args,'--local-embedding-skill') is None:args+=['--local-embedding-skill',str(S)]
env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONNOUSERSITE='1')
for k in ['PYTHONPATH','GEMINI_API_KEY','GOOGLE_API_KEY','ANTHROPIC_API_KEY']+([] if args[0]=='render-api' else ['OPENAI_API_KEY']):env.pop(k,None)
launcher="import gc,sys,runpy;gc.disable();from pathlib import Path;entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));runpy.run_path(entry,run_name='__main__')"
raise SystemExit(subprocess.run([str(runtime_python(S,manifest)),'-I','-c',launcher,str(native/'scripts/photo_workflow.py'),*args],env=env).returncode)
