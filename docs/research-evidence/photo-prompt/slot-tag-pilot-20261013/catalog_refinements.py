"""Apply four individually authored role boundaries discovered in the pilot."""
import copy
import json
from pathlib import Path
import sys
from sample import HERE, SKILL

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c


def role(tag, description, ko, dimensions, prefixes, terms, includes, excludes, neighbors):
    return {"id": tag, "description": description, "description_ko": ko,
        "dimensions": dimensions, "applicability": {}, "semantic_role": "direct",
        "owners": ["actor"], "property_prefixes": prefixes, "evidence_terms": terms,
        "includes": includes, "excludes": excludes, "neighbors": neighbors,
        "core_fields": ["subject", "event", "visual_priorities"], "priority": "support"}


NEW_ROLES = {
    "gaze_direction": role("gaze_direction",
        "Owned eye or iris orientation toward a direction in the selected frame, independent of head orientation, a named gaze target and viewer engagement.",
        "같은 주체 눈·홍채의 선택 프레임 내 방향. 머리 방향·시선의 명명 대상·눈맞춤 여부와 독립하며 감은 눈이나 동공 모양으로 방향을 추정하지 않는다.",
        ["expression"], ["gaze.direction", "eyes.direction", "eyes.eyeline"],
        ["iris", "irises", "eye direction", "eyeline", "looking back", "시선 방향", "홍채"],
        ["Upward iris direction without a named target.", "An authored over-shoulder eye direction when that branch is selected."],
        ["Head or body turn alone.", "Eye closure, pupil shape or private intent.", "Named gaze target or engagement alone."],
        ["body_orientation", "eye_detail", "expression", "gaze_engagement", "gaze_target"]),
    "nail_appearance": role("nail_appearance",
        "Visible shape, length, color, finish or decoration of an owned fingernail or toenail plate, separate from skin marks and joint pose.",
        "소유자가 명시된 손톱·발톱 판의 보이는 모양·길이·색·마감·장식. 피부의 문양·손 관절 자세·손가락 길이와 구별하며 건강이나 정체성을 진단하지 않는다.",
        ["appearance", "color", "material"], ["nails.", "nail.", "makeup.nails"],
        ["nail", "nails", "manicure", "pedicure", "손톱", "발톱"],
        ["Light free-edge band distinct from a nail's base color.", "Named nail plate shape, length or finish."],
        ["Skin pigment or a tattoo on a finger.", "Hand pose or finger proportions.", "Clinical diagnosis, ancestry or age inferred from nails."],
        ["body_marking", "body_region", "color", "hand_pose", "makeup_decoration", "skin_finish", "texture"]),
    "body_form": role("body_form",
        "Owned non-facial anatomical contour, regional volume or visible muscle and tendon form, independent of connection topology, relative proportions, pose and garment fit.",
        "같은 주체의 얼굴 이외 신체에서 보이는 해부학적 윤곽·국소 부피·근육·힘줄 형태. 부위 이름·연결 구조·상대 비율·자세·의복 부피와 독립하며 체중·건강·능력·정체성을 추정하지 않는다.",
        ["body_geometry", "appearance"], ["body.form", "body.contour", "body.morphology", "body.muscle", "body.tendon", "body.build", "body.gluteal_thigh_boundary"],
        ["muscle", "tendon", "contour", "body build", "body form", "vein contour", "근육", "힘줄", "윤곽"],
        ["Restrained visible muscle planes on the declared subject.", "A localized neck vein contour or gluteal-thigh surface fold.", "Depicted anatomy remains owned by its declared representation."],
        ["Body region names or skeletal connectivity alone.", "Relative body proportions, garment fit, pose or facial geometry alone.", "Body weight, health, strength, age or origin inferred from contour.", "An artifact's depicted body does not alter a live actor's body."],
        ["anatomical_connection", "body_pose", "body_region", "facial_geometry", "garment_fit", "silhouette_proportion", "skin_finish", "texture"]),
}


def main():
    path = SKILL / "assets/photo_candidate_slot_catalog.json"
    module = c.decode(path.read_bytes())
    frozen = c.decode((HERE / "CATALOG.json").read_bytes())
    if module["slot_catalog"] != frozen:
        raise ValueError("Catalog changed since review; reread before applying refinements")
    source = c.validate(c.load(SKILL / "assets"))
    before = c.digest(source)
    catalog = copy.deepcopy(frozen)
    catalog.update(NEW_ROLES)
    skin = catalog["skin_tone"]
    skin.update({
        "description": "Owned skin color and local color variation under declared illumination and white balance, distinct from cosmetics and image grading; apparent color does not prove intrinsic pigment or identity.",
        "description_ko": "같은 피부 부위의 색과 국소 색 변이. 조명·화이트밸런스 기준이 명시된 보이는 색도 포함하되, 그 색으로 고유 색소·민족·정체성을 역추정하지 않으며 화장·그레이딩과 구별한다.",
        "property_prefixes": ["skin.color", "skin.tone", "complexion.color", "body.skin.color", "body.skin.tone", "body.skin.apparent_color"],
        "evidence_terms": ["skin tone", "skin color", "complexion", "pigment", "피부톤", "피부색", "피부의 보이는 색"],
        "includes": ["Owned skin color or local variation.", "Apparent color of a named skin region with capture illumination and white balance declared."],
        "excludes": ["Light color, cosmetic pigment, textile lining color or image grading alone.", "Apparent skin color without its observation conditions cannot establish intrinsic pigment, ancestry or identity."],
    })
    projected = {**source, "slot_catalog": catalog}
    c.validate(projected)
    assert all(catalog[tag] == spec for tag, spec in frozen.items() if tag != "skin_tone")
    changes = [{"slot_id": tag, "action": "add" if tag in NEW_ROLES else "refine",
        "before": frozen.get(tag), "after": catalog[tag],
        "pilot_cases": {"gaze_direction": [113, 418], "nail_appearance": [354],
            "body_form": [26, 27, 371], "skin_tone": [607]}[tag]}
        for tag in [*NEW_ROLES, "skin_tone"]]
    (HERE / "CATALOG-CHANGES.json").write_text(json.dumps({"schema": "photo-slot-pilot-catalog-changes/v1",
        "before_corpus_sha256": before, "after_corpus_sha256": c.digest(projected),
        "before_count": len(frozen), "after_count": len(catalog), "changes": changes,
        "unchanged_native_payloads_conditions_effects_bindings_policies": True}, ensure_ascii=False, indent=2) + "\n")
    module["slot_catalog"] = catalog
    path.write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"before_slots": len(frozen), "after_slots": len(catalog),
        "source_sha256": c.digest(c.validate(c.load(SKILL / "assets")))}))


if __name__ == "__main__":
    main()
