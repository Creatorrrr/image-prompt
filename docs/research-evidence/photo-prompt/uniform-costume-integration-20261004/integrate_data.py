"""Add equivalent wardrobe descriptions; retain earlier work and exact duties."""
from __future__ import annotations
import copy
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = HERE.parent / "uniform-costume-20261004"

# Existing component equivalents. These are NOT new exact activation aliases.
# Every clause keeps the original owner, cardinality, attachment and subtype.
EXISTING = r"""
costume_ccx_cc01_01|two shoulder bands connect directly to the apron chest panel above its waist support|앞치마의 어깨 띠 두 개가 허리 지지부 위의 가슴 패널에 직접 이어진다
costume_ccx_cc01_02|the apron band wraps outside the dress waist and ends in separate visible side ties|앞치마 띠가 드레스 허리 바깥을 감싸고 옆의 독립된 묶임 끝으로 이어진다
costume_ccx_cc01_03|the apron front cloth has its own lower edge above the separate dress bottom|앞치마 앞면 천이 별도 드레스 밑단 위에서 자체 아랫단으로 끝난다
costume_ccx_cc02_01|the same formal coat ends high at the front and splits into two lower rear tails behind the hips|같은 정장 코트가 앞에서는 짧게 끝나고 골반 뒤에서는 더 긴 뒤자락 두 개로 갈라진다
costume_ccx_cc02_02|an independently buttoned inner vest shows between the parted lapels of the outer coat|바깥 코트의 벌어진 라펠 사이에 자체 단추 여밈을 가진 안쪽 조끼가 보인다
costume_ccx_cc03_01|one broad collar runs over both shoulders and spreads across the upper back of that wearer|넓은 칼라 하나가 양 어깨를 지나 같은 착용자의 등 위쪽으로 펼쳐진다
costume_ccx_cc03_02|the knotted chest ribbon lies beneath the neckline while the separate collar remains visible above it|묶인 가슴 리본이 목선 아래에 놓이고 별도 칼라는 그 위에서 보이게 남는다
costume_ccx_cc05_01|each decorative shoulder fitting rests on a visible mounting base on the jacket|각 장식 어깨 부속이 재킷 위의 보이는 부착 밑판에 놓인다
costume_ccx_cc05_02|the decorative braided chest cord connects at both ends to that same jacket|장식용 땋은 가슴 끈의 양끝이 같은 재킷에 연결된다
costume_ccx_cc13_01|separate rigid armor pieces leave joint intervals filled by the same wearer's dark flexible cloth|분리된 단단한 갑주 조각 사이 관절 구간에 같은 착용자의 어둡고 유연한 천이 남는다
costume_ccx_cc13_02|overlapping plate margins stop at a bending joint and retain the gap through which it articulates|겹치는 판 가장자리들이 굽혀지는 관절에서 멈추고 그 관절이 움직이는 틈을 남긴다
costume_ccx_cc13_03|painted metallic highlights stay on the outer costume plates while the intervening joint cloth remains matte|칠한 금속풍 하이라이트는 바깥 코스튬 판에 놓이고 그 사이 관절 천은 무광으로 남는다
costume_ccx_cc15_01|the helmet has its own lower rim above an independently edged cloth neck layer|헬멧 자체의 아래 테두리 밑에 독립된 가장자리를 가진 천 목층이 놓인다
costume_ccx_cc15_02|a distinct dark visor surface ends at a readable boundary inside the helmet shell|독립된 어두운 바이저 면이 헬멧 외피 안쪽의 읽히는 경계에서 끝난다
costume_ccx_cc17_01|two artificial fur-covered ears fasten by their roots to a single headband|인공 모피 귀 두 개가 밑동에서 하나의 머리띠에 고정된다
costume_ccx_cc17_02|the artificial ear perimeter encloses a differently colored inner insert and stays separate from the wig|인공 귀의 테두리가 다른 색의 안쪽 삽입 면을 둘러싸고 가발과는 분리되어 있다
costume_ccx_cc26_01|several upright stitched channels continue down the separately bounded corset body|여러 개의 세로 봉제 채널이 독립된 코르셋 몸판을 따라 연속해서 내려온다
costume_ccx_cc26_02|two opposing rows of loops and crossing lace draw together the back of the corset itself|서로 마주 보는 고리 두 열과 교차 끈이 코르셋 자체의 뒷판을 모아 여민다
costume_ccx_cc32_01|loose fibers stay at the chosen garment border while the middle cloth panel remains whole|풀린 섬유는 선택한 옷 경계에 머물고 중앙 천 패널은 온전하게 남는다
costume_ccx_cc32_02|a separate repair cloth lies over the original textile and stitches follow its outer perimeter|별도 수선 천이 원래 직물 위에 겹치고 봉제 실이 수선 천의 바깥 둘레를 따른다
costume_ccx_cc35_01|thin luminous lines trace only the selected boundaries of the costume plates|가는 발광선이 선택한 코스튬 판의 경계만을 따라간다
costume_ccx_cc35_02|cloth immediately beside the localized costume light keeps a visibly nonluminous surface|국소 코스튬 광원 바로 옆의 천은 눈에 보이는 비발광 표면을 유지한다
costume_ccx_cc36_01|the gloved hand wraps its fingers around the prop grip and the contact remains visible|장갑 낀 손이 소품 손잡이를 손가락으로 감싸고 접촉 부분이 보이게 남는다
costume_ccx_cc36_02|one continuous grip joins the single sculpted body of the held costume prop|하나로 이어진 손잡이가 든 코스튬 소품의 단일 조형 몸체에 이어진다
clothing_ct028_v1|reflective bands follow sewn routes across the same work jacket cloth|반사 띠들이 같은 작업 재킷 천 위의 봉제 경로를 가로질러 이어진다
clothing_ct041_v2|the sailor neckline expands rearward into a wide rectangular cloth panel on the upper back|세일러 목선이 뒤쪽으로 넓어져 등 위쪽의 폭넓은 직사각 천 패널로 이어진다
clothing_ct043_v1|closely folded fabric forms one ruff ring around the wearer neck|촘촘히 접힌 천이 착용자 목 둘레에 하나의 러프 고리를 이룬다
clothing_ct141_v1|three linked kerosang fittings bridge the opposing edges of the open kebaya front|연결된 케로상 부속 세 개가 열린 케바야 앞판의 마주 보는 가장자리 사이를 잇는다
clothing_ct141_v2|the separate kebaya top overlaps a sarong that wraps around the lower body|별도의 케바야 상의가 하체를 감싸 입은 사롱 위에 겹친다
"""

