"""Author reviewed body morphology data; provenance stays in this evidence area."""
from collections import defaultdict
from pathlib import Path
import copy
import csv
import hashlib
import json
import sys

OUT = Path(__file__).resolve().parent
RESEARCH = OUT.parent
ROOT = OUT.parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

PROFILE_FILE = 'photo_prompt_visual_obligations_body_morphology.json'
CANDIDATE_FILE = 'photo_prompt_body_morphology_extension.json'
LOCAL_SEPARATIONS = {'hip_width', 'hip_dip_local'}
ADDITIONAL_PROFILE_REUSE = {'cleavage_relation': 'pfe_cleavage', 'midriff_boundary': 'pfe_midriff'}
CANDIDATE_REUSE = {
    'slender_build': ('silhouette_proportion', 'slender_linear_build'),
    'long_limb_build': ('silhouette_proportion', 'willowy_long_limb_proportion'),
    'soft_volume': ('silhouette_proportion', 'soft_full_figure_volume'),
    'curvilinear_relation': ('silhouette_proportion', 'curvilinear_figure_relation'),
    'muscle_definition': ('silhouette_proportion', 'toned_muscular_definition'),
    'clavicle_landmark': ('anatomical_connection', 'clavicle_supraclavicular_hollow'),
    'breast_projection': ('anatomical_connection', 'bust_to_ribcage_projection_relation'),
    'hip_dip_local': ('anatomical_connection', 'trochanteric_depression_hip_dip'),
    'back_dimples': ('anatomical_connection', 'posterior_psis_dimples_pair'),
    'gluteal_fold': ('anatomical_connection', 'infragluteal_crease_boundary'),
    'calf_contour': ('anatomical_connection', 'calf_to_ankle_taper'),
    'philtral_contour': ('anatomical_connection', 'philtral_columns_cupid_bow'),
    'neckline_exposure': ('anatomical_connection', 'decolletage_neckline_exposure_boundary'),
    'lateral_chest_boundary': ('garment_detail', 'pfe_lateral_chest_candidate'),
    'lower_chest_boundary': ('garment_detail', 'pfe_lower_chest_candidate'),
    'cleavage_relation': ('garment_detail', 'pfe_cleavage_candidate'),
    'midriff_boundary': ('garment_detail', 'pfe_midriff_candidate'),
    'striae_surface': ('skin_finish', 'ctx_c109'),
}
# These are scoped morphology senses, never bare community/evaluative labels.
SCOPED_ALIASES = {
    'stocky_build': ['stocky body build', '다부진 몸통과 사지 체격'],
    'wiry_definition': ['wiry body build', '가는 체격의 근육과 힘줄 윤곽'],
    'muscle_volume': ['regional muscle bulk', '부위별 근육 부피'],
    'muscle_striation': ['regional muscle striations', '국소 근육 줄무늬 윤곽'],
    'vascular_surface': ['localized superficial vascularity', '국소 표재 혈관 윤곽'],
    'shoulder_width': ['bilateral shoulder width relation', '양쪽 어깨 폭 관계'],
    'shoulder_slope': ['neck-to-shoulder slope relation', '목에서 어깨 끝으로의 경사'],
    'ribcage_width': ['ribcage transverse width relation', '흉곽 가로 폭 관계'],
    'ribcage_depth': ['ribcage front-back depth relation', '흉곽 앞뒤 깊이 관계'],
    'breast_root_width': ['breast attachment width relation', '가슴 부착 폭 관계'],
    'breast_projection': ['breast anterior projection relation', '가슴 앞쪽 돌출 관계'],
    'breast_spacing': ['bilateral breast spacing relation', '양쪽 가슴 사이 간격 관계'],
    'hip_width': ['bilateral hip width relation', '양쪽 골반 부위 폭 관계'],
    'gluteal_projection': ['posterior gluteal projection relation', '엉덩이 뒤쪽 돌출 관계'],
    'hip_dip_local': ['localized lateral hip indentation', '국소 힙딥 윤곽'],
    'thigh_volume': ['thigh transverse volume relation', '허벅지 가로 볼륨 관계'],
    'finger_proportion': ['finger-to-palm proportion relation', '손가락 대 손바닥 비율'],
    'eye_spacing': ['bilateral eye spacing relation', '양쪽 눈 사이 간격 관계'],
    'eye_aperture': ['eye-opening aspect relation', '눈 개구의 가로세로 관계'],
    'cellulite_relief': ['localized skin cellulite relief', '국소 피부 패임 부조'],
    'body_hair_distribution': ['regional body-hair distribution', '부위별 체모 분포'],
    'skin_relief_texture': ['localized skin pore microrelief', '국소 모공 미세 요철'],
}
SPECIAL_DIMENSIONS = {
    'compression_contour': ['appearance', 'body_geometry'],
    'thigh_gap': ['body_geometry', 'pose'],
    'pose_surface_change': ['pose', 'body_geometry', 'appearance'],
}
SPECIAL_PROPERTIES = {
    'compression_contour': [('appearance', 'wardrobe.band.contact'), ('body_geometry', 'body.abdomen.contact_contour')],
    'thigh_gap': [('body_geometry', 'body.inner_thighs.negative_space'), ('pose', 'body.feet.stance')],
    'pose_surface_change': [('pose', 'body.load_and_configuration'), ('body_geometry', 'body.regional.surface_deformation'),
                            ('appearance', 'body.regional.surface_relief')],
}
ANATOMICAL_CONTEXT_IDS = {'nipple_projection', 'areolar_surface', 'gluteal_cleft', 'vulvar_topology',
    'penile_topology', 'scrotal_testis_boundary', 'perineal_location'}
