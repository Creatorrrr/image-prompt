"""Compile and validate research proposals; never export or mutate runtime data.

Run from the repository root with .venv/bin/python. This script does not rebuild
indexes, build a candidate pack, call an image API, or execute proposed regressions.
"""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg


def read(name):
    with (OUT / name).open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="|"))
    assert rows and all(None not in row and None not in row.values() for row in rows), name
    return rows


def split(value, delimiter=","):
    return [item.strip() for item in value.split(delimiter) if item.strip()]


def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def unique(rows):
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    return set(ids)


inventory = json.loads((OUT / "TERM-INVENTORY.json").read_text())
audit = json.loads((OUT / "CURRENT-DATA-AUDIT.json").read_text())
registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
corpus = pg.load_json(SKILL / "assets/photo_prompt_tags.json")
owners = {}
for path in [SKILL / "assets/photo_prompt_visual_obligations.json", *[
    SKILL / "assets" / name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES
]]:
    for profile in json.loads(path.read_text()).get("profiles", []):
        owners[profile["id"]] = str(path.relative_to(ROOT))
assert len(owners) == len(registry["profiles"])
candidate_ids = {
    slot: {entry["id"] for entry in entries}
    for slot, entries in corpus["slots"].items()
}
all_candidate_ids = set().union(*candidate_ids.values())
slot_dimensions = corpus["candidate_semantic_policy"]["slot_dimensions"]

sources = read("SOURCE-SPECS.psv")
source_ids = unique(sources)
for row in sources:
    assert row["url"].startswith("https://"), row
    row["retrieved_on"] = "2026-10-03"
    row["evidence_scope"] = "Only the recorded entry or extract; not every lemma in an expression group."
    row["not_proof_of"] = ["universal usage", "candidate eligibility", "pixel realization", "user acceptance"]
write("SOURCES.json", {"schema_version": "neutral-expression-sources/v1", "sources": sources})
lines = ["# 확인한 외부 자료", "", "2026-10-03 접근 기록. 정의의 어휘 범위와 추출 방식은 자료마다 다릅니다. 검색 발췌·접근 제한 자료를 전체 본문 검증으로 계산하지 않습니다.", "",
         "| ID | 자료 | 접근 근거 | 사용하는 범위 | 한계 |", "| --- | --- | --- | --- | --- |"]
for row in sources:
    lines.append(f"| {row['id']} | [{row['title']}]({row['url']}) | {row['access']} | {row['supports']} | {row['limits']} |")
(OUT / "SOURCES.md").write_text("\n".join(lines) + "\n")

units = read("SEMANTIC-UNIT-SPECS.psv")
contexts = read("CONTEXT-UNIT-SPECS.psv")
unit_ids = unique(units)
context_ids = unique(contexts)
for row in units:
    row["owners"] = split(row["owners"])
    row["candidate_reuse"] = split(row["candidate_reuse"])
    row["sources"] = split(row["sources"])
    assert set(row["owners"]) <= owners.keys(), row
    assert set(row["candidate_reuse"]) <= all_candidate_ids, row
    assert set(row["sources"]) <= source_ids, row
    row["owner_references"] = [{"profile_id": owner, "path": owners[owner],
        "scope": "related contract for comparison" if row["id"] == "U29" else "reuse or scope review; not lexical equivalence"}
        for owner in row["owners"]]
    row["components"] = split(row["components"], ";")
    row["confounders"] = split(row["confounders"], ";")
    row["visual_gate_status"] = "proposed_not_pixel_qualified"
    row["operational_definition_status"] = "research_author_proposal_not_external_source_fact"
    row["runtime_export_allowed"] = False
    row["exact_alias_promotion_allowed"] = False
    row["partial_is_fail"] = True
for row in contexts:
    row["runtime_export_allowed"] = False
    row["hard_activation_allowed"] = False
    row["storage_plan"] = "Review existing contextual_usage, claim_limits and core contracts; no new production meaning store."
