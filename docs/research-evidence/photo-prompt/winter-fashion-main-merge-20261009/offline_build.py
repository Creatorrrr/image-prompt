"""Canonical merged index builds using only identical compatible cached vectors."""
from pathlib import Path
import hashlib,json,os,sys

ROOT=Path(sys.argv[1]).resolve()
OUT=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-main-merge-20261009')
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(SCRIPTS))
os.environ['PHOTO_RUNTIME_STORE']=str(OUT/'publication-runtime-store')
import prompt_generator as pg
import build_semantic_index as semantic
import build_visual_profile_index as visual

def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

data=pg.load_json(ASSETS/'photo_prompt_tags.json')
semantic_caches=[pg.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json'),pg.load_semantic_index_payload(PRIMARY/'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json')]
expected=semantic.base_payload(data,pg.SEMANTIC_PROVIDER,pg.SEMANTIC_MODEL_ID,pg.DEFAULT_SEMANTIC_DIMENSIONS)
entries={};missing=[]
for key,kind,entry,slot in pg.iter_semantic_entries(data):
    text=pg.semantic_text_for_entry(entry,slot,kind=kind)
    choices=[cache.get('entries',{}).get(key) for cache in semantic_caches if semantic.metadata_matches(cache,expected)]
    exact=next((row for row in reversed(choices) if isinstance(row,dict) and row.get('text')==text and isinstance(row.get('vector'),list) and len(row['vector'])==pg.DEFAULT_SEMANTIC_DIMENSIONS),None)
    if exact is None:missing.append(key)
    else:entries[key]=exact
if missing:raise RuntimeError('Missing identical semantic vectors: '+repr(missing))
expected['entries']=entries
checkpoint=OUT/'merged-semantic-cache.partial'
save(checkpoint.name,expected)
primary_visual=pg.load_visual_profile_index_payload(PRIMARY/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json')
visual_cache=OUT/'frozen-visual-cache.local.json'
save(visual_cache.name,primary_visual)
registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
vectors=visual.reusable_vectors([visual_cache,ASSETS/'photo_prompt_visual_profile_index.json'],registry,provider=pg.SEMANTIC_PROVIDER,model=pg.SEMANTIC_MODEL_ID,dimensions=pg.DEFAULT_SEMANTIC_DIMENSIONS)
visual_ids={p['id'] for p in registry['profiles']}
if visual_ids-set(vectors):raise RuntimeError('Missing identical visual vectors: '+repr(sorted(visual_ids-set(vectors))))
calls=0
def forbid_embedding(*args,**kwargs):
    global calls
    calls+=1
    raise RuntimeError('Publication is offline; a new embedding request is forbidden')
semantic.embed_texts_with_gemini=forbid_embedding
visual.embed_texts_with_gemini=forbid_embedding
print(json.dumps({'cached_semantic_entries':len(entries),'cached_visual_profiles':len(vectors),'provider':pg.SEMANTIC_PROVIDER,'model':pg.SEMANTIC_MODEL_ID,'dimensions':pg.DEFAULT_SEMANTIC_DIMENSIONS,'new_embedding_calls':calls}),flush=True)
sys.argv=['build_semantic_index.py','--checkpoint',str(checkpoint),'--batch-size','1','--request-interval','0','--progress','--no-runtime-publication']
assert semantic.main()==0
sys.argv=['build_visual_profile_index.py','--cache-index',str(visual_cache),'--batch-size','1','--no-runtime-publication']
assert visual.main()==0
save('OFFLINE-BUILD.json',{'status':'pass','source_root':str(ROOT),'semantic_entries':len(entries),'visual_profiles':len(vectors),'new_embedding_calls':calls,'reuse_rule':'same entry identity, full text, provider, model and dimensions','semantic_manifest_sha256':digest(ASSETS/'photo_prompt_semantic_index.json'),'visual_manifest_sha256':digest(ASSETS/'photo_prompt_visual_profile_index.json')})
print('PASS canonical merged indexes; new embedding calls = '+str(calls),flush=True)
