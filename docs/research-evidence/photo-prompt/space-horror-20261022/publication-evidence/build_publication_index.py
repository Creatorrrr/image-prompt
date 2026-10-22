"""Offline publication union, with exact existing text/recipe/vector reuse only."""
from pathlib import Path
import gc,hashlib,json,sys,time
gc.disable()
WORK=Path(__file__).resolve().parents[5]
OUT=WORK/'generated/maintenance/space-horror-publication-build'
OUT.mkdir(parents=True,exist_ok=True)
SKILL=WORK/'skills/photo-prompt-image-generator';ASSETS=SKILL/'assets'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as c,photo_global_index as docs,photo_search_layout as layout
from photo_search_reader import SearchReader
from build_shared_candidate_index import offline_vector_map
from photo_embedding_provider import embed_many
original_digest=c.digest
def streamed(value):
    digest=hashlib.sha256();parts=[];size=0
    for part in json.JSONEncoder(ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).iterencode(value):
        raw=part.encode();parts.append(raw);size+=len(raw)
        if size>=1048576:digest.update(b''.join(parts));parts=[];size=0
    if parts:digest.update(b''.join(parts))
    return digest.hexdigest()
new=json.loads((ASSETS/'photo_candidate_space_horror_20261022.json').read_text())['candidates']
new_bindings=json.loads((ASSETS/'photo_candidate_space_horror_bindings_20261022.json').read_text())['slot_bindings']
for v in [*new.values(),{'unicode':'한글','numbers':[1,-0.0,1.25,True,None]}]:assert streamed(v)==original_digest(v)
c.digest=streamed
started=time.monotonic();current=c.load(ASSETS)
base={**current,'candidates':{k:v for k,v in current['candidates'].items() if k not in new},'slot_bindings':{k:v for k,v in current['slot_bindings'].items() if k not in new_bindings}}
old_manifest=json.loads((ASSETS/layout.MANIFEST).read_text());assert old_manifest['corpus_sha256']==c.digest(base),'upstream source/index must match preserved baseline'
base_source_hashes={k:c.digest(v) for k,v in base['candidates'].items()};base_binding_hashes={k:c.digest(v) for k,v in base['slot_bindings'].items()}
print(json.dumps({'stage':'verify_vectors','base_candidates':len(base['candidates']),'new':len(new),'base_layout':old_manifest['layout_id']}),flush=True)
reader=SearchReader(ASSETS)
try:basevectors=offline_vector_map(reader,base)
finally:reader.close()
docs.validate(basevectors,base)
new_corpus={**current,'candidates':new}
# The pinned experimental native release owns a V2 grounded document recipe.
# Main owns the V1 global recipe. Do not relabel V2 vectors as V1 evidence.
assert basevectors['space']['provider']=='embeddinggemma2-local'
newvectors={'entries':{}};provider_calls=0;cache_hits=0
positives=sorted((cid,row) for cid,row in new.items() if row['record_kind'] in docs.POSITIVE_KINDS)
for start in range(0,len(positives),32):
    batch=positives[start:start+32];projected=[docs.text(row) for _,row in batch]
    encoded=embed_many([text for _,text in projected],[{'candidate_id':cid,'recipe':recipe} for (cid,_),(recipe,_) in zip(batch,projected,strict=True)],OUT/'index-cache/requests',space=basevectors['space'],kind='document')
    for (cid,_),(recipe,text),result in zip(batch,projected,encoded,strict=True):
        newvectors['entries'][cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':result['vector'],'embedding_execution':result['execution']}
        if result['cache_hit']:cache_hits+=1
        else:provider_calls+=1
assert len(newvectors['entries'])==53
new_layout=None
vectors={'schema':docs.SCHEMA,'space':basevectors['space'],'corpus_sha256':c.digest(current),'entries':{**basevectors['entries'],**newvectors['entries']}}
docs.validate(vectors,current)
print(json.dumps({'stage':'build_union_layout','positive':len(vectors['entries']),'local_document_calls':provider_calls}),flush=True)
manifest=layout.build(ASSETS,current,vectors);verification=layout.verify(ASSETS,current,manifest,vectors)
(ASSETS/layout.MANIFEST).write_bytes(c.canonical_bytes(manifest)+b'\n')
staging=ASSETS/'photo_candidate_search.staging.json'
if staging.exists():staging.unlink()
fresh=c.load(ASSETS);assert fresh==current
assert all(c.digest(fresh['candidates'][k])==h for k,h in base_source_hashes.items())
assert all(c.digest(fresh['slot_bindings'][k])==h for k,h in base_binding_hashes.items())
report={'status':'pass','source_candidates':len(current['candidates']),'positive_candidates':len(vectors['entries']),'diagnostics':len(current['candidates'])-len(vectors['entries']),'bindings':len(current['slot_bindings']),'preserved_base_candidates':len(base['candidates']),'preserved_base_bindings':len(base['slot_bindings']),'base_vectors_reused_exactly':len(basevectors['entries']),'new_records':len(new),'new_positive':53,'new_diagnostic':26,'new_bindings':len(new_bindings),'source_sha256':c.digest(current),'base_layout':old_manifest['layout_id'],'experimental_native_layout_schema':'photo-candidate-search-layout/v2','published_layout_schema':manifest['schema'],'experimental_vectors_reused':False,'layout_id':manifest['layout_id'],'verification':verification,'index_closure_members':len(manifest['shards'])+1,'local_document_calls':provider_calls,'local_cache_hits':cache_hits,'image_calls':0,'network_model_calls':0,'streamed_hash_equivalence_checks':len(new)+1,'runtime_code_changes':False,'runtime_config_changed':False,'CURRENT_writes':0,'elapsed_seconds':time.monotonic()-started}
(OUT/'INDEX-BUILD.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
dest=WORK/'docs/research-evidence/photo-prompt/space-horror-20261022/publication-evidence/index-build.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
