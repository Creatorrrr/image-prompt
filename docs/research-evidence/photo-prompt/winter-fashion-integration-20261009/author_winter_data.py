"""Author reviewed winter variants, preserving research/runtime separation."""
from pathlib import Path
import collections, hashlib, json, sys

ROOT = Path(sys.argv[1]).resolve()
RESEARCH = ROOT / 'docs/research-evidence/photo-prompt/winter-fashion-20261009'
OUT = ROOT / 'docs/research-evidence/photo-prompt/winter-fashion-integration-20261009'
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

# variant | Korean visible meaning | relation subject | type | object | actual effects
# Each line specializes the clause, rather than copying the family's relation/effect pool.
WIRE = '''
01.1|니트 커프가 외투 커프 밖으로 이어지는 층|inner knit cuff|extends_beyond|same wearer's outer coat cuff|layers.visible_edges
01.2|열린 코트 앞판 안에 별도 니트가 보이는 층|open coat panels|frame|same wearer's separate inner knit|layers.order,closure.open_front
04.1|눌린 봉제선 사이 솟은 가로 패딩 구획|recessed stitched lines|separate|inflated horizontal chambers of same puffer panel|structure.chambers,material.surface_relief
04.2|봉제선으로 구획된 얕은 다이아몬드 누빔|visible stitch lines|bound|shallow diamond cells of same quilted panel|structure.quilting,material.surface_relief
05.1|코를 가리지 않는 낮고 짧은 니트 잔털|short fiber halo|lies_over|same knit panel's readable stitches|material.fiber_halo
05.2|바탕 코에서 길게 뻗는 니트 잔털|long wispy fibers|project_from|same yarn's visible knitted ground|material.fiber_halo
06.1|원단 끝단이 읽히는 짧고 촘촘한 코트 파일|short dense pile|covers|same coat panel with readable fabric edge|material.pile_length,material.pile_density
06.2|자기 솔기 일부를 덮는 긴 코트 파일|long pile|projects_from_and_veils|same coat panel's seam|material.pile_length,layers.self_occlusion
07.1|뒤집힌 칼라에서 이어지는 매끈한 면과 털면|turned jacket collar's smooth face|continues_into|same collar's short woolly reverse|material.two_sided_surface,structure.turned_collar
07.2|직물 바탕 가장자리 위 말린 셰르파 파일|rounded curled pile|rises_from|same fleece jacket's textile-backed edge|material.pile_structure
08.1|매끈한 코트 몸판과 구별되는 칼라 파일 트림|pile trim|follows|same coat collar edge above smooth body panel|structure.trim_attachment,material.pile_structure
08.2|커프에 붙어 밖으로 뻗는 깃털형 트림|separate feather-like vanes|attach_and_project_from|same cuff edge|structure.trim_attachment,material.feather_surface
09.1|반전 지점에서 어긋나는 헤링본 사선|opposed diagonal runs|break_and_offset_at|same coat panel's direction reversal|pattern.geometry
09.2|뜬 코를 따라 반복되는 하운드투스 체크|broken-check color boundaries|follow|same knit panel's stitches|pattern.geometry,color.distribution
10.1|바탕 위 솟은 불규칙 부클레 고리|small irregular yarn loops|rise_from|same boucle panel's readable ground|material.yarn_loops
10.2|무늬를 지정하지 않는 짧은 플란넬 기모|short brushed nap|softens|same flannel panel surface|material.brushed_nap
11.1|바탕 홈 사이 솟은 코듀로이 파일 골|raised pile wales|alternate_with|same corduroy panel's narrow ground channels|material.pile_wales
11.2|파일 방향에 따라 명암이 달라지는 벨벳형 면|dense short pile|produces_directional_shading_on|same velvet-like panel|material.pile_structure,material.surface_sheen
12.1|부츠통 위 짧고 확산된 스웨이드형 기모|short diffuse nap|covers|same boot shaft|material.brushed_nap
12.2|굽힘 주름이 남는 매끈한 가죽형 면|shallow bending creases|interrupt|same smooth leather-like panel|material.surface_structure,material.drape
13.1|스커트 접힘을 따라가는 새틴형 하이라이트|smooth highlight band|follows|same satin-like skirt folds|material.surface_sheen,material.drape
13.2|저지 겉면의 작은 뜬 코|small face-side loops|belong_to|same jersey panel|material.knit_structure
14.1|중간층에만 속하는 플리스 털면|fuzzy fleece surface|covers|same separate midlayer|material.fiber_halo,layers.owner_binding
14.2|뒤집힌 커프의 매끈한 겉면과 기모 안면|brushed inner face|lies_beneath|same turned cuff's smoother outer face|material.two_sided_surface,structure.turned_cuff
15.1|작고 촘촘한 니트 코|small close stitches|cover|same knit panel|material.knit_scale
15.2|굵은 실로 읽히는 큰 청키 니트 고리|thick yarn|forms|same sweater panel's large readable loops|material.yarn_thickness,material.knit_scale
16.1|뜨개 기둥과 오목한 홈이 반복되는 리브|raised knitted columns|alternate_with|same top's recessed knit channels|material.knit_ribs
16.2|넓은 골과 넓은 홈의 와이드 리브|broad knitted ribs|alternate_with|same panel's wide recessed intervals|material.knit_ribs
17.1|같은 뜬 줄이 위아래로 교차하는 케이블|raised knitted strands|cross_over_and_under|other strands of same sweater panel|material.cable_crossing
17.2|별도 케이블과 질감 기둥이 나란한 아란형 니트|cable columns|stand_beside|textured-knit columns of same panel|material.cable_crossing,pattern.column_layout
18.1|가로 띠에 반복되는 작은 다색 니트 모티프|small multicolor motifs|repeat_in|horizontal bands of same knit|pattern.band_layout,color.distribution
18.2|아래 몸판과 구별되는 목어깨 요크 무늬|patterned band|follows|same sweater's neck-and-shoulder yoke above plain lower body|pattern.yoke_placement,color.distribution
19.1|마름모를 가로지르는 가는 사선의 아가일|thin diagonal lines|cross|contrasting diamond blocks of same knit panel|pattern.geometry,color.distribution
20.1|뜬 코에 맞는 큰 대비 색면|large contrasting color areas|follow|same knit panel's stitches|pattern.color_blocks,color.distribution
20.2|뒤집힌 뜨개 가장자리의 뒷실 플로트|separate yarn floats|span|same turned knit edge's reverse|material.reverse_yarn_path,structure.turned_edge
21.1|포인텔 구멍 아래 보이는 별도 불투명 이너|small repeating eyelets|open_through_and_reveal|same knitted ground over separate opaque inner layer|material.openwork,coverage.transmission,layers.order
21.2|큰 열린 고리 공간의 니트 메시|large open loop spaces|form|mesh-like area of same knit panel|material.openwork,coverage.transmission
22.1|뜬 바탕이 읽히는 퍼지 니트 가장자리|wispy fibers|soften|same knit's edge with visible knitted ground|material.fiber_halo
22.2|실 안에서 섞이는 밝고 어두운 멜란지 조각|fine light and dark flecks|intermingle_within|same knit yarn|color.distribution
23.1|착용자 발목 부근에 닿는 코트 밑단|tailored coat hem|ends_near|same wearer's ankles|length
23.2|힙 아래와 허벅지 사이에 끝나는 코트|shorter coat hem|ends_below|same wearer's hips above lower thighs|length,coverage.lower_body
24.1|두 단추열 아래 넓게 겹친 더블 앞판|two coat front panels|overlap_beneath|same coat's two button rows|structure.front_overlap,closure.button_rows
24.2|한 단추열로 좁게 겹쳐 닫히는 싱글 앞판|single-front coat panels|close_along|same coat's narrow overlap and one main button row|structure.front_overlap,closure.button_rows
25.1|반대 앞판 고리를 통과하는 더플 토글|coat toggle|passes_through|loop anchored on opposite front panel of same coat|closure.toggle_loop_path
25.2|토글 위 목선에 연결된 더플 후드|duffle coat hood|joins|same coat neckline above toggle fastenings|structure.hood_attachment,closure.toggle_fastening
26.1|같은 코트 벨트 아래 겹친 랩 앞판|coat front panels|overlap_under|belt tied around same coat|structure.front_overlap,closure.belt_path
26.2|몸판 볼륨 사이 허리만 조이는 코트 벨트|coat belt|indents|same coat waist between fuller upper and lower panels|closure.belt_path,fit.waist_distribution
27.1|몸통이 둥글고 밑단으로 좁아지는 코쿤 코트|rounded coat torso|narrows_toward|same coat's lower hem|fit.width_distribution
27.2|어깨에서 밑단으로 퍼지는 스윙 코트|coat body|widens_from|same coat shoulders toward flaring hem|fit.width_distribution,material.drape
28.1|어깨에서 상완 위로 내려오는 케이프 코트|cape panel|hangs_from|same wearer's shoulders over upper arms|structure.shoulder_support,coverage.upper_arm,material.drape
28.2|케이프의 경계 있는 틈을 통과하는 팔|same wearer's forearm|emerges_through|bounded slit in same cape panel|structure.arm_opening,coverage.arm_opening
29.1|트렌치 상부 앞판을 덮는 스톰 플랩|storm flap|overlaps|same trench coat's upper front panel|structure.flap_attachment,layers.self_overlap
29.2|허리 벨트와 구별되는 어깨 에폴레트|narrow epaulette|anchors_to|same coat shoulder above separate waist belt|structure.epaulette_attachment,closure.belt_path
30.1|코트 목선에 붙어 목을 감는 스카프 패널|scarf panel|joins_and_wraps_from|same coat neckline around same wearer's neck|structure.scarf_attachment,coverage.neck
30.2|코트와 경계가 분리된 자유 끝 스카프|separate scarf|lies_over|same wearer's coat with independent scarf ends|layers.order,structure.scarf_separation
31.1|기존 하의 위 허리 근처에 끝나는 푸퍼|puffer hem|ends_near|same wearer's waist above separate lower garment|length,coverage.waist,layers.visible_edges
31.2|구획 볼륨 사이 허리를 좁히는 푸퍼 벨트|puffer belt|narrows|same waist between inflated chambers above and below|closure.belt_path,fit.waist_distribution,structure.chambers
32.1|뒷밑단이 두 갈래인 피시테일 파카|parka rear hem|divides_into|two tail-like points of same garment|structure.rear_hem
32.2|가슴 아래에서 끝나는 아노락 짧은 지퍼|hooded pullover's short zipper|ends_above|same garment's continuous lower torso panel|closure.zipper_length,structure.hood_attachment
33.1|긴소매 이너 위 마감된 암홀의 민소매 겉층|finished outer armhole edges|frame|same wearer's separate long-sleeved inner layer|structure.armholes,layers.order
33.2|열린 외투 아래 분리된 얕은 누빔 라이너|shallow quilted liner|lies_beneath|same wearer's open outer coat|structure.quilting,layers.order
34.1|짧은 재킷 가장자리를 모으는 리브 커프와 밑단|ribbed cuffs and hem|gather|same short jacket edges|structure.edge_gathering,material.knit_ribs,length
34.2|자기 라펠에서 아래 여밈으로 향하는 비대칭 지퍼|asymmetric zipper|crosses_between|same jacket lapel and lower fastening|closure.zipper_path,structure.lapel
35.1|매끈한 몸판과 대비되는 넓은 털 칼라|broad woolly collar|contrasts_with|same jacket's smooth body panel|structure.collar,material.pile_structure
35.2|두 칼라 탭을 잇는 에비에이터 버클|collar buckle|joins|two collar tabs of same jacket|closure.collar_buckle_path
36.1|두 가디건 앞단을 잇는 자체 단추|cardigan buttons|join|two separate front edges of same cardigan|closure.button_path,structure.front_opening
36.2|자기 옆허리 끈으로 고정되는 랩 니트|crossing knit front panels|are_secured_by|tie at same garment's side waist|structure.front_overlap,closure.tie_path
37.1|칼라 아래 윗가슴에서 끝나는 니트 폴로 여밈|short knit-polo fastening|ends_on|same garment's upper chest beneath collar|structure.collar,closure.fastening_length
37.2|목선부터 밑단까지 이어지는 니트 지퍼|cardigan zipper|continues_from|same garment neckline to lower hem|closure.zipper_length,structure.front_opening
38.1|이너 몸판이 보이도록 어깨와 팔을 덮는 슈러그|shrug shoulder and arm sections|frame|same wearer's separate inner torso garment|coverage.shoulder_arm,layers.order
38.2|같은 착용자의 위허벅지에 끝나는 튜닉|tunic knit hem|ends_over|same wearer's upper thighs|length
39.1|높은 목과 두 마감 암홀의 민소매 니트|sleeveless knit torso|joins|high neck collar and two finished armholes of same top|structure.neckline,structure.armholes,coverage.shoulder_arm
39.2|뜨개면과 독립 밑단이 남는 짧은 니트 탑|knitted short top fabric|ends_at|same top's bounded lower edge|material.knit_structure,length
40.1|자기 위로 접혀 내려오는 터틀 칼라|high collar|folds_down_onto|same collar's own textile face|structure.neckline
40.2|목선의 여분 원단이 앞으로 처지는 카울|extra neckline fabric|hangs_from|same top neckline in forward cowl fold|structure.neckline,material.drape
41.1|평평한 아래변과 두 선 옆변의 스퀘어 목선|level lower neckline edge|meets|two upright side edges of same top|structure.neckline
41.2|중앙 패임 양옆 두 곡선의 하트 목선|two upper neckline curves|meet_at|central dip of same sweetheart top|structure.neckline
41.3|넓고 얕게 가로지르는 보트 목선|wide shallow neckline|runs_across|same top's upper chest|structure.neckline,coverage.shoulder
42.1|양어깨 아래 목선과 상완 소매의 오프숄더|top upper edge|lies_below|both shoulders of same wearer above sleeves around upper arms|structure.neckline,coverage.shoulder
42.2|열린 어깨 위 원단 다리가 남는 콜드숄더|shoulder fabric bridges|remain_above|bounded shoulder openings of same top|structure.shoulder_bridges,coverage.shoulder
42.3|앞판에서 착용자 뒷목으로 이어지는 홀터 끈|halter straps|connect|same top front panel around same wearer's back neck|structure.strap_path,coverage.neck
43.1|연결 목선 아래 경계가 닫힌 키홀|bounded keyhole opening|sits_below|same top's connected neckline|structure.opening,coverage.chest
43.2|자기 끝단을 가진 목선 메시 브리지|fine mesh panel|bridges|same neckline opening with own fabric edge|structure.opening_bridge,material.mesh,coverage.transmission
44.1|기존 몸통을 따르며 허리 굽힘 주름이 남는 니트|knit fabric|follows_with_bending_folds|same wearer's existing torso at waist|fit.contact_distribution,material.drape
44.2|옆솔기와 몸통 사이 좁은 간격이 남는 탑|top side seam|stands_narrowly_away_from|same wearer's torso|fit.local_ease
45.1|연속 이너 위 가슴 아래에서 끝나는 언더버스트 의복|underbust waist garment|ends_below|same wearer's bust over separate continuous inner top|length,layers.order,coverage.chest
45.2|코르셋 몸판의 곡선 컵 솔기와 세로 케이싱|curved cup seams|join_with|vertical casing lines on same corset-style bodice|structure.cup_seams,structure.casing
46.1|몸판 가슴 구역을 지나는 곡선 패널 연결선|curved seam|joins|same bodice panels through bust region|structure.panel_seams
46.2|몸판 가슴 부근에서 끝나는 짧은 다트|short tapered dart|ends_near|same bodice bust region|structure.dart
46.3|허리 솔기에 연결된 퍼지는 페플럼|short flaring peplum|joins_at|same garment waist seam|structure.peplum_attachment,fit.waist_distribution,material.drape
47.1|크롭 밑단과 기존 허리단 사이의 간격|cropped top hem|ends_above|same wearer's separate lower garment waistband|length,coverage.waist,layers.visible_edges
47.2|크롭 밑단과 만나는 높은 허리단|high waistband|reaches|same wearer's cropped top hem forming contiguous waist coverage|layers.visible_edges,coverage.waist
48.1|위아래 연결 원단을 남기는 옆허리 컷아웃|bounded side-waist opening|interrupts_between|same dress panel's upper and lower fabric connections|structure.cutout,coverage.waist
48.2|불투명 이너가 보이는 언더버스트 개구부|bounded underbust opening|reveals|same wearer's separate opaque inner layer|structure.cutout,layers.order,coverage.chest
49.1|위 연결 원단을 남긴 하이넥 긴소매 오픈백|bounded back opening|retains|upper fabric connection of same high-neck long-sleeved dress|structure.back_opening,structure.neckline,structure.sleeves,coverage.back
49.2|겨드랑이 아래 암홀로 별도 이너가 보이는 탑|deep armhole|extends_below_and_reveals|same wearer's underarm over separate inner layer|structure.armholes,coverage.underarm,layers.order
50.1|성인 의복 옆경계 밖으로 보이는 가슴 측면|adult wearer's garment side edge|bounds|same wearer's visible lateral bust region|coverage.lateral_bust
50.2|성인 탑 하단 경계 아래 보이는 가슴 하부|adult wearer's top lower edge|bounds|same wearer's visible lower-bust region|coverage.lower_bust
51.1|두 앞판을 매듭으로 잇는 가디건 끈|cardigan front ties|knot_between|two front panels of same cardigan|closure.tie_path,structure.front_opening
51.2|아래 슬라이더 밑에서만 벌어지는 투웨이 지퍼|lower zipper slider|bounds|same garment's closed panels above and separated panels below|closure.zipper_slider_state,structure.front_opening
52.1|분리된 연속 불투명 안층이 보이는 시어 겉층|sheer outer panel|reveals|same wearer's separate continuous opaque inner panel|coverage.transmission,layers.order
52.2|겹친 앞판 사이 틈에서 이너만 보이는 층|small overlap opening|reveals|same wearer's separate inner garment|structure.front_overlap,layers.order
53.1|몸판에서 스커트까지 이어지는 니트 드레스|knit torso fabric|continues_into|same dress skirt fabric|garment_type,material.knit_structure,structure.torso_skirt_join
53.2|하이넥 이너와 분리된 민소매 피나포어|sleeveless pinafore layer|lies_over|same wearer's separate high-neck top|garment_type,structure.armholes,layers.order
54.1|허리에서 A형 밑단으로 넓어지는 스커트|skirt panels|widen_from|same skirt waist toward A-shaped hem|fit.width_distribution
54.2|솟은 능선과 돌아간 골이 읽히는 플리츠|folded skirt panels|alternate_between|same skirt's ridges and recessed returns|structure.pleats,material.drape
54.3|힙과 위다리를 따른 뒤 아래에서 퍼지는 스커트|skirt upper panels|follow_then_widen_below|same wearer's hips and upper legs toward lower skirt|fit.width_distribution,fit.contact_distribution
55.1|무릎 위 꼭짓점이 있는 긴 스커트 옆트임|long skirt side slit|ends_at|visible apex above same wearer's knee|structure.slit,coverage.leg
55.2|봉제 트임과 구별되는 랩 스커트 겹침 벌어짐|wrap skirt front edge|separates_from|underlying panel of same skirt|structure.front_overlap,closure.wrap_state,coverage.leg
56.1|무릎 부근은 좁고 밑단은 완만히 넓은 바지|trouser lower legs|widen_from|same trousers' narrow knee sections toward hems|fit.leg_width_distribution
56.2|무릎 외곽이 둥글고 발목으로 좁아지는 바지|rounded trouser knee curves|taper_toward|same trousers' ankles|fit.leg_width_distribution
57.1|레깅스 밑단에서 같은 발 아래로 이어지는 스티럽|legging stirrup loops|continue_beneath|same wearer's feet from legging hems|structure.stirrup_path,coverage.foot
57.2|몸판과 두 긴 다리 원단이 연결된 캣수트|catsuit torso fabric|continues_into|both long leg sections of same garment|garment_type,structure.torso_leg_join,coverage.torso_leg
58.1|같은 다리면이 일부 투과되는 어두운 호지어리|dark hosiery textile|partially_transmits|same underlying leg surface|coverage.transmission,color
58.2|다리면을 덮는 경계 있는 불투명 타이츠|opaque tights fabric|covers|same underlying leg with distinct textile boundary|coverage.transmission
59.1|뒤집힌 가장자리의 어두운 겉층과 피부색 직물 안층|turned hosiery edge|reveals|same hosiery's dark sheer outer and skin-toned inner textile|structure.turned_edge,layers.order,coverage.transmission,color.distribution
59.2|맨살 대신 불투명 안감색이 투과되는 호지어리|dark outer hosiery layer|transmits|same hosiery's separate opaque skin-toned lining color|layers.order,coverage.transmission,color.distribution
60.1|불투명 층 위 연결된 마름모 피시넷|connected diamond mesh|repeats_over|same wearer's separate opaque inner layer|material.mesh,pattern.geometry,layers.order
60.2|스타킹 뒤면을 따라 이어지는 좁은 백심|narrow continuous back line|runs_down|same stocking's rear surface|structure.back_seam
61.1|허리 연결면과 구별되는 스타킹 허벅지 밴드|stocking upper edge|ends_at|same leg's separate upper-thigh band|length,structure.upper_band,coverage.upper_thigh
61.2|허리 벨트부터 스타킹 밴드까지 고정된 가터|waist belt strap|reaches_and_fastens_to|same wearer's stocking upper band|structure.garter_support_path,layers.owner_binding
62.1|발 원단과 이어져 무릎 아래에서 끝나는 삭스|sock foot section|continues_to|same sock's upper edge below wearer's knee|length,structure.foot_leg_join
62.2|호지어리와 발 의복에서 분리된 레그워머|separate knitted leg warmer|ends_over|same wearer's ankle hosiery above distinct foot garment|length,layers.order,material.knit_structure
63.1|같은 착용자의 무릎 아래에 끝나는 부츠통|boot shaft edge|ends_below|same wearer's knee|length
63.2|같은 발에서 무릎 위 허벅지로 이어지는 부츠통|boot upper edge|rises_above|same wearer's knee toward thigh continuous with boot foot|length,structure.foot_shaft_join
64.1|단단한 앞뒤 패널 사이 첼시 탄성 거싯|elastic side gusset|joins_between|same boot's solid front and rear panels|structure.side_gusset,material.elastic_panel
64.2|부츠통 둘레를 잇는 엔지니어 버클 스트랩|boot strap and buckle|join_around|same boot shaft|closure.buckle_strap_path
65.1|앞발과 뒤꿈치 모두 아래 두꺼운 플랫폼 밑창|thick boot sole|supports_beneath|same boot's forefoot and heel|structure.sole_thickness
65.2|부츠통 위끝이 바깥으로 이어져 접힌 커프|boot shaft upper edge|folds_out_into|continuous turned cuff of same shaft|structure.turned_cuff
65.3|발목 위 부드러운 주름으로 내려앉는 부츠통|soft shaft folds|settle_above|same boot ankle|material.drape,fit.shaft_slouch
66.1|어깨 위 두 독립 끝이 내려오는 직사각 스톨|rectangular stole|rests_across|same wearer's shoulders with two hanging ends|structure.stole_path,coverage.shoulder
66.2|목 둘레를 닫힌 직물 튜브로 감는 넥워머|continuous textile tube|encircles|same wearer's neck|structure.neck_tube,coverage.neck
67.1|얼굴 개구 주위로 머리와 목이 이어진 발라클라바|balaclava fabric|continues_around|same wearer's bounded face opening from head to neck|structure.head_neck_join,coverage.head_neck
67.2|자기 밴드로 연결된 두 귀마개 패드|earmuff band|connects|two ear-covering pads on same wearer|structure.band_pad_path,coverage.ear
67.3|머리 덮개에 두 스카프 끝이 붙은 후드 스카프|head-covering scarf section|joins|two hanging ends of same hooded scarf|structure.hood_scarf_join,coverage.head
68.1|공유 손가락 방 옆 독립 엄지칸의 미튼|separate thumb chamber|sits_beside|one shared finger chamber of same mitten|structure.hand_chambers,coverage.hand
68.2|손목부를 남기며 손끝 전에 끝나는 핑거리스 장갑|fingerless glove edge|ends_before|same wearer's finger tips above its own wrist section|length,coverage.hand
68.3|한 머프의 양끝에 들어간 같은 착용자 두 손|same wearer's hands|enter|two ends of one muff|structure.hand_tube,coverage.hand
69.1|겉의복 허리만 두르는 별도 코르셋 벨트|separate corset-style belt|encircles|same outer garment waist|closure.belt_path,fit.waist_distribution,layers.order
69.2|옷 입은 몸통 위 접합이 읽히는 하네스 끈|continuous fashion-harness straps|join_over|same wearer's separate clothed torso layer|structure.harness_path,layers.order
70.1|어깨 끝 바깥 상완에 연결된 드롭 소매|sleeve seam|lies_beyond|same wearer's shoulder tip along upper arm|structure.sleeve_join
70.2|좁게 닫힌 커프로 모이는 소매|gathered sleeve|narrows_into|same sleeve's closed cuff|structure.cuff_gathering,material.drape
70.3|긴 소매의 전용 구멍을 통과한 같은 손 엄지|same hand thumb|passes_through|dedicated opening in same extended sleeve cuff|structure.thumbhole_path,coverage.hand
71.1|두 의복 패널 아일릿열 사이 교차하는 끈|cord|crosses_between|two anchored eyelet rows on same garment panels|closure.lacing_path,structure.eyelets
71.2|직물면 위 겹친 납작한 시퀸 판|individual flat sequin plates|overlap_on|same fabric surface|structure.sequin_attachment,material.surface_sheen
71.3|스카프 끝에 붙어 각각 끝나는 프린지|fine fringe strands|attach_to_and_end_beyond|same scarf edge|structure.fringe_attachment
72.1|깨끗한 코트선 안의 별도 파인 니트 조합|clean-lined coat|frames|same wearer's separate fine-knit layer|garment_type,layers.order,material.knit_scale
72.2|칼라 셔츠 위 별도 무늬 니트 베스트|patterned knit vest|lies_over|same wearer's collared shirt|garment_type,layers.order,pattern.layout
73.1|셸 아래 플리스가 읽히는 아웃도어 조합|visible fleece midlayer|lies_beneath|same wearer's separate outer shell|garment_type,layers.order,material.fiber_halo
73.2|외투 패널 위 포켓과 조절 부품|bounded pockets and adjustment parts|attach_to|same technical-style outer garment|structure.pockets,closure.adjustment
74.1|보디수트 위 랩 니트와 별도 타이츠 레그워머|wrap knit and leg warmers|remain_separate_over|same wearer's bodysuit and tights respectively|garment_type,layers.order,structure.front_overlap
74.2|의복 가장자리에 붙은 두 고리와 꼬리의 리본|small bow's two loops and tails|attach_at|same garment edge|structure.bow_attachment
75.1|스터드 패널과 별도 체크 층의 펑크 조합|visible studs|attach_to|same garment panel beside separate check-pattern layer|structure.stud_attachment,layers.order,pattern.layout
75.2|외투에 붙은 경계 있는 패치 포켓과 여밈 탭|patch pockets and fastening tabs|belong_to|same utility-inspired coat|structure.pockets,closure.tabs
76.1|벨루어형 면과 별개 반사 장식의 조합|reflective ornaments|remain_separate_from|same outfit's velour-like textile surface|material.pile_structure,structure.ornament_attachment
76.2|파일 코트와 별도 큰 금속 액세서리 조합|large metallic accessories|remain_separate_from|same wearer's pile coat|garment_type,material.pile_structure,layers.order
77.1|열린 코트 안 불투명 이너 위 코르셋형 탑|open coat panels|frame|same wearer's corset-style top over separate opaque layer|garment_type,layers.order,closure.open_front
77.2|민소매 이브닝 의복 옆 별도 긴 장갑|long gloves|remain_separate_beside|same wearer's sleeveless evening garment|garment_type,layers.order,coverage.arm
78.1|스커트와 부츠 사이 최전면 불투명 타이츠|opaque tights|remain_foremost_between|same leg's skirt hem and boot top|layers.order,coverage.leg
78.2|상의 목선을 바꾸지 않고 가리는 스카프|scarf|covers|same top's otherwise wide neckline|layers.order,coverage.neck
79.1|양 의복을 유지하며 니트 목선을 드러내는 코트|open coat panels|leave_visible|same wearer's separate knit neckline|layers.order,closure.open_front
79.2|같은 다리에서 별도 경계를 가진 스커트와 호지어리|skirt hem and hosiery top|bound|one interval on same leg with independent textile edges|layers.visible_edges,length
'''

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def main():
    cards={c['id']:c for c in json.loads((RESEARCH/'semantic-cards.json').read_text())['cards']}
    proposals={p['id']:p for p in json.loads((RESEARCH/'candidate-proposals.json').read_text())['proposals']}
    specs={}
    for line in WIRE.strip().splitlines():
        code,ko,sub,typ,obj,props=line.split('|')
        family,var=code.split('.')
        key=f'WF{family}_D{int(var):02d}'
        assert key not in specs
        specs[key]=(ko,sub,typ,obj,props.split(','))
    assert set(specs)==set(proposals),(set(proposals)-set(specs),set(specs)-set(proposals))
    ext={'schema_version':'photo-prompt-research-extension/v1','slots':{},'visual_semantics':[]}
    registry={'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Selected winter garment surfaces, fastenings, layers and accessory paths; each visible variant is independently optional.','profiles':[]}
    mappings=[]
    for key,p in proposals.items():
        ko,sub,typ,obj,props=specs[key];card=cards[p['card_id']]
        en=p['en'].replace('the declared ','the ').replace('declared ','').replace('existing ','separate ')
        en=en.replace('only the explicitly requested lateral bust region','the lateral bust region').replace('only the explicitly requested lower-bust region','the lower-bust region')
        overrides={
            'WF47_D02':'the high waistband reaches the cropped top hem, forming contiguous textile coverage across the waist',
            'WF50_D01':"the adult wearer's garment side edge borders the visible lateral bust region",
            'WF50_D02':"the adult wearer's top lower edge borders the visible lower-bust region",
            'WF61_D01':"the stocking ends in a separate upper-thigh band, leaving a distinct textile edge below the waist",
        }
        en=overrides.get(key,en);en=en[:1].upper()+en[1:];en=en.rstrip('.')+'.'
        ident='winter_'+key.lower().replace('_d','_v').replace('_v0','_v')
        effects=[]
        for suffix in props:
            full='wardrobe.'+suffix
            for dim in (['appearance','material'] if suffix.startswith('material.') else ['appearance']):
                effects.append({'dimension':dim,'target':'main_subject','property':full})
        dims=list(dict.fromkeys(e['dimension'] for e in effects))
        relation={'id':ident+'_owner_relation','type':typ,'subject':sub,'object':obj}
        terms=[ko,en,f'{sub} {typ.replace("_"," ")} {obj}']
        candidate={'id':ident+'_candidate','ko':ko,'en':en,'weight':0.35,'tags':['clothing'],'aliases':terms[:2],'keywords':terms,'embedding_text':en+' | '+terms[-1],'concept_units':[en],'relations':[relation],'affected_dimensions':dims,'affected_properties':effects,'core_assertion_discovery':True,'for_any':['human']}
        if p['requires_explicit_adult_context']:
            candidate['tags'].append('adult')
            candidate['facets']={'safety_tier':'adult_only'}
        slot=p['proposed_slot'];ext['slots'].setdefault(slot,[]).append(candidate)
        limits=[card['observation_prerequisites_ko'],'Bind the named garment, its actual layers and both relation endpoints to the same wearer. A prerequisite absent from the authored scene is not established by a search hit.','This visible variant does not determine fiber content, insulation values, weather performance, wearer body dimensions or unseen construction.','Family alternatives and aesthetic labels remain optional. Partial or hidden endpoints do not pass the selected relation.']
        profile={'id':ident,'category':'winter_fashion_selected_visible_relation','activation':{'exact_terms':[en],'requires_adult_character':p['requires_explicit_adult_context'],'semantic_discovery_requires_component_evidence':True,'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'selected_visible_variant','any_terms':[en]}]}},'semantics':{'definition':en,'paraphrase_examples':[ko,terms[-1]],'visual_components':[en],'contrast_examples':[card['confusion_boundary_ko']],'claim_limits':limits},'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[{'id':'owner_bound_variant','match_terms':[en],'evidence_field':'owner_bound_variant_phrase','evidence_terms':[en],'min_content_words':3,'instruction':f'Preserve the selected owner-bound visible relationship: {en}','render_gate':{'id':'vo_'+ident+'_relation','review_scale':'native','description':f'{en} Verify {sub}, {obj}, and their {typ.replace("_"," ")} relationship on the named garment in the same image. Both endpoints and the joining surface or path must be readable; partial or hidden evidence does not pass.'}}]},'concept_candidate':{'concept_terms':terms[:2],'core_assertion_discovery':True,'affected_dimensions':dims,'affected_properties':effects},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':[card['confusion_boundary_ko']]}
        registry['profiles'].append(profile)
        ext['visual_semantics'].append({'id':ident+'_bundle','primary_visual_proposition':en,'hard_profile_ids':[ident],'component_groups':[{'id':'owner_bound_variant','visible_evidence':[en]}],'candidate_ids':[candidate['id']],'candidate_slots':{candidate['id']:slot},'confusion_boundaries':[card['confusion_boundary_ko']],'source_keywords':terms[:2],'candidate_only':True,'activation_mode':'component_complete_exact_only','relations':[relation]})
        mappings.append({'proposal_id':key,'card_id':p['card_id'],'candidate_id':candidate['id'],'profile_id':ident,'bundle_id':ident+'_bundle','slot':slot,'source_ids':p['source_ids'],'effects':effects,'relation':relation,'meaning_state':'selected_visible_variant_not_family_default','historical_existing_ids_preserved':card['existing_ids_to_review']})
    # Hidden specifications are available as interpretation context, never positive
    # search aliases or image obligations. No claimed test result is synthesized.
    contexts={}
    context_targets={
        'WF02':['winter_wf04_v1_candidate'],
        'WF03':['winter_wf04_v1_candidate'],
        'WF05':['winter_wf05_v1_candidate','winter_wf05_v2_candidate'],
        'WF20':['winter_wf20_v1_candidate','winter_wf20_v2_candidate'],
        'WF58':['winter_wf58_v1_candidate','winter_wf58_v2_candidate'],
    }
    for card_id,targets in context_targets.items():
        c=cards[card_id]
        for target in targets:
            slot=next(r['slot'] for r in mappings if r['candidate_id']==target)
            context=contexts.setdefault(slot,{}).setdefault(target,{'contexts':[]})
            context['contexts'].append({'id':card_id.lower()+'_specification_boundary','meaning':c['meaning_ko'],'claim_limits':c['confusion_boundary_ko']+' '+c['observation_prerequisites_ko']})
    # Equivalent old candidates receive language/context additions through the
    # supported append-only surface. Their authored IDs, prose and effects stay.
    reuse=[
        ('wardrobe_style','clt_ct008_v1','WF17',['솟은 뜬 줄이 교차하는 케이블 니트','raised cable-knit braid crossings']),
        ('surface_material','clt_ct087_v1','WF16',['뜨개 능선과 오목한 홈이 반복되는 리브','raised knitted columns and recessed rib channels']),
        ('surface_material','clt_ct089_v1','WF11',['파일 웨일과 바탕 홈이 반복되는 코듀로이','raised corduroy pile wales and ground channels']),
        ('garment_detail','clt_ct031_v2','WF46',['가슴 부근에서 끝나는 짧은 봉제 다트','short tapered bodice dart near the bust']),
        ('garment_detail','thumbhole_cuff_hand_opening','WF70',['긴 소매 커프의 전용 엄지 개구','dedicated thumb opening in an extended sleeve cuff']),
    ]
    for slot,ident,card_id,phrases in reuse:
        c=cards[card_id]
        contexts.setdefault(slot,{})[ident]={'paraphrases':phrases,'contexts':[{'id':'winter_'+card_id.lower()+'_equivalent_reading','meaning':phrases[0],'claim_limits':c['confusion_boundary_ko']}]}
    ext['existing_slot_context_extensions']=contexts
    names=[('photo_prompt_winter_fashion_extension.json','candidate',ext),('photo_prompt_visual_obligations_winter_fashion.json','visual_profile',registry)]
    manifest_path=ASSETS/'photo_prompt_source_manifest.json';manifest=json.loads(manifest_path.read_text())
    for name,kind,payload in names:
        dump(ASSETS/name,payload)
        if not any(s['file']==name for s in manifest['sources']):
            manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':1+max(s['load_order'] for s in manifest['sources'] if s['kind']==kind)})
    dump(manifest_path,manifest)
    terms=json.loads((RESEARCH/'term-plan.json').read_text())['terms']
    for t in terms:
        rows=[r for r in mappings if r['card_id'] in t['card_ids']]
        t['candidate_ids']=[r['candidate_id'] for r in rows];t['profile_ids']=[r['profile_id'] for r in rows]
        t['implementation_state']='source_registered_visible_variants' if rows else 'specification_or_existing_context_preserved_no_visual_certification'
        t['runtime_ready']=False
        t['source_registration_note']='Term labels do not activate the entire variant family. Linked alternatives require exact scene and owner review.'
    dump(OUT/'AUTHORED-MAPPING.json',{'schema_version':'winter-fashion-authored-map/v1','mappings':mappings,'hidden_specification_cards':['WF02','WF03'],'term_routes':terms,'count':len(mappings)})
    dump(OUT/'AUTHORING-SUMMARY.json',{'candidates':len(mappings),'profiles':len(registry['profiles']),'bundles':len(ext['visual_semantics']),'equivalent_existing_candidates_extended':len(reuse),'term_routes':len(terms),'slots':{k:len(v) for k,v in ext['slots'].items()},'registered_sources':[x[0] for x in names],'runtime_status':'not_yet_indexed_or_published','counts_do_not_prove_retrieval_or_pixels':True})
    print(json.dumps({'candidates':len(mappings),'profiles':len(registry['profiles']),'bundles':len(ext['visual_semantics'])}))

if __name__=='__main__':main()
