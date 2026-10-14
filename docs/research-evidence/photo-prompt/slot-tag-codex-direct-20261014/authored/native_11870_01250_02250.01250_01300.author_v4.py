"""Literal manual native draft 1250:1300. No registration, conversion or qualification.

P/E/C clauses below are authored independently from full source meaning, not copied
from old tags/effects. The serializer only repeats explicit per-string clause maps,
copies whole source snapshots, and calculates local provenance/shape checks.
"""
import copy, hashlib, json
from pathlib import Path

R=Path(__file__).resolve().parents[1]
P=Path(__file__).with_name('native_11870_01250_02250.01250_01300.inputs_v1.json')
B=Path(__file__).with_name('native_11870_01250_02250.01250_01300.ownbindings_v1.json')
assert hashlib.sha256(P.read_bytes()).hexdigest()=='bfc9e15238845982fd3b316d706759a1ba935ac3099a1dc3371ab811c02c09b9'
assert hashlib.sha256(B.read_bytes()).hexdigest()=='c3f6c5c5b899200eda2ae707554f00c87b6ebc1a58dfa6e4515b5300278a14f8'
I=json.loads(P.read_text()); OWN=json.loads(B.read_text())['bindings_by_cid']
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
# Each tuple explicitly states mode, typed value, dependencies and mutation scope.
# id,dimension,target,property,mode,namespace,value,requires,operation,receivers
def Pq(i,d,t,p,ns,v,req):return (i,d,t,p,'prerequisite',ns,v,req,None,None)
def Eq(i,d,t,p,ns,v,req,op,receivers):return (i,d,t,p,'effect',ns,v,req,op,receivers)
def Cq(i,d,t,p,ns,v,req):return (i,d,t,p,'context',ns,v,req,None,None)
def Sq(i,d,t,p,ns,v,req):return (i,d,t,p,'preservation',ns,v,req,None,None)
# Binding conditions are independently selected below; these are not whole-source
# condition copies or blanket intersections. Candidate intrinsic guards stay separate.
NONE={'subject_applicability':{}}
H={'subject_applicability':{'subject_categories':['human']}}
HP={'subject_applicability':{'subject_categories':['human'],'deny_domains':['product','jewelry','food','wildlife']}}
STYLE={'subject_applicability':{'subject_categories':['human'],'deny_domains':['documentary','craft','wildlife','product','jewelry','food']}}
SURF={'subject_applicability':{'subject_categories':['object','food','plant','environment','sign','human','animal'],'allow_domains':['product','jewelry','food','architecture','subculture_practice','worldbuilding_system','cjk_narrative_world'],'allow_domains_override_subject_categories':True}}
OBJ={'subject_applicability':{'subject_categories':['object','product','food']}}
def role(tag,refs,modes,conditions,weight,semantic_role,why):
 return {'tag':tag,'fact_ids':refs,'support_modes':modes,'conditions':conditions,'role':'optional','semantic_role':semantic_role,'weight':weight,'intent':why}
ROWS=[]
def row(n,meaning,contract,owners,clauses,units,roles,boundaries,pending,translations,binding_review):
 ROWS.append(dict(ordinal=n,meaning=meaning,application_contract_proposal=contract,owner_bindings=owners,clauses=clauses,unit_clause_map=units,roles=roles,rejected_boundaries=boundaries,pending=pending,translation_proposals=translations,own_binding_review=binding_review))

row(1250,'A face is portrayed briefly softening; the caught/tsundere reading does not establish private feelings or another observer.',
 'Apply only to the independently declared existing face bound to primary_face. Portray a fleeting softening expression; no new observer or prior event is introduced.',
 [('face','primary_face')],
 [Pq('face','expression','face','anatomy.face.presence','anatomy.face.presence/v1','present',[]),Eq('soft','expression','face','expression.face','expression.face/v1','fleeting_softening',['face'],'set_value',[])],
 {'en':['soft'],'ko':['soft'],'application_contract':['face','soft']},
 [role('expression',['soft'],['effect'],H,.82,'direct','Face expression is directly stated; source human guard remains intrinsic, unlike the old animal allowance.')],
 ['No affection, temperature, watcher identity, history or bodily action.'],[],{},
 'Old expression/H-or-animal/.82 is display applicability. Keep human-only source guard; do not extend this CID to animals through the old role condition.')
row(1251,'A tight face crop fills the image; the crop extent and dominant face layout are selected together.',
 'Use the independently declared existing image and face bound to image and primary_face. Select the tight face crop and face-filling layout without adding a face or changing its anatomy.',
 [('image','image'),('face','primary_face')],
 [Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Pq('face','expression','face','anatomy.face.presence','anatomy.face.presence/v1','present',[]),Eq('crop','framing','image','framing.shot_scale','framing.shot_scale/v1','tight_face_crop',['image','face'],'set_value',['face']),Eq('layout','composition','image','composition.dominant_subject','composition.dominant_subject/v1','face_fills_frame',['image','face'],'set_value',['face'])],
 {'en':['crop','layout'],'ko':['crop','layout'],'application_contract':['image','face','crop','layout']},
 [role('shot_scale',['crop'],['effect'],NONE,.8,'direct','Tight close-up extent is explicit.'),role('subject_framing',['crop'],['effect'],NONE,.8,'direct','The named face is the included/cropped subject.'),role('composition',['layout'],['effect'],NONE,.8,'direct','Face filling the frame is a stated dominant layout, not inferred solely from beauty.')],
 ['No lens focal length, focal plane, gender or cosmetic requirement.'],[],{},'Old composition .8 unrestricted is display-only; retain it for the actual layout, add separately evidenced crop roles with the same explicit face prerequisite.')
row(1252,'An exhausted-looking yet satisfied facial expression, without certifying fatigue or completed work.',
 'Apply only to the independently declared existing face bound to primary_face. Select the exhausted-but-satisfied facial expression without asserting a prior job or measured fatigue.',
 [('face','primary_face')],
 [Pq('face','expression','face','anatomy.face.presence','anatomy.face.presence/v1','present',[]),Eq('look','expression','face','expression.face','expression.face/v1','exhausted_but_satisfied',['face'],'set_value',[])],
 {'en':['look'],'ko':['look'],'application_contract':['face','look']},
 [role('expression',['look'],['effect'],H,1.,'direct','The source names the expression rather than worker identity.')],
 ['No physical exhaustion measurement, occupational role or completed event.'],[],{'ko':'지쳐 보이지만 만족스러운 표정'},'Old expression human/animal gate is display-only; source human guard is essential and remains. Weight 1 retained for explicit expression.')
row(1253,'A counter creates a formal sense of distance, but the distance endpoints are not supplied.',None,[],[],{},[],
 ['Do not invent two people, a customer/server pair, a camera observer or a specific barrier layout.'],
 ['The positive prose does not identify the separated endpoints; viewer_outcome is coarse and cannot simply become a spatial relation. Need matching original intent or explicit requester-grounded endpoints before a complete native inventory.'],{},
 'Old proxemics .75 unrestricted is a routing/display choice, not proof of two declared participants. No proposed replacement binding until endpoints and the actual relation effect are grounded.')
row(1254,'A red thread charm is tangled; nominal existence is not an instruction to add a new charm.',
 'Apply only to the independently declared existing thread charm bound to primary_prop. Keep its identity fixed and select its red color and tangled state; do not add a charm, holder, attachment or symbolic relationship.',
 [('charm','primary_prop')],
 [Pq('charm','subject','charm','prop.identity','entity.type/v1','thread_charm',[]),Eq('red','color','charm','color.local','color.local/v1','red',['charm'],'set_value',[]),Eq('tangle','role','charm','prop.state','prop.state/v1','tangled',['charm'],'set_value',[])],
 {'en':['red','tangle'],'ko':['red','tangle'],'embedding_text':['red','tangle'],'application_contract':['charm','red','tangle']},
 [role('prop',['charm'],['prerequisite'],H,.62,'direct','Declared charm identity supports object role; actual changes remain red/tangled.'),role('color',['red'],['effect'],H,.62,'direct','Local red belongs to the charm, not image grading.'),role('prop_state',['tangle'],['effect'],H,.62,'direct','Tangle is this object current arrangement, not an actor pose.')],
 ['No add_entity, fate bond, romantic relation or attachment site.'],[],{'ko':'엉킨 붉은 실 부적'},
 'Old prop .62 unrestricted display condition cannot remove candidate human-only use. New color/state share that intrinsic candidate restriction without inheriting unrelated human-specific prop-placement exclusions.')
