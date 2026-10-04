"""Author research-only keyword cards; this script never writes runtime assets."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
ASSETS = REPO / 'skills/photo-prompt-image-generator/assets'
receipts = json.loads((ROOT / 'SOURCE-RECEIPTS.json').read_text())
supplemental = json.loads((ROOT / 'SUPPLEMENTAL-SOURCES.json').read_text())
cases = {x['case_id']: x for x in receipts['cases']}
sources = {x['source_id']: x for x in [*receipts['receipts'], *supplemental['receipts']]}
profiles = {}
for path in ASSETS.glob('photo_prompt_visual_obligations*.json'):
    for profile in json.loads(path.read_text()).get('profiles', []):
        profiles[profile['id']] = (path.name, profile)

cards = []


def add(n, group, term, en, owner, ko_units, en_units, edges, seeds,
        decision, existing, slot, prop, contrasts, gate, limit='', priority='P1'):
    cid = f'K{n:02d}'
    units_ko = ko_units.split(';')
    units_en = en_units.split(';')
    assert len(units_ko) == len(units_en), cid
    refs = []
    for seed in seeds.split():
        sid = cases[seed]['source_id'] if seed.startswith('C') else seed
        refs.append({'case_id': seed if seed.startswith('C') else None,
                     'source_id': sid, 'url': sources[sid]['requested_url'],
                     'review_status': sources[sid].get('visual_review_status', 'not_reviewed')})
    existing_ids = existing.split()
    assert all(x in profiles for x in existing_ids), (cid, existing_ids)
    relations = [{'id': f'{cid.lower()}_r{i}', 'type': kind,
                  'subject': subject, 'object': obj}
                 for i, (subject, kind, obj) in enumerate(edges, 1)]
    dimension = 'body_geometry' if slot == 'silhouette_proportion' else (
        'material' if slot == 'surface_material' else 'appearance')
    if slot == 'prop':
        dimension = None
    cards.append({
        'id': cid, 'group': group, 'reference_term': term, 'en_label': en,
        'owner': owner,
        'visible_components': [{'id': f'{cid.lower()}_c{i}', 'ko': k, 'en': e}
                               for i, (k, e) in enumerate(zip(units_ko, units_en), 1)],
        'required_relations': relations,
        'source_examples': refs,
        'source_use': 'Design evidence and research leads; the listed source does not certify every proposed component or every version.',
        'authoring_decision': decision,
        'existing_profile_crosswalk': [
            {'profile_id': x, 'file': profiles[x][0],
             'current_definition': profiles[x][1].get('semantics', {}).get('definition', ''),
             'relationship': 'reusable_or_related_scope; read the card limits before binding'}
            for x in existing_ids],
        'proposed_slot': slot,
        'proposed_effect': {'dimension': dimension,
                            'target': 'selected_prop' if slot == 'prop' else 'main_subject',
                            'property': prop,
                            'status': 'unresolved_prop_scope' if slot == 'prop' else 'proposal_requires_core_compatibility'},
        'confusion_boundaries': contrasts.split(';'),
        'render_gate_proposal': {'review_scale': 'native', 'all_required': True,
                                 'description_ko': gate, 'partial_is_fail': True,
                                 'occluded_required_relation': 'UNOBSERVABLE'},
        'limits': limit,
        'priority': priority,
        'qualification': 'research_only; no runtime exposure, prompt or generated-image qualification claimed',
    })


# 17 hair/face terms. Owner, geometry, color and hardware remain separate axes.
add(1, 'hair_face', '트윈테일·양갈래 묶음', 'bilateral gathered twin tails', 'main_subject.hair',
    '두피 좌우에 독립된 묶임점 두 개가 있다;각 묶임점에서 별도 머리 다발이 내려온다',
    'two separate tie points lie on opposite sides of the scalp;each tie point feeds its own descending hair bundle',
    [('left tail', 'connected_to', 'left scalp tie'), ('right tail', 'connected_to', 'right scalp tie')],
    'C001 C078 C081', 'reuse', 'bilateral_twin_tail_gather', 'hair_style', 'hair.style.gather.bilateral_roots',
    '묶이지 않은 긴 옆머리;두 가발 조각을 옆에 놓은 배치', '양쪽 묶임점과 각각 이어지는 두 다발이 동시에 보여야 한다.',
    '길이·색·묶임 높이·좌우 대칭은 별도 속성이다.')
add(2, 'hair_face', '하이 트윈테일', 'high bilateral twin-tail roots', 'main_subject.hair',
    '두 묶임점이 각 귀의 윗끝보다 높다;두 다발이 각 높은 묶임점에서 아래로 이어진다',
    'each of two scalp ties lies above its corresponding ear top;each descending tail continues from its own high tie point',
    [('left tie', 'above', 'left ear top'), ('right tie', 'above', 'right ear top')],
    'C001', 'extend', 'bilateral_twin_tail_gather', 'hair_style', 'hair.style.gather.root_height',
    '낮은 양갈래;머리끝만 위로 날린 양갈래', '귀 위치와 두 묶임점의 높이 관계를 같은 머리에서 확인한다.',
    '기존 트윈테일 정의 전체에 high를 기본값으로 추가하지 않는다.')
add(3, 'hair_face', '사이드 포니테일', 'single lateral ponytail', 'main_subject.hair',
    '한쪽 두피에 하나의 묶임점이 있다;한 다발이 그 묶임점에서 길게 이어진다',
    'one gather root lies on one side of the scalp;one continuous tail descends from that lateral root',
    [('single tail', 'connected_to', 'one lateral scalp root')],
    'C044', 'reuse', 'sca_h09', 'hair_style', 'hair.style.gather.lateral_root',
    '양갈래;귀 앞에 놓인 느슨한 옆머리', '단일 묶임점과 해당 다발의 연속성을 보여야 한다.', '얼굴의 좌우는 인물 기준이며 화면 좌우와 분리한다.')
add(4, 'hair_face', '짧은 뒤묶음', 'short partial rear gather', 'main_subject.hair',
    '후두부의 일부 모발이 한 점에 모인다;그 묶임점에서 짧은 꼬리 다발이 나온다',
    'a subset of rear scalp hair converges at one tie point;a short tail projects from that rear tie',
    [('short rear tail', 'connected_to', 'rear gather root')],
    'C003', 'new', '', 'hair_style', 'hair.style.gather.partial_rear_tail',
    '묶임점 없는 짧은 뒷머리;정수리 아호게', '후두부의 실제 묶임점과 짧은 꼬리의 접속을 함께 확인한다.',
    '참조의 렌 설명을 S003 3면도로 확인했지만 분리된 묶임점은 확정하지 못했다. 다른 공식 판본의 명확한 후면 증거를 확보하기 전 이 사례를 PASS로 쓰지 않는다.', 'P2')
add(5, 'hair_face', '보브·단발', 'compact bob perimeter', 'main_subject.hair',
    '턱 부근에서 머리의 바깥 끝선이 이어진다;같은 끝선이 얼굴 양옆을 감싼다',
    'a compact hair perimeter terminates around the jaw;the same perimeter continues around both sides of the face',
    [('bob perimeter', 'surrounds', 'same face sides')],
    'C002 C005', 'reuse', 'ca_compact_bob', 'hair_style', 'hair.style.bob.perimeter_length',
    '장발의 앞부분만 자른 히메컷;포니테일 뒤의 짧아 보이는 앞머리', '턱 부근의 전체 끝선과 후면 길이를 함께 확인한다.', '목 길이 단발을 기존 턱 길이 프로파일에 무조건 합치지 않는다.')
add(6, 'hair_face', '외뻗침·외하네', 'outward flipped hair ends', 'main_subject.hair',
    '머리끝 구간이 목 쪽에서 바깥쪽으로 휜다;끝부분의 굽음이 각 다발에 이어진다',
    'terminal hair sections bend outward away from the neck;each outward hook remains continuous with its hair strand mass',
    [('terminal bend', 'points_away_from', 'neck'), ('terminal bend', 'connected_to', 'hair mass')],
    'C007', 'new', '', 'hair_style', 'hair.style.ends.outward_flip',
    '머리 전체를 바람으로 띄운 상태;아호게', '끝부분의 반복된 외향 굽음과 모발 연결을 확인한다.', '바람·움직임·성격의 원인을 만들지 않는다.')
add(7, 'hair_face', '드릴 컬', 'repeated helical hair bundles', 'main_subject.hair',
    '한 다발이 여러 번의 나선 회전을 만든다;각 나선 다발이 자신의 묶임점에 이어진다',
    'each selected hair bundle makes several repeated helical turns;each helix continues to its own gather root',
    [('helical bundle', 'connected_to', 'its own gather root')],
    'C092', 'reuse', 'sca_h05 sca_h06', 'hair_style', 'hair.style.gather.spiral_topology',
    '단순한 물결 머리;옆에 떠 있는 나선 소품', '반복 회전·연속 다발·요청한 개수를 모두 확인한다.', '단일 포니 드릴과 좌우 트윈 드릴은 대안이다. 둘을 동시에 의무로 만들지 않는다.')
add(8, 'hair_face', '아호게·바보털', 'isolated crown hair tuft', 'main_subject.hair',
    '정수리에서 한두 다발이 주변 머리 윤곽 밖으로 솟는다;솟은 다발의 밑동이 같은 모발 덩어리에 이어진다',
    'one or two selected tufts project beyond the crown hair silhouette;each raised tuft has a root continuous with the surrounding hair',
    [('raised tuft', 'connected_to', 'same crown hair')],
    'C015 C044', 'reuse', 'sca_h01 sca_h02', 'hair_style', 'hair.style.crown.isolated_tuft',
    '안테나 장치;머리띠 장식', '다발의 개수와 두피 쪽 연속성을 확인한다.', '한 개와 두 개는 요청별 대안이며 지능·성격의 의미는 없다.')
add(9, 'hair_face', '긴 옆머리·사이드록', 'short rear hair with paired long sidelocks', 'main_subject.hair',
    '후두부의 머리는 목 위에서 짧게 끝난다;얼굴 양옆의 두 다발만 가슴 쪽까지 이어진다',
    'rear scalp hair ends above the neck;only two face-side locks extend downward toward the chest',
    [('rear hair', 'shorter_than', 'paired face-side locks'), ('long locks', 'flank', 'same face')],
    'C019 X001 X002 X003', 'new', 'hime_cut_structural', 'hair_style', 'hair.style.length.regional_partition',
    '뒷머리가 긴 히메컷;두피 양쪽의 전체 트윈테일', '후면의 짧은 길이와 두 긴 앞쪽 다발의 대비가 같은 인물에서 보여야 한다.',
    '2011 설정 자료에서 직접 확인했다. hime_cut_structural은 긴 뒷머리를 유지하므로 이 형태의 대체 프로파일이 아니다.', 'P0')
add(10, 'hair_face', '고리형 땋은 머리', 'folded braid loop', 'main_subject.hair',
    '반복 교차가 보이는 땋은 다발이 있다;그 다발을 접어 고리로 고정한다',
    'a hair bundle contains repeated braid crossings;the same braid folds back into a secured loop',
    [('braid tip', 'returns_to', 'braid fastening region'), ('loop', 'formed_from', 'same braided bundle')],
    'C039 X006', 'new', 'sca_h10 ca_hanging_hair_braid', 'hair_style', 'hair.style.braid.closed_loop',
    '정수리를 두르는 왕관 땋기;땋지 않은 머리 고리', '교차 구조와 접힌 고리, 고정점을 함께 확인한다.',
    'V3 공식 아카이브 200px 이미지는 세부 교차·고정점을 확인하기 어렵다. V5 Lite 상품 페이지에는 전신 설정화가 없다. 정밀 공식 자료 확보를 선행한다.', 'P2')
add(11, 'hair_face', '옴브레·머리끝 그라데이션', 'root-to-tip hair color transition', 'main_subject.hair',
    '같은 모발에서 뿌리와 끝의 색이 다르다;두 색 사이에 중간 색 구간이 이어진다',
    'root and tip colors differ along the same hair length;intermediate colors form a gradual transition between them',
    [('color transition', 'along', 'same strand length')],
    'C010 C026 C086', 'reuse', 'sca_h21', 'hair_color', 'hair.color.root_tip_transition',
    '조명 그라데이션;투톤의 뚜렷한 경계', '뿌리-중간-끝의 색 순서를 모발 길이를 따라 확인한다.', '색 두 개를 자동으로 고정하지 않는다. Racing2017은 피규어의 표현이다.')
add(12, 'hair_face', '투톤·분할 염색', 'spatially partitioned hair colors', 'main_subject.hair',
    '서로 다른 두 색이 지정한 머리 구획을 채운다;구획 경계가 모발에 고정된다',
    'two selected colors occupy declared hair regions;a spatial color boundary remains fixed to those hair regions',
    [('color A', 'occupies', 'declared hair region A'), ('color B', 'occupies', 'declared hair region B')],
    'C023 C052', 'extend', 'sca_h19', 'hair_color', 'hair.color.lateral_partition',
    '한쪽 조명으로 색이 달라 보이는 머리;뿌리-끝 옴브레', '지정 구획과 색의 경계를 확인한다.', '현재 sca_h19는 좌우 분할이다. 임의 큰 패널 분할은 별도 변형으로 정의해야 한다.')
add(13, 'hair_face', '안쪽 배색·언더컬러', 'revealed inner hair color layer', 'main_subject.hair',
    '겉 모발층은 한 색을 유지한다;열린 틈에서 다른 색의 안쪽 모발층이 드러난다',
    'the outer hair layer retains one color;a revealed inner hair layer carries a different color',
    [('inner color layer', 'beneath', 'outer hair layer')],
    'C031 C052', 'reuse', 'sca_h20', 'hair_color', 'hair.color.layer_partition',
    '목의 그림자;별개의 색 리본', '층의 가림 관계와 안쪽 색이 실제 모발에 속함을 확인한다.', '단일 정면 그림에서 안쪽 층인지 색 패널인지 불명확하면 UNOBSERVABLE이다.')
add(14, 'hair_face', '한쪽 눈을 가리는 앞머리', 'one-eye fringe occlusion', 'main_subject.hair',
    '앞머리 다발이 한쪽 눈 위로 이어진다;다른 눈은 별도 가림 없이 보인다',
    'fringe hair crosses over one eye;the other eye remains visible without a separate covering',
    [('fringe', 'occludes', 'one eye'), ('other eye', 'remains_visible_on', 'same face')],
    'C021 C028 C029', 'reuse', 'sca_h13', 'hair_style', 'hair.style.fringe.eye_occlusion',
    '안대;양쪽 눈을 모두 가리는 앞머리', '모발에 의한 한쪽 눈 가림과 반대 눈의 가시성을 함께 확인한다.')
add(15, 'hair_face', '주근깨', 'small face-surface dot scatter', 'main_subject.face.skin',
    '코와 볼의 지정 영역에 작은 점들이 흩어져 있다;점의 크기와 간격이 일부 달라도 같은 피부 면에 놓인다',
    'small dots scatter over declared nose and cheek regions;the dots vary in size or spacing while remaining on the same facial skin surface',
    [('dot scatter', 'lies_on', 'declared facial skin')],
    'C045 C050', 'new', 'ca_bounded_body_patches', 'body_marking', 'body.face.surface_dot_distribution',
    '얼굴 전체의 반점 패널;압축 노이즈나 별 장식', '각 점의 경계와 코·볼의 피부 소유 관계를 원본에서 확인한다.',
    '기존 cosmetic_freckle_dot_scatter 후보는 화장이라는 원인을 추가한다. 자연/화장 원인을 지정하지 않은 점 형태는 별도이며, 패키지·축약 그림의 미세 점은 확대 자료 확보 전 정밀 PASS로 쓰지 않는다.')
add(16, 'hair_face', '짙은 입술 표현', 'lip-to-skin dark value contrast', 'main_subject.face.lips',
    '입술 내부의 명도 또는 지정 색 농도가 주변 피부와 다르다;변화가 입술 경계 안에 유지된다',
    'lip value or selected color density contrasts with adjacent facial skin;the darker color remains within the lip boundary',
    [('dark lip region', 'contrasts_with', 'adjacent skin')],
    'C011', 'new', '', 'lip_color_placement', 'face.lips.color.local_contrast',
    '입 안의 검정;전체 제한색 그림의 공통 어두운 면', '입술 경계와 바로 인접한 피부의 대비를 확인한다.', 'Chika의 제한색 그림에서 관찰한 명도는 캐릭터의 고유 화장색을 확정하지 않는다.')
add(17, 'hair_face', '뺨의 표식', 'bounded cheek surface glyph', 'main_subject.face.skin',
    '한쪽 뺨의 지정 위치에 닫힌 도상 또는 선 도상이 있다;도상이 해당 피부 면 안에 붙어 있다',
    'a selected closed or linear glyph occupies one declared cheek location;the glyph remains attached to that facial skin surface',
    [('cheek glyph', 'lies_on', 'same cheek surface')],
    'C044 C032', 'extend', 'ca_surface_line_motif ca_bounded_body_patches', 'body_marking', 'body.face.surface_glyph',
    '홍채 무늬;상처나 피라는 원인 해석', '도상의 모양·위치·표면 귀속을 함께 확인한다.', 'UNI의 별, Fukase의 붉은 얼굴 표식은 별도 선택이다. 혈액·상처·정신 상태로 재해석하지 않는다.', 'P0')

# 9 proportion/body terms. Existing adult geometry cannot be copied from chibi art.
add(18, 'body', '작은 체구', 'compact frame and stature with references', 'main_subject.body',
    '같은 깊이의 기준물에 비해 전신 높이가 작다;몸통과 사지의 크기를 키와 별도로 기술한다',
    'full-body height is small against a same-plane reference;torso and limb frame extent is described separately from stature',
    [('body height', 'compared_at_same_depth_to', 'declared reference')],
    'C016 C030 C050', 'boundary', 'bm_stature_scale bm_compact_frame', 'silhouette_proportion', 'body.person.stature_scale',
    '원근 때문에 작아진 인물;축약 그림을 실제 작은 체격으로 해석', '전신 범위·같은 깊이 기준물·매체를 확인한다.', '유키 등 아동 설정이나 chibi를 성인 morphology 프로파일로 자동 변환하지 않는다. 연령은 비율에서 추론하지 않는다.', 'P2')
add(19, 'body', '높은 머리 비율', 'head-to-body length ratio with a declared medium', 'main_subject.body',
    '머리 높이의 두 기준점을 지정한다;전신 높이의 두 기준점을 같은 축척에서 지정한다',
    'head height has two declared endpoints;full-body height has two declared endpoints at the same image scale',
    [('head height', 'compared_at_same_scale_to', 'full-body height')],
    'C050 C051 C078 C081', 'boundary', 'bm_head_body_ratio', 'silhouette_proportion', 'body.body.head_body_length_relation',
    '가까운 광각 얼굴;Nendoroid 비율을 사람 기본 체형으로 전이', '매체와 기준점을 고정한 전신에서 비율을 확인한다.', 'Snow2023/2026 자료도 축약 설정표다. 성인 프로파일은 성인 요청에만 적용하고 chibi 규칙은 별도 표현 속성으로 둔다.', 'P2')
add(20, 'body', '긴 다리 비율', 'leg-to-torso length relation', 'main_subject.body',
    '골반 기준점부터 발까지의 길이를 지정한다;몸통 기준 길이와 같은 자세·축척에서 비교한다',
    'leg length is bounded by a declared pelvis landmark and foot endpoint;leg and torso reference lengths are compared in one pose at one scale',
    [('leg length', 'compared_at_same_scale_to', 'torso length')],
    'C025 C041', 'boundary', 'bm_torso_limb_ratio bm_long_limb_build', 'silhouette_proportion', 'body.body.torso_limb_length_relation',
    '하이웨이스트 의상;굽 높이나 카메라 원근', '골반·발·몸통 기준점과 의복 허리선의 차이를 확인한다.', 'bm_long_limb_build는 길고 가는 사지를 함께 요구한다. 다리 길이만 요청한 경우 가늘기까지 묶지 않는다.', 'P2')
add(21, 'body', '가느다란 팔다리', 'limb width-to-length relation', 'main_subject.body',
    '선택한 사지 구간의 양 끝점이 보인다;그 구간의 가로 폭을 길이와 별도로 비교한다',
    'the selected limb segment has visible endpoints;its transverse width is compared separately with segment length',
    [('limb width', 'compared_to', 'same segment length')],
    'C025 C034', 'boundary', 'bm_long_limb_build', 'silhouette_proportion', 'body.limbs.width_length_relation',
    '긴 다리;가느다란 옷소매', '같은 사지의 길이와 실제 윤곽 폭이 모두 보인다.', '현재 long/slender 결합 프로파일을 폭만의 의미로 쓰지 않는다. 연령·건강·체중·영양 상태를 추론하지 않는다.', 'P2')
add(22, 'body', '허리가 들어간 윤곽', 'local inward waist contour', 'main_subject.body_or_garment',
    '허리 위와 아래의 기준 폭을 지정한다;그 사이 양측 윤곽이 안으로 좁아진다',
    'reference widths are declared above and below the waist;the intervening bilateral contour narrows inward',
    [('waist contour', 'narrower_than', 'declared neighboring contours')],
    'C004 C044', 'boundary', 'hourglass_silhouette_relation bm_waist_width_depth', 'silhouette_proportion', 'body.waist.transverse_width_depth',
    '상의 절개선만 잘록한 형태;포즈나 팔로 가려진 허리', '몸 윤곽인지 의상 윤곽인지 소유자를 먼저 정한다.', '의상 허리 패널의 모양을 인체로 넘기지 않는다. 성인 body 프로파일의 조건을 유지한다.', 'P2')
add(23, 'body', '직선형 몸통 윤곽', 'low waist-indentation torso contour', 'main_subject.body',
    '상체·허리·골반의 양측 폭 차이가 비교적 작다;서로 이어진 몸통 윤곽을 같은 시점에서 본다',
    'upper torso waist and hip widths vary relatively little;the connected torso contours are visible from one declared view',
    [('upper torso contour', 'continues_through', 'waist and hip contour')],
    'C038 C043', 'boundary', 'rectangle_silhouette_relation', 'silhouette_proportion', 'body.torso.width_transition',
    '직선 코트가 몸을 가린 상태;기하학적 완전 직사각형', '세 기준 영역의 윤곽이 같은 인물에서 가려지지 않는다.', '원문의 도식적 몸통 설명을 성별·나이·정확한 등폭으로 고정하지 않는다.', 'P2')
add(24, 'body', '어깨가 드러나는 윤곽', 'declared shoulder coverage topology', 'main_subject.wardrobe',
    '목에서 위팔로 이어지는 선택한 어깨 표면이 보인다;상의 경계와 소매 경계를 서로 구분한다',
    'the selected shoulder surface from neck to upper arm remains visible;bodice and sleeve boundaries remain separately readable',
    [('shoulder surface', 'between', 'declared garment boundaries')],
    'C012 C044', 'extend', 'cold_shoulder_cutout_topology clothing_ct038_v1 clothing_ct038_v2 sca_g01', 'garment_detail', 'wardrobe.coverage.shoulder_topology',
    '어깨에 창이 있는 콜드숄더와 낮은 전체 목선을 같은 것으로 처리;가려진 어깨를 추정', '어느 재단으로 어깨가 열렸는지 실제 경계에 따라 판정한다.', '오프숄더·홀터·콜드숄더·분리 소매는 대안이며 동시 의무가 아니다.')
add(25, 'body', '피부색 대비', 'skin-to-garment local color contrast', 'main_subject.skin_and_wardrobe',
    '피부와 인접한 의복 영역을 각각 지정한다;같은 조명 아래 두 영역의 명도 또는 색 차이가 유지된다',
    'skin and neighboring garment regions are declared separately;a value or color difference remains visible between them under the same lighting',
    [('skin region', 'contrasts_with', 'adjacent garment region')],
    'C102 C032', 'new', '', 'body_marking', 'body.skin.local_carrier_contrast',
    '인종·질병으로의 해석;그림자나 전역 색보정', '경계 양쪽의 지정 영역과 지역 대비를 같은 시점에서 확인한다.', '특정 피부색을 기본으로 강제하지 않으며 종족·건강·서사를 도출하지 않는다.', 'P2')
add(26, 'body', '맨발', 'uncovered feet with continuous anatomy', 'main_subject.feet',
    '선택한 발의 발등과 발가락이 신발·양말 밖에서 보인다;발과 발목의 연결이 유지된다',
    'the selected foot dorsum and toes are visible without footwear or socks;the foot remains continuously connected to its ankle',
    [('uncovered foot', 'connected_to', 'same ankle')],
    'C036 C053', 'new', '', 'footwear', 'wardrobe.footwear.coverage.none',
    '피부색 신발;끝부분만 열린 신발', '요청한 발 전체의 외곽과 발목 연결을 확인한다.', '발뒤꿈치가 프레임 밖이면 전신 맨발의 완전 판정은 보류한다. 미성년·성인 여부나 성적 의미를 추가하지 않는다.')

# 24 garment terms.
add(27, 'garment', '분리 소매·Detached sleeves', 'detached sleeve attachment gap', 'main_subject.wardrobe.sleeves',
    '소매 윗단이 몸판의 어깨 경계와 분리되어 있다;두 경계 사이의 간격이 같은 팔에서 보인다',
    'the sleeve upper edge is separate from the bodice shoulder edge;a visible interval separates those edges on the same arm',
    [('sleeve upper edge', 'separate_from', 'bodice shoulder edge')],
    'C001 C003 C053', 'reuse', 'sca_g01 costume_ccx_cc08_02', 'garment_detail', 'wardrobe.sleeves.attachment_gap',
    '소매에 구멍만 난 콜드숄더;긴 장갑', '몸판-소매 접속이 없는 간격과 팔 소유 관계가 보여야 한다.', '소매의 폭·길이·재질은 독립 속성이다.')
add(28, 'garment', '벨 슬리브·종형 소매', 'bell sleeve widening toward an open cuff', 'main_subject.wardrobe.sleeves',
    '소매 폭이 위팔보다 손목 부근에서 넓다;끝이 열린 넓은 커프로 이어진다',
    'sleeve width increases toward the wrist;a broad open cuff terminates the same sleeve',
    [('wide cuff', 'connected_to', 'narrower upper sleeve')],
    'C001 C022', 'reuse', 'clothing_ct047_v2', 'garment_detail', 'wardrobe.sleeves.bell_width',
    '퍼프의 둥근 부피;손목을 모은 벌룬 소매', '팔 쪽 좁은 부분에서 열린 넓은 끝까지 같은 소매의 폭 변화를 확인한다.')
add(29, 'garment', '퍼프 슬리브', 'gathered short puff sleeve', 'main_subject.wardrobe.sleeves',
    '짧은 소매의 양 끝에서 주름이 모인다;두 끝 사이 천이 둥글게 부푼다',
    'gathers collect at both ends of a short sleeve;fabric bulges between those gathered boundaries',
    [('puffed fabric volume', 'between', 'two gathered sleeve edges')],
    'C081 C095', 'reuse', 'clothing_ct046_v2', 'garment_detail', 'wardrobe.sleeves.puff_volume',
    '어깨 갑주;손목만 좁은 긴 소매', '짧은 길이·모인 양 끝·중간 부피를 동시에 확인한다.', '원문 사례의 미세 주름은 축약 그림에서 충분히 확인되지 않을 수 있다.')
add(30, 'garment', '오프숄더', 'off-shoulder continuous neckline', 'main_subject.wardrobe.neckline',
    '목선 윗단이 양쪽 어깨 아래에 놓인다;소매가 낮아진 목선의 몸판에 이어진다',
    'the continuous upper neckline lies below both shoulder tops;sleeves remain connected to the lowered bodice neckline',
    [('neckline', 'below', 'both shoulder tops'), ('sleeves', 'connected_to', 'bodice')],
    'C012 C023', 'reuse', 'clothing_ct038_v2', 'garment_detail', 'wardrobe.neckline.off_shoulder',
    '홀터넥;어깨 구멍만 난 콜드숄더', '전체 목선의 낮아짐과 연결 소매를 함께 확인한다.')
add(31, 'garment', '콜드숄더·어깨 컷아웃', 'bounded shoulder cutout with fabric bridges', 'main_subject.wardrobe.shoulders',
    '각 어깨 개방부에 완성된 테두리가 있다;목선과 아래 소매를 잇는 천 경로가 남는다',
    'each shoulder opening has a finished bounded edge;a fabric route remains from neckline to the lower sleeve',
    [('shoulder opening', 'bounded_by', 'continuous garment edges')],
    'C033 C034', 'reuse', 'cold_shoulder_cutout_topology', 'garment_detail', 'wardrobe.shoulder.cutout_topology',
    '찢어진 소매;소매를 몸판에서 완전히 떼어낸 형태', '테두리·천 연결 경로·개방부가 같은 옷에서 모두 보인다.', '넓은 소매의 틈만으로 bounded cutout을 판정하지 않는다.')
add(32, 'garment', '홀터넥', 'halter neck-loop support', 'main_subject.wardrobe.top',
    '앞 몸판의 끈 또는 띠가 목 뒤로 이어진다;양 어깨의 바깥 면은 그 끈에서 떨어져 있다',
    'front bodice straps or a band continue around the rear neck;outer shoulder surfaces remain clear of that neck support',
    [('neck support', 'connects', 'front bodice and rear neck')],
    'C005 C036', 'reuse', 'clothing_ct038_v1', 'garment_detail', 'wardrobe.neckline.halter_route',
    '어깨끈 두 개;목걸이만 착용한 스트랩리스', '목 뒤 지지 경로와 앞 몸판 연결을 확인한다.', 'MEIKO 기본 3면도가 참조의 high collar 설명을 수정하는 근거다.')
add(33, 'garment', '스트랩리스', 'strapless bodice upper edge', 'main_subject.wardrobe.top',
    '몸판의 윗단이 가슴 위를 연속해서 가로지른다;몸판에서 어깨나 목으로 올라가는 끈이 없다',
    'a continuous bodice upper edge crosses above the chest;no garment strap rises from that bodice to shoulder or neck',
    [('bodice upper edge', 'separate_from', 'neck and shoulder straps')],
    'C101', 'reuse', 'clothing_ct004_v2', 'garment_detail', 'wardrobe.top.strapless_upper_edge',
    '투명 끈이 가려진 상의;홀터넥', '윗단의 연속성과 끈의 가시성을 충분한 시점에서 확인한다.', '236px 모듈 이미지는 얇은 투명 끈의 부재까지 입증하지 못한다.')
add(34, 'garment', '크롭트 톱', 'short top hem relative to the waist', 'main_subject.wardrobe.top',
    '상의 밑단이 지정한 허리 기준보다 높다;상의 밑단과 하의 허리 경계가 각각 식별된다',
    'the top hem ends above a declared waist reference;top hem and lower-garment waistband remain separate boundaries',
    [('top hem', 'above', 'declared waist reference')],
    'C002 C005 C028', 'new', 'pfe_midriff', 'garment_detail', 'wardrobe.top.hem_relative_to_waist',
    '하이웨이스트 하의로 짧아 보이는 몸통;한 벌 옷의 중앙 구멍', '상의 밑단·허리 기준·하의 경계를 확인한다.', '크롭트 길이와 피부 노출은 별도다. pfe_midriff는 성인 피부 간격을 요구하므로 크롭트 톱의 보편 대체로 쓰지 않는다.', 'P0')
add(35, 'garment', '복부 컷아웃', 'bounded abdominal garment opening', 'main_subject.wardrobe.torso_panel',
    '복부의 지정 영역에서 옷이 개방되어 있다;완성 테두리와 주변 천 연결 경로가 남는다',
    'a selected abdominal garment region contains an opening;finished edges and surrounding fabric bridges remain continuous',
    [('abdominal opening', 'bounded_by', 'same garment panel')],
    'C090 C086', 'new', 'sw_cutout', 'garment_detail', 'wardrobe.torso_panel.abdominal_opening',
    '크롭트 상의와 하의 사이 간격;피부색 인쇄 패널', '개방부·테두리·연결 천을 동시에 확인한다.', 'sw_cutout의 수영복 소유 범위를 모든 무대복으로 넓히지 않는다. 컷아웃의 위치와 크기는 요청한 범위만 적용한다.', 'P0')
add(36, 'garment', '프린세스·절개선형 몸판', 'curved princess-seam bodice panels', 'main_subject.wardrobe.bodice',
    '앞 몸판과 옆앞 몸판의 경계가 곡선으로 이어진다;경계의 양쪽이 서로 다른 봉제 패널이다',
    'curved seams join the front and side-front bodice panels;both sides of each seam belong to adjoining sewn panels',
    [('princess seam', 'joins', 'front and side-front panels')],
    'C044 C101', 'reuse', 'clothing_ct031_v1', 'garment_detail', 'wardrobe.details.princess_dart',
    '그림자 선;일반 허리 다트나 인쇄 줄', '곡선 절개와 패널 접합을 확인한다.', '컬러 패널 경계만 보이면 실제 봉제선의 입체 증거는 별도로 확보한다.')
add(37, 'garment', '주름치마·플리츠', 'repeated skirt fold structure', 'main_subject.wardrobe.skirt',
    '세로 접힘의 능선과 골이 반복된다;접힘이 같은 허리부터 치마 밑단 방향으로 이어진다',
    'vertical folded ridges and recesses repeat;the folds continue from one waistband toward the skirt hem',
    [('repeated folds', 'continue_from', 'same waistband toward hem')],
    'C001 C024', 'reuse', 'clothing_ct063_v1 clothing_ct063_v2 costume_ccx_cc39_02', 'garment_detail', 'wardrobe.skirt.pleat_topology',
    '인쇄 세로 줄;여러 수평 단의 티어드', '실제 접힘·반복·허리-밑단 연속성을 확인한다.', 'knife/inverted box는 요청에 따른 대안이며 동시에 강제하지 않는다.')
add(38, 'garment', '티어드 스커트', 'horizontal gathered skirt tiers', 'main_subject.wardrobe.skirt',
    '수평 경계로 나뉜 치마 단이 위아래로 반복된다;각 단의 모인 천이 해당 경계에 이어진다',
    'horizontal skirt tiers repeat vertically;gathered fabric in each tier joins its own horizontal boundary',
    [('gathered tier', 'attached_at', 'its horizontal seam')],
    'C026 C093', 'reuse', 'clothing_ct018_v2', 'garment_detail', 'wardrobe.skirt.horizontal_tiers',
    '같은 허리에서 겹친 여러 겹;수평 프린트 줄', '각 단의 접합과 천의 모임을 확인한다.', 'tier는 수평 단 구조이며 모든 층이 다른 길이로 겹치는 layered와 동의어가 아니다.')
add(39, 'garment', '튀튀', 'short multi-layer flaring tutu', 'main_subject.wardrobe.skirt',
    '짧은 치마가 허리에서 바깥으로 퍼진다;여러 얇은 천 층의 별도 끝선이 보인다',
    'a short skirt spreads outward from the waist;separate edges reveal several thin fabric layers',
    [('thin layers', 'spread_from', 'same waist attachment')],
    'C074 C086', 'extend', 'costume_ccx_cc27_02 clothing_ct090_v2', 'garment_detail', 'wardrobe.skirt.tutu_layer_spread',
    '속치마만 부풀린 일반 치마;한 장의 둥근 플라스틱 판', '허리 부착·외향 퍼짐·복수 얇은 층을 확인한다.', '롱 romantic tutu도 존재한다. 여기서는 참조가 요청한 short variant만 정의하며 모든 발레 의상을 짧게 만들지 않는다.')
add(40, 'garment', '프릴', 'gathered ruffle trim', 'main_subject.wardrobe.trim',
    '좁은 장식 천의 한쪽 경계에 잔주름이 모인다;반대 끝선이 물결처럼 퍼진다',
    'one edge of a narrow trim strip contains gathered folds;its opposite free edge spreads into small waves',
    [('ruffle gathered edge', 'attached_to', 'declared garment edge')],
    'C026 C081 C101', 'extend', 'clothing_ct065_v1 clothing_ct065_v2', 'garment_detail', 'wardrobe.trim.gathered_ruffle',
    '주름 없이 원형 재단으로 퍼지는 flounce;단순 물결무늬 인쇄', '모인 접합 경계와 자유 끝선을 구분해 확인한다.', '소매용 기존 ruffle과 치마용 flounce의 소유자·구조를 구분하고 필요한 공통 trim 변형만 추가한다.')
add(41, 'garment', '레이스', 'openwork textile motif layer', 'main_subject.wardrobe.surface',
    '실로 이어진 도상과 연결 부분이 있다;도상 사이에 실제 작은 빈 공간이 남는다',
    'thread motifs join through visible textile connections;actual small openings remain between those motifs',
    [('open cells', 'between', 'connected thread motifs')],
    'C026 C063', 'extend', 'clothing_ct090_v1 clothing_ct090_v2', 'surface_material', 'wardrobe.surface.openwork_motif_structure',
    '레이스처럼 인쇄한 무늬;도상 없이 균일한 mesh', '실 구조·도상·실제 빈 공간을 원본 픽셀에서 함께 확인한다.', 'guipure의 무망 구조를 모든 lace에 강제하지 않는다. 축약 그림의 흰 가장자리만으로 실제 openwork를 확정하지 않는다.')
add(42, 'garment', '비대칭 밑단', 'directional asymmetric garment hem', 'main_subject.wardrobe.hem',
    '같은 옷의 앞뒤 또는 좌우 기준 영역을 지정한다;지정한 한쪽 밑단이 다른 쪽보다 길다',
    'front-back or left-right regions are declared on one garment;the hem extends farther in one selected region than the other',
    [('selected longer hem', 'longer_than', 'opposing garment region')],
    'C020 C054', 'new', 'clothing_ct062_v2', 'garment_detail', 'wardrobe.hem.directional_length_difference',
    '포즈 때문에 한쪽이 올라간 동일 길이 치마;원근으로 짧아 보이는 밑단', '같은 옷의 기준 방향·연속 끝선·길이 차이를 확인한다.', '비대칭의 방향과 수량을 별도 속성으로 두며 좌우를 화면 기준으로 고정하지 않는다.')
add(43, 'garment', '옆트임·슬릿', 'side slit opening from a free hem', 'main_subject.wardrobe.skirt',
    '자유 밑단에서 위로 열린 옆선이 있다;열린 선 양쪽에 같은 치마의 두 가장자리가 남는다',
    'a side opening rises upward from a free hem;two edges of the same skirt flank that opening',
    [('side opening', 'rises_from', 'free skirt hem')],
    'C004 C099', 'reuse', 'clothing_ct061_v1', 'garment_detail', 'wardrobe.skirt.side_slit',
    '닫힌 복부 구멍;두 벌의 옷 사이 간격', '밑단-트임 꼭짓점-두 자락의 연속성을 확인한다.')
add(44, 'garment', '롱테일·긴 뒷자락', 'rear attached costume panel', 'main_subject.wardrobe.rear_panel',
    '짧은 앞 영역과 긴 뒤 영역이 같은 의상에 속한다;뒤 패널의 윗부분이 허리 또는 몸판에 이어진다',
    'short front and longer rear regions belong to the same costume;the rear panel upper edge joins the waist or bodice',
    [('rear panel', 'connected_to', 'same waist or bodice')],
    'C058 C059 C054', 'new', 'clothing_ct062_v1 clothing_ct062_v2 opening_tailcoat_formal_tail_topology', 'garment_detail', 'wardrobe.rear_panel.attachment_length',
    '바닥에 닿는 드레스 train;별도 망토나 정장 연미복의 두 꼬리', '연결점·앞뒤 길이 차이·뒤 패널 소유를 확인한다.', '뒤 패널이 있다는 이유로 격식 정장·바닥 접촉·두 꼬리를 추가하지 않는다.', 'P0')
add(45, 'garment', '피나포어·멜빵형 드레스', 'bib-and-strap skirt overdress', 'main_subject.wardrobe.overdress',
    '어깨끈이 가슴판과 치마 허리에 이어진다;가슴판 아래가 두 바지통이 아니라 치마로 이어진다',
    'shoulder straps join a chest bib and skirt waistband;the lower garment continues as a skirt rather than two trouser legs',
    [('shoulder straps', 'join', 'bib and skirt waistband')],
    'C016 C026', 'new', 'clothing_ct016_v1 clothing_ct016_v2 costume_ccx_cc01_01', 'garment_detail', 'wardrobe.overdress.bib_strap_skirt',
    '멜빵 바지;앞쪽에만 놓인 가슴판 앞치마', '끈-가슴판-치마 연결과 아래 별도 블라우스가 요청되었을 때 그 레이어를 확인한다.', '참조 사례의 검은 몸판만으로 실제 피나포어 전체 구조가 확정되지는 않는다. 명확한 전후면 공식 사례를 추가 확보한다.', 'P2')
add(46, 'garment', '오비형 허리띠', 'broad external waist sash', 'main_subject.wardrobe.sash',
    '폭이 넓은 별도 천 띠가 겉옷 위에서 허리를 둘러싼다;요청한 매듭이 그 띠와 이어진다',
    'a broad separate textile band encircles the outer garment at the waist;the requested knot remains connected to that sash',
    [('broad sash', 'surrounds', 'same garment waist')],
    'C087 C102', 'extend', 'costume_ccx_cc24_02 clothing_ct139_v2', 'garment_detail', 'wardrobe.sash.external_waist_band',
    '얇은 가죽 벨트;몸판 자체의 색 띠', '별도 띠·허리 둘레 경로·요청한 매듭 소유를 확인한다.', 'obi-like와 실제 kimono의 wrap/obi 체계를 구분한다. 정면에 보이지 않는 뒤 매듭은 추정하지 않는다.')
add(47, 'garment', '허벅지 길이 양말·부츠', 'upper-thigh legwear height by subtype', 'main_subject.wardrobe.legwear',
    '착용물의 윗단이 무릎 위 허벅지에 놓인다;선택한 양말 또는 부츠의 발 덮임과 밑창을 구분한다',
    'the selected legwear upper edge reaches above the knee onto the thigh;foot covering and sole construction distinguish stockings from boots',
    [('legwear top', 'above', 'same knee landmark')],
    'C001 C090 C101', 'extend', 'clothing_ct107_v1', 'wearable_accessory', 'wardrobe.legwear.height_and_subtype',
    '무릎 아래 양말;부츠와 스타킹을 한 종류로 합침', '무릎·윗단·발 덮임·선택한 밑창 구조를 확인한다.', '스타킹 기존 프로파일은 재사용하고 thigh-high boots의 단단한 신발 구조는 별도 변형으로 작성한다.')
add(48, 'garment', '가터형 연결끈', 'waist-to-stocking support straps', 'main_subject.wardrobe.garter_straps',
    '가는 끈의 위쪽 끝이 허리 지지부에 이어진다;아래쪽 끝이 같은 다리의 양말 윗단에 닿는다',
    'each narrow strap upper end joins a waist support;its lower end connects to the top of the same leg stocking',
    [('support strap', 'connects', 'waist support and stocking top')],
    'C054 C090', 'reuse', 'clothing_ct025_v1', 'garment_detail', 'wardrobe.legwear.support_connection',
    '허벅지를 두르는 가터 밴드만 있음;끈처럼 인쇄한 선', '상하 끝점의 실제 연결과 다리 소유를 확인한다.', '직업·성적 행동이나 실제 지지 기능을 그림만으로 추론하지 않는다.')
add(49, 'garment', '레그워머', 'foot-open calf tubes', 'main_subject.wardrobe.legwear',
    '별도 원통형 천이 종아리를 감싼다;발등과 발은 그 원통의 끝 바깥에 남는다',
    'a separate textile tube surrounds the calf;the foot remains outside the open lower end of that tube',
    [('calf tube', 'surrounds', 'calf without enclosing foot')],
    'C002 C003', 'reuse', 'clothing_ct107_v2', 'wearable_accessory', 'wardrobe.legwear.foot_open_tube',
    '발을 덮는 긴 양말;부츠 샤프트', '종아리의 원통·열린 하단·별도 신발 또는 맨발을 확인한다.', '게임/설정화의 장비성 부츠인지 직물 레그워머인지 재질 증거가 없는 경우 분류를 보류한다.')
add(50, 'garment', '손가락이 드러나는 장갑', 'fingerless glove hand coverage', 'main_subject.wardrobe.gloves',
    '장갑이 손등과 손바닥을 덮는다;같은 손의 손가락 끝이 장갑 밖에 보인다',
    'the glove covers the hand dorsum and palm;fingertips of the same hand remain outside the glove',
    [('exposed fingertips', 'extend_from', 'same gloved hand')],
    'C037 C038', 'reuse', 'clothing_ct106_v1', 'wearable_accessory', 'wardrobe.gloves.finger_coverage',
    '손목 커프만 착용;손가락이 가려진 프레임', '장갑 경계와 노출된 손가락이 같은 손에 이어져야 한다.')

# 22 accessory/hardware/prop terms.
add(51, 'hardware', '헤드셋', 'earpiece-to-mouth boom assembly', 'main_subject.wardrobe.headset',
    '귀 옆의 장치에 가는 마이크 막대가 붙어 있다;막대 끝이 같은 얼굴의 입 근처에 놓인다',
    'a thin microphone boom connects to an earpiece;the boom tip terminates beside the same face mouth',
    [('microphone boom', 'connected_to', 'earpiece'), ('boom tip', 'beside', 'same mouth')],
    'C001 C003 C044', 'new', 'sca_x16', 'wearable_accessory', 'wardrobe.accessories.headset_boom_route',
    '마이크 없는 헤드폰;손으로 든 마이크', '귀 장치-막대-입 옆 끝점의 한 조립체 연결을 확인한다.', 'sca_x16은 두 earcup과 돌출 장치 연결이며 mouth boom까지 보장하지 않는다. 음향 작동 여부는 별도다.', 'P0')
add(52, 'hardware', '기계형 머리 장식', 'rigid hair-tie hardware', 'main_subject.wardrobe.hair_hardware',
    '각진 판 또는 고리의 단단한 외곽이 보인다;그 장치가 머리 묶임 부근에 고정된다',
    'a rigid plate or ring has readable angular boundaries;the hardware attaches near a declared hair gather point',
    [('rigid hardware', 'attached_to', 'declared hair tie region')],
    'C001 C019 X002', 'new', 'sca_x16 y2kr_barrette', 'wearable_accessory', 'wardrobe.accessories.hair_hardware_attachment',
    '부드러운 리본;주변에 떠 있는 화면 도형', '두께 또는 단단한 경계와 머리 부착 위치를 확인한다.', '밝은 선·원형 장식만으로 전자기기, 전원 상태, 자체 발광을 확정하지 않는다.', 'P0')
add(53, 'hardware', '이퀄라이저 무늬', 'flat variable-height bar motif', 'main_subject.wardrobe.surface',
    '평행한 세로 막대가 일정 간격으로 반복된다;막대 높이가 달라도 같은 의복 표면에 놓인다',
    'parallel vertical bars repeat at regular intervals;bar heights differ while the marks remain on one garment surface',
    [('variable-height bars', 'printed_on', 'same garment panel')],
    'C044 C001', 'new', 'sca_x15', 'garment_detail', 'wardrobe.surface.equalizer_bar_layout',
    '같은 길이 세로 줄;실제 소리를 분석하는 전자 표시창', '반복 간격·높이 차이·평면 표면 귀속을 모두 확인한다.', '픽셀 블록을 쌓은 열도 변형으로 정의할 수 있다. 막대 무늬는 소리·박자·실시간 반응을 뜻하지 않는다.', 'P0')
add(54, 'hardware', '건반무늬', 'flat long-and-short keyboard motif', 'main_subject.wardrobe.surface',
    '길게 반복되는 밝은 직사각형 열이 있다;그 열의 한쪽에 더 짧고 어두운 직사각형이 어긋나 배치된다',
    'a row of long light rectangular marks repeats;shorter dark rectangles sit offset along one side of that same row',
    [('short dark rectangles', 'offset_along', 'long light rectangle row'), ('keyboard motif', 'printed_on', 'same textile panel')],
    'C026 C003 C036', 'new', 'midi_controller_external_sound_source', 'garment_detail', 'wardrobe.surface.keyboard_motif_layout',
    '독립된 건반 악기;균일한 흑백 줄무늬', '긴 밝은 열·짧은 어두운 열·평면 부착을 함께 확인한다.', 'MAYU의 치마 무늬와 사파이어의 몸 밖 건반형 고리는 다른 owner/입체 배치다. 실제 MIDI controller 프로파일을 무늬에 연결하지 않는다.', 'P0')
add(55, 'hardware', '표시창·컨트롤 패널', 'flat garment control-panel graphic', 'main_subject.wardrobe.surface',
    '작은 사각 테두리 안에 줄·점·숫자형 도형이 모인다;모든 도형이 지정한 소매 또는 치마 표면에 붙어 있다',
    'lines dots or numeral-like marks cluster inside small rectangular borders;all marks remain flat on the declared sleeve or skirt panel',
    [('panel graphic', 'printed_on', 'declared garment surface')],
    'C001 C003', 'new', 'ca_surface_fastener_row', 'garment_detail', 'wardrobe.surface.control_panel_graphic',
    '입체 단추열;손목에 별도 태블릿 부착', '사각 테두리·내부 도형·의복 면 연속성을 확인한다.', '읽을 수 있는 정확한 문자, 버튼 기능, 실제 화면·전원을 자동 추가하지 않는다.', 'P0')
add(56, 'hardware', '거대 스피커 장비', 'large circular arm-mounted speaker-like gear', 'main_subject.wardrobe.arm_gear',
    '팔 부근 장치에 바깥 원형 프레임과 안쪽 동심원 면이 있다;장치가 팔 지지부에 이어지고 손보다 큰 크기로 보인다',
    'arm-side gear has an outer circular frame and inner concentric surfaces;the gear joins an arm support and appears larger than the hand',
    [('large circular gear', 'attached_to', 'same arm support')],
    'C018', 'new', '', 'wearable_accessory', 'wardrobe.accessories.arm_circular_gear',
    '배경의 스피커;손과 연결되지 않은 떠 있는 원', '동심원 구조·팔 연결·손 대비 크기를 모두 확인한다.', '이로하 V2 패키지에서 직접 보인다. 손 전체를 덮은 경우 손가락 가시성을 동시에 요구하지 않으며 음향 출력은 추정하지 않는다.', 'P0')
add(57, 'hardware', '수정·다면체 장식', 'faceted ornament with separately selected transmission', 'main_subject.wardrobe.ornament',
    '여러 평면이 각진 모서리에서 만난다;장식의 지정 부착점 또는 소유 관계가 보인다',
    'several planar faces meet at angular edges;the ornament has a declared visible attachment or owner relation',
    [('faceted ornament', 'attached_to', 'declared carrier')],
    'C030 C031', 'extend', 'y2kr_hair_gems y2kr_rhinestones clothing_ct121_v1', 'wearable_accessory', 'wardrobe.accessories.facet_geometry',
    '밝은 점 하나;반짝임만 있는 둥근 구슬', '면-모서리-외곽과 선택한 부착점을 확인한다.', 'red stone의 고정 색을 일반 crystal에 전이하지 않는다. 투명·반투명·불투명과 작은 보석·큰 결정의 크기는 독립 속성이다.')
add(58, 'hardware', '부유 장식', 'off-body ornament with visible separation', 'selected_prop_or_external_ornament',
    '몸과 소품 사이에 연속된 배경 간격이 있다;선택한 시점에서 둘을 잇는 끈이나 지지대가 보이지 않는다',
    'a continuous background interval separates the body from the ornament;no tether or support is visible between them in the selected view',
    [('ornament', 'separated_by_visible_gap_from', 'declared body owner')],
    'C036 C037 C034', 'new', '', 'prop', 'prop.placement.off_body_visible_gap',
    '끈에 달린 소품;별도 동료 로봇을 몸 장식으로 합침', '몸-소품 사이 배경·가림 경계·지정 owner를 확인한다.', '간격은 해당 시점의 관찰이며 물리적 무지지·비행·자율 이동을 입증하지 않는다. prop 슬롯의 dimension scope는 현재 비어 있어 자동 채택을 보류한다.', 'P2')
add(59, 'hardware', '고양이 귀·여우 귀', 'paired triangular costume ear pieces', 'main_subject.wardrobe.ear_accessory',
    '삼각형 귀 형태 두 개에 안쪽 면이 구분된다;두 귀의 밑동이 같은 머리띠 또는 모자에 붙는다',
    'two triangular ear-shaped pieces contain distinct inner panels;both ear bases attach to one headband or cap carrier',
    [('two costume ear bases', 'attached_to', 'same headband or cap')],
    'C018 C047 C096 C097', 'reuse', 'costume_ccx_cc17_01 costume_ccx_cc17_02 sca_x01', 'wearable_accessory', 'wardrobe.accessories.costume_ear_carrier',
    '몸에서 자란 동물 귀;삼각형 리본 두 개', '두 외곽·안쪽 면·외부 carrier 부착을 확인한다.', 'DAINA 등의 캐릭터 해부학적 귀인지 액세서리인지 불명확하면 wearer anatomy를 변경하지 않는다.')
add(60, 'hardware', '뿔', 'horn-like projections with declared carrier', 'main_subject.declared_horn_carrier',
    '머리 부근에 단단한 뿔형 돌출물이 있다;돌출물의 뿌리가 지정한 carrier에 이어진다',
    'rigid horn-like projections rise near the head;each projection root joins its declared carrier',
    [('horn projection root', 'connected_to', 'declared carrier')],
    'C022 C023 C092', 'extend', 'sca_x02 ca_coiled_head_elements', 'wearable_accessory', 'wardrobe.accessories.horn_carrier_topology',
    '아호게;헬멧 뿔을 몸의 뿔로 해석', '형태와 뿌리 carrier를 동시에 확인한다.', '히메·미코토 그림의 뿔 모양은 확인되지만 소재·성장 원인은 확정하지 않는다. helmet ornament와 명시된 nonhuman anatomy는 서로 다른 적용 범위다.')
add(61, 'hardware', '박쥐형 날개', 'external rib-and-membrane costume wings', 'main_subject.external_wing_accessory',
    '가는 날개 골격 사이에 막 표면이 이어진다;오목한 구간이 바깥 날개 끝들 사이에 반복된다',
    'membrane surfaces span between slender wing ribs;concave edge segments repeat between outer wing tips',
    [('membrane', 'spans_between', 'wing ribs'), ('wing accessory', 'attached_to', 'declared external back support')],
    'C090', 'new', 'ca_membrane_wings', 'wearable_accessory', 'wardrobe.accessories.membrane_wing_topology',
    '새의 깃털 날개;등 뒤의 배경 장식', '골격·막·오목한 가장자리·선택한 외부 부착을 확인한다.', 'ca_membrane_wings의 creature ownership을 인간 코스튬에 자동 전이하지 않는다. 堕悪天使 모듈명만으로 날개를 추가하지 않는다.', 'P0')
add(62, 'hardware', '요정형 날개', 'external thin patterned wing plates', 'main_subject.external_wing_accessory',
    '등 뒤에 별도 얇은 날개 판들이 있다;판의 외곽 안에 선무늬가 있고 선택한 투과가 보인다',
    'separate thin wing plates lie behind the back;line motifs remain inside the plate outlines with the requested light transmission',
    [('line motif', 'lies_within', 'thin wing plate'), ('wing plates', 'behind', 'same wearer back')],
    'C086', 'new', '', 'wearable_accessory', 'wardrobe.accessories.thin_wing_plate_topology',
    '생물학적 날개 관절;배경 회로 그림', '얇은 판·내부 선·겹침/투과·외부 부착 관계를 확인한다.', '2017 피규어에서 투명 판을 확인했다. 회로처럼 보이는 인쇄는 작동 회로나 발광을 뜻하지 않는다.', 'P0')
add(63, 'hardware', '해파리 모티프', 'canopy and dependent streamer motif', 'declared_canopy_prop_and_garment_parts',
    '반구 또는 원형 우산형 구조가 위쪽에 있다;지정한 띠형 부속이 그 아래로 길게 이어진다',
    'a dome or circular canopy occupies an upper region;declared narrow streamers extend below that canopy',
    [('streamers', 'below', 'declared canopy')],
    'C034', 'new', 'ca_ribbon_body_appendages', 'prop', 'prop.canopy_streamer_layout',
    '생물의 실제 촉수;소매 띠를 등 장치의 촉수로 합침', '우산형 구조·띠 위치·각 부속의 carrier를 별도로 확인한다.', 'LUMi 패키지에서 뒤쪽 원형 canopy와 소매에서 이어진 띠가 보인다. 전부 하나의 부품이라는 연결은 확정하지 않는다. ca_ribbon_body_appendages는 creature owner다.', 'P2')
add(64, 'hardware', '동물형 모자', 'animal-face cap carrier', 'main_subject.wardrobe.cap',
    '머리 위 모자의 몸체와 테두리가 구분된다;그 모자 안에 눈·입 도상과 선택한 돌출 부속이 있다',
    'a cap crown and edge remain distinct above the head;eye or mouth motifs and selected projections belong to that cap',
    [('animal-face motifs', 'on', 'cap crown')],
    'C009 C056 C057', 'extend', 'ca_cap_projections', 'wearable_accessory', 'wardrobe.accessories.cap_face_motif',
    '캐릭터 얼굴 자체를 동물로 바꿈;모자 옆의 별도 봉제인형', '모자 carrier·얼굴 도상·선택한 부속의 귀속을 확인한다.', 'Una Sugar/Spicy의 색과 부속 구성을 섞지 않는다. 장어형 모자를 일반 cat ear 두 개로 치환하지 않는다.')
add(65, 'hardware', '붕대', 'overlapping cloth wrap on a declared region', 'main_subject.declared_wrapped_region',
    '폭이 일정한 천 띠가 지정한 부위를 감싼다;감긴 띠의 가장자리가 서로 겹친다',
    'a consistently wide cloth strip wraps a declared body region;successive strip edges visibly overlap',
    [('overlapping cloth turns', 'surround', 'same declared region')],
    'C048 X005', 'new', 'ca_lower_face_wrap y2kr_bandage', 'wearable_accessory', 'wardrobe.wrap.region_overlap',
    '밴디지 드레스의 수평 패널;얼굴에 인쇄한 흰 선', '천 폭·겹침·부위 둘레 경로를 확인한다.', 'OLIVER 공식 썸네일은 한쪽 눈 주변의 흰 덮임만 확인된다. 전신/팔 붕대와 질병·부상 원인은 확정하지 않는다. 기존 mouth wrap의 위치를 눈으로 자동 확대하지 않는다.')
add(66, 'hardware', '패치워크', 'joined textile patch panels', 'main_subject.wardrobe.surface',
    '색 또는 무늬가 다른 천 조각의 경계가 있다;인접 조각들이 봉제 경계로 이어진다',
    'textile pieces differ in color or pattern;sewn boundaries join adjacent pieces',
    [('patch panel', 'sewn_to', 'adjacent textile panel')],
    'C032 C098', 'reuse', 'sca_x12', 'garment_detail', 'wardrobe.surface.patch_panel_seams',
    '패치워크처럼 인쇄한 구획;피부의 색 반점', '두 조각·접합 경계·같은 의복 carrier를 확인한다.', '색 경계가 보인다는 사실과 실제 봉제 구조의 증거를 분리한다.')
add(67, 'hardware', '노출 봉제선', 'visible seam stitch rhythm', 'main_subject.wardrobe.seam',
    '두 천 패널 사이의 접합 경계가 보인다;그 경계 위에 반복된 실 선 또는 교차가 있다',
    'a joint boundary separates two textile panels;repeated thread strokes or crossings lie along that boundary',
    [('visible stitch rhythm', 'along', 'same panel joint')],
    'C032 C026', 'extend', 'sca_x12 clothing_ct097_v1', 'garment_detail', 'wardrobe.seam.visible_stitch_rhythm',
    '그래픽 점선;천 위의 자수 무늬', '패널 접합·실 반복·표면 두께 또는 관통 증거를 확인한다.', 'Fukase의 선 표현만으로 실제 실 섬유를 확정하지 않는다. seam joint, embroidery, quilting의 역할을 분리한다.')
add(68, 'hardware', '의료 모자', 'small cap with bounded cross motif', 'main_subject.wardrobe.cap',
    '작은 모자가 머리 위에 별도 테두리를 가진다;모자 앞면 안에 십자 도상이 놓인다',
    'a small cap has a separate edge above the head;a bounded cross glyph lies on its front panel',
    [('cross glyph', 'on', 'same cap front')],
    'C037 C091', 'new', 'ca_cap_projections', 'wearable_accessory', 'wardrobe.accessories.cap_cross_motif',
    '배경의 의료 표지;실제 의료인 자격으로 해석', '모자·앞면·십자 도상의 귀속을 확인한다.', 'NurseRobot의 도상은 주황색이다. 흰 모자/빨간 십자를 보편 기본값으로 강제하지 않는다. 이름만으로 노출된 기계 관절을 추가하지 않는다.', 'P0')
add(69, 'hardware', '여우 가면', 'fox-form mask with independent placement', 'main_subject.wardrobe.mask_or_selected_prop',
    '가면 외곽에 선택한 뾰족 귀와 주둥이 형태가 있다;선택한 눈·볼 문양이 그 얼굴판 안에 놓인다',
    'the mask silhouette includes selected pointed ears and muzzle form;selected eye or cheek motifs remain within that face plate',
    [('mask motifs', 'on', 'same mask face plate'), ('mask', 'at', 'declared face or offset head location')],
    'C096 C097 C102', 'extend', 'ca_animal_head_mask ca_projecting_face_mask ca_offset_head_mask', 'wearable_accessory', 'wardrobe.accessories.mask_shape_and_position',
    '사람 얼굴의 동물화;머리 옆 가면을 얼굴 전체에 씌움', '가면 형태·문양·요청 위치와 얼굴의 가림 상태를 확인한다.', 'S096에서 가면은 머리 옆에 비껴 있으며 얼굴을 모두 가리지 않는다. 흰 바탕·붉은 문양도 해당 판본의 선택 속성이다.', 'P0')
add(70, 'hardware', '봉제인형', 'soft sewn plush prop', 'selected_prop',
    '부드러운 볼륨의 천 부품들이 이음선으로 이어진다;선택한 단추 또는 실 얼굴 부속이 같은 천 몸체에 붙는다',
    'soft volumetric textile parts join through seams;selected button or stitched face elements attach to the same cloth body',
    [('plush parts', 'sewn_to', 'same textile body')],
    'C026', 'new', '', 'prop', 'prop.plush.sewn_surface_topology',
    '살아 있는 동물;인간의 외형을 봉제인형으로 변경', '천 부피·이음선·선택한 부속의 귀속을 확인한다.', 'MAYU가 든 소품과 MAYU 자체의 owner를 분리한다. 버튼 눈 두 개·긴 귀·찢김은 선택한 경우만 채택하며 현재 prop scope는 자동 채택할 수 없다.', 'P2')
add(71, 'hardware', '갑주형 장식', 'localized overlapping rigid costume plates', 'main_subject.wardrobe.rigid_panels',
    '어깨·팔·허리의 지정 부위에 두께 있는 단단한 판이 있다;판 경계가 겹치되 움직이는 관절을 통째로 합치지 않는다',
    'thick rigid plates occupy a declared shoulder arm or waist region;plate edges overlap without fusing across a moving joint',
    [('rigid plate edges', 'overlap_on', 'declared garment region')],
    'C008 C037', 'extend', 'costume_ccx_cc13_01 costume_ccx_cc13_02', 'garment_detail', 'wardrobe.rigid_panels.local_overlap',
    '금속색 인쇄;전신 갑옷이나 로봇 신체로 확대', '판 두께·겹침·지정 부착 부위를 확인한다.', '상품 배너가 어깨만 보여주면 전신 갑주·허리 장비·무기까지 확정하지 않는다.')
add(72, 'hardware', '의장용 창 같은 소품', 'long shaft and pointed terminal silhouette', 'selected_prop',
    '긴 직선 자루가 있다;그 끝에 좁고 뾰족한 외곽이 이어진다',
    'a long straight shaft is visible;a narrow pointed terminal silhouette joins one shaft end',
    [('pointed terminal', 'connected_to', 'same long shaft')],
    'C085', 'boundary', '', 'prop', 'prop.long_shaft.pointed_terminal',
    '접힌 우산을 실제 창으로 분류;의장용이라는 기능·서사 추가', '자루-끝 형태의 연결만 판정하고 소품 종류는 일차 자료 명칭과 대조한다.', '2015 참조는 피규어의 우산 계열 소품이다. 창 같은 형태 비유를 실제 무기 정체성으로 활성화하지 않는다.', 'P2')

assert len(cards) == 72 and len({x['id'] for x in cards}) == 72
next(x for x in cards if x['id'] == 'K39')['definition_support_sources'] = [
    {'url': 'https://www.pnb.org/blog/wardrobe-types-of-tutus/',
     'purpose': 'Primary ballet-company wardrobe reference distinguishes long Romantic and several short Classical tutu structures.'}]
next(x for x in cards if x['id'] == 'K72')['definition_support_sources'] = [
    {'url': 'https://www.goodsmile.com/en/product/2739/Nendoroid%2BRacing%2BMiku%2B2015%2BVer.',
     'purpose': 'Official figure description identifies the accessory as a parasol.'}]
doc = {
    'schema_version': 'vocaloid-keyword-research/v1', 'runtime_artifact': False,
    'date': '2026-10-04', 'reference_conversation_id': receipts['reference_conversation_id'],
    'reference_term_count': 72, 'decision_counts': dict(Counter(x['authoring_decision'] for x in cards)),
    'contract': {
        'status': 'authored research proposals, not a runtime registry extension',
        'decision_meanings': {
            'reuse': '기존 구조 정의 재사용; add retrieval wording only when holdouts reveal a gap',
            'extend': 'Add owner, variant or component detail while preserving existing profile scope; may become a sibling after deduplication',
            'new': 'A distinct observable relation needs an authored profile or candidate; source qualification remains separate',
            'boundary': 'Preserve age, medium, owner or object-identity boundary before enabling the term',
        },
        'adoption': 'Exact contextual definitions may qualify after core checks; BM25F and embedding matches stay optional until explicit selection',
        'evidence': 'All requested components and relations must coexist on the declared owner; partial evidence fails; occluded required evidence is UNOBSERVABLE',
        'independence': 'Hair shape, color, attachment, material, coverage, pose, body geometry and representation are independent selected properties',
        'forbidden_inference': ['name-to-whole-character appearance', 'age from proportions', 'injury from red marks or wraps', 'robot joints from product narrative', 'sound or power from printed motifs', 'flight from a single-view visible gap'],
        'prop_scope': 'The current prop slot has no automatic affected dimension. Independent prop cards are advisory research until an actual requester-owned effect scope is established.',
    },
    'cards': cards,
}
(ROOT / 'KEYWORD-RESEARCH.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')

titles = {'hair_face': '머리와 얼굴 17개', 'body': '신체·비율 9개', 'garment': '의복 24개', 'hardware': '장치·장식·소품 22개'}
decisions = {'reuse': '재사용', 'extend': '보강/변형', 'new': '새 구조', 'boundary': '경계 우선'}
lines = ['# 보컬로이드 외형 키워드 72개 연구 카드', '',
         '2026-10-04. 원 대화의 용어 전부를 현재 데이터와 대조했다. 아래는 연구 제안이며 runtime 데이터나 이미지 합격 기록이 아니다.', '',
         '기본 색·길이·재질·노출·연령·매체를 키워드에 일괄 묶지 않는다. `새 구조` 수는 추가할 프로파일 개수와 같지 않다. 세부 카드의 출처는 예시/검증 후보이며 모든 구성요소를 이미 입증했다는 뜻이 아니다.', '',
         '|ID|원문 용어|처리|주요 기존 프로파일|', '|---|---|---|---|']
for x in cards:
    lines.append(f"|[{x['id']}](#{x['id'].lower()})|{x['reference_term']}|{decisions[x['authoring_decision']]}|{' · '.join(p['profile_id'] for p in x['existing_profile_crosswalk']) or '없음'}|")
for group, title in titles.items():
    lines.extend(['', f'## {title}', ''])
    for x in (x for x in cards if x['group'] == group):
        lines.extend([f"### {x['id']}: {x['reference_term']}", '',
                      f"<a id=\"{x['id'].lower()}\"></a>", '',
                      f"**소유자:** `{x['owner']}`. **처리:** {decisions[x['authoring_decision']]} ({x['priority']}).", '',
                      '**보여야 할 구성요소:** ' + ' / '.join(y['ko'] for y in x['visible_components']) + '.', '',
                      '**필수 관계:** ' + '; '.join(f"{r['subject']} → {r['type']} → {r['object']}" for r in x['required_relations']) + '.', '',
                      '**혼동 경계:** ' + ' / '.join(x['confusion_boundaries']) + '.', '',
                      '**현재 데이터:** ' + (' / '.join(f"`{p['profile_id']}` ({p['file']})" for p in x['existing_profile_crosswalk']) or '직접 대응 프로파일 없음') + '.', '',
                      f"**후보 제안:** `{x['proposed_slot']}` → `{x['proposed_effect']['property']}`. 독립 소품의 dimension은 미해결 상태로 유지한다." if x['proposed_slot'] == 'prop' else f"**후보 제안:** `{x['proposed_slot']}` → `{x['proposed_effect']['dimension']}` / `{x['proposed_effect']['target']}` / `{x['proposed_effect']['property']}`.", '',
                      '**원본 픽셀 게이트:** ' + x['render_gate_proposal']['description_ko'] + ' 가려진 필수 관계는 `UNOBSERVABLE`; 일부만 만족하면 `FAIL`.', '',
                      '**범위·추가 확인:** ' + (x['limits'] or '사용자가 선택한 구성과 실제 보이는 부위만 적용한다.') , '',
                      '**일차 자료/예시:** ' + ', '.join(f"[{s['case_id'] or s['source_id']}]({s['url']})" for s in x['source_examples']) + '.', ''])
        if x.get('definition_support_sources'):
            lines.extend(['**추가 일차 정의 자료:** ' + ', '.join(
                f"[{s['purpose']}]({s['url']})" for s in x['definition_support_sources']) + '.', ''])
(ROOT / 'KEYWORD-RESEARCH.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'cards': len(cards), 'decisions': doc['decision_counts'],
                  'groups': dict(Counter(x['group'] for x in cards))}, ensure_ascii=False))
