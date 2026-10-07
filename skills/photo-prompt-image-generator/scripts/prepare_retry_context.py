#!/usr/bin/env python3
"""Coordinator-only parent verification and closed retry extraction.

Writers may execute this named entrypoint and read its projected output. Parent
bytes, auditor details, and coordinator diagnostics are never printed here.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

from photo_retry_projection import project
from photo_workflow_state import (WorkflowError, atomic_write, bound_path, commit_stage, digest, encode,
    load_state, locked_state, read_json, save_state, value, verify_freeze)
from photo_workflow_worker import audit_bound


def one(raw):
    if isinstance(raw, list) and len(raw) == 1: raw = raw[0]
    if not isinstance(raw, dict): raise WorkflowError("expected_one_parent_object")
    return raw


def import_parent_manifest(path, directory):
    """Verify original legacy inputs with their worker; author no parent meaning."""
    manifest = read_json(path)
    if not isinstance(manifest, dict) or set(manifest) != {"schema_version", "artifacts", "runtime_store"} or manifest["schema_version"] != "photo-retry-parent-artifacts/v1":
        raise WorkflowError("invalid_parent_artifact_manifest")
    required = {"request_envelope_input", "authorial_core_input", "creative_controls", "pack", "runtime_receipt", "composed", "render_request"}
    optional = {"embodiment_review", "generic_review", "visual_review", "feature_selection", "catalog"}
    rows = manifest["artifacts"]
    if not isinstance(rows, dict) or not required <= rows.keys() or set(rows) - required - optional:
        raise WorkflowError("invalid_parent_artifact_roles")
    artifacts = {}
    for role, row in rows.items():
        if isinstance(row, str): row = {"path": row}
        if not isinstance(row, dict) or set(row) - {"path", "sha256"} or not isinstance(row.get("path"), str):
            raise WorkflowError("invalid_parent_artifact_path")
        source = Path(row["path"])
        source = source if source.is_absolute() else Path(path).resolve().parent / source
        sha = digest(source.read_bytes())
        if "sha256" in row and row["sha256"] != sha:
            raise WorkflowError("stale_parent_artifact")
        artifacts[role] = {"path": str(source.resolve()), "sha256": sha}
    state = {"schema_version": "photo-workflow-run/v1", "historical_parent_import": True, "artifacts": artifacts,
             "operations": [], "source_binding": {"runtime_store": str(Path(manifest["runtime_store"]).resolve())}}
    actual = audit_bound(state, runtime=True, reviews=True)
    if actual["composed_audit"]["status"] != "pass" or actual["runtime_audit"]["status"] != "pass":
        raise WorkflowError("historical_parent_audit_failed")
    for role, key in (("authorial_core_normalized", "source_core"), ("request_envelope_normalized", "source_envelope")):
        target = Path(directory) / (role + ".json")
        atomic_write(target, encode(actual[key]))
        artifacts[role] = {"path": str(target.resolve()), "sha256": digest(target.read_bytes())}
    target = Path(directory) / "imported_parent_state.json"
    atomic_write(target, encode(state))
    return state, {"path": str(target.resolve()), "sha256": digest(target.read_bytes())}


def parent_inputs(parent_state, attempt_path, ledger_path):
    from record_image_run import stable_text_id
    from photo_workflow_reviews import gates, validate_visual_scales
    if parent_state.get("historical_parent_import"):
        core, controls = value(parent_state, "authorial_core_normalized"), value(parent_state, "creative_controls")
    else:
        _, core, controls = verify_freeze(parent_state)
    pack, receipt, composed, runtime = (one(value(parent_state, k)) for k in ("pack", "runtime_receipt", "composed", "render_request"))
    if pack.get("contract_version") != "photo-candidate-pack/v6" or pack["authorial_core"] != core or pack["creative_controls"] != controls:
        raise WorkflowError("parent_core_pack_mismatch")
    audit = audit_bound(parent_state, runtime=True, reviews=True)
    if parent_state.get("historical_parent_import") and (audit.get("source_core") != core or audit.get("source_controls") != controls):
        raise WorkflowError("historical_authored_input_mismatch")
    if audit["composed_audit"]["status"] != "pass" or audit["runtime_audit"]["status"] != "pass" or audit.get("contract_failures"):
        raise WorkflowError("parent_audit_failed")
    attempt = one(read_json(attempt_path))
    ledger_rows = [json.loads(line) for line in Path(ledger_path).read_bytes().splitlines() if line.strip()]
    matches = [row for row in ledger_rows if row.get("run_id") == attempt.get("run_id")]
    if len(matches) != 1 or matches[0] != attempt:
        raise WorkflowError("parent_ledger_row_mismatch")
    if attempt.get("run_id") != stable_text_id(f"{attempt['ts']}|{stable_text_id(composed['prompt_en'])}|{attempt['attempt']}"):
        raise WorkflowError("parent_run_identity_mismatch")
    for key, expected in {"pack_id": pack["pack_id"], "prompt_en": composed["prompt_en"], "negative_en": composed.get("negative_en"),
        "authorial_core_sha256": core["canonical_sha256"], "intent_lock_sha256": core["intent_lock"]["canonical_sha256"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"], "chosen_visual_concept_ids": composed["chosen_visual_concept_ids"]}.items():
        if attempt.get(key) != expected:
            raise WorkflowError("parent_attempt_input_mismatch")
    operation = attempt.get("workflow_operation_id")
    if operation:
        identifier, number = operation.split(":")
        found = [op for op in parent_state["operations"] if op["operation_id"] == identifier]
        if len(found) != 1 or not any(row["run_id"] == attempt["run_id"] and row["attempt"] == int(number) for row in found[0]["attempts"]):
            raise WorkflowError("parent_operation_mismatch")
        if any(parent_state["artifacts"][k]["sha256"] != sha for k, sha in found[0]["input_bindings"].items()):
            raise WorkflowError("parent_operation_inputs_changed")
    if attempt.get("native_render_plan_json"):
        native_path = Path(attempt["native_render_plan_json"])
        if digest(native_path.read_bytes()) != attempt.get("native_render_plan_sha256"):
            raise WorkflowError("parent_native_plan_mismatch")
        plan = read_json(native_path)
        if any(plan["inputs"][role]["sha256"] != parent_state["artifacts"][role]["sha256"] for role in ("pack", "runtime_receipt", "composed", "render_request")) or plan["payload"]["prompt"] != runtime["runtime_prompt_en"]:
            raise WorkflowError("parent_native_plan_mismatch")
    if attempt.get("api_render_input_json"):
        # This API receipt must have been emitted for exactly the audited inputs.
        preflight = Path(attempt["api_render_input_json"])
        if digest(preflight.read_bytes()) != attempt.get("api_render_input_sha256"):
            raise WorkflowError("parent_api_preflight_mismatch")
        document = read_json(preflight)
        for role, key in (("pack", "pack"), ("runtime_receipt", "receipt"), ("composed", "composed"), ("render_request", "request")):
            row = document["inputs"][key]
            if row["sha256"] != parent_state["artifacts"][role]["sha256"] or digest(row["raw_utf8"].encode("utf-8")) != row["sha256"]:
                raise WorkflowError("parent_api_preflight_mismatch")
    reviews, failed, image_sha = {}, [], None
    for role, key in (("generic_review", "generic_review_audit"), ("visual_review", "visual_review_audit")):
        if role not in parent_state["artifacts"]: continue
        review = one(value(parent_state, role)); reviewed = audit[key]
        if role == "generic_review":
            if reviewed["status"] != "pass" or reviewed["failures"]:
                raise WorkflowError("invalid_parent_review_record")
            failed.extend(reviewed["failed_gate_ids"])
            actual_path, actual_sha = review["result"]["path"], review["result"]["sha256"]
        else:
            if reviewed["schema_failures"]:
                raise WorkflowError("invalid_parent_review_record")
            validate_visual_scales(review, audit)
            failed.extend(row["gate"] for row in reviewed["failed_hard_gates"])
            actual_path, actual_sha = review["result_image"], review["result_sha256"]
        actual = Path(actual_path)
        actual = actual if actual.is_absolute() else bound_path(parent_state, role).parent / actual
        from record_image_run import PROJECT_ROOT
        recorded_paths = {((Path(p) if Path(p).is_absolute() else PROJECT_ROOT / p).resolve()) for p in attempt.get("image_paths", [])}
        if actual.resolve() not in recorded_paths or digest(actual.read_bytes()) != actual_sha:
            raise WorkflowError("parent_review_attempt_image_mismatch")
        if image_sha is not None and image_sha != actual_sha:
            raise WorkflowError("parent_reviews_different_images")
        if attempt.get("image_hashes") and not any(row["sha256"] == actual_sha and (Path(row["path"]) if Path(row["path"]).is_absolute() else PROJECT_ROOT / row["path"]).resolve() == actual.resolve() for row in attempt["image_hashes"]):
            raise WorkflowError("parent_ledger_image_hash_mismatch")
        image_sha = actual_sha; reviews[role] = review
    if attempt["status"] == "success":
        if len(attempt.get("image_paths", [])) != 1:
            raise WorkflowError("parent_requires_one_concrete_result")
        from record_image_run import PROJECT_ROOT
        result_path = Path(attempt["image_paths"][0])
        result_path = result_path if result_path.is_absolute() else PROJECT_ROOT / result_path
        actual_result_sha = digest(result_path.read_bytes())
        recorded_hashes = attempt.get("image_hashes", [])
        if recorded_hashes and (len(recorded_hashes) != 1 or recorded_hashes[0]["sha256"] != actual_result_sha):
            raise WorkflowError("parent_ledger_image_hash_mismatch")
        if image_sha is not None and actual_result_sha != image_sha:
            raise WorkflowError("parent_review_attempt_image_mismatch")
        image_sha = actual_result_sha
        if audit.get("repair") and "generic_review" not in reviews or gates(audit) and "visual_review" not in reviews:
            raise WorkflowError("required_parent_review_missing")
    else:
        from image_attempt_evidence import validate_evidence
        validate_evidence(Path(attempt["attempt_evidence_path"]), expected_sha256=attempt["attempt_evidence_sha256"],
            attempt=attempt["attempt"], tool=attempt["tool"], generation_environment=attempt["generation_environment"],
            prompt_en=attempt["prompt_en"], negative_en=attempt.get("negative_en"), status=attempt["status"],
            runtime_prompt_en=runtime["runtime_prompt_en"] if attempt.get("native_render_plan_json") else None)
    return {"core": core, "controls": controls, "pack": pack, "receipt": receipt, "composed": composed, "runtime": runtime,
            "attempt": attempt, "reviews": reviews, "audit": audit, "failed_gate_ids": list(dict.fromkeys(failed)), "image_sha256": image_sha}


def recompute(proof):
    if proof.get("schema_version") != "photo-retry-proof/v1":
        raise WorkflowError("invalid_retry_proof")
    if proof.get("imported_parent_state"):
        row = proof["imported_parent_state"]
        if digest(Path(row["path"]).read_bytes()) != row["sha256"]:
            raise WorkflowError("stale_imported_parent_state")
        state = read_json(row["path"])
    else:
        state = load_state(proof["parent_run"])
    for role, row in proof["inputs"].items():
        if digest(Path(row["path"]).read_bytes()) != row["sha256"]:
            raise WorkflowError("stale_retry_parent_or_decision")
        if role in state["artifacts"] and state["artifacts"][role] != row:
            raise WorkflowError("parent_role_revision_changed")
    parent = parent_inputs(state, Path(proof["inputs"]["attempt"]["path"]), Path(proof["ledger"]))
    derived = parent["audit"].get("effective_visual")
    if "image" in proof["inputs"] and parent["image_sha256"] != proof["inputs"]["image"]["sha256"]:
        raise WorkflowError("stale_parent_image")
    inputs = dict(proof["inputs"])
    inputs["effective_visual"] = {"sha256": digest(encode(derived))}
    context = project(parent, read_json(proof["inputs"]["current_envelope"]["path"]), read_json(proof["inputs"]["decision"]["path"]), inputs)
    return context, parent


def prepare(args):
    output = Path(args.output).resolve()
    if (output / "retry_proof.json").exists():
        proof = read_json(output / "retry_proof.json")
        if proof["parent_run"] != str(args.run.resolve()) or proof["ledger"] != str(args.ledger.resolve()) or any(
            digest(path.read_bytes()) != proof["inputs"][role]["sha256"] for role, path in (("decision", args.decision), ("current_envelope", args.current_envelope), ("attempt", args.attempt))):
            raise WorkflowError("retry_reentry_input_conflict")
        manifest = getattr(args, "parent_manifest", None)
        if bool(manifest) != ("parent_manifest" in proof["inputs"]) or manifest and digest(manifest.read_bytes()) != proof["inputs"]["parent_manifest"]["sha256"]:
            raise WorkflowError("retry_reentry_input_conflict")
        context, _ = recompute(proof)
        if context != read_json(output / "retry_context.json"):
            raise WorkflowError("retry_projection_mismatch")
        return {"status": "pass", "context": str(output / "retry_context.json"), "reused": True}
    output.mkdir(parents=True, exist_ok=True)
    imported = None
    if getattr(args, "parent_manifest", None):
        state, imported = import_parent_manifest(args.parent_manifest, output / "private")
    else:
        state = load_state(args.run)
    roles = list(state["artifacts"]) if imported else ["request_raw", "request_envelope_input", "request_envelope_normalized", "creative_controls", "authorial_core_input",
        "authorial_core_normalized", "embodiment_review", "catalog", "feature_selection", "freeze_receipt", "freeze_author_input_hashes", "baseline",
        "pack", "runtime_receipt", "composed", "render_request"]
    roles += [k for k in ("generic_review", "visual_review", "review_audit") if k in state["artifacts"]]
    inputs = {role: state["artifacts"][role] for role in roles}
    for role, path in (("attempt", args.attempt), ("current_envelope", args.current_envelope), ("decision", args.decision)):
        # Keep an immutable coordinator copy, never rewrite the caller's file.
        raw = path.read_bytes(); target = output / "private" / (role + ".json")
        atomic_write(target, raw)
        inputs[role] = {"path": str(target), "sha256": digest(raw)}
    proof = {"schema_version": "photo-retry-proof/v1", "parent_run": str(args.run.resolve()), "inputs": inputs,
             "ledger": str(args.ledger.resolve())}
    if imported:
        target = output / "private/parent_manifest.json"
        atomic_write(target, args.parent_manifest.read_bytes())
        inputs["parent_manifest"] = {"path": str(target), "sha256": digest(target.read_bytes())}
        proof["imported_parent_state"] = imported
    try:
        context, parent = recompute(proof)
        if parent["image_sha256"] is not None:
            from record_image_run import PROJECT_ROOT
            image = Path(parent["attempt"]["image_paths"][0])
            image = image if image.is_absolute() else PROJECT_ROOT / image
            proof["inputs"]["image"] = {"path": str(image.resolve()), "sha256": parent["image_sha256"]}
            context, parent = recompute(proof)
        proof["projection_sha256"] = context["projection_sha256"]
        # A second derivation checks the closed projection against real sources.
        again, _ = recompute(proof)
        if again != context: raise WorkflowError("retry_sources_changed")
        atomic_write(output / "retry_context.json", encode(context))
        atomic_write(output / "retry_projection_audit.json", encode({"schema_version": "photo-retry-projection-audit/v1",
            "status": "pass", "projection_sha256": context["projection_sha256"], "projection_file_sha256": digest(encode(context)),
            "parent_audits_verified": True, "lineage_status": context["lineage_status"]}))
        atomic_write(output / "retry_proof.json", encode(proof))
        atomic_write(output / "private/retry_coordinator_diagnostics.json", encode({"status": "pass", "parent_audit": parent["audit"]}))
        return {"status": "pass", "context": str(output / "retry_context.json"), "lineage_status": context["lineage_status"]}
    except (ValueError, OSError, KeyError, TypeError) as error:
        atomic_write(output / "private/retry_coordinator_diagnostics.json", encode({"status": "error", "detail": str(error), "worker_detail": getattr(error, "private_detail", None)}))
        raise


def attach_child(args):
    proof = read_json(args.proof)
    context, _ = recompute(proof)
    if context != read_json(args.proof.parent / "retry_context.json"):
        raise WorkflowError("retry_projection_mismatch")
    with locked_state(args.run) as child:
        if child["phase"] not in {"request_prepared", "controls_bound"}:
            raise WorkflowError("attach_retry_before_child_freeze")
        from photo_precore_bridge import load
        envelope = load("photo_authoring_wire").normalize_request_envelope(value(child, "request_envelope_input"))
        if envelope["canonical_sha256"] != context["decision_binding"]["current_envelope_sha256"]:
            raise WorkflowError("retry_child_request_mismatch")
        commit_stage(args.run, child, child["phase"], {"retry_proof": args.proof.read_bytes(), "retry_context": encode(context)})
    return {"status": "pass", "retry_attached": True}


def verify_child(state):
    proof, context = value(state, "retry_proof"), value(state, "retry_context")
    actual, parent = recompute(proof)
    if actual != context or context["projection_sha256"] != proof["projection_sha256"]:
        raise WorkflowError("retry_projection_mismatch")
    from photo_precore_bridge import load
    envelope = load("photo_authoring_wire").normalize_request_envelope(value(state, "request_envelope_input"))
    if envelope["canonical_sha256"] != context["decision_binding"]["current_envelope_sha256"]:
        raise WorkflowError("retry_child_request_mismatch")
    if "authorial_core_normalized" not in state["artifacts"]: return context
    if context["lineage_status"] != "representable":
        raise WorkflowError("scope_not_representable_in_lineage_v2")
    child = value(state, "authorial_core_normalized")
    controls = value(state, "creative_controls")
    for name, expected in context["execution_scope"]["preserved_controls"].items():
        if controls["controls"][name]["value"] != expected["value"]:
            raise WorkflowError("child_preserved_control_changed")
    if "render_request" in state["artifacts"]:
        actual_refs = sorted((row["role"], row["sha256"]) for row in value(state, "render_request")["references"])
        expected_refs = sorted((row["role"], row["sha256"]) for row in context["execution_scope"]["references"])
        if actual_refs != expected_refs:
            raise WorkflowError("child_preserved_reference_changed")
    lineage = child.get("request_lineage") or {}
    expected = {"parent_request_id": context["parent_binding"]["request_id"], "parent_core_sha256": context["parent_binding"]["core_sha256"]}
    if any(lineage.get(k) != v for k, v in expected.items()) or set(lineage.get("preserved_dimensions", [])) != set(context["preserved_dimensions"]) or set(lineage.get("allowed_changes", [])) != set(context["allowed_scope"]["dimensions"]):
        raise WorkflowError("child_lineage_scope_mismatch")
    if child["request_binding"]["request_id"] == expected["parent_request_id"]:
        raise WorkflowError("child_requires_current_request_identity")
    for field in context["preserved_fields"]:
        scope, data = field["scope"], field["value"]
        if not any(all(row.get(k) == v for k, v in scope.items()) and row.get("prompt_evidence") == data["prompt_evidence"] for row in child["intent_lock"]["semantic_anchors"]):
            raise WorkflowError("child_preserved_lock_missing")
    for assertion in context["required_assertions"]:
        row = assertion["value"]
        if not any(all(a.get(k) == v for k, v in row.items()) for a in child["semantic_assertions"]):
            raise WorkflowError("child_required_relation_missing")
    child_targets = lineage.get("repair_targets", [])
    for target in child_targets:
        if not set(target["allowed_repair_axes"]) <= set(context["allowed_scope"]["local_axes"]):
            raise WorkflowError("child_repair_axis_widened")
    for relation in context["required_relations"]:
        old = relation["value"]
        keys = ("actor_phrase", "object_phrase", "interaction_state", "actor_object_contact")
        if not any(all(t.get(k) == old[k] for k in keys) and all(t.get(k) == v for k, v in old["frozen_evidence"].items()) for t in child_targets):
            raise WorkflowError("child_preserved_interaction_missing")
    if "pack" in state["artifacts"]:
        from photo_retry_projection import visual_obligation
        if "composed" in state["artifacts"]:
            current = audit_bound(state)
            if current["composed_audit"]["status"] != "pass":
                raise WorkflowError("child_composed_audit_failed")
            effective, failures = current["effective_visual"], current["contract_failures"]
        else:
            effective, failures = one(value(state, "pack")).get("visual_obligations"), []
        if failures and "composed" in state["artifacts"]: raise WorkflowError("child_effective_contract_invalid")
        old_ids = {row["value"]["id"] for row in context["effective_obligations"] if isinstance(row["value"], dict) and "id" in row["value"]}
        if not old_ids <= {row["id"] for row in (effective or {}).get("obligations", [])}:
            raise WorkflowError("child_preserved_effective_obligation_missing")
        for old in context["effective_obligations"]:
            if isinstance(old["value"], dict) and "id" in old["value"]:
                row = next(r for r in effective["obligations"] if r["id"] == old["value"]["id"])
                if visual_obligation(row) != old["value"]:
                    raise WorkflowError("child_effective_obligation_changed")
    return context


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare"); p.add_argument("--run", type=Path, required=True)
    for name in ("decision", "current-envelope", "attempt", "ledger", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--parent-manifest", type=Path, help="Exact legacy authored inputs and private receipt, validated in their immutable generation.")
    p = sub.add_parser("verify-child"); p.add_argument("--run", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = prepare(args) if args.command == "prepare" else {"status": "pass", "projection_sha256": verify_child(load_state(args.run))["projection_sha256"]}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError, StopIteration) as error:
        print(json.dumps({"status": "error", "code": getattr(error, "code", "retry_input_invalid")}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