row(1255,'A held object is near a subject with neutral presentation; English and Korean do not safely fix whose side/holder.',None,[],[],{},[],
 ['Do not choose the main actor as holder, merge holder and subject, invent an object, or turn holding/near placement into context.'],
 ['Object, holder and subject endpoints are unbound. Korean 자기 쪽 suggests self-side while English near the subject leaves relation ownership open. Need original SHA-matched whole entry or explicit endpoint contract; current empty effects cannot cover actual holding/placement.'],{},
 'Old prop_placement .82 human plus product/jewelry/food/wildlife exclusions is presentation-role policy, not evidence of owner identity. Typed holder/object/subject prerequisites would be essential to every later role; no automatic gate copy or new binding now.')
row(1256,'Gaze is directed toward a blank badge or an access card; blank scope and actual alternative remain unselected.',None,[],[],{},[],
 ['No simultaneous two props, text-bearing eye movement, invented card blankness, hand pose or office actor.'],
 ['English OR and shorter Korean branch do not provide a selected actual RID. Need explicit branch proposals preserving badge-versus-card and exact blank scope; root must approve source branching before complete gaze/target effects.'],{},
 'Old gaze_target .74 human domain exclusions are role policy. Source human guard is intrinsic. Badge/card identity and eye presence are exact future prerequisites, not inferred from that gate; no forced binding now.')
row(1257,'Light drizzle is selected, with an evaluative comment that an umbrella is barely necessary.',
 'Apply the stated light-drizzle weather to the independently declared scene bound to scene. Umbrella need is an evaluative description, not an instruction to add an umbrella or a safety conclusion.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('drizzle','atmosphere','scene','weather.precipitation','weather.precipitation/v1','light_drizzle',['scene'],'set_value',[]),Cq('umbrella','concept','scene','weather.umbrella_need_description','weather.umbrella_need_description/v1','barely_needs_umbrella',[])],
 {'en':['drizzle','umbrella'],'ko':['drizzle','umbrella'],'application_contract':['scene','drizzle','umbrella']},
 [role('weather',['drizzle'],['effect'],NONE,.82,'direct','Explicit precipitation type/intensity; no umbrella object follows.')],
 ['No exact rainfall quantity, umbrella carrier, no-risk certification or generic mist substitution.'],[],{},'Old weather .82 unrestricted is display-only and remains appropriate. Scene prerequisite plus actual weather effect prevents reclassifying selection as context.')
row(1258,'A person checks voltage with a tester while the source explicitly requires safe practice.',None,[],[],{},[],
 ['No invented probe placement, electrical endpoint, numerical voltage, PPE details or safety certification.'],
 ['Tester and checking action are stated, but the tested endpoint and the safety contract are not. The positive safely condition cannot be dropped or certified visually. Need requester-declared equipment/endpoint and independently grounded applicable safety protocol, or exact original-source clarification.'],{},
 'Old action weight1 has no binding guard. Source human use is intrinsic and must survive any future tool/relational role; safety is a whole-cue condition, not a removable display preference.')
row(1259,'A spread arrangement of tarot cards, without predicting a reading or adding a card set.',
 'Apply only to the independently declared existing tarot-card set bound to primary_prop. Keep that set identity fixed and select a spread arrangement; do not add cards, a reader, legible card text or divinatory efficacy.',
 [('cards','primary_prop')],
 [Pq('cards','subject','cards','prop.identity','entity.type/v1','tarot_card_set',[]),Eq('spread','role','cards','prop.state','prop.state/v1','spread_arrangement',['cards'],'set_value',[])],
 {'en':['spread'],'ko':['spread'],'embedding_text':['spread'],'application_contract':['cards','spread']},
 [role('prop',['cards'],['prerequisite'],H,.62,'direct','Declared card-set identity is retained.'),role('prop_state',['spread'],['effect'],H,.62,'direct','Spread is current arrangement; no unstated exact layout.')],
 ['No new cards, fixed count, fortune, reader action or specific geometry.'],[],{},'Old prop .62 unrestricted is display-only; intrinsic human use survives both proposed roles. Existing set identity is a typed prerequisite, not an add permission.')
row(1260,'K-beauty-influencer-like styling is selected as visible presentation, without assigning nationality or profession.',
 'Apply this presentation styling to the independently declared existing person bound to main_subject. Select the stated K-beauty-influencer-like appearance without changing identity, nationality, occupation or declaring any particular cosmetic placement.',
 [('person','main_subject')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Eq('styling','appearance','person','presentation.style','presentation.style/v1','k_beauty_influencer_like',['person'],'set_value',[])],
 {'en':['styling'],'ko':['styling'],'application_contract':['person','styling']},
 [role('presentation_style',['styling'],['effect'],STYLE,.8,'direct','Named visible presentation is an actual choice even without enumerated cosmetics.')],
 ['No Korean nationality, influencer employment, makeup placement or youth fact.'],[],{},'Old presentation human/domain limits are role-specific catalog scope, retained for this role. Independently source-human and existing-person prerequisites remain whole-cue obligations. Styling is effect, not context/no-op.')
row(1261,'Select a hotel-lobby physical setting.',
 'Select the stated hotel-lobby location for the independently declared scene bound to scene. This is a setting change, not an already-hotel prerequisite and not an instruction to add staff or guests.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('place','setting','scene','setting.location','setting.location/v1','hotel_lobby',['scene'],'set_value',[])],
 {'en':['place'],'ko':['place'],'phrase_en':['place'],'phrase_ko':['place'],'application_contract':['scene','place']},
 [role('location',['place'],['effect'],NONE,1.,'direct','An explicit physical place, including usage phrases.')],
 ['No luxury, receptionist, guest, era or country.'],[],{},'Old location1 unrestricted is display-only; retain explicit unrestricted role application, existing scene and actual setting mutation.')
row(1262,'A bid is announced with a gavel raised; the cue includes both announcing and raised-object presentation.',
 'Use the independently declared existing person and gavel bound to main_subject and primary_prop. Select the bid-announcing action and raised-gavel position; do not add a gavel, declare an occupation, prescribe words or assert a completed sale.',
 [('person','main_subject'),('gavel','primary_prop')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Pq('gavel','subject','gavel','entity.type','entity.type/v1','gavel',[]),Eq('announce','action','person','action.announcing','action.announcing/v1','announcing_bid',['person','gavel'],'set_value',['gavel']),Eq('raise','pose','gavel','props.placement','props.placement/v1','raised_by_declared_person',['person','gavel'],'relocate',['person'])],
 {'en':['announce','raise'],'ko':['announce','raise'],'application_contract':['person','gavel','announce','raise']},
 [role('action',['announce'],['effect'],H,.38,'direct','Announcing is explicit; no utterance invented.'),role('prop_placement',['raise'],['effect'],H,.55,'direct','Raised gavel has a stated owner relation, separately from announcing.')],
 ['No exact hand anatomy, auctioneer identity, price or sale success.'],[],{'ko':'의사봉을 들어 입찰을 선언하는'},'Old action .38 unrestricted does not remove source human guard. New placement has final142 unrestricted catalog scope but this CID remains human-only with explicit gavel/person prerequisites.')
row(1263,'A single face contrasts warm-looking eyes with a cold-looking mouth line; warmth is affective.',
 'Use only the independently declared existing face with its eyes and mouth, bound to primary_face. Select the contrasting warm-eye/cold-mouth expression; the terms are expressive qualities, not temperatures or private emotions.',
 [('face','primary_face')],
 [Pq('face','expression','face','anatomy.face.parts','anatomy.face.parts/v1',['eyes','mouth'],[]),Eq('contrast','expression','face','expression.face','expression.face/v1','warm_eyes_cold_mouth_line',['face'],'set_value',[]),Eq('contrast_relation','character_response','face','character.contrast','character.contrast/v1','warm_eyes_versus_cold_mouth_line',['face'],'set_value',[])],
 {'en':['contrast','contrast_relation'],'ko':['contrast','contrast_relation'],'application_contract':['face','contrast','contrast_relation']},
 [role('expression',['contrast'],['effect'],H,.82,'direct','Owned eye/mouth expressive qualities are explicit.'),role('character_contrast',['contrast_relation'],['effect'],HP,.7,'contextual','The declared contrast lies in the face; contextual role does not make selection a no-op.')],
 ['No temperature, measured kindness, private affection or changed anatomy.'],[],{},'Old expression H/A gate is display-only; source human is intrinsic. Additional contrast role keeps same actual expression effect and prerequisites, without importing unspecified whole-body traits.')
