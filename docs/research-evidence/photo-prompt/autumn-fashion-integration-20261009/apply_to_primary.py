"""Add this domain only. Preserve concurrent authored sources and old shards."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone

WORKTREE=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=Path('skills/photo-prompt-image-generator')
EVIDENCE=Path('docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009')
sys.path.insert(0,str(WORKTREE/REL/'scripts'))
import prompt_generator as pg
from photo_runtime_sources import source_update

def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy_new(src,dst):
 if dst.exists():
  if src.read_bytes()!=dst.read_bytes():raise ValueError('Existing destination differs: '+str(dst))
 else:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)

def main():
 src=WORKTREE/REL/'assets';dst=PRIMARY/REL/'assets';ev=PRIMARY/EVIDENCE
 before={str(p.relative_to(PRIMARY)):sha(p) for p in dst.glob('*.json')}
 original_manifest=json.loads((dst/'photo_prompt_source_manifest.json').read_text())
 manifest=json.loads(json.dumps(original_manifest))
 for filename,kind in [('photo_prompt_autumn_fashion_extension.json','candidate'),('photo_prompt_visual_obligations_autumn_fashion.json','visual_profile')]:
  if any(s['file']==filename for s in manifest['sources']):raise ValueError('Already registered '+filename)
  manifest['sources'].append({'file':filename,'kind':kind,'required':True,'load_order':max(s['load_order'] for s in manifest['sources'] if s['kind']==kind)+1})
 dump(ev/'PRIMARY-PREAPPLY.json',{'time':datetime.now(timezone.utc).isoformat(),'files':before,'manifest':original_manifest})
 with source_update(PRIMARY/REL):
  if json.loads((dst/'photo_prompt_source_manifest.json').read_text())!=original_manifest:raise ValueError('Concurrent registration changed; recapture instead of overwriting')
  for name in ['photo_prompt_autumn_fashion_extension.json','photo_prompt_visual_obligations_autumn_fashion.json']:copy_new(src/name,dst/name)
  for p in (WORKTREE/'docs/research-evidence/photo-prompt/extension-maintenance').glob('autumn-fashion-selected-relations-20261009-*.json'):
   copy_new(p,PRIMARY/'docs/research-evidence/photo-prompt/extension-maintenance'/p.name)
  dump(dst/'photo_prompt_source_manifest.json',manifest)
  # Only copy index bytes when canonical compiled meanings are identical.
  wdata=pg.load_json(src/'photo_prompt_tags.json');pdata=pg.load_json(dst/'photo_prompt_tags.json')
  if pg.dictionary_hash(wdata)!=pg.dictionary_hash(pdata):raise ValueError('Concurrent source difference requires a canonical merged rebuild')
  wreg=pg.load_visual_obligation_registry(src/'photo_prompt_visual_obligations.json');preg=pg.load_visual_obligation_registry(dst/'photo_prompt_visual_obligations.json')
  if wreg!=preg:raise ValueError('Concurrent visual difference requires a merged rebuild')
  for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
   pg_payload=pg.load_semantic_index_payload(src/name) if name=='photo_prompt_semantic_index.json' else pg.load_visual_profile_index(src/name,wreg)
   if name=='photo_prompt_semantic_index.json':pg.validate_semantic_index_metadata(pg_payload,wdata)
   m=json.loads((src/name).read_text())
   # Content-addressed generations remain available to current readers.
   for directory in ['photo_prompt_semantic_index_shards','photo_prompt_visual_profile_index_shards']:
    if (src/directory).exists():
     for p in (src/directory).glob('*.json'):copy_new(p,dst/directory/p.name)
   shutil.copy2(src/name,dst/name)
 copy_new(WORKTREE/'tests/test_photo_autumn_fashion_semantics.py',PRIMARY/'tests/test_photo_autumn_fashion_semantics.py')
 for p in (WORKTREE/EVIDENCE).iterdir():
  if p.is_file() and p.name not in {'PRIMARY-BEFORE.json','PRIMARY-TRACKED-BEFORE.zip','PRIMARY-PREAPPLY.json','PRIMARY-APPLICATION.json'}:
   target=ev/p.name
   if not target.exists():shutil.copy2(p,target)
 changed=[p for p,h in before.items() if sha(PRIMARY/p)!=h]
 allowed={str(REL/'assets'/n) for n in ['photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']}
 unexpected=[p for p in changed if p not in allowed]
 result={'time':datetime.now(timezone.utc).isoformat(),'original_manifest_rows_preserved':manifest['sources'][:len(original_manifest['sources'])]==original_manifest['sources'],
  'dictionary_sha256':pg.dictionary_hash(pdata),'new_candidates':112,'new_profiles':112,'reused_contracts':17,
  'prior_assets_compared':len(before),'changed_original_assets':changed,'unexpected_authored_differences':unexpected,
  'primary_runtime_publication':'pending','commit_push':'not_requested'}
 dump(ev/'PRIMARY-APPLICATION.json',result);print(json.dumps(result))
 if unexpected:raise ValueError('Concurrent original-source changes observed; not overwritten')

if __name__=='__main__':main()
