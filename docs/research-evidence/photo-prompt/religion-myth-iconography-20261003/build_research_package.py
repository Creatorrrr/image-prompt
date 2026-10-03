#!/usr/bin/env python3
"""Build and validate a research package. No runtime writes, network or image calls."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'skills/photo-prompt-image-generator').is_dir())
PHOTO = ROOT / 'skills/photo-prompt-image-generator'


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def normalize(s):
    return ' '.join(unicodedata.normalize('NFKC', s).casefold().split())


def reference_terms(row):
    terms = re.split(r' — | / |·', row['label'])
    return list(dict.fromkeys(t.strip() for t in terms if len(t.strip()) >= 2))


def live_audit(rows):
    sys.path.insert(0, str(PHOTO / 'scripts'))
    import prompt_generator as pg
    asset_names = {'photo_prompt_tags.json', 'photo_prompt_visual_obligations.json',
                   'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'}
    asset_names.update(pg.RESEARCH_EXTENSION_FILENAMES)
    asset_names.update(pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES)
    dependencies = [PHOTO / 'assets' / n for n in sorted(asset_names)]
    dependencies += [PHOTO / 'scripts' / n for n in
                     ('prompt_generator.py', 'photo_candidate_semantics.py', 'photo_contracts.py')]
    dependencies = [p for p in dependencies if p.is_file()]
    before = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    head_before = git('rev-parse', 'HEAD')
    tags = pg.load_json(PHOTO / 'assets/photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(PHOTO / 'assets/photo_prompt_visual_obligations.json')
    records = []
    for slot, entries in tags['slots'].items():
        for entry in entries:
            positive = [entry.get('ko', ''), entry.get('en', '')]
            for key in ('aliases', 'paraphrases', 'keywords'):
                positive.extend(entry.get(key, []))
            records.append((slot, entry['id'], [normalize(v) for v in positive if isinstance(v, str)]))
    mention_audit = []
    for row in rows:
        terms = reference_terms(row)
        patterns = [(term, re.compile(r'(?<!\w)' + re.escape(normalize(term)) + r'(?!\w)')) for term in terms]
        found = []
        for slot, candidate_id, fields in records:
            matches = [term for term, pat in patterns if any(pat.search(v) for v in fields)]
            if matches:
                found.append({'slot': slot, 'candidate_id': candidate_id, 'matched_terms': matches})
        mention_audit.append({'row_id': row['row_id'], 'queried_terms': terms,
                              'mention_count': len(found), 'examples': found[:4],
                              'meaning': 'LEXICAL_LEAD_ONLY_NOT_SEMANTIC_COVERAGE'})
    extensions = []
    for name in ('mythology', 'legend'):
        file = PHOTO / f'assets/photo_prompt_{name}_extension.json'
        data = json.loads(file.read_text())
        extensions.append({'path': str(file.relative_to(ROOT)), 'sha256': digest(file),
                           'semantic_ids': [r['id'] for r in data['visual_semantics']],
                           'candidate_count': sum(len(v) for v in data['slots'].values()),
                           'slots': {s: len(v) for s, v in data['slots'].items()}})
    selected = []
    for p in registry['profiles']:
        if p['id'] in {'egyptian_heart_weighing_judgment', 'katabasis_living_underworld_descent',
                       'moirai_fate_thread_life_allocation', 'axis_mundi_three_realm_connection'}:
            selected.append({'profile_id': p['id'], 'activation': p.get('activation'),
                             'semantics': p.get('semantics'),
                             'reuse_limit': 'Preserve existing ID and required groups. A different mechanism needs a distinct variant.'})
    after = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    head_after = git('rev-parse', 'HEAD')
    audit = {'schema_version': 'religion-myth-live-readonly-audit/v1',
             'captured_at_utc': datetime.now(timezone.utc).isoformat(),
             'runtime_load': 'PASS', 'git_head_before': head_before, 'git_head_after': head_after,
             'git_branch': git('branch', '--show-current'),
             'input_stable_during_read': before == after and head_before == head_after,
             'slot_count': len(tags['slots']), 'candidate_count': len(records),
             'profile_count': len(registry['profiles']),
             'slot_policy': tags['candidate_semantic_policy'],
             'extension_summary': extensions, 'selected_existing_profiles': selected,
             'lexical_mention_audit': mention_audit, 'protected_input_sha256': after,
             'outside_research_status_at_capture': [l for l in git('status', '--short').splitlines()
                  if 'religion-myth-iconography-20261003/' not in l],
             'verification_boundary': 'Read-only loader and lexical leads. No bundle exposure, runtime selection or native pixels tested.'}
    return audit


PAIRS = [
    ('head_halo', 'body_mandorla', 'different_spatial_scope'),
    ('buddhapada', 'empty_throne', 'related_distinct_symbols'),
    ('vajra_bell_pair', 'five_prong_bell', 'general_specific_not_alias'),
    ('kartika_shape', 'khatvanga_owner', 'different_object_and_contact'),
    ('chakra_blue12', 'chakra_white2', 'exclusive_selected_variant'),
    ('chakra_blue12', 'hevajra_eight16', 'different_deity_and_arity'),
    ('vajravarahi_red', 'chakra_white2', 'actor_vs_union_scene'),
    ('mandala_foundation', 'sri_yantra_graph', 'same_triangle_vocabulary_different_topology'),
    ('sri_yantra_graph', 'generic_yantra', 'named_graph_vs_broader_class'),
    ('nataraja_chola', 'durga_eight', 'shared_trampling_different_owner'),
    ('durga_eight', 'durga_four', 'exclusive_selected_variant'),
    ('ardhana_cambodia', 'rebis_two_heads', 'different_body_connection'),
    ('rebis_two_heads', 'rebis_three_legs', 'distinct_source_variant'),
    ('mithuna_couple', 'maithuna_boundary', 'couple_vs_event_category'),
    ('jina_kayotsarga', 'mithuna_couple', 'nudity_does_not_establish_union'),
    ('hodegetria_pointing', 'eleousa_contact', 'different_decisive_contact'),
    ('virgin_hybrid_variant', 'hodegetria_pointing', 'documented_hybrid_not_global_exclusion'),
    ('pieta_support', 'dormition_soul', 'body_support_vs_soul_symbol'),
    ('lucy_plate_eyes', 'arm_reliquary', 'attribute_vs_container'),
    ('bartholomew_knife', 'chinnamasta_streams', 'attribute_does_not_establish_mutilation'),
    ('daoist_robe_xuanwu', 'tsukumogami_object_body', 'depicted_motif_vs_animated_anatomy'),
    ('jangseung_face_post', 'sotdae_three_birds', 'face_post_vs_bird_pole'),
    ('heart_ani_roles', 'heart_maat_figure', 'existing_feather_rule_vs_new_figure_variant'),
    ('siren_human_bird', 'sphinx_greek', 'bird_body_vs_lion_body'),
    ('sphinx_greek', 'griffin_eagle_lion', 'human_head_vs_eagle_head'),
    ('buraq_golconda', 'sleipnir_eight_legs', 'composite_surface_vs_leg_arity'),
    ('nkisi_container_scope', 'mangaaka_nkondi', 'class_vs_specific_nail_form'),
    ('drapo_material', 'gede_distinct_name', 'artifact_class_vs_dedication'),
    ('sheela_interpretation', 'dilukai_gable', 'similar_exposure_different_provenance'),
    ('volvelle_layers', 'ripley_static_wheel', 'movable_layers_vs_single_print'),
    ('chinnamasta_streams', 'ballgame_sacrifice_limit', 'self_action_vs_other_sacrificial_event'),
    ('babayaga_hut', 'babayaga_mortar', 'setting_support_vs_transport_vessel'),
    ('danae_gold', 'leda_swan', 'different_transformed_agent'),
    ('persephone_abduction', 'mithuna_couple', 'abduction_vs_loving_embrace'),
    ('centaur_rimmer_form', 'centaur_nessos_human_knees', 'modern_form_vs_early_human_leg_variant'),
    ('centaur_rimmer_form', 'centaur_pholos_horse_chest', 'human_abdomen_vs_equine_chest'),
    ('minotaur_bull_head', 'centaur_rimmer_form', 'bull_head_vs_horse_lower_body'),
    ('naga_seven_hood', 'naga_handle_five', 'heads_of_one_serpent_vs_five_deity_bodies'),
    ('thor_hammer_ring', 'peter_keys', 'owned_emblem_different_named_role'),
]

SPECIFIC_CASES = [
    ('durga_unspecified', '두르가라는 이름만 있는 frozen core', 'Do not hard-fix four/eight/ten arms without a selected form.'),
    ('chakra_unspecified', '얍윰이라고만 명시한 요청', 'Do not instantiate Chakrasamvara, Hevajra or specific consort/count from retrieval.'),
    ('nataraja_mirror', '나타라자 사진의 좌우가 반전된 경우', 'Distinguish actor-relative hands from screen coordinates; compare selected original.'),
    ('sikh_identity_lock', '참조 얼굴 유지, 다스타르만 추가', 'No inferred real-world religion, ethnicity or biography in identity.'),
    ('temple_mithuna_event_lock', '성교 없는 포옹형 사원 미투나 부조', 'No added intercourse or fetish styling; preserve stated event.'),
    ('digambara_tone_lock', '금욕적 디감바라상, 절제된 박물관 촬영', 'Do not turn nudity into a sexual event or sensual styling.'),
    ('persephone_event_lock', '페르세포네 납치 재현', 'Do not replace abduction with a romance or invent consent/desire.'),
    ('heart_maat_conflict', '그린필드형 저울 반대편에 앉은 마아트상', 'Feather-only parent profile must not silently replace the requested counterweight.'),
    ('hanukkiah_count', '여덟 심지 받침과 샤마시 주전자', 'Count receptacles independently of branches and burning flames.'),
    ('sleipnir_occlusion', '여섯 다리만 보이고 두 다리는 가려짐', 'Required eight-leg gate is UNOBSERVABLE, not PASS.'),
    ('hevajra_owner_swap', '손 수는 맞지만 잔 일부가 배우자에게 붙음', 'Fail the one-cup-per-owned-hand relation.'),
    ('kapala_material', '해골잔 외형은 보이지만 재료 기록 없음', 'Do not certify human-bone provenance from pixels.'),
    ('diagram_text', '세피로트 노드 수는 맞지만 이름·연결이 틀림', 'Fail the curated diagram; visual node count alone is insufficient.'),
    ('volvelle_static', '인쇄된 리플리 바퀴만 보임', 'Do not count printed concentric bands as movable layers.'),
    ('rider_exclusion', '골콘다 무탑승자 부라크, 새 인물 추가 금지', 'Preserve subject/count exclusions; do not add a rider.'),
    ('prop_unknown_scope', 'prop 슬롯의 affected_dimensions가 빈 현재 정책', 'Hold semantic adoption until a real owner/dimension/property exists.'),
    ('retrieval_pollution', '출처 설명에 부정 예시·다른 전통 명칭이 많음', 'No source prose, rejected terms or context interpretations in retrieval projection.'),
    ('optional_all_reject', 'frozen core가 모든 조사 후보와 충돌', 'Return no adopted bundle; keep discovery advisory and core unchanged.'),
]


def build(audit):
    rows = read('REFERENCE-KEYWORDS.json')['rows']
    seeds = read('UNIT-SEEDS.json')['units'] + read('SUPPLEMENT-UNIT-SEEDS.json')['units']
    sources = {s['source_id']: s for s in read('SOURCES.json')['sources']}
    slot_policy = audit['slot_policy']['slot_dimensions']
    units, drafts, regressions, pixels = [], [], [], []
    effect_properties = {'composition': 'composition.iconographic_relations',
                         'location': 'setting.architectural_relations',
                         'action': 'actions.iconographic_contact',
                         'relational_action': 'actions.inter_actor_contact',
                         'anatomical_connection': 'body.connections',
                         'body_orientation': 'pose.orientation',
                         'garment_detail': 'wardrobe.details',
                         'wearable_accessory': 'wardrobe.accessories',
                         'costume_style': 'wardrobe.form',
                         'surface_material': 'surface.material_appearance'}
    for seed in seeds:
        uid = seed['unit_id']
        component_ids = [f'{uid}_c{i+1}' for i in range(len(seed['observable_components']))]
        unit = dict(seed)
        unit['reference_rows'] = [f'ref_{n:03}' for n in seed['reference_rows']]
        unit['components'] = [{'component_id': cid, 'observable_statement': statement,
                               'basis': 'TEXT_BASED_CHECK_PROPOSAL_NOT_REFERENCE_PIXEL_AUDIT'}
                              for cid, statement in zip(component_ids, seed['observable_components'])]
        unit['relations'] = [dict(rel, relation_id=f'{uid}_r{i+1}',
                                 owner_binding_status='RESEARCH_ENTITY_NOT_FROZEN_CORE_TARGET')
                             for i, rel in enumerate(seed['relations'])]
        unit['activation_plan'] = {
            'authority': 'FROZEN_CORE_AND_REQUEST_DERIVED_EXACT_CONTEXT_ONLY',
            'candidate_discovery': 'BM25F_OR_EMBEDDING_ADVISORY_ONLY',
            'unqualified_name': 'DO_NOT_FORCE_ONE_VARIANT',
            'source_prose': 'PROVENANCE_ONLY_NOT_ACTIVATION_OR_RETRIEVAL',
            'conditions': ['Resolve representation mode and selected variant.',
                           'Bind named actors/objects to actual core targets.',
                           'Respect negation, exclusions, locks and existing required meanings.']}
        unit['context_limit'] = 'Faith, identity, efficacy, consent, desire, function or hidden contents are not certified by appearance.'
        unit['non_pixel_claims'] = seed.get('non_pixel_claims', [])
        unit['source_review_remaining'] = ['Examine the specific reference image and its rights before active adoption.',
                                          'Confirm all detailed components against that exact variant.']
        unit['runtime_status'] = 'NOT_INTEGRATED'
        unit['existing_owner_plan'] = ({'decision': 'REUSE_SPECIFIC_EXISTING_OWNER',
                  'profile_id': 'egyptian_heart_weighing_judgment'} if uid == 'heart_ani_roles' else
            {'decision': 'NEW_VARIANT_REVIEW_REQUIRED_DO_NOT_BROADEN_FEATHER_OWNER',
             'proposed_profile_id': 'egyptian_heart_weighing_maat_figure',
             'related_existing_profile': 'egyptian_heart_weighing_judgment'} if uid == 'heart_maat_figure' else
            {'decision': 'COMPARE_CURRENT_AUTHORED_OWNERS_BEFORE_ADDING'})
        units.append(unit)
        if seed['slot_hint'] == 'context_only':
            continue
        slot = seed['slot_hint']
        dimensions = slot_policy[slot]
        held_sources = [s for s in seed['source_ids'] if sources[s]['access_status'] != 'PAGE_TEXT_RETURNED']
        reasons = ['Bind actual frozen-core target and property; proposed paths are not existing runtime owner declarations.',
                   'Decompose multi-dimension observations before constructing slot-owned candidate members.',
                   'Review selected reference image; no native qualification has been run.']
        if not dimensions:
            reasons.insert(0, 'HOLD_UNKNOWN_SLOT_SCOPE: prop currently has no semantic dimension owner. Do not invent a prop dimension or reroute through style.')
        if held_sources or seed['evidence_level'] != 'CURATORIAL_DESCRIPTION':
            reasons.append('HOLD_SOURCE_OR_VARIANT_EVIDENCE: complete the explicitly listed text/diagram/variant checks.')
        draft_id = f'research_{uid}'
        effects = [{'dimension': d, 'target_binding': '<bind_actual_frozen_core_target>',
                    'property_path_draft': effect_properties.get(slot, '<owner_mapping_required>') + '.' + uid,
                    'status': 'PROPOSED_PATH_NOT_CONFIRMED_RUNTIME_PROPERTY'} for d in dimensions]
        drafts.append({'draft_id': draft_id, 'unit_id': uid, 'status': 'PROPOSED_NOT_INTEGRATED',
                       'slot_hint': slot, 'label_ko': seed['title'], 'observation_text_en': seed['description_en'],
                       'positive_discovery_terms_draft': [seed['title']],
                       'affected_dimensions_hint': dimensions, 'affected_properties_draft': effects,
                       'not_a_complete_runtime_payload': True, 'owner_mapping_status': 'HOLD_FOR_AUTHORED_TRANSLATION',
                       'hold_reasons': reasons, 'source_review_pending_ids': held_sources,
                       'optional': True, 'hard_profile_activation_from_selection': False,
                       'source_ids': seed['source_ids'], 'all_of_observation_component_ids': component_ids,
                       'priority_batch': seed['phase']})
        regressions += [
            {'case_id': f'{uid}_positive', 'unit_ids': [uid], 'status': 'PROPOSED_NOT_RUN',
             'layer': 'REQUEST_CORE_DATA_AND_PACK',
             'request_fixture': seed['title'] + ' / ' + seed['variant_scope'],
             'required_core_evidence': seed['observable_components'],
             'expectations': ['Discovery may expose an optional draft.', 'No adoption until all owner, scope, lock and exclusion checks pass.',
                              'Exact obligation requires request-derived variant evidence; retrieval alone cannot activate it.']},
            {'case_id': f'{uid}_negated', 'unit_ids': [uid], 'status': 'PROPOSED_NOT_RUN',
             'layer': 'ACTIVATION_EXCLUSIONS', 'request_fixture': seed['title'] + '은 넣지 않는다.',
             'expectations': ['No negated obligation or incompatible candidate adopted.', seed['confusion_boundaries'][0]]},
            {'case_id': f'{uid}_owner_lock', 'unit_ids': [uid], 'status': 'PROPOSED_NOT_RUN',
             'layer': 'SLOT_OWNERSHIP_AND_LOCK', 'research_relation_fixture': seed['relations'],
             'mutation_fixture': 'Lock this target property; then attempt ownership swap or candidate addition.',
             'expectations': ['Reject the mutation; core targets and source-owned property locks remain unchanged.']},
        ]
        pixels.append({'pixel_case_id': f'{uid}_native', 'unit_id': uid, 'status': 'NOT_RUN',
                       'gate_mode': 'ALL_OF', 'partial_is_fail': True,
                       'required_component_ids': component_ids,
                       'required_relation_ids': [r['relation_id'] for r in unit['relations']],
                       'source_variant_confirmation': 'REQUIRED_BEFORE_GENERATION',
                       'allowed_decisions': ['PASS', 'FAIL', 'UNOBSERVABLE'],
                       'occluded_required_evidence': 'UNOBSERVABLE_NOT_PASS',
                       'review_scale': ['whole_original_image', 'native_resolution_component_crop'],
                       'claim_limit': 'No pixel inference of hidden contents, real identity, historical efficacy or actual motion.'})
    pairs = [{'pair_id': f'pair_{i+1:03}', 'unit_a': a, 'unit_b': b, 'relation_type': rel,
              'status': 'RESEARCH_RELATION_NOT_RUNTIME_ALIAS',
              'rule': 'Do not merge aliases, owners or obligations; allow documented hybrids and explicitly combined requests.'}
             for i, (a, b, rel) in enumerate(PAIRS)]
    regressions += [{'case_id': p['pair_id'], 'unit_ids': [p['unit_a'], p['unit_b']],
                     'status': 'PROPOSED_NOT_RUN', 'layer': 'CONFUSION_BOUNDARY',
                     'request_fixture': 'Explicitly select unit_a; present a neighboring unit_b retrieval hit.',
                     'expectations': [p['relation_type'], p['rule']]} for p in pairs]
    regressions += [{'case_id': key, 'unit_ids': [], 'status': 'PROPOSED_NOT_RUN',
                     'layer': 'CROSS_CUTTING_CONTRACT', 'request_fixture': request,
                     'expectations': [expected]} for key, request, expected in SPECIFIC_CASES]
    mapped = {}
    for unit in units:
        for ref in unit['reference_rows']:
            mapped.setdefault(ref, []).append(unit)
    mentions = {m['row_id']: m for m in audit['lexical_mention_audit']}
    decisions = []
    for row in rows:
        linked = mapped.get(row['row_id'], [])
        detailed = [u for u in linked if u['slot_hint'] != 'context_only']
        status = 'DRAFTED_VARIANT_WITH_EVIDENCE_GATES' if detailed else 'CONTEXT_ONLY_OBJECT_RESEARCH_PENDING' if linked else 'FOLLOWUP_SOURCE_RESEARCH_REQUIRED'
        decisions.append({'row_id': row['row_id'], 'label': row['label'], 'section': row['section'],
                          'decision': status, 'linked_unit_ids': [u['unit_id'] for u in linked],
                          'linked_source_ids': sorted({s for u in linked for s in u['source_ids']}),
                          'live_lexical_leads': mentions[row['row_id']],
                          'reference_description_status': 'LEAD_NOT_INDEPENDENTLY_VERIFIED',
                          'duplicate_index_handling': 'Link to semantic owner/variant; do not create a duplicate entry.' if row['section'] in (22,23) else 'Preserve original row identity.',
                          'remaining_research': ['Find two dated regional examples and authoritative object descriptions.',
                              'Confirm diagnostic components, owned attributes, relations and nearby confusions.',
                              'Separate source interpretation from visible evidence.'] if not detailed else
                              ['Complete source-image review and runtime target mapping for each linked variant.']})
    write('SEMANTIC-UNITS.json', {'schema_version': 'religion-myth-semantic-research/v1', 'status': 'RESEARCH_ONLY', 'units': units})
    write('CANDIDATE-DRAFTS.json', {'schema_version': 'religion-myth-candidate-research-drafts/v1', 'runtime_schema': False, 'drafts': drafts})
    write('VARIANT-RELATIONS.json', {'schema_version': 'religion-myth-variant-research/v1', 'pairs': pairs})
    write('TERM-DECISIONS.json', {'schema_version': 'religion-myth-term-research-decisions/v1', 'decisions': decisions})
    write('REGRESSION-PROPOSALS.json', {'schema_version': 'religion-myth-regression-proposals/v1', 'status': 'PROPOSED_NOT_RUN', 'cases': regressions})
    write('PIXEL-GATES.json', {'schema_version': 'religion-myth-native-pixel-proposals/v1', 'status': 'NOT_RUN', 'cases': pixels})
    catalog_lines = ['# 종교·신화 도상 상세 카탈로그', '',
        f'{len(units)}개 연구 단위의 관찰 제안이다. 모든 관계는 연구 엔티티이며 실제 frozen core target 바인딩 전에는 운영 의무나 채택 후보가 아니다.', '',
        '원본 도판의 픽셀 검토와 새 이미지 생성은 수행하지 않았다. 출처의 해석·서사와 아래의 가시성 검증 제안을 구별한다.', '']
    for unit in units:
        catalog_lines += ['## ' + unit['unit_id'] + ' — ' + unit['title'], '',
            '- 범위: ' + unit['variant_scope'],
            '- 근거 단계: `' + unit['evidence_level'] + '`; 직접 원본 도판 대조 미실행.',
            '- 관찰 요소: ' + '; '.join(unit['observable_components']),
            '- 비시각적 맥락: ' + ('; '.join(unit['non_pixel_claims']) or '정체·효능·해석은 픽셀 판정에서 분리한다.'),
            '- 소유·관계: ' + '; '.join(r['subject'] + ' → ' + r['type'] + ' → ' + r['object'] for r in unit['relations']),
            '- 혼동 경계: ' + '; '.join(unit['confusion_boundaries']),
            '- 후보 위치: `' + unit['slot_hint'] + '`; ' + ('맥락만, 후보 없음.' if unit['slot_hint']=='context_only' else '운영 번역·소유권 검토 전 채택 보류.'),
            '- 출처: ' + ', '.join('[' + sources[s]['title'].replace('[','').replace(']','') + '](' + sources[s]['url'] + ')' for s in unit['source_ids']), '']
    (HERE / 'CATALOG.md').write_text('\n'.join(catalog_lines) + '\n')
    counts = {'reference_rows': len(rows), 'semantic_units': len(units), 'candidate_drafts': len(drafts),
              'context_only_units': len(units)-len(drafts), 'variant_pairs': len(pairs),
              'regression_proposals': len(regressions), 'pixel_proposals': len(pixels),
              'sources': len(sources), 'source_access': dict(Counter(s['access_status'] for s in sources.values())),
              'term_decisions': dict(Counter(d['decision'] for d in decisions)),
              'drafts_by_slot': dict(Counter(d['slot_hint'] for d in drafts)),
              'drafts_by_phase': dict(Counter(d['priority_batch'] for d in drafts)),
              'unknown_scope_holds': sum(not d['affected_dimensions_hint'] for d in drafts)}
    return counts


def build_execution_and_followup():
    """Map all drafts to bounded research batches and all pending rows to questions."""
    rows = read('REFERENCE-KEYWORDS.json')['rows']
    units = {u['unit_id']: u for u in read('SEMANTIC-UNITS.json')['units']}
    sources = {s['source_id']: s for s in read('SOURCES.json')['sources']}
    drafts = read('CANDIDATE-DRAFTS.json')['drafts']
    decisions = read('TERM-DECISIONS.json')['decisions']
    by_row = {r['row_id']: r for r in rows}
    families = {
        1: 'COMMON', 2: 'BUDDHIST', 3: 'TANTRIC', 4: 'HINDU',
        5: 'JAIN_SIKH', 6: 'CHRISTIAN', 7: 'JEWISH', 8: 'ISLAM_PERSIAN',
        9: 'DAOIST', 10: 'KOREAN', 11: 'JAPANESE', 12: 'EGYPTIAN',
        13: 'MESOPOTAMIAN', 14: 'IRANIAN', 15: 'GRECO_ROMAN',
        16: 'NORSE', 17: 'EUROPEAN_FOLK', 18: 'AFRICAN_DIASPORA',
        19: 'MESOAMERICAN', 20: 'PACIFIC_SOUTHEAST_ASIA', 21: 'ALCHEMY',
        22: 'COMPARATIVE', 23: 'COMPARATIVE',
    }
    groups = {}
    for d in drafts:
        section = min(by_row[r]['section'] for r in units[d['unit_id']]['reference_rows'])
        groups.setdefault((d['priority_batch'], families[section]), []).append(d)
    batches = []
    for (phase, family), members in sorted(groups.items()):
        for start in range(0, len(members), 8):
            part = members[start:start+8]
            batches.append({
                'batch_id': f'{phase}_{family.lower()}_{start//8+1:02}',
                'phase': phase, 'family': family, 'status': 'PROPOSED_NOT_RUN',
                'unit_ids': [d['unit_id'] for d in part],
                'draft_ids': [d['draft_id'] for d in part],
                'source_ids': sorted({sid for d in part for sid in d['source_ids']}),
                'unknown_prop_scope_holds': [d['unit_id'] for d in part if not d['affected_dimensions_hint']],
                'source_access_holds': sorted({sid for d in part for sid in d['source_ids']
                                              if sources[sid]['access_status'] != 'PAGE_TEXT_RETURNED'}),
                'all_unit_prerequisites': ['D0_SOURCE_IMAGE_AND_VARIANT_REVIEW',
                    'D1_EXISTING_OWNER_COMPARISON', 'D2_ACTUAL_TARGET_PROPERTY_BINDING'],
                'execution_order': ['authored_translation', 'focused_contract_regressions',
                    'derived_indexes', 'same_frozen_core_pack_check', 'native_all_of_qualification'],
                'completion_rule': 'Each unit must satisfy its own source, owner and scope gates; phase does not override HOLD.',
            })
    write('BATCH-PLAN.json', {
        'schema_version': 'religion-myth-research-execution-plan/v1',
        'runtime_schema': False, 'status': 'PROPOSED_NOT_RUN',
        'maximum_research_units_per_batch': 8,
        'not_runtime_bundle_limit': True, 'candidate_draft_count': len(drafts),
        'batch_count': len(batches), 'batches': batches,
    })

    # These are research questions, not factual assertions about unexamined works.
    questions = {
        '열반상': '횡와한 불상, 제자·침상·나무의 배치가 지역별로 어떻게 다른가? 수면상과 구별하는 근거는 무엇인가?',
        '본생담': '한 패널의 등장 개체와 동일 주인공의 반복 표상을 어떻게 구별하는가? 어떤 본생 이야기·사건 단계인가?',
        '문수보살': '검·경전·좌대·탈것을 가진 실제 지역별 작품에서 손과 지물의 관계가 어떻게 다른가?',
        '미륵': '좌정·의좌·보관·지물이 다른 변형과 동아시아 포대 표상을 어떤 근거로 분리하는가?',
        '타라': '색·자세·발 위치·연꽃 소유가 명시된 백색/녹색 변형 두 작품을 어떻게 구별하는가?',
        '비사문천': '갑옷·탑·무기·탈것의 지역별 변형을 어떻게 구별하며 지국천 등 이웃 사천왕과 무엇이 다른가?',
        '진언': '정확한 언어·문자·종자자와 방향·위치를 어떻게 전사하는가? 장식적 유사 글자와 구별 가능한가?',
        '금강지': '손 교차·금강저·방울의 위치가 실제 작품에서 어떻게 다른가? 이름만으로 결합상을 요구할 수 있는가?',
        '골장신구': '공개 소장품에서 장신구와 앞치마의 구성·결합·착용 주체를 어떻게 확인하는가?',
        '시체림': '특정 만다라의 외곽 공간과 장면의 개체·단계는 무엇인가? 수행 해석과 가시 요소를 어떻게 분리하는가?',
        '비슈누': '손별 소라·원반·곤봉·연꽃, 탈것·아바타가 자료에 어떻게 명시되어 있으며 어떤 변형을 분리해야 하는가?',
        '하누만': '원숭이 머리·몸, 산 또는 곤봉, 무릎 자세가 어느 사건·작품에 속하는가? 일반 원숭이와 구별점은 무엇인가?',
        '크리슈나': '피리·손·자세·소·동반자의 관계가 어떤 변형에 속하는가? 유아·목동·전사 변형을 어떻게 분리하는가?',
        '칼리': '혀·손·목걸이·발밑 대상·팔 수가 명시된 지역별 두 작품에서 실제 진단 요소는 무엇인가?',
        '차문다': '야윈 신체·좌대·지물의 작품별 차이를 칼리·두르가와 구별하는 데 어떤 근거가 필요한가?',
        '바이라바': '지물·개·표현된 신체의 유형을 시바 일반형·분노존과 어떻게 구별하는가?',
        '바라히': '멧돼지 얼굴 인간형 몸과 작은 별도 멧돼지 머리형의 차이를 어떤 작품이 직접 보여 주는가?',
        '약샤': '성별 명칭·수호·풍요 해석을 외형과 분리할 때 자세·나무·공간 관계에서 무엇을 확인할 수 있는가?',
        '링가': '기물의 축·받침·배수 구조와 지역별 타입은 무엇인가? 상징적 해석을 성행위 사건과 어떻게 분리하는가?',
        '생식 상징': '링가·요니의 기물 구조를 기존 조사 단위에 연결하고, 기능 해석과 가시 관계를 어떻게 분리하는가?',
        '구르드와라': '특정 건물의 공간·문·표지·경전 배치와 일반 종교 건축을 어떻게 구별하는가?',
        '판토크라토르': '책·축복 손·정면/반신/돔 배치가 판본별로 어떻게 다르며 글자 전사가 필요한가?',
        '수태고지': '가브리엘·마리아·거리·손·백합·빛의 관계 중 어떤 요소가 선정 작품의 필수인가?',
        '가시관': '보유 기물·착용 지물·수난 사건을 구별하고 머리와 관의 관계만으로 무엇을 판정할 수 있는가?',
        '묵시록': '구체 장·장면·등장 개체를 무엇으로 한정할 것인가? 네 기수와 다른 심판 장면의 역할이 섞이지 않는가?',
        '성 세바스티아누스': '묶인 자세·화살·기둥의 소유 관계와 상해 상태가 작품별로 어떻게 다른가?',
        '성녀 카타리나': '바퀴·칼·책 등 지물과 순교 사건을 어떻게 구별하고 어느 카타리나를 말하는가?',
        '메노라': '연대가 확인된 일곱 가지 기물 두 점의 가지·줄기·받침을 대조할 수 있는가? 하누키아와 계수 단위가 다른가?',
        '메주자': '외함·문설주·기울기와 숨은 양피지 내용을 어떻게 분리하고 공동체별 차이를 어떻게 기록하는가?',
        '키파': '실제 기물·착용 위치·재료·형태와 다른 머리 덮개를 어떻게 구별하며 착용자의 정체를 추론하지 않을 수 있는가?',
        '함사': '손 모양·눈·문자·대칭의 작품별 차이와 여러 전통의 사용을 어떻게 기록해 독점적 정체 표지를 피하는가?',
        '메르카바': '구체 문헌·도판에서 전차·바퀴·생물의 관계가 무엇인가? 현대 별 도형 표기와 어디서 갈라지는가?',
        '미나레트': '특정 지역 건물의 탑·발코니·사원 관계와 일반 탑을 어떤 근거로 구별하는가?',
        '라흘라': '접이식 경전 받침의 맞물림·경첩·책 지지 구조는 무엇인가? 책 자체와 용기의 소유를 분리하는가?',
        '디브': '페르시아 필사본의 피부·머리·의복·무기와 사건 단계가 작품별로 어떻게 다른가? 일반 오니·악마와 혼합되지 않는가?',
        '음양': '선정 도표의 흑백 경계·점·방향과 후대 변형을 어떻게 구별하며 모든 원형 도표로 넓히지 않을 수 있는가?',
        '뇌부 신장': '특정 신장 이름·날개·망치·북·복식과 배치를 어떤 작품의 설명으로 확인할 수 있는가?',
        '부록': '문자/도형의 정확한 전사·작성 매체·사용 범위를 확인하고 도교 일반 장식과 어떻게 분리하는가?',
        '서낭당': '돌무더기·나무·기물·공간 배치의 지역 사례와 사당형 차이를 무엇으로 확인하는가?',
        '단군 신화': '곰·호랑이·동굴·환웅·단군이 등장하는 구체 사건 단계와 현대 재구성의 창작 요소를 어떻게 분리하는가?',
        '이자나기': '국토 생성 사건의 두 주체·창·물·섬의 관계가 어느 도판에 근거하는가? 해석을 프리셋 배경으로 바꾸지 않는가?',
        '요미': '특정 이야기 단계의 통로·인물·가림·경계 중 실제 도판이 보여 주는 것은 무엇인가?',
        '야마타노오로치': '머리·꼬리·몸의 연결과 사건 인물 수를 도판별로 확인할 수 있는가? 히드라와 소유 구조가 다른가?',
        '오니': '가면·공연복·회화 생물의 뿔·이빨·무기·몸 구조를 어떻게 구별하는가?',
        '덴구': '새 부리형·긴 코형·가면·공연복의 시대별 변형을 어떤 작품에서 나눌 수 있는가?',
        '갓파': '머리 접시·등껍질·손발이 실제 지역 도판에서 어떻게 표현되며 일반 물 요괴와 무엇이 다른가?',
        '오시리스': '관·지팡이·채찍·몸의 싸인 형식이 특정 작품에서 누구에게 속하는가? 심판 결과의 역할을 어떻게 보존하는가?',
        '호루스': '매 전체형·매 머리 인간형·유아형과 왕관의 변형을 어떻게 나누고 눈 부적과 실체를 구별하는가?',
        '바': '인간 머리 새 몸·미라/무덤과의 관계가 정확히 어떤 작품에 보이는가? 세이렌과 연결 구조가 다른가?',
        '미라 부적': '머리받침·가슴 등 위치별 기물 형태와 실제 보존 상태는 무엇인가? 숨은 내용·효능은 어떻게 제외하는가?',
        '멜람무': '문헌의 광휘 개념과 실제 후광·의복·몸 표지가 어떻게 연결되는가? 모든 밝은 빛을 고유 도상으로 볼 근거가 있는가?',
        '에레슈키갈': '귀속이 확실한 유물과 논쟁적 인물 식별을 나누고 네르갈의 지물·역할을 어떻게 확인하는가?',
        '길가메시': '확정/불확정 인물 식별과 영웅·동물 접촉의 실제 관계를 어떻게 분리하는가?',
        '파라바하르': '선정 부조의 날개 원반·인물·손·꼬리와 후대 명칭·정체 해석을 어떻게 구별하는가?',
        '다흐마': '특정 장소의 평면·외벽·공간 구조와 사용 해석을 어떻게 나누며 단일 원형 건물을 동일시하지 않을 수 있는가?',
        '프라쇼케레티': '문헌의 갱신 서사에 고정 시각 도상이 있는가? 없다면 어떤 실제 도판 단위만 후보화할 수 있는가?',
        '고르곤': '고르곤 정면 얼굴·메두사 머리·목의 신체 연결과 뱀의 위치가 시대별로 어떻게 다른가?',
        '히드라': '머리 수와 목/몸의 연결을 작품별로 확인할 수 있는가? 잘린 머리·재생은 어떤 사건 단계인가?',
        '페가수스': '한 말 몸의 날개 부착·다리·기수 유무와 일반 날개 말 사이에 특정 도상 범위를 정할 근거가 있는가?',
        '히포캄포스': '말 앞몸과 물고기 꼬리의 접속점·다리 수·동반자가 작품별로 어떻게 다른가?',
        '키클롭스': '중앙 눈·양옆 눈의 유무가 실제 작품에서 어떻게 다르며 문헌의 외눈 정의와 일치하는가?',
        '헤카톤케이레스': '문헌의 거대한 팔/머리 수를 실제 한 이미지가 어느 정도 표현하는가? count 불가이면 무엇을 보류해야 하는가?',
        '탈로스': '청동 거인·발목·접촉 인물의 지물이 어떤 고대 작품에 근거하며 후대 기계 이미지와 어떻게 구별하는가?',
        '그라이아이': '세 인물·공유 눈/이의 소유 관계가 명시된 실제 작품이 있는가? 서사만으로 지물을 추정하지 않는가?',
        '케레스': '문헌과 꽃병 도상에서 날개·몸·죽은 대상의 관계 및 확정적 식별 근거는 무엇인가?',
        '프레이야': '목걸이·수레·동물·복식의 시대별 작품 근거가 있는가? 이름에서 모든 지물을 강제하지 않을 수 있는가?',
        '티르': '손 결손·펜리르 접촉이 어느 사건 단계와 어떤 도판에 속하는가?',
        '로키': '고대 자료의 식별 확실성과 현대 영화 디자인을 어떻게 분리하고 사건별 변신 타입을 무엇으로 한정하는가?',
        '위그드라실': '뿌리·줄기·층·동물·세계의 관계가 어떤 도판/판본에 근거하는가? 일반 세계수 소유자를 재사용할 범위는 어디까지인가?',
        '비프로스트': '다리·경계·양 끝의 관계와 색/재료는 실제 어떤 판본에 명시되는가? 친바트와 이름만으로 합치지 않는가?',
        '노른': '인물 수·우물·실/기록·나무의 관계가 작품별로 어떻게 다르며 모이라이와 소유자를 어떻게 분리하는가?',
        '발키리': '선택·전장·마중 장면과 지물의 역사 자료를 현대 갑옷/날개 디자인과 어떻게 구별하는가?',
        '펜리르': '한 늑대의 크기·속박·주체의 접촉이 어떤 사건이며 일반 늑대와 의무를 어떻게 나누는가?',
        '요르문간드': '한 뱀 몸의 감쌈·머리/꼬리·토르와의 관계를 장면별로 어떻게 구별하는가?',
        '이미르': '몸으로 세계를 만드는 서사를 실제 시각 자료가 어떻게 표현하며 요소의 소유·변환 경계가 무엇인가?',
        '라그나로크': '구체 사건 하나의 주체·대상·시간을 무엇으로 한정할 것인가? 모든 종말 요소를 한 장에 넣지 않을 수 있는가?',
        '밴시': '지역 채록·미술에서 형태와 울음 사건의 가시 근거를 어떻게 나누는가? 죽음 예고 효능은 어떻게 제외하는가?',
        '케르눈노스': '뿔·토르크·동물·자세의 확정 유물과 이름 귀속의 불확실성을 어떻게 기록하는가?',
        '모리간': '인물·까마귀·변신의 구체 장면과 후대 재구성·일반 새 상징을 어떻게 구별하는가?',
        '다그다': '곤봉·솥 등 지물이 확정된 시각 자료가 있는가? 문헌 소유만으로 얼굴/복식을 고정하지 않는가?',
        '오리샤': '포괄 명칭에서 구체 인물·지역·작품으로 범위를 좁힐 수 있는가? 어떤 지물 소유가 직접 확인되는가?',
        '샹고': '확보한 Met 지팡이의 이중 도끼와 인물/착용물 관계를 원본으로 대조하고 다른 지역 변형은 무엇인가?',
        '베베': '특정 lwa의 공개 도식에서 선·교차·문자·바닥 매체를 정확히 전사할 수 있는가? 드라포 그림과 구별하는가?',
        '아손': '공개 기물의 박·구슬망·손잡이·소유 관계와 일반 딸랑이를 어떤 근거로 구별하는가?',
        '파파 레그바': '아이티의 특정 기물·그림·행위와 다른 전통의 이름 대응을 어떻게 나눠 일반화하지 않을 수 있는가?',
        '담발라': '각 뱀 개체·맞물림·기물/도표 매체와 이름의 소유 관계를 실제 공개 자료에서 확인할 수 있는가?',
        '라 시렌': '인어 꼬리·거울/빗·기물의 작품별 소유와 마미 와타·세이렌과의 구별 근거는 무엇인가?',
        '시우아테오틀': '특정 조각의 얼굴·손·의복·자세와 정체 해석의 확실성을 어떻게 기록하는가?',
        '찰치우틀리쿠에': '물·복식·지물의 확정 작품과 논쟁적인 인물 식별을 어떻게 분리하는가?',
        '피에서': '특정 장면의 목/혈류·뱀/식물 연결을 어떤 도판이 보여 주는가? 일반 공놀이·희생 장면에 강제하지 않는가?',
        '신체로': '이미르 등 특정 서사별 몸 부분–세계 요소의 변환을 어떤 실제 도판으로 좁힐 수 있는가?',
        '죽은 자의': '발키리·심판·안내자의 서로 다른 역할을 기존 단위에 연결하고 어떤 선택 사건만 추가하는가?',
        '시체림 수행': '밀교 시체림 조사 단위로 연결하되 공개 도판의 공간·대상·단계를 무엇으로 특정하는가?',
        '종말과': '라그나로크·갱신 등 서로 다른 서사의 특정 장면과 기존 파괴/재생 의미를 어떻게 분리하는가?',
    }
    default_by_section = {
        2: '정확한 불상/보살 변형 두 점의 자세·지물·지지 관계와 이웃 식별 근거는 무엇인가?',
        3: '판본·전통이 명시된 도판의 개수·소유 지물·문자/공간을 어떻게 대조하는가?',
        4: '시기·지역이 다른 두 작품의 신체·지물·행위 차이를 어떻게 분리하는가?',
        6: '해당 인물·장면의 지물 소유와 사건 단계를 두 작품에서 어떻게 구별하는가?',
        15: '고대 도판과 후대 재구성의 몸 연결·count·지물 차이를 무엇으로 확인하는가?',
        16: '문헌 서사와 실제 도판을 분리하고 특정 사건의 주체·대상·연결은 무엇인가?',
        18: '지역/전통 내부 공개 설명과 구체 작품의 기물·매체·소유 관계를 어떻게 확인하는가?',
    }
    leads_by_section = {
        2: ['buddhism', 'early_buddhist'], 3: ['rubin_glossary', 'ritual_guide'],
        4: ['nataraja', 'durga4'], 5: ['sikh_identity', 'jina'],
        6: ['icons', 'byzantine_scenes'], 7: ['hanukkiah', 'sefirot'],
        8: ['islam_glossary', 'islam_figures'], 9: ['dao_context'],
        10: ['musindo', 'sanshin'], 11: ['shinto_shrine', 'uzume'],
        12: ['amulets', 'book_dead'], 13: ['meso_deities', 'enki'],
        14: ['fire_altar', 'chinvat'], 15: ['greek_attributes', 'chimera'],
        16: ['odin', 'sleipnir_stone'], 17: ['sheela', 'selkie'],
        18: ['shango', 'egungun', 'drapo'], 19: ['ballgame', 'coatlicue'],
        22: ['mithuna'], 23: ['book_dead', 'odin'],
    }
    high_prefixes = ('링가', '생식 상징', '칼리', '차문다', '바이라바', '바라히',
        '메노라', '고르곤', '히드라', '키클롭스', '위그드라실', '노른', '베베', '샹고')
    pending = [d for d in decisions if d['decision'] == 'FOLLOWUP_SOURCE_RESEARCH_REQUIRED']
    contexts = [d for d in decisions if d['decision'] == 'CONTEXT_ONLY_OBJECT_RESEARCH_PENDING']
    lines = ['# 후속 조사와 활성화 보류 목록', '',
        '이 문서의 질문은 아직 검증되지 않은 주장이다. 이름에서 답을 추정하거나 아래의 출처 탐색 시작점을 해당 키워드의 직접 증거로 사용하지 않는다.', '',
        f'관찰 초안이 없는 {len(pending)}행을 모두 아래에 기록했다. 맥락 단위에 연결된 {len(contexts)}행도 별도 목록으로 남긴다. 원 대화의 중복 색인 행은 삭제하지 않는다.', '',
        '## 먼저 해결할 충돌', '',
        '- 링가·요니: 기물 구조·배수/받침의 소유와 상징적 기능을 분리. 성행위 사건으로 승격하지 않기.',
        '- 칼리·차문다·바이라바·바라히: 개수·지물·표현 타입을 지역별 작품으로 분리. 이미 조사한 두르가·바즈라바라히와 경계 비교.',
        '- 메노라: 일곱 가지 작품을 확보해 하누키아의 여덟+별도 점화 위치와 비교.',
        '- 고르곤·히드라·키클롭스: 머리/눈의 count와 몸 연결을 고대 작품 단위로 확인.',
        '- 위그드라실·노른: 기존 axis_mundi·moirai 소유자를 넓힐 수 있는지, 다른 의미로 분리할지 판단.',
        '- 베베·샹고: 바닥 도표와 천 기물의 매체, 이중 도끼의 소유·착용 구조 확인.', '',
        '## 조사 방법과 완료 조건', '',
        '각 항목에서 가능한 경우 시기·지역/전통이 명시된 두 객체 또는 도판을 비교한다. 단일 자료나 귀속 논쟁만 있으면 보편 정의를 만들지 않고 그 범위를 기록한다. museum/공공 아카이브의 소장번호·원본, 전문 연구, 전통 내부의 공개 설명을 우선한다.', '',
        '남길 레코드는 원본 URL·접근 상태·대상/부분 타입·개수·지물 소유·관계·사건 단계·매체·가까운 혼동·비시각 맥락·원본 검토 결과다. 답을 찾지 못하면 context/HOLD를 유지한다.', '',
        '## 추가 출처가 필요한 94행', '']
    for section in sorted({d['section'] for d in pending}):
        section_rows = [d for d in pending if d['section'] == section]
        title = next(r['section_title'] for r in rows if r['section'] == section)
        lines += [f'### {section}. {title}', '']
        lead_ids = [sid for sid in leads_by_section.get(section, []) if sid in sources]
        if lead_ids:
            lines += ['탐색 시작점(해당 미조사 키워드의 직접 근거가 아님): ' + ', '.join(
                '[' + sources[sid]['title'].replace('[','').replace(']','') + '](' + sources[sid]['url'] + ')'
                for sid in lead_ids) + '.', '']
        lines += ['| 원문 행 | 키워드 | 조사 질문 | 순서 |', '|---|---|---|---|']
        for d in section_rows:
            matches = [(prefix, q) for prefix, q in questions.items() if d['label'].startswith(prefix)]
            q = max(matches, key=lambda item: len(item[0]))[1] if matches else default_by_section.get(
                section, '어떤 날짜·지역의 실제 도판이 진단 형태·소유·관계를 보여 주며 가장 가까운 혼동은 무엇인가?')
            priority = '우선 충돌 조사' if d['label'].startswith(high_prefixes) else '후속 객체 조사'
            lines.append('| ' + ' | '.join([d['row_id'], d['label'], q, priority]) + ' |')
        lines.append('')
    lines += ['## 맥락 수준 62행의 다음 질문', '',
        '아래 행은 이미 연결된 연구 단위가 있으나 활성 후보를 만들 만큼 특정 객체·관찰 구조가 확정되지 않았다. 추가 조사 후 같은 소유자 보강/새 변형/맥락 유지 중 하나를 결정한다.', '',
        '| 행 | 키워드 | 연결된 연구 단위 |', '|---|---|---|']
    for d in contexts:
        lines.append('| ' + ' | '.join([d['row_id'], d['label'], ', '.join(d['linked_unit_ids'])]) + ' |')
    lines += ['', '맥락 보강의 구체 방향:', '',
        '- 보호·길상·연금술 단계: 효능·해석을 그림 요소와 분리하고 특정 작품의 행위/기물만 관찰 후보로 전환.',
        '- 아발로키테슈바라·분노존·도교 신계·무신도: 포괄 명칭을 실제 지역·인물·작품 단위로 세분화.',
        '- 시크 5K·비형상/종교적 기원 개념: 숨은 기물·신앙·정체를 픽셀 판정에서 제외하고 visible 외형만 범위화.',
        '- 이슬람 인물 표현·신체/성적 색인: 명칭으로 전역 금지나 새로운 행위/sexual tone을 만들지 않고 요청·매체를 확인.',
        '- 바리·우즈메·친바트·영웅 쌍둥이·저승: 특정 사건·주체·대상의 공개 도판부터 확보.',
        '- 에궁군·마미 와타·베베/드라포·응갈료드: 속옷/완전 의상, 지역/전통, 가면/착용자, 도표/천 매체를 분리.',
        '- 이집트·메소아메리카 희생·사후 문헌: 역할·원본 귀속의 확실성을 먼저 기록하고 이름에서 결과를 추론하지 않기.',
        '- 셀키·레다·페르세포네: 문헌 사건과 실제 작품 변형, 표현된 행위와 실제 사람의 동의/욕망을 분리.', '',
        '## 이미 있는 초안에도 남은 보류', '',
        '모든 110개 초안은 원본 도판 대조와 실제 core target/property 번역이 필요하다. 그중 `prop` 27건은 현재 허용 차원이 없으며, 검색 발췌 자료·도판 미확정 케르베로스·정확한 도표/문자 전사가 필요한 항목은 추가 확인 전 보류한다. [후보 초안](CANDIDATE-DRAFTS.json)과 [실행 묶음](BATCH-PLAN.json)의 unit별 보류를 따른다.', '']
    (HERE / 'FOLLOWUP-RESEARCH.md').write_text('\n'.join(lines) + '\n')


def validate(counts, audit):
    errors = []
    rows = read('REFERENCE-KEYWORDS.json')['rows']
    units = read('SEMANTIC-UNITS.json')['units']
    drafts = read('CANDIDATE-DRAFTS.json')['drafts']
    sources = read('SOURCES.json')['sources']
    unit_ids, source_ids, row_ids = ({r['unit_id'] for r in units}, {s['source_id'] for s in sources}, {r['row_id'] for r in rows})
    for label, entries, key in [('unit', units, 'unit_id'), ('draft', drafts, 'draft_id'), ('source', sources, 'source_id'), ('row', rows, 'row_id')]:
        if len({e[key] for e in entries}) != len(entries): errors.append('duplicate '+label+' IDs')
    for u in units:
        if not set(u['source_ids']) <= source_ids or not set(u['reference_rows']) <= row_ids: errors.append('invalid unit references '+u['unit_id'])
        if not u['components'] or not u['relations'] or not u['confusion_boundaries']: errors.append('incomplete unit '+u['unit_id'])
        if u['slot_hint'] != 'context_only' and u['slot_hint'] not in audit['slot_policy']['slot_dimensions']: errors.append('unknown slot '+u['slot_hint'])
    for d in drafts:
        allowed = audit['slot_policy']['slot_dimensions'][d['slot_hint']]
        if not set(d['affected_dimensions_hint']) <= set(allowed): errors.append('dimension crosses slot '+d['draft_id'])
        if not allowed and d['affected_properties_draft']: errors.append('invented owner for unknown scope '+d['draft_id'])
        if any(k in d for k in ('rank','score','weight')): errors.append('runtime ranking in research draft')
        if not d['optional'] or d['hard_profile_activation_from_selection']: errors.append('candidate authority escalation')
    for c in read('REGRESSION-PROPOSALS.json')['cases']:
        if c['status'] != 'PROPOSED_NOT_RUN' or not set(c['unit_ids']) <= unit_ids: errors.append('false regression status/reference')
    for p in read('PIXEL-GATES.json')['cases']:
        if p['status'] != 'NOT_RUN' or not p['partial_is_fail']: errors.append('false pixel claim')
        u = next(u for u in units if u['unit_id'] == p['unit_id'])
        if p['required_component_ids'] != [c['component_id'] for c in u['components']]: errors.append('missing all-of component')
    decisions = read('TERM-DECISIONS.json')['decisions']
    if {d['row_id'] for d in decisions} != row_ids or len(decisions) != len(rows): errors.append('incomplete keyword ledger')
    for pair in read('VARIANT-RELATIONS.json')['pairs']:
        if pair['unit_a'] not in unit_ids or pair['unit_b'] not in unit_ids: errors.append('invalid pair')
    batches = read('BATCH-PLAN.json')['batches']
    batched_ids = [uid for batch in batches for uid in batch['unit_ids']]
    if len(batched_ids) != len(set(batched_ids)) or set(batched_ids) != {d['unit_id'] for d in drafts}:
        errors.append('incomplete or duplicate research batch mapping')
    for batch in batches:
        if len(batch['unit_ids']) > 8 or batch['status'] != 'PROPOSED_NOT_RUN':
            errors.append('invalid research batch size/status')
        if not set(batch['source_ids']) <= source_ids: errors.append('invalid batch sources')
        for uid in batch['unit_ids']:
            if next(d['priority_batch'] for d in drafts if d['unit_id'] == uid) != batch['phase']:
                errors.append('batch phase mismatch '+uid)
    links_checked = 0
    for path in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^\n)]+)\)', path.read_text()):
            if target.startswith(('https://','http://','chatgpt-conversation://')): continue
            resolved = Path(target.split('#')[0].strip('<>'))
            if not resolved.is_absolute(): resolved = path.parent / resolved
            if not resolved.exists(): errors.append('missing local link '+target)
            links_checked += 1
    for path in list(HERE.glob('*.md')) + list(HERE.glob('*.py')):
        if any(line.rstrip()!=line for line in path.read_text().splitlines()): errors.append('trailing whitespace '+path.name)
    ast.parse(Path(__file__).read_text())
    drift = [p for p,h in audit['protected_input_sha256'].items() if digest(ROOT / p) != h]
    if not audit['input_stable_during_read']:
        errors.append('operating input changed during read-only load')
    if drift:
        errors.append('operating input changed during research build; refresh the audit')
    result = {'schema_version': 'religion-myth-research-validation/v1',
              'status': 'PASS' if not errors else 'FAIL', 'counts': counts, 'errors': errors,
              'checks': ['JSON and unique IDs', 'all 286 row decisions', 'unit/source/reference cross-links',
                         'existing slot dimensions only', 'no rank/score/weight in drafts',
                         'optional candidates and core authority', 'all-of pixel plan',
                         'proposals remain NOT_RUN', 'all draft batch membership and phases',
                         'local Markdown links', 'whitespace and Python AST'],
              'local_links_checked': links_checked,
              'live_readonly_loader': audit['runtime_load'],
              'input_stable_during_read': audit['input_stable_during_read'],
              'protected_inputs_changed_during_build': drift,
              'evidence_layers': {'research_structure': 'PASS' if not errors else 'FAIL',
                  'runtime_integration': 'NOT_PERFORMED', 'candidate_pack_exposure': 'NOT_RUN',
                  'proposed_regressions': 'PROPOSED_NOT_RUN', 'reference_pixel_examination': 'NOT_PERFORMED',
                  'native_image_generation': 'NOT_RUN', 'native_pixel_qualification': 'NOT_RUN', 'user_acceptance': 'NOT_ASSESSED'},
              'scope': 'Only this research directory is written. No operating assets, scripts or tests are changed.'}
    write('VALIDATION.json', result)
    manifest = {p.name: digest(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'MANIFEST.json'}
    write('MANIFEST.json', {'schema_version': 'religion-myth-research-manifest/v1', 'sha256': manifest})
    print(json.dumps({'status': result['status'], 'counts': counts, 'errors': errors,
                      'protected_input_drift': drift}, ensure_ascii=False))
    if errors: raise SystemExit(1)


if __name__ == '__main__':
    audit = live_audit(read('REFERENCE-KEYWORDS.json')['rows'])
    write('LIVE-AUDIT.json', audit)
    counts = build(audit)
    build_execution_and_followup()
    validate(counts, audit)
