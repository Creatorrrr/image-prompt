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
