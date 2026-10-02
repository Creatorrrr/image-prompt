#!/usr/bin/env python3
"""Pure read-only full production V6 replay of the frozen two-action fixture.

No TestCase/fixture imports, rule generation, retrieval, API, network or writes.
The source elderly commuter and liminal location establish unforced compatibility
without using the action to satisfy its own requirements. Controlled pool exposure
is not natural retrieval/adoption evidence. All actual surfaces are compared.
"""
import copy
import socket
import urllib.request
from unittest.mock import patch
from cycle_common import A,E,SLOT,TARGET,g,load_freeze,read_json,require,sha,states_from_freeze
import compose_pack_view as view
import photo_candidate_semantics as semantics


def differences(before, after, path=''):
    if type(before) is not type(after):
        return [{'path':path,'baseline':before,'proposal':after}]
    if isinstance(before,dict):
        result=[]
        for key in sorted(set(before)|set(after)):
            child=path+'/'+key.replace('~','~0').replace('/','~1')
            if key not in before or key not in after:
                result.append({'path':child,'baseline':before.get(key),'proposal':after.get(key),'missing_side':'baseline' if key not in before else 'proposal'})
            else:
                result.extend(differences(before[key],after[key],child))
        return result
    if isinstance(before,list):
        if len(before)!=len(after):
            return [{'path':path,'baseline':before,'proposal':after}]
        return [item for i,(b,a) in enumerate(zip(before,after)) for item in differences(b,a,path+'/'+str(i))]
    return [] if before==after else [{'path':path,'baseline':before,'proposal':after}]


def check():
    frozen=load_freeze()
    states=states_from_freeze(frozen)
    record=read_json(E/'scout/two-action-fixture-freeze.json')
    result=read_json(E/'scout/generated-contract.json')
    require(sha((E/'scout/generated-contract.json').read_bytes())==record['original_generated_contract_sha256'],'Generated contract changed')
    original_core=result['provenance']['authorial_core']
    require(original_core['intent_lock']['locked_dimensions']==['concept','subject','event'],'Original core locks changed')
    require(record['forced'] is False and record['action_used_for_its_own_compatibility'] is False,'Fixture compatibility scope changed')
    selected_id=TARGET.split(':')[-1]
    surfaces={}
    blocked=AssertionError('Network/API/retrieval forbidden in read-only V6 replay')
    with patch.object(g,'embed_texts_with_gemini',side_effect=blocked),patch.object(urllib.request,'urlopen',side_effect=blocked),patch.object(urllib.request.OpenerDirector,'open',side_effect=blocked),patch.object(socket,'create_connection',side_effect=blocked):
        for label,data in states.items():
            data[g.QUALITY_LAYERS_DATA_KEY]=g.load_quality_layers(A/'photo_prompt_quality_layers.json')
            registry=g.load_visual_obligation_registry(A/'photo_prompt_visual_obligations.json')
            data[g.VISUAL_OBLIGATIONS_DATA_KEY]=registry
            data[g.VISUAL_PROFILE_INDEX_DATA_KEY]=g.load_visual_profile_index(A/'photo_prompt_visual_profile_index.json',registry)
            semantics.validate_candidate_entries(data,g.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
            subject=next(r for r in data['slots']['subject'] if r['id']=='elderly_commuter')
            location=next(r for r in data['slots']['location'] if r['id']=='between_use_transit_interior')
            companion=next(r for r in data['slots'][SLOT] if r['id']=='waiting_train')
            require(subject==record['subject_row'] and subject['kind']==['human'] and subject['en']=='an elderly commuter','Genuine elderly human source changed')
            require(location==record['location_row'] and companion==record['companion_row'],'Source context or companion changed')
            row=next(r for r in data['slots'][SLOT] if r['id']==selected_id)
            context={'subject':subject,'location':location}
            for candidate in [row,companion]:
                require(g.compatible_with_picked([candidate],context,forced=False,slot=SLOT,source=data)==[candidate],'Genuine context compatibility failed')
            fixture=copy.deepcopy(result)
            fixture['choices']={'subject':copy.deepcopy(subject),'location':copy.deepcopy(location),SLOT:{'id':selected_id}}
            fixture['preset_id']=None
            trace=fixture['semantic_trace'];trace['preset_scores']=[]
            trace['slot_scores']=[{'slot':SLOT,'selected':selected_id,'candidate_count':2,'top':[{'id':r['id'],'weight':r['weight'],'score':1.,'applicability_status':'eligible','applicability_source':'controlled_source_compatible_fixture'} for r in [row,companion]]}]
            contract=trace['generation_contract']
            contract['candidate_pool_trace']={SLOT:{'eligible_ids':[selected_id,companion['id']],'weights':{r['id']:r['weight']for r in [row,companion]},'forced':False}}
            pack=g.build_candidate_pack(fixture,data,'v6')
            candidates=pack.get('slots',{}).get(SLOT,{}).get('candidates',[])
            candidate=next((r for r in candidates if r['id']==TARGET),None)
            require(candidate is not None and any(r['id']=='slot:action:waiting_train'for r in candidates),'Both source actions must actually be exposed')
            overview=view.build_view(pack);view.verify_view(pack,overview)
            detail=view.build_view(pack,[TARGET]);view.verify_view(pack,detail)
            require(pack['authorial_core']==original_core,'Frozen core changed')
            require(pack['negative_intent_guard']==result['negative_intent_guard'],'Negative guard changed')
            require(contract['soft_anchor_policy']==result['semantic_trace']['generation_contract']['soft_anchor_policy'],'Generated soft policy changed')
            require(fixture['provenance']==result['provenance'],'Generated provenance changed')
            surface={'full_pack':pack,'candidate':candidate,'overview':overview,'detail':detail,'detail_verified':True}
            expected=read_json(E/(label+'-actual-v6.json'))
            delta=differences(expected,surface)
            require(not delta,'Actual expected V6 differences: '+str(delta))
            require(surface==read_json(E/('scout/two-action-'+label+'-actual-v6.json')),'Scout complete actual surface changed')
            surfaces[label]=surface
    delta=differences(surfaces['baseline'],surfaces['proposal'])
    require(not delta,'Actual two-state V6 differences: '+str(delta))
    require(surfaces['baseline']['full_pack']['pack_id']=='9a9674d57112ec23','Actual controlled pack ID changed')
    gate=read_json(E/'actual-v6-preservation.json')
    require(all(gate['checks'].values()) and gate['api_calls']==gate['retrieval_executions']==gate['new_rule_generations']==gate['repository_writes']==0,'Saved scout gate invalid')
    return {'status':'pass','full_pack_equal':True,'candidate_equal':True,'overview_equal':True,'verified_detail_equal':True,'actual_difference_paths':delta,'genuine_elderly_human_and_source_liminal_location_unforced':True,'api_calls':0,'rule_generations':0,'retrieval_executions':0,'writes':0}


if __name__=='__main__':
    print(check())
