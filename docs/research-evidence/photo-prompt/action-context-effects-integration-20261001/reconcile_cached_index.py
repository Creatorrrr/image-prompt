"""Reconcile two immutable exact-text caches without credentials or API calls."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).resolve().parent
A = ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(A.parent/'scripts'))
import prompt_generator as g
import build_semantic_index as build
CLEANUP='06bd1edb6dfc5f3b69aad78137ec3fd3755a9f97'
UPSTREAM='98847a8bcc35f85142fe0eb4322e35eacbe9fdc2'

def cache_at(commit):
    raw=subprocess.check_output(['git','show',commit+':skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json'],cwd=ROOT)
    with tempfile.NamedTemporaryFile(dir=A,suffix='.json',delete=False)as f:
        temporary=Path(f.name);f.write(raw)
    try:return g.load_semantic_index_payload(temporary)
    finally:temporary.unlink()

old=cache_at(CLEANUP);upstream=cache_at(UPSTREAM)
assert all(x['provider']==g.SEMANTIC_PROVIDER and x['embedding_model']==g.SEMANTIC_MODEL_ID and x['embedding_dimensions']==g.DEFAULT_SEMANTIC_DIMENSIONS==768 for x in [old,upstream])
data=g.load_json(A/'photo_prompt_tags.json');bm=g.build_semantic_bm25f_payload(data);entries={};provenance=[];missing=[]
for key,kind,entry,slot in g.iter_semantic_entries(data):
    text=g.semantic_text_for_entry(entry,slot,kind=kind)
    hits=[(name,c['entries'][key])for name,c in [('cleanup',old),('upstream',upstream)]if key in c['entries']and c['entries'][key]['text']==text]
    if not hits:missing.append(key);continue
    assert all(v['vector']==hits[0][1]['vector']for _,v in hits),key
    entries[key]={'kind':kind,'slot':slot,'id':entry['id'],'text':text,'vector':hits[0][1]['vector'],'bm25f_document':bm['documents'][key]}
    provenance.append({'key':key,'matching_caches':[n for n,_ in hits],'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
assert not missing,missing
assert len(entries)==10174
payload={'provider':g.SEMANTIC_PROVIDER,'dictionary_hash':g.dictionary_hash(data),'semantic_text_recipe':g.SEMANTIC_TEXT_RECIPE_VERSION,'embedding_model':g.SEMANTIC_MODEL_ID,'embedding_dimensions':768,'bm25f':{k:v for k,v in bm.items()if k!='documents'},'entries':entries}
g.validate_semantic_index_metadata(payload,data)
build.write_sharded_payload(A/'photo_prompt_semantic_index.json',payload,keep_stale_generations=True)
verified=g.load_semantic_index(A/'photo_prompt_semantic_index.json',data)
assert len(verified['entries'])==len(entries)
counts={','.join(v):sum(r['matching_caches']==v for r in provenance)for v in [['cleanup','upstream'],['cleanup'],['upstream']]}
report={'cleanup_commit':CLEANUP,'upstream_commit':UPSTREAM,'dictionary_hash':g.dictionary_hash(data),'documents':len(entries),'model':g.SEMANTIC_MODEL_ID,'dimensions':768,'cache_counts':counts,'missing_exact_text_inputs':missing,'new_api_calls':0,'additional_cost_usd':0,'shared_matching_vectors_identical':True,'all_previous_shard_generations_preserved':True,'provenance':provenance}
(E/'index-reconciliation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='provenance'},ensure_ascii=False,indent=2))
