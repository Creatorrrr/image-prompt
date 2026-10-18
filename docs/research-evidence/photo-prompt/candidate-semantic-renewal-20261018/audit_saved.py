"""Replay saved full rankings/known positives without a model, runtime or cache.

Requires NumPy only for the sealed NPZ arrays. No retrieval call is performed.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import io
import sys
import zipfile

import numpy as np

E = Path(__file__).resolve().parent
ROOT = E.parents[3]
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import read, write, file_sha


def metrics(orders, pairs):
    """Independent direct-count implementation: unknown results are not negatives."""
    assert len(pairs) == len({tuple(p) for p in pairs})
    totals = defaultdict(int)
    hits = defaultdict(int)
    for goal, cid, rid in pairs:
        totals[goal] += 1
        hits[goal] += (cid+'|'+rid) in orders[goal][:8]
    return {'retrieved_positive_pairs': sum(hits.values()), 'positive_pairs': len(pairs),
            'supported_goals': len(totals), 'goals_with_positive_at_k': sum(v > 0 for v in hits.values())}


def audit():
    for freeze in ['FREEZE.json', 'EXECUTION-FREEZE.json']:
        for relative, expected in read(E/freeze)['files'].items():
            assert file_sha(ROOT/relative) == expected, relative
    seal = read(E/'SCORE-ARCHIVE.json')
    assert file_sha(E/'ranking-metadata.json.gz') == seal['metadata_sha256']
    meta = read(E/'ranking-metadata.json.gz')['rows']
    ids = [row['id'] for row in meta]
    assert len(ids) == 18182 and len({row['cid'] for row in meta}) == 18180
    for item in seal['archives'].values():
        assert file_sha(E/item['path']) == item['sha256']
    fresh = [('fresh/'+r['goal_id'], r['cid'], r['rid'])
             for r in read(E/'baseline/FRESH-JUDGMENTS.json.gz')['rows']
             if r['contribution'] == 'concrete_material']
    pairs = read(E/'baseline/EVALUATION.json')['positive_pairs']
    primary = {}; supplementary = {}; checked = 0
    for arm in 'ABC':
        result = read(E/('RESULT-'+arm+'.json'))
        orders = {}
        with zipfile.ZipFile(E/seal['archives'][seal['arms'][arm]]['path']) as archive:
            assert set(archive.namelist()) == set(result['raw_files'])
            for goal in result['top8']:
                name = hashlib.sha256(goal.encode()).hexdigest()+'.npz'
                payload = archive.read(name)
                assert hashlib.sha256(payload).hexdigest() == result['raw_files'][name]
                with np.load(io.BytesIO(payload), allow_pickle=False) as raw:
                    sparse, dense = raw['bm25'], raw['cosine']
                    assert sparse.shape == dense.shape == (len(ids),)
                    assert np.isfinite(sparse).all() and np.isfinite(dense).all()
                    ranks = []
                    for lane, eligible in [(sparse, [i for i,v in enumerate(sparse) if v > 0]), (dense, range(len(ids)))]:
                        ranks.append({i:r for r,i in enumerate(sorted(eligible,key=lambda i:(-float(lane[i]),ids[i])),1)})
                    scores = [sum(1/(10+r[i]) for r in ranks if i in r) for i in range(len(ids))]
                    seen = set(); expected = []
                    for i in sorted(range(len(ids)), key=lambda i:(-scores[i],ids[i])):
                        if meta[i]['cid'] not in seen:
                            seen.add(meta[i]['cid']); expected.append(i)
                    assert expected == list(raw['order'])
                    orders[goal] = [ids[i] for i in expected]
                    assert orders[goal][:8] == [r['id'] for r in result['top8'][goal]]
                    checked += 1
        primary[arm] = metrics(orders, pairs)
        supplementary[arm] = metrics(orders, fresh)
        for key, value in primary[arm].items():
            assert value == result['metrics'][key]
        for key, value in supplementary[arm].items():
            assert value == result['fresh_known_positive_recall'][key]
    write(E/'SAVED-AUDIT.json', {'status':'PASS','full_orders_checked':checked,'primary':primary,
        'supplementary':supplementary,'new_search_calls':0,'new_model_calls':0,
        'runtime_or_research_checkout_required':False,'frozen_inputs_unchanged':True})
    print('PASS', checked, 'archived full orders; primary and supplementary positive counts agree')


if __name__ == '__main__':
    audit()
