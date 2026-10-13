"""Offline derived layout: global postings, lossless vectors and source locators."""
from array import array
import gzip
import hashlib
import math
from pathlib import Path
import sys
import zlib
import photo_candidate_corpus as c
import photo_global_index as old_index
from photo_embedding_provider import SPACE, atomic

SCHEMA = 'photo-candidate-search-layout/v1'
MANIFEST = 'photo_candidate_search.json'
DIRECTORY = 'photo_candidate_search_shards'


def guard_record(record):
    content = record['content']
    # Keep all filtering fields; large realization bodies belong to the payload.
    removed = {'components', 'semantics', 'concept_candidate', 'render_requirements', 'render_hard_gates',
               'paraphrases', 'definition', 'definitions_by_topic', 'relations', 'concept_units',
               'manifestations', 'provenance', 'acceptance', 'failure_modes', 'confounders'}
    value = {key: value for key, value in record.items() if key not in {'content', 'provenance'}}
    value['content'] = {key: value for key, value in content.items() if key not in removed}
    return value


def _tf(document, term, lexical):
    value = 0.0
    for name, config in sorted(lexical['policy']['fields'].items()):
        field = document['fields'].get(name) or {}
        frequency = float(field.get('term_frequencies', {}).get(term, 0))
        if frequency <= 0:
            continue
        length = float(field.get('length', 0) or 0)
        average = float(lexical['average_field_lengths'].get(name, 0) or 0)
        ratio = length / average if average > 0 else 1.0
        value += config['weight'] * frequency / max(1.0 - config['b'] + config['b'] * ratio, 1e-12)
    return value


