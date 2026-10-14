"""Serialize individually authored alternatives; never generate native proof/status.

All application text, guards, effects and semantic judgments below are literal
manual proposals. Loops copy/hash exact inputs and serialize structural deltas.
"""
from pathlib import Path
import copy, gzip, hashlib, json

R=Path(__file__).resolve().parents[1]
OUT=R/'authored/root_pending13_source_proposals_native_v1.json'
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(path):return json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes())
paths=[R/'SOURCE.json.gz',R/'native-inputs/root-00000-00020-plan-01/CURRENT-PROPOSAL.json.gz',
    R/'native_batches/root-00000-00020-01/BATCH-WIRE-02.json',R/'decisions/batch_00000_00020.json',
    R/'authored/batch_00000_00020.json',R/'CATALOG-FINAL-144-V4.json',
    R/'native-inputs/root-00000-00020-plan-01/ROOT-REVIEW-REQUIREMENTS.json']
source,current,batch,old,authored,catalog,requirements=[read(path) for path in paths]
assert digest(current)=='f1a7b55527c677e3401a19aec37e57e36a0f07584c0464536bce8b9f141897be'
assert digest(catalog)=='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
assert hashlib.sha256(paths[2].read_bytes()).hexdigest()=='26ad6216c781ae3cf24ea8a71997fcf6f1a098c70ed9b6c19749ee79bc1fef9b'
pins=[{'file':str(p),'bytes':p.stat().st_size,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'canonical_sha256':digest(v)} for p,v in zip(paths,[source,current,batch,old,authored,catalog,requirements])]

def frozen(target,dimension,prop,value):
    return {'kind':'frozen_value','owner':target,'dimension':dimension,'property':prop,
        'value':{'type':prop+'/v1','value':value}}
def link(left,right,dimension,prop):
    return {'kind':'frozen_entity_relation','left':left,'right':right,'dimension':dimension,
        'property':prop,'value_type':prop+'/v1'}
def effect(dim,target,prop,value,receivers=(),value_type=None):
    return {'dimension':dim,'target':target,'property':prop,'value':{'type':value_type or prop+'/v1','value':value},
        'operation':'set_value','receivers':list(receivers)}
def option(name,app,targets,guards,effects,roles,scope,unresolved=()):
    return {'name':name,'application':app,'targets':targets,'guards':guards,'effects':effects,
        'role_review_proposal':roles,'new_scope_or_meaning_choice':scope,'unresolved':list(unresolved)}
SURFACE=frozen('receiver','body_geometry','surface.presence','present')
LIGHT_TYPE=lambda value:frozen('light','lighting','lighting.source.type',value)
SOURCE_E=lambda value:effect('lighting','light','lighting.source.selection',value,['receiver'],'photo.light_source_selection/v1')
THEME_LINK=link('image','topic','concept','photo.theme_owner')
GENRE_E=lambda value:effect('style','image','genre.selection',value,(), 'photo.genre/v1')

