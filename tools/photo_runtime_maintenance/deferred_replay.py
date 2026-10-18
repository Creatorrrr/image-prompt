"""Re-run sealed historical layout validators in independent restored trees."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import checks
from deferred_restore import restore_shards
from deferred_state import E, ROOT
from managed_smoke import copied_file
import state


def clone_generation(source,destination):
    source=Path(source);manifest=state.read(source/'manifest.json')
    for name in ['manifest.json',*manifest['members']]:
        p=source/name
        if p.is_symlink() or not p.is_file():raise ValueError('unsafe historical generation member')
        expected=manifest['members'].get(name)
        if expected and state.sha(p)!=expected['sha256']:raise ValueError('historical generation changed')
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);copied_file(p,target)
    if (destination/'embedding-runtime.lock.json').exists():
        lock=state.read(destination/'embedding-runtime.lock.json')
        origin=ROOT/'skills/photo-prompt-image-generator'
        if state.read(origin/'embedding-runtime.lock.json')!=lock:raise ValueError('historical model installation differs')
        for name,row in lock['files'].items():
            src=origin/lock['package']/name
            if state.sha(src)!=row['sha256']:raise ValueError('model source changed')
            target=destination/lock['package']/name;target.parent.mkdir(parents=True,exist_ok=True);copied_file(src,target)
        # Copy the real pinned NumPy package for frozen local search; no fake space/runtime.
        packages=origin/'.runtime/embedding-python/lib/python3.14/site-packages'
        target=destination/'.runtime/embedding-python/lib/python3.14/site-packages';target.mkdir(parents=True,exist_ok=True)
        for p in packages.glob('numpy*'):
            if p.is_dir() and not p.is_symlink():
                shutil.copytree(p,target/p.name,copy_function=copied_file,ignore=shutil.ignore_patterns('__pycache__'))
    return manifest


def worker(root):
    root=Path(root);sys.path.insert(0,str(root/'scripts'))
    import photo_candidate_corpus as corpus
    import photo_search_layout as layout
    import photo_embedding_provider as provider
    def forbidden(*args,**kwargs):raise ValueError('new embedding execution forbidden during historical replay')
    provider.embed=provider.embed_many=forbidden
    if (root/'scripts/photo_local_embedding.py').exists():
        import photo_local_embedding
        photo_local_embedding.infer=forbidden
    manifest=state.read(root/'manifest.json');source=corpus.load(root/'assets')
    result=layout.verify(root/'assets',source,state.read(root/'assets/photo_candidate_search.json'))
    if result!=manifest['search_layout']['qualification']:raise ValueError('saved historical qualification changed')
    query_result=None
    query_file=E/('QUERY-'+manifest['search_layout']['layout_id'][:12]+'.json')
    if query_file.exists():
        query=state.read(query_file)
        from photo_search_reader import SearchReader
        reader=SearchReader(root/'assets');positive=set(reader.meta['positive_ids'])
        if len(positive)!=query['expected_pool']:raise ValueError('historical query pool changed')
        provider.validate_execution(query['execution'],reader.manifest['space'],query['query'],query['vector'],'query')
        if query['kind']=='hybrid':
            import photo_sharded_search as search
            from bm25f_retrieval import reciprocal_rank_fusion
            lexical=search.lexical_rank(reader,{'slot_focus':query['query']},positive,384)
            cosine,proof=search.cosine_rank(reader,query['vector'],positive,384)
            if not search.audit_cosine(reader,query['vector'],positive,cosine,proof):raise ValueError('historical pruning proof failed')
            fused=reciprocal_rank_fusion([[r['document_id'] for r in lexical],[r['document_id'] for r in cosine]],k=30)
            if {'lexical':lexical,'cosine':cosine,'rrf':fused}!=query['expected']:
                raise ValueError('saved named-phrase lane/rank results differ')
            query_result={'kind':'hybrid','lexical_rows':len(lexical),'cosine_rows':len(cosine),
                'rrf_rows':len(fused),'saved_results_equal':True,'pruning_audit':True}
        else:
            from photo_local_embedding import numpy_runtime
            np=numpy_runtime();ids=list(reader.meta['positive_ids']);positions={cid:i for i,cid in enumerate(ids)}
            matrix=np.empty((len(ids),768),dtype=np.float64)
            for number,leaf in enumerate(reader.meta['vector_shards']):
                values=np.asarray(reader.block('vector',number)).reshape((-1,768))
                for cid,row in zip(leaf['ids'],values):matrix[positions[cid]]=row
            matrix/=np.linalg.norm(matrix,axis=1)[:,None]
            vector=np.asarray(query['vector'],dtype=np.float64);vector/=np.linalg.norm(vector)
            scores=vector@matrix.T;ranked=np.argsort(-scores,kind='stable');gold=query['expected']
            if [ids[i] for i in ranked[:10]]!=[r['id'] for r in gold['top10']]:raise ValueError('saved dense top10 differs')
            tolerance=query['score_absolute_tolerance']
            if any(abs(float(scores[i])-row['score'])>tolerance for i,row in zip(ranked[:10],gold['top10'])):
                raise ValueError('saved dense score differs beyond frozen tolerance')
            rank=int(np.flatnonzero(ranked==positions[query['target']])[0])+1
            if rank!=gold['target_rank']:raise ValueError('saved dense target rank differs')
            query_result={'kind':'dense','top10_ids_equal':True,'target_rank':rank,
                'score_absolute_tolerance':tolerance,'saved_results_equal':True}
        reader.close()
    print(json.dumps({'status':'PASS','layout_id':manifest['search_layout']['layout_id'],
        'qualification':result,'saved_qualification_equal':True,'saved_query_replay':query_result,'new_embedding_calls':0,
        'scope':'full frozen source/payload/slot-binding/vector/routing/posting validator replay; no new semantic quality claim'}))


def replay(group,label,backend='git'):
    output=E/('REPLAY-'+label+'-'+group[:12]+'.json')
    if output.exists():raise FileExistsError('historical replay output already exists; choose a fresh label')
    row=next(r for r in state.read(E/'TARGETS.json.gz')['shards'] if r['id']==group)
    original=Path(row['duplicate']['generation'])
    with tempfile.TemporaryDirectory(prefix='photo-historical-validator-') as temp:
        temp=Path(temp);root=temp/'generation';manifest=clone_generation(original,root)
        # Replace the copied old shard with an independently recovered exact tree.
        old=root/'assets/photo_candidate_search_shards'/group
        shutil.rmtree(old)
        restored=restore_shards(temp/'recovered',backend,group)
        recovered=restored/row['path'];recovered.rename(old)
        denied=[ROOT/'skills/photo-prompt-image-generator/scripts',ROOT/'skills/photo-prompt-image-generator/precore',
            Path('/Users/chasoik/.codex/worktrees/slot-search-relevance/image-prompt'),original,
            *[ROOT/r['path'] for r in state.read(E/'TARGETS.json.gz')['shards']]]
        profile=checks.profile()+'(deny file-read* '+' '.join('(subpath '+json.dumps(str(p))+')' for p in denied)+')'
        python=ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
        launcher="import sys,runpy;from pathlib import Path;p=sys.argv.pop(1);sys.path.insert(0,str(Path(p).parent));runpy.run_path(p,run_name='__main__')"
        command=['/usr/bin/sandbox-exec','-p',profile,str(python),'-I','-c',launcher,str(Path(__file__).resolve()),'worker',str(root)]
        p=subprocess.run(command,env=checks.environment(),capture_output=True,text=True,timeout=420)
        result={'status':'FAIL','group':group,'backend':backend,'exit_code':p.returncode,
            'stderr':p.stderr,'stdout':p.stdout,'generation':str(original),'generation_manifest_sha256':state.sha(original/'manifest.json'),
            'original_reads_denied':True,'original_writes_denied':True,'network_denied':True,
            'Gemini_calls':0,'CURRENT_writes':0}
        if p.returncode==0:result.update(json.loads(p.stdout))
        state.write(output,result)
        print('historical validator',group[:12],result['status'],flush=True)
        if result['status']!='PASS':print(p.stderr[-4000:]+p.stdout[-1000:]);raise ValueError('historical validator replay failed')
        return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['worker','replay']);p.add_argument('path')
    p.add_argument('--label',default='baseline');p.add_argument('--backend',choices=['git','sealed'],default='git');a=p.parse_args()
    worker(a.path) if a.command=='worker' else replay(a.path,a.label,a.backend)
