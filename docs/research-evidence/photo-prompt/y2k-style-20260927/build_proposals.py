"""Rebuild research proposals and check them against the current authored contract.

Writes only this evidence directory. Does not register an extension, rebuild an
index, render an image, or modify the runtime dictionary.
"""
from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import photo_candidate_semantics as semantics


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(value):
    return [item.strip() for item in value.split(";") if item.strip()]


def family(fid, terms, scope, status, members, refs, boundary):
    return {
        "id": fid, "seed_terms": terms, "period_scope_ko": scope,
        "historical_status": status, "example_component_ids": members.split(),
        "source_refs": refs.split(), "boundary_ko": boundary,
        "activation": "advisory_only_until_literal_components_are_requested",
        "era_bounds_are_not_component_invention_dates": True,
    }


FAMILIES = [
    family("millennium_futurism", ["Y2K Futurism"], "밀레니엄 전후의 미래주의; 1999 런웨이는 확인 사례", "archived_example_not_universal_period", "metallic pvc iridescent shield circuit_graphic", "S01 S06", "실버 한 면으로 시대를 판정하지 않는다. 1999 계열에 2005 기기를 자동 혼합하지 않는다."),
    family("cyber_y2k", ["Cyber Y2K / Cybercore", "Cyber Y2K"], "밀레니엄 주변의 테크·클럽 표현과 현대 재해석을 구분", "overlapping_label_not_fixed_era", "mesh vinyl wraparound circuit_graphic binary_graphic", "S01 S25", "Cybercore를 역사적 정식 명칭 또는 동일 시대의 보증으로 쓰지 않는다."),
    family("techno_futurism", ["Techno Futurism", "Tech Futurism"], "1999 런웨이 사례; 일반 기술 소재 어휘는 시대 독점 아님", "archived_runway_example", "bodysuit retroreflective metal_mesh pvc circuit_graphic", "S01 S20 S21", "외관상의 광택과 실제 기술 기능을 분리한다."),
    family("pop_y2k", ["Pop Y2K / Teen Pop", "Pop Y2K"], "2000년 전후 팝 패션을 찾는 검색 계열; 단일 시작·종료 연도 보류", "retrospective_family", "baby_tee low_rise bootcut butterfly_clips spiky_bun gloss", "S03 S08 S10", "Teen Pop은 스타일·음악 문맥이며 인물의 나이를 지정하지 않는다."),
    family("mcbling", ["McBling"], "회고적 분류에서 대략 2003–2008; 아이템은 이전에도 존재", "editorial_approximation", "velour_hoodie velour_pants rhinestones stone_belt trucker crown_graphic", "S02 S07 S33", "큐빅을 사용한 2000 사진도 있다. 계열의 연대와 장식의 발명 연도를 혼동하지 않는다."),
    family("sporty_y2k", ["Y2K Sporty", "Sporty Y2K"], "스포츠 의복 요소를 결합한 계열; 특정 국가나 정확한 연대는 추가 증거 필요", "morphological_family", "track_jacket track_pants visor racing_stripe crop_tank", "S04", "현대 athleisure와 자동 동일화하지 않는다. 팀·국적·성적 분위기 자동 부여 없음."),
    family("streetwear_y2k", ["Y2K Streetwear"], "힙합·스케이트 등을 나눠 읽어야 하는 상위 검색 계열", "umbrella_with_separate_contexts", "baggy jersey oversize_tee skate_shoes", "S04", "힙합과 스케이트의 활동·장비를 서로 대신 쓰지 않는다."),
    family("hiphop_street", ["Hip-hop Streetwear"], "박물관 자료는 장기간의 역사와 디자이너·참여자를 다룸", "broad_historical_context", "jersey baggy layer_chains panel_cap", "S04", "의복에서 인종·계층·소속·직업을 추정하지 않는다. 모든 착장에 chain 필수 아님."),
    family("skate_street", ["Skate Streetwear"], "넓은 의복과 스케이트 신발의 형태 연구; 개별 연대·지역은 보류", "researcher_operational_family", "oversize_tee baggy skate_shoes checkerboard", "", "보드가 배경에 있다고 실제 스케이트 활동·기술 수준이 입증되지 않는다."),
    family("mall_goth", ["Y2K Mall Goth", "Mall Goth", "Goth Y2K"], "2000년대 대안 패션과 후대 회고의 경계", "retrospective_context_limited", "mesh grommet platform_boots goth_motif blackletter", "S24", "검은색 하나로 정체성 판정하지 않는다. Emo·Scene을 자동 대체하지 않는다."),
    family("rave", ["Y2K Rave / Club Kid", "Rave Y2K"], "레이브 계열은 Y2K 이전에도 존재; 1980년대 자료는 선행 사례", "preexisting_scene_not_y2k_exclusive", "mesh retroreflective furry_boots platform_boots", "S25 S20", "네온·털·플랫폼의 동시 필수화 없음. Club Kid와 모든 rave 활동의 동의어화 없음."),
    family("boho_2000s", ["2000s Boho"], "2000년대 중반 보헤미안 층입기; 2004–2007 엄밀 범위는 보류", "retrospective_mid_2000s", "peasant tiered skinny_scarf wide_belt bolero", "S03", "재료·주름·레이어로 표현한다. 특정 민족·지역의 전통복으로 치환하지 않는다."),
    family("gyaru", ["Gyaru / Heisei Gyaru", "Gyaru"], "1999 관찰과 시부야 문화 자료; 헤이세이 전체를 단일 미학으로 축소하지 않음", "period_place_context_with_internal_variation", "loose_socks mini_boots color_streak stone_nails platform_sandal", "S27 S29 S30", "갸루 하위 계열·시기 변이를 보존한다. 피부색·국적·교복을 필수로 넣지 않는다."),
    family("nu_metal", ["Nu-metal Fashion"], "참조 대화의 인접 계열; 의복 수준 제안이며 정확한 역사 검증은 미완", "seed_context_requires_primary_archive", "baggy mesh grommet abstract_blades", "S24", "음악 장르와 의복 유사성은 별도 증거이다. 몰 고스의 완전한 동의어 아님."),
    family("emo", ["Emo"], "초기 Y2K와 섞이지 않도록 인접 계열로 관리; 정확한 연대 보류", "seed_context_requires_primary_archive", "side_fringe skinny_jeans grommet", "", "대각 앞머리 하나로 정체성·정서 상태·자해를 추론하지 않는다."),
    family("scene", ["Scene"], "후기 2000년대와 현대 회고; 자료의 2008 사례는 존재 증거", "later_example_not_exact_birthdate", "teased_crown color_streak skinny_jeans", "S31", "참조 대화의 2005 시작을 검증된 경계로 승격하지 않는다."),
    family("indie_sleaze", ["Indie Sleaze"], "회고적 범위 대략 2006–2013; 정의에 따라 변동", "editorial_approximation_later_neighbor", "skinny_jeans retro_flash", "S31", "직광 플래시만으로 스타일을 판정하지 않는다. 1999 고증과 구분한다."),
    family("acubi", ["Acubi"], "2020년대 현대 한국 패션 문맥; 2026 설명을 확인", "contemporary_neighbor", "layered_tanks mesh asym_top cargo", "S23", "원조 Y2K의 역사 범주로 소급하지 않는다. 브랜드 창립 연도는 이번 근거로 확정하지 않는다."),
    family("balletcore", ["Balletcore"], "현대 명칭의 재유행은 2022 기사로 확인; 발레의 패션 영향은 훨씬 이전", "contemporary_label_with_older_components", "ballet_flats wrap_knit ribbon_tie legwarmers", "S34", "발레 플랫 하나로 balletcore 또는 댄서 직업·체형을 지정하지 않는다."),
    family("frutiger_aero", ["Frutiger Aero"], "CARI의 디지털 디자인 분류 대략 2005–2013", "design_taxonomy_not_fashion_era", "", "S22", "잔디·유리·구름 UI 분위기를 옷 실루엣이나 1999 미래주의로 치환하지 않는다."),
    family("cybercore_revival", ["Cybercore"], "현대 인터넷 용법과 과거 테크 계열을 분리; 명칭 탄생일 보류", "seed_context_contemporary_reinterpretation", "wraparound circuit_graphic chrome_star", "S01 S22", "현대 과장·혼합을 재현 고증과 별도 모드로 관리한다."),
]


