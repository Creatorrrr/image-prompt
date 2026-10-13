"""Whole-pool source applicability, independent of requested presentation tags."""
from __future__ import annotations
import photo_candidate_corpus as c
import photo_global_index as index
import photo_candidate_realizations as realizations
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
    reader=data.get('_search_reader')
    if reader is not None:
        data=dict(data);data['candidates']=reader.meta['guards']
    contract,picked=g.frozen_core_context(data,core,controls);allowed={};role_ids={};text,_=g.authorial_core_retrieval_text(core)
    adult=g.candidate_pack_visual_obligation_adult_context([{'text':text}],None)
    by_candidate={}
    for bid,b in sorted(data['slot_bindings'].items()):by_candidate.setdefault(b['candidate_id'],[]).append((bid,b))
    overridden=g.visual_profile_user_definition_override_ids(data[g.VISUAL_OBLIGATIONS_DATA_KEY],data[g.VISUAL_PROFILE_INDEX_DATA_KEY],core.get('user_definitions') or [])
    for cid,record in data['candidates'].items():
        if record['record_kind'] not in index.POSITIVE_KINDS:continue
        entry=c.entry(data,cid)
        # Canonical conditions and effects govern every presentation role.
        # A new empty binding cannot bypass this independent source check.
        if (not guard_policy(entry.get('subject_applicability') or {},contract)
                or not g.core_entry_eligible(data,core,contract,picked,'',entry,check_effect_scope=False)):
            continue
        if record['record_kind']=='visual_profile':
            if (entry.get('activation') or {}).get('requires_adult_character') is True and not adult:continue
            if not g.visual_profile_context_applicability(entry,text,has_authorial_core_context=True)[0]:continue
            if cid in overridden:continue
        conditional=record['effects'].get('realizations') or record['record_kind']=='visual_bundle'
        realization_ids = (realizations.eligible_ids(data,cid,core,contract,picked,check_effect_scope=False)
                           if conditional else ['base'])
        if not realization_ids:continue
        entry['_eligible_realization_ids'] = realization_ids
        bindings=by_candidate.get(cid,[])
        candidates=[]
        for bid,b in bindings:
            fits=(realizations.eligible_ids(data,cid,core,contract,picked,b['slot_id'],bid)
                  if conditional else g.core_entry_eligible(data,core,contract,picked,b['slot_id'],c.entry(data,cid,bid)))
            if guard_policy(b['conditions']['subject_applicability'],contract) and fits:
                candidates.append(bid)
        blob=reader.meta['positive_blobs'][cid] if reader is not None else ' '.join(v for field in index.fields(record).values() for v in field)
        if any(g.intent_alias_matches(blob,e) for e in core.get('user_exclusions') or []):continue
        allowed[cid]=entry;role_ids[cid]=candidates
    return allowed,role_ids,contract
