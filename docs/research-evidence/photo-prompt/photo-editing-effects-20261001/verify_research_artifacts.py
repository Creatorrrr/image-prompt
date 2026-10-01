#!/usr/bin/env python3
"""Verify research artifacts and isolated draft contracts; never register runtime data."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
ASSETS = SCRIPTS.parent / "assets"
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as pg
import photo_candidate_semantics as semantics
from photo_contracts import property_effects_allowed


def read(name):
    return json.loads((OUT / name).read_text())


checks = []


def check(name, condition, detail):
    if not condition:
        raise ValueError(f"{name}: {detail}")
    checks.append({"check": name, "status": "PASS", "evidence": detail})


def rejects(name, callback):
    try:
        callback()
    except ValueError as exc:
        checks.append({"check": name, "status": "PASS", "evidence": str(exc)})
        return
    raise ValueError(f"{name}: malformed research projection was accepted")


reference = read("reference-keywords.json")
matrix = read("keyword-matrix.json")["rows"]
groups = read("concept-proposals.json")["groups"]
sources = read("source-ledger.json")["sources"]
snapshot = read("current-catalog-snapshot.json")
plan = read("validation-plan.json")
draft = read("runtime-projection-draft.json")
provenance = read("prototype-provenance.json")

check("complete_reference_row_mapping", len(reference["rows"]) == len(matrix) == 245
      and [row["reference_row"] for row in matrix] == list(range(1, 246)), "245/245 unique table rows")
assigned = [term for group in groups for term in group["reference_terms"]]
check("complete_distinct_group_assignments", len(groups) == 88 and len(assigned) == len(set(assigned)) == 245,
      "88 design families; preserve Soft light versus Soft Light as separate reference assignments")
source_ids = {row["id"] for row in sources}
group_ids = {row["id"] for row in groups}
check("source_reference_integrity", len(source_ids) == len(sources) == 54
      and all(set(row["source_ids"]) <= source_ids for row in groups + matrix), "54 unique source IDs; no dangling links")
check("prospective_case_integrity", len(plan["cases"]) == 42
      and len({row["id"] for row in plan["cases"]}) == 42
      and all(row["status"] == "planned_not_executed" and set(row["proposal_group_ids"]) <= group_ids for row in plan["cases"]),
      "42 prospective cases; no fabricated test or pixel PASS")
check("draft_provenance_hash", provenance["draft_sha256"] == hashlib.sha256((OUT / "runtime-projection-draft.json").read_bytes()).hexdigest(),
      "Draft content is hash-bound to research provenance")

data = pg.load_json(ASSETS / "photo_prompt_tags.json")
registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
profile_by_id = {row["id"]: row for row in registry["profiles"]}
reuse_ids = sorted({pid for group in groups for pid in group["reuse_profile_ids"]})
check("existing_profile_reuse_references", len(reuse_ids) == 17 and set(reuse_ids) <= set(profile_by_id),
      "17 reuse profile IDs exist in the current merged registry; activation/pixels are separate")
check("proposed_slot_and_dimension_references", all(set(row["target_slots"]) <= set(data["slots"])
      and set(row["affected_dimensions"]) <= pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS for row in groups),
      f"All proposed slots exist; use {len(pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)} existing core dimensions")
check("draft_not_registered", "photo_prompt_editing_effects_extension.json" not in pg.RESEARCH_EXTENSION_FILENAMES
      and not any((ASSETS / filename).exists() for filename in ["photo_prompt_editing_effects_extension.json", "photo_prompt_visual_obligations_editing_effects.json"]),
      "Research draft remains outside runtime loader registration")

before_candidates = sum(len(rows) for rows in data["slots"].values())
before_bundles = len(data.get("candidate_bundles", []))
merged = pg.merge_research_extension(copy.deepcopy(data), copy.deepcopy(draft))
semantics.validate_candidate_entries(merged, pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
semantics.validate_bundle_references(merged, registry["profiles"])
new_bundles = [row for row in merged["candidate_bundles"] if row["id"].startswith("edit_research_bundle_")]
check("in_memory_draft_merge", sum(len(rows) for rows in merged["slots"].values()) == before_candidates + 25
      and len(merged["candidate_bundles"]) == before_bundles + 6,
      "25 candidates / 6 bundles compile only in memory; production data unchanged")
check("bundle_profiles_remain_advisory", all(row["adoption"] == "optional"
      and row["profile_activation"] == "independent_request_evidence_only" for row in new_bundles),
      "Associated profile references do not become hard obligations")
check("one_evidence_unit_per_simultaneous_component", all(len(component["concept_units"]) == 1
      and component["minimum_realizations"] == 1 for row in new_bundles for component in row["components"]),
      "Every simultaneous duty gets its own component ID")

# Isolated declared-eligibility fixtures exercise the compiler/public surface.
# They are not actual ranked retrieval packs and do not establish exposure.
isolated = {"candidate_bundles": new_bundles, "candidate_semantic_policy": data["candidate_semantic_policy"]}
slots = {slot: {"candidates": [{"id": f"slot:{slot}:{row['id']}", "applicability": {"status": "eligible"}, "conflicts_with": []}
                              for row in entries]} for slot, entries in draft["slots"].items()}
pack = {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": sorted(pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)}},
        "provenance": {"seed": 101}}
mechanical_cases = []
for bundle in new_bundles:
    scoped_data = {**isolated, "candidate_bundles": [bundle]}
    available = semantics.public_bundles(scoped_data, pack)["candidates"]
    check("isolated_eligible_" + bundle["id"], len(available) == 1, "All declared members eligible and dimensions open")
    missing = copy.deepcopy(pack)
    member = bundle["member_candidates"][0]
    missing["slots"][member["slot"]]["candidates"] = [row for row in missing["slots"][member["slot"]]["candidates"] if row["id"] != member["id"]]
    check("isolated_missing_member_" + bundle["id"], not semantics.public_bundles(scoped_data, missing)["candidates"], "Missing member prevents bundle exposure")
    locked = copy.deepcopy(pack)
    dimension = member["affected_dimensions"][0]
    locked["authorial_core"]["intent_lock"]["open_dimensions"].remove(dimension)
    check("isolated_locked_dimension_" + bundle["id"], not semantics.public_bundles(scoped_data, locked)["candidates"], "Closed whole dimension prevents bundle exposure")
    mechanical_cases.append(bundle["id"])

partial_lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [
    {"dimension": "color", "target": "subject", "property": "wardrobe.color"}]}
chroma_entry = next(row for row in draft["slots"]["color_grading"] if row["id"].endswith("muted_chroma"))
check("isolated_property_helper_conservative_scope", not property_effects_allowed(partial_lock,
      chroma_entry["affected_dimensions"], chroma_entry["affected_properties"]),
      "Wildcard global color effect cannot claim compatibility with a wardrobe.color lock; general pack path not tested")

rejects("unsupported_extension_metadata_rejected", lambda: pg.merge_research_extension(copy.deepcopy(data),
        {"schema_version": pg.RESEARCH_EXTENSION_SCHEMA, "source_ledger": {}}))
bad_entry = {"slots": {"quality": [{"id": "bad_cycle", "canonical_concept_id": "bad_cycle"}]}}
rejects("canonical_cycle_rejected", lambda: semantics.validate_candidate_entries(bad_entry, pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS))
bad_bundle = copy.deepcopy(draft)
bad_bundle["visual_semantics"][0]["candidate_ids"][0] = "missing_research_member"
rejects("missing_bundle_reference_rejected", lambda: pg.merge_research_extension(copy.deepcopy(data), bad_bundle))

probe_specs = [
    ("highlight_rolloff_tone_response", "highlight-rolloff tone response", "single_effect"),
    ("highlight_rolloff_tone_response", "highlight-rolloff tone response with localized bloom around bright practical lights", "explicit_coexistence"),
    ("diffusion_filter_highlight_halation", "diffusion-filter highlight halation", "single_effect"),
    ("diffusion_filter_highlight_halation", "diffusion-filter highlight halation together with film halation at bright edges", "explicit_coexistence"),
    ("panning_subject_tracking_motion_relation", "panning subject tracking motion relation", "single_effect"),
    ("panning_subject_tracking_motion_relation", "panning subject tracking motion relation with rear-curtain flash", "explicit_coexistence"),
    ("film_halation_highlight_edge_relation", "film halation at bright edges with localized bloom", "explicit_coexistence"),
]
probes = []
for profile_id, context, intent in probe_specs:
    applicable, reason = pg.visual_profile_context_applicability(profile_by_id[profile_id], context,
                        has_authorial_core_context=True)
    probes.append({"profile_id": profile_id, "context_text": context, "declared_intent": intent,
                   "context_applicable": applicable, "reason": reason,
                   "probe_scope": "direct_context_helper_only_not_full_request_routing"})

unchanged = [row["path"] for row in snapshot["source_files"]
             if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]]
check("production_source_hashes_unchanged", len(unchanged) == len(snapshot["source_files"]),
      f"{len(unchanged)}/{len(snapshot['source_files'])} catalog/registry source files retain baseline SHA-256")
tracked_changes = subprocess.check_output(["git", "diff", "--name-only", "HEAD", "--", "skills/photo-prompt-image-generator", "tests"], cwd=ROOT, text=True).splitlines()
check("no_tracked_runtime_or_test_changes", not tracked_changes, "No tracked skill assets/scripts/tests changed")

reuse_details = [{"id": pid, "requires_adult_character": profile_by_id[pid].get("activation", {}).get("requires_adult_character"),
                  "exclude_if_any_terms": profile_by_id[pid].get("activation", {}).get("exclude_if_any_terms", []),
                  "render_gate_count": len(profile_by_id[pid].get("render_gates", []))} for pid in reuse_ids]
result = {
    "schema_version": "photo-editing-research-verification/v1", "date": "2026-10-01",
    "research_artifact_and_isolated_structure_status": "PASS",
    "checks": checks,
    "source_verification_status_counts": dict(Counter(row["verification_status"] for row in sources)),
    "reuse_profiles": reuse_details,
    "existing_profile_context_probes": probes,
    "findings_requiring_implementation_review": [
        {"kind": "coexistence_lexical_veto", "scope": "direct_context_helper", "blocked_cases": [row for row in probes if row["declared_intent"] == "explicit_coexistence" and not row["context_applicable"]]},
        {"kind": "partial_property_path_not_qualified", "scope": "ordinary_candidates_and_bundles", "note": "The helper exists and conservative declarations work in isolation. public_bundles does not directly evaluate affected_properties; end-to-end propagation/audit must be verified."},
    ],
    "qualification_boundaries": {
        "production_runtime_registered": False, "real_request_retrieval_pack_tested": False,
        "actual_candidate_selection_tested": False, "final_prompt_audit_tested": False,
        "implementation_test_suites_run": False, "native_images_generated": 0,
        "native_pixel_qualification": "not_tested", "user_acceptance": "pending",
    },
}
(OUT / "research-validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"artifact_checks": len(checks), "status": "PASS",
                  "context_probe_count": len(probes), "coexistence_cases_blocked_in_helper": sum(row['declared_intent'] == 'explicit_coexistence' and not row['context_applicable'] for row in probes),
                  "production_source_hashes_unchanged": len(unchanged), "native_images_generated": 0}, ensure_ascii=False))
