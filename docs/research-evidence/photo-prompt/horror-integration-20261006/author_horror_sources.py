"""Materialize reviewed still-image proposals; keep research provenance in a sidecar."""
from __future__ import annotations
import collections
import copy
import hashlib
import json
import pathlib
import sys

PROJECT = pathlib.Path(__file__).resolve().parents[4]
SKILL = PROJECT / 'skills/photo-prompt-image-generator'
EVIDENCE = pathlib.Path(__file__).resolve().parent
RESEARCH = EVIDENCE.parent / 'horror-visual-semantics-20261006'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as generator
from photo_runtime_sources import source_update

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Each property is an effect scope, not permission to change it. Wildcard
# target includes every carrier of the stated property, including child paths.
# These deliberately include comparison owners instead of inheriting the slot
# table's often empty scope. Additional actors/objects are declared separately.
SCOPE = {
    'composition': [('composition','*','spatial_arrangement')],
    'reflection_logic': [('composition','*','reflection'),('pose','reflected_subject','gesture')],
    'anatomical_connection': [('body_geometry','main_subject','anatomy'),('material','*','junction')],
    'surface_material': [('material','*','surface')],
    'prop': [('subject','*','props'),('composition','*','object_arrangement')],
    'scale_relation': [('body_geometry','*','scale'),('composition','*','depth')],
    'space_condition': [('setting','*','spatial_structure')],
    'surreal_physics_detail': [('concept','*','scene_physics'),('composition','*','spatial_arrangement')],
    'concept_tension': [('concept','*','causal_relation'),('setting','*','spatial_structure')],
    'relational_action': [('action','*','interaction'),('relationship','*','spatial_relation')],
    'situation_context': [('setting','*','occupancy'),('subject','*','props')],
    'aftermath_trace': [('material','*','residue'),('subject','*','props')],
    'capture_context': [('camera','*','recording_viewpoint'),('composition','*','frame_boundary')],
    'caption_context': [('text','*','evidence_display'),('composition','*','frame_boundary')],
    'frame_anchor_medium': [('composition','*','display_relation'),('subject','*','props')],
    'proxemics': [('relationship','*','distance'),('pose','*','gesture')],
    'subject': [('subject','*','entity_form'),('material','*','surface')],
    'species_marker': [('species','main_subject','anatomy'),('body_geometry','main_subject','anatomy')],
    'expression': [('expression','main_subject','mouth'),('appearance','main_subject','face')],
    'body_pose': [('pose','main_subject','body'),('composition','*','body_floor_relation')],
    'body_orientation': [('pose','main_subject','orientation'),('expression','main_subject','gaze')],
    'prop_direction': [('subject','*','props'),('composition','*','object_arrangement')],
    'skin_condition': [('appearance','main_subject','skin'),('color','main_subject','skin')],
    'skin_finish': [('appearance','main_subject','skin.surface')],
    'face_shape_relation': [('body_geometry','main_subject','face')],
    'eye_detail': [('appearance','main_subject','eyes')],
    'appearance_type': [('appearance','main_subject','face')],
    'hair_style': [('appearance','main_subject','hair'),('material','main_subject','wetness')],
    'lens_artifact': [('camera','*','localized_edge_artifact')],
    'wardrobe_style': [('appearance','main_subject','wardrobe')],
    'transition_stage': [('body_geometry','main_subject','anatomy'),('material','*','junction')],
    'viewer_position': [('camera','*','viewpoint'),('composition','*','occlusion')],
    'fetish_styling': [('sexual_tone','main_subject','fetish'),('appearance','main_subject','wardrobe')],
    'contact_point': [('relationship','*','contact'),('subject','*','props')],
    'location': [('setting','*','spatial_structure'),('subject','*','props')],
    'weather': [('atmosphere','*','weather'),('camera','*','visibility')],
    'atmosphere': [('atmosphere','*','fog'),('camera','*','visibility')],
    'ambient_particle': [('atmosphere','*','particles'),('lighting','*','scattering')],
    'time_of_day': [('timing','*','daylight'),('lighting','*','ambient_light')],
    'lighting': [('lighting','*','illumination')],
    'texture': [('material','*','surface')],
    'color': [('color','*','palette'),('subject','*','props')],
    'light_direction': [('lighting','*','direction')],
    'gaze_target': [('expression','*','gaze'),('composition','*','sightline')],
    'lens': [('camera','*','perspective')],
    'apparatus_pov': [('camera','*','viewpoint'),('composition','*','frame_boundary')],
}