write("SEMANTIC-UNITS.json", {"schema_version": "neutral-expression-semantic-proposal/v1",
    "status": "research_only", "units": units, "contexts": contexts})

specs = read("TERM-DECISION-SPECS.psv")
expanded = {}
for spec in specs:
    for item in split(spec["ids"]):
        match = re.fullmatch(r"NE(\d{3})-(\d{3})", item)
        ids = [f"NE{n:03d}" for n in range(int(match[1]), int(match[2]) + 1)] if match else [item]
        for term_id in ids:
            assert term_id not in expanded, term_id
            expanded[term_id] = spec
assert set(expanded) == {term["id"] for term in inventory["terms"]}
decisions = []
for term in inventory["terms"]:
    spec = expanded[term["id"]]
    mapped = split(spec["units"])
    evidence_ids = split(spec["lexical_sources"])
    assert set(mapped) <= unit_ids | context_ids, spec
    assert set(evidence_ids) <= source_ids, spec
    scope = ("no_external_source_attached_lexical_verification_pending" if not evidence_ids else
             "form_basis_not_lexical_alias_verification" if "form_basis" in spec["decision"] else
             "analytic_concept_support_not_lexical_verification" if spec["kind"] == "objectification_analysis" else
             "source_entry_attached_group_scope_review_required")
    decisions.append({"id": term["id"], "expression_group": term["expression_group"],
        "row_kind": term["row_kind"], "domain": term["domain"],
        "source_turn_id": term["source_turn_id"], "source_line": term["source_line"],
        "semantic_kind": spec["kind"], "proposed_units": mapped,
        "external_evidence_ids": evidence_ids, "external_evidence_scope": scope,
        "decision": spec["decision"], "preserve": spec["preserve"],
        "do_not_add": spec["do_not_add"], "runtime_export_allowed": False,
        "full_expression_group_verified": False,
        "pending_review": "Verify each lemma and context before any exact alias; inspect existing owner contract, frozen core and candidate effects."})
write("TERM-DECISIONS.json", {"schema_version": "neutral-expression-term-decisions/v1",
    "status": "research_triage_not_activation_map", "decisions": decisions})

properties_dimension = {
    "invitation_action": "action", "offering_withdrawal_action": "action",
    "body_orientation": "pose", "hand_pose": "pose", "target_relation": "relationship",
    "restraint_material": "appearance", "restraint_attachment": "appearance",
    "limb_position": "pose", "movement_constraint": "action",
    "contact_pose": "pose", "current_surface_deformation": "body_geometry",
    "compression_relief": "appearance", "care_handoff_action": "action",
    "recipient_relation": "relationship",
}
candidates = read("CANDIDATE-SPECS.psv")
unique(candidates)
for row in candidates:
    row["units"] = split(row["units"])
    row["existing_candidate_ids"] = split(row["existing_candidate_ids"])
    row["affected_dimensions"] = split(row["affected_dimensions"])
    props = split(row["affected_properties"])
    assert set(row["units"]) <= unit_ids, row
    assert row["slot"] in corpus["slots"], row
    assert set(row["existing_candidate_ids"]) <= candidate_ids[row["slot"]], row
    row["affected_properties"] = [{"dimension": properties_dimension.get(prop, row["affected_dimensions"][0]),
        "property": prop, "target": "$core.bound_owner_id"} for prop in props]
    assert set(p["dimension"] for p in row["affected_properties"]) == set(row["affected_dimensions"]), row
    row["current_slot_dimensions"] = slot_dimensions.get(row["slot"], [])
    row["dimensions_not_owned_by_current_slot"] = sorted(set(row["affected_dimensions"]) - set(row["current_slot_dimensions"]))
    if row["dimensions_not_owned_by_current_slot"]:
        assert row["readiness"] == "hold_cross_dimension_slot_policy", row
    row["source_ids"] = sorted({source for unit in units if unit["id"] in row["units"] for source in unit["sources"]})
    row["binding_status"] = "unbound_placeholder_not_eligible"
    row["required_core_bindings"] = ["owner_id", "requested_property_scope", "relevant_objects_and_targets", "already_allowed_visibility"]
    row["property_names_status"] = "research_proposed_names_must_map_to_runtime_property_inventory"
    row["positive_index_fields_proposed"] = ["definition"]
    row["excluded_positive_index_fields"] = ["contrast", "evidence_gate", "source_ids", "readiness", "category_ids"]
    row["runtime_export_allowed"] = False
    row["test_status"] = "proposed_not_pack_or_pixel_tested"