SLOT_OVERRIDES = {'nail_shape': 'body_evidence_region', 'thigh_gap': 'body_evidence_region'}

def load(path):
    return json.loads(path.read_text())

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def distinct(values):
    seen = set()
    result = []
    for value in values:
        if value.casefold() not in seen:
            result.append(value)
            seen.add(value.casefold())
    return result

with (RESEARCH / 'PROPOSAL-SPECS.psv').open() as f:
    specs = list(csv.DictReader(f, delimiter='|'))
registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
corpus = pg.load_json(ASSETS / 'photo_prompt_tags.json')
if PROFILE_FILE in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES or (ASSETS / PROFILE_FILE).exists():
    raise SystemExit('Integration is already authored. Review source diffs; do not replay blindly.')
baseline = dict(registry_profiles=len(registry['profiles']),
    candidate_entries=sum(len(es) for es in corpus['slots'].values()),
    profile_ids=[p['id'] for p in registry['profiles']],
    candidate_ids={s:[e['id'] for e in es] for s, es in corpus['slots'].items()},
    source_receipts=load(RESEARCH / 'CURRENT-DATA-AUDIT.json')['source_files'])
save(OUT / 'BASELINE.json', baseline)
documents = {name: load(ASSETS / name) for name in
    ['photo_prompt_visual_obligations.json', 'photo_prompt_tags.json',
     *pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES, *pg.RESEARCH_EXTENSION_FILENAMES]}
originals = copy.deepcopy(documents)
profile_owner = {p['id']:(name,p) for name, doc in documents.items() for p in doc.get('profiles', [])}
candidate_owner = {(slot,e['id']):(name,e) for name, doc in documents.items()
                   for slot, entries in doc.get('slots', {}).items() for e in entries}
new_profiles, new_slots, crosswalk = [], defaultdict(list), []
policy = documents['photo_prompt_tags.json']['candidate_semantic_policy']
existing_terms = {t.casefold():p['id'] for p in registry['profiles']
    for t in p['activation']['exact_terms'] + p['activation'].get('project_glossary_aliases', [])}

