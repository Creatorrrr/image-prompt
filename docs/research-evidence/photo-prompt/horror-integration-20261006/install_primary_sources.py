"""Install only authored additions and their derived indexes; preserve the dirty checkout."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

EVIDENCE = Path(__file__).resolve().parent
WORKTREE = EVIDENCE.parents[3]
PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
REL = Path('skills/photo-prompt-image-generator')
sys.path.insert(0,str(PRIMARY/REL/'scripts'))
from photo_runtime_sources import source_update

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

snapshot = json.loads((EVIDENCE/'LATEST-SOURCE-SNAPSHOT.json').read_text())
drift = [row['path'] for row in snapshot['files'] if not (PRIMARY/row['path']).is_file() or sha(PRIMARY/row['path'])!=row['sha256']]
if drift:
    raise RuntimeError('Reconcile current primary changes before installation: '+repr(drift))

new_files = [REL/'assets/photo_prompt_horror_extension.json', REL/'assets/photo_prompt_visual_obligations_horror.json',Path('tests/test_photo_horror_visual_semantics.py')]
for relative in new_files:
    if (PRIMARY/relative).exists():
        raise RuntimeError('New file appeared during preflight: '+str(relative))

manifest_path = PRIMARY/REL/'assets/photo_prompt_source_manifest.json'
manifest = json.loads(manifest_path.read_text())
authored = json.loads((WORKTREE/REL/'assets/photo_prompt_source_manifest.json').read_text())
for filename in ['photo_prompt_horror_extension.json','photo_prompt_visual_obligations_horror.json']:
    row = next(r for r in authored['sources'] if r['file']==filename)
    if any(r['file']==filename for r in manifest['sources']):
        raise RuntimeError('Source is already registered: '+filename)
    if any(r['kind']==row['kind'] and r['load_order']==row['load_order'] for r in manifest['sources']):
        raise RuntimeError('Registration order now conflicts: '+filename)
    manifest['sources'].append(row)
if manifest!=authored:
    raise RuntimeError('Primary registration differs; regenerate indexes after reconciliation')

derived = []
for filename in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
    relative = REL/'assets'/filename
    payload = json.loads((WORKTREE/relative).read_text())
    derived.extend(REL/'assets'/row['path'] for row in payload.get('shards',[]))
    derived.append(relative)

records = []
with source_update(PRIMARY/REL):
    for relative in [*new_files,*derived]:
        source,target=WORKTREE/relative,PRIMARY/relative
        before=sha(target) if target.is_file() else None
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_name(target.name+'.horror-install.tmp')
        shutil.copy2(source,temporary)
        temporary.replace(target)
        if sha(source)!=sha(target):
            raise RuntimeError('Copy hash mismatch: '+str(relative))
        records.append({'path':str(target),'before_sha256':before,'after_sha256':sha(target)})
    before=sha(manifest_path)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    records.append({'path':str(manifest_path),'before_sha256':before,'after_sha256':sha(manifest_path)})

protected=[]
changed={str(Path(r['path']).relative_to(PRIMARY)) for r in records}
for row in snapshot['files']:
    if row['path'] not in changed and sha(PRIMARY/row['path'])!=row['sha256']:
        protected.append(row['path'])
if protected:
    raise RuntimeError('Unrelated file changed during installation: '+repr(protected))
(EVIDENCE/'PRIMARY-INSTALLATION.json').write_text(json.dumps({'primary':str(PRIMARY),'worktree':str(WORKTREE),'modified_files':records,'unrelated_snapshot_files_preserved':len(snapshot['files'])-sum(r['path'] in changed for r in snapshot['files']),'unrelated_drift':protected,'old_shard_generations':'preserved','committed':False,'pushed':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'installed_files':len(records),'unrelated_drift':protected}))
