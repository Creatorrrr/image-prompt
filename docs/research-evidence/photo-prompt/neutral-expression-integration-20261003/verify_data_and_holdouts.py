"""Source invariants and unseen whole-sentence lexical holdouts, A/B."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg

EV=Path(__file__).parent
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'

HOLDS=[
 ('long_narrow_limbs','bm_long_limb_build','In a lamp-lit service bay, the same adult subject and named body region provide a body torso length reference, long upper and lower limb segments, and narrow limb volumes. The photographed proportions belong to one standing person.'),
 ('local_sinewy_contours','bm_wiry_definition','At the workbench, the same adult subject and named body region show narrow torso and limbs, local muscle planes, and tendon contours. These are shallow contours in one visible adult frame.'),
 ('lip_structure','bm_lip_volume','The portrait keeps upper lip vermilion thickness, lower lip vermilion thickness, and the boundary of the lip opening distinct on the same adult subject and named body region, while the lamp reflects in a nearby ceramic ornament.'),
 ('eye_boundaries','bm_eye_aperture','In the window portrait, upper eye-opening border and lower eye-opening border connect to medial and lateral eye corners. The same adult subject and named body region retain one coherent eye aperture.'),
 ('skin_pores_finish','bm_skin_relief_texture','The close portrait separates distribution of visible pores, low skin microrelief, and specular finish is separately readable. All observations belong to the same adult subject and named body region beside a glazed bowl.'),
 ('skin_striae_continuity','bm_striae_surface','Long narrow skin bands have localized color variation, and the bands continue on the same skin surface. The same adult subject and named body region remain visible beside the garment edge.'),
 ('skin_dimple_relief','bm_cellulite_relief','A continuous adult skin surface has distributed small shallow depressions and localized skin surface relief variation. The same adult subject and named body region stay distinguishable from a pebbled leather pouch.'),
 ('new_regional_volume','ne_regional_soft_volume','An adult portrait studies adult regional rounded soft volume in one upper arm beside the repair bench; the torso scale, garment and facial expression stay independently authored.'),
 ('new_regional_curves','ne_regional_contour_transition','An adult portrait studies adult regional convex-concave contour transition in one stated lateral torso segment beside a book press; other body regions retain their separately chosen form.'),
 ('new_current_pout','ne_current_lip_protrusion','A human adult face displays a current forward lip pout while watching the lantern; the ceramic pot on the nearby ledge retains its own broad rim.'),
]


def main():
    before_registry=json.loads((EV/'input-snapshot/merged-registry.json').read_text())
    before_data=json.loads((EV/'input-snapshot/merged-candidates.json').read_text())
    registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
    data=pg.load_json(ASSETS/'photo_prompt_tags.json')
    before_profiles={p['id']:p for p in before_registry['profiles']};profiles={p['id']:p for p in registry['profiles']}
    old_entries={(s,e['id']):e for s,rows in before_data['slots'].items() for e in rows};entries={(s,e['id']):e for s,rows in data['slots'].items() for e in rows}
    invariant_errors=[]
    for profile_id,old in before_profiles.items():
        new=profiles[profile_id]
        for key in ('definition','visual_components','contrast_examples'):
            if old['semantics'].get(key)!=new['semantics'].get(key):invariant_errors.append(f'{profile_id}.semantics.{key}')
        for key in ('category','required_evidence_fields','render_gates','reject_substitutes','concept_candidate','runtime_expression','composition_instruction'):
            if old.get(key)!=new.get(key):invariant_errors.append(f'{profile_id}.{key}')
        if profile_id!='embodied_corruption_transition' and old['activation']!=new['activation']:invariant_errors.append(f'{profile_id}.activation')
        old_cs=old['semantics'].get('component_semantics') or {};new_cs=new['semantics'].get('component_semantics') or {}
        for key in ('minimum_component_groups','required_group_ids'):
            if old_cs.get(key)!=new_cs.get(key):invariant_errors.append(f'{profile_id}.{key}')
        for old_group in old_cs.get('groups',[]):
            new_group=next(g for g in new_cs['groups'] if g['id']==old_group['id'])
            if not set(old_group['any_terms'])<=set(new_group['any_terms']):invariant_errors.append(f'{profile_id}.removed_component_terms')
    for (slot,entry_id),old in old_entries.items():
        new=entries[(slot,entry_id)]
        if {k:v for k,v in old.items() if k not in ('paraphrases','contextual_usage')}!={k:v for k,v in new.items() if k not in ('paraphrases','contextual_usage')}:invariant_errors.append(f'{slot}.{entry_id}.label_effect_guard_or_relation')
    aindex=pg.build_visual_profile_index_payload(before_registry)
    bindex=pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',registry)
    output=[]
    for case_id,expected,text in HOLDS:
        # The complete test sentence has never been added to a positive field.
        if any(text in pg.visual_profile_semantic_text(p) for p in registry['profiles']):raise AssertionError('holdout sentence indexed')
        lanes={}
        for lane,reg,index in (('before',before_registry,aindex),('after',registry,bindex)):
            result=pg.resolve_visual_profile_hits(reg,[{'source':'authorial_core_interpretation' if not case_id.startswith('new_') else 'user_requirement','text':text,'polarity':'advisory' if not case_id.startswith('new_') else 'required'}],visual_profile_index=index,query_fields={'active_request':text},query_text=text,adult_context=True)
            hits=[{'profile_id':h['profile_id'],'basis':h['match_basis'],'hard':h['hard_eligible'],'optional':h['optional_eligible']} for h in result['hits']]
            lanes[lane]={'hits':hits,'expected_accessible':any(h['profile_id']==expected for h in hits),'unexpected_hard_ids':[h['profile_id'] for h in hits if h['hard'] and h['profile_id']!=expected]}
        output.append({'id':case_id,'text':text,'expected_profile_id':expected,'lexical_only_comparison':True,**lanes})
    report={'source_invariants':{'status':'PASS' if not invariant_errors else 'FAIL','errors':invariant_errors,'existing_profiles_preserved':len(before_profiles),'existing_ordinary_candidates_preserved':len(old_entries),'conditional_activation_change_only':'embodied_corruption_transition'},'holdout_method':'Same unseen full sentence and unchanged rank policy; before/after exact + BM25F only. No vector or pixel claim. New component synonyms still require every component and common owner.','holdouts':output,'after_expected_accessible':sum(x['after']['expected_accessible'] for x in output),'before_expected_accessible':sum(x['before']['expected_accessible'] for x in output),'unexpected_hard_count':sum(len(x['after']['unexpected_hard_ids']) for x in output)}
    (EV/'DATA-INVARIANTS-AND-HOLDOUTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in report.items() if k not in ('holdouts','holdout_method')})
    return 0 if not invariant_errors and report['unexpected_hard_count']==0 and report['after_expected_accessible']==len(HOLDS) else 1


if __name__=='__main__':raise SystemExit(main())
