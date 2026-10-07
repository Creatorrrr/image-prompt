"""Build research-only companions; no runtime source, index, or image writes."""
from __future__ import annotations
import json
import pathlib
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def read(name):
    return json.loads((HERE / name).read_text())

def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def md(name, lines):
    (HERE / name).write_text('\n'.join(lines).rstrip() + '\n')

sources = read('SOURCES.json')
source_map = {s['id']: s for s in sources['sources']}
topics = read('TOPIC-SOURCE-MAP.json')
cards = read('SEMANTIC-SPEC.json')['cards']
seeds = read('SEED-KEYWORDS.json')['items']
audit = read('EXISTING-DATA-AUDIT.json')
literal = {r['seed_id']: r for r in audit['seed_results']}

manifest = json.loads((ASSETS / 'photo_prompt_source_manifest.json').read_text())
source_files = list(dict.fromkeys(['photo_prompt_tags.json', 'photo_prompt_visual_obligations.json'] + [s['file'] for s in manifest['sources'] if s['kind'] in ('candidate', 'visual_profile') and (ASSETS / s['file']).exists()]))
entities = defaultdict(list)
slots = set()
for name in source_files:
    doc = json.loads((ASSETS / name).read_text())
    for slot, entries in doc.get('slots', {}).items():
        slots.add(slot)
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and entry.get('id'):
                    entities[entry['id']].append({'kind': 'candidate', 'file': name, 'slot': slot, 'id': entry['id']})
    for profile in doc.get('profiles', []):
        entities[profile['id']].append({'kind': 'visual_profile', 'file': name, 'id': profile['id']})

DOMAIN_FILES = {
    'expression': ('photo_prompt_acting_expression_extension.json', 'photo_prompt_visual_obligations_acting_expression.json'),
    'eye_detail': ('photo_prompt_character_appearance_extension.json', 'photo_prompt_visual_obligations_character_appearance.json'),
    'body_orientation': ('photo_prompt_pose_vocabulary_extension.json', 'photo_prompt_visual_obligations_pose_vocabulary.json'),
    'composition': ('photo_prompt_portrait_composition_extension.json', 'photo_prompt_visual_obligations_portrait_composition.json'),
    'focus': ('photo_prompt_editing_effects_extension.json', 'photo_prompt_visual_obligations.json'),
    'hair_style': ('photo_prompt_character_appearance_extension.json', 'photo_prompt_visual_obligations_character_appearance.json'),
    'hair_color': ('photo_prompt_tags.json', 'photo_prompt_visual_obligations_character_appearance.json'),
    'makeup_style': ('photo_prompt_tags.json', 'photo_prompt_visual_obligations.json'),
    'lip_finish': ('photo_prompt_tags.json', 'photo_prompt_visual_obligations.json'),
    'garment_detail': ('photo_prompt_clothing_structure_extension.json', 'photo_prompt_visual_obligations_clothing_structure.json'),
    'surface_material': ('photo_prompt_textile_surface_extension.json', 'photo_prompt_visual_obligations_textile_surface.json'),
    'wearable_accessory': ('photo_prompt_ornament_structure_extension.json', 'photo_prompt_visual_obligations_ornament_structure.json'),
    'prop': ('photo_prompt_ethereal_gothic_scene_extension.json', 'photo_prompt_visual_obligations_ethereal_gothic_scene.json'),
    'texture': ('photo_prompt_ethereal_gothic_scene_extension.json', 'photo_prompt_visual_obligations_ethereal_gothic_scene.json'),
    'location': ('photo_prompt_realistic_background_extension.json', 'photo_prompt_visual_obligations_realistic_background.json'),
    'light_shape': ('photo_prompt_lighting_extension.json', 'photo_prompt_visual_obligations.json'),
    'light_direction': ('photo_prompt_lighting_extension.json', 'photo_prompt_visual_obligations.json'),
    'light_type': ('photo_prompt_lighting_extension.json', 'photo_prompt_visual_obligations.json'),
    'lighting': ('photo_prompt_lighting_extension.json', 'photo_prompt_visual_obligations.json'),
    'color': ('photo_prompt_palette_applications_extension.json', 'photo_prompt_visual_obligations_palette_applications.json'),
    'quality': ('photo_prompt_editing_effects_extension.json', 'photo_prompt_visual_obligations.json'),
    'color_grading': ('photo_prompt_editing_effects_extension.json', 'photo_prompt_visual_obligations_editing_effects.json'),
    'grain_profile': ('photo_prompt_editing_effects_extension.json', 'photo_prompt_visual_obligations_editing_effects.json'),
    'ambient_particle': ('photo_prompt_ethereal_gothic_scene_extension.json', 'photo_prompt_visual_obligations_ethereal_gothic_scene.json'),
    'genre': ('photo_prompt_tags.json', None),
    'aesthetic_trend': ('photo_prompt_tags.json', None),
    'costume_style': ('photo_prompt_historical_womenswear_extension.json', None),
}