row(1264,'An overturned chair and a recently disturbed seat are selected as a visible aftermath-like arrangement.',None,[],[],{},[],
 ['Do not invent an attacker, a struggle, a previous event, or force seat to be the same chair component.'],
 ['Chair/seat identity relation is not explicit, Korean omits overturned, and no specific prior event is declared. Need exact whole-original clarification before choosing same versus separate object targets and before replacing empty effects. Generic narrative residue is not sufficient for the strict aftermath_trace spec.'],{},
 'Old aftermath_trace .72 domain override/human policy is role-specific, not an intrinsic source restriction or proof of an event. Do not copy it onto later prop/state roles. Recentness remains a source obligation if clarified.')
row(1265,'A declared saltwater surface has a sheen; no chemical measurement is established.',
 'Apply only to the independently declared existing saltwater surface bound to foreground_surface. Keep its declared saltwater identity fixed and select its visible sheen; do not infer concentration, temperature, cause or a new water body.',
 [('surface','foreground_surface')],
 [Pq('surface','material','surface','surface.material','surface.material/v1','declared_saltwater',[]),Eq('sheen','material','surface','surface.optical_response','surface.optical_response/v1','sheen',['surface'],'set_value',[])],
 {'en':['sheen'],'ko':['sheen'],'embedding_text':['sheen'],'application_contract':['surface','sheen']},
 [role('surface_material',['surface','sheen'],['prerequisite','effect'],SURF,.58,'direct','Declared material identity and optical response are distinct facts on the same selected surface.')],
 ['No salinity test, lighting source, temperature, exact roughness or location.'],[],{},'Old surface-material gate is role-only scope, expanded by final142 to allow declared human/animal carriers; this actual saltwater surface is not inferred from a category. No whole-cue subject gate is introduced.')
row(1266,'A person takes a stage pose while holding a magic-wand prop; stage setting and wand ownership are explicit cue parts.',
 'Use the independently declared existing person, wand prop and scene bound to main_subject, primary_prop and scene. Select a stage setting, the stated stage pose and holding the wand; do not add the wand, perform a spell or assert magic.',
 [('person','main_subject'),('wand','primary_prop'),('scene','scene')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Pq('wand','subject','wand','prop.identity','entity.type/v1','magic_wand_prop',[]),Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('pose','pose','person','body.pose','body.pose/v1','stage_pose',['person','wand'],'set_value',[]),Eq('hold','action','person','action.holding','action.holding/v1','holding_declared_wand',['person','wand'],'set_value',['wand']),Eq('stage','setting','scene','setting.location','setting.location/v1','stage',['scene'],'set_value',[])],
 {'en':['pose','wand','stage'],'ko':['pose','hold','stage'],'application_contract':['person','wand','scene','pose','hold','stage']},
 [role('body_pose',['pose'],['effect'],HP,.5,'direct','Posing is a static whole-body presentation.'),role('action',['hold'],['effect'],H,.5,'direct','Korean explicitly says holding the wand.'),role('prop',['wand'],['prerequisite'],H,.5,'direct','Named existing wand identity, without add_entity.'),role('location',['stage'],['effect'],H,.5,'direct','Stage is an actual selected setting, not a silent prerequisite.')],
 ['No spell efficacy, precise limb pose, performance success or new audience.'],[],{},'Old action .5 unrestricted is display-only. Human-only source guard and the actual wand/person prerequisites apply to every new role; final142 location has no extra domain gate.')
row(1267,'Shrine-lantern grid light is named, but grid geometry and receiver are not resolved.',None,[],[],{},[],
 ['Do not turn lamp-grid arrangement into projected stripes, invent a receiving face, build a shrine or infer religious practice.'],
 ['Grid may modify source arrangement or projected light shape. Source lacks a receiver and mechanism distinction. Need SHA-matched whole original or explicit source clarification before effects/owner map; light_shape routing is not positive evidence of projection.'],{},
 'Old light_shape .62 unrestricted is display-only. It cannot supply receiver/grid mechanism. No replacement binding now.')
row(1268,'A declared person is cast/styled as a gothic-doll cosplay performer; this is portrayal, not a literal doll.',
 'Use the independently declared existing person bound to main_subject. Select the gothic-doll cosplay portrayal and presentation without changing species/identity, adding a doll, naming a costume piece or prescribing a performance action.',
 [('person','main_subject')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Eq('cast','subject','person','subject.portrayal_role','subject.portrayal_role/v1','gothic_doll_cosplay_performer',['person'],'set_value',[]),Eq('style','appearance','person','presentation.style','presentation.style/v1','gothic_doll_cosplay',['person'],'set_value',[]),Eq('attire','appearance','person','wardrobe.context','wardrobe.context/v1','gothic_doll_cosplay',['person'],'set_value',[])],
 {'en':['cast','style','attire'],'ko':['cast','style','attire'],'application_contract':['person','cast','style','attire']},
 [role('subject',['cast'],['effect'],H,.55,'direct','Performer portrayal is explicit, separate from a living doll.'),role('presentation_style',['style'],['effect'],STYLE,.55,'direct','Cosplay presentation is stated without invented clothing details.'),role('attire_context',['attire'],['effect'],HP,.5,'contextual','Cosplay framing is explicit contextual purpose; actual presentation choice remains an effect.')],
 ['No literal doll species, gothic architecture, specific garment construction or stage action.'],[],{},'Old subject .55 unrestricted is a display choice. Source kind/human and performer meaning limit this application to the existing person; style/context use their current role-specific human/domain gates without making them universal source restrictions.')
row(1269,'Pursed lips with a small huff as a portrayed expression.',
 'Apply only to the independently declared existing mouth-bearing face bound to primary_face. Select pursed lips and the tiny-huff expression, without asserting audible sound, permanent lip shape or private anger.',
 [('face','primary_face')],
 [Pq('lips','expression','face','anatomy.lips.presence','anatomy.lips.presence/v1','present',[]),Eq('purse','expression','face','expression.mouth','expression.mouth/v1','pursed_lips_tiny_huff',['lips'],'set_value',[])],
 {'en':['purse'],'ko':['purse'],'application_contract':['lips','purse']},
 [role('expression',['purse'],['effect'],H,.82,'direct','Transient lip configuration/expression is explicit.')],
 ['No audio level, angry personality or permanent lip geometry.'],[],{},'Old expression human/animal scope is display-only; source human guard and actual lips prerequisite remain essential.')
row(1270,'Fairy lights are represented as bokeh dots, an image optical treatment, not a projected light grid.',
 'Use the independently declared existing fairy-light source and image bound to light_source and image. Keep the source type fixed and select its bokeh-dot appearance in the image; do not add lamps or project dots onto a receiving object.',
 [('lights','light_source'),('image','image')],
 [Pq('lights','lighting','lights','lighting.source.type','lighting.source.type/v1','fairy_lights',[]),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Eq('bokeh','camera','image','lens.artifact.bokeh','lens.artifact.bokeh/v1','fairy_light_bokeh_dots',['lights','image'],'set_value',['lights'])],
 {'en':['bokeh'],'ko':['bokeh'],'embedding_text':['bokeh'],'application_contract':['lights','image','bokeh']},
 [role('lens_artifact',['bokeh'],['effect'],NONE,.6,'direct','Final142 lens_artifact owns the named image-plane bokeh; no numerical lens identity is invented.'),role('light_type',['lights'],['prerequisite'],NONE,.44,'direct','Named existing fairy lights support source type, separately from image artifact.')],
 ['No projected dot pattern, dust particles, particular focal length, subject focus or new emitter.'],[],{},'Old light_shape .44 unrestricted is display-only and rejected for the bokeh fact. Explicit lighting-to-camera footprint correction retains named source identity as a typed prerequisite, rather than silently discarding it.')
