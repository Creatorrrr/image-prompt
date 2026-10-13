from pathlib import Path
import sys
from tests.photo_native_authoring import *
ROOT=Path(__file__).resolve().parents[1]
SCRIPT_DIR=ROOT/'skills/photo-prompt-image-generator/scripts'
if str(SCRIPT_DIR) not in sys.path:sys.path.insert(0,str(SCRIPT_DIR))
import prompt_generator
import audit_composed_prompt

import copy,hashlib
import photo_candidate_corpus as native_corpus

def native_profile_registry():
    source=native_corpus.load(SCRIPT_DIR.parent/'assets')
    return {**source['policies']['visual_meaning_contract'], 'profiles':[native_corpus.entry(source,cid) for cid,r in source['candidates'].items() if r['record_kind']=='visual_profile']}

def integrity_query_context(core,controls,data=None):
    # Synthetic response for unit integrity tests only, never a real-query claim.
    from tests.test_photo_slot_queries import synthetic_set
    import photo_slot_retrieval
    from photo_search_reader import SearchReader,LazyRuntimeData
    data=(data if data is not None else LazyRuntimeData(SearchReader(SCRIPT_DIR.parent/'assets'))).for_core(core)
    return synthetic_set(core,controls,data['slot_catalog'],photo_slot_retrieval.active_slots(data,core,controls))

def compose_native(pack):
    core=pack['authorial_core'];lock=core['intent_lock'];prompt=core['baseline_prompt_en']
    review=copy.deepcopy(pack['embodiment_preflight']['baseline_review'])
    review.update(provenance='agent_postcomposition',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())
    result={'pack_id':pack['pack_id'],'composer':'agent','prompt_en':prompt,'negative_en':pack['negative_en'],
      'chosen_candidate_ids':[],'chosen_visual_concept_ids':[],'candidate_interpretations':[],
      'global_retrieval_sha256':pack['global_retrieval']['canonical_sha256'],
      'embodiment_review':{'source_contract_sha256':pack['embodiment_preflight']['canonical_sha256'],'review':review},
      'authorial_core_binding':{'source_authorial_core_sha256':core['canonical_sha256'],'source_intent_lock_sha256':lock['canonical_sha256'],'preserved_anchor_ids':[r['anchor_id'] for r in lock['semantic_anchors']],'preserved_evidence':[],'authorial_decisions':[]},
      'semantic_clarification_decisions':[{'clarification_id':r['id'],'decision':'applied' if r.get('required_in_final_prompt') else 'rejected','rationale':'Preserve the frozen requester-owned photograph and decline optional interpretation.','prompt_evidence':lock['semantic_anchors'][0]['prompt_evidence']} for r in (pack.get('semantic_clarification') or {}).get('candidates',[])],
      'creative_augmentation_brief':{'decisions':[{'candidate_id':r['id'],'decision':'rejected','rationale':'Keep the frozen baseline visual hierarchy.'} for r in (pack.get('creative_augmentation') or {}).get('candidates',[])]}}
    assertions=pack.get('semantic_assertion_obligations') or {}
    if assertions.get('enabled'):
        result['semantic_assertion_evidence']={'source_contract_sha256':assertions['canonical_sha256'],
            'evidence':{row['assertion_id']:copy.deepcopy(row['frozen_evidence']) for row in assertions['obligations']}}
    return result
