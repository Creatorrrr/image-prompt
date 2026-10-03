"""Validate research against its saved live snapshot; report current drift separately."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
errors = []
checks = []

def load(name):
    return json.loads((OUT / name).read_text())

def require(condition, name):
    checks.append({"check": name, "passed": bool(condition)})
    if not condition:
        errors.append(name)

inventory = load("TERM-INVENTORY.json")
decisions = load("TERM-DECISIONS.json")
sources = load("SOURCES.json")["sources"]
units = load("SEMANTIC-UNITS.json")["units"]
drafts = load("CANDIDATE-DRAFTS.json")["drafts"]
cases = load("REGRESSION-PROPOSALS.json")["cases"]
backlog = load("LEXICAL-BACKLOG.json")["backlog"]
audit = load("CURRENT-DATA-AUDIT.json")
receipt = load("INPUT-RECEIPT.json")
source_map = {s["id"]: s for s in sources}
group_map = {g["id"]: g for g in decisions["groups"]}
unit_map = {u["id"]: u for u in units}
draft_map = {d["id"]: d for d in drafts}
candidate_map = {c["id"]: c for c in audit["all_candidate_scopes"]}
profile_ids = set(audit["all_profile_ids"])
policy = audit["slot_dimensions"]

require(len(inventory["rows"]) == 274, "274 source table rows retained")
require(len(set(r["expression_group"] for r in inventory["rows"])) == 217, "217 overlapping expression groups retained")
require(len(inventory["spellings"]) == 234, "234 distinct spellings retained")
require(len(decisions["terms"]) == len(inventory["spellings"]), "every spelling has one decision")
require({t["id"]: t["term"] for t in decisions["terms"]} ==
        {t["id"]: t["term"] for t in inventory["spellings"]}, "term IDs and spellings match inventory")
require(len(group_map) == 42, "42 research work groups; no synonym claim")
require(len(source_map) == 42, "42 source records")
require(len([s for s in sources if s["verification_scope"] != "NO_CONTENT_EVIDENCE"]) == 39,
        "39 relevant-content source records")
require(len(unit_map) == 36 and len(draft_map) == 28 and len(cases) == 92,
        "36 units, 28 drafts and 92 proposed regressions")
require(audit["loader_status"] == "PASS", "saved baseline loader passed")
require(not audit["unresolved_selected_profile_ids"] and not audit["unresolved_selected_candidate_ids"],
        "saved baseline selected references resolved")
require(audit["candidate_limits"] == {"core_per_slot": 4, "support_per_slot": 2, "pack_total": 64},
        "candidate budgets recorded as read from baseline")
row_ids = {r["id"] for r in inventory["rows"]}
covered = []
for group in decisions["groups"]:
    covered.extend(group["terms"])
    require(bool(group["meaning_to_preserve"]) and bool(group["do_not_infer"]),
            group["id"] + " preserves meaning and rejects unsupported inferences")
    require(set(group["semantic_unit_ids"]) <= set(unit_map), group["id"] + " unit references")
    require(set(group["related_source_ids"]) <= set(source_map), group["id"] + " source references")
    require(group["runtime_export_allowed"] is False, group["id"] + " not an active alias group")
require(Counter(covered) == Counter(t["term"] for t in inventory["spellings"]),
        "groups cover every spelling exactly once")
for term in decisions["terms"]:
    require(term["decision_group_id"] in group_map, term["id"] + " decision group exists")
    require(set(term["source_row_ids"]) <= row_ids, term["id"] + " original row references")
    sids = term["term_specific_source_ids"] + term["related_framework_source_ids"]
    require(set(sids) <= set(source_map), term["id"] + " source references")
    require(term["runtime_export_allowed"] is False and term["exact_activation_recommendation"] == "NONE_FROM_RESEARCH",
            term["id"] + " no research-to-runtime exact promotion")
    if term["lexical_evidence_status"].startswith("SPELLING_"):
        require(bool(term["term_specific_source_ids"]), term["id"] + " direct spelling has evidence")
        require(all(term["term"] in source_map[sid]["verified_terms"] for sid in term["term_specific_source_ids"]),
                term["id"] + " direct spelling limited to attested source spelling")
    require(all(source_map[sid]["verification_scope"] != "NO_CONTENT_EVIDENCE"
                for sid in term["term_specific_source_ids"]), term["id"] + " no failed lookup used as lexical evidence")
pending = {t["id"] for t in decisions["terms"] if
           t["lexical_evidence_status"] == "INDIVIDUAL_LEXICAL_EVIDENCE_PENDING"}
require({b["term_id"] for b in backlog} == pending and len(backlog) == 187,
        "lexical backlog matches 187 individually unverified spellings")
for unit in units:
    require(set(unit["source_ids"]) <= set(source_map), unit["id"] + " source references")
    require(set(unit["existing_profile_ids"]) <= profile_ids, unit["id"] + " baseline profile references")
    require(set(unit["existing_candidate_ids"]) <= set(candidate_map), unit["id"] + " baseline candidate references")
    require(unit["runtime_export_allowed"] is False, unit["id"] + " research-only")
    if unit["evidence_mode"] == "VISIBLE_COMPONENTS":
        require(unit["render_gate_policy"]["partial_is_fail"] and
                unit["render_gate_policy"]["occluded_required_component"] == "UNOBSERVABLE",
                unit["id"] + " complete visible proof required")
    else:
        require(unit["render_gate_policy"]["pixel_inference_allowed"] is False,
                unit["id"] + " contextual/temporal evidence not a still-pixel diagnosis")
held = []
for draft in drafts:
    require(set(draft["semantic_unit_ids"]) <= set(unit_map), draft["id"] + " unit references")
    require(set(draft["source_ids"]) <= set(source_map), draft["id"] + " source references")
    require(draft["proposed_slot"] in policy, draft["id"] + " existing slot")
    require(draft["runtime_export_allowed"] is False and not draft["automatic_slang_activation_allowed"] and
            not draft["lexical_aliases_to_add"], draft["id"] + " no automatic alias activation")
    require(draft["status"] == "PROPOSED_NOT_ADOPTED" and
            draft["native_pixels_status"] == "NOT_GENERATED_OR_EVALUATED", draft["id"] + " status boundaries")
    if draft["held_reason"]:
        held.append(draft["id"])
    else:
        require(set(draft["affected_dimensions"]) <= set(policy[draft["proposed_slot"]]),
                draft["id"] + " proposed dimensions within baseline slot policy")
        require(bool(draft["affected_dimensions"]) and bool(draft["affected_properties"]),
                draft["id"] + " explicit conservative effects")
    if draft["reuse_candidate_id"]:
        existing = candidate_map.get(draft["reuse_candidate_id"])
        require(existing is not None, draft["id"] + " actual candidate owner exists in baseline")
        if existing:
            require(draft["proposed_slot"] == existing["slot"] and
                    draft["affected_dimensions"] == existing["affected_dimensions"] and
                    draft["affected_properties"] == existing["affected_properties"] and
                    draft["existing_owner_file"] == existing["owner_file"],
                    draft["id"] + " existing scope and owner preserved")
    if draft["reuse_profile_id"]:
        require(draft["reuse_profile_id"] in profile_ids, draft["id"] + " existing profile reference")
    for effect in draft["affected_properties"]:
        require(set(effect) == {"dimension", "target", "property"} and
                effect["dimension"] in draft["affected_dimensions"] and
                all(isinstance(v, str) and v for v in effect.values()),
                draft["id"] + " explicit target/dimension/property effect")
    require(bool(draft["eligibility_guard"]), draft["id"] + " core eligibility guard")
require(set(held) == {"SV11", "SV13", "SV14", "SV22", "SV23", "SV25"}, "six explicit held drafts")
require(len({c["id"] for c in cases}) == len(cases) and
        len({c["request_ko"] for c in cases}) == len(cases), "unique holdout cases and requests")
for case in cases:
    require(set(case["semantic_unit_ids"]) <= set(unit_map), case["id"] + " unit references")
    require(set(case["candidate_draft_ids"]) <= set(draft_map), case["id"] + " draft references")
    require(case["status"] == "PROPOSED_NOT_RUN" and case["is_holdout"] and
            case["export_to_search_index"] is False, case["id"] + " not run and no retrieval leakage")
require(len(audit["contextual_probes"]) == 22, "22 current-source-row diagnostics separated from holdouts")
require(audit["contextual_probes"][-1]["supplied_polarity"] == "excluded" and
        not audit["contextual_probes"][-1]["hits"], "excluded source row not a positive diagnostic")

link_results = []
for path in OUT.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        dest = (path.parent / unquote(target.strip("<>"))).resolve()
        link_results.append({"file": path.name, "target": target, "exists": dest.exists()})
require(all(x["exists"] for x in link_results), "all local Markdown links resolve")
json_files = sorted(OUT.glob("*.json"))
for path in json_files:
    json.loads(path.read_text())
require(True, "all existing research JSON parses")

drift = []
for file in receipt["files"]:
    path = ROOT / file["path"]
    current = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    if current != file["sha256"]:
        drift.append({"path": file["path"], "baseline_sha256": file["sha256"], "current_sha256": current})
baseline_paths = {file["path"] for file in receipt["files"]}
current_paths = {str(path.relative_to(ROOT)) for path in
                 (ROOT / "skills/photo-prompt-image-generator/assets").rglob("*.json")}
new_paths = sorted(current_paths - baseline_paths)
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
artifacts = [{"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "bytes": path.stat().st_size}
             for path in sorted(OUT.iterdir()) if path.is_file() and path.name != "VALIDATION.json"]
result = {
    "schema_version": "slang-research-validation/v1", "checked_on": "2026-10-03",
    "research_structure_status": "PASS" if not errors else "FAIL",
    "reference_mode": "RECORDED_LIVE_BASELINE",
    "baseline_reference_status": "PASS" if not errors else "FAIL",
    "current_input_state": "DRIFT_DETECTED_RECAPTURE_BEFORE_INTEGRATION" if
        drift or new_paths or head != receipt["head"] else "HASHES_MATCH_BASELINE",
    "check_count": len(checks), "errors": errors,
    "counts": {"spellings": len(decisions["terms"]), "decision_groups": len(group_map),
        "sources": len(sources), "relevant_content_sources": 39, "units": len(units),
        "drafts": len(drafts), "held_drafts": len(held), "proposed_regressions": len(cases),
        "executed_new_regressions": 0, "baseline_diagnostics": len(audit["contextual_probes"]),
        "local_links": len(link_results), "json_files_parsed_before_validation_write": len(json_files)},
    "lexical_evidence_counts": dict(Counter(t["lexical_evidence_status"] for t in decisions["terms"])),
    "regression_category_counts": dict(Counter(c["category"] for c in cases)),
    "native_image_generation": "NOT_PERFORMED", "runtime_integration": "NOT_PERFORMED_BY_THIS_RESEARCH",
    "current_runtime_readiness": "NOT_ASSERTED",
    "baseline_head": receipt["head"], "head_at_validation": head,
    "git_status_at_validation": status, "baseline_file_drift": drift,
    "new_asset_paths_since_baseline": new_paths, "local_links": link_results,
    "artifact_hashes": artifacts,
    "scope_note": "Only this research directory was authored by this task. Shared-checkout mutations are reported without resetting or attributing them. Structural PASS does not assert current loader/index consistency, candidate adoption, prompt quality, native pixels or user acceptance.",
}
(OUT / "VALIDATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"research_structure_status": result["research_structure_status"],
    "check_count": len(checks), "errors": errors, "counts": result["counts"],
    "current_input_state": result["current_input_state"], "changed_baseline_files": len(drift),
    "new_asset_paths": len(new_paths)}, ensure_ascii=False))
raise SystemExit(1 if errors else 0)

