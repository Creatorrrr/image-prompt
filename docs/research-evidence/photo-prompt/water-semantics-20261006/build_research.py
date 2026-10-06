"""Compile the hand-authored research inputs; never edits live assets."""
import collections
import hashlib
import importlib.util
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'

def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def load(name):
    return json.loads((OUT/name).read_text())

def parse_rows(name, n):
    for number,line in enumerate((OUT/name).read_text().splitlines(),1):
        if not line.strip() or line.startswith('#'): continue
        fields=line.split('|')
        if len(fields)!=n: raise ValueError(f'{name}:{number}: {len(fields)} fields, expected {n}')
        yield fields

def seeds():
    original=load('SOURCE-CONVERSATION.json')
    rows=[]
    group=0
    heading=''
    counter=collections.Counter()
    for line in original['assistant_text'].splitlines():
        m=re.match(r'## (\d+)\. (.+)',line)
        if m: group=int(m.group(1)); heading=m.group(2)
        if 1<=group<=19 and line.startswith('|'):
            cells=[s.strip() for s in line.strip('|').split('|')]
            if len(cells)!=2 or cells[0] in {'용어','용어·생물','표현'} or set(cells[0])<={'-'}: continue
            counter[group]+=1
            rows.append({'seed_id':f'S{group:02}-{counter[group]:02}','section':group,'section_title':heading,'row':counter[group],'term':cells[0],'original_explanation':cells[1],'provenance':'read_thread_cached_text'})
    headings={20:'의복·관능·성적 맥락에서 쓰이는 표현',21:'재난·위험·오염 관련 용어',22:'죽음·폭력·수중 공포의 어휘',23:'신화·민속·의례·상징',24:'소리·한국어 묘사·사진 구성에 유용한 표현'}
    for group,term,explanation in parse_rows('TAIL-TABLES.psv',3):
        group=int(group);counter[group]+=1
        rows.append({'seed_id':f'S{group:02}-{counter[group]:02}','section':group,'section_title':headings[group],'row':counter[group],'term':term,'original_explanation':explanation,'provenance':'browser_rendered_table_transcription'})
    if len(rows)!=345: raise ValueError(f'Seed extraction returned {len(rows)}, expected 345')
    save('SEED-INVENTORY.json',{'schema':'water-seed-inventory/v1','conversation_id':original['conversation_id'],'completeness':'All 24 numbered tables recovered: 345 rows. Full prose remains a bounded 20000-character cached excerpt.','source_reading':'Read-only browser DOM recovered tables 20-24; first 19 table rows also matched the visible DOM inventory.','section_counts':dict(sorted(counter.items())),'rows':rows})
    return rows

def sources():
    rows=[]
    for id_,title,url,type_,status,claim in parse_rows('SOURCE-REGISTRY.psv',6):
        rows.append({'id':id_,'title':title,'url':url,'type':type_,'verification':status,'supported_scope':claim,'retrieved_on_kst':'2026-10-06','visual_proposal_boundary':'Source supports the named meaning/mechanism or usage; card staging, owner graph, effects and pixel criteria are researcher-authored proposals, not source quotations.'})
    save('SOURCES.json',{'schema':'water-research-sources/v1','sources':rows,'not_verified_as_full_text':['CVPR full PDFs returned errors; indexed author abstract used only','Aquaphilia gallery exposes title usage only','No community prevalence or clinical diagnosis established'],'failed_fetches':[{'url':'https://openaccess.thecvf.com/content_CVPR_2019/html/Akkaynak_Sea-Thru_A_Method_for_Removing_Water_From_Underwater_Images_CVPR_2019_paper.html','result':'403'},{'url':'https://openaccess.thecvf.com/content_cvpr_2018/papers/Akkaynak_A_Revised_Underwater_CVPR_2018_paper.pdf','result':'403'},{'url':'https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf','result':'open error; indexed abstract read'},{'url':'https://www.usgs.gov/water-science-school/science/water-cycle','result':'timeout'},{'url':'https://oceanservice.noaa.gov/facts/waves.html','result':'404; replaced with wavesinocean.html and tutorial_currents/03coastal1.html'}]})
    md=['# 공개 출처와 근거 범위','','본문 열람·검색 excerpt·논문 abstract·제목 용례를 구분한다. 모든 사진 배치·관계·효과·검증 명세는 연구자 제안이다.','']
    for row in rows:
        md.extend([f"- **{row['id']}** — [{row['title']}]({row['url']}) · `{row['verification']}`. {row['supported_scope']}"])
    (OUT/'SOURCES.md').write_text('\n'.join(md)+'\n')
    return {r['id']:r for r in rows}

