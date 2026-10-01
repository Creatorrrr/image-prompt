"""Reproduce actual V6 pack/detail surfaces for published DATA rows, zero APIs."""
from pathlib import Path
import copy,json,sys
ROOT=Path(__file__).resolve().parents[4]
EVIDENCE=Path(__file__).resolve().parent
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as generator
import compose_pack_view as views
from tests.test_photo_authorial_core_v6 import PhotoAuthorialCoreV6Tests


def runtime_data():
    return PhotoAuthorialCoreV6Tests().runtime_data()


def build_state(data, entry, slot, eid, contract_result, control=None):
    """Fix trace exposure, retain production projection/adoption policies."""
    candidate_data={**data,'slots':{**data['slots'],slot:[copy.deepcopy(entry)if row['id']==eid else row for row in data['slots'][slot]]}}
    candidate_data.pop(generator.SEMANTIC_INDEX_DATA_KEY,None)
    fixture=copy.deepcopy(contract_result);fixture['choices']={slot:{'id':eid}};fixture['preset_id']=None
    ids=[eid]+([control]if control else[])
    trace=fixture['semantic_trace'];trace['slot_scores']=[{'slot':slot,'selected':eid,'candidate_count':len(ids),'top':[{'id':v,'weight':1.,'score':1.,'applicability_status':'eligible'}for v in ids]}]
    contract=trace['generation_contract'];contract['candidate_pool_trace']={slot:{'eligible_ids':ids,'weights':{v:1. for v in ids}}};contract['soft_anchor_policy']={};trace['preset_scores']=[]
    pack=generator.build_candidate_pack(fixture,candidate_data,'v6');cid='slot:'+slot+':'+eid
    candidate=next((c for c in pack.get('slots',{}).get(slot,{}).get('candidates',[])if c['id']==cid),None)
    detail=views.build_view(pack,[cid])if candidate else None
    if detail:views.verify_view(pack,detail)
    return {'pack_id':pack.get('pack_id'),'candidate':candidate,'detail':detail,'candidate_surface_version':pack.get('candidate_semantic_surface_version')}


def main():
    data=runtime_data();raw=generator.load_json(ASSETS/'photo_prompt_tags.json')
    audit=json.loads((EVIDENCE/'projection-audit.json').read_text());assert generator.dictionary_hash(raw)==audit['current_dictionary_hash'],'Run at the audited source/index snapshot'
    rows={r['id']:r for r in audit['rows']};assert len(rows)==58
    result=json.loads((EVIDENCE/'generated-contract-result.json').read_text());verified=0
    for filename in ['full-public-pack-audit.json','multichoice-full-public-pack-audit.json']:
        expected=json.loads((EVIDENCE/filename).read_text())
        for case in expected['cases']:
            row=rows[case['id']];slot=row['slot'];eid=row['id']
            assert next(v for v in raw['slots'][slot]if v['id']==eid)==row['accepted']
            for label,key in [('baseline','before'),('changed','accepted')]:
                actual=build_state(data,row[key],slot,eid,result,case.get('unchanged_control_id'))
                saved=case['states'][label]
                assert all(actual[k]==v for k,v in saved.items()),(filename,eid,label)
                verified+=1
    assert verified==122
    print('Verified122 production pack states for58 published rows; controlled exposure, zero API calls')


if __name__=='__main__':main()
