"""Build research projections only. No runtime files or indexes are written."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSET_REL = "skills/photo-prompt-image-generator/assets/"
STATUS = "PROPOSED_NOT_INTEGRATED"

FAMILIES = [
    (1, 10, "concept_context", "넓은 개념·맥락"),
    (11, 34, "face_expression", "표정·눈·입"),
    (35, 56, "hand_gesture", "손·얼굴 주변 제스처"),
    (57, 72, "body_support", "몸 자세·지지·동작"),
    (73, 90, "interaction_scene", "상호작용·상황"),
    (91, 110, "camera_light", "카메라·구도·조명"),
    (111, 124, "appearance_graphics", "조형·의복·기호"),
    (125, 132, "adult_charm_context", "성인 매력·연출 맥락"),
    (133, 140, "contrast_response", "불편함·폭력 모티프·반응의 대비"),
]
CONTEXT_NUMBERS = set(range(1, 11)) | {125, 126, 127, 128} | set(range(133, 141))
DRAFT_NUMBERS = {
    11, 14, 15, 16, 18, 19, 20, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34,
    35, 36, 37, 39, 41, 42, 43, 45, 47, 49, 50, 51, 52, 53, 54, 55, 56,
    58, 59, 60, 61, 62, 66, 67, 69, 70, 71, 72,
    73, 75, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90,
    94, 95, 97, 103, 104, 107, 108, 109, 116, 122, 124,
    128, 130, 131, 132, 135, 136,
}
HOMONYMS = {
    58: "shrug 의복과 어깨 상승 동작은 다른 의미",
    95: "flat-lay 물체 배열과 카메라의 수직 관찰 방향은 다른 축",
    97: "광대뼈 전방 돌출과 3/4 관찰 방향은 다른 축",
    107: "특정 Petzval 소용돌이 보케와 일반 초점 이탈의 질감은 범위가 다름",
}
VARIANT_HOLD = {
    29: "테헤페로의 명명된 변형과 혀끝·윙크 조합은 원저자·실제 예시의 추가 대조 후 exact alias 승격",
    35: "기존 보류 pv_finger_heart를 단순 복원하지 말고 교차형 thumb-index 변형과 금전 문맥을 새로 심사",
    36: "검지·엄지 접점은 손하트 전체의 불변 조건이 아님; 변형별 분리",
    37: "볼하트의 C형·손가락형, 접촉·투영상 연결 변형은 별도 확인",
    47: "ViVi는 명명된 사용을 확인하지만 원본 사진의 손목·손바닥·손가락 픽셀 대조는 아직 필요",
}
ALTERNATIVE_REUSES = {11, 24, 25, 31}
PARTIAL_REUSE = {18, 20, 28, 45, 47, 49, 50, 51, 53, 54, 55, 56, 59, 62, 69, 71, 76, 88, 89, 109, 131, 132}
SOURCE_ROLE = {
    "S01": "infant_experiment_not_adult_body_rule",
    "S02": "cuteness_attention_experiment_not_pose_definition",
    "S03": "facial_movement_framework_not_emotion_or_limb_definition",
    "S04": "stylized_character_construction_not_age",
    "S05": "cultural_exhibition_context_not_each_geometry_definition",
    "S06": "creator_term_scope_not_wearer_diagnosis",
    "S07": "creator_fashion_usage_not_all_pastel_definition",
    "S08": "named_product_usage_not_complete_hand_topology",
    "S09": "gesture_proposal_and_multiple_meanings",
    "S10": "creator_variant_inventory_not_review_of_all_100_shapes",
    "S11": "shot_geometry_documentation_not_image_api_guarantee",
    "S12": "projection_and_depth_relation",
    "S13": "subject_space_relation_not_all_composition_terms",
    "S14": "photographer_high_key_example_not_soft_light_equivalence",
    "S15": "lexical_meaning_not_fixed_facial_pose",
    "S16": "flirtation_meaning_not_gender_or_consent",
    "S17": "fictional_performance_usage_not_real_person_intent",
    "S18": "brand_named_adult_style_example_not_required_outfit",
    "S19": "programme_named_examples_not_population_classifier",
    "S20": "creator_brand_motif_examples_not_required_character_identity",
    "S21": "viewer_response_experiment_not_required_harm_action",
    "S22": "dictionary_meaning_not_one_visible_pose",
    "S23": "artist_expression_framework_not_medical_or_social_inference",
    "S24": "studio_named_pose_usage_not_anatomical_size_change",
    "S25": "eye_reflection_geometry_not_emotion_or_unique_light_reconstruction",
    "S26": "focus_blur_and_bokeh_optics_not_cuteness",
    "S27": "light_source_shadow_geometry_not_exposure_tone",
    "S28": "own_shoot_named_usage_geometry_pixel_review_pending",
    "S29": "hand_construction_framework_not_each_social_gesture_definition",
    "S30": "hand_foot_structure_framework_not_whole_pose_or_diagnosis",
}


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split(value):
    return [x for x in value.split(",") if x]


def family(number):
    return next((slug, title) for lo, hi, slug, title in FAMILIES if lo <= number <= hi)


def owner(extension, slot, dimension, prop, target="main_subject", profile=None, new=False):
    return {
        "candidate_file": ASSET_REL + f"photo_prompt_{extension}_extension.json",
        "candidate_slot": slot,
        "profile_file": ASSET_REL + (f"photo_prompt_visual_obligations_{profile or extension}.json" if profile or extension in {
            "pose_vocabulary", "acting_expression", "portrait_composition", "body_morphology",
            "textile_surface", "clothing_structure", "subculture_appearance", "accessory_structure",
            "motion_graphics", "color_relations",
        } else "photo_prompt_visual_obligations.json"),
        "dimension": dimension,
        "target": target,
        "property": prop,
        "file_status": "PROPOSED_NEW_OWNER_REQUIRES_GENERIC_LOADER_REGISTRATION" if new else "EXISTING_OWNER_FILE",
        "mapping_status": "PROPOSAL_REQUIRES_RUNTIME_PROPERTY_AND_LOCK_VALIDATION",
    }


def planned_mappings(n):
    if n in {1, 3, 4, 10, 128, 133, 134, 135, 136, 137}:
        result = [owner("cute_contrast", "aesthetic_trend", "style", "scene.visual_style", "scene", new=True)]
        if n == 128: result.append(owner("cute_contrast", "aesthetic_trend", "sexual_tone", "scene.requested_adult_appeal", "scene", new=True))
        if n in {3, 4}: result.append(owner("body_morphology", "silhouette_proportion", "body_geometry", "declared_object.proportion", "declared_object"))
        if n in {135, 136}: result.append(owner("motion_graphics", "composition", "composition", "declared_surface.motif_placement", "declared_surface"))
        return result
    if n in CONTEXT_NUMBERS:
        return [owner("character_moe", "action", "character_response", "scene.actor_target_response", "scene"), owner("character_moe", "action", "action", "scene.visible_action_and_consequence", "scene")]
    if n <= 34:
        result = [owner("acting_expression", "expression", "expression", "face.expression")]
        if n in {19, 21, 22, 23}: result.append(owner("pose_vocabulary", "gaze_engagement", "expression", "eyes.eyeline"))
        if n == 20: result.append(owner("lighting", "light_shape", "lighting", "lighting.eye_reflection", "scene"))
        return result
    if n <= 56:
        result = [owner("pose_vocabulary", "hand_pose", "pose", "body.hand_configuration")]
        if n in {37, 40, 41, 42, 43, 44, 52}: result.append(owner("pose_vocabulary", "contact_point", "pose", "body.contact_configuration"))
        if n == 53: result.append(owner("acting_expression", "expression", "expression", "face.expression"))
        return result
    if n <= 72:
        result = [owner("pose_vocabulary", "body_orientation" if n <= 60 else "body_pose", "pose", "head.orientation" if n == 57 else "body.configuration")]
        if n in {60, 66}: result.append(owner("pose_vocabulary", "gaze_engagement", "expression", "eyes.eyeline"))
        if n == 60: result.append(owner("acting_expression", "expression", "expression", "face.expression"))
        if n in {61, 63, 64, 65, 66, 67, 68, 70, 71, 72}: result.append(owner("pose_vocabulary", "contact_point", "pose", "body.support_configuration"))
        return result
    if n <= 90:
        result = [owner("pose_vocabulary", "relational_action" if n in {73, 74, 77, 78, 79, 80, 84} else "action", "action", "scene.actor_target_action", "scene"), owner("pose_vocabulary", "contact_point", "relationship", "scene.actor_target_contact", "scene"), owner("pose_vocabulary", "body_pose", "pose", "body.configuration")]
        if n in {75, 76, 80, 83, 84, 86, 87}: result.append({"candidate_file": ASSET_REL + "photo_prompt_tags.json", "candidate_slot": "prop", "profile_file": ASSET_REL + "photo_prompt_visual_obligations.json", "dimension": "body_geometry", "target": "declared_prop", "property": "object.configuration", "file_status": "EXISTING_OWNER_FILE", "mapping_status": "PROPOSAL_REQUIRES_RUNTIME_PROPERTY_AND_LOCK_VALIDATION", "precondition": "Bind to an already-declared or explicitly adopted object; do not add objects across count/subject/event locks."})
        if n in {82, 89}: result.append(owner("clothing_structure", "garment_detail", "appearance", "wardrobe.coverage"))
        if n in {85, 87, 88}: result.append(owner("acting_expression", "expression", "expression", "face.expression"))
        return result
    if n <= 107:
        sl = "subject_framing" if n <= 93 else "camera_height" if n in {94, 95, 96, 98} else "camera_direction" if n == 97 else "focus" if n == 107 else "composition"
        dim = "framing" if sl == "subject_framing" else "composition" if sl == "composition" else "camera"
        result = [owner("portrait_composition", sl, dim, "camera." + sl, "camera")]
        if n in {95, 104, 105, 106}: result.append(owner("portrait_composition", "composition", "composition", "scene.projection_and_viewpoint", "scene"))
        return result
    if n <= 110:
        return [owner("lighting", "light_type" if n == 108 else "light_shape" if n == 109 else "light_intensity", "lighting", "lighting.shadow_transition" if n == 108 else "lighting.eye_reflection" if n == 109 else "lighting.tone_distribution", "scene")]
    if n in {111, 112}: return [owner("body_morphology", "silhouette_proportion", "body_geometry", "declared_object.proportion", "declared_object")]
    if n == 113: return [owner("textile_surface", "surface_material", "material", "declared_object.surface", "declared_object")]
    if n == 114: return [owner("clothing_structure", "garment_detail", "appearance", "wardrobe.fit")]
    if n in {115, 116}: return [owner("subculture_appearance", "garment_detail", "appearance", "wardrobe.sleeves.hand_coverage")] + ([owner("pose_vocabulary", "hand_pose", "pose", "body.hand_configuration")] if n == 116 else [])
    if n in {117, 118}: return [owner("accessory_structure", "wearable_accessory", "appearance", "wardrobe.accessories.attachment")]
    if n == 119: return [owner("pose_vocabulary", "contact_point", "pose", "body.hand_object_contact")]
    if n == 120: return [owner("color_relations", "color", "color", "scene.palette_relation", "scene")]
    if n in {121, 122, 124}: return [owner("motion_graphics", "composition", "composition", "image.graphic_symbol_placement", "image")]
    if n == 123: return [owner("subculture_appearance", "expression", "expression", "face.symbolic_mouth")]
    result = [owner("pose_vocabulary", "body_orientation" if n in {130, 132} else "hand_pose", "pose", "body.configuration")]
    if n in {129, 130, 131}: result.append(owner("acting_expression", "expression", "expression", "face.expression"))
    return result


def evidence_mode(n):
    if n in CONTEXT_NUMBERS: return "OPTIONAL_REALIZATION_NOT_UNIVERSAL_DEFINITION"
    if n in {29, 35, 36, 37, 47}: return "NAMED_VARIANT_REVIEW_BEFORE_EXACT_ACTIVATION"
    if n in {55, 69, 70, 72, 85, 87, 139}: return "SINGLE_FRAME_STATE_TEMPORAL_CLAIMS_NOT_ESTABLISHED"
    if n in {122, 123, 124}: return "MEDIA_DEPENDENT_SYMBOLIC_FORM"
    return "DECLARED_GEOMETRY_ONLY_NOT_EMOTION_INFERENCE"


def applicability(n):
    pair = n in {73, 74, 77, 78, 79, 84}
    symbolic = n in {122, 123, 124}
    broad = n in CONTEXT_NUMBERS or n in {111, 113, 120, 121}
    return {
        "subject_domain": "declare human/animal/object/drawn character explicitly; this label alone does not select the domain" if broad else "declared articulated human or compatible drawn character; preserve current member for_any/other guards",
        "required_owners_if_variant_adopted": ["actor_A", "actor_B"] if pair else ["declared_actor_or_object", "declared_target_if_relation_requires_it"],
        "actor_count_rule": "Bind only to core-declared or explicitly adopted owners; do not introduce a partner/observer across count, subject or event locks.",
        "medium_rule": "symbolic drawn/printed/overlay form must not become real anatomy/fluid without explicit medium change" if symbolic else "resolve photograph/drawing/sculpture/print/overlay before choosing or translating the visible realization",
        "age_rule": "adult sensual context required; cute does not authorize infantilization" if n == 128 else "neutral geometry is not restricted to adult charm merely because it can be used in an adult scene; actual sexual portrayal requires declared adult context",
        "form_vs_intent": "Visible configuration does not prove emotion, health, intent, consent, identity or relationship history.",
        "variation_axes_must_be_instantiated": ["owner and target", "actor-relative side when relevant", "chosen contact or projection variant", "medium and physical/symbolic layer", "visibility and crop", "one temporal phase for a still image"],
    }


def context_case(n, row):
    if n in HOMONYMS:
        return ("homonym_context", f"원래 단어를 다른 뜻으로 정의한 요청: {HOMONYMS[n]}. 이 정의를 따라라.", "맥락이 다른 cute 단위·프로필은 활성화하지 않고 해당 뜻의 기존 후보만 검토")
    if n in {3, 4, 111, 112, 123}:
        return ("media_and_age", "성인 실사 초상이며 나이·체형·얼굴 비율은 고정. 귀여운 분위기를 원하지만 만화 데포르메는 쓰지 않는다.", "실사 신체에 데포르메·유아 비례·상징 입을 강제하지 않음")
    if n in {122, 124}:
        return ("graphic_vs_physical", "손그림 반응 기호를 요청했다. 실제 피부 홍조·눈물·땀을 새로 만들지 않는다.", "그림 기호 소유를 image 층에 유지하며 실제 체액·건강·감정 사실로 변환하지 않음")
    if n in {73, 74, 77, 78, 79, 80, 84}:
        return ("actor_target_lock", "한 사람만 있는 단독 구도를 고정했다. 파트너와의 접촉 표현은 제외한다.", "두 번째 행위자·접촉 대상을 생성하지 않고 다인 후보를 부적합 처리")
    if n in {35, 36, 37, 41, 42, 43, 44, 52, 54, 75, 76, 83, 116, 119}:
        return ("observability", "핵심 손가락·접점이 소매나 소품 뒤에 완전히 가려진 이미지로 결과를 평가한다.", "그 접점·손가락 형태는 UNOBSERVABLE; 보이지 않는 사실을 PASS로 추정하지 않음")
    if n in {125, 126, 127, 128, 131, 132}:
        return ("context_and_body_lock", "성인임을 유지하고 나이·체형·의상 노출은 고정. 요청된 매력과 귀여움의 연출만 표현한다.", "허용된 표정·자세만 바꾸며 신체 비율·노출·동의·욕망·인격을 새로 추정하지 않음")
    if n in {133, 134, 135, 136, 137, 138, 139, 140}:
        return ("meaning_override", "해당 단어를 인쇄된 장식 또는 관찰자의 반응으로 한정했다. 실제 사건과 건강 상태는 명시하지 않았다.", "요청한 매체·대비 두 층을 유지하고 실제 손상·질환·관계 이력을 덧붙이지 않음; 실제 사건 요청을 일괄 장식화하는 규칙도 만들지 않음")
    return ("definition_negation_and_lock", f"{row['label']}라는 단어는 설명에 인용했을 뿐이다. 그 예시 형태를 제외하고 기존 구도와 해당 속성을 고정한다.", "인용·부정·고정 속성이 우선; 키워드 존재만으로 hard profile 또는 optional 변화가 생기지 않음")


PIXEL_CASES = [
    ("P01", [40], "성인 한 명이 두 손을 턱 아래 꽃받침처럼 펼친 반신 사진.", ["두 손바닥 개방", "각 손에서 별도 팔로 연결", "턱 아래 좌우 프레임"], "기도 손·턱 지지와 구분"),
    ("P02", [35], "성인 한 명이 엄지와 검지를 짧게 교차한 한국식 손하트를 얼굴 옆에 둔다.", ["같은 손의 엄지·검지 교차", "나머지 손가락 경로", "교차가 읽히는 크기와 방향"], "돈을 세는 문맥·검지중지 교차 제외"),
    ("P03", [77], "성인 두 명이 각자 한쪽 팔을 써서 중앙에 공동 하트 윤곽을 만든다.", ["A와 B의 각 절반", "중앙 끝의 선택한 연결", "하나의 열린 중심과 전체 외곽"], "각자 별도 하트·세 번째 손 제외"),
    ("P04", [27], "성인 인물의 왼쪽 볼만 부풀고 오른쪽 볼은 상대적으로 평상 윤곽, 입술은 닫힌 초상.", ["행위자 왼쪽 볼 팽창", "반대 볼의 차이", "닫힌 입술"], "양 볼 팽창·영구 얼굴형 변화 제외"),
    ("P05", [15], "양쪽 눈을 감고 입꼬리를 올려 웃는 성인 초상.", ["양쪽 눈 닫힘", "올라간 양 입꼬리", "눈과 입의 동일 얼굴 소유"], "윙크·잠든 입 형태와 구분"),
    ("P06", [125], "성인 인물이 머리를 약간 돌리고도 상대 위치에 시선을 남긴 작은 미소의 코이 연출.", ["머리 회전", "머리 축과 다른 남은 홍채 방향", "요청한 상대 위치 일치"], "고개와 눈을 모두 피하는 경우와 구분"),
    ("P07", [73], "성인 A가 옆에 있는 성인 B의 소매 끝을 자기 엄지·검지로 작게 집는다.", ["A의 손과 팔", "B의 소매와 팔", "실제 집기 접점"], "자기 소매·손잡기로 대체 금지"),
    ("P08", [76], "성인 한 명이 같은 컵 몸체 양옆을 두 손으로 감싼다.", ["하나의 컵", "두 손의 실제 접점", "컵 주위 각 손가락 연결"], "한 손 손잡이 잡기·떠 있는 컵 제외"),
    ("P09", [61], "한 다리로 서고 반대 발끝은 바닥에 둔 채 그 뒤꿈치만 살짝 든 성인 전신.", ["주 지지 발 접지", "반대 발끝 접지", "반대 뒤꿈치 이격"], "양발 발돋움·발 전체 들기와 구분"),
    ("P10", [115, 116], "같은 상의의 긴 두 소매가 손 일부를 덮고 두 소매 끝이 몸 앞에 모인 성인 반신.", ["상의에서 이어지는 각 소매", "선언한 손 덮임 범위", "두 소매와 두 팔의 올바른 소유"], "장갑·분리 팔토시 제외; 가린 손가락 접촉은 평가하지 않음"),
    ("P11", [82], "담요가 성인 한 명의 몸 둘레를 연속해서 감싸고 머리와 한 손이 밖으로 보인다.", ["동일 몸 둘레 천의 연속", "겹침과 접촉", "밖으로 남은 머리·손의 소유"], "뒤에 걸린 담요·음식 부리토 제외"),
    ("P12", [95, 96], "앉은 성인과 주변 소품을 거의 수직으로 위에서 내려다본 사진. 얼굴·몸 비율은 유지한다.", ["위쪽 관찰점", "수직에 가까운 하향 축", "일관된 소품·몸의 가림 관계"], "보통 하이앵글·flat-lay 행동 별칭과 구분"),
    ("P13", [107], "성인 얼굴의 눈은 선명하고 배경의 작은 조명 점들만 초점 밖에서 둥글게 번진 초상.", ["눈과 얼굴의 해상", "배경 초점 이탈", "요청한 광점의 번진 형태"], "전체 흐림·눈 초점 상실·무조건 소용돌이 제외"),
    ("P14", [109], "성인 눈 안에 옆 위쪽 광원을 반영한 작은 반사광이 보이는 초상.", ["안구 표면 안의 반사", "선언한 위치·형태", "눈 윤곽과 홍채 보존"], "외부 별 그래픽·동공 발광 제외"),
    ("P15", [128, 132], "성인의 에로카와이 연출. 기존 체형·나이·의상은 유지하고 관능적인 자세와 귀여운 작은 손동작을 함께 보여 준다.", ["요청한 성인 관능 자세의 구체적 축", "독립된 작은 손동작", "고정 체형·나이·의상 유지"], "구체적 관능 축은 독립 core 작성 때 먼저 선언; 귀여움만 남기거나 유아화하지 않음"),
    ("P16", [135], "파스텔 의복 위에 어두운 의료·불안 상징이 인쇄된 야미카와이 패션. 살아 있는 인물의 실제 병력은 설정하지 않는다.", ["파스텔/환상 층", "독립 core가 선택한 어두운 인쇄 모티프", "같은 의복 표면에 두 층 공존"], "단순 파스텔·단순 의료품·질환 추론 제외; 용어 전체를 의료품으로 좁히지 않음"),
    ("P17", [136], "작고 둥근 봉제 조형물의 같은 천 표면에 붉은 흔적과 뼈 모양 패치가 있는 구로카와이 정물.", ["작고 둥근 봉제 형상", "요청한 붉은/뼈 모티프", "장식이 놓인 동일 천 표면"], "그로테스크·귀여움 한 층 삭제 금지; 현실 손상으로 전환하지 않음"),
    ("P18", [5], "무뚝뚝한 표정의 성인이 상대를 향해 돌아선 채 그 상대의 컵 바닥을 조심스럽게 받쳐 수평을 유지한다.", ["관찰 가능한 무뚝뚝한 표면 태도", "동일 행위자의 같은 상대를 향한 지지 행동", "손-컵 접점과 수평으로 유지된 결과"], "의복·인형·미소만으로 갭모에를 대체하지 않음; 실제 내면 성격은 판정하지 않음"),
]


def main():
    source = read("SOURCE-KEYWORDS.json")
    sources = read("SOURCES.json")
    coverage = read("EXISTING-COVERAGE.json")
    snapshot = read("CHECKOUT-SNAPSHOT.json")
    with (HERE / "ANNOTATIONS.tsv").open() as stream:
        annotations = {int(x["number"]): x for x in csv.DictReader(stream, delimiter="\t")}
    assert len(DRAFT_NUMBERS) == 78
    assert [x["number"] for x in source["entries"]] == list(range(1, 141))
    assert set(annotations) == set(range(1, 141))
    source_ids = {x["id"] for x in sources["sources"]}
    assets = {}
    candidate_by_id = defaultdict(list)
    candidate_bundles = defaultdict(list)
    profile_by_id = defaultdict(list)
    for file in snapshot["authored_source_hashes"]:
        payload = json.loads((ROOT / file).read_text())
        assets[file] = payload
        for sl, entries in payload.get("slots", {}).items():
            for entry in entries:
                guards = {key: value for key, value in entry.items() if key in {"for_any", "for_all", "exclude", "exclude_any", "incompatible_with"} or key.startswith("requires_") or key.startswith("exclude_")}
                candidate_by_id[entry["id"]].append({"file": file, "slot": sl, "id": entry["id"], "ko": entry.get("ko"), "en": entry.get("en"), "affected_dimensions": entry.get("affected_dimensions", []), "affected_properties": entry.get("affected_properties", []), "existing_applicability_guards_to_preserve": guards})
        for bundle in payload.get("visual_semantics", []):
            pids = bundle.get("hard_profile_ids", []) + ([bundle["hard_profile_id"]] if bundle.get("hard_profile_id") else [])
            for cid in bundle.get("candidate_ids", []):
                candidate_bundles[cid].append({"file": file, "bundle_id": bundle["id"], "associated_profile_ids_not_automatic_activation": pids})
        for profile in payload.get("profiles", []):
            profile_by_id[profile["id"]].append({"file": file, "id": profile["id"], "activation": profile.get("activation", {})})
    lexical = {x["number"]: x for x in coverage["rows"]}
    import sys
    sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    units, drafts, regressions = [], [], []
    for item in source["entries"]:
        n, row = item["number"], annotations[item["number"]]
        groups, sids, reuse = row["observable_groups"].split("~"), split(row["source_ids"]), split(row["reuse_ids"])
        assert len(groups) == 3 and set(sids) <= source_ids
        assert all(x in candidate_by_id for x in reuse), (n, reuse)
        mappings = planned_mappings(n)
        for mapping in mappings:
            file = mapping["candidate_file"]
            if not file.endswith("photo_prompt_cute_contrast_extension.json"):
                assert file in assets and mapping["candidate_slot"] in assets[file].get("slots", {}), (n, mapping)
            assert (ROOT / mapping["profile_file"]).exists(), mapping
            assert mapping["dimension"] in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS, mapping
        route = "CONTEXT_PATTERN" if n in CONTEXT_NUMBERS else "COMPOSE_EXISTING_ATOMS" if len(reuse) > 1 else "REUSE_WITH_BOUNDARY_REVIEW" if reuse else "NEW_VARIANT_OR_EXISTING_EQUIVALENT_SEARCH"
        if n not in CONTEXT_NUMBERS and n in ALTERNATIVE_REUSES: route = "REVIEW_ALTERNATIVE_REUSES_DO_NOT_STACK"
        elif n not in CONTEXT_NUMBERS and n in PARTIAL_REUSE and reuse: route = "PARTIAL_REUSE_NEEDS_RELATION_OR_COMPONENT"
        refs = [ref for cid in reuse for ref in candidate_by_id[cid]]
        existing_effects = list({tuple((p[k] for k in ["dimension", "target", "property"])): p for ref in refs for p in ref["affected_properties"]}.values())
        existing_dimensions = sorted({d for ref in refs for d in ref["affected_dimensions"]})
        bundles = list({(b["file"], b["bundle_id"]): b for cid in reuse for b in candidate_bundles[cid]}.values())
        pids = {pid for b in bundles for pid in b["associated_profile_ids_not_automatic_activation"]}
        profiles = [ref for pid in sorted(pids) for ref in profile_by_id[pid]]
        unit = {
            "id": f"cute_u{n:03d}_{row['slug']}", "number": n,
            "source_label": item["label"], "source_definition_unverified_input": item["prior_definition"],
            "family": family(n)[0], "research_status": STATUS,
            "interpretation_mode": evidence_mode(n),
            "applicability_and_variation_proposal": applicability(n),
            "observable_realization_proposal": {"component_groups": [{"id": f"g{i+1}", "visible_evidence": x} for i, x in enumerate(groups)], "relations": [{"id": "ownership_and_relation", "statement": row["relation_to_preserve"]}], "confusion_boundary": row["false_substitute"], "all_of_scope": "Only selected/explicitly requested realization and its declared components. Never require this example for every use of the broad label."},
            "claim_layers": {"original_vocabulary": "CONVERSATION_SOURCE_NOT_AUTHORITY", "external_sources": [{"id": sid, "scope": SOURCE_ROLE[sid]} for sid in sids], "component_relations": "AUTHOR_GEOMETRY_PROPOSAL_REQUIRES_RUNTIME_AND_NATIVE_REVIEW", "cute_effect": "HYPOTHESIS_REQUIRES_USER_PERCEPTION_VALIDATION"},
            "reuse_proposals": refs,
            "reuse_scope": "ALTERNATIVES_NOT_ALL_MEMBERS" if n in ALTERNATIVE_REUSES else "PARTIAL_COMPONENT_NOT_WHOLE_MEANING" if n in PARTIAL_REUSE else "REVIEW_EQUIVALENCE_AND_GUARDS_BEFORE_REUSE",
            "existing_runtime_effects_to_preserve": {"dimensions": existing_dimensions, "properties": existing_effects},
            "existing_bundle_refs_to_review": bundles,
            "existing_associated_profile_refs_not_activation": profiles,
            "lexical_inventory_candidate_ids": [x["id"] for x in lexical[n]["exact_positive_candidate_label_matches"]],
            "lexical_caution": HOMONYMS.get(n, "Exact label inventory is not applicability, profile exposure, selection or native pixels."),
            "planned_route": route, "planned_owner_effects": mappings,
            "promotion_conditions": ["whole-request definition, negation, medium and owner resolve first", "deduplicate by visible action/owner/material, not label", "all effect dimensions and real properties must pass current locks", "approximate retrieval stays optional", "native all-of and perception gates remain separate"] + ([VARIANT_HOLD[n]] if n in VARIANT_HOLD else []),
            "source_ids": sids,
            "regression_case_ids": [f"cute_r{n:03d}_{suffix}" for suffix in ["positive", "confounder", "context"]],
            "candidate_draft_id": f"cute_d{n:03d}_{row['slug']}" if n in DRAFT_NUMBERS else None,
        }
        units.append(unit)
        if n in DRAFT_NUMBERS:
            draft = {
                "id": unit["candidate_draft_id"], "unit_id": unit["id"], "source_number": n,
                "status": "RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA", "operation": route,
                "proposed_runtime_bundle_id": None if route in {"REUSE_WITH_BOUNDARY_REVIEW", "REVIEW_ALTERNATIVE_REUSES_DO_NOT_STACK"} else f"cute_bundle_{row['slug']}",
                "positive_surface_draft": {"ko": " / ".join(groups), "descriptive_paraphrase_ko": "이미지에 " + ", ".join(groups) + "이 같은 주체와 지정한 대상 관계로 보인다."},
                "existing_member_candidate_ids_to_review": reuse,
                "reuse_scope": unit["reuse_scope"],
                "existing_runtime_effects_to_preserve": unit["existing_runtime_effects_to_preserve"],
                "existing_bundle_refs_to_review": bundles,
                "applicability_and_variation_proposal": unit["applicability_and_variation_proposal"],
                "component_groups": unit["observable_realization_proposal"]["component_groups"],
                "relations_to_encode": [row["relation_to_preserve"]],
                "confusion_boundaries_not_positive_retrieval_text": [row["false_substitute"]],
                "proposed_owner_effects": mappings,
                "adoption": {"default": "OPTIONAL_UNORDERED_CANDIDATE", "if_selected": "all declared components and relations must be preserved", "exact_term_hardening": "only narrow source-reviewed geometry in valid request context; requester definitions/negations dominate", "broad_term": "keep realization optional and axes independent", "existing_profile_note": "Selecting an optional bundle does not itself activate its associated hard profiles."},
                "variant_review": VARIANT_HOLD.get(n, "Before promotion, review actual existing equivalents and compile under the current owner contracts."),
                "query_projection_rule": "Only reviewed positive ko/en/paraphrases/concept components. Source prose, URLs, contrast, limits, IDs and this research metadata stay outside embeddings/relevance.",
                "source_ids_evidence_only": sids,
            }
            drafts.append(draft)
        case_kind, context_request, expectation = context_case(n, item)
        regressions.extend([
            {"id": f"cute_r{n:03d}_positive", "unit_id": unit["id"], "status": "PROPOSED_NOT_RUN", "kind": "descriptive_without_cultural_label", "request": "정지 이미지에서 " + ", ".join(groups) + ". " + row["relation_to_preserve"], "expectation": "Compatible geometry may be exposed as an optional candidate; only requested/adopted components become obligations. Cultural term is not required in the query.", "candidate_id_assertion": reuse, "is_independent_holdout": False},
            {"id": f"cute_r{n:03d}_confounder", "unit_id": unit["id"], "status": "PROPOSED_NOT_RUN", "kind": "minimal_pair_wrong_form_or_relation", "counterexample": row["false_substitute"], "expectation": "Do not treat the counterexample as satisfaction of the requested selected realization; contrast text must not positively retrieve this meaning.", "evaluate_at": ["context relevance", "candidate adoption", "native component/relationship gate"]},
            {"id": f"cute_r{n:03d}_context", "unit_id": unit["id"], "status": "PROPOSED_NOT_RUN", "kind": case_kind, "request_or_review_condition": context_request, "expectation": expectation, "evaluate_at": ["frozen core", "affected property locks", "profile activation or native observability as applicable"]},
        ])
    counts = {"source_keywords": len(units), "external_primary_source_records": len(sources["sources"]), "context_patterns": len(CONTEXT_NUMBERS), "candidate_drafts": len(drafts), "regression_proposals_not_run": len(regressions), "native_case_plans_not_run": len(PIXEL_CASES)}
    write("SEMANTIC-UNITS.json", {"schema_version": "cute-research-units/v1", "status": STATUS, "counts": counts, "units": units})
    write("CANDIDATE-DRAFTS.json", {"schema_version": "cute-research-drafts/v1", "runtime_schema": False, "status": STATUS, "drafts": drafts})
    write("REGRESSION-PROPOSALS.json", {"schema_version": "cute-regression-proposals/v1", "status": "PROPOSED_NOT_RUN", "count": len(regressions), "holdout_boundary": "These proposals are derived from research annotations and are not independent holdouts. Future qualification must author a separate holdout set before reading candidate data.", "cases": regressions})
    write("RUNTIME-MAPPING.json", {"schema_version": "cute-runtime-mapping-proposals/v1", "status": "OWNERS_EXIST_PROPERTIES_PROPOSED_NOT_VALIDATED", "units": [{"unit_id": x["id"], "number": x["number"], "route": x["planned_route"], "existing_refs": x["reuse_proposals"], "proposed_effects": x["planned_owner_effects"]} for x in units]})
    write("PIXEL-QUALIFICATION-PLAN.json", {
        "schema_version": "cute-native-qualification-plan/v1", "status": "PROPOSED_NOT_RUN",
        "first_batch": "18 request cases x 2 matched image arms = 36 native images, plus 18 pack-only negative controls. Not executed or scheduled by this research.",
        "arms": {"A": "frozen pre-promotion authored data and independently frozen core", "B": "same positive request/core, promoted data; record actual exposed/selected target IDs", "C": "post-promotion pack-only control with independently frozen negation/definition/lock counter-request; not a matched third image arm"},
        "pre_core": "Author requests, meaning axes and observable obligations from human/primary meaning before candidate/research access. The seeds below are research-derived, so they cannot certify independent evaluation by themselves.",
        "evidence_chain": ["authored bytes/hash", "derived indexes/current source hash", "request/core frozen before pack", "candidate exposure", "adoption/decline and actual selected IDs", "prompt and tool arguments actually used", "original native pixels", "component and relation all-of", "human cute/contrast perception", "user acceptance"],
        "gate_policy": {"partial_is_fail": True, "required_but_occluded": "UNOBSERVABLE_NOT_PASS", "moderation_block": "BLOCKED_UNSCORED_KEEP_SEPARATE_FROM_SEMANTIC_FAILURE", "minimum_actual_case_arm_evidence": "original image, prompt, args, refs, source/index/core hashes and exposed/selected IDs", "causal_claim": "No data-improvement attribution when target data was not exposed/adopted or arms differ outside declared data changes.", "acceptance": "Pending human perception and user acceptance even if all component gates pass."},
        "cases": [{"id": cid, "source_numbers": ns, "research_seed_not_independent_core": request, "all_of_groups_for_declared_variant": gates, "boundary": boundary} for cid, ns, request, gates, boundary in PIXEL_CASES],
    })
    lines = ["# 140개 키워드 시각 의미 대조표", "", "원래 번호를 유지했다. 관찰 성분은 선택 가능한 구현안이며, 넓은 이름의 불변 정의가 아니다. `재사용`은 검토 대상인 현재 후보 ID다. 정확한 lexical hit만으로 포함·노출·선택·이미지 성공을 판단하지 않는다. 출처가 특정 형태의 직접 정의인지 관찰 프레임워크인지는 SEMANTIC-UNITS.json의 claim_layers에서 구분한다.", ""]
    for lo, hi, slug, title in FAMILIES:
        lines += [f"## {lo}–{hi}: {title}", "", "|번호·용어|관찰 성분 3개|보존할 관계|혼동·대체 실패|재사용·반영안|출처|", "|---|---|---|---|---|---|"]
        for u in units[lo-1:hi]:
            r = annotations[u["number"]]
            refs = ", ".join(split(r["reuse_ids"])) or "기존 동등 후보 재탐색 후 분리"
            if u["number"] in HOMONYMS: refs += " · " + HOMONYMS[u["number"]]
            if u["number"] in VARIANT_HOLD: refs += " · 명명 변형 검토 후 승격"
            lines.append("|" + "|".join(str(x).replace("|", "\\|").replace("\n", " ") for x in [f"{u['number']}. {u['source_label']}", r["observable_groups"].replace("~", "; "), r["relation_to_preserve"], r["false_substitute"], refs + " / " + u["planned_route"], " ".join(f"[{sid}](SOURCES.md#{sid.lower()})" for sid in u["source_ids"])]) + "|")
        lines.append("")
    (HERE / "MATRIX.md").write_text("\n".join(lines) + "\n")
    ledger = ["# 출처와 주장 범위", "", "2026-10-05 KST 확인. 30건은 실험 논문, 공식 기술 설명, 사전, 창작자 본인의 설명·작업·상품 사례다. 각각의 근거 범위는 다르다. 본문 열람·검색 초록·검색 사전 항목의 확인 상태를 분리했다. 외형의 귀여움, 의도, 동의, 건강 상태를 보편적으로 판정하는 출처로 취급하지 않는다.", ""]
    for s in sources["sources"]:
        ledger += [f"## {s['id']}", "", f"[{s['title']}]({s['url']})", "", f"- 유형: `{s['evidence_type']}`", f"- 확인 상태: `{s['verification']}`", f"- 뒷받침하는 범위: {s['supports']}", f"- 주장 한계: {s['claim_limit']}", ""]
        if s.get("supporting_url"): ledger += [f"- 추가로 읽은 [관련 사전 항목]({s['supporting_url']})", ""]
    ledger += ["## 사용하지 않은 근거·남은 출처 조건", ""]
    ledger += [f"- [{r['status']}]({r['url']})" for r in sources["unavailable_references"]]
    ledger += ["", "테헤페로의 원저자 원문을 본문까지 읽지 못했다. 갸루피스는 촬영 주체의 명명된 용례를 확인했지만 사진 픽셀의 손목·손바닥 방향을 대조하지 않았다. 이 용어들의 세부 변형을 자동 hard alias로 승격하지 않는다. 손하트 100변형 모두를 검토했다고 주장하지 않는다. FACS는 얼굴 움직임의 분석 프레임워크이며 손·다리 형태나 감정의 정답표가 아니다.", ""]
    (HERE / "SOURCES.md").write_text("\n".join(ledger))
    drift = [file for file, expected in snapshot["authored_source_hashes"].items() if digest(ROOT / file) != expected]
    checks = {
        "source_numbers_1_to_140_unique": len(units) == len({u["number"] for u in units}) == 140,
        "annotations_one_to_one": len(annotations) == 140,
        "all_source_ids_resolve": all(set(u["source_ids"]) <= source_ids for u in units),
        "all_reuse_candidate_ids_resolve_in_current_authored_files": all(r["id"] in candidate_by_id for u in units for r in u["reuse_proposals"]),
        "existing_owner_files_slots_and_profile_files_resolve": True,
        "proposed_dimension_names_in_current_contract_vocabulary": True,
        "candidate_draft_count_78": len(drafts) == 78,
        "regression_count_420_three_per_unit": len(regressions) == 420,
        "pixel_plan_count_18": len(PIXEL_CASES) == 18,
        "positive_draft_projection_has_no_source_url_or_provenance": all("http" not in json.dumps(d["positive_surface_draft"], ensure_ascii=False) for d in drafts),
        "all_drafts_marked_non_runtime": all(d["status"] == "RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA" for d in drafts),
    }
    assert all(checks.values()), checks
    write("VALIDATION.json", {"schema_version": "cute-research-validation/v1", "status": "STRUCTURAL_RESEARCH_PACKAGE_PASS", "counts": counts, "checks": checks, "snapshot_authored_file_drift": drift, "verification_boundary": {"research_structure": "PASS", "runtime_property_schema_and_lock_compatibility": "NOT_RUN", "generated_index_rebuild": "NOT_RUN", "regressions": "PROPOSED_NOT_RUN", "pack_exposure_selection": "NOT_RUN", "native_pixels": "NOT_RUN", "cute_perception": "NOT_EVALUATED", "user_acceptance": "PENDING"}})
    manifest_names = sorted(x.name for x in HERE.iterdir() if x.is_file() and x.name != "MANIFEST.json")
    write("MANIFEST.json", {"schema_version": "cute-research-manifest/v1", "files": [{"name": name, "sha256": digest(HERE / name), "bytes": (HERE / name).stat().st_size} for name in manifest_names], "counts": counts, "status": "RESEARCH_ONLY"})
    print(json.dumps({"status": "STRUCTURAL_RESEARCH_PACKAGE_PASS", "counts": counts, "authored_file_drift": drift}, ensure_ascii=False))


if __name__ == "__main__":
    main()
