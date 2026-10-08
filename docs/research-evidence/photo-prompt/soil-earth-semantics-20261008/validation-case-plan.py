"""Author future regression and render cases. No case is executed here."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

# Regression canaries, authored after the research drafts. They are not a
# blind holdout and cannot establish runtime quality before implementation.
SENSE_PAIRS = [
    ("soil_texture", "식토의 모래·실트·점토 비율을 설명하는 토양 단면", "흙을 먹는 식토 행위를 설명하는 장면", ["E003", "E114"]),
    ("plasticity_firing", "손으로 누른 점토에 접힌 모양이 남아 있는 소성", "그릇을 가마 안에서 열처리하는 소성", ["E014", "E095"]),
    ("earth_fort", "토성 삼각형에서 점토 비율이 높은 영역", "흙으로 쌓은 토성과 그 옆의 마른 해자", ["E003", "E092"]),
    ("archipelago_saber", "물에 둘러싸인 여러 섬으로 이루어진 군도", "장교가 허리에 찬 군도", ["E055"]),
    ("burial_store", "유물을 층위 속 원래 위치에 보존한 매장", "생활용품을 판매하는 매장", ["E099", "E100"]),
    ("burial_resource", "장례용 매장 공간을 흙으로 덮은 봉분", "광물 자원이 지하에 매장된 지질 단면", ["E073", "E100"]),
    ("construction_earth", "건물이 서 있는 대지의 경계", "끝없이 펼쳐진 대지의 풍경", ["E001"]),
    ("earth_color_origin", "황토색 재킷을 입은 인물", "바람에 운반된 실트가 쌓인 뢰스 절벽", ["E021", "E061"]),
    ("soil_crust_crust", "지표 위의 얇은 생물 토양 피각", "대륙지각과 해양지각을 나타내는 단면", ["E075", "E071"]),
    ("porcelain_self", "유약 경계가 드러나는 자기 그릇", "자기 자신을 돌아보는 인물", ["E096"]),
    ("stoneware_tool", "가마에 소성한 석기 그릇", "돌을 깎아 만든 석기 도구", ["E096", "E072"]),
    ("mud_play_fetish", "비성적인 진흙놀이에서 흙을 만지는 손", "머드 페티시라는 명시된 취향 문맥", ["E109", "E111", "E112"]),
    ("land_ritual_resign", "땅과 곡식에 관한 사직 의례", "직장에서 사직하는 사람", ["E105"]),
    ("sand_mineral", "석영을 포함하지 않은 모래 표본", "모래가 아니라 큰 석영 결정 표본", ["E002", "E072"]),
    ("cracks_frozen", "건조한 진흙 판을 둘러싼 건열", "지중 얼음 쐐기와 연결된 동토 다각형", ["E012", "E068"]),
    ("contingent_class", "검은 흙이 보이는 일반 숲바닥", "조사로 분류된 체르노젬의 단면", ["E017", "E022"]),
]

RELATION_PAIRS = [
    ("E010", "발이 진흙에 눌리고 바로 옆에 같은 밑창 자국과 밀려난 흙이 보인다.", "발은 바닥 위에 떠 있고 전혀 다른 바닥에 발자국만 보인다."),
    ("E109", "팔의 원래 피부와 두꺼운 진흙 경계가 보이고 그 경계를 손가락이 쓸어낸 자국이 있다.", "진흙은 배경 바닥에만 있고 팔에는 흙색 조명만 비친다."),
    ("E110", "불투명 바지 밑단에 도톰한 진흙이 붙고 깨끗한 천과 부착물 경계가 보인다.", "바지는 깨끗하고 뒤의 흙바닥만 젖어 있다."),
    ("E016", "지표부터 아래까지 연속 단면에 불규칙한 층 경계와 같은 위치의 깊이 척도가 보인다.", "벽지에 갈색 줄무늬를 인쇄하고 옆에 자만 놓는다."),
    ("E086", "굽지 않은 흙벽돌이 엇갈린 단으로 쌓이고 흙 줄눈과 깨진 모서리가 보인다.", "연속 판축벽에 벽돌 줄눈을 페인트로 그린다."),
    ("E089", "같은 깨진 패널의 엮은 나뭇가지에 흙 채움이 붙어 있다.", "엮은 나뭇가지 소품과 별개의 갈색 벽이 나란히 서 있다."),
    ("E036", "사면의 작은 홈이 아래로 갈라져 이어지고 출구 아래에 퇴적물이 있다.", "타이어 무늬가 반복되는 평평한 흙길이다."),
    ("E038", "파인 하안에서 뿌리가 나오고 그 하안 바로 아래에 떨어진 흙덩이가 있다.", "공중에 매단 끈을 강변 앞에 배치한다."),
    ("E050", "좁은 산지 물길이 출구에서 넓어지며 선상 퇴적체를 만든다.", "바다로 들어가는 하천 끝에 갈라지는 물길이 있다."),
    ("E055", "큰 두 육지를 연결하는 좁은 땅의 양옆에 물이 있다.", "물속에서 분리되어 있는 섬 두 개 사이의 좁은 해협이다."),
    ("E056", "모래 띠가 육지와 떨어진 섬 양끝을 실제로 이어 준다.", "모래 띠는 육지 쪽 끝만 붙어 있고 섬 앞에서 끊긴다."),
    ("E065", "종유석은 천장에, 석순은 바닥에 붙고 별도 석주는 양쪽을 연결한다.", "바닥의 뾰족한 돌만을 종유석이라고 부른다."),
    ("E007", "바퀴와 마른 흙의 접촉점에서 먼지가 시작해 같은 장면으로 퍼진다.", "정지한 흙바닥 앞에 출처가 없는 안개만 보인다."),
    ("E115", "달 문맥의 회색 레골리스에 선명한 밑창 자국과 작은 각진 암편이 있다.", "회색 아스팔트 위에 바람에 날리는 안개를 넣는다."),
]

CONTEXT_CASES = [
    ("E032", "검은 흙만 보고 토양 pH를 7이라고 정해 달라.", "retain_unknown_measurement; no_visual_diagnosis"),
    ("E022", "검은 표토가 보이되 토양 이름은 알 수 없는 풍경.", "no_Chernozem_classification_from_color"),
    ("E027", "회색 흙과 녹슨 점이 보이지만 조사 자료는 없다.", "describe_mottles_only; no_Gleysol_or_pollution_diagnosis"),
    ("E028", "흙 위의 흰 피막은 소금인지 페인트인지 확실하지 않다.", "retain_ambiguous_material; no_salt_identity"),
    ("E034", "지하수의 흐름을 일반 지상 사진으로 찍은 장면.", "no_automatic_cutaway_or_giant_underground_lake"),
    ("E068", "겨울 눈 덮인 땅의 사진만 있다.", "no_two_year_permafrost_claim"),
    ("E095", "구운 적갈색 그릇 하나만 보이는 사진.", "no_temperature_or_firing_duration_claim"),
    ("E103", "평범한 흙무더기만 보고 암매장지라고 판단해 달라.", "no_crime_or_concealment_inference"),
    ("E112", "비성적인 머드팩 사진.", "no_fetish_or_arousal_inference"),
    ("E113", "페트리코 냄새가 나는 비 온 뒤의 정원.", "retain_olfactory_context; no_smoke_or_visible_odor_requirement"),
    ("E119", "고향에 뿌리내린 느낌의 평범한 가족 사진.", "no_literal_roots_growing_from_people"),
    ("E120", "희망을 상징하는 흙 장면이되 식물은 추가하지 않는다.", "preserve_negated_plant_lock; optional_bridge_not_recipe"),
]

LOCK_CASES = [
    ("E010", "pose", "main_subject", "foot", "block_pose_change"),
    ("E109", "pose", "main_subject", "hand", "block_added_hand_contact"),
    ("E109", "appearance", "main_subject", "skin", "block_skin_coating"),
    ("E110", "appearance", "main_subject", "wardrobe", "block_garment_deposit"),
    ("E110", "appearance", "main_subject", "wardrobe.optical_transmission", "surface_deposit_may_remain_eligible; never_add_transparency"),
    ("E007", "atmosphere", "scene_particles", "source_and_distribution", "block_added_dust"),
    ("E108", "concept", "selected_terrain", "fictional_physics", "block_unrequested_surreal_physics"),
    ("E016", "setting", "selected_terrain", "spatial_structure", "block_automatic_soil_cut"),
]

RENDER_CASES = [
    ("R01", ["E010", "E008"], "발과 진흙의 접촉", "부츠·눌린 같은 바닥·맞는 밑창 자국·밀려난 흙을 같은 프레임에 둔다.", ["contact", "same_surface", "material_boundary"]),
    ("R02", ["E109"], "피부의 진흙 피막", "맨피부·붙은 진흙·손가락 자국이 모두 보이는 근접 장면.", ["correct_owner", "thickness", "contact_track"]),
    ("R03", ["E110"], "불투명 의복의 진흙", "봉제선·국소 진흙덩이·깨끗한 천 경계. 옷은 불투명하게 유지.", ["wardrobe_lock", "solid_deposit", "same_garment"]),
    ("R04", ["E016", "E019"], "토양 단면", "표면·불규칙한 흙 띠·기반암 접촉·깊이 척도를 같은 절개에서 확인.", ["vertical_continuity", "boundary", "bedrock"]),
    ("R05", ["E012"], "건열과 균열판", "연결된 다각형 균열과 둘러싸인 마른 판이 같은 지표에 반복됨.", ["closed_network", "bounded_plates", "no_ice_substitute"]),
    ("R06", ["E036", "E038"], "작은 침식 홈과 하안", "세류와 하안은 각각 장면 변형으로 나눠 생성; 크기·뿌리·퇴적 관계를 확인.", ["scale", "downhill_relation", "root_attachment"]),
    ("R07", ["E086", "E088", "E089"], "흙건축 재료 구별", "어도비·판축·와틀 도브를 별개 이미지로 비교. 같은 갈색 표면으로 채점하지 않음.", ["brick_vs_lift", "woven_support", "material_contact"]),
    ("R08", ["E055", "E056"], "육지 연결 위상", "지협과 육계사주를 별개 공중 시점으로 확인; 양끝 연결과 양옆 물을 확인.", ["connection_topology", "both_endpoints", "same_water_plane"]),
    ("R09", ["E065"], "동굴 부착 방향", "천장 부착 종유석·바닥 부착 석순·양쪽 연결 석주를 같은 동굴에서 확인.", ["attachment_direction", "continuous_column", "rock_not_ice"]),
    ("R10", ["E115"], "달 표면 흔적", "달 문맥을 별도 고정하고 부츠 자국·입자·각진 암편을 근접 확인.", ["same_substrate", "vacuum_context", "no_airborne_haze"]),
    ("R11", ["E107"], "흙 골렘", "기존 골렘의 몸체·관절·작용 결과를 유지하면서 선택한 흙 재질을 확인.", ["material_continuity", "joint_connection", "task_consequence"]),
    ("R12", ["E108"], "허구 지층의 분리", "흙덩이와 지면 사이의 공기 틈, 아래쪽 노출 지층과 매달린 뿌리를 확인.", ["air_gap", "underside", "root_owner"]),
]


def main():
    cases = []
    for name, a, b, ids in SENSE_PAIRS:
        for suffix, text, other in [("a", a, b), ("b", b, a)]:
            cases.append(dict(id="sense_" + name + "_" + suffix, family="sense_disambiguation",
                              request_ko=text, counterexample_ko=other, research_unit_ids=ids,
                              expectation="resolve_contextual_sense; never activate all group recipes"))
    for uid, positive, negative in RELATION_PAIRS:
        cases.extend([
            dict(id="relation_" + uid + "_positive", family="owner_relation",
                 request_ko=positive, research_unit_ids=[uid],
                 expectation="offer_only_the_complete_owned_realization_when_scope_is_open"),
            dict(id="relation_" + uid + "_negative", family="owner_relation",
                 request_ko=negative, research_unit_ids=[uid],
                 expectation="do_not_assert_the_target_relation"),
        ])
    for i, (uid, text, expectation) in enumerate(CONTEXT_CASES, 1):
        cases.append(dict(id=f"context_{i:02d}", family="nonvisual_and_negation", research_unit_ids=[uid],
                          request_ko=text, expectation=expectation))
    for i, (uid, dimension, target, prop, expectation) in enumerate(LOCK_CASES, 1):
        cases.append(dict(id=f"lock_{i:02d}", family="scope_and_property_lock", research_unit_ids=[uid],
                          lock=dict(dimension=dimension, target=target, property=prop), expectation=expectation))
    renders = [dict(id=i, research_unit_ids=u, title_ko=t, framing_ko=f, gates=g,
                    execution_status="planned_not_rendered", scoring="all_required_gates_pass; partial_is_fail")
               for i, u, t, f, g in RENDER_CASES]
    payload = dict(schema_version="soil-earth-validation-case-plan/v1",
                   status="research_canaries_authored; runtime_and_render_execution_not_performed",
                   independence="Author saw the drafts. These are regression canaries, not a blind holdout. Commission independent paraphrases before release evaluation.",
                   regression_cases=cases, render_scenario_families=renders)
    (OUT / "validation-case-plan.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"planned_regression_cases": len(cases), "render_scenario_families": len(renders)}))


if __name__ == "__main__":
    main()
