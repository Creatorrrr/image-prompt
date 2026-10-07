"""Closed retry projection. No candidate inventories or broad parent prompt view."""
from __future__ import annotations
import copy
import re
from photo_precore_bridge import load
from photo_workflow_state import WorkflowError, digest, encode

contracts = load("photo_authoring_contracts")
wire = load("photo_authoring_wire")
FAILURE_CLASSES = {"meaning_rebuild", "agent_spatial_inconsistency", "pixel_realization_mismatch", "unobservable_required_scale",
    "transient_http", "provider_blocked", "persistence_failed", "recorder_failed", "execution_unknown", "invalid_review_record", "artistic_revision"}
DECISION_FIELDS = {"schema_version", "current_source_span_ids", "source_text", "preserved_dimensions", "allowed_changes",
    "requester_corrected_dimensions", "allowed_properties", "local_axes", "failed_gate_ids", "failure_class",
    "additional_invocation_limit", "obligation_dimensions"}


def unique_strings(items, *, allow_empty=True):
    if not isinstance(items, list) or len(items) > 64 or not allow_empty and not items:
        raise WorkflowError("invalid_scope_shape")
    if any(not isinstance(s, str) or not s.strip() or len(s) > 2048 for s in items) or len(items) != len(set(items)):
        raise WorkflowError("invalid_scope_shape")
    return set(items)


def bounded(value, depth=0):
    if depth > 8:
        raise WorkflowError("projection_scope_unresolved")
    if isinstance(value, str):
        if len(value) > 4096: raise WorkflowError("projection_scope_unresolved")
    elif isinstance(value, list):
        if len(value) > 128: raise WorkflowError("projection_scope_unresolved")
        for row in value: bounded(row, depth + 1)
    elif isinstance(value, dict):
        if len(value) > 128: raise WorkflowError("projection_scope_unresolved")
        for key, row in value.items():
            if not isinstance(key, str): raise WorkflowError("projection_scope_unresolved")
            bounded(row, depth + 1)
    elif value is not None and type(value) not in (int, float, bool):
        raise WorkflowError("projection_scope_unresolved")
    return copy.deepcopy(value)


def select(row, fields):
    if not isinstance(row, dict): raise WorkflowError("projection_scope_unresolved")
    return {k: bounded(row[k]) for k in fields if k in row}


def evidence_requirements(row):
    allowed = {"min_content_words", "must_mention_any", "must_not_contain"}
    result = {}
    for field, requirement in row.items():
        if not isinstance(requirement, dict) or set(requirement) - allowed:
            raise WorkflowError("unsupported_obligation_projection_shape")
        for key, value in requirement.items():
            if key == "min_content_words":
                if type(value) is not int or value < 1: raise WorkflowError("unsupported_obligation_projection_shape")
            elif not isinstance(value, list) or any(not isinstance(v, str) for v in value):
                raise WorkflowError("unsupported_obligation_projection_shape")
        result[field] = bounded(requirement)
    return result


