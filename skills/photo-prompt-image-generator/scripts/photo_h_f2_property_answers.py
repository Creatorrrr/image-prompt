"""Compile and match selected-RID primary-source property evidence.

Source scans occur once per profile; query matching uses compiled options.
Witness spans refer to original primary text and selected-RID effects.
"""
from __future__ import annotations

import re


def parse_intent(query: str) -> dict:
    """Separate requested answer properties from scene/context anchors.

    Values are included only when the query itself asks for them.  For example,
    an ingredient still-life layout question does not acquire centered,
    balanced, or shadow requirements from a source candidate.
    """
    text = query.casefold()
    requested: list[str] = []
    contexts: list[str] = []
    facets: dict[str, list[str]] = {}
    open_requests: list[str] = []

    if re.search(r"\b(?:model|woman|person|subject)\b.{0,45}\b(?:where|placed|placement|position)\b|\bwhere\b.{0,40}\b(?:model|woman|person|subject)\b.{0,24}\b(?:placed|positioned)\b|(?:인물|여성|사람).{0,16}(?:어디|배치|위치)|(?:어디에|어디서).{0,16}(?:놓|배치)", text):
        requested.append("subject_placement")
    if re.search(r"\b(?:landscape|open space|negative space|left open|space left)\b|\bopen\b.{0,36}\b(?:around|landscape|field|sky)\b|풍경.{0,18}(?:여백|비우|열린)|(?:여백|비워|열린).{0,24}(?:풍경|주변|하늘|들판)", text):
        requested.append("negative_space")

    camera_question = bool(re.search(
        r"\b(?:where|from where)\b.{0,56}\b(?:camera|shot|look\w* up|looking up)\b|"
        r"\b(?:camera|viewpoint)\b.{0,40}\b(?:where|from|angle|height)\b|"
        r"어디에서.{0,24}(?:올려다|위쪽|위로)|카메라.{0,24}(?:어디|시점|높이|각도)", text))
    if camera_question:
        requested.append("camera_viewpoint")
        if re.search(r"\b(?:upward|looking up|look up)\b|올려다|위로", text):
            facets["camera_viewpoint"] = ["upward"]
        elif re.search(r"\b(?:downward|looking down|look down)\b|내려다|아래로", text):
            facets["camera_viewpoint"] = ["downward"]
    if re.search(r"\b(?:stairs?|staircase|steps?)\b.{0,45}\b(?:direction|diagonal|run|lead|rise|descend|cross)\b|\b(?:direction|diagonal)\b.{0,35}\b(?:stairs?|staircase|steps?)\b|계단.{0,24}(?:방향|대각선|가로지르|이어)", text):
        requested.append("stair_direction")

    if re.search(r"\b(?:how much|amount|percentage|percent|occup\w*|take up|frame area)\b|(?:얼마나.{0,14}(?:차지|면적|비율)|차지|면적|비율|퍼센트)", text):
        requested.append("frame_occupancy")
        open_requests.append("quantity")
    if re.search(r"\b(?:foreground|near[- ]camera|close[- ]to[- ]lens)\b.{0,32}\bhand\b.{0,36}\b(?:large|big|dominates?|occup\w*|takes? up)\b|"
                 r"\bhand\b.{0,32}\b(?:large|big|dominates? the foreground|takes? up)\b.{0,36}\b(?:foreground|frame|image)\b|"
                 r"전경.{0,18}손.{0,18}(?:크|차지|보이)|손.{0,24}(?:전경|크게|차지)", text):
        contexts.append("foreground_hand_scale")
    if (re.search(r"\b(?:why|reason|cause|what makes)\b|이유|원인", text)
            and "foreground_hand_scale" in contexts):
        requested.append("causal_explanation")

    focus_requested = bool(re.search(
        r"\b(?:focus|sharp|crisp|blur\w*|soft|out of focus)\b|초점|선명|흐리|흐려|흐릿", text))
    if focus_requested:
        requested.append("focus_partition")
        sharp = bool(re.search(r"\b(?:sharp|crisp|in focus)\b|선명", text))
        soft = bool(re.search(r"\b(?:blur\w*|soft|out of focus)\b|흐리|흐려|흐릿", text))
        facets["focus_partition"] = [value for value, found in (("sharp", sharp), ("soft", soft)) if found]
        focus_owner_constraints = {}
        cue_patterns = {
            "sharp": re.compile(r"\b(?:sharp|crisp|in focus)\b|선명", re.I),
            "soft": re.compile(r"\b(?:blur\w*|soft|out of focus)\b|흐리|흐려|흐릿", re.I),
        }
        owner_patterns = {
            "head": re.compile(r"\bface\b|얼굴", re.I),
            "eyes": re.compile(r"\beyes?\b|눈", re.I),
            "leg": re.compile(r"\bknees?\b|무릎", re.I),
            "hand": re.compile(r"\bhands?\b|손", re.I),
            "environment": re.compile(r"\bbackground\b|\bwall\b|배경|벽", re.I),
        }
        separators = list(re.finditer(
            r",|;|\b(?:and|while|whereas|but)\b|그리고|반면|하지만|고(?=\s*(?:얼굴|눈|무릎|손|배경|벽))",
            text, re.I))
        for facet, pattern in cue_patterns.items():
            match = pattern.search(text)
            if not match:
                continue
            left = max((sep.end() for sep in separators if sep.end() <= match.start()), default=0)
            right = min((sep.start() for sep in separators if sep.start() >= match.end()), default=len(text))
            clause = text[left:right]
            owner_types = [owner for owner, owner_rx in owner_patterns.items() if owner_rx.search(clause)]
            if owner_types:
                focus_owner_constraints[facet] = owner_types
        if focus_owner_constraints:
            facets["focus_owner_constraints"] = focus_owner_constraints

    if re.search(r"\b(?:ingredient\w*|food)\b.{0,50}\bstill[- ]life\b|\bstill[- ]life\b.{0,50}\b(?:ingredient\w*|food)\b|재료.{0,24}정물|정물.{0,24}재료", text):
        contexts.append("ingredient_still_life")
    if re.search(r"\bseated portrait\b|앉은.{0,12}(?:인물|사진|초상)", text):
        contexts.append("seated_portrait")

    if re.search(r"\b(?:composition|layout|arrang\w*|frame arrangement|within the frame)\b|프레임.{0,12}(?:배치|구도)|구도|정물.{0,18}(?:배치|구도)", text):
        requested.append("composition_layout")

    # A bare frame-layout phrase is not a request for subject placement.  Remove
    # that accidental feature if it was found only through generic placement
    # vocabulary and no person/subject was named.
    if "subject_placement" in requested and "frame" in text and not re.search(
            r"\b(?:model|woman|person|subject)\b|인물|여성|사람", text):
        requested.remove("subject_placement")

    return {
        "requested_features": list(dict.fromkeys(requested)),
        "context_anchors": list(dict.fromkeys(contexts)),
        "explicit_value_facets": facets,
        "open_answer_requests": list(dict.fromkeys(open_requests)),
    }