def expand_refs(text):
    result=[]
    for part in text.split(';'):
        section,rows=part.split(':')
        for span in rows.split(','):
            bounds=span.split('-');a=int(bounds[0]);b=int(bounds[-1])
            result.extend(f'S{int(section):02}-{i:02}' for i in range(a,b+1))
    return result

OWNER_FILES={
    'default':['photo_prompt_aquatic_structure_extension.json','photo_prompt_visual_obligations_aquatic_structure.json'],
    'hair_style':['photo_prompt_tags.json','photo_prompt_visual_obligations.json'],
    'garment_detail':['photo_prompt_textile_surface_extension.json','photo_prompt_visual_obligations_textile_surface.json'],
    'wardrobe_style':['photo_prompt_swimwear_extension.json','photo_prompt_visual_obligations_swimwear.json'],
    'skin_condition':['photo_prompt_tags.json','photo_prompt_visual_obligations_tactile_reality.json'],
    'reflection_logic':['photo_prompt_emotional_place_extension.json','photo_prompt_realistic_background_extension.json'],
    'situation_context':['RESEARCH_GLOSSARY_ONLY'],
}
REUSE={
    'W004':['dew_water_droplets_texture'],
    'W006':['wet_receipt_paper_texture'],
    'W019':['water_droplet_freeze'],
    'W020':['wet_surface'],
    'W027':['water_refraction_texture'],
    'W046':['sparkling_water_reflection_highlights'],
    'W047':['ep_wet_reflection_owner_alignment','rb_wet_dry_boundary_candidate'],
    'W049':['underwater_caustics','underwater_caustic_light','surface_caustic_light','pool_caustic_reflections','water_caustic_table_pattern'],
    'W059':['wetland_hydrology_mosaic_aesthetic','wetland_shallow_channel_mosaic_location'],
    'W064':['riparian_floodplain_gradient_aesthetic'],
    'W080':['intertidal_high_low_exposure_zonation','intertidal_wet_dry_biotic_band_surface'],
    'W091':['coral_reef','coral_reef_cross_shore_location'],
    'W094':['mangrove_water_root_canopy_depth_frame'],
    'W117':['wet_rock_biofilm_surface'],
    'W119':['rb_water_path_stain_candidate','rb_water_path_stain'],
    'W121':['ep_wet_dry_boundary_footprint','rb_wet_dry_boundary_candidate'],
    'W143':['underwater_suspended_midframe'],
    'W149':['sw_candidate_wetsuit','sw_wetsuit'],
    'W155':['sw_candidate_wet','sw_wet'],
    'W156':['wet_damp_clumped_hair_state','slicked_back_wet','y2kr_wet_hair'],
    'W160':['wet_look_bodycon'],
    'W161':['sw_wet'],
    'W162':['sheer_garment_optical_layering'],
    'W175':['ghost_ship_former_vessel_breach'],
}

