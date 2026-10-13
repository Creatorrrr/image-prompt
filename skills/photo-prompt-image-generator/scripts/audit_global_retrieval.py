"""Bounded independent proof/rank/allocation audit for native slot queries."""
import hashlib
import math
import photo_candidate_corpus as c
import photo_native_pack as packs
import photo_global_retrieval as guards
import photo_role_proposals as roles
import photo_slot_queries as queries
import photo_slot_retrieval as rules
import photo_candidate_realizations as realizations
import photo_sharded_search as search
from bm25f_retrieval import _query_term_weights


def lexical_replay(reader,fields,allowed,limit):
    stats=reader.meta['statistics'];policy=stats['policy'];values={};matched={}
    for term,weight in sorted(_query_term_weights(fields,policy=policy,lexicon=stats['lexicon']).items()):
        block=reader.meta['posting_locator'].get(term)
        if block is None:continue
        df=stats['document_frequencies'][term]
        idf=math.log(1+(stats['document_count']-df+.5)/max(df+.5,1e-12))
        for cid,tf in reader.block('posting',block)[term]:
            if cid in allowed:
                values[cid]=values.get(cid,0.)+float(weight)*idf*((tf*(policy['k1']+1))/(policy['k1']+tf))
                matched.setdefault(cid,[]).append(term)
    rows=[{'document_id':cid,'score':round(score,12),'matched_terms':matched[cid]} for cid,score in values.items() if score>0]
    return sorted(rows,key=lambda r:(-r['score'],r['document_id']))[:limit]


def fusion(lanes):
    sums={};counts={}
    for hits in lanes:
        for position,row in enumerate(hits,1):
            cid=row['document_id'];sums[cid]=sums.get(cid,0.)+1/(30+position);counts[cid]=counts.get(cid,0)+1
    rows=[{'document_id':cid,'score':round(v,12),'lane_count':counts[cid]} for cid,v in sums.items()]
    return sorted(rows,key=lambda r:(-r['score'],-r['lane_count'],r['document_id']))


