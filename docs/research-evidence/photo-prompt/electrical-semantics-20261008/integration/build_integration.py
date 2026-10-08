#!/usr/bin/env python3
"""Reviewed electricity source adoption; research/provenance stays outside runtime."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RESEARCH = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
CANDIDATE_FILE = 'photo_prompt_electrical_relations_extension.json'
PROFILE_FILE = 'photo_prompt_visual_obligations_electrical_relations.json'

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

# Temporal records, reported phenomena, specialist explanatory/medical families,
# and purpose-only contexts need their own reviewed realization, not a generic
# electric-looking scene. Their research is retained with an explicit disposition.
DEFER = {
    'EL021': 'Sequence/exposure history is not a single-frame electrical duty.',
    'EL023': 'Reported ball-lightning identity cannot be inferred from a rounded glow.',
    'EL032': 'Gamma detector/model requires a separately authored scientific panel.',
    'EL033': 'Occulted solar-corona geometry needs a separate solar observation context.',
    'EL055': 'Flicker needs multiple time-bound frames.',
    'EL058': 'Opposite/like-charge diagram variants require a separate arrow/legend review.',
    'EL059': 'Probability-density model needs a separately authored explanatory panel.',
    'EL060': 'Energy-band/carrier variants require a separate diagram review.',
    'EL066': 'Battery/supercapacitor/storage architectures are not visually equivalent.',
    'EL072': 'Handle states and state labels need device-specific ownership review.',
    'EL083': 'Neural-signal diagram needs a separate membrane/channel/graph panel.',
    'EL084': 'ECG electrode count and lead configuration need clinical source review.',
    'EL086': 'Pacemaker/neurostimulator cutaway targets are different device families.',
    'EL101': 'Motion trail and an additional double have different count effects.',
    'EL102': 'Body-internal and device-internal receivers need different geometry review.',
    'EL103': 'Before/after exhaustion is a temporal family.',
    'EL105': 'Sensing overlay needs an explicit diagram/legend contract.',
    'EL108': 'Fictional apparatus and subject response need a separately authored relationship.',
    **{f'EL{i:03d}': 'Purpose/metaphor/sound context is retained in research; no standalone visual atom or literal-discharge default.' for i in range(110, 117)},
}

# Replace incidental presentation choices with definition-essential geometry.
OVERRIDES = {
 'EL001': ['separate fine strands rise from one scalp', 'the raised strands spread apart above that same head', 'the lifted strand roots remain attached to that scalp'],
 'EL003': ['small paper fragments cluster around one rod tip', 'several paper fragments contact that same tip', 'the rod and contacted fragments remain separately recognizable'],
 'EL006': ['one concentrated luminous column joins two electrodes', 'both bright attachment regions meet their respective electrodes', 'the luminous column remains continuous between those attachments'],
 'EL015': ['one irregular bright trunk runs from a cloud region to a visible ground endpoint', 'narrow side branches fork from that same trunk', 'the ground endpoint meets the declared landscape object'],
 'EL027': ['a red-dominant luminous cluster appears high above a storm cloud', 'lower tendrils descend from that same high cluster', 'a dark vertical interval separates the lower tendrils from the storm cloud top'],
 'EL036': ['two loads lie consecutively along one circuit branch', 'one conductor path connects the source through both loads and returns to the other source terminal', 'the wire junctions remain continuous through the same series path'],
 'EL045': ['one heating wire follows a repeated bent path', 'separate ceramic-looking supports hold sections of that wire', 'the wire ends belong to the same terminal assembly'],
 'EL051': ['a visible lightning channel owns the light falling on one wet ground patch', 'a broken reflection occupies the geometrically corresponding wet surface region', 'dry ground interrupts the same bounded reflective patch'],
 'EL061': ['a bounded beam vessel encloses the selected beam path', 'a declared slit lies on that internal path', 'a separate glowing target or detector region belongs inside the same vessel'],
 'EL074': ['conductive-looking mesh panels enclose one bounded volume', 'a mesh door continues that enclosure boundary', 'an interior object remains visibly behind those same mesh panels'],
 'EL091': ['a tall winding column supports one top terminal', 'a distinct lower coil assembly belongs to that same column', 'luminous filaments originate at that top terminal and extend into surrounding air'],
 'EL092': ['a hollow glass electrode seats into one handpiece', 'a separately declared glass attachment rests beside that same handpiece', 'the handpiece cable continues to its own controller'],
 'EL093': ['one central handle joins two opposed terminal clusters', 'the prongs of each terminal converge around their own central tip', 'both terminal clusters remain part of the same bounded metal ritual object'],
 'EL095': ['a group of drums belongs to one declared thunder-god depiction', 'the depicted beaters are directed toward those same drums', 'the drum bodies remain separate from the depicted surrounding clouds'],
 'EL104': ['separately identifiable fictional devices occupy one declared area', 'their owned screens or indicators show the declared common response state', 'a separately declared fictional source remains visible in that area'],
}

SPLITS = {
 'EL057': [
  ('meter_voltage_parallel', '전압 모드 계기와 같은 부하 양단의 프로브', 'prop',
   ['two insulated leads connect to the COM and voltage inputs of one meter', 'the remote probe tips contact opposite terminals of the same load in parallel', 'the selected voltage mode and a V display unit belong to that meter'],
   [('probe_pair','connected_to','same_meter'),('probe_tips','contacts_opposite_terminals','same_load')], ['setting','text']),
  ('meter_current_series', '전류 모드 계기와 직렬 삽입된 리드', 'prop',
   ['two insulated leads connect to the COM and current inputs of one meter', 'the meter leads complete a single interrupted circuit branch in series with the load', 'the selected current mode and an A display unit belong to that meter'],
   [('meter_leads','completes','same_circuit_branch'),('meter','in_series_with','same_load')], ['setting','text']),
 ],
 'EL099': [
  ('fantasy_electric_spear', '고체 창축과 창끝에 속한 전격', 'prop',
   ['one solid spear shaft joins its pointed tip', 'a fictional luminous branch originates at that same spear tip', 'the shaft and discharge remain separately recognizable'], [('spear_tip','belongs_to','same_shaft'),('luminous_branch','originates_at','spear_tip')], ['setting','lighting','concept']),
  ('fantasy_electric_blade', '고체 검날의 경계를 따라 붙은 전격', 'prop',
   ['one solid blade joins its own grip', 'a fictional luminous edge follows that same blade boundary', 'the metal blade remains distinct inside the luminous edge'], [('solid_blade','joins','same_grip'),('luminous_edge','follows','blade_boundary')], ['setting','lighting','concept']),
  ('fantasy_electric_whip', '손잡이에서 이어지는 유연한 발광 채찍', 'prop',
   ['one declared grip anchors a fictional flexible luminous path', 'the same path bends continuously away from that grip', 'its free end remains separate from neighboring objects'], [('luminous_path','extends_from','same_grip'),('free_end','belongs_to','luminous_path')], ['setting','lighting','concept']),
 ],
 'EL100': [
  ('fantasy_external_barrier', '몸과 떨어진 외부 전격 방벽', 'surreal_physics_detail',
   ['one fictional luminous barrier occupies a bounded plane', 'a visible spatial gap separates that plane from the protected body', 'the plane boundary remains continuous around its own illuminated region'], [('barrier_plane','separate_from','protected_body'),('luminous_boundary','bounds','barrier_plane')], ['concept','lighting','composition']),
  ('fantasy_surface_armor', '몸 표면을 따라 붙은 전격 갑옷', 'surreal_physics_detail',
   ['a fictional luminous layer follows one declared body surface', 'the same layer follows the visible limb articulation', 'the illuminated layer remains attached to that same body contour'], [('luminous_layer','follows','same_body_surface'),('layer_contour','belongs_to','same_body')], ['concept','lighting','appearance','body_geometry']),
 ],
 'EL107': [
  ('fantasy_blue_white_channel', '같은 채널의 백색 코어와 푸른 가장자리', 'color',
   ['one fictional luminous channel has a near-white core', 'a bounded blue edge belongs to that same channel', 'nearby illuminated surfaces receive light aligned with that channel'], [('blue_edge','belongs_to','same_channel'),('surface_light','aligned_with','same_channel')], ['color','lighting']),
  ('fantasy_red_gold_channel', '같은 채널의 금빛 코어와 붉은 가장자리', 'color',
   ['one fictional luminous channel has a gold-dominant core', 'a bounded red edge belongs to that same channel', 'nearby illuminated surfaces receive light aligned with that channel'], [('red_edge','belongs_to','same_channel'),('surface_light','aligned_with','same_channel')], ['color','lighting']),
 ],
 'EL109': [
  ('fictional_crown_owned_pattern', '관에만 속한 전격 패턴', 'surreal_physics_detail',
   ['a fictional luminous pattern follows one declared crown', 'the pattern remains bounded to the physical rim of that crown', 'the crown remains visibly separate from surrounding objects'], [('pattern','localized_on','same_crown'),('pattern','follows','crown_rim')], ['concept','lighting','appearance']),
  ('fictional_altar_owned_pattern', '제단 표면에만 속한 전격 패턴', 'surreal_physics_detail',
   ['a fictional luminous pattern follows one declared altar surface', 'the pattern remains bounded to the edge of that same altar', 'neighboring objects remain separate from the patterned surface'], [('pattern','localized_on','same_altar'),('pattern','bounded_by','altar_edge')], ['concept','lighting','setting']),
  ('fictional_skin_owned_mark', '선언된 피부 영역에 속한 허구 발광 표식', 'body_marking',
   ['a fictional luminous mark occupies one declared skin region', 'the pattern remains bounded to that same skin surface', 'the surrounding skin contour remains distinct around the mark'], [('luminous_mark','localized_on','same_skin_region'),('mark_boundary','belongs_to','same_skin')], ['concept','lighting','appearance']),
 ],
}

# Reviewed alternate positive component phrases. Broad labels remain insufficient:
# all independent carrier/geometry groups must match for approximate discovery.
COMPONENT_TERMS = {
 'radial_static_hair': [['raised hair strands','static hair','lifted fine strands'],['strands spread apart','radiating hair','radial strands'],['same scalp','attached roots','hair roots']],
 'short_spark_gap': [['spark','spark gap','short luminous channel'],['metal tips','electrodes','metal terminals','conducting spheres','terminals'],['air gap','between the electrodes','between the terminals','between two spheres']],
 'constricted_arc_bridge': [['electric arc','concentrated arc','luminous column'],['electrode attachments','arc endpoints','electrodes'],['continuous column','continuous luminous bridge','between the electrodes']],
 'tip_local_corona': [['corona glow','local corona','faint compact glow'],['conductive tip','electrode tip','pointed metal tip'],['localized glow','immediately around the tip','hugs the tip']],
 'bounded_glow_tube': [['glass discharge tube','glass tube','translucent tube','neon tube'],['end electrodes','electrode caps','metal end caps'],['luminous gas','gas glow','inside the tube','tube interior']],
 'streamer_tip_filaments': [['streamer filaments','luminous filaments'],['branching offshoots','fine branches'],['electrode origin','start at the electrode','free filament ends']],
 'declared_spark_gap_apparatus': [['opposed terminals','facing metal terminals','two electrodes'],['separate terminal supports','insulating supports'],['bounded air gap','gap between the terminals']],
 'plasma_globe_center_radial': [['central electrode','center electrode'],['radial filaments','filaments from the center','internal plasma filaments'],['transparent sphere','glass globe','inner glass boundary']],
 'plasma_globe_touch_concentration': [['fingertip on the glass','finger touching the sphere'],['filaments converge','filaments beneath the finger'],['glass wall','outer glass','internal gas']],
 'jacobs_ladder_arc': [['diverging rods','rods diverge upward'],['arc spanning the rods','arc between the rods'],['arc endpoints','attached to both rods']],
 'cloud_ground_branched_channel': [['cloud to ground','cloud-ground lightning','ground-reaching trunk'],['forked branches','side branches','branched lightning'],['ground endpoint','landscape contact','channel meets the ground']],
 'intracloud_diffuse_illumination': [['cloud interior','inside the cloud','intracloud illumination'],['uneven bright patches','illuminated cloud volume'],['cloud silhouette','cloud boundary','same cloud']],
 'cloud_cloud_channel': [['two cloud masses','separate cloud banks'],['lateral luminous channel','horizontal lightning channel'],['enters both clouds','channel between cloud masses']],
 'cloud_air_free_end': [['branch exits the cloud','cloud-edge branch'],['far end in open sky','channel fades in the sky'],['ground separated','ends above the ground']],
 'mast_st_elmo_glow': [['St Elmo glow','mast-tip corona','local luminous veil'],['pointed mast','mast tip','ship mast'],['glow at the tip','mast visible beneath','localized tip glow']],
 'red_sprite_above_storm': [['red sprite','red luminous cluster','high red cluster'],['lower tendrils','descending tendrils'],['above the storm','separated from the cloud top','dark vertical interval']],
 'blue_jet_cloud_origin': [['blue jet','blue upward jet','tapering blue structure'],['cloud-top junction','starts at the cloud top'],['upward into dark sky','above the same cloud']],
 'gigantic_jet_bridge': [['lower luminous trunk','cloud-top trunk'],['upper branched fan','upper branching structure'],['continuous connection','trunk joins the fan']],
 'closed_circuit_loop': [['source terminals','battery terminals','power source'],['load connection','connected load','load terminals'],['return conductor','complete loop','return path']],
 'open_switch_gap': [['raised switch blade','open switch','separated contact'],['gap interrupts the path','open circuit gap'],['conductors on both sides','attached switch wires']],
 'series_one_path': [['two consecutive loads','loads in series'],['single circuit branch','one current path','one conductor path'],['return to the source','continuous wire junctions']],
 'parallel_shared_nodes': [['separate load branches','parallel branches'],['shared source nodes','same two nodes'],['branch junction','branches divide','complete paths']],
 'copper_winding_ownership': [['wire turns','copper winding','wrapped wire'],['winding terminals','two terminal ends'],['same core','curved metal turns']],
 'glass_neon_sign_structure': [['bent glass tube','glass sign stroke'],['gas inside the tube','luminous region inside glass'],['tube end electrodes','feed wires','same sign stroke']],
 'visible_led_segment_array': [['LED packages','luminous packages','LED segments'],['separate emission centers','individual light centers'],['common board','board connections']],
 'wet_ground_owned_flash_reflection': [['visible lightning channel','in-frame lightning'],['aligned wet reflection','broken reflection','corresponding wet surface'],['wet-dry boundary','dry ground interrupts','bounded reflective patch']],
 'screen_voltage_time_axes': [['oscilloscope screen','screen graticule','continuous waveform'],['voltage scale','vertical voltage axis'],['time scale','horizontal time axis'],['connected probe','scope probe']],
 'tesla_coil_terminal_streamers': [['winding column','Tesla coil column'],['lower coil','primary coil assembly'],['top terminal streamers','filaments from the terminal','terminal-origin discharge']],
}

OWNER_CONFOUNDS = {
 'short_spark_gap': ['printed spark', 'embroidered spark', 'spark tattoo', 'illustrated spark gap'],
 'constricted_arc_bridge': ['printed electric arc', 'embroidered electric arc', 'arc tattoo'],
 'bounded_glow_tube': ['painted neon tube', 'neon graphic on fabric'],
 'cloud_ground_branched_channel': ['printed lightning', 'lightning tattoo', 'embroidered lightning', 'storm diagram'],
 'cloud_cloud_channel': ['printed lightning', 'lightning tattoo', 'embroidered lightning', 'storm diagram'],
 'intracloud_diffuse_illumination': ['printed lightning', 'lightning tattoo', 'embroidered lightning', 'storm diagram'],
 'closed_circuit_loop': ['circuit graphic on fabric', 'printed circuit diagram'],
 'open_switch_gap': ['circuit graphic on fabric', 'printed circuit diagram'],
 'series_one_path': ['circuit graphic on fabric', 'printed circuit diagram'],
 'parallel_shared_nodes': ['circuit graphic on fabric', 'printed circuit diagram'],
}

def effects(card, slug, slot):
    dims = {'hair_style':['appearance'], 'garment_detail':['appearance','material'],
            'body_marking':['appearance'], 'wearable_accessory':['appearance','relationship'],
            'light_shape':['lighting','setting'], 'light_type':['lighting','setting'],
            'lighting':['lighting'], 'weather':['atmosphere','lighting','setting'],
            'prop':['setting'], 'texture':['material'], 'surface_material':['material','setting'],
            'action':['action','setting','lighting'], 'relational_action':['action','relationship','setting'],
            'aftermath_trace':['material','setting'], 'location':['setting'],
            'reflection_logic':['composition','lighting','material'], 'lens_artifact':['camera'],
            'color':['color','lighting'], 'subject':['subject','appearance','setting'],
            'composition':['composition'], 'surreal_physics_detail':['concept','lighting']}.get(slot)
    if not dims: raise ValueError(('unreviewed slot', slug, slot))
    dims = list(dims)
    if slug in {'plasma_globe_center_radial','jacobs_ladder_arc','joule_heating_element',
                'glass_neon_sign_structure','screen_voltage_time_axes','tesla_coil_terminal_streamers'}:
        dims += ['lighting']
    if slug in {'red_sprite_above_storm','blue_jet_cloud_origin','mast_st_elmo_glow','auroral_curtain_and_rays'}:
        dims += ['color']
    if slug == 'screen_voltage_time_axes': dims += ['text']
    if slug == 'battery_terminal_pair': dims += ['text']
    if slug in {'intracloud_diffuse_illumination','distant_heat_flash'}:dims += ['atmosphere']
    if slug == 'arc_flash_owned_origin':dims += ['setting']
    if slug == 'plasma_globe_touch_concentration':dims += ['lighting','pose']
    if slug == 'welding_arc_and_spatter':dims += ['material','atmosphere']
    if slug in {'electrolysis_electrodes_bubbles','low_pressure_electron_beam_detector'}:dims += ['material']
    if slug == 'low_pressure_electron_beam_detector':dims += ['lighting']
    if slug == 'esd_bench_wrist_connection':dims += ['setting']
    if slug == 'aed_pad_same_patient':dims += ['appearance','relationship']
    if slug == 'tms_coil_head_relation':dims += ['relationship']
    if slug == 'fantasy_hand_owned_discharge': dims += ['relationship','appearance']
    if slug == 'fantasy_chain_targets': dims += ['lighting','concept','count']
    if slug == 'fictional_emp_device_response': dims += ['setting','text','count']
    if slug == 'plasma_being_elemental': dims += ['lighting','body_geometry','concept']
    dims=list(dict.fromkeys(dims))
    return dims

def property_scopes(slug, dimensions):
    # Consumer paths are literal and carrier-independent, not a semantic owner
    # resolver. Keep an unresolved owner conservative, while naming the actual
    # observable property domain so a light source does not claim to alter a face.
    paths={
      'setting':['apparatus','scene.object_inventory','object_inventory','spatial_structure','topology'],
      'lighting':['lighting','emission','source','light_source'],
      'atmosphere':['atmosphere','weather','cloud'],
      'material':['material','surface','damage','coating'],
      'appearance':['body.surface','skin','wardrobe'],
      'relationship':['relationship','contact','connection','body.hand_contact'],
      'action':['action','contact','body.hand_contact'],
      'pose':['pose','hand.pose','body.pose'],
      'body_geometry':['body','body_geometry'],
      'composition':['composition','spatial_relation','reflection','occlusion'],
      'camera':['camera','capture','artifact'],
      'color':['color','palette','emission.color','lighting.color'],
      'text':['text','display','label'],
      'concept':['concept','fictional_physics'],
      'count':['count','subject_count','target_count'],
      'subject':['subject','species','identity'],
    }
    if slug=='radial_static_hair':paths['appearance']=['hair','hairstyle']
    if slug=='static_cling_cloth':
        paths['appearance']=['wardrobe','garment','fabric.contact_state']
        paths['material']=['wardrobe','garment','fabric.contact_state']
    if slug in {'skin_lichtenberg_fern_pattern','fictional_skin_owned_mark'}:
        paths['appearance']=['skin','body.marking','face','facial_appearance']
    if slug=='esd_bench_wrist_connection':paths['appearance']=['wrist.accessory','wearable_accessory']
    if slug=='aed_pad_same_patient':paths['appearance']=['chest.surface','skin.electrode_contact']
    return [{'dimension':d,'target':'*','property':p} for d in dimensions for p in paths[d]]

def main():
    cards=json.loads((RESEARCH/'research.json').read_text())['cards']
    seeds={r['seed_id']:r for r in json.loads((RESEARCH/'SEED-KEYWORDS.json').read_text())['seeds']}
    candidate={'schema_version':'photo-prompt-research-extension/v1','slots':{}}
    registry={'schema_version':'photo-visual-obligation-registry-extension/v1',
              'relation_contract_version':'photo-visual-relation/v1','profiles':[]}
    ledger=[]
    for card in cards:
        cid=card['card_id']
        if cid in DEFER:
            ledger.append({'research_card_id':cid,'disposition':'deferred','reason':DEFER[cid],'runtime_candidate_ids':[],'runtime_profile_ids':[]});continue
        variants=SPLITS.get(cid)
        if variants is None:
            if card['atomization_status']=='family_split_required': raise ValueError(('unsplit family',cid))
            units=OVERRIDES.get(cid,card['concept_units'])
            variants=[(card['slug'],card['label_ko'],card['candidate_plan']['suggested_slot'],units,
                       [(r['subject'],r['type'],r['object']) for r in card['relations']],
                       effects(card,card['slug'],card['candidate_plan']['suggested_slot']))]
        ids=[];pids=[]
        for slug,ko,slot,units,relations,dims in variants:
            eid='electric_'+slug
            pid='auroral_arc_curtain_atmosphere' if cid=='EL031' else 'electric_'+slug+'_relation'
            ids.append(eid);pids.append(pid)
            props=property_scopes(slug,dims)
            aliases=[]
            if cid not in SPLITS:
                for sid in card['source_seed_ids']:
                    for term in [seeds[sid]['term_ko'],seeds[sid]['term_en']]:
                        if term and term not in aliases: aliases.append(term)
            english='; '.join(units)
            entry={'id':eid,'ko':ko,'en':english,'weight':0.42,'tags':['electricity'],
                   'aliases':aliases,'keywords':list(units),'paraphrases':[english],
                   'embedding_text':english,'concept_terms':[ko,*units],
                   'concept_units':list(units),'relations':[{'id':f'relation_{i}', 'subject':a,'type':r,'object':b} for i,(a,r,b) in enumerate(relations,1)],
                   'affected_dimensions':dims,'affected_properties':props,'core_assertion_discovery':True,
                   'contextual_usage':{'contexts':[{'id':'electrical_observable_scope','definition':ko,
                       'observable_interpretation':english,'claim_limits':card['claim_limits'],
                       'activation_authority':'interpretation_only_not_required'}]}}
            candidate['slots'].setdefault(slot,[]).append(entry)
            if cid=='EL031':
                # Existing full horizon/arc/curtain/ray profile remains the owner.
                # A bounded sibling candidate adds no replacement or weaker gates.
                continue
            components=[];obligations=[]
            for i,unit in enumerate(units,1):
                comp=f'component_{i}'
                alternatives=COMPONENT_TERMS.get(slug,[[] for _ in units])[i-1]
                components.append({'id':comp,'match_terms':list(dict.fromkeys([unit,*alternatives]))})
                obligations.append({'component_ids':[comp],
                  'evidence':[{'field':f'component_{i}_phrase','requirement':{'min_content_words':3,'must_mention_any':[unit]}}],
                  'instruction':f'Keep this selected observable component on its declared owner, with the stated physical connection: {unit}.',
                  'render_gates':[{'id':f'vo_{pid}_{i}','review_scale':'native',
                    'description':f'At original image resolution inspect the complete selected component and its actual owner or connection: {unit}. A hidden, partial, or wrongly owned required component does not pass.'}]})
            registry['profiles'].append({'id':pid,'category':'electrical_owned_observable_relation',
              'activation':{'exact_terms':[english], 'requires_adult_character':False,
                **({'exclude_if_any_terms':OWNER_CONFOUNDS[slug]} if slug in OWNER_CONFOUNDS else {}),
                'semantic_discovery_requires_component_evidence':True,
                'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_owned_proposition','any_terms':[english]}]}},
              'semantics':{'definition':english,'paraphrase_examples':[ko],
                'visual_components':list(units),'contrast_examples':card['confusion_boundaries'],
                'claim_limits':card['claim_limits']+['Approximate similarity is an optional proposal. All opt-in duties apply only after deliberate adoption; a broad electricity, lightning, color or metaphor label adds no subtype duty.']},
              'authored_components':{'contract_version':'photo-authored-visual-components/v2','components':components,
                'discovery':{'minimum_component_groups':len(components),'required_group_ids':[c['id'] for c in components]},'obligations':obligations},
              'concept_candidate':{'concept_terms':[ko,*units], 'core_assertion_discovery':True,
                'affected_dimensions':dims,'affected_properties':props},
              'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
                'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
              'reject_substitutes':card['confusion_boundaries']})
        ledger.append({'research_card_id':cid,'slug':card['slug'],
                       'disposition':'split_and_adopted' if cid in SPLITS else 'bounded_sibling_adopted',
                       'runtime_candidate_ids':ids,'runtime_profile_ids':pids,
                       'sources':card['sources'],'existing_ids_preserved':card['candidate_plan']['reuse_decision']['existing_ids'],
                       'effects_review':'Current consumer uses literal carrier-independent path overlap. Unresolved owners use wildcard target, with reviewed positive property domains and explicit indirect dimensions. This is no object-instance resolver or semantic-truth proof; compare actual final owners and preserve requester evidence separately.',
                       'fiction_review': 'Creative depiction proposed by the agent; cited science does not establish fictional powers.' if card['observation_mode']=='fantasy' else None})
    OUT.mkdir(exist_ok=True)
    save(OUT/CANDIDATE_FILE,candidate);save(OUT/PROFILE_FILE,registry)
    save(OUT/'ADOPTION-LEDGER.json',{'contract_version':'electrical-source-adoption/v1','research_cards':len(cards),
         'adopted_cards':sum(r['disposition']!='deferred' for r in ledger),'candidates':sum(len(v) for v in candidate['slots'].values()),
         'profiles':len(registry['profiles']),'records':ledger,
         'evidence_boundary':'Source/compiler/effect review is separate from candidate-pack exposure, deliberate adoption, literal prompt evidence, native pixels and user acceptance.'})
    print(json.dumps({'candidate_count':sum(len(v) for v in candidate['slots'].values()),'profile_count':len(registry['profiles']),
                      'adopted_cards':sum(r['disposition']!='deferred' for r in ledger),'deferred_cards':len(DEFER),'slots':list(candidate['slots'])}))

if __name__=='__main__': main()