def cards(seed_rows,source_map):
    seed_map={r['seed_id']:r for r in seed_rows}
    existing=load('EXISTING-DATA-CATALOG.json')
    live_ids={r['id'] for r in existing['all_ids']}
    data=json.loads((ASSETS/'photo_prompt_tags.json').read_text())
    slot_dimensions=data['candidate_semantic_policy']['slot_dimensions']
    units=[];candidates=[];mappings=[]
    for id_,refs,ko,slot,mode,priority,source_refs,components,relations,boundary in parse_rows('CARD-INPUT.psv',10):
        refs=expand_refs(refs)
        if any(x not in seed_map for x in refs): raise ValueError((id_,'bad seeds',refs))
        if slot not in data['slots']: raise ValueError((id_,'unknown slot',slot))
        pubs=[] if source_refs=='-' else source_refs.split(',')
        if any(x not in source_map for x in pubs): raise ValueError((id_,'bad source',pubs))
        components=[x.strip() for x in components.split(';')]
        graph=[]
        for i,r in enumerate(relations.split(';'),1):
            subject,type_,object_=r.split('>')
            graph.append({'id':f'{id_.lower()}_relation_{i}','type':type_,'subject':subject,'object':object_,'owner_binding':{'scene':id_,'subject_ref':f'{id_}:{subject}','object_ref':f'{id_}:{object_}','continuity':'same named entities within this unit; actual scene owners must be resolved during adoption'}})
        unit={'id':id_,'ko':ko,'seed_refs':refs,'seed_terms':[seed_map[x]['term'] for x in refs],'mode':mode,'priority':priority,'proposed_slot':slot,'observable_components_proposal':[{'id':f'{id_.lower()}_component_{i}','positive_predicate_en':s} for i,s in enumerate(components,1)],'relations_proposal':graph,'confusion_boundary':boundary,'public_source_refs':pubs,'claim_status':'MEANING_AND_MECHANISM_WITH_AUTHORED_VISUAL_PROPOSAL' if pubs else 'SEED_MEANING_ONLY_ADDITIONAL_PRIMARY_SOURCE_REQUIRED','context_limits':'Still pixels do not establish chemical identity, safety, measured quantities, history, periodicity, sound, smell, mental state, consent or clinical diagnosis. Retain named context separately.','qualification':'PROPOSED_NOT_RUN'}
        units.append(unit)
        refs_existing=[r for r in existing['all_ids'] if r['id'] in REUSE.get(id_,[])]
        missing=sorted(set(REUSE.get(id_,[]))-live_ids)
        action='context_only' if mode=='context' else 'split_family_before_adoption' if mode=='family' else 'compare_existing_then_extend_or_sibling' if refs_existing else 'new_atom_proposal'
        mapping={'unit_id':id_,'adoption_action':action,'existing_refs':refs_existing,'missing_lookup_ids':missing,'target_files_proposal':OWNER_FILES.get(slot,OWNER_FILES['default']),'slot':slot,'known_slot_dimensions':slot_dimensions.get(slot,[]),'property_mapping_status':'UNVERIFIED_PROPOSAL: resolve actual owner, target and consumed property paths before activation','source_registration':'New candidate/profile files must be registered once in photo_prompt_source_manifest.json. Existing owners remain in their registered files.','qualification':'PROPOSED_NOT_RUN'}
        mappings.append(mapping)
        if mode=='visual':
            candidate={'id':f'water_research_{id_.lower()}','unit_id':id_,'ko':ko,'slot_proposal':slot,'concept_terms_proposal':components,'concept_units_proposal':components,'relations_proposal':graph,'positive_retrieval_text_proposal':'; '.join(components),'affected_dimensions_proposal':slot_dimensions.get(slot,[]),'affected_properties_proposal':[],'property_status':'NOT_MAPPED_DO_NOT_ADOPT','owner_resolution_required':True,'source_status':unit['claim_status'],'eligible_for_hard_activation':False,'hard_eligibility_policy_proposal':'Direct positive requester evidence for the named carrier and relation, or legitimate explicit selected opt-in duty; frozen definition overrides and property locks prevail. Retrieval alone grants no duty.','qualification':'PROPOSED_NOT_RUN'}
            candidates.append(candidate)
    if len({u['id'] for u in units})!=len(units): raise ValueError('duplicate units')
    save('SEMANTIC-UNITS.json',{'schema':'water-research-semantic-units/v1','unit_count':len(units),'units':units})
    save('CANDIDATE-DRAFTS.json',{'schema':'water-research-candidate-drafts/v1','count':len(candidates),'qualification':'PROPOSED_NOT_RUN','warning':'These are research projections. Property effects, actual owners, validators, aliases and hard activation are not yet mapped. No direct runtime copy.','candidates':candidates})
    save('RUNTIME-MAPPING.json',{'schema':'water-research-runtime-mapping/v1','mappings':mappings,'current_contracts':{'source_manifest':'photo-source-manifest/v1','flat_components':'photo-authored-visual-components/v1','grouped_components':'photo-authored-visual-components/v2','candidate_pack':'photo-candidate-pack/v6'},'limits':'File proposals and lexical existing refs are not approved equivalence or verified runtime effects.'})
    coverage=[]
    for seed in seed_rows:
        assigned=[u for u in units if seed['seed_id'] in u['seed_refs']]
        coverage.append({'seed_id':seed['seed_id'],'term':seed['term'],'unit_refs':[u['id'] for u in assigned],'route_modes':sorted({u['mode'] for u in assigned}),'status':'ROUTED_RESEARCH_NOT_RUNTIME' if assigned else 'UNROUTED'})
    save('SEED-COVERAGE.json',{'schema':'water-research-seed-coverage/v1','seed_count':len(seed_rows),'routed':sum(bool(r['unit_refs']) for r in coverage),'rows':coverage})
    md=['# 물 시각 의미 카드','','모든 component·관계·gate는 연구자 제안이다. 가족(`family`)은 여러 의미를 유지한 분해 대기 카드이고, 맥락(`context`)은 외관만으로 확정할 수 없는 의미다. `visual`만 후보 초안을 만들며 그 초안도 hard activation·property·owner 검증 전이다.','']
    for u in units:
        md.extend([f"## {u['id']} · {u['ko']} · {u['priority']}",'',f"원 대화: {', '.join(u['seed_terms'])}. 경로: `{u['mode']}` → `{u['proposed_slot']}`.",'','관찰 명세:',''])
        md.extend('- '+c['positive_predicate_en'] for c in u['observable_components_proposal'])
        md.extend(['', '관계: '+'; '.join(f"`{r['subject']} → {r['type']} → {r['object']}`" for r in u['relations_proposal'])+'.', '', '오인 경계: '+u['confusion_boundary'], ''])
        if u['public_source_refs']:
            md.append('관련 근거: '+', '.join(f"[{source_map[x]['title']}]({source_map[x]['url']})" for x in u['public_source_refs'])+'. 외형 투영과 source의 사실 주장은 구분한다.')
        else: md.append('근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.')
        md.extend(['','후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.',''])
    (OUT/'SEMANTIC-CARDS.md').write_text('\n'.join(md))
    return units,candidates,mappings,coverage