MANUAL={
0:{'meaning':'neon denotes the named illumination source; no hue, sign, city or new lamp is stated.',
 'options':[option('existing_actual_neon_source',
    'Choose the independently declared existing neon light source to contribute actual illumination to the independently declared existing receiving surface. Preserve the source identity and the receiver. This application selects a real neon source, not neon-colored grading or an imitation look. It introduces no emitter, sign, text, city, hue, direction, intensity or complete lighting arrangement.',
    ['light','receiver'],[LIGHT_TYPE('neon'),SURFACE],[SOURCE_E('neon')],['light_type'],
    'New existing-only application constraint: independent actual neon-source and receiver witnesses. The original bare noun did not state these preconditions.')],
 'alternatives':['A neon-colored imitation without an actual neon source needs a distinct clarified literal and actual owned color/treatment E; source identity cannot be fabricated from appearance.',
    'Introducing a neon emitter is a different application requiring real entity/count/subject effects and permissions; no creation branch is authored here.']},
1:{'meaning':'Both lab and LED must remain. The body does not settle laboratory-use equipment versus an actual laboratory capture setting.',
 'options':[option('existing_laboratory_use_led',
    'Choose an independently declared existing laboratory-use LED source to contribute actual illumination to the existing receiving surface. Here lab qualifies the source as laboratory-use equipment; that qualification must already be explicitly declared, not inferred from its appearance. Preserve both the LED identity and the lab-use qualification. No laboratory room, medical function, wavelength, certification, housing, color or intensity is introduced.',
    ['light','receiver'],[LIGHT_TYPE('led'),frozen('light','lighting','lighting.source.usage_context','laboratory_use'),SURFACE],
    [SOURCE_E('laboratory_use_led')],['light_type'],
    'Explicitly selects the laboratory-use reading, with a new exact custom witness. This is not proof that the original lab label uniquely means laboratory-use.',
    ['Root must choose lab-use versus actual lab-context meaning; no branch is approved by this proposal.']),
 option('existing_led_in_existing_laboratory_context',
    'Choose the existing LED source, already explicitly located in the existing laboratory, as illumination on the existing receiving surface. Preserve the independently declared laboratory and the source-to-laboratory relation. Here lab is the actual setting context, not a source brand or an invented clinical look. No room, researcher, experiment, medical property, color or source housing is created.',
    ['light','receiver','laboratory'],[LIGHT_TYPE('led'),SURFACE,
      frozen('laboratory','setting','location.type','laboratory'),link('light','laboratory','setting','location.container_owner')],
    [SOURCE_E('led_in_declared_laboratory')],['light_type','location (prerequisite only, if root accepts this reading)'],
    'Adds an existing laboratory + exact location relation as explicit preconditions. This is a narrower alternative, not a label-derived location fact.')],
 'alternatives':['If lab is an unresolved product/series name, preserve that unresolved text and keep pending; neither laboratory-use nor laboratory setting is a safe automatic expansion.']},
2:{'meaning':'softbox names a source-side modifier/device; actual shadow softness, source size and distance are not asserted.',
 'options':[option('existing_installed_softbox_source',
    'Choose illumination through the independently declared existing softbox modifier already associated with the existing light source, on the existing receiving surface. Preserve the modifier identity and the declared association. Do not add or attach equipment, change its position, or derive soft shadow transitions, angular size, distance, direction or output level from the device name.',
    ['light','modifier','receiver'],[frozen('modifier','lighting','lighting.source.modifier_type','softbox'),
      link('light','modifier','lighting','lighting.source.modifier_owner'),SURFACE],
    [effect('lighting','light','lighting.source.modifier.selection','softbox',['receiver'],'photo.light_modifier_selection/v1')],
    ['light_type'],
    'Existing already-associated modifier is one explicit application. Common entity presence is not proof of softbox identity or association.')],
 'alternatives':['Choosing an unattached existing softbox and actually installing/moving it needs explicit arrangement/relationship effects; the existing-associated precondition does not cover that application.',
    'A softbox-like rendered illumination look without an actual device is a distinct source clarification; a device name alone supplies no light_quality assignment.']},
6:{'meaning':'hard flash declares both flash source class and hard illumination quality; neither clause may disappear.',
 'options':[option('existing_actual_flash_hard_quality',
    'Choose the independently declared existing flash source as actual illumination on the existing receiving surface, and render its illumination there with the explicitly selected hard quality. Preserve the source and receiver identities. No front-facing placement, intensity, color, source size, exposure or additional equipment is specified.',
    ['light','receiver'],[LIGHT_TYPE('flash'),SURFACE],
    [SOURCE_E('flash'),effect('lighting','light','lighting.quality','hard',['receiver'])],['light_type','light_quality'],
    'Adds existing actual flash/receiver preconditions but retains two real chosen effects. A frozen conflicting quality remains a permission failure, not a prerequisite-mode waiver.')],
 'alternatives':['Imitation hard-flash appearance without an actual flash cannot inherit the actual source-type witness; it needs an explicitly distinct source literal and whole effect review.']},
7:{'meaning':'fluorescent is read here as a real light-source class; paint color, hue shift or a room do not follow.',
 'options':[option('existing_actual_fluorescent_source',
    'Choose the independently declared existing fluorescent light source as actual illumination on the existing receiving surface. Fluorescent denotes that source class here, not an object pigment or a grading look. Preserve the source and receiver identities; no tube shape, paint color, green cast, flicker, hospital, laboratory, brightness or apparatus is added.',
    ['light','receiver'],[LIGHT_TYPE('fluorescent'),SURFACE],[SOURCE_E('fluorescent')],['light_type'],
    'Makes the source-class reading and independent existing carrier explicit. The generic adjective alone does not prove an actual emitter.')],
 'alternatives':['If the intended meaning is fluorescent material behavior or object pigment, retain pending for a separately authored literal/material or color effect and its actual carrier. Do not remap a color adjective to a light-source fact.']},
8:{'meaning':'travel photograph is a photographic genre/theme, not an acquisition medium or automatic evidence of a trip.',
 'options':[option('genre_on_existing_travel_topic',
    'Apply the travel-photography genre to the existing image about its independently declared existing travel topic or travel context. Preserve that exact topic owner and the frozen participants, place and events. The choice changes the work genre; it does not create a trip, traveler, destination, vehicle or itinerary, and it does not attest to an actual capture history.',
    ['image:core_role=image','topic'],[frozen('topic','concept','photo.topic','travel_context'),THEME_LINK],
    [GENRE_E('travel')],['genre'],
    'Adds an exact existing travel-topic and image-to-topic precondition. It expressly selects the genre/topic interpretation rather than asserting an actual historical journey.')],
 'alternatives':['If the intended noun asserts a photograph actually captured during a real journey, independently declared travel capture context/history is also required. That stronger interpretation is not erased or proved by the proposed genre-only application.',
    'A generic travel-looking aesthetic with no declared travel topic is not automatically admitted by a genre label; root must explicitly approve a different literal and its actual effects.']},
10:{'meaning':'pet photography requires its pet subject matter, without inventing an animal, owner, species, companion relation or count.',
 'options':[option('genre_on_existing_declared_pet_subject',
    'Apply the pet-photography genre to the existing image about the independently declared existing animal with explicitly declared pet status. Preserve that exact animal and the image-to-subject relation. No animal, human owner, species, companion, action, anatomy or number of animals is added or inferred.',
    ['image:core_role=image','topic'],[frozen('topic','subject','entity.category','animal'),
      frozen('topic','subject','entity.pet_status','pet'),THEME_LINK],
    [GENRE_E('pet')],['genre','subject prerequisite: review only if the source application establishes primary declared subject matter'],
    'Adds exact animal + pet-status + image-topic witnesses. A category or an animal-looking depiction is insufficient, and pet status does not supply a companion endpoint.')],
 'alternatives':['A toy/portrait/depiction of a pet or an illustration of pet-photography conventions is a distinct source/application interpretation, not silently treated as an actual animal.',
    'Creating a new pet requires separate entity/subject/count and identity effects; this proposal only supplies a bounded existing-subject application.']},
11:{'meaning':'golden hour may name an actual natural-light-cycle phase or an imitation lighting look; latest time_of_day requires disambiguation.',
 'options':[option('actual_scene_natural_day_phase',
    'Set the existing scene actual day phase to golden hour within the natural-light cycle. This is an actual scene-time choice, not an imitation lighting treatment or color grade. Preserve the independently frozen place, participants and events. Neither sunrise versus sunset, clock time, sun position, weather, color, intensity nor a lamp type is specified.',
    ['scene:core_role=scene'],[],[effect('timing','scene','timing.time_of_day','golden_hour')],['time_of_day'],
    'Explicit source-intent choice changes the old coarse lighting footprint to the real timing footprint. It is an E, not already-golden-hour P/context.',
    ['The bare label does not uniquely select this reading; root adjudication required.'])],
 'alternatives':['Imitation alternative remains pending: explicitly name the actual owned lighting/color/tone treatment before authoring its E footprint. The bare phrase cannot invent warm color, softness, source geometry, a complete lighting setup or a movement.',
    'Do not keep the timing E while asserting actual-day-phase as P to evade a timing lock. A user-frozen different day phase rejects the actual-time application.']},
12:{'meaning':'soft window means window-mediated light plus explicit soft quality; a window/location must not be created from the label.',
 'options':[option('existing_window_transmitted_light_soft_quality',
    'Choose the independently declared existing light transmitted through the independently declared existing window as illumination on the existing receiving surface, and select soft illumination quality there. Preserve the existing window and exact light-through-window relation. No window, curtain, room, opening geometry, position, direction, daylight color or source apparatus is created.',
    ['light','window','receiver'],[frozen('window','subject','object.type','window'),
      frozen('light','lighting','lighting.source.path_type','window_transmitted'),
      link('light','window','lighting','lighting.source.window_owner'),SURFACE],
    [SOURCE_E('window_transmitted'),effect('lighting','light','lighting.quality','soft',['receiver'])],['light_type','light_quality'],
    'Adds exact existing window, source pathway and receiver requirements. Window is a transmission path, not an invented emission mechanism or an automatic interior-location role.')],
 'alternatives':['A window-light imitation with no actual window needs its own explicitly corrected literal and actual rendered light properties. It must not satisfy the real-window relation by naming a role.']},
13:{'meaning':'food photography has actual food subject matter; neither generic style alone nor a new dish preserves the whole meaning.',
 'options':[option('genre_on_existing_food_subject',
    'Apply the food-photography genre to the existing image about its independently declared existing food subject. Preserve that exact food subject and image-to-subject relation. No food, dish, plate, utensil, ingredient, cooking action, serving state or count is added, and the work is not automatically restricted to still life.',
    ['image:core_role=image','topic'],[frozen('topic','subject','entity.category','food'),THEME_LINK],
    [GENRE_E('food')],['genre','subject prerequisite: review primary-subject support separately'],
    'Adds existing food and image-topic witnesses. Existing raw subject_category=food is not automatically the exact native fact tuple.')],
 'alternatives':['Creating or replacing the food subject is a separate application with subject/entity/count and any actual preparation effects. A fake already-existing food P is not a substitute.',
    'If food is only a named aesthetic on nonfood subject matter, the source must explicitly distinguish that meaning before qualification.']},
14:{'meaning':'dieselpunk mood / 디젤펑크 감성 declares named visual sensibility. Old setting metadata is not evidence of a world/place; mood may be holistic aesthetic wording or an additional affective reading.',
 'options':[option('visual_aesthetic_and_named_affective_reading',
    'Apply the named dieselpunk visual aesthetic to the existing image and convey its named dieselpunk sensibility as a proposed mood reading. Preserve the frozen subjects, place and events. The mood is not a proven private emotion or physical air state. No particular emotion, historical era, industrial object, diesel engine, machinery, institution, world rule, new place or event is asserted.',
    ['image:core_role=image'],[],
    [effect('style','image','style.aesthetic.selection','dieselpunk',(), 'photo.aesthetic/v1'),
     effect('atmosphere','image','mood.presentation','dieselpunk_sensibility',(), 'photo.mood/v1')],
    ['aesthetic_trend','mood'],
    'Protective two-effect reading preserves both style and named sensibility; it explicitly changes setting to style+atmosphere. It is not proof that the original necessarily has two independent assignments.',
    ['Root must decide holistic aesthetic vs independent mood meaning; atmosphere cannot be dropped merely because it is locked.']),
 option('holistic_named_visual_sensibility',
    'Apply dieselpunk mood as the named holistic visual aesthetic sensibility of the existing image. Here mood names that visual sensibility rather than adding a separate specific emotional atmosphere. Preserve the frozen subjects, place and events. No historical period, world system, machinery, diesel device, new place, private emotion or physical air condition is supplied.',
    ['image:core_role=image'],[],[effect('style','image','style.aesthetic.selection','dieselpunk_mood',(), 'photo.aesthetic/v1')],
    ['aesthetic_trend'],
    'Alternative explicit interpretation of the complete phrase, not an automatic omission of an independently intended mood effect. Root must affirm the sense before using this smaller footprint.')],
 'alternatives':['A sustained dieselpunk world system or actual historical/industrial setting is not supplied by these words; do not preserve the legacy setting dimension as if it were positive source evidence.',
    'Retain aesthetic_trend current deny_domains documentary/craft/wildlife and every source/binding guard as applicable; this proposal does not erase catalog gates.']},
15:{'meaning':'street photography is a genre and subject-matter convention; it does not prove an actual city, street construction, crowd or candid capture history.',
 'options':[option('genre_on_existing_public_life_topic',
    'Apply the street-photography genre to the existing image about its independently declared existing public-life subject matter or public-space context. Preserve the exact topic and the existing actual location and participants. No street, city, crowd, unsuspecting person or unposed capture history is introduced or attested. The public-life topic is a required independently declared context, not a label-derived scene fact.',
    ['image:core_role=image','topic'],[frozen('topic','concept','photo.topic','public_life_context'),THEME_LINK],
    [GENRE_E('street')],['genre'],
    'Adds an explicit topic precondition without forcing a physical street. This broader genre reading needs root adjudication; it is not inferred solely from an urban tag.')],
 'alternatives':['If the intended application is literally an existing street scene, a separate narrowed source application can require exact existing location.type=street and image-topic ownership; it still cannot create a city/street or assert candid history.',
    'A purely stylistic street look with no such subject/context is not automatically equivalent; retain pending until explicitly clarified.']},
19:{'meaning':'interior photography concerns the declared interior-space subject, not generic style divorced from space or an instruction to create furniture.',
 'options':[option('genre_on_existing_interior_space_subject',
    'Apply the interior-photography genre to the existing image about its independently declared existing interior-space subject. Preserve that exact space, its structure, contents, occupants and image-to-space relation as independently frozen. No room, wall, furniture, living trace, window, lens choice or staging condition is introduced.',
    ['image:core_role=image','topic'],[frozen('topic','setting','location.type','interior_space'),THEME_LINK],
    [GENRE_E('interior')],['genre','location (prerequisite only)'],
    'Adds exact existing interior-space and image-theme ownership. The selected owner may be whichever independently declared actual space is the work topic; no automatic main/foreground owner mapping.')],
 'alternatives':['Depicting or creating a new interior is a distinct application requiring its real setting/entity/content effects; do not hide that under genre E alone.',
    'The existence of a room somewhere in a background is not by itself proof that the image is about interior space. The exact image-theme witness must also hold.']},
}

