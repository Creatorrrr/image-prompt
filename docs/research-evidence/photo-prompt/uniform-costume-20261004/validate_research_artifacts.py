"""Validate research cross-references; does not claim retrieval or pixel success."""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def read(name):
    return json.loads((HERE / name).read_text())

def unique(rows, key, label, errors):
    values = [r[key] for r in rows]
    if len(values) != len(set(values)): errors.append(f"duplicate {label}")
    return set(values)

def run():
    errors = []
    inventory = read("keyword-inventory.json")
    assessments = read("keyword-assessments.json")["rows"]
    ledger = read("sources.json")
    sources = ledger["sources"]
    proposal = read("relation-proposals.json")
    atoms = proposal["atoms"]
    bundle_document = read("bundle-proposals.json")
    bundles = bundle_document["bundles"]
    cases = [json.loads(line) for line in (HERE / "validation-cases.jsonl").read_text().splitlines() if line]
    draft = read("runtime-example-drafts.json")
    baseline = read("baseline-audit.json")
    sid = unique(sources, "id", "source id", errors)
    unique(sources, "url", "source URL", errors)
    aid = unique(atoms, "id", "atom id", errors)
    unique(bundles, "id", "pool id", errors)
    unique(cases, "id", "planned case id", errors)
    iid = unique(inventory, "id", "inventory id", errors)
    rid = unique(assessments, "id", "assessment id", errors)
    expected = {f"UC{n:03d}" for n in range(1, 146)}
    if iid != expected or rid != expected: errors.append("145 reference rows must be retained exactly once")
    if len(sources) != ledger["source_count"]: errors.append("source_count mismatch")
    for source in sources:
        if not source["url"].startswith("https://") or not source["supported_scope_ko"] or not source["limits_ko"]:
            errors.append(f"source scope missing: {source['id']}")
    original = {r["id"]: r for r in inventory}
    used_atoms = set()
    for row in assessments:
        for key in ("label_ko", "section", "subsection", "conversation_description_ko", "provenance"):
            if row[key] != original[row["id"]][key]: errors.append(f"reference changed: {row['id']} {key}")
        if not set(row["source_ids"]).issubset(sid): errors.append(f"unknown source: {row['id']}")
        if not set(row["proposed_atom_ids"]).issubset(aid): errors.append(f"unknown atom: {row['id']}")
        if row["named_version_hard_activation_ready"] is not False: errors.append(f"unvalidated activation promoted: {row['id']}")
        used_atoms.update(row["proposed_atom_ids"])
    if used_atoms != aid: errors.append("an atom is detached from reference inventory")
    if dict(Counter(r["section"] for r in inventory)) != baseline["reference_section_counts"]:
        errors.append("reference section counts changed")
    reuse_ids = set()
    gate_ids = []
    for atom in atoms:
        if not set(atom["source_ids"]).issubset(sid): errors.append(f"unknown atom source: {atom['id']}")
        if len(atom["components"]) < 2 or not atom["confusion_boundaries_ko"]: errors.append(f"incomplete atom: {atom['id']}")
        if atom["relations_proposal"][0]["type"] != "declared_owner_scope": errors.append(f"owner relation missing: {atom['id']}")
        if atom["activation_plan"]["bare_role_alias_hard_activation"] is not False:
            errors.append(f"bare role became hard activation: {atom['id']}")
        for component in atom["components"]:
            gate = component["native_gate_proposal"]
            gate_ids.append(gate["id"])
            if component["owner"] != atom["owner_scope"]: errors.append(f"owner mismatch: {atom['id']}")
            if not component["carrier"] or not component["observable_evidence"]: errors.append(f"empty component: {atom['id']}")
            if gate["review_scale"] != "native" or gate["partial_is_fail"] is not True or gate["occluded"] != "UNOBSERVABLE":
                errors.append(f"gate policy mismatch: {atom['id']}")
        for prop in atom["affected_properties_research"]:
            if prop["runtime_key_status"] != "unvalidated_mapping": errors.append(f"unvalidated property promoted: {atom['id']}")
        reuse_ids.update(atom["reuse_existing_ids"])
    if len(gate_ids) != len(set(gate_ids)): errors.append("duplicate native gate IDs")
    for bundle in bundles:
        if not set(bundle["research_atom_pool"]).issubset(aid): errors.append(f"unknown pool atom: {bundle['id']}")
        if bundle["pool_semantics"] != "research_comparison_pool_not_all_of_bundle" or bundle["candidate_only"] is not True:
            errors.append(f"comparison pool accidentally all-of: {bundle['id']}")
    for case in cases:
        if not set(case["atom_ids"]).issubset(aid): errors.append(f"unknown case atom: {case['id']}")
        if case["status"] != "planned_not_executed": errors.append(f"unexecuted case promoted: {case['id']}")
        if case["request_pair"]["a"] == case["request_pair"]["b"]: errors.append(f"identical pair: {case['id']}")
    if any(d.get("runtime_ready") is not False for d in (proposal, bundle_document, draft)):
        errors.append("research document incorrectly marked runtime ready")
    if not set(draft["research_source_ids"]).issubset(sid) or draft["research_atom_id"] not in aid:
        errors.append("draft source/atom reference broken")
    allowed_candidate = {"id", "ko", "en", "weight", "for_any", "aliases", "keywords", "embedding_text", "concept_units", "relations", "tags", "affected_dimensions", "affected_properties"}
    if set(draft["candidate"]) - allowed_candidate: errors.append("example candidate includes research metadata")
    for field in ("candidate", "profile"):
        serialized = json.dumps(draft[field], ensure_ascii=False)
        if "https://" in serialized or "source_ids" in serialized or "proposal_status" in serialized or "unvalidated_mapping" in serialized:
            errors.append(f"evidence metadata leaked into runtime example {field}")
    terms = draft["profile"]["activation"]["exact_terms"]
    if any(len(term) < 12 for term in terms): errors.append("broad exact term in example")
    active_ids = set()
    drift = []
    for snapshot in baseline["source_snapshots"]:
        path = ROOT / snapshot["path"]
        if not path.exists(): continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != snapshot["sha256"]:
            drift.append(snapshot["path"])
        data = json.loads(raw)
        active_ids.update(p["id"] for p in data.get("profiles", []))
        for entries in data.get("slots", {}).values(): active_ids.update(c["id"] for c in entries)
    missing_reuse = reuse_ids - active_ids
    if missing_reuse: errors.append("missing existing reuse IDs: " + ", ".join(sorted(missing_reuse)))
    outputs = ["research-report.md", "implementation-plan.md", "keyword-catalogue.md", "relation-proposals.md"]
    for name in outputs:
        if not (HERE / name).exists(): errors.append(f"deliverable missing: {name}")
    result = {
        "schema": "uniform-costume-research-validation/v1", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "research integrity and cross references only; no runtime tests, embedding calls or image generation",
        "counts": {"reference_keywords": len(inventory), "assessed_keywords": len(assessments), "sources": len(sources),
            "relation_proposals": len(atoms), "comparison_pools": len(bundles), "native_gate_proposals": len(gate_ids),
            "planned_request_pairs": len(cases), "existing_reuse_ids_confirmed": len(reuse_ids)},
        "proposal_status_counts": dict(Counter(a["proposal_status"] for a in atoms)),
        "source_read_mode_counts": dict(Counter(s["read_mode"] for s in sources)),
        "baseline_asset_drift_paths": drift,
        "drift_note": "Concurrent changes may exist. Drift is not attributed to this research and does not update the saved baseline.",
        "runtime_test_status": "not_run_research_only", "native_pixel_status": "not_generated_or_reviewed",
        "errors": errors, "pass": not errors,
    }
    (HERE / "validation-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(run())
