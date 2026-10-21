"""Production H/F2 kernel: full positive RID pool; one invocation per lane."""
import math
import numpy as np
import photo_recall_first as rf
from photo_recall_first import require
from photo_h_f2_query_scope import analyze, correct, compile_focus_contracts, order_focus
from photo_h_f2_literal_text import compile_contracts, order_literal
from photo_h_f2_event_phase import compile_contracts as phase_contracts, order_phase

def fuse(metadata,sparse,dense,k):
    require(type(k) is int and k in (10,30),'only frozen RRF10/30 admitted')
    ids=[d['id'] for d in metadata]
    require(len(ids)==len(set(ids))==len(sparse)==len(dense),'lane identity mismatch')
    require(all(math.isfinite(float(v)) for v in [*sparse,*dense]),'nonfinite score')
    require(all(v>=0 for v in sparse),'negative sparse score')
    lr={i:r for r,i in enumerate(sorted((i for i,s in enumerate(sparse) if s>0),key=lambda i:(-sparse[i],ids[i])),1)}
    dr={i:r for r,i in enumerate(sorted(range(len(ids)),key=lambda i:(-dense[i],ids[i])),1)}
    rows=[{'id':d['id'],'cid':d['cid'],'rid':d['rid'],'bm25':float(sparse[i]),'cosine':float(dense[i]),
           'bm25_rank':lr.get(i),'dense_rank':dr[i],
           'rrf':(1/(k+lr[i]) if i in lr else 0.)+1/(k+dr[i])} for i,d in enumerate(metadata)]
    rows.sort(key=lambda d:(-d['rrf'],d['id']))
    seen=set();out=[]
    for row in rows:
        if row['cid'] not in seen:seen.add(row['cid']);out.append(row)
    return out


def field_scores(index,query,tokenize,weighted,*,trace=False):
    scores=[0.]*index['n']
    contributions={}
    for term in sorted(set(tokenize(query))):
        postings=index['postings'].get(term,[])
        idf=math.log1p((index['n']-len(postings)+.5)/(len(postings)+.5))
        for i,fields in postings:
            terms=[]
            for field,tf in sorted(fields.items()):
                config=index['fields'][field];avg=index['average_lengths'][field]
                ratio=index['lengths'][field][i]/avg if avg>0 else 1.
                norm=1-config['b']+config['b']*ratio
                terms.append((config['weight'] if weighted else 1.)*tf/max(norm,1e-12))
            tf=math.fsum(terms)
            if tf>0:
                value=idf*tf*2.2/(1.2+tf);scores[i]+=value
                if trace:contributions.setdefault(term,{})[i]=value
    return (scores,contributions) if trace else scores

def known_row_contributions(index,query,tokenize,ordinal):
    """Audit one already identified RID; no ranking or candidate discovery."""
    from bisect import bisect_left
    out={}
    for term in sorted(set(tokenize(query))):
        postings=index['postings'].get(term,[])
        at=bisect_left(postings,ordinal,key=lambda row:row[0])
        if at==len(postings) or postings[at][0]!=ordinal:continue
        idf=math.log1p((index['n']-len(postings)+.5)/(len(postings)+.5));parts=[]
        for field,tf in sorted(postings[at][1].items()):
            config=index['fields'][field];avg=index['average_lengths'][field]
            ratio=index['lengths'][field][ordinal]/avg if avg>0 else 1.
            parts.append(config['weight']*tf/max(1-config['b']+config['b']*ratio,1e-12))
        tf=math.fsum(parts)
        if tf>0:out[term]=idf*tf*2.2/(1.2+tf)
    return out

