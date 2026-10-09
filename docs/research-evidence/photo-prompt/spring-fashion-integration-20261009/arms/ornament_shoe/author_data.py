from pathlib import Path
import json,hashlib,sys,collections
B=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
R=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009')
AS=ROOT/'skills/photo-prompt-image-generator/assets'
D={d['draft_id'].replace('SPR_DRAFT_','').lower():d for d in json.loads((B/'assigned_drafts.json').read_text())}
CARDS={x['id']:x for x in json.loads((R/'semantic-cards.json').read_text())['cards']}
TERMS={x['term_id']:x for x in json.loads((R/'term-plan.json').read_text())['terms']}
SOURCES={x['id']:x for x in json.loads((R/'sources.json').read_text())['sources']}
ROWS={}
def a(key,ko,owner,parts,paths,edges,contrast,slot=None):
 assert key in D and key not in ROWS,key
 ROWS[key]={'ko':ko,'owner':owner,'parts':parts,'paths':paths,'edges':edges,'contrast':contrast,'slot':slot}
# Geometry is authored per selected sentence, not imported from family blueprints.
a('sf002_02','얕은 수평 중앙을 가진 넓은 상의 목선','top',
 ["the selected top has a wide neckline spanning between the shoulders","its central neckline edge is shallow and almost horizontal"],
 ['wardrobe.neckline.width','wardrobe.neckline.contour','wardrobe.neckline.depth'],
 [('spans_between','top.neckline.ends','wearer.shoulders'),('has_contour','top.neckline.center','shallow_horizontal_edge')],
 'A wide V opening has a different central contour; width does not imply an off-shoulder top.')
a('sf004_01','수평 바닥에 양쪽 세로 변이 연결되는 상의 목선','top',
 ["the top neckline has a straight horizontal lower edge","two upright side edges join the ends of that same lower edge"],
 ['wardrobe.neckline.contour'],
 [('joined_to','top.neckline.lower_edge','top.neckline.side_edges')],
 'A rounded U edge or two slopes meeting in a V does not form this three-sided opening.')
a('sf006_01','서로 다른 앞판의 사선 겹침으로 만드는 V 목선','top',
 ["two distinct top front panels overlap diagonally","the upper boundaries of those overlapping panels form one V-shaped neckline"],
 ['wardrobe.front.overlap','wardrobe.neckline.contour'],
 [('overlaps','top.front.outer_panel','top.front.under_panel'),('forms','top.front.panel_upper_edges','top.neckline.v_shape')],
 'A V cut into one uninterrupted front panel does not show the two-panel overlap; visible overlap does not prove an adjustable wrap closure.')
a('sf008_01','같은 목선 직물이 앞에서 늘어지는 U형 접힘','top',
 ["fabric continuous with the top neckline hangs across the front","the hanging neckline fabric forms a soft U-shaped lower fold"],
 ['wardrobe.neckline.drape'],
 [('continuous_with','top.neckline.hanging_fabric','top.neckline.attachments'),('curves_below','top.neckline.fold_bottom','top.neckline.attachments')],
 'A necklace, scarf or detached ruffle cannot replace fabric continuous with this neckline.')
a('sf010_01','왼쪽 어깨를 잇고 오른쪽 어깨를 여는 상의','top',
 ["the same top extends across the wearer's left shoulder","the top upper boundary leaves the wearer's right shoulder open"],
 ['wardrobe.shoulder.support_topology','wardrobe.shoulder.opening'],
 [('crosses','top.left_support','wearer.left_shoulder'),('ends_below','top.right_upper_edge','wearer.right_shoulder')],
 'An enclosed shoulder cutout or a symmetrical off-shoulder edge is a different support topology.')
a('sf012_01','목선 아래에 둘러싸인 작은 상의 개구부','top',
 ["a small opening lies below the neckline of the same top","a continuous fabric rim encloses that opening"],
 ['wardrobe.opening.location','wardrobe.opening.topology'],
 [('below','top.small_opening','top.neckline'),('encloses','top.opening.fabric_rim','top.small_opening')],
 'A skin-colored patch, translucent panel or open hem has a different boundary; the visible surface behind the opening is not prescribed.')
a('sf014_01','앞뒤 몸판을 연결하는 넓은 어깨 직물','tank_top',
 ["broad fabric bridges extend over the tank top wearer's shoulders","each bridge connects the same tank front to its back"],
 ['wardrobe.strap.width','wardrobe.strap.attachment','wardrobe.sleeve.presence'],
 [('connects','tank_top.front','tank_top.shoulder_bridges'),('connects','tank_top.shoulder_bridges','tank_top.back')],
 'Thin cords, necklace strands and an independent shoulder accessory are different owners.')
a('sf015_01','앞뒤 부착점을 잇는 두 가는 어깨끈','top',
 ["two narrow straps attach to the selected top front","each strap passes over a shoulder and reaches the same top back"],
 ['wardrobe.strap.width','wardrobe.strap.attachment','wardrobe.strap.route'],
 [('attached_to','top.narrow_straps.front_ends','top.front'),('runs_over','top.narrow_straps','wearer.shoulders'),('attached_to','top.narrow_straps.back_ends','top.back')],
 'A painted line or necklace lacks the same-garment attachment endpoints; fixed strap width in millimeters is unspecified.')
a('sf016_02','등에서 서로 교차하는 같은 상의의 두 끈','top',
 ["two straps belong to the same top and span the back","the two strap paths cross in a visible X over that back"],
 ['wardrobe.back.strap_topology'],
 [('belongs_to','top.back.straps','top'),('crosses_over','top.back.strap_a','top.back.strap_b')],
 'Parallel straps and straps converging into one central join are separate variants; front-only pixels cannot verify a back crossing.')
a('sf018_01','어깨 연결과 하단 옆 매듭 사이가 열린 상의 옆','top',
 ["the top retains an upper shoulder connection and a lower side tie","an open side interval lies between those two same-top connections"],
 ['wardrobe.side.opening','wardrobe.shoulder.support_topology','wardrobe.closure.tie_location'],
 [('between','top.side.open_interval','top.upper_shoulder_and_lower_side_tie'),('belongs_to','top.side.tie','top')],
 'A deep but bounded armhole does not create the same side opening; athletic ability and muscle dimensions are unrelated.')
a('sf019_02','등 중앙 매듭으로 이어지는 상의 뒷판 두 끈','top',
 ["two ties start at the top back edges","those ties meet in a visible knot at the center back"],
 ['wardrobe.closure.tie_location','wardrobe.closure.connection'],
 [('attached_to','top.back.ties','top.back_edges'),('joins','top.back.tie_knot','top.back.tie_ends')],
 'A sewn decorative bow with detached tails does not establish a connection between the back edges; adjustability remains unproven.')
a('sf021_01','어깨 끝까지만 덮는 짧은 블라우스 소매','blouse',
 ["a short sleeve attaches at the blouse shoulder","the sleeve lower edge ends just over the wearer's shoulder tip"],
 ['wardrobe.sleeve.length','wardrobe.sleeve.attachment'],
 [('attached_to','blouse.short_sleeve','blouse.shoulder'),('ends_at','blouse.short_sleeve.hem','wearer.shoulder_tip')],
 'A broad flaring sleeve or an unattached shoulder ornament is a different structure; the underarm surface is not inferred.')
a('sf022_02','세로 채널과 앞 여밈이 보이는 몸판','corset_style_top',
 ["vertical channels run within the corset-style top bodice","a constructed closure joins the two edges at that top front"],
 ['wardrobe.bodice.visible_channels','wardrobe.closure.topology','wardrobe.closure.location'],
 [('within','corset_style_top.vertical_channels','corset_style_top.bodice'),('joins','corset_style_top.front_closure','corset_style_top.front_edges')],
 'Vertical paint stripes do not form channels; visible casings do not prove internal rigid stays or compression.')
a('sf024_02','삼각 패널과 좁은 하단 밴드가 연결된 브라렛','bralette',
 ["soft triangular bralette panels form the upper garment","the lower panel edges join a narrow continuous band"],
 ['wardrobe.bra.panel_structure','wardrobe.bra.lower_band'],
 [('joins','bralette.triangular_panels.lower_edges','bralette.lower_band')],
 'Cup padding, wire, support performance and exact breast dimensions are not determined by triangular panel appearance.')
