"""Read-only integrity checks for the three actual surreal=3 image runs.

This validates recorded inputs and outputs. Pixel judgments are separately
authored after inspecting originals; these checks do not establish visual truth.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
REQUEST = "surreal 3 으로 테스트해줘."
REFERENCE = Path("/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg")
EXPECTED_CONTROLS = {
    "sensual": 1, "fetish": 0, "adult_appeal_emphasis": "auto",
    "creativity": 1, "viewer_experience": False,
    "reference_edit_mode": "off", "surreal": 3, "trend_layer": "off",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text_sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


pin = read(OUT / "version-pin.json")
assert sha(ROOT / "skills/photo-prompt-image-generator/SKILL.md") == pin["skill_sha256"]
assert sha(ROOT / "skills/photo-prompt-image-generator/precore/creative_controls.json") == pin["control_definitions_sha256"]
assert read(ROOT / "skills/photo-prompt-image-generator/retrieval-runtime.json") == pin["installed_runtime"]
records = []
for arm in "abc":
    run = ROOT / f"generated/photo-runs/surreal3-fresh-20261024-{arm}"
    workflow = read(run / "workflow.json")
    assert workflow["phase"] == "review_record_validated", (arm, workflow["phase"])
    artifacts = workflow["artifacts"]
    for name, artifact in artifacts.items():
        assert sha(artifact["path"]) == artifact["sha256"], (arm, name, "artifact hash")
    artifact = lambda name: read(artifacts[name]["path"])
    assert Path(artifacts["request_raw"]["path"]).read_text() == REQUEST
    controls = artifact("creative_controls")
    values = {key: value["value"] for key, value in controls["controls"].items()}
    assert controls["overrides"] == {"surreal": 3}
    assert values == EXPECTED_CONTROLS, (arm, values)
    assert controls["source_request_sha256"] == text_sha(REQUEST)
    assert workflow["h_f2_binding"]["generation_id"] == pin["installed_runtime"]["generation_id"]
    assert artifact("composed_audit")["status"] == "pass"
    assert artifact("runtime_audit")["status"] == "pass"
    composed = artifact("composed")
    assert "chosen_candidate_ids" in composed and "chosen_visual_concept_ids" in composed
    render = artifact("render_request")
    plan = artifact("native_plan")
    assert plan["payload"]["prompt"] == render["runtime_prompt_en"]
    assert render["referenced_image_paths"] == [str(REFERENCE)]
    assert plan["payload"]["referenced_image_paths"] == [str(REFERENCE)]
    assert len(render["references"]) == 1
    assert render["references"][0]["sha256"] == sha(REFERENCE)
    manifest = read(run / "run_manifest.json")
    assert len(workflow["operations"]) == 1
    operation = workflow["operations"][0]
    record_args = operation["record_args"]
    ledger_path = Path(record_args[record_args.index("--ledger") + 1])
    if not ledger_path.is_absolute():
        ledger_path = ROOT / ledger_path
    ledger = [json.loads(line) for line in ledger_path.read_text().splitlines() if line]
    ledger = [row for row in ledger if row["run_id"] == manifest["ledger_run_id"]]
    assert len(ledger) == 1 and manifest["image_call_count"] == 1
    row = ledger[0]
    assert row["image_call_count"] == 1 and row["tool"] == "image_gen"
    assert row["status"] == "success"
    assert manifest["cross_arm_inputs_used"] is False and row["cross_arm_inputs_used"] is False
    assert manifest["skill_sha256"] == pin["skill_sha256"]
    assert manifest["reference_sha256"] == [sha(REFERENCE)]
    assert row["prompt_en"] == render["runtime_prompt_en"]
    assert manifest["runtime_prompt_sha256"] == text_sha(render["runtime_prompt_en"])
    prompt_file_text = (run / "final_prompt.txt").read_text()
    assert prompt_file_text in [render["runtime_prompt_en"], render["runtime_prompt_en"] + "\n"]
    assert len(manifest["image_hashes"]) == 1
    for result in manifest["image_hashes"]:
        assert sha(result["path"]) == result["sha256"]
    assert operation["status"] == "complete" and len(operation["attempts"]) == 1
    review = artifact("review_audit")["visual"]
    assert review["schema_failures"] == []
    records.append({
        "arm": arm, "run": str(run), "phase": workflow["phase"],
        "control_override": controls["overrides"], "controls": values,
        "request_sha256": text_sha(REQUEST), "reference_sha256": sha(REFERENCE),
        "skill_sha256": manifest["skill_sha256"],
        "h_f2_generation": workflow["h_f2_binding"]["generation_id"],
        "image_call_count": 1, "images": manifest["image_hashes"],
        "runtime_prompt_sha256": manifest["runtime_prompt_sha256"],
        "runtime_prompt_authoritative_artifact": artifacts["render_request"]["path"],
        "human_prompt_file_has_extra_terminal_newline": prompt_file_text != render["runtime_prompt_en"],
        "ledger": str(ledger_path), "ledger_run_id": manifest["ledger_run_id"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"],
        "chosen_visual_concept_ids": composed["chosen_visual_concept_ids"],
        "compose_and_runtime_audits": "pass",
        "formal_review_record_valid": True,
        "formal_embodiment_technical_qualified": review["technical_qualified"],
        "formal_failed_hard_gates": review["failed_hard_gates"],
        "cross_arm_inputs_used": False,
    })

result = {
    "schema": "surreal3-fresh-integrity-validation/v1", "status": "pass",
    "actual_request": REQUEST, "actual_image_calls": sum(r["image_call_count"] for r in records),
    "runs": records,
    "boundary": "Input/output integrity and recorded review validity only; see coordinator-pixel-review.json for visual judgments. No controlled level-0 versus level-3 effect estimate or whole-source native qualification is inferred.",
}
(OUT / "FINAL-VALIDATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": "pass", "runs": len(records), "actual_image_calls": 3}, ensure_ascii=False))