# A conjunction in one coherent outfit or a single inspected detail. Members
# are not alternative haircuts, incompatible waist heights, or all style tropes.
BUNDLE_SPECS = [
    ("pop_denim", "짧은 상의와 낮은 부츠컷 팬츠", "baby_tee low_rise bootcut butterfly_clips platform_sandal", "S03 S08", "the short upper hem and low waistband remain separate above the widening lower trouser legs", "same_outfit", "baby_tee", "low_rise", "appearance body_geometry"),
    ("spiky_hair", "솟은 끝가닥·가르마·앞가닥", "spiky_bun zigzag_part tendrils", "S08 S09", "the zigzag scalp part leads into gathered hair while thin front strands remain outside the bun", "same_head", "zigzag_part", "spiky_bun", "appearance"),
    ("millennium_surface", "메탈릭·투명층·차폐형 안경", "metallic pvc shield circuit_graphic", "S01", "flexible metal-like cloth remains separate from the clear outer layer and the single shield lens", "different_surface_owners", "metallic", "pvc", "appearance material"),
    ("cyber_club", "메시·비닐·곡률 렌즈", "mesh_top mesh vinyl wraparound barcode_graphic", "S01 S25", "the open mesh belongs to the upper garment and remains distinct from the glossy solid lower surface", "material_on", "mesh", "mesh_top", "appearance material"),
    ("velour_set", "파일 원단의 짧은 후디와 팬츠", "velour_hoodie velour_pants velour stone_belt trucker", "S02 S07", "the hoodie and trousers share short-pile texture while the belt retains separate faceted stones", "material_on_set", "velour", "velour_hoodie", "appearance material"),
    ("bling_detail", "로고형 프린트와 작은 스톤", "crown_graphic rhinestones stone_bag gloss", "S02 S33", "small faceted decorations remain distinguishable from the flat crown print and broad lip gloss highlights", "different_surface_owners", "rhinestones", "crown_graphic", "appearance material"),
    ("sport_panels", "스포츠 패널과 낮은 카고", "track_jacket low_cargo visor racing_stripe", "S04", "parallel stripe details remain on the athletic jacket above the separate low utility trousers", "graphic_on", "racing_stripe", "track_jacket", "appearance"),
    ("hiphop_volume", "느슨한 저지와 넓은 팬츠", "jersey varsity_number baggy layer_chains", "S04", "block numerals remain on the loose jersey while separate trousers retain generous leg volume", "graphic_on", "varsity_number", "jersey", "appearance"),
    ("skate_volume", "큰 티셔츠·넓은 팬츠·낮은 신발", "oversize_tee baggy skate_shoes checkerboard", "", "the loose tee and wide trousers retain separate hems above low skate shoes with a bounded check detail", "graphic_on", "checkerboard", "oversize_tee", "appearance"),
    ("mallgoth_hardware", "검은 메시와 아일렛·부츠", "mesh_top mesh grommet platform_boots goth_motif", "S24", "open thread mesh and metal-rimmed belt holes remain visible as separate structures", "material_on", "mesh", "mesh_top", "appearance material"),
    ("rave_trim", "망사 의복과 반사 트림", "mesh_top mesh retroreflective furry_boots", "S25 S20", "a narrow bright source-facing trim stays separate from open mesh and the furry boot shafts", "material_on", "mesh", "mesh_top", "appearance material"),
    ("boho_layers", "셔링 상의와 층진 치마", "peasant tiered skinny_scarf wide_belt bolero", "S03", "a thin scarf and broad belt remain separate from the blouse gathering and stacked skirt tiers", "same_outfit", "peasant", "tiered", "appearance"),
    ("gyaru_detail", "미니·플랫폼·루즈삭스의 구성", "denim_mini platform_sandal loose_socks large_hoops", "S27 S29", "independent gathered sock tubes remain visible between the short skirt and thick shoe platforms", "same_wearer", "loose_socks", "platform_sandal", "appearance"),
    ("frost_lip", "서리광 눈과 경계가 다른 입술", "lilac_frost brown_liner nude_center gloss", "S10 S11", "the darker lip perimeter surrounds a lighter center while gloss is a separate surface reflection", "surrounds", "brown_liner", "nude_center", "appearance"),
    ("nail_macro", "사각 손톱·프렌치 끝·입체 장식", "square_nails french_nails star_nail", "", "a contrasting French tip follows the square free edge and a raised star remains attached to the nail plate", "same_nail_plate", "french_nails", "star_nail", "appearance"),
    ("early_devices", "2001년 말 이후 iPod와 접이식 폰", "ipod flip_phone wired_earbuds", "S12 S16", "a cable visibly connects the earphones to the player while the phone retains a separate hinge and keypad", "connects_to", "wired_earbuds", "ipod", ""),
    ("mid_devices", "2005년 이후 기기 배열", "nano razr_phone digicam phone_charm", "S13 S15 S18", "the slim player phone camera and attached charm remain four distinct objects", "attached_to", "phone_charm", "razr_phone", ""),
    ("revival_layers", "현대 얇은 레이어와 비대칭", "layered_tanks mesh asym_top cargo", "S23", "asymmetric upper edges remain distinct from a translucent mesh layer and attached utility pockets", "same_outfit", "asym_top", "cargo", "appearance material"),
    ("ballet_neighbor", "겹친 니트·리본·플랫", "wrap_knit ribbon_tie ballet_flats legwarmers", "S34", "the knitted wrap edge and ribbon knot remain separate above low flats and independent leg sleeves", "same_outfit", "wrap_knit", "ballet_flats", "appearance"),
    ("palette_roles", "색과 반짝임의 영역 구별", "bling_palette velour_hoodie velour rhinestones", "S02 S07", "the selected vivid color belongs to the hoodie cloth while small bright accents remain local to its ornaments", "color_and_material_on", "bling_palette", "velour_hoodie", "appearance material color"),
]

