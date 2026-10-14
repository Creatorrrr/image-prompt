import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored';J=json.loads((A/'native_08250_06250_07250.prepared.json').read_text());S={r['ordinal']:r for r in J['records']};D=[]
def f(p,q,d,t,prop,m,v):return dict(pointer=p,quote=q,dimension=d,target=t,property=prop,mode=m,value={'type':prop+'/v1','value':v},operation='set_value' if m=='effect' else None,receivers=[],requires=[],requires_status='pending_exact_owner_selected_RID_and_receiver_design')
def row(o,meaning,facts,roles,pending):
 s=S[o]
 for f in facts:
  v=s['exact_5B_after']
  for k in f['pointer'][1:].split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
  assert f['quote'] in v
 D.append(dict(ordinal=o,candidate_id=s['candidate_id'],source_after=s['exact_5B_after'],compiled_locator=s['compiled_review_locator'],source_bindings=s['all_own_source_bindings'],references=s['complete_reference_records'],reference_bindings=s['complete_reference_bindings'],actual_rids=s['actual_realization_ids'],meaning=meaning,manual_fact_drafts=facts,roles=roles,pending=pending,proof=None,status='pending',whole_source_and_full_compiled_5B_directly_read=True))
E='effect';C='context'
row(6605,'Adult hotel worker verifies reservation before room assignment, blank-keycard issue and service direction to a guest.',[
 f('/content/embedding_text','an adult hotel front-desk worker','age','worker','age.presentation',E,'adult'),
 f('/content/embedding_text','verifies one guest reservation','action','worker','action.verifies_reservation',E,'one_guest_reservation_verified'),
 f('/content/embedding_text','assigns a room','action','worker','action.assigns_room',E,'room_assignment'),
 f('/content/embedding_text','issues a blank keycard','action','worker','action.interaction.issues_keycard',E,'blank_keycard_issued_to_actual_guest'),
 f('/content/embedding_text','a blank keycard','subject','keycard','props.keycard',E,'blank_keycard'),
 f('/content/embedding_text','blank keycard','role','keycard','prop.state.printed_content',E,'blank'),
 f('/content/embedding_text','points out one service direction','action','worker','action.interaction.service_direction',E,'one_service_direction_to_guest'),
 f('/content/en','verifying one reservation before issuing a room keycard','timing','procedure','procedure.order.reservation_before_issue',C,'verification_before_issue')],
 {'action':'actual operations cannot be reduced to procedure context','relational_action':'worker/guest actual endpoints','procedure_step':'explicit ordered task, one selected instantaneous step needed','prop':'blank keycard','prop_state':'blank surface is independent actual state','age_presentation':'adult worker explicit embedding; guest age not inherited','participant_role':'declared hotel worker/guest roles','wardrobe_style':'uniform expressly optional'},
 ['No all steps visibly simultaneous, actual prior verification hidden success or unreadable reservation details claimed.','Actual worker/guest/keycard/room-allocation receiver owners and procedure RID need explicit design; one guest not same as one total person. for_any human/role and optional direct action0.48 binding retained. Actual room assignment is a nonvisual E allocation, not dropped because unseen.'])
row(6606,'Adult engineer/artist/resident-steward groups belong to an original Black future community, without a prescribed skin tone or active task.',[
 f('/content/en','adult engineers, artists, and resident stewards','subject','groups','subject.declared_participants',E,['engineers','artists','resident_stewards']),
 f('/content/en','adult engineers, artists, and resident stewards','age','groups','age.presentation',E,'adult'),
 f('/content/en','engineers, artists, and resident stewards','role','groups','participant.role.inventory',E,['engineer','artist','resident_steward']),
 f('/content/en','in an original Black future community','identity','groups','identity.background.black_future_community',C,'declared_original_Black_future_community_membership'),
 f('/content/en','an original Black future community','concept','world_context','world.original_black_future_community',C,'declared_original_future_community')],
 {'subject':'actual groups no exact3 people','age_presentation':'literal adult across coordinated group, individual owner scope pending','participant_role':'declared participation/occupation context not visual identity proof','declared_person_background':'explicit community membership no skin ancestry inference','world':'declared future community; no invented technical institutions','skin_tone':'not supplied by Black community declaration','action':'role nouns do not create engineering/art-making acts'},
 ['Source subject-only effects omit adult/declared roles/background. Creation versus existing application unresolved; metadata age_context_only cannot erase actual age declaration.','Community background is not uniform morphology, exact nationality, technology, clothing or biological ancestry. optional subject1 empty binding retained.'])
