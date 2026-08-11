#!/usr/bin/env python3
"""Compile the five reviewed moe dossiers into one executable v2 grammar.

The raw dossiers remain the human-readable research authority.  This compiler
only normalizes their heterogeneous schemas, adds the paired neutral/preference
intent fixtures, and emits deterministic typed candidates for the runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence


GRAMMAR_SCHEMA = "subculture-illustration-moe-grammar/v2"
DOSSIER_NAMES = ("narrative", "wardrobe", "body", "staging_social", "fantasy")


# These are product directions distilled from the paired intent corpus.  They
# are deliberately construction/event language, never bare culture labels.
PREFERENCE_REALIZATIONS: dict[str, tuple[str, list[str], list[str]]] = {
    "moe_darkening_corruption": (
        "Use a three-stage sequence in which the adult protagonist freely chooses power, breaks the old oath emblem by hand, and carries an irreversible allegiance mark into the final frame.",
        [
            "a voluntary reach toward the power source",
            "the oath emblem breaking under the protagonist's own hand",
            "one irreversible allegiance mark in the final state",
        ],
        ["스스로", "옛 서약", "불가역", "세 단계"],
    ),
    "moe_ntr_relationship_displacement": (
        "Stage a missed-chance witness sequence: an adult who never confessed arrives too late and sees the other two adults form the relationship, with the unrealized bond and missed timing kept explicit.",
        [
            "an unsent confession or unopened keepsake",
            "the new pair forming in the witness's sightline",
            "a visible too-late arrival cue",
        ],
        ["고백하지 못한", "BSS", "미성립 관계", "놓친 시점"],
    ),
    "moe_sensory_deprivation_magic": (
        "In one frame suppress only hearing: keep the awake adult able to see mouth shapes and vibration while the sound-wave path stops at a clear field boundary and the caster maintains the spell directly behind them.",
        [
            "visible mouth movement and surface vibration",
            "a sound-wave path ending at the field boundary",
            "the caster maintaining the field behind the subject",
        ],
        ["청각만", "청각이 차단", "듣지 못", "소리 파형", "진동", "바로 뒤"],
    ),
    "moe_virgin_killer_clothing": (
        "Choose the 2015 lineage: a frilled blouse tucked into a strongly articulated high-waisted skirt, shown in front three-quarter view so the separate garments, waist panel, and blouse-to-skirt volume contrast remain legible.",
        [
            "a visibly separate frilled blouse",
            "a high structured waistband",
            "skirt volume expanding below the fitted waist",
        ],
        ["2015년", "프릴 블라우스", "하이웨이스트", "허리선"],
    ),
    "moe_mesugaki_provocation": (
        "Build a matched two-panel reversal between adults: confident targeted provocation first, then the counterpart immediately succeeds and the provocateur recoils into visible embarrassment through expression and distance rather than explanatory text.",
        [
            "a first-panel confident targeted challenge",
            "the counterpart's completed result",
            "a second-panel retreat and flustered expression",
        ],
        ["역으로 당황", "두 컷", "표정과 거리", "바로 성공"],
    ),
    "moe_i_balance_pose": (
        "Show an unassisted lateral I-balance in a frontal vertical full-body frame: one free leg rises nearly vertical beside the torso while both arms spread as counterweights and neither hand touches the leg.",
        [
            "one planted support foot",
            "a near-vertical lateral free leg",
            "both hands clear of the leg and arms counterbalancing",
        ],
        ["무보조", "옆으로 거의 수직", "두 팔", "세로 전신"],
    ),
    "moe_pajama_challenge": (
        "Use one locked camera for a three-stage garment-action sequence: loose shirt, right rear-waist grip pulling diagonally, then the final twisted tension silhouette, preserving the same adult and the same shirt.",
        [
            "the same loose shirt before tension",
            "a right rear-waist grip and diagonal pull",
            "the final directional fabric-tension lines",
        ],
        ["세 단계", "오른쪽 뒤 허리", "대각선", "같은 카메라"],
    ),
    "moe_reverse_bunny_costume": (
        "Make the reverse-bunny coverage arm-heavy: combine long opera gloves and large detached sleeves with only thin thigh-high legwear, while a frontal view clearly preserves the inverted classic-bunny torso coverage and rabbit identity accessories.",
        [
            "large detached sleeves above long gloves",
            "thin thigh-high legwear",
            "a clearly absent classic torso-suit region with rabbit accessories",
        ],
        ["팔 쪽", "오페라 글러브", "detached sleeves", "torso coverage inversion"],
    ),
    "moe_implied_all_ages_staging": (
        "Use a reaction-first Kuleshov diptych: show the adult's directed gaze and startled hand first, then a doorway gap and displaced props, while leaving the hidden action genuinely unresolved.",
        [
            "a reaction with a directed eyeline",
            "a second-panel doorway gap",
            "two displaced aftermath props without a revealed action",
        ],
        ["반응을 먼저", "Kuleshov", "문틈", "확정하지"],
    ),
    "moe_dolphin_shorts": (
        "Choose loose retro satin dolphin-hem running shorts with a higher side notch, shown during a lateral running stride so contrast binding follows the curved hem without collapsing into compression hotpants.",
        [
            "a loose athletic shell",
            "a high side notch and rounded bound hem",
            "contrast piping visible through the running profile",
        ],
        ["복고풍 새틴", "옆트임", "달리는 측면", "핫팬츠"],
    ),
    "moe_thermal_bodysuit": (
        "Use a smooth crew-neck short-sleeve thermal bodysuit in a front product-style view, with no shirt hem and with both leg openings and the small crotch snap closure visible.",
        [
            "a continuous torso-to-crotch garment",
            "two visible leg openings",
            "a small snap closure without a separate shirt hem",
        ],
        ["크루넥", "반소매", "매끈", "snap closure"],
    ),
    "moe_maternal_care": (
        "Show an adult role reversal through practical care: the usual recipient now removes damaged gear, washes the other adult's hand, and offers a bandage across a clear three-step care sequence.",
        [
            "damaged gear being removed",
            "the caregiver washing the injured hand",
            "a bandage offered as the completed next step",
        ],
        ["역할을 바꿔", "장비를 벗겨", "손을 씻긴", "붕대"],
    ),
    "moe_screen_shake_illusion": (
        "Design an interactive horizontal-shake illusion with vertical phase bands: only the central heart contour oscillates during left-right screen motion while all surrounding contours stay phase-stable.",
        [
            "vertical phase bands inside the heart contour",
            "a stationary surrounding reference grid",
            "an explicit left-right viewer interaction instruction",
        ],
        ["좌우로 흔들", "심장 윤곽", "세로 위상 띠", "주변 윤곽"],
    ),
    "moe_bubble_tea_challenge": (
        "Support a small bubble-tea cup off-center on the left upper torso in a three-quarter view, with both hands visibly overhead, a continuous straw path, and a level liquid surface.",
        [
            "the cup supported without either hand",
            "both hands fully visible overhead",
            "a continuous straw and level liquid surface",
        ],
        ["왼쪽 upper torso", "3/4", "두 손은 머리 위", "액면은 수평"],
    ),
    "moe_thigh_gap": (
        "Use a level frontal stance with feet together and retain only a subtle upper-thigh triangular negative space; close the silhouette below that small gap instead of extending it toward the knees.",
        [
            "both feet together on one ground plane",
            "one small upper-thigh triangular gap",
            "no continuing gap below the upper thighs",
        ],
        ["작은 삼각형", "아주 미묘", "발은 붙이고", "무릎 아래"],
    ),
    "moe_quicksand_sinking": (
        "Depict the early knee-level phase of a quicksand rescue: the adult explorer minimizes movement while a companion extends a broad board and the material depression and displaced rim remain physically legible.",
        [
            "one knee at the material boundary",
            "a broad rescue board spanning firm ground",
            "reduced movement and a visible displaced rim",
        ],
        [
            "한쪽 무릎",
            "무릎까지",
            "초기 단계",
            "넓은 판자",
            "구조 판자",
            "움직임을 줄여",
        ],
    ),
    "moe_axilla": (
        "Use a bilateral overhead stretch with both arms extended and side lighting that defines the anterior axillary folds toward the pectoral edge while preserving continuous shoulder-to-torso anatomy.",
        [
            "both arms extended overhead",
            "side-lit anterior axillary folds",
            "continuous shoulder, upper-arm, and torso connections",
        ],
        ["양팔", "앞겨드랑주름", "앞뒤 주름", "옆빛", "분리되지"],
    ),
    "moe_stockings": (
        "Choose sheer seam-back stockings supported by a garter belt, shown rear three-quarter so four suspender straps connect to two top bands and each center-back seam continues down the leg.",
        [
            "four visible garter straps",
            "two separate stocking top bands",
            "continuous center-back seams",
        ],
        ["가터벨트", "seam-back", "후면 3/4", "네 개의 가터"],
    ),
    "moe_morals_committee": (
        "Give the adult morals-committee character a practical festival-eve duty: repairing route safety tape by the rules, then briefly flustering when another adult helps, so role competence and emotional gap share one event.",
        [
            "festival route tape being repaired",
            "a visible rule or route plan",
            "a brief flustered reaction to offered help",
        ],
        ["축제 전날", "통로 안전선", "도움받은", "당황"],
    ),
    "moe_adult_finger_sucking": (
        "Use a side-profile thumb-contact gesture: the adult's lips close around the thumb pad while the other hand turns a book page, with no claim about habit, motive, or emotion.",
        [
            "thumb-pad contact at the lips",
            "a clear side-profile mouth boundary",
            "the other hand turning a book page",
        ],
        ["엄지를", "옆얼굴", "엄지 패드", "책장을"],
    ),
    "moe_classic_bunny_costume": (
        "Choose a dark navy matte-velvet structured one-piece with a lower leg line, opaque tights, and short heels while retaining the paired ears, detached collar, cuffs, bow, and centered tail.",
        [
            "a matte structured navy torso suit",
            "paired ears, detached collar, bow, and cuffs",
            "opaque tights and a small centered tail",
        ],
        ["남색", "매트 벨벳", "덜 높게", "불투명 스타킹"],
    ),
    "moe_tsf_transformation": (
        "Use an instantaneous reversible body swap between two adults: show both viewpoints across a short sequence, preserve identity anchors through the exchanged bodies, and keep the triggering device plus a visible reversal indicator.",
        [
            "two adult identity anchors exchanged across bodies",
            "the same triggering device at the swap moment",
            "a visible reversible-state indicator",
        ],
        ["두 성인", "몸이 바뀌", "양쪽 관점", "되돌릴"],
    ),
    "moe_yandere_obsession": (
        "Build a nonviolent logistical-control sequence from the target's viewpoint: helpful message handling becomes unauthorized replies and a hidden exit key, making ordinary care visibly narrow the target's choices.",
        [
            "messages answered without the target's action",
            "an exit key moved into concealment",
            "the target discovering reduced choices",
        ],
        ["연락을 대신", "열쇠를 숨기", "비폭력", "고립"],
    ),
    "moe_glasses": (
        "Use thick angular acetate glasses and catch one hand lifting the right temple, keeping lens reflections weak enough that both eyes and the frame construction remain visible.",
        [
            "thick angular acetate rims",
            "fingertip contact at the right temple",
            "both eyes readable through low-reflection lenses",
        ],
        ["두꺼운 각진", "아세테이트", "오른쪽 temple", "반사는 거의"],
    ),
    "moe_ponytail": (
        "Choose a low side ponytail anchored near the nape, with one heavy wavy bundle draped over a shoulder and almost no motion so the tie point and weight remain readable.",
        [
            "one low side tie point near the nape",
            "a thick wavy bundle over one shoulder",
            "a gravity-led resting curve with minimal motion",
        ],
        ["낮은 사이드", "목덜미", "굵은 웨이브", "정지형"],
    ),
    "moe_contempt_derision": (
        "Use dialogue-led comedic derision from a low camera: one short addressed balloon, one raised mouth corner, and an exaggerated recoil from the adult counterpart, without multiplying facial cues.",
        [
            "one short addressed speech balloon",
            "one asymmetrically raised mouth corner",
            "the counterpart's exaggerated recoil",
        ],
        ["짧은 말풍선", "코미디", "낮은 카메라", "한쪽 입꼬리"],
    ),
    "moe_abdomen": (
        "Show a seated adult leaning forward in side view so compression creates two soft horizontal folds below and around the navel, with no invented abdominal-muscle lines.",
        [
            "a seated forward-flexed torso",
            "two soft horizontal compression folds",
            "a visible navel without etched muscle segmentation",
        ],
        ["의자에 앉아", "앞으로 숙인", "두 개의 가로", "복근 선"],
    ),
    "moe_strategic_occlusion_selfie": (
        "Use a landscape upper-body mirror selfie: keep the phone beside the face and make the left hand's direct and reflected images point diagonally to three different occlusion sites while the mirror edge stays visible.",
        [
            "a phone beside rather than over the face",
            "three distinct diagonal occlusion points",
            "the mirror edge plus direct and reflected left hands",
        ],
        ["가로 상반신", "얼굴 옆", "세 지점", "거울 가장자리"],
    ),
    "moe_ahegao_expression": (
        "Choose a low-intensity asymmetric expression: roll only one eye upward, leave the other half-lidded, show a small tongue tip and slight drool, and omit tears.",
        [
            "one upward-rolled eye",
            "one half-lidded eye",
            "a small tongue tip and slight drool without tears",
        ],
        ["저강도", "한쪽 눈만", "반쯤 감긴", "눈물 없이"],
    ),
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one object")
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slug(value: object) -> str:
    text = re.sub(r"[^a-z0-9]+", "_", str(value).casefold()).strip("_")
    return text or "unnamed"


def _unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        clean = " ".join(str(value).split())
        if clean and clean not in result:
            result.append(clean)
    return result


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_strings(item))
        return result
    if isinstance(value, Mapping):
        preferred = (
            "question_ko",
            "question",
            "summary",
            "definition",
            "definition_ko",
            "distinction",
            "criterion_en",
            "prompt_operation_en",
            "claim",
            "mechanism",
            "description",
            "effect",
            "reason",
            "limitation",
        )
        result: list[str] = []
        for key in preferred:
            if key in value:
                result.extend(_strings(value[key]))
        if result:
            return result
        for item in value.values():
            result.extend(_strings(item))
        return result
    return []


def _rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = payload.get("dossiers", payload.get("elements"))
    if not isinstance(values, list):
        raise ValueError("dossier file lacks dossiers/elements")
    return [dict(row) for row in values if isinstance(row, Mapping)]


def _row_id(row: Mapping[str, Any]) -> str:
    return str(row.get("id") or row.get("element_id") or "")


def _raw_candidates(row: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = row.get("candidate_realizations", row.get("typed_candidates", []))
    return (
        [dict(item) for item in values if isinstance(item, Mapping)]
        if isinstance(values, list)
        else []
    )


def _source_objects(
    payload: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    top = payload.get("sources")
    if isinstance(top, list):
        result.extend(dict(item) for item in top if isinstance(item, Mapping))
    for row in rows:
        local = row.get("sources")
        if isinstance(local, list):
            result.extend(dict(item) for item in local if isinstance(item, Mapping))
        claims = row.get("source_claims")
        if isinstance(claims, list):
            result.extend(dict(item) for item in claims if isinstance(item, Mapping))
    return result


def _source_id(source: Mapping[str, Any]) -> str:
    return str(source.get("id") or source.get("source_id") or "")


def _discover_refs(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in {"source_ids", "source_refs", "sources"} and isinstance(
                item, list
            ):
                result.extend(str(entry) for entry in item if isinstance(entry, str))
            else:
                result.extend(_discover_refs(item))
    elif isinstance(value, list):
        for item in value:
            result.extend(_discover_refs(item))
    return _unique(result)


def _subtypes(row: Mapping[str, Any]) -> list[dict[str, str]]:
    values = row.get("semantic_subtypes", [])
    result: list[dict[str, str]] = []
    if isinstance(values, list):
        for index, raw in enumerate(values):
            if not isinstance(raw, Mapping):
                continue
            subtype_id = str(
                raw.get("id") or raw.get("subtype_id") or f"subtype_{index + 1}"
            )
            label = str(raw.get("label") or raw.get("label_ko") or subtype_id)
            distinction_values = _strings(
                raw.get(
                    "distinction",
                    raw.get(
                        "definition",
                        raw.get(
                            "definition_ko", raw.get("distinguishing_features", raw)
                        ),
                    ),
                )
            )
            result.append(
                {
                    "id": _slug(subtype_id),
                    "label": label,
                    "distinction": "; ".join(_unique(distinction_values)[:6]) or label,
                }
            )
    while len(result) < 2:
        index = len(result) + 1
        result.append(
            {
                "id": f"researched_variant_{index}",
                "label": f"researched variant {index}",
                "distinction": "A separately routed interpretation preserved by the research dossier.",
            }
        )
    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in result:
        if item["id"] not in seen:
            seen.add(item["id"])
            deduped.append(item)
    return deduped


def _axes(row: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = row.get("preference_axes", [])
    result: list[dict[str, Any]] = []
    if isinstance(values, list):
        for index, raw in enumerate(values):
            if not isinstance(raw, Mapping):
                continue
            axis_id = _slug(
                raw.get("id")
                or raw.get("axis_id")
                or raw.get("axis")
                or f"axis_{index + 1}"
            )
            description = (
                "; ".join(
                    _unique(
                        _strings(
                            raw.get(
                                "description",
                                raw.get(
                                    "effect",
                                    raw.get(
                                        "effects", raw.get("selection_effect", axis_id)
                                    ),
                                ),
                            )
                        )
                    )[:4]
                )
                or axis_id
            )
            raw_values = raw.get("values")
            normalized_values: list[dict[str, Any]] = []
            if isinstance(raw_values, list):
                for value_index, raw_value in enumerate(raw_values):
                    if isinstance(raw_value, Mapping):
                        value_id = _slug(
                            raw_value.get("id")
                            or raw_value.get("value_id")
                            or raw_value.get("value")
                            or f"value_{value_index + 1}"
                        )
                        label = str(
                            raw_value.get("label")
                            or raw_value.get("label_ko")
                            or value_id
                        )
                        cues = _unique(
                            _strings(
                                raw_value.get(
                                    "request_cues",
                                    raw_value.get(
                                        "ko_cues",
                                        raw_value.get(
                                            "korean_cues",
                                            raw_value.get(
                                                "korean_user_cues",
                                                raw_value.get("cues", []),
                                            ),
                                        ),
                                    ),
                                )
                            )
                        )
                    else:
                        value_id = _slug(raw_value)
                        label = str(raw_value)
                        cues = []
                    normalized_values.append(
                        {
                            "id": value_id,
                            "label": label,
                            "request_cues": cues or [label],
                        }
                    )
            if len(normalized_values) < 2:
                cues = _unique(_strings(raw.get("cues_ko", raw.get("cues", []))))
                normalized_values = [
                    {
                        "id": "default",
                        "label": "default",
                        "request_cues": [f"{axis_id} default"],
                    },
                    {
                        "id": "specified",
                        "label": "specified",
                        "request_cues": cues or [axis_id],
                    },
                ]
            result.append(
                {"id": axis_id, "description": description, "values": normalized_values}
            )
    while len(result) < 2:
        axis_id = f"research_axis_{len(result) + 1}"
        result.append(
            {
                "id": axis_id,
                "description": "Research-derived variant routing.",
                "values": [
                    {
                        "id": "grounded",
                        "label": "grounded",
                        "request_cues": [f"{axis_id} grounded"],
                    },
                    {
                        "id": "developed",
                        "label": "developed",
                        "request_cues": [f"{axis_id} developed"],
                    },
                ],
            }
        )
    return result


def _route_cues(
    row: Mapping[str, Any],
) -> tuple[dict[str, list[str]], dict[str, dict[str, str]]]:
    cues: dict[str, list[str]] = {}
    profiles: dict[str, dict[str, str]] = {}
    values = row.get("preference_axes", [])
    if not isinstance(values, list):
        return cues, profiles
    for raw_axis in values:
        if not isinstance(raw_axis, Mapping):
            continue
        axis_id = _slug(
            raw_axis.get("id")
            or raw_axis.get("axis_id")
            or raw_axis.get("axis")
            or "axis"
        )
        for raw_value in (
            raw_axis.get("values", [])
            if isinstance(raw_axis.get("values"), list)
            else []
        ):
            if not isinstance(raw_value, Mapping):
                continue
            value_id = _slug(
                raw_value.get("id")
                or raw_value.get("value_id")
                or raw_value.get("value")
                or "specified"
            )
            value_cues = _unique(
                _strings(
                    raw_value.get(
                        "request_cues",
                        raw_value.get(
                            "ko_cues",
                            raw_value.get(
                                "korean_cues",
                                raw_value.get(
                                    "korean_user_cues", raw_value.get("cues", [])
                                ),
                            ),
                        ),
                    )
                )
            )
            effect = raw_value.get("effect")
            route_values: list[str] = []
            for key in ("route_to", "candidate_bias"):
                route_values.extend(_strings(raw_value.get(key)))
                if isinstance(effect, Mapping):
                    route_values.extend(_strings(effect.get(key)))
            for raw_candidate_id in route_values:
                candidate_key = str(raw_candidate_id)
                cues.setdefault(candidate_key, []).extend(value_cues)
                profiles.setdefault(candidate_key, {})[axis_id] = value_id
    return {key: _unique(value) for key, value in cues.items()}, profiles


def _candidate_id(raw: Mapping[str, Any]) -> str:
    return str(raw.get("id") or raw.get("candidate_id") or "")


def _novelty(raw: Mapping[str, Any]) -> int:
    value = raw.get("novelty", raw.get("novelty_level", 1))
    if type(value) is int and value in {0, 1, 2}:
        return value
    return {
        "grounded": 0,
        "baseline": 0,
        "developed": 1,
        "interpretive": 1,
        "novel": 2,
        "experimental": 2,
    }.get(_slug(value), 1)


def _evidence(raw: Mapping[str, Any]) -> list[str]:
    for key in (
        "evidence_phrases_en",
        "observable_or_narrative_evidence_en",
        "observable_evidence_groups",
        "required_evidence",
        "observable_evidence",
    ):
        values = _unique(_strings(raw.get(key)))
        if values:
            return values[:4]
    return ["one visible construction cue", "one visible action or relation cue"]


def _representation(element_id: str, raw: Mapping[str, Any], legacy_mode: str) -> str:
    text = " ".join(
        _strings(
            [
                raw.get("prompt_operation_en"),
                raw.get("frame_or_format_implications"),
                raw.get("format_implications"),
                raw.get("camera"),
            ]
        )
    ).casefold()
    if element_id == "moe_screen_shake_illusion":
        return "optical_interaction"
    if any(
        token in text
        for token in ("three-stage", "three phase", "triptych", "sequence")
    ):
        return "sequence"
    if any(token in text for token in ("diptych", "two-panel", "two panel", "paired")):
        return "paired_or_sequence"
    return legacy_mode


def _resolve_research_placeholders(value: str) -> str:
    """Turn dossier variables into readable generic slots, never raw braces."""

    replacements = {
        "channel_scope": "the explicitly selected sensory channel",
        "affected_scope": "the explicitly selected body region",
        "narrative_phase": "the requested narrative phase",
        "effect_source": "the visible spell source",
        "safe_visible_task": "one safe visible task",
    }
    return re.sub(
        r"\{([a-z0-9_]+)\}",
        lambda match: replacements.get(
            match.group(1), match.group(1).replace("_", " ")
        ),
        value,
    )


def _integration_role(category: str) -> str:
    return {
        "character_relationship_narrative": "relationship_event",
        "wardrobe": "wardrobe",
        "body_hair_pose": "pose",
        "expression_staging_perception": "expression",
        "participatory_social_meme": "participatory_action",
        "fantasy_hazard": "environment_hazard",
    }[category]


def _atoms(
    candidate_id: str, operation: str, evidence: Sequence[str]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = _slug(candidate_id.removeprefix("moe_candidate_"))
    primary = {
        "id": f"moe_atom_{base}_primary",
        "prompt_fragment_en": operation.rstrip(".") + ".",
        "observable_evidence": list(evidence),
    }
    supports: list[dict[str, Any]] = []
    for index, phrase in enumerate(list(evidence)[:3], 1):
        fragment = phrase.strip().rstrip(".")
        supports.append(
            {
                "id": f"moe_atom_{base}_support_{index}",
                "prompt_fragment_en": f"Directly show {fragment[0].lower() + fragment[1:] if fragment else 'the researched evidence'}.",
                "observable_evidence": [phrase],
            }
        )
    while len(supports) < 2:
        index = len(supports) + 1
        supports.append(
            {
                "id": f"moe_atom_{base}_support_{index}",
                "prompt_fragment_en": "Keep the selected construction and its causal relation visible.",
                "observable_evidence": ["selected construction and causal relation"],
            }
        )
    return primary, supports


def _preference_profile(pref: Mapping[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in (
        pref.get("parsed_preference_axes", [])
        if isinstance(pref.get("parsed_preference_axes"), list)
        else []
    ):
        if isinstance(row, Mapping):
            result[_slug(row.get("axis") or "axis")] = _slug(
                row.get("value") or "specified"
            )
    return result or {"intent": "specified"}


def compile_grammar(asset_dir: Path) -> dict[str, Any]:
    legacy_path = asset_dir / "illustration_moe_elements_v1.json"
    legacy_research_path = (
        asset_dir / "research_evidence_moe_elements" / "research_v1.json"
    )
    compatibility_path = asset_dir / "illustration_moe_compatibility_v2.json"
    corpus_path = asset_dir / "research_evidence_moe_elements" / "intent_corpus_v2.json"
    dossier_root = asset_dir / "research_evidence_moe_elements" / "dossiers_v2"
    legacy = _load(legacy_path)
    legacy_research = _load(legacy_research_path)
    corpus = _load(corpus_path)
    compatibility = _load(compatibility_path)
    dossier_payloads = {
        name: _load(dossier_root / f"{name}.json") for name in DOSSIER_NAMES
    }
    dossier_rows = {name: _rows(payload) for name, payload in dossier_payloads.items()}
    row_by_id: dict[str, tuple[str, dict[str, Any]]] = {}
    for name in DOSSIER_NAMES:
        for row in dossier_rows[name]:
            element_id = _row_id(row)
            if element_id in row_by_id:
                raise ValueError(f"duplicate dossier for {element_id}")
            row_by_id[element_id] = (name, row)
    element_ids = [str(row["id"]) for row in legacy["elements"]]
    if set(row_by_id) != set(element_ids):
        raise ValueError(
            f"dossier coverage drift: missing={sorted(set(element_ids) - set(row_by_id))}, extra={sorted(set(row_by_id) - set(element_ids))}"
        )

    normalized_sources = [dict(source) for source in legacy_research["sources"]]
    source_maps: dict[str, dict[str, str]] = {}
    for name in DOSSIER_NAMES:
        source_maps[name] = {}
        for source in _source_objects(dossier_payloads[name], dossier_rows[name]):
            raw_id = _source_id(source)
            url = source.get("url")
            if not raw_id or not isinstance(url, str) or not url.startswith("https://"):
                continue
            normalized_id = f"v2_{name}_{_slug(raw_id)}"
            if normalized_id in {item["id"] for item in normalized_sources}:
                continue
            source_maps[name][raw_id] = normalized_id
            normalized_sources.append(
                {
                    "id": normalized_id,
                    "kind": "supplemental_source",
                    "title": str(source.get("title") or raw_id),
                    "url": url,
                    "publisher": str(
                        source.get("publisher")
                        or source.get("source_kind")
                        or source.get("source_type")
                        or "reviewed supplemental source"
                    ),
                    "claim_scope": "; ".join(
                        _unique(
                            _strings(
                                source.get(
                                    "claim_scope",
                                    source.get(
                                        "scope_note",
                                        source.get(
                                            "supports",
                                            source.get(
                                                "claim",
                                                source.get(
                                                    "limitations",
                                                    "research dossier source",
                                                ),
                                            ),
                                        ),
                                    ),
                                )
                            )
                        )[:5]
                    )
                    or "research dossier source",
                }
            )

    neutral_rows = {
        row["expected_primary_element_id"]: row
        for row in corpus["sections"]["neutral_requests"]
    }
    preference_rows = {
        row["expected_primary_element_id"]: row
        for row in corpus["sections"]["preference_requests"]
    }
    compatibility_profiles = {
        row["element_id"]: row for row in compatibility["element_profiles"]
    }
    compiled_elements: list[dict[str, Any]] = []
    candidate_count = 0

    for legacy_row in legacy["elements"]:
        element_id = legacy_row["id"]
        dossier_name, raw = row_by_id[element_id]
        neutral = neutral_rows[element_id]
        preference = preference_rows[element_id]
        subtypes = _subtypes(raw)
        subtype_ids = {row["id"] for row in subtypes}
        for corpus_row in (neutral, preference):
            subtype_id = _slug(corpus_row["expected_candidate_selection"]["subtype_id"])
            if subtype_id not in subtype_ids:
                distinction = "; ".join(
                    corpus_row["expected_candidate_selection"][
                        "primary_candidate_direction"
                    ]
                )
                subtypes.append(
                    {
                        "id": subtype_id,
                        "label": subtype_id.replace("_", " "),
                        "distinction": distinction,
                    }
                )
                subtype_ids.add(subtype_id)

        mapped_source_ids = [
            source_maps[dossier_name][ref]
            for ref in _discover_refs(raw)
            if ref in source_maps[dossier_name]
        ]
        definition_sources = _unique(
            [*legacy_row["origin_source_ids"], *mapped_source_ids[:8]]
        )
        evidence_sources = _unique(
            [
                *legacy_row["independent_source_ids"],
                *mapped_source_ids[8:16],
                *mapped_source_ids[:2],
            ]
        )
        claim_definition = f"moe_claim_{int(legacy_row['ordinal']):02d}_definition"
        claim_evidence = f"moe_claim_{int(legacy_row['ordinal']):02d}_evidence"
        claims = [
            {
                "id": claim_definition,
                "claim": "; ".join(
                    _unique(_strings(raw.get("definition_and_history")))[:5]
                )
                or legacy_row["design_inference"],
                "source_ids": definition_sources,
                "confidence": "medium",
            },
            {
                "id": claim_evidence,
                "claim": "The dossier separates the culture label from construction, action, relation, camera, or format evidence that can be requested explicitly.",
                "source_ids": evidence_sources,
                "confidence": "medium",
            },
        ]

        route_cues, route_profiles = _route_cues(raw)
        raw_candidates = [
            candidate
            for candidate in _raw_candidates(raw)
            if str(candidate.get("role", candidate.get("candidate_type", "primary")))
            != "router"
        ]
        normalized_candidates: list[dict[str, Any]] = []
        used_candidate_ids: set[str] = set()

        def add_candidate(
            candidate_id: str,
            *,
            label: str,
            subtype_id: str,
            novelty: int,
            canonical: bool,
            intent_keys: list[str],
            representation: str,
            cues: list[str],
            profile: dict[str, str],
            operation: str,
            evidence: list[str],
            tags: list[str],
        ) -> None:
            nonlocal candidate_count
            typed_id = f"moe_candidate_{_slug(candidate_id)}"
            if typed_id in used_candidate_ids:
                return
            used_candidate_ids.add(typed_id)
            primary, supports = _atoms(typed_id, operation, evidence)
            normalized_candidates.append(
                {
                    "id": typed_id,
                    "label_en": label,
                    "subtype_id": subtype_id,
                    "novelty_level": novelty,
                    "canonical_default": canonical,
                    "intent_keys": intent_keys,
                    "representation_mode": representation,
                    "integration_role": _integration_role(legacy_row["category"]),
                    "selection_cues": _unique(cues) or [typed_id],
                    "preference_profile": profile or {"variant": subtype_id},
                    "primary_atom": primary,
                    "support_atoms": supports,
                    "resource_claims": [
                        "|".join(map(str, claim))
                        for claim in compatibility_profiles[element_id][
                            "resource_claims"
                        ]
                    ],
                    "compatibility_tags": list(
                        compatibility_profiles[element_id]["rule_tags"]
                    )
                    or ["researched_moe_candidate"],
                    "source_claim_ids": [claim_definition, claim_evidence],
                    "limitation": legacy_row["limitation"],
                }
            )
            candidate_count += 1

        neutral_key = neutral["expected_candidate_selection"]["primary_candidate_key"]
        neutral_evidence = [
            group[0] for group in legacy_row["evidence_groups_en"] if group
        ][:3]
        add_candidate(
            f"{element_id}_neutral",
            label=f"Canonical researched {legacy_row['label_en']}",
            subtype_id=_slug(neutral["expected_candidate_selection"]["subtype_id"]),
            novelty=1,
            canonical=True,
            intent_keys=[neutral_key],
            representation=legacy_row["representation_mode"],
            cues=["neutral canonical default"],
            profile={"intent": "neutral"},
            operation=legacy_row["prompt_clause_en"],
            evidence=neutral_evidence,
            tags=["canonical_neutral"],
        )
        operation, preference_evidence, preference_cues = PREFERENCE_REALIZATIONS[
            element_id
        ]
        add_candidate(
            f"{element_id}_preference",
            label=f"Preference-developed {legacy_row['label_en']}",
            subtype_id=_slug(preference["expected_candidate_selection"]["subtype_id"]),
            novelty=2,
            canonical=False,
            intent_keys=[
                preference["expected_candidate_selection"]["primary_candidate_key"]
            ],
            representation={"paired_frame": "paired_or_sequence"}.get(
                preference["expected_format_routing"]["representation_mode"],
                preference["expected_format_routing"]["representation_mode"],
            ),
            cues=preference_cues,
            profile=_preference_profile(preference),
            operation=operation,
            evidence=preference_evidence,
            tags=["paired_preference_fixture"],
        )
        for index, raw_candidate in enumerate(raw_candidates):
            raw_id = _candidate_id(raw_candidate) or f"raw_{index + 1}"
            operation_values = _strings(raw_candidate.get("prompt_operation_en"))
            if not operation_values:
                continue
            subtype_values = raw_candidate.get(
                "subtype_ids",
                raw_candidate.get(
                    "subtype_links",
                    [raw_candidate.get("subtype_ref", raw_candidate.get("facet"))],
                ),
            )
            subtype_id = _slug(
                next(
                    (value for value in _strings(subtype_values) if value),
                    subtypes[0]["id"],
                )
            )
            if subtype_id not in subtype_ids:
                subtypes.append(
                    {
                        "id": subtype_id,
                        "label": subtype_id.replace("_", " "),
                        "distinction": "A research-dossier candidate facet preserved as its own route.",
                    }
                )
                subtype_ids.add(subtype_id)
            add_candidate(
                f"{element_id}_{raw_id}",
                label=str(
                    raw_candidate.get("label_en")
                    or raw_candidate.get("label_ko")
                    or raw_id
                ).replace("_", " "),
                subtype_id=subtype_id,
                novelty=_novelty(raw_candidate),
                canonical=False,
                intent_keys=[
                    f"research.{element_id.removeprefix('moe_')}.{_slug(raw_id)}"
                ],
                representation=_representation(
                    element_id, raw_candidate, legacy_row["representation_mode"]
                ),
                cues=route_cues.get(raw_id, [raw_id.replace("_", " ")]),
                profile=route_profiles.get(raw_id, {"variant": subtype_id}),
                operation=_resolve_research_placeholders(operation_values[0]),
                evidence=_evidence(raw_candidate),
                tags=[
                    str(
                        raw_candidate.get("role")
                        or raw_candidate.get("candidate_type")
                        or "research_variant"
                    )
                ],
            )
        if not any(
            candidate["novelty_level"] == 0 for candidate in normalized_candidates
        ):
            for candidate in normalized_candidates:
                if (
                    not candidate["canonical_default"]
                    and candidate["novelty_level"] == 1
                ):
                    candidate["novelty_level"] = 0
                    break

        questions = _unique(_strings(raw.get("research_questions")))
        evidence_values = _unique(
            _strings(
                raw.get(
                    "observable_or_narrative_evidence",
                    raw.get("observable_evidence", []),
                )
            )
        )
        if not evidence_values:
            evidence_values = _unique(
                [*legacy_row["observable_evidence"], *neutral_evidence]
            )
        definition = "; ".join(
            _unique(_strings(raw.get("definition_and_history")))[:10]
        )
        raw_mechanisms = _unique(_strings(raw.get("appeal_mechanisms")))
        axes = _axes(raw)
        compiled_elements.append(
            {
                "id": element_id,
                "ordinal": legacy_row["ordinal"],
                "category": legacy_row["category"],
                "label_ko": legacy_row["label_ko"],
                "aliases": legacy_row["aliases"],
                "research_questions": questions[:8],
                "definition_and_history": definition or legacy_row["design_inference"],
                "semantic_subtypes": subtypes,
                "appeal_mechanisms": [
                    {
                        "id": f"{element_id}_source_mechanism",
                        "description": raw_mechanisms[0]
                        if raw_mechanisms
                        else definition or legacy_row["design_inference"],
                        "basis": "source_supported",
                        "source_ids": definition_sources,
                    },
                    {
                        "id": f"{element_id}_design_mechanism",
                        "description": raw_mechanisms[1]
                        if len(raw_mechanisms) > 1
                        else legacy_row["design_inference"],
                        "basis": "design_inference",
                        "source_ids": [],
                    },
                ],
                "observable_or_narrative_evidence": evidence_values[:16],
                "preference_axes": axes,
                "candidates": normalized_candidates,
                "compatibility_and_conflicts": _unique(
                    _strings(
                        raw.get(
                            "compatibility_and_conflicts",
                            raw.get(
                                "compatibility_conflicts", raw.get("compatibility", [])
                            ),
                        )
                    )
                )[:16]
                or ["Resolve through the typed compatibility profile."],
                "format_implications": _unique(
                    _strings(
                        raw.get(
                            "format_implications",
                            raw.get(
                                "frame_camera_implications",
                                raw.get("pose_camera_format_resource_constraints", []),
                            ),
                        )
                    )
                )[:16]
                or [f"Default representation: {legacy_row['representation_mode']}."],
                "source_supported_claims": claims,
                "cross_source_synthesis": "; ".join(
                    _unique(_strings(raw.get("cross_source_synthesis")))[:8]
                )
                or "The culture label routes to visible construction, action, relation, camera, and format evidence rather than becoming a prompt tag.",
                "design_inference": _unique(_strings(raw.get("design_inference")))[:12]
                or [legacy_row["design_inference"]],
                "limitations": _unique(_strings(raw.get("limitations")))[:12]
                or [legacy_row["limitation"]],
            }
        )

    hard_conflicts: list[list[str]] = []
    synergies: list[dict[str, Any]] = []
    for row in compatibility["representative_combinations"]:
        pair = sorted(row["element_ids"])
        if row["decision"] == "block":
            hard_conflicts.append(pair)
        else:
            synergies.append(
                {
                    "element_ids": pair,
                    "bridge_clause_en": f"Unify the selected elements through one event spine: {row['reason']}",
                }
            )
    return {
        "schema": GRAMMAR_SCHEMA,
        "created_at": "2026-08-11T18:00:00+09:00",
        "legacy_element_asset_sha256": _sha(legacy_path),
        "legacy_research_sha256": _sha(legacy_research_path),
        "research_dossier_hashes": {
            name: _sha(dossier_root / f"{name}.json") for name in DOSSIER_NAMES
        },
        "intent_corpus_sha256": _sha(corpus_path),
        "compatibility_sha256": _sha(compatibility_path),
        "element_count": len(compiled_elements),
        "candidate_count": candidate_count,
        "source_count": len(normalized_sources),
        "sources": normalized_sources,
        "selection_contract": {
            "activation": "explicit_id_or_complete_reviewed_alias_only",
            "max_selected_elements": 3,
            "default_creativity": 0.5,
            "creative_cue_preserves_numeric_value": True,
            "candidate_precedence": [
                "explicit_preference_cue",
                "creative_development_contract",
                "numeric_creativity_band",
                "stable_seed_tiebreak",
            ],
            "max_support_atoms": 2,
        },
        "compatibility_rules": {
            "hard_conflicts": sorted(hard_conflicts),
            "synergies": sorted(synergies, key=lambda row: row["element_ids"]),
            "generic_integration_clause_en": "Use exactly one governing event and make every support element visible as its action, relation, wardrobe, pose, expression, prop, or consequence rather than as an unrelated tag.",
        },
        "elements": compiled_elements,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--asset-dir", type=Path, default=Path(__file__).resolve().parents[1] / "assets"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    asset_dir = args.asset_dir.expanduser().resolve()
    output = args.output or asset_dir / "illustration_moe_grammar_v2.json"
    payload = compile_grammar(asset_dir)
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "elements": payload["element_count"],
                "candidates": payload["candidate_count"],
                "sources": payload["source_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
