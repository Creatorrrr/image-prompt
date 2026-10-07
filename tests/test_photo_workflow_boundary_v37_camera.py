"""Original six camera witnesses against both actual current629 call routes.

Fixture and assertion AST nodes are compiled unchanged from the sealed original.
Only their callable namespace changes. No candidate DATA or runtime is loaded.
"""
from __future__ import annotations

import ast
import contextlib
import copy
import importlib
from pathlib import Path
import sys
import unittest
from unittest import mock

from tests import photo_workflow_boundary_v37 as v

ROOT = Path(__file__).resolve().parents[1]
PHOTO = ROOT / v.PHOTO
ORIGINAL = "tests/test_photo_camera_authoring_guidance_contract.py"
MODULE_NAMES = {
    "creative_controls", "photo_authoring_contracts", "photo_authoring_wire", "photo_camera_authoring",
    "photo_contracts", "photo_camera_evidence", "photo_camera_clauses", "photo_precore_bridge",
}


def source_node(filename, name):
    source = (PHOTO / "scripts" / filename).read_bytes()
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise AssertionError("Current camera callable source is ambiguous: " + name)
    return nodes[0]


@contextlib.contextmanager
def current_namespace(route):
    before_path = sys.path[:]
    names = MODULE_NAMES | {name for name in sys.modules if name.startswith("photo_precore_")}
    missing = object()
    before = {name: sys.modules.get(name, missing) for name in names}
    for name in names:
        sys.modules.pop(name, None)
    sys.path[:0] = [str(PHOTO / "precore"), str(PHOTO / "scripts")]
    try:
        wire = importlib.import_module("photo_authoring_wire")
        camera = importlib.import_module("photo_camera_authoring")
        contracts = importlib.import_module("photo_contracts")
        for module, directory in ((wire, "precore"), (camera, "precore"), (contracts, "scripts")):
            if Path(module.__file__).resolve().parent != PHOTO / directory:
                raise AssertionError("Current camera owner imported from another root")
        namespace = dict(vars(contracts))
        namespace.update(normalize_intent_lock=wire.normalize_intent_lock,
                         camera_authoring_declaration=camera.camera_authoring_declaration,
                         require_camera_evidence=camera.require_camera_evidence)
        future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
        scope = ast.Module(body=[future, source_node("prompt_generator.py", "authorial_core_intent_dimension_scope")], type_ignores=[])
        exec(compile(ast.fix_missing_locations(scope), str(PHOTO / "scripts/prompt_generator.py"), "exec"), namespace)
        if route == "scripts":
            evidence = importlib.import_module("photo_camera_evidence")
            bridge = importlib.import_module("photo_precore_bridge")
            if any(Path(module.__file__).resolve().parent != PHOTO / "scripts" for module in (evidence, bridge)):
                raise AssertionError("Current camera bridge imported from another root")
            # Execute the actual, bounded bridge statements, not replacement
            # aliases written in this test and not the candidate-aware module.
            tree = ast.parse((PHOTO / "scripts/prompt_generator.py").read_bytes())
            wanted = {"_authoring_wire", "normalize_intent_lock"}
            nodes = [node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == "photo_precore_bridge"]
            nodes += [node for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id in wanted for target in node.targets)]
            if len(nodes) != 3:
                raise AssertionError("Current normalize bridge source drift")
            exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])),
                         str(PHOTO / "scripts/prompt_generator.py"), "exec"), namespace)
            namespace.update(camera_authoring_declaration=evidence.camera_authoring_declaration,
                             require_camera_evidence=evidence.require_camera_evidence)
            if namespace["normalize_intent_lock"] is not bridge.load("photo_authoring_wire").normalize_intent_lock:
                raise AssertionError("Current normalize bridge does not expose its owner")
            for name in ("camera_authoring_declaration", "require_camera_evidence"):
                if namespace[name] is not getattr(bridge.load("photo_camera_authoring"), name):
                    raise AssertionError("Current camera bridge does not expose its owner")
        elif route != "neutral":
            raise AssertionError("Unknown camera route")
        yield namespace
    finally:
        touched = MODULE_NAMES | {name for name in sys.modules if name.startswith("photo_precore_")} | names
        for name in touched:
            old = before.get(name, missing)
            if old is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
        sys.path[:] = before_path


def build_cases():
    raw = (ROOT / v.retained_name(ORIGINAL)).read_bytes()
    if v.digest(raw) != v.ORIGINAL_TESTS[ORIGINAL]:
        raise AssertionError("Original six camera bodies drift")
    original = ast.parse(raw)
    functions = {"fixture", "normalize", "allows"}
    nodes = [node for node in original.body
             if (isinstance(node, ast.FunctionDef) and node.name in functions)
             or (isinstance(node, ast.ClassDef) and node.name == "CameraAuthoringGuidanceContractTests")]
    if len(nodes) != 4:
        raise AssertionError("Original camera witness closure drift")
    namespace = {"copy": copy, "unittest": unittest, "__name__": __name__}
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])),
                 str(ROOT / v.retained_name(ORIGINAL)), "exec"), namespace)
    original_case = namespace["CameraAuthoringGuidanceContractTests"]

    class CurrentBindings:
        def setUp(self):
            active = self.enterContext(current_namespace(self.route))
            self.enterContext(mock.patch.dict(namespace, {"NS": active}))
            super().setUp()

    return (type("NeutralOwnerCameraTests", (CurrentBindings, original_case), {"route": "neutral", "__module__": __name__}),
            type("ScriptsBridgeCameraTests", (CurrentBindings, original_case), {"route": "scripts", "__module__": __name__}))


NeutralOwnerCameraTests, ScriptsBridgeCameraTests = build_cases()


if __name__ == "__main__":
    unittest.main()