a('sf026_01','곡선 컵 절개 아래로 연속되는 상의 몸판','top',
 ["separate curved cup seams divide the selected top front","the lower cup boundaries connect to a continuous lower bodice"],
 ['wardrobe.cup.seaming','wardrobe.bodice.panel_connection'],
 [('divides','top.curved_cup_seams','top.front_panels'),('joins','top.cup_lower_edges','top.lower_bodice')],
 'Natural skin contour and folded fabric shadows are not cup seams; metal underwire and padding are not visible claims.')
a('sf028_01','밀착 몸판 패널을 따라 이어지는 좁은 세로 케이싱','bodice',
 ["several narrow raised-edged casings run vertically along the bodice panels","the fitted garment surface stays continuous between those casings"],
 ['wardrobe.bodice.visible_channels','wardrobe.fit.local_contact'],
 [('runs_along','bodice.vertical_casings','bodice.panels'),('between','bodice.continuous_surface','bodice.vertical_casings')],
 'Rib knitting, flat drawn stripes and a single seam are different surface structures; hidden support material is unscored.')
a('sf030_01','가슴 아래에서 위아래 몸판을 잇는 연속 봉제선','bodice',
 ["a continuous seam lies directly beneath the wearer's bust","that seam connects upper and lower panels of the same bodice"],
 ['wardrobe.bodice.seam_height','wardrobe.bodice.panel_connection'],
 [('below','bodice.panel_join','wearer.bust'),('joins','bodice.panel_join','bodice.upper_and_lower_panels')],
 'A top hem, skin gap or belt is a different boundary; this seam alone does not establish an empire skirt join.')
a('sf032_01','높은 허리단 위의 짧은 상의와 좁은 의복 간격','top_and_lower_garment',
 ["the short top hem ends just above the same wearer's high waistband","a narrow interval separates that top hem from the lower garment waistband"],
 ['wardrobe.top.hem_height','wardrobe.lower.waistband_height','wardrobe.coverage.midriff_gap'],
 [('above','top.hem','lower_garment.high_waistband'),('separates','garment_gap','top.hem_and_lower_garment.waistband')],
 'The interval does not automatically expose the navel or establish a missing hidden layer; wearer proportions remain unchanged.')
a('sf033_01','상의 앞판에서 이어져 한 매듭으로 만나는 두 끝','top',
 ["two fabric ends remain continuous with the top front","the two front ends meet in a visible knot"],
 ['wardrobe.front.knot','wardrobe.front.tie_attachment'],
 [('continuous_with','top.front.fabric_ends','top.front_panels'),('joins','top.front.knot','top.front.fabric_ends')],
 'A detached appliqued knot lacks front-panel continuity; the image does not prove the knot opens a functional closure.')
a('sf034_02','양옆보다 낮은 중앙 꼭짓점의 상의 밑단','top',
 ["the top hem descends to one distinct central point","both side portions of the same hem remain higher than that point"],
 ['wardrobe.hem.asymmetry','wardrobe.hem.center_point'],
 [('lower_than','top.hem.center_point','top.hem.side_edges')],
 'A centered shadow or perspective distortion is not a shaped hem; scarf origin, backlessness and cropped length remain unspecified.')
a('sf035_02','배꼽 영역을 둘러싼 드레스 개구부','dress',
 ["an opening in the dress lies around the same wearer's navel area","a continuous remaining dress rim bounds that opening"],
 ['wardrobe.cutout.location','wardrobe.cutout.topology'],
 [('at','dress.opening','wearer.navel_area'),('bounds','dress.opening.fabric_rim','dress.opening')],
 'A printed patch, transparent panel or open separation between two garments has another topology; the behind-opening surface must be identified.')
a('sf037_01','상의 부착 끈이 노출 허리를 감아 옆 매듭으로 이어짐','top',
 ["thin ties start at the selected top and wrap around the visible waist","the same tie paths continue to a knot at the wearer's side"],
 ['wardrobe.tie.attachment','wardrobe.tie.route','wardrobe.tie.knot_location','wardrobe.coverage.waist'],
 [('attached_to','top.waist_ties','top'),('wraps_around','top.waist_ties','wearer.visible_waist'),('joins','top.side_knot','top.waist_tie_ends')],
 'A separate waist chain, detached belt or drawn line lacks the same-top tie path; restraint or sexual behavior is not inferred.')
a('sf039_01','성인 상의 옆 경계 밖에 보이는 작은 측면 가슴 피부','adult_top',
 ["the adult wearer's top side edge ends beside a small lateral breast region","that lateral skin region is visibly outside the same top boundary"],
 ['wardrobe.coverage.side_breast','wardrobe.top.side_edge'],
 [('beside','top.side_edge','adult_wearer.lateral_breast'),('outside','adult_wearer.visible_lateral_skin','top.side_boundary')],
 'An underbust seam, skin-colored lining or dark side shadow does not establish this skin location; the inner visible surface must be inspected.')
a('sf040_02','무릎 아래와 발목 위에 놓이는 스커트 밑단','skirt',
 ["the selected skirt hem lies below the same wearer's knees","that hem remains above the same ankles"],
 ['wardrobe.skirt.hem_height'],
 [('below','skirt.hem','wearer.knees'),('above','skirt.hem','wearer.ankles')],
 'A crop hiding anatomical landmarks cannot verify relative hem height; fixed centimeter length and leg dimensions remain unspecified.')
a('sf041_01','허벅지 높이에서 시작되는 긴 치마의 슬릿','skirt',
 ["two slit edges separate from a high point beside the same thigh","the long skirt remains continuous around the slit start"],
 ['wardrobe.skirt.slit_location','wardrobe.skirt.slit_height','wardrobe.skirt.slit_topology','wardrobe.skirt.hem_height'],
 [('starts_at','skirt.slit.upper_endpoint','wearer.upper_thigh_region'),('bounds','skirt.continuous_surround','skirt.slit_start')],
 'A fold shadow, wrap overlap or printed black line lacks two separated fabric edges; the visible underlying surface is independent.')
a('sf041_04','같은 스커트 앞 중앙에서 갈라지는 슬릿','skirt',
 ["a slit occupies the center front of the selected skirt","two separated fabric edges continue down from that front slit start"],
 ['wardrobe.skirt.slit_location','wardrobe.skirt.slit_topology'],
 [('at','skirt.slit','skirt.center_front'),('extends_from','skirt.slit.side_edges','skirt.slit.upper_endpoint')],
 'A side slit, crease shadow and wrap-panel free edge are distinct; no thigh-height start or universal slit count is added.')
a('sf043_01','같은 스커트의 뒤보다 짧은 앞 밑단','skirt',
 ["the front hem of the skirt ends higher on the wearer than its back hem","front and back boundaries remain parts of one continuous skirt"],
 ['wardrobe.hem.height_distribution'],
 [('higher_than','skirt.front_hem','skirt.back_hem')],
 'Viewpoint foreshortening or lifted fabric alone cannot establish a cut front-to-back height difference.')
a('sf045_01','바깥으로 부풀고 모아진 밑단에서 안쪽으로 돌아가는 치마','skirt',
 ["the skirt shell expands outward above its lower edge","the same shell turns inward into a gathered hem"],
 ['wardrobe.skirt.volume','wardrobe.skirt.hem_construction'],
 [('expands_above','skirt.shell','skirt.hem'),('turns_into','skirt.shell.lower_edge','skirt.gathered_hem')],
 'A broad A-line edge without the inward lower turn is different; hip size and hidden lining construction are unproven.')
a('sf047_01','두 다리의 허벅지 높이에서 끝나는 짧은 바지','shorts',
 ["the shorts divide into two distinct trouser legs","both leg hems end high along the same wearer's thighs"],
 ['wardrobe.shorts.length','wardrobe.shorts.leg_separation'],
 [('ends_at','shorts.leg_hems','wearer.upper_thighs'),('divides_into','shorts.body','shorts.two_legs')],
 'A short skirt or one connected hem does not show two trouser legs; a cut-off manufacturing history is not asserted.')