def visual_obligation(row):
    result = select(row, {"id", "composition_instruction", "reject_substitutes", "bindings"})
    component = row.get("component_semantics", {})
    if component:
        expected = {"minimum_component_groups", "required_group_ids", "groups"}
        if set(component) - expected or not isinstance(component.get("groups"), list):
            raise WorkflowError("unsupported_obligation_projection_shape")
        result["component_semantics"] = select(component, {"minimum_component_groups", "required_group_ids"})
        result["component_semantics"]["groups"] = []
        for group in component["groups"]:
            if not isinstance(group, dict) or set(group) != {"id", "any_terms"}:
                raise WorkflowError("unsupported_obligation_projection_shape")
            result["component_semantics"]["groups"].append(select(group, {"id", "any_terms"}))
    else:
        result["component_semantics"] = {}
    result["prompt_binding"] = select(row.get("prompt_binding", {}), {"composed_field", "required_evidence_fields",
        "minimum_distinct_evidence_phrases", "prompt_evidence_must_be_literal", "maximum_pairwise_content_token_overlap_ratio", "forbidden_filler_phrases"})
    result["evidence_requirements"] = evidence_requirements(row.get("evidence_requirements", {}))
    result["render_gates"] = [select(g, {"id", "review_scale", "criterion", "description"}) for g in row.get("render_gates", [])]
    if row.get("visual_relation"):
        # Unsupported relations stop explicitly rather than losing an endpoint.
        relation = row["visual_relation"]
        allowed = {"schema_version", "status", "owner_axis", "entities", "visible_regions", "relations", "observable_effects", "confusion_negatives", "observability", "hard_binding", "invariant_fields", "flexible_fields"}
        if set(relation) - allowed - {"source", "activation"}:
            raise WorkflowError("projection_scope_unresolved")
        result["visual_relation"] = select(relation, allowed - {"observability", "hard_binding", "invariant_fields", "flexible_fields"})
        if "observability" in relation:
            expected = {"required_visible_regions", "minimum_review_scale", "crop_policy", "occlusion_policy", "proof_budget", "ineligible_state"}
            if set(relation["observability"]) - expected: raise WorkflowError("projection_scope_unresolved")
            result["visual_relation"]["observability"] = select(relation["observability"], expected)
        if "proof_budget" in relation.get("observability", {}) and set(relation["observability"]["proof_budget"]) - {"thumbnail", "native"}:
            raise WorkflowError("unsupported_obligation_projection_shape")
        if "hard_binding" in relation:
            # Unknown future binding structures are never exposed or clipped.
            raise WorkflowError("unsupported_obligation_projection_shape")
    return result


def overlaps(left, right):
    return left == "*" or right == "*" or left == right or left.startswith(right + ".") or right.startswith(left + ".")


