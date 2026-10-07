"""Post-core, candidate-free camera checks and conservative literal projection.

This is a small English clause grammar, not a scene or camera-angle classifier.
Unresolved ownership stays unresolved; projection never creates a property lock.
"""
from __future__ import annotations

import re
from photo_camera_clauses import bounded_camera_clauses










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
    background_camera = (r"\b(?:background|depicted|painted|displayed)\s+(?:[\w-]+\s+){0,5}camera\b"
                         r"|\bcamera\b[^,;.!?]{0,60}\bbackground\b"
                         r"|\b(?:toy|miniature|antique)\s+camera\b"
                         r"|\bcamera\b[^,;.!?]{0,40}\bon\s+display\b")
    camera_parts = [part for sentence in sentences
                    for part in re.split(r",|\b(?:and|but|while|whereas)\b", sentence, flags=re.I)]
    if any(re.search(background_camera, part, re.I) for part in camera_parts):
        return []
    # Decide over complete owner predicates before extracting any literal span.
    # The bounded parser retains coordinated directions and local polarity; a
    # prefix-only fast path could silently discard their contradictory tails.
    return bounded_camera_clauses(text, axis)

from photo_precore_bridge import load as _load_precore
_authoring = _load_precore("photo_camera_authoring")
CAMERA_AXES = _authoring.CAMERA_AXES
AUTHORING_MARKER = _authoring.AUTHORING_MARKER
camera_authoring_declaration = _authoring.camera_authoring_declaration
authored_camera_query = _authoring.authored_camera_query
require_camera_evidence = _authoring.require_camera_evidence
