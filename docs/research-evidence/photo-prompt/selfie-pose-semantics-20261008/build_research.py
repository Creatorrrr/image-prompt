"""Build research drafts only. Output is confined to this evidence directory."""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]

def dump(name, data):
    assert '/' not in name and name.endswith('.json')
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

GROUPS = [
    '표정 중심 셀카', '머리 방향·시선 중심 셀카', '볼·턱에 손을 대는 셀카',
    '눈·입 주변 손동작과 얼굴 가리기', 'V·캐릭터형 손동작', '하트·호감·교감 손동작',
    '머리카락·옷·액세서리를 만지는 셀카', '기본 카메라 높이·크롭 변형',
    '0.5배 초광각·과장된 원근 셀카', '상반신 거울 셀카', '서서 찍는 전신 거울 셀카',
    '앉기·쪼그리기 거울 셀카', '누운 자세·휴식형 셀프포트레이트',
    '일상 행동·소품을 이용한 셀카', '두 사람·그룹·포토부스 셀카',
    '성인 패션·부두아·관능적 셀카', '반항·도발·코믹·액션 연출', '빛·반사·흔들림을 활용하는 셀카',
]
GROUP_SOURCES = {
    1:['S03','S04'], 2:['S16'], 3:['S09'], 4:['S09'], 5:['S07'], 6:['S09'],
    7:['S01','S10'], 8:['S01','S02'], 9:['S02','S13'], 10:['S11','S12'],
    11:['S14'], 12:['S10'], 13:['S10'], 14:['S01','S10'], 15:['S01','S12'],
    16:['S09','S10'], 17:['S17'], 18:['S01','S02','S12','S18'],
}
EXTRA_SOURCES = {6:['S05','S06'],24:['S07'],31:['S08'],39:['S19'],
                 44:['S07'],45:['S07'],56:['S23'],130:['S20'],154:['S26']}

# These are review references, often covering only one component. They are not
# equivalence claims and they do not import scene/age/wardrobe defaults.
REUSE = {
 1:['pv_smile_closed'],2:['pv_smile_teeth'],3:['pv_smile_teeth'],4:['ae_smize'],5:['ae_squinch'],
 7:['ae_pucker'],8:['pv_parted_lips'],9:['pv_asymmetric_mouth'],10:['ae_nose_wrinkle','pv_smile_closed'],
 11:['pv_gaze_direct'],12:['pv_head_turn'],13:['pv_head_turn'],14:['pv_head_tilt'],
 15:['pv_chin_down','pv_gaze_up'],16:['pv_chin_up','pv_gaze_down'],17:['pv_gaze_offcamera'],18:['pv_gaze_down'],
 19:['pv_eyes_closed'],20:['pv_wink'],23:['pv_chin_support','pv_clenched_fist'],
 24:['pv_clenched_fist'],25:['pv_flower_chin'],26:['pv_palms_up'],27:['pv_finger_gun'],28:['pv_chin_support'],
 30:['pv_cupped_hands'],31:['pv_relaxed_fingers'],33:['pv_shush'],34:['pv_self_cover_hands'],35:['pv_self_cover_hands'],
 36:['pv_splayed_fingers'],38:['pv_palms_down'],39:['pv_temple_touch'],40:['ae_hand_mouth'],
 41:['pv_v_sign'],42:['pv_v_sign'],43:['pv_v_sign'],44:['pv_v_sign'],45:['pv_v_sign'],46:['pv_double_v'],47:['pv_double_v'],
 48:['pv_cat_paw'],
 55:['pv_arm_heart'],59:['pv_thumbs_up'],60:['pv_foreshortened_reach'],65:['pv_lapel_grip'],66:['pv_lapel_grip'],
 77:['pc_pc30_component_2','pc_px08_component_3'],78:['pc_pc30_component_4'],
 81:['ultrawide_near_far_scale_expansion'],82:['pv_foreshortened_reach'],83:['pv_foreshortened_reach','pv_splayed_fingers'],
 84:['ultrawide_near_far_scale_expansion'],85:['ultrawide_near_far_scale_expansion'],
 86:['ultrawide_near_far_scale_expansion'],87:['pv_knee_hug','ultrawide_near_far_scale_expansion'],
 90:['pv_side_by_side'],101:['pv_single_support'],
 104:['pv_wide_stance'],105:['pv_single_support'],106:['pv_negative_space_arms'],107:['pv_toe_light_touch'],
 108:['pv_wall_shoulder_support'],109:['pv_head_turn'],110:['pv_rear_three_quarter','pv_head_turn'],
 111:['pv_cross_leg_floor'],113:['pv_knee_hug'],114:['pv_seated_legs_extended'],
 115:['pv_squat_grounded'],116:['pv_squat_grounded'],117:['pv_seated_upright'],118:['pv_knee_over_knee'],119:['pv_reverse_chair'],
 121:['pv_supine'],122:['pv_side_lying'],123:['pv_prone_forearms'],124:['pv_side_lying'],
 125:['pv_seated_upright'],126:['pv_arms_behind_head'],127:['pv_knee_hug','pv_curled_side'],128:['pv_sheet_wrap'],
 129:['pv_prone_feet_raised'],130:['pv_heel_sit'],131:['pv_mug_grip'],
 139:['pv_head_turn'],142:['pv_head_shoulder_pair'],144:['pv_back_hug'],145:['pv_circle_group'],146:['pv_staggered_group'],
 152:['pv_rear_three_quarter'],153:['pv_collarbone_touch'],154:['pv_rear_three_quarter'],
 155:['pv_single_support','pv_negative_space_arms'],156:['pv_wrists_cross_overhead','pv_arms_behind_head'],
 157:['pv_robe_edge_hold','pv_sheet_wrap'],158:['pv_side_lying'],159:['pv_negative_space_arms'],160:['ae_lip_bite'],
 162:['pv_thumb_hook'],165:['pv_foreshortened_reach','pv_clenched_fist'],166:['pv_finger_gun'],
 169:['ae_knitted_brow','ae_upper_lip'],170:['pv_chin_down','pv_gaze_direct'],
 176:['rb_local_motion_blur_candidate'],
}
NEW = {4,6,21,22,23,24,26,27,28,29,30,31,32,34,35,36,37,38,42,43,44,45,46,47,49,50,
       51,52,53,54,56,57,58,60,61,62,63,64,67,68,69,70,71,73,74,76,91,92,93,94,95,96,97,99,
       112,113,117,120,126,133,135,136,140,143,147,148,149,150,163,164,167,168,175,178,179,180}
