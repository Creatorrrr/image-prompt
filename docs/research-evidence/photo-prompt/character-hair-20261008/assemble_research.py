"""Assemble research cross-references and review drafts, without runtime writes."""
import collections
import importlib.util
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

OUT = Path(__file__).resolve().parent
PREFIXES = ['cuts', 'topology', 'color-state', 'main', 'cuts-supplement']


def read(name):
    return json.loads((OUT / name).read_text())


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def keyword_ids(card):
    ids = card.get('reference_keyword_ids', [])
    for k in ['reference_keywords', 'input_keywords']:
        ids += [r['id'] if isinstance(r, dict) else r for r in card.get(k, [])]
    return list(dict.fromkeys(ids))


def source_ids(card):
    values=card.get('source_refs', card.get('source_support', []))
    return [r.get('source_id',r.get('id')) if isinstance(r,dict) else r for r in values]


def normalized_url(url):
    p=urlsplit(url)
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/'),p.query,''))


# Each tuple is a review choice, not automatic insertion or a new semantic ID.
# fields: glossary IDs, primary semantic card, slot, existing IDs, provisional ID,
# label, wording, properties, directed relations.
SPECS = [
 (['H109'],'hair-cut-hime','hair_style',['hime_cut'],'chrh_hime_face_shelves','얼굴 옆 짧은 단차','short face-side panels end in clear shelves while longer hair continues behind them',['hair.style.length.regional_partition'],[('face_side_panels','shorter_than','rear_lengths')]),
 (['H110'],'hair-cut-jellyfish','hair_style',[],'chrh_jellyfish_cap','둘레 cap 아래 긴 층','a short upper cap continues around the sides and back above a separate long underlayer',['hair.style.length.regional_partition'],[('short_cap','above','long_underlayer')]),
 (['H097'],'hair-cut-a_line','hair_style',[],'chrh_a_line_perimeter','앞이 긴 보브 외곽','the front perimeter of the bob extends lower than its shorter rear perimeter',['hair.style.bob.front_back_perimeter'],[('front_ends','longer_than','rear_ends')]),
 (['H053','H099'],'hair-cut-stacked_bob','hair_style',[],'chrh_occipital_stack','뒤에 쌓인 보브 층','short layers stack at the nape and occipital area while preserving the chosen front perimeter',['hair.style.bob.occipital_stack'],[('short_layers','stack_at','nape_occipital_region')]),
 (['H128'],'hair-cut-full_bangs','hair_style',[],'chrh_full_fringe_coverage','이마를 넓게 덮는 앞머리','the front fringe covers the selected forehead width as a continuous hair mass',['hair.fringe.coverage'],[('front_fringe','covers','selected_forehead_width')]),
 (['H129'],'hair-cut-blunt_bangs','hair_style',[],'chrh_blunt_fringe_edge','또렷한 앞머리 끝선','the selected fringe ends in a clear transverse edge',['hair.fringe.edge'],[('fringe_ends','form','transverse_edge')]),
 (['H134'],'hair-cut-micro_bangs','hair_style',[],'chrh_micro_fringe_length','눈썹 위 짧은 앞머리','the selected front fringe ends clearly above the visible eyebrows',['hair.fringe.length'],[('fringe_ends','above','eyebrows')]),
 (['H083'],'hair-cut-low_fade','hair_style',[],'chrh_low_fade_band','낮은 위치의 페이드','a length transition remains low around the lower side and rear scalp',['hair.style.fade.height'],[('length_transition','located_at','lower_side_rear_scalp')]),
 (['H087'],'hair-cut-drop_fade','hair_style',[],'chrh_drop_fade_path','귀 뒤로 내려가는 페이드','the fade transition curves downward behind the ear',['hair.style.fade.path'],[('fade_transition','curves_down_behind','ear')]),
 (['H174'],'hair.topology.high_ponytail','hair_style',['y2kr_high_pony','sleek_high_ponytail'],'chrh_high_pony_root','높은 밑동의 꼬리','one high scalp tie point connects continuously to a free tail',['hair.style.gather.root_height'],[('tail','emerges_from','high_tie_point')]),
 (['H184','H210'],'hair.topology.braided_pigtails','hair_style',['sca_h11'],'chrh_two_braided_tails','각각 땋인 두 꼬리','two separate left and right gathers each continue into a braided tail',['hair.style.braid.bilateral_roots'],[('left_braid','emerges_from','left_gather'),('right_braid','emerges_from','right_gather')]),
 (['H185'],'hair.topology.half_up','hair_style',['y2kr_half_up'],'chrh_half_up_layers','풀린 아래층을 남긴 반묶음','the upper hair is gathered while a separate lower hair layer falls freely',['hair.style.gather.partial_fraction'],[('upper_hair','gathered_above','free_lower_layer')]),
 (['H219'],'hair.topology.cornrows','hair_style',['cornrows'],'chrh_scalp_braid_rows','두피 경로를 따르는 땋기','multiple continuous braid rows follow visible paths on the scalp',['hair.style.braid.scalp_paths'],[('braid_rows','follow','scalp_paths')]),
 (['H214'],'hair.topology.rope_twist','hair_style',[],'chrh_two_section_rope','두 덩어리의 나선 꼬임','two hair sections wind around each other along one continuous free length',['hair.style.twist.two_section_path'],[('hair_section_a','winds_around','hair_section_b')]),
 (['H229'],'hair.topology.locs','hair_style',['dreadlocks'],'chrh_loc_cord_surface','연속적인 록스 몸체','separate cord-like hair bodies retain continuous fiber surfaces along their lengths',['hair.style.locs.cord_surface'],[('cord_body','continues_along','hair_length')]),
 (['H278','H279'],'hair_color_state.peekaboo','hair_color',['sca_h20','y2kr_peekaboo'],'chrh_inner_color_reveal','겉층 아래 드러난 색','a differently colored inner hair layer is partly revealed beneath the outer layer',['hair.color.layer_partition'],[('outer_layer','partly_occludes','colored_inner_layer')]),
 (['H276'],'hair_color_state.split_color','hair_color',['sca_h19','y2kr_two_tone'],'chrh_split_color_regions','두 큰 모발 색 구역','the left and right hair regions carry distinct chosen colors separated spatially',['hair.color.lateral_partition'],[('left_color_region','adjacent_to','right_color_region')]),
 (['H269'],'hair_color_state.ombre','hair_color',['sca_h21'],'chrh_root_tip_gradient','뿌리에서 끝으로 색 전이','the chosen color changes gradually along the same hair lengths from roots toward tips',['hair.color.root_tip_transition'],[('root_color','transitions_along_length_to','tip_color')]),
 (['H272'],'hair_color_state.dip_dye','hair_color',[],'chrh_sharp_tip_color','끝 구역의 뚜렷한 배색','a distinct color occupies the terminal hair region with a comparatively clear transition',['hair.color.tip_boundary'],[('tip_color_region','ends_at_boundary_with','upper_base_region')]),
 (['H263'],'hair_color_state.money_piece','hair_color',['y2kr_money_piece'],'chrh_front_color_sections','얼굴 앞 강조 색 가닥','chosen lighter front hair sections frame the face against the base hair color',['hair.color.front_sections'],[('lighter_front_sections','frame','face')]),
 (['H260'],'hair_color_state.babylights','hair_color',[],'chrh_fine_highlight_sections','극세 밝은 색 가닥','many very fine lighter sections run among the base hair strands',['hair.color.highlight.width'],[('fine_lighter_sections','interspersed_with','base_strands')]),
 (['H368'],'hair_color_state.wet_look','hair_style',['slicked_back_wet','y2kr_wet_hair'],'chrh_wet_look_finish','젖어 보이는 연출 표면','compact aligned hair sections carry a glossy wet-looking finish',['hair.surface.gloss_clumping'],[('glossy_finish','lies_on','aligned_hair_sections')]),
 (['H369'],'hair_color_state.wet_hair','hair_style',['wet_damp_clumped_hair_state'],'chrh_damp_downward_weight','피부에서 떨어진 젖은 처짐','damp hair bundles lose airy volume and hang downward under coherent moisture weight, clear of the skin',['hair.moisture_and_configuration'],[('damp_bundles','hang_down_from','scalp_roots')]),
 (['H433'],'hair_color_state.ahoge','hair_style',['sca_h01'],'chrh_single_ahoge','한 긴 돌출 다발','one continuous long hair lock protrudes from the crown',['hair.style.crown.tuft_topology'],[('single_lock','protrudes_from','crown')]),
 (['H434'],'hair_color_state.antenna_hair','hair_style',['sca_h02'],'chrh_antenna_locks','두 개 이상 가는 돌출 다발','two or more thin hair locks protrude separately from their scalp roots',['hair.style.crown.tuft_topology'],[('thin_locks','protrude_from','scalp_roots')]),
 (['H441','H442'],'hair_color_state.twin_drills','hair_style',['sca_h05'],'chrh_tapered_drill_tails','끝으로 좁아지는 두 나선','two gathered hair masses coil into tapering conical spirals',['hair.style.gather.spiral_topology'],[('left_spiral','tapers_toward','left_tip'),('right_spiral','tapers_toward','right_tip')]),
 (['H447'],'hair.main.hair_neck_wrap','hair_style',[],'chrh_hair_neck_wrap','목을 둘러 이어지는 모발','one continuous length of the subject’s hair curves around the neck',['hair.style.body_overlap.neck'],[('hair_length','wraps','subject_neck')]),
 (['H204'],'hair.main.hair_formed_bow','hair_style',[],'chrh_hair_formed_bow','모발로 만든 보우','the hair itself forms two loops joined at a visible center',['hair.style.gather.bow_topology'],[('hair_loop_left','joins_at','hair_bow_center'),('hair_loop_right','joins_at','hair_bow_center')]),
 (['H386','H387'],'hair.main.ribbon_or_fabric_bow','wearable_accessory',['egr_attached_trailing_hair_ribbon'],'chrh_fabric_ribbon_attachment','모발에 연결된 천 리본','a fabric ribbon is visibly tied around the selected hair base',['hair.accessories','hair.accessories.material'],[('fabric_ribbon','tied_around','hair_base')]),
 (['H388'],'hair.main.scrunchie','wearable_accessory',['y2kr_scrunchie'],'chrh_scrunchie_attachment','밑동을 감싼 스크런치','a ruched fabric scrunchie encircles the selected gathered hair base',['hair.accessories.scrunchie_attachment'],[('scrunchie','encircles','gather_base')]),
 (['H393'],'hair.main.claw_clip','wearable_accessory',[],'chrh_claw_clip_attachment','다발을 잡는 집게핀','a visible claw clip grips the selected gathered hair section',['hair.accessories.clip_attachment'],[('claw_clip','grips','gathered_section')]),
 (['H416','H417'],'hair.main.daenggi','wearable_accessory',[],'chrh_daenggi_braid_end','땋은 끝에 연결된 댕기','a cloth daenggi is visibly connected to the end of the braid',['hair.accessories.daenggi_attachment'],[('daenggi','attached_to','braid_end')]),
]


