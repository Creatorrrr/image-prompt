#!/usr/bin/env python3
"""Reviewed authored alternatives; research records never become runtime schemas."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent / 'subculture-appearance-20261003'
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as semantics


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def rows(name: str):
    for line in (HERE / name).read_text().splitlines():
        if line and not line.startswith('#'):
            yield line.split('|')


def unique(values):
    return list(dict.fromkeys(values))


def snapshot(path: Path):
    dest = HERE / 'input-snapshot' / path.name
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():
        dest.write_bytes(path.read_bytes())


def main():
    catalog = json.loads((HERE / 'BASELINE-CATALOG.json').read_text())
    baseline_profiles = {p['id']: p for p in catalog['profiles']}
    units = {u['id'].removeprefix('sca_').upper(): u for u in json.loads((RESEARCH / 'SEMANTIC-UNITS.json').read_text())['units']}
    for extra in ('F05_SECTORAL', 'F05_CENTRAL'):
        units[extra] = copy.deepcopy(units['F05'])
        units[extra]['id'] = 'sca_' + extra.lower()
        units[extra]['confusions'] = ['a different color over the complete opposite iris', 'a light reflection substituted for an iris color region']
    candidates = {e['id']: (slot, e) for slot, entries in catalog['slots'].items() for e in entries}
    source_payloads = {}
    profile_files = {}
    for path in [ASSETS / 'photo_prompt_visual_obligations.json'] + [ASSETS / n for n in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]:
        if path.exists():
            source_payloads[path] = json.loads(path.read_text())
            for p in source_payloads[path].get('profiles', []):
                profile_files[p['id']] = path

    extension = {'schema_version': 'photo-prompt-research-extension/v1', 'slots': {}, 'existing_slot_context_extensions': {}}
    new_registry = {'schema_version': 'photo-visual-obligation-registry-extension/v1', 'relation_contract_version': 'photo-visual-relation/v1', 'profiles': []}
    receipt = {'schema_version': 'subculture-appearance-authored-integration/v1', 'new_relations': [], 'existing_owner_enrichments': [], 'held_units': []}

    def context(entry_id, phrases):
        slot, entry = candidates[entry_id]
        extension['existing_slot_context_extensions'].setdefault(slot, {})[entry_id] = {'paraphrases': unique(phrases)}

    # Research rows containing interpretive instructions or negatives are rewritten
    # as positive, selected visible relations rather than copied into runtime.
    rewritten = {'H09', 'F01', 'F02', 'F03', 'F05', 'F05_SECTORAL', 'F05_CENTRAL', 'F12', 'F13', 'G08', 'G13', 'G14', 'G20', 'X12', 'X15', 'X16'}
    advisory_labels = {
        'H01': ['아호게', 'ahoge'], 'H02': ['머리 촉각', 'antenna hair tufts'],
        'H05': ['트윈 드릴', '트윈드릴', 'twin drill hair', 'twin-drill curls'],
        'H06': ['포니 드릴', '포니드릴', 'pony drill'], 'H07': ['쌍번 머리', 'paired hair buns'],
        'H08': ['번과 포니테일 조합', 'bun and trailing tail'], 'H09': ['사이드 포니테일', 'side ponytail'],
        'H10': ['크라운 브레이드', 'crown braid'], 'H11': ['땋은 양갈래', 'braided pigtails'],
        'H13': ['한쪽 눈 메카쿠레', 'one-eye mekakure'], 'H14': ['양눈 메카쿠레', 'both-eye mekakure'],
        'H16': ['언더컷', 'undercut hair'], 'H17': ['뒤로 넘긴 앞머리 볼륨', 'raised swept-back forelock'],
        'H18': ['스파이키 헤어', 'spiky hair'], 'H19': ['반반 머리 색', 'split hair color'],
        'H20': ['인너 컬러', 'underlayer hair color'], 'H21': ['옴브레 헤어', 'ombre hair'],
        'F01': ['츠리메', 'tsurime'], 'F02': ['타레메', 'tareme'], 'F03': ['지토메', 'jitome'],
        'F04': ['하삼백안', 'lower sanpaku'], 'F05': ['좌우 오드아이', 'complete heterochromia'],
        'F05_SECTORAL': ['부분 오드아이', 'sectoral heterochromia'], 'F05_CENTRAL': ['중심 오드아이', 'central heterochromia'],
        'F06': ['세로 동공', 'vertical slit pupil'], 'F07': ['동심원 홍채', 'ringed iris'],
        'F12': ['긴 아래 속눈썹', 'long lower lashes'], 'F13': ['겹쳐 보이는 덧니', 'overlapping yaeba tooth'],
        'F14': ['삼각형 치열', 'pointed shark-like teeth'], 'F18': ['얼굴 색 분할', 'split facial surface colors'],
        'G01': ['분리 소매', 'detached sleeves'], 'G04': ['모에소데', 'moesode'],
        'G08': ['페티코트', 'cosplay petticoat'], 'G13': ['오페라 글러브', 'opera gloves'],
        'G14': ['건틀릿', 'gauntlet'], 'G19': ['멀티 벨트', 'multiple garment belts'],
        'G20': ['대비 파이핑', 'contrast piping'], 'X01': ['고양이 귀 머리띠', 'cat ear headband', 'animal-ear headband'],
        'X02': ['뿔 장식 헬멧', 'horned helmet'], 'X03': ['양눈 천 가리개', 'cloth eye band'],
        'X04': ['한쪽 눈 안대', 'monocular eyepatch'], 'X10': ['나선 머리에 감긴 리본', 'ribbon wrapped hair coil'],
        'X12': ['패치워크 의상', 'patchwork garment'], 'X15': ['옷의 평행선 도안', 'parallel line garment graphic'],
        'X16': ['기계 장식 헤드폰', 'mechanical headphones'],
    }
    changed_files = set()
    for term_id, slot, dimension, prop, exact_en, exact_ko, en_terms, ko_terms in rows('NEW-RELATION-ALTERNATIVES.psv'):
        unit = units[term_id]
        alt_en = en_terms.split(';')
        alt_ko = ko_terms.split(';')
        primary = [c['positive_relation'] for c in unit['components']]
        if term_id in rewritten:
            primary = alt_en[:]
        assert len(primary) == len(alt_en) == len(alt_ko)
        if term_id.startswith('H') and slot == 'hair_style':
            prop = 'hair.style.' + prop.removeprefix('hair.')
        if term_id == 'F03':
            prop = 'face.expression.eyelid_openness'
        if term_id == 'F18':
            prop = 'body.skin_region.pigment_distribution'
        if term_id == 'G14':
            prop = 'wardrobe.details.armour_owner_parts.hand_coverage'
        if term_id == 'G20':
            prop = 'wardrobe.details.piping_binding_welt.edge_trim'
        effects = [{'dimension': dimension, 'target': 'main_subject', 'property': prop}]
        if term_id == 'G20':
            effects.append({'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.color'})
        profile_id = 'sca_' + term_id.lower()
        phrases = unique(['; '.join(primary), '; '.join(alt_en), '; '.join(alt_ko)])
        components = []
        for i, (original, en, ko) in enumerate(zip(primary, alt_en, alt_ko), 1):
            variants = unique([original, en, ko])
            components.append({
                'id': f'component_{i}', 'match_terms': variants,
                'evidence_field': f'component_{i}_phrase',
                'evidence_terms': variants, 'min_content_words': 3,
                'instruction': f'Keep this selected relation on its declared owner: {original}.',
                'render_gate': {'id': f'vo_{profile_id}_{i}', 'review_scale': 'native',
                                'description': f'{original}. Inspect the same selected owner in original pixels. Every component is required; partial evidence fails and occluded evidence is unobservable.'},
            })
        carrier = ['hair', 'hairstyle', 'head', 'wig', '머리', '헤어', '모발', '가발'] if term_id.startswith('H') else (
            ['eye', 'eyes', 'eyelid', 'eyelids', 'face', 'mouth', 'tooth', 'teeth', 'dental', 'lashes', 'iris', 'irises', 'pupil', '눈', '눈꺼풀', '홍채', '동공', '얼굴', '치아', '치열', '속눈썹'] if term_id.startswith('F') else
            ['garment', 'sleeve', 'sleeves', 'skirt', 'petticoat', 'glove', 'gloves', 'armor', 'gauntlet', 'hand', 'headband', 'helmet', 'ribbon', 'headphones', '옷', '의복', '소매', '치마', '페티코트', '장갑', '손', '건틀릿', '갑주', '머리띠', '헬멧', '리본', '헤드폰'])
        profile = {
            'id': profile_id, 'category': 'observable_appearance_component_relation',
            'activation': {'exact_terms': [exact_en, exact_ko],
                           'requires_adult_character': dimension == 'body_geometry',
                           'semantic_discovery_requires_component_evidence': True,
                           'hard_activation': {'contract_version': 'photo-visual-hard-activation/v1',
                                               'required_any_groups': [{'id': 'declared_carrier', 'any_terms': carrier}]}},
            'semantics': {'definition': '; '.join(primary), 'paraphrase_examples': phrases,
                          'visual_components': primary,
                          'contrast_examples': unit['confusions'],
                          'claim_limits': ['Preserve the declared subject, carrier, medium and all dimension and property locks.',
                                           'This is the selected observable relation; a broad fan label or named character does not establish every component.',
                                           'Color, finish, anatomy, age and narrative cause remain separate unless explicitly selected.',
                                           'Required relations are all-of; missing components fail and occluded components are unobservable.']},
            'concept_candidate': {'concept_terms': unique([exact_en, exact_ko] + phrases + primary + advisory_labels.get(term_id, [])),
                                  'core_assertion_discovery': True, 'affected_dimensions': [dimension], 'affected_properties': effects},
            'runtime_expression': {'default_mode': 'definition_with_optional_label', 'prompt_label_terms': [],
                                   'forbidden_prompt_terms': [], 'runtime_forbidden_labels': []},
            'authored_components': {'contract_version': 'photo-authored-visual-components/v1', 'components': components},
            'reject_substitutes': unit['confusions'],
        }
        new_registry['profiles'].append(profile)
        if term_id == 'H07':
            context('space_buns', phrases)
            candidate_id = 'space_buns'
        else:
            candidate_id = profile_id
            carrier_name = 'the selected hair arrangement' if term_id.startswith('H') else ('the selected facial region' if term_id.startswith('F') else 'the selected garment or accessory')
            entry = {'id': candidate_id, 'ko': exact_ko, 'en': '; '.join(primary), 'weight': 0.5,
                     'tags': ['human', 'observable_relation'], 'for_any': ['human'],
                     'aliases': advisory_labels.get(term_id, []),
                     'paraphrases': unique([exact_en, exact_ko] + phrases),
                     'keywords': unique(primary + alt_en + alt_ko),
                     'embedding_text': ' '.join(unique([exact_en, exact_ko] + phrases)),
                     'concept_units': primary,
                     'relations': [{'id': 'declared_owner', 'type': 'declared_owner_scope', 'subject': carrier_name, 'object': 'main_subject'},
                                   {'id': 'same_owner_components', 'type': 'same_owner', 'subject': primary[0], 'object': primary[1]}],
                     'affected_dimensions': [dimension], 'affected_properties': effects, 'core_assertion_discovery': True}
            extension['slots'].setdefault(slot, []).append(entry)
        receipt['new_relations'].append({'term_id': term_id, 'profile_id': profile_id, 'candidate_id': candidate_id,
                                         'source_ids': unit['source_ids'], 'effects': effects,
                                         'decision': 'SELECTED_RELATION_SPLIT', 'components': primary})

    # Existing owners keep IDs, definitions, exact activation, guards, component
    # count, gates and effects. Only equivalent positive alternatives are added.
    for profile_id, en_terms, ko_terms in rows('EXISTING-COMPONENT-ALTERNATIVES.psv'):
        before = baseline_profiles[profile_id]
        path = profile_files[profile_id]
        profile = next(p for p in source_payloads[path]['profiles'] if p['id'] == profile_id)
        en = en_terms.split(';'); ko = ko_terms.split(';')
        groups = before['semantics']['component_semantics']['groups']
        if groups[-1]['id'] == 'owner_state':
            en.append('all compared contours remain on the same adult subject and specified region')
            ko.append('비교한 모든 윤곽이 같은 성인 인물의 지정한 영역에 속한다')
        assert len(groups) == len(en) == len(ko), profile_id
        phrases = ['; '.join(en), '; '.join(ko)]
        profile.setdefault('semantics', {}).setdefault('paraphrase_examples', [])
        profile['semantics']['paraphrase_examples'] = unique(profile['semantics']['paraphrase_examples'] + phrases)
        candidate = profile.setdefault('concept_candidate', {})
        candidate['concept_terms'] = unique(candidate.get('concept_terms', []) + phrases)
        source = profile.get('authored_components')
        if source:
            for comp, alt_en, alt_ko in zip(source['components'], en, ko):
                comp['match_terms'] = unique(comp['match_terms'] + [alt_en, alt_ko])
                comp['evidence_terms'] = unique(comp['evidence_terms'] + [alt_en])
            for field in ('composition_instruction', 'required_evidence_fields', 'evidence_requirements', 'render_gates'):
                profile.pop(field, None)
            profile['semantics'].pop('component_semantics', None)
        else:
            for group, alt_en, alt_ko, field in zip(profile['semantics']['component_semantics']['groups'], en, ko, profile['required_evidence_fields']):
                group['any_terms'] = unique(group['any_terms'] + [alt_en, alt_ko])
                profile['evidence_requirements'][field]['must_mention_any'] = unique(profile['evidence_requirements'][field]['must_mention_any'] + [alt_en])
        entry_id = {'hime_cut_structural': 'hime_cut', 'sheer_garment_optical_layering': 'sheer_garment_optical_layering'}.get(profile_id, profile_id.replace('clothing_ct', 'clt_ct').replace('costume_ccx_', 'ccx_'))
        if entry_id in candidates:
            context(entry_id, phrases)
        else:
            # Some historical profiles own a bundle, not one equivalent entry.
            # Their partial component candidates cannot inherit the whole profile.
            entry_id = None
        receipt['existing_owner_enrichments'].append({'profile_id': profile_id, 'source_file': path.name, 'candidate_id': entry_id,
                                                      'decision': 'REUSE_EQUIVALENT', 'new_full_paraphrases': phrases,
                                                      'unchanged_activation': before['activation'],
                                                      'unchanged_effects': before.get('concept_candidate', {}).get('affected_properties', []),
                                                      'unchanged_gate_ids': [g['id'] for g in before['render_gates']]})
        changed_files.add(path)

    # Keep ordinary mesh alternatives on the same owner and existing scope.
    for entry_id in ('y2kr_mesh_garment', 'athletic_mesh_open_structure'):
        context(entry_id, ['intersecting textile strands bound repeated actual openings', '직물 실이 교차하여 실제로 열린 구멍들을 둘러싼다'])
    context('short_bob_hair', ['a compact hair mass ends in a neat perimeter near the chin', '작은 머리 덩어리가 턱 부근의 정돈된 끝선에서 끝난다'])

    promoted = {r['term_id'] for r in receipt['new_relations']}
    for unit_id, unit in units.items():
        if unit_id not in promoted:
            receipt['held_units'].append({'unit_id': unit['id'], 'term_ids': unit['term_ids'], 'mode': unit['mode'],
                                          'status': 'EXISTING_AXIS_OR_SCOPED_CONTEXT_ONLY' if unit['mode'] == 'reuse' else 'NO_NEW_AUTOMATIC_ALIAS',
                                          'reason': 'Existing local owners are enriched where equivalent. Broader recipes, species/body conversion, medium changes, uncertain carriers and empty-scope prop or aftermath slots receive no automatic promotion.'})
    receipt['counts'] = {'new_profiles': len(new_registry['profiles']),
                          'new_candidates': sum(len(v) for v in extension['slots'].values()),
                          'enriched_existing_profiles': len(receipt['existing_owner_enrichments']),
                          'enriched_existing_candidates': sum(len(v) for v in extension['existing_slot_context_extensions'].values()),
                          'added_candidate_paraphrases': sum(len(x['paraphrases']) for v in extension['existing_slot_context_extensions'].values() for x in v.values())}
    save(HERE / 'INTEGRATION-MAINTENANCE.json', receipt)
    maintenance_record = {
        'contract_version': 'photo-extension-maintenance-record/v1',
        'record_id': 'subculture-appearance-integration-20261003',
        'maintenance_only': True,
        'integration_receipt': {
            'path': str((HERE / 'INTEGRATION-MAINTENANCE.json').relative_to(ROOT)),
            'sha256': sha((HERE / 'INTEGRATION-MAINTENANCE.json').read_bytes()),
        },
        'counts': receipt['counts'],
    }
    maintenance_path = HERE.parent / 'extension-maintenance' / 'subculture-appearance-integration-20261003.json'
    maintenance_path.parent.mkdir(exist_ok=True)
    save(maintenance_path, maintenance_record)
    extension['maintenance_ref'] = {'contract_version': 'photo-extension-maintenance-ref/v1',
                                  'record_id': 'subculture-appearance-integration-20261003',
                                  'sha256': semantics.digest(maintenance_record)}
    for path in sorted(changed_files):
        snapshot(path)
        save(path, source_payloads[path])
    save(ASSETS / 'photo_prompt_subculture_appearance_extension.json', extension)
    save(ASSETS / 'photo_prompt_visual_obligations_subculture_appearance.json', new_registry)
    source = SKILL / 'scripts/prompt_generator.py'
    snapshot(source)
    text = source.read_text()
    for anchor, addition in [('    "photo_prompt_visual_obligations_religion_iconography.json",', '    "photo_prompt_visual_obligations_subculture_appearance.json",'),
                             ('    "photo_prompt_religion_iconography_extension.json",', '    "photo_prompt_subculture_appearance_extension.json",')]:
        if addition not in text:
            assert anchor in text
            text = text.replace(anchor, anchor + '\n' + addition, 1)
    source.write_text(text)
    reg = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    # Refresh Python module constants after registering the files.
    import importlib
    importlib.reload(pg)
    reg = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    print(json.dumps({'counts': receipt['counts'], 'registry_profiles': len(reg['profiles']),
                      'candidate_rows': sum(len(v) for v in data['slots'].values())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
