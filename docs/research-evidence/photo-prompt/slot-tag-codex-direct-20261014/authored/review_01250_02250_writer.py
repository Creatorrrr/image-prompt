"""Serialization only of individually authored source-read judgments for this worker."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import direct_review as d
C=json.loads((HERE.parent/'CATALOG.json').read_text())
P={
'transformation_stage':('body_geometry','transformation.stage'),
'camera_type':('camera','camera.type'),'camera_distance':('camera','camera.distance'),
'companion_animal':('subject','companion.animal'),
'expression':('expression','face.expression'), 'character_contrast':('character_response','character.contrast'),
'subject_framing':('framing','framing.coverage'),'shot_scale':('framing','shot.scale'),
'proxemics':('relationship','spacing'),'prop':('subject','props.type'),'prop_state':('role','props.state'),
'prop_placement':('composition','props.placement'),'gaze_target':('expression','gaze.target'),
'weather':('atmosphere','weather'),'action':('action','action'),'relational_action':('action','relation.action'),
'presentation_style':('appearance','presentation.style'),'location':('setting','setting.location'),
'color':('color','color.local'),'body_pose':('pose','body.pose'),'physical_motion':('action','motion'),
'light_shape':('lighting','lighting.pattern'),'light_type':('lighting','lighting.source'),
'subject':('subject','subject.type'),'attire_context':('role','wardrobe.context'),
'surface_material':('material','surface.material'),'texture':('material','surface.texture'),
'ambient_particle':('atmosphere','air.particles'),'atmospheric_medium':('atmosphere','air.medium'),
'composition':('composition','layout.arrangement'),'camera_direction':('camera','camera.direction'),
'camera_height':('camera','camera.height'),'mood':('atmosphere','mood'),
'season':('timing','timing.season'),'narrative_clue':('concept','narrative.clue'),
'focus':('camera','focus.target'),'apparatus_pov':('camera','view.optical_path'),
'participant_role':('relationship','participant.role'),'offscreen_context':('relationship','context.offscreen'),
'motion_rendering':('camera','image.motion'),'camera_movement':('camera','camera.movement'),
'hair_style':('appearance','hair.style'),'hair_color':('appearance','hair.color'),
'skin_finish':('appearance','skin.finish'),'age_presentation':('age','age.presentation'),
'contact_point':('relationship','contact'),'character_intent':('character_response','character.intent'),
'narrative_phase':('timing','narrative.phase'),'narrative_core':('event','narrative.core'),
'lighting':('lighting','lighting.setup'),'light_direction':('lighting','lighting.direction'),
'light_quality':('lighting','lighting.quality'),'light_color':('lighting','lighting.color'),
'light_intensity':('lighting','lighting.level'),'color_grading':('color','grading'),
'garment_detail':('appearance','garment.detail'),'garment_fit':('appearance','garment.fit'),
'garment_state':('appearance','garment.state'),'wardrobe_style':('appearance','wardrobe.style'),
'wearable_accessory':('appearance','accessories'),'genre':('style','genre'),
'body_orientation':('pose','body.orientation'),'hand_pose':('pose','hands.pose'),
'eye_detail':('appearance','eyes.structure'),'gaze_direction':('expression','gaze.direction'),
'gaze_engagement':('relationship','gaze.engagement'),'facial_geometry':('body_geometry','face.geometry'),
'visible_text':('text','text'),'environment_detail':('setting','environment.detail'),
'space_condition':('setting','space.state'),'background_element':('setting','background.elements'),
'situation_context':('event','situation'),'occasion_context':('event','occasion'),
'calendar_context':('timing','calendar'),'time_of_day':('timing','timing.time_of_day'),
'historical_period':('timing','timing.era'),'aesthetic_trend':('style','style.aesthetic'),
'film_emulation':('style','rendering.film'),'image_artifact':('camera','image.artifact'),
'image_detail':('camera','image.detail'),'grain_profile':('style','image.grain'),
'lens_artifact':('camera','optics'),'lens':('camera','lens'),'exposure':('camera','image.exposure'),
'depth_of_field':('camera','image.depth_of_field'),'format':('format','format'),
'capture_configuration':('camera','capture.configuration'),'capture_context':('camera','capture.context'),
'staging_degree':('style','capture.staging'),'world':('concept','world'),
'concept_tension':('concept','concept.contrast'),'surreal_concept':('concept','concept.surreal'),
'surreal_physics_detail':('concept','surreal.physics'),'reality_anchor':('concept','concept.anchor'),
'sensory_cue':('viewer_outcome','sensory.cue'),'reflection_logic':('composition','reflection'),
'shadow_relation':('lighting','shadow.relation'),'subject_count':('count','subject.count'),
'spatial_depth':('composition','spatial.depth'),'visual_density':('composition','layout.density'),
'visual_hierarchy':('composition','layout.hierarchy'),'body_region':('body_geometry','body.region'),
'body_form':('body_geometry','body.form'),'silhouette_proportion':('body_geometry','body.proportion'),
'species_marker':('species','species'),'anatomical_connection':('body_geometry','body.connection'),
'body_marking':('appearance','skin.marking'),'skin_condition':('appearance','skin.state'),
'skin_tone':('appearance','skin.tone'),'body_hair':('appearance','body.hair'),
'footwear':('appearance','footwear'),'wardrobe_layering':('appearance','wardrobe.layers'),
'medium':('style','media'),'procedure_step':('action','procedure.step'),
'viewer_position':('viewer_outcome','viewer.position'),'social_cue':('relationship','social'),
'publication_caption_context':('text','publication.caption'),'platform_framing':('framing','platform.framing'),
'aftermath_trace':('material','trace'),'crowd_density':('setting','crowd.density'),
'scale_relation':('body_geometry','scale.relation'),'gender_presentation':('appearance','presentation.gender'),
'declared_person_background':('identity','identity.background'),
'lip_finish':('appearance','lips.finish'),'lip_color_placement':('appearance','lips.color'),
'eye_makeup_line':('appearance','makeup.eyeliner'),'eyeshadow_style':('appearance','makeup.eyeshadow'),
'lash_style':('appearance','lashes'),'brow_style':('appearance','brows'),
'makeup_style':('appearance','makeup.style'),'makeup_contour':('appearance','makeup.contour'),
'makeup_decoration':('appearance','makeup.decoration'),'makeup_wear_state':('appearance','makeup.state'),
'cheek_makeup':('appearance','makeup.cheek'),'complexion_coverage':('appearance','makeup.coverage'),
'facial_hair':('appearance','face.facial_hair'),'nail_appearance':('appearance','nails'),
'adult_presentation_context':('sexual_tone','presentation.adult'),'fetish_styling':('sexual_tone','presentation.fetish'),
}
def save(start, lines):
 packet=json.loads((HERE.parent/'packets'/f'{start:05d}-250.json').read_text())
 path=HERE/f'review_01250_02250_{start:05d}_{start+250:05d}.json'
 rows=[]
 for line in lines.strip().splitlines():
  n,meaning,decls,boundary=line.split('|'); n=int(n); cid=packet['ids'][n-start]
  record=packet['records'][cid]; assert record['record_kind']=='visual_option'; assert 'realizations' not in record
  facts=[];roles={}
  for decl in decls.split(';'):
   tag,owner,suffix=decl.split(':'); tag,field=(tag.split('@') if '@' in tag else (tag,'en'));dim,prefix=P[tag]
   fact=dict(pointer='/content/'+field,quote=record['content'][field],dimension=dim,target=owner,property=prefix+'.'+suffix)
   if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=C[tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=meaning,evidence=[])
   roles[tag]['evidence'].append(fact); facts.append(dict(**fact,realization_id='base'))
  rows.append(dict(candidate_id=cid,meaning_summary=meaning,recommended_kind='visual_option',corrections=[],roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=[],status='approved',all_roles_considered=True))
 existing=json.loads(path.read_text())['decisions'] if path.exists() else []
 assert not set(x['candidate_id'] for x in existing)&set(x['candidate_id'] for x in rows)
 rows=existing+rows
 d.write(path,dict(decisions=rows))
 data=d.source()
 for i,row in enumerate(rows,1):
  expanded=dict(d.binding(data,row['candidate_id']) | row,schema=d.SCHEMA,reviewer='Codex',review_method='codex_direct_source_read',independent_human_review=False,packet_sha256=d.c.digest(packet),authored_decision=dict(file=str(path.relative_to(d.ROOT)),item=i,sha256=d.c.digest(row)))
  d.validate_decision(expanded,data)
 print(path.name,len(rows),'locally valid')
