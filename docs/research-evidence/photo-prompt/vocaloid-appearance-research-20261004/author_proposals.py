"""Prepare reviewable candidate/profile proposals without installing them."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cards = {c['id']: c for c in json.loads((ROOT / 'KEYWORD-RESEARCH.json').read_text())['cards']}

# General visual forms; character names stay in provenance, never positive text.
specs = [
 ('K09', 'vr_short_rear_long_sidelocks', 'sca_short_rear_long_sidelocks', 'subculture_appearance'),
 ('K17', 'vr_cheek_surface_glyph', 'sca_cheek_surface_glyph', 'subculture_appearance'),
 ('K34', 'vr_crop_top_waist_hem', 'clothing_crop_top_waist_hem', 'clothing_structure'),
 ('K35', 'vr_abdominal_bounded_opening', 'clothing_abdominal_bounded_opening', 'clothing_structure'),
 ('K44', 'vr_attached_rear_costume_panel', 'costume_attached_rear_panel', 'costume_cosplay'),
 ('K51', 'vr_earpiece_mouth_boom', 'accessory_earpiece_mouth_boom', 'accessory_structure'),
 ('K52', 'vr_rigid_hair_tie_hardware', 'sca_rigid_hair_tie_hardware', 'subculture_appearance'),
 ('K53', 'vr_flat_equalizer_bars', 'sca_flat_equalizer_bars', 'subculture_appearance'),
 ('K54', 'vr_flat_keyboard_motif', 'sca_flat_keyboard_motif', 'subculture_appearance'),
 ('K55', 'vr_flat_control_panel_motif', 'sca_flat_control_panel_motif', 'subculture_appearance'),
 ('K56', 'vr_arm_circular_speaker_gear', 'accessory_arm_circular_speaker_gear', 'accessory_structure'),
 ('K61', 'vr_external_membrane_wings', 'costume_external_membrane_wings', 'costume_cosplay'),
 ('K62', 'vr_external_thin_wing_plates', 'costume_external_thin_wing_plates', 'costume_cosplay'),
 ('K68', 'vr_cap_cross_glyph', 'accessory_cap_cross_glyph', 'accessory_structure'),
]
proposals = []
for key, candidate_id, profile_id, family in specs:
    c = cards[key]
    units = [x['en'] for x in c['visible_components']]
    kr_units = [x['ko'] for x in c['visible_components']]
    if key == 'K62':
        units[1] = 'line motifs remain inside the outlines of those thin wing plates'
        kr_units[1] = '선무늬가 얇은 날개 판의 외곽 안에 놓인다'
    if key == 'K61':
        units.append('the external wing root joins a declared costume back support')
        kr_units.append('외부 날개 뿌리가 지정한 코스튬 등 지지부에 이어진다')
    entry = {
        'id': candidate_id, 'ko': ' · '.join(kr_units), 'en': '; '.join(units),
        'weight': 0.5, 'tags': ['human', 'observable_relation'], 'for_any': ['human'],
        'aliases': ['; '.join(kr_units)],
        'paraphrases': ['; '.join(kr_units), '; '.join(units)],
        'keywords': [*units, *kr_units],
        'embedding_text': ' '.join([*units, *kr_units]),
        'concept_units': units,
        'relations': [
            {'id': 'declared_owner', 'type': 'declared_owner_scope',
             'subject': c['owner'], 'object': 'main_subject'},
            *c['required_relations'],
        ],
        'affected_dimensions': ['appearance'],
        'affected_properties': [{k: c['proposed_effect'][k]
                                 for k in ['dimension', 'target', 'property']}],
        'core_assertion_discovery': True,
    }
    proposals.append({
        'research_card_id': key,
        'destination_candidate_file': f'photo_prompt_{family}_extension.json',
        'destination_profile_file': f'photo_prompt_visual_obligations_{family}.json',
        'entry': entry,
        'profile_binding_plan': {
            'proposed_profile_id': profile_id,
            'related_existing_profile_ids': [x['profile_id'] for x in c['existing_profile_crosswalk']],
            'binding_surface': 'visual_semantics[].hard_profile_ids after profile authoring and validation',
            'association_does_not_promote_hard_obligations': True,
            'mode': 'independent_component_request_evidence_only',
        },
        'blocked_until': [
            'Deduplicate against the then-current authored registry and preserve existing scope.',
            'Qualify the selected source variant and all required component relations.',
            'Bind owner/target/property to the frozen core and pass exclusion/open-property checks.',
            'Compile profile evidence and opt-in gates, then rebuild compatible indexes and measure retrieval.',
        ],
        'separate_material_scope': 'Transmission, gloss or emission needs a separately qualified material effect and an open material property. This appearance prototype does not change them.',
    })

candidate_doc = {'schema_version': 'vocaloid-candidate-proposals/v1',
                 'runtime_artifact': False, 'proposal_count': len(proposals),
                 'not_a_candidate_pack': 'These are ordinary source-entry proposals. A request-specific immutable photo-candidate-pack/v6 must be generated later from qualified runtime sources.',
                 'scope': '14 human/wearer-owned appearance prototypes only. Independent prop scope and adult body geometry are intentionally unresolved.',
                 'proposals': proposals}
(ROOT / 'CANDIDATE-PROTOTYPES.json').write_text(json.dumps(candidate_doc, ensure_ascii=False, indent=2) + '\n')

# Three complete authored-component examples, eligible for syntax compilation only.
profile_samples = []
for key in ['K09', 'K51', 'K53']:
    c = cards[key]
    p = next(p for p in proposals if p['research_card_id'] == key)
    entry = p['entry']
    owner_units = {
        'K09': ('the short rear hair and paired long face-side locks belong to the same hairstyle',
                '짧은 뒤머리와 두 긴 얼굴 옆 다발이 같은 모발 구조에 속한다'),
        'K51': ('the boom and mouth endpoint remain on the same wearer as the earpiece',
                '마이크 막대와 입 옆 끝점이 귀 장치를 쓴 같은 얼굴에 속한다'),
        'K53': ('all variable-height bars remain printed on one continuous garment panel',
                '높이가 다른 막대들이 같은 연속된 의복 패널에 인쇄되어 있다'),
    }
    units = [*entry['concept_units'], owner_units[key][0]]
    kr = [x['ko'] for x in c['visible_components']] + [owner_units[key][1]]
    profile_id = p['profile_binding_plan']['proposed_profile_id']
    carriers = ['hair', 'hairstyle', 'wig', '머리', '모발', '가발'] if key == 'K09' else (
        ['headset', 'earpiece', 'microphone', '헤드셋', '귀 장치', '마이크'] if key == 'K51' else
        ['garment', 'skirt', 'sleeve', 'fabric', '의복', '치마', '소매', '옷'])
    profile = {
        'id': profile_id, 'category': 'selected_local_appearance_relation',
        'activation': {
            'exact_terms': [entry['en'], entry['ko']],
            'requires_adult_character': False,
            'semantic_discovery_requires_component_evidence': True,
            'hard_activation': {'contract_version': 'photo-visual-hard-activation/v1',
                                'required_any_groups': [{'id': 'declared_carrier', 'any_terms': carriers}]},
        },
        'semantics': {
            'definition': '; '.join(units), 'paraphrase_examples': [entry['en'], '; '.join(kr)],
            'visual_components': units, 'contrast_examples': c['confusion_boundaries'],
            'claim_limits': [c['limits'], 'All requested components must coexist on the declared owner. Source artwork review does not prove prompt coverage or generated pixels.'],
        },
        'concept_candidate': {
            'concept_terms': [entry['en'], entry['ko'], *units],
            'core_assertion_discovery': True,
            'affected_dimensions': entry['affected_dimensions'],
            'affected_properties': entry['affected_properties'],
        },
        'runtime_expression': {'default_mode': 'definition_with_optional_label',
                               'prompt_label_terms': [], 'forbidden_prompt_terms': [],
                               'runtime_forbidden_labels': []},
        'authored_components': {
            'contract_version': 'photo-authored-visual-components/v1',
            'components': [
                {'id': f'component_{i}', 'match_terms': [unit, k],
                 'evidence_field': f'component_{i}_phrase', 'evidence_terms': [unit, k],
                 'min_content_words': 3,
                 'instruction': 'Keep this selected carrier relation explicit: ' + unit + '.',
                 'render_gate': {'id': f'vo_{profile_id}_{i}', 'review_scale': 'native',
                                 'description': unit + '. Inspect this relation on the selected same owner in original pixels. Partial evidence fails; an occluded required relation is unobservable.'}}
                for i, (unit, k) in enumerate(zip(units, kr), 1)
            ],
        },
        'reject_substitutes': c['confusion_boundaries'],
    }
    bundle = {
        'id': f'{entry["id"]}_bundle', 'primary_visual_proposition': entry['en'],
        'component_groups': [{'id': f'component_{i}', 'visible_evidence': [unit]}
                             for i, unit in enumerate(entry['concept_units'], 1)],
        'candidate_ids': [entry['id']], 'candidate_slots': {entry['id']: c['proposed_slot']},
        'hard_profile_ids': [profile_id], 'relations': entry['relations'],
        'confusion_boundaries': c['confusion_boundaries'], 'candidate_only': True,
        'activation_mode': 'independent_component_request_evidence_only',
        'source_keywords': [c['reference_term']],
    }
    profile_samples.append({'research_card_id': key, 'destination_file': p['destination_profile_file'],
                            'profile': profile, 'proposed_visual_semantics_bundle': bundle,
                            'qualification': 'syntax_example_only; not installed or render-qualified'})
(ROOT / 'PROFILE-PROTOTYPES.json').write_text(json.dumps({
    'schema_version': 'vocaloid-profile-proposals/v1', 'runtime_artifact': False,
    'proposal_count': 3, 'proposals': profile_samples}, ensure_ascii=False, indent=2) + '\n')

abstracts = [
 ('A01', '미래적인 가수 의상', ['귀 옆 장치의 형태와 부착', '몸판/소매의 실제 평면 패널', '요청한 경우만 자체 발광'], ['K51', 'K52', 'K53', 'K55'], '전자 무늬로 실제 기능·음향·전원을 도출하지 않는다.'),
 ('A02', '고딕한 의상', ['선택한 몸판 절개', '프릴/레이스의 carrier', '교차끈 접속', '선택한 색/길이'], ['K36', 'K38', 'K40', 'K41'], '검정 색이나 캐릭터명만으로 구성 전체를 강제하지 않는다.'),
 ('A03', '노출이 있는 의상', ['개방 부위', '상의-하의 간격인지 bounded cutout인지', '완성 테두리와 천 경로'], ['K24', 'K27', 'K30', 'K31', 'K34', 'K35'], '노출 정도·몸 비율·연령·성적 의미는 따로 확정한다. 같은 옷의 서로 배타적인 재단은 혼합하지 않는다.'),
 ('A04', '요염한 무대복', ['지정한 목선과 밑단 길이', '의복 윤곽', '선택한 광택 또는 색 대비'], ['K32', 'K33', 'K34', 'K42', 'K43'], '평가어에서 가슴/허리 확대·표정·성적 행동을 자동 도출하지 않는다. 원문 모듈명 Sexy는 provenance일 뿐이다.'),
 ('A05', '괴이하거나 불길한 외형', ['독립적으로 선택한 홍채/피부/모발 색', '가면의 위치', '비대칭 부속', '실제 봉제선'], ['K17', 'K25', 'K42', 'K67', 'K69'], '붉은 표식과 밝은 얼굴에서 상처·혈액·질병·위협 의도나 성격을 추론하지 않는다.'),
 ('A06', '인형 같은 외형', ['illustration/chibi/figure/human medium', '머리 비율의 명시 기준', '요청된 경우의 실제 관절/표면 seam'], ['K19', 'K67', 'K70'], '균일한 피부와 큰 머리를 로봇 관절·아동 연령·봉제 신체의 증거로 사용하지 않는다.'),
]
(ROOT / 'ABSTRACT-TERMS.json').write_text(json.dumps({
    'schema_version': 'vocaloid-abstract-term-boundaries/v1', 'runtime_artifact': False,
    'terms': [{'id': i, 'reference_term': t, 'needed_request_properties': ps,
               'related_card_ids': cs, 'limits': lim, 'automatic_geometry_activation': False}
              for i, t, ps, cs, lim in abstracts]}, ensure_ascii=False, indent=2) + '\n')

lead_specs = [
 ('L01', '묶임점의 단단한 머리 장치', 'C001', '각진 장치 → attached_to → 좌우 모발 묶임점', ['K01', 'K02', 'K52'], '머리 모양과 장치 carrier를 분리한다.'),
 ('L02', '짧은 후두부와 긴 옆머리 링', 'C019', '긴 두 sidelock → longer_than → 짧은 뒤머리', ['K09', 'K52'], '2011 제작자 3면 자료 X001–X003로 보완했다.'),
 ('L03', '소매 면의 작은 패널 도형', 'C001', '사각 패널 → printed_on → 분리 소매', ['K27', 'K55'], '소매 접속과 패널 표면은 별도 두 조건이다.'),
 ('L04', '치마 밑단의 건반형 열', 'C026', '짧은 어두운 칸 → offset_along → 긴 밝은 칸', ['K54'], '치마 프린트와 키보드 악기는 다른 owner다.'),
 ('L05', '치마 면의 픽셀 막대 열', 'C044', '다른 높이의 블록 열 → on → 같은 치마 면', ['K53'], '실시간 audio 기능은 추론하지 않는다.'),
 ('L06', '귀-입 마이크 연결', 'C003', '마이크 막대 → connected_to → 귀 장치', ['K51'], '손 마이크/헤드폰 단독을 대체로 쓰지 않는다.'),
 ('L07', '허리 양옆의 원형 장치', 'C019', '원형 장치 → attached_at → 의복 허리 양옆', ['K52', 'K57'], '후드·다리 장치와 연결 관계를 따로 기록한다. X003 참고.'),
 ('L08', 'canopy와 소매 띠의 다중 carrier', 'C034', 'canopy → behind → 몸통 / 띠 → connected_to → 소매', ['K58', 'K63'], '두 관계가 한 부품의 물리 연결을 뜻하지 않는다.'),
 ('L09', '몸 밖의 건반형 고리', 'C036', '건반형 열 → encircles_at_gap → 몸 바깥 허리 높이', ['K54', 'K58'], '공간형 그래픽이며 옷 프린트·실제 MIDI 장치로 합치지 않는다.'),
 ('L10', '뺨 별과 모자 십자의 carrier 차이', 'C044 C037', '별 → on → 뺨 / 십자 → on → 모자 앞면', ['K17', 'K68'], '도상의 소유자가 피부인지 의복인지 먼저 고정한다.'),
 ('L11', '착용자와 둥근 동료 로봇', 'C037', '둥근 별도 물체 → beside → 착용자', ['K58', 'K71'], '코드·등 장치를 별도 검사한다. 둥근 동료를 인물의 신체 부품으로 합치지 않는다.'),
 ('L12', '좌우 다른 다리 장식', 'C080', '다리 부속 A → on → 왼쪽 / 부속 B → on → 오른쪽', ['K42', 'K47'], '의복 비대칭과 몸 길이 차이를 구분한다. 정밀 원본 검토는 후속이다.'),
 ('L13', '꽃잎형 드레스 아래 패널', 'C086', '겹치는 끝 패널 → attached_to → 같은 치마 허리', ['K39', 'K42'], 'tier·tutu·생물 꽃잎을 자동 혼합하지 않는다. 추가 topology 후보.'),
 ('L14', '아이싱처럼 굴곡진 밑단', 'C081', '밝은 굴곡 띠 → borders → 지정 치마 밑단', ['K40', 'K42'], '실제 식용 재질이라는 해석은 제외한다. 새로운 모양 변형은 확대 근거를 확인한다.'),
 ('L15', '디저트 도상이 붙은 비스듬한 모자', 'C081', '롤/과일형 도상 → on → 모자 윗면', ['K64'], '모자 자체가 케이크로 변하는 것과 모자에 도상을 부착한 것을 구분한다.'),
 ('L16', '머리 옆 가면과 드러난 얼굴', 'C102', '가면 → offset_from → 얼굴 / 양 눈 → visible_on → 얼굴', ['K69'], '얼굴 전체 mask로 치환하지 않는다.'),
 ('L17', '새 머리처럼 읽히는 후드', 'C073', '부리형 후드 앞끝 → above → 착용자 이마', ['K64'], '후드 carrier를 유지하고 새 신체로 바꾸지 않는다. 현재는 contact-sheet 수준.'),
 ('L18', '종형 꽃과 잎의 머리/옷 부착', 'C070', '꽃/잎 장식 → attached_to → 지정 머리 또는 의복', ['K52', 'K57'], '실제 식물 몸 부속과 착용 장식의 범위를 구분한다. 현재는 coarse lead.'),
 ('L19', '열매 같은 둥근 단추', 'C070', '둥근 부속 → aligned_on → 몸판 여밈', ['K55', 'K57'], '인쇄 도형과 실제 raised fastener의 증거를 분리한다.'),
 ('L20', '별자리 선의 표면 carrier', 'C072', '점 연결 선 → printed_on → 지정 자락', ['K55', 'K41'], '배경 별자리나 실제 발광 회로로 넘기지 않는다. 투과는 별도 확인.'),
 ('L21', '손/몸과 금관형 소품', 'C075', '관형 소품 → held_by → 지정 손', [], '독립 prop의 owner/효과 범위가 선행한다. 음향 기능·연주 동작을 자동 추가하지 않는다.'),
 ('L22', '모자 앞의 시계형 도상', 'C076', '눈금/바늘 도상 → on → 모자 면', ['K55', 'K64'], '실제 시계 기구인지 표면 도형인지 추가 증거가 필요하다.'),
 ('L23', '다면체 왕관의 머리 부착', 'C080', '다면체 첨두 → arranged_on → 머리 왕관 carrier', ['K57'], '결정 형태·투명도·얼음이라는 재질 의미를 각각 검사한다.'),
 ('L24', '접힘에서 드러나는 다른 색 안감', 'C061 C019', '안감 색 → beneath → 같은 겉옷 층', [], '부속의 보라색·분홍색 면을 다른 피부/모발 색으로 옮기지 않는다. 겉-안쪽의 가림을 확인한다.'),
]
case_map = {c['case_id']: c for c in json.loads((ROOT / 'SOURCE-RECEIPTS.json').read_text())['cases']}
leads = [{'id': i, 'relation_label': label,
          'source_cases': [{'case_id': x, 'url': case_map[x]['url']} for x in seeds.split()],
          'directed_relation_proposal': relation, 'related_keyword_card_ids': related,
          'limits': limits, 'qualification': 'design relation lead; source-specific detail needs per-component qualification'}
         for i, label, seeds, relation, related, limits in lead_specs]
(ROOT / 'DESIGN-RELATION-LEADS.json').write_text(json.dumps({
    'schema_version': 'vocaloid-design-relation-leads/v1', 'runtime_artifact': False,
    'lead_count': len(leads), 'leads': leads}, ensure_ascii=False, indent=2) + '\n')
lines = ['# 판본·행사 의상에서 얻은 추가 관계 24개', '',
         '원문 용어 72개 외에 부품의 배치·연결·표면 carrier를 보강할 연구 lead다. 새로운 프로파일 24개를 자동 추가하는 목록이 아니며 coarse 자료의 미세 관계는 후속 일차 자료 검토가 필요하다.', '',
         '|ID|추가 관계|방향과 소유|관련 카드|범위·다음 확인|', '|---|---|---|---|---|']
for x in leads:
    ref = ', '.join(f"[{s['case_id']}]({s['url']})" for s in x['source_cases'])
    lines.append(f"|{x['id']} {ref}|{x['relation_label']}|{x['directed_relation_proposal']}|{' '.join(x['related_keyword_card_ids']) or '독립 범위 확인'}|{x['limits']}|")
(ROOT / 'DESIGN-RELATION-LEADS.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'candidate_proposals': 14, 'profile_examples': 3, 'abstract_boundaries': 6,
                  'additional_relation_leads': 24}))
