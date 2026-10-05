"""Consolidate the full suite and unchanged-source historical-fixture rerun."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


initial = json.loads((HERE / "FULL-REGRESSION-RESULT.json").read_text())
plan = json.loads((HERE / "FULL-REGRESSION-PLAN.json").read_text())
rerun = json.loads((HERE / "FIXTURE-RERUN-RESULT.json").read_text())
repair = json.loads((HERE / "VALIDATOR-REPAIR-REGRESSION-RESULT.json").read_text())
initial_freeze = json.loads((HERE / "SOURCE-AND-TEST-FREEZE.json").read_text())
freeze = json.loads((HERE / "FINAL-SOURCE-AND-TEST-FREEZE.json").read_text())
reviewed_paths = {"skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py",
                  "skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json"}
changed = {name for name, digest in initial_freeze["source_files"].items()
           if freeze["source_files"][name] != digest}
assert changed == reviewed_paths
drift = [name for name, digest in freeze["source_files"].items()
         if sha(ROOT / name) != digest]
assert not drift, f"Sources changed during regression: {drift}"
failed_ids = set()
for group in initial["groups"]:
    log = (ROOT / group["log"]).read_text()
    actual_count = int(re.search(r"Ran (\d+) tests? in", log).group(1))
    assert actual_count == group["expected_tests"]
    if group["exit_code"] == 0:
        assert log.rstrip().endswith("OK")
    else:
        matches = re.findall(r"^(?:ERROR|FAIL): (\w+) \(([^)]+)\)", log, re.M)
        assert matches, f"Unexpected process failure: {group['log']}"
        failed_ids.update(case.rsplit(".", 1)[0] + "." + method
                          for method, case in matches)
expected = {
    "tests.test_photo_makeup_reference_balance.PhotoMakeupReferenceBalanceTests.test_source_observation_is_hash_bound_and_identity_independent",
    "tests.test_photo_makeup_reference_balance.PhotoMakeupReferenceBalanceTests.test_five_frozen_cores_are_distinct_and_share_only_the_makeup_contract",
    "tests.test_photo_poverty_visual_semantics.PhotoPovertyVisualSemanticsTests.test_three_arm_pixel_cases_are_hash_bound_independent_and_fail_closed",
    "tests.test_subculture_illustration_photo_boundary.SubcultureIllustrationPhotoBoundaryTests.test_illustration_modules_do_not_import_photo_runtime",
}
assert failed_ids == expected, f"Unreviewed initial failures: {sorted(failed_ids)}"
assert rerun["exit_code"] == 0 and rerun["all_pass"]
rerun_log = (HERE / rerun["log"]).read_text()
assert rerun_log.rstrip().endswith("OK")
fixture_failure_ids = {case for case in failed_ids if not case.startswith("tests.test_subculture_illustration_photo_boundary.")}
assert set(case.rsplit(".", 2)[0] for case in fixture_failure_ids) <= set(rerun["modules"])
assert repair["all_pass"]
assert "tests.test_subculture_illustration_photo_boundary" in repair["targets"]
for group in repair["groups"]:
    content = (HERE / group["log"]).read_text()
    assert content.rstrip().endswith("OK")
    assert group["exit_code"] == 0 and group["actual_tests"] == group["expected_tests"]
result = {
    "test_count": initial["test_count"],
    "module_count": initial["module_count"],
    "all_pass": True,
    "evidence_method": "All discovered methods executed in eight unittest processes; historical dependency failures replayed with original SHA-verified files; the validator path repair replayed in focused boundary, immutable-history, and universal-contract tests. Test sources and expectations unchanged.",
    "initial_full_result": "FULL-REGRESSION-RESULT.json",
    "initial_failed_test_methods": sorted(failed_ids),
    "initial_failed_subtests": 4,
    "failure_causes": ["Ignored historical makeup JSON and poverty result images absent from managed worktree.",
                       "New V17 helper used a concrete sibling skill path, violating the existing source separation rule."],
    "fixture_rerun": "FIXTURE-RERUN-RESULT.json",
    "validator_repair_regression": "VALIDATOR-REPAIR-REGRESSION-RESULT.json",
    "reviewed_post_full_suite_source_changes": sorted(changed),
    "verified_unchanged_source_and_test_files": len(freeze["source_files"]) - len(changed),
    "verified_final_source_and_test_files": len(freeze["source_files"]),
    "tests_skipped_or_relaxed": 0,
    "source_files_edited_after_full_suite_started": len(changed),
    "test_sources_or_expectations_edited_after_full_suite_started": 0,
}
(HERE / "FINAL-REGRESSION-RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
ownership = json.loads((HERE / "PRIMARY-OWNERSHIP.json").read_text())
historical_docs = {name: digest for name, digest in ownership["owned_files"].items()
                   if name.startswith("docs/research-evidence/photo-prompt/")}
assert all(sha(ROOT / name) == digest for name, digest in historical_docs.items())
proof = json.loads((HERE / "V17-CUTE-DATA-PROOF.json").read_text())
for section in ("source_files", "active_semantic_shards", "immutable_history"):
    assert all(sha(ROOT / name) == digest for name, digest in proof[section].items())
assert sha(ROOT / proof["source_parent_archive"]) == proof["source_parent_archive_sha256"]
verification = {
    "status": "PASS",
    "full_regression": result,
    "v17_runtime": json.loads((HERE / "V17-VALIDATION-AFTER-REPAIR.json").read_text()),
    "source_and_test_freeze_sha256": sha(HERE / "FINAL-SOURCE-AND-TEST-FREEZE.json"),
    "original_cute_research_and_native_evidence_files_preserved": len(historical_docs),
    "previous_manifest_and_pack_files_byte_preserved": len(proof["immutable_history"]),
    "index_rebuild": "INDEX-REBUILD.json",
    "authored_intent_preservation": "MERGE-PRESERVATION.json",
    "new_image_calls_during_main_merge": 0,
    "native_verdicts_unchanged": ["PASS", "BLOCKED_UNSCORED", "FAIL"],
    "user_acceptance": "PENDING",
}
(HERE / "FINAL-VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n")
print(f"{result['test_count']} tests qualified with fixture replay and {repair['test_count']} repair checks; final source/test hashes verified; original native evidence preserved.")
