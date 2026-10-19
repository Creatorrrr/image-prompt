#!/usr/bin/env python3
"""Offline paired, same-corpus retrieval qualification from frozen inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import photo_candidate_corpus as c
from photo_embedding_provider import atomic,embed_many,GEMINI_SPACE
from photo_local_embedding import space as local_space


def matrix(assets):
    import numpy as np
    from photo_search_reader import SearchReader
    reader=SearchReader(assets)
    try:
        ids=list(reader.meta['positive_ids']);positions={cid:i for i,cid in enumerate(ids)}
        values=np.empty((len(ids),768),dtype=np.float64)
        for number,leaf in enumerate(reader.meta['vector_shards']):
            rows=np.asarray(reader.block('vector',number)).reshape((-1,768))
            for cid,row in zip(leaf['ids'],rows,strict=True):values[positions[cid]]=row
        values/=np.linalg.norm(values,axis=1)[:,None]
        return ids,values,dict(reader.manifest)
    finally:reader.close()


def queries(inputs,out):
    values=[];space=local_space()
    for offset in range(0,len(inputs),32):
        batch=inputs[offset:offset+32]
        rows=embed_many([r['query'] for r in batch],[{'qualification_index':r['index']} for r in batch],out/'query-cache',space=space)
        values.extend(rows)
        print(json.dumps({'queries_complete':len(values),'queries':len(inputs)}),flush=True)
    return values


def run(a):
    import numpy as np
    inputs=json.loads(a.inputs.read_bytes());a.output.mkdir(parents=True,exist_ok=True)
    local_queries=queries(inputs['queries'],a.output)
    if a.prepare_queries_only:return {'queries_prepared':len(local_queries)}
    before_ids,gemini,old=matrix(a.gemini_assets);after_ids,local,new=matrix(a.local_assets)
    if (before_ids!=after_ids or old['space']!=GEMINI_SPACE or new['space']!=local_space()
            or old['corpus_sha256']!=inputs['corpus_sha256'] or new['corpus_sha256']!=inputs['corpus_sha256']):
        raise ValueError('qualification inputs/source/model populations do not match')
    positions={cid:i for i,cid in enumerate(before_ids)};results=[]
    for offset in range(0,len(inputs['queries']),32):
        batch=inputs['queries'][offset:offset+32]
        gq=np.asarray([r['gemini_vector'] for r in batch]);lq=np.asarray([r['vector'] for r in local_queries[offset:offset+32]])
        gq/=np.linalg.norm(gq,axis=1)[:,None];lq/=np.linalg.norm(lq,axis=1)[:,None]
        scores={'gemini':gq@gemini.T,'local':lq@local.T}
        for row_number,row in enumerate(batch):
            result={k:row[k] for k in ('index','target','provenance','query','language','fidelity')}
            for label,table in scores.items():
                ranked=np.argsort(-table[row_number],kind='stable')
                target=positions[row['target']]
                rank=int(np.flatnonzero(ranked==target)[0])+1
                result[label]={'target_rank':rank,'target_score':float(table[row_number,target]),
                    'top10':[{'id':before_ids[i],'score':float(table[row_number,i])} for i in ranked[:10]]}
            results.append(result)
    summary={};passed=True
    for language in ('ko','en'):
        subset=[r for r in results if r['language']==language and r['fidelity']=='VALID']
        metrics={}
        for backend in ('gemini','local'):
            metrics[backend]={'n':len(subset),'recall1':sum(r[backend]['target_rank']<=1 for r in subset)/len(subset),
                'recall5':sum(r[backend]['target_rank']<=5 for r in subset)/len(subset),
                'recall10':sum(r[backend]['target_rank']<=10 for r in subset)/len(subset),
                'mrr':sum(1/r[backend]['target_rank'] for r in subset)/len(subset)}
        delta=metrics['local']['recall5']-metrics['gemini']['recall5'];gate=delta>=-0.02-1e-12
        summary[language]={**metrics,'recall5_delta':delta,'gate_pass':gate};passed&=gate
    report={'schema':'photo-local-vector-qualification/v1','corpus_sha256':inputs['corpus_sha256'],
        'inputs_sha256':hashlib.sha256(a.inputs.read_bytes()).hexdigest(),'gemini_layout_id':old['layout_id'],'local_layout_id':new['layout_id'],
        'space':new['space'],'languages':summary,'valid_queries':sum(r['fidelity']=='VALID' for r in results),
        'excluded_ambiguous':sum(r['fidelity']!='VALID' for r in results),'vector_quality_pass':bool(passed),
        'scope':'Same current full positive pool; reused frozen source-conditioned synthetic queries and original Gemini query vectors. Does not prove production or image quality.'}
    atomic(a.output/'ranks.json',results);atomic(a.output/'vector-summary.json',report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gemini-assets',type=Path,required=True);p.add_argument('--local-assets',type=Path,required=True)
    p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--prepare-queries-only',action='store_true')
    a=p.parse_args();print(json.dumps(run(a),ensure_ascii=False))


if __name__=='__main__':main()