a('sf048_01','옆으로 올라가는 바인딩 경계의 쇼츠 밑단','shorts',
 ["the shorts hems curve upward at their outer sides","a distinct bound strip follows those curved hem edges"],
 ['wardrobe.shorts.hem_contour','wardrobe.hem.edge_binding'],
 [('rises_at','shorts.hem_curves','shorts.outer_sides'),('follows','shorts.bound_edge','shorts.hem_curves')],
 'A straight horizontal hem or color stripe above the edge is different; stretch, pressure and sports performance are unscored.')
a('sf049_02','종아리 영역에서 끝나는 바지 두 밑단','trousers',
 ["the two trouser hems end around the same wearer's calves","both hems remain continuous with their respective trouser legs"],
 ['wardrobe.pants.length'],
 [('ends_at','trousers.leg_hems','wearer.calves')],
 'An ankle-length trouser hem or a camera crop at the calf is a different condition; no fixed leg width is added.')
a('sf050_02','가슴·허리·힙 윤곽을 가까이 따르는 드레스','dress',
 ["the dress surface follows closely around the bust and waist","the same dress continues close to the hip contour"],
 ['wardrobe.fit.local_contact'],
 [('follows','dress.bodice_surface','wearer.bust_and_waist_contours'),('follows','dress.hip_surface','wearer.hip_contour')],
 'A draped garment with visible loose space has different local contact; apparent fit does not establish compression, stretch percentage or body measurements.')
a('sf051_01','위와 힙 영역 사이에서 좁아지는 의복 허리 윤곽','garment',
 ["the garment silhouette narrows at the waist","the same garment has fuller visible upper and hip regions on either side of that narrowing"],
 ['wardrobe.silhouette.width_distribution'],
 [('narrower_than','garment.waist_outline','garment.upper_and_hip_outlines')],
 'Changing the wearer anatomy does not establish garment silhouette; a waist belt alone does not prove both adjacent fuller garment regions.')
a('sf052_02','밀착 몸판 아래 허리부터 퍼지는 치마 연결','dress',
 ["a fitted bodice joins the skirt at the waist","the skirt expands outward below that same join"],
 ['wardrobe.fit.local_contact','wardrobe.silhouette.flare_start','wardrobe.silhouette.width_distribution','wardrobe.skirt.join_height'],
 [('joins_at','dress.bodice_and_skirt','wearer.waist'),('expands_below','dress.skirt','dress.waist_join')],
 'A loose A-line garment starting near the shoulders is a different variant; wearer torso dimensions remain unchanged.')
a('sf054_01','가슴 바로 아래 높게 연결되어 내려오는 드레스 치마','dress',
 ["the dress skirt joins the bodice directly below the bust","the skirt falls downward from that raised bodice seam"],
 ['wardrobe.waist_seam.height','wardrobe.skirt.join_height'],
 [('below','dress.skirt_join','wearer.bust'),('starts_at','dress.skirt','dress.raised_bodice_seam')],
 'A high trouser waistband or a seam with no attached skirt is a different owner relation; support and comfort are unproven.')
a('sf055_02','몸통 옆 공간을 남기는 넓고 곧은 상의 옆판','top',
 ["the top side panels fall in a broad straight outline","visible space separates those panels from the wearer's torso"],
 ['wardrobe.fit.local_ease','wardrobe.silhouette.contour'],
 [('beside','top.side_panels','wearer.torso'),('separates','top.side_ease','top.panels_and_wearer.torso')],
 'An enlarged body silhouette or a flaring peplum is a different condition; visible ease does not quantify garment dimensions.')
a('sf057_01','니트 실·루프가 각 작은 구멍 둘레를 이루며 같은 면에서 반복됨','knit_top',
 ["knit yarn loops form the complete rims around each small opening in the top","the yarn-bounded openings repeat in a geometric pattern within the same continuous knit surface"],
 ['wardrobe.textile.openwork_topology','wardrobe.textile.visible_loop_texture','wardrobe.textile.opening_rim_structure'],
 [('forms_rim_around','knit_top.yarn_loops','knit_top.small_opening_boundaries'),('continuous_with','knit_top.opening_rim_loops','knit_top.surrounding_yarn_loops'),('repeats_across','knit_top.yarn_bounded_openings','knit_top.continuous_knit_surface')],
 'A smooth sheet bordering a hole, a separate stitched ring, printed dots or loop shapes merely nearby cannot substitute for knit yarn forming each rim. Fiber composition, exact gauge and manufacturing process remain unproven.', 'surface_material')
ROWS['sf057_01']['visible_regions']=['small opening rims formed by knit yarn loops','continuous knit surface surrounding repeated openings']
ROWS['sf057_01']['gate_descriptions']=[
 'Trace actual knit yarn loops around the complete rim of each inspected small opening and into the surrounding knitted surface at native resolution. A smooth sheet bordering a hole, a separate stitched ring, printed dots or loops merely nearby does not satisfy a rim formed by continuous knit yarn. Fiber composition, exact gauge and manufacturing process are unscored.',
 'Inspect geometric repetition of the yarn-bounded openings within one continuous knit top surface at native resolution. Each inspected opening must show a knit yarn rim continuous with that same surrounding surface; repeated holes on a separate trim or mesh layer do not satisfy this relation. Missing, hidden or partial rim evidence fails.'
]
a('sf059_01','분리된 앞 가장자리의 단추·단춧구멍 밴드','cardigan',
 ["separate front edges belong to the same cardigan","one edge carries buttons and the opposing band has visible buttonholes"],
 ['wardrobe.cardigan.closure','wardrobe.closure.edge_structure'],
 [('belongs_to','cardigan.front_edges','cardigan'),('opposes','cardigan.button_band','cardigan.buttonhole_band')],
 'A printed button row or continuous center panel lacks the opposing closure edges; open state and cropped length remain unspecified.')
a('sf060_01','같은 니트 결·색의 안쪽 상의와 별도 카디건','inner_top_and_cardigan',
 ["a separate knit-textured top lies beneath the same wearer's cardigan","the two garments show matching visible loop texture and color"],
 ['wardrobe.layer.order','wardrobe.layer.matching_surface','wardrobe.palette.item_relationship'],
 [('beneath','inner_top','cardigan'),('matches_surface','inner_top.visible_knit_and_color','cardigan.visible_knit_and_color')],
 'A printed imitation of two garments or only matching color lacks the independent layer and texture relation; shared fiber content is unproven.')
a('sf062_01','짧은 단추 플래킷으로 연결되는 니트 칼라','polo_top',
 ["a loop-textured collar attaches around the polo top neckline","that collar joins a short front button placket"],
 ['wardrobe.collar.presence','wardrobe.collar.visible_surface','wardrobe.placket.extent','wardrobe.placket.connection'],
 [('attached_to','polo_top.collar','polo_top.neckline'),('joins','polo_top.collar','polo_top.short_button_placket')],
 'A collar-free partial opening or a full-length shirt closure is a different combination; fiber type is not established.')
a('sf062_04','마감된 암홀과 연속 루프 표면의 민소매 베스트','knit_vest',
 ["the vest has finished armhole edges with the upper arms outside sleeve tubes","its body remains a continuous loop-textured garment surface"],
 ['wardrobe.sleeve.presence','wardrobe.armhole.edge_finish','wardrobe.textile.visible_loop_texture'],
 [('bounds','knit_vest.finished_armholes','wearer.upper_arms'),('continuous_with','knit_vest.body_surface','knit_vest.armhole_rims')],
 'A shirt with hidden sleeves or printed knit-like stripes does not show the declared visible vest structure.')
a('sf064_01','겉 셔츠 결을 통해 보이는 안쪽 상의 윗단','outer_shirt_and_inner_top',
 ["the outer shirt texture remains visible over a solid inner top","the separate inner top upper edge is visible through that shirt fabric"],
 ['wardrobe.layer.transmission','wardrobe.layer.order'],
 [('over','outer_shirt','inner_top'),('visible_through','inner_top.upper_edge','outer_shirt.fabric')],
 'An uncovered gap, solid painted patch and skin-tone lining cannot substitute for a separately bounded inner top.')
