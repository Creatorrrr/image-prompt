"""Reviewed equivalent language and local visual forms; no topic runtime routing."""
from __future__ import annotations
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as g
from photo_candidate_semantics import digest

EXT = "photo_prompt_cute_visual_forms_extension.json"
VIS = "photo_prompt_visual_obligations_cute_visual_forms.json"
RECORD = "cute-visual-forms-20261005-v1"

def read(p): return json.loads(p.read_text())
def write(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# Each pair is a reviewed equivalent positive realization, not a cultural definition.
REUSE = {
 "pv_flower_chin": ["양손을 펼쳐 턱 아래 양옆에 꽃잎처럼 받친다", "Both open hands frame the underside of the chin, each joined to its own wrist and forearm."],
 "pv_arm_heart": ["양팔을 머리 위로 굽혀 마주 보는 두 곡선과 하트 꼭짓점을 만든다", "Raised arms curve into two opposing heart halves with the hands meeting near the apex."],
 "pv_cat_paw": ["손목을 살짝 굽히고 손가락을 느슨하게 접어 앞발 모양을 만든다", "Loosely curled fingers and bent wrists form the chosen paw-like hand gesture."],
 "pv_v_sign": ["검지와 중지는 벌린 채 펴고 나머지 손가락은 접는다", "Extended index and middle fingers diverge into a V while the remaining fingers stay folded."],
 "pv_double_v": ["양손마다 검지와 중지로 서로 독립된 브이를 만든다", "Each of the two separately attached hands forms its own index-middle V."],
 "pv_prayer_palms": ["두 손바닥을 마주 붙이고 손끝을 나란히 세운다", "The two palms meet face to face with the fingers aligned upward."],
 "pv_clenched_fist": ["네 손가락을 손바닥으로 접고 엄지를 바깥에 둔 주먹", "Four fingers curl into the palm with the thumb outside the folded fingers."],
 "pv_splayed_fingers": ["한 손의 손가락들이 서로 떨어져 부채꼴로 펼쳐진다", "The attached fingers spread apart in a visible fan."],
 "pv_hands_behind_back": ["자기 두 손을 몸통 뒤쪽에 모아 둔다", "Both of the actor's hands are gathered behind their own torso."],
 "pv_wink": ["같은 얼굴에서 한쪽 눈만 닫히고 반대쪽 눈은 열린다", "One eye shuts while the opposite eye on the same face stays open."],
 "pv_smile_closed": ["치아가 보이지 않는 닫힌 입술 선 위로 양 입꼬리가 올라간다", "Upturned mouth corners accompany a closed lip seam with the teeth concealed."],
 "pv_smile_teeth": ["올라간 입꼬리 사이로 치아가 드러나는 미소", "The mouth corners lift around a smile with visible teeth."],
 "pv_eyes_closed": ["두 눈의 눈꺼풀이 각각 닫혀 눈 틈이 사라진다", "Both eye apertures close on the same face."],
 "pv_half_lidded": ["눈을 완전히 감지 않은 채 윗눈꺼풀이 홍채 일부를 덮는다", "Partly lowered upper lids cover some iris while the eyes remain open."],
 "pv_asymmetric_mouth": ["한쪽 입꼬리가 다른 쪽보다 더 높이 올라간다", "One mouth corner rises farther than the other on the same face."],
 "pv_parted_lips": ["윗입술과 아랫입술 사이에 작은 틈이 남는다", "A narrow opening separates the upper and lower lip margins."],
 "pv_puffed_cheeks": ["표정으로 양 볼이 바깥쪽으로 부풀어 둥글어진다", "Both cheeks bulge outward in the selected facial expression."],
 "pv_raised_brows": ["같은 얼굴의 두 눈썹이 평소 위치보다 위로 올라간다", "Both eyebrows sit visibly higher over their respective eyes."],
 "pv_gaze_up": ["머리 방향과 별개로 동공이 위쪽의 지정한 대상을 향한다", "The pupils direct their gaze upward toward the declared target."],
 "pv_gaze_down": ["눈의 시선이 아래에 있는 대상을 향한다", "The eyes look downward toward the identified lower target."],
 "pv_gaze_offcamera": ["두 눈이 렌즈 밖의 같은 지정 대상을 바라본다", "Both eyes address the same declared target away from the lens."],
 "pv_side_eye": ["얼굴 방향에서 옆으로 벗어난 대상을 눈으로 바라본다", "The eyes turn sideways relative to the head's direction."],
 "pv_head_tilt": ["목에 연결된 머리 축이 좌우 한쪽으로 기울어진다", "The head inclines laterally over its connected neck."],
 "pv_head_turn": ["몸통의 방향을 유지한 채 머리만 옆으로 돌아간다", "The head rotates relative to the torso while its neck connection remains continuous."],
 "pv_chin_down": ["턱이 아래로 내려가며 머리의 앞뒤 기울기가 보인다", "The chin lowers in a visible downward head pitch."],
 "pv_forward_torso_lean": ["골반과 이어진 몸통이 앞쪽으로 기울어진다", "The torso inclines forward from its connection above the pelvis."],
 "pv_shoulder_raise": ["어깨 양끝이 위로 올라가 목 옆 간격이 짧아진다", "The shoulder line rises toward the neck in the declared shrug configuration."],
 "pv_shoulder_forward": ["어깨띠가 몸통 앞쪽으로 모여 앞으로 말린다", "The shoulders draw forward around the upper torso."],
 "pv_foreshortened_reach": ["손과 팔이 촬영 렌즈 쪽 깊이 방향으로 뻗는다", "The arm extends toward the capture lens with depth foreshortening."],
 "pv_narrow_stance": ["두 발이 바닥에 가까운 폭으로 나란히 놓인다", "Both grounded feet form a narrow lateral support base."],
 "pv_single_support": ["한쪽 다리가 주로 몸을 받치고 반대 다리는 다른 접지 역할을 가진다", "One planted leg supports the body while the other has a distinct relaxed contact role."],
 "pv_knee_hug": ["세운 무릎 둘레를 자기 팔로 감싼 앉은 자세", "The seated actor wraps their own arms around their raised knees."],
 "pv_cross_leg_floor": ["바닥에 골반을 지지한 채 두 정강이가 앞에서 교차한다", "The pelvis rests on the floor while the two shins cross in front."],
 "pv_side_sit_floor": ["골반이 바닥에 닿고 굽힌 두 다리가 한쪽으로 모인다", "Both bent legs fold to one side of the floor-supported pelvis."],
 "pv_squat_grounded": ["양발의 접지를 유지하며 골반을 낮춘 깊은 무릎 굴곡", "The pelvis lowers through bent knees over two grounded feet."],
 "pv_prone_forearms": ["몸 앞면을 바닥에 두고 두 전완의 접점으로 상체를 받친다", "Both forearms contact the supporting surface beneath a prone upper torso."],
 "pv_curled_side": ["몸 옆면을 지지면에 둔 채 무릎과 몸통을 가까이 접는다", "The side-supported body folds the knees closer to the torso."],
 "pv_demi_pointe": ["뒤꿈치를 든 채 앞발 볼로 바닥을 지지한다", "Raised heels leave the forefoot balls visibly supporting the stance."],
 "pv_chin_support": ["턱 아래가 자기 손에 닿고 팔의 지지 경로가 이어진다", "The chin rests against the actor's own hand along a connected supporting arm."],
 "pv_head_shoulder_pair": ["한 인물의 머리가 다른 인물의 어깨에 직접 닿아 기댄다", "One actor's head rests in direct contact with the other actor's shoulder."],
 "pv_mug_grip": ["컵을 쥔 손가락이 컵 몸체나 손잡이에 실제로 닿는다", "The grasping fingers visibly contact the declared cup or its handle."],
 "ae_lip_press": ["윗입술과 아랫입술이 닫힌 경계를 따라 눌려 맞닿는다", "The upper and lower lip margins press together along a sealed seam."],
 "ae_lip_tighten": ["입술 가장자리가 가로로 팽팽해지고 입 선이 비교적 곧아진다", "Taut thinned lip margins accompany a relatively straight mouth line."],
 "ae_purse": ["입술 둘레를 안쪽으로 모아 입 폭을 좁힌다", "The lips draw inward around a narrowed mouth aperture."],
 "ae_pucker": ["오므린 입술이 얼굴 앞쪽으로 돌출된다", "The gathered lips project forward from the face in the chosen pucker."],
 "ae_lip_roll": ["입 선이 닫힌 채 입술 가장자리를 안으로 말아 붉은 입술 면을 줄인다", "The lip margins roll inward while the mouth seam stays closed, reducing the exposed lip surface."],
 "ae_inner_brow": ["양 눈썹의 안쪽 끝이 바깥쪽보다 위로 들린다", "The inner ends of both eyebrows lift relative to the outer ends."],
 "ae_nose_wrinkle": ["콧등 피부가 모여 짧은 주름과 당김을 만든다", "The skin over the nose bridge bunches into short visible creases."],
 "ae_tears": ["아래 눈꺼풀 경계를 따라 눈물이 고인 액체 띠가 보인다", "A visible pool of tear fluid lies along the lower lid margins."],
 "ae_smile_tears": ["눈에 눈물이 고인 상태와 작은 올라간 입꼬리가 같은 얼굴에 공존한다", "Tear-filled eyes and a small upturned smile coexist on the same face."],
 "ae_hand_mouth": ["자기 손이 자기 입 앞을 가리되 손목과 손가락 연결이 보인다", "The actor's own connected hand covers the front of their mouth."],
 "ae_duchenne_shape": ["올라간 볼과 좁아진 눈 틈이 올라간 입꼬리와 함께 나타난다", "Raised cheeks and narrowed eye apertures accompany upturned mouth corners."],
 "ae_smize": ["입꼬리와 볼이 올라가고 두 눈은 완전히 감기지 않은 채 좁아진다", "Raised mouth corners and lifted cheeks accompany narrowed eye openings that remain partly open."],
 "ae_coy_variant": ["이미 정한 새침한 교류에서 머리를 살짝 돌려도 상대를 향한 눈길은 남는다", "Within the established reserved encounter, a slight head turn retains the gaze toward the same addressee."],
 "ae_coquettish_variant": ["이미 정한 성인 플러팅 장면에서 작은 미소를 유지하며 상대를 향해 윙크한다", "Within the established adult flirting encounter, the actor winks toward its addressee while retaining a small smile."],
 "sca_f03": ["같은 눈의 윗눈꺼풀이 내려와 열린 홍채 위쪽과 겹친다", "Lowered upper eyelid edges overlap the upper portions of the still-visible irises."],
 "sca_g04": ["자기 소매 끝이 손목을 지나 손 위까지 연속해서 덮인다", "The wearer's sleeve continues past the wrist over the stated part of the hand."],
 "sca_x01": ["동물 귀 모양 장식의 밑부분이 모발 위 별도 머리띠에 붙는다", "The ear-shaped ornaments attach at their bases to a separate band resting over the hair."],
 "pe_shallow_falloff": ["주 초점면은 선명하고 그 앞뒤 깊이의 물체는 점차 흐려진다", "The selected focal plane stays sharp as surfaces farther from that depth grow softer."],
 "pe_background_bokeh": ["초점 밖 배경 광원들이 부드러운 원반처럼 흐려진다", "Defocused background light points spread into soft optical discs."],
 "lit_window_diffused_daylight_field": ["넓게 확산된 창 주광이 완만한 명암 경계를 만든다", "A broad diffused daylight field produces gradual shadow transitions."],
 "third_grid_off_center_subject": ["주 피사체를 삼분할 교차점 가까이에 두어 화면 중심에서 비켜 놓는다", "The main subject sits off center near a rule-of-thirds intersection."],
 "subject_field_negative_space_relation": ["주 피사체 곁의 넓고 단순한 배경 여백이 분리되어 보인다", "A large contiguous low-detail field remains visibly separate beside the main subject."],
 "mg_rounded_corners": ["표시된 사각 도안의 모서리가 곡선으로 이어진다", "Curved corner transitions join the edges of the displayed rectangular graphic."],
 "mg_round_cap": ["도안 선의 끝이 반원형으로 마감된다", "The displayed stroke ends in a rounded cap."],
 "plush_doll": ["작은 봉제 인형 소품", "A small stuffed fabric toy used as the declared prop."],
 "y2kr_faux_fur": ["보이는 옷 가장자리 위로 긴 섬유가 복슬복슬 솟는다", "Long projecting fibers form a fluffy nap above a visible garment edge."],
}

# (ID, slot, KO label, exact narrow labels, component groups, contrasts, properties, sources)
NEW = [
 ("cv_single_cheek_puff", "expression", "지정한 한쪽 볼만 부풀린 표정", ["한쪽 볼 부풀리기", "single-cheek puff"],
  ["the specified cheek bulges outward", "the opposite cheek retains its unpuffed contour", "both cheek states belong to the same face"], ["both cheeks puffed", "permanent facial asymmetry"], [("expression","main_subject","face.expression.cheek_inflation")], ["S03","S23"]),
 ("cv_small_o_mouth", "expression", "작은 둥근 O형 입 틈", ["작은 O자 입", "small O-shaped mouth"],
  ["the lips surround a small rounded opening", "the opening has a continuous curved lip boundary", "the jaw stays close enough to retain a small mouth aperture"], ["a thin horizontal lip gap", "a widely dropped jaw"], [("expression","main_subject","face.expression.mouth_aperture")], ["S03","S23"]),
 ("cv_wide_eye_apertures", "expression", "크게 열린 두 눈의 개안부", ["동그랗게 뜬 눈", "wide-open eye apertures"],
  ["both upper lids lift to expose larger eye apertures", "the visible irises remain seated within their own eye contours"], ["permanently enlarged eyeballs", "a pupil size change alone"], [("expression","main_subject","face.expression.eyelid_openness")], ["S03","S23"]),
 ("cv_thumb_index_cross", "hand_pose", "한 손의 엄지와 검지가 교차한 작은 손 모양", ["엄지검지 교차 손동작", "crossed thumb-index hand gesture"],
  ["the thumb and index finger of one hand overlap in a small cross", "the remaining fingers curl toward that same palm", "the crossing belongs to one continuously connected hand"], ["a heart formed by two hands", "interlaced fingers from two hands"], [("pose","main_subject","body.hand_configuration")], ["S09","S29"]),
 ("cv_hand_heart_tips", "hand_pose", "검지 끝과 엄지 끝을 각각 맞댄 양손 하트", ["검지·엄지 접점형 양손 하트", "index-and-thumb fingertip hand heart"],
  ["the two index fingertips meet at the upper inward notch", "the two thumb tips meet at the lower point", "the opposed curved hands enclose one heart-shaped opening"], ["an overhead arm heart", "two unconnected half hearts"], [("pose","main_subject","body.hand_configuration"),("pose","main_subject","body.arm_configuration")], ["S10","S29"]),
 ("cv_cheek_poke", "contact_point", "자기 검지 끝과 자기 볼의 접점", ["자기 볼 콕", "own-cheek fingertip poke"],
  ["one index fingertip directly touches the actor's own cheek", "the fingertip continues into that actor's hand and wrist", "the cheek surface and fingertip share one visible contact point"], ["a fingertip hovering beside the face", "another actor's hand touching the cheek"], [("pose","main_subject","body.contact_configuration")], ["S29","S23"]),
 ("cv_cheek_palm", "contact_point", "자기 볼 옆에 닿은 자기 손바닥", ["자기 볼 손바닥 접촉", "own-cheek palm contact"],
  ["the actor's own palm rests against the side of their cheek", "the palm belongs to the same actor through a visible wrist connection"], ["chin support", "a hand held away from the cheek"], [("pose","main_subject","body.contact_configuration")], ["S24","S29"]),
 ("cv_two_cheek_press", "contact_point", "자기 양손으로 양볼을 안쪽으로 누른 접촉", ["양손으로 자기 양볼 누르기", "bilateral own-cheek compression"],
  ["each palm contacts its corresponding cheek on the same actor", "both cheek contours indent inward at the palm contacts", "each hand connects to its own wrist and arm"], ["both palms hovering", "air-inflated cheeks without palm contact"], [("pose","main_subject","body.contact_configuration"),("expression","main_subject","face.expression.cheek_compression")], ["S29","S23"]),
 ("cv_index_tip_meet", "hand_pose", "자기 양손 검지 끝만 맞댄 손동작", ["자기 양손 검지 끝 맞대기", "own index fingertips touching"],
  ["one extended index finger from each of the actor's two hands points inward", "the two index fingertips touch each other", "the remaining fingers stay folded into their respective palms"], ["interlaced hands", "tips separated by a gap"], [("pose","main_subject","body.hand_configuration")], ["S29"]),
 ("cv_eye_between_fingers", "hand_pose", "자기 손가락 틈으로 보이는 자기 눈", ["자기 손가락 틈으로 눈 보기", "eye peeking through own fingers"],
  ["the actor's own hand lies in front of their face", "a gap between connected fingers exposes one stated eye", "the visible eye remains behind that finger gap"], ["a hand beside the face", "an eye painted onto a palm"], [("pose","main_subject","body.hand_configuration"),("relationship","main_subject","hand_face.occlusion")], ["S29","S12"]),
 ("cv_single_heel_lift", "body_pose", "한쪽 뒤꿈치만 들고 반대 발로 지지한 서기", ["한쪽 뒤꿈치 들기", "one-heel-raised stance"],
  ["one heel is lifted above the support surface while its forefoot stays in contact", "the opposite foot remains planted as the support foot", "the legs and pelvis stay continuously connected above that base"], ["both heels raised", "both feet airborne"], [("pose","main_subject","body.support_and_configuration")], ["S30"]),
 ("cv_two_hand_cup", "contact_point", "두 손이 같은 컵 몸체를 감싼 접촉", ["컵 몸체를 두 손으로 감싸기", "two-hand cup cradle"],
  ["both of the actor's hands curve around the same cup body", "fingers from each hand visibly contact that cup surface", "both wrists connect the cradling hands to the same actor"], ["one hand on a handle alone", "hands hovering near different cups"], [("pose","main_subject","body.contact_configuration"),("relationship","main_subject","hand_object.contact")], ["S29"]),
 ("cv_plush_hug", "relational_action", "같은 봉제인형을 두 팔로 몸 앞에 감싼 관계", ["봉제인형을 두 팔로 안기", "two-arm plush embrace"],
  ["both arms curve around the same declared plush toy", "the toy contacts the actor's front torso inside that arm enclosure", "the toy boundary remains distinguishable from the hands and garment"], ["a toy floating behind the actor", "two different toys under separate arms"], [("pose","main_subject","body.arm_configuration"),("relationship","main_subject","body_object.contact")], ["S29"]),
 ("cv_partner_sleeve_pinch", "contact_point", "상대의 소매 끝을 자기 손가락으로 집은 접촉", ["상대 소매 끝 집기", "partner sleeve-edge pinch"],
  ["the actor's fingertips pinch the other declared actor's sleeve edge", "that sleeve remains continuously attached to the other actor's garment", "the pinching hand stays attached to the initiating actor"], ["pinching one's own hem", "floating cloth unrelated to the partner"], [("pose","main_subject","body.contact_configuration"),("relationship","main_subject","partner_sleeve.contact")], ["S29"]),
 ("cv_general_catchlight", "eye_detail", "눈 표면의 일반 광원 반사", ["눈 표면의 캐치라이트", "corneal catchlight reflection"],
  ["a compact reflected light patch lies within the visible eye surface", "the reflection follows the surface of the same eye rather than becoming a separate floating symbol"], ["a drawn star floating beside an eye", "a prescribed pair of vertically aligned lights"], [("lighting","main_subject","eye_surface.reflected_light")], ["S25"]),
]

# Complete observational equivalents reuse the original candidate, including every guard/effect.
PROFILE_REUSE = {
 "pv_flower_chin": ("cv_profile_flower_chin", ["턱 아래 두 손 꽃받침", "bilateral hands-under-chin flower pose"]),
 "pv_arm_heart": ("cv_profile_arm_heart", ["머리 위 팔 하트", "overhead arm-heart pose"]),
 "pv_cat_paw": ("cv_profile_cat_paw", ["고양이 앞발 손동작", "curled cat-paw hand gesture"]),
 "pv_wink": ("cv_profile_wink", ["한쪽 눈만 감는 윙크", "one-eye wink"]),
 "pv_smile_closed": ("cv_profile_closed_smile", ["입 다문 미소", "closed-mouth smile"]),
 "pv_smile_teeth": ("cv_profile_toothy_smile", ["치아가 드러난 미소", "tooth-bearing smile"]),
 "pv_puffed_cheeks": ("cv_profile_puffed_cheeks", ["양볼 부풀리기", "bilaterally puffed cheeks"]),
 "pv_head_tilt": ("cv_profile_head_tilt", ["머리의 좌우 갸웃", "lateral head tilt"]),
 "ae_pucker": ("cv_profile_pucker", ["앞으로 내민 오므린 입술", "protruding lip pucker"]),
 "ae_lip_roll": ("cv_profile_lip_roll", ["입술 안으로 말아 넣기", "inward lip roll"]),
 "ae_smile_tears": ("cv_profile_smile_tears", ["눈물 고임과 작은 미소", "tear-filled eyes with a small smile"]),
}

def profile(pid, labels, units, contrasts, effects, paraphrases):
    components=[]
    for i,u in enumerate(units,1):
        components.append(dict(id=f"component_{i}", match_terms=[u], evidence_field=f"component_{i}_phrase", evidence_terms=[u], min_content_words=3,
            instruction=f"Bind the complete visible relation to the declared owner: {u}.",
            render_gate=dict(id=f"vo_{pid}_{i}", review_scale="native", description=f"Inspect original pixels for {u}. Every component is required; partial evidence fails and occlusion is unobservable.")))
    return dict(id=pid, category="observable_local_configuration", activation=dict(exact_terms=labels, requires_adult_character=False,
        semantic_discovery_requires_component_evidence=True,
        hard_activation=dict(contract_version="photo-visual-hard-activation/v1", required_any_groups=[dict(id="human_owner_context",any_terms=["human","person","woman","man","actor","portrait","face","hand","인물","사람","얼굴","손","배우"]) ])),
        semantics=dict(definition="; ".join(units), paraphrase_examples=[x for x in paraphrases if x.casefold() not in {y.casefold() for y in labels}], visual_components=units,
            contrast_examples=contrasts, claim_limits=["Bind every stated body part, contact and prop to its declared owner.","This visible configuration establishes no age, personality, emotion, desire, health, wardrobe or actor count.","A locked crop is preserved; an invisible prerequisite cannot be reported as satisfied.","Every required component must pass; partial evidence fails and occlusion is unobservable."]),
        concept_candidate=dict(concept_terms=list(dict.fromkeys([*labels,*paraphrases,*units])), core_assertion_discovery=True,
            affected_dimensions=list(dict.fromkeys(x['dimension'] for x in effects)), affected_properties=effects),
        runtime_expression=dict(default_mode="definition_with_optional_label",prompt_label_terms=[],forbidden_prompt_terms=[],runtime_forbidden_labels=[]),
        reject_substitutes=contrasts, authored_components=dict(contract_version="photo-authored-visual-components/v1",components=components))

def bundle(pid, entry_id, slot, p):
    return dict(id=pid.replace("profile","bundle"),candidate_only=True,primary_visual_proposition=p['semantics']['definition'],candidate_ids=[entry_id],candidate_slots={entry_id:slot},hard_profile_ids=[pid],
        component_groups=[dict(id=f"component_{i}",visible_evidence=[u]) for i,u in enumerate(p['semantics']['visual_components'],1)],
        source_keywords=p['activation']['exact_terms'],confusion_boundaries=p['reject_substitutes'],
        relations=[dict(id="owner_scope",type="declared_owner_scope",subject="main_subject",object="the declared actor and stated local configuration")])

def main():
    if (HERE/'BASELINE.json').exists(): raise RuntimeError("Integration already initialized; do not overwrite baseline")
    data=g.load_json(ASSETS/'photo_prompt_tags.json')
    entries={e['id']:(slot,e) for slot,rows in data['slots'].items() for e in rows}
    existing_files=['photo_prompt_visual_obligations_pose_vocabulary.json','photo_prompt_visual_obligations_acting_expression.json','photo_prompt_visual_obligations_portrait_composition.json']
    files=[ASSETS/'photo_prompt_tags.json',SCRIPTS/'prompt_generator.py',ASSETS/'photo_prompt_semantic_index.json',ASSETS/'photo_prompt_visual_profile_index.json',*[ASSETS/n for n in existing_files]]
    status=subprocess.check_output(['git','status','--porcelain=v1','-uall'],cwd=ROOT,text=True)
    baseline=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),status=status,files=[])
    for p in files:
        dest=HERE/'baseline'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        baseline['files'].append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p)))
    # Capture all authored DATA as evidence for independent semantic-preservation checks.
    baseline['authored_files']={str(p.relative_to(ROOT)):sha(p) for p in ASSETS.glob('*.json') if 'index' not in p.name}
    write(HERE/'BASELINE.json',baseline)
    ext=dict(schema_version=g.RESEARCH_EXTENSION_SCHEMA,slots={},existing_slot_context_extensions={},visual_semantics=[])
    vis=dict(schema_version=g.VISUAL_OBLIGATION_EXTENSION_SCHEMA_VERSION,relation_contract_version="photo-visual-relation/v1",profiles=[])
    for eid,phrases in REUSE.items():
        slot,e=entries[eid]
        ext['existing_slot_context_extensions'].setdefault(slot,{})[eid]=dict(paraphrases=phrases,contexts=[dict(id=f"cute_equivalent_{eid}",application_conditions=["Equivalent meaning only; retain the original owner, prerequisites, all effects and guards."],limits=["No emotion, age, universal cuteness or extra actor inferred from this local form."])])
    for eid,slot,ko,labels,units,contrasts,props,sources in NEW:
        effects=[dict(dimension=d,target=t,property=p) for d,t,p in props]
        # New narrow labels name only the local form; broad cultural labels stay in maintenance.
        paraphrases=[ko, "; ".join(units)]
        e=dict(id=eid,ko=ko,en="; ".join(units),weight=0.5,tags=["human","observable_relation"],for_any=["human"],aliases=labels,keywords=labels,paraphrases=paraphrases,
            embedding_text="; ".join([ko,*labels,*units]),concept_units=units,
            relations=[dict(id="owner_scope",type="declared_owner_scope",subject="main_subject",object="the declared actor and the stated body parts or contact target")],
            affected_dimensions=list(dict.fromkeys(d for d,_,_ in props)),affected_properties=effects,core_assertion_discovery=True)
        if eid=='cv_partner_sleeve_pinch': e['requires_primary_any_tags']=['partner','pair','two people','상대','두 사람']
        if eid=='cv_plush_hug': e['requires_primary_any_tags']=['plush','stuffed toy','봉제인형','인형']
        if eid=='cv_two_hand_cup': e['requires_primary_any_tags']=['cup','mug','컵','머그']
        ext['slots'].setdefault(slot,[]).append(e)
        p=profile(eid.replace('cv_','cv_profile_',1),labels,units,contrasts,effects,paraphrases)
        vis['profiles'].append(p);ext['visual_semantics'].append(bundle(p['id'],eid,slot,p))
    for eid,(pid,labels) in PROFILE_REUSE.items():
        slot,e=entries[eid]
        units=e['concept_units'][:]
        # Non-observable ownership bookkeeping is a claim limit, not an extra pixel component.
        if eid=='pv_wink': units=units[:2]
        if eid in {'pv_cat_paw','pv_head_tilt'}: units=units[:2]
        if eid=='pv_puffed_cheeks': units=["both cheeks visibly bulge outward in the selected expression"]
        if eid=='pv_smile_closed': units=units[:2]
        if eid=='pv_smile_teeth': units=units[:2]
        p=profile(pid,labels,units,["a different owner, opening, support or contact than the stated configuration"],e['affected_properties'],REUSE[eid])
        vis['profiles'].append(p);ext['visual_semantics'].append(bundle(pid,eid,slot,p))
    # Bilingual full-equivalent examples strengthen existing profile semantics; activation/gates stay byte-equivalent.
    augmented=[]
    for filename in existing_files:
        d=read(ASSETS/filename);changed=False
        for p in d['profiles']:
            eid=p['id'].replace('pv_profile_','pv_').replace('ae_profile_','ae_')
            if eid in REUSE:
                exact={x.casefold() for x in p['activation']['exact_terms']}
                additions=[s for s in REUSE[eid] if s.casefold() not in exact]
                p['semantics']['paraphrase_examples']=list(dict.fromkeys([*p['semantics'].get('paraphrase_examples',[]),*additions]))
                p['concept_candidate']['concept_terms']=list(dict.fromkeys([*p['concept_candidate']['concept_terms'],*additions]))
                augmented.append(dict(file=filename,id=p['id'],added=additions));changed=True
        if changed:write(ASSETS/filename,d)
    record=dict(contract_version="photo-extension-maintenance-record/v1",record_id=RECORD,maintenance_only=True,based_on_commit=baseline['head'],
        research_reference="docs/research-evidence/photo-prompt/cute-semantics-20261005/REPORT.md",source_records=read(HERE.parent/'cute-semantics-20261005/SOURCES.json'),
        reviewed_equivalents=REUSE,new_form_decisions=[dict(id=x[0],source_ids=x[-1],confusion_boundaries=x[-3]) for x in NEW],
        enriched_profiles=augmented,
        deferred=[dict(term=t,reason=r) for t,r in [
            ('pv_finger_heart','Historical deferred candidate remains absent. cv_thumb_index_cross is an explicit local geometry; the Unicode source also records money meanings. Neither broad finger-heart nor money labels activate it.'),
            ('tehepero','Creator source unavailable; no fixed tongue-wink culture alias.'),
            ('gyaru peace','Named first-party shoot found, but hand orientation pixels not reviewed; retain generic V alternatives.'),
            ('broad cuteness and viewer reactions','No fixed age, face geometry, species, wardrobe or pose obligation.'),
            ('temporal actions','A still does not establish waving, swallowing, skipping or a past hidden event.'),
            ('dark-cute contrasts','Preserve both semantic axes in independent core; no blanket sanitization or automatic real injury.')]],
        boundaries=["Contexts cannot broaden existing labels/effects/guards.","New form aliases require a human owner context; cultural labels are not imported as hard meanings.","Selected bundles are optional and do not autoactivate linked profiles.","Native pixels and user preference remain separate from authored-data/index checks."])
    write(HERE.parent/'extension-maintenance'/f'{RECORD}.json',record)
    ext['maintenance_ref']=dict(contract_version="photo-extension-maintenance-ref/v1",record_id=RECORD,sha256=digest(record))
    write(ASSETS/EXT,ext);write(ASSETS/VIS,vis)
    tags=read(ASSETS/'photo_prompt_tags.json');tags['candidate_semantic_policy']['required_extensions'].append(EXT);write(ASSETS/'photo_prompt_tags.json',tags)
    source=(SCRIPTS/'prompt_generator.py').read_text()
    source=source.replace('    "photo_prompt_visual_obligations_seduction_expression.json",\n)',f'    "photo_prompt_visual_obligations_seduction_expression.json",\n    "{VIS}",\n)',1)
    source=source.replace('    "photo_prompt_seduction_expression_extension.json",\n)',f'    "photo_prompt_seduction_expression_extension.json",\n    "{EXT}",\n)',1)
    (SCRIPTS/'prompt_generator.py').write_text(source)
    write(HERE/'AUTHORED-RECEIPT.json',dict(reused_candidate_targets=len(REUSE),added_candidate_paraphrases=sum(map(len,REUSE.values())),new_candidates=len(NEW),new_profiles=len(vis['profiles']),new_bundles=len(ext['visual_semantics']),existing_profiles_enriched=augmented,
        runtime_files=[EXT,VIS,*[n for n in existing_files if any(r['file']==n for r in augmented)],'photo_prompt_tags.json'],status="authored; indexes and tests pending"))
    print(json.dumps(dict(reused=len(REUSE),new=len(NEW),profiles=len(vis['profiles']),enriched_profiles=len(augmented))))

if __name__=='__main__':main()