EXTRA = {
    'reflection_pose_disagreement': [('expression','main_subject','mouth'),('expression','reflected_subject','mouth'),('appearance','reflected_subject','wardrobe')],
    'uncanny_familiar_discrepancy': [('pose','main_subject','hand'),('appearance','reflected_subject','wardrobe')],
    'folk_horror_collective_boundary': [('count','scene','people'),('subject','scene','secondary_people'),('setting','*','spatial_structure')],
    'bodily_fusion_shared_junction': [('subject','*','hardware')],
    'shadow_independent_pose': [('pose','main_subject','hands'),('lighting','*','shadow')],
    'doppelganger_pair_divergence': [('count','scene','people'),('identity','secondary_subject','appearance'),('appearance','secondary_subject','wardrobe'),('pose','*','hands')],
    'erotic_horror_attraction_threat': [('sexual_tone','*','sensual'),('count','scene','people'),('species','secondary_subject','anatomy')],
    'psychosexual_competing_attention': [('sexual_tone','*','sensual'),('count','scene','people')],
    'vampiric_seduction_dual_signal': [('sexual_tone','*','sensual'),('count','scene','people'),('species','main_subject','anatomy')],
    'daylight_exposed_threat': [('count','scene','people'),('subject','scene','secondary_people'),('pose','*','task')],
    'supernatural_coherent_breach': [('subject','scene','apparition'),('count','scene','people')],
    'cosmic_incompatible_scale': [('lighting','*','sky'),('composition','*','reflection'),('setting','*','shoreline')],
    'psychological_record_conflict': [('pose','recorded_subject','gesture'),('subject','*','props')],
    'translucent_body_occlusion': [('material','main_subject','opacity')],
    'levitation_clearance': [('concept','*','scene_physics'),('lighting','*','shadow')],
    'morgue_inventory_mismatch': [('count','scene','storage_forms')],
    'elevator_presence_comparison': [('count','scene','people'),('subject','scene','reflected_presence')],
    'recording_local_discrepancy': [('count','scene','people'),('subject','scene','recorded_presence')],
    'portrait_identity_discrepancy': [('identity','portrait_subject','appearance'),('appearance','portrait_subject','face')],
    'dramatic_irony_unseen_back': [('subject','scene','background_presence'),('expression','main_subject','gaze')],
    'offscreen_reaction_vector': [('pose','main_subject','head')],
    'slasher_pursuit_corridor': [('count','scene','people'),('subject','scene','secondary_people'),('setting','*','route_structure')],
    'laboratory_observation_barrier': [('count','scene','people'),('subject','scene','secondary_people'),('setting','*','barrier')],
    'seance_shared_focus': [('count','scene','people'),('subject','scene','secondary_people'),('subject','*','props')],
    'exorcism_contested_threshold': [('count','scene','people'),('subject','scene','secondary_people'),('subject','*','props')],
    'vampire_identity_variant': [('count','scene','people'),('subject','scene','secondary_people')],
    'zombie_reanimated_body': [('count','scene','people'),('subject','scene','secondary_people')],
}

LIMITS = [
    'This is a project-authored observable interpretation, not a mandatory genre definition or a universal cultural appearance.',
    'A still image does not establish sound, elapsed time, supernatural causation, biography, mental state, consent, chemical identity or cultural authenticity.',
    'Approximate discovery is optional. Selecting this realization requires every comparison owner and component, and cannot override frozen requester meaning.',
]

