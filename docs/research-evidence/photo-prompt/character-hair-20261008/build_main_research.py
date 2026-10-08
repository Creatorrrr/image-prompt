"""Build bounded research artifacts only; never imported by the runtime.

All outputs are in this research folder. Sources, card geometry and integration
choices are author proposals with claim-level support, not rendered-image proof.
"""
import csv
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
INVENTORY = {r['id']: r for r in csv.DictReader((OUT / 'reference/keyword-inventory.tsv').open(), delimiter='\t')}


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def source(id, publisher, title, url, read_status, claim, limits):
    return dict(id=id, publisher=publisher, title=title, url=url,
                accessed_on='2026-10-08', retrieval_status=read_status,
                supported_claim=claim, limitations=limits,
                source_image_pixels_reviewed=False, verbatim_quote_words=0)


SOURCES = [
    source('M01', 'Stanford / Marschner et al.', 'Light Scattering from Human Hair Fibers',
           'https://graphics.stanford.edu/papers/hair/', 'direct_primary_abstract',
           'Measured hair reflection has multiple specular features and depends on fiber orientation and pigmentation.',
           'Physical reference, not a generation benchmark or a colour classifier.'),
    source('M02', 'PBRT authors', 'PBRT 4e 9.9 Scattering from Hair',
           'https://www.pbr-book.org/4ed/Reflection_Models/Scattering_from_Hair', 'direct_body',
           'Hair absorption, roughness and scattering geometry jointly affect its rendered appearance.',
           'A rendering model does not establish a fixed RGB for a hairstyle label or the true colour in one photo.'),
    source('M03', 'Bico et al. / Nature / PubMed', 'Adhesion: elastocapillary coalescence in wet hair',
           'https://pubmed.ncbi.nlm.nih.gov/15592402/', 'primary_abstract_in_search_direct_body_limited',
           'Wet flexible lamellae form bundles through elastocapillary interaction in the published model.',
           'Full paper not read. This is a lamella/brush model, not proof that glossy clumps in an image contain water.'),
    source('M04', '한국학중앙연구원', '한국민족문화대백과사전: 댕기',
           'https://encykorea.aks.ac.kr/Article/E0015303', 'direct_body',
           '댕기는 땋은 머리 끝 등에 연결하는 천 장식이며 형태·용도가 다양하다.',
           '실루엣 하나로 시대·신분·혼인·착용자의 정체성을 확정하지 않는다.'),
    source('M05', '한국학중앙연구원', '한국민족문화대백과사전: 상투',
           'https://encykorea.aks.ac.kr/Article/E0027380', 'direct_body',
           '머리를 모아 정수리 쪽에 감아 올린 구조와 동곳·망건의 문화적 맥락.',
           '현대 topknot과 역사적 상투의 이름을 무조건 같은 exact 의미로 합치지 않는다.'),
    source('M06', 'Wella', 'Shockwaves Extra Strong Wet Look Gel',
           'https://www.wella.com/international/hair-style/gel/wella-shockwaves-extra-strong-wet-look-gel-200-ml', 'direct_body',
           '제품은 마르거나 축축한 머리에 바르고 자연 건조하여 wet effect를 연출하도록 안내한다.',
           '젤 성분의 수분이나 광택을 실제 비·물에 젖은 사건의 증거로 바꾸지 않는다.'),
    source('M07', 'Kitsch', 'Black & Tort Micro Cloud Clip Set',
           'https://www.mykitsch.com/products/black-tort-micro-cloud-clip-set', 'direct_body',
           '클립을 열어 모발 구역 위에 놓고 닫아 고정한다. 작은 구역과 half/full updo 적용 용례.',
           '모든 claw clip의 이빨 수·재료·치수나 성능을 이 제품 하나에서 일반화하지 않는다.'),
    source('M08', 'Kitsch', 'Cherry Blossom Ruched Satin Scrunchies',
           'https://www.mykitsch.com/products/cherry-blossom-ruched-satin-scrunchies-5pc-set', 'direct_body',
           '주름진 새틴 scrunchie를 포니테일·브레이드·번의 묶음에 사용하는 용례.',
           '색·무늬는 제품 사례다. 마찰·건강·보호·손상 방지 홍보 주장은 의미 데이터에 채택하지 않는다.'),
    source('M09', 'BELLAMI Europe', 'Hair Extensions Frequently Asked Questions',
           'https://eu.bellamihair.com/pages/frequently-asked-questions', 'direct_body',
           'clip weft 규격과 wrap ponytail / clip ponytail의 서로 다른 접합 방법을 직접 설명한다.',
           '붙임머리 전체에 한 접합법을 강제하지 않음. 완성 사진만으로 실제 설치법을 입증하지 않음.'),
    source('M10', 'Jon Renau', 'Top Smart 18 Lace Front Topper',
           'https://jonrenau.com/top-smart-18', 'direct_body',
           '국소 crown topper에 lace front, clip, adhesive tab이 함께 구성되는 제품 사례.',
           'lace-front와 topper는 배타 클래스가 아니다. 이 제품의 치수·clip 수가 보편 정의는 아니다.'),
    source('M11', 'Jon Renau', 'Catalina Blonde Toppers',
           'https://jonrenau.com/blog/catalina-blonde-toppers/', 'direct_body',
           '같은 색명도 lace-front 여부·hairline 설치 위치에 따라 flash-front 배치가 달라지는 제품 사례.',
           '이 브랜드의 특정 출시 사례. 전역 hairline 거리나 색표 규칙으로 확장하지 않음.'),
    source('M12', 'L’Oréal Paris', 'Tips to Tame Flyaways',
           'https://www.lorealparisusa.com/beauty-magazine/hair-care/frizzy-hair/tips-to-tame-flyaways', 'direct_body',
           '주 흐름과 다르게 솟는 짧은 가닥을 flyaway로 설명하며 여러 가능한 원인을 든다.',
           '시각 설계는 이탈 방향만 채택. 손상·새 성장·정전기·위생 원인을 사진에서 진단하지 않음.'),
    source('M13', 'L’Oréal Paris', 'How to Tame Frizzy Baby Hairs',
           'https://www.lorealparisusa.com/beauty-magazine/hair-care/frizzy-hair/how-to-tame-baby-hairs', 'direct_body',
           'hairline 근처 작은 wispy strands를 눌러 정렬하거나 그대로 두는 용례.',
           '모발이 짧다는 이유로 영유아·유전·성장 상태를 추론하지 않음.'),
    source('M14', 'L’Oréal Paris', 'Guide to Edge Styling',
           'https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/guide-to-edge-styling', 'direct_body',
           'hairline wisps를 아래로 정렬하거나 swoop/swirl 모양으로 연출한다.',
           '머리 경계의 연출 형태를 저장. 이를 인종·성별의 필수 증거로 만들지 않음.'),
    source('M15', 'BELLAMI', 'Tape-In Express Weft Installation',
           'https://www.bellamihair.com/a/blog/pro-tips/tape-in-express-weft-installation-how-to-get-the-hidden-row-effect',
           'search_primary_excerpt_only_direct_404',
           '검색에 남은 자사 글은 tape-in + weft 하이브리드 설치를 설명한다.',
           '현재 직접 열람은 404. 이 자료만으로 구체 설치법의 검증 완료를 선언하지 않는다.'),
]


