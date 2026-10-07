"""Neutral durable file bindings shared by pre-core and post-core commands."""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import uuid
import photo_authoring_wire as wire
import creative_controls
import photo_feature_selection as features
import photo_embodiment_review as embodiment
import photo_camera_authoring as camera

VERSION = "photo-workflow-run/v1"


class WorkflowError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    # Preserve ordered authoring_brief mappings. Canonical hashes are separate.
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def atomic_write(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def load_state(run):
    state = read_json(Path(run) / "workflow.json")
    if state.get("schema_version") != VERSION:
        raise WorkflowError("unsupported_run_version")
    return state


def save_state(run, state):
    atomic_write(Path(run) / "workflow.json", encode(state))


@contextmanager
def file_lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


@contextmanager
def locked_state(run):
    run = Path(run).resolve()
    with file_lock(run / ".LOCK"):
        yield load_state(run) if (run / "workflow.json").exists() else None


def bound_path(state, role):
    try:
        row = state["artifacts"][role]
        path = Path(row["path"])
        if not path.is_absolute() or digest(path.read_bytes()) != row["sha256"]:
            raise WorkflowError("stale_artifact")
        return path
    except (KeyError, OSError) as error:
        raise WorkflowError("missing_artifact") from error


def value(state, role):
    return read_json(bound_path(state, role))


def commit_stage(run, state, phase, outputs, *, metadata=None):
    """Write immutable revision files, then atomically admit the complete stage."""
    directory = Path(run).resolve() / "revisions" / uuid.uuid4().hex
    directory.mkdir(parents=True)
    artifacts = {}
    for role, raw in outputs.items():
        path = directory / (role + (".json" if role != "baseline" else ".txt"))
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        artifacts[role] = {"path": str(path), "sha256": digest(raw)}
    state["artifacts"].update(artifacts)
    state["phase"] = phase
    if metadata:
        state.update(metadata)
    save_state(run, state)
    return state


def verify_freeze(state):
    receipt = value(state, "freeze_receipt")
    if receipt.get("schema_version") != "photo-core-freeze/v1":
        raise WorkflowError("invalid_freeze_receipt")
    for role, expected in receipt["files"].items():
        path = bound_path(state, role)
        if digest(path.read_bytes()) != expected:
            raise WorkflowError("stale_freeze")
    envelope = wire.normalize_request_envelope(value(state, "request_envelope_input"))
    if envelope["request_text"].encode("utf-8") != bound_path(state, "request_raw").read_bytes():
        raise WorkflowError("request_bytes_mismatch")
    controls = value(state, "creative_controls")
    creative_controls.validate(controls, envelope["request_text"])
    core = wire.normalize_authorial_core(value(state, "authorial_core_input"), request_envelope=envelope,
                                         creative_control_snapshot=controls)
    if core != value(state, "authorial_core_normalized") or envelope != value(state, "request_envelope_normalized"):
        raise WorkflowError("normalized_binding_mismatch")
    features.validate_selection(value(state, "catalog"), bound_path(state, "catalog").read_bytes(), value(state, "feature_selection"),
                                value(state, "request_envelope_input"), value(state, "authorial_core_input"), value(state, "embodiment_review"))
    embodiment.build_policy(core, value(state, "embodiment_review"))
    declared = "camera" in set(core["intent_lock"]["open_dimensions"]) | set(core["intent_lock"]["locked_dimensions"])
    camera.camera_authoring_declaration(core, required=declared)
    expected = {"envelope": envelope["canonical_sha256"], "core": core["canonical_sha256"],
                "intent_lock": core["intent_lock"]["canonical_sha256"], "controls": controls["canonical_sha256"]}
    if receipt["contracts"] != expected:
        raise WorkflowError("freeze_contract_mismatch")
    return envelope, core, controls


def status(state):
    # No candidate import, parsing of packs, or filesystem traversal.
    stale = []
    for role in state["artifacts"]:
        try:
            bound_path(state, role)
        except WorkflowError:
            stale.append(role)
    for operation in state.get("operations", []):
        for key in ("result_binding", "recovered_result"):
            row = operation.get(key)
            if row:
                try:
                    if digest(Path(row["path"]).read_bytes()) != row["sha256"]:
                        stale.append(operation["operation_id"] + ":" + key)
                except OSError:
                    stale.append(operation["operation_id"] + ":" + key)
    operations = [{k: row[k] for k in ("operation_id", "lane", "status", "attempts", "recovered_result") if k in row}
                  for row in state.get("operations", [])]
    return {"schema_version": VERSION, "run_id": state["run_id"], "mode": state["mode"],
            "phase": "stale" if stale else state["phase"], "stale_roles": stale, "operations": operations,
            "technical_qualification": state.get("technical_qualification"), "user_judgment": state.get("user_judgment")}
