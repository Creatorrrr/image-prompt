from pathlib import Path
import json, hashlib, re, sys
from collections import defaultdict
WORK=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
BASE=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem')
RESEARCH=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009')
ASSETS=WORK/'skills/photo-prompt-image-generator/assets'
SCRIPTS=WORK/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
from visual_profile_contracts import validate_visual_profile_source, compile_visual_profile
from photo_candidate_semantics import validate_candidate_entries
specs={}
def add(key,ko,owner,props,components,edges,contrast,claim='',slot=None):
    assert key not in specs
    specs[key]={'ko':ko,'owner':owner,'props':props.split('|'),'components':components.split('~'),'edges':[t.split('>') for t in edges.split('~')], 'contrast':contrast, 'claim':claim,'slot':slot}

add('SF002_01','같은 상의에서 쇄골 양옆으로 넓게 열린 목선','selected top','wardrobe.neckline.width',
 'The selected top neckline spans widely across the same wearer\u2019s collarbone area',
 'selected top neckline>spans_across>same wearer collarbone area',
 'A deep narrow opening changes depth rather than establishing a wide opening across the collarbone; width alone does not place the top below the shoulders.')
add('SF003_02','세로로 길어져 아래쪽이 둥근 같은 상의의 U 목선','selected top','wardrobe.neckline.contour|wardrobe.neckline.depth',
 'The same top neckline has two descending side edges joined by an extended rounded U-shaped bottom',
 'selected top neckline side edges>joined_by>selected top rounded U bottom~selected top rounded U bottom>extends_below>selected top neckline upper endpoints',
 'A centered sharp V point or a wide shallow round opening does not provide this elongated U boundary; body shading is not the cloth edge.')
add('SF005_02','같은 몸통 중앙으로 낮게 뻗는 두 경계의 V 목선','selected top','wardrobe.neckline.contour|wardrobe.neckline.depth',
 'The same top has two sloping neckline edges that meet at a low point along the center of the existing torso',
 'selected top left neckline edge>converges_with>selected top right neckline edge~selected top convergence point>lies_low_along>same wearer torso center',
 'A rounded opening or a skin shadow cannot replace the two cloth edges and their low convergence point; the shape does not require cleavage.')
add('SF007_02','같은 몸판 가슴 위를 거의 수평으로 가로지르는 윗선','selected bodice','wardrobe.neckline.contour',
 'The selected bodice upper edge runs nearly straight across the same upper chest',
 'selected bodice upper edge>runs_across>same wearer upper chest',
 'Two rounded sweetheart arcs are a different contour; a straight edge makes no claim about straps, cup seams or hidden support.')
add('SF009_02','양어깨 아래에서 같은 상의 윗선을 따라 접힌 직물 띠','selected top','wardrobe.shoulder.coverage|wardrobe.neckline.fold',
 'A folded fabric band follows the selected top upper edge below both shoulders~The doubled fold remains continuous with that same top edge',
 'selected top folded band>follows>selected top upper edge~selected top upper edge>lies_below>same wearer left and right shoulder landmarks~selected top folded band>continuous_with>selected top upper cloth edge',
 'A broad neckline resting on the shoulders is not a folded band below both shoulders; an unrelated scarf does not supply the top fold.')
add('SF011_01','같은 상의 앞판에 붙어 목 뒤로 이어지는 홀터 끈','selected top','wardrobe.strap.route|wardrobe.strap.front_attachment',
 'The selected top front joins two strap paths that continue beside the same neck and around its back',
 'selected top front strap roots>join>selected top front panel~selected top left and right straps>continue_around>same wearer neck back',
 'A high neckline, racerback or necklace supplies no front-panel-to-neck-back strap connection.',
 'A frontal crop cannot establish a hidden rear route; both roots and the continuing neck-side/rear path must be observed for a full pixel pass.')
add('SF013_01','양어깨 경로가 드러난 같은 상의의 끈 없는 윗선','selected top','wardrobe.strap.presence',
 'The selected top upper edge spans the torso while both visible shoulder paths are free of straps belonging to that top',
 'selected top upper edge>spans_across>same wearer torso~selected top left shoulder path>visibly_open_beside>same wearer left shoulder~selected top right shoulder path>visibly_open_beside>same wearer right shoulder',
 'A necklace or a strap belonging to a separate inner garment is a different owner; a cropped shoulder cannot establish this visible strap-free path.',
 'Review only paths actually exposed in the saved view; this is no claim about a concealed back strap or an unseen inner garment.')
add('SF014_03','같은 민소매 상의의 완성된 암홀 둘레와 열린 팔 경로','selected top','wardrobe.sleeve.presence|wardrobe.armhole.edge_finish',
 'The selected top has finished cloth armhole edges opening onto the same upper arms~Each visible armhole edge ends without an attached sleeve tube',
 'selected top left armhole edge>opens_onto>same wearer left upper arm~selected top right armhole edge>opens_onto>same wearer right upper arm',
 'A sleeve cropped outside the frame does not prove a sleeveless armhole; strap width and concealed inner layers remain separate choices.')
add('SF016_01','견갑골 사이 중앙으로 모여 연결된 같은 상의의 레이서백','selected top','wardrobe.back.strap_topology',
 'The same top back narrows into one central fabric bridge between the shoulder blades~Both back shoulder paths join that bridge',
 'selected top left rear shoulder path>joins>selected top central back bridge~selected top right rear shoulder path>joins>selected top central back bridge~selected top central back bridge>lies_between>same wearer shoulder blades',
 'Parallel rear straps and crossed straps have different junctions; a front-only view cannot prove the bridge.')
add('SF017_02','같은 탱크의 겨드랑이 아래로 깊게 내려오는 암홀','selected tank top','wardrobe.armhole.depth',
 'The selected tank armhole lower cloth edge descends well below the same wearer\u2019s armpit landmark',
 'selected tank armhole lower edge>lies_below>same wearer armpit landmark',
 'A low shoulder seam changes sleeve placement, not the armhole bottom; a deep opening does not require exposed side-chest skin or removal of an inner layer.')
add('SF019_01','같은 상의 옆 가장자리 두 타이가 만나 만드는 옆매듭','selected top','wardrobe.closure.tie_location|wardrobe.closure.connection',
 'Two fabric tie ends originate at the selected top side edges~Those same tie ends meet in a visible knot at the top side',
 'selected top first tie root>attached_to>selected top first side edge~selected top second tie root>attached_to>selected top opposite side edge~selected top first tie end>knotted_with>selected top second tie end',
 'A separately attached decorative bow or a belt from another garment does not establish these two tie roots and their shared side knot.',
 'Visible ties and a knot do not establish adjustable fit, tightening force or whether hidden fasteners exist.')
add('SF020_02','아래 몸판은 이어진 채 등 윗선만 낮게 내려온 상의','selected top','wardrobe.back.coverage|wardrobe.back.panel_continuity',
 'The selected top back upper edge lies low across the same back~The lower back cloth panel remains continuous beneath that edge',
 'selected top back upper edge>lies_low_across>same wearer back~selected top lower back panel>continues_below>selected top back upper edge',
 'A deep front neckline, mesh across the back or an occluded rear panel is not this low rear edge with a continuous lower panel.')
add('SF022_01','휘어진 컵 패널이 긴 밀착 몸판에 이어지는 같은 뷔스티에','selected bustier','wardrobe.bodice.cup_panels|wardrobe.bodice.panel_connection|wardrobe.bodice.length',
 'Distinct curved cup panels occupy the selected bustier front~Their lower cloth boundaries join a longer fitted torso panel of that same bustier',
 'selected bustier cup lower boundaries>join>selected bustier torso panel~selected bustier torso panel>extends_below>selected bustier cups',
 'Two separate bra cups above an unrelated skirt or belt are not the same longer bustier body; printed curved lines are not joined cup panels.',
 'Visible cup panels do not establish concealed wire, boning, padding, compression or altered body measurements.')
add('SF024_01','두 컵 영역이 짧은 몸통 밴드에 연결된 같은 브라형 상의','selected bra-style top','wardrobe.bra.cup_regions|wardrobe.bra.band_length|wardrobe.bra.panel_connection',
 'The selected bra-style top has two separate visible cup regions~Both cup lower boundaries join a short torso band of the same top',
 'selected top left cup region>joins>selected top short torso band~selected top right cup region>joins>selected top short torso band',
 'Cup-like print or two cups belonging to a separate undergarment does not supply this same top band; long bustier panels are another variant.',
 'This visible panel arrangement does not establish wire, padding, support performance or textile stretch.')
add('SF025_02','양어깨 경로가 드러나고 허리까지 이어지는 같은 튜브 톱','selected tube top','wardrobe.bodice.length|wardrobe.strap.presence',
 'The same tube top cloth body continues from its upper-torso edge down to the waist~Both observable shoulder paths are free of straps belonging to that tube top',
 'selected tube top cloth body>continues_between>selected top upper-torso edge and waist hem~selected tube top shoulder paths>remain_open_beside>same wearer shoulders',
 'A narrow bandeau band ends higher; a crop that hides shoulders cannot prove the visible strap-free paths.',
 'Only shown shoulder and torso paths are checked; hidden support or concealed underwear absence remains unclaimed.')
