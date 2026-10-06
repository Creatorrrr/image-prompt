#!/usr/bin/env python3
"""Build reviewable research artifacts; never edits runtime assets or indexes."""
from __future__ import annotations
import csv, hashlib, json, re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
STATUS = "RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA"
def load(name):
    return json.loads((OUT / name).read_text())
def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
def split(value):
    return [s.strip() for s in value.split(",") if s.strip()]

FAMILY_FILES = {
    "garment": ("photo_prompt_visual_obligations_clothing_structure.json", "photo_prompt_clothing_structure_extension.json"),
    "accessory": ("photo_prompt_visual_obligations_accessory_structure.json", "photo_prompt_accessory_structure_extension.json"),
    "hair": ("photo_prompt_visual_obligations_subculture_appearance.json", "photo_prompt_subculture_appearance_extension.json"),
    "skin": ("photo_prompt_visual_obligations_body_morphology.json", "photo_prompt_body_morphology_extension.json"),
    "face": ("photo_prompt_visual_obligations_subculture_appearance.json", "photo_prompt_subculture_appearance_extension.json"),
    "material": ("photo_prompt_visual_obligations_textile_surface.json", "photo_prompt_textile_surface_extension.json"),
    "prosthesis": ("photo_prompt_visual_obligations_body_morphology.json", "photo_prompt_body_morphology_extension.json"),
    "creature": ("photo_prompt_visual_obligations_character_appearance.json", "photo_prompt_character_appearance_extension.json"),
    "body_scale": ("photo_prompt_visual_obligations_character_appearance.json", "photo_prompt_research_extension.json"),
    "pose": ("photo_prompt_visual_obligations_pose_vocabulary.json", "photo_prompt_pose_vocabulary_extension.json"),
    "expression": ("photo_prompt_visual_obligations_subculture_appearance.json", "photo_prompt_subculture_appearance_extension.json"),
    "prop": ("photo_prompt_visual_obligations_accessory_structure.json", "photo_prompt_research_extension.json"),
    "marking": ("photo_prompt_visual_obligations_subculture_appearance.json", "photo_prompt_subculture_appearance_extension.json"),
    "representation": ("photo_prompt_visual_obligations_character_appearance.json", "photo_prompt_character_appearance_extension.json"),
    "interaction": ("photo_prompt_visual_obligations_character_appearance.json", "photo_prompt_character_appearance_extension.json"),
}
# These are morphological relation drafts, independent from canonical character claims.
EDGES = {
 "H002": [("shirt","inside","knit"),("tie","in_front_of","shirt"),("tie","passes_below","knit_neckline"),("knit","inside","outer_robe")],
 "H003": [("hood","attached_at","robe_neckline"),("inside_colour","on","hood_inside"),("fold_edge","separates","hood_inside_and_outside")],
 "H004": [("diagonal_bands","bounded_by","tie_surface"),("tie_knot","continuous_with","tie_blade")],
 "H005": [("contrast_band","follows","knit_neck_or_cuff_edge")],
 "H006": [("small_emblem","localized_on","selected_garment_chest_panel")],
 "H008": [("tapered_crown","rises_from","brim"),("brim","encircles","crown_base"),("hat","rests_above","wearer_head")],
 "H009": [("capelet","covers","wearer_shoulders"),("capelet_hem","ends_above","wearer_elbows"),("lower_garment","continues_below","capelet_hem")],
 "H016": [("glove","encloses","selected_hand"),("other_hand","outside","glove"),("glove_cuff","terminates_at","selected_wrist")],
 "H027": [("three_tiers","part_of","same_short_dress"),("tier_edges","project_from","wearer_body"),("each_tier","retains","separate_free_edge")],
 "H028": [("bird_motif_a","on","same_bodice"),("bird_motif_b","on","same_bodice"),("inward_curves","jointly_outline","heart")],
 "H043": [("dark_region","on","selected_crown_or_front_roll"),("light_region","on","selected_side_or_lower_hair"),("both_regions","part_of","one_hairstyle")],
 "H048": [("left_rim","encloses","left_eye_region_lens"),("right_rim","encloses","right_eye_region_lens"),("nose_bridge","joins","same_two_rims")],
 "H050": [("lens","bounds","magnified_eye_projection"),("adjacent_face","outside","lens_boundary")],
 "H058": [("angular_scar_path","localized_on","forehead_skin"),("successive_bends","continuous_with","same_path")],
 "H061": [("artificial_eye","occupies","selected_orbit"),("housing","supports","same_artificial_eye"),("ordinary_other_eye","separate_from","replacement")],
 "H062": [("socket","meets","same_residual_limb_endpoint"),("prosthetic_segment","continues_from","socket"),("segment","reaches_toward","support_plane")],
 "H063": [("replacement_hand","continues_from","same_forearm_endpoint"),("replacement_fingers","part_of","replacement_hand"),("metal_like_reflection","on","replacement_surface")],
 "H064": [("nostril_openings","on","same_flattened_facial_surface"),("altered_nose_region","continuous_with","head")],
 "H065": [("skull_motif","on","forearm_skin"),("serpent_path","emerges_from","skull_mouth"),("serpent_path","on","same_forearm_skin")],
 "H066": [("background_features","visible_through","figure_interior"),("figure_contour","bounds","same_translucent_region")],
 "H067": [("hood","covers","head_region"),("long_cloth","continues_from","hood"),("lowest_figure_contour","separated_from","support_plane_if_floating_selected")],
 "H069": [("whiskers","emerge_from","transformed_muzzle"),("ears","join","transformed_head"),("fur","continuous_with","transformed_face_surface")],
 "H070": [("two_ear_bases","connected_to","same_nonhuman_head"),("inner_panels","inside","their_own_ear_contours")],
 "H071": [("human_torso","joined_at","equine_torso_junction"),("four_horse_legs","part_of","equine_lower_body"),("equine_tail","connected_to","same_hindquarters")],
 "H072": [("avian_forequarters","joined_to","same_hybrid_torso"),("paired_wings","connected_to","torso"),("equine_hindquarters","continuous_with","same_hybrid_torso")],
 "H074": [("eight_legs","connected_to","same_arachnid_body"),("hair","on","same_creature_surface")],
 "H075": [("mask","separate_from","face"),("apertures","through","same_mask"),("mask_perimeter","bounds","selected_face_coverage")],
 "H076": [("incisions","on","mask_solid_surface"),("eye_apertures","through","mask"),("solid_ground","between","incised_motif_lines")],
 "H077": [("hourglass","inside","pendant_centre"),("rings","encircle","hourglass"),("chain","attached_to","same_pendant")],
 "H078": [("cord","holds","several_cork_plugs"),("cord","forms","neck_loop")],
 "H079": [("root_fruit_pendant","hangs_from","ear_attachment"),("leaf_like_top","part_of","same_ornament")],
 "H082": [("lion_head_object","rests_above","human_head"),("mane","surrounds","object_face"),("wearer_head","distinct_from","hat_object")],
 "H083": [("beads","on","pouch_surface"),("handle_or_drawcord","attached_to","same_pouch"),("pouch_mouth","bounds","pouch_opening")],
 "H086": [("same_hand_fingers","in_contact_with","prop_handle"),("handle","continuous_with","shaft"),("shaft","continuous_to","prop_tip")],
 "H087": [("ring","connected_to","declared_ear"),("closed_ring_contour","separate_from","hair_loops")],
 "H093": [("upper_lids","overlap","their_irises"),("one_mouth_corner","higher_than","other_corner"),("eye_and_mouth_actions","co_owned_by","same_face")],
 "H094": [("two_forearms","cross_in_front_of","same_torso"),("each_hand","continuous_with","its_own_forearm")],
 "H095": [("each_prop","held_by","declared_holder"),("each_gaze","directed_at","declared_target"),("participant_a","separate_from","participant_b")],
 "H102": [("shaped_fabric_piece","over","ground_cloth"),("specified_stitching","joins","piece_to_ground_if_requested")],
 "H103": [("cord","crosses_between","paired_eyelet_rows"),("cord","passes_through","declared_eyelets"),("both_rows","part_of","same_garment")],
 "H106": [("hair","gathers_at","tie_point"),("ribbon_knot","attached_at","same_tie_point"),("ribbon_tails","separate_from","hair_bundle")],
 "H108": [("dark_colour","inside","nail_plate_boundary"),("nail_plate","on","same_connected_finger")],
 "H109": [("overlapping_bands","wrap","declared_head"),("free_end","descends_toward","shoulder")],
 "H112": [("broad_sleeve_openings","part_of","large_outer_cloth_body"),("loose_trousers","inside_or_below","same_outer_garment")],
 "H115": [("head_and_arm_openings","bounded_by","same_simple_cloth"),("cloth_body","separate_covering_on","nonhuman_torso")],
 "H118": [("strap","joins","artificial_eye_housing"),("strap","follows","selected_head_region"),("skin","separate_from","strap")],
 "H119": [("each_head_or_mask","owned_by","its_participant"),("individual_features","separate_across","participants")],
}
RECHECK = {
 1:("S01","원작 표준 로브·선택적 뾰족모자만 확인. 영화식 층·여밈은 별도."),
 3:("S02","원작 빨강·금색 조합 확인. 배치·폭·문장 형태는 별도."),
 4:("S02","원작 초록·은색 조합 확인. 악역/순혈 판정으로 사용하지 않음."),
 5:("S02","원작 노랑·검정 조합 확인. 각 옷 부위의 배치는 별도."),
 6:("S02,S33,S34","원작 파랑·청동/독수리와 상품 남색·은색 확인. 상품을 모든 영화 판본과 같다고 단정하지 않음."),
 7:("S06,S25","3편 재설계의 후드·안쪽 배색 설명, 팬아트의 초록 안쪽 면 관찰. 전 편 공통 사양은 미확인."),
 8:("S01","전통적 뾰족모자 언급 확인. 구체 챙·크라운 형태는 일반 구조 제안."),
 10:("S05","보바통 파란 짧은 망토와 드레스·모자·신발 조합 확인."),
 11:("S04","초기 두 편의 두꺼운 로브형 경기복 확인."),
 12:("S04","후기 가벼운 스포츠형과 등판 이름·번호 설명 확인."),
 13:("S04","6편 운동복형 훈련복·경기 보호대와 헬멧 설명 확인."),
 14:("S03","책의 검정 머리·초록 눈·원형 안경·이마 흉터, 영화 파란 눈·비중앙 흉터 확인."),
 15:("S03","책의 큰 앞니·부푼 머리와 영화의 완화된 치아·웨이브 차이 확인."),
 18:("S30","책 요약의 긴 은빛 수염·반달 안경·자주색 망토 확인. 초기/후기 영화 장식 재단 전부는 미확인."),
 19:("S30","책 요약의 단단한 번·사각 안경·초록 망토 확인. 높은 칼라/영화 모자 세부는 별도."),
 20:("S30,S44","굽은 코·검정 머리·긴 검정 로브의 핵심 확인. 목 단추/옷감 전체는 별도."),
 24:("S05","영화 니트 가슴의 큰 R와 적갈색 사례 확인. 모든 니트의 글자·색은 다름."),
 25:("S31","사람 상체·팔로미노 말 하체 묘사 확인. 공식 글의 책명 표기에 오류 가능성이 있어 원문 대조 필요."),
 26:("S05,S31","금색 망토·크라바트와 원작 눈색에 맞춘 파란 로브·물결 머리 확인. 한 장면으로 합치지 않음."),
 27:("S05","누빔·문장 조끼, 술 망토, 한쪽 장갑 조합 확인."),
 32:("S37","고양이 변신 실패 사건 확인. 회색 영화 털·정확한 귀 부착 구조는 아직 별도 이미지 확인 필요."),
 35:("S06","3편의 일반 청소년 방향 재설계 설명 확인. 개별 사복의 색·제품·재단은 미확인."),
 39:("S31","큰 렌즈의 눈 확대, 얇은 숄과 다중 장신구 묘사 확인. 정확한 광학 수치/잠금 위치 미확인."),
 40:("S13,S14","목에 착용하는 작은 모래시계와 replica 고리 구조 확인. 회전/시간 이동은 정지영상 증명 불가."),
 41:("S31,S32","보가트의 레이스 긴 드레스·박제 새 모자·붉은 가방 확인. 실제 스네이프의 신체 TS가 아님."),
 42:("S15","후드·긴 덮개·미끄러지는 모습·회색 딱지 피부 확인. 부유 간격은 선택된 장면에서 따로 평가."),
 44:("S08,S46","맹금류 앞부분·말 뒤부분과 조류 해부 설계 근거 확인. 기존 profile의 효과 매핑은 추가 심사 필요."),
 45:("S04,S05","파란 원피스·짧은 망토·모자·신발 세트 확인. 옷감/봉제 세부는 원본 사진과 구분."),
 50:("S05","원작 청보라 예복 확인. 영화 분홍색과 별도 버전."),
 51:("S04,S05","영화 분홍·층·실크/시폰 확인. 모든 층 수·광학 효과를 기본 의무로 만들지 않음."),
 52:("S05","낡은 레이스·작은 칼라의 예복 핵심 확인. 직물 문양·부품 봉제는 별도."),
 53:("S45","리타의 기자 소품·초록 깃펜 일부 확인. 노랑 로브·분홍 손톱·악어 가방 전부가 재검증된 것은 아님."),
 55:("S11,S12","마법 의안과 나무 의족 확인. 얼굴 흉터·띠 고정/측면은 추가 이미지 필요."),
 56:("S09","영화 코를 뱀형 콧구멍으로 디지털 변형한 제작 사실 확인. 책의 붉은 눈은 이번 원문 재검증 보류."),
 57:("S07","4편 부분 가면/5편 전면 가면·은빛 장식·복식 문양 연동 확인."),
 58:("S36","대체한 은빛 손의 설정 확인. 손목 접합/제작 방식·마법 힘은 별도."),
 59:("S39","분홍 의상 계열 확인. 치마 정장 재단·가방·리본 전체는 미확인."),
 60:("S39","분홍 톤의 단계 변화 설명 확인. 여러 프레임 비교가 필요한 의미."),
 62:("S05,S16","코르크/열매형 귀걸이·목걸이 언급 확인. 정확한 잎/재질/고리 수는 이미지 단계."),
 63:("S03","짧은 보라색 머리·펑크 방향·붉은 군복 재단 코트 확인. 색 상태는 판본별."),
 65:("S03","제작자가 Agbada·Kota 바지·특수 모자의 영감을 직접 설명. 착용자 국적/문화 정체성 추정 금지."),
 70:("S03,S42","책의 긴 금발/영화 투톤 차이 확인. 직접 본 promo는 어두운 위/앞 롤·밝은 옆/아래 영역; 뒤는 보이지 않음."),
 74:("S05,S43","세 입체 층·짧은 드레스 외곽·별형 귀걸이를 텍스트와 공식 스틸에서 확인."),
 75:("S16","큰 유색 장식 안경 사례 확인. 재질·정확한 렌즈색/패턴은 추가 소품 원본 필요."),
 76:("S16","사자 응원모자 확인. 소리/움직임과 실제 사자 머리는 별개."),
 77:("S04","6편 경기/훈련 보호구 설명 확인. 모든 신체 부위에 같은 패널을 의무화하지 않음."),
 78:("S05","책의 단순 흰 결혼식 드레스 확인. 주변 은광 효과는 별도."),
 79:("S05","영화 흰 튈·검정 불사조 두 문양의 하트·머리 장식 확인. 실제 아플리케 제작 방식은 미확인."),
 85:("S38","비즈 가방과 확장 설정 확인. 작은 가방 사진이 무한 수납을 증명하지 않음."),
 89:("S08","각 고블린의 귀·코·턱을 다르게 만든 제작 원칙 확인. 얼굴 특정 수치/피부 재질은 별도."),
 90:("S04","후일담의 성인 재단과 익숙한 색 범위 설명 확인. 특정 노화 외형은 별도."),
 91:("S04,S40","영화 반지·타이핀과 책의 높은 코트/후퇴한 머리선 구분. 무대 장발과 합치지 않음."),
 93:("S10","아래팔 표식과 하늘 표식의 carrier 차이 확인. 같은 문양이라고 같은 profile로 자동 활성화하지 않음."),
 95:("S11","전기 같은 파란 홍채의 마법 의안 설정 확인. 스냅샷만으로 360도 회전은 증명 불가."),
 96:("S36","연결된 은빛 대체 손 설정 확인. 장갑/독립 소품과 구분."),
 98:("S09","영화 뱀형 콧구멍 제작 근거 확인. 전체 원작/영화 눈·손·색 묶음은 별도."),
 99:("S44","유령의 투명성 원문 인용 확인. 실제 전 인물 투명 효과 세부/원인 식별은 별도."),
 101:("S07","공통 착장·개별 가면 문양의 원칙 확인. 동일 얼굴 복제와 구분."),
 102:("S17","첫 영화 petrol/peacock blue 코트·상의 핏·짧은 바지 설명 확인. 모든 속옷/조끼색은 별도."),
 103:("S19","티나의 여유 있는 천 코트·차분한 색 설명 확인. 큰 칼라/바지 재단은 추가 이미지 필요."),
 104:("S19","퀴니의 밝고 분홍빛 방향·금빛 bob 일부 확인. 정확한 peach/pink coat ombre는 미확인."),
 105:("S18","긴 어깨 강조 코트·검백 테두리·cashmere/Lurex 설명 확인. 장화 세부는 별도."),
 106:("S31","젊은 영화판 조끼·테일러링 방향 확인. 특정 판본 전체 정장색/질감은 별도."),
 107:("S31","원작 회상의 적갈색 긴 머리·수염·자두색 벨벳 정장 확인."),
 108:("S20,S21","무대 홍보/장발·뒤묶음 변형 확인. 긴 머리로 성별 전환을 추정하지 않음."),
 109:("S20","2016 홍보 금발·정돈되고 구속적인 교복 설명 확인. 캐스트별 차이를 유지."),
 110:("S22,S24,S25,S26","개별 팬 작품·원 게시물로 성별 재해석 사례 확인. 변신 과정/신체 치수는 증명하지 않음."),
 111:("S22","특정 한국 팬소설 제목·작가·TS 태그 확인. 해외 모든 여성형 팬아트의 원류는 미확인."),
 112:("S22","작품 소개의 카리나 이름 확인. 외형 표준 또는 다른 작가 그림의 이름으로 일반화하지 않음."),
 113:("S24,S25,S26","세 작가의 직접 표시된 사례를 조사. 표본 빈도/인기도 순위나 모든 변형은 추정하지 않음."),
 114:("S24,S25,S26","세 사례의 긴 옅은 금발 확인. 여성형 디자인의 필수 길이/색으로 정하지 않음."),
 115:("S24,S25,S26","교복에서 초록·회색 배색/로브 안쪽 사례 확인. 일부 그림의 하의·색 표현은 선택 변형."),
 116:("S24,S25","눈꺼풀·입꼬리 행동 차이 사례 확인. 오만함/의도는 별도 독해."),
 117:("S25,S26","서로 다른 포즈 관찰. 팔짱·턱들기·기울임 세 가지를 모두 필수로 만들지 않음."),
 118:("S24,S26","고리 귀걸이와 어두운 손톱을 서로 다른 작가 사례에서 확인. 한 작가 공통 세트라고 합치지 않음."),
 119:("S24,S26","초록·회청색 눈 사례 관찰. 눈색/머리 장식의 공식 고정 규격은 없음."),
}
DESIGN_REFS = set(range(120,130))
TERM_REFS = set(range(130,150))
CONTEXT_DISPOSITIONS = {"CONTEXT_ONLY", "TEMPORAL_ONLY", "BUNDLE_ONLY"}
def effects_for(row):
    dims = split(row["dimensions"])
    result = []
    for prop in split(row["property_paths"]):
        dim = dims[0]
        if "color" in dims and any(v in prop for v in ("color","colour","hue")):
            dim = "color"
        elif "material" in dims and any(v in prop for v in ("surface","texture","padding","thickness","cloth")):
            dim = "material"
        elif "action" in dims and "contact" in prop:
            dim = "action"
        elif "pose" in dims and any(v in prop for v in ("pose","gaze")):
            dim = "pose"
        elif "body_geometry" in dims and prop.startswith(("body.","face.","creature.")) and not "surface" in prop:
            dim = "body_geometry"
        elif "composition" in dims and prop.startswith("scene."):
            dim = "appearance" if "appearance" in prop and "appearance" in dims else "composition"
        target = "request_selected_prop" if prop.startswith("prop.") else "request_selected_scene" if prop.startswith("scene.") else "main_subject"
        result.append({"dimension": dim, "target": target, "property": prop})
    return result