def main():
    research_units = load(RESEARCH / 'SEMANTIC-UNITS.json')['units']
    units = [u for u in research_units if u['mode'] == 'visual']
    data = generator.load_json(SKILL / 'assets/photo_prompt_tags.json')
    registry = generator.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
    existing = {(slot, str(e['id'])) for slot, rows in data['slots'].items() for e in rows}
    existing_profiles = {p['id'] for p in registry['profiles']}
    existing_texts = collections.defaultdict(list)
    for slot, rows in data['slots'].items():
        for entry in rows:
            existing_texts[(slot, str(entry.get('en','')).strip().casefold())].append(entry['id'])
    slots, profiles, mappings = collections.defaultdict(list), [], []
    candidates_by_unit = {}
    for unit in units:
        slug = unit['id'][4:]
        cid, pid = 'hr_' + slug, 'hvr_profile_' + slug
        slot = unit['proposed_slot']
        components = [c['observable_predicate_en'] for c in unit['components']]
        proposition = '; '.join(components)
        if (slot,cid) in existing or pid in existing_profiles:
            raise ValueError('Existing ID collision: ' + cid)
        if existing_texts.get((slot,proposition.casefold())):
            raise ValueError('Existing complete proposition requires manual reuse: ' + cid)
        scopes = list(dict.fromkeys(SCOPE[slot] + EXTRA.get(slug, [])))
        effects = [dict(zip(['dimension','target','property'], s)) for s in scopes]
        dimensions = list(dict.fromkeys(s[0] for s in scopes))
        if not set(dimensions) <= generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
            raise ValueError('Unknown dimension: ' + cid)
        label = unit['label'].split(' — ')[0]
        ko = label + '의 관찰 가능한 관계'
        entry = {
            'id':cid, 'ko':ko, 'en':proposition, 'weight':0.35,
            'tags':['observable_relation'], 'aliases':[proposition],
            'keywords':[label, *components],
            'paraphrases':[unit['meaning_ko'], proposition],
            'embedding_text':' ; '.join([ko, unit['meaning_ko'], proposition]),
            'concept_terms':[label, *components], 'concept_units':components,
            'relations':copy.deepcopy(unit['relations']),
            'affected_dimensions':dimensions, 'affected_properties':effects,
            'core_assertion_discovery':True,
            'contextual_usage':{'contexts':[{
                'id':cid+'_observable_scope', 'definition':unit['meaning_ko'],
                'observable_interpretation':proposition,
                'claim_limits':[ *LIMITS, 'Reject visual substitutions: ' + '; '.join(unit['confusion_boundaries'])],
                'activation_authority':'interpretation_only_not_a_required_visual_recipe',
            }]},
        }
        slots[slot].append(entry)
        candidates_by_unit[unit['id']] = entry
        authored = {
            'contract_version':'photo-authored-visual-components/v2',
            'components':[{'id':f'component_{i:02d}','match_terms':[p]} for i,p in enumerate(components,1)],
            'discovery':{'minimum_component_groups':len(components),'required_group_ids':[f'component_{i:02d}' for i in range(1,len(components)+1)]},
            'obligations':[{
                'component_ids':[f'component_{i:02d}' for i in range(1,len(components)+1)],
                'evidence':[{'field':f'component_{i:02d}_phrase','requirement':{'min_content_words':2,'must_mention_any':[p]}} for i,p in enumerate(components,1)],
                'instruction':'Retain all selected comparison owners and connected components together in one readable photograph: ' + proposition + '.',
                'render_gates':[{
                    'id':f'vo_hvr_{slug}_{i:02d}', 'review_scale':'native',
                    'description':'Inspect the original image for this component on its stated owner: ' + p + '. Hidden owners, incomplete comparison or a substitute fail this gate.',
                } for i,p in enumerate(components,1)],
            }],
        }
        complete = proposition + '.'
        profiles.append({
            'id':pid, 'category':'observable_horror_relation',
            'activation':{
                'exact_terms':[complete],
                'requires_adult_character':slug in {'erotic_horror_attraction_threat','psychosexual_competing_attention','vampiric_seduction_dual_signal','fetish_material_owner'},
                'semantic_discovery_requires_component_evidence':True,
                'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_owned_proposition','any_terms':[complete]}]},
            },
            'semantics':{
                'definition':proposition,
                'paraphrase_examples':[ko,unit['meaning_ko'],proposition],
                'visual_components':components,
                'contrast_examples':unit['confusion_boundaries'],
                'claim_limits':LIMITS,
                'interpretation_scope':{'kind':'project_visual_interpretation','description':'A concrete optional realization of the named research topic; all physical owners must remain readable.'},
            },
            'authored_components':authored,
            'concept_candidate':{'concept_terms':[label,*components], 'core_assertion_discovery':True,'affected_dimensions':dimensions,'affected_properties':effects},
            'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
            'reject_substitutes':unit['confusion_boundaries'],
        })
        mappings.append({'semantic_id':unit['id'],'candidate_id':cid,'profile_id':pid,'slot':slot,'seed_refs':unit['seed_refs'],'source_refs':unit['source_refs'],'effects':effects,'complete_proposition_duplicates':existing_texts.get((slot,proposition.casefold()),[]),'source_claim_scope':unit['source_support_scope']})

    bundles, held_bundles = [], []
    for draft in load(RESEARCH / 'BUNDLE-DRAFTS.json')['bundles']:
        members = list(draft['member_draft_ids'])
        missing = [m for m in members if not any(m == e['id'] for e in candidates_by_unit.values())]
        if missing:
            held_bundles.append({'id':draft['id'],'reason':'Contains a held cultural variant without a qualified visual interpretation','missing':missing})
            continue
        # Neighbor links are comparison notes, never implied equivalent members.
        bundles.append({
            'id':draft['id'],'primary_visual_proposition':'; '.join(draft['joint_components']),
            'component_groups':draft['joint_components'], 'candidate_ids':members,
            'hard_profile_ids':['hvr_profile_'+m[3:] for m in members],
            'confusion_boundaries':['Selecting the bundle requires the whole connected arrangement; adjacency alone is insufficient.', 'A neighboring historical or craft entry is not an equivalent owner relation.'],
            'source_keywords':[draft['id'].split('_',2)[-1].replace('_',' ')],
            'activation_mode':'optional', 'terms':draft['joint_components'],
            'relations':draft['relations'], 'candidate_only':True,
        })
    manifest = load(SKILL / 'assets/photo_prompt_source_manifest.json')
    with source_update(SKILL, EVIDENCE / 'runtime-store'):
        save(SKILL / 'assets/photo_prompt_horror_extension.json',{'schema_version':'photo-prompt-research-extension/v1','slots':dict(slots),'visual_semantics':bundles})
        save(SKILL / 'assets/photo_prompt_visual_obligations_horror.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':profiles})
        for filename,kind in [('photo_prompt_horror_extension.json','candidate'),('photo_prompt_visual_obligations_horror.json','visual_profile')]:
            if any(x['file'] == filename for x in manifest['sources']):
                raise ValueError('Already registered: '+filename)
            order = max(x['load_order'] for x in manifest['sources'] if x['kind']==kind) + 1
            manifest['sources'].append({'file':filename,'kind':kind,'required':True,'load_order':order})
        save(SKILL / 'assets/photo_prompt_source_manifest.json',manifest)
    save(EVIDENCE / 'ADOPTION-MAP.json',{
        'schema_version':'horror-data-adoption/v1',
        'counts':{'research_units':len(research_units),'added_candidates':len(units),'added_profiles':len(profiles),'added_bundles':len(bundles),'held_bundles':len(held_bundles),'native_rendered_units':0},
        'baseline_counts':{'slots':len(data['slots']),'candidates':sum(len(x) for x in data['slots'].values()),'profiles':len(registry['profiles']),'bundles':len(data.get('candidate_bundles',[]))},
        'adopted':mappings,
        'research_only':[{'id':u['id'],'mode':u['mode'],'meaning':u['meaning_ko'],'sources':u['source_refs']} for u in research_units if u['mode'] not in {'visual','reuse'}],
        'existing_neighbors':load(RESEARCH / 'RUNTIME-MAPPING.json')['mappings'],
        'held_bundles':held_bundles,
        'proof_boundary':'Authored data only. Index publication, actual candidate exposure, selection, prompt audit and native pixels require their own evidence.',
    })
    print(json.dumps({'added_candidates':len(units),'added_profiles':len(profiles),'added_bundles':len(bundles),'held_bundles':len(held_bundles),'slots':len(slots)},ensure_ascii=False))

if __name__ == '__main__':
    main()