add('SF027_01','중앙 봉제선이 읽히지 않는 같은 컵의 매끈한 연속 겉면','selected garment cup','wardrobe.cup.surface|wardrobe.cup.visible_seam',
 'The selected garment cup shows a smooth continuous outer surface~The observable cup center remains an uninterrupted cloth area',
 'selected cup center surface>continuous_with>selected cup surrounding outer surface',
 'A cup center hidden by a hand, blur or a fold cannot establish an uninterrupted visible surface.',
 'Padding thickness, moulding process, internal seams, wire and support are metadata; an externally smooth cup is not evidence of them.')
add('SF029_02','같은 몸판에서 가슴 부위를 지나 허리로 이어지는 곡선 절개','selected bodice','wardrobe.bodice.shaping_seams',
 'One curved joining seam continues through the selected bodice bust area toward its waist~The seam separates two adjoining cloth panels on that same bodice',
 'selected bodice curved seam>continues_between>selected bodice bust area and waist~selected bodice adjoining panel edges>joined_by>selected bodice curved seam',
 'A straight decorative stripe, body skin line or dart ending within the panel does not supply this continuing curved panel join.')
add('SF031_02','같은 상의 앞판 두 직물 부분이 중앙에서 꼬여 교차함','selected top','wardrobe.front.twist|wardrobe.bust.folds',
 'Two front cloth sections of the same top twist around a visible central crossing~Each section continues from its own front panel into that crossing',
 'selected top first front section>crosses_and_twists_with>selected top second front section~selected top central crossing>continuous_with>selected top two front panels',
 'A printed X, a detached bow or folds merely converging at a stitch point is not the two cloth sections twisting together.')
add('SF032_03','같은 상의 밑단과 바지 허리단 사이에 보이는 미드리프 간격','selected top and trousers','wardrobe.top.hem_height|wardrobe.coverage.midriff_gap|wardrobe.bottom.waistband_height',
 'The same top lower cloth edge ends above the separate trouser waistband~A visible midriff interval lies between those two garment boundaries',
 'selected top lower edge>lies_above>selected trouser waistband~visible midriff interval>lies_between>selected top lower edge and selected trouser waistband',
 'A skin-colored lining or a cutout enclosed within one dress is not an interval between the independent top hem and trouser waistband.',
 'This checks the declared visible interval only; top length alone does not prove bare skin or the absence of a concealed layer.')
add('SF034_01','같은 상의 여밈 아래에서 갈라지는 두 앞판 밑단','selected top','wardrobe.front.split|wardrobe.closure.extent',
 'The same top closure stops above the front lower edges~The two front lower cloth edges separate into an open split below that closure',
 'selected top closure lower endpoint>lies_above>selected top front split~selected top left lower front edge>separates_from>selected top right lower front edge',
 'A printed dark line, wrinkle or whole front opening without the declared terminating closure is not this local split.')
add('SF035_01','같은 드레스 허리의 둘러싸인 개구부와 위아래 이어진 직물','selected dress','wardrobe.cutout.location|wardrobe.cutout.topology|wardrobe.panel.continuity',
 'A cloth-bounded opening interrupts the selected dress waist panel~Connected dress fabric remains above and below the opening',
 'selected dress waist opening>bounded_by>selected dress cloth perimeter~selected dress upper and lower waist panels>connected_around>selected dress waist opening',
 'A transparent solid insert, skin-tone lining or a crop top\u2019s unbounded lower gap is not a bounded waist opening in one connected dress.',
 'The surface visible through the opening must keep its actual owner; this shape adds no automatic skin exposure.')
add('SF036_01','같은 고리의 서로 반대쪽에 붙은 별도 직물 탭 두 개','selected garment ring connection','wardrobe.hardware.connection|wardrobe.hardware.tab_attachment',
 'Two separate cloth tabs terminate at opposite sides of the same visible ring~Each tab has a readable attachment to its own garment section',
 'selected garment first tab>attached_to>selected ring first side~selected garment second tab>attached_to>selected ring opposite side~selected ring>connects>selected garment first and second sections',
 'A loose ring print, dangling decorative circle or two tabs belonging to unrelated garments does not establish these opposing connections.',
 'A visible ring connection does not establish tightening force, adjustable closure, abdominal exposure or hardware material.')
add('SF038_02','같은 착용자의 배꼽보다 높게 위치한 바지 허리단','selected trousers','wardrobe.bottom.waistband_height',
 'The selected trouser waistband upper edge lies above the same wearer\u2019s visible navel reference',
 'selected trouser waistband upper edge>lies_above>same wearer navel landmark',
 'A high belt on a separate garment is another owner; a covered or cropped navel cannot establish the stated vertical comparison.',
 'Review does not infer an unseen navel, measured rise, leg length or body proportion change.')
add('SF040_01','같은 착용자의 양무릎 위에서 끝나는 치마 밑단','selected skirt','wardrobe.skirt.hem_height',
 'The selected skirt textile hem ends above both knee landmarks of the same wearer',
 'selected skirt hem>lies_above>same wearer left and right knee landmarks',
 'A camera crop above the knees or an inner garment edge does not establish the outer skirt\u2019s length.',
 'The gate requires the actual skirt edge and the relevant knee landmarks; it supplies no exposure, age or numeric length claim.')
add('SF040_04','이미 선언된 성인 착용자의 허벅지 높은 지점에서 끝나는 짧은 치마','selected skirt','wardrobe.skirt.hem_height',
 'On the already-declared adult wearer, the same skirt textile hem ends high along the thighs',
 'selected skirt hem>ends_high_along>declared adult wearer thigh landmarks',
 'A cropped frame or a folded skirt temporarily lifted by a hand is not the stated settled short hem.',
 'Adult eligibility is a prerequisite, not an age transformation. No hidden underwear or exposure amount is inferred.')
add('SF041_03','같은 치마에 두 개로 구분되어 열린 슬릿','selected skirt','wardrobe.skirt.slit_count|wardrobe.skirt.slit_topology',
 'Two distinct slit openings interrupt the same skirt~Each slit has its own upper endpoint and two separating cloth edges',
 'selected skirt first slit>distinct_from>selected skirt second slit~selected skirt first slit>bounded_by>first slit paired cloth edges~selected skirt second slit>bounded_by>second slit paired cloth edges',
 'Two pleat shadows, a printed stripe or one wrap overlap cannot stand in for two independently bounded openings.',
 'Location and upper height beyond the visible endpoints remain open; the visible surface behind each slit retains its actual owner.')
add('SF042_02','엉덩이를 감싼 같은 스커트 패널이 옆에서 매듭으로 만남','selected wrap skirt','wardrobe.skirt.overlap|wardrobe.skirt.closure|wardrobe.closure.tie_location',
 'The same skirt cloth wraps around the hips with one panel overlapping another~Its two cloth ends meet in a visible side knot',
 'selected skirt outer panel>overlaps>selected skirt inner panel~selected skirt first cloth end>knotted_with>selected skirt second cloth end~selected skirt side knot>lies_beside>same wearer hip',
 'A diagonal print or a separate belt bow does not establish overlapping skirt panels and a knot made from those ends.',
 'Visible overlap and a knot do not prove adjustable fit, hidden-fastener absence or that the skirt can open in use.')
add('SF044_02','엉덩이와 허벅지에서 좁게 내려와 무릎 근처에 끝나는 같은 치마','selected skirt','wardrobe.skirt.width_distribution|wardrobe.skirt.hem_height',
 'The same skirt remains narrow alongside the hips and thighs~Its textile hem ends near the same wearer\u2019s knees',
 'selected skirt side edges>remain_narrow_along>same wearer hips and thighs~selected skirt hem>ends_near>same wearer knee landmarks',
 'A skirt that flares below the knees, a short crop or pleats alone does not establish this narrow contour and knee-level edge.',
 'Skirt contour does not establish pressure, comfort, body-size alteration or a measured ease value.')
add('SF046_01','겹친 치마 앞판 아래 별도로 읽히는 두 쇼츠 밑단','selected skirt-and-shorts arrangement','wardrobe.bottom.layer_topology|wardrobe.bottom.leg_opening_count',
 'A selected skirt panel overlaps the front of the lower outfit~Two separate shorts textile hems remain visible beneath that panel',
 'selected front skirt panel>overlaps>selected shorts front~selected shorts left hem>distinct_from>selected shorts right hem~selected shorts two hems>visible_below>selected front skirt panel',
 'One skirt edge, a lining fold or inferred concealed shorts cannot supply two independent short leg openings.',
 'The visible arrangement does not prove the skirt and shorts were manufactured as one skort; a hidden internal join remains metadata.')
add('SF047_03','같은 쇼츠의 두 다리 끝이 각 허벅지 윗부분에서 끝남','selected shorts','wardrobe.shorts.length|wardrobe.bottom.leg_opening_count',
 'The same shorts divide into two separate leg openings~Each short trouser hem ends near the top of its corresponding thigh',
 'selected shorts left hem>ends_near>same wearer left upper-thigh landmark~selected shorts right hem>ends_near>same wearer right upper-thigh landmark',
 'A short skirt edge or an image crop is not a pair of short trouser hems; length does not establish cutting history or frayed edges.')
