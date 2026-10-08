"""Copy only verified selfie sources and required index manifests/shards."""
from __future__ import annotations
import hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path
WT=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=Path('docs/research-evidence/photo-prompt/selfie-pose-integration-20261008')
OUT=PRIMARY/REL;OUT.mkdir(parents=True,exist_ok=True)
SKILL=Path('skills/photo-prompt-image-generator');ASSETS=SKILL/'assets'
baseline=json.loads((OUT/'primary-before.json').read_text())
before={r['path']:r['sha256']for r in baseline['copied_live_files']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_names=['photo_prompt_selfie_pose_extension.json','photo_prompt_visual_obligations_selfie_pose.json','photo_prompt_visual_obligations.json','photo_prompt_source_manifest.json']
index_names=['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']
owned={str(ASSETS/n)for n in source_names+index_names}
drift=[]
for rel in before:
    if rel in owned or '_index_shards/'in rel:continue
    p=PRIMARY/rel;w=WT/rel
    if not p.is_file()or not w.is_file()or sha(p)!=sha(w):drift.append(rel)
assert not drift,('Latest primary sources changed; reconcile before applying',drift)
for n in source_names:
    rel=str(ASSETS/n);p=PRIMARY/rel
    if rel in before:assert sha(p)==before[rel],('Concurrent mutation of owned source',rel)
    else:assert not p.exists(),('New source already exists',rel)
copy_rel=[ASSETS/n for n in source_names+index_names]
for n in index_names:
    meta=json.loads((WT/ASSETS/n).read_text())
    copy_rel += [ASSETS/s['path']for s in meta.get('shards',[])]
copy_rel += [Path('tests/test_photo_selfie_pose_semantics.py'),Path('docs/research-evidence/photo-prompt/extension-maintenance/selfie_pose_reviewed_20261008.json')]
backup=OUT/'primary-owned-before.zip'
assert not backup.exists(),'Application already recorded; do not replace its recovery evidence.'
with zipfile.ZipFile(backup,'w',compression=zipfile.ZIP_DEFLATED)as z:
    for rel in copy_rel:
        if(PRIMARY/rel).is_file():z.write(PRIMARY/rel,str(rel))
records=[]
sys.path.insert(0,str(PRIMARY/SKILL/'scripts'))
from photo_runtime_sources import source_update,SnapshotPublisher
with source_update(PRIMARY/SKILL):
    # Publish shards before switching their manifests; keep old shards intact.
    ordered=[r for r in copy_rel if r not in [ASSETS/n for n in index_names]]+[ASSETS/n for n in index_names]
    for rel in ordered:
        src=WT/rel;dst=PRIMARY/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        old=sha(dst)if dst.is_file()else None;shutil.copy2(src,dst)
        records.append({'path':str(rel),'before_sha256':old,'after_sha256':sha(dst)})
write_receipt={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=PRIMARY).decode().strip(),'copied':records,'backup':str(backup),'protected_source_drift':drift,'scope':'Reviewed selfie source/profile/registration, required generated index artifacts, new semantic tests and canonical maintenance record only.'}
(OUT/'primary-application.json').write_text(json.dumps(write_receipt,ensure_ascii=False,indent=2)+'\n')
pointer=SnapshotPublisher(PRIMARY/SKILL).publish()
(OUT/'primary-runtime-publication.json').write_text(json.dumps(pointer,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'copied_files':len(records),'publication':pointer},ensure_ascii=False,indent=2))