compiled_cards = []
mapping = []
for c in cards:
    c['source_ids'] = list(dict.fromkeys(sid for topic in c['source_topics'] for sid in topics[topic]))
    c['source_coverage'] = 'Only SOURCES.json claims are externally supported. These components, relations and candidate choices are authored research proposals.'
    c['existing_references'] = [ref for eid in c['integration']['existing_ids'] for ref in entities[eid]]
    c['source_access_limits'] = [sid for sid in c['source_ids'] if any(t in source_map[sid]['access'] for t in ('snippet', 'search_text', 'excerpt', 'metadata')) and sid != 'R00']
    compiled_cards.append(c)
    home = DOMAIN_FILES[c['integration']['proposed_slot']]
    if c['id'] in ('EG04', 'EG32', 'EG40', 'EG49', 'EG51', 'EG52', 'EG56'):
        home = ('photo_prompt_ornament_structure_extension.json', 'photo_prompt_visual_obligations_ornament_structure.json')
    if c['id'] in ('EG53', 'EG54', 'EG55'):
        home = ('photo_prompt_ethereal_gothic_scene_extension.json', 'photo_prompt_visual_obligations_ethereal_gothic_scene.json')
    mapping.append({
        'card_id': c['id'], 'treatment': c['integration']['treatment'],
        'priority': c['integration']['priority'], 'proposed_slot': c['integration']['proposed_slot'],
        'slot_exists_in_raw_authored_sources': c['integration']['proposed_slot'] in slots,
        'existing_references': c['existing_references'],
        'proposed_candidate_home': home[0], 'proposed_profile_home': home[1],
        'new_file_requires_manifest_registration': bool(home[0] and not (ASSETS / home[0]).exists()),
        'owner_resolution': 'Bind research owner paths to actual frozen core owners before authoring runtime properties.',
        'affected_properties_status': 'PROPOSED_DOMAIN_ONLY_NOT_RUNTIME_VALIDATED',
        'runtime_schema_validation': 'NOT_RUN',
    })
write('SEMANTIC-CARDS.json', {'schema_version': 'research-semantic-cards/v1', 'status': 'PROPOSED_NOT_INTEGRATED', 'cards': compiled_cards})
write('RUNTIME-MAPPING.json', {'schema_version': 'research-runtime-mapping/v1', 'status': 'PROPOSED_NOT_RUN', 'entries': mapping})

drafts = []
for c in cards:
    if c['integration']['treatment'] not in ('NEW_SIBLING', 'ENRICH_EXISTING'):
        continue
    variants = [(c['key'], '; '.join(c['observable_components']), c['observable_components'])]
    if c['id'] == 'EG48':
        variants = [
            ('frost_on_petals', 'Small pale ice-like crystals cling to the named dark petal surfaces; the petal folds remain readable.', ['Small pale ice-like crystals cling to the declared petal surface.', 'The dark petal folds remain readable behind the localized crystals.']),
            ('dew_on_petals', 'Discrete clear droplets rest along the named petal edges; each droplet remains separate from film grain.', ['Separate clear droplets lie on the named petal edge.', 'The droplet boundaries remain distinct from picture-plane grain.']),
            ('dried_curled_petals', 'The named dry petals have localized curled edges and uneven faded surface tones; no frost or droplets are added.', ['Localized dry curled edges belong to the named petals.', 'Faded tones remain on the same petals without added wet droplets.']),
        ]
    for key, en, components in variants:
        drafts.append({
            'draft_id': 'egr_' + key, 'semantic_card_id': c['id'], 'ko_label': c['label_ko'],
            'en': en, 'proposed_slot': c['integration']['proposed_slot'],
            'treatment': c['integration']['treatment'], 'status': 'PROPOSED_NOT_INTEGRATED',
            'is_runtime_record': False, 'source_ids': c['source_ids'],
            'concept_units_proposal': components, 'relations_proposal': c['directed_relations'],
            'confusion_negatives': c['confusion_boundaries'], 'existing_references': c['existing_references'],
            'selection_preconditions': ['The required owners already exist in the frozen core or are explicitly selected within an open dimension.', 'Read the entire candidate and bind every component to the same declared owners.', 'Do not add age, ethnicity, personality, exposure, extra people, faith, historical identity or new objects from style labels.'],
            'excluded_automatic_assumptions': ['No fixed lens distance, light ratio, color temperature, exact lip gap, HEX code, generation provider or fabrication history.'],
            'locked_dimension_rule': 'A required assertion can affect only a locked requested property; optional support cannot overwrite frozen closed properties.',
            'owner_property_binding': 'REQUIRES_RUNTIME_CONTRACT_REVIEW',
        })