def build():
    files=[p for p in PREFIXES if (OUT/(p+'-cards.json')).exists()]
    cards=[]; records=[]; pairs=[]
    for prefix in files:
        d=read(prefix+'-cards.json')
        cards.extend(dict(c, artifact_file=prefix+'-cards.json') for c in d['cards'])
        pairs.extend(dict(q, artifact_file=prefix+'-cards.json') for q in d.get('minimal_pairs', []))
        for s in read(prefix+'-sources.json')['sources']:
            records.append(dict(s, artifact_file=prefix+'-sources.json'))
    assert len({c['id'] for c in cards})==len(cards)
    by_card={c['id']:c for c in cards}; by_h=collections.defaultdict(list)
    for c in cards:
        for hid in keyword_ids(c): by_h[hid].append(c['id'])
    by_source={s['id']:s for s in records}
    assert len(by_source)==len(records)
    direct=[]; limited=[]; urls=[]
    for s in records:
        status=s.get('access_status',s.get('retrieval_status',s.get('read_status','unknown')))
        s['normalized_read_status']=status
        if any(x in status for x in ['only','limited','missing','mismatch','404']): limited.append(s['id'])
        else: direct.append(s['id'])
        if s.get('url'): urls.append(normalized_url(s['url']))
        for doc in s.get('documents',[]):
            if doc.get('url'): urls.append(normalized_url(doc['url']))
    save('SOURCE-CATALOG.json',dict(status='source_receipts_not_universal_definition_validation',
        counts=dict(source_records=len(records), current_direct_body_or_api_records=len(direct),
                    limited_or_search_only_records=len(limited), unique_url_strings=len(set(urls))),
        counting_rule='Records and unique URL strings differ; Danbooru grouped record includes documents. Direct body includes local salon cases, not universal standards.',
        direct_record_ids=direct, limited_record_ids=limited, sources=records))

    audit=read('KEYWORD-CROSSWALK.json');color=read('color-state-cards.json')
    color_disp={r['id']:r for r in color['reference_keyword_dispositions']}
    accessory={r['id']:r for r in read('ACCESSORY-DISPOSITION.json')['rows']}
    result=[]
    for row in audit['rows']:
        hid=row['id']; links=by_h.get(hid,[])
        r=dict(row, semantic_card_refs=links,
               research_route=('detailed_card_and_boundary_review' if links else 'shared_axis_or_definition_followup'),
               semantic_equivalence='not_implied_by_input_mapping',runtime_adoption='not_performed')
        if hid in color_disp:r['specialist_disposition']=color_disp[hid]
        if hid in accessory:r['attachment_disposition']=accessory[hid]
        if hid=='H369':r['routing_override']='Actual moisture counterpart. topology wet_look related-card mapping is boundary research, not synonymy with H368.'
        if hid=='H432':r['research_route']='nonvisual_context_only_no_hair_obligation'
        result.append(r)
    save('RESEARCH-CROSSWALK.json',dict(status='research_routes_not_complete_independent_validation_of_454_definitions',
        term_count=len(result),terms_with_detailed_card_links=sum(bool(r['semantic_card_refs']) for r in result),rows=result))

    spec=importlib.util.spec_from_file_location('read_only_hair_audit',OUT/'audit_keyword_coverage.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    current_candidates,current_profiles,_,_=m.source_rows()
    entries={(r['slot'],r['row']['id']):r for r in current_candidates}
    profile_refs={r['row']['id']:r for r in current_profiles}
    draft=[]
    for hids,cid,slot,reuse,new_id,label,wording,properties,relations in SPECS:
        assert cid in by_card
        assert (slot,new_id) not in entries
        found=[dict(slot=slot,id=eid,source=entries[(slot,eid)]['source']) for eid in reuse if (slot,eid) in entries]
        mismatched=[dict(id=eid,actual_slots=[s for s,i in entries if i==eid]) for eid in reuse if (slot,eid) not in entries]
        action='review_and_enrich_existing' if found else ('review_cross_slot_owner_before_new' if mismatched else 'propose_new_after_equivalence_review')
        runtime=dict(id=found[0]['id'] if found else new_id,ko=label,en=wording,
            concept_units=[wording],relations=[dict(id=f'r{i+1}',type=b,subject=a,object=c) for i,(a,b,c) in enumerate(relations)],
            affected_dimensions=['appearance'],affected_properties=[dict(dimension='appearance',target='main_subject',property=p) for p in properties])
        c=by_card[cid]
        draft.append(dict(proposed_slot=slot, reference_keyword_ids=hids, semantic_card_ref=cid,
            source_refs=source_ids(c), existing_candidate_matches=found, cross_slot_review=mismatched,
            action=action,provisional_new_id=new_id,
            source_support_boundary=c.get('source_support_status',c.get('definition_status',c.get('confidence'))),
            runtime_entry_draft=runtime,
            prerequisites=['Confirm semantic equivalence and current owner source','Validate property paths against actual locks','Review maintenance successor and positive retrieval prototype'],
            activation='optional_after_independent_core_and_explicit_adoption', status='proposal_not_inserted'))
    save('CANDIDATE-DRAFTS.json',dict(status='review_wrapper_not_runtime_extension',draft_count=len(draft),
        existing_source_snapshot='CURRENT-DATA-AUDIT.json',
        schema_boundary='Only runtime_entry_draft is runtime-shaped; all IDs and properties require source owner/schema/semantic review. Existing matches are not equivalence assertions.', drafts=draft))

    family_specs=[
      ('hime_shelves',['hair-cut-hime'],['hime_cut_structural'],'reuse_narrow_structure_with_variant_review'),
      ('jellyfish_cap',['hair-cut-jellyfish'],[],'new_profile_if_selected_cap_duty_requires_it'),
      ('perimeter_and_stack',['hair-cut-a_line','hair-cut-stacked_bob'],[],'independent_candidates_first_optional_joint_profile'),
      ('fringe_axes',['hair-cut-full_bangs','hair-cut-blunt_bangs','hair-cut-micro_bangs'],[],'atomic_candidates_joint_profile_only_if_explicitly_selected'),
      ('fade_geometry',['hair-cut-low_fade','hair-cut-drop_fade','hair-cut-skin_fade'],[],'independent_height_path_endpoint'),
      ('gather_bases',['hair.topology.twintails','hair.topology.high_ponytail'],['bilateral_twin_tail_gather'],'reuse_count_and_add_scoped_root_height'),
      ('half_up_layers',['hair.topology.half_up'],[],'reuse_y2k_lower_layer_relation'),
      ('scalp_braid_path',['hair.topology.french_braid','hair.topology.dutch_braid','hair.topology.cornrows'],['cornrow_scalp_row_topology'],'separate_crossing_and_continuous_scalp_path'),
      ('free_braid_twist',['hair.topology.free_hanging_braid','hair.topology.fishtail_braid','hair.topology.rope_twist'],[],'reuse_hanging_braid_add_repetition_boundary'),
      ('loc_body_and_roots',['hair.topology.locs','hair.topology.box_braids','hair.topology.knotless_braids'],['locs_cord_structure'],'keep_body_partition_installation_axes_separate'),
      ('color_partition',['hair_color_state.split_color','hair_color_state.peekaboo','hair_color_state.underlights'],[],'reuse_subculture_y2k_profiles_and_candidates'),
      ('root_tip_and_paint',['hair_color_state.balayage_process','hair_color_state.balayage_pattern','hair_color_state.ombre'],['balayage_ribbon_color_placement'],'P0_narrow_pattern_preserve_explicit_method_result_separation'),
      ('wet_finish_moisture',['hair_color_state.wet_look','hair_color_state.wet_hair'],['wet_damp_clumped_hair_state'],'P0_split_finish_and_water_state_preserve_weight_alternative'),
      ('fantasy_tuft_spiral',['hair_color_state.ahoge','hair_color_state.antenna_hair','hair_color_state.twin_drills'],[],'reuse_subculture_owner_count_taper'),
      ('material_attachment',['hair.main.hair_formed_bow','hair.main.ribbon_or_fabric_bow','hair.main.fabric_scarf','hair.main.hair_neck_wrap'],[],'separate_material_owner_and_continuity_with_source_holds'),
      ('cultural_attachment',['hair.main.daenggi','hair.main.sangtu'],[],'optional_contextual_structure_no_identity_inference'),
    ]
    bundles=[]
    for name,ids,reuse,action in family_specs:
        assert all(i in by_card for i in ids)
        bundles.append(dict(id='research_family_'+name,semantic_card_refs=ids,
            existing_profile_refs=[dict(id=i,source=profile_refs[i]['source']) for i in reuse],
            proposed_action=action,
            minimum_signature_refs=[dict(card_id=i,field=('minimum_visible_signature' if 'minimum_visible_signature' in by_card[i] else 'minimum_visual_signature' if 'minimum_visual_signature' in by_card[i] else 'minimum_signature')) for i in ids],
            gate_policy='all_of_selected_duties; missing visibility is UNOBSERVABLE_NOT_PASS',
            runtime_serialization='author authored_components v1/v2; do not copy research keys or generated gate fields',
            candidate_ids=[d['runtime_entry_draft']['id'] for d in draft if d['semantic_card_ref'] in ids],
            activation='association_does_not_create_hard_activation',status='proposal_not_integrated'))
    save('PROFILE-AND-BUNDLE-PLAN.json',dict(status='design_wrapper_not_profile_registry',family_count=len(bundles),families=bundles))

    plan_cases=[
      ('wet_dry_gel','A dry, gel-set wet-look finish; no water event.', 'H368','Wet-looking finish permitted; actual moisture/contact/rain obligations must not be added.'),
      ('wet_nonadherent','Damp bundles hanging away from face and clothing.', 'H369','Actual moisture counterpart preserves downward-weight alternative without invented skin adhesion.'),
      ('wet_explicit_contact','Rain-damp temple strands adhering to the cheek.', 'H369','Selected local cheek contact must remain visible; generic no-contact variant cannot satisfy this duty.'),
      ('balayage_ombre','Balayage coloring with an ombre gradient.', 'H265,H269','Method and gradient may coexist; no automatic not-ombre gate or universal dark-root requirement.'),
      ('stacked_a_line','An A-line bob with stacked rear layers.', 'H053,H097','Front/rear perimeter and occipital stack coexist on correct regions.'),
      ('bang_axes','Full blunt micro bangs.', 'H128,H129,H134','Coverage, edge and length coexist; no unasked black colour or demographic attributes.'),
      ('box_knotless','Knotless braids in box-shaped scalp partitions.', 'H217,H218','Partition and root/installation claims coexist; final image alone does not prove installation.'),
      ('bow_material','A cloth bow in hair versus a bow made from the hair.', 'H204,H387','Separate material continuity and attachment. Shared bare alias cannot substitute one for the other.'),
      ('scarf_material','A fabric hair scarf versus long hair wrapping the neck.', 'H397,H447','Different material/owner/path; distinct namespaces and selected duties.'),
      ('color_light','Brown hair under teal light, versus teal hair under neutral light.', 'H236','Light/grade effect cannot count as hair pigment colour or bypass hair lock.'),
      ('negated_braid','Loose hair, no braids, beside a braided chair.', 'H210','Background braid is not subject hair; excluded hair braid cannot become a selected duty.'),
      ('owner_split','Two subjects with different hair colors and different tail counts.', 'H184,H276','No cross-owner aggregation of color regions or fastening roots.'),
      ('generic_graduation','Graduation portrait versus a graduated haircut.', 'H052','Event candidate cannot establish hair-cut layering; owner-qualified sense required.'),
      ('fine_density','Fine-looking strands with high apparent coverage.', 'H031,H033','Diameter, apparent coverage and volume independent; no actual follicle count without suitable evidence.'),
      ('parent_lock','Hair color is locked while an inner-layer candidate is proposed.', 'H278','Parent lock rejects inner-layer color mutation; no dimension or alias bypass.'),
      ('source_origin','Identical visible loc forms with different documented installation histories.', 'H229,H230','Image-level topology may match; source origin remains not_proven without process evidence.'),
      ('clinical_patch','A white front hair patch with no medical history.', 'H324,H325','Appearance may be described; no poliosis diagnosis or age inference.'),
      ('neon_glow','Neon-colored hair versus hair contributing emitted light.', 'H354,H357','Saturation does not prove emission; light contribution is a separate selected relation.'),
      ('interest_only','Trichophilia as a topic, without any requested hairstyle.', 'H432','No mandatory hair appearance, behavior or interest inferred from the topic.'),
      ('hidden_root','A ponytail hanging low with the fastening base hidden.', 'H174,H175','High/low base cannot pass from tail-tip position; observation UNOBSERVABLE_NOT_PASS.'),
    ]
    cases=[dict(id='MAIN-'+name,layer='source_scope_retrieval_or_prompt',input=inp,glossary_ids=hids.split(','),expected=exp,status='proposed_not_run') for name,inp,hids,exp in plan_cases]
    cases.extend(dict(id=q['id'],layer='controlled_minimal_pair',status='proposed_not_run',design=q) for q in pairs)
    with (OUT/'VALIDATION-CASES.jsonl').open('w') as f:
        for q in cases:f.write(json.dumps(q,ensure_ascii=False)+'\n')
    summary=dict(status='research_assembled_not_runtime_or_pixel_validation', semantic_cards=len(cards),
                 term_routes=len(result),terms_with_detailed_card_links=sum(bool(r['semantic_card_refs']) for r in result),
                 candidate_drafts=len(draft),profile_bundle_families=len(bundles),
                 controlled_minimal_pairs=len(pairs),additional_boundary_cases=len(plan_cases),
                 case_count=len(cases),source_counts=read('SOURCE-CATALOG.json')['counts'])
    save('ASSEMBLY-SUMMARY.json',summary)
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':build()
