"""CAS-check upstream inputs and copy only owned additive changes/index outputs."""
from pathlib import Path
import json
import hashlib
import sys

WORKTREE=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=Path('skills/photo-prompt-image-generator')
EVIDENCE=Path(__file__).resolve().parent
SNAP=json.loads((EVIDENCE/'INPUT-SNAPSHOT.json').read_text())
before={r['path']:r['sha256'] for r in SNAP['files']}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
for row in SNAP['files']:
    if row['path'].startswith('skills/') and sha(PRIMARY/row['path'])!=row['sha256']:
        raise RuntimeError('Upstream source changed; merge and rebuild first: '+row['path'])
test=Path('tests/test_photo_structure_maintenance.py')
if sha(PRIMARY/test)!=before[str(test)]:raise RuntimeError('Upstream registration test changed')
sys.path.insert(0,str(PRIMARY/REL/'scripts'))
from photo_runtime_sources import source_update
owned=[REL/'assets/photo_prompt_palette_applications_extension.json',
       REL/'assets/photo_prompt_visual_obligations_palette_applications.json',
       REL/'assets/photo_prompt_source_manifest.json',test,Path('tests/test_photo_palette_applications.py'),
       Path('docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_palette_applications_extension-20261006.json')]
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
    path=REL/'assets'/name;d=json.loads((WORKTREE/path).read_text())
    owned.extend([REL/'assets'/s['path'] for s in d['shards']]);owned.append(path)
copied=[]
with source_update(PRIMARY/REL):
    for rel in owned:
        source=WORKTREE/rel;target=PRIMARY/rel
        if target.exists() and str(rel) not in before and sha(target)!=sha(source):
            raise RuntimeError('Owned destination already has different data: '+str(rel))
        raw=source.read_bytes();target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        copied.append({'path':str(rel),'sha256':sha(target)})
report={'schema_version':'color-palette-safe-sync/v1','upstream_snapshot_unchanged':True,'copied':copied,
        'untouched_authored_sources':len([r for r in SNAP['files'] if r['path'].startswith('skills/') and r['path'] not in {str(x) for x in owned}]),
        'old_shards_removed':0,'commit':False,'push':False}
(EVIDENCE/'SYNC-REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'copied_files':len(copied),'untouched_inputs':report['untouched_authored_sources']},indent=2))
