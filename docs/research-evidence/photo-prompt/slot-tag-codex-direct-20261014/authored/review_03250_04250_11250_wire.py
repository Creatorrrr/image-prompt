"""Serialize literal per-record authored judgements; no semantic classification."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R));import direct_review as d
# Each default is an explicitly chosen schema path, not inferred source semantics.
S={
 'brow_style':('appearance','brows.structure'),
 'body_form':('body_geometry','body.form'),
 'declared_person_background':('identity','identity.background'),
 'character_contrast':('character_response','character.contrast'),
 'lip_color_placement':('appearance','lips.color'),
 'lip_finish':('appearance','lips.finish'),
 'facial_geometry':('body_geometry','face.geometry'),
 'platform_framing':('framing','platform.framing'),
 'skin_tone':('appearance','skin.color'),
 'facial_hair':('appearance','face.facial_hair'),
 'gender_presentation':('appearance','presentation.gender'),
 'light_intensity':('lighting','lighting.level'),
 'capture_configuration':('camera','capture.configuration'),
 'camera_type':('camera','camera.type'),
 'camera_distance':('camera','camera.distance'),
 'eye_detail':('appearance','eyes.structure'),
 'lash_style':('appearance','lashes.state'),
 'garment_fit':('appearance','garment.fit'),
 'attire_context':('role','wardrobe.context'),
 'body_hair':('appearance','body.hair'),
 'nail_appearance':('appearance','nails.decoration'),
 'wearable_accessory':('appearance','accessories.type'), 'subject_framing':('framing','framing.coverage'),
 'image_artifact':('camera','image.artifact'), 'action':('action','action.activity'),
 'garment_detail':('appearance','garment.construction'), 'makeup_style':('appearance','makeup.style'),
 'makeup_decoration':('appearance','makeup.decoration'), 'contact_point':('relationship','contact.endpoints'),
 'hand_pose':('pose','hands.pose'), 'proxemics':('relationship','spacing.relative'),
 'location':('setting','setting.location'), 'prop':('subject','props.type'),
 'composition':('composition','layout.arrangement'), 'physical_motion':('action','motion.state'),
 'subject':('subject','subject.type'), 'body_pose':('pose','body.pose'),
 'time_of_day':('timing','timing.time_of_day'), 'situation_context':('event','situation.context'),
 'capture_context':('camera','capture.context'), 'genre':('style','genre.type'),
 'relational_action':('action','relation.action'), 'prop_placement':('composition','props.placement'),
 'prop_state':('role','props.state'), 'surface_material':('material','surface.material'),
 'space_condition':('setting','space.state'), 'visible_text':('text','text.content'),
 'mood':('atmosphere','mood.reading'), 'companion_animal':('relationship','companion.animal'),
 'age_presentation':('age','age.declared'), 'wardrobe_style':('appearance','wardrobe.ensemble'),
 'color_grading':('color','grading.tone'), 'color':('color','color.palette'),
 'texture':('material','surface.texture'), 'light_shape':('lighting','lighting.pattern'),
 'light_direction':('lighting','lighting.direction'), 'exposure':('camera','image.exposure'),
 'wardrobe_layering':('appearance','wardrobe.layers'), 'lighting':('lighting','lighting.setup'),
 'format':('format','format.layout'), 'scale_relation':('body_geometry','scale.relation'),
 'expression':('expression','face.expression'), 'participant_role':('relationship','participant.role'),
 'narrative_phase':('timing','timing.event_phase'), 'calendar_context':('timing','calendar.context'),
 'gaze_direction':('expression','gaze.direction'), 'body_orientation':('pose','body.orientation'),
 'aesthetic_trend':('style','aesthetic.reference'), 'footwear':('appearance','footwear.type'),
 'gaze_target':('expression','gaze.target'), 'gaze_engagement':('expression','gaze.engagement'),
 'garment_state':('appearance','garment.state'), 'world':('setting','world.rule'),
 'aftermath_trace':('timing','aftermath.trace'), 'light_color':('lighting','lighting.color'),
 'light_type':('lighting','lighting.source'), 'skin_finish':('appearance','skin.finish'),
 'skin_condition':('appearance','skin.state'), 'hair_style':('appearance','hair.style'),
 'hair_color':('appearance','hair.color'), 'body_region':('body_geometry','body.region'),
 'body_marking':('appearance','body.marking'), 'presentation_style':('appearance','presentation.style'),
 'lens_artifact':('camera','optics.artifact'), 'motion_rendering':('camera','image.motion'),
 'light_quality':('lighting','lighting.quality'), 'narrative_core':('event','narrative.core'),
 'narrative_clue':('concept','narrative.clue'), 'concept_tension':('concept','concept.contrast'),
 'surreal_concept':('concept','concept.surreal'), 'surreal_physics_detail':('concept','surreal.physics'),
 'sensory_cue':('viewer_outcome','sensory.cue'), 'image_detail':('camera','image.detail'),
 'staging_degree':('style','capture.staging'), 'historical_period':('timing','timing.era'),
 'viewer_position':('viewer_outcome','viewer.position'), 'shot_scale':('framing','shot.scale'),
 'camera_height':('camera','camera.height'), 'camera_direction':('camera','camera.direction'),
 'apparatus_pov':('camera','view.optical_path'), 'depth_of_field':('camera','camera.depth_of_field'),
 'focus':('camera','focus.plane'), 'lens':('camera','lens.projection'),
 'season':('timing','timing.season'), 'weather':('atmosphere','weather.state'),
 'environment_detail':('setting','environment.detail'), 'background_element':('setting','background.elements'),
 'character_intent':('character_response','character.intent'), 'social_cue':('relationship','social.response'),
 'silhouette_proportion':('body_geometry','wardrobe.silhouette'), 'spatial_depth':('composition','spatial.depth'),
 'grain_profile':('style','image.grain'), 'film_emulation':('style','film.emulation'),
 'medium':('style','media.type'), 'procedure_step':('action','procedure.step'),
 'occasion_context':('event','occasion.type'), 'crowd_density':('setting','crowd.density'),
 'anatomical_connection':('body_geometry','body.connection'), 'species_marker':('species','species.marker'),
 'transformation_stage':('timing','timing.transformation_stage'), 'visual_density':('composition','layout.density'),
 'visual_hierarchy':('composition','layout.hierarchy'), 'reflection_logic':('composition','reflection.correspondence'),
 'shadow_relation':('composition','shadow.relation'), 'ambient_particle':('atmosphere','particles.type'),
 'atmospheric_medium':('atmosphere','atmosphere.medium'), 'offscreen_context':('event','context.offscreen'),
 'subject_count':('count','subject.count'), 'fetish_styling':('sexual_tone','sexual_tone.fetish'),
 'adult_presentation_context':('sexual_tone','sexual_tone.adult_context'),
}
def save(start,stop,literal,corrections=None,pending=None):
 p=R/'packets'/f'{start:05d}-250.json';packet=json.loads(p.read_text());data=d.source();catalog=data['slot_catalog'];rows=[]
 for line in literal.strip().splitlines():
  if not line.strip():continue
  n,meaning,specs,boundary=line.split('|');n=int(n);cid=packet['ids'][n-start];record=d.corrected_record(packet['records'][cid],(corrections or {}).get(n,[]));facts=[];roles={}
  for spec in specs.split(';'):
   tag,owner,*extra=spec.split(':'); field='en';prop=None
   for item in extra:
    if item.startswith('@'):field=item[1:]
    else:prop=item
   dimension,default=S[tag];prop=prop or default
   f=dict(pointer='/content/'+field,quote=d.pointer(record,'/content/'+field,positive=True),dimension=dimension,target=owner,property=prop)
   facts.append(dict(f,realization_id='base'))
   if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=catalog[tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=meaning,evidence=[])
   roles[tag]['evidence'].append(f)
  row=dict(candidate_id=cid,meaning_summary=meaning,recommended_kind='visual_option',corrections=(corrections or {}).get(n,[]),roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=[],status='approved',all_roles_considered=True)
  if n in (pending or {}):
   row['status']='needs_boundary_review';row['uncertainties']=[dict(kind='inline_alternative_scope',detail=pending[n])]
  if n == 11429:
   # Explicit source-native optional realization, directly authored after full branch read.
   rid='visible_recorded_playback'
   for role in row['roles']:
    role['realization_ids']=['base',rid]
   for f in list(row['facts']):row['facts'].append({**f,'realization_id':rid})
   f=dict(pointer='/content/en',quote='only when an already-declared recorded playback is visible, signal dropout appears in that playback image rather than on the physical tape surface',dimension='camera',target='recorded_playback_image',property='image.artifact.signal_dropout')
   row['facts'].append({**f,'realization_id':rid})
   row['roles'].append(dict(slot_id='image_artifact',semantic_role=catalog['image_artifact']['semantic_role'],scope='positive_alternative',realization_ids=[rid],rationale='Only already-declared visible recorded playback carries signal dropout; physical carriers do not.',evidence=[f]))
  rows.append(row)
 assert len(rows)==stop-start,(len(rows),stop-start)
 authored=R/'authored'/f'review_03250_04250_{start:05d}_{stop:05d}.json'
 for i,row in enumerate(rows,1):
  full={**d.binding(data,row['candidate_id']),**row,'schema':d.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':d.c.digest(packet),'authored_decision':dict(file=str(authored.relative_to(d.ROOT)),item=i,sha256=d.c.digest(row))}
  try:d.validate_decision(full,data)
  except Exception:
   print("Validation row",start+i-1,row["candidate_id"],[(x["slot_id"],x["evidence"]) for x in row["roles"]]);raise
 d.write(authored,dict(decisions=rows))
 print(authored,len(rows))
