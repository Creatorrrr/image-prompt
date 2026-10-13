"""Verify audit coverage, reproducible observations and unchanged operating inputs.

This verifies the evidence ledger, not the correctness of semantic judgments.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as corpus
import photo_role_proposals as roles
import photo_runtime_sources as runtime


def read(name):
    return json.loads((OUT / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    snapshot = read("SOURCE-VERIFICATION.json")
    data = corpus.load(SKILL / "assets")
    require(corpus.digest(data) == snapshot["corpus_sha256"], "authored corpus changed")
    require(data["slot_catalog"] == read("CATALOG-SNAPSHOT.json"), "catalog changed")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(head == snapshot["git_head"], "Git baseline changed")
    for name, expected in snapshot["input_files"].items():
        require(sha(ROOT / name) == expected, "input changed: " + name)
    for name, expected in snapshot["unrelated_tracked_dirty_hashes"].items():
        require(sha(ROOT / name) == expected, "unrelated work changed: " + name)
    require(runtime.code_inventory(SKILL) == snapshot["operating_code_sha256"], "operating code changed")
    search = SKILL / "assets/photo_candidate_search.json"
    require(sha(search) == snapshot["active_search_manifest_sha256"], "search manifest changed")
    pointer = Path(snapshot["runtime_pointer_path"])
    require(sha(pointer) == snapshot["runtime_pointer_sha256"], "runtime CURRENT changed")
    require(json.loads(search.read_text())["corpus_sha256"] == corpus.digest(data), "index source identity differs")
    require(json.loads(pointer.read_text()) == snapshot["runtime_pointer"], "runtime pointer differs")

    inventory = read("INVENTORY.json")
    with (OUT / "REVIEWS.tsv").open() as stream:
        reviews = list(csv.DictReader(stream, delimiter="\t"))
    catalog_ids = set(data["slot_catalog"])
    require(len(reviews) == len(catalog_ids) == 112, "review count differs")
    require({row["slot_id"] for row in reviews} == catalog_ids, "review missing a slot")
    require(len({row["slot_id"] for row in reviews}) == len(reviews), "duplicate review")
    actions = collections.Counter(row["action"] for row in reviews)
    require(dict(actions) == {"redefine": 44, "retain": 45, "contextualize": 5, "generalize": 12, "retire": 6}, "report action counts differ")
    for row in reviews:
        require(set(row) == {"slot_id", "action", "proposed_name", "role_definition_draft", "boundary_or_problem"}
                and all(row.values()), "incomplete review: " + row["slot_id"])
    require(len(inventory) == 112 and {r["slot_id"] for r in inventory} == catalog_ids, "inventory coverage differs")
    counts = collections.Counter(b["slot_id"] for b in data["slot_bindings"].values())
    require(sum(counts.values()) == 12020 and len(data["candidates"]) == 18250, "source counts differ")
    for row in inventory:
        require(row["definition"] == data["slot_catalog"][row["slot_id"]], "definition snapshot differs")
        require(row["linked_binding_count"] == counts[row["slot_id"]], "binding count differs")
    require(sum(row["label_only_description"] for row in inventory) == 112, "description count differs")
    require(sum(row["empty_dimensions"] for row in inventory) == 10, "empty dimensions differ")
    require(sum(row["linked_binding_count"] for row in inventory if row["empty_dimensions"]) == 1515, "empty-dimension binding count differs")
    require(sum(row["dimension_disjoint_bindings"] for row in inventory if not row["empty_dimensions"]) == 182, "disjoint effects differ")
    require(sum(not row["focus_groups"] for row in inventory) == 65, "focus coverage differs")

    cards = [json.loads(line) for line in (OUT / "CANDIDATE-CARDS.jsonl").read_text().splitlines()]
    require(len(cards) == 709 and len({row["candidate"]["id"] for row in cards}) == 709, "card counts differ")
    require({row["slot_id"] for row in cards} == catalog_ids, "representatives missing a slot")
    represented = collections.defaultdict(set)
    for card in cards:
        binding = card["binding"]
        require(data["slot_bindings"][binding["id"]] == binding, "card binding changed")
        require(data["candidates"][binding["candidate_id"]] == card["candidate"], "card candidate changed")
        require(binding["slot_id"] == card["slot_id"], "card slot differs")
        represented[card["slot_id"]].add(binding["id"])
    for slot, count in counts.items():
        if count <= 12:
            require(len(represented[slot]) == count, "rare role not fully represented: " + slot)
    for row in inventory:
        require(set(row["representative_candidate_ids"]) == {
            card["candidate"]["id"] for card in cards if card["slot_id"] == row["slot_id"]
        }, "inventory examples differ")

    by_candidate = collections.defaultdict(list)
    for bid, binding in data["slot_bindings"].items():
        by_candidate[binding["candidate_id"]].append(bid)
    probes = read("ROLE-FIT-PROBES.json")
    require(len(probes) == 4, "probe count differs")
    for probe in probes:
        actual = roles.propose(data, probe["target_slot"], probe["candidate_id"], by_candidate[probe["candidate_id"]])
        require(actual == probe["proposal"], "fit probe cannot be reproduced")
        require(probe["content"] == data["candidates"][probe["candidate_id"]]["content"], "probe content changed")
    require([row["proposal"]["applicability_status"] for row in probes] == ["eligible", "review_required", "review_required", "eligible"], "fit observations differ")

    plan = ROOT / "docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md"
    stages = re.findall(r"^## ([0-8])단계", plan.read_text(), re.M)
    require(stages == [str(number) for number in range(9)], "plan stage ordering differs")
    result_path = OUT / "AUDIT-VERIFICATION.json"
    for path in [OUT / "REPORT.ko.md", plan]:
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" not in link:
                target = (path.parent / link).resolve()
                require(target.exists() or target == result_path, "missing report link: " + link)
    for path in OUT.iterdir():
        if path.is_file():
            require(not any(line.endswith(b" ") or line.endswith(b"\t") or line.endswith(b"\r")
                            for line in path.read_bytes().split(b"\n")), "whitespace issue: " + path.name)

    changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    expected_dirty = set(snapshot["unrelated_tracked_dirty_hashes"]) | {str(plan.relative_to(ROOT))}
    require(set(changed) <= expected_dirty, "unexpected tracked change")
    result = {
        "verified": True,
        "git_head": head,
        "corpus_sha256": corpus.digest(data),
        "slot_review_coverage": [112, 112],
        "candidate_cards_verified": 709,
        "all_rare_slot_bindings_represented": True,
        "action_counts": dict(actions),
        "reproduced_role_fit_probes": 4,
        "plan_stages": stages,
        "authored_source_unchanged": True,
        "operating_code_unchanged": True,
        "search_manifest_unchanged": True,
        "runtime_current_unchanged": True,
        "unrelated_tracked_dirty_files_unchanged": sorted(snapshot["unrelated_tracked_dirty_hashes"]),
        "provider_calls": 0,
        "semantic_judgments_automatically_verified": False,
        "end_to_end_search_executed": False,
        "pixels_evaluated": False,
        "evidence_sha256": {path.name: sha(path) for path in sorted(OUT.iterdir())
                            if path.is_file() and path != result_path},
        "plan_sha256": sha(plan),
    }
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in {"evidence_sha256", "unrelated_tracked_dirty_files_unchanged"}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
