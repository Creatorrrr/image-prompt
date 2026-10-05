"""Add reviewed equivalent descriptions while preserving source identities and duties.

This maintenance script is research evidence, never a live pre-core input.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent / "vocaloid-appearance-research-20261004"

# Each pair describes exactly one existing component, including its original
# cardinality, carrier, attachment, and selected subtype. These are semantic
# examples and evidence alternatives, not newly promoted exact activators.
ALTERNATIVES = {
    "sca_h01": [
        ("one stray crown lock stands above the surrounding hairstyle", "정수리의 모발 다발 하나가 주변 머리 윤곽 위로 솟아 있다"),
        ("the upright lock grows continuously out of the same crown hair", "솟은 다발의 밑동이 같은 정수리 모발에 연속해서 이어진다"),
    ],
    "sca_h02": [
        ("a pair of fine crown locks rises from two distinct hair roots", "가는 정수리 다발 두 개가 서로 다른 모발 기점에서 올라온다"),
        ("both projections consist of continuous strands from that hairstyle", "두 돌출부 모두 같은 머리에서 이어지는 실제 모발 가닥으로 이루어진다"),
    ],
    "sca_h05": [
        ("a coiled hair column on either side descends through repeated spiral turns", "머리 양쪽에 있는 모발 기둥이 반복되는 나선 회전으로 내려온다"),
        ("both descending coils become progressively narrower at their ends", "아래로 이어지는 두 나선 다발이 각각 끝으로 갈수록 좁아진다"),
    ],
    "sca_h06": [
        ("one hair bundle gathered at the rear winds downward as a single spiral", "뒤에서 모은 모발 다발 하나가 단일 나선으로 감기며 내려온다"),
        ("that spiral retains an uninterrupted connection to its one rear gathering point", "그 나선이 하나의 뒤쪽 묶임점에 끊기지 않고 이어진다"),
    ],
    "sca_h09": [
        ("a single scalp gathering point sits on one selected side of the head", "머리의 지정한 한쪽 두피에 묶임점 하나가 놓인다"),
        ("one hanging hair bundle runs directly out of that same side gathering", "머리 다발 하나가 같은 옆쪽 묶임점에서 곧바로 이어져 내려온다"),
    ],
    "sca_h10": [
        ("crossing sections of hair make one uninterrupted plait", "교차하는 모발 구간들이 하나의 끊기지 않는 땋은 다발을 만든다"),
        ("the continuous plait curves around the crown of the same head", "연속된 땋은 다발이 같은 머리의 정수리 둘레를 휘어 돌아간다"),
    ],
    "sca_h13": [
        ("a front hair section overlaps the area of just one eye", "앞머리 구간이 한쪽 눈 영역 위에 겹쳐 놓인다"),
        ("the opposite eye area stays exposed on that same face", "같은 얼굴의 반대쪽 눈 영역은 드러난 채 남는다"),
    ],
    "sca_h19": [
        ("one declared hair color fills the left side and another fills the right side", "지정한 한 모발색이 왼쪽을 채우고 다른 모발색이 오른쪽을 채운다"),
        ("the two colors meet at a stable division in the hair itself", "두 색이 모발 자체에 고정된 구획 경계에서 만난다"),
    ],
    "sca_h20": [
        ("the exterior hair sheet keeps its declared outer color", "겉으로 놓인 모발층이 지정한 바깥 색을 유지한다"),
        ("an opening in that sheet reveals an underlying hair layer of another color", "겉 모발층의 열린 틈으로 다른 색의 아래 모발층이 드러난다"),
    ],
    "sca_h21": [
        ("hair color varies from the roots toward the tips along the same strands", "같은 모발 가닥을 따라 뿌리에서 끝 방향으로 색이 달라진다"),
        ("a sequence of intermediate tones connects the root color to the tip color", "중간 색조들이 뿌리 색에서 끝 색까지 점진적으로 이어진다"),
    ],
    "sca_g01": [
        ("the arm sleeve has its own upper rim apart from the torso garment", "팔 소매가 몸통 옷과 떨어진 독립적인 윗단을 가진다"),
        ("a readable interval lies between that sleeve rim and the bodice armhole", "그 소매 윗단과 몸판 암홀 사이에 읽히는 간격이 놓인다"),
    ],
    "sca_x01": [
        ("the bases of the ear-shaped accessories join an exposed headband", "귀 모양 장식들의 밑동이 드러난 머리띠에 이어진다"),
        ("the supporting band lies visibly over the wearer's hair and head", "지지하는 띠가 착용자의 모발과 머리 위에 보이게 놓인다"),
    ],
    "sca_x02": [
        ("the horn-shaped fittings connect directly to a wearable helmet surface", "뿔 모양 부속들이 착용한 헬멧 표면에 직접 연결된다"),
        ("the helmet retains its own outer shell around the wearer's head", "헬멧이 착용자의 머리 둘레에서 자체 외피를 유지한다"),
    ],
    "sca_x12": [
        ("distinct cloth panels share a visible sewn meeting edge in the garment", "서로 다른 천 패널들이 옷에서 보이는 봉제 접합 경계를 공유한다"),
        ("actual joining thread follows that very meeting edge between the panels", "실제 연결 실이 그 천 패널 사이의 같은 접합 경계를 따라간다"),
    ],
    "sca_x15": [
        ("a group of parallel line marks lies inside a single bounded cloth panel", "평행한 선 표시들이 경계가 정해진 하나의 천 패널 안에 놓인다"),
        ("all those line marks remain a flat pattern on the same fabric face", "그 선 표시들 모두가 같은 천 면의 평면 무늬로 남는다"),
    ],
    "sca_x16": [
        ("one headphone structure links the two ear-covering cups", "하나의 헤드폰 구조가 귀를 덮는 두 컵을 연결한다"),
        ("the projecting fittings have continuous attachments to those same earcups", "돌출 부속들이 같은 이어컵들에 연속해서 부착된다"),
    ],
    "clothing_ct004_v2": [("a tubular bodice has one continuous top rim below the shoulders and an uncovered neck support region", "관 모양 몸판의 윗단이 어깨 아래에서 연속되고 목 지지 부위는 드러나 있다")],
    "clothing_ct018_v2": [("successive horizontal skirt sections gather into their separate joining seams", "연속된 수평 치마 단들이 각각의 별도 접합선에 주름져 모인다")],
    "clothing_ct025_v1": [("narrow hanging straps connect the waist support belt directly to the stocking upper edges", "가는 아래 방향 끈들이 허리 지지 벨트에서 양말 윗단으로 직접 이어진다")],
    "clothing_ct031_v1": [("curving stitched panel joins run between the bodice front and its side-front pieces", "몸판의 앞 조각과 옆앞 조각 사이에 곡선 형태의 봉제 접합선들이 이어진다")],
    "clothing_ct038_v1": [("the bodice support strap travels around the nape behind the neck", "몸판을 지지하는 끈이 목 뒤의 목덜미를 돌아간다")],
    "clothing_ct038_v2": [("both shoulder tops lie above a lowered neckline whose sleeves stay joined to the bodice", "양 어깨 윗면이 낮아진 목선 위에 놓이고 소매들은 몸판에 이어져 있다")],
    "clothing_ct046_v2": [("a short rounded sleeve swells between its gathered shoulder join and gathered lower rim", "짧고 둥근 소매가 주름진 어깨 접합부와 주름진 아랫단 사이에서 부푼다")],
    "clothing_ct047_v2": [("the same sleeve broadens down the arm into a wide open cuff", "같은 소매가 팔 아래 방향으로 넓어져 폭이 큰 열린 커프로 끝난다")],
    "clothing_ct061_v1": [("a free skirt bottom opens upward along a side edge into two separate finished margins", "치마의 자유 밑단에서 옆선을 따라 위로 열린 두 개의 마감 가장자리가 이어진다")],
    "clothing_ct062_v1": [("the rear edge of the dress continues into fabric lying beyond it on the floor", "드레스의 뒤 밑단이 그 너머 바닥에 놓인 천으로 계속 이어진다")],
    "clothing_ct062_v2": [("one shirt has a rear bottom edge extending lower than its front bottom edge", "한 셔츠의 뒤쪽 밑단이 앞쪽 밑단보다 아래로 더 길게 이어진다")],
    "clothing_ct063_v1": [("repeated narrow fabric folds turn toward the same side in a parallel sequence", "반복되는 좁은 천 접힘들이 평행한 배열로 같은 쪽을 향해 접힌다")],
    "clothing_ct063_v2": [("two opposing fabric folds approach one another and meet at an inward box-pleat center", "서로 반대 방향인 천 접힘 두 개가 다가와 안쪽 박스 주름의 중심에서 만난다")],
    "clothing_ct065_v1": [("a narrow gathered trim joins the sleeve border and spreads into a waved free edge", "좁고 주름진 장식 띠가 소매 경계에 이어져 물결 모양의 자유 끝으로 퍼진다")],
    "clothing_ct065_v2": [("a circularly flared trim joins the skirt's bottom edge and falls in broad waves", "원형으로 퍼진 장식 천이 치마 아랫단에 이어져 넓은 물결로 내려온다")],
    "clothing_ct106_v1": [("a hand-covering glove ends in openings through which that hand's fingertips emerge", "손을 덮는 장갑이 열린 끝으로 끝나고 같은 손의 손가락 끝들이 그 밖으로 나온다")],
    "clothing_ct107_v1": [("each separate stocking continues up the leg to an upper edge on the thigh", "각각의 별도 스타킹이 다리를 따라 허벅지에 놓인 윗단까지 올라간다")],
    "clothing_ct107_v2": [("a calf-covering textile tube has an open lower rim above the exposed foot", "종아리를 덮는 천 원통이 드러난 발 위에서 열린 아랫단을 가진다")],
    "clothing_ct121_v1": [("a red ornament presents several flat faces bounded by sharp intersecting edges", "붉은 장식물이 날카롭게 만나는 모서리로 둘러싸인 여러 평평한 면을 드러낸다")],
    "clothing_ct139_v2": [("a separate obi band wraps around the outside of the kimono's waist", "별도의 오비 띠가 기모노 허리의 바깥을 둘러 감싼다")],
    "clothing_ct090_v1": [("discrete lace motifs connect through thread bars spanning the open spaces between them", "서로 구분되는 레이스 도상들이 그 사이의 열린 공간을 가로지르는 실 막대로 이어진다")],
    "clothing_ct090_v2": [("fine garment threads enclose a regular array of genuinely open mesh cells", "옷의 가는 실들이 실제로 열린 망사 셀들을 일정한 배열로 둘러싼다")],
    "clothing_ct097_v1": [("stitched courses on the textile surround individual softly raised quilted areas", "천 표면의 봉제 경로들이 각각의 부드럽게 솟은 퀼팅 영역을 둘러싼다")],
    "costume_ccx_cc08_02": [("independent sleeve cuffs wrap the arms while a visible interval separates them from the bodice", "독립된 소매 커프들이 팔을 감싸고 몸판과의 사이에는 보이는 간격이 남는다")],
    "costume_ccx_cc13_01": [("dark pliable cloth remains readable at the joints between separate hard armor pieces", "분리된 단단한 갑주 조각 사이의 관절에서 어두운 유연한 천이 읽히게 남는다")],
    "costume_ccx_cc13_02": [("the overlapping armor margins end around the bending joint with an articulation interval", "겹친 갑주 가장자리들이 굽혀진 관절 주변에서 관절 움직임을 위한 간격을 두고 끝난다")],
    "costume_ccx_cc17_01": [("two imitation-fur ear pieces join the same visible hair band at their lower roots", "모조 모피 귀 조각 두 개가 아래 밑동에서 같은 보이는 머리띠에 이어진다")],
    "costume_ccx_cc17_02": [("each costume ear outline encloses a contrasting inner panel separate from the wig below", "각 코스튬 귀 외곽이 아래 가발과 구분되는 대비된 안쪽 패널을 둘러싼다")],
    "costume_ccx_cc24_02": [("an independent broad obi-like cloth band surrounds the waist over the costume", "독립적인 넓은 오비형 천 띠가 코스튬 바깥에서 허리를 둘러싼다")],
    "costume_ccx_cc27_02": [("the selected short tutu extends radially out from its attachment around the hips", "선택한 짧은 튀튀가 골반 둘레의 부착부에서 바깥 방향으로 퍼져 나간다")],
    "costume_ccx_cc39_02": [("a sequence of folded skirt ridges runs from the waist toward the moving lower edge", "접힌 치마 능선들이 허리에서 움직이는 아랫단 방향으로 반복해서 이어진다")],
    "y2kr_hair_gems": [("individual angular-faced decorations join visible points along the hairstyle", "각진 면을 가진 개별 장식들이 모발 구조를 따라 보이는 지점들에 부착된다")],
    "y2kr_rhinestones": [("each small faceted decoration keeps a separate outline around its compact reflected highlight", "각각의 작은 다면 장식이 조밀한 반사 하이라이트 둘레에 별도 외곽을 유지한다")],
    "ca_compact_bob": [
        ("a short compact hair silhouette reaches its lower limit near the jaw", "짧고 조밀한 모발 윤곽이 턱 부근에서 아래쪽 끝에 이른다"),
        ("the tips join into a readable short outline around the same face", "모발 끝들이 같은 얼굴 둘레의 읽히는 짧은 외곽으로 이어진다"),
    ],
    "ca_hanging_hair_braid": [
        ("one hanging lock shows an alternating sequence of interlaced hair sections", "늘어진 모발 다발 하나에 엇갈려 교차하는 모발 구간들이 반복된다"),
        ("the interlacing stays continuous down that same suspended lock", "그 교차 구조가 같은 늘어진 다발을 따라 연속해서 내려간다"),
    ],
    "ca_cap_projections": [
        ("a pair of pointed fittings projects upward from a cap crown", "뾰족한 부속 한 쌍이 모자 몸체에서 위로 돌출된다"),
        ("both fittings have roots connected to that single cap shell", "두 부속 모두가 같은 하나의 모자 외피에 연결된 밑동을 가진다"),
    ],
    "ca_surface_line_motif": [
        ("a drawn contour symbol occupies the selected visible skin area", "그려진 윤곽 도상이 선택한 보이는 피부 영역에 놓인다"),
        ("the symbol's continuous lines follow that same body's skin plane", "그 도상의 연속된 선들이 같은 신체의 피부 면을 따라간다"),
    ],
    "ca_bounded_body_patches": [
        ("distinct contrasting color areas lie in the selected body surface zones", "구분되는 대비 색 영역들이 선택한 신체 표면 구역들에 놓인다"),
        ("each colored area ends at its own readable surface boundary", "각 색 영역이 자체의 읽히는 표면 경계에서 끝난다"),
    ],
    "ca_offset_head_mask": [
        ("an independent mask is positioned at the temple or upper side of the head", "독립된 가면이 관자놀이 또는 머리 윗쪽 옆면에 놓인다"),
        ("the wearer's eye areas stay exposed beyond the offset mask", "착용자의 눈 영역들이 옆으로 비켜 놓인 가면 밖에 드러나 있다"),
    ],
}

# Existing legacy profiles keep all their original component duties. These
# complete descriptions help retrieval without editing their compiled gates.
LEGACY_ALTERNATIVES = {
    "bilateral_twin_tail_gather": [
        "Hair on each side converges into its own visible scalp tie; two separate tails continue from those ties along distinct left and right paths.",
        "좌우 두피 모발이 각각의 보이는 묶임점으로 모이고 두 별도 꼬리가 그 기점에서 좌우의 다른 경로로 이어진다.",
    ],
    "hime_cut_structural": [
        "Long hair remains at the back while two blunt face-side panels stop near the cheek or jaw, creating a distinct cut-length step on each side.",
        "뒤의 긴 모발은 유지되고 얼굴 양옆의 반듯한 패널은 볼이나 턱 부근에서 끝나 양쪽에 분명한 절단 길이 차이를 만든다.",
    ],
    "cold_shoulder_cutout_topology": [
        "Each shoulder lies inside a finished opening in the top; continuous fabric connects the upper bodice around the opening to the sleeve below.",
        "각 어깨가 상의의 마감된 개방부 안에 놓이고 연속된 천이 개방부 둘레의 위 몸판에서 아래 소매로 이어진다.",
    ],
    "bm_stature_scale": [
        "The complete adult head-to-foot height is comparatively short beside an explicit reference standing at the same depth.",
        "성인의 머리에서 발까지 완전한 높이가 같은 깊이에 놓인 명시적 기준물에 비해 작게 보인다.",
    ],
    "bm_compact_frame": [
        "The adult torso has compact transverse extent and the limb segments have a compact frame scale, with stature stated independently.",
        "성인 몸통의 가로 범위와 사지 구간의 골격 규모가 조밀하게 보이고 전체 키는 별도로 지정된다.",
    ],
    "bm_torso_limb_ratio": [
        "The adult torso and leg lengths are bounded by stated anatomical landmarks and compared in one pose at a common scale.",
        "성인 몸통과 다리 길이가 지정한 해부학적 기준점들로 구획되어 같은 자세와 공통 축척에서 비교된다.",
    ],
    "bm_head_body_ratio": [
        "Declared head endpoints and full adult body endpoints establish the head-to-body length comparison at a common scale.",
        "지정한 머리 양 끝점과 성인 전신의 양 끝점이 같은 축척에서 머리와 몸 길이의 비교를 성립시킨다.",
    ],
    "bm_waist_width_depth": [
        "The adult waist's side-to-side extent and front-to-back extent are evaluated separately against readable rib and pelvis references.",
        "성인 허리의 좌우 범위와 앞뒤 범위가 읽히는 갈비와 골반 기준에 대해 각각 따로 비교된다.",
    ],
    "hourglass_silhouette_relation": [
        "An adult torso and hip silhouette widens above and below a narrower waist through continuous bilateral contours, with pose and clothing shaping distinguished.",
        "성인 몸통과 골반 윤곽이 좁은 허리 위아래에서 연속된 양측 외곽으로 넓어지고 자세와 의복에 의한 변화는 구분된다.",
    ],
    "rectangle_silhouette_relation": [
        "The connected adult upper torso, waist and hip contours show relatively little width change from one view, with a shallow waist indentation.",
        "같은 시점에서 이어진 성인 상체와 허리와 골반 외곽은 폭 변화가 비교적 작고 허리의 안쪽 굴곡이 얕다.",
    ],
}

# Source-supported new relations are authored separately from nearby profiles.
# K17 is merged into the existing skin-surface profiles instead of duplicating
# them. Unresolved source/prop/age/medium leads remain in the disposition ledger.
NEW_SPECS = [
    ("K02", "vr_high_twin_tail_roots", "sca_high_twin_tail_roots", "subculture_appearance"),
    ("K06", "vr_outward_hair_tips", "sca_outward_hair_tips", "subculture_appearance"),
    ("K09", "vr_short_rear_long_sidelocks", "sca_short_rear_long_sidelocks", "subculture_appearance"),
    ("K15", "vr_facial_surface_dot_scatter", "sca_facial_surface_dot_scatter", "subculture_appearance"),
    ("K16", "vr_local_dark_lip_contrast", "sca_local_dark_lip_contrast", "subculture_appearance"),
    ("K26", "vr_uncovered_foot", "accessory_uncovered_foot", "accessory_structure"),
    ("K34", "vr_crop_top_waist_hem", "clothing_crop_top_waist_hem", "clothing_structure"),
    ("K35", "vr_abdominal_bounded_opening", "clothing_abdominal_bounded_opening", "clothing_structure"),
    ("K44", "vr_attached_rear_costume_panel", "costume_attached_rear_panel", "costume_cosplay"),
    ("K51", "vr_earpiece_mouth_boom", "accessory_earpiece_mouth_boom", "accessory_structure"),
    ("K52", "vr_rigid_hair_tie_hardware", "sca_rigid_hair_tie_hardware", "subculture_appearance"),
    ("K53", "vr_flat_equalizer_bars", "sca_flat_equalizer_bars", "subculture_appearance"),
    ("K54", "vr_flat_keyboard_motif", "sca_flat_keyboard_motif", "subculture_appearance"),
    ("K55", "vr_flat_control_panel_motif", "sca_flat_control_panel_motif", "subculture_appearance"),
    ("K56", "vr_arm_circular_speaker_gear", "accessory_arm_circular_speaker_gear", "accessory_structure"),
    ("K61", "vr_external_membrane_wings", "costume_external_membrane_wings", "costume_cosplay"),
    ("K62", "vr_external_thin_wing_plates", "costume_external_thin_wing_plates", "costume_cosplay"),
    ("K64", "vr_cap_face_motif", "accessory_cap_face_motif", "accessory_structure"),
    ("K68", "vr_cap_cross_glyph", "accessory_cap_cross_glyph", "accessory_structure"),
]

# Unlike the research prototype, each new component has an independently
# written EN/KR equivalent for retrieval and literal evidence.
NEW_ALTERNATIVES = {
    "K02": [("both scalp gathering sites sit higher than the tops of their respective ears", "양쪽 두피 묶임 기점이 각각의 귀 윗끝보다 위에 놓인다"), ("a separate hair tail runs downward from each elevated gathering site", "각 높은 묶임 기점에서 별도의 모발 꼬리가 아래로 이어진다")],
    "K06": [("the ends of the hair curve laterally away from the neck", "모발 끝들이 목에서 옆의 바깥 방향으로 휘어진다"), ("the flipped ends remain uninterrupted extensions of their own hair bundles", "바깥으로 꺾인 끝들이 각 모발 다발에서 끊기지 않고 이어진다")],
    "K09": [("the rear hair perimeter stops high at the nape", "뒤 모발의 외곽 끝이 목덜미 위쪽에서 멈춘다"), ("two elongated locks beside the face alone descend toward the chest", "얼굴 옆의 긴 모발 두 다발만 가슴 방향으로 내려온다"), ("one hairstyle combines that short back with the two longer front-side lengths", "하나의 머리 구조가 짧은 뒤 길이와 긴 얼굴 옆 길이 두 개를 함께 가진다")],
    "K15": [("a scatter of tiny marks occupies the selected nose and cheek skin", "작은 표시들의 흩어진 배열이 지정한 코와 볼 피부에 놓인다"), ("the dots stay on that facial surface with uneven spacing or dot sizes", "점들이 불균일한 간격이나 크기로 같은 얼굴 표면에 남는다")],
    "K16": [("the selected lips have lower value than the neighboring skin", "선택한 입술의 명도가 주변 피부보다 낮다"), ("the local dark tone ends at the visible lip outline", "국소적인 짙은 색조가 보이는 입술 외곽에서 끝난다")],
    "K26": [("the top of the selected bare foot and its toes are fully uncovered", "지정한 맨발의 발등과 발가락이 완전히 드러나 있다"), ("the uncovered foot connects directly into its own ankle", "드러난 발이 자신의 발목으로 직접 이어진다")],
    "K34": [("the upper garment bottom edge stops higher than the chosen waist landmark", "윗옷의 아랫단이 선택한 허리 기준점보다 위에서 끝난다"), ("that top edge remains distinct from the lower garment's waistband", "그 상의 끝선이 하의의 허리 경계와 구분되어 남는다")],
    "K35": [("the clothing has a bounded aperture over the selected abdominal region", "의복이 지정한 복부 영역 위에서 경계가 있는 개방부를 가진다"), ("continuous finished cloth margins and fabric bridges surround that aperture", "연속된 마감 천 가장자리와 천 연결 구간들이 그 개방부를 둘러싼다")],
    "K44": [("one costume combines a shorter frontal section with a longer back section", "하나의 코스튬이 짧은 앞 구간과 긴 뒤 구간을 함께 가진다"), ("the long back panel has an upper connection to that costume's waist or torso panel", "긴 뒤 패널의 윗부분이 같은 코스튬의 허리 또는 몸통 패널에 연결된다")],
    "K51": [("a slim mic arm runs continuously out of the ear-mounted fitting", "귀에 장착한 부속에서 가는 마이크 암이 연속해서 이어진다"), ("its outer end reaches the area beside the wearer's lips", "그 바깥 끝이 착용자의 입술 옆 영역에 이른다"), ("the ear fitting and lip-side microphone end serve one and the same wearer", "귀 부속과 입술 옆 마이크 끝이 하나의 같은 착용자에게 속한다")],
    "K52": [("the hair fitting has a solid plate or ring outline with a distinct edge", "머리 부속이 구분되는 가장자리를 가진 단단한 판 또는 고리 외곽을 이룬다"), ("that fitting is fastened beside the visible scalp gathering point", "그 부속이 보이는 두피 묶임점 옆에 고정되어 있다")],
    "K53": [("evenly spaced upright bars form a parallel row on the clothing", "일정한 간격의 수직 막대들이 의복 위에 평행한 열을 이룬다"), ("their unequal top heights remain part of the same flat cloth graphic", "서로 다른 윗높이들이 같은 평면 천 무늬에 속한다"), ("a single continuous garment area carries the entire differing-height bar row", "하나의 연속된 의복 영역이 높이가 다른 전체 막대 열을 담는다")],
    "K54": [("elongated pale rectangles form the repeating base of a textile keyboard pattern", "긴 밝은 직사각형들이 천의 건반 무늬에서 반복되는 기본 열을 이룬다"), ("smaller dark rectangles interrupt one side of that row at staggered positions", "작고 어두운 직사각형들이 그 열 한쪽의 어긋난 위치에 놓인다"), ("the complete key-shaped design lies flat within one clothing panel", "전체 건반 모양 무늬가 하나의 의복 패널 안에 평면으로 놓인다")],
    "K55": [("compact outlined boxes contain line and dot symbols or digit-like marks", "작고 테두리가 있는 상자들이 선과 점 도상 또는 숫자형 표시를 담는다"), ("the display-like graphics remain level with the sleeve or skirt fabric", "표시창 같은 무늬들이 소매나 치마 천 면과 같은 평면에 남는다")],
    "K56": [("the arm-mounted circular fitting shows nested concentric surfaces inside its outer rim", "팔에 장착한 원형 부속이 바깥 테두리 안에 겹친 동심원 면들을 보인다"), ("a visible arm support carries a fitting whose overall span exceeds the hand", "보이는 팔 지지부가 손보다 전체 폭이 큰 부속을 지지한다")],
    "K61": [("continuous thin sheets fill the intervals between the costume wing struts", "연속된 얇은 막이 코스튬 날개 지지골 사이의 구간을 채운다"), ("inward curved scallops connect successive outer wing points", "안으로 휘어진 오목한 가장자리가 연속된 바깥 날개 끝점들을 연결한다"), ("the wing root attaches to an external support over the costume back", "날개 밑동이 코스튬 등 바깥에 놓인 지지부에 부착된다")],
    "K62": [("distinct shallow wing panels sit outside and behind the costume wearer's back", "구분되는 얇은 날개 패널들이 코스튬 착용자의 등 밖과 뒤에 놓인다"), ("drawn line paths stay contained inside those wing panel edges", "그려진 선 경로들이 날개 패널 가장자리 안에 머문다"), ("the external wing panels have roots connected to a declared costume back fitting", "외부 날개 패널들의 밑동이 지정한 코스튬 등 부속에 이어진다")],
    "K64": [("the wearable cap retains a readable crown and rim above the hair", "착용한 모자가 모발 위에서 읽히는 몸체와 테두리를 유지한다"), ("the cap surface itself carries the selected eye or mouth shapes and selected fittings", "모자 표면 자체가 선택한 눈 또는 입 도상과 선택한 부속들을 담는다")],
    "K68": [("a distinct small head cap has its own visible perimeter", "머리 위의 별도 작은 모자가 자체의 보이는 외곽을 가진다"), ("the crossed-line emblem stays inside the front face of that cap", "교차된 선의 도상이 같은 모자의 앞면 안에 놓인다")],
}

EXTRA_UNITS = {
    "K09": ("the short rear hair and paired long face-side locks belong to the same hairstyle", "짧은 뒤머리와 두 긴 얼굴 옆 다발이 같은 모발 구조에 속한다"),
    "K51": ("the boom and mouth endpoint remain on the same wearer as the earpiece", "마이크 막대와 입 옆 끝점이 귀 장치를 쓴 같은 얼굴에 속한다"),
    "K53": ("all variable-height bars remain printed on one continuous garment panel", "높이가 다른 막대들이 같은 연속된 의복 패널에 인쇄되어 있다"),
    "K54": ("all key-shaped marks remain flat on the same textile panel", "모든 건반 모양 표시가 같은 천 패널에 평면으로 놓인다"),
    "K61": ("the external wing root joins a declared costume back support", "외부 날개 뿌리가 지정한 코스튬 등 지지부에 이어진다"),
    "K62": ("the external wing plate roots join a declared costume back fitting", "외부 날개 판의 밑동이 지정한 코스튬 등 부속에 이어진다"),
}

HELD = {
    "K04": "Rear tie point is not confirmed in the Len source; do not turn a suggested rear silhouette into gathering evidence.",
    "K10": "Existing crown and hanging braids are enriched independently; a secured folded loop still needs its own fastening evidence.",
    "K21": "Width-only slenderness is not equivalent to the existing long-and-slender build; do not add that broader profile as a synonym.",
    "K25": "Local skin/garment contrast needs an explicit complete two-carrier color effect; no ethnicity, health or default skin color is installed.",
    "K42": "The reviewed Macne package does not establish unequal lateral hems. Existing shirt high-low and floor-train variants remain distinct.",
    "K45": "The source does not establish the complete bib/strap/skirt route; trouser overalls and aprons stay separate.",
    "K58": "Independent ornament gap has unresolved prop effect scope; no floating mechanism is inferred.",
    "K63": "Canopy and cuff streamers have different owners; the proposed single-owner compound is not installed.",
    "K65": "The Oliver thumbnail supports a covered eye area but not repeated overlapping cloth turns; no injury or generic wrap is inferred.",
    "K70": "Independent plush object needs its own complete prop effect scope; human surface candidates cannot change the plush.",
    "K72": "The official 2015 accessory is a parasol. A pointed silhouette does not establish a spear; independent prop scope remains unresolved.",
}


def append_unique(container: list, values: list) -> int:
    before = len(container)
    for value in values:
        if value not in container:
            container.append(copy.deepcopy(value))
    return len(container) - before


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    paths = sorted(set(ASSETS.glob("photo_prompt*extension*.json")) | set(ASSETS.glob("photo_prompt_visual_obligations*.json")) | {ASSETS / "photo_prompt_tags.json"})
    docs = {p: read(p) for p in paths}
    originals = copy.deepcopy(docs)
    profiles = {p["id"]: (path, p) for path, doc in docs.items() for p in doc.get("profiles", [])}
    entries = {e["id"]: (path, slot, e) for path, doc in docs.items() for slot, rows in doc.get("slots", {}).items() for e in rows}
    cards = {c["id"]: c for c in read(RESEARCH / "KEYWORD-RESEARCH.json")["cards"]}
    log = {"schema_version": "vocaloid-appearance-integration/v1", "existing_profiles": [], "new_profiles": [], "candidate_changes": [], "card_dispositions": [], "source_reviews": [], "source_files": []}

    def existing_entry(profile_id: str):
        candidate_id = profile_id
        if profile_id.startswith("clothing_ct"):
            candidate_id = profile_id.replace("clothing_", "clt_", 1)
        elif profile_id.startswith("costume_ccx_"):
            candidate_id = profile_id.removeprefix("costume_")
        return entries.get(candidate_id)

    def enrich_candidate(profile_id: str, phrases: list[str]) -> None:
        found = existing_entry(profile_id)
        if not found:
            return
        path, slot, entry = found
        n = append_unique(entry.setdefault("paraphrases", []), phrases)
        append_unique(entry.setdefault("keywords", []), phrases)
        positive = entry.get("embedding_text", entry.get("en", ""))
        for phrase in phrases:
            if phrase not in positive:
                positive += " | " + phrase
        entry["embedding_text"] = positive
        if n:
            log["candidate_changes"].append({"id": entry["id"], "profile_id": profile_id, "slot": slot, "file": path.name, "new": False, "added_paraphrases": phrases})

    for profile_id, alternatives in ALTERNATIVES.items():
        path, profile = profiles[profile_id]
        components = profile["authored_components"]["components"]
        assert len(components) == len(alternatives), (profile_id, len(components), len(alternatives))
        full = ["; ".join(pair[i] for pair in alternatives) for i in [0, 1]]
        for component, pair in zip(components, alternatives):
            append_unique(component["match_terms"], list(pair))
            append_unique(component.setdefault("evidence_terms", []), list(pair))
        n = append_unique(profile["semantics"].setdefault("paraphrase_examples", []), full)
        append_unique(profile["concept_candidate"].setdefault("concept_terms", []), full)
        if n:
            log["existing_profiles"].append({"id": profile_id, "file": path.name, "added_paraphrases": full, "component_alternatives": [list(p) for p in alternatives], "exact_activation_unchanged": True, "duties_unchanged": True})
        enrich_candidate(profile_id, full)

    for profile_id, phrases in LEGACY_ALTERNATIVES.items():
        path, profile = profiles[profile_id]
        n = append_unique(profile["semantics"].setdefault("paraphrase_examples", []), phrases)
        append_unique(profile["concept_candidate"].setdefault("concept_terms", []), phrases)
        if n:
            log["existing_profiles"].append({"id": profile_id, "file": path.name, "added_paraphrases": phrases, "exact_activation_unchanged": True, "duties_unchanged": True})
        enrich_candidate(profile_id, phrases)

    # Cheek location is a descriptive variant of existing surface markings.
    # Keep contour and filled-area alternatives separate instead of adding a
    # new profile whose disjunction would duplicate both stable identities.
    cheek = {
        "ca_surface_line_motif": ["a contour glyph drawn on the selected cheek remains a flat line mark on that same skin surface", "선택한 뺨에 그린 윤곽 도상이 같은 피부 표면의 평면 선 표시로 남는다"],
        "ca_bounded_body_patches": ["a bounded filled-color cheek mark stays inside its declared facial skin region", "경계가 있는 채워진 뺨 색 표시가 지정한 얼굴 피부 영역 안에 머문다"],
    }
    for profile_id, phrases in cheek.items():
        _, profile = profiles[profile_id]
        append_unique(profile["semantics"]["paraphrase_examples"], phrases)
        append_unique(profile["concept_candidate"]["concept_terms"], phrases)
        next(row for row in log["existing_profiles"] if row["id"] == profile_id)["added_paraphrases"].extend(phrases)

    # Character-appearance profiles currently have registry candidates but no
    # ordinary slot counterpart. Add only the six wearer-owned meanings used
    # here; never cast creature anatomy as a human costume effect.
    ca_slots = {"ca_compact_bob": "hair_style", "ca_hanging_hair_braid": "hair_style", "ca_cap_projections": "wearable_accessory", "ca_surface_line_motif": "body_marking", "ca_bounded_body_patches": "body_marking", "ca_offset_head_mask": "wearable_accessory"}
    for profile_id, slot in ca_slots.items():
        if profile_id in entries:
            continue
        profile = profiles[profile_id][1]
        phrases = list(profile["semantics"]["paraphrase_examples"])
        units = list(profile["semantics"]["visual_components"])
        en = phrases[0]
        ko = next(p for p in phrases if any("가" <= c <= "힣" for c in p))
        entry = {"id": profile_id, "ko": ko, "en": en, "weight": 0.5, "tags": ["human", "observable_relation"], "for_any": ["human"], "aliases": [], "paraphrases": phrases, "keywords": [*units, *phrases], "embedding_text": " | ".join([en, ko, *phrases]), "concept_units": units, "relations": [{"id": "declared_owner", "type": "declared_owner_scope", "subject": "the selected visible carrier", "object": "main_subject"}, {"id": "same_carrier", "type": "same_owner", "subject": units[0], "object": units[1]}], "affected_dimensions": copy.deepcopy(profile["concept_candidate"]["affected_dimensions"]), "affected_properties": copy.deepcopy(profile["concept_candidate"]["affected_properties"]), "core_assertion_discovery": True}
        path = ASSETS / "photo_prompt_subculture_appearance_extension.json"
        docs[path]["slots"].setdefault(slot, []).append(entry)
        entries[entry["id"]] = (path, slot, entry)
        log["candidate_changes"].append({"id": entry["id"], "profile_id": profile_id, "slot": slot, "file": path.name, "new": True, "added_paraphrases": phrases, "reason": "ordinary counterpart of the existing stable profile"})

    for key, candidate_id, profile_id, family in NEW_SPECS:
        assert profile_id not in profiles, profile_id
        assert candidate_id not in entries, candidate_id
        card = cards[key]
        units = [v["en"] for v in card["visible_components"]]
        korean = [v["ko"] for v in card["visible_components"]]
        if key == "K16":
            units[0] = "the selected lip region is darker than the adjacent facial skin"
            korean[0] = "선택한 입술 영역이 인접한 얼굴 피부보다 짙다"
        if key == "K52":
            units[0] = "a rigid hair-tie fitting has a distinct plate or ring perimeter"
            korean[0] = "단단한 머리 묶임 부속이 구분되는 판 또는 고리 외곽을 가진다"
        if key == "K62":
            units[1] = "line motifs remain inside the outlines of those thin wing plates"
            korean[1] = "선무늬가 얇은 날개 판의 외곽 안에 놓인다"
        if key in EXTRA_UNITS:
            e, k = EXTRA_UNITS[key]
            units.append(e)
            korean.append(k)
        alternatives = NEW_ALTERNATIVES[key]
        assert len(units) == len(alternatives), key
        full = ["; ".join(units), "; ".join(korean), "; ".join(pair[0] for pair in alternatives), "; ".join(pair[1] for pair in alternatives)]
        slot = card["proposed_slot"]
        effect = {k: card["proposed_effect"][k] for k in ["dimension", "target", "property"]}
        entry = {"id": candidate_id, "ko": full[1], "en": full[0], "weight": 0.5, "tags": ["human", "observable_relation"], "for_any": ["human"], "aliases": [], "paraphrases": full, "keywords": [*units, *korean, *full[2:]], "embedding_text": " | ".join(full), "concept_units": units, "relations": [{"id": "declared_owner", "type": "declared_owner_scope", "subject": card["owner"], "object": "main_subject"}, *copy.deepcopy(card["required_relations"])], "affected_dimensions": ["appearance"], "affected_properties": [effect], "core_assertion_discovery": True}
        if key in ["K53", "K54", "K55"]:
            # Graphic location/topology changes are independent of fabric or
            # hardware function; adopt only these complete appearance effects.
            entry["relations"].append({"id": "flat_carrier", "type": "printed_on", "subject": "all selected graphic marks", "object": "the same declared garment panel"})
        if key in ["K61", "K62"]:
            entry["relations"].append({"id": "external_costume_attachment", "type": "attached_to", "subject": "external wing root", "object": "declared costume back support"})
        carrier_terms = {
            "hair_style": ["hair", "hairstyle", "wig", "머리", "모발", "가발"],
            "body_marking": ["skin", "cheek", "nose", "face", "피부", "볼", "뺨", "코", "얼굴"],
            "lip_color_placement": ["lip", "lips", "mouth", "입술", "입"],
            "footwear": ["foot", "feet", "ankle", "barefoot", "발", "발목", "맨발"],
            "garment_detail": ["garment", "top", "skirt", "sleeve", "fabric", "clothing", "costume", "의복", "상의", "치마", "소매", "천", "옷", "의상"],
            "wearable_accessory": ["wearer", "wearing", "headset", "earpiece", "microphone", "cap", "hair", "costume", "arm", "head", "착용", "헤드셋", "귀", "마이크", "모자", "머리", "의상", "팔"],
        }[slot]
        profile = {"id": profile_id, "category": "selected_local_appearance_relation", "activation": {"exact_terms": full[:2], "requires_adult_character": False, "semantic_discovery_requires_component_evidence": True, "hard_activation": {"contract_version": "photo-visual-hard-activation/v1", "required_any_groups": [{"id": "declared_carrier", "any_terms": carrier_terms}]}}, "semantics": {"definition": full[0], "paraphrase_examples": full[2:], "visual_components": units, "contrast_examples": copy.deepcopy(card["confusion_boundaries"]), "claim_limits": [card["limits"], "Preserve all requester-owned subject, reference, age, count, dimension and property locks.", "This selected visible form does not establish character identity, biological cause, sound, operation, emission, transmission or narrative role.", "All components must coexist on the same declared carrier. Hidden required relations are unobservable and partial evidence fails."]}, "concept_candidate": {"concept_terms": [*full, *units], "core_assertion_discovery": True, "affected_dimensions": ["appearance"], "affected_properties": [effect]}, "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [], "forbidden_prompt_terms": [], "runtime_forbidden_labels": []}, "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": []}, "reject_substitutes": copy.deepcopy(card["confusion_boundaries"])}
        for i, (unit, korean_unit, pair) in enumerate(zip(units, korean, alternatives), 1):
            terms = [unit, korean_unit, *pair]
            profile["authored_components"]["components"].append({"id": f"component_{i}", "match_terms": terms, "evidence_field": f"component_{i}_phrase", "evidence_terms": terms, "min_content_words": 3, "instruction": "Keep this selected relation literal on its declared carrier: " + unit + ".", "render_gate": {"id": f"vo_{profile_id}_{i}", "review_scale": "native", "description": unit + ". Inspect this same-carrier relation in the original image; missing components fail and hidden components are unobservable."}})
        candidate_path = ASSETS / f"photo_prompt_{family}_extension.json"
        profile_path = ASSETS / f"photo_prompt_visual_obligations_{family}.json"
        docs[candidate_path]["slots"].setdefault(slot, []).append(entry)
        docs[profile_path]["profiles"].append(profile)
        profiles[profile_id] = (profile_path, profile)
        entries[candidate_id] = (candidate_path, slot, entry)
        log["new_profiles"].append({"card_id": key, "id": profile_id, "candidate_id": candidate_id, "profile_file": profile_path.name, "candidate_file": candidate_path.name, "slot": slot, "components": len(units), "paraphrases": full, "source_examples": card["source_examples"], "source_limit": card["limits"]})
        log["candidate_changes"].append({"id": candidate_id, "profile_id": profile_id, "slot": slot, "file": candidate_path.name, "new": True, "added_paraphrases": full})

    enriched = {row["id"] for row in log["existing_profiles"]}
    new_by_card = {row["card_id"]: row for row in log["new_profiles"]}
    for key, card in cards.items():
        existing = [x["profile_id"] for x in card["existing_profile_crosswalk"]]
        touched = [i for i in existing if i in enriched]
        if key in new_by_card:
            disposition = "new_selected_relation"
            linked = [new_by_card[key]["id"]]
            reason = "Separate carrier/topology/effect; concrete bilingual equivalents and native all-of duties are installed."
        elif key in HELD:
            disposition, linked, reason = "bounded_or_deferred", touched, HELD[key]
        elif touched:
            disposition, linked = "enrich_existing_equivalents", touched
            reason = "Only the existing selected subtype is expanded; related variants remain alternatives."
            if key in ["K18", "K19", "K20", "K22", "K23"]:
                disposition = "enrich_existing_adult_boundary"
                reason = "Adult eligibility, anatomical endpoints, scale and separate body axes remain authoritative; source chibi proportions are not human defaults."
        else:
            disposition, linked, reason = "reuse_unchanged_boundary", existing, "No equivalent positive widening is justified; the existing owner and selected variant stay unchanged."
        log["card_dispositions"].append({"card_id": key, "reference_term": card["reference_term"], "disposition": disposition, "profile_ids": linked, "reason": reason})

    log["source_reviews"] = [
        {"source_id": "S009", "review_scale": "original_source_pixels", "observation": "Cap crowns and rims carry visible eye/mouth motifs; Sugar and Spicy colors and projections are independent selected variants."},
        {"source_id": "S011", "review_scale": "original_source_pixels", "observation": "A bounded dark lip region is visible in restricted-palette artwork. Natural pigmentation, cosmetic color and personality are not established."},
        {"source_id": "S020", "review_scale": "original_source_pixels", "observation": "Package art does not establish unequal lateral skirt hem lengths; K42 stays deferred."},
        {"source_id": "S043", "review_scale": "original_source_pixels", "observation": "Small scattered facial dots are visible as a coarse distribution. This source is not a precise freckle-size or cause measurement."},
        {"source_id": "S052", "review_scale": "original_source_pixels", "observation": "A shorter frontal costume opening and continuing rear/lateral skirt fabric are visible. A new rendered test must independently show the selected upper panel connection."},
        {"source_id": "S054", "review_scale": "original_source_pixels", "observation": "Large rear ornaments and garment fabric are visible on package art; hidden fastenings, floor contact and two formal tails are not established."},
        {"source_id": "S055", "review_scale": "original_source_pixels", "observation": "Separate outer costume panels and wide waist bands are visible; this crop does not qualify their entire rear extent."},
        {"source_id": "S084", "review_scale": "original_source_pixels", "observation": "External membrane wing pieces with concave perimeter segments are visible behind the costume shoulder/back region. Anatomy, flight and a specific hidden harness are not established."},
    ]
    for path, doc in docs.items():
        if doc == originals[path]:
            continue
        # Re-read immediately before writing to avoid losing another chat's
        # simultaneous authored changes on this shared checkout.
        if read(path) != originals[path]:
            raise RuntimeError("Concurrent source change; rebase this additive edit before writing: " + str(path))
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        log["source_files"].append({"path": str(path.relative_to(ROOT)), "before_sha256": before, "after_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    log["counts"] = {"enriched_existing_profiles": len(log["existing_profiles"]), "new_profiles": len(log["new_profiles"]), "existing_candidate_entries_enriched": sum(not x["new"] for x in log["candidate_changes"]), "new_candidate_entries": sum(x["new"] for x in log["candidate_changes"]), "added_existing_profile_full_paraphrases": sum(len(x["added_paraphrases"]) for x in log["existing_profiles"]), "added_existing_component_term_alternatives": sum(sum(len(p) for p in x.get("component_alternatives", [])) for x in log["existing_profiles"]), "cards": len(log["card_dispositions"]), "source_files_changed": len(log["source_files"])}
    (HERE / "INTEGRATION-LEDGER.json").write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(log["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
