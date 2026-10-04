"""Post-core, candidate-free camera checks and conservative literal projection.

This is a small English clause grammar, not a scene or camera-angle classifier.
Unresolved ownership stays unresolved; projection never creates a property lock.
"""
from __future__ import annotations

import re
from photo_camera_clauses import bounded_camera_clauses


CAMERA_AXES = ("direction", "height")
AUTHORING_MARKER = "camera_axis_review_v1"


def camera_authoring_declaration(core: dict, *, required: bool = False) -> dict | None:
    """Validate declarations, literal binding and existing locks, not semantics.

    This uses the existing assertion/anchor wire. A partial-camera handoff is
    advisory; its requester duties remain mandatory property anchors. Reviewing
    every axis makes omission visible, but code cannot prove an author correctly
    understood a request or attributed the capture owner.
    """
    rows = [a for a in core.get("semantic_assertions") or []
            if a.get("dimension") == "camera" and "camera_axis_review" in (a.get("axes") or {})]
    if not rows:
        if required:
            raise ValueError("new camera authoring requires a separate direction/height declaration")
        return None
    if len(rows) != 1:
        raise ValueError("camera authoring requires exactly one axis declaration")
    row = rows[0]
    axes, evidence = row.get("axes") or {}, row.get("evidence") or {}
    expected = {"camera_axis_review", "capture_owner", "direction_requirement", "height_requirement"}
    if set(axes) != expected or axes["camera_axis_review"] != AUTHORING_MARKER:
        raise ValueError("camera authoring declaration has unsupported axes or version")
    if row.get("polarity") not in {"required", "advisory"}:
        raise ValueError("camera authoring declaration must use the existing required/advisory contract")
    states = {axis: axes[axis + "_requirement"] for axis in CAMERA_AXES}
    if any(not isinstance(state, str) or state not in {"requested", "open", "excluded"} for state in states.values()):
        raise ValueError("camera authoring must review direction and height as requested/open/excluded")
    requested = [axis for axis, state in states.items() if state == "requested"]
    if axes["capture_owner"] != ("camera" if requested else "unprescribed"):
        raise ValueError("requested camera axes require the declared capture owner camera")
    fields = {axis + "_phrase" for axis in requested} | ({"owner_phrase"} if requested else set())
    if set(evidence) != fields:
        raise ValueError("camera authoring requires exactly the owner and requested-axis literal evidence")
    baseline = core.get("baseline_prompt_en") or ""
    for key, phrase in evidence.items():
        maximum = 16 if key == "owner_phrase" else 24
        if not isinstance(phrase, str) or not 2 <= len(phrase.split()) <= maximum or phrase not in baseline:
            raise ValueError("camera authoring evidence must be a bounded exact literal baseline phrase")
        if re.search(r"[!?;]|\.(?:\s|$)", phrase):
            raise ValueError("camera authoring evidence must stay within one clause, not broad scene prose")
    if requested and not re.search(r"\bcamera\b", evidence["owner_phrase"], re.I):
        raise ValueError("camera authoring owner evidence must name the capture camera")
    lock = core.get("intent_lock") or {}
    anchors = [a for a in lock.get("semantic_anchors") or [] if a.get("dimension") == "camera"]
    whole = "camera" in (lock.get("locked_dimensions") or [])
    for axis, state in states.items():
        related = [a for a in anchors if a.get("property", "").startswith("viewpoint.")
                   and axis in re.findall(r"[a-z]+", a["property"])]
        if state == "requested":
            applicable = anchors if whole else [a for a in related if a.get("target") == "camera"]
            if not any(evidence[axis + "_phrase"] in (a.get("prompt_evidence") or "") for a in applicable):
                raise ValueError(f"camera {axis} declaration must bind an existing camera viewpoint anchor")
        elif related or whole:
            raise ValueError(f"camera {axis} declaration conflicts with existing requester property locks")
        if state == "excluded" and not core.get("user_exclusions"):
            raise ValueError("excluded camera axis requires requester-grounded user_exclusions")
    return row


def authored_camera_query(core: dict, axis: str) -> tuple[list[str], list[str]] | None:
    row = camera_authoring_declaration(core)
    if row is None or row["axes"][axis + "_requirement"] == "open":
        return None
    if row["axes"][axis + "_requirement"] == "excluded":
        return [], ["semantic_assertions.camera_axis_excluded"]
    evidence = row["evidence"]
    return [evidence["owner_phrase"] + " | " + evidence[axis + "_phrase"]], ["semantic_assertions.camera_axis_evidence"]


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