add('SF049_01','같은 쇼츠의 두 밑단이 각각 무릎 근처에서 끝남','selected shorts','wardrobe.pants.length|wardrobe.bottom.leg_opening_count',
 'The selected shorts retain two distinct trouser leg openings~Both hems finish near the corresponding knee landmarks',
 'selected shorts left hem>ends_near>same wearer left knee~selected shorts right hem>ends_near>same wearer right knee',
 'A knee-length skirt has one enclosing hem rather than two trouser openings; width, fiber and fixed commercial length categories remain separate.')
add('SF050_01','같은 옷이 허리에서 몸통 가까이 따라가는 국소 맞음새','selected garment','wardrobe.fit.local_contact',
 'The selected garment follows the same torso at the waist with only a small visible cloth-to-body separation',
 'selected garment waist cloth>follows_close_to>same wearer waist contour',
 'A distant silhouette or a cinching belt without readable waist cloth does not establish local garment contact.',
 'The apparent fit does not establish negative ease, pressure, stretch, compression, body measurements or concealed support.')
add('SF050_04','같은 밀착 드레스 몸판에 넓은 띠 패널들이 수평으로 반복됨','selected fitted dress','wardrobe.fit.local_contact|wardrobe.bodice.band_structure',
 'The same fitted dress follows the existing torso~Broad cloth bands form repeated horizontal panel divisions across that dress body',
 'selected dress body>follows>same wearer torso~selected dress horizontal band panels>divide>selected dress body surface',
 'Printed stripes, a loose belt or a separate harness do not establish repeated broad cloth panels on the fitted dress.',
 'This visible banded construction does not establish compression, elasticity, body reshaping or individual band tension.')
add('SF053_02','같은 드레스가 엉덩이와 윗다리를 따라가다 무릎 아래에서 퍼짐','selected dress','wardrobe.silhouette.contour|wardrobe.silhouette.flare_start',
 'The selected dress follows the same hips and upper legs~Its skirt widens outward beginning below the knee landmarks',
 'selected dress upper skirt>follows>same wearer hips and upper legs~selected dress lower skirt>flares_below>same wearer knee landmarks',
 'A skirt flaring at or above the knees is another chosen variant; a fish tail, extra body appendage or pose change is not a garment flare.')
add('SF058_01','같은 상의의 고리 꽃 모티프가 열린 실 브리지로 이어짐','selected top fabric','wardrobe.textile.motif_connection|wardrobe.textile.loop_structure',
 'Looped floral yarn motifs occupy the selected top surface~Open yarn bridges visibly join one floral motif to its neighbor',
 'selected top floral yarn motif>joined_by>selected top open yarn bridge~selected top open yarn bridge>connects_to>neighboring floral yarn motif on same top',
 'A flat floral print, stitched flower on solid cloth or disconnected lace-like shapes do not supply the visible yarn-loop motifs and inter-motif bridges.',
 'The yarn appearance does not identify hand crochet, machine production, fiber content or the maker\u2019s process.')
add('SF059_03','같은 카디건의 앞판이 겹쳐 허리에서 타이로 묶임','selected cardigan','wardrobe.cardigan.front_overlap|wardrobe.cardigan.closure',
 'The same cardigan front panels cross at the waist~Tie ends continuing from those front panels meet in a waist knot',
 'selected cardigan first front panel>crosses_over>selected cardigan second front panel~selected cardigan first panel tie end>knotted_with>selected cardigan second panel tie end',
 'An open cardigan with parallel front edges or a detached belt knot does not establish two crossed cardigan fronts and their own ties.',
 'A visible knot does not prove adjustment range, hidden-fastener absence or that a front can open during wear.')
add('SF061_02','같은 슈러그의 어깨와 양팔을 연결하는 작은 뒤판','selected shrug','wardrobe.outer.coverage_topology|wardrobe.outer.back_panel_extent|wardrobe.outer.front_coverage_topology',
 'The selected shrug cloth covers the same shoulders and both arms~A small back panel of that shrug connects the two shoulder-and-arm sections~The same shrug front ends at its shoulder-and-arm edges with an open center between them',
 'selected shrug first shoulder-arm section>joined_by>selected shrug small back panel~selected shrug small back panel>connects_to>selected shrug opposite shoulder-arm section~selected shrug first front edge>separated_from>selected shrug opposite front edge',
 'A cropped top with a full front body, disconnected sleeve tubes or a broad coat back is a different coverage arrangement.',
 'The back connection cannot pass when hidden by a front-only view; no inner garment or exposed body amount is prescribed.')
add('SF062_03','이미 선언된 성인 착용자의 허리 높은 지점에서 끝나는 밀착 반팔 티','selected tee','wardrobe.fit.local_contact|wardrobe.sleeve.length|wardrobe.top.length',
 'On the already-declared adult wearer, the same tee has a fitted torso and two short sleeves~The tee hem ends high at that wearer\u2019s waist',
 'selected tee torso cloth>follows>declared adult wearer torso~selected tee sleeves>end_along>declared adult wearer upper arms~selected tee hem>ends_high_at>declared adult wearer waist',
 'An infant garment, a long loose tee or an image crop cannot replace the declared adult-owned fitted short tee.',
 'Adult context is a prerequisite, not an age transformation. The tee length adds no automatic exposed midriff or absent underwear.')
add('SF063_02','같은 소매의 어깨 모음에서 윗팔 위로 둥글게 부푸는 직물','selected sleeve','wardrobe.sleeve.gather_attachment|wardrobe.sleeve.volume_distribution',
 'The selected sleeve cloth gathers into its shoulder-head seam~The same sleeve forms a rounded puff above the upper arm',
 'selected sleeve gathered head>joins>selected garment shoulder seam~selected sleeve rounded cloth volume>rises_over>same wearer upper arm',
 'A bare shoulder silhouette, puffed hair or fullness only at a wrist cuff does not establish sleeve-head gathering and upper-arm volume.')
add('SF065_02','같은 드레스의 형태 잡힌 허리 아래로 부드럽게 처지는 치마','selected dress','wardrobe.dress.waist_shape|wardrobe.skirt.drape',
 'The same dress has a visibly shaped waist region~Its skirt cloth falls below that waist in soft continuous folds',
 'selected dress waist contour>joins_above>selected dress skirt~selected dress soft skirt folds>descend_from>selected dress waist region',
 'A separate top and skirt, a rigid skirt plane or a loose body without the selected waist shaping is a different garment state.',
 'The arrangement is one visible dress variant; it does not prove a daywear role, tea event, season performance or comfort.')
add('SF067_01','같은 드레스 앞판이 몸통을 사선으로 겹쳐 허리에서 묶임','selected dress','wardrobe.front.overlap|wardrobe.closure.tie_location|wardrobe.closure.topology',
 'The selected dress outer front panel crosses diagonally over its inner torso panel~Cloth tie ends of that dress meet in a visible waist knot',
 'selected dress outer front panel>overlaps_diagonally>selected dress inner front panel~selected dress first tie end>knotted_with>selected dress second tie end~selected dress waist knot>belongs_to>selected dress',
 'A diagonal seam without overlapped panels or an unrelated belt bow does not provide this dress-front overlap and same-dress knot.',
 'A visible overlap may be fixed; adjustable opening and hidden fastening remain unverified.')
add('SF068_02','같은 드레스가 어깨에서 헐겁게 내려오며 허리 폭은 거의 좁아지지 않음','selected dress','wardrobe.dress.width_distribution|wardrobe.fit.local_ease',
 'The same dress body falls loosely from its shoulder attachments~Its side boundaries show little narrowing at the waist',
 'selected dress body>descends_from>selected dress shoulder attachments~selected dress waist side boundaries>retain_similar_width_to>selected dress upper body',
 'A fitted waist and a high seam attached to a wide skirt are other variants; a loose shape does not establish a child\u2019s age, underwear role or hidden construction.')
add('SF069_02','같은 드레스 몸통과 치마에 이어져 읽히는 니트 루프','selected knit dress','wardrobe.textile.knit_structure|wardrobe.dress.surface_continuity',
 'Readable knitted loops occupy the selected dress torso cloth~The same looped surface continues onto that dress skirt cloth',
 'selected dress torso looped surface>continues_onto>selected dress skirt looped surface~selected dress skirt cloth>belongs_to>selected dress body',
 'A knitted top above a separate skirt or a loop-like print does not prove continuity across the same dress.',
 'Only visible loop paths are checked; exact gauge, stretch, fiber composition and machine-knit history remain metadata.')
add('SF071_01','별도 블라우스 바깥에 어깨끈과 앞판이 이어진 에이프런형 드레스','selected over-dress and separate blouse','wardrobe.layer.order|wardrobe.dress.overpanel_connection',
 'The selected apron-style dress front panel joins its own shoulder straps~That dress front and straps lie over a separate blouse',
 'selected over-dress front panel>joined_to>selected over-dress shoulder straps~selected over-dress front and straps>outside_of>selected separate blouse',
 'A blouse\u2019s decorative bib, a detached apron print or sleeves belonging to the dress itself cannot replace the declared over-dress and inner blouse boundaries.',
 'This selected layering establishes no profession, personality, social role or uniform status.')
