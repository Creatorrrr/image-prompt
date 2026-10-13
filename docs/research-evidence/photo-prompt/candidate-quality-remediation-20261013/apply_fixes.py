"""Apply the reviewed 1,000-sample quality fixes, retaining native identities.

This is a bounded maintenance record, not a runtime migration or tag classifier.
Run without --write to inspect the proposed ledger before writing source modules.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
AUDIT = HERE.parent / "candidate-quality-random-1000-20261013"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as corpus
import photo_global_index as index
from photo_embedding_provider import atomic


def replace_strings(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_strings(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, old, new) for key, item in value.items()}
    return value


def propose(source):
    result = copy.deepcopy(source)
    samples = {row["sample_number"]: row for row in map(
        json.loads, (AUDIT / "samples.jsonl").read_text().splitlines())}
    for sample in samples.values():
        cid = sample["candidate"]["id"]
        if corpus.digest(source["candidates"][cid]) != sample["record_sha256"]:
            raise ValueError(f"audited source changed before remediation: {cid}")
    reasons = {}

    def record(number, reason):
        cid = samples[number]["candidate"]["id"]
        reasons.setdefault(cid, []).append(reason)
        return result["candidates"][cid]

    def content(number, reason):
        return record(number, reason)["content"]

    def english(number, value, reason):
        row = record(number, reason)
        old = row["content"]["en"]
        row["content"] = replace_strings(row["content"], old, value)
        row["content"]["en"] = value
        return row["content"]

    def effects(number, dimensions, properties):
        row = record(number, "Align effects with the actual owner and modified properties.")
        row["effects"] = {"dimensions": dimensions, "properties": [
            {"dimension": dimension, "target": target, "property": prop}
            for dimension, target, prop in properties]}
        for binding in result["slot_bindings"].values():
            if binding["candidate_id"] == row["id"]:
                binding["effects"] = copy.deepcopy(row["effects"])
        return row

    # Translate the 45 labels explicitly identified as lacking Korean.
    korean = {
        1: "발광 스틱 소품", 33: "젖은 흙에서 일하는 논농사 농부",
        61: "서비스 카운터를 사이에 둔 예의 있는 거리",
        71: "여백을 둔 상품 플랫레이", 74: "소리쳐 부르는 순간의 표정",
        108: "드레스의 하트형 몸판 가장자리와 높은 네크라인을 잇는 얇은 메시 패널",
        120: "작은 인물과 주변 대상 사이의 크기 대비", 149: "CCTV 모니터 벽 앞",
        152: "도자기 인형을 연상시키는 메이크업", 171: "인형 관절을 조심스럽게 조정하는 동작",
        195: "공연장 취재 구역의 플래시 촬영 맥락",
        245: "코케트 스타일의 티 테이블을 위에서 내려다보는 플랫레이",
        264: "블라우스의 긴 목 끈으로 칼라 바로 아래에 만든 두 리본 고리",
        283: "이를 악물고 힘쓰는 표정", 311: "작업장 안전 점검 사진",
        317: "먼지가 이는 승마 훈련장", 331: "창작 의례용 여신 드레이프 의상",
        398: "도표 형식 없이 한 장면을 사진처럼 표현한 이미지",
        401: "낡은 삼각모 소품", 453: "풍성한 봄버 재킷 몸판이 좁은 리브 허리밴드로 모이는 연결",
        459: "코트의 칼라 밑에서 양쪽 겨드랑이로 이어지는 래글런 봉제선",
        466: "소매 커프의 구멍으로 엄지가 나오고 같은 손등을 덮는 긴 소매",
        468: "선택적으로 더하는 아가미 선 흔적과 젖은 잉어 비늘 같은 광택",
        508: "브러시 처리한 강철의 미세한 결", 517: "라탄을 엮은 표면 질감",
        546: "실물과 자세가 어긋나 지연을 연상시키는 거울상",
        551: "읽을 수 있는 글자 없이 쌓인 MP3 플레이어·빈 CD·스티커",
        594: "진주광택이 도는 조개껍질 표면",
        595: "수정·허브·촛불·읽을 수 없는 카드로 구성한 신비로운 마녀풍 정물",
        598: "무거운 샌드백을 치는 동작", 614: "부드럽게 옅어지는 소품 그림자",
        626: "부드러운 스웨이드 기모", 627: "창고에서 열리는 레이브",
        630: "물속에 떠 있는 상태", 665: "검은색 앤티크 회전식 전화기 소품",
        672: "자외선 손전등 소품", 690: "도로변에서 배달 경로를 확인하는 상황",
        717: "탁자 위 자료를 내려다보는 카메라 높이", 752: "루페로 시계 무브먼트를 점검하는 동작",
        763: "풍선 하나 소품", 776: "셔츠 앞단만 바지 허리밴드에 넣고 옆단과 뒷단은 밖에 둔 상태",
        785: "후드 개구와 꼬리 틈을 함께 보여 의상 장식과 살아 있는 신체를 구분하는 상태",
        860: "좌석 하나를 비워 둔 거리", 919: "같은 착용자의 허리에서 끝나고 앞판이 겹치는 크롭 블레이저",
        983: "입술을 다물고 시선을 고정한 집중 표정",
    }
    for number, text in korean.items():
        content(number, "Supply a Korean description matching the concrete English meaning.")["ko"] = text

    # Align the 23 scope differences. Preserve explicit actors, owners and variants.
    english(2, "one adult turns their head toward another adult whose shoe meets the floor",
            "Restore the head-direction owner rather than changing the whole body.")
    row = content(27, "Replace a component-number label and broader crop aliases with this exact component.")
    row["ko"] = "얼굴의 초점이 화면의 기하학적 중심에서 벗어난 배치"
    row["aliases"] = ["off-center face focal point", row["ko"]]
    row["keywords"] = list(row["aliases"])
    row["embedding_text"] = row["en"] + " | " + row["ko"]
    english(59, "an adult seeker's hand is about to reach a partly exposed sealed cache that remains fixed in its original position and has not transferred to the seeker",
            "Preserve the adult hand, pre-contact state and anchored cache.")
    english(115, "the outer robe has narrow sleeves and a readable front closure", "Restore the narrow sleeve value.")
    content(154, "Name the concrete selected two-adult subject rather than an equivalent abstract topic.")["ko"] = "숙련된 성인 제작자와 성인 동료"
    row = content(154, "Keep aliases within this actor set; the thematic label is not an equivalent subject.")
    row["aliases"] = [row["ko"], row["en"]]
    effects(154, ["subject", "count"], [("count", "scene", "adult_actor_count")])
    english(196, "lichen-and-moss-covered bark surface", "Preserve both organisms named in Korean.")
    row = record(209, "Remove unscoped dusk from an action whose Korean meaning leaves timing open.")
    row["content"] = replace_strings(row["content"], " at dusk", "")
    content(239, "Replace a generic topic template with the actual selected place.")["ko"] = "배송 거점의 건조 작업 구역"
    english(284, "moving the pallet in response to a spotter's signal only while the spotter maintains the marked loading boundary",
            "Preserve the signal and maintained loading boundary.")
    content(288, "Align adult count, shared target and non-occlusion in both languages.")["ko"] = "두 성인이 같은 기능 접점을 양쪽에서 가리지 않고 확인하는 동작"
    english(320, "checking food temperature, the order ticket and hygiene before releasing one completed dish through the kitchen pass",
            "Restore the hygiene check already present in Korean.")
    content(377, "State the selected drink and office-desk realization in Korean.")["ko"] = "음료를 들고 사무실 책상으로 돌아가는 동작"
    content(603, "Scope this selected leggings variant to the ankle hems actually described.")["ko"] = "별도 허리밴드와 두 다리의 발목선 밑단을 가진 수영 레깅스"
    content(693, "Name the concrete prop pair instead of equating it to an abstract theme.")["ko"] = "절반쯤 수리된 비고유 기계 부품과 손목 받침"
    row = record(705, "Preserve the wig carrier explicitly selected by the Korean description.")
    row["content"] = replace_strings(row["content"], "styled hair", "styled wig")
    content(750, "Align the caption with the selected fatigue/support action without adding an unsupported injury.")["ko"] = "정밀 수리를 지휘하다 피로가 드러나 잠시 멈추고 다음 작업의 선택권을 유지하며 도움을 받아들이는 동작"
    row = english(787, "a divination abacus with beads resting at intermediate positions along their rods",
                  "Disambiguate resting beads from autonomous movement.")
    row["ko"] = "주판알이 막대의 중간 위치에 놓인 점술용 주판"
    row["claim_limits"] = ["The divination use is authored context; bead positions alone do not establish autonomous motion or a supernatural result."]
    content(794, "Keep repeated observation as intended use, with one present place state and stable anchors.")["ko"] = "재관찰의 기준이 될 문·고정물·가장자리·수평선에 맞춰 정리된 한 장소의 상태"
    content(800, "Replace the component-number label with the actual near-setting hand-activity constraint.")["ko"] = "가까운 주변 공간에서 구체적인 손동작 하나가 가리지 않고 읽히는 상태"
    english(855, "a red Lunar New Year lantern prop", "Restore the explicitly red lantern color.")
    content(897, "Replace an unrelated topic template with the actual coastal location.")["ko"] = "바람이 부는 해안 전망 산책로"
    content(905, "Name the leg and underarm owners of retained natural body hair.")["ko"] = "다리와 겨드랑이의 자연 체모를 유지한 성인 여성"
    row = content(1000, "Distinguish face orientation and visible eye direction; replace the component-number label.")
    row["ko"] = "높은 가까운 카메라 쪽으로 든 얼굴 또는 그 카메라를 향하는 보이는 눈의 방향"
    row["claim_limits"] = ["Face orientation and eye direction are separate observations; a raised face alone does not establish camera eye contact."]

    # Correct five verified semantic mismatches and the unsupported seam detail.
    row = record(83, "Hook-and-eye back-band closure is a different component from shoulder-strap adjustment.")
    row["content"] = replace_strings(row["content"], "bra strap detail", "bra back-band closure")
    row["content"] = replace_strings(row["content"], "wardrobe.details.bra_strap_adjust", "wardrobe.details.bra_back_band_closure")
    boundary = "훅앤아이는 같은 브라 뒷밴드 개구의 양쪽을 잇는다. 어깨끈 길이 조절 링·슬라이더와 구분한다."
    row["content"]["semantics"]["contrast_examples"] = [boundary]
    row["content"]["reject_substitutes"] = [boundary]
    effects(83, ["appearance"], [("appearance", "main_subject", "wardrobe.details.bra_back_band_closure")])
    row = content(123, "Make the NASA-documented near-edge-on view a selected variant, not every accretion-disk view.")
    row["activation"]["exact_terms"] = ["nearly edge-on relativistic accretion-disk visualization",
        "nearly edge-on lensed far-side accretion disk around black hole", "거의 옆에서 본 상대론적 강착원반 중력렌즈 시각화"]
    row["semantics"]["definition"] = "This selected nearly edge-on relativistic black-hole accretion-disk visualization shows a luminous disk, a dark central shadow, far-side light bent above and below the shadow, and side-to-side Doppler-like brightness asymmetry. These visible arcs and brightness asymmetry are view-dependent; this profile does not define a face-on view or every accretion-disk visualization."
    view = "the accretion disk is viewed nearly edge-on rather than directly face-on"
    row["semantics"].setdefault("claim_limits", []).append("At a directly face-on view, side-to-side Doppler brightness asymmetry disappears; other viewing angles require their own selected components.")
    row["semantics"].setdefault("visual_components", []).append(view)
    row["semantics"]["component_semantics"]["groups"].append({"id": "viewing_angle", "any_terms": [view]})
    row["semantics"]["component_semantics"]["required_group_ids"].append("viewing_angle")
    row["semantics"]["component_semantics"]["minimum_component_groups"] = 5
    row["authored_components"]["components"].append({"id": "viewing_angle", "match_terms": [view]})
    row["authored_components"]["discovery"]["required_group_ids"].append("viewing_angle")
    row["authored_components"]["discovery"]["minimum_component_groups"] = 5
    obligation = row["authored_components"]["obligations"][0]
    obligation["component_ids"].append("viewing_angle")
    requirement = {"min_content_words": 7, "must_mention_any": [view]}
    obligation["evidence"].append({"field": "viewing_angle_phrase", "requirement": requirement})
    row["required_evidence_fields"].append("viewing_angle_phrase")
    row["evidence_requirements"]["viewing_angle_phrase"] = copy.deepcopy(requirement)
    gate = {"id": "vo_space_accretion_viewing_angle", "review_scale": "both", "description": view}
    obligation["render_gates"].append(gate)
    row["render_gates"].append(copy.deepcopy(gate))
    row["composition_instruction"] = obligation["instruction"] = "Show this selected nearly edge-on disk view with its shadow, far-side lensing and side-to-side brightness difference."
    row = record(278, "Use the mustache documented for the selected Cambodian work, not a beard.")
    row["content"] = replace_strings(row["content"], "its beard and third eye", "its mustache and third eye")
    row["content"] = replace_strings(row["content"], "시바 수염·제삼안", "시바 콧수염·제삼안")
    for cid in ("cand_11c8bac53d3b53b4b945954771e44d06", "cand_2e0e917fc95156d8afb39627c34359cc"):
        related = result["candidates"][cid]
        if "its beard and third eye" not in json.dumps(related["content"], ensure_ascii=False):
            raise ValueError("selected iconography companion changed before review: " + cid)
        related["content"] = replace_strings(related["content"], "its beard and third eye", "its mustache and third eye")
        reasons.setdefault(cid, []).append("Propagate the documented mustache correction through the same selected variant's option and bundle; preserve member and profile references.")
    row = content(503, "Separate EL-wire synonyms from gas-discharge glass-tube aliases.")
    row["aliases"] = ["EL wire", "electroluminescent wire", "EL 와이어", "전계발광 와이어"]
    row["keywords"] = list(row["aliases"])
    row["claim_limits"] = ["An EL wire is distinct from a gas-discharge glass tube. Visible emission geometry alone does not prove hidden electrical or material construction."]
    row = content(263, "Retain the exposed glove seam confirmed by Dents, without claiming an unverified butted-edge construction.")
    row["ko"] = "바깥으로 드러난 장갑 봉제선"
    row["en"] = "prix seam with an exposed outer glove seam"
    row["aliases"] = ["prix seam", "prixseam", row["ko"]]
    row["embedding_text"] = "prix seam; exposed outer glove seam; 바깥으로 드러난 장갑 봉제선"
    row["concept_units"] = ["an exposed seam along the glove outer boundary", "노출된 장갑 외곽 박음선"]
    row["claim_limits"] = ["The cited manufacturer describes an exposed seam; this candidate makes no additional claim about butted edges."]

    # Clarify bounded fictional/expressive realizations; do not universalize labels.
    row = english(20, "adult-only social-media context with an intentionally suggestive gaze and pose",
                  "Replace undefined borderline wording with an authored expressive context, not a safety classification.")
    row["ko"] = "성인 인물의 시선과 자세로 의도적인 성적 암시를 표현하는 소셜미디어 맥락"
    row["definition"] = "A selected adult social-media portrayal whose gaze and pose intentionally carry sexual suggestion. The particular expression and pose remain authored choices; this is not a platform moderation threshold."
    row = english(193, "an original sculptural object with a rigid angular silhouette enclosed by transparent film following its contours and a sealed edge",
                  "Specify a selected concept-object form and observable packaging boundaries.")
    row["ko"] = "각진 실루엣을 따라 밀착된 투명 필름과 봉합 가장자리를 가진 창작 조형물"
    row["aliases"] = ["vacuum-packed concept object", "투명 진공 포장된 창작 조형물"]
    row["claim_limits"] = ["Vacuum packaging is authored context; film geometry does not independently prove measured pressure or hidden package contents."]
    row = english(230, "one adult presses a palm to the mirror while the reflected hand occupies a visibly offset position on that same mirror",
                  "Specify the contact owner, mirror plane and bounded mismatch.")
    row["ko"] = "거울에 손바닥을 대지만 같은 거울의 반사 손 위치가 어긋난 동작"
    row["concept_units"] = [row["en"]]
    row["claim_limits"] = ["This is one selected fictional mismatched-reflection realization, not a physical mirror-law claim."]
    effects(230, ["action", "pose", "composition"], [("pose", "main_subject", "hands"), ("composition", "mirror_image", "hand_position")])
    row = english(260, "an intentionally eclectic outfit with uneven layer lengths and asymmetric accessory placement",
                  "Describe one selected expressive styling variant without inferring profession or personality.")
    row["ko"] = "레이어 길이와 장신구 배치가 비대칭인 자유로운 창작 스타일"
    row["aliases"] = ["eclectic expressive styling", row["ko"]]
    row["claim_limits"] = ["This selected styling does not establish an artist occupation or a free-spirited personality."]
    row = content(315, "Separate supplied reputation context from the visible recognition, which does not prove beauty ranking.")
    row["definition"] = "The requester-supplied story describes a locally recognized beauty reputation. Several adults visibly turn toward and make room for the selected adult; those gestures show recognition, not independent evidence of beauty or a ranking."
    row["claim_limits"] = ["Beauty reputation is supplied narrative context, not a conclusion from appearance or crowd behavior; it does not set facial traits, ethnicity or body proportions."]
    row = english(331, "an original fictional ceremonial costume with layered cloth crossing one shoulder and long hanging drape folds",
                  "Define one original costume realization without inventing a universal religious or cultural dress.")
    row["ko"] = "한쪽 어깨를 가로지르는 겹천과 길게 드리운 주름을 가진 창작 의례 의상"
    row["claim_limits"] = ["This is an original fictional draped-costume variant; it makes no claim of cultural authenticity or deity identity."]
    row = english(546, "one subject has the hand lowered beside the body while the same mirror image keeps that hand raised at chest height",
                  "Make the contrasting hand states visible; delay remains an interpretation rather than a measured fact.")
    row["ko"] = "실물은 손을 내렸지만 같은 거울상은 가슴 높이로 손을 든 상태"
    row["aliases"] = ["delayed-reflection illusion", "지연을 연상시키는 거울상"]
    row["claim_limits"] = ["One image shows a state mismatch, not elapsed time or proof of a delayed physical reflection."]
    effects(546, ["composition", "pose"], [("composition", "mirror_image", "hand_position"), ("pose", "main_subject", "hands")])
    row = english(675, "visible luminous ribbons in haze extend from the monitor face and converge toward the selected subject without changing the monitor boundary",
                  "Bound one surreal glow geometry by its source, path and endpoint.")
    row["ko"] = "모니터 면에서 나온 안개 속 발광 띠가 피사체 쪽으로 모이는 초현실적 빛의 형상"
    row["claim_limits"] = ["This is a selected fictional light-path realization, not proof of energy transfer or an invisible psychological process."]
    row = english(983, "a closed mouth, fixed gaze and lightly drawn brows convey held concentration",
                  "Use observable facial cues; breath holding itself remains contextual.")
    row["ko"] = "입술을 다물고 시선을 고정하며 눈썹을 살짝 모은 집중 표정"
    row["claim_limits"] = ["Facial cues do not establish respiratory state; breath holding requires separate authored context."]
    row = english(998, "a reserved facial expression contrasts with hands gently supporting another adult's forearm",
                  "Resolve the emotional metaphor as expression and helping gesture, without asserting hand temperature.")
    row["ko"] = "무덤덤한 얼굴과 다른 성인의 전완을 부드럽게 받쳐 주는 손이 대비되는 모습"
    row["claim_limits"] = ["Cold and warm describe this expressive contrast; the image does not establish skin temperature or private feelings."]
    effects(998, ["expression", "pose", "character_response", "count", "relationship"], [("expression", "main_subject", "facial_expression"), ("pose", "main_subject", "hands"), ("character_response", "main_subject", "supporting_gesture"), ("count", "scene", "adult_actor_count"), ("relationship", "main_subject", "support_recipient")])

    # Replace editorial instructions with joint owned meanings, preserving members.
    bundle_units = {
        22: "같은 착용자의 앞쪽 직물 컵과 허리밴드가 연결되고 두 끈이 뒤쪽으로 내려간다",
        484: "같은 수영복 브리프에서 가는 끈이 위로 이어지며 상단 컵 없이 열린 구조를 이룬다",
        924: "같은 브라의 작은 하부 컵과 컵 아래 받침 띠가 이어지고 두 안쪽 컵 끝 사이에 열린 V 공간이 있다",
    }
    for number, unit in bundle_units.items():
        row = content(number, "Replace a record-only instruction with the joint garment relation; keep native member references and requirements.")
        old = row["components"][0]["concept_units"][0]
        row["components"][0]["concept_units"] = [unit]
        for relation in row["relations"]:
            if relation["object"] == old:
                relation["object"] = unit
        if number == 22:
            row["components"] = [part for part in row["components"] if part["id"] != "part_4"]
    row = content(588, "Remove internal duplicate-review instructions from the semantic confusion boundary.")
    row["semantics"]["contrast_examples"] = ["모래사장 외형만으로 아레노솔 토양 분류를 확정하지 않는다."]
    if "reject_substitutes" in row:
        row["reject_substitutes"] = ["모래사장 외형만으로 아레노솔 토양 분류를 확정하지 않는다."]

    # Correct nine misplaced roles, retaining their binding IDs and references.
    roles = {40: "prop", 132: "lens_artifact", 234: "composition", 302: "aesthetic_trend",
             396: "light_shape", 428: "atmosphere", 451: "mood", 642: "body_marking", 643: "light_shape"}
    for number, slot in roles.items():
        row = record(number, f"Replace the mismatched persistent role with {slot}; this is correction, not bulk multi-tag enrichment.")
        for binding in result["slot_bindings"].values():
            if binding["candidate_id"] == row["id"]:
                binding["slot_id"] = slot
                binding["conditions"]["guard_role"] = slot
    effects(132, ["camera", "color"], [("camera", "background_lights", "defocus_discs"), ("color", "background_lights", "blue_white")])
    row = content(132, "Bokeh describes defocused light images, not falling atmospheric particles.")
    row["tags"] = [tag for tag in row.get("tags", []) if tag != "air"]
    row["embedding_text"] = "blue-white defocused background light discs behind a sharper subject; crystal-rain appearance is a simile, not falling particles"
    effects(302, ["style", "camera"], [("style", "image_plane", "media_register"), ("camera", "image_plane", "capture_register")])
    effects(451, ["atmosphere", "color", "style"], [("color", "image_plane", "saturation"), ("atmosphere", "scene", "mood"), ("style", "image_plane", "editorial_register")])
    effects(642, ["appearance"], [("appearance", "main_subject", "body_marking.leg_paint")])
    effects(643, ["composition", "pose", "lighting"], [("composition", "cast_shadow", "placement"), ("pose", "cast_shadow", "gesture"), ("pose", "main_subject", "hands"), ("lighting", "scene", "shadow")])
    effects(135, ["composition", "camera"], [("camera", "image_plane", "height"), ("camera", "image_plane", "view_direction")])
    row = content(135, "Keep the complete camera term rather than unrelated words as aliases.")
    row["aliases"] = ["worm's-eye view", "worm’s-eye view", "지면 가까이에서 올려다보는 벌레 시점"]
    effects(440, ["appearance", "material"], [("appearance", "main_subject", "accessories.jewelry"), ("appearance", "main_subject", "hair.arrangement")])
    effects(382, ["appearance", "action"], [("appearance", "main_subject", "wardrobe.sleeves"), ("action", "main_subject", "rolling_sleeves")])
    effects(792, ["appearance"], [("appearance", "main_subject", "wardrobe.trouser_silhouette")])
    row = content(222, "Static burner/flame geometry affects the light source and apparatus rather than an action.")
    row["concept_candidate"]["affected_dimensions"] = ["lighting", "setting"]
    row["concept_candidate"]["affected_properties"] = [{"dimension": "lighting", "target": "burner_flame", "property": "shape"}, {"dimension": "setting", "target": "burner", "property": "outlet_geometry"}]
    effects(222, ["lighting", "setting"], [("lighting", "burner_flame", "shape"), ("setting", "burner", "outlet_geometry")])
    row = content(687, "Crossed arms do not inherently require a tripod, timer or remote; actual hand/camera feasibility is reviewed separately.")
    row.pop("requires_any_tags", None)

    # Additional concrete field defects from the same audit. Broad but relevant
    # role suggestions remain for the separate full-corpus tag-enrichment plan.
    aliases = {
        58: ["object flat-lay capture", "flat-lay set dressing", "소품 배열 플랫레이"],
        117: ["wide phone room-tour capture", "smartphone room tour", "스마트폰 방 투어 촬영"],
        184: ["Y2K dailywear nostalgia", "Y2K dailywear", "Y2K 일상복 노스탤지어"],
        250: ["balletcore rehearsal styling", "balletcore", "발레코어 리허설 스타일"],
        703: ["soft grunge styling", "soft grunge", "소프트 그런지 스타일"],
        789: ["designer desk with AI tools", "AI-tool designer workspace", "AI 도구를 사용하는 디자이너 작업 공간"],
        857: ["non-legible shop sign glow", "abstract shop-sign light", "읽을 수 없는 간판의 추상적 빛"],
    }
    for number, values in aliases.items():
        row = content(number, "Use complete role-specific aliases; remove isolated generic words or neighboring styles as equivalent aliases.")
        row["aliases"] = values
        if number == 184:
            row["embedding_text"] = "Y2K dailywear nostalgia with capri pants, cropped windbreaker and jelly shoes in one selected playful casual outfit"
    content(148, "Remove an unscoped bright-apartment setting from the action's embedding text.")["embedding_text"] = "sitting on a sofa while leaning against the same sofa arm"
    row = english(77, "an adult collectible-doll studio with small parts separated into trays and finishing tools arranged on the workbench",
                  "Replace unobservable safely wording with visible organization; do not claim safety certification.")
    row["ko"] = "작은 부품을 트레이별로 나누고 마감 도구를 작업대에 정리한 성인 수집 인형 작업실"
    row["claim_limits"] = ["Visible organization does not establish workshop safety, tool certification or chemical handling conditions."]
    english(398, "one scene with photographic appearance rather than a diagram",
            "Distinguish photographic appearance from proof that a depicted scene was physically photographed.")
    for number in (62, 167):
        row = record(number, "Keep graphic-motif arrangement changes on the displayed artwork, not the photograph's whole image plane.")
        for prop in row["effects"]["properties"]:
            if prop["target"] == "image_plane":
                prop["target"] = "displayed_artwork"
        for binding in result["slot_bindings"].values():
            if binding["candidate_id"] == row["id"]:
                binding["effects"] = copy.deepcopy(row["effects"])
    row = content(126, "Replace unrelated document-pointer confusion text with eyewear-contact boundaries.")
    boundary = "손가락이 착용 중인 같은 안경의 브리지에 실제로 닿는다. 떠 있는 안경·렌즈를 가리키기만 하는 손·별도 문서 포인터와 구분한다."
    row["semantics"]["contrast_examples"] = [boundary]
    row["reject_substitutes"] = [boundary]
    row = content(882, "Name the relation's actual eyelid/crease owner instead of a garment template.")
    for relation in row.get("relations", []):
        if relation["type"] == "co_realized_with_same_subject_and_garment":
            relation["type"] = "co_realized_with_same_subject_and_eye_region"

    # Correct inherited role restrictions only where the whole-role exclusion is
    # semantically invalid. Individual for_any, prerequisites, denies and adult
    # conditions otherwise retain their original authority.
    catalog_changes = {}
    for slot in ("surface_material", "capture_context", "apparatus_pov"):
        old = copy.deepcopy(result["slot_catalog"][slot]["applicability"])
        policy = copy.deepcopy(old)
        if slot == "surface_material":
            policy["subject_categories"] = list(dict.fromkeys(policy.get("subject_categories", []) + ["human", "animal"]))
        elif slot == "capture_context":
            domains = ["documentary", "craft", "wildlife", "product", "jewelry", "food", "architecture"]
            policy["allow_domains"] = list(dict.fromkeys(policy.get("allow_domains", []) + domains))
            policy["deny_domains"] = [domain for domain in policy.get("deny_domains", []) if domain not in domains]
        else:
            policy["subject_categories"] = ["human", "animal", "food", "object", "plant", "environment"]
            policy["deny_domains"] = []
        result["slot_catalog"][slot]["applicability"] = policy
        catalog_changes[slot] = {"before": old, "after": policy}
        for binding in result["slot_bindings"].values():
            if slot not in {"capture_context", "apparatus_pov"} or binding["slot_id"] != slot:
                continue
            if binding["conditions"].get("subject_applicability") == old:
                binding["conditions"]["subject_applicability"] = copy.deepcopy(policy)
                reasons.setdefault(binding["candidate_id"], []).append("Remove a demonstrably inherited whole-role subject/domain restriction; retain candidate-specific prerequisites.")
    material_cohort = []
    categories = {"human", "animal", "food", "object", "plant", "environment", "sign"}
    for binding in result["slot_bindings"].values():
        if binding["slot_id"] != "surface_material":
            continue
        policy = binding["conditions"].get("subject_applicability", {})
        allowed = policy.get("subject_categories")
        if not allowed:
            continue
        candidate = result["candidates"][binding["candidate_id"]]
        declared = categories & set(candidate["content"].get("for_any", []))
        if any(prop["property"].startswith(("wardrobe.", "accessories.")) for prop in binding["effects"]["properties"]):
            declared.add("human")
        missing = sorted(declared - set(allowed))
        if missing:
            policy["subject_categories"] = allowed + missing
            material_cohort.append({"candidate_id": candidate["id"], "binding_id": binding["id"], "added_subject_categories": missing})
            reasons.setdefault(candidate["id"], []).append("Reconcile material applicability with explicit for_any subjects or wardrobe/accessory owners; do not infer new semantics from similarity.")
    for number in (58, 117):
        row = content(number, "Object flat-lay and room-tour photography do not require a human in frame.")
        row.pop("for_any", None)
        row["tags"] = [tag for tag in row.get("tags", []) if tag != "human"]

    # Retain complete original provenance and add immutable remediation evidence.
    changed_records = {}
    for cid, row in result["candidates"].items():
        if row == source["candidates"][cid]:
            continue
        payload = {"candidate_id": cid, "before_sha256": corpus.digest(source["candidates"][cid]),
                   "content": row["content"], "effects": row["effects"], "reasons": reasons[cid]}
        row["provenance"].append({"source": "quality-remediation:20261013:" + cid, "sha256": corpus.digest(payload)})
        changed_records[cid] = {"before": source["candidates"][cid], "after": row, "reasons": reasons[cid]}
    changed_bindings = {bid: {"before": source["slot_bindings"][bid], "after": row, "reasons": reasons.get(row["candidate_id"], [])}
        for bid, row in result["slot_bindings"].items() if row != source["slot_bindings"][bid]}
    corpus.validate(result)
    expected = {"candidates", "slot_bindings", "slot_catalog"}
    if any(result[key] != source[key] for key in set(source) - expected):
        raise ValueError("unrequested policy/source changes")
    ledger = {"schema": "photo-candidate-quality-remediation/v1",
        "audit": str(AUDIT.relative_to(ROOT)), "audit_sample_sha256": hashlib.sha256((AUDIT / "samples.jsonl").read_bytes()).hexdigest(),
        "before_corpus_sha256": corpus.digest(source), "after_corpus_sha256": corpus.digest(result),
        "candidates": changed_records, "bindings": changed_bindings, "catalog": catalog_changes,
        "material_cohort": material_cohort, "sample_fixes": sorted({row["sample_number"] for row in samples.values()
            if row["candidate"]["id"] in changed_records or any(bid in changed_bindings for bid in [b["id"] for b in row["bindings"]])}),
        "summary": {"candidates": len(source["candidates"]), "bindings": len(source["slot_bindings"]),
            "changed_payloads": len(changed_records), "changed_bindings": len(changed_bindings), "corrected_slot_roles": len(roles),
            "translated_ko_labels": len(korean), "catalog_roles": len(catalog_changes), "material_subject_conflicts_repaired": len(material_cohort),
            "changed_search_texts": sum(index.text(row) != index.text(source["candidates"][cid]) for cid, row in result["candidates"].items())}}
    return result, ledger


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    source = corpus.load(ASSETS)
    previous_path = HERE / "FIXES.json"
    if previous_path.exists():
        previous = corpus.decode(previous_path.read_bytes())
        if corpus.digest(source) != previous["after_corpus_sha256"]:
            raise ValueError("source changed since the recorded remediation")
        for cid, row in previous["candidates"].items():
            source["candidates"][cid] = row["before"]
        for bid, row in previous["bindings"].items():
            source["slot_bindings"][bid] = row["before"]
        for slot, row in previous["catalog"].items():
            source["slot_catalog"][slot]["applicability"] = row["before"]
        if corpus.digest(source) != previous["before_corpus_sha256"]:
            raise ValueError("recorded pre-remediation source does not reconstruct")
    proposed, ledger = propose(source)
    if not args.write:
        atomic(HERE / "PROPOSED-FIXES.json", ledger)
        print(json.dumps(ledger["summary"], ensure_ascii=False))
        return
    expected = corpus.decode((HERE / "PROPOSED-FIXES.json").read_bytes())
    if ledger != expected:
        raise ValueError("reviewed proposal changed")
    before = {"git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_files": {}, "protected_dirty_files": {}}
    for relative in ["docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md",
                     "docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md"]:
        before["protected_dirty_files"][relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    manifest = corpus.decode((ASSETS / corpus.MANIFEST_NAME).read_bytes())
    modules = []
    for module in manifest["modules"]:
        path = ASSETS / module["file"]
        raw = path.read_bytes()
        before["source_files"][module["file"]] = hashlib.sha256(raw).hexdigest()
        payload = corpus.decode(raw)
        field = module["kind"]
        values = payload[field]
        edited = False
        for key in values:
            if values[key] != proposed[field][key]:
                values[key] = proposed[field][key]
                edited = True
        if edited:
            modules.append((path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()))
    if not (HERE / "SOURCE-BEFORE.json").exists():
        atomic(HERE / "SOURCE-BEFORE.json", before)
    from photo_runtime_sources import source_update
    with source_update(SKILL):
        from photo_global_index_storage import atomic_write
        for path, raw in modules:
            atomic_write(path, raw)
        if corpus.digest(corpus.load(ASSETS)) != ledger["after_corpus_sha256"]:
            raise ValueError("source write did not match reviewed patch")
    atomic(HERE / "FIXES.json", ledger)
    (HERE / "PROPOSED-FIXES.json").unlink()
    print(json.dumps({**ledger["summary"], "changed_modules": [path.name for path, _ in modules]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
