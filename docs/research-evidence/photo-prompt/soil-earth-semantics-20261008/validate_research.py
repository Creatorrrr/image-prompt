"""Validate only the research package and current pure source contracts."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
from photo_candidate_semantics import validate_candidate_entries, validate_relations
from visual_profile_contracts import compile_visual_profile, validate_visual_profile_source, validate_hard_activation
from photo_contracts import INTENT_LOCK_DIMENSIONS, property_effects_allowed


def read(name):
    return json.loads((OUT / name).read_text())


def main():
    errors = []
    units = read("research-units.json")["units"]
    sources = read("sources.json")["sources"]
    candidates = read("candidate-proposals.json")["proposals"]
    profiles = read("visual-profile-proposals.json")["proposals"]
    routing = read("keyword-routing.json")["routing"]
    case_plan = read("validation-case-plan.json")
    unit_ids = {u["id"] for u in units}
    source_ids = {s["id"] for s in sources}
    if len(unit_ids) != len(units):
        errors.append("duplicate research unit ID")
    if len(source_ids) != len(sources):
        errors.append("duplicate source ID")
    for unit in units:
        if not set(unit["source_ids"]) <= source_ids:
            errors.append("broken source link: " + unit["id"])
        if not unit["confusion_boundary_ko"] or not unit["capture_policy"]:
            errors.append("missing boundary/capture policy: " + unit["id"])
        if any(not c["owner"] or not c["visible_phrase_en"] for c in unit["components"]):
            errors.append("unowned observation: " + unit["id"])
        validate_relations(unit["relations"], unit["id"])
    original_rows = sum(len(g["terms"]) for g in read("original-keywords.json")["groups"])
    if len(routing) != original_rows or any(not set(r["research_unit_ids"]) <= unit_ids or not r["research_unit_ids"] for r in routing):
        errors.append("original-term routing is incomplete")
    if len({r["term_id"] for r in routing}) != len(routing):
        errors.append("duplicate original term routing ID")
    slots = {}
    by_candidate = {}
    for proposal in candidates:
        candidate = proposal["candidate_draft"]
        by_candidate[proposal["research_unit_id"]] = candidate
        slots.setdefault(proposal["suggested_slot"], []).append(candidate)
        if proposal["research_unit_id"] not in unit_ids:
            errors.append("broken candidate research link")
    validate_candidate_entries({"slots": slots}, set(INTENT_LOCK_DIMENSIONS))
    compiler_gates = 0
    for proposal in profiles:
        profile = proposal["profile_draft"]
        validate_visual_profile_source(profile)
        validate_hard_activation(profile["activation"]["hard_activation"])
        compiled = compile_visual_profile(profile)
        compiler_gates += len(compiled["render_gates"])
        if len(compiled["render_gates"]) != len(profile["authored_components"]["components"]):
            errors.append("compiler dropped an authored duty: " + profile["id"])
    # Meaningful static lock checks for these proposed effects, not end-to-end
    # activation checks. They verify that declared effects cannot evade locks.
    lock_checks = []
    for uid, dim, target, prop, expected in [
        ("E010", "pose", "main_subject", "foot", False),
        ("E109", "appearance", "main_subject", "skin", False),
        ("E110", "appearance", "main_subject", "wardrobe", False),
        ("E110", "appearance", "main_subject", "wardrobe.optical_transmission", True),
        ("E108", "concept", "selected_terrain", "fictional_physics", False),
    ]:
        c = by_candidate[uid]
        lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [
            {"dimension": dim, "target": target, "property": prop}]}
        result = property_effects_allowed(lock, c["affected_dimensions"], c["affected_properties"])
        lock_checks.append({"unit": uid, "lock": lock, "expected": expected, "actual": result})
        if result != expected:
            errors.append("property lock mismatch: " + uid)
    for case in case_plan["regression_cases"] + case_plan["render_scenario_families"]:
        if not set(case["research_unit_ids"]) <= unit_ids:
            errors.append("broken case link: " + case["id"])
    # Assert identity existence against the saved working-source inventory.
    inventory = read("existing-inventory.json")
    actual_refs = set()
    for file in inventory["files"]:
        data = json.loads((ROOT / file["path"]).read_text())
        for slot, rows in data.get("slots", {}).items():
            actual_refs.update("slot:" + slot + ":" + row["id"] for row in rows)
        actual_refs.update("profile:" + row["id"] for row in data.get("profiles", []))
    reused = [ref for row in read("reuse-plan.json")["reuse"] for ref in row["existing_refs"]]
    for ref in reused:
        if ref not in actual_refs:
            errors.append("reuse identity missing: " + ref)
    # Record baseline file preservation. This does not attribute other agents'
    # changes and does not claim to hash all ignored/untracked material.
    before = read("workspace-before.json")
    changed = [p for p, record in before["protected_files"].items()
               if not (ROOT / p).is_file()
               or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != record["sha256"]]
    inventory_drift = [f["path"] for f in inventory["files"]
                       if hashlib.sha256((ROOT / f["path"]).read_bytes()).hexdigest() != f["sha256"]]
    summary = {
        "status": "pass" if not errors else "fail",
        "errors": errors, "research_units": len(units), "source_records": len(sources),
        "owned_observation_proposals": sum(len(u["components"]) for u in units),
        "candidate_drafts_contract_checked": len(candidates),
        "visual_profile_drafts_compiler_checked": len(profiles),
        "compiled_draft_gate_count": compiler_gates,
        "planned_regression_cases": len(case_plan["regression_cases"]),
        "planned_render_scenario_families": len(case_plan["render_scenario_families"]),
        "property_lock_contract_checks": lock_checks,
        "reuse_references_checked": len(reused),
        "protected_file_count": len(before["protected_files"]),
        "protected_files_changed_since_baseline": changed,
        "working_source_inventory_drift": inventory_drift,
        "preservation_status": "baseline_drift_observed" if changed else "baseline_hashes_identical",
        "preservation_boundary": "Status pass refers to the research contracts. Baseline drift is recorded separately and does not attribute changes. This research's authored writes are confined to its new evidence directory.",
        "representation_modes": dict(Counter(u["representation_mode"] for u in units)),
        "source_evidence_statuses": dict(Counter(s["evidence_status"] for s in sources)),
        "proof_boundary": "Research referential integrity, pure source contracts and current file hashes only. No published runtime, resolver search accuracy, candidate adoption, prompt audit, image rendering, pixels or user acceptance tested.",
    }
    (OUT / "research-validation.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