write('CANDIDATE-DRAFTS.json', {'schema_version': 'research-candidate-drafts/v1', 'status': 'PROPOSED_NOT_INTEGRATED', 'is_runtime_schema': False, 'items': drafts})

bundle_defs = [
    ('EB01', '중앙 세로광의 초상 구성', ['EG13','EG60','EG61','EG62'], 'A bust portrait, one rear aperture and the selected receiving contours already exist. Aperture and rim need separate evidence.'),
    ('EB02', '고요한 눈꺼풀·시선·입술', ['EG07','EG08','EG09','EG10'], 'One declared adult portrait face and separate head/eye axes exist. Sleep, menace and desire remain absent unless separately requested.'),
    ('EB03', '낮은 번·앞머리·옆머리·리본', ['EG18','EG19','EG20','EG21'], 'The same hair owner and its ribbon fastening are selected. Preserve the requested hair length and color.'),
    ('EB04', '하이넥 레이스·안감·튈', ['EG27','EG28','EG32','EG34'], 'Declare distinct collar, lace panel, tulle panel and underlayer owners; reject the bundle if the selected garment lacks them.'),
    ('EB05', '실제 매화 가지와 초상 여백', ['EG14','EG15','EG17','EG41'], 'Physical scene branches occupy declared planes around the same portrait; painted motifs are not substitutes.'),
    ('EB06', '회화 꽃가지가 있는 금박 패널', ['EG05','EG53'], 'One physical backdrop carries painted floral motifs and a selected reflective gold-like surface. Do not infer live flowers.'),
    ('EB07', '어두운 옷·장식의 재질 분리', ['EG28','EG32','EG39','EG52'], 'The declared garment and existing accessory have separate cloth and metal owners. No accessory is created just to satisfy this bundle.'),
    ('EB08', '절제된 확산·톤·그레인', ['EG65','EG66','EG67','EG68','EG69'], 'Select an explicit optical variant, output tone, grain and owner-specific palette. A generic matte label does not require every member.'),
]
bundles = [{'id': bid, 'label_ko': ko, 'card_ids': ids, 'status': 'PROPOSED_NOT_INTEGRATED', 'is_runtime_schema': False, 'candidate_draft_refs': [d['draft_id'] for d in drafts if d['semantic_card_id'] in ids], 'existing_data_refs': list(dict.fromkeys(eid for c in cards if c['id'] in ids for eid in c['integration']['existing_ids'])), 'precondition': pre, 'adoption_rule': 'Optional composition recipe. Select members deliberately; an adopted member must satisfy all its components. Do not auto-activate the entire recipe from an aesthetic label.'} for bid, ko, ids, pre in bundle_defs]
write('BUNDLE-DRAFTS.json', {'schema_version': 'research-bundle-drafts/v1', 'items': bundles})

palettes = []
for seed in seeds:
    if seed['category'] != 16:
        continue
    terms = [s.strip() for s in seed['en'].split('+')]
    palettes.append({'id': 'PAL_' + seed['id'], 'seed_id': seed['id'], 'phrase': seed['en'], 'status': 'PROPOSED_NOT_INTEGRATED', 'color_terms': terms, 'roles_proposal': [{'color': terms[0], 'role': 'dominant_existing_field'}, {'color': terms[1], 'role': 'secondary_existing_surface_or_light'}, {'color': terms[2], 'role': 'small_existing_accent_owner'}], 'owner_binding': 'Resolve the three roles to actual requested owners; this proposal does not create those owners or prescribe skin color.', 'constraints': ['No universal HEX values, area ratios or usage-frequency ranking.', 'Material local color, light color and global grading are separate.', 'Metal-associated color words do not require that metal object.'], 'related_card': 'EG69'})