def project(parent, current_envelope, decision, source_artifacts):
    envelope = wire.normalize_request_envelope(current_envelope)
    if not isinstance(decision, dict) or set(decision) != DECISION_FIELDS or decision["schema_version"] != "photo-repair-decision/v1":
        raise WorkflowError("invalid_repair_decision")
    current_ids = unique_strings(decision["current_source_span_ids"], allow_empty=False)
    spans = {s["span_id"]: s["text"] for s in envelope["active_spans"]}
    if not current_ids <= spans.keys() or not isinstance(decision["source_text"], str) or not decision["source_text"].strip() or not any(decision["source_text"] in spans[s] for s in current_ids):
        raise WorkflowError("current_request_evidence_required")
    core, pack, attempt, audit = (parent[k] for k in ("core", "pack", "attempt", "audit"))
    lock = core["intent_lock"]
    preserved = unique_strings(decision["preserved_dimensions"])
    changed = unique_strings(decision["allowed_changes"])
    corrected = unique_strings(decision["requester_corrected_dimensions"])
    if not preserved | changed <= contracts.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS or preserved & changed or not corrected <= changed:
        raise WorkflowError("invalid_dimension_scope")
    if not set(lock["locked_dimensions"]) <= preserved | corrected or not changed <= set(lock["open_dimensions"]) | corrected:
        raise WorkflowError("parent_lock_scope_conflict")
    failure_class = decision["failure_class"]
    if failure_class not in FAILURE_CLASSES:
        raise WorkflowError("invalid_failure_class")
    if corrected and failure_class != "meaning_rebuild":
        raise WorkflowError("requester_correction_requires_meaning_rebuild")
    local = unique_strings(decision["local_axes"])
    if not local <= contracts.RENDER_REPAIR_ALLOWED_AXES:
        raise WorkflowError("invalid_local_axis")
    for axis, dimension in contracts.RENDER_REPAIR_DIMENSION_AXES.items():
        if axis in local and dimension not in changed:
            raise WorkflowError("local_axis_outside_allowed_changes")
    failed = unique_strings(decision["failed_gate_ids"])
    actual_failed = set(parent["failed_gate_ids"])
    if not failed <= actual_failed or failure_class in {"pixel_realization_mismatch", "unobservable_required_scale"} and not failed:
        raise WorkflowError("failed_gate_scope_conflict")
    if failure_class == "artistic_revision" and failed:
        raise WorkflowError("artistic_revision_cannot_invent_failed_gate")
    limit = decision["additional_invocation_limit"]
    if type(limit) is not int or not 0 <= limit <= 64:
        raise WorkflowError("invalid_retry_budget")
    if failure_class in {"provider_blocked", "persistence_failed", "recorder_failed", "execution_unknown", "invalid_review_record"}:
        if local or changed or limit:
            raise WorkflowError("failure_route_cannot_rerender")
    repair = audit.get("repair")
    if repair:
        limit = min(limit, repair["retry_policy"]["maximum_additional_attempts"])
    properties = decision["allowed_properties"]
    if not isinstance(properties, list) or len(properties) > 64:
        raise WorkflowError("invalid_property_scope")
    for row in properties:
        if not isinstance(row, dict) or set(row) != {"dimension", "target", "property"} or row["dimension"] not in changed or any(
            not isinstance(row[k], str) or not re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*", row[k]) for k in ("target", "property")):
            raise WorkflowError("invalid_property_scope")
    property_locks = [a for a in lock["semantic_anchors"] if "property" in a and a["dimension"] not in corrected]
    for effect in properties:
        if any(overlaps(effect["target"], anchor["target"]) and overlaps(effect["property"], anchor["property"]) for anchor in property_locks):
            raise WorkflowError("locked_property_overlap")
    if property_locks and local - set(contracts.RENDER_REPAIR_DIMENSION_AXES) and not properties:
        raise WorkflowError("projection_scope_unresolved")
    fields, assertions = [], []
    def record(role, pointer, data, scope=None):
        out = {"value": data, "source_role": role, "source_pointer": pointer, "source_sha256": source_artifacts[role]["sha256"]}
        if scope is not None: out["scope"] = scope
        return out
    for index, anchor in enumerate(lock["semantic_anchors"]):
        if anchor["dimension"] in preserved or anchor in property_locks:
            fields.append(record("authorial_core_normalized", f"/intent_lock/semantic_anchors/{index}",
                select(anchor, {"prompt_evidence"}), select(anchor, {"dimension", "target", "property"})))
    for index, assertion in enumerate(core.get("semantic_assertions", [])):
        if assertion["polarity"] != "required" or not set(assertion["affected_dimensions"]) & preserved:
            continue
        if not set(assertion["affected_dimensions"]) <= preserved:
            raise WorkflowError("projection_scope_unresolved")
        assertions.append(record("authorial_core_normalized", f"/semantic_assertions/{index}",
            select(assertion, {"dimension", "polarity", "affected_dimensions", "axes", "evidence", "relations"})))
    obligations, relations, target_axes = [], [], set()
    hard_gates = set()
    for index, target in enumerate((repair or {}).get("targets", [])):
        gate_ids = {g["id"] for g in target["render_gates"]}
        hard_gates |= gate_ids
        if set(target["protected_dimensions"]) & preserved or gate_ids & failed:
            if not set(target["protected_dimensions"]) <= preserved:
                raise WorkflowError("projection_scope_unresolved")
            if gate_ids & failed: target_axes |= set(target["allowed_repair_axes"])
            relations.append(record("pack", f"/render_repair/targets/{index}", select(target, {
                "importance", "relation_origin", "actor_phrase", "object_phrase", "interaction_state", "actor_object_contact",
                "protected_dimensions", "frozen_evidence", "prompt_binding"})))
            obligations.append(record("pack", f"/render_repair/targets/{index}/render_gates",
                [select(g, {"id", "review_scale", "criterion", "description"}) for g in target["render_gates"]]))
    if local and failed and repair and any(g.startswith("rr_") for g in failed) and not local <= target_axes:
        raise WorkflowError("local_axis_outside_failed_target")
    mappings = decision["obligation_dimensions"]
    effective = audit.get("effective_visual") or {}
    if not isinstance(mappings, dict) or set(mappings) != {row["id"] for row in effective.get("obligations", [])}:
        raise WorkflowError("obligation_scope_declaration_required")
    for index, row in enumerate(effective.get("obligations", [])):
        dimensions = unique_strings(mappings[row["id"]], allow_empty=False)
        hard_gates |= {g["id"] for g in row["render_gates"]}
        if not dimensions <= preserved:
            raise WorkflowError("projection_scope_unresolved")
        obligations.append(record("effective_visual", f"/obligations/{index}", visual_obligation(row), {"dimensions": sorted(dimensions)}))
    hard_gates |= set(audit.get("character_gates", [])) | set(audit.get("embodiment_gates", []))
    if audit.get("character"):
        if "character_response" not in preserved:
            raise WorkflowError("projection_scope_unresolved")
        obligations.append(record("pack", "/character_response/render_gates", [select(g, {"id", "evidence_field", "criterion"}) for g in audit["character"]["render_gates"]]))
    if audit.get("embodiment_gates"):
        obligations.append(record("pack", "/embodiment_preflight/required_checks", list(audit["embodiment_gates"])))
    if not failed <= hard_gates:
        raise WorkflowError("unknown_failed_gate")
    defects = []
    for role, review in parent["reviews"].items():
        rows = review.get("gates", []) if role == "generic_review" else [{"gate_id": key, **row} for key, row in review.get("hard_gates", {}).items()]
        for index, row in enumerate(rows):
            if row.get("gate_id") in failed:
                pointer = f"/gates/{index}" if role == "generic_review" else "/hard_gates/" + row["gate_id"].replace("~", "~0").replace("/", "~1")
                defects.append(record(role, pointer, select(row, {"gate_id", "status", "evidence", "reviewed_scales"})))
    error = attempt.get("error_details") or {}
    if failure_class == "transient_http" and error.get("http_status") not in {429, 500, 502, 503, 504}:
        raise WorkflowError("observed_transient_code_required")
    if failure_class == "provider_blocked" and attempt.get("status") != "safety_block":
        raise WorkflowError("observed_provider_block_required")
    # Never expose arbitrary provider text/codes, which may contain raw input.
    if error:
        defects.append(record("attempt", "/error_details", {"http_status": error.get("http_status"),
            "observed_outcome": "provider_blocked" if attempt.get("status") == "safety_block" else "unclassified_error"}))
    context = {"schema_version": "photo-retry-context/v1", "parent_binding": {
        "request_id": core["request_binding"]["request_id"], "request_sha256": core["request_binding"]["request_sha256"],
        "core_sha256": core["canonical_sha256"], "intent_lock_sha256": lock["canonical_sha256"], "pack_id": pack["pack_id"],
        "ledger_run_id": attempt["run_id"], "generation_id": parent["receipt"]["generation_id"], "receipt_sha256": parent["receipt"]["canonical_sha256"],
        "image_sha256": parent.get("image_sha256")},
        "source_artifacts": [{"role": role, "sha256": row["sha256"]} for role, row in sorted(source_artifacts.items())],
        "preserved_fields": fields, "required_assertions": assertions, "required_relations": relations, "effective_obligations": obligations,
        "reported_defects": defects, "allowed_scope": {"dimensions": sorted(changed), "properties": bounded(properties), "local_axes": sorted(local)},
        "preserved_dimensions": sorted(preserved), "repair_route": failure_class,
        "lineage_status": "representable" if preserved and changed else "scope_not_representable_in_lineage_v2",
        "decision_binding": {"sha256": source_artifacts["decision"]["sha256"], "current_source_span_ids": sorted(current_ids),
                             "current_envelope_sha256": envelope["canonical_sha256"]},
        "execution_scope": {"additional_invocation_limit": limit, "references": [select(r, {"role", "sha256"}) for r in parent["runtime"]["references"]],
                            "preserved_controls": {name: select(row, {"value"}) for name, row in parent["controls"]["controls"].items()}}}
    # Canonical digest is over the closed payload; byte hash remains separate.
    context["projection_sha256"] = contracts.canonical_json_sha256(context)
    return context
