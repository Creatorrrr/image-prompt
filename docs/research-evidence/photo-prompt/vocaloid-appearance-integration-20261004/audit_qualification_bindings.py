"""Root audit of frozen inputs, real exposed candidates and exact native requests."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = json.loads((HERE / "SOURCE-SNAPSHOT.json").read_text())
REFERENCE = Path("/tmp/codex-remote-attachments/01a10435-e463-7100-8694-4bbcfcbf94be/1AAA2E0B-1BD6-4D66-8E89-B6CC6421F60E/1-사진-1.jpg")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
CONFIG = {
    "arm-a": {"freeze": "precore_freeze.json", "calls": 1, "attempts": [
        ["attempt-01/composed_prompt.json", "attempt-01/composed_audit.json", "attempt-01/render_request.json", "attempt-01/native_arguments.json", "attempt-01/render_request_audit.json", "attempt-01/native_error_evidence.json"]]},
    "arm-b": {"freeze": "freeze_manifest.json", "calls": 1, "attempts": [
        ["composed_prompt.json", "composed_audit.json", "runtime_request.attempt-1.json", "native_tool_inputs.attempt-1.json", "runtime_audit.attempt-1.json", "native_error.attempt-1.json"]]},
    "arm-c": {"freeze": "freeze_manifest.json", "calls": 2, "attempts": [
        ["composed_prompt_attempt_1.json", "composed_audit.json", "runtime_request_attempt_1.json", "native_args_attempt_1.json", "runtime_audit_attempt_1.json", None],
        ["composed_prompt_attempt_2.json", "composed_audit_attempt_2.json", "runtime_request_attempt_2.json", "native_args_attempt_2.json", "runtime_audit_attempt_2.json", None]]},
}


def ids(value):
    result = set()
    if isinstance(value, dict):
        if isinstance(value.get("id"), str):
            result.add(value["id"])
        for child in value.values():
            result.update(ids(child))
    elif isinstance(value, list):
        for child in value:
            result.update(ids(child))
    return result


arms = []
for arm, cfg in CONFIG.items():
    directory = HERE / "qualification" / arm
    manifest = load(directory / "run_manifest.json")
    pack = load(directory / "candidate_pack.json")
    if isinstance(pack, list):
        assert len(pack) == 1
        pack = pack[0]
    freeze = load(directory / cfg["freeze"])
    frozen_files = freeze.get("files", freeze.get("file_sha256"))
    assert isinstance(frozen_files, dict) and frozen_files
    file_checks = {name: sha(directory / name) == digest for name, digest in frozen_files.items()}
    checks = {
        "frozen_files_unchanged": all(file_checks.values()),
        "manifest_v2": manifest["contract_version"] == "photo-independent-run-manifest/v2",
        "pack_v6": pack["contract_version"] == "photo-candidate-pack/v6",
        "pack_identity": manifest["pack_id"] == pack["pack_id"],
        "normalized_core_binding": manifest["authorial_core_sha256"] == pack["authorial_core"]["canonical_sha256"],
        "intent_binding": manifest["intent_lock_sha256"] == pack["authorial_core"]["intent_lock"]["canonical_sha256"],
        "common_snapshot": manifest["source_ref"] == FROZEN["canonical_sha256"],
        "common_skill": manifest["skill_sha256"] == FROZEN["skill_sha256"],
        "no_cross_arm_inputs_declared": manifest["cross_arm_inputs_used"] is False,
        "actual_call_count": manifest["image_call_count"] == cfg["calls"],
        "reference_binding": manifest["reference_sha256"] == [sha(REFERENCE)],
    }
    exposed = set()
    for key in ("slots", "candidate_bundles", "photographic_integration", "photographic_craft", "quality_profile", "visual_concept_candidates"):
        exposed.update(ids(pack.get(key)))
    attempts = []
    for number, names in enumerate(cfg["attempts"], 1):
        composed, audit, request, arguments, runtime_audit = [load(directory / name) for name in names[:5]]
        positive, negative = composed["prompt_en"], composed["negative_en"]
        runtime = positive + ("\n\nAvoid: " + negative if negative else "")
        attempt_checks = {
            "chosen_candidates_exposed": set(composed["chosen_candidate_ids"]) <= exposed,
            "chosen_visual_concepts_exposed": set(composed["chosen_visual_concept_ids"]) <= exposed,
            "composed_audit_pass": audit["status"] == "pass" and not audit["failures"],
            "runtime_audit_pass": runtime_audit["status"] == "pass" and not runtime_audit["failures"],
            "pack_binding": composed["pack_id"] == request["pack_id"] == pack["pack_id"],
            "retrieval_binding": composed["core_retrieval_sha256"] == request["core_retrieval_sha256"] == pack["core_retrieval"]["canonical_sha256"],
            "intent_binding": request["source_intent_lock_sha256"] == manifest["intent_lock_sha256"],
            "negative_unchanged": negative == request["runtime_negative_en"] == pack["negative_en"],
            "exact_native_prompt": arguments["prompt"] == request["runtime_prompt_en"] == runtime,
            "actual_reference_paths": arguments["referenced_image_paths"] == [str(REFERENCE)],
            "reference_request_digest": [(r["path"], r["sha256"]) for r in request["references"]] == [(str(REFERENCE), sha(REFERENCE))],
            "visual_contract_binding": request.get("effective_visual_contract_sha256") == audit.get("effective_visual_contract_sha256"),
        }
        if names[5]:
            error = load(directory / names[5])
            attempt_checks.update({
                "error_preserves_positive": error["request"]["prompt_en"] == positive,
                "error_preserves_negative": error["request"]["negative_en"] == negative,
                "error_preserves_runtime": error["request"]["runtime_prompt_en"] == runtime,
                "structured_output_block": error["outcome"]["error_code"] == "moderation_blocked" and error["outcome"]["moderation_stage"] == "output",
                "exact_error_fidelity": error["raw_error"]["fidelity"] == "exact_string",
            })
        else:
            native = load(directory / f"native_result_attempt_{number}.json")
            copied = directory / "generated_images" / f"attempt-{number}.png"
            returned = [Path(path) for path in native["returned_local_paths"]]
            attempt_checks["original_native_copy_bytes"] = len(returned) == 1 and sha(returned[0]) == sha(copied)
        attempts.append({"attempt": number, "status": "pass" if all(attempt_checks.values()) else "fail", "checks": attempt_checks,
                         "artifact_sha256": {name: sha(directory / name) for name in names if name},
                         "chosen_candidate_ids": composed["chosen_candidate_ids"], "chosen_visual_concept_ids": composed["chosen_visual_concept_ids"]})
    arms.append({"arm_id": arm, "status": "pass" if all(checks.values()) and all(a["status"] == "pass" for a in attempts) else "fail",
                 "checks": checks, "frozen_file_checks": file_checks, "attempts": attempts,
                 "manifest_sha256": sha(directory / "run_manifest.json"), "pack_file_sha256": sha(directory / "candidate_pack.json")})

receipt = {"schema_version": "photo-root-independent-binding-audit/v1", "status": "pass" if all(a["status"] == "pass" for a in arms) else "fail",
           "arms": arms, "actual_native_call_count": sum(c["calls"] for c in CONFIG.values()),
           "delivered_native_images": 2, "boundary": "This checks declared independence, frozen bytes, actual exposures, recorded native request bytes and source-file copies. It does not prove native pixel fidelity or user acceptance."}
(HERE / "ROOT-BINDING-AUDIT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": receipt["status"], "arm_status": {a["arm_id"]: a["status"] for a in arms},
                  "failed_checks": {a["arm_id"]: [k for k, v in a["checks"].items() if not v] + [f"attempt-{t['attempt']}:{k}" for t in a["attempts"] for k, v in t["checks"].items() if not v] for a in arms}}, ensure_ascii=False))
raise SystemExit(0 if receipt["status"] == "pass" else 1)