write('PALETTE-ROLE-DRAFTS.json', {'schema_version': 'research-palette-role-drafts/v1', 'items': palettes})

category_routes = {
 1: ['EG01','EG03','EG04','EG05','EG06','EG29'], 2: ['EG02','EG70'],
 3: ['EG07','EG08','EG09','EG10','EG11','EG12'], 4: ['EG13','EG14','EG15','EG16','EG17'],
 5: ['EG18','EG19','EG20','EG21','EG22'], 6: ['EG23','EG24','EG25','EG26'],
 7: ['EG27','EG28','EG29','EG30','EG31'], 8: ['EG32','EG33','EG34','EG35','EG36','EG37','EG38','EG39','EG40'],
 9: ['EG41','EG42','EG43','EG44','EG45','EG46','EG47','EG48'], 10: ['EG49','EG50','EG51','EG52'],
 11: ['EG53','EG54','EG55','EG56'], 12: ['EG57','EG58','EG59'],
 13: ['EG60','EG61','EG62','EG63','EG64'], 14: ['EG17','EG24','EG65','EG66'],
 15: ['EG69','EG52'], 16: ['EG69'], 17: ['EG65','EG66','EG67','EG68'], 18: ['EG03','EG48','EG70'],
}
term_routes = [
 ('art nouveau', ['EG04']), ('symbolist', ['EG03']), ('mourning', ['EG29','EG37']),
 ('half-lidded', ['EG07','EG12']), ('eyelid', ['EG07','EG12']), ('upward', ['EG08','EG09']), ('closed eyes', ['EG11']), ('parted lips', ['EG10']),
 ('low coiled bun', ['EG18']), ('chignon', ['EG18']), ('fringe', ['EG19']), ('tendrils', ['EG20']), ('ribbon', ['EG21']),
 ('skin texture', ['EG23']), ('reflected light', ['EG24']), ('mauve eyeshadow', ['EG25']), ('lips', ['EG26']),
 ('collar', ['EG27']), ('sheer', ['EG28','EG35','EG36']), ('corsage', ['EG30']), ('rosettes', ['EG31']),
 ('chantilly', ['EG32']), ('tulle', ['EG33','EG34']), ('organza', ['EG35']), ('chiffon', ['EG36']), ('crape', ['EG37']), ('corded silk', ['EG38']), ('velvet', ['EG39']), ('embroidery', ['EG40']),
 ('plum blossom', ['EG41']), ('camellia', ['EG42']), ('magnolia', ['EG43']), ('lily-of-the-valley', ['EG44']), ('black roses', ['EG45']), ('gypsophila', ['EG46']), ('fern', ['EG47']), ('frost', ['EG48']), ('dew', ['EG48']), ('dried petal', ['EG48']),
 ('filigree', ['EG49']), ('pearl', ['EG50']), ('beads', ['EG50']), ('cameo', ['EG51']), ('patina', ['EG52']), ('tarnished', ['EG52']),
 ('gold-leaf', ['EG53']), ('gilding', ['EG53','EG55']), ('mosaic', ['EG54']), ('flaking', ['EG55']), ('gilded branch', ['EG56']),
 ('charcoal', ['EG57','EG69']), ('niche', ['EG58']), ('mirror', ['EG59']),
 ('light slit', ['EG60']), ('axial backlight', ['EG60']), ('rim light', ['EG61']), ('fill', ['EG62']), ('low-key', ['EG63']), ('cooler face', ['EG64']),
 ('diffusion', ['EG65']), ('bloom', ['EG65']), ('halation', ['EG65']), ('roll-off', ['EG66']), ('grain', ['EG67']), ('lifted', ['EG68']),
]
coverage = []
for seed in seeds:
    term_ids = list(dict.fromkeys(cid for term, ids in term_routes if term in seed['en'].lower() for cid in ids))
    routes = term_ids or category_routes[seed['category']]
    coverage.append({'seed_id': seed['id'], 'en': seed['en'], 'ko': seed['ko'], 'category': seed['category'], 'research_card_routes': routes, 'routing_basis': 'TERM_FAMILY_REVIEW_REQUIRED' if term_ids else 'CATEGORY_ROUTE_REVIEW_REQUIRED', 'is_semantic_equivalence_or_runtime_coverage': False, 'lexical_hit_count': literal[seed['id']]['lexical_hit_count'], 'lexical_hits': literal[seed['id']]['lexical_hits'], 'review_requirement': 'Compare all requested components, carriers, variants and negatives before deciding reuse, enrichment, a new sibling or no activation.'})