# atom | stable slug | owner file bucket | slot | property | canonical EN/KO
# | equivalent EN/KO. Semicolons delimit independently necessary components.
NEW = r"""
U01|contrasting_robe_sleeves|traditional_clothing_detail|garment_detail|wardrobe.details.body_sleeve_color_boundary|the long robe body forms one color field; contrasting sleeves begin at that robe's armhole boundaries|긴 옷의 몸판이 하나의 색면을 이룬다; 대비되는 소매색이 같은 옷의 진동 경계에서 시작된다|the torso cloth keeps its selected body color; each differently colored sleeve joins that same body at the arm opening|몸통 천이 선택한 몸판색을 유지한다; 다른 색의 각 소매가 팔 구멍에서 같은 몸판에 이어진다
U02|sleeveless_robe_over_inner_sleeves|traditional_clothing_detail|garment_detail|wardrobe.layers.sleeveless_outer_robe|the outer robe has open sleeveless armholes; the independent inner garment sleeves emerge through those openings on the same wearer|겉포는 소매 없는 열린 진동을 가진다; 같은 착용자의 독립된 안쪽 옷 소매가 그 열린 부분으로 나온다|the long outer layer leaves both arm openings free of outer sleeves; visible inner sleeves pass through those outer arm openings|긴 바깥 층의 양쪽 팔 구멍에는 겉소매가 없다; 보이는 안쪽 소매가 그 겉옷 팔 구멍을 통과한다
U03|robe_waist_join_pleats|traditional_clothing_detail|garment_detail|wardrobe.details.robe_waist_join|the robe upper body ends at a sewn waist join; lower cloth pleats descend directly from that same join|포의 상체 몸판이 봉제된 허리 접합선에서 끝난다; 아래 천의 주름들이 같은 접합선에서 직접 내려온다|one upper robe section joins its lower section along the waist seam; the lower section folds outward from that continuous seam|한 포의 상체 구간이 허리 봉제선을 따라 아래 구간에 이어진다; 아래 구간이 그 연속된 봉제선에서 주름져 펼쳐진다
U06|shoulder_draped_empty_sleeve|costume_cosplay|garment_detail|wardrobe.layers.shoulder_draped_coat|a separate fur-edged short coat rests on one shoulder over the inner jacket; its unoccupied sleeve hangs below that shoulder; a visible coat support cord holds that outer coat|모피 테두리의 별도 짧은 코트가 안쪽 재킷 위 한 어깨에 놓인다; 비어 있는 코트 소매가 그 어깨 아래로 내려온다; 보이는 코트 지지끈이 그 겉코트를 잡아 준다|one shoulder carries a short outer coat with fur along its edge; the hanging outer sleeve contains no arm; the draped coat is supported by its own readable cord|한 어깨가 가장자리에 모피가 있는 짧은 겉코트를 지지한다; 내려온 겉소매 안에는 팔이 없다; 걸친 코트를 그 자체의 읽히는 끈이 지지한다
U07|angular_czapka_top_brim|accessory_structure|wearable_accessory|wardrobe.accessories.angular_cap|a four-cornered top plate sits above the cap body; a separate brim projects below that angular top|네 모서리 윗판이 모자 몸체 위에 놓인다; 별도의 챙이 그 각진 윗판 아래에서 돌출한다|the cap crown ends in a distinct quadrangular upper shape; its lower body retains an independent projecting visor edge|모자 정수리 부분이 구분되는 사각 윗형태로 끝난다; 아래 몸체는 독립적으로 돌출하는 챙 가장자리를 유지한다
U09|jacket_attached_false_vest|clothing_structure|garment_detail|wardrobe.details.attached_vest_panel|a vest-like front panel is joined to the short jacket construction; that panel shares the jacket attachment rather than forming a separately worn waistcoat|조끼처럼 보이는 앞패널이 짧은 재킷 구조에 이어져 있다; 그 패널은 별도로 입은 조끼를 이루지 않고 재킷의 부착부를 공유한다|the short outer jacket carries its own sewn imitation-vest front; the imitation front belongs to that jacket instead of an independent inner vest|짧은 겉재킷이 자체 봉제된 모조 조끼 앞판을 가진다; 모조 앞판은 독립된 속조끼 대신 그 재킷에 속한다
U11|tall_fur_headwear|accessory_structure|wearable_accessory|wardrobe.accessories.tall_fur_cap|a tall fur-textured cap has a separate outline above the head; its lower edge sits on the same tunic wearer|높은 모피 질감 모자가 머리 위에서 별도 외곽을 가진다; 그 아래 가장자리가 같은 튜닉 착용자의 머리에 놓인다|the head supports a high cap volume with a fur-covered surface; the cap rim stays distinct from the wearer's hair beneath it|머리가 모피로 덮인 표면의 높은 모자 부피를 지지한다; 모자 테두리가 그 아래 착용자의 머리카락과 구분되어 남는다
U15|green_coat_tan_shirt_taupe_trousers|costume_cosplay|costume_style|wardrobe.layers.service_palette|the green service coat opens over a separate tan shirt; separate taupe trousers continue below that coat on the same wearer|녹색 근무정복 코트가 별도의 탠색 셔츠 위에서 열린다; 같은 착용자의 별도 토프색 바지가 그 코트 아래로 이어진다|a green outer coat surrounds the visible tan inner shirt; the wearer's lower garment remains a distinct taupe pair of trousers|녹색 겉코트가 보이는 탠색 속셔츠를 둘러싼다; 착용자의 하의는 구분되는 토프색 바지로 남는다
U16|blue_coat_over_white_shirt|costume_cosplay|costume_style|wardrobe.layers.blue_white_service|the blue service coat retains its own front edges; a separate white shirt shows inside that coat opening|청색 정복 코트가 자체 앞판 가장자리를 유지한다; 별도 흰 셔츠가 그 코트의 열린 안쪽에서 보인다|the blue outer jacket frames an independent white inner shirt; the white cloth remains inside the outer lapel boundaries|청색 겉재킷이 독립된 흰 속셔츠를 둘러싼다; 흰 천이 바깥 라펠 경계 안쪽에 남는다
U17|utility_pockets_beside_closure|clothing_structure|garment_detail|wardrobe.details.utility_pocket_closure|the utility jacket has a distinct central closure; bounded pocket openings attach to that jacket body beside the closure|작업 재킷에 구분되는 중앙 여밈이 있다; 경계가 있는 주머니 입구들이 여밈 옆의 같은 재킷 몸판에 붙는다|one closing edge runs down the utility top front; independent pocket mouths lie on either selected panel beside that edge|하나의 여밈 가장자리가 작업 상의 앞면을 따라 내려온다; 독립된 주머니 입구들이 그 가장자리 옆의 선택한 패널에 놓인다
U20|blue_frock_collar_cuffs|costume_cosplay|garment_detail|wardrobe.details.blue_frock_edges|the visible frock collar has the same blue color as its body; the visible cuff cloth remains blue like that same frock|보이는 프록 칼라가 몸판과 같은 청색이다; 보이는 커프 천이 같은 프록처럼 청색으로 남는다|the neckline cloth belongs to the selected blue frock color field; the exposed sleeve ends retain that matching blue cloth|목선 천이 선택한 청색 프록의 색면에 속한다; 드러난 소매 끝들이 그와 일치하는 청색 천을 유지한다
U21|separate_flared_trouser_hems|clothing_structure|garment_detail|wardrobe.details.flared_trouser_hem|two trouser legs remain separate below the knees; each lower leg widens toward its own hem|두 바지통이 무릎 아래에서 각각 분리된 채 남는다; 각 아랫바지통이 자체 밑단을 향해 넓어진다|independent left and right pant tubes continue down the lower legs; their bottom openings are wider than the knee regions|독립된 좌우 바지 원통이 아랫다리를 따라 이어진다; 각 아래 입구가 무릎 영역보다 넓다
U22|norfolk_pleats_under_belt|clothing_structure|garment_detail|wardrobe.details.belt_over_vertical_pleats|vertical pleats run down the selected coat panels; a separate waist belt crosses those same coat pleats|세로 주름이 선택한 코트 패널을 따라 내려온다; 별도의 허리 벨트가 같은 코트 주름들을 가로지른다|long folded cloth lines descend along the coat body; a horizontal outer belt encircles that body across the folds|긴 접힌 천 선들이 코트 몸판을 따라 내려온다; 가로 겉벨트가 접힘을 가로질러 같은 몸판을 둘러싼다
U23|fabric_flight_coverall_zips|clothing_structure|garment_detail|wardrobe.details.coverall_zip_pockets|one fabric coverall continues from torso into two trouser legs; its central front zipper remains distinct from the selected pocket zippers|하나의 직물 일체복이 몸통에서 두 바지통으로 이어진다; 중앙 앞지퍼가 선택한 주머니 지퍼들과 구분되어 남는다|the cloth flight suit crosses the waist as one garment; one main opening zipper and independent pocket zip openings belong to that same suit|천 비행복이 하나의 의복으로 허리를 가로질러 이어진다; 주 여밈 지퍼 하나와 독립된 주머니 지퍼 입구들이 같은 복장에 속한다
U25|helmet_connected_suit_neck|costume_cosplay|wearable_accessory|wardrobe.accessories.integrated_helmet|the enclosing helmet and visor have their own head boundaries; the helmet lower edge joins the suit neck assembly|감싸는 헬멧과 바이저가 자체 머리 경계를 가진다; 헬멧 아래 가장자리가 복장 목 연결부에 이어진다|one helmet shell surrounds the selected head area; its bottom rim meets a visibly connected suit neck fitting|하나의 헬멧 외피가 선택한 머리 영역을 둘러싼다; 그 아래 테두리가 눈에 보이게 연결된 복장 목 부속에 닿는다
U27|breastplate_cloth_ruff_layers|costume_cosplay|garment_detail|wardrobe.layers.breastplate_ruff|a separate breastplate lies outside the cloth uniform; a separately edged ruff encircles the neck above that breastplate|별도 흉갑이 천 제복 바깥에 놓인다; 별도 가장자리를 가진 러프가 그 흉갑 위에서 목을 둘러싼다|the cloth garment remains beneath an independently bounded chest plate; the folded neck ruff retains its own edge above the plate|천 의복이 독립된 경계의 가슴판 아래에 남는다; 접힌 목 러프가 가슴판 위에서 자체 가장자리를 유지한다
U28|yellow_black_uniform_sections|costume_cosplay|garment_detail|wardrobe.color.yellow_black_sections|yellow and black areas occupy the selected uniform panels; their color boundaries belong to the same wearer's garment|황색과 검정 영역이 선택한 제복 패널을 차지한다; 그 색 경계들이 같은 착용자의 의복에 속한다|one selected uniform carries contrasting yellow and black cloth sections; those sections stay on the garment instead of a nearby flag|하나의 선택한 제복이 대비되는 황색과 검정 천 구간을 가진다; 그 구간들은 주변 깃발 대신 의복 위에 남는다
U31|domed_helmet_with_tunic|costume_cosplay|costume_style|wardrobe.layers.helmet_tunic|a domed helmet with a separate rim sits on the wearer's head; the same wearer has a separate tunic body below that headwear|별도 테두리가 있는 둥근 헬멧이 착용자의 머리에 놓인다; 같은 착용자가 그 머리wear 아래에 별도 튜닉 몸판을 입고 있다|the selected headwear has a rounded helmet crown; a separately bounded tunic belongs to that helmet wearer|선택한 머리wear에 둥근 헬멧 정수리 부분이 있다; 별도 경계가 있는 튜닉이 그 헬멧 착용자에게 속한다
U32|red_coat_outer_leg_stripe|costume_cosplay|costume_style|wardrobe.layers.red_coat_striped_trousers|a red coat remains a separate upper garment; a yellow stripe runs down the outer trouser seam of that same wearer|적색 코트가 별도 상의로 남는다; 노란 줄이 같은 착용자의 바지 바깥 봉제선을 따라 내려온다|the red tunic has its own lower edge above the trousers; yellow trim follows the outside length of those trouser legs|적색 튜닉이 바지 위에서 자체 아랫단을 가진다; 노란 장식이 그 바지통 바깥 길이를 따라간다
U37|continuous_coverall_front_closure|clothing_structure|garment_detail|wardrobe.details.one_piece_coverall|the coverall cloth body continues across the waist into the trouser section; a separate front closure runs along that same garment body|커버올 천 몸체가 허리를 가로질러 바지 구간으로 이어진다; 별도 앞여밈이 같은 의복 몸체를 따라 이어진다|one continuous garment surrounds the torso and separate legs; its own opening edge lies along the front rather than ending at a jacket hem|하나의 연속된 의복이 몸통과 분리된 다리를 둘러싼다; 자체 열린 가장자리가 재킷 밑단에서 끝나는 대신 앞면을 따라 놓인다
U38|plain_top_separate_trousers|clothing_structure|garment_detail|wardrobe.layers.plain_separates|the plain sweatshirt ends at its own lower hem; separate trousers begin beneath that hem on the same wearer|단색 스웨트셔츠가 자체 아랫단에서 끝난다; 별도 바지가 같은 착용자의 그 밑단 아래에서 시작된다|the single-color upper garment has a readable ending edge; an independent lower garment continues below that edge|단색 상의에 읽히는 끝 가장자리가 있다; 독립된 하의가 그 가장자리 아래로 이어진다
U40|loose_scrub_separates|clothing_structure|garment_detail|wardrobe.layers.scrub_separates|a loose scrub top ends at its own hem; independent scrub trousers remain a separate lower garment on that wearer|여유 있는 스크럽 상의가 자체 밑단에서 끝난다; 독립된 스크럽 바지가 같은 착용자의 별도 하의로 남는다|the loose medical-style top has a free lower edge; the wearer has separate trousers underneath rather than a continuous dress|여유 있는 의료풍 상의에 자유로운 아랫단이 있다; 착용자가 연속된 원피스 대신 그 아래에 별도 바지를 입는다
U42|fabric_hood_coverall_face_opening|clothing_structure|garment_detail|wardrobe.details.hood_coverall_join|the fabric hood joins the coverall neck; the hood retains a separate soft-edged opening around the face|직물 후드가 커버올 목에 이어진다; 후드가 얼굴 둘레에 별도의 부드러운 가장자리 입구를 유지한다|cloth from the selected hood continues to the suit neckline; a visible face opening remains bounded by that hood cloth|선택한 후드 천이 복장 목선으로 이어진다; 보이는 얼굴 입구가 그 후드 천의 경계 안에 남는다
U44|single_uniform_button_row|clothing_structure|garment_detail|wardrobe.details.single_button_front|one vertical button row belongs to the selected uniform front; the garment closing edge follows that single row|하나의 세로 단추열이 선택한 제복 앞판에 속한다; 의복 여밈 가장자리가 그 단일 열을 따라간다|the uniform front carries one line of separate buttons; its own front opening remains aligned to that one button line|제복 앞판이 분리된 단추들의 한 줄을 가진다; 자체 앞여밈이 그 하나의 단추 선에 맞춰 남는다
U45|front_belt_rear_dress_zip|clothing_structure|garment_detail|wardrobe.details.belt_rear_zip|a separate red belt wraps outside the dress waist; an independent zipper closure runs on the back of that same dress|별도 적색 벨트가 드레스 허리 바깥을 감싼다; 독립된 지퍼 여밈이 같은 드레스의 뒷판을 따라 이어진다|the dress front has its own red waist band accessory; the garment closing zip belongs to the rear dress panel|드레스 앞면에 자체 적색 허리 띠 액세서리가 있다; 의복 여밈 지퍼가 드레스 뒤 패널에 속한다
U47|neck_scarf_separate_hair_ornament|accessory_structure|wearable_accessory|wardrobe.accessories.scarf_hair_ornament|a raised scarf end extends from the wearer's neck accessory; a separate ornament attaches to the same wearer's hair above it|올라온 스카프 끝이 착용자의 목 액세서리에서 이어진다; 별도 장식이 그 위 같은 착용자의 머리카락에 붙는다|one projecting scarf tip belongs to the collar area; an independently edged hair decoration sits above it on that same head|하나의 돌출된 스카프 끝이 목깃 영역에 속한다; 독립된 가장자리의 머리 장식이 같은 머리에서 그 위에 놓인다
U53|chef_overlapping_double_front|clothing_structure|garment_detail|wardrobe.details.chef_double_front|the chef jacket front panels overlap; two rows of separate buttons attach to that same jacket front|조리 재킷 앞패널들이 겹친다; 분리된 단추들의 두 열이 같은 재킷 앞판에 붙는다|one kitchen-style jacket has a crossing front closure; an independent button line lies on each selected side of that front|하나의 주방풍 재킷이 교차하는 앞여밈을 가진다; 독립된 단추 선이 그 앞판의 선택한 각 측면에 놓인다
U55|white_collar_cuffs_black_dress|clothing_structure|garment_detail|wardrobe.details.white_trim_black_dress|the white collar follows the black dress neckline; matching white cuffs end the sleeves of that same dress|흰 칼라가 검정 드레스의 목선을 따른다; 일치하는 흰 커프스가 같은 드레스의 소매를 끝맺는다|a separately edged white neck trim belongs to the black dress body; white sleeve-end bands attach to that very dress|별도 가장자리의 흰 목 장식이 검정 드레스 몸판에 속한다; 흰 소매 끝 띠들이 바로 그 드레스에 붙는다
U57|sailor_lines_follow_collar|clothing_structure|garment_detail|wardrobe.details.collar_border_lines|the selected parallel lines lie within the sailor collar cloth; the lines follow that same collar edge with their chosen count|선택한 평행 선들이 세일러 칼라 천 안에 놓인다; 선들이 선택한 개수대로 같은 칼라 가장자리를 따른다|the collar itself carries a chosen number of narrow edge stripes; every stripe turns with the perimeter of that collar panel|칼라 자체가 선택한 개수의 가는 가장자리 줄을 가진다; 모든 줄이 그 칼라 패널의 둘레를 따라 꺾인다
U60|gown_separate_selected_cap|costume_cosplay|wearable_accessory|wardrobe.accessories.academic_cap|the selected academic cap has its own crown boundary above the head; a separate gown rests on the shoulders of that same wearer|선택한 학위 모자가 머리 위에서 자체 정수리 경계를 가진다; 별도 가운이 같은 착용자의 어깨에 놓인다|the headwear remains an independent selected academic shape; the garment below is a separately edged shoulder-supported gown|머리wear가 독립적으로 선택한 학위 모자 형태로 남는다; 그 아래 의복은 별도 가장자리의 어깨 지지 가운이다
U62|habit_hood_separate_waist_cord|traditional_clothing_detail|garment_detail|wardrobe.details.habit_cord_hood|the habit tunic remains a continuous cloth body; a separate cord gathers its waist; the hood or capuche has its own edge above that tunic|수도복 튜닉이 연속된 천 몸판으로 남는다; 별도 끈이 그 허리를 모아 준다; 후드 또는 카푸슈가 그 튜닉 위에 자체 가장자리를 가진다|one long tunic surrounds the wearer's torso and lower body; an independent rope belt encircles the tunic waist; a separately bounded hood layer lies at its neck|하나의 긴 튜닉이 착용자의 몸통과 하체를 둘러싼다; 독립된 로프 벨트가 튜닉 허리를 감싼다; 별도 경계가 있는 후드 층이 그 목에 놓인다
U64|kesa_patchwork_outer_border|traditional_clothing_detail|garment_detail|wardrobe.details.patchwork_border|rectangular joined cloth blocks form the inner kesa field; a separate cloth border surrounds that whole patchwork field|접합된 직사각 천 조각들이 가사 안쪽 면을 이룬다; 별도의 천 테두리가 그 전체 패치워크 면을 둘러싼다|an inner array of sewn rectangular pieces fills the selected robe panel; a continuous outer band encloses that same array|봉제된 직사각 조각들의 안쪽 배열이 선택한 옷 패널을 채운다; 연속된 바깥 띠가 같은 배열을 둘러싼다
U65|white_top_red_hakama_layers|traditional_clothing_detail|garment_detail|wardrobe.layers.white_red_hakama|the white upper garment has its own lower boundary; a separate red hakama begins below that upper garment|흰 상의가 자체 아래 경계를 가진다; 별도의 붉은 하카마가 그 상의 아래에서 시작된다|one independently bounded white top sits above the waist; the red pleated hakama remains a separate lower garment on that wearer|독립된 경계의 흰 상의 하나가 허리 위에 놓인다; 붉은 주름 하카마가 같은 착용자의 별도 하의로 남는다
U68|grey_yoke_black_body_color_neck|costume_cosplay|garment_detail|wardrobe.details.yoke_body_neck_palette|the grey shoulder yoke joins the black outer uniform body; a separate department-color neck layer shows within its opening|회색 어깨 요크가 검정 바깥 제복 몸판에 이어진다; 별도 부서색 목층이 그 열린 부분 안에서 보인다|a grey upper shoulder section belongs to the black outer jacket; an independent colored inner collar remains visible at that jacket neck|회색 윗어깨 구간이 검정 겉재킷에 속한다; 독립된 색 있는 속깃이 그 재킷 목에서 보이게 남는다
U69|lapel_chain_separate_inner_neck|accessory_structure|wearable_accessory|wardrobe.accessories.lapel_chain|the selected chain attaches to the maroon outer lapel; the raised inner neckline remains a separate garment layer behind it|선택한 사슬이 적갈색 바깥 라펠에 붙는다; 올라온 안쪽 목선이 그 뒤 별도 의복 층으로 남는다|a distinct small chain fitting belongs to the burgundy coat front; an independently edged undershirt neck rises within that coat|구분되는 작은 사슬 부속이 버건디 코트 앞판에 속한다; 독립된 가장자리의 속셔츠 목이 그 코트 안에서 올라온다
U70|work_suit_narrow_shoulder_color|costume_cosplay|garment_detail|wardrobe.details.narrow_shoulder_trim|the work-style suit remains one selected outer garment; narrow department-color trim follows its shoulder area|작업복풍 복장이 하나의 선택한 겉의복으로 남는다; 가는 부서색 장식이 그 어깨 영역을 따른다|one work suit has a continuous selected body; its contrasting identifying color stays within a narrow shoulder strip|하나의 작업복이 연속된 선택 몸판을 가진다; 대비되는 식별색이 가는 어깨 띠 안에 머문다
U72|hood_belt_cape_layers|costume_cosplay|garment_detail|wardrobe.layers.hood_belt_cape|a separate hood surrounds the head above the selected suit; a cape hangs from the same wearer's belt; the cape retains its own edge below that belt|별도 후드가 선택한 복장 위에서 머리를 둘러싼다; 케이프가 같은 착용자의 벨트에서 내려온다; 케이프가 그 벨트 아래에 자체 가장자리를 유지한다|an independently edged head covering lies outside the suit; a hanging cloth cape joins the waist support; the cape bottom remains separate from the lower suit panels|독립된 가장자리의 머리 가리개가 복장 바깥에 놓인다; 내려온 천 케이프가 허리 지지부에 이어진다; 케이프 밑단이 복장 아래 패널들과 분리되어 남는다
"""

