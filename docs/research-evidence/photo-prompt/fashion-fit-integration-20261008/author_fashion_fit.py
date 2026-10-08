"""Promote reviewed visible variants, never the family placeholder templates."""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
RESEARCH=ROOT/"docs/research-evidence/photo-prompt/fashion-fit-20261008"
sys.path.insert(0,str(ASSETS.parent/"scripts"))
import photo_candidate_semantics as cs
from photo_runtime_sources import source_update

# Each row declares actual endpoints and only the selected variant's effects.
# Vertical bars separate alternatives; these are independent variants, never all-of families.
RELATIONS="""FF01|shirt side panels|stand_away_from|same wearer's waist|fit.local_ease
FF01|dress skirt folds|hang_below|same dress's upper torso contact|fit.contact_distribution,material.drape
FF02|dress hanging folds|bridge_between|same dress's local torso contact areas|fit.contact_distribution,material.drape
FF02|top textile edges|remain_distinct_while_following|same wearer's torso|fit.contact_distribution
FF03|shirt torso and sleeves|enclose_clearance_around|same wearer's torso and arms|fit.body_clearance,fit.sleeve_width
FF03|jacket shoulder and sleeve edges|extend_beyond|same wearer's shoulder and torso contour|fit.shoulder.extent,fit.sleeve_width,fit.body_clearance
FF04|cropped jacket hem|ends_above|same wearer's trouser waistband|silhouette.torso_outline,length.hem_landmark
FF04|short top side edges|form_rectangle_above|same top's level hem|silhouette.torso_outline,length.hem_landmark
FF05|trouser waistband|narrows_relative_to|same trousers' roomy hip and thigh panels|fit.waist_to_hip_distribution,fit.thigh_ease,structure.waistband_contour
FF05|shirt side seams|narrow_below|same shirt's roomy chest and shoulders|fit.chest_to_waist_distribution,fit.shoulder.clearance
FF06|dress side edges|widen_toward|same dress's lower hem|silhouette.width_distribution
FF06|ensemble's shoulder and skirt outline|widens_around|same clothing's cinched waist|silhouette.width_distribution,fit.waist_suppression
FF07|coat side edges|bow_out_then_narrow_toward|same coat's lower hem|silhouette.convex_volume,fit.hem_taper
FF07|blouse folds|gather_into|same blouse's fitted waist band|silhouette.convex_volume,fit.hem_gathering,structure.waist_band
FF08|gown's lower skirt flare|begins_near|same wearer's knees below close hip and thigh fabric|fit.hip_thigh_contact,silhouette.flare_origin
FF08|gown's skirt widening|begins_above|same wearer's knees|silhouette.flare_origin
FF09|shirt sleeve attachment seam|lies_beyond|same wearer's shoulder tip on the upper arm|fit.shoulder.seam_position,structure.sleeve_attachment
FF09|jacket extended shoulder edge|supports|same jacket's attached sleeve outside the shoulder tip|fit.shoulder.extent,structure.sleeve_attachment
FF10|jacket shoulder outline|follows|same wearer's shoulder slope|silhouette.shoulder_profile,structure.sleeve_head
FF10|sleeve head ridge|rises_above|same jacket's shoulder attachment seam|structure.sleeve_head
FF11|separate shirt sleeve|joins_at|same shirt's curved armhole seam|structure.sleeve_attachment
FF11|shirt sleeve panel|joins_diagonally_to|same shirt's neckline and underarm|structure.sleeve_attachment
FF12|top underarm fabric|continues_between|same top's torso and sleeve below the armpit|structure.underarm_connection,fit.underarm_volume
FF12|top's body fabric|continues_into|same top's wrist-tapered sleeve across the shoulder|structure.sleeve_attachment,fit.sleeve_taper
FF13|garment armhole edge|lies_close_beneath|same wearer's armpit|fit.armhole_depth
FF13|garment armhole edge|hangs_below|same wearer's armpit with extra underarm fabric|fit.armhole_depth,fit.underarm_volume
FF14|short sleeve fabric|gathers_between|same sleeve's shoulder and lower edge|silhouette.sleeve_volume,structure.sleeve_gathering,length.sleeve
FF14|sleeve's upper volume|narrows_below|same sleeve's elbow-to-wrist section|silhouette.sleeve_volume,fit.sleeve_taper,length.sleeve
FF15|full sleeve folds|gather_into|same sleeve's narrow wrist cuff|fit.cuff_gathering,silhouette.sleeve_volume,length.sleeve
FF15|sleeve fabric|widens_toward|same sleeve's freely open wrist edge|silhouette.sleeve_flare,structure.cuff_edge,length.sleeve
FF16|sleeve fabric segments|swell_between|same sleeve's separated gathering bands|silhouette.sleeve_segments,structure.sleeve_gathering,length.sleeve
FF17|top neckline edges|meet_at|same top's central V point above continuous fabric|neckline.outline,neckline.depth
FF17|bodice upper edge arcs|meet_at|same bodice's lower central notch|neckline.outline
FF18|top's neckline fabric|falls_into|same top's connected front folds|structure.neck_folds
FF18|tall neck fabric|folds_over|same garment's doubled neck edge|neckline.height,structure.neck_folds
FF19|bodice supporting straps|pass_around|same wearer's neck outside both shoulders|coverage.shoulder,structure.strap_attachment
FF19|bodice upper edge|joins_to|same garment's sleeves below both shoulder tips|coverage.shoulder,structure.sleeve_attachment
FF20|top's enclosed opening boundary|connects_to|same top's fabric below the neckline|coverage.opening_location,structure.panel_connection
FF20|dress open-back side panels|connect_at|same dress's visible waist and shoulder supports|coverage.opening_location,structure.panel_connection,structure.strap_attachment
FF21|bodice-skirt joining seam|sits_directly_below|same wearer's bust above the hanging skirt|structure.waist_seam_position
FF21|bodice-skirt joining seam|sits_below|same wearer's natural waist|structure.waist_seam_position
FF22|dress waist fabric|gathers_into|same dress's encircling belt|fit.waist_suppression,structure.waist_adjuster
FF22|jacket side seams|narrow_then_widen_over|same jacket's waist and hip regions|fit.waist_suppression,silhouette.width_distribution
FF23|trouser waistband|sits_above|same wearer's natural waist|fit.waistband_landmark
FF23|trouser leg bifurcation|hangs_below|same wearer's body crotch level|structure.crotch_junction
FF24|trouser lower leg edges|narrow_below|same trousers' roomy upper thighs and knees|fit.thigh_ease,silhouette.knee_to_hem_width
FF24|trouser knee and hem edges|retain_similar_width_below|same trousers' narrow thigh panels|fit.thigh_ease,silhouette.knee_to_hem_width
FF25|trouser lower legs|widen_from|same trousers' narrow knees toward shoe-covering hems|silhouette.flare_origin,silhouette.hem_width,length.hem_contact
FF25|two trouser legs|flare_below|same trousers' knees above two distinct wide hems|silhouette.flare_origin,silhouette.hem_width
FF26|two convex trouser side seams|narrow_toward|same trousers' smooth smaller hems|silhouette.outer_leg_curve,silhouette.volume_peak,fit.hem_taper
FF26|rounded trouser upper legs|taper_into|same trousers' ungathered lower openings|silhouette.outer_leg_curve,silhouette.volume_peak,fit.hem_taper,structure.cuff_edge
FF27|two voluminous trouser legs|gather_into|same trousers' separate ankle cuffs|structure.leg_bifurcation,fit.ankle_gathering,length.hem_landmark
FF27|two cropped trouser legs|end_below|same wearer's knees in separate free hems|structure.leg_bifurcation,length.hem_landmark,silhouette.hem_width
FF28|skirt lower side edges|narrow_below|same skirt's close hip panels toward its knee hem|silhouette.side_outline,fit.hip_contact,length.hem_landmark
FF28|straight dress side edges|hang_from|same dress's shoulders around its uncinched waist|silhouette.side_outline,fit.waist_contact
FF29|triangular skirt insert|widens_between|same skirt's two panel seams toward its hem|structure.panel_joins,silhouette.lower_fullness
FF29|skirt front panel edge|overlaps|same skirt's second panel toward the tied waist|structure.wrap_overlap,structure.waist_adjuster
FF30|skirt hem|ends_between|same wearer's knee and ankle|length.hem_landmark
FF30|gown rear skirt extension|continues_from|same gown's floor-length main skirt|length.hem_landmark,length.front_back_difference
FF31|trouser front shallow fold|forms_above|same trouser hem's contact with the shoe upper|length.hem_contact,fit.lower_leg_fold_distribution
FF31|extra trouser fabric folds|spread_onto|floor beside the same shoe under that trouser leg|length.hem_contact,fit.lower_leg_fold_distribution
FF32|jacket front panels|overlap_across|same jacket's two visible button columns|structure.front_overlap,structure.front_fastener
FF32|jacket lower front edges|curve_apart_below|same jacket's fastening point|structure.front_edge_outline
FF33|jacket separate lining edge|lies_inside|same jacket's opened front panel|structure.visible_lining,structure.front_fastener_state
FF34|bodice dart folded intake|ends_near|same wearer's bust within the same bodice|structure.dart
FF34|bodice front panel|joins_along_curved_seam|same bodice's side-front panel through its shaped waist|structure.princess_seam,fit.waist_suppression
FF35|polygonal underarm gusset edges|join_to|same garment's adjacent fabric panels|structure.gusset,structure.panel_joins
FF35|shirt upper back yoke seam|joins_to|same shirt's lower torso panel|structure.yoke
FF36|parallel panel pleat ridges|fold_toward|same direction from their attached top to free hem|structure.pleat_direction,structure.fold_attachment
FF36|two panel folds|meet_inward_at|same panel's center to form an inverted box pleat|structure.pleat_direction,structure.fold_attachment
FF37|panel fabric folds|converge_into|same panel's gathering seam|structure.gather_anchor
FF37|small repeated panel gathers|lie_between|same panel's parallel stitch rows|structure.stitch_rows,structure.gather_anchor
FF38|dress soft folds|fall_from|same dress's hip region toward its distinct textile hem|material.drape,length.hem_landmark
FF38|jacket angular fabric folds|hold_above|same jacket's clearly defined lower edge|material.drape
FF40|two bra cups|connect_through|same bra's central fabric gore and underband|structure.cup_band_connection,structure.center_gore
FF40|two curved bra casings|follow|same bra's lower cup boundaries apart from its straps|structure.underwire_casing
FF41|bra angled cup edges|join_at|same bra's low center front with separate strap anchors|coverage.cup_edge,structure.center_height,structure.strap_attachment
FF41|bra open upper cup edges|connect_at_sides_to|same bra's lateral straps above its underband|coverage.cup_edge,structure.strap_attachment
FF42|bra upper cup textile edge|stands_away_from|same wearer's adjacent body surface|fit.cup_edge_gap
FF42|bra rear band|sits_above|same bra's side band along the torso|fit.band_alignment
FF43|corset upper edge|ends_beneath|same wearer's bust above waist-to-upper-hip panels|coverage.upper_edge,length.lower_edge
FF43|bodice vertical casings|follow|same bodice's connected seams over bust and waist|coverage.upper_edge,structure.bone_casing
FF44|bodice front metal loops|engage|same bodice's matching studs on the opposite edge|structure.front_fastener
FF44|bodice crossed laces|pass_through|both same-bodice eyelet edges above a fabric backing panel|structure.lacing,coverage.lacing_backing
FF46|garment abdominal panel edge|joins_to|same garment's adjacent fabric|structure.control_panel
FF47|one-piece garment torso|continues_into|same garment's brief with two leg openings|structure.torso_lower_connection,structure.leg_bifurcation,length.leg_coverage
FF47|fitted garment torso|continues_into|same garment's two long leg tubes|structure.torso_lower_connection,structure.leg_bifurcation,length.leg_coverage,fit.contact_distribution
FF48|garment leg opening edge|rises_at|same wearer's outer hip below a separate waist edge|coverage.leg_opening
FF48|brief rear panel edge|spans_across|same wearer's buttocks between distinct waist and leg edges|coverage.rear_panel
FF49|translucent outer panel|reveals|same garment's distinct inner lining edge at its opening|material.transmission,structure.visible_lining
FF49|loose sheer sleeve|hangs_away_from|same wearer's separately readable arm beneath its open weave|material.transmission,material.visible_weave,fit.sleeve_width
FF50|garment central neckline opening|lies_between|same garment's two cup regions apart from lateral openings|coverage.opening_location
FF50|garment lateral cup aperture|lies_beside|same garment's cup apart from its front neckline|coverage.opening_location
FF51|outer trouser fabric trace|overlies|same wearer's underwear edge|material.surface_relief
FF51|rear garment fabric folds|converge_into|same garment's stitched center seam|structure.rear_gathering
FF52|two shoulder straps|converge_into|same top's central yoke attached to its lower band|structure.back_strap_connection
FF52|two back straps|cross_once_before_opposite_attachment|same top's opposite lower anchor points|structure.back_strap_connection
FF53|leggings continuous front panel|joins_at_sides_to|same leggings' adjacent panels|structure.front_center_seam
FF53|low-profile athletic seam|joins|same garment's two fabric panels|structure.seam_relief
FF54|curved trouser knee panels|join_above_and_below|same wearer's bent knee|structure.articulation_panel
FF54|seated trouser rear waistband|sits_higher_than|same trousers' less-full front lap panel|fit.front_back_rise_distribution,fit.front_panel_ease
FF55|jacket opened back pleat|reveals_extra_fabric_between|same jacket's joined shoulder-blade panel edges|structure.action_back
FF55|waistband drawstring ends|emerge_from|same waistband's adjustment casing|structure.adjuster
FF56|jacket tension folds|radiate_toward|same jacket's fastened front button|fit.strain_lines,structure.front_fastener_state
FF56|trouser rear waistband edge|stands_away_from|same wearer's lower back|fit.edge_gap
FF57|panel seam-adjacent ripples|follow|same panel's stitched line|fit.seam_puckering
FF57|trouser side seam|turns_toward|same leg tube's lower front|structure.leg_seam_orientation
FF58|waistband rolled edge|folds_outward_over|same waistband's connected lower fabric|fit.band_roll
FF58|sleeve bunched fabric|collects_above|same wearer's elbow apart from the sleeve's free edge|fit.local_bunching
FF60|skirt lateral outline|extends_more_than|same skirt's front-to-back depth beside the waist|silhouette.lateral_volume
FF60|gown rear skirt mass|projects_behind|same gown's waist above its falling rear skirt|silhouette.rear_projection
FF61|long fitted bodice lower edge|extends_below|same wearer's waist over hips above the separate skirt|length.bodice_lower_edge,fit.contact_distribution
FF61|visible skirt support|lies_beneath|same skirt's lifted outer fabric layer|structure.visible_support,structure.lifted_layer_state
FF62|trouser fashion straps|span_between|same trousers' visible attachment points apart from leg seams|structure.strap_anchors
FF62|outer sleeve slashes|reveal|same sleeve's separate inner textile layer|structure.slashes,structure.visible_lining
FF63|soft shirt folds|hang_from|same shirt's lowered shoulder joins beneath long sleeves|material.drape,fit.shoulder.seam_position,length.sleeve
FF63|garment held shoulder and lower outline|retain_shape_at|same garment's defined fabric edges|material.drape,silhouette.width_distribution
FF64|cropped boxy jacket torso|joins_at_lowered_seams_to|same jacket's wide sleeves|length.hem_landmark,silhouette.torso_outline,fit.shoulder.seam_position,structure.sleeve_attachment,fit.sleeve_width
FF64|trouser roomy thighs|taper_below|same trousers' high waistband toward separate ankle hems|fit.waistband_landmark,fit.thigh_ease,silhouette.knee_to_hem_width,length.hem_landmark"""

