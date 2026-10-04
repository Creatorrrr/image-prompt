"""Apply reviewed authored meanings; never synthesize source meanings at runtime."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
RESEARCH = EVIDENCE.parent / 'seduction-expression-20261004'
NEW_CANDIDATES = 'photo_prompt_seduction_expression_extension.json'
NEW_PROFILES = 'photo_prompt_visual_obligations_seduction_expression.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def distinct(values):
    result = []
    seen = set()
    for value in values:
        if value.casefold() not in seen:
            result.append(value)
            seen.add(value.casefold())
    return result

def psv(name):
    return [line.split('|') for line in (HERE / name).read_text().splitlines()
            if line.strip() and not line.startswith('#')]

def effect(dimension, prop, target='main_subject'):
    return {'dimension': dimension, 'target': target, 'property': prop}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    skill = args.root / 'skills/photo-prompt-image-generator'
    assets = skill / 'assets'
    sys.path.insert(0, str(skill / 'scripts'))
    import prompt_generator as pg
    from visual_profile_contracts import compile_visual_profile

    documents = {path.name: read(path) for path in assets.glob('*.json')
                 if path.name not in {'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'}}
    before_hashes = {name: sha(assets / name) for name in documents}
    candidate_owners = {}
    profile_owners = {}
    for name, document in documents.items():
        for slot, entries in document.get('slots', {}).items():
            for entry in entries:
                candidate_owners[slot + '.' + entry['id']] = (name, entry)
        for profile in document.get('profiles', []):
            profile_owners[profile['id']] = (name, profile)
    baseline_candidates = {key: copy.deepcopy(row[1]) for key, row in candidate_owners.items()}
    baseline_profiles = {key: copy.deepcopy(row[1]) for key, row in profile_owners.items()}
    touched = set()
    profile_additions = defaultdict(list)
    candidate_additions = defaultdict(list)
    for key, english, korean in psv('CANDIDATE-ALTERNATIVES.psv'):
        if key not in candidate_owners:
            raise ValueError('Unresolved candidate: ' + key)
        candidate_additions[key].extend([english, korean])

    # Alternatives append to existing identities without replacing effects or guards.
    context_extensions = defaultdict(dict)
    for key, alternatives in candidate_additions.items():
        slot, entry_id = key.split('.', 1)
        context_extensions[slot][entry_id] = {'paraphrases': distinct(alternatives)}

    whole_alts = {key: [english, korean] for key, english, korean in psv('PROFILE-ALTERNATIVES.psv')}
    component_alts = defaultdict(dict)
    for key, index, english, korean in psv('COMPONENT-ALTERNATIVES.psv'):
        component_alts[key][int(index)] = [english, korean]
    for profile_id, alternatives in whole_alts.items():
        name, profile = profile_owners[profile_id]
        semantics = profile['semantics']
        semantics['paraphrase_examples'] = distinct(semantics.get('paraphrase_examples', []) + alternatives)
        candidate = profile['concept_candidate']
        candidate['concept_terms'] = distinct(candidate['concept_terms'] + alternatives)
        profile_additions[profile_id].extend(alternatives)
        if 'authored_components' in profile:
            components = profile['authored_components']['components']
            if len(components) != len(component_alts[profile_id]):
                raise ValueError('Component mapping incomplete: ' + profile_id)
            for index, component in enumerate(components):
                values = component_alts[profile_id][index]
                component['match_terms'] = distinct(component['match_terms'] + values)
                component['evidence_terms'] = distinct(component['evidence_terms'] + values)
                candidate['concept_terms'] = distinct(candidate['concept_terms'] + values)
                profile_additions[profile_id].extend(values)
            # Remove old projection before rebuilding from the single authored source.
            for field in ('required_evidence_fields', 'evidence_requirements', 'render_gates', 'composition_instruction'):
                profile.pop(field, None)
            semantics.pop('component_semantics', None)
            compile_visual_profile(profile)
        else:
            groups = semantics['component_semantics']['groups']
            fields = profile['required_evidence_fields']
            if len(groups) != len(fields) or len(groups) != len(component_alts[profile_id]):
                raise ValueError('Legacy component/evidence mapping incomplete: ' + profile_id)
            for index, group in enumerate(groups):
                values = component_alts[profile_id][index]
                group['any_terms'] = distinct(group['any_terms'] + values)
                requirement = profile['evidence_requirements'][fields[index]]
                requirement['must_mention_any'] = distinct(requirement['must_mention_any'] + values)
                candidate['concept_terms'] = distinct(candidate['concept_terms'] + values)
                profile_additions[profile_id].extend(values)
        # Activation, definition, all-of minima and pixel gates keep their identity.
        before = compile_visual_profile(baseline_profiles[profile_id])
        after = compile_visual_profile(profile)
        for field in ('activation', 'render_gates', 'required_evidence_fields', 'runtime_expression'):
            assert before[field] == after[field], (profile_id, field)
        assert before['semantics']['definition'] == after['semantics']['definition']
        assert before['semantics']['component_semantics']['required_group_ids'] == after['semantics']['component_semantics']['required_group_ids']
        assert before['semantics']['component_semantics']['minimum_component_groups'] == after['semantics']['component_semantics']['minimum_component_groups']
        touched.add(name)

    research_candidates = read(RESEARCH / 'CANDIDATE-DRAFTS.json')
    # Reuse known meanings. Only missing physical units / complete scopes are authored.
    new_metadata = {
        'expression.playful_smirk': {
            'concept_units': ['a small playful smirk remains visible at the lip corners'],
            'relations': [{'id': 'se_lip_owner', 'type': 'belongs_to', 'subject': 'main_subject.lip_corners', 'object': 'main_subject.face'}],
            'affected_dimensions': ['expression'], 'affected_properties': [effect('expression', 'face.expression')]},
        'hand_pose.tucking_hair_behind_ear': {
            'concept_units': ['fingers guide the same actor hair behind the same ear', 'the fingers wrist and forearm remain attached to that actor'],
            'relations': [{'id': 'se_hair_tuck_contact', 'type': 'guides_behind', 'subject': 'main_subject.fingers', 'object': 'main_subject.hair_near_ear'}],
            'affected_dimensions': ['pose', 'appearance'],
            'affected_properties': [effect('pose', 'body.hand_configuration'), effect('pose', 'body.arm_configuration'), effect('pose', 'body.contact_configuration'), effect('appearance', 'hair')]},
        'hand_pose.reaching_toward_camera': {
            'concept_units': ['the actor arm extends toward the camera', 'the attached hand occupies a nearer depth plane than the torso', 'shoulder elbow wrist and hand remain continuous'],
            'relations': [{'id': 'se_hand_depth', 'type': 'nearer_than', 'subject': 'main_subject.hand', 'object': 'main_subject.torso'}, {'id': 'se_arm_direction', 'type': 'extends_toward', 'subject': 'main_subject.arm', 'object': 'camera'}],
            'affected_dimensions': ['pose'], 'affected_properties': [effect('pose', 'body.hand_configuration'), effect('pose', 'body.arm_configuration')]},
    }
    missing_effects = {
        'expression.ctx_c126': [effect('expression', 'face.expression'), effect('action', 'body.action_configuration')],
        'lighting.sff_pro_l01': [effect('lighting', 'face')],
        'lighting.sff_pro_l05': [effect('lighting', 'face')],
        'lighting.sff_pro_l07': [effect('lighting', 'face')],
        'lighting.sff_pro_l08': [effect('lighting', 'face')],
        'light_shape.lit_clean_vertical_catchlight_pair': [effect('lighting', 'eyes.light_reflection')],
        'composition.pc_pc17_component_2': [effect('camera', '*', '*'), effect('composition', '*', '*')],
    }
    metadata_updated = []
    for key, patch in new_metadata.items():
        name, entry = candidate_owners[key]
        for field, value in patch.items():
            if entry.get(field):
                raise ValueError('Existing metadata must be reviewed instead of replaced: ' + key + '.' + field)
            entry[field] = copy.deepcopy(value)
        entry['core_assertion_discovery'] = True
        metadata_updated.append(key); touched.add(name)
    for key, effects in missing_effects.items():
        name, entry = candidate_owners[key]
        if entry.get('affected_properties'):
            raise ValueError('Existing effects must not be replaced: ' + key)
        entry['affected_properties'] = effects
        entry['affected_dimensions'] = distinct(entry.get('affected_dimensions', []) + [e['dimension'] for e in effects])
        metadata_updated.append(key); touched.add(name)
    # Existing explicit adult / attraction / task prerequisites survive byte for byte.
    for key in metadata_updated:
        for field in ('requires_all_tags', 'requires_primary_any_tags', 'for_any', 'contextual_usage', 'aliases', 'en', 'ko'):
            assert baseline_candidates[key].get(field) == candidate_owners[key][1].get(field), (key, field)

    new_whole = {key: [english, korean] for key, english, korean in psv('NEW-CANDIDATE-ALTERNATIVES.psv')}
    new_components = defaultdict(dict)
    for key, index, english, korean in psv('NEW-COMPONENT-ALTERNATIVES.psv'):
        new_components[key][int(index)] = [english, korean]
    slots = defaultdict(list)
    new_by_key = {}
    owner_replacements = {
        'core_declared_gaze_target': 'the specified gaze target',
        'core_declared_gesture_target': 'the specified gesture target',
        'core_declared_light': 'the specified light source',
        'core_existing_garment.lapel_edge': 'main_subject.wardrobe.lapel_edge',
        'core_existing_garment.small_fold': 'main_subject.wardrobe.small_fold',
        'core_existing_garment': 'main_subject.wardrobe',
        'core_existing_pendant.body': 'main_subject.accessories.pendant.body',
        'core_existing_necklace.chain': 'main_subject.accessories.necklace.chain',
        'core_existing_partner.lips': 'the specified existing partner lip region',
    }
    for draft in research_candidates['new_candidate_proposals']:
        slot = draft['slot']; entry = copy.deepcopy(draft['candidate_entry_template']); entry_id = entry['id']
        entry['weight'] = 0.6
        entry['for_any'] = ['human']
        entry['tags'] = distinct(['human', slot])
        entry['paraphrases'] = distinct(entry.get('paraphrases', []) + new_whole[entry_id])
        entry['core_assertion_discovery'] = True
        for relation in entry['relations']:
            for field in ('subject', 'object'):
                relation[field] = owner_replacements.get(relation[field], relation[field])
        for row in entry['affected_properties']:
            if row['property'] == 'garment': row['property'] = 'wardrobe'
        if entry_id == 'se_existing_pendant_fingertip_hold':
            entry['affected_dimensions'].append('appearance')
            entry['affected_properties'].append(effect('appearance', 'accessories'))
        if entry_id == 'se_eye_visible_through_own_hair':
            entry['affected_properties'].append(effect('expression', 'face.expression'))
        # Conditions are explicit premises, not inferred from the candidate's tags.
        prerequisites = {
            'se_lapel_fingertip_touch': ['lapel', 'collar', 'jacket', 'blazer', '라펠', '옷깃'],
            'se_small_garment_fold_pinch': ['garment', 'clothing', 'fabric', 'apron', 'shirt', 'dress', '옷', '천', '앞치마'],
            'se_existing_pendant_fingertip_hold': ['pendant', 'necklace', '펜던트', '목걸이'],
        }
        if entry_id in prerequisites:
            entry['requires_primary_any_tags'] = prerequisites[entry_id]
        if entry_id in {'se_gaze_at_existing_partner_lips_state', 'se_beckon_shaped_finger_static_state'}:
            entry['contextual_usage'] = {'contexts': [{
                'id': entry_id + '_still_boundary',
                'application_conditions': ['The stated target already exists in the final scene.'],
                'limits': ['One still establishes the current direction or flexion only; temporal order and repeated movement require separate frames.'],
                'status': 'current_visible_state_only'}]}
        slots[slot].append(entry); new_by_key[slot + '.' + entry_id] = entry

    lip = {
        'id': 'se_tongue_lip_contact_state', 'ko': '같은 입의 혀끝과 바깥 입술의 접촉 상태',
        'en': 'the tongue tip from the same mouth touches the specified outer lip surface',
        'weight': 0.6, 'tags': ['human', 'expression'], 'for_any': ['human'],
        'aliases': ['same-mouth tongue tip on the outer lip', '같은 입의 혀끝이 바깥 입술에 닿음'],
        'keywords': ['tongue tip lip contact', '혀끝 입술 접촉'],
        'concept_units': ['the visible tongue tip meets the stated outer lip surface', 'the tongue continues into the same actor mouth', 'the touching tongue tip and receiving lip area are both visible'],
        'relations': [{'id': 'se_tongue_lip_contact', 'type': 'contact', 'subject': 'main_subject.tongue.tip', 'object': 'main_subject.specified_outer_lip'}],
        'affected_dimensions': ['expression'], 'affected_properties': [effect('expression', 'face.expression')],
        'core_assertion_discovery': True, 'paraphrases': new_whole['se_tongue_lip_contact_state'],
        'contextual_usage': {'contexts': [{'id': 'se_tongue_lip_contact_still', 'limits': ['A still shows contact; it does not establish a complete lick, wetting or movement sequence.'], 'status': 'current_visible_state_only'}]},
    }
    lip['embedding_text'] = '; '.join([lip['ko'], lip['en'], *lip['concept_units'], *lip['paraphrases']])
    slots['expression'].append(lip); new_by_key['expression.' + lip['id']] = lip

    profiles = []
    candidate_profiles = {}
    profile_drafts = read(RESEARCH / 'PROFILE-DRAFTS.json')
    for draft in profile_drafts['new_profile_proposals']:
        profile = copy.deepcopy(draft['profile_template'])
        entry = new_by_key[draft['candidate_key']]
        candidate_profiles[draft['candidate_key']] = profile['id']
        exact = {term.casefold() for term in profile['activation']['exact_terms']}
        profile['semantics']['paraphrase_examples'] = [term for term in distinct(profile['semantics'].get('paraphrase_examples', []) + new_whole[entry['id']]) if term.casefold() not in exact]
        profile['semantics']['claim_limits'] = ['Only the current visible configuration is established by a still image.']
        profile['concept_candidate'].update({
            'core_assertion_discovery': True,
            'affected_dimensions': entry['affected_dimensions'],
            'affected_properties': entry['affected_properties'],
        })
        profile['concept_candidate']['concept_terms'] = distinct(profile['concept_candidate']['concept_terms'] + new_whole[entry['id']])
        for index, component in enumerate(profile['authored_components']['components']):
            alternatives = new_components[entry['id']][index]
            component['match_terms'] = distinct(component['match_terms'] + alternatives)
            component['evidence_terms'] = distinct(component['evidence_terms'] + alternatives)
            component['instruction'] = 'Show this visible configuration on the specified actor: ' + entry['concept_units'][index] + '.'
            component['render_gate']['description'] = 'The image visibly shows that ' + entry['concept_units'][index] + '.'
            profile['concept_candidate']['concept_terms'] = distinct(profile['concept_candidate']['concept_terms'] + alternatives)
        for field in ('required_evidence_fields', 'evidence_requirements', 'render_gates', 'composition_instruction'):
            profile.pop(field, None)
        profile['semantics'].pop('component_semantics', None)
        compile_visual_profile(profile)
        profiles.append(profile)
    lip_profile = {
        'id': 'se_profile_tongue_lip_contact_state', 'category': 'observable_mouth_contact',
        'activation': {'exact_terms': lip['aliases'], 'requires_adult_character': False, 'semantic_discovery_requires_component_evidence': True},
        'semantics': {'definition': lip['en'], 'paraphrase_examples': lip['paraphrases'], 'visual_components': lip['concept_units'], 'contrast_examples': ['a protruding tongue separated from the lip', 'a tongue hidden inside the mouth'], 'claim_limits': ['A still proves current contact only.']},
        'concept_candidate': {'concept_terms': distinct([lip['ko'], lip['en'], *lip['concept_units'], *lip['paraphrases']]), 'core_assertion_discovery': True, 'affected_dimensions': lip['affected_dimensions'], 'affected_properties': lip['affected_properties']},
        'runtime_expression': {'default_mode': 'definition_with_optional_label', 'prompt_label_terms': [], 'forbidden_prompt_terms': [], 'runtime_forbidden_labels': []},
        'reject_substitutes': ['tongue protrusion without lip contact', 'a complete movement sequence claimed from one still'],
        'authored_components': {'contract_version': 'photo-authored-visual-components/v1', 'components': []},
    }
    for index, unit in enumerate(lip['concept_units']):
        alternatives = new_components[lip['id']][index]
        lip_profile['authored_components']['components'].append({
            'id': 'c' + str(index + 1), 'match_terms': distinct([unit, *alternatives]),
            'evidence_field': 'c' + str(index + 1) + '_phrase', 'evidence_terms': distinct([unit, *alternatives]),
            'min_content_words': 3, 'instruction': 'Show this current mouth relation on the specified actor: ' + unit + '.',
            'render_gate': {'id': 'vo_se_tongue_lip_contact_c' + str(index + 1), 'review_scale': 'native', 'description': 'The image visibly shows that ' + unit + '.'}})
        lip_profile['concept_candidate']['concept_terms'] = distinct(lip_profile['concept_candidate']['concept_terms'] + alternatives)
    compile_visual_profile(lip_profile); profiles.append(lip_profile)
    candidate_profiles['expression.' + lip['id']] = lip_profile['id']

    bundles = []
    for draft in read(RESEARCH / 'BUNDLE-DRAFTS.json')['bundles']:
        source = draft['bundle_entry_template']
        keys = draft['candidate_keys']
        members = [(key.split('.', 1)[0], new_by_key.get(key, candidate_owners.get(key, (None, None))[1])) for key in keys]
        if any(entry is None for _, entry in members): raise ValueError('Unresolved bundle ' + source['id'])
        # A member contributes its own exact observable meaning, never a widened draft summary.
        bundles.append({
            'id': source['id'], 'candidate_only': True,
            'primary_visual_proposition': 'Optional combination of the stated visible configurations.',
            'candidate_ids': [entry['id'] for _, entry in members],
            'candidate_slots': {entry['id']: slot for slot, entry in members},
            'hard_profile_ids': [candidate_profiles[key] for key in keys if key in candidate_profiles],
            'component_groups': [{'id': 'option_' + str(index + 1), 'visible_evidence': pg.photo_candidate_semantics.concept_units(entry)} for index, (_, entry) in enumerate(members)],
            'confusion_boundaries': ['Only selected components change the final scene.', 'Each component retains its declared owner, dependencies and property effects.', 'Profile activation requires independent request evidence.'],
            'relations': [],
        })
    maintenance_record = {
        'record_id': 'seduction-expression-integration-20261005',
        'contract_version': 'photo-extension-maintenance-record/v1',
        'research_sources': str(RESEARCH / 'SOURCES.json'),
        'scope': 'Equivalent positive paraphrases, component evidence alternatives and scoped current visible relations.',
        'baseline_source_sha256': {name: before_hashes[name] for name in sorted(touched)},
        'previous_maintenance_refs': {name: documents[name].get('maintenance_ref') for name in sorted(touched) if documents[name].get('schema_version') == 'photo-prompt-research-extension/v1'},
        'authored_alternative_inputs': {name: sha(HERE / name) for name in ['CANDIDATE-ALTERNATIVES.psv', 'PROFILE-ALTERNATIVES.psv', 'COMPONENT-ALTERNATIVES.psv', 'NEW-CANDIDATE-ALTERNATIVES.psv', 'NEW-COMPONENT-ALTERNATIVES.psv']},
        'candidate_equivalent_paraphrase_count': sum(len(distinct(v)) for v in candidate_additions.values()),
        'candidate_equivalent_target_count': len(candidate_additions),
        'profile_alternative_count': sum(len(distinct(v)) for v in profile_additions.values()),
        'profile_equivalent_target_count': len(profile_additions),
        'candidate_metadata_updated': metadata_updated,
        'new_candidate_keys': list(new_by_key), 'new_profile_ids': [p['id'] for p in profiles],
        'optional_bundle_ids': [b['id'] for b in bundles],
        'limits': ['No psychological motive, age or relationship is inferred from appearance.', 'Still images establish current state, not temporal sequence.', 'Exact activation, original profile definitions, all-of minima and existing pixel gates remain unchanged for enriched profiles.', 'Rendered qualification is recorded separately.'],
    }
    record_path = HERE / 'MAINTENANCE-RECORD.json'; write(record_path, maintenance_record)
    maintenance_ref = {'contract_version': 'photo-extension-maintenance-ref/v1', 'record_id': maintenance_record['record_id'], 'sha256': sha(record_path)}
    extension = {'schema_version': 'photo-prompt-research-extension/v1', 'maintenance_ref': maintenance_ref, 'slots': dict(slots), 'existing_slot_context_extensions': dict(context_extensions), 'visual_semantics': bundles}
    profile_extension = {'schema_version': 'photo-visual-obligation-registry-extension/v1', 'relation_contract_version': 'photo-visual-relation/v1', 'profiles': profiles}
    documents['photo_prompt_tags.json']['candidate_semantic_policy']['required_extensions'].append(NEW_CANDIDATES)
    touched.add('photo_prompt_tags.json')
    for name in touched:
        document = documents[name]
        if document.get('schema_version') == 'photo-prompt-research-extension/v1': document['maintenance_ref'] = maintenance_ref
        write(assets / name, document)
    write(assets / NEW_CANDIDATES, extension); write(assets / NEW_PROFILES, profile_extension)
    generator = skill / 'scripts/prompt_generator.py'
    code = generator.read_text()
    for name, marker in [(NEW_CANDIDATES, 'RESEARCH_EXTENSION_FILENAMES = (\n'), (NEW_PROFILES, 'VISUAL_OBLIGATION_EXTENSION_FILENAMES = (\n')]:
        if '    "' + name + '",' in code: raise ValueError('Already registered: ' + name)
        start = code.index(marker)
        end = code.index('\n)\n', start)
        code = code[:end] + '\n    "' + name + '",' + code[end:]
    generator.write_text(code)
    write(HERE / 'APPLIED-CHANGES.json', {
        'implementation_root': str(args.root.resolve()),
        'authored_files': sorted(touched | {NEW_CANDIDATES, NEW_PROFILES}),
        'registration_file': 'skills/photo-prompt-image-generator/scripts/prompt_generator.py',
        'source_hashes_after': {name: sha(assets / name) for name in sorted(touched | {NEW_CANDIDATES, NEW_PROFILES})},
        'original_profile_invariants_preserved': sorted(profile_additions),
        'existing_candidate_guards_and_labels_preserved': metadata_updated,
        'counts': {key: maintenance_record[key] for key in ['candidate_equivalent_paraphrase_count', 'candidate_equivalent_target_count', 'profile_alternative_count', 'profile_equivalent_target_count']},
    })
    print(json.dumps({'authored_files': len(touched) + 2, 'candidate_paraphrases': len(candidate_additions), 'enriched_profiles': len(profile_additions), 'new_candidates': len(new_by_key), 'new_profiles': len(profiles), 'optional_bundles': len(bundles)}))

if __name__ == '__main__':
    main()
