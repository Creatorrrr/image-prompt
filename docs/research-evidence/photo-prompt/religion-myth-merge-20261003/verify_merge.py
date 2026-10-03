"""Reconcile the complete run and its narrow recheck against final merge sources."""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def read(path):
    return json.loads(path.read_text())


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def git_bytes(revision, path):
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=REPO)


def main():
    summary = read(HERE / "full-suite/summary.json")
    discovery = read(HERE / "full-suite/discovery.json")
    assert not summary["missing_execution_ids"]
    assert not summary["unexpected_execution_ids"]
    assert not summary["duplicate_execution_ids"]
    assert summary["discovered_tests"] == summary["executed_tests"]
    assert summary["module_count"] == len(discovery["modules"])
    records = {module: read(HERE / "full-suite" / f"{module}.json")
               for module in discovery["modules"]}
    runtime = {p.name: sha(p.read_bytes()) for p in
               (REPO / "skills/photo-prompt-image-generator/scripts").glob("*.py")}
    data = {p.name: sha(p.read_bytes()) for p in
            (REPO / "skills/photo-prompt-image-generator/assets").glob("*.json")}
    rechecked = []
    for path in sorted((HERE / "full-suite-rechecks").glob("tests.*.json")):
        record = read(path)
        module = record["module"]
        assert module in records
        assert Counter(record["executed_ids"]) == Counter(records[module]["executed_ids"])
        rechecked.append({"module": module, "tests": record["tests_run"],
                          "record_sha256": sha(path.read_bytes())})
        records[module] = record
    all_records = [read(HERE / "full-suite" / f"{module}.json")
                   for module in discovery["modules"]] + [
        read(path) for path in (HERE / "full-suite-rechecks").glob("tests.*.json")]
    assert all(r["runtime_sources"] == runtime for r in all_records)
    assert all(r["data_sources"] == data for r in all_records)
    assert Counter(i for r in records.values() for i in r["executed_ids"]) == Counter(discovery["discovered_ids"])
    final_failures = [f for r in records.values() for f in r["failures"]]
    final_errors = [e for r in records.values() for e in r["errors"]]
    unexpected = [i for r in records.values() for i in r["unexpected_successes"]]
    assert not final_failures and not final_errors and not unexpected
    binding = read(HERE / "SOURCE-BINDING.json")
    assert all(sha((REPO / path).read_bytes()) == value for path, value in binding["files"].items())
    proof = read(HERE / "PRESERVATION-PROOF.json")
    local, remote = proof["parents"]
    for path in proof["local_authored_files_byte_unchanged"]:
        assert (REPO / path).read_bytes() == git_bytes(local, path)
    for path in proof["remote_authored_files_byte_unchanged"]:
        assert (REPO / path).read_bytes() == git_bytes(remote, path)
    assets = REPO / "skills/subculture-illustration-image-generator/assets"
    old_name = "photo_regression_baseline_v6.json"
    local_name = "photo_regression_baseline_v6_religion_iconography.json"
    assert (assets / local_name).read_bytes() == git_bytes(local, str((assets / old_name).relative_to(REPO)))
    v7 = read(assets / "photo_regression_baseline_v7.json")
    for key in ("historical_baseline", "parallel_local_baseline"):
        assert sha((assets / v7[key]["path"]).read_bytes()) == v7[key]["sha256"]
    assert all(sha((REPO / path).read_bytes()) == value for path, value in v7["frozen_inputs"].items())
    universal_path = "skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json"
    upstream_universal = json.loads(git_bytes(remote, universal_path))
    merged_universal = copy.deepcopy(read(REPO / universal_path))
    validator_sha = merged_universal["validator_contract"]["sha256"]
    assert validator_sha == sha((REPO / "skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py").read_bytes())
    merged_universal["validator_contract"]["sha256"] = upstream_universal["validator_contract"]["sha256"]
    assert merged_universal == upstream_universal
    retrieval = read(HERE / "MERGED-RETRIEVAL.json")
    assert all(all(arm["selected_meanings_exposed"].values()) for arm in retrieval["arms"].values())
    test_path = "tests/test_photo_candidate_semantics.py"
    payload = {
        "schema_version": "religion-myth-merge-verification/v1",
        "production_source_commit": summary["commit"],
        "complete_initial_run": {
            "tests": summary["executed_tests"], "modules": summary["module_count"],
            "failures": summary["failures"], "errors": summary["errors"],
            "skipped": summary["skipped"], "wall_seconds": summary["wall_seconds"],
            "summary_sha256": sha((HERE / "full-suite/summary.json").read_bytes()),
            "original_failure_records_retained": True,
        },
        "narrow_rechecks": rechecked,
        "latest_results": {
            "distinct_test_ids": len(discovery["discovered_ids"]),
            "failures": final_failures, "errors": final_errors,
            "skipped": [s for r in records.values() for s in r["skipped"]],
            "expected_failures": [i for r in records.values() for i in r["expected_failures"]],
            "unexpected_successes": unexpected,
            "missing_execution_ids": [], "duplicate_execution_ids": [],
        },
        "test_repair": {
            "path": test_path,
            "before_sha256": sha(git_bytes(summary["commit"], test_path)),
            "after_sha256": sha((REPO / test_path).read_bytes()),
            "scope": "Select the clean-beauty bundle and its forgery by stable ID instead of shuffled position; all component, relation, full-view, audit, lock and tamper assertions retained.",
        },
        "all_recorded_photo_runtime_and_data_hashes_match_final_sources": True,
        "runtime_source_count": len(runtime), "data_source_count": len(data),
        "source_binding_matches_final": True,
        "both_authored_parents_and_v6_bytes_preserved": True,
        "universal_v2_only_validator_sha_changed": True,
        "merged_frozen_arm_selected_meanings_all_exposed": True,
        "focused_merge_tests": binding["focused_tests"],
        "native_calls_during_merge": 0,
        "historical_native_pixels": "Six originals preserved; strict final 0/3 PASS is unchanged.",
    }
    (HERE / "VERIFICATION.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"tests": payload["latest_results"]["distinct_test_ids"],
                      "failures": len(final_failures), "errors": len(final_errors),
                      "rechecks": rechecked, "source_hashes_match": True}))


if __name__ == "__main__":
    main()