def plans(units,candidates):
    by_id={x['id']:x for x in units}
    bundle_groups={
        'micro_water_surface':['W004','W006','W007','W014','W026','W027','W028'],
        'air_water_optics':['W046','W047','W048','W049','W050','W051','W052','W053','W190'],
        'shore_wave_relations':['W032','W033','W034','W035','W036','W080','W169'],
        'river_topology':['W064','W067','W069','W070','W073'],
        'ice_and_phase':['W014','W039','W040','W042','W043','W045'],
        'deep_sea_particles':['W088','W089','W090','W052','W054','W055'],
        'rooted_aquatic_habitat':['W092','W093','W094','W097','W098'],
        'diver_equipment_continuity':['W144','W146','W150','W151','W152'],
        'wet_carrier_and_cloth':['W155','W156','W157','W160','W161','W162'],
        'water_aftermath':['W116','W119','W120','W121','W166','W175'],
        'myth_and_context':['W163','W165','W173','W176','W178','W180','W181','W182','W183','W184','W185','W187','W189'],
    }
    bundles=[{'id':'water_bundle_'+k,'unit_refs':v,'type':'optional_review_group_not_scene_recipe','selection_policy':'Review members separately. A group never adopts all effects, strengthens a context meaning into a hard visual duty, or creates a fixed scene.','qualification':'PROPOSED_NOT_RUN'} for k,v in bundle_groups.items()]
    save('BUNDLE-DRAFTS.json',{'schema':'water-research-bundle-drafts/v1','bundles':bundles})
    regressions=[]
    scenarios={
        'W006':['종이 모서리만 물에 닿아 그 안쪽으로 젖은 경계가 번진다.','종이 위에 물결 무늬만 인쇄되어 있다.'],
        'W007':['유리 컵 안 물이 벽과 만나는 가장자리에서 살짝 올라간다.','컵 밖에 맺힌 물방울을 보여준다.'],
        'W026':['방울이 수면에 닿은 중심 주위로 얇은 테두리가 왕관처럼 솟았다.','물 옆에 왕관 장식이 놓여 있다.'],
        'W049':['얕은 물 바닥의 돌 위로 빛이 가는 그물무늬를 만든다.','수면의 반짝임만 보고 바닥은 전혀 보이지 않는다.'],
        'W050':['물속에서 위를 바라본 밝은 바깥 풍경의 창과 주변의 수중 반사가 함께 보인다.','잠수정의 둥근 창으로 물 밖을 본다.'],
        'W070':['자갈톱을 사이에 둔 물길들이 갈라졌다가 아래쪽에서 다시 만난다.','여러 물길이 바다로만 갈라져 나간다.'],
        'W092':['바위 고정 부위에서 줄기가 올라가 넓은 엽체로 이어지는 수중 켈프.','해저에 뿌리내린 가는 잘피 잎.'],
        'W101':['젤리 같은 몸을 따라 길게 난 빗살판 줄에서 무지갯빛이 반사된다.','촉수 끝마다 파란 LED처럼 빛나는 해파리.'],
        'W144':['수면에 엎드린 인물의 입에 연결된 스노클 끝이 물 위로 나와 있다.','물속 인물의 입에는 탱크 호스가 연결되어 있다.'],
        'W151':['수면 부유체에 채집 그물주머니가 매달리고 잠수 작업자가 같은 부유체를 짚는다.','끈 없이 떨어진 부표와 일반 스쿠버 배낭.'],
        'W156':['물 밖 젖은 머리가 여러 무거운 다발로 뭉쳐 목에 일부 붙어 있다.','물속에서 뿌리에 이어진 머리카락이 넓게 떠 있다.'],
        'W162':['지정한 얇은 천의 섬유와 솔기는 남으면서 그 뒤의 요청된 표면이 일부 비친다.','불투명한 젖은 옷의 재질만 표현한다.'],
        'W169':['쇄파 구간 사이에서 좁은 거품 띠가 해안 바깥으로 이어진다.','배수구 중심으로 내려가는 깔때기 소용돌이.'],
        'W175':['물에 잠긴 방의 문틀과 바닥 연결이 수면 아래까지 이어진다.','물이 없는 어두운 폐건물.'],
        'W182':['인간 상체와 물고기 하체가 같은 몸으로 이어지는 인어.','여성 얼굴에 새 몸이 이어지는 초기 세이렌.'],
        'W190':['한 사진의 수면 위 갈대 줄기가 수면 아래 뿌리와 이어진다.','두 장의 독립 사진을 위아래 붙인 콜라주.'],
    }
    for id_,(positive,negative) in scenarios.items():
        regressions.append({'id':'water_regression_'+id_.lower(),'unit_id':id_,'positive_request':positive,'adjacent_negative':negative,'mutations':['remove_one_required_component','detach_relation_endpoint','assign_effect_to_other_owner','negate_requested_relation','use_advisory_hit_without_selection','conflict_with_locked_property','requester_definition_override','hide_required_relation_in_crop'],'expected':'Preserve the positive meaning; reject false hard activation/equivalence and owner or lock bypass.','qualification':'PROPOSED_NOT_RUN','independence':'Authored by this researcher after seeing the cards; not a blind holdout.'})
    save('REGRESSION-PLAN.json',{'schema':'water-regression-plan/v1','case_groups':regressions,'live_suites_proposal':['tests.test_photo_candidate_semantics','tests.test_photo_visual_profile_retrieval','tests.test_photo_positive_retrieval','tests.test_photo_core_retrieval','tests.test_photo_authorial_core_v6','tests.test_photo_tactile_reality_semantics','tests.test_photo_natural_environment_semantics','tests.test_photo_swimwear_semantics','tests.test_photo_textile_opacity_effect_scope','tests.test_photo_object_morphology_ownership','tests.test_photo_structure_maintenance','tests.test_photo_semantic_index','tests.test_photo_prepack_isolation'],'qualification':'PROPOSED_NOT_RUN'})
    pixels=[]
    for id_,scenario in scenarios.items():
        u=by_id[id_]
        pixels.append({'id':'water_pixel_'+id_.lower(),'unit_id':id_,'scenario':scenario[0],'confound':scenario[1],'all_of_components':[x['positive_predicate_en'] for x in u['observable_components_proposal']],'all_of_relations':u['relations_proposal'],'visibility':'Each required carrier and both relation endpoints must be assessable at original resolution. Preserve requester framing.','verdicts':['PASS_ALL_REQUIRED','FAIL_PARTIAL_IS_FAIL','UNOBSERVABLE_NOT_PASS','BLOCKED_UNSCORED'],'qualification':'PROPOSED_NOT_RUN'})
    save('PIXEL-QUALIFICATION-PLAN.json',{'schema':'water-pixel-qualification-plan/v1','groups':pixels,'comparison':'Freeze independent requests and cores before inspecting candidate data. A uses baseline authored sources; B uses adopted sources with the same preserved requester meaning, model and exposed settings. Log available randomness; do not claim unavailable seed control. Multiple generated attempts are needed before attributing improvement.','evidence_layers':['retrieval','candidate_exposure','selected_effects','literal_prompt_binding','runtime_preflight','native_pixels','user_acceptance'],'qualification':'PROPOSED_NOT_RUN'})