row(1271,'A stack of Polaroid prints is held in one hand.',
 'Use only the independently declared existing Polaroid-print stack and its holder hand bound to primary_prop and primary_hands. Select stacked arrangement and one-hand holding; do not add prints or prescribe fingers, image contents or capture history.',
 [('prints','primary_prop'),('hand','primary_hands')],
 [Pq('prints','subject','prints','prop.identity','entity.type/v1','polaroid_print_stack',[]),Pq('hand','pose','hand','anatomy.hand.presence','anatomy.hand.presence/v1','one_declared_holder_hand',[]),Eq('stack','role','prints','prop.state','prop.state/v1','stacked',['prints'],'set_value',[]),Eq('hold','action','hand','action.holding','action.holding/v1','holding_declared_print_stack',['prints','hand'],'set_value',['prints'])],
 {'en':['stack','hold'],'ko':['stack','hold'],'application_contract':['prints','hand','stack','hold']},
 [role('prop',['prints'],['prerequisite'],H,.5,'direct','Print-stack object identity is stated.'),role('prop_state',['stack'],['effect'],H,.5,'direct','Current stacked arrangement is stated.'),role('action',['hold'],['effect'],H,.5,'direct','One-hand holding is explicit without added digit articulation.')],
 ['No legible photo content, print count, camera type used for capture or finger pose.'],[],{},'Old prop .5 unrestricted is display-only. Intrinsic source human use applies to every new role; one actual holder hand is a typed prerequisite, not inferred from human.')
row(1272,'Cracked texture belongs to a declared leather surface.',
 'Apply only to the independently declared existing leather surface bound to foreground_surface. Preserve its declared leather identity and select the cracked texture; do not infer manufacture, age, cause or a new object.',
 [('surface','foreground_surface')],
 [Pq('leather','material','surface','surface.material','surface.material/v1','declared_leather',[]),Eq('cracked','material','surface','texture.surface','texture.surface/v1','cracked',['leather'],'set_value',[])],
 {'en':['cracked'],'ko':['cracked'],'embedding_text':['cracked'],'application_contract':['leather','cracked']},
 [role('texture',['cracked'],['effect'],NONE,.42,'direct','Owned physical crack texture, not a flat motif.'),role('surface_material',['leather'],['prerequisite'],SURF,.42,'direct','Leather is declared material, not inferred chemistry.')],
 ['No age, cause, garment type, damage event or printed crack motif.'],[],{},'Old texture .42 unrestricted is display-only. The additional material role uses final142 surface scope independently; it does not narrow the whole cue to a garment or human.')
row(1273,'A small action figure or doll is a prop; the actual identity alternative is unselected.',None,[],[],{},[],
 ['Do not add a new doll, convert it to a living child, choose one OR branch, or invent an exact size.'],
 ['Actual action-figure/doll choice is absent and nominal existence/addition remains unspecified. An existing-only contract could preserve nominal scope, but full native identity/type and selected source RID require a root-approved explicit branch design.'],{},
 'Old prop .55 unrestricted is display-only; human source use remains intrinsic if branches are authored. No branch-specific new binding now.')
row(1274,'Volumetric light beams are visible through dust and haze; the atmosphere is not specified as separable motes.',
 'Use the independently declared existing air volume bound to light_receiver and scene bound to scene. Select visible volumetric beams and the stated dust-and-haze air medium; do not add a lamp or require separately resolved dust particles.',
 [('air','light_receiver'),('scene','scene')],
 [Pq('air','atmosphere','air','atmosphere.air_volume.presence','atmosphere.air_volume.presence/v1','present',[]),Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('beams','lighting','air','lighting.shape.volumetric_beams','lighting.shape.volumetric_beams/v1','visible_volumetric_beams',['air','scene'],'set_value',[]),Eq('medium','atmosphere','air','atmosphere.medium','atmosphere.medium/v1',['dust','haze'],['air'],'set_value',[])],
 {'en':['beams','medium'],'ko':['beams','medium'],'application_contract':['air','scene','beams','medium']},
 [role('atmospheric_medium',['medium'],['effect'],NONE,.7,'direct','Dust/haze air field is stated without inventing distinguishable particles.')],
 ['No resolved mote count, source location, beam direction, color or implied lamp.','Do not assert light_shape fit: the positive receiver is an air volume, while its full spec requires specified receiving surfaces. Do not upgrade to a complete lighting setup without source/placement/surface relations. The lighting beam effect is retained even though no displayed lighting role is proposed.'],[],{},'Old light_shape .8 unrestricted is display-only; reject that role because the specified air volume is not a declared receiving surface. New atmospheric-medium role is independently unrestricted. Both beam and medium actual mutations remain in the effect set; lack of a role never erases an effect.')
row(1275,'A person studies an unfamiliar star-map tablet, without adding specific gaze/hand geometry.',
 'Use the independently declared existing person and star-map tablet bound to main_subject and primary_prop. Keep the tablet identity and declared star-map content fixed; select studying it. Unfamiliar is the authored perspective, not proof of intelligence, origin or readable map content.',
 [('person','main_subject'),('tablet','primary_prop')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Pq('tablet','subject','tablet','prop.identity','entity.type/v1','star_map_tablet',[]),Eq('study','action','person','action.studying','action.studying/v1','studying_declared_tablet',['person','tablet'],'set_value',['tablet']),Cq('unfamiliar','concept','tablet','object.familiarity_description','object.familiarity_description/v1','unfamiliar_to_declared_person',[])],
 {'en':['study','unfamiliar'],'ko':['study','unfamiliar'],'application_contract':['person','tablet','study','unfamiliar']},
 [role('action',['study'],['effect'],H,.72,'direct','Studying a named tablet is explicit.'),role('prop',['tablet'],['prerequisite'],H,.6,'direct','Existing tablet identity is required; no extraterrestrial genre follows.')],
 ['No aliens, navigation result, intelligence fact, hand contact or exact gaze direction.'],[],{},'Old action .72 unrestricted is display-only. Source human remains intrinsic for both action and prop. Familiarity stays interpretive context without changing tablet content.')
row(1276,'A downward observational camera view looks over a railing, with a corresponding frame arrangement.',
 'Use the independently declared existing camera, image and railing bound to recording_camera, image and primary_prop. Select the downward viewing direction and over-railing framing arrangement; do not add a railing or assert surveillance, height or a person leaning.',
 [('camera','recording_camera'),('image','image'),('railing','primary_prop')],
 [Pq('camera','camera','camera','camera.presence','camera.presence/v1','present',[]),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Pq('railing','subject','railing','entity.type','entity.type/v1','railing',[]),Eq('down','camera','camera','camera.direction','camera.direction/v1','downward',['camera','railing'],'set_value',[]),Eq('over','composition','image','composition.boundary_arrangement','composition.boundary_arrangement/v1','over_declared_railing',['image','railing'],'set_value',['railing'])],
 {'en':['down','over'],'ko':['down','over'],'application_contract':['camera','image','railing','down','over']},
 [role('camera_direction',['down'],['effect'],NONE,.85,'direct','Explicit downward camera observation.'),role('composition',['over'],['effect'],NONE,.9,'direct','Over-railing boundary arrangement is explicit.')],
 ['No observer profession, building height, leaning actor or surveillance purpose.'],[],{},'Old composition .9 unrestricted is display-only. Retain its actual boundary layout and add independent camera direction; no human restriction is invented.')
row(1277,'An unpolished real-person-like presentation is selected, not verified identity or documentary truth.',
 'Apply to the independently declared existing person bound to main_subject. Select unpolished real-person-like presentation without claiming actual authenticity, identity, absent cosmetics or a documentary capture process.',
 [('person','main_subject')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Eq('presence','appearance','person','presentation.style','presentation.style/v1','unpolished_real_person_like',['person'],'set_value',[])],
 {'en':['presence'],'ko':['presence'],'application_contract':['person','presence']},
 [role('presentation_style',['presence'],['effect'],STYLE,.8,'direct','The visible presentation choice is explicit even without a detailed grooming recipe.')],
 ['No real identity, no-makeup certainty, unretouched provenance or documentary certification.'],[],{},'Old presentation-style .8 human/domain scope remains role policy. Source human is intrinsic; actual styling remains an appearance effect.')
