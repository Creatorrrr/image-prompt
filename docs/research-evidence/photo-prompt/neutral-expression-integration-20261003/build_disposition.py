"""Link research proposals to audited data changes without exporting research schema."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
RESEARCH=HERE.parent/'neutral-expression-semantics-20261003'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg

def read(path):return json.loads(path.read_text())
def save(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    registry=pg.load_visual_obligation_registry(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json')
    data=pg.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
    profiles={p['id']:p for p in registry['profiles']}
    entries={e['id'] for rows in data['slots'].values() for e in rows}
    receipt=read(HERE/'DATA-CHANGE-RECEIPT.json')
    changed={p['id'] for row in receipt['existing_profile_updates'] for p in row['profiles']}
    component_ids={r['profile_id'] for r in read(HERE/'COMPONENT-ALTERNATIVES.json')['updates']}
    research=read(RESEARCH/'SEMANTIC-UNITS.json')
    extra={'U01':['ne_regional_soft_volume'],'U02':['ne_regional_contour_transition'],'U16':['ne_current_lip_protrusion'],'U29':['pfe_cleavage']}
    rows=[]
    for unit in research['units']:
        owner_ids=list(dict.fromkeys(unit['owners']+extra.get(unit['id'],[])))
        assert all(i in profiles for i in owner_ids),(unit['id'],owner_ids)
        appended=[i for i in owner_ids if i in changed]
        new=[i for i in owner_ids if i in receipt['new_profile_ids']]
        reused=[i for i in unit['candidate_reuse'] if i in entries]
        if new:status='narrow_operational_profile_added'
        elif appended:status='equivalent_positive_alternatives_added_to_existing_owner'
        elif owner_ids or reused:status='existing_full_contract_retained'
        else:status='core_context_only_no_new_runtime_export'
        note='Observable form and same-owner components only; broad evaluation and history remain in their original research context.'
        if unit['id']=='U29':note='Central depression uses pfe_cleavage; decolletage remains the separate neckline region. Their contracts are not aliases.'
        if unit['id']=='U36':note='Only present load/flex/contact geometry is operationalized; recovery and repeated elasticity require time evidence. Cross-dimension research draft is not exported.'
        if unit['id'] in ('U20','U21'):note='Existing full target/action/result obligations are retained; broad seductive or playful language is not a new exact trigger.'
        rows.append({'unit_id':unit['id'],'title':unit['title'],'status':status,'current_owner_ids':owner_ids,'new_profile_ids':new,'profile_alternatives_added':appended,'component_alternatives_added':[i for i in owner_ids if i in component_ids],'existing_ordinary_candidate_ids':reused,'research_source_ids':unit['sources'],'note':note,'research_schema_copied_to_runtime':False,'broad_lexeme_exact_promotion':False})
    byunit={r['unit_id']:r for r in rows}
    terms=[]
    for row in read(RESEARCH/'TERM-DECISIONS.json')['decisions']:
        terms.append({'research_term_id':row['id'],'row_kind':row['row_kind'],'expression_group':row['expression_group'],'research_decision':row['decision'],'proposed_units':row['proposed_units'],'unit_implementation_status':{u:byunit[u]['status'] if u in byunit else 'context_record_retained' for u in row['proposed_units']},'preserved_scope':row['preserve'],'excluded_inference':row['do_not_add'],'whole_expression_group_exported_as_runtime_alias':False,'full_expression_group_verified':row['full_expression_group_verified'],'limitation':row.get('pending_review','')})
    candidate_map={'NC01':['bm_breast_projection'],'NC02':['bm_breast_root_width'],'NC03':['bm_gluteal_projection'],'NC04':['bm_lip_volume'],'NC05':['ae_pucker'],'NC06':['bm_eye_aperture'],'NC07':['pv_side_eye'],'NC08':['pv_half_lidded'],'NC09':['same_adult_target_coordinated_gaze'],'NC12':['pv_gaze_direct'],'NC17':['bm_fabric_body_outline'],'NC18':['pfe_cleavage_candidate'],'NC19':['pfe_lateral_chest_candidate'],'NC20':['pfe_lower_chest_candidate'],'NC21':['bm_cellulite_relief'],'NC22':['bm_striae_surface']}
    drafts=[]
    for row in read(RESEARCH/'CANDIDATE-DRAFTS.json')['candidates']:
        targets=candidate_map.get(row['id'],[]);targets=[i for i in targets if i in entries]
        drafts.append({'research_draft_id':row['id'],'units':row['units'],'runtime_ordinary_candidate_ids':targets,'resolution':'reuse_existing_runtime_entry_with_existing_effects_and_guards' if targets else 'retain_research_draft_no_literal_runtime_export','unit_implementation_status':{u:byunit[u]['status'] for u in row['units']},'placeholder_owner_or_property_exported':False,'raw_draft_exported':False,'original_readiness':row['readiness']})
    save('RESEARCH-DISPOSITION.json',{'schema_version':'neutral-research-to-runtime-disposition/v1','keyword_group_count':sum(t['row_kind']=='keyword_group' for t in terms),'prior_assistant_example_count':sum(t['row_kind']!='keyword_group' for t in terms),'semantic_unit_count':len(rows),'context_units_retained':research['contexts'],'unit_status_counts':dict(Counter(r['status'] for r in rows)),'units':rows,'term_decisions':terms,'candidate_draft_dispositions':drafts,'new_ordinary_candidates':receipt['new_ordinary_candidate_ids'],'narrow_exact_terms':receipt['new_exact_terms'],'boundary':'Operational clauses are newly authored equivalents, not wholesale verification or export of the 181 keyword groups. Original research remains research-only.'})
    print(json.dumps({'units':len(rows),'terms':len(terms),'drafts':len(drafts),'statuses':dict(Counter(r['status'] for r in rows))},ensure_ascii=False))

if __name__=='__main__':main()