row(6607,'One grounded hydra torso/limb system supports at least3 complete separately rooted necks and nonmerged heads/jaws on same shoulders.',[
 f('/content/en','a single-body hydra','subject','hydra','entity.declared_type',E,'single_body_hydra'),
 f('/content/embedding_text','one grounded creature torso and limb system','count','hydra','subject.count.bodies',E,'one'),
 f('/content/embedding_text','one grounded creature torso and limb system','pose','hydra','body.support',E,'grounded_torso_and_limb_system'),
 f('/content/embedding_text','at least three complete neck paths','body_geometry','hydra','anatomy.connection.neck_inventory',E,'at_least_three_complete_neck_paths'),
 f('/content/embedding_text','roots remain separate on the same shoulder system','body_geometry','hydra','anatomy.connection.separate_neck_roots',E,'separate_roots_same_owned_shoulder_system'),
 f('/content/embedding_text','head jaws and orientations do not merge','body_geometry','hydra','anatomy.connection.head_jaw_separation',E,'nonmerged_owned_heads_and_jaws'),
 f('/content/en','three or more separately rooted necks and heads','species','hydra','body.species.multi_neck_hydra',E,'hydra_multi_neck_anatomy')],
 {'subject':'one actual fantasy creature','species_marker':'declared morphological distinguishing pattern','anatomical_connection':'same-body shoulder roots and complete neck/head continuity','subject_count':'one body; head count is not people count','body_pose':'embedding grounded support independent; exact support contacts not invented','body_orientation':'nonmerging orientation constraint not a selected angle','body_form':'neck-path completeness/topology alone does not specify volume or contour'},
 ['Exact>=3 anatomical count constraint and owned parts must become actual bounded/native realization design; no arbitrary exact3 default or exact body.parts equality from minimum.','No snake bundle, duplicate body, three-headed-dog substitution, real-life species, extra people or inferred unspecified limb count. optional subject0.4 empty binding retained.'])
row(6608,'Measurement-derived limited-resolution ring reconstruction encloses one roughly circular central brightness depression and one brighter side.',[
 f('/content/en','a measurement-derived emission ring','subject','representation','props.measurement_reconstruction',E,'declared_measurement_derived_emission_ring_reconstruction'),
 f('/content/embedding_text','one roughly circular central depression enclosed by a thick','composition','representation','composition.enclosed_central_depression',E,'one_roughly_circular_central_depression_enclosed_by_thick_ring'),
 f('/content/embedding_text','limited-resolution emission ring','camera','representation','image.detail.resolution',E,'limited_resolution_on_reconstruction_carrier'),
 f('/content/embedding_text','one side is visibly brighter than the opposite side','camera','representation','image.detail.local_brightness_relation',E,'one_ring_side_brighter_than_opposite'),
 f('/content/en','measurement-derived','concept','reconstruction_context','record.context.measurement_derivation',C,'declared_derivation_not_actual_measurement_certification')],
 {'prop':'representation carrier, no physical space-ring invention','composition':'enclosure and asymmetric depiction arrangement','image_detail':'local reconstruction resolution and visible tonal contrast; outer photograph not automatically degraded','light_intensity':'not real illumination incident on a ring','object_structure':'2D graphic representation not physical bounded object geometry','surreal_physics_detail':'not a portal/eclipse or direct black sphere'},
 ['Empty E footprint omits depicted image geometry/tonal relation/detail. Exact representation carrier versus outerimage and declared measurement derivation provenance need mapping.','requires_primary_any_tags compact_object_visualization and optional prop0.86 binding remain exact. No black-hole mass/temperature, realdata accuracy or direct captured spherical object claimed.'])
row(6609,'Small simple camera body with fixed lens window, flash window and viewfinder lies on visible work surface; winding feature conditional when visible.',[
 f('/content/en','a small simple camera body','subject','camera_prop','props.camera_type',E,'small_simple_camera_body'),
 f('/content/en','on a visible working surface','composition','camera_prop','prop.position.working_surface',E,'on_actual_visible_working_surface'),
 f('/content/en','fixed lens window flash window and basic viewfinder','appearance','camera_prop','object.structure.optical_windows',E,['fixed_lens_window','flash_window','basic_viewfinder']),
 f('/content/ko','간단한 필름 카메라 외형','appearance','camera_prop','object.geometry.declared_film_camera_appearance',E,'simple_film_camera_appearance'),
 f('/content/aliases/0','Disposable Camera','subject','camera_prop','props.declared_camera_subclass',E,'disposable_camera_label_not_manufacture_proof')],
 {'prop':'depicted camera, no capture camera transfer','prop_placement':'actual work-surface relation','object_structure':'explicit camera windows/viewfinder independent new144spec fit','contact_point':'on-surface wording requires actual contact/support review, not guessed handhold','camera':'no acquisition-device optics change from depicted camera'},
 ['Winding feature only when visible; no unconditional component E or hidden installation/removal. Exact optional-visibility guard/RID pending.','Surface is not automatically a table or foreground surface. Disposable alias and film-camera KO retained as declared subclass/appearance, without actual manufacture, loading, power or operability proof. setting-only effects omit actual prop/geometry/placement; optional prop0.45 empty binding retained.'])
out=dict(schema='photo-native-manual-bulk-checkpoint/v1',task_name='/root/review_08250_09250',model='gpt-6.1-sol',reasoning_effort='high',prepared_total=1000,read_range=[6605,6610],actual_direct_read_count=5,records=D,complete_native_proof_count=0,operating_native_qualified_count=0,limitations='Incomplete draft: empty requires/receivers and grouped/conditional values not qualified native proof. No complete source-unit coverage or admission claimed.');p=A/'native_08250_06250_07250.06605_06610.checkpoint.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(hashlib.sha256(p.read_bytes()).hexdigest(),sum(len(x['manual_fact_drafts']) for x in D))