row(1278,'A blank face contrasts with warm/helpful-looking hands; no specific helping gesture is named.',None,[],[],{},[],
 ['Do not invent a helpful action, hand pose, actual warmth, altruism or specific relationship.'],
 ['Blank facial expression is clear, but the required hand portrayal has no actual configuration and the English helpful is absent from the shorter Korean warm impression. A partial face fact would not cover the whole cue. Need original-source clarification of the intended hand/social portrayal before correcting the expression-only footprint.'],{},
 'Old expression .82 human/animal scope is display policy; intrinsic source human applies. Additional social/hand roles cannot be supplied by the old tag or by the word helpful alone.')
row(1279,'Select a bamboo-forest path setting.',
 'Select the bamboo-forest path for the independently declared scene bound to scene. This is a setting choice, without adding a walker or selecting a country or season.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('place','setting','scene','setting.location','setting.location/v1','bamboo_forest_path',['scene'],'set_value',[])],
 {'en':['place'],'ko':['place'],'phrase_en':['place'],'phrase_ko':['place'],'application_contract':['scene','place']},
 [role('location',['place'],['effect'],NONE,.9,'direct','An explicit physical route in a declared environment.')],
 ['No nationality, season, traveler, walking action or exact architecture.'],[],{},'Old location .9 unrestricted is a display role; retained with explicit existing-scene prerequisite and actual setting mutation.')
row(1280,'A window room is selected within a ghost-bride-associated fictional framing; the title does not add a bride.',
 'Use the independently declared scene bound to scene. Select the stated room-with-window setting. Ghost-bride association is the authored fictional context only; it does not introduce a bride, establish a haunting or prescribe visible apparition details.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('room','setting','scene','setting.location','setting.location/v1','room_with_window',['scene'],'set_value',[]),Cq('ghost','concept','scene','narrative.context','narrative.context/v1','ghost_bride_associated_fictional_room',[])],
 {'en':['room','ghost'],'ko':['room','ghost'],'embedding_text':['room','ghost'],'application_contract':['scene','room','ghost']},
 [role('location',['room'],['effect'],NONE,.58,'direct','The room/window is physical setting; no ghost actor is inferred.')],
 ['No bride entity, supernatural proof, costume, death history or window-light effect.'],[],{},'Old location .58 unrestricted is display-only. Ghost-bride association is retained as interpretive context without granting entity addition or visual supernatural effects; the actual room selection remains an effect.')
row(1281,'Select a summer beach shoreline, preserving both seasonal timing and physical setting meaning.',
 'Apply to the independently declared scene bound to scene. Select beach-shoreline setting and summer seasonal timing; neither selected property is converted to an already-frozen prerequisite. Do not add swimmers or choose weather/geography.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('shore','setting','scene','setting.location','setting.location/v1','beach_shoreline',['scene'],'set_value',[]),Eq('summer','timing','scene','timing.season','timing.season/v1','summer',['scene'],'set_value',[])],
 {'en':['shore','summer'],'ko':['shore','summer'],'embedding_text':['shore','summer'],'application_contract':['scene','shore','summer']},
 [role('location',['shore'],['effect'],NONE,.52,'direct','Physical shoreline setting is explicit.'),role('season',['summer'],['effect'],NONE,.6,'contextual','Summer is a selected timing constraint; contextual role does not make its mode context.')],
 ['No temperature, specific day, swimmer, resort or tropical geography.'],[],{},'Old location .52 unrestricted is display-only. New season independently unrestricted; source has no intrinsic human gate. Both timing and setting must be permitted.')
row(1282,'Select glitch anxiety as an affective mood; the already-approved correction excludes robot proof.',
 'Apply the stated affective mood to the independently declared scene bound to scene. Glitch anxiety is a mood selection, not a robot identity, scene anchor or automatic image-encoding glitch.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('mood','atmosphere','scene','mood.atmosphere','mood.atmosphere/v1','glitch_anxiety',['scene'],'set_value',[])],
 {'en':['mood'],'ko':['mood'],'embedding_text':['mood'],'application_contract':['scene','mood']},
 [role('mood',['mood'],['effect'],NONE,.66,'contextual','Affective mood is explicitly selected; no physical-measurement requirement and no lock-avoiding context mode.')],
 ['No robot concept, identity, new actor, scene anchor or default visual corruption artifact.'],[],{},'Old mood .66 contextual semantic role is display classification, not native mode. Intrinsic conditions empty by direct review; actual mood mutation retained in atmosphere.')
row(1283,'A low upward concert camera angle is composed from beyond a crowd; event context and crowd relation are cue parts.',
 'Use the independently declared existing camera, image, crowd and scene bound to recording_camera, image, secondary_subject and scene. Select the upward low angle, beyond-crowd layout and concert occasion. Do not introduce a crowd or infer exact count, identity or performance success.',
 [('camera','recording_camera'),('image','image'),('crowd','secondary_subject'),('scene','scene')],
 [Pq('camera','camera','camera','camera.presence','camera.presence/v1','present',[]),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Pq('crowd','subject','crowd','entity.type','entity.type/v1','declared_crowd',[]),Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('angle','camera','camera','camera.direction','camera.direction/v1','low_angle_upward',['camera'],'set_value',[]),Eq('layout','composition','image','composition.view_boundary','composition.view_boundary/v1','from_beyond_declared_crowd',['image','crowd'],'set_value',['crowd']),Eq('concert','event','scene','occasion.context','occasion.context/v1','concert',['scene'],'set_value',[])],
 {'en':['angle','layout','concert'],'ko':['angle','layout','concert'],'application_contract':['camera','image','crowd','scene','angle','layout','concert']},
 [role('camera_direction',['angle'],['effect'],NONE,.65,'direct','Upward low camera angle is explicit.'),role('composition',['layout'],['effect'],NONE,.6,'direct','Crowd/beyond relation is a stated layout.'),role('occasion_context',['concert'],['effect'],{'subject_applicability':{'deny_domains':['product','jewelry','food','wildlife','adult']}},.6,'contextual','Concert is explicitly selected occasion, not a derived profession; preserve the role-specific domain exclusions.')],
 ['No exact crowd count, stage actor, festival identity, physical height or noise measurement.'],[],{},'Old composition .6 unrestricted is display-only. Its crowd endpoint is now an exact typed prerequisite; newly selected camera/event effects are independently retained and not waived through contextual role.')
row(1284,'Select precise eye focus in an album-cover-like treatment under the existing kpop-or-album guard.',
 'Use the independently declared existing image and actual eyes bound to image and primary_face. Select the focal plane on those eyes. Keep the original kpop-or-album eligibility guard; album-cover styling does not prove release format or an actual album.',
 [('image','image'),('eyes','primary_face')],
 [Pq('image','camera','image','image.presence','image.presence/v1','present',[]),Pq('eyes','expression','eyes','anatomy.eyes.presence','anatomy.eyes.presence/v1','present',[]),Eq('focus','camera','image','focus.selected_plane','focus.selected_plane/v1','declared_eyes',['image','eyes'],'select_plane',['eyes']),Cq('album','concept','image','presentation.reference','presentation.reference/v1','album_cover_like',[])],
 {'en':['focus','album'],'ko':['focus','album'],'application_contract':['image','eyes','focus','album']},
 [role('focus',['focus'],['effect'],NONE,.45,'direct','Actual focus selection is explicit and cannot be preservation.')],
 ['No new eyes, eye identity, k-pop occupation, release medium or frozen focus preservation.'],[],{},'Old focus .45 unrestricted is display-only. Source requires_any_tags[kpop,album] is intrinsic and must gate the entire candidate, including this new fact inventory; empty binding applicability cannot bypass it.')
row(1285,'An unspecified object is propped against a partner chair; the partner/chair/object endpoints need binding.',None,[],[],{},[],
 ['Do not invent a stick, a seated partner, primary owner identity or a chair owner relationship.'],
 ['The positive prose omits the prop and leaves partner-chair ownership/reference underspecified. Need exact original clarification or request-grounded object/chair/partner relation before native relocate/placement effects; no automatic primary assignment.'],{},
 'Old prop_placement .82 human/domain restrictions are role policy. The partner relation and object/chair type would be intrinsic typed prerequisites for every later role; do not replace those with that gate.')
