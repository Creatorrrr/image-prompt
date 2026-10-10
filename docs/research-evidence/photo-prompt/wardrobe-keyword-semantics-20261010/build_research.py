"""Build research artifacts only. No runtime source, index or API is changed."""
from pathlib import Path
import collections
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

FAMILIES = {
 '01': ('상의 유형', '의상 유형 / 목선 / 소매 / 기장 / 핏 / 내외층', 'clothing_structure,fashion_fit'),
 '02': ('겉옷과 레이어 상태', '외층 / 내층 / 열린 경계 / 착용·놓임 / 고정점', 'clothing_structure,fashion_fit,everyday_scene'),
 '03': ('완성 의상과 영감 출처', '유형 / 외곽 / 구조 / 문화·시대·판타지 한정 / 선택 장식', 'costume_cosplay,historical_womenswear,traditional_clothing_detail'),
 '04': ('하의 구조', '바지·치마 / 허리 / 기장 / 플리츠·티어드·러플 / 겹침', 'clothing_structure,fashion_fit'),
 '05': ('수영복과 이너', '몸판 연속성 / 분리 상하의 / 지지 경로 / 가림성 / 추정 상태', 'swimwear,clothing_structure'),
 '06': ('목선과 등판', '경계 형상 / 높이 / 폭 / 끈 지지 / 키홀 / 앞뒤 소유자', 'clothing_structure'),
 '07': ('소매와 커프스', '길이 / 부피 위치 / 끝단 / 부착·분리 / 걷은 상태', 'clothing_structure,fashion_fit'),
 '08': ('핏과 실루엣', '국소 접촉 / 여유 / 강성 인상 / 길이 / 외곽 / 부피 위치', 'fashion_fit,clothing_structure'),
 '09': ('재단과 연결', '패널 / 이음선 / 고정점 / 겹침 방향 / 여밈 / 안감', 'clothing_structure,visual_grammar,traditional_clothing_detail'),
 '10': ('소재와 표면', '명시 섬유 / 조직 / 마감 / 비침 / 반사 / 드레이프 / 외형 추정', 'textile_surface'),
 '11': ('패턴과 장식', '모티프 / 기법 / 반복 / 크기 / 부피 / 부착 / 개수 / 위치', 'ornament_structure,textile_surface,clothing_structure'),
 '12': ('색상과 귀속', '색 계열 / 명도·채도 / 소유자 / 영역 / 역할 / 후보·배색 / 광원', 'color_relations'),
 '13': ('레그웨어', '종료점 / 연속성 / 투과성 / 조직 / 상단 밴드 / 연결', 'accessory_structure,clothing_structure'),
 '14': ('신발', '앞코 / 굽 / 플랫폼 / 지지끈 / 부츠 기장 / 가시성', 'accessory_structure'),
 '15': ('가방과 착용 부속', '형태 / 지지 경로 / 부착 / 착용자 / 모티프 / 선택 여부', 'accessory_structure,costume_cosplay'),
 '16': ('주얼리와 금속', '위치 / 고정 / 개수 / 비대칭 / 연결 호 / 표면 상태 / 추정 재료', 'accessory_structure,ornament_structure'),
 '17': ('콘셉트의 문맥', '정의 / 문화·시대·장르 경계 / 요청 한정 / 다중 실현 / 선택 사례', 'costume_cosplay,model_editorial,contextual_appeal'),
 '18': ('장소와 상황', '공간 기능 / 배치 / 행동 전제 / 사건 단계 / 현재 보이는 흔적', 'everyday_scene,realistic_background,model_editorial'),
 '19': ('신체·의상·소품 관계', '행위자 / 신체 소유 / 접촉점 / 목표 / 방향 / 현재 결과 / 시선', 'pose_vocabulary,fashion_fit,everyday_scene,visual_grammar'),
 '20': ('물질 상태', '국소 주름 / 장력 / 마모 / 수선 / 젖음 / 파편의 출처 / 반사', 'tactile_reality,textile_surface,fashion_fit'),
 '21': ('촬영과 관찰 범위', '카메라 위치 / 거리 / 크롭 / 광원 / 표면색 / 노출 / 이미지 평면 처리', 'portrait_composition,lighting,color_relations,editing_effects'),
}

