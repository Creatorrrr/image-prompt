#!/usr/bin/env python3
"""Compile the reviewed, optional visual projection of both returned reports.

Raw reports remain immutable evidence. The decisions below are local review,
not an instruction to execute an external analyst's integration map. Different
actions/owners are independent atoms; equivalent notes enrich existing atoms.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
NAME = "photo_prompt_contextual_appeal_extension"


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


# These records chiefly supply interpretation, not a new visual configuration.
# Qualify notes by the existing atom instead of broadening its positive meaning.
ACADEMIC_CONTEXT = {
    "self-glove-stop": "sff_pro_p02",
    "chosen-restraint-language": "sff_pro_y03",
    "bra-over-shirt-self-style": "sff_pro_y02",
    "obi-ornament-not-binding": "kimono_obi_obijime_layer",
    "focus-with-person": "sff_pro_k03",
    "light-material-not-arousal": "sff_pro_l11",
    "leather-fashion-only": "sff_pro_y06",
    "heels-function-only": "sff_pro_b07",
    "mesh-sport-only": "sff_pro_y04",
    "object-interest-without-exposure": "sff_pro_k03",
    "request-nonsexual-version": "sff_pro_k01",
    "self-covering-choice": "sff_pro_y04",
    "fuller-body-fit-agency": "sff_pro_p10",
    "queer-style-not-inference": "sff_pro_x03",
    "private-not-secret": "sff_pro_x08",
    "learned-association-caution": "character_signature_object_scene_action",
    "uncertain-sensory-reading": "mep_environment_relation_candidate",
    "interest-not-diagnosis": "sff_pro_k04",
    "collector-not-fetish": "character_signature_object_scene_action",
    "expressive-without-costume": "sff_pro_p04",
}
COMMUNITY_CONTEXT = {
    "C021": "small_eyebrow_scar", "C024": "sff_pro_p07",
    "C027": "performing_competency_task", "C037": "short_bob_hair",
    "C040": "soft_peach_fuzz_detail", "C046": "gonial_angle_definition",
    "C111": "hairline_contour_shape", "C112": "central_abdominal_projection_relation",
    "C117": "realistic_skin_texture_no_retouch", "C118": "candid_unaware_of_camera",
    "C125": "emotional_teary_eyes", "C128": "candid_unaware_of_camera",
    "C139": "central_abdominal_projection_relation", "C152": "calf_to_ankle_taper",
    "C154": "rounded_gluteal_projection", "C155": "realistic_skin_texture_no_retouch",
    "C156": "same_adult_target_coordinated_gaze",
}
# Authored paraphrases express the existing atom only. No whole proposed scene
# is appended to a garment, body detail, or role-specific entry as a synonym.
PARAPHRASES = {
    "sfr26.self-glove-stop": ["the wearer's free fingers rest on the opposite glove cuff", "본인의 반대 장갑 커프에 쉬듯 닿은 손가락"],
    "sfr26.light-material-not-arousal": ["broad soft panel highlights follow the folds of a garment", "옷 주름을 따르는 넓고 부드러운 면 반사"],
    "C024": ["fingertips adjust the earring fastening with the face clear of the hand", "얼굴을 가리지 않는 귀걸이 고정부 조절"],
    "C027": ["skilled hands work beside a directly inspectable task result", "직접 확인할 수 있는 작업 결과와 숙련된 손"],
    "C040": ["natural fine vellus hair on skin", "피부의 자연스러운 미세 솜털"],
    "C125": ["a natural tearful expression", "자연스럽게 눈물이 맺힌 표정"],
    "C128": ["gaze attends to the ongoing activity rather than the camera", "카메라보다 하던 일에 머무는 시선"],
    "C155": ["natural skin surface detail retained in a portrait", "인물 사진에 남은 자연스러운 피부 표면"],
}

# Community effects were not supplied as runtime-ready scopes. These are
# explicitly reviewed visual effects, not a keyword classifier in retrieval.
COMMUNITY_SCOPES = {}


def scope(ids, slot, dimensions, property_path=None):
    for cid in ids.split():
        COMMUNITY_SCOPES[cid] = (slot, dimensions.split(), property_path)


scope("C001 C007 C014 C022 C023 C055 C056 C069 C070 C085 C089 C104 C106 C107 C110 C113 C121 C137 C146 C148", "action", "action pose")
scope("C003 C058 C134 C158", "action", "action pose appearance", "wardrobe.wearing_state")
scope("C002 C005", "action", "action pose appearance", "accessories.eyewear")
scope("C008 C013 C017 C038 C081 C082 C083 C100 C105 C108 C130 C141", "body_pose", "action pose")
scope("C009 C015 C072 C073 C077 C078 C079 C136 C143", "relational_action", "action pose expression")
scope("C011 C129 C132", "action", "action pose appearance", "hair.style")
scope("C012", "action", "action pose appearance", "makeup.wear_state")
scope("C018 C063 C071 C093 C095 C096 C099 C101 C133 C135 C150", "wardrobe_style", "appearance material", "wardrobe")
scope("C019 C031 C060", "wearable_accessory", "appearance material", "accessories")
scope("C025 C026 C043 C044 C045 C051 C052 C092 C119 C120 C122 C126", "expression", "expression")
scope("C016 C029 C033 C034 C039 C067 C084 C138", "anatomical_connection", "body_geometry appearance", "body")
scope("C035 C036 C053 C153 C157", "anatomical_connection", "body_geometry appearance", "face")
scope("C109 C140", "skin_finish", "appearance", "body.skin")
scope("C042 C049", "skin_finish", "appearance", "body.skin")
scope("C041", "body_framing", "framing composition")
scope("C020 C064", "body_pose", "action pose expression appearance body_geometry", "body")
scope("C059", "wardrobe_style", "appearance material", "wardrobe")
scope("C062", "hair_style", "appearance", "hair.style")
scope("C086", "action", "action pose expression appearance", "accessories.mask")
scope("C094", "action", "action pose appearance", "wardrobe.wearing_state")
scope("C098 C102", "action", "action pose appearance", "wardrobe.wearing_state")
scope("C116", "hair_color", "appearance", "hair.color")
scope("C149", "brow_style", "appearance", "face.brows")
scope("C151", "body_marking", "appearance", "body.markings")
scope("C025 C043 C044 C045", "expression", "expression appearance body_geometry", "face")
scope("C051 C052 C120", "expression", "expression action pose")
scope("C119 C122", "expression", "expression pose")
scope("C126", "expression", "expression action")
scope("C063 C071 C093 C101", "wardrobe_style", "appearance material action pose", "wardrobe")
scope("C099", "wardrobe_style", "appearance material body_geometry", "wardrobe")
scope("C031", "wearable_accessory", "appearance material body_geometry", "accessories.rings")
scope("C089", "action", "action pose appearance", "body.hands.nails")

ACADEMIC_SCOPES = {
    "pile-turn": ("surface_material", ["material", "appearance", "action"], "wardrobe.material"),
    "rib-flatten": ("action", ["action", "pose", "appearance", "material"], "wardrobe.wearing_state"),
    "inside-seam-choice": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "rolled-sleeve-task": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "loose-tie-after-duty": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "requested-collar-fix": ("relational_action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "sari-self-drape-adjust": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "work-shirt-own-fit": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "coat-settling": ("action", ["action", "pose", "appearance"], "wardrobe.wearing_state"),
    "opaque-under-sheer-layer": ("wardrobe_style", ["appearance", "material"], "wardrobe"),
    "soft-tailored-full-look": ("wardrobe_style", ["appearance", "material", "pose"], "wardrobe"),
    "masculine-lace-own-choice": ("wardrobe_style", ["appearance", "material"], "wardrobe"),
    "body-not-garment-sculpture": ("garment_detail", ["appearance", "material"], "wardrobe.construction"),
    "breeze-adjustment": ("action", ["action", "pose", "atmosphere"], None),
}


def all_existing():
    output = {}
    for path in sorted(ASSETS.glob("*.json")):
        if path.stem == NAME:
            continue
        data = read(path)
        if not isinstance(data, dict):
            continue
        for slot, entries in data.get("slots", {}).items():
            for row in entries:
                output.setdefault(row["id"], []).append((path, slot, row))
    return output


def main():
    academic = read(HERE / "research/academic/candidate-research.json")["candidates"]
    community = read(HERE / "research/community/community-candidate-research.json")["records"]
    assert len(academic) == 150 and len(community) == 158
    existing = all_existing()
    slots, updates, ledger = {}, {}, []
    # Exact visible equivalents across the two reports share one new atom.
    cross_report = {"C058": "sfr26.loose-tie-after-duty"}
    assigned = {}
    for origin, records in [("academic", academic), ("community", community)]:
        for row in records:
            academic_row = origin == "academic"
            rid = row["stable_id"] if academic_row else row["candidate_research_id"]
            short = rid.removeprefix("sfr26.")
            recommendation = row["integration_action"] if academic_row else row["integration_recommendation"]
            positive = row["positive_retrieval_surface"] if academic_row else row["positive_retrieval_proposal"]
            label = row["label_ko"] if academic_row else row["plain_korean_meaning"]
            record = {"origin": origin, "research_id": rid, "source_ids": row["source_ids"],
                      "reported_recommendation": recommendation, "label_ko": label}
            if recommendation == "defer" or not positive["en"]:
                record.update(operation="research_only", reason="Core observation is not established by a single photograph, or the source-specific design is underspecified; retain full record and proposed evaluation in the research archive.", runtime_ids=[])
                ledger.append(record)
                continue
            context = {
                "id": "context_" + rid.replace(".", "_").replace("-", "_"),
                "ordinary": row["ordinary_reading"],
                "expressive": (row["explanation_layers"]["researcher_interpretation"] if academic_row else {
                    "sensual": row["possible_sensual_reading"]["reading"],
                    "fetish": row["possible_fetish_reading"]["reading"]}),
                "limits": (row["counterexamples"] if academic_row else row["visual_limitations"]),
                "status": "optional_contextual_reading; visible configuration is not proof of desire or a universal preference",
            }
            target_id = (ACADEMIC_CONTEXT.get(short) if academic_row else COMMUNITY_CONTEXT.get(rid))
            if rid in cross_report:
                target_id = assigned[cross_report[rid]]
                path, slot, target = None, "action", next(x for x in slots["action"] if x["id"] == target_id)
                target["contextual_usage"]["contexts"].append(context)
                record.update(operation="merge_equivalent", runtime_ids=[target_id], reason="Same after-duty necktie loosening relation already supplied by the other report; preserve both evidence origins without duplicating a candidate.")
            elif target_id:
                matches = existing[target_id]
                assert len(matches) == 1, (rid, target_id)
                path, slot, target = matches[0]
                context["scope"] = "Applies only when the existing candidate's complete object, owner, action and material definition already holds; this note does not substitute the broader research example."
                addition = updates.setdefault(slot, {}).setdefault(target_id, {"contexts": []})
                addition["contexts"].append(context)
                if rid in PARAPHRASES:
                    addition.setdefault("paraphrases", []).extend(PARAPHRASES[rid])
                record.update(operation="enrich_existing", runtime_ids=[target_id], target_path=str(path.relative_to(ROOT)), slot=slot, reason="Interpretation context qualified by existing meaning; only separately reviewed equivalent paraphrases enter search. Existing effects and guards remain unchanged.", positive_search_added=rid in PARAPHRASES)
            else:
                target_id = "ctx_" + (short.replace("-", "_") if academic_row else rid.lower())
                assert target_id not in existing
                en = positive["en"][0]
                ko = positive["ko"][0]
                if academic_row:
                    dims = row["affected_dimensions"]
                    slot = "composition" if set(dims) <= {"composition", "lighting"} else "action"
                    prop = "wardrobe" if "appearance" in dims else None
                    slot, dims, prop = ACADEMIC_SCOPES.get(short, (slot, dims, prop))
                else:
                    assert rid in COMMUNITY_SCOPES, (rid, "missing authored scope")
                    slot, dims, prop = COMMUNITY_SCOPES[rid]
                context["application_conditions"] = [
                    "This is an optional configuration, not a sensual/fetish classification.",
                    "Every mentioned actor, object, garment and place outside the declared change scope must already be established in the frozen core; otherwise the candidate is inapplicable.",
                    "Any actual wardrobe, material, appearance or scene change must fit the declared effects and the current property locks.",
                    "Established reference appearance and requester-owned identity remain unchanged; natural physical traits are alternatives only when explicitly open.",
                ]
                candidate = {
                    "id": target_id, "ko": ko, "en": en, "weight": 0.42,
                    "tags": ["human", "adult", "contextual_visual_relation"], "for_any": ["human"],
                    "aliases": [], "paraphrases": list(dict.fromkeys(positive["en"][1:])),
                    "concept_units": [en],
                    "relations": [{"id": target_id + "_relation", "type": "visible_configuration",
                                   "subject": "the established adult subject and scene elements", "object": en}],
                    "affected_dimensions": sorted(set(dims)),
                    "expression_scope": "whole_direction" if slot == "wardrobe_style" else "construction_or_material" if slot in {"garment_detail", "wearable_accessory", "surface_material"} else "portrayal_or_scene_relation",
                    "contextual_usage": {"contexts": [context]},
                }
                if prop:
                    candidate["affected_properties"] = [{"dimension": "appearance", "target": "main_subject", "property": prop}]
                slots.setdefault(slot, []).append(candidate)
                record.update(operation="add_visual_relation", runtime_ids=[target_id], slot=slot,
                              affected_dimensions=candidate["affected_dimensions"], reason="The complete visible relation differs from reported neighbors in action, owner, object, material or scope. It is an optional atom, not a synonym of a partially matching neighbor.")
            assigned[rid] = target_id
            ledger.append(record)
    assert len(ledger) == 308
    output = {"schema_version": "photo-prompt-research-extension/v1",
              "slots": dict(sorted(slots.items())), "existing_slot_context_extensions": updates}
    plan = {"schema_version": "photo-reviewed-research-integration/v1", "records": ledger,
            "counts": dict(Counter(r["operation"] for r in ledger)),
            "new_runtime_candidates": sum(map(len, slots.values())),
            "enriched_existing_candidates": sum(map(len, updates.values())),
            "new_slot_counts": {slot: len(rows) for slot, rows in sorted(slots.items())},
            "limits": ["All research records retained; source access statements are the external researchers' reports, not new local source visits.",
                       "Search and image verification are recorded separately; research proposals are not successful test results.",
                       "No intrinsic sensual/fetish flags, universal attraction score, or exposure default was added.",
                       "Nonvisual observations and proposed multi-frame comparisons are archived, not misrepresented as observable still-image cues."]}
    write(HERE / "integration-ledger.json", plan)
    maintenance = {"contract_version": "photo-extension-maintenance/v1", "record_id": NAME,
                   "source_filename": NAME + ".json", "authored_source_sha256": digest(plan),
                   "runtime_keys": ["slots", "existing_slot_context_extensions"],
                   "maintenance_only": {"review_ledger": str((HERE / "integration-ledger.json").relative_to(ROOT)),
                                        "raw_evidence": str((HERE / "research").relative_to(ROOT)),
                                        "scope": "Optional positive visual relations and context; no research prose or source URLs in search input."}}
    write(HERE.parent / "extension-maintenance" / (NAME + ".json"), maintenance)
    output["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": NAME, "sha256": digest(maintenance)}
    write(ASSETS / (NAME + ".json"), output)
    tags = read(ASSETS / "photo_prompt_tags.json")
    required = tags["candidate_semantic_policy"]["required_extensions"]
    if NAME + ".json" not in required:
        path = ASSETS / "photo_prompt_tags.json"
        raw = path.read_text()
        marker = '"photo_prompt_sensual_fetish_fashion_extension.json"'
        assert raw.count(marker) == 1
        path.write_text(raw.replace(marker, marker + ',\n      "' + NAME + '.json"'))
    print(json.dumps({key: value for key, value in plan.items() if key != "records"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