REUSE={
 ("FF11",2):("garment_detail","clt_ct044_v1","clothing_ct044_v1"),
 ("FF14",1):("garment_detail","clt_ct046_v2","clothing_ct046_v2"),
 ("FF15",1):("garment_detail","clt_ct047_v1","clothing_ct047_v1"),
 ("FF34",1):("garment_detail","clt_ct031_v2","clothing_ct031_v2"),
}
DEFER={"FF51":"VPL and rear-scrunch variants require directly applicable term-specific source confirmation; product name/other-garment sources alone are insufficient."}
REWRITE={
 ("FF05",2):"The shirt has space through the chest and shoulders; its side seams narrow toward the waist.",
 ("FF04",2):"The short top has a broad rectangular body; its hem remains level across the front.",
 ("FF20",2):"The dress has an open back region; its side panels remain connected across visible waist and shoulder supports.",
 ("FF23",1):"The trouser waistband sits above the wearer's natural waist; the two leg tubes split below that waistband.",
 ("FF23",2):"The trouser leg junction hangs below the body's crotch level; a separate waistband borders the same trousers above it.",
 ("FF30",1):"The skirt hem ends between the knee and ankle; its textile edge remains distinct from the leg beneath it.",
 ("FF15",2):"The sleeve widens toward a freely open wrist edge; the flared end hangs freely at that same open edge.",
 ("FF26",2):"The trousers have rounded volume through the upper legs; their lower openings have smooth tapering edges.",
 ("FF41",2):"The bra cups have an open upper edge and laterally placed strap attachments; the underband remains a distinct textile component.",
 ("FF46",1):"The garment has a distinct abdominal fabric panel; its stitched boundary joins the adjacent fabric of that same garment.",
 ("FF48",2):"The brief's rear panel spans across the buttocks; its edges remain distinct from the garment's waist and leg openings.",
 ("FF63",1):"The shirt hangs softly from its lowered shoulder joins; long sleeves and flowing fabric continue from that same shirt body.",
 ("FF63",2):"The garment keeps a clearly defined shoulder edge and straight lower outline; its fabric holds that angular contour.",
}
SPECIAL_TERMS={
 ("FF05",1):["curvy-fit trouser waistband and hip room","커비핏 바지의 허리단과 힙 여유"],
 ("FF05",2):["athletic-fit shirt chest-to-waist room","애슬레틱핏 셔츠의 가슴과 허리 분량"],
 ("FF08",1):["knee-origin mermaid gown flare","무릎 부근에서 퍼지는 머메이드 드레스"],
 ("FF08",2):["above-knee gradual trumpet skirt flare","무릎 위에서 점차 퍼지는 트럼펫 스커트"],
 ("FF09",1):["drop-shoulder shirt seam beyond shoulder tip","드롭 숄더 셔츠의 어깨 끝 밖 연결선"],
 ("FF26",1):["barrel-leg convex seams and clean taper","배럴 레그의 볼록한 양쪽 솔기와 밑단 수축"],
 ("FF33",1):["visible lining inside an opened jacket","열린 재킷 안쪽에 보이는 별도 안감"],
 ("FF42",1):["bra cup-edge gaping","브라 컵 가장자리의 국소 들뜸"],
 ("FF52",1):["racerback Y strap convergence","레이서백 Y 끈 합류"],
 ("FF52",2):["cross-back X strap intersection","크로스백 X 끈 교차"],
 ("FF56",2):["rear waistband gaping","뒤 허리단 들뜸"],
}
KO_LABELS="""FF01|허리 옆판이 몸통에서 떨어지는 셔츠|상체를 따르고 힙 아래에서 접혀 떨어지는 드레스
FF02|몸의 국소 접촉 사이에 처진 직물이 남는 드레스|몸통을 따라 붙으며 목과 밑단 경계가 뚜렷한 상의
FF03|몸통과 소매에 따로 여유가 남는 셔츠|어깨 바깥으로 넓어지고 몸통과 소매가 함께 여유로운 재킷
FF04|바지 허리단 위에서 끝나는 직선 옆판의 박시 재킷|넓은 직사각 몸판과 수평 밑단의 짧은 상의
FF05|허리단은 가까이 맞고 힙과 허벅지에는 분량이 남는 바지|가슴과 어깨 분량보다 허리 옆선이 좁아지는 셔츠
FF06|몸판 위에서 밑단으로 점차 넓어지는 A형 드레스|어깨와 치마 폭 사이에 조인 허리가 있는 의복 윤곽
FF07|몸통 옆판이 볼록하고 아래로 다시 좁아지는 코트|허리 밴드 바로 위에 직물이 부풀어 모인 블라우스
FF08|힙과 허벅지에 붙고 무릎 부근에서 퍼지는 가운|무릎 위에서 치마 폭이 점차 넓어지는 가운
FF09|어깨 끝 바깥 상완에 소매 연결선이 놓이는 셔츠|어깨 바깥으로 연장된 의복 끝에 소매가 붙는 재킷
FF10|어깨 경사를 따라 부드럽게 소매로 이어지는 재킷|소매산 능선이 어깨 연결선 위로 솟는 재킷
FF11|둥근 암홀에 별도 소매가 붙는 셔츠|목둘레부터 겨드랑이까지 사선 연결선이 이어지는 소매
FF12|몸판에서 팔 아래로 넓게 이어지는 상의 직물|어깨 몸판과 연속되고 손목 쪽으로 좁아지는 소매
FF13|겨드랑이 바로 아래의 높은 암홀 연결선|겨드랑이 아래로 내려가 직물이 남는 낮은 암홀
FF14|어깨와 아래 가장자리 사이에 둥글게 부푼 짧은 소매|팔꿈치 위가 풍성하고 손목 쪽이 좁아지는 소매
FF15|풍성한 긴 소매가 좁은 손목 커프스로 모이는 형태|손목의 열린 가장자리로 넓어지는 벨 소매
FF16|여러 결속 밴드 사이에 둥글게 부푼 소매 구간
FF17|중앙 V점에서 만나는 사선 목둘레 가장자리|가운데 낮은 홈에서 만나는 두 곡선의 보디스 상단
FF18|목둘레 직물이 앞몸판의 부드러운 접힘으로 내려오는 상의|높은 목 직물이 바깥으로 접혀 이중 경계를 이루는 상의
FF19|양쪽 어깨 밖에서 목을 둘러 지지하는 보디스 끈|어깨 끝 아래로 내려간 몸판 경계에 붙는 소매
FF20|목둘레 아래에서 원단으로 완전히 둘러싸인 작은 개구부|허리와 어깨 지지부에 연결된 드레스의 열린 등판
FF21|가슴 바로 아래에서 몸판과 치마가 연결되는 높은 허리선|자연 허리 아래에서 몸판과 치마가 연결되는 드레스
FF22|허리를 두른 벨트로 직물 주름이 모이는 드레스|허리에서 안으로 굽고 힙에서 다시 넓어지는 재킷 옆선
FF23|자연 허리 위에 놓이는 바지 허리단|몸의 밑위보다 아래에서 두 다리로 갈라지는 바지
FF24|허벅지에는 여유가 있고 무릎 아래로 좁아지는 바지|허벅지는 좁고 무릎부터 밑단의 폭 변화가 작은 바지
FF25|좁은 무릎부터 신발 위의 밑단으로 조금 넓어지는 바지|무릎 아래에서 두 밑단이 크게 퍼지는 바지
FF26|양쪽 옆선이 중간 다리에서 볼록하고 밑단으로 수축하는 바지|상부 다리가 둥글고 발목 커프스 없이 아래가 좁아지는 바지
FF27|두 풍성한 바지통이 각각 발목 커프스로 모이는 형태|두 개의 열린 밑단이 무릎 아래에서 끝나는 넓은 크롭 바지
FF28|힙을 따라 붙고 무릎 길이의 밑단으로 좁아지는 스커트|어깨에서 직선으로 떨어지고 허리가 조이지 않은 드레스
FF29|두 치마 솔기 사이에서 아래로 넓어지는 삼각 삽입 패널|앞의 한 치마 패널이 다른 패널을 겹쳐 묶인 허리로 이어지는 형태
FF30|무릎과 발목 사이에서 끝나는 스커트 밑단|바닥 길이 치마 뒤로 같은 직물이 이어지는 트레인
FF31|신발 윗면에 닿아 앞쪽에 얕은 접힘 하나가 생기는 바짓단|신발 위의 여러 접힘과 바닥으로 퍼진 여분 바지 직물
FF32|두 버튼 열 위에서 앞판이 겹치는 재킷|여밈점 아래에서 앞판 가장자리가 곡선으로 벌어지는 재킷
FF33|열린 재킷 앞판 안쪽에서 경계가 보이는 별도 안감
FF34|가슴 부근에서 끝나는 짧은 테이퍼드 몸판 다트|허리로 이어지는 곡선에서 앞과 옆앞 패널이 연결되는 보디스
FF35|겨드랑이의 인접 패널을 연결하는 다각형 거싯|아래 몸판에 솔기로 연결되는 셔츠 상부 등 요크
FF36|부착된 상단부터 자유 밑단까지 같은 방향으로 접힌 플리트|패널 중앙에서 두 접힘이 안쪽으로 만나는 인버티드 박스 플리트
FF37|같은 패널의 모음 솔기로 작은 주름이 모이는 형태|평행한 스티치 열 사이에 작은 반복 주름이 모이는 패널
FF38|힙부터 밑단으로 부드러운 접힘이 내려오는 드레스 직물|아래 경계가 분명하고 각진 넓은 접힘을 유지하는 재킷 직물
FF40|중앙 고어와 같은 언더밴드에 연결되는 두 브라 컵|각 컵의 하부 가장자리를 따라 놓인 두 곡선 케이싱
FF41|낮은 중앙 연결부와 끈 앵커에 이어지는 사선 브라 컵 가장자리|옆 끈과 아래 밴드에 연결되는 열린 상부 브라 컵 경계
FF42|같은 브라의 상부 컵 경계와 몸 사이에 보이는 작은 틈|옆 밴드보다 뒤 밴드가 높게 놓인 브라
FF43|가슴 아래의 상단부터 허리와 상부 힙으로 이어지는 코르셋|가슴과 허리 패널 솔기를 따라 세로 케이싱이 연결된 보디스
FF44|서로 맞물리는 고리와 스터드가 양쪽 앞 경계를 연결하는 보디스|양쪽 아일릿의 교차 레이스 뒤로 별도 직물 패널이 보이는 보디스
FF46|인접한 직물에 봉제 경계로 이어지는 복부 의복 패널
FF47|몸판이 허리를 지나 두 다리 개구부의 브리프와 연결된 한 의복|붙는 몸판부터 두 긴 바지통까지 한 의복으로 연결된 형태
FF48|별도 허리 경계 아래에서 외측 힙으로 높아지는 다리 개구부|허리와 다리 개구부 사이에서 둔부를 덮는 브리프 뒤 패널
FF49|겉의 반투명 패널 아래로 경계가 따로 읽히는 안감|팔에서 떨어진 느슨한 시어 소매의 망과 그 아래 팔
FF50|두 컵 구역 사이에 놓인 중앙 목둘레 개구부|앞 목둘레와 분리되어 컵 옆에 놓인 의복 개구부
FF51|연속된 겉 바지 직물 위로 보이는 아래층 속옷 가장자리 자국|뒤중심의 같은 봉제선으로 작은 직물 접힘이 모이는 형태
FF52|등의 두 어깨 끈이 중앙 요크로 합류해 같은 밴드에 붙는 형태|등에서 한 번 교차한 두 끈이 반대쪽 아래 앵커로 이어지는 형태
FF53|중앙이 연속되고 옆에서 인접 패널과 연결되는 레깅스 앞판|두 운동복 패널이 낮은 돌출의 봉제선으로 연결된 형태
FF54|굽힌 무릎 위아래에서 연결되는 곡선 바지 패널|앉은 바지의 뒤 허리단은 높고 앞 무릎 위 직물 분량은 적은 형태
FF55|재킷 어깨뼈 옆의 연결된 등 주름을 열어 보이는 여분 직물|같은 허리단 조절 통로에서 양끝이 나오는 드로스트링
FF56|잠긴 재킷 버튼으로 짧은 당김 주름이 모이는 형태|뒤 허리단 가장자리와 허리 아래 등 사이에 보이는 틈
FF57|같은 패널의 봉제선 바로 옆을 따라 반복되는 잔주름|같은 바지통의 옆 솔기가 아래 앞쪽으로 돌아가는 형태
FF58|연결된 허리 밴드 위로 바깥쪽에 말린 가장자리|자유 소매 끝과 떨어져 팔꿈치 위에 뭉친 직물
FF60|앞뒤 깊이보다 허리 좌우 폭이 크게 확장된 스커트|허리 바로 아래의 뒤 돌출부에서 치마가 떨어지는 가운
FF61|자연 허리 아래의 힙까지 내려가 아래 치마와 경계가 구분되는 보디스|들린 치마층 아래에서 겉 원단을 받치는 별도 지지 형태
FF62|바지 솔기와 분리되어 같은 바지의 앵커 사이를 잇는 끈|겉 소매의 반복 절개로 아래의 다른 직물이 보이는 형태|같은 의복의 두 원단 앵커를 버클로 연결하는 웨빙 끈
FF63|낮은 어깨 연결선부터 긴 소매로 이어져 부드럽게 처지는 셔츠|어깨 경계와 직선 하단의 각진 외곽을 유지하는 의복
FF64|짧고 박시한 몸판과 낮은 연결선의 넓은 소매가 한 재킷인 형태|높은 허리와 여유로운 허벅지 아래로 두 발목 밑단이 좁아지는 바지"""
KO={line.split("|")[0]:line.split("|")[1:] for line in KO_LABELS.splitlines()}

