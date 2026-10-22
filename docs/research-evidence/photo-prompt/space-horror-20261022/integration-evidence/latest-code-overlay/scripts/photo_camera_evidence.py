"""Post-core, candidate-free camera checks and conservative literal projection.

This is a small English clause grammar, not a scene or camera-angle classifier.
Unresolved ownership stays unresolved; projection never creates a property lock.
"""
from __future__ import annotations












from photo_precore_bridge import load as _load_precore
_authoring = _load_precore("photo_camera_authoring")
CAMERA_AXES = _authoring.CAMERA_AXES
AUTHORING_MARKER = _authoring.AUTHORING_MARKER
camera_authoring_declaration = _authoring.camera_authoring_declaration
authored_camera_query = _authoring.authored_camera_query
require_camera_evidence = _authoring.require_camera_evidence
