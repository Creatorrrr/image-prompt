"""Independent rank/allocation replay using immutable source and recorded vectors."""
import hashlib,math
import photo_candidate_corpus as c
import photo_global_index as idx
import photo_global_retrieval as rules
import photo_shared_views as views
import photo_frozen_query as query
import photo_native_pack as packs
from bm25f_retrieval import rank_bm25f


def audit(pack,data,context):
    import prompt_generator as g
    failures=[]
    def fail(reason):failures.append({'check':'global_retrieval_contract','reason':reason})
    try:
        packs.validate(pack);record=pack['global_retrieval'];core=pack['authorial_core'];controls=pack['creative_controls'];text,_=g.authorial_core_retrieval_text(core)
        if record.get('contract_version')!=rules.VERSION or record.get('mode') not in rules.MODES:raise ValueError('native global retrieval contract required')
        if record['mode']=='hybrid_required':query.validate(context,text,core['canonical_sha256'],controls['canonical_sha256'])
        elif context is not None:raise ValueError('keyword diagnostic cannot claim query vector execution')
        expected_bindings={'corpus_sha256':c.digest(views.source(data)),'binding_sha256':c.digest(data['slot_bindings']),
            'catalog_sha256':c.digest(data['slot_catalog']),'index_sha256':data['_global_index_sha256'],
            'query_context_sha256':context['canonical_sha256'] if context else None,'source_authorial_core_sha256':core['canonical_sha256'],'creative_controls_sha256':controls['canonical_sha256'],
            'query_sha256':hashlib.sha256(text.encode()).hexdigest(),'algorithm':'global_bm25f_exact_cosine_rrf/v1','rrf_k':30,'minimum_similarity':0.30,
            'unique_candidate_limit':64,'role_limits':{'core':4,'support':2},'tag_admission_filter':False,'candidate_adoption':'optional'}
        if any(record.get(key)!=value for key,value in expected_bindings.items()):fail('source/index/query/algorithm binding mismatch')
        if record.get('canonical_sha256')!=c.digest({k:v for k,v in record.items() if k!='canonical_sha256'}):fail('retrieval checksum mismatch')
        allowed,role_ids,_=rules.eligible(data,core,controls)
        # Do not consume the publisher's index cache, lane ranks, selected IDs or budgets.
        lexical=idx.lexical(views.source(data));lh=rank_bm25f(lexical,{'frozen_core':text},allowed_ids=allowed,limit=384)
        vh=[]
        if record['mode']=='hybrid_required':
            vector=context['vector'];norm=math.sqrt(math.sumprod(vector,vector));scored=[]
            for cid in sorted(allowed):
                reference=data['_global_index']['entries'][cid]['vector'];score=math.sumprod(reference,vector)/(math.sqrt(math.sumprod(reference,reference))*norm)
                if score>=0.30:scored.append((cid,score))
            scored.sort(key=lambda row:(-row[1],row[0]));vh=[{'document_id':cid,'score':round(score,9)} for cid,score in scored[:384]]
        lanes={'bm25f':{'state':'executed','positive_hits':len(lh),'ranks':lh},'embedding':{'state':'executed' if record['mode']=='hybrid_required' else 'not_requested','positive_hits':len(vh),'ranks':vh}}
        if record.get('lanes')!=lanes:fail('lane execution/ranks differ from full-corpus replay')
        sums={};counts={}
        for hits in ([lh,vh] if record['mode']=='hybrid_required' else [lh]):
            for position,row in enumerate(hits,1):
                cid=row['document_id'];sums[cid]=sums.get(cid,0.0)+1.0/(30+position);counts[cid]=counts.get(cid,0)+1
        # The pure RRF implementation rounds to its declared wire score before sorting.
        ranked=sorted(sums,key=lambda cid:(-round(sums[cid],12),-counts[cid],cid))
        selected=[];usage={};expected_refs={};expected_binding_ids=set()
        for cid in ranked:
            bindings=[]
            for bid in role_ids[cid]:
                tag=data['slot_bindings'][bid]['slot_id']
                if usage.get(tag,0)<g.candidate_pack_slot_limit(tag):bindings.append(bid)
            if role_ids[cid] and not bindings:continue
            selected.append(cid)
            for bid in bindings:
                tag=data['slot_bindings'][bid]['slot_id'];usage[tag]=usage.get(tag,0)+1;expected_binding_ids.add(bid);expected_refs.setdefault(tag,[]).append({'candidate_id':cid,'binding_id':bid})
            if len(selected)>=64:break
        if record.get('selected_candidate_ids')!=selected or record.get('eligible_candidates')!=len(allowed):fail('candidate omission/substitution or global unique allocation changed')
        if set(pack['candidate_pool'])!=set(selected):fail('pack pool differs from globally retrieved unique candidates')
        actual_refs={tag:row['candidate_refs'] for tag,row in pack['role_views'].items()}
        canonical_refs=lambda rows:{tag:sorted((r['candidate_id'],r['binding_id']) for r in refs) for tag,refs in rows.items()}
        if canonical_refs(actual_refs)!=canonical_refs(expected_refs):fail('role/tag/guard presentation mismatch')
        if set(pack['candidate_bindings'])!=expected_binding_ids or any(pack['candidate_bindings'].get(bid)!=data['slot_bindings'][bid] for bid in expected_binding_ids):fail('declared role effect/weight/condition mismatch')
        for cid,row in pack['candidate_pool'].items():
            if row['authored_record']!=data['candidates'][cid]:fail('candidate authored meaning/owner/effects changed')
    except (KeyError,TypeError,ValueError,AttributeError) as error:fail(str(error))
    return failures