add('SF072_02','짧은 밑단 위에 앞판 겹침과 견장이 남아 있는 같은 트렌치형 재킷','selected trench-style jacket','wardrobe.coat.front_overlap|wardrobe.coat.shoulder_tabs|wardrobe.coat.length',
 'The selected short jacket has overlapping front cloth panels~Distinct fabric tabs attach at its shoulders above the same jacket\u2019s short hem',
 'selected jacket outer front panel>overlaps>selected jacket inner front panel~selected jacket shoulder tabs>attached_to>selected jacket shoulders~selected jacket hem>ends_below>selected jacket front overlap and shoulder tabs',
 'A long coat, printed shoulder stripes or a separate belt cannot supply the selected short jacket\u2019s own overlap and shoulder tabs.',
 'The trench-style reference does not require a waist belt or establish waterproofing, wind resistance or a universal garment length.')
add('SF073_02','같은 블레이저 어깨 직물에 보이는 부드러운 처짐 주름','selected blazer','wardrobe.blazer.shoulder_drape',
 'The selected blazer shoulder cloth falls in soft folds around its own shoulder region',
 'selected blazer soft shoulder folds>belong_to>selected blazer shoulder cloth',
 'A smooth rigid shoulder cap, wrinkles on an inner shirt or a drooping arm does not supply the blazer cloth folds.',
 'Soft outer folds do not prove unlined, unpadded or unstructured interior tailoring.')
add('SF074_02','같은 재킷 앞판에 붙은 여러 개의 큰 패치 포켓','selected jacket','wardrobe.jacket.pocket_topology|wardrobe.jacket.pocket_scale|wardrobe.jacket.pocket_count',
 'Several large separate cloth patch pockets attach over the selected jacket front~Each pocket retains visible attached side and lower edges and a separate upper mouth',
 'selected jacket patch pocket side and lower edges>attach_to>selected jacket front panel~selected jacket patch pocket upper mouth>opens_above>same pocket cloth face',
 'Printed rectangles, a welt slit or pocket shapes on another garment do not establish applied front pockets.',
 'Visible pocket construction establishes no profession, military role, storage capacity or commercial jacket category.')
add('SF075_01','같은 재킷 몸판이 모인 허리 밑단과 커프스 위에서 살짝 부풂','selected jacket','wardrobe.outer.hem_gathering|wardrobe.sleeve.cuff_gathering|wardrobe.outer.volume_distribution',
 'The same jacket waist hem and cuffs gather into narrow edge bands~Loose jacket body and sleeve cloth billow slightly above those respective bands',
 'selected jacket body folds>gather_into>selected jacket waist hem band~selected jacket sleeve folds>gather_into>selected jacket corresponding cuff bands',
 'A loose straight jacket hem or gathered waist without matching cuffs is a different chosen variant.',
 'Gathered bands and billowing cloth do not require bomber military details or establish insulation, stretch or elastic composition.')
add('SF075_04','같은 얇게 보이는 연속 겉면에 후드가 붙은 가벼운 재킷','selected outer jacket','wardrobe.outer.shell_continuity|wardrobe.outer.edge_thickness_appearance|wardrobe.hood.attachment',
 'The selected outer jacket shows a continuous shell with thin-looking cloth edges~Its hood visibly joins the neck edge of that same jacket',
 'selected jacket shell edges>continuous_with>selected jacket shell panels~selected jacket hood base>joins>selected jacket neck edge',
 'A scarf over a jacket or a hood belonging to an inner sweatshirt is another owner; a bulky padded edge is a different surface appearance.',
 'Thin-looking edges do not prove actual mass, thickness, breathability, water resistance or wind protection.')
add('SF077_02','같은 바깥 직물 층이 고유 표면을 남기며 안쪽 옷 색을 투과함','selected outer and inner garments','wardrobe.layer.transmission|wardrobe.textile.visible_weave',
 'Fine crossing threads remain readable on the selected outer cloth~The inner garment color shows softly through that same outer layer',
 'selected outer crossing threads>form>selected outer cloth surface~selected inner garment color>visible_through>selected outer cloth',
 'A globally tinted image, a printed imitation of the inner garment or a fully opaque outer layer is not localized cloth transmission.',
 'This appearance does not identify voile, lawn, poplin, fiber content, GSM or actual weave manufacture beyond the readable crossing threads.')
add('SF078_01','같은 직물에서 부푼 좁은 띠와 평평한 띠가 번갈아 반복됨','selected garment fabric','wardrobe.textile.relief_pattern',
 'Raised puckered cloth strips alternate with flatter strips across the same fabric face',
 'selected fabric raised puckered strips>alternate_with>selected fabric flatter strips',
 'Flat printed stripes, random washing wrinkles or isolated seam puckering do not supply the repeated alternating relief on one cloth face.',
 'The relief does not establish the seersucker manufacturing method, fiber composition or thermal function.')
add('SF079_03','같은 반투명 소매가 선명한 접힘을 가진 둥근 부피를 유지함','selected sleeve','wardrobe.textile.transmission|wardrobe.textile.fold_shape|wardrobe.sleeve.volume_distribution',
 'The selected sleeve cloth transmits the surface beneath it~That same sleeve retains a rounded volume bounded by crisp folds',
 'surface beneath selected sleeve>visible_through>selected sleeve cloth~selected sleeve crisp folds>bound>selected sleeve rounded volume',
 'Soft collapsed drape alone or transparent skin without a cloth boundary does not supply this translucent rounded sleeve and crisp fold structure.',
 'The visible state does not establish organza, exact stiffness, fiber composition, fabric weight or tactile feel.')
add('SF080_03','별도 불투명 안감 위에서 읽히는 같은 바깥 망상 직물의 규칙적 격자','selected mesh outer and lining','wardrobe.textile.open_space_pattern|wardrobe.layer.order|wardrobe.layer.transmission',
 'A regular thread mesh grid remains readable on the selected outer panel~A separate solid lining is visible behind its openings',
 'selected outer mesh threads>bound>selected outer mesh regular openings~selected separate lining>lies_behind>selected outer mesh openings',
 'A grid print on solid cloth, a wall behind the person or inferred lining cannot replace mesh openings and a separate inner cloth layer.',
 'Grid appearance does not establish a manufacturing method, fiber or a universal mesh-versus-tulle size threshold.')
add('SF081_03','같은 저지형 의복 겉면에서 이어지는 작은 니트 루프','selected jersey-like garment','wardrobe.textile.surface_structure',
 'Small readable knitted loops continue across the same garment cloth face',
 'selected garment small loop rows>continue_across>selected garment cloth face',
 'Printed loop-like marks, sports-team jersey naming or a smooth blurred surface are not readable cloth loops.',
 'Loop appearance does not establish a particular fiber, measured gauge, stretch rate or the industrial knitting process.')
add('SF083_01','직물 고정점에서 내려와 같은 몸통을 따라 놓이는 길고 부드러운 드레이프','selected garment fabric','wardrobe.textile.drape|wardrobe.folds.attachment',
 'Long soft folds descend from the selected cloth attachment~The same folds settle along the existing torso surface',
 'selected garment long folds>descend_from>selected garment cloth attachment~selected garment long folds>settle_along>same wearer torso',
 'A detached scarf crease, rigid panel or hidden attachment cannot establish this connected drape path.',
 'Visible drape does not prove bias cutting, silk content, textile elasticity or a measured softness.')
add('SF085_01','같은 바탕 직물에서 도톰한 모티프와 반투명 영역이 번갈아 나타남','selected garment panel','wardrobe.textile.density_pattern|wardrobe.textile.motif_relief|wardrobe.textile.transmission',
 'Dense raised motifs alternate with translucent ground areas on the same cloth panel~The underlying cloth ground remains continuous through both areas',
 'selected panel dense raised motifs>alternate_with>selected panel translucent ground regions~selected panel underlying ground>continues_between>selected panel motif and translucent regions',
 'A flat opaque print, attached opaque motifs without a continuous ground or true cut holes does not provide the selected relief/transmission contrast.',
 'This visible contrast does not prove burnout, devore, fiber removal, laser cutting or any specific finish history.')
add('SF086_03','같은 직물을 여러 평행 봉제 줄이 모아 좁은 반복 밴드를 만듦','selected garment gathered band','wardrobe.stitching.row_pattern|wardrobe.folds.anchor_topology|wardrobe.folds.band_repeat',
 'Several parallel stitched rows cross the same cloth band~The cloth gathers directly into those repeated rows',
 'selected band parallel stitch rows>cross>selected garment cloth band~selected band cloth gathers>anchor_to>selected band parallel stitched rows',
 'Printed stitch stripes, natural wrinkles or one gathering seam does not establish multiple parallel stitched gathering rows.',
 'The visible rows do not prove elastic thread, actual stretch or a smocking process; the selected band may use other gathering techniques.')