write('KEYWORD-COVERAGE.json', {'schema_version': 'research-keyword-coverage/v1', 'visible_seed_count': len(seeds), 'unrecovered_seed_count': 10, 'coverage_meaning': 'All visible keywords have a review destination; routing does not certify exact meaning, active data or generation support.', 'items': coverage})

lines = ['# 시각 의미 카드 초안', '', '상태: PROPOSED_NOT_INTEGRATED · 2026-10-07', '', '이 문서는 출처 사실을 바탕으로 작성한 시각 연출 제안이다. 모든 카드가 운영 프로파일 한 개에 대응하는 것은 아니다. 계열 카드 안의 대안은 따로 좁혀 작성한다. 분위기 문맥과 보류 카드는 hard obligation으로 승격하지 않는다. 숨겨진 요소는 미관찰이며, 일부만 보이는 결과는 해당 카드의 전체 통과가 아니다.', '']
for c in cards:
    lines += ['## ' + c['id'] + ' · ' + c['label_ko'], '', '- 처리: ' + c['integration']['treatment'] + ' · ' + c['integration']['priority'] + ' · 후보 슬롯 제안: `' + c['integration']['proposed_slot'] + '`', '- 소유자: ' + ', '.join('`'+v+'`' for v in c['owners']), '- 관찰 요소: ' + ' / '.join(c['observable_components']), '- 관계: ' + '; '.join(r['subject']+' → '+r['type']+' → '+r['object'] for r in c['directed_relations']), '- 혼동 경계: ' + ' / '.join(c['confusion_boundaries']), '- 기존 ID: ' + (', '.join('`'+v+'`' for v in c['integration']['existing_ids']) or '없음 또는 추가 도메인 확인 필요'), '- 근거: ' + ', '.join('['+sid+' · '+source_map[sid]['title']+']('+source_map[sid]['url']+')' for sid in c['source_ids']), '- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.', '- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.', '']
md('SEMANTIC-CARDS.md', lines)

lines = ['# 출처와 근거 범위', '', '접근일: 2026-10-07 · Asia/Seoul', '', '기관·제조사 자료, 작가의 실제 촬영 기록, 공개 프롬프트 예시는 서로 다른 근거다. access의 delegate는 해당 분담 연구자가 본문을 확인했음을 뜻한다. 검색 추출문·PDF 일부·본문 접근 실패는 제한 상태로 유지한다. 출처에 쓰인 장비·인물·제작 공정을 생성 결과의 실제 이력으로 주장하지 않는다.', '']
for s in sources['sources']:
    lines += ['## ' + s['id'] + ' · [' + s['title'] + '](' + s['url'] + ')', '', '- 종류: ' + s['source_type'] + ' · 확인: ' + s['access'] + ' · 발행/작품 시점: ' + s['published'], '- 확인한 주장: ' + ' '.join(s['claims_ko']), '- 적용 한계: ' + ' '.join(s['limits_ko']), '']
lines += ['## 재확인되지 않은 이전 출처', '']
for s in sources['source_leads_not_reverified']:
    lines += ['- **' + s['title'] + '**: ' + s['status'] + '. ' + s['reason']]
md('SOURCES.md', lines)

counts = Counter(c['integration']['treatment'] for c in cards)
write('PACKAGE-SUMMARY.json', {'status': 'RESEARCH_DRAFTS_COMPLETE_RUNTIME_NOT_RUN', 'semantic_cards': len(cards), 'treatments': dict(counts), 'candidate_drafts': len(drafts), 'new_sibling_drafts': sum(d['treatment']=='NEW_SIBLING' for d in drafts), 'enrichment_drafts': sum(d['treatment']=='ENRICH_EXISTING' for d in drafts), 'bundles': len(bundles), 'palette_role_drafts': len(palettes), 'visible_keywords': len(seeds), 'missing_keywords': 10, 'external_sources': len(sources['sources'])-1})
print(json.dumps(read('PACKAGE-SUMMARY.json'), ensure_ascii=False))
