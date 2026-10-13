"""Independent, full-positive-pool hybrid retrieval before presentation budgets."""
import hashlib
import photo_candidate_corpus as c
import photo_global_retrieval as guards
import photo_slot_queries as queries
import photo_role_proposals as roles
import photo_sharded_search as search
from bm25f_retrieval import reciprocal_rank_fusion

VERSION='photo-slot-retrieval/v2'
MODES={'hybrid_required','keyword_only'}


def active_slots(data,core,controls,requested=None):
    import prompt_generator as g
    if requested is not None:
        slots=sorted(set(requested))
        for slot in slots:queries.specification(data['slot_catalog'],slot)
        return slots
    contract,_=g.frozen_core_context(data,core,controls)
    opened=set(core['intent_lock']['open_dimensions'])
    return [slot for slot,spec in sorted(data['slot_catalog'].items())
            if not g.slot_block_reason(data,slot,contract)
            and (not spec['dimensions'] or bool(opened & set(spec['dimensions'])))]


def retrieve(data,core,controls,context=None,mode='hybrid_required',*,requested_slots=None,language='en',unique_limit=64):
    import prompt_generator as g
    if mode not in MODES or not 1<=unique_limit<=64:raise ValueError('invalid slot retrieval mode/budget')
    reader=data.get('_search_reader')
    if reader is None:raise ValueError('lazy shared search generation required')
    reader.check_presence()
    slots=active_slots(data,core,controls,requested_slots)
    fields=queries.validate_set(context,core,controls,data['slot_catalog'],slots) if mode=='hybrid_required' else {}
    if mode=='keyword_only' and context is not None:raise ValueError('keyword diagnostic cannot claim query embeddings')
    allowed,source_roles,contract=guards.eligible(data,core,controls)
    _,picked=g.frozen_core_context(data,core,controls)
    guard_data=dict(data);guard_data['candidates']=reader.meta['guards']
    traces={};desired={};proposals={};counts={};limits={slot:g.candidate_pack_slot_limit(slot) for slot in slots}
    for slot in slots:
        text,lexical,binding=queries.inputs(core,controls,data['slot_catalog'],slot,language)
        if mode=='hybrid_required':
            lexical=fields[slot];row=context['slots'][slot];text=row['text'];binding=row['binding'];vector=row['vector']
        limit=384;rejected=set();chosen=[];iterations=0
        while True:
            lh=search.lexical_rank(reader,lexical,allowed,limit)
            vh,proof=search.cosine_rank(reader,vector,allowed,limit) if mode=='hybrid_required' else ([],None)
            rankings=[[r['document_id'] for r in lh]]+([[r['document_id'] for r in vh]] if mode=='hybrid_required' else [])
            fused=reciprocal_rank_fusion(rankings,k=30)
            chosen=[];iterations+=1
            blocked=g.slot_block_reason(data,slot,contract)
            if blocked:
                rejected.update(hit['document_id'] for hit in fused)
                break
            for hit in fused:
                cid=hit['document_id'];proposal=roles.propose(data,slot,cid,source_roles[cid]);entry=roles.entry(guard_data,proposal)
                if blocked or not g.core_entry_eligible(data,core,contract,picked,slot,entry):rejected.add(cid);continue
                proposals[proposal['proposal_id']]=proposal
                chosen.append((cid,proposal['proposal_id'],hit))
                if len(chosen)>=limits[slot]:break
            # Extend both lane prefixes and refusion, never append a stale RRF page.
            if chosen or blocked or limit>=len(allowed) or (len(lh)<limit and len(vh)<limit):break
            limit=min(len(allowed),limit*2)
        desired[slot]=chosen;counts[slot]=len(fused)
        traces[slot]={'state':'executed','search_scope':'whole_shared_positive_corpus','tag_admission_filter':False,
                      'query_sha256':hashlib.sha256(text.encode()).hexdigest(),'slot_spec_sha256':binding['slot_spec_sha256'],
                      'lane_limit':limit,'iterations':iterations,'eligible_candidates':len(allowed),
                      'role_block_reason':blocked,'role_rejected_candidate_ids':sorted(rejected),
                      'lanes':{'bm25f':{'state':'executed','positive_hits':len(lh),'ranks':lh},
                               'embedding':{'state':'executed' if mode=='hybrid_required' else 'not_requested','positive_hits':len(vh),'ranks':vh}},
                      'cosine_proof':proof,'rrf':fused,'desired_proposal_ids':[p for _,p,_ in chosen]}
    selected=[];cards={};admitted={slot:[] for slot in slots};priority=sorted(slots,key=lambda s:(s not in g.CANDIDATE_PACK_CORE_SLOTS,s))
    for position in range(max(limits.values(),default=0)):
        for slot in priority:
            if position>=len(desired[slot]):continue
            cid,pid,hit=desired[slot][position]
            if cid not in selected:
                if len(selected)>=unique_limit:continue
                selected.append(cid)
            admitted[slot].append((cid,pid,hit))
    presented=dict(data);presented['_request_role_proposals']={slot:{cid:proposals[pid] for cid,pid,_ in admitted[slot]} for slot in slots}
    for slot in slots:
        rows=[]
        for cid,pid,hit in admitted[slot]:
            proposal=proposals[pid]
            candidate,_=g.candidate_pack_summarize_slot_candidate(presented,slot,{'id':cid,'applicability_status':proposal['applicability_status'],'applicability_source':'independent_full_pool_hybrid'})
            candidate.update(proposal_id=pid,binding_id=proposal['source_binding_id'],retrieval_evidence={'rrf_score':hit['score'],'lane_count':hit['lane_count']})
            candidate['_v7_semantic_source']=g.photo_candidate_semantics.semantic_source(roles.entry(data,proposal));rows.append(candidate)
        state='blocked' if traces[slot]['role_block_reason'] else ('no_hits' if not desired[slot] else ('budget_excluded' if not rows else ('budget_partial' if len(rows)<len(desired[slot]) else 'available')))
        cards[slot]={'slot':slot,'role':'core' if slot in g.CANDIDATE_PACK_CORE_SLOTS else 'support','selected':None,'candidates':rows,
                     'candidate_count':len(allowed),'retrieved_candidate_count':counts[slot],'candidate_limit':limits[slot],'status':state}
    retained={pid:proposals[pid] for rows in admitted.values() for _,pid,_ in rows}
    record={'contract_version':VERSION,'source_authorial_core_sha256':core['canonical_sha256'],'creative_controls_sha256':controls['canonical_sha256'],
            'corpus_sha256':reader.meta['corpus_sha256'],'binding_sha256':c.digest(data['slot_bindings']),'catalog_sha256':c.digest(data['slot_catalog']),
            'index_sha256':data['_global_index_sha256'],'query_context_sha256':context['canonical_sha256'] if context else None,
            'mode':mode,'query_language':language,'requested_slot_ids':sorted(set(requested_slots)) if requested_slots is not None else None,
            'active_slot_ids':slots,'inactive_slot_ids':sorted(set(data['slot_catalog'])-set(slots)),
            'algorithm':'independent_global_bm25f_certified_cosine_rrf/v2','rrf_k':30,'minimum_similarity':.30,
            'lanes':{'bm25f':{'state':'executed' if slots else 'not_requested','slot_count':len(slots)},
                     'embedding':{'state':'executed' if mode=='hybrid_required' and slots else 'not_requested','slot_count':len(slots) if mode=='hybrid_required' else 0}},
            'slot_searches':traces,'role_proposals':retained,'eligible_candidates':len(allowed),'selected_candidate_ids':selected,
            'unique_candidate_limit':unique_limit,'role_limits':{'core':4,'support':2},'tag_admission_filter':False,'candidate_adoption':'optional'}
    record['canonical_sha256']=c.digest(record)
    return cards,record,contract
