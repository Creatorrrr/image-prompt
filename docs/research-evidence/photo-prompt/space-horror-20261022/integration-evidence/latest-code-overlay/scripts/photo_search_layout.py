"""Offline derived layout: global postings, lossless vectors and source locators."""
from array import array
import base64
from bisect import bisect_right, bisect_left
import gzip
import hashlib
import math
from pathlib import Path
from collections.abc import Mapping, Sequence
import struct
import sys
import zlib
import photo_candidate_corpus as c
import photo_global_index as documents
from photo_embedding_provider import SPACE, atomic, validate_space, validate_execution

SCHEMA = 'photo-candidate-search-layout/v1'
MANIFEST = 'photo_candidate_search.json'
DIRECTORY = 'photo_candidate_search_shards'
ROUTING_RECIPE = 'photo-scalar-error-bounds/v2'
VECTOR_CODEC = 'photo-lossless-vector-extents/v2'
POSTING_CODEC = 'photo-ordinal-tf-postings/v1'
POSTING_ROW = struct.Struct('<Id')


class PostingRows(Sequence):
    def __init__(self, body, ids): self.body=body;self.ids=ids
    def __len__(self): return len(self.body)//POSTING_ROW.size
    def __iter__(self):
        for ordinal,tf in POSTING_ROW.iter_unpack(self.body): yield self.ids[ordinal],tf
    def __getitem__(self, pos):
        if isinstance(pos,slice): return tuple(self)[pos]
        if pos<0:pos+=len(self)
        if not 0<=pos<len(self):raise IndexError(pos)
        ordinal,tf=POSTING_ROW.unpack_from(self.body,pos*POSTING_ROW.size)
        return self.ids[ordinal],tf


class PostingPage(Mapping):
    """Immutable decoded bytes; candidate identities are shared metadata ordinals."""
    def __init__(self, raw, ids):
        if len(raw)<4:raise ValueError('truncated posting header')
        length=struct.unpack_from('<I',raw)[0]
        if length>len(raw)-4:raise ValueError('truncated posting header')
        header=c.decode(raw[4:4+length]);self.body=memoryview(raw)[4+length:];self.ids=ids
        self.ranges={};end=0
        for term,offset,count in header:
            if term in self.ranges or offset!=end or count<1:raise ValueError('invalid posting range')
            end=offset+count*POSTING_ROW.size
            self.ranges[term]=(offset,end)
        if end!=len(self.body):raise ValueError('posting body coverage mismatch')
        for ordinal,tf in POSTING_ROW.iter_unpack(self.body):
            if ordinal>=len(ids) or not math.isfinite(tf) or tf<=0:raise ValueError('invalid posting value')
        self.cache_weight=len(raw)+sys.getsizeof(self)+sys.getsizeof(self.body)+sys.getsizeof(self.ranges)+sum(sys.getsizeof(k)+sys.getsizeof(v)+sum(sys.getsizeof(n) for n in v) for k,v in self.ranges.items())
    def __len__(self):return len(self.ranges)
    def __iter__(self):return iter(self.ranges)
    def __getitem__(self,term):
        start,end=self.ranges[term]
        return PostingRows(self.body[start:end],self.ids)


def posting_bytes(postings, ordinals):
    header=[];body=bytearray()
    for term,rows in sorted(postings.items()):
        header.append([term,len(body),len(rows)])
        for cid,tf in sorted(rows):body.extend(POSTING_ROW.pack(ordinals[cid],tf))
    raw=c.canonical_bytes(header)
    return zlib.compress(struct.pack('<I',len(raw))+raw+body)


def guard_record(record, corpus=None):
    content = record['content']
    # Keep all filtering fields; large realization bodies belong to the payload.
    removed = {'components', 'semantics', 'concept_candidate', 'render_requirements', 'render_hard_gates',
               'paraphrases', 'definition', 'definitions_by_topic', 'relations', 'concept_units',
               'manifestations', 'provenance', 'acceptance', 'failure_modes', 'confounders',
               'role_evidence', 'semantic_review'}
    value = {key: value for key, value in record.items() if key not in {'content', 'provenance'}}
    value['content'] = {key: value for key, value in content.items() if key not in removed}
    import photo_semantic_evidence
    proof = photo_semantic_evidence.compact(record, corpus)
    if proof is not None:
        # Condition provenance lives in the sealed source/member guard sets;
        # never flatten v2 parent and child CID namespaces during projection.
        value['_semantic_evidence_guard'] = proof
        base = photo_semantic_evidence.with_projection(record, record['effects'])
        value['effects'] = {**base, **({'realizations':record['effects']['realizations']}
                                      if record['effects'].get('realizations') else {})}
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