def build(assets, corpus, vectors, *, leaf_size=32, activate=False):
    """Never invokes a provider. Default output cannot replace the live manifest."""
    assets = Path(assets)
    old_index.validate(vectors, corpus)
    lexical = old_index.lexical(corpus)
    identity = c.digest({'schema': SCHEMA, 'source': c.digest(corpus), 'vectors': c.digest(vectors),
                         'leaf_size': leaf_size, 'lexical_policy': old_index.POLICY})
    directory = assets / DIRECTORY / identity
    directory.mkdir(parents=True, exist_ok=True)
    members = {}

    def write(name, raw, count):
        path = directory / name
        path.write_bytes(raw)
        row = {'path': str(path.relative_to(assets)), 'sha256': hashlib.sha256(raw).hexdigest(),
               'bytes': len(raw), 'count': count}
        members[name] = row
        return row

    def json_file(name, value, count):
        return write(name, gzip.compress(c.canonical_bytes(value), mtime=0), count)

    ids = sorted(vectors['entries'])
    raw_vectors = {cid: vectors['entries'][cid]['vector'] for cid in ids}
    units = {}
    for cid, values in raw_vectors.items():
        norm = math.sqrt(math.sumprod(values, values))
        units[cid] = [x / norm for x in values]
    leaves = []; nodes = []

    def partition(keys):
        pos = len(nodes); nodes.append(None)
        center = [math.fsum(units[cid][d] for cid in keys) / len(keys) for d in range(SPACE['dimensions'])]
        norm = math.sqrt(math.sumprod(center, center))
        if norm:
            center = [x/norm for x in center]
            radius_cos = min(math.sumprod(center, units[cid]) for cid in keys) - 1e-12
        else:
            radius_cos = -1.0
        node = {'center': center, 'radius_cos': max(-1.0, radius_cos), 'count': len(keys)}
        if len(keys) <= leaf_size:
            leaf = len(leaves)
            values = array('d', (value for cid in keys for value in raw_vectors[cid]))
            if sys.byteorder != 'little': values.byteswap()
            shard = write(f'vector-{leaf:05d}.f64.z', zlib.compress(values.tobytes()), len(keys))
            leaves.append({**shard, 'ids': keys})
            node['leaf'] = leaf
        else:
            first = units[keys[0]]
            a = min(keys, key=lambda cid: (math.sumprod(first, units[cid]), cid))
            b = min(keys, key=lambda cid: (math.sumprod(units[a], units[cid]), cid))
            axis = [x-y for x,y in zip(units[a], units[b])]
            ordered = sorted(keys, key=lambda cid: (math.sumprod(units[cid], axis), cid))
            middle = len(keys)//2
            node['children'] = [partition(ordered[:middle]), partition(ordered[middle:])]
        nodes[pos] = node
        return pos

    partition(ids)
    payloads = []; locators = {}; guards = {}; record_hashes = {}; blobs = {}; profile_terms = []
    all_ids = sorted(corpus['candidates'])
    for offset in range(0, len(all_ids), 64):
        keys = all_ids[offset:offset+64]; block = len(payloads)
        payloads.append(json_file(f'payload-{block:05d}.json.gz', {cid:corpus['candidates'][cid] for cid in keys}, len(keys)))
        for cid in keys:
            record = corpus['candidates'][cid]; locators[cid] = block; guards[cid] = guard_record(record)
            record_hashes[cid] = c.digest(record)
            blobs[cid] = ' '.join(v for values in old_index.fields(record).values() for v in values)
            if record['record_kind'] == 'visual_profile':
                for field in ('exact_terms', 'project_glossary_aliases'):
                    for term in record['content'].get('activation', {}).get(field, []):
                        profile_terms.append({'term': term, 'term_key': term.casefold(), 'profile_id': cid,
                                              'term_type': 'exact_term' if field == 'exact_terms' else 'project_glossary_alias'})
    profile_terms.sort(key=lambda r:(r['term_key'],r['profile_id'],r['term_type']))
    postings = {}
    for cid, document in lexical['documents'].items():
        terms = set().union(*(set(row['term_frequencies']) for row in document['fields'].values()))
        for term in terms: postings.setdefault(term, []).append([cid, _tf(document, term, lexical)])
    posting_shards = []; posting_locator = {}
    terms = sorted(postings)
    for offset in range(0, len(terms), 128):
        keys = terms[offset:offset+128]; block = len(posting_shards)
        posting_shards.append(json_file(f'postings-{block:05d}.json.gz', {term:sorted(postings[term]) for term in keys}, len(keys)))
        posting_locator.update({term:block for term in keys})
    stats = {key:value for key,value in lexical.items() if key != 'documents'}
    metadata = {'corpus_sha256': c.digest(corpus), 'guards': guards, 'positive_blobs': blobs,
                'vector_recipes': {cid:{key:row[key] for key in ('recipe','text_sha256','embedding_execution') if key in row}
                                   for cid,row in vectors['entries'].items()},
                'record_sha256': record_hashes, 'payload_locator': locators, 'payload_shards': payloads,
                'nodes': nodes, 'vector_shards': leaves, 'positive_ids': ids,
                'statistics': stats, 'posting_locator': posting_locator, 'posting_shards': posting_shards,
                'profile_lookup': profile_terms, 'slot_catalog': corpus['slot_catalog'],
                'slot_bindings': corpus['slot_bindings'], 'policies': corpus['policies']}
    metadata_member = json_file('metadata.json.gz', metadata, len(ids))
    manifest = {'schema': SCHEMA, 'space': SPACE, 'corpus_sha256': c.digest(corpus),
                'index_source_sha256': c.digest(vectors), 'layout_id': identity, 'metadata': metadata_member,
                'shards': [row for name,row in sorted(members.items()) if name != 'metadata.json.gz'],
                'lexical_recipe': lexical['recipe_version'], 'endianness': 'little', 'vector_type': 'float64'}
    target = assets / (MANIFEST if activate else 'photo_candidate_search.staging.json')
    atomic(target, manifest)
    return manifest


def upper_bound(node, query_unit):
    """Spherical-cap maximum; outward rounding protects score/tie boundaries."""
    a = max(-1.0, min(1.0, math.sumprod(node['center'], query_unit)))
    b = node['radius_cos']
    if b <= -1 or a >= b: return 1.0
    return min(1.0, a*b + math.sqrt(max(0.0, 1-a*a))*math.sqrt(max(0.0, 1-b*b)) + 1e-11)


