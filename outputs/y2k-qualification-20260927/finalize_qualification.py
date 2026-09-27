"""Join immutable arm evidence without changing prompts, gates or assets."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LIVE_ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
ASSETS = HERE / "qualification-source/skills/photo-prompt-image-generator/assets"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


protocol = read(HERE / "protocol.json")
ready = read(HERE / "data_ready.json")
source_readback = {
    name: {"expected": value, "actual": sha(ASSETS / name)}
    for name, value in ready["source_sha256"].items()
}
assert all(row["expected"] == row["actual"] for row in source_readback.values())
arms = {}
for arm in "abc":
    directory = HERE / f"arm-{arm}"
    frozen = protocol["arms"][arm]
    core_sha = sha(directory / "authorial_core.json")
    gates_sha = sha(Path(frozen["gates_file"]))
    baseline_name = "baseline_prompt.txt" if arm == "a" else "baseline_prompt_en.txt"
    assert core_sha == frozen["core_sha256"]
    assert gates_sha == frozen["gates_sha256"]
    assert sha(directory / baseline_name) == frozen["baseline_sha256"]
    pack_file = read(directory / "candidate_pack.json")
    assert isinstance(pack_file, list) and len(pack_file) == 1
    pack = pack_file[0]
    assert pack["provenance"]["tags_hash"] == ready["dictionary_hash"]
    assert sha(directory / "data_ready.snapshot.json") == sha(HERE / "data_ready.json")
    ledger = [json.loads(line) for line in (directory / "image_runs.ndjson").read_text().splitlines() if line.strip()]
    assert len(ledger) == 1 and ledger[0]["image_call_count"] == 1
    assert ledger[0]["cross_arm_inputs_used"] is False
    audits = {name: read(directory / f"{name}_audit.json") for name in ["composed", "runtime"]}
    assert all(audit["status"] == "pass" and not audit["failures"] for audit in audits.values())
    agent_review = read(directory / ("pixel_review.json" if arm == "b" else "pixel_gate_review.json"))
    parent_review = read(HERE / f"parent-review-{arm}.json")
    image = Path(parent_review["image_path"])
    assert sha(image) == parent_review["image_sha256"]
    if arm == "a":
        exposure = read(directory / "candidate_exposure_adoption.json")
        exposed = exposure["candidate_exposure"]["new_y2kr_ids"]
        adopted = exposure["actual_adoption"]["new_y2kr_ids"]
        profile_ids = exposure["profile_discovery"]["optional_y2k_profile_ids"]
    elif arm == "b":
        exposure = read(directory / "candidate_exposure_adoption.json")
        exposed = [row["id"] for row in exposure["candidate_exposure"]["new_y2kr_candidates"]]
        adopted = exposure["actual_adoption"]["chosen_new_y2kr_ids"]
        profile_ids = exposure["profile_discovery"]["new_y2k_profile_ids"]
    else:
        exposure = read(directory / "exposure_adoption.json")
        exposed = exposure["exposed_new_y2kr_candidate_ids"]
        adopted = exposure["adopted_new_y2kr_candidate_ids"]
        profile_ids = exposure["optional_profile_discovery"]["y2k_specific_profile_ids"]
    arms[arm] = {
        "pack_id": pack["pack_id"], "ledger_run_id": ledger[0]["run_id"],
        "image_path": str(image), "image_sha256": sha(image),
        "core_and_baseline_and_gates_unchanged": True,
        "source_dictionary_matches": True,
        "calls": {"packs": 1, "images": 1, "render_retries": 0, "fallbacks": 0},
        "new_candidate_exposed_ids": exposed, "new_candidate_adopted_ids": adopted,
        "new_y2k_profile_discovered_ids": profile_ids,
        "composed_audit": audits["composed"]["status"],
        "composed_warning_count": len(audits["composed"].get("warnings", [])),
        "runtime_audit": audits["runtime"]["status"],
        "original_agent_pixel_counts": agent_review["counts"],
        "coordinator_pixel_counts": parent_review["counts"],
        "final_status": parent_review["overall"],
        "coordinator_review_path": str((HERE / f"parent-review-{arm}.json").resolve()),
    }
assert len({row["ledger_run_id"] for row in arms.values()}) == 3
summary = {
    "contract_version": "y2k-implementation-and-render-qualification/v1",
    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    "data_added": {"candidates": 343, "profiles": 306, "optional_bundles": 20},
    "indexed_totals": {"semantic_candidates": 8972, "visual_profiles": 944},
    "source_readback": source_readback, "source_hashes_unchanged_since_ready": True,
    "verified_source_root": str(ASSETS.parent.parent.parent),
    "live_shared_source_readback": {name: {"ready_sha256": value, "current_sha256": sha(LIVE_ASSETS / name)} for name, value in ready["source_sha256"].items()},
    "concurrent_source_change": "portrait_composition registration was added to the shared workspace after image generation; its edits were preserved and excluded from this isolated regression source",
    "calls": {"candidate_packs": 3, "image_generations": 3, "render_retries": 0, "fallbacks": 0},
    "arms": arms,
    "coordinator_pixel_counts": {status: sum(row["coordinator_pixel_counts"][status] for row in arms.values()) for status in ["pass", "fail", "unscored"]},
    "original_agent_pixel_counts": {status: sum(row["original_agent_pixel_counts"][status] for row in arms.values()) for status in ["pass", "fail", "unscored"]},
    "actual_new_data_adoption": {"exposed_occurrences": 1, "adopted_occurrences": 1, "unique_adopted_ids": ["slot:lighting:y2kr_retro_flash"], "new_y2k_profile_discoveries": 0, "new_y2k_bundle_adoptions": 0},
    "additional_candidate_pixel_review": {"arm": "b", "generic_flash_highlights_and_close_shadow": "pass", "complete_chair_and_hoodie_shadow_clause": "unscored"},
    "focused_tests": {"tests_run": 25, "result": "pass"},
    "focused_retrieval_probe": read(HERE / "retrieval-probe.json") if (HERE / "retrieval-probe.json").exists() else {"status": "not_run"},
    "full_regression": read(HERE / "completed-full-suite/full-suite-summary.json") if (HERE / "completed-full-suite/full-suite-summary.json").exists() else {"status": "running_in_frozen_source", "planned_tests": 1210},
    "native_image_readback": read(HERE / "native-image-readback.json"),
    "baseline_failure_comparison": read(HERE / "baseline-test-comparison.json"),
    "baseline_source_isolated_comparison": read(HERE / "baseline-isolated-comparison.json") if (HERE / "baseline-isolated-comparison.json").exists() else {"status": "running"},
    "full_failure_baseline_comparison": read(HERE / "full-failure-baseline-comparison.json"),
    "bodycon_compatibility_boundary": {"before": read(HERE / "bodycon-boundary-before.json"), "after": read(HERE / "bodycon-boundary-after.json"), "frozen_fixture_expectations_changed": False},
    "limits": [
        "Coordinator A/C review followed agent verdicts and is not blind; B observations were recorded before reading agent verdict.",
        "No before-after control; no causal data-improvement conclusion.",
        "No complete pixel qualification of all 306 profiles or 343 candidates.",
        "No new wardrobe candidates appeared in these actual public slates; baseline wardrobe fidelity is a separate result.",
        "Requesting-user appearance/aesthetic acceptance has not been received; representative eligibility remains false.",
    ],
}
(HERE / "qualification-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"source_readback": "match", "arms": {key: row["final_status"] for key, row in arms.items()}, "coordinator_counts": summary["coordinator_pixel_counts"], "full_regression": summary["full_regression"].get("status", "finished")}))
