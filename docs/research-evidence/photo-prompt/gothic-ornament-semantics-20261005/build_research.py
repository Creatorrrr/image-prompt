"""Build research drafts, not runtime registries, from reviewed annotation tables."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATUS = 'RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA'

def read(name):
    return json.loads((HERE / name).read_text())

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def table(name):
    with (HERE / name).open() as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def clean(value):
    return value.replace('|', '/').replace('\n', ' ')

ROUTES = {
    'composition': ('photo_prompt_portrait_composition_extension.json', 'photo_prompt_visual_obligations_portrait_composition.json'),
    'accessory': ('photo_prompt_accessory_structure_extension.json', 'photo_prompt_visual_obligations_accessory_structure.json'),
    'textile': ('photo_prompt_textile_surface_extension.json', 'photo_prompt_visual_obligations_textile_surface.json'),
    'architecture': ('photo_prompt_palace_fortification_extension.json', 'photo_prompt_visual_obligations_palace_fortification.json'),
    'historical': ('photo_prompt_historical_womenswear_extension.json', 'photo_prompt_visual_obligations_historical_womenswear.json'),
    'subculture': ('photo_prompt_subculture_extension.json', None),
    'fetish': ('photo_prompt_sensual_fetish_fashion_extension.json', None),
    'iconography': ('photo_prompt_religion_iconography_extension.json', 'photo_prompt_visual_obligations_religion_iconography.json'),
    'fantasy': ('photo_prompt_imaginal_extension.json', 'photo_prompt_visual_obligations.json'),
    'worldbuilding': ('photo_prompt_worldbuilding_extension.json', None),
    'light': ('photo_prompt_lighting_extension.json', 'photo_prompt_visual_obligations.json'),
    'medium': ('photo_prompt_tags.json', None),
}
PROCESS_LIMIT = 'Visible appearance cannot prove fabrication method, material authenticity, hidden fastening, date, function, identity or intent.'
GENERAL_LIMIT = 'Owner, placement and relevant boundaries must remain visible; a nearby substitute or inferred occluded relation is not a pass.'
CONTEXT_KINDS = {'density', 'descriptor', 'style_family', 'fashion_family', 'theme', 'context', 'narrative', 'production_process', 'authoring_composite'}
DEFER_SPECIFIC = {22, 27, 90, 91, 97, 100, 111, 112}

def source_units():
    keywords = {r['number']: r for r in read('SOURCE-KEYWORDS.json')['entries']}
    units = []
    for row in table('term_annotations.tsv'):
        number = int(row['number'])
        source = keywords[number]
        components = [x.strip() for x in row['observable_realization_en'].split(';')]
        contextual = row['kind'] in CONTEXT_KINDS
        units.append({
            'id': f'GO{number:03}', 'source_number': number, 'source_label': source['label'],
            'source_section': source['section'], 'source_span': {'start': source['source_start'], 'end': source['source_end']},
            'kind': row['kind'], 'owner_family': row['family'], 'meaning_ko': row['meaning_ko'],
            'observable_realization_en': components,
            'realization_status': 'ONE_OPTIONAL_REALIZATION_NOT_UNIVERSAL' if contextual else 'SELECTED_VISIBLE_VARIANT_DRAFT',
            'component_logic': 'Conjunction applies only after this particular variant and owner are explicitly bound; the broad term does not require every listed realization.',
            'confusion_boundaries': [row['confusion_boundary_ko']],
            'claim_limits': [row['claim_limit_ko'], GENERAL_LIMIT] + ([PROCESS_LIMIT] if row['kind'] in {'craft_process', 'textile_process', 'production_process'} else []),
            'sources': row['sources'].split(','),
            'evidence_status': 'SOURCE_TEXT_PLUS_AUTHORING_INFERENCE',
            'follow_up': 'Focused work/object sources and native form comparisons required before narrow historical/subgenre activation.' if number in DEFER_SPECIFIC else 'Verify current owner, shape specificity, and native observability before adoption.',
            'hard_activation_plan': 'Never activate a fixed outfit/object palette from this broad label alone.' if contextual else 'Only exact context-valid selected form on a bound owner may become required; process claims remain outside pixel gates.',
            'suggested_route': dict(candidate_owner=ROUTES[row['family']][0], profile_owner=ROUTES[row['family']][1]),
            'status': STATUS,
        })
    for row in table('supplement_annotations.tsv'):
        units.append({
            'id': row['id'], 'source_number': None, 'source_label': row['label'], 'source_section': 'AUTHORING_SUPPLEMENT',
            'kind': 'authoring_supplement', 'owner_family': row['family'], 'meaning_ko': row['meaning_ko'],
            'observable_realization_en': [x.strip() for x in row['observable_realization_en'].split(';')],
            'realization_status': 'SELECTED_VISIBLE_VARIANT_DRAFT',
            'component_logic': 'A researcher-authored relation proposal, not a recovered conversation term or a universal source definition.',
            'confusion_boundaries': [row['confusion_boundary_ko']], 'claim_limits': [GENERAL_LIMIT, PROCESS_LIMIT],
            'sources': row['sources'].split(','), 'evidence_status': 'SOURCE_TEXT_PLUS_AUTHORING_INFERENCE',
            'hard_activation_plan': 'Only a specifically requested and fully bound visible variant may be required.',
            'suggested_route': dict(candidate_owner=ROUTES[row['family']][0], profile_owner=ROUTES[row['family']][1]),
            'status': STATUS,
        })
    return units

REUSE_IDS = {
    'GD13': ['sff_pro_j06'], 'GD14': ['sff_pro_j06'], 'GD20': ['sff_pro_j07'],
    'GD29': ['hw_brocade_raised_motifs_1', 'brocade_raised_supplementary_weft_surface', 'brocade_supplementary_pattern_texture'],
    'GD30': ['hw_damask_tonal_pattern_1'],
    'GD50': ['pf_muqarnas_location', 'pf_muqarnas_composition'],
    'GD52': ['victorian_gothic_world'],
    'GD56': ['gothic_lolita_dress'],
    'GD58': ['mortality_symbol_still_life', 'mortality_symbol_contemplation', 'extinguished_candle_prop'],
    'GD65': ['chiaroscuro', 'chiaroscuro_window_light', 'baroque_gilded_chiaroscuro_lighting'],
}

def candidates(units):
    lookup = {u['id']: u for u in units}
    inventory = read('AUTHORING-INVENTORY.json')
    active_files = set(read('CHECKOUT-SNAPSHOT.json')['authored_source_sha256'])
    result = []
    for row in table('candidate_specs.tsv'):
        ids = row['unit_ids'].split(',')
        effects = []
        for area in row['effect_areas'].split(';'):
            dimension, property_area = area.split('.', 1)
            if dimension == 'scale_relation':
                dimension, property_area = 'composition', 'part_hierarchy'
            effects.append({'dimension': dimension, 'target_binding': row['owner_binding'], 'proposed_property_area': property_area})
        retained = []
        for id in REUSE_IDS.get(row['id'], []):
            for entry in inventory['review_candidates']:
                if entry['id'] == id:
                    retained.append({k: entry.get(k) for k in ['file', 'slot', 'id', 'en', 'concept_units', 'relations', 'affected_dimensions', 'affected_properties']})
        route = ROUTES[row['family']]
        if row['owner_binding'].startswith(('bound_', 'selected_')) and row['slot'] == 'prop' and row['family'] == 'accessory':
            owner_review = 'Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.'
        else:
            owner_review = 'Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.'
        result.append({
            'draft_id': row['id'], 'label_ko': row['label_ko'], 'unit_ids': ids,
            'sources': sorted({s for id in ids for s in lookup[id]['sources']}),
            'proposed_slot': row['slot'], 'owner_binding': row['owner_binding'],
            'positive_concept_units': list(dict.fromkeys(phrase for id in ids for phrase in lookup[id]['observable_realization_en'])),
            'proposed_relations': [{'relation_id': row['id'].lower() + '_owner_topology', 'source_owner_binding': row['owner_binding'], 'predicate_description_en': row['relation_topology'], 'targets': ids}],
            'proposed_effects': effects,
            'effect_mapping_status': 'REQUIRES_CURRENT_DIMENSION_TARGET_PROPERTY_BINDING; proposed_property_area is not a validated runtime property path.',
            'proposed_owner': {'candidate_file': route[0], 'profile_file': route[1], 'candidate_file_registered_now': route[0] in active_files, 'profile_file_registered_now': route[1] in active_files if route[1] else False},
            'current_reuse_records': retained,
            'owner_review': owner_review,
            'adoption_choice': 'REUSE_AND_EXTEND_CURRENT_MEANING' if retained else 'REVIEW_EXISTING_COMPONENTS_BEFORE_NEW_ATOM',
            'applicability': [
                'A compatible owner and its requested role are already bound in the frozen core.',
                'Every effect must be open or preserve an explicitly locked property; material/color/composition changes need their own compatibility review.',
                'No new actor, exposure, event, identity, historical date, functioning mechanism, or process claim follows from ornament alone.',
            ],
            'variant_exclusivity': row['notes'],
            'confusion_boundaries': list(dict.fromkeys(x for id in ids for x in lookup[id]['confusion_boundaries'])),
            'render_requirement_policy': 'Optional until adopted; if selected as required, owner + topology + boundaries + observability are all-of. Broad family labels do not activate every member.',
            'status': STATUS,
        })
    return result

BUNDLES = [
    ('GB01', '필리그리 주얼리', ['GD13', 'GD14', 'GD11'], 'Choose exactly one backing variant; rosette is an independently optional member.'),
    ('GB02', '세공 프레임', ['GD05', 'GD06', 'GD07', 'GD10'], 'Alternative motif structures; do not require every historical motif.'),
    ('GB03', '패턴 금속 표면', ['GD18', 'GD19', 'GD27'], 'Incised appearance variants; fabrication processes are not pixel conclusions.'),
    ('GB04', '에나멜 구획', ['GD20', 'GD21', 'GD22'], 'Cloisonne-like, champleve-like, and niello-like structures remain separate alternatives.'),
    ('GB05', '직조/망/브리지의 비교', ['GD29', 'GD30', 'GD31', 'GD32'], 'Select the requested material structure; lining/exposure stays independent.'),
    ('GB06', '겹친 의상 장식', ['GD33', 'GD34', 'GD39', 'GD42'], 'Only the selected attachment and layer order are all-of; no extra trims by label alone.'),
    ('GB07', '코르셋의 읽히는 구조', ['GD40', 'GD41'], 'Front busk and lacing locations bind separately; preserve torso shape and exposure locks.'),
    ('GB08', '고딕 건축 구획', ['GD43', 'GD44', 'GD45', 'GD46', 'GD48', 'GD52'], 'Choose plate/bar and lobe-count variants; terminal attachment is independent.'),
    ('GB09', '천장 입체 구조', ['GD47', 'GD50'], 'Fan ribs and muqarnas cells are different geometries, not one generic dense ceiling.'),
    ('GB10', '맥시멀리즘의 밀도/재료/계층', ['GD01', 'GD02', 'GD04'], 'Scope each effect to scene or surface; no fixed number of objects or candidates.'),
    ('GB11', '상징 정물/쇠락/용기', ['GD58', 'GD59', 'GD60', 'GD68'], 'Object set, material condition, religious context and adult tone need separate authorizations in request meaning.'),
    ('GB12', '기계 밀도와 형상 가독성', ['GD62', 'GD63', 'GD65', 'GD66'], 'Static mechanism shape, density and lighting are independent; no implied operation.'),
]

def disposition(unit, linked):
    n = unit.get('source_number')
    if n in DEFER_SPECIFIC:
        return 'CONTEXT_AND_FORM_OPTIONS_NOW; DEFER_NARROW_SUBGENRE_OR_PERIOD_PROFILE'
    if n in {26, 28, 29, 30, 98, 99, 108, 114}:
        return 'CONTEXT_ONLY_WITH_OPTIONAL_VISIBLE_DECOMPOSITION'
    if n in {72, 73, 124}:
        return 'MEDIUM_OR_PROCESS_CONTEXT; SELECTED_VISIBLE_FORM_ONLY'
    if linked and any(c['current_reuse_records'] for c in linked):
        return 'REUSE_OR_EXTEND_CURRENT_STABLE_IDENTITIES'
    if unit['kind'] in CONTEXT_KINDS:
        return 'ADVISORY_REALIZATION_FAMILY; NO_LABEL_ONLY_HARD_PROFILE'
    return 'REVIEW_CURRENT_OWNER_THEN_NEW_OR_EXTENDED_VISIBLE_ATOM'

def main():
    units = source_units()
    drafts = candidates(units)
    links = {u['id']: [c for c in drafts if u['id'] in c['unit_ids']] for u in units}
    evidence = read('EXISTING-COVERAGE.json')
    exact = {r['number']: r for r in evidence['rows']}
    mapping = []
    for u in units:
        row = exact.get(u.get('source_number'), {})
        mapping.append({
            'unit_id': u['id'], 'source_label': u['source_label'],
            'disposition': disposition(u, links[u['id']]),
            'candidate_draft_ids': [c['draft_id'] for c in links[u['id']]],
            'exact_positive_label_matches': row.get('exact_candidates', []),
            'lexical_leads_not_reviewed_reuse': row.get('lexical_candidates_for_review', []),
            'exact_profile_label_matches': row.get('exact_profiles', []),
            'dictionary_visual_semantics_leads': row.get('dictionary_visual_semantics_leads', []),
            'owner_route_review': u['suggested_route'],
            'new_profile_policy': u['hard_activation_plan'], 'status': 'PLANNED_NOT_IMPLEMENTED',
        })
    write('SEMANTIC-UNITS.json', {'status': STATUS, 'source_terms': 124, 'authoring_supplements': 20, 'units': units})
    write('CANDIDATE-DRAFTS.json', {'status': STATUS, 'warning': 'Do not load this file into the generator. Predicates, targets and property areas are authoring proposals, not validated runtime schema.', 'drafts': drafts})
    bundle_rows = [{'id': id, 'label_ko': label, 'member_draft_ids': ids, 'choice_policy': policy, 'status': STATUS, 'effects': 'Union every selected member effect; no partial selection under a falsely complete bundle.'} for id, label, ids, policy in BUNDLES]
    write('BUNDLE-DRAFTS.json', {'status': STATUS, 'bundles': bundle_rows})
    reuse = {(r['file'], r['slot'], r['id']): r for c in drafts for r in c['current_reuse_records']}
    profiles = read('AUTHORING-INVENTORY.json')['profile_catalog']
    reused_profiles = [p for p in profiles if p['id'] in {'pf_muqarnas', 'hw_brocade_raised_motifs', 'hw_damask_tonal_pattern', 'sff_pro_j06', 'sff_pro_j07'}]
    write('ADOPTION-MAP.json', {'status': 'PLANNED_NOT_IMPLEMENTED', 'current_head': read('CHECKOUT-SNAPSHOT.json')['head'], 'units': mapping, 'reviewed_reuse_candidates': list(reuse.values()), 'profile_id_leads_require_full_record_review': reused_profiles, 'boundary': 'Label equality and stored ID existence are not semantic coverage, current eligibility, exposure, adoption, prompt binding or pixels.'})
    counts = {'recovered_source_terms': 124, 'source_tail_truncated': True, 'authoring_supplements': 20, 'semantic_units': len(units), 'candidate_drafts': len(drafts), 'bundle_drafts': len(bundle_rows), 'source_records': len(read('SOURCES.json')['sources']), 'retrieved_sources': 60, 'inaccessible_follow_up_documents': 1, 'reviewed_reuse_candidate_identities': len(reuse), 'profile_identity_leads': len(reused_profiles), 'dispositions': dict(Counter(r['disposition'] for r in mapping)), 'runtime_adopted': False, 'native_images_generated': 0, 'native_pixel_evaluated': False}
    write('PACKAGE-COUNTS.json', counts)
    md = ['# 용어별 시각 의미와 혼동 경계', '', '**RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA**. 124개는 도구로 복원한 참조 대화의 용어다. GX01–GX20은 이번 연구의 보조 관계이며 원문 용어로 세지 않는다. 가시 구성은 출처를 바탕으로 연구자가 만든 선택형이다. 조합/양식의 목록 전체는 필수 조건이 아니다. 제작 과정·역사·정체성과 픽셀로 확인할 외형을 구분한다.', '']
    family = None
    for u in units:
        if u['owner_family'] != family:
            family = u['owner_family']
            md += [f'## {family}', '', '| ID / 용어 | 의미와 가시 구성 | 혼동 경계와 한계 | 근거 |', '|---|---|---|---|']
        source_links = ', '.join(f'[{id}](SOURCES.md)' for id in u['sources'])
        realization = '; '.join(u['observable_realization_en'])
        md.append(f"| {u['id']} **{clean(u['source_label'])}** | {clean(u['meaning_ko'])}<br>{clean(realization)} | {clean(u['confusion_boundaries'][0])}<br>{clean(u['claim_limits'][0])} | {source_links} |")
    (HERE / 'SEMANTIC-UNITS.md').write_text('\n'.join(md) + '\n')
    md = ['# 후보 초안과 반영 결정', '', f'**{len(drafts)}개 후보 초안**은 같은 구조를 재사용하기 위한 저작 단위다. 같은 수의 활성 ID를 자동으로 만들자는 뜻이 아니다. 모든 `target_binding`과 `proposed_property_area`는 현재 runtime의 dimension/target/property로 변환·검증해야 한다. 중립적인 물체와 인물에 착용한 장신구의 owner가 다르다.', '']
    for c in drafts:
        md += [f"## {c['draft_id']} {c['label_ko']}", '',
            f"의미 단위: {', '.join(c['unit_ids'])}. 제안 slot: `{c['proposed_slot']}`. 소유 바인딩: `{c['owner_binding']}`.", '',
            '**가시 관계:** ' + c['proposed_relations'][0]['predicate_description_en'] + '.', '',
            '**효과:** ' + '; '.join(f"{e['dimension']} / {e['target_binding']} / {e['proposed_property_area']}" for e in c['proposed_effects']) + '.', '',
            '**채택 조건:** ' + c['variant_exclusivity'] + '. ' + c['owner_review'], '',
            '**기존 ID 재사용 검토:** ' + (', '.join(f"`{r['file']}:{r['slot']}:{r['id']}`" for r in c['current_reuse_records']) or '확정 없음. 기존 소유 파일의 원자를 먼저 대조.') + '.', '',
            '**구별:** ' + ' / '.join(c['confusion_boundaries']), '',
            '**근거:** ' + ', '.join(f'[{s}](SOURCES.md)' for s in c['sources']) + '.', '']
    (HERE / 'CANDIDATE-DETAILS.md').write_text('\n'.join(md) + '\n')
    md = ['# 용어별 반영 상태', '', '모든 항목은 계획 상태다. 정확한 라벨 일치 수를 데이터 갭의 수나 runtime coverage로 쓰지 않는다.', '', '| 단위 | 반영 결정 | 후보 초안 |', '|---|---|---|']
    md += [f"| {r['unit_id']} {clean(r['source_label'])} | {r['disposition']} | {', '.join(r['candidate_draft_ids']) or '문맥/선택형 설명 유지; 고정 후보 추가 없음'} |" for r in mapping]
    (HERE / 'TERM-DISPOSITIONS.md').write_text('\n'.join(md) + '\n')
    print(json.dumps(counts, ensure_ascii=False))

if __name__ == '__main__':
    main()