def card(suffix, ko, en, ids, region, definition, signature, relations, boundaries, sources,
         wording, support='direct_class_support_author_geometry_proposal', domain='accessory_attachment'):
    return dict(id='hair.main.' + suffix, status='research_draft_not_runtime',
                labels=dict(ko=ko, en=en), namespace='hair.' + domain, domain=domain,
                owner='subject.hair', region=region, definition=definition,
                observable_components=signature,
                directed_relations=[dict(source=a, relation=b, target=c) for a,b,c in relations],
                minimum_signature=signature, confusion_boundaries=boundaries,
                source_refs=sources, source_support_status=support,
                input_keywords=[INVENTORY[i] for i in ids],
                proposed_candidate_wording=dict(en=wording, activation='optional_after_core_adoption'),
                camera_visibility=dict(required_region=region, hidden_relation='UNOBSERVABLE_NOT_PASS'),
                pixel_gate=dict(status='not_run', all_of=signature, outcomes=['PASS','FAIL','UNOBSERVABLE_NOT_PASS']),
                procedure_or_identity_inference='not_proven_from_still_image')


CARDS = [
 card('baby_hair', '헤어라인 짧은 모발', 'Baby hairs at the hairline', ['H022'], 'forehead_and_temporal_hairline',
      '헤어라인에서 이어지는 짧은 가닥의 위치 표현. 공중으로 솟는지는 별도 축이다.',
      ['짧은 가닥의 뿌리가 헤어라인과 연결됨','주 모발 덩어리와 구별되는 짧은 길이'],
      [('short_strand','emerges_from','hairline')], ['flyaway와 함께 존재 가능','짧다고 끊어진 모발이나 새 성장을 진단하지 않음'], ['M13','M14'],
      'short fine-looking strands tracing the forehead hairline', domain='surface'),
 card('flyaway', '흐름 밖으로 뜬 잔가닥', 'Flyaway strands', ['H022','H371'], 'crown_part_or_hairline',
      '주 모발의 방향·표면에서 벗어나 따로 솟거나 떠 있는 가닥의 상태.',
      ['주 모발 흐름이 보임','가닥이 그 흐름 밖으로 돌출함'], [('flyaway','deviates_from','main_hair_flow')],
      ['baby hairs는 부위·길이이고 flyaway는 이탈 상태','다른 인물의 머리나 배경 실선으로 대체하지 않음'], ['M12'],
      'a few fine strands lifting away from the main hair flow', domain='surface'),
 card('laid_edges', '눌러 연출한 헤어라인 곡선', 'Laid edges / hairline swirls', ['H022'], 'forehead_and_temporal_hairline',
      '짧은 헤어라인 가닥이 피부 가까이 정렬되어 swoop 또는 swirl을 만드는 선택 변형.',
      ['헤어라인에 연결된 짧은 가닥','피부 가까이 이어지는 선택된 곡선'], [('short_strand','traces_curve_on','forehead_edge')],
      ['이마 전체를 덮는 fringe와 구별','착용자의 인종·성격을 추론하지 않음'], ['M14'],
      'short hairline wisps smoothed into a visible curved swoop', domain='surface'),
 card('ribbon_or_fabric_bow', '천 리본·보우 접합', 'Fabric hair ribbon / bow', ['H386','H387'], 'selected_gather_base_or_clip_site',
      '별도 천 재료가 모발 밑동을 감싸거나 고정 부품을 통해 연결된 장식. 보우와 리본의 배치를 분리한다.',
      ['모발과 구별되는 천 재료','장식과 모발 구역의 접합이 보임'], [('fabric_ribbon','attached_to','hair_carrier')],
      ['모발 자체로 만든 보우 H204와 구별','보우 형태만으로 clip/tie라는 숨은 설치법을 확정하지 않음'], [],
      'a fabric ribbon visibly tied around the selected hair base', support='input_term_geometry_proposal_material_source_followup',
      domain='accessory_attachment'),
 card('hair_formed_bow', '모발 자체로 만든 보우', 'Bow formed from hair', ['H204'], 'selected_gather_site',
      '같은 모발 다발이 좌우 loop와 가운데 조임으로 이어지는 보우 모양. 천 장식은 별도 의미다.',
      ['모발의 연속적인 좌우 loop','같은 모발이 가운데 접힘에 이어짐'], [('hair_loop_left','joins_at','hair_bow_center'),('hair_loop_right','joins_at','hair_bow_center')],
      ['천 보우를 모발 보우로 합격시키지 않음','판타지 ribbon-like flat hair와 조형 보우를 분리'], [],
      'the gathered hair itself shaped into two loops joined at a visible center',
      support='input_term_geometry_proposal_dedicated_source_hold',domain='fantasy_or_styled_shape'),
 card('fabric_scarf', '천 헤어 스카프', 'Fabric hair scarf', ['H396','H397'], 'head_or_gather_base',
      '모발과 별개인 천이 머리 또는 묶음 구역을 감싸는 장식. headwrap의 덮는 범위는 따로 지정한다.',
      ['모발과 구별되는 천 면','천이 머리·모발 구역을 감싸는 관계'], [('fabric_scarf','wraps','head_or_hair')],
      ['목을 두르는 모발 H447와 별도 namespace','근처 배경 천은 착용 증거가 아님'], [],
      'a fabric scarf wrapped around the selected hair region',support='input_term_geometry_proposal_attachment_source_followup'),
 card('hair_neck_wrap', '목을 감싸는 모발', 'Hair wrapping around the neck', ['H447'], 'long_hair_and_neck',
      '같은 인물의 긴 모발이 머리에서 연속되어 목 주위를 감싸는 형태. bare hair scarf로 천 의미와 병합하지 않는다.',
      ['두피에서 이어지는 모발 길이','그 길이가 목 주위를 둘러 지나감'], [('hair_length','continuous_from','subject_scalp'),('hair_length','wraps','subject_neck')],
      ['천 스카프 H397 제외','접촉 형태는 독립적 의지·움직임의 증거가 아님'], [],
      'a continuous length of the subject’s hair curving around the neck',
      support='input_term_geometry_proposal_platform_support_in_other_lane', domain='fantasy_or_styled_shape'),
 card('scrunchie', '주름진 천 밴드로 묶음 고정', 'Scrunchie at a hair base', ['H388'], 'gather_base',
      '주름진 천이 둘러진 밴드가 선택한 모발 묶음의 밑동을 감싼다.',
      ['주름진 천 고리','같은 묶음 밑동을 둘러싼 접촉'], [('scrunchie','encircles','gather_base')],
      ['장식만 곁에 떠 있거나 손목에 있으면 헤어 접합 미충족','특정 색·재질·건강 효능은 필수 아님'], ['M08'],
      'a ruched fabric scrunchie encircling the ponytail base'),
 card('claw_clip', '클립으로 다발 고정', 'Claw clip securing a hair section', ['H393'], 'selected_hair_section',
      '열고 닫는 클립의 구조가 선택한 모발 구역을 잡아 고정하는 접합.',
      ['별도 클립 몸체','클립과 모발 다발의 고정 접촉'], [('claw_clip','grips','hair_section')],
      ['clip 크기·색·이빨 수는 별도 변형','모발 가까이 있는 클립만으로 고정 판정 불가'], ['M07'],
      'a visible claw clip gripping the gathered hair section'),
 card('pin_insertion', '핀·스틱의 삽입 경로', 'Inserted hairpin / stick attachment', ['H389','H390','H398','H399'], 'bun_or_selected_hair_section',
      '핀·스틱·빗의 보이는 부분이 선택 모발 구역 안으로 들어가며 연결된다. 각 도구의 구조는 별도 subtype이다.',
      ['모발 구역과 별도 도구','도구가 모발 안으로 이어지는 삽입 경로'], [('hair_tool','inserts_into','hair_section')],
      ['금속 선을 머리카락으로 대체하지 않음','숨은 잠금·U핀 형태·빗니 수를 invent하지 않음'], ['M09'],
      'a hairpin visibly inserted through the selected gathered section',
      support='M09_anchor_example_only_specific_pin_types_source_followup'),
 card('threaded_or_clamped_adornment', '가닥을 통과·감싸는 장식', 'Bead / cuff / ring on a strand', ['H400','H401','H402','H403'], 'strand_or_braid_length',
      '장식 subtype의 구멍·열린 고리·커프 또는 연결 고리가 모발 가닥·땋은 길이와 연결된다.',
      ['장식의 물질 경계','모발 carrier를 통과하거나 감싸는 연결'], [('adornment','attaches_to','strand_or_braid')],
      ['각 subtype의 thread/clamp/link는 관찰에 따라 분리','목걸이나 배경 장신구로 substitute 금지'], [],
      'small adornments visibly connected along the selected braid',support='attachment_geometry_proposal_specific_subtypes_source_followup'),
 card('tinsel_attachment', '모발에 연결된 반짝임 실', 'Hair tinsel strands', ['H404'], 'root_to_length',
      '별도 반짝임 실이 모발 구역에서 시작하여 같은 흐름을 따라 내려가는 접합 제안.',
      ['모발과 다른 반짝임 실','모발 구역에서 길이로 이어지는 흐름'], [('tinsel','attached_near','hair_root'),('tinsel','follows','hair_length')],
      ['빛 반사만으로 실제 tinsel 선언 금지','귀걸이·배경 glitter와 소유자 분리'], [],
      'fine reflective tinsel strands attached within and following the hair',support='input_term_geometry_proposal_reuse_y2k_source_review'),
 card('clip_in_weft', '클립이 있는 붙임 모발 띠', 'Clip-in hair weft', ['H408','H410','H412'], 'attachment_row',
      '띠 형태의 모발 조각과 clip 접합을 분리하여 보관한다. clip-in bangs는 앞머리 적용 구역의 변형이다.',
      ['모발 조각의 base 또는 띠','clip이 자연 모발 구역에 연결됨'], [('extension_fibers','emerge_from','weft_base'),('clip','connects','weft_base_to_hair')],
      ['완성 길이나 숱만으로 clip 설치법 판정 불가','weft는 tape-in 방식과 조합될 수 있음'], ['M09'],
      'a clip-in hair piece with its base and attachment visible',support='direct_clip_weft_class_support_bang_variant_source_followup',domain='installation'),
 card('tape_attachment', '테이프 설치 구역', 'Tape-in attachment', ['H409','H410'], 'revealed_attachment_row',
      '접합부가 드러나거나 명시된 시술 문맥에서 tape 설치를 별도 표현한다. 완성 외형과 동일시하지 않는다.',
      ['명시되거나 관찰 가능한 접합 row','붙임 모발과 carrier의 연결'], [('extension_base','attaches_to','natural_hair_section')],
      ['완성 사진만으로 adhesive 종류나 설치법 미입증','weft와 tape는 배타성 없음'], ['M15'],
      'an extension attachment row revealed beneath the upper hair',support='search_only_primary_direct_404_hold_installation_claim',domain='installation'),
 card('ponytail_piece', '포니테일 피스와 밑동 연결', 'Ponytail extension attachment', ['H413'], 'ponytail_base',
      '모발 조각의 꼬리가 기존 포니테일 밑동에 연결된다. wrap과 clip은 서로 다른 설치 변형이다.',
      ['기존 묶음 밑동','밑동에 연결되는 피스의 길이'], [('extension_tail','attaches_to','existing_ponytail_base')],
      ['길고 풍성한 포니테일만으로 붙임모발 확정 불가','제품 변형의 숨은 clip/anchor를 invent하지 않음'], ['M09'],
      'a ponytail hair piece visibly connected at the gathered base',domain='installation'),
 card('lace_front', '레이스 앞경계 구조', 'Lace-front construction', ['H414','H415'], 'frontal_hairpiece_boundary',
      '앞쪽 lace 구조를 가진 모발 제품의 경계. 전체 가발과 국소 topper 모두에 나타날 수 있다.',
      ['앞쪽의 lace 또는 명시된 제품 경계','경계에서 이어지는 모발 fibers'], [('hairpiece_fibers','anchored_to','front_lace')],
      ['자연스럽게 보이는 hairline만으로 lace 제품 판정 불가','lace-front와 topper를 배타성 규칙으로 만들지 않음'], ['M10','M11'],
      'the frontal lace edge of the hair piece shown at the hairline',domain='installation'),
 card('topper', '국소 모발 피스의 덮는 영역', 'Hair topper coverage', ['H415'], 'hairline_or_crown_piece_base',
      '국소 base가 머리 일부를 덮고 나머지 모발과 연결되는 피스. 앞경계 위치와 설치법은 제품별로 다르다.',
      ['국소 피스의 base 영역','주변 모발과의 연결'], [('topper_base','covers','selected_head_region'),('piece_fibers','blends_with','remaining_hair')],
      ['완성 사진만으로 탈모나 임상 상태를 진단하지 않음','명도·볼륨만으로 topper라고 분류하지 않음'], ['M10','M11'],
      'a local hair topper with its coverage base and surrounding hair visible',domain='installation'),
 card('daenggi', '댕기와 땋은 끝의 연결', 'Daenggi braid-end attachment', ['H416','H417'], 'braid_end',
      '천 댕기가 땋은 머리 끝 또는 해당 유형의 지정 부위에 연결되는 관계. 장식과 헤어 구조를 따로 저장한다.',
      ['땋은 모발의 연속적인 끝','그 끝과 연결된 천 장식'], [('daenggi','attached_to','braid_end')],
      ['천 장식 색으로 혼인·신분을 자동 판정하지 않음','각 시대·유형의 배치 차이는 별도 맥락'], ['M04','T13'],
      'a cloth daenggi visibly connected to the end of the braid'),
 card('sangtu', '정수리에 감아 올린 상투', 'Sangtu crown wrap', ['H418'], 'crown_gather',
      '머리에서 연속된 길이를 정수리 부근에 모아 감아 올린 구조. 역사적 이름의 사용은 문맥에 유지한다.',
      ['모발이 정수리로 모임','모인 길이가 같은 상투 몸체로 감겨 있음'], [('hair_lengths','gather_at','crown'),('gathered_lengths','wrap_into','sangtu_body')],
      ['현대 topknot과 역사적 이름을 무조건 alias 병합하지 않음','동곳·망건은 요청·유형에 따른 별도 장식'], ['M05'],
      'hair gathered upward and wrapped into a compact crown sangtu',domain='cultural_structure'),
]