def ep(cid,target):return {'kind':'source_target','candidate_id':cid,'target':target}
def make_guard(cid,row,index):
    value={'id':'required_'+str(index),**copy.deepcopy(row)}
    for key in ['owner','left','right']:
        if key in value:value[key]=ep(cid,value[key])
    return value
def owner_plan(targets):
    rows=[]
    for target in targets:
        if ':core_role=' in target:
            target,role=target.split(':core_role=');selector={'kind':'core_role','role':role}
        else:selector={'kind':'selected_existing_owner'}
        rows.append({'target':target,'origin':'existing','introduced_by':None,'selector':selector})
    return {'schema':'photo-native-owner-bindings/v3','bindings':rows}

records=[]
for ordinal,judgment in MANUAL.items():
    row=batch['records'][ordinal];cid=row['candidate_id'];before=current['candidates'][cid]
    assert row['ordinal']==ordinal and row['status']=='pending' and row['proof'] is None
    assert before==source['candidates'][cid]==row['source_before']==row['source_after']
    compiled=old['decisions'][ordinal]
    assert digest(compiled)==row['original_compiled']['row_sha256']
    assert compiled['source_record_sha256']==digest(before)
    assert digest(authored['decisions'][ordinal])==compiled['authored_decision']['sha256']
    own={k:copy.deepcopy(v) for k,v in current['slot_bindings'].items() if v['candidate_id']==cid}
    assert own=={k:v for k,v in source['slot_bindings'].items() if v['candidate_id']==cid}
    alternatives=[]
    for proposed in judgment['options']:
        after=copy.deepcopy(before);after['content']['application']=proposed['application']
        after['effects']={'dimensions':sorted({v['dimension'] for v in proposed['effects']}),
            'properties':[{k:v[k] for k in ['dimension','target','property']} for v in proposed['effects']]}
        after['conditions']=copy.deepcopy(before['conditions'])
        if proposed['guards']:
            after['conditions']['native_guards']={'schema':'photo-native-source-guards/v2',
                'rules':[make_guard(cid,g,i) for i,g in enumerate(proposed['guards'])]}
        deltas=[]
        for key in ['effects','conditions']:
            if before[key]!=after[key]:deltas.append({'pointer':'/'+key,'before_exists':True,'after_exists':True,
                'before':copy.deepcopy(before[key]),'after':copy.deepcopy(after[key]),'reason':proposed['new_scope_or_meaning_choice']})
        deltas.append({'pointer':'/content/application','before_exists':False,'after_exists':True,
            'after':proposed['application'],'reason':proposed['new_scope_or_meaning_choice']})
        alternatives.append({'name':proposed['name'],'source_after':after,'source_after_sha256':digest(after),
            'exact_top_delta':deltas,'proposed_owner_map':owner_plan(proposed['targets']),
            'manually_selected_whole_effect_assignments':copy.deepcopy(proposed['effects']),
            'frozen_requirements_are_new_explicit_application_preconditions':copy.deepcopy(proposed['guards']),
            'role_review_proposal_not_binding_change':proposed['role_review_proposal'],
            'new_scope_or_meaning_choice':proposed['new_scope_or_meaning_choice'],'unresolved':proposed['unresolved']})
    records.append({'ordinal':ordinal,'candidate_id':cid,'direct_meaning_review':judgment['meaning'],
        'original_source':copy.deepcopy(source['candidates'][cid]),'source_current':copy.deepcopy(before),
        'original_and_current_sha256':digest(before),'own_bindings_whole_unchanged':own,
        'exact5B_row':copy.deepcopy(compiled),'exact5B_row_sha256':digest(compiled),
        'native_pending_rationale':row['rationale'],'literal_application_options':alternatives,
        'other_interpretations_kept_pending':judgment['alternatives']})

