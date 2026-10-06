"""Rebuild main plus palette indexes; require complete exact compatible caches."""
from pathlib import Path
import gc
import hashlib
import json
import sys
import tempfile
from contextlib import nullcontext

E=Path(__file__).resolve().parent
W=E.parents[3]
Q=Path('/Users/chasoik/.codex/worktrees/color-palette-integration/image-prompt')
S=Path('skills/photo-prompt-image-generator')
A=W/S/'assets'
sys.path.insert(0,str(W/S/'scripts'))
import prompt_generator as pg
import build_visual_profile_index as visual
import build_semantic_index as semantic
from photo_runtime_sources import source_update, complete_source_update, _pointer_directory

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def projection(payload):return {k:digest({'text':v['text'],'vector':v['vector']}) for k,v in payload['entries'].items()}
def cache_miss(*a,**kw):raise AssertionError('Merged input is missing an exact compatible cached embedding')
visual.embed_texts_with_gemini=cache_miss
semantic.embed_texts_with_gemini=cache_miss
sem=A/'photo_prompt_semantic_index.json';vis=A/'photo_prompt_visual_profile_index.json'
# The first cache attempt retained an interrupted maintenance revision. Restore
# its unchanged parent projection before retrying the owned derived outputs.
parent_vis=E/'v32-parent-source-files'/S/'assets'/vis.name
if not (E/'INDEX-REBUILD.json').exists():vis.write_bytes(parent_vis.read_bytes())
before_sem=projection(pg.load_semantic_index_payload(sem));gc.collect()
before_vis=projection(pg.load_visual_profile_index_payload(vis));gc.collect()
metadata=json.loads(sem.read_text());provider,model,dimensions=(metadata[k] for k in ['provider','embedding_model','embedding_dimensions'])
registry=pg.load_visual_obligation_registry(A/'photo_prompt_visual_obligations.json')
data=pg.load_json(A/'photo_prompt_tags.json')
store=Path('/tmp/color-palette-main-merge-20261007/runtime-store')
repair='--repair-interrupted-revision' in sys.argv
revision=json.loads((_pointer_directory(store,W/S,'local_current')/'SOURCE.json').read_text()) if repair else None
if repair:assert revision.get('editing') and not (E/'INDEX-REBUILD.json').exists()
with nullcontext() if repair else source_update(W/S,store):
    vectors=visual.reusable_vectors([vis,Q/S/'assets'/vis.name],registry,provider=provider,model=model,dimensions=dimensions)
    assert len(vectors)==len(registry['profiles'])
    payload=visual.build_visual_profile_index_payload(registry,vectors=vectors,provider=provider,model=model,dimensions=dimensions)
    visual.write_payload(vis,payload)
    after_vis=projection(payload)
    del payload,vectors;gc.collect()
    with tempfile.TemporaryDirectory(prefix='palette-merged-cache-') as temporary:
        combined=semantic.build_resumable_index_payload(data,output=sem,checkpoint=Path(temporary)/'merged.partial.json',provider=provider,model=model,dimensions=dimensions,batch_size=1,request_interval=0,retry_attempts=1,retry_initial_delay=0,cache_indexes=[Q/S/'assets'/sem.name,sem])
        semantic.write_sharded_payload(sem,combined,shard_count=16,keep_stale_generations=True)
        after_sem=projection(combined)
        dictionary_hash=combined['dictionary_hash']
        del combined;gc.collect()

assert set(before_sem)<=set(after_sem) and all(v==after_sem[k] for k,v in before_sem.items())
assert set(before_vis)<=set(after_vis) and all(v==after_vis[k] for k,v in before_vis.items())
assert len(after_sem)-len(before_sem)==37
assert len(after_vis)-len(before_vis)==13
pg.validate_semantic_index_metadata(pg.load_semantic_index_payload(sem),data)
pg.validate_visual_profile_index_metadata(pg.load_visual_profile_index_payload(vis),registry)
if repair:complete_source_update(W/S,store,token=revision['editing'])
receipt={'schema':'palette-merged-index-rebuild/v1','status':'PASS','embedding_calls':0,'native_image_calls':0,'provider':provider,'model':model,'dimensions':dimensions,
         'semantic_entries':len(after_sem),'visual_profiles':len(after_vis),'semantic_original_main_entries_preserved':len(before_sem),'visual_original_main_entries_preserved':len(before_vis),'new_semantic_entries':37,'new_visual_profiles':13,'removed_entries':0,'old_shards_removed':0,'dictionary_hash':dictionary_hash,'semantic_index_sha256':sha(sem),'visual_index_sha256':sha(vis)}
(E/'INDEX-REBUILD.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2),flush=True)
