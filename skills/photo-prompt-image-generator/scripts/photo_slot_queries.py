"""Post-freeze, candidate-free role queries and immutable provider contexts."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import photo_candidate_corpus as c
from photo_embedding_provider import embed, SPACE, validate_vector
from photo_frozen_query import HASH

RECIPE = 'photo-independent-slot-query/v1'
SCHEMA = 'photo-slot-query-set/v1'
_KO = '''medium=사진 매체;genre=사진 장르;subject=주체;person_origin=인물의 외관 배경;appearance_type=외모 유형;hair_style=머리 형태;hair_color=머리 색;makeup_style=화장 스타일;expression=표정;costume_style=복식 스타일;wardrobe_style=의복 스타일;adult_context=성인 상황 맥락;action=행동;capture_context=촬영 상황;prop=소품;fetish_styling=페티시 표현;caption_context=사진의 상황 의미;location=장소;world=세계 환경;lighting=조명;light_direction=빛 방향;light_type=빛 종류;light_intensity=빛 강도;light_shape=빛 형태;camera_type=카메라 방식;camera_direction=카메라 방향;composition=구도;subject_framing=주체 프레이밍;body_framing=몸 프레이밍;lens=렌즈;focus=초점;motion=움직임;color=색;mood=정서;surreal_concept=초현실 개념;surreal_anchor=초현실의 현실 기준;scale_relation=크기 관계;surreal_physics_detail=초현실 물리 상태;texture=질감;format=화면 형식;quality=시각 품질;film_emulation=필름 표현;weather=날씨;time_of_day=시간대;wearable_accessory=착용 액세서리;facial_hair=수염;surface_material=표면 재질;aesthetic_trend=미적 경향;relational_action=관계 행동;prop_direction=소품 방향;partner_role=상대 역할;partner_framing=상대 프레이밍;gaze_target=시선 대상;body_orientation=몸 방향;proxemics=인물 간 거리;contact_point=접촉 지점;intent_state=의도 상태;emotional_contradiction=감정 모순;viewer_position=관찰자 위치;narrative_phase=이야기의 시점;species_marker=종의 특징;transition_stage=변화 단계;procedure_step=절차 단계;duty_prop_state=작업 소품 상태;social_cue=사회적 단서;reflection_logic=반사 관계;camera_height=카메라 높이;distance_narrative=거리의 서사 의미;sensory_focus=감각적 초점;frame_anchor_medium=화면 기준 매체;face_shape_relation=얼굴 형태 관계;anatomical_connection=신체 연결;body_evidence_region=신체의 관찰 영역;aftermath_trace=행동 이후 흔적;apparatus_pov=장치 관점;complexion_coverage=피부 화장 범위;brow_style=눈썹 형태;lip_finish=입술 표면;eyeshadow_style=아이섀도;eye_makeup_line=눈 화장 선;lash_style=속눈썹;cheek_makeup=볼 화장;face_sculpting=얼굴 명암;lip_color_placement=입술 색 위치;makeup_decoration=화장 장식;makeup_wear_state=화장의 시간 상태;skin_finish=피부 표면 표현;eye_detail=눈 세부;body_marking=몸의 표식;lens_artifact=렌즈 흔적;gaze_engagement=시선의 관계;hand_pose=손 자세;skin_condition=피부 상태;ambient_particle=공중 입자;grain_profile=입자감;garment_detail=의복 세부;companion_animal=동반 동물;color_grading=색 보정;footwear=신발;silhouette_proportion=실루엣 비례;space_condition=공간 상태;crowd_density=군중 밀도;situation_context=상황 맥락;occasion_context=행사 맥락;body_pose=몸 자세;shot_scale=촬영 거리;platform_framing=화면 사용 목적;narrative_core=이야기의 중심;concept_tension=개념의 긴장;atmosphere=분위기;material=재질;capture_mode=촬영 방식'''
KO = dict(row.split('=', 1) for row in _KO.split(';'))


def specification(catalog, slot):
    if slot not in catalog or slot not in KO:
        raise ValueError('unknown managed slot: ' + slot)
    row = catalog[slot]
    return {'recipe': RECIPE, 'slot_id': slot, 'focus_en': row['description'],
            'focus_ko': KO[slot], 'dimensions': row['dimensions'],
            'applicability': row['applicability'], 'search_scope': 'whole_shared_positive_corpus'}


def inputs(core, controls, catalog, slot, language='en'):
    import prompt_generator as g
    if language not in {'en', 'ko'}:
        raise ValueError('unsupported slot query language')
    spec = specification(catalog, slot)
    global_text, _ = g.authorial_core_retrieval_text(core)
    projection, fields = g.candidate_pack_slot_focus_text(core, slot)
    focus = spec['focus_' + language] + (': ' + projection if projection else '')
    lexical = {'global_context': global_text, 'slot_focus': focus}
    text = global_text + '\nPhotographic role: ' + focus
    binding = {'recipe': RECIPE, 'slot_id': slot, 'slot_spec_sha256': c.digest(spec),
               'core_sha256': core['canonical_sha256'], 'controls_sha256': controls['canonical_sha256'],
               'language': language, 'query_fields': lexical, 'focus_fields': fields}
    if not global_text.strip() or any(not HASH.fullmatch(v) for v in (core['canonical_sha256'], controls['canonical_sha256'])):
        raise ValueError('slot queries require frozen core and controls')
    return text, lexical, binding


def context(core, controls, catalog, slot, cache, language='en'):
    text, fields, binding = inputs(core, controls, catalog, slot, language)
    row = embed(text, binding, cache)
    value = {'schema': 'photo-slot-query-vector/v1', 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
             'binding': binding, 'space': SPACE, 'vector': row['vector'], 'vector_sha256': row['vector_sha256'],
             'execution': row['execution'], 'cache_hit': row['cache_hit']}
    value['canonical_sha256'] = c.digest(value)
    return value


def validate(row, core, controls, catalog, slot):
    language = (row.get('binding') or {}).get('language') if isinstance(row, dict) else None
    text, fields, binding = inputs(core, controls, catalog, slot, language)
    if (row.get('schema') != 'photo-slot-query-vector/v1' or row.get('binding') != binding
            or row.get('space') != SPACE or row.get('text') != text
            or row.get('text_sha256') != hashlib.sha256(text.encode()).hexdigest()
            or row.get('vector_sha256') != c.digest(row.get('vector'))
            or row.get('canonical_sha256') != c.digest({k:v for k,v in row.items() if k != 'canonical_sha256'})):
        raise ValueError('foreign or modified independent slot query')
    validate_vector(row.get('vector'))
    trace = row.get('execution') or {}
    if trace.get('provider_executed') is not True or trace.get('http_status') != 200 or not HASH.fullmatch(trace.get('response_sha256', '')):
        raise ValueError('slot query lacks successful provider evidence')
    return fields


def prepare(core, controls, catalog, slots, cache, *, workers=4, language='en'):
    slots = sorted(set(slots))
    with ThreadPoolExecutor(max_workers=max(1, min(8, workers))) as pool:
        rows = list(pool.map(lambda slot: context(core, controls, catalog, slot, cache, language), slots))
    value = {'schema': SCHEMA, 'slots': dict(zip(slots, rows))}
    value['canonical_sha256'] = c.digest(value)
    return value


def validate_set(value, core, controls, catalog, slots):
    if not isinstance(value, dict) or value.get('schema') != SCHEMA or set(value.get('slots', {})) != set(slots):
        raise ValueError('exact independent slot query set required')
    if value.get('canonical_sha256') != c.digest({k:v for k,v in value.items() if k != 'canonical_sha256'}):
        raise ValueError('slot query set checksum mismatch')
    return {slot: validate(value['slots'][slot], core, controls, catalog, slot) for slot in sorted(slots)}