TWO_HAND = {24,25,30,46,47,53,54,55,56,58,127,148,156,161,163,164}
MIRROR = set(range(91,121)) | {147,175}
P0 = {4,5,6,8,11,14,15,16,21,24,25,34,35,36,41,44,45,50,51,54,56,71,73,77,78,79,
      81,83,86,91,92,93,94,95,96,97,99,101,103,111,115,119,130,143,147,148,167,168,175,176,178,179,180}
RELATION = {
 1:('main_subject.face.mouth_corners','rise_beside','main_subject.face.closed_lips'),
 2:('main_subject.face.teeth','visible_between','main_subject.face.lips'),
 3:('main_subject.face.cheeks','rise_beside','main_subject.face.open_smile'),
 4:('main_subject.face.eye_apertures','narrow_with','main_subject.face.cheek_rise'),
 5:('main_subject.face.lower_eyelids','approach','main_subject.face.irises'),
 6:('main_subject.face.upper_lip','projects_more_than','main_subject.face.lower_lip'),
 7:('main_subject.face.lips','project_forward_from','main_subject.face.plane'),
 8:('main_subject.face.upper_lip','separated_by_small_gap_from','main_subject.face.lower_lip'),
 9:('main_subject.face.mouth_corner_a','higher_than','main_subject.face.mouth_corner_b'),
 10:('main_subject.face.nose_scrunch','co_occurs_with','main_subject.face.smile'),
 11:('main_subject.face.eye_axes','point_toward','camera.active_lens'),
 12:('main_subject.head.face_yaw','differs_from','main_subject.body.torso_yaw'),
 13:('main_subject.face.profile_contour','faces_laterally_to','camera'),
 14:('main_subject.head.roll','differs_from','main_subject.body.thorax_roll'),
 15:('main_subject.face.eye_axes','look_above','main_subject.head.face_forward_axis'),
 16:('main_subject.face.eye_axes','look_below','main_subject.head.face_forward_axis'),
 17:('main_subject.face.eye_axes','point_away_from','camera.active_lens'),
 18:('main_subject.face.eye_axes','point_toward','declared_lower_target'),
 19:('main_subject.face.upper_eyelid_margins','meet','main_subject.face.lower_eyelid_margins'),
 20:('main_subject.face.closed_eye_a','contrasts_with','main_subject.face.open_eye_b'),
 21:('main_subject.hand.index_tip','touches','main_subject.face.cheek'),
 22:('main_subject.hand.palm','supports_configuration','main_subject.face.cheek'),
 23:('main_subject.face.chin','rests_on','main_subject.hand.knuckles'),
 24:('main_subject.hands','lie_below','main_subject.face.cheeks'),
 25:('main_subject.hands','frame_below','main_subject.face.chin'),
 26:('main_subject.hand','frames_below','main_subject.face.chin'),
 27:('main_subject.hand.thumb','lies_under','main_subject.face.chin'),
 28:('main_subject.face.chin','rests_on','main_subject.hand.dorsum'),
 29:('main_subject.hand.thumb_and_index','pinch','main_subject.face.cheek'),
 30:('main_subject.hands','cup','main_subject.face.cheeks'),
 31:('main_subject.hand.curled_digits','lie_near','main_subject.face'),
 32:('main_subject.hand.index_tip','touches_outside','main_subject.face.lip'),
 33:('main_subject.hand.index','stands_vertical_before','main_subject.face.lips'),
 34:('main_subject.hand','occludes','main_subject.face.lateral_half'),
 35:('main_subject.hand','occludes','main_subject.face.selected_eye'),
 36:('main_subject.face.eye','appears_through','main_subject.hand.digit_gap'),
 37:('main_subject.hand.palm','touches','main_subject.face.forehead'),
 38:('main_subject.hand','lies_above','main_subject.face.brow'),
 39:('main_subject.hand.fingertips','touch','main_subject.face.temple'),
 40:('main_subject.hand','occludes','main_subject.face.mouth'),
 41:('main_subject.hand.index','diverges_from','main_subject.hand.middle'),
 42:('main_subject.hand.v_digits','frame_beside','main_subject.face.outer_eye'),
 43:('main_subject.hand.v_digits','lie_below','main_subject.face.chin'),
 44:('main_subject.hand','reaches_toward','camera.lens'),
 45:('main_subject.hand.v_digits','lie_above','main_subject.head.crown'),
 46:('main_subject.hands.v_pair','lie_above_opposite_sides_of','main_subject.head'),
 47:('main_subject.hand_a','higher_than','main_subject.hand_b'),
 48:('main_subject.hand.curled_digits','continue_beyond','main_subject.hand.flexed_wrist'),
 49:('main_subject.hand.grouped_fingers','lie_beside','main_subject.face.forehead_edge'),
 50:('main_subject.hand.thumb','diverges_from','main_subject.hand.little_finger'),
 51:('main_subject.hand.thumb','crosses','main_subject.hand.index'),
 52:('main_subject.hand.curve','frames_beside','main_subject.face.cheek'),
 53:('main_subject.hands.curve_pair','frame_opposite_sides_of','main_subject.face.cheeks'),
 54:('main_subject.hands','bound','heart_aperture'),
 55:('main_subject.arms','bound_around','main_subject.head'),
 56:('main_subject.hands.selected_ear_digits','form_peaks_above','heart_aperture'),
 57:('main_subject.hand.curve','bounds_half_of','open_heart_space'),
 58:('main_subject.face.eye','appears_through','heart_aperture'),
 59:('main_subject.hand.thumb','points_up_from','main_subject.hand.folded_digit_base'),
 60:('main_subject.hand.index','points_toward','camera.active_lens'),
 61:('main_subject.hand.fingers','guide_behind','main_subject.ear'),
 62:('main_subject.hand.fingers','lie_over','main_subject.forehead.hairline'),
 63:('main_subject.hand','grips','main_subject.hair.ponytail'),
 64:('main_subject.hair.strand','curves_around','main_subject.hand.finger'),
 65:('main_subject.hand','touches','main_subject.wardrobe.collar'),
 66:('main_subject.hand','grips','main_subject.wardrobe.lapel'),
 67:('main_subject.wardrobe.sleeve','covers','main_subject.hand'),
 68:('main_subject.hand','grips_and_lowers','main_subject.accessory.glasses'),
 69:('main_subject.hand','touches','main_subject.accessory.glasses_frame'),
 70:('main_subject.hand','grips','main_subject.accessory.cap_brim'),
 71:('camera.lens','at_height_of','main_subject.face.eyes'),
 72:('camera.lens','slightly_above','main_subject.face.eyes'),
 73:('main_subject.capture_arm','holds_above','camera'),
 74:('camera.lens','looks_down_on','main_subject.head.crown'),
 75:('camera.lens','below','main_subject.face.eyes'),
 76:('camera','rests_near','support_surface.floor'),
 77:('setting.vertical_lines','tilt_relative_to','image.vertical_axis'),
 78:('image.crop','cuts_selected_edges_of','main_subject.face'),
 79:('image.frame_edge','cuts_through','main_subject.face.lateral_half'),
 80:('setting.projected_area','larger_than','main_subject.projected_area'),
 81:('main_subject.head','nearer_than','main_subject.feet'),
 82:('main_subject.capture_arm','projects_diagonally_from','image.corner'),
 83:('main_subject.free_hand','nearer_than','main_subject.face'),
 84:('prop','nearer_than','main_subject.face'),
 85:('main_subject.foot.shoe','nearer_than','main_subject.face'),
 86:('image.edge_object_projection','stretches_relative_to','image.center_object_projection'),
 87:('main_subject.knee','nearer_than','main_subject.face'),
 88:('setting.sky','lies_behind','main_subject.head_and_shoulders'),
 89:('main_subject.projected_area','smaller_than','room.projected_area'),
 90:('main_subject.face','nearer_than','partner_subject.body'),
 91:('phone','occludes','main_subject.face'),92:('phone','occludes','main_subject.face.lateral_half'),
 93:('main_subject.face.eye','visible_beyond','phone.edge'),94:('phone','lies_below','main_subject.face.chin'),
 95:('phone','lies_beside','main_subject.face.cheek'),96:('main_subject.face.eyes','look_at','phone.screen'),
 97:('main_subject.face.eyes','look_at','phone.reflected_lens'),99:('mirror_pair','reflect','main_subject'),
 98:('main_subject.reflection','lies_lateral_to','mirror.center'),
 100:('image.crop','isolates','main_subject.upper_wardrobe'),
 101:('main_subject.principal_support_leg','supports_configuration_of','main_subject.pelvis'),
 102:('main_subject.foot_a','anterior_to','main_subject.foot_b'),
 103:('main_subject.lower_leg_a','crosses_at_ankle','main_subject.lower_leg_b'),
 104:('main_subject.foot_a','laterally_separated_from','main_subject.foot_b'),
 105:('main_subject.pelvis','laterally_offset_from','main_subject.shoulder_midpoint'),
 106:('main_subject.elbow','separated_by_gap_from','main_subject.torso'),
 107:('main_subject.heel','clears','support_surface.floor'),
 108:('main_subject.shoulder_or_back','contacts','wall.plane'),
 109:('main_subject.torso.side','faces','mirror.plane'),
 110:('main_subject.torso.back','faces','mirror.plane'),
 111:('main_subject.shin_a','crosses_before_pelvis_with','main_subject.shin_b'),
 112:('main_subject.knee_a','higher_than','main_subject.knee_b'),
 113:('main_subject.knee_a','rises_above','main_subject.folded_leg_b'),
 114:('main_subject.legs','extend_diagonally_from','main_subject.pelvis'),
 115:('main_subject.feet','support_low_squat_configuration_of','main_subject.pelvis'),
 116:('main_subject.bent_knees','lie_below_oblique','main_subject.torso'),
 117:('main_subject.pelvis','rests_on','chair.seat_front'),120:('main_subject.back','contacts','sofa.front'),
 118:('main_subject.thigh_a','crosses_above','main_subject.thigh_b'),
 119:('main_subject.torso','faces','chair.backrest'),
 121:('main_subject.torso.back','rests_on','support_surface'),
 122:('main_subject.torso.side','rests_on','support_surface'),
 123:('main_subject.forearms','contact_in_front_of','prone_supported_torso'),
 124:('main_subject.torso','reclines_against','sofa.support_surface'),
 125:('main_subject.pelvis','rests_on','bed.mattress_edge'),
 126:('main_subject.arm','reaches_behind','main_subject.head'),
 127:('main_subject.arms','wrap','main_subject.bent_knees'),
 128:('blanket','wraps','main_subject.shoulders_and_torso'),
 129:('main_subject.feet','clear_surface_behind','main_subject.prone_torso'),
 130:('main_subject.pelvis','lowers_toward','main_subject.heels'),
 131:('cup.rim','lies_below','main_subject.face.eyes'),133:('book','occludes','main_subject.face.selected_region'),
 132:('main_subject.hand','holds','requested_food_or_utensil'),
 134:('flower.head','lies_below','main_subject.face.nose'),135:('tool.tip','contacts','main_subject.face.declared_target'),
 136:('toothbrush.head','contacts_or_approaches','main_subject.face.mouth'),
 137:('main_subject.advancing_leg','lies_anterior_to','main_subject.support_leg'),
 138:('main_subject.hair.strands','deflect_laterally_from','main_subject.hair.roots'),
 139:('main_subject.head.yaw','differs_from','main_subject.shoulder_yaw'),
 140:('vehicle.side_window','lies_beside','main_subject.face'),
 141:('main_subject.face','at_similar_depth_to','partner_subject.face'),
 142:('main_subject.head','rests_on','partner_subject.shoulder'),143:('main_subject.hand','meets','partner_subject.hand'),
 144:('partner_subject.arms','wrap','main_subject.torso'),147:('mirror','reflects','requested_actor_group'),
 145:('requested_actor_group.faces','gather_below','camera'),
 146:('requested_actor_group.heads','form_height_triangle_in','image'),
 148:('four_panels','preserve_identity_of','declared_actor'),149:('designated_actor.expression','differs_from','actor_group.expression'),
 150:('main_subject.face','at_height_of','animal_subject.face'),153:('main_subject.hand','touches','main_subject.clavicle'),
 151:('main_subject.shoulder','lies_above','existing_off_shoulder_neckline'),
 152:('existing_garment.back_opening','frames','main_subject.back'),
 154:('main_subject.rear_body_region','dominates','selected_crop'),
 155:('main_subject.pelvis','offset_over','main_subject.support_leg'),
 156:('main_subject.arms','rise_above','main_subject.head'),
 157:('main_subject.hand','grips','existing_robe_or_towel_edge'),
 158:('main_subject.arm','supports_configuration_of','main_subject.reclining_torso'),
 159:('bright_window','lies_behind','main_subject.side_silhouette'),
 160:('main_subject.face.upper_teeth','contact','main_subject.face.lower_lip'),
 161:('main_subject.forearm_a','crosses_before_torso_with','main_subject.forearm_b'),
 162:('main_subject.free_hand','enters','existing_pocket_opening'),
 163:('main_subject.forearms','rise_above','main_subject.bent_elbows'),
 164:('main_subject.fists','lie_before_opposite_sides_of','main_subject.face'),
 165:('main_subject.fist','nearer_than','main_subject.face'),
 166:('main_subject.hand.index','extends_beside_raised','main_subject.hand.thumb'),
 167:('main_subject.hand.middle_finger','extends_between','main_subject.hand.folded_neighbor_digits'),
 168:('main_subject.hand.index_and_little','extend_beside','main_subject.hand.folded_middle_and_ring'),
 169:('main_subject.face.upper_lip','lifts_to_expose','main_subject.face.teeth'),
 170:('main_subject.face.eye_axes','point_toward','camera.active_lens'),
 171:('window.source','illuminates_front_of','main_subject.face'),
 172:('window.source','illuminates_side_of','main_subject.face'),
 173:('main_subject.face.lit_half','brighter_than','main_subject.face.shadow_half'),
 174:('rear_light_source','illuminates_edges_of','main_subject.hair'),
 175:('mirror','reflects','phone.flash'),178:('hand_mirror','reflects','main_subject.face'),
 176:('main_subject.moving_region_trail','contrasts_with','stationary_scene_edges'),
 177:('window_occluder','casts_bands_on','main_subject.receiving_surface'),
 179:('glass_plane','overlays_reflection_on','transmitted_exterior'),180:('light_source','casts_shadow_on','support_surface'),
}