a('sf066_01','드레이프 몸판과 연속 치마에 부착된 가는 드레스 끈','dress',
 ["thin straps attach to the softly draped dress bodice","that bodice continues into the same dress skirt"],
 ['wardrobe.dress.strap_connection','wardrobe.strap.width','wardrobe.textile.drape','wardrobe.bodice.skirt_connection'],
 [('attached_to','dress.thin_straps','dress.draped_bodice'),('continuous_with','dress.bodice','dress.skirt')],
 'A separate camisole above a skirt has a different garment continuity; silk, bias-cut manufacture and hidden underwear remain unproven.')
a('sf067_02','허리의 고정 연결로 만나는 겹친 드레스 앞판','dress',
 ["two distinct dress front panels overlap","their meeting area has a fixed visible join at the same waist"],
 ['wardrobe.front.overlap','wardrobe.closure.topology','wardrobe.front.join_location'],
 [('overlaps','dress.front.outer_panel','dress.front.under_panel'),('joined_at','dress.front.panels','dress.waist_fixed_join')],
 'A freely tied opening and one-panel V cut are different; the visible fixed join does not prove adjustable or opening wrap function.')
a('sf068_03','가슴 아래 높은 연결선부터 시작하는 짧고 풍성한 치마','dress',
 ["a high skirt seam lies below the same wearer's bust","a short full skirt expands from that dress seam"],
 ['wardrobe.skirt.join_height','wardrobe.skirt.length','wardrobe.skirt.volume'],
 [('below','dress.high_skirt_seam','wearer.bust'),('starts_at','dress.short_full_skirt','dress.high_skirt_seam')],
 'A low waist seam or an unattached flounce has a different relationship; the garment name does not establish wearer age or exact centimeter length.')
a('sf070_01','가로 봉제선에 연결된 여러 모음 치마 층','skirt',
 ["several gathered tiers form the same skirt","horizontal seams join each tier to the neighboring skirt section"],
 ['wardrobe.dress.tier_connections','wardrobe.folds.anchor_topology','wardrobe.skirt.tier_count'],
 [('joins','skirt.horizontal_tier_seams','skirt.adjacent_gathered_tiers')],
 'Separate stacked garments or unjoined fold shadows do not establish skirt tiers; all family alternatives remain optional.')
a('sf071_02','드레스 어깨에 부착되어 소매 밖으로 내려오는 케이프판','dress',
 ["a cape panel attaches at the dress shoulders","the same panel hangs outside the dress sleeves"],
 ['wardrobe.dress.overpanel_connection','wardrobe.layer.order'],
 [('attached_to','dress.cape_panel','dress.shoulders'),('outside','dress.cape_panel','dress.sleeves')],
 'A loose scarf or sleeve fabric does not form this shoulder-mounted exterior panel; role and occupation are unspecified.')
a('sf072_03','외부 장식이 적은 레인코트 앞 플래킷 여밈','raincoat',
 ["a clean central placket closes the raincoat front edges","the visible exterior front panels have a sparse arrangement of details"],
 ['wardrobe.coat.front_structure','wardrobe.coat.details'],
 [('joins','raincoat.clean_placket','raincoat.front_edges'),('on','raincoat.sparse_details','raincoat.visible_front_panels')],
 'A belt-only tie or concealed open front is a different closure; visible simplicity does not prove waterproofing or hidden lining absence.')
a('sf073_03','안쪽 상의 밑단보다 위의 허리 높이 블레이저 밑단','blazer_and_inner_top',
 ["the blazer hem ends near the same wearer's waist","the separate inner top hem extends below that blazer hem"],
 ['wardrobe.outer.length','wardrobe.layer.hem_relation'],
 [('at','blazer.hem','wearer.waist'),('below','inner_top.hem','blazer.hem')],
 'One uninterrupted fabric panel cannot establish two hems; shortened outer length does not prove an unlined or unpadded interior.')
a('sf074_03','여러 플랩 포켓과 부착 벨트를 가진 재킷','jacket',
 ["multiple pockets on the jacket have separate overlying flaps","a belt is attached to that same jacket"],
 ['wardrobe.jacket.pocket_topology','wardrobe.belt.attachment'],
 [('overlies','jacket.pocket_flaps','jacket.pocket_openings'),('attached_to','jacket.belt','jacket')],
 'Painted pocket outlines or an unrelated waist accessory do not establish attachment; wearer military or farming identity is unproven.')
a('sf075_02','후드가 달린 겉옷의 몸판 중간까지만 열린 앞 여밈','outer_top',
 ["a hood attaches at the outer top neckline","its front opening ends partway down the same body panel"],
 ['wardrobe.hood.attachment','wardrobe.placket.extent'],
 [('attached_to','outer_top.hood','outer_top.neckline'),('ends_within','outer_top.front_opening','outer_top.body_panel')],
 'A full-length coat opening or detached hood is different; wind resistance, thickness and thermal performance are unscored.')
a('sf075_05','칼라·단추밴드·덧댄 가슴 포켓의 셔츠형 겉옷','outer_shirt_layer',
 ["a collar joins the shirt-like outer layer neckline","a front button placket connects its front edges","patch pockets sit on the same layer at chest height"],
 ['wardrobe.collar.presence','wardrobe.placket.topology','wardrobe.jacket.pocket_topology','wardrobe.jacket.pocket_location'],
 [('joined_to','outer_shirt_layer.collar','outer_shirt_layer.neckline'),('connects','outer_shirt_layer.button_placket','outer_shirt_layer.front_edges'),('on','outer_shirt_layer.patch_pockets','outer_shirt_layer.chest_panels')],
 'Printed pockets, an inner shirt glimpsed through a jacket or an unrelated collar cannot replace these same-layer components.')
a('sf077_03','미세하고 촘촘한 직교 격자의 셔츠 원단 표면','shirt',
 ["fine closely spaced threads form an orthogonal grid on the shirt cloth","the small crossing pattern follows the same cloth surface"],
 ['wardrobe.textile.visible_weave'],
 [('crosses','shirt.surface.horizontal_threads','shirt.surface.vertical_threads'),('on','shirt.thread_grid','shirt.cloth')],
 'Blurred solid cloth and printed grid lines do not show visible thread crossings; fiber content and named commercial fabric identity are unproven.', 'surface_material')
a('sf079_01','작고 부드러운 접힘으로 내려오는 얇은 투과 원단','fabric',
 ["thin translucent fabric retains a readable textile boundary","the same fabric falls in small soft folds"],
 ['wardrobe.layer.transmission','wardrobe.textile.fold_scale','wardrobe.textile.drape'],
 [('transmits_through','fabric.visible_background_surface','fabric.thin_textile'),('folds_within','fabric.small_soft_folds','fabric.same_textile')],
 'A solid opaque lining or stiff large projecting folds has a different visible state; fiber composition, weight and hand feel are unscored.', 'surface_material')
a('sf080_01','작은 망상 셀이 반복되는 고운 네트 레이어','net_layer',
 ["small mesh cells repeat across the fine net layer","each opening is bounded by strands continuous with that same net"],
 ['wardrobe.textile.open_space_pattern','wardrobe.textile.visible_cell_scale'],
 [('bounds','net_layer.strands','net_layer.small_cells'),('repeats_across','net_layer.cell_pattern','net_layer.surface')],
 'Printed dots and shirt weave noise lack open mesh cells; cell appearance alone does not identify fiber or a production process.', 'surface_material')
a('sf081_01','매끈한 원단 접힘을 따라가는 넓고 부드러운 하이라이트','fabric',
 ["the fabric surface appears smooth between its folds","broad soft highlights follow the curves of that same fabric"],
 ['wardrobe.textile.reflectance','wardrobe.textile.surface_structure'],
 [('follows','fabric.broad_highlights','fabric.curved_folds')],
 'A narrow metallic glint or uniformly painted bright patch has different light behavior; a smooth highlight does not establish silk or a satin weave.', 'surface_material')
a('sf082_01','겉 원단 결 너머로 비치는 별도 안쪽 의복 경계','outer_fabric_and_inner_garment',
 ["the outer fabric texture remains readable","the separate inner garment edge shows through that same outer fabric"],
 ['wardrobe.layer.transmission'],
 [('outside','outer_fabric','inner_garment'),('visible_through','inner_garment.edge','outer_fabric')],
 'A cutout exposing an edge directly has a different optical path; outer and inner layers are prerequisites rather than permission to remove either one.', 'surface_material')
