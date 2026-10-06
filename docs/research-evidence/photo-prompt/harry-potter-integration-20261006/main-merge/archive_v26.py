"""Archive exact qualified main bytes without changing its sealed history."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path.cwd();OUT=ROOT/'docs/research-evidence/photo-prompt/harry-potter-integration-20261006/main-merge'
PIN=subprocess.check_output(['git','rev-parse','origin/main']).decode().strip()
TREE=subprocess.check_output(['git','rev-parse',PIN+'^{tree}']).decode().strip()
old=json.loads((ROOT/'docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006/V25-PARENT-SOURCE.json').read_text())
index={}
for record in subprocess.check_output(['git','ls-tree','-r','-z',PIN]).decode().split('\0'):
 if not record:continue
 head,path=record.split('\t');mode,kind,blob=head.split();index[path]=(mode,blob)
paths={r['path']:r for r in old['members']}
extra=['docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006/V25-PARENT-SOURCE.json','docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006/V26-SCENE-BUDGET-PROOF.json','skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v26.json','skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v26_pack.json']
extra += [p for p in index if p.startswith('docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006/v25-parent-source-files/')]
for name in extra:paths.setdefault(name,{})
archive_set={'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py','skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json'}
archive_set.update('skills/photo-prompt-image-generator/assets/'+n for n in json.loads((OUT/'MERGED-ADOPTION-MANIFEST.json').read_text())['source_files_changed'] if n not in ['photo_prompt_character_appearance_extension.json','photo_prompt_visual_obligations_appearance_relations.json'])
archive_set.update(['skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json','skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json'])
rows=[]
for name,prior in sorted(paths.items()):
 mode,blob=index[name]
 live=ROOT/name
 same_prior=prior.get('git_blob')==blob
 source=ROOT/prior['source_path'] if same_prior else live
 raw=source.read_bytes()
 raw_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if name in archive_set or raw_blob!=blob:
  raw=subprocess.check_output(['git','show',PIN+':'+name])
  source=OUT/'v26-parent-source-files'/name;source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(raw)
 rows.append({'path':name,'source_path':str(source.relative_to(ROOT)),'kind':'retained_parent_source' if source==live else 'archived_parent_source','mode':mode,'git_blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
assert all(hashlib.sha1(b'blob '+str(r['bytes']).encode()+b'\0'+(ROOT/r['source_path']).read_bytes()).hexdigest()==r['git_blob'] for r in rows)
manifest={'schema':'photo-v26-parent-source-manifest/v1','source_pin':PIN,'source_tree':TREE,'member_count':len(rows),'total_member_bytes':sum(r['bytes'] for r in rows),'archived_member_count':sum(r['kind']=='archived_parent_source' for r in rows),'members':rows}
path=OUT/'V26-PARENT-SOURCE.json';path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='members'}));print('manifest_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
