"""Independent archive replay and fixed development gate; no new retrieval/model."""
from pathlib import Path
from collections import defaultdict
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
OLD=E.parent/'candidate-semantic-renewal-20261018'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import read,write,file_sha
from diagnose import order
from build import verify_freeze


def direct_metrics(orders,pairs):
    if len(pairs)!=len({tuple(p) for p in pairs}):raise ValueError('duplicate positive denominator')
    hits=defaultdict(int);totals=defaultdict(int);retrieved=[]
    for goal,cid,rid in pairs:
        totals[goal]+=1
        if cid+'|'+rid in orders[goal][:8]:hits[goal]+=1;retrieved.append([goal,cid+'|'+rid])
    return {'positive_pairs':len(pairs),'supported_goals':len(totals),'retrieved_positive_pairs':sum(hits.values()),
        'goals_with_positive_at_k':len([g for g in totals if hits[g]>0]),
        'per_goal_hits':{g:hits[g] for g in totals},'retrieved':sorted(retrieved)}


if __name__=='__main__':
    verify_freeze()
    for name in ['EVALUATOR-FREEZE.json','Q1-AUTHOR-FREEZE.json','Q1-EXECUTION-FREEZE.json']:
        if not (E/name).exists():continue
        for relative,sha in read(E/name)['files'].items():
            if file_sha(ROOT/relative)!=sha:raise ValueError('frozen artifact changed: '+relative)
    meta=read(OLD/'ranking-metadata.json.gz')['rows'];ids=[r['id'] for r in meta]
    pairs=read(OLD/'baseline/EVALUATION.json')['positive_pairs']
    fresh=[('fresh/'+r['goal_id'],r['cid'],r['rid']) for r in read(OLD/'baseline/FRESH-JUDGMENTS.json.gz')['rows'] if r['contribution']=='concrete_material']
    metrics={};orders_by_arm={};checked=0
    for arm in ['D1','D1b','Q1']:
        if not (E/('RESULT-'+arm+'.json')).exists():continue
        result=read(E/('RESULT-'+arm+'.json'));archive=E/('scores-'+arm+'.npz')
        if file_sha(archive)!=result['scores_sha256']:raise ValueError('score archive changed')
        orders={}
        with np.load(archive,allow_pickle=False) as raw:
            goals=list(raw['goals']);ss=raw['bm25'];ds=raw['cosine'];saved=raw['order']
            if not (ss.shape==ds.shape==(75,18182)) or len(goals)!=len(set(goals)) or set(goals)!=set(read(E/'RESULT-D1.json')['top8']):
                raise ValueError('invalid complete goal/score population')
            if not np.isfinite(ss).all() or not np.isfinite(ds).all():raise ValueError('nonfinite scores')
            for i,g in enumerate(goals):
                recomputed,_=order(meta,ss[i],ds[i])
                if recomputed!=list(saved[i]):raise ValueError('independent exact full rank differs')
                orders[g]=[ids[j] for j in recomputed]
                if orders[g][:8]!=[r['id'] for r in result['top8'][g]]:raise ValueError('saved top8 differs')
                checked+=1
            if arm=='Q1':
                with np.load(E/('scores-'+result['document_arm']+'.npz'),allow_pickle=False) as control:
                    rewritten=set(read(E/'CRITERIA.json')['Q1_goals']);untouched=[i for i,g in enumerate(goals) if g not in rewritten]
                    if list(control['goals'])!=goals or not np.array_equal(ss[untouched],control['bm25'][untouched]) or not np.array_equal(ds[untouched],control['cosine'][untouched]):
                        raise ValueError('Q1 changed undeclared goals/document scores')
        measured=direct_metrics(orders,pairs)
        for key,value in measured.items():
            if value!=result['metrics'][key]:raise ValueError('main metric audit differs: '+key)
        supplementary=direct_metrics(orders,fresh)
        for key,value in supplementary.items():
            if value!=result['supplementary'][key]:raise ValueError('supplementary metric audit differs: '+key)
        metrics[arm]=measured;orders_by_arm[arm]=orders
    doc_selection=read(E/'SELECTED-DOCUMENTS.json')
    candidates=['D1']+(['D1b'] if doc_selection['D1b_eligible'] else [])+(['Q1'] if 'Q1' in metrics else [])
    winner=max(candidates,key=lambda a:(metrics[a]['retrieved_positive_pairs'],metrics[a]['goals_with_positive_at_k'],-['D1','D1b','Q1'].index(a)))
    selected=metrics[winner];minimum=read(E/'CRITERIA.json')['minimum']
    passed=selected['retrieved_positive_pairs']>=minimum['FIT8'] and selected['goals_with_positive_at_k']>=minimum['goals8']
    baseline=read(E/'REFERENCE.json')['top8']['A'];changes={}
    for arm,orders in orders_by_arm.items():
        gain=[];lost=[]
        for g,c,r in pairs:
            value=c+'|'+r;a=value in baseline[g];b=value in orders[g][:8]
            if a and not b:lost.append([g,c,r])
            if b and not a:gain.append([g,c,r])
        changes[arm]={'gained':gain,'lost':lost,'net':len(gain)-len(lost)}
    write(E/'DEVELOPMENT-QUALIFICATION.json',{'status':'PASS' if passed else 'HOLD','winner':winner,'metrics':metrics,'changes':changes,
        'full_orders_independently_replayed':checked,'fixed_gate':minimum,'new_request_confirmation_required':passed,
        'operating_promotion_allowed':False,'new_search_calls':0,'new_embedding_calls':0,
        'new_semantic_judgments':0,'CURRENT_writes':0})
    print('development', 'PASS' if passed else 'HOLD',winner,selected['retrieved_positive_pairs'],selected['goals_with_positive_at_k'],flush=True)
