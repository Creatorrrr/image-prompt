"""Post-core, candidate-free camera checks and conservative literal projection.

This is a small English clause grammar, not a scene or camera-angle classifier.
Unresolved ownership stays unresolved; projection never creates a property lock.
"""
from __future__ import annotations

import re


CAMERA_AXES = ("direction", "height")


def require_camera_evidence(core: dict, axes: list[str]) -> None:
    """Check the writer's declared requester requirements, without inferring them."""
    if set(axes) - set(CAMERA_AXES):
        raise ValueError("camera evidence requirements must be direction or height")
    lock = core.get("intent_lock") or {}
    anchors = [a for a in lock.get("semantic_anchors") or [] if a.get("dimension") == "camera"]
    if "camera" in (lock.get("locked_dimensions") or []) and anchors:
        return
    for axis in dict.fromkeys(axes):
        if not any(a.get("property", "").startswith("viewpoint.")
                   and axis in re.findall(r"[a-z]+", a["property"])
                   and a.get("prompt_evidence") for a in anchors):
            raise ValueError(f"requester camera {axis} requires a camera viewpoint property anchor before retrieval")


def legacy_camera_clauses(core: dict, axis: str) -> list[str]:
    """Project only literal single-camera clauses from the frozen English baseline.

    Explicit actor starts and local camera verbs permit a bounded fallback for
    old cores. Depicted/background cameras, multiple cameras and negated clauses
    need independently authored owner evidence instead. No text is translated,
    completed, or added from another field or a candidate document.
    """
    if axis not in CAMERA_AXES:
        return []
    text = core.get("baseline_prompt_en") or ""
    if re.search(r"\bcameras?\b|카메라", core.get("subject") or "", re.I):
        return []
    if re.search(r"\bcameras\b|\b(?:another|second|third|first|other|both|two|three|secondary|backup)\s+(?:\w+\s+){0,2}camera\b", text, re.I):
        return []
    sentences = re.split(r"[.!?;]+\s*", text)
    if any(re.search(r"\bcamera\b", sentence, re.I)
           and re.search(r"\b(?:background|depicted|painted|displayed)\b|\b(?:toy|miniature|antique)\s+camera\b|\bon\s+display\b", sentence, re.I)
           for sentence in sentences):
        return []
    queries = []
    direction = r"(?:upwards?|downwards?|up|down|horizontally|vertically|forward|backward|ahead|left|right|towards?|from|above|below)\b"
    for sentence in sentences:
        if re.search(r"\b(?:not|never|without|instead)\b|\b\w+n['’]t\b|\brather\s+than\b", sentence, re.I):
            continue
        # Stop before another scene actor, a relative clause or a consequence.
        clause = re.split(r",|\b(?:while|whereas|because|making|which|whose|that|with)\b|\band\s+(?=the|a\b|an\b|its\b|they\b|it\s+(?:is|looks|faces|points)\b)", sentence, flags=re.I)[0].strip()
        head = re.fullmatch(
            r"(?:(?P<command>Position|Place|Put|Set|Keep|Mount|Hold|Tilt|Aim|Point|Turn)\s+(?:(?:the|our)\s+)?(?:shooting\s+)?camera\b|(?:The|Our)\s+(?:shooting\s+)?camera\b)\s*(?P<body>.+)",
            clause, re.I)
        if not head:
            continue
        body, command = head["body"], (head["command"] or "").lower()
        if axis == "direction":
            supported = (
                command in {"tilt", "aim", "point", "turn"} and re.match(direction, body, re.I)
                or re.match(r"(?:looks?|faces?|points?|aims?|tilts?|turns?|views?)\s+(?:straight\s+)?" + direction, body, re.I)
                or re.search(r"\band\s+(?:tilt|aim|point|turn)\s+(?:it|the\s+camera)\s+(?:straight\s+)?" + direction, body, re.I)
            )
        else:
            spatial = r"(?:above|below|under|low|high|lower|higher)\b|(?:at|near)\s+(?:[\w-]+\s+){0,3}(?:height|level)\b"
            supported = (
                command in {"position", "place", "put", "set", "keep", "mount", "hold"} and re.match(spatial, body, re.I)
                or re.match(r"(?:(?:is|sits|stands|remains|stays|rests)\s+(?:(?:positioned|placed|mounted|held|located)\s+)?)?" + spatial, body, re.I)
            )
        if supported and clause not in queries:
            queries.append(clause)
    return queries
