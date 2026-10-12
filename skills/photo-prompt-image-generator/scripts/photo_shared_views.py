"""Native logical views of shared records; never reads an ownership tree."""
import copy
from pathlib import Path
import photo_candidate_corpus as c
import photo_global_index as index

def source(data):return {key:data[key] for key in c.CORPUS_FIELDS}

def role_entries(data,tag):
    allowed=getattr(data,'admitted_ids',None)
    for bid in data.get('_binding_tags',{}).get(tag,[]):
        row=data['slot_bindings'][bid]
        if allowed is None or row['candidate_id'] in allowed:yield c.entry(data,row['candidate_id'],bid)

def roles(data):return {tag:list(role_entries(data,tag)) for tag in data['slot_catalog']}

def entry_for_role(data,tag,cid):
    if cid not in data['candidates']:return None
    for bid in data.get('_binding_tags',{}).get(tag,[]):
        if data['slot_bindings'][bid]['candidate_id']==cid:return c.entry(data,cid,bid)
    return None

class RequestCandidates(dict):
    """An explicit bounded view of already retrieved IDs, not a new source."""
    def __init__(self,data,ids):super().__init__(data);self.admitted_ids=frozenset(ids)

def assemble(corpus,vectors):
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
            binding=corpus['slot_bindings'][pointer['binding_id']];member=c.entry(corpus,pointer['candidate_id'],pointer['binding_id']);member.update(copy.deepcopy(pointer['requirements']));member.update({'slot':binding['slot_id'],'entry_id':pointer['candidate_id'],'adoption':pointer['adoption']});members.append(member)
        row['member_candidates']=members;bundles.append(row)
    data['candidate_bundles']=bundles
    return data

def load(assets):
    corpus=c.load(assets);return assemble(corpus,index.load(assets,corpus))
