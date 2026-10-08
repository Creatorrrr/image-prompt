"""Assemble unchanged native bytes and admitted audit records; never render."""
from pathlib import Path
import hashlib
import json
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
RUNS = ROOT / "skills/photo-prompt-image-generator/data/runs/electrical-integration-20261008"
OUT = HERE / "qualification"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def assemble():
    old = load(OUT / "CASE-MANIFEST.json")
    validation = load(HERE / "INTEGRATION-VALIDATION.json")
    generation = validation["runtime"]["generation_id"]
    skill_sha = sha(ROOT / "skills/photo-prompt-image-generator/SKILL.md")
    reference = Path("/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg")
    reference_sha = sha(reference)
    definitions = {
        1: {
            "manifest": RUNS / "arm_1/run_manifest.json",
            "ledger": RUNS / "arm_1/image_runs.ndjson",
            "criteria": RUNS / "arm_1/native_pixel_test_criteria.frozen.json",
            "assessment_name": "native_pixel_test_results.json",
            "concept": "이동 박물관 고전압 시연기 복원",
            "whole_case": "fail",
            "reason": "E07_body_and_contact / embodiment_contact_and_space: 손이 지정한 별도 콘솔 대신 기록지·작업대에 놓임",
            "source_components_passed": None,
            "new_electrical_profile_gates_passed": 6,
            "own_required_result": "전기 형상 4/4, 보조 4/5; 전체 FAIL",
        },
        2: {
            "manifest": RUNS / "arm_2/run_manifest.json",
            "ledger": RUNS / "arm_2/image_runs.ndjson",
            "criteria": RUNS / "arm_2/native_test_criteria.json",
            "assessment_name": "independent_native_test_result.json",
            "concept": "폭풍 속 선박 조타실의 기록과 창 닫기",
            "whole_case": "pass",
            "reason": None,
            "source_components_passed": 4,
            "new_electrical_profile_gates_passed": 0,
            "own_required_result": "독립 필수 5/5; 전체 PASS",
        },
        3: {
            "manifest": RUNS / "arm_3/scope-replay-01/run_manifest.json",
            "ledger": RUNS / "arm_3/scope-replay-01/image_runs.ndjson",
            "criteria": RUNS / "arm_3/independent_pixel_criteria.json",
            "assessment_name": "native_independent_assessment.json",
            "concept": "마지막 등대 기록실의 장치 종료",
            "whole_case": "fail",
            "reason": "fiction_circuit_ownership: 램프로 돌아오는 별도 두 번째 배선 끝점을 추적할 수 없음",
            "source_components_passed": 6,
            "new_electrical_profile_gates_passed": 0,
            "own_required_result": "독립 필수 5/6; 전체 FAIL",
        },
    }
    rows = []
    for prior in old["cases"]:
        arm = prior["arm"]
        spec = definitions[arm]
        run = Path(prior["managed_run"])
        target = OUT / f"case-{arm}"
        workflow = load(run / "workflow.json")
        manifest = load(spec["manifest"])
        ledger_rows = [json.loads(line) for line in spec["ledger"].read_text().splitlines() if line.strip()]
        assert workflow["phase"] == "review_record_validated"
        assert workflow["source_binding"]["generation_id"] == generation
        assert manifest["contract_version"] == "photo-independent-run-manifest/v2"
        assert manifest["image_call_count"] == 1 and len(ledger_rows) == 1
        assert manifest["cross_arm_inputs_used"] is False
        assert manifest["skill_sha256"] == skill_sha
        assert manifest["reference_sha256"] == [reference_sha]
        assert sha(prior["original_native_path"]) == prior["image_sha256"]
        assert sha(target / "image.png") == prior["image_sha256"]
        assert sha(target / "prompt.en.txt") == prior["positive_prompt_sha256"]

        artifact_hashes = {}
        roles = ["request_raw", "request_envelope_input", "request_envelope_normalized",
                 "creative_controls", "authorial_core_input", "authorial_core_normalized",
                 "freeze_receipt", "embodiment_review", "feature_selection", "feature_selection_audit",
                 "pack", "runtime_receipt", "composed", "composed_audit", "render_request",
                 "runtime_audit", "visual_review", "review_audit"]
        for role in roles:
            artifact = workflow["artifacts"].get(role)
            if artifact is None:
                continue
            src = Path(artifact["path"])
            assert sha(src) == artifact["sha256"], role
            dst = target / f"{role}.json"
            shutil.copyfile(src, dst)
            artifact_hashes[role] = sha(dst)
        for name, src in [("run_manifest.json", spec["manifest"]),
                          ("frozen_native_criteria.json", spec["criteria"]),
                          ("independent_native_assessment.json", run / spec["assessment_name"]),
                          ("root_native_review.json", Path(prior["root_review_file"]))]:
            shutil.copyfile(src, target / name)
            artifact_hashes[name] = sha(target / name)
        save(target / "native_ledger_row.json", ledger_rows[0])
        request = load(target / "render_request.json")
        (target / "runtime.prompt.txt").write_bytes(request["runtime_prompt_en"].encode("utf-8"))
        (target / "runtime.negative.txt").write_bytes(request["runtime_negative_en"].encode("utf-8"))
        assert sha(target / "runtime.prompt.txt") == manifest["runtime_prompt_sha256"]
        audit = load(target / "review_audit.json")["visual"]
        assert audit["schema_failures"] == []
        row = dict(prior)
        row.update({
            "concept": spec["concept"],
            "ledger_review_status": workflow["phase"],
            "formal_native_technical_qualification": workflow["technical_qualification"],
            "formal_hard_gate_count": audit["required_hard_gate_count"],
            "formal_failed_hard_gates": audit["failed_hard_gates"],
            "whole_case_required_qualification": spec["whole_case"],
            "whole_case_failure_reason": spec["reason"],
            "own_required_result": spec["own_required_result"],
            "new_electrical_profile_gates_passed": spec["new_electrical_profile_gates_passed"],
            "adopted_slot_components_passed": spec["source_components_passed"],
            "new_electrical_visual_profiles_selected": [x for x in manifest["chosen_visual_concept_ids"] if x.startswith("visual-concept:electric_")],
            "main_electrical_forms_visible": True,
            "user_acceptance": "pending",
            "skill_sha256": skill_sha,
            "reference_sha256": reference_sha,
            "runtime_prompt_sha256": manifest["runtime_prompt_sha256"],
            "native_ledger_run_id": manifest["ledger_run_id"],
            "native_ledger_row_count": len(ledger_rows),
            "original_run_manifest": str(spec["manifest"]),
            "original_ledger": str(spec["ledger"]),
            "frozen_criteria_sha256": sha(spec["criteria"]),
            "proof_copy_sha256": artifact_hashes,
        })
        save(target / "metadata.json", row)
        rows.append(row)
    final = {
        "schema_version": "electrical-native-qualification/v1",
        "cases": rows,
        "native_tool": "image_gen",
        "observed_native_model": "not_observed",
        "call_count": 3,
        "source_generation": generation,
        "source_fingerprint": validation["runtime"]["source_fingerprint"],
        "main_electrical_forms_visible_in_cases": 3,
        "whole_case_required_pass_count": 1,
        "whole_case_required_fail_count": 2,
        "formal_native_technical_pass_count": 2,
        "formal_native_technical_fail_count": 1,
        "unique_new_ordinary_candidate_ids_selected": sorted({c for row in rows for c in row["chosen_candidate_ids"]}),
        "unique_new_electrical_profile_ids_selected": sorted({c for row in rows for c in row["new_electrical_visual_profiles_selected"]}),
        "no_baseline_render_comparison": True,
        "statistical_or_causal_improvement_proved": False,
        "full_new_source_native_coverage_proved": False,
        "user_acceptance": "pending",
        "qualification_completed": True,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    save(OUT / "CASE-MANIFEST.json", final)
    validation["native_qualification"] = {
        "status": "completed",
        "actual_native_image_calls": 3,
        "main_electrical_forms_visible_in_cases": 3,
        "whole_case_required_pass_count": 1,
        "whole_case_required_fail_count": 2,
        "formal_native_technical_pass_count": 2,
        "formal_native_technical_fail_count": 1,
        "user_acceptance": "pending",
        "case_manifest": str(OUT / "CASE-MANIFEST.json"),
    }
    validation["preservation"] = load(HERE / "PRIMARY-PRESERVATION-FINAL.json")
    validation["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    save(HERE / "INTEGRATION-VALIDATION.json", validation)
    print(json.dumps({"call_count": 3, "main_electrical_forms_visible": 3,
                      "whole_case_pass": 1, "whole_case_fail": 2,
                      "original_image_prompt_and_proof_bytes_verified": True}, ensure_ascii=False))


if __name__ == "__main__":
    assemble()