ACCESSORY_GROUPS = [
 ('fabric_tie_or_bow', ['H386','H387','H388'], 'wraps_or_ties_to_gather_base', ['M08'], 'scrunchie 직접 용례; ribbon/bow 특정 접합은 추가 출처 필요'),
 ('inserted_tool', ['H389','H390','H398','H399'], 'inserts_into_hair_or_bun', ['M09'], 'pony anchor 예시만 직접 확인; U핀·빗 subtype 정의 보완'),
 ('clip_subtypes', ['H391','H392','H393','H394'], 'grips_or_clamps_hair_section', ['M07'], 'claw clip 직접 용례; barrette/snap/banana subtype은 설치 구조 추가 조사'),
 ('head_cover_or_band', ['H395','H396','H397'], 'encircles_or_covers_head', ['M13'], 'headband 용례; scarf/headwrap 범위는 창작 선택과 직접 자료 보완'),
 ('strand_adornment', ['H400','H401','H402','H403','H404'], 'threads_clamps_links_or_follows_strand', [], '관계 설계 제안; 각 재료·접합 subtype 및 Y2K 기존 source 확인 필요'),
 ('placed_head_adornment', ['H405','H406','H407'], 'attached_at_head_or_hair_carrier', [], '생화·티아라·베일은 다른 소품 slot과 중복 소유자 검토; 고정 부품 보이지 않으면 설치법 미확인'),
 ('extension_piece', ['H408','H409','H410','H411','H412','H413'], 'piece_base_attaches_to_head_or_hair', ['M09','M15'], 'clip/weft/pony 직접 계열; tape 현재 본문 보류; halo/clip bangs 특정 구성 보완'),
 ('hairpiece_base', ['H414','H415'], 'fibers_anchor_to_local_or_whole_base', ['M10','M11'], 'lace-front topper 공존 직접 제품 사례; 완성 외형으로 제품이나 임상 상태 추정 금지'),
]


def main():
    save('main-sources.json', dict(status='research_source_receipts_not_runtime', as_of='2026-10-08', sources=SOURCES))
    save('main-cards.json', dict(status='research_draft_not_runtime', card_count=len(CARDS), cards=CARDS,
                                note='Source supports its stated claim only. Operational geometry and image gates are design proposals.'))
    rows=[]
    for group, ids, relation, refs, note in ACCESSORY_GROUPS:
        rows.extend({**INVENTORY[i], 'attachment_family':group, 'proposed_relation':relation,
                     'source_refs':refs,'support_boundary':note,'runtime_adoption':'not_performed'} for i in ids)
    assert len(rows)==30 and len({r['id'] for r in rows})==30
    save('ACCESSORY-DISPOSITION.json',dict(status='research_proposals_with_explicit_holds', rows=sorted(rows,key=lambda r:r['id'])))
    print(json.dumps(dict(main_cards=len(CARDS),main_sources=len(SOURCES),accessory_dispositions=len(rows))))


if __name__ == '__main__':
    main()
