"""Exact global BM25F/cosine over only provably necessary shard bodies."""
import heapq
import math
import operator
from bm25f_retrieval import _query_term_weights
from photo_embedding_provider import validate_vector

EPSILON=1e-10


def routing_bounds(reader,query_unit,allowed):
    quant=reader.meta['quantization'];centers=quant['centers'];tables=[]
    for d in range(0,768,2):
        a=[query_unit[d]*v for v in centers[d]];b=[query_unit[d+1]*v for v in centers[d+1]]
        tables.append([a[code&15]+b[code>>4] for code in range(256)])
    codes=memoryview(reader.quant_codes);points={}
    for pos,cid in enumerate(reader.meta['positive_ids']):
        if cid in allowed:
            row=codes[pos*384:(pos+1)*384]
            points[cid]=min(1.0,math.fsum(map(operator.getitem,tables,row))+quant['errors'][pos]+1e-10)
    bounds=[-2.0]*len(reader.meta['nodes'])
    for pos in range(len(bounds)-1,-1,-1):
        node=reader.meta['nodes'][pos]
        bounds[pos]=max((points[cid] for cid in reader.meta['vector_shards'][node['leaf']]['ids'] if cid in points),default=-2.0) if 'leaf' in node else max(bounds[c] for c in node['children'])
    return bounds


def lexical_rank(reader,fields,allowed,limit=384):
    stats=reader.meta['statistics'];policy=stats['policy']
    terms=_query_term_weights(fields,policy=policy,lexicon=stats['lexicon'])
    scores={};matches={}
    for term,query_weight in sorted(terms.items()):
        block=reader.meta['posting_locator'].get(term)
        if block is None:continue
        rows=reader.block('posting',block)[term]
        frequency=stats['document_frequencies'][term];n=stats['document_count'];k=policy['k1']
        idf=math.log(1.0+(n-frequency+0.5)/max(frequency+0.5,1e-12))
        for cid,tf in rows:
            if cid not in allowed:continue
            scores[cid]=scores.get(cid,0.0)+float(query_weight)*idf*((tf*(k+1.0))/(k+tf))
            matches.setdefault(cid,[]).append(term)
    result=[{'document_id':cid,'score':round(score,12),'matched_terms':matches[cid]} for cid,score in scores.items() if score>0]
    result.sort(key=lambda row:(-row['score'],row['document_id']))
    return result[:limit]


def eligible_counts(reader,allowed):
    nodes=reader.meta['nodes'];counts=[0]*len(nodes)
    for pos in range(len(nodes)-1,-1,-1):
        node=nodes[pos]
        counts[pos]=sum(cid in allowed for cid in reader.meta['vector_shards'][node['leaf']]['ids']) if 'leaf' in node else sum(counts[c] for c in node['children'])
    return counts


def cosine_rank(reader,vector,allowed,limit=384,minimum=0.30):
    validate_vector(vector)
    if limit<1:raise ValueError('positive lane limit required')
    if not set(allowed)<=set(reader.meta['positive_ids']):raise ValueError('unknown positive identity')
    norm=math.sqrt(math.sumprod(vector,vector));unit=[v/norm for v in vector]
    counts=eligible_counts(reader,allowed);nodes=reader.meta['nodes'];bounds=routing_bounds(reader,unit,allowed);heap=[];visited=[];skipped=[]
    queue=[(-bounds[0],0)]
    while queue:
        negative,pos=heapq.heappop(queue);bound=-negative
        threshold=heap[0][0] if len(heap)>=limit else minimum
        if not counts[pos]:skipped.append({'node':pos,'reason':'context_ineligible'});continue
        if bound<threshold-EPSILON:
            skipped.extend([{'node':p,'reason':'score_bound' if counts[p] else 'context_ineligible'} for _,p in [(negative,pos)]+queue]);break
        node=nodes[pos]
        if 'leaf' not in node:
            for child in node['children']:heapq.heappush(queue,(-bounds[child],child))
            continue
        leaf=node['leaf'];row=reader.meta['vector_shards'][leaf];values=reader.block('vector',leaf);visited.append(leaf)
        for offset,cid in enumerate(row['ids']):
            if cid not in allowed:continue
            reference=values[offset*768:(offset+1)*768]
            score=math.sumprod(reference,vector)/(math.sqrt(math.sumprod(reference,reference))*norm)
            if score<minimum:continue
            item=(score,-int(cid[5:],16),cid)
            if len(heap)<limit:heapq.heappush(heap,item)
            elif item>heap[0]:heapq.heapreplace(heap,item)
    ranked=sorted(heap,key=lambda r:(-r[0],r[2]))
    proof={'schema':'photo-cosine-shard-proof/v1','limit':limit,'minimum':minimum,
           'threshold':heap[0][0] if len(heap)>=limit else minimum,
           'visited_leaves':sorted(visited),'skipped_nodes':sorted(skipped,key=lambda r:r['node'])}
    return [{'document_id':cid,'score':round(score,9)} for score,_,cid in ranked],proof


def audit_cosine(reader,vector,allowed,hits,proof):
    """Recompute visited scores and independently close the entire routing tree."""
    validate_vector(vector);nodes=reader.meta['nodes'];counts=eligible_counts(reader,allowed)
    if proof.get('schema')!='photo-cosine-shard-proof/v1' or proof['limit']<1:raise ValueError('native pruning proof required')
    visited=set(proof['visited_leaves']);skipped={r['node']:r['reason'] for r in proof['skipped_nodes']}
    if len(visited)!=len(proof['visited_leaves']) or len(skipped)!=len(proof['skipped_nodes']):raise ValueError('duplicate pruning coverage')
    norm=math.sqrt(math.sumprod(vector,vector));unit=[v/norm for v in vector];bounds=routing_bounds(reader,unit,allowed);scored=[];seen_leaves=set();seen_skipped=set()
    def walk(pos):
        node=nodes[pos]
        if pos in skipped:
            reason=skipped[pos];seen_skipped.add(pos)
            bound=bounds[pos]
            if reason=='context_ineligible':
                if counts[pos]:raise ValueError('eligible documents hidden by context pruning')
            elif reason!='score_bound' or bound>=proof['threshold']-EPSILON:raise ValueError('unsafe score pruning')
            return
        if 'leaf' not in node:
            for child in node['children']:walk(child)
            return
        leaf=node['leaf']
        if leaf not in visited:raise ValueError('unaccounted search region')
        seen_leaves.add(leaf);values=reader.block('vector',leaf)
        for offset,cid in enumerate(reader.meta['vector_shards'][leaf]['ids']):
            if cid not in allowed:continue
            reference=values[offset*768:(offset+1)*768]
            score=math.sumprod(reference,vector)/(math.sqrt(math.sumprod(reference,reference))*norm)
            if score>=proof['minimum']:scored.append((cid,score))
    walk(0)
    if seen_leaves!=visited or seen_skipped!=set(skipped):raise ValueError('overlapping/foreign pruning regions')
    scored.sort(key=lambda r:(-r[1],r[0]));ranked=scored[:proof['limit']]
    threshold=ranked[-1][1] if len(ranked)==proof['limit'] else proof['minimum']
    expected=[{'document_id':cid,'score':round(score,9)} for cid,score in ranked]
    if threshold!=proof['threshold'] or expected!=hits:raise ValueError('cosine ranks/threshold differ from verified shard proof')
    return True
