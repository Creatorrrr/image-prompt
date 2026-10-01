#!/usr/bin/env python3
"""Replay actual production V6 surfaces from a frozen controlled rule fixture.

Default is read-only comparison against saved evidence. --record writes only
this experiment's V6 evidence. Neither mode invokes retrieval or an API.
"""
import argparse
import copy
from cycle_common import A, E, TARGET, g, load_freeze, read_json, require, states_from_freeze, write_json
import compose_pack_view as view
import photo_candidate_semantics as semantics


def generate():
    frozen = load_freeze()
    source_states = states_from_freeze(frozen)
    result = read_json(E / 'scout/synthetic-rule-contract-result.json')
    fixed_core = copy.deepcopy(result['provenance']['authorial_core'])
    candidate_id = TARGET.split(':')[-1]
    pool_ids = [candidate_id,'interacting_galaxy_pair_subject']
    surfaces = {}
    for label,data in source_states.items():
        data[g.QUALITY_LAYERS_DATA_KEY] = g.load_quality_layers(A / 'photo_prompt_quality_layers.json')
        registry = g.load_visual_obligation_registry(A / 'photo_prompt_visual_obligations.json')
        data[g.VISUAL_OBLIGATIONS_DATA_KEY] = registry
        data[g.VISUAL_PROFILE_INDEX_DATA_KEY] = g.load_visual_profile_index(A / 'photo_prompt_visual_profile_index.json',registry)
        semantics.validate_candidate_entries(data,g.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        subject = next(r for r in data['slots']['subject'] if r['id'] == candidate_id)
        pool = [next(r for r in data['slots']['subject'] if r['id'] == value) for value in pool_ids]
        require(g.compatible_with_picked(pool,{'subject':subject},forced=False,slot='subject',source=data) == pool,'Genuine subject-bearing alternatives lost compatibility')
        dependent = next(r for r in data['slots']['location'] if r['id'] == 'dusty_protostar_envelope_location')
        require(g.compatible_with_picked([dependent],{'subject':subject},forced=False,slot='location',source=data) == [dependent],'Narrow protostar location lost genuine source compatibility')
        fixture = copy.deepcopy(result)
        fixture['choices'] = {'subject':copy.deepcopy(subject)}
        fixture['preset_id'] = None
        contract = fixture['semantic_trace']['generation_contract']
        normalized = g.candidate_pack_normalized_slot_contract(data,fixed_core,contract)
        require(all(not g.entry_block_reason(option,'subject',normalized) for option in pool),'Controlled alternative blocked by real core')
        trace = fixture['semantic_trace']
        trace['slot_scores'] = [{'slot':'subject','selected':candidate_id,'candidate_count':len(pool),'top':[{'id':row['id'],'weight':row['weight'],'score':1.,'applicability_status':'eligible','applicability_source':'controlled_source_compatible_fixture'} for row in pool]}]
        trace['preset_scores'] = []
        contract['candidate_pool_trace'] = {'subject':{'eligible_ids':pool_ids,'weights':{row['id']:row['weight'] for row in pool},'forced':False}}
        pack = g.build_candidate_pack(fixture,data,'v6')
        candidate = next((row for row in pack.get('slots',{}).get('subject',{}).get('candidates',[]) if row['id'] == TARGET),None)
        require(candidate is not None,'Protostar absent from actual final pack')
        overview = view.build_view(pack)
        view.verify_view(pack,overview)
        detail = view.build_view(pack,[TARGET])
        view.verify_view(pack,detail)
        require(pack['authorial_core'] == fixed_core,'Frozen authorial core changed')
        require(pack['negative_intent_guard'] == result['negative_intent_guard'],'Negative guard changed')
        require(contract['soft_anchor_policy'] == result['semantic_trace']['generation_contract']['soft_anchor_policy'],'Generated soft policy changed')
        surfaces[label] = {'candidate':candidate,'full_pack':pack,'detail':detail,'overview':overview}
    require(surfaces['baseline'] == surfaces['proposal'],'Actual V6 candidate/full pack/overview/detail changed')
    report = {'status':'pass','scope':'Actual production V6 surfaces rebuilt from the exact frozen controlled rule fixture and complete cycle14 states; equality is preservation only, not retrieval or final-output improvement.','candidate_equal':True,'full_pack_equal':True,'detail_equal':True,'overview_equal':True,'genuine_subject_compatibility_without_force':True,'narrow_location_compatibility_without_force':True,'generated_soft_policy_preserved':True,'negative_guard_preserved':True,'frozen_core_preserved':True,'controlled_pool_ids':pool_ids,'api_calls':0,'query_retrieval_executions':0}
    return surfaces,report


def check():
    """Read-only full V6 replay for current regression modules; no rule rerun."""
    surfaces,report = generate()
    for label,surface in surfaces.items():
        require(read_json(E / (label+'-actual-v6.json')) == surface,'Saved actual V6 surface mismatch: '+label)
    require(read_json(E / 'actual-v6-preservation.json') == report,'Saved actual V6 report mismatch')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',action='store_true')
    args = parser.parse_args()
    surfaces,report = generate()
    values = [(label+'-actual-v6.json',surface) for label,surface in surfaces.items()] + [('actual-v6-preservation.json',report)]
    for name,value in values:
        if args.record:
            write_json(E / name,value)
        else:
            require(read_json(E / name) == value,'Saved actual V6 preservation mismatch: '+name)
    print('PASS: actual full V6 pack, detail, overview and candidate are exactly preserved; zero API/retrieval calls')


if __name__ == '__main__':
    main()