write("CANDIDATE-DRAFTS.json", {"schema_version": "neutral-expression-candidate-drafts/v1",
    "status": "research_only_not_runtime_schema", "candidates": candidates})

regressions = read("REGRESSION-SPECS.psv")
unique(regressions)
for row in regressions:
    row["units"] = split(row["units"])
    assert set(row["units"]) <= unit_ids | context_ids, row
    row["execution_status"] = "PROPOSED_NOT_RUN"
    row["specification_type"] = "policy_acceptance_case_requires_full_fixture"
write("REGRESSION-PROPOSALS.json", {"schema_version": "neutral-expression-regression-proposals/v1", "cases": regressions})

changed_sources = []
for source in audit["source_files"]:
    path = ROOT / source["path"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    if actual != source["sha256"]:
        changed_sources.append({"path": source["path"], "before": source["sha256"], "after": actual})
for path in OUT.glob("*.psv"):
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        assert line == line.rstrip(), (path.name, line_number, "trailing whitespace")

report = {
    "schema_version": "neutral-expression-package-validation/v1",
    "checked_on": "2026-10-03", "structural_status": "PASS",
    "input_snapshot_status": "UNCHANGED" if not changed_sources else "INPUT_DRIFT_REVIEW_REQUIRED",
    "status": "PASS" if not changed_sources else "INPUT_DRIFT_REVIEW_REQUIRED",
    "counts": {"keyword_groups": sum(d["row_kind"] == "keyword_group" for d in decisions),
        "authoring_examples": sum(d["row_kind"] == "authoring_example" for d in decisions),
        "term_decisions": len(decisions), "external_sources": len(sources), "observable_relation_units": len(units),
        "context_units": len(contexts), "candidate_drafts": len(candidates),
        "cross_dimension_holds": sum(bool(c["dimensions_not_owned_by_current_slot"]) for c in candidates),
        "regression_proposals": len(regressions), "exact_only_diagnostics_executed": 12,
        "referenced_existing_profiles": len({owner for unit in units for owner in unit["owners"]}),
        "units_with_existing_profile_references": sum(bool(unit["owners"]) for unit in units),
        "protected_source_files": len(audit["source_files"])},
    "keyword_evidence_scopes": dict(Counter(d["external_evidence_scope"] for d in decisions if d["row_kind"] == "keyword_group")),
    "candidate_readiness": dict(Counter(c["readiness"] for c in candidates)),
    "checks": ["Every extracted row has exactly one decision", "All source and unit references resolve",
        "All named existing profile ids exist in the live merged registry",
        "All named reused candidate ids exist in the declared live slot",
        "All property effects have a dimension and an explicitly unbound target",
        "Every cross-slot-dimension proposal is held", "All proposals are non-exportable",
        "All planned regressions remain PROPOSED_NOT_RUN", "Input file hashes compared after research compilation"],
    "protected_source_changes": changed_sources,
    "limits": ["PASS validates the research package structure and current references only.",
        "It does not qualify lexical equivalence, new aliases, production core behavior, candidate packs or images.",
        "Named properties and target placeholders are proposals, not a directly importable runtime schema."]}
write("VALIDATION.json", report)
print(json.dumps(report, ensure_ascii=False, indent=2))
