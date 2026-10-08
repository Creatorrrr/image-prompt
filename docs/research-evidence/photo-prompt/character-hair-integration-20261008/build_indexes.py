"""Invoke the maintained builders; credentials stay in process environment."""
from pathlib import Path
import os,runpy,sys

ROOT=Path(__file__).resolve().parents[4]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
# The isolated worktree deliberately has no copied credential file.
env_path=Path('/Users/chasoik/Projects/image-prompt/.env')
if env_path.is_file():
    for raw in env_path.read_text().splitlines():
        line=raw.strip()
        if not line or line.startswith('#') or '=' not in line:continue
        key,value=line.split('=',1);key=key.strip()
        if key in {'GEMINI_API_KEY','GOOGLE_API_KEY'} and key not in os.environ:
            value=value.strip().strip('"\'')
            if value:os.environ[key]=value
kind=sys.argv[1]
name={'candidate':'build_semantic_index.py','profile':'build_visual_profile_index.py'}[kind]
sys.path.insert(0,str(SCRIPTS))
sys.argv=[str(SCRIPTS/name),'--batch-size','1','--request-interval','0.8','--no-runtime-publication']
if kind=='candidate':sys.argv.append('--progress')
runpy.run_path(str(SCRIPTS/name),run_name='__main__')
