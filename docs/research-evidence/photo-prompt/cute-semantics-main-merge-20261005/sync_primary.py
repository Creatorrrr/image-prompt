"""Fast-forward primary main while preserving unrelated dirty authored sources.

Run only after the reviewed integration has been pushed. A verified backup is
created before clearing only the already-published owned paths for fast-forward.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args,cwd=PRIMARY):return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
record=json.loads((HERE/'PRIMARY-OWNERSHIP.json').read_text())
owned=record['owned_files']
changed=[name for name,digest in owned.items() if not (PRIMARY/name).is_file() or sha(PRIMARY/name)!=digest]
assert not changed, f'Concurrent changes on owned paths need reconciliation: {changed}'
assert git('branch','--show-current')=='main'
target=git('rev-parse','HEAD',cwd=ROOT)
assert git('ls-remote','origin','refs/heads/main').split()[0]==target
indexes=['skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json',
         'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json']
backup=HERE/'PRIMARY-OWNED-BEFORE-SYNC.zip'
selected=sorted(set(owned)|set(indexes))
before={name:sha(PRIMARY/name) for name in selected}
unrelated={name:sha(PRIMARY/name) for name in record['unrelated_authored_files']}
with zipfile.ZipFile(backup,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as saved:
    for name in selected:saved.write(PRIMARY/name,name)
with zipfile.ZipFile(backup) as saved:
    assert all(hashlib.sha256(saved.read(name)).hexdigest()==digest for name,digest in before.items())
tracked=set(git('ls-files','--',*selected).splitlines())
subprocess.run(['git','restore','--source=HEAD','--worktree','--',*sorted(tracked)],cwd=PRIMARY,check=True)
for name in selected:
    if name not in tracked:(PRIMARY/name).unlink()
subprocess.run(['git','fetch','origin','main'],cwd=PRIMARY,check=True)
assert git('rev-parse','origin/main')==target
subprocess.run(['git','merge','--ff-only','origin/main'],cwd=PRIMARY,check=True,
               stdout=subprocess.DEVNULL)
assert git('rev-parse','HEAD')==target
sys.path.insert(0,str(PRIMARY/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
assets=PRIMARY/'skills/photo-prompt-image-generator/assets'
data=g.load_json(assets/'photo_prompt_tags.json')
registry=g.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json')
with zipfile.ZipFile(backup) as saved:
    original=json.loads(saved.read(indexes[0]))
    assert original['dictionary_hash']==g.dictionary_hash(data), 'Working authored DATA changed; rebuild rather than restoring stale vectors.'
    for name in indexes:(PRIMARY/name).write_bytes(saved.read(name))
g.validate_semantic_index_metadata(g.load_semantic_index_payload(assets/'photo_prompt_semantic_index.json'),data)
g.load_visual_profile_index(assets/'photo_prompt_visual_profile_index.json',registry)
assert all(sha(PRIMARY/name)==digest for name,digest in unrelated.items())
result=dict(primary_head=target,origin_main=git('rev-parse','origin/main'),
    primary_main_fast_forwarded=True,owned_source_changes_already_published=True,
    unrelated_authored_files_preserved=len(unrelated),
    working_indexes_valid_for_retained_dirty_authored_DATA=True,
    backup_sha256=sha(backup),backup=str(backup),
    canonical_published_DATA_verified_in=str(ROOT))
(HERE/'PRIMARY-SYNC-VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print('Primary main synchronized; unrelated authored DATA unchanged; working indexes valid.')