add('SF087_02','같은 직물의 넓은 중앙 플리츠 면 양쪽을 마주 접힌 두 주름이 둘러쌈','selected garment pleat','wardrobe.pleats.direction|wardrobe.pleats.face_width',
 'Two opposing cloth folds meet around a broad central pleat face on the same garment',
 'selected pleat first fold>opposes>selected pleat second fold~selected pleat opposing folds>bound>selected pleat broad central cloth face',
 'A recessed inverted crease, ribbed knit or printed stripe does not supply two opposing folded cloth boundaries around the broad central face.',
 'Visible fold direction does not prove heat setting, pressing history or fiber composition.')
add('SF088_01','같은 블라우스 앞판에서 좁게 접혀 봉제된 여러 세로 핀턱','selected blouse','wardrobe.tucks.visible_structure|wardrobe.tucks.stitch_attachment',
 'Several very narrow folded ridges rise along the same blouse front~Visible stitch lines hold each small fold to that blouse cloth',
 'selected blouse narrow folded ridge>held_by>selected blouse corresponding stitch line~selected blouse narrow tucks>extend_along>selected blouse front panel',
 'A dart converging to an internal point, a joining princess seam, a lace strip or a flat printed line is a different construction.')
add('SF090_01','같은 의복 밑단에 봉합 경계로 붙은 별도 레이스 띠','selected garment','wardrobe.trim.connection|wardrobe.trim.layer_boundary',
 'A separate lace strip joins the same garment hem along a readable cloth attachment line~Its lace boundary remains distinct from the base garment cloth',
 'selected lace strip upper edge>attached_along>selected garment hem~selected lace strip>distinct_from>selected base garment cloth',
 'Lace printed on the garment, a lace layer belonging to another item or an unrelated scalloped edge does not supply the attached separate strip.',
 'The lace attachment does not prescribe scallops, eyelet embroidery, fiber content or hand manufacture unless independently selected.')
add('SF091_01','같은 바탕 원단 위에 별도 가장자리가 있는 직물 모티프가 붙음','selected garment ornament','wardrobe.ornament.attachment|wardrobe.ornament.layer_boundary',
 'A separate cloth motif lies attached over the selected base cloth~The motif has its own readable perimeter above that base surface',
 'selected separate cloth motif>attached_over>selected garment base cloth~selected motif perimeter>distinct_from>selected base cloth surface',
 'A flat floral print, real loose flower or embroidery threads without a separate cloth-piece perimeter is a different surface construction.',
 'Visible attachment does not specify stitching, adhesive, cutting history or fabrication process unless its own evidence is present.')
add('SF093_03','같은 의복 봉제선을 따라 붙은 좁게 솟은 파이핑','selected garment seam','wardrobe.trim.seam_route|wardrobe.trim.raised_profile',
 'A narrow raised piping ridge follows the same garment joining seam~That ridge remains attached along the seam path',
 'selected piping ridge>follows_and_attaches_to>selected garment joining seam',
 'A printed border, freestanding cord or distant stitch shadow is not an attached raised piping ridge following the cloth seam.',
 'This visible ridge does not prove a hidden cord core, manufacturing method or exact trim material.')
add('SF094_02','별도 상의 아래에서 부드럽게 모인 꽃무늬 치마','selected floral skirt and separate top','wardrobe.skirt.folds|wardrobe.print.motif|wardrobe.layer.order',
 'Floral motifs belong to the selected skirt cloth~That skirt falls in soft gathered folds beneath a separate top',
 'selected floral motifs>belong_to>selected skirt cloth~selected skirt gathered folds>lie_below>selected separate top',
 'Flowers on the blouse, a flat floral background or lace motifs belonging to another layer do not supply the declared floral gathered skirt.',
 'These item relations are one optional styling variant and do not prove romantic, coquette or feminine personality, age or behavior.',slot='garment_detail')
add('SF096_01','작은 꽃무늬 드레스의 퍼프 소매와 앞치마형 앞판','selected dress','wardrobe.print.motif_scale|wardrobe.sleeve.volume_distribution|wardrobe.dress.overpanel_connection',
 'Small floral motifs occupy the selected dress cloth~The same dress has rounded puff sleeves and a distinct apron-like front panel',
 'selected dress small floral motifs>belong_to>selected dress cloth~selected dress puff sleeves>join>selected dress shoulders~selected dress apron-like front panel>belongs_to>selected dress front',
 'A floral wall, an unrelated apron or ordinary sleeve folds cannot replace the flowered dress\u2019s own puff sleeves and front panel.',
 'This selected outfit variant establishes no rural residence, ethnicity, occupation, era or cottagecore lifestyle.',slot='garment_detail')
add('SF097_01','같은 착용자의 폴로 상의와 플리츠 치마·로퍼 조합','selected top skirt and shoes','wardrobe.top.collar|wardrobe.top.placket_extent|wardrobe.skirt.pleats|wardrobe.shoe.upper_structure|wardrobe.layer.item_combination',
 'The selected polo top has its own collar and short center-front opening~The same wearer pairs that top with a skirt of repeated cloth pleats~Distinct loafer shoes with continuous low uppers belong to the same outfit',
 'selected polo collar and short opening>belong_to>selected polo top~selected top>paired_on_same_wearer_with>selected pleated skirt~selected loafer shoes>worn_by>same wearer',
 'A tennis prop, school setting or polo logo does not supply the declared collar/opening, cloth pleats and loafer footwear.',
 'This optional combination does not establish school enrollment, tennis ability, wealth or uniform status; it is not a universal preppy definition.',slot='garment_detail')
add('SF098_01','같은 착용자의 별도 상의·레깅스와 낮은 스니커즈 조합','selected top leggings and sneakers','wardrobe.layer.item_combination|wardrobe.bottom.leg_tube_structure|wardrobe.shoe.upper_height',
 'The selected upper top remains a separate garment above the leggings~Two legging tubes follow the same legs~Low sneaker uppers stay below the same ankle landmarks',
 'selected upper top>separate_from>selected leggings~selected leggings left and right tubes>follow>same wearer corresponding legs~selected sneaker uppers>end_below>same wearer ankles',
 'A one-piece suit, a skirt hiding the legging boundaries or high boot shafts does not supply the selected separate top/leggings/low-sneaker arrangement.',
 'Sports-style is context for one item selection, not a pixel duty; appearance proves no athletic performance, moisture wicking or compression.',slot='garment_detail')
add('SF099_01','같은 착용자의 가로줄 상의·곧은 데님룩 바지와 플랫 조합','selected top trousers and flat shoes','wardrobe.print.stripe_direction|wardrobe.pants.leg_contour|wardrobe.textile.denim_appearance|wardrobe.shoe.heel_profile|wardrobe.layer.item_combination',
 'Horizontal stripes follow the selected top cloth~The same wearer pairs it with straight-sided denim-look trousers~Flat shoes retain low heel profiles beneath the same outfit',
 'selected top horizontal stripes>follow>selected top cloth~selected trouser side edges>remain_straight_along>selected trouser legs~selected flat shoes>worn_beneath>same wearer trouser hems',
 'Wall stripes, tapered trouser legs or a visibly high heel is a different declared item arrangement.',
 'Denim-look is appearance, not verified fiber or dye process; this combination proves no nationality, residence, price or sailing skill.',slot='garment_detail')
add('SF100_01','짧은 밀착 상의·낮은 허리 청바지와 짧은 스트랩 소형 숄더백','selected top jeans and shoulder bag','wardrobe.top.length|wardrobe.fit.local_contact|wardrobe.bottom.waistband_height|wardrobe.bag.size|wardrobe.bag.strap_length|wardrobe.bag.strap_attachment|wardrobe.layer.item_combination',
 'The selected fitted top has a short torso hem~The same jeans waistband lies low relative to the wearer\u2019s waist~A small bag hangs just below that wearer\u2019s shoulder from a short strap attached to both bag ends',
 'selected fitted top hem>ends_above>same wearer lower torso~selected jeans waistband>lies_low_relative_to>same wearer waist~selected bag first strap end>attached_to>selected bag first upper end~selected bag second strap end>attached_to>selected bag opposite upper end~selected small bag>hangs_below>same wearer shoulder',
 'A long loose top, high-waisted trousers or a long crossbody strap is a different outfit and bag path.',
 'This chosen combination does not define every Y2K variant or prescribe era, a body-proportion change, midriff exposure or a hidden layer absence.',slot='garment_detail')
add('SF101_03','같은 짧은 플리츠 치마 바깥을 가로지르는 스터드 벨트','selected belt and pleated skirt','wardrobe.accessory.belt_route|wardrobe.accessory.hardware_attachment|wardrobe.skirt.pleats|wardrobe.skirt.hem_height|wardrobe.layer.order',
 'Separate reflective stud-like pieces attach to the selected belt~That belt crosses outside the same short skirt waist~Repeated cloth pleats continue below the belt on that skirt~The same skirt hem ends above the corresponding knee landmarks',
 'selected belt stud-like pieces>attach_to>selected belt surface~selected belt>outside_of>selected pleated skirt waist~selected skirt pleats>continue_below>selected belt~selected skirt hem>ends_above>same wearer corresponding knee landmarks',
 'Printed metal dots, a detached chain or pleats on another skirt cannot supply the same belt attachments and belt-over-skirt arrangement.',
 'Stud appearance does not prove metal composition; style labels do not require sexual behavior, restraint, consent, exposure or a body change.',slot='garment_detail')