class Index:
    def __init__(self,metadata,fields,matrix,documents,*,source_units,source_effects=None,source_constraints=None):
        self.metadata=metadata;self.fields=fields;self.matrix=matrix;self.calls=[]
        require(len(metadata)==fields['n']>0,'empty or mismatched RID pool')
        require(matrix.shape==(len(metadata),768),'vector dimensions or coverage changed')
        require(len({d['id'] for d in metadata})==len(metadata),'duplicate RID identity')
        require(all(d['id']==d['cid']+'|'+d['rid'] for d in metadata),'crossed CID/RID identity')
        self.documents={d['id']:d['text'] for d in documents}
        require(set(self.documents)=={d['id'] for d in metadata},'document witness coverage changed')
        self.literal_contracts=compile_contracts(self.documents,rf.tokens,source_units=source_units)
        self.phase_contracts=phase_contracts(self.documents,rf.tokens,source_units=source_units)
        self.focus_contracts=compile_focus_contracts(self.documents,source_units=source_units,source_effects=source_effects,source_constraints=source_constraints)
        self.norms=np.linalg.norm(matrix,axis=1)
        require(np.isfinite(matrix).all() and (self.norms>0).all(),'invalid document vectors')
    def search(self,text,row,binding,*,chunk_size=1024):
        require(isinstance(text,str) and bool(text.strip()),'empty H query')
        require(type(chunk_size) is int and chunk_size>0,'positive chunk size required')
        rf.check_embedding(row,binding,text,'query')
        v=np.asarray(row['vector'],dtype=np.float64);norm=np.linalg.norm(v)
        require(norm>0,'zero query vector')
        self.calls.append('BM25F')
        scope=analyze(text,rf.tokens)
        sparse,contributions=field_scores(self.fields,text,rf.tokens,True,trace=True)
        self.calls.append('local_cosine')
        dense=np.empty(len(self.metadata),dtype=np.float64)
        for offset in range(0,len(self.metadata),chunk_size):
            dense[offset:offset+chunk_size]=np.einsum('ij,j->i',self.matrix[offset:offset+chunk_size],v,optimize=False)/(self.norms[offset:offset+chunk_size]*norm)
        corrected,order,correction=correct(self.metadata,sparse,dense,scope,rf.tokens,fuse,
            lambda i:{term:rows[i] for term,rows in contributions.items() if i in rows},
            lambda i:self.documents[self.metadata[i]['id']],lambda term:len(self.fields['postings'].get(term,())))
        order,focus=order_focus(order,text,self.focus_contracts)
        order,literal=order_literal(order,text,scope,self.literal_contracts,rf.tokens)
        order,phase=order_phase(order,text,scope,self.phase_contracts,rf.tokens)
        return {'bm25':corrected,'bm25_raw':sparse,'cosine':dense,'order':order,'lane_calls':{'BM25F':1,'local_cosine':1},
                'considered_RIDs':len(self.metadata),'considered_CIDs':len({d['cid'] for d in self.metadata}),
                'query_scope':{'analysis':scope,'correction':correction,'literal_text':literal,'primary_focus':focus,'event_phase':phase}}


def present_material(rows,phase,*,literal=None,focus=None):
    """Witnessed material presentation after unchanged complete score lanes.

    A recognized property request exposes its proved role/carrier sources without
    filling the remaining budget from unproved or contradictory alternatives.
    Ordinary unrecognized requests keep the ordinary material path. This is not
    native source qualification or permission to adopt any complete candidate.
    """
    from photo_h_f2_event_phase import present_material as phase_present
    base,projection=phase_present(rows,phase)
    if phase.get('request') is not None:return base,projection
    literal=literal or {};focus=focus or {};allowed=None;excluded=set(phase.get('rejected_completed_sources',{}));mode=None
    request=literal.get('request',{})
    if literal.get('schema')=='photo-h-f2-primary-carried-literal/v3':
        excluded.update(literal.get('conflicting',{}))
        if request.get('mode')=='physical':allowed=set(literal.get('compatible',{}));mode='literal_source_witnesses'
    req=focus.get('request')
    if allowed is None and req and req.get('role') is not None:
        allowed=set(focus.get('supported_ids',[]));mode='primary_focus_source_witnesses'
    ongoing=bool((phase.get('excluded_phase') or {}).get('positive_ongoing_witnesses'))
    generic_only=bool(req and req.get('strict_nonpositive_roles')==['unmodeled_restricted_change'])
    if allowed is None and req and req.get('role') is None and req.get('strict_nonpositive_roles') and not (ongoing and generic_only):
        allowed=set();mode='nonpositive_scope_without_requested_change'
    excluded.update(focus.get('conflicting_ids',[]))
    if allowed is None and not excluded:return base,projection
    compatible=[r for r in rows if r['id'] not in excluded and (allowed is None or r['id'] in allowed)]
    chosen=compatible[:8]
    return chosen,{**projection,'mode':mode or 'explicit_source_exclusion',
        'available':len(compatible),'returned':len(chosen),'unfilled':8-len(chosen),
        'returned_ids':[r['id'] for r in chosen],'excluded_source_ids':sorted(excluded),
        'unknown_source_padding':allowed is None,'reason':'no_independently_requested_positive_change' if mode=='nonpositive_scope_without_requested_change' else 'source_witnesses_only' if allowed is not None else 'explicitly_excluded_source_meaning',
        'role_source_focus':req,'literal_source_request':request if literal.get('schema')=='photo-h-f2-primary-carried-literal/v3' else None,
        'native_approval':False,'semantic_approval':False,'additional_search_calls':0}
