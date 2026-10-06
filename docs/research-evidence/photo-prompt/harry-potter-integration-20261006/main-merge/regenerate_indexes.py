"""Regenerate merged indexes using only byte-identical compatible cached vectors."""
from pathlib import Path
import sys, json, hashlib
from datetime import datetime, timezone
from unittest.mock import patch
ROOT=Path.cwd(); OUT=ROOT/'docs/research-evidence/photo-prompt/harry-potter-integration-20261006/main-merge';ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as pg
import build_semantic_index as sb
import build_visual_profile_index as vb
PRIMARY=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets')
data=pg.load_json(ASSETS/'photo_prompt_tags.json')
space={'provider':pg.SEMANTIC_PROVIDER,'model':pg.SEMANTIC_MODEL_ID,'dimensions':pg.DEFAULT_SEMANTIC_DIMENSIONS}
expected=sb.base_payload(data,space['provider'],space['model'],space['dimensions'])
caches=[('main',pg.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json')),('qualified_appearance',pg.load_semantic_index_payload(PRIMARY/'photo_prompt_semantic_index.json'))]
entries={};selection=[];missing=[]
for key,kind,row,slot in pg.iter_semantic_entries(data):
 text=pg.semantic_text_for_entry(row,slot,kind=kind)
 for name,cache in caches:
  if not sb.metadata_matches(cache,expected):continue
  entry=cache.get('entries',{}).get(key)
  if not entry or entry.get('text')!=text or len(entry.get('vector',[]))!=space['dimensions']:continue
  entries[key]=entry;selection.append({'key':key,'cache':name,'text_sha256':hashlib.sha256(text.encode()).hexdigest()});break
 else:missing.append(key)
assert missing==['slot:wearable_accessory:wireframe_round_glasses'],missing
sb.load_project_env()
checkpoint=OUT/'merged-semantic.checkpoint.json';checkpoint.write_text(json.dumps(dict(expected,entries=entries)))
semantic=sb.build_resumable_index_payload(data,output=ASSETS/'photo_prompt_semantic_index.json',checkpoint=checkpoint,batch_size=1,request_interval=0,retry_attempts=0,retry_initial_delay=0,**space)
semantic['created_at']=datetime.now(timezone.utc).isoformat()
sb.write_sharded_payload(ASSETS/'photo_prompt_semantic_index.json',semantic,shard_count=16,keep_stale_generations=True)
checkpoint.unlink()
registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
vectors=vb.reusable_vectors([ASSETS/'photo_prompt_visual_profile_index.json',PRIMARY/'photo_prompt_visual_profile_index.json'],registry,**space)
assert len(vectors)==len(registry['profiles'])
visual=pg.build_visual_profile_index_payload(registry,vectors=vectors,**space)
vb.write_payload(ASSETS/'photo_prompt_visual_profile_index.json',visual)
pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',registry,**space)
proof={'status':'REGENERATED_FROM_BOTH_AUTHORED_SIDES','dictionary_hash':pg.dictionary_hash(data),'profile_count':len(registry['profiles']),'candidate_count':sum(len(x) for x in data['slots'].values()),'semantic_entries':len(semantic['entries']),'new_embedding_calls':len(missing),'batch_size':1,'vector_reuse':{n:sum(r['cache']==n for r in selection) for n,_ in caches},'exact_text_and_provider_model_dimensions_required':True,'semantic_selection':selection}
(OUT/'INDEX-REGENERATION.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k!='semantic_selection'}))