for spec in specs:
    key = spec['id']
    units = spec['components'].split(';')
    slot = CANDIDATE_REUSE.get(key, (SLOT_OVERRIDES.get(key, spec['slot']), ''))[0]
    dimensions = SPECIAL_DIMENSIONS.get(key, policy['slot_dimensions'][slot])
    if key == 'neckline_exposure':
        dimensions = ['appearance']
    properties = [dict(dimension=d, target='main_subject', property=p) for d, p in
        SPECIAL_PROPERTIES.get(key, [(d, 'body.' + spec['owner'].removeprefix('adult_') + '.' + spec['property'])
                                    for d in dimensions])]
    existing = [p for p in spec['existing_profiles'].split(',') if p]
    if key in LOCAL_SEPARATIONS:
        existing = []
    if key in ADDITIONAL_PROFILE_REUSE:
        existing = [ADDITIONAL_PROFILE_REUSE[key]]
    if existing:
        profile_id = existing[0]
        owner_name, profile = profile_owner[profile_id]
        semantic = profile['semantics']
        semantic['paraphrase_examples'] = distinct(semantic.get('paraphrase_examples', []) + [spec['ko'], spec['en']])
        profile['concept_candidate']['concept_terms'] = distinct(profile['concept_candidate']['concept_terms'] + units)
        profile_action = 'enriched_existing_without_replacing_contract'
    else:
        profile_id = 'bm_' + key
        exact = distinct([spec['ko'], spec['en'], *SCOPED_ALIASES.get(key, [])])
        exact = [term for term in exact if term.casefold() not in existing_terms]
        for term in exact:
            existing_terms[term.casefold()] = profile_id
        component_groups = [dict(id=f'component_{i+1}', any_terms=[u]) for i,u in enumerate(units)]
        component_groups.append(dict(id='owner_state', any_terms=[
            'the stated contours belong to the same adult subject and specified body region',
            'the named body region remains connected to the same adult subject']))
        evidence_keys = [f'component_{i+1}_phrase' for i in range(len(units))] + ['owner_state_phrase']
        profile = dict(id=profile_id, category='adult_local_morphology_relation',
            activation=dict(exact_terms=exact, requires_adult_character=True,
                semantic_discovery_requires_component_evidence=True),
            semantics=dict(definition=spec['en'] + '; the same adult region visibly establishes ' + '; '.join(units) + '.',
                paraphrase_examples=['같은 성인 인물에서 ' + spec['ko'] + '를 부위별로 읽는 형태',
                                     'An adult region showing ' + '; '.join(units) + '.'],
                visual_components=units,
                component_semantics=dict(minimum_component_groups=len(component_groups),
                    required_group_ids=[g['id'] for g in component_groups], groups=component_groups),
                contrast_examples=[spec['closest_counterexample']],
                claim_limits=[
                    'Observe the named adult body region in the specified view and current state; an occluded required component is unassessable.',
                    'Visible surface geometry does not establish numerical composition, health, strength, attractiveness or personal history.',
                    'Preserve the requester-defined property and reference scope; adjacent regions and garment geometry are separate owners.',
                    'Partial evidence fails complete qualification; retrieval alone creates no hard obligation.']),
            concept_candidate=dict(concept_terms=distinct([spec['ko'], spec['en'], *units]),
                core_assertion_discovery=True, affected_dimensions=dimensions, affected_properties=properties),
            runtime_expression=dict(default_mode='definition_with_optional_label',
                prompt_label_terms=[spec['en']], forbidden_prompt_terms=[], runtime_forbidden_labels=[]),
            composition_instruction='Bind each visible component to the same adult subject and specified body region; show ' +
                '; '.join(units) + '; retain the current garment boundary, pose state and requester property locks.',
            required_evidence_fields=evidence_keys,
            evidence_requirements={name:dict(min_content_words=2, must_mention_any=component_groups[i]['any_terms'])
                                   for i,name in enumerate(evidence_keys)},
            render_gates=[dict(id=f'vo_{profile_id}_{g["id"]}', review_scale='native' if spec['batch'] in {'P3','P4'} else 'both',
                description='The same adult subject and specified region visibly establish ' + g['any_terms'][0] + '.')
                          for g in component_groups],
            reject_substitutes=['wrong_owner_or_body_region', 'garment_or_shadow_substitute',
                               'occluded_required_component', 'unsupported_history_or_quantity_inference'])
        if key in ANATOMICAL_CONTEXT_IDS:
            profile['activation']['context_disambiguation'] = dict(required_with_authorial_core=True,
                any_terms=['anatomy', 'anatomical', 'diagram', '해부', '도식'],
                exclude_if_any_terms=['unrelated ordinary portrait', '일반 얼굴 사진'])
            profile['semantics']['claim_limits'].append('This local topology applies to an explicitly requested neutral anatomical view or diagram; names alone create no exposure or action requirement.')
        new_profiles.append(profile)
        profile_action = 'new_independent_axis'
        owner_name = PROFILE_FILE

    candidate_id = CANDIDATE_REUSE.get(key, ('', 'bm_' + key))[1]
    if key in CANDIDATE_REUSE:
        candidate_file, candidate = candidate_owner[(slot, candidate_id)]
        candidate['paraphrases'] = distinct(candidate.get('paraphrases', []) + [spec['ko'], spec['en']])
        candidate['concept_units'] = distinct(candidate.get('concept_units', []) + units)
        candidate['relations'] = candidate.get('relations', []) + [dict(id='body_morphology_owner_' + key,
            type='has_visible_property', subject='main_subject', object=spec['en'])]
        candidate['affected_dimensions'] = dimensions
        candidate['affected_properties'] = properties
        candidate['core_assertion_discovery'] = True
        candidate_action = 'enriched_existing_candidate'
    else:
        candidate_file = CANDIDATE_FILE
        candidate = dict(id=candidate_id, ko=spec['ko'], en=spec['en'], weight=0.5,
            tags=['human', spec['owner'].removeprefix('adult_')], for_any=['human'],
            aliases=distinct([spec['ko'], *SCOPED_ALIASES.get(key, [])]),
            keywords=units, paraphrases=[spec['ko'], spec['en']],
            embedding_text=spec['en'] + '; ' + '; '.join(units), concept_units=units,
            relations=[dict(id='owner_property', type='has_visible_property', subject='main_subject',
                            object=spec['en'])],
            affected_dimensions=dimensions, affected_properties=properties, core_assertion_discovery=True)
        if key in ANATOMICAL_CONTEXT_IDS:
            candidate['requires_any_tags'] = ['anatomy', 'anatomical', 'diagram', '해부', '도식']
        new_slots[slot].append(candidate)
        candidate_action = 'new_scoped_candidate'
    crosswalk.append(dict(proposal_id='body_research_' + key, axis=key, profile_id=profile_id,
        profile_source=owner_name, profile_action=profile_action, candidate_id=candidate_id,
        candidate_slot=slot, candidate_source=candidate_file, candidate_action=candidate_action,
        affected_dimensions=dimensions, affected_properties=properties, source_refs=spec['sources'].split(','),
        preserved_legacy_exact=True))

