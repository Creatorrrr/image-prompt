"""Native logical views of shared records; never reads an ownership tree."""
import copy
from pathlib import Path
import photo_candidate_corpus as c
import photo_global_index as index

def source(data):return {key:data[key] for key in c.CORPUS_FIELDS}

def role_entries(data,tag):
    allowed=getattr(data,'admitted_ids',None)
    if '_request_role_proposals' in data:
        import photo_role_proposals
        for cid,proposal in data['_request_role_proposals'].get(tag,{}).items():
            if allowed is None or cid in allowed:yield photo_role_proposals.entry(data,proposal)
        return
    for bid in data.get('_binding_tags',{}).get(tag,[]):
        row=data['slot_bindings'][bid]
        if allowed is None or row['candidate_id'] in allowed:yield c.entry(data,row['candidate_id'],bid)

def roles(data):return {tag:list(role_entries(data,tag)) for tag in data['slot_catalog']}

def entry_for_role(data,tag,cid):
    if cid not in data['candidates']:return None
    if '_request_role_proposals' in data:
        import photo_role_proposals
        proposal=data['_request_role_proposals'].get(tag,{}).get(cid)
        return photo_role_proposals.entry(data,proposal) if proposal else None
    for bid in data.get('_binding_tags',{}).get(tag,[]):
        if data['slot_bindings'][bid]['candidate_id']==cid:return c.entry(data,cid,bid)
    return None

class RequestCandidates(dict):
    """An explicit bounded view of already retrieved IDs, not a new source."""
    def __init__(self,data,ids,proposals=None):
        presented=data.presentations(ids) if hasattr(data,'presentations') else data
        super().__init__(presented);self.admitted_ids=frozenset(ids)
        if proposals is not None:
            self['_request_role_proposals']={tag:{} for tag in self['slot_catalog']}
            for proposal in proposals.values():self['_request_role_proposals'][proposal['target_slot_id']][proposal['candidate_id']]=proposal

def materialize_member(data, pointer, *, realization_id=None, dependency_selections=None):
    """CID owns meaning; an explicitly declared role only supplies presentation conditions."""
    bid = pointer.get('binding_id')
    binding = data['slot_bindings'][bid] if bid else None
    role = pointer.get('presentation_role', binding['slot_id'] if binding else '')
    if binding and (binding['candidate_id'] != pointer['candidate_id'] or role != binding['slot_id']):
        raise ValueError('member presentation role does not match its explicit binding')
    if role and role not in data['slot_catalog']:
        raise ValueError('unknown explicit member presentation role')
    member = c.entry(data, pointer['candidate_id'], bid, realization_id=realization_id,
                     dependency_selections=dependency_selections)
    requirements = copy.deepcopy(pointer.get('requirements') or {})
    member['_member_requirements'] = requirements
    # These are additional semantic/render obligations, never condition or body overrides.
    member['member_requirements']=copy.deepcopy(requirements)
    member.update(slot=role, entry_id=pointer['candidate_id'], adoption=pointer.get('adoption'))
    return member


def assemble(corpus,vectors):
    """Offline fixture/evaluation projection; production always uses SearchReader."""
    data=dict(corpus);data.update(corpus['policies']);data['_global_index']=vectors;data['_global_index_sha256']=c.digest(vectors)
    data['_binding_tags']={tag:[] for tag in corpus['slot_catalog']}
    for bid,binding in corpus['slot_bindings'].items():data['_binding_tags'][binding['slot_id']].append(bid)
    meaning=copy.deepcopy(corpus['policies']['visual_meaning_contract']);meaning['profiles']=[c.entry(corpus,cid) for cid in corpus['policies']['visual_profile_refs']]
    data['_visual_meaning']=meaning
    from prompt_generator import visual_profile_exact_term_rows
    data['_visual_meaning_lookup']={'exact_lookup':visual_profile_exact_term_rows(meaning)}
    graph=copy.deepcopy(corpus['policies']['relationship_graph']);graph['runtime_nodes']=[c.entry(corpus,cid) for cid in graph.pop('runtime_node_refs')];graph['concept_profiles']=[]
    for cid in graph.pop('concept_profile_refs'):
        row=c.entry(corpus,cid);row['confounders']=[c.entry(corpus,ref['candidate_ref']) for ref in row['confounders']];graph['concept_profiles'].append(row)
    data['relationship_graph']=graph
    bundles=[]
    for cid in corpus['policies']['bundle_refs']:
        row=c.entry(corpus,cid);members=[]
        for pointer in row['member_candidates']:
            members.append(materialize_member(corpus,pointer))
        row['member_candidates']=members;bundles.append(row)
    data['candidate_bundles']=bundles
    return data