TREND_ROWS = [
 ('Gen Z Pout / 젠지 파우트',[6]),('Unbothered / Nonchalant Selfie',[6,17,18]),
 ('0.5 Selfie / Point-five Selfie',[71,81,82,83,86]),('High-angle 0.5 Selfie',[73,74,81]),
 ('Big-hand Perspective',[83]),('Extreme Close-up',[78]),('Half-face Mirror Selfie',[92,93]),
 ('Off-center Mirror Selfie',[98]),('Outfit-check Mirror Selfie',[94,101,102,109]),
 ('Floor Mirror Selfie',[111,113,115,120]),('Look-away Selfie',[17,18]),
 ('Cheek-touch / Face-touch',[21,22,30]),('Finger-to-lip / Chin-touch',[23,28,32]),
 ('Loose V-sign',[41,42,44,45,47]),('Tiny Heart / Finger Heart',[51,52,54]),
 ('Scrunched Expression',[10]),('Flash Selfie',[175]),('Motion / Blurry Selfie',[176]),
 ('Overhead Group Selfie',[145]),('Coordinated Group Pose',[146,148,149]),
]

# Reviewed positive Korean descriptions. They are equivalents of these local
# components, not broad mood aliases or copied negative examples.
KO_COMPONENTS = {
 4:['볼과 눈꼬리 주변이 가볍게 올라간다','양 눈이 부드럽게 좁아진 채 열려 있다','입술은 중립이거나 아주 조금만 굽어진다'],
 6:['윗입술이 작은 파우트로 조금 앞으로 나온다','아랫입술의 돌출은 과장된 키시 페이스보다 작다','눈과 입꼬리는 변화가 크지 않은 윤곽을 유지한다'],
 21:['한 검지 끝이 지정한 볼에 닿는다','접점은 눈 아래 입 옆의 볼에 놓인다','손은 같은 손목과 전완으로 이어진다'],
 24:['두 개의 주먹이 각각 양 볼 아래에 놓인다','얼굴은 두 주먹 사이 중앙에 남는다','각 주먹은 서로 다른 손목과 팔로 이어진다'],
 28:['손등 면이 턱 아랫면을 향한다','턱이 지정한 손등 면에 닿는다','손목은 뒤집히지 않고 같은 전완에 이어진다'],
 34:['세운 손바닥이 얼굴 한쪽 절반을 가린다','반대쪽 눈과 볼은 손 바깥에 보인다','가리는 손은 같은 인물의 팔로 이어진다'],
 35:['한 손이 지정한 눈 부위만 가린다','코와 입은 그 손 바깥에 남아 보인다','가리는 손바닥이나 손등이 같은 손목으로 이어진다'],
 36:['손가락들이 얼굴 앞에서 서로 벌어진다','한쪽 눈이 손가락 사이 틈으로 보인다','틈 양쪽 손가락은 같은 전경 손에 속한다'],
 44:['검지 중지의 브이가 아래와 앞을 향한다','포즈 팔이 렌즈 쪽으로 뻗는다','브이 손은 얼굴 앞에서 한 손목으로 이어진다'],
 45:['검지 중지 브이가 정수리 중앙 위에 놓인다','정수리가 브이 밑부분 바로 아래에 놓인다','올린 손목이 포즈를 취하는 인물의 팔로 이어진다'],
 46:['두 브이가 머리의 서로 반대쪽 위에 놓인다','머리가 서로 다른 두 브이 아래에 남는다','각 손이 서로 다른 팔로 이어진다'],
 51:['엄지와 검지가 작은 모양으로 교차한다','교차점에 구별되는 두 손가락 끝이 보인다','두 손가락이 같은 한 손목에 속한다'],
 54:['양손의 굽힌 손가락들이 하트 윗곡선을 만든다','양 엄지가 아래쪽 만나는 점을 만든다','두 손 사이에 하트 모양 빈 공간이 남는다'],
 61:['손끝이 작은 머리 가닥을 귀 뒤로 넘긴다','같은 가닥이 귀의 윤곽 뒤를 지나간다','귀와 접촉 손은 별개의 윤곽으로 남는다'],
 67:['소매 끝이 손 대부분을 덮는다','지정한 손끝만 소매 입구 밖에 보인다','가려진 손목이 같은 소매 안의 팔로 이어진다'],
 91:['쥔 폰이 반사된 눈 코 입을 가린다','거울 속 한 손이 그 폰을 실제로 쥔다','폰과 인물이 같은 반사 공간 안에 보인다'],
 92:['쥔 폰이 반사된 얼굴의 한쪽 부위를 가린다','폰 가장자리 옆에 한쪽 눈과 볼이 보인다','손 폰 얼굴이 일관된 같은 반사 공간을 공유한다'],
 93:['폰 몸체가 반사된 얼굴 대부분을 가린다','한쪽 눈이 폰 위나 옆 가장자리 밖에 보인다','폰이 거울 속 같은 인물의 쥔 손에 연결된다'],
 94:['폰이 거울 속 턱 아래에 놓인다','얼굴 전체가 그 폰 위로 드러난다','거울 속 한 손이 가슴 윗부분의 폰을 쥔다'],
 95:['폰이 거울 속 볼의 바깥 옆에 놓인다','얼굴 윤곽이 폰과 떨어져 보인다','쥔 손이 같은 반사 공간에서 기기를 잡는다'],
 96:['두 눈의 방향이 실제로 쥔 화면 쪽으로 향한다','화면 대상은 얼굴 아래나 옆에 놓인다','반사된 시선이 같은 물리 화면 위치와 맞는다'],
 97:['눈이 반사된 사용 렌즈 위치를 향한다','사용 렌즈가 거울 속 폰 뒷면에 보인다','눈 렌즈 관계가 같은 물리 반사 안에서 일관된다'],
 99:['서로 다른 방향의 두 물리 거울면이 보인다','같은 인물이 두 거울에서 일관된 다른 면으로 비친다','폰과 손 관계가 선택한 반사 경로와 맞는다'],
 143:['첫 인물의 한 손이 하트 절반을 만든다','다른 인물의 한 손이 반대 절반을 만든다','각자 소유의 두 반쪽이 하트 빈 공간 둘레에서 만난다'],
 148:['네 개의 패널이 지정한 인물 정체성을 보존한다','패널마다 얼굴이나 손 구성이 달라진다','비슷한 프레임이 순서 있는 네 패널을 연결한다'],
 167:['가운데손가락이 손바닥 중앙에서 펴진다','나머지 손가락들은 그 뿌리 주위에 구별되어 접힌다','제스처 손이 인물 자신의 손목으로 이어진다'],
 168:['검지와 새끼손가락이 각각 펴진다','중지와 약지는 접힌 채 남는다','엄지는 선택한 접힘 또는 누름 위치를 유지한다'],
 175:['보이거나 반사된 기기 플래시가 거울 장면에 놓인다','거울의 플래시 정반사가 지정한 화면 영역에 보인다','요청한 얼굴이 그 반사 옆이나 일부 뒤에 놓인다'],
 178:['한 손이 경계가 있는 작은 거울을 잡는다','거울면에 같은 얼굴 일부의 반사가 보인다','실제 얼굴과 반사 얼굴이 선택한 보기 기하와 맞는다'],
 179:['한 유리면이 바깥 장면을 투과한다','같은 인물의 반사가 투과된 장면 위에 겹친다','반사와 바깥 장면의 깊이 밝기 단서가 구별된다'],
 180:['광원이 인물 그림자를 받는 면에 드리운다','그 면에 연결된 머리 몸통 팔다리의 그림자가 보인다','벽이나 바닥이 그림자를 받는 표면으로 남는다'],
}
PIXEL_PROJECTIONS = {
 71:{1:('main_subject.face','the face presents a nearly frontal eye level perspective')},
 73:{2:('main_subject.body','upper facial planes and a downward receding body agree with a raised viewpoint')},
 74:{1:('main_subject.body','crown and shoulders are viewed predominantly from above against a support surface')},
 76:{1:('composition','a low viewpoint presents the actor above it with room verticals receding upward')},
 140:{3:('composition','the actor is viewed within a recognizable vehicle cabin beside the side window')},
}

