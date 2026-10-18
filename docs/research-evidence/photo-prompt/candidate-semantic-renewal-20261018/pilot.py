"""Whole-pool A/B/C in the installed local runtime. No query/rank tuning."""
from pathlib import Path
from collections import Counter
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).parent
S = ROOT/'skills/photo-prompt-image-generator'
CACHE = Path.home()/'.cache/image-prompt/candidate-semantic-renewal-20261018'
sys.path.insert(0, str(S/'scripts'))
from photo_candidate_authoring import Source, read, write, file_sha, digest
from photo_candidate_review import validate
from photo_candidate_documents import project, field_index
from photo_candidate_evaluation import measure, qualified
from photo_installed_h_f2 import default_store, release
config = read(S/'retrieval-runtime.json')
NATIVE, _, _ = release(default_store(), config['generation_id'])
sys.path.insert(0, str(NATIVE/'scripts'))
from photo_h_f2_generation import Generation
from photo_h_f2_search import Index
from photo_h_f2_encoder import LocalEncoder
import photo_recall_first as rf
import numpy as np


def check_freeze():
    for relative, expected in read(E/'FREEZE.json')['files'].items():
        if file_sha(ROOT/relative) != expected:
            raise ValueError('frozen input changed: '+relative)


def collect_reviews(source):
    files = sorted((E/'reviews').glob('luna-*/*.json'))
    reviews = {}
    for path in files:
        row = read(path);cid = row['candidate_id']
        if cid in reviews:
            raise ValueError('duplicate reviewed CID')
        validate(row, source.record(cid), source.header['slot_catalog'])
        reviews[cid] = row
    expected = set(read(E/'PILOT.json')['candidates'])
    if set(reviews) != expected:
        raise ValueError('exactly96 complete CID reviews required')
    accepted = read(E/'REVIEW-ACCEPTANCE.json')
    for cid, row in reviews.items():
        if accepted['reviews'][cid]['sha256'] != digest(row):
            raise ValueError('parent-reviewed annotation changed')
    if accepted['status'] != 'PASS':
        raise ValueError('parent source comparison incomplete')
    return reviews


def corpus(generation, arm):
    source = Source(S/'candidate-authoring/v1')
    selected = set(read(E/'PILOT.json')['candidates'])
    reviews = collect_reviews(source) if arm == 'C' else {}
    original = read(generation.root/'documents.json.gz')['rows']
    field_documents = read(generation.root/'field-documents.json.gz')['rows']
    compiled = []
    for meta, document, fields in zip(generation.metadata, original, field_documents, strict=True):
        if not (meta['id'] == document['id'] == fields['id'] and
                meta['source_sha256'] == document['source_sha256'] == fields['source_sha256']):
            raise ValueError('mixed source or RID document')
        if meta['cid'] in selected and arm != 'A':
            record = source.record(meta['cid'])
            source_document = next(d for d in rf.documents(record) if d['rid'] == meta['rid'])
            result = project(document['text'], fields['fields'], record, meta['rid'], source_document,
                arm=arm, selected=True, review=reviews.get(meta['cid']), catalog=source.header['slot_catalog'])
        else:
            result = {'text': document['text'], 'text_sha256': document['text_sha256'],
                'fields': fields['fields'], 'additions': [], 'source_sha256': meta['source_sha256'], 'rid': meta['rid']}
        if not result['text'].startswith(document['text']):
            raise ValueError('original D lookup/prefix was replaced')
        compiled.append({**result, 'id': meta['id'], 'cid': meta['cid']})
    statistics = field_index(compiled, generation.fields['fields'])
    if arm == 'A' and any(statistics[key] != generation.fields[key] for key in statistics):
        raise ValueError('independently rebuilt baseline F2 statistics differ')
    return compiled, statistics


