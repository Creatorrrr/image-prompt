#!/usr/bin/env python3
"""Read-only production V6 replay from the exact frozen source fixture.

No TestCase import, rule generation, retrieval, API call or writes. Compare the
full expected scout packs, candidate, verified overview and hash-bound detail.
"""
import copy
from cycle_common import A, E, SLOT, TARGET, g, load_freeze, read_json, require, states_from_freeze
import compose_pack_view as view
import photo_candidate_semantics as semantics


def check():
    frozen = load_freeze()
    states = states_from_freeze(frozen)
    result = read_json(E / 'scout/generated-contract.json')
    original_summary = read_json(E / 'scout/surface-summary.json')
    fixed_core = copy.deepcopy(result['provenance']['authorial_core'])
    source_subject = original_summary['fixture']['subject_row']
    compatibility = read_json(E / 'scout/twelve-source-compatibility-checks.json')['checks']
    candidate_id = TARGET.split(':')[-1]
    surfaces = {}
    for label,data in states.items():
        data[g.QUALITY_LAYERS_DATA_KEY] = g.load_quality_layers(A / 'photo_prompt_quality_layers.json')
        registry = g.load_visual_obligation_registry(A / 'photo_prompt_visual_obligations.json')
        data[g.VISUAL_OBLIGATIONS_DATA_KEY] = registry
        data[g.VISUAL_PROFILE_INDEX_DATA_KEY] = g.load_visual_profile_index(A / 'photo_prompt_visual_profile_index.json',registry)
        semantics.validate_candidate_entries(data,g.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        subject = next(r for r in data['slots']['subject'] if r['id'] == source_subject['id'])
        require(subject == source_subject and subject['kind'] == ['human'] and 'adult' in subject['tags'], 'Real source adult subject changed')
        for source_check in compatibility:
            _,slot,entry_id = source_check['candidate_id'].split(':')
            row = next(r for r in data['slots'][slot] if r['id'] == entry_id)
            owner = next(r for r in data['slots']['subject'] if r['id'] == source_check['source_subject_id'])
            require(owner['kind'] == ['human'] and 'adult' in owner['tags'], 'Source human/adult compatibility lost')
            require(g.compatible_with_picked([row],{'subject':owner},forced=False,slot=slot,source=data) == [row], 'Reviewed source row lost genuine unforced compatibility: '+entry_id)
        row = next(r for r in data['slots'][SLOT] if r['id'] == candidate_id)
        fixture = copy.deepcopy(result)
        fixture['choices'] = {'subject':copy.deepcopy(subject),SLOT:{'id':candidate_id}}
        fixture['preset_id'] = None
        trace = fixture['semantic_trace']
        trace['preset_scores'] = []
        trace['slot_scores'] = [{'slot':SLOT,'selected':candidate_id,'candidate_count':1,'top':[{'id':candidate_id,'weight':row['weight'],'score':1.,'applicability_status':'eligible','applicability_source':'controlled_source_compatible_fixture'}]}]
        contract = trace['generation_contract']
        contract['candidate_pool_trace'] = {SLOT:{'eligible_ids':[candidate_id],'weights':{candidate_id:row['weight']},'forced':False}}
        require(g.compatible_with_picked([row],fixture['choices'],forced=False,slot=SLOT,source=data) == [row], 'Corrected row lost real source compatibility')
        pack = g.build_candidate_pack(fixture,data,'v6')
        candidate = next((r for r in pack.get('slots',{}).get(SLOT,{}).get('candidates',[]) if r['id'] == TARGET),None)
        require(candidate is not None, 'Corrected row absent from actual V6 pack')
        overview = view.build_view(pack)
        view.verify_view(pack,overview)
        detail = view.build_view(pack,[TARGET])
        view.verify_view(pack,detail)
        require(pack['authorial_core'] == fixed_core,'Frozen authorial core changed')
        require(pack['negative_intent_guard'] == result['negative_intent_guard'],'Negative guard changed')
        require(contract['soft_anchor_policy'] == result['semantic_trace']['generation_contract']['soft_anchor_policy'],'Generated soft policy changed')
        require(fixture['provenance'] == result['provenance'],'Fixture provenance changed')
        surface = {'full_pack':pack,'detail':detail,'overview':overview,'candidate':candidate,'detail_verified':True}
        expected_name = 'before' if label == 'baseline' else 'proposed'
        require(surface == read_json(E / ('scout/'+expected_name+'-actual-v6.json')), 'Full expected scout surface mismatch: '+label)
        require(surface == read_json(E / (label+'-actual-v6.json')), 'Saved cycle surface mismatch: '+label)
        surfaces[label] = surface
    require(surfaces['baseline'] == surfaces['proposal'],'Actual V6 full pack/candidate/overview/detail changed')
    require(surfaces['baseline']['full_pack']['pack_id'] == '946d69ecd0b85dc6', 'Expected full pack identity changed')
    report = {'status':'pass','scope':'Production V6 rebuilt from the exact frozen synthetic source-compatible contract and complete two-state data. Equality is preservation only, not a V6 semantic-loss repair or natural retrieval/adoption/prompt/image improvement.','candidate_equal':True,'full_pack_equal':True,'detail_equal':True,'overview_equal':True,'pack_id':'946d69ecd0b85dc6','genuine_human_adult_subject_compatibility_without_force':True,'all_12_reviewed_rows_compatible_with_source_adult_subjects':True,'generated_soft_policy_preserved':True,'negative_guard_preserved':True,'frozen_core_preserved':True,'fixture_provenance_preserved':True,'api_calls':0,'query_retrieval_executions':0,'rule_generation_executions':0,'writes':0}
    require(report == read_json(E / 'actual-v6-preservation.json'), 'Saved V6 report mismatch')
    return report


if __name__ == '__main__':
    check()
    print('PASS: full expected V6 pack, candidate, verified overview and detail preserved; zero API/retrieval/rule generation/writes')
