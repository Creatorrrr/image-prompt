"""Run one canonical maintenance step; logs contain no credential values."""
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
env=os.environ.copy();env['PHOTO_RUNTIME_STORE']=str(OUT/'runtime-store')
if (PRIMARY/'.env').exists() and not (ROOT/'.env').exists() and ROOT!=PRIMARY:
    (ROOT/'.env').symlink_to(PRIMARY/'.env')
stage=sys.argv[1]
scripts=ROOT/'skills/photo-prompt-image-generator/scripts'
assets=scripts.parent/'assets'
if stage in ('semantic','visual'):
    name='photo_prompt_semantic_index.json'if stage=='semantic'else'photo_prompt_visual_profile_index.json'
    meta=json.loads((assets/name).read_text())
    cmd=[str(PRIMARY/'.venv/bin/python'),str(scripts/('build_semantic_index.py'if stage=='semantic'else'build_visual_profile_index.py')),
         '--model',meta['embedding_model'],'--dimensions',str(meta['embedding_dimensions']),'--batch-size','1','--no-runtime-publication']
    if stage=='semantic':cmd.append('--progress')
elif stage=='validate':cmd=[str(PRIMARY/'.venv/bin/python'),str(scripts/'validate_photo_prompt_dictionary.py'),'--no-runtime-publication']
elif stage=='check':cmd=[str(PRIMARY/'.venv/bin/python'),str(scripts/'build_visual_profile_index.py'),'--check','--no-runtime-publication']
elif stage=='publish':cmd=[str(PRIMARY/'.venv/bin/python'),str(scripts/'publish_photo_runtime_snapshot.py')]
else:raise ValueError(stage)
n=1
while(OUT/f'{stage}-{n}.log').exists():n+=1
log=OUT/f'{stage}-{n}.log'
with log.open('w')as f:result=subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
record={'stage':stage,'exit_code':result.returncode,'log':str(log),'argv':cmd,'runtime_store':env['PHOTO_RUNTIME_STORE']}
(OUT/f'{stage}-{n}-receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False));raise SystemExit(result.returncode)