def prototypes(units):
    path=ROOT/'skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py'
    spec=importlib.util.spec_from_file_location('water_research_profile_contract',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    profiles=[];checks=[]
    for id_ in ['W007','W049','W146','W190']:
        u=next(x for x in units if x['id']==id_)
        components=[]
        for i,c in enumerate(u['observable_components_proposal'],1):
            phrase=c['positive_predicate_en']
            components.append({'id':f'{id_.lower()}_component_{i}','match_terms':[phrase],'evidence_field':f'{id_.lower()}_component_{i}_phrase','evidence_terms':[phrase],'min_content_words':3,'instruction':'Preserve this visible component and its named carrier in the same scene: '+phrase+'.','render_gate':{'id':f'vo_water_research_{id_.lower()}_{i}','review_scale':'native','description':phrase+'. The named component must remain connected to its correct carrier in the saved original image.'}})
        source={'id':'water_research_prototype_'+id_.lower(),'category':'aquatic_structure_research','activation':{'exact_terms':[],'semantic_discovery_requires_component_evidence':True},'semantics':{'definition':'; '.join(c['positive_predicate_en'] for c in u['observable_components_proposal'])},'concept_candidate':{'concept_terms':[c['positive_predicate_en'] for c in u['observable_components_proposal']]},'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components}}
        compiled=module.compile_visual_profile(source)
        profiles.append({'unit_id':id_,'source_prototype':source,'compiled_format_preview':{k:compiled[k] for k in ['required_evidence_fields','evidence_requirements','render_gates','composition_instruction']},'status':'COMPILER_FORMAT_ONLY_NOT_REGISTRY_OR_PIXEL_QUALIFIED','missing':'Real aliases, activation, relation owner/target/property mapping, effect compatibility and full registry validation.'})
        checks.append({'unit_id':id_,'component_count':len(components),'evidence_field_count':len(compiled['required_evidence_fields']),'render_gate_count':len(compiled['render_gates']),'format_pass':len(components)==len(compiled['render_gates'])==len(compiled['required_evidence_fields'])})
    save('PROFILE-PROTOTYPES.json',{'schema':'water-research-profile-prototypes/v1','compiler_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'profiles':profiles,'format_checks':checks,'proof_boundary':'Only the existing compiler format was exercised; nothing registered, indexed, exposed, selected or rendered.'})
    return checks

def main():
    rows=seeds();source_map=sources();units,candidates,mappings,coverage=cards(rows,source_map);plans(units,candidates);checks=prototypes(units)
    stats={'seed_rows':len(rows),'sections':len({r['section'] for r in rows}),'semantic_units':len(units),'mode_counts':dict(collections.Counter(u['mode'] for u in units)),'candidate_drafts':len(candidates),'sources':len(source_map),'priority_counts':dict(collections.Counter(u['priority'] for u in units)),'routed_seeds':sum(bool(r['unit_refs']) for r in coverage),'unrouted_seeds':[r for r in coverage if not r['unit_refs']],'missing_existing_ids':[{'unit_id':r['unit_id'],'missing':r['missing_lookup_ids']} for r in mappings if r['missing_lookup_ids']],'profile_compiler_checks':checks,'research_status':'DRAFT_PENDING_PACKAGE_VALIDATION','runtime_adoption':'NOT_PERFORMED','index_rebuild':'NOT_PERFORMED','candidate_exposure':'NOT_PERFORMED','image_generation':'NOT_PERFORMED'}
    save('RESEARCH-STATS.json',stats)
    print(json.dumps(stats,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
