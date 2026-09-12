"""Validate this research package, not runtime retrieval or image quality."""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS

def read(name):
    return json.loads((HERE / name).read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

inventory = read("input-inventory.json")
terms = read("term-map.json")["rows"]
sources = read("sources.json")["sources"]
proposals = read("visual-proposals.json")["proposals"]
bundles = read("candidate-bundles.json")["bundles"]
plans = read("integration-plan.json")["rows"]
cases = [json.loads(x) for x in (HERE / "evaluation-cases.jsonl").read_text().splitlines() if x.strip()]
audit = read("repo-audit.json")
checks = []
def check(name, condition):
    checks.append({"name": name, "passed": bool(condition)})

source_ids = {x["id"] for x in sources}
proposal_ids = {x["id"] for x in proposals}
check("source_ids_unique", len(source_ids) == len(sources))
check("proposal_ids_unique", len(proposal_ids) == len(proposals))
check("bundle_and_case_ids_unique", len({x["id"] for x in bundles}) == len(bundles)
      and len({x["id"] for x in cases}) == len(cases))
check("original_occurrences_preserved", Counter((i+1, x["term"])
      for i,g in enumerate(inventory["groups"]) for x in g["terms"])
      == Counter((x["source_section"],x["term"]) for x in terms))
check("all_term_context_refs_resolve", all(set(x["context_source_ids"]) <= source_ids
      and set(x["proposal_ids"]) <= proposal_ids for x in terms))
check("proposal_source_refs_resolve", all(x["source_ids"] and set(x["source_ids"]) <= source_ids for x in proposals))
check("component_evidence_and_confounders", all(len(x["components"]) >= 3
      and len(x["contrast_examples_ko"]) >= 2
      and all(c["prompt_fragment_en"] and c["review_scale"] in {"native","thumbnail","both"} for c in x["components"])
      for x in proposals))
check("intent_dimensions_are_existing", all(set(x["affected_dimensions"]) <= AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
      for x in proposals+bundles))
check("bundle_links_resolve", all(set(x["component_proposal_ids"]) <= proposal_ids for x in bundles))
check("broad_terms_never_automatically_hard", all(not x["broad_label_hard_activation"] for x in terms)
      and all(not x["activation"]["broad_term_alone_hard_eligible"] for x in proposals))
check("all_proposals_have_integration_plan", {x["proposal_id"] for x in plans} == proposal_ids)
slots = set(read("../../../../skills/photo-prompt-image-generator/assets/photo_prompt_tags.json")["slots"])
check("proposed_slots_exist", all(x["proposed_slot"] in slots for x in plans))
existing = {x["id"] for x in audit["selected_existing_records"]}
check("case_targets_resolve", all(x["target"] in proposal_ids or
      (x["target"].startswith("existing:") and x["target"].split(":",1)[1] in existing) for x in cases))
check("evaluation_and_render_not_claimed", all(x["status"] == "NOT_RUN" for x in cases)
      and all(x["render_status"] == "NOT_RUN" for x in proposals)
      and all(x["pixel_status"] == "NOT_RUN" and x["runtime_status"] == "NOT_INTEGRATED" for x in bundles))
check("runtime_authored_files_unchanged_since_audit", all(sha(ROOT / x["path"]) == x["sha256"] for x in audit["source_files"]))
report = (HERE / "report.md").read_text()
local_links = re.findall(r"\]\((/Users/[^)]+)\)",report)
check("report_local_links_resolve", all(Path(x).exists() or x == str(HERE / "validation.json") for x in local_links))
check("report_citation_ids_resolve", set(re.findall(r"\[S(\d{2})\]",report)) <= {x[1:] for x in source_ids})
check("all_sources_have_https_urls", all(x["url"].startswith("https://") for x in sources))
files = {p.name: sha(p) for p in HERE.iterdir() if p.is_file() and p.name != "validation.json"}
result = {
    "schema_version": "photo-research-validation/v1",
    "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
    "checked_at": "2026-09-12",
    "counts": {"source_groups": len(inventory["groups"]), "term_occurrences":len(terms),
       "unique_terms":len({x["term"] for x in terms}), "sources":len(sources),
       "visual_proposals":len(proposals), "candidate_bundles":len(bundles),
       "design_cases":len(cases), "local_exact_lookup_queries":len(audit["exact_match_diagnostic"])},
    "checks": checks, "artifact_sha256": files,
    "validation_boundary": "Research artifact consistency and read-only exact lookup only.",
    "runtime_integration":"NOT_IMPLEMENTED", "candidate_exposure":"NOT_RUN",
    "composed_audit":"NOT_RUN", "render":"NOT_RUN", "pixel_review":"NOT_RUN",
    "improvement_claim":"NOT_ESTABLISHED", "user_judgment":"NOT_REQUESTED"
}
(HERE / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status":result["status"], "counts":result["counts"],
      "failed_checks":[c["name"] for c in checks if not c["passed"]]}, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["status"] == "PASS" else 1)

