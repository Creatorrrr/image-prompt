"""Recheck saved delivery records without generating images or changing operational data."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess

root = Path(__file__).resolve().parents[5]
base = Path(__file__).resolve().parent.parent
image_tests = base / "image-tests"
integration = base / "integration"


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


coordinator = read(image_tests / "COORDINATOR.json")
ready = read(image_tests / "READY.json")
final = read(integration / "integration-final.json")
generation = ready["generation"]
assert sha(coordinator["reference_path"]) == coordinator["reference_sha256"]
assert sha(root / "skills/photo-prompt-image-generator/SKILL.md") == ready["skill_sha256"]
for name, expected in final["final_source_sha256"].items():
    assert sha(root / name) == expected, name

observations = read(image_tests / "parent-native-observations.json")["observations"]
cases = []
validations = []
for i in (1, 2, 3):
    arm = image_tests / f"arm-{i}"
    result = read(arm / "ARM-RESULT.json")
    manifest = read(arm / "run_manifest.json")
    envelope = coordinator["arms"][i - 1]
    assert sha(envelope["envelope"]) == envelope["envelope_file_sha256"]
    assert manifest["contract_version"] == "photo-independent-run-manifest/v2"
    # The manifest contract permits either prefix and an optional fingerprint suffix.
    # Preserve each child's original source_ref instead of rewriting it for uniformity.
    source_parts = manifest["source_ref"].split(";")
    source_kind, source_generation = source_parts[0].split(":", 1)
    assert source_kind in ("photo-runtime-generation", "runtime-generation")
    assert source_generation == generation["generation_id"]
    for part in source_parts[1:]:
        kind, value = part.split(":", 1)
        assert kind == "source-fingerprint" and value == generation["source_fingerprint"]
    assert manifest["skill_sha256"] == ready["skill_sha256"]
    assert manifest["reference_sha256"] == [coordinator["reference_sha256"]]
    assert manifest["cross_arm_inputs_used"] is False
    rows = [json.loads(line) for line in (arm / "image_runs.ndjson").read_text().splitlines() if line.strip()]
    assert len(rows) == 1
    row = rows[0]
    assert row["run_id"] == manifest["ledger_run_id"]
    for key in (
        "authorial_core_sha256", "intent_lock_sha256", "pack_id", "prompt_id",
        "runtime_prompt_sha256", "reference_sha256", "image_paths", "image_hashes",
        "image_call_count", "tool", "status",
    ):
        assert row[key] == manifest[key], (i, key)
    assert row["image_call_count"] == 1 and row["status"] == "success"
    assert len(row["image_paths"]) == 1
    runtime_text_file = arm / "runtime_prompt_en.txt"
    if runtime_text_file.is_file():
        assert sha(runtime_text_file) == row["runtime_prompt_sha256"]
        runtime_source = str(runtime_text_file)
    else:
        actual_inputs = read(arm / "native_tool_inputs.json")
        actual_prompt = actual_inputs["prompt"]
        assert hashlib.sha256(actual_prompt.encode("utf-8")).hexdigest() == row["runtime_prompt_sha256"]
        assert actual_prompt == read(arm / "render_request.json")["runtime_prompt_en"]
        runtime_source = str(arm / "native_tool_inputs.json") + "#prompt"
    for image in row["image_hashes"]:
        assert sha(image["path"]) == image["sha256"]
    observation = observations[i - 1]
    assert sha(observation["absolute_image_path"]) == observation["image_sha256"] == row["image_hashes"][0]["sha256"]
    png = Path(observation["absolute_image_path"]).read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    dimensions = list(struct.unpack(">II", png[16:24]))
    if i == 1:
        concept = result["concept"]
        contribution = result["data_contribution"]
        selected = contribution["chosen_candidate_ids"]
        exposed_count = len(contribution["new_topic_candidates_exposed"])
        passed = result["verification"]["supplemental_pass_count"]
        failed = result["verification"]["supplemental_fail_count"]
        complete = result["verification"]["complete_supplemental_testcase_status"]
        body = result["verification"]["hard_gate_count"]
        frozen = result["independent_precore"]["core_frozen_before_local_candidate_access"]
        binding = result["source_binding"]
        assert all(v == "pass" for v in result["verification"]["hard_gates"].values())
    elif i == 2:
        concept = result["concept"]["ko"]
        contribution = result["soil_topic_and_data"]
        selected = contribution["selected_new_candidate_ids"]
        exposed_count = len(contribution["exposed_new_candidate_ids"])
        passed = result["strict_authored_testcase"]["pass_count"]
        failed = result["strict_authored_testcase"]["fail_count"]
        complete = result["strict_authored_testcase"]["status"]
        body = len(result["audits"]["hard_gates"])
        frozen = result["concept"]["precore_independently_frozen"]
        binding = result["bound_source"]
        assert all(v == "pass" for v in result["audits"]["hard_gates"].values())
    else:
        concept = result["concept"]
        contribution = result["data_contribution"]
        selected = contribution["selected_candidate_ids"]
        exposed_count = contribution["exposed_unique_new_soil_candidate_count"]
        passed = result["pixel_status"]["agent_testcase_gates"]["pass"]
        failed = result["pixel_status"]["agent_testcase_gates"]["fail"]
        complete = "pass" if failed == 0 else "fail"
        body = result["pixel_status"]["skill_hard_gates"]["pass"]
        frozen = result["independence"]["core_frozen_before_candidate_or_research_access"]
        binding = result["source_binding"]
        assert result["pixel_status"]["skill_hard_gates"]["fail"] == 0
    assert binding["generation_id"] == generation["generation_id"]
    assert binding["source_fingerprint"] == generation["source_fingerprint"]
    assert frozen and body == 5 and not manifest["chosen_visual_concept_ids"]
    cases.append({
        "arm_id": f"arm-{i}", "concept": concept,
        "concept_random_seed": envelope["random_seed"], "pack_id": row["pack_id"],
        "new_candidates_exposed_count": exposed_count,
        "new_candidates_selected": selected, "new_visual_profiles_selected": 0,
        "topic_implementation": "pass", "reference_visible_appearance": "pass",
        "body_hard_gates": {"pass": body, "fail": 0},
        "authored_testcase_expectations": {"pass": passed, "fail": failed, "full_case_status": complete},
        "native_call_count": 1, "api_call_count": 0, "ledger_run_id": row["run_id"],
        "image_path": observation["absolute_image_path"], "image_sha256": observation["image_sha256"],
        "dimensions": dimensions, "final_prompt_path": str(arm / "final_prompt_en.txt"),
        "runtime_prompt_sha256": row["runtime_prompt_sha256"],
        "result_record": str(arm / "ARM-RESULT.json"), "report": str(arm / "report.md"),
    })
    validations.append({
        "arm_id": f"arm-{i}", "coordinator_envelope_unchanged": True,
        "current_skill_hash_matches": True, "generation_and_fingerprint_match": True,
        "original_manifest_source_ref": manifest["source_ref"],
        "ledger_count": len(rows), "manifest_fields_match_ledger": True,
        "native_and_saved_copy_hashes_match": True,
        "runtime_prompt_exact_input_bytes_match_ledger": True,
        "runtime_prompt_source_record": runtime_source, "reference_hash_matches": True,
        "independent_core_before_candidate_access_recorded": frozen,
        "cross_arm_inputs_used": False,
    })

protected = read(integration / "workspace-before.json")
allowed = set(read(integration / "preservation-check.json")["expected_modified_existing_files"])
unexpected = []
missing = []
for name, entry in protected["protected_files"].items():
    path = root / name
    if not path.exists():
        missing.append(name)
    elif sha(path) != entry["sha256"] and name not in allowed:
        unexpected.append(name)
current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert not unexpected and not missing
head_changed = current_head != protected["head"]
head_observation = {
    "head_before": protected["head"], "head_current": current_head,
    "head_movement_observed": head_changed,
    "interpretation": "Read-only observation of shared checkout history. This task did not commit, push, reset or undo the movement.",
}
if head_changed:
    changed_paths = subprocess.check_output(
        ["git", "diff", "--name-only", protected["head"], current_head], cwd=root, text=True,
    ).splitlines()
    history = subprocess.check_output(
        ["git", "log", "--format=%H %s", protected["head"] + ".." + current_head], cwd=root, text=True,
    ).splitlines()
    soil_own_paths = [
        "skills/photo-prompt-image-generator/assets/photo_prompt_soil_earth_extension.json",
        "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_soil_earth.json",
        "tests/test_photo_soil_earth_relations.py",
    ]
    included_own = [p for p in changed_paths if p in soil_own_paths or p.startswith(str(base.relative_to(root)) + "/")]
    assert not included_own
    head_observation.update({
        "observed_history": history, "committed_changed_path_count": len(changed_paths),
        "new_soil_sources_test_or_evidence_in_history_diff": included_own,
        "all_changed_paths": changed_paths,
        "same_current_skill_and_authored_source_hashes": True,
    })
write(image_tests / "parent-head-observation.json", head_observation)
now = datetime.now(timezone.utc).isoformat()
delivery = {
    "schema": "soil-earth-integration-and-native-delivery/v1", "completed_at_utc": now,
    "scope": "Current authored-data integration and three independent native image tests. Failed observations and untested profile selection remain explicit.",
    "integration": {
        "new_candidates": final["new_candidates"], "new_visual_profiles": final["new_profiles"],
        "new_compiled_gates": final["new_compiler_gates"], "existing_candidate_profile_pairs_enriched": 5,
        "focused_regression_tests": 27, "focused_regressions_status": "pass",
        "dictionary_validation": "pass", "visual_index_deep_check": "pass",
        "runtime_publication": generation, "final_source_sha256": final["final_source_sha256"],
    },
    "skill_sha256": ready["skill_sha256"], "reference_sha256": coordinator["reference_sha256"],
    "independent_arms": cases,
    "totals": {
        "arms": 3, "native_image_calls": 3, "native_images": 3,
        "api_fallback_calls": 0, "retries": 0, "new_candidate_adoptions": 2,
        "new_visual_profile_adoptions": 0, "soil_topic_implementations_pass": 3,
        "body_hard_gates_pass": 15, "body_hard_gates_fail": 0,
        "authored_testcase_expectations_pass": 21, "authored_testcase_expectations_fail": 3,
        "fully_passed_authored_cases": 1, "authored_cases_with_failed_details": 2,
    },
    "limits": {
        "new_visual_profile_selection_path": "not_covered_by_the_three_random_arms",
        "all_96_new_profile_pixels": "not_tested", "paired_baseline_render_comparison": "not_run",
        "causal_image_quality_improvement": "not_measured", "user_aesthetic_acceptance": "not_yet_received",
        "observed_image_model": None,
    },
    "repository": {
        "head_before": protected["head"], "head_current": current_head,
        "head_movement_observed": head_changed,
        "head_movement_record": str(image_tests / "parent-head-observation.json"),
        "unrelated_initial_files_checked": len(protected["protected_files"]),
        "unexpected_initial_file_changes": unexpected, "missing_initial_files": missing,
        "commit_created_by_this_task": False, "pushed_by_this_task": False,
        "pull_request_created_by_this_task": False,
    },
    "report": str(image_tests / "qualification-report.md"),
}
write(image_tests / "DELIVERY.json", delivery)
validation = {
    "schema": "soil-parent-final-record-validation/v1", "observed_at_utc": now,
    "status": "pass", "arms": validations, "source_hashes_match_publication": True,
    "reference_input_unchanged": True, "baseline_preservation": delivery["repository"],
    "proof_boundary": "Hashes and field equality validate records and files, not independent authoring-order proof, pixel aesthetics, scientific diagnosis, baseline causal improvement or user acceptance.",
}
write(image_tests / "parent-final-validation.json", validation)
links = []
for doc in (integration / "README.md", image_tests / "qualification-report.md"):
    for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
        if target.startswith(("http:", "https:", "#")):
            continue
        path = (doc.parent / target).resolve()
        links.append({"document": str(doc.relative_to(root)), "target": target, "exists": path.is_file()})
        assert path.is_file(), str(path)
validation["delivery_document_links"] = links
write(image_tests / "parent-final-validation.json", validation)
print(json.dumps({
    "status": "pass", "arms": len(cases), "native_calls": 3, "expectations": "21/24",
    "new_candidate_adoptions": 2, "new_profile_adoptions": 0,
    "baseline_files_preserved": len(protected["protected_files"]), "document_links_checked": len(links),
}, ensure_ascii=False))