def verify(assets, corpus, manifest, vectors=None):
    """Offline complete source/statistics/boundary verification, not a request path."""
    assets=Path(assets)
    if manifest.get('schema')!=SCHEMA or manifest.get('space')!=SPACE or manifest.get('corpus_sha256')!=c.digest(corpus):
        raise ValueError('layout source/space mismatch')
    def read(row):
        p=assets/row['path']
        if p.is_symlink() or assets.resolve() not in p.resolve().parents: raise ValueError('unsafe layout member')
        raw=p.read_bytes()
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']: raise ValueError('layout member checksum mismatch')
        return raw
    for row in manifest['shards']: read(row)
    meta=c.decode(gzip.decompress(read(manifest['metadata'])))
    expected={cid for cid,r in corpus['candidates'].items() if r['record_kind'] in old_index.POSITIVE_KINDS}
    if set(meta['positive_ids'])!=expected or len(meta['positive_ids'])!=len(expected): raise ValueError('positive coverage mismatch')
    if meta['slot_catalog']!=corpus['slot_catalog'] or meta['slot_bindings']!=corpus['slot_bindings'] or meta['policies']!=corpus['policies']: raise ValueError('role/policy preservation mismatch')
    seen=set()
    for block,row in enumerate(meta['payload_shards']):
        payload=c.decode(gzip.decompress(read(row)))
        if len(payload)!=row['count'] or seen&set(payload): raise ValueError('duplicate payload owner/count')
        seen.update(payload)
        for cid,record in payload.items():
            if record!=corpus['candidates'][cid] or meta['payload_locator'][cid]!=block or meta['record_sha256'][cid]!=c.digest(record): raise ValueError('payload locator/source changed')
            if meta['guards'][cid]!=guard_record(record): raise ValueError('guard projection changed')
    if seen!=set(corpus['candidates']): raise ValueError('payload coverage mismatch')
    leaf_paths={}
    def walk(pos,parents):
        node=meta['nodes'][pos]
        if len(node['center'])!=SPACE['dimensions'] or not all(math.isfinite(v) for v in node['center']) or not -1<=node['radius_cos']<=1: raise ValueError('invalid cap')
        if 'leaf' in node:
            if node['leaf'] in leaf_paths: raise ValueError('duplicate leaf owner')
            leaf_paths[node['leaf']]=parents+[pos]
            if node['count']!=meta['vector_shards'][node['leaf']]['count']: raise ValueError('leaf count mismatch')
        else:
            if len(node['children'])!=2 or any(p<=pos or p>=len(meta['nodes']) for p in node['children']): raise ValueError('invalid tree topology')
            if sum(meta['nodes'][p]['count'] for p in node['children'])!=node['count']: raise ValueError('internal count mismatch')
            for p in node['children']: walk(p,parents+[pos])
    walk(0,[]);seen=set()
    for leaf,row in enumerate(meta['vector_shards']):
        values=array('d'); values.frombytes(zlib.decompress(read(row)))
        if sys.byteorder!='little': values.byteswap()
        if len(values)!=row['count']*SPACE['dimensions'] or len(row['ids'])!=row['count'] or seen&set(row['ids']): raise ValueError('vector owner/count mismatch')
        seen.update(row['ids'])
        for offset,cid in enumerate(row['ids']):
            vector=values[offset*768:(offset+1)*768].tolist(); old_index.validate_vector(vector)
            if vectors is not None and vector!=vectors['entries'][cid]['vector']: raise ValueError('vector precision loss')
            recipe,text=old_index.text(corpus['candidates'][cid]);ref=meta.get('vector_recipes',{}).get(cid)
            if not ref or ref['recipe']!=recipe or ref['text_sha256']!=hashlib.sha256(text.encode()).hexdigest(): raise ValueError('vector text/recipe mismatch')
            norm=math.sqrt(math.sumprod(vector,vector));unit=[v/norm for v in vector]
            for pos in leaf_paths[leaf]:
                node=meta['nodes'][pos]
                if node['radius_cos']>-1 and math.sumprod(node['center'],unit)<node['radius_cos']-1e-13: raise ValueError('unsafe routing cap')
    if seen!=expected: raise ValueError('vector coverage mismatch')
    lexical=old_index.lexical(corpus)
    if meta['statistics']!={k:v for k,v in lexical.items() if k!='documents'}: raise ValueError('global lexical statistics mismatch')
    seen_terms=set()
    for block,row in enumerate(meta['posting_shards']):
        postings=c.decode(gzip.decompress(read(row)))
        if seen_terms&set(postings) or len(postings)!=row['count']: raise ValueError('duplicate posting owner/count')
        seen_terms.update(postings)
        for term,rows in postings.items():
            if meta['posting_locator'][term]!=block or len(rows)!=lexical['document_frequencies'][term]: raise ValueError('posting coverage mismatch')
            if len({cid for cid,tf in rows})!=len(rows): raise ValueError('duplicate lexical vote')
            for cid,tf in rows:
                if tf!=_tf(lexical['documents'][cid],term,lexical): raise ValueError('posting TF changed scoring arithmetic')
    if seen_terms!=set(lexical['document_frequencies']) or seen_terms!=set(meta['posting_locator']): raise ValueError('missing term postings')
    return {'verified':True,'candidates':len(corpus['candidates']),'positive':len(expected),'vector_shards':len(meta['vector_shards']),
            'payload_shards':len(meta['payload_shards']),'posting_shards':len(meta['posting_shards']),'nodes':len(meta['nodes']),
            'metadata_bytes':manifest['metadata']['bytes'],'provider_calls':0}
