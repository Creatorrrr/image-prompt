"""Narrow per-card role proposals. No runtime binding is granted."""
DEFAULTS={
 "exchange_and_documents":["prop_state"],
 "observation_devices":["prop"],
 "body_gaze_and_hands":["body_pose"],
 "two_person_blocking":["body_pose"],
 "tailoring_and_outerwear":["garment_detail"],
 "evening_and_functional_clothing":["garment_detail"],
 "wearables_and_surface":["texture"],
}
OVERRIDES={}
def assign(roles,slugs):
 for slug in slugs.split():OVERRIDES[slug]=roles.split(",")
assign("relational_action,contact_point","direct_handoff suspended_handoff drop_placement")
assign("prop_state,prop_placement","concealment_cavity drop_spike pocket_litter identity_comparison redaction document_seal opened_flap number_pad burn_bag document_case")
assign("relational_action,gaze_target","analysis_comparison")
assign("narrative_clue","source_chain_board")
assign("body_pose,gaze_target","briefing_table window_observer")
assign("relational_action,contact_point","threshold_departure kompromat_display")
assign("prop_state","cash_envelope")
assign("contact_point,hand_pose","earpiece_contact receiver_pose")
assign("wearable_accessory","button_lens watch_camera")
assign("prop_placement","reel_console monitor_boundary concealed_device_view")
assign("gaze_target","camera_target mirror_attention")
assign("body_pose","tail_spacing")
assign("gaze_direction","sideways_glance offscreen_gaze")
assign("gaze_direction,gaze_target","downcast_gaze chin_down")
assign("body_pose,gaze_target","over_shoulder_glance listening_tilt")
assign("expression","restrained_smile tense_jaw")
assign("hand_pose,contact_point","cuff_adjustment lapel_hold loose_tie pocket_hand glasses_adjustment glove_removal glass_stem")
assign("relational_action,contact_point","back_to_back whisper_proximity other_tie ballroom_hold supported_walk")
assign("body_pose,gaze_target","divergent_gazes seated_standing")
assign("body_pose","face_to_face side_by_side threshold_standoff head_lowered raised_hands")
assign("hand_pose,prop_placement","lowered_weapon")
assign("body_pose,contact_point","restrained_seated")
assign("wardrobe_layering,garment_detail","three_piece sheer_layer")
assign("wardrobe_style,garment_detail","tuxedo_facing ivory_dinner trench_assembly")
assign("garment_detail","bow_tie cummerbund stocking_support stocking_seam opera_gloves")
assign("garment_detail,garment_fit","structured_shoulder bias_drape catsuit bodysuit jumpsuit")
assign("wearable_accessory","chest_rig plate_carrier fashion_harness cufflink_bridge tie_bar_anchor ring_on_finger lanyard_card shoulder_holster crossbody_bag")
assign("footwear,garment_detail","oxford_closure derby_closure")
assign("surface_material,texture","glossy_folds velvet_pile patent_reflection")
assign("surface_pattern","ripstop_grid pinstripe herringbone")
assign("hair_style","slickback blunt_bob finger_waves chignon")
assign("facial_hair","stubble")
assign("eye_makeup_line","winged_liner")
assign("makeup_style","smoky_gradient")
assign("lip_color_placement","bold_lip")
assign("prop_state","wig_boundary prosthetic_edge")
assign("makeup_wear_state","smudged_makeup")
assign("garment_state","wrinkled_suit torn_edge")
assign("surface_moisture","wet_patch")
assign("texture","surface_abrasion")
def roles_for(domain,slug):
 return OVERRIDES.get(slug,DEFAULTS[domain])