def dump(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")

def main():
 cards=json.loads((RESEARCH/"semantic-cards.json").read_text())["cards"]
 idx={c["id"]:c for c in cards}
 declarations={}
 for line in RELATIONS.splitlines():
  family,subject,op,obj,props=line.split("|")
  declarations.setdefault(family,[]).append((subject,op,obj,props.split(",")))
 ext={"schema_version":json.loads((ASSETS/"photo_prompt_clothing_structure_extension.json").read_text())["schema_version"],"slots":{},"visual_semantics":[],"existing_slot_context_extensions":{}}
 profiles=[];decisions=[];backlog=[]
 for c in cards:
  if not c["alternative_clauses_en"]:
   backlog.append({"card_id":c["id"],"disposition":"specification_or_process_not_a_pixel_contract","reason":c["meaning_ko"]})
   continue
  if c["id"] in DEFER:
   backlog.append({"card_id":c["id"],"disposition":"term_specific_evidence_pending","reason":DEFER[c["id"]]})
   continue
  for n,original in enumerate(c["alternative_clauses_en"],1):
   key=(c["id"],n);subj,op,obj,props=declarations[c["id"]][n-1]
   clause=REWRITE.get(key,original)
   if key in REUSE:
    slot,cid,pid=REUSE[key]
    # Keep the existing narrower, fully declared variant instead of adding new demands.
    alias={"FF11":"shirt raglan neckline-to-underarm attachment",
           "FF14":"short puff sleeve gathered at both shoulder and lower edge",
           "FF15":"full bishop sleeve gathered at wrist cuff",
           "FF34":"short tapered bodice dart ending near the bust"}[c["id"]]
    ext["existing_slot_context_extensions"].setdefault(slot,{})[cid]={
       "paraphrases":[alias],
       "contexts":[{"id":f"fit_reuse_{c['id'].lower()}_{n}",
          "meaning":c["meaning_ko"],"claim_limits":c["confusion_boundary_ko"]}]}
    decisions.append({"card_id":c["id"],"variant":n,"disposition":"existing_narrower_variant_reused",
        "candidate_id":cid,"profile_id":pid,"slot":slot,
        "preserve_existing_scope":True,"source_ids":c["source_ids"]})
    continue
   register_variant(c,n,clause,subj,op,obj,props,ext,profiles,decisions)

 # Garment-instance generalization of the researched fashion-strap/anchor topology.
 c=idx["FF62"]
 register_variant(c,3,
   "A garment strap bridges two visible fabric anchors on the same item; a buckle joins its two webbing sections.",
   "same garment's webbing strap","joins_through_buckle_between","two visible fabric anchors of that garment",
   ["structure.strap_anchors","structure.strap_fastener"],ext,profiles,decisions)

 old_path=ASSETS/"photo_prompt_fashion_fit_extension.json"
 prior_ref=json.loads(old_path.read_text()).get("maintenance_ref") if old_path.exists() else None
 revision=2
 while (ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/f"fashion-fit-observable-variants-20261008-r{revision}.json").exists(): revision+=1
 record_id=f"fashion-fit-observable-variants-20261008-r{revision}"
 changes=[{"id":r["candidate_id"],"profile_id":r["profile_id"],"slot":r["slot"],
           "new":r["disposition"]=="new_scoped_visible_variant","card_id":r["card_id"],"variant":r["variant"]}
          for r in decisions]
 record={"schema_version":"photo-extension-maintenance/v1","record_id":record_id,
     "maintenance_only":True,
     "source_filename":"photo_prompt_fashion_fit_extension.json","authored_source_sha256":cs.digest(ext),
     "scope":"Selected, concrete garment fit/structure/state variants with same-owner endpoints and complete effects; equivalent existing paraphrases only.",
     "candidate_changes":changes,"evidence_basis":"Bounded 41-source fashion-fit research; source-specific limits, reuse and pending terms retained outside runtime.",
     "property_scope":"main_subject.wardrobe.* effects preserve garment ownership; material behavior declares both appearance and material scope; explicit posture prerequisites declare pose scope. No body reshaping, diagnosis, material measurement or identity change.",
     "history_preservation":"Existing authored files and prior immutable maintenance records are preserved.",
     "validation_status":{"authored":"pending","retrieval":"pending","native_pixels":"pending","user_acceptance":"not_tested"}}
 if prior_ref:record["prior_maintenance_ref"]=prior_ref
 ext["maintenance_ref"]={"contract_version":cs.MAINTENANCE_VERSION,"record_id":record_id,"sha256":cs.digest(record)}
 manifest=json.loads((ASSETS/"photo_prompt_source_manifest.json").read_text())
 additions=[("photo_prompt_fashion_fit_extension.json","candidate"),("photo_prompt_visual_obligations_fashion_fit.json","visual_profile")]
 for filename,kind in additions:
  if not any(s["file"]==filename for s in manifest["sources"]):
   manifest["sources"].append({"file":filename,"kind":kind,"required":True,
      "load_order":1+max(s["load_order"] for s in manifest["sources"] if s["kind"]==kind)})
 with source_update(ASSETS.parent):
  dump(ASSETS/"photo_prompt_fashion_fit_extension.json",ext)
  visual_shape=json.loads((ASSETS/"photo_prompt_visual_obligations_clothing_structure.json").read_text())
  dump(ASSETS/"photo_prompt_visual_obligations_fashion_fit.json",{
     "schema_version":visual_shape["schema_version"],
     "relation_contract_version":visual_shape["relation_contract_version"],
     "description":"Selected same-garment fit, panel, layer and boundary relationships; alternatives remain independent.",
     "profiles":profiles})
  dump(ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/(record_id+".json"),record)
  dump(ASSETS/"photo_prompt_source_manifest.json",manifest)
 dump(HERE/"runtime-integration.json",{"state":"authored_pending_validation",
     "new_candidate_count":sum(len(v) for v in ext["slots"].values()),"new_profile_count":len(profiles),
     "reused_candidate_count":len(REUSE),"integrated_card_count":len({r["card_id"] for r in decisions}),
     "total_research_cards":64,"decisions":decisions,"backlog":backlog,
     "source_ids":sorted({s for c in cards for s in c["source_ids"]}),
     "source_note":"Family/label/source mapping is not proof of every alias; only selected clauses are runtime variants."})
 terms=json.loads((RESEARCH/"term-plan.json").read_text())["terms"]
 mapping=[]
 for t in terms:
  matched=[r for r in decisions if r["card_id"] in t["semantic_card_ids"]]
  held=[r for r in backlog if r["card_id"] in t["semantic_card_ids"]]
  mapping.append({"id":t["id"],"source_term":t["source_term"],"evidence_class":t["evidence_class"],
      "semantic_card_ids":t["semantic_card_ids"],
      "related_selected_variant_ids":[r["profile_id"] for r in matched],
      "backlog":held,"status":"family_related_selected_variants_not_universal_alias_activation"})
 dump(HERE/"term-runtime-map.json",{"count":len(mapping),"terms":mapping})
 print(json.dumps({"new_candidates":sum(map(len,ext["slots"].values())),"new_profiles":len(profiles),
    "reuse":len(REUSE),"integrated_cards":len({r["card_id"] for r in decisions}),"backlog":len(backlog)}))

def register_variant(c,n,clause,subj,op,obj,props,ext,profiles,decisions):
 prefix=f"fit_{c['id'].lower()}_v{n}";cid=prefix+"_candidate";pid=prefix
 parts=[p.strip().rstrip(".")+"." for p in clause.split(";")]
 effects=[{"dimension":"appearance","target":"main_subject","property":"wardrobe."+p} for p in props]
 for p in props:
  if p.startswith("material."):
   effects.append({"dimension":"material","target":"main_subject","property":"wardrobe."+p})
 pose_prerequisite={("FF12",1):"posture.arm_elevation",("FF54",1):"posture.knee_flexion",("FF54",2):"posture.seated"}.get((c["id"],n))
 if pose_prerequisite:effects.append({"dimension":"pose","target":"main_subject","property":pose_prerequisite})
 dimensions=list(dict.fromkeys(e["dimension"] for e in effects))
 short_ko=KO[c["id"]][n-1]
 concept_terms=SPECIAL_TERMS.get((c["id"],n),[short_ko,clause])
 slot="wardrobe_style" if c["axis"] in {"volume","silhouette","dress_geometry","historical_volume","composition"} else "garment_detail"
 row={"id":cid,"ko":short_ko,"en":clause,"weight":0.35,"tags":["clothing"],
      "aliases":concept_terms,"keywords":list(dict.fromkeys(concept_terms+parts)),
      "embedding_text":clause+" | "+subj+" "+op.replace("_"," ")+" "+obj,
      "concept_units":parts,"relations":[{"id":prefix+"_owner_relation","type":op,"subject":subj,"object":obj}],
      "affected_dimensions":dimensions,"affected_properties":effects,"core_assertion_discovery":True,
      "for_any":["human"]}
 ext["slots"].setdefault(slot,[]).append(row)
 components=[]
 for i,part in enumerate(parts,1):
  components.append({"id":f"component_{i}","match_terms":[part],
      "evidence_field":f"component_{i}_phrase","evidence_terms":[part],"min_content_words":3,
      "instruction":"Keep this selected same-garment relation visible: "+part,
      "render_gate":{"id":f"vo_{prefix}_{i}","review_scale":"native",
       "description":part+" Read its declared owner and both endpoints in the same saved image. Hidden or partial evidence is not a pass."}})
 profiles.append({"id":pid,"category":"fashion_fit_selected_visible_relation",
     "activation":{"exact_terms":[clause],"requires_adult_character":False,
       "semantic_discovery_requires_component_evidence":True,
       "hard_activation":{"contract_version":"photo-visual-hard-activation/v1",
        "required_any_groups":[{"id":"selected_visible_variant","any_terms":[clause]}]}},
     "semantics":{"definition":clause,"paraphrase_examples":list(dict.fromkeys([x for x in concept_terms if x!=clause]+["Observable relation between "+subj+" and "+obj])),
       "visual_components":parts,"contrast_examples":[c["confusion_boundary_ko"]],
       "claim_limits":[c["visibility_prerequisite_ko"],
         "One selected visible variant; labels and family alternatives never impose an all-of duty.",
         "Garment geometry does not alter or establish wearer identity, body dimensions, age, personality or health.",
         "Still pixels do not establish numeric ease, compression pressure, fiber content, comfort, support performance or change history."]},
     "authored_components":{"contract_version":"photo-authored-visual-components/v1","components":components},
     "concept_candidate":{"concept_terms":concept_terms,"core_assertion_discovery":True,
        "affected_dimensions":dimensions,"affected_properties":effects},
     "runtime_expression":{"default_mode":"definition_with_optional_label","prompt_label_terms":[],
        "forbidden_prompt_terms":[],"runtime_forbidden_labels":[]},
     "reject_substitutes":[c["confusion_boundary_ko"]]})
 ext["visual_semantics"].append({"id":prefix+"_bundle","primary_visual_proposition":clause,
      "hard_profile_ids":[pid],"component_groups":[{"id":f"component_{i}","visible_evidence":[part]} for i,part in enumerate(parts,1)],
      "candidate_ids":[cid],"candidate_slots":{cid:slot},"confusion_boundaries":[c["confusion_boundary_ko"]],
      "source_keywords":concept_terms,"candidate_only":True,"activation_mode":"component_complete_exact_only",
      "relations":copy.deepcopy(row["relations"])})
 decisions.append({"card_id":c["id"],"variant":n,"candidate_id":cid,"profile_id":pid,"slot":slot,
    "disposition":"new_scoped_visible_variant","source_ids":c["source_ids"],"same_owner_relation":row["relations"],
    "affected_properties":effects,"revised_research_clause":clause!=c["alternative_clauses_en"][n-1] if n<=len(c["alternative_clauses_en"]) else True,
    "abstracted_geometry_note":"FF62 v3 abstracts visible strap/buckle/anchor topology; it establishes no safety, restraint or performance claim." if c["id"]=="FF62" and n==3 else None})

if __name__=="__main__":main()