row(1286,'Two declared people are included together through a mirror; reflected framing does not add duplicate people.',
 'Use only two independently declared existing people and the independently declared existing mirror and image bound to main_subject, secondary_subject, primary_prop and image. Select inclusion of that pair together through the mirror; the visible included-person count is two, without adding/removing people or imposing contact.',
 [('person_a','main_subject'),('person_b','secondary_subject'),('mirror','primary_prop'),('image','image')],
 [Pq('a','subject','person_a','entity.type','entity.type/v1','person',[]),Pq('b','subject','person_b','entity.type','entity.type/v1','person',[]),Pq('mirror','subject','mirror','entity.type','entity.type/v1','mirror',[]),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Eq('together','composition','image','composition.group_arrangement','composition.group_arrangement/v1','declared_pair_together_through_mirror',['a','b','mirror','image'],'set_value',['person_a','person_b','mirror']),Eq('frame','framing','image','framing.subject_inclusion','framing.subject_inclusion/v1','declared_pair_through_mirror',['a','b','mirror','image'],'set_value',['person_a','person_b']),Eq('count','count','image','participant.count.visible','participant.count.visible/v1','two',['a','b','image'],'set_value',['person_a','person_b']),Eq('reflected','composition','image','image.reflection','image.reflection/v1','declared_pair_in_declared_mirror',['a','b','mirror','image'],'set_value',['person_a','person_b','mirror'])],
 {'en':['together','frame','count','reflected'],'ko':['together','frame','count','reflected'],'application_contract':['a','b','mirror','image','together','frame','count','reflected']},
 [role('composition',['together'],['effect'],NONE,.82,'direct','Together-through-mirror layout is explicit.'),role('subject_framing',['frame'],['effect'],NONE,.75,'direct','The declared pair is included via a mirror.'),role('subject_count',['count'],['effect'],NONE,.7,'direct','Selected visible pair count is two; frozen existence of two people does not waive visible-count selection.'),role('reflection_logic',['reflected'],['effect'],NONE,.7,'direct','The stated pair is depicted through the declared mirror; no mismatch or second pair is invented.')],
 ['No duplicate reflected entities, contact, inferred couple identity or camera apparatus visible in the mirror.'],[],{},'Old composition .82 unrestricted is display-only. New framing/count independently unrestricted but require both existing declared people and mirror. Core must separately ground distinct people; no extra persons are introduced.')
row(1287,'A declared colleague remains outside the frame; the cue neither adds a colleague nor removes them from the scene.',
 'Use the independently declared existing colleague bound to secondary_subject and existing image bound to image. The colleague relation must already be declared in the request; preserve that relation and select off-frame visibility without adding or removing an entity.',
 [('colleague','secondary_subject'),('image','image')],
 [Pq('colleague','subject','colleague','entity.type','entity.type/v1','person',[]),Pq('relation','relationship','colleague','participant.role','participant.role/v1','request_declared_colleague', ['colleague']),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Sq('keep','relationship','colleague','participant.role','participant.role/v1','request_declared_colleague',['relation']),Eq('offframe','framing','image','framing.subject_visibility','framing.subject_visibility/v1','declared_colleague_off_frame',['colleague','relation','image'],'set_value',['colleague']),Eq('offcontext','relationship','colleague','context.offscreen','context.offscreen/v1','off_frame_colleague',['colleague','relation','image'],'set_value',['image'])],
 {'en':['offframe','relation','offcontext'],'ko':['offframe','relation','offcontext'],'application_contract':['colleague','relation','image','keep','offframe','offcontext']},
 [role('offscreen_context',['offcontext'],['effect'],H,.7,'contextual','Explicit off-frame participant context; effect mode retains actual offscreen relation and framing constraint, catalog adds no domain gate.'),role('participant_role',['relation'],['prerequisite'],HP,.82,'contextual','Colleague is a declared relation prerequisite, not inferred social identity.'),role('subject_framing',['offframe'],['effect'],H,.7,'direct','Named existing participant is outside the selected frame.')],
 ['No new coworker, employer, current action, colleague location or remove_entity.'],
 ['The exact colleague-of endpoint must be independently bound by the request, rather than guessed from source. Proposed relation token is a typed request-declared relation; no formal core/signature exists yet. Root must confirm endpoint representation before a complete native proof.'],{},
 'Old participant-role .82 human/domain policy is role-specific. Source human is intrinsic. Exact declared colleague relation is essential to all later roles and must not be weakened to a mere category or context label.')
row(1288,'Panning produces motion blur while the declared subject is sharp; sharpness is a selected image constraint.',
 'Use the independently declared existing camera, image and subject bound to recording_camera, image and main_subject. Select panning capture movement, panning motion blur and the subject-sharp image result; do not prescribe subject movement, shutter speed or reinterpret sharpness as preservation.',
 [('camera','recording_camera'),('image','image'),('subject','main_subject')],
 [Pq('camera','camera','camera','camera.presence','camera.presence/v1','present',[]),Pq('image','composition','image','image.presence','image.presence/v1','present',[]),Pq('subject','subject','subject','entity.presence','entity.presence/v1','present',[]),Eq('pan','camera','camera','camera.movement','camera.movement/v1','panning',['camera'],'set_value',[]),Eq('blur','camera','image','image.motion.blur','image.motion.blur/v1','panning_motion_blur',['camera','image','subject'],'set_value',[]),Eq('sharp','camera','image','focus.subject_sharpness','focus.subject_sharpness/v1','declared_subject_sharp',['image','subject'],'select_plane',['subject'])],
 {'en':['pan','blur','sharp'],'ko':['pan','blur','sharp'],'application_contract':['camera','image','subject','pan','blur','sharp']},
 [role('camera_movement',['pan'],['effect'],NONE,.9,'direct','Panning is explicit capture movement.'),role('motion_rendering',['blur'],['effect'],NONE,.9,'direct','Recorded panning motion blur is explicitly separate from camera movement.'),role('focus',['sharp'],['effect'],NONE,.85,'direct','Sharp subject is an actual selected focus/sharpness constraint, not frozen preservation.')],
 ['No athlete, specific subject action, shutter value, general frame layout or preserved focus waiver.'],[],{},'Old composition weight1 unrestricted is display-only and unsupported by an independent arrangement clause here. Explicitly propose camera footprint correction, retaining every panning/blur/sharp effect rather than inheriting the old composition tag.')
row(1289,'Select a campus café setting; Korean is aligned to campus rather than silently broadening to any college district.',
 'Select a campus café location for the independently declared scene bound to scene. Do not infer a specific institution, student identity or an off-campus neighborhood.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('cafe','setting','scene','setting.location','setting.location/v1','campus_cafe',['scene'],'set_value',[])],
 {'en':['cafe'],'ko':['cafe'],'phrase_en':['cafe'],'phrase_ko':['cafe'],'application_contract':['scene','cafe']},
 [role('location',['cafe'],['effect'],NONE,.8,'direct','English campus café anchors the proposed translation clarification.')],
 ['No university identity, student age, café staff or city.'],[],{'ko':'캠퍼스 카페','phrase_ko':'캠퍼스 카페 안에서'},'Old location .8 unrestricted is display-only. Translation proposal resolves campus versus college-district mismatch explicitly; no category gate is added.')
row(1290,'Sticky tropical heat is selected as declared weather/atmosphere, without a temperature reading or bodily consequence.',
 'Apply the stated sticky tropical heat as declared weather to the independently declared scene bound to scene. This selects the weather description; it does not certify numerical temperature/humidity or add sweating, a tropical country or a summer date.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('heat','atmosphere','scene','weather.declared','weather.declared/v1','sticky_tropical_heat',['scene'],'set_value',[])],
 {'en':['heat'],'ko':['heat'],'embedding_text':['heat'],'application_contract':['scene','heat']},
 [role('weather',['heat'],['effect'],NONE,.56,'direct','Explicit qualitative weather choice remains an atmosphere mutation even without a measurable proxy.')],
 ['No temperature value, sweat, exact humidity, season or geographical identity.'],[],{},'Old weather .56 unrestricted is display-only. Scene existence is prerequisite; weather itself is not frozen as a precondition to bypass atmosphere locks.')
