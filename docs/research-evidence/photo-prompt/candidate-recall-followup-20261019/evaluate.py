"""Execute the sealed full-pool kernel once per lane/goal and audit its outputs."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import io
import sys
import time
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
OLD=E.parent/'candidate-semantic-renewal-20261018';S=ROOT/'skills/photo-prompt-image-generator'
CACHE=Path.home()/'.cache/image-prompt/candidate-recall-followup-20261019'
sys.path.insert(0,str(S/'scripts'))
from photo_candidate_authoring import read, write, file_sha
from photo_candidate_lane_generation import Generation, kernel
from photo_candidate_evaluation import measure
from diagnose import order as independent_order
from build import verify_freeze


def execute(arm):
    verify_freeze()
    for relative,sha in read(E/'EVALUATOR-FREEZE.json')['files'].items():
        if file_sha(ROOT/relative)!=sha:raise ValueError('evaluator changed: '+relative)
    target=E/('RESULT-'+arm+'.json')
    if target.exists():raise ValueError('arm already evaluated; do not repeat to tune it')
    doc_arm=arm if arm!='Q1' else read(E/'SELECTED-DOCUMENTS.json')['selected']
    built=read(E/('BUILD-'+doc_arm+'.json'))
    generation=Generation(CACHE/'store',built['generation_id'])
    index=generation.index();rf=kernel(generation.root)['photo_recall_first']
    reference=read(OLD/'baseline/QUERIES.json.gz')
    if reference['binding']!=generation.binding:raise ValueError('query/model binding differs')
    queries=dict(reference['goals'])
    fresh=read(OLD/'baseline/FRESH-QUERIES.json.gz')['rows']
    for value in read(OLD/'baseline/FRESH-GOALS.json.gz')['goals']:
        queries['fresh/'+value['goal_id']]={'text':value['query'],'row':fresh[value['goal_id']]}
    if arm=='Q1':
        q=read(E/'Q1-QUERIES.json')
        expected=set(read(E/'CRITERIA.json')['Q1_goals'])
        if set(q['goals'])!=expected or q['binding']!=generation.binding:raise ValueError('Q1 scope or model changed')
        queries.update(q['goals'])
    goals=sorted(queries);positions={r['id']:i for i,r in enumerate(generation.metadata)}
    rows=[];sparse_rows=[];dense_rows=[];top8={};orders={};durations=[]
    started=time.monotonic()
    archived=np.load(E/'reference-orders.npz',allow_pickle=False)
    old_goals=list(archived['goals']);bitwise=0
    az=zipfile.ZipFile(OLD/'saved-scores-A.zip');cz=zipfile.ZipFile(OLD/'saved-scores-C.zip')
    for number,goal in enumerate(goals,1):
        query=queries[goal];rf.check_embedding(query['row'],generation.binding,query['text'],'query')
        tick=time.monotonic();result=index.search(query['text'],query['row'],generation.binding)
        durations.append(time.monotonic()-tick)
        if result['lane_calls']!={'BM25F':1,'local_cosine':1} or result['considered_CIDs']!=18180 or result['considered_RIDs']!=18182:
            raise ValueError('full pool or lane budget changed')
        sparse=np.asarray(result['bm25'],dtype='<f8');dense=np.asarray(result['cosine'],dtype='<f8')
        actual=[positions[r['id']] for r in result['order']]
        recomputed,_=independent_order(generation.metadata,sparse,dense)
        if actual!=recomputed:raise ValueError('independent full-rank RRF differs')
        name=hashlib.sha256(goal.encode()).hexdigest()+'.npz'
        with np.load(io.BytesIO(cz.read(name)),allow_pickle=False) as old:
            if arm!='Q1' and not np.array_equal(sparse,old['bm25']):raise ValueError('sparse differs from frozen C')
        if arm=='D1':
            with np.load(io.BytesIO(az.read(name)),allow_pickle=False) as old:
                if not np.array_equal(dense,old['cosine']):raise ValueError('D1 dense differs from A')
            if actual!=list(archived['D1'][old_goals.index(goal)]):raise ValueError('D1 rank differs from cross-lane reference')
            bitwise+=1
        sparse_rows.append(sparse);dense_rows.append(dense);rows.append(actual)
        orders[goal]=[r['id'] for r in result['order']];top8[goal]=result['order'][:8]
        if number%15==0:print(arm,'full-pool goals',number,len(goals),flush=True)
    az.close();cz.close();archived.close()
    if Counter(index.calls)!={'BM25F':75,'local_cosine':75}:raise ValueError('extra search calls')
    if max(durations)>30:raise ValueError('warm query exceeded frozen30s budget')
    pairs=read(OLD/'baseline/EVALUATION.json')['positive_pairs'];metric=measure(orders,pairs)
    if arm=='D1' and (metric['retrieved_positive_pairs'],metric['goals_with_positive_at_k'])!=(56,29):
        raise ValueError('D1 did not reproduce expected control')
    fresh_pairs=[('fresh/'+r['goal_id'],r['cid'],r['rid']) for r in read(OLD/'baseline/FRESH-JUDGMENTS.json.gz')['rows'] if r['contribution']=='concrete_material']
    archive=E/('scores-'+arm+'.npz')
    np.savez_compressed(archive,goals=np.asarray(goals),bm25=np.asarray(sparse_rows,dtype='<f8'),
        cosine=np.asarray(dense_rows,dtype='<f8'),order=np.asarray(rows,dtype='<i4'))
    write(target,{'execution_status':'PASS','arm':arm,'document_arm':doc_arm,'generation_id':built['generation_id'],
        'metrics':metric,'supplementary':measure(orders,fresh_pairs),'top8':top8,'scores_sha256':file_sha(archive),
        'actual_lane_calls':dict(Counter(index.calls)),'full_orders_independently_checked':75,
        'D1_bitwise_lane_and_full_order_agreement':bitwise,'full_pool':{'CIDs':18180,'RIDs':18182},
        'warm_query_seconds_max':max(durations),'search_seconds':sum(durations),'elapsed_seconds':time.monotonic()-started,
        'Gemini_calls':0,'CURRENT_writes':0,'new_semantic_judgments':0,'prospective_quality_pass':False})
    print(arm,'FIT8',metric['retrieved_positive_pairs'],'goals8',metric['goals_with_positive_at_k'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('arm',choices=['D1','D1b','Q1']);execute(p.parse_args().arm)
