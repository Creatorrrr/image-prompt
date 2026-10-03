"""Apply reviewed, observable alternatives without promoting broad labels to exact aliases.

Research rows are provenance, not runtime schema. Existing contracts and effects
are preserved; only their positive paraphrases and non-indexed limits are extended.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg

TABLE='''
soft_full_figure_volume|몸통과 골반, 위팔과 허벅지에 둥근 살집이 연속된 성인 체형|a plump adult build with rounded soft volume through torso hips upper arms and thighs|여러 몸 구간의 풍부한 볼륨이 부드럽게 이어지는 성인 전신 형태|a fleshy full figure with continuous soft contours across several torso and limb regions
slender_linear_build|성인 몸통과 팔다리의 가로 폭이 전반적으로 좁고 관절 연결이 자연스러운 체격|a slender adult frame with narrow torso and limb volumes and continuous joint transitions|몸통에서 팔과 다리까지 가는 가로 볼륨이 이어지는 선형 체형|a slim linear build whose narrow transverse contours continue from torso into limbs
curvilinear_figure_relation|상체에서 자연 허리와 골반, 허벅지까지 안으로 들어가고 밖으로 나오는 선이 이어지는 성인 몸매|a curvaceous adult figure with alternating inward and outward contours across upper torso waist hips and thighs|위몸통과 옆허리, 골반과 허벅지 사이의 여러 둥근 전환이 연결된 형태|a curvy figure defined by several connected convex and concave torso-to-thigh transitions
toned_muscular_build|성인 어깨와 팔, 몸통과 다리에서 절제된 근육 면과 힘줄 전환이 읽히는 체격|a toned adult build with restrained muscle planes and tendon transitions across upper and lower body|여러 상체와 하체 구간에서 얕은 근육 경계가 자연스럽게 이어지는 성인 형태|a moderately defined adult physique with readable muscle and tendon contours in several body regions
bust_prominence_relation|같은 성인의 양쪽 가슴 볼륨이 흉곽보다 앞과 옆으로 나와 자연 허리와 비교되는 형태|a bust-prominent adult torso with bilateral breast volume projecting from the ribcage beside the natural waist|양측 가슴의 돌출을 흉곽 바탕과 허리 관계 안에서 함께 읽는 성인 실루엣|bilateral breast prominence shown with coherent front and side projection relative to ribcage and waist
hourglass_silhouette_relation|성인 상체와 골반의 폭 사이에서 자연 허리가 양쪽보다 좁게 이어지는 비율|an adult hourglass relation with a narrower natural waist between upper torso and hips|윗몸통과 골반의 양쪽 폭이 허리의 들어감과 함께 읽히는 전신 관계|balanced upper-torso and hip widths linked by an inward natural-waist transition
triangle_lower_body_dominant_relation|성인 상체보다 골반과 허벅지의 가로 볼륨이 넓게 읽히는 하체 중심 비율|a lower-body-dominant adult silhouette with hips and thighs broader than the upper torso|같은 인물의 위몸통과 비교해 골반과 위허벅지 폭이 상대적으로 큰 형태|a pear-like adult proportion defined by relative upper-torso hip and thigh widths
inner_thigh_negative_space|곧고 가까운 두 다리와 거의 맞닿은 발 위에서 안쪽 윗허벅지 사이로 연속 배경이 보이는 틈|continuous background between the actual upper inner-thigh edges above close straight legs and nearly touching feet|두 다리를 가까이 둔 서기에서 양쪽 안허벅지 경계가 작은 배경 공간을 둘러싸는 형태|a stance-dependent inner-thigh gap bounded by both thigh contours while the feet remain close
upper_lip_philtral_contour|인중 중앙 홈 양옆의 두 기둥이 윗입술의 두 봉우리 곡선으로 이어지는 얼굴 세부|two philtral ridges descend around a central groove into the paired Cupid's-bow arcs|중앙 인중 홈과 양쪽 솟은 선, 윗입술 이중 곡선의 연속 관계|the central philtral groove and its bordering columns join a double upper-lip arc
decolletage_neckline_exposure|낮은 옷 목선 안에서 목 아래와 쇄골, 어깨와 위가슴이 함께 드러나는 성인 패션 관계|a low neckline frames the adult lower neck clavicles shoulders and upper chest|의복 네크라인이 쇄골과 어깨를 포함한 위가슴 노출 영역을 정하는 형태|a neckline-defined decolletage region connecting lower neck shoulders and upper chest
sheer_garment_optical_layering|직물의 실과 가장자리, 접힘이 남아 있고 같은 천 너머의 표면과 빛이 부분적으로 보이는 겹침|a translucent cloth layer retains visible fibers edges and folds while partly transmitting light and the underlying surface|직조와 솔기 경계가 식별되는 얇은 천이 아래 표면을 부분적으로 투과시키는 모습|a sheer textile remains materially present through weave seams and diffusion over the requested underlying surface
bm_stature_scale|같은 깊이의 비교 물체 옆에서 성인 머리부터 발까지의 낮은 신장이 읽히는 관계|short adult stature measured visually against a same-plane reference with head-to-foot extent readable|머리와 발의 전체 높이를 같은 평면의 기준과 비교하는 작은 성인 신장|an adult's short vertical extent compared with an explicit reference at the same depth
bm_compact_frame|키는 별도로 두고 몸통의 가로 규모와 사지 구간이 조밀하게 읽히는 성인 골격 비율|a compact adult torso-and-limb frame with stature specified independently|몸통 폭과 팔다리 구간의 규모가 함께 작은 틀을 이루는 성인 체격|a close-set adult body frame described by transverse torso extent and limb segment scale
bm_stocky_build|사지 길이에 비해 몸통과 팔, 다리가 두툼한 성인 체격|a stocky adult build with thick torso and limb volumes relative to segment length|같은 인물의 몸통과 팔다리 가로 두께를 해당 구간 길이와 비교한 형태|a sturdy-looking adult frame defined by transverse torso and limb thickness against their lengths
bm_long_limb_build|몸통 길이를 기준으로 팔과 다리가 길고 가는 성인 비율|a willowy adult proportion with long slender limb segments relative to a readable torso|같은 성인의 몸통에 비해 상지와 하지가 길게 이어지고 가로 폭은 가는 형태|elongated slender arms and legs compared with the same adult torso reference
bm_wiry_definition|가는 성인 몸통과 팔다리에 국소 근육 면과 힘줄 선이 읽히는 체격|a sinewy adult build with narrow torso and limbs plus localized muscle planes and tendon contours|사지 폭은 가늘고 그 표면의 얕은 근육과 힘줄 윤곽이 구별되는 성인 형태|a wiry adult frame whose slender volumes retain readable local muscle and tendon definition
bm_muscle_volume|명시한 성인 근육의 배가 두툼하고 양쪽 관절 부착으로 자연스럽게 이어지는 부피|substantial volume of a named adult muscle belly with continuous anatomical attachments|지정된 근육 부위의 팽창된 볼륨과 관절 연결을 함께 읽는 형태|regional muscular bulk anchored to the stated muscle and its connected joints
bm_shoulder_width|같은 시점에서 양쪽 어깨 끝 사이 폭을 흉곽 폭과 비교하는 성인 비율|both adult shoulder endpoints define a width compared with the ribcage in the same view|흉곽 기준과 좌우 어깨 경계가 함께 보이는 가로 폭 관계|bilateral shoulder breadth read against the same torso's ribcage reference
bm_breast_root_width|각 가슴이 흉벽에 붙는 안쪽부터 바깥쪽까지의 가로 바탕 범위|the medial-to-lateral attachment footprint of each breast on the same adult chest wall|같은 가슴의 내측과 외측 기저 경계를 흉곽 바탕 위에서 비교한 부착 폭|breast base width shown by medial and lateral attachment extents on its chest-wall owner
bm_breast_root_height|성인 가슴이 흉벽에 붙는 위쪽부터 아래쪽까지의 세로 범위|the superior-to-inferior attachment extent of the adult breast on the chest wall|위 부착 경계와 아래 부착 구간을 흉벽 기준 안에서 읽는 세로 바탕 높이|vertical breast-root extent bounded by its upper and lower attachment regions
bm_breast_projection|같은 성인의 국소 흉벽 면에서 가슴 앞 경계까지 나온 깊이|anterior breast projection measured visually from the local adult chest-wall plane|흉벽 바탕과 앞으로 나온 가슴 윤곽이 같은 사선 보기에서 읽히는 돌출|breast projection depth between its chest-wall base and anterior contour
bm_breast_fullness|같은 가슴의 위아래와 안팎 구간별로 나뉘어 읽히는 볼륨 분포|regional fullness distributed between the upper lower medial and lateral parts of the same adult breast|하나의 가슴에서 지정한 위·아래 또는 안·밖 구간의 둥근 볼륨을 비교하는 형태|breast fullness compared across named regional partitions within the same owner
bm_breast_spacing|몸통 중앙선 양쪽의 가슴 안쪽 경계와 그 간격, 방향의 관계|the two medial breast contours define spacing and orientation about the adult torso midline|같은 성인의 좌우 가슴 경계를 정중선 기준에서 함께 비교하는 형태|bilateral breast separation and direction read against the same torso centerline
bm_breast_vertical_position|같은 가슴의 아래 접힘을 기준으로 가슴 윤곽과 돌출점의 위아래 위치가 읽히는 관계|breast contour and nipple height read relative to the same adult inframammary fold|가슴 아래 주름과 가슴 앞 돌출점, 주변 윤곽을 한 상태에서 비교하는 세로 관계|the vertical positions of breast contour and nipple compared with their connected lower fold
bm_waist_width_depth|갈비뼈와 골반 사이 자연 허리의 좌우 폭과 앞뒤 깊이를 따로 읽는 형태|adult waist width and front-to-back depth shown with rib and pelvis references|허리 양옆 경계와 앞뒤 윤곽이 같은 몸통 기준에 연결된 형태|transverse waist extent and sagittal depth compared within the same adult torso
bm_abdominal_projection|같은 성인의 상복부와 하복부가 옆몸통 기준으로 얼마나 앞으로 나오는지 읽는 관계|upper and lower abdominal projection linked by a continuous adult side-torso contour|상복부와 아래배의 볼륨을 이어지는 옆선 안에서 구별하는 형태|the upper belly and lower abdomen have separately readable projections along the same torso
bm_hip_width|같은 성인의 골반 양쪽 폭을 허리와 상체 폭에 견주어 읽는 형태|bilateral adult hip breadth compared with natural waist and upper-torso widths|양쪽 골반 바깥 경계와 허리, 위몸통이 같은 보기에서 연결되는 폭 비율|the left and right hip contours define width relative to the same waist and upper torso
bm_gluteal_projection|골반 바탕에서 뒤로 나온 둔부 윤곽이 허벅지 부착으로 이어지는 깊이|posterior gluteal projection from the adult pelvis continuing into the thigh attachment|같은 골반의 뒤쪽 바탕과 둔부 돌출, 위허벅지 연결이 함께 읽히는 형태|buttock projection depth anchored to the same pelvis and connected upper thigh
bm_gluteal_fullness|둔부 위쪽과 아래쪽의 살집이 하나의 연속된 뒤 윤곽 안에서 읽히는 분포|upper and lower adult gluteal fullness along one continuous posterior contour|같은 둔부의 상부와 하부 볼륨을 이어지는 뒤쪽 경계로 비교하는 형태|regional buttock fullness compared along the same connected upper-to-lower outline
bm_thigh_volume|성인 위허벅지와 중간 허벅지의 가로 볼륨이 무릎 쪽으로 자연스럽게 이어지는 형태|adult thigh volume tapers coherently from the upper and middle thigh toward the knee|같은 다리의 윗부분 살집과 허벅지 중간 윤곽, 무릎 연결이 읽히는 형태|rounded thigh transverse volume with a continuous anatomical knee transition
bm_hip_dip_local|골반 옆선의 국소 들어감이 바깥 위허벅지 경계로 이어지는 형태|a localized adult lateral hip indentation continues into the outer upper thigh|같은 골반 바깥 윤곽에서 위허벅지로 넘어가는 짧은 패임|a local concave hip contour above the connected outer thigh
bm_lip_volume|같은 얼굴의 윗입술과 아랫입술 붉은 면 두께, 입 틈 경계가 함께 읽히는 형태|upper and lower vermilion fullness and their mouth-opening boundary on the same adult face|윗입술과 아랫입술의 볼륨과 바깥 경계가 구별되는 입술 구조|the thickness of both lip surfaces and their perimeter remain separately readable
bm_eye_aperture|같은 눈의 위아래 눈꺼풀 가장자리 사이 가로·세로 열린 크기|horizontal and vertical eye-opening extents bounded by the same adult eyelid margins|한 눈의 눈꺼풀 틈 폭과 높이를 가장자리 기준에서 비교하는 형태|eye aperture width and height measured visually between its upper and lower lid boundaries
bm_fabric_body_outline|연속된 불투명 옷이 같은 성인 몸에 닿아 국소 몸 윤곽을 바깥 천 표면으로 전달하는 모습|continuous opaque clothing follows the same adult body at contact and transmits its local contour|몸과 천의 접촉 때문에 바깥 옷 경계에 해당 부위 형태가 읽히는 관계|a body outline carried by a continuous opaque garment surface at the stated contact
bm_garment_central_crease|같은 불투명 옷 중앙의 국소 접힘 양옆에 두 천 윤곽이 이어지는 형태|a localized central crease in the same opaque garment with adjacent paired fabric contours|중앙에 들어간 천 선과 그 양쪽의 의복 표면이 연결되는 국소 주름|a central garment fold bordered by two connected fabric contours
bm_cellulite_relief|명시한 성인 피부 부위에 작은 오목함과 고르지 않은 지형이 연속 피부로 이어지는 모습|localized skin dimples and uneven adult surface relief continuous with neighboring skin|같은 피부 표면에서 읽히는 얕은 오목한 요철의 국소 분포|a localized dimpled skin surface whose small depressions retain continuous skin ownership
bm_striae_surface|같은 성인 피부에 길쭉한 띠가 국소 색과 질감 차이를 이루는 표면|elongated striae-like bands with localized color and texture changes on the same adult skin|피부에 이어진 가늘고 긴 선형 띠들의 색·미세 지형 관계|long narrow skin bands retain readable localized pigment and surface-texture differences
bm_skin_tone_appearance|기록한 조명과 화이트밸런스 아래 같은 성인 피부에서 보이는 색|apparent adult skin color read under the declared lighting and white balance|같은 피부 부위의 현재 색을 빛과 색 균형 조건 안에서 읽는 모습|the current color appearance of a named skin region with illumination conditions stated
bm_skin_relief_texture|미세 모공과 피부 지형은 남고 반사광과 표면 거칠기가 따로 읽히는 성인 피부|a smooth-looking adult skin surface retains fine pores and low relief distinct from specular finish|피부의 작은 모공과 얕은 미세 지형이 광택층과 구별되는 모습|fine pores and subtle skin microrelief remain readable beneath the independently selected surface finish
bm_pose_surface_change|같은 성인 부위의 현재 하중이나 굽힘, 접촉에 맞춰 국소 피부·옷 표면이 달라진 상태|a localized adult surface contour change follows the declared current load flexion or contact|지정한 몸 구간의 지금 자세와 물체 접촉에 연결된 표면 변화|the named body region's present surface change is tied to its visible flexion or contact state
bm_compression_contour|같은 옷 띠 가장자리가 성인 몸에 닿은 곳에서 주변 윤곽이 국소적으로 밀리는 형태|localized adult contour displacement beside the same garment band's contact edge|의복 띠의 식별 가능한 경계와 몸 접촉, 인접한 눌림 윤곽이 함께 읽히는 관계|a visible clothing-band edge contacts the named region beside a localized contour indentation
pfe_cleavage|성인 옷 목선 안에서 양쪽 가슴 사이 피부의 중앙 오목한 선과 같은 옷 경계가 읽히는 관계|a central intermammary depression lies inside the adult neckline with continuous constructed garment edges|같은 네크라인 양쪽 경계가 가슴 사이 중앙 피부 윤곽을 둘러싸는 모습|the same garment neckline bounds a readable central skin depression between the breasts
pfe_lateral_chest|같은 불투명 몸판의 옆 가장자리 밖에서 제한된 바깥 가슴 윤곽이 보이는 성인 의복 관계|a bounded lateral breast contour is visible beside the same adult opaque bodice edge|가슴 중앙은 덮고 옆 의복 경계 밖에서만 외측 윤곽이 드러나는 형태|the opaque bodice covers the central breast while its continuous side edge borders a limited outer contour
pfe_lower_chest|같은 불투명 상의 밑단 아래에 제한된 가슴 하부 윤곽이 드러나는 성인 의복 관계|a bounded lower breast contour remains visible below the same adult opaque top hem|상의의 연속된 밑단과 그 아래 가슴 윤곽을 같은 인물에서 함께 읽는 형태|the continuous opaque top hem bounds the same adult's limited lower breast contour
'''

# Existing gaze and action entries own these observable states; no duplicate
# gaze registry or interpretation-to-emotion route is introduced.
CANDIDATE_ONLY={
 'pv_gaze_direct':['같은 인물의 보이는 눈 축이 카메라 쪽으로 모이는 주시','the visible irises of the declared actor align with the camera direction'],
 'pv_gaze_offcamera':['얼굴 방향과 별도로 지정한 화면 밖 대상을 향하는 눈 축','the actor eye axes point toward the declared off-camera target'],
 'pv_side_eye':['얼굴 방향에 비해 양쪽 눈동자가 지정한 옆 대상으로 돌아간 현재 시선','a sideways glance with irises displaced laterally relative to the same face orientation','머리의 회전과 구분되는 눈동자의 옆 방향 이동','both visible irises look laterally toward the declared target while head yaw remains separately readable'],
 'pv_half_lidded':['위아래 눈꺼풀 틈이 작아져도 눈동자가 일부 보이는 상태','narrowed eye apertures remain open with partly visible pupils'],
 'pv_parted_lips':['같은 얼굴의 위아래 입술 사이에 작고 보이는 틈이 남은 상태','a small readable gap remains between the same actor upper and lower lips'],
 'ae_pucker':['입 양끝이 중앙으로 모이고 입술이 앞으로 둥글게 나온 현재 표정','a current forward lip pout with rounded projecting lips and mouth corners gathered inward','원래 입술 두께와 별도로 입술을 앞으로 내민 순간','the lips currently protrude in a small rounded pucker while the corners move toward the center'],
 'ae_purse':['입 양끝이 가까워지고 입 틈이 좁고 둥글어진 상태','the mouth corners approach the center around a narrowed rounded lip opening'],
 'realistic_skin_texture_no_retouch':['얼굴 표면의 미세 질감과 자연스러운 모공이 남은 인물 사진','a portrait retains real fine skin texture and natural pore detail'],
 'skin_texture':['표면의 미세 지형이 남은 자연스러운 피부 질감','natural skin microtexture remains visible'],
}


def read(p): return json.loads(p.read_text())
def write(p,value): p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def profile(profile_id, terms, components, ko, en, *, expression=False):
    effects=['expression'] if expression else ['body_geometry']
    property_name='face.expression' if expression else 'body'
    groups=[{'id':f'component_{i+1}','any_terms':[text]} for i,text in enumerate(components)]
    activation={'exact_terms':terms,'requires_adult_character':not expression,'semantic_discovery_requires_component_evidence':True}
    if expression:
        activation['hard_activation']={'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'actor_face_context','any_terms':['face','facial','portrait','actor','person','human','woman','man','얼굴','표정','인물','사람','배우','초상']}]}
    fields=[f'component_{i+1}_phrase' for i in range(len(components))]
    authored=[]
    for i,text in enumerate(components):
        authored.append({'id':f'component_{i+1}','match_terms':[text],'evidence_field':fields[i],'evidence_terms':[text],'min_content_words':3,'instruction':f'Preserve the declared owner and show this complete current relation: {text}.','render_gate':{'id':f'vo_{profile_id}_{i+1}','review_scale':'native','description':f'Inspect the declared owner at native resolution: {text}. Every component is required; partial evidence fails and an occluded component is unobservable.'}})
    return {'id':profile_id,'category':'observable_current_expression' if expression else 'adult_regional_contour_relation','activation':activation,'semantics':{'definition':en,'paraphrase_examples':[ko,en],'visual_components':components,'component_semantics':{'minimum_component_groups':len(groups),'required_group_ids':[g['id'] for g in groups],'groups':groups},'contrast_examples':(['full lips without current forward motion','lip pressing alone','lip gloss without a projecting contour','assumed sulking or invitation'] if expression else ['whole-body build substituted for the named region','garment padding substituted for bodily volume','shadow alone substituted for the continuous outline']),'claim_limits':['All evidence belongs to the same declared owner and current state; occlusion is unobservable and partial evidence fails complete qualification.','Visible shape does not establish real emotion, health, body composition, attractiveness, intent, consent or history.','Retrieve broad labels only as advisory interpretations; no bare plump, fleshy, curvaceous or pouty exact alias is supplied.','Regional body alternatives declare broad body effects and cannot bypass a partial body-property lock.']},'concept_candidate':{'concept_terms':[ko,en,*components],'core_assertion_discovery':True,'affected_dimensions':effects,'affected_properties':[{'dimension':effects[0],'target':'main_subject','property':property_name}]},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':authored},'required_evidence_fields':fields,'evidence_requirements':{field:{'min_content_words':3,'must_mention_any':[components[i]]} for i,field in enumerate(fields)},'render_gates':[a['render_gate'] for a in authored],'composition_instruction':' '.join(a['instruction'] for a in authored),'reject_substitutes':['wrong_owner_or_named_region','occluded_required_component',*( ['static_lip_volume_for_current_expression','motive_inferred_from_lip_shape'] if expression else ['clothing_bulk_for_body_contour','one_component_for_complete_regional_relation'])]}


def main():
    receipt_path=Path(__file__).parent/'DATA-CHANGE-RECEIPT.json'
    if receipt_path.exists() and (ASSETS/'photo_prompt_neutral_expression_extension.json').exists():
        receipt=read(receipt_path)
        live_registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        profiles={p['id']:p for p in live_registry['profiles']}
        live=pg.load_json(ASSETS/'photo_prompt_tags.json')
        entries={(slot,e['id']):e for slot,rows in live['slots'].items() for e in rows}
        for file in receipt['existing_profile_updates']:
            for update in file['profiles']:
                if not set(update['added_paraphrases'])<=set(profiles[update['id']]['semantics']['paraphrase_examples']):raise ValueError('recorded profile additions missing')
        for update in receipt['existing_candidate_updates']:
            if not set(update['added_paraphrases'])<=set(entries[(update['slot'],update['id'])].get('paraphrases',[])):raise ValueError('recorded candidate additions missing')
        print('Recorded alternatives are present; verified without rewriting sources or the original receipt.')
        return
    rows={row.split('|')[0]:row.split('|')[1:] for row in TABLE.strip().splitlines()}
    owners={}; changed=[]
    for path in [ASSETS/'photo_prompt_visual_obligations.json',*[ASSETS/name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]]:
        value=read(path); additions=[]
        for item in value['profiles']:
            if item['id'] not in rows:continue
            before=copy.deepcopy(item); target=item['semantics'].setdefault('paraphrase_examples',[])
            added=[text for text in rows[item['id']] if text not in target];target.extend(added)
            owners[item['id']]=str(path.relative_to(ROOT))
            if added:additions.append({'id':item['id'],'added_paraphrases':added,'preserved_activation_and_required_contract':all(before[k]==item[k] for k in before if k!='semantics')})
        if additions:write(path,value);changed.append({'path':str(path.relative_to(ROOT)),'profiles':additions})
    missing=set(rows)-set(owners)
    if missing:raise ValueError(f'unknown owner IDs: {sorted(missing)}')
    data=pg.load_json(ASSETS/'photo_prompt_tags.json'); entry_map={e['id']:(s,e) for s,entries in data['slots'].items() for e in entries}
    extensions={}; extended=[]
    # Body candidate IDs may reuse an existing owner under a different name;
    # only actual equivalent IDs are exported here.
    for item_id,texts in {**rows,**CANDIDATE_ONLY}.items():
        candidate_id={'pfe_cleavage':'pfe_cleavage_candidate','pfe_lateral_chest':'pfe_lateral_chest_candidate','pfe_lower_chest':'pfe_lower_chest_candidate'}.get(item_id,item_id)
        if candidate_id not in entry_map:continue
        slot,entry=entry_map[candidate_id]
        available=[text for text in texts if text not in entry.get('paraphrases',[])]
        if available:
            extensions.setdefault(slot,{})[candidate_id]={'paraphrases':available}
            extended.append({'slot':slot,'id':candidate_id,'added_paraphrases':available,'label_effects_and_property_locks_preserved':True})
    new_profiles=[
        profile('ne_regional_soft_volume',['adult regional rounded soft volume','성인 특정 부위의 둥근 살집 윤곽'],['a named adult body region belongs to the same declared subject','rounded outward volume is visible in that named region','the regional outline joins its neighboring contour continuously'],'같은 성인의 지정한 몸 부위에 둥근 살집이 있고 인접 윤곽과 연속되는 형태','Rounded fleshy volume of a named adult body region belongs to the same subject and continues into the neighboring regional contour.'),
        profile('ne_regional_contour_transition',['adult regional convex-concave contour transition','성인 지정 몸통 구간의 안팎 곡선 연결'],['the named torso segment belongs to the same adult subject','an inward contour and an outward contour are both visible within that segment','the two curves join continuously along the same regional outline'],'같은 성인 몸통의 지정 구간에서 들어간 선과 나온 선이 하나의 연속 윤곽으로 이어지는 형태','A named segment of the same adult torso has both inward and outward curves joined continuously along its regional outline.'),
        profile('ne_current_lip_protrusion',['current forward lip pout','현재 입술을 앞으로 내민 표정'],['the upper and lower lips of the same declared face project forward in a rounded contour','the mouth corners of that same face gather toward the center'],'같은 얼굴의 입술이 현재 앞으로 둥글게 나오고 입 양끝이 중앙 쪽으로 모이는 표정','The same face currently has rounded forward-projecting lips with its mouth corners gathered toward the center.',expression=True),
    ]
    new_profiles[0]['semantics']['paraphrase_examples'] += ['지정된 아래배나 위팔의 국소 살집과 주변 윤곽이 같은 성인에게 연결된 형태','a plump named adult region with a rounded local volume and connected adjoining outline','a fleshy upper-arm region has rounded volume continuous with its connected arm contour']
    new_profiles[1]['semantics']['paraphrase_examples'] += ['지정한 옆몸통 구간에서 오목함과 볼록함이 연속되는 국소 곡선','a curvaceous regional torso outline joins an inward curve and an outward curve within the same stated segment']
    new_profiles[2]['semantics']['paraphrase_examples'] += ['pouty lips in the current-expression sense project forward while the mouth corners gather inward','a small forward pucker is visible on the same face with gathered mouth corners']
    visual={'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':new_profiles}
    write(ASSETS/'photo_prompt_visual_obligations_neutral_expression.json',visual)
    ordinary=[]
    for p in new_profiles[:2]:
        effects=p['concept_candidate']; ordinary.append({'id':p['id'],'ko':p['semantics']['paraphrase_examples'][0],'en':p['semantics']['definition'],'weight':0.5,'tags':['human','adult','regional_contour'],'for_any':['human'],'paraphrases':p['semantics']['paraphrase_examples'],'keywords':p['semantics']['visual_components'],'embedding_text':' '.join(p['semantics']['paraphrase_examples']),'concept_units':p['semantics']['visual_components'],'relations':[{'id':'named_region_owner','type':'has_visible_property','subject':'main_subject','object':p['semantics']['definition']}],'affected_dimensions':effects['affected_dimensions'],'affected_properties':effects['affected_properties'],'core_assertion_discovery':True})
    for slot,entry_id,context in [
        ('gaze_engagement','pv_side_eye',{'id':'ne_lateral_gaze_scope','application_conditions':['Preserve a declared actor, face orientation and lateral gaze target.'],'limits':['A lateral eye position alone does not prove suspicion, scorn, desire or personality.'],'status':'current_gaze_not_inner_state'}),
        ('expression','ae_pucker',{'id':'ne_pout_structure_action_split','application_conditions':['Use only the current-expression sense when the forward lip contour and gathered corners are intended.'],'limits':['Pouty as static full-lip appraisal uses lip structure instead; lip shape does not establish sulking or invitation.'],'status':'request_context_resolves_polysemy'}),
        ('skin_finish','bm_skin_relief_texture',{'id':'ne_smooth_supple_surface_scope','application_conditions':['A named current skin region; preserve pores, surface relief and independent finish.'],'limits':['Smooth does not establish suppleness, elasticity, health, retouching history or material identity.','A single frame can show a bend or fold but cannot prove rebound or temporal elasticity.'],'status':'current_observable_surface_only'}),
    ]:
        extensions.setdefault(slot,{}).setdefault(entry_id,{}).setdefault('contexts',[]).append(context)
    candidate={'schema_version':'photo-prompt-research-extension/v1','slots':{'silhouette_proportion':ordinary},'existing_slot_context_extensions':extensions}
    write(ASSETS/'photo_prompt_neutral_expression_extension.json',candidate)
    base=read(ASSETS/'photo_prompt_tags.json'); required=base['candidate_semantic_policy']['required_extensions']; name='photo_prompt_neutral_expression_extension.json'
    if name not in required:required.append(name);write(ASSETS/'photo_prompt_tags.json',base)
    report={'existing_profile_count':len(rows),'added_existing_profile_paraphrases':sum(len(x['added_paraphrases']) for file in changed for x in file['profiles']),'new_profile_ids':[p['id'] for p in new_profiles],'new_ordinary_candidate_ids':[e['id'] for e in ordinary],'existing_candidate_count':len(extended),'added_candidate_paraphrases':sum(len(x['added_paraphrases']) for x in extended),'new_exact_terms':{p['id']:p['activation']['exact_terms'] for p in new_profiles},'existing_profile_updates':changed,'existing_candidate_updates':extended,'same_scope_positive_language_only':True,'broad_lexemes_not_exact_promoted':True,'contextual_limits_excluded_from_positive_projection':True}
    write(Path(__file__).parent/'DATA-CHANGE-RECEIPT.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('existing_profile_updates','existing_candidate_updates')},ensure_ascii=False))


if __name__=='__main__':main()
