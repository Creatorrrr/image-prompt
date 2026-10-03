"""Bounded local camera clause structure; literal spans, no scene completion.

Owner NP modifiers, predicates and conjunctions are parsed separately. Lens
attachment is local to a single explicit camera. This is deliberately not a
whole-scene parser; unsupported attachments and polarity stay unresolved.
"""
from __future__ import annotations

import re

CAMERA_NP = r"(?:the|our)\s+(?:shooting\s+)?camera\b"
IMAGE_NP = r"(?:(?:this|the|a|our)\s+)?(?:photograph|photo|picture|image|scene)\b"
CAPTURE_MODIFIER = (
    r"\s+(?:(?:that|which)\s+)?(?:(?:is|was)\s+)?(?:\w+ly\s+)?"
    r"(?:(?:taking|takes|making|makes|producing|produces|recording|records|capturing|captures)\s+"
    r"|used\s+(?:to\s+(?:take|make|record|capture)\s+|for\s+))" + IMAGE_NP
)
COMMAND = r"(?:position|place|put|set|keep|mount|hold|tilt|aim|point|turn)"
DIRECTION = r"(?:upwards?|downwards?|up|down|horizontally|vertically|forward|backward|ahead|left|right|towards?|from|above|below)\b"
LOCATIVE = (r"(?:(?:just|very|slightly)\s+)?(?:above|below|under|low|high|lower|higher)\b"
            r"|(?:close|near)\s+to\s+(?:the\s+)?(?:floor|ground|pavement)\b"
            r"|(?:at|near)\s+(?:[\w-]+\s+){0,3}(?:height|level)\b"
            r"|(?:\d+|one|two|three|four|five|ten)\s+(?:centimeters?|centimetres?|meters?|metres?|inches|feet)\s+(?:above|below)\b")
COPULA = r"(?:(?:is|was|sits|stands|remains|stays|rests)\s+(?:(?:positioned|placed|mounted|held|located)\s+)?)?"
NEGATIVE = r"\b(?:not|never|without|instead|rather\s+than)\b|\b\w+n['’]t\b"
UNCERTAIN = r"\b(?:might|could|may|would|perhaps|supposedly|allegedly|apparently|seemingly|presumably|if)\b"


def _axes(predicate: str, command: str = "") -> set[str]:
    result = set()
    if (command in {"tilt", "aim", "point", "turn"} and re.match(DIRECTION, predicate, re.I)
        or re.match(r"(?:looks?|faces?|points?|aims?|tilts?|turns?|views?)\s+(?:straight\s+)?" + DIRECTION, predicate, re.I)
        or re.match(r"(?:(?:is|was|remains)\s+)?(?:tilted|aimed|pointed|angled|turned|oriented)\s+(?:straight\s+)?" + DIRECTION, predicate, re.I)
        or re.match(r"(?:(?:is|was)\s+)?raised\s+to\s+(?:look|point|aim)\s+" + DIRECTION, predicate, re.I)):
        result.add("direction")
    if (command in {"position", "place", "put", "set", "keep", "mount", "hold"} and re.match(LOCATIVE, predicate, re.I)
        or not command and re.match(COPULA + r"(?:" + LOCATIVE + r")", predicate, re.I)):
        result.add("height")
    return result


def _orientation(text: str) -> set[str]:
    # Used only for a local negative-tail contradiction guard, never to infer
    # height or add canonical direction text to a prompt/query.
    result = set()
    for value, pattern in (("up", r"\bup(?:ward(?:s)?)?\b"), ("down", r"\bdown(?:ward(?:s)?)?\b"),
                           ("horizontal", r"\bhorizontally?\b"), ("vertical", r"\bvertically?\b")):
        if re.search(pattern, text, re.I):
            result.add(value)
    return result


def bounded_camera_clauses(text: str, axis: str) -> list[str]:
    queries = []
    for sentence in re.split(r"[.!?;]+\s*", text):
        if re.search(UNCERTAIN, sentence, re.I) or re.search(r"\brather\s+than\b|\binstead\b", sentence, re.I):
            continue
        sentence = sentence.strip()
        camera = re.match(r"(?P<for>for\s+)?(?P<owner>" + CAMERA_NP + r")", sentence, re.I)
        command = re.match(r"(?P<verb>" + COMMAND + r")\s+(?:(?:the|our)\s+)?(?:shooting\s+)?camera\b", sentence, re.I)
        if not camera and not command:
            continue
        end = (camera or command).end()
        modifier = re.match(CAPTURE_MODIFIER, sentence[end:], re.I) if camera else None
        if modifier:
            end += modifier.end()
        if camera and camera["for"] and not modifier:
            continue
        owner_only = camera is not None and camera["for"] is not None
        cursor, span_end, found = end, end, set()
        first_command = command["verb"].lower() if command else ""
        # Delimiters are recognized structurally. A subsequent piece is kept
        # only if it is a predicate of this owner or an unambiguous local lens.
        pieces = list(re.finditer(r"(?:^|,\s*(?:with\s+)?|\s+and\s+|\s+with\s+)([^,]+?)(?=,|\s+and\s+|\s+with\s+|$)", sentence[cursor:], re.I))
        positive_direction = set()
        invalid = False
        for index, piece in enumerate(pieces):
            content = piece[1].strip()
            content_start = cursor + piece.start(1) + len(piece[1]) - len(piece[1].lstrip())
            delimiter = piece[0][:piece.start(1) - piece.start()]
            if content.lower().startswith("without "):
                tail = re.fullmatch(r"without\s+(?:(?:a|an|any|the)\s+)?(upwards?|downwards?|up|down|horizontal|vertical)\s+(?:tilt|angle|aim)(?:\s+.*)?", content, re.I)
                denied = _orientation(content)
                if not tail or not denied or "direction" in found and (not positive_direction or denied & positive_direction):
                    invalid = True
                break
            if re.search(NEGATIVE, content, re.I):
                invalid = True
                break
            # Stop before subordinate scene actors and consequences.
            content = re.split(r"\b(?:while|whereas|because|keeping|including|making|which|whose|that|but)\b", content, maxsplit=1, flags=re.I)[0].strip()
            lens = re.match(r"(?:its|the)\s+lens\s+", content, re.I)
            explicit_camera_object = re.match(r"(?P<verb>" + COMMAND + r")\s+(?:it|the\s+camera)\s+", content, re.I)
            predicate, local_command = content, first_command if index == 0 else ""
            if lens:
                if not found and not modifier:
                    break
                predicate = content[lens.end():]
            elif explicit_camera_object:
                predicate, local_command = content[explicit_camera_object.end():], explicit_camera_object["verb"].lower()
            elif owner_only:
                break
            # A new noun subject cannot inherit the camera's ownership. The
            # predicate grammar has an anchored start, not a substring search.
            axes = _axes(predicate, local_command)
            if not axes:
                break
            if index and delimiter.strip().lower() == "with" and not lens:
                break
            found.update(axes)
            if "direction" in axes:
                positive_direction.update(_orientation(predicate))
            span_end = content_start + len(content)
            owner_only = False
        if not invalid and axis in found:
            clause = sentence[:span_end].strip(" ,")
            if clause and clause not in queries:
                queries.append(clause)
    return queries
