"""Compile reviewed research into optional candidates and narrow visual contracts."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
RESEARCH=HERE.parent/'realistic-background-20260912'
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
props=read(RESEARCH/'visual-proposals.json')['proposals']
spec='''
architecture_connectivity|composition|composition|the doorway is recessed within visible wall thickness;the path continues to the doorway threshold;service fixtures remain visibly attached to the building surface
use_trace_affordance|space_condition|setting|a recently used object rests on a stable working surface;the object is placed within the user's reach;the adjacent walking route remains clear
infrastructure_attachment|composition|composition|a drain cover fits flush within the walking surface;a service pipe follows the wall on visible supports;the fixtures leave a continuous passage through the space
repair_patch_locality|texture|material|one bounded repair patch is visible on the selected wall;the patch differs subtly from the surrounding paint;the wall joints remain continuous outside the patch
contact_wear_locality|texture|material|wear is localized to the gripping area of the selected handle;the adjacent unhandled surface remains comparatively intact;the handle keeps a continuous solid shape through the worn area
water_path_stain|texture|material|a drainage outlet is visible above the selected wall;a narrow runoff mark begins immediately below that outlet;the surrounding wall remains distinct from the localized water trace
material_response_contrast|texture|material|the matte surface has broad subdued shading;the adjacent metal surface carries a limited sharper highlight;the adjacent glass retains its distinct reflection and transmission
wet_dry_boundary|reflection_logic|lighting,material|one wet patch has a visible boundary against dry ground;the patch reflects the identified doorway light;grout lines or a grounded object interrupt that reflection
glass_reflection_transmission|reflection_logic|material,composition|a visible window frame locates the glass plane;the glass reflection corresponds to the opposite facade;the interior beyond the pane remains readable through another part of the glass
window_room_gradient|lighting|lighting|the window-facing tabletop receives brighter daylight;the deeper room surfaces remain at a lower light level;the subject and nearby objects share the window's light direction
practical_pool|lighting|lighting|the acting wall lamp is visible;the lamp produces a localized light pool on the adjacent surface;the pool fades into the surrounding room illumination
mixed_source_zones|lighting|lighting,color|the window-side sleeve receives cool window light;the lamp-side tabletop receives warmer local light;the source-bound color zones mix gradually where their illumination overlaps
bounce_owner|color|lighting,color|a muted green wall is close to the white sleeve;only the sleeve area facing that wall carries a faint green return;the other sleeve planes retain their neutral material color
shared_cast_shadow|lighting|lighting|the person casts a shadow connected to the supporting ground contact;the nearby post casts a shadow compatible with the same acting light;both shadows follow the geometry of the receiving pavement
soft_ground_contact|contact_point|pose,lighting|the supporting shoe sole meets the paving without a gap;soft local darkening remains directly beneath the sole;the supporting leg connects plausibly to the grounded shoe
exposure_priority|light_intensity|lighting|the specified subject detail retains readable midtones;the window or local light source remains brighter than the interior;the darker interior zones retain a distinct lower tonal level
highlight_shoulder|color_grading|color|bright surface tones approach white through a gradual transition;texture remains visible around the brightest area;the small brightest core remains distinct from the wider bright surface
distance_haze|ambient_particle|atmosphere|the nearest solid surfaces retain clear local contrast;the distant landscape shows lower contrast along the long viewing path;the atmospheric separation follows the landscape's depth order
readable_environment_focus|focus|camera|the selected subject plane remains crisp;the middle-distance environmental forms remain recognizable;the farther background loses fine detail consistently with its depth
depth_focus_continuity|focus|camera|the selected focus plane retains stable fine detail;near and distant forms leave focus according to their depth;occluding subject edges remain continuous without a cutout halo
foreground_occlusion|composition|composition|a nearby chair back continues beyond the lower frame edge;the chair back coherently overlaps part of the table;the subject's requested hand action remains visible beyond the overlap
scale_perspective|composition|composition,camera|near and distant doorways have consistent relative scale;the paving lines recede coherently through the depth;the doorway boundaries stay connected to their walls
local_motion_blur|motion|camera,timing|the moving hand carries a short directional blur;the stationary doorframe and torso remain comparatively clear;the moving hand remains connected to its arm
shared_wind_response|motion|atmosphere|loose hair bends while remaining attached at the scalp;the free jacket hem responds while the jacket's supported parts stay stable;exposed leaves respond compatibly while retaining their own stems and stiffness
low_light_noise|grain_profile|camera|darker neutral wall tones contain fine random luminance variation;the main object edges remain readable;the fine variation remains distinct from colored blocks and surface scratches
optional_lens_falloff|lens_artifact|camera|the outer image field darkens gradually from the center;the scene's own local illumination pattern remains readable;the falloff stays mild without becoming a solid border
optional_chromatic_fringe|lens_artifact|camera|a slight color offset appears on selected peripheral high-contrast edges;flat areas keep their original color structure;the fringe stays distinct from colored scene illumination
restrained_processing|color_grading|color,camera|architectural edges retain restrained local contrast;large surface tones keep gradual transitions;surface texture remains distinct without bright sharpening halos
clean_space_plausibility|space_condition|composition,material|the clean interior retains readable wall floor and frame joints;the furniture rests securely on the floor;matte and reflective materials retain distinct surface responses
spatial_density_variation|space_condition|setting|a small object cluster occupies the active working area;an adjacent usable surface remains clear;the main passage remains separate from the cluster
support_compression|contact_point|pose,material|the seated body meets a coherent support area on the soft cushion;a small cushion depression is localized beneath the load;the clothing folds follow the seated contact without penetrating the seat
glass_smudge_locality|texture|material|a faint smudge sits near the glass door pull;the mark remains attached to the glass plane;the rest of the pane retains readable reflection and transparency
vegetation_site_relation|composition|composition,setting|small plants emerge from soil at the paving edge;their stems remain connected to that ground area;the maintained walking surface remains clear beside the plants
coating_substrate_boundary|texture|material|a small worn edge interrupts the paint coating;exposed metal carries a different local highlight;the coating boundary follows the solid shape of the part
soft_source_environment|lighting|lighting|the acting large source produces broad shadow transitions;the subject and surroundings share compatible form shading;local support contact remains readable within the soft light
hard_source_environment|lighting|lighting|direct sunlight creates a crisp eave shadow;the shadow follows the wall and pavement geometry;the same light direction shapes the subject
film_grain_choice|film_emulation|camera,style|restrained irregular film-like grain remains visible;scene edges and material differences stay readable;the grain stays distinct from digital colored noise and film scratches
'''
specs={}
for line in spec.strip().splitlines():
 key,slot,dims,phrases=line.split('|');specs['rb_'+key]=(slot,dims.split(','),phrases.split(';'))
# Short, positive visual units support natural phrase retrieval. They are not
# aliases for hard activation and do not replace the complete selected contract.
cue_spec='''
architecture_connectivity|recessed doorway;wall thickness;pavement joints
use_trace_affordance|used cup;working surface;clear passage
infrastructure_attachment|drain cover;drainage grate;service pipe;visible brackets
repair_patch_locality|repair patch;paint boundary;continuous wall
contact_wear_locality|worn handle;gripping area;localized scuffs
water_path_stain|drainage outlet;runoff mark;localized water trace
material_response_contrast|matte surface;matte limestone;brushed steel;coated metal;glass panels;glass partition;material surfaces;surface reflections
wet_dry_boundary|wet pavement;dry ground;shallow puddle
glass_reflection_transmission|window glass;glass panels;glass reflection;interior transparency
window_room_gradient|window light;window daylight;deeper room;daylight gradient
practical_pool|wall lamp;local light;light pool
mixed_source_zones|mixed lighting;window light;warm lamp;overlapping illumination
bounce_owner|green wall;white sleeve;reflected color
shared_cast_shadow|cast shadows;ground contact;shadow direction
soft_ground_contact|shoe sole;contact shadows;grounded feet
exposure_priority|readable midtones;bright window;interior exposure
highlight_shoulder|highlight rolloff;bright surface;retained texture
distance_haze|distant landscape;distant mountain;far hills;lighter contrast;depth order
readable_environment_focus|environmental detail;middle distance;background detail;environmental portrait;spacious architectural view
depth_focus_continuity|focus plane;depth of field;continuous edges
foreground_occlusion|foreground chair;frame edge;partial overlap
scale_perspective|relative scale;receding lines;coherent perspective
local_motion_blur|moving hand;directional blur;stationary torso
shared_wind_response|loose hair;jacket hem;exposed leaves;gentle breeze
low_light_noise|low light;dark wall;luminance noise
optional_lens_falloff|image periphery;gradual darkening;optical falloff
optional_chromatic_fringe|peripheral edges;color offset;chromatic fringe
restrained_processing|architectural edges;tonal transitions;surface texture
clean_space_plausibility|clean interior;clean room;floor joints;matte materials;reflective materials
spatial_density_variation|object cluster;working area;clear surface
support_compression|soft cushion;seated contact;localized depression
glass_smudge_locality|glass door;door pull;faint smudge
vegetation_site_relation|rooted plants;paving edge;connected stems
coating_substrate_boundary|paint coating;exposed metal;worn edge
soft_source_environment|soft daylight;overcast morning;cloudy sky;diffuse illumination
hard_source_environment|direct sunlight;crisp shadow;receiving pavement
film_grain_choice|film grain;irregular grain;readable materials
'''
cues={'rb_'+line.split('|')[0]:line.split('|')[1].split(';') for line in cue_spec.strip().splitlines()}
reuse={'rb_wet_dry_boundary':'wet_surface_light_reflection_owner_relation',
 'rb_highlight_shoulder':'highlight_rolloff_tone_response',
 'rb_depth_focus_continuity':'shallow_depth_focus_falloff_relation',
 'rb_soft_source_environment':'soft_light_shadow_edge_relation',
 'rb_hard_source_environment':'hard_light_shadow_edge_relation'}
profiles=[];slots={};coverage=[]
core=read(RESEARCH/'core-keyword-map.json')['rows']
for p in props:
 pid=p['id'];slot,dims,units=specs[pid];definition='; '.join(units)
 expression=p['candidate_expression_en']
 if pid in {'rb_clean_space_plausibility','rb_distance_haze','rb_readable_environment_focus','rb_material_response_contrast'}:
  expression=definition[0].upper()+definition[1:]+'.'
 aliases=[p['label_ko'],pid.removeprefix('rb_').replace('_',' ')+' relation']
 keywords=[x['term'] for x in core if pid in x['proposal_ids']]
 # Generic labels are searchable candidate context, never exact profile activators.
 if pid not in reuse:
  profile={'id':pid,'category':'photographic_environment_relation',
   'activation':{'exact_terms':[definition], 'requires_adult_character':False,
       'semantic_discovery_requires_component_evidence':False},
   'semantics':{'definition':definition,'paraphrase_examples':[expression,*aliases],
     'visual_components':cues[pid],
     'contrast_examples':p['confusion_boundaries'],
     'claim_limits':['The selected owner and all components must be visible in one image.',
       'A depiction is not evidence of capture history, material diagnosis or geographic authenticity.',
       'The concrete objects are a selected manifestation, never defaults for a broad realism request.']},
   'concept_candidate':{'concept_terms':[*aliases,*cues[pid],*units]},
   'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
     'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
   'reject_substitutes':p['confusion_boundaries'],
   'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[]}}
  for i,phrase in enumerate(units,1):
   profile['authored_components']['components'].append({'id':f'component_{i}',
     'match_terms':[phrase],'evidence_field':f'component_{i}_phrase','evidence_terms':[phrase],
     'min_content_words':3,'instruction':'Show this selected relationship in the declared environment: '+phrase,
     'render_gate':{'id':f'vo_{pid}_{i}','review_scale':'native' if slot in ['texture','grain_profile','lens_artifact','contact_point'] else 'both',
       'description':phrase+'. All named owners must be visible in this image. Missing, ambiguous, substituted or partly realized evidence fails.'}})
  profiles.append(profile)
 entry={'id':pid+'_candidate','ko':p['label_ko'],'en':expression,'weight':0.5,
   'tags':['photographic_environment','realistic_background',slot],
   'aliases':aliases,'keywords':keywords,
   'embedding_text':p['label_ko']+'; '+expression+'; '+'; '.join(units),
   'concept_units':[p['label_ko'],*cues[pid],*units],
   'relations':[{'id':pid+'_owner_relation','type':'scene_bound_owner_relation',
     'subject':p['owner'],'object':'the selected connected environment and its visible receiving surfaces'}],
   'affected_dimensions':dims}
 slots.setdefault(slot,[]).append(entry)
 coverage.append({'proposal_id':pid,'runtime_profile_id':reuse.get(pid,pid),'disposition':'reuse_existing' if pid in reuse else 'new_profile',
   'slot':slot,'candidate_id':entry['id'],'source_ids':p['source_ids'],'evidence_level':p['evidence_level']})
bs=[];deferred_bundles=[]
authored_bundles=read(RESEARCH/'candidate-bundles.json')['bundles']
for bid,scenario,ids in [
 ('rbb_surface_focus','서로 다른 표면 반응과 읽히는 환경의 깊이',['rb_material_response_contrast','rb_readable_environment_focus']),
 ('rbb_landscape_depth','가까운 환경 형태와 먼 풍경의 깊이',['rb_distance_haze','rb_readable_environment_focus']),
]:
 authored_bundles.append({'id':bid,'scenario_ko':scenario,'required_if_this_bundle_is_explicitly_selected':ids,
  'do_not_infer':'These optional relationships preserve the frozen scene; they do not establish capture provenance.'})
for b in authored_bundles:
 ids=b['required_if_this_bundle_is_explicitly_selected']
 if b['id']=='rbb_dry_noon':ids=[pid for pid in ids if pid!='rb_clean_space_plausibility']
 if len({specs[pid][0] for pid in ids})!=len(ids):
  deferred_bundles.append({'id':b['id'],'reason':'same-slot joint adoption is not supported by the runtime policy'})
  continue
 bs.append({'id':b['id'],'primary_visual_proposition':b['scenario_ko'],
   'component_groups':[{'id':pid+'_component','visible_evidence':['; '.join(specs[pid][2])]} for pid in ids],
   'candidate_ids':[pid+'_candidate' for pid in ids],
   'candidate_slots':{pid+'_candidate':specs[pid][0] for pid in ids},
   'hard_profile_ids':[reuse.get(pid,pid) for pid in ids],
   'confusion_boundaries':[b['do_not_infer'],'The bundle is optional and cannot change locked intent dimensions.'],
   'source_keywords':[b['scenario_ko'],*ids],
   'relations':[{'id':b['id']+'_joint','type':'co_realized_in_one_environment','subject':'all selected component owners','object':'one coherent photographic space'}]})
ext={'schema_version':'photo-prompt-research-extension/v1','slots':slots,'visual_semantics':bs}
record={'record_id':'photo_prompt_realistic_background_extension','authored_source_sha256':digest(ext),
 'maintenance_only':{'research_path':str(RESEARCH.relative_to(ROOT)), 'coverage':coverage,
  'source_ids':sorted({s for p in props for s in p['source_ids']}),
  'source_support':'Research evidence supports physical distinctions; specific staging and generation effects are hypotheses.',
  'broad_policy':'realism, RAW, HDR, documentary, noise and weather labels alone never harden a relation',
  'reference_only_bundles':read(RESEARCH/'candidate-bundles.json')['bundles'],
  'deferred_bundles':deferred_bundles,
  'retrieval_revision':'Natural positive visual units; generic focus/depth/clean-interior owners. Two cross-slot relationship bundles. Calibrated after first three-arm exposure failure; not independent holdout validation.'}}
write(ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_realistic_background_extension.json',record)
ext['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
write(ASSETS/'photo_prompt_realistic_background_extension.json',ext)
write(ASSETS/'photo_prompt_visual_obligations_realistic_background.json',{
 'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1',
 'description':'Optional scene-bound environmental relationships; no universal realism style or capture-authenticity claim.',
 'profiles':profiles})
write(HERE/'source-coverage.json',{'new_profiles':len(profiles),'reused_profiles':reuse,'candidates':len(coverage),
 'bundles':len(bs),'rows':coverage,'render_status':'not_run'})
print(json.dumps({'new_profiles':len(profiles),'reused_profiles':len(reuse),'candidates':len(coverage),'bundles':len(bs)}))
