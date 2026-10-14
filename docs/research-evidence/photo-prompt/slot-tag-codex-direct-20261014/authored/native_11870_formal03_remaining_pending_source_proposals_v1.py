"""Manually authored source-only alternatives. Serialization/hashes never approve native facts."""
import copy,datetime,gzip,hashlib,json,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
D=R/'native-inputs/prepared/review11870-01250-01300-03'
P=json.load(open(D/'PREPARED-PACKET.json'));I=json.load(open(D/'INPUT.json'));B=json.load(open(R/'native_batches/review11870-01250-01300-03/BATCH.json'))
S=json.load(gzip.open(I['current_snapshot']['file'],'rt'));C=json.load(open(R/'CATALOG-FINAL-144-V4.json'))
O=json.load(open('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json'))
def sha(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def filepin(path):
 data=Path(path).read_bytes();return {'file':str(path),'file_sha256':hashlib.sha256(data).hexdigest(),'sha256':sha(json.loads(data))}
def E(d,t,p):return {'dimension':d,'target':t,'property':p}
def effects(*rows):return {'dimensions':sorted({x['dimension'] for x in rows}),'properties':list(rows)}
def choice(en,ko):return {'en':en,'ko':ko,'embedding_text':en,'concept_units':[en],'relations':[]}
def branches(rows):return {'mode':'one','branches':[{'id':rid,'conditions':{},'effects':eff,'context_terms':[]} for rid,eff in rows]}
# Each item below is an independent manual meaning decision, not inferred from old tags/effects.
PLANS={
1253:{'specs':['proxemics','social_cue','narrative_clue','narrative_core','prop','prop_placement'],
 'classification':['source_meaning_requires_root_choice','generic_actual_endpoint_selection','existing_application_proposed_not_authorized_by_noun'],
 'reason':'The full original has counter-caused formal distance but does not distinguish physical access/spacing from a social reading. Neither the old target participants nor a physical access barrier is an original assertion. The two alternatives below are root choices, not an invented canonical OR.',
 'options':[
 {'id':'physical_counter_separation','contract':'Use only an independently declared existing counter and the actual existing participant endpoints explicitly selected by the caller. Select physical counter-mediated separation between those same endpoints, with the formal social reading stated by the source. The caller must identify those endpoints and the actual counter-between-endpoints relation; no extra person, precise gap, occupation, intimacy or access entitlement is supplied. The formal reading and separation are selected effects, not frozen context.',
  'effects':effects(E('relationship','participants','spacing.counter_mediated_separation'),E('relationship','participants','relationship.distance.formal_reading')),
  'meaning':'Physical counter separation AND its formal reading. Root must select this interpretation before the new physical statement can be used.'},
 {'id':'social_counter_distance','contract':'Use only an independently declared existing counter and the actual existing participant endpoints explicitly selected by the caller. Select formal interpersonal distance mediated by that same counter. This alternative declares the formal relational reading without asserting a measurable gap, physical barrier or access restriction. No participant, occupation or intimacy is added; the formal counter-mediated relation is an effect rather than already frozen context.',
  'effects':effects(E('relationship','participants','relationship.distance.formal_counter_mediated')),
  'meaning':'Counter-mediated formal relational distance. This does not justify proxemics without separately positive physical spacing/access meaning.'}],
 'P':'Independent actual counter identity/presence and all selected endpoints; exact distinctness/topology must come from the actual request, not names or service tags.',
 'E':'All formal distance/counter-mediated relation meaning remains selected; physical spacing E only in the explicitly root-chosen physical interpretation.',
 'boundary':'Do not infer clerk/customer, two newly visible people, opposite-side pose, legal access, a numeric distance, friendship or emotion. Neither option currently receives a native proof.'},
1255:{'specs':['prop_placement','action','relational_action','contact_point','prop_state'],
 'classification':['source_application_clarification','generic_actual_holder_and_object_selection','existing_application_root_choice'],
 'reason':'Korean 자기 쪽 anchors near-self placement to the holder; English near the subject is made co-referential with that same existing holder. Neutral presentation is retained as a selected qualification, not a private intention or safety guarantee.',
 'options':[{'id':'same_holder_existing_item','contract':'Use only the independently declared existing holder and the existing held object explicitly selected by the caller, as distinct actual owners. The subject in the English phrase and 자기 in the Korean phrase refer to that same holder. Select that holder holding that same object neutrally near their own side. Holding, near-self placement and neutral presentation remain selected effects. Do not add an object or person, choose an object type, prescribe hand/finger geometry, aim it at another person or infer a private intention.',
 'effects':effects(E('action','holder','action.holding'),E('composition','held_object','props.placement.near_same_holder'),E('role','held_object','prop.state.neutral_presentation')),
 'meaning':'Same actual holder holds same actual object neutrally near self; no other-person endpoint.'}],
 'P':'Actual existing holder/object presence and independent actual disjointness; no primary/main owner default. Old human/domain binding eligibility remains separate.',
 'E':'holder action.holding with held_object receiver; held_object near_same_holder placement with holder receiver; neutral presentation on same object. No pre-frozen holding required.',
 'boundary':'Near-self does not mean a particular hand, exact metric distance, surrender, offering, threat, weapon, gaze or emotional neutrality.'},
1256:{'specs':['gaze_target','gaze_direction','eye_detail','prop','prop_state','visible_text'],
 'classification':['source_translation_and_modifier_scope_root_choice','explicit_original_OR','generic_actual_gaze_owner_and_target_selection','existing_application_root_choice'],
 'reason':'English supplies badge OR access card; Korean only supplies the blank badge. The original does not settle blank scope on access card. Keep both actual OR alternatives; root must decide whether a blank-card constraint is intended. Badge blankness includes Korean 글자 없는, not an inference from an ID or office tag.',
 'options':[
 {'id':'blank_badge_or_text_unspecified_access_card','contract':'Use only the independently declared existing gaze owner and existing target explicitly selected for the actual realization. Require actual owned eyes on that same gaze carrier; a role name does not create eyes. Select its gaze toward that same branch target. The badge branch selects blankness without lettering; the access-card branch makes no lettering claim. Add no person, badge or card, office, access authority, readable name or head/body orientation. The actual target and gaze remain effects rather than already frozen gaze context.',
  'ko':'글자 없는 배지 또는 출입 카드를 향한 시선',
  'realizations':{'blank_badge':choice('gaze toward a blank badge','글자 없는 배지를 향한 시선'),'access_card':choice('gaze toward an access card','출입 카드를 향한 시선')},
  'effects':{'dimensions':['expression'],'properties':[E('expression','gaze_owner','gaze.target')],'realizations':branches([('blank_badge',effects(E('role','target','prop.state.blank_without_lettering'))),('access_card',effects())])},
  'meaning':'Blank badge OR access card with unspecified text. Least added lettering constraint, but English modifier scope still requires root selection.'},
 {'id':'blank_badge_or_blank_access_card','contract':'Use only the independently declared existing gaze owner and existing target explicitly selected for the actual realization. Require actual owned eyes on that same gaze carrier. Select gaze toward that same target and its blank state without lettering in each branch. Add no actor or target, office, access authority, readable name or head/body orientation. Blank access-card meaning is an explicit root clarification choice, not a fact proved by the original Korean.',
  'ko':'글자 없는 배지 또는 글자 없는 출입 카드를 향한 시선',
  'realizations':{'blank_badge':choice('gaze toward a blank badge','글자 없는 배지를 향한 시선'),'blank_access_card':choice('gaze toward a blank access card','글자 없는 출입 카드를 향한 시선')},
  'effects':{'dimensions':['expression','role'],'properties':[E('expression','gaze_owner','gaze.target'),E('role','target','prop.state.blank_without_lettering')],'realizations':branches([('blank_badge',effects()),('blank_access_card',effects())])},
  'meaning':'Both original object alternatives retained; blank card is a root-selected modifier-scope clarification, not silent source entailment.'}],
 'P':'Actual gaze carrier, same-carrier atomic eyes presence and branch-specific existing badge/access-card identity; actual target selection and source human for_any must be consumed independently.',
 'E':'gaze_owner gaze.target with exact selected target receiver; blank_without_lettering E only on the branch whose positive text asserts it. No branch effects inherited across OR.',
 'boundary':'Never combine badge and card into a single invented access-token type or require both objects; do not infer office, employment, head direction or a released credential.'},
1258:{'specs':['action','relational_action','prop','procedure_step','contact_point'],
 'classification':['source_application_clarification','generic_actual_operator_tool_and_tested_endpoint_selection','existing_application_root_choice','safety_qualification_not_deleted'],
 'reason':'The original states actual safely-qualified voltage checking using a tester. Source does not choose operator, tester, measured endpoint, contact geometry, circuit arrangement, voltage/result or safety protocol. Naming the actual application endpoints can preserve the full activity without inventing those details.',
 'options':[{'id':'same_operator_tester_actual_voltage_check','contract':'Use only the independently declared existing human operator, existing voltage tester and actual existing tested endpoint explicitly selected by the caller. Select that same operator checking voltage safely using that same tester at that same tested endpoint. Preserve safely as a qualification of the selected checking activity; do not replace the activity or its safety qualification with frozen context or certify real-world safety from a still image. The actual endpoint topology must be supplied by the request. Do not add equipment or an operator, choose voltage/result, prescribe wiring, contact, PPE or a safety procedure, or assert successful completion.',
 'effects':effects(E('action','operator','action.checking_voltage_safely_with_same_tester')),
 'meaning':'One safely-qualified checking activity retains operator, actual tester and tested endpoint together.'}],
 'P':'Existing actual human operator, precise voltage tester identity, actual tested endpoint(s) and any required topology/disjointness. No generic existence substitution for tester type. No unmentioned electrical configuration or safe-activity witness manufactured.',
 'E':'action.checking_voltage_safely_with_same_tester on operator, receivers same tester and tested endpoint. Safe qualification remains inside the selected effect, not P/context; root must assess adequate exact safety meaning/admission before any proof.',
 'boundary':'This is a semantic source proposal, not electrical instructions or real safety certification. Do not infer a contact/hand pose, profession, current, live/dead status, measurement or completed result.'},
1264:{'specs':['aftermath_trace','prop','prop_state','prop_placement','narrative_phase','narrative_clue','object_structure'],
 'classification':['source_application_clarification','generic_actual_chair_seat_allocation_selection','existing_application_root_choice'],
 'reason':'Both overturned chair AND recently disturbed seat/place are positive, and the newer Korean correction preserves the English. The word seat/자리 does not uniquely declare the chair seat part versus a separate seating place. Require the caller to declare that actual topology, without changing AND into OR or silently merging owners.',
 'options':[{'id':'chair_and_actual_selected_seat_topology','contract':'Use only the independently declared existing chair and actual existing seat or seating place explicitly selected by the caller. The caller must declare whether that seat is an actual part of that chair or a separate seating place, retaining that exact identity/part relationship; no automatic merge or new seat is permitted. Select the chair overturned AND the same selected seat recently disturbed, with recent disturbance explicitly treated as declared prior-event history rather than inferred from arbitrary appearance. Both state and recency/history remain effects. Do not add a chair, seat, person, cause, assailant, current overturning action or an exact elapsed duration.',
 'effects':effects(E('role','chair','prop.state.overturned'),E('role','seat','prop.state.disturbed'),E('timing','seat','trace.recent_disturbance')),
 'meaning':'AND retained across actual selected chair and actual selected seat/place; caller chooses actual topology, not an alternative state.'}],
 'P':'Actual existing chair identity and seat/place identity, explicit same-chair part-of versus separate-owner relation; independent topology evidence must be consumed in fresh input. Neither distinctness nor part-of guessed. The seat prop.state footprint is provisional for an actual object/seat carrier; a place-only carrier needs a separately reviewed generic state/trace address rather than pretending it is a prop.',
 'E':'chair overturned state; seat disturbed state; prior recent-disturbance trace on same seat. A newly selected history cannot be moved to P merely because it is before the frame.',
 'boundary':'No attacker, fight, departure, exact time, injury, new participant, generalized tension, or original5B assertion that seat necessarily belongs to this chair. Exact generic topology guard support remains fresh-input work.'},
1267:{'specs':['light_shape','light_type','lighting','prop_placement','composition'],
 'classification':['irreducible_original_geometry_carrier_ambiguity','root_meaning_choice_required','existing_application_root_choice'],
 'reason':'Every positive original field is only shrine lantern grid light / 신단 등불 격자 빛. No extra original clause identifies projected receiving-surface pattern, volumetric geometry or a lantern-array layout. Three proposals below expose that ambiguity; none is approved source entailment and they are not an original OR.',
 'options':[
 {'id':'projected_grid_choice','contract':'Root interpretation choice: use only the existing shrine-lantern light source and actual existing receiving surface explicitly selected by the caller. Select shrine-lantern illumination forming a grid pattern on that same receiving surface. This projected-surface interpretation requires explicit root selection; the short original does not identify a surface. Do not add a surface, shrine location, religious event, faith, lamp technology, color or intensity.',
 'effects':effects(E('lighting','light','lighting.source.shrine_lantern'),E('lighting','light','lighting.pattern.grid_on_selected_surface')),
 'meaning':'Illumination grid on actual receiving surface; light_shape possible only after root clarification and actual source/receiver proof.'},
 {'id':'lantern_array_choice','contract':'Root interpretation choice: use only the independently declared existing shrine-lantern source array explicitly selected by the caller. Select its grid arrangement and shrine-lantern illumination, without asserting a projected grid or volumetric grid of rays. This array-layout interpretation requires explicit root selection; the short original does not distinguish source layout from light geometry. Do not add lanterns, a shrine location, religious event, faith, technology, color or intensity.',
 'effects':effects(E('composition','lantern_array','props.placement.grid'),E('lighting','light','lighting.source.shrine_lantern')),
 'meaning':'Grid is source-array placement; this does not independently support light_shape.'},
 {'id':'spatial_illumination_grid_choice','contract':'Root interpretation choice: use only the independently declared existing shrine-lantern source and actual existing illuminated spatial region explicitly selected by the caller. Select shrine-lantern illumination with grid geometry in that same region, without inventing a receiving surface or particulate scattering mechanism. This spatial-light interpretation requires explicit root selection; the short original does not identify such a region. Do not add smoke, fog, dust, religion, a shrine setting, color or intensity.',
 'effects':effects(E('lighting','light','lighting.source.shrine_lantern'),E('lighting','light','lighting.shape.grid_in_selected_region')),
 'meaning':'Actual light grid in declared spatial region; no compulsory physical surface, but region cannot be inferred.'}],
 'P':'Only independently declared actual owners appropriate to a root-chosen interpretation; no canonical receiving_surface target inherited from old5B.',
 'E':'Real shrine-lantern lighting selection and the root-chosen grid meaning remain effects. No mood/context/no-op escape. Original lighting dimension kept in every option.',
 'boundary':'Do not turn ambiguity into an automatic three-way OR, sacred deity, world/location/faith fact, grid shadow, lamp technology, brightness or warm color. Native remains pending until root selects meaning and actual owners.'},
1273:{'specs':['prop','prop_state','object_structure','scale_relation'],
 'classification':['explicit_original_OR','generic_actual_existing_branch_target_selection','existing_application_root_choice'],
 'reason':'Both EN and KO explicitly say small action figure OR doll prop. Keep both alternatives and small prop meaning in each full selected projection. Existing-target-only is a proposed application restriction; noun alone does not prove creation, add_entity or frozen scene role.',
 'options':[{'id':'existing_small_toy_or_branches','contract':'Use only the independently declared existing object explicitly selected for the actual realization. Independently require the precise identity stated by that branch. Select that same object as a small scene prop; smallness and scene-prop presentation remain effects rather than frozen context. Choose exactly one actual realization, retaining the source action-figure OR doll alternative. Do not add a toy, living actor, child, body, holder, comparative size ratio, count or motion. Original human applicability remains mandatory.',
 'realizations':{'small_action_figure':choice('a small action figure prop','작은 액션 피규어 소품'),'small_doll':choice('a small doll prop','작은 인형 소품')},
 'effects':{'dimensions':['appearance','role'],'properties':[E('appearance','toy','object.geometry.size'),E('role','toy','props.scene_role')],'realizations':branches([('small_action_figure',effects()),('small_doll',effects())])},
 'meaning':'Exactly one existing action figure OR existing doll is rendered as small prop; branch identity precise P, actual smallness/scene role E.'}],
 'P':'Existing actual object presence AND precise branch action_figure/doll identity. Human source for_any retained, not supplied by toy anatomy. No mutually exclusive whole-source conjunction of both types.',
 'E':'toy object.geometry.size small; toy props.scene_role scene_prop. No invented add_entity or living-subject effect. No scale_relation tag solely from absolute smallness.',
 'boundary':'No new entity, living child, ownership/collector, toy count or relative metric ratio. Any action-figure/doll metadata relation remains separate from an actual chosen RID. Both branch contracts still need fresh native proof.'},
1284:{'specs':['focus','image_detail','depth_of_field','eye_detail','gaze_target'],
 'classification':['source_application_owner_scope_clarification','existing_actual_face_carrier'],
 'reason':'Current contract incorrectly leaves actual eyes bound directly to primary_face. Preserve the actual face owner as carrier, require eyes atomically on that same carrier and address its eye region as focal-plane receiver; never alias a face into an eyes node. Original says precise eye focus, not generic image sharpness, and retains kpop OR album condition.',
 'options':[{'id':'same_face_carrier_owned_eyes','contract':'Use only the independently declared existing image bound to image and actual existing face carrier bound to primary_face. Independently require subject/anatomy.face.presence/anatomy.face.presence/v1/present and subject/anatomy.eyes.presence/anatomy.eyes.presence/v1/present on that same actual face carrier. Select the image focal plane precisely on the owned eye region of that same face, in the stated album-cover style. The focal-plane effect receiver is that face carrier with its explicitly identified eye-region scope; this does not rename the face owner into a separate eyes owner. Keep the original kpop-or-album eligibility guard. Do not add eyes, another face, lens, depth extent, album release or publication format.',
 'effects':effects(E('camera','image','focus.selected_plane')),
 'meaning':'Image focus plane set to eyes_of_same_selected_face, receiver actual face carrier scoped to its eyes.'}],
 'P':'Independent image existence; same actual primary_face carrier exact atomic face presence AND eyes presence, both subject dimension canonical tuples. No body.parts subset/alias or implicit eye inheritance.',
 'E':'camera/image/focus.selected_plane, select_plane, value album_cover_precise_eyes_of_same_selected_face, receiver actual primary_face eye-region scope. No image_detail substitution or preservation claim.',
 'boundary':'If native can only bind separate eye owner, this carrier-scoped representation must be handled explicitly in fresh input; do not create a second eyes node or claim parent/part identity from role labels. No proof/status changed.'},
1285:{'specs':['prop_placement','prop_state','contact_point','participant_role','relational_action'],
 'classification':['generic_actual_prop_chair_and_counterpart_selection','source_application_relational_meaning_clarification','existing_application_root_choice'],
 'reason':'Propped object is not named. Partner chair positively requires a counterpart-related chair but neither counterpart-of endpoint nor legal ownership/use designation is specified. Existing application can keep actual prop/chair/endpoints generic, while explicitly selecting counterpart-associated chair relation and propped support rather than assuming them frozen.',
 'options':[{'id':'actual_counterpart_associated_chair','contract':'Use only the independently declared existing propped object, supporting chair and actual counterpart relation endpoints explicitly selected by the caller. The caller must identify the actual chair associated with that counterpart without inferring legal ownership, current occupancy or a romantic relationship. Select that same object propped against that same counterpart-associated chair, preserving the counterpart relation and chair association as selected relational meaning rather than silently pre-frozen context. Require actual object/chair distinctness and actual support/contact topology independently. Do not add an object, chair or person, prescribe the object type or a body pose, or infer a performed propping action.',
 'effects':effects(E('composition','propped_object','props.placement.against_selected_chair'),E('role','propped_object','prop.state.propped'),E('relationship','propped_object','contact.leaning_support'),E('relationship','counterpart','relationship.role.counterpart'),E('relationship','chair','relationship.chair_association')),
 'meaning':'Actual object propped/supporting contact against actual counterpart-associated chair; association and counterpart relation not inferred from a prop target name.'}],
 'P':'Independent actual object/chair identity, actual relation endpoints, object-chair disjointness and their requested topology. Caller selection cannot supply a newly created counterpart or infer title/occupancy.',
 'E':'Placement/state/contact on same object with actual chair receiver; explicit counterpart relation and chair association retain source relational meaning as E. Root must confirm exact role-vs-association allocation before native proof.',
 'boundary':'No unnamed existing_prop old5B target treated as authority; no main actor default, partner romance/occupation, visible partner body, legally owned chair, sitting or ongoing leaning motion. Native dynamic topology remains pending.'},
1287:{'specs':['participant_role','offscreen_context','subject_framing','relational_action'],
 'classification':['generic_actual_colleague_and_colleague_of_selection','source_application_selected_relationship_and_offframe_effect','existing_application_root_choice'],
 'reason':'Colleague is relational and off-frame is an actual selected spatial/context condition. Declare existing colleague and colleague-of endpoint without creating a visible person or assuming the colleague role already true. Source human condition remains, and role/offscreen effects are not replaced by context mode.',
 'options':[{'id':'same_existing_offframe_colleague_relation','contract':'Use only the independently declared existing human colleague candidate, the actual existing person to whom that colleague relation applies, and existing image/frame explicitly selected by the caller. Independently require the two actual people to be distinct. Select the first person as colleague of that same second person and explicitly outside that same frame. Both colleague relation and off-frame relation are selected effects, not assumed frozen context. Do not add a person, make the colleague visible, infer a workplace, profession, identity, name or a performed interaction.',
 'effects':effects(E('relationship','colleague','participant.role.colleague'),E('relationship','colleague','context.offscreen.off_frame')),
 'meaning':'Same actual colleague-of endpoint and same actual frame; off-frame remains selected.'}],
 'P':'Actual existing human endpoints plus existing image/frame and independently consumed actual distinctness; exact source human for_any retained. No new counterpart from role label.',
 'E':'colleague participant.role.colleague with other_person receiver; colleague context.offscreen.off_frame with image/frame receiver. Contextual slot role does not imply fact mode context.',
 'boundary':'No visible body, numerical total person count, costume/job, speech, intimacy or performed collaboration. Old participant_role optional/contextual .82/human/domain gate unchanged, not positive proof.'},
1295:{'specs':['skin_finish','age_presentation','texture','skin_condition','character_contrast','body_region'],
 'classification':['generic_actual_owned_skin_regions_selection','source_application_visible_age_texture_contrast_clarification','existing_application_root_choice'],
 'reason':'Aged versus young skin texture is explicit, but one owner versus multiple owners is not specified. Keep two actual region endpoints caller-selected, retaining their real owner/part relation without forcing two people or a baby. Apparent local age texture is selected visual meaning, not actual chronological age or family role.',
 'options':[{'id':'actual_two_owned_skin_regions_contrast','contract':'Use only two independently declared existing skin regions explicitly selected by the caller, retaining each regions actual owner and actual part relationship. The regions must be distinct; their owners may be the same or different only as independently declared by the request. Select aged-looking skin texture on the first region contrasted with young-looking skin texture on the second region. Preserve both local texture and visible local age-presentation contrast as selected effects; do not treat selected aged/young appearance as a frozen age fact. Do not add skin, people or a baby, declare chronological ages, family relationship, disease or a specific wrinkle/pore pattern.',
 'ko':'나이 들어 보이는 피부와 젊어 보이는 피부 질감의 대비',
 'effects':effects(E('appearance','aged_region','skin.texture.age_appearance'),E('appearance','young_region','skin.texture.age_appearance'),E('age','aged_region','age.presentation.local_skin'),E('age','young_region','age.presentation.local_skin')),
 'meaning':'Actual distinct skin-region comparison, apparent aged versus young textures; no owner-count or real-age inference.'}],
 'P':'Actual existing skin regions, precise owned-skin identity and independent region distinctness/part-of/owner topology. No child/adult age P from provenance ID or family tags.',
 'E':'aged_region aged_looking texture/local skin age presentation; young_region young_looking texture/local skin age presentation; each mutually references the other for contrast. No numeric or actual age effect.',
 'boundary':'Local skin presentation does not set whole-person age or create an infant. Root must assess age_presentation local scope and current skin_finish human gate separately; no automatic character_contrast (bearing/role) or physical-microstructure texture claim.'},
1299:{'specs':['shot_scale','subject_framing','composition','relational_action','action','contact_point','hand_pose'],
 'classification':['generic_actual_owned_hand_and_exchange_endpoint_selection','exchange_kind_unresolved_requires_actual_input','existing_application_root_choice'],
 'reason':'Hands-only macro framing AND exchange are explicit. Exchange alone does not supply transferred object, exact number of people, self-versus-other topology or exact activity flavor. Hands-only may describe participant coverage or the complete frame; the proposed participant-coverage reading requires root selection and must not silently relax a complete-frame exclusion. Keep that actual activity unresolved until caller explicitly selects source-compatible exchange endpoints/type; generic framing approval must not hide exchange E.',
 'options':[{'id':'actual_selected_exchange_and_hands_only_macro','contract':'Use only the independently declared existing image, participating hands with their actual owners, and actual exchange endpoints explicitly selected by the caller. The caller must state the actual exchange type and all its required endpoints or exchanged subject matter; this source does not supply a transferred object, a new person or an exact person count. Retain the independently declared ownership, distinctness or self-owned part relationships without guessing them. Select that actual exchange AND a macro composition showing only its participating hands, preserving the hands-only coverage of the participants rather than deleting necessary exchange meaning. Exchange, macro scale and coverage remain effects. This proposal reads hands-only as participant coverage; root must explicitly resolve that scope before application if hands-only instead excludes every non-hand item in the complete frame. Do not apply until both coverage scope and actual exchange configuration are explicit; do not invent fingers, hand pose, payload or a completed transfer.',
 'effects':effects(E('framing','image','shot.scale'),E('framing','image','framing.coverage.participating_hands_only'),E('action','exchange_actor','relation.action.exchange')),
 'meaning':'Macro scale AND hands-only participant framing AND same actual exchange; actual activity type/configuration remains caller-required, not a fabricated transfer.'}],
 'P':'Independent actual image and hands, exact owned-part topology, all actual exchange endpoints and any intrinsic payload identity appropriate to explicitly chosen activity. A caller choosing actual activity is not a generic-existing-witness shortcut.',
 'E':'image macro shot.scale; image participant-hands-only coverage scoped to actual participating hands; performed exchange on actual actor with actual named endpoints/receivers. No action omission and no actual exchange frozen as P/context.',
 'boundary':'Still pending if exchange kind/endpoints or hands-only scope cannot be made explicit without adding meaning. No generic two-person handoff, prop, exact count, visible whole bodies, hand-joint geometry or completed ownership transfer inferred.'}
}

BINDING_REVIEW={
1253:'One optional/direct proxemics binding weight0.75 with empty subject_applicability; no source intrinsic condition. Physical role fit remains interpretation-dependent; current catalog human/domain applicability must be checked independently, not copied into global source.',
1255:'One optional/direct prop_placement binding weight0.82; human category plus product/jewelry/food/wildlife deny is display eligibility. Source conditions empty. Retain actual self-holder relation; do not derive human owner identity from display policy.',
1256:'One optional/direct gaze_target binding weight0.74 human plus product/jewelry/food/wildlife deny. Source for_any human is independently intrinsic and remains. Prop/blank roles require their actual branch evidence and separately assessed new policy, not union/intersection of old binding conditions.',
1258:'One optional/direct action binding weight1 with unrestricted subject_applicability; source for_any human is intrinsic and remains. Tool identity and actual action relation cannot be replaced with old binding or safety tag.',
1264:'One optional/direct aftermath_trace binding weight0.72: human category; allow disaster_risk_operations/longitudinal_place_state/visual_structure with override; deny product/jewelry/food/wildlife. These exact conditions remain display policy, no empty/default/intersection rewrite; source intrinsic conditions empty.',
1267:'One optional/direct light_shape binding weight0.62 unrestricted. No source intrinsic condition. It does not prove that grid is an illumination shape; array placement option has different role fit. Do not preserve role merely to satisfy the old binding.',
1273:'One optional/direct prop binding weight0.55 unrestricted. Source for_any human intrinsic remains in every actual RID. New size role fit cannot infer a comparative scale or human toy anatomy; actual branch identity must remain precise P.',
1284:'One optional/direct focus binding weight0.45 unrestricted. Source requires_any_tags kpop OR album intrinsic retained exactly. No binding/category can create owned eyes or actual album release; atomic same-carrier P must be consumed.',
1285:'One optional/direct prop_placement binding weight0.82 human with product/jewelry/food/wildlife deny. Display-only; source conditions empty. Contact/state/relational meaning require actual same endpoints, not copying human conditions as source identity.',
1287:'One optional/contextual participant_role binding weight0.82 human with product/jewelry/food/wildlife deny; source for_any human intrinsic. Contextual semantic_role never changes selected colleague/offframe fact mode from effect to context.',
1295:'One optional/direct texture binding weight1 unrestricted; source conditions empty. The precise owned skin meaning may support skin_finish and local age-presentation review rather than generic texture. New human gate, if applicable, is evaluated per proposed role; do not impose it on the entire source by intersection.',
1299:'One optional/direct composition binding weight0.8 unrestricted; source conditions empty. Macro/coverage/exchange individually reviewed; composition label does not authorize an extra layout effect, person count or invented exchange payload.'}
ROLE_REVIEW={
1253:'Physical option: proxemics only for actual counter separation, formal reading retained separately. Social-only option has no automatic proxemics/social_cue/narrative_core role because no physical spacing, reaction/allocation or central event is independently declared.',
1255:'prop_placement covers near-self object position; action covers holding; contact_point would require exact support/contact endpoint representation; neutral presentation state can remain untagged if no precise prop_state mapping is defensible. No relational_action inferred from neutral intent.',
1256:'gaze_target fits actual target-directed gaze, not gaze_direction/head turn. Blankness can support prop_state only where asserted; exact absence-of-lettering may require distinct text policy review. Object identity P does not automatically produce a prop role effect.',
1258:'action covers safely-qualified voltage check; relational_action can cover the full actual operator/tester/tested endpoint interaction. Tool precise P does not automatically create a prop effect. No procedure_step without a declared ordered stage; no contact_point from testing alone.',
1264:'prop_state for actual overturned chair and object-like seat state; aftermath_trace for explicitly recent disturbance history on actual carrier. No ongoing action or inferred full prior event. Seating-place carrier/property requires further role review instead of forced prop target.',
1267:'Projected and spatial-light options can fit light_shape with actual carrier; array-layout option fits prop_placement/composition as appropriate, not light_shape solely because original slot says so. Light_type requires actual shrine-lantern source selection; no complete lighting setup inferred.',
1273:'prop scene-role selection and actual small geometry may support prop/object_structure individually. Absolute smallness has no stated comparator/depth basis so does not fit scale_relation. No body/anatomical role for a toy.',
1284:'focus fits precise eye focal-plane selection. image_detail is recorded acuity; depth_of_field is extent; neither follows from eye focus. Gaze target/eye detail do not follow from the selected optical focus.',
1285:'prop_placement, prop_state and contact_point each address actual propped object/chair relation. Counterpart role/association E retained but not automatic interaction: relational_action excludes mere role/contact. Native participant-role fit needs actual counterpart endpoints.',
1287:'participant_role and offscreen_context each have explicit source meaning with actual endpoints. Neither role means a performed interaction; subject_framing requires its own actual image visibility scope, not a visible colleague.',
1295:'skin_finish microtexture and age_presentation local visible age are plausible separate meanings. Generic texture is physical organization, not an automatic duplicate skin tag; character_contrast is bearing/response/role, not skin age comparison; no skin_condition diagnosis.',
1299:'shot_scale and subject_framing for explicit macro/coverage; relational_action for actual exchange once endpoints/type are explicit. No hand_pose/contact_point solely because hands participate; composition is not an extra layout assertion merely from the word composition.'}

TARGET=[1253,1255,1256,1258,1264,1267,1273,1284,1285,1287,1295,1299]
assert sorted(PLANS)==TARGET
assert sorted(x['ordinal'] for x in B['records'] if x['status']=='pending' and x['ordinal'] not in [1266,1271,1275,1278,1296])==TARGET
bp=filepin(R/'native_batches/review11870-01250-01300-03/BATCH.json')
proposals=[]
for n in TARGET:
 cid=P['ids'][n-1250];before=P['current_records'][cid];original=P['original_records'][cid];plan=PLANS[n]
 assert before==S['candidates'][cid]
 pr=original['provenance'][0];_,slot,eid=pr['source'].split(':');oe=next(x for x in O['slots'][slot] if x['id']==eid);assert sha(oe)==pr['sha256']
 compiled=P['historical_compiled_rows'][cid];row=next(x for x in B['records'] if x['ordinal']==n)
 opts=[]
 for op in plan['options']:
  after=copy.deepcopy(before);after['content']['application_contract']=op['contract'];after['effects']=copy.deepcopy(op['effects'])
  if 'ko' in op:after['content']['ko']=op['ko']
  if 'realizations' in op:after['content']['realization_content']=copy.deepcopy(op['realizations'])
  delta=[]
  for key in ['application_contract','ko','realization_content']:
   if before['content'].get(key)!=after['content'].get(key):delta.append({'pointer':'/content/'+key,'before_exists':key in before['content'],'before':before['content'].get(key),'after_exists':True,'after':after['content'][key],'reason':plan['reason']})
  if before['effects']!=after['effects']:delta.append({'pointer':'/effects','before_exists':True,'before':before['effects'],'after_exists':True,'after':after['effects'],'reason':'Manually account for all selected positive meaning and actual owners; old coarse/empty effects are not source evidence. '+plan['E']})
  assert after['conditions']==before['conditions'] and after['provenance']==before['provenance'] and after['content']['en']==before['content']['en']
  opts.append({'option_id':op['id'],'root_choice_not_applied':True,'meaning':op['meaning'],'whole_proposed_after_source':after,'proposed_after_source_sha256':sha(after),'exact_delta':delta})
 proposals.append({'ordinal':n,'candidate_id':cid,'classification':plan['classification'],'reason':plan['reason'],
  'whole_original_source':original,'whole_before_source':before,'before_source_sha256':sha(before),'whole_original_compiled_row':compiled,'original_compiled_row_sha256':sha(compiled),
  'original_compiled_locator':I['original_decisions'].get(cid),
  'before_formal03_row':{'artifact':bp,'pointer':'/records/'+str(n-1250),'sha256':sha(row)},
  'whole_original_provenance_entry':{'pointer':'/slots/'+slot+'/'+str(O['slots'][slot].index(oe)),'sha256':sha(oe),'entry':oe},
  'complete_own_bindings':[v for v in S['slot_bindings'].values() if v['candidate_id']==cid],
  'whole_references':P['references'].get(cid,{}),'whole_reference_bindings':P['reference_bindings'].get(cid,{}),
  'prerequisite_intent':plan['P'],'selected_effect_intent':plan['E'],
  'own_binding_preservation_and_classification':BINDING_REVIEW[n],'proposed_role_and_neighbor_review':ROLE_REVIEW[n],
  'original_positive_quotes':[{'pointer':'/content/'+k,'quote':original['content'][k]} for k in ['en','ko'] if k in original['content']],
  'role_and_neighbor_boundaries':plan['boundary'],
  'relevant_full_current_specs':{k:{'sha256':sha(C[k]),'whole_spec':C[k]} for k in plan['specs']},
  'options':opts,'conditions_and_own_bindings_changed':False,
  'guard_boundary':'Prose describes required actual selection/topology but does not prove native consumption. No new native guard is asserted operational. Fresh exact input and manual typed guard/fact/map review are required.',
  'whole_source_and_original_compiled_and_own_binding_reread_complete':True,
  'formal03_status_changed':False,'proof_or_signature_created':False,'root_acceptance':False,'applied':False})
OUT={'schema':'photo-native-source-only-pending-proposals/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','method':'codex_subagent_direct_source_read',
 'assignment_sha256':sha(json.load(open(D/'ASSIGNMENT.json'))),'input_sha256':sha(I),'packet':filepin(D/'PREPARED-PACKET.json'),'current_source_sha256':sha(S),'catalog_sha256':sha(C),
 'actual_ordinals':TARGET,'proposal_count':12,'alternative_count':sum(len(x['options']) for x in proposals),'proposals':proposals,
 'boundary':'Source-only manually authored proposals. Ambiguous options are root choices, not original OR additions. Original EN retained; exact KO expansions/translations individually shown. All original conditions, provenance and self binding policy unchanged. Existing-target restrictions explicitly proposed, not proved by nouns. No proof/signature/status/operating/code/source/global/Git/provider/network changes.'}
if '--write' in sys.argv:
 assert '--reread-confirmed' in sys.argv
 OUT['whole_proposed_after_semantic_reread_complete']=True
 target=R/'authored/native_11870_formal03_remaining_pending_source_proposals_v1.json'
 assert not target.exists();target.write_text(json.dumps(OUT,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'file':str(target),'canonical_sha256':sha(OUT),'file_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'count':len(proposals),'options':OUT['alternative_count']}))
else:
 selected=[int(x) for x in sys.argv[1:]] or TARGET
 for row in proposals:
  if row['ordinal'] in selected:print(json.dumps({'ordinal':row['ordinal'],'before':row['whole_before_source'],'options':row['options'],'prerequisite_intent':row['prerequisite_intent'],'selected_effect_intent':row['selected_effect_intent'],'boundary':row['role_and_neighbor_boundaries']},ensure_ascii=False,indent=2))
