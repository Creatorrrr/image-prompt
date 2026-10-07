#!/usr/bin/env python3
"""Prepare and freeze current authored inputs without candidate access."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import uuid

import creative_controls
import photo_authoring_wire as wire
import photo_camera_authoring as camera
import photo_embodiment_review as embodiment
import photo_feature_selection as features
from photo_run_files import (VERSION, WorkflowError, bound_path, commit_stage, digest, encode,
                             locked_state, read_json, save_state, value, verify_freeze)


def stamp(row, key, expected):
    if key in row and row[key] != expected:
        raise WorkflowError("stale_authored_binding")
    row[key] = expected


def init(args):
    raw = args.request.read_bytes()
    request = raw.decode("utf-8")
    if args.whole_request:
        spans = [{"span_id": "request", "start": 0, "end": len(request)}]
    else:
        spans = read_json(args.spans)
    if not isinstance(spans, list):
        raise WorkflowError("invalid_span_shape")
    for span in spans:
        if not isinstance(span, dict) or set(span) != {"span_id", "start", "end"}:
            raise WorkflowError("explicit_span_offsets_required")
        if type(span["start"]) is not int or type(span["end"]) is not int:
            raise WorkflowError("invalid_span_offsets")
        span["text"] = request[span["start"]:span["end"]]
    envelope = {"contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
                "request_id": args.request_id or "request-" + uuid.uuid4().hex, "request_text": request,
                "request_sha256": digest(raw), "active_spans": spans}
    wire.normalize_request_envelope(envelope)
    with locked_state(args.run) as state:
        if state is not None:
            raise WorkflowError("run_already_exists_use_new_run")
        state = {"schema_version": VERSION, "run_id": uuid.uuid4().hex, "mode": args.mode,
                 "phase": "request_prepared", "artifacts": {}, "source_binding": None,
                 "render_scope": None, "operations": []}
        commit_stage(args.run, state, "request_prepared", {"request_raw": raw,
            "request_envelope_input": encode(envelope), "authoring_shapes": Path(__file__).with_name("photo_workflow_shapes.json").read_bytes()})
    return {"status": "pass", "phase": state["phase"], "request_id": envelope["request_id"]}


def controls(args):
    with locked_state(args.run) as state:
        if state is None or state["phase"] != "request_prepared":
            raise WorkflowError("controls_require_prepared_request")
        request = value(state, "request_envelope_input")["request_text"]
        snapshot = creative_controls.resolve(request, overrides=read_json(args.overrides) if args.overrides else None,
            context=read_json(args.context), seed=args.seed)
        commit_stage(args.run, state, "controls_bound", {"creative_controls": encode(snapshot)})
    return {"status": "pass", "phase": state["phase"]}


def freeze(args):
    with locked_state(args.run) as state:
        if state is None or state["phase"] not in {"controls_bound", "core_frozen"}:
            raise WorkflowError("freeze_requires_controls")
        if state["phase"] == "core_frozen":
            verify_freeze(state)
            # Reentry must be the same authored inputs, never silently ignore edits.
            author = value(state, "freeze_author_input_hashes")
            if author != {k: digest(p.read_bytes()) for k, p in (("core", args.core), ("selection", args.selection), ("review", args.review))}:
                raise WorkflowError("frozen_inputs_changed_use_new_run")
            return {"status": "pass", "phase": "core_frozen", "reused": True}
        envelope_input = value(state, "request_envelope_input")
        envelope = wire.normalize_request_envelope(envelope_input)
        snapshot = value(state, "creative_controls")
        authored = read_json(args.core)
        stamp(authored, "source_request", envelope["request_text"])
        stamp(authored, "creative_controls_sha256", snapshot["canonical_sha256"])
        if "retry_context" in state["artifacts"]:
            context = value(state, "retry_context")
            lineage = authored.get("request_lineage")
            if not isinstance(lineage, dict):
                raise WorkflowError("authored_child_lineage_required")
            stamp(lineage, "parent_request_id", context["parent_binding"]["request_id"])
            stamp(lineage, "parent_core_sha256", context["parent_binding"]["core_sha256"])
        baseline = authored.get("baseline_prompt_en")
        if not isinstance(baseline, str) or baseline != wire.clean_spaces(baseline):
            raise WorkflowError("canonicalize_baseline_before_evidence_review")
        core = wire.normalize_authorial_core(authored, request_envelope=envelope, creative_control_snapshot=snapshot)
        review = read_json(args.review)
        stamp(review, "prompt_sha256", digest(baseline.encode("utf-8")))
        embodiment.build_policy(core, review)
        declared = "camera" in set(core["intent_lock"]["open_dimensions"]) | set(core["intent_lock"]["locked_dimensions"])
        camera.camera_authoring_declaration(core, required=declared)
        selection = read_json(args.selection)
        catalog = Path(__file__).with_name("visual_feature_catalog.json").read_bytes()
        for key, expected in {"contract_version": features.SELECTION_VERSION, "catalog_path": features.CATALOG_PATH,
            "catalog_schema_version": features.CATALOG_VERSION, "catalog_sha256": digest(catalog),
            "request_id": envelope["request_id"], "request_sha256": envelope["request_sha256"],
            "active_span_ids": [s["span_id"] for s in envelope["active_spans"]],
            "baseline_prompt_sha256": digest(baseline.encode("utf-8"))}.items():
            stamp(selection, key, expected)
        selection_audit = features.validate_selection(json.loads(catalog), catalog, selection, envelope_input, authored, review)
        outputs = {"authorial_core_input": encode(authored), "authorial_core_normalized": encode(core),
            "request_envelope_normalized": encode(envelope), "embodiment_review": encode(review),
            "feature_selection": encode(selection), "feature_selection_audit": encode(selection_audit), "catalog": catalog, "baseline": baseline.encode("utf-8"),
            "freeze_author_input_hashes": encode({k: digest(p.read_bytes()) for k, p in (("core", args.core), ("selection", args.selection), ("review", args.review))})}
        receipt = {"schema_version": "photo-core-freeze/v1", "files": {
            **{k: state["artifacts"][k]["sha256"] for k in ("request_raw", "request_envelope_input", "creative_controls")},
            **{k: digest(v) for k, v in outputs.items()}}, "contracts": {
            "envelope": envelope["canonical_sha256"], "core": core["canonical_sha256"],
            "intent_lock": core["intent_lock"]["canonical_sha256"], "controls": snapshot["canonical_sha256"]}}
        outputs["freeze_receipt"] = encode(receipt)
        commit_stage(args.run, state, "core_frozen", outputs)
        verify_freeze(state)
        if "retry_proof" in state["artifacts"]:
            # Explicit retry execution exception: only the coordinator reads
            # parent artifacts; this process receives a sanitized exit code.
            import subprocess
            child = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/prepare_retry_context.py"),
                "verify-child", "--run", str(args.run)], capture_output=True, text=True)
            if child.returncode:
                state["phase"] = "retry_binding_failed"
                save_state(args.run, state)
                import re
                try:
                    reported = json.loads(child.stderr).get("code")
                except (ValueError, AttributeError):
                    reported = None
                code = reported if isinstance(reported, str) and re.fullmatch(r"[a-z0-9_]{1,80}", reported) else "retry_child_freeze_binding_failed"
                raise WorkflowError(code)
    return {"status": "pass", "phase": "core_frozen"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("--run", type=Path, required=True)
    p.add_argument("--request", type=Path, required=True); p.add_argument("--request-id")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--whole-request", action="store_true"); group.add_argument("--spans", type=Path)
    p.add_argument("--mode", choices=("prompt_only", "image"), required=True)
    p = sub.add_parser("controls"); p.add_argument("--run", type=Path, required=True)
    p.add_argument("--context", type=Path, required=True); p.add_argument("--overrides", type=Path); p.add_argument("--seed", type=int)
    p = sub.add_parser("canonicalize"); p.add_argument("--baseline", type=Path, required=True)
    p = sub.add_parser("freeze"); p.add_argument("--run", type=Path, required=True)
    for name in ("core", "selection", "review"):
        p.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "canonicalize":
            print(wire.clean_spaces(args.baseline.read_bytes().decode("utf-8")))
            return 0
        result = {"init": init, "controls": controls, "freeze": freeze}[args.command](args)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "code": getattr(error, "code", "invalid_author_input"),
                          "detail": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
