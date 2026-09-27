#!/usr/bin/env python3
"""Read back saved source, candidate, frozen-core and image evidence; no rendering."""
import hashlib
import json
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    integration = load(BASE / "integration/verification.json")
    reference = Path("/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg")
    reference_sha = sha(reference)
    arms, gate_counts, pc_counts, profiles = [], Counter(), Counter(), set()
    inputs = [
        ("arm_a", "final_prompt.txt", "baseline_prompt.txt", "pixel_review.json", 3, 4400049719420549872),
        ("arm_b", "prompt_en.txt", None, "pixel_review.json", 3, 1292956637129113158),
        ("arm_c", "final_prompt_en.txt", "baseline_prompt_en.txt", "image_render_review.json", 2, 15331982403002488971),
    ]
    for arm, prompt, baseline, review, passes, seed in inputs:
        directory = BASE / "qualification" / arm
        manifest = load(directory / "run_manifest.json")
        frozen = load(directory / "core_freeze.json")
        core = load(directory / "authorial_core.json")
        composed = load(directory / "composed_prompt.json")
        assert sha(directory / "authorial_core.json") == frozen["authorial_core_file_sha256"]
        envelope_sha = frozen.get("request_envelope_file_sha256", frozen.get("envelope_file_sha256", frozen.get("request_envelope_sha256")))
        assert sha(directory / "request_envelope.json") == envelope_sha
        baseline_bytes = core["baseline_prompt_en"].encode()
        assert hashlib.sha256(baseline_bytes).hexdigest() == frozen["baseline_prompt_sha256"]
        if baseline:
            # Exported text files have one terminal newline; freeze hashes the core string.
            assert (directory / baseline).read_bytes() == baseline_bytes + b"\n"
        ledger = [json.loads(line) for line in (directory / "image_runs.ndjson").read_text().splitlines() if line.strip()]
        assert len(ledger) == 1 and ledger[0]["run_id"] == manifest["ledger_run_id"]
        row = ledger[0]
        assert manifest["image_call_count"] == row["image_call_count"] == 1
        assert manifest["reference_sha256"] == row["reference_sha256"] == [reference_sha]
        assert manifest["cross_arm_inputs_used"] == row["cross_arm_inputs_used"] == False
        assert composed["pack_id"] == manifest["pack_id"] == row["pack_id"]
        catalog_ids = {candidate["id"] for candidate in load(directory / "composer_view.json")["candidate_catalog"]}
        chosen_profiles = set(composed["chosen_visual_concept_ids"])
        assert chosen_profiles.issubset(catalog_ids)
        pc_slots = [candidate for candidate in composed.get("chosen_candidate_ids", []) if candidate.startswith("slot:") and ":pc_" in candidate]
        assert set(pc_slots).issubset(catalog_ids)
        assert chosen_profiles == set(manifest["chosen_visual_concept_ids"])
        pc_profiles = sorted(candidate for candidate in chosen_profiles if candidate.startswith("visual-concept:pc_"))
        profiles.update(pc_profiles)
        source = load(directory / "source_snapshot.json")
        source_files = source.get("files_sha256", source.get("files"))
        file_map = source_files if isinstance(source_files, dict) else {row["path"]: row["sha256"] for row in source_files}
        assert all(sha(ROOT / path) == digest for path, digest in file_map.items())
        images = manifest["image_hashes"]
        assert len(images) == 1
        image = images[0]
        assert sha(image["path"]) == image["sha256"]
        raw = Path(image["path"]).read_bytes()
        assert raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR"
        size = list(struct.unpack(">II", raw[16:24]))
        pixel = load(directory / review)
        assert pixel["result_sha256"] == image["sha256"] and pixel["result_image"] == image["path"]
        gates = pixel["hard_gates"]
        pc_gates = {key: value for key, value in gates.items() if key.startswith("vo_pc_")}
        statuses = Counter(value["status"] for value in gates.values())
        pc_statuses = Counter(value["status"] for value in pc_gates.values())
        assert set(statuses).issubset({"pass", "fail"})
        gate_counts.update(statuses)
        pc_counts.update(pc_statuses)
        coordinator = load(directory / "coordinator_pixel_review.json")
        assert coordinator["image_sha256"] == image["sha256"]
        assert sum(result["status"] == "pass" for result in coordinator["keyword_results"]) == passes
        assert coordinator["frozen_staging_result"]["status"] == "fail"
        arms.append({
            "arm": arm, "seed": seed, "pack_id": manifest["pack_id"], "run_id": manifest["ledger_run_id"],
            "keyword_pass": passes, "keyword_total": 3, "full_frozen_scene_status": "fail", "generation_call_count": 1,
            "image": image, "native_size": size, "selected_new_profile_ids": pc_profiles, "selected_new_slot_ids": pc_slots,
            "new_profile_pixel_gates": dict(pc_statuses), "all_derived_pixel_gates": dict(statuses),
            "exact_scene_failure": coordinator["frozen_staging_result"]["evidence"],
            "canonical_authorial_core_sha256": manifest["authorial_core_sha256"], "intent_lock_sha256": manifest["intent_lock_sha256"],
            "frozen_authorial_core_file_sha256": frozen["authorial_core_file_sha256"],
            "effective_visual_contract_sha256": manifest["effective_visual_contract_sha256"],
            "unchanged_generation_source_files_verified": len(file_map), "prompt_path": str(directory / prompt),
            "report_path": str(directory / "report.md"), "manifest_path": str(directory / "run_manifest.json"),
            "coordinator_review_path": str(directory / "coordinator_pixel_review.json"),
        })
    assert pc_counts == {"pass": 28} and len(profiles) == 7
    assert gate_counts == {"pass": 37, "fail": 6}
    result = {
        "schema_version": "portrait-composition-final-qualification/v1", "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_integration": {key: integration[key] for key in ["status", "counts", "dictionary_hash", "visual_registry_sha256", "preserved_preexisting_index_entries"]},
        "reference_path": str(reference), "reference_sha256": reference_sha,
        "qualification": {
            "independent_arms": 3, "native_image_calls": 3, "keyword_pass": 8, "keyword_total": 9,
            "full_frozen_scene_pass": 0, "full_frozen_scene_total": 3, "new_profiles_selected_and_observed": 7,
            "new_profile_gates": dict(pc_counts), "derived_visual_and_embodiment_gates": dict(gate_counts),
            "additional_exact_assertion_failure_outside_derived_gates": "arm_a: a_offer_camera.grasp requires bottom edge; visible grasp is upper edge",
            "user_judgment": "not_yet_received", "retries": 0, "bundles_jointly_adopted_in_live_arms": 0,
            "coverage_boundary": "Seven of sixteen new profiles were selected. The other nine profiles, all forty-two bundle joint adoptions, and the entire catalog are not pixel-qualified by these three images.",
        },
        "checks": {
            "new_portrait_regression_tests": {"pass": 10, "log": "integration/portrait-final-tests.log"},
            "source_and_index_integrity": "pass",
            "scene_expression_routes": {"pass": 112, "total": 112, "file": "integration/scene-expression-audit.json"},
            "full_repository_suite": {
                "completed": False, "status": "failed_early",
                "attribution_files": ["integration/arm_a_pc_preexisting_failure_diagnostic.json", "integration/broad-failure-attribution-b.json"],
                "boundary": "Failures reproduced with same current code and hash-exact pre-extension data. This comparison does not prove every unexecuted test would pass.",
            },
        }, "arms": arms,
    }
    (BASE / "qualification-summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "pass", "arms_verified": len(arms), "new_profile_gates": dict(pc_counts), "derived_gates": dict(gate_counts), "source_files_verified": [arm["unchanged_generation_source_files_verified"] for arm in arms]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