# Keep locally narrow wording separate from historical whole-transition aliases.
transition_file, transition = profile_owner['lateral_waist_hip_contour_transition']
transition['activation']['exclude_if_any_terms'] = distinct(transition['activation'].get('exclude_if_any_terms', []) +
    ['localized lateral hip indentation', '국소 힙딥 윤곽'])

save(ASSETS / PROFILE_FILE, dict(schema_version='photo-visual-obligation-registry-extension/v1',
    relation_contract_version='photo-visual-relation/v1', profiles=new_profiles))
save(ASSETS / CANDIDATE_FILE, dict(schema_version='photo-prompt-research-extension/v1', slots=dict(new_slots)))
for name, doc in documents.items():
    if doc != originals[name]:
        save(ASSETS / name, doc)

script_path = SKILL / 'scripts/prompt_generator.py'
script = script_path.read_text()
for last, new in [('photo_prompt_visual_obligations_pose_vocabulary.json', PROFILE_FILE),
                  ('photo_prompt_pose_vocabulary_extension.json', CANDIDATE_FILE)]:
    needle = '    "' + last + '",\n'
    assert script.count(needle) == 1, (last, script.count(needle))
    script = script.replace(needle, needle + '    "' + new + '",\n')
script_path.write_text(script)
tags_path = ASSETS / 'photo_prompt_tags.json'
tags = load(tags_path)
tags['candidate_semantic_policy']['required_extensions'].append(CANDIDATE_FILE)
save(tags_path, tags)

changed = [name for name,doc in documents.items() if doc != originals[name]]
save(OUT / 'INTEGRATION-MANIFEST.json', dict(schema_version='body-morphology-integration/v1',
    axes_integrated=len(crosswalk), new_profiles=len(new_profiles),
    enriched_profiles=sum(x['profile_action'] != 'new_independent_axis' for x in crosswalk),
    new_candidates=sum(len(v) for v in new_slots.values()),
    enriched_candidates=sum(x['candidate_action']=='enriched_existing_candidate' for x in crosswalk),
    crosswalk=crosswalk, changed_existing_assets=changed,
    context_only_records='All 11 measurement/taxonomy/history/community/workflow records remain research provenance, not positive prototypes.',
    property_review='Existing explicit per-entry affected_dimensions override supports coupled effects; all affected properties are declared.',
    legacy_boundary='Existing ID, label, component requirements and gates retained. Narrow local indentation suppresses the broader historical transition when explicitly named.'))
print(json.dumps(dict(axes=len(crosswalk), new_profiles=len(new_profiles), new_candidates=sum(len(v) for v in new_slots.values()),
    enriched_candidates=len(CANDIDATE_REUSE), changed_assets=changed), ensure_ascii=False))
