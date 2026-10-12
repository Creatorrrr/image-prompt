"""Frozen-core global hybrid discovery. Role tags are presentation metadata."""
from __future__ import annotations
import copy,hashlib
import photo_candidate_corpus as c
import photo_shared_views as views
import photo_global_index as index
import photo_frozen_query as query
from bm25f_retrieval import rank_bm25f,reciprocal_rank_fusion
VERSION='photo-global-retrieval/v1'
MODES={'hybrid_required','keyword_only'}

def guard_policy(policy,contract):
    category=contract.get('subject_category','generic');domains=set(contract.get('domains') or [])
    if category in set(policy.get('deny_subject_categories') or []):return False
    allowed=set(policy.get('subject_categories') or []);allow_domains=set(policy.get('allow_domains') or [])
    override=bool(policy.get('allow_domains_override_subject_categories') and allow_domains&domains)
    if allowed and category not in allowed and not override:return False
    if domains&set(policy.get('deny_domains') or []):return False
    return not(policy.get('require_domain_match') and allow_domains and not domains&allow_domains)

def eligible(data,core,controls):
    import prompt_generator as g
    contract,picked=g.frozen_core_context(data,core,controls);allowed={};role_ids={};text,_=g.authorial_core_retrieval_text(core)
    adult=g.candidate_pack_visual_obligation_adult_context([{'text':text}],None)
    by_candidate={}
    for bid,b in data['slot_bindings'].items():by_candidate.setdefault(b['candidate_id'],[]).append((bid,b))
    overridden=g.visual_profile_user_definition_override_ids(data[g.VISUAL_OBLIGATIONS_DATA_KEY],data[g.VISUAL_PROFILE_INDEX_DATA_KEY],core.get('user_definitions') or [])
    for cid,record in data['candidates'].items():
        if record['record_kind'] not in index.POSITIVE_KINDS:continue
        entry=c.entry(data,cid)
        if record['record_kind']=='visual_profile':
            if (entry.get('activation') or {}).get('requires_adult_character') is True and not adult:continue
            if not g.visual_profile_context_applicability(entry,text,has_authorial_core_context=True)[0]:continue
            if cid in overridden:continue
        bindings=by_candidate.get(cid,[])
        candidates=[]
        for bid,b in bindings:
            bound=c.entry(data,cid,bid)
            if guard_policy(bound.get('subject_applicability') or {},contract) and g.core_entry_eligible(data,core,contract,picked,bound.get('guard_role',''),bound):candidates.append(bid)
        if bindings and not candidates:continue
        if not bindings and record['record_kind'] not in {'visual_profile','visual_bundle'}:
            if not g.core_entry_eligible(data,core,contract,picked,'',entry):continue
        if record['record_kind']=='visual_bundle':
            if any(not guard_policy(c.entry(data,p['candidate_id'],p['binding_id']).get('subject_applicability') or {},contract) or not g.core_entry_eligible(data,core,contract,picked,c.entry(data,p['candidate_id'],p['binding_id']).get('guard_role',''),c.entry(data,p['candidate_id'],p['binding_id'])) for p in record['content']['member_candidates']):continue
        blob=' '.join(v for field in index.fields(record).values() for v in field)
        if any(g.intent_alias_matches(blob,e) for e in core.get('user_exclusions') or []):continue
        allowed[cid]=entry;role_ids[cid]=candidates
    return allowed,role_ids,contract

def retrieve(data,core,controls,context=None,mode='hybrid_required'):
    import prompt_generator as g
    if mode not in MODES:raise ValueError('unknown global retrieval mode')
    text,_=g.authorial_core_retrieval_text(core)
    if mode=='hybrid_required':query.validate(context,text,core['canonical_sha256'],controls['canonical_sha256'])
    allowed,roles,contract=eligible(data,core,controls)
    lexical=data.lexical_index() if hasattr(data,'lexical_index') else index.lexical(views.source(data))
    lexical_hits=rank_bm25f(lexical,{'frozen_core':text},allowed_ids=allowed,limit=384)
    vector_hits=index.cosine_rank(data['_global_index'],context['vector'],allowed_ids=allowed,limit=384) if mode=='hybrid_required' else []
    fused=reciprocal_rank_fusion([[r['document_id'] for r in lexical_hits],*[([r['document_id'] for r in vector_hits]) for _ in range(mode=='hybrid_required')]],k=30)
    admitted=[];role_counts={};cards={}
    for row in fused:
        cid=row['document_id'];eligible_bindings=[]
        for bid in roles[cid]:
            tag=data['slot_bindings'][bid]['slot_id']
            if role_counts.get(tag,0)<g.candidate_pack_slot_limit(tag):eligible_bindings.append(bid)
        if roles[cid] and not eligible_bindings:continue
        admitted.append(cid)
        for bid in eligible_bindings:
            tag=data['slot_bindings'][bid]['slot_id'];role_counts[tag]=role_counts.get(tag,0)+1
            candidate,_=g.candidate_pack_summarize_slot_candidate(data,tag,{'id':cid,'applicability_status':'eligible','applicability_source':'global_shared_hybrid'})
            candidate['binding_id']=bid;candidate['retrieval_evidence']={'rrf_score':row['score'],'lane_count':row['lane_count']};candidate['_v7_semantic_source']=g.photo_candidate_semantics.semantic_source(c.entry(data,cid,bid))
            cards.setdefault(tag,{'slot':tag,'role':'core' if tag in g.CANDIDATE_PACK_CORE_SLOTS else 'support','selected':None,'candidates':[],'candidate_count':sum(tag==data['slot_bindings'][b]['slot_id'] for bs in roles.values() for b in bs),'candidate_limit':g.candidate_pack_slot_limit(tag)})['candidates'].append(candidate)
        if len(admitted)>=64:break
    binding={'contract_version':VERSION,'source_authorial_core_sha256':core['canonical_sha256'],'creative_controls_sha256':controls['canonical_sha256'],
        'corpus_sha256':c.digest(views.source(data)),'binding_sha256':c.digest(data['slot_bindings']),'catalog_sha256':c.digest(data['slot_catalog']),
        'index_sha256':data['_global_index_sha256'],'query_context_sha256':context['canonical_sha256'] if context else None,
        'mode':mode,'query_sha256':hashlib.sha256(text.encode()).hexdigest(),'algorithm':'global_bm25f_exact_cosine_rrf/v1','rrf_k':30,'minimum_similarity':0.30,
        'lanes':{'bm25f':{'state':'executed','positive_hits':len(lexical_hits),'ranks':lexical_hits},'embedding':{'state':'executed' if mode=='hybrid_required' else 'not_requested','positive_hits':len(vector_hits),'ranks':vector_hits}},
        'eligible_candidates':len(allowed),'selected_candidate_ids':admitted,'unique_candidate_limit':64,'role_limits':{'core':4,'support':2},'tag_admission_filter':False,'candidate_adoption':'optional'}
    binding['canonical_sha256']=c.digest(binding)
    return cards,binding,contract