a('sf084_01','휘어진 직물 표면을 따라가는 넓은 밝은 반사','fabric',
 ["a broad luminous highlight occupies the curved fabric surface","the bright band follows that same fabric curvature"],
 ['wardrobe.textile.reflectance'],
 [('follows','fabric.luminous_highlight','fabric.curved_surface')],
 'A background light streak or painted white stripe is a different owner; one lighting condition does not prove intrinsic gloss or fiber identity.', 'surface_material')
a('sf086_01','하나의 고정 봉제선으로 모이는 작은 직물 접힘','garment',
 ["small fabric folds converge toward one attachment seam","their bases join that same visible seam"],
 ['wardrobe.folds.anchor_topology'],
 [('converges_into','garment.small_folds','garment.single_attachment_seam'),('joins','garment.fold_bases','garment.attachment_seam')],
 'Random wrinkles or detached ruffles lack the declared fixed line; elastic thread and stretch are not established.')
a('sf086_04','모음 주름의 꼭대기를 잇는 기하학 장식 스티치','garment',
 ["decorative stitches connect the peaks of gathered fabric folds","those linked fold peaks form a geometric stitched pattern"],
 ['wardrobe.folds.anchor_topology','wardrobe.stitching.row_pattern'],
 [('links','garment.decorative_stitches','garment.gathered_fold_peaks'),('forms','garment.linked_peaks','garment.geometric_stitch_pattern')],
 'A printed grid or plain gathering seam lacks the stitches bridging fold peaks; the image does not prove elastic thread.')
a('sf087_03','치마 밑단 방향으로 벌어지는 좁은 반복 플리츠','skirt',
 ["narrow repeated pleat ridges run down the selected skirt","the same pleat intervals fan wider toward that skirt hem"],
 ['wardrobe.pleats.direction','wardrobe.pleats.repeat_scale','wardrobe.pleats.spacing_distribution'],
 [('runs_toward','skirt.narrow_pleat_ridges','skirt.hem'),('widens_toward','skirt.pleat_intervals','skirt.hem')],
 'Printed stripes, rib knitting and random creases do not show folded pleat edges; heat-setting history is unscored.')
a('sf089_01','한쪽에 모아 부착되고 자유 끝이 물결치는 직물 띠','garment_trim',
 ["a gathered fabric strip attaches along one edge to the garment","the opposite free edge ripples outward from that attachment"],
 ['wardrobe.trim.attachment','wardrobe.trim.gathering','wardrobe.trim.free_edge_contour'],
 [('attached_to','garment_trim.gathered_edge','garment.edge'),('opposite','garment_trim.rippling_free_edge','garment_trim.attached_edge')],
 'A printed wavy border or a sleeve body is a different construction; the outward contour does not prove a particular cutting method.')
a('sf090_02','작은 원단 구멍을 둘러싸는 보이는 자수 스티치','garment_surface',
 ["small openings interrupt the same garment fabric surface","visible embroidery stitches surround the rims of those openings"],
 ['wardrobe.embroidery.hole_border','wardrobe.textile.open_space_pattern'],
 [('within','garment_surface.small_openings','garment_surface.fabric'),('surrounds','garment_surface.embroidery_stitches','garment_surface.opening_rims')],
 'Printed holes, translucent patches and metal eyelets lack the stitched fabric rims; actual cutting process is unproven.')
a('sf091_02','목선에 부착된 작은 입체 직물 로제트','garment',
 ["rolled fabric folds form a small raised rosette","the rosette base attaches to the same garment neckline"],
 ['wardrobe.ornament.attachment','wardrobe.ornament.structure','wardrobe.ornament.scale'],
 [('forms','garment.rosette.rolled_folds','garment.rosette.raised_volume'),('attached_to','garment.rosette.base','garment.neckline')],
 'A floral print, real cut flower or jewelry rosette on a different band is a different object; a decorative rosette is not a tie closure.', 'garment_detail')
a('sf093_01','의복 가장자리에서 각각 내려오는 연속 술 가닥','garment',
 ["separate fringe strands start continuously from the garment edge","the individual strands hang below that same attachment line"],
 ['wardrobe.trim.endpoint_topology','wardrobe.trim.strand_count'],
 [('starts_at','garment.fringe_strands','garment.edge'),('hangs_below','garment.fringe_strands','garment.fringe_attachment_line')],
 'A hanging tassel bundle, loose background threads and a fringe print have a different endpoint topology.')
a('sf093_04','벨트 표면에 하나씩 부착된 금속성 스터드','belt',
 ["individual metal-looking studs sit on the belt surface","each visible stud has its own attachment footprint on that belt"],
 ['wardrobe.hardware.attachment','wardrobe.belt.surface_relief'],
 [('attached_to','belt.individual_studs','belt.surface')],
 'Printed dots or studs on another garment do not establish this belt attachment; visual metal appearance does not certify alloy or composition.')
a('sf094_03','형태를 잡은 허리·부드러운 치마·부착 장식의 같은 착장','outfit',
 ["the selected outfit forms a shaped waist line","its skirt falls in soft flowing folds","a small ornament attaches to that same outfit"],
 ['wardrobe.silhouette.waist_shape','wardrobe.skirt.folds','wardrobe.ornament.attachment','wardrobe.ornament.scale'],
 [('belongs_to','outfit.shaped_waist_and_flowing_skirt','outfit'),('attached_to','outfit.small_ornament','outfit')],
 'One bow alone does not establish the whole garment combination; the outfit does not prove personality, sexual behavior or age.')
a('sf096_02','높은 목선·풍성한 소매·긴 층 치마의 같은 드레스','dress',
 ["a high neckline encloses the upper opening of the dress","full sleeves attach to that same bodice","a long skirt continues from the bodice through joined tiers"],
 ['wardrobe.neckline.height','wardrobe.sleeve.volume','wardrobe.sleeve.attachment','wardrobe.skirt.length','wardrobe.dress.tier_connections'],
 [('attached_to','dress.full_sleeves','dress.bodice'),('joined_to','dress.long_tiered_skirt','dress.bodice'),('within','dress.high_neckline','dress.upper_opening')],
 'Floral print alone does not create this garment combination; rural residence, ethnicity and historical social role remain unproven.')
a('sf097_02','열린 블레이저 안의 단추 셔츠와 곧은 바지','outfit',
 ["an open blazer lies outside the same wearer's collared button-front shirt","straight trouser legs continue below those separate upper layers"],
 ['wardrobe.layer.order','wardrobe.blazer.closure.current_state','wardrobe.shirt.collar','wardrobe.shirt.front_button_band','wardrobe.pants.leg_width','wardrobe.layer.item_combination'],
 [('outside','outfit.open_blazer','outfit.collared_button_front_shirt'),('below','outfit.straight_trousers','outfit.upper_layers')],
 'A shirt printed onto one jacket panel lacks independent layers; school status, wealth, fiber identity and educational background are not established.')
a('sf098_02','스포츠 상의 밖의 열린 블레이저와 넓은 바지','outfit',
 ["an open blazer lies over a separately bounded sports top","wide trouser legs belong to the same wearer's lower garment"],
 ['wardrobe.layer.order','wardrobe.blazer.closure.current_state','wardrobe.inner_top.garment_type','wardrobe.pants.leg_width','wardrobe.layer.item_combination'],
 [('outside','outfit.open_blazer','outfit.sports_top'),('belongs_to','outfit.wide_trousers','wearer')],
 'One printed sports motif on a blazer does not create a separate sports top; sports ability and performance properties remain unscored.')
a('sf099_02','표시 없는 재킷과 바지의 절제된 중성색 관계','jacket_and_trousers',
 ["the visible jacket and trouser panels have unmarked surfaces","those two garments share a restrained neutral color palette"],
 ['wardrobe.jacket.surface.markings','wardrobe.pants.surface.markings','wardrobe.palette.item_relationship'],
 [('shares_palette','jacket.visible_color','trousers.visible_color'),('on','outfit.unmarked_surfaces','jacket_and_trousers.visible_panels')],
 'A neutral background filter does not establish garment-local color; visible unmarked panels do not certify hidden logo absence, actual price or luxury provenance.')
