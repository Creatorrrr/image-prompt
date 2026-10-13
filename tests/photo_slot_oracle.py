"""Offline full-scan reference; never imported by production retrieval."""
import math
from bm25f_retrieval import rank_bm25f, reciprocal_rank_fusion


def full_scan(lexical, entries, fields, vector, allowed, *, limit=384, minimum=0.30):
    lh = rank_bm25f(lexical, fields, allowed_ids=allowed, limit=limit)
    norm = math.sqrt(math.sumprod(vector, vector))
    scored = []
    for cid in sorted(allowed):
        values = entries[cid]['vector']
        score = math.sumprod(values, vector) / (math.sqrt(math.sumprod(values, values)) * norm)
        if score >= minimum:
            scored.append((cid, score))
    scored.sort(key=lambda row: (-row[1], row[0]))
    vh = [{'document_id': cid, 'score': round(score, 9)} for cid, score in scored[:limit]]
    return {'bm25f': lh, 'embedding': vh, 'rrf': reciprocal_rank_fusion(
        [[r['document_id'] for r in lh], [r['document_id'] for r in vh]], k=30)}


class PreparedFullScan:
    """Offline whole-pool reference, deriving TF from original field documents.

    Memoized per-term arithmetic accelerates the 224-query matrix; this class
    never consumes routing metadata, persisted postings, or runtime search.
    """
    def __init__(self,lexical,entries):
        self.lexical=lexical;self.entries=entries;self.terms={}
        self.norms={cid:math.sqrt(math.sumprod(row['vector'],row['vector'])) for cid,row in entries.items()}
    def rank(self,fields,vector,allowed,limit=384,minimum=.30):
        from bm25f_retrieval import _query_term_weights
        lex=self.lexical;policy=lex['policy'];weights=_query_term_weights(fields,policy=policy,lexicon=lex['lexicon'])
        for term in weights:
            if term in self.terms:continue
            contributions={};frequency=lex['document_frequencies'].get(term,0);n=lex['document_count'];k=policy['k1']
            idf=math.log(1.0+(n-frequency+.5)/max(frequency+.5,1e-12))
            for cid,document in lex['documents'].items():
                tf=0.
                for name,config in sorted(policy['fields'].items()):
                    field=document['fields'].get(name) or {};count=float(field.get('term_frequencies',{}).get(term,0))
                    if count<=0:continue
                    average=float(lex['average_field_lengths'].get(name,0) or 0);length=float(field.get('length',0) or 0)
                    tf+=config['weight']*count/max(1.-config['b']+config['b']*(length/average if average>0 else 1.),1e-12)
                if tf>0:contributions[cid]=(idf,tf)
            self.terms[term]=contributions
        lexical=[]
        for cid in sorted(allowed):
            score=0.;matched=[]
            for term,w in sorted(weights.items()):
                pair=self.terms[term].get(cid)
                if pair is None:continue
                idf,tf=pair;k=policy['k1'];score+=float(w)*idf*((tf*(k+1.))/(k+tf));matched.append(term)
            if score>0:lexical.append({'document_id':cid,'score':round(score,12),'matched_terms':matched})
        lexical.sort(key=lambda row:(-row['score'],row['document_id']));lexical=lexical[:limit]
        norm=math.sqrt(math.sumprod(vector,vector));scored=[]
        for cid in sorted(allowed):
            score=math.sumprod(self.entries[cid]['vector'],vector)/(self.norms[cid]*norm)
            if score>=minimum:scored.append((cid,score))
        scored.sort(key=lambda row:(-row[1],row[0]));vh=[{'document_id':cid,'score':round(score,9)} for cid,score in scored[:limit]]
        return {'bm25f':lexical,'embedding':vh,'rrf':reciprocal_rank_fusion([[r['document_id'] for r in lexical],[r['document_id'] for r in vh]],k=30)}