def matrix_for(generation, documents, arm):
    path = CACHE/('vectors-'+arm+'.f64')
    if path.exists():
        raise ValueError('preserve existing vector output; use its checkpoint instead of overwriting')
    matrix = np.memmap(path, dtype='<f8', mode='w+', shape=(len(documents),768))
    matrix[:] = generation.index().matrix
    old_documents = read(generation.root/'documents.json.gz')['rows']
    changed = [i for i,(before,after) in enumerate(zip(old_documents,documents,strict=True)) if before['text'] != after['text']]
    cache = CACHE/'document-embedding-cache';cache.mkdir(exist_ok=True)
    unique = {documents[i]['text_sha256']: documents[i]['text'] for i in changed}
    missing = [(key,text) for key,text in unique.items() if not (cache/(key+'.json.gz')).exists()]
    inferred = 0
    if missing:
        with LocalEncoder(S) as encoder:
            if encoder.binding != generation.binding:
                raise ValueError('local model binding changed')
            for offset in range(0,len(missing),8):
                part = missing[offset:offset+8]
                rows = encoder.encode([text for _,text in part], 'document')
                for (key,text),row in zip(part,rows,strict=True):
                    rf.check_embedding(row,generation.binding,text,'document')
                    write(cache/(key+'.json.gz'), {'text':text,'row':row,'binding':generation.binding})
                    inferred += 1
                print('local document inputs',arm,min(offset+8,len(missing)),len(missing),flush=True)
    for i in changed:
        document = documents[i];item = read(cache/(document['text_sha256']+'.json.gz'))
        if item['text'] != document['text'] or item['binding'] != generation.binding:
            raise ValueError('foreign cached document input')
        rf.check_embedding(item['row'],generation.binding,document['text'],'document')
        matrix[i] = np.asarray(item['row']['vector'],dtype=np.float64)
    matrix.flush()
    return matrix, {'changed_RIDs': len(changed), 'unique_changed_inputs': len(unique), 'new_local_inference': inferred,
                    'exact_input_cache_reuse': len(unique)-inferred, 'vector_sha256':file_sha(path)}


def execute(arm):
    check_freeze()
    if (E/('RESULT-'+arm+'.json')).exists():
        raise ValueError('arm already evaluated; do not retry to optimize its outcome')
    started = time.monotonic()
    generation = Generation(default_store(),config['generation_id'],full=True)
    documents, statistics = corpus(generation,arm)
    write(CACHE/('documents-'+arm+'.json.gz'), {'rows':documents})
    write(CACHE/('fields-'+arm+'.json.gz'), statistics)
    matrix, inference = matrix_for(generation,documents,arm)
    index = Index(generation.metadata,statistics,matrix)
    queries = read(E/'baseline/QUERIES.json.gz')
    if queries['binding'] != generation.binding:
        raise ValueError('query model space differs')
    goal_queries = queries['goals']
    fresh_queries = read(E/'baseline/FRESH-QUERIES.json.gz')['rows']
    fresh_goals = read(E/'baseline/FRESH-GOALS.json.gz')['goals']
    all_queries = {**goal_queries, **{'fresh/'+g['goal_id']:{'text':g['query'],'row':fresh_queries[g['goal_id']]} for g in fresh_goals}}
    orders = {};files = {};top8 = {}
    positions = {row['id']:i for i,row in enumerate(generation.metadata)}
    raw = CACHE/'raw'/arm;raw.mkdir(parents=True,exist_ok=True)
    for key, query in sorted(all_queries.items()):
        rf.check_embedding(query['row'],generation.binding,query['text'],'query')
        result = index.search(query['text'],query['row'],generation.binding)
        if result['lane_calls'] != {'BM25F':1,'local_cosine':1} or result['considered_CIDs'] != 18180 or result['considered_RIDs'] != 18182:
            raise ValueError('search count or global candidate population changed')
        path = raw/(rf.sha(key)+'.npz')
        with path.open('wb') as stream:
            np.savez_compressed(stream,bm25=np.asarray(result['bm25'],dtype='<f8'),cosine=result['cosine'],
                order=np.asarray([positions[row['id']] for row in result['order']],dtype='<i4'))
        files[path.name] = file_sha(path)
        orders[key] = [row['id'] for row in result['order']]
        top8[key] = result['order'][:8]
    if Counter(index.calls) != {'BM25F':len(all_queries),'local_cosine':len(all_queries)}:
        raise ValueError('extra actual lane execution')
    evaluation = read(E/'baseline/EVALUATION.json')
    metrics = measure(orders,evaluation['positive_pairs'])
    if arm == 'A' and (metrics['retrieved_positive_pairs'],metrics['goals_with_positive_at_k']) != (55,28):
        raise ValueError('installed baseline is not expected55/126,28/40')
    prior_fresh = read(E/'baseline/FRESH-JUDGMENTS.json.gz')['rows']
    fresh_pairs = [('fresh/'+row['goal_id'],row['cid'],row['rid']) for row in prior_fresh if row['contribution']=='concrete_material']
    fresh_metric = measure(orders,fresh_pairs)
    result = {'status':'PASS','arm':arm,'metrics':metrics,'fresh_known_positive_recall':fresh_metric,
        'fresh_scope':'same prior4 synthetic requests/8goals; unjudged returned connections remain unknown',
        'inference':inference,'new_query_inference':0,'actual_lane_calls':dict(Counter(index.calls)),
        'queries':len(all_queries),'top8':top8,'raw_files':files,'full_pool':{'CIDs':18180,'RIDs':18182},
        'compiled_documents_sha256':file_sha(CACHE/('documents-'+arm+'.json.gz')),
        'fields_sha256':file_sha(CACHE/('fields-'+arm+'.json.gz')),
        'elapsed_seconds':time.monotonic()-started,'CURRENT_changed':False,'Gemini_calls':0}
    write(E/('RESULT-'+arm+'.json'),result)
    print('arm',arm,'FIT8',metrics['retrieved_positive_pairs'],'goals8',metrics['goals_with_positive_at_k'],flush=True)


