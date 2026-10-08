"""Build research-only artifacts. Does not write live assets, indexes or runtime."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]

# Definitions summarize the cited material. Visible components, relations,
# confusion tests and crop requirements are this research's authoring proposals.
# Format: ID | original groups | label | source IDs | mode | proposed slot |
# priority | brief definition | owned visible components | directed relation |
# contrast / rejected inference
UNIT_ROWS = """
E001|1|흙·땅·지반의 관찰 단위|S01,S03|context|none|P0|물질·지표 공간·지지 기반은 서로 다른 관찰 단위다.|ground::a bounded exposed ground patch beside the path;soil::loose particles resting on that ground patch|soil:rests_on:ground|땅이라는 말만으로 갈색 토양·수직 절개·지하 공동을 강제하지 않는다.
E002|2,29|구분되는 모래 입자|S02,S35|direct|texture|P0|USDA에서 모래는 0.05–2 mm 입경 범위다.|sand::individual coarse grains resolved on one sand patch;sand::small shadows between adjacent grains on that patch;scale_reference::a scale reference in the same focal plane|scale_reference:scales:sand|멀리서 보이는 점무늬는 개별 입자 증거가 아니다. 모래를 석영과 동일시하지 않는다.
E003|2,5|실트·점토 입경과 토성|S02,S35|micro|none|P0|실트 0.002–0.05 mm와 점토 0.002 mm 미만은 입경 분류다.|sample::a labelled fine sediment sample under magnification;scale_bar::a calibrated scale bar beside the resolved sample;sample::a separate bulk sample outside the magnified view|scale_bar:scales:sample|일반 풍경 사진에서 점토 입자의 판상 결정이나 정확한 토성 비율을 주장하지 않는다. 양토는 1:1:1 혼합이 아니다.
E004|2,17,29|둥근 자갈·각진 쇄석·잔돌|S01,S18|direct|surface_material|P0|입경·원마도·광물 종류는 별개의 속성이다.|gravel::rounded pebbles embedded in a finer sediment bed;gravel::irregular grain sizes with visible pebble edges;matrix::fine sediment occupying gaps around the pebbles|matrix:surrounds:gravel|갈색 흙만으로 자갈 혼합을 증명하지 않는다. 각진 쇄석 변형은 별도 후보로 분리한다.
E005|2,5,29|입단과 경운 흙덩이|S01,S02|macro|texture|P0|입단은 구조 단위이며 경운으로 생긴 흙덩이와 동일하지 않다.|aggregate::small crumb aggregates on a broken soil face;aggregate::irregular natural boundaries around each crumb;soil_face::interaggregate gaps continuing into the exposed soil face|aggregate:part_of:soil_face|돌·팝콘·구슬로 대체하지 않는다. 흙덩이 모양만으로 안정성·생물 접착 원인을 확정하지 않는다.
E006|5|판상·괴상·주상 구조|S01,S02|macro|texture|P1|토양 구조는 입자가 모여 배열된 형식이다.|soil_face::thin horizontal peds stacked within a soil face;ped_boundary::separation planes bounding those same peds;scale_reference::a centimetre scale adjacent to the exposed structure|ped_boundary:bounds:soil_face|입자의 납작함과 판상 입단을 구별한다. 주상·괴상 변형은 수직/덩어리 방향을 별도로 작성한다.
E007|2,12,29|마른 흙의 분진과 발생점|S06|direct|ambient_particle|P0|바람·접촉으로 지표 입자가 공중에 이동할 수 있다.|soil_surface::a dry loose surface at the wheel contact;dust::a suspended dust plume starting at that contact;wheel::a wheel touching the same dusty ground patch|dust:originates_at:soil_surface|먼지와 안개·연기·필름 입자를 구별한다. 달에서는 대기 중 먼지 구름으로 적용하지 않는다.
E008|2,6,29|진흙과 흙탕물의 상태 차이|S01,S13|direct|surface_material|P0|진흙의 변형 가능한 바탕과 물속 부유 입자는 다른 상태다.|mud::a cohesive muddy bed holding a shallow groove;water::turbid standing water adjoining that muddy bed;contact_boundary::a visible margin between bed and standing water|water:adjoins:mud|갈색 액체만으로 진흙 바닥을 증명하지 않는다. 물의 탁함과 점도는 같은 뜻이 아니다.
E009|4,6,29|촉촉한 무광 흙과 수막 광택|S01,S03|direct|texture|P0|토색 관찰에는 수분 상태를 함께 기록한다.|soil_surface::a damp matte patch beside a wetter glossy patch;water_film::small specular reflections confined to the wetter patch;boundary::a local moisture boundary across the same soil surface|water_film:coats:soil_surface|젖은 흙 전체를 검정 플라스틱으로 바꾸지 않는다. 어두운 색만으로 수분량을 측정하지 않는다.
E010|29|발의 압력과 진흙 발자국|S01,S40|direct|aftermath_trace|P0|접촉 자국은 눌린 바탕과 그 접촉체의 관계로 작성한다.|boot::one boot partly pressing into a muddy surface;footprint::a matching tread depression beside that same boot;mud_ridge::displaced mud raised along the impression edge|boot:imprints:footprint|공중에 뜬 부츠와 떨어진 자국은 접촉 증거가 아니다. 얕은 자국으로 지반 지지력을 확정하지 않는다.
E011|29,21|차륜 홈과 융기한 흙|S01,S40|direct|aftermath_trace|P0|하중 흔적은 차륜·홈·밀려난 재료의 연결로 묘사한다.|rut::two parallel wheel ruts along one dirt track;soil_ridge::displaced soil ridges along the rut sides;tread::repeated tread marks aligned with each rut|tread:marks:rut|하천 도랑·경작 이랑과 혼동하지 않는다. 자국만으로 차량 무게·통행 횟수를 추정하지 않는다.
E012|8,12,29|다각형 건열과 마른 판|S01,S40|reuse|surface_material|P0|기존 건열 후보의 연결된 균열·마른 판·공통 표면을 재사용한다.|crack_network::connected polygonal cracks across one dry sediment surface;sediment_plate::dried sediment plates bounded by those cracks;surface::a coherent drying bed carrying the complete crack network|crack_network:bounds:sediment_plate|시멘트 줄눈·파충류 비늘·얼음 쐐기 다각형은 다른 의미다. 건열만으로 버티솔을 진단하지 않는다.
E013|5,19|공극과 뿌리 통로|S01,S17|macro|texture|P1|공극은 입자·입단 사이의 공간이며 통로와 연결될 수 있다.|soil_face::an exposed soil face with resolved channel openings;root_channel::a root-sized channel continuing into the soil face;aggregate::crumb boundaries surrounding the channel mouth|root_channel:passes_through:soil_face|모든 공극을 거대한 동굴로 바꾸지 않는다. 사진으로 공극률·투수계수를 수치화하지 않는다.
E014|5,22|가소성 점토의 눌림|S02,S21|direct|action|P0|가소성의 시각 단서는 성형 후 남는 변형을 보여주는 것이다.|hand::fingertips pressing one soft clay lump;clay::finger grooves retained on that same clay lump;clay::a folded edge adjoining the fresh grooves|hand:deforms:clay|가마 소성과 구별한다. 표면 홈만으로 광물 조성이나 손의 감각을 확정하지 않는다.
E015|5|팽윤·수축·압밀의 시간성|S01|context|none|P1|부피 변화와 배수 과정은 시점·하중·수분 조건을 필요로 한다.|sample_pair::two time-labelled views of the same soil specimen;scale_reference::the same scale visible beside both specimen views;measurement::a separate measurement annotation outside the soil material|measurement:describes:sample_pair|단일 정지 사진으로 변화량·속도·원인을 증명하지 않는다. 다짐과 압밀을 동의어로 묶지 않는다.
E016|3|토양 단면의 층위 경계|S03|direct|location|P0|토양 단면은 층위의 수직 배열이다.|soil_cut::a continuous vertical soil exposure from surface downward;horizon_boundary::irregular boundaries separating contrasting soil bands;scale_reference::a vertical depth scale against the same soil cut|horizon_boundary:divides:soil_cut|O-A-E-B-C-R을 모든 토양에 강제하지 않는다. 장식 줄무늬와 퇴적 층리를 토양층위로 확정하지 않는다.
E017|3,19,20|낙엽층과 어두운 상부 광물층|S03,S17|direct|surface_material|P0|유기성 피복과 아래의 광물성 상부층은 구별한다.|litter::recognisable leaf fragments lying at the ground surface;topsoil::a darker mineral layer directly beneath those fragments;root::fine roots crossing the litter to topsoil boundary|litter:overlies:topsoil|어두운 색만으로 유기물 함량·비옥도를 확정하지 않는다. 낙엽층을 모든 A층의 필수 조건으로 삼지 않는다.
E018|3,4|밝은 용탈층과 아래 집적층의 대비|S03,S05|named_context|location|P1|밝은 용탈층과 어두운 아래층은 특정 단면 표현의 대비 단서다.|upper_band::a pale subsurface band in one soil cut;lower_band::a darker band immediately below that pale band;boundary::the continuous boundary linking the two bands|upper_band:overlies:lower_band|밝음만으로 E층·포드졸을 진단하지 않는다. 토양학 이름을 쓸 때 조사된 단면 문맥을 별도 유지한다.
E019|3,17|풍화 모재와 연속 기반암|S03,S18|direct|location|P0|모재에 가까운 층과 단단한 기반암은 같은 흙층이 아니다.|weathered_material::loose weathered fragments above a rock contact;bedrock::continuous coherent bedrock below that contact;contact::a visible transition from loose material to solid rock|weathered_material:overlies:bedrock|기반암을 검은 흙층으로 그리지 않는다. C층 모재가 언제나 바로 아래 암석에서 유래한다고 단정하지 않는다.
E020|3,24|묻힌 옛 토양과 시간 문맥|S01,S03|named_context|location|P2|고토양은 과거 형성 후 보존된 토양이라는 해석을 포함한다.|buried_band::a soil-like band buried below younger sediment;overburden::a younger sediment package above the buried band;soil_cut::a single exposure showing their stratigraphic relation|overburden:overlies:buried_band|색 띠만으로 연대·고기후를 확정하지 않는다. 인물 초상 배경에 수직 절개를 자동 추가하지 않는다.
E021|4,23,29|황갈색·적갈색·검은 토색|S01,S03|direct|color|P0|색 이름은 토양군·광물·기원 분류와 분리해 기록한다.|soil_surface::a reddish brown soil patch under neutral illumination;reference::a neutral colour reference beside the soil patch;soil_surface::visible granular texture inside the coloured patch|reference:calibrates:soil_surface|적토를 피·화산재·오커 안료와 동일시하지 않는다. 조명색·후보정색을 흙의 물체색으로 대신하지 않는다.
E022|4|체르노젬 문맥과 두꺼운 어두운 표층|S04,S05|named_context|location|P1|체르노젬은 진단 요건을 가진 토양군이다.|soil_cut::a thick dark surface band in a documented soil cut;lower_band::a contrasting lower band beneath that surface band;grass_roots::grass roots entering the dark upper band|grass_roots:penetrate:soil_cut|검은 흙만으로 체르노젬·비옥도·초원 기원을 확정하지 않는다. 분류 검증은 사진 gate 밖에 둔다.
E023|4|포드졸의 조사 단면 문맥|S04,S05|named_context|location|P1|포드졸 분류는 표층의 검은색 하나로 결정되지 않는다.|soil_cut::a documented cut with a pale intermediate band;subsoil::a darker subsurface band below the pale band;boundary::continuous uneven contacts across the same cut|subsoil:underlies:soil_cut|일반 숲바닥을 밝은 E층과 B층의 필수 조합으로 강제하지 않는다. E018과 중복 반영을 피한다.
E024|4,17|화산성 흙·신선한 재·마사 재료|S04,S05,S18|named_context|surface_material|P1|토양의 화산성 기원과 신선한 화산재·화강암 풍화재는 별개다.|volcanic_sample::a documented loose volcanic soil specimen;fragment::porous rock fragments adjoining that specimen;sample_boundary::a clear boundary between soil and separate ash sample|fragment:adjoins:volcanic_sample|안도솔=검은 흙으로 등록하지 않는다. 마사토와 신선한 화산재는 독립 후보가 필요하다.
E025|4,18,20|이탄의 식물 섬유와 유기층|S04,S05,S17|macro|surface_material|P1|이탄과 유기성 토양군 이름은 재료와 분류의 차이를 유지한다.|peat::recognisable plant fibres within a dark organic slab;peat::compressed layered fibres exposed along the slab edge;cut_edge::a wet cut edge belonging to that same slab|cut_edge:exposes:peat|검은 진흙·석탄·부엽토와 자동 병합하지 않는다. 히스토솔 진단·탄소량은 별도 자료가 필요하다.
E026|4,5|버티솔의 수축 흔적과 쐐기 입단|S04,S05|named_context|texture|P1|버티솔은 수축성 점토와 진단 구조를 포함하는 분류다.|soil_face::wedge-shaped peds within a documented clay soil face;ped_face::smooth grooved faces on those same peds;crack::a deep crack extending from the upper surface|ped_face:part_of:soil_face|건열 하나만으로 버티솔을 확정하지 않는다. 매끈한 면을 젖은 피부 광택으로 치환하지 않는다.
E027|4,6|회색 바탕과 산화환원 반점|S04,S05|named_context|texture|P1|글레이성 표현의 회색 바탕과 반점은 수분 문맥과 함께 해석한다.|soil_face::a grey matrix on one exposed soil face;mottle::rust-coloured mottles embedded within that grey matrix;root_channel::a root channel crossing the mottled soil face|mottle:embedded_in:soil_face|회색 흙=글레이솔·오염·특정 수위로 등록하지 않는다. 반점을 단순 색보정으로 대신하지 않는다.
E028|4,8,12,29|소금 피막과 토양 바탕|S04,S05,S10|macro|surface_material|P1|표면 염류 석출과 솔론차크 분류는 다른 증거 수준이다.|salt_crust::a white crystalline crust attached to a soil patch;soil_surface::brown substrate exposed through broken crust edges;salt_crust::raised crystal grains resolved at the crust margin|salt_crust:adheres_to:soil_surface|눈·흰 페인트·석고·균사를 배제한다. 하얀 피막만으로 염류 종류·농도·식물 피해를 진단하지 않는다.
E029|4,7,10|최근 충적 재료의 층과 입경 변화|S04,S05,S07|named_context|location|P1|플루비솔은 충적성 물질과 진단 조건으로 분류한다.|soil_cut::thin sediment bands in a documented riverbank cut;gravel_band::a coarse band interleaved with finer bands;river::the adjacent river in the same wider view|gravel_band:interleaves:soil_cut|층리만으로 플루비솔·홍수 연대·층위 기호를 확정하지 않는다.
E030|4,2|아레노솔과 사질 바탕|S04,S05|named_context|surface_material|P1|아레노솔은 모래성 단면의 분류이며 모래 색 이름이 아니다.|soil_cut::a deep documented cut dominated by loose sandy material;grain_patch::resolved sand grains at the cut margin;root::sparse roots entering the same sandy cut|grain_patch:part_of:soil_cut|모래사장만으로 아레노솔 분류를 확정하지 않는다. E002와 신규 중복을 검토한다.
E031|4,5|탄산염 집적의 결절·백색 띠|S04,S05|named_context|texture|P1|칼시솔은 탄산염 집적 진단을 가진 토양군이다.|soil_face::pale nodules embedded in a documented soil face;nodule::white material exposed at a broken nodule edge;matrix::contrasting finer soil matrix around the nodules|nodule:embedded_in:matrix|돌·염류·석고를 색만으로 구별하지 않는다. 산 반응·화학 조성은 사진 gate로 삼지 않는다.
E032|5,8,20|pH·CEC·밀도·비옥도의 비가시성|S01,S03,S04|context|none|P0|측정 성질과 외형은 동일한 데이터가 아니다.|soil_sample::a soil specimen beside a separate test report;report::reported values printed outside the specimen image;sample_label::a specimen identifier matching the separate report|report:describes:soil_sample|어두움=비옥함, 푸석함=높은 CEC, 황색=산성을 금지한다. 수치와 화학 안전성은 외형으로 생성하지 않는다.
E033|6,5|표면 침투의 관찰 문맥|S01,S13|context|none|P1|침투는 물이 지표에서 토양으로 들어가는 과정이다.|wetting_front::a visibly darkened wetting patch beneath added water;soil_surface::a surrounding drier patch on the same soil surface;time_pair::two ordered views retaining the same framing|wetting_front:within:soil_surface|단일 젖은 표면으로 침투율·함양량을 증명하지 않는다. 검은 화살표를 자연 사진 표면에 삽입하지 않는다.
E034|6|대수층·지하수면의 단면 표현|S13,S14|diagram|none|P1|지하수는 포화된 공극·틈에 존재하며 대수층은 공급 능력도 포함한다.|porous_layer::a diagram showing water in connected pore spaces;confining_layer::a lower permeability layer drawn above a confined unit;water_table::a labelled saturation boundary inside the diagram|confining_layer:overlies:porous_layer|지하수를 자동으로 거대 지하 호수로 바꾸지 않는다. 투시 단면·화살표는 도식 요청에서만 채택한다.
E035|6,13|샘과 연결된 출수 물길|S13,S08,S40|reuse|location|P1|기존 샘 출수점 후보를 재사용하고 토양·암반 출구를 구별한다.|spring_outlet::water emerging from a bounded natural ground opening;channel::a shallow channel connected to that same outlet;substrate::damp substrate immediately adjoining the outlet|spring_outlet:feeds:channel|배관·배수구를 자연 샘으로 바꾸지 않는다. 피압 여부·음용 가능성을 사진으로 확정하지 않는다.
E036|7,8|세류침식의 작은 분기 홈|S11|direct|location|P0|집중 유출은 작은 침식 물길을 만들 수 있다.|slope::several narrow shallow channels on one exposed slope;rill::branching channels following the downhill direction;deposit::small sediment deposits below the channel mouths|rill:cuts:slope|경운 이랑·타이어 홈과 구별한다. 공통 척도 없이 크기를 임의 규정하지 않는다.
E037|7,8|구곡침식의 깊은 도랑과 두부|S11,S12|direct|location|P1|구곡은 깊고 뚜렷한 침식 통로로 기술한다.|gully::a deeply incised channel with steep soil sides;head_scarp::an abrupt headcut at the upper channel end;scale_reference::a scale object beside the same channel wall|head_scarp:terminates:gully|작은 균열을 구곡으로 키우지 않는다. 자연 계곡·굴착 배수로와 구별한다.
E038|7,8,29|하안 침식과 노출 뿌리|S07,S11|direct|location|P0|침식면은 잘린 바탕·노출된 뿌리·물길의 관계로 표현한다.|bank::an undercut soil bank beside the active channel;root::roots extending from that same exposed bank;fallen_clod::loose clods resting beneath the undercut edge|root:protrudes_from:bank|나무뿌리를 공중의 장식 끈으로 그리지 않는다. 정지 사진으로 침식 속도를 확정하지 않는다.
E039|7,8|면상 유실과 빗방울 비산의 한계|S11,S26|context|none|P1|면상 유실은 얇은 표층 제거이며 빗방울 충격과 구별한다.|pedestal::small soil pedestals protected beneath stones;stone::stones resting atop those soil pedestals;soil_surface::lower exposed material surrounding the protected patches|stone:covers:pedestal|전체 표토 손실 두께는 비교 조사 없이 주장하지 않는다. 빗방울 splash와 공중 먼지는 다른 후보다.
E040|8|토석류의 큰 돌과 세립 기질|S15,S16|direct|aftermath_trace|P1|토석류는 물·퇴적물·암석이 섞이는 흐름 문맥이다.|debris_lobe::a lobate mixed debris deposit at a channel mouth;boulder::large clasts protruding from its finer muddy matrix;levee::lateral ridges bounding the same deposit|boulder:embedded_in:debris_lobe|균일한 갈색 물과 구별한다. 퇴적 외형만으로 발생 시점·유속·피해 인원을 추론하지 않는다.
E041|8|산사태의 상부 절벽과 하부 퇴적|S15,S16|direct|location|P1|중력 사면 이동은 발생부·이동부·퇴적부로 나눠 기술한다.|head_scarp::an exposed arcuate scarp high on one slope;displaced_mass::displaced earth extending below that same scarp;toe::a bulging debris toe at the lower end|displaced_mass:below:head_scarp|수직 절벽 하나를 산사태 증거로 삼지 않는다. 회전형·병진형 변형은 별도 작성한다.
E042|8,9|낙석과 사면 아래 각진 암편|S16,S18|direct|location|P1|낙석 흔적은 공급 절벽과 사면 아래 암편을 연결해 보여준다.|cliff::a fractured rock face above a steep slope;talus::angular fragments accumulated below that same face;fragment::one large block resting among the smaller fragments|talus:below:cliff|하천의 둥근 자갈층과 구별한다. 정지 블록으로 떨어지는 순간을 증명하지 않는다.
E043|8,13|돌리네·함몰의 표면 형태|S08|named_context|location|P1|카르스트 함몰은 용해·붕괴 문맥과 함께 해석한다.|depression::a closed ground depression with continuous surrounding rim;rim::exposed soil and rock along part of that rim;floor::a lower floor inside the same depression|rim:bounds:depression|모든 도로 함몰을 카르스트 싱크홀로 단정하지 않는다. 숨은 공동을 실제 사진에 자동 투시하지 않는다.
E044|8|액상화 문맥의 분사공과 침하|S16|named_context|aftermath_trace|P1|포화 지반 강도 손실에는 지진·지반 조사 문맥이 필요하다.|sand_vent::a sand vent surrounded by fresh sandy ejecta;ground_crack::a nearby crack within the same affected ground patch;settled_object::a tilted object adjoining the disturbed patch|sand_vent:emits:sandy_ejecta|모래 분사공 하나로 액상화를 확진하지 않는다. 지열 샘·배관 누출과 대조한다.
E045|8,21|다짐과 토양 밀봉의 차이|S01,S10|direct|surface_material|P1|밀봉은 표면 피복이며 다짐은 토양의 치밀화 과정이다.|pavement::an impervious pavement edge covering ground;soil_cut::exposed soil continuing beneath the pavement edge;boundary::a visible cover boundary at the pavement margin|pavement:covers:soil_cut|포장색을 토양 상태로 오인하지 않는다. 겉으로 단단함만으로 용적밀도를 정하지 않는다.
E046|8,12,30|황폐지·사막화의 시간·지역 문맥|S10,S06|context|none|P2|사막화는 시간과 환경 문맥을 포함하는 토지 변화 개념이다.|land_pair::two dated views of the same documented land patch;vegetation::reduced ground cover in the later view;soil_surface::more exposed soil within the matched later framing|vegetation:covers:soil_surface|모래언덕·황색·건열 하나를 사막화 진단으로 등록하지 않는다.
E047|9,12|고원·메사·뷰트의 윤곽|S36|direct|location|P1|평탄한 상부와 사면 형태는 상대 크기·주변 지형과 함께 기술한다.|mesa::a broad flat summit bounded by steep sides;butte::a smaller isolated flat-topped remnant nearby;plain::a lower surrounding plain connecting both landforms|mesa:above:plain|지평선만으로 높은 고원을 증명하지 않는다. 메사와 뷰트의 절대 크기 임계값을 만들지 않는다.
E048|9,10|능선·안부·분지·계곡의 상대 위치|S01,S07|direct|location|P1|지형 이름은 주변의 높낮이와 연결 관계를 필요로 한다.|ridge::two high ridge segments flanking a lower saddle;saddle::a pass joining the two ridge segments;valley::a valley floor lying below that same saddle|saddle:connects:ridge|높은 점 하나는 능선이 아니다. 능선과 분수계는 문맥 없이 동일시하지 않는다.
E049|7,17|암석 풍화의 제자리 흔적|S18|direct|texture|P1|풍화는 제자리에서 물질이 변하는 작용이다.|rock_face::a weathered outer rind on a fractured rock face;fresh_face::a fresher contrasting interior at the same break;loose_grains::loose grains immediately beneath that broken surface|rock_face:surrounds:fresh_face|운반·퇴적과 원인 표기를 분리한다. 붉음만으로 철 산화 조성을 확정하지 않는다.
E050|10,7|선상지와 삼각주의 출구 차이|S07,S36|direct|location|P1|산지 출구의 선상 퇴적과 수역 진입의 삼각주는 위치 관계가 다르다.|fan::a fan-shaped deposit spreading from a narrow mountain outlet;outlet::a confined channel opening onto the fan apex;plain::an open plain receiving the widening deposit|outlet:feeds:fan|삼각주는 바다·호수 진입을 별도 후보로 작성한다. 모든 삼각주를 삼각형으로 강제하지 않는다.
E051|10,6|자연제방과 낮은 배후습지|S07|direct|location|P1|하천 가까운 미고지와 뒤쪽 낮은 습지는 상대 위치가 핵심이다.|river::a channel flanked by low sediment ridges;levee::a continuous low ridge adjoining that channel;backswamp::lower wet ground behind the same ridge|levee:separates:backswamp|인공 제방과 혼동하지 않는다. 단일 사진으로 범람 주기를 확정하지 않는다.
E052|10|곡류·우각호·침식안·퇴적안|S07,S40|reuse|location|P1|기존 하천 의미에서 연결과 단절을 재사용한다.|oxbow::a curved water body disconnected from the main channel;land_neck::land separating the curved water body from the river;river::the nearby main river visible in the same aerial view|land_neck:separates:oxbow|넓은 굽이를 곧바로 우각호로 부르지 않는다. 하중도·안쪽 퇴적안은 독립 세부 후보로 검토한다.
E053|10|망상하천의 분기와 재결합|S07,S40|reuse|location|P1|여러 물길이 퇴적체 사이에서 갈라졌다 다시 만난다.|channels::multiple shallow channels splitting around sediment bars;bars::exposed gravel bars bounded by those channels;reconnection::downstream reconnections between previously separated channels|channels:surround:bars|지류 합류 한 번과 구별한다. 기존 water_w070 계열을 우선 재사용한다.
E054|10,9|하안단구의 상·하 평탄면|S07|direct|location|P1|단구는 현재 물길보다 높게 남은 과거 하천면의 문맥이다.|terrace::a flat bench above the current river;scarp::a step-like slope separating bench from lower floodplain;river::the current river lying below that same bench|terrace:above:river|계단식 농경지와 구별한다. 높이만으로 형성 연대나 융기량을 확정하지 않는다.
E055|11,16|반도·지협·섬의 연결 그래프|S09,S37|direct|location|P1|물과 육지의 연결·둘러싸임은 이름의 주요 공간 단서다.|isthmus::a narrow land neck connecting two larger land areas;water::water bordering both sides of that neck;landmasses::two continuous land areas joined through the neck|isthmus:connects:landmasses|사람 높이 사진의 좁은 길만으로 지협을 주장하지 않는다. 군도와 군용 칼의 동음 의미를 분리한다.
E056|11|사취·육계사주·석호의 결합|S09,S38,S40|reuse|location|P1|퇴적 띠의 양끝 연결과 뒤쪽 수역을 구별한다.|tombolo::a sediment ridge joining mainland to an offshore island;island::an island attached at the ridge outer end;water::water flanking both sides of the connecting ridge|tombolo:connects:island|한쪽만 붙은 사취와 구별한다. 기존 water_w077 계열의 관계를 우선 재사용한다.
E057|11,2|모래 해변·자갈 해변·펄의 바탕|S09,S06|direct|surface_material|P1|해변 재료와 조간대 위치는 별도 속성이다.|tidal_flat::a fine wet sediment flat beside a shallow tidal channel;channel::branching drainage grooves across that flat;waterline::a receding waterline adjoining the same flat|channel:cuts:tidal_flat|모든 갯벌이 순수 점토라는 정의를 피한다. 펄의 질척함만으로 염도·조석 시각을 정하지 않는다.
E058|11,13|해식애와 바다의 고립 바위기둥|S09|direct|location|P1|해안 침식 지형의 바위와 해수 경계를 연결해 보여준다.|sea_stack::an isolated rock pillar surrounded by seawater;cliff::a nearby coastal cliff above the same waterline;water::seawater continuously separating pillar from the cliff|water:separates:sea_stack|단순 육상 뷰트와 구별한다. 고립 외형만으로 침식 연대를 확정하지 않는다.
E059|12,11|사구의 사면과 바르한 방향|S06|direct|location|P1|사구는 바람에 쌓인 모래 언덕이며 해안에도 존재한다.|dune::a crescent-shaped sandy ridge with two extending horns;slip_face::a steeper face on one side of that ridge;stoss_slope::a gentler opposing slope on the same dune|slip_face:part_of:dune|바람 방향은 물체 움직임·문맥으로 검증한다. 모든 사막·해변에 바르한을 추가하지 않는다.
E060|12,2|모래 표면 사련의 배율|S06,S01|direct|texture|P1|작은 퇴적물 물결무늬와 물의 표면 파도는 다르다.|sand_patch::repeated low ripple ridges on one sand patch;trough::dry sandy troughs between those ridges;scale_reference::a small scale reference beside the ripple pattern|trough:separates:sand_patch|수면 물결·거대한 사구와 구별한다. 사련만으로 바람/물 원인을 확정하지 않는다.
E061|4,12,7|뢰스의 퇴적 기원과 절개 표현|S06|named_context|location|P1|뢰스는 바람에 운반된 실트 중심 퇴적물이다.|loess_cut::a documented fine sediment cliff with vertical joints;fine_matrix::fine material exposed across that same cut;land_context::the surrounding landscape visible beyond the cut|fine_matrix:part_of:loess_cut|황토색·황토 재료를 뢰스의 동의어로 강제하지 않는다. 기원은 조사 문맥으로 유지한다.
E062|12|야르당 능선과 풍식석의 표면|S06|direct|location|P2|풍식의 능선형 지형과 암석 표면 마모는 규모가 다르다.|yardang::elongated parallel ridges in a sparsely vegetated terrain;corridor::eroded troughs running between those ridges;terrain::a common ground plane carrying the ridge field|corridor:separates:yardang|풍식석은 개별 암석의 면·홈으로 별도 작성한다. 사구의 퇴적 사면과 구별한다.
E063|12|자갈 포장 사막과 모래바다|S06,S36|direct|surface_material|P2|사막의 표면은 모래·암석·자갈·염류 등 다양하다.|pavement::a closely packed gravel surface extending across dry terrain;fine_matrix::fine material visible between the gravel clasts;boundary::a nearby loose sand patch separated from the gravel cover|pavement:covers:fine_matrix|사막포도를 포도 열매로 오해하지 않는다. 어스 톤만으로 건조 기후를 진단하지 않는다.
E064|13,7|용식·용암·해식동굴의 문맥|S08,S39|named_context|location|P1|동굴의 빈 공간과 형성 원인은 별개 자료다.|cave::a bounded cave entrance continuing into a dark passage;rock_wall::coherent bedrock framing the passage entrance;ground::an entrance floor continuous with the exterior ground|rock_wall:bounds:cave|어둠만으로 지하·카르스트를 주장하지 않는다. 원인별 동굴은 조사 문맥과 재료를 별도 작성한다.
E065|13|종유석·석순·석주의 부착 방향|S39|direct|location|P1|천장·바닥 부착과 두 구조의 연결을 구별한다.|stalactite::a tapered formation attached to the cave ceiling;stalagmite::an upward formation attached to the floor below;column::a separate continuous column joining floor and ceiling|stalactite:attached_to:cave_ceiling|바닥 위의 뾰족한 돌을 종유석으로 부르지 않는다. 물고드름은 다른 재료다.
E066|14,9|빙하 계곡·권곡·아레트의 지형|S19|named_context|location|P2|빙하 침식 지형은 주변 사면과 계곡 단면으로 표현한다.|valley::a broad U-shaped valley with steep sidewalls;floor::a relatively broad valley floor between the sidewalls;cirque::a bowl-like headwall basin at the upper valley end|floor:between:valley_walls|모든 계곡을 U자곡으로 만들지 않는다. 빙하가 현재 화면 안에 있어야만 옛 빙하 지형인 것은 아니다.
E067|14,2|틸·모레인·표석·에스커의 규모|S19|named_context|location|P2|퇴적 재료와 퇴적 지형의 이름을 분리한다.|moraine::a debris ridge along a documented glacier margin;clasts::mixed-size rock fragments visible on that ridge;glacier::the adjoining glacier edge in the same landscape view|moraine:adjoins:glacier|틸을 모두 둥근 하천 자갈로 그리지 않는다. 드럼린·에스커는 형태별 별도 세부 후보로 작성한다.
E068|14,5|영구동토·활동층과 얼음 쐐기|S20,S40|named_context|location|P2|영구동토는 최소 2년의 동결 지속이라는 시간 정의다.|ground_cut::a documented frozen-ground cut with an exposed ice wedge;ice_wedge::a wedge of ice extending downward into that cut;surface_polygon::polygon boundaries at the surface above the wedge|ice_wedge:within:ground_cut|눈 덮인 땅을 영구동토로 확정하지 않는다. 마른 진흙 건열과 얼음 쐐기를 별도 의미로 둔다.
E069|14,8|열카르스트의 꺼진 지표와 수면|S20|named_context|location|P2|열카르스트는 지중 얼음 해빙과 연결된 지표 변화 문맥이다.|depression::a subsided ground patch adjoining a thaw pond;pond::standing water within the lower depression;bank::an uneven retreating bank beside the same pond|pond:occupies:depression|모든 웅덩이를 열카르스트로 부르지 않는다. 사진으로 동토 온도·해빙 기간을 확정하지 않는다.
E070|15,7|단층 어긋남과 습곡의 연속 층|S18,S37|direct|location|P2|끊겨 어긋난 층과 이어져 굽은 층은 다른 형상이다.|strata::continuous layered bands bent through one rock exposure;fold_hinge::a curved hinge shared by several adjacent bands;rock_face::a coherent rock face containing the whole fold|fold_hinge:bends:strata|토양 줄무늬·회화 무늬와 구별한다. 단층 변형은 잘린 같은 층의 양쪽 어긋남을 별도 작성한다.
E071|15,16,1|대륙·지각·판·대륙붕의 표현|S37,S13|diagram|none|P2|지리 단위와 지질 구조·수심 단위는 서로 다른 관찰 범위다.|map::a labelled map with a declared projection and date;continental_shelf::a bathymetric shelf band beyond a coastline;tectonic_boundary::a separately styled plate boundary on the same map|continental_shelf:extends_beyond:coastline|대륙 이름만으로 특정 지형·인종·의상을 강제하지 않는다. 판 경계와 해안선을 동일 선으로 그리지 않는다.
E072|17,2|암석·광물·입경의 독립 축|S18|macro|texture|P1|암석 종류·광물 종류·입자 크기는 함께 적용될 수 있는 다른 분류다.|rock::interlocking light and dark crystals on a rock specimen;fracture::a fresh broken face exposing those same crystals;scale_reference::a scale reference beside the specimen edge|fracture:exposes:rock|모래=석영, 흰색=대리암, 검은색=현무암으로 확정하지 않는다. 화성·퇴적·변성의 각각은 따로 조사한다.
E073|18,17|광맥·광상·사금의 주장 한계|S18|named_context|texture|P2|광물의 집중과 경제적 광석 평가는 동일하지 않다.|vein::a contrasting mineral band crossing a rock specimen;host_rock::host rock visible on both sides of that band;contact::two clear contacts bounding the mineral band|vein:cuts:host_rock|반짝임만으로 금·광석 품위를 확정하지 않는다. 사금은 퇴적물 속 입자 관계를 별도 작성한다.
E074|18,17|석탄·원유·가스·지열의 별도 기원|S18,S13|context|none|P2|지하 자원을 오래된 흙의 단순 변형으로 설명하지 않는다.|specimen::a separately labelled resource specimen;host_context::a documented geological context outside the specimen;record::a resource identification record beside that context|record:describes:specimen|검은 흙을 석탄·원유로 바꾸지 않는다. 지열은 흙의 외형 재료 후보가 아니다.
E075|19|토양 미생물과 생물 피각|S17,S40|micro|none|P1|미생물의 실체와 지표 생물 피각의 거시 외형은 구별한다.|micrograph::a calibrated micrograph of one soil sample;scale_bar::a micrometre scale inside that micrograph;soil_sample::the bulk sample separately identified beside the micrograph|micrograph:depicts:soil_sample|풍경에 거대 세균·선충을 자동 추가하지 않는다. 생물 피각은 기존 후보를 보강하는 별도 거시 변형이다.
E076|19,20|균사·균근·근권·뿌리털|S17,S22|micro|none|P1|실 모양 구조와 공생 관계·활동 영역은 다른 의미다.|root::an identified root segment in a magnified sample;hyphae::fine fungal filaments adjoining the same root;scale_bar::a calibrated scale beside the root and filaments|hyphae:adjoin:root|흰 실만으로 균근·질소고정·건강한 공생을 확정하지 않는다. 뿌리털과 균사는 별도로 식별한다.
E077|19,20|지렁이·굴 입구·분변토|S17|macro|subject|P1|생물과 그 흔적은 서로의 위치 관계를 함께 작성한다.|earthworm::a segmented earthworm on a moist soil patch;burrow::a small burrow opening beside that same animal;cast::small coiled soil casts adjoining the opening|cast:adjoins:burrow|일반 흙덩이를 자동 분변토로 분류하지 않는다. 몸 마디가 없는 끈으로 지렁이를 대체하지 않는다.
E078|19|개미·흰개미와 흙 구조물|S17|macro|subject|P2|굴과 구조물의 종·행동 해석에는 생물 식별 문맥이 필요하다.|ant::a resolved ant beside a soil nest opening;nest_opening::a bounded opening with loose grains around its rim;soil_grains::grains carried or displaced near that same opening|ant:adjoins:nest_opening|모든 흙무더기를 흰개미집으로 부르지 않는다. 흰개미 변형은 몸 구조와 출처를 별도로 조사한다.
E079|19|톡토기·응애·노래기·지네의 배율|S17|micro|none|P2|분류군별 외형과 먹이망 역할을 하나의 벌레로 통합하지 않는다.|arthropod::a resolved small arthropod on leaf litter;legs::visible appendages attached to that same body;scale_bar::a calibrated scale beside the organism|legs:attached_to:arthropod|서로 다른 다리 수·몸 구획을 공통 레시피로 만들지 않는다. 대형화는 요청된 초현실 변형에만 둔다.
E080|19,20,29|낙엽 분해와 숲바닥 피복|S17,S22|direct|surface_material|P0|낙엽 형태의 잔존과 무너진 유기물 바탕을 함께 관찰한다.|litter::partly decomposed leaves still retaining some veins;organic_layer::dark broken organic fragments beneath those leaves;ground::a common forest-floor patch supporting both layers|litter:overlies:organic_layer|검은색만으로 분해 단계·부식 화학을 확정하지 않는다. 이끼 피복은 별도 재료/생물 변형이다.
E081|20,29,3|잘린 흙벽의 뿌리 연결|S03,S17|direct|location|P0|노출 뿌리는 식물·흙벽·절단면의 연결로 표현한다.|root::branching roots protruding from one cut soil wall;soil_wall::fine material continuing around the exposed roots;plant::a plant above connected to the larger root branches|root:connects:plant|갈라진 흙에 장식 끈을 얹는 것으로 대체하지 않는다. 뿌리털은 이 배율의 필수 요소가 아니다.
E082|20,21|경운의 이랑·도구·뒤집힌 흙|S22|direct|action|P1|경운 흔적은 도구 방향과 뒤집힌 표토의 관계로 기술한다.|tool::a soil-turning tool engaging one field strip;furrow::a fresh furrow continuing behind the tool;turned_soil::turned clods deposited beside that same furrow|tool:forms:furrow|도로 차륜 홈·침식 수로와 구별한다. 경운을 건강한 토양의 자동 증거로 쓰지 않는다.
E083|20|무경운·피복작물·멀칭·윤작|S22|named_context|surface_material|P1|현재 피복의 외형과 여러 해의 관리 이력은 다르다.|residue::crop residues covering soil between living rows;seedling::seedlings emerging through that same residue layer;soil_patch::small uncovered soil patches between the residues|residue:covers:soil_patch|단일 사진으로 무경운·윤작 이력을 확정하지 않는다. 플라스틱 멀칭은 유기 피복과 별도 재료다.
E084|20,9|등고선 경작과 계단식 경작지|S22,S01|direct|location|P1|경사면에서 선의 방향과 단의 연속성을 관찰한다.|terraces::cultivated benches stepping down one hillside;riser::steep risers separating adjacent cultivated benches;crop_rows::crop rows following each bench rather than descending slope|riser:separates:terraces|하안단구·임의 곡선 무늬와 구별한다. 등고선 경작은 계단 구조 없이도 별도로 표현한다.
E085|20,18|퇴비·부엽토·배양토·바이오차|S17,S22|named_context|surface_material|P2|배지와 토양 개량재의 재료·제조·용도는 별개다.|potting_mix::a documented growing mix with fibrous pieces and coarse inclusions;container::a plant container holding that same mix;plant::roots entering the mix inside the container|container:contains:potting_mix|모든 배양토에 광물성 흙을 강제하지 않는다. 검은 입자만으로 바이오차·비료 효능을 단정하지 않는다.
E086|21|어도비 흙벽돌과 줄눈|S23|direct|surface_material|P1|전통 어도비는 가마에 굽지 않고 말린 흙벽돌이다.|adobe_blocks::unfired earthen blocks laid in staggered courses;mortar::earthen joints visibly separating those blocks;broken_edge::a broken block edge showing granular fibrous material|mortar:between:adobe_blocks|갈색 소성벽돌·판축과 구별한다. 완성 미장면에서 숨은 벽돌 줄눈을 반드시 노출시키지 않는다.
E087|21|콥의 덩어리 흙벽과 섬유|S24,S25|named_context|surface_material|P2|콥은 덩어리 흙 배합물을 쌓는 건축 문맥이다.|cob_wall::a continuous earthen wall with rounded irregular edges;fibre::fibres visible at a local damaged wall edge;wall_body::continuous material without modular brick joints|fibre:embedded_in:cob_wall|갈색 벽 전체로 콥을 확정하지 않는다. 지방·시대별 마감 차이를 보존한다.
E088|21|판축의 다짐층과 거푸집 흔적|S24,S25|direct|surface_material|P1|판축은 거푸집 안의 층별 다짐 방식이다.|rammed_wall::horizontal compacted lifts on one continuous earthen wall;formwork_mark::regular formwork impressions crossing those lifts;wall_edge::a wall edge showing continuous compacted material|formwork_mark:marks:rammed_wall|수평 띠만으로 판축을 확정하지 않는다. 퇴적 지층·콘크리트 판넬과 대조한다.
E089|21|와틀 앤드 도브의 골격과 흙|S24,S25|direct|surface_material|P1|엮은 골격과 흙 배합물의 피복 관계가 핵심이다.|wattle::woven rods exposed at a broken wall panel;daub::earthen daub adhering around the same woven rods;frame::a timber frame bounding the infilled panel|daub:coats:wattle|나무 위 갈색 페인트로 치환하지 않는다. 멀쩡한 완성 벽에 손상부를 강제로 추가하지 않는다.
E090|21,20|잔디집·흙지붕의 층과 지지부|S24,S25|named_context|location|P2|식물 뿌리와 흙층·지지 구조의 결합을 표현한다.|sod::root-bound turf blocks at a documented wall edge;root_mat::dense roots holding the turf block together;support::a supporting structure beneath an earthen roof layer|root_mat:binds:sod|초록 지붕만으로 잔디집 구조를 확정하지 않는다. 실제 하중·방수 성능은 사진으로 평가하지 않는다.
E091|21,8|절토·성토·굴착·되메우기의 상태|S01,S40|direct|location|P1|파낸 면·쌓은 바탕·채운 공간을 서로 다른 상태로 둔다.|excavation::an open trench with exposed soil sides;spoil::a separate spoil pile beside that same trench;cut_face::a continuous cut face ending at the trench floor|spoil:beside:excavation|굴착=산사태·참호로 자동 치환하지 않는다. 되메우기는 채워진 공간의 별도 변형이다.
E092|21,25,10|토루·제방·흙댐·토성·해자|S07,S23,S40|named_context|location|P2|흙 구조물의 재료 형태와 방어·차수 기능은 분리한다.|earth_rampart::a long earthen embankment with a continuous crest;ditch::a parallel ditch on one side of the embankment;ground::the same ground plane joining embankment and ditch|ditch:adjoins:earth_rampart|토성의 토양 입경 의미와 구별한다. 마른 해자에 물을 자동 추가하지 않는다. 군사 구조의 시공법을 제공하는 데이터가 아니다.
E093|22,5|물레의 젖은 태토와 슬립|S21|direct|action|P1|슬립은 물속에 분산된 점토 배합물이다.|hands::two hands shaping one vessel on a pottery wheel;vessel::a wet clay vessel centred on that same wheel;slip::thin clay slurry deposited on fingers and wheel rim|hands:shape:vessel|물레 회전 자국과 몸 위 진흙을 혼동하지 않는다. 슬립은 액체 상태이고 소성 후 유약과 다르다.
E094|22|코일링·판 성형의 접합|S21,S40|direct|action|P2|띠를 쌓는 방식과 판을 붙이는 방식은 접합 방향이 다르다.|coil::a clay coil being joined to an existing vessel rim;vessel::previous coils forming the lower vessel wall;finger::a fingertip smoothing the junction on that same vessel|coil:joins:vessel|물레의 회전 줄무늬만으로 코일링을 확정하지 않는다. 판 성형은 판 모서리 접합을 별도 작성한다.
E095|22,5,21|가마 소성과 가소성의 동음 경계|S21,S23|context|none|P0|소성 firing은 열처리이며 plasticity는 변형 성질이다.|kiln::a documented kiln chamber containing ceramic pieces;shelf::shelves supporting those pieces inside the chamber;ceramic_piece::a separate ceramic object after the documented firing|shelf:supports:ceramic_piece|붉은 조명만으로 소성 온도·완료 상태를 주장하지 않는다. 단어 소성 하나로 가마 장면을 강제하지 않는다.
E096|22,21|테라코타·유약·석기·자기|S21|named_context|texture|P1|몸체와 소성 상태·유리질 표면은 독립 재료 속성이다.|ceramic_body::an exposed matte terracotta body at an unglazed foot;glaze::a glossy glaze terminating above that foot;boundary::a visible edge separating glaze from the clay body|glaze:coats:ceramic_body|유광만으로 자기를 확정하지 않는다. 자기의 인칭·자기장 의미와 구별하고 석기는 석제 도구 의미와 분리한다.
E097|23,4|오커·시에나·엄버의 재료와 색|S27,S28|named_context|prop|P1|흙 안료의 원료 이름과 색상군 이름은 분리한다.|pigment::a mound of documented brown earth pigment powder;swatch::a bound paint swatch beside the loose powder;binder::a separate binder container adjoining the powder|pigment:beside:swatch|흙색 옷·주황 조명은 안료 실물의 증거가 아니다. 광물 조성·가열 이력은 색만으로 확정하지 않는다.
E098|22,30|대지미술의 장소와 개입|S29|named_context|location|P2|대지미술은 장소·재료·예술가의 개입 문맥을 포함한다.|earthwork::a deliberate arrangement of earth and stones across a site;site::the surrounding landscape continuous with that arrangement;viewer_scale::a scale reference establishing the arrangement's site extent|earthwork:part_of:site|대지미술을 고정 나선 모양으로 정의하지 않는다. 우연한 흙무더기를 작품으로 확정하지 않는다.
E099|24,3|발굴 단면·유물의 제자리 관계|S30,S40|direct|location|P1|발굴은 층위와 물체 위치를 기록하는 조사 문맥이다.|baulk::a stratified excavation face beside a bounded grid;artifact::a pottery fragment partly embedded at one layer contact;scale_reference::a scale beside that same fragment and contact|artifact:embedded_in:baulk|주워 놓은 소품으로 제자리 유물 증거를 대신하지 않는다. 아래=항상 더 오래됨은 교란 문맥을 검토한다.
E100|24,25|봉분·토광·석실·부장품의 구별|S30|named_context|location|P2|무덤의 덮개·매장 공간·재료·부장 배치는 별도 단위다.|burial_mound::a rounded earthen mound in a documented cemetery;chamber::a separately documented stone chamber exposure;grave_goods::objects recorded within that chamber context|grave_goods:within:chamber|단일 사진에 닫힌 봉분과 내부 석실을 동시에 투시하지 않는다. 매장 埋藏·埋葬·상점 의미를 분리한다.
E101|25,21|참호의 흙벽·바닥·통로|S31,S40|direct|location|P2|군사 참호는 방호·이동 문맥을 가진 지면 통로다.|trench::a narrow recessed passage with continuous earthen walls;duckboard::wooden boards resting on the muddy passage floor;sandbag::sandbags placed along part of the upper trench edge|duckboard:rests_on:trench_floor|트렌치코트와 구별한다. 역사·지역·시기별 요소는 선택적이며 모든 참호에 덧붙이지 않는다.
E102|25,8,28|파괴 구덩이와 매몰 생활 흔적|S16,S40|named_context|aftermath_trace|P2|구덩이 외형과 폭발·충돌·굴착 원인은 별도 의미다.|crater::a ground depression with a disturbed raised rim;ejecta::displaced soil fragments adjoining that rim;object::a household object partly buried in nearby sediment|ejecta:adjoins:crater|정지 구덩이만으로 포탄 종류·폭발 원인·전쟁을 확정하지 않는다.
E103|25,24|지뢰·암매장·집단매장·생매장의 관찰 경계|S30,S40|context|none|P2|은폐·범죄·살아 있음·피해 규모는 외형과 별개인 사건 문맥이다.|buried_object::an object partially obscured by deposited soil;soil_cover::soil covering a clearly bounded part of that object;record::a separate scene narrative identifying the requested event|soil_cover:occludes:buried_object|평범한 흙을 지뢰·범죄 흔적으로 추정하지 않는다. 설치·은폐·실행 절차는 시각 의미 데이터에 포함하지 않는다.
E104|26,30|가이아·텔루스·게브·대지모신의 문화 문맥|S43,S40|context|none|P2|대지 신격의 성별·재료·표상은 문화와 개별 자료에 따라 다르다.|object_reference::a specific cited cultural object reference;iconographic_detail::a documented motif on that same object;catalogue::the object catalogue identifying place and period|catalogue:describes:object_reference|모든 대지 신을 흙 피부의 풍만한 여성으로 강제하지 않는다. 게브 자료의 거위 연관도 보편 외형으로 확대하지 않는다.
E105|26,20|지신·터주·사직·지신밟기|S33,S44,S45|named_context|action|P2|땅·집터·곡식 의례와 농악 공연은 구별되는 문화 문맥이다.|performers::a named regional nongak group within a village yard;instruments::percussion instruments held by the same performers;yard::the ground of that yard continuous beneath the group|performers:stand_on:yard|땅을 밟는 동작 하나를 지신밟기로 확정하지 않는다. 사직은 사직 resignation 의미와 구별한다.
E106|26,16|파차마마·아푸와 땅에 바치는 행위|S34|named_context|action|P2|안데스 자료의 봉헌·돌무더기·산신 문맥을 구체 사례로 유지한다.|offering::liquid poured from a vessel onto a bounded ground spot;vessel::a ceremonial vessel held above that same spot;cairn::a documented stone offering pile beside the ground spot|offering:contacts:ground_spot|모든 안데스 땅 장면에 같은 의례를 강제하지 않는다. 인카 ushnu 태양 제단과 파차마마 봉헌은 자료 맥락을 구별한다.
E107|26|흙 골렘의 재료와 작용|S32,S40|reuse|subject|P2|골렘 전승과 선택한 흙 재질의 허구적 구현을 분리한다.|golem::a constructed humanoid with a visibly earthen body;body_joint::lump-like articulated joints belonging to that body;material_trace::earthen crumbs beside a hand acting on one object|material_trace:originates_at:golem|기존 구성 재료·행위 프로필을 재사용한다. 돌 거인·살아 있는 갑옷과 재질만으로 동일시하지 않는다.
E108|26,30|떠 있는 지층과 대지 마법|S40|fantasy|surreal_physics_detail|P2|허구 물리와 실제 지질 작용은 명시적으로 구별한다.|floating_block::a layered earth block separated from the ground;root::roots hanging from its exposed underside;ground_gap::a continuous air gap beneath the same block|root:hangs_from:floating_block|사진적 자연 설명으로 융기·섭입을 이 장면에 연결하지 않는다. 석화 저주는 선택한 변환 경계가 필요하다.
E109|27,29|피부 위 진흙의 부착과 접촉 흔적|S40|direct|skin_condition|P0|피부와 진흙은 경계·두께·접촉 흔적으로 구별한다.|skin::visible bare skin adjoining a local mud coating;mud_coat::a thick mud patch adhering to that same skin;finger_track::a dragged fingertip track crossing the coating edge|mud_coat:adheres_to:skin|노동·놀이·의례·패션·페티시 문맥을 외형만으로 결정하지 않는다. 피부 색을 흙 색으로 바꾸지 않는다.
E110|27,29|옷에 묻은 진흙과 젖은 천|S40|direct|garment_detail|P0|고형 부착물과 천의 수분 변화는 서로 다른 표면 효과다.|garment::an opaque garment retaining its original seams;mud_deposit::raised muddy clumps attached near the garment hem;stain_edge::a bounded deposit edge contrasting with nearby clean fabric|mud_deposit:adheres_to:garment|진흙·젖음으로 의복 투명화·노출·소재 변경을 자동 허용하지 않는다. 물 후보의 광학 관계와 경계를 유지한다.
E111|27|머드팩·목욕·놀이·레슬링의 목적 문맥|S40|context|none|P1|비슷한 진흙 접촉 외형이라도 장면의 목적은 다르다.|mud::mud contacting a clearly identified skin patch;tool::an applicator or play object belonging to the chosen scene;setting::a setting consistent with the separately stated activity|tool:contacts:mud|머드팩의 미용 효능·머드놀이의 성적 의미·레슬링의 의도를 외형으로 확정하지 않는다.
E112|27|WAM·스플로싱·머드 페티시|S40|context|none|P2|원 대화의 하위문화 용어는 명시된 취향 문맥으로 보존한다.|mud_coat::a local mud coating with a visible material boundary;gesture::a hand contacting that same coating;garment::the requested garment structure retained beside the contact|gesture:contacts:mud_coat|용어의 1차 자료 검증은 미완료다. 일반 splosh 동사·비성적 진흙 접촉을 취향 표기로 승격하지 않는다. 동의·흥분은 픽셀로 판단하지 않는다.
E113|27|흙냄새·페트리코·지오스민|S26|context|none|P0|비와 지표의 접촉은 냄새 성분을 공기로 옮기는 과정과 관련된다.|raindrop::a raindrop contacting a previously dry soil patch;wet_patch::a local wet patch around that same contact;plant::nearby vegetation retained in the scene context|raindrop:contacts:wet_patch|냄새를 갈색 연기·녹색 발광으로 고정하지 않는다. 지오스민 분자·페트리코의 향은 실제 사진 gate로 삼지 않는다.
E114|27,2|식토 토성·지오파지 식토의 동음 경계|S35,S40|context|none|P0|점토 함량의 토성 말과 흙을 먹는 행위는 다른 뜻이다.|clay_sample::a separately identified clay-rich soil specimen;context_record::a record stating material classification or consumption context;scene_subject::the explicitly requested actor kept separate from specimen identity|context_record:describes:clay_sample|흙을 만지는 손을 섭취 장면으로 바꾸지 않는다. 영양·치료 효능이나 건강 상태를 외형으로 주장하지 않는다.
E115|28,2|달 레골리스의 표면과 발자국|S41|direct|surface_material|P1|달 표면 재료와 지구의 생물성 토양은 환경이 다르다.|regolith::a grey granular regolith bed around one bootprint;bootprint::sharp tread impressions pressed into that same bed;rock_fragment::small angular rock fragments beside the impression|bootprint:within:regolith|회색 흙만으로 달 위치를 증명하지 않는다. 바람에 떠다니는 먼지·낙엽·유기 뿌리를 자동 추가하지 않는다.
E116|28,25|충돌구와 분출물의 원인 경계|S41,S42|named_context|location|P2|원인 이름과 오목한 지형·주변 분출물의 외형은 분리한다.|impact_crater::a bounded crater with a continuous raised rim;ejecta::a radial rough deposit extending beyond that rim;terrain::surrounding terrain continuous with the crater exterior|ejecta:surrounds:impact_crater|화산 분화구·포탄 구덩이·싱크홀과 구별한다. 정지 외형으로 충돌체·연대를 확정하지 않는다.
E117|28,17|충돌 유리와 어글루티네이트의 배율|S42|micro|none|P2|어글루티네이트는 유리질 결합을 가진 입자라는 재료 문맥이다.|grain::an identified agglutinate grain under microscopy;glass_binding::glass-like material connecting fragments within that grain;scale_bar::a calibrated microscopic scale adjoining the grain|glass_binding:binds:grain|달 풍경의 거대한 유리 구슬·반짝이로 대신하지 않는다. 미세 재료 정체는 검증 시료 문맥이 필요하다.
E118|28,18|레골리스 모사토와 현지자원활용|S41,S42|context|none|P2|모사 재료·실제 천체 시료·장비 용도는 별도 식별한다.|sample::a labelled regolith simulant container;apparatus::a documented processing apparatus adjoining that container;output::a separately identified processed specimen|apparatus:uses:sample|지구 실험실 시료를 실제 달 시료로 주장하지 않는다. ISRU 기술 가능성과 실제 운용 성공은 사진으로 확정하지 않는다.
E119|30,1,24|고향·죽음·기억·금기·뿌리내림|S40|symbolic|none|P2|비유는 장면 의미를 열어두며 보편적인 물체 레시피가 아니다.|hand::a hand holding a bounded amount of soil;place::a separately stated meaningful place in the frame;gesture::a visible gesture directed toward that held soil|gesture:directed_at:hand|흙으로 돌아가다를 즉시 시신·무덤으로, 뿌리내리다를 몸의 실제 뿌리로 강제하지 않는다. 소속감은 픽셀에서 확정하지 않는다.
E120|20,29,30|풍요·척박함·생장 관계의 선택적 표현|S22,S40|context|none|P1|생장 외형과 비옥도·정서·토양 건강 진단은 구별한다.|seedling::a seedling emerging from one crumbly soil patch;root::roots entering that same patch at a visible edge;soil::granular soil supporting the stem at its base|root:penetrates:soil|새싹·검은 흙만으로 비옥도·재생·희망을 증명하지 않는다. 인간의 반응은 배우·대상·행위·감정·결과를 별도 작성한다.
""".strip()

SOURCE_ROWS = [
    ("S01", "USDA NRCS Soil Survey Manual", "https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual", "direct_page", "관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다."),
    ("S02", "NRCS Soil Texture and Structure Guide", "https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf", "pdf_structure_verified", "입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다."),
    ("S03", "NRCS A Soil Profile", "https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile", "direct_text", "수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별."),
    ("S04", "IUSS WRB Documents", "https://wrb.isric.org/documents.html", "direct_text_version", "WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다."),
    ("S05", "WRB Reference Soil Groups", "https://wrb.isric.org/soilgroups/", "direct_text_overview", "32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다."),
    ("S06", "NPS Aeolian Landforms", "https://www.nps.gov/subjects/geology/aeolian-landforms.htm", "direct_text", "바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경."),
    ("S07", "NPS River Systems and Fluvial Landforms", "https://www.nps.gov/subjects/geology/fluvial-landforms.htm", "direct_text", "유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계."),
    ("S08", "NPS Karst Landscapes", "https://www.nps.gov/subjects/caves/karst-landscapes.htm", "direct_text", "용해성 기반암·함몰·지하 물길·샘의 관계."),
    ("S09", "NPS Beaches and Coastal Landforms", "https://www.nps.gov/subjects/geology/coastal-landforms.htm", "direct_text", "육수 경계·침식/퇴적 해안과 재료/조석/파랑 조건의 분리."),
    ("S10", "NRCS Resource Concern Guide Sheets", "https://www.nrcs.usda.gov/sites/default/files/2023-03/Resource%20Concern%20Guide%20Sheets_1.pdf", "primary_search_excerpt", "침식·다짐·유기물·염류 등 자원 문제 범주. 개별 현상 진단은 조사 자료가 필요하다."),
    ("S11", "NRCS Rangeland Water Erosion", "https://www.nrcs.usda.gov/sites/default/files/2024-05/NRCS_Rangeland%20Soil_Water%20Erosion_Factsheet_04092024.pdf", "primary_search_excerpt", "면상 유실과 집중 유출에 의한 세류·구곡, 속도 감소 구간의 퇴적."),
    ("S12", "NRCS Rangeland Hydrology and Soil Erosion", "https://directives.nrcs.usda.gov/sites/default/files2/1712930328/33930.pdf", "primary_search_excerpt", "실제 세류/구곡 사진 및 도랑 두부와 사면의 관계. 수치 기준은 보편 threshold로 전사하지 않는다."),
    ("S13", "USGS Aquifers and Groundwater", "https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater", "primary_search_excerpt_after_timeout", "대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout."),
    ("S14", "USGS What Is Groundwater", "https://www.usgs.gov/faqs/what-groundwater?items_per_page=6&page=1", "primary_search_excerpt", "지하 호수/강이라는 단일 비유로 지하수를 설명하지 않는 경계."),
    ("S15", "USGS Landslide Types and Processes", "https://pubs.usgs.gov/circ/c1244/c1244.pdf", "primary_search_excerpt", "회전형·병진형 등 재해 유형과 물질·이동 방식의 구별."),
    ("S16", "USGS Effects of Earthquakes", "https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes", "primary_search_excerpt", "낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다."),
    ("S17", "NRCS Soil Biology Primer", "https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer", "direct_text_scope", "먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다."),
    ("S18", "British Geological Survey Rocks and Minerals", "https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/", "direct_page_scope", "암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다."),
    ("S19", "NPS Glaciers and Glacial Landforms", "https://home.nps.gov/subjects/geology/glacial-landforms.htm", "primary_search_excerpt", "빙하 침식과 퇴적 지형 및 틸과 지형의 구별."),
    ("S20", "NSIDC Science of Frozen Ground", "https://nsidc.org/learn/parts-cryosphere/frozen-ground-permafrost/science-frozen-ground", "direct_text", "2년 이상 동결의 정의, 얼음 쐐기·열카르스트와 관측 문맥."),
    ("S21", "V&A An A-Z of Ceramics", "https://www.vam.ac.uk/articles/a-z-of-ceramics", "primary_search_text_and_page", "슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다."),
    ("S22", "NRCS Soil Health Management", "https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management", "direct_text", "교란·피복·뿌리·식물 다양성과 관리 이력의 관계."),
    ("S23", "NPS Preservation of Historic Adobe Buildings", "https://www.nps.gov/orgs/1739/upload/preservation-brief-05-adobe.pdf", "direct_pdf_text", "전통 어도비의 비소성·재료·흙 줄눈·목재 등과의 접합."),
    ("S24", "Getty Earthen Architecture", "https://www.getty.edu/news/why-earthen-architecture-may-be-a-big-part-of-our-future/", "direct_text", "어도비·판축·와틀 도브와 지역/문화별 건축 변형."),
    ("S25", "Historic England Repairing Walls", "https://historicengland.org.uk/advice/your-home/maintain-repair/walls/", "primary_search_excerpt", "목구조의 엮은 골격과 흙 채움, 콥 등 흙벽 및 보호 마감."),
    ("S26", "MIT Rainfall Can Release Aerosols", "https://news.mit.edu/2015/rainfall-can-release-aerosols-0114", "direct_text", "빗방울 접촉과 에어로졸 이동 연구; 냄새의 가시적 실체를 주장하지 않는다."),
    ("S27", "MFA CAMEO Umber", "https://cameo.mfa.org/wiki/Umber", "direct_text", "엄버의 안료 재료·raw/burnt 차이. 색만으로 화학 조성을 판단하지 않는다."),
    ("S28", "MFA CAMEO Sienna", "https://cameo.mfa.org/wiki/Sienna", "blocked_403", "원 대화와 안료 계열의 추가 출처 단서. 시에나 세부 화학은 확인 미완료."),
    ("S29", "Dia Robert Smithson Spiral Jetty Publication", "https://www.diaart.org/about/press/dia-art-foundation-and-the-university-of-california-press-publish-new-book-on-robert-smithsons-monumental-earthwork-spiral-jetty/type/text", "primary_search_excerpt", "작품·영화·텍스트와 장소 관계. 모든 대지미술을 나선으로 일반화하지 않는다."),
    ("S30", "한국학중앙연구원 한국민족문화대백과사전 무덤", "https://encykorea.aks.ac.kr/Article/E0018983", "direct_text", "봉분·매장 공간·재료별 무덤의 구별. 범죄 사건 판단의 자료가 아니다."),
    ("S31", "IWM Voices of the First World War Trench Life", "https://www.iwm.org.uk/podcasts/voices-of-the-first-world-war/ep-20-trench-life", "direct_fetch_failed", "원 대화의 역사 출처 단서. 장비·구조·시대별 세부는 후속 확인 대상으로 남긴다."),
    ("S32", "Jewish Museum Berlin GOLEM", "https://www.jmberlin.de/en/exhibition-golem", "direct_text", "전승과 다양한 현대 표상; 특정 흙 거인 외형을 보편 골렘 정의로 삼지 않는다."),
    ("S33", "국립국악원 지신밟기", "https://www.gugak.go.kr/ency/topic/view/747", "direct_text", "농악대·집/마을 의례·공동우물 등 지역별 진행 차이."),
    ("S34", "NMAI Inka Road Religion", "https://americanindian.si.edu/inkaroad/inkauniverse/inkaroadexpansion/road-religion.html", "direct_text", "파차마마 봉헌·아푸·apacheta와 us hnu의 자료별 맥락."),
    ("S35", "NRCS Rangeland Ecohydrology Soil Particle Size", "https://directives.nrcs.usda.gov/sites/default/files2/1712930384/33921.pdf", "primary_search_excerpt", "USDA 입경 수치와 육안으로 구분 가능한 입경의 한계."),
    ("S36", "NPS Arid and Semi-arid Landforms", "https://www.nps.gov/subjects/geology/arid-landforms.htm", "direct_text", "메사·뷰트의 평탄한 상부/급한 사면, 자갈 포장, 산지 출구의 선상 퇴적을 본문에서 확인. 수치 크기 기준을 만들지 않는다."),
    ("S37", "USGS This Dynamic Earth Plate Boundaries", "https://pubs.usgs.gov/gip/dynamic/understanding.html", "direct_fetch_failed", "원 대화의 판 구조 출처 단서. 지도/단층의 상세 지질 해석은 승격 전 재확인."),
    ("S38", "NPS Sandy Coast Landforms", "https://www.nps.gov/articles/sandy-coast-landforms.htm", "direct_text", "사주·사취·육계사주의 연결/퇴적 관계."),
    ("S39", "NPS Speleothems", "https://www.nps.gov/subjects/caves/speleothems.htm", "direct_text", "천장 종유석·바닥 석순·연결 기둥의 부착 방향을 본문에서 확인. 형태만으로 정확한 광물 조성을 판정하지 않는다."),
    ("S40", "흙 관련 용어 조사 및 이번 저작 제안", "https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a", "user_referenced_conversation_not_primary_fact", "용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다."),
    ("S41", "NASA What Is Lunar Regolith", "https://science.nasa.gov/biological-physical/what-is-lunar-regolith/", "direct_text", "각진 표면 재료·발자국·자원 이용 연구. 본문의 지구 토양 단순화는 S01/S03으로 교차 해석한다."),
    ("S42", "NASA Moon Composition", "https://science.nasa.gov/moon/composition/", "direct_text_and_primary_search", "암편·광물편·유리·어글루티네이트 및 입경/발생 환경의 차이."),
    ("S43", "Met Cosmetic Spoon 27.3.614", "https://www.metmuseum.org/art/collection/search/552553", "direct_text", "거위와 게브의 연관을 신중하게 설명한 개별 소장품. 게브 신상의 보편적인 외형 자료는 아니다."),
    ("S44", "한국학중앙연구원 지신", "https://encykorea.aks.ac.kr/Article/E0054279", "direct_text", "대지·토지의 신격이라는 정의와 터의 신앙 문맥."),
    ("S45", "한국학중앙연구원 사직", "https://encykorea.aks.ac.kr/Article/E0025967", "direct_page_scope", "토지·곡식 의례의 출처 입구. 사직 resignation과 구별하기 위한 문맥 검토."),
    ("S46", "USGS What Is a Tectonic Plate", "https://pubs.usgs.gov/gip/dynamic/tectonic.html", "primary_search_excerpt_after_403", "기관 검색 본문에서 판이 대륙·해양 암석권을 함께 포함할 수 있음을 확인; 직접 요청은 403. 대륙 윤곽과 판을 동일시하지 않는다."),
    ("S47", "NPS Cryptobiotic Soil Crusts", "https://www.nps.gov/glca/learn/nature/soils.htm", "primary_search_excerpt", "생물 피각과 일반 마른 물리 피막을 구별하는 출처 단서."),
]


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_units():
    units = []
    for line in UNIT_ROWS.splitlines():
        parts = line.split("|")
        if len(parts) != 11:
            raise ValueError((len(parts), line))
        uid, groups, label, sources, mode, slot, priority, definition, visible, relation, contrast = parts
        components = []
        for index, text in enumerate(visible.split(";"), 1):
            owner, phrase = text.split("::", 1)
            components.append({
                "id": f"{uid.lower()}_component_{index}",
                "owner": owner,
                "visible_phrase_en": phrase,
                "evidence_kind": "authored_observation_proposal",
                "pixel_gate": f"Resolve {phrase} on its declared owner {owner} in the original image. Missing, hidden, contradictory or wrongly owned evidence fails.",
            })
        a, typ, b = relation.split(":")
        units.append({
            "id": uid, "original_groups": [int(g) for g in groups.split(",")],
            "label_ko": label, "definition_ko": definition,
            "source_ids": sources.split(","), "representation_mode": mode,
            "proposed_slot": None if slot == "none" else slot,
            "priority": priority, "components": components,
            "relations": [{"id": f"{uid.lower()}_relation_1", "subject": a, "type": typ, "object": b}],
            "confusion_boundary_ko": contrast,
            "semantic_fact_status": "bounded_by_source_status; authoring proposal is not an empirical observation",
            "runtime_status": "research_only_not_registered",
            "capture_policy": {
                "macro": "Frame the material and a same-plane scale; do not infer microscopic particles.",
                "micro": "Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.",
                "diagram": "Require an explicit map/cutaway/diagram request; no natural-photo projection.",
                "context": "Retain named context; components are optional bridges, not required evidence of the abstract term.",
                "symbolic": "Retain authored emotional context; never turn metaphor into an automatic object recipe.",
                "named_context": "Visible form is optional; cause/classification/culture/time requires separately grounded context.",
                "fantasy": "Require explicit fictional physics and open concept scope.",
                "reuse": "Review the cited existing ID before adding any duplicate realization.",
                "direct": "Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.",
            }[mode],
        })
    # Replace inaccessible general tectonics pointers for the high-level
    # plate distinction; detailed fault/continental reconstructions remain
    # explicitly subject to follow-up source review.
    for unit in units:
        if unit["id"] in {"E070", "E071"}:
            unit["source_ids"] = ["S46", "S40"]
        if unit["id"] == "E075":
            unit["source_ids"].append("S47")
    return units


REUSE = {
    "E012": ["slot:surface_material:water_w120", "profile:water_rel_w120"],
    "E035": ["slot:location:water_w002", "profile:water_rel_w002"],
    "E043": ["profile:karst_closed_depression_losing_stream_resurgence"],
    "E052": ["slot:location:water_w069", "profile:water_rel_w069"],
    "E053": ["slot:location:water_w070", "profile:water_rel_w070"],
    "E056": ["slot:location:water_w077", "profile:water_rel_w077"],
    "E064": ["profile:karst_closed_depression_losing_stream_resurgence"],
    "E067": ["slot:subject:active_glacier_landform_subject", "slot:composition:ice_flow_valley_moraine_frame"],
    "E068": ["slot:subject:freeze_thaw_soil_polygon_patch"],
    "E075": ["slot:subject:biological_soil_crust_patch", "slot:action:showing_soil_crust_maturity_boundary"],
    "E107": ["slot:subject:constructed_golem_subject", "profile:golem_constructed_material_agency"],
    "E118": ["slot:prop:rover_sample_trace_prop"],
}

SCOPE = {
    "texture": ("material", "selected_surface", "surface_structure"),
    "surface_material": ("material", "selected_surface", "surface_material"),
    "ambient_particle": ("atmosphere", "scene_particles", "source_and_distribution"),
    "aftermath_trace": ("material", "selected_surface", "contact_trace"),
    "location": ("setting", "selected_terrain", "spatial_structure"),
    "color": ("color", "selected_surface", "object_color"),
    "action": ("action", "selected_actor", "physical_interaction"),
    "subject": ("subject", "selected_subject", "physical_category_and_structure"),
    "prop": ("material", "selected_prop", "surface_material"),
    "surreal_physics_detail": ("concept", "selected_terrain", "fictional_physics"),
    "skin_condition": ("appearance", "main_subject", "skin.surface_coating"),
    "garment_detail": ("appearance", "main_subject", "wardrobe.surface_deposit"),
}

KOREAN_COMPONENTS = {
    "E002": ["한 모래 표면에서 굵은 알갱이가 낱개로 구분됨", "인접한 모래알 사이에 작은 그림자가 생김", "모래와 같은 초점면에 놓인 크기 기준"],
    "E005": ["잘린 흙 단면의 작은 부스러기형 입단", "각 입단을 둘러싼 불규칙한 자연 경계", "단면 안으로 이어지는 입단 사이 틈"],
    "E007": ["바퀴가 닿는 곳의 마른 흙 표면", "접촉점에서 시작하여 공중으로 이어지는 먼지", "같은 흙바닥에 닿아 있는 바퀴"],
    "E008": ["얕은 홈이 형태를 유지하는 진흙 바닥", "그 진흙 바닥 옆에 고여 있는 흙탕물", "바닥과 고인 물을 가르는 보이는 경계"],
    "E009": ["같은 흙에서 촉촉한 무광 부분과 더 젖은 부분", "더 젖은 부분에 국한된 수막 반사", "같은 흙 표면을 가로지르는 국소 수분 경계"],
    "E010": ["부츠 한쪽이 진흙 표면을 눌러 일부 잠김", "바로 옆 같은 진흙에 남은 맞는 밑창 자국", "눌린 자국 가장자리로 밀려 올라온 진흙"],
    "E011": ["한 흙길에 나란히 이어지는 두 차륜 홈", "홈 양옆에 밀려 올라온 흙 능선", "각 홈의 진행 방향과 맞는 반복 타이어 자국"],
    "E012": ["한 마른 퇴적면에 이어진 다각형 균열", "균열로 둘러싸인 마른 퇴적물 판", "균열과 판 전체를 담는 하나의 건조 바탕"],
    "E014": ["손가락 끝이 한 덩이 점토를 누름", "그 점토에 남아 형태를 유지하는 손가락 홈", "새 홈 옆 같은 점토의 접힌 가장자리"],
    "E016": ["지표에서 아래로 이어지는 연속 수직 토양 단면", "서로 다른 흙 띠를 가르는 불규칙한 경계", "같은 단면에 붙여 놓은 수직 깊이 기준"],
    "E017": ["지면 맨 위에 놓인 알아볼 수 있는 낙엽 조각", "낙엽 조각 바로 아래의 더 어두운 광물성 층", "낙엽과 표토 경계를 가로지르는 가는 뿌리"],
    "E019": ["암석 접촉면 위의 느슨한 풍화 조각", "접촉면 아래의 이어진 단단한 기반암", "느슨한 물질과 단단한 암석 사이의 전이"],
    "E021": ["중립 조명 아래 한 적갈색 토양 부분", "흙 옆에 놓인 중립 색 기준", "그 색 부분 안에 드러난 입자 질감"],
    "E035": ["구분되는 자연 지표 구멍에서 나오는 물", "그 출수점과 끊김 없이 연결된 얕은 물길", "출수점 바로 옆의 젖은 바탕"],
    "E036": ["한 노출 사면에 팬 가늘고 얕은 물길 여러 개", "내리막을 따라 갈라지는 세류 홈", "그 물길 입구 아래에 쌓인 작은 퇴적물"],
    "E038": ["현재 물길 옆 아래가 파인 흙 하안", "같은 노출 하안에서 밖으로 나온 뿌리", "파인 가장자리 아래에 놓인 떨어진 흙덩이"],
    "E080": ["일부 잎맥이 남은 분해 중 낙엽", "그 낙엽 아래에 있는 어두운 유기물 조각", "두 층이 함께 놓인 하나의 숲바닥"],
    "E081": ["잘린 흙벽 하나에서 뻗어 나오는 가지 친 뿌리", "노출 뿌리 주위로 이어지는 고운 흙벽", "굵은 뿌리와 연결된 흙벽 위 식물"],
    "E086": ["엇갈린 단으로 쌓인 굽지 않은 흙벽돌", "같은 벽돌 사이를 구분하는 흙 줄눈", "입자와 섬유가 드러난 벽돌의 깨진 모서리"],
    "E088": ["하나의 연속 흙벽에 나타난 수평 다짐층", "다짐층을 가로지르는 규칙적인 거푸집 자국", "이어진 다짐 재료가 보이는 벽 가장자리"],
    "E089": ["깨진 벽 패널에서 드러난 엮은 나뭇가지", "같은 나뭇가지 주위에 붙어 있는 흙 배합물", "채움 패널의 경계를 이루는 목재 틀"],
    "E093": ["같은 물레 위 그릇 하나를 빚는 두 손", "그 물레 중심에 있는 젖은 점토 그릇", "손가락과 물레 가장자리에 묻은 묽은 점토액"],
    "E109": ["국소 진흙 피막 옆에 보이는 원래 맨피부", "같은 피부에 두께를 갖고 붙은 진흙 부분", "그 진흙 경계를 가로지르는 손가락 쓸린 자국"],
    "E110": ["원래 봉제선이 유지되는 불투명 의복", "그 의복의 밑단 가까이에 붙은 도톰한 진흙덩이", "근처 깨끗한 천과 구분되는 국소 부착물 경계"],
    "E115": ["부츠 자국 주위의 회색 입자성 레골리스", "같은 바탕에 선명하게 눌린 밑창 자국", "자국 옆의 작은 각진 암편"],
}

# These are specific effects in addition to the slot's material/scene effect.
# They remain proposals; the final maintenance pass must inspect every owner.
EXTRA_EFFECTS = {
    "E007": [("action", "wheel", "ground_contact")],
    "E010": [("pose", "main_subject", "foot.contact_depth")],
    "E014": [("pose", "main_subject", "hand.contact_shape")],
    "E082": [("setting", "selected_terrain", "furrow_structure")],
    "E093": [("pose", "main_subject", "hand.contact_shape"), ("count", "main_subject", "visible_hands")],
    "E094": [("pose", "main_subject", "hand.contact_shape")],
    "E105": [("setting", "selected_terrain", "yard_context"), ("role", "selected_actor", "cultural_activity")],
    "E106": [("relationship", "selected_actor", "contact_target"), ("setting", "ground_spot", "offering_context")],
    "E108": [("setting", "selected_terrain", "ground_separation")],
    "E109": [("material", "main_subject", "skin.surface_deposit"), ("pose", "main_subject", "hand.contact_shape")],
}


def build_proposals(units, sources):
    proposals = []
    templates = []
    source_by_id = {s["id"]: s for s in sources}
    for unit in units:
        slot = unit["proposed_slot"]
        if slot is None:
            continue
        uid = unit["id"]
        phrases = [c["visible_phrase_en"] for c in unit["components"]]
        ko_phrases = KOREAN_COMPONENTS.get(uid, [])
        korean_proposition = "; ".join(ko_phrases)
        proposition = "; ".join(phrases) + "."
        effects = [dict(dimension=d, target=t, property=p)
                   for d, t, p in [SCOPE[slot], *EXTRA_EFFECTS.get(uid, [])]]
        dimensions = list(dict.fromkeys(e["dimension"] for e in effects))
        status = "reuse_existing_or_scoped_enrichment" if uid in REUSE else "new_realization_draft"
        low_evidence = [s for s in unit["source_ids"] if source_by_id[s]["evidence_status"]
                        in {"direct_fetch_failed", "blocked_403", "direct_page_scope", "direct_text_scope",
                            "pdf_structure_verified", "primary_search_excerpt", "primary_search_excerpt_after_timeout",
                            "primary_search_excerpt_after_403", "user_referenced_conversation_not_primary_fact"}]
        candidate = {
            "id": "soil_" + uid.lower(),
            "ko": unit["label_ko"] + "의 선택적 관찰 표현",
            "en": "; ".join(phrases),
            "weight": 0.45, "tags": ["soil_earth", "owned_observation"],
            "aliases": [], "keywords": [unit["label_ko"], *phrases, *ko_phrases],
            "paraphrases": [proposition, *([korean_proposition] if korean_proposition else [])],
            "embedding_text": unit["label_ko"] + "; " + proposition + (" " + korean_proposition if korean_proposition else ""),
            "concept_terms": phrases, "concept_units": phrases,
            "relations": unit["relations"],
            "affected_dimensions": dimensions, "affected_properties": effects,
            "core_assertion_discovery": True,
            "contextual_usage": {"contexts": [{
                "id": "soil_" + uid.lower() + "_boundary",
                "definition": unit["confusion_boundary_ko"],
                "observable_interpretation": "; ".join(phrases),
                "claim_limits": [unit["capture_policy"]],
                "activation_authority": "interpretation_only_not_a_required_visual_recipe",
            }]},
        }
        if slot == "subject":
            candidate["kind"] = ["object"] if uid == "E107" else ["animal"]
        components = [{
            "id": c["id"], "match_terms": [c["visible_phrase_en"], *([ko_phrases[i]] if ko_phrases else [])],
            "evidence_field": c["id"] + "_phrase", "evidence_terms": [c["visible_phrase_en"]],
            "min_content_words": 3,
            "instruction": "Bind the selected component to its declared owner and preserve the connection: " + c["visible_phrase_en"] + ".",
            "render_gate": {"id": "vo_soil_" + c["id"],
                            "review_scale": "native", "description": c["pixel_gate"]},
        } for i, c in enumerate(unit["components"])]
        profile = {
            "id": "soil_rel_" + uid.lower(), "category": "soil_earth_owned_observation",
            "activation": {
                "exact_terms": [proposition],
                "requires_adult_character": False,
                "semantic_discovery_requires_component_evidence": True,
                "hard_activation": {
                    "contract_version": "photo-visual-hard-activation/v1",
                    "required_any_groups": [{"id": "complete_owned_proposition", "any_terms": [proposition]}],
                },
            },
            "semantics": {
                "definition": "; ".join(phrases),
                "paraphrase_examples": [unit["label_ko"], proposition, *([korean_proposition] if korean_proposition else [])],
                "visual_components": phrases, "contrast_examples": [unit["confusion_boundary_ko"]],
                "claim_limits": [
                    "Scientific class, origin, history, chemistry, smell, intent and consent require separately grounded context.",
                    unit["capture_policy"],
                ],
            },
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": components},
            "concept_candidate": {"concept_terms": phrases, "core_assertion_discovery": True,
                                  "affected_dimensions": dimensions, "affected_properties": effects},
            "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                                   "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "reject_substitutes": [unit["confusion_boundary_ko"]],
        }
        meta = {
            "proposal_id": "proposal_" + uid.lower(), "research_unit_id": uid,
            "priority": unit["priority"], "source_ids": unit["source_ids"],
            "disposition": status, "existing_refs": REUSE.get(uid, []),
            "promotion_status": "not_registered_not_indexed_not_published",
            "source_followup_ids": low_evidence,
            "language_status": "owned_Korean_and_English_components_drafted" if ko_phrases else "English_components_Korean_label; natural_Korean_components_pending",
            "adoption_prerequisites": [
                "Bind each physical owner to the frozen core and final scene.",
                "Review effects against all open dimensions and property locks.",
                "Do not treat the glossary label or semantic similarity as a full requester proposition.",
                "If named context or multiple variants are involved, review and split before integration.",
            ],
        }
        proposals.append({**meta, "suggested_slot": slot, "candidate_draft": candidate})
        templates.append({**meta, "profile_draft": profile})
    return proposals, templates


def build_mapping(units, original):
    # Mapping is a review routing aid, not a 470-term exact-activation table.
    # Per-term refinement and unresolved definitions are explicit in the report.
    return [{
        "term_id": f"g{g['number']:02d}_t{i:02d}", "term": term, "original_group": g["number"],
        "research_unit_ids": [u["id"] for u in units if g["number"] in u["original_groups"]],
        "mapping_kind": "group_to_research_review_queue_not_semantic_equivalence",
        "activation": "none_from_term_mapping",
    } for g in original["groups"] for i, term in enumerate(g["terms"], 1)]


def main():
    units = build_units()
    source_data = {
        "schema_version": "soil-earth-research-sources/v1", "access_date_kst": "2026-10-08",
        "method": "primary agency, research institution or museum pages; source status distinguishes text/excerpt/scope/blocked/reference",
        "sources": [dict(id=i, title=t, url=u, evidence_status=s, supported_scope_ko=n)
                    for i, t, u, s, n in SOURCE_ROWS],
    }
    write_json("sources.json", source_data)
    write_json("research-units.json", {
        "schema_version": "soil-earth-research-units/v1",
        "stage": "research_and_implementation_plan_only",
        "units": units,
        "policy": "No unit is a current runtime rule, scientific classification detector or image-quality certification.",
    })
    proposals, templates = build_proposals(units, source_data["sources"])
    write_json("candidate-proposals.json", {"schema_version": "soil-earth-candidate-proposals/v1",
               "note": "Reviewable drafts including reuse records; never import this wrapper into live extension assets.",
               "proposals": proposals})
    write_json("visual-profile-proposals.json", {"schema_version": "soil-earth-visual-profile-proposals/v1",
               "note": "Compiler-compatible draft shape does not prove source completeness, activation quality, retrieval or pixels.",
               "proposals": templates})
    original = json.loads((OUT / "original-keywords.json").read_text())
    write_json("keyword-routing.json", {"schema_version": "soil-earth-keyword-routing/v1",
               "routing": build_mapping(units, original)})
    write_json("reuse-plan.json", {"schema_version": "soil-earth-reuse-plan/v1",
               "reuse": [{"research_unit_id": k, "existing_refs": v, "status": "verify_identity_and_meaning_before_implementation"}
                        for k, v in REUSE.items()]})
    lines = ["# 120개 흙·땅 연구 카드", "",
             "모든 항목은 연구·저작 제안이다. 정의의 출처 상태와 시각 구현의 검증 상태는 별개다.",
             "각 card의 구성은 전체 term의 공통 외형이 아니라 선택 가능한 구체적 realization이다.", ""]
    by_source = {s["id"]: s for s in source_data["sources"]}
    for unit in units:
        lines.extend([
            "## " + unit["id"] + " · " + unit["label_ko"], "",
            unit["definition_ko"], "",
            "원 대화 범주: " + ", ".join(map(str, unit["original_groups"])) +
            " · 표현 방식: " + unit["representation_mode"] + " · 우선순위: " + unit["priority"], "",
            "| 소유 대상 | 선택한 관찰 표현 |", "|---|---|",
            *[f"| {c['owner']} | {c['visible_phrase_en']} |" for c in unit["components"]], "",
            "관계: " + "; ".join(f"{r['subject']} → {r['type']} → {r['object']}" for r in unit["relations"]), "",
            "혼동 경계: " + unit["confusion_boundary_ko"], "",
            "프레이밍·배율·채택 조건: " + unit["capture_policy"], "",
            "출처: " + ", ".join(f"[{s} {by_source[s]['title']}]({by_source[s]['url']})" for s in unit["source_ids"]), "",
            "출처 확인 범위: " + "; ".join(f"{s} [{by_source[s]['evidence_status']}] {by_source[s]['supported_scope_ko']}" for s in unit["source_ids"]), "",
        ])
    (OUT / "research-cards.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"research_units": len(units), "source_records": len(SOURCE_ROWS),
                      "owned_observation_proposals": sum(len(u["components"]) for u in units),
                      "candidate_drafts": len(proposals), "profile_drafts": len(templates)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
