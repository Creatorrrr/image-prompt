"""One positive search document per global candidate, independent of role tags."""
from __future__ import annotations
import gzip, hashlib, math
from pathlib import Path
import photo_candidate_corpus as corpus
from photo_embedding_provider import SPACE, validate_vector, atomic
from photo_visual_retrieval import positive_visual_profile_fields, positive_visual_profile_text
from bm25f_retrieval import build_bm25f_index

SCHEMA='photo-global-candidate-index/v1'
MANIFEST='photo_candidate_index.json'
RECIPE='photo-global-visual-text/v1'
PROFILE_RECIPE='photo-visual-profile-text/v2'
QUERY_RECIPE='photo-frozen-core-query/v1'
POSITIVE_KINDS=corpus.KINDS-{'diagnostic'}
POLICY={'k1':1.2,'rrf_k':30,'candidate_limit':64,
 'query_fields':{'frozen_core':1.0,'global_context':1.0,'slot_focus':1.0},
 'fields':{k:{'weight':w,'b':0.75} for k,w in {'aliases':4,'labels':3,'definition':2,'paraphrases':2,
 'semantic_relations':2,'concept_units':2,'manifestations':1,'keywords':1,'semantic_caption':1}.items()}}

def strings(v):
    if isinstance(v,str):return [v] if v.strip() else []
    if isinstance(v,list):return [x for x in v if isinstance(x,str) and x.strip()]
    return []

def fields(record):
    c=record['content']
    if record['record_kind']=='visual_profile':
        positive=positive_visual_profile_fields(c)
        return {'aliases':positive['aliases'],'definition':positive['definition'],'paraphrases':positive['paraphrases'],
            'concept_units':positive['visual_components'],'keywords':positive['support_cues']}

    result={'aliases':strings(c.get('aliases')),'labels':[c[k] for k in ('en','ko','ja') if c.get(k)],
      'definition':strings(c.get('definition')),'paraphrases':strings(c.get('paraphrases')),
      'concept_units':strings(c.get('concept_units')),'manifestations':strings(c.get('manifestations')),
      'keywords':sum((strings(c.get(k)) for k in ('keywords','terms','embedding_text')),[]),'semantic_relations':[],
      'semantic_caption':[]}
    for rel in c.get('relations') or []:
        if isinstance(rel,dict):result['semantic_relations'].append(' '.join(str(rel[k]) for k in ('subject','type','object') if k in rel))
    for row in c.get('components') or []:
        if isinstance(row,dict):result['concept_units'].extend(strings(row.get('concept_units')))
    for value in (c.get('definitions_by_topic') or {}).values():result['definition'].extend(strings(value))
    return result

def text(record):
    if record['record_kind']=='visual_profile':return PROFILE_RECIPE,positive_visual_profile_text(record['content'])
    f=fields(record);parts=[]
    for name in ('labels','definition','aliases','paraphrases','concept_units','semantic_relations','manifestations','keywords'):
        values=list(dict.fromkeys(f.get(name) or []))
        if values:parts.append(name.replace('_',' ')+': '+'; '.join(values))
    return RECIPE,'\n'.join(parts)

def documents(c):return {cid:fields(r) for cid,r in c['candidates'].items() if r['record_kind'] in POSITIVE_KINDS}

def lexical(c):
    docs=documents(c);lexicon=sorted({v for f in docs.values() for name in ('aliases','labels','paraphrases') for v in f.get(name) or []})
    return build_bm25f_index(docs,policy=POLICY,lexicon=lexicon)

def validate(index,c):
    expected={cid:r for cid,r in c['candidates'].items() if r['record_kind'] in POSITIVE_KINDS}
    if index.get('schema')!=SCHEMA or index.get('space')!=SPACE or index.get('query_recipe')!=QUERY_RECIPE or index.get('corpus_sha256')!=corpus.digest(c):
        raise ValueError('native shared index schema/space/source mismatch')
    if set(index.get('entries',{}))!=set(expected):raise ValueError('native shared index coverage mismatch')
    for cid,record in expected.items():
        row=index['entries'][cid];recipe,body=text(record)
        if row.get('id')!=cid or row.get('text')!=body or row.get('recipe')!=recipe or row.get('text_sha256')!=hashlib.sha256(body.encode()).hexdigest():
            raise ValueError('native shared index identity/text/recipe mismatch: '+cid)
        validate_vector(row.get('vector'),SPACE['dimensions'])
    return index

def load(assets,c):
    assets=Path(assets).resolve();manifest=corpus.decode((assets/MANIFEST).read_bytes())
    if manifest.get('schema')!=SCHEMA:raise ValueError('native shared index required')
    entries={};seen=set()
    for shard in manifest['shards']:
        path=(assets/shard['path']).resolve()
        if assets not in path.parents or path in seen or path.is_symlink():raise ValueError('escaping/duplicate index shard')
        seen.add(path);raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=shard['sha256']:raise ValueError('shared index shard hash mismatch')
        rows=corpus.decode(gzip.decompress(raw))
        if len(rows)!=shard['count'] or set(entries)&set(rows):raise ValueError('shared index duplicate owner/count mismatch')
        entries.update(rows)
    result={k:v for k,v in manifest.items() if k!='shards'};result['entries']=entries
    return validate(result,c)

def write(assets,index):
    assets=Path(assets);identity=corpus.digest(index);directory=assets/'photo_candidate_index_shards'/identity;directory.mkdir(parents=True,exist_ok=True)
    keys=sorted(index['entries']);shards=[]
    for offset in range(0,len(keys),128):
        rows={key:index['entries'][key] for key in keys[offset:offset+128]}
        path=directory/f'{offset//128:04d}.json.gz';raw=gzip.compress(corpus.canonical_bytes(rows),mtime=0);path.write_bytes(raw)
        shards.append({'path':str(path.relative_to(assets)),'sha256':hashlib.sha256(raw).hexdigest(),'count':len(rows)})
    atomic(assets/MANIFEST,{k:v for k,v in index.items() if k!='entries'}|{'shards':shards})
    return identity

def cosine_rank(index, vector, allowed_ids=None, limit=384, minimum_similarity=0.30):
    """Exact cosine over the entire allowed shared corpus, no role selection."""
    validate_vector(vector,index['space']['dimensions'])
    ids=sorted(index['entries']) if allowed_ids is None else sorted(set(allowed_ids))
    if not set(ids)<=set(index['entries']):raise ValueError('cosine search has unknown candidate identity')
    if not ids:return []
    query_norm=math.sqrt(math.sumprod(vector,vector))
    scores=[]
    for cid in ids:
        values=index['entries'][cid]['vector']
        scores.append(math.sumprod(values,vector)/(math.sqrt(math.sumprod(values,values))*query_norm))
    ranked=sorted(((cid,float(score)) for cid,score in zip(ids,scores) if score>=minimum_similarity),key=lambda row:(-row[1],row[0]))
    return [{'document_id':cid,'score':round(score,9)} for cid,score in ranked[:limit]]