def build():
    source_rows = load("SOURCES.json")["sources"]
    sources = {s["id"]: s for s in source_rows}
    seed_rows = load("SEED-INVENTORY.json")["rows"]
    seeds = {r["id"]: r for r in seed_rows}
    catalog = load("EXISTING-DATA-CATALOG.json")
    profiles = {p["id"]: p for p in catalog["profiles"]}
    entries = {p["id"]: p for p in catalog["candidates"]}
    raw = list(csv.DictReader((OUT/"CARD-INPUT.psv").open(), delimiter="|"))
    units, proposals, mappings, checks = [], [], [], []
    for row in raw:
        assert None not in row and all(v is not None for v in row.values()), row["id"]
        sid = row["id"]
        refs = ["ref_%03d" % int(v) for v in split(row["seed_refs"])]
        src = split(row["sources"])
        assert all(v in seeds for v in refs) and all(v in sources for v in src), sid
        components = row["components_en"].split("~")
        assert len(components)==3 and all(len(v.split())>=5 for v in components), sid
        ep, ec = row["existing"].split(";")
        existing_profiles, existing_candidates = split(ep), split(ec)
        assert all(v in profiles for v in existing_profiles), (sid,existing_profiles)
        assert all(v in entries for v in existing_candidates), (sid,existing_candidates)
        draft_effects = effects_for(row)
        edges = EDGES.get(sid, [])
        draft_relations = [{"id": sid.lower()+"_r"+str(i+1),"subject":a,"type":t,"object":b,"owner_binding":"same_declared_owner_unless_explicit_scene_participants"} for i,(a,t,b) in enumerate(edges)]
        if not draft_relations:
            draft_relations = [{"id":sid.lower()+"_r"+str(i+1),"subject":"component_"+str(i+1),"type":"co_owned_by","object":"declared_carrier","predicate_en":part,"owner_binding":"same_declared_owner_unless_explicit_scene_participants","endpoint_mapping_status":"REVIEW_REQUIRED"} for i,part in enumerate(components)]
        semantic = {
            "id":sid,"label_ko":row["label_ko"],"family":row["family"],"seed_refs":refs,
            "source_refs":src,"source_qualification":row["qualification"],
            "status":STATUS,"canon_claim_limit":"Sources verify only their stated facts; the three morphology propositions below are researcher-authored implementation specifications, not claims that every listed seed has all these properties.",
            "positive_definition_en":"; ".join(components)+".","decomposition_ko":row["decomposition_ko"],
            "owner_carrier":{"default":"same explicitly declared wearer, head, body model, object or scene","binding":"must be bound from requesting user/frozen core before runtime adoption","scene_participants_separate":row["family"]=="interaction"},
            "components":[{"id":sid.lower()+"_c"+str(i+1),"observable_predicate_en":part,"evidence_phrase_proposal":part,"review_scale":"native","required_only_if":"the requesting user selects this complete morphology; a search hit alone is advisory"} for i,part in enumerate(components)],
            "relations":draft_relations,"confusion_boundaries":[row["confusion_boundary"]],
            "version_policy":{"source_family":"book/film-number/stage-production/replica/individual-fanwork remain independent","source_case_refs":refs,"unselected_dimensions":"colour, hairstyle length, age, pose, sex/gender presentation, garment material and biography remain open unless explicitly selected","single_still_limits":"no inference of movement, transformation history, magical function or mental state"},
            "existing_links":{"profiles":[{"id":v,"file":profiles[v]["file"],"activation_preservation":profiles[v]["activation"]} for v in existing_profiles],"candidates":[entries[v] for v in existing_candidates]},
            "disposition":row["disposition"],"adoption_note":row["note"],
            "native_gate_policy":"all selected components and owned relations required; partial_is_fail; required hidden feature is UNOBSERVABLE_NOT_PASS; blocked generation is BLOCKED_UNSCORED, not an image failure or pass",
        }
        units.append(semantic)
        files = FAMILY_FILES.get(row["family"])
        source_files = [{"filename":v,"exists_in_snapshot":(ASSETS/v).exists(),"role":"profile_source" if i==0 else "candidate_source","mapping":"PROPOSED_NOT_ADOPTED"} for i,v in enumerate(files or [])]
        related_owner_files = sorted({profiles[v]["file"] for v in existing_profiles}|{entries[v]["file"] for v in existing_candidates})
        mapping = {"semantic_id":sid,"disposition":row["disposition"],"proposed_slot":row["slot"],"proposed_dimensions":split(row["dimensions"]),"proposed_effects":draft_effects,"effect_mapping_status":"DRAFT_PATHS_AND_TARGETS_REQUIRE_RUNTIME_OWNER_REVIEW","suggested_source_files":source_files,"confirmed_existing_owner_files":related_owner_files,"requires_adoption_review":True,"note":row["note"]}
        mappings.append(mapping)
        if row["disposition"] not in CONTEXT_DISPOSITIONS:
            positive = [row["label_ko"], row["decomposition_ko"], *components]
            proposal = {
                "id":"draft_"+sid.lower(),"semantic_id":sid,"status":STATUS,"adoption_ready":False,
                "proposed_slot":row["slot"],"ko":row["label_ko"],"en":semantic["positive_definition_en"],
                "concept_units":components,"relations":draft_relations,"paraphrases":[row["decomposition_ko"]],
                "positive_retrieval_text":" | ".join(positive),
                "affected_dimensions_proposal":split(row["dimensions"]),"affected_properties_proposal":draft_effects,
                "profile_association":"planned association only; never creates requester locks or hard obligations",
                "adoption_constraints":{"default_optional":True,"exact_request_context_required_for_hard":True,"no_name_based_auto_bundle":True,"source_and_owner_review_required":True,"negation_exclusions_locks_and_medium_must_pass":True},
                "source_refs":src,"existing_profile_ids":existing_profiles,"existing_candidate_ids":existing_candidates,
                "keep_out_of_positive_retrieval":["source URLs and names","book/film/cast/version metadata","confusion negatives","claim limits","research status","profile/candidate IDs","character biography or personality"],
            }
            proposals.append(proposal)
        examples = [
            ("positive_components","; ".join(components),"Complete component match may be found as advisory; any hard eligibility still needs grounded exact requester context."),
            ("remove_component","; ".join(components[:-1]),"Incomplete conjunction must not pass complete-profile component coverage."),
            ("negate","Do not add this selected relation: "+"; ".join(components),"Negated meaning creates no hard activation or positive fallback."),
            ("wrong_owner",row["confusion_boundary"],"Nearby object, surface or owner substitute must not satisfy the same-owner profile."),
            ("advisory_origin","; ".join(components),"Agent-authored core/candidate origin remains advisory and cannot become requester-owned locks."),
            ("property_lock",json.dumps(draft_effects,ensure_ascii=False),"Candidate must be rejected or narrowed when a requested affected property is locked; a broad parent effect cannot bypass child locks."),
            ("request_definition_override","The requesting user explicitly defines this label differently.","User definition takes precedence; registry/default version is not forced."),
            ("source_version_mismatch",", ".join(refs),"An unselected book/film/stage/product/fanwork version cannot overwrite the declared version."),
            ("hidden_required_component",components[0]+" is occluded in the generated frame.","Required pixel predicate is UNOBSERVABLE_NOT_PASS, never inferred from the prompt.")
        ]
        for kind,text,expected in examples:
            checks.append({"id":sid.lower()+"_"+kind,"semantic_id":sid,"test_kind":kind,"case_material":text,"expected_boundary":expected,"status":"PLANNED_NOT_EXECUTED","independence":"Derived from these same authoring records; specification checks, not independent holdouts."})

    coverage=[]
    for seed in seed_rows:
        n=int(seed["id"][4:])
        mapped=[u["id"] for u in units if seed["id"] in u["seed_refs"]]
        assert mapped, seed["id"]
        if n in RECHECK:
            src, claim = RECHECK[n]
            status, note = "SELECTED_FACTS_RECHECKED_NOT_WHOLE_ROW", claim
            source_refs=split(src)
        elif n in DESIGN_REFS:
            status, note="RESEARCHER_DESIGN_PROPOSAL","원 대화 자체가 변형안으로 제안한 행. 공식·모든 팬아트 공통 외형으로 채택하지 않는다."
            source_refs=[]
        elif n in TERM_REFS:
            status, note="GENERIC_MORPHOLOGY_OR_EXISTING_DATA","용어의 구조·소유·오인 경계를 재정의했다. 해당 인물/영화의 실제 제작 방식·모든 속성 확인과는 별개다."
            source_refs=sorted({s for u in units if u["id"] in mapped for s in u["source_refs"]})
        else:
            status, note="CASE_SOURCE_LEAD_NOT_CANON_VERIFIED","표의 고유 사례 세부는 수신본의 조사 lead로 보존했다. 일반 형태 설명·기존 데이터 재사용은 가능하나 특정 판본의 색/재질/연결을 확정하지 않는다."
            source_refs=[]
        coverage.append({**seed,"mapped_semantic_ids":mapped,"source_recheck_status":status,"verified_scope_note":note,"source_refs_for_verified_scope":source_refs,"series_or_context":seed["section"],"whole_seed_row_verified":False})
    bundles_spec = [
        ("B01","같은 착용자의 교복 층과 지역 배색",["H002","H003","H004","H005","H006"],"H002", "House colour, crest, lower garment and hood state require explicit choices."),
        ("B02","장식적인 결투복의 독립 부품",["H012","H014","H015","H016"],"H014","Do not force a glove side, exact crest or robe colour."),
        ("B03","짧은 어깨 망토와 아래 의복",["H009","H025","H100"],"H009","Only capelet/lower-layer geometry is established. Chiffon/pleats are optional design alternatives, not a Beauxbatons canon set."),
        ("B04","가면 군집의 덮임과 개체 차이",["H075","H076","H119"],"H075","Select partial/full coverage by version; engraving, material and participants stay separate."),
        ("B05","팬 해석에서 선택한 머리·교복·장식",["H036","H120","H002","H003","H004","H087","H093","H094","H108"],"H002","No female/age/body/long-hair/eye-colour default is created by TS, Female Draco or a title."),
        ("B06","인공 눈·얼굴 흉터·고정부",["H061","H059","H118"],"H061","H118 film strap still needs source qualification; a blue eye does not select replacement anatomy."),
        ("B07","몸판의 두 새 문양과 별도 튈",["H028","H099"],"H028","No proof of applique manufacture, wings as anatomy or exact fiber from appearance."),
        ("B08","선택한 히포그리프의 접합형",["H072"],"H072","Reuse existing topology profile; review body category and affected-property mapping before adoption.")
    ]
    unitmap={u["id"]:u for u in units}
    bundles=[]
    for bid,label,ids,primary,note in bundles_spec:
        eff=[]
        for sid in ids:
            for e in next(m for m in mappings if m["semantic_id"]==sid)["proposed_effects"]:
                if e not in eff:eff.append(e)
        bundles.append({"id":bid,"label_ko":label,"semantic_members":ids,"primary_relation":primary,"member_draft_ids":["draft_"+v.lower() for v in ids],"candidate_only":True,"status":STATUS,"selection_policy":"adopt only selected components; complete bundle metadata is not blanket permission to apply every member","effect_union_proposal":eff,"no_hard_activation_by_association":True,"note":note})
    save("SEMANTIC-UNITS.json",{"schema_version":"harry-potter-research-semantics/v1","status":STATUS,"units":units})
    save("CANDIDATE-DRAFTS.json",{"schema_version":"harry-potter-research-candidates/v1","status":STATUS,"candidates":proposals})
    save("RUNTIME-MAPPING.json",{"schema_version":"harry-potter-research-mapping/v1","status":STATUS,"mappings":mappings})
    save("SEED-COVERAGE.json",{"schema_version":"harry-potter-research-coverage/v1","status":"ALL_RECEIVED_SEED_ROWS_MAPPED_NOT_ALL_CANON_VERIFIED","rows":coverage})
    save("BUNDLE-DRAFTS.json",{"schema_version":"harry-potter-research-bundles/v1","status":STATUS,"bundles":bundles})
    save("REGRESSION-PLAN.json",{"schema_version":"harry-potter-planned-regressions/v1","status":"PLANNED_NOT_EXECUTED","independent_holdouts":0,"cases":checks})

    card_doc=["# 시각 의미 상세 카드", "", "2026-10-06 KST. 120개 연구 단위이며 활성 profile/후보 수가 아니다. 각 카드의 영어·한국어 형태는 고유명사를 제거한 연구자 작성 명세다. 출처는 연결된 특정 사실만 확인하며 전체 형태·모든 참조 행을 자동 보증하지 않는다.", "", "RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA. 색·길이·동작·연령·몸 형태·원인·기능은 명시적으로 선택된 범위에만 적용한다.", ""]
    for u in units:
        src_links=", ".join("["+sid+"]("+sources[sid]["url"]+")" for sid in u["source_refs"])
        ep=", ".join(p["id"] for p in u["existing_links"]["profiles"]) or "없음"
        ec=", ".join(p["id"] for p in u["existing_links"]["candidates"]) or "없음"
        card_doc += ["## "+u["id"]+" "+u["label_ko"],"",u["decomposition_ko"],"",u["positive_definition_en"],"",
                    "- 관찰 요소: "+" / ".join(p["observable_predicate_en"] for p in u["components"]),
                    "- 소유·관계: "+json.dumps(u["relations"],ensure_ascii=False),
                    "- 오인 경계: "+u["confusion_boundaries"][0],
                    "- 출처 상태: "+u["source_qualification"]+"; "+src_links,
                    "- 기존 profile: "+ep+"; 기존 후보: "+ec,
                    "- 제안 처리: "+u["disposition"]+" — "+u["adoption_note"],
                    "- 참조 행: "+", ".join(u["seed_refs"]),
                    "- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.", ""]
    (OUT/"SEMANTIC-CARDS.md").write_text("\n".join(card_doc)+"\n")
    audit=["# 참조 키워드 149행 대조", "", "수신된 20,000자 답변에서 보이는 표 149행의 coverage다. 마지막 예시/인용 URL이 잘려 원 대화 전체 회수 성공을 주장하지 않는다. 아래 연결은 형태 연구의 연결이며 whole-row canon verification을 뜻하지 않는다.", ""]
    current=""
    for row in coverage:
        if row["section"]!=current:
            current=row["section"];audit += ["## "+re.sub(r'^#+\s*','',current),"","|행|키워드|연결 카드|재확인 범위|","|---|---|---|---|"]
        audit.append("|"+row["id"]+"|"+row["label"]+"|"+", ".join(row["mapped_semantic_ids"])+"|"+row["source_recheck_status"]+": "+row["verified_scope_note"].replace("|","/")+"|")
    (OUT/"KEYWORD-AUDIT.md").write_text("\n".join(audit)+"\n")
    ledger=["# 출처와 한계", "", "출처 확인일: 2026-10-06 KST. 제작자 인터뷰·원작 공개 글·공식 제작 자료·실제 팬 게시물·박물관 기술 참고를 구분했다. secondary trend index와 replica는 해당 범위에만 사용했다. Source image inspection은 생성 이미지의 native-pixel qualification이 아니다.", "", "|ID|자료|유형/접근|직접 뒷받침하는 범위|한계|", "|---|---|---|---|---|"]
    for s in source_rows:
        ledger.append("|"+s["id"]+"|["+s["title"]+"]("+s["url"]+")|"+s["type"]+" / "+s["access"]+"|"+s["supported_claims"]+"|"+s["claim_limits"]+"|")
    (OUT/"SOURCES.md").write_text("\n".join(ledger)+"\n")
    stats={"seed_rows":len(seed_rows),"semantic_units":len(units),"candidate_drafts":len(proposals),"bundle_drafts":len(bundles),"source_records":len(source_rows),"planned_regression_cases":len(checks),"seed_status_counts":dict(Counter(r["source_recheck_status"] for r in coverage)),"qualification_counts":dict(Counter(r["source_qualification"] for r in units)),"disposition_counts":dict(Counter(r["disposition"] for r in units)),"linked_existing_profiles":len({v["id"] for u in units for v in u["existing_links"]["profiles"]}),"linked_existing_candidates":len({v["id"] for u in units for v in u["existing_links"]["candidates"]}),"missing_suggested_files":sorted({r["filename"] for m in mappings for r in m["suggested_source_files"] if not r["exists_in_snapshot"]}),"runtime_adoption":"NOT_PERFORMED","native_generation":"NOT_PERFORMED","user_judgment":"pending"}
    save("RESEARCH-STATS.json",stats)
    print(json.dumps(stats,ensure_ascii=False))
if __name__=="__main__":
    build()
