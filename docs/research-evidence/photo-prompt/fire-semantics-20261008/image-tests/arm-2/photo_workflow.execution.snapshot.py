#!/usr/bin/env python3
"""Manage frozen photographic runs, fresh audits, and bounded invocations."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import secrets
import subprocess
import sys
import uuid

from photo_workflow_state import (WorkflowError, atomic_write, bound_path, commit_stage, digest, encode,
    load_state, locked_state, file_lock, read_json, save_state, status, value, verify_freeze)


def one(value):
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if not isinstance(value, dict):
        raise WorkflowError("expected_one_object")
    return value


def stamp(row, key, expected):
    if key in row and row[key] != expected:
        raise WorkflowError("authored_binding_mismatch")
    row[key] = expected


def ensure(state):
    verify_freeze(state)
    if "retry_proof" in state["artifacts"]:
        from prepare_retry_context import verify_child
        verify_child(state)


def retrieve(args):
    with locked_state(args.run) as state:
        ensure(state)
        if "pack" in state["artifacts"]:
            if args.seed is not None and args.seed != state["retrieval_seed"]:
                raise WorkflowError("retrieval_seed_conflict")
            if getattr(args, "runtime_store", None) is not None and str(args.runtime_store.resolve()) != state["source_binding"]["runtime_store"]:
                raise WorkflowError("retrieval_store_conflict")
            pack, receipt = one(value(state, "pack")), value(state, "runtime_receipt")
            from photo_runtime_sources import RuntimeSnapshotProvider
            RuntimeSnapshotProvider(store=Path(state["source_binding"]["runtime_store"])).from_receipt(pack, receipt)
            return {"status": "pass", "phase": state["phase"], "reused": True}
        if state["phase"] != "core_frozen":
            raise WorkflowError("retrieve_requires_frozen_core")
        staging = Path(args.run).resolve() / ".staging" / "retrieve"
        staging.mkdir(parents=True, exist_ok=True)
        transaction = staging / "transaction.json"
        if transaction.exists():
            intent = read_json(transaction)
            if args.seed is not None and intent["seed"] != args.seed:
                raise WorkflowError("retrieval_seed_conflict")
        else:
            intent = {"seed": args.seed if args.seed is not None else secrets.randbits(63),
                      "runtime_store": str(args.runtime_store.resolve()) if args.runtime_store else None,
                      "source_mode": args.source_mode, "source_remote": args.source_remote, "source_ref": args.source_ref,
                      "started": False}
            atomic_write(transaction, encode(intent))
        from photo_runtime_sources import RuntimeSnapshotProvider, default_store, SKILL_ROOT
        pack_path, receipt_path = staging / "pack.json", staging / "receipt.json"
        if not pack_path.exists() or not receipt_path.exists():
            if intent["started"]:
                raise WorkflowError("incomplete_retrieve_pair_reconciliation_required")
            core = value(state, "authorial_core_normalized")
            from photo_camera_evidence import camera_authoring_declaration
            declaration = camera_authoring_declaration(core)
            requested = [axis for axis in ("direction", "height") if declaration and declaration["axes"][axis + "_requirement"] == "requested"]
            command = [sys.executable, str(Path(__file__).with_name("generate_photo_prompt.py")),
                "--request-envelope-json", str(bound_path(state, "request_envelope_input")),
                "--authorial-core-json", str(bound_path(state, "authorial_core_input")),
                "--creative-controls-json", str(bound_path(state, "creative_controls")),
                "--embodiment-review-json", str(bound_path(state, "embodiment_review")),
                "--new-author-camera-evidence", "--seed", str(intent["seed"]),
                "--output-file", str(pack_path), "--runtime-receipt", str(receipt_path),
                "--source-mode", intent["source_mode"], "--source-ref", intent["source_ref"]]
            if intent["runtime_store"]:
                command += ["--runtime-store", intent["runtime_store"]]
            if intent["source_remote"]:
                command += ["--source-remote", intent["source_remote"]]
            for axis in requested:
                command += ["--require-camera-evidence", axis]
            if args.visual_intent:
                command += ["--visual-intent-json", str(args.visual_intent.resolve())]
                intent["visual_intent_sha256"] = digest(args.visual_intent.read_bytes())
            intent["started"] = True
            atomic_write(transaction, encode(intent))
            child = subprocess.run(command, capture_output=True, text=True)
            if child.returncode:
                atomic_write(staging / "private-error.json", encode({"stderr": child.stderr}))
                raise WorkflowError("retrieve_failed_no_pair_admitted")
        pack, receipt = one(read_json(pack_path)), read_json(receipt_path)
        store = Path(intent["runtime_store"]) if intent["runtime_store"] else default_store()
        RuntimeSnapshotProvider(store=store).from_receipt(pack, receipt)
        if pack["authorial_core"] != value(state, "authorial_core_normalized") or pack["creative_controls"] != value(state, "creative_controls"):
            raise WorkflowError("retrieved_core_mismatch")
        commit_stage(args.run, state, "pack_bound", {"pack": pack_path.read_bytes(), "runtime_receipt": receipt_path.read_bytes()},
            metadata={"retrieval_seed": intent["seed"], "source_binding": {"generation_id": receipt["generation_id"],
                "source_fingerprint": receipt["source_fingerprint"], "runtime_store": str(store.resolve())}})
    return {"status": "pass", "phase": "pack_bound"}


def compose_audit(args):
    with locked_state(args.run) as state:
        ensure(state)
        if state["operations"]:
            raise WorkflowError("composition_revision_requires_new_run")
        pack = one(value(state, "pack"))
        composed = one(read_json(args.composed))
        # Choice and evidence are always authored, including explicit zero choices.
        for key in ("chosen_candidate_ids", "chosen_visual_concept_ids"):
            if key not in composed:
                raise WorkflowError("explicit_candidate_decision_required")
        stamp(composed, "pack_id", pack["pack_id"])
        stamp(composed, "core_retrieval_sha256", pack["core_retrieval"]["canonical_sha256"])
        binding = composed.get("authorial_core_binding")
        if not isinstance(binding, dict):
            raise WorkflowError("authored_core_binding_required")
        stamp(binding, "source_authorial_core_sha256", pack["authorial_core"]["canonical_sha256"])
        stamp(binding, "source_intent_lock_sha256", pack["authorial_core"]["intent_lock"]["canonical_sha256"])
        if isinstance(composed.get("embodiment_review"), dict):
            stamp(composed["embodiment_review"], "source_contract_sha256", pack["embodiment_preflight"]["canonical_sha256"])
            review = composed["embodiment_review"].get("review")
            if isinstance(review, dict):
                stamp(review, "prompt_sha256", digest(composed["prompt_en"].encode("utf-8")))
        # Stage a private revision for the real pinned auditor; admit only on pass.
        temporary = dict(state, artifacts=dict(state["artifacts"]))
        path = Path(args.run).resolve() / ".staging" / (uuid.uuid4().hex + ".composed.json")
        atomic_write(path, encode(composed))
        temporary["artifacts"]["composed"] = {"path": str(path), "sha256": digest(path.read_bytes())}
        from photo_workflow_worker import audit_bound
        result = audit_bound(temporary)["composed_audit"]
        if result["status"] != "pass" or result["failures"]:
            atomic_write(path.with_suffix(".audit.json"), encode(result))
            return result
        for role in ("render_request", "runtime_audit", "api_preflight", "native_plan", "generic_review", "visual_review", "review_audit"):
            state["artifacts"].pop(role, None)
        commit_stage(args.run, state, "composition_audited", {"composed": path.read_bytes(), "composed_audit": encode(result)})
    return result


def prepare_render(args):
    with locked_state(args.run) as state:
        ensure(state)
        if state["operations"]:
            raise WorkflowError("transport_revision_requires_new_run")
        pack, composed = one(value(state, "pack")), value(state, "composed")
        parameters = read_json(args.parameters)
        allowed = {"references", "referenced_image_paths", "num_last_images_to_include", "transparent_background",
                   "runtime_prompt_en", "runtime_negative_en"}
        if not isinstance(parameters, dict) or set(parameters) - allowed or "references" not in parameters:
            raise WorkflowError("explicit_transport_parameters_required")
        prompt = composed["prompt_en"] + ("\n\nAvoid: " + composed["negative_en"] if composed.get("negative_en") is not None else "")
        request = {"schema_version": "photo-image-render-request/v2", "pack_id": pack["pack_id"],
            "core_retrieval_sha256": pack["core_retrieval"]["canonical_sha256"],
            "source_intent_lock_sha256": pack["authorial_core"]["intent_lock"]["canonical_sha256"],
            "source_embodiment_preflight_sha256": pack["embodiment_preflight"]["canonical_sha256"],
            "runtime_prompt_en": prompt, "runtime_negative_en": composed.get("negative_en"),
            "audit_boundary": {"composed_prompt_audit_status": "pass", "runtime_prompt_audit_status": "not_run", "inherits_composed_prompt_pass": False},
            **parameters}
        if pack.get("render_repair"):
            request["render_repair_contract_sha256"] = pack["render_repair"]["canonical_sha256"]
        if composed.get("chosen_visual_concept_ids"):
            request["effective_visual_contract_sha256"] = value(state, "composed_audit").get("effective_visual_contract_sha256")
        path = Path(args.run).resolve() / ".staging" / (uuid.uuid4().hex + ".request.json")
        atomic_write(path, encode(request))
        temporary = dict(state, artifacts=dict(state["artifacts"]))
        temporary["artifacts"]["render_request"] = {"path": str(path), "sha256": digest(path.read_bytes())}
        from photo_workflow_worker import audit_bound
        result = audit_bound(temporary, runtime=True)
        if any(result[k]["status"] != "pass" or result[k]["failures"] for k in ("composed_audit", "runtime_audit")):
            return result
        outputs = {"render_request": path.read_bytes(), "runtime_audit": encode(result["runtime_audit"])}
        if args.lane == "api":
            from photo_api_render import prepare_api_render
            prepared = prepare_api_render(bound_path(state, "pack"), bound_path(state, "runtime_receipt"),
                bound_path(state, "composed"), path, model=args.model, size=args.size,
                runtime_store=state["source_binding"]["runtime_store"])
            outputs["api_preflight"] = prepared.document_bytes
        commit_stage(args.run, state, "runtime_audited", outputs, metadata={"transport": {"lane": args.lane, "model": args.model, "size": args.size}})
    return {"status": "pass", "phase": "runtime_audited", "image_call_count": 0}


def authorize(args):
    with locked_state(args.run) as state:
        ensure(state)
        scope = read_json(args.scope)
        if not isinstance(scope, dict) or set(scope) != {"lanes", "invocation_limit", "authorization_source"}:
            raise WorkflowError("invalid_authorization_scope")
        if state["mode"] != "image" or not isinstance(scope["lanes"], list) or not scope["lanes"] or set(scope["lanes"]) - {"api", "native"}:
            raise WorkflowError("unauthorized_lane")
        if type(scope["invocation_limit"]) is not int or scope["invocation_limit"] < 1:
            raise WorkflowError("invalid_invocation_limit")
        if not isinstance(scope["authorization_source"], str) or not scope["authorization_source"].strip():
            raise WorkflowError("authorization_source_required")
        if state["render_scope"] is not None and state["render_scope"] != scope:
            raise WorkflowError("authorization_revision_requires_new_run")
        state["render_scope"] = scope
        save_state(args.run, state)
    return {"status": "pass", "scope_recorded": True}


def reserve(run, lane, requested):
    with locked_state(run) as state:
        ensure(state)
        if status(state)["stale_roles"]:
            raise WorkflowError("stale_artifact")
        scope = state.get("render_scope")
        if state["mode"] != "image" or not scope or lane not in scope["lanes"]:
            raise WorkflowError("missing_existing_authorization")
        if any(op["status"] in {"reserved", "invocation_started", "execution_unknown", "record_ready", "recorder_failed", "result_received", "persistence_failed", "provider_blocked"} for op in state["operations"]):
            raise WorkflowError("pending_operation_reconcile_without_invocation")
        used = sum(len(op["attempts"]) for op in state["operations"])
        maximum = scope["invocation_limit"]
        pack = one(value(state, "pack"))
        if pack.get("render_repair"):
            maximum = min(maximum, pack["render_repair"]["retry_policy"]["maximum_additional_attempts"])
        if "retry_proof" in state["artifacts"]:
            context = value(state, "retry_context")
            maximum = min(maximum, context["execution_scope"]["additional_invocation_limit"])
        budget = min(requested, maximum - used)
        if budget < 1:
            raise WorkflowError("invocation_budget_exhausted")
        op = {"operation_id": uuid.uuid4().hex, "lane": lane, "status": "reserved", "budget": budget,
              "timestamp": datetime.now(timezone.utc).isoformat(timespec="microseconds"), "attempts": [],
              "input_bindings": {role: state["artifacts"][role]["sha256"] for role in ("pack", "runtime_receipt", "composed", "render_request")}}
        if "retry_proof" in state["artifacts"]:
            proof = value(state, "retry_proof")
            parent_run = Path(proof["parent_run"]).resolve()
            if parent_run == Path(run).resolve():
                raise WorkflowError("retry_parent_cycle")
            # Cross-child reservations protect the shared parent's additional
            # budget. Unobserved/unused reservations are conservatively retained.
            path = Path(proof["ledger"]).with_name(Path(proof["ledger"]).name + ".retry-reservations.json")
            with file_lock(path.with_name(path.name + ".LOCK")):
                reservations = read_json(path) if path.exists() else []
                parent_id = value(state, "retry_context")["parent_binding"]["ledger_run_id"]
                matching = [row for row in reservations if row["parent_run_id"] == parent_id]
                rows = [json.loads(line) for line in Path(proof["ledger"]).read_bytes().splitlines() if line.strip()]
                descendants = {parent_id}
                while True:
                    added = {row["run_id"] for row in rows if row.get("retry_of") in descendants} - descendants
                    if not added: break
                    descendants |= added
                recorded_unreserved = {row["run_id"] for row in rows if row["run_id"] in descendants - {parent_id}
                    and str(row.get("workflow_operation_id", "")).split(":")[0] not in {r["operation_id"] for r in matching}}
                remaining = value(state, "retry_context")["execution_scope"]["additional_invocation_limit"] - sum(r["reserved_invocations"] for r in matching) - len(recorded_unreserved)
                op["budget"] = min(op["budget"], remaining)
                if op["budget"] < 1: raise WorkflowError("parent_retry_budget_exhausted")
                reservations.append({"parent_run_id": parent_id, "operation_id": op["operation_id"], "child_run": str(Path(run).resolve()), "reserved_invocations": op["budget"]})
                atomic_write(path, encode(reservations))
        state["operations"].append(op)
        save_state(run, state)
    return op


def update_operation(run, identifier, event):
    with locked_state(run) as state:
        op = next(op for op in state["operations"] if op["operation_id"] == identifier)
        if event["stage"] == "invocation_started":
            if len(op["attempts"]) >= op["budget"]:
                raise WorkflowError("invocation_budget_exhausted")
            op["attempts"].append({k: event[k] for k in ("attempt", "timestamp", "run_id")})
        if event.get("ledger_args"):
            op["record_args"] = event["ledger_args"]
        if event.get("image_path"):
            path = Path(event["image_path"]).resolve()
            op["result_binding"] = {"path": str(path), "sha256": digest(path.read_bytes())}
        if event["stage"] == "preflight_failed" and event.get("known_no_invocations") and not op["attempts"] and "retry_proof" in state["artifacts"]:
            proof = value(state, "retry_proof")
            budget_path = Path(proof["ledger"]).with_name(Path(proof["ledger"]).name + ".retry-reservations.json")
            with file_lock(budget_path.with_name(budget_path.name + ".LOCK")):
                reservations = read_json(budget_path)
                for row in reservations:
                    if row["operation_id"] == identifier:
                        row["reserved_invocations"] = 0
                        row["known_no_invocations"] = True
                atomic_write(budget_path, encode(reservations))
        op["status"] = event["stage"]
        op["last_event"] = event
        if event["stage"] == "attempt_recorded" and event.get("terminal"):
            op["status"] = ("provider_blocked" if event.get("outcome") == "safety_block" else
                            "execution_unknown" if event.get("provider_outcome") == "unknown" else
                            "persistence_failed" if event.get("provider_outcome") == "returned" and event.get("outcome") == "error" else "complete")
        save_state(run, state)


def render_api(args):
    state = load_state(args.run)
    ensure(state)
    from generate_images_via_api import generate_for_request
    transport = state["transport"]
    if transport["lane"] != "api":
        raise WorkflowError("transport_lane_mismatch")
    kwargs = dict(receipt_file=bound_path(state, "runtime_receipt"), composed_file=bound_path(state, "composed"),
        request_file=bound_path(state, "render_request"), runtime_store=Path(state["source_binding"]["runtime_store"]),
        model=transport["model"], size=transport["size"], concept=args.concept, slug=None,
        out_base=Path(args.run).resolve() / "results", timestamp=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"), ledger=args.ledger)
    if args.dry_run:
        okay = generate_for_request(bound_path(state, "pack"), **kwargs, attempts=1, dry_run=True)
        return {"status": "pass" if okay else "fail", "image_call_count": 0}
    # Reaudit before reserving. No network or key read occurs here.
    from photo_api_render import prepare_api_render
    prepare_api_render(bound_path(state, "pack"), kwargs["receipt_file"], kwargs["composed_file"], kwargs["request_file"],
        model=transport["model"], size=transport["size"], runtime_store=kwargs["runtime_store"])
    op = reserve(args.run, "api", args.attempts)
    summary = Path(args.run).resolve() / "operations" / (op["operation_id"] + ".json")
    try:
        okay = generate_for_request(bound_path(state, "pack"), **kwargs, attempts=op["budget"],
            initial_retry_of=value(state, "retry_context")["parent_binding"]["ledger_run_id"] if "retry_context" in state["artifacts"] else None,
            workflow_operation_id=op["operation_id"], execution_summary=summary,
            attempt_event=lambda event: update_operation(args.run, op["operation_id"], event))
    except BaseException:
        update_operation(args.run, op["operation_id"], {"stage": "execution_unknown"})
        raise
    latest = load_state(args.run)
    active = next(row for row in latest["operations"] if row["operation_id"] == op["operation_id"])
    if active["status"] == "reserved":
        update_operation(args.run, op["operation_id"], {"stage": "preflight_failed", "known_no_invocations": True})
    return {"status": "pass" if okay else "fail", "operation_id": op["operation_id"], "summary": str(summary)}


def native_plan(args):
    state = load_state(args.run); ensure(state)
    if state["transport"]["lane"] != "native":
        raise WorkflowError("transport_lane_mismatch")
    from photo_workflow_worker import audit_bound
    result = audit_bound(state, runtime=True)
    if any(result[k]["status"] != "pass" for k in ("composed_audit", "runtime_audit")):
        raise WorkflowError("native_preflight_failed")
    request = value(state, "render_request")
    if request.get("num_last_images_to_include"):
        raise WorkflowError("native_context_references_require_local_attachment")
    payload = {"prompt": request["runtime_prompt_en"], "transparent_background": request.get("transparent_background", False)}
    if request.get("referenced_image_paths"):
        payload["referenced_image_paths"] = request["referenced_image_paths"]
    from photo_native_bridge import BRIDGE_JAVASCRIPT
    op = reserve(args.run, "native", 1)
    with locked_state(args.run) as state:
        plan = {"schema_version": "photo-native-plan/v1", "operation_id": op["operation_id"], "payload": payload,
                "input_bindings": op["input_bindings"], "references": [{"role": r["role"], "sha256": r["sha256"]} for r in request["references"]],
                "capture_helper": str(Path(__file__).with_name("image_attempt_evidence.py")), "timestamp": op["timestamp"],
                "bridge_sha256": digest(BRIDGE_JAVASCRIPT.encode("utf-8")),
                "inputs": {role: state["artifacts"][role] for role in ("pack", "runtime_receipt", "composed", "render_request")},
                "runtime_store": state["source_binding"]["runtime_store"]}
        commit_stage(args.run, state, "invocation_reserved", {"native_plan": encode(plan)})
    return {"status": "pass", "plan": state["artifacts"]["native_plan"]["path"], "operation_id": op["operation_id"]}


def native_started(args):
    state = load_state(args.run); ensure(state)
    plan = value(state, "native_plan")
    op = next(op for op in state["operations"] if op["operation_id"] == plan["operation_id"])
    if op["status"] != "reserved" or any(state["artifacts"][k]["sha256"] != sha for k, sha in plan["input_bindings"].items()):
        raise WorkflowError("native_operation_not_ready")
    from photo_native_bridge import BRIDGE_JAVASCRIPT
    if plan["bridge_sha256"] != digest(BRIDGE_JAVASCRIPT.encode("utf-8")):
        raise WorkflowError("native_bridge_changed")
    from photo_workflow_worker import audit_bound
    audited = audit_bound(state, runtime=True)
    if any(audited[k]["status"] != "pass" or audited[k]["failures"] for k in ("composed_audit", "runtime_audit")):
        raise WorkflowError("native_preflight_failed")
    composed = value(state, "composed")
    from record_image_run import stable_text_id
    run_id = stable_text_id(f"{op['timestamp']}|{stable_text_id(composed['prompt_en'])}|1")
    update_operation(args.run, op["operation_id"], {"stage": "invocation_started", "attempt": 1, "timestamp": op["timestamp"], "run_id": run_id})
    return {"status": "pass", "payload": plan["payload"], "operation_id": op["operation_id"]}


def native_result(args):
    state = load_state(args.run); ensure(state)
    plan = value(state, "native_plan")
    op = next(op for op in state["operations"] if op["operation_id"] == plan["operation_id"])
    if op["status"] not in {"invocation_started", "execution_unknown", "record_ready", "recorder_failed"}:
        raise WorkflowError("native_operation_not_started")
    observed = read_json(args.result)
    if not isinstance(observed, dict) or set(observed) - {"operation_id", "outcome", "image_path", "evidence_path", "evidence_sha256"} or observed.get("operation_id") != op["operation_id"]:
        raise WorkflowError("invalid_native_observation")
    outcome = observed.get("outcome")
    if outcome not in {"returned", "preview_only", "rejected", "unknown"}:
        raise WorkflowError("invalid_native_outcome")
    if outcome in {"preview_only", "unknown"}:
        if observed.get("image_path") or observed.get("evidence_path"):
            raise WorkflowError("invalid_native_preview")
        update_operation(args.run, op["operation_id"], {"stage": "preview_only" if outcome == "preview_only" else "execution_unknown"})
        return {"status": outcome, "image_call_count": 1}
    composed = value(state, "composed"); pack = one(value(state, "pack"))
    flags = ["--ts", op["timestamp"], "--prompt-en", composed["prompt_en"], "--attempt", "1",
        "--workflow-operation-id", op["operation_id"] + ":1", "--tool", "image_gen", "--generation-environment", "native_imagegen",
        "--pack-id", pack["pack_id"], "--authorial-core-sha256", pack["authorial_core"]["canonical_sha256"],
        "--intent-lock-sha256", pack["authorial_core"]["intent_lock"]["canonical_sha256"], "--image-call-count", "1",
        "--chosen-candidate-ids-json", json.dumps(composed["chosen_candidate_ids"]),
        "--chosen-visual-concept-ids-json", json.dumps(composed["chosen_visual_concept_ids"]), "--composer", "agent", "--audit-status", "pass",
        "--ledger", str(args.ledger), "--native-render-plan-json", str(bound_path(state, "native_plan")),
        "--native-render-plan-sha256", state["artifacts"]["native_plan"]["sha256"]]
    if pack.get("render_repair"):
        flags += ["--render-repair-contract-sha256", pack["render_repair"]["canonical_sha256"]]
    if composed["chosen_visual_concept_ids"]:
        from photo_workflow_worker import audit_bound
        effective_hash = audit_bound(state, runtime=True)["composed_audit"]["effective_visual_contract_sha256"]
        flags += ["--effective-visual-contract-sha256", effective_hash]
    for reference in plan["references"]:
        flags += ["--reference-sha256", reference["sha256"]]
    if composed.get("negative_en") is not None:
        flags += ["--negative-en", composed["negative_en"]]
    if outcome == "returned":
        path = Path(observed["image_path"]).resolve()
        if not path.is_file():
            raise WorkflowError("concrete_native_result_required")
        flags += ["--status", "success", "--image-path", str(path)]
    else:
        from image_attempt_evidence import validate_evidence
        evidence = read_json(observed["evidence_path"])
        if digest(Path(observed["evidence_path"]).read_bytes()) != observed["evidence_sha256"]:
            raise WorkflowError("stale_native_error_evidence")
        flags += ["--status", evidence["outcome"]["status"], "--attempt-evidence-json", observed["evidence_path"], "--attempt-evidence-sha256", observed["evidence_sha256"]]
    if "retry_context" in state["artifacts"]:
        flags += ["--retry-of", value(state, "retry_context")["parent_binding"]["ledger_run_id"]]
    update_operation(args.run, op["operation_id"], {"stage": "record_ready", "ledger_args": flags, "image_path": str(path) if outcome == "returned" else None})
    from generate_images_via_api import record
    try:
        recorded = record(flags)
    except RuntimeError:
        update_operation(args.run, op["operation_id"], {"stage": "recorder_failed", "ledger_args": flags})
        raise
    update_operation(args.run, op["operation_id"], {"stage": "attempt_recorded", "ledger_run_id": recorded["run_id"], "terminal": True,
        "outcome": "safety_block" if outcome == "rejected" and evidence["outcome"]["status"] == "safety_block" else outcome,
        "provider_outcome": "unknown" if outcome == "rejected" and evidence.get("provider_outcome") == "unknown" else "returned"})
    return {"status": "attempt_recorded", "ledger_run_id": recorded["run_id"]}


def resume(args):
    state = load_state(args.run)
    if state["phase"] == "core_frozen" and (Path(args.run) / ".staging/retrieve/transaction.json").exists():
        return retrieve(args)
    for op in state["operations"]:
        summary_path = Path(args.run) / "operations" / (op["operation_id"] + ".json")
        summary = read_json(summary_path) if summary_path.exists() else None
        recorded = next((event for event in reversed(summary["attempts"]) if event["stage"] == "attempt_recorded"), None) if summary else None
        ready = next((event for event in reversed(summary["attempts"]) if event["stage"] == "record_ready"), None) if summary else None
        if op["status"] in {"invocation_started", "result_received", "execution_unknown", "record_ready", "recorder_failed"} and ready:
            # Recompute and idempotently reconnect a saved row, even if the state
            # write after ledger append was interrupted. Never invoke a provider.
            from generate_images_via_api import record
            ledger_result = record(ready["ledger_args"])
            event = recorded or {"stage": "attempt_recorded", "attempt": ready.get("attempt"),
                "outcome": ready.get("outcome"), "provider_outcome": ready.get("provider_outcome")}
            update_operation(args.run, op["operation_id"], {**event, "ledger_run_id": ledger_result["run_id"], "terminal": True})
        elif op["status"] in {"record_ready", "recorder_failed"} and "ledger_args" in op.get("last_event", {}):
            from generate_images_via_api import record
            ledger_result = record(op["last_event"]["ledger_args"])
            update_operation(args.run, op["operation_id"], {"stage": "attempt_recorded", "ledger_run_id": ledger_result["run_id"], "terminal": True})
        elif op["status"] in {"invocation_started", "result_received", "execution_unknown"}:
            update_operation(args.run, op["operation_id"], {"stage": "execution_unknown"})
        if summary:
            # Restore only bytes actually returned and durably hash-bound. The
            # original failed attempt remains intact in the ledger.
            for returned in (e for e in summary["attempts"] if e["stage"] == "result_received"):
                raw = Path(returned["recovery"]).read_bytes()
                if digest(raw) != returned["sha256"]: raise WorkflowError("stale_returned_image_bytes")
                if op["status"] in {"result_received", "persistence_failed"}:
                    destination = Path(args.run).resolve() / "recovered-results" / (op["operation_id"] + f"-{returned['attempt']}.png")
                    if destination.exists() and digest(destination.read_bytes()) != returned["sha256"]:
                        raise WorkflowError("recovered_image_conflict")
                    atomic_write(destination, raw)
                    with locked_state(args.run) as latest:
                        actual_op = next(row for row in latest["operations"] if row["operation_id"] == op["operation_id"])
                        actual_op["recovered_result"] = {"path": str(destination), "sha256": returned["sha256"]}
                        actual_op["status"] = "result_saved_after_recovery"
                        save_state(args.run, latest)
    return status(load_state(args.run))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "retrieve", "resume", "view", "compose-audit", "prepare-render", "authorize", "render-api", "native-plan", "native-started", "native-result", "review-shape", "review-audit", "retry-prepare", "attach-retry", "deliver"):
        p = sub.add_parser(command, allow_abbrev=False); p.add_argument("--run", type=Path, required=True)
        if command in {"retrieve", "resume"}:
            p.add_argument("--seed", type=int); p.add_argument("--runtime-store", type=Path)
            p.add_argument("--source-mode", choices=("local_current", "remote_before_retrieval"), default="local_current")
            p.add_argument("--source-remote"); p.add_argument("--source-ref", default="main"); p.add_argument("--visual-intent", type=Path)
        if command == "view": p.add_argument("--candidate-id", action="append")
        if command == "compose-audit": p.add_argument("--composed", type=Path, required=True)
        if command == "prepare-render":
            p.add_argument("--parameters", type=Path, required=True); p.add_argument("--lane", choices=("api", "native"), required=True)
            p.add_argument("--model", default="gpt-image-2"); p.add_argument("--size", default="1024x1536")
        if command == "authorize": p.add_argument("--scope", type=Path, required=True)
        if command == "render-api":
            p.add_argument("--attempts", type=int, default=2); p.add_argument("--concept"); p.add_argument("--dry-run", action="store_true")
        if command in {"render-api", "native-result", "retry-prepare"}: p.add_argument("--ledger", type=Path, required=True)
        if command == "native-result": p.add_argument("--result", type=Path, required=True)
        if command in {"review-shape", "review-audit"}:
            p.add_argument("--image", type=Path); p.add_argument("--generic-review", type=Path); p.add_argument("--visual-review", type=Path)
        if command == "retry-prepare":
            for name in ("decision", "current-envelope", "attempt"):
                p.add_argument("--" + name, type=Path, required=True)
            p.add_argument("--output", type=Path, required=True)
        if command == "attach-retry": p.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        handlers = {"retrieve": retrieve, "compose-audit": compose_audit, "prepare-render": prepare_render, "authorize": authorize,
            "render-api": render_api, "native-plan": native_plan, "native-started": native_started, "native-result": native_result, "resume": resume}
        if args.command == "status": result = status(load_state(args.run))
        elif args.command == "view":
            state = load_state(args.run); ensure(state)
            from compose_pack_view import build_view
            result = build_view(value(state, "pack"), args.candidate_id)
        elif args.command in {"review-shape", "review-audit"}:
            from photo_workflow_reviews import review_shape, review_audit
            result = (review_shape if args.command == "review-shape" else review_audit)(args)
        elif args.command in {"retry-prepare", "attach-retry"}:
            from prepare_retry_context import prepare, attach_child
            result = (prepare if args.command == "retry-prepare" else attach_child)(args)
        elif args.command == "deliver":
            with locked_state(args.run) as state:
                ensure(state)
                from photo_workflow_worker import audit_bound
                result = audit_bound(state)["composed_audit"]
                if result["status"] == "pass":
                    state["phase"] = "prompt_delivered"; save_state(args.run, state)
        else: result = handlers[args.command](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("status") in {"fail", "error"} else 0
    except (ValueError, OSError, KeyError, TypeError, StopIteration) as error:
        print(json.dumps({"status": "error", "code": getattr(error, "code", "invalid_workflow_input")}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