GRAPHIC_GROUPS = {
    "Cute Pop": "cute_motifs", "Celestial": "celestial_motifs", "Angelcore": "angel_motif",
    "Devilish": "devil_heart flame_graphic", "Tattoo Graphics": "tattoo_graphic abstract_blades",
    "McBling": "crown_graphic monogram_graphic rhinestones", "Racing": "racing_stripe checkerboard varsity_number",
    "Cyber": "circuit_graphic barcode_graphic pixel_graphic binary_graphic chrome_type",
    "Space": "space_graphic chrome_star", "Street": "graffiti varsity_number",
    "Animal Print": "leopard_print zebra_print snakeskin_print", "Military": "camouflage",
    "Goth Y2K": "goth_motif blackletter cross_pendant",
}


def main():
    seeds = read("seed-keywords.json")["rows"]
    sources = read("sources.json")["sources"]
    source_ids = {s["id"] for s in sources}
    rows = []
    for name in ("components.tsv", "additional-components.tsv"):
        rows += list(csv.DictReader((HERE / name).open(), delimiter="|"))
    # Preserve category-specific modifiers rather than flattening to synonyms.
    correction = {
        "denim_jacket": ["Denim Jacket"], "flare": ["Flared Jeans"],
        "cargo": ["Cargo Pants"], "capri": ["Capri Pants"],
        "metallic": ["Metallic Fabric"], "hoops": ["Hoop Earrings"],
        "pendant": ["Pendant Necklace"], "frost_eye": ["Frosted Eyeshadow"],
        "thin_brows": ["Thin Brows"], "body_glitter": ["Body Glitter"],
        "nail_charms": [],
    }
    for row in rows:
        row["terms"] = correction.get(row["id"], tokens(row["seed_terms"]))
    assert len(rows) == len({r["id"] for r in rows})
    by_id = {r["id"]: r for r in rows}
    families_by_term = defaultdict(list)
    for f in FAMILIES:
        assert set(f["source_refs"]) <= source_ids
        assert set(f["example_component_ids"]) <= set(by_id)
        for term in f["seed_terms"]:
            families_by_term[term.casefold()].append(f["id"])
    broad_terms = {s["term"].casefold() for s in seeds if s["section"] in (1, 17, 20)}
    broad_terms.update(families_by_term)
    live = json.loads((ASSETS / "photo_prompt_tags.json").read_text())
    policy = live["candidate_semantic_policy"]
    dimensions = set(d for dims in policy["slot_dimensions"].values() for d in dims)
    semantics.validate_semantic_policy(policy, dimensions)
    components, slots = [], defaultdict(list)
    term_components = defaultdict(list)
    frame_groups = defaultdict(list)
    for row in rows:
        cid, slot = row["id"], row["slot"]
        assert slot in policy["slot_dimensions"], slot
        narrow = [t for t in row["terms"] if t.casefold() not in broad_terms]
        for term in row["terms"]:
            term_components[term.casefold()].append(cid)
        refs = []
        if slot == "hair_style" or slot == "hair_color":
            refs = ["S08"]
        elif slot in {"eyeshadow_style", "lip_color_placement", "lip_finish", "brow_style"}:
            refs = ["S10", "S11"]
        if cid == "zigzag_part": refs = ["S09"]
        if cid == "retroreflective": refs = ["S20", "S21"]
        if cid == "ipod": refs = ["S12"]
        if cid == "nano": refs = ["S13", "S14"]
        if cid == "razr_phone": refs = ["S15", "S16"]
        if cid == "sidekick_phone": refs = ["S17"]
        if cid == "digicam": refs = ["S18", "S19"]
        if cid in {"phone_neckstrap", "phone_charm"}: refs = ["S27", "S30"]
        if cid in {"bedazzled_phone", "purikura"}: refs = ["S30"]
        if cid in {"mini_shoulder", "underarm"}: refs = ["S26"]
        if cid == "baguette": refs = ["S05", "S06"]
        if cid in {"rhinestones", "sequins", "beads"}: refs = ["S33"]
        if cid == "velour": refs = ["S35", "S36"]
        if cid == "terry": refs = ["S35", "S36"]
        if cid == "satin": refs = ["S37"]
        units = tokens(row["visible_components_en"])
        comp = {
            "id": cid, "label_ko": row["ko"], "seed_terms": row["terms"],
            "slot": slot, "owner": row["owner"], "visible_components": units,
            "confusion_negatives_ko": [row["confusion_boundary_ko"]],
            "minimum_view": row["view"], "affected_dimensions": policy["slot_dimensions"][slot],
            "source_refs": refs,
            "source_role": "context_or_form_guide_only_not_validation_of_every_predicate",
            "definition_origin": "researcher_authored_operational_proposal",
            "historical_prevalence": "not_established_by_this_record",
            "morphology_revision_needed": "regional_hat_labels" if cid == "panel_cap" else None,
            "pixel_gates": [
                {"id": f"{cid}_owner", "criterion": f"the evidence belongs to {row['owner']} rather than another object or the whole image"},
                {"id": f"{cid}_form", "criterion": "all declared visible components are readable in the minimum view"},
                {"id": f"{cid}_boundary", "criterion": "the stated confusion substitute is absent as the sole realization"},
            ],
            "qualification_status": "not_rendered_not_pixel_qualified",
            "admission": "explicit_component_request_or_optional_inspiration_no_umbrella_hard_activation",
        }
        components.append(comp)
        # Positive runtime language contains literal visible forms only. Era,
        # citations, claim limits, exclusions and cultural identities stay here.
        entry = {
            "id": "y2kr_" + cid, "ko": row["ko"], "en": "; ".join(units),
            "aliases": narrow, "concept_units": units,
            "affected_dimensions": policy["slot_dimensions"][slot], "weight": 0.45,
            "tags": ["y2k_morphology_visual_semantics", slot],
            "keywords": narrow + [row["ko"]], "embedding_text": "; ".join(units),
        }
        slots[slot].append(entry)
        frame_groups[row["view"]].append(cid)
    mappings = []
    for seed in seeds:
        term = seed["term"].casefold()
        matched_components = GRAPHIC_GROUPS[seed["term"]].split() if seed["section"] == 17 else term_components.get(term, [])
        mappings.append({
            "seed_id": seed["seed_id"], "term": seed["term"], "section": seed["section"],
            "component_ids": matched_components,
            "family_ids": families_by_term.get(term, []),
            "status": "component_and_context_proposed" if matched_components and families_by_term.get(term)
                else "operational_component_proposed" if matched_components
                else "context_only_proposed" if families_by_term.get(term) else "unmapped",
            "mapping_is_not_synonym_or_historical_certification": True,
            "modifier_check": "size_color_material_placement_preserved_in_variant_or_boundary",
        })
    assert not [m for m in mappings if m["status"] == "unmapped"]
    bundle_designs, runtime_bundles = [], []
    for bid, ko, member_text, ref_text, sentence, rel_type, subject, obj, _ in BUNDLE_SPECS:
        members = member_text.split()
        assert len(members) <= policy["joint_adoption"]["maximum_members_per_bundle"]
        assert set(members) <= set(by_id)
        refs = ref_text.split()
        assert set(refs) <= source_ids
        designs = {
            "id": bid, "label_ko": ko, "component_ids": members,
            "source_refs": refs, "same_frame_relation": sentence,
            "era_policy": "early_player_available_from_2001_11_10" if bid == "early_devices"
                else "nano_and_razr_combination_no_earlier_than_2005_09_07" if bid == "mid_devices"
                else "no_precise_year_guarantee_choose_historical_or_revival_context_explicitly",
            "all_members_jointly_optional": True,
            "minimum_view": "multi_scale_details_needed" if bid not in {"spiky_hair", "frost_lip", "nail_macro"}
                else "head_or_macro_detail",
            "owner_binding_pending": [m for m in members if not policy["slot_dimensions"][by_id[m]["slot"]]],
            "qualification_status": "contract_candidate_proposal_pixels_pending",
        }
        bundle_designs.append(designs)
        runtime_bundles.append({
            "id": "y2kr_bundle_" + bid,
            "primary_visual_proposition": sentence,
            "candidate_only": True,
            "component_groups": [{"id": "visible_" + m, "visible_evidence": tokens(by_id[m]["visible_components_en"])} for m in members]
                + [{"id": "coherent_relation", "visible_evidence": [sentence]}],
            "candidate_ids": ["y2kr_" + m for m in members],
            "candidate_slots": {"y2kr_" + m: by_id[m]["slot"] for m in members},
            "confusion_boundaries": [by_id[m]["confusion_boundary_ko"] for m in members],
            "source_keywords": [ko],
            "relations": [{"id": bid + "_owner_relation", "type": rel_type,
                "subject": "y2kr_" + subject, "object": "y2kr_" + obj}],
        })
    maintenance = {
        "id": "y2k-style-research-20260927", "status": "research_proposal_not_registered",
        "source_ledger_sha256": sha(HERE / "sources.json"),
        "seed_keywords_sha256": sha(HERE / "seed-keywords.json"),
        "component_tables_sha256": {name: sha(HERE / name) for name in ("components.tsv", "additional-components.tsv")},
        "source_metadata_excluded_from_runtime_positive_language": True,
        "claim_limits": ["the 308 rows are keyword seeds not 308 verified historical facts",
            "morphology records are proposed operational definitions not qualified images",
            "compiler validity does not establish real pack exposure selection or pixels",
            "unscoped prop candidates require explicit owner binding before adoption"],
    }
    extension = {
        "schema_version": "photo-prompt-research-extension/v1", "slots": dict(slots),
        "visual_semantics": runtime_bundles,
        "maintenance_ref": {"contract_version": semantics.MAINTENANCE_VERSION,
            "record_id": maintenance["id"], "sha256": semantics.digest(maintenance)},
    }
    write("maintenance.json", maintenance)
    write("style-families.json", {"schema_version": "y2k-style-taxonomy-proposal/v1", "families": FAMILIES})
    write("keyword-coverage.json", {"schema_version": "y2k-keyword-coverage/v1", "mappings": mappings})
    write("graphic-groups.json", {"schema_version": "y2k-graphic-groups/v1",
        "groups": [{"label": label, "component_ids": members.split(), "not_synonyms": True,
            "rule": "choose a literal motif and bind it to a garment print; actual text remains user controlled"} for label, members in GRAPHIC_GROUPS.items()]})
    write("semantic-components.proposed.json", {"schema_version": "y2k-semantic-component-proposal/v1",
        "global_rule": "all visible components and owner gates required; partial_is_fail; invisible_or_blocked_is_unscored",
        "components": components, "frame_groups": dict(frame_groups)})
    write("candidate-bundle-designs.json", {"schema_version": "y2k-candidate-bundle-design/v1", "bundles": bundle_designs})
    write("runtime-extension.proposed.json", extension)

    # Narrow audit of only authored direct entry fields. Generated sharded
    # indexes and large parent preset objects are never searched as dictionaries.
    tree = ast.parse((SCRIPTS / "prompt_generator.py").read_text())
    names = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "RESEARCH_EXTENSION_FILENAMES" for t in node.targets):
            for item in node.value.elts:
                names.append("photo_prompt_research_extension.json" if isinstance(item, ast.Name) else item.value)
    assert names
    authored_files = ["photo_prompt_tags.json"] + names
    audit_terms = ["y2k", "heisei", "gyaru", "mcbling", "spiky bun", "butterfly clip", "velour", "terry", "baguette", "bootcut", "low-rise", "low rise", "shield", "wraparound", "razr", "sidekick", "ipod", "nano", "zigzag", "rhinestone", "capri", "mall goth", "scene", "indie sleaze", "acubi", "frutiger", "holographic", "metallic", "retroreflective", "chrome", "crimp", "chunky highlights"]
    hits = {term: [] for term in audit_terms}
    fingerprints = {}
    direct_fields = ["id", "ko", "en", "label_ko", "label_en", "aliases", "keywords", "concept_units", "embedding_text", "description", "tags"]
    for name in authored_files:
        path = ASSETS / name
        fingerprints[name] = sha(path)
        value = json.loads(path.read_text())
        groups = [(slot, entries) for slot, entries in value.get("slots", {}).items()] + [("presets", value.get("presets", []))]
        for slot, entries in groups:
            for entry in entries:
                text = " ".join(str(entry.get(k, "")) for k in direct_fields).casefold()
                for term in audit_terms:
                    if term in text:
                        hits[term].append({"file": name, "slot": slot, "id": entry.get("id")})
    # Detect proposal collisions in the current authored dictionary, without
    # loading/building generated indexes or changing source files.
    known_ids = {entry["id"] for name in authored_files for entries in json.loads((ASSETS/name).read_text()).get("slots", {}).values() for entry in entries}
    proposed_ids = {entry["id"] for entries in slots.values() for entry in entries}
    assert not known_ids & proposed_ids
    sandbox = {"slots": copy.deepcopy(dict(slots)), "candidate_semantic_policy": policy}
    semantics.validate_extension_keys(extension)
    semantics.validate_candidate_entries(sandbox, dimensions)
    semantics.compile_extension_bundles(sandbox, extension)
    semantics.validate_bundle_references(sandbox, [])
    assert all(b["profile_activation"] == "independent_request_evidence_only" for b in sandbox["candidate_bundles"])
    # Synthetic contract fixture only: this is not a generator-produced pack.
    all_visible = {
        "authorial_core": {"intent_lock": {"open_dimensions": sorted(dimensions)}},
        "provenance": {"seed": "y2k-contract-fixture"},
        "slots": {slot: {"candidates": [{"id": "slot:" + slot + ":" + entry["id"],
            "applicability": {"status": "eligible"}, "conflicts_with": []} for entry in entries]} for slot, entries in slots.items()},
    }
    fixture_policy = copy.deepcopy(policy)
    fixture_policy["joint_adoption"]["maximum_bundles"] = len(runtime_bundles)
    fixture_data = {**sandbox, "candidate_semantic_policy": fixture_policy}
    fixture_exposed = semantics.public_bundles(fixture_data, all_visible)["candidates"]
    expected_scoped = {"bundle:y2kr_bundle_" + b["id"] for b in bundle_designs if not b["owner_binding_pending"]}
    assert {b["id"] for b in fixture_exposed} == expected_scoped
    closed = copy.deepcopy(all_visible)
    closed["authorial_core"]["intent_lock"]["open_dimensions"] = []
    assert not semantics.public_bundles(fixture_data, closed)["candidates"]
    assert len(semantics.public_bundles(sandbox, all_visible)["candidates"]) <= policy["joint_adoption"]["maximum_bundles"]
    unscoped = [c["id"] for c in components if not c["affected_dimensions"]]
    source_counts = Counter(s["access_status"] for s in sources)
    summary = {
        "schema_version": "y2k-research-validation/v1", "date": "2026-09-27",
        "repo_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "counts": {"seed_rows": len(seeds), "mapped_seed_rows": len(mappings),
            "component_records": len(components), "style_families": len(FAMILIES),
            "optional_bundle_proposals": len(runtime_bundles), "sources": len(sources),
            "source_access_status": dict(source_counts), "sources_with_direct_image_inspection": sum(s["image_directly_inspected"] for s in sources),
            "unscoped_component_records": len(unscoped), "audited_authored_files": len(authored_files)},
        "checks": {"unique_ids": "pass", "all_308_seed_rows_mapped": "pass",
            "family_component_and_source_references": "pass", "existing_slots_and_dimensions_only": "pass",
            "candidate_id_collisions_with_current_authored_sources": "none",
            "current_extension_key_validation": "pass", "current_candidate_validation": "pass",
            "current_bundle_compiler": "pass", "no_hard_profile_association": "pass",
            "synthetic_ordinary_exposure_fixture": "18 scoped bundles admitted; 2 unscoped device bundles excluded",
            "synthetic_all_dimensions_locked_fixture": "all proposed bundles excluded",
            "synthetic_default_bundle_cap_fixture": "at most 8 admitted",
            "maximum_members_per_bundle": max(len(b["candidate_ids"]) for b in runtime_bundles),
            "runtime_registration": "not_performed", "generated_index_build": "not_performed",
            "actual_pack_exposure": "not_tested", "candidate_selection": "not_tested",
            "image_generation": "not_performed", "pixel_qualification": "pending", "user_acceptance": "pending"},
        "unscoped_components_require_owner_binding": unscoped,
        "live_source_fingerprints": fingerprints,
    }
    write("current-data-gap-audit.json", {"schema_version": "y2k-authored-gap-audit/v1", "scope": "direct authored slot and preset fields only; substring hit is not semantic equivalence",
        "authored_files": authored_files, "hits": hits,
        "zero_hit_terms": [term for term, matches in hits.items() if not matches]})
    for component in components:
        assert set(component["source_refs"]) <= source_ids
    if (HERE / "qualification-plan.json").exists():
        qualification = read("qualification-plan.json")
        for row in qualification["render_pair_designs"]:
            assert set(row["positive_component_ids"] + row["comparison_component_ids"]) <= set(by_id)
        summary["counts"]["prospective_text_cases"] = len(qualification["text_cases"])
        summary["counts"]["prospective_render_pair_designs"] = len(qualification["render_pair_designs"])
    if (HERE / "era-compatibility.json").exists():
        for row in read("era-compatibility.json")["records"]:
            assert set(row["source_refs"]) <= source_ids
            if row.get("component_id"):
                assert row["component_id"] in by_id
    assert extension["maintenance_ref"]["sha256"] == semantics.digest(read("maintenance.json"))
    for name, fingerprint in fingerprints.items():
        assert sha(ASSETS / name) == fingerprint
    report = HERE / "report.ko.md"
    if report.exists():
        for target in re.findall(r"\]\(([^)]+)\)", report.read_text()):
            if target.startswith("/"):
                assert Path(target).is_file(), target
        summary["checks"]["local_report_links"] = "all_resolve"
    summary["checks"].update({
        "cross_file_source_and_component_references": "pass",
        "maintenance_reference_sha256": "pass",
        "live_authored_sources_unchanged_after_research": "pass",
    })
    write("validation.json", summary)
    print(json.dumps(summary["counts"], ensure_ascii=False, indent=2))
    print("Research proposal contract checks passed; runtime and pixels remain untested.")


if __name__ == "__main__":
    main()
