"""Synthetic full V6 cases: moral meaning must not require bodily mutation."""
from __future__ import annotations

import json
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tests import photo_prompt_fixtures as fixtures


def cases():
    rows = [
        ("moral_choice", "이익 때문에 원칙을 포기한 성인 인물의 타락을 봉투를 받고 약속 문서를 접는 현재 선택으로 보여줘.",
         "An adult office worker accepts a sealed envelope and folds a written promise on the desk. The current choice trades a stated principle for personal gain. The same person's hand touches the envelope while the folded promise remains legible beside it. An ordinary rainlit office establishes the setting, and a restrained eye-level medium view keeps the actor, the accepted envelope and the abandoned written commitment within one coherent frame.", False),
        ("embodied_transition", "성인 인물의 몸에 어둠이 번지는 타락 변화, 이전 표식과 아직 남은 얼굴, 진행 중인 경계를 보여줘.",
         "An adult fictional figure stands before a stone doorway as an unfinished darkness boundary spreads across the same adult body. A former white emblem and the unchanged half of the face remain readable beside the dark current state. A cracked glowing seal beneath the hand supplies a visible cause. The moving boundary crosses the shoulder and forearm in one coherent photographic frame, with the former identity, present transformation and incomplete transition all distinct.", True),
        ("user_defined_moral", "이 요청에서 타락은 성인 인물이 약속을 돈과 바꾸는 현재 선택만 뜻한다. 봉투를 받고 서약서를 접는 순간을 보여줘.",
         "An adult office worker accepts a sealed envelope and folds a written promise on the desk. The current choice trades a stated principle for personal gain. The same person's hand touches the envelope while the folded promise remains legible beside it. An ordinary rainlit office establishes the setting, and a restrained eye-level medium view keeps the actor, the accepted envelope and the abandoned written commitment within one coherent frame.", False),
        ("negated_transition", "성인 인물이 책을 확인하는 평범한 장면. 타락 변화 없이 현재 얼굴과 몸을 보여줘.",
         "An adult librarian checks an open book at a quiet reading-room desk. The current face and body belong to the same ordinary adult, with one hand resting beside the page and the other supporting the book. A window illuminates the book, the connected arms and the readable present expression. A restrained medium photograph keeps the person and the actual page-checking event together while the room provides clear near-to-far depth.", False),
    ]
    result=[]
    for case_id, request, baseline, expected in rows:
        core=fixtures.core(request, interpreted_intent=baseline, subject="one adult fictional figure" if expected else "one adult librarian" if case_id=='negated_transition' else "one adult office worker", setting="a weathered stone sanctuary doorway" if expected else "a quiet windowlit library reading desk" if case_id=='negated_transition' else "a rainlit office with wooden furniture", event="an unfinished darkness boundary spreads across the same adult body" if expected else "accepts a sealed envelope and folds a written promise" if 'moral' in case_id else "checks an open book", baseline_prompt_en=baseline, visual_priorities=("same adult ownership", "current visible action", "distinct evidence within one frame"), open_dimensions=("body_geometry", "appearance", "expression", "pose", "action", "setting", "framing", "composition", "lighting", "camera"))
        if case_id == "user_defined_moral":
            core['user_definitions']=[{'term':'타락', 'source_text':request, 'interpreted_meaning':'a moral choice trading a promise for personal gain', 'prompt_evidence':'accepts a sealed envelope and folds a written promise'}]
        result.append({'id':case_id,'request':request,'core':core,'expected_embodied_hard':expected})
    return result


def run(stage):
    baseline_pg=None
    if stage=='before':
        snapshot=Path(__file__).parent/'input-snapshot'
        spec=importlib.util.spec_from_file_location('neutral_baseline_generator',snapshot/'prompt_generator.py')
        baseline_pg=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline_pg)
        assets=ROOT/'skills/photo-prompt-image-generator/assets'
        data=json.loads((snapshot/'merged-candidates.json').read_text())
        registry=json.loads((snapshot/'merged-registry.json').read_text())
        data[baseline_pg.VISUAL_OBLIGATIONS_DATA_KEY]=registry
        data[baseline_pg.VISUAL_PROFILE_INDEX_DATA_KEY]=baseline_pg.load_visual_profile_index(assets/'photo_prompt_visual_profile_index.json',registry)
        data[baseline_pg.SEMANTIC_INDEX_DATA_KEY]=baseline_pg.load_semantic_index_payload(assets/'photo_prompt_semantic_index.json')
        data[baseline_pg.QUALITY_LAYERS_DATA_KEY]=baseline_pg.load_quality_layers(assets/baseline_pg.QUALITY_LAYERS_FILENAME)
        baseline_pg.validate_semantic_index_metadata(data[baseline_pg.SEMANTIC_INDEX_DATA_KEY],data)
    results=[]
    for case in cases():
        if baseline_pg:
            raw=case['core']; controls=baseline_pg.creative_controls.resolve(raw['source_request'],overrides={'sensual':0,'fetish':0,'creativity':1,'surreal':0},seed=7)
            raw['creative_controls_sha256']=controls['canonical_sha256']
            frozen=baseline_pg.normalize_authorial_core(raw,request_envelope=baseline_pg.normalize_request_envelope(fixtures.envelope(raw['source_request'])),creative_control_snapshot=controls)
            pack=baseline_pg.generate_candidate_pack(data,frozen,controls,fixtures.review(frozen['baseline_prompt_en']),seed=91)
        else:
            pack=fixtures.run_current(case['core'])
        hard=[row['id'] for row in pack.get('visual_obligations',{}).get('obligations',[])]
        results.append({'id':case['id'],'source_request':case['request'],'authorial_core_sha256':pack['authorial_core']['canonical_sha256'],'hard_profile_ids':hard,'expected_embodied_hard':case['expected_embodied_hard'],'pass':('embodied_corruption_transition' in hard)==case['expected_embodied_hard'],'retrieval_query':pack['provenance'].get('retrieval_query')})
    output=Path(__file__).parent/f'FULL-CORE-{stage.upper()}.json'
    output.write_text(json.dumps({'stage':stage,'synthetic_contract_tests_not_user_requests':True,'cases':results},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'stage':stage,'cases':[{k:r[k] for k in ('id','hard_profile_ids','pass')} for r in results]},ensure_ascii=False))
    return results


if __name__=='__main__':
    run(sys.argv[1] if len(sys.argv)>1 else 'current')