# Existing identities checked directly in authored JSON, not inferred by similarity.
REUSE = {
 'WK024': [('photo_prompt_clothing_structure_extension.json','garment_detail','clt_ct037_v1','retain_and_review_equivalent_context')],
 'WK029': [('photo_prompt_clothing_structure_extension.json','garment_detail','clt_ct047_v1','retain_and_strengthen_owner_trace_if_needed')],
 'WK038': [('photo_prompt_clothing_structure_extension.json','garment_detail','clt_ct031_v1','retain_and_review_equivalent_context')],
 'WK046': [('photo_prompt_visual_grammar_extension.json','garment_detail','vg_ribbon_to_garment_seam','reuse_complete_existing_relation')],
 'WK048': [('photo_prompt_tags.json','surface_material','sheer_organza_chiffon_transmission','reuse_general_surface_then_split_selected_drape_variants')],
 'WK051': [('photo_prompt_reactorprompt_visual_relations_extension.json','surface_material','velvet_pile_nap_direction_surface','reuse_pile_surface_without_inferring_fiber')],
}

# Concrete alternatives to generic comparative cards. These are research proposals.
VARIANTS = {
 'WK023': [
  ('crew','The neckline of the same top forms a shallow rounded edge close to the neck base.'),
  ('scoop','The neckline of the same top forms a wider rounded opening below the neck base.'),
  ('square','Two neckline corners connect the straighter side edges to the same horizontal lower edge.'),
  ('bateau','The same garment has a broad, shallow neckline running laterally near the collarbones.'),
  ('asymmetric_bateau','The broad neckline reaches a different height at the two shoulders of the same wearer.')],
 'WK026': [
  ('strapless','The same bodice has a continuous upper edge across the torso, with support contained in the bodice.'),
  ('off_shoulder','The garment and sleeve attachment edges sit below the same wearer’s shoulder tops.'),
  ('spaghetti','Two narrow straps join the same front bodice to its back over the declared shoulders.'),
  ('halter','The support straps of the same bodice rise toward the neck and join at the declared neck attachment.')],
 'WK030': [
  ('short_puff','The short sleeve gathers at its shoulder attachment and its narrower lower edge, enclosing a rounded upper volume.'),
  ('shoulder_puff_long','The upper sleeve has a local shoulder puff while the lower sleeve remains narrow along the same arm.')],
 'WK031': [
  ('three_quarter','The loose sleeve hem ends on the same forearm below the elbow and above the wrist.'),
  ('lower_drape','Wide cloth hangs below the same elbow from the attached lower sleeve section.'),
  ('column','Long folds run along the same sleeve from its upper attachment to the wrist edge.')],
 'WK033': [
  ('lace_cuff','A lace cuff joins the same opaque sleeve at its wrist edge.'),
  ('rolled','Folded layers of the same shirt sleeve form a visible rolled edge on the forearm.'),
  ('detachable','A separate white cuff closes around the wrist with an independent edge beside the garment sleeve.')],
 'WK036': [
  ('high','The same waistband sits visibly above the wearer’s natural waist landmark.'),
  ('natural','The same waistband follows the wearer’s declared natural waist landmark.'),
  ('low','The same waistband sits visibly below the wearer’s natural waist landmark.')],
 'WK037': [
  ('a_line','The same skirt’s side outlines widen gradually from its waist toward the hem.'),
  ('bell','The skirt rounds outward below its gathered waistband before returning toward its hem.'),
  ('narrow_layers','Two distinct skirt layers hang within a comparatively narrow outer silhouette.'),
  ('lower_volume','The gown’s upper bodice stays comparatively narrow while its lower skirt carries the outward volume.')],
 'WK039': [
  ('diagonal','One diagonal textile panel edge visibly overlaps the adjacent panel of the same skirt.'),
  ('crescent','The same textile panel has a bounded crescent-shaped edge at its declared attachment.'),
  ('curved_overlay','A curved leather-like overlay follows the same boot’s surface with a visible separate edge.')],
 'WK041': [
  ('slit','A single opening separates two skirt edges from a visible upper endpoint to the hem.'),
  ('wrap_gap','The visible gap lies between two overlapping panels of the same skirt.'),
  ('drawstring','Two cord ends emerge from the same gathered side channel and join at its adjustment point.')],
 'WK050': [
  ('faille_surface','Fine transverse ribs remain visible across the same faille-like textile panel.'),
  ('satin_surface','A broad smooth sheen follows the folds of the same satin-like panel.')],
 'WK053': [
  ('rib','Parallel raised knit ribs remain visible along the same garment panel.'),
  ('cable','Raised knit columns cross over each other along the same sweater panel.'),
  ('pointelle','Ordered small openings remain within the same knitted sock panel.')],
 'WK059': [
  ('floral','Small flower motifs repeat within the same garment panel and follow its folds.'),
  ('plaid','Two intersecting stripe directions form repeated checks on the same skirt panel.'),
  ('pinstripe','Thin parallel stripes repeat along the same skirt panel and follow its fold direction.')],
 'WK062': [
  ('petal_relief','Attached flower petals rise above the same fabric surface with small local shadows.'),
  ('rhinestone','Small faceted reflective ornaments remain attached at distinct points on the same garment.'),
  ('pearl_like','Small rounded pearl-like ornaments remain attached at distinct points on the same garment.')],
 'WK075': [
  ('knee_sock','The same knitted sock has a visible top edge below the knee.'),
  ('thigh_high','The same legwear has a visible top band above the knee on the thigh.'),
  ('tights','The legwear continues upward from both legs into the same covered hip section.')],
 'WK077': [
  ('mary_jane','A strap crosses the same shoe’s instep and joins the shoe at its fastening point.'),
  ('ankle_sandal','A sandal strap wraps around the same ankle and joins the sandal’s supporting straps.'),
  ('knee_boot','The same boot shaft ends near the knee and remains distinct from the legwear edge.')],
 'WK081': [
  ('horn_headband','Two costume horns attach to the visible headband worn by the same person.'),
  ('bunny_headband','Two long costume ears attach to the visible headband worn by the same person.'),
  ('hair_ribbon','The hair ribbon’s knot and tails join the same declared hair fastening.')],
 'WK083': [
  ('pendant','A distinct pendant hangs from its chain on the same wearer.'),
  ('brooch','A brooch attaches at one visible point on the same garment surface.'),
  ('neck_armor','A separate armor-like collar surrounds the same neck above the garment neckline.')],
}

