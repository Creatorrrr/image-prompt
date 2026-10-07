#!/usr/bin/env python3
"""Maintenance-only reviewed paraphrases; never an initial authoring input."""
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg

def read(p): return json.loads(p.read_text())
def write(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
def unique(xs): return list(dict.fromkeys(xs))

# Each pair is a reviewed, same-owner description, not an exact activation alias.
EXISTING = {
 'y2kr_rib_tank': [
  '민소매 탑 원단에 가늘고 솟은 세로 니트 골이 반복된다',
  '소매 없는 탱크톱 표면의 세로 리브가 잔잔한 높낮이를 이룬다',
  'a sleeveless top shows fine vertical knitted ridges repeating over its fabric',
  'fine raised lengthwise knit ribs repeat across the sleeveless tank surface'],
 'sw_rib': [
  '수영복의 같은 원단 패널에 평행한 솟은 골과 낮은 홈이 작은 그림자로 구분된다',
  '수영복 패널의 반복 리브가 음영을 사이에 두고 원단 위로 돌출된다',
  'parallel rib relief and recessed channels are separated by small shadows on one swimsuit panel',
  'the swimsuit fabric shows raised parallel ridges with shaded grooves between them'],
 'vg_faille_crossgrain_ribs_profile': [
  '기존 천의 가는 가로 직조 골이 천의 굽음과 이어지고 작은 방향성 광택으로 드러난다',
  '직물 표면의 낮고 촘촘한 횡방향 리브가 같은 천의 주름을 따라 연속된다',
  'fine low crosswise woven ribs follow the existing cloth curvature under small directional highlights',
  'the existing textile carries closely spaced flat cross-grain ridges bending with its surface'],
 'pfe_slit': [
  '치마 옆 패널의 마감된 두 가장자리 사이로 같은 다리가 이어지고 나머지 치마의 밑단과 늘어진 주름은 남는다',
  '한 장의 치마 옆트임에 연속된 한쪽 다리가 보이며 열린 경계와 남은 치마 밑단이 따로 읽힌다',
  'one continuous leg appears between two finished side-slit edges while the remaining skirt retains its hem and hanging folds',
  'a bounded side opening separates two finished skirt edges around the same leg, leaving the other skirt panel draped to its own hem'],
 'pfe_opaque_fit': [
  '불투명한 옷이 성인 몸통과 허리 및 엉덩이 윤곽을 따르며 솔기와 밑단 및 국소 주름으로 피부와 구별된다',
  '성인의 몸 윤곽을 따르는 밀착 의복은 속 피부 디테일을 통과시키지 않고 천의 가장자리와 주름을 유지한다',
  'opaque fabric follows the adult torso, waist and hips, with hems, seams and small folds keeping clothing separate from skin',
  'the adult silhouette is followed by close-fitting nontransparent cloth whose edges and folds remain distinct from the body'],
 'pfe_skimming': [
  '성인 몸통과 엉덩이를 따르는 옷이 접촉 부위 사이에서 여유 있게 늘어지고 밑단과 옆선은 별도 천 층으로 남는다',
  '옷은 성인의 몸 윤곽을 스치되 모든 면을 압착하지 않고 접촉점 사이의 늘어진 주름과 가장자리를 유지한다',
  'the garment skims the adult torso and hips with hanging ease between contact areas and separately readable hems and side edges',
  'soft cloth follows the adult contour while bridging contact points in relaxed folds, retaining its own hem and side boundaries'],
 'pfe_one_shoulder': [
  '성인의 한 어깨에만 연결된 의복 지지가 있고 반대 어깨는 연속된 비대칭 목선 밖에 남는다',
  '성인 의상의 한쪽 어깨 지지와 사선 목선이 이어지며 다른 어깨는 그 목선 외부에 드러난다',
  'one continuous diagonal neckline leaves the adult opposite shoulder outside the garment while the single supporting shoulder stays attached',
  'the adult garment has one shoulder support and a traceable asymmetrical neckline bordering the opposite uncovered shoulder'],
 'satin_directional_luster_drape_surface': [
  '같은 새틴 계열 의복의 넓고 매끈한 광택이 주름 방향과 굽음을 따르고 어두운 면의 원단과 솔기가 이어진다',
  '의복 가장자리로 연결된 새틴 표면에 주름을 따라 부드러운 빛 띠가 흐르고 그늘에서도 같은 천이 읽힌다',
  'broad smooth luster follows curved satin garment folds while darker cloth planes, seams and edges remain connected',
  'a coherent satin-like garment keeps shadow detail and traceable seams as wide highlights follow its draped fold direction'],
 'lace_trim_attached_edge': [
  '다른 바탕 원단의 가장자리에 좁은 레이스 띠가 봉제되고 열린 실무늬 셀과 물결 모양 자유 가장자리가 구분된다',
  '의복 끝에 붙인 레이스는 반복되는 실제 빈 셀과 봉제 부착선 및 스캘럽 테두리를 유지한다',
  'a narrow openwork lace strip is stitched to a different base fabric, with repeating empty cells and a scalloped free edge',
  'the garment edge carries an attached lace band whose stitch join, open thread motifs and scalloped border remain distinct'],
 'decolletage_neckline_exposure': [
  '성인 의복의 낮은 목선이 목 아래와 쇄골 및 어깨와 상흉부의 보이는 영역을 정의한다',
  '낮게 열린 성인 의상의 목선 안에 쇄골과 윗가슴이 보이며 가슴 사이 골은 별도 조건이다',
  'the adult garment neckline bounds a visible lower-neck, clavicle, shoulder and upper-chest region',
  'a low adult fashion neckline reveals the upper chest and clavicles without making a cleavage line necessary'],
 'wet_damp_clumped_hair_state': [
  '젖거나 축축한 머리가 마른 상태보다 부피가 줄고 가닥 묶음과 무게 방향 또는 국소 부착 및 수분 단서를 함께 보인다',
  '머리의 수분 흔적과 모여 붙은 가닥 및 눌린 부피가 중력 방향이나 접촉 지점과 일관된다',
  'damp hair has reduced dry volume, moisture cues and bundled strands with coherent weight or local adherence',
  'wet-looking hair is supported by compact strand clumps, lowered volume and consistent moisture and weight cues'],
 'hvr_profile_wet_hair_skin_contact': [
  '젖은 머리 가닥이 가는 다발로 모이고 일부가 같은 사람의 볼과 목에 실제로 붙어 있다',
  '볼과 목의 피부에 닿는 젖은 머리 다발의 접촉 경계가 보인다',
  'narrow wet strand bundles visibly adhere to the same cheek and neck',
  'clustered damp hair ropes touch the cheek and neck at readable skin-contact patches'],
 'y2kr_bra_straps': [
  '어깨의 가는 안쪽 지지 끈이 바깥 의복의 끈과 별개로 이어진다',
  '같은 어깨 위 안쪽 의복 끈과 바깥 의복 끈의 두 경계가 따로 읽힌다',
  'a narrow inner support strap stays separately traceable beside the outer shoulder strap',
  'the inner garment strap and outer clothing strap remain two distinct shoulder supports'],
 'y2kr_bustier': [
  '컵의 형태를 정하는 봉제선과 몸통을 지지하는 밀착 패널이 서로 구분된다',
  '몸통 패널 위 컵 솔기가 독립된 의복 구조로 남는다',
  'cup-defining seams stay distinct from the fitted supporting torso panels',
  'the shaped cup stitching and supporting body panels remain separately readable garment structures'],
 'pv_profile_supine': [
  '같은 사람의 등쪽 몸통이 지지면에 닿고 앞쪽 몸통은 그 면 반대쪽을 향하며 팔다리는 누운 몸과 연결된다',
  '지지면 위로 등은 내려앉고 앞몸통은 바깥을 향하며 사지는 같은 누운 인물의 관절로 이어진다',
  'the reclining actor rests the back of the torso on the support with the front facing away and connected limbs',
  'back-to-support contact identifies the supine actor while the anterior torso faces outward and every limb remains attached'],
 'pv_profile_side_lying': [
  '몸통 또는 엉덩이의 옆면이 지지면에 닿고 어깨와 골반도 옆으로 놓이며 팔로 버티기는 따로 정한다',
  '옆으로 누운 몸의 어깨와 엉덩이가 같은 측면 방향을 보이고 옆 몸통이 받침에 닿는다',
  'lateral torso or hip contact and side-oriented shoulders and hips identify side lying, with arm support separately specified',
  'the actor lies on a torso or hip side with shoulders and pelvis turned sideways to the support'],
 'pv_profile_tall_kneel': [
  '두 무릎은 받침에 닿고 골반은 발뒤꿈치보다 높으며 허벅지는 몸통 쪽으로 일어난다',
  '양 무릎으로 지지하며 엉덩이를 뒤꿈치 위로 들어 올려 허벅지를 세운 무릎 자세',
  'both knees rest on the support while raised thighs place the pelvis clearly above the heels',
  'the actor kneels upright on both grounded knees with thighs rising to a pelvis lifted above the heels'],
 'pv_profile_half_kneel': [
  '한쪽 무릎은 바닥에 닿고 다른 다리의 발은 앞으로 디뎌 두 지지점이 서로 다른 다리에 속한다',
  '바닥의 한 무릎과 앞쪽에 세운 반대 발이 반무릎 자세를 지지한다',
  'one grounded knee and the opposite planted forward foot belong to different legs',
  'a half-kneeling actor supports on one floor-contact knee and the other foot planted ahead'],
 'pv_profile_heel_sit': [
  '무릎과 정강이는 받침에 놓이고 골반은 뒤꿈치 쪽으로 낮아지며 허벅지가 정강이 위에 접힌다',
  '뒤꿈치에 엉덩이를 낮춘 무릎 앉기에서 무릎과 정강이가 바닥에 닿고 하체 연결이 보인다',
  'knees and shins contact the support as the pelvis settles toward the heels with thighs folded over the shins',
  'the actor sits back toward the heels on grounded knees and shins, retaining a connected folded lower body'],
 'contrapposto_weight_shift': [
  '한 지지 다리에 주 체중을 두고 다른 다리는 풀리거나 굽으며 골반과 어깨가 반대로 기울어 머리와 몸통의 균형을 유지한다',
  '전신 선 자세에서 지지 다리와 쉬는 다리가 구분되고 반대 기울기의 어깨와 골반이 같은 몸을 균형 있게 잇는다',
  'one leg carries the standing weight while the other relaxes, with counter-tilted pelvis and shoulders balancing the head and torso',
  'a balanced full-body stance contrasts a support leg with a relaxed leg and opposing shoulder-pelvis tilts'],
 'mep_gaze_target': [
  '보이는 두 눈이 지정된 표적을 일관되게 향하고 얼굴 방향과 구도가 그 시선 관계를 읽게 한다',
  '얼굴의 방향과 맞는 안구 시선이 같은 목표에 닿고 눈과 목표 판단에 필요한 영역이 프레임에 남는다',
  'visible eyes point consistently toward the named target, with compatible face orientation and framing that shows the relation',
  'the specified gaze target is supported by readable eyes, a compatible face direction and sufficient framing'],
 'vg_matte_cloth_polished_metal_profile': [
  '같은 조명 아래 기존 천은 넓고 부드러운 명암을, 기존 광택 금속은 경계가 선명한 반사를 보인다',
  '기존 원단의 퍼진 색조 변화와 같은 빛 방향의 금속 반사 경계가 서로 대비된다',
  'the existing cloth gives broad soft tonal changes while polished metal gives tighter bounded reflections under the same light',
  'shared illumination contrasts soft matte textile shading with sharper reflections on the existing polished metal'],
 'egr_profile_matte_mourning_crape': [
  '지정된 어두운 천은 미세하게 불규칙한 저광택 표면을 가지며 주름에는 절제된 빛과 원단 경계가 남는다',
  '어두운 크레이프 원단의 잔잔한 불규칙 결이 주름과 함께 이어지고 빛은 약하게 남는다',
  'the selected dark low-sheen cloth retains fine irregular texture, restrained fold highlights and readable textile edges',
  'dark crape has a subtly uneven matte surface with connected folds and restrained edge-defining highlights'],
 'rb_glass_reflection_transmission': [
  '창틀이 유리면을 정하고 맞은편 건물 반사가 그 면에 맺히며 다른 구역으로는 창 안쪽이 읽힌다',
  '같은 창유리에서 맞은편 파사드의 반사와 유리 뒤 실내의 투과가 구역을 나누어 공존한다',
  'a window frame anchors the pane, opposite-facade reflection occupies one region and the interior reads through another',
  'the framed window combines a coherent opposite-building reflection with a separately readable interior through the glass'],
}

# A complete new relation receives descriptive alternatives, never a broad token alias.
# Components are meaning atoms; they do not encode a source-case palette or biography.
NEW = [
 ('closed_waist_vest_layers','닫힌 허리 베스트와 남는 중앙 안쪽 층','wardrobe_style',
  ['the vest waist panel is closed continuously over the inner top','side vest straps rise beside a central upper-chest area where the inner top and tie remain visible','the jacket opening reveals separate vest and inner-top boundaries'],
  ['베스트 허리 앞판이 안쪽 탑 위에서 닫히고 옆 끈 사이 상흉부 중앙에는 탑과 넥타이가 남으며 재킷 안쪽 층의 경계가 구분된다','a closed waist vest covers the inner top at the waist while ascending side straps leave the central top and tie visible inside a separate jacket opening'],
  [('vest_waist','lies_over','inner_top_waist'),('vest_side_straps','border','visible_central_top_and_tie'),('jacket_opening','reveals','separate_inner_layers')],
  [('appearance','main_subject','wardrobe.structure')],
  ['a center-open harness substituted for the closed waist panel','the inner top erased','busk boning or lacing added by the vest label'],
  'A waist closure and a visible upper center refer to different regions. Colors, collar design and fastening type remain separate choices.'),
 ('slipped_attached_shoulder_strap','两根肩带中一根滑落但仍连接的状态','garment_detail',
  ['the same garment has two attached shoulder straps','one attached strap rests outside the upper arm while the other remains on its shoulder','both strap ends continue to the same garment panels'],
  ['두 어깨끈 중 한쪽이 위팔 외측에 내려와도 양쪽 끝의 의복 연결과 반대 어깨의 지지가 남는다','같은 두 끈 의복에서 한 끈은 위팔 바깥으로 내려오고 다른 끈은 어깨에 남으며 두 끈의 끝은 옷에 연결된다','one of two still-attached garment straps has slipped outside the upper arm while the opposite strap remains supported on the shoulder'],
  [('lowered_strap','attaches_to','same_garment'),('supported_strap','rests_on','opposite_shoulder')],
  [('appearance','main_subject','wardrobe.straps.position')],
  ['original one-shoulder construction','a detached floating strap','a strap hidden entirely by hair'],
  'This describes a two-strap garment state, not a one-shoulder design. The support and both connections must be observable.'),
 ('mirror_surface_condensation_face','거울 표면 결로와 읽히는 반사 얼굴','texture',
  ['localized droplets or moisture haze belong to the mirror front surface','the same mirror retains a separately readable reflected face','reflected facial detail remains distinct from the surface moisture layer'],
  ['거울 앞면의 국소 물방울이나 습기막과 그 뒤로 읽히는 반사 얼굴이 다른 광학 층으로 보인다','local condensation sits on the mirror face while the reflected facial features remain separately readable'],
  [('condensation','belongs_to','mirror_front_surface'),('mirror','reflects','readable_face')],
  [('material','existing_mirror','surface.condensation'),('camera','capture_camera','focus.target')],
  ['camera defocus substituted for condensation','a window with an opposite facade substituted for the mirror','a fully erased reflected face'],
  'Condensation does not imply a shower story. Its contrast depends on illumination; a continuous film need not be white.'),
 ('open_ring_choker_mount','초커 앞에 부착된 열린 금속 고리','wearable_accessory',
  ['a rigid metal O-ring has a traceable open center at the choker front','the ring joins the neck-following band through readable mounting points','the ring aperture reveals the actual background behind the opening'],
  ['목을 따르는 초커 띠 앞의 금속 O링이 부착점으로 이어지고 열린 중앙에는 뒤쪽 실제 배경이 보인다','a hollow metal ring mounted to the front of the neck band retains a visible opening and separately traceable attachment points'],
  [('metal_ring','attaches_to','choker_front_band'),('ring_aperture','reveals','actual_background')],
  [('appearance','main_subject','accessories.choker.structure'),('material','main_subject','accessories.choker.material')],
  ['a solid round medallion','a tattoo-loop choker','an unattached floating ring'],
  'The ring and flexible neck band are distinct parts. No chain, restraint, force or relationship follows from this construction.'),
 ('contact_bedding_depression','身体接触位置对应的寝具下陷','contact_point',
  ['the resting head or shoulder contacts one soft bedding surface','the bedding is locally depressed at that same body contact patch','nearby less-compressed bedding continues around the depression'],
  ['머리나 어깨가 같은 푹신한 침구에 닿고 그 접촉 위치에서만 천이 눌리며 옆 침구는 덜 압축된 채 이어진다','soft bedding dips directly beneath the resting head or shoulder and continues into less-compressed fabric nearby'],
  [('head_or_shoulder','contacts','soft_bedding'),('bedding_depression','coincides_with','same_contact_patch')],
  [('pose','main_subject','body.support'),('material','existing_bedding','surface.deformation')],
  ['a nearby depression disconnected from the body','an unsupported floating head','a rigid floor substituted for bedding'],
  'Visible depression supports a contact depiction, not a force, duration or physical comfort measurement.'),
 ('small_lip_gap_concealed_teeth','작은 입술 틈과 가려진 치아','expression',
  ['upper and lower lip edges leave one narrow visible gap','the jaw remains only slightly open','the teeth remain concealed behind the lips at this selected viewing angle'],
  ['입술 사이에 좁은 틈이 있지만 턱은 조금만 열리고 이 시점에서 치아는 입술 뒤에 가려져 있다','a slim opening separates the lips with a barely opened jaw and teeth concealed at the selected angle'],
  [('upper_lip','separates_from','lower_lip'),('lips','occlude','teeth')],
  [('expression','main_subject','mouth.aperture')],
  ['a clenched closed lip seam','a broad jaw-drop opening','a tooth-baring grin'],
  'This is the selected small-gap-and-hidden-teeth form. A still image without scale cannot establish millimeters, breathing or emotion.'),
 ('barrier_localized_impact_depth','방어막 충돌과 뒤쪽 인물의 깊이 순서','action',
  ['an incoming effect meets a localized area on the front barrier surface','the figure remains separately readable behind the partly transparent barrier','impact particles originate at the effect-barrier contact region'],
  ['날아온 효과가 앞쪽 방어막의 한 구역에 닿고 뒤 인물이 따로 보이며 입자는 그 충돌 구역에서 퍼진다','a localized incoming strike meets the barrier in front of a readable figure, with particles radiating from that barrier contact'],
  [('incoming_effect','meets','barrier_front'),('figure','lies_behind','barrier'),('impact_particles','originate_at','barrier_contact')],
  [('action','existing_effect','trajectory.contact'),('composition','existing_barrier','depth.order'),('lighting','existing_contact_region','emission')],
  ['a body wound substituted for barrier contact','particles unrelated to the incoming path','an opaque sheet hiding the figure'],
  'The incoming effect, barrier and figure must already belong to the scene. Particular magic style or attack source remains open.'),
 ('shoe_chest_contact_separate_support','신발의 상대 의복 접촉과 별도 지지 발','contact_point',
  ['one actor shoe touches the other existing actor upper-chest garment','the shoe contact and receiving clothing patch are jointly visible','the contacting actor other foot rests separately on the floor'],
  ['한 인물의 신발이 다른 인물의 상흉부 의복에 닿고 받는 천과 접촉 경계가 보이며 반대 발은 바닥을 지지한다','one shoe contacts the other actor clothed upper chest while the contacting actor opposite foot remains separately planted on the floor'],
  [('contact_shoe','contacts','other_actor_chest_garment'),('opposite_foot','supports_on','floor')],
  [('pose','main_subject','feet.support_and_contact'),('relationship','other_subject','contact.receiving_surface')],
  ['contact transferred to the actor own chest','the support foot suspended','projection overlap without surface contact'],
  'A nonsexual two-actor contact configuration, not an injury, consent or duration claim. It cannot introduce a second actor into a single-person scene.'),
 ('hand_face_visible_clearance','손과 상대 얼굴 사이에 남는 간격','contact_point',
  ['one actor hand is directed toward the other existing actor face','a visible air gap separates the hand from that face','both the hand endpoint and face boundary remain readable together'],
  ['상대 얼굴 쪽으로 향한 손 끝과 얼굴 경계가 함께 보이며 둘 사이에 공기 간격이 남는다','the directed hand stops short of the other face with both endpoints visible across a clear gap'],
  [('directed_hand','approaches','other_actor_face'),('air_gap','separates','hand_and_face')],
  [('action','main_subject','hand.direction'),('relationship','other_subject','contact.clearance')],
  ['a striking hand in contact','the hand hidden beyond the crop','a gap asserted only by prose'],
  'The gesture does not by itself prove rebuke, injury or emotion. A second actor must already exist in the frozen scene.'),
 ('glass_rubble_material_contrast','유리 파편과 불투명 잔해의 표면 구별','material',
  ['bounded glass fragments have dielectric edges or partial transmission','nearby opaque rubble retains solid nontransmitting surfaces','both materials remain separate environmental objects'],
  ['환경의 유리 조각은 투과 또는 유전체 가장자리를 보이고 옆의 불투명 잔해는 막힌 고체 표면으로 구별된다','separate environmental debris contrasts bounded glass fragments with solid opaque rubble surfaces'],
  [('glass_fragments','contrast_with','opaque_rubble')],
  [('material','existing_debris','surface.optical_response')],
  ['all debris made uniformly transparent','metal sparks substituted for glass fragments','body damage inferred from environmental debris'],
  'Glass glints depend on source and viewpoint. Environmental breakage does not establish any person injury or event sequence.'),
 ('soft_contact_glass_patch','유리면에 닿아 눌린 국소 접촉 패치','contact_point',
  ['the selected soft body region meets the actual glass plane','a bounded contact patch shows local soft-surface flattening at that same plane','surrounding body and glass boundaries remain separately continuous'],
  ['지정한 부드러운 신체 부위가 실제 유리면에 닿고 그 패치에 국소 눌림이 보이며 주변 몸과 유리 경계는 각각 이어진다','a bounded soft body contact patch flattens against the actual pane while surrounding body and glass contours remain continuous'],
  [('soft_body_region','contacts','actual_glass_plane'),('local_flattening','coincides_with','contact_patch')],
  [('pose','main_subject','body.contact'),('body_geometry','main_subject','contact.local_deformation')],
  ['a hovering body near glass','a reflected duplicate substituted for contact','an added pusher or injury'],
  'Contact is a visible local configuration. Force, duration, consent and confinement cannot be inferred from this patch.'),
 ('airborne_red_code_metal_receiver','공중 붉은 기호와 금속의 광원 반사 구별','light_type',
  ['red luminous code shapes occupy the air in front of an existing machine','a separate bounded machine aperture acts as a red light source','nearby metal receives localized red reflections aligned with that source'],
  ['기계 앞 공중에 붉게 빛나는 코드가 있고 별도 틈의 붉은 광원과 그 방향을 받는 금속 반사가 구별된다','airborne red symbols, a bounded machine emission opening and source-aligned reflections on nearby metal remain three distinct light owners'],
  [('luminous_code','occupies','air_before_machine'),('machine_aperture','emits_toward','metal_receiver')],
  [('lighting','existing_machine','emission.source'),('lighting','existing_metal','reflected_color'),('color','existing_code','emissive.color')],
  ['a red bloodstain substituted for emitted light','uniform red grading of the whole frame','status LED substituted for airborne code'],
  'Symbols need not be readable language unless requested. A blood exclusion does not exclude red emitted light or reflected color.'),
 ('held_towel_continuous_front','같은 타월을 양손에 든 전면 가림','garment_detail',
  ['both hands grip separate points on the upper edge of the same towel','the upper towel edge is tensioned while its center hangs continuously over the front torso and pelvis','the separately worn swimsuit remains behind the towel with only a small strap region visible'],
  ['양손이 같은 타월 윗단의 다른 점을 잡고 위는 팽팽한 반면 중앙은 몸통과 골반 앞에 연속해서 늘어지며 뒤 수영복은 작은 끈 영역만 보인다','two hands hold one towel upper edge taut as its central panel drapes continuously across the torso and pelvis, leaving a small strap window of the separate swimsuit behind it'],
  [('left_hand','grips','same_towel_upper_edge'),('right_hand','grips','same_towel_upper_edge'),('towel_center','occludes','front_torso_and_pelvis'),('swimsuit','lies_behind','held_towel')],
  [('appearance','main_subject','wardrobe.layering_and_coverage'),('pose','main_subject','hands.grip'),('material','existing_towel','fabric.tension_and_drape')],
  ['a towel wrapped around the body','two disconnected towels','an open central gap exposing the covered region'],
  'This selected variant includes a separately worn swimsuit. Color and lower-edge height are open choices; the same cloth and central coverage must persist.'),
]

# Candidate-only alternatives whose profile has a different owner or none.
EXTRA = {
 ('gaze_target','head_eye_counterorientation_relation'): [
  '머리가 향한 방향과 같은 인물의 눈동자가 향한 두 번째 목표가 다르고 눈과 목 연결은 자연스럽게 이어진다',
  'the head turns one way while the same actor irises return toward a second readable target with coherent eyes and neck'],
 ('gaze_engagement','pv_gaze_direct'): [
  '보이는 눈동자 또는 안구 축이 카메라를 향하고 얼굴 방향은 별도로 정해진다',
  'readable pupils or eye axes point toward the lens independently of the stated face orientation'],
 ('surface_material','y2kr_satin'): [
  '부드럽게 늘어진 매끈한 천 주름에 넓고 이어진 방향성 하이라이트가 남는다',
  'smooth softly draped cloth folds carry broad continuous directional highlights'],
 ('wearable_accessory','unif_lapel_chain_separate_inner_neck'): [
  '적갈색 바깥 라펠의 사슬 부착과 뒤쪽 올라온 안쪽 목선의 별도 의복 층이 구분된다',
  'the chain stays attached to the maroon outer lapel while the raised inner collar remains a distinct layer behind it'],
 ('garment_detail','water_w159'): [
  '지정한 몸 부위를 타월의 한 면이 겹쳐 두르고 가장자리 접촉과 천 결이 보인다',
  'one continuous towel wraps and overlaps around the stated body region with readable fabric and edge contact'],
 ('texture','condensation_window_smear_texture'): [
  '창유리 표면에 밀려 번진 응결 수분의 결',
  'a dragged moisture smear lies on the window glass surface'],
 ('wearable_accessory','ctx_c019'): [
  '성인의 목 둘레를 따라가는 가느다란 초커 띠',
  'a slim neck band follows the adult neck contour'],
 ('prop','real_holstered_service_pistol'): [
  '눈에 보이는 홀스터 안에 놓인 실제 서비스 권총',
  'a service pistol remains seated inside a visible holster'],
 ('action','carrying_holstered_real_sidearm'): [
  '보이는 홀스터에 권총 모양 참고 소품을 넣어 착용한 상태',
  'the actor wears a sidearm-shaped reference prop retained in a readable holster'],
 ('light_type','status_led_glow'): [
  '기계 상태 표시 LED의 작은 발광',
  'a small status-indicator LED emits its own light'],
 ('contact_point','no_contact_just_close'): [
  '서로 가까운 두 표면 사이에 실제 간격이 남아 접촉하지 않은 배치',
  'the nearby surfaces remain separated by a visible air gap'],
 ('fetish_styling','glossy_latex_look'): [
  '라텍스처럼 광택이 강한 패션 의복 조각',
  'fashion garment pieces with a glossy latex-like surface'],
}

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 manifest=read(ASSETS/'photo_prompt_source_manifest.json')
 raw={r['file']:read(ASSETS/r['file']) for r in manifest['sources']}
 raw['photo_prompt_visual_obligations.json']=read(ASSETS/'photo_prompt_visual_obligations.json')
 baseline={f:hashlib.sha256((ASSETS/f).read_bytes()).hexdigest() for f in raw}
 if (OUT/'IMPLEMENTATION-SUMMARY.json').exists():
  baseline=read(OUT/'IMPLEMENTATION-SUMMARY.json')['baseline_source_hashes']
 data=pg.load_json(ASSETS/'photo_prompt_tags.json')
 slot_lookup={r['id']:(s,r) for s,rows in data['slots'].items() for r in rows}
 profile_lookup={r['id']:(f,r) for f,d in raw.items() for r in d.get('profiles',[])}
 extension={'schema_version':'photo-prompt-research-extension/v1','slots':{},'existing_slot_context_extensions':{},'visual_semantics':[]}
 delta=[]; changed=set(); existing_candidate_count=0
 def add_context(slot,eid,variants,limits):
  nonlocal existing_candidate_count
  assert any(r['id']==eid for r in data['slots'][slot]),(slot,eid)
  target=extension['existing_slot_context_extensions'].setdefault(slot,{}).setdefault(eid,{'paraphrases':[],'contexts':[]})
  target['paraphrases']=unique(target['paraphrases']+variants)
  if not target['contexts']:
   target['contexts'].append({'id':'vel_'+eid+'_meaning_boundary','definition':'Interpret the existing entry on its declared owner and within frozen scope.','claim_limits':limits,'activation_authority':'interpretation_only_not_a_required_visual_recipe'})
   existing_candidate_count+=1
 for pid, variants in EXISTING.items():
  f,p=profile_lookup[pid]
  old=copy.deepcopy(p)
  p['semantics']['paraphrase_examples']=unique(p['semantics']['paraphrase_examples']+variants)
  p['concept_candidate']['concept_terms']=unique(p['concept_candidate']['concept_terms']+variants)
  delta.append({'file':f,'profile_id':pid,'paraphrases':variants,'unchanged_activation':old['activation'],'unchanged_authored_components_sha256':hashlib.sha256(json.dumps(old['authored_components'],sort_keys=True).encode()).hexdigest()})
  changed.add(f)
  # Exact matching morphology; exceptions deliberately listed, not fuzzy guessed.
  candidate_id={'pfe_slit':'pfe_slit_candidate','pfe_opaque_fit':'pfe_opaque_fit_candidate','pfe_skimming':'pfe_skimming_candidate','pfe_one_shoulder':'pfe_one_shoulder_candidate','lace_trim_attached_edge':'lace_trim_edge','hvr_profile_wet_hair_skin_contact':'hr_wet_hair_skin_contact','vg_faille_crossgrain_ribs_profile':'vg_faille_crossgrain_ribs','vg_matte_cloth_polished_metal_profile':'vg_matte_cloth_polished_metal','egr_profile_matte_mourning_crape':'egr_matte_mourning_crape','mep_gaze_target':'mep_gaze_target_candidate','rb_glass_reflection_transmission':'rb_glass_reflection_transmission_candidate','contrapposto_weight_shift':'contrapposto_full_body'}.get(pid,pid.removeprefix('pv_profile_').removeprefix('egr_profile_').removeprefix('vg_').removesuffix('_profile'))
  if pid.startswith('pv_profile_'):candidate_id='pv_'+pid.removeprefix('pv_profile_')
  if candidate_id in slot_lookup:
   s,r=slot_lookup[candidate_id];add_context(s,candidate_id,variants,p['semantics'].get('claim_limits',[]))
  else:
   # Record no candidate mutation when a source has no equivalent same-owner candidate.
   delta[-1]['candidate_unmatched']=candidate_id
 for (s,eid),variants in EXTRA.items():
  add_context(s,eid,variants,['The existing owner, object and action remain unchanged; retrieval context creates no hard obligation.'])
 profiles=[]
 component_alternatives=read(OUT/'component_alternatives.json')
 for name,ko,slot,units,variants,rels,props,confounds,limits in NEW:
  if name=='slipped_attached_shoulder_strap':ko='두 끈 중 하나가 내려온 부착 상태'
  if name=='contact_bedding_depression':ko='신체 접촉 위치에 대응하는 침구 눌림'
  eid='vel_'+name;pid=eid+'_profile';definition='; '.join(units)
  dimensions=unique([x[0] for x in props])
  properties=[{'dimension':dim,'target':target,'property':prop} for dim,target,prop in props]
  relation_rows=[{'id':eid+'_r'+str(i+1),'type':kind,'subject':subject,'object':obj} for i,(subject,kind,obj) in enumerate(rels)]
  row={'id':eid,'ko':ko,'en':definition,'weight':0.38,'tags':['observable_relation'],'for_any':['human'],'aliases':[ko],'keywords':[ko]+units,'paraphrases':variants,'concept_units':units,'relations':relation_rows,'affected_dimensions':dimensions,'affected_properties':properties,'core_assertion_discovery':True,'contextual_usage':{'contexts':[{'id':eid+'_boundary','definition':limits,'claim_limits':[limits],'activation_authority':'interpretation_only_not_a_required_visual_recipe'}]},'embedding_text':'; '.join([ko,definition]+variants)}
  extension['slots'].setdefault(slot,[]).append(row)
  components=[]
  for i,u in enumerate(units,1):
   alternatives=component_alternatives[name][i-1]
   components.append({'id':'component_'+str(i),'match_terms':[u]+alternatives,'evidence_field':'component_'+str(i)+'_phrase','evidence_terms':[u]+alternatives,'min_content_words':3,'instruction':'Keep the declared owner and complete selected relation visible: '+u,'render_gate':{'id':'vo_'+eid+'_'+str(i),'review_scale':'both','description':u+'. Inspect the same saved image at full-frame and native detail; hidden, substituted or partial components fail.'}})
  profiles.append({'id':pid,'category':'owner_bound_visual_relation','activation':{'exact_terms':[definition],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_relation','any_terms':[definition]}]}},'semantics':{'definition':definition,'paraphrase_examples':variants,'visual_components':units,'contrast_examples':confounds,'claim_limits':[limits],'interpretation_scope':{'kind':'observable_relation','description':'A complete selected relation on existing scene owners; descriptive alternatives aid retrieval without becoming exact hard aliases.'}},'concept_candidate':{'concept_terms':[ko]+variants+units,'core_assertion_discovery':True,'affected_dimensions':dimensions,'affected_properties':properties},'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':confounds})
 for f in sorted(changed):write(ASSETS/f,raw[f])
 candidate_file='photo_prompt_vel_appearance_relations_extension.json'
 profile_file='photo_prompt_visual_obligations_vel_appearance_relations.json'
 provenance={'contract_version':'vel-alternative-expression-adoption/v1','record_id':'vel-alternatives-20261007','input_research':'vel-visual-semantics-20261007 and appearance-decomposition-followup','prior_original_authentication':'historical original prompts and pixels not independently authenticated','existing_profile_delta':delta,'new_relations':[{'id':'vel_'+r[0],'relation':r[5],'confounds':r[7],'claim_limits':r[8]} for r in NEW]}
 write(OUT/'ADOPTION.json',provenance)
 record={'schema_version':'photo-extension-maintenance/v1','maintenance_only':True,'source_filename':candidate_file,'description':'Reviewed bilingual same-owner alternatives and complete optional appearance relations. Research observations do not authenticate historical originals or rendered success.','adoption_evidence':'docs/research-evidence/photo-prompt/vel-alternatives-integration-20261007/ADOPTION.json','reviewed_existing_profile_count':len(EXISTING),'new_relation_count':len(NEW)}
 record_path=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/vel-alternatives-20261007.json'
 record_path.parent.mkdir(parents=True,exist_ok=True);write(record_path,record)
 extension['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':'vel-alternatives-20261007','sha256':hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
 write(ASSETS/candidate_file,extension)
 write(ASSETS/profile_file,{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':profiles})
 for f,kind in [(candidate_file,'candidate'),(profile_file,'visual_profile')]:
  if any(r['file']==f for r in manifest['sources']):continue
  order=max(r['load_order'] for r in manifest['sources'] if r['kind']==kind)+1
  manifest['sources'].append({'file':f,'kind':kind,'required':True,'load_order':order})
 write(ASSETS/'photo_prompt_source_manifest.json',manifest)
 summary={'existing_profiles_enriched':len(EXISTING),'existing_profile_paraphrases_added':sum(len(v) for v in EXISTING.values()),'existing_candidates_enriched':existing_candidate_count,'existing_candidate_paraphrases_added':sum(len(r['paraphrases']) for rows in extension['existing_slot_context_extensions'].values() for r in rows.values()),'new_profiles':len(profiles),'new_candidates':sum(len(rows) for rows in extension['slots'].values()),'new_descriptive_paraphrases':sum(len(p['semantics']['paraphrase_examples']) for p in profiles),'new_component_alternative_expressions':sum(len(terms) for rows in component_alternatives.values() for terms in rows),'activation_and_obligations_of_existing_profiles_preserved':True,'baseline_source_hashes':baseline,'changed_profile_files':sorted(changed),'new_files':[candidate_file,profile_file]}
 write(OUT/'IMPLEMENTATION-SUMMARY.json',summary)
 print(json.dumps({k:v for k,v in summary.items() if k!='baseline_source_hashes'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
