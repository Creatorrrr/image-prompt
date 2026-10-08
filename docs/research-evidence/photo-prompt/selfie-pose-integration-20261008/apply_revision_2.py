"""Scoped second application with exact checks against the first receipt."""
import hashlib,json,shutil,sys,zipfile
from pathlib import Path
WT=Path(__file__).resolve().parents[4];PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=Path('docs/research-evidence/photo-prompt/selfie-pose-integration-20261008');OUT=PRIMARY/REL
SKILL=Path('skills/photo-prompt-image-generator');ASSETS=SKILL/'assets'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
old=json.loads((OUT/'primary-application.json').read_text())
owned_names=['photo_prompt_selfie_pose_extension.json','photo_prompt_visual_obligations_selfie_pose.json','photo_prompt_visual_obligations.json','photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']
owned={str(ASSETS/n)for n in owned_names}
baseline=json.loads((OUT/'primary-before.json').read_text())
for row in baseline['copied_live_files']:
    rel=row['path']
    if rel in owned or '_index_shards/'in rel:continue
    assert sha(PRIMARY/rel)==sha(WT/rel),('Concurrent source drift',rel)
for row in old['copied']:
    assert sha(PRIMARY/row['path'])==row['after_sha256'],('Concurrent change of applied artifact',row['path'])
paths=[ASSETS/n for n in owned_names]
for n in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
    paths += [ASSETS/s['path']for s in json.loads((WT/ASSETS/n).read_text())['shards']]
paths += [Path('tests/test_photo_selfie_pose_semantics.py'),Path('docs/research-evidence/photo-prompt/extension-maintenance/selfie_pose_reviewed_20261008.json')]
backup=OUT/'primary-owned-before-revision-2.zip';assert not backup.exists()
with zipfile.ZipFile(backup,'w',compression=zipfile.ZIP_DEFLATED)as z:
    for rel in paths:
        if(PRIMARY/rel).is_file():z.write(PRIMARY/rel,str(rel))
sys.path.insert(0,str(PRIMARY/SKILL/'scripts'))
from photo_runtime_sources import source_update,SnapshotPublisher
index_paths=[ASSETS/n for n in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']]
records=[]
with source_update(PRIMARY/SKILL):
    for rel in [r for r in paths if r not in index_paths]+index_paths:
        src=WT/rel;dst=PRIMARY/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        before=sha(dst)if dst.is_file()else None;shutil.copy2(src,dst)
        records.append({'path':str(rel),'before_sha256':before,'after_sha256':sha(dst)})
for name in ['maintenance-record.json','coverage-180.json','authored-receipt.json','capture-input-proof-boundaries.json','data-revision-2-rationale.json']:
    shutil.copy2(WT/REL/name,OUT/name)
(OUT/'primary-application-revision-2.json').write_text(json.dumps({'copied':records,'backup':str(backup),'prior_application_preserved':str(OUT/'primary-application.json')},ensure_ascii=False,indent=2)+'\n')
pointer=SnapshotPublisher(PRIMARY/SKILL).publish()
(OUT/'primary-runtime-publication-revision-2.json').write_text(json.dumps(pointer,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'copied_files':len(records),'publication':pointer},ensure_ascii=False))