RECIPE_CARDS = {
 'R01': ['WK005','WK018','WK030','WK066','WK073','WK077'],
 'R02': ['WK019','WK029','WK038','WK040','WK051','WK072'],
 'R03': ['WK012','WK058','WK065','WK072','WK083'],
 'R04': ['WK021','WK033','WK037','WK083','WK112'],
 'R05': ['WK035','WK037','WK070','WK103'],
 'R06': ['WK023','WK046','WK050','WK063','WK070'],
 'R07': ['WK048','WK062','WK066','WK108','WK112'],
 'R08': ['WK039','WK072','WK073','WK106','WK112','WK114'],
 'R09': ['WK022','WK035','WK043','WK054','WK077'],
 'R10': ['WK035','WK037','WK043','WK071','WK077'],
 'R11': ['WK020','WK027','WK032','WK040','WK066','WK071'],
 'R12': ['WK022','WK025','WK042','WK078'],
 'R13': ['WK003','WK054','WK080','WK087'],
 'R14': ['WK006','WK008','WK093','WK106'],
 'R15': ['WK009','WK053','WK056','WK076','WK095','WK098'],
 'R16': ['WK011','WK075','WK089'],
 'R17': ['WK018','WK053','WK079','WK088','WK102'],
 'R18': ['WK010','WK023','WK051','WK081','WK092'],
 'R19': ['WK019','WK045','WK077','WK100','WK113','WK115'],
 'R20': ['WK015','WK016','WK067','WK091','WK116'],
}

ADDITIONAL_FOCUSED_MAPPINGS = {
 'WK021': [4,5], 'WK026': [20,21], 'WK035':[25,63,64],
 'WK054':[74], 'WK053':[14], 'WK060':[71], 'WK023':[143],
}


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def seed_ids(value):
    out = []
    for token in value.split(','):
        pair = [int(x) for x in token.split('-')]
        values = range(pair[0], pair[-1] + 1)
        out.extend(f'K{n:03}' for n in values)
    return list(dict.fromkeys(out))