def _owner_types(value) -> set[str]:
    return set(value) if isinstance(value, dict) else set(value or [])


def _source_properties(effects: dict) -> list[dict]:
    rows = effects.get("properties", []) if isinstance(effects, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def _one_span(text: str, pattern: re.Pattern) -> dict | None:
    match = pattern.search(text)
    if match is None:
        return None
    return {"start": match.start(), "end": match.end(), "quote": match.group()}


_UNQUALIFIED = re.compile(
    r"\b(?:not inferred|cannot be inferred|not specified|not enough information|cannot determine|"
    r"unclear|unknown|impossible to tell|not resolved|maybe|possibly|perhaps|might|may be|could be)\b|"
    r"추론할 수 없|명시되지 않|알 수 없|불명확|판단할 수 없", re.I)


def _cue_source_eligible(text: str, cue: dict) -> bool:
    """Reject unqualified, negated, or quoted cue uses conservatively.

    The original text span remains the only lexical evidence. A same-RID
    effect can corroborate it, but cannot turn a negated/quoted mention into a
    positive scene fact.
    """
    start, end = cue.get("start"), cue.get("end")
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end > len(text):
        return False
    sentence_start = max(text.rfind(mark, 0, start) for mark in (".", "?", "!", "。", "？", "！", "\n")) + 1
    endings = [at for mark in (".", "?", "!", "。", "？", "！", "\n")
               if (at := text.find(mark, end)) >= 0]
    sentence_end = min(endings) if endings else len(text)
    sentence = text[sentence_start:sentence_end]
    if _UNQUALIFIED.search(sentence):
        return False
    before = text[max(sentence_start, start - 32):start]
    after = text[end:min(sentence_end, end + 20)]
    if re.search(r"\b(?:not|never|without|cannot|can't)\b[^.!?;]{0,24}$|(?:않|아니|못|없이)\s*$", before, re.I):
        return False
    if re.match(r"\s*(?:\b(?:not|never|impossible)\b|(?:하지|하지는|스럽지)\s*(?:않|아니)|않|아니|못|없이)", after, re.I):
        return False
    for opening, closing in (("“", "”"), ("‘", "’"), ('"', '"')):
        left = text.rfind(opening, 0, start)
        right = text.find(closing, end)
        if left >= sentence_start and right >= end and right - left <= 220:
            return False
    return True


def _relation_options(profile: dict, feature_id: str) -> list[dict]:
    return profile.get("relations", {}).get(feature_id, {}).get("direct", [])


def _effect_options(profile: dict, feature_id: str, predicate) -> list[dict]:
    return [row for row in profile.get("relations", {}).get(feature_id, {}).get("properties", [])
            if predicate(row)]


def _profile_effect_options(profile: dict, predicate) -> list[dict]:
    """Return deduplicated same-RID effects already compiled in this profile."""
    found = {}
    for evidence in profile.get("relations", {}).values():
        for row in evidence.get("properties", []):
            if not isinstance(row, dict) or not predicate(row):
                continue
            key = (row.get("dimension"), row.get("property"), row.get("target"))
            found[key] = row
    return list(found.values())


def _same_pointer_property(direct: dict, properties: list[dict]) -> dict | None:
    # Compiled effect properties belong to the selected RID rather than to an
    # individual text pointer. They can support a primary-unit lexical witness
    # from this profile, but cannot substitute for that exact unit/span.
    return next((row for row in properties
                 if row.get("pointer") in (None, direct.get("pointer"))), None)


def _composition_relation(profile: dict, feature_id: str, required_owner_types: set[str],
                          property_pattern: re.Pattern, *, require_owner_pair: bool = False) -> list[dict]:
    """Keep exact relation cues and structured property on the same primary unit.

    For subject placement, both the placed person and frame endpoint must be
    locally named and present in the effect.  Other composition relationships
    use their own typed endpoints rather than inheriting a generic query owner.
    """
    result = []
    property_predicate = lambda row: property_pattern.search(str(row.get("property", ""))) is not None
    properties = _effect_options(profile, feature_id, property_predicate)
    # Some relations are represented structurally under a neighboring
    # relation family (for example stair-line geometry under composition).
    properties.extend(_profile_effect_options(profile, property_predicate))
    deduplicated = {}
    for prop in properties:
        deduplicated[(prop.get("dimension"), prop.get("property"), prop.get("target"))] = prop
    properties = list(deduplicated.values())
    for direct in _relation_options(profile, feature_id):
        if not any(_cue_source_eligible(direct.get("unit", ""), cue)
                   for cue in direct.get("matches", [])):
            continue
        local_owners = _owner_types(direct.get("owners"))
        prop = next((row for row in properties
                     if row.get("pointer") in (None, direct.get("pointer"))
                     and required_owner_types <= _owner_types(row.get("owners"))
                     and (not require_owner_pair or required_owner_types <= local_owners)), None)
        if prop is None:
            continue
        effect_owners = _owner_types(prop.get("owners"))
        result.append({
            "pointer": direct.get("pointer"),
            "literal_id": direct.get("literal_id"),
            "relation_cues": direct.get("matches", []),
            "source_clause": direct.get("clause"),
            "source_local_owners": sorted(local_owners),
            "effect_property": prop.get("property"),
            "effect_target": prop.get("target"),
            "effect_owner_types": sorted(effect_owners),
        })
    return result


def _owner_bound_focus(profile: dict, facets: list[str], owner_constraints: dict | None = None) -> list[dict]:
    """Bind each focus value to its exact cue and nearest source owner.

    Do not search the whole clause for every value: a clause containing both
    sharp and soft cues otherwise assigns both values to all mentioned parts.
    """
    if not facets or not set(facets) <= {"sharp", "soft"}:
        return []
    owner_constraints = owner_constraints or {}
    by_unit: dict[tuple, dict[str, list[dict]]] = {}
    for direct in _relation_options(profile, "focus_plane"):
        owners = set(direct.get("relation_owners", []))
        if not owners:
            continue
        for cue in direct.get("matches", []):
            if not _cue_source_eligible(direct.get("unit", ""), cue):
                continue
            quote = str(cue.get("quote", ""))
            quote_fold = quote.casefold()
            facet = ("sharp" if quote_fold in {"sharp", "crisp", "in focus", "clear focus", "선명"}
                     else "soft" if quote_fold in {"blur", "blurred", "blurry", "soft", "out of focus", "흐리", "흐릿"}
                     else None)
            if facet not in facets:
                continue
            if owner_constraints.get(facet) and not owners.intersection(owner_constraints[facet]):
                continue
            key = (direct.get("pointer"), direct.get("literal_id"), direct.get("source_sha256"))
            by_unit.setdefault(key, {}).setdefault(facet, []).append({
                "cue": cue,
                "source_clause": direct.get("clause"),
                "owner_types": sorted(owners),
                "owner_witnesses": direct.get("relation_owner_witnesses", {}),
            })
    result = []
    for (pointer, literal_id, _), by_facet in by_unit.items():
        if any(not by_facet.get(facet) for facet in facets):
            continue
        facet_owners = {facet: {owner for row in by_facet.get(facet, []) for owner in row["owner_types"]}
                        for facet in facets}
        if any(not owners for owners in facet_owners.values()):
            continue
        if len(facets) > 1 and len({tuple(sorted(owners)) for owners in facet_owners.values()}) == 1:
            continue
        result.append({
            "pointer": pointer,
            "literal_id": literal_id,
            "facet_evidence": {facet: by_facet.get(facet, []) for facet in facets},
            "facet_owner_types": {facet: sorted(owners) for facet, owners in facet_owners.items()},
            "sharp_owner_types": sorted(facet_owners.get("sharp", set())),
            "soft_owner_types": sorted(facet_owners.get("soft", set())),
        })
    return result


def _camera_view_options(units: list[dict], effects: dict, requested_facets: list[str]) -> list[dict]:
    camera_location_up = re.compile(
        r"\b(?:camera|viewpoint|shot)\b.{0,90}\b(?:at|from)\b.{1,130}"
        r"\b(?:looking|shooting|pointing|aimed|viewing)\s+(?:upward|up)\b|"
        r"카메라.{0,90}(?:에서|부터).{0,50}(?:올려다|위로|위쪽|위를\s*향하)", re.I)
    camera_location_down = re.compile(
        r"\b(?:camera|viewpoint|shot)\b.{0,90}\b(?:at|from)\b.{1,130}"
        r"\b(?:looking|shooting|pointing|aimed|viewing)\s+(?:downward|down)\b|"
        r"카메라.{0,90}(?:에서|부터).{0,50}(?:내려다|아래로|아래쪽|아래를\s*향하)", re.I)
    direction_effects = [row for row in _source_properties(effects)
                         if re.search(r"camera\.(?:direction|viewpoint|position|height)",
                                       str(row.get("property", "")), re.I)]
    result = []
    for unit in units:
        text = unit.get("text", "")
        for direction, pattern in (("upward", camera_location_up), ("downward", camera_location_down)):
            if requested_facets and direction not in requested_facets:
                continue
            span = _one_span(text, pattern)
            if span is None or not _cue_source_eligible(text, span):
                continue
            supporting_effects = [row for row in direction_effects
                                  if re.search(direction, str(row.get("property", "")), re.I)]
            if supporting_effects:
                result.append({"pointer": unit.get("pointer"), "direction": direction,
                               "source_span": span,
                               "effect_properties": [row.get("property") for row in supporting_effects]})
    return result


def _foreground_cause_options(units: list[dict], effects: dict) -> list[dict]:
    perspective_rx = re.compile(r"\bwide[- ]angle(?: perspective)?\b|광각.{0,10}원근", re.I)
    reach_rx = re.compile(
        r"\bhand\b.{0,70}\b(?:reach(?:es|ing)?|extend(?:s|ing)?)\b.{0,30}\b(?:toward|towards)\s+(?:the\s+)?(?:lens|camera)\b|"
        r"손.{0,45}(?:렌즈|카메라).{0,12}(?:뻗|향하)|(?:렌즈|카메라).{0,18}손.{0,15}(?:뻗|향하)", re.I)
    props = _source_properties(effects)
    has_perspective = any(re.search(r"camera\.(?:focal_length|perspective)", str(row.get("property", "")), re.I)
                          for row in props)
    hand_action = any(re.search(r"hand\.action", str(row.get("property", "")), re.I)
                      and re.search(r"hand", str(row.get("target", "")), re.I)
                      for row in props)
    foreground_projection = any(re.search(r"spatial\.foreground_projection", str(row.get("property", "")), re.I)
                                and re.search(r"hand", str(row.get("target", "")), re.I)
                                for row in props)
    has_reach = hand_action and foreground_projection
    if not (has_perspective and has_reach):
        return []
    result = []
    for unit in units:
        text = unit.get("text", "")
        perspective = _one_span(text, perspective_rx)
        reach = _one_span(text, reach_rx)
        if (perspective and reach and _cue_source_eligible(text, perspective)
                and _cue_source_eligible(text, reach)):
            result.append({"pointer": unit.get("pointer"),
                           "perspective_span": perspective,
                           "near_lens_action_span": reach,
                           "effect_properties": [row.get("property") for row in props
                                                 if re.search(r"camera\.(?:focal_length|perspective)|hand\.action|spatial\.foreground_projection",
                                                              str(row.get("property", "")), re.I)]})
    return result


def _frame_occupancy_options(units: list[dict], effects: dict) -> list[dict]:
    """Exact hand-to-frame occupancy paraphrases plus a typed same-RID effect."""
    occupancy_rx = re.compile(
        r"\bhand\b.{0,60}\b(?:occup\w*|takes? up|dominates?)\b.{0,55}\b(?:frame|image|most|\d+(?:[.–-]\d+)?\s*%)\b|"
        r"\b(?:occup\w*|takes? up|dominates?)\b.{0,50}\b(?:hand|frame|image|most|\d+(?:[.–-]\d+)?\s*%)\b|"
        r"손.{0,34}(?:프레임|화면).{0,22}(?:\d+(?:[.–-]\d+)?\s*%|대부분|큰|많은).{0,18}(?:차지|담당)|"
        r"손.{0,55}(?:차지|담당).{0,30}(?:프레임|화면)", re.I)
    effects_by_hand_frame = [row for row in _source_properties(effects)
        if re.search(r"(?:frame_occupancy|subject_occupancy|occupancy)", str(row.get("property", "")), re.I)
        and re.search(r"hand|손", str(row.get("target", "")), re.I)
        and re.search(r"frame|프레임", str(row.get("target", "")), re.I)]
    if not effects_by_hand_frame:
        return []
    result = []
    for unit in units:
        span = _one_span(unit.get("text", ""), occupancy_rx)
        if span and _cue_source_eligible(unit.get("text", ""), span):
            result.append({"pointer": unit.get("pointer"), "source_span": span,
                           "effect_properties": [row.get("property") for row in effects_by_hand_frame]})
    return result


def _scene_layout_options(intent: dict, units: list[dict], effects: dict, *, require_ingredient_context: bool = True) -> list[dict]:
    if require_ingredient_context and "ingredient_still_life" not in intent.get("context_anchors", []):
        return []
    context_rx = re.compile(r"\bingredient\w*\b.{0,80}\bstill[- ]life\b|\bstill[- ]life\b.{0,80}\bingredient\w*\b|재료.{0,24}정물|정물.{0,24}재료", re.I)
    layout_rx = re.compile(r"\b(?:composition|layout|arrangement)\b|구도|배치", re.I)
    layout_props = [row for row in _source_properties(effects)
                    if re.search(r"(?:layout|composition|spacing|shadow)", str(row.get("property", "")), re.I)]
    result = []
    for unit in units:
        text = unit.get("text", "")
        context = _one_span(text, context_rx) if require_ingredient_context else None
        requested_property = _one_span(text, layout_rx)
        has_context = not require_ingredient_context or context is not None
        if (has_context and requested_property and layout_props
                and (context is None or _cue_source_eligible(text, context))
                and _cue_source_eligible(text, requested_property)):
            result.append({"pointer": unit.get("pointer"),
                           "scene_context_span": context,
                           "requested_property_span": requested_property,
                           "effect_properties": [row.get("property") for row in layout_props],
                           "query_value_facets": intent.get("explicit_value_facets", {}).get("composition_layout", [])})
    return result


def _context_options(intent: dict, units: list[dict], profile: dict, effects: dict) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    if "ingredient_still_life" in intent.get("context_anchors", []):
        context_rx = re.compile(r"\bingredient\w*\b.{0,80}\bstill[- ]life\b|\bstill[- ]life\b.{0,80}\bingredient\w*\b|재료.{0,24}정물|정물.{0,24}재료", re.I)
        result["ingredient_still_life"] = [
            {"pointer": unit.get("pointer"), "source_span": span, "context_kind": "ingredient_still_life"}
            for unit in units
            if (span := _one_span(unit.get("text", ""), context_rx)) is not None
            and _cue_source_eligible(unit.get("text", ""), span)
        ]
    if "seated_portrait" in intent.get("context_anchors", []):
        seated_rx = re.compile(r"\b(?:sit(?:s|ting)?|seated)\b|앉", re.I)
        posture_rows = _relation_options(profile, "posture")
        posture_effects = _effect_options(profile, "posture", lambda row: bool(re.search(
            r"seat(?:ed)?|sit(?:ting|s)?|앉", str(row.get("property", "")) + " " + str(row.get("target", "")), re.I)))
        options = []
        for unit in units:
            span = _one_span(unit.get("text", ""), seated_rx)
            if span is None or not _cue_source_eligible(unit.get("text", ""), span):
                continue
            matching = [row for row in posture_rows if row.get("pointer") == unit.get("pointer")]
            if matching and posture_effects:
                options.append({"pointer": unit.get("pointer"), "source_span": span,
                                "context_kind": "seated_portrait",
                                "effect_properties": posture_effects,
                                "relation_cues": [cue for row in matching for cue in row.get("matches", [])]})
        result["seated_portrait"] = options
    if "foreground_hand_scale" in intent.get("context_anchors", []):
        hand_scale_rx = re.compile(
            r"\bhand\b.{0,48}\b(?:dominates?|occup\w*|takes? up|large|big)\b.{0,32}\b(?:foreground|frame|image)\b|"
            r"\bforeground\b.{0,32}\bhand\b.{0,48}\b(?:dominates?|occup\w*|takes? up|large|big)\b|"
            r"전경.{0,14}손.{0,28}(?:차지|큰|크|dominates?)|손.{0,32}(?:전경|프레임).{0,22}(?:차지|큰|크)", re.I)
        options = _frame_occupancy_options(units, effects)
        result["foreground_hand_scale"] = [
            {**row, "context_kind": "foreground_hand_scale"}
            for row in options
            if hand_scale_rx.search(row.get("source_span", {}).get("quote", ""))
            or re.search(r"foreground|전경", row.get("source_span", {}).get("quote", ""), re.I)
        ]
    return result


def _common_primary_pointers(witnesses: dict[str, list[dict]], required: set[str]) -> tuple[dict[str, set[str]], set[str]]:
    supported = {feature: {row.get("pointer") for row in witnesses.get(feature, []) if row.get("pointer")}
                 for feature in required if witnesses.get(feature)}
    if not required or set(supported) != required:
        return supported, set()
    return supported, set.intersection(*supported.values()) if supported else set()


def compile_property_answers(units: list[dict], profile: dict, effects: dict) -> dict:
    """Compile source answer options once per candidate/RID for query reuse.

    Query-time matching selects among these bounded, exact-span options. This
    keeps source scans and regex work out of the query/candidate inner loop.
    """
    features = {
        "subject_placement": _composition_relation(
            profile, "subject_placement", {"person", "frame"},
            re.compile(r"layout\.subject_position|subject\.position|frame_position", re.I),
            require_owner_pair=True),
        "negative_space": _composition_relation(
            profile, "negative_space", {"environment", "frame"},
            re.compile(r"negative_space|layout\.negative_space", re.I)),
        "camera_viewpoint": _camera_view_options(units, effects, []),
        "stair_direction": _composition_relation(
            profile, "stair_direction", {"stairs", "frame"},
            re.compile(r"leading_lines|stair|step|diagonal|line_direction", re.I)),
        "frame_occupancy": _frame_occupancy_options(units, effects),
        "causal_explanation": _foreground_cause_options(units, effects),
        "composition_layout": _scene_layout_options(
            {"context_anchors": []}, units, effects, require_ingredient_context=False),
        "composition_layout:ingredient_still_life": _scene_layout_options(
            {"context_anchors": ["ingredient_still_life"]}, units, effects,
            require_ingredient_context=True),
    }
    # Negative-space answer owners are frame/environment; the person's
    # presence and landscape referent scope the answer in this same unit.
    features["negative_space"] = [row for row in features["negative_space"]
        if any(row["pointer"] == unit.get("pointer")
               and re.search(r"\b(?:woman|person|model|subject)\b|여성|인물|사람", unit.get("text", ""), re.I)
               and re.search(r"\b(?:landscape|field|sky|horizon)\b|풍경|들판|하늘|지평선", unit.get("text", ""), re.I)
               for unit in units)]
    # These properties come from the selected RID; source spans are still
    # mandatory and are not inferred from effects.
    focus_effects = _effect_options(profile, "focus_plane", lambda row: bool(row.get("property")))
    focus = {}
    for key, facets in (("sharp", ["sharp"]), ("soft", ["soft"]),
                        ("sharp_soft", ["sharp", "soft"])):
        focus[key] = [{**row, "effect_properties": focus_effects}
                      for row in _owner_bound_focus(profile, facets)] if focus_effects else []
    all_contexts = {"context_anchors": ["ingredient_still_life", "seated_portrait", "foreground_hand_scale"]}
    contexts = _context_options(all_contexts, units, profile, effects)
    return {"schema": "compiled-composition-source-answers/v1",
            "owned_support": compile_owned_support(units, effects),
            "source_unit_count": len(units), "features": features,
            "focus_partitions": focus, "contexts": contexts}


def _query_focus_options(intent: dict, compiled: dict) -> list[dict]:
    facets = intent.get("explicit_value_facets", {}).get("focus_partition", [])
    key = "_".join(sorted(facets))
    options = compiled.get("focus_partitions", {}).get(key, [])
    constraints = intent.get("explicit_value_facets", {}).get("focus_owner_constraints", {})
    result = []
    for option in options:
        if any(constraints.get(facet)
               and not set(option.get("facet_owner_types", {}).get(facet, [])).intersection(constraints[facet])
               for facet in facets):
            continue
        result.append(option)
    return result


def match_property_answers(intent: dict, compiled: dict) -> dict:
    """Match explicit query properties/context against precompiled options."""
    required = set(intent.get("requested_features", []))
    features = compiled.get("features", {})
    witnesses: dict[str, list[dict]] = {}
    for feature in required:
        if feature == "focus_partition":
            witnesses[feature] = _query_focus_options(intent, compiled)
        elif feature == "camera_viewpoint":
            requested_direction = intent.get("explicit_value_facets", {}).get("camera_viewpoint", [])
            witnesses[feature] = [row for row in features.get(feature, [])
                                  if not requested_direction or row.get("direction") in requested_direction]
        elif feature == "composition_layout" and "ingredient_still_life" in intent.get("context_anchors", []):
            witnesses[feature] = features.get("composition_layout:ingredient_still_life", [])
        else:
            witnesses[feature] = features.get(feature, [])

    context_names = set(intent.get("context_anchors", []))
    contexts = {name: compiled.get("contexts", {}).get(name, []) for name in context_names}
    context_witnesses = {f"context:{key}": value for key, value in contexts.items()}
    all_witnesses = {**witnesses, **context_witnesses}
    required_scope = set(required) | set(context_witnesses)
    supported, common_pointers = _common_primary_pointers(all_witnesses, required_scope)
    complete = bool(required) and set(supported) == required_scope and bool(common_pointers)
    return {
        "requested_features": sorted(required),
        "supported_features": sorted(feature for feature in supported if not feature.startswith("context:")),
        "context_anchors": sorted(context_names),
        "supported_context_anchors": sorted(feature.removeprefix("context:") for feature in supported
                                             if feature.startswith("context:")),
        "witnesses": witnesses,
        "context_witnesses": contexts,
        "common_primary_pointers": sorted(common_pointers),
        "complete_same_primary_source_witness": complete,
        "ranking_effect": "none",
    }


def source_witness_options(intent: dict, units: list[dict], profile: dict, effects: dict) -> dict:
    """Convenience wrapper; long-lived retrieval code should compile once."""
    return match_property_answers(intent, compile_property_answers(units, profile, effects))



# Open support relationship plus an explicitly owned limb. These rules never
# infer which person leans: the answer remains a source-bound witness.
_ROLE_NAME = {'male': r'(?:(?<!wo)man|(?<!fe)male|남성|남자)', 'female': r'(?:woman|female|여성|여자)'}
_ARM_SOURCE = {
    'male': re.compile(r"\b(?:the\s+)?man(?:['’]s)\s+(?:(?:left|right)\s+)?arm\b[^.!?;\n]{0,100}\b(?:lies|rests|runs|placed|positioned)\b[^.!?;\n]{0,80}\b(?:along|on|against|behind|backrest|back|shoulders)\b|(?:남성|남자)의\s*(?:왼|오른|양쪽)?팔[^.!?;\n]{0,65}(?:놓|두|뻗|얹)",re.I),
    'female': re.compile(r"\b(?:the\s+)?woman(?:['’]s)\s+(?:(?:left|right)\s+)?arm\b[^.!?;\n]{0,100}\b(?:lies|rests|runs|placed|positioned)\b[^.!?;\n]{0,80}\b(?:along|on|against|behind|backrest|back|shoulders)\b|(?:여성|여자)의\s*(?:왼|오른|양쪽)?팔[^.!?;\n]{0,65}(?:놓|두|뻗|얹)",re.I),
}
_SUPPORT_SOURCE = re.compile(
    r"\b(?:man|woman|he|she)\b[^.!?;\n]{0,100}\b(?:leans?|rests?|press(?:es|ing)?|leaning|resting)\b[^.!?;\n]{0,130}\b(?:against|on|onto)\b[^.!?;\n]{0,90}\b(?:his|her|man|woman)\b|"
    r"(?:남성|남자|여성|여자)[^.!?;\n]{0,100}(?:남성|남자|여성|여자)[^.!?;\n]{0,55}(?:기대|가슴과\s*어깨.{0,30}대고)",re.I)
_BENCH_SOURCE = re.compile(r'\bbench\b|벤치',re.I)
_BAD_RELATION = re.compile(r'\b(?:not|never|without|maybe|perhaps|might|could|if)\b|않|아니|못|가능성|[?？"“”]',re.I)

def owned_support_query(text: str) -> dict:
    if not re.search(r'\bbench\b|벤치',text,re.I): return {}
    if not re.search(r'\bwho\b.{0,45}\b(?:lean|leaning|leans|rest|rests)\b.{0,35}\b(?:whom|who)\b|누가.{0,20}누구에게.{0,18}기대',text,re.I): return {}
    if re.search(r'\b(?:woman|man|she|he)\b.{0,40}\b(?:leans?|rests?)\b.{0,25}\b(?:woman|man|her|him)\b|(?:여성|남성|여자|남자).{0,16}(?:여성|남성|여자|남자).{0,12}기대',text,re.I): return {}
    role = ('male' if re.search(r'\bhis\s+arm\b|(?:남성|남자)의\s*팔',text,re.I) else
            'female' if re.search(r'\bher\s+arm\b|(?:여성|여자)의\s*팔',text,re.I) else None)
    if not role or not re.search(r'\bwhere\b|어디',text,re.I): return {}
    return {'support_direction_unbound':True,'arm_owner':role,'scene_context':'bench'}

def compile_owned_support(units: list[dict], effects: dict) -> dict:
    props = [p for p in effects.get('properties',[]) if isinstance(p,dict)] if isinstance(effects,dict) else []
    support_effects=[p for p in props if re.search(r'body\.(?:support|contact)|relationship.*(?:support|contact|lean)',str(p.get('property','')),re.I)]
    result={'male':[],'female':[]}
    if not support_effects: return result
    for role, arm_rx in _ARM_SOURCE.items():
        role_word = r"(?:man|male|남성|남자)" if role == 'male' else r"(?:woman|female|여성|여자)"
        property_owner = re.compile(r"(?:^|[._])" + role_word + r"(?:[_ .](?:left|right))?[_ .]arm(?:[._]|$)", re.I)
        target_owner = re.compile(r"\b" + role_word + r"(?:['’]s)?\s+(?:(?:left|right)\s+)?arm\b|" +
            (r"(?:남성|남자)의\s*(?:왼|오른)?팔" if role == 'male' else r"(?:여성|여자)의\s*(?:왼|오른)?팔"), re.I)
        arm_effects=[p for p in props if re.search(r'arm\.(?:position|placement)',str(p.get('property','')),re.I)
                     and (property_owner.search(str(p.get('property',''))) or target_owner.search(str(p.get('target',''))))]
        if not arm_effects: continue
        for unit in units:
            text=unit.get('text',''); bench=_one_span(text,_BENCH_SOURCE); support=_one_span(text,_SUPPORT_SOURCE); arm=_one_span(text,arm_rx)
            if not bench or not support or not arm: continue
            if not all(re.search(pattern, text, re.I) for pattern in _ROLE_NAME.values()): continue
            if any(not _cue_source_eligible(text,span) for span in (bench,support,arm)): continue
            if _BAD_RELATION.search(support['quote']) or _BAD_RELATION.search(arm['quote']): continue
            result[role].append({'pointer':unit['pointer'],'literal_id':unit.get('literal_id'),
                'source_sha256':unit.get('source_sha256'),'bench_span':bench,'support_span':support,
                'owned_arm_span':arm,'arm_owner':role,'support_effect_properties':support_effects,
                'arm_effect_properties':arm_effects})
    return result