row(1291,'Fresh campus-student-like styling is a selected presentation, not enrollment or age evidence.',
 'Use the independently declared existing person bound to main_subject. Select fresh campus-student-like styling without assigning actual enrollment, age, campus location or specific garments.',
 [('person','main_subject')],
 [Pq('person','subject','person','entity.type','entity.type/v1','person',[]),Eq('style','appearance','person','presentation.style','presentation.style/v1','fresh_campus_student_like',['person'],'set_value',[])],
 {'en':['style'],'ko':['style'],'application_contract':['person','style']},
 [role('presentation_style',['style'],['effect'],STYLE,.7,'direct','The appearance treatment is explicit; student role is only likeness.')],
 ['No enrollment, adult/minor declaration, exact clothing or university setting.'],[],{},'Old presentation-style .7 human/domain applicability remains role policy. Candidate human use remains intrinsic and cannot be replaced by a style-category inference.')
row(1292,'An existing folded paper crane is left behind as a signal token; no sender, recipient or successful decoding is implied.',
 'Use only the independently declared existing paper crane bound to primary_prop. Select its folded state and left-behind disposition as a signal token. The signaling purpose is authored narrative function; do not add an actor, choose a hidden group, or assert delivery/decoding success.',
 [('crane','primary_prop')],
 [Pq('crane','subject','crane','prop.identity','entity.type/v1','paper_crane',[]),Eq('fold','role','crane','prop.state','prop.state/v1','folded',['crane'],'set_value',[]),Eq('left','role','crane','prop.state.disposition','prop.state.disposition/v1','left_behind',['crane'],'set_value',[]),Eq('signal','concept','crane','narrative.clue.function','narrative.clue.function/v1','signal_token',['crane'],'set_value',[])],
 {'en':['fold','left','signal'],'ko':['fold','left','signal'],'application_contract':['crane','fold','left','signal']},
 [role('prop',['crane'],['prerequisite'],H,.85,'direct','Existing object identity is explicit.'),role('prop_state',['fold','left'],['effect'],H,.75,'direct','Folded/left-behind disposition are stated object states.'),role('narrative_clue',['signal'],['effect'],H,.75,'contextual','Signal-token function is explicit narrative interpretation, with actual semantic selection retained; source-human is intrinsic, catalog adds no extra domain gate.')],
 ['No sender identity, secret organization, particular recipient, hand action or successful decoding.'],[],{'ko':'신호 토큰으로 남겨진 접힌 종이학'},'Old prop .85 unrestricted is display-only. Source human guard applies to all roles; narrative-clue has no extra catalog applicability gate; preserve this CID source-human restriction. Selecting signal function is not demoted to a no-op.')
row(1293,'Long wavy black hair with naturally flowing visual arrangement; no wind action or ethnicity is entailed.',
 'Use only the independently declared existing owned hair bound to primary_hair. Select long length, wavy form, black local hair color and naturally flowing visual arrangement. Do not add hair, choose biological versus wig origin, alter identity or assert actual wind/movement.',
 [('hair','primary_hair')],
 [Pq('hair','appearance','hair','hair.presence','hair.presence/v1','declared_owned_hair',[]),Eq('length','appearance','hair','hair.length','hair.length/v1','long',['hair'],'set_value',[]),Eq('wave','appearance','hair','hair.style','hair.style/v1','wavy',['hair'],'set_value',[]),Eq('flow','appearance','hair','hair.strands.arrangement','hair.strands.arrangement/v1','naturally_flowing_visual_arrangement',['hair'],'set_value',[]),Eq('black','appearance','hair','hair.color','hair.color/v1','black',['hair'],'set_value',[])],
 {'en':['length','wave','black'],'ko':['length','wave','flow','black'],'application_contract':['hair','length','wave','flow','black']},
 [role('hair_style',['length','wave','flow'],['effect'],HP,1.,'direct','Length and wave are explicit in English/Korean; naturally flowing arrangement is specifically anchored in Korean and the clarified contract, not borrowed into the shorter English string.'),role('hair_color',['black'],['effect'],HP,.85,'direct','Black is hair-local color, not global image grading.')],
 ['No ethnicity, wind source, motion, wig/biological origin or face similarity.'],[],{},'Old hair-style1 human/domain limits are role-specific and retained for hair roles. Source human is intrinsic; actual owned hair is an independent typed prerequisite, not inferred from human.')
row(1294,'Select an apartment-door threshold setting.',
 'Select the apartment-door threshold for the independently declared scene bound to scene. Do not add a resident, entry/exit action or an entire unseen apartment interior.',
 [('scene','scene')],
 [Pq('scene','setting','scene','scene.presence','scene.presence/v1','present',[]),Eq('threshold','setting','scene','setting.location','setting.location/v1','apartment_door_threshold',['scene'],'set_value',[])],
 {'en':['threshold'],'ko':['threshold'],'embedding_text':['threshold'],'application_contract':['scene','threshold']},
 [role('location',['threshold'],['effect'],NONE,.58,'direct','A concrete structural place is explicitly selected.')],
 ['No resident, entry action, ownership, time or hidden room layout.'],[],{},'Old location .58 unrestricted is display-only and retained. Scene existence prerequisite does not freeze the chosen location in advance.')
row(1295,'Aged-looking skin is contrasted with young-looking skin texture; actual owner/region partition is unspecified.',None,[],[],{},[],
 ['Do not infer two actors, baby/elder family identity, exact ages, same-body regions or actual age from texture.'],
 ['The source leaves number and ownership of skin surfaces open. Native core cannot select main/secondary actors or surfaces by guess. Material-only effects are also coarse for age-presentation/appearance meaning. Need original SHA-matched whole intent or explicit request-bound skin-region partition and an exact footprint correction.'],{},
 'Old texture1 unrestricted is display-only, not evidence of a particular skin owner or ages. Future skin-finish/age roles require exact owned regions; do not inherit a generic texture union or choose a family scenario.')
row(1296,'A warm mug is held in both hands; warmth is declared object state and holding/wrapping are actual actions.',None,[],[],{},[],
 ['Do not add steam, a beverage, comfort emotion, actual heating or unspecified hand articulation.'],
 ['Existing-only mug/hands application can be proposed, but warm is an actual stated thermal condition and current empty effects do not define whether cue sets warmth or requires an independently warm mug. A warmth prerequisite cannot be chosen simply to avoid a thermal mutation lock. Need original intent clarification and explicit thermal property/operation treatment before a complete inventory.'],{},
 'Old prop .6 unrestricted is display-only. Both owned hands and mug identity are essential prerequisites for later roles; source has no human gate to copy mechanically. Do not let a prop role bypass the warm/holding whole meaning.')
row(1297,'An object is staged to appear floating in midair; the statement is static styling rather than literal levitation.',
 'Use only the independently declared existing object bound to primary_prop under the original object/product/food eligibility. Select apparently midair-suspended placement and staged floating presentation; do not add an object, assert physical levitation or prescribe motion.',
 [('object','primary_prop')],
 [Pq('object','subject','object','entity.presence','entity.presence/v1','present',[]),Eq('place','composition','object','objects.position','objects.position/v1','apparently_suspended_midair',['object'],'relocate',[]),Eq('stage','style','object','presentation.staging','presentation.staging/v1','styled_as_if_floating',['object'],'set_value',[])],
 {'en':['place','stage'],'ko':['place','stage'],'application_contract':['object','place','stage']},
 [role('prop_placement',['place'],['effect'],OBJ,.8,'direct','Final142 permits object-local placement; static apparent suspension is explicit.'),role('staging_degree',['stage'],['effect'],OBJ,.7,'contextual','Staged apparent floating is a selected presentation degree; mode remains effect.')],
 ['No real levitation, motion path, human action, gravity violation or implicit add_entity.'],[],{},'Old action .8 unrestricted is display-only and rejected for apparent static staging. Source object/product/food restriction is intrinsic across both proposed roles. Correct action footprint explicitly to composition/style, not merely relabel its fact mode.')
row(1298,'A florist delivery box functions as a cover-identity prop, without proving a real florist or successful deception.',
 'Use only the independently declared existing florist-delivery box bound to primary_prop. Keep its identity fixed and select its authored cover-identity prop function. Do not add a florist, flowers, delivery action, specific actor intention or successful deception.',
 [('box','primary_prop')],
 [Pq('box','subject','box','prop.identity','entity.type/v1','florist_delivery_box',[]),Eq('cover','concept','box','narrative.clue.function','narrative.clue.function/v1','cover_identity_prop',['box'],'set_value',[])],
 {'en':['cover'],'ko':['cover'],'application_contract':['box','cover']},
 [role('prop',['box'],['prerequisite'],H,.9,'direct','Box identity is declared; no automatic new entity.'),role('narrative_clue',['cover'],['effect'],H,.75,'contextual','Explicit cover function is contextual narrative meaning, with the semantic selection still an effect; catalog adds no human/domain gate beyond this source intrinsic human restriction.')],
 ['No performer identity, florist occupation, flower contents, covert group or successful deception.'],[],{},'Old prop .9 unrestricted is display-only. Source human remains intrinsic; narrative-clue has no extra catalog applicability gate; preserve the CID intrinsic human use. No character_intent role is supplied because the box purpose does not bind a specific mind/actor endpoint.')