def effects(value):
    out = []
    for token in value.split(';'):
        dimension, property_name = token.strip().split(':', 1)
        out.append({'dimension': dimension.strip(), 'target': 'main_subject', 'property': property_name.strip()})
    return out


def main():
    catalog = json.loads((HERE / 'inputs/wardrobe_keyword_catalog.json').read_text())
    keywords = {r['id']: r for r in catalog['keywords']}
    source_doc = json.loads((HERE / 'SOURCES.json').read_text())
    for s in source_doc['sources']:
        if s['id'] == 'W01':
            s['evidence_file'] = 'web-evidence/textile-definitions.txt'
    write('SOURCES.json', source_doc)
    columns = (HERE / 'CARD-SPECS.tsv').read_text().splitlines()[0].split('|')
    cards = []
    for line in (HERE / 'CARD-SPECS.tsv').read_text().splitlines()[1:]:
        parts = line.split('|')
        assert len(parts) == len(columns), (parts[0], len(parts))
        spec = dict(zip(columns, parts))
        ids = seed_ids(spec['seed_numbers'])
        ids += [f'K{n:03}' for n in ADDITIONAL_FOCUSED_MAPPINGS.get(spec['id'], [])]
        ids = list(dict.fromkeys(ids))
        efx = effects(spec['effects'])
        for e in efx:
            # Source roles differ; do not attach a non-worn blazer to the person.
            if spec['id'] == 'WK011': e['target'] = 'blazer_A'
            if e['dimension'] in {'camera','framing','composition','lighting','color'}: e['target'] = 'scene'
            if spec['id'] == 'WK061' and e['dimension'] == 'text': e['target'] = 'jersey_A'
        related_sources = sorted({s for k in ids for s in keywords[k]['source_ids']})
        public = spec['public_sources'].split(',') if spec['public_sources'] else []
        annotation = spec['slot'] == 'none'
        card = {
          'id': spec['id'], 'group': spec['group'], 'priority': spec['priority'],
          'seed_keyword_ids': ids, 'seed_coverage_role': 'focused_proposition_or_context_boundary_not_exhaustive_term_definition',
          'label_ko': spec['meaning_ko'].split('。')[0].split('. ')[0],
          'definition_ko': spec['meaning_ko'],
          'observation_mode': 'annotation_or_context_only' if annotation else 'present_visible_relation',
          'owner': spec['owner'], 'counterpart': spec['counterpart'].replace('inst e p','instep'),
          'observable_proposition_en': spec['proposition_en'],
          'components': [{'id': spec['id'].lower() + '_visible_proposition', 'positive_evidence_en': spec['proposition_en']}],
          'relations': [{'id': spec['id'].lower() + '_relation', 'type': spec['relation'],
                         'subject': spec['owner'], 'object': spec['counterpart'].replace('inst e p','instep')}],
          'confusion_boundaries_ko': spec['confusions_ko'].split(';'),
          'affected_dimensions': list(dict.fromkeys(e['dimension'] for e in efx)),
          'affected_properties': efx,
          'catalog_source_ids': related_sources, 'public_source_ids': public,
          'provenance': {'seed_semantics': 'recovered_catalog_normalization_or_description',
                         'public_facts': 'only_the_bounded_facts_in_SOURCES_json',
                         'propositions_relations_effects_and_tests': 'researcher_authored_inferences_not_public_source_quotations',
                         'original_library_files_revalidated': False},
          'claim_limits_ko': ['관련 키워드 전부의 보편 정의나 자동 의상 레시피가 아니다.',
                              '원자료의 명시·선택·추정·제외·비착용 상태를 합치지 않는다.',
                              '숨은 제작 방식·섬유 함량·신원·연령·사적 심리·시간 이력은 픽셀만으로 확정하지 않는다.'],
          'suggested_slot': None if annotation else spec['slot'],
          'variants': [{'id': k, 'positive_evidence_en': v} for k,v in VARIANTS.get(spec['id'], [])],
          'maintenance_decision': 'annotation_only_no_runtime_candidate' if annotation else (
              'reuse_existing_identity_first' if spec['id'] in REUSE else 'semantic_review_required_before_extend_or_add'),
          'confirmed_reuse_refs': [],
          'pixel_gate_proposal': None if annotation else {
              'review_scale': 'native', 'expected_evidence_en': spec['proposition_en'],
              'inspect': ['declared_owner','declared_counterpart','connection_or_boundary','distinguishing_state'],
              'not_a_global_obligation': True,
              'unobservable_policy': 'unobservable_not_pass_for_a_required_focal_relation',
              'activation': 'actual_requester_bound_requirement_or_complete_adopted_optional_variant',
              'annotation_limits': 'A current cloth position can support a plausible state, not measured force, speed or chronology.'},
          'runtime_ready': False, 'effects_verified': False, 'native_pixels_verified': False}
        for filename,slot,entry_id,decision in REUSE.get(spec['id'], []):
            d = json.loads((ROOT/'skills/photo-prompt-image-generator/assets'/filename).read_text())
            row = next(r for r in d['slots'][slot] if r['id'] == entry_id)
            card['confirmed_reuse_refs'].append({'file':filename,'slot':slot,'id':entry_id,'decision':decision,
              'existing_en':row.get('en'), 'row_sha256':hashlib.sha256(json.dumps(row, ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
        cards.append(card)
    card_map = {c['id']:c for c in cards}
    blueprints = []
    for card in cards:
        if card['suggested_slot'] is None: continue
        alternatives = card['variants'] or [{'id':'selected_relation','positive_evidence_en':card['observable_proposition_en']}]
        for variant in alternatives:
            existing = card['confirmed_reuse_refs'] if not card['variants'] else []
            blueprints.append({
              'id':f"draft_{card['id'].lower()}_{variant['id']}", 'card_id':card['id'],
              'priority':card['priority'], 'slot':card['suggested_slot'],
              'candidate_text_en':variant['positive_evidence_en'],
              'concept_units':[variant['positive_evidence_en']],
              'relations':card['relations'] if not card['variants'] else [],
              'relation_drafting_status':'bound_to_card' if not card['variants'] else 'variant_endpoints_require_specific_authored_edges',
              'affected_dimensions':card['affected_dimensions'], 'affected_properties':card['affected_properties'],
              'effect_review_status':'provisional_complete_effect_requires_variant_and_target_review',
              'prerequisites': ['Every declared wearer, garment, body part and object must be present in the allowed final scene.',
                                'Candidate effects must preserve requester-owned whole-dimension and property locks.',
                                'A candidate may develop an open detail only within its fully declared effect.'],
              'applicability': 'selected_concrete_variant_after_core_freeze',
              'candidate_only':True, 'automatic_hard_activation':False,
              'source_keyword_ids_are_aliases':False,
              'reuse_refs':existing,
              'confusion_boundaries_ko':card['confusion_boundaries_ko'],
              'source_card_provenance':card['provenance'],
              'required_before_runtime': ['settle_variant_owner_and_complete_effect','review_positive_alias_equivalence',
                                           'resolve_existing_id_reuse','write_authored_components_without_generated_fields',
                                           'validate_dictionary_and_references','rebuild_required_indexes','publish_verified_generation',
                                           'verify_candidate_exposure_and_optional_adoption'],
              'runtime_ready':False,'effects_verified':False,'native_pixels_verified':False})
    write('SEMANTIC-CARDS.json', {'schema_version':'wardrobe-visual-research-cards/v1','cards':cards})
    write('CANDIDATE-BLUEPRINTS.json', {'schema_version':'wardrobe-candidate-research-blueprints/v1','runtime_ready':False,'drafts':blueprints})
    coverage_doc=json.loads((HERE/'KEYWORD-COVERAGE.json').read_text())
    for row in coverage_doc['rows']:
        related=[c['id'] for c in cards if row['id'] in c['seed_keyword_ids']]
        fam=FAMILIES[row['category'][:2]]
        row.update({'research_card_ids':related,'research_depth':'focused_card_mapping' if related else 'family_axes_only',
          'research_family':fam[0],'family_observation_axes':fam[1].split(' / '),
          'planned_data_families':fam[2].split(','),
          'semantic_equivalence_review':'pending_except_named_reuse_decisions'})
    write('KEYWORD-COVERAGE.json',coverage_doc)
    with (HERE/'KEYWORD-RESEARCH-ROUTING.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['id','keyword_en','usage_status','candidate_lexical_status','research_card_ids','research_depth','planned_data_families'])
        for r in coverage_doc['rows']:w.writerow([r['id'],r['keyword_en'],r['usage_status'],r['candidate_lexical_status'],';'.join(r['research_card_ids']),r['research_depth'],';'.join(r['planned_data_families'])])
    recipes=[]
    for row in catalog['analyzed_combinations']:
        related=RECIPE_CARDS[row['id']]
        recipes.append({**row,'research_card_ids':related,'origin':'recovered_combination_with_researcher_structural_analysis',
          'always_optional_recipe':True,'hard_activation_from_style_label':False,
          'seed_source_authority':'historical_example_not_current_request',
          'reconstruction_axes':['garment_owner_and_layer_order','color_region_and_accent_count','material_region',
                                 'attachment_and_closure','action_contact_and_current_result','frame_visibility'],
          'adoption_rule':'all introduced owners, garments, props and effects must be grounded and compatible; style label alone does not request the entire example',
          'semantic_review_status':'research_proposal','runtime_ready':False,'native_pixels_verified':False})
    write('COMBINATION-ANALYSIS.json',{'schema_version':'wardrobe-optional-combination-research/v1','recipes':recipes})
    exclusions=[{**r,'current_request_default':False,'source_scope_required':True,
                 'matching_policy':'exact_current_request_exclusion_after_directive_prefix_normalization; no category expansion',
                 'research_role':'negative_control_pair_not_runtime_negative_pool'} for r in catalog['contextual_exclusions']]
    write('CONTEXT-BOUNDARIES.json',{'schema_version':'wardrobe-context-boundary-research/v1','exclusions':exclusions,
      'special_cases':['K002 button-down normalization','K035 unworn blazer','K049 type uncertainty','K050 structural ambiguity',
                       'S02 costume-color placeholder','S07 alternative palette','S11 unverified naval rank','K324 barefoot versus out-of-frame footwear',
                       'K262 color versus material','descriptive material and color guesses']})
    counts={'seed_keywords':len(keywords),'categories':len(FAMILIES),'cards':len(cards),
      'card_priorities':dict(collections.Counter(c['priority'] for c in cards)),
      'card_modes':dict(collections.Counter(c['observation_mode'] for c in cards)),
      'candidate_blueprints':len(blueprints),'optional_combination_analyses':len(recipes),
      'contextual_exclusions':len(exclusions),'public_sources':len(source_doc['sources']),
      'routing_depth':dict(collections.Counter(r['research_depth'] for r in coverage_doc['rows']))}
    write('RESEARCH-COUNTS.json',counts)
    md=['# 시각 의미 리서치 카드', '', '이 문서는 연구 설계이다. 각 카드는 키워드의 특정 관찰 관계 또는 문맥 경계를 다룬다. 전체 보편 정의·런타임 데이터·이미지 검증 결과가 아니다.', '',
        '[조사 보고서](RESEARCH.md) · [반영 계획](IMPLEMENTATION-PLAN.md) · [원본 사전](inputs/wardrobe_keyword_catalog.md)', '']
    for c in cards:
        md += [f"## {c['id']} · {c['group']} · {c['priority']}", '', c['definition_ko'], '',
               f"- 대상 키워드: {', '.join(c['seed_keyword_ids'])}",
               f"- 관찰 명제: {c['observable_proposition_en']}",
               f"- 관계: `{c['owner']}` → `{c['relations'][0]['type']}` → `{c['counterpart']}`",
               f"- 혼동 경계: {'; '.join(c['confusion_boundaries_ko'])}",
               f"- 반영 방식: {c['maintenance_decision']}",
               f"- 기존 항목: {', '.join(r['slot']+':'+r['id'] for r in c['confirmed_reuse_refs']) or '의미 대조 후 결정'}",
               f"- 근거: 원사전 {', '.join(c['catalog_source_ids'])}; 공개 일반 사실 {', '.join(c['public_source_ids']) or '별도 사실 주장 없음'}", '']
        for v in c['variants']:md += [f"  - 선택 변형 `{v['id']}`: {v['positive_evidence_en']}"]
        if c['variants']:md.append('')
    (HERE/'CARD-CATALOG.md').write_text('\n'.join(md)+'\n')
    print(json.dumps(counts,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