a('sf101_01','레이스가 연결된 슬립 드레스 밖의 별도 카디건','outfit',
 ["lace trim attaches to the slip dress fabric edge","a separate cardigan lies outside that same dress"],
 ['wardrobe.dress.garment_type','wardrobe.trim.connection','wardrobe.layer.order'],
 [('attached_to','slip_dress.lace_trim','slip_dress.fabric_edge'),('outside','cardigan','slip_dress')],
 'A lace print or one simulated cardigan panel cannot replace the distinct trim and layer relation; hidden underwear presence is unproven.')
a('sf101_04','연속 블라우스 위에서 버클로 이어지는 별도 하네스','harness_and_blouse',
 ["a separate fashion harness lies over the continuous blouse surface","its strap segments connect at a visible buckle"],
 ['wardrobe.layer.order','wardrobe.accessory.strap_topology','wardrobe.accessory.buckle_connection'],
 [('outside','fashion_harness','blouse.continuous_surface'),('joins','fashion_harness.buckle','fashion_harness.strap_segments')],
 'Printed straps or disconnected hardware lack this physical connection; a fashion harness does not establish restraint, consent or sexual activity.')
a('sf103_01','선택한 카디건 면의 옅고 따뜻한 노랑','cardigan',
 ["the selected cardigan surface is pale warm yellow","the yellow color remains local to that cardigan fabric"],
 ['wardrobe.cardigan.color'],
 [('colors','pale_warm_yellow','cardigan.fabric_surface')],
 'Warm global lighting or a yellow background does not establish cardigan-local color; no fixed RGB, Pantone or seasonal prevalence is claimed.', 'color')
a('sf103_04','작은 가방 면의 선명한 빨강 액센트','bag',
 ["the small bag surface is saturated red","that bag forms a localized red accent within the outfit"],
 ['wardrobe.accessories.bag.color','wardrobe.accessories.bag.scale'],
 [('colors','saturated_red','bag.surface'),('belongs_to','bag.local_accent','wearer.outfit')],
 'A red background or red color on a separate garment is a different owner; no exact spectral color or material authenticity is claimed.', 'color')
a('sf103_07','선택한 블라우스 면의 베이지 기가 도는 옅은 따뜻한 분홍','blouse',
 ["the selected blouse surface is pale warm pink","a muted beige undertone remains within that same blouse color"],
 ['wardrobe.blouse.color'],
 [('colors','pale_warm_pink_with_muted_beige','blouse.fabric_surface')],
 'Cheek blush or a pink global tint does not establish blouse-local color; undertone names do not certify an exact numerical color.', 'color')
a('sf103_10','선택한 셔츠 면의 밝고 맑은 파랑','shirt',
 ["the selected shirt surface is light clear blue","the blue color stays within the shirt fabric boundary"],
 ['wardrobe.shirt.color'],
 [('colors','light_clear_blue','shirt.fabric_surface')],
 'Blue sky or a global cool white balance is a different color owner; no brand color code or universal reference swatch is claimed.', 'color')
a('sf103_13','선택한 바지 면의 옅고 절제된 베이지 회색','trousers',
 ["the selected trouser surface is light muted beige-gray","that beige-gray remains a local lower-garment color"],
 ['wardrobe.pants.color'],
 [('colors','light_muted_beige_gray','trousers.fabric_surface')],
 'A neutral grading filter or beige background is a different owner; exact greige boundaries require a chosen swatch.', 'color')
a('sf104_03','봉제선에서 만나는 같은 옷의 큰 서로 다른 색판','garment',
 ["large differently colored panels form the same garment","the colored panels meet along visible garment seams"],
 ['wardrobe.palette.panel_layout','wardrobe.palette.panel_color_relationship'],
 [('meets_along','garment.distinct_color_panels','garment.panel_seams')],
 'A scene-wide gradient or color blocks in the background are different owners; panel layout does not require changing unrelated garments.', 'color')
a('sf105_03','드레스 인쇄면의 부드러운 가장자리 꽃 색면','dress',
 ["floral color patches form a print on the dress fabric","the printed patches have soft watercolor-like edges"],
 ['wardrobe.print.motif','wardrobe.print.edge_quality'],
 [('printed_on','dress.floral_color_patches','dress.fabric_surface'),('has_edge','dress.floral_print','soft_color_boundary')],
 'Actual flowers, attached embroidery and lace openings are different objects; painting method and exact physical print scale are unproven.', 'color')
a('sf106_03','같은 의복 면에 반복되는 둥근 점 무늬','garment',
 ["round dots repeat on the garment fabric","the dot pattern follows the same garment surface through its folds"],
 ['wardrobe.print.repeat_topology','wardrobe.print.motif_contour'],
 [('repeats_on','garment.round_dots','garment.fabric_surface')],
 'Background dots, mesh openings and circular appliques are different owners or constructions; dyeing and printing process are unscored.', 'color')
a('sf107_01','발 앞부분을 감싸는 낮은 플랫과 뱀프 리본','shoe',
 ["the low flat shoe upper encloses the forefoot","a small tied bow sits at the same shoe vamp"],
 ['wardrobe.shoe.upper_coverage','wardrobe.shoe.heel_shape','wardrobe.shoe.vamp_ornament'],
 [('encloses','shoe.upper','wearer.forefoot'),('at','shoe.small_bow','shoe.vamp')],
 'A pointe shoe, tall heel or unrelated ankle bow is a different construction; low flat appearance does not establish comfort or dance ability.', 'footwear')
a('sf107_04','뒤꿈치를 감싸는 끈이 없는 열린 신발 뒷경계','shoe',
 ["the shoe upper terminates before the rear heel","the visible rear boundary is an uninterrupted open heel interval"],
 ['wardrobe.shoe.rear_coverage','wardrobe.shoe.rear_strap_topology'],
 [('ends_before','shoe.upper.rear_boundary','wearer.rear_heel'),('around','shoe.open_rear_interval','wearer.rear_heel')],
 'A slingback strap bridging the visible rear boundary is different; an occluded rear heel cannot certify the open interval.', 'footwear')
a('sf107_07','교차 끈 여밈 대신 연속 뱀프가 이어지는 낮은 슬립온','shoe',
 ["the low slip-on shoe has a continuous unbroken vamp","the visible vamp surface spans the forefoot as one upper panel"],
 ['wardrobe.shoe.upper_structure','wardrobe.shoe.vamp_closure','wardrobe.shoe.heel_shape'],
 [('spans','shoe.continuous_vamp','wearer.forefoot')],
 'Crossing laces across the visible vamp or tall boots form another construction; hidden fastening methods are not certified.', 'footwear')
a('sf108_03','얇아 보이는 낮은 밑창과 좁은 스니커즈 갑피','sneaker',
 ["the sneaker sole has a low thin-looking side profile","a narrow upper joins that same low sole"],
 ['wardrobe.shoe.sole_height','wardrobe.shoe.upper_volume','wardrobe.shoe.upper_sole_connection'],
 [('joins','sneaker.narrow_upper','sneaker.low_sole')],
 'A chunky platform or broad upper is a different visible profile; precise sole thickness, weight and performance are unscored.', 'footwear')
a('sf109_02','같은 무릎보다 위에 도달하는 스타킹 윗단','stocking',
 ["the stocking upper edge lies above the same wearer's knee","that upper edge bounds the stocking tube around the leg"],
 ['wardrobe.hosiery.hem_height'],
 [('above','stocking.upper_edge','wearer.knee'),('bounds','stocking.upper_edge','stocking.leg_tube')],
 'A knee-high edge or frame crop lacks the specified relative location; denier, fiber and hidden garter support are unproven.', 'wearable_accessory')
a('sf109_05','발을 바깥에 두고 종아리에서 모이는 별도 니트 튜브','legwarmer',
 ["a separate loop-textured tube gathers around the calf","the same foot remains outside that calf tube"],
 ['wardrobe.legwarmer.coverage','wardrobe.legwarmer.folds','wardrobe.legwarmer.visible_surface'],
 [('around','legwarmer.gathered_tube','wearer.calf'),('outside','wearer.foot','legwarmer.tube')],
 'A continuous footed stocking is a different garment; the foot may carry another sock or shoe, and fiber content is not established.', 'wearable_accessory')