row(1299,'Hands-only macro framing shows an exchange, but actual exchange endpoints/carried object are not supplied.',None,[],[],{},[],
 ['Do not invent two people, two hands, a gift, money, direction of transfer or digit pose.'],
 ['Macro/hands-only image effect is clear but the whole exchange relation needs requester-grounded existing hand owners and actual exchange endpoints. A partial crop inventory would omit action/relationship meaning. Need source/application clarification before replacing composition-only effects and proposing complete native bindings.'],{},
 'Old composition .8 unrestricted is display-only. Future framing/shot-scale must retain typed hand/exchange prerequisites and complete relational/action effects; no new role may bypass the unresolved relation.')

assert [r['ordinal'] for r in ROWS]==list(range(1250,1300))

def write_new(path,value):
 assert not path.exists(),str(path)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

out=[]
for literal in ROWS:
 n=literal['ordinal'];cid=I['ids'][n-1250];v=I['records'][cid]
 before=copy.deepcopy(v['after_existing5B_corrections']);after=copy.deepcopy(before)
 changes=[]
 for key,text in literal['translation_proposals'].items():
  changes.append({'pointer':'/content/'+key,'before':copy.deepcopy(after['content'][key]),'after':text,'reason':'Explicit whole-meaning translation alignment; see manual meaning and boundaries.'});after['content'][key]=text
 if literal['application_contract_proposal'] is not None:
  text=literal['application_contract_proposal'];assert 'application_contract' not in after['content']
  changes.append({'pointer':'/content/application_contract','before':None,'after':text,'reason':'Proposed explicit existing-owner application and/or non-additive scope, preserving all selected effects. Root approval required.'});after['content']['application_contract']=text
 clauses={q[0]:q for q in literal['clauses']};assert len(clauses)==len(literal['clauses'])
 facts=[];units=[]
 for key,ids in literal['unit_clause_map'].items():
  text=after['content'][key];refs=[]
  for name in ids:
   q=clauses[name];i,d,t,p,mode,ns,val,requires,operation,receivers=q
   # Each explicit source-string assignment makes a separate same-pointer fact.
   # Common semantic IDs are resolved to application-contract prerequisites only.
   req=[x+'__application_contract' for x in requires]
   f={'id':i+'__'+key,'realization_id':'base','pointer':'/content/'+key,'quote':text,'dimension':d,'target':t,'property':p,'mode':mode,'value':{'type':ns,'value':val},'requires':req}
   if mode=='effect':f.update(operation=operation,receivers=receivers)
   facts.append(f);refs.append(f['id'])
  units.append({'realization_id':'base','pointer':'/content/'+key,'quote':text,'fact_refs':refs,'disposition':'semantic'})
 if literal['application_contract_proposal'] is not None:
  # Footprint is constructed from the explicitly authored mutation clauses, not
  # from tags, words, old effects or inferred owner conventions.
  effects=[q for q in literal['clauses'] if q[4]=='effect']
  proposed={'dimensions':sorted({q[1] for q in effects}),'properties':[{'dimension':q[1],'property':q[3],'target':q[2]} for q in effects]}
  if proposed!=after['effects']:
   changes.append({'pointer':'/effects','before':copy.deepcopy(after['effects']),'after':copy.deepcopy(proposed),'reason':'Explicit per-clause effects selected by this fresh source review; retain selected timing, mood, appearance, arrangement and relational consequences. Coarse/misowned original footprint is proposed for correction, never silently narrowed in proof.'});after['effects']=proposed
  required_fields={k for k,val in after['content'].items() if k in ['en','ko','phrase_en','phrase_ko','embedding_text','application_contract'] and isinstance(val,str)}
  assert set(literal['unit_clause_map'])==required_fields,(n,required_fields,set(literal['unit_clause_map']))
 for f in facts:
  expected={'id','realization_id','pointer','quote','dimension','target','property','mode','value','requires'} | ({'operation','receivers'} if f['mode']=='effect' else set())
  assert set(f)==expected and f['quote']==after['content'][f['pointer'].split('/')[-1]]
  assert all(any(x['id']==rid and x['mode'] in ['prerequisite','preservation'] for x in facts) for rid in f['requires']),(n,f)
  assert f['mode']!='effect' or f['operation'] in ['set_value','add_entity','remove_entity','relocate','select_plane']
 active={f['target'] for f in facts}|{t for f in facts if f['mode']=='effect' for t in f['receivers']}
 assert active=={x[0] for x in literal['owner_bindings']},(n,active,literal['owner_bindings'])
 roles=[]
 for r in literal['roles']:
  assert r['tag'] in I['catalog_final142']
  refs=[]
  for i in r['fact_ids']:
   refs.append(i+'__application_contract')
  assert all(any(f['id']==x and f['mode'] in r['support_modes'] for f in facts) for x in refs)
  roles.append({**r,'fact_refs':refs,'spec_sha256':sha(I['catalog_final142'][r['tag']]),'scope':'whole_record','realization_ids':['base']})
 out.append({'ordinal':n,'candidate_id':cid,'status':'exact_semantic_pending' if literal['pending'] else 'manual_source_fact_draft_ready_for_root_source_review','complete_native_proof':False,'formal_input_rebind_required':True,
  'whole_meaning':literal['meaning'],'source_before':before,'source_proposal':after,'exact_source_correction_proposals':changes,
  'before_source_full_sha256':sha(before),'after_proposed_full_sha256':sha(after),'original_source_full_sha256':v['before_full_record_sha256'],
  'registered5B_locator':v['registered5B_locator'],'registered5B_decision_sha256':sha(v['registered5B']),
  'source_guard_classification':{'intrinsic_conditions_retained_exactly':copy.deepcopy(before['conditions']),'all_proposed_roles_must_obey_intrinsic_conditions':True,'reason':literal['own_binding_review']},
  'existing_own_bindings_full':copy.deepcopy(OWN[cid]),'own_binding_review':literal['own_binding_review'],
  'member_binding_migration':{'member_bindings':[],'reason':'Actual whole-source/member closure reread: primitive base option with no CID members or explicit member-binding references. Own display binding is accounted separately.'},
  'actual_realization_ids':v['actual_rids'],'required_cid_closure':copy.deepcopy(v['required_cid_closure']),'explicit_binding_closure':copy.deepcopy(v['explicit_binding_closure']),
  'native_fact_draft':facts,'owner_maps_draft':{'base':{'schema':'photo-native-owner-bindings/v2','bindings':[{'target':t,'core_role':core,'origin':'existing','introduced_by':None} for t,core in literal['owner_bindings']]}},
  'source_units_draft':units,'proposed_roles_and_binding_intent':roles,'rejected_boundaries':literal['rejected_boundaries'],'exact_pending_reasons':literal['pending'],
  'actual_read':{'source_original_full':True,'source_after5B_full':True,'registered5B_full_with_provenance':True,'own_bindings_full':True,'mandatory_reference_closure_full':True,'proposed_full_source_reread':False}})
body={'schema':'native-direct-manual-source-fact-draft/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','range':[1250,1300],'count':50,'source_sha256':I['source_sha256'],'catalog_sha256':I['catalog_final142_sha256'],'input_bytes_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'own_bindings_bytes_sha256':hashlib.sha256(B.read_bytes()).hexdigest(),'formal_root_fullsnapshot_input_pending':True,'operational_or_native_qualification_claim':False,'rows':out}
write_new(Path(__file__).with_name('native_11870_01250_02250.01250_01300.draft_before_reread_v4.json'),body)
print('MANUAL_DRAFT_PREPARED_FOR_WHOLE_CORRECTED_REREAD',len(out),'rows',sum(bool(x['exact_pending_reasons']) for x in out),'pending; no native proof/signature/registration')
