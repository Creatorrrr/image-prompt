#!/usr/bin/env python3
"""Author reviewed fire data; run explicitly against an isolated checkout."""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import sys
from pathlib import Path

REUSE = {
    'F127': ('subject', 'coronal_mass_ejection_observation_subject'),
    'F131': ('lens_artifact', 'pe_veiling_flare'),
    'F132': ('lens_artifact', 'pe_aligned_ghosts'),
    'F133': ('lens_artifact', 'pe_horizontal_anamorphic_streak'),
}
# Reviewed natural component expressions. These affect optional discovery only.
MATCH = {
 'F001': [['dark wick','candle wick'],['flame attached to the wick','flame above the wick'],['liquid wax pool','melted wax pool','wax pool']],
 'F002': [['wood surfaces','burning wood','stacked logs'],['flame tongues','flames attached to the wood'],['gaps between the logs','gaps between the wood']],
 'F003': [['charred fuel fragment','charred ember','charcoal fragment'],['red luminous patch','red glowing patch','red glow'],['adjoining dark surface','dark charcoal surface']],
 'F004': [['emitting fire','hot work point','source fire'],['separate luminous particles','detached sparks','separate sparks'],['dark air separating','air gaps between sparks']],
 'F005': [['glowing fuel fragment','glowing wood fragment'],['air separating the fragment','air gap around the fragment'],['source fire','charred fuel bed']],
 'F008': [['candle wick','extinguished wick'],['wisp rooted at the wick','smoke wisp from the wick'],['wax pool','cooling wax']],
 'F011': [['burner outlet','burner port'],['blue inner cone','blue conical flame'],['outer flame envelope','enclosing flame envelope']],
 'F014': [['discharge opening','torch nozzle','nozzle opening'],['continuous flame jet','elongated flame jet'],['aligned with the nozzle','aligned with the outlet']],
 'F033': [['blue flame envelope','blue flame'],['burner at its base','flame rooted at the burner'],['scene outside the flame','surrounding material colors']],
 'F034': [['yellow orange flame','orange flame','red flame'],['source at its base','fire base'],['irregular flame boundary','luminous flame boundary']],
 'F037': [['luminous fire source','visible fire source'],['fire facing surface','warm firelight on her face','warm illumination on the face'],['darker far side','surface turned away from the fire']],
 'F038': [['surface illuminated from one direction','firelit face'],['transition to the unlit side','unlit side of the face'],['offscreen fire source','fire outside the frame']],
 'F039': [['fire beside the water','fire above the water','flame beside the water'],['reflective water plane','reflective water surface'],['broken elongated reflection','broken fire reflection','reflection aligned with the fire']],
 'F041': [['hot surface','visible fire source'],['background edge above the source','background edge through hot air'],['localized waviness','wavy background edge','heat shimmer']],
 'F045': [['emitting fire','smoke source'],['plume rooted at that source','smoke plume connected to the fire'],['background obscured by smoke','detail obscured behind the plume']],
 'F048': [['room ceiling','ceiling plane'],['smoke beneath the ceiling','ceiling smoke layer'],['clearer lower room','legible room below the smoke']],
 'F051': [['loose ash deposit','flaky ash deposit'],['tray supporting the ash','ground supporting the ash'],['dark fuel fragments','charcoal fragments in ash']],
 'F052': [['wall surface','object surface'],['dark matte soot deposit','soot adhering to the surface'],['cleaner area boundary','boundary with a cleaner area']],
 'F058': [['charred wood surface','charred timber'],['polygonal cracks','blocky char cracks'],['raised dark blocks','raised char blocks']],
 'F070': [['battery enclosure','battery cell'],['outlet on the enclosure','cell vent'],['plume rooted at the outlet','plume from the same vent']],
 'F074': [['suppression nozzle','hose nozzle'],['water stream from the nozzle','connected water stream'],['stream lands on the burning material','water reaches the same fire']],
 'F082': [['low fuel layer','low vegetation'],['branches bridging the gap','shrubs bridging the vertical gap'],['same tree crown','higher crown above the bridge']],
 'F083': [['main fire front','main fire line'],['unburned gap','unburned space between fires'],['smaller active fire beyond','secondary fire beyond the gap']],
 'F085': [['smoke plume from the fire','fire rooted smoke plume'],['condensate cloud above the plume','cloud above the smoke'],['towering upper cloud','connected towering cloud']],
 'F090': [['open brazier','bounded brazier'],['charcoal inside the brazier','charcoal bed'],['red glow in the charcoal','glowing charcoal patches']],
 'F092': [['wax candle','recognizable candle'],['wax runnel','wax running down its side'],['wax deposit at the lower end','thickened wax at the base']],
 'F094': [['torch shaft','torch body'],['burning torch head','fuel at the torch head'],['flames attached to the head','flame rooted at the torch head']],
 'F098': [['long handled fire tool','fire poker'],['tip inside the fire bed','poker tip inside the fuel bed'],['fuel touched by the tip','tip contacting the same log']],
 'F101': [['vessel of molten metal','crucible holding molten metal'],['stream from the vessel lip','molten stream from the lip'],['receiving mold beneath','same mold receiving the stream']],
 'F102': [['heated metal on an anvil','glowing metal on the anvil'],['hammer aligned with the metal','hammer above the same workpiece'],['same metal impact region','same workpiece contact region']],
 'F104': [['welding tool','welding torch'],['bright region on the joint','bright weld joint'],['sparks leaving the joint','particles from the same joint']],
 'F105': [['pipe held by the glassworker','glass blowpipe','blowpipe'],['glass gather attached','glass gather on the pipe'],['shaping tool touching the gather','tool contacting the same glass']],
 'F106': [['fixed flame source','lampworking burner','fixed torch flame'],['glass rod into the flame','rod entering the flame'],['softened section of the rod','softened glass rod tip']],
 'F107': [['wood grain surface','wooden drawing surface'],['drawing tip meeting the wood','heated pen touching the wood'],['dark line at the tip','line adjoining the same tip']],
 'F110': [['charcoal heat source','wood fire heat source'],['cooking support above the fire','grate above the charcoal'],['food resting on the grate','food on the same cooking support']],
 'F114': [['cooking pan','flambe pan'],['food in the same pan','sauce in the pan'],['flame above the pan contents','flame envelope above the food']],
 'F115': [['culinary torch','kitchen torch'],['flame toward one food patch','torch flame aimed at the food'],['same food beneath the tip','food patch below the flame']],
 'F123': [['solar limb edge','edge of the solar disk'],['plasma arch beyond the limb','prominence beyond the limb'],['contacts with the solar limb','feet attached to the limb']],
 'F132': [['bright optical source','bright source entering the lens'],['translucent flare ghosts','separate optical shapes'],['scene behind the shapes','objects behind the ghosts']],
 'F136': [['molten rock flow','lava flow'],['darker lava crust','solidifying crust'],['luminous gaps in the crust','orange gaps within the crust']],
 'F138': [['pointed mast','pointed structure'],['blue violet tip glow','violet glow at the mast tip'],['intact mast below','structure beneath the glow']],
 'F144': [['creature silhouette','figure silhouette'],['flames composing the body','flame forms composing the body'],['ground relation for the creature','creature standing above the ground']],
 'F145': [['fictional bird body','phoenix body'],['paired wings connected','wings attached to the bird'],['flames integrated with wing edges','flames at the tail edges']],
 'F146': [['readable dragon','dragon body'],['mouth opening on the dragon','open dragon mouth'],['flame jet from the same mouth','connected breath flame']],
 'F148': [['heat source','visible fire'],['hands of the same person','her hands'],['gap between hands and fire','hands separated from the source']],
 'F149': [['selected skin region','same forearm patch'],['wax deposit on the skin','wax resting on that skin'],['wax skin contact boundary','wax touching the same skin']],
 'F150': [['garment owned by its wearer','same garment'],['blackened curled fabric edge','charred fabric edge'],['missing fabric patch','hole contiguous with the burned edge']],
 'F152': [['bearer of a historical flame tool','historical flame tool bearer'],['tool connected to the fuel pack','hose to the same fuel pack'],['flame from the nozzle','continuous flame issuing from the nozzle']],
}
NONVISUAL = {('F038','component_3'),('F118','component_3'),('F130','component_2')}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def effects(card):
    uid=card['id']; rows=copy.deepcopy(card['proposed_effects'])
    # Paths shared with the existing owner/partial-property consumer; a slot
    # carrier cannot hide a change to skin, clothing or camera properties.
    overrides={
      'F030':[('camera','image_plane','motion.particle_trails')],
      'F037':[('lighting','receiver_surface','illumination.firelight')],
      'F038':[('lighting','receiver_surface','illumination.firelight')],
      'F040':[('lighting','receiver_surface','illumination.cast_shadow')],
      'F059':[('appearance','main_subject','hair.local_surface_state')],
      'F077':[('appearance','main_subject','wardrobe.protective_equipment'),('action','main_subject','body.hand_tool_contact')],
      'F105':[('action','main_subject','body.hand_tool_contact'),('material','glass_gather','surface.shaping_contact')],
      'F130':[('color','solar_image_plane','processing.channel_color')],
      'F148':[('pose','main_subject','hands.position'),('relationship','main_subject','hands.heat_source_gap')],
      'F149':[('material','main_subject','body.skin.wax_deposit'),('relationship','main_subject','body.skin.wax_contact')],
      'F150':[('appearance','main_subject','wardrobe.surface.thermal_damage'),('appearance','main_subject','wardrobe.coverage'),('material','main_subject','wardrobe.surface.thermal_damage')],
      'F152':[('action','main_subject','body.hand_tool_contact'),('relationship','historical_flame_tool','nozzle.fuel_pack_connection')],
    }
    if uid in overrides:
        rows=[dict(zip(('dimension','target','property'),x)) for x in overrides[uid]]
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve();skill=root/'skills/photo-prompt-image-generator'
    sys.path.insert(0,str(skill/'scripts'))
    import prompt_generator as pg
    from photo_runtime_sources import source_update
    from visual_profile_contracts import compile_visual_profile,validate_visual_profile_source,validate_hard_activation
    research=root/'docs/research-evidence/photo-prompt/fire-semantics-20261008'
    evidence=research/'integration';evidence.mkdir(exist_ok=True)
    cards=json.loads((research/'SEMANTIC-UNITS.json').read_text())['cards']
    drafts={d['unit_id']:d for d in json.loads((research/'CANDIDATE-DRAFTS.json').read_text())['drafts']}
    existing=pg.load_json(skill/'assets/photo_prompt_tags.json')
    ids={e['id'] for values in existing['slots'].values() for e in values}
    extension={'schema_version':'photo-prompt-research-extension/v1','slots':{},'existing_slot_context_extensions':{}}
    profiles=[];ledger=[]
    for original in cards:
        c=copy.deepcopy(original);uid=c['id']
        if not c['renderable']:
            ledger.append({'unit_id':uid,'decision':'context_only','reason':c['confusion_boundaries'],'source_ids':c['source_ids']});continue
        components=c['observable_components']
        if uid=='F104':components[2]['observable_form_en']='separate luminous particles leaving that same joint'
        if uid=='F105':components[2]['observable_form_en']='a shaping tool contacting that same glass gather'
        if uid=='F130':components[2]['observable_form_en']='a consistent assigned display color across the same solar image'
        phrase='; '.join(x['observable_form_en'] for x in components)
        ef=effects(c);dimensions=list(dict.fromkeys(x['dimension'] for x in ef))
        context={'id':f'fire_{uid.lower()}_boundary','definition':c['confusion_boundaries'][0],
          'observable_interpretation':phrase,'claim_limits':c['claim_limits'],
          'activation_authority':'interpretation_only_not_a_required_visual_recipe'}
        slot=c['proposed_slot'];eid=c['candidate_id']
        if uid in REUSE:
            slot,eid=REUSE[uid];assert eid in ids
            # Context is excluded from retrieval projections. These reviewed
            # paraphrases retain the original carrier/effects and candidate ID.
            extension['existing_slot_context_extensions'].setdefault(slot,{})[eid]={'paraphrases':[c['label_ko'],phrase],'contexts':[context]}
            decision='reuse_existing_identity_with_equivalent_paraphrase'
        else:
            entry=copy.deepcopy(drafts[uid]['runtime_entry_proposal']);assert eid not in ids
            entry.update(en=phrase,paraphrases=[phrase],concept_terms=[x['observable_form_en'] for x in components],
                         concept_units=[x['observable_form_en'] for x in components],affected_dimensions=dimensions,affected_properties=ef,
                         embedding_text=c['label_ko']+'; '+phrase,contextual_usage={'contexts':[context]})
            if slot=='subject':entry['kind']=['environment' if c['domain'] in ['solar','noncombustion'] else 'object']
            extension['slots'].setdefault(slot,[]).append(entry);decision='new_optional_owned_realization'
        proposition=phrase+'.'
        component_rows=[];gates=[];evidence_rows=[]
        for i,comp in enumerate(components):
            terms=[comp['observable_form_en']]+MATCH.get(uid,[[],[],[]])[i]
            component_rows.append({'id':comp['id'],'match_terms':list(dict.fromkeys(terms))})
            evidence_rows.append({'field':comp['id']+'_phrase','requirement':{'min_content_words':3,'must_mention_any':[comp['observable_form_en']]}})
            if (uid,comp['id']) not in NONVISUAL:
                gates.append({'id':f'vo_fire_{uid.lower()}_{i+1}','review_scale':'native',
                  'description':f'Inspect the complete visible component on its stated owner {comp["owner_role"]}: {comp["observable_form_en"]}. Partial, hidden or different-owner substitutes fail. This does not establish temperature, chemical identity or causal history.'})
        if uid=='F038':relation_gate='The illumination and unlit transition belong to the same receiving surface. The declared offscreen source is prompt context, not a visible-source requirement.'
        elif uid=='F130':relation_gate='One solar observation image carries a consistent assigned display color. Channel identity is declared metadata and cannot be verified from the hue alone.'
        else:relation_gate='The visible parts share their specified physical owners and continuous spatial connections in this single frame: '+ '; '.join(f'{r["subject"]} {r["type"]} {r["object"]}' for r in c['relations'])+'. A transferred component or disconnected neighboring object fails.'
        gates.append({'id':f'vo_fire_{uid.lower()}_owned_relation','review_scale':'both','description':relation_gate})
        profile={'id':f'fire_rel_{uid.lower()}','category':'fire_component_relation',
          'activation':{'exact_terms':[proposition],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,
            'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_owned_proposition','any_terms':[proposition]}]}},
          'semantics':{'definition':phrase,'paraphrase_examples':[c['label_ko'],phrase],
            'visual_components':[x['observable_form_en'] for x in components],
            'contrast_examples':c['confusion_boundaries'],'claim_limits':c['claim_limits']+['Approximate discovery is optional; neither a broad keyword nor a visual realization creates requester authority.']},
          'authored_components':{'contract_version':'photo-authored-visual-components/v2','components':component_rows,
            'discovery':{'minimum_component_groups':2,'required_group_ids':['component_2']},
            'obligations':[{'component_ids':[x['id'] for x in components],'evidence':evidence_rows,
             'instruction':'Retain the complete selected realization on the stated owners: '+phrase+'. Metadata remains declared context; invisible attributes are not pixel evidence.',
             'render_gates':gates}]},
          'concept_candidate':{'concept_terms':[c['label_ko']]+[x['observable_form_en'] for x in components],
             'core_assertion_discovery':True,'affected_dimensions':dimensions,'affected_properties':ef},
          'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
             'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':c['confusion_boundaries']}
        validate_visual_profile_source(profile);validate_hard_activation(profile['activation']['hard_activation']);compile_visual_profile(profile)
        profiles.append(profile)
        ledger.append({'unit_id':uid,'decision':decision,'source_ids':c['source_ids'],'source_access_limits':c['source_access_limits'],
          'candidate_id':eid,'profile_id':profile['id'],'slot':slot,'owner_roles':[x['owner_role'] for x in components],
          'effects':ef,'metadata_component_ids':[x['id'] for x in components if (uid,x['id']) in NONVISUAL],
          'claim_basis':'authored_optional_visual_realization_with_source_boundaries',
          'process_identity_claim':'not_inferred_from_pixels','consumer_review':'declared effects consumed by property_effects_allowed; physical role binding remains literal composition and native review',
          'additional_specialist_claims':'not_promoted; specific age, history, process identity and ritual edition require requester context or separate evidence'})
    record={'schema_version':'photo-extension-maintenance-record/v1','record_id':'fire-owned-realizations-20261008',
      'source_filename':'photo_prompt_fire_relations_extension.json','maintenance_only':True,
      'research_source':'fire-semantics-20261008','rows':ledger}
    record_bytes=(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode()
    extension['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],
      'sha256':hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
    assets=skill/'assets';manifest_path=assets/'photo_prompt_source_manifest.json'
    manifest=json.loads(manifest_path.read_text())
    names=[('photo_prompt_fire_relations_extension.json','candidate'),('photo_prompt_visual_obligations_fire_relations.json','visual_profile')]
    for name,kind in names:
        assert not any(r['file']==name for r in manifest['sources'])
        manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':1+max(r['load_order'] for r in manifest['sources'] if r['kind']==kind)})
    with source_update(skill):
        write(assets/names[0][0],extension)
        write(assets/names[1][0],{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':profiles})
        write(manifest_path,manifest)
    (evidence/'ADOPTION-LEDGER.json').write_bytes(record_bytes)
    (root/'docs/research-evidence/photo-prompt/extension-maintenance'/f'{record["record_id"]}.json').write_bytes(record_bytes)
    stats={'new_candidates':sum(map(len,extension['slots'].values())),'reused_candidates':len(REUSE),'new_profiles':len(profiles),
      'native_and_relation_gates':sum(len(x['authored_components']['obligations'][0]['render_gates']) for x in profiles),
      'context_only_units':sum(not c['renderable'] for c in cards),'new_candidate_slots':len(extension['slots']),
      'source_files':[name for name,kind in names],'runtime_version_changes':False,'scientific_process_or_safety_claims':False}
    write(evidence/'ADOPTION-STATS.json',stats);print(json.dumps(stats,ensure_ascii=False))

if __name__=='__main__':main()
