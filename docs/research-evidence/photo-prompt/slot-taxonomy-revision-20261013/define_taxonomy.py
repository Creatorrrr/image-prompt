"""Authored taxonomy specification and reference coverage; offline maintenance only."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_corpus as c
import prompt_generator as g

# A family is a display aid, never a parent search node. Definition and scope
# are authored here; positive corpus documents never include these tag texts.
DEFINITIONS = """
medium|Physical photographic acquisition or display medium and the image-bearing substrate.|image|style|media.,substrate.,rendering.medium|film,print,negative,transparency,digital,image-bearing
genre|Photographic genre and the conventions of the work, distinct from equipment and world rules.|context|style|genre.,style.genre|photography,photographic,editorial,reportage,portrait,documentary
subject|The primary declared visible entity or entities that the photograph is about.|entity|subject|subject.,entity.,object_inventory|subject,person,adult,animal,object,tree,sculpture
declared_person_background|Explicitly declared personal origin or background used as context, never inferred from appearance.|context|identity|identity.background,identity.origin|from,origin,background,출신
presentation_style|Visible personal presentation and grooming, without inferring profession, personality or identity.|actor|appearance|presentation.,appearance.presentation|look,presence,styling,professional,unpolished
hair_style|Owned hair shape, length, arrangement and strand topology, separate from its color.|actor|appearance|hair.style,hair.shape,hair.length,hair.structure,hair.topology,hair.strands|hair,braid,fringe,bob,머리
hair_color|Color and color placement bounded to the declared hair regions.|actor|appearance|hair.color,hair.base_color,hair.hue,hair.pigment|hair color,colored hair,blonde,brunette,머리 색
makeup_style|A coherent combination of cosmetic treatments, distinct from an isolated cosmetic component.|actor|appearance|makeup.style,makeup.overall,face.makeup.style|makeup,cosmetic,화장
expression|Observable facial or eye-area response belonging to one declared actor, not a proven private emotion.|actor|expression|face.expression,expression.,eyes.expression|smile,expression,mouth,eyes,표정
attire_context|Declared role, culture, era or ceremony informing attire, separate from general garment construction.|context|appearance,role|wardrobe.context,wardrobe.cultural,wardrobe.role,attire.|costume,uniform,ceremonial,traditional,cosplay
wardrobe_style|Overall outfit combination and styling of a declared wearer, distinct from garment details.|actor|appearance|wardrobe.ensemble,wardrobe.style,wardrobe.outfit|outfit,wardrobe,dress,shirt,clothing
adult_presentation_context|Explicitly selected adult presentation context; adulthood alone is not sexual styling.|context|sexual_tone|sexual_tone.,presentation.adult|adult-only,suggestive,mature,adult fashion
action|A declared actor or object performing one concrete activity at the selected instant.|entity|action|action.,activity.,operation.|holding,playing,walking,working,performing,hand
capture_context|Purpose, access, observational circumstances and recording context of photography, not apparatus geometry.|context|camera,role|capture.context,capture.purpose,record.context|capture,record,photography,documentary,snapshot
prop|An explicitly owned scene object serving a declared role; placement and state are separate properties.|object|subject,role|props.,prop.,objects.,object_inventory|object,prop,tool,device,instrument,cabinet
fetish_styling|An explicitly selected fetish styling context with appropriate adult scope, not a material-only inference.|context|sexual_tone|sexual_tone.fetish,presentation.fetish|fetish,페티시
publication_caption_context|Context of an external publication caption and how it frames interpretation, not text inside the image.|context|viewer_outcome,text|publication.caption,caption.context|caption,comment,publication,캡션
location|Physical place and structural setting of the scene, distinct from use state or world rules.|environment|setting|setting.location,location.,spatial_structure.,architecture.|room,street,place,hall,window,landscape
world|Persistent fictional or declared world rules, institutions and systems underlying the scene.|context|setting,concept|world.,setting.world|world,system,speculative,coexistence,세계
lighting|A coherent illumination setup combining source, spatial placement and receiving surfaces.|light|lighting|lighting.setup,lighting.configuration|light,illumination,lighting,glow,조명
light_direction|Incident light direction relative to a declared receiver and coordinate frame.|light|lighting|lighting.direction,light.direction,illumination.direction|side light,front light,backlight,overhead,from the left,from the right
light_type|Light-source type and emission mechanism, distinct from exposure trails and image artifacts.|light|lighting|lighting.source,lighting.type,source.light,emission.|lamp,flash,headlight,neon,fluorescent,light source
light_intensity|Level of illumination reaching a declared receiver, distinct from recorded exposure and tone mapping.|light|lighting|lighting.intensity,lighting.level,illumination.level|illumination,dim light,bright light,light intensity
light_shape|Spatial distribution of light, highlights and shadow boundaries on specified receiving surfaces.|light|lighting|lighting.pattern,lighting.shape,lighting.shadow,shadow.boundary|dappled,sliver,shadow,light pattern,highlight
camera_type|Declared acquisition device class, distinct from its mounting and from the image's imitation of a device look.|camera|camera|camera.type,capture.device_type,apparatus.type|camera,bodycam,cctv,scanner,rig,webcam
camera_direction|Camera viewing axis and roll relative to the subject, distinct from height, distance and body orientation.|camera|camera|camera.direction,camera.angle,camera.roll,view.direction|view,angle,frontal,oblique,over-the-shoulder,roll
composition|Arrangement of declared elements and negative space within one frame.|image|composition|layout.,composition.,placement.|frame,arrangement,negative space,composition,layer
subject_framing|Inclusion, crop and visibility of named subjects or body regions, with explicit owner and participant count.|image|framing|framing.,frame.coverage,body.framing,subject.visibility|frame,crop,visible,includes,preserving
lens|Declared lens optics and projection characteristics, distinct from camera distance and chosen focus planes.|camera|camera|lens.,camera.lens|lens,fisheye,telephoto,wide-angle,anamorphic
focus|Placement and priority of the focus plane and relative sharpness of named planes.|image|camera|focus.,camera.focus,image.focus|focus,sharp,blurred,softer,선명
physical_motion|Physical motion or rest of declared actors, objects and materials, separate from recorded streaks or shake.|entity|action|motion.,movement.,body.motion,material.motion|motion,moving,rest,still,wind,flow
color|Owned local colors and bounded color arrangements, separate from whole-image grading.|entity|color|color.,local_color.,surface.color|color,hue,palette,red,blue,green,색
mood|Emotional atmosphere or proposed affective reading of the scene, not a measured state of air or a proven private emotion.|context|atmosphere|mood.,affect.,scene.mood|mood,tension,intimate,serene,calm,정서
surreal_concept|Explicitly intended departure from ordinary reality through one identifiable scene rule.|context|concept|concept.surreal,surreal.|impossible,surreal,unreal,초현실
reality_anchor|A declared ordinary reference whose relation makes a selected extraordinary concept legible.|entity|concept|concept.anchor,reference.reality|anchor,reference,rim,surface,ordinary
scale_relation|Comparative size relation between explicitly identified entities with a stated depth or perspective basis.|entity|body_geometry|scale.,size.relation,body.scale|larger,smaller,scale,height,size,giant
surreal_physics_detail|Local observable consequence of a selected impossible rule, distinct from ordinary coherence checks.|entity|concept|surreal.physics,concept.physical_rule|transmutation,impossible,fictional,shifting,shared-border
texture|Physical surface organization, roughness and repeated structure, not image-plane grain, compression or air particles.|surface|material|surface.texture,texture.,surface.weave,material.texture|texture,stitch,weave,rough,grain structure,질감
format|Image aspect ratio and output or display container, distinct from crop-safe composition and media appearance.|image|format|format.,image.aspect_ratio,image.container|aspect ratio,square,vertical,format,frame
film_emulation|A coherent visual emulation of a named film or photographic medium, without claiming the medium was actually used.|image|style|rendering.film,style.film,film.|film,halation,rolloff,consumer-film,필름
weather|Declared weather and its observable effects, separate from airborne material and unsupported causal inference.|environment|atmosphere|weather.,environment.weather|rain,snow,wind,fog,weather,날씨
time_of_day|Time within a day or natural-light cycle; event stage and calendar occasion are separate.|context|timing|timing.time_of_day,time.day_phase|dawn,morning,noon,afternoon,twilight,night
wearable_accessory|Accessory visibly worn by a declared owner, with attachment and location preserved.|actor|appearance|accessories.,wearable.,jewelry.|necklace,pendant,earring,glasses,ornament,accessory
facial_hair|Facial hair form, length and distribution, including a visibly shaved state.|actor|appearance|face.facial_hair,facial_hair.,beard.,mustache.|mustache,beard,stubble,shaven,goatee
surface_material|Declared surface material and observable optical response; chemical identity and performance require separate context.|surface|material|surface.material,surface.optical,surface.finish,material.|glass,metal,leather,fabric,surface,material
aesthetic_trend|Visual aesthetic movement or stylistic practice, distinct from an entire plot, institution or world system.|context|style|style.aesthetic,style.trend,aesthetic.|aesthetic,style,sensibility,visual,미감
relational_action|Concrete interaction between explicitly declared participants or participant and object.|entity|action,relationship|action.interaction,relation.action,interaction.|handoff,offering,conversation,together,listener,contact
prop_placement|Position and orientation of owned props relative to named actors, surfaces and boundaries.|object|composition,pose|props.placement,prop.position,prop.orientation,objects.position|held,beside,between,horizontal,pocket,encircles
participant_role|Explicit role of another participant, not inferred identity, occupation or relationship from appearance.|context|relationship,role|relationship.role,participant.role|partner,rival,colleague,family,participant
gaze_target|Target of the declared actor's gaze, with head orientation and eye state treated separately.|actor|expression|gaze.target,eyes.gaze_target|gaze toward,looking at,gaze tracking,시선 대상
body_orientation|Orientation of body axes and relative rotations of connected body regions.|actor|pose|body.orientation,body.rotation,body.pelvic_tilt,pose.orientation|turn,rotation,yaw,tilt,orientation,rotates
proxemics|Physical spacing and access barriers between declared participants, without automatically inferring intimacy or intent.|entity|relationship|relationship.distance,proxemics.,spacing.|distance,gap,between,across,closer,threshold
contact_point|Explicit contact, support or occlusion relation with each endpoint and owner identified.|entity|relationship|contact.,body.contact,support.,relation.contact|contact,touch,rests on,support,holds,occludes
character_intent|Explicit character goal or intended response used as narrative context, not a proven private mental state.|context|character_response|character.intent,intent.|resolve,intent,refusing,goal,의도
character_contrast|Contrast between a declared character's visible bearing, local response, role or status.|context|character_response|character.contrast,response.contrast|contrasts,contradiction,denial,authority,guarded
viewer_position|Observer's declared position and participation relation in the scene, separate from geometric camera settings.|context|viewer_outcome|viewer.position,viewer.role|viewer,viewpoint,observer,confidant,관찰자
narrative_phase|Selected instant within an explicitly declared event, distinct from clock time or inferred chronology.|context|timing|timing.event_phase,narrative.phase|before,after,mid,phase,first,reveal
species_marker|Anatomical species cues owned by a declared subject, distinct from detachable costume ornaments.|actor|species|species.,body.species,body.ear_structure,body.tail|ears,tail,fur,wing,antennae,species
transformation_stage|Observable stage of an explicitly selected transformation in body, form or material.|entity|timing,body_geometry|transformation.,timing.transformation_stage|transformation,mid-shift,transition,metamorphosis,dissolving
procedure_step|One identified step in a declared procedure, not a claim that a sequence was observed in one still image.|context|action,timing|procedure.,process.step|step,verify,inspect,record,measure,process
prop_state|Owned object's current use, attachment, readiness, damage or arrangement state, with occupational context optional.|object|role|props.state,prop.state,objects.state|in use,secured,set-down,worn,sorted,folded,open
social_cue|Visible reactions, attention or allocation relations supporting a declared social reading.|context|character_response,relationship|social.,response.social|audience,bystander,stares,access,allocation,presenter
reflection_logic|Correspondence or intended discrepancy between an owned physical object and its reflected image.|entity|composition|reflection.,image.reflection|reflection,mirror,reflected,puddle,inverted
camera_height|Camera height relative to a declared reference, distinct from viewing axis and distance.|camera|camera|camera.height,view.height|height,eye-level,chest-level,ground-level,above,below
sensory_cue|Observable proxy for a proposed touch, heat, smell or sound interpretation, without claiming the sensation was measured.|entity|viewer_outcome|sensory.,perception.cue|fingertips,steam,breath,heat haze,vibration,pulse
facial_geometry|Owned facial shape, local anatomical geometry and proportions, separate from cosmetic contour or skin finish.|actor|body_geometry|face.shape,face.geometry,face.proportion,body.face|face,forehead,jaw,cheek,nose,earlobe
anatomical_connection|Ownership and continuity, articulation or intended separation of anatomical parts.|actor|body_geometry|body.connection,body.topology,anatomy.connection,topology.|joins,connect,root,emerging,continuous,attached
body_region|Named anatomical region or selected body part, distinct from the obligation to prove its visibility.|actor|body_geometry|body.region,anatomy.region,body.part|region,torso,forearm,wrist,nape,anatomical
aftermath_trace|Owned physical residue of an explicitly declared prior event, distinct from an arbitrary surface state or ongoing process.|entity|timing,material|trace.,aftermath.,surface.event_trace|residue,trace,after-event,discoloration,completion
apparatus_pov|View through an identified aperture, optical apparatus or observation surface.|camera|camera|apparatus.view,view.aperture,view.optical_path|through,peephole,keyhole,field of view,observation mirror
complexion_coverage|Opacity and region coverage of the owned complexion cosmetic layer.|actor|appearance|makeup.coverage,complexion.coverage|complexion,coverage,concealment,cosmetic layer
brow_style|Owned eyebrow shape, strand arrangement, grooming or cosmetic line.|actor|appearance|brows.,eyebrows.,makeup.brows|brow,eyebrow,眉,눈썹
lip_finish|Optical surface finish of the owned lips, separate from pigment placement and lip anatomy.|actor|appearance|lips.finish,lip.finish,makeup.lip_finish|lip,gloss,satin,matte,balm
eyeshadow_style|Cosmetic pigment or shimmer distribution on selected eyelid regions.|actor|appearance|makeup.eyeshadow,eyelids.makeup|eyeshadow,eyelid,crease,lid,아이섀도
eye_makeup_line|Path and boundary of cosmetic eyeliner around the declared eye.|actor|appearance|makeup.eyeliner,eyes.eyeliner|eyeliner,tightline,kohl,wing liner,아이라인
lash_style|Owned lash length, distribution, separation and mascara treatment.|actor|appearance|lashes.,eyelashes.,makeup.lashes|lash,mascara,속눈썹
cheek_makeup|Placement and distribution of cosmetic pigment on the declared cheek area.|actor|appearance|makeup.cheek,cheeks.makeup,makeup.blush|blush,cheek makeup,cosmetic,볼 화장
makeup_contour|Cosmetic contour and highlight placement across facial planes, separate from actual facial geometry.|actor|appearance|makeup.contour,makeup.highlight,face.cosmetic_contour|contour,strobing,bronzed,cosmetic,highlight
lip_color_placement|Bounded lip pigment regions, opacity, concentration and color transitions.|actor|appearance|lips.color,lip.color,makeup.lip_color|lip pigment,lip color,lip line,vermilion,ombre lip
makeup_decoration|Cosmetic painted or attached skin decoration, distinct from natural markings and garment ornament.|actor|appearance|makeup.decoration,skin.cosmetic_decoration|cosmetic,face gem,decal,foil,painted,ornament
makeup_wear_state|Current distribution, transfer or loss of an owned cosmetic layer, without inferring elapsed time or cause.|actor|appearance|makeup.state,makeup.wear|makeup,worn,tear track,pigment,coverage loss
skin_finish|Optical finish and microtexture of the owned skin surface, not body hair, geometry or private health state.|actor|appearance|skin.finish,skin.texture,skin.optical|skin,pores,sheen,skin texture,피부
eye_detail|Owned local eye structure, iris color and surface appearance, distinct from gaze and surrounding cosmetics.|actor|appearance|eyes.structure,eyes.iris,eyes.color,eye.|iris,pupil,eye,안구
body_marking|Bounded natural, declared or applied markings on an owned body surface.|actor|appearance|skin.marking,body.marking,skin.pigment,skin.scar|mark,mole,scar,pigment,patch,tattoo
lens_artifact|Image effects arising along the optical path, distinct from physical scene particles and encoding damage.|image|camera|optics.,image.optical_artifact,lens.artifact|flare,bloom,halation,vignette,aberration,lens
gaze_engagement|Declared visual engagement with the camera or another participant, separate from mere eye direction or closure.|actor|expression,relationship|gaze.engagement,eyes.engagement|eye contact,looking past,engagement,avoiding the camera
hand_pose|Static shape and articulation of owned hands and fingers, with support and contact represented separately.|actor|pose|hands.pose,hand.pose,fingers.pose,body.hand_pose|hand,finger,palm,thumb,손
skin_condition|Current observable skin state, separate from durable markings, cosmetic layers and unproven diagnosis.|actor|appearance|skin.state,skin.condition|skin,sweat,flushed,damp,reddened,puffy
ambient_particle|Distinct airborne particles or droplets with spatial distribution, not particle-free atmospheric attenuation.|environment|atmosphere|air.particles,particles.,atmosphere.particles|particle,droplet,pollen,spray,motes
grain_profile|Grain or stochastic noise distribution on the image plane, not physical material grain or airborne dust.|image|style,camera|image.grain,image.noise,rendering.grain,grain.,noise.|film grain,digital noise,chroma noise,luminance noise,입자감
garment_detail|Construction, topology, trim and local form owned by the garment, distinct from anatomy and material identity.|object|appearance|wardrobe.,garment.,clothing.|garment,sleeve,cuff,hem,neckline,skirt,cloth
companion_animal|A separately declared animal participant accompanying the primary subject, with count and ownership explicit.|entity|subject,relationship|participant.animal,companion.animal|companion,pet,perched,cat,dog,dove
color_grading|Image-wide or specified tonal-band color and tone transformations, preserving locked local colors.|image|color|grading.,image.color,image.tone,rendering.color|grade,grading,tonal,rolloff,shifted color,색 보정
footwear|Owned footwear type, construction and appearance, with wearing versus standalone object role explicit.|object|appearance|footwear.,wardrobe.footwear|shoe,boot,sandal,heel,footwear,신발
silhouette_proportion|Owned body or clothed silhouette proportions, with body and garment carriers explicitly distinguished.|actor|body_geometry|body.proportion,body.silhouette,wardrobe.silhouette,silhouette.|proportion,silhouette,waist,torso,hips,비례
space_condition|Current use, preparation, maintenance or damage state of the place, distinct from structural location.|environment|setting|setting.condition,space.state,environment.state|space,place,abandoned,preparation,damage,cleanup
crowd_density|Spatial occupancy and density of a declared group within the frame, with actor counts preserved.|entity|setting,count|crowd.,group.density|crowd,dense,group,packed,cluster
situation_context|Concrete local circumstances explaining the scene's event, distinct from genre, world rules and a named occasion.|context|event,setting|situation.,scene.situation|situation,scene,waiting,preparing,service,상황
occasion_context|Explicit occasion, ceremony or scheduled event shaping the scene, distinct from any arbitrary process step.|context|event,timing|occasion.,event.occasion|ceremony,festival,graduation,occasion,release,행사
body_pose|Whole-body posture, support and articulation of a declared subject.|actor|pose|body.pose,pose.,body.support|seated,standing,kneeling,lying,pose,pelvis
shot_scale|Extent of subject coverage relative to the photograph's field, without equating it to focal length or physical distance.|image|framing|shot.scale,framing.shot_scale|shot,close-up,wide,full-length,waist-up
platform_framing|Crop-safe and interface-safe placement for a declared output platform, separate from aspect ratio.|image|framing,composition|platform.framing,layout.safe_area,frame.crop_safe|safe,crop,profile-picture,lower-third,platform
narrative_core|Central event, problem or relationship organizing the scene, distinct from a world system or a title alone.|context|concept,event|narrative.core,scene.central_event|narrative,event,problem,relationship,core
concept_tension|A declared conceptual contrast embodied by identifiable owners or states, not an unsupported abstract label.|context|concept|concept.contrast,concept.tension|versus,contrast,tension,opposition,contradiction
atmospheric_medium|Physical air, haze or fog and its spatial optical response, separate from emotion and distinct particles.|environment|atmosphere|air.medium,atmosphere.medium,environment.haze|haze,fog,air,attenuation,contrast across
capture_configuration|Arrangement of camera, operator, support, subject and reflecting surfaces during capture.|camera|camera|capture.configuration,camera.support,camera.operator,apparatus.configuration|camera,phone,mirror,self portrait,capture,device
"""

NEW = """
background_element|배경 요소|Declared secondary entities and structures in the background, separate from primary subjects and whole-place state.|environment|setting|background.elements,background.objects|background,behind,secondary,배경
environment_detail|환경의 국소 세부|Local wear, utilities and use traces owned by environmental surfaces or fixtures.|environment|setting,material|environment.detail,setting.detail,background.surface|peeling,scratch,stain,pipe,cable,dust,fixture
season|계절|Explicit seasonal setting or its declared observable cues, not a season inferred from one ambiguous object.|context|timing|timing.season,setting.season|spring,summer,autumn,winter,season,계절
historical_period|시대 배경|Explicit historical or future period as scene context, separate from nostalgic color grading.|context|timing,setting|timing.era,setting.era,world.period|century,1980s,1990s,contemporary,near future,era
calendar_context|달력 시점|Explicit day type or calendar interval such as weekday, weekend or eve, distinct from clock time and named occasion.|context|timing|timing.calendar,calendar.|weekday,weekend,sunday,eve,calendar,주말
subject_count|주체 수|Explicit number and grouping of declared visible or required participants.|entity|count|subject.count,actors.count,participant.count|one,two,three,group,count,인원
age_presentation|명시된 연령 표현|Declared age range and visible age presentation; real age is not inferred and adult restrictions remain intrinsic.|actor|age|age.,subject.age,appearance.age|adult,child,older,young,age,연령
gender_presentation|성별 표현|Explicit visual gender presentation without inferring sex, gender identity, personality or orientation.|actor|appearance|presentation.gender,appearance.gender|presentation,androgynous,masculine,feminine,성별 표현
skin_tone|피부 고유색|Owned skin color and local color variation, distinct from illumination, cosmetics and image grading.|actor|appearance,color|skin.color,skin.tone,complexion.color|skin tone,skin color,complexion,pigment,피부톤
body_hair|체모|Owned regional body-hair density, length and distribution, separate from skin finish and scalp hair.|actor|appearance|body.hair,skin.body_hair|body hair,regional hair,hair density,체모
garment_fit|의복 핏|Relation of a garment's volume and contour to its declared wearer, without inferring body shape from clothing.|object|appearance|wardrobe.fit,garment.fit|fitted,loose,oversized,fit,relaxed,핏
garment_state|의복의 현재 상태|Current garment wear, fastening, wetness or deformation, separate from construction and body state.|object|appearance|wardrobe.state,garment.state|wrinkled,damp,fastened,unbuttoned,worn,creased
wardrobe_layering|의복 레이어 관계|Explicit order, overlap and exposure of separately owned garment layers.|object|appearance|wardrobe.layers,garment.layering|layer,under,overlap,inner garment,레이어
light_quality|빛의 경계와 광질|Illumination softness, angular extent and resulting shadow transition, separate from intensity and image exposure.|light|lighting|lighting.softness,lighting.quality,light.angular_extent|soft light,hard light,diffused,shadow transition,광질
light_color|빛의 색|Color or color-temperature relation of declared illumination and its receivers, separate from local pigment or grading.|light|lighting,color|lighting.color,light.color,emission.color|colored light,warm light,cool light,red glow,green glow,temperature
exposure|기록 노출과 톤 범위|Recorded exposure, clipping and preservation of tonal information, separate from incident light level.|image|camera,color|image.exposure,camera.exposure,image.dynamic_range|exposure,clipped,clipping,underexposed,overexposed,shadow detail
camera_distance|카메라 거리|Physical camera-to-subject distance or declared observer separation, independent of shot scale and lens choice.|camera|camera|camera.distance,view.distance|arm's-length,distance,across the street,meters,metres
depth_of_field|심도|Depth extent of acceptable sharpness and background or foreground blur, separate from focus-plane selection.|image|camera|camera.depth_of_field,image.depth_of_field|depth of field,deep focus,shallow,background blur,bokeh
spatial_depth|장면의 깊이 구조|Depth ordering, overlap and perspective relations among foreground, middle distance and background owners.|image|composition|spatial.depth,composition.depth,layout.depth|foreground,midground,background,depth,perspective,overlap
motion_rendering|영상에 기록된 움직임|Image-plane freezing, streaks or blur from declared motion and capture, separate from physical action itself.|image|camera|image.motion,camera.motion_rendering|motion blur,streak,motion smear,frozen motion,panning
camera_movement|카메라 움직임|Declared camera movement or support stability during capture, separate from subject movement and its recorded blur.|camera|camera|camera.movement,camera.stability|camera shake,camera movement,panning,tripod,handheld
image_artifact|매체와 인코딩 흔적|Encoding, scanning, signal or processing artifacts on the image plane, separate from optical effects and scene surfaces.|image|camera,style|image.artifact,encoding.,signal.,rendering.artifact|jpeg,compression,noise line,color bleed,solarized,scratch
image_detail|영상 세부와 선명도|Recorded detail, acuity and edge rendering, distinct from physical realism claims and focus-plane placement.|image|camera,style|image.detail,image.acuity,image.sharpness|detail,sharpness,acuity,oversharpen,readable contours
staging_degree|촬영의 연출 정도|Declared posed, candid or directed presentation, without claiming unobserved camera awareness as fact.|context|style,role|capture.staging,presentation.staging|candid,staged,posed,spontaneous,observational,unposed
visual_hierarchy|시각적 읽기 순서|Declared order and prominence in which visible owners should be read.|image|composition|layout.hierarchy,composition.hierarchy|primary,secondary,prominent,read first,visual hierarchy
visual_density|시각적 정보 밀도|Amount and distribution of visible information, independent of the number of people.|image|composition|layout.density,composition.density|minimal,sparse,busy,cluttered,dense,empty
offscreen_context|화면 밖 맥락|Explicitly declared off-frame participants, events or space and their visible relation, not automatically added actors.|context|event,relationship|context.offscreen,narrative.offscreen|off-frame,offscreen,outside the frame,unseen,화면 밖
narrative_clue|서사 해석의 단서|An owned visible clue supporting a declared event interpretation, with observation and inferred chronology kept separate.|context|concept,timing|narrative.clue,scene.event_cue|trace,clue,readiness,umbrella,luggage,서사적 단서
visible_text|이미지 안의 글자|Explicit visible lettering, symbols and placement within the photograph, distinct from an external publication caption.|entity|text|text.,lettering.,sign.content|lettering,text,sign,menu,label,글자
shadow_relation|그림자 대응 관계|Declared caster, receiving surface and shadow correspondence, separate from reflection and light-level claims.|entity|lighting,composition|shadow.relation,lighting.shadow_relation|casts a shadow,cast shadows,shadow consistent,shadow source
"""

SPLITS = {
    "body_framing": ["subject_framing"], "partner_framing": ["subject_framing", "composition"],
    "distance_narrative": ["proxemics", "participant_role", "body_orientation"],
    "frame_anchor_medium": ["composition", "subject_framing", "depth_of_field", "grain_profile", "reflection_logic", "visible_text"],
    "quality": ["image_detail", "skin_finish", "image_artifact", "color_grading", "staging_degree"],
    "material": ["surface_material"], "motion": ["physical_motion", "motion_rendering", "camera_movement"],
}

VISUAL_CONTEXT_ROLES = {"genre", "attire_context", "adult_presentation_context", "fetish_styling",
    "publication_caption_context", "capture_context", "world", "aesthetic_trend", "mood", "surreal_concept",
    "character_intent", "character_contrast", "participant_role", "viewer_position", "narrative_phase",
    "procedure_step", "social_cue", "time_of_day", "occasion_context", "situation_context", "narrative_core",
    "concept_tension", "declared_person_background", "season", "historical_period", "calendar_context",
    "staging_degree", "offscreen_context", "narrative_clue"}

def make_row(name, description, owner, dims, paths, terms, ko, boundary):
    dimensions = dims.split(",")
    fields = list(dict.fromkeys(field for dimension in dimensions for field in g.DIMENSION_FIELDS.get(dimension, [])))
    if name in {"capture_context", "capture_configuration", "camera_type"}:
        fields = ["style", "event", "visual_priorities"]
    if name in {"subject_count", "participant_role", "offscreen_context"}:
        fields = ["subject", "event", "visual_priorities"]
    if name in {"prop", "prop_state", "prop_placement", "action", "physical_motion"}:
        fields = ["event", "subject"]
    if name in {"surreal_concept", "reality_anchor", "surreal_physics_detail", "concept_tension"}:
        fields = ["subject", "event", "setting", "visual_priorities"]
    return {
        "id": name, "description": description, "description_ko": ko + ": " + boundary,
        "dimensions": dimensions, "applicability": {},
        "semantic_role": "contextual" if name in VISUAL_CONTEXT_ROLES else "direct",
        "owners": [owner], "property_prefixes": paths.split(","),
        "evidence_terms": terms.split(","),
        "includes": [description], "excludes": [boundary], "neighbors": [],
        "core_fields": fields, "priority": "core" if name in g.CANDIDATE_PACK_CORE_SLOTS else "support",
    }

def build():
    audit = ROOT / "docs/research-evidence/photo-prompt/slot-taxonomy-audit-20261013"
    reviews = list(csv.DictReader((audit / "REVIEWS.tsv").open(), delimiter="\t"))
    old = json.loads((audit / "CATALOG-SNAPSHOT.json").read_text())
    renamed = {row["slot_id"]: row["proposed_name"] for row in reviews}
    renamed["motion"] = "physical_motion"
    reverse = {value: key for key, value in renamed.items() if value not in {"multiple_existing_roles", "proxemics_and_context"}}
    # The surviving owner of a merged role is its original non-retired role.
    reverse.update(subject_framing="subject_framing", surface_material="surface_material")
    review_by_id = {row["slot_id"]: row for row in reviews}
    catalog = {}
    for line in DEFINITIONS.strip().splitlines():
        name, description, owner, dims, paths, terms = line.split("|")
        origin = reverse[name]; review = review_by_id[origin]
        row = make_row(name, description, owner, dims, paths, terms,
                       review["role_definition_draft"], review["boundary_or_problem"])
        row["applicability"] = old[origin]["applicability"]
        row["priority"] = "core" if origin in g.CANDIDATE_PACK_CORE_SLOTS else "support"
        catalog[name] = row
    for line in NEW.strip().splitlines():
        name, ko, description, owner, dims, paths, terms = line.split("|")
        catalog[name] = make_row(name, description, owner, dims, paths, terms, ko,
            "대상·속성·관계를 실제로 표현할 때만 직접 역할로 판정하며, 맥락·원인·정체를 외관에서 확정하지 않는다.")
    for row in reviews:
        targets = SPLITS.get(row["slot_id"], [renamed[row["slot_id"]]])
        for target in targets:
            if target not in catalog:
                raise ValueError("missing target: " + target)
    decisions = {row["slot_id"]: {"action": row["action"],
        "targets": SPLITS.get(row["slot_id"], [renamed[row["slot_id"]]]),
        "rationale": row["boundary_or_problem"]} for row in reviews}
    families = [
        ["medium", "genre", "capture_context", "capture_configuration", "camera_type", "staging_degree"],
        ["skin_finish", "skin_condition", "skin_tone", "body_hair", "body_marking", "makeup_decoration"],
        ["texture", "surface_material", "grain_profile", "image_artifact", "lens_artifact", "ambient_particle", "atmospheric_medium"],
        ["lighting", "light_type", "light_direction", "light_intensity", "light_quality", "light_shape", "light_color", "exposure", "shadow_relation"],
        ["camera_direction", "camera_height", "camera_distance", "viewer_position", "body_orientation"],
        ["composition", "subject_framing", "shot_scale", "platform_framing", "format", "spatial_depth", "visual_hierarchy", "visual_density"],
        ["focus", "depth_of_field", "lens", "image_detail"],
        ["physical_motion", "motion_rendering", "camera_movement", "action", "body_pose", "hand_pose", "contact_point"],
        ["world", "narrative_core", "situation_context", "occasion_context", "aesthetic_trend", "concept_tension"],
        ["time_of_day", "season", "historical_period", "calendar_context", "narrative_phase", "transformation_stage", "procedure_step"],
        ["mood", "character_intent", "character_contrast", "social_cue", "participant_role", "proxemics", "offscreen_context", "narrative_clue", "aftermath_trace"],
        ["gaze_target", "gaze_engagement", "expression", "eye_detail"],
        ["garment_detail", "wardrobe_style", "attire_context", "garment_fit", "garment_state", "wardrobe_layering", "footwear", "silhouette_proportion"],
        ["color", "color_grading", "light_color", "skin_tone", "hair_color", "lip_color_placement"],
        ["visible_text", "publication_caption_context", "background_element", "environment_detail", "location", "space_condition"],
    ]
    for family in families:
        for name in family:
            catalog[name]["neighbors"] = sorted(set(catalog[name]["neighbors"]) | (set(family) - {name}))
    for name, row in catalog.items():
        if not row["neighbors"]:
            row["neighbors"] = sorted(other for other, spec in catalog.items()
                                      if other != name and set(row["owners"]) & set(spec["owners"]))
    coverage = {
        1: ["situation_context", "occasion_context", "staging_degree", "narrative_phase"],
        2: ["narrative_core", "narrative_phase", "character_intent", "participant_role", "narrative_clue"],
        3: ["location"], 4: ["time_of_day", "season", "historical_period", "calendar_context", "narrative_phase"],
        5: ["weather", "atmospheric_medium", "ambient_particle", "physical_motion"],
        6: ["background_element", "visual_density", "spatial_depth", "depth_of_field"],
        7: ["environment_detail", "space_condition", "prop_state"],
        8: ["subject", "subject_count", "age_presentation", "gender_presentation", "skin_tone", "facial_geometry", "hair_style", "makeup_style", "participant_role"],
        9: ["relational_action", "proxemics", "contact_point", "participant_role"],
        10: ["action", "physical_motion", "narrative_phase"], 11: ["body_pose", "body_orientation"],
        12: ["hand_pose", "action", "contact_point"], 13: ["gaze_target", "gaze_engagement", "expression"],
        14: ["expression"], 15: ["mood"],
        16: ["wardrobe_style", "attire_context", "garment_detail", "garment_fit", "garment_state", "wardrobe_layering", "surface_material", "color", "footwear"],
        17: ["prop", "prop_placement", "prop_state"], 18: ["light_type", "lighting"],
        19: ["light_direction", "light_shape"], 20: ["light_quality", "light_shape", "light_intensity"],
        21: ["exposure", "color_grading"], 22: ["color", "light_color", "skin_tone"],
        23: ["color_grading", "film_emulation"], 24: ["composition"], 25: ["shot_scale"],
        26: ["camera_height", "camera_direction"], 27: ["camera_direction"], 28: ["camera_distance"],
        29: ["lens", "camera_distance", "depth_of_field"], 30: ["focus", "image_detail"],
        31: ["depth_of_field"], 32: ["physical_motion", "motion_rendering", "camera_movement"],
        33: ["subject_framing", "composition"], 34: ["spatial_depth", "camera_distance", "atmospheric_medium"],
        35: ["medium", "camera_type", "capture_context", "genre"],
        36: ["grain_profile", "image_artifact", "lens_artifact", "image_detail", "skin_finish"],
        37: ["skin_finish", "garment_state", "anatomical_connection", "contact_point", "reflection_logic", "shadow_relation", "surface_material", "environment_detail"],
        38: ["capture_context", "capture_configuration", "genre"], 39: ["staging_degree", "gaze_engagement"],
        40: ["visual_hierarchy", "composition"], 41: ["visual_density", "crowd_density"],
        42: ["garment_state", "physical_motion", "subject_framing", "focus", "camera_direction", "motion_rendering"],
        43: ["offscreen_context", "gaze_target", "relational_action"],
        44: ["narrative_clue", "aftermath_trace", "prop_state", "environment_detail"],
        45: ["genre", "aesthetic_trend", "film_emulation", "staging_degree"],
    }
    for slots in coverage.values():
        if not set(slots) <= set(catalog):
            raise ValueError("reference coverage uses unknown slots")
    return catalog, decisions, coverage

if __name__ == "__main__":
    catalog, decisions, coverage = build()
    for name, value in [("TARGET-CATALOG.json", catalog), ("SLOT-DECISIONS.json", decisions), ("REFERENCE-COVERAGE.json", coverage)]:
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"target_slots": len(catalog), "source_slot_decisions": len(decisions),
                      "reference_groups": len(coverage), "added_roles": [line.split("|")[0] for line in NEW.strip().splitlines()]}, ensure_ascii=False))