def audit():
    check_freeze()
    generation = Generation(default_store(),config['generation_id'],full=True)
    ids = [row['id'] for row in generation.metadata]
    evaluation = read(E/'baseline/EVALUATION.json')
    results = {};orders_by_arm = {}
    for arm in 'ABC':
        saved = read(E/('RESULT-'+arm+'.json'));orders = {}
        for goal in saved['top8']:
            path = CACHE/'raw'/arm/(rf.sha(goal)+'.npz')
            if file_sha(path) != saved['raw_files'][path.name]:
                raise ValueError('saved scores changed')
            with np.load(path) as raw:
                sparse,dense,order = raw['bm25'],raw['cosine'],list(raw['order'])
                if not (sparse.shape == dense.shape == (len(ids),)) or not np.isfinite(sparse).all() or not np.isfinite(dense).all():
                    raise ValueError('invalid saved score population')
                lr = {i:r for r,i in enumerate(sorted((i for i,s in enumerate(sparse) if s>0),key=lambda i:(-float(sparse[i]),ids[i])),1)}
                dr = {i:r for r,i in enumerate(sorted(range(len(ids)),key=lambda i:(-float(dense[i]),ids[i])),1)}
                score = [(1/(10+lr[i]) if i in lr else 0)+1/(10+dr[i]) for i in range(len(ids))]
                seen = set();expected = []
                for i in sorted(range(len(ids)),key=lambda i:(-score[i],ids[i])):
                    cid = generation.metadata[i]['cid']
                    if cid not in seen:
                        seen.add(cid);expected.append(i)
                if order != expected:
                    raise ValueError('independent exact RRF order differs')
                orders[goal] = [ids[i] for i in order]
                if orders[goal][:8] != [row['id'] for row in saved['top8'][goal]]:
                    raise ValueError('saved top8 differs')
        measured = measure(orders,evaluation['positive_pairs'])
        if measured != saved['metrics']:
            raise ValueError('independent metric audit differs')
        results[arm] = measured;orders_by_arm[arm] = orders
    verdict = qualified(results['A'],results['B'],results['C'],read(E/'CRITERIA.json'))
    changes = {}
    for before,after in [('A','B'),('B','C'),('A','C')]:
        lost = [];gained = []
        for goal,cid,rid in evaluation['positive_pairs']:
            key = cid+'|'+rid
            a = key in orders_by_arm[before][goal][:8];b = key in orders_by_arm[after][goal][:8]
            if a and not b: lost.append([goal,cid,rid])
            if b and not a: gained.append([goal,cid,rid])
        changes[before+'-'+after] = {'gained':gained,'lost':lost,'net':len(gained)-len(lost)}
    write(E/'QUALIFICATION.json',{'status':verdict['status'],'criteria':verdict,'metrics':results,'changes':changes,
        'independent_full_orders_checked':sum(len(v) for v in orders_by_arm.values()),
        'new_semantic_judgments':0,'source_core_mutations':0,'additional_audit_search_calls':0,
        'Gemini_calls':0,'CURRENT_changed':False,'full_rollout_allowed':verdict['status']=='PASS'})
    print(json.dumps(verdict,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['A','B','C','audit'])
    args = parser.parse_args()
    CACHE.mkdir(exist_ok=True)
    audit() if args.command == 'audit' else execute(args.command)
