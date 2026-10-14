#!/usr/bin/env python3
"""Build/verify the lazy shared layout; reuse only current verified vector text."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,hashlib,json,time,shutil
import photo_candidate_corpus as c
import photo_global_index as documents
import photo_search_layout as layout
from photo_search_reader import SearchReader
from photo_embedding_provider import embed,embed_many,atomic,load_env,SPACE,default_space


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
    return {'schema':documents.SCHEMA,'space':reader.manifest['space'],'corpus_sha256':c.digest(corpus),'entries':entries}


def build(assets,cache,workers=4,repair_unknown=False,*,space=None,batch_size=32):
    space=space or default_space()
    assets=Path(assets);cache=Path(cache);corpus=c.load(assets)
    records={cid:r for cid,r in corpus['candidates'].items() if r['record_kind'] in documents.POSITIVE_KINDS};reused={}
    if (assets/layout.MANIFEST).is_file():
        reader=SearchReader(assets)
        try:
            if reader.manifest['space']==space:reused=offline_vector_map(reader,corpus)['entries']
        finally:reader.close()
    def one(cid,record):
        recipe,text=documents.text(record);old=reused.get(cid)
        if old is not None:
            documents.validate_vector(old['vector']);return cid,old,'reused'
        result=embed(text,{'candidate_id':cid,'recipe':recipe},cache/'requests',repair_unknown=repair_unknown,space=space,kind='document')
        return cid,{'id':cid,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'recipe':recipe,
                    'vector':result['vector'],'embedding_execution':result['execution']},'cache' if result['cache_hit'] else 'provider'
    entries={};counts={'reused':0,'cache':0,'provider':0};start=time.monotonic();failed=[]
    if space['provider']=='embeddinggemma2-local':
        todo=[]
        for cid,record in sorted(records.items()):
            if cid in reused:entries[cid]=reused[cid];counts['reused']+=1
            else:todo.append((cid,record))
        todo.sort(key=lambda item:(len(documents.text(item[1])[1]),item[0]))
        for offset in range(0,len(todo),batch_size):
            batch=todo[offset:offset+batch_size];projected=[documents.text(r) for _,r in batch]
            rows=embed_many([t for _,t in projected],[{'candidate_id':cid,'recipe':recipe} for (cid,_),(recipe,_) in zip(batch,projected,strict=True)],cache/'requests',space=space,kind='document')
            for (cid,_),(recipe,text),row in zip(batch,projected,rows,strict=True):
                entries[cid]={'id':cid,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'recipe':recipe,'vector':row['vector'],'embedding_execution':row['execution']}
                counts['cache' if row['cache_hit'] else 'provider']+=1
            atomic(cache/'PROGRESS.json',{'records':len(records),'complete':len(entries),'space':space,'counts':counts,'elapsed_seconds':time.monotonic()-start})
            print(json.dumps({'complete':len(entries),'records':len(records),'elapsed_seconds':round(time.monotonic()-start,2)}),flush=True)
    else:
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
    vectors={'schema':documents.SCHEMA,'space':space,'corpus_sha256':c.digest(corpus),'entries':entries}
    documents.validate(vectors,corpus)
    staged=layout.build(assets,corpus,vectors);verification=layout.verify(assets,corpus,staged,vectors)
    # Source and complete derived closure must verify before the active pointer moves.
    if c.digest(c.load(assets))!=c.digest(corpus):raise ValueError('source changed before layout activation')
    atomic(assets/layout.MANIFEST,staged)
    staging=assets/'photo_candidate_search.staging.json'
    if staging.exists():staging.unlink()
    report={'layout_id':staged['layout_id'],'space':space,'records':len(records),'vector_reuse':counts['reused'],'provider_cache_hits':counts['cache'],
            'provider_calls':counts['provider'],'elapsed_seconds':round(time.monotonic()-start,3),'verification':verification}
    atomic(cache/'BUILD-REPORT.json',report);return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[1]/'assets');p.add_argument('--cache',type=Path)
    p.add_argument('--env-file',type=Path);p.add_argument('--workers',type=int,default=4);p.add_argument('--verify',action='store_true')
    p.add_argument('--publish',action='store_true');p.add_argument('--runtime-store',type=Path)
    p.add_argument('--backend',choices=['gemini','embeddinggemma2-local']);p.add_argument('--batch-size',type=int,default=32)
    p.add_argument('--output-assets',type=Path,help='Build separately; retain the original manifest and all Gemini shards.')
    p.add_argument('--repair-unknown',action='store_true',help='Explicit maintenance retry preserving possible duplicate-cost attempt evidence.')
    a=p.parse_args()
    if not 1<=a.batch_size<=128:p.error('batch size must be between 1 and 128')
    if a.backend=='gemini':space=SPACE
    elif a.backend=='embeddinggemma2-local':
        from photo_local_embedding import space as local_space
        space=local_space()
    else:space=default_space()
    if a.output_assets:
        if a.publish:p.error('publish a complete skill source root after evaluating a separate build')
        if a.output_assets.resolve()==a.assets.resolve():p.error('output assets must be separate')
        if not a.output_assets.exists():shutil.copytree(a.assets,a.output_assets)
        elif c.digest(c.load(a.output_assets))!=c.digest(c.load(a.assets)):raise ValueError('resume output source differs from current source')
        a.assets=a.output_assets
    root=a.assets.resolve().parent
    if a.env_file:load_env(a.env_file)
    if a.verify:
        result=layout.verify(a.assets,c.load(a.assets),c.decode((a.assets/layout.MANIFEST).read_bytes()))
    else:
        from photo_runtime_sources import source_update
        with source_update(root,a.runtime_store):result=build(a.assets,a.cache or Path.home()/'.cache/image-prompt/shared-embedding-build',a.workers,a.repair_unknown,space=space,batch_size=a.batch_size)
    if a.publish:
        from photo_runtime_sources import SnapshotPublisher
        published=SnapshotPublisher(root,a.runtime_store).publish();result['publication']=published
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
