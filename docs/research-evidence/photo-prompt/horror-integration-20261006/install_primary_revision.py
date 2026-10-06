"""Replace only our installed sources/test and current derived outputs after repair."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
EVIDENCE=Path(__file__).resolve().parent
WORKTREE=EVIDENCE.parents[3]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=Path('skills/photo-prompt-image-generator')
sys.path.insert(0,str(PRIMARY/REL/'scripts'))
from photo_runtime_sources import source_update
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
previous=json.loads((EVIDENCE/'PRIMARY-INSTALLATION.json').read_text())
for row in previous['modified_files']:
 if not Path(row['path']).is_file() or sha(Path(row['path']))!=row['after_sha256']:
  raise RuntimeError('Concurrent modification requires reconciliation: '+row['path'])
modified={str(Path(r['path']).relative_to(PRIMARY)) for r in previous['modified_files']}
snapshot=json.loads((EVIDENCE/'LATEST-SOURCE-SNAPSHOT.json').read_text())
for row in snapshot['files']:
 if row['path'] not in modified and sha(PRIMARY/row['path'])!=row['sha256']:
  raise RuntimeError('Unrelated primary drift: '+row['path'])
files=[REL/'assets/photo_prompt_horror_extension.json',REL/'assets/photo_prompt_visual_obligations_horror.json',Path('tests/test_photo_horror_visual_semantics.py')]
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
 relative=REL/'assets'/name
 d=json.loads((WORKTREE/relative).read_text())
 files.extend(REL/'assets'/r['path'] for r in d.get('shards',[]))
 files.append(relative)
records=[]
with source_update(PRIMARY/REL):
 for relative in files:
  source,target=WORKTREE/relative,PRIMARY/relative
  before=sha(target) if target.is_file() else None
  target.parent.mkdir(parents=True,exist_ok=True)
  temp=target.with_name(target.name+'.horror-revision.tmp')
  shutil.copy2(source,temp);temp.replace(target)
  if sha(source)!=sha(target):raise RuntimeError('Copy mismatch '+str(relative))
  records.append({'path':str(target),'before_sha256':before,'after_sha256':sha(target)})
save={'modified_files':records,'source_manifest_sha256':sha(PRIMARY/REL/'assets/photo_prompt_source_manifest.json'),'previous_installation_preserved':True,'old_shard_generations':'preserved','committed':False,'pushed':False}
(EVIDENCE/'PRIMARY-INSTALLATION-FINAL.json').write_text(json.dumps(save,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'installed_files':len(records),'source_manifest':'unchanged from registered addition'}))
