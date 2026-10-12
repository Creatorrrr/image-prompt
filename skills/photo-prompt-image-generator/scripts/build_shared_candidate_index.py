#!/usr/bin/env python3
"""Build/verify only the native shared index, with durable resumable embeddings."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,hashlib,json,time
import photo_candidate_corpus as c
import photo_global_index as index
from photo_embedding_provider import embed,atomic,load_env,SPACE

def build(assets,cache,workers=12,repair_unknown=False):
    corpus=c.load(assets);records={cid:r for cid,r in corpus['candidates'].items() if r['record_kind'] in index.POSITIVE_KINDS}
    reused={}
    if (assets/index.MANIFEST).is_file():
        # Source binding may change; only same native ID, space, full text and recipe can be reused.
        manifest=c.decode((assets/index.MANIFEST).read_bytes())
        if manifest.get('space')==SPACE and manifest.get('schema')==index.SCHEMA:
            import gzip
            for shard in manifest['shards']:
                raw=(assets/shard['path']).read_bytes()
                if hashlib.sha256(raw).hexdigest()!=shard['sha256']:raise ValueError('corrupt reuse shard')
                reused.update(c.decode(gzip.decompress(raw)))
    seed=cache/'VERIFIED-SEED.json'
    if seed.is_file():
        seed_value=c.decode(seed.read_bytes())
        if seed_value.get('schema')!='photo-native-index-seed/v1' or seed_value.get('space')!=SPACE:raise ValueError('invalid native seed')
        reused.update(seed_value['entries'])
    def one(cid,record):
        recipe,text=index.text(record);old=reused.get(cid)
        if old and old.get('id')==cid and old.get('text')==text and old.get('recipe')==recipe:
            index.validate_vector(old['vector']);return cid,old,True
        result=embed(text,{'candidate_id':cid,'recipe':recipe},cache/'requests',repair_unknown=repair_unknown)
        return cid,{'id':cid,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'recipe':recipe,
            'vector':result['vector'],'embedding_execution':result['execution']},result['cache_hit']
    entries={};hits=0;start=time.monotonic();failed=[]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(one,cid,r) for cid,r in records.items()]
        for future in as_completed(futures):
            try:cid,row,hit=future.result();entries[cid]=row;hits+=hit
            except Exception as e:failed.append(str(e))
            completed=len(entries)+len(failed)
            if completed%250==0:print(json.dumps({'complete':completed,'total':len(records),'cache':hits,'failed':len(failed),'seconds':round(time.monotonic()-start)}),flush=True)
            if len(failed)>=12:
                for pending in futures:pending.cancel()
                raise RuntimeError('build stopped after repeated provider failures; durable records preserved')
    if failed:raise RuntimeError(f'{len(failed)} embedding requests failed; inspect cache before resuming')
    payload={'schema':index.SCHEMA,'space':SPACE,'corpus_sha256':c.digest(corpus),'query_recipe':index.QUERY_RECIPE,'entries':entries}
    index.validate(payload,corpus);identity=index.write(assets,payload)
    report={'index_sha256':identity,'records':len(records),'cache_hits':hits,'provider_calls':len(records)-hits,'elapsed_seconds':round(time.monotonic()-start,3)}
    atomic(cache/'BUILD-REPORT.json',report);return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[1]/'assets');p.add_argument('--cache',type=Path);p.add_argument('--env-file',type=Path);p.add_argument('--workers',type=int,default=12);p.add_argument('--verify',action='store_true');p.add_argument('--repair-unknown',action='store_true',help='Explicit maintenance retry with possible duplicate provider cost; keep original attempt evidence.');a=p.parse_args()
    if a.verify:print(json.dumps({'verified':True,'entries':len(index.load(a.assets,c.load(a.assets))['entries'])}));return
    if a.env_file:load_env(a.env_file)
    print(json.dumps(build(a.assets,a.cache or Path.home()/'.cache/image-prompt/shared-embedding-build',a.workers,a.repair_unknown)))
if __name__=='__main__':main()