add('SF102_02','같은 상의의 넓은 목선과 소매에 처지는 부드러운 직물 주름','selected top','wardrobe.neckline.width|wardrobe.sleeve.drape',
 'The same top neckline opens widely across the upper torso~Soft cloth folds descend along that top\u2019s sleeves',
 'selected top neckline>spans_widely_across>same wearer upper torso~selected top soft sleeve folds>belong_to>selected top sleeves',
 'A low narrow neckline, torso folds or a hair drape does not supply the declared wide neckline and same-top sleeve folds.',
 'These cloth relations do not establish innocence, glamour, attraction, youth or body measurements.',slot='garment_detail')
add('SF103_03','선택한 바지 면에 한정한 차분한 회녹색','selected trousers','wardrobe.trousers.color',
 'Muted gray-green color occupies the selected trouser cloth regions',
 'muted gray-green color>belongs_to>selected trouser cloth surface',
 'Green background light, a plant beside the wearer or gray-green grading across the whole image is not assigned trouser color.',
 'No fixed RGB, Pantone match, measured color difference or universal spring trend is claimed.',slot='color')
add('SF103_06','선택한 상의 면에 한정한 옅고 부드러운 분홍색','selected top','wardrobe.top.color',
 'Pale soft pink color occupies the selected top cloth regions',
 'pale soft pink color>belongs_to>selected top cloth surface',
 'Pink facial blush, reflected pink light or a global grade is not assigned top color.',
 'No fixed RGB, Pantone match, measured color difference or universal spring trend is claimed.',slot='color')
add('SF103_09','선택한 카디건 면에 한정한 옅은 보라색','selected cardigan','wardrobe.cardigan.color',
 'Pale violet color occupies the selected cardigan cloth regions',
 'pale violet color>belongs_to>selected cardigan cloth surface',
 'A violet background or violet light across every surface is not a cardigan-owned color assignment.',
 'No fixed RGB, Pantone match, measured color difference or universal spring trend is claimed.',slot='color')
add('SF103_12','선택한 치마 면에 한정한 따뜻한 오프화이트','selected skirt','wardrobe.skirt.color',
 'Warm off-white color occupies the selected skirt cloth regions',
 'warm off-white color>belongs_to>selected skirt cloth surface',
 'Warm global white balance or an off-white wall does not establish color assigned to the skirt.',
 'No fixed RGB, Pantone match, measured color difference or universal spring trend is claimed.',slot='color')
add('SF104_02','같은 블라우스와 치마의 가까운 차분한 웜톤 관계','selected blouse and skirt','wardrobe.blouse.color|wardrobe.skirt.color|wardrobe.palette.item_relationship',
 'The selected blouse and skirt carry closely related muted warm tones~Their separate cloth boundaries remain readable between the two colors',
 'selected blouse muted warm tone>closely_related_to>selected skirt muted warm tone~selected blouse cloth boundary>distinct_from>selected skirt cloth boundary',
 'An identical hue on all background surfaces or strongly opposed saturated colors is a different color relation.',
 'Related tones are not compulsory identical hues; this relation changes only the two declared items and adds no measured color-difference threshold.',slot='color')
add('SF105_02','같은 직물에서 잎·줄기·꽃이 따로 읽히는 큰 보태니컬 모티프','selected garment print','wardrobe.print.motif|wardrobe.print.scale',
 'Leaves, stems and flowers form larger readable botanical motifs on the same cloth surface~The motifs follow that cloth\u2019s folds and boundaries',
 'selected print leaves stems and flowers>form>selected fabric botanical motifs~selected botanical motifs>follow>selected fabric folds and boundaries',
 'Small dot-like sprigs, real foliage behind the person or raised stitched flowers are different owners or surface constructions.',
 'Motif scale is relative appearance; no centimeter size, fiber, printing method or overall floral style is established.',slot='color')
add('SF106_02','같은 상의 원단을 따라 이어지는 밝고 어두운 가로 줄','selected top print','wardrobe.print.repeat_topology|wardrobe.print.stripe_direction|wardrobe.print.local_lightness',
 'Repeated horizontal light and dark stripes occupy the same top fabric~Each stripe continues with that fabric\u2019s folds',
 'selected top light stripes>alternate_horizontally_with>selected top dark stripes~selected top stripes>follow>selected top cloth folds',
 'Shadow bands, raised knit ribs or horizontal background stripes do not supply alternating light/dark stripes on the top itself.',
 'The pattern establishes no fiber, dye method, yarn-dyed process or global grade.',slot='color')
add('SF106_05','같은 원단에서 갈고리 끝을 가진 굽은 물방울 모티프가 반복됨','selected garment print','wardrobe.print.repeat_topology|wardrobe.print.motif',
 'Curved teardrop-shaped motifs with hooked tips repeat across the same cloth surface',
 'selected hooked teardrop motifs>repeat_across>selected garment cloth surface',
 'Simple round dots, straight droplets or a paisley-like object outside the garment is a different motif or owner.',
 'Visible motif shape establishes no ethnicity, origin, printing process or fixed palette.',slot='color')
add('SF107_03','같은 신발 양옆에 붙어 뒤꿈치 뒤로 도는 슬링백 끈','selected shoe','wardrobe.shoe.strap_route|wardrobe.shoe.strap_attachment',
 'The same shoe strap passes behind the corresponding heel~Its two ends attach to opposite sides of that shoe upper',
 'selected shoe strap first end>attaches_to>selected shoe upper first side~selected shoe strap second end>attaches_to>selected shoe upper opposite side~selected shoe strap>passes_behind>same wearer corresponding heel',
 'An ankle strap from a different shoe or a detached heel band does not establish the two same-shoe attachments and heel-back route.',
 'Hidden attachment endpoints are not a full pass; the route proves no comfort, support or material content.',slot='footwear')
add('SF107_06','같은 신발 밑창 둘레로 이어지는 로프처럼 꼰 겉면 띠','selected shoe','wardrobe.shoe.sole_surface|wardrobe.shoe.trim_route',
 'A rope-like braided surface layer runs around the same shoe sole edge',
 'selected shoe braided surface layer>runs_around>selected shoe sole edge',
 'A flat rope print, loose cord beside the foot or shoe laces above the upper is not the braided sole-edge layer.',
 'Rope-like appearance does not identify jute, raffia or other real fibers, a weaving process or sole performance.',slot='footwear')
add('SF108_02','같은 신발 밑창 위로 발을 덮는 분리된 메시 갑피','selected shoe','wardrobe.shoe.upper_structure|wardrobe.shoe.upper_sole_connection',
 'A visible thread mesh upper spans the corresponding foot~That upper joins the same shoe sole above its boundary',
 'selected shoe mesh upper>spans_over>same wearer corresponding foot~selected shoe mesh upper lower edge>joins>selected shoe sole upper edge',
 'A net stocking over a different shoe, a mesh print or detached net floating above the foot cannot supply the same mesh upper-to-sole join.',
 'The mesh appearance does not establish fiber, mesh manufacturing process or a universal mesh opening-size threshold.',slot='footwear')
add('SF109_01','같은 다리의 무릎 바로 아래에서 끝나는 양말 윗단','selected sock','wardrobe.hosiery.hem_height',
 'The selected sock textile upper edge ends just below the corresponding knee landmark',
 'selected sock upper textile edge>ends_below>same wearer corresponding knee',
 'A boot shaft, a knee-level picture crop or a shadow band is not the actual sock top edge.',
 'Observed length does not establish denier, fiber, compression or hidden garter support.',slot='wearable_accessory')
add('SF109_04','같은 다리 둘레에 붙어 이어지는 구분된 네트 조직','selected legwear','wardrobe.hosiery.surface|wardrobe.hosiery.wrap_topology',
 'A distinct thread net pattern follows the same legwear around the corresponding leg',
 'selected legwear net thread paths>wrap_around>same wearer corresponding leg',
 'A flat dark grid behind the leg, patterned skin or an opaque grid print without thread openings is another surface construction.',
 'A net appearance does not establish exact denier, fiber, support function or the absence of an underlying lining.',slot='wearable_accessory')
add('SF110_02','같은 머리 꼭대기를 가로지르는 별도 굽은 머리띠','selected headband','accessory.headband.route',
 'A separate curved headband crosses the top of the same head~Its band remains distinct from the surrounding hair strands',
 'selected curved headband>crosses_over>same wearer head top~selected headband surface>distinct_from>same wearer surrounding hair',
 'A hair braid, garment ribbon or a visor\u2019s open space does not supply a distinct curved headband crossing the head.',
 'The headband route does not establish exact accessory material or silk fiber content.',slot='wearable_accessory')
