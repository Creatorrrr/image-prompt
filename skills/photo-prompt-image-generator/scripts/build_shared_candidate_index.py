#!/usr/bin/env python3
"""Build/verify the lazy shared layout; reuse only current verified vector text."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,hashlib,json,time
import photo_candidate_corpus as c
import photo_global_index as documents
import photo_search_layout as layout
from photo_search_reader import SearchReader
from photo_embedding_provider import embed,atomic,load_env,SPACE


def offline_vector_map(reader,corpus):
    """Explicit offline all-vector materialization, never called by retrieval."""
    entries={}
    for number,row in enumerate(reader.meta['vector_shards']):
        values=reader.block('vector',number)
        for offset,cid in enumerate(row['ids']):
            if cid not in corpus['candidates']:continue
            recipe,text=documents.text(corpus['candidates'][cid]);old=reader.meta['vector_recipes'][cid]
            if old['recipe']!=recipe or old['text_sha256']!=hashlib.sha256(text.encode()).hexdigest():continue
            entry={'id':cid,'recipe':recipe,'text':text,'text_sha256':old['text_sha256'],'vector':values[offset*768:(offset+1)*768].tolist()}
            if 'embedding_execution' in old:entry['embedding_execution']=c.decode(c.canonical_bytes(old['embedding_execution']))
            entries[cid]=entry
    return {'schema':documents.SCHEMA,'space':SPACE,'corpus_sha256':c.digest(corpus),'entries':entries}


def build(assets,cache,workers=4,repair_unknown=False):
    assets=Path(assets);cache=Path(cache);corpus=c.load(assets)
    records={cid:r for cid,r in corpus['candidates'].items() if r['record_kind'] in documents.POSITIVE_KINDS};reused={}
    if (assets/layout.MANIFEST).is_file():
        reader=SearchReader(assets)
        try:reused=offline_vector_map(reader,corpus)['entries']
        finally:reader.close()
    def one(cid,record):
        recipe,text=documents.text(record);old=reused.get(cid)
        if old is not None:
            documents.validate_vector(old['vector']);return cid,old,'reused'
        result=embed(text,{'candidate_id':cid,'recipe':recipe},cache/'requests',repair_unknown=repair_unknown)
        return cid,{'id':cid,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'recipe':recipe,
                    'vector':result['vector'],'embedding_execution':result['execution']},'cache' if result['cache_hit'] else 'provider'
    entries={};counts={'reused':0,'cache':0,'provider':0};start=time.monotonic();failed=[]
    with ThreadPoolExecutor(max_workers=max(1,min(8,workers))) as pool:
        futures=[pool.submit(one,cid,r) for cid,r in records.items()]
        for future in as_completed(futures):
            try:cid,row,state=future.result();entries[cid]=row;counts[state]+=1
            except Exception as error:failed.append(type(error).__name__)
            if len(failed)>=12:
                for pending in futures:pending.cancel()
                raise RuntimeError('repeated provider failures; durable attempts preserved')
    if failed:raise RuntimeError(f'{len(failed)} embedding requests failed; inspect durable attempts before resuming')
    if c.digest(c.load(assets))!=c.digest(corpus):raise ValueError('source changed during offline build')
    vectors={'schema':documents.SCHEMA,'space':SPACE,'corpus_sha256':c.digest(corpus),'entries':entries}
    documents.validate(vectors,corpus)
    staged=layout.build(assets,corpus,vectors);verification=layout.verify(assets,corpus,staged,vectors)
    # Source and complete derived closure must verify before the active pointer moves.
    if c.digest(c.load(assets))!=c.digest(corpus):raise ValueError('source changed before layout activation')
    atomic(assets/layout.MANIFEST,staged)
    staging=assets/'photo_candidate_search.staging.json'
    if staging.exists():staging.unlink()
    report={'layout_id':staged['layout_id'],'records':len(records),'vector_reuse':counts['reused'],'provider_cache_hits':counts['cache'],
            'provider_calls':counts['provider'],'elapsed_seconds':round(time.monotonic()-start,3),'verification':verification}
    atomic(cache/'BUILD-REPORT.json',report);return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[1]/'assets');p.add_argument('--cache',type=Path)
    p.add_argument('--env-file',type=Path);p.add_argument('--workers',type=int,default=4);p.add_argument('--verify',action='store_true')
    p.add_argument('--publish',action='store_true');p.add_argument('--runtime-store',type=Path)
    p.add_argument('--repair-unknown',action='store_true',help='Explicit maintenance retry preserving possible duplicate-cost attempt evidence.')
    a=p.parse_args();root=a.assets.resolve().parent
    if a.env_file:load_env(a.env_file)
    if a.verify:
        result=layout.verify(a.assets,c.load(a.assets),c.decode((a.assets/layout.MANIFEST).read_bytes()))
    else:
        from photo_runtime_sources import source_update
        with source_update(root,a.runtime_store):result=build(a.assets,a.cache or Path.home()/'.cache/image-prompt/shared-embedding-build',a.workers,a.repair_unknown)
    if a.publish:
        from photo_runtime_sources import SnapshotPublisher
        published=SnapshotPublisher(root,a.runtime_store).publish();result['publication']=published
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
