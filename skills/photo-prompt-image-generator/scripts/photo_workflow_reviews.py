"""Bind agent pixel-review records without authoring their judgments."""
from pathlib import Path

from photo_workflow_state import WorkflowError, bound_path, commit_stage, digest, encode, locked_state, read_json, value
from photo_workflow_worker import audit_bound


def gates(result):
    rows = []
    for obligation in (result.get("effective_visual") or {}).get("obligations", []):
        rows.extend(obligation.get("render_gates", []))
    rows.extend((result.get("character") or {}).get("render_gates", []))
    rows.extend({"id": gate, "review_scale": "native", "criterion": "Agent-reviewed body actuation is visible in the actual result"}
                for gate in result.get("embodiment_gates", []))
    return rows


def validate_visual_scales(review, contracts):
    # Existing moe auditor checks schema, gates, evidence and image. This adds
    # the declared observation scale that newer visual obligations require.
    for gate in gates(contracts):
        needed = {"native", "thumbnail"} if gate.get("review_scale") == "both" else {gate.get("review_scale", "native")}
        scales = (review.get("hard_gates", {}).get(gate["id"], {})).get("reviewed_scales")
        if not isinstance(scales, list) or len(scales) != len(set(scales)) or set(scales) - {"native", "thumbnail"} or not needed <= set(scales):
            raise WorkflowError("required_review_scale_unobserved")


def review_shape(args):
    from photo_workflow import ensure, one
    with locked_state(args.run) as state:
        ensure(state)
        contracts = audit_bound(state, runtime=True)
        if contracts["composed_audit"]["status"] != "pass" or contracts["runtime_audit"]["status"] != "pass":
            raise WorkflowError("review_requires_audited_inputs")
        if args.image is None or not args.image.is_file():
            raise WorkflowError("concrete_review_image_required")
        image = str(args.image.resolve()); image_sha = digest(args.image.read_bytes())
        pack = one(value(state, "pack")); outputs = {}; available = []
        repair = contracts.get("repair")
        if repair:
            shape = {"schema_version": "photo-image-render-review/v1", "pack_id": pack["pack_id"],
                "source_render_repair_contract_sha256": repair["canonical_sha256"], "result": {"path": image, "sha256": image_sha},
                "reviewer": {"reviewer_id": None, "method": "direct_pixel_inspection"}, "gates": [
                    {"gate_id": gate["id"], "status": None, "reviewed_scales": [], "evidence": None,
                     "required_scales": ["native", "thumbnail"] if gate["review_scale"] == "both" else [gate["review_scale"]]}
                    for target in repair["targets"] for gate in target["render_gates"]]}
            # required_scales is instructions outside the review wire.
            instructions = {row["gate_id"]: row.pop("required_scales") for row in shape["gates"]}
            outputs["generic_review_shape"] = encode({"review": shape, "required_scales": instructions})
            available.append("generic")
        visual = gates(contracts)
        if visual:
            contract = (contracts.get("character") or contracts.get("effective_visual") or {"contract_version": "photo-embodiment-preflight/v1"})
            shape = {"schema_version": "moe-render-review/v1", "pack_id": pack["pack_id"],
                "contract_version": contract["contract_version"], "reviewer": None, "result_image": image, "result_sha256": image_sha,
                "hard_gates": {gate["id"]: {"status": None, "evidence": None, "reviewed_scales": []} for gate in visual},
                "user_judgment": {"baseline_available": None, "genuinely_moe": None, "better_than_baseline": None, "source": None, "evidence": None}}
            outputs["visual_review_shape"] = encode({"review": shape, "gate_definitions": visual})
            available.append("visual")
        commit_stage(args.run, state, state["phase"], outputs)
        return {"status": "pass", "available_reviews": available,
                "shapes": {k: state["artifacts"][k]["path"] for k in outputs}}


def review_audit(args):
    from photo_workflow import ensure
    with locked_state(args.run) as state:
        ensure(state)
        pending = dict(state, artifacts=dict(state["artifacts"]))
        outputs = {}
        for role in ("generic_review", "visual_review"):
            path = getattr(args, role)
            if path:
                raw = path.read_bytes()
                pending["artifacts"][role] = {"path": str(path.resolve()), "sha256": digest(raw)}
                outputs[role] = raw
        if not outputs:
            raise WorkflowError("authored_review_required")
        for role in outputs:
            review = read_json(bound_path(pending, role))
            raw_path = review.get("result", {}).get("path") if role == "generic_review" else review.get("result_image")
            expected_sha = review.get("result", {}).get("sha256") if role == "generic_review" else review.get("result_sha256")
            path = Path(raw_path) if isinstance(raw_path, str) else None
            if path is None: raise WorkflowError("concrete_review_image_required")
            path = path if path.is_absolute() else bound_path(pending, role).parent / path
            if not any(op.get("result_binding") == {"path": str(path.resolve()), "sha256": expected_sha} for op in state["operations"]):
                raise WorkflowError("review_result_not_bound_to_observed_attempt")
        contracts = audit_bound(pending, runtime=True, reviews=True)
        if contracts["composed_audit"]["status"] != "pass" or contracts["runtime_audit"]["status"] != "pass":
            raise WorkflowError("review_requires_audited_inputs")
        if contracts.get("repair") and "generic_review" not in pending["artifacts"]:
            raise WorkflowError("generic_review_required")
        if gates(contracts) and "visual_review" not in pending["artifacts"]:
            raise WorkflowError("effective_visual_review_required")
        audits = {}
        if "generic_review_audit" in contracts:
            audits["generic"] = contracts["generic_review_audit"]
            if audits["generic"]["status"] != "pass" or audits["generic"]["failures"]:
                raise WorkflowError("invalid_generic_review_record")
        if "visual_review_audit" in contracts:
            audits["visual"] = contracts["visual_review_audit"]
            if audits["visual"]["schema_failures"]:
                raise WorkflowError("invalid_visual_review_record")
            validate_visual_scales(read_json(bound_path(pending, "visual_review")), contracts)
        technical = all(a["technical_qualified"] for a in audits.values())
        outputs["review_audit"] = encode(audits)
        commit_stage(args.run, state, "review_record_validated", outputs, metadata={
            "technical_qualification": "pass" if technical else "fail",
            "user_judgment": audits.get("visual", {}).get("user_judgment")})
        return {"status": "pass", "record_valid": True, "technical_qualification": state["technical_qualification"],
                "user_judgment": state["user_judgment"]}
