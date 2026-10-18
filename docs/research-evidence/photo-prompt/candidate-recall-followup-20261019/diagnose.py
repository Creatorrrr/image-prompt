"""Replay A/C and cross-lane controls; never search or infer embeddings."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import io
import sys
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).parent
OLD = E.parent/'candidate-semantic-renewal-20261018'
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import read, write, file_sha
from photo_candidate_evaluation import measure


def order(meta, sparse, dense):
    ids = [r['id'] for r in meta]
    lanes = []
    for scores, eligible in [(sparse, [i for i,v in enumerate(sparse) if v > 0]),
                             (dense, range(len(meta)))]:
        lanes.append({i:r for r,i in enumerate(sorted(eligible,key=lambda i:(-float(scores[i]),ids[i])),1)})
    fused = [(1/(10+lanes[0][i]) if i in lanes[0] else 0)+1/(10+lanes[1][i]) for i in range(len(meta))]
    seen = set(); result = []
    for i in sorted(range(len(meta)),key=lambda i:(-fused[i],ids[i])):
        if meta[i]['cid'] not in seen:
            seen.add(meta[i]['cid']); result.append(i)
    return result, lanes


def main():
    if (E/'STAGE01.json').exists():
        raise ValueError('diagnosis already sealed')
    seal = read(OLD/'SCORE-ARCHIVE.json')
    for value in seal['archives'].values():
        assert file_sha(OLD/value['path']) == value['sha256']
    meta = read(OLD/'ranking-metadata.json.gz')['rows']
    ids = [r['id'] for r in meta]; positions = {r['id']:i for i,r in enumerate(meta)}
    pairs = read(OLD/'baseline/EVALUATION.json')['positive_pairs']
    goals = sorted(read(OLD/'RESULT-A.json')['top8'])
    reviews = read(OLD/'REVIEW-ACCEPTANCE.json')['reviews']
    arrays = {arm:[] for arm in ['A','C','D1','D2']}
    lane_positions = {}; top8 = {arm:{} for arm in arrays}
    with zipfile.ZipFile(OLD/'saved-scores-A.zip') as az, zipfile.ZipFile(OLD/'saved-scores-C.zip') as cz:
        for goal in goals:
            name = hashlib.sha256(goal.encode()).hexdigest()+'.npz'
            with np.load(io.BytesIO(az.read(name)),allow_pickle=False) as a, np.load(io.BytesIO(cz.read(name)),allow_pickle=False) as c:
                sparse_a,dense_a,sparse_c,dense_c = a['bm25'],a['cosine'],c['bm25'],c['cosine']
                for arm,sparse,dense in [('A',sparse_a,dense_a),('C',sparse_c,dense_c),('D1',sparse_c,dense_a),('D2',sparse_a,dense_c)]:
                    result, lanes = order(meta,sparse,dense)
                    if arm in ['A','C']:
                        assert result == list((a if arm=='A' else c)['order']), (arm,goal)
                    if arm == 'A': lane_positions[goal] = lanes
                    arrays[arm].append(result);top8[arm][goal] = [ids[i] for i in result[:8]]
    metrics = {}; strata = {}; slots = {}
    for arm in arrays:
        metric = measure(top8[arm],pairs)
        assert (metric['retrieved_positive_pairs'],metric['goals_with_positive_at_k']) == {'A':(55,28),'C':(55,29),'D1':(56,29),'D2':(55,29)}[arm]
        metrics[arm] = metric; counts = Counter(); per_slot = Counter()
        for goal,cid,rid in pairs:
            exposed = 'enrich' if reviews.get(cid,{}).get('decision')=='enrich' else 'unchanged'
            counts[exposed+'_pairs'] += 1
            if cid+'|'+rid in top8[arm][goal]:
                counts[exposed+'_hits'] += 1;per_slot[goal.rsplit('/',1)[1]] += 1
        strata[arm] = dict(counts);slots[arm] = dict(per_slot)
    zeros = sorted(g for g,n in metrics['A']['per_goal_hits'].items() if n == 0)
    assert len(zeros)==12
    zero_rows = {}
    for goal in zeros:
        sparse,dense = lane_positions[goal]
        zero_rows[goal] = [{'cid':cid,'rid':rid,'bm25_rank':sparse.get(positions[cid+'|'+rid]),
                            'dense_rank':dense[positions[cid+'|'+rid]]} for g,cid,rid in pairs if g==goal]
    np.savez_compressed(E/'reference-orders.npz', goals=np.asarray(goals), **{k:np.asarray(v,dtype='<i4') for k,v in arrays.items()})
    write(E/'REFERENCE.json',{'metrics':metrics,'strata':strata,'slots':slots,'top8':top8,'zero_goals':zero_rows,
        'full_orders_replayed':len(goals)*4,'new_search_calls':0,'new_embedding_calls':0,
        'diagnostic_only':True,'quality_gate_unchanged':True})
    write(E/'STAGE01.json',{'status':'PASS','main_goals':67,'supplementary_goals':8,'full_orders':300,
        'expected':{k:[v['retrieved_positive_pairs'],v['goals_with_positive_at_k']] for k,v in metrics.items()},
        'positive_pairs':126,'supported_goals':40,'A_zero_goals':zeros,'source_semantic_reviews_added':0,
        'reference_orders_sha256':file_sha(E/'reference-orders.npz')})
    print({k:(v['retrieved_positive_pairs'],v['goals_with_positive_at_k']) for k,v in metrics.items()},flush=True)


if __name__ == '__main__':main()
