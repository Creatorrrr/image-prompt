"""Deep-validate concurrent-source indexes before publishing their manifests."""
from pathlib import Path
import hashlib,json,os,shutil,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
ASSETS=SKILL/'assets';STAGE=OUT/'primary-index-staging'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from photo_runtime_sources import source_update,capture_sources
from photo_source_manifest import SourceInventory
from validate_photo_prompt_dictionary import validate_source_corpus

before,_=capture_sources(SKILL)
inv=SourceInventory.load(ASSETS)
data=pg.load_json(ASSETS/'photo_prompt_tags.json',inventory=inv)
registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json',inventory=inv)
semantic=pg.load_semantic_index_payload(STAGE/'photo_prompt_semantic_index.json')
pg.validate_semantic_index_metadata(semantic,data)
assert set(semantic['entries'])=={key for key,*_ in pg.iter_semantic_entries(data)}
visual=pg.load_visual_profile_index(STAGE/'photo_prompt_visual_profile_index.json',registry)
assert set(visual['entries'])=={p['id'] for p in registry['profiles']}
errors=validate_source_corpus(SKILL,data,inv)
assert not errors,errors
members=[]
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
 manifest=json.loads((STAGE/name).read_text())
 for shard in manifest['shards']:
  path=STAGE/shard['path'];raw=path.read_bytes()
  assert hashlib.sha256(raw).hexdigest()==shard['sha256']
  dest=ASSETS/shard['path']
  if dest.exists():assert dest.read_bytes()==raw,'Do not overwrite a different existing shard.'
  members.append((path,dest,raw))
with source_update(SKILL):
 current,_=capture_sources(SKILL)
 assert current==before,'Concurrent source/index changed; retain staging and revalidate.'
 for source,dest,raw in members:
  dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   tmp=dest.with_name(dest.name+'.spring-tmp');tmp.write_bytes(raw);os.replace(tmp,dest)
 for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
  old=OUT/'index-before-primary'/name;old.parent.mkdir(parents=True,exist_ok=True)
  assert not old.exists(),'Preserve original index manifest evidence.'
  shutil.copy2(ASSETS/name,old)
  tmp=ASSETS/(name+'.spring-tmp');tmp.write_bytes((STAGE/name).read_bytes());os.replace(tmp,ASSETS/name)
receipt={'schema_version':'spring-staged-index-install/v1','status':'PASS',
 'semantic_entries':len(semantic['entries']),'visual_profiles':len(visual['entries']),
 'manifest_rows':len(inv.rows),'source_before':before,
 'dictionary_hash':pg.dictionary_hash(data),'registry_sha256':pg.visual_profile_registry_sha256(registry),
 'old_shards_preserved':True,'installed_shards':len(members),'runtime_publication':'not_yet_published'}
(OUT/'PRIMARY-INDEX-INSTALL.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','semantic_entries','visual_profiles','manifest_rows','installed_shards']},indent=2))
