"""Check the research delivery and record pre-existing source preservation.

This checks document/reference integrity and a bounded tokenizer equivalence
sample. It never validates/registers runtime drafts or dispatches a provider.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit, unquote
import csv
import hashlib
import json
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT = ROOT / "docs/analysis/2026-10-09-summer-fashion-visual-semantics-research.md"
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as pg

def read(name):
    return json.loads((HERE / name).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).rstrip("\n")

def main():
    timestamp = datetime.now(timezone(timedelta(hours=9))).isoformat()
    before = read("workspace-before.json")
    differences = []
    for rel, old in before["files"].items():
        path = ROOT / rel
        new_sha = sha(path) if path.is_file() else None
        if new_sha != old["sha256"]:
            differences.append(dict(path=rel, before_sha256=old["sha256"], after_sha256=new_sha))
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    tracked = git("status", "--short", "--untracked-files=no")
    preservation = dict(
        checked_at=timestamp,
        baseline_captured_at=before["captured_at"],
        protected_files_checked=len(before["files"]),
        unchanged_files=len(before["files"])-len(differences),
        differences=differences,
        baseline_head=before["head"], current_head=head,
        baseline_branch=before["branch"], current_branch=branch,
        head_unchanged=head == before["head"],
        branch_unchanged=branch == before["branch"],
        tracked_status_unchanged=tracked == before["tracked_status"].rstrip("\n"),
        current_tracked_status=tracked,
        action_boundary="Authored only the new summer-fashion research directory and its new analysis report. No restore, stage, commit, index rebuild or runtime publication.",
        status="UNCHANGED" if not differences and head == before["head"] and tracked == before["tracked_status"].rstrip("\n") else "OBSERVED_CONCURRENT_DIFFERENCES_NO_RESTORE"
    )
    write("final-preservation.json", preservation)
    # The report links here. Create the file before resolving local links; the
    # final result below replaces this temporary marker in the same invocation.
    write("final-validation.json", {"status": "RUNNING", "checked_at": timestamp})
    terms, cards, proposals, sources = (read(x) for x in ["term-plan.json", "semantic-cards.json", "candidate-proposals.json", "source-ledger.json"])
    inventory = read("term-inventory.json")
    reg, plan, prior = (read(x) for x in ["regression-plan.json", "implementation-plan.json", "research-validation.json"])
    checks = {}
    counts = dict(seed_rows=len(terms), semantic_cards=len(cards), candidate_drafts=len(proposals), source_rows=len(sources),
                  comparison_pairs=len(reg["comparison_pairs"]), allowed_combinations=len(reg["allowed_combinations"]),
                  mutations=len(reg["mutations"]), pixel_groups=len(reg["pixel_groups"]))
    checks["counts_match_plan_and_build_result"] = counts == plan["counts"] == prior["counts"]
    seed_labels = [line for line in (HERE/"seed-terms.txt").read_text().splitlines() if line.strip() and not line.startswith("#")]
    checks["all_299_seed_rows_in_original_order"] = len(seed_labels) == 299 and seed_labels == [t["term"] for t in terms] == [t["term"] for t in inventory]
    checks["card_and_candidate_ids_unique"] = len({c["id"] for c in cards}) == len(cards) and len({p["id"] for p in proposals}) == len(proposals)
    checks["source_ids_unique"] = len({s["id"] for s in sources}) == len(sources)
    source_ids, card_ids, draft_ids = ({x["id"] for x in rows} for rows in [sources, cards, proposals])
    checks["all_source_references_resolve"] = all(set(c["source_ids"]).issubset(source_ids) for c in cards) and all(set(p["source_ids"]).issubset(source_ids) for p in proposals)
    checks["every_source_is_used_and_has_access_limit"] = source_ids == {s for c in cards for s in c["source_ids"]} and all(s.get("access") and s.get("limits") and s.get("supports") and urlsplit(s["url"]).scheme == "https" for s in sources)
    checks["all_term_card_and_draft_references_resolve"] = all(t["card_id"] in card_ids and set(t["related_family_draft_ids"]).issubset(draft_ids) for t in terms)
    checks["family_mapping_does_not_claim_direct_synonyms"] = all(t["semantic_equivalence_status"] == "requires_variant_specific_review" and t["candidate_assignment_status"] == "family_inventory_only_not_direct_alias_mapping" for t in terms)
    csv_rows = list(csv.DictReader((HERE/"term-plan.csv").open()))
    checks["csv_json_all_exported_fields_agree"] = len(csv_rows) == len(terms) and all(
        all(v == (";".join(t[k]) if isinstance(t[k], list) else str(t[k])) for k, v in row.items())
        for row, t in zip(csv_rows, terms))
    checks["all_relation_types_and_endpoints_present"] = all(
        all(r.get(k) for k in ["subject", "type", "object"]) and "_or_" not in r["type"]
        for p in proposals for r in p["payload_draft"]["relations"])
    checks["research_urls_stay_outside_runtime_payload_drafts"] = all(not re.search(r"https?://", json.dumps(p["payload_draft"])) for p in proposals)
    checks["effect_scope_is_draft_and_does_not_edit_identity_or_body"] = all(
        p["scope_review_status"] == "requires_complete_per_variant_effect_review"
        and p["payload_draft"]["affected_dimensions"] == ["appearance"]
        and all(e["dimension"] == "appearance" and e["target"] == "main_subject" and e["property"].startswith("wardrobe.") for e in p["payload_draft"]["affected_properties"])
        for p in proposals)
    checks["gates_and_runtime_proof_remain_unexecuted"] = reg["status"] == "planned_not_executed" and all(
        all(g["status"] == "planned_not_executed" for g in p["render_gate_drafts"])
        and all(p["proof_status"][k] is False for k in ["runtime_registered", "retrieval_executed", "composition_executed", "pixel_verified", "user_accepted"])
        for p in proposals)
    checks["regression_card_references_resolve"] = all(
        set(row["card_ids"]).issubset(card_ids)
        for key in ["comparison_pairs", "allowed_combinations", "pixel_groups"] for row in reg[key])
    target_names = [n for phase in plan["phases"] for n in phase.get("source_targets", [])]
    checks["implementation_source_targets_and_tests_exist"] = all(
        (ROOT/"skills/photo-prompt-image-generator/assets"/name).is_file() for name in target_names
    ) and all((ROOT/name).is_file() for name in plan["scoped_existing_tests"])
    checks["zero_generation_and_embedding_calls_recorded"] = prior["embedding_calls"] == 0 and prior["image_calls"] == 0

    # Deterministic, bounded comparison to the actual public matching helper.
    # This only tests the audit's caching equivalence; it is not retrieval.
    records = read("current-positive-records.json")
    samples, mismatches = [], []
    for index, term in enumerate(inventory[::11]):
        alias = term["aliases"][-1]
        positive = next((r for r in records if any(h["id"] == r["id"] and alias in h["matched_terms"] for h in term["lexical_neighbors"])), None)
        texts = ([positive["positive_text"]] if positive else []) + [records[(index*31) % len(records)]["positive_text"], "unrelated object beside a plain wall"]
        for value in texts:
            expected = pg.semantic_text_contains_authored_term(value, alias)
            tokens = set(pg.tokenize_bm25f_text(alias, lexicon=[alias]))
            cached = bool(tokens) and tokens.issubset(set(pg.tokenize_bm25f_text(value)))
            samples.append(dict(term_id=term["id"], alias=alias, official=expected, cached=cached))
            if expected != cached:
                mismatches.append(samples[-1])
    checks["bounded_cached_tokenizer_equivalence"] = bool(samples) and not mismatches

    missing_links = []
    local_link_count = 0
    for path in [REPORT, HERE/"semantic-cards.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            target = target.strip("<>")
            if target.startswith("/"):
                local_link_count += 1
                plain = re.sub(r":\d+$", "", unquote(target))
                if not Path(plain).is_file():
                    missing_links.append(dict(document=str(path), target=target))
    checks["all_local_report_links_exist"] = not missing_links
    body = REPORT.read_text()
    checks["human_report_current_counts"] = all(s in body for s in ["원문 용어 299행", "공개 출처 68개", "의미 카드 118개", "후보 문장 초안 166개", "비교 사례 57개", "정상 동시 조합 16개"])
    checks["all_json_artifacts_parse"] = True
    for path in HERE.glob("*.json"):
        json.loads(path.read_text())
    artifact_paths = sorted(p for p in HERE.iterdir() if p.is_file() and p.name != "final-validation.json") + [REPORT]
    manifest = [dict(path=str(p.relative_to(ROOT)), bytes=p.stat().st_size, sha256=sha(p)) for p in artifact_paths]
    result = dict(status="PASS" if all(checks.values()) else "FAIL", checked_at=timestamp,
                  scope="research_artifact_and_reference_integrity_only", counts=counts, checks=checks,
                  tokenizer_samples=len(samples), tokenizer_mismatches=mismatches,
                  local_links_checked=local_link_count, missing_local_links=missing_links,
                  pre_existing_preservation_status=preservation["status"],
                  artifact_sha256=manifest,
                  hash_exclusion="final-validation.json excludes its own hash to avoid a recursive manifest; Python cache directories are not research artifacts.",
                  runtime_validation="not_run", embedding_calls=0, image_calls=0)
    write("final-validation.json", result)
    print(json.dumps({k:result[k] for k in ["status", "scope", "counts", "tokenizer_samples", "local_links_checked", "pre_existing_preservation_status"]}, ensure_ascii=False))
    print(json.dumps(dict(protected_files_checked=preservation["protected_files_checked"], unchanged_files=preservation["unchanged_files"], head_unchanged=preservation["head_unchanged"], tracked_status_unchanged=preservation["tracked_status_unchanged"], failed_checks=[k for k,v in checks.items() if not v]), ensure_ascii=False))
    assert result["status"] == "PASS", result["checks"]

if __name__ == "__main__":
    main()
