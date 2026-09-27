"""Verify saved independent originals and distinct developmental alternatives.

Metadata integrity is separate from directly recorded pixel judgments.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    protocol, source = load(HERE / "protocol.json"), load(HERE / "source_snapshot.json")
    drift = [p for p, value in source["files"].items() if sha(ROOT / p) != value]
    assert not drift, drift
    assert sha(protocol["reference"]["path"]) == protocol["reference"]["sha256"]
    request = (HERE / "request.txt").read_text()
    assert hashlib.sha256(request.encode()).hexdigest() == protocol["raw_request_sha256"]
    frozen = load(HERE / "coordinator_frozen_cases.json")
    for item in frozen["arms"]:
        arm = HERE / item["arm_id"]
        assert sha(ROOT / item["test_case_file"]) == item["test_case_sha256"]
        assert sha(arm / "authorial_core.json") == item["core_file_sha256"]
        assert sha(arm / "request_envelope.json") == item["envelope_file_sha256"]
    for item in load(HERE / "coordinator_alternative_bindings.json")["cases"]:
        for filename, digest in item["files"].items():
            assert sha(HERE / item["case_id"] / filename) == digest
    extension = load(ROOT / "skills/photo-prompt-image-generator/assets/photo_prompt_portrait_fashion_exposure_extension.json")
    new_candidate_ids = {c["id"] for candidates in extension["slots"].values() for c in candidates}
    new_bundle_ids = {b["id"] for b in extension["visual_semantics"]}
    case_ids = list(protocol["arm_ids"])
    amendment = protocol.get("post_block_amendment", {})
    case_ids += [arm + "/covered-alternative" for arm in amendment.get("applicable_arms", [])]
    cases = []
    for case_id in case_ids:
        arm = HERE / case_id
        envelope = load(arm / "request_envelope.json")
        assert envelope["request_text"] == request
        assert envelope["request_sha256"] == protocol["raw_request_sha256"]
        manifest = load(arm / "run_manifest.json")
        assert manifest["image_call_count"] == 1
        assert manifest["cross_arm_inputs_used"] is False
        assert manifest["reference_sha256"] == [protocol["reference"]["sha256"]]
        assert manifest["source_ref"] == source["source_snapshot_id"]
        assert manifest["skill_sha256"] == source["skill_sha256"]
        assert manifest["tool"] == "image_gen"
        ledger_path = arm / "runs/image_runs.ndjson"
        if not ledger_path.exists():
            ledger_path = arm / "image_runs.ndjson"
        ledger = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]
        assert len(ledger) == 1
        row = ledger[0]
        assert row["run_id"] == manifest["ledger_run_id"]
        assert row["image_call_count"] == 1
        assert row["status"] == manifest["status"]
        composed = load(arm / "composed_prompt.json")
        pack = load(arm / "candidate_pack.json")
        if isinstance(pack, list):
            assert len(pack) == 1
            pack = pack[0]
        pack_id = pack.get("pack_id", pack.get("id"))
        assert composed["pack_id"] == pack_id == manifest["pack_id"] == row["pack_id"]
        assert set(composed["chosen_visual_concept_ids"]) == set(manifest["chosen_visual_concept_ids"])
        assert set(composed["chosen_candidate_ids"]) == set(row["chosen_candidate_ids"])
        assert row["prompt_en"] == composed["prompt_en"]
        assert row["negative_en"] == composed["negative_en"]
        assert row["prompt_id"] == hashlib.sha256(composed["prompt_en"].encode()).hexdigest()[:16]
        assert (arm / "prompt_en.txt").read_text() == composed["prompt_en"]
        assert (arm / "negative_en.txt").read_text() == composed["negative_en"]
        assert load(arm / "composed_audit.json")["status"] == "pass"
        assert load(arm / "runtime_audit.json")["status"] == "pass"
        render = load(arm / "render_request.json")
        assert render["effective_visual_contract_sha256"] == manifest["effective_visual_contract_sha256"]
        runtime_path = arm / "runtime_prompt.txt"
        if not runtime_path.exists():
            runtime_path = arm / "runtime_prompt_en.txt"
        assert render["runtime_prompt_en"] == runtime_path.read_text()
        inputs = render.get("tool_inputs")
        if inputs:
            assert inputs["prompt"] == render["runtime_prompt_en"]
            assert inputs["referenced_image_paths"] == [protocol["reference"]["path"]]
        assert pack["provenance"]["retrieval_query"]["source_authorial_core_sha256"] == manifest["authorial_core_sha256"]
        assert pack["provenance"]["retrieval_query"]["source_intent_lock_sha256"] == manifest["intent_lock_sha256"]
        image_rows = manifest["image_hashes"]
        for image in image_rows:
            assert sha(image["path"]) == image["sha256"]
        result = {"case_id": case_id, "manifest": str(arm / "run_manifest.json"),
                     "ledger_run_id": row["run_id"], "pack_id": pack_id,
                     "image_call_count": 1, "tool_status": manifest["status"],
                     "selected_visual_concepts": composed["chosen_visual_concept_ids"],
                     "selected_candidate_ids": composed["chosen_candidate_ids"],
                     "selection_mode": pack["provenance"]["selection_mode"],
                     "developmental_alternative": "/covered-alternative" in case_id}
        slot_candidates = [c for slot in pack["slots"].values() for c in slot["candidates"]]
        result["new_slot_candidates_exposed"] = [c["id"] for c in slot_candidates if c.get("entry_id") in new_candidate_ids]
        result["new_slot_candidates_adopted"] = [cid for cid in composed["chosen_candidate_ids"] if cid.rsplit(":", 1)[-1] in new_candidate_ids]
        result["new_visual_profiles_exposed"] = [c["id"] for c in pack["visual_concept_candidates"]["candidates"] if c["id"].startswith("visual-concept:pfe_")]
        result["new_visual_profiles_adopted"] = [cid for cid in composed["chosen_visual_concept_ids"] if cid.startswith("visual-concept:pfe_")]
        result["bundles_exposed"] = [c["id"] for c in pack["candidate_bundles"]["candidates"]]
        result["new_bundles_exposed"] = [cid for cid in result["bundles_exposed"] if cid.rsplit(":", 1)[-1] in new_bundle_ids]
        result["new_bundles_adopted"] = [cid for cid in composed["chosen_candidate_ids"] if cid.rsplit(":", 1)[-1] in new_bundle_ids]
        if manifest["status"] == "safety_block":
            assert not image_rows and not manifest["image_paths"]
            review = load(arm / "render_review.json")
            assert review["status"] == "UNSCORED"
            result.update(image=None, scene_result="UNSCORED", target_results=None)
        else:
            assert manifest["status"] == "success" and len(image_rows) == 1
            coordinator = load(arm / "coordinator_pixel_review.json")
            assert coordinator["result_sha256"] == image_rows[0]["sha256"]
            assert coordinator["result_image"] == image_rows[0]["path"]
            audit = load(arm / "coordinator_review_audit.json")
            assert not audit["schema_failures"]
            assert set(coordinator["hard_gates"]) == set(audit["required_hard_gates"])
            assert coordinator["effective_visual_contract_sha256"] == manifest["effective_visual_contract_sha256"]
            for gate in coordinator["hard_gates"].values():
                assert gate["status"] in {"pass", "fail"} and gate["evidence"]
            result.update(image=image_rows[0], target_results=coordinator["target_results"],
                          scene_result=coordinator["scene_result"],
                          derived_gate_pass_count=sum(g["status"] == "pass" for g in coordinator["hard_gates"].values()),
                          derived_gate_count=len(coordinator["hard_gates"]))
        cases.append(result)
    report = {"status": "PASS", "verification_scope": "File, reference, pack, selection, ledger and independent-manifest integrity only; pixel verdicts are separate agent/coordinator judgments.",
              "source_files_verified": len(source["files"]), "independent_arms": len(protocol["arm_ids"]),
              "original_cases": len(protocol["arm_ids"]), "developmental_alternatives": len(case_ids) - len(protocol["arm_ids"]),
              "native_image_calls": len(cases), "retained_images": sum(c["image"] is not None for c in cases),
              "blocked_original_cases": sum(c["scene_result"] == "UNSCORED" for c in cases),
              "new_slot_candidate_inventory": len(new_candidate_ids),
              "new_bundle_inventory": len(new_bundle_ids),
              "new_bundles_exposed": sorted({v for c in cases for v in c["new_bundles_exposed"]}),
              "new_bundles_adopted": sorted({v for c in cases for v in c["new_bundles_adopted"]}),
              "new_slot_candidates_exposed": sorted({v for c in cases for v in c["new_slot_candidates_exposed"]}),
              "new_slot_candidates_adopted": sorted({v for c in cases for v in c["new_slot_candidates_adopted"]}),
              "new_visual_profiles_exposed": sorted({v for c in cases for v in c["new_visual_profiles_exposed"]}),
              "new_visual_profiles_adopted": sorted({v for c in cases for v in c["new_visual_profiles_adopted"]}),
              "retained_image_full_scene_passes": sum(c["scene_result"] == "PASS" for c in cases),
              "cases": cases}
    (HERE / "saved-runs-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
