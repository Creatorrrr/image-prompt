"""Advisory natural-query/source-fact alignment for H-F2.

This lane is deliberately separate from BM25F and cosine. It recognizes a
small, generic set of photographic owner/relation requests, then ranks only on
direct selected-RID primary text and its effect footprint. It never filters a
candidate, supplies a missing query fact, or treats an interrogative as an
affirmative constraint.
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

try:
    from photo_h_f2_single_property import query_recognizer as _single_property_query
    from photo_h_f2_single_property import source_witness as _single_property_source_witness
except ModuleNotFoundError as error:
    if error.name != 'photo_h_f2_single_property':
        raise
    _single_property_path = Path(__file__).with_name('photo_h_f2_single_property.py')
    _single_property_spec = importlib.util.spec_from_file_location(
        'photo_h_f2_single_property', _single_property_path)
    _single_property_module = importlib.util.module_from_spec(_single_property_spec)
    sys.modules[_single_property_spec.name] = _single_property_module
    _single_property_spec.loader.exec_module(_single_property_module)
    _single_property_query = _single_property_module.query_recognizer
    _single_property_source_witness = _single_property_module.source_witness

def _load_sibling(module_name):
    try:
        return __import__(module_name)
    except ModuleNotFoundError as error:
        if error.name != module_name:
            raise
        spec = importlib.util.spec_from_file_location(module_name, Path(__file__).with_name(module_name + '.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(spec.name, None)
            raise
        return module

_property_answers = _load_sibling('photo_h_f2_property_answers')
_pose_answers = _load_sibling('photo_h_f2_pose_answers')

RECIPE = 'photo-h-f2-natural-source-relevance/v8'
SCORING_POLICY = 'rrf10_owner_paired_source_and_scoped_primary_witness_partitions_v2'
PROPERTY_ANSWER_RECIPE = 'photo-h-f2-property-answer/v1'
PROPERTY_ANSWER_ORDERING_POLICY = 'stable-positive-complete-same-primary-partition'
DEFAULT_RELATION_LANE_WEIGHT = 1.00
ATTRIBUTE_LANE_WEIGHT = 0.20
SINGLE_PROPERTY_ORDERING_POLICY = 'stable_positive_primary_witness_before_current_order'


def _rx(value):
    return re.compile(value, re.I | re.U)


# Query patterns identify requested properties. Source patterns allow ordinary
# paraphrases of those properties, while the property patterns recognize the
# authored owner/property path. A path never supplies a positive witness alone:
# at least one direct primary field must also support the relation.
_RULES = [
    {'id': 'weight_distribution',
     'query': r'\b(?:weight|load|weight-bearing)\b|체중|무게|하중|체중.{0,12}(?:실리|두)|(?:실리|딛).{0,12}(?:체중|무게)',
     'source': r'\b(?:weight|load|weighted|weight-bearing|rests? (?:most of )?(?:her )?weight|planted leg)\b|체중|무게|하중|체중.{0,12}(?:실리|두)|(?:실리|딛).{0,12}(?:체중|무게)',
     'property': r'(?:^|[._])weight(?:[._]|$)|body\.support\.weight|weight\.distribution',
     'owners': {'person', 'leg'}, 'owner_mode': 'any'},
    {'id': 'knee_state',
     'query': r'\bknees?\b|무릎',
     'source': r'\bknees?\b|무릎',
     'property': r'knee|legs?\.position',
     'owners': {'person', 'leg'}, 'owner_mode': 'any'},
    {'id': 'ankle_state',
     'query': r'\bankles?\b|발목',
     'source': r'\bankles?\b|발목',
     'property': r'ankle|legs?\.crossed_at_ankles',
     'owners': {'person', 'leg'}, 'owner_mode': 'any'},
    {'id': 'finger_pointing',
     'query': r'\b(?:point(?:s|ed|ing)?|indicat(?:e|es|ed|ing))\b|가리키',
     'source': r'\b(?:point(?:s|ed|ing)?|pointing finger|finger points?)\b|손가락.{0,14}가리키|검지.{0,14}가리키|가리키.{0,14}(?:손가락|검지)',
     'property': r'index_finger|finger.*point|point.*finger',
     'owners': {'person', 'hand', 'arm'}, 'owner_mode': 'any'},
    {'id': 'gaze_direction',
     'query': r'\b(?:look(?:s|ing)?\s+(?:at|toward|towards|away from|into)\b|gaze\b|eye contact\b|where\b.{0,32}\blook(?:s|ing)?\b|eyes?\s+(?:land|meet|turn toward))|시선|바라보|눈길|눈.{0,12}(?:향|두)',
     'source': r'\b(?:look(?:s|ed|ing)?\s+(?:at\s+(?:the\s+)?(?:camera|lens)|toward\w*|away\w*|into\s+(?:the\s+)?(?:camera|lens))|gaze\s+(?:toward|towards|away|at)|eyes?\s+(?:go|turn|face|meet)\s+(?:toward|the\s+camera|the\s+lens)|eye contact)\b|시선.{0,14}(?:카메라|렌즈|향하|벗어나|외면)|카메라.{0,12}바라보|렌즈.{0,12}바라보',
     'property': r'eyes?\.gaze|gaze\.',
     'owners': {'person', 'eyes', 'head'}, 'owner_mode': 'any'},
    {'id': 'body_orientation',
     'query': r'\b(?:turn(?:ed|s|ing)?|fac(?:e|es|ed|ing)|orientation|profile|back toward|rear three[- ]quarter)\b|몸.{0,16}(?:돌|향)|등.{0,10}카메라|옆모습|후면',
     'source': r'\b(?:turn(?:ed|s|ing)?|fac(?:e|es|ed|ing)|orientation|profile|back (?:mostly )?(?:toward|to)|rear three[- ]quarter|away from the camera)\b|몸.{0,16}(?:돌|향)|등.{0,10}카메라|옆모습|후면',
     'property': r'body\.orientation|face\.orientation|camera\.viewpoint',
     'owners': {'person', 'body', 'torso'}, 'owner_mode': 'any'},
    {'id': 'head_orientation',
     'query': r'\bhead\b.{0,24}\b(?:turn|direction|face|point|orient)\w*|\b(?:turn|direction|face|orient)\w*.{0,24}\bhead\b|머리.{0,18}(?:돌|향|방향)',
     'source': r'\bhead\b.{0,36}\b(?:turn|direction|face|point|orient|lift)\w*|\b(?:turn|direction|face|orient|lift)\w*.{0,36}\bhead\b|머리.{0,18}(?:돌|향|방향)',
     'property': r'head\.orientation|head\.direction',
     'owners': {'person', 'head'}, 'owner_mode': 'any'},
    {'id': 'posture',
     'query': r'\b(?:sit(?:s|ting)?|seated|stand(?:s|ing)?|posture|pose)\b|앉|서\s*(?:있|자세|있는)',
     'source': r'\b(?:sit(?:s|ting)?|seated|stand(?:s|ing)?|posture|pose)\b|앉|서\s*(?:있|자세|있는)',
     'property': r'body\.posture|pose\.posture|posture\.',
     'owners': {'person', 'body', 'leg'}, 'owner_mode': 'any'},
    {'id': 'arms_position',
     'query': r'\barms?\b|\bcross(?:ed|ing)?\b|팔.{0,24}(?:모으|교차|잡|들|어떻게)',
     'source': r'\barms?\b|\bcross(?:ed|ing)?\b|\b(?:hold|grip|raise|hang)(?:s|ed|ing)? (?:her |the )?arms?\b|팔.{0,32}(?:모으|교차|잡|들|늘어|벌리)',
     'property': r'arms?\.|arm\.position|arm\.action',
     'owners': {'person', 'arm', 'hand'}, 'owner_mode': 'any',
     'value_patterns': {'bilateral': r'\b(?:both arms|two arms|each arm|arms? on both sides)\b|양팔|양쪽\s*팔'}},
    {'id': 'camera_crop',
     'query': r'\b(?:crop(?:ped|ping)?|tight(?:ly)?|cut(?:ting)?|close[- ]?up|framing)\b|타이트|잘리|크롭|클로즈업|가슴.{0,8}위|허리.{0,8}위',
     'source': r'\b(?:crop(?:ped|ping)?|tight(?:ly)?|close[- ]?up|upper[- ]chest|chest upward|waist upward|framing|frame(?:s|d)? from)\b|타이트|잘리|크롭|클로즈업|가슴.{0,8}위|허리.{0,8}위',
     'property': r'framing\.crop|crop_extent',
     'owners': {'person', 'frame', 'camera'}, 'owner_mode': 'any'},
    {'id': 'camera_height',
     'query': r'\b(?:camera height|camera angle|viewpoint|eye[- ]level|high[- ]angle|low[- ]angle|shot from|from where.{0,48}shot)\b|카메라.{0,14}(?:높이|각도|시점)|눈높이|앵글|시점|어디에서.{0,18}(?:촬영|올려다|내려다)',
     'source': r'\b(?:camera height|camera angle|eye[- ]level|high[- ]angle|low[- ]angle|overhead shot|shot from above|shot from below|camera positioned|camera placed|photographed from above|photographed from below|elevated camera)\b|카메라.{0,14}(?:높이|각도|시점)|눈높이|앵글|카메라.{0,12}(?:위|아래).{0,10}(?:촬영|바라)',
     'property': r'camera\.(?:height|viewpoint|angle)|height_relation',
     'owners': {'camera', 'person', 'stairs'}, 'owner_mode': 'any'},
    {'id': 'focal_length',
     'query': r'\b(?:lens|focal length|wide[- ]angle|\d+(?:[.–-]\d+)?\s*mm)\b|렌즈|초점거리|화각',
     'source': r'\b(?:focal length|wide[- ]angle|\d+(?:[.–-]\d+)?\s*mm)\b|초점거리|화각|렌즈.{0,16}(?:85|100|135|200)\s*mm',
     'property': r'camera\.focal_length|focal_length|camera\.lens',
     'owners': {'camera'}, 'owner_mode': 'any'},
    {'id': 'subject_placement',
     'query': r'\b(?:placement|position|placed|where.{0,32}(?:model|woman|person).{0,20}frame|frame.{0,18}(?:left|right|center))\b|프레임.{0,14}(?:어디|왼|오른|중앙)|어디에.{0,14}(?:두|배치)|배치|위치',
     'source': r'\b(?:placement|position|placed|frame[- ]left|frame[- ]right|left third|right third|center(?:ed|ed)?|off[- ]center)\b|프레임.{0,14}(?:왼|오른|중앙)|배치|위치',
     'property': r'layout\.subject_position|subject\.position|frame_position',
     'owners': {'person', 'frame'}, 'owner_mode': 'any'},
    {'id': 'negative_space',
     'query': r'\b(?:negative space|open space|empty|open|leave.{0,24}(?:space|open)|space.{0,16}left)\b|여백|비우|빈\s*공간|공간.{0,8}(?:남기|비우)',
     'source': r'\b(?:negative space|open space|empty|open sky|open field|space.{0,16}(?:left|around)|leave.{0,24}(?:space|open)|uninterrupted)\b|여백|비우|빈\s*공간|공간.{0,8}(?:남기|비우)',
     'property': r'negative_space|layout\.negative_space',
     'owners': {'frame', 'environment', 'person'}, 'owner_mode': 'any'},
    {'id': 'stair_direction',
     'query': r'\b(?:leading lines?|steps?\s+(?:rise|descend|lead)|stairs?\s+(?:lead|run|rise|descend|direction)|direction.{0,32}(?:staircase|stairs?|steps?)|(?:staircase|stairs?|steps?).{0,32}(?:direction|lead|rise|descend|run through))\b|계단.{0,24}(?:방향|이어|가로지르|대각선)|선.{0,16}(?:방향|가로)|가로질러',
     'source': r'\b(?:leading lines?|steps?\s+(?:rise|descend|lead)|stairs?\s+(?:lead|run|rise|descend)|staircase.{0,28}(?:rise|descend|lead|diagonal)|diagonal lines?|run through the frame|edge[- ]to[- ]edge)\b|계단.{0,24}(?:이어|가로지르|대각선)|선.{0,16}(?:방향|가로)|가로질러|대각선.{0,12}선',
     'property': r'leading_lines|stair|step|diagonal.*(?:line|composition)',
     'owners': {'stairs', 'frame'}, 'owner_mode': 'any'},
    {'id': 'reflection_identity',
     'query': r'\b(?:mirror|reflection|glass|selfie|own|herself|second person|same person)\b|거울|유리|반사|셀카|본인|자신|거울상|비친',
     'source': r'\b(?:mirror|reflection|glass|selfie|photographs? (?:herself|oneself)|same subject|same person|second person|in the mirror)\b|거울|유리|반사|셀카|본인|자신|거울상|비친',
     'property': r'reflection\.logic|same_subject|photographs_self|mirror.*(?:identity|reflection)',
     'owners': {'person', 'mirror', 'accessory'}, 'owner_mode': 'any',
     'value_patterns': {'same_subject': r'\b(?:same (?:person|subject|woman|man)|photographs? (?:herself|oneself)|selfie|own reflection)\b|같은\s*(?:사람|인물)|본인|자신',
                        'different_subject': r'\b(?:second person|someone else|other person|different (?:person|subject))\b|다른\s*(?:사람|인물)'}},
    {'id': 'frame_occupancy',
     'query': r'\b(?:occup\w*|how much.{0,28}(?:frame|image|area)|amount.{0,20}(?:frame|space)|percent(?:age)?|frame area|takes? up.{0,30}(?:frame|image)|area.{0,18}(?:occup|frame)|\d+(?:[.–-]\d+)?\s*%)\b|차지|면적|비율|퍼센트|프레임.{0,12}얼마나|얼마나.{0,12}(?:차지|면적|비율)',
     'source': r'\b(?:occup\w*|percent(?:age)?|frame area|takes? up.{0,30}(?:frame|image)|dominates? the frame|\d+(?:[.–-]\d+)?\s*%)\b|차지|면적|비율|퍼센트',
     'property': r'frame_occupancy|subject_occupancy|occupancy|percent',
     'owners': {'person', 'hand', 'frame'}, 'owner_mode': 'any'},
    {'id': 'tilt_or_roll',
     'query': r'\b(?:tilt(?:ed|ing)?|roll|horizon|frame itself|head tilt)\b|기울|수평선|머리.{0,12}기울',
     'source': r'\b(?:tilt(?:ed|ing)?|roll|horizon|canted|dutch angle|head.{0,24}tilt|frame.{0,24}tilt)\b|기울|수평선|머리.{0,12}기울',
     'property': r'camera\.roll|tilted_horizon|frame_rotation|head\.orientation.*tilt|head.*tilt',
     'owners': {'frame', 'camera', 'head'}, 'owner_mode': 'any'},
    {'id': 'focus_plane',
     'query': r'\b(?:focus|sharp|crisp|blur(?:red|ry)?|soft|out of focus)\b|초점|선명|흐리|흐릿',
     'source': r'\b(?:focus|sharp|crisp|blur(?:red|ry)?|soft|out of focus|clear focus)\b|초점|선명|흐리|흐릿',
     'property': r'focus\.|focus_plane',
     'owners': {'person', 'eyes', 'head', 'hand', 'leg', 'environment', 'frame'}, 'owner_mode': 'any',
     'value_patterns': {'sharp': r'\b(?:sharp|crisp|in focus|clear focus)\b|선명',
                        'soft': r'\b(?:blur(?:red|ry)?|soft|out of focus|soft focus)\b|흐리|흐릿'}},
    {'id': 'composition_layout',
     'query': r'\b(?:arrang\w*|composition|layout|still life|within the frame|frame arrangement|balanced?)\b|정물|배치|구도|균형|간격',
     'source': r'\b(?:arrang\w*|composition|layout|centered|centred|balanced?|spacing|symmetry|negative space|diagonal composition)\b|배치|구도|균형|간격|중앙.{0,12}구도',
     'property': r'layout\.|composition\.|scene\.arrangement|spacing|symmetry',
     'owners': {'frame', 'environment'}, 'owner_mode': 'any'},
    {'id': 'doorway_framing',
     'query': r'\b(?:doorway|door frame|frame the person|frame-within-frame)\b|문틀|문간|감싸|문.{0,8}틀',
     'source': r'\b(?:doorway|door frame|frame-within-frame|framed between|framed by the door)\b|문틀|문간|감싸|문.{0,8}틀',
     'property': r'frame_within_frame|doorway',
     'owners': {'doorway', 'person', 'frame'}, 'owner_mode': 'any'},
    {'id': 'background_visibility',
     'query': r'\b(?:beyond|behind|visible|what can be seen|background)\b|뒤쪽|너머|배경|(?:무엇|어떤).{0,12}보이',
     'source': r'\b(?:beyond|behind|visible|see(?:n)?|background|landscape|beach|field|horizon|sky|opens? onto)\b|뒤쪽|너머|보이|배경|풍경|해변|들판|수평선|하늘',
     'property': r'spatial\.depth_layers|background_context|spatial\.background|scene\.setting|spatial\.background_context',
     'owners': {'environment', 'person', 'doorway', 'frame'}, 'owner_mode': 'any'},
    {'id': 'wear_or_hold',
     'query': r'\b(?:wear(?:s|ing)?|worn|hold(?:s|ing)?|held|carry(?:ing)?|glasses|eyewear)\b|쓰고|착용|들고|쥐고|안경',
     'source': r'\b(?:wear(?:s|ing)?|worn|hold(?:s|ing)?|held|carry(?:ing)?|glasses|eyewear)\b|쓰고|착용|들고|쥐고|안경',
     'property': r'wardrobe\.|wear|grip|hold|hand\.action',
     'owners': {'person', 'garment', 'accessory', 'eyewear', 'phone', 'bag', 'hand'}, 'owner_mode': 'any',
     'value_patterns': {'worn': r'\b(?:wear(?:s|ing)?|worn)\b|착용|쓰고',
                        'held': r'\b(?:hold(?:s|ing)?|held|carry(?:ing)?)\b|들고|쥐고'}},
]

# Conservative token-root cues supplement exact phrase patterns. They are used
# only inside this advisory source lane; sealed BM25 tokens and query bytes stay
# unchanged.
_ROOT_CUES = {
    'weight_distribution': {'weight', 'load', '체중', '무게', '하중', '실리', '딛'},
    'knee_state': {'knee', '무릎'},
    'ankle_state': {'ankle', '발목'},
    'finger_pointing': {'point', '가리키'},
    'gaze_direction': {'gaze', '시선', '바라보', '눈길'},
    'body_orientation': {'turn', 'face', 'orientation', 'back', 'profile', '돌아', '향하', '등'},
    'head_orientation': {'turn', 'direction', 'face', 'orient', '향하', '돌리'},
    'posture': {'sit', 'stand', 'posture', 'pose', '앉', '서'},
    'arms_position': {'cross', 'hold', 'raise', 'hang', '팔', '교차', '모으'},
    'camera_crop': {'crop', 'tight', 'close', 'framing', '타이트', '잘리', '크롭', '클로즈업'},
    'camera_height': {'height', 'angle', 'level', 'shot', '높이', '각도', '시점', '눈높이'},
    'focal_length': {'focal', 'mm', '초점거리', '화각'},
    'subject_placement': {'placement', 'position', 'place', '배치', '위치'},
    'negative_space': {'space', 'empty', 'open', '여백', '비우', '빈'},
    'stair_direction': set(),
    'reflection_identity': {'mirror', 'reflection', 'glass', 'selfie', 'own', '거울', '유리', '반사', '셀카', '본인', '자신', '비치'},
    'frame_occupancy': {'occupy', 'percent', 'area', '차지', '면적', '비율'},
    'tilt_or_roll': {'tilt', 'roll', 'horizon', '기울', '수평선'},
    'focus_plane': {'focus', 'sharp', 'crisp', 'blur', 'soft', '초점', '선명', '흐리', '흐릿'},
    'composition_layout': {'arrange', 'composition', 'layout', 'balance', 'spacing', '배치', '구도', '균형', '간격'},
    'doorway_framing': {'doorway', 'door', 'frame', '문틀', '문간', '감싸'},
    'background_visibility': {'beyond', 'behind', 'visible', 'background', '뒤쪽', '너머', '배경'},
    'wear_or_hold': {'wear', 'hold', 'carry', 'glasses', 'eyewear', '착용', '쓰', '들', '안경'},
}

_ROOT_REQUIREMENTS = {
    'finger_pointing': ({'point', '가리키'}, {'hand'}),
    'body_orientation': ({'turn', 'face', 'orientation', 'back', 'profile', '돌아', '향하', '등'},
                         {'person', 'body', 'camera'}),
    'head_orientation': ({'turn', 'direction', 'face', 'orient', '향하', '돌리'}, {'head'}),
    'arms_position': ({'cross', 'hold', 'raise', 'hang', '교차', '모으'}, {'arm'}),
    'camera_height': ({'height', 'angle', 'viewpoint', 'level', '높이', '각도', '시점'},
                      {'camera', 'stairs'}),
    'subject_placement': ({'placement', 'position', 'place', '배치', '위치'}, {'person', 'frame'}),
    'stair_direction': ({'stair', 'step', '계단'}, {'direction', 'line', 'lead', '가로지르'}),
    'frame_occupancy': ({'occupy', 'percent', 'area', '차지', '면적', '비율'}, {'hand', 'frame', 'person'}),
    'background_visibility': ({'beyond', 'behind', 'visible', 'background', '뒤쪽', '너머', '배경'},
                              {'person', 'environment', 'doorway', 'frame'}),
    'doorway_framing': ({'doorway', 'door', '문틀', '문간', '감싸'}, {'doorway', 'person', 'frame'}),
    'reflection_identity': ({'mirror', 'reflection', 'glass', 'selfie', '거울', '유리', '반사', '셀카'},
                            {'mirror', 'person', 'accessory'}),
}

for _row in _RULES:
    _row['query_rx'] = _rx(_row['query'])
    _row['source_rx'] = _rx(_row['source'])
    _row['property_rx'] = _rx(_row['property'])
    _row['value_rx'] = {k: _rx(v) for k, v in _row.get('value_patterns', {}).items()}

_OWNER_PATTERNS = {
    'person': r'\b(?:woman|women|person|people|subject|model|figure|actor|girl|man|portrait subject|she|he|they|her|him|them)\b|인물|여성|사람|모델|피사체|주인공|여자|남성',
    'camera': r'\b(?:camera|lens|viewpoint|shot|photograph|photographic)\b|카메라|렌즈|촬영|시점',
    'frame': r'\b(?:frame|image|picture|photo|photograph|screen)\b|프레임|화면|사진|이미지',
    'body': r'\b(?:body|torso|back|upper body)\b|몸통|몸|상체|등|허리',
    'head': r'\b(?:head|face)\b|머리|얼굴',
    'eyes': r'\b(?:eyes?|gaze|sightline)\b|눈|시선|눈길',
    'hand': r'\b(?:hands?|fingers?|palms?|thumbs?|index finger)\b|손|손가락|검지|손끝|손바닥',
    'arm': r'\barms?\b|팔|팔뚝',
    'leg': r'\b(?:legs?|knees?|ankles?|feet|foot)\b|다리|무릎|발목|발',
    'environment': r'\b(?:landscape|background|beach|field|shore|wall|room|interior|exterior|sky|horizon|setting)\b|풍경|배경|해변|들판|벽|실내|실외|하늘|수평선|환경',
    'doorway': r'\b(?:doorway|door frame|door|doorframe)\b|문틀|문간|문',
    'stairs': r'\b(?:staircase|stairs?|steps?)\b|계단',
    'mirror': r'\b(?:mirror|glass|reflection|reflective surface)\b|거울|유리|반사|거울상',
    'garment': r'\b(?:clothing|clothes|garment|shirt|coat|dress|skirt|pants|jacket|wardrobe)\b|의복|옷|셔츠|코트|치마|바지|재킷',
    'accessory': r'\b(?:glasses|eyewear|phone|bag|accessory|prop)\b|안경|휴대전화|휴대폰|가방|소품',
    'shirt': r'\b(?:shirt|blouse|top)\b|셔츠|블라우스',
    'jacket': r'\b(?:jacket|blazer)\b|재킷|자켓|블레이저',
    'dress': r'\b(?:dress|gown)\b|드레스|원피스',
    'coat': r'\b(?:coat|overcoat)\b|코트',
    'skirt': r'\bskirt\b|치마|스커트',
    'pants': r'\b(?:pants|trousers|jeans)\b|바지|청바지',
    'sock': r'\b(?:socks?|hosiery)\b|양말|스타킹',
    'boot': r'\b(?:boots?|booties)\b|부츠',
    'footwear': r'\b(?:footwear|shoes?)\b|신발|구두',
    'bandana': r'\bbandanas?\b|반다나',
    'headband': r'\bheadbands?\b|헤어밴드',
    'scarf': r'\bscarves|scarf\b|스카프|목도리',
    'lips': r'\blips?\b|입술|립',
    'blush': r'\b(?:blush|rouge)\b|블러셔|볼터치',
    'brows': r'\b(?:brows?|eyebrows?)\b|눈썹',
    'eyewear': r'\b(?:glasses|eyewear|sunglasses|spectacles)\b|안경|선글라스',
    'phone': r'\b(?:phone|mobile phone|smartphone)\b|휴대전화|휴대폰|스마트폰',
    'bag': r'\b(?:bag|handbag|backpack)\b|가방|핸드백|배낭',
    'ring': r'\b(?:ring|rings)\b|반지',
    'wall': r'\bwall\b|벽',
    'nails': r'\b(?:nails?|fingernails?)\b|손톱|네일',
    'hair': r'\b(?:hair|hairstyle|haircut)\b|머리카락|헤어|머릿결',
}
_OWNER_RX = {key: _rx(value) for key, value in _OWNER_PATTERNS.items()}

_POSTURE_CONTEXT = _rx(
    r'\bin\s+(?:(?:this|the|a|that)\s+)?(?:standing|sitting|seated)\s+(?:pose|position)\b'
    r'|(?:서\s*있는|앉은)\s*(?:자세|포즈)\s*(?:에서|로|의)')

_QUESTION = _rx(r'[?？]|^\s*(?:which|what|who|how|why|where|whether|is|are|does|do|did|can|could|would)\b|^\s*(?:어디|어느|무엇|무슨|어떻게|어떤)\b|(?:인가요|일까요|일까|있나요|있어|인가)\s*[?？]?$')
_IMPERATIVE = _rx(r'^\s*(?:please\s+)?(?:find|show|retrieve|select|return|give|search|look\s+for|choose|identify)\b|^\s*(?:찾아|보여|골라|선택|검색|찾아줘)')
_ALTERNATIVE = _rx(r'\b(?:or|either)\b|아니면|혹은|또는')
_NEGATIVE = _rx(r'\b(?:not|never|without|no longer|doesn.t|isn.t|aren.t|wasn.t|weren.t)\b|않|없|아니')
_POSITIVE_ASSERTION = _rx(r'\b(?:wears?|wearing|holds?|holding|looks? at|faces?|facing|points?|pointing)\b|착용|쓰고|들고|바라보|향한다|가리킨')
_NUMBER = _rx(r'(?<![A-Za-z0-9])\d+(?:\.\d+)?(?:\s*(?:[-–—]|to)\s*\d+(?:\.\d+)?)?\s*(?:mm|cm|m|%|percent|°\s*[CF])?(?![A-Za-z])')
_COLOR_PATTERNS = {
    'black': r'\bblack\b|검은|검정', 'white': r'\bwhite\b|흰|하얀|백색',
    'red': r'\bred\b|빨간|붉은|적색', 'blue': r'\bblue\b|파란|푸른|청색',
    'green': r'\bgreen\b|초록|녹색', 'yellow': r'\byellow\b|노란|황색',
    'purple': r'\bpurple\b|보라|자주', 'pink': r'\bpink\b|분홍',
    'brown': r'\bbrown\b|갈색', 'gray': r'\bgr[ae]y\b|회색',
    'beige': r'\bbeige\b|베이지', 'cream': r'\bcream\b|크림색',
    'ivory': r'\bivory\b|아이보리', 'aqua': r'\baqua\b|아쿠아|청록',
    'gold': r'\bgold(?:en)?\b|금색|황금색', 'silver': r'\bsilver\b|은색',
}
_COLOR_RX = {key: _rx(value) for key, value in _COLOR_PATTERNS.items()}
_NUMBER_UNITS = _rx(r'(?i)(mm|cm|m|%|percent|°\s*[CF])')
_UNMODELED_ATTRIBUTE_CONSTRAINT = _rx(r'\b(?:gloss(?:y)?|matte|sheer|finish|pattern(?:ed)?|paisley|monogram|canvas|lace|striped|plaid|embroidered)\b|광택|매트|무늬|패턴|자수')
_UNQUALIFIED_SOURCE = _rx(r'\b(?:not inferred|cannot be inferred|not specified|not enough information|cannot determine|unclear|unknown|impossible to tell|not resolved)\b|추론할 수 없|명시되지 않|알 수 없|불명확|판단할 수 없')


_posture_rule = next(rule for rule in _RULES if rule['id'] == 'posture')
_posture_rule['value_rx']['floor'] = _rx(r'\b(?:floor|ground)\b|바닥|지면')
_posture_rule['property_rx'] = _rx(_posture_rule['property_rx'].pattern + r'|pose\.body\.seated\.floor|body\.posture\.seated_on_floor')
_knee_rule = next(rule for rule in _RULES if rule['id'] == 'knee_state')
_knee_rule['value_rx']['camera_relative'] = _rx(r'\bknees?\b[\s\S]{0,40}(?:toward(?:s)?\s+(?:the\s+)?(?:camera|lens)|near(?:er)?\s+(?:the\s+)?(?:camera|lens)|foreground)|(?:foreground|(?:toward(?:s)?|near(?:er)?)\s+(?:the\s+)?(?:camera|lens))[\s\S]{0,40}\bknees?\b|무릎.{0,36}(?:렌즈|카메라.{0,8}(?:향|앞|기준)|전경)|(?:렌즈|전경).{0,28}무릎')

def _token_spans(text):
    return [(m.group(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[가-힣]+", text)]


_KO_PARTICLES = tuple(sorted((
    '으로부터', '에게서', '으로써', '으로', '에서', '에게', '한테', '께서', '부터', '까지',
    '처럼', '만큼', '보다', '마다', '조차', '이라도', '라도', '이나', '이랑', '랑', '과', '와',
    '은', '는', '이', '가', '을', '를', '의', '에', '도', '만', '로', '요',
), key=len, reverse=True))
_KO_ENDINGS = tuple(sorted((
    '하면서', '되었고', '되었', '되어', '해서', '하고', '하며', '한다', '하는', '한', '했다', '했',
    '있어서', '있으며', '있고', '있는', '있다', '있어', '있게', '없어서', '없으며', '없고', '없는', '없다',
    '보이고', '보이는', '보인다', '보여서', '보여', '가리키고', '가리키는', '가리킨', '가리켜',
    '바라보고', '바라보는', '바라본', '향하고', '향하는', '향해', '향한다', '돌리고', '돌린', '돌아가',
    '차지하고', '차지하는', '차지해', '비우고', '비우는', '비워', '배치되어', '배치하고', '배치해',
    '기울어진', '기울고', '기울어', '흐려져', '흐려지고', '흐려', '선명하고', '선명한', '흐릿한',
    '올려다보고', '내려다보고', '올려다보', '내려다보', '앉아있는', '앉은', '앉아서', '앉아', '서있는', '서는',
    '잡고', '잡은', '잡아', '들고', '든', '놓고', '놓은', '남기고', '남긴', '남겨', '묻고', '어떻게',
    '고', '며', '면', '서', '게', '다', '어', '아', '여', '니', '야',
), key=len, reverse=True))
_EN_IRREGULAR = {
    'women': 'woman', 'people': 'person', 'men': 'man', 'eyes': 'eye', 'knees': 'knee',
    'legs': 'leg', 'hands': 'hand', 'fingers': 'finger', 'arms': 'arm', 'steps': 'step',
    'sitting': 'sit', 'seated': 'sit', 'sits': 'sit', 'standing': 'stand', 'stood': 'stand',
    'pointing': 'point', 'points': 'point', 'pointed': 'point', 'looking': 'look', 'looks': 'look',
    'gazing': 'gaze', 'turned': 'turn', 'turning': 'turn', 'facing': 'face', 'faced': 'face',
    'wearing': 'wear', 'worn': 'wear', 'holding': 'hold', 'held': 'hold', 'blurred': 'blur',
    'blurry': 'blur', 'occupies': 'occupy', 'occupying': 'occupy', 'arranged': 'arrange',
    'arrangement': 'arrange', 'cropped': 'crop', 'cropping': 'crop', 'centered': 'center',
    'centred': 'center', 'placed': 'place', 'placement': 'place', 'raised': 'raise',
}
_KO_IRREGULAR = {'바라본': '바라보', '흐려': '흐리', '흐려져': '흐리', '흐려지고': '흐리',
                 '비워': '비우', '비운': '비우', '향해': '향하', '향하는': '향하'}


def _root(token):
    word = token.casefold()
    if re.fullmatch(r'[가-힣]+', word):
        if word in _KO_IRREGULAR:
            return _KO_IRREGULAR[word]
        original = word
        for suffix in _KO_ENDINGS:
            if word.endswith(suffix) and len(word) - len(suffix) >= 2:
                word = word[:-len(suffix)]
                break
        for suffix in _KO_PARTICLES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 2:
                word = word[:-len(suffix)]
                break
        # A bounded single-suffix normalizer: it records a root for lexical
        # matching, never rewrites query text or synthesizes a source clause.
        return word if word else original
    if word in _EN_IRREGULAR:
        return _EN_IRREGULAR[word]
    if len(word) > 6 and word.endswith('ing'):
        stem = word[:-3]
        if len(stem) > 3 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem
    if len(word) > 5 and word.endswith('ed'):
        stem = word[:-2]
        return stem[:-1] if stem.endswith('i') else stem
    if len(word) > 4 and word.endswith('ies'):
        return word[:-3] + 'y'
    if len(word) > 4 and word.endswith('s') and not word.endswith(('ss', 'us', 'is')):
        return word[:-1]
    return word


def _owners(text):
    found = {}
    for owner, pattern in _OWNER_RX.items():
        matches = []
        for m in pattern.finditer(text):
            matches.append({'start': m.start(), 'end': m.end(), 'quote': m.group()})
        if matches:
            found[owner] = matches
    return found


def _matches(pattern, text, maximum=6):
    out = []
    for m in pattern.finditer(text):
        out.append({'start': m.start(), 'end': m.end(), 'quote': m.group()})
        if len(out) >= maximum:
            break
    return out


_CLAUSE_EDGE = _rx(r'[;.!?。！？,，\n]|\b(?:and|but|while|whereas|or)\b|그리고|하지만|그러나|또는|아니면|반면에')


def _clause_bounds(text, start, end):
    left, right = 0, len(text)
    for match in _CLAUSE_EDGE.finditer(text):
        if match.end() <= start:
            left = match.end()
        elif match.start() >= end:
            right = match.start()
            break
    while left < right and text[left].isspace():
        left += 1
    while right > left and text[right - 1].isspace():
        right -= 1
    return left, right


def _owners_for_clause(text, start, end):
    result = {}
    for owner, matches in _owners(text[start:end]).items():
        result[owner] = [{'start': row['start'] + start, 'end': row['end'] + start,
                          'quote': row['quote']} for row in matches]
    return result


@lru_cache(maxsize=8192)
def _root_index(text):
    """Tokenize and stem one source string once for all advisory cues."""
    by_root = {}
    for surface, start, end in _token_spans(text):
        root = _root(surface)
        by_root.setdefault(root, []).append({'start': start, 'end': end,
                                             'quote': surface, 'root': root})
    return tuple((root, tuple(rows)) for root, rows in sorted(by_root.items()))


def _root_witnesses(text, cues, maximum=6):
    wanted = set(cues)
    out = [row for root, rows in _root_index(text) if root in wanted for row in rows]
    out.sort(key=lambda row: (row['start'], row['end'], row['root']))
    return out[:maximum]


def _root_triggered(rule_id, root_witnesses, owner_mentions):
    if not root_witnesses:
        return False
    requirement = _ROOT_REQUIREMENTS.get(rule_id)
    roots = {row['root'] for row in root_witnesses}
    if requirement:
        needed_roots, needed_owners = requirement
        return bool(roots & needed_roots) and bool(set(owner_mentions) & needed_owners)
    return True


def _primary_unit(unit):
    pointer = unit.get('pointer', '')
    return (isinstance(pointer, str) and re.match(
        r'^/content/(?:en$|ko$|definition$|phrase_en$|phrase_ko$|semantics/definition$|concept_units(?:/|$)|semantic_relations(?:/|$)|embedding_text$|components/)',
        pointer) is not None)


def _unit_order(pointer):
    if pointer.endswith('/definition'):
        return (0, pointer)
    if pointer.endswith(('/en', '/phrase_en')):
        return (1, pointer)
    if pointer.endswith(('/ko', '/phrase_ko')):
        return (2, pointer)
    return (3, pointer)


def compile_profiles(documents, *, source_units, source_effects):
    """Compile compact, exact-span witnesses from selected primary sources."""
    profiles = {}
    for identity in documents:
        units = sorted((u for u in source_units(identity) if _primary_unit(u) and isinstance(u.get('text'), str)),
                       key=lambda u: _unit_order(u.get('pointer', '')))
        effects = source_effects(identity) or {}
        properties = effects.get('properties', []) if isinstance(effects, dict) else []
        by_rule = {}
        for rule in _RULES:
            direct = []
            for unit in units:
                matches = _matches(rule['source_rx'], unit['text'], maximum=12)
                roots = _root_witnesses(unit['text'], _ROOT_CUES[rule['id']], maximum=3)
                root_matches = []
                for root in roots:
                    root_left, root_right = _clause_bounds(unit['text'], root['start'], root['end'])
                    root_owners = _owners_for_clause(unit['text'], root_left, root_right)
                    if _root_triggered(rule['id'], [root], root_owners):
                        root_matches.append(root)
                for witness in matches or root_matches:
                    start, end = witness['start'], witness['end']
                    clause_start, clause_end = _clause_bounds(unit['text'], start, end)
                    clause_owners = _owners_for_clause(unit['text'], clause_start, clause_end)
                    relation_owners = _nearest_owners([witness], clause_owners, rule['owners'])
                    if rule['id'] == 'frame_occupancy' and 'hand' in clause_owners and 'frame' in clause_owners:
                        relation_owners = sorted(set(relation_owners) | {'hand'})
                    direct.append({'pointer': unit['pointer'], 'literal_id': unit.get('literal_id'),
                                   'source_sha256': unit.get('source_sha256'), 'unit': unit['text'],
                                   'clause': unit['text'][clause_start:clause_end],
                                   'clause_bounds': {'start': clause_start, 'end': clause_end},
                                   'matches': [witness], 'root_witnesses': roots,
                                   'owners': clause_owners, 'relation_owners': relation_owners,
                                   'relation_owner_witnesses': _selected_owner_witnesses(
                                       [witness], clause_owners, relation_owners)})
            structured = []
            for prop in properties:
                if not isinstance(prop, dict):
                    continue
                path = prop.get('property', '')
                target = prop.get('target', '')
                if isinstance(path, str) and rule['property_rx'].search(path):
                    structured.append({'dimension': prop.get('dimension'), 'property': path,
                                       'target': target, 'owners': _owners(path.replace('_', ' ') + ' ' + str(target).replace('_', ' '))})
            if direct:
                by_rule[rule['id']] = {'direct': direct, 'properties': structured}
        # Color and numeric values are paired to owners inside one original
        # clause, so a color on one object cannot support another object.
        attributes = []
        for unit in units:
            for color, pattern in _COLOR_RX.items():
                for witness in _matches(pattern, unit['text'], maximum=3):
                    start, end = witness['start'], witness['end']
                    clause_start, clause_end = _clause_bounds(unit['text'], start, end)
                    attributes.append({'kind': 'color', 'value': color, 'value_witness': witness,
                                       'pointer': unit['pointer'], 'literal_id': unit.get('literal_id'),
                                       'source_sha256': unit.get('source_sha256'), 'unit': unit['text'],
                                       'clause': unit['text'][clause_start:clause_end],
                                       'owners': _selected_owner_witnesses([witness],
                                           _owners_for_clause(unit['text'], clause_start, clause_end),
                                           _nearest_owners([witness], _owners_for_clause(
                                               unit['text'], clause_start, clause_end), set(_OWNER_RX)))})
            for witness in _numbers(unit['text']):
                if not witness.get('unit'):
                    continue
                start, end = witness['start'], witness['end']
                clause_start, clause_end = _clause_bounds(unit['text'], start, end)
                attributes.append({'kind': 'number', 'value': witness['canonical'], 'value_witness': witness,
                                   'pointer': unit['pointer'], 'literal_id': unit.get('literal_id'),
                                   'source_sha256': unit.get('source_sha256'), 'unit': unit['text'],
                                   'clause': unit['text'][clause_start:clause_end],
                                   'owners': _selected_owner_witnesses([witness],
                                       _owners_for_clause(unit['text'], clause_start, clause_end),
                                       _nearest_owners([witness], _owners_for_clause(
                                           unit['text'], clause_start, clause_end), set(_OWNER_RX)))})
        single_property = {}
        for kind in ('reflection_identity', 'tilt_owner_disambiguation'):
            witness = _single_property_source_witness(kind, units, effects)
            if witness:
                single_property[kind] = {**witness, 'selected_rid_identity': identity}
        profile = {'relations': by_rule, 'attributes': attributes, 'single_property': single_property,
                   'primary_metadata': {unit['pointer']: {'literal_id': unit.get('literal_id'),
                       'source_sha256': unit.get('source_sha256')} for unit in units}}
        profile['property_answers'] = _property_answers.compile_property_answers(units, profile, effects)
        profiles[identity] = profile
    return profiles


def _query_mode(text):
    question = bool(_QUESTION.search(text))
    alternative = bool(_ALTERNATIVE.search(text))
    negative = bool(_NEGATIVE.search(text))
    positive = bool(_POSITIVE_ASSERTION.search(text))
    if question:
        return {'kind': 'interrogative_property', 'polarity': 'unbound',
                'alternatives_unbound': alternative}
    if _IMPERATIVE.search(text):
        return {'kind': 'imperative_request', 'polarity': 'negative' if negative and not alternative else 'positive',
                'alternatives_unbound': alternative}
    if negative and not alternative:
        return {'kind': 'declarative_assertion', 'polarity': 'negative',
                'alternatives_unbound': False}
    if positive and not alternative:
        return {'kind': 'declarative_assertion', 'polarity': 'positive',
                'alternatives_unbound': False}
    return {'kind': 'natural_query', 'polarity': 'unbound',
            'alternatives_unbound': alternative}


def _feature_query_mode(text, mentions):
    """Use only the clause carrying a feature mention for its polarity."""
    local_modes = []
    for mention in mentions:
        start, end = _clause_bounds(text, mention['start'], mention['end'])
        local_modes.append(_query_mode(text[start:end]))
    if not local_modes:
        return _query_mode(text)
    polarities = {row['polarity'] for row in local_modes}
    alternatives = any(row['alternatives_unbound'] for row in local_modes)
    if alternatives:
        return {'kind': 'natural_query', 'polarity': 'unbound', 'alternatives_unbound': True}
    if len(polarities) != 1:
        return {'kind': 'natural_query', 'polarity': 'unbound', 'alternatives_unbound': False}
    selected = local_modes[0].copy()
    if len({row['kind'] for row in local_modes}) > 1:
        selected['kind'] = 'natural_query'
    return selected


def _numbers(text):
    values = []
    for m in _NUMBER.finditer(text):
        raw = re.sub(r'\s+', '', m.group()).replace('—', '–').casefold()
        unit_match = _NUMBER_UNITS.search(raw)
        unit = unit_match.group(1).replace(' ', '').casefold() if unit_match else ''
        numbers = re.findall(r'\d+(?:\.\d+)?', raw)
        if numbers:
            values.append({'start': m.start(), 'end': m.end(), 'quote': m.group(),
                           'numbers': numbers, 'unit': unit,
                           'canonical': '-'.join(numbers) + unit})
    return values


def _colors(text):
    result = []
    for color, pattern in _COLOR_RX.items():
        for match in pattern.finditer(text):
            result.append({'color': color, 'start': match.start(), 'end': match.end(),
                           'quote': match.group()})
    return sorted(result, key=lambda row: (row['start'], row['end'], row['color']))


def _nearest_owners(feature_spans, owner_spans, allowed):
    # Attach only the nearest compatible owner to each relation/value mention.
    # This keeps unrelated owners elsewhere in a long sentence from leaking in.
    selected = set()
    for span in feature_spans:
        candidates = []
        for owner, rows in owner_spans.items():
            if owner not in allowed:
                continue
            for row in rows:
                distance = (0 if row['start'] <= span['end'] and span['start'] <= row['end'] else
                            min(abs(row['start'] - span['end']), abs(span['start'] - row['end'])))
                candidates.append((distance, owner, row['start']))
        candidates.sort()
        if not candidates or candidates[0][0] > 80:
            continue
        nearest = candidates[0][0]
        selected.update(owner for distance, owner, _ in candidates if distance == nearest)
    # Keep the most specific object owner when a generic accessory alias is
    # also present (for example eyewear versus a phone or bag).
    specific = {'eyewear', 'phone', 'bag', 'nails', 'hair', 'shirt', 'jacket', 'dress',
                'coat', 'skirt', 'pants', 'ring', 'wall', 'sock', 'boot', 'footwear',
                'bandana', 'headband', 'scarf', 'lips', 'blush', 'brows'}
    if set(selected) & specific:
        selected.discard('accessory')
    if set(selected) & {'shirt', 'jacket', 'dress', 'coat', 'skirt', 'pants', 'sock', 'boot',
                        'footwear', 'bandana', 'headband', 'scarf'}:
        selected.discard('garment')
    return sorted(selected)


def _selected_owner_witnesses(feature_spans, owner_spans, selected):
    result = {}
    for owner in selected:
        rows = []
        for span in feature_spans:
            distances = [(0 if row['start'] <= span['end'] and span['start'] <= row['end'] else
                          min(abs(row['start'] - span['end']), abs(span['start'] - row['end'])), row)
                         for row in owner_spans.get(owner, [])]
            if not distances:
                continue
            distances.sort(key=lambda item: (item[0], item[1]['start']))
            nearest = distances[0][0]
            rows.extend(row for distance, row in distances if distance == min(80, nearest))
        unique = {(row['start'], row['end'], row['quote']): row for row in rows}
        if unique:
            result[owner] = [unique[key] for key in sorted(unique)]
    return result


def _attribute_requests(numbers, colors, owner_spans):
    requests = []
    for kind, values in (('number', numbers), ('color', colors)):
        for value in values:
            value_span = {'start': value['start'], 'end': value['end'], 'quote': value['quote']}
            owners = _nearest_owners([value_span], owner_spans, set(_OWNER_RX))
            requests.append({'kind': kind, 'value': value, 'owners': owners,
                             'owner_witnesses': _selected_owner_witnesses([value_span], owner_spans, owners)})
    return requests


def _query_features(text):
    owners = _owners(text)
    mode = _query_mode(text)
    numbers = _numbers(text)
    colors = _colors(text)
    features = []
    for rule in _RULES:
        mentions = _matches(rule['query_rx'], text, maximum=12)
        root_witnesses = _root_witnesses(text, _ROOT_CUES[rule['id']], maximum=12)
        if not mentions and _root_triggered(rule['id'], root_witnesses, owners):
            mentions = [{'start': r['start'], 'end': r['end'], 'quote': r['quote']}
                        for r in root_witnesses]
        if rule['id'] == 'posture' and mentions:
            contextual_spans = [(match.start(), match.end())
                                for match in _POSTURE_CONTEXT.finditer(text)]
            mentions = [mention for mention in mentions if not any(
                start <= mention['start'] and mention['end'] <= end
                for start, end in contextual_spans)]
        if rule['id'] == 'body_orientation':
            mentions = [m for m in mentions if m['quote'].casefold() != 'face' or re.search(r'\bface\s+(?:the\s+)?(?:camera|lens|away|toward|forward|left|right)\b', text, re.I)]
        if rule['id'] == 'head_orientation' and not re.search(r'\bhead\b.{0,24}\b(?:turn|direction|face|point|orient)\w*|\b(?:turn|direction|orient)\w*.{0,24}\bhead\b|머리.{0,18}(?:돌|향|방향)', text, re.I):
            mentions = []
        if rule['id'] == 'focal_length' and not re.search(r'\b(?:focal length|wide[- ]angle|\d+(?:[.–-]\d+)?\s*mm|lens (?:length|type|focal))\b|초점거리|화각', text, re.I):
            mentions = []
        if rule['id'] == 'subject_placement' and re.search(r'\bknees?\s+(?:are\s+)?position\w*|무릎.{0,10}위치', text, re.I) and not re.search(r'\b(?:person|woman|model|subject)\s+(?:is\s+)?(?:placed|positioned)\b|프레임.{0,14}(?:배치|위치)', text, re.I):
            mentions = []
        if rule['id'] == 'background_visibility' and not re.search(r'\b(?:visible|visibility|see|seen|show|beyond|behind)\b|보이|보여|너머|뒤쪽', text, re.I):
            mentions = []
        if rule['id'] == 'camera_height' and not mentions:
            m = re.search(r'\bhow high\s+(?:is|was)\s+(?:the\s+)?camera\b', text, re.I)
            if m: mentions = [{'start':m.start(), 'end':m.end(), 'quote':m.group()}]
        if not mentions:
            continue
        feature_mode = _feature_query_mode(text, mentions)
        feature_owners = _nearest_owners(mentions, owners, rule['owners'])
        owner_alternatives = bool(mode['alternatives_unbound'] and rule['id'] == 'tilt_or_roll')
        if owner_alternatives:
            feature_owners = sorted(set(feature_owners) | (set(owners) & rule['owners']))
        if rule['id'] == 'subject_placement' and not set(feature_owners) & {'person', 'frame'}:
            continue
        value_labels = []
        for label, pattern in rule['value_rx'].items():
            if pattern.search(text):
                value_labels.append(label)
        value_any_facets = []
        if rule['id'] == 'reflection_identity' and re.search(
                r'\b(?:same|other|second person|someone else|who.{0,24}(?:mirror|reflection)|(?:mirror|reflection).{0,24}who)\b|같은.{0,8}(?:사람|인물)|다른.{0,8}(?:사람|인물)|거울.{0,16}(?:누구|동일)', text, re.I):
            if mode['kind'] == 'interrogative_property' or mode['alternatives_unbound']:
                value_labels = []
                value_any_facets = ['same_subject', 'different_subject']
        if rule['id'] == 'wear_or_hold' and (mode['kind'] == 'interrogative_property' or mode['alternatives_unbound']):
            value_labels = []
        elif rule['id'] == 'wear_or_hold':
            if re.search(r'\b(?:worn|wearing|wears?)\b.{0,20}\bnot\s+(?:held|holding)\b|착용.{0,16}(?:들지|쥐지)\s*않', text, re.I):
                value_labels = ['worn']
            elif re.search(r'\b(?:held|holding)\b.{0,20}\bnot\s+(?:worn|wearing)\b|(?:들고|쥐고).{0,16}착용하지\s*않', text, re.I):
                value_labels = ['held']
            elif len(value_labels) > 1:
                value_labels = []
        nearby_numbers = [n for n in numbers if min(abs(n['start'] - m['end']) for m in mentions) <= 80]
        nearby_colors = [c for c in colors if min(abs(c['start'] - m['end']) for m in mentions) <= 80]
        attribute_requests = _attribute_requests(nearby_numbers, nearby_colors, owners)
        features.append({'id': rule['id'], 'query_text': text, 'owners': feature_owners,
                         'owner_alternatives_unbound': owner_alternatives,
                         'relation_witnesses': mentions, 'owner_witnesses':
                             _selected_owner_witnesses(mentions, owners, feature_owners),
                         'root_witnesses': root_witnesses,
                         'value_facets': value_labels,
                         'value_any_facets': value_any_facets,
                         'numbers': nearby_numbers, 'colors': nearby_colors,
                         'attribute_requests': attribute_requests,
                         'polarity': feature_mode['polarity'], 'query_mode': feature_mode,
                         'alternative_group':
                             rule['id'] if mode['alternatives_unbound'] and rule['id'] in {'tilt_or_roll', 'reflection_identity', 'wear_or_hold'} else None})
    floor = re.search(r'(?:\b(?:floor|ground)\b.{0,24}\b(?:sit(?:s|ting)?|seated)\b|\b(?:sit(?:s|ting)?|seated)\b.{0,24}\b(?:floor|ground)\b|(?:바닥|지면).{0,16}앉|앉.{0,16}(?:바닥|지면))', text, re.I)
    if floor:
        posture = next((f for f in features if f['id'] == 'posture'), None)
        if posture is None:
            posture = {'id':'posture', 'query_text':text, 'owners':['person'], 'owner_alternatives_unbound':False, 'relation_witnesses':[], 'owner_witnesses':{}, 'root_witnesses':[], 'value_facets':[], 'value_any_facets':[], 'numbers':[], 'colors':[], 'attribute_requests':[], 'polarity':'positive', 'query_mode':mode, 'alternative_group':None}
            features.append(posture)
        posture['context_only'] = True
        posture['value_facets'] = sorted(set(posture['value_facets']) | {'floor'})
        posture['relation_witnesses'].append({'start':floor.start(), 'end':floor.end(), 'quote':floor.group()})
    knee_camera = re.search(r'\bknees?\b[\s\S]{0,56}\b(?:relative to|with respect to|in relation to)\s+(?:the\s+)?(?:camera|lens)\b|\bknees?\b[\s\S]{0,28}\btoward(?:s)?\s+(?:the\s+)?(?:camera|lens)\b|무릎.{0,32}(?:카메라.{0,8}기준|렌즈.{0,8}방향|전경)', text, re.I)
    if knee_camera:
        for feature in features:
            if feature['id'] == 'knee_state': feature['value_facets'] = sorted(set(feature['value_facets']) | {'camera_relative'})
    unit_numbers = [row for row in numbers if row.get('unit')]
    if colors or unit_numbers:
        value_spans = [*colors, *unit_numbers]
        requests = _attribute_requests(unit_numbers, colors, owners)
        attribute_owners = sorted({owner for request in requests for owner in request['owners']})
        features.append({'id': 'color_or_numeric_attribute', 'owners': attribute_owners,
                         'relation_witnesses': value_spans,
                         'owner_witnesses': {owner: sorted({(row['start'], row['end'], row['quote']): row
                             for request in requests for row in request['owner_witnesses'].get(owner, [])}.values(),
                             key=lambda row: (row['start'], row['end'])) for owner in attribute_owners},
                         'root_witnesses': [], 'value_facets': [],
                         'numbers': unit_numbers, 'colors': colors, 'attribute_requests': requests,
                         'ranking_blockers': (['unmodeled_attribute_constraint']
                             if _UNMODELED_ATTRIBUTE_CONSTRAINT.search(text) else []),
                         'polarity': mode['polarity'], 'query_mode': mode, 'alternative_group': None})
    # Explicit numbers can themselves be queried attributes, but are never
    # copied from source into query semantics. Attach them to the closest known
    # feature; a stand-alone numeric query stays unrecognized and falls back.
    return features, mode, owners, numbers, colors


def _compatible_owners(query_owners, evidence_owners):
    if not query_owners:
        return True
    if not evidence_owners:
        return False
    # Generic parent/child compatibility for a person and a named body part.
    if 'person' in query_owners and evidence_owners & {'person', 'body', 'head', 'eyes', 'hand', 'arm', 'leg'}:
        return True
    if 'frame' in query_owners and evidence_owners & {'frame', 'camera', 'environment', 'doorway', 'stairs'}:
        return True
    if 'environment' in query_owners and evidence_owners & {'environment', 'doorway', 'stairs', 'frame'}:
        return True
    # A generic garment query may be supported by an explicitly named garment
    # owner. The inverse does not hold: a jacket request needs a jacket witness.
    garment_children = {'shirt', 'jacket', 'dress', 'coat', 'skirt', 'pants', 'sock', 'boot',
                        'footwear', 'bandana', 'headband', 'scarf'}
    if 'garment' in query_owners and evidence_owners & (garment_children | {'garment'}):
        return True
    # A generic environment owner can include a named wall, but wall color is
    # never transferred to a different specific object.
    if 'environment' in query_owners and 'wall' in evidence_owners:
        return True
    return bool(set(query_owners) & evidence_owners)


def _evidence_owners(row):
    out = set(row.get('owners', {}))
    return out


def _source_polarity(rule_id, direct, properties):
    text = direct.get('clause', direct['unit'])
    material = text + ' ' + ' '.join(str(p.get('property', '')) + ' ' + str(p.get('target', '')) for p in properties)
    if rule_id == 'gaze_direction':
        if re.search(r'\b(?:looks? away|gaze.{0,24}away|not look(?:s|ing)? at|does not look at|away from the camera|away from lens)\b|카메라.{0,12}(?:보지|바라보지)|(?:시선|눈길).{0,12}(?:벗어나|외면)', material, re.I):
            return 'negative'
        if re.search(r'\b(?:looks? at (?:the )?camera|looks? toward (?:the )?(?:camera|lens)|gaze.{0,24}(?:camera|lens)|eyes? meet(?:s)? the lens|eye contact)\b|카메라.{0,12}바라보|렌즈.{0,12}바라보', material, re.I):
            return 'positive'
    if rule_id == 'body_orientation':
        if re.search(r'\b(?:faces? away|back (?:mostly )?(?:to|toward) the camera|away from the camera)\b|등.{0,12}카메라.{0,8}(?:향하|보이)', material, re.I):
            return 'negative'
        if re.search(r'\b(?:faces? the camera|facing the camera|front toward the camera)\b|몸.{0,12}카메라.{0,8}(?:향하|바라보)', material, re.I):
            return 'positive'
    return 'unbound'


def _match_feature(profile, feature, rule, *, all_options=False):
    evidence = profile.get('relations', {}).get(rule['id'])
    if not evidence:
        return None
    query_owners = feature.get('owners') or []
    options = []
    all_value_witnesses = []
    for direct in evidence.get('direct', []):
        if rule['id'] == 'arms_position':
            query_text = feature.get('query_text', '')
            actions = {'raised': r'\b(?:raise[ds]?|raising|lift(?:ed|s|ing)?)\b|팔.{0,20}(?:들|올리)',
                       'hanging': r'\bhang(?:s|ing)?\b|팔.{0,20}(?:늘어뜨리|내리)',
                       'crossed': r'\bcross(?:ed|ing)?\b|팔.{0,20}(?:교차|포개)'}
            requested = [name for name, rx in actions.items() if re.search(rx, query_text, re.I)]
            clause = direct.get('clause', direct['unit'])
            if any(not re.search(actions[name], clause, re.I) for name in requested):
                continue
            if requested and 'bilateral' in feature.get('value_facets', []):
                for name in requested:
                    rx = actions[name]
                    if not re.search(r'(?:\b(?:both|two|each)\s+arms?\b.{0,40}(?:' + rx + r')|(?:' + rx + r').{0,40}\b(?:both|two|each)\s+arms?\b|양팔.{0,24}(?:들|올리|늘어뜨리|내리|교차|포개))', clause, re.I):
                        break
                else:
                    pass
                if name != requested[-1] or not re.search(r'(?:\b(?:both|two|each)\s+arms?\b.{0,40}(?:' + actions[requested[-1]] + r')|(?:' + actions[requested[-1]] + r').{0,40}\b(?:both|two|each)\s+arms?\b|양팔.{0,24}(?:들|올리|늘어뜨리|내리|교차|포개))', clause, re.I):
                    continue
        direct_owner_rows = direct.get('owners', {})
        direct_owners = set(direct.get('relation_owners', []))
        prop_matches = []
        for prop in evidence.get('properties', []):
            prop_owner = set(prop.get('owners', {}))
            if _compatible_owners(query_owners, prop_owner) and (
                    not query_owners or _compatible_owners(query_owners, direct_owners)):
                prop_matches.append(prop)
        if 'camera_relative' in feature.get('value_facets', []) and not prop_matches:
            continue
        if feature.get('context_only'):
            prop_matches = [p for p in prop_matches if p.get('property') in {'pose.body.seated.floor', 'body.posture.seated_on_floor'}]
            if not prop_matches:
                continue
        # Relation owners come from the nearest clause-local source witnesses;
        # a union of all owners in the unit cannot establish this relation.
        if not _compatible_owners(query_owners, direct_owners):
            continue
        supported_values = []
        for value, pattern in rule.get('value_rx', {}).items():
            value_matches = _matches(pattern, direct.get('clause', direct['unit']), maximum=2)
            if value_matches:
                supported_values.append({'value': value, 'witnesses': value_matches,
                                         'pointer': direct['pointer'],
                                         'source_clause_bounds': direct.get('clause_bounds')})
                all_value_witnesses.extend(supported_values[-1:])
        if rule['id'] == 'arms_position' and 'bilateral' in feature.get('value_facets', []) and not requested:
            anchor = (direct.get('matches') or [{}])[0].get('start')
            pair = _pose_answers.same_owner_arm_pair(direct['unit'], anchor_offset=anchor)
            if pair and prop_matches:
                supported_values.append({'value': 'bilateral', 'witnesses': [pair['first_arm'], pair['other_arm']], 'pointer': direct['pointer'], 'source_span': pair['source_span'], 'source_quote': pair['source_quote']})
        supported_labels = {value['value'] for value in supported_values}
        if feature.get('value_facets') and not set(feature['value_facets']) <= supported_labels:
            continue
        if feature.get('value_any_facets') and not (set(feature['value_any_facets']) & supported_labels):
            continue
        if _UNQUALIFIED_SOURCE.search(direct.get('clause', direct['unit'])):
            continue
        source_polarity = _source_polarity(rule['id'], direct, prop_matches)
        if feature.get('polarity') in {'positive', 'negative'} and source_polarity in {'positive', 'negative'} and source_polarity != feature['polarity']:
            continue
        options.append({'pointer': direct['pointer'], 'literal_id': direct.get('literal_id'),
                        'source_sha256': direct.get('source_sha256'), 'relation_witnesses': direct['matches'],
                        'source_clause_bounds': direct.get('clause_bounds'),
                        'source_clause': direct.get('clause'),
                        'owner_evidence': {o: direct.get('relation_owner_witnesses', {}).get(o, [])
                                           for o in sorted(direct_owners)},
                        'effect_properties': prop_matches[:3], 'value_witnesses': supported_values,
                        'source_polarity': source_polarity,
                        'source_unit': direct['unit']})
    if not options:
        return None
    options.sort(key=lambda row: (_unit_order(row['pointer']), row['literal_id'] or '', row['source_sha256'] or ''))
    if feature.get('value_facets'):
        options = [{**o, 'query_value_supports': [v for v in all_value_witnesses if v['value'] in feature['value_facets'] and v['pointer'] == o['pointer']]} for o in options]
    return options if all_options else options[0]


def _match_attributes(profile, feature):
    requests = feature.get('attribute_requests', [])
    if not requests:
        return None
    # Attribute ranking is allowed only when both query and source name the
    # same owner class. A color without a witnessed owner remains lexical data.
    if any(not request.get('owners') or not request.get('owner_witnesses') for request in requests):
        return None
    by_unit = {}
    for request_index, request in enumerate(requests):
        query = request['value']
        query_owners = set(request.get('owners') or [])
        for row in profile.get('attributes', []):
            evidence_owners = _evidence_owners(row)
            if (row.get('kind') != request['kind'] or not evidence_owners
                    or not _compatible_owners(query_owners, evidence_owners)):
                continue
            equal = query.get('canonical') == row.get('value') if request['kind'] == 'number' else query.get('color') == row.get('value')
            if not equal:
                continue
            match = {'query': query, 'query_owner_witnesses': request.get('owner_witnesses', {}),
                     'source': row}
            unit_key = (row['pointer'], row.get('literal_id') or '', row.get('source_sha256') or '')
            unit = by_unit.setdefault(unit_key, {'request_indices': set(), 'number_matches': [],
                                                  'color_matches': []})
            unit['request_indices'].add(request_index)
            unit['number_matches' if request['kind'] == 'number' else 'color_matches'].append(match)
    if not by_unit:
        return None
    complete_keys = [key for key, unit in by_unit.items() if len(unit['request_indices']) == len(requests)]
    best_key = sorted(complete_keys or list(by_unit),
                      key=lambda key: (-len(by_unit[key]['request_indices']),
                                       _unit_order(key[0]), key[1], key[2]))[0]
    best = by_unit[best_key]
    number_matches = best['number_matches']
    color_matches = best['color_matches']
    ordered = sorted([m['source'] for m in number_matches + color_matches],
                     key=lambda row: (_unit_order(row['pointer']), row.get('literal_id') or '',
                                      row.get('value_witness', {}).get('start', -1)))
    complete_same_unit = len(best['request_indices']) == len(requests)
    source_unit_pointers = [best_key[0]]
    return {'pointer': ordered[0]['pointer'], 'literal_id': ordered[0].get('literal_id'),
            'source_sha256': ordered[0].get('source_sha256'),
            'owners': ordered[0].get('owners', {}), 'number_witnesses': number_matches,
            'color_witnesses': color_matches, 'matched_request_count': len(best['request_indices']),
            'request_count': len(requests), 'source_unit_pointers': source_unit_pointers,
            'source_unit_identity': {'pointer': best_key[0], 'literal_id': best_key[1],
                                     'source_sha256': best_key[2]},
            'complete_same_unit': complete_same_unit,
            'source_facts': [{'kind': row['kind'], 'value': row['value'],
                              'value_witness': row['value_witness'], 'pointer': row['pointer'],
                              'literal_id': row.get('literal_id'), 'source_sha256': row.get('source_sha256'),
                              'owners': row['owners'], 'clause': row['clause']}
                             for row in ordered]}


def _canonical_order_sha(rows):
    raw = '\n'.join(row['id'] for row in rows).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def _apply_single_property_order(rows, text, profiles, trace, *, structured, original_rows):
    """Stable-partition direct, selected-RID witnesses for two open question classes."""
    query = None if structured else _single_property_query(text)
    original_rank = {row['id']: rank for rank, row in enumerate(original_rows, 1)}
    incoming_order = list(rows)
    incoming_sha = _canonical_order_sha(incoming_order)
    query_kind = query.get('kind') if query else None
    positive = []
    witness_by_id = {}
    if query_kind:
        for row in incoming_order:
            witness = profiles.get(row['id'], {}).get('single_property', {}).get(query_kind)
            if witness and witness.get('promoted') is True:
                positive.append(row)
                witness_by_id[row['id']] = witness
    positive_ids = {row['id'] for row in positive}
    ordered = positive + [row for row in incoming_order if row['id'] not in positive_ids]
    output_sha = _canonical_order_sha(ordered)
    lane = {'schema': 'photo-h-f2-single-property-lane/v1',
            'policy': SINGLE_PROPERTY_ORDERING_POLICY,
            'applicable': bool(query),
            'reason': ('structured_scope' if structured else
                       'query_class_unrecognized' if not query else
                       'no_direct_primary_and_effect_witness' if not positive else
                       'stable_positive_witness_partition'),
            'query_kind': query_kind,
            'query_evidence_spans': query.get('evidence_spans', []) if query else [],
            'query_property_value_unbound': bool(query),
            'query_alternatives_unbound': bool(query and re.search(
                r'\b(?:or|either|rather than|instead of|versus|vs)\b|아니면|혹은|또는|반면', text, re.I)),
            'source_witness_candidate_count': len(positive),
            'source_witness_order_sha256': _canonical_order_sha(positive),
            'candidate_order_before_sha256': incoming_sha,
            'candidate_order_after_sha256': output_sha,
            'top8_witnesses': [],
            'candidate_filter': False,
            'query_rewritten': False,
            'embedding_input_changed': False,
            'source_profiles_read_only': True,
            'primary_source_only': True,
            'effects_read_from_same_selected_rid_profile': True,
            'semantic_controller_verified': False,
            'native_approval': False,
            'semantic_approval': False}
    previous_witnesses = {item['id']: item for item in trace.get('top8_source_witnesses', [])}
    top_witnesses = []
    for rank_after, row in enumerate(ordered[:8], 1):
        witness = witness_by_id.get(row['id'])
        previous = previous_witnesses.get(row['id'])
        if not previous and not witness:
            continue
        item = dict(previous or {})
        item.update({'id': row['id'], 'cid': row['cid'], 'rid': row['rid'],
                     'rank_before': original_rank.get(row['id']), 'rank_after': rank_after})
        item.setdefault('score', 0.0)
        item.setdefault('base_rrf', float(row.get('rrf', 0.0)))
        item.setdefault('source_lane_rank', None)
        item.setdefault('source_lane_contribution', 0.0)
        features = list(item.get('supported_features', []))
        if witness:
            item['single_property_witness'] = witness
            feature_id = 'single_property:' + query_kind
            if not any(feature.get('feature_id') == feature_id for feature in features):
                features.append({'feature_id': feature_id,
                                 'support': 'DIRECT_PRIMARY_TEXT_AND_SAME_SELECTED_RID_EFFECT',
                                 'query': query,
                                 'source': witness,
                                 'ranking_eligible': True,
                                 'semantic_controller_verified': False})
        if features:
            item['supported_features'] = features
        top_witnesses.append(item)
        if witness:
            lane['top8_witnesses'].append({'id': row['id'], 'cid': row['cid'],
                                           'rid': row['rid'], 'rank_after': rank_after,
                                           'witness': witness})
    trace['single_property_lane'] = lane
    trace['applied'] = [row['id'] for row in ordered] != [row['id'] for row in original_rows]
    trace['candidate_order_before_sha256'] = _canonical_order_sha(original_rows)
    trace['candidate_order_after_sha256'] = output_sha
    trace['candidate_order_sha256'] = output_sha
    trace['top8_source_witnesses'] = top_witnesses
    if positive:
        trace['reason'] = 'stable_positive_single_property_witness_partition'
    return ordered, json.loads(json.dumps(trace, ensure_ascii=False, sort_keys=True, allow_nan=False))


def _order_source_relevance_v6(rows, text, profiles, *, structured=False,
                           relation_lane_weight=DEFAULT_RELATION_LANE_WEIGHT,
                           attribute_lane_weight=ATTRIBUTE_LANE_WEIGHT):
    """Stable, non-filtering advisory rank. Unknown requests keep the input order."""
    weights = {'relation': float(relation_lane_weight), 'attribute': float(attribute_lane_weight)}
    if any(not 0.0 <= value <= 1.0 for value in weights.values()):
        raise ValueError('source relevance weights must be in [0, 1]')
    if structured:
        trace = {'schema': RECIPE, 'policy': SCORING_POLICY, 'lane_weights': weights,
                      'applied': False, 'reason': 'structured_scope',
                      'recognized_features': [], 'candidate_filter': False,
                      'query_rewritten': False, 'embedding_input_changed': False,
                      'native_approval': False, 'semantic_approval': False}
        return _apply_single_property_order(rows, text, profiles, trace,
                                            structured=True, original_rows=rows)
    features, mode, query_owners, numbers, colors = _query_features(text)
    if not features:
        trace = {'schema': RECIPE, 'policy': SCORING_POLICY, 'lane_weights': weights,
                      'applied': False, 'reason': 'no_recognized_relation',
                      'query_mode': mode, 'recognized_features': [], 'candidate_filter': False,
                      'query_rewritten': False, 'embedding_input_changed': False,
                      'native_approval': False, 'semantic_approval': False}
        return _apply_single_property_order(rows, text, profiles, trace,
                                            structured=False, original_rows=rows)
    rule_by_id = {r['id']: r for r in _RULES}
    relation_features = [feature for feature in features if feature['id'] != 'color_or_numeric_attribute']
    mentioned_roles = {owner for feature in relation_features for owner in feature.get('owners', [])}
    attribute_lane_blocked = any(feature.get('ranking_blockers') for feature in features)
    relation_lane_applicable = (mode['kind'] == 'interrogative_property'
                                and len(relation_features) >= 2
                                and not attribute_lane_blocked)
    eligible_feature_ids = {feature['id'] for feature in features
                             if (feature['id'] == 'color_or_numeric_attribute'
                                 and not feature.get('ranking_blockers')) or relation_lane_applicable}
    scored = []
    support_digest_rows = []
    all_supported = 0
    rankable_supported = 0
    for old_rank, row in enumerate(rows, 1):
        profile = profiles.get(row['id'], {})
        evidence_rows = []
        supported_units = {}
        score = 0.0
        rank_score = 0.0
        ranking_feature_ids = set()
        for feature in features:
            ranking_eligible = feature['id'] in eligible_feature_ids
            attribute = _match_attributes(profile, feature)
            if feature['id'] == 'color_or_numeric_attribute':
                if attribute:
                    coverage = attribute['matched_request_count'] / max(attribute['request_count'], 1)
                    contribution = coverage + (0.25 * coverage if feature.get('owners') and attribute.get('owners') else 0.0)
                    score += contribution
                    if attribute.get('complete_same_unit'):
                        supported_units[feature['id']] = set(attribute.get('source_unit_pointers', []))
                    if ranking_eligible and attribute.get('complete_same_unit'):
                        rank_score += contribution
                        ranking_feature_ids.add(feature['id'])
                    evidence_rows.append({'feature_id': feature['id'],
                                          'support': ('direct_primary_attribute' if attribute.get('complete_same_unit')
                                                      and not feature.get('ranking_blockers') else 'partial_primary_attribute'),
                                          'query': feature, 'source': attribute,
                                          'ranking_eligible': ranking_eligible})
                continue
            rule = rule_by_id[feature['id']]
            options = _match_feature(profile, feature, rule, all_options=True) or []
            evidence = options[0] if options else None
            # Values/owners contribute only when tied to this same selected RID.
            value_points = 0.0
            if evidence:
                owner_points = 0.25 if feature.get('owners') and evidence.get('owner_evidence') else 0.0
                contribution = 1.0 + owner_points + value_points
                score += contribution
                supported_units[feature['id']] = {evidence['pointer']}
                if ranking_eligible:
                    rank_score += contribution
                    ranking_feature_ids.add(feature['id'])
                evidence_rows.append({'feature_id': feature['id'], 'support': 'LEXICAL_SOURCE_FACET_MATCH',
                                      'query': feature, 'source': evidence,
                                      '_source_options': options,
                                      'attribute_source': attribute,
                                      'ranking_eligible': ranking_eligible})
            elif attribute:
                score += value_points
                if ranking_eligible:
                    rank_score += value_points
                evidence_rows.append({'feature_id': feature['id'], 'support': 'direct_primary_attribute',
                                      'query': feature, 'source': None,
                                      'attribute_source': attribute,
                                      'ranking_eligible': ranking_eligible})
        if score > 0:
            all_supported += 1
        complete_unit_coverage = bool(eligible_feature_ids) and all(
            feature_id in supported_units for feature_id in eligible_feature_ids)
        if complete_unit_coverage:
            common_units = set.intersection(*(supported_units[feature_id] for feature_id in sorted(eligible_feature_ids)))
            complete_unit_coverage = bool(common_units)
            if complete_unit_coverage:
                for evidence_row in evidence_rows:
                    options = evidence_row.get('_source_options', [])
                    same = [option for option in options if option['pointer'] in common_units]
                    if same:
                        evidence_row['source'] = same[0]
        for evidence_row in evidence_rows:
            evidence_row.pop('_source_options', None)
        if not complete_unit_coverage:
            rank_score = 0.0
        if rank_score > 0:
            rankable_supported += 1
        relation_ids = {feature['id'] for feature in relation_features}
        lane_weight = (weights['relation'] if relation_lane_applicable and ranking_feature_ids & relation_ids
                       else weights['attribute'])
        scored.append((rank_score, old_rank, row, evidence_rows, score, lane_weight))
        support_digest_rows.append({'id': row['id'], 'score': score, 'rank_score': rank_score,
                                    'features': [e['feature_id'] for e in evidence_rows]})
    if not rankable_supported:
        top_witnesses = []
        for _, old_rank, row, evidence, raw_score, lane_weight in scored[:8]:
            if evidence:
                top_witnesses.append({'id': row['id'], 'cid': row['cid'], 'rid': row['rid'],
                                      'rank_before': old_rank, 'rank_after': old_rank,
                                      'score': raw_score, 'base_rrf': float(row.get('rrf', 0.0)),
                                      'source_lane_rank': None, 'source_lane_contribution': 0.0,
                                      'supported_features': evidence})
        trace = {'schema': RECIPE, 'policy': SCORING_POLICY, 'lane_weights': weights,
                 'applied': False,
                 'reason': 'relation_lane_not_applicable' if all_supported else 'no_primary_source_support',
                 'query_mode': mode, 'recognized_features': features,
                 'relation_lane_applicable': relation_lane_applicable,
                 'eligible_feature_ids': sorted(eligible_feature_ids),
                 'candidates_with_primary_support': all_supported,
                 'top8_source_witnesses': top_witnesses,
                 'candidate_filter': False, 'query_rewritten': False,
                 'embedding_input_changed': False, 'native_approval': False,
                 'semantic_approval': False, 'candidate_order_sha256': _canonical_order_sha(rows)}
        return _apply_single_property_order(rows, text, profiles, trace,
                                            structured=False, original_rows=rows)
    source_lane = sorted(scored, key=lambda item: (-item[0], item[1], item[2]['id']))
    source_rank = {item[2]['id']: rank for rank, item in enumerate(source_lane, 1)}
    merged = []
    for rank_score, old_rank, row, evidence, raw_score, lane_weight in scored:
        base_rrf = float(row.get('rrf', 0.0))
        contribution = lane_weight / (10 + source_rank[row['id']]) if rank_score > 0 else 0.0
        merged.append((-(base_rrf + contribution), old_rank, row['id'], rank_score,
                       row, evidence, contribution, raw_score, lane_weight))
    merged.sort(key=lambda item: (item[0], item[1], item[2]))
    ordered = [item[4] for item in merged]
    position = {item[4]['id']: rank for rank, item in enumerate(merged, 1)}
    top_witnesses = []
    for _, old_rank, identity, rank_score, row, evidence, contribution, raw_score, lane_weight in merged[:8]:
        top_witnesses.append({'id': row['id'], 'cid': row['cid'], 'rid': row['rid'],
                              'rank_before': old_rank, 'rank_after': position[row['id']],
                              'score': raw_score, 'rank_score': rank_score,
                              'lane_weight': lane_weight,
                              'base_rrf': float(row.get('rrf', 0.0)),
                              'source_lane_rank': source_rank[row['id']],
                              'source_lane_contribution': contribution,
                              'supported_features': evidence})
    digest_payload = json.dumps(support_digest_rows, ensure_ascii=False, sort_keys=True,
                                separators=(',', ':'), allow_nan=False).encode('utf-8')
    trace = {'schema': RECIPE, 'policy': SCORING_POLICY, 'lane_weights': weights,
             'applied': [r['id'] for r in rows] != [r['id'] for r in ordered],
             'reason': 'bounded_primary_source_rank_fusion', 'query_mode': mode,
             'query_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
             'query_owner_mentions': query_owners,
             'query_numeric_witnesses': numbers, 'query_color_witnesses': colors,
             'recognized_features': features,
             'relation_lane_applicable': relation_lane_applicable,
             'eligible_feature_ids': sorted(eligible_feature_ids),
             'candidate_filter': False, 'embedding_input_changed': False,
             'query_rewritten': False, 'additional_search_calls': 0,
             'source_profiles_read_only': True, 'primary_source_only': True,
             'semantic_controller_verified': False,
             'alias_label_only_support': False, 'candidate_count': len(rows),
             'candidates_with_primary_support': all_supported,
             'candidates_rankable': rankable_supported,
             'supported_candidate_scores_sha256': hashlib.sha256(digest_payload).hexdigest(),
             'candidate_order_before_sha256': _canonical_order_sha(rows),
             'candidate_order_after_sha256': _canonical_order_sha(ordered),
             'top8_source_witnesses': top_witnesses,
             'native_approval': False, 'semantic_approval': False}
    return _apply_single_property_order(ordered, text, profiles, trace,
                                        structured=False, original_rows=rows)


def order_source_relevance(rows, text, profiles, *, structured=False,
                           relation_lane_weight=DEFAULT_RELATION_LANE_WEIGHT,
                           attribute_lane_weight=ATTRIBUTE_LANE_WEIGHT):
    ordered, trace = _order_source_relevance_v6(
        rows, text, profiles, structured=structured,
        relation_lane_weight=relation_lane_weight, attribute_lane_weight=attribute_lane_weight)
    intent = _property_answers.parse_intent(text) if not structured and _query_mode(text)['kind'] == 'interrogative_property' else {}
    # Disjunction must not be converted into simultaneous bound values.
    if re.search(r'\b(?:or|either|versus|vs)\b|아니면|혹은|또는', text, re.I):
        intent = {}
    # Activate only when every recognized relation is covered by this lane.
    existing_features, _, _, query_numbers, query_colors = _query_features(text)
    mapping = {'subject_placement':'subject_placement', 'negative_space':'negative_space',
               'camera_height':'camera_viewpoint', 'stair_direction':'stair_direction',
               'frame_occupancy':'frame_occupancy', 'focus_plane':'focus_partition',
               'composition_layout':'composition_layout'}
    requested = set(intent.get('requested_features', []))
    contexts = set(intent.get('context_anchors', []))
    facets = intent.get('explicit_value_facets', {})
    def covered(feature):
        feature_id = feature['id']
        if feature_id == 'posture' and 'seated_portrait' in contexts:
            return not feature.get('value_facets') or set(feature['value_facets']) <= {'seated'}
        if (feature_id == 'subject_placement' and 'ingredient_still_life' in contexts
                and 'composition_layout' in requested and 'person' not in feature.get('owners', [])):
            return not feature.get('value_facets')
        mapped = mapping.get(feature_id)
        if mapped not in requested:
            return False
        values = set(feature.get('value_facets', []))
        if not values:
            return True
        return values <= set(facets.get(mapped, []))
    if (query_numbers or query_colors or _UNMODELED_ATTRIBUTE_CONSTRAINT.search(text)
            or re.search(r'\b(?:page|pages|page layout|grid of portraits)\b|페이지|지면', text, re.I)
            or any(not covered(feature) for feature in existing_features)):
        intent = {}
    witnesses = {}
    for row in ordered:
        compiled = profiles.get(row['id'], {}).get('property_answers')
        if compiled and intent.get('requested_features'):
            match = _property_answers.match_property_answers(intent, compiled)
            if match['complete_same_primary_source_witness']:
                witnesses[row['id']] = match
    positive = [row for row in ordered if row['id'] in witnesses]
    final = positive + [row for row in ordered if row['id'] not in witnesses]
    trace['property_answer_lane'] = {
        'schema': PROPERTY_ANSWER_RECIPE,
        'policy': PROPERTY_ANSWER_ORDERING_POLICY,
        'intent': intent, 'candidate_count': len(positive),
        'candidate_order_before_sha256': _canonical_order_sha(ordered),
        'candidate_order_after_sha256': _canonical_order_sha(final),
        'top8_witnesses': [{'id': row['id'], 'cid': row['cid'], 'rid': row['rid'],
                            'rank_after': rank, 'witness': witnesses[row['id']],
                            'primary_metadata': {p: profiles[row['id']]['primary_metadata'][p] for p in witnesses[row['id']]['common_primary_pointers']}}
                           for rank, row in enumerate(final[:8], 1) if row['id'] in witnesses],
        'candidate_filter': False, 'query_rewritten': False, 'additional_search_calls': 0,
        'native_approval': False, 'semantic_approval': False}
    previous = {item['id']: item for item in trace.get('top8_source_witnesses', [])}
    original_rank = {row['id']: rank for rank, row in enumerate(rows, 1)}
    final_witnesses = []
    for rank, row in enumerate(final[:8], 1):
        witness = witnesses.get(row['id'])
        if not witness and row['id'] not in previous:
            continue
        item = dict(previous.get(row['id'], {}))
        item.update({'id': row['id'], 'cid': row['cid'], 'rid': row['rid'],
                     'rank_before': original_rank[row['id']], 'rank_after': rank})
        item.setdefault('score', 0.0)
        item.setdefault('base_rrf', float(row.get('rrf', 0.0)))
        item.setdefault('source_lane_rank', None)
        item.setdefault('source_lane_contribution', 0.0)
        if witness:
            metadata = {p: profiles[row['id']]['primary_metadata'][p]
                        for p in witness['common_primary_pointers']}
            item['property_answer_contribution'] = 0.0
            item['property_answer_witness'] = witness
            item['primary_metadata'] = metadata
            features = list(item.get('supported_features', []))
            features.append({'feature_id': 'property_answer',
                             'support': 'direct_primary_text_and_same_selected_rid_effect',
                             'query': intent, 'source': witness, 'primary_metadata': metadata,
                             'ranking_eligible': True, 'semantic_controller_verified': False})
            item['supported_features'] = features
        final_witnesses.append(item)
    trace['top8_source_witnesses'] = final_witnesses
    support_query = (_property_answers.owned_support_query(text)
                     if not structured and _query_mode(text)['kind'] == 'interrogative_property' else {})
    if support_query and (query_numbers or query_colors or _UNMODELED_ATTRIBUTE_CONSTRAINT.search(text)
            or _ALTERNATIVE.search(text)
            or re.search(r'\b(?:left|right|raised|raising|raise|lifted|lifting|hanging|hangs|hanged|crossed|crossing)\b|왼팔|오른팔|팔.{0,12}(?:올리|들어|늘어뜨|내리|교차)', text, re.I)
            or any(feature['id'] != 'arms_position' or feature.get('value_facets')
                   for feature in existing_features)):
        support_query = {}
    support_witnesses = {}
    if support_query:
        for row in final:
            options = profiles.get(row['id'], {}).get('property_answers', {}).get('owned_support', {}).get(support_query['arm_owner'], [])
            if options: support_witnesses[row['id']] = options
    support_positive = [row for row in final if row['id'] in support_witnesses]
    before_support = final
    final = support_positive + [row for row in final if row['id'] not in support_witnesses]
    trace['owned_support_lane'] = {'schema':'photo-h-f2-owned-support-answer/v1',
        'policy':'stable-positive-same-primary-and-selected-rid-effects', 'query':support_query,
        'candidate_count':len(support_positive), 'candidate_filter':False, 'query_rewritten':False,
        'candidate_order_before_sha256':_canonical_order_sha(before_support),
        'candidate_order_after_sha256':_canonical_order_sha(final),
        'top8_witnesses':[{'id':row['id'],'cid':row['cid'],'rid':row['rid'],'rank_after':rank,
                           'witnesses':support_witnesses[row['id']]} for rank,row in enumerate(final[:8],1)
                          if row['id'] in support_witnesses],
        'native_approval':False,'semantic_approval':False}
    previous = {item['id']:item for item in trace.get('top8_source_witnesses', [])}
    updated=[]
    for rank,row in enumerate(final[:8],1):
        evidence=support_witnesses.get(row['id'])
        if not evidence and row['id'] not in previous: continue
        item=dict(previous.get(row['id'],{})); item.update({'id':row['id'],'cid':row['cid'],
            'rid':row['rid'],'rank_before':original_rank[row['id']],'rank_after':rank})
        item.setdefault('score',0.0); item.setdefault('base_rrf',float(row.get('rrf',0.0)))
        item.setdefault('source_lane_rank',None); item.setdefault('source_lane_contribution',0.0)
        if evidence:
            item['owned_support_witnesses']=evidence
            item['owned_support_contribution']=0.0
            features=list(item.get('supported_features',[]))
            features.append({'feature_id':'owned_support','support':'direct_primary_text_and_same_selected_rid_effect',
                'query':support_query,'source':evidence,'ranking_eligible':True,'semantic_controller_verified':False})
            item['supported_features']=features
        updated.append(item)
    trace['top8_source_witnesses']=updated
    trace['applied'] = [r['id'] for r in rows] != [r['id'] for r in final]
    trace['candidate_order_before_sha256'] = _canonical_order_sha(rows)
    trace['candidate_order_after_sha256'] = _canonical_order_sha(final)
    trace['candidate_order_sha256'] = _canonical_order_sha(final)
    return final, trace


def verify_source_relevance_trace(rows, text, profiles, expected_trace, *, structured=False):
    """Replay only sealed policy weights; the receipt cannot choose its scorer."""
    sealed_weights = {'relation': DEFAULT_RELATION_LANE_WEIGHT,
                      'attribute': ATTRIBUTE_LANE_WEIGHT}
    if expected_trace.get('lane_weights') != sealed_weights:
        raise ValueError('source-relevance receipt weights differ from sealed policy')
    ordered, actual = order_source_relevance(rows, text, profiles, structured=structured)
    expected_bytes = json.dumps(expected_trace, ensure_ascii=False, sort_keys=True,
                                separators=(',', ':'), allow_nan=False).encode('utf-8')
    actual_bytes = json.dumps(actual, ensure_ascii=False, sort_keys=True,
                              separators=(',', ':'), allow_nan=False).encode('utf-8')
    if expected_bytes != actual_bytes:
        raise ValueError('source-relevance receipt replay mismatch')
    return ordered, actual