a('sf110_03','목을 돌아 작은 매듭으로 만나는 얇은 스카프','scarf',
 ["a thin scarf passes around the same wearer's neck","the scarf ends meet in a small visible knot"],
 ['wardrobe.accessories.scarf.route','wardrobe.accessories.scarf.knot','wardrobe.accessories.scarf.visible_thickness'],
 [('wraps_around','scarf.fabric_length','wearer.neck'),('joins','scarf.small_knot','scarf.ends')],
 'A necklace, garment bow or detached fabric strip has a different owner; thin shine does not prove silk composition.', 'wearable_accessory')
a('sf112_01','같은 착장 밖 허리를 감는 별도 링크 체인','waist_chain',
 ["linked metal-looking segments form a separate chain","the chain passes around the same wearer's waist outside the outfit"],
 ['wardrobe.accessories.chain.connection_topology','wardrobe.accessories.chain.route','wardrobe.accessories.chain.layer_order'],
 [('joins','waist_chain.links','waist_chain.neighboring_links'),('wraps_around','waist_chain','wearer.waist'),('outside','waist_chain','wearer.outfit')],
 'A printed chain motif, top ties or detached background chain has a different owner; alloy, restraint and sexual activity are unscored.', 'wearable_accessory')
a('sf112_04','스타킹 클립 연결 대신 허벅지에 도는 별도 장식 밴드','thigh_band',
 ["a separate decorative band circles the same wearer's thigh","the band's visible lower boundary remains independent of a stocking attachment"],
 ['wardrobe.accessories.thigh_band.route','wardrobe.accessories.thigh_band.connection_topology'],
 [('circles','thigh_band','wearer.thigh'),('independent_of','thigh_band.visible_lower_boundary','stocking_attachment')],
 'A visible stocking-support clip has a different connection; an occluded boundary cannot certify absence of a hidden clip.', 'wearable_accessory')
a('sf113_03','겉옷의 실제 개구부로 드러나는 별도 안쪽 의복','outer_and_inner_garment',
 ["a bounded opening lies in the outer garment","a separate inner garment surface is visible through that opening"],
 ['wardrobe.layer.order','wardrobe.layer.revealed_surface','wardrobe.opening.topology'],
 [('within','outer_garment.opening','outer_garment'),('visible_through','inner_garment.surface','outer_garment.opening')],
 'Skin, a skin-tone patch or translucency through continuous fabric is a different surface or optical path.')
a('sf116_01','연속 피부색 안감 위의 투과 드레스 층','outer_dress_and_lining',
 ["a sheer dress layer remains outside a continuous skin-tone lining","the lining surface and its garment boundary remain distinct beneath the translucent outer texture"],
 ['wardrobe.layer.order','wardrobe.layer.transmission','wardrobe.lining.continuity','wardrobe.lining.color'],
 [('outside','dress.sheer_outer_layer','dress.continuous_skin_tone_lining'),('visible_through','dress.lining_boundary','dress.outer_texture')],
 'Actual bare skin or an opaque painted outer panel is a different surface; visible lining does not establish absence of other hidden layers.')
a('sf117_02','바깥으로 접혀 이중 띠가 된 같은 의복 윗경계','garment',
 ["the garment upper edge folds outward","that same fabric forms one continuous doubled band along the edge"],
 ['wardrobe.edge.fold_state','wardrobe.edge.layer_count'],
 [('folds_outward','garment.upper_edge','garment.outer_surface'),('forms','garment.folded_edge','garment.continuous_doubled_band')],
 'An attached independent band or soft hanging cowl has a different continuity; hidden stitching and manufacturing method remain unproven.')
# Clause review corrections: preserved object context is not an extra color or garment effect.
ROWS['sf014_01']['paths'].remove('wardrobe.sleeve.presence')
ROWS['sf103_04']['paths'].remove('wardrobe.accessories.bag.scale')
ROWS['sf103_04']['parts'][0]="the existing small bag surface is saturated red"
ROWS['sf077_03']['parts']=["fine closely spaced thread rows cross at right angles on the shirt cloth","the visible crossings alternate single-thread over-and-under steps across that grid"]
ROWS['sf077_03']['edges']=[('crosses','shirt.surface.horizontal_threads','shirt.surface.vertical_threads'),('alternates_at','shirt.single_thread_paths','shirt.surface.crossings')]

assert set(ROWS)==set(D), {'missing':sorted(set(D)-set(ROWS)),'extra':sorted(set(ROWS)-set(D))}
base_dictionary=json.loads((AS/'photo_prompt_tags.json').read_text())
slot_scopes=base_dictionary['candidate_semantic_policy']['slot_dimensions']
manifest=json.loads((AS/'photo_prompt_source_manifest.json').read_text())['sources']
existing_candidates={}
existing_profiles={}
for f in manifest:
 j=json.loads((AS/f['file']).read_text())
 if f['kind']=='candidate':
  for sl,vs in j.get('slots',{}).items():
   for v in vs: existing_candidates[(f['file'],sl,v['id'])]=v
 else:
  for v in j.get('profiles',[]):existing_profiles[v['id']]=v