def audit(pack,data,context):
    import prompt_generator as g
    failures=[]
    try:
        packs.validate(pack);record=pack['global_retrieval'];core=pack['authorial_core'];controls=pack['creative_controls']
        if hasattr(data,'for_core'):data=data.for_core(core)
        reader=data['_search_reader'];reader.check_presence();slots=rules.active_slots(data,core,controls,record['requested_slot_ids']);mode=record['mode']
        if record['contract_version']!=rules.VERSION or mode not in rules.MODES or record['canonical_sha256']!=c.digest({k:v for k,v in record.items() if k!='canonical_sha256'}):raise ValueError('slot retrieval schema/checksum mismatch')
        expected={'corpus_sha256':reader.meta['corpus_sha256'],'binding_sha256':c.digest(data['slot_bindings']),'catalog_sha256':c.digest(data['slot_catalog']),'index_sha256':data['_global_index_sha256'],
                  'source_authorial_core_sha256':core['canonical_sha256'],'creative_controls_sha256':controls['canonical_sha256'],'active_slot_ids':slots,'inactive_slot_ids':sorted(set(data['slot_catalog'])-set(slots)),
                  'unique_candidate_limit':64,'role_limits':{'core':4,'support':2},'minimum_similarity':.30,'rrf_k':30,'tag_admission_filter':False,'candidate_adoption':'optional','algorithm':'independent_global_bm25f_certified_cosine_rrf/v3',
                  'lanes':{'bm25f':{'state':'executed' if slots else 'not_requested','slot_count':len(slots)},'embedding':{'state':'executed' if mode=='hybrid_required' and slots else 'not_requested','slot_count':len(slots) if mode=='hybrid_required' else 0}}}
        if any(record.get(k)!=v for k,v in expected.items()):raise ValueError('slot source/query/policy binding mismatch')
        if mode=='hybrid_required':fields=queries.validate_set(context,core,controls,data['slot_catalog'],slots)
        elif context is not None:raise ValueError('keyword diagnostic claims query vectors')
        if record['query_context_sha256']!=(context['canonical_sha256'] if context else None):raise ValueError('foreign slot query set')
        allowed,source_roles,contract=guards.eligible(data,core,controls);_,picked=g.frozen_core_context(data,core,controls)
        gd=dict(data);gd['candidates']=reader.meta['guards'];wanted={};expected_proposals={}
        limits={s:4 if data['slot_catalog'][s]['priority']=='core' else 2 for s in slots}
        declared={}
        for bid,b in data['slot_bindings'].items():declared.setdefault(b['candidate_id'],[]).append(bid)
        if set(record['slot_searches'])!=set(slots) or record['eligible_candidates']!=len(allowed):raise ValueError('missing independent slot search')
        for slot in slots:
            trace=record['slot_searches'][slot];limit=trace['lane_limit']
            text,lexical,binding=queries.inputs(core,controls,data['slot_catalog'],slot,record['query_language'])
            if mode=='hybrid_required':
                row=context['slots'][slot]
                if row['binding']['language']!=record['query_language']:raise ValueError('slot language changed')
                text=row['text'];lexical=fields[slot];binding=row['binding']
            if limit<384 or trace['state']!='executed' or trace['search_scope']!='whole_shared_positive_corpus' or trace['tag_admission_filter'] is not False or trace['query_sha256']!=hashlib.sha256(text.encode()).hexdigest() or trace['slot_spec_sha256']!=binding['slot_spec_sha256'] or trace['eligible_candidates']!=len(allowed):raise ValueError('slot execution binding mismatch')
            lh=lexical_replay(reader,lexical,allowed,limit);vh=trace['lanes']['embedding']['ranks']
            if trace['lanes']['bm25f']!={'state':'executed','positive_hits':len(lh),'ranks':lh}:raise ValueError('global posting BM25F ranks differ')
            if mode=='hybrid_required':
                proof=trace['cosine_proof']
                if proof['limit']!=limit or proof['minimum']!=.30:raise ValueError('cosine search scope/cutoff changed')
                search.audit_cosine(reader,row['vector'],allowed,vh,proof)
            elif vh or trace['cosine_proof'] is not None:raise ValueError('keyword search claims cosine ranks')
            if trace['lanes']['embedding']!={'state':'executed' if mode=='hybrid_required' else 'not_requested','positive_hits':len(vh),'ranks':vh}:raise ValueError('embedding lane execution mismatch')
            combined=fusion([lh,vh] if mode=='hybrid_required' else [lh])
            if trace['rrf']!=combined:raise ValueError('slot RRF changed')
            chosen=[];rejected=set();blocked=g.slot_block_reason(data,slot,contract)
            if blocked:rejected.update(r['document_id'] for r in combined)
            else:
                for hit in combined:
                    cid=hit['document_id']
                    possible=realizations.eligible_ids(gd,cid,core,contract,picked,slot)
                    if not possible:
                        rejected.add(cid);continue
                    p=roles.propose(data,slot,cid,source_roles[cid],declared.get(cid,[]),realization_ids=possible)
                    entry=roles.entry(gd,p)
                    if p['applicability_status']=='incompatible' or not g.core_entry_eligible(data,core,contract,picked,slot,entry):rejected.add(cid);continue
                    expected_proposals[p['proposal_id']]=p;chosen.append((cid,p['proposal_id']))
                    if len(chosen)>=limits[slot]:break
            if trace['desired_proposal_ids']!=[p for _,p in chosen] or trace['role_rejected_candidate_ids']!=sorted(rejected) or trace['role_block_reason']!=blocked:raise ValueError('role guard/adoption projection changed')
            wanted[slot]=chosen
        selected=[];refs={s:[] for s in slots}
        for position in range(max(limits.values(),default=0)):
            for slot in sorted(slots,key=lambda s:(data['slot_catalog'][s]['priority']!='core',s)):
                if position>=len(wanted[slot]):continue
                cid,pid=wanted[slot][position]
                if cid not in selected:
                    if len(selected)>=64:continue
                    selected.append(cid)
                refs[slot].append({'candidate_id':cid,'proposal_id':pid})
        retained={r['proposal_id']:expected_proposals[r['proposal_id']] for rows in refs.values() for r in rows}
        if selected!=record['selected_candidate_ids'] or set(pack['candidate_pool'])!=set(selected):raise ValueError('global unique allocation changed')
        if pack['role_proposals']!=retained or record['role_proposals']!=retained:raise ValueError('role source effect/condition altered')
        canonical_refs=lambda values:{slot:sorted((r['candidate_id'],r['proposal_id']) for r in rows) for slot,rows in values.items()}
        if canonical_refs({s:v['candidate_refs'] for s,v in pack['role_views'].items()})!=canonical_refs(refs):raise ValueError('role reference allocation changed')
        bids={p['source_binding_id'] for p in retained.values() if p['source_binding_id'] is not None}
        if pack['candidate_bindings']!={bid:data['slot_bindings'][bid] for bid in bids}:raise ValueError('persistent source binding altered')
        for cid,row in pack['candidate_pool'].items():
            if row['authored_record']!=data['candidates'][cid]:raise ValueError('candidate authored meaning altered')
    except (KeyError,TypeError,ValueError,AttributeError) as error:failures.append({'check':'global_retrieval_contract','reason':str(error)})
    return failures
