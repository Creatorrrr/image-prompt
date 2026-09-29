"""Post-core bridge to the same candidate-free resolver used before authoring."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_spec = spec_from_file_location("photo_precore_creative_controls", Path(__file__).resolve().parents[1] / "precore" / "creative_controls.py")
_module = module_from_spec(_spec)
_spec.loader.exec_module(_module)
VERSION = _module.VERSION
AXES = _module.AXES
INTENSITY_CONTROLS = _module.INTENSITY_CONTROLS
LEVEL_CONTROLS = _module.LEVEL_CONTROLS
digest = _module.digest
load_definitions = _module.load_definitions
resolve = _module.resolve
validate = _module.validate
runtime_values = _module.runtime_values
authoring_brief = _module.authoring_brief
split_request_spans = _module.split_request_spans
strip_assignments = _module.strip_assignments