for v in json.loads((AS/'photo_prompt_visual_obligations.json').read_text()).get('profiles',[]):existing_profiles[v['id']]=v
claim_limits=[
 'Only the complete selected visible variant is represented; a family or style name does not activate its sibling variants.',
 'Use the existing declared garment, accessory and wearer. A different owner or unsupported prerequisite makes this choice inapplicable.',
 'Visible boundaries and contact must be inspectable in the saved image; prompt wording, a painted imitation or unresolved occlusion is insufficient.',
 'Pixels do not certify fiber composition, hidden garment presence or absence, manufacturing history, functional performance, body measurements, biography, social class or desire.'
]
groups={}; decisions=[]; evidence=[]
for key,row in ROWS.items():
 d=D[key];card=CARDS[d['card_id']]
 cf=d['candidate_file_proposal']; pf=card['route_profiles'][0]
 if row['slot']:slot=row['slot']
 elif cf=='photo_prompt_textile_surface_extension.json':slot='surface_material'
 elif cf=='photo_prompt_color_relations_extension.json':slot='color'
 elif cf=='photo_prompt_accessory_structure_extension.json':slot='wearable_accessory'
 else:slot='garment_detail'
 file_slots=json.loads((AS/cf).read_text())['slots']
 assert slot in file_slots,(key,cf,slot)
 dims=slot_scopes[slot]
 # Effects use the exact same target/property spelling on every possible carrier.
 effects=[{'dimension':dim,'target':'main_subject','property':p} for dim in dims for p in row['paths']]
 parts=row['parts'];en='; '.join(parts)+'.'
 cid='spf_'+key;pid='spring_'+key
 assert all(cid!=old[2] for old in existing_candidates),(key,'existing candidate ID collision')
 assert pid not in existing_profiles,(key,'existing profile ID collision')
 relations=[{'id':'declared_owner','type':'declared_owner_scope','subject':row['owner'],'object':'main_subject'}]
 for i,(typ,sub,obj) in enumerate(row['edges'],1):
  relations.append({'id':f'edge_{i:02d}','type':typ,'subject':sub,'object':obj})
 candidate={
 'id':cid,'ko':row['ko'],'en':en,'weight':0.35,'tags':['clothing'],'for_any':['human'],
 'aliases':[row['ko'],en],'keywords':list(dict.fromkeys([row['ko'],en]+parts)),
 'embedding_text':' | '.join([row['ko'],en]+parts),'concept_units':parts,'relations':relations,
 'affected_dimensions':dims,'affected_properties':effects,'core_assertion_discovery':True}
 if d['requires_adult_context']:
  candidate['requires_all_tags']=['human','adult']
 components=[]
 for i,p in enumerate(parts,1):
  comp_id=f'component_{i:02d}'
  components.append({
  'id':comp_id,'match_terms':[p],'evidence_field':comp_id+'_phrase','evidence_terms':[p],'min_content_words':3,
  'instruction':'Keep this selected owner-bound structure readable in the photograph: '+p+'.',
  'render_gate':{'id':f'vo_{pid}_{i:02d}','review_scale':'native',
  'description':row.get('gate_descriptions',[])[i-1] if row.get('gate_descriptions') else 'Inspect this actual same-owner structure at native resolution: '+p+'. The declared surface, boundary and relational endpoints must resolve in this same saved image. Missing, occluded, printed, substituted or partial geometry fails.'}})
 graph_lines=[f"{r['subject']} {r['type']} {r['object']}" for r in relations]
 profile={
 'id':pid,'category':'spring_fashion_selected_visible_structure',
 'activation':{'exact_terms':[en],'requires_adult_character':d['requires_adult_context'],'semantic_discovery_requires_component_evidence':True,
 'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_selected_geometry','any_terms':[en]}]}},
 'semantics':{'definition':en,'paraphrase_examples':[row['ko']],'visual_components':parts,'contrast_examples':[row['contrast']],'claim_limits':claim_limits},
 'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},
 'concept_candidate':{'concept_terms':[row['ko'],en],'core_assertion_discovery':True,'affected_dimensions':dims,'affected_properties':effects},
 'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
 'reject_substitutes':[row['contrast']],
 'visual_relation':{
 'schema_version':'photo-visual-relation/v1','status':'advisory','owner_axis':'main_subject',
 'source':{'kind':'advisory_candidate','literal_evidence':parts,'priority':'P2','confidence':'high'},
 'entities':list(dict.fromkeys([row['owner'],'main_subject']+[x for r in row['edges'] for x in r[1:]])),
 'visible_regions':row.get('visible_regions') or [f'selected {row["owner"]} surface and boundaries', 'both endpoints of each selected structural relation'],
 'relations':graph_lines,'observable_effects':parts,'confusion_negatives':[row['contrast']],
 'observability':{'required_visible_regions':row.get('visible_regions') or [f'selected {row["owner"]} surface and boundaries','both endpoints of each selected structural relation'],
 'minimum_review_scale':'native','crop_policy':'A cropped required boundary cannot receive a pass.','occlusion_policy':'A hidden required endpoint remains unresolved in pixel review.',
 'proof_budget':{'thumbnail':'Check selected object placement and overall silhouette only.','native':'Resolve each component boundary and both relation endpoints.'},'ineligible_state':'UNSCORED'},
 'activation':{'hard_only_from_exact_source':True,'embedding_only_is_advisory':True,'all_required_components_coexist':True},
 'invariant_fields':['wearer identity and anatomy','unselected garment and accessory owners','camera pose lighting and setting outside the declared effects'],
 'flexible_fields':row['paths']}}
 bundle={
 'id':cid+'_bundle','primary_visual_proposition':en,'hard_profile_ids':[pid],
 'component_groups':[{'id':f'component_{i:02d}','visible_evidence':[p]} for i,p in enumerate(parts,1)],
 'candidate_ids':[cid],'candidate_slots':{cid:slot},'confusion_boundaries':[row['contrast']],
 'source_keywords':[row['ko'],en],'candidate_only':True,'activation_mode':'independent_component_request_evidence_only','relations':relations}
 k=(cf,slot,pf)
 group=groups.setdefault(k,{'candidate_file':cf,'slot':slot,'candidates':[],'profile_file':pf,'profiles':[],'visual_semantics':[],'context_extensions':[]})
 group['candidates'].append(candidate);group['profiles'].append(profile);group['visual_semantics'].append(bundle)
 # Exact equality is a narrow diagnostic, never proof of conceptual equivalence.
 exact=[{'file':f,'slot':s,'id':i} for (f,s,i),old in existing_candidates.items() if ' '.join(old.get('en','').casefold().split())==' '.join(d['en'].casefold().split())]
 neighbors=[]
 for n in card.get('existing_review_neighbors',[]):
  locs=[x for x in n.get('source_locations',[]) if x['file'] in {cf,pf,'photo_prompt_autumn_fashion_extension.json','photo_prompt_visual_obligations_autumn_fashion.json'}]
  if locs:neighbors.append({'entity_id':n['entity_id'],'source_locations':locs,'record_sha256':n.get('record_sha256'),'status':'lexical_lead_not_established_equivalent'})
 reason='New narrow variant for '+row['ko']+'. Its complete clauses are bound to '+', '.join(row['paths'])+'. Existing lexical leads have no established equality of owner, full geometry, prerequisites and declared effects; their IDs and content remain intact.'
 decisions.append({'draft_id':d['draft_id'],'decision':'new','candidate_id':cid,'profile_id':pid,'source_ids':d['source_ids'],'reason':reason})
 special=[]
 if key=='sf057_01':special.append('Every small opening rim is formed by actual knit yarn loops and continues into the surrounding knit surface; repeated nearby loop-like marks do not establish this boundary topology. Manufacturing process, exact gauge and fiber composition are not pixel duties.')
 if key=='sf103_04':special.append('The existing small bag is an owner prerequisite. Selection changes only bag-local color, preserving its size and type.')
 if key=='sf112_04':special.append('Only the exposed lower band boundary is scored for an independent visible connection. Absence of a clip concealed elsewhere is metadata and never a pixel proof.')
 if key=='sf077_03':special.append('Plain weave is represented by inspectable single-thread alternation, not by a named textile or an inferred weaving process.')
 if key=='sf014_01':special.append('A pre-existing tank owner is retained; the selected geometry affects shoulder-bridge width and connections without an extra sleeve-presence change.')
 if key=='sf082_01':special.append('The outer and inner garments are existing prerequisites. The material-slot effect changes transmission only and does not reorder, create or remove either garment.')
 evidence.append({
 'draft_id':d['draft_id'],'card_id':d['card_id'],'term_ids':d['term_ids'],'original_research_sentence':d['en'],
 'original_terms':[{'term_id':t,'label':TERMS[t]['label'],'original_description':TERMS[t]['original_description']} for t in d['term_ids']],
 'candidate_id':cid,'profile_id':pid,'bundle_id':cid+'_bundle','candidate_file':cf,'slot':slot,'profile_file':pf,
 'owner_binding':'Bind the existing '+row['owner']+' and its same wearer; reject if the final scene has no eligible owner. A source label does not create a new object.',
 'authored_variant_components':parts,'authored_variant_relations':relations,'effect_paths':row['paths'],
 'family_blueprint_handling':'Not copied. Only the current sentence-specific nodes and relationships are emitted; sibling alternatives remain independent.',
 'native_review_duties':[c['render_gate']['id'] for c in components],'contrast':row['contrast'],'special_claim_limits':special,
 'source_ids':d['source_ids'],'sources':[SOURCES[x] for x in d['source_ids']],
 'verification_basis':'Source support and access statuses come from the supplied upstream register. This arm independently authored physical variants and did not reread every source page.',
 'existing_lexical_neighbors':neighbors,'byte_equal_sentence_diagnostics':exact,
 'research_definition':card['definition_ko'],'research_confusion_boundaries':card['confusion_boundaries'],
 'qualification':{'source':'authored','profile_compile':'pending','index':'not_integrated','retrieval':'not_run','prompt':'not_run','runtime':'not_published','pixel':'not_run','user_acceptance':'not_requested'}})
fragment={'domain_writes':list(groups.values()),'decisions':decisions,'evidence':evidence}
(B/'data-fragment.json').write_text(json.dumps(fragment,ensure_ascii=False,indent=2)+'\n')
(B/'evidence-sidecar.json').write_text(json.dumps({'schema_version':'spring-fashion-arm-evidence/v1','arm':'ornament_shoe','records':evidence},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'drafts':len(D),'authored_rows':len(ROWS),'candidates':sum(len(g['candidates']) for g in groups.values()),'profiles':sum(len(g['profiles']) for g in groups.values()),'bundles':sum(len(g['visual_semantics']) for g in groups.values()),'components':sum(len(p['authored_components']['components']) for g in groups.values() for p in g['profiles']),'groups':len(groups),'fragment_sha256':hashlib.sha256((B/'data-fragment.json').read_bytes()).hexdigest()},indent=2))