def effects_for(n, slot):
    base = {
      'expression': [('expression','main_subject','face.expression')],
      'gaze_engagement': [('pose','main_subject','body.gaze_target')],
      'body_orientation': [('pose','main_subject','body.orientation')],
      'body_pose': [('pose','main_subject','body.support_configuration')],
      'hand_pose': [('pose','main_subject','body.hand_configuration')],
      'contact_point': [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.contact_target')],
      'action': [('action','main_subject','action.phase'),('pose','main_subject','body.contact_target')],
      'capture_context': [('camera','capture_camera','capture.mode'),('pose','main_subject','body.capture_hand_role')],
      'composition': [('composition','image','spatial_arrangement')],
      'subject_framing': [('framing','image','crop')],
      'relational_action': [('relationship','declared_actors','spatial_relation'),('pose','declared_actors','body.configuration')],
      'lighting': [('lighting','image','source_target_relation')],
      'motion': [('camera','capture_camera','exposure_motion_relation')],
    }[slot]
    if n in {71,73,74,76}: base += [('camera','capture_camera','camera.position')]
    if n in {91,92,93,94,95}: base += [('framing','main_subject','face.occlusion')]
    if n in {96,97}: base += [('camera','capture_camera','reflection_path')]
    if n in {57,58}: base += [('composition','image','hand_face_negative_space')]
    if n in {63,64}: base += [('appearance','main_subject','hair.placement')]
    if n == 67: base += [('appearance','main_subject','wardrobe.sleeve_placement')]
    if n in {68,69,70}: base += [('appearance','main_subject','accessory.placement')]
    if n in {133,135,136}: base += [('pose','main_subject','body.hand_configuration')]
    if n == 135: base += [('appearance','main_subject','makeup.application')]
    if n == 140: base += [('setting','declared_vehicle','cabin_window_relation')]
    if n == 147: base += [('camera','capture_camera','reflection_path')]
    if n == 148: base += [('format','image','panel_count'),('expression','declared_actor','face.expression')]
    if n == 149: base += [('expression','declared_actors','face.expression_distribution')]
    if n == 150: base += [('camera','capture_camera','camera.position')]
    if n == 175: base += [('camera','capture_camera','flash'),('composition','image','reflection_glare_region')]
    if n in {99,178,179}: base += [('camera','capture_camera','reflection_path')]
    return [{'dimension':d,'target':t,'property':p} for d,t,p in dict.fromkeys(base)]

def capture_policy(n):
    if n==133:
        return {'mode':'one_hand_grip_or_fixed_two_hand_grip','posing_hands_variants':[1,2],
                'condition':'책을 한 손으로 잡는 변형과 두 손으로 잡는 변형을 먼저 선택한다. 두 손을 쓰면 동일 인물의 촬영 손은 남지 않는다.'}
    if n in TWO_HAND:
        return {'mode':'fixed_self_portrait_or_other_camera_holder','posing_hands_per_primary_actor':2,
                'capture_hands_per_primary_actor':0,'condition':'한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.'}
    if n == 143:
        return {'mode':'fixed_or_handheld_by_one_participant','posing_hands_per_actor':1,
                'capture_hands_possible':1,'condition':'두 사람 각자 한 손의 하트라면 참가자 한 명의 다른 손으로 폰 촬영이 가능하다.'}
    if n in MIRROR:
        return {'mode':'physical_mirror_capture','capture_hands':1,'posing_hand_budget_max':1,
                'condition':'물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.'}
    return {'mode':'resolved_from_request','capture_hands_if_handheld':1,'posing_hand_budget_if_handheld':1,
            'condition':'포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.'}

def main():
    inv = json.loads((OUT/'existing-inventory.json').read_text())
    sources = json.loads((OUT/'sources.json').read_text())['sources']
    candidates_by_id = {}
    for r in inv['records']:
        if r['kind']=='candidate': candidates_by_id.setdefault(r['id'],[]).append(r)
    units=[]; original=[]; reuse=[]; unresolved=[]
    for line in (OUT/'seed-research.tsv').read_text().splitlines():
        n,ko,en,slot,obs,boundary,confusion,visibility=line.split('|');n=int(n)
        group=(n-1)//10+1; uid=f'SF{n:03d}'
        components=[]
        for i,bit in enumerate(obs.split(';'),1):
            owner,phrase=bit.split('::',1)
            components.append({'id':f'component_{i}','owner':owner,'visible_phrase_en':phrase,
                               'evidence_domain':'capture_instruction_or_projection_consistency' if owner=='camera'else'visible_configuration_proposal'})
        sub,typ,obj=RELATION[n]
        relations=[{'id':'visible_geometry','type':typ,'subject':sub,'object':obj}]
        for owner in dict.fromkeys(c['owner'] for c in components):
            if owner.startswith('main_subject.'):
                relations.append({'id':f'owner_{len(relations)}','type':'belongs_to','subject':owner,'object':'main_subject'})
        refs=[]
        for cid in REUSE.get(n,[]):
            rows=candidates_by_id.get(cid,[])
            if not rows:
                unresolved.append({'research_unit_id':uid,'requested_id':cid,'reason':'not found in snapshot; not represented as a verified reuse reference'})
                continue
            # Prefer the component source over a broad dictionary entry.
            row=next((r for r in rows if 'extension' in r['file']),rows[0])
            refs.append({'id':cid,'slot':row['slot'],'file':row['file'],'ko':row.get('ko'),'en':row.get('en'),
                         'reuse_status':'component_review_only','constraints':'접촉 대상·손 개수·좌면·의상·시점이 같아야 재사용한다. 해당 ID가 전체 셀카 변형의 동등성을 입증하지 않는다.'})
        if refs: reuse.append({'research_unit_id':uid,'existing_refs':refs})
        decision='new_or_specialized_draft' if n in NEW else ('compose_existing_components' if refs else 'literal_research_then_inventory_review')
        if n==56: decision='geometry_draft_name_activation_deferred'
        if n==130: decision='reuse_heel_sit_geometry_bambi_name_deferred'
        exact=[f'{ko} 포즈',f'{en} pose']
        if n==4: exact=['입 중립형 눈웃음','eye smile with neutral lips']
        if n==56: exact=['하트 빈 공간과 두 귀 봉우리가 함께 보이는 손 모양']
        if n in {91,92,93,94,95}: exact=[f'{ko} 거울 셀카',f'{en} with visible mirror and held phone']
        if n==96: exact=['실제 폰 화면을 보는 거울 셀카','mirror selfie looking at the held screen']
        if n==97: exact=['거울 속 촬영 렌즈 응시','gaze at the active lens reflection']
        unit={'id':uid,'seed_number':n,'group':group,'group_ko':GROUPS[group-1],'label_ko':ko,'label_en':en,
              'priority':'P0' if n in P0 else 'P1','proposed_slot':slot,
              'definition_ko':confusion,'components':components,'relations':relations,
              'confusion_boundary_id':boundary,'confusion_boundary_ko':confusion,'observability_ko':visibility,
              'capture_policy':capture_policy(n),'effects':effects_for(n,slot),'integration_decision':decision,
              'source_ids':list(dict.fromkeys(['S25']+GROUP_SOURCES[group]+EXTRA_SOURCES.get(n,[]))),
              'source_scope':'S25는 표제어와 원문 범위다. 외부 출처는 해당 분류의 원리 또는 지정된 명칭만 지지한다. 개별 관찰·관계·후보·게이트는 연구 설계 제안이다.',
              'proposed_exact_terms':exact,'proof_status':'research_only_not_runtime_or_pixel_qualified',
              'claim_limits':['표정·제스처만으로 실제 감정·성격·세대·동의·능력·사건 이력을 확정하지 않는다.',
                              '지정된 인물 수·연령·정체성·체형·의상·참조 외형·크롭은 보존한다.',
                              '필수 관계가 가려지면 UNOBSERVABLE, 일부만 맞으면 PARTIAL이며 전체 PASS로 세지 않는다.']}
        if n in {67,63,68,69,70}: unit['claim_limits'].append('해당 머리 모양·소매·안경·모자가 이미 있는 장면에서만 접촉 후보로 사용한다.')
        if n in {56,130}: unit['claim_limits'].append('통상 명칭의 대표 형태·문화 용법 확인이 남아 있다. 이름 기반 hard activation은 현재 초안에서 제안하지 않는다.')
        if group==16: unit['claim_limits'].append('원문의 성인 패션·부두아 맥락은 유지하되 자세 자체를 성적 의도·특정 의상·노출의 필수 요건으로 만들지 않는다.')
        units.append(unit)
        original.append({'id':f'pose_{n:03d}','number':n,'group':group,'ko':ko,'en':en,
                         'origin':'numbered table row verified in browser; headings and labels transcribed into seed-research.tsv'})
    assert [u['seed_number'] for u in units]==list(range(1,181))
    candidate_proposals=[];profiles=[]
    for u in units:
        if u['seed_number'] not in NEW:continue
        variants=[('base',u['components'])]
        if u['seed_number']==133:
            variants=[]
            for variant,owner,phrase in [('one_hand','main_subject.hand','one hand visibly grips the book spine or lower edge'),
                                         ('two_hand','main_subject.hands','two separate hands grip opposite outer book edges')]:
                variants.append((variant,[{'id':'component_1','owner':owner,'visible_phrase_en':phrase}]+u['components'][1:]))
        if u['seed_number']==135:
            variants=[]
            for name,tool,target in [('lipstick','lipstick tip','outer lip'),('brush','cosmetic brush bristles','cheek'),('puff','cosmetic puff surface','cheek')]:
                variants.append((name,[{'id':'component_1','owner':'main_subject.hand','visible_phrase_en':f'the actor hand visibly grips one {tool}'},
                                      {'id':'component_2','owner':'tool','visible_phrase_en':f'the {tool} contacts the same actor {target}'},
                                      {'id':'component_3','owner':'main_subject.face','visible_phrase_en':f'the {target} and tool contact remain readable outside the gripping fingers'}]))
        for variant,components in variants:
            capture_checks=[]
            pixel_components=[]
            for i,c in enumerate(components,1):
                revised=dict(c)
                if i in PIXEL_PROJECTIONS.get(u['seed_number'],{}):
                    owner,phrase=PIXEL_PROJECTIONS[u['seed_number']][i]
                    capture_checks.append(c['visible_phrase_en'])
                    revised.update(owner=owner,visible_phrase_en=phrase)
                pixel_components.append(revised)
            cid=f'sf_{u["seed_number"]:03d}_{variant}';pid=f'sf_profile_{u["seed_number"]:03d}_{variant}'
            phrases=[c['visible_phrase_en'] for c in components]
            label=f'{u["label_ko"]} / {variant}' if variant!='base' else u['label_ko']
            variant_relations=u['relations']
            if u['seed_number']==135:
                contact_part='surface'if variant=='puff'else'tip_or_bristles'
                target='lip_outer_edge'if variant=='lipstick'else'cheek'
                variant_relations=[{'id':'tool_contact','type':'contacts','subject':f'tool.{contact_part}','object':f'main_subject.face.{target}'},
                                   {'id':'tool_grip','type':'gripped_by','subject':'tool.handle_or_body','object':'main_subject.hand'}]
            entry={'id':cid,'ko':label,'en':'; '.join(phrases),'weight':0.5,'tags':['selfie_visual_form',u['proposed_slot']],
                   'aliases':[label],'keywords':[label,u['label_en']],'embedding_text':'; '.join([label,u['label_en']]+phrases+KO_COMPONENTS.get(u['seed_number'],[])),
                   'concept_units':phrases,'relations':variant_relations,'affected_dimensions':list(dict.fromkeys(e['dimension']for e in u['effects'])),
                   'affected_properties':u['effects'],'core_assertion_discovery':True}
            proposal={'research_unit_id':u['id'],'suggested_slot':u['proposed_slot'],'variant':variant,
                      'draft_status':'research_only_needs_semantic_and_activation_review','candidate_draft':entry,
                      'context_prerequisites_ko':[u['capture_policy']['condition'],u['observability_ko']],
                      'capture_spec_checks':capture_checks,
                      'pixel_proof_scope':'기기 배율·실제 렌즈 높이/거리·촬영자·셔터 원인은 픽셀만으로 계측하지 않는다. 원본에서는 요구된 투영·깊이·가림·접촉의 일관성을 판단한다.',
                      'not_a_live_extension':'이 wrapper는 assets의 extension에 그대로 import하지 않는다. 기존 ID 동등성·property 잠금·slot 정책을 검토한 뒤 내부 entry만 채택한다.'}
            if u['seed_number']==56:proposal['draft_status']='observable_proposal_only_named_convention_unverified'
            if u['seed_number']==133:
                proposal['context_prerequisites_ko'][0]='책 잡는 손 하나를 남는 손으로 사용한다.'if variant=='one_hand'else'양손이 책을 잡으므로 고정 촬영 또는 다른 촬영자가 필요하다.'
            candidate_proposals.append(proposal)
            terms=u['proposed_exact_terms'] if variant=='base'else[f'{u["label_ko"]} {variant} 도구 접촉']
            ac=[]
            pixel_phrases=[c['visible_phrase_en'] for c in pixel_components]
            for i,c in enumerate(pixel_components,1):
                phrase=c['visible_phrase_en']
                ko=KO_COMPONENTS.get(u['seed_number'],[])
                terms_local=[phrase]+([ko[i-1]]if variant=='base'and ko and i not in PIXEL_PROJECTIONS.get(u['seed_number'],{})else[])
                ac.append({'id':f'component_{i}','match_terms':terms_local,'evidence_field':f'component_{i}_phrase',
                           'evidence_terms':terms_local,'min_content_words':3,
                           'instruction':f'Bind this already requested or explicitly adopted configuration to {c["owner"]}: {phrase}.',
                           'render_gate':{'id':f'vo_{cid}_{i}','review_scale':'native' if u['seed_number']in {5,21,29,51,56,58,96,97,135,160,167,168}else'both',
                                          'description':f'{phrase}. Inspect the complete relation in original pixels; partial fails and hidden prerequisites are unobservable.'}})
            profile={'id':pid,'category':'observable_selfie_configuration',
                     'activation':{'exact_terms':terms,'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,
                                   'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[
                                       {'id':'self_portrait_or_visible_form_context','any_terms':['selfie','self portrait','pose','portrait','hand','face','mirror','셀카','셀피','셀프포트레이트','포즈','손','얼굴','거울']}] }},
                     'semantics':{'definition':'; '.join(pixel_phrases),'paraphrase_examples':pixel_phrases+KO_COMPONENTS.get(u['seed_number'],[]),'visual_components':pixel_phrases,
                                  'contrast_examples':[u['confusion_boundary_ko']],'claim_limits':u['claim_limits']},
                     'concept_candidate':{'concept_terms':phrases+[label], 'core_assertion_discovery':True,
                                          'affected_dimensions':entry['affected_dimensions'],'affected_properties':entry['affected_properties']},
                     'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
                                           'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
                     'reject_substitutes':[u['confusion_boundary_id']],'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':ac}}
            profiles.append({'research_unit_id':u['id'],'variant':variant,'candidate_id':cid,
                             'draft_status':'not_registered_compiler_check_is_not_activation_approval','profile_draft':profile,
                             'activation_review_required_ko':'문맥·부정·사용자 정의·소유 대상·인물 수·크롭을 확인한다. 정확한 이름이라도 현재 초안은 등록되지 않았으며 hard obligation이 아니다.'})
    routing=[{'seed_id':r['id'],'research_unit_ids':[f'SF{r["number"]:03d}'],'relation':'same numbered research scope; not runtime hard activation'}for r in original]
    trend=[]
    for i,(label,ns)in enumerate(TREND_ROWS,1):
        sid=f'trend_{i:02d}';trend.append({'id':sid,'label':label,'origin':'first summary table in the referenced conversation'})
        routing.append({'seed_id':sid,'research_unit_ids':[f'SF{n:03d}'for n in ns],
                        'relation':'advisory research routes to related visual mechanisms; no automatic alias equivalence'})
    dump('original-keywords.json',{'numbered_row_count':180,'summary_row_count':20,'groups':GROUPS,'numbered_rows':original,'summary_rows':trend})
    dump('research-units.json',{'schema_version':'selfie-research-units/v1','units':units})
    dump('keyword-routing.json',{'routing':routing})
    dump('candidate-proposals.json',{'proposals':candidate_proposals})
    dump('visual-profile-proposals.json',{'proposals':profiles})
    dump('reuse-plan.json',{'reuse':reuse,'unresolved_requested_ids':unresolved,'equivalence_status':'references exist; complete semantic equivalence is not approved'})
    source_map={s['id']:s for s in sources}
    md=['# 셀카 포즈 상세 연구 카드','', '2026-10-08 KST · 180개 원문 행을 각각 하나의 연구 카드로 보존했다. 관찰 문장과 관계는 설계 제안이며 운영 등록·이미지 심사는 아직 실행하지 않았다.',
        '', '출처는 명칭 또는 촬영 원리를 지지한다. 아래 프레이밍·소유·후보 설계 전부를 각 기사에서 확인했다는 뜻이 아니다.', '']
    for u in units:
        if(u['seed_number']-1)%10==0:md+=['',f'## {u["group"]}. {u["group_ko"]}','']
        md +=[f'### {u["seed_number"]:03d}. {u["label_ko"]} / {u["label_en"]}', '',
              f'- 의미·혼동 경계: {u["definition_ko"]}',
              '- 관찰 구성: '+' / '.join(f'{c["owner"]}: {c["visible_phrase_en"]}'for c in u['components']),
              '- 방향 관계: '+'; '.join(f'{r["subject"]} → {r["type"]} → {r["object"]}'for r in u['relations']),
              f'- 촬영·손 역할: {u["capture_policy"]["condition"]}',f'- 가시성: {u["observability_ko"]}',
              f'- 반영 판단: {u["priority"]} · {u["integration_decision"]}',
              '- 출처 범위: '+', '.join(f'[{sid} — {source_map[sid]["title"]}]({source_map[sid]["url"]})'for sid in u['source_ids']), '']
    (OUT/'research-cards.md').write_text('\n'.join(md)+'\n')
    dump('package-counts.json',{'numbered_rows':180,'summary_rows':20,'research_units':len(units),
                              'owned_observation_proposals':sum(len(u['components'])for u in units),'candidate_drafts':len(candidate_proposals),
                              'profile_drafts':len(profiles),'source_records':len(sources),
                              'reuse_unit_rows':len(reuse),'reuse_references':sum(len(r['existing_refs'])for r in reuse),
                              'unresolved_reuse_hints':len(unresolved),'source_evidence_statuses':dict(Counter(s['evidence_status']for s in sources)),
                              'decision_counts':dict(Counter(u['integration_decision']for u in units))})
    print((OUT/'package-counts.json').read_text())

if __name__=='__main__':main()