primary=['light_type','light_quality','lighting','light_color','time_of_day','genre','aesthetic_trend','mood','world']
neighbors=sorted({v for k in primary for v in catalog[k]['neighbors']})
additional=['subject','location','prop','companion_animal','environment_detail','background_element','subject_count']
read_specs=sorted(set(primary+neighbors+additional))
payload={'schema':'photo-native-source-application-proposals/v1','author':'/root/native_evidence',
    'purpose':'Manual alternatives for root adjudication; no proof, native signature, acceptance, status update or binding migration.',
    'input_pins':pins,'direct_read_scope':{'actual_pending_ordinals':list(MANUAL),'whole_source_records':13,
        'whole_compiled5B_rows':13,'own_binding_records':13,'whole_latest_specs':len(read_specs),
        'primary_specs':primary,'immediate_neighbors':neighbors,'additional_boundaries':additional,
        'comparison_only_approved_rows_read':[3,4]},
    'full_specs_read':{k:copy.deepcopy(catalog[k]) for k in read_specs},
    'common_protocol_and_custom_witness_boundary':{
        'existing_shared_neutral_presence':{'dimension':'subject','property':'entity.presence','value_type':'entity.presence/v1','value':'present'},
        'genre_selection_namespace_seen_in_actual_root_rows3_4':{'dimension':'style','property':'genre.selection','value_type':'photo.genre/v1'},
        'new_custom_witnesses_are_not_neutral_defaults':['lighting.source.type','lighting.source.usage_context','lighting.source.modifier_type',
            'lighting.source.modifier_owner','lighting.source.path_type','lighting.source.window_owner','surface.presence','object.type',
            'location.type','location.container_owner','photo.theme_owner','photo.topic','entity.category','entity.pet_status'],
        'required_exact_binding':'Caller selects source-local targets explicitly against an independently frozen graph; guard endpoints remain own CID namespace/base RID. No first owner, role/category->anatomy, raw subject_category->native fact, array-subset, implicit alias or candidate-informed core enrichment.',
        'core_authoring':'Every new custom tuple/relation must be independently and directly authored with active source spans and required protection before candidate discovery. Missing/unknown cannot be filled from these proposals or labels.',
        'choice_effects':'Existing identity/topic P are not choices. Each source option retains explicit nonempty E for actual illumination, genre, day-phase, aesthetic and/or mood selection. Locks remain separately strict; source correction cannot merely rename an E to P/context.'},
    'records':records,'qualified_or_approved_records_generated':0,'proofs_or_native_signatures_generated':0,
    'prohibited_mutations_or_provider_network_calls':0,
    'limits':['Source label ambiguity is not resolved by structural validation. Every option adds explicit interpretation/application constraints requiring root whole-after adjudication.',
        'The proposed existing-only applications do not cover actual creation/replacement; no count/subject/setting effect is silently waived.',
        'Old own bindings are preserved as evidence, including world for dieselpunk; role review proposals are not automatic binding edits.',
        'Manual source effects and conditions are proposals, not actual source changes, runtime tests, native qualification or image proof.']}
assert set(MANUAL)=={0,1,2,6,7,8,10,11,12,13,14,15,19}
assert not OUT.exists()
assert all(hashlib.sha256(Path(p['file']).read_bytes()).hexdigest()==p['raw_sha256'] for p in pins)
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(OUT),'records':len(records),'literal_options':sum(len(v['literal_application_options']) for v in records),
    'full_specs_read':len(read_specs),'raw_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'canonical_sha256':digest(payload)},ensure_ascii=False))