def build(assets, corpus, vectors, *, leaf_size=8, activate=False):
    """Never invokes a provider. Default output cannot replace the live manifest."""
    assets = Path(assets)
    c.validate(corpus)
    documents.validate(vectors, corpus)
    lexical = documents.lexical(corpus)
    identity = c.digest({'schema': SCHEMA, 'routing_recipe': ROUTING_RECIPE, 'vector_codec': VECTOR_CODEC, 'posting_codec':POSTING_CODEC, 'source': c.digest(corpus), 'vectors': c.digest(vectors),
                         'leaf_size': leaf_size, 'lexical_policy': documents.POLICY})
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
    leaves = []; nodes = [];vector_parts=[]

    def partition(keys):
        pos = len(nodes); nodes.append(None)
        node = {'count': len(keys)}
        if len(keys) <= leaf_size:
            leaf = len(leaves)
            values = array('d', (value for cid in keys for value in raw_vectors[cid]))
            if sys.byteorder != 'little': values.byteswap()
            raw=zlib.compress(values.tobytes());vector_parts.append(raw)
            leaves.append({'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'count':len(keys),'ids':keys,'encoding':'f64_le'})
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
    # Each leaf is a seekable, independently checksummed compressed extent.
    for first in range(0,len(leaves),64):
        pack=write(f'vector-pack-{first//64:05d}.bin',b''.join(vector_parts[first:first+64]),sum(r['count'] for r in leaves[first:first+64]))
        offset=0
        for row in leaves[first:first+64]:row.update(path=pack['path'],offset=offset);offset+=row['bytes']
    del vector_parts
    quantization = scalar_quantization(ids, units)
    payloads = []; locators = {}; guards = {}; record_hashes = {}; blobs = {}; profile_terms = []
    all_ids = sorted(corpus['candidates'])
    for offset in range(0, len(all_ids), 64):
        keys = all_ids[offset:offset+64]; block = len(payloads)
        payloads.append(json_file(f'payload-{block:05d}.json.gz', {cid:corpus['candidates'][cid] for cid in keys}, len(keys)))
        for cid in keys:
            record = corpus['candidates'][cid]; locators[cid] = block; guards[cid] = guard_record(record, corpus)
            record_hashes[cid] = c.digest(record)
            blobs[cid] = ' '.join(v for values in documents.fields(record).values() for v in values)
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
    ordinals={cid:i for i,cid in enumerate(ids)}
    terms = sorted(postings)
    for offset in range(0, len(terms), 128):
        keys = terms[offset:offset+128]; block = len(posting_shards)
        posting_shards.append(write(f'postings-{block:05d}.posting.z',posting_bytes({term:postings[term] for term in keys},ordinals),len(keys)))
        posting_locator.update({term:block for term in keys})
    stats = {key:value for key,value in lexical.items() if key != 'documents'}
    metadata = {'corpus_sha256': c.digest(corpus), 'guards': guards, 'positive_blobs': blobs,
                'vector_recipes': {cid:{key:row[key] for key in ('recipe','text_sha256','embedding_execution') if key in row}
                                   for cid,row in vectors['entries'].items()},
                'record_sha256': record_hashes, 'payload_locator': locators, 'payload_shards': payloads,
                'nodes': nodes, 'vector_shards': leaves, 'positive_ids': ids, 'quantization': quantization,
                'statistics': stats, 'posting_locator': posting_locator, 'posting_shards': posting_shards,
                'profile_lookup': profile_terms, 'slot_catalog': corpus['slot_catalog'],
                'slot_bindings': corpus['slot_bindings'], 'policies': corpus['policies']}
    metadata_member = json_file('metadata.json.gz', metadata, len(ids))
    manifest = {'schema': SCHEMA, 'routing_recipe': ROUTING_RECIPE, 'vector_codec': VECTOR_CODEC, 'posting_codec':POSTING_CODEC, 'space': vectors['space'], 'corpus_sha256': c.digest(corpus),
                'index_source_sha256': c.digest(vectors), 'layout_id': identity, 'metadata': metadata_member,
                'shards': [row for name,row in sorted(members.items()) if name != 'metadata.json.gz'],
                'lexical_recipe': lexical['recipe_version'], 'endianness': 'little', 'vector_type': 'float64'}
    target = assets / (MANIFEST if activate else 'photo_candidate_search.staging.json')
    atomic(target, manifest)
    return manifest


def scalar_quantization(ids,units):
    """4-bit coordinates plus exact residual norms, not full-precision vectors."""
    stride=SPACE['dimensions']//2;codes=bytearray(len(ids)*stride);centers=[];errors=[0.0]*len(ids)
    for d in range(SPACE['dimensions']):
        ordered=sorted(units[cid][d] for cid in ids);n=len(ordered)
        row=[math.fsum(ordered[i*n//16:max(i*n//16+1,(i+1)*n//16)])/len(ordered[i*n//16:max(i*n//16+1,(i+1)*n//16)]) for i in range(16)]
        # Deterministic one-dimensional Lloyd refinement reduces the residual
        # certificate without ever changing a stored exact document vector.
        for _ in range(12):
            cuts=[(a+b)/2 for a,b in zip(row,row[1:])]
            borders=[0]+[bisect_left(ordered,cut) for cut in cuts]+[n]
            row=[math.fsum(ordered[a:b])/(b-a) if b>a else row[i] for i,(a,b) in enumerate(zip(borders,borders[1:]))]
        centers.append(row);cuts=[(a+b)/2 for a,b in zip(row,row[1:])]
        for pos,cid in enumerate(ids):
            code=bisect_right(cuts,units[cid][d]);codes[pos*stride+d//2]|=code<<(4*(d%2))
            errors[pos]+=(units[cid][d]-row[code])**2
    return {'recipe':ROUTING_RECIPE,'levels':16,'stride':stride,'centers':centers,
            'errors':[math.sqrt(v)+1e-10 for v in errors],'codes_base64':base64.b64encode(codes).decode()}


def vector_body(raw,row):
    encoding=row.get('encoding')
    if encoding!='f64_le':raise ValueError('unsupported lossless vector encoding')
    values=array('d');values.frombytes(zlib.decompress(raw))
    if sys.byteorder!='little':values.byteswap()
    return values.tobytes()


def verify(assets, corpus, manifest, vectors=None):
    """Offline complete source/statistics/boundary verification, not a request path."""
    assets=Path(assets)
    validate_space(manifest.get('space'))
    if vectors is not None and vectors['space']!=manifest['space']:raise ValueError('layout/vector embedding space mismatch')
    if manifest.get('schema')!=SCHEMA or manifest.get('routing_recipe')!=ROUTING_RECIPE or manifest.get('posting_codec')!=POSTING_CODEC or manifest.get('vector_codec')!=VECTOR_CODEC or manifest.get('corpus_sha256')!=c.digest(corpus):
        raise ValueError('layout source/space mismatch')
    def read(row):
        p=assets/row['path']
        if p.is_symlink() or assets.resolve() not in p.resolve().parents: raise ValueError('unsafe layout member')
        if 'offset' in row:
            with p.open('rb',buffering=0) as stream:stream.seek(row['offset']);raw=stream.read(row['bytes'])
        else:raw=p.read_bytes()
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']: raise ValueError('layout member checksum mismatch')
        return raw
    for row in manifest['shards']: read(row)
    meta=c.decode(gzip.decompress(read(manifest['metadata'])))
    members={row['path']:row for row in manifest['shards']}
    extents={}
    for row in meta['vector_shards']:extents.setdefault(row['path'],[]).append(row)
    needed=set(extents)|{row['path'] for row in meta['payload_shards']+meta['posting_shards']}
    if set(members)!=needed or len(members)!=len(manifest['shards']):raise ValueError('physical shard closure mismatch')
    for path,rows in extents.items():
        end=0
        for row in sorted(rows,key=lambda r:r['offset']):
            if row['offset']!=end or row['bytes']<1:raise ValueError('overlapping or missing vector extent')
            end+=row['bytes']
        if end!=members[path]['bytes'] or sum(r['count'] for r in rows)!=members[path]['count']:raise ValueError('vector pack coverage mismatch')
    expected={cid for cid,r in corpus['candidates'].items() if r['record_kind'] in documents.POSITIVE_KINDS}
    if set(meta['positive_ids'])!=expected or len(meta['positive_ids'])!=len(expected): raise ValueError('positive coverage mismatch')
    if meta['slot_catalog']!=corpus['slot_catalog'] or meta['slot_bindings']!=corpus['slot_bindings'] or meta['policies']!=corpus['policies']: raise ValueError('role/policy preservation mismatch')
    seen=set()
    for block,row in enumerate(meta['payload_shards']):
        payload=c.decode(gzip.decompress(read(row)))
        if len(payload)!=row['count'] or seen&set(payload): raise ValueError('duplicate payload owner/count')
        seen.update(payload)
        for cid,record in payload.items():
            if record!=corpus['candidates'][cid] or meta['payload_locator'][cid]!=block or meta['record_sha256'][cid]!=c.digest(record): raise ValueError('payload locator/source changed')
            if meta['guards'][cid]!=guard_record(record, corpus): raise ValueError('guard projection changed')
    if seen!=set(corpus['candidates']): raise ValueError('payload coverage mismatch')
    leaf_paths={}
    quant=meta['quantization'];codes=base64.b64decode(quant['codes_base64'],validate=True);positions={cid:i for i,cid in enumerate(meta['positive_ids'])}
    if quant['recipe']!=ROUTING_RECIPE or quant['levels']!=16 or quant['stride']!=384 or len(codes)!=len(expected)*384 or len(quant['centers'])!=768 or any(len(row)!=16 or not all(math.isfinite(v) for v in row) for row in quant['centers']) or len(quant['errors'])!=len(expected):raise ValueError('invalid routing quantization')
    def walk(pos,parents):
        node=meta['nodes'][pos]
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
        values=memoryview(vector_body(read(row),row)).cast('d')
        if len(values)!=row['count']*SPACE['dimensions'] or len(row['ids'])!=row['count'] or seen&set(row['ids']): raise ValueError('vector owner/count mismatch')
        seen.update(row['ids'])
        for offset,cid in enumerate(row['ids']):
            vector=values[offset*768:(offset+1)*768].tolist(); documents.validate_vector(vector)
            if vectors is not None and vector!=vectors['entries'][cid]['vector']: raise ValueError('vector precision loss')
            recipe,text=documents.text(corpus['candidates'][cid]);ref=meta.get('vector_recipes',{}).get(cid)
            if not ref or ref['recipe']!=recipe or ref['text_sha256']!=hashlib.sha256(text.encode()).hexdigest(): raise ValueError('vector text/recipe mismatch')
            if manifest['space']['provider']=='embeddinggemma2-local':
                validate_execution(ref.get('embedding_execution') or {},manifest['space'],text,vector,'document')
            norm=math.sqrt(math.sumprod(vector,vector));unit=[v/norm for v in vector]
            pos=positions[cid];approx=[quant['centers'][d][(codes[pos*384+d//2]>>(4*(d%2)))&15] for d in range(768)]
            residual=math.sqrt(math.fsum((a-b)**2 for a,b in zip(unit,approx)))
            if not math.isfinite(quant['errors'][pos]) or quant['errors'][pos]<residual:raise ValueError('unsafe quantization error bound')
    if seen!=expected: raise ValueError('vector coverage mismatch')
    lexical=documents.lexical(corpus)
    if meta['statistics']!={k:v for k,v in lexical.items() if k!='documents'}: raise ValueError('global lexical statistics mismatch')
    seen_terms=set()
    for block,row in enumerate(meta['posting_shards']):
        postings=PostingPage(zlib.decompress(read(row)),meta['positive_ids'])
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