add('SF111_02','가방 양끝에 붙은 짧은 스트랩으로 같은 어깨 바로 아래 매달린 소형 백','selected shoulder bag','wardrobe.bag.size|wardrobe.bag.strap_length|wardrobe.bag.strap_attachment|wardrobe.bag.position',
 'A small bag hangs close below the same shoulder~A short strap joins both upper ends of that bag and passes over the shoulder',
 'selected bag strap first end>attaches_to>selected bag first upper end~selected bag strap second end>attaches_to>selected bag opposite upper end~selected bag short strap>passes_over>same wearer shoulder~selected small bag>hangs_close_below>same wearer shoulder',
 'A long crossbody route, a dangling unattached handle or a bag below the opposite hip is a different arrangement.',
 'This visible path does not prove material composition, load-bearing performance, tactile feel or a hidden strap attachment.',slot='wearable_accessory')
add('SF112_03','같은 가터 끈의 끝 클립이 스타킹 윗밴드에 붙은 연결','selected garter strap and stocking','wardrobe.accessory.connection_topology|wardrobe.hosiery.clip_attachment',
 'The selected garter strap ends in a visible clip~That same clip grips the selected stocking top band',
 'selected garter strap lower end>joins>selected garter clip~selected garter clip>attached_to>selected stocking upper band',
 'A decorative thigh band, loose clip or strap ending beside the stocking does not supply the required strap-to-clip-to-stocking path.',
 'A visible clip connection does not prove support force, restraint, consent, sexual action or hidden underwear state.',slot='wearable_accessory')
add('SF113_02','별도 불투명 안쪽 상의 위로 자기 조직을 남긴 채 투과하는 겉셔츠','selected outer shirt and inner top','wardrobe.layer.order|wardrobe.layer.revealed_surface|wardrobe.textile.transmission|wardrobe.textile.surface',
 'The selected sheer outer shirt retains readable cloth texture~A separate solid inner top is visible through that same outer shirt',
 'selected sheer shirt texture>belongs_to>selected outer shirt~selected separate inner top>visible_through>selected outer shirt',
 'An opaque printed imitation, skin-colored solid insert or inner top shown only beside the shirt cannot replace cloth transmission through the declared outer shirt.',
 'The visible transmitted surface remains the actual inner top; the state adds no automatic skin exposure or hidden layer absence.')
add('SF114_02','열린 겉옷 안에서 드레스로 읽히는 별도 슬립','selected slip dress and open outer layer','wardrobe.layer.revealed_garment|wardrobe.layer.order|wardrobe.outer.front_opening',
 'The selected slip forms a separate visible dress with its own cloth boundaries~Open front edges of an outer garment lie outside that dress',
 'selected slip dress>inside_of>selected open outer garment~selected outer first front edge>separates_from>selected outer second front edge~selected slip dress cloth boundaries>distinct_from>selected outer garment edges',
 'A camisole that ends above a separate skirt or a bra hidden beneath a closed outer top is a different garment arrangement.',
 'Lingerie-style is a styling context, not proof that a real bra or concealed underwear exists or is absent; no sexual behavior is prescribed.')
add('SF117_01','같은 카디건의 위쪽 단추 하나는 잠겼고 그 아래 앞판 경계는 벌어짐','selected cardigan','wardrobe.closure.current_state|wardrobe.cardigan.front_edge_separation',
 'One selected upper cardigan button is fastened across the two front edges~Those same front edges separate below that button',
 'selected cardigan upper button>fastens_together>selected cardigan paired front edges~selected cardigan front edges below upper button>separate_from_each_other>selected cardigan lower opening',
 'A decorative button on one panel, a fully closed lower front or two unrelated cardigan edges does not provide the shared upper fastening and lower separation.',
 'Only visible current closure state is claimed; unseen button states, adjustment, underwear absence and exposure remain separate.')
add('SF118_02','같은 착용자의 짧은 밀착 상의와 길고 넓은 두 바지 다리의 대비','selected top and trousers','wardrobe.top.length|wardrobe.fit.local_contact|wardrobe.pants.length|wardrobe.pants.leg_width|wardrobe.layer.proportion_relationship',
 'The same wearer has a short fitted top with its own hem~Separate trousers form two long wide cloth legs beneath that top',
 'selected short fitted top>paired_on_same_wearer_with>selected long wide trousers~selected top hem>distinct_from>selected trouser waistband~selected trousers left and right legs>extend_below>selected top hem',
 'A one-piece garment, long loose top or narrow cropped trouser legs is a different declared garment-proportion arrangement.',
 'Garment proportion contrast does not change actual body proportions, height, body measurements or hidden fit performance.')
all_drafts=sorted(json.loads((RESEARCH/'candidate-drafts.json').read_text())['drafts'],key=lambda d:d['draft_id'])
mine=[d for i,d in enumerate(all_drafts) if i%3==1]
cards={c['id']:c for c in json.loads((RESEARCH/'semantic-cards.json').read_text())['cards']}
terms={t['term_id']:t for t in json.loads((RESEARCH/'term-plan.json').read_text())['terms']}
sources={s['id']:s for s in json.loads((RESEARCH/'sources.json').read_text())['sources']}
reuse={
 'SF052_01':{'candidate_file':'photo_prompt_clothing_structure_extension.json','slot':'wardrobe_style','candidate_id':'clt_ct017_v1','profile_file':'photo_prompt_visual_obligations_clothing_structure.json','profile_id':'clothing_ct017_v1','decision':'enrich','paraphrases':['The same skirt widens gradually from its waist edge toward the hem.'],'reason':'Existing clt_ct017_v1 explicitly states waist-to-hem gradual widening on one skirt, equivalent to the draft\u2019s skirt upper-edge-to-hem widening. Its existing profile checks that same relation. Add only a positive equivalent same-skirt paraphrase; retain IDs, effects, activation and gates.'},
 'SF055_01':{'candidate_file':'photo_prompt_clothing_structure_extension.json','slot':'wardrobe_style','candidate_id':'clt_ct005_v1','profile_file':'photo_prompt_visual_obligations_clothing_structure.json','profile_id':'clothing_ct005_v1','decision':'enrich','paraphrases':['A short flared peplum attaches at the waist of the same top bodice.'],'reason':'Existing clt_ct005_v1 is a short flared peplum attached at the bodice waist, matching the draft\u2019s short flared extension attached around the top waist. The native gate already requires the attachment on its bodice owner. Add only a synonymous positive owner-bound paraphrase, without broadening to oversized or boxy alternatives.'},
 'SF056_02':{'candidate_file':'photo_prompt_textile_surface_extension.json','slot':'surface_material','candidate_id':'clt_ct087_v1','profile_file':'photo_prompt_visual_obligations_textile_surface.json','profile_id':'clothing_ct087_v1','decision':'reuse','reason':'Existing vertical rib-knit ridges separated by recessed channels already encode the draft\u2019s raised vertical ribs on one knit surface. This is surface relief and repeated topology; no new loop gauge, fiber or stretch duty is needed. Keep the existing source and ID unchanged.'},
 'SF092_01':{'candidate_file':'photo_prompt_ornament_structure_extension.json','slot':'garment_detail','candidate_id':'orn_gd41','profile_file':'photo_prompt_visual_obligations_ornament_structure.json','profile_id':'orn_profile_gd41','decision':'reuse','reason':'Existing orn_gd41 explicitly has opposed eyelet rows on two panels, one continuous crossing lace and passage through visible eyelet openings. Those components and existing native gates cover the single alternating lace route in the draft. Retain the optional bundle/profile boundary and the existing IDs unchanged.'}
}
expected={d['draft_id'].replace('SPR_DRAFT_','') for d in mine}
assert len(mine)==94 and expected==set(specs)|set(reuse), (len(specs),sorted(expected-(set(specs)|set(reuse))),sorted((set(specs)|set(reuse))-expected))
assert not(set(specs)&set(reuse))

# Review same-source lexical leads as candidates for equivalence, never as definitions.
local_candidates=[]
for filename in sorted({d['candidate_file_proposal'] for d in mine}|{r['candidate_file'] for r in reuse.values()}):
    x=json.loads((ASSETS/filename).read_text())
    for slot,rows in x['slots'].items():
        for c in rows:local_candidates.append((filename,slot,c))
