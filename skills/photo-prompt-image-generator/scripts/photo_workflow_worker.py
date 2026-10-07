"""Run real auditors inside the exact immutable parent generation.

The bridge is supplied as code to a compatible Python process. It never copies
new source into a saved generation or lets current DATA reinterpret an old pack.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from photo_workflow_state import WorkflowError, bound_path, read_json

BRIDGE = r'''
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import audit_composed_prompt as ca
import audit_image_render_request as ra
import audit_image_render_review as gr
import audit_moe_render_review as vr
from photo_runtime_sources import RuntimeSnapshotProvider
payload = json.loads(Path(sys.argv[2]).read_bytes())
objects, paths = {}, {}
for role, row in payload["inputs"].items():
    path = Path(row["path"])
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != row["sha256"]:
        raise ValueError("stale_worker_input")
    objects[role] = ra.one_object(json.loads(raw), role)
    paths[role] = path
pack, receipt, composed = (objects[k] for k in ("pack", "runtime_receipt", "composed"))
snapshot = RuntimeSnapshotProvider(store=Path(payload["store"])).from_receipt(pack, receipt)
authored = {}
if payload.get("historical_parent_import"):
    import prompt_generator as generator
    envelope = generator.normalize_request_envelope(objects["request_envelope_input"])
    controls = objects["creative_controls"]
    core = generator.normalize_authorial_core(objects["authorial_core_input"], request_envelope=envelope, creative_control_snapshot=controls)
    if core != pack["authorial_core"] or controls != pack["creative_controls"]:
        raise ValueError("historical_authored_input_mismatch")
    authored = {"source_core": core, "source_envelope": envelope, "source_controls": controls}
first = ca.audit_composed_prompt(pack, composed, source_data=snapshot.data)
result = {"composed_audit": first, **authored}
if "render_request" in objects:
    result["runtime_audit"] = ra.audit_image_render_request(pack, composed, objects["render_request"], request_path=paths["render_request"])
# The source-bound audit above must pass before contract/review derivation.
if first["status"] == "pass" and not first["failures"]:
    # Keep the old auditor's internal character review in the same source context.
    ca._audit_source_data = lambda: snapshot.data
    effective, failures = ca.derive_effective_visual_obligation_contract(pack, composed)
    character, gates, character_failures = vr.derive_character_response_render_gates(pack, composed)
    embodiment, embodiment_failures = ca.photo_embodiment.render_gate_ids(pack, composed)
    result.update(effective_visual=effective, contract_failures=failures + character_failures + embodiment_failures,
                  repair=ca.expected_render_repair_contract(pack["authorial_core"]),
                  character=character, character_gates=gates, embodiment_gates=embodiment)
    if "generic_review" in objects:
        result["generic_review_audit"] = gr.audit_image_render_review(pack, composed, objects["generic_review"], review_path=paths["generic_review"])
    if "visual_review" in objects:
        result["visual_review_audit"] = vr.audit_moe_render_review(pack, objects["visual_review"], composed=composed, review_path=paths["visual_review"])
Path(sys.argv[3]).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
'''


def audit_bound(state, *, runtime=False, reviews=False):
    from photo_runtime_sources import SnapshotPublisher, default_store, environment_binding
    receipt = read_json(bound_path(state, "runtime_receipt"))
    generation = receipt.get("generation_id", "")
    import re
    if not isinstance(generation, str) or not re.fullmatch(r"[0-9a-f]{64}", generation):
        raise WorkflowError("invalid_generation_id")
    store = Path((state.get("source_binding") or {}).get("runtime_store") or default_store()).resolve()
    root = store / "generations" / generation
    manifest = SnapshotPublisher._verify_generation(root, generation)
    if manifest["source"]["environment"] != environment_binding():
        raise WorkflowError("incompatible_historical_worker")
    roles = ["pack", "runtime_receipt", "composed"]
    if runtime:
        roles.append("render_request")
    if reviews:
        roles.extend(k for k in ("generic_review", "visual_review") if k in state["artifacts"])
    if state.get("historical_parent_import"):
        roles.extend(("request_envelope_input", "authorial_core_input", "creative_controls"))
    inputs = {}
    for role in roles:
        bound_path(state, role)
        inputs[role] = state["artifacts"][role]
    with tempfile.TemporaryDirectory(prefix="photo-bound-audit-") as folder:
        folder = Path(folder)
        source, target = folder / "input.json", folder / "result.json"
        source.write_text(json.dumps({"inputs": inputs, "store": str(store), "historical_parent_import": state.get("historical_parent_import", False)}), encoding="utf-8")
        child = subprocess.run([sys.executable, "-c", BRIDGE, str(root / "scripts"), str(source), str(target)],
                               capture_output=True, text=True)
        if child.returncode or not target.exists():
            # This exception detail belongs to the coordinator, never retry stdout.
            error = WorkflowError("historical_worker_failed")
            error.private_detail = child.stderr[-4000:]
            raise error
        return read_json(target)
