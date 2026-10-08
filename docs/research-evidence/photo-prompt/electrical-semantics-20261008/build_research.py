"""Build research artifacts only; never imports or publishes the photo runtime."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def fnv_utf16(text):
    raw = text.encode('utf-16-le')
    h = 2166136261
    for i in range(0, len(raw), 2):
        h = ((h ^ (raw[i] | raw[i + 1] << 8)) * 16777619) & 0xffffffff
    return f'{h:08x}'


def build_seeds():
    ref = json.loads((HERE / 'REFERENCE-EXCERPT.json').read_text())
    body = next(item['text'] for turn in ref['turns'] for item in turn['items'] if item['type'] == 'agentMessage')
    seeds = []
    section = 0
    title = ''
    for line in body.splitlines():
        heading = re.match(r'^## (\d+)\. (.+)$', line)
        if heading:
            section, title = int(heading[1]), heading[2]
        term = re.match(r'^\|\s*\*\*([^*]+)\*\*\s*\|', line)
        if term and section <= 15:
            seeds.append({'section': section, 'section_title': title, 'label': term[1], 'recovery': 'read_thread_excerpt'})
    for line in (HERE / 'reference-supplement.tsv').read_text().splitlines():
        number, title, terms = line.split('\t')
        for term in terms.split(';'):
            seeds.append({'section': int(number), 'section_title': title, 'label': term, 'recovery': 'visible_browser_dom_supplement'})
    expected = [18,20,16,15,22,18,16,17,16,13,17,18,16,16,14,14,17,15,18,14,12,10,13,18,30,22]
    counts = Counter(seed['section'] for seed in seeds)
    assert [counts[i] for i in range(1,27)] == expected, counts
    assert len(seeds) == 435
    actual_hash = fnv_utf16('\n'.join(seed['label'] for seed in seeds))
    assert actual_hash == '60b23815', f'Ordered DOM labels differ: {actual_hash}'
    for i, seed in enumerate(seeds, 1):
        seed.update(seed_id=f'K{i:04d}', term_ko=seed['label'].split(' — ')[0],
                    term_en=seed['label'].split(' — ', 1)[1] if ' — ' in seed['label'] else None)
    save('SEED-KEYWORDS.json', {
        'contract_version': 'electrical-seed-research/v1', 'conversation_id': ref['conversation_id'],
        'numbered_sections': 26, 'keyword_rows': 435, 'combination_examples': 5,
        'integrity': {'method': 'FNV1a32 UTF16 code units over ordered labels joined by LF', 'expected_browser_digest': '60b23815', 'actual_digest': actual_hash, 'match': True},
        'source_limits': 'The cached response remains truncated. All numbered keyword labels were recovered from visible DOM and checked; the full response prose and all citations were not exported verbatim.',
        'reference_is_untrusted': True, 'seeds': seeds,
        'composition_examples_ko': ['현실적인 산업 장면','자연의 압도감','복고 SF 연구실','전기 능력자','기묘하고 정적인 분위기'],
    })
    return seeds


def build_sources():
    rows = list(csv.DictReader((HERE / 'sources.tsv').read_text().splitlines(), delimiter='\t'))
    assert len(rows) == 42
    assert len({r['id'] for r in rows}) == len(rows)
    for row in rows:
        assert row['url'].startswith('https://') and row['support_scope'] and row['limits']
        row['accessed_local_date'] = '2026-10-08'
        row['verification_boundary'] = 'Read status describes available source text, not native image review or verification of every proposed visual component.'
    save('SOURCES.json', {'scope': 'Primary institutions, textbooks, research abstracts and a first-party cultural vocabulary source. Read-depth limitations are explicit.', 'sources': rows})
    return {row['id']: row for row in rows}


FAMILIES = {
    'fantasy_spear_blade_whip', 'fantasy_barrier_armor_shell', 'fantasy_dash_double_traces',
    'fantasy_absorption_core', 'fantasy_overcharge_exhaustion', 'fantasy_lightning_color_variants',
    'fictional_crown_altar_mark', 'implanted_stimulator_model', 'conducted_energy_device_context',
    'charge_carrier_band_model', 'field_line_dipole_model', 'ecg_leads_trace_relation',
    'storage_rack_connected_modules', 'breaker_owned_handle_state', 'meter_probes_same_nodes',
}

REUSE = {
    'radial_static_hair': ('enrich_or_narrow_sibling', ['static_hair_charge'], '기존 넓은 항목을 보존하며 같은 모발 carrier의 관측 형태만 보강.'),
    'static_cling_cloth': ('enrich_or_narrow_sibling', ['static_cling_fabric'], '젖음·비침·신체 접촉 범위가 바뀌면 sibling.'),
    'glass_neon_sign_structure': ('narrow_sibling', ['neon_sign', 'neon_sign_light'], '기존 rain-soaked subject와 광원 spill을 gas-tube 정의로 덮어쓰지 않음.'),
    'wet_ground_owned_flash_reflection': ('conditional_reuse', ['wet_surface_light_reflection_owner_relation'], '기존 5개 소유·정렬·경계·차폐 조건을 모두 유지할 때만 재사용.'),
    'auroral_curtain_and_rays': ('conditional_reuse', ['auroral_arc_curtain_atmosphere', 'aurora_borealis_field'], '커튼 subtype과 지평선 근거가 맞을 때 재사용;설원은 선택된 기존 location의 의미.'),
    'cumulonimbus_owned_structure': ('conditional_reuse_or_sibling', ['cumulonimbus_tower_anvil_precipitation_outflow'], '기존 profile의 강수·outflow duty를 축약하지 않음;이번 카드와 같은 complete subtype인지 대조.'),
    'solar_corona_occulted_view': ('distinct_sibling', ['cme_coronagraph_snapshot'], '단순 코로나에 CME front를 강제하지 않음.'),
    'skin_lichtenberg_fern_pattern': ('distinct_sibling', ['appearance_h058', 'appearance_rel_h058'], '기존 이마의 짧은 각진 흉터는 피부의 분지 홍반과 동치가 아님.'),
    'tesla_coil_terminal_streamers': ('reuse_system_keep_new_atom_separate', ['punk_teslapunk_mechanism_prop', 'punk_teslapunk_system_diagnostic_prop'], '세계관·설비 관계는 유지하고 구체 장치 원자를 별도 작성.'),
    'scorched_contact_patch': ('not_equivalent_to_existing_cascade', ['technical_overload_progressive_failure'], '탄 흔적 하나는 정격 초과·전파·차단의 complete cascade가 아님.'),
    'fantasy_hand_owned_discharge': ('distinct_carrier', ['y2kr_circuit_graphic', 'ca_zigzag_tail'], '의복 회로 프린트·각진 꼬리와 공중 방전은 carrier가 다름.'),
}

EFFECTS = {
    'hair_style': [('appearance','selected_subject','hair.geometry')],
    'garment_detail': [('appearance','selected_garment','fabric.contact_state')],
    'light_shape': [('lighting','selected_source','emission.geometry')],
    'light_type': [('lighting','selected_source','emission.mechanism_and_shape')],
    'weather': [('atmosphere','selected_atmospheric_event','spatial_structure')],
    'lighting': [('lighting','selected_source','illumination.geometry')],
    'color': [('color','selected_source','emission.color')],
    'composition': [('composition','selected_view','spatial_or_diagram_structure')],
    'lens_artifact': [('camera','selected_capture','optical_recording_effect')],
    'texture': [('material','selected_surface','visible_pattern')],
    'surface_material': [('material','selected_workpiece','surface_finish')],
    'subject': [('subject','selected_subject','visible_structure')],
    'location': [('setting','selected_environment','apparatus_layout')],
    'body_marking': [('appearance','selected_subject','skin.visible_pattern')],
    'wearable_accessory': [('appearance','selected_subject','accessory.connection')],
    'relational_action': [('action','selected_event','visible_connection')],
    'surreal_physics_detail': [('concept','selected_fictional_event','mechanism'),('lighting','selected_source','emission.geometry')],
    'motion': [('action','selected_actor','motion_representation'),('camera','selected_capture','recording_effect')],
    'narrative_phase': [('timing','selected_event','represented_phase')],
    'prop': [('subject','selected_apparatus','structure'),('setting','selected_apparatus','connections')],
    'aftermath_trace': [('material','selected_damaged_object','surface_state')],
    'reflection_logic': [('composition','selected_source_surface_pair','reflection.geometry'),('lighting','selected_source','illumination.geometry')],
}

GLOBAL_LIMITS = [
    'A visual resemblance is not proof of hidden voltage, current, polarity, temperature, material identity, safety, medical diagnosis, death, consent, purpose, or physical causation.',
    'Still images cannot directly establish sound, onset direction, duration, repeated flicker, charge/discharge direction, measured speed, successful treatment, or before-after history.',
    'Approximate retrieval is advisory. It does not create requester duties, force a subtype, or override definitions, negation, locked carriers or properties.',
    'A source may support a mechanism while the selected geometry, staging and capture are agent-proposed. Component fields are research proposals until adopted and validated.',
]


def build_cards(seeds, sources):
    raw = list(csv.DictReader((HERE / 'cards.tsv').read_text().splitlines(), delimiter='|'))
    assert len({row['slug'] for row in raw}) == len(raw)
    base = json.loads((ASSETS / 'photo_prompt_tags.json').read_text())
    slots = set(base['slots'])
    known_ids = set()
    repo = json.loads((HERE / 'REPO-COVERAGE.json').read_text())
    known_ids.update(hit['id'] for hit in repo['hits'])
    manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
    for name in ['photo_prompt_tags.json','photo_prompt_visual_obligations.json',*[s['file'] for s in manifest['sources']]]:
        data=json.loads((ASSETS/name).read_text())
        known_ids.update(row['id'] for rows in data.get('slots',{}).values() for row in rows)
        known_ids.update(row['id'] for row in data.get('profiles',[]))
    cards = []
    blueprints = []
    for i, row in enumerate(raw, 1):
        assert None not in row and all(v is not None for v in row.values()), row
        assert row['slot'] in slots, row['slot']
        source_ids = row['sources'].split(',')
        assert set(source_ids) <= set(sources)
        components = row['components_en'].split('^')
        assert len(components) >= 3 and all(len(c.split()) >= 4 for c in components)
        relations = []
        for j, relation in enumerate(row['relations'].split(';'), 1):
            kind, subject, obj = relation.split(',')
            relations.append({'id':f'relation_{j}','type':kind,'subject':subject,'object':obj})
        roles = sorted({r[k] for r in relations for k in ['subject','object']})
        cid = f'EL{i:03d}'
        seed_terms = row['seed_terms_ko'].split(',')
        sections = list(map(int, row['sections'].split(',')))
        mapped = [s['seed_id'] for s in seeds if s['section'] in sections and s['term_ko'] in seed_terms]
        reused = REUSE.get(row['slug'])
        if reused:
            assert set(reused[1]) <= known_ids, f'Unverified reuse ID: {reused}'
        candidate_allowed = row['mode'] != 'context' and row['slug'] not in FAMILIES
        effects = [{'dimension':d,'target':t,'property':p} for d,t,p in EFFECTS.get(row['slot'], [])]
        card = {
            'card_id':cid, 'slug':row['slug'], 'label_ko':row['label_ko'],
            'source_sections':sections, 'source_seed_ids':mapped, 'additional_term_if_unmapped':not bool(mapped),
            'observation_mode':row['mode'], 'priority':row['priority'],
            'selected_observable_realization_en':'; '.join(components),
            'concept_units':components, 'roles':[{'role_id':role,'binding':'Explicitly bind to the selected request object; these are local research graph nodes, not resolved runtime targets.'} for role in roles],
            'relations':relations, 'confusion_boundaries':[row['confounder_ko']],
            'claim_limits':[row['claim_limit_ko'],*GLOBAL_LIMITS[:2]],
            'sources':[{'source_id':sid,'supported_scope':sources[sid]['support_scope'],'read_status':sources[sid]['read_status']} for sid in source_ids],
            'evidence_grade':'creative_design_not_empirical_claim' if row['mode']=='fantasy' else 'context_only' if row['mode']=='context' else 'source_supported_core_with_agent_proposed_visual_realization',
            'atomization_status':'family_split_required' if row['slug'] in FAMILIES else 'context_not_standalone_visual_atom' if row['mode']=='context' else 'bounded_realization_proposal',
            'candidate_plan':{
                'suggested_slot':row['slot'],'standalone_draft_allowed':candidate_allowed,
                'proposed_affected_dimensions':sorted({e['dimension'] for e in effects}),
                'proposed_affected_properties':effects,
                'effect_mapping_status':'Proposal only. Verify actual consumer binding and indirect effects before adoption; no empty effect list means no change.',
                'reuse_decision': {'kind':reused[0],'existing_ids':reused[1],'reason':reused[2]} if reused else {'kind':'new_atom_or_context_after_review','existing_ids':[],'reason':'No equivalence claim from keyword absence; check the latest complete corpus before authoring.'},
            },
            'promotion_state':'research_only_not_runtime_validated',
            'remaining_research': 'Resolve all limits, source-specific apparatus variants and family splits before promotion. P2 is explicitly not source-qualified implementation.' if row['priority']=='P2' or not candidate_allowed else 'Review source-to-component support and exact owner/effect binding before implementation.',
            'native_review_plan':{
                'conditional_on':'Only requester-required meaning or complete legitimately adopted opt-in duties, not similarity hits or all research components.',
                'inspect':[] if row['mode']=='context' else [*components,*[f"{r['subject']} {r['type']} {r['object']}" for r in relations]],
                'unobservable_policy':'UNOBSERVABLE_NOT_PASS for a required visual duty; do not score hidden/temporal claims as image duties.',
                'whole_scene_policy':'Every selected hard duty and requester lock must pass; partial realization is failure. Creative preference remains separate.',
            },
        }
        cards.append(card)
        if candidate_allowed:
            positive = '; '.join(components)
            assert 'http' not in positive and 'S0' not in positive and not re.search(r'\b(not|reject|without)\b', positive, re.I)
            blueprints.append({
                'draft_id':'electrical_'+row['slug'], 'research_card_id':cid,
                'prototype_schema':'electrical-candidate-blueprint/v1 (research, not loadable runtime extension)',
                'suggested_slot':row['slot'],'ko_proposal':row['label_ko'],'en_proposal':positive,
                'concept_terms_proposal':components,'concept_units_proposal':components,'relations_proposal':relations,
                'affected_dimensions_proposal':card['candidate_plan']['proposed_affected_dimensions'],
                'affected_properties_proposal':effects,'effects_verified':False,
                'positive_embedding_text_proposal':positive,
                'default_adoption':'optional_postcore','exact_hard_activation_proposal':None,
                'core_assertion_discovery_proposal':False,
                'runtime_ready':False,'weight_proposal':None,
                'review_required':'No default color, victim, erotic action, rain, costume, unsafe working procedure, or named device purpose is inferred from a broad electrical token.',
            })
    save('research.json', {'contract_version':'electrical-visual-semantics-research/v1',
         'date':'2026-10-08','timezone':'Asia/Seoul','request_scope':'Detailed research and implementation planning only',
         'global_limits':GLOBAL_LIMITS,'cards':cards})
    save('CANDIDATE-BLUEPRINTS.json', {'contract_version':'electrical-candidate-blueprint-set/v1','runtime_integrated':False,
         'warning':'These proposed rows are not validated candidate or profile extensions. Research folders are not runtime/pre-core sources.',
         'blueprints':blueprints,'excluded_family_or_context_cards':[c['card_id'] for c in cards if not c['candidate_plan']['standalone_draft_allowed']]})
    return cards,blueprints


CONTEXT_ROUTES = {
    1:('hidden_physical_quantity','전하·전위·전압·전류·전력·에너지의 뜻을 분리. 관측 결과/계측/모형을 요청에 맞춰 선택하고 양을 색으로 표현하지 않음.'),
    2:('microscopic_model','전자·양전자·정공·오비탈·스핀은 모형/검출 문맥. 전자 자체의 발광 구슬과 행성 궤도를 실제 사진의 필수 형태로 만들지 않음.'),
    3:('material_property_context','도체·절연체·반도체·유전체·초전도체는 기능/재료 문맥. 광택·투명도·자기부상만으로 물성이나 임계온도를 증명하지 않음.'),
    4:('unit_and_label_context','V/A/C/Ω/S/W/J/Wh/Ah/F/H/Hz/T/Wb/eV는 단위. 계기 라벨·축·문맥 외 독립 발광 atom을 만들지 않음. Tesla 단위와 코일 장치 분리.'),
    5:('topology_or_time_signal','연결 방식과 시간파형 분리. 전류·신호의 직접 가시화가 아닌 회로 노드/계기/명시적 설명 도식을 사용.'),
    6:('field_law_or_mechanical_effect','법칙·자기장·유도·와전류는 설명/측정 문맥. 물리적 코일과 모형 장선의 범위를 구분.'),
    7:('discharge_subtype_or_hidden_state','전하 이동·기체 상태·발광 형태를 분리. 잔류전하·절연내력·온도는 직접 시각 atom이 아님.'),
    8:('atmospheric_topology_or_time','cloud/ground/air의 종점과 관측자 위치를 분리. 극성·flash/stroke 수·발생 방향·지속 시간은 추가 기록.'),
    9:('storm_process_or_trace','기류·입자·전하분리는 설명 모형;구름·유리관·돛대 발광은 visible subtype. 천둥은 오디오 영역.'),
    10:('upper_atmosphere_or_space_model','TLE·오로라·태양 코로나·전리층·자기권·GIC를 다른 owner/공간/관측 모드로 구분. TGF는 검출 기록.'),
    11:('device_variant_context','각 부품의 casing·lead·package 판본을 제조사/박물관 1차 자료로 추가 검증. 기능·bandgap·증폭·접합은 외형으로 입증하지 않음.'),
    12:('energy_conversion_and_direction','전기화학 저장·전기장 저장·발전·변환 분리. 케이블·게이지·랙은 관측표현이며 흐름·량의 직접 증거가 아님.'),
    13:('infrastructure_connections','계통 접속과 설비 외형을 구분. 전력 수요·peak·brownout·정전 원인은 값/시간/운영 기록 필요.'),
    14:('emission_heat_and_motion','가열 필라멘트·기체 방전·반도체 발광과 기계 운동을 분리. 켜짐·회전·소리는 요청에서 필요한 상태만 채택.'),
    15:('measurement_information_context','안테나·송수신기·계기는 판본별 장치. 실제 전파·디지털 상태·신호값·측정 정확도는 계기/설명 기록.'),
    16:('electrochemical_context','산화·환원과 부호 분리. electrode/bath/bubbles/coating의 owner를 명시하며 기포 색만으로 성분을 추정하지 않음.'),
    17:('biological_function_or_model','물고기 형태와 발전기관/전기 감각 기능 구분. 신경 전위·세포·이온은 과학 모형/계측으로 표현.'),
    18:('clinical_device_and_purpose','ECG/EMG/전도검사·자극/기록 장치 구분. 치료 목적·진단·동의·성공은 시각적 형태의 필수 gate가 아님.'),
    19:('fault_cause_and_visible_damage','고장 원인·전기 현상·표면 흔적·인체 손상을 별개로 보관. 사고·사망·전류경로를 흔적이나 pose만으로 판정하지 않음.'),
    20:('protective_function_context','보호 장치의 외형·연결은 조사하되 실제 성능·법규준수·기기 안전을 외형으로 증명하지 않음. maker 판본 추가 조사.'),
    21:('historical_apparatus_variant','유물 판본의 disc·layer·terminal·tube 연결을 조사. 역사 광고·갈바니즘·fictional reanimation은 실제 효능과 분리.'),
    22:('purpose_sensitive_context','무기·강압·성인 문화·의료 용어를 모두 ledger에 유지. 장치 외형으로 용도·동의·상해·효능을 추정하지 않음;제작·사용 절차가 아닌 의미 연구.'),
    23:('cultural_iconography_or_authored_fiction','실제 유물/도상 판본과 새 창작 명칭 분리. 문화 이름 하나로 북·망치·손잡이·복장·번개를 모두 강제하지 않음.'),
    24:('figurative_language','literal physical sense와 figurative emotional sense 구분. 사용자의 재정의·전체 문장·관계가 우선하며 방전 효과는 비유에서 자동 생성하지 않음.'),
    25:('capture_surface_sound_owner','발생체·수광면·표면 손상·광학 번짐·음향·시간 변화를 다른 carrier/property로 분리. 형용사 하나를 글로벌 style gate로 만들지 않음.'),
    26:('authored_fantasy_mechanism','창작 설정임을 유지. 형태·기점·대상·경로·피복·반응을 요청으로 정의하고 과학적 기전/의료 효능으로 승격하지 않음.'),
}


def build_coverage(seeds,cards):
    ledger=[]
    for seed in seeds:
        linked=[c for c in cards if seed['seed_id'] in c['source_seed_ids']]
        route,reason=CONTEXT_ROUTES[seed['section']]
        ledger.append({**seed,'research_card_ids':[c['card_id'] for c in linked],
            'disposition':'detailed_card_mapping' if linked else 'context_or_variant_followup',
            'context_route':route,'context_reason':reason,
            'qualification':'No claim that every seed has independent primary-source verification or is a runtime-ready visual atom.',
            'remaining':'Validate proposed cards and source-to-component support.' if linked else 'Interpretation context is recorded; obtain term/device-specific sources and bounded realization before creating a new standalone candidate.'})
    save('SEED-COVERAGE.json',{'all_seed_rows_accounted_for':len(ledger)==435,'term_level_source_verification_claim':False,'rows':ledger})
    with (HERE/'SEED-COVERAGE.tsv').open('w') as f:
        writer=csv.writer(f,delimiter='\t')
        writer.writerow(['seed_id','section','original_label','disposition','card_ids','context_route'])
        for row in ledger: writer.writerow([row['seed_id'],row['section'],row['label'],row['disposition'],','.join(row['research_card_ids']),row['context_route']])
    return ledger


def build_catalog(cards,sources):
    lines=['# 전기 시각 의미 연구 카드','', '각 카드는 선택 가능한 관측 표현의 초안이다. 실제 의미가 요구하지 않는 세부를 hard duty로 만들지 않는다. `P2`와 family 카드는 추가 리서치·분해 후 채택한다.','']
    for c in cards:
        lines += [f"## {c['card_id']} — {c['label_ko']}",'',f"- 모드/우선순위: `{c['observation_mode']}` / `{c['priority']}`; 원자화: `{c['atomization_status']}`",f"- 시각 표현: {c['selected_observable_realization_en']}",f"- 관계: {'; '.join(r['subject']+' → '+r['type']+' → '+r['object'] for r in c['relations'])}",f"- 혼동 경계: {c['confusion_boundaries'][0]}",f"- 판정 한계: {c['claim_limits'][0]}",f"- 반영 경로: `{c['candidate_plan']['suggested_slot']}`; `{c['candidate_plan']['reuse_decision']['kind']}`",'- 출처: '+', '.join(f"[{sid}: {sources[sid]['title']}]({sources[sid]['url']})" for sid in [s['source_id'] for s in c['sources']]),'']
    (HERE/'CARD-CATALOG.md').write_text('\n'.join(lines)+'\n')


def build_regression(cards):
    rows=list(csv.DictReader((HERE/'regression-cases.tsv').read_text().splitlines(),delimiter='|'))
    assert len(rows)==36 and len({r['id'] for r in rows})==36
    by_slug={c['slug']:c['card_id'] for c in cards}
    cases=[]
    for row in rows:
        assert None not in row and all(v is not None for v in row.values()),row
        slugs=row.pop('card_slugs').split(',')
        assert set(slugs)<=set(by_slug)
        row['research_card_ids']=[by_slug[s] for s in slugs]
        row['stages']=row['stages'].split(',')
        row['execution_status']='planned_not_run'
        row['authorship']='Research-informed public test design; not a blind independent holdout.'
        cases.append(row)
    save('REGRESSION-PLAN.json',{'contract_version':'electrical-regression-plan/v1',
        'cases':cases,'executed_case_count':0,'native_generation_count':0,
        'promotion_rule':'Actual changed-source contract/retrieval tests are required during integration. Native image evaluation needs separately requested image work and exact frozen meaning; no weak partial passes.',
        'hidden_claims_not_pixel_gates':['voltage','current','polarity','temperature','frequency','duration','onset_direction','sound','consent','medical_outcome','death','purpose','safety']})


def main():
    seeds=build_seeds();sources=build_sources();cards,blueprints=build_cards(seeds,sources)
    ledger=build_coverage(seeds,cards);build_catalog(cards,sources);build_regression(cards)
    stats={'seed_rows':len(seeds),'numbered_sections':26,'ordered_seed_dom_digest_match':True,'source_records':len(sources),
           'research_cards':len(cards),'blueprints':len(blueprints), 'modes':dict(Counter(c['observation_mode'] for c in cards)),
           'priorities':dict(Counter(c['priority'] for c in cards)),
           'family_split_cards':sum(c['atomization_status']=='family_split_required' for c in cards),
           'context_cards':sum(c['observation_mode']=='context' for c in cards),
           'mapped_seed_rows':sum(bool(r['research_card_ids']) for r in ledger),
           'context_or_variant_seed_rows':sum(not r['research_card_ids'] for r in ledger)}
    save('PACKAGE-STATS.json',stats)
    print(json.dumps(stats,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