stop={'the','a','an','of','to','same','with','and','on','its','in','from','at','has','have','along','visible','selected','wearer'}
def tokens(text):return set(re.findall(r'[a-z]+',text.casefold()))-stop
def review_leads(d):
    target=tokens(d['en'])
    rows=sorted([(len(target&tokens(c['en']))/max(1,len(target|tokens(c['en']))),n,sl,c) for n,sl,c in local_candidates if n==d['candidate_file_proposal']],key=lambda r:r[0],reverse=True)[:3]
    return [{'candidate_file':n,'slot':sl,'candidate_id':c['id'],'en':c['en'],'record_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()} for score,n,sl,c in rows]

def route_slot(filename,spec):
    if spec['slot']:return spec['slot']
    if 'textile_surface' in filename:return 'surface_material'
    if 'accessory_structure' in filename:return 'wearable_accessory'
    if 'color_relations' in filename:return 'color'
    return 'garment_detail'
allowed_dimensions={'concept','subject','identity','count','age','role','species','appearance','pose','body_geometry','expression','action','event','setting','relationship','sexual_tone','style','reference_use','viewer_outcome','text','format','framing','composition','lighting','camera','color','material','timing','atmosphere','character_response'}
groups={}
decisions=[]; evidence=[]; gates=[]
for draft in mine:
    key=draft['draft_id'].replace('SPR_DRAFT_',''); card=cards[draft['card_id']]
    leading=review_leads(draft)
    if key in reuse:
        r=reuse[key]
        ca=next(c for n,sl,c in local_candidates if n==r['candidate_file'] and sl==r['slot'] and c['id']==r['candidate_id'])
        payload=json.loads((ASSETS/r['profile_file']).read_text()); pr=next(p for p in payload['profiles'] if p['id']==r['profile_id'])
        validate_visual_profile_source(pr)
        decision={k:r[k] for k in ('decision','candidate_id','profile_id','reason')}
        decisions.append({'draft_id':draft['draft_id'],**decision,'source_ids':draft['source_ids']})
        evidence.append({'draft_id':draft['draft_id'],'authorship':'existing_equivalent_visible_relation','research_sentence':draft['en'],'card_id':card['id'],'source_records':[sources[i] for i in draft['source_ids']], 'term_ids':draft['term_ids'],'reused_candidate_file':r['candidate_file'],'reused_profile_file':r['profile_file'],'candidate_record_sha256':hashlib.sha256(json.dumps(ca,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'profile_record_sha256':hashlib.sha256(json.dumps(pr,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'reviewed_leads':leading,'reason':r['reason'],'native_gate_ids':[g['id'] for g in compile_visual_profile(pr)['render_gates']]})
        if r['decision']=='enrich':
            group_key=(r['candidate_file'],r['slot'],r['profile_file'])
            group=groups.setdefault(group_key,{'candidate_file':r['candidate_file'],'slot':r['slot'],'candidates':[],'profile_file':r['profile_file'],'profiles':[],'context_extensions':[]})
            group['context_extensions'].append({'candidate_id':r['candidate_id'],'paraphrases':r['paraphrases']})
        continue
    spec=specs[key]; filename=draft['candidate_file_proposal']; slot=route_slot(filename,spec); profile_file=card['route_profiles'][0]
    if not (ASSETS/filename).exists() or not (ASSETS/profile_file).exists():raise ValueError('unregistered proposed filename')
    if slot not in json.loads((ASSETS/filename).read_text())['slots']:raise ValueError('new slot forbidden')
    sf,number=key.split('_');variant=int(number)
    cid=f'spf_{sf.lower()}_{variant}';pid=f'spring_{sf.lower()}_{variant}'
    components=spec['components']
    en='; '.join(components)+'.'
    dimension='color' if slot=='color' else 'appearance'
    effects=[{'dimension':dimension,'target':'main_subject','property':prop} for prop in spec['props']]
    relations=[{'id':'existing_wearer_scope','type':'belongs_to_existing_wearer','subject':spec['owner'],'object':'main_subject'}]
    relations.extend({'id':f'{sf.lower()}_{variant}_relation_{i}','type':kind,'subject':subj,'object':obj} for i,(subj,kind,obj) in enumerate(spec['edges'],1))
    candidate={'id':cid,'ko':spec['ko'],'en':en,'weight':0.35,'aliases':[spec['ko'],en], 'keywords':[spec['ko'],*components],'embedding_text':' | '.join([spec['ko'],spec['owner'],*components]),'concept_units':components,'relations':relations,'tags':['clothing'],'for_any':['human'],'affected_dimensions':[dimension],'affected_properties':effects,'core_assertion_discovery':True}
    if key in {'SF040_04','SF062_03'}:candidate['requires_primary_any_tags']=['adult','성인']
    authored=[]
    for i,component in enumerate(components,1):
        gate_id=f'vo_{pid}_{i}'
        authored.append({'id':f'component_{i}','match_terms':[component],'evidence_field':f'component_{i}_phrase','evidence_terms':[component],'min_content_words':3,'instruction':f'On the existing {spec["owner"]} of the declared wearer, keep this selected relation visible: {component}.','render_gate':{'id':gate_id,'review_scale':'native','description':f'At native resolution, verify that {component[0].lower()+component[1:]}. Trace the stated owner and both endpoints or cloth boundaries. Every named attachment, landmark or layer must be readable; cropped, blurred or occluded required parts are UNOBSERVABLE_NOT_PASS.'}})
        gates.append(gate_id)
    claims=[
      'This is one selected visible variant. Other terms or members of the related term family remain alternatives, not cumulative requirements.',
      'Bind every selected item, body landmark and attachment to the existing declared wearer; no candidate creates a new person or alters identity, age, body measurements, pose, camera or background.',
      'Visible cloth appearance does not establish fiber composition, hidden padding, internal support, process history, performance, tactile feel or absence of concealed garments.',
      'A native gate requires the actual declared owner and the relevant boundaries or connection endpoints in the saved image; a label, prompt audit or similar nearby item is insufficient.'
    ]
    if spec['claim']:claims.append(spec['claim'])
    profile={'id':pid,'category':'owner_bound_spring_garment_variant','activation':{'exact_terms':[en,spec['ko']],'requires_adult_character':key in {'SF040_04','SF062_03'},'semantic_discovery_requires_component_evidence':True,'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_selected_variant','any_terms':[en,spec['ko']]}]}},'semantics':{'definition':en,'paraphrase_examples':[f'Observable {spec["owner"]}: '+ '; '.join(components)],'visual_components':components,'contrast_examples':[spec['contrast']],'claim_limits':claims},'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':authored},'concept_candidate':{'concept_terms':[spec['ko'],*components],'core_assertion_discovery':True,'affected_dimensions':[dimension],'affected_properties':effects},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':[spec['contrast']]}
    validate_candidate_entries({'slots':{slot:[candidate]}},allowed_dimensions)
    validate_visual_profile_source(profile)
    group_key=(filename,slot,profile_file)
    group=groups.setdefault(group_key,{'candidate_file':filename,'slot':slot,'candidates':[],'profile_file':profile_file,'profiles':[],'context_extensions':[]})
    group['candidates'].append(candidate);group['profiles'].append(profile)
    reason=f'New narrow visible variant with explicit existing-owner and endpoint relations. The reviewed lexical leads do not supply this complete selected variant without adding or omitting a condition. Scope only {", ".join(spec["props"])}; reject this confusion: {spec["contrast"]}'
    decisions.append({'draft_id':draft['draft_id'],'decision':'new','candidate_id':cid,'profile_id':pid,'source_ids':draft['source_ids'],'reason':reason})
    nodes=list(dict.fromkeys([spec['owner'],'main_subject',*[n for edge in spec['edges'] for n in (edge[0],edge[2])]]))
    evidence.append({'draft_id':draft['draft_id'],'authorship':'agent_authored_single_visible_variant','research_sentence':draft['en'],'card_id':card['id'],'term_ids':draft['term_ids'],'source_records':[sources[i] for i in draft['source_ids']],'source_support_scope':card['source_support_scope'],'term_inventory_status':'Original term provenance stays in this evidence sidecar; runtime is only the abstracted selected geometry.', 'authored_candidate_id':cid,'authored_profile_id':pid,'variant_graph':{'owner':spec['owner'],'wearer':'main_subject','nodes':nodes,'relations':relations,'positive_visible_components':components},'affected_properties':effects,'omitted_proposed_effects':[p for p in draft['property_path_proposals'] if p not in spec['props']],'scope_review':spec['claim'] or 'The authored property set binds only effects present in these selected clauses; the broader family proposal is not inherited.', 'reviewed_leads':leading,'contrast':spec['contrast'],'native_gate_ids':[c['render_gate']['id'] for c in authored],'index':'not_integrated','retrieval':'not_run','prompt':'core_frozen_before_research_access','runtime':'not_published','pixel':'not_run','user_acceptance':'not_requested'})
fragment={'domain_writes':list(groups.values()),'decisions':decisions,'evidence':evidence}
assert len(decisions)==94 and len({d['draft_id'] for d in decisions})==94
assert len(gates)==len(set(gates))
serialized=json.dumps(fragment['domain_writes'],ensure_ascii=False)
for forbidden in ['http://','https://','source_ids','SPR_DRAFT_','S00','original_description','research_sentence','reviewed_leads','source_records','"property": "metadata.']:
    assert forbidden not in serialized, forbidden
newids=[c['id'] for g in fragment['domain_writes'] for c in g['candidates']]
assert len(newids)==len(set(newids))==90
# All writes stay in the arm; this file is a fragment, not a source installation.
raw=(json.dumps(fragment,ensure_ascii=False,indent=2)+'\n').encode()
(BASE/'data-fragment.json').write_bytes(raw)
summary={'assigned_count':len(mine),'new_candidates':len(newids),'new_profiles':sum(len(g['profiles']) for g in fragment['domain_writes']),'decisions':{d:sum(r['decision']==d for r in decisions) for d in ['new','enrich','reuse','metadata']},'native_gate_count':len(gates),'source_profile_compilation':'pass','candidate_relations_and_property_scope_structure':'pass','runtime_source_provenance_exclusion':'pass','new_slots':0,'shared_source_mutations':0,'generation_invocations':0,'fragment_sha256':hashlib.sha256(raw).hexdigest(),'fragment_path':str(BASE/'data-fragment.json')}
(BASE/'fragment-validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