COLOR_ATOMS = {"U01", "U15", "U16", "U20", "U28", "U32", "U45", "U47", "U55", "U65", "U68", "U69", "U70"}

def read(path): return json.loads(path.read_text())
def digest(value): return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def append_unique(seq, values):
    added = [x for x in values if x not in seq]
    seq.extend(added)
    return added
def candidate_id(profile_id):
    if profile_id.startswith("costume_ccx_"): return profile_id.removeprefix("costume_")
    if profile_id.startswith("clothing_ct"): return profile_id.replace("clothing_", "clt_", 1)
    return profile_id

def main():
    paths = sorted(set(ASSETS.glob("photo_prompt*extension*.json")) | set(ASSETS.glob("photo_prompt_visual_obligations*.json")) | {ASSETS / "photo_prompt_tags.json"})
    docs = {p: read(p) for p in paths}
    originals = copy.deepcopy(docs)
    baseline = HERE / "baseline"
    baseline.mkdir(exist_ok=True)
    # Never overwrite a saved pre-edit baseline on reruns.
    for path in paths:
        dest = baseline / path.name
        if not dest.exists(): dest.write_bytes(path.read_bytes())
    state = HERE / "working-tree-before.txt"
    if not state.exists(): state.write_text(subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True))
    profiles = {p["id"]: (path, p) for path, d in docs.items() for p in d.get("profiles", [])}
    entries = {e["id"]: (path, slot, e) for path, d in docs.items() for slot, values in d.get("slots", {}).items() for e in values}
    atoms = {a["id"]: a for a in read(RESEARCH / "relation-proposals.json")["atoms"]}
    log = {"schema_version": "uniform-costume-integration/v1", "existing_profiles": [], "new_profiles": [], "candidate_changes": [], "source_files": [], "research_dispositions": []}
    for line in EXISTING.strip().splitlines():
        pid, en, ko = line.split("|")
        path, p = profiles[pid]
        components = p["authored_components"]["components"]
        assert len(components) == 1, pid
        changes = append_unique(p["semantics"].setdefault("paraphrase_examples", []), [en, ko])
        append_unique(p["concept_candidate"].setdefault("concept_terms", []), [en, ko])
        append_unique(components[0]["match_terms"], [en, ko])
        append_unique(components[0].setdefault("evidence_terms", []), [en, ko])
        if changes: log["existing_profiles"].append({"id": pid, "file": path.name, "added_paraphrases": changes, "component_alternatives": [[en, ko]], "activation_unchanged": True, "duties_unchanged": True})
        cid = candidate_id(pid)
        if cid not in entries: raise ValueError("no candidate counterpart: " + pid)
        cp, slot, entry = entries[cid]
        changes = append_unique(entry.setdefault("paraphrases", []), [en, ko])
        append_unique(entry.setdefault("keywords", []), [en, ko])
        text = entry.get("embedding_text", entry.get("en", ""))
        entry["embedding_text"] = " | ".join([text, *[x for x in (en, ko) if x not in text]])
        if changes: log["candidate_changes"].append({"id": cid, "profile_id": pid, "file": cp.name, "slot": slot, "new": False, "added_paraphrases": changes})
    mapped = {}
    for line in NEW.strip().splitlines():
        aid, slug, bucket, slot, prop, en, ko, pen, pko = line.split("|")
        units, kunits, alternate, kalternate = [[x.strip() for x in text.split(";")] for text in (en, ko, pen, pko)]
        assert len(units) == len(kunits) == len(alternate) == len(kalternate), slug
        pid, cid = "uniform_" + slug, "unif_" + slug
        pp = ASSETS / f"photo_prompt_visual_obligations_{bucket}.json"
        cp = ASSETS / f"photo_prompt_{bucket}_extension.json"
        assert pp in docs and cp in docs, bucket
        effect = {"dimension": "appearance", "target": "main_subject", "property": prop}
        effects = [effect]
        if aid in COLOR_ATOMS and not prop.startswith("wardrobe.color"):
            effects.append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe.color"})
        if aid in {"U47"}: effects.append({"dimension": "appearance", "target": "main_subject", "property": "hair.accessories"})
        if aid in {"U31", "U60", "U72"}: effects.append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe.accessories.headwear"})
        if aid in {"U15", "U16", "U28", "U31", "U32", "U60", "U70"}:
            effects.append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe.layers"})
        full = [en, ko, pen, pko]
        entry = {"id": cid, "ko": ko, "en": en, "weight": 0.45, "tags": ["human", "observable_relation"], "for_any": ["human"], "aliases": [], "paraphrases": full, "keywords": [*units, *kunits, pen, pko], "embedding_text": " | ".join(full), "concept_units": units,
            "relations": [{"id": "declared_owner", "type": "declared_owner_scope", "subject": prop, "object": "main_subject"}, *copy.deepcopy(atoms[aid]["relations_proposal"][1:])],
            "affected_dimensions": ["appearance"], "affected_properties": effects, "core_assertion_discovery": True}
        limits = ["Only this selected visible garment relation is asserted; a profession, date, rank or named character alone does not request it.", "Preserve requester-owned face, hair, species, age, subject count, body, pose and camera properties.", "Visible coverage and material appearance do not establish protection, biological anatomy, operation, belief, motivation or historical authenticity.", "Every required component must be visible on the same declared wearer; partial evidence fails and hidden relations are unobservable."]
        profile = {"id": pid, "category": "selected_uniform_garment_relation", "activation": {"exact_terms": full[:2], "requires_adult_character": False, "semantic_discovery_requires_component_evidence": True,
            "hard_activation": {"contract_version": "photo-visual-hard-activation/v1", "required_any_groups": [{"id": "selected_relation", "any_terms": full[:2]}]}},
            "semantics": {"definition": en, "paraphrase_examples": full[2:], "visual_components": units, "contrast_examples": [atoms[aid]["confusion_boundaries_ko"][0]], "claim_limits": limits},
            "concept_candidate": {"concept_terms": [*full, *units, *kunits], "core_assertion_discovery": True, "affected_dimensions": ["appearance"], "affected_properties": effects},
            "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [], "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": []}, "reject_substitutes": [atoms[aid]["confusion_boundaries_ko"][0]]}
        for i, (unit, ku, alt, ka) in enumerate(zip(units, kunits, alternate, kalternate), 1):
            phrases = [unit, ku, alt, ka]
            profile["authored_components"]["components"].append({"id": f"component_{i}", "match_terms": phrases, "evidence_field": f"component_{i}_phrase", "evidence_terms": phrases, "min_content_words": 3,
                "instruction": "Keep this selected relation literal on the declared wearer: " + unit + ".",
                "render_gate": {"id": f"vo_{pid}_{i}", "review_scale": "native", "description": unit + ". Inspect the original image at native resolution on the same wearer; partial or wrong-owner evidence fails and hidden connections are unobservable."}})
        if pid in profiles or cid in entries: raise ValueError("ID already exists; inspect rather than replace: " + pid)
        docs[pp]["profiles"].append(profile)
        docs[cp].setdefault("slots", {}).setdefault(slot, []).append(entry)
        profiles[pid] = (pp, profile); entries[cid] = (cp, slot, entry)
        mapped[aid] = [pid]
        log["new_profiles"].append({"atom_id": aid, "id": pid, "candidate_id": cid, "profile_file": pp.name, "candidate_file": cp.name, "slot": slot, "components": len(units), "canonical_components": units, "alternative_components": alternate, "alternative_components_ko": kalternate, "source_ids": atoms[aid]["source_ids"], "source_scope": atoms[aid]["status_scope_ko"]})
        log["candidate_changes"].append({"id": cid, "profile_id": pid, "file": cp.name, "slot": slot, "new": True, "added_paraphrases": full})
    # A small set of actual same-wearer combinations; research comparison pools
    # (AGSU/ASU, skirts/trousers, early/late editions) are never all-of bundles.
    combos = [
        ("uniform_layered_contrast_robe", ["unif_contrasting_robe_sleeves", "unif_sleeveless_robe_over_inner_sleeves"], ["uniform_contrasting_robe_sleeves", "uniform_sleeveless_robe_over_inner_sleeves"]),
        ("uniform_draped_coat_inner_braid", ["unif_shoulder_draped_empty_sleeve", "ccx_cc05_02"], ["uniform_shoulder_draped_empty_sleeve", "costume_ccx_cc05_02"]),
        ("uniform_sailor_collar_edge_lines", ["ccx_cc03_01", "unif_sailor_lines_follow_collar"], ["costume_ccx_cc03_01", "uniform_sailor_lines_follow_collar"]),
        ("uniform_patchwork_robe_waist_support", ["unif_kesa_patchwork_outer_border", "unif_habit_hood_separate_waist_cord"], ["uniform_kesa_patchwork_outer_border", "uniform_habit_hood_separate_waist_cord"]),
    ]
    # Kesa and a hooded habit are separate religious systems. Keep that
    # comparison out of runtime rather than inventing a universal ensemble.
    combos = [x for x in combos if x[0] != "uniform_patchwork_robe_waist_support"]
    costume = docs[ASSETS / "photo_prompt_costume_cosplay_extension.json"]
    for bid, ids, pids in combos:
        members = [entries[cid][2] for cid in ids]
        costume["visual_semantics"].append({"id": bid, "primary_visual_proposition": "; ".join(m["en"] for m in members),
            "component_groups": [{"id": f"member_{i}", "visible_evidence": m["concept_units"]} for i, m in enumerate(members, 1)],
            "candidate_ids": ids, "candidate_slots": {cid: entries[cid][1] for cid in ids}, "hard_profile_ids": pids,
            "relations": [{"id": "same_wearer", "type": "same_owner", "subject": members[0]["en"], "object": members[1]["en"]}],
            "confusion_boundaries": ["Each component keeps its own visible carrier on one declared wearer.", "An associated profile activates only from its independent requested or selected relation."],
            "candidate_only": True, "activation_mode": "independent_component_request_evidence_only", "source_keywords": [bid.replace("_", " ")]})
    for aid, a in atoms.items():
        reuse = [x for x in a["reuse_existing_ids"] if x in profiles]
        links = mapped.get(aid, []) + reuse
        status = "new_bounded_relation" if aid in mapped else "enrich_or_reuse_existing" if reuse else "bounded_or_deferred"
        log["research_dispositions"].append({"atom_id": aid, "disposition": status, "profile_ids": links,
            "reason": "Exact terms describe the selected visible form, not a whole institutional/canonical uniform. Unsupported dates, ranks, color-role mappings and unseen construction are not promoted."})
    changed = [path for path in paths if docs[path] != originals[path]]
    for path in changed:
        doc = docs[path]
        if "slots" in doc and path.name.endswith("extension.json"):
            old = originals[path].get("maintenance_ref")
            plain = copy.deepcopy(doc); plain.pop("maintenance_ref", None)
            rid = path.stem + "-uniform-equivalents-20261004"
            record = {"schema_version": "photo-extension-maintenance/v1", "record_id": rid, "authored_source_sha256": digest(plain), "prior_maintenance_ref": old,
                "research_directory": str(RESEARCH.relative_to(ROOT)), "candidate_changes": [x for x in log["candidate_changes"] if x["file"] == path.name],
                "scope": "Equivalent descriptions preserve original effects and guards; new selected relations have explicit property scope. Research IDs and source URLs remain outside the runtime data."}
            record_path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (rid + ".json")
            record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
            doc["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": rid, "sha256": digest(record)}
        if read(path) != originals[path]: raise RuntimeError("Concurrent source change; rebase additive edits: " + str(path))
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        log["source_files"].append({"path": str(path.relative_to(ROOT)), "before_sha256": before, "after_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    log["counts"] = {"existing_profiles_enriched": len(log["existing_profiles"]), "new_profiles": len(log["new_profiles"]), "existing_candidates_enriched": sum(not c["new"] for c in log["candidate_changes"]), "new_candidates": sum(c["new"] for c in log["candidate_changes"]), "new_optional_bundles": len(combos), "existing_profile_full_paraphrases_added": sum(len(p["added_paraphrases"]) for p in log["existing_profiles"]), "new_profile_full_paraphrases": len(log["new_profiles"]) * 2, "source_files_changed": len(changed)}
    (HERE / "INTEGRATION-LEDGER.json").write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(log["counts"], ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
